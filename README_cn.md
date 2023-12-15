**| [English](README.md) | Simplified Chinese |**

# You-Get 非官方构建的可执行文件

![platform](https://img.shields.io/badge/platform-Windows-brightgreen?logo=windows)
![GitHub release](https://img.shields.io/github/v/release/LussacZheng/you-get.exe?include_prereleases&label=build)
[![GitHub All Releases](https://img.shields.io/github/downloads/LussacZheng/you-get.exe/total?color=green&logo=github)](https://github.com/LussacZheng/you-get.exe/releases)

使用 [PyInstaller](https://github.com/pyinstaller/pyinstaller) 打包 [You-Get](https://github.com/soimort/you-get) 为一个独立的可执行文件 (Windows)。

## 获取 "you-get.exe"

> 注意：这**不是**由官方构建发布的。

从 [Releases 页面](https://github.com/LussacZheng/you-get.exe/releases) 下载最新发布的可执行文件即可。

## 反馈

在使用过程中遇到任何问题（请先确保为最新版），你可以通过 [创建 Discussion](https://github.com/LussacZheng/you-get.exe/discussions) 或 [提交 Issue](https://github.com/LussacZheng/you-get.exe/issues) 进行反馈。
反馈时最好能附带上 debug 信息，你可以通过添加 `--debug` 参数来获得详细的错误报告：

```shell
you-get --debug https://your.video/url/here
```

对于 SSL 相关的问题，请尝试使用 `-k, --insecure` 参数：

```shell
you-get -k --debug https://your.video/url/here
```

---

## 开发者指引

你可以参照下文自行构建、打包。

### 准备

依次安装以下依赖或运行相应命令。

- [Python 3.8-3.12](https://www.python.org/downloads/windows/)  
   在 PyInstaller 的[说明文档](https://github.com/pyinstaller/pyinstaller#requirements-and-tested-platforms)中可以找到其支持的 Python 版本号。
   若需创建32位的可执行文件，请在32位 Python 环境下运行 PyInstaller 。

- [Poetry](https://python-poetry.org/docs/#installation)

   ```shell
   # 安装时可能需要使用代理
   # set HTTP_PROXY=http://127.0.0.1:7890 & set HTTPS_PROXY=http://127.0.0.1:7890
   wget https://install.python-poetry.org -O install-poetry.py
   python3 install-poetry.py
   ```

- [Git](https://git-scm.com/)

### 第一次构建

```shell
# 获取此项目
git clone --recurse-submodules https://github.com/LussacZheng/you-get.exe.git

# 创建虚拟环境并安装依赖
poetry install --no-root

在虚拟环境中运行 `build.py`
poetry run python build.py
```

打包好的可执行文件为 `dist/` 文件夹下。

### You-Get 更新后的构建

在 You-Get 发布新版本后，按以下步骤重新打包：

```shell
# 确保此项目文件为最新
git pull

# 更新 `you-get` 项目仓库
git submodule update --remote

# 更新依赖
poetry update

# 重新在虚拟环境中运行 `build.py`
poetry run python build.py
```

打包好的可执行文件在 `dist/` 文件夹下。

---

## TODO

- [x] 引入 [Poetry](https://github.com/python-poetry/poetry) 用于依赖管理。
- [x] 用 Python 重写构建脚本。
- [x] 使用 GitHub Actions 进行构建和发布。
- [x] 将 `you-get` 作为 git submodule 管理。
- [x] 构建时自动向 `src/you_get/extractors/__init__.py` 追加缺失的 extractors。
- [ ] 支持 Linux 和 macOS。

## License

[You-Get](https://github.com/soimort/you-get) is originally distributed under the [MIT license](https://github.com/soimort/you-get/blob/develop/LICENSE.txt).
