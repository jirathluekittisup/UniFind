"""Notification routes — list and mark notifications as read."""
from flask import Blueprint, jsonify, g
from utils.db import query, execute
from utils.auth import require_auth

bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")


@bp.get("")
@require_auth
def list_notifications():
    rows = query(
        "SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC LIMIT 50",
        (g.user["id"],),
    )
    for r in rows:
        if r.get("created_at"):
            r["created_at"] = r["created_at"].isoformat()
    unread = query(
        "SELECT COUNT(*) c FROM notifications WHERE user_id = %s AND is_read = FALSE",
        (g.user["id"],), one=True,
    )["c"]
    return jsonify({"notifications": rows, "unread_count": unread})


@bp.put("/<int:notif_id>/read")
@require_auth
def mark_read(notif_id):
    execute(
        "UPDATE notifications SET is_read = TRUE WHERE id = %s AND user_id = %s",
        (notif_id, g.user["id"]),
    )
    return jsonify({"ok": True})


@bp.put("/read-all")
@require_auth
def mark_all_read():
    execute(
        "UPDATE notifications SET is_read = TRUE WHERE user_id = %s",
        (g.user["id"],),
    )
    return jsonify({"ok": True})
