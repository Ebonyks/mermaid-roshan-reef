$p=Split-Path $PSScriptRoot -Parent
$env:PYTHONUTF8='1';$env:PYTHONIOENCODING='utf-8'
while(!(Test-Path ($p+'/evidence/render_magician_v5/engine_receipt.json'))){Start-Sleep -Seconds 5}
& python ($p+'/scripts/package_costumes.py') *> ($p+'/evidence/package_review_v5.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/package_review_v5.exit')
& python ($p+'/scripts/archive_swaps.py') *> ($p+'/evidence/archive_swaps.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/archive_swaps.exit')
& python ($p+'/scripts/comparison_reel.py') *> ($p+'/evidence/comparison_reel.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/comparison_reel.exit')
