from flask import request, jsonify
from app.blueprints.service_tickets import service_tickets_bp
from app.extensions import db
from app.models import ServiceTicket, Mechanic
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema
from marshmallow import ValidationError

# create ticket
@service_tickets_bp.route("/", methods=["POST"])
def create_ticket():
    try:
        ticket = service_ticket_schema.load(request.json)   # validate + build object
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 201


# get all tickets
@service_tickets_bp.route("/", methods=["GET"])
def get_tickets():
    tickets = ServiceTicket.query.all()
    return service_tickets_schema.jsonify(tickets)

# update ticket
@service_tickets_bp.route("/<int:id>", methods=["PUT"])
def update_ticket(id):
    ticket = ServiceTicket.query.get_or_404(id)
    data = request.json
    ticket.description = data.get("description", ticket.description)
    ticket.status = data.get("status", ticket.status)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket)

# delete ticket
@service_tickets_bp.route("/<int:id>", methods=["DELETE"])
def delete_ticket(id):
    ticket = ServiceTicket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Ticket {id} deleted"})

# assign mechanic
@service_tickets_bp.route("/<int:ticket_id>/assign/<int:mech_id>", methods=["POST"])
def assign_mechanic(ticket_id, mech_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mech = Mechanic.query.get_or_404(mech_id)
    if mech not in ticket.mechanics:
        ticket.mechanics.append(mech)
        db.session.commit()
    return service_ticket_schema.jsonify(ticket)

# remove mechanic
@service_tickets_bp.route("/<int:ticket_id>/remove/<int:mech_id>", methods=["POST"])
def remove_mechanic(ticket_id, mech_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mech = Mechanic.query.get_or_404(mech_id)
    if mech in ticket.mechanics:
        ticket.mechanics.remove(mech)
        db.session.commit()
    return service_ticket_schema.jsonify(ticket)
