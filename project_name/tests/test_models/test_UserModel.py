from extensions.guard import guard
from models.UserModel import UserModel


def test_new_user(new_user):
    assert new_user.email == "admin@google.net"
