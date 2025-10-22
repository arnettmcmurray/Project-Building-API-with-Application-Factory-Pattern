import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mechanic_shop.db")


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///testing.db")
    TESTING = True


class ProductionConfig(Config):
    uri = os.getenv("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    # Enforce SSL for Render Postgres
    if uri and "sslmode" not in uri and "sqlite" not in uri:
        uri = f"{uri}?sslmode=require"

    SQLALCHEMY_DATABASE_URI = uri or "sqlite:///mechanic_shop.db"
    RATELIMIT_DEFAULT = "100 per minute"
    CACHE_DEFAULT_TIMEOUT = 300

