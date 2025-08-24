from app.extensions import ma
from marshmallow import fields
from app.models import Mechanic, Customer, ServiceTicket, Inventory

class InventorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventory
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    price = ma.auto_field(required=True)

    # Nested: show tickets this part is used in
    tickets = fields.List(fields.Nested(lambda: ServiceTicketSchema(exclude=("parts",))))

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
