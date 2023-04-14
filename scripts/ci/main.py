"""Prepare for release"""

import argparse
import copy
import glob
import os
import re
import shutil
import sys

from scripts import ROOT
from scripts.artifact import ArtifactInfo, CoreInfo
from scripts.ci.release_notes import generate_release_notes
from scripts.versions import pyinstaller_version, py_version_strings_match


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--poetry", required=True, help="set the version of Poetry to use", metavar="VERSION")
    parser.add_argument("--main", required=True, help="select a Python version for the main release",
                        metavar="PY_VERSION")
    return parser.parse_args()


def get_core_info() -> CoreInfo:
    arg = cli()

    if not re.match(r"^(py)?\d\.\d+(\.\d+)?$", arg.main):
        print(f"Please select a valid Python version, not `{arg.main}`!")
        sys.exit(1)

    return CoreInfo(arg.main, arg.poetry, pyinstaller_version())


def get_artifact_infos() -> list[ArtifactInfo]:
    location = os.path.join(ROOT, ".ci/**/*.json")

    artifact_infos = []
    for artifact_info_file in glob.glob(location):
        with open(artifact_info_file, "r", encoding="utf-8") as f:
            artifact_infos.append(ArtifactInfo.from_json_str(f.read()))

    if not artifact_infos:
        print(f"Unable to find any `{ArtifactInfo.DUMP_FILENAME}` in `{location}`!")
        sys.exit(1)

    # sort artifact_infos by `py_version.minor`, then `py_arch`
    artifact_infos.sort(key=lambda x: (int(x.py_version.split(".")[1]), x.py_arch))

    return artifact_infos


def select_main_artifacts(artifact_infos: list[ArtifactInfo], main_py_version: str) -> list[ArtifactInfo]:
    targets = []
    for artifact_info in artifact_infos:
        if py_version_strings_match(main_py_version, artifact_info.py_version):
            targets.append(copy.deepcopy(artifact_info))

    if not targets:
        print(f"Unable to find any artifacts matching the Python version `{main_py_version}`!")
        sys.exit(1)
    else:
        print(f"Setting the Python version to `{targets[0].py_version}` for the main release.")

    for target in targets:
        for archive in glob.glob(os.path.join(ROOT, f".ci/**/{target.filename}")):
            dirname, filename = os.path.split(archive)
            # Convert the filename of a normal artifact into the format of the main artifact.
            # e.g. 'you-get_0.4.1650_win64_py3.11.0_UB221214.zip' --> 'you-get_0.4.1650_win64_UB221214.zip'
            target.filename = re.sub(r"_py[\d.]+_", "_", filename)
            shutil.copy2(archive, os.path.join(dirname, target.filename))

    return targets


def main():
    core = get_core_info()
    artifacts = get_artifact_infos()
    main_artifacts = select_main_artifacts(artifacts, core.main_py_version)

    generate_release_notes(core, artifacts, main_artifacts)


if __name__ == "__main__":
    main()
