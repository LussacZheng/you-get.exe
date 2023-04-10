#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import stat
import subprocess

WD = os.path.normpath(os.path.join(os.path.abspath(__file__), "../../../repository"))
REPO = os.path.join(WD, "you-get")

REMOTE = "https://github.com/soimort/you-get.git"


def main():
    if shutil.which("git") is None:
        print(" * You should install `git` first.")
        return

    os.chdir(WD)

    if not os.path.exists(REPO):
        print(" * Repository `you-get` not found, starting to clone it.")
        clone()
        return

    print(f" * You might have already cloned the repository at `{REPO}`.\n")
    print("To  update  the repository `you-get`, please enter U;")
    print("To re-clone the repository `you-get`, please enter R;")
    choice = input("Press ENTER to cancel and exit: ").upper()
    if choice == "U":
        update()
    elif choice == "R":
        re_clone()
    else:
        echo("Invalid input. Cancelled.")


def clone():
    apply_proxy_config()
    echo(f'git cloning "{REMOTE}" ...')
    subprocess.call(f"git clone {REMOTE}")
    echo("Initialization complete.")


def update():
    apply_proxy_config()
    os.chdir(REPO)
    echo(f'git pulling "{REMOTE}" ...')
    subprocess.call("git pull")
    echo("Update complete.")


def re_clone():
    def redo_with_write(redo_func, path, _):
        os.chmod(path, stat.S_IWRITE)
        redo_func(path)

    shutil.rmtree(REPO, onerror=redo_with_write)
    clone()


def echo(msg: str):
    # horizontal rule of 'equal'
    hre = f"\n{'=' * 60}\n"
    print(hre)
    print(f" * {msg}")
    print(hre)


def apply_proxy_config():
    """Read the configuration file `./prepare.conf` to determine whether to set the proxy."""
    config_file = os.path.splitext(__file__)[0] + ".conf"

    if not os.path.isfile(config_file):
        with open(config_file, "w", encoding="utf-8") as f:
            f.write("\n".join([
                "[proxy]",
                "# `true` or `false`",
                "enable = false",
                "HTTP_PROXY = http://127.0.0.1:7890",
                "HTTPS_PROXY = http://127.0.0.1:7890",
            ]))
        print(f"\n * To use proxy when cloning, edit `{config_file}` first.\n")
        return

    import configparser
    config = configparser.ConfigParser()
    config.read(config_file)
    if config.getboolean("proxy", "enable"):
        http_proxy = config["proxy"]["HTTP_PROXY"]
        https_proxy = config["proxy"]["HTTPS_PROXY"]
        print("\n * Proxy       : enabled")
        print("   HTTP_PROXY  :", http_proxy)
        print("   HTTPS_PROXY :", https_proxy)
        os.environ["HTTP_PROXY"] = http_proxy
        os.environ["HTTPS_PROXY"] = https_proxy


if __name__ == '__main__':
    main()
