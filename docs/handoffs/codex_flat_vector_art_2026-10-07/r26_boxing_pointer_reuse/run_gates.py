"""Run applicable evidence/document gates,retaining exact command bytes."""
from pathlib import Path
import subprocess,json,hashlib,datetime,sys
P=Path(__file__).resolve().parent;R=P.parents[3];receipt='--receipt' in sys.argv
commands=[[sys.executable,'-B',str(P/'validate.py')],[sys.executable,'-B','tools/audit_document_authority.py'],[sys.executable,'-B','tools/audit_development.py','--base','auto']]
if not receipt:commands.append([sys.executable,'-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'])
commands.append([sys.executable,'-B','tools/audit_game_2d.py','--regression-gate'])
log=P/('receipt_gates.log' if receipt else 'gates.log');rows=[]
report=P/('RECEIPT_GATES.json' if receipt else 'GATES.json')
if not report.exists():report.write_text(json.dumps({'status':'PENDING','scope':'Report initialized before linked-document checks; no pass claimed'})+'\n',encoding='utf-8',newline='\n')
with log.open('wb') as out:
 for cmd in commands:
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();print('START',cmd[-2:],flush=True);q=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);out.write(q.stdout);out.flush();rows.append({'command':cmd,'started_at_utc':start,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':q.returncode,'result':'PASS' if q.returncode==0 else 'FAIL','evidence':log.name});print('RESULT',q.returncode,flush=True)
  if q.returncode:break
result={'status':'PASS_WITH_ACCEPTANCE_OPEN' if all(x['exit_code']==0 for x in rows) else 'FAIL','commands':rows,'raw_log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'scope':'Nonruntime Boxing first-phase whole-source reuse diagnostic;production/source pixels unchanged;inherited R16 exact82 trusted native passes. New fixture checks separate;no art generation/replacement/acceptance. Global/QA11/device/child/owner remain open.'}
(P/('RECEIPT_GATES.json' if receipt else 'GATES.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n');sys.exit(0 if result['status'].startswith('PASS') else 1)
