from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,time
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
staging=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930/tmp')
out=r/'audit/job_vector_mount_review_v1_20261001'
assert (out/'PROFILE.json').exists() and not (out/'capture.gd').exists()
shutil.copyfile(staging/'capture_vector_mount_v86.gd',out/'capture.gd')
shutil.copyfile(__file__,out/'executed_run_vector_mount_v86.py')
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def rel(p):return p.relative_to(r).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
impact=r/'design/audit_impacts/job-vector-mounted-review-20261001.json'
data=json.loads(impact.read_text(encoding='utf-8'))
data['files']=sorted(set(data['files'])|{rel(p) for p in out.rglob('*') if p.is_file()})
write(impact,data)
profile=json.loads((out/'PROFILE.json').read_text(encoding='utf-8'))
before={x['source_path']:sha(r/x['source_path']) for x in profile['sources']}
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
commands=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',rel(out/'capture.gd')]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',rel(out/'capture.gd')]),('analyzer',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+rel(out/'capture.gd')]),('native',[godot,'--path',str(r),'--script','res://'+rel(out/'capture.gd')])]
rows=[]
for name,cmd in commands:
 start=time.monotonic()
 with (out/(name+'.stdout.log')).open('wb') as so,(out/(name+'.stderr.log')).open('wb') as se:
  try:p=subprocess.run(cmd,cwd=r,stdout=so,stderr=se,timeout=900 if name=='native' else 240,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timeout=False
  except subprocess.TimeoutExpired:code=None;timeout=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timeout,seconds=time.monotonic()-start,stdout=rel(out/(name+'.stdout.log')),stderr=rel(out/(name+'.stderr.log'))))
 print(name,code,flush=True)
 if code!=0:
  print((out/(name+'.stdout.log')).read_text(encoding='utf-8',errors='replace')[-1800:],(out/(name+'.stderr.log')).read_text(encoding='utf-8',errors='replace')[-3500:],flush=True);break
after={p:sha(r/p) for p in before}
passed=len(rows)==len(commands) and all(x['process_exit']==0 for x in rows) and before==after
write(out/'PROCESS_RECEIPT.json',dict(status='PASS_NATIVE_VECTOR_MOUNT_CAPTURE' if passed else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=rows,original_source_hashes_unchanged=before==after,original_source_hashes=after,qualification='Machine capture only. Individual native source-to-context opinions,50px room crest, whole career/story/action/device/child/owner remain unassigned.'))
data=json.loads(impact.read_text(encoding='utf-8'));data['files']=sorted(set(data['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});data['validation'].append(dict(command='Official4.7.2 parser/inference/analyzer/native phase-fixture capture',result='PASS' if passed else 'FAIL',evidence=rel(out/'PROCESS_RECEIPT.json')));write(impact,data)
raise SystemExit(0 if passed else 1)
