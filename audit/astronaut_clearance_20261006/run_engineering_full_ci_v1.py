from pathlib import Path
import subprocess,os,json,hashlib,datetime,time,re
ROOT=Path(__file__).resolve().parents[2]
AD=Path(__file__).resolve().parent
BASH=Path('C:/Program Files/Git/bin/bash.exe')
PLAN=json.loads((AD/'ENGINEERING_FULL_CI_V1_PLAN.json').read_text(encoding='utf-8'))
assert hashlib.sha256(Path(PLAN['engine']).read_bytes()).hexdigest()==PLAN['engine_sha256']
log=AD/'ENGINEERING_FULL_CI_V1_LOG.txt'
receipt=AD/'ENGINEERING_FULL_CI_V1_RECEIPT.json'
assert not log.exists() and not receipt.exists()
paths=subprocess.check_output(['git','ls-files','--cached'],cwd=ROOT,text=True).splitlines()
paths=[p for p in paths if p=='project.godot' or p=='scripts/ci.sh' or p.startswith('scripts/') and p.endswith('.gd') or p.startswith('tools/') and p.endswith('.py') or p.startswith('assets/') and p.endswith(('.png','.ogg','.import')) or p.startswith('design/audit_impacts/') or p in ['design/05_DOC_LEDGER.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/audio_quality_ledger_2026-08-24.csv','audit/audio_quality_summary_2026-08-24.json']]
bind={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths if (ROOT/p).is_file()}
(AD/'ENGINEERING_FULL_CI_V1_SOURCE_BINDINGS.json').write_text(json.dumps(bind,indent=2)+'\n',encoding='utf-8')
env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
argv=[str(BASH),'audit/astronaut_clearance_20261006/run_engineering_full_ci_v1.sh']
start=time.monotonic()
with log.open('xb') as out:
 proc=subprocess.Popen(argv,cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
 print('ENGINEERING_FULL_CI|START|PID'+str(proc.pid),flush=True)
 receipt.write_text(json.dumps({'result':'RUNNING','pid':proc.pid,'argv':argv,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan':'ENGINEERING_FULL_CI_V1_PLAN.json'},indent=2)+'\n',encoding='utf-8')
 try:rc=proc.wait(timeout=PLAN['run_cap_seconds']+60)
 except subprocess.TimeoutExpired:
  subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  rc=proc.wait(timeout=15)
text=log.read_text(encoding='utf-8',errors='replace')
probe_exits=[{'probe':name,'exit_code':int(code)} for name,code in re.findall(r'^PROBE (\S+) process exit: (\d+)',text,re.M)]
changed=[p for p,h in bind.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
result='PASS' if rc==0 and probe_exits and all(row['exit_code']==0 for row in probe_exits) and not changed else 'FAIL'
data={'result':result,'exit_code':rc,'elapsed_seconds':time.monotonic()-start,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':argv,'engine_sha256':PLAN['engine_sha256'],'probe_exits':probe_exits,'source_binding_count':len(bind),'source_changes':changed,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'limits':'Unmodified complete local CI; source-bound machine lane only. Native/independent/device/child/owner/4.6/art acceptance and exact-head remote CI remain separate.'}
receipt.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('ENGINEERING_FULL_CI|'+('ALL OK' if result=='PASS' else 'FAIL')+'|'+str(len(probe_exits))+' probes|'+str(round(data['elapsed_seconds'],3))+' seconds',flush=True)
raise SystemExit(0 if result=='PASS' else 1)
