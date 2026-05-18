"""Auth routes — register, login (email/password + Firebase SSO), profile."""
from flask import Blueprint, request, jsonify, g
from config import Config
from utils.db import query, execute
from utils.auth import (
    hash_password, check_password, create_jwt,
    verify_firebase_token, require_auth,
)

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/register")
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    display_name = (data.get("display_name") or "").strip()
    faculty = (data.get("faculty") or "").strip()

    if not email or not password or not display_name:
        return jsonify({"error": "email, password, display_name are required"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if not email.endswith("@" + Config.ALLOWED_EMAIL_DOMAIN):
        return jsonify({"error": f"Email must be @{Config.ALLOWED_EMAIL_DOMAIN}"}), 400

    if query("SELECT id FROM users WHERE email = %s", (email,), one=True):
        return jsonify({"error": "Email already registered"}), 409

    uid = execute(
        "INSERT INTO users (email, password_hash, display_name, faculty) VALUES (%s, %s, %s, %s)",
        (email, hash_password(password), display_name, faculty),
        return_id=True,
    )

    user = query("SELECT id, email, display_name, faculty, role FROM users WHERE id = %s",
                 (uid,), one=True)
    token = create_jwt(user)
    return jsonify({"token": token, "user": user}), 201


@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = query("SELECT * FROM users WHERE email = %s AND is_active = TRUE",
                 (email,), one=True)
    if not user or not user.get("password_hash") or not check_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_jwt(user)
    safe = {k: user[k] for k in ("id", "email", "display_name", "faculty", "role", "photo_url")}
    return jsonify({"token": token, "user": safe})


@bp.post("/firebase-login")
def firebase_login():
    """Exchange a Firebase ID token for a backend JWT."""
    data = request.get_json() or {}
    id_token = data.get("id_token")
    if not id_token:
        return jsonify({"error": "id_token is required"}), 400

    try:
        decoded = verify_firebase_token(id_token)
    except Exception as e:
        return jsonify({"error": f"Invalid Firebase token: {e}"}), 401

    email = (decoded.get("email") or "").lower()
    firebase_uid = decoded.get("uid")
    display_name = decoded.get("name") or email.split("@")[0]

    if not email.endswith("@" + Config.ALLOWED_EMAIL_DOMAIN):
        return jsonify({"error": f"Email must be @{Config.ALLOWED_EMAIL_DOMAIN}"}), 403

    user = query("SELECT * FROM users WHERE email = %s", (email,), one=True)
    if not user:
        uid = execute(
            "INSERT INTO users (firebase_uid, email, display_name) VALUES (%s, %s, %s)",
            (firebase_uid, email, display_name), return_id=True,
        )
        user = query("SELECT * FROM users WHERE id = %s", (uid,), one=True)
    elif not user.get("firebase_uid"):
        execute("UPDATE users SET firebase_uid = %s WHERE id = %s", (firebase_uid, user["id"]))

    token = create_jwt(user)
    safe = {k: user[k] for k in ("id", "email", "display_name", "faculty", "role", "photo_url")}
    return jsonify({"token": token, "user": safe})


@bp.get("/me")
@require_auth
def me():
    user = g.user
    return jsonify({
        "id": user["id"],
        "email": user["email"],
        "display_name": user["display_name"],
        "faculty": user["faculty"],
        "role": user["role"],
        "photo_url": user.get("photo_url"),
    })


@bp.put("/me")
@require_auth
def update_me():
    data = request.get_json() or {}
    display_name = data.get("display_name")
    faculty = data.get("faculty")
    photo_url = data.get("photo_url")

    updates, params = [], []
    if display_name:
        updates.append("display_name = %s"); params.append(display_name)
    if faculty is not None:
        updates.append("faculty = %s"); params.append(faculty)
    if photo_url is not None:
        updates.append("photo_url = %s"); params.append(photo_url)

    if not updates:
        return jsonify({"error": "No fields to update"}), 400

    params.append(g.user["id"])
    execute(f"UPDATE users SET {', '.join(updates)} WHERE id = %s", tuple(params))
    return jsonify({"ok": True})
