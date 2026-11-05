"""Record actual scoped project gates; structural green is not visual acceptance."""
from pathlib import Path
import datetime,json,subprocess,sys
V=Path(__file__).resolve().parent;R=V.parents[4]
commands=[['tools/audit_document_authority.py'],['tools/audit_development.py','--base','auto'],['-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']]
checks=[]
for command in commands:
 result=subprocess.run([sys.executable,'-X','utf8','-B',*command],cwd=R,encoding='utf8',text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 row=dict(command='python -X utf8 -B '+' '.join(command),exit_code=result.returncode,output=result.stdout)
 checks.append(row);print(row['command'],result.returncode,flush=True);print(result.stdout[-2000:],flush=True)
record=dict(checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),checks=checks,scope='Static book and documentation; no engine/runtime probes applicable.')
(V/'project_gates.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
if any(q['exit_code'] for q in checks):raise SystemExit(1)
