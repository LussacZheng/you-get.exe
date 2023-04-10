"""Generate release notes"""

import os
import re

from scripts.artifact import ArtifactInfo, CoreInfo

INPUT = os.path.splitext(__file__)[0] + ".md.tmpl"
OUTPUT = os.path.splitext(__file__)[0] + ".md"

INJECT_LABEL_MAIN = "{% main %}"
INJECT_LABEL_ARTIFACT = "{% artifact %}"


def load_artifacts(raw: str, artifacts: list[ArtifactInfo], inject_label: str) -> str:
    template = re.search(f"{inject_label}\\s*(.*)\\s*{inject_label}", raw).group(1)
    contents = []
    for artifact in artifacts:
        contents.append(artifact.inject_into(template))
    return re.sub(f"{inject_label}.*{inject_label}", "\n".join(contents), raw, flags=re.S)


def generate_release_notes(core: CoreInfo, artifacts: list[ArtifactInfo], main_artifacts: list[ArtifactInfo]):
    with open(INPUT, "r", encoding="utf-8") as fin, open(OUTPUT, "w", encoding="utf-8") as fout:
        content = load_artifacts(fin.read(), main_artifacts, INJECT_LABEL_MAIN)
        content = load_artifacts(content, artifacts, INJECT_LABEL_ARTIFACT)
        fout.write(core.inject_into(content))
    print(f"The release note has been generated at `{OUTPUT}`.")
