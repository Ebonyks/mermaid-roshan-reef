from pathlib import Path
import json,hashlib,subprocess,datetime,os,re,sys
R=Path.cwd();S=Path(__file__).parent;E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe');P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r115_geologist_station_props_runtime';BASE='6d2e7c515738bb40a923210bb05c01aafc526e0e'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
lane=sys.argv[1];assert lane in ['source','candidate'];W=S/(lane+'_native');assert not W.exists();W.mkdir()
assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'and subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE
normal=Path(rd(R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base']);suffixes=['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.bak','.before_new_game.tmp']
def normals():return {n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in suffixes}
before=normals();paths=set(rd(Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-geologist-goal-20261030/SOURCE_PIN.json'))['runtime_hashes'])|{'scripts/opera_world_backdrop_2d.gd'}
if lane=='candidate':paths|={str(p.relative_to(R).as_posix())for p in (R/'assets/opera/worlds/props').glob('geologist_station_tray_*')}
pin={p:sha(R/p)for p in sorted(paths)if(R/p).is_file()};wr(W/'SOURCE_PIN.json',dict(baseline=BASE,runtime_hashes=pin,normal_before=before,engine=str(E),engine_sha256=sha(E),fixture_lf_sha256=hashlib.sha256((P/'capture_stations.gd').read_bytes().replace(b'\r\n',b'\n')).hexdigest()))
errors=r'SCRIPT ERROR|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)'
cases=[]
try:
 for width in [1280,1600]:
  for phase in [0,1,2,3]:
   d=W/(str(width)+'_'+str(phase));d.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
   for key,name in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/name;p.mkdir();env[key]=str(p)
   env.update(R115_LANE=lane,R95_OUT=str(d/'output'),R95_WIDTH=str(width),R115_PHASE=str(phase),R95_REV=BASE+'; current sourcebound '+sha(R/'scripts/opera_world_backdrop_2d.gd'),R95_NORMAL_BASE=str(normal));cmd=[str(E),'--path',str(R),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--log-file',str(d/'native_engine.log'),'--script','res://export/flat_vector_r115/capture_stations.gd'];wr(d/'LAUNCH.json',dict(command=cmd,at_utc=now()));wr(S/'FOCUSED_STATE.json',dict(state='RUNNING_NATIVE_'+lane,width=width,phase=phase,at_utc=now()))
   with(d/'engine.log').open('wb')as log:q=subprocess.run(cmd,cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
   text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert q.returncode==0 and not re.search(errors,text),text[-3000:]
   result=rd(d/'output/RESULT.json');assert result['status']=='PASS'and all(x['pass']for x in result['checks'])and result['normal_before']==result['normal_after'];cases.append(dict(width=width,phase=phase,checks=len(result['checks']),frames=result['captures'],result=str(d/'output/RESULT.json'),result_sha256=sha(d/'output/RESULT.json')));print('R115_NATIVE',lane,width,phase,len(result['checks']),len(result['captures']),flush=True)
 drift=[p for p,h in pin.items()if not(R/p).is_file()or sha(R/p)!=h];assert not drift and normals()==before
 out=dict(state='ACTUAL_ORIGINAL_MAIN_FOUR_PHASE_TWO_ASPECT_PASS_REVIEW_REQUIRED',lane=lane,cases=cases,checks=sum(x['checks']for x in cases),new_native_frame_events=sum(len(x['frames'])for x in cases),source_drift=drift,normal_unchanged=True,normal_before=before,normal_after=normals(),formal_QA11=None,device=None,child=None,owner=None,completed_at_utc=now());wr(W/'FOCUSED_RESULT.json',out);wr(S/'FOCUSED_STATE.json',dict(state='TERMINAL_'+lane+'_PASS',checks=out['checks'],frames=out['new_native_frame_events'],at_utc=now()))
except Exception as e:wr(S/(lane+'_FOCUSED_STOP.json'),dict(error=str(e),at_utc=now()));raise
