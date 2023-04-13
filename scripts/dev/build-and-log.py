#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.abspath(__file__), "../../../"))


def main():
    sys.path.append(ROOT)
    from build import DIST, DIST_FILENAME

    if shutil.which("poetry") is None:
        print(" * You should install `poetry` first.")
        return

    os.chdir(ROOT)

    if not os.path.exists(DIST):
        os.mkdir(DIST)

    print(" * Building `you-get.exe` ...")

    # Set the filename of the log file to the same as the zip file
    log = os.path.join(DIST, os.path.splitext(DIST_FILENAME)[0] + ".log")
    with open(log, "w", encoding="utf-8") as f:
        # "python -u": force the stdout and stderr streams to be unbuffered
        # "build.py --force": force delete the outputs of last build
        subprocess.call(["poetry", "run", "python", "-u", "build.py", "--force"], stdout=f, stderr=subprocess.STDOUT)

    print(" * All completed.")
    print(f" * Build logs saved in: `{log}`")


if __name__ == '__main__':
    main()
