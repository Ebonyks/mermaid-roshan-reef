$p=Split-Path $PSScriptRoot -Parent
Set-Location (Join-Path $PSScriptRoot '../../../..')
$env:PYTHONUTF8='1';$env:PYTHONIOENCODING='utf-8'
& 'C:/Program Files/Git/bin/bash.exe' ($p+'/scripts/project_gates.sh') *> ($p+'/evidence/project_gates.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/project_gates.exit')
