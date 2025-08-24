from app.extensions import ma
from app.models import Customer

class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    phone = ma.auto_field(required=False)   # not forced, DB match
    car = ma.auto_field(required=False)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
