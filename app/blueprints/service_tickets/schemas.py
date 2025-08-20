from app.extensions import ma
from marshmallow import fields
from app.models import ServiceTicket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

    description = fields.String(required=True)
    status = fields.String(required=False)

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)

