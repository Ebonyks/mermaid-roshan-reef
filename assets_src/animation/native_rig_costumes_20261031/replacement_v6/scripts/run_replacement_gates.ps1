$ErrorActionPreference='Stop'
function Read-FreshReceipt([string]$path,[datetime]$started) {
 $item=Get-Item -LiteralPath $path -ErrorAction Stop
 if($item.LastWriteTimeUtc -lt $started){throw ('Stale receipt '+$path)}
 return (Get-Content -LiteralPath $path -Raw | ConvertFrom-Json)
}
$r=Split-Path $PSScriptRoot -Parent
$repo=Join-Path $PSScriptRoot '../../../../..'
$g=(& python (Join-Path $repo 'tools/resolve_godot.py') --godot 'C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe').Trim()
foreach($name in @('study.gd','render_stress.gd','stress_swaps.gd','audit_replacement.gd','quick_replacement.gd')) {
 & $g --headless --path ($r+'/godot') --check-only -s $name *> ($r+'/evidence/analyzer_'+$name+'.log')
 if($LASTEXITCODE -ne 0){throw ('Analyzer '+$name)}
}
foreach($theme in @('ballet','magician','original')) {
 $out=$r+'/evidence/render_'+$theme+'_v8'
 $started=(Get-Date).ToUniversalTime()
 $p=Start-Process -FilePath $g -WindowStyle Hidden -ArgumentList @('--disable-vsync','--max-fps','120','--path',($r+'/godot'),'-s','render_stress.gd','--',$out,$theme) -RedirectStandardOutput ($r+'/evidence/'+$theme+'_render.log') -RedirectStandardError ($r+'/evidence/'+$theme+'_render.err') -Wait -PassThru
 if($p.ExitCode -ne 0 -or -not (Test-Path ($out+'/engine_receipt.json'))){throw ('Incomplete render '+$theme)}
 $receipt=Read-FreshReceipt ($out+'/engine_receipt.json') $started
 if($receipt.frames_rendered -ne 291){throw ('Wrong render count '+$theme)}
 if($theme -ne 'original') {
  & python -B ($r+'/scripts/audit_study.py') $out --rig ($r+'/godot/rig_'+$theme+'.json') *> ($r+'/evidence/'+$theme+'_geometry.log')
  $geom=$LASTEXITCODE
  & python -B ($r+'/scripts/audit_motion.py') $out *> ($r+'/evidence/'+$theme+'_motion.log')
  $motion=$LASTEXITCODE
  @{geometry=$geom;motion=$motion}|ConvertTo-Json|Set-Content ($r+'/evidence/'+$theme+'_gates.json')
  if($geom -ne 0 -or $motion -ne 0){throw ('Geometry or motion '+$theme)}
 }
}
$started=(Get-Date).ToUniversalTime()
$p=Start-Process -FilePath $g -WindowStyle Hidden -ArgumentList @('--disable-vsync','--max-fps','120','--path',($r+'/godot'),'-s','stress_swaps.gd','--',($r+'/evidence/swaps_v8')) -RedirectStandardOutput ($r+'/evidence/swaps.log') -RedirectStandardError ($r+'/evidence/swaps.err') -Wait -PassThru
$p.ExitCode|Set-Content ($r+'/evidence/swaps.exit')
if($p.ExitCode -ne 0){throw 'Swaps'}
$receipt=Read-FreshReceipt ($r+'/evidence/swaps_v8/swap_audit.json') $started
if(!$receipt.pass -or $receipt.pixel_cases -ne 243 -or $receipt.swaps -ne 19248){throw 'Missing/incomplete native swap receipt'}

$started=(Get-Date).ToUniversalTime()
$p=Start-Process -FilePath $g -WindowStyle Hidden -ArgumentList @('--disable-vsync','--max-fps','120','--path',($r+'/godot'),'-s','audit_replacement.gd','--',($r+'/evidence/replacement')) -RedirectStandardOutput ($r+'/evidence/replacement.log') -RedirectStandardError ($r+'/evidence/replacement.err') -Wait -PassThru
$p.ExitCode|Set-Content ($r+'/evidence/replacement.exit')
if($p.ExitCode -ne 0){throw 'Replacement contamination audit'}
$receipt=Read-FreshReceipt ($r+'/evidence/replacement/replacement_audit.json') $started
if(!$receipt.pass -or $receipt.frames -ne 582){throw 'Missing/incomplete replacement receipt'}
