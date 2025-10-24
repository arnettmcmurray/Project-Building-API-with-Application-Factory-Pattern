from flask import request, jsonify
from app.extensions import db, limiter
from app.models import Mechanic, ServiceTicket, ticket_mechanics
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema, login_schema
from app.utils.auth import encode_token, token_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc
from . import mechanics_bp


# === Register mechanic ===
@mechanics_bp.route("/create", methods=["POST"])
def create_mechanic():
    data = request.get_json() or {}
    try:
        mech = mechanic_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "details": err.messages}), 400

    try:
        db.session.add(mech)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "IntegrityError", "message": "Email already exists"}), 409

    return jsonify({"message": "Mechanic created successfully", "mechanic": mechanic_schema.dump(mech)}), 201


# === Login ===
@mechanics_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    try:
        creds = login_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "details": err.messages}), 400

    mech = Mechanic.query.filter_by(email=creds["email"]).first()
    if mech and mech.check_password(creds["password"]):
        token = encode_token(mech.id, "mechanic")
        return jsonify({
        "message": "Login successful",
        "token": str(token),
        "id": mech.id,
        "name": mech.name,
        "email": mech.email,
        "specialty": mech.specialty
    }), 200

    return jsonify({"error": "InvalidCredentials", "message": "Invalid email or password"}), 401


# === Get all mechanics ===
@mechanics_bp.route("/get_all", methods=["POST"])
@token_required
def get_all_mechanics():
    mechs = Mechanic.query.all()
    if not mechs:
        return jsonify({"message": "No mechanics found"}), 200
    return jsonify(mechanics_schema.dump(mechs)), 200


# === Get one mechanic ===
@mechanics_bp.route("/get_one", methods=["POST"])
@token_required
def get_one_mechanic():
    data = request.get_json() or {}
    mech_id = data.get("id")
    if not mech_id:
        return jsonify({"error": "Missing id"}), 400
    mech = Mechanic.query.get_or_404(mech_id)
    return jsonify(mechanic_schema.dump(mech)), 200


# === Update mechanic ===
@mechanics_bp.route("/update", methods=["PUT"])
@token_required
def update_mechanic():
    data = request.get_json() or {}
    mech_id = data.get("id")
    if not mech_id:
        return jsonify({"error": "Missing id"}), 400

    mech = Mechanic.query.get_or_404(mech_id)
    for field in ("name", "specialty", "password"):
        if field in data and data[field]:
            if field == "password":
                mech.set_password(data["password"])
            else:
                setattr(mech, field, data[field])
    db.session.commit()
    return jsonify({"message": "Mechanic updated", "mechanic": mechanic_schema.dump(mech)}), 200


# === Delete mechanic ===
@mechanics_bp.route("/delete", methods=["DELETE"])
@token_required
def delete_mechanic():
    data = request.get_json() or {}
    mech_id = data.get("id")
    if not mech_id:
        return jsonify({"error": "Missing id"}), 400
    mech = Mechanic.query.get_or_404(mech_id)
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mech_id} deleted"}), 200


# === My tickets ===
@mechanics_bp.route("/my_tickets", methods=["POST"])
@token_required
def my_tickets():
    mech_id = request.mechanic_id
    tickets = (
        ServiceTicket.query.join(ticket_mechanics)
        .filter(ticket_mechanics.c.mechanic_id == mech_id)
        .all()
    )
    if not tickets:
        return jsonify({"message": "No tickets to show"}), 200
    result = [{
        "id": t.id,
        "description": t.description,
        "status": t.status,
        "date": t.date.isoformat(),
        "customer_id": t.customer_id
    } for t in tickets]
    return jsonify(result), 200


# === Top mechanic ===
@mechanics_bp.route("/top", methods=["POST"])
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
