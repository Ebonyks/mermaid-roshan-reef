from pathlib import Path
import hashlib,json,subprocess,os
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019';v=s/'verification';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pins={p.relative_to(r).as_posix():sha(p) for p in list((r/'scripts').rglob('*.gd'))+list((r/'assets/opera/worlds/nursery_quality_20261019').glob('*.png'))};records=[]
engine='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe'
for name in ['probe_opera_nursery','probe_opera_gesture_quality','probe_opera_2d']:
 private=r/'tmp'/('p5_focused01_'+name);assert not private.exists();(private/'Roaming').mkdir(parents=True);(private/'Local').mkdir();env=os.environ.copy();env['APPDATA']=str(private/'Roaming');env['LOCALAPPDATA']=str(private/'Local');log=v/(name+'_focused01.log')
 with log.open('wb') as output:q=subprocess.run([engine,'--headless','--path',str(r),'--script','res://scripts/'+name+'.gd'],stdout=output,stderr=subprocess.STDOUT,env=env,timeout=480)
 t=log.read_text('utf-8',errors='replace');ok=q.returncode==0 and 'ALL OK' in t and '|FAIL|' not in t and 'SCRIPT ERROR' not in t;records.append({'probe':name,'exit':q.returncode,'status':'PASS' if ok else 'FAIL','log':log.relative_to(r).as_posix(),'sha256':sha(log)});print(name,records[-1]['status'],q.returncode,flush=True)
 if not ok:print(t[-3000:],flush=True)
drift=[p for p,h in pins.items() if sha(r/p)!=h];status='PASS' if all(x['status']=='PASS' for x in records) and not drift else 'FAIL';(v/'focused01.json').write_text(json.dumps({'status':status,'records':records,'source_sha256':pins,'source_drift':drift,'isolation':'Fresh APPDATA and LOCALAPPDATA per probe; no unsupported user-data-dir flag.'},indent=2)+'\n');raise SystemExit(0 if status=='PASS' else 1)
