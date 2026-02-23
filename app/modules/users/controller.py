from .model import UserCreate, UserRead
from app.errors.handlers import ValidationError, NotFoundError
from marshmallow import ValidationError as MarshmallowValidationError
from .repository import UserRepository
from app.utils.lib import to_dict_list


class UserController:

    def __init__(self):
        self.repository = UserRepository()

    def list_users(self, params) -> list[UserRead]:
        users = self.repository.get_all()
        return to_dict_list(users, UserRead())

    def create_user(self, json_data):
        try:
            validated_data = UserCreate().load(json_data)
            user = self.repository.add(**validated_data)
            return UserRead().dump(user)
            
        except MarshmallowValidationError as err:
            raise ValidationError(message=err.messages)

    def get_user(self, user_id):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found")
        return UserRead().dump(user)