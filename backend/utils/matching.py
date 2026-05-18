"""Rule-based matching engine between lost & found items."""
import re
from utils.db import query


def tokenize(text: str) -> set:
    return set(re.findall(r"\w+", (text or "").lower()))


def score_match(a: dict, b: dict) -> float:
    """Score similarity between two item dicts on a 0-1 scale."""
    score = 0.0

    # Category match (40%)
    if a.get("category") == b.get("category"):
        score += 0.40

    # Keyword overlap in title + description (40%)
    toks_a = tokenize(a.get("title", "") + " " + (a.get("description") or ""))
    toks_b = tokenize(b.get("title", "") + " " + (b.get("description") or ""))
    if toks_a and toks_b:
        common = toks_a & toks_b
        union = toks_a | toks_b
        score += 0.40 * (len(common) / len(union))

    # Location overlap (10%)
    if a.get("location") and b.get("location"):
        loc_a = set(a["location"].lower().split())
        loc_b = set(b["location"].lower().split())
        if loc_a & loc_b:
            score += 0.10

    # Date proximity (10%) — within 14 days
    da, db_ = a.get("event_date"), b.get("event_date")
    if da and db_:
        diff = abs((da - db_).days)
        if diff <= 14:
            score += 0.10 * (1 - diff / 14)

    return round(score, 3)


def find_matches(item: dict, threshold: float = 0.5, limit: int = 10) -> list:
    """Given a lost item, find candidate found items (or vice versa)."""
    opposite = "found" if item["type"] == "lost" else "lost"
    candidates = query(
        "SELECT * FROM items WHERE type = %s AND status = 'active' AND user_id != %s "
        "ORDER BY created_at DESC LIMIT 200",
        (opposite, item["user_id"]),
    )

    scored = []
    for c in candidates:
        s = score_match(item, c)
        if s >= threshold:
            scored.append({**c, "match_score": s})

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:limit]
