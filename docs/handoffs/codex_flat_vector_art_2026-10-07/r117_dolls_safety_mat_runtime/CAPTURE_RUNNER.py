from pathlib import Path
import json,hashlib,subprocess,datetime,os,re,sys
U=Path.cwd();S=Path(__file__).parent;P=U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r117_dolls_safety_mat_runtime';BASE='086e9285e56b2e6b31bdbaf1c4209b57c9722460';E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
lane=sys.argv[1];assert lane in['source','candidate'];W=S/(lane+'_native_final');assert not W.exists();W.mkdir();assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE and sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
normal=Path(rd(U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base']);suffixes=['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.bak','.before_new_game.tmp']
def normals():return {n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in suffixes}
before=normals();paths=set(rd(U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r116_geologist_layered_rock_runtime/SOURCE_PIN.json')['runtime_hashes'])|{'scripts/games/dolls.gd','scripts/opera_nursery_catch.gd'}
if lane=='candidate':paths|={'assets/dolls/safety_mat_painted.png','assets/dolls/safety_mat_painted.png.import'}
pin={p:sha(U/p)for p in sorted(paths)if(U/p).is_file()};wr(W/'SOURCE_PIN.json',dict(baseline=BASE,runtime_hashes=pin,runtime_deletions=[],normal_before=before,engine=str(E),engine_sha256=sha(E),fixture_lf_sha256=sha(P/'capture_mat.gd')));cases=[]
try:
 for width in[1280,1600]:
  d=W/str(width);d.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
  for key,name in[('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/name;p.mkdir();env[key]=str(p)
  env.update(R117_LANE=lane,R117_OUT=str(d/'output'),R117_WIDTH=str(width),R117_REV=BASE+'; exactactualDolls:'+sha(U/'scripts/games/dolls.gd'),R117_NORMAL_BASE=str(normal));cmd=[str(E),'--path',str(U),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--log-file',str(d/'native_engine.log'),'--script','res://export/flat_vector_r117/capture_mat.gd'];wr(d/'LAUNCH.json',dict(command=cmd,at_utc=now()));wr(S/'FOCUSED_STATE.json',dict(state='RUNNING_NATIVE_'+lane,width=width,at_utc=now()))
  with(d/'engine.log').open('wb')as log:q=subprocess.run(cmd,cwd=U,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
  text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)',text),text[-3000:]
  result=rd(d/'output/RESULT.json');assert result['status']=='PASS'and all(x['pass']for x in result['checks'])and result['normal_before']==result['normal_after'];cases.append(dict(width=width,checks=len(result['checks']),frames=result['captures'],result=str(d/'output/RESULT.json'),result_sha256=sha(d/'output/RESULT.json')));print('R117_NATIVE',lane,width,len(result['checks']),len(result['captures']),flush=True)
 changed=[p for p,h in pin.items()if not(U/p).is_file()or sha(U/p)!=h];assert not changed and normals()==before;out=dict(state='ORIGINAL_MAIN_FARON_DOLLS_FIVE_STATES_TWO_ASPECT_PASS_REVIEW_REQUIRED',lane=lane,cases=cases,checks=sum(x['checks']for x in cases),new_native_frame_events=sum(len(x['frames'])for x in cases),source_drift=changed,normal_before=before,normal_after=normals(),normal_unchanged=True,formal_QA11=None,device=None,child=None,owner=None,completed_at_utc=now());wr(W/'FOCUSED_RESULT.json',out);wr(S/'FOCUSED_STATE.json',dict(state='TERMINAL_'+lane+'_PASS',checks=out['checks'],frames=out['new_native_frame_events'],at_utc=now()))
except Exception as e:wr(S/(lane+'_FOCUSED_FINAL_STOP.json'),dict(error=str(e),at_utc=now()));raise
