from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_river_join_study_v1_20261001';g=f/'runtime_gate';g.mkdir(exist_ok=True)
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';engine='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/Path(__file__).name)
scripts=[p.relative_to(b).as_posix() for p in sorted(f.glob('*.gd'))]
for tag,args in [('parser_v1',[py,'-X','utf8','-B','-m','gdtoolkit.parser']+scripts),('inference_v1',[py,'-X','utf8','-B','tools/lint_inference.py']+scripts),('analyzer_v4',[engine,'--headless','--path',str(b),'--check-only','-s','audit/job_river_join_study_v1_20261001/capture_join_study_v4.gd']),('authority_v1',[py,'-X','utf8','-B','tools/audit_document_authority.py']),('development_v1',[py,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(args,cwd=b,capture_output=True,timeout=180)
 for name,data in [('stdout',p.stdout),('stderr',p.stderr)]: (g/(tag+'.'+name+'.log')).write_bytes(data)
 receipt={'command':args,'exit_code':p.returncode,'status':'PASS' if p.returncode==0 else 'FAIL','started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()};write(g/(tag+'.receipt.json'),receipt)
 print(tag,p.returncode,p.stdout.decode('utf-8','replace')[-2200:],p.stderr.decode('utf-8','replace')[-800:],flush=True)
 # Keep all independent diagnostics even if one gate fails; never conceal failed logs.
allow=b/'tmp/v2_preview_allowed.json';d=read(allow);paths={p.relative_to(b).as_posix() for folder in [f,b/'assets_src/imagegen/geologist_river_junctions_v1_20261001'] for p in folder.rglob('*') if p.is_file()}
if isinstance(d,list):d=sorted(set(d)|paths)
else:raise AssertionError('Unexpected allowlist format; no broad fallback')
write(allow,d)
for name,folder in [('job-geology-river-join-study-20261001',f),('job-geology-river-junction-source-20261001',b/'assets_src/imagegen/geologist_river_junctions_v1_20261001')]:
 ip=b/('design/audit_impacts/'+name+'.json');d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in folder.rglob('*') if p.is_file()});write(ip,d)
print('Focused gates captured; exact preview allowlist extended to',len(read(allow)),flush=True)
