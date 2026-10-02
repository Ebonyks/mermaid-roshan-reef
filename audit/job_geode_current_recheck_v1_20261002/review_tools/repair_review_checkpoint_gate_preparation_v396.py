from pathlib import Path
import json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_current_recheck_v1_20261002'
for name in ['authority','development']:
 for suffix in ['stdout.log','stderr.log']:
  p=f/'runtime_gate'/f'{name}_final_v1.{suffix}';assert not p.exists();p.write_text('NOT RUN: exact stage validation required declared gate files to exist before launch. Preparation stopped before executing the audit command. See GATE_PREPARATION_FAILURE_V395.json.\n',encoding='utf-8')
 p=f/'runtime_gate'/f'{name}_final_v1.receipt.json';assert not p.exists();p.write_text(json.dumps(dict(status='NOT_RUN_PREPARATION_FAILED',actual_audit_command_executed=False,reason='Declared future logs/receipt did not yet exist when exact scope was validated before launch.',repair='prepare_current_review_checkpoint_p_v396.py'),indent=2)+'\n',encoding='utf-8')
(f/'GATE_PREPARATION_FAILURE_V395.json').write_text(json.dumps(dict(status='PRESERVED_PREPARATION_FAILURE',actual_audit_commands_executed=False,failures=['authority_final_v1.stdout.log declared but absent','authority_final_v1.stderr.log remained absent during next attempted preparation'],repair='Create explicit PENDING receipt and empty log files before exact stage checks, then execute unchanged authority/development tools as final_v2. No checker suppression, covered-path omission or waived gate.'),indent=2)+'\n',encoding='utf-8')
p=f/'review_tools/prepare_current_review_checkpoint_p_v395.py';s=p.read_text();s=s.replace('_final_v1','_final_v2').replace("stage();started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()", "paths[0].touch();paths[1].touch();write(paths[2],dict(status='PENDING_NOT_RUN',command=command));stage();started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()")
q=f/'review_tools/prepare_current_review_checkpoint_p_v396.py';assert not q.exists();q.write_text(s,encoding='utf-8',newline='\n');shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
print('Preparation failures preserved; unchanged audit tools ready for v2.')
