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

assert N.exists() and not(N/'1280x720').exists(),'Resume exact state, never duplicate healthy native captures'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='27c88288bf6e39582072811443df79919e7bbb89'
pin=rd(S/'SOURCE_BASELINE_PIN.json');assert len(pin['runtime_hashes'])==5062 and all(sha(U/p)==h for p,h in pin['runtime_hashes'].items())
assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
import_log=(N/'import/engine.log').read_text(encoding='utf-8',errors='replace')
assert not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:',import_log)
normal=Path(rd(U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base']);suffixes=['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.bak','.before_new_game.tmp']
def normals():return{n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in suffixes}
before=rd(N/'SOURCE_PIN_attempt02.json')['normal_before'];assert normals()==before
wr(N/'SOURCE_PIN.json',dict(pin,fixture_sha256=sha(P/'capture_snowball.gd'),engine=str(E),engine_sha256=sha(E),normal_before=before,additional_context_reason=rd(S/'PLAN.json')['additional_context_dependency'],diagnostic='Zero-frame setup attempts retained. Headless suppresses title; synthetic screen drag held mouse polling but did not advance polled angular position. Use original trusted probe virtual-stick vector drive with actual original controller tick, and real screen taps for face. Display/clock/native context only, physical touch/natural route/QA11 remain unclaimed. Original successful import reused.'))
wr(N/'SOURCE_CONTEXT_DIAGNOSIS_attempt03.json',dict(failed_operation='11187 / Godot88088',failure='Headless main suppresses actual display title. Null-title fixture method stopped before original pointer clock check.',affected_lane='Evidence fixture only',native_frame_events=0,art_outputs=0,production_files_changed=0,fix='Guard null menu and use display Mobile preflight. Successful original import reused, not rerun.',original_fixture_sha256=sha(S/'capture_snowball_attempt01.gd'),fixed_fixture_sha256=sha(P/'capture_snowball.gd'),formal_QA11=None))
cases=[]
try:
 d=N/'driver_display_preflight_03';d.mkdir();e=env_for(d);e.update(R131_OUT=str(d/'output'),R131_LANE='source',R131_WIDTH='1280',R131_HEIGHT='720',R131_DRIVER_ONLY='1',R131_PIN_SHA256=sha(N/'SOURCE_PIN.json'))
 cmd=[str(E),'--max-fps','30','--path',str(U),'--rendering-method','mobile','--audio-driver','Dummy','--resolution','1280x720','--script','res://export/flat_vector_r131/capture_snowball.gd']
 state('SOURCE_INPUT_CLOCK_PREFLIGHT_NO_NATIVE_FRAMES')
 with(d/'engine.log').open('wb')as f:
  proc=subprocess.Popen(cmd,cwd=U,env=e,stdout=f,stderr=subprocess.STDOUT,creationflags=0x08000000);wr(d/'LAUNCH.json',dict(pid=proc.pid,command=cmd,at_utc=now()));rc=proc.wait(timeout=120)
 text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert rc==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|R131\|FAIL\|',text),text[-4000:]
 r=rd(d/'output/RESULT.json');assert r['status']=='PASS'and len(r['captures'])==0 and all(c['pass']for c in r['checks'])
 print('R131_SOURCE_PREFLIGHT_OK',r['pointer_driver'],len(r['checks']),flush=True)
 for width,height in[(1280,720),(1600,720),(1280,800)]:
  d=N/(str(width)+'x'+str(height));d.mkdir();e=env_for(d);e.update(R131_OUT=str(d/'output'),R131_LANE='source',R131_WIDTH=str(width),R131_HEIGHT=str(height),R131_PIN_SHA256=sha(N/'SOURCE_PIN.json'))
  cmd=[str(E),'--path',str(U),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x'+str(height),'--max-fps','30','--script','res://export/flat_vector_r131/capture_snowball.gd']
  state('CAPTURING_SELECTED_SNOWBALL_ACTION_CONTEXT',width=width,height=height)
  with(d/'engine.log').open('wb')as f:
   proc=subprocess.Popen(cmd,cwd=U,env=e,stdout=f,stderr=subprocess.STDOUT,creationflags=0x08000000);wr(d/'LAUNCH.json',dict(pid=proc.pid,command=cmd,at_utc=now(),source_pin_sha256=sha(N/'SOURCE_PIN.json')));rc=proc.wait(timeout=240)
  text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert rc==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:.*(Failed loading resource|Cannot open file|No loader found)',text),text[-3000:]
  r=rd(d/'output/RESULT.json');assert r['status']=='PASS'and len(r['captures'])==18 and all(c['pass']for c in r['checks']);cases.append(dict(width=width,height=height,checks=len(r['checks']),frames=r['captures'],result_sha256=sha(d/'output/RESULT.json')));print('R131_SOURCE_CONTEXT',width,height,len(r['checks']),flush=True)
 assert all(sha(U/p)==h for p,h in pin['runtime_hashes'].items())and normals()==before
 wr(N/'FINAL_RESULT.json',dict(state='PASS_SELECTED_ROLE_ORIGINAL_ACTION_CONTEXT_REVIEW_REQUIRED',cases=cases,checks=sum(c['checks']for c in cases),new_native_frame_events=dict(bounded=54,excluded=0,retained=54),baseline5062raw_exact=True,normal_before=before,normal_after=normals(),normal_unchanged=True,generation_calls=0,candidate_outputs=0,formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,completed_at_utc=now()))
 state('TERMINAL_SELECTED_SOURCE_CONTEXT_PASS_NO_ART_OUTPUT_YET');print('R131_SOURCE_CONTEXT_ALL_OK54FRAMES',flush=True)
except Exception as exc:
 wr(S/'SOURCE_CONTEXT_STOP.json',dict(state='STOPPED_RESUME_EXACT_OPERATION_NO_AUTOMATIC_RETRY',error=str(exc),at_utc=now()));state('TERMINAL_SOURCE_CONTEXT_FAIL',error=str(exc));raise
