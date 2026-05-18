"""Items routes — report, search, browse lost & found items."""
from datetime import datetime
from flask import Blueprint, request, jsonify, g
from config import Config
from utils.db import query, execute, mongo
from utils.auth import require_auth
from utils.matching import find_matches

bp = Blueprint("items", __name__, url_prefix="/api/items")


def _serialise_item(item: dict, include_photos: bool = True) -> dict:
    item = dict(item)
    for k in ("event_date", "created_at", "updated_at"):
        if item.get(k):
            item[k] = item[k].isoformat() if hasattr(item[k], "isoformat") else str(item[k])
    if item.get("latitude") is not None:
        item["latitude"] = float(item["latitude"])
    if item.get("longitude") is not None:
        item["longitude"] = float(item["longitude"])
    if include_photos:
        photos = query(
            "SELECT photo_url FROM item_photos WHERE item_id = %s ORDER BY sort_order",
            (item["id"],),
        )
        item["photos"] = [p["photo_url"] for p in photos]
        tags = query("SELECT tag FROM item_tags WHERE item_id = %s", (item["id"],))
        item["tags"] = [t["tag"] for t in tags]
    return item


@bp.get("/categories")
def list_categories():
    return jsonify({"categories": Config.CATEGORIES})


@bp.get("")
def list_items():
    """Browse / search items with filters.

    Query params: q, type (lost|found), category, location,
                  date_from, date_to, limit, offset
    """
    q = request.args.get("q", "").strip()
    type_ = request.args.get("type")
    category = request.args.get("category")
    location = request.args.get("location")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    limit = min(int(request.args.get("limit", 20)), 100)
    offset = int(request.args.get("offset", 0))

    sql = "SELECT i.*, u.display_name AS user_name FROM items i JOIN users u ON i.user_id = u.id WHERE i.status = 'active'"
    params = []

    if type_ in ("lost", "found"):
        sql += " AND i.type = %s"; params.append(type_)
    if category:
        sql += " AND i.category = %s"; params.append(category)
    if location:
        sql += " AND i.location LIKE %s"; params.append(f"%{location}%")
    if date_from:
        sql += " AND i.event_date >= %s"; params.append(date_from)
    if date_to:
        sql += " AND i.event_date <= %s"; params.append(date_to)
    if q:
        sql += " AND (i.title LIKE %s OR i.description LIKE %s)"
        params.extend([f"%{q}%", f"%{q}%"])

    sql += " ORDER BY i.created_at DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    rows = query(sql, tuple(params))
    return jsonify({"items": [_serialise_item(r) for r in rows], "limit": limit, "offset": offset})


@bp.get("/<int:item_id>")
def get_item(item_id):
    item = query(
        "SELECT i.*, u.display_name AS user_name, u.email AS reporter_email "
        "FROM items i JOIN users u ON i.user_id = u.id WHERE i.id = %s",
        (item_id,), one=True,
    )
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"item": _serialise_item(item)})


@bp.post("")
@require_auth
def create_item():
    data = request.get_json() or {}
    required = ("type", "title", "category", "event_date")
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    if data["type"] not in ("lost", "found"):
        return jsonify({"error": "type must be 'lost' or 'found'"}), 400
    if data["category"] not in Config.CATEGORIES:
        return jsonify({"error": f"category must be one of {Config.CATEGORIES}"}), 400

    item_id = execute(
        """INSERT INTO items (user_id, type, title, description, category,
           location, latitude, longitude, event_date)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (g.user["id"], data["type"], data["title"], data.get("description"),
         data["category"], data.get("location"), data.get("latitude"),
         data.get("longitude"), data["event_date"]),
        return_id=True,
    )

    for i, url in enumerate(data.get("photos") or []):
        execute("INSERT INTO item_photos (item_id, photo_url, sort_order) VALUES (%s,%s,%s)",
                (item_id, url, i))

    for tag in (data.get("tags") or [])[:5]:
        execute("INSERT IGNORE INTO item_tags (item_id, tag) VALUES (%s, %s)",
                (item_id, tag.strip().lower()[:50]))

    # Log event to MongoDB for analytics
    try:
        mongo().item_events.insert_one({
            "item_id": item_id, "event": "created",
            "user_id": g.user["id"], "type": data["type"],
            "category": data["category"], "timestamp": datetime.utcnow(),
        })
    except Exception as e:
        print(f"[MongoDB] log failed: {e}")

    created = query("SELECT * FROM items WHERE id = %s", (item_id,), one=True)
    matches = find_matches(created, threshold=0.5, limit=5)

    # Create notifications for matches
    for m in matches:
        execute(
            "INSERT INTO notifications (user_id, type, title, body, link_url) "
            "VALUES (%s, 'match', %s, %s, %s)",
            (m["user_id"], "Potential match found",
             f"A new {data['type']} report may match your {m['type']} item: {m['title']}",
             f"/items/{item_id}"),
        )

    return jsonify({"item": _serialise_item(created), "matches": [_serialise_item(m) for m in matches]}), 201


@bp.put("/<int:item_id>")
@require_auth
def update_item(item_id):
    item = query("SELECT * FROM items WHERE id = %s", (item_id,), one=True)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if item["user_id"] != g.user["id"] and g.user["role"] == "student":
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    allowed = ["title", "description", "category", "location", "latitude", "longitude", "event_date", "status"]
    updates, params = [], []
    for f in allowed:
        if f in data:
            updates.append(f"{f} = %s"); params.append(data[f])
    if not updates:
        return jsonify({"error": "No fields to update"}), 400
    params.append(item_id)
    execute(f"UPDATE items SET {', '.join(updates)} WHERE id = %s", tuple(params))
    return jsonify({"ok": True})


@bp.delete("/<int:item_id>")
@require_auth
def delete_item(item_id):
    item = query("SELECT * FROM items WHERE id = %s", (item_id,), one=True)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if item["user_id"] != g.user["id"] and g.user["role"] == "student":
        return jsonify({"error": "Forbidden"}), 403
    execute("UPDATE items SET status = 'removed' WHERE id = %s", (item_id,))
    return jsonify({"ok": True})


@bp.get("/<int:item_id>/matches")
@require_auth
def item_matches(item_id):
    item = query("SELECT * FROM items WHERE id = %s", (item_id,), one=True)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if item["user_id"] != g.user["id"] and g.user["role"] == "student":
        return jsonify({"error": "Forbidden"}), 403
    matches = find_matches(item, threshold=0.4, limit=10)
    return jsonify({"matches": [_serialise_item(m) for m in matches]})


@bp.get("/mine")
@require_auth
def my_items():
    rows = query(
        "SELECT * FROM items WHERE user_id = %s ORDER BY created_at DESC",
        (g.user["id"],),
    )
    return jsonify({"items": [_serialise_item(r) for r in rows]})
