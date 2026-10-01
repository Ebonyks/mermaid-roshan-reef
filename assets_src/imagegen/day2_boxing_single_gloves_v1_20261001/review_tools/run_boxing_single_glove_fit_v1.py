from pathlib import Path
import datetime, hashlib, json, os, subprocess, time
r=Path.cwd();f=r/'assets_src/imagegen/day2_boxing_single_gloves_v1_20261001';out=f/'native_static_fit_v1'
assert not out.exists();out.mkdir()
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
scripts=[(f/p).relative_to(r).as_posix() for p in ['normalize_whole_canvas.gd','unbound_glove_surface.gd','capture_unbound_glove_fit.gd']]
env=os.environ.copy()
for k,name in [('APPDATA','Roaming'),('LOCALAPPDATA','Local')]:
 p=r/'tmp/boxing_single_glove_fit_v1'/name;p.mkdir(parents=True,exist_ok=True);env[k]=str(p)
rows=[]
def run(name,cmd):
 started=time.monotonic()
 with (out/(name+'.stdout.log')).open('wb') as o,(out/(name+'.stderr.log')).open('wb') as e:q=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e,creationflags=subprocess.CREATE_NO_WINDOW)
 rows.append(dict(name=name,command=cmd,exit=q.returncode,seconds=time.monotonic()-started));print(name,q.returncode,flush=True)
 return q.returncode==0
commands=[('parser',[py,'-X','utf8','-B','-m','gdtoolkit.parser',*scripts]),('inference',[py,'-X','utf8','-B','tools/lint_inference.py',*scripts])]
commands.extend((f'analyzer_{i}',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+s]) for i,s in enumerate(scripts))
commands.append(('normalize',[godot,'--headless','--path',str(r),'--script','res://'+scripts[0]]))
for name,cmd in commands:
 if not run(name,cmd):
  (out/'PROCESS_RECEIPT.json').write_text(json.dumps(dict(status='FAIL_PRESERVED',processes=rows),indent=2)+'\n',encoding='utf-8');raise SystemExit(1)
paths=['project.godot','scenes/main.tscn','scripts/main.gd','scripts/opera_career_world_2d.gd','scripts/opera_boxing_surface.gd','scripts/opera_gesture_surface.gd','assets/opera/worlds/widgets/widget_push_boxer_mover.png','assets/opera/worlds/props/fx_dust_puff.png',*scripts]+[(f/p).relative_to(r).as_posix() for p in ['left_attempt_02_native.png','right_attempt_01_native.png','left_whole_canvas_1024.png','right_whole_canvas_1024.png']]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(r/p) for p in paths}
native_ok=run('native',[godot,'--path',str(r),'--windowed','--resolution','1280x720','--script','res://'+scripts[2],'--','--touch','--classic-touch-test'])
after={p:sha(r/p) for p in paths}
(out/'PROCESS_RECEIPT.json').write_text(json.dumps(dict(status='PASS' if native_ok and before==after else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=rows,source_before=before,source_after=after,source_unchanged=before==after,qualification='Exact4.7.2 native static appearance-only diagnostic subclass; all gameplay methods inherited and zero awards; no actual route/input/action acceptance.'),indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if native_ok and before==after else 1)
