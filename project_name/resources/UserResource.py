from extensions.guard import guard
from flask import request, jsonify, make_response
from flask_restful import Resource
from libs.strings import gettext
from models.UserModel import UserModel
from schemas.UserSchema import UserSchema

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
            response = jsonify({"message": gettext("user_registered")})
            response.status_code = 201
            return response
        except:
            return {"message": gettext("user_invalid_credentials")}, 400


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json_data = request.get_json()
        user_data = user_schema.load(
            user_json_data, partial=("first_name", "last_name")
        )

        user_authenticated = guard.authenticate(user_data.email, user_data.password)
        response = jsonify({"message": gettext("user_login_successful")})
        response.headers["Authorization"] = guard.encode_jwt_token(user_authenticated)
        response.status_code = 200
        return response


class TestUser(Resource):
    @classmethod
    def get(cls):
        a = jsonify("test")
        a.status_code
        return a
