from app.extensions import ma
from app.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ServiceTicket
        load_instance = True

    id = ma.auto_field(dump_only=True)
    description = ma.auto_field(required=True)
    date = ma.auto_field()
    customer_id = ma.auto_field(required=True)

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

