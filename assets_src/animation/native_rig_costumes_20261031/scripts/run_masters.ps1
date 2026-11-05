$p=Split-Path $PSScriptRoot -Parent
$env:PYTHONUTF8='1';$env:PYTHONIOENCODING='utf-8'
foreach($theme in @('ballet','magician')){New-Item -ItemType Directory -Force -Path ($p+'/masters/'+$theme)|Out-Null;foreach($clip in @('arm_bend','blink','tail_bend')){New-Item -ItemType Directory -Force -Path ($p+'/masters/reopened/'+$theme+'/'+$clip)|Out-Null}}
while(!(Test-Path ($p+'/evidence/render_magician_v5/engine_receipt.json'))){Start-Sleep -Seconds 5}
$args=@('-b','--script-param',('root='+$p.Replace('\','/')),'--script',($p+'/scripts/import_masters.lua'))
$import=Start-Process 'C:/Program Files/Aseprite/Aseprite.exe' -ArgumentList $args -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput ($p+'/evidence/aseprite_import.log') -RedirectStandardError ($p+'/evidence/aseprite_import.err')
$reopen=Start-Process 'C:/Program Files/Aseprite/Aseprite.exe' -ArgumentList @('-b','--script-param',('root='+$p.Replace('\','/')),'--script',($p+'/scripts/reopen_masters.lua')) -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput ($p+'/evidence/aseprite_reopen.log') -RedirectStandardError ($p+'/evidence/aseprite_reopen.err')
& python ($p+'/scripts/verify_masters.py') *> ($p+'/evidence/aseprite_verify.log')
@{import=$import.ExitCode;reopen=$reopen.ExitCode;verify=$LASTEXITCODE}|ConvertTo-Json|Set-Content ($p+'/evidence/aseprite_processes.json')
