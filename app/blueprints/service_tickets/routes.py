from flask import request, jsonify
from app.extensions import db, limiter
from app.models import ServiceTicket, Mechanic, Inventory
from .schemas import service_ticket_schema, service_tickets_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.utils.auth import token_required
from . import service_tickets_bp


# === Create ticket ===
@service_tickets_bp.route("/create", methods=["POST"])
@token_required
def create_ticket():
    try:
        ticket = service_ticket_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "details": err.messages}), 400
    db.session.add(ticket)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 201


# === Get all tickets ===
@service_tickets_bp.route("/get_all", methods=["POST"])
@token_required
def get_all_tickets():
    tickets = ServiceTicket.query.all()
    if not tickets:
        return jsonify({"message": "No tickets found"}), 200
    return jsonify(service_tickets_schema.dump(tickets)), 200


# === Get one ticket ===
@service_tickets_bp.route("/get_one", methods=["POST"])
@token_required
def get_ticket():
    data = request.get_json() or {}
    tid = data.get("ticket_id")
    if not tid:
        return jsonify({"error": "Missing ticket_id"}), 400
    ticket = ServiceTicket.query.get_or_404(tid)
    return jsonify(service_ticket_schema.dump(ticket)), 200


# === Update ticket ===
@service_tickets_bp.route("/update", methods=["PUT"])
@token_required
def update_ticket():
    data = request.get_json() or {}
    tid = data.get("ticket_id")
    if not tid:
        return jsonify({"error": "Missing ticket_id"}), 400
    ticket = ServiceTicket.query.get_or_404(tid)
    for field in ("description", "status", "customer_id"):
        if field in data:
            setattr(ticket, field, data[field])
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200


# === Delete ticket ===
@service_tickets_bp.route("/delete", methods=["DELETE"])
@token_required
def delete_ticket():
    data = request.get_json() or {}
    tid = data.get("ticket_id")
    if not tid:
        return jsonify({"error": "Missing ticket_id"}), 400
    ticket = ServiceTicket.query.get_or_404(tid)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Ticket {tid} deleted"}), 200


# === Assign mechanic ===
@service_tickets_bp.route("/assign", methods=["POST"])
@token_required
def assign_mechanic():
    data = request.get_json() or {}
    tid = data.get("ticket_id")
    mid = data.get("mech_id")
    if not tid or not mid:
        return jsonify({"error": "Missing ticket_id or mech_id"}), 400
    ticket = ServiceTicket.query.get_or_404(tid)
    mechanic = Mechanic.query.get_or_404(mid)
    if mechanic in ticket.mechanics:
        return jsonify({"error": "Mechanic already assigned"}), 400
    ticket.mechanics.append(mechanic)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200


# === Remove mechanic ===
@service_tickets_bp.route("/remove", methods=["POST"])
@token_required
def remove_mechanic():
    data = request.get_json() or {}
    tid = data.get("ticket_id")
    mid = data.get("mech_id")
    if not tid or not mid:
        return jsonify({"error": "Missing ticket_id or mech_id"}), 400
    ticket = ServiceTicket.query.get_or_404(tid)
    mechanic = Mechanic.query.get_or_404(mid)
    if mechanic not in ticket.mechanics:
        return jsonify({"error": "Mechanic not assigned"}), 400
    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200


# === Add parts ===
@service_tickets_bp.route("/add_parts", methods=["POST"])
@limiter.limit("5 per minute")
@token_required
def add_parts():
    data = request.get_json() or {}
    tid = data.get("ticket_id")
    parts_data = data.get("parts", [])
    if not tid:
        return jsonify({"error": "Missing ticket_id"}), 400
    if not parts_data:
        return jsonify({"error": "No parts provided"}), 400

    ticket = ServiceTicket.query.get_or_404(tid)
    added = []
    for item in parts_data:
        part_id = item.get("part_id")
        part = Inventory.query.get_or_404(part_id)
        if part not in ticket.parts:
            ticket.parts.append(part)
            added.append(part.name)
        else:
            added.append(f"{part.name} already linked")

    db.session.commit()
    return jsonify({"message": f"Ticket {tid} updated", "parts": added}), 201
