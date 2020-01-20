from project_name.config import DevelopmentConfig
from project_name.extensions.db import db
from project_name.extensions.guard import guard
from project_name.extensions.ma import ma
from flask import Flask, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from project_name.models.UserModel import UserModel
from project_name.resources.UserResource import UserLogin, UserRegister, TestIndex


def create_app(config_filename=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    api.add_resource(UserRegister, "/v1/user")
    api.add_resource(UserLogin, "/v1/login")
    api.add_resource(TestIndex, "/")

    with app.app_context():
        guard.init_app(app, UserModel)
        db.init_app(app)
        ma.init_app(app)

    return app
