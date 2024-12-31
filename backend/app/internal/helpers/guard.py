from typing import Optional, TypeVar

from app.exceptions.app_exception import AppException

G = TypeVar("G")


def guard(value: Optional[G], message: str = "Not found (Guard)") -> G:
    if not value:
        raise AppException(message, 404)
    return value
