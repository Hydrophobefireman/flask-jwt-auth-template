from app.db.schemas.user import User


def confirm_email(user: User, base: str):
    raise NotImplementedError


def reset_password(user: User, base: str):
    raise NotImplementedError
