from datetime import timedelta

import cloudinary
from flask import Flask

from app.config import Config
from app.extensions import bcrypt, cors, db, jwt


def create_app(config_class: type = Config) -> Flask:
    """Application factory: builds and configures the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        seconds=app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    )

    # --- Extensions -------------------------------------------------
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    cloudinary.config(
        cloud_name=app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=app.config.get("CLOUDINARY_API_KEY"),
        api_secret=app.config.get("CLOUDINARY_API_SECRET"),
        secure=True,
    )

    # --- Models (imported so db.create_all() sees them) -------------
    from app.models import MatchResult, Resume, User  # noqa: F401

    # --- Blueprints ---------------------------------------------------
    from app.routes.auth import auth_bp
    from app.routes.match import match_bp
    from app.routes.resume import resume_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(resume_bp, url_prefix="/api/resume")
    app.register_blueprint(match_bp, url_prefix="/api/match")

    with app.app_context():
        db.create_all()

    @app.get("/api/health")
    def health():
        return {"status": "ok"}, 200

    @app.errorhandler(413)
    def file_too_large(_e):
        return {"message": "File exceeds the 10 MB upload limit"}, 413

    return app
