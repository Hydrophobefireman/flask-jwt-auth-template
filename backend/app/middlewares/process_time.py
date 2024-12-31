from time import time

from flask import Request

from ._handler import State


def middleware(request: Request, state: State):
    start = time()
    yield
    process = time() - start
    state.response.headers.add("x-process-time", str(round(process, 2)))
