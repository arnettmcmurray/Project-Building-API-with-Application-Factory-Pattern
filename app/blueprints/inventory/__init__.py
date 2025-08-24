from flask import Blueprint

inventory_bp = Blueprint(
    "inventory",
    __name__,
    url_prefix="/parts"
)

from . import routes
