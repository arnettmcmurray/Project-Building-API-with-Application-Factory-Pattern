from app.extensions import ma
from marshmallow import fields
from app.models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    price = ma.auto_field(required=True)
    quantity = ma.auto_field(required=True)

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
