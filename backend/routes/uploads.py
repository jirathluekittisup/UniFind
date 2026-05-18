"""File upload endpoint — stores images under ./uploads and serves them back."""
import os
import uuid
from pathlib import Path
from flask import Blueprint, request, jsonify, send_from_directory, url_for
from utils.auth import require_auth

bp = Blueprint("uploads", __name__, url_prefix="/api/uploads")

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads")).resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic"}
MAX_BYTES = 8 * 1024 * 1024  # 8 MB


@bp.post("")
@require_auth
def upload():
    f = request.files.get("file")
    if not f or not f.filename:
        return jsonify({"error": "file is required"}), 400

    ext = Path(f.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error": f"unsupported type {ext}"}), 400

    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)
    if size > MAX_BYTES:
        return jsonify({"error": "file too large (max 8MB)"}), 413

    name = f"{uuid.uuid4().hex}{ext}"
    dest = UPLOAD_DIR / name
    f.save(dest)

    # Store a relative URL so the same DB row works from any client (mobile, web, LAN, localhost).
    relative_url = f"/api/uploads/{name}"
    return jsonify({"url": relative_url, "filename": name}), 201


@bp.get("/<path:filename>")
def serve(filename):
    return send_from_directory(UPLOAD_DIR, filename)
