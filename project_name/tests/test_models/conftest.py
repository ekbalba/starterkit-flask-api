import pytest
from config import TestingConfig
from extensions.guard import guard
from models.UserModel import UserModel
from tests.support.conftest import app


@pytest.fixture(scope="module")
def new_user(app):
    app = app(TestingConfig)
    user = UserModel(
        email="admin@google.net",
        password=guard.hash_password("123456"),
        first_name="errol".title(),
        last_name="alba".title(),
    )
    user.save_to_db()
    return user
