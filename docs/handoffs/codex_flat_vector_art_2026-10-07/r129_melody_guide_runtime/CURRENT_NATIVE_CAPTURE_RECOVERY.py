from pathlib import Path
import json,hashlib,subprocess,os,re,datetime
U=Path.cwd();S=Path(__file__).parent;P=U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r129_melody_guide_runtime';N=S/'candidate_native_recovery1';E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(n,**kw):wr(S/'NATIVE_RECOVERY_STATE.json',dict(state=n,at_utc=now(),**kw))
assert not N.exists(),'Resume exact existing operation'
old=S/'candidate_native/SOURCE_PIN.json';pin=rd(old);assert rd(S/'candidate_import/FINAL_RESULT.json')['state']=='PASS_NEW_GUIDE_LOSSLESS_MIPMAPS_NO_VRAM'
assert all(sha(U/p)==h for p,h in pin['runtime_hashes'].items())and sha(E)==pin['engine_sha256']and sha(P/'capture_guide.gd')==pin['fixture_sha256']
assert (U/'export/flat_vector_r129/capture_guide.gd').read_bytes()==(P/'capture_guide.gd').read_bytes()
N.mkdir();wr(N/'SOURCE_PIN.json',pin);normal=Path(rd(U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'])
def normals():return{n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in pin['normal_before']}
assert normals()==pin['normal_before'];cases=[]
wr(N/'RECOVERY.json',dict(reason='Failed launcher referenced export/flat_vector_r128/capture_guide.gd. Correct only the launcher path to the existing exactR129fixture. Both healthy imports reused; same all5068source inputs and fixture bytes. No prior native PNGs existed.',failed_session=53217,healthy_import_result_sha256=sha(S/'candidate_import/FINAL_RESULT.json'),original_source_pin_sha256=sha(old),generation_calls_added=0,technical_reexports=0,excluded_native_frame_events=0))
try:
 for width,height in[(1280,720),(1600,720),(1280,800)]:
  d=N/(str(width)+'x'+str(height));d.mkdir();e=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
  for k,n in[('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/n;p.mkdir();e[k]=str(p)
  e.update(R129_OUT=str(d/'output'),R129_LANE='candidate',R129_WIDTH=str(width),R129_HEIGHT=str(height),R129_PIN_SHA256=sha(N/'SOURCE_PIN.json'))
  cmd=[str(E),'--path',str(U),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x'+str(height),'--max-fps','30','--script','res://export/flat_vector_r129/capture_guide.gd']
  with(d/'engine.log').open('wb')as f:
   proc=subprocess.Popen(cmd,cwd=U,env=e,stdout=f,stderr=subprocess.STDOUT,creationflags=0x08000000);wr(d/'LAUNCH.json',dict(pid=proc.pid,command=cmd,at_utc=now()));state('RUNNING_CORRECT_CURRENT_NATIVE_GUIDE',pid=proc.pid,width=width,height=height,log=str(d/'engine.log'));rc=proc.wait(timeout=240)
  text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert rc==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:.*(Failed loading resource|Cannot open file|No loader found)',text),text[-4500:]
  r=rd(d/'output/RESULT.json');assert r['status']=='PASS'and len(r['captures'])==11 and all(x['pass']for x in r['checks']);cases.append(dict(width=width,height=height,checks=len(r['checks']),frames=r['captures'],result_sha256=sha(d/'output/RESULT.json')));print('R129_NATIVE',width,height,len(r['checks']),'11frames',flush=True)
 drift=[p for p,h in pin['runtime_hashes'].items()if sha(U/p)!=h];assert not drift and normals()==pin['normal_before']
 wr(N/'FINAL_RESULT.json',dict(state='PASS_CONFIGURED_CURRENT_NATIVE_REVIEW_REQUIRED',cases=cases,checks=sum(x['checks']for x in cases),new_native_frame_events=33,source_drift=drift,normal_unchanged=True,normal_before=pin['normal_before'],normal_after=normals(),healthy_import_reused=True,excluded_native_frame_events=0,formal_QA11=None,device=None,child=None,owner=None,completed_at_utc=now()));state('TERMINAL_NATIVE_PASS');print('R129_NATIVE_ALL_OK',flush=True)
except Exception as exc:wr(S/'NATIVE_RECOVERY_STOP.json',dict(state='STOPPED_PRESERVE_EXACT_OPERATION',error=str(exc),at_utc=now()));state('TERMINAL_NATIVE_FAILURE',error=str(exc));raise
