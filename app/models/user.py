# pylint: disable=E0213
from typing import Optional
from pydantic.fields import Field
from pydantic.main import BaseModel
from app.internal.security.danger import generate_password_hash
from app.internal.helpers import sanitize

from app.exceptions import AppException
from app.models.base import CustomBase
from pydantic import constr, AfterValidator
from typing_extensions import Annotated


def validate_user(user: str):
    sanitized = sanitize(user)
    if sanitized != user.lower():
        raise AppException("User cannot contain invalid characters")
    return sanitized


class UserSession(BaseModel):
    user_id: Optional[str]
    user: Optional[str]
    is_admin: bool


PasswordType = Annotated[constr(min_length=4), AfterValidator(generate_password_hash)]
UserName = Annotated[constr(strip_whitespace=True, max_length=100), validate_user]


class AuthModel(BaseModel):
    user: Annotated[UserName, str.lower]


class LoginModel(AuthModel):
    password: PasswordType


class _UserBase(AuthModel):
    name: constr(strip_whitespace=True, max_length=256) # type: ignore


class UserEditable(_UserBase):
    pass


class UserIn(_UserBase):
    is_admin: bool
    password_hash: PasswordType


class UserOut(CustomBase):
    id_: str
    user: str
    name: str
    is_admin: bool


class UserOutSecure(UserOut):
    secure: dict = Field(alias="_secure_")
