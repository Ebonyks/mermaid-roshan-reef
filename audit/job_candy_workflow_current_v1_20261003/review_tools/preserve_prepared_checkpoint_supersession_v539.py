from pathlib import Path
import datetime,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');c=b/'audit/job_candy_workflow_current_v1_20261003'
def write(p,d):
 n=p.with_name(p.name+'.new');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');n.replace(p)
for name in ['SCOPED_PUBLICATION_BOUNDARY_V527.json','INDEX_PATH_LENGTH_V527.json','PUBLICATION_SOURCE_NEWLINE_BRIDGE_V527.json']:
 p=c/name;assert not p.exists();write(p,dict(status='NOT_RUN_PREPARED_PLAN_SUPERSEDED',prepared_version='V527',superseding_version='V537',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),qualification='Earlier Candy-only sealing was prepared while fullCI was still pending and before the18-source/104-cell entrance review. It was never run or sealed. This is a literal not-run history receipt, not source/length/newline PASS evidence. The separately named V537 receipts own the actual expanded checkpoint checks.'))
write(c/'SEAL_PREPARATION_FAILURE_V537.json',dict(status='PRESERVED_MISSING_PREPARED_HISTORY_PATH_FAILURE',error='AssertionError: audit/job_candy_workflow_current_v1_20261003/PUBLICATION_SOURCE_NEWLINE_BRIDGE_V527.json',effect='Expanded sealer stopped while validating scope file existence, before staging its expanded payload or creating the final closed map/seal. No commit, push, production or original artwork change.',cause='The previous --prepare impact included three intended V527 evidence paths but the earlier sealer was never run after the audit grew.',correction='Preserve all three planned paths as explicit NOT_RUN_PREPARED_PLAN_SUPERSEDED history receipts. They do not inherit PASS. Fresh V537 actual checks remain blocking.'))
shutil.copyfile(__file__,c/'review_tools/preserve_prepared_checkpoint_supersession_v539.py')
ip=b/'design/audit_impacts/job-candy-workflow-current-20261003.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in c.rglob('*') if p.is_file()});write(ip,d)
print('Prior prepared evidence paths recorded as explicitly NOT_RUN; failed scope check preserved; no commit/push.')
