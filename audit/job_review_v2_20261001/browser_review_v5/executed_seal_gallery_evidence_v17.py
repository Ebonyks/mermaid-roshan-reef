from pathlib import Path
from PIL import Image
import datetime,hashlib,json,re,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
t=Path(__file__).parent;e=r/'audit/job_review_v2_20261001/browser_review_v5'
names=['craft_region_register_corrected_v14.png','craft_region_register_row2_v14.png','craft_region_register_row3_v14.png','craft_paint_register_corrected_v14.png','palette_register_v14.png','idea_register_v14.png','hall_craft_report_browser_v14.png','region_after_v14.json','paint_region_geometry_v14.json','palette_region_geometry_v14.json','idea_region_geometry_v14.json','standalone_craft_geometry_v14.json']
for name in names:shutil.copyfile(t/name,e/name)
shutil.copyfile(__file__,e/'executed_seal_gallery_evidence_v17.py')
ribbon=json.loads((e/'region_after_v14.json').read_text(encoding='utf-8'))
assert len(ribbon['cells'])==8 and all(x['loaded'] and x['maxWidth']=='none' for x in ribbon['cells'])
report=json.loads((e/'standalone_craft_geometry_v14.json').read_text(encoding='utf-8'))
assert len(report['cells'])==32 and all(x['loaded'] and x['maxWidth']=='none' and x['overflow']=='hidden' for x in report['cells'])
source=json.loads((r/'audit/job_source_review_hall_craft_v1_20261001/REVIEW.json').read_text(encoding='utf-8'))
for row in source['source_items']:assert hashlib.sha256((r/row['path']).read_bytes()).hexdigest()==row['sha256']
proof=[dict(path=p.relative_to(r).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),dimensions=list(Image.open(p).size)) for p in e.glob('*v14.png')]
receipt=dict(status='SCOPED_PASS_REVIEW_ATLAS_PREVIEW_GEOMETRY',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ribbon_images_loaded=8,standalone_craft_images_loaded=32,source_files_unchanged=8,ribbon_direct_browser_views=['craft_region_register_corrected_v14.png','craft_region_register_row2_v14.png','craft_region_register_row3_v14.png'],paint_direct_browser_view='craft_paint_register_corrected_v14.png',remaining_screenshot_qualification='Palette/idea/header screenshots show partial cards. All32 standalone cell elements have correct measured unconstrained atlas geometry and load; this is gallery verification, not32 fully displayed individual browser screenshot reviews.',screenshots=proof,qualification='Earlier two failed preview observations are preserved. The UTF-8 subprocess invocation first failed while reading the document ledger; the corrected explicit UTF-8 rerun completed. No game/protected original/art source changed. No mounted/action/device/child/owner acceptance follows from review-gallery measurements.')
(e/'QUALIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
license=r/'ASSET_LICENSES.md';s=license.read_text(encoding='utf-8')
for p in e.glob('*v14.png'):
 rel=p.relative_to(r).as_posix()
 if '| '+rel+' |' not in s:s+='\n| '+rel+' | Codex browser screenshot of local authored review gallery, 2026-10-01 | Project review evidence; underlying artwork retains original provenance | Local localhost review | Unmodified screenshot; review-only cell geometry or report view, no runtime artwork replacement. |\n'
license.write_text(s,encoding='utf-8',newline='\n')
for path in ['audit/MASTER_AUDIT_2026-08-09.md','audit/job_review_v2_20261001/index.html']:
 p=r/path;s=p.read_text(encoding='utf-8')
 s=s.replace('512 source opinions','554 source opinions').replace('455 current source reviews','403 current source reviews').replace('512 inclusive source priorities','554 inclusive source priorities').replace('455 current opinions unassigned','403 current opinions unassigned')
 if path.endswith('.md'):
  note=' Source-only attribution correction:52 existing Day One evaluations are restored by exact recorded/current hashes; this adds42 inclusive priorities and does not represent new visual review.'
  line=next(line for line in s.splitlines() if line.startswith('Known individual job-art register'))
  if note not in line:s=s.replace(line,line+note)
 else:
  note='<p>Register attribution correction:52 already documented unchanged source opinions are restored, including42 inclusive priorities. <a href="SOURCE_OPINION_RECONCILIATION_V1.json">Exact-hash reconciliation</a> preserves their earlier scope. <a href="browser_review_v5/QUALIFICATION.json">Atlas gallery correction and retained failures</a> records the scoped desktop preview verification; no current in-game acceptance follows.</p>'
  if 'SOURCE_OPINION_RECONCILIATION_V1.json' not in s:s=s.replace('</main>',note+'</main>')
 p.write_text(s,encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'))
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in e.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md','audit/job_review_v2_20261001/index.html','audit/MASTER_AUDIT_2026-08-09.md'})
d['validation']=[v for v in d['validation'] if v.get('command')!='Scoped distinctV2 atlas-gallery correction']+[dict(command='Scoped distinctV2 atlas-gallery correction',result='PASS',evidence='audit/job_review_v2_20261001/browser_review_v5/QUALIFICATION.json; two earlier crop failures preserved;8 ribbon screenshots,32 loaded standalone geometry elements; source images unchanged.')]
impact.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
allowed=r/'tmp/v2_preview_allowed.json';v=json.loads(allowed.read_text(encoding='utf-8'));assert isinstance(v,list)
v=sorted(set(v)|{p.relative_to(r).as_posix() for p in e.rglob('*') if p.is_file()}|{'audit/job_review_v2_20261001/SOURCE_OPINION_RECONCILIATION_V1.json','audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v7.py','audit/job_review_v2_20261001/review_tools/executed_reconcile_recorded_source_opinions_v16.py'})
allowed.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status=receipt['status'],source_unchanged=8,screenshots=len(proof),allowlist_paths=len(v))))
