"""Bounded artifact/document checks only; this is not the full trusted suite."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,time

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
started=time.monotonic();start_utc=datetime.now(timezone.utc).isoformat()
binding=json.loads((OUT/'SOURCE_BINDINGS.json').read_text())
frozen={'manifest':sha(OUT/'MANIFEST.json'),'sources':binding['captured_source_sha256']}
steps=[];errors=[];lines=[];cap=88.608
commands=[('artifact parity',[sys.executable,'-X','utf8','-B',str(OUT/'verify_walkthrough_v2.py')]),
 ('document authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),
 ('development coverage',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto']),
 ('whitespace',['git','diff','--check'])]
for name,command in commands:
 remaining=cap-(time.monotonic()-started)
 if remaining<=0:errors.append('remaining88.608s cap before '+name);break
 tick=time.monotonic()
 try:
  result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=remaining)
  output=result.stdout+result.stderr
  lines.extend(['STEP | '+name,'COMMAND | '+json.dumps(command),output,'EXIT | '+str(result.returncode)])
  steps.append({'label':name,'command':command,'exit':result.returncode,'elapsed_seconds':round(time.monotonic()-tick,3)})
  if result.returncode:errors.append(name+' returned '+str(result.returncode));break
 except subprocess.TimeoutExpired as exc:
  lines.extend(['STEP | '+name,'TIMEOUT | remaining88.608s cap',str(exc.stdout or ''),str(exc.stderr or '')]);errors.append(name+' timed out');break
source_match=all(sha(ROOT/p)==h for p,h in frozen['sources'].items())
manifest_match=sha(OUT/'MANIFEST.json')==frozen['manifest']
if not source_match or not manifest_match:errors.append('frozen source or manifest changed during gates')
result='PASS' if not errors and len(steps)==len(commands) else 'FAIL'
lines+=['RESULT | '+result,'SCOPE | Artifact/document checks only; no full trusted suite or runtime/visual4.6 acceptance.']
log=OUT/'DOCUMENT_GATES_V2_LOG.txt';log.write_text('\n'.join(lines)+'\n',encoding='utf-8')
receipt={'result':result,'started_utc':start_utc,'finished_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':round(time.monotonic()-started,3),'aggregate_cap_seconds':cap,'retained_parent_spent_seconds':1.392,'original_aggregate_cap_seconds':90,'steps':steps,'errors':errors,'source_bindings_unchanged':source_match,'manifest_unchanged':manifest_match,'manifest_sha256':frozen['manifest'],'log_sha256':sha(log),'engine_launches':0,'scope':'Document/artifact verification only; full trusted suite, native/browser UI, independent/device/child/owner and GitHub publication pending.'}
(OUT/'DOCUMENT_GATES_V2_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt));raise SystemExit(0 if result=='PASS' else 1)
