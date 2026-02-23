from marshmallow import ValidationError as MarshmallowValidationError
from .model import RegisterSchema, LoginSchema, UserResponseSchema
from .service import AuthService
from app.errors.handlers import ValidationError, UnauthorizedError
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

class AuthController:
    """HTTP layer - handles validation, serialization, and token generation"""
    
    def __init__(self):
        self.service = AuthService()
        self.register_schema = RegisterSchema()
        self.login_schema = LoginSchema()
        self.user_response_schema = UserResponseSchema()
    
    def register_user(self, json_data):
        """Validate input, call service, return serialized response"""
        try:
            validated_data = self.register_schema.load(json_data)
        except MarshmallowValidationError as err:
            raise ValidationError(message=err.messages)
        
        user = self.service.register_user(
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
        """Validate input, authenticate, generate tokens, return response"""
        try:
            validated_data = self.login_schema.load(json_data)
        except MarshmallowValidationError as err:
            raise ValidationError(message=err.messages)
        
        user = self.service.authenticate_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # HTTP concern: Generate JWT tokens
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
        """Get user, generate new token, return response"""
        user = self.service.get_user_by_id(user_id)
        
        if not user:
            raise UnauthorizedError(message="User not found")
        
        # HTTP concern: Generate JWT token
        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity=user_id,
            additional_claims=additional_claims,
            expires_delta=timedelta(minutes=15)
        )
        
        return {"access_token": access_token}
