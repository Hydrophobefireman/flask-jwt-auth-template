from os import path
from pathlib import Path
from tempfile import gettempdir

from dotenv import load_dotenv

load_dotenv()


try:
    _CACHE_DIR = Path(gettempdir(), "@cache").resolve()
    _CACHE_DIR.mkdir(exist_ok=True)
except:  # noqa: E722
    _CACHE_DIR = Path(path.dirname(path.realpath(__file__)), "@cache").resolve()
    _CACHE_DIR.mkdir(exist_ok=True)
CACHE_DIR = str(_CACHE_DIR)
print(f"[Cache] dir: {CACHE_DIR}")


# del environ
del Path
del path
