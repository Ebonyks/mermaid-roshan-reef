from pathlib import Path
import json,hashlib,subprocess,os,datetime,re,sys
U=Path.cwd();S=Path(__file__).parent;P=U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r120_melody_curtains_runtime';E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe');BASE='27c88288bf6e39582072811443df79919e7bbb89';lane=sys.argv[1];assert lane in['source','candidate'];W=S/(lane+'_native_entry_repaired');W.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(n,**kw):wr(S/'NATIVE_STATE.json',dict(state=n,lane=lane,at_utc=now(),**kw))
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE;assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
normal=Path(json.loads((U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json').read_text(encoding='utf-8'))['normal_base']);suffixes=['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.bak','.before_new_game.tmp']
def normals():return{n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in suffixes}
before=normals();paths=[p for p in subprocess.check_output(['git','ls-files'],text=True,encoding='utf-8').splitlines()if p.startswith(('assets/','scripts/','scenes/'))or p in['project.godot','tools/godot_baseline.json']];paths+=['assets/melody/curtain_left_painted.png','assets/melody/curtain_left_painted.png.import','assets/melody/curtain_right_painted.png','assets/melody/curtain_right_painted.png.import']if lane=='candidate'else[];hashes={p:sha(U/p)for p in paths if(U/p).is_file()};pin=dict(baseline=BASE,runtime_hashes=hashes,engine=str(E),engine_sha256=sha(E),fixture_sha256=sha(P/'capture_curtains.gd'),normal_before=before);wr(W/'SOURCE_PIN.json',pin);pinsha=sha(W/'SOURCE_PIN.json');cases=[]
try:
 state('REUSING_SUCCESSFUL_EXACT_IMPORT_NEW_POST_IMPORT_PIN_REAL_CONTINUE_ENTRY')
 assert json.loads((S/'IMPORT_EOL_BINDING.json').read_text(encoding='utf-8'))['state']=='ALL_IMPORT_DRIFT_IS_EOL_ONLY_NO_LOGICAL_GIT_OR_PIXELS_CHANGE'
 for width,height in[(1280,720),(1600,720),(1280,800)]:
  d=W/(str(width)+'x'+str(height));d.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
  for key,name in[('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/name;p.mkdir();env[key]=str(p)
  env.update(R120_OUT=str(d/'output'),R120_LANE=lane,R120_WIDTH=str(width),R120_HEIGHT=str(height),R120_PIN_SHA256=pinsha);cmd=[str(E),'--path',str(U),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x'+str(height),'--max-fps','30','--script','res://export/flat_vector_r120/capture_curtains.gd'];wr(d/'LAUNCH.json',dict(command=cmd,at_utc=now(),pin_sha256=pinsha));state('RUNNING_ACTUAL_NATIVE_CONTEXT',width=width,height=height)
  with(d/'engine.log').open('wb')as log:q=subprocess.run(cmd,cwd=U,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
  text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:.*(Failed loading resource|Cannot open file|No loader found)',text),text[-4000:]
  r=json.loads((d/'output/RESULT.json').read_text(encoding='utf-8'));assert r['status']=='PASS'and all(x['pass']for x in r['checks']);cases.append(dict(width=width,height=height,checks=len(r['checks']),frames=r['captures'],result_sha256=sha(d/'output/RESULT.json')));print('R120_NATIVE',lane,width,height,len(r['checks']),flush=True)
 drift=[p for p,h in hashes.items()if sha(U/p)!=h];assert not drift and normals()==before;wr(W/'FINAL_RESULT.json',dict(state='PASS_CONFIGURED_SOURCE_BOUND_NATIVE_CONTEXT_REVIEW_REQUIRED',lane=lane,cases=cases,checks=sum(x['checks']for x in cases),new_native_frame_events=sum(len(x['frames'])for x in cases),source_drift=drift,normal_unchanged=True,normal_before=before,normal_after=normals(),formal_QA11=None,device=None,child=None,owner=None,completed_at_utc=now()));state('TERMINAL_NATIVE_CONTEXT_PASS',checks=sum(x['checks']for x in cases),frames=sum(len(x['frames'])for x in cases))
except Exception as e:wr(S/(lane+'_NATIVE_REPAIRED_STOP.json'),dict(error=str(e),at_utc=now()));state('TERMINAL_NATIVE_CONTEXT_FAILURE',error=str(e));raise
