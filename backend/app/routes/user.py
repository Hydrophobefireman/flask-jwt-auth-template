from flask import Blueprint

from app.db.mutations.user import create_user, verify_user_email, change_password
from app.db.mutations.util import commit
from app.db.queries.user import get_user_by_user_name, get_user_by_email
from app.decorators.api_response import api
from app.exceptions.app_exception import AppException
from app.internal.context import Context
from app.internal.helpers.json_response import json_response
from app.internal.security.auth_token import (
    AccessToken,
    authenticate,
    get_bearer_token,
    regenerate_auth_tokens_from_refresh,
)

from app.email.auth import (
    confirm_email,
    reset_password,
)
from app.internal.security.email_verification import (
    should_verify_email,
    allow_password_reset,
)
from app.internal.security.danger import decode_token, serialize_jwt_token
from app.models.user import (
    LoginModel,
    UserEditable,
    UserIn,
    UserOut,
    UserOutSecure,
    ConfirmEmail,
    ResetPassword,
)
from app.settings import app_settings

router = Blueprint("user", __name__, url_prefix="/users")


@router.post("/-/register", strict_slashes=False)
@api.none
def register():
    req = Context()
    body = UserIn(**req.json, is_admin=False)
    js = create_user(body)
    confirm_email(js, req.host)
    return {"user_data": js.as_json}


@router.post("/-/login")
@api.none
def login():
    req = Context(LoginModel)
    body = req.body
    access, refresh, user_data = authenticate(body.email, body.password)
    return json_response(
        {"user_data": user_data.as_json},
        headers={"x-access-token": access, "x-refresh-token": refresh},
    )


if app_settings.email_features_enabled:

    @router.post("/-/confirm-email")
    @api.none
    def api_confirm_email():
        context = Context(ConfirmEmail)
        token = context.body.token
        who = should_verify_email(token)
        verify_user_email(who)
        return {"ok": True}

    @router.post("/-/change-password")
    @api.none
    def api_change_passord():
        context = Context(ResetPassword)
        token = context.body.token
        new_password = context.body.password
        who = allow_password_reset(token)
        change_password(who, new_password)
        return {"ok": True}

    @router.get("/-/request-email-confirmation")
    @api.none
    def api_request_confirm_email():
        context = Context()
        user = get_user_by_email(context.args.get("email"))
        confirm_email(user, context.host)
        return {"ok": True}

    @router.post("/-/request-password-reset")
    @api.none
    def send_password_reset():
        context = Context()
        email = context.json.get("email")
        if not email:
            raise AppException("No email provided")
        user = get_user_by_email(email)
        reset_password(user, context.host)
        return {"ok": True}


@router.get("/-/token/refresh")
@api.none
def refresh_token():
    context = Context()
    headers = context.headers
    access_token = get_bearer_token(headers)
    decoded_access: AccessToken | None = (
        decode_token(access_token) if access_token else None
    )
    if decoded_access is None:
        refresh_token = headers.get("x-refresh-token")
        access, refresh = regenerate_auth_tokens_from_refresh(refresh_token)

        return json_response(
            {},
            headers={
                "x-access-token": serialize_jwt_token(access),
                "x-refresh-token": serialize_jwt_token(refresh),
            },
        )
    return {}


def get_user_details_common(user: str):
    req = Context()
    auth = req.auth
    is_me = user == "me"
    if is_me:
        if not auth.user_name:
            raise AppException("Not authenticated", 401)
        user = auth.user_name
    user_data = get_user_by_user_name(user)
    show_secure = user_data.user_name == auth.user_name or auth.is_admin
    model = (
        UserOutSecure.from_db(user_data) if show_secure else UserOut.from_db(user_data)
    )
    return {"user_data": model.model_dump(by_alias=True)}


@router.get("/me")
@api.strict
def user_details_mine():
    return get_user_details_common("me", False)


@router.get("/<user>/")
@api.lax
def user_details(user: str):
    return get_user_details_common(user, True)


@router.patch("/<user>/")
@api.strict
def edit(user: str):
    req = Context()  # type: ignore
    user = user.lower()
    if user != req.auth.user_name and not req.auth.is_admin:
        raise AppException("Not authorized to edit", 401)
    if not req.auth.is_admin:
        body = UserEditable.model_validate(req.json)  # type: ignore
    else:
        body = UserIn(**req.json)  # type: ignore
    user_data = get_user_by_user_name(user)
    user_data.user_name = body.user_name or user_data.user_name
    user_data.name = body.name or user_data.name
    user_data.email = body.email or user_data.email
    json = user_data.as_json
    commit()
    return json
