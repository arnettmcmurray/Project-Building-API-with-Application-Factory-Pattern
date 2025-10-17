from app import create_app
import os

# Auto-detect config
env = os.getenv("FLASK_ENV", "production")

if env == "development":
    app = create_app("config.DevelopmentConfig")
else:
    app = create_app("config.ProductionConfig")
