"""UniFind Flask API entrypoint."""
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from utils.db import init_mysql, init_mongo
from routes.auth import bp as auth_bp
from routes.items import bp as items_bp
from routes.claims import bp as claims_bp
from routes.messages import bp as messages_bp
from routes.notifications import bp as notifications_bp
from routes.admin import bp as admin_bp
from routes.uploads import bp as uploads_bp


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialise connections (non-fatal if unreachable in dev)
    try:
        init_mysql()
    except Exception as e:
        print(f"[startup] MySQL init failed: {e}")
    try:
        init_mongo()
    except Exception as e:
        print(f"[startup] MongoDB init failed: {e}")

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(claims_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(uploads_bp)

    @app.get("/")
    def root():
        return jsonify({
            "app": "UniFind API",
            "version": "1.0.0",
            "status": "ok",
            "endpoints": [
                "/api/auth/register", "/api/auth/login", "/api/auth/me",
                "/api/items", "/api/items/<id>", "/api/items/mine",
                "/api/claims", "/api/claims/mine", "/api/claims/on-my-items",
                "/api/messages/claim/<id>", "/api/notifications",
                "/api/admin/stats", "/api/admin/users",
            ],
        })

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)
