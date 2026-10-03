from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,os,re,sys,time
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
J=R/'audit/job_geology_fossil_reveal_continuity_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-geology-fossil-reveal-continuity-20261003.json'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='c5977ebb29bb2011b20fc149ad350290f045045c'
# Correct the inherited fixture labels before execution; no capture existed.
c=J/'capture.gd';s=c.read_text(encoding='utf-8-sig');s=s.replace('ACTUAL_LIBRARY_COMPLETE_FOSSIL_PAN_ALL4_EARNED_RETURN_AND_DEV_ENTRY_CAPTURED_REVIEW_PENDING','COUNTERFACTUAL_DRAW_ONLY_COMPLETE_FOSSIL_ALL4_EARNED_RETURN_REVIEW_PENDING').replace('Every input/wait frame of phases 1 and 2 captured','Every input/wait frame of phase1 fossil captured; pan receives selected views only');c.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),J/'review_tools'/Path(__file__).name)
# Initial preparation and A1 runner remain preserved separately.
G=J/'runtime_gate_a1';G.mkdir(exist_ok=False)
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
commands=[('parser',[py,'-X','utf8','-B','-m','gdtoolkit.parser',str(J/'capture.gd'),str(J/'reveal_surface.gd')]),('inference',[py,'-X','utf8','-B','tools/lint_inference.py',str(J/'capture.gd'),str(J/'reveal_surface.gd')])]
for filename in ['reveal_surface.gd','capture.gd']:commands.append(('analyzer_'+filename.removesuffix('.gd'),[godot,'--headless','--path',str(R),'--check-only','--script',str(J/filename)]))
for width in [1280,1600]:commands.append(('capture'+str(width),[godot,'--path',str(R),'-s',str(J/'capture.gd'),'--','--width='+str(width),'--touch','--classic-touch-test']))
boundary=read(J/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(boundary)==783
for label,command in commands:
 outputs=[G/(label+'.'+ext) for ext in ['stdout.log','stderr.log','receipt.json']];assert not any(x.exists() for x in outputs)
 d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in outputs}|{x.relative_to(R).as_posix() for x in (J/'review_tools').glob('*.py')});write(ip,d)
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 if label.startswith('capture'):
  home=R/'tmp'/('geology_fracture_'+label+'_v478');home.mkdir(exist_ok=False)
  for key,folder in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
   x=home/folder;x.mkdir();env[key]=str(x)
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();print('PAINTED_FRACTURE|'+label+'|START',flush=True)
 with outputs[0].open('wb') as out,outputs[1].open('wb') as err:result=subprocess.run(command,cwd=R,env=env,stdout=out,stderr=err,timeout=900,creationflags=subprocess.CREATE_NO_WINDOW)
 logs='\n'.join(x.read_text(encoding='utf-8',errors='replace') for x in outputs[:2])
 errors=[l for l in logs.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed|Failed loading resource|Unable to convert a value',l)]
 unchanged=all(sha(R/x['path'])==x['sha256'] for x in boundary)
 passed=result.returncode==0 and not errors and unchanged
 if label.startswith('capture'):
  cap_path=J/'attempt01'/('CAPTURE_'+label.removeprefix('capture')+'.json')
  cap=read(cap_path) if cap_path.exists() else {}
  passed=passed and 'ALL4_EARNED_LIBRARY_RETURN_AND_DEV_BACK' in logs and any(e.get('event')=='NON_RUNTIME_FOSSIL_REVEAL_HOME_PLACEMENT_SUBSTITUTION' for e in cap.get('events',[]))
  passed=passed and {e.get('phase_index') for e in cap.get('events',[]) if e.get('event')=='intentional_completed'}=={0,1,2,3}
  passed=passed and any(e.get('event')=='complete_work_sequence_recorded' and e.get('from_phase')==1 for e in cap.get('events',[]))
 write(outputs[2],{'status':'PASS' if passed else 'FAIL_PRESERVED','command':command,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'process_exit':result.returncode,'blocking_diagnostics':errors,'all783_production_sources_unchanged':unchanged,'qualification':'Explicit non-runtime reveal/home placement study; homes intentionally changed, original material/input/targets/state/progress and actual world callbacks inherited. Not production visual/action acceptance or full suite or device/child/owner acceptance.','stdout_sha256':sha(outputs[0]),'stderr_sha256':sha(outputs[1])})
 d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in J.rglob('*') if x.is_file()});d['validation'].append({'command':' '.join(command),'result':'PASS' if passed else 'FAIL','evidence':outputs[2].relative_to(R).as_posix()});write(ip,d)
 print('PAINTED_FRACTURE|'+label+'|'+('PASS' if passed else 'FAIL_PRESERVED')+'|'+str(round(time.monotonic()-t,1))+'s',flush=True)
 if not passed:print(logs[-2200:]);sys.exit(1)
print('PAINTED_FRACTURE|BOTH_ACTUAL_INPUT_ROUTES_MACHINE_COMPLETE_VISUAL_REVIEW_PENDING',flush=True)
