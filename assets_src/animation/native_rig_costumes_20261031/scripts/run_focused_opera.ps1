$p=Split-Path $PSScriptRoot -Parent
& 'C:/Program Files/Git/bin/bash.exe' ($p+'/scripts/focused_opera_gate.sh') *> ($p+'/evidence/opera_2d_focused.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/opera_2d_focused.exit')
