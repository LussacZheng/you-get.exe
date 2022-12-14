import json

UNKNOWN = "unknown"


class ArtifactInfo:

    def __init__(self, filename: str, py_version: str, py_arch: str, poetry_version: str, pyinstaller_version: str,
                 sha256: str):
        self.filename = filename
        self.py_version = py_version
        self.py_arch = py_arch
        self.poetry_version = poetry_version
        self.pyinstaller_version = pyinstaller_version
        self.sha256 = sha256

    @classmethod
    def from_json_str(cls, info: str):
        """Construct an instance from JSON string."""
        data = json.loads(info)
        return cls(
            filename=data.get("filename", UNKNOWN),
            py_version=data.get("py_version", UNKNOWN),
            py_arch=data.get("py_arch", UNKNOWN),
            poetry_version=data.get("poetry_version", UNKNOWN),
            pyinstaller_version=data.get("pyinstaller_version", UNKNOWN),
            sha256=data.get("sha256", UNKNOWN)
        )

    def json(self) -> str:
        """Return the JSON representation of this ArtifactInfo."""
        return json.dumps(self.__dict__)

    def inject(self, template: str) -> str:
        """Format the template string with data from this ArtifactInfo instance."""
        return template.format(
            filename=self.filename,
            py_version=self.py_version,
            py_arch="64" if self.py_arch == "64" else "86",
            poetry_version=self.poetry_version,
            pyinstaller_version=self.pyinstaller_version,
            sha256=self.sha256
        )
