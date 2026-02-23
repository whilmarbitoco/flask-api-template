from app.extensions import db
from app.database.schema import User
from werkzeug.security import generate_password_hash, check_password_hash

class AuthRepository:
    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def create_user(self, email, name, password, age=None, role='user'):
        password_hash = generate_password_hash(password)
        new_user = User(
            email=email,
            name=name,
            age=age,
            password_hash=password_hash,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    def verify_password(self, user, password):
        if not user or not user.password_hash:
            return False
        return check_password_hash(user.password_hash, password)
    
    def get_user_by_id(self, user_id):
        return User.query.get(user_id)
