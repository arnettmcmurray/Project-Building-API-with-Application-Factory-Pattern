from app.extensions import ma
from marshmallow import fields
from app.models import Mechanic, Customer, ServiceTicket, Inventory
from app.blueprints.service_tickets.schemas import ServiceTicketSchema

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    phone = ma.auto_field()
    car = ma.auto_field()

    # Nested: show customer's tickets
    tickets = fields.List(fields.Nested(lambda: ServiceTicketSchema(exclude=("customer",))))

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

