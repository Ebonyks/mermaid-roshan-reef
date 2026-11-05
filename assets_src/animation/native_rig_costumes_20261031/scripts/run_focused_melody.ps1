$p=Split-Path $PSScriptRoot -Parent
& 'C:/Program Files/Git/bin/bash.exe' ($p+'/scripts/focused_melody_gate.sh') *> ($p+'/evidence/melody_focused.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/melody_focused.exit')
