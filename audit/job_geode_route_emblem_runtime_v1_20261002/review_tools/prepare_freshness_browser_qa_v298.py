from pathlib import Path
import copy,json,shutil,subprocess,sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
live=b/'audit/job_artwork_refinement_live';family=b/'audit/job_geode_route_emblem_runtime_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
html=live/'all_items.html';s=html.read_text(encoding='utf-8')
s=s.replace("if(!c||!c.source_match)","if(!c||c.path!==q.path||c.registered_sha256!==q.current_checkout_sha256||!c.source_match)")
s=s.replace("q.current_byte_status==='CHANGED_BYTES_REVIEW_REQUIRED'","['CHANGED_BYTES_REVIEW_REQUIRED','CHANGED_SINCE_REGISTER_REFRESH_REVIEW_REQUIRED'].includes(q.current_byte_status)")
s=s.replace('return d;}).then(d=>{registry=d;', 'd.last_boundary_refresh=stamp.checked_utc;return d;}).then(d=>{registry=d;')
s=s.replace('Updated ${d.created_utc}.','Opinions dated ${d.created_utc}; source boundary checked ${d.last_boundary_refresh}.')
html.write_text(s,encoding='utf-8',newline='\n')
subprocess.run([sys.executable,'-X','utf8','-B',str(live/'review_tools/refresh_current_job_review_v31.py')],cwd=b,check=True)
fixture=b/'tmp/job_register_freshness_negative_v31';fixture.mkdir(exist_ok=False)
registry=read(live/'ALL_ITEMS.json');stamp=read(live/'CURRENT_BOUNDARY_REFRESH.json')
negative=copy.deepcopy(stamp)
negative['geode_capture_boundary_match']=False
negative['status']='QA_ONLY_INJECTED_NEGATIVE_DATA_NOT_A_SOURCE_CAPTURE'
for item in negative['items']:
 if item['id']=='GEO-USE-LIBRARY-50PX':item['source_match']=False
 if item['id']=='GEO-USE-CELEBRATION-220PX':item['binding_match']=False
actual_ids=[x['id'] for x in registry['items'] if x['id'].startswith('GEO-USE-')]
assert len(actual_ids)==4
# Names are obtained from the actual register, never assumed.
library=next(x for x in actual_ids if 'LIBRARY' in x)
celebration=next(x for x in actual_ids if 'CELEBRATION' in x)
for item in negative['items']:
 if item['id']==library:item['source_match']=False
 if item['id']==celebration:item['binding_match']=False
write(fixture/'ALL_ITEMS.json',registry);write(fixture/'CURRENT_BOUNDARY_REFRESH.json',negative)
(fixture/'index.html').write_text(s.replace('<h1>Known job artwork: individual review register</h1>','<h1>QA-only injected stale-source negative control</h1>'),encoding='utf-8',newline='\n')
write(family/'FRESHNESS_BROWSER_CONTROL_PLAN_V298.json',dict(status='PREPARED_NOT_YET_BROWSER_VERIFIED',negative_source_item=library,negative_binding_item=celebration,negative_geode_context_boundary=False,qualification='Ignored isolated fixture injects stale comparison data only. It does not alter runtime sources, canonical register opinions or canonical hash results. All four mounted claims should be withheld; the Library source score should also be withheld. Verify canonical four/priority-three rows separately.'))
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip)
d['files']=sorted(set(d['files'])|{(family/'review_tools'/Path(__file__).name).relative_to(b).as_posix(),(family/'FRESHNESS_BROWSER_CONTROL_PLAN_V298.json').relative_to(b).as_posix()});write(ip,d)
allow=b/'tmp/v2_preview_allowed.json';paths=set(read(allow))
paths.update({p.relative_to(b).as_posix() for p in fixture.iterdir()})
paths.update({(live/'CURRENT_BOUNDARY_REFRESH.json').relative_to(b).as_posix(),(live/'review_tools/refresh_current_job_review_v31.py').relative_to(b).as_posix()})
write(allow,sorted(paths))
print(json.dumps(dict(status='CANONICAL_AND_ISOLATED_NEGATIVE_READY',geode_ids=actual_ids,fixture=fixture.relative_to(b).as_posix())))
