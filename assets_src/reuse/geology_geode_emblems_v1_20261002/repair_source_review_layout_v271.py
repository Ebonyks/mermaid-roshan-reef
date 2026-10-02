from pathlib import Path
import datetime, json, re, shutil

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
families=[('assets_src/reuse/geology_geode_emblems_v1_20261002','job-geology-geode-emblem-reuse-20261002.json'),('assets_src/imagegen/geologist_grotto_native2k_v1_20261002','job-geology-grotto-native-resolution-20261002.json'),('audit/job_training_shared_source_review_v1_20261002','job-training-shared-source-review-20261002.json')]
for rel,impact in families:
 f=b/rel;p=f/'index.html';s=p.read_text(encoding='utf-8');snapshot=f/'index_LAYOUT_BEFORE_V271.html';assert not snapshot.exists();shutil.copyfile(p,snapshot)
 css=re.search(r'<style>(.*?)</style>',s,re.S).group(1)
 corrected=re.sub(r'#[0-9a-fA-F]+(?: +[0-9a-fA-F]+)*',lambda m:m.group(0).replace(' ',''),css)
 corrected=corrected.replace('h 1{','h1{')
 s=s.replace('<style>'+css+'</style>','<style>'+corrected+'</style>')
 # Exact source identifiers are technical facts, not prose to normalize.
 s=s.replace('geologist_painted_rebuild_v 1_','geologist_painted_rebuild_v1_').replace('EncounterGestureGuide 2D.','EncounterGestureGuide2D.').replace('2048x 1024','2048 × 1024')
 p.write_text(s,encoding='utf-8',newline='\n')
 prior=f/'BROWSER_QA.json'
 if prior.exists():shutil.copyfile(prior,f/'BROWSER_QA_V1.json')
 write(f/'LAYOUT_CORRECTION_V271.json',dict(status='CORRECTED_PENDING_BROWSER_RECHECK',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reason='Earlier prose spacing pass also reached CSS raw text, inserting spaces into hexadecimal colors and h1 selector. Images loaded but caption backgrounds disappeared; dark-panel labels had poor contrast. Preserve earlier page/QA; repair only CSS declarations and exact source labels, without changing artwork or scores.',before='index_LAYOUT_BEFORE_V271.html',after='index.html',css_before=css,css_after=corrected))
 ip=b/'design/audit_impacts'/impact;d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
f=b/families[0][0];p=f/'REVIEW.json';d=read(p);assert len(d['individual_items'])==8;shutil.copyfile(p,f/'REVIEW_V1.json')
opinions=[dict(id='GEO-INVITATION-EXISTING-142',width=142,role='Existing approved closed source, isolated invitation-size review',score=4.6,actual_route_score=4.5,evaluation='The rounded lavender stone and broad pale violet/aqua planes remain clear at literal 142px. One dark central seam invites opening. This existing source is acceptable; its actual route invitation has a separate 4.5 presentation opinion and later transitions to a different authored closed family. Preserve it rather than inventing a source defect.',direct_review=True,owner_acceptance=None),dict(id='GEO-INVITATION-REUSE-142',width=142,role='Current opening-family closed source, isolated invitation-size reuse',score=4.5,actual_route_score=None,evaluation='The wider rounded purple shell, darker plum contour and broad aqua lower band read clearly at literal 142px. Its single central seam and rounded body match the current seven-state opening family. Isolated presentation reaches 4.5 provisionally; invitation placement, pulse, touch geometry and whole-route continuity require actual mounted review after binding.',direct_review=True,owner_acceptance=None)]
d['individual_items'].extend(opinions);d['status']='ALL10_ISOLATED_REUSE_PRESENTATIONS_REVIEWED_NOT_MOUNTED';d['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();d['qualification']='Ten isolated browser presentations individually inspected, with actual-route scores retained separately. Same-source closed 142px and open 50px reuse reach 4.5 provisionally; open larger sizes4.6. No new generation or image pixel edits; no mounted/device/child/owner acceptance.';write(p,d)
p=f/'index.html';s=p.read_text(encoding='utf-8');old='Isolated comparison review pending; no production binding is changed.';assert old in s;s=s.replace(old,'Existing closed source 4.6/5; same opening-family isolated closed preview 4.5/5 provisional. Both were directly reviewed at 142px. Actual invitation-to-opening placement, input and continuity await binding.');p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/Path(__file__).name)
ip=b/'design/audit_impacts/job-geology-geode-emblem-reuse-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
allow=b/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{p.relative_to(b).as_posix() for rel,_ in families for p in (b/rel).rglob('*') if p.is_file()}))
# K has not been prepared. Disable broad prose transformations before execution.
p=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/prepare_geology_checkpoint_k_v264.py');s=p.read_text(encoding='utf-8');old="def prose(s):return re.sub(r'(?<=[a-z])(?=\\d)', ' ',s)";assert old in s;s=s.replace(old,'def prose(s):return s').replace('entries,675 inclusive','entries,676 inclusive');p.write_text(s,encoding='utf-8',newline='\n');compile(s,str(p),'exec')
print('Repaired three new source-page CSS blocks; preserved prior layouts/QA; ten opinions complete. K broad prose normalization disabled.',flush=True)
