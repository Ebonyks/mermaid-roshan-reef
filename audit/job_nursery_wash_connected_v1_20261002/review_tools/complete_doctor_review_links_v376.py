from pathlib import Path
import datetime,hashlib,json,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
O=F/'doctor_dated_full_review_v1'
S=R/'assets_src/imagegen/nursery_palm_attention_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip)
new=[F/'review_tools'/Path(__file__).name,F/'review_tools/DOCTOR_LINK_REPAIR_V376.json']
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in new});write(ip,imp)
shutil.copyfile(Path(__file__),new[0])
p=O/'index.html';t=p.read_text(encoding='utf-8');assert t.count('../../../../audit/')==24
t=t.replace('../../../../audit/','../../../audit/');p.write_text(t,encoding='utf-8',newline='\n')
p=R/'audit/job_artwork_refinement_live/all_items.html';t=p.read_text(encoding='utf-8');pos=t.index('<h1>')
link='<p class="review-history"><a href="../job_nursery_wash_connected_v1_20261002/doctor_dated_full_review_v1/index.html">Doctor dated complete wash review: 12 individual priorities, all 1023 frames</a> · <a href="../../assets_src/local_motion/nursery_connected_scrub_v1_20261002/index.html">Nursery local motion A1: rejected 3.6/5</a>. Historical/reference scores do not approve current gameplay.</p>\n'
assert 'class="review-history"' not in t;t=t[:pos]+link+t[pos:];p.write_text(t,encoding='utf-8',newline='\n')
write(new[1],{'status':'DOCUMENT_LINKS_REPAIRED','recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_helper':'review_tools/record_doctor_review_and_reference_block_v375.py','first_helper_error':'The library uses an implicit body; the explicit <body> assertion stopped the final link insertion. Doctor review and authorization-block records were already saved. No production/source pixels changed.','repair':'Inserted evidence links inside the existing library header. Corrected Doctor native-detail links to the repository root; all original image hashes preserved.','native_details_unchanged':all(hashlib.sha256((R/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in read(O/'INDEX.json')['native_details'])})
imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in F.rglob('*') if p.is_file()}|{p.relative_to(R).as_posix() for p in S.rglob('*') if p.is_file()})
imp['validation'].append({'command':'Root direct dated Doctor visual review: all 24 ordered boards / 1023 frames and 12 native details','result':'PASS','evidence':(O/'DIRECT_REVIEW.json').relative_to(R).as_posix()})
imp['validation'].append({'command':'OpenAI built-in image-generation reference edit authorization','result':'PENDING','evidence':(S/'REFERENCE_UPLOAD_BLOCK.json').relative_to(R).as_posix()})
write(ip,imp)
print('DOCTOR_LINKS|native details preserved|dated report and library linked|authorization pending')
