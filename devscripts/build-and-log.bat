@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
@echo off
setlocal

:: Enter the root directory
pushd "%~dp0"
pushd ..

if NOT exist .\dist\ md dist
set "log=.\dist\you-get.logging"

:: "python -u": force the stdout and stderr streams to be unbuffered
:: "build.py -f": force delete the outputs of last build
poetry run python -u build.py -f %* > %log% 2>&1

:: Set the filename of the log file to the same as the zip file
for /f "delims=" %%i in ('dir /b /a:a /o:d .\dist\you-get*win*UB*.zip') do ( set "filename=%%i" )
set "log2=.\dist\%filename:.zip=.log%"
move %log% %log2% > NUL

echo  * All completed.
echo  * Build logs saved in: "%cd%\%log2:.\=%"

popd & popd
endlocal
