import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 60
    SECURITY_ADMIN_EMAIL = os.environ.get("SECURITY_ADMIN_EMAIL", "admin@example.com")
    SECURITY_ADMIN_PASSWORD = os.environ.get("SECURITY_ADMIN_PASSWORD", "admin123")
    MAIL_ENABLED = os.environ.get("MAIL_ENABLED", "false").lower() == "true"
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"


def load_config(app):
    app.config.from_object(Config)
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
    print("🔍 SQLite DB path:", db_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

