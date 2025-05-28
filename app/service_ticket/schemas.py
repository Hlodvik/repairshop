from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models import Ticket

class TicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        load_instance = True
        include_relationships = True

    id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)
    mechanics = fields.List(fields.Int(), required=False)