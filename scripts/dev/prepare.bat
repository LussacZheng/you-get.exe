@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
@echo off

:: Enter the target directory
pushd "%~dp0"
call use-proxy.bat
cd ..\..\repository


if NOT exist you-get\ (
    echo  * Repository `you-get` not found, starting to clone it.
    goto Init
)

set choice=0
echo  * You might have already cloned the repository at `repository\you-get`.
echo.
echo To  update  the repository `you-get`, please enter U;
echo To re-clone the repository `you-get`, please enter R;
set /p choice="Press ENTER to cancel and exit: "
if /i "%choice%"=="U" goto Update
if /i "%choice%"=="R" goto ReClone
call :echo_title Invalid input. Cancelled.
goto Exit


rem ================= Action Types =================


:Init
call :echo_title git cloning "https://github.com/soimort/you-get.git" ...
git clone https://github.com/soimort/you-get.git
call :echo_title Initialization complete.
goto Exit


:Update
cd you-get
call :echo_title git pulling "https://github.com/soimort/you-get.git" ...
git pull
call :echo_title Update complete.
goto Exit


:ReClone
rd /S /Q you-get
goto Init


:Exit
popd
pause > NUL
exit


rem ================= FUNCTIONS =================


:echo_title
call :echo_hre
echo  * %*
call :echo_hre
goto :eof


:: echo horizontal rule (equal)
:echo_hre
echo.
echo ============================================================
echo.
goto :eof
