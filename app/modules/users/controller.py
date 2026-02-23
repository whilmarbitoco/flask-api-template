from .model import UserCreate, UserRead
from app.errors.handlers import ValidationError
from marshmallow import ValidationError as MarshmallowValidationError
from .service import UserService
from app.utils.lib import to_dict_list


class UserController:
    """HTTP layer - handles validation and serialization"""

    def __init__(self):
        self.service = UserService()

    def list_users(self, params) -> list[UserRead]:
        """Get all users and serialize for HTTP response"""
        users = self.service.get_all_users()
        return to_dict_list(users, UserRead())

    def create_user(self, json_data):
        """Validate input, create user, serialize response"""
        try:
            validated_data = UserCreate().load(json_data)
            user = self.service.create_user(**validated_data)
            return UserRead().dump(user)
            
        except MarshmallowValidationError as err:
            raise ValidationError(message=err.messages)

    def get_user(self, user_id):
        """Get user by ID and serialize for HTTP response"""
        user = self.service.get_user_by_id(user_id)
        return UserRead().dump(user)