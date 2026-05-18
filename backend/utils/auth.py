"""JWT authentication + Firebase token verification."""
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
from config import Config
from utils.db import query

try:
    import firebase_admin
    from firebase_admin import auth as fb_auth, credentials
    _fb_initialised = False

    def init_firebase():
        global _fb_initialised
        if _fb_initialised:
            return
        try:
            cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
            firebase_admin.initialize_app(cred, {"storageBucket": Config.FIREBASE_STORAGE_BUCKET})
            _fb_initialised = True
            print("[AUTH] Firebase Admin initialised")
        except Exception as e:
            print(f"[AUTH] Firebase not initialised: {e}")

    def verify_firebase_token(id_token: str):
        init_firebase()
        return fb_auth.verify_id_token(id_token)

except ImportError:
    def verify_firebase_token(id_token: str):
        raise RuntimeError("firebase_admin not installed")


# ─── Password helpers ─────────────────────────────────────────────────────────
def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt(rounds=12)).decode()


def check_password(pw: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode(), hashed.encode())
    except Exception:
        return False


# ─── JWT helpers ──────────────────────────────────────────────────────────────
def create_jwt(user: dict) -> str:
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "role": user.get("role", "student"),
        "exp": datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRY_HOURS),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])


# ─── Flask decorators ─────────────────────────────────────────────────────────
def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = header.split(" ", 1)[1].strip()
        try:
            payload = decode_jwt(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        user = query("SELECT * FROM users WHERE id = %s AND is_active = TRUE",
                     (payload["user_id"],), one=True)
        if not user:
            return jsonify({"error": "User not found or inactive"}), 401
        g.user = user
        return fn(*args, **kwargs)
    return wrapper


def require_admin(fn):
    @wraps(fn)
    @require_auth
    def wrapper(*args, **kwargs):
        if g.user["role"] not in ("admin", "super_admin"):
            return jsonify({"error": "Admin privileges required"}), 403
        return fn(*args, **kwargs)
    return wrapper
