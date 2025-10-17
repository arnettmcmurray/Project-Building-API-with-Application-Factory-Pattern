from app import create_app
import os
from dotenv import load_dotenv

# === Load .env if present ===
load_dotenv()

# === Config switch ===
env = os.getenv("FLASK_ENV", "production").lower()

if env == "development":
    print("[flask_app] Using DevelopmentConfig")
    app = create_app("config.DevelopmentConfig")
else:
    print("[flask_app] Using ProductionConfig")
    app = create_app("config.ProductionConfig")
