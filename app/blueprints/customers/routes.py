# TODO: Customers blueprint not showing in flask routes (404s).
# Possible cause: migration not applied or model/schema mismatch.
# Endpoints defined but not registering → revisit after confirming DB.

from flask import Blueprint, request, jsonify
from app.extensions import db, cache
from app.models import Customer
from app.utils.auth import token_required
from .schemas import customer_schema, customers_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import customers_bp

print(">>> customers/routes.py loaded")

# === Create customer ===
@customers_bp.route("", methods=["POST"])
def create_customer():   # no token_required at moment
    try:
        customer = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        db.session.add(customer)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409   

    return customer_schema.jsonify(customer), 201


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

    return customer_schema.jsonify(customer), 200


# === Get all customers ===
@customers_bp.route("", methods=["GET"])
@token_required
@cache.cached(timeout=60)   # cache results for 60 seconds
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers), 200



# === Update a customer ===
@customers_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json or {}

    if "name" in data:
        customer.name = data["name"]
    if "email" in data:
        customer.email = data["email"]
    if "phone" in data:
        customer.phone = data["phone"]
    if "car" in data:
        customer.car = data["car"]

    try:   # IntegrityError handling
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return customer_schema.jsonify(customer), 200


# === Delete a customer ===
@customers_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"}), 200
