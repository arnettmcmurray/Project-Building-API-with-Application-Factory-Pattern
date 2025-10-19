import os
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

from app.extensions import db, ma, migrate, limiter, cache
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.customers import customers_bp
from app.blueprints.inventory import inventory_bp
from config import DevelopmentConfig, TestingConfig, ProductionConfig


# === load environment variables ===
load_dotenv()

SWAGGER_URL = "/api/docs"  # swagger endpoint


# === helper: choose config dynamically ===
def _pick_config():
    env = os.getenv("FLASK_ENV", "production").lower()
    return {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }.get(env, ProductionConfig)


# === create app factory ===
def create_app(config_obj=None):
    app = Flask(__name__, static_folder="static")

    # pick config
    cfg = _pick_config()
    app.config.from_object(config_obj or cfg)

    print(f"[create_app] FLASK_ENV={os.getenv('FLASK_ENV')}, using {cfg.__name__}")
    print(f"[create_app] DB URI → {app.config['SQLALCHEMY_DATABASE_URI']}")

    # === enable CORS ===
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # === swagger setup (switch base automatically for Render vs local) ===
    base_api_url = "/static/swagger.yaml"
    if os.getenv("FLASK_ENV") == "production":
        base_api_url = "https://mechanics-api.onrender.com/static/swagger.yaml"

    swagger_bp = get_swaggerui_blueprint(
        base_url=SWAGGER_URL,
        api_url=base_api_url,
        config={"app_name": "Mechanic Workshop API"},
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    # === init extensions ===
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    # === auto create tables locally ===
    with app.app_context():
        uri = (app.config.get("SQLALCHEMY_DATABASE_URI") or "").lower()
        if "sqlite" in uri:
            db.create_all()
            print("[DB] SQLite tables ensured locally")

    # === register blueprints ===
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # === base route ===
    @app.get("/")
    def root():
        return {
            "message": "Mechanic Workshop API is live",
            "docs": "/api/docs",
            "examples": {
                "mechanic_login": {"email": "alex@shop.com", "password": "password123"},
                "customer_create": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "312-555-1111",
                    "car": "Honda Civic"
                },
                "ticket_create": {
                    "description": "Brake pad replacement",
                    "customer_id": 1
                }
            },
        }, 200

    return app
