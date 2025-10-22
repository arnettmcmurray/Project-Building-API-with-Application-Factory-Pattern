from flask import request, jsonify
from app.extensions import db
from app.models import Inventory
from app.utils.auth import token_required
from .schemas import inventory_schema, inventories_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import inventory_bp


# === Create part ===
@inventory_bp.route("/create", methods=["POST"])
@token_required
def create_part():
    try:
        part = inventory_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "details": err.messages}), 400
    try:
        db.session.add(part)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "IntegrityError", "message": "Part already exists"}), 409
    return jsonify(inventory_schema.dump(part)), 201


# === Get all parts ===
@inventory_bp.route("/get_all", methods=["POST"])
def get_parts():
    parts = Inventory.query.all()
    if not parts:
        return jsonify({"message": "No parts found"}), 200
    return jsonify(inventories_schema.dump(parts)), 200


# === Get one part ===
@inventory_bp.route("/get_one", methods=["POST"])
def get_part():
    data = request.get_json() or {}
    pid = data.get("id")
    if not pid:
        return jsonify({"error": "Missing id"}), 400
    part = Inventory.query.get_or_404(pid)
    return jsonify(inventory_schema.dump(part)), 200


# === Update part ===
@inventory_bp.route("/update", methods=["PUT"])
@token_required
def update_part():
    data = request.get_json() or {}
    pid = data.get("id")
    if not pid:
        return jsonify({"error": "Missing id"}), 400
    part = Inventory.query.get_or_404(pid)
    for field in ("name", "price", "quantity"):
        if field in data:
            setattr(part, field, data[field])
    db.session.commit()
    return jsonify(inventory_schema.dump(part)), 200


# === Delete part ===
@inventory_bp.route("/delete", methods=["DELETE"])
@token_required
def delete_part():
    data = request.get_json() or {}
    pid = data.get("id")
    if not pid:
        return jsonify({"error": "Missing id"}), 400
    part = Inventory.query.get_or_404(pid)
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part {pid} deleted"}), 200
