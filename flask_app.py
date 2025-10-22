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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
