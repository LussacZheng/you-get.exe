#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import re
import shutil
import sys
from enum import Enum, unique

import PyInstaller.__main__

from scripts import utils
from scripts.artifact import ArtifactInfo
from scripts.utils import path_resolve, py_arch, py_version, date, date_tuple

ROOT = os.path.dirname(os.path.realpath(__file__))

# region ########## Util Functions ##########


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
        version_file = path_resolve(ROOT, "repository/you-get/src/you_get/version.py")
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
STATIC = os.path.join(ROOT, "build")
TEMP = os.path.join(ROOT, ".temp")
ENTRY_POINT = "repository/you-get/you-get"
DIST_FILENAME = f"you-get_{version()}_win{py_arch()}_py{py_version()}_UB{date()}.zip"

CONFIG = {
    "dist": {
        "name": "you-get.exe",
        "path": os.path.join(DIST, "you-get.exe"),
    },
    "build": {
        "products": os.path.join(TEMP, "you-get"),
        "version_info_tmpl": os.path.join(STATIC, "file_version_info.tmpl"),
        "version_info": os.path.join(TEMP, "file_version_info.txt"),
        "artifact_info": os.path.join(TEMP, "artifact_info.json"),
    },
    "copy": [
        ("repository/you-get/LICENSE.txt", "LICENSE.txt"),
        ("README.md", "README.md"),
        ("README_cn.md", "README_cn.md"),
    ],
    "sha256sum": os.path.join(DIST, "sha256sum.txt"),
    "crlf2lf": ["LICENSE.txt", "README.md", "README_cn.md", "sha256sum.txt"],
    "zip": {
        "path": os.path.join(DIST, DIST_FILENAME),
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

    if not os.path.isfile(path_resolve(ROOT, ENTRY_POINT)):
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
    if os.path.exists(TEMP):
        shutil.rmtree(TEMP)

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

    # create temp directory if necessary
    if not os.path.exists(TEMP):
        os.mkdir(TEMP)

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
                py_version=py_version(),
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
            '--workpath=.temp',
            '--specpath=.temp',
            '--distpath=dist',
            '--hidden-import=you_get.extractors',
            '--hidden-import=you_get.cli_wrapper',
            '--hidden-import=you_get.processor',
            '--hidden-import=you_get.util',
            '-F',
            '--noupx',
            '--icon=../build/you-get.ico',
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
        shutil.copy(path_resolve(ROOT, src), os.path.join(DIST, dst))
    EchoStyle.Running.echo(f'All the required files are now in: "{DIST}"')
    EchoStyle.Complete.echo("Copy")


def checksum() -> str:
    """Step 5: Checksum"""

    EchoStyle.Title.echo('SHA256 Checksum of "you-get.exe"')
    hash_value = utils.sha256sum(CONFIG["dist"]["path"])
    output = CONFIG["sha256sum"]
    with open(output, "w", encoding="utf-8") as f:
        f.write(f'{hash_value} *{CONFIG["dist"]["name"]}')

    EchoStyle.Running.echo(f'SHA256 Checksum: {hash_value}')
    # EchoStyle.Running.echo("SHA256 Checksum has been copied into your clipboard.")
    EchoStyle.Running.echo(f'Checksum file saved to: "{output}"')
    EchoStyle.Complete.echo("Checksum")

    return hash_value


def convert_line_endings():
    """Step 6: CRLF to LF"""

    EchoStyle.Title.echo("Convert line endings to LF")
    for file in CONFIG["crlf2lf"]:
        EchoStyle.Running.echo(f'Converting "{file}"...')
        utils.crlf_to_lf(os.path.join(DIST, file))
    EchoStyle.Complete.echo("Convert")


def package():
    """Step 7: Zip all the required files"""

    EchoStyle.Title.echo('Generate "you-get.zip"')
    output = CONFIG["zip"]["path"]
    utils.compress_files(output, DIST, CONFIG["zip"]["list"], CONFIG["zip"]["comment"])
    EchoStyle.Running.echo(f'Zip archive file saved to:\n   "{output}"')
    EchoStyle.Complete.echo("Zip")


def generate_artifact_info(sha256: str):
    with open(CONFIG["build"]["artifact_info"], "w", encoding="utf-8") as f:
        f.write(ArtifactInfo(
            filename=DIST_FILENAME,
            py_version=py_version(),
            py_arch=py_arch(),
            poetry_version=utils.poetry_version(),
            pyinstaller_version=PyInstaller.__version__,
            sha256=sha256
        ).json())


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
    sha256 = checksum()
    convert_line_endings()
    package()
    generate_artifact_info(sha256)
    finish()
    return


if __name__ == "__main__":
    main()
