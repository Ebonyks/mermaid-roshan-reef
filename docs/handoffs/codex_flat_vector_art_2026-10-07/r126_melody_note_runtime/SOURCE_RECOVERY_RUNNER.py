from pathlib import Path
import json,hashlib,subprocess,os,re,datetime
U=Path.cwd();S=Path(__file__).parent;P=U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r126_melody_note_runtime';N=S/'source_native_recovery';E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def sandbox(d):
 env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 for k,n in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
  p=d/n;p.mkdir(exist_ok=True);env[k]=str(p)
 return env
assert not N.exists(),'Resume existing operation';assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='27c88288bf6e39582072811443df79919e7bbb89';assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424';pin=json.loads((S/'SOURCE_BASELINE_PIN.json').read_text(encoding='utf-8'));hashes=pin['runtime_hashes'];assert all(sha(U/p)==h for p,h in hashes.items());N.mkdir();fixture=sha(P/'capture_note.gd');pin['fixture_sha256']=fixture;wr(N/'SOURCE_PIN.json',pin);pinsha=sha(N/'SOURCE_PIN.json');cases=[];wr(N/'LAUNCH.json',dict(pid=os.getpid(),at_utc=now(),source_revision=pin['baseline'],fixture_sha256=fixture,pin_sha256=pinsha))
try:
 for width,height in [(1280,720),(1600,720),(1280,800)]:
  assert all(sha(U/p)==h for p,h in hashes.items());d=N/(str(width)+'x'+str(height));d.mkdir();env=sandbox(d);env.update(R126_OUT=str(d/'output'),R126_LANE='source',R126_WIDTH=str(width),R126_HEIGHT=str(height),R126_PIN_SHA256=pinsha);cmd=[str(E),'--path',str(U),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x'+str(height),'--max-fps','30','--script','res://export/flat_vector_r126/capture_note.gd'];wr(d/'LAUNCH.json',dict(command=cmd,at_utc=now(),pin_sha256=pinsha));wr(S/'SOURCE_RECOVERY_STATE.json',dict(state='RUNNING_BASELINE_SEVEN_NOTE_STATES',pid=os.getpid(),width=width,height=height,at_utc=now()))
  with(d/'engine.log').open('wb')as f:q=subprocess.run(cmd,cwd=U,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=300,creationflags=0x08000000)
  t=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:.*(Failed loading resource|Cannot open file|No loader found)',t),t[-4000:];r=json.loads((d/'output/RESULT.json').read_text(encoding='utf-8-sig'));assert r['status']=='PASS'and len(r['captures'])==7 and all(x['pass']for x in r['checks']);cases.append(dict(width=width,height=height,checks=len(r['checks']),frames=r['captures'],result_sha256=sha(d/'output/RESULT.json')));print('R126_SOURCE_NATIVE',width,height,len(r['checks']),flush=True)
 assert all(sha(U/p)==h for p,h in hashes.items());wr(N/'FINAL_RESULT.json',dict(state='PASS_SELECTED_ROLE_ALL_SEVEN_STATES_THREE_ASPECTS',source_revision=pin['baseline'],source_pin_sha256=pinsha,fixture_sha256=fixture,checks=sum(x['checks']for x in cases),new_native_frame_events=sum(len(x['frames'])for x in cases),cases=cases,normal_save_isolated=True,source_drift=[],formal_QA11=None,device=None,child=None,owner=None,completed_at_utc=now()));wr(S/'SOURCE_RECOVERY_STATE.json',dict(state='TERMINAL_SOURCE_NATIVE_PASS',at_utc=now()));print('R126_SOURCE_NATIVE_ALL_OK',flush=True)
except Exception as e:wr(S/'SOURCE_RECOVERY_STOP.json',dict(state='STOPPED_NO_AUTOMATIC_RESTART',error=str(e),at_utc=now()));raise
