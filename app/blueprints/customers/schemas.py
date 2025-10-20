from app.extensions import ma
from marshmallow import fields
from app.models import Customer

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
    # Optional: tickets can be exposed later via ServiceTicketSchema if desired

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
