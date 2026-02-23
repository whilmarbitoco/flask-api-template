from marshmallow.fields import Email, Integer, String
from marshmallow import validate, Schema

class UserCreate(Schema):
    email = Email(required=True)
    age = Integer(required=True, validate=validate.Range(min=16, max=120))
    name = String(required=True, validate=validate.Length(min=2, max=120))

class UserRead(Schema):
    id = Integer(required=True)
    email = Email(required=True)
    age = Integer(required=True)
    name = String(required=True)