import pytest

from project_name.config import TestingConfig
from project_name.extensions.guard import guard
from project_name.models.UserModel import UserModel
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
