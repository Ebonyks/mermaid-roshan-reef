from pathlib import Path
import datetime, hashlib, json, shutil, subprocess

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
c=b/'audit/job_candy_workflow_current_v1_20261003'
families=['audit/job_candy_workflow_current_v1_20261003','audit/job_candy_wrap_contact_runtime_v1_20261003','assets_src/imagegen/candy_wrap_states_v1_20261003','assets_src/imagegen/candy_wrap_contact_v1_20261003']
k=b/'audit/job_geology_fossil_reveal_continuity_v1_20261003'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=b,text=True).strip()=='c5977ebb29bb2011b20fc149ad350290f045045c'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=b,text=True).strip(),'Do not mix an existing index.'
src=b/'audit/job_nursery_wash_connected_v1_20261002/review_tools/run_current_full_ci_v357.py'
t=src.read_text(encoding='utf-8').replace('audit/job_nursery_wash_connected_v1_20261002','audit/job_candy_workflow_current_v1_20261003').replace('job-nursery-wash-connected-20261002','job-candy-workflow-current-20261003').replace('SOURCE_CURRENT_MACHINE_V3.json','SOURCE_CURRENT_A3_BEFORE_CAPTURE.json').replace('connected Nursery v3','Candy birthday physical-station repair A3').replace('Nursery connected washing v3','Candy birthday physical-station repair A3')
runner=c/'review_tools/run_current_full_ci_v519.py'
assert not runner.exists();runner.write_text(t,encoding='utf-8')
shutil.copyfile(__file__,c/'review_tools/prepare_candy_checkpoint_v519.py')
g=b/'.gitattributes'; gt=g.read_text(encoding='utf-8')
for p in families+['audit/job_artwork_refinement_live/ALL_ITEMS_V42.original.json','audit/job_artwork_refinement_live/all_items_V42.original.html','audit/job_artwork_refinement_live/BOUNDARY_V42.original.json']:
 line=p+('/**' if p in families else '')+' -text'
 if line not in gt.splitlines(): gt+='\n'+line+'\n'
g.write_text(gt,encoding='utf-8')
ip=b/'design/audit_impacts/job-candy-workflow-current-20261003.json'; d=json.loads(ip.read_text(encoding='utf-8'))
paths={p.relative_to(b).as_posix() for f in families for p in (b/f).rglob('*') if p.is_file()}
paths|={'.gitattributes','ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','scripts/opera_career_world_2d.gd'}
paths|={p.relative_to(b).as_posix() for p in (b/'audit/job_artwork_refinement_live').rglob('*') if p.is_file()}
d['files']=sorted(set(d['files'])|paths);ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
kp=b/'design/audit_impacts/job-geology-fossil-reveal-continuity-20261003.json';kd=json.loads(kp.read_text(encoding='utf-8'));kd['files']=sorted(set(kd['files'])|{p.relative_to(b).as_posix() for p in k.rglob('*') if p.is_file()});kp.write_text(json.dumps(kd,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
allow=b/'tmp/v2_preview_allowed.json';a=json.loads(allow.read_text(encoding='utf-8'));a=sorted(set(a)|paths|{p.relative_to(b).as_posix() for p in k.rglob('*') if p.is_file()});allow.write_text(json.dumps(a,indent=2)+'\n',encoding='utf-8')
result=subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(runner),'--prepare'],cwd=b,text=True,capture_output=True)
print(result.stdout);print(result.stderr);assert result.returncode==0
paths|={p.relative_to(b).as_posix() for f in families for p in (b/f).rglob('*') if p.is_file()}|{p.relative_to(b).as_posix() for p in k.rglob('*') if p.is_file()}|{ip.relative_to(b).as_posix(),kp.relative_to(b).as_posix()}
assert all(not p.startswith(('assets/book/','assets/audio/voices/','assets/characters/friends/','.github/','.codex/','.claude/')) for p in paths)
result=subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=b,input=b'\0'.join(p.encode('utf-8') for p in sorted(paths))+b'\0',capture_output=True)
assert result.returncode==0,result.stderr.decode('utf-8',errors='replace')
print('Prepared exact scoped Candy/Fossil checkpoint:',len(paths),'paths; production change exactly one shared station source. No commit or push yet.')
