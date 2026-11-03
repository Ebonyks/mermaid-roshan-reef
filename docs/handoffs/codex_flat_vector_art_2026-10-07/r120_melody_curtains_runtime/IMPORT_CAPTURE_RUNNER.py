from pathlib import Path
import json,hashlib,subprocess,os,re,datetime,sys
U=Path.cwd();S=Path(__file__).parent;W=S/'candidate_import';W.mkdir();E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe');env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
for key,name in[('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=W/name;p.mkdir();env[key]=str(p)
cmd=[str(E),'--headless','--path',str(U),'--rendering-method','mobile','--import'];rows=[]
try:
 for leg in['initial_new_assets','final_new_import_settings']:
  log=W/(leg+'.log')
  with log.open('wb')as f:q=subprocess.run(cmd,cwd=U,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
  text=log.read_text(encoding='utf-8',errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:',text),text[-4000:];rows.append(dict(leg=leg,exit_code=0,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
  if leg=='initial_new_assets':
   for name in['curtain_left_painted.png','curtain_right_painted.png']:
    p=U/'assets/melody'/(name+'.import');t=p.read_text(encoding='utf-8');assert 'compress/mode=0'in t and '"vram_texture": false'in t;t=t.replace('mipmaps/generate=false','mipmaps/generate=true').replace('process/size_limit=0','process/size_limit=1024');p.write_text(t,encoding='utf-8',newline='\n')
 (W/'FINAL_RESULT.json').write_text(json.dumps(dict(state='PASS_NEW_NPOT_CURTAINS_LOSSLESS_MIPMAPS_NO_VRAM',legs=rows,settings='384x768 mode0 lossless/mipmaps true/size_limit1024; no existing import setting changed.'),indent=2)+'\n',encoding='utf-8');print('R120_NEW_CURTAINS_IMPORT_PASS',flush=True);subprocess.run([sys.executable,'-X','utf8','-B',str(S/'capture_native_candidate.py'),'candidate'],cwd=U,check=True)
except Exception as e:(S/'CANDIDATE_IMPORT_CAPTURE_STOP.json').write_text(json.dumps(dict(error=str(e),at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n',encoding='utf-8');raise
