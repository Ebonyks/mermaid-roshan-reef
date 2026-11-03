$p=Split-Path $PSScriptRoot -Parent
& 'C:/Program Files/Git/bin/bash.exe' ($p+'/scripts/project_probe_rerun.sh') *> ($p+'/evidence/project_probes_rerun.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/project_probes_rerun.exit')
