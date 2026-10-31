$ErrorActionPreference = 'Stop'
$portableRoot = 'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\ComfyUI\0.34.0\ComfyUI_windows_portable'
$comfyRoot = Join-Path $portableRoot 'ComfyUI'
$pythonExe = Join-Path $portableRoot 'python_embeded\python.exe'
$root = 'H:\MermaidReefTools\LocalVideo'
$port = 8191
foreach ($directory in @((Join-Path $root 'retake_temp'),(Join-Path $root 'retake_user'))) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) { throw 'Port 8191 is occupied; existing process left untouched.' }
$env:PYTHONDONTWRITEBYTECODE = '1'
$arguments = @('-s','-B','-u', (Join-Path $PSScriptRoot 'retake_server_boot.py'), '--listen','127.0.0.1','--port','8191',
 '--extra-model-paths-config',(Join-Path $root 'model_paths.yaml'),
 '--input-directory',(Join-Path $root 'input'),'--output-directory',(Join-Path $root 'output'),
 '--temp-directory',(Join-Path $root 'retake_temp'),'--user-directory',(Join-Path $root 'retake_user'),
 '--lowvram','--cpu-vae','--fp32-text-enc','--bf16-unet','--reserve-vram','2.8',
 '--disable-dynamic-vram','--disable-async-offload','--disable-pinned-memory','--disable-cuda-malloc',
 '--preview-method','none','--cache-none','--disable-all-custom-nodes','--whitelist-custom-nodes','ComfyUI-GGUF')
$process = Start-Process -FilePath $pythonExe -ArgumentList $arguments -WorkingDirectory $comfyRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $root 'logs\retake.stdout.log') -RedirectStandardError (Join-Path $root 'logs\retake.stderr.log')
$process.Id | Set-Content -LiteralPath (Join-Path $root 'retake.pid')
Write-Output "Started isolated retake server on 8191: PID $($process.Id)"
