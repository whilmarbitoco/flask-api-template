from app.extensions import db
from app.database.schema import User

class UserRepository:
    def get_all(self):
        return User.query.all()

    def get_by_id(self, user_id):
        user = User.query.get(user_id)
        return user

    def add(self, name, email, age):
        new_user = User(name=name, email=email, age=age)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        return True