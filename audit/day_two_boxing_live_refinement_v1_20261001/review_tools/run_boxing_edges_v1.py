from pathlib import Path
import datetime,hashlib,json,os,subprocess,time,shutil
r=Path.cwd();f=r/'audit/day_two_boxing_live_refinement_v1_20261001';o=f/'native_edges_v1';assert not o.exists();o.mkdir()
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
script=(f/'capture_edge_gloves_v1.gd').relative_to(r).as_posix()
paths=['project.godot','scenes/main.tscn','scripts/main.gd','scripts/opera_boxing_surface.gd','scripts/opera_career_world_2d.gd','scripts/opera_gesture_surface.gd',script,'assets/opera/worlds/props/fx_dust_puff.png','assets/opera/worlds/widgets/refinement_v1/boxing_glove_left.png','assets/opera/worlds/widgets/refinement_v1/boxing_glove_right.png']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(r/p) for p in paths};rows=[]
env=os.environ.copy()
for k,n in [('APPDATA','Roaming'),('LOCALAPPDATA','Local')]:
    p=r/'tmp/boxing_edges_v1'/n;p.mkdir(parents=True,exist_ok=True);env[k]=str(p)
commands=[('parser',[py,'-X','utf8','-B','-m','gdtoolkit.parser','scripts/opera_boxing_surface.gd',script]),('inference',[py,'-X','utf8','-B','tools/lint_inference.py','scripts/opera_boxing_surface.gd',script])]
for i,s in enumerate(['scripts/opera_boxing_surface.gd',script]):commands.append((f'analyzer_{i}',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+s]))
commands.append(('native',[godot,'--path',str(r),'--windowed','--resolution','1280x720','--script','res://'+script,'--','--touch','--classic-touch-test']))
for name,cmd in commands:
    started=time.monotonic()
    with (o/(name+'.stdout.log')).open('wb') as out,(o/(name+'.stderr.log')).open('wb') as err:p=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
    rows.append(dict(name=name,command=cmd,exit=p.returncode,seconds=time.monotonic()-started));print(name,p.returncode,flush=True)
    if p.returncode:break
after={p:sha(r/p) for p in paths};passed=len(rows)==len(commands) and all(x['exit']==0 for x in rows) and before==after
(o/'PROCESS_RECEIPT.json').write_text(json.dumps(dict(status='PASS' if passed else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=rows,source_before=before,source_after=after,source_unchanged=before==after,qualification='Current production source local-handler/native actual local-handler boundary fixture checks. Engine import diagnostics retained. No ordinary-route, continuous playback, phone or owner acceptance.'),indent=2)+'\n',encoding='utf-8')
review_tools=f/'review_tools';review_tools.mkdir(exist_ok=True);shutil.copyfile(Path(__file__),review_tools/Path(__file__).name)
raise SystemExit(0 if passed else 1)
