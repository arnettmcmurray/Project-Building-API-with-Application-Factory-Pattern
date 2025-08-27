from flask import request, jsonify
from app.extensions import db
from . import inventory_bp
from app.models import Inventory
from .schemas import InventorySchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)


# === Create part ===
@inventory_bp.route("", methods=["POST"])
def create_part():
    try:
        part = inventory_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        db.session.add(part)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Part already exists"}), 409

    return inventory_schema.jsonify(part), 201


# === Get all parts ===
@inventory_bp.route("", methods=["GET"])
def get_parts():
    parts = Inventory.query.all()
    return inventories_schema.jsonify(parts), 200


# === Get single part ===
@inventory_bp.route("/<int:id>", methods=["GET"])
def get_part(id):
    part = Inventory.query.get_or_404(id)
    return inventory_schema.jsonify(part), 200


# === Update part ===
@inventory_bp.route("/<int:id>", methods=["PUT"])
def update_part(id):
    part = Inventory.query.get_or_404(id)
    data = request.json or {}

    try:
        updated = inventory_schema.load(data, instance=part, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.commit()
    return inventory_schema.jsonify(updated), 200


# === Delete part ===
@inventory_bp.route("/<int:id>", methods=["DELETE"])
def delete_part(id):
    part = Inventory.query.get_or_404(id)
    try:
        db.session.delete(part)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Part is linked to a ticket and cannot be deleted"}), 400
    return jsonify({"message": f"Part {id} deleted"}), 200