from app.modules.example.repository import ExampleRepository
from app.errors.handlers import NotFoundError


class ExampleService:
    def __init__(self, repository: ExampleRepository = None):
        self.repository = repository or ExampleRepository()

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, user_id):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found")
        return user

    def create(self, name, email, age):
        return self.repository.create(name=name, email=email, age=age)

    def delete(self, user_id):
        user = self.repository.delete(user_id)
        if not user:
            raise NotFoundError(message="User not found")
        return user
