class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic_shop.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: rate limit + cache
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = "50 per minute"
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60
