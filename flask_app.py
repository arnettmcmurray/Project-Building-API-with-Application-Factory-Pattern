import os
from dotenv import load_dotenv
from app import create_app
from config import DevelopmentConfig, TestingConfig, ProductionConfig

load_dotenv()

env = os.getenv("FLASK_ENV", "production").lower()
print(f"[flask_app] Environment: {env}")

config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
config_class = config_map.get(env, ProductionConfig)

app = create_app(config_class)

# === Ensure tables exist (safe for local + Render) ===
with app.app_context():
    from app.extensions import db
    db.create_all()
    print("[DB] Tables ensured")

# === No app.run(); Gunicorn handles this in Render ===
# Local dev still works fine with: flask run
