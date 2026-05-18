"""Messaging routes — in-app chat between claimant and item owner."""
import re
from flask import Blueprint, request, jsonify, g
from utils.db import query, execute
from utils.auth import require_auth

bp = Blueprint("messages", __name__, url_prefix="/api/messages")

# Content safety — block phone numbers, emails, URLs
PHONE_RE = re.compile(r"(\+?\d[\d\s\-()]{6,}\d)")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
URL_RE   = re.compile(r"https?://\S+|www\.\S+")


def contains_pii(text: str) -> bool:
    return bool(PHONE_RE.search(text) or EMAIL_RE.search(text) or URL_RE.search(text))


def _serialise(m: dict) -> dict:
    m = dict(m)
    if m.get("created_at"):
        m["created_at"] = m["created_at"].isoformat() if hasattr(m["created_at"], "isoformat") else str(m["created_at"])
    return m


def _authorised_for_claim(claim_id: int, user_id: int) -> dict | None:
    claim = query(
        """SELECT c.*, i.user_id AS item_owner_id
           FROM claims c JOIN items i ON c.item_id = i.id
           WHERE c.id = %s""", (claim_id,), one=True,
    )
    if not claim:
        return None
    if user_id in (claim["claimant_id"], claim["item_owner_id"]):
        return claim
    return None


@bp.get("/claim/<int:claim_id>")
@require_auth
def list_messages(claim_id):
    claim = _authorised_for_claim(claim_id, g.user["id"])
    if not claim:
        return jsonify({"error": "Claim not found or forbidden"}), 404
    rows = query(
        """SELECT m.*, u.display_name AS sender_name
           FROM messages m JOIN users u ON m.sender_id = u.id
           WHERE m.claim_id = %s ORDER BY m.created_at ASC""",
        (claim_id,),
    )
    return jsonify({"messages": [_serialise(r) for r in rows]})


@bp.post("/claim/<int:claim_id>")
@require_auth
def send_message(claim_id):
    claim = _authorised_for_claim(claim_id, g.user["id"])
    if not claim:
        return jsonify({"error": "Claim not found or forbidden"}), 404
    if claim["status"] not in ("approved", "pending"):
        return jsonify({"error": "Cannot message on a closed claim"}), 400

    data = request.get_json() or {}
    body = (data.get("body") or "").strip()
    if not body:
        return jsonify({"error": "body is required"}), 400
    if len(body) > 500:
        return jsonify({"error": "Message too long (500 char max)"}), 400

    is_flagged = contains_pii(body)
    if is_flagged:
        return jsonify({
            "error": "Message blocked: do not share phone numbers, emails, or links. "
                     "Use the in-app chat to arrange meetups safely."
        }), 400

    msg_id = execute(
        "INSERT INTO messages (claim_id, sender_id, body, is_flagged) VALUES (%s,%s,%s,%s)",
        (claim_id, g.user["id"], body, is_flagged), return_id=True,
    )

    # Notify the other party
    other_id = claim["item_owner_id"] if g.user["id"] == claim["claimant_id"] else claim["claimant_id"]
    execute(
        "INSERT INTO notifications (user_id, type, title, body, link_url) "
        "VALUES (%s, 'message', %s, %s, %s)",
        (other_id, "New message",
         f"{g.user['display_name']}: {body[:60]}",
         f"/chat/{claim_id}"),
    )

    msg = query("SELECT * FROM messages WHERE id = %s", (msg_id,), one=True)
    return jsonify(_serialise(msg)), 201
