from app.extensions import ma
from marshmallow import fields
from app.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)

    # === Homework-required fields ===
    name = fields.String(required=True)
    specialty = fields.String(required=False)


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


# === Login Schema (for login route) damn error===
class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

login_schema = LoginSchema()
