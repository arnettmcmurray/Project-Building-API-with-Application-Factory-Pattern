from flask import request, jsonify
from app.blueprints.mechanics import mechanics_bp
from app.extensions import db
from app.models import Mechanic
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError

# create mechanic
@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        mech = mechanic_schema.load(request.json)   # validate + build object
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.add(mech)
    db.session.commit()
    return mechanic_schema.jsonify(mech), 201


# get all mechanics
@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    mechs = Mechanic.query.all()
    return mechanics_schema.jsonify(mechs)

# update mechanic
@mechanics_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    mech = Mechanic.query.get_or_404(id)
    data = request.json
    mech.name = data.get("name", mech.name)
    mech.specialty = data.get("specialty", mech.specialty)
    db.session.commit()
    return mechanic_schema.jsonify(mech)

# delete mechanic
@mechanics_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mech = Mechanic.query.get_or_404(id)
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted"})
