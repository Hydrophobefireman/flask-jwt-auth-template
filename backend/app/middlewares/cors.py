from flask import Request

from app.internal.helpers.cors_headers import apply_cors

from ._handler import State


def middleware(request: Request, state: State):
    yield
    resp = state.response
    apply_cors(resp)
    return resp
