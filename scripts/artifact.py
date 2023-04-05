import json
from abc import ABCMeta, abstractmethod
from string import Template

UNKNOWN = "unknown"


class Info(metaclass=ABCMeta):
    @abstractmethod
    def inject_into(self, template: str) -> str:
        raise NotImplementedError


class CoreInfo(Info):

    def __init__(self, main_py_version: str, poetry_version: str, pyinstaller_version: str):
        """
        :param main_py_version: Note that version string starting with `py` is also valid (e.g. `py3.8`).
        """
        self.main_py_version = main_py_version[2:] if main_py_version.startswith("py") else main_py_version
        self.poetry_version = poetry_version
        self.pyinstaller_version = pyinstaller_version

    def inject_into(self, template: str) -> str:
        """Format the template string with data from this CoreInfo instance."""
        return Template(template).safe_substitute(
            poetry_version=self.poetry_version,
            pyinstaller_version=self.pyinstaller_version,
        )


class ArtifactInfo(Info):

    def __init__(self, filename: str, sha256: str, py_version: str, py_arch: str, poetry_version: str,
                 pyinstaller_version: str):
        self.filename = filename
        self.sha256 = sha256

        self.py_version = py_version

        self.py_arch = py_arch
        self.poetry_version = poetry_version
        self.pyinstaller_version = pyinstaller_version

    def __repr__(self):
        return self.json()

    @classmethod
    def from_json_str(cls, info: str):
        """Construct an instance from JSON string."""
        data = json.loads(info)
        return cls(
            filename=data.get("filename", UNKNOWN),
            sha256=data.get("sha256", UNKNOWN),
            py_version=data.get("py_version", UNKNOWN),
            py_arch=data.get("py_arch", UNKNOWN),
            poetry_version=data.get("poetry_version", UNKNOWN),
            pyinstaller_version=data.get("pyinstaller_version", UNKNOWN),
        )

    def json(self) -> str:
        """Return the JSON representation of this ArtifactInfo."""
        return json.dumps(self.__dict__)

    def inject_into(self, template: str) -> str:
        """Format the template string with data from this ArtifactInfo instance."""
        return Template(template).safe_substitute(
            filename=self.filename,
            sha256=self.sha256,
            py_version=self.py_version,
        )
