**| English | [简体中文](README_cn.md) |**

# You-Get Unofficial Build Executable

![platform](https://img.shields.io/badge/platform-Windows-brightgreen?logo=windows)
![GitHub release](https://img.shields.io/github/v/release/LussacZheng/you-get.exe?include_prereleases&label=build)
[![GitHub All Releases](https://img.shields.io/github/downloads/LussacZheng/you-get.exe/total?color=green&logo=github)](https://github.com/LussacZheng/you-get.exe/releases)

Use [PyInstaller](https://github.com/pyinstaller/pyinstaller) to bundle [You-Get](https://github.com/soimort/you-get) into a single executable for Windows.

## Get "you-get.exe"

> Notice: This is **NOT** the official build.

Download the latest build executable from [Releases Page](https://github.com/LussacZheng/you-get.exe/releases).

## Bugs

If something goes wrong when using the latest released executable, feel free to [start a new discussion](https://github.com/LussacZheng/you-get.exe/discussions) or [submit an issue](https://github.com/LussacZheng/you-get.exe/issues). If you don't have a GitHub account, leave a message in [this page](https://blog.lussac.net/archives/315/). You'd better attach the debug info. Get the detailed error report by adding the `--debug` option:

```shell
you-get --debug https://your.video/url/here
```

For SSL related issues, try to use `-k` option:

```shell
you-get -k --debug https://your.video/url/here
```

---

## Developer Instructions

See below if you want to bundle and build by yourself.

### Preparation

The following dependencies are required and must be installed separately.

- [Python 3.7-3.11](https://www.python.org/downloads/windows/)  
   You can find the supported Python versions in the [README](https://github.com/pyinstaller/pyinstaller#requirements-and-tested-platforms) of PyInstaller.
   To create a 32-bit executable, run PyInstaller under a 32-bit Python.

- [Poetry](https://python-poetry.org/docs/#installation)

- [Git](https://git-scm.com/)

### Build for the first time

```shell
# clone this repository
git clone --recurse-submodules https://github.com/LussacZheng/you-get.exe.git

# create virtualenv and install dependencies
poetry install

# run `build.py` under virtualenv
poetry run python build.py
```

Find the executable in `dist/` directory.

### Build again if You-Get upgraded

To re-build after the new release of You-Get:

```shell
# make sure the build script is up to date
git pull

# update the repository of `you-get`
git submodule foreach git pull

# update dependencies
poetry update

# re-run `build.py` under virtualenv
poetry run python build.py
```

Find the executable in `dist/` directory.

### More Information

If You-Get modified the
[`src/you_get/extractors/__init__.py`](https://github.com/soimort/you-get/blob/develop/src/you_get/extractors/__init__.py)
and I have not followed up and submitted in time,
you need to manually edit `repository/_extractors/__init__.py` according to
[this](https://github.com/LussacZheng/you-get.exe/blob/master/doc/PyInstaller-Options.md#%E7%89%B9%E6%AE%8A%E6%83%85%E5%86%B5).

See more information in [**doc**](https://github.com/LussacZheng/you-get.exe/tree/master/doc) folder.

---

## TODO

- [x] Introduce [Poetry](https://github.com/python-poetry/poetry) for dependency management.
- [x] Rewrite `build.bat` with Python.
- [x] Use GitHub Action to build and release.

## License

[You-Get](https://github.com/soimort/you-get) is originally distributed under the [MIT license](https://github.com/soimort/you-get/blob/develop/LICENSE.txt).
