from pathlib import Path
import json,hashlib,datetime,shutil,subprocess,os,sys,re,time
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');C=R/'audit/job_candy_workflow_current_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='c5977ebb29bb2011b20fc149ad350290f045045c'
shutil.copyfile(Path(__file__),C/'review_tools'/Path(__file__).name)
G=C/'runtime_gate_entry';G.mkdir(exist_ok=False)
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
commands=[('parser',[py,'-X','utf8','-B','-m','gdtoolkit.parser',str(C/'capture_entry_diagnostic.gd')]),('inference',[py,'-X','utf8','-B','tools/lint_inference.py',str(C/'capture_entry_diagnostic.gd')]),('analyzer_capture',[godot,'--headless','--path',str(R),'--check-only','--script',str(C/'capture_entry_diagnostic.gd')])]
for lane in ('story',):
 for width in (1280,1600):commands.append((f'{lane}_{width}',[godot,'--path',str(R),'-s',str(C/'capture_entry_diagnostic.gd'),'--',f'--width={width}','--touch','--classic-touch-test']+(['--story'] if lane=='story' else [])))
boundary=read(C/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(boundary)==783
ip=R/'design/audit_impacts/job-candy-workflow-current-20261003.json'
for label,command in commands:
 outputs=[G/(label+'.'+x) for x in ('stdout.log','stderr.log','receipt.json')];assert not any(x.exists() for x in outputs)
 d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in outputs}|{x.relative_to(R).as_posix() for x in (C/'review_tools').glob('*') if x.is_file()});write(ip,d)
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 if label.startswith(('training','story')):
  home=R/'tmp'/('candy_v491_'+label);home.mkdir(exist_ok=False)
  for key,folder in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
   x=home/folder;x.mkdir();env[key]=str(x)
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();print('CANDY_WORKFLOW|'+label+'|START',flush=True)
 with outputs[0].open('wb') as out,outputs[1].open('wb') as err:
  process=subprocess.Popen(command,cwd=R,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
  while process.poll() is None:
   time.sleep(0.5)
   current='\n'.join(x.read_text(encoding='utf-8',errors='replace') for x in outputs[:2])
   if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed',current) or time.monotonic()-t>600:
    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
    break
  result=subprocess.CompletedProcess(command,process.wait())
 logs='\n'.join(x.read_text(encoding='utf-8',errors='replace') for x in outputs[:2]);errors=[l for l in logs.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed|Failed loading resource|Unable to convert a value',l)]
 unchanged=all(sha(R/x['path'])==x['sha256'] for x in boundary);passed=result.returncode==0 and not errors and unchanged
 if label.startswith('story'):
  cap=read(C/'entry_diagnostic'/('ENTRY_'+label.split('_')[1]+'.json'))
  passed=passed and 'NO_MAPPED_STATION_REPRODUCED' in logs and cap['armed_station']==-1 and not cap['station_for_phase'] and not cap['state']['task_open']
 write(outputs[2],{'status':'PASS' if passed else 'FAIL_PRESERVED','command':command,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'process_exit':result.returncode,'blocking_diagnostics':errors,'all783_production_sources_unchanged':unchanged,'qualification':'Current unmodified runtime route and input. Selected remaining-phase evidence, complete circle only. Explicit isolated entry/prerequisite save fixture. Not visual/device/child/owner acceptance.','stdout_sha256':sha(outputs[0]),'stderr_sha256':sha(outputs[1])})
 d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in C.rglob('*') if x.is_file()});d['validation'].append({'command':' '.join(command),'result':'PASS' if passed else 'FAIL','evidence':outputs[2].relative_to(R).as_posix()});write(ip,d)
 print('CANDY_WORKFLOW|'+label+'|'+('PASS' if passed else 'FAIL_PRESERVED')+'|'+str(round(time.monotonic()-t,1))+'s',flush=True)
 if not passed:print(logs[-3500:]);sys.exit(1)
print('CANDY_WORKFLOW|UNMODIFIED_STORY_ENTRY_DIAGNOSTIC_REPRODUCED_NOT_ACTION_ACCEPTANCE',flush=True)
