from app.db.schemas.user import User
from .danger import (
    serialize_jwt_token,
    EMAIL_CONF_TOKEN,
    decode_token,
    RESET_PASSWORD_TOKEN,
)
from app.exceptions import AppException


def email_verification_token(user: User):
    return serialize_jwt_token({"user_id": user.id_, "token_type": EMAIL_CONF_TOKEN})


def reset_password_token(user: User):
    return serialize_jwt_token(
        {"user_id": user.id_, "token_type": RESET_PASSWORD_TOKEN}
    )


def should_verify_email(token: str) -> str:
    t = decode_token(token)
    if t is None:
        raise AppException("Token expired")
    return t["user_id"]


def allow_password_reset(token: str) -> str:
    t = decode_token(token)
    if t is None:
        raise AppException("Token expired")
    return t["user_id"]
