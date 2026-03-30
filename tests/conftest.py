import pytest
import os

os.environ["FLASK_ENV"] = "testing"

from app import create_app
from app.extensions import db as _db
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
        token = create_access_token(identity="test-user")
        return {"Authorization": f"Bearer {token}"}
