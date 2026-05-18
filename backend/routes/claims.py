"""Claim routes — submit, approve, reject, list claims."""
from flask import Blueprint, request, jsonify, g
from utils.db import query, execute
from utils.auth import require_auth

bp = Blueprint("claims", __name__, url_prefix="/api/claims")


def _serialise(c: dict) -> dict:
    c = dict(c)
    for k in ("created_at", "updated_at"):
        if c.get(k):
            c[k] = c[k].isoformat() if hasattr(c[k], "isoformat") else str(c[k])
    return c


@bp.post("")
@require_auth
def create_claim():
    data = request.get_json() or {}
    item_id = data.get("item_id")
    proof = (data.get("proof") or "").strip()

    if not item_id or not proof:
        return jsonify({"error": "item_id and proof are required"}), 400
    if len(proof) < 10:
        return jsonify({"error": "Proof must be at least 10 characters"}), 400

    item = query("SELECT * FROM items WHERE id = %s", (item_id,), one=True)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if item["user_id"] == g.user["id"]:
        return jsonify({"error": "Cannot claim your own item"}), 400
    if item["status"] != "active":
        return jsonify({"error": "Item is not active"}), 400

    existing = query(
        "SELECT id FROM claims WHERE item_id = %s AND claimant_id = %s AND status = 'pending'",
        (item_id, g.user["id"]), one=True,
    )
    if existing:
        return jsonify({"error": "You already have a pending claim on this item"}), 409

    claim_id = execute(
        "INSERT INTO claims (item_id, claimant_id, proof) VALUES (%s, %s, %s)",
        (item_id, g.user["id"], proof), return_id=True,
    )

    execute(
        "INSERT INTO notifications (user_id, type, title, body, link_url) "
        "VALUES (%s, 'claim', %s, %s, %s)",
        (item["user_id"], "New claim on your item",
         f"{g.user['display_name']} submitted a claim on '{item['title']}'",
         f"/claims/{claim_id}"),
    )

    claim = query("SELECT * FROM claims WHERE id = %s", (claim_id,), one=True)
    return jsonify(_serialise(claim)), 201


@bp.get("/mine")
@require_auth
def my_claims():
    rows = query(
        """SELECT c.*, i.title AS item_title, i.type AS item_type, i.status AS item_status
           FROM claims c JOIN items i ON c.item_id = i.id
           WHERE c.claimant_id = %s ORDER BY c.created_at DESC""",
        (g.user["id"],),
    )
    return jsonify({"claims": [_serialise(r) for r in rows]})


@bp.get("/on-my-items")
@require_auth
def claims_on_my_items():
    rows = query(
        """SELECT c.*, i.title AS item_title, u.display_name AS claimant_name
           FROM claims c
           JOIN items i ON c.item_id = i.id
           JOIN users u ON c.claimant_id = u.id
           WHERE i.user_id = %s ORDER BY c.created_at DESC""",
        (g.user["id"],),
    )
    return jsonify({"claims": [_serialise(r) for r in rows]})


@bp.put("/<int:claim_id>/approve")
@require_auth
def approve(claim_id):
    claim = query(
        """SELECT c.*, i.user_id AS item_owner_id, i.title AS item_title
           FROM claims c JOIN items i ON c.item_id = i.id
           WHERE c.id = %s""",
        (claim_id,), one=True,
    )
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    if claim["item_owner_id"] != g.user["id"]:
        return jsonify({"error": "Only the item owner can approve"}), 403
    if claim["status"] != "pending":
        return jsonify({"error": "Claim is not pending"}), 400

    execute("UPDATE claims SET status = 'approved' WHERE id = %s", (claim_id,))
    execute("UPDATE items SET status = 'resolved' WHERE id = %s", (claim["item_id"],))
    # Reject all other pending claims on the same item
    execute(
        "UPDATE claims SET status = 'rejected' WHERE item_id = %s AND id != %s AND status = 'pending'",
        (claim["item_id"], claim_id),
    )
    execute(
        "INSERT INTO notifications (user_id, type, title, body, link_url) "
        "VALUES (%s, 'claim_approved', %s, %s, %s)",
        (claim["claimant_id"], "Your claim was approved!",
         f"You can now chat with the finder of '{claim['item_title']}'",
         f"/claims/{claim_id}"),
    )
    return jsonify({"ok": True})


@bp.put("/<int:claim_id>/reject")
@require_auth
def reject(claim_id):
    claim = query(
        """SELECT c.*, i.user_id AS item_owner_id, i.title AS item_title
           FROM claims c JOIN items i ON c.item_id = i.id
           WHERE c.id = %s""",
        (claim_id,), one=True,
    )
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    if claim["item_owner_id"] != g.user["id"]:
        return jsonify({"error": "Only the item owner can reject"}), 403
    if claim["status"] != "pending":
        return jsonify({"error": "Claim is not pending"}), 400

    execute("UPDATE claims SET status = 'rejected' WHERE id = %s", (claim_id,))
    execute(
        "INSERT INTO notifications (user_id, type, title, body, link_url) "
        "VALUES (%s, 'claim_rejected', %s, %s, %s)",
        (claim["claimant_id"], "Your claim was not approved",
         f"Your claim on '{claim['item_title']}' was not approved by the finder",
         f"/claims/{claim_id}"),
    )
    return jsonify({"ok": True})


@bp.get("/<int:claim_id>")
@require_auth
def get_claim(claim_id):
    claim = query(
        """SELECT c.*, i.title AS item_title, i.user_id AS item_owner_id,
                  u.display_name AS claimant_name
           FROM claims c
           JOIN items i ON c.item_id = i.id
           JOIN users u ON c.claimant_id = u.id
           WHERE c.id = %s""",
        (claim_id,), one=True,
    )
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    if g.user["id"] not in (claim["claimant_id"], claim["item_owner_id"]) and g.user["role"] == "student":
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(_serialise(claim))
