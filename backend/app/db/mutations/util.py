from app.db import db
from app.db.errors import check_integrity_error


# pylint: disable=E1101
def commit():
    try:
        db.session.commit()
    except Exception as e:
        check_integrity_error(e)


def create(col, batch, return_json: bool):
    db.session.add(col)
    js = col.as_json if return_json else None
    if not batch:
        commit()
    return col if not return_json else js


def delete(col):
    db.session.delete(col)
    commit()
