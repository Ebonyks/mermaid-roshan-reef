from pathlib import Path
import json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');c=b/'audit/job_candy_workflow_current_v1_20261003';root=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp');p=root/'seal_candy_checkpoint_v537.py'
assert not (b/'tmp/candy_review_v_sealed_v537.json').exists()
backup=c/'review_tools/seal_candy_checkpoint_v537_before_bridge_order_fix.py';assert not backup.exists();shutil.copyfile(p,backup)
t=p.read_text(encoding='utf-8');old='for path in scope-{mp}:\n';assert t.count(old)==1
t=t.replace(old,"pending_bridge=(c/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V537.json').relative_to(b).as_posix()\n# This file is generated from the staged tested sources below, then separately staged and verified.\nfor path in scope-{mp,pending_bridge}:\n")
old="for p in sorted(scope-{mp})";assert t.count(old)==1;t=t.replace(old,"for p in sorted(scope-{mp,pending_bridge})")
p.write_text(t,encoding='utf-8',newline='\n');compile(t,str(p),'exec');shutil.copyfile(p,c/'review_tools/seal_candy_checkpoint_v537.py');shutil.copyfile(__file__,c/'review_tools/fix_checkpoint_bridge_order_v540.py')
record=dict(status='CHECKPOINT_BUILDER_ORDER_CORRECTED',second_error='AssertionError: audit/job_candy_workflow_current_v1_20261003/PUBLICATION_SOURCE_NEWLINE_BRIDGE_V537.json',cause='Builder tried to require its own staged-source newline bridge before generating that bridge from the staged source blobs.',correction='Only the builder-generated bridge is deferred from initial input-file validation and staging. It is generated from all783 frozen tested source members, independently staged, included in the final scope/map and checked byte-for-byte before sealing. Every real input and final output check remains blocking.',original_helper=backup.relative_to(b).as_posix(),effect='Both attempts stopped before final payload sealing, commit or push. No trusted validator, production source or artwork changed.')
(c/'SEAL_BUILDER_ORDER_FAILURE_V540.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
ip=b/'design/audit_impacts/job-candy-workflow-current-20261003.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in c.rglob('*') if x.is_file()});n=ip.with_name(ip.name+'.new');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');n.replace(ip)
print('Builder output order fixed; staged-source bridge and every final hash remain required. No commit/push.')
