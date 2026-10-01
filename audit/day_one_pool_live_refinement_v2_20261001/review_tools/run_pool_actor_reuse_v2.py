from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, time

root=Path(__file__).resolve().parents[1];family=root/'audit/day_one_pool_live_refinement_v2_20261001'
base=family/'actor_reuse_inventory_v1';out=base/'native_mount_v2'
assert not out.exists(),'Preserve every prior unbound fit attempt.';out.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
script=(base/'capture_pose_mount_candidates_v2.gd').relative_to(root).as_posix()
sources=[script,'scripts/games/pool_skimmer_activity.gd','scripts/games/day_one_pool_cleanup.gd','scripts/main.gd',
 'assets/characters/roshan_25d/roshan_gesture_c.png','assets/characters/roshan_25d/roshan_gesture_d.png','assets/characters/roshan_25d/roshan_play_a.png',
 'assets/castle/day_one_pool/activities/refinement_v2/pool_skimmer.png']
before={p:sha(root/p) for p in sources}
env=os.environ.copy();env['POOL_REUSE_CAPTURE_OUT']=str(out)
for key,name in [('APPDATA','Roaming'),('LOCALAPPDATA','Local')]:
 p=root/'tmp/pool_actor_reuse_native_v1'/name;p.mkdir(parents=True,exist_ok=True);env[key]=str(p)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
python='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
commands=[('parser',[python,'-X','utf8','-B','-m','gdtoolkit.parser',script]),
 ('inference',[python,'-X','utf8','-B','tools/lint_inference.py',script]),
 ('analyzer',[godot,'--headless','--path',str(root),'--check-only','--script','res://'+script]),
 ('native',[godot,'--path',str(root),'--windowed','--resolution','1280x720','--script','res://'+script,'--','--touch','--classic-touch-test'])]
results=[]
for name,command in commands:
 started=time.monotonic()
 with (out/(name+'.stdout.log')).open('wb') as stdout,(out/(name+'.stderr.log')).open('wb') as stderr:
  result=subprocess.run(command,cwd=root,env=env,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
 results.append({'name':name,'command':command,'process_exit':result.returncode,'elapsed_seconds':time.monotonic()-started})
 if result.returncode:break
after={p:sha(root/p) for p in sources}
receipt={'status':'PASS_UNBOUND_STATIC_VIEWS' if all(r['process_exit']==0 for r in results) and len(results)==4 and before==after else 'FAIL_PRESERVED',
 'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':results,'source_before':before,'source_after':after,'source_unchanged':before==after,
 'qualification':'Explicit prospective reuse fixture, not production textures/poses/actions. No progress awards. Source purpose and mounted/timed acceptance remain separate. No original/protected art or production controller changes.'}
(out/'PROCESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
licenses=root/'ASSET_LICENSES.md';text=licenses.read_text(encoding='utf-8');rows=[]
for p in sorted(out.glob('*.webp')):
 rel=p.relative_to(root).as_posix();rows.append(f'| `{rel}` | Godot4.7.2 diagnostic of owner-approved complete Roshan atlas cells and pool sources; original rights retained | actor_reuse_inventory_v1/native_mount_v2/CAPTURE_RECEIPT.json exact source/output hashes | Unbound whole-cell flip and declared complete-card/skimmer fit; no source pixel editing or production binding. Full1280x720 lossless diagnostic only. |')
if rows:licenses.write_text(text.rstrip()+'\n'+'\n'.join(rows)+'\n',encoding='utf-8')
impact=root/'design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json';d=json.loads(impact.read_text())
d['files']=sorted(set(d['files'])|{p.relative_to(root).as_posix() for p in family.rglob('*') if p.is_file()})
d['validation'].append({'command':'Exact4.7.2 parser/inference/analyzer and unbound five-pose pool tool-fit fixture','result':'PASS' if receipt['status']=='PASS_UNBOUND_STATIC_VIEWS' else 'FAIL','evidence':(out/'PROCESS_RECEIPT.json').relative_to(root).as_posix()+'; no progress awards; direct mounted visual review still separate.'})
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':receipt['status'],'views':len(rows),'source_unchanged':before==after,'commands':[(r['name'],r['process_exit']) for r in results]}),flush=True)
raise SystemExit(0 if receipt['status']=='PASS_UNBOUND_STATIC_VIEWS' else 1)
