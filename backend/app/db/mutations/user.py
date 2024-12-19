from app.db.mutations.util import create, commit
from app.db.schemas.user import User
from app.models.user import UserIn
from app.db.queries.user import get_user_by_id
# pylint: disable=E1101


def create_user(user_model: UserIn, batch=False, return_json=False):
    u = user_model
    col = User(user_name=u.user_name, name=u.name, password=u.password, email=u.email)
    return create(col, batch, return_json)


def verify_user_email(user_id: str):
    u = get_user_by_id(user_id)
    u.has_verified_email = True
    commit()


def change_password(user_id: str, new_password: str):
    u = get_user_by_id(user_id)
    u.update_password(new_password)
    commit()
