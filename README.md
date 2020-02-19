**| English | [简体中文](README_cn.md) |**

# You-Get Unofficial Build Executable

![platform](https://img.shields.io/badge/platform-windows-brightgreen)
![build](https://img.shields.io/badge/build-200219-blue)

Use [PyInstaller](https://github.com/pyinstaller/pyinstaller) to bundle [You-Get](https://github.com/soimort/you-get) into a single executable for Windows.

## Get you-get.exe

> Notice: This is **NOT** official build.

Download the latest build executable from [Release](https://github.com/LussacZheng/you-get.exe/releases).

## Bugs

If something went wrong when using the latest released  executable, feel free to [submit an issue](https://github.com/LussacZheng/you-get.exe/issues). If you don't have a GitHub account, leave a message in [this page](https://blog.lussac.net/archives/315/).

---

## Developer Instructions

See below if you want to bundle by yourself.

### Preparation

The following dependencies are required and must be installed separately.

1. [Python 3.7](https://www.python.org/downloads/windows/)  
   Accoprding to the README of PyInstaller, the supported Python version is 3.5-3.7 now (Feb. 19th, 2020). To create a 32-bit executable, run PyInstaller under a 32-bit Python.

2. PyInstaller  
   ```shell
   $ pip install pyinstaller
   ```

3. [Git](https://git-scm.com/) 

### Get this repository

```shell
$ git clone https://github.com/LussacZheng/you-get.exe.git
```

### Build for first time

There are several batchfiles, just click them by the following order:

1. Run `devscripts/init.bat` .  
   (It will clone the you-get repository by `git clone` . If you want to use proxy when cloning, edit `devscripts/use-proxy.settings` according to the sample.)
2. After initialization, run `build.bat` .
3. Find the executable in `dist/` folder.
   
### Build again if You-Get upgraded

To re-build after the new release of You-Get:

1. Run `devscripts/update.bat` .  
   (It also reads the proxy settings from `devscripts/use-proxy.settings` )
2. Run `build.bat`.
3. Find the executable in `dist/` folder.

### More Information

See more information in [**doc**](https://github.com/LussacZheng/you-get.exe/tree/master/doc) folder.
