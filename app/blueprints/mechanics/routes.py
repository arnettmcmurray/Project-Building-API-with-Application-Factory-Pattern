from flask import request, jsonify
from . import mechanics_bp
from app.extensions import db, limiter
from app.models import Mechanic, ServiceTicket, ticket_mechanics
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema, login_schema
from app.utils.auth import encode_token, token_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

# === Ping ===
@mechanics_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"ok": True}), 200


# === Register Mechanic ===
@mechanics_bp.route("", methods=["POST"])
def create_mechanic():
    try:
        mech = mechanic_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        db.session.add(mech)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return jsonify(mechanic_schema.dump(mech)), 201


# === Login ===
@mechanics_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    try:
        creds = login_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    mech = Mechanic.query.filter_by(email=creds["email"]).first()
    if mech and mech.check_password(creds["password"]):
        token = encode_token(mech.id, "mechanic")
        return jsonify({"message": "Login successful", "token": str(token)}), 200

    return jsonify({"error": "Invalid email or password"}), 401


# === Get Mechanics ===
@mechanics_bp.route("", methods=["GET"])
@token_required
def get_mechanics():
    mechs = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(mechs)), 200


# === Update ===
@mechanics_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_mechanic(id):
    if request.mechanic_id != id:
        return jsonify({"error": "Forbidden"}), 403

    mech = Mechanic.query.get_or_404(id)
    data = request.get_json() or {}
    if "name" in data:
        mech.name = data["name"]
    if "specialty" in data:
        mech.specialty = data["specialty"]
    if "password" in data and data["password"]:
        mech.set_password(data["password"])
    db.session.commit()
    return jsonify(mechanic_schema.dump(mech)), 200


# === Delete ===
@mechanics_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_mechanic(id):
    if request.mechanic_id != id:
        return jsonify({"error": "Forbidden"}), 403
    mech = Mechanic.query.get_or_404(id)
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted"}), 200


# === My Tickets ===
@mechanics_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets():
    mech_id = request.mechanic_id
    tickets = (
        ServiceTicket.query.join(ticket_mechanics)
        .filter(ticket_mechanics.c.mechanic_id == mech_id)
        .all()
    )
    return jsonify([
        {
            "id": t.id,
            "description": t.description,
            "status": t.status,
            "date": t.date.isoformat(),
            "customer_id": t.customer_id
        } for t in tickets
    ]), 200


# === Top Mechanic ===
@mechanics_bp.route("/top", methods=["GET"])
@token_required
def top_mechanic():
    result = (
        db.session.query(
            Mechanic.id,
            Mechanic.name,
            func.count(ticket_mechanics.c.service_ticket_id).label("count")
        )
        .join(ticket_mechanics)
        .group_by(Mechanic.id)
        .order_by(desc("count"))
        .first()
    )
    if not result:
        return jsonify({"message": "No data"}), 404
    return jsonify({"id": result.id, "name": result.name, "ticket_count": result.count}), 200
