from marshmallow import ValidationError as MarshmallowValidationError
from app.modules.example.model import ExampleCreate, ExampleRead
from app.modules.example.service import ExampleService
from app.errors.handlers import ValidationError


class ExampleController:
    def __init__(self, service: ExampleService = None):
        self.service = service or ExampleService()
        self.read_schema = ExampleRead()
        self.create_schema = ExampleCreate()

    def list(self):
        return self.read_schema.dump(self.service.get_all(), many=True)

    def get(self, user_id):
        return self.read_schema.dump(self.service.get_by_id(user_id))

    def create(self, json_data):
        try:
            data = self.create_schema.load(json_data)
        except MarshmallowValidationError as e:
            raise ValidationError(message=e.messages)
        return self.read_schema.dump(self.service.create(**data))

    def delete(self, user_id):
        self.service.delete(user_id)
