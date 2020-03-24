**| [English](README.md) | Simplified Chinese |**

# You-Get 非官方构建的可执行文件

![platform](https://img.shields.io/badge/platform-windows-brightgreen)
![GitHub release](https://img.shields.io/github/v/release/LussacZheng/you-get.exe?include_prereleases&label=build)
![GitHub All Releases](https://img.shields.io/github/downloads/LussacZheng/you-get.exe/total?color=yellowgreen)

使用 [PyInstaller](https://github.com/pyinstaller/pyinstaller) 打包 [You-Get](https://github.com/soimort/you-get) 为一个独立的可执行文件 (Windows)。

## 获取 "you-get.exe"

> 注意：这**不是**由官方构建发布的。

从 [Release 页面](https://github.com/LussacZheng/you-get.exe/releases) 下载最新发布的可执行文件即可。

## 反馈

在使用过程中遇到任何问题（请先确保为最新版），你可以 [提交 Issue](https://github.com/LussacZheng/you-get.exe/issues) 进行反馈。若没有 GitHub 账号，可以在 [这里](https://blog.lussac.net/archives/315/) 留言。

---

## 开发者指引

你可以参照下文自行构建、打包。

### 准备

依次安装以下依赖或运行相应命令。

1. [Python 3.7](https://www.python.org/downloads/windows/)  
   根据 PyInstaller 的[说明文档](https://github.com/pyinstaller/pyinstaller#requirements-and-tested-platforms)，其目前(2020-02-19)支持的 Python 版本为 3.5-3.7。若需创建32位的可执行文件，请在32位 Python 环境下运行 PyInstaller 。

2. PyInstaller

   ```shell
   # 可以加上使用镜像源的参数： --index-url=https://pypi.tuna.tsinghua.edu.cn/simple
   $ pip install pyinstaller
   ```

3. [Git](https://git-scm.com/) 

### 获取此项目

```shell
$ git clone https://github.com/LussacZheng/you-get.exe.git
```

### 第一次构建

项目中有若干批处理脚本，根据下文依次点击运行即可：

1. 运行 `devscripts/init.bat` 。  
   （即通过 `git clone` 来克隆 you-get 项目仓库。如果需要在 clone 时使用代理，请参照示例文件编辑 `devscripts/use-proxy.settings` 。）
2. 初始化完成后，运行 `build.bat` 。
3. 打包好的可执行文件在 `dist/` 文件夹下。

### You-Get 更新后的构建

在 You-Get 发布新版本后，按以下步骤重新打包：

1. 确保此项目脚本文件为最新：

   ```shell
   $ git pull
   ```

   *若 You-Get 修改了 [`src/you_get/extractors/__init__.py`](https://github.com/soimort/you-get/blob/develop/src/you_get/extractors/__init__.py) 而我尚未及时跟进并提交，你需要参照 [此处](https://github.com/LussacZheng/you-get.exe/blob/master/doc/PyInstaller-Options.md#%E7%89%B9%E6%AE%8A%E6%83%85%E5%86%B5) 手动修改 `repository/_extractors/__init__.py` 。*

2. 运行 `devscripts/update.bat` 。  
   （该脚本也会从 `devscripts/use-proxy.settings` 中读取代理设置）
3. 运行 `build.bat`.
4. 打包好的可执行文件在 `dist/` 文件夹下。

### 更多信息

查阅 [**doc**](https://github.com/LussacZheng/you-get.exe/tree/master/doc) 文件夹以了解更多信息。
