from pathlib import Path
import hashlib,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=b/'audit/job_geode_runtime_v1_20261001'
p=out/'ARTWORK_ITEMS.json';d=json.loads(p.read_text())
for q in d['items'][4:]:
 q['sha256']=hashlib.sha256((b/q['path']).read_bytes()).hexdigest();q['source_parent_id']='GEO-RUNTIME-OPEN_EMBEDDED';q['source_dimensions']=[1024,683]
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
src=(b/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v19.py').read_text(encoding='utf-8')
inject='''# Six source-preserving embedded geode components, each individually inspected.
geode_parts=json.loads((r/'audit/job_geode_runtime_v1_20261001/ARTWORK_ITEMS.json').read_text())
for x in geode_parts['items'][4:]:
 items[x['id']]=dict(id=x['id'],aliases=[],kind='source object region',path=x['path'],region=x['review_annotation_source_rect'],source_dimensions=x['source_dimensions'],earlier_sha256=x['sha256'],historical_source_score=x['source_finish'],evaluation=x['evaluation'],refinement='Preserve this embedded cavity component and review all authored opening states, phone-size visibility and full timed action; do not turn it into a detached pickup.',families=['Geologist','Embedded geode component'],original_reports=['audit/job_geode_runtime_v1_20261001/index.html#embedded-components'],source_qualification=x['qualification'],preview_path=x['path'],native_reference_observations=[],independent_runtime_object=False,source_parent_id=x['source_parent_id'])
'''
assert 'for q in items.values():' in src
src=src.replace('for q in items.values():',inject+'\nfor q in items.values():',1)
src=src.replace('38 runtime prop regions and 5 source-object regions','38 runtime prop regions and 11 source-object regions')
src=src.replace('build_current_job_item_register_v18.py','build_current_job_item_register_v20.py')
# Existing region display is now shared by the explicit embedded source regions.
src=src.replace("q.kind===\\'runtime prop region\\'&&q.image_path===q.path", "[\\'runtime prop region\\',\\'source object region\\'].includes(q.kind)&&q.image_path===q.path")
src=src.replace('32 individually inspected craft prop regions, including the complete shared-source native review.', '32 individually inspected craft prop regions, plus11 source-object regions including six embedded geode details. Includes the complete shared-source native review.')
target=b/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v20.py';target.write_text(src,encoding='utf-8',newline='\n');compile(src,str(target),'exec')
dest=out/'review_tools/register_geode_components_v169.py';shutil.copyfile(__file__,dest)
ip=b/'design/audit_impacts/job-geode-painted-runtime-20261001.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{target.relative_to(b).as_posix(),dest.relative_to(b).as_posix(),'audit/job_artwork_refinement_live/review_tools/build_current_job_item_register_v20.py','audit/job_artwork_refinement_live/all_items.html'});ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('Prepared currentV20 source-hash/register coverage for all six embedded geode details.')
