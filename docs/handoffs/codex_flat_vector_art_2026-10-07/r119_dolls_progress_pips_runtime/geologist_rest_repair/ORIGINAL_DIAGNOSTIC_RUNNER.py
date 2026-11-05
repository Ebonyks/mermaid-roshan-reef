from pathlib import Path
import os,json,subprocess,hashlib,datetime
R=Path.cwd();S=Path(__file__).parent;D=S/'opera2d_staging_diagnostic';E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe')
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',R119_GEO_DIAG_OUT=str(D/'GEOMETRY.json'))
for k,n in[('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=D/n;p.mkdir();env[k]=str(p)
cmd=[str(E),'--verbose','--log-file',str(D/'native_engine.log'),'--headless','--path',str(R),'-s','res://export/flat_vector_r119/opera2d_staging_diag.gd','--','--touch','--classic-touch-test']
with(D/'engine.log').open('wb')as f:q=subprocess.run(cmd,cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,timeout=480,creationflags=0x08000000)
out=dict(state='DIAGNOSTIC_TERMINAL_NOT_TRUSTED_GATE',exit_code=q.returncode,command=cmd,log_sha256=hashlib.sha256((D/'engine.log').read_bytes()).hexdigest(),geometry_written=(D/'GEOMETRY.json').exists(),completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());(D/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8');print(json.dumps(out),flush=True)
