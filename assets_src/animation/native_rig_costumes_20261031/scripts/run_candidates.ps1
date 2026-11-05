$ErrorActionPreference='Stop'
$p=Split-Path $PSScriptRoot -Parent
$repo=Join-Path $PSScriptRoot '../../../..'
$g=(& python (Join-Path $repo 'tools/resolve_godot.py')).Trim()
if($LASTEXITCODE -ne 0){throw 'Approved Godot resolver failed'}
foreach($theme in @('ballet','magician')) {
 $out=Join-Path $p ('evidence/render_'+$theme+'_v5')
 $process=Start-Process -FilePath $g -WindowStyle Hidden -ArgumentList @('--path',($p+'/godot'),'-s','render_stress.gd','--',$out,$theme) -RedirectStandardOutput ($p+'/evidence/'+$theme+'_render_v5.log') -RedirectStandardError ($p+'/evidence/'+$theme+'_render_v5.err') -Wait -PassThru
 if($process.ExitCode -ne 0){throw ('Render failed '+$theme)}
 & python ($p+'/scripts/audit_study.py') $out --rig ($p+'/godot/rig_'+$theme+'.json') *> ($p+'/evidence/'+$theme+'_geometry_v5.log')
 $geometry=$LASTEXITCODE
 & python ($p+'/scripts/audit_motion.py') $out *> ($p+'/evidence/'+$theme+'_motion_v5.log')
 $motion=$LASTEXITCODE
 @{theme=$theme;render=$process.ExitCode;geometry=$geometry;motion=$motion}|ConvertTo-Json|Set-Content ($p+'/evidence/'+$theme+'_gates_v5.json')
}
