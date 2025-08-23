from app.models import Customer
from app.extensions import ma
from marshmallow import fields

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True   

    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    car = fields.Str(required=False)   

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)