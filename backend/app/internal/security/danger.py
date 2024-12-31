# ==============================================================
#                        Danger Zone
#   All the code needed to manage password
#   hashing and JWT Token creation/validation.
#   Other implementation ( Like storing the passwords
#   or requesting a new access_token to be done elsewhere )
# ==============================================================

from gc import collect
from http import HTTPStatus
from time import time as _time

import jwt as _jwt
import passlib.hash as _pwhash

from app.exceptions import AppException
from app.settings import app_settings

_hash_method = _pwhash.argon2.using(memory_cost=20 * 1024)

_jwt_encode_token = _jwt.encode
_jwt_decode_token = _jwt.decode


# =======================================================================
#                       Password Hashing
def check_password_hash(_hash: str, pw: str) -> bool:
    val = _hash_method.verify(pw, _hash)
    collect()
    return val


def generate_password_hash(pw):
    val = _hash_method.hash(pw)
    collect()
    return val


# =======================================================================

ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"
EMAIL_CONF_TOKEN = "email_conf"
RESET_PASSWORD_TOKEN = "reset_pass"
_ALLOWED_TOKEN_TYPES = (
    ACCESS_TOKEN,
    REFRESH_TOKEN,
    EMAIL_CONF_TOKEN,
    RESET_PASSWORD_TOKEN,
)

_EXPIRED = _jwt.exceptions.ExpiredSignatureError


# =======================================================================
#                            JWT Token Management
def serialize_jwt_token(data: dict) -> str:
    token_type = data.get("token_type")
    if token_type is None or token_type not in _ALLOWED_TOKEN_TYPES:
        raise Exception("Invalid token type")
    if token_type == ACCESS_TOKEN:
        # data['exp'] is JWT Spec for defining expireable tokens
        data["exp"] = _time() + app_settings.token_expiration_time
    if token_type in {EMAIL_CONF_TOKEN, RESET_PASSWORD_TOKEN}:
        data["exp"] = _time() + (
            max(60 * 15, app_settings.token_expiration_time)
        )  # atleast 15 mins
        print(data["exp"])
    return to_str(
        _jwt_encode_token(data, app_settings.jwt_signing_key, algorithm="HS512"),
    )


def decode_token(data: str) -> dict | None:
    try:
        return _jwt_decode_token(
            data, app_settings.jwt_signing_key, algorithms=["HS512"],
        )
    except _EXPIRED:
        return None
    except Exception as e:
        print(e)
        raise AppException("Invalid token", HTTPStatus.BAD_REQUEST)


def to_str(x):
    return x.decode() if isinstance(x, bytes) else x


# =======================================================================
