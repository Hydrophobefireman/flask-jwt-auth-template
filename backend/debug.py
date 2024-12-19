# ruff: noqa
from set_env import setup_env

setup_env()
from app.main import app
from app.main import *
from app.db.schemas import *
from app.models.user import *
from app.settings import *
from app.media.config import *
from app.media import upload

app.app_context().push()
