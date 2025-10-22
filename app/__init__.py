from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os

# === Extensions ===
from app.extensions import db, ma, migrate, limiter, cache
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.customers import customers_bp
from app.blueprints.inventory import inventory_bp
from config import DevelopmentConfig, TestingConfig, ProductionConfig

# === Load env ===
load_dotenv()

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'


def create_app(config_name=None):
    app = Flask(__name__)

    # === Config selection ===
    env = os.getenv("FLASK_ENV", "production").lower()
    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    app.config.from_object(config_map.get(env, ProductionConfig))

    # === Permanent CORS ===
    CORS(
        app,
        resources={r"/*": {"origins": [
            "http://localhost:5173",
            "https://mechanics-api.onrender.com"
        ]}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Credentials"
        ]
    )

    # === Swagger setup ===
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Mechanic Workshop API"}
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    # === Initialize extensions ===
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    # === Register blueprints ===
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # === Root ===
    @app.get("/")
    def root():
        return {
            "message": "Mechanic Workshop API is live",
            "docs": "/api/docs",
            "examples": {
                "mechanic_login": {"email": "alex@shop.com", "password": "password123"},
                "admin_login": {"email": "admin@shop.com", "password": "admin123"},
            },
        }, 200

    return app
