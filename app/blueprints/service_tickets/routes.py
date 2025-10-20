from flask import request, jsonify
from app.extensions import db, limiter
from app.models import ServiceTicket, Mechanic, Inventory
from .schemas import service_ticket_schema, service_tickets_schema
from . import service_tickets_bp
from marshmallow import ValidationError
from app.utils.auth import token_required

# === Create a ticket ===
@service_tickets_bp.route("", methods=["POST"])
@token_required
def create_ticket():
    try:
        ticket = service_ticket_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.add(ticket)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 201


# === Get all tickets (simple list) ===
@service_tickets_bp.route("", methods=["GET"])
def get_all_tickets():
    tickets = ServiceTicket.query.all()
    return jsonify(service_tickets_schema.dump(tickets)), 200


# === Get single ticket ===
@service_tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    return jsonify(service_ticket_schema.dump(ticket)), 200


# === Update ticket ===
@service_tickets_bp.route("/<int:ticket_id>", methods=["PUT"])
@token_required
def update_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    data = request.get_json() or {}
    if "description" in data:
        ticket.description = data["description"]
    if "status" in data:
        ticket.status = data["status"]
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200


# === Delete ticket ===
@service_tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
@token_required
def delete_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Ticket {ticket_id} deleted"}), 200


# === Assign a mechanic ===
@service_tickets_bp.route("/<int:ticket_id>/assign/<int:mech_id>", methods=["POST"])
@token_required
def assign_mechanic(ticket_id, mech_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mech_id)

    if mechanic in ticket.mechanics:
        return jsonify({"error": f"Mechanic {mech_id} already assigned to Ticket {ticket_id}"}), 400

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200


# === Remove a mechanic ===
@service_tickets_bp.route("/<int:ticket_id>/remove/<int:mech_id>", methods=["POST"])
@token_required
def remove_mechanic(ticket_id, mech_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mech_id)

    if mechanic not in ticket.mechanics:
        return jsonify({"error": f"Mechanic {mech_id} not assigned to Ticket {ticket_id}"}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200


# === Add multiple parts ===
@service_tickets_bp.route("/<int:ticket_id>/parts", methods=["POST"])
@limiter.limit("5 per minute")
@token_required
def add_parts_to_ticket(ticket_id):
    data = request.get_json() or {}
    parts_data = data.get("parts", [])
    if not parts_data:
        return jsonify({"error": "No parts provided"}), 400

    ticket = ServiceTicket.query.get_or_404(ticket_id)
    added = []

    for item in parts_data:
        part_id = item.get("part_id")
        if not part_id:
            continue
        part = Inventory.query.get_or_404(part_id)
        if part not in ticket.parts:
            ticket.parts.append(part)
            added.append(part.name)
        else:
            added.append(f"{part.name} already linked")

    db.session.commit()
    return jsonify({"message": f"Updated Service Ticket {ticket.id} parts", "details": added}), 201
