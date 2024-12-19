from flask import Request
from ._handler import State

from app.internal.helpers.cors_headers import apply_cors


def middleware(request: Request, state: State):
    yield
    resp = state.response
    apply_cors(resp)
    return resp
