$p=Split-Path $PSScriptRoot -Parent
& 'C:/Program Files/Git/bin/bash.exe' ($p+'/scripts/trace_melody_gate.sh') *> ($p+'/evidence/melody_diagnostic.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/melody_diagnostic.exit')
