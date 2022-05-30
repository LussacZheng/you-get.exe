@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
@echo off

:: Set the root directory
pushd "%~dp0"

set "_output=you-get.exe.zip"

if exist %_output% del /P .\%_output%

pushd ..

zip -r %_output% ^
    bin/bzip2.dll ^
    bin/dos2unix.exe ^
    bin/zip.exe ^
    build/file_version_info.txt ^
    build/you-get.ico ^
    devscripts/build-and-log.bat ^
    repository/ ^
    build.bat ^
    poetry.lock poetry.toml pyproject.toml ^
    README.md README_cn.md ^
    -x "repository/you-get/.git/*"

move %_output% devscripts\

popd & popd
