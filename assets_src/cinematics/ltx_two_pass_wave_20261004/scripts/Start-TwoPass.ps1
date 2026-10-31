$ErrorActionPreference = 'Stop'
$portableRoot = 'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\ComfyUI\0.34.0\ComfyUI_windows_portable'
$comfyRoot = Join-Path $portableRoot 'ComfyUI'
$pythonExe = Join-Path $portableRoot 'python_embeded\python.exe'
$dataRoot = 'H:\MermaidReefTools\LocalVideo'
foreach ($directory in @('two_pass_temp','two_pass_user','logs','input','output')) { New-Item -ItemType Directory -Path (Join-Path $dataRoot $directory) -Force | Out-Null }
if (Get-NetTCPConnection -LocalPort 8192 -State Listen -ErrorAction SilentlyContinue) { throw 'Port8192 occupied; existing process untouched.' }
$arguments = @('-s','-B','-u',(Join-Path $PSScriptRoot 'study_server_boot.py'),'--listen','127.0.0.1','--port','8192',
 '--extra-model-paths-config',(Join-Path $dataRoot 'two_pass_model_paths.yaml'),
 '--input-directory',(Join-Path $dataRoot 'input'),'--output-directory',(Join-Path $dataRoot 'output'),
 '--temp-directory',(Join-Path $dataRoot 'two_pass_temp'),'--user-directory',(Join-Path $dataRoot 'two_pass_user'),
 '--reserve-vram','1.2','--disable-dynamic-vram','--disable-async-offload','--disable-pinned-memory','--disable-cuda-malloc',
 '--preview-method','none','--use-pytorch-cross-attention','--disable-api-nodes','--disable-all-custom-nodes','--whitelist-custom-nodes','ComfyUI-GGUF')
$process = Start-Process -FilePath $pythonExe -ArgumentList $arguments -WorkingDirectory $comfyRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $dataRoot 'logs\two_pass.stdout.log') -RedirectStandardError (Join-Path $dataRoot 'logs\two_pass.stderr.log')
$process.Id | Set-Content -LiteralPath (Join-Path $dataRoot 'two_pass.pid')
Write-Output "Started isolated two-pass server8192: PID $($process.Id)"

# Keep this launch host alive so managed tool-session cleanup does not stop the owned server.
Wait-Process -Id $process.Id
