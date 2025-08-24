from flask import Blueprint

service_tickets_bp = Blueprint( "service_tickets", __name__, url_prefix="/service_tickets")

from . import routes
