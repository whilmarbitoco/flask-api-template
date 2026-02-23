from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError as MarshmallowValidationError
from datetime import timedelta
from .model import RegisterSchema, LoginSchema, UserResponseSchema
from .repository import AuthRepository
from app.errors.handlers import ValidationError, UnauthorizedError, ConflictError

class AuthController:
    def __init__(self):
        self.repository = AuthRepository()
        self.register_schema = RegisterSchema()
        self.login_schema = LoginSchema()
        self.user_response_schema = UserResponseSchema()
    
    def register_user(self, json_data):
        try:
            validated_data = self.register_schema.load(json_data)
        except MarshmallowValidationError as err:
            raise ValidationError(message=err.messages)
        
        if self.repository.get_user_by_email(validated_data['email']):
            raise ConflictError(message="Email already registered")
        
        user = self.repository.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            age=validated_data.get('age')
        )
        
        return {
            "message": "User registered successfully",
            "user_id": user.id
        }
    
    def login_user(self, json_data):
        try:
            validated_data = self.login_schema.load(json_data)
        except MarshmallowValidationError as err:
            raise ValidationError(message=err.messages)
        
        user = self.repository.get_user_by_email(validated_data['email'])
        
        if not self.repository.verify_password(user, validated_data['password']):
            raise UnauthorizedError(message="Invalid email or password")
        
        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims,
            expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            expires_delta=timedelta(days=30)
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": self.user_response_schema.dump(user)
        }
    
    def refresh_access_token(self, user_id):
        user = self.repository.get_user_by_id(user_id)
        
        if not user:
            raise UnauthorizedError(message="User not found")
        
        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity=user_id,
            additional_claims=additional_claims,
            expires_delta=timedelta(minutes=15)
        )
        
        return {"access_token": access_token}
