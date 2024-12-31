# mypy: ignore-errors
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from floodgate.flask import guard

import app.db.schemas
from app.db import db
from app.internal.helpers import ip_resolver
from app.internal.helpers.client_errors import method_not_allowed, not_found
from app.internal.helpers.cors_headers import apply_cors
from app.routes import common, user
from app.settings import app_settings

load_dotenv()
app = Flask(__name__)

app.config["SECRET_KEY"] = app_settings.flask_secret

app.config["SQLALCHEMY_DATABASE_URI"] = str(app_settings.database_url)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# Enable if needed
# with app.app_context():
#     db.create_all()


Migrate(app, db)
app.url_map.strict_slashes = False


@app.before_request
@guard(ban_time=5, ip_resolver=ip_resolver, request_count=50, per=15)
def gate_check():
    pass


@app.after_request
def after_req(resp):
    apply_cors(resp)
    return resp


app.register_blueprint(common.router)
app.register_blueprint(user.router)
app.register_error_handler(404, not_found)
app.register_error_handler(405, method_not_allowed)
