import hashlib
import time


def date() -> str:
    """Return current date in the format of `%y%m%d`."""

    return time.strftime("%y%m%d", time.localtime())


def date_tuple() -> str:
    """Return current date in the format of zero-trimmed `(%Y, %#m, %#d)`."""

    return time.strftime("(%Y, %#m, %#d, 0)", time.localtime())


def sha256sum(file_path: str) -> str:
    """Return the SHA-256 checksum of input file."""

    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def crlf_to_lf(file_path: str) -> bytes:
    """Return the content of input file, with line endings converted from CRLF to LF."""

    with open(file_path, "rb") as f:
        return f.read().replace(b"\r\n", b"\n")
