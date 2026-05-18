"""Admin routes — dashboard stats, user management, moderation."""
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Blueprint, request, jsonify, g
from utils.db import query, execute
from utils.auth import require_admin

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@bp.get("/stats")
@require_admin
def stats():
    total_items  = query("SELECT COUNT(*) c FROM items", one=True)["c"]
    total_lost   = query("SELECT COUNT(*) c FROM items WHERE type = 'lost'", one=True)["c"]
    total_found  = query("SELECT COUNT(*) c FROM items WHERE type = 'found'", one=True)["c"]
    resolved     = query("SELECT COUNT(*) c FROM items WHERE status = 'resolved'", one=True)["c"]
    total_users  = query("SELECT COUNT(*) c FROM users WHERE is_active = TRUE", one=True)["c"]
    total_claims = query("SELECT COUNT(*) c FROM claims", one=True)["c"]
    approved_claims = query("SELECT COUNT(*) c FROM claims WHERE status = 'approved'", one=True)["c"]

    recovery_rate = round((resolved / total_items) * 100, 1) if total_items else 0.0
    claim_success = round((approved_claims / total_claims) * 100, 1) if total_claims else 0.0

    # Items by category
    by_category = query("""SELECT category, COUNT(*) AS c FROM items
                           GROUP BY category ORDER BY c DESC""")

    # Reports over the last 30 days
    by_day = query("""SELECT DATE(created_at) AS day, type, COUNT(*) AS c
                      FROM items WHERE created_at >= %s
                      GROUP BY day, type ORDER BY day""",
                   (datetime.utcnow() - timedelta(days=30),))

    return jsonify({
        "total_items": total_items,
        "total_lost": total_lost,
        "total_found": total_found,
        "resolved": resolved,
        "recovery_rate": recovery_rate,
        "total_users": total_users,
        "total_claims": total_claims,
        "approved_claims": approved_claims,
        "claim_success_rate": claim_success,
        "by_category": by_category,
        "by_day": [{"day": str(r["day"]), "type": r["type"], "count": r["c"]} for r in by_day],
    })


@bp.get("/chart/items-by-category")
@require_admin
def chart_items_by_category():
    """Return a Plotly chart as HTML for embedding in the admin dashboard."""
    rows = query("SELECT category, COUNT(*) AS count FROM items GROUP BY category")
    df = pd.DataFrame(rows)
    if df.empty:
        return jsonify({"html": "<p>No data yet.</p>"})
    fig = px.bar(df, x="category", y="count", color="category",
                 title="Items by Category", template="simple_white")
    fig.update_layout(showlegend=False, margin=dict(l=40, r=20, t=60, b=40))
    html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
    return jsonify({"html": html})


@bp.get("/chart/items-over-time")
@require_admin
def chart_items_over_time():
    """Daily lost/found counts for the last 30 days."""
    rows = query(
        """SELECT DATE(created_at) AS day, type, COUNT(*) AS count
           FROM items
           WHERE created_at >= %s
           GROUP BY day, type
           ORDER BY day""",
        (datetime.utcnow() - timedelta(days=30),),
    )
    if not rows:
        return jsonify({"html": "<p style='color:#64748b;padding:20px'>No items reported in the last 30 days.</p>"})

    df = pd.DataFrame(rows)
    df["day"] = pd.to_datetime(df["day"])
    fig = px.line(
        df, x="day", y="count", color="type",
        markers=True, template="simple_white",
        color_discrete_map={"lost": "#dc2626", "found": "#16a34a"},
    )
    fig.update_layout(
        margin=dict(l=40, r=20, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title=None, yaxis_title="Reports",
    )
    html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
    return jsonify({"html": html})


@bp.get("/users")
@require_admin
def list_users():
    q = request.args.get("q", "").strip()
    sql = "SELECT id, email, display_name, faculty, role, is_active, created_at FROM users"
    params = []
    if q:
        sql += " WHERE email LIKE %s OR display_name LIKE %s"
        params = [f"%{q}%", f"%{q}%"]
    sql += " ORDER BY created_at DESC LIMIT 100"
    users = query(sql, tuple(params))
    for u in users:
        if u.get("created_at"):
            u["created_at"] = u["created_at"].isoformat()
    return jsonify({"users": users})


@bp.put("/users/<int:user_id>/suspend")
@require_admin
def suspend_user(user_id):
    execute("UPDATE users SET is_active = FALSE WHERE id = %s", (user_id,))
    return jsonify({"ok": True})


@bp.put("/users/<int:user_id>/activate")
@require_admin
def activate_user(user_id):
    execute("UPDATE users SET is_active = TRUE WHERE id = %s", (user_id,))
    return jsonify({"ok": True})


@bp.delete("/items/<int:item_id>")
@require_admin
def remove_item(item_id):
    execute("UPDATE items SET status = 'removed' WHERE id = %s", (item_id,))
    return jsonify({"ok": True})


@bp.get("/claims")
@require_admin
def list_claims():
    status = request.args.get("status")
    sql = (
        "SELECT c.*, i.title AS item_title, i.type AS item_type, "
        "       iu.display_name AS item_owner_name, "
        "       cu.display_name AS claimant_name "
        "FROM claims c "
        "JOIN items i ON c.item_id = i.id "
        "JOIN users iu ON i.user_id = iu.id "
        "JOIN users cu ON c.claimant_id = cu.id"
    )
    params = []
    if status in ("pending", "approved", "rejected", "resolved"):
        sql += " WHERE c.status = %s"; params.append(status)
    sql += " ORDER BY c.created_at DESC LIMIT 200"
    rows = query(sql, tuple(params))
    for r in rows:
        for k in ("created_at", "updated_at"):
            if r.get(k):
                r[k] = r[k].isoformat() if hasattr(r[k], "isoformat") else str(r[k])
    return jsonify({"claims": rows})


@bp.get("/flagged-messages")
@require_admin
def flagged_messages():
    rows = query(
        """SELECT m.*, u.display_name AS sender_name
           FROM messages m JOIN users u ON m.sender_id = u.id
           WHERE m.is_flagged = TRUE ORDER BY m.created_at DESC LIMIT 100"""
    )
    for r in rows:
        if r.get("created_at"):
            r["created_at"] = r["created_at"].isoformat()
    return jsonify({"messages": rows})
