from app import ma
from app.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_relationships = True


service_ticket_schema = ServiceTicketSchema()

service_tickets_schema = ServiceTicketSchema(many=True)
