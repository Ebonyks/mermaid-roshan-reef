"""Fresh source/document gates; no runtime/import/GPU work."""
from pathlib import Path
import json,hashlib,subprocess,datetime,sys
P=Path(__file__).resolve().parent;R=P.parents[3]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
commands=[[sys.executable,'-B',str(P/'verify_source_inventory.py')],[sys.executable,'-B',str(P/'validate.py')],[sys.executable,'-B','tools/audit_document_authority.py'],[sys.executable,'-B','tools/audit_development.py','--base','auto'],[sys.executable,'-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'],[sys.executable,'-B','tools/audit_game_2d.py','--regression-gate']];rows=[]
with (P/'gates.log').open('wb') as out:
 for cmd in commands:
  start=now();q=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);out.write(q.stdout);out.flush();rows.append({'command':cmd,'started_at_utc':start,'checked_at_utc':now(),'exit_code':q.returncode,'execution':'FRESH','evidence':'gates.log'});print('R37_GATE',q.returncode,cmd[-1],flush=True)
  if q.returncode:break
result={'status':'PASS_SOURCE_ONLY_ACCEPTANCE_OPEN' if len(rows)==len(commands) and all(x['exit_code']==0 for x in rows) else 'FAIL','commands':rows,'raw_log_sha256':hashlib.sha256((P/'gates.log').read_bytes()).hexdigest(),'scope':'Fresh source/canonical/document/impact/unittest andactual2Dregression. Actual priorR32full82/R35CI retainedatbyteidenticalproduction,notnewR37execution. Sourcecounts notartpieces;QA11/device/child/owner/globalclosure open.'};(P/'GATES.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n');sys.exit(0 if result['status'].startswith('PASS') else 1)
