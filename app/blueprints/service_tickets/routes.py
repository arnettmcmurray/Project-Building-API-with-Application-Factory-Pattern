from flask import request, jsonify
from app.blueprints.service_tickets import service_tickets_bp
from app.extensions import db
from app.models import ServiceTicket, Mechanic, ticket_mechanics
from app.blueprints.service_tickets.schemas import ticket_schema, tickets_schema

# reuse the decorator 
from app.blueprints.mechanics.routes import token_required


# Create a ticket
@service_tickets_bp.route("/", methods=["POST"])
@token_required
def create_ticket():
    data = request.get_json() or {}
    try:
        ticket = ticket_schema.load(data)
    except Exception as err:
        return jsonify({"errors": getattr(err, "messages", str(err))}), 400

    db.session.add(ticket)
    db.session.commit()
    return ticket_schema.jsonify(ticket), 201


# List tickets
@service_tickets_bp.route("/", methods=["GET"])
@token_required
def list_tickets():
    tickets = ServiceTicket.query.all()
    return tickets_schema.jsonify(tickets), 200


# Get single ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["GET"])
@token_required
def get_ticket(ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    return ticket_schema.jsonify(t), 200


# Update ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["PUT"])
@token_required
def update_ticket(ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    data = request.get_json() or {}
    if "description" in data:
        t.description = data["description"]
    if "status" in data:
        t.status = data["status"]
    db.session.commit()
    return ticket_schema.jsonify(t), 200


# Delete ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
@token_required
def delete_ticket(ticket_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": f"ticket {ticket_id} deleted"}), 200


# Assign a mechanic to a ticket (many-to-many)
@service_tickets_bp.route("/<int:ticket_id>/assign/<int:mech_id>", methods=["POST"])
@token_required
def assign_mechanic(ticket_id, mech_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    m = Mechanic.query.get_or_404(mech_id)
    if m not in t.mechanics:
        t.mechanics.append(m)
        db.session.commit()
    return ticket_schema.jsonify(t), 200


# Remove a mechanic from a ticket
@service_tickets_bp.route("/<int:ticket_id>/remove/<int:mech_id>", methods=["POST"])
@token_required
def remove_mechanic(ticket_id, mech_id):
    t = ServiceTicket.query.get_or_404(ticket_id)
    m = Mechanic.query.get_or_404(mech_id)
    if m in t.mechanics:
        t.mechanics.remove(m)
        db.session.commit()
    return ticket_schema.jsonify(t), 200
