from flask import request

from app.internal.helpers.get_origin import get_origin

EXPOSE_HEADERS = ", ".join(("x-access-token", "x-refresh-token", "x-dynamic"))
ALLOWED_METHODS = ", ".join(("GET", "PUT", "POST", "PATCH", "DELETE"))


def apply_cors(resp):
    origin = get_origin(request)
    resp.headers["access-control-allow-origin"] = origin
    resp.headers["access-control-allow-headers"] = request.headers.get(
        "access-control-request-headers", "*"
    )
    resp.headers["access-control-allow-methods"] = ALLOWED_METHODS
    resp.headers["access-control-allow-credentials"] = "true"
    resp.headers["access-control-max-age"] = "86400"
    resp.headers["access-control-expose-headers"] = EXPOSE_HEADERS
