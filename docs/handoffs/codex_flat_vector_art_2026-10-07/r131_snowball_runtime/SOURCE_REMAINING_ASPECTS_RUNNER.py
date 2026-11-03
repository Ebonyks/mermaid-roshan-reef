from pathlib import Path
import json,hashlib,subprocess,os,re,datetime
U=Path.cwd();S=Path(__file__).parent;P=U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r131_snowball_runtime';N=S/'source_native';E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(n,**kw):wr(S/'SOURCE_CONTEXT_STATE.json',dict(state=n,pid=os.getpid(),at_utc=now(),**kw))
def env_for(d):
 e=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 for k,n in[('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
  p=d/n;p.mkdir();e[k]=str(p)
 return e


assert N.exists()and(N/'1280x720/output/RESULT.json').exists()and not(N/'1600x720').exists(),'Resume exact operation, no duplicate first-aspect captures'
pin=rd(S/'SOURCE_BASELINE_PIN.json');assert len(pin['runtime_hashes'])==5062 and all(sha(U/p)==h for p,h in pin['runtime_hashes'].items())
normal=Path(rd(U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base']);suffixes=['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.bak','.before_new_game.tmp']
def normals():return{n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in suffixes}
before=rd(N/'SOURCE_PIN.json')['normal_before'];assert normals()==before
wr(N/'SOURCE_PIN_ADDITIONAL_ASPECTS.json',dict(pin,fixture_sha256=sha(P/'capture_snowball.gd'),engine=str(E),engine_sha256=sha(E),normal_before=before,geometry_tolerance_receipt_sha256=sha(N/'SOURCE_GEOMETRY_TOLERANCE_RECEIPT.json'),reason='No production change/import/preflight rerun. Reuse original18source frames with retained strict-float failure and scoped tolerance receipt; capture only missing2aspects.'))
r=rd(N/'1280x720/output/RESULT.json')
cases=[dict(width=1280,height=720,checks=len(r['checks']),frames=r['captures'],original_status='FAIL_EXACT_FLOAT_EQUALITY3',scoped_tolerance_supplement='PASS',result_sha256=sha(N/'1280x720/output/RESULT.json'),original_source_pin_sha256=sha(N/'SOURCE_PIN.json'))]
try:
 for width,height in[(1600,720),(1280,800)]:
  d=N/(str(width)+'x'+str(height));d.mkdir();e=env_for(d);e.update(R131_OUT=str(d/'output'),R131_LANE='source',R131_WIDTH=str(width),R131_HEIGHT=str(height),R131_PIN_SHA256=sha(N/'SOURCE_PIN_ADDITIONAL_ASPECTS.json'))
  cmd=[str(E),'--path',str(U),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x'+str(height),'--max-fps','30','--script','res://export/flat_vector_r131/capture_snowball.gd']
  state('CAPTURING_SELECTED_SNOWBALL_ACTION_CONTEXT',width=width,height=height)
  with(d/'engine.log').open('wb')as f:
   proc=subprocess.Popen(cmd,cwd=U,env=e,stdout=f,stderr=subprocess.STDOUT,creationflags=0x08000000);wr(d/'LAUNCH.json',dict(pid=proc.pid,command=cmd,at_utc=now(),source_pin_sha256=sha(N/'SOURCE_PIN_ADDITIONAL_ASPECTS.json')));rc=proc.wait(timeout=240)
  text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert rc==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:.*(Failed loading resource|Cannot open file|No loader found)',text),text[-3000:]
  r=rd(d/'output/RESULT.json');assert r['status']=='PASS'and len(r['captures'])==18 and all(c['pass']for c in r['checks']);cases.append(dict(width=width,height=height,checks=len(r['checks']),frames=r['captures'],result_sha256=sha(d/'output/RESULT.json')));print('R131_SOURCE_CONTEXT',width,height,len(r['checks']),flush=True)
 assert all(sha(U/p)==h for p,h in pin['runtime_hashes'].items())and normals()==before
 wr(N/'FINAL_RESULT.json',dict(state='PASS_SCOPED_SELECTED_SOURCE_CONTEXT_WITH_RETAINED_EXACT_FLOAT_FAILURE_SUPPLEMENT_REVIEW_REQUIRED',cases=cases,checks=sum(c['checks']for c in cases),new_native_frame_events=dict(bounded=54,excluded=0,retained=54),baseline5062raw_exact=True,normal_before=before,normal_after=normals(),normal_unchanged=True,generation_calls=0,candidate_outputs=0,formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,completed_at_utc=now()))
 state('TERMINAL_SELECTED_SOURCE_CONTEXT_PASS_NO_ART_OUTPUT_YET');print('R131_SOURCE_CONTEXT_ALL_OK54FRAMES',flush=True)
except Exception as exc:
 wr(S/'SOURCE_CONTEXT_STOP.json',dict(state='STOPPED_RESUME_EXACT_OPERATION_NO_AUTOMATIC_RETRY',error=str(exc),at_utc=now()));state('TERMINAL_SOURCE_CONTEXT_FAIL',error=str(exc));raise
