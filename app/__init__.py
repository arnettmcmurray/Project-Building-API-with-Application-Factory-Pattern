from flask import Flask
from flask_cors import CORS
from app.extensions import db, ma, migrate, limiter, cache
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.customers import customers_bp
from app.blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint
import os

SWAGGER_URL = "/api/docs"

def create_app(config_class=None):
    if config_class is None:
        config_class = os.getenv("FLASK_CONFIG", "config.ProductionConfig")
    is_render = os.getenv("RENDER", False)
    base_url = "https://mechanics-api.onrender.com" if is_render else "http://127.0.0.1:5000"
    API_URL = f"{base_url}/static/swagger.yaml"

    swagger_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Mechanic Workshop API"}
    )

    app = Flask(__name__, static_folder="static")

    # === Config ===
    if isinstance(config_class, str):
        app.config.from_object(config_class)
    else:
        app.config.from_object(config_class)

    print(f"[create_app] Loaded config: {config_class}, DB = {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    # === Enable CORS for Swagger + React ===
    CORS(
        app,
        resources={r"/*": {"origins": [
            "https://mechanics-api.onrender.com",
            "https://react-mechanic-api.onrender.com",
            "http://127.0.0.1:5000",
            "http://localhost:5000",   
            "http://127.0.0.1:5173",
            "http://localhost:5173"
        ]}},
        supports_credentials=True
    )

    # === Init extensions ===
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    # === Auto-init DB on free Render (SQLite fallback) ===
    with app.app_context():
        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if isinstance(uri, str) and "sqlite" in uri.lower():
            try:
                db.create_all()
                print("[DB] create_all() executed (SQLite) — tables ready for Try it out")
            except Exception as e:
                print(f"[DB] create_all() skipped/error: {e}")

    # === Register blueprints ===
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(customers_bp)
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/")
    def home():
        return {"message": "Mechanics API is live 🚀"}, 200

    print(f"[create_app] Running on Render={is_render}, Base URL={base_url}")

    return app
