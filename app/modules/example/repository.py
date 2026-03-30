from app.extensions import db
from app.database.schema import User


class ExampleRepository:
    def get_all(self):
        return db.session.execute(db.select(User)).scalars().all()

    def get_by_id(self, user_id):
        return db.session.get(User, user_id)

    def create(self, name, email, age):
        user = User(name=name, email=email, age=age)
        db.session.add(user)
        db.session.commit()
        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user
