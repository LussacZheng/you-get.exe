import os
import platform
import re
import subprocess
import sys

from scripts import ROOT

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


def pyinstaller_version(lock_file="poetry.lock") -> str:
    """Get the version of currently installed PyInstaller."""

    return _read_and_search(os.path.join(ROOT, lock_file), 'name = "pyinstaller"\nversion = "(.*)"')


def you_get_version(repo_path: str) -> str:
    """Return the version string of 'you-get'. (Defined in `src/you_get/version.py`)"""

    return _read_and_search(os.path.join(ROOT, repo_path, "src/you_get/version.py"), r"version.*'([\d.]+)'")


def you_get_version_tuple(repo_path: str) -> tuple:
    """Return the version tuple of 'you-get'."""

    v = [int(x) for x in you_get_version(repo_path).split(".")]
    while len(v) < 4:
        v.append(0)
    return tuple(v)


def _read_and_search(file_path: str, regexp: str) -> str:
    """Read th file and return the first matched sub-string."""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return re.search(regexp, f.read()).group(1)
    except FileNotFoundError as e:
        sys.exit(e)
    except AttributeError:
        sys.exit(f"[ERROR] Unable to find substring matching `{regexp}` in `{file_path}`")
