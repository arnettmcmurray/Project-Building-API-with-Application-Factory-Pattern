from flask import Flask
from flask_cors import CORS
from app.extensions import db, ma, migrate, limiter, cache
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.customers import customers_bp
from app.blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

# === Swagger ===
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Mechanic Shop API"}
)

def create_app(config_class="config.ProductionConfig"):
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

    # === Register blueprints ===
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(customers_bp)
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/")
    def home():
        return {"message": "Mechanics API is live 🚀"}, 200

    return app
