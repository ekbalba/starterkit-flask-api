from flask import request
from flask_restful import Resource

from project_name.extensions.guard import guard
from project_name.libs.strings import gettext
from project_name.models.UserModel import UserModel
from project_name.schemas.UserSchema import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        if UserModel.lookup(user_data.email):
            return {"message": gettext("username_exists")}, 400
        new_user = UserModel(
            email=user_data.email,
            password=guard.hash_password(user_data.password),
            first_name=user_data.first_name.title(),
            last_name=user_data.last_name.title(),
        )
        try:
            new_user.save_to_db()
            data = {"message": gettext("register_success")}
            return data, 201
        except Exception as inst:
            data = {"message": gettext("register_fail"), "reason": str(inst)}
            return data, 401


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        not_include = ("first_name", "last_name")
        user_data = user_schema.load(user_json, partial=not_include)
        email = user_data.email
        password = user_data.password
        try:
            user_authenticated = guard.authenticate(email, password)
            jwt_token = guard.encode_jwt_token(user_authenticated)
            data = {"message": gettext("login_success"), "access_token": jwt_token}
            return data, 200
        except Exception as inst:
            data = {"message": gettext("login_fail"), "reason": str(inst)}
            return data, 401


class TestIndex(Resource):
    @classmethod
    def get(cls):
        return {"message": gettext("test_index")}, 200
