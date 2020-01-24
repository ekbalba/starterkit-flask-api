import pytest

from project_name import create_app
from project_name.config import TestingConfig
from project_name.extensions.db import db


@pytest.fixture(scope="module")
def app():
    def _app(config_class):
        app = create_app(config_class)
        app.test_request_context().push()

        if config_class is TestingConfig:
            # always starting with an empty DB
            db.drop_all()
            db.create_all()
        return app

    yield _app
