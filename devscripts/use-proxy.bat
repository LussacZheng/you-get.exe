@rem - Encoding:utf-8; Mode:Batch; Language:en; LineEndings:CRLF -
@echo off
echo.

:: Read the configuration file: "./use-proxy.settings"
set "_config=%~dp0%~n0.settings"
if NOT exist %_config% (
    echo # EDIT AT YOUR OWN RISK.>%_config%
    echo.>>%_config%
    echo # "true" or "false">>%_config%
    echo GlobalProxy: false>>%_config%
    echo ProxyHost: http://127.0.0.1>>%_config%
    echo HttpPort: 1080>>%_config%
    echo HttpsPort: 1080>>%_config%
    echo  * You'd better close this window and edit the configuration file "%_config%" first.
    echo.
    pause
    echo.
)

:: Set proxy for CMD console window
for /f "tokens=2 delims= " %%i in ('findstr /i "GlobalProxy" "%_config%"') do ( set "_globalProxy=%%i" )
for /f "tokens=2 delims= " %%i in ('findstr /i "ProxyHost" "%_config%"') do ( set "_proxyHost=%%i" )
for /f "tokens=2 delims= " %%i in ('findstr /i "HttpPort" "%_config%"') do ( set "_httpPort=%%i" )
for /f "tokens=2 delims= " %%i in ('findstr /i "HttpsPort" "%_config%"') do ( set "_httpsPort=%%i" )
echo  * GlobalProxy : %_globalProxy%
if "%_globalProxy%"=="true" (
    set "http_proxy=%_proxyHost%:%_httpPort%"
    set "https_proxy=%_proxyHost%:%_httpsPort%"
    echo    HTTP_PROXY  : %_proxyHost%:%_httpPort%
    echo    HTTPS_PROXY : %_proxyHost%:%_httpsPort%
)
echo.
