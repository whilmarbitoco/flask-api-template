from marshmallow.fields import Email, Integer
from marshmallow import validate, Schema

class UserCreate(Schema):
    email = Email(required=True)
    age = Integer(required=True, validate=validate.Range(min=16, max=120))