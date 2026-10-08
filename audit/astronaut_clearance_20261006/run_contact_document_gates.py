from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,time
root=Path(__file__).resolve().parents[2];packet=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
names=['audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','scripts/opera_astronaut_surface.gd','scripts/opera_career_world_2d.gd','scripts/opera_roshan_actor.gd','scripts/opera_gesture_surface.gd','scripts/probe_opera_gesture_quality.gd','scripts/save_state.gd','audit/astronaut_clearance_20261006/verify_birthday_contact_v1.gd','audit/astronaut_clearance_20261006/run_birthday_contact_v1.py','audit/astronaut_clearance_20261006/run_contact_document_gates.py','audit/astronaut_clearance_20261006/CONTACT_BASELINE_REVIEW.json','audit/astronaut_clearance_20261006/ASTRONAUT_PARK_ACTION_PILOT_BRIEF.json']
sources=[{'path':n,'sha256':sha(root/n)} for n in names]
log=packet/'CONTACT_DOCUMENT_GATES_LOG.txt';receipt=packet/'CONTACT_DOCUMENT_GATES_RECEIPT.json';assert not log.exists() and not receipt.exists()
commands=[('Contact diagnostic parser',[sys.executable,'-B','-m','gdtoolkit.parser','audit/astronaut_clearance_20261006/verify_birthday_contact_v1.gd']),('Contact diagnostic inference',[sys.executable,'-B','tools/lint_inference.py','audit/astronaut_clearance_20261006/verify_birthday_contact_v1.gd']),('Document authority',[sys.executable,'-B','tools/audit_document_authority.py']),('Authority/development unit',[sys.executable,'-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']),('Authority stress',[sys.executable,'-B','tools/audit_document_authority.py','--stress']),('Audit impact coverage',[sys.executable,'-B','tools/audit_development.py','--base','auto']),('Whitespace',['git','diff','--check','HEAD'])]
t=time.monotonic();started=utc();steps=[]
with log.open('xb') as out:
 for label,cmd in commands:
  out.write(('\nSTEP '+label+'\n').encode());out.flush();process=subprocess.Popen(cmd,cwd=root,stdout=out,stderr=subprocess.STDOUT);print(json.dumps({'label':label,'owned_pid':process.pid}),flush=True);timed_out=False
  try:process.wait(timeout=max(1,180-(time.monotonic()-t)))
  except subprocess.TimeoutExpired:timed_out=True;process.terminate();process.wait(timeout=15)
  steps.append({'label':label,'command':cmd,'owned_pid':process.pid,'exit_code':process.returncode,'timed_out':timed_out})
  if timed_out:break
lines=log.read_text(encoding='utf-8',errors='replace').splitlines();errors=[l for l in lines if any(x in l for x in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error'])];matched=all(sha(root/s['path'])==s['sha256'] for s in sources)
passed=len(steps)==len(commands) and all(s['exit_code']==0 and not s['timed_out'] for s in steps) and not errors and matched
result={'result':'PASS' if passed else 'FAIL','status':'TERMINAL','started_utc':started,'finished_utc':utc(),'steps':steps,'elapsed_seconds':round(time.monotonic()-t,2),'sources':sources,'source_bindings_still_match':matched,'errors':errors,'log_path':log.relative_to(root).as_posix(),'log_sha256':sha(log),'meaning':'Diagnostic source and canonical document traceability only. The separate actual contact baseline FAIL remains mandatory repair evidence; these structural passes never grant contact/visual/fullsuite/device/child/owner acceptance.'}
receipt.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'result':result['result'],'failed_steps':[s['label'] for s in steps if s['exit_code']!=0 or s['timed_out']],'errors':errors[:5],'source_bindings_still_match':matched,'receipt_sha256':sha(receipt)}),flush=True);sys.exit(0 if passed else 1)
