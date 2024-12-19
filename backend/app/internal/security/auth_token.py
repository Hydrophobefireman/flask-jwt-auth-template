"""Decorators that ensure authentication is provided"""

from typing import Literal, TypedDict

from flask import request
from werkzeug.datastructures import Headers

from app.db.queries.user import get_user_by_id, get_user_by_email
from app.exceptions import AppException
from app.settings import app_settings
from app.internal.security.danger import (
    ACCESS_TOKEN,
    REFRESH_TOKEN,
    decode_token,
    generate_password_hash,
    serialize_jwt_token,
)
from app.internal.security.danger import check_password_hash as check
from app.internal.security.danger import decode_token as decode


class AccessToken(TypedDict):
    token_type: Literal["access"]
    user_id: str
    user_name: str
    is_admin: bool


class RefreshToken(TypedDict):
    token_type: Literal["refresh"]
    user_id: str
    integrity: str


class AccessTokenExpired(AppException):
    def __init__(self):
        super().__init__("refresh", 401)


def regenerate_access_token(
    refresh: RefreshToken,
) -> tuple[AccessToken | None, RefreshToken | None]:
    user_id = refresh["user_id"]
    integrity = refresh["integrity"]
    data = get_user_by_id(user_id)
    is_admin = data.is_admin
    user_name = data.user_name
    current = get_integrity(data.id_, data.password_hash)
    if check(integrity, current):
        return (
            issue_access_token(user_id, user_name, is_admin, data.has_verified_email),
            issue_refresh_token(user_id, data.password_hash),
        )
    return None, None


def issue_access_token(
    user_id: str, user_name: str, is_admin: bool, verified_email: bool
) -> AccessToken:
    return AccessToken(
        {
            "token_type": ACCESS_TOKEN,  # type:ignore
            "user_id": user_id,
            "user_name": user_name,
            "is_admin": is_admin,
            "verified_email": verified_email,
        }
    )


def issue_refresh_token(user_id, password_hash) -> RefreshToken:
    return RefreshToken(
        {
            "token_type": REFRESH_TOKEN,  # type:ignore
            "user_id": user_id,
            "integrity": generate_password_hash(get_integrity(user_id, password_hash)),
        }
    )


def get_integrity(user_id: str, password_hash: str):
    return f"{user_id}{app_settings.refresh_token_salt}{password_hash}"


def extract_access_token(bearer_token: str, strict: bool) -> AccessToken | None:
    if not bearer_token:
        if strict:
            raise AppException("No authentication provided")
        return None
    try:
        access = decode(bearer_token)
    except Exception:
        if strict:
            raise AppException("invalid token")
        return None

    if access is None:
        if strict:
            raise AccessTokenExpired()
        return None

    return AccessToken(access)


def get_access_token(strict=True):
    headers = request.headers
    received_access_token = get_bearer_token(headers)
    return extract_access_token(received_access_token, strict)


def get_bearer_token(headers: Headers) -> str:
    auth = headers.get("Authorization", "")
    # count= 1 as in the rare case that the bearer token itself has the word Bearer in it we want it intact
    return auth.replace("Bearer", "", 1).strip()


def authenticate(email: str, password: str):
    user_data = get_user_by_email(email)
    pw_hash = user_data.password_hash
    if not check(pw_hash, password):
        raise AppException("Incorrect Password", code=401)
    user_name = user_data.user_name
    is_admin = user_data.is_admin
    access_token = serialize_jwt_token(
        issue_access_token(
            user_data.id_, user_name, is_admin, user_data.has_verified_email
        )
    )  # type: ignore
    refresh_token = serialize_jwt_token(issue_refresh_token(user_data.id_, pw_hash))  # type: ignore
    return access_token, refresh_token, user_data


def regenerate_auth_tokens_from_refresh(
    refresh_token: str,
) -> tuple[AccessToken, RefreshToken]:
    decoded_refresh: RefreshToken | None = decode_token(refresh_token)
    if decoded_refresh is None:
        raise AppException("re-auth")
    access, refresh = regenerate_access_token(decoded_refresh)
    if access is None or refresh is None:
        raise AppException("re-auth")
    return access, refresh
