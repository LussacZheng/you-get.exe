@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
@echo off
setlocal

:: Set the root directory
pushd "%~dp0"
pushd ..

set "output=devscripts\you-get.exe.zip"

if exist %output% del /P .\%output%

zip -r %output% ^
    build/file_version_info.tmpl ^
    build/you-get.ico ^
    devscripts/build-and-log.bat ^
    repository/ ^
    build.py ^
    poetry.lock poetry.toml pyproject.toml ^
    README.md README_cn.md ^
    -x "repository/you-get/.git/*" ^
    -x "*__pycache__*"

echo. & echo  * Zip file saved in: "%cd%\%output%"

popd & popd
endlocal
