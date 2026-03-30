import pytest
import os

os.environ["FLASK_ENV"] = "testing"

from app import create_app
from app.extensions import db as _db
from app.database.schema import User, Role, Permission
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="session")
def app():
    app = create_app()
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def auth_headers(app):
    with app.app_context():
        permissions = [
            Permission(name="example.create", description="Create example"),
            Permission(name="example.delete", description="Delete example"),
        ]
        _db.session.add_all(permissions)
        _db.session.flush()

        role = Role(name="admin", description="Full access", permissions=permissions)
        _db.session.add(role)
        _db.session.flush()

        user = User(name="Test User", email="test@example.com", role=role)
        _db.session.add(user)
        _db.session.commit()

        token = create_access_token(identity=str(user.id))
        return {"Authorization": f"Bearer {token}"}
