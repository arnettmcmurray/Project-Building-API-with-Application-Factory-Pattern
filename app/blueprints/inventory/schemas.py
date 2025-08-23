from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Inventory, ServiceTicketInventory

class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True

class ServiceTicketInventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicketInventory
        load_instance = True

# for singular or lis
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

service_ticket_inventory_schema = ServiceTicketInventorySchema()
service_ticket_inventories_schema = ServiceTicketInventorySchema(many=True)
