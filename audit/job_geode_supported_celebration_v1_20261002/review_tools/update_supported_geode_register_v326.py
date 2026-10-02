from pathlib import Path
import datetime, hashlib, json, re, shutil, subprocess

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
family=b/'audit/job_geode_supported_celebration_v1_20261002'
live=b/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
snapshot=read(family/'SOURCE_CURRENT_BEFORE_CAPTURES.json')['source_files']
assert len(snapshot)==375 and all(sha(b/x['path'])==x['sha256'] for x in snapshot)
original=live/'ALL_ITEMS_V31.original.json'
assert not original.exists(),'Preserve version boundaries; do not rerun.'
shutil.copyfile(live/'ALL_ITEMS.json',original)
shutil.copyfile(live/'all_items.html',live/'ALL_ITEMS_V31.original.html')
shutil.copyfile(b/'audit/job_review_v2_20261001/index.html',b/'audit/job_review_v2_20261001/INDEX_BEFORE_SUPPORTED_GEODE_V326.original.html')
d=read(live/'ALL_ITEMS.json');assert len(d['items'])==1726
review=read(family/'REVIEW.json')
opinions={x['id']:x for x in review['individual_objects']}
known={x['id']:x for x in d['items']}
assert len([x for x in d['items'] if x['id'].startswith('GEO-USE-')])==4
record=family.relative_to(b).as_posix()
support=json.loads(json.dumps(known['GEO-USE-CELEBRATION']))
support.update(id='GEO-USE-SUPPORT',aliases=['GEO-USE-SUPPORT'],path='assets/opera/worlds/geology/painted_work_v1_20261001/work_slab.png',region=[68,332,889,369],source_dimensions=[1024,1024],current_binding='scripts/opera_world_backdrop_2d.gd',families=['Geologist','Painted celebration support · 330 px'],original_reports=[])
support['earlier_sha256']=support['current_checkout_sha256']=sha(b/support['path'])
support['image_path']=support['preview_path']=support['path']
support['historical_source_score']=4.6
support.pop('current_reviewed_utc',None);support.pop('current_capture_review',None)
d['items'].append(support)
for item in d['items']:
 if not item['id'].startswith('GEO-USE-'):continue
 o=opinions[item['id']]
 if item['id']!='GEO-USE-SUPPORT':
  item.setdefault('mounted_review_history',[]).append({k:item[k] for k in ['current_mounted_score','current_source_score','evaluation','refinement','current_capture_review','current_reviewed_utc','binding_sha256'] if k in item})
 item.update(current_source_score=o['artwork_score'],current_mounted_score=o['score'],priority=o['priority'],evaluation=o['evaluation'],refinement=o['refinement'],source_qualification=o['qualification'],binding_sha256=sha(b/item['current_binding']),current_capture_review=record+'/REVIEW.json',current_reviewed_utc=review['reviewed_utc'])
 item['original_reports']=list(dict.fromkeys(item['original_reports']+[record+'/index.html#'+item['id']]))
 item['latest_refinement']={'report':record+'/index.html#'+item['id'],'note':o['name']+'; material '+str(o['artwork_score'])+'/5; mounting '+str(o['score'])+'/5. '+o['evaluation']}
d['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
d['scope']='V32 known source union: 1245 unique source files, 328 pose cells, 50 runtime prop/use regions and 104 source-object regions = 1727 entries. One added painted celebration support is another presentation of an existing source. Five current Geologist uses have fresh 375-file source-bound direct review; other item opinions keep their prior dates and qualified evidence. V31 exact JSON/HTML bytes and former mounted opinions are preserved. Supported geode mounting 4.5/material 4.6; whole stage 4.1 and room/contact/coverage priorities remain. No exhaustive actual-use, whole-job, device, child or owner acceptance.'
d['counts'].update(additional_runtime_prop_regions=50,registered_items=1727,current_geode_mounted_priorities=4)
d['refresh_command']='python -B audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v32.py'
assert d['counts']['inclusive_current_source_priorities']==676 and d['counts']['unreviewed_current_source']==385
write(live/'ALL_ITEMS.json',d)
tool=live/'review_tools/refresh_current_job_review_v32.py'
src=(live/'review_tools/refresh_current_job_review_v31.py').read_text()
src=src.replace('job_geode_route_emblem_runtime_v1_20261002','job_geode_supported_celebration_v1_20261002')
src=src.replace('Dated Doctor capture remains explicitly historical','All eight dated Doctor/Nursery capture cases remain explicitly historical')
tool.write_text(src,encoding='utf-8',newline='\n')
html=(live/'all_items.html').read_text()
html=html.replace('refresh_current_job_review_v31.py','refresh_current_job_review_v32.py')
html=html.replace('Current illustrated review and geode route evidence','Current illustrated review and supported geode evidence')
html=html.replace('Opinions dated ${d.created_utc}; source boundary checked','Register updated ${d.created_utc}; individual opinion dates retained in records; source boundary checked')
(live/'all_items.html').write_text(html,encoding='utf-8',newline='\n')
for p in [family/'index.html',family/'REVIEW.json']:
 s=p.read_text()
 # Readable spacing in newly drafted prose; do not modify hashes, paths or numeric JSON.
 pairs={'unsupported4.2':'unsupported 4.2','remains4.1':'remains 4.1','inclusive≤4.5':'inclusive ≤4.5','inclusive4.5':'inclusive 4.5','Inclusive4.5':'Inclusive 4.5','room4.5':'room 4.5','scene4.5':'scene 4.5','actual1280':'actual 1280','frame125':'frame 125','suite2':'suite 2','on375':'on 375','PreviousL':'Previous L','All58':'All 58','all316':'all 316','on27':'on 27','and10':'and 10','same220':'same 220','the1280':'the 1280','y490':'y 490','existing1024':'existing 1024','nominal4':'nominal 4','recorded8':'recorded 8','scored3.2':'scored 3.2','least2048':'least 2048','references1672':'references 1672','/110 opinions':' / 110 opinions','No5/5':'No 5/5','no5/5':'no 5/5','Both cream':'Both cream'}
 for a,z in pairs.items():s=s.replace(a,z)
 p.write_text(s,encoding='utf-8',newline='\n')
attr=b/'.gitattributes';s=attr.read_text();s+='\naudit/job_artwork_refinement_live/ALL_ITEMS_V31.original.* -text\naudit/job_review_v2_20261001/INDEX_BEFORE_SUPPORTED_GEODE_V326.original.html -text\n';attr.write_text(s,encoding='utf-8',newline='\n')
ledger=b/'design/05_DOC_LEDGER.md';s=ledger.read_text()
s=s.replace('`SUPPORTING_CURRENT`: reversible four-use actual route review','`SUPPORTING_HISTORICAL`: reversible four-use actual route review')
lines=s.splitlines()
for i,l in enumerate(lines):
 if l.startswith('| `audit/job_artwork_refinement_live/all_items.html`'):
  lines[i]='| `audit/job_artwork_refinement_live/all_items.html` | 🟣 | `CANDIDATE`; V32 searchable known union: 1727 entries / 1245 unique sources / 328 pose cells / 50 runtime prop-use regions / 104 source-object regions. Five Geologist uses have fresh direct review on 375 unchanged capture sources; geode and support mounted 4.5, whole stage 4.1. Four inclusive mounted priorities are additional to the unchanged 676 source priorities / 385 unassigned source reviews. Other opinions retain their earlier dates. Exact V31 bytes and former mounted opinions are preserved; refresh V32 withholds changed source/binding/context claims. No exhaustive actual-use, full-action, device/child/owner or all-job acceptance. |'
s='\n'.join(lines)+'\n'
s+='\n| `audit/job_artwork_refinement_live/ALL_ITEMS_V31.original.json` | ⚪ | `HISTORICAL_SUPPORTING`; exact prior V31 source register, including the former unsupported geode mounted 4.2 opinion. |\n| `audit/job_review_v2_20261001/INDEX_BEFORE_SUPPORTED_GEODE_V326.original.html` | ⚪ | `HISTORICAL_SUPPORTING`; exact prior landing at the support-review transition. Its earlier source/status labels do not establish current evidence. |\n'
ledger.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-supported-celebration-20261002.json';imp=read(ip)
paths=[live/'ALL_ITEMS.json',original,live/'ALL_ITEMS_V31.original.html',live/'all_items.html',tool,b/'audit/job_review_v2_20261001/INDEX_BEFORE_SUPPORTED_GEODE_V326.original.html']
imp['files']=sorted(set(imp['files'])|{p.relative_to(b).as_posix() for p in paths}|{p.relative_to(b).as_posix() for p in family.rglob('*') if p.is_file()})
write(ip,imp)
allowed=b/'tmp/v2_preview_allowed.json';a=read(allowed)
if isinstance(a,list):a=sorted(set(a)|set(imp['files']))
else:
 key='paths' if 'paths' in a else 'files';a[key]=sorted(set(a[key])|set(imp['files']))
write(allowed,a)
assert all(sha(b/x['path'])==x['sha256'] for x in snapshot)
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(tool)],cwd=b,check=True)
print('V32 supported-use register: 1727 entries; 5 current mounted uses; 375 capture sources unchanged.')
