from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
staging=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930/tmp')
original=staging/'prepare_geology_imagegen_rebuild_v88.py'
v=r/'assets_src/vector/job_geology_teacher_refinement_v1_20261001'
correction=v/'OWNER_CORRECTION_V1.json'
original_correction_bytes=correction.read_bytes()
assert json.loads(original_correction_bytes)['status']=='OWNER_REJECTED_GEOLOGY_VECTOR_STYLE_SOURCE_FLOORS_WITHDRAWN'
assert (v/'index.html').read_text(encoding='utf-8').count('<main>')==1
code=original.read_text(encoding='utf-8')
code=code.replace("def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\\n',encoding='utf-8',newline='\\n')", "def write(p,d):\n if p.name=='OWNER_CORRECTION_V1.json' and p.exists():\n  assert p.read_bytes()==original_correction_bytes\n  return\n p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\\n',encoding='utf-8',newline='\\n')")
code=code.replace('assert not correction.exists()','assert correction.exists()').replace("marker='<body>'","marker='<main>'")
code=code.replace('executed_prepare_geology_imagegen_rebuild_v88.py','executed_prepare_geology_imagegen_rebuild_v90.py')
exec(compile(code,str(original)+':verified_main_selector_v90','exec'))
out=r/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001'
for number,name,reason in [(1,'prepare_geology_imagegen_rebuild_v88.py','Exact body opening absent in valid implicit-body gallery HTML.'),(2,'prepare_geology_imagegen_rebuild_v89.py','Regular-expression body opening absent; no attributed body exists. Direct markup inspection then identified the exact single main opening.')]:
 failure=out/('preparation_attempt%02d_failure'%number);failure.mkdir()
 shutil.copyfile(staging/name,failure/('executed_'+name))
 (failure/'FAILURE.json').write_text(json.dumps(dict(status='FAIL_PRESERVED',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exception='AssertionError' if number==1 else 'AttributeError: NoneType.group',reason=reason,qualification='Failed before generation directory/queue/impact creation; already written owner correction stays byte-identical. No generation, runtime or source-art mutation.'),indent=2)+'\n',encoding='utf-8')
s=(v/'index.html').read_text(encoding='utf-8')
s=s.replace('Five selected replacement sources meet the 4.5/5 drafting floor.','Earlier isolated review marked five selected sources at4.5. The owner has since rejected the four selected geology sources for their flat vector style; those geology floors are withdrawn. Only the teacher source retains its provisional mark.')
(v/'index.html').write_text(s,encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-geology-painted-rebuild-20261001.json'
d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in out.rglob('*') if p.is_file()});impact.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert correction.read_bytes()==original_correction_bytes
