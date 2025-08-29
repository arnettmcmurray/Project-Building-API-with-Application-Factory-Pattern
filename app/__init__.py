from flask import Flask
from app.extensions import db, ma, migrate, limiter, cache
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.customers import customers_bp
from app.blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Mechanic Shop API"}
)

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__, static_folder="static")

    # load config dynamically
    app.config.from_object(config_class)
 # Debug print to confirm which DB is being used
    print(f"[create_app] Loaded config: {config_class}, DB = {app.config['SQLALCHEMY_DATABASE_URI']}")

    # init extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    # register blueprints
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(customers_bp)
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/")
    def home():
        return {"message": "Mechanics API is live 🚀"}, 200

    return app
