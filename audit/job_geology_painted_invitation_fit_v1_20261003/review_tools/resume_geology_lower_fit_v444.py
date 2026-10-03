from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=R/'audit/job_geology_painted_invitation_fit_v1_20261003';G=P/'runtime_gate_lower_a2'
assert G.is_dir() and not list(G.iterdir())
runner=P/'review_tools/run_lower_fit_v443.py';s=runner.read_text();assert "ip=R/" not in s and s.count('G.mkdir(exist_ok=False)')==1
s=s.replace("G=P/'runtime_gate_lower_a2';G.mkdir(exist_ok=False)","ip=R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json'\nG=P/'runtime_gate_lower_a2';G.mkdir(exist_ok=True)")
runner.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/prepare_and_run_geology_lower_fit_v443.py'),P/'review_tools/prepare_and_run_geology_lower_fit_v443.py')
shutil.copyfile(Path(__file__),P/'review_tools'/Path(__file__).name)
p=P/'LOWER_FIT_PLAN_V443.json';d=json.loads(p.read_text());d['helper_preflight_correction']={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'failure':'Generated runner omitted ip variable; NameError before first command. Empty runtime output directory verified; no engine capture had begun. Added exact impact path and resumed runner, without preparing again or replacing any capture.','production_changes':False};p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
exec(compile(s,str(runner),'exec'),{'__file__':str(runner),'__name__':'__main__'})
