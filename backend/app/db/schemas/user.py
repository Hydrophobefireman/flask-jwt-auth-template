from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import TEXT

from app.db.base import db
from app.db.web import auto_json
from app.internal.helpers.gen_id import gen_id
from app.internal.security.danger import generate_password_hash
from app.settings import app_settings


@auto_json(skip=["password_hash"], serializers={}, secure=["email"])
class User(db.Model):  # type: ignore
    # pylint: disable=E1101
    id_: str = db.Column(TEXT, unique=True, nullable=False, primary_key=True)
    user_name: str = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name: str = db.Column(db.String(100), nullable=False)
    password_hash: str = db.Column(TEXT, nullable=False)
    created_at: datetime = db.Column(db.DateTime())
    is_admin: bool = db.Column(db.Boolean, default=False)
    if app_settings.email_features_enabled:
        # make a migration if you use it after generating tables!
        email: str = db.Column(db.String(), nullable=False)
        has_verified_email: bool = db.Column(db.Boolean, default=False)
    # pylint: enable=E1101

    def update_password(self, new_password: str):
        hsh = generate_password_hash(new_password)
        self.password_hash = hsh

    def __init__(
        self,
        *,
        user_name: str,
        name: str,
        password: str,
        email: str = None,
    ):
        self.id_ = gen_id()
        self.user_name = user_name.lower()
        if app_settings.email_features_enabled:
            self.email = email.lower()
        self.name = name
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.now(timezone.utc)
