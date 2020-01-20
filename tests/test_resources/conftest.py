import json
import pytest
from project_name import create_app
from project_name.config import TestingConfig
from project_name.models.UserModel import UserModel
from project_name.extensions.db import db
from project_name.extensions.guard import guard


@pytest.fixture(scope="module")
def testing_client():
    app = create_app(TestingConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    @app.before_first_request
    def init_db():
        # always start with an empty DB
        db.drop_all()
        from project_name.models.UserModel import UserModel

        db.create_all()
        insert_test_user()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


def insert_test_user():
    user = UserModel(
        email="admin1@google.net",
        password=guard.hash_password("Admin123!"),
        first_name="errol".title(),
        last_name="alba".title(),
    )
    user.save_to_db()
    return None
