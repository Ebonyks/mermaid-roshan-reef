$p=Split-Path $PSScriptRoot -Parent
& 'C:/Program Files/Git/bin/bash.exe' ($p+'/scripts/trace_opera_gate.sh') *> ($p+'/evidence/opera_2d_diagnostic.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/opera_2d_diagnostic.exit')
