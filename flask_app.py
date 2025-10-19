from app import create_app
import os
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

# Pick config dynamically based on FLASK_ENV
env = os.getenv("FLASK_ENV", "production").lower()
config_name = f"config.{env.capitalize()}Config"

print(f"[flask_app] Environment: {env}")
app = create_app(config_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
