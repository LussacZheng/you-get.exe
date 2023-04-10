#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import glob
import os
import shutil
import sys

from scripts import utils, ROOT
from scripts.artifact import ArtifactInfo
from scripts.echo import EchoStyle
from scripts.versions import py_version, py_arch, you_get_version, you_get_version_tuple, poetry_version

# region ########## Config ##########

DIST = os.path.join(ROOT, "dist")
STATIC = os.path.join(ROOT, "build")
TEMP = os.path.join(ROOT, ".temp")
ENTRY_POINT = "repository/you-get/you-get"
DIST_FILENAME = f"you-get_{you_get_version()}_win{py_arch()}_py{py_version()}_UB{utils.date()}.zip"

CONFIG = {
    "dist": {
        "name": "you-get.exe",
        "path": os.path.join(DIST, "you-get.exe"),
    },
    "build": {
        "products": os.path.join(TEMP, "you-get"),
        "version_info_tmpl": os.path.join(STATIC, "file_version_info.tmpl"),
        "version_info": os.path.join(TEMP, "file_version_info.txt"),
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
    "ci": {
        "artifact_info": os.path.join(DIST, "artifact_info.json"),
    },
}

FLAGS = {
    # force delete the outputs of last build
    "force": False,
    "skip_build": False,
    "ci": False,
}


# endregion


# region ########## Steps ##########


def init():
    """Step 0: Init"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", help="force the whole process, do not ask anything")
    parser.add_argument("-s", "--skip-build", action="store_true", help="skip the main building process")
    parser.add_argument("--ci", action="store_true", help="CI-specific argument")

    global FLAGS
    FLAGS = parser.parse_args().__dict__

    if FLAGS["ci"]:
        FLAGS["force"] = True


def check():
    """Step 1: Check"""

    if not os.path.isfile(utils.path_resolve(ROOT, ENTRY_POINT)):
        EchoStyle.Warn.echo("Please run `scripts/dev/prepare.py` to clone the repository `you-get`.")
        sys.exit(1)


def clean():
    """Step 2: Clean"""

    def rm(file_path: str, force_delete: bool = True):
        if not force_delete:
            choose = input(f' ! "{file_path}".\n ! Is it OK to delete this file (Y/N)? ').upper()
            if choose != "Y":
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
            rm(archive, FLAGS["force"])

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
                version_tuple=you_get_version_tuple(),
                date_tuple=utils.date_tuple(),
                version=you_get_version(),
                date=utils.date(),
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

        import PyInstaller.__main__

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
            '--onefile',
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
        shutil.copy(utils.path_resolve(ROOT, src), os.path.join(DIST, dst))
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


def ci(sha256: str):
    """Step 88: CI-specific step

    1. generate `artifact_info.json`
    2. ...
    """

    if not FLAGS["ci"]:
        return

    import PyInstaller

    with open(CONFIG["ci"]["artifact_info"], "w", encoding="utf-8") as f:
        f.write(ArtifactInfo(
            filename=DIST_FILENAME,
            sha256=sha256,
            py_version=py_version(),
            py_arch=py_arch(),
            poetry_version=poetry_version(),
            pyinstaller_version=PyInstaller.__version__,
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
    ci(sha256)
    finish()
    return


if __name__ == "__main__":
    main()
