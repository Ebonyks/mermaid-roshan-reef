"""Replay ci.sh trusted probes with native Windows process waiting, no shell wrapper.
Static gates/import are separately recorded from the unchanged final candidate.
No production code or probe verdict is changed by this diagnostic runner.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess,tempfile,time
root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--probes', nargs='*')
parser.add_argument('--tag', default='native_suite_isolated')
args=parser.parse_args()
ci=(root/'scripts/ci.sh').read_text(encoding='utf-8')
names=re.search(r'^for p in (.+); do$',ci,re.M).group(1).split()
if args.probes:
    assert all(x in names for x in args.probes)
    names=args.probes
source=json.loads((root/'audit/chef_overdraw_20261003/CANDIDATE_SOURCE.json').read_text(encoding='utf-8'))
for row in source['files']:
    assert hashlib.sha256((root/row['path']).read_bytes()).hexdigest()==row['filesystem_sha256'], row['path']
engine='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
version=subprocess.check_output([engine,'--version'],text=True).strip()
assert version=='4.7.2.stable.official.ed1daf0bf',version
assert re.fullmatch(r'[a-z0-9_]+',args.tag)
out=root/'audit/chef_overdraw_20261003'/args.tag
out.mkdir(exist_ok=True)
rows=[]
hybrid={'probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'}
failures=re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error')
for name in names:
    home=Path(tempfile.mkdtemp(prefix=name+'-',dir=root/'tmp'))
    env=os.environ.copy()
    for key,folder in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
        path=home/folder;path.mkdir();env[key]=str(path)
    log=out/(name+'.log')
    command=[engine,'--headless','--verbose','--path',str(root),'-s','scripts/'+name+'.gd','--','--touch','--hybrid-touch-test' if name in hybrid else '--classic-touch-test']
    print('=== '+name+' ===',flush=True)
    started=time.monotonic()
    with log.open('wb') as f:
        try:
            run=subprocess.run(command,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=480,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW)
            code=run.returncode
        except subprocess.TimeoutExpired:
            code=124
    text=log.read_text(encoding='utf-8',errors='replace')
    hard=bool(failures.search(text))
    row={'probe':name,'command':command,'exit_code':code,'hard_failure':hard,'seconds':round(time.monotonic()-started,3),'log':log.relative_to(root).as_posix(),'sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
    rows.append(row)
    print('PROBE '+name+' process exit: '+str(code)+' hard_failure='+str(hard),flush=True)
    manifest={'engine':version,'runtime_source':source,'runner':Path(__file__).relative_to(root).as_posix(),'expected_probe_count':len(names),'full_ci_probe_count':len(re.search(r'^for p in (.+); do$',ci,re.M).group(1).split()),'rows':rows,'result':'RUNNING','method':'Native Windows subprocess waiting with separate process group/no console window and fresh per-probe save roots; same trusted scripts and touch modes as ci.sh, verbose diagnostics only. Static gates/import reference full_ci_final.log; no failed shell attempt is converted into a pass.'}
    (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    if code!=0 or hard:
        print('NATIVE_SUITE_STOPPED_ON_FAILURE',flush=True)
        break
manifest['result']='ALL OK' if len(rows)==len(names) and all(x['exit_code']==0 and not x['hard_failure'] for x in rows) else 'FAIL'
manifest['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('NATIVE_PROBE_SUITE '+manifest['result'],flush=True)
raise SystemExit(0 if manifest['result']=='ALL OK' else 1)
