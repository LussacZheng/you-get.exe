@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
:: You-Get Unofficial Build Executable for Windows
:: Author: Lussac (https://blog.lussac.net)
:: Last updated: 2021-01-31
:: >>> Get updated from: https://github.com/LussacZheng/you-get.exe <<<
:: >>> EDIT AT YOUR OWN RISK. <<<
@echo off
setlocal


rem ================= STEP 0: Init =================


:: Set the root directory
set "root=%~dp0"
set "root=%root:~0,-1%"
cd "%root%"

:: Set a list of required files
set "_bin_list=bzip2.dll dos2unix.exe zip.exe"
set "_dos2unix_list=LICENSE.txt README.md README_cn.md sha256sum.txt"
set "_zip_list=you-get.exe LICENSE.txt README.md README_cn.md sha256sum.txt"


rem ================= STEP 1: Check =================


if NOT exist repository\you-get\you-get (
    echo.
    echo  * Please run "devscripts\init.bat" first or clone the repository of "you-get".
    pause > NUL
    exit /b 1
)

:: Check the necessary tools
pushd bin
for %%i in ( %_bin_list% ) do (
    if NOT exist %%i call :no_exe "%%i"
)
if "%errorlevel%" == "1" goto :no_exe
popd


rem ================= STEP 2: Clean =================


call :echo_title "Clean before building"

if exist build\you-get\ rd /S /Q build\you-get
if exist dist\ (
    pushd dist
    for %%i in ( %_zip_list% ) do (
        if exist %%i ( del .\%%i && echo  * Deleted "%root%\dist\%%i" )
    )
    echo.
    if exist you-get*win*UB*.zip del /P .\you-get*win*UB*.zip
    popd
)

call :echo_hrd
echo  * Clean completed.


rem ================= STEP 3: Build =================


pushd repository

:: First, move out the original `__init__.py` from "you_get.extractors",
::     in order that we can recover everything after build.
:: Then copy all the extractors from `repository\_extractors\`, with a new `__init__.py`
::     which has imported these extractors, into the module "you_get.extractors"
move you-get\src\you_get\extractors\__init__.py .\ > NUL
xcopy _extractors\*.py you-get\src\you_get\extractors\ >NUL

pushd you-get

call :echo_title "pyinstaller "you-get""

:: PyInstaller bundle command - START
::     For PyInstaller 4.6,  use `--icon ..\build\you-get.ico`;
::                     4.10, use `--icon you-get.ico`;
::                     5.0,  DO NOT use 5.0
pyinstaller -F --path=src ^
    --noupx ^
    --distpath ..\..\dist ^
    --workpath ..\..\build ^
    --specpath ..\..\build ^
    --icon you-get.ico ^
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

pushd ..\build
if exist file_version_info.txt (
    call :echo_hrd
    pyi-set_version file_version_info.txt ..\dist\you-get.exe
)

popd & popd

call :echo_hrd
echo  * Build logs saved in:       "%root%\build\you-get\"
echo  * Build executable saved to: "%root%\dist\you-get.exe"
echo  * Build completed.


rem ================= STEP 4: Copy =================


call :echo_title "Copy the required files"

xcopy /Y repository\you-get\LICENSE.txt dist\ >NUL
xcopy /Y README.md dist\ >NUL
xcopy /Y README_cn.md dist\ >NUL

echo  * All the required files are now in: "%root%\dist\you-get.exe"
echo  * Copy completed.


rem ================= STEP 5: Checksum =================


call :echo_title "SHA256 Checksum of "you-get.exe""

pushd dist
:: Remove unnecessary whitespace from the hash value.
::   This is for the compatibility with Windows 7 (32-bit),
::       since the output of "certutil -hashfile *" on 32-bit Win7 is in the format of:
::       xx xx xx xx xx ... xx xx xx xx
::   And "Get-FileHash" is not available in PowerShell 2.0 :
::       powershell -command "(Get-FileHash you-get.exe -Algorithm SHA256).Hash.ToLower()"
for /f "usebackq" %%i in (`powershell -command "(certutil -hashfile you-get.exe SHA256 | Select-Object -Skip 1 -First 1) -replace ' '"`) do (
    set "_hash_result=%%i"
)
echo %_hash_result% *you-get.exe> sha256sum.txt
:: Use `echo %_hash_result% | clip` will cause an additional whitespace and one more line.
set /p "_hash_trimSpace=%_hash_result%" < NUL | clip
popd

echo  * SHA256 Checksum: %_hash_result%
echo  * SHA256 Checksum has been copied into your clipboard.
echo  * Checksum file saved to: "%root%\dist\sha256sum.txt"
echo  * Checksum completed.


rem ================= STEP 6: CRLF to LF =================


call :echo_title "Convert line endings to LF"

pushd dist
for %%i in ( %_dos2unix_list% ) do (
    ..\bin\dos2unix.exe %%i
)
popd

call :echo_hrd
echo  * Convert completed.


rem ================= STEP 7: Zip =================


call :echo_title "zip "you-get.zip""

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
set "_zip_archive=you-get_%_version%_win%_arch%_UB%_date%.zip"

cd dist
:: Zip all the required files
..\bin\zip.exe %_zip_archive% %_zip_list% -z < LICENSE.txt

call :echo_hrd
echo  * Zip archive file saved to: "%root%\dist\%_zip_archive%"
echo  * Zip completed.


rem ================= STEP 99: Finish =================


call :echo_end "All completed."
pause
exit /b 0


rem ================= FUNCTIONS =================


:no_exe
echo.
if NOT "%~1"=="" (
    echo  ! "%~1" NOT found.
) else (
    echo  * Please download the above tool^(s^), and put it/them into "bin/".
    pause > NUL
)
exit /b 1


:echo_title
call :echo_hre
echo  * %~1 ...
call :echo_hrd
goto :eof


:: echo horizontal rule (equal)
:echo_hre
echo.
echo ============================================================
echo.
goto :eof


:: echo horizontal rule (dash)
:echo_hrd
echo.
echo ------------------------------------------------------------
echo.
goto :eof


:echo_end
call :echo_hre
echo  * %~1
call :echo_hre
goto :eof
