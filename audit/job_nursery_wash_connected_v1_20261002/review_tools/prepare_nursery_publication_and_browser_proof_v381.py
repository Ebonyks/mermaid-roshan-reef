from pathlib import Path
import datetime,hashlib,json,shutil
from urllib.request import urlopen
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_nursery_wash_connected_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
bridge=F/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V381.json'
manifest=R/'audit/job_review_v2_20261001/CONNECTED_NURSERY_WASH_SUPPLEMENT_FILES_V12.json'
receipt=F/'BROWSER_QA_V381.json';target=F/'review_tools'/Path(__file__).name
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip)
proofs=['BROWSER_DOCTOR_DATED_V379.png','BROWSER_DOCTOR_NATIVE_V380.png','BROWSER_REVIEW_MACHINE_V381.png','BROWSER_LIBRARY_UPDATED_V381.png']
planned=[bridge,manifest,receipt,target]+[F/n for n in proofs]
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in planned});write(ip,imp)
shutil.copyfile(Path(__file__),target)
shots=[]
for n in proofs:
 src=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')/n;assert src.is_file();shutil.copyfile(src,F/n)
 shots.append({'path':(F/n).relative_to(R).as_posix(),'sha256':sha((F/n).read_bytes())})
idx=read(F/'doctor_dated_full_review_v1/INDEX.json');http=[]
for row in idx['boards']+idx['native_details']:
 with urlopen('http://127.0.0.1:8880/'+row['path'],timeout=20) as response:raw=response.read();assert response.status==200
 assert sha(raw)==row['sha256'];http.append({'path':row['path'],'sha256':sha(raw),'status':200})
write(receipt,{'status':'PASS_REVIEW_UI_ONLY','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'screenshots':shots,'observed':{'doctor_heading':'Doctor washing: dated captures remain below the action standard','doctor_individual_evaluations':12,'doctor_evidence_images':36,'doctor_native_link_width':1280,'doctor_native_link_height':720,'doctor_native_link_loaded':True,'all_doctor_image_dimensions_reserved':True,'current_nursery_probes':82,'current_nursery_frozen_sources':783,'current_nursery_raw_diagnostics':53,'library_entries':1756,'library_source_cell_region_priorities':690,'library_additional_current_nursery_priorities':10,'library_source_reviews_unassigned':385,'geode_mounted_current_claims':'WITHHELD_STALE_BOUNDARY','reference_motion_a1_action':3.6,'current_game_action':3.9},'exact_local_http_evidence_checks':http,'preserved_browser_issue':'The first lazy Doctor-image click matched a zero-size image before load; after declaring each actual native aspect ratio, the same link opened the full1280x720 native image. No artwork pixels changed. An initial Control+Home key did not scroll the Nursery report; documented browser scroll then reached the actual opening before the final screenshot.','qualification':'UI navigation/labels and local HTTP byte verification only. Draft scores, dated Doctor evidence, rejected motion and current acceptance scopes remain distinct; no device/child/owner/global approval.'})
layout=F/'doctor_dated_full_review_v1/IMAGE_LAYOUT_V380.json';d=read(layout);d['browser_verification']='PASS_FULL_NATIVE_LINK_AND_ALL36_INTRINSIC_DIMENSIONS';d['evidence']=receipt.relative_to(R).as_posix();write(layout,d)
assert not bridge.exists() and not manifest.exists()
write(bridge,{'status':'EXACT_STAGED_SOURCE_BRIDGE_PREPARED','expected_source_count':783})
write(manifest,{'status':'SCOPED_NURSERY_MANIFEST_PREPARED','base_revision':imp['baseline']})
imp=read(ip);imp['validation'].append({'command':'Current report/Doctor illustrated review and native-image browser QA v381','result':'PASS','evidence':receipt.relative_to(R).as_posix()});imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in F.rglob('*') if p.is_file()});write(ip,imp)
print('NURSERY_PUBLICATION_PREPARED|36 exact local HTTP images match|4 browser proofs|manifest/783-source bridge planned')
