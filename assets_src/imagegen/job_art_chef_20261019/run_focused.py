from pathlib import Path
import hashlib,json,os,subprocess,time,sys,re
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent/'verification'
out.mkdir(exist_ok=True)
engine='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[root/'scripts'/name for name in ['chef_painted_art.gd','opera_gesture_surface.gd','opera_chef_surface.gd','opera_career_world_2d.gd','opera_world_backdrop_2d.gd']]
pins={p.relative_to(root).as_posix():sha(p) for p in sources}
records=[]
revision=sys.argv[1] if len(sys.argv)>1 else '01'
assert revision.isdigit()
ci=(root/'scripts/ci.sh').read_text()
failure=re.search(r"FAILURE_RE='([^']+)'",ci).group(1)
runtime=re.search(r"RUNTIME_ERROR_RE='([^']+)'",ci).group(1)
for name in ['opera_gesture_quality','opera_2d','chapter2_farmer_resume','chapter2']:
    log=out/(name+'_focused_'+revision+'.log')
    assert not log.exists(),'Preserve earlier transcripts'
    env=os.environ.copy();env['APPDATA']=str(root/'tmp'/('chef_focused_user_'+revision)/name);env['PYTHONUTF8']='1'
    assert not Path(env['APPDATA']).exists(),'Every probe requires a fresh save home'
    Path(env['APPDATA']).mkdir(parents=True)
    start=time.monotonic()
    with log.open('wb') as handle:
        run=subprocess.run([engine,'--headless','--path',str(root),'-s','scripts/probe_'+name+'.gd'],cwd=root,env=env,stdout=handle,stderr=subprocess.STDOUT,timeout=720)
    transcript=log.read_text('utf-8',errors='replace')
    record={'probe':name,'exit':run.returncode,'elapsed_seconds':round(time.monotonic()-start,3),'log_sha256':sha(log),
        'status':'PASS' if run.returncode==0 and transcript.strip() and not re.search(failure+'|'+runtime,transcript) else 'FAIL'}
    records.append(record);print(json.dumps(record),flush=True)
drift=[name for name,h in pins.items() if sha(root/name)!=h]
receipt={'status':'PASS' if all(r['status']=='PASS' for r in records) and not drift else 'FAIL','records':records,'source_sha256':pins,'source_drift':drift,'limits':'Focused machine lane only; no visual, motion, device or owner acceptance.'}
(out/('focused_'+revision+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
raise SystemExit(0 if receipt['status']=='PASS' else 1)
