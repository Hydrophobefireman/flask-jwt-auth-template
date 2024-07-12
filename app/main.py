from dotenv import load_dotenv
from flask import Flask
from floodgate.flask import guard

from app.db import db
from app.internal.constants import DATABASE_URL
from app.internal.helpers import ip_resolver
from app.internal.helpers.client_errors import method_not_allowed, not_found
from app.routes import common, user

load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

app.url_map.strict_slashes = False


@app.before_request
@guard(ban_time=5, ip_resolver=ip_resolver, request_count=50, per=15)
def gate_check():
    pass


@app.after_request
def after_req(resp):
    from flask import request

    EXPOSE_HEADERS = ", ".join(("x-access-token", "x-refresh-token", "x-dynamic"))
    origin = request.headers.get("Origin", "*")
    resp.headers["access-control-allow-origin"] = origin
    resp.headers["access-control-allow-headers"] = request.headers.get(
        "access-control-request-headers", "*"
    )
    resp.headers["access-control-allow-credentials"] = "true"
    resp.headers["access-control-max-age"] = "86400"
    resp.headers["access-control-expose-headers"] = EXPOSE_HEADERS
    return resp


app.register_blueprint(common.router)
app.register_blueprint(user.router)

app.register_error_handler(404, not_found)
app.register_error_handler(405, method_not_allowed)
