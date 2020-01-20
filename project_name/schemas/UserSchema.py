from project_name.extensions.ma import ma
from marshmallow import fields, validate
from project_name.models.UserModel import UserModel

validate_email = [validate.Email()]
validate_password = [
    validate.Regexp(regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).\S{8,}$")
]
validate_name = [validate.Regexp(regex=r"^[a-zA-Z][a-zA-Z ]+$")]


class UserSchema(ma.ModelSchema):
    first_name = fields.Str(validate=validate_name, required=True)
    last_name = fields.Str(validate=validate_name, required=True)
    email = fields.Email(validate=validate_email, required=True)
    password = fields.Str(validate=validate_password, required=True)

    class Meta:
        model = UserModel
        ordered = True
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
        ]
        dump_only = [
            "id",
        ]
