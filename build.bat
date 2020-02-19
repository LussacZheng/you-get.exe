@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
:: Video Downloaders (You-Get, Youtube-dl, Annie) One-Click Deployment Batch (Windows)
:: Author: Lussac (https://blog.lussac.net)
:: Last updated: 2020-02-19
:: >>> Get updated from: https://github.com/LussacZheng/you-get.exe <<<
:: >>> EDIT AT YOUR OWN RISK. <<<
@echo off

if exist build\you-get\ rd /S /Q build\you-get
if exist dist\you-get.exe del /S /Q dist\you-get.exe >NUL 2>NUL
pushd repository\you-get

echo.
echo ============================================================
echo  * pyinstaller "you-get" ...
echo ------------------------------------------------------------
echo.
:: PyInstaller bundle command - START
pyinstaller -F --path=src ^
    --distpath ..\..\dist ^
    --workpath ..\..\build ^
    --specpath ..\..\build ^
    --hidden-import=you_get.extractors ^
    --hidden-import=you_get.cli_wrapper ^
    --hidden-import=you_get.processor ^
    --hidden-import=you_get.util ^
    you-get
:: PyInstaller bundle command - END
echo.
echo ============================================================
echo.

popd
cd dist
if exist file_version_info.txt (
    pyi-set_version file_version_info.txt you-get.exe
    echo.
    echo ============================================================
    echo.
)

echo  * Build logs saved in:       "%~dp0build\you-get\"
echo  * Build executable saved to: "%~dp0dist\you-get.exe"
echo  * Build complete.
echo.

pause
