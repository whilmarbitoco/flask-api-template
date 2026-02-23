from app.modules.auth.repository import AuthRepository
from app.errors.handlers import ConflictError, UnauthorizedError

class AuthService:
    """Pure business logic for authentication - no HTTP concerns"""
    
    def __init__(self):
        self.repository = AuthRepository()
    
    def register_user(self, email, name, password, age=None):
        """Register a new user - returns User entity"""
        if self.repository.get_user_by_email(email):
            raise ConflictError(message="Email already registered")
        
        user = self.repository.create_user(
            email=email,
            name=name,
            password=password,
            age=age
        )
        return user
    
    def authenticate_user(self, email, password):
        """Authenticate user credentials - returns User entity or raises error"""
        user = self.repository.get_user_by_email(email)
        
        if not self.repository.verify_password(user, password):
            raise UnauthorizedError(message="Invalid email or password")
        
        return user
    
    def get_user_by_id(self, user_id):
        """Get user by ID - returns User entity or None"""
        return self.repository.get_user_by_id(user_id)
