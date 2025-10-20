from flask import request, jsonify
from app.extensions import db, cache
from app.models import Customer
from app.utils.auth import token_required
from .schemas import customer_schema, customers_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import customers_bp

print(">>> customers/routes.py loaded")

# === Create customer === (open for demo)
@customers_bp.route("", methods=["POST"])
def create_customer():
    try:
        customer = customer_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        db.session.add(customer)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return jsonify(customer_schema.dump(customer)), 201


# === Search customer by email ===
@customers_bp.route("/search", methods=["GET"])
@token_required
def search_customer_by_email():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email query parameter is required"}), 400

    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer_schema.dump(customer)), 200


# === Get all customers ===
@customers_bp.route("", methods=["GET"])
@token_required
@cache.cached(timeout=60)
def get_customers():
    customers = Customer.query.all()
    return jsonify(customers_schema.dump(customers)), 200


# === Update a customer ===
@customers_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json() or {}

    for field in ("name", "email", "phone", "car"):
        if field in data:
            setattr(customer, field, data[field])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return jsonify(customer_schema.dump(customer)), 200


# === Delete a customer ===
@customers_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"}), 200
