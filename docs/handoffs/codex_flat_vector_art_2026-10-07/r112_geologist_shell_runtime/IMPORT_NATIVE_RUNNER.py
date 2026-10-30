from pathlib import Path
import json,hashlib,subprocess,datetime,os,re,sys
R=Path.cwd();S=Path(__file__).parent;E=Path(r'C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\Godot\4.7.2\godot.exe');P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r112_geologist_shell_runtime';A=R/'assets/opera/worlds/props/geologist_geode_shell_painted.png'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(n,**x):wr(S/'FOCUSED_STATE.json',{'state':n,'at_utc':now(),**x})
assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
normal=Path(rd(R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'])
def normals():return {n:sha(Path(str(normal)+n)) if Path(str(normal)+n).is_file() else 'absent' for n in ['', '.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.tmp','.before_new_game.old']}
assets=[A,A.with_name("geologist_geode_shell_left_painted.png"),A.with_name("geologist_geode_shell_right_painted.png")]
before=normals();wr(S/'FOCUSED_LAUNCH.json',{'baseline':'70715413b21232920f07a4df79a5721f9885962a','started_at_utc':now(),'engine':str(E),'engine_sha256':sha(E),'normal_before':before,'candidate_png_sha256':sha(A),'fixture':(P/'capture_shell.gd').relative_to(R).as_posix(),'method':'Private import, final actual mipmap settings, then serial two-aspect native fixture; no simultaneous headless logic probe/display job.'})
errors=r'SCRIPT ERROR|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)'
def envdir(label):
 d=S/label;d.mkdir(exist_ok=False);env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 for key,name in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/name;p.mkdir();env[key]=str(p)
 return d,env
try:
 imports=[]
 for pass_index in [1,2]:
  d,env=envdir('import'+str(pass_index));state('IMPORTING_ACTUAL_PAINTED_GALLERY_CANDIDATE',pass_index=pass_index)
  cmd=[str(E),'--headless','--log-file',str(d/'native_engine.log'),'--path',str(R),'--import'];wr(d/'LAUNCH.json',{'command':cmd,'at_utc':now()})
  with(d/'engine.log').open('wb')as log:q=subprocess.run(cmd,cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,timeout=720,creationflags=0x08000000)
  text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert q.returncode==0 and not re.search(errors,text),text[-2500:]
  imports.append({'pass':pass_index,'exit_code':q.returncode,'log':str(d/'engine.log'),'sha256':sha(d/'engine.log')});changes=[]
  for asset in assets:
   imp=asset.with_suffix('.png.import');t=imp.read_text(encoding='utf-8');u=re.sub(r'^mipmaps/generate=.*$','mipmaps/generate=true',t,flags=re.M);u=re.sub(r'^compress/mode=.*$','compress/mode=0',u,flags=re.M);u=re.sub(r'^process/size_limit=.*$','process/size_limit=1024',u,flags=re.M)
   if t!=u:
    assert pass_index==1,'Importer changed final settings unexpectedly';imp.write_text(u,encoding='utf-8',newline='\n');changes.append({'path':imp.relative_to(R).as_posix(),'before':t,'after':u})
  if not changes:break
  wr(S/'IMPORT_SETTINGS_CHANGE.json',{'reason':'Actual new512-square lossless runtime textures require mipmaps; no unchanged healthy engine suite rerun.','changes':changes})
 source_paths=rd(Path(r"C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-geologist-seam-20261030/SOURCE_PIN.json"))["runtime_hashes"];paths=sorted(set(source_paths)|{p.relative_to(R).as_posix()for a in assets for p in[a,a.with_suffix(".png.import")]});pin={p:sha(R/p)for p in paths};wr(S/"SOURCE_PIN.json",{"baseline":"70715413b21232920f07a4df79a5721f9885962a","runtime_hashes":pin,"normal_before":before,"engine":str(E),"engine_sha256":sha(E),"new_asset_sha256":sha(A),"fixture_lf_sha256":hashlib.sha256((P/"capture_shell.gd").read_bytes().replace(b"\r\n",b"\n")).hexdigest()})
 cases=[]
 for width in [1280,1600]:
  for phase in [3]:
   d,env=envdir("candidate_"+str(width)+"_"+str(phase));env.update(R95_OUT=str(d/"output"),R95_WIDTH=str(width),R112_PHASE=str(phase),R95_REV="70715413b21232920f07a4df79a5721f9885962a + actual candidateSHA256 "+sha(R/"scripts/opera_geology_surface.gd"),R95_NORMAL_BASE=str(normal));cmd=[str(E),"--path",str(R),"--rendering-method","mobile","--audio-driver","Dummy","--resolution",str(width)+"x720","--max-fps","30","--log-file",str(d/"native_engine.log"),"--script","res://export/flat_vector_r112/capture_shell.gd"];wr(d/"LAUNCH.json",{"command":cmd,"source_pin":str(S/"SOURCE_PIN.json"),"started_at_utc":now()});state("ACTUAL_CANDIDATE_NATIVE_CONTEXT",width=width,phase=phase)
   with(d/"engine.log").open("wb")as log:q=subprocess.run(cmd,cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
   text=(d/"engine.log").read_text(encoding="utf-8",errors="replace");assert q.returncode==0 and not re.search(errors,text),text[-2800:]
   result=rd(d/"output/RESULT.json");assert result["status"]=="PASS"and all(x["pass"]for x in result["checks"])and result["normal_before"]==result["normal_after"];cases.append({"width":width,"phase":phase,"checks":len(result["checks"]),"frames":result["captures"],"result":str(d/"output/RESULT.json"),"result_sha256":sha(d/"output/RESULT.json")});print("R112_NATIVE_PASS",width,phase,len(result["checks"]),len(result["captures"]),flush=True)
 drift=[p for p,h in pin.items()if not(R/p).is_file()or sha(R/p)!=h];assert not drift and normals()==before
 out={"state":"FOCUSED_IMPORT_AND_GEODE_TWO_ASPECT_CONTEXT_PASS_AGENT_REVIEW_REQUIRED","imports":imports,"cases":cases,"checks":sum(x["checks"]for x in cases),"new_native_frame_events":sum(len(x["frames"])for x in cases),"source_drift":drift,"normal_unchanged":True,"normal_before":before,"normal_after":normals(),"new_generation_calls":1,"formal_QA11":None,"device":None,"child":None,"owner":None,"full_trusted_suite":"PENDING_AFTER_AGENT_SCENE_REVIEW","completed_at_utc":now()};wr(S/"FOCUSED_RESULT.json",out);state("FOCUSED_PASS_AWAIT_AGENT_REVIEW",checks=out["checks"],new_frames=out["new_native_frame_events"]);print("R112_FOCUSED_PASS",flush=True)
except Exception as e:state("FAILED_NO_AUTOMATIC_RETRY",error=str(e));wr(S/"FOCUSED_STOP.json",{"error":str(e),"at_utc":now()});raise
