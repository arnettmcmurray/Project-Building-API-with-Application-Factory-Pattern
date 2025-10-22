import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "my-mechanics-secret-2025")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    RATELIMIT_STORAGE_URI = "memory://"
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mechanic_shop.db")
    RATELIMIT_DEFAULT = "10 per minute"


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///testing.db")
    TESTING = True
    RATELIMIT_DEFAULT = "10 per minute"


class ProductionConfig(Config):
    uri = os.getenv("DATABASE_URL")

    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    # === Force SSL for Render ===
    if uri and "sslmode" not in uri and "sqlite" not in uri:
        uri = f"{uri}?sslmode=require"

    SQLALCHEMY_DATABASE_URI = uri or "sqlite:///mechanic_shop.db"
    RATELIMIT_DEFAULT = "100 per minute"
    CACHE_DEFAULT_TIMEOUT = 300
