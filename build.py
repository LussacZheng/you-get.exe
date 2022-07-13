#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import hashlib
import os.path
import platform
import re
import shutil
import sys
import time
import zipfile
from enum import Enum, unique

import PyInstaller.__main__

ROOT = os.path.split(os.path.realpath(__file__))[0]


# region ########## Util Functions ##########


def join_and_norm(base: str, *paths: str) -> str:
    """Return the normalized path after joining the two paths.

    For example, join_and_norm("a/b/c", "..\\d\\.\\e.txt", "../../f/g.jpg" == "a/b/f/g.jpg".
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


# Don't use this variable directly, use `version()` instead.
__ver = "0.0.0"
# In order to avoid redundant file IO
__ver_found = False


def version() -> str:
    """Return the version string of 'you-get'. (Defined in `src/you_get/version.py`)"""

    global __ver, __ver_found
    if not __ver_found:
        # Whether the version number is actually found, set to it True
        __ver_found = True
        # Try to get version string from `src/you_get/version.py`
        version_file = join_and_norm(ROOT, "repository/you-get/src/you_get/version.py")
        if os.path.isfile(version_file):
            with open(version_file, "r", encoding="utf-8") as f:
                res = re.search(r"version.*'([\d.]+)'", f.read())
                if res is not None:
                    __ver = res.group(1)

    return __ver


def version_tuple() -> tuple:
    """Return the version tuple of 'you-get'."""

    v = [int(x) for x in version().split(".")]
    while len(v) < 4:
        v.append(0)
    return tuple(v)


def date() -> str:
    """Return current date in the format of `%y%m%d`."""

    return time.strftime("%y%m%d", time.localtime())


def date_tuple() -> str:
    """Return current date in the format of zero-trimmed `(%Y, %#m, %#d)`."""

    return time.strftime("(%Y, %#m, %#d, 0)", time.localtime())


def py_arch() -> str:
    """Get the architecture of the python interpreter ("32" or "64")

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


@unique
class EchoStyle(Enum):
    HrEqual = -1  # horizontal rule (equal)
    HrDash = -2  # horizontal rule (dash)
    Title = 1  # title of a step
    Running = 2  # running a sub-step
    Complete = 3  # completed a step
    Finish = 4  # finish of all the steps
    Warn = 10  # error message

    def echo(self, content: str = ""):
        def line_of(char):
            print(f'\n{char * 60}\n')

        if self is EchoStyle.HrEqual:
            line_of("=")
        elif self is EchoStyle.HrDash:
            line_of("-")
        elif self is EchoStyle.Title:
            EchoStyle.HrEqual.echo()
            print(f' * {content}...')
            EchoStyle.HrDash.echo()
        elif self is EchoStyle.Running:
            print(f' - {content}')
        elif self is EchoStyle.Complete:
            print(f'\n * {content} completed.')
        elif self is EchoStyle.Finish:
            EchoStyle.HrEqual.echo()
            print(f' * {content}')
            EchoStyle.HrEqual.echo()
        elif self is EchoStyle.Warn:
            print(f' ! {content}')


# endregion


# region ########## Config ##########

DIST = os.path.join(ROOT, "dist")
BUILD = os.path.join(ROOT, "build")
ENTRY_POINT = "repository/you-get/you-get"

CONFIG = {
    "dist": {
        "name": "you-get.exe",
        "path": os.path.join(DIST, "you-get.exe"),
    },
    "build": {
        "products": os.path.join(BUILD, "you-get"),
        "version_info_tmpl": os.path.join(BUILD, "file_version_info.tmpl"),
        "version_info": os.path.join(BUILD, "file_version_info.txt"),
    },
    "copy": [
        ("repository/you-get/LICENSE.txt", "LICENSE.txt"),
        ("README.md", "README.md"),
        ("README_cn.md", "README_cn.md"),
    ],
    "sha256sum": os.path.join(DIST, "sha256sum.txt"),
    "crlf2lf": ["LICENSE.txt", "README.md", "README_cn.md", "sha256sum.txt"],
    "zip": {
        "path": os.path.join(DIST, f"you-get_{version()}_win{py_arch()}_UB{date()}.zip"),
        "list": ["you-get.exe", "LICENSE.txt", "README.md", "README_cn.md", "sha256sum.txt"],
        "comment": os.path.join(DIST, "LICENSE.txt"),
    },
}

FLAGS = {
    "force_delete": False,
    "skip_build": False,
    # "something": False,
}


# endregion


# region ########## Steps ##########


def init():
    """Step 0: Init"""

    for arg in sys.argv[1:]:
        if arg == "-f":
            FLAGS["force_delete"] = True
        if arg == "--skip-build":
            FLAGS["skip_build"] = True
        if arg == "--ci":
            FLAGS["force_delete"] = True
            # FLAGS["something"] = True


def check():
    """Step 1: Check"""

    if not os.path.isfile(join_and_norm(ROOT, ENTRY_POINT)):
        EchoStyle.Warn.echo('Please run "devscripts\\init.bat" first or clone the repository of "you-get".')
        sys.exit(1)


def clean():
    """Step 2: Clean"""

    def rm(file_path: str, force_delete: bool = True):
        if not force_delete:
            choose = input(f' ! "{file_path}".\n ! Is it OK to delete this file (Y/N)? ')
            if choose != "Y" and choose != "y":
                EchoStyle.Finish.echo("Clean stopped.")
                sys.exit(0)
        os.remove(file_path)
        EchoStyle.Running.echo(f'Deleted "{file_path}"')

    EchoStyle.Title.echo("Clean before building")

    # Clean last build products
    build_dir = CONFIG["build"]["products"]
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    # Clean last dist
    if os.path.exists(DIST):
        for f in CONFIG["zip"]["list"]:
            file = os.path.join(DIST, f)
            if os.path.isfile(file):
                if not (FLAGS["skip_build"] and f == "you-get.exe"):
                    rm(file)
        archive = CONFIG["zip"]["path"]
        if os.path.isfile(archive):
            rm(archive, FLAGS["force_delete"])

    EchoStyle.Complete.echo("Clean")


def build():
    """Step 3: Build"""

    # Skip build if the corresponding arg was passed in
    if FLAGS["skip_build"]:
        EchoStyle.Title.echo("Skip building")
        EchoStyle.Warn.echo("Build Skipped.")
        return

    # Prepare `file_version_info.txt`
    src = CONFIG["build"]["version_info_tmpl"]
    dst = CONFIG["build"]["version_info"]
    if os.path.isfile(src):
        with open(src, "r", encoding="utf-8") as f:
            template = f.read()
        with open(dst, "w", encoding="utf-8") as f:
            f.write(template.format(
                version_tuple=version_tuple(),
                date_tuple=date_tuple(),
                version=version(),
                date=date(),
                py_arch="64" if py_arch() == "64" else "86",
            ))

    EchoStyle.Title.echo('pyinstaller "you-get"')

    # Run this script from the `ROOT` directory
    previous_dir = os.getcwd()
    os.chdir(ROOT)

    try:
        # First, move out the original `__init__.py` from "you_get.extractors",
        #     in order that we can recover everything after build.
        # Then copy a new `__init__.py`, which has imported the missing extractors,
        #     into the module "you_get.extractors".
        shutil.move("repository/you-get/src/you_get/extractors/__init__.py", "repository/")
        for file in glob.glob("repository/_extractors/*.py"):
            shutil.copy(file, "repository/you-get/src/you_get/extractors/")

        # PyInstaller bundle command
        PyInstaller.__main__.run([
            ENTRY_POINT,
            '--path=repository/you-get/src',
            '--workpath=build',
            '--specpath=build',
            '--distpath=dist',
            '--hidden-import=you_get.extractors',
            '--hidden-import=you_get.cli_wrapper',
            '--hidden-import=you_get.processor',
            '--hidden-import=you_get.util',
            '-F',
            '--noupx',
            '--icon=you-get.ico',
            '--version-file=file_version_info.txt'
        ])
    finally:
        # Recover everything in "you-get.git" after built, whether this step was successful or not
        for file in glob.glob("repository/_extractors/*.py"):
            os.remove("repository/you-get/src/you_get/extractors/" + os.path.basename(file))
        shutil.move("repository/__init__.py", "repository/you-get/src/you_get/extractors/")
        os.chdir(previous_dir)

    EchoStyle.HrDash.echo()
    EchoStyle.Running.echo(f'Build logs saved in:       "{CONFIG["build"]["products"]}"')
    EchoStyle.Running.echo(f'Build executable saved to: "{CONFIG["dist"]["path"]}"')
    EchoStyle.Complete.echo("Build")


def copy():
    """Step 4: Copy"""

    EchoStyle.Title.echo("Copy the required files")
    for src, dst in CONFIG["copy"]:
        EchoStyle.Running.echo(f'Copying "{src}" to "{dst}"...')
        shutil.copy(join_and_norm(ROOT, src), os.path.join(DIST, dst))
    EchoStyle.Running.echo(f'All the required files are now in: "{DIST}"')
    EchoStyle.Complete.echo("Copy")


def checksum():
    """Step 5: Checksum"""

    EchoStyle.Title.echo('SHA256 Checksum of "you-get.exe"')
    hash_value = sha256sum(CONFIG["dist"]["path"])
    output = CONFIG["sha256sum"]
    with open(output, "w", encoding="utf-8") as f:
        f.write(f'{hash_value} *{CONFIG["dist"]["name"]}')

    EchoStyle.Running.echo(f'SHA256 Checksum: {hash_value}')
    # EchoStyle.Running.echo("SHA256 Checksum has been copied into your clipboard.")
    EchoStyle.Running.echo(f'Checksum file saved to: "{output}"')
    EchoStyle.Complete.echo("Checksum")


def convert_line_endings():
    """Step 6: CRLF to LF"""

    EchoStyle.Title.echo("Convert line endings to LF")
    for file in CONFIG["crlf2lf"]:
        EchoStyle.Running.echo(f'Converting "{file}"...')
        crlf_to_lf(os.path.join(DIST, file))
    EchoStyle.Complete.echo("Convert")


def package():
    """Step 7: Zip all the required files"""

    EchoStyle.Title.echo('Generate "you-get.zip"')
    output = CONFIG["zip"]["path"]
    compress_files(output, DIST, CONFIG["zip"]["list"], CONFIG["zip"]["comment"])
    EchoStyle.Running.echo(f'Zip archive file saved to:\n   "{output}"')
    EchoStyle.Complete.echo("Zip")


def finish():
    """Step 99: Finish"""

    EchoStyle.Finish.echo("All completed.")


# endregion


def main():
    init()
    check()
    clean()
    build()
    copy()
    checksum()
    convert_line_endings()
    package()
    finish()
    return


if __name__ == "__main__":
    main()
