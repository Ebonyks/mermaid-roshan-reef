$p=Split-Path $PSScriptRoot -Parent
$env:PYTHONUTF8='1';$env:PYTHONIOENCODING='utf-8'
& python ($p+'/scripts/archive_swaps.py') *> ($p+'/evidence/archive_swaps.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/archive_swaps.exit')
