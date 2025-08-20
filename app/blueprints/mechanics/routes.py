
from flask import request, jsonify, current_app
from functools import wraps
from datetime import datetime, timedelta, timezone

from app.blueprints.mechanics import mechanics_bp
from app.extensions import db
from app.models import Mechanic, ServiceTicket, ticket_mechanics
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema, login_schema

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError  # python-jose


# ---- token helpers (python-jose) ----
def encode_token(mechanic_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(mechanic_id),                      
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=1)).timestamp()),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


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


# ---- routes ----

# create mechanic
@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        mech = mechanic_schema.load(request.json)  # validate + build object
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # hash password
    if "password" in request.json:
        mech.set_password(request.json["password"])

    try:
        db.session.add(mech)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return mechanic_schema.jsonify(mech), 201


# get all mechanics
@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    mechs = Mechanic.query.all()
    return mechanics_schema.jsonify(mechs)


# login
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


# update mechanic (self-only)
@mechanics_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_mechanic(id):
    if request.mechanic_id != id:
        return jsonify({"error": "Forbidden: you can only update your own profile"}), 403

    mech = Mechanic.query.get_or_404(id)
    data = request.json or {}

    # allow name/specialty change; handle password reset if provided
    if "name" in data:
        mech.name = data["name"]
    if "specialty" in data:
        mech.specialty = data["specialty"]
    if "password" in data and data["password"]:
        mech.set_password(data["password"])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Update failed"}), 400

    return mechanic_schema.jsonify(mech), 200


# delete mechanic (self-only)
@mechanics_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_mechanic(id):
    if request.mechanic_id != id:
        return jsonify({"error": "Forbidden: you can only delete your own profile"}), 403

    mech = Mechanic.query.get_or_404(id)
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted"}), 200


# protected: get my tickets
@mechanics_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets():
    mid = request.mechanic_id
    tickets = (
        ServiceTicket.query.join(ticket_mechanics)
        .filter(ticket_mechanics.c.mechanic_id == mid)
        .all()
    )
    data = [{"id": t.id, "description": t.description, "status": t.status} for t in tickets]
    return jsonify(data), 200
