from app.models import Customer
from app.extensions import ma

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

# single record
customer_schema = CustomerSchema()

# many records
customers_schema = CustomerSchema(many=True)