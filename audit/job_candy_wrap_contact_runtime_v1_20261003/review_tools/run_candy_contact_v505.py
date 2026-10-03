from pathlib import Path
import json,hashlib,datetime,shutil,subprocess,os,sys,re,time
B=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');D=B/'audit/job_candy_wrap_contact_runtime_v1_20261003';C=B/'audit/job_candy_workflow_current_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
a=sys.argv[1] if len(sys.argv)>1 else '01';G=D/('runtime_gate_a'+a);G.mkdir(exist_ok=False);shutil.copyfile(Path(__file__),D/'review_tools'/Path(__file__).name)
py=r'C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot=r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
commands=[]
for key in ['contact_surface','capture']:
 commands.extend([(key+'_parser',[py,'-X','utf8','-B','-m','gdtoolkit.parser',str(D/(key+'.gd'))]),(key+'_inference',[py,'-X','utf8','-B','tools/lint_inference.py',str(D/(key+'.gd'))]),(key+'_analyzer',[godot,'--headless','--path',str(B),'--check-only','--script',str(D/(key+'.gd'))])])
for width in [1280,1600]:commands.append(('training_'+str(width),[godot,'--path',str(B),'-s',str(D/'capture.gd'),'--','--width='+str(width),'--touch','--classic-touch-test']))
boundary=read(C/'SOURCE_CURRENT_A3_BEFORE_CAPTURE.json')['source_files'];ip=B/'design/audit_impacts/job-candy-workflow-current-20261003.json'
for label,command in commands:
 paths=[G/(label+'.'+s) for s in ['stdout.log','stderr.log','receipt.json']]
 impact=read(ip);impact['files']=sorted(set(impact['files'])|{str(p.relative_to(B)).replace('\\','/') for p in paths}|{p.relative_to(B).as_posix() for p in (D/'review_tools').glob('*')});write(ip,impact)
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 if label.startswith('training'):
  home=B/'tmp'/('candy_contact_v505_a'+a+'_'+label);home.mkdir(exist_ok=False)
  for key,folder in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
   p=home/folder;p.mkdir();env[key]=str(p)
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();print('CANDY_CONTACT|'+label+'|START',flush=True)
 with paths[0].open('wb') as out, paths[1].open('wb') as err:
  process=subprocess.Popen(command,cwd=B,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
  while process.poll() is None:
   time.sleep(0.5);logs='\n'.join(p.read_text(encoding='utf-8',errors='replace') for p in paths[:2])
   if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed',logs) or time.monotonic()-t>600:
    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW);break
  code=process.wait()
 logs='\n'.join(p.read_text(encoding='utf-8',errors='replace') for p in paths[:2]);errors=[l for l in logs.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed|Failed loading resource|Unable to convert a value|\bFAIL\b',l)]
 unchanged=all(sha(B/x['path'])==x['sha256'] for x in boundary);passed=code==0 and not errors and unchanged
 if label.startswith('training'):
  cap_path=D/('attempt'+a)/('CAPTURE_'+label+'.json');cap=read(cap_path) if cap_path.exists() else {}
  passed=passed and 'ALL_PHASES_EARNED_RETURN_AND_CIRCLE_CAPTURE' in logs and {e.get('phase') for e in cap.get('events',[]) if e.get('event')=='intentional_phase_completed'}==set(range(4)) and len(cap.get('motion_frames',[]))>100
 write(paths[2],{'status':'PASS' if passed else 'FAIL_PRESERVED','command':command,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'process_exit':code,'blocking_diagnostics':errors,'all783_declared_source_hashes_unchanged':unchanged,'qualification':'Explicit non-runtime drawing/contact substitution; original input/geometry/state and earned callbacks. Machine result never implies source/whole action/device/child/owner acceptance.','stdout_sha256':sha(paths[0]),'stderr_sha256':sha(paths[1])})
 impact=read(ip);impact['files']=sorted(set(impact['files'])|{p.relative_to(B).as_posix() for p in D.rglob('*') if p.is_file()});impact['validation'].append({'command':' '.join(command),'result':'PASS' if passed else 'FAIL','evidence':paths[2].relative_to(B).as_posix()});write(ip,impact)
 print('CANDY_CONTACT|'+label+'|'+('PASS' if passed else 'FAIL_PRESERVED')+'|'+str(round(time.monotonic()-t,1))+'s',flush=True)
 if not passed:print(logs[-2500:]);sys.exit(1)
print('CANDY_CONTACT|ALL_CHECKS_COMPLETE_VISUAL_REVIEW_PENDING',flush=True)
