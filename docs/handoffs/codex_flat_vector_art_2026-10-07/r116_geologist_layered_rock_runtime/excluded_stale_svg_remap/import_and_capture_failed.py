from pathlib import Path
import subprocess,json,hashlib,re,os,sys,datetime,shutil
S=Path(__file__).parent;U=Path.cwd();P=U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r116_geologist_layered_rock_runtime';E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe');W=S/'candidate_import';assert not W.exists();W.mkdir()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
assert(S/'RUNTIME_BINDING_READY.json').exists();imports=[];changes=[]
try:
 for i in [1,2]:
  d=W/str(i);d.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
  for key,name in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/name;p.mkdir();env[key]=str(p)
  cmd=[str(E),'--headless','--log-file',str(d/'native_engine.log'),'--path',str(U),'--import'];wr(S/'FOCUSED_STATE.json',dict(state='IMPORTING_REAL_LAYERED_ROCK_CANDIDATE',pass_index=i,command=cmd,at_utc=now()))
  with(d/'engine.log').open('wb')as log:q=subprocess.run(cmd,cwd=U,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,timeout=720,creationflags=0x08000000)
  t=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource',t),t[-3000:];imports.append(dict(pass_index=i,exit_code=0,log=str(d/'engine.log'),sha256=sha(d/'engine.log')))
  changed=[]
  for p in (U/'assets/opera/worlds/hotspots').glob('geologist_layered_rock_painted.png.import'):
   t=p.read_text(encoding='utf-8');u=re.sub(r'^mipmaps/generate=.*$','mipmaps/generate=true',t,flags=re.M);u=re.sub(r'^compress/mode=.*$','compress/mode=0',u,flags=re.M);u=re.sub(r'^process/size_limit=.*$','process/size_limit=1024',u,flags=re.M)
   if t!=u:assert i==1;p.write_text(u,encoding='utf-8',newline='\n');changed.append(dict(path=p.relative_to(U).as_posix(),before=t,after=u))
  changes+=changed
  if not changed:break
 wr(S/'IMPORT_RESULT.json',dict(state='PASS_ACTUAL_FINAL_SETTINGS_IMPORT',imports=imports,settings_changed=changes,reason='One newly created512whole layeredrock texture, lossless and mipmaps; secondimport onlyfor actual changedsettings, no unchanged suite repeat.'))
 q=subprocess.run([sys.executable,'-X','utf8','-B',str(S/'capture_native.py'),'candidate'],cwd=U,stdin=subprocess.DEVNULL,creationflags=0x08000000);assert q.returncode==0
except Exception as e:wr(S/'CANDIDATE_IMPORT_STOP.json',dict(error=str(e),at_utc=now()));raise
