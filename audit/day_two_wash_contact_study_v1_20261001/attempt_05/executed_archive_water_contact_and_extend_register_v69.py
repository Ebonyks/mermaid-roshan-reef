from pathlib import Path
import datetime,hashlib,html,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(r).as_posix()
packet=r/'audit/day_two_wash_contact_study_v1_20261001/attempt_05';source=r/'tmp/doctor_sink_water_contact_v68'
assert read(source/'PROCESS_RECEIPT.json')['status']=='PASS_STATIC_CAPTURE_ONLY'
for filename in ['PROFILE.json','PROCESS_RECEIPT.json','parser.stdout.log','parser.stderr.log','inference.stdout.log','inference.stderr.log','analyzer.stdout.log','analyzer.stderr.log','native.stdout.log','native.stderr.log']:
 shutil.copyfile(source/filename,packet/filename)
receipt=read(source/'native_views/CAPTURE_RECEIPT.json');assert len(receipt['views'])==18
rows=[]
for x in receipt['views']:
 native=source/'native_views'/x['path'];assert sha(native)==x['sha256'];shutil.copyfile(native,packet/x['path'])
 original=x['variant']=='original_after_actual_approach'
 shift=x.get('sink_offset_y');flow=x.get('water_on',False);clean='reach_clean_' in x.get('source','')
 if original:
  contact,composition,overall=2.3,2.9,2.9
  text='The actual station approach still leaves Roshan beside the room illustration and a separate procedural hand-washing panel across the screen. Her hands are not visibly working at the depicted sink. This original context remains unchanged and below floor.'
 else:
  contact=4.4;composition=4.4 if shift==0 else 4.3;overall=4.2 if flow else min(contact,composition)
  text=('The complete '+('bare-hand clean ending' if clean else 'soapy reaching figure')+' sits beside the reused shell basin with both wrists attached and the hands near the faucet. Her face, coat and satchel stay visible; the sink cabinet overlaps part of the curled tail and the busy background competes with the small work area. ')
  text+=('The higher sink trims more of the lower fingers at its front rim. ' if shift==-10 else 'The unshifted basin leaves the hand cluster clearer above its front rim. ')
  text+=('The test water line is largely hidden behind the hand pair/foam. At the full native game view the on/off difference is too subtle to communicate a clear stream from the tap over the hands into the basin. Sparse graphic drawing alone does not pass the washing consequence.' if flow else 'With water off, the still pose reads as hands held over the basin, but does not establish running water, rubbing, rinsing or a completed action.')
 rows.append(dict(id=x['path'].removesuffix('.webp'),path=x['path'],sha256=x['sha256'],dimensions=x['viewport'],direct_full_native_review=True,variant=x['variant'],source=x.get('source'),sink_vertical_shift=shift,water_on=flow,hand_sink_contact_score=contact,composition_score=composition,visible_water_score=3.7 if flow else None,individual_static_context_score=overall,evaluation=text,complete_action_score=None,runtime_binding=False))
write(packet/'CAPTURE_RECEIPT.json',receipt)
review=dict(status='ALL18_NATIVE_VIEWS_DIRECTLY_REVIEWED_STATIC_CONTEXT_BELOW_FLOOR',checked_utc=now,direct_full_native_views=18,frames_unreviewed=0,total_direct_contact_views_across_five_attempts=94,items=rows,best_static_no_water_context=4.4,best_hand_sink_contact=4.4,visible_water_consequence=3.7,best_water_on_context=4.2,source_score_not_transferred=4.5,machine_status='PASS_CAPTURE_NO_AWARD_SOURCE_UNCHANGED',qualification='Actual viewport touch approach precedes frozen test-only composition. Every full 1280/1600 by720 native view directly inspected. Game code, original sink and all source portraits unchanged. Static game composition only; no timed action/input-causal result, runtime replacement, device/child/owner or cinematic acceptance.',next_gap='Expose a short clear spout-to-upper-hand stream without hiding or repairing the authored hands; show a downward consequence inside the basin. Then verify the independent palm rub, rinse-to-clean continuity, quiet settle and actual ordinary route.',complete_washing_action_score=None,owner_approval=None,runtime_integration=False)
write(packet/'REVIEW.json',review)
style='body{margin:0;background:#edf4fa;color:#25304a;font:17px/1.5 system-ui}main{max-width:1440px;margin:auto;padding:24px}header,article{background:white;border-radius:16px;padding:20px;margin:0 0 18px}a{color:#504096}h1,h2{line-height:1.25}small,code{display:block;overflow-wrap:anywhere}img{width:100%;height:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(450px,1fr));gap:18px}.grid article{min-width:0}.score{font-weight:bold;color:#8e451f}@media(max-width:520px){.grid{grid-template-columns:1fr}}'
cards=''.join(f'<article><h2>{html.escape(x["id"])}</h2><img loading="lazy" src="{x["path"]}" alt="Complete native game-size sink contact view {html.escape(x["id"])}"><p class="score">Static context {x["individual_static_context_score"]}/5 · hand contact {x["hand_sink_contact_score"]}/5 · composition {x["composition_score"]}/5</p><p>{html.escape(x["evaluation"])}</p><small>{x["sha256"]}</small></article>' for x in rows)
(packet/'index.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doctor: tap and clean-hand contact study</title><style>{style}</style><main><header><a href="../../job_review_v2_20261001/index.html">Current audit entry</a><h1>Doctor sink: water and matching clean hands</h1><p class="score">Every 18 native views directly reviewed · best still contact 4.4/5 · visible water 3.7/5</p><p>Reuses the original painted sink and complete outward soapy/clean sources. The water is too hidden at game size, so no mounted or complete washing pass follows. All five contact attempts remain inspectable: 94 direct native views.</p><p><a href="REVIEW.json">Each view and complete written evaluation</a> · <a href="CAPTURE_RECEIPT.json">Exact viewport/source/anchor evidence</a> · <a href="PROCESS_RECEIPT.json">Machine checks and unchanged sources</a> · <a href="../attempt_04/index.html">Preserved earlier reaching placement</a></p></header><div class="grid">{cards}</div></main></html>',encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),packet/'executed_archive_water_contact_and_extend_register_v69.py')
license=r/'ASSET_LICENSES.md';text=license.read_text(encoding='utf-8')
for x in rows:
 p=packet/x['path']
 if f'`{rel(p)}`' not in text:text+=f'\n| `{rel(p)}` | Local official Godot 4.7.2 Mobile-rendered isolated review fixture; source/anchors in adjacent CAPTURE_RECEIPT.json, SHA-256 `{x["sha256"]}`. | Project/generated review artwork, underlying original licenses retained. | Internal native viewport capture, 2026-10-01. | Complete unmodified lossless native WebP, static review only, individual context {x["individual_static_context_score"]}/5, no runtime/owner/cinematic acceptance. |\n'
license.write_text(text,encoding='utf-8',newline='\n')
impactfile=r/'design/audit_impacts/job-doctor-reach-water-contact-study-20261001.json';impact=read(impactfile)
impact['files']=sorted(set(impact['files'])|{rel(p) for p in packet.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md'})
impact['validation']=[dict(command='Parser, inference, official4.7.2 analyzer/native capture and literal source/no-award assertions',result='PASS',evidence=rel(packet/'PROCESS_RECEIPT.json')),dict(command='Direct full-native review of all18 water/clean static contact variants',result='FAIL',evidence=rel(packet/'REVIEW.json')+'; best hand/still contact4.4, visible water3.7, water-on context4.2; all below floor.')]
impact['acceptance_gaps']=review['qualification']+' '+review['next_gap'];write(impactfile,impact)
old=r/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v10.py'
s=old.read_text(encoding='utf-8')
needle="for q in items.values():\n p=q['path']\n if p not in hashes:"
assert s.count(needle)==1
addition="""# Matching fresh clean-reaching source is source-only, even after static contact review.
reachclean=read('assets_src/imagegen/day2_doctor_wash_reach_clean_v1_20261001/ATTEMPT01_REVIEW.json');p=reachclean['path']
items[p]=dict(id=reachclean['id'],aliases=[],kind='source',path=p,earlier_sha256=reachclean['sha256'],historical_source_score=reachclean['source_score'],evaluation=reachclean['evaluation'],refinement='Source-only4.5 clean ending remains unbound. All18 new native sink/water views are below4.5; best still contact4.4, visible water3.7, water-on context4.2. Require independent rubbing, a visible rinse and matched quiet return.',families=['Day Two washing','Unbound matching clean-reaching doctor source'],original_reports=['assets_src/imagegen/day2_doctor_wash_reach_clean_v1_20261001/index.html'],source_qualification=reachclean['qualification'],preview_path=p,native_reference_observations=[],runtime_binding_state=reachclean['status'],latest_refinement=dict(report='audit/day_two_wash_contact_study_v1_20261001/attempt_05/index.html',note='Every18 full native static water/clean placement directly reviewed; all94 contact views preserved. Source4.5 does not pass static/context or complete action.'))
items[reach['path']]['latest_refinement']=dict(report='assets_src/local_motion/day2_doctor_wash_reach_rub_study_v1_20261001/index.html',note='Every41 new local native motion frames directly reviewed: reference4.0, independent palm stroke3.9, entry3.8 and exact return4.0. Complete contextual washing remains open. All94 native static sink/contact views are retained; best4.4, water visibility3.7.')
"""
s=s.replace(needle,addition+needle)
s=s.replace('Union of two existing discovery inventories and240 individually catalogued pose cells.','Union of two existing discovery inventories, 328 individually catalogued pose cells and 38 prop regions, plus named reversible replacement sources.')
s=s.replace('review_tools/build_current_job_item_register_v8.py','review_tools/build_current_job_item_register_v11.py')
s=s.replace('snapshot,240 source pose cells,6 current pool regions and32 individually inspected craft prop regions.','snapshot, 328 source pose cells, 6 current pool regions and 32 individually inspected craft prop regions, including the complete shared-source native review.')
new=r/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v11.py';new.write_text(s,encoding='utf-8',newline='\n')
result=subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(new)],cwd=r,capture_output=True,text=True,encoding='utf-8');assert result.returncode==0,result.stderr
counts=read(r/'audit/job_artwork_refinement_live/ALL_ITEMS.json')['counts'];assert counts['registered_items']==1519 and counts['unique_source_files']==1153 and counts['individual_pose_cells']==328 and counts['inclusive_current_source_priorities']==558
master=r/'audit/MASTER_AUDIT_2026-08-09.md';s=master.read_text(encoding='utf-8')
s=s.replace('now contains1518 entries,1152 source files,328 pose cells and38 prop regions, with557 inclusive source priorities and395 unassigned source opinions.','now contains 1519 entries, 1153 source files, 328 pose cells and 38 prop regions, with 558 inclusive source priorities and 395 unassigned source opinions.')
paragraph='\nLater matching clean/water review (2026-10-01): the [complete clean-reaching source](../assets_src/imagegen/day2_doctor_wash_reach_clean_v1_20261001/index.html) meets source-only 4.5. [Every 41 outward-rub native frames](../assets_src/local_motion/day2_doctor_wash_reach_rub_study_v1_20261001/index.html) are directly reviewed, reference 4.0 / independent stroke 3.9 / entry 3.8 / exact return 4.0. [Every 18 static tap/clean variants](day_two_wash_contact_study_v1_20261001/attempt_05/index.html) brings the direct contact record to 94 views; best still contact 4.4 and visible water 3.7 remain below floor. Source images, complete static views and motion frames retain individual evaluations; no runtime action, device, child, owner or cinematic acceptance. [Contact impact](../design/audit_impacts/job-doctor-reach-water-contact-study-20261001.json).\n'
if 'Later matching clean/water review (2026-10-01)' not in s:s=s.replace('\n## 0. Planning entry',paragraph+'\n## 0. Planning entry',1)
if paragraph not in s and 'Later matching clean/water review (2026-10-01)' not in s:s=paragraph+s
master.write_text(s,encoding='utf-8',newline='\n')
ledger=r/'design/05_DOC_LEDGER.md';s=ledger.read_text(encoding='utf-8').replace('has1518 entries,557 inclusive source priorities and395 unassigned source opinions.','has 1519 entries, 558 inclusive source priorities and 395 unassigned source opinions.')
ledger.write_text(s,encoding='utf-8',newline='\n')
for file in [r/'audit/job_review_v2_20261001/index.html',r/'audit/job_artwork_refinement_live/index.html']:
 s=file.read_text(encoding='utf-8').replace('Search1,518 known','Search 1,519 known').replace('contains557 source priorities','contains 558 source priorities').replace('catalogues1152 source files,328 pose cells and38 prop regions','catalogues 1153 source files, 328 pose cells and 38 prop regions')
 links=('<section><h2>Current matching clean hands and water contact</h2><p><a href="../../assets_src/imagegen/day2_doctor_wash_reach_clean_v1_20261001/index.html">Clean-reaching source: 4.5 only</a> · <a href="../../assets_src/local_motion/day2_doctor_wash_reach_rub_study_v1_20261001/index.html">Every 41 new motion frames: 4.0</a> · <a href="../day_two_wash_contact_study_v1_20261001/attempt_05/index.html">Every 18 new native water/clean views: below floor</a> · <a href="../job_shared_source_native_review_v1_20261001/index.html">Eight shared sources and 94 individual native regions</a>.</p><p>94 complete static contact views across five attempts remain inspectable. The source and static motion lanes are separate from complete in-game action and owner acceptance.</p></section>')
 if 'Current matching clean hands and water contact' not in s:s=s.replace('</main>',links+'</main>',1)
 file.write_text(s,encoding='utf-8',newline='\n')
combined=read(r/'design/audit_impacts/job-shared-native-source-review-20261001.json')
combined['files']=sorted(set(combined['files'])|{rel(new),'audit/job_artwork_refinement_live/review_tools/build_current_job_item_register_v11.py','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','audit/job_review_v2_20261001/index.html','audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/all_items.html','audit/job_artwork_refinement_live/STATUS.json','design/audit_impacts/job-review-separate-v2-20261001.json'})
combined['scope']+=' Refresh the individually illustrated register with one separately scored matching clean-reaching source and all new motion/contact links; 1519 entries,558 inclusive source priorities,395 unassigned source opinions. No global or actual-use acceptance.'
write(r/'design/audit_impacts/job-shared-native-source-review-20261001.json',combined)
allow=r/'tmp/v2_preview_allowed.json';d=read(allow);paths={rel(p) for p in packet.rglob('*') if p.is_file()}|{rel(new),'audit/job_artwork_refinement_live/review_tools/build_current_job_item_register_v11.py'}
if isinstance(d,list):d=sorted(set(d)|paths)
else:
 key=next(k for k,v in d.items() if isinstance(v,list));d[key]=sorted(set(d[key])|paths)
write(allow,d)
print(json.dumps(dict(counts=counts,new_water_contact_views=18,all_direct_contact_views=94,source_files_unchanged=read(source/'PROCESS_RECEIPT.json')['source_unchanged'])))
