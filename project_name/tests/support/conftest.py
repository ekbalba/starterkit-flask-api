import pytest
from app import create_app
from config import TestingConfig, get_env_db_url
from extensions.db import db


@pytest.fixture(scope="module")
def app():
    def _app(config_class):
        app = create_app(config_class)
        app.test_request_context().push()

        if config_class is TestingConfig:
            # always starting with an empty DB
            db.drop_all()
            from models.UserModel import UserModel

            db.create_all()

        return app

    yield _app
    db.session.remove()
    if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
        db.drop_all()
