# === flask_app.py ===
from dotenv import load_dotenv
load_dotenv()  # Must load before anything else

import os
from app import create_app
from app.extensions import db
from config import DevelopmentConfig, TestingConfig, ProductionConfig

# === Step 1: detect environment ===
env = os.getenv("FLASK_ENV", "production").lower()
print(f"[flask_app] Environment: {env}")

# === Step 2: choose correct config class ===
config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
config_class = config_map.get(env, ProductionConfig)
print(f"[flask_app] Using config class: {config_class.__name__}")

# === Step 3: build app ===
app = create_app(config_class)

# === Step 4: verify DATABASE_URL loaded correctly ===
db_url = os.getenv("DATABASE_URL")
print(f"[flask_app] DATABASE_URL (runtime): {db_url}")

# === Step 5: ensure tables exist (safe for local + Render) ===
with app.app_context():
    db.create_all()
    print("[DB] Tables ensured")

# === Step 6: Gunicorn handles serving on Render ===
# Local dev works with: flask run
