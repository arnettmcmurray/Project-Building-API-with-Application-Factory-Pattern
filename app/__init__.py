from flask import Flask
from app.extensions import db, ma, migrate, limiter, cache
# import BP
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.customers import customers_bp
from app.blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint # need to create a blueprint to plug into ur app

SWAGGER_URL = '/api/docs' #Url for exposing my swagger ui
API_URL = '/static/swagger.yaml'

#create swagger blueprint
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Mechanic Shop API'} )

def create_app(config_class="config.Config"): #application factory
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    # register blueprints
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL) #registering my swagger blueprint to make it accesible on my own
    
    return app
