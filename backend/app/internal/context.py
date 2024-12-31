from enum import Enum, auto
from typing import Generic, TypeVar

from flask import g, request
from pydantic import BaseModel
from werkzeug.exceptions import UnsupportedMediaType

from app.exceptions import AppException
from app.models.user import UserSession

M = TypeVar("M", bound=BaseModel)


class ReqContentType(Enum):
    json = auto()
    binary = auto()


class Context(Generic[M]):
    body: M | None

    def __init__(
        self,
        model: type[M] | None = None,
        content_type: ReqContentType = ReqContentType.json,
    ) -> None:
        self._reqest = request
        self.binary = None
        try:
            if content_type == ReqContentType.binary:
                self.json = None
                self.binary = request.get_data()
            elif request.method.lower() in (
                "get",
                "head",
                "options",
                "connect",
                "delete",
            ):
                self.json = None
            else:
                self.json = request.get_json() or {}
        except UnsupportedMediaType:
            raise AppException("Expected JSON")
        self.body = model.model_validate(self.json) if model else None
        self.headers = request.headers
        self.auth: UserSession = g._auth_state  # pylint: disable=E0237
        self.args = request.args
        _host = self.headers.get("host")
        self.host = (
            self.headers.get("origin")
            or ("http://" if "localhost" in _host else "https://") + _host
        )
