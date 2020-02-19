@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
@echo off

call use-proxy.bat
cd ..\repository

if NOT exist you-get\.git\ (
    echo  * Please run "init.bat" or clone the repository first.
    pause > NUL
    exit
)
cd you-get

echo.
echo ============================================================
echo  * git pulling "https://github.com/soimort/you-get.git" ...
echo.
git pull
echo.
echo ============================================================
echo.

echo  * Update complete.
echo.

pause
