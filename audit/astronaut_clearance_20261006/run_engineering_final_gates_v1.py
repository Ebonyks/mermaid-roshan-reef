from pathlib import Path
import subprocess,json,hashlib,datetime,time,sys,re
ROOT=Path(__file__).resolve().parents[2]; AD=Path(__file__).resolve().parent
RECEIPT=AD/'ENGINEERING_FINAL_GATES_V1_RECEIPT.json'; LOG=AD/'ENGINEERING_FINAL_GATES_V1_LOG.txt'; BIND=AD/'ENGINEERING_FINAL_GATES_V1_SOURCE_BINDINGS.json'
assert json.loads(RECEIPT.read_text())['result']=='PREPARED' and LOG.stat().st_size==0
names=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMR'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).splitlines()
excluded={RECEIPT.relative_to(ROOT).as_posix(),LOG.relative_to(ROOT).as_posix(),BIND.relative_to(ROOT).as_posix()}
bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in names if p not in excluded and (ROOT/p).is_file()}
BIND.write_text(json.dumps(bindings,indent=2)+'\n',encoding='utf-8')
gd=[p for p in names if p.endswith('.gd')]
commands=[[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',*gd],[sys.executable,'-X','utf8','-B','tools/lint_inference.py',*gd],[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py'],[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto']]
steps=[];start=time.monotonic()
with LOG.open('ab') as log:
 for argv in commands:
  t=time.monotonic();p=subprocess.run(argv,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=180)
  steps.append({'argv':argv,'exit_code':p.returncode,'elapsed_seconds':time.monotonic()-t});print('FINAL_GATE|'+argv[5]+'|'+str(p.returncode),flush=True)
  if p.returncode:break
changed=[p for p,h in bindings.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
ci=json.loads((AD/'ENGINEERING_FULL_CI_V1_SOURCE_BINDINGS.json').read_text()); postci=[p for p,h in ci.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
allowed=['audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/audit_impacts/astronaut-clearance-20261006.json']
unexpected=[p for p in postci if p not in allowed]
result='PASS' if len(steps)==len(commands) and all(x['exit_code']==0 for x in steps) and not changed and not unexpected else 'FAIL'
r={'result':result,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'changed_gd_count':len(gd),'steps':steps,'source_binding_count':len(bindings),'source_changes_during_gates':changed,'intentional_post_ci_metadata_changes':postci,'unexpected_post_ci_changes':unexpected,'log_sha256':hashlib.sha256(LOG.read_bytes()).hexdigest(),'limits':'Metadata currency after complete82probe CI, current92+92native and70stills. Current runtime/art/audio/CI/tool bytes remain the full-CI bytes. Exact-head remoteCI, full-speed/independent/4.6/device/child/owner acceptance remain separate.'}
RECEIPT.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('FINAL_GATE|'+result,flush=True);raise SystemExit(0 if result=='PASS' else 1)
