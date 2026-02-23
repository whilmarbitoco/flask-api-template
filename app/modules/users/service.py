from app.modules.users.repository import UserRepository
from app.errors.handlers import NotFoundError

class UserService:
    """Pure business logic for user operations - no HTTP concerns"""
    
    def __init__(self):
        self.repository = UserRepository()
    
    def get_all_users(self):
        """Get all users - returns list of User entities"""
        return self.repository.get_all()
    
    def get_user_by_id(self, user_id):
        """Get user by ID - returns User entity or raises NotFoundError"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found")
        return user
    
    def create_user(self, name, email, age):
        """Create a new user - returns User entity"""
        return self.repository.add(name=name, email=email, age=age)
