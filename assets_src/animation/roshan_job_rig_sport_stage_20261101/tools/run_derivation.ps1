$ErrorActionPreference='Stop'
$root=(Split-Path $PSScriptRoot -Parent).Replace('\','/')
$exe='C:/Program Files/Aseprite/Aseprite.exe'
$repo=Split-Path (Split-Path (Split-Path $root -Parent) -Parent) -Parent
$p=Start-Process -FilePath $exe -ArgumentList @('-b','--script-param',('root='+$root),'--script',($root+'/tools/prepare_art.lua')) -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput ($root+'/evidence/derive_v3_prepare.log') -RedirectStandardError ($root+'/evidence/derive_v3_prepare.err')
if($p.ExitCode -ne 0){throw 'Aseprite preparation failed'}
$p=Start-Process -FilePath $exe -ArgumentList @('-b','--script-param',('root='+$root),'--script-param',('racer='+$repo+'/assets/opera/worlds/actors/roshan_racer.png'),'--script',($root+'/tools/segment_actions.lua')) -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput ($root+'/evidence/derive_v3_segment.log') -RedirectStandardError ($root+'/evidence/derive_v3_segment.err')
if($p.ExitCode -ne 0){throw 'Aseprite action segmentation failed'}
python -X utf8 -B ($root+'/tools/build_mesh.py')
$godot='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe'
$p=Start-Process -FilePath $godot -ArgumentList @('--path',($root+'/demo'),'--rendering-method','mobile','--resolution','1280x720','--position','10000,10000','-s','capture.gd','--',($root+'/evidence/quick_v3')) -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput ($root+'/evidence/quick_v3.log') -RedirectStandardError ($root+'/evidence/quick_v3.err')
if($p.ExitCode -ne 0){throw 'Actual native capture failed'}
Write-Output 'BASE_DERIVATION_COMPLETE; run racer_panel.lua and joint_caps.lua before final capture as documented in provenance.'
