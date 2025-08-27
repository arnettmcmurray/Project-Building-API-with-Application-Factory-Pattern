from flask import Blueprint

# Define the blueprint for customers
customers_bp = Blueprint(
    "customers",              # Blueprint name (used for url_for lookups)what a headache
    __name__,                 # Module where it’s defined
    url_prefix="/customers"   # route in routes.py will start with /customers
)

# register this blueprint
from . import routes
