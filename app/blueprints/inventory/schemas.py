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
