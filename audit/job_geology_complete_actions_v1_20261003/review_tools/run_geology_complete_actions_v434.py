from pathlib import Path
import datetime, hashlib, json, os, re, shutil, subprocess, sys, time

R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_geology_complete_actions_v1_20261003'
G=F/'runtime_gate';G.mkdir(exist_ok=True)
ip=R/'design/audit_impacts/job-geology-complete-actions-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
target=F/'review_tools'/Path(__file__).name
shutil.copyfile(Path(__file__),target)
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
commands=[('parser',[py,'-X','utf8','-B','-m','gdtoolkit.parser',str(F/'capture.gd')]),
 ('inference',[py,'-X','utf8','-B','tools/lint_inference.py',str(F/'capture.gd')]),
 ('analyzer',[godot,'--headless','--path',str(R),'--check-only','--script',str(F/'capture.gd')]),
 ('capture1280',[godot,'--path',str(R),'-s',str(F/'capture.gd'),'--','--width=1280','--touch','--classic-touch-test']),
 ('capture1600',[godot,'--path',str(R),'-s',str(F/'capture.gd'),'--','--width=1600','--touch','--classic-touch-test'])]
boundary=read(F/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files']
assert len(boundary)==783 and all(sha(R/r['path'])==r['sha256'] for r in boundary)
for label,command in commands:
 outputs=[G/(label+'.'+s) for s in ['stdout.log','stderr.log','receipt.json']]
 assert not any(p.exists() for p in outputs)
 imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in outputs}|{target.relative_to(R).as_posix()});write(ip,imp)
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 if label.startswith('capture'):
  home=R/'tmp'/('geology_complete_'+label+'_v434');home.mkdir(exist_ok=False)
  for key,folder in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
   p=home/folder;p.mkdir();env[key]=str(p)
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();timer=time.monotonic()
 print('GEOLOGY_COMPLETE_ACTIONS|'+label+'|START',flush=True)
 with outputs[0].open('wb') as out,outputs[1].open('wb') as err:
  result=subprocess.run(command,cwd=R,env=env,stdout=out,stderr=err,timeout=900,creationflags=subprocess.CREATE_NO_WINDOW)
 logs='\n'.join(p.read_text(encoding='utf-8',errors='replace') for p in outputs[:2])
 errors=[l for l in logs.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed|Failed loading resource',l)]
 unchanged=all(sha(R/r['path'])==r['sha256'] for r in boundary)
 passed=result.returncode==0 and not errors and unchanged
 if label.startswith('capture'):
  receipt_path=F/'attempt01'/('CAPTURE_'+label.removeprefix('capture')+'.json')
  passed=passed and 'ALL4_EARNED_LIBRARY_RETURN_AND_DEV_BACK' in logs and receipt_path.exists()
  if receipt_path.exists():
   cap=read(receipt_path)
   passed=passed and all(any(e.get('event')=='complete_work_sequence_recorded' and e.get('from_phase')==phase for e in cap['events']) for phase in [1,2])
 write(outputs[2],{'status':'PASS' if passed else 'FAIL_PRESERVED','command':command,'started_utc':started,
  'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-timer,
  'process_exit':result.returncode,'blocking_diagnostics':errors,'source_count':783,'all_sources_unchanged':unchanged,
  'stdout_sha256':sha(outputs[0]),'stderr_sha256':sha(outputs[1]),
  'qualification':'Scoped actual-input desktop capture/analyzer only. Raw stdout/stderr retained, including unchanged engine diagnostics. No direct visual, owner/device/child, full-suite or acceptance claim.'})
 imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in F.rglob('*') if p.is_file()});imp['validation'].append({'command':' '.join(command),'result':'PASS' if passed else 'FAIL','evidence':outputs[2].relative_to(R).as_posix()});write(ip,imp)
 print('GEOLOGY_COMPLETE_ACTIONS|'+label+'|'+('PASS' if passed else 'FAIL_PRESERVED')+'|'+str(round(time.monotonic()-timer,1))+'s',flush=True)
 if not passed:
  print(logs[-2500:]);sys.exit(1)
checks=[{'path':r['path'],'before_sha256':r['sha256'],'after_sha256':sha(R/r['path']),'match':sha(R/r['path'])==r['sha256']} for r in boundary]
write(F/'BOUNDARY_AFTER_CAPTURE.json',{'status':'PASS_ALL_783_LITERAL_PRODUCTION_BYTES_UNCHANGED','source_checks':checks})
imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in F.rglob('*') if p.is_file()});write(ip,imp)
print('GEOLOGY_COMPLETE_ACTIONS|ALL_SCOPED_GATES_AND_BOTH_CAPTURES_PASS_VISUAL_REVIEW_PENDING',flush=True)
