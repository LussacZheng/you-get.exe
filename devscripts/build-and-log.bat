@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
@echo off

:: Enter the root directory
pushd "%~dp0"
pushd ..

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
set "_log=.\dist\you-get_%_version%_win%_arch%_UB%_date%.log"

if exist %_log% del %_log%


poetry run build.bat -f --no-pause > %_log% 2>&1

echo  * All completed.
echo  * Build logs saved in: "%_log%"

popd & popd
