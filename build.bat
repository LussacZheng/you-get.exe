@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
:: You-Get Unofficial Build Executable for Windows
:: Author: Lussac (https://blog.lussac.net)
:: Last updated: 2020-07-20
:: >>> Get updated from: https://github.com/LussacZheng/you-get.exe <<<
:: >>> EDIT AT YOUR OWN RISK. <<<
@echo off


rem ================= STEP 0: Root =================


:: Set the root directory
set "root=%~dp0"
set "root=%root:~0,-1%"
cd "%root%"


rem ================= STEP 1: Clean =================


if exist build\you-get\ rd /S /Q build\you-get
if exist dist\ (
    pushd dist
    if exist you-get.exe del /S /Q you-get.exe >NUL 2>NUL
    if exist LICENSE.txt del /S /Q LICENSE.txt >NUL 2>NUL
    if exist README.md del /S /Q README.md >NUL 2>NUL
    if exist README_cn.md del /S /Q README_cn.md >NUL 2>NUL
    popd
)


:: Step 2. Check
if NOT exist repository\you-get\you-get (
    echo.
    echo  * Please run "devscripts\init.bat" first or clone the repository of "you-get".
    pause > NUL
    exit
)


rem ================= STEP 3: Build =================


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
    --icon ..\build\you-get.ico ^
    --hidden-import=you_get.extractors ^
    --hidden-import=you_get.cli_wrapper ^
    --hidden-import=you_get.processor ^
    --hidden-import=you_get.util ^
    you-get
:: PyInstaller bundle command - END

popd

:: Recover everything in you-get.git after built
for /f "delims=" %%i in ('dir /b /a-d _extractors') do (
    del /Q you-get\src\you_get\extractors\%%i >NUL 2>NUL
)
move __init__.py you-get\src\you_get\extractors\ > NUL

cd ..\build
if exist file_version_info.txt (
    echo.
    echo ============================================================
    echo.
    pyi-set_version file_version_info.txt ..\dist\you-get.exe
)
cd ..

echo.
echo ============================================================
echo.
echo  * Build logs saved in:       "%~dp0build\you-get\"
echo  * Build executable saved to: "%~dp0dist\you-get.exe"
echo  * Build completed.


rem ================= STEP 4: Zip =================


echo.
echo ============================================================
echo  * zip "you-get.zip" ...
echo ------------------------------------------------------------
echo.

:: copy the files to be zipped
xcopy /Y repository\you-get\LICENSE.txt dist\ >NUL
xcopy /Y README.md dist\ >NUL
xcopy /Y README_cn.md dist\ >NUL

if NOT exist bin\zip.exe goto :no_zip_exe
if NOT exist bin\bzip2.dll goto :no_zip_exe

:: Get the version of you-get, arch of executable, and build date tag
::   -->  %_version%, %_arch%, %_date%
::   ==>  %_zip_archive%
if exist build\file_version_info.txt (
    set "_info=file_version_info.txt"
) else ( set "_info=file_version_info.sample.txt" )
for /f "tokens=4 delims='" %%i in ('type "build\%_info%" ^| find "FileVersion"') do ( set "_version=%%i" )
for /f "tokens=5 delims='x" %%i in ('type "build\%_info%" ^| find "ProductVersion"') do ( set "_arch=%%i" )
if "%_arch%"=="86" ( set "_arch=32" )
for /f %%i in ('WMIC OS GET LocalDateTime ^| find "."') do ( set "_LDT=%%i" )
set "_date=%_LDT:~2,2%%_LDT:~4,2%%_LDT:~6,2%"
set "_zip_archive=you-get-%_version%-win%_arch%_UB%_date%.zip"

cd dist
..\bin\zip.exe %_zip_archive% you-get.exe LICENSE.txt README.md README_cn.md -z < LICENSE.txt

echo.
echo  * Zip archive file saved to: "%~dp0dist\%_zip_archive%"
echo  * Zip completed.
echo.
echo ============================================================
echo.
echo  * All completed.
echo.
echo ============================================================
echo.

pause
goto :eof

:no_zip_exe
echo.
echo  * Please download "zip.exe" and "bzip2.dll", and put them into "bin/".
pause > NUL
exit

