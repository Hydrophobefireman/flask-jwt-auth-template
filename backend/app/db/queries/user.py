from app.internal.helpers import sanitize
from app.internal.helpers.guard import guard

from ..schemas.user import User

message = "User does not exist"


def get_user_by_user_name(idx: str) -> User:
    if sanitize(idx) != idx or not idx:
        return guard(None, message)
    return guard(User.query.filter_by(user_name=idx).first(), message)


def get_user_by_email(email: str) -> User:
    return guard(User.query.filter_by(email=email).first(), message)


def get_user_by_id(idx: str) -> User:
    return guard(User.query.filter_by(id_=idx).first(), message)
