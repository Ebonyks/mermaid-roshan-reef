from pathlib import Path
import datetime,hashlib,json,re,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
staging=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930/tmp')
original=staging/'prepare_geology_imagegen_rebuild_v88.py'
v=r/'assets_src/vector/job_geology_teacher_refinement_v1_20261001'
correction=v/'OWNER_CORRECTION_V1.json'
existing=json.loads(correction.read_text(encoding='utf-8'))
assert existing['status']=='OWNER_REJECTED_GEOLOGY_VECTOR_STYLE_SOURCE_FLOORS_WITHDRAWN' and len(existing['items'])==6
original_correction_bytes=correction.read_bytes()
code=original.read_text(encoding='utf-8')
code=code.replace("def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\\n',encoding='utf-8',newline='\\n')", "def write(p,d):\n if p.name=='OWNER_CORRECTION_V1.json' and p.exists():\n  assert p.read_bytes()==original_correction_bytes\n  return\n p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\\n',encoding='utf-8',newline='\\n')")
code=code.replace('assert not correction.exists()', 'assert correction.exists()')
code=code.replace("marker='<body>'", "marker=re.search(r'<body(?:\\s[^>]*)?>',s).group(0)")
code=code.replace('executed_prepare_geology_imagegen_rebuild_v88.py','executed_prepare_geology_imagegen_rebuild_v89.py')
exec(compile(code,str(original)+':recovered_body_selector_v89','exec'))
out=r/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001'
failure=out/'preparation_attempt01_failure';failure.mkdir()
shutil.copyfile(original,failure/'executed_prepare_geology_imagegen_rebuild_v88.py')
(failure/'FAILURE.json').write_text(json.dumps(dict(status='FAIL_PRESERVED',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exception='AssertionError at HTML body selector before generation queue/rebuild impact creation; page body has attributes.',qualification='Owner correction JSON had already been written and remains byte-identical. No generation or original artwork change. Recovery locates existing body markup with attributes; no score or threshold change.'),indent=2)+'\n',encoding='utf-8')
impact=r/'design/audit_impacts/job-geology-painted-rebuild-20261001.json'
d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in failure.rglob('*') if p.is_file()});impact.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert correction.read_bytes()==original_correction_bytes
