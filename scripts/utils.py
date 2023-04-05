import hashlib
import os
import platform
import re
import subprocess
import time
import zipfile


def path_resolve(base: str, *paths: str) -> str:
    """Return the normalized path after joining the two or more paths.

    For example, path_resolve("a/b/c", "..\\d\\.\\e.txt", "../../f/g.jpg" == "a/b/f/g.jpg".
    """

    return os.path.normpath(os.path.join(base, *paths))


def sha256sum(file_path: str) -> str:
    """Return the SHA-256 checksum of input file.

    :return: empty string if the `path` is not an existing regular file.
    """

    if not os.path.isfile(file_path):
        return ""
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def date() -> str:
    """Return current date in the format of `%y%m%d`."""

    return time.strftime("%y%m%d", time.localtime())


def date_tuple() -> str:
    """Return current date in the format of zero-trimmed `(%Y, %#m, %#d)`."""

    return time.strftime("(%Y, %#m, %#d, 0)", time.localtime())


def py_version() -> str:
    """Get the version of current python interpreter `major.minor.patch`."""

    return platform.python_version()


def py_version_strings_match(a: str, b: str) -> bool:
    """Determine whether one of the two version strings matches the other."""

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


def crlf_to_lf(file_path: str):
    """Convert the line endings of the input file from CRLF to LF.

    Note: this works in-place, which means it will overwrite the original file.
    """

    with open(file_path, "rb") as f:
        content = f.read()
    content = content.replace(b"\r\n", b"\n")
    with open(file_path, "wb") as f:
        f.write(content)


def compress_files(output_name: str, base_dir: str, file_list: list, comment: str = ""):
    """Compress all the files of `file_list` inside the `base_dir`, into a ZIP archive.

    :param output_name: Filename of the output ZIP archive
    :param base_dir: Root directory as the prefix for `file_list`
    :param file_list: A list of filenames inside the `base_dir`
    :param comment: The comment string to be written into the ZIP file. If a path to text file
        is provided, the contents of that file are used instead.
    """

    with zipfile.ZipFile(output_name, "w", zipfile.ZIP_DEFLATED) as z:
        for file in file_list:
            z.write(os.path.join(base_dir, file), arcname=file)
        if os.path.isfile(comment):
            with open(comment, "r", encoding="utf-8") as f:
                z.comment = f.read().encode("utf-8")
        else:
            z.comment = comment.encode("utf-8")


def poetry_version() -> str:
    """Get the version of currently installed poetry."""
    try:
        version = subprocess.run(["poetry", "--version"], capture_output=True, text=True).stdout.strip()
        return re.search(r"(\d[\d.]+)", version).group(1)
    except (subprocess.CalledProcessError, FileNotFoundError, AttributeError):
        return "unknown poetry version"
