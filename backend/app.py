from flask import Flask, send_from_directory, jsonify
from .config import load_config
from .extensions import db, login_manager, cache
from .models import ensure_default_admin


def create_app() -> Flask:
    app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
    load_config(app)

    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)

    with app.app_context():
        db.create_all()
        ensure_default_admin()

    # Blueprints
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.user import user_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(user_bp, url_prefix="/api/user")

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/assets/<path:filename>")
    def assets(filename: str):
        return send_from_directory(app.static_folder + "/assets", filename)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)