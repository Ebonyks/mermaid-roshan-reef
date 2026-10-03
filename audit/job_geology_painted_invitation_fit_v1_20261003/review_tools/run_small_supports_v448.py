from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,os,re,sys,time
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=R/'audit/job_geology_painted_invitation_fit_v1_20261003'
F=R/'assets_src/imagegen/geologist_specimen_tray_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json'
G=P/'runtime_gate_small_a3';G.mkdir(exist_ok=False)
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
commands=[('parser',[py,'-X','utf8','-B','-m','gdtoolkit.parser',str(P/'capture.gd'),str(P/'painted_prop_backdrop.gd')]),('inference',[py,'-X','utf8','-B','tools/lint_inference.py',str(P/'capture.gd'),str(P/'painted_prop_backdrop.gd')])]
for filename in ['painted_prop_backdrop.gd','capture.gd']:
 commands.append(('analyzer_'+filename.removesuffix('.gd'),[godot,'--headless','--path',str(R),'--check-only','--script',str(P/filename)]))
for width in [1280,1600]:commands.append(('capture'+str(width),[godot,'--path',str(R),'-s',str(P/'capture.gd'),'--','--width='+str(width),'--touch','--classic-touch-test']))
boundary=read(P/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(boundary)==783
for label,command in commands:
 outputs=[G/(label+'.'+ext) for ext in ['stdout.log','stderr.log','receipt.json']];assert not any(x.exists() for x in outputs)
 d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in outputs});write(ip,d)
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 if label.startswith('capture'):
  home=R/'tmp'/('geology_prop_fit_'+label+'_v448');home.mkdir(exist_ok=False)
  for key,folder in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
   x=home/folder;x.mkdir();env[key]=str(x)
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();print('COUNTERFACTUAL_GEOLOGY_PROPS|'+label+'|START',flush=True)
 with outputs[0].open('wb') as out,outputs[1].open('wb') as err:
  result=subprocess.run(command,cwd=R,env=env,stdout=out,stderr=err,timeout=600,creationflags=subprocess.CREATE_NO_WINDOW)
 logs='\n'.join(x.read_text(encoding='utf-8',errors='replace') for x in outputs[:2])
 errors=[l for l in logs.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed|Failed loading resource',l)]
 unchanged=all(sha(R/x['path'])==x['sha256'] for x in boundary)
 passed=result.returncode==0 and not errors and unchanged
 if label.startswith('capture'):
  passed=passed and 'ALL4_EARNED_LIBRARY_RETURN_AND_DEV_BACK' in logs
  cap=read(P/'attempt03'/('CAPTURE_'+label.removeprefix('capture')+'.json')) if passed else {}
  passed=passed and any(e.get('event')=='NON_RUNTIME_COUNTERFACTUAL_BACKDROP_SUBSTITUTION' for e in cap.get('events',[]))
 write(outputs[2],{'status':'PASS' if passed else 'FAIL_PRESERVED','command':command,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'process_exit':result.returncode,'blocking_diagnostics':errors,'all783_production_sources_unchanged':unchanged,'qualification':'Counterfactual static backdrop fit only, with explicit substitution. Not current production visual/action acceptance, not full suite, not device/child/owner acceptance.','stdout_sha256':sha(outputs[0]),'stderr_sha256':sha(outputs[1])})
 d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in P.rglob('*') if x.is_file()});d['validation'].append({'command':' '.join(command),'result':'PASS' if passed else 'FAIL','evidence':outputs[2].relative_to(R).as_posix()});write(ip,d)
 print('COUNTERFACTUAL_GEOLOGY_PROPS|'+label+'|'+('PASS' if passed else 'FAIL_PRESERVED'),flush=True)
 if not passed:print(logs[-2000:]);sys.exit(1)
print('COUNTERFACTUAL_GEOLOGY_PROPS|SELECTED_BOTH_WIDTHS_MACHINE_COMPLETE_VISUAL_REVIEW_PENDING',flush=True)
