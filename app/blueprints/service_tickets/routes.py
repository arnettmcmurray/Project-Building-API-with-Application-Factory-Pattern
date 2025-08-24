from flask import request, jsonify
from app.extensions import db, limiter
from app.models import ServiceTicket, Mechanic, ticket_mechanics, Inventory, ServiceTicketInventory
from .schemas import service_ticket_schema, service_tickets_schema
from . import service_tickets_bp
from marshmallow import ValidationError

from app.utils.auth import token_required


# Create a ticket
@service_tickets_bp.route("/", methods=["POST"])
@token_required
def create_ticket():
    try:
        ticket = service_ticket_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 201


# Paginated tickets
@service_tickets_bp.route("/paginated", methods=["GET"])
def get_paginated_tickets():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    tickets_query = ServiceTicket.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "tickets": service_tickets_schema.dump(tickets_query.items),
        "total": tickets_query.total,
        "page": tickets_query.page,
        "pages": tickets_query.pages,
    }), 200


# Get single ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    return service_ticket_schema.jsonify(ticket), 200


# Get all tickets
@service_tickets_bp.route("/", methods=["GET"])
def get_all_tickets():
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.jsonify(tickets), 200


# Update ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["PUT"])
@token_required
def update_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    data = request.get_json() or {}

    if "description" in data:
        ticket.description = data["description"]
    # 🔧 removed phantom 'status'

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# Delete ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
@token_required
def delete_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mech = Mechanic.query.get(request.mechanic_id)

    if mech and mech.specialty == "ADMIN":
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({"message": f"Ticket {ticket_id} deleted by admin"}), 200

    if mech not in ticket.mechanics:
        return jsonify({"error": "Forbidden: you can only delete your own tickets"}), 403

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Ticket {ticket_id} deleted"}), 200


# Assign a mechanic
@service_tickets_bp.route("/<int:ticket_id>/assign/<int:mech_id>", methods=["POST"])
def assign_mechanic(ticket_id, mech_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mech_id)

    if mechanic in ticket.mechanics:
        return jsonify({"error": f"Mechanic {mech_id} already assigned to Ticket {ticket_id}"}), 400

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# Remove a mechanic
@service_tickets_bp.route("/<int:ticket_id>/remove/<int:mech_id>", methods=["POST"])
def remove_mechanic(ticket_id, mech_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mech_id)

    if mechanic not in ticket.mechanics:
        return jsonify({"error": f"Mechanic {mech_id} not assigned to Ticket {ticket_id}"}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# Add multiple parts
@service_tickets_bp.route("/<int:ticket_id>/parts", methods=["POST"])
@limiter.limit("5 per minute")
def add_parts_to_ticket(ticket_id):
    data = request.get_json() or {}
    parts_data = data.get("parts", [])

    if not parts_data:
        return jsonify({"error": "No parts provided"}), 400

    ticket = ServiceTicket.query.get_or_404(ticket_id)
    added_parts = []

    for item in parts_data:
        part_id = item.get("part_id")
        quantity = item.get("quantity", 1)
        if not part_id:
            continue

        part = Inventory.query.get_or_404(part_id)

        link = ServiceTicketInventory(
            service_ticket_id=ticket.id,
            inventory_id=part.id,
            quantity=quantity
        )
        db.session.add(link)
        added_parts.append(f"{quantity} x {part.name}")

    db.session.commit()

    return jsonify({
        "message": f"Added parts to Service Ticket {ticket.id}",
        "details": added_parts
    }), 201
