from flask import request, jsonify, current_app
from functools import wraps
from datetime import datetime, timedelta, timezone

from . import mechanics_bp
from app.extensions import db
from app.models import Mechanic, ServiceTicket, ticket_mechanics
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema, login_schema

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError
from sqlalchemy import func, desc
from .schemas import mechanic_schema, mechanics_schema

@mechanics_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"ok": True}), 200

# ---------------- JWT helper ----------------
def encode_token(mechanic_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(mechanic_id),                     # subject must be a string
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=7)).timestamp()),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


# --------------- token_required ---------------
def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth.split(" ", 1)[1].strip()
        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
            )
            request.mechanic_id = int(payload.get("sub"))
        except JWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        return fn(*args, **kwargs)
    return wrapper


# ---------------- Mechanics routes ----------------
@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        mech = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400


    if "password" in request.json:
        mech.set_password(request.json["password"])

    try:
        db.session.add(mech)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return mechanic_schema.jsonify(mech), 201


@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    mechs = Mechanic.query.all()
    return mechanics_schema.jsonify(mechs), 200


@mechanics_bp.route("/login", methods=["POST"])
def login():
    try:
        creds = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    mech = Mechanic.query.filter_by(email=creds["email"]).first()
    if mech and mech.check_password(creds["password"]):
        token = encode_token(mech.id)
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid email or password"}), 401


# ---- protected: update/delete self ----
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


@mechanics_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_mechanic(id):
    if request.mechanic_id != id:
        return jsonify({"error": "Forbidden: you can only delete your own profile"}), 403

    mech = Mechanic.query.get_or_404(id)
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted"}), 200


@mechanics_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets():
    # admin passes 
    mech_id = request.args.get("mechanic_id") or (request.json.get("mechanic_id") if request.is_json else None)

    if not mech_id:
        mech_id = request.mechanic_id  

    tickets = (
        ServiceTicket.query.join(ticket_mechanics)
        .filter(ticket_mechanics.c.mechanic_id == mech_id)
        .all()
    )
    return jsonify([
        {"id": t.id, "description": t.description, "status": t.status}
        for t in tickets
    ]), 200

# === HOMEWORK ADDITION: Mechanic(s) with most tickets ===
@mechanics_bp.route("/top", methods=["GET"])
@token_required
def mechanic_with_most_tickets():
    result = (
        db.session.query(
            Mechanic.id,
            Mechanic.name,
            Mechanic.email,
            func.count(ticket_mechanics.c.ticket_id).label("ticket_count")
        )
        .join(ticket_mechanics, Mechanic.id == ticket_mechanics.c.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(desc("ticket_count"))
        .first()
    )

    if not result:
        return jsonify({"message": "No mechanics found"}), 404

    return jsonify({
        "id": result.id,
        "name": result.name,
        "email": result.email,
        "ticket_count": int(result.ticket_count)
    }), 200

@mechanics_bp.route("/ticket-count", methods=["GET"])
@token_required
def mechanics_by_ticket_count():
    rows = (
        db.session.query(
            Mechanic.id,
            Mechanic.name,
            Mechanic.email,
            func.count(ticket_mechanics.c.ticket_id).label("ticket_count")
        )
        .join(ticket_mechanics, Mechanic.id == ticket_mechanics.c.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(desc("ticket_count"))
        .all()
    )

    return jsonify([
        {
            "id": r.id,
            "name": r.name,
            "email": r.email,
            "ticket_count": int(r.ticket_count)
        }
        for r in rows
    ]), 200
