from pathlib import Path
import json, shutil, subprocess, sys

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
staging=Path(__file__).parent
tools=r/'audit/job_review_v2_20261001/review_tools'
source=tools/'build_current_job_item_register_v5.py'
new=tools/'build_current_job_item_register_v6.py'
s=source.read_text(encoding='utf-8')
old="return 'position:absolute;width:'"
assert s.count(old)==1
s=s.replace(old,"return 'position:absolute;max-width:none;max-height:none;width:'")
new.write_text(s,encoding='utf-8',newline='\n')
subprocess.run([sys.executable,'-X','utf8','-B',str(new)],cwd=r,check=True)
e=r/'audit/job_review_v2_20261001/browser_review_v5'
e.mkdir(exist_ok=True)
shutil.copyfile(staging/'craft_region_register_corrected_v13.png',e/'craft_region_second_failed_v13.png')
shutil.copyfile(staging/'region_before_v14.json',e/'REGION_BEFORE_V14.json')
shutil.copyfile(__file__,e/'executed_fix_region_image_maxwidth_v14.py')
(e/'QUALIFICATION.json').write_text(json.dumps(dict(status='REVIEW_PENDING',failure='The generic max-width:100% rule shrank the absolute full atlas to one-cell width while keeping full-atlas offsets. The first cell displayed multiple compressed props and subsequent cells were empty.',correction='New separately named V6 builder overrides max-width and max-height only on region-atlas images. Source artwork is unchanged.',source_review='Static individual source opinions remain separate; browser verification pending.'),indent=2)+'\n',encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json'
d=json.loads(impact.read_text(encoding='utf-8'))
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in e.rglob('*') if p.is_file()}|{new.relative_to(r).as_posix()})
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
licenses=r/'ASSET_LICENSES.md'
line='| audit/job_review_v2_20261001/browser_review_v5/craft_region_second_failed_v13.png | Codex browser screenshot of local authored review gallery, 2026-10-01 | Project review evidence; underlying art retains original provenance | Local localhost review | Unmodified screenshot; failed constrained full-atlas scaling preserved; no runtime art replacement. |\n'
text=licenses.read_text(encoding='utf-8')
assert line.split(' | ')[0] not in text
licenses.write_text(text+'\n'+line,encoding='utf-8',newline='\n')
allowed=r/'tmp/v2_preview_allowed.json'
d=json.loads(allowed.read_text(encoding='utf-8'))
print('allowlist_type',type(d).__name__)
if isinstance(d,list): d=sorted(set(d)|{p.relative_to(r).as_posix() for p in e.rglob('*') if p.is_file()}|{new.relative_to(r).as_posix()})
else:
 key='paths' if 'paths' in d else 'allowed_paths'
 assert key in d,list(d)
 d[key]=sorted(set(d[key])|{p.relative_to(r).as_posix() for p in e.rglob('*') if p.is_file()}|{new.relative_to(r).as_posix()})
allowed.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='CORRECTION_READY_FOR_BROWSER',builder=new.relative_to(r).as_posix())))
