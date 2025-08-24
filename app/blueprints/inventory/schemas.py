from app.extensions import ma
from app.models import Inventory

class InventorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventory
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    price = ma.auto_field(required=True)

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
