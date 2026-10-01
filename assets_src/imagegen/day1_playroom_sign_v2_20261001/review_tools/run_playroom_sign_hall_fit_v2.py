from pathlib import Path
import os,json,hashlib,subprocess,datetime,time,shutil
r=Path.cwd();f=r/'assets_src/imagegen/day1_playroom_sign_v2_20261001';out=f/'native_hall_fit_v2';assert not out.exists();out.mkdir()
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';script=(f/'capture_unbound_hall_fit_v2.gd').relative_to(r).as_posix()
paths=['project.godot','scenes/main.tscn','scripts/main.gd','scripts/arena/castle_rooms_25d.gd',script,'assets/flats/castle/main_hall_redraw_2026-08-03/signs/sign_playroom.png','assets_src/imagegen/day1_playroom_sign_v2_20261001/attempt_02_native.png','assets_src/imagegen/day1_playroom_sign_v2_20261001/attempt_02_whole_canvas_256.png']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(r/p) for p in paths}
env=os.environ.copy()
for k,n in [('APPDATA','Roaming'),('LOCALAPPDATA','Local')]:
 p=r/'tmp/playroom_sign_native_fit_v2'/n;p.mkdir(parents=True,exist_ok=True);env[k]=str(p)
results=[]
commands=[('parser',[py,'-X','utf8','-B','-m','gdtoolkit.parser',script]),('inference',[py,'-X','utf8','-B','tools/lint_inference.py',script]),('analyzer',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+script]),('native',[godot,'--path',str(r),'--windowed','--resolution','1280x720','--script','res://'+script,'--','--touch','--classic-touch-test'])]
for name,cmd in commands:
 t=time.monotonic()
 with (out/(name+'.stdout.log')).open('wb') as o,(out/(name+'.stderr.log')).open('wb') as e:q=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e,creationflags=subprocess.CREATE_NO_WINDOW)
 results.append({'name':name,'command':cmd,'exit':q.returncode,'seconds':time.monotonic()-t});print(name,q.returncode,flush=True)
 if q.returncode:break
after={p:sha(r/p) for p in paths};passed=len(results)==4 and all(x['exit']==0 for x in results) and before==after
(out/'PROCESS_RECEIPT.json').write_text(json.dumps({'status':'PASS' if passed else 'FAIL_PRESERVED','processes':results,'source_before':before,'source_after':after,'source_unchanged':before==after,'qualification':'Unbound static actual-hall fit; no live binding or visual acceptance.'},indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if passed else 1)
