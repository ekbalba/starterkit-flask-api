import os
from dotenv import load_dotenv

from os.path import dirname, join


def get_env_variable(variable_name):
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path=dotenv_path, verbose=True)
    try:
        return os.getenv(variable_name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(variable_name)
        raise Exception(message)


def create_db_url(db_name):
    return f"sqlite:///{db_name}.db"


# import .env variables for DB connection
# TODO: Unify these ENV variables by pulling from different dot files
def get_env_db_url(env_setting):
    if env_setting == "development":
        DB_NAME = get_env_variable("DEV_DB")
    elif env_setting == "testing":
        DB_NAME = get_env_variable("TESTING_DB")
    elif env_setting == "production":
        DB_NAME = get_env_variable("PROD_DB")

    return create_db_url(DB_NAME)


# DB URLS for each Environment
DEV_DB_URL = get_env_db_url("development")
TESTING_DB_URL = get_env_db_url("testing")
PROD_DB_URL = get_env_db_url("production")


class Config(object):
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # Praetorian
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_LIFESPAN = {"hours": 24}
    JWT_REFRESH_LIFESPAN = {"days": 30}

    # Flask Settings
    PROPAGATE_EXCEPTIONS = True
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = TESTING_DB_URL
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = PROD_DB_URL
    DEBUG = False
    TESTING = False
