$p=Split-Path $PSScriptRoot -Parent
Set-Location (Join-Path $PSScriptRoot '../../../..')
$env:PYTHONUTF8='1';$env:PYTHONIOENCODING='utf-8'
& python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development *> ($p+'/evidence/authority_contract_tests.log')
$LASTEXITCODE|Set-Content ($p+'/evidence/authority_contract_tests.exit')
& python -m gdtoolkit.parser ($p+'/godot/study.gd') ($p+'/godot/render_stress.gd') ($p+'/godot/stress_swaps.gd') *> ($p+'/evidence/native_script_parser.log')
$parse=$LASTEXITCODE
& python tools/lint_inference.py ($p+'/godot/study.gd') ($p+'/godot/render_stress.gd') ($p+'/godot/stress_swaps.gd') *> ($p+'/evidence/native_script_inference.log')
$lint=$LASTEXITCODE
$repo=Join-Path $PSScriptRoot '../../../..'
$g=(& python (Join-Path $repo 'tools/resolve_godot.py')).Trim()
if($LASTEXITCODE -ne 0){throw 'Approved Godot resolver failed'}
$results=@{}
foreach($script in @('study.gd','render_stress.gd','stress_swaps.gd')){
 $proc=Start-Process $g -WindowStyle Hidden -ArgumentList @('--headless','--path',($p+'/godot'),'--check-only','-s',$script) -PassThru -RedirectStandardOutput ($p+'/evidence/analyzer_'+$script+'.log') -RedirectStandardError ($p+'/evidence/analyzer_'+$script+'.err')
 $proc.WaitForExit()
 $results[$script]=$proc.ExitCode
}
@{parser=$parse;inference=$lint;native_analyzer=$results}|ConvertTo-Json|Set-Content ($p+'/evidence/native_script_gates.json')
