from flask import Blueprint

service_tickets_bp = Blueprint("service_tickets", __name__, url_prefix="/tickets")

from . import routes  # noqa: F401,E402

