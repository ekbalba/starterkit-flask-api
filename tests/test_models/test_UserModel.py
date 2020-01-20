from project_name.extensions.guard import guard
from project_name.models.UserModel import UserModel


def test_new_user(new_user):
    assert new_user.email == "admin@google.net"
