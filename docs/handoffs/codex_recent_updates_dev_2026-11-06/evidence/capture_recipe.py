from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,os,json,hashlib,time,datetime,re
W=Path.cwd();T=Path(__file__).parent;D=T/'recent_merged_native_capture';assert not D.exists(),'Resume actual recorded capture; never duplicate';D.mkdir()
F='assets_src/review/recent_updates_dev_20261106/capture_review.gd';O=W/'assets_src/review/recent_updates_dev_20261106/captures';assert not list(O.glob('*.png'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def git(*a):return subprocess.check_output(['git','-c','core.safecrlf=false',*a],stderr=subprocess.PIPE)
E=Path(subprocess.check_output(['python','-B','tools/resolve_godot.py'],text=True).strip());assert sha(E.read_bytes())=='c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbe846643'
paths=sorted(p for p in git('ls-files','-z','--','scripts','assets','scenes','shaders','addons','project.godot','export_presets.cfg').decode().split('\0')if p)
with ThreadPoolExecutor(max_workers=4)as pool:before=dict(pool.map(lambda p:(p,sha((W/p).read_bytes())),paths))
fixture_sha=sha((W/F).read_bytes());np=json.loads((T/'NORMAL_SAVE_PIN.json').read_text());nb=Path(np['normal_base'])
def normals():return{s:sha(Path(str(nb)+s).read_bytes())if Path(str(nb)+s).is_file()else'absent'for s in np['hashes']}
normal_before=normals();wr(D/'SOURCE_PIN.json',dict(runtime_hashes=before,fixture=F,fixture_sha256=fixture_sha,engine_sha256=sha(E.read_bytes()),normal_before=normal_before))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
 q=D/key;q.mkdir();env[key]=str(q)
command=[str(E),'--path',str(W),'--rendering-method','mobile','--display-driver','windows','--audio-driver','Dummy','--log-file',str(D/'native_engine.log'),'-s','res://'+F]
with(D/'console.log').open('wb')as log:
 proc=subprocess.Popen(command,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
 wr(T/'RECENT_CAPTURE_STATE.json',dict(stage='RUNNING_NATIVE_CAPTURE',pid=proc.pid,command=command,source_pin=str(D/'SOURCE_PIN.json'),fixture_sha256=fixture_sha,started_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 try:rc=proc.wait(timeout=240)
 except subprocess.TimeoutExpired:
  wr(T/'RECENT_CAPTURE_STATE.json',dict(stage='TIMED_OUT_INSPECT_OWN_CAPTURE',pid=proc.pid,fixture_sha256=fixture_sha));raise
text=(D/'console.log').read_text(encoding='utf-8',errors='replace')
assert rc==0,(rc,text[-3000:]);assert not re.search(r'SCRIPT ERROR|Parse Error|Assertion failed|ERROR:',text),text[-3000:]
rows=json.loads((O/'captures.json').read_text());profile=json.loads((O/'profile.json').read_text());assert len(rows)==17
assert profile['renderer']=='mobile'and profile['display']=='Windows'and profile['frame_cap']==30 and profile['canvas_size']==[1280,720]and profile['window_size']==[1280,720]
assert profile['version']['major']==4 and profile['version']['minor']==7 and profile['version']['patch']==2
for row in rows:
 assert row['size']==[1280,720]and row['save_error']==0 and row['renderer']=='mobile'
 assert sha((O/row['file']).read_bytes())==row['sha256']
assert sum(r['quality_context']=='speedy'for r in rows)==1
assert sum(r['quality_context']=='fixed_pc_no_quality_selector'for r in rows)==16
with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda p:(p,sha((W/p).read_bytes())),paths))
assert before==after,'Runtime source drift during native capture';assert normals()==normal_before;assert sha((W/F).read_bytes())==fixture_sha
result=dict(state='PASS17_ACTUAL_MERGED_MOBILE_NATIVE_DIAGNOSTIC_FRAMES',exit_code=rc,frame_count=17,profile=profile,fixture_sha256=fixture_sha,runtime_input_count=len(paths),runtime_drift=[],normal_save_unchanged=True,console_sha256=sha((D/'console.log').read_bytes()),native_engine_log_sha256=sha((D/'native_engine.log').read_bytes()),formal_QA11=None,natural_route_acceptance=None,device=None,child=None,owner=None,accepted_removed=0,limits='Posed diagnostic views; PC fixed renderer has no quality selector, Opera explicitlySpeedy. 30fps cap is configured, not a physical device performance measurement. None is generation pixels or formalQA11.')
wr(D/'RESULT.json',result);wr(T/'RECENT_CAPTURE_STATE.json',dict(stage='TERMINAL_PASS',result=str(D/'RESULT.json'),frame_count=17));print(json.dumps(dict(state=result['state'],frames=17,runtime_drift=[],normal_save_unchanged=True)),flush=True)
