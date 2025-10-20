from flask import request, jsonify
from app.extensions import db
from . import inventory_bp
from app.models import Inventory
from .schemas import inventory_schema, inventories_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.utils.auth import token_required

# === Create part ===
@inventory_bp.route("", methods=["POST"])
@token_required
def create_part():
    try:
        part = inventory_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        db.session.add(part)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Part already exists"}), 409

    return jsonify(inventory_schema.dump(part)), 201


# === Get all parts ===
@inventory_bp.route("", methods=["GET"])
def get_parts():
    parts = Inventory.query.all()
    return jsonify(inventories_schema.dump(parts)), 200


# === Get single part ===
@inventory_bp.route("/<int:id>", methods=["GET"])
def get_part(id):
    part = Inventory.query.get_or_404(id)
    return jsonify(inventory_schema.dump(part)), 200


# === Update part ===
@inventory_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_part(id):
    part = Inventory.query.get_or_404(id)
    data = request.get_json() or {}

    try:
        updated = inventory_schema.load(data, instance=part, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.commit()
    return jsonify(inventory_schema.dump(updated)), 200


# === Delete part ===
@inventory_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_part(id):
    part = Inventory.query.get_or_404(id)
    try:
        db.session.delete(part)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Part is linked to a ticket and cannot be deleted"}), 400
    return jsonify({"message": f"Part {id} deleted"}), 200
