from pathlib import Path
import datetime,hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geode_route_emblem_runtime_v1_20261002';w=r/'audit/job_wash_root_doctor_sequence_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
shutil.copyfile(f/'REVIEW.json',f/'REVIEW_BEFORE_COLOUR_CORRECTION_V293.json')
p=f/'REVIEW.json';d=read(p)
obj=next(x for x in d['individual_objects'] if x['id']=='GEO-SLAB');old=obj['evaluation'];assert 'aqua/lavender' in old;obj['evaluation']=old.replace('broad aqua/lavender support','broad cream top and lavender-sided support');write(p,d)
p=f/'index.html';s=p.read_text(encoding='utf-8');assert s.count('broad aqua/lavender support')==1;s=s.replace('broad aqua/lavender support','broad cream top and lavender-sided support');p.write_text(s,encoding='utf-8',newline='\n')
source=r/'assets/opera/worlds/geology/painted_work_v1_20261001/work_slab.png'
write(f/'SOURCE_COLOUR_CORRECTION_V293.json',dict(status='DIRECT_NATIVE_SOURCE_COLOUR_FACT_CORRECTED_SCORE_UNCHANGED',checked_utc=now,path=source.relative_to(r).as_posix(),sha256=sha(source),previous_evaluation=old,current_evaluation=obj['evaluation'],score=4.6,qualification='Direct whole native source viewed: top is cream, side lavender. Correct prose colour fact only; earlier draft preserved, image pixels, staging and opinion score unchanged.'))
for target,name in [(f,'geode_priority_filter_v293.png'),(w,'doctor_complete_wash_report_v293.png')]:shutil.copyfile(Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')/name,target/name)
write(f/'BROWSER_PRIORITY_REGISTER_QA_V293.json',dict(status='PASS_SOURCE_OR_MOUNTED_PRIORITY_FILTER',checked_utc=now,query='GEO-USE-',selected_lane='Current source or mounted priorities ≤4.5',visible_ids=['GEO-USE-INVITATION','GEO-USE-LIBRARY','GEO-USE-CELEBRATION'],result='3 matching items · showing1–3',celebration_mounted4_2_visible=True,screenshot='geode_priority_filter_v293.png',screenshot_sha256=sha(f/'geode_priority_filter_v293.png'),qualification='Actual browser control verified; source4.6 celebration remains included because mounting4.2. Developer icon4.6 excluded from priority lane, visible in All known items. No new creative acceptance.'))
write(w/'BROWSER_QA.json',dict(status='PASS_CURRENT_WASH_REPORT_RENDER',checked_utc=now,url='http://127.0.0.1:8880/'+w.relative_to(r).as_posix()+'/index.html',title='Doctor washing · every preserved training frame',visible_scores={'workflow':2.7,'contact':2.3,'subject':2.2,'basin':2.9},dated_capture_limit_visible=True,other1818_frames_unreviewed_visible=True,screenshot='doctor_complete_wash_report_v293.png',screenshot_sha256=sha(w/'doctor_complete_wash_report_v293.png'),qualification='Report browser layout/limits verified; not a new gameplay capture or target-device evidence.'))
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
for target,impact in [(f,'job-geode-route-emblem-runtime-20261002.json'),(w,'job-wash-root-doctor-sequence-review-20261002.json')]:
 p=r/'design/audit_impacts'/impact;d=read(p);d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in target.rglob('*') if p.is_file()});write(p,d)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{p.relative_to(r).as_posix() for target in [f,w] for p in target.rglob('*') if p.is_file()}))
print('Native slab colour fact corrected without score/art change; actual mounted-priority and dated-wash browser evidence saved.')
