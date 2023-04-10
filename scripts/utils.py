import hashlib
import os
import time
import zipfile


def path_resolve(base: str, *paths: str) -> str:
    """Return the normalized path after joining the two or more paths.

    For example, path_resolve("a/b/c", "..\\d\\.\\e.txt", "../../f/g.jpg") == "a/b/f/g.jpg".
    """

    return os.path.normpath(os.path.join(base, *paths))


def date() -> str:
    """Return current date in the format of `%y%m%d`."""

    return time.strftime("%y%m%d", time.localtime())


def date_tuple() -> str:
    """Return current date in the format of zero-trimmed `(%Y, %#m, %#d)`."""

    return time.strftime("(%Y, %#m, %#d, 0)", time.localtime())


def sha256sum(file_path: str) -> str:
    """Return the SHA-256 checksum of input file.

    :return: empty string if the `path` is not an existing regular file.
    """

    if not os.path.isfile(file_path):
        return ""
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


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
