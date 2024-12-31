from flask import request

from app.internal.helpers import apply_cors, get_origin, json_response


def not_found(e):
    resp = json_response(
        {"error": "Not Found"},
        status=404,
        headers={"access-control-allow-origin": get_origin(request)},
    )
    apply_cors(resp)
    return resp


def method_not_allowed(e):
    resp = json_response(
        {"error": "Method not allowed"},
        status=405,
        headers={"access-control-allow-origin": get_origin(request)},
    )
    apply_cors(resp)
    return resp
