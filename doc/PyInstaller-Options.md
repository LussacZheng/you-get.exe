# 使用 PyInstaller 打包 You-Get

> [PyInstaller](https://github.com/pyinstaller/pyinstaller) bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules.

本文将叙述如何使用 PyInstaller 将 you-get 打包为可独立运行的 exe 程序 (Windows)。

---

## Preparation

依次安装以下依赖或运行相应命令。

1. [Python 3.7](https://www.python.org/downloads/windows/)  
   根据 PyInstaller 的说明文档，其目前(2020-02-18)支持的 Python 版本为 3.5-3.7。这里选择目前最高版本 3.7.6。若需创建32位的可执行文件，请在32位Python环境下运行PyInstaller。（此外 you-get 目前最新版本为 0.4.1403）

2. PyInstaller  
   ```shell
   # 可以加上使用镜像源的参数： --index-url=https://pypi.tuna.tsinghua.edu.cn/simple
   $ pip install pyinstaller
   ```

3. [Git](https://git-scm.com/) clone
   ```shell
   $ git clone https://github.com/soimort/you-get.git
   ```

## Options

根据 [*Using PyInstaller — PyInstaller 3.6 documentation*](https://pyinstaller.readthedocs.io/en/stable/usage.html) 所述，打包一个简单 Python 程序的命令为：
```shell
pyinstaller myscript.py
```

添加 `-F` 参数即可打包为单个可执行文件：
```shell
pyinstaller -F myscript.py
```

PyInstaller 会自动在当前目录下生成 `build/` , `dist/` , `myscript.spec` ，并且打包好的 `myscript.exe` 文件就在 `dist/` 目录下。

但要打包 you-get 这样的项目，需要处理其中一些模块依赖的问题。虽然 PyInstaller 能够自行分析项目的模块依赖，但对于一些特殊情况，需要提供额外参数来解决模块依赖的问题。

## Attempt

> 你可以 [跳过](#final-command) 这一节，直接查看最终的命令。本节将叙述最终命令中各参数的意义。

首先进入 `git clone` 下来的 you-get 项目目录
```shell
$ cd you-get
$ ls
CHANGELOG.rst    LICENSE.txt  README.md   setup.py*  you-get*
contrib/         Makefile     README.rst  src/       you-get.json
CONTRIBUTING.md  MANIFEST.in  setup.cfg   tests/     you-get.plugin.zsh*
```

尝试使用 PyInstaller 直接打包：
```shell
> pyinstaller -F you-get
```

打包成功后，尝试运行则报错 `No module named 'you_get'` ：
```shell
> cd dist
> you-get.exe -V

Traceback (most recent call last):
  File "you-get", line 9, in <module>
ModuleNotFoundError: No module named 'you_get'
[13528] Failed to execute script you-get
```

查阅 [*Helping PyInstaller Find Modules*](https://pyinstaller.readthedocs.io/en/stable/when-things-go-wrong.html#helping-pyinstaller-find-modules) 后得知，由于 `./you-get` 中使用了 `sys.path` ，需要通过 `--path` 参数为 PyInstaller 指明 you_get 这个模块在哪（即 `./src` 目录下）。
```shell
> cd ..
> pyinstaller -F --path=src you-get
> cd dist
> you-get.exe -V

you-get: version 0.4.1403, a tiny downloader that scrapes the web.
```

可以看到已经能正确输出版本号了，接下来试试获取视频信息：
```shell
> you-get.exe -i https://www.bilibili.com/video/av59988590/

you-get: [error] oops, something went wrong.
    # Omit for Brevity...
you-get:   (4) Run the command with '--debug' option,
you-get:       and report this issue with the full output.
```

直接报错了，试试加上 `--debug` 参数：
```shell
> you-get.exe -i https://www.bilibili.com/video/av59988590/ --debug

you-get: version 0.4.1403, a tiny downloader that scrapes the web.
    # Omit for Brevity...
ModuleNotFoundError: No module named 'you_get.extractors'
[1536] Failed to execute script you-get
```
那就尝试导入 `you_get.extractors`
```shell
> cd ..
> pyinstaller -F --path=src you-get --hidden-import=you_get.extractors

> cd dist

# 直接下载 (正常)
> you-get.exe -i https://www.bilibili.com/video/av59988590/
> you-get.exe -o D:/test https://www.bilibili.com/video/av59988590/

# 下载长一点的视频试试 (调用 FFmpeg 合并也没有问题)
> you-get.exe --format=dash-flv360 https://www.bilibili.com/bangumi/play/ep285906

# 试试别的视频网站 (正常下载)
> you-get.exe https://v.qq.com/x/cover/rjae621myqca41h.html

# 试试使用代理 (正常下载)
> you-get.exe -x 127.0.0.1:10809 https://www.youtube.com/watch?v=Ie5qE1EHm_w

# 调用播放器 (能够唤起 PotPlayer 播放视频)
> you-get.exe -p D:/MyProgram/PotPlayer/PotPlayerMini64.exe https://v.qq.com/x/cover/rjae621myqca41h.html

# 下载播放列表 (正常下载)
> you-get.exe -l --format=dash-flv360 https://www.bilibili.com/bangumi/play/ep285906 

```

似乎一切正常，但为了避免潜在问题，不妨将 `src/you_get/cli_wrapper/` ,  `src/you_get/processor/` , `src/you_get/util/` 也都导入并打包：

```shell
> pyinstaller -F --path=src you-get --hidden-import=you_get.extractors --hidden-import=you_get.cli_wrapper --hidden-import=you_get.processor --hidden-import=you_get.util

70 INFO: PyInstaller: 3.6
71 INFO: Python: 3.7.6
    # Omit for Brevity...
4255 INFO: Analyzing hidden import 'you_get.extractors'
4979 INFO: Analyzing hidden import 'you_get.cli_wrapper'
4979 INFO: Processing module hooks...
    # Omit for Brevity...
8347 INFO: Building EXE from EXE-00.toc completed successfully.
```

可以看到即使提供了四个 `--hidden-import` 参数，其导入时只用到了 `you_get.extractors` 和 `you_get.cli_wrapper` ，即便更换顺序也同样如此:
```shell
> pyinstaller -F --path=src you-get --hidden-import=you_get.processor --hidden-import=you_get.cli_wrapper --hidden-import=you_get.util --hidden-import=you_get.extractors
```

暂不清楚其与下面的打包命令的结果有何不同，可能需要深入了解 PyInstaller 的工作原理和 You-Get 内部模块间的调用关系才能知晓。
```shell
> pyinstaller -F --path=src you-get --hidden-import=you_get.extractors --hidden-import=you_get.cli_wrapper
```

---

## Issues

### 网站支持

目前即使是 "通过 pip 安装的 you-get" 也似乎无法下载爱奇艺；解析腾讯视频只有单一清晰度。对此请通过 [annie](https://github.com/iawia002/annie) 下载。
```shell
$ you-get --format=LD https://www.iqiyi.com/v_19ruzj8gv0.html
```

### 特殊情况
 
对于某些视频网站（如西瓜视频），使用 "通过 pip 安装的 you-get" 能正常下载，而使用 "以上文方法打包的 you-get.exe" 则无法下载，例如：
```shell
# 正常下载
$ you-get https://www.ixigua.com/i6701579536644964872

# 无法下载
> you-get.exe https://www.ixigua.com/i6701579536644964872 --debug

you-get: version 0.4.1403, a tiny downloader that scrapes the  web.
    # Omit for Brevity...
ModuleNotFoundError: No module named 'you_get.extractors.ixigua'
[12120] Failed to execute script you-get
```

根据提示导入 `you_get.extractors.ixigua` 重新打包后，能够正常下载。
```shell
> pyinstaller -F --path=src you-get --hidden-import=you_get.extractors --hidden-import=you_get.cli_wrapper --hidden-import=you_get.processor --hidden-import=you_get.util --hidden-import=you_get.extractors.ixigua

# 正常下载
> you-get.exe https://www.ixigua.com/i6701579536644964872 
```

导致需要额外导入单个站点模块的原因可能是 `src/you_get/extractors/__init__.py` 中没有以下语句：
```python
from .ixigua import *
```

若加上这一句后再执行打包，则无需 `--hidden-import=you_get.extractors.ixigua` 也能正常下载。
```shell
> pyinstaller -F --path=src you-get --hidden-import=you_get.extractors --hidden-import=you_get.cli_wrapper --hidden-import=you_get.processor --hidden-import=you_get.util

# 正常下载
> you-get.exe https://www.ixigua.com/i6701579536644964872
```

与之相同的，在 `src/you_get/extractors/` 目录下有对应 extractor (100) 却未在 `src/you_get/extractors/__init__.py` (88) 中 `import` 的站点有：
1. baomihua.py
2. giphy.py
3. huomaotv.py
4. iwara.py
5. ixigua.py
6. missevan.py
7. qie_video.py
8. qq_egame.py
9. toutiao.py
10. vidto.py
11. ximalaya.py
12. yizhibo.py

此外还有一些出现在 Release 的 `you-get-0.4.1403.tar.gz` 中，却不在 GitHub 源码中的 extractors (10)，包含：
1. _blip.py
2. _catfun.py
3. _coursera.py
4. _dongting.py
5. _jpopsuki.py
6. _qianmo.py
7. _songtaste.py
8. _thvideo.py
9. _vid48.py
10. _videobam.py

这些 extractors 均以 `_` 开头，而（参照 `Makefile`）直接运行 `python setup.py sdist`生成的  `dist/you-get-0.4.1403.tar.gz` 则不包含这些 extractors 。 暂不知其原因。

根据上文分析，可以想到解决办法为：将 `"you-get-0.4.1403.tar.gz" you-get-0.4.1403/src/you_get/extractors/` 中以 `_` 开头的 `py` 文件复制到 clone 目录对应位置，并编辑 `src/you_get/extractors/__init__.py` ，在其中逐一导入这些模块，最后再重新打包。

```python
# 为 src/you_get/extractors/__init__.py 文件追加以下语句
from .baomihua import *
from .giphy import *
from .huomaotv import *
from .iwara import *
from .ixigua import *
from .missevan import *
from .qie_video import *
from .qq_egame import *
from .toutiao import *
from .vidto import *
from .ximalaya import *
from .yizhibo import *

from ._blip import *
from ._catfun import *
from ._coursera import *
from ._dongting import *
from ._jpopsuki import *
from ._qianmo import *
from ._songtaste import *
from ._thvideo import *
from ._vid48 import *
from ._videobam import *
```

---

## Final command

综上所述，**最后打包的命令为**：

```shell
> pyinstaller -F --path=src you-get --hidden-import=you_get.extractors --hidden-import=you_get.cli_wrapper --hidden-import=you_get.processor --hidden-import=you_get.util
```