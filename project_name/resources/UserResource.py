from project_name.extensions.guard import guard
from flask import request, jsonify, make_response
from flask_restful import Resource
from project_name.libs.strings import gettext
from project_name.models.UserModel import UserModel
from project_name.schemas.UserSchema import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json_data = request.get_json()
        user_data = user_schema.load(user_json_data)
        if UserModel.lookup(user_data.email):
            return {"message": gettext("user_username_exists")}, 400

        new_user = UserModel(
            email=user_data.email,
            password=guard.hash_password(user_data.password),
            first_name=user_data.first_name.title(),
            last_name=user_data.last_name.title(),
        )
        try:
            new_user.save_to_db()
            return {"message": gettext("user_registered")}, 201
        except:
            return {"message": gettext("user_invalid_credentials")}, 400


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json_data = request.get_json()
        user_data = user_schema.load(
            user_json_data, partial=("first_name", "last_name")
        )
        try:
            user_authenticated = guard.authenticate(user_data.email, user_data.password)
            jwt_token = guard.encode_jwt_token(user_authenticated)
            return {"message": gettext("user_login_successful")}, 200 , {"Authorization": jwt_token}
        except:
            return {"message": gettext("user_invalid_credentials")}, 400


class TestIndex(Resource):
    @classmethod
    def get(cls):
        return {"message": gettext("test_index")}, 200
