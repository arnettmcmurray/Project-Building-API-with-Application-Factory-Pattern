from app.extensions import ma
from marshmallow import fields
from app.models import Mechanic, Customer, ServiceTicket, Inventory

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    description = ma.auto_field(required=True)
    date = ma.auto_field()
    status = ma.auto_field()

    # Nested: customer, mechanics, and parts
    customer = fields.Nested("CustomerSchema", exclude=("tickets",))
    mechanics = fields.List(fields.Nested("MechanicSchema", exclude=("tickets",)))
    parts = fields.List(fields.Nested("InventorySchema", exclude=("tickets",)))

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

