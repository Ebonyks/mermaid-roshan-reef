@echo off
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_video_tools.ps1" %*
exit /b %ERRORLEVEL%
