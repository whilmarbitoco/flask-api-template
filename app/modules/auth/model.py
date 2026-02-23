from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    age = fields.Int(validate=validate.Range(min=16, max=120))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserResponseSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
