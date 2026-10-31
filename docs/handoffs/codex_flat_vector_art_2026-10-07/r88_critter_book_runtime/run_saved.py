from pathlib import Path
import json,subprocess,hashlib,os,shutil,datetime,re,sys
T=Path('C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef'); P=Path(__file__).resolve().parent; S=Path(os.environ['R88_JOB_ROOT']); A=Path('C:/Users/Peter/.codex/worktrees/flat-vector-r6-20261012/mermaid-roshan-reef'); H=A/'docs/handoffs/codex_flat_vector_art_2026-10-07'; pin=json.loads((P/'CANDIDATE_SOURCE_PIN.json').read_text(encoding="utf-8-sig")); width=int(sys.argv[1]); assert width in [1280,1600]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=T,text=True).strip()==pin['baseline']
assert subprocess.check_output(['git','branch','--show-current'],cwd=T,text=True).strip()=='codex/flat-vector-critter-book-runtime-20261017'
def changes(key):return [p for p,v in pin[key].items()if not(T/p).is_file()or sha(T/p)!=v]
assert not changes('runtime_hashes')and not changes('sidecars')
pre=json.loads((H/'r77_intro_entry_ownership/USERDIR_PREFLIGHT.json').read_text(encoding='utf-8')); normal=Path(json.loads(next(x['output']for x in pre['checks']if'R77_USERDIR_PREFLIGHT|'in x['output']).split('R77_USERDIR_PREFLIGHT|',1)[1].strip())['normal_path'])
suffixes=['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.tmp','.before_new_game.old']
def normals():return {x:sha(Path(str(normal)+x))if Path(str(normal)+x).is_file()else'absent'for x in suffixes}
G=subprocess.check_output(['python','-B','tools/resolve_godot.py'],cwd=T,text=True).strip(); name=os.environ.get('R88_ATTEMPT','attempt3')+'_saved_'+os.environ['R88_SAVED_MODE']+'_'+str(width); job=S/name; job.mkdir(exist_ok=False);dest=P/'native'/name;dest.mkdir(parents=True,exist_ok=False);fixture=P/'capture_saved.gd';executed=T/'export/flat_vector_r88/capture_saved.gd';assert fixture.read_bytes()==executed.read_bytes()
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',R88_WIDTH=str(width),R88_OUT=str(job/'output'),R88_REV=pin['baseline'],R88_PRIVATE_NAME='mermaid-roshan-r88-critter-'+str(width)+'-20261017',R88_CODE_SHA256=sha(T/'scripts/collection_system.gd'))
for key,sub in [('APPDATA','roaming'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:env[key]=str(job/sub);Path(env[key]).mkdir()
checks=[]
for cmd in [['python','-B','-m','gdtoolkit.parser',str(fixture)],['python','-B','tools/lint_inference.py',str(fixture)],[G,'--headless','--path',str(T),'--check-only','--script','res://export/flat_vector_r88/capture_saved.gd']]:
 q=subprocess.run(cmd,cwd=T,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,creationflags=0x08000000);checks.append({'command':cmd,'exit_code':q.returncode,'output':q.stdout.decode(errors='replace'),'sha256':hashlib.sha256(q.stdout).hexdigest()})
wr(dest/'SYNTAX.json',{'checks':checks});assert all(x['exit_code']==0 for x in checks),checks
before=normals();cmd=[G,'--path',str(T),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--script','res://export/flat_vector_r88/capture_saved.gd'];wr(dest/'LAUNCH.json',{'command':cmd,'source_revision':pin['baseline'],'integration_baseline':pin['baseline'],'runtime_pin_sha256':sha(P/'CANDIDATE_SOURCE_PIN.json'),'fixture_sha256':sha(fixture),'normal_before':before,'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Actual original caller on currentN plus declared book constructor; natural private entry, categories/held/repeat/Back/reentry. No fixture visual/route/time/save override or new art. All frames excluded from currentDev coverage and acceptance.','isolation':'Private APPDATA/XDG before engine plus fresh custom namespace before Main; actual normal eleven names hashed only.'})
print('R88_NATIVE_BEGIN',width,flush=True)
with(dest/'engine.log').open('wb')as log:
 try:q=subprocess.run(cmd,cwd=T,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=900);code=q.returncode;timed=False
 except subprocess.TimeoutExpired:code=None;timed=True
out=job/'output'
for f in [out/'capture_manifest.json',*out.glob('*.png')]:
 if f.is_file():shutil.copyfile(f,dest/f.name)
raw=(dest/'engine.log').read_bytes();r={'exit_code':code,'timed_out':timed,'normal_before':before,'normal_after':normals(),'runtime_source_changes':changes('runtime_hashes'),'sidecar_changes':changes('sidecars'),'fixture_unchanged':sha(fixture)==sha(executed),'script_or_shader_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw)),'log_sha256':hashlib.sha256(raw).hexdigest(),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};wr(dest/'RESULT.json',r);print('R88_NATIVE_DONE',width,code,'\n'+raw.decode(errors='replace')[-1400:],flush=True);assert code==0 and not timed and before==r['normal_after']and not r['runtime_source_changes']and not r['sidecar_changes']and r['fixture_unchanged']and not r['script_or_shader_errors']
report=json.loads((dest/'capture_manifest.json').read_text(encoding="utf-8-sig"));assert report['observer_status']=='PASS';assert len(report['states'])>=14
assert report['expected_caught'] in [6,18] and report['saved_mode'] in ['partial','full']
print('R88_SAVED_CONSUMER_PASS',width,report['saved_mode'],'checks',len(report['checks']),'frames',len(report['states']),flush=True)
