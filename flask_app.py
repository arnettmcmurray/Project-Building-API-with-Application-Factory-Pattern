# === flask_app.py ===
from dotenv import load_dotenv
load_dotenv()  # Step 1: must be first

import os
from app import create_app
from app.extensions import db
from config import DevelopmentConfig, TestingConfig, ProductionConfig

# Step 2: detect environment
env = os.getenv("FLASK_ENV", "production").lower()
print(f"[flask_app] Environment: {env}")

# Step 3: choose correct config class
config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
config_class = config_map.get(env, ProductionConfig)

# Step 4: build app
app = create_app(config_class)

# Step 5: verify DATABASE_URL loaded correctly
print(f"[flask_app] DATABASE_URL (runtime): {os.getenv('DATABASE_URL')}")

# Step 6: ensure tables exist
with app.app_context():
    db.create_all()
    print("[DB] Tables ensured")

# Step 7: no app.run(); Gunicorn starts server on Render
