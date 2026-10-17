from pathlib import Path
import subprocess,json,hashlib,datetime,os,shutil,re,sys
T=Path.cwd(); P=Path(__file__).resolve().parent; S=Path(os.environ['R83_JOB_ROOT']); width=int(sys.argv[1]); assert width in (1280,1600)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
pin=json.loads((S/'SOURCE_PIN.json').read_text(encoding='utf-8')); assert all(sha(T/p)==v for p,v in pin['runtime_hashes'].items())
normal=Path(os.environ['R83_NORMAL_PATH'])
def normals():return {x:sha(Path(str(normal)+x)) if Path(str(normal)+x).is_file() else 'absent' for x in pin['normal_save_hashes_before']}
G=subprocess.check_output(['python','-B','tools/resolve_godot.py'],text=True).strip(); name='actual_source_'+str(width); job=S/name; job.mkdir(exist_ok=False); dest=P/'native'/name; dest.mkdir(parents=True,exist_ok=False)
fixture=P/'capture_entry.gd'; target=T/'export/flat_vector_r83/capture_entry.gd'; assert fixture.read_bytes()==target.read_bytes(); before=normals()
env=dict(os.environ,APPDATA=str(job/'roaming'),LOCALAPPDATA=str(job/'local'),XDG_DATA_HOME=str(job/'data'),XDG_CONFIG_HOME=str(job/'config'),R83_OUT=str(job/'output'),R83_WIDTH=str(width),R83_REV=pin['baseline'],R83_PRIVATE_NAME='mermaid-roshan-r83-'+name.replace('_','-')+'-20261016')
for key in ('APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME'):Path(env[key]).mkdir()
syntax=[]
for cmd in [['python','-B','-m','gdtoolkit.parser',str(fixture)],['python','-B','tools/lint_inference.py',str(fixture)],[G,'--headless','--path',str(T),'--check-only','--script','res://export/flat_vector_r83/capture_entry.gd']]:
 q=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,creationflags=0x08000000);syntax.append({'command':cmd,'exit_code':q.returncode,'output':q.stdout.decode(errors='replace'),'sha256':hashlib.sha256(q.stdout).hexdigest()})
wr(dest/'SYNTAX.json',{'checks':syntax});assert all(x['exit_code']==0 for x in syntax),syntax
cmd=[G,'--path',str(T),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--script','res://export/flat_vector_r83/capture_entry.gd']
wr(dest/'LAUNCH.json',{'command':cmd,'baseline':pin['baseline'],'runtime_pin_sha256':sha(S/'SOURCE_PIN.json'),'touch_ui_sha256':sha(T/'scripts/touch_ui.gd'),'fixture_sha256':sha(fixture),'normal_before':before,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'isolation':'Private APPDATA/LOCALAPPDATA/XDG before engine startup plus unique custom user name before Main. No normal saves parsed/copied/restored.','scope':'Actual runtime trial source, read-only observer with no material/controller/game/timer override; not origin/dev or accepted replacement.'})
with(dest/'engine.log').open('wb')as log:
 try:q=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=900);code=q.returncode;timed=False
 except subprocess.TimeoutExpired:code=None;timed=True
out=job/'output'
for f in [out/'capture_manifest.json',*out.glob('*.png')]:
 if f.is_file():shutil.copyfile(f,dest/f.name)
raw=(dest/'engine.log').read_bytes(); after=normals(); changed=[p for p,v in pin['runtime_hashes'].items() if sha(T/p)!=v]
res={'exit_code':code,'timed_out':timed,'normal_before':before,'normal_after':after,'normal_unchanged':before==after,'runtime_source_changes':changed,'fixture_unchanged':sha(fixture)==sha(target),'log_sha256':hashlib.sha256(raw).hexdigest(),'script_or_shader_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw)),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};wr(dest/'RESULT.json',res)
print('R83_NATIVE',width,'exit',code,'normal_exact',before==after,'runtime_exact',not changed,'\n'+raw.decode(errors='replace')[-1200:],flush=True)
assert code==0 and not timed and before==after and not changed and res['fixture_unchanged'] and not res['script_or_shader_errors']
assert json.loads((dest/'capture_manifest.json').read_text())['observer_status']=='PASS'
