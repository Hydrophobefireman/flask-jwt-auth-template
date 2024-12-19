# pylint: disable=E0213
from typing import Optional
from pydantic import AfterValidator, StringConstraints, Field

from app.internal.helpers import sanitize

from app.exceptions import AppException
from app.models.base import CustomBase
from pydantic import BaseModel, EmailStr
from typing_extensions import Annotated
from app.settings import app_settings


def validate_user(user: str):
    sanitized = sanitize(user)
    if sanitized != user.lower():
        raise AppException(
            "User cannot contain invalid characters. Only letters, numbers and underscores allowed."
        )
    return sanitized


class UserSession(BaseModel):
    user_id: Optional[str]
    user_name: Optional[str]
    is_admin: bool
    if app_settings.email_features_enabled:
        verified_email: bool


PasswordType = Annotated[str, StringConstraints(min_length=4)]
UserName = Annotated[
    Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=100, to_lower=True)
    ],
    AfterValidator(validate_user),
]


class AuthModel(BaseModel):
    user_name: UserName


class LoginModel(BaseModel):
    email: EmailStr
    password: PasswordType


class _UserBase(AuthModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, max_length=256)]
    email: EmailStr


class UserEditable(BaseModel):
    user_name: Optional[UserName] = Field(default=None)
    name: Optional[
        Annotated[str, StringConstraints(strip_whitespace=True, max_length=256)]
    ] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)


class UserIn(_UserBase):
    is_admin: bool
    password: PasswordType


class UserOut(CustomBase):
    id_: str
    user_name: str
    name: str
    is_admin: bool
    if app_settings.email_features_enabled:
        has_verified_email: bool


class UserOutSecure(UserOut):
    secure: dict = Field(alias="_secure_")


class _TokenModel(BaseModel):
    token: str


class ConfirmEmail(_TokenModel): ...


class ResetPassword(_TokenModel):
    password: PasswordType
