from marshmallow import Schema, fields, post_load
from app.models import Mechanic

# === Mechanic Schema ===
class MechanicSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    specialty = fields.Str()
    password = fields.Str(load_only=True, required=True)  # only accepted on input

    @post_load
    def make_mechanic(self, data, **kwargs):
        password = data.pop("password", None)
        mech = Mechanic(**data)
        if password:
            mech.set_password(password)
        return mech


# === Login Schema ===
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


# === Schema Instances for routes ===
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
login_schema = LoginSchema()
