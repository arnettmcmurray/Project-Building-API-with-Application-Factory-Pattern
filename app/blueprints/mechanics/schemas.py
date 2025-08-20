# app/blueprints/mechanics/schemas.py
from app.extensions import ma
from marshmallow import fields
from app.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True
        # do NOT exclude password

    # fields
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)  # accept on input, never output
    name = fields.String(required=True)
    specialty = fields.String(allow_none=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

login_schema = LoginSchema()
