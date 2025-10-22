import os
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

# === Extensions ===
from app.extensions import db, ma, migrate, limiter, cache
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.customers import customers_bp
from app.blueprints.inventory import inventory_bp
from config import DevelopmentConfig, TestingConfig, ProductionConfig

# === Load env ===
load_dotenv()
SWAGGER_URL = "/api/docs"


def _pick_config():
    env = os.getenv("FLASK_ENV", "production").lower()
    return {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }.get(env, ProductionConfig)


def create_app(config_obj=None):
    app = Flask(__name__, static_folder="static")
    cfg = _pick_config()
    app.config.from_object(config_obj or cfg)

    # === SQLAlchemy engine ===
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    # === CORS (local + Render frontend) ===
    CORS(app, origins=[
        "http://localhost:5173",
        "https://mechanics-api.onrender.com"
    ])

    # === Swagger ===
    env = os.getenv("FLASK_ENV", "production").lower()
    api_url = (
        "http://127.0.0.1:5000/static/swagger.yaml"
        if env == "development"
        else "https://mechanics-api.onrender.com/static/swagger.yaml"
    )

    swagger_bp = get_swaggerui_blueprint(
        base_url=SWAGGER_URL,
        api_url=api_url,
        config={
            "app_name": "Mechanic Workshop API",
            "validatorUrl": None,
            "persistAuthorization": True,
        },
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    # === Init extensions ===
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    # === Auto-seed only if local SQLite ===
    with app.app_context():
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "").lower()
        if "sqlite" in uri:
            db.create_all()
            print("[DB] SQLite tables ensured")

            from app.models import Mechanic
            if not Mechanic.query.first():
                from app.models import Customer, Inventory, ServiceTicket

                admin = Mechanic(name="Admin User", email="admin@shop.com", specialty="Admin")
                admin.set_password("admin123")
                alex = Mechanic(name="Alex Rivera", email="alex@shop.com", specialty="Brakes")
                alex.set_password("password123")
                db.session.add_all([admin, alex])
                db.session.commit()

                john = Customer(name="John Doe", email="john@example.com", phone="312-555-1111", car="Honda Civic")
                jane = Customer(name="Jane Smith", email="jane@example.com", phone="312-555-2222", car="Toyota Corolla")
                db.session.add_all([john, jane])
                db.session.commit()

                brake = Inventory(name="Brake Pads", price=49.99, quantity=20)
                oil = Inventory(name="Oil Filter", price=9.99, quantity=50)
                db.session.add_all([brake, oil])
                db.session.commit()

                ticket1 = ServiceTicket(description="Brake pad replacement", status="Open", customer_id=john.id)
                ticket2 = ServiceTicket(description="Oil change", status="Closed", customer_id=jane.id)
                db.session.add_all([ticket1, ticket2])
                db.session.commit()

                print("✅ Auto-seed complete — default data ready.")

    # === Blueprints ===
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

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
