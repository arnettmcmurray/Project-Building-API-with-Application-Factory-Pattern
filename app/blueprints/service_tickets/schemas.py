from app.extensions import ma
from marshmallow import fields
from app.models import ServiceTicket

# === Simple nested references ===
class MechanicRef(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    specialty = fields.Str()

class InventoryRef(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    quantity = fields.Int()

class CustomerRef(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    phone = fields.Str()
    car = fields.Str()


# === Main Service Ticket Schema ===
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    description = ma.auto_field(required=True)
    date = ma.auto_field()
    status = ma.auto_field()

    customer = fields.Nested(CustomerRef)
    mechanics = fields.List(fields.Nested(MechanicRef))
    parts = fields.List(fields.Nested(InventoryRef))


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
