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

If something goes wrong when using the latest released executable, feel free to [submit an issue](https://github.com/LussacZheng/you-get.exe/issues). If you don't have a GitHub account, leave a message in [this page](https://blog.lussac.net/archives/315/). You'd better attach the debug info. Get the detailed error report by adding the `--debug` option:

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

1. [Python 3.7 or 3.8](https://www.python.org/downloads/windows/)  
   According to the [README](https://github.com/pyinstaller/pyinstaller#requirements-and-tested-platforms) of PyInstaller, the supported Python version is 3.5-3.8 now (July 10th, 2020). To create a 32-bit executable, run PyInstaller under a 32-bit Python.

2. PyInstaller

   ```shell
   $ pip install pyinstaller
   ```

3. [Git](https://git-scm.com/) 

### Get this repository

```shell
$ git clone https://github.com/LussacZheng/you-get.exe.git
```

### Build for the first time

There are several batchfiles, just click them by the following order:

1. Run `devscripts/init.bat` .  
   (It will clone the you-get repository by `git clone` . If you want to use proxy when cloning, edit `devscripts/use-proxy.settings` according to the sample.)
2. After initialization, run `build.bat` .
3. Find the executable in `dist/` folder.

### Build again if You-Get upgraded

To re-build after the new release of You-Get:

1. Make sure the scripts of this repository is up to date:

   ```shell
   $ git pull
   ```

   *If You-Get modified the [`src/you_get/extractors/__init__.py`](https://github.com/soimort/you-get/blob/develop/src/you_get/extractors/__init__.py) and I have not followed up and submitted in time, you need to manually edit `repository/_extractors/__init__.py` according to [this](https://github.com/LussacZheng/you-get.exe/blob/master/doc/PyInstaller-Options.md#%E7%89%B9%E6%AE%8A%E6%83%85%E5%86%B5) .*

2. Run `devscripts/update.bat` .  
   (It also reads the proxy settings from `devscripts/use-proxy.settings` )
3. Run `build.bat`.
4. Find the executable in `dist/` folder.

### More Information

See more information in [**doc**](https://github.com/LussacZheng/you-get.exe/tree/master/doc) folder.

---

## License

[You-Get](https://github.com/soimort/you-get)  is originally distributed under the [MIT license](https://github.com/soimort/you-get/blob/develop/LICENSE.txt).
