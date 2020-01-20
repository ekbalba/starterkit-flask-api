import pytest
from project_name import create_app
from project_name.config import TestingConfig, get_env_db_url
from project_name.extensions.db import db


@pytest.fixture(scope="module")
def app():
    def _app(config_class):
        app = create_app(config_class)
        app.test_request_context().push()

        if config_class is TestingConfig:
            # always starting with an empty DB
            db.drop_all()
            from project_name.models.UserModel import UserModel

            db.create_all()

        return app

    yield _app
