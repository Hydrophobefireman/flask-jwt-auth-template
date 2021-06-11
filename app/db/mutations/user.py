from app.models.user import UserIn
from app.db.schemas import User
from app.db import db
from app.db.errors import check_integrity_error


# pylint: disable=E1101
def commit():
    try:
        db.session.commit()
    except Exception as e:
        check_integrity_error(e)


def _create(col, batch, return_json):
    js = col.as_json
    db.session.add(col)
    if not batch:
        commit()
    return col if not return_json else js


def create_user(user_model: UserIn, batch=False, return_json=False):
    u = user_model
    col = User(name=u.name, user=u.user, password_hash=u.password_hash)
    return _create(col, batch, return_json)
