from flask import request, jsonify
from app.extensions import db
from . import inventory_bp
from app.models import Inventory
from .schemas import InventorySchema
from marshmallow import ValidationError

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

# === Inventory CRUD ===

@inventory_bp.route("/", methods=["POST"])
def create_part():
    try:
        part = inventory_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.add(part)
    db.session.commit()
    return inventory_schema.jsonify(part), 201


@inventory_bp.route("/", methods=["GET"])
def get_parts():
    parts = Inventory.query.all()
    return inventories_schema.jsonify(parts)


@inventory_bp.route("/<int:id>", methods=["GET"])
def get_part(id):
    part = Inventory.query.get_or_404(id)
    return inventory_schema.jsonify(part)


@inventory_bp.route("/<int:id>", methods=["PUT"])
def update_part(id):
    part = Inventory.query.get_or_404(id)
    data = request.json
    part.name = data.get("name", part.name)
    part.price = data.get("price", part.price)
    db.session.commit()
    return inventory_schema.jsonify(part)


@inventory_bp.route("/<int:id>", methods=["DELETE"])
def delete_part(id):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()
    return jsonify({"msg": f"Part {id} deleted"})

