from pathlib import Path
import collections,datetime,hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geode_route_emblem_runtime_v1_20261002';live=r/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
shots=[]
for name in ['geode_route_report_header_v289.png','geode_route_report_celebration_v289.png','geode_current_use_register_v289.png']:
 p=f/name;shutil.copyfile(Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')/name,p);shots.append(dict(path=p.relative_to(r).as_posix(),sha256=sha(p)))
write(f/'BROWSER_QA.json',dict(status='PASS_CURRENT_REPORT_AND_FOUR_USE_REGISTER',checked_utc=now,url='http://127.0.0.1:8880/'+f.relative_to(r).as_posix()+'/index.html',viewport=[1280,720],document_width=1265,caption_text_color='rgb(37, 52, 73)',caption_background='rgb(246, 249, 255)',priority_control=dict(checked=True,visible_context_opinions=16,hidden_above_threshold=3),celebration_images=dict(loaded=True,native_sizes=[[1280,720],[1600,720]]),register=dict(query='GEO-USE-',lane='All known items',matching_items=4,registered_items=1726,source_priorities=676,unassigned_sources=385),screenshots=shots,qualification='Actual browser rendering and controls checked after intrinsic image extents were added. Initial actions navigated to a menu image; adding reserved extents resolved the observed behavior on retest. This supports the layout explanation but does not independently prove a browser internals root cause. No artwork/source changes or creative/device acceptance.'))
p=f/'LAYOUT_STABILITY_V289.json';d=read(p);d['status']='INTRINSIC_CANVAS_EXTENTS_BROWSER_CONTROL_RECHECK_PASS';d['recheck']='BROWSER_QA.json';write(p,d)
# Two old technical labels each named two distinct source attempts. Preserve their
# prior labels as aliases and make the current four entries individually addressable.
p=live/'ALL_ITEMS.json';d=read(p);counts=collections.Counter(x['id'] for x in d['items']);changes=[]
assert {k:v for k,v in counts.items() if v>1}=={'GEO-PAINT-TECH-OPEN_GEODE':2,'GEO-PAINT-TECH-WASHING_PAN':2}
for x in d['items']:
 if counts[x['id']]<=1:continue
 prior=x['id'];attempt='01' if '/attempt_01/' in x['path'] else '02' if '/attempt_02/' in x['path'] else None;assert attempt
 x['id']=prior+'-ATTEMPT-'+attempt;x['aliases']=sorted(set(x.get('aliases',[]))|{prior})
 changes.append(dict(path=x['path'],previous_label=prior,current_id=x['id'],score_changed=False))
assert len({x['id'] for x in d['items']})==1726
d['scope']+=' Four pre-existing ambiguous technical labels now include their attempt number; old labels remain aliases, all source opinions/hashes unchanged.'
write(p,d);write(live/'REGISTER_ID_CORRECTION_V31.json',dict(status='CURRENT_IDS_DISTINCT_HISTORICAL_LABELS_PRESERVED',checked_utc=now,items=changes,qualification='Identity/navigation bookkeeping only; no new visual review or changed art/score. V30 exact bytes remain preserved.'))
p=live/'all_items.html';s=p.read_text(encoding='utf-8');assert s.count('Current source priorities ≤4.5')==1;s=s.replace('Current source priorities ≤4.5','Current source or mounted priorities ≤4.5');p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
ip=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip)
d['scope']+=' Browser priority control now stable with reserved native image extents; current four ambiguous source-attempt IDs distinguished while preserving old labels as aliases and scores. Priority filter label includes mounted opinions.'
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()}|{'audit/job_artwork_refinement_live/REGISTER_ID_CORRECTION_V31.json'})
d['validation'].append(dict(command='Actual localhost report browser rendering, priority control and four current register entries',result='PASS',evidence=f.relative_to(r).as_posix()+'/BROWSER_QA.json; no creative/device acceptance.'))
write(ip,d)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|set(d['files'])))
print('Browser evidence saved;1726 distinct current IDs, four historical labels retained as aliases; source scores unchanged.')
