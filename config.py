import os
from dotenv import load_dotenv

# Load .env file if present (local dev only)
load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key")

    # Optional: rate limit + cache
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = "10 per minute"
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL", "sqlite:///mechanic_shop.db"
    )


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL", "sqlite:///testing.db"
    )
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    RATELIMIT_DEFAULT = "100 per minute"
    CACHE_DEFAULT_TIMEOUT = 300
