from marshmallow import Schema, fields, validate


class ExampleCreate(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=16, max=120))


class ExampleRead(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    age = fields.Int(required=True)
