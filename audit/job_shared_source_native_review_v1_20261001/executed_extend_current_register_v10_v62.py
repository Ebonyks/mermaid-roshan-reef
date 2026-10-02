from pathlib import Path
import hashlib, json, re, shutil, subprocess, sys
from PIL import Image

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
reviewdir=r/'audit/job_shared_source_native_review_v1_20261001'
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
review=json.loads((reviewdir/'REVIEW.json').read_text(encoding='utf-8'))
cellsdir=reviewdir/'cells';assert not cellsdir.exists();cellsdir.mkdir()
lic=r/'ASSET_LICENSES.md';s=lic.read_text(encoding='utf-8')
for x in review['cells']+review['pool_regions']:
    rect=x['region'];image=Image.open(r/x['path']);crop=image.crop((rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3]))
    path=cellsdir/(x['id']+'.png');crop.save(path)
    x['preview_path']=path.relative_to(r).as_posix();x['preview_sha256']=hashlib.sha256(path.read_bytes()).hexdigest();x['preview_operation']='Exact native atlas region extraction for inspection; no paint, alpha mask, scaling or source repair.'
    assert x['preview_path'] not in s
    s+='\n| '+x['preview_path']+' | '+x['path']+' native region'+str(rect)+' | Project diagnostic crop; original provenance retained | Exact source-region extraction, original unchanged | Individual still review preview only; source4.6, no mounted/action/owner acceptance. |\n'
lic.write_text(s,encoding='utf-8',newline='\n');write(reviewdir/'REVIEW.json',review)
page=(reviewdir/'index.html').read_text(encoding='utf-8')
for x in review['cells']+review['pool_regions']:
    pattern=r'<div class="cell" role="img" aria-label="'+re.escape(x['id'])+r'"[^>]*></div>'
    page,count=re.subn(pattern,'<img class="cell-preview" loading="lazy" src="cells/'+x['id']+'.png" alt="'+x['id']+' exact native region">',page)
    assert count==1,x['id']
page=page.replace('minmax(350px,1fr)','minmax(min(100%,350px),1fr)').replace('.sheet{','.cell-preview{display:block;width:100%;max-width:341px;height:auto}.sheet{')
(reviewdir/'index.html').write_text(page,encoding='utf-8',newline='\n')
v9=r/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v9.py'
code=v9.read_text(encoding='utf-8').replace('build_current_job_item_register_v9.py','build_current_job_item_register_v10.py')
marker="for q in items.values():\n p=q['path']\n if p not in hashes:"
assert code.count(marker)==1
extra='''# Direct native shared source/region review; preserve earlier unknown opinions.
shared=read('audit/job_shared_source_native_review_v1_20261001/REVIEW.json')
for x in shared['sources']:
 matches=[q for q in items.values() if q['path']==x['path'] and q['kind']=='source']
 assert len(matches)==1,x['path']
 q=matches[0];q['earlier_written_evaluation']=q['evaluation'];q['latest_source_score']=x['source_score'];q['latest_source_sha256']=x['sha256'];q['evaluation']=x['evaluation'];q['source_qualification']=x['qualification'];q['latest_refinement']=dict(report='audit/job_shared_source_native_review_v1_20261001/index.html',note='Every native region directly inspected; source-only4.6. Literal-reference evidence is separate from current mounted/complete-action acceptance.');q['literal_reference_evidence']=x['literal_reference_evidence']
for x in shared['cells']:
 assert x['id'] not in items
 items[x['id']]=dict(id=x['id'],aliases=[],kind='pose cell',path=x['path'],region=x['region'],earlier_sha256=x['sha256'],historical_source_score=x['source_score'],evaluation=x['evaluation'],refinement='Reuse this exact source region when its meaning matches; review actual phone-size visibility, contact, row ordering and loop/return before runtime acceptance.',families=['Shared Roshan native sheet','Individual still source review'],original_reports=['audit/job_shared_source_native_review_v1_20261001/index.html'],source_qualification=x['qualification'],preview_path=x['preview_path'],native_reference_observations=[],literal_reference_evidence=x['literal_reference_evidence'])
reach=read('assets_src/imagegen/day2_doctor_wash_reach_v1_20261001/ATTEMPT01_REVIEW.json');p=reach['path']
items[p]=dict(id=reach['id'],aliases=[],kind='source',path=p,earlier_sha256=reach['sha256'],historical_source_score=reach['source_score'],evaluation=reach['evaluation'],refinement='All18 reaching native placements are below4.5; best contact/composition4.4. Align the actual faucet/contact, add literal rinsing and a matching clean-reaching ending; then audit full wet/rub/rinse/clean/quiet-return sequence.',families=['Day Two washing','Unbound outward-reaching doctor source'],original_reports=['assets_src/imagegen/day2_doctor_wash_reach_v1_20261001/index.html'],source_qualification=reach['qualification'],preview_path=p,native_reference_observations=[],runtime_binding_state=reach['status'],latest_refinement=dict(report='audit/day_two_wash_contact_study_v1_20261001/attempt_04/index.html',note='Every18 native reach view directly reviewed, best static contact4.4. All76 contact views remain; source4.5 is not action acceptance.'))
'''
code=code.replace(marker,extra+marker)
v10=v9.with_name('build_current_job_item_register_v10.py');assert not v10.exists();v10.write_text(code,encoding='utf-8',newline='\n')
run=subprocess.run([sys.executable,'-X','utf8','-B',str(v10)],cwd=r,capture_output=True,text=True)
(r/'tmp/register_v10.stdout.log').write_text(run.stdout,encoding='utf-8');(r/'tmp/register_v10.stderr.log').write_text(run.stderr,encoding='utf-8');print(run.stdout);print(run.stderr);assert run.returncode==0
data=json.loads((r/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text(encoding='utf-8'));print(json.dumps(data['counts']))
# Actual counts drive the current human entry. Historical evidence stays unchanged.
assert len(data['items'])==1518
assert sum(x['current_source_score'] is None for x in data['items'])==395
assert sum(x['priority'] for x in data['items'])==557
entry=r/'audit/job_review_v2_20261001/index.html';t=entry.read_text(encoding='utf-8');t=t.replace('Search1,429','Search1,518').replace('contains556 source priorities','contains557 source priorities').replace('and403 unassigned','and395 unassigned').replace('catalogues1151 source files,240 pose cells','catalogues1152 source files,328 pose cells');t=t.replace('</nav>','<a href="../job_shared_source_native_review_v1_20261001/index.html">8 shared source sheets and94 individual regions</a></nav>',1);entry.write_text(t,encoding='utf-8',newline='\n')
master=r/'audit/MASTER_AUDIT_2026-08-09.md';t=master.read_text(encoding='utf-8');a=t.index('Washing iteration and local motion (2026-10-01):');b=t.index('\n\n',a);replacement='Washing and shared-source review (2026-10-01): [all18 outward-reaching native placements](day_two_wash_contact_study_v1_20261001/attempt_04/index.html) bring the direct static contact record to76 views; best contact/composition4.4 remains below floor. The new outward-reaching source is unbound4.5. [Eight shared native sheets and94 regions](job_shared_source_native_review_v1_20261001/index.html) add8 source opinions and88 individual Roshan cell opinions, source-only4.6. The searchable register now contains1518 entries,1152 source files,328 pose cells and38 prop regions, with557 inclusive source priorities and395 unassigned source opinions. These counts include unbound/rejected/reference/shared sources and do not claim exhaustive live weak objects. [Every41 earlier doctor rubbing reference frames](../assets_src/local_motion/day2_doctor_wash_rub_study_v1_20261001/index.html) remain individually scored; motion4.0/return3.5 is below floor. [Shared-source impact](../design/audit_impacts/job-shared-native-source-review-20261001.json). No finding closure, runtime action or owner acceptance.';t=t[:a]+replacement+t[b:];master.write_text(t,encoding='utf-8',newline='\n')
ledger=r/'design/05_DOC_LEDGER.md';t=ledger.read_text(encoding='utf-8');note='Current job artwork review supplement (2026-10-01): [eight shared source sheets and94 individual native regions](../audit/job_shared_source_native_review_v1_20261001/index.html) and [76 doctor static contact views](../audit/day_two_wash_contact_study_v1_20261001/attempt_04/index.html) extend the existing structured review library. The current register has1518 entries,557 inclusive source priorities and395 unassigned source opinions. Native still/source, exact published bytes, hosted checks and complete-action/device/child/owner acceptance remain separate; no authority or finding lifecycle changes.\n\n';pos=t.index('\n\n')+2;t=t[:pos]+note+t[pos:];ledger.write_text(t,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,reviewdir/'executed_extend_current_register_v10_v62.py')
ip=r/'design/audit_impacts/job-shared-native-source-review-20261001.json';impact=json.loads(ip.read_text(encoding='utf-8'));paths={p.relative_to(r).as_posix() for p in reviewdir.rglob('*') if p.is_file()};paths.update(['audit/job_review_v2_20261001/index.html','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/STATUS.json','audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/all_items.html','audit/job_artwork_refinement_live/review_tools/build_current_job_item_register_v10.py',v10.relative_to(r).as_posix(),'design/audit_impacts/job-review-separate-v2-20261001.json']);impact['files']=sorted(set(impact['files'])|paths);impact['validation'].append({'command':'Exact88 pose-cell and6 prop-region diagnostic extraction plus current register refresh','result':'PASS','evidence':'audit/job_artwork_refinement_live/ALL_ITEMS.json;1518 entries,395 unassigned source opinions and557 inclusive priorities. All8 reviewed original source hashes unchanged.'});write(ip,impact)
allow=r/'tmp/v2_preview_allowed.json';allowed=set(json.loads(allow.read_text(encoding='utf-8')));allowed.update(impact['files']);write(allow,sorted(allowed))
print(json.dumps({'status':'CURRENT_REGISTER_V10_EXTENDED','entries':1518,'source_priorities':557,'unassigned_source_opinions':395,'new_cell_previews':88,'existing_prop_previews':6}))
