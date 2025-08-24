from app.extensions import ma
from marshmallow import fields
from app.models import Mechanic
from app.blueprints.service_tickets.schemas import ServiceTicketSchema

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)

    # accept plain password, hide password_hash
    password = fields.String(load_only=True, required=True)
    password_hash = fields.String(dump_only=True)   # exclude input

    name = fields.String(required=True)
    specialty = fields.String(required=False)

    # Nested: show tickets mechanic works on
    tickets = fields.List(fields.Nested(lambda: ServiceTicketSchema(exclude=("mechanics",))))
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


# === Login Schema (for login route) ===
class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

login_schema = LoginSchema()
