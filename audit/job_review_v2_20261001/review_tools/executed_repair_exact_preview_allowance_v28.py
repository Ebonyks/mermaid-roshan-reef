from pathlib import Path
import json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');family=r/'audit/job_review_v2_20261001'
old=json.loads((family/'resource_checks_v6/RECEIPT.json').read_text(encoding='utf-8'))
missing=[x['path'] for x in old['resource_heads'] if not x['pass']]
assert missing==['audit/job_review_v2_20261001/full_ci_candidate_retry_v2/RECEIPT.json']
allow=r/'tmp/v2_preview_allowed.json';paths=set(json.loads(allow.read_text(encoding='utf-8')))
assert all((r/x).is_file() and not x.startswith(('.git/','.secrets/','.codex/','.aws/','.github/')) for x in missing)
paths.update(missing)
src=(family/'review_tools/check_distinct_review_resources_v7.py').read_text(encoding='utf-8').replace('resource_checks_v6','resource_checks_v7').replace('check_distinct_review_resources_v7.py','check_distinct_review_resources_v8.py')
checker=family/'review_tools/check_distinct_review_resources_v8.py';assert not checker.exists();checker.write_text(src,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,family/'review_tools/executed_repair_exact_preview_allowance_v28.py')
paths.update(x.relative_to(r).as_posix() for x in family.rglob('*') if x.is_file())
allow.write_text(json.dumps(sorted(paths),indent=2)+'\n',encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in family.rglob('*') if x.is_file()});impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
result=subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(checker)],cwd=r)
raise SystemExit(result.returncode)
