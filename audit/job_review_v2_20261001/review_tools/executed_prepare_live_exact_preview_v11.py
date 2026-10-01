from pathlib import Path
import json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
tool=r/'audit/job_review_v2_20261001/review_tools'
allow=r/'tmp/v2_preview_allowed.json';paths=set(json.loads(allow.read_text()))
for family in ['audit/job_source_review_hall_craft_v1_20261001','assets_src/imagegen/day2_doctor_wash_pose_v1_20261001']:
 paths.update(p.relative_to(r).as_posix() for p in (r/family).rglob('*') if p.is_file() and p.suffix.lower() in {'.html','.json','.png','.py'})
paths.add('audit/job_review_v2_20261001/failed_probe_diagnostics_v1/RECEIPT.json')
assert all('..' not in p.split('/') and not any(x.startswith('.') and x not in {'.gdignore','.gitattributes'} for x in p.split('/')) for p in paths)
allow.write_text(json.dumps(sorted(paths),indent=2)+'\n',encoding='utf-8');shutil.copyfile(allow,tool/'V2_PREVIEW_ALLOWED.json')
old=r/'tmp/serve_distinct_review_v2.py';new=r/'tmp/serve_distinct_review_v3.py'
code=old.read_text();code=code.replace("ALLOW=set(json.loads((ROOT/'tmp/v2_preview_allowed.json').read_text()))", "ALLOW_PATH=ROOT/'tmp/v2_preview_allowed.json'\nALLOW=set()\nALLOW_MTIME=None\ndef refresh_allow():\n    global ALLOW,ALLOW_MTIME\n    stamp=ALLOW_PATH.stat().st_mtime_ns\n    if stamp!=ALLOW_MTIME:\n        ALLOW=set(json.loads(ALLOW_PATH.read_text()))\n        ALLOW_MTIME=stamp")
code=code.replace("raw=unquote(urlsplit(self.path).path).lstrip('/')", "refresh_allow()\n        raw=unquote(urlsplit(self.path).path).lstrip('/')")
new.write_text(code,encoding='utf-8');shutil.copyfile(new,tool/'serve_distinct_review_v3.py');shutil.copyfile(Path(__file__),tool/'executed_prepare_live_exact_preview_v11.py')
checker=tool/'check_distinct_review_resources_v6.py';code=checker.read_text();code=code.replace("'assets_src/imagegen/day2_doctor_wash_pose_v1_20261001/index.html']", "'assets_src/imagegen/day2_doctor_wash_pose_v1_20261001/index.html','audit/job_source_review_hall_craft_v1_20261001/index.html']");checker.write_text(code,encoding='utf-8')
counts=json.loads((r/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text())['counts']
p=r/'audit/job_review_v2_20261001/index.html';s=p.read_text();s=s.replace('Search1,395','Search1,427').replace('contains488 source priorities','contains512 source priorities').replace('and463 unassigned current source opinions','and455 unassigned current source opinions').replace('240 pose cells and6 pool regions','240 pose cells and38 prop regions (6 pool and32 craft cells)');p.write_text(s,encoding='utf-8')
p=r/'audit/MASTER_AUDIT_2026-08-09.md';s=p.read_text();s=s.replace('1149 source files, 240 pose cells and6 current pool prop regions (1395 addressable entries). 488 source opinions','1149 source files, 240 pose cells and38 current prop regions (6 pool and32 craft cells;1427 addressable entries). 512 source opinions').replace('463 current source reviews remain unassigned','455 current source reviews remain unassigned');p.write_text(s,encoding='utf-8')
p=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for x in tool.rglob('*') if x.is_file()]));d['validation'].append({'command':'Live exact-allowlist preview V3','result':'PENDING','evidence':'audit/job_review_v2_20261001/review_tools/serve_distinct_review_v3.py; exact allowlist refresh follows its authored file timestamp. Loopback binding, containment, no parent paths, no directory listing and exact-byte range behavior unchanged. Owned server restart and fresh browser/resource tests pending.'});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'explicit_paths':len(paths),'current_counts':counts,'server_change':'Only reload exact authored allowlist after its file changes; same loopback/containment/no-listing/range rules.'}))
