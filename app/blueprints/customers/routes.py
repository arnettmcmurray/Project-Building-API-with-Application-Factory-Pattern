from flask import request, jsonify
from app.extensions import db
from app.models import Customer
from app.utils.auth import token_required
from .schemas import customer_schema, customers_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import customers_bp


# === Create customer ===
@customers_bp.route("/create", methods=["POST"])
def create_customer():
    try:
        customer = customer_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "ValidationError", "details": err.messages}), 400

    try:
        db.session.add(customer)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "IntegrityError", "message": "Email already exists"}), 409

    return jsonify(customer_schema.dump(customer)), 201


# === Get all customers ===
@customers_bp.route("/get_all", methods=["POST"])
@token_required
def get_all_customers():
    data = request.get_json() or {}
    customers = Customer.query.all()
    if not customers:
        return jsonify({"message": "No customers found"}), 200
    return jsonify(customers_schema.dump(customers)), 200


# === Get single customer ===
@customers_bp.route("/get_one", methods=["POST"])
@token_required
def get_one_customer():
    data = request.get_json() or {}
    email = data.get("email")
    if not email:
        return jsonify({"error": "Missing email"}), 400
    customer = Customer.query.filter_by(email=email).first_or_404()
    return jsonify(customer_schema.dump(customer)), 200


# === Update customer ===
@customers_bp.route("/update", methods=["PUT"])
@token_required
def update_customer():
    data = request.get_json() or {}
    cust_id = data.get("id")
    if not cust_id:
        return jsonify({"error": "Missing id"}), 400

    customer = Customer.query.get_or_404(cust_id)
    for field in ("name", "email", "phone", "car"):
        if field in data:
            setattr(customer, field, data[field])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "IntegrityError", "message": "Email already exists"}), 409

    return jsonify(customer_schema.dump(customer)), 200


# === Delete customer ===
@customers_bp.route("/delete", methods=["DELETE"])
@token_required
def delete_customer():
    data = request.get_json() or {}
    cust_id = data.get("id")
    if not cust_id:
        return jsonify({"error": "Missing id"}), 400

    customer = Customer.query.get_or_404(cust_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {cust_id} deleted"}), 200
