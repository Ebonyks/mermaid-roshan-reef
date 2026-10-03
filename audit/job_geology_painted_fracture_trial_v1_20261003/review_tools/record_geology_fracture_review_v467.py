from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, os

R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
J=R/'audit/job_geology_painted_fracture_trial_v1_20261003'
L=R/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='ce154e1452c92252b90f5455989a21726d94ff62'
assert not (J/'DIRECT_REVIEW_ATTEMPT02.json').exists()
boundary=read(J/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files']
assert len(boundary)==783 and all(sha(R/x['path'])==x['sha256'] for x in boundary)
m=read(J/'QA_BOARD_MANIFEST_A2.json')
assert len(m['boards'])==47 and sum(x['count'] for x in m['boards'])==493
for b in m['boards']:
 assert sha(R/b['path'])==b['sha256'];b['direct_review']=True
 for v in b['members']:
  assert sha(R/v['path'])==v['sha256'];v['direct_review']=True
m['status']='ALL_435_CONSECUTIVE_FRAMES_AND_58_SELECTED_CANVASES_DIRECTLY_REVIEWED'
m['reviewed_utc']=now
write(J/'QA_BOARD_MANIFEST_A2.json',m)
details=[];reviewed=[];threshold=[]
for width,indices,before,after,complete in [(1280,[104,105,140,165,190,201],104,105,201),(1600,[102,103,138,163,188,199],102,103,199)]:
 cap=read(J/'attempt02'/f'CAPTURE_{width}.json')
 chosen=[x for x in cap['views'] if any(x['path'].endswith(f'_phase1_{tag}.webp') for tag in ['brushed','one_piece','two_pieces','earned_completion'])]
 chosen += [cap['motion_frames'][i] for i in indices]
 assert len(chosen)==10
 for x in chosen:
  assert sha(R/x['path'])==x['sha256']
  details.append({'path':x['path'],'sha256':x['sha256'],'direct_review':True,'scope':'Original entire native canvas inspected independently of ordered QA boards.'})
 for kind in ['motion_frames','views']:
  for x in cap[kind]:
   assert sha(R/x['path'])==x['sha256']
   reviewed.append({'path':x['path'],'sha256':x['sha256'],'width':width,'kind':kind,'direct_review':True,'review_method':'Consecutive entire native canvases on full-aspect row-major QA boards, with 20 original native details inspected separately.','index_or_state':x.get('index',x.get('state'))})
 assert cap['motion_frames'][before]['surface']['stage']=='FOSSIL_BRUSH'
 assert cap['motion_frames'][after]['surface']['stage']=='FOSSIL_ASSEMBLE'
 assert cap['motion_frames'][complete]['surface']['complete']
 threshold.append({'width':width,'brush_last_index':before,'fragments_first_index':after,'complete_first_index':complete,'qualification':'Actual independently inspected A2 native frames and captured state, not inherited A1 indices.'})
opinions=[]
def op(item,score,evaluation,refinement):
 opinions.append({'item':item,'score':score,'priority_inclusive':score<=4.5,'meets_floor_provisional':score>=4.5,'evaluation':evaluation,'refinement':refinement,'scope':'A2 NON_RUNTIME_COUNTERFACTUAL inherited fracture renderer only. Does not replace current production score or grant owner/device/child acceptance.'})
for name in ['left fragment','middle fragment','right fragment']:
 op(name,4.5,'The conserved painted lavender stone and warm spiral now end in complementary irregular fracture silhouettes. Restrained plum contours follow only opaque exposed internal cuts; native drag frames retain readable material and a coherent silhouette without the unfinished strip edge seen in A1. Provisional floor; minor raster contour aliasing remains.','Preserve the exact shared partition, original source and touch margin. Review actual production binding, pointer/hand contact and device-scale clarity before acceptance; 4.5 remains an inclusive priority.')
op('reassembled fossil',4.5,'The spiral rejoins continuously in both native aspects. Internal contour strokes disappear when both adjacent pieces are snapped, restoring the original painted surface without added seams or duplicated material.','Preserve adjacent-snap suppression. Test reversible runtime binding, restore/repeat and physical-device readability independently.')
op('intact fossil material',4.5,'The original reusable broad painted lavender stone and warm spiral retain their storybook identity. The material is unchanged; the repaired renderer does not require a newly generated bitmap.','Keep the original source and attribution. Material quality does not establish contact or action quality.')
op('soil clearing',3.9,'The unchanged inherited brush grid still reveals the fossil coarsely and removes remaining soil at the threshold. Cleaner fragment contours do not repair clearing.','Develop gradual, truthful brush/soil removal in a separate reversible action study and inspect every rendered input/wait frame.')
op('brush-to-fragments transition',3.2,'Native threshold pairs 1280:104→105 and1600:102→103 show the remaining soil vanishing and fragments appearing at remote homes abruptly. Geometry continuity after assembly does not excuse this staging jump.','Repair reveal/separation continuity and retain the specimen in a readable working area; recapture every frame against the actual input path.')
op('working hand contact',2.7,'Roshan stays away from the working specimen during brushing and dragging. Neither a visible brush/stone touch nor a gripping action is established.','Build and audit connected work/contact poses and sequencing at the actual surface; preserve one-finger mechanics and truthful cause/effect.')
op('ghost fossil target',4.2,'The faint intact target remains a useful placement aid, but a moving piece overlapping it can read as a doubled spiral/material patch.','Review target opacity and overlap throughout full drags and snaps without hiding the fragment or depending on text.')
op('room',2.8,'The surrounding flat bands, generic spotlights and empty stage remain visibly below the painted world language. The fracture study changes none of them.','Inventory and qualify a painted room with required native coverage, then audit layering and interaction clearance in actual play.')
op('earned completion transition',4.0,'Actual intentional completion and normal Library return still work, but generic celebration presentation loses the restored specimen context.','Keep the completed fossil grounded and visible through its celebration; independently review full action, return and replay.')
op('whole fossil action',3.6,'Fragment material reaches the provisional floor, but coarse clearing, abrupt separation, distant hands and generic celebration keep the complete sequence below it. No material score is transferred to the action.','Continue truthful reveal/contact/celebration refinement and complete recapture; actual production action remains separately scored3.2.')
write(J/'DIRECT_REVIEW_ATTEMPT02.json',{'status':'FRAGMENTS_AND_JOIN_4_5_PROVISIONAL_WHOLE_ACTION_3_6_REJECTED_FOR_FLOOR','reviewed_utc':now,'consecutive_frames':435,'selected_views':58,'ordered_boards':47,'native_details':details,'reviewed_canvases':reviewed,'threshold_pairs':threshold,'opinions':opinions,'source_sha256':sha(R/'assets/opera/worlds/geology/painted_work_v1_20261001/fossil.png'),'fixture_sha256':{'capture':sha(J/'capture.gd'),'surface':sha(J/'painted_fracture_surface.gd')},'production_binding':False,'owner_acceptance':None,'qualification':'Actual inherited Library four-phase intentional-input route, earned Library return and elevator developer entry/Back, with an explicit draw-only counterfactual substitution. Complete fossil action only; pan/geode selected views. Main/Castle entry fixture, isolated saves, desktop Mobile and slow readback do not establish ordinary travel, natural pacing, phone, child, owner or all-job acceptance. All783 production files remain unchanged.'})
write(J/'PREFLIGHT_V465.json',{'status':'RUNNER_LAUNCH_ERROR_PRESERVED_AND_CORRECTED_BEFORE_CAPTURE','error_type':'shutil.SameFileError','cause':'Launching the preserved canonical runner in review_tools made its archive-copy source equal its destination. This happened before Godot gates/captures started.','correction':'Copied the exact runner to the intended primary staging tmp path and launched from there. No renderer or production change; both fresh captures and all six checks passed.','successful_runner':'review_tools/run_geology_fracture_trial_v465.py','evidence':'runtime_gate_a2/','qualification':'Helper launch error, not a game/analyzer/capture failure. Raw later gates remain authoritative.'})
qahelper=Path(__file__).with_name('check_fracture_board_pixels_v466.py')
shutil.copyfile(qahelper,J/'review_tools'/qahelper.name)
out=subprocess.run([os.sys.executable,'-X','utf8','-B',str(qahelper)],cwd=R,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
(J/'QA_CELL_SPOT_CHECK_V466.stdout.log').write_bytes(out.stdout)
(J/'QA_CELL_SPOT_CHECK_V466.stderr.log').write_bytes(out.stderr)
assert out.returncode==0
checks=[json.loads(line) for line in out.stdout.decode('utf-8').splitlines()]
assert len(checks)==5 and all(x['index']==x['closest_source_index'] for x in checks)
write(J/'QA_CELL_SPOT_CHECK_V466.json',{'status':'DECLARED_SOURCE_CLOSEST_FOR_ALL5_SPOT_CHECKED_CELLS','checked_utc':now,'rows':checks,'method':'Read-only FFmpeg decoded raw bytes in memory; each declared QA cell compared with all12 scaled native members of the same board. No image mutation or generated asset.','qualification':'Literal raw-pixel equality is false. Thumbnail differences are retained; closest-source checks provide only bounded ordering evidence. Original full-native files and complete direct review remain authoritative.'})
for old,new in [('ALL_ITEMS.json','ALL_ITEMS_V40.original.json'),('all_items.html','all_items_V40.original.html'),('CURRENT_BOUNDARY_REFRESH.json','BOUNDARY_V40.original.json')]:
 assert not (L/new).exists();shutil.copyfile(L/old,L/new)
reg=read(L/'ALL_ITEMS.json');oldcounts=dict(reg['counts'])
ids={'left fragment':'GEO-FOSSIL-LEFT','middle fragment':'GEO-FOSSIL-CENTRE','right fragment':'GEO-FOSSIL-RIGHT','reassembled fossil':'GEO-FOSSIL-JOINED','intact fossil material':'GEO-WORK-FOSSIL','soil clearing':'GEO-FOSSIL-CLEARING','brush-to-fragments transition':'GEO-FOSSIL-FRACTURE','working hand contact':'GEO-FOSSIL-HAND','ghost fossil target':'GEO-FOSSIL-TARGET','room':'GEO-ROOM','earned completion transition':'GEO-FOSSIL-PAN-RESET','whole fossil action':'GEO-FOSSIL-FULL'}
byid={x['id']:x for x in reg['items']}
for attempt in [1,2]:
 rev=read(J/f'DIRECT_REVIEW_ATTEMPT0{attempt}.json')
 for opinion in rev['opinions']:
  ident=ids[opinion['item']];assert ident in byid
  byid[ident].setdefault('candidate_reviews',[]).append({'attempt':attempt,'report':J.relative_to(R).as_posix()+f'/index.html#attempt0{attempt}','review':J.relative_to(R).as_posix()+f'/DIRECT_REVIEW_ATTEMPT0{attempt}.json','score':opinion['score'],'evaluation':opinion['evaluation'],'refinement':opinion['refinement'],'production_binding':False,'scope':opinion['scope'],'reviewed_utc':rev['reviewed_utc']})
reg['display_revision']='V41_PAINTED_FOSSIL_FRACTURE_CANDIDATE_HISTORY'
reg['updated_utc']=now
reg['scope']+=' V41 appends two explicitly unbound fossil fracture attempts: all868 consecutive frames/116 selected views,24 separate component/action opinions. A1 fragment4.4 rejected;A2 fragments/join4.5 provisional;whole3.6. Current production mounted/action scores and all1821 counts remain unchanged.'
reg['review_resources'].append({'path':J.relative_to(R).as_posix()+'/index.html','scope':'Two non-runtime painted fracture attempts;all868 frames/116 selected views directly reviewed;A1 cut edges4.4 rejected,A2 fragments/join4.5 provisional,whole3.6. Current production scores unchanged.'})
assert reg['counts']==oldcounts and len(reg['items'])==1821
(L/'ALL_ITEMS.json').write_text(json.dumps(reg,separators=(',',':'),ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert (L/'ALL_ITEMS.json').stat().st_size<4194304
html=(L/'all_items.html').read_text(encoding='utf-8-sig')
link='<p><a href="../job_geology_painted_fracture_trial_v1_20261003/index.html">New: painted fossil fracture review — both attempts, every frame and individual opinions</a>. Unbound A2 fragments/join4.5; whole action3.6. Current production scores remain separate.</p>'
assert '</header>' in html
html=html.replace('</header>',link+'</header>',1)
# Display candidate history inside each existing item card without changing current scores.
needle='q.latest_refinement'
assert needle in html
card='${q.candidate_reviews?\'<details><summary>Unbound candidate history (current scores unchanged)</summary>\'+q.candidate_reviews.map(c=>\'<p><a href="\'+esc(url(c.report))+\'">Attempt \'+esc(c.attempt)+\': \'+esc(c.score)+\'/5</a><br>\'+esc(c.evaluation)+\'<br>Refine: \'+esc(c.refinement)+\'</p>\').join(\'\')+\'</details>\':\'\'}'
html=html.replace('<details><summary>Identity, hashes and reference evidence</summary>',card+'<details><summary>Identity, hashes and reference evidence</summary>',1)
html=html.replace('latest_refinement:q.latest_refinement,native_reference_observations:', 'latest_refinement:q.latest_refinement,candidate_reviews:q.candidate_reviews,native_reference_observations:',1)
(L/'all_items.html').write_text(html,encoding='utf-8',newline='\n')
write(J/'REGISTER_CHANGE_PROOF_V41.json',{'status':'CANDIDATE_HISTORY_ONLY_CURRENT_PRODUCTION_SCORES_COUNTS_UNCHANGED','before_register_sha256':sha(L/'ALL_ITEMS_V40.original.json'),'after_register_sha256':sha(L/'ALL_ITEMS.json'),'counts':oldcounts,'candidate_opinions_added':24,'ids':list(ids.values()),'current_mounted_scores_unchanged':all(x.get('current_mounted_score')=={y['id']:y for y in read(L/'ALL_ITEMS_V40.original.json')['items']}[x['id']].get('current_mounted_score') for x in reg['items']),'production_files_unchanged':783})
shutil.copyfile(Path(__file__),J/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-painted-fracture-trial-20261003.json';impact=read(ip)
impact['scope']+=' A2 all435frames/58views/47boards/20 native details directly reviewed; three fragments and joined4.5 provisional, whole3.6. A1 rejected4.4 preserved. V41 appends24 candidate opinions without changing any production score/count; exact V40 register/page/boundary preserved.'
impact['validation'][0].update(result='PASS',evidence=J.relative_to(R).as_posix()+'/DIRECT_REVIEW_ATTEMPT02.json; direct review complete, quality failures remain.')
impact['validation'][1].update(result='PASS',evidence=J.relative_to(R).as_posix()+'/runtime_gate_a1/ and runtime_gate_a2/;all six checks each,783 unchanged production files.')
impact['files']=sorted(set(impact['files'])|{x.relative_to(R).as_posix() for x in J.rglob('*') if x.is_file()}|{(L/x).relative_to(R).as_posix() for x in ['ALL_ITEMS.json','all_items.html','ALL_ITEMS_V40.original.json','all_items_V40.original.html','BOUNDARY_V40.original.json']})
write(ip,impact)
assert all(sha(R/x['path'])==x['sha256'] for x in boundary)
print(json.dumps({'status':'A2_REVIEW_RECORDED_V41_CANDIDATE_HISTORY_ONLY','boards':47,'frames':435,'views':58,'native_details':20,'opinions':12,'production_unchanged':783,'register_items':1821,'register_bytes':(L/'ALL_ITEMS.json').stat().st_size,'spot_check_indices':[x['index'] for x in checks]}))
