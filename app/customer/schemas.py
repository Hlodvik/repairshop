from app.extensions import ma 
from app.models import Customer
from marshmallow import fields
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)