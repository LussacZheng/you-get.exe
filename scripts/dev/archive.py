#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile

_dir = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(_dir, "../.."))
OUTPUT = os.path.join(_dir, "you-get.exe.zip")

INCLUDE = [
    "build/file_version_info.tmpl",
    "build/you-get.ico",
    "repository/",
    "scripts/dev/build-and-log.bat",
    "build.py",
    "poetry.lock",
    "poetry.toml",
    "pyproject.toml",
    "README.md",
    "README_cn.md",
]
EXCLUDE = [".git", "__pycache__"]


def main():
    os.chdir(ROOT)

    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as z:
        for item in INCLUDE:
            if os.path.isfile(item):
                z.write(item)
            elif os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    # https://stackoverflow.com/a/19859907
                    dirs[:] = [d for d in dirs if d not in EXCLUDE]
                    for file in files:
                        z.write(os.path.join(root, file))

    print(f" * Zip file saved in: `{OUTPUT}`")


if __name__ == '__main__':
    main()
