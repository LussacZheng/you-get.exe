@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
:: You-Get Unofficial Build Executable for Windows
:: Author: Lussac (https://blog.lussac.net)
:: Last updated: 2020-02-19
:: >>> Get updated from: https://github.com/LussacZheng/you-get.exe <<<
:: >>> EDIT AT YOUR OWN RISK. <<<
@echo off

if exist build\you-get\ rd /S /Q build\you-get
if exist dist\you-get.exe del /S /Q dist\you-get.exe >NUL 2>NUL

if NOT exist repository\you-get\you-get (
    echo.
    echo  * Please run "devscripts\init.bat" first or clone the repository of "you-get".
    pause > NUL
    exit
)

cd repository
:: First, move out the original `__init__.py` from "you_get.extractors",
::     in order that we can recover everything after build.
:: Then copy all the extractors from `repository\_extractors\`, with a new `__init__.py`
::     which has imported these extractors, into the module "you_get.extractors"
move you-get\src\you_get\extractors\__init__.py .\ > NUL
xcopy _extractors\*.py you-get\src\you_get\extractors\ >NUL
pushd you-get

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
    --icon ..\dist\you-get.ico ^
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
:: Recover everything in you-get.git after build
for /f "delims=" %%i in ('dir /b /a-d _extractors') do (
    del /Q you-get\src\you_get\extractors\%%i >NUL 2>NUL
)
move __init__.py you-get\src\you_get\extractors\ > NUL

cd ..\dist
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
