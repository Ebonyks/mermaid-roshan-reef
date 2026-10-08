from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,time
root=Path(__file__).resolve().parents[2];packet=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
python='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
impact=json.loads((root/'design/audit_impacts/astronaut-clearance-20261006.json').read_text(encoding='utf-8'))
gd=[n for n in impact['files'] if n.endswith('.gd') and (root/n).exists()]
commands=[[python,'-X','utf8','-B','-m','gdtoolkit.parser',*gd],[python,'-X','utf8','-B','tools/lint_inference.py',*gd],[python,'-X','utf8','-B','tools/audit_document_authority.py'],[python,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'],[python,'-X','utf8','-B','tools/audit_document_authority_stress.py'],[python,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate'],[python,'-X','utf8','-B','tools/audit_development.py','--base','auto']]
log=packet/'FINAL_SOURCE_DOCUMENT_GATES_LOG.txt';receipt=packet/'FINAL_SOURCE_DOCUMENT_GATES_RECEIPT.json'
record=json.loads(receipt.read_text(encoding='utf-8'));assert record['status']=='PREFLIGHT' and log.stat().st_size==0
source_names=['scripts/opera_astronaut_surface.gd','scripts/opera_career_world_2d.gd','scripts/save_state.gd','scripts/probe_opera_gesture_quality.gd','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md']
record.update({'status':'RUNNING','started_utc':datetime.now(timezone.utc).isoformat(),'sources':[{'path':n,'sha256':sha(root/n)} for n in source_names],'changed_gd_count':len(gd),'results':[]})
receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
with log.open('ab') as output:
 for command in commands:
  result=subprocess.run(command,cwd=root,capture_output=True,timeout=180)
  text=(result.stdout+result.stderr).decode('utf-8',errors='replace');output.write(('COMMAND '+json.dumps(command)+'\n'+text+'\n').encode());output.flush()
  entry={'command':command,'exit_code':result.returncode,'result':'PASS' if result.returncode==0 else 'FAIL','summary':text.splitlines()[-7:]};record['results'].append(entry);receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'command':command[4:6],'result':entry['result'],'summary':entry['summary']}),flush=True)
record.update({'status':'TERMINAL','finished_utc':datetime.now(timezone.utc).isoformat(),'result':'PASS' if all(x['result']=='PASS' for x in record['results']) else 'FAIL','source_bindings_match':all(sha(root/x['path'])==x['sha256'] for x in record['sources']),'log_sha256':sha(log),'scope':'Final source/parser/inference, canonical facts,54unit,6stress,shrinking2D and exact staged coverage. Full scripts/ci.sh and native/device/child/owner acceptance remain pending.'})
receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'result':record['result'],'receipt_sha256':sha(receipt),'sources_match':record['source_bindings_match']}),flush=True)
raise SystemExit(0 if record['result']=='PASS' else 1)
