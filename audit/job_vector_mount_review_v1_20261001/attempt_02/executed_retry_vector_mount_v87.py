from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,time
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
parent=r/'audit/job_vector_mount_review_v1_20261001'
previous=json.loads((parent/'PROCESS_RECEIPT.json').read_text(encoding='utf-8'))
assert previous['status']=='FAIL_PRESERVED' and previous['processes'][-1]['process_exit']==4294967295
assert len(list((r/'tmp/vector_mount_v86/native_views').glob('*.webp')))==0
out=parent/'attempt_02';assert not out.exists();out.mkdir()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def rel(p):return p.relative_to(r).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
shutil.copyfile(__file__,out/'executed_retry_vector_mount_v87.py')
code=(parent/'capture.gd').read_text(encoding='utf-8')
old='\t\t\tvar names: Array[String] = ["PATTERN", "COUNT", "ADD", "MATCH"] \\\n\t\t\t\tif career == "teacher" else ["RIVER", "FOSSIL", "PAN", "GEODE"]'
assert old in code
new='\t\t\tvar names: Array[String] = []\n\t\t\tif career == "teacher":\n\t\t\t\tnames.assign(["PATTERN", "COUNT", "ADD", "MATCH"])\n\t\t\telse:\n\t\t\t\tnames.assign(["RIVER", "FOSSIL", "PAN", "GEODE"])'
code=code.replace(old,new).replace('tmp/vector_mount_v86/native_views','tmp/vector_mount_v87/native_views')
(out/'capture.gd').write_text(code,encoding='utf-8',newline='\n')
write(out/'PREPARATION.json',dict(status='CORRECTED_DISPOSABLE_FIXTURE_PREPARED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),failure='Runtime typed Array[String] assignment from conditional untyped array; original failed source/process logs preserved at parent,0captures.',original_capture=rel(parent/'capture.gd'),original_capture_sha256=sha(parent/'capture.gd'),corrected_capture=rel(out/'capture.gd'),corrected_capture_sha256=sha(out/'capture.gd'),modification='Use explicit Array[String].assign for each unchanged4-name phase list; separate native output directory. No game code, object source, score, phase selection, input, reward guard or gate changes.',failed_process_stop='Only verified failed Godot capture PID47904 stopped; wrapper recorded actual4294967295 exit, no synthetic pass.'))
profile=json.loads((parent/'PROFILE.json').read_text(encoding='utf-8'))
before={x['source_path']:sha(r/x['source_path']) for x in profile['sources']}
impact=r/'design/audit_impacts/job-vector-mounted-review-20261001.json'
d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(impact,d)
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
after={p:sha(r/p) for p in before};passed=len(rows)==len(commands) and all(x['process_exit']==0 for x in rows) and before==after
write(out/'PROCESS_RECEIPT.json',dict(status='PASS_NATIVE_VECTOR_MOUNT_CAPTURE' if passed else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=rows,original_source_hashes_unchanged=before==after,original_source_hashes=after,qualification='Machine capture only. Original typed-array failure remains preserved. Native context grades,50px crest, complete career/story/action/device/child/owner remain unassigned.'))
d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{rel(p) for p in parent.rglob('*') if p.is_file()});d['validation'].append(dict(command='Corrected official4.7.2 native fixture retry with unchanged sources/guards',result='PASS' if passed else 'FAIL',evidence=rel(out/'PROCESS_RECEIPT.json')));write(impact,d)
raise SystemExit(0 if passed else 1)
