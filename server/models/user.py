from secrets import token_urlsafe
from time import time

from server.danger import generate_password_hash
from server.util import AppException, sanitize
from sqlalchemy.orm import validates

from .shared import db


class User(db.Model):
    # pylint: disable=E1101
    _id: str = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
    user: str = db.Column(db.String(30), unique=True, nullable=False)
    name: str = db.Column(db.String(30), nullable=False)
    password_hash: str = db.Column(db.String, nullable=False)
    created_at: int = db.Column(db.Integer)
    # pylint: enable=E1101

    @property
    def as_json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "user": self.user,
            "created_at": self.created_at,
            "_secure_": {},
        }

    @validates("user")
    def _validate_user(self, key, user: str):
        length = len(user)
        if length > 30:
            raise AppException("Username cannot be longer than 30 characters")
        if length < 4:
            raise AppException("Username cannot be shorter than 4 characters")
        if sanitize(user) != user:
            raise AppException("Username cannot have special characters or whitespace")
        return user

    @validates("password_hash")
    def _validate_password(self, key, password: str):
        length = len(password)
        if length < 4:
            raise AppException("Password cannot be shorter than 4 characters")
        return generate_password_hash(password)

    def __init__(
        self,
        user: str = None,
        name: str = None,
        password: str = None,
    ):
        raise_if_invalid_data(user, name, password)
        self._id = token_urlsafe(20)
        self.user = user.lower()
        self.name = name
        self.password_hash = password
        self.created_at = time()


def raise_if_invalid_data(*args):
    if any(not x or not ((x).strip() if isinstance(x, str) else True) for x in args):
        raise AppException("Invalid Input")
