@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
:: You-Get Unofficial Build Executable for Windows
:: Author: Lussac (https://blog.lussac.net)
:: Last updated: 2021-01-30
:: >>> Get updated from: https://github.com/LussacZheng/you-get.exe <<<
:: >>> EDIT AT YOUR OWN RISK. <<<
@echo off
setlocal


rem ================= STEP 0: Root =================


:: Set the root directory
set "root=%~dp0"
set "root=%root:~0,-1%"
cd "%root%"


rem ================= STEP 1: Check =================


if NOT exist repository\you-get\you-get (
    echo.
    echo  * Please run "devscripts\init.bat" first or clone the repository of "you-get".
    pause > NUL
    exit /b 1
)


rem ================= STEP 2: Clean =================


call :echo_title "Clean before building"

if exist build\you-get\ rd /S /Q build\you-get
if exist dist\ (
    pushd dist
    for %%i in ( you-get.exe LICENSE.txt README.md README_cn.md sha256sum.txt) do (
        if exist %%i ( del .\%%i && echo  * Deleted "%root%\dist\%%i" )
    )
    echo.
    if exist you-get*win*UB*.zip del /P .\you-get*win*UB*.zip
    popd
)

call :echo_hrd
echo  * Clean completed.


rem ================= STEP 3: Build =================


cd repository

:: First, move out the original `__init__.py` from "you_get.extractors",
::     in order that we can recover everything after build.
:: Then copy all the extractors from `repository\_extractors\`, with a new `__init__.py`
::     which has imported these extractors, into the module "you_get.extractors"
move you-get\src\you_get\extractors\__init__.py .\ > NUL
xcopy _extractors\*.py you-get\src\you_get\extractors\ >NUL

pushd you-get

call :echo_title "pyinstaller "you-get""

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
    call :echo_hrd
    pyi-set_version file_version_info.txt ..\dist\you-get.exe
)
cd ..

call :echo_hrd
echo  * Build logs saved in:       "%root%\build\you-get\"
echo  * Build executable saved to: "%root%\dist\you-get.exe"
echo  * Build completed.


rem ================= STEP 4: Checksum =================


call :echo_title "SHA256 Checksum of "you-get.exe""

pushd dist
for /f "usebackq skip=1 delims=" %%i in (`certutil -hashfile you-get.exe SHA256`) do (
    set "_hash_result=%%i"
    goto :checksum_next
)
:checksum_next
echo %_hash_result% *you-get.exe> sha256sum.txt
:: Use `echo %_hash_result% | clip` will cause an additional whitespace and one more line.
set /p "_hash_trimSpace=%_hash_result%" < NUL | clip
popd

echo  * SHA256 Checksum: %_hash_result%
echo  * SHA256 Checksum has been copied into your clipboard.
echo  * Checksum file saved to: "%root%\dist\sha256sum.txt"
echo  * Checksum completed.


rem ================= STEP 5: Zip =================


call :echo_title "zip "you-get.zip""

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
set "_zip_archive=you-get_%_version%_win%_arch%_UB%_date%.zip"

cd dist
..\bin\zip.exe %_zip_archive% you-get.exe LICENSE.txt README.md README_cn.md sha256sum.txt -z < LICENSE.txt

call :echo_hrd
echo  * Zip archive file saved to: "%root%\dist\%_zip_archive%"
echo  * Zip completed.


rem ================= STEP 6: Finish =================


call :echo_end "All completed."
pause
exit /b 0


rem ================= FUNCTIONS =================


:no_zip_exe
echo.
echo  * Please download "zip.exe" and "bzip2.dll", and put them into "bin/".
pause > NUL
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
