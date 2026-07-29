@echo off
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0encode_cartoon.ps1" %*
exit /b %ERRORLEVEL%
