@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
@echo off

call use-proxy.bat
cd ..\repository

if exist you-get\ (
    echo  * You might have cloned the repository already.
    echo    Press any key to continue ^(remove the and re-clone^); Close this window to stop.
    pause > NUL
    rd /S /Q you-get
)

echo.
echo ============================================================
echo  * git cloning "https://github.com/soimort/you-get.git" ...
echo.
git clone https://github.com/soimort/you-get.git
echo.
echo ============================================================
echo.

echo  * Initialization complete.
echo.

pause
