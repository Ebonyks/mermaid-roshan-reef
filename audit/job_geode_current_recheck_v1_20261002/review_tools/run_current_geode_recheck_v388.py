from pathlib import Path
import datetime,hashlib,json,os,re,shutil,subprocess,sys,time
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_geode_current_recheck_v1_20261002';G=F/'runtime_gate';G.mkdir(exist_ok=True)
ip=R/'design/audit_impacts/job-geode-current-recheck-20261002.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
label=sys.argv[1];action=label.split('_')[0]
commands={'parser':[py,'-X','utf8','-B','-m','gdtoolkit.parser',str(F/'capture.gd')],'inference':[py,'-X','utf8','-B','tools/lint_inference.py',str(F/'capture.gd')],'analyzer':[godot,'--headless','--path',str(R),'--check-only','--script',str(F/'capture.gd')],'capture1280':[godot,'--path',str(R),'-s',str(F/'capture.gd'),'--','--width=1280','--touch','--classic-touch-test'],'capture1600':[godot,'--path',str(R),'-s',str(F/'capture.gd'),'--','--width=1600','--touch','--classic-touch-test']}
assert action in commands
target=F/'review_tools'/Path(__file__).name
if Path(__file__).resolve()!=target.resolve():shutil.copyfile(Path(__file__),target)
outputs=[G/(label+'.'+n) for n in ['stdout.log','stderr.log','receipt.json']];assert not any(p.exists() for p in outputs)
imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in outputs}|{target.relative_to(R).as_posix()});write(ip,imp)
boundary=read(F/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(boundary)==783 and all(sha(R/r['path'])==r['sha256'] for r in boundary)
env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
if action.startswith('capture'):
 home=R/'tmp'/('geode_current_'+label+'_v388');home.mkdir(exist_ok=False)
 for key,folder in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
  p=home/folder;p.mkdir();env[key]=str(p)
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with outputs[0].open('wb') as out,outputs[1].open('wb') as err:
 result=subprocess.run(commands[action],cwd=R,env=env,stdout=out,stderr=err,timeout=360,creationflags=subprocess.CREATE_NO_WINDOW)
logs='\n'.join(p.read_text(encoding='utf-8',errors='replace') for p in outputs[:2]);errors=[l for l in logs.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed|Failed loading resource',l)]
checks=[{'path':r['path'],'before_sha256':r['sha256'],'after_sha256':sha(R/r['path']),'match':sha(R/r['path'])==r['sha256']} for r in boundary]
passed=result.returncode==0 and not errors and all(r['match'] for r in checks)
if action.startswith('capture'):passed=passed and 'ALL4_EARNED_LIBRARY_RETURN_AND_DEV_BACK' in logs
write(outputs[2],{'status':'PASS' if passed else 'FAIL_PRESERVED','command':commands[action],'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'process_exit':result.returncode,'blocking_diagnostics':errors,'source_count':783,'all_sources_unchanged':all(r['match'] for r in checks),'source_checks':checks,'stdout_sha256':sha(outputs[0]),'stderr_sha256':sha(outputs[1]),'qualification':'Scoped capture/analyzer/source evidence only. All current native images need direct review; no visual, physical-device, child, owner or full-suite acceptance.'})
imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in F.rglob('*') if p.is_file()});imp['validation'].append({'command':' '.join(commands[action]),'result':'PASS' if passed else 'FAIL','evidence':outputs[2].relative_to(R).as_posix()});write(ip,imp)
print('CURRENT_GEODE_RECHECK|'+label+'|'+('PASS' if passed else 'FAIL_PRESERVED')+'|783 unchanged|'+str(round(time.monotonic()-t,1))+'s',flush=True)
if not passed:print(logs[-3000:])
sys.exit(0 if passed else 1)
