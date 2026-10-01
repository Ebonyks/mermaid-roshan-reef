from pathlib import Path
import os,json,hashlib,subprocess,datetime,time,shutil
r=Path.cwd();f=r/'audit/day_two_boxing_puff_reuse_v1_20261001';out=f/'native_timed_reuse_v1';assert not out.exists();out.mkdir()
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';script=(f/'capture_unbound_timed_reuse.gd').relative_to(r).as_posix()
paths=['project.godot','scenes/main.tscn','scripts/main.gd','scripts/opera_career_world_2d.gd','scripts/opera_boxing_surface.gd',script,'assets/opera/worlds/props/fx_bop_puff.png','assets/opera/worlds/props/fx_dust_puff.png']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(r/p) for p in paths}
env=os.environ.copy()
for k,n in [('APPDATA','Roaming'),('LOCALAPPDATA','Local')]:
 p=r/'tmp/boxing_puff_native_timed_reuse_v1'/n;p.mkdir(parents=True,exist_ok=True);env[k]=str(p)
results=[]
commands=[('parser',[py,'-X','utf8','-B','-m','gdtoolkit.parser',script]),('inference',[py,'-X','utf8','-B','tools/lint_inference.py',script]),('analyzer',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+script]),('native',[godot,'--path',str(r),'--windowed','--resolution','1280x720','--script','res://'+script,'--','--touch','--classic-touch-test'])]
for name,cmd in commands:
 t=time.monotonic()
 with (out/(name+'.stdout.log')).open('wb') as o,(out/(name+'.stderr.log')).open('wb') as e:q=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e,creationflags=subprocess.CREATE_NO_WINDOW)
 results.append({'name':name,'command':cmd,'exit':q.returncode,'seconds':time.monotonic()-t});print(name,q.returncode,flush=True)
 if q.returncode:break
after={p:sha(r/p) for p in paths};passed=len(results)==4 and all(x['exit']==0 for x in results) and before==after
(out/'PROCESS_RECEIPT.json').write_text(json.dumps({'status':'PASS' if passed else 'FAIL_PRESERVED','processes':results,'source_before':before,'source_after':after,'source_unchanged':before==after,'qualification':'Unbound timed actual-viewport one-punch boxing puff fit; no live binding or visual acceptance.'},indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if passed else 1)
