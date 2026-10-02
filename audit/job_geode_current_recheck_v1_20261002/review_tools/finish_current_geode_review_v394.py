from pathlib import Path
import concurrent.futures,datetime,hashlib,json,re,shutil,urllib.request
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_current_recheck_v1_20261002';live=b/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
for name in ['repair_current_geode_review_v392.py','finish_current_geode_review_v394.py']:
 shutil.copyfile(Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')/name,f/'review_tools'/name)
r=read(f/'DIRECT_REVIEW.json')
for x in r['individual_objects']:
 if x['id']=='GEO-PAN-ACTION':x['evaluation']='Selected panning canvases show a painted dish and contained grains/minerals. Remote hands and the generic displayed rock/return relationship remain weak at3.8. The complete timed panning sequence was not captured in this fresh recheck; its separate dated motion studies remain failed and preserved.'
 if x['id']=='GEO-CAVITIES':x['refinement']='Retain this provisionally reviewed cavity painting; owner acceptance remains separate.'
write(f/'DIRECT_REVIEW.json',r)
reg=read(live/'ALL_ITEMS.json')
for x in reg['items']:
 if x['id'] in ['GEO-PAN-ACTION','GEO-FOSSIL-CLEARING']:
  x['current_complete_action_score']=None;x['current_selected_action_relationship_score']=x['current_mounted_score']
 if x['id']=='GEO-PAN-ACTION':
  item=next(q for q in r['individual_objects'] if q['id']==x['id']);x['evaluation']=item['evaluation'];x['latest_refinement']['note']=item['evaluation']
write(live/'ALL_ITEMS.json',reg)
p=f/'index.html';s=p.read_text();s=s.replace('The painted dish rocks and grains give way to contained cyan specimens. Remote hands and the generic rocking/return keep the complete action weak.',next(x['evaluation'] for x in r['individual_objects'] if x['id']=='GEO-PAN-ACTION'));s=s.replace('Retain the accepted cavity painting.','Retain this provisionally reviewed cavity painting; owner acceptance remains separate.')
pieces=re.split('(<[^>]+>)',s)
for i in range(0,len(pieces),2):pieces[i]=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ',pieces[i])
p.write_text(''.join(pieces),encoding='utf-8',newline='\n')
proof=[]
for name in ['BROWSER_LIBRARY_GEODE_V393.png','BROWSER_NATIVE_GEODE_V393.png','BROWSER_GEODE_REPORT_V393.png']:
 src=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')/name;dst=f/name;shutil.copyfile(src,dst);proof.append(dict(path=dst.relative_to(b).as_posix(),sha256=sha(dst.read_bytes())))
members={x['path']:x['sha256'] for x in r['views']+r['frames']+r['boards']}
def check(pair):
 path,digest=pair;raw=urllib.request.urlopen('http://127.0.0.1:8880/'+path,timeout=30).read();assert sha(raw)==digest,path;return dict(path=path,sha256=digest,http='GET',literal_match=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:checks=list(pool.map(check,sorted(members.items())))
write(f/'BROWSER_QA_V394.json',dict(status='PASS_REVIEW_UI_ONLY',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),screenshots=proof,http_image_checks=checks,counts=dict(articles=27,registry=1778,source_priorities=690,geologist_priorities=23,nursery_priorities=10,source_unassigned=385,default_filter_items=723,unchanged_native_and_board_images=len(checks)),qualification='Browser observed27 articles/current boundaries, native image link opens1280x720 original; library search shows current contact2.7 separately from rejected/unbound sources4.3/4.5. Exact413 current native/QA image HTTP bytes checked. Screenshots precede minor text spacing/selected-panning qualification repair. Browser deliverable-tab marking rejected before action; explicit authorization pending, no mark/approval recorded. Report saved regardless; no runtime/device/child/owner acceptance.'))
write(f/'BROWSER_TAB_PERSISTENCE_BLOCK_V393.json',dict(status='BLOCKED_AWAITING_EXPLICIT_REVIEW_TAB_PERSISTENCE_APPROVAL',action='Keep fresh Geologist preview tab open as review draft using markDeliverable',approval_review_reason='Treated tab mark as consequential handoff/status change without explicit authorization while owner acceptance pending.',performed=False,creative_owner_acceptance=None,unaffected='Saved illustrated report, source-bound direct visual review and read-only browser checks continue.'))
ip=b/'design/audit_impacts/job-geode-current-recheck-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});d['validation'].append(dict(command='Current report/library browser and exact413 local image-link verification',result='PASS',evidence=f.relative_to(b).as_posix()+'/BROWSER_QA_V394.json'));write(ip,d)
allow=b/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|set(d['files'])))
print('CURRENT_GEODE_REPORT_BROWSER_QA|27 opinions|413 exact HTTP images|1778 entries|23 Geologist priorities|no owner/tab approval')
