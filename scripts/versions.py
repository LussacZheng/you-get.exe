import os
import platform
import re
import subprocess

from scripts import ROOT
from scripts.utils import path_resolve

UNKNOWN = "unknown"


def py_version() -> str:
    """Get the version of current python interpreter `major.minor.patch`."""

    return platform.python_version()


def py_version_strings_match(a: str, b: str) -> bool:
    """Determine whether one of the two version strings matches the other.

    Example:
        py_version_strings_match("3.8", "3.8.10")   -> True
        py_version_strings_match("3.8.9", "3.8")    -> True
        py_version_strings_match("3.8.9", "3.8.10") -> False
    """

    if (not a.startswith(b)) and (not b.startswith(a)):
        return False
    list_a = a.split(".")
    list_b = b.split(".")
    short, long = (list_a, list_b) if len(list_a) < len(list_b) else (list_b, list_a)
    for (i, s) in enumerate(short):
        if s != long[i]:
            return False
    return True


def py_arch() -> str:
    """Get the architecture of current python interpreter ("32" or "64").

    Return the arch of the python interpreter currently in use.
    Note that if you are using a 32-bit python interpreter on 64-bit Windows, you will get "32".
    """

    return platform.architecture()[0].rstrip("bit")


def poetry_version() -> str:
    """Get the version of currently installed Poetry."""

    try:
        version = subprocess.run(["poetry", "--version"], capture_output=True, text=True).stdout.strip()
        return re.search(r"(\d[\d.]+)", version).group(1)
    except (subprocess.CalledProcessError, FileNotFoundError, AttributeError):
        return UNKNOWN


def pyinstaller_version() -> str:
    """Get the version of currently installed PyInstaller."""

    return _read_and_search(os.path.join(ROOT, "poetry.lock"), 'name = "pyinstaller"\nversion = "(.*)"')


def you_get_version() -> str:
    """Return the version string of 'you-get'. (Defined in `src/you_get/version.py`)"""

    return _read_and_search(path_resolve(ROOT, "repository/you-get/src/you_get/version.py"), r"version.*'([\d.]+)'")


def you_get_version_tuple() -> tuple:
    """Return the version tuple of 'you-get'."""

    v = [int(x) for x in you_get_version().split(".")]
    while len(v) < 4:
        v.append(0)
    return tuple(v)


def _read_and_search(file_path: str, regexp: str) -> str:
    """Read th file and return the first matched sub-string."""

    with open(file_path, "r", encoding="utf-8") as f:
        res = re.search(regexp, f.read())
    return res.group(1) if res is not None else UNKNOWN
