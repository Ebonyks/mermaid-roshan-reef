from pathlib import Path
import subprocess,os,json,datetime,hashlib,re
U=Path.cwd();S=Path(__file__).parent;E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe');W=S/'candidate_import';assert not W.exists();W.mkdir()
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
for k,n in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=W/n;p.mkdir();env[k]=str(p)
cmd=[str(E),'--headless','--path',str(U),'--rendering-method','mobile','--import'];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with(W/'IMPORT.log').open('wb')as f:q=subprocess.run(cmd,cwd=U,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
txt=(W/'IMPORT.log').read_text(encoding='utf8',errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:',txt),txt[-4000:]
(W/'RESULT.json').write_text(json.dumps(dict(status='PASS',command=cmd,started_at_utc=start,completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),log_sha256=hashlib.sha256((W/'IMPORT.log').read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf8')
paths=[U/'assets/dolls/progress_empty_painted.png.import',U/'assets/dolls/progress_filled_painted.png.import']
changes=[]
for p in paths:
 t=p.read_text(encoding='utf8');new=t.replace('mipmaps/generate=false','mipmaps/generate=true').replace('process/size_limit=0','process/size_limit=1024')
 if new!=t:p.write_text(new,encoding='utf8',newline='\n');changes.append(p.relative_to(U).as_posix())
if changes:
 with(W/'IMPORT_FINAL_SETTINGS.log').open('wb')as f:q=subprocess.run(cmd,cwd=U,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
 txt=(W/'IMPORT_FINAL_SETTINGS.log').read_text(encoding='utf8',errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:',txt),txt[-4000:]
(W/'FINAL_IMPORT_SETTINGS.json').write_text(json.dumps(dict(changed_sidecars=changes,settings='lossless512 RGBA with mipmaps, no VRAM NPOT'),indent=2)+'\n',encoding='utf8')
print('R119_IMPORT_PASS',flush=True)
subprocess.run(['python','-X','utf8','-B',str(S/'capture_native_final.py'),'candidate'],cwd=U,env=os.environ,check=True)
