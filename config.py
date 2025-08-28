class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic_shop.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "supersecretkey123"

    # Optional: rate limit + cache
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = "10 per minute"
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "testsecretkey"

    TESTING = True
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = "10 per minute"
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///production.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "prodsecretkey"

    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = "100 per minute"
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
