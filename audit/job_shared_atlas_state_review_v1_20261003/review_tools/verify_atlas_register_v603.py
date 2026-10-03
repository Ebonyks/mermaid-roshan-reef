from pathlib import Path
import datetime,hashlib,json,shutil,sys
from PIL import Image
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');ROOT=Path('C:/Users/Peter/Documents/mermaid-roshan-reef');S=B/'audit/job_shared_atlas_state_review_v1_20261003';L=B/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda x:hashlib.sha256(x).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):
 n=p.with_name(p.name+'.v603_next');n.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());n.replace(p)
sys.path.insert(0,str(L/'review_tools'));from register_parts_v51 import load_register
r=load_register(L);old=read(S/'previous_v50/ALL_ITEMS.json');assert r['items'][:2050]==old['items'],'Existing item identities/opinions must remain identical'
assert len(r['items'])==2138 and len({q['id'] for q in r['items']})==2138
stamp=read(L/'CURRENT_BOUNDARY_REFRESH.json');assert stamp['registry_root_sha256']==sha((L/'ALL_ITEMS.json').read_bytes()) and stamp['registry_items']==stamp['registered_source_matches']==2138 and stamp['registry_parts']==r['item_shards'] and stamp['assembled_registry_parts_verified']
assert stamp['candy_capture_boundary_match'] and stamp['candy_capture_source_count']==783 and not stamp['geode_capture_boundary_match'] and not stamp['nursery_capture_boundary_match']
for label in ['authority','development','document_tests','game2d','register_parts']:assert read(S/'gates_v1'/(label+'.receipt.json'))['status']=='PASS'
partcheck=read(S/'REGISTER_PART_CHECK.json');partcheck.update(status='PASS_LITERAL_ROOT_PART_ALL2138_HASHES_9_REGISTER_TESTS',checked_utc=now(),source_matches=2138,existing2050_records_identical=True,register_negative_and_positive_tests=9,browser_loaded_assembled_entries=2138,qualification='Root/part literal SHA,size,count,unique IDs and all2138 source/binding refresh entries verified. Python tests reject missing/tampered/duplicate/path escape/over-ceiling/count errors. Browser independently loads and hashes the additional part; no timed/game/device/child/owner acceptance.');write(S/'REGISTER_PART_CHECK.json',partcheck)
proofs=[]
for name in ['ATLAS_BROWSER_PROOF_V601.jpg','ATLAS_BROWSER_PROOF_FULL_V602.jpg']:
 src=ROOT/'tmp'/name;dst=S/name;assert src.exists();shutil.copyfile(src,dst);im=Image.open(dst);assert im.format=='JPEG' and list(im.size)==[1265,712]
 proofs.append(dict(path=dst.relative_to(B).as_posix(),sha256=sha(dst.read_bytes()),bytes=dst.stat().st_size,dimensions=list(im.size),format=im.format))
write(S/'BROWSER_VERIFY_V603.json',dict(status='ACTUAL_REPORT_AND_V51_PART_LOADED_IN_BROWSER',checked_utc=now(),browser_id='2',tab_id='71',viewport=[1280,720],document_width=1265,report_cell_articles=88,report_players=11,report_native_visible_cell_dimensions=[244,502],next_key_control_observed='Entry 2/12 · cell1',library_entries=2138,library_source_files=1286,library_source_object_regions=373,library_inclusive_priorities=1041,library_primary_pending=294,library_filtered_id='D2X-0065-CELL-01',library_filtered_source_score=2.7,library_current_geode_mounted_priorities=0,library_current_nursery_mounted_priorities=0,library_current_candy_priorities=48,library_filtered_atlas_loaded_dimensions=[976,1004],screenshots=proofs,qualification='Actual browser DOM and JPEG observations. Report preserves native crop dimensions; lazy images outside the viewed range are not claimed loaded. Full timed player/action/device/child/owner acceptance remains unassigned.'))
page=L/'all_items.html';raw=page.read_bytes();oldcmd=b'refresh_current_job_review_v50.py';assert raw.count(oldcmd)==1;n=page.with_name(page.name+'.v603_next');n.write_bytes(raw.replace(oldcmd,b'refresh_current_job_review_v51.py'));n.replace(page)
licenses=B/'ASSET_LICENSES.md';text=licenses.read_text(encoding='utf-8')
for p in proofs:
 if p['path'] not in text:text+='\n| `'+p['path']+'` | Actual local browser QA screenshot of the owner-directed individual shared-prop artwork report. | Project audit evidence; underlying art retains source attribution | N/A (localhost preview) | Native browser JPEG '+str(p['dimensions'])+'; screenshot only, no artwork replacement or runtime/cinematic delivery. |'
n=licenses.with_name(licenses.name+'.v603_next');n.write_bytes((text.rstrip()+'\n').encode());n.replace(licenses)
shutil.copyfile(__file__,S/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-shared-atlas-state-review-20261003.json';d=read(ip);d['files']=sorted(set(d['files']+[p.relative_to(B).as_posix() for p in S.rglob('*') if p.is_file()]));d['validation'][2].update(result='PASS',evidence='audit/job_shared_atlas_state_review_v1_20261003/REGISTER_PART_CHECK.json/BROWSER_VERIFY_V603.json/gates_v1:2138 exact registered source hashes,2050 earlier records unchanged,88 new native state opinions,9 part tests and52 document tests; authority/development all OK,2D no-regression only. Final staged bytes require their own checks.');write(ip,d)
print('VERIFIED_2138_IDENTICAL2050_PLUS88_AND_BROWSER',proofs,flush=True)
