from .model import UserCreate
from app.errors.handlers import ValidationError, NotFoundError
from marshmallow import ValidationError as MarshmallowValidationError

class UserController:
    def list_users(self, params):
        return [{"id": 1, "username": "dev_user"}]

    def create_user(self, json_data):
        try:
            data = UserCreate().load(json_data)
            return data
        except MarshmallowValidationError as err:
            raise ValidationError(message=err.messages)

    def get_user(self, user_id):
        if user_id != 1:
            raise NotFoundError(f"User {user_id} not found")
        return {"id": 1, "username": "dev_user"}