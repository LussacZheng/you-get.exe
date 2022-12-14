import glob
import os
import re
import sys

from scripts.artifact import ArtifactInfo
from scripts.utils import path_resolve

DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = path_resolve(DIR, "../../")

FILENAME = os.path.splitext(os.path.basename(__file__))[0]
INPUT = os.path.join(DIR, f"{FILENAME}.md.tmpl")
OUTPUT = os.path.join(DIR, f"{FILENAME}.md")

INJECT_LABEL_START = "{% for %}"
INJECT_LABEL_END = "{% endfor %}"


def main():
    location = os.path.join(ROOT, ".ci/**/*.json")

    artifact_infos = []
    for artifact_info_file in glob.glob(location):
        with open(artifact_info_file, "r", encoding="utf-8") as f:
            artifact_infos.append(ArtifactInfo.from_json_str(f.read()))

    if not artifact_infos:
        print(f"Unable to find any `artifact_info.json` in `{location}`!")
        sys.exit(1)

    with open(INPUT, "r", encoding="utf-8") as fin, open(OUTPUT, "w", encoding="utf-8") as fout:
        raw = fin.read()
        template = re.search(f"{INJECT_LABEL_START}\\s*(.*)\\s*{INJECT_LABEL_END}", raw).group(1)
        contents = []
        for artifact_info in artifact_infos:
            contents.append(artifact_info.inject(template))
        new = re.sub(f"{INJECT_LABEL_START}.*{INJECT_LABEL_END}", "\n".join(contents), raw, flags=re.S)
        fout.write(new)


if __name__ == "__main__":
    main()
