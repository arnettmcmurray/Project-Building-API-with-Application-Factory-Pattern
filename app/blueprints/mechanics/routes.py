from flask import request, jsonify, current_app

from . import mechanics_bp
from app.extensions import db, limiter
from app.models import Mechanic, ServiceTicket, ticket_mechanics
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema, login_schema
from app.utils.auth import encode_token, token_required

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

# ---------------- Ping route (rate-limited) ----------------
@mechanics_bp.route("/ping", methods=["GET"])
@limiter.limit("5 per minute")   # limit route
def ping():
    return jsonify({"ok": True}), 200


# ---------------- Create mechanic (signup - open) ----------------
@mechanics_bp.route("", methods=["POST"])
def create_mechanic():
    try:
        mech = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        db.session.add(mech)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return mechanic_schema.jsonify(mech), 201


# ---------------- List mechanics (now protected) ----------------
@mechanics_bp.route("", methods=["GET"])
@token_required
def get_mechanics():
    mechs = Mechanic.query.all()
    return mechanics_schema.jsonify(mechs), 200


# ---------------- Login mechanic (open, rate-limited) ----------------
@mechanics_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    try:
        creds = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    mech = Mechanic.query.filter_by(email=creds["email"]).first()   # fixed lookup

    if mech and mech.check_password(creds["password"]):
        token = encode_token(mech.id, "mechanic")   # pass id + role
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid email or password"}), 401


# ---------------- Update mechanic (self-only, protected) ----------------
@mechanics_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_mechanic(id):
    if request.mechanic_id != id:
        return jsonify({"error": "Forbidden: you can only update your own profile"}), 403

    mech = Mechanic.query.get_or_404(id)
    data = request.json or {}
    if "name" in data:
        mech.name = data["name"]
    if "specialty" in data:
        mech.specialty = data["specialty"]
    if "password" in data and data["password"]:
        mech.set_password(data["password"])
    db.session.commit()
    return mechanic_schema.jsonify(mech), 200


# ---------------- Delete mechanic (self-only, protected) ----------------
@mechanics_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_mechanic(id):
    if request.mechanic_id != id:
        return jsonify({"error": "Forbidden: you can only delete your own profile"}), 403

    mech = Mechanic.query.get_or_404(id)
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted"}), 200


# ---------------- Mechanic tickets (protected) ----------------
@mechanics_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets():
    # if mechanic_id not sent in body/params, fall back to token
    mech_id = request.args.get("mechanic_id") or (request.json.get("mechanic_id") if request.is_json else None)
    if not mech_id:
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
        }
        for t in tickets
    ]), 200


# ---------------- Mechanic with most tickets (protected) ----------------
@mechanics_bp.route("/top", methods=["GET"])
@token_required
def mechanic_with_most_tickets():
    result = (
        db.session.query(
            Mechanic.id,
            Mechanic.name,
            Mechanic.email,
            func.count(ticket_mechanics.c.service_ticket_id).label("ticket_count")   # fixed column
        )
        .join(ticket_mechanics, Mechanic.id == ticket_mechanics.c.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(desc("ticket_count"))
        .first()
    )

    if not result:
        return jsonify({"message": "No mechanics found"}), 404

    retur
