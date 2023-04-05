import os

from scripts.utils import path_resolve

ROOT = path_resolve(os.path.dirname(os.path.realpath(__file__)), "../")
POETRY_LOCK = os.path.join(ROOT, "poetry.lock")
