from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models import Inventory

class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True