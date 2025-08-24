from app.extensions import ma
from marshmallow import fields
from app.models import Mechanic

class MechanicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Mechanic
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    specialty = ma.auto_field(required=False)

    # Accepts password on input only; never dumped
    password = fields.String(load_only=True, required=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


# === Login Schema (for login route) ===
class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

login_schema = LoginSchema()
