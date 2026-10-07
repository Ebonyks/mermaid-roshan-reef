@echo off
rem Mermaid Roshan rig pilot: starts ComfyUI (LTX-2.5, port 8194) and runs the job files Claude writes
rem to jobs\rig_pilot\queue. Close this window to stop everything.
setlocal
set "RT=%~dp0"
set "PY=C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\ComfyUI\0.34.0\ComfyUI_windows_portable\python_embeded\python.exe"
title Mermaid Roshan rig pilot runner
if not exist "%PY%" (
  echo Python was not found at:
  echo   %PY%
  echo Tell Claude, and it will update this file.
  pause
  exit /b 1
)
"%PY%" -I "%RT%scripts\rig_pilot_runner.py"
echo.
echo The rig pilot runner has stopped.
pause
