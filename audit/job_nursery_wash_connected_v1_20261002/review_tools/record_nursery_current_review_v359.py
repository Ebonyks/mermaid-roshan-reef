from pathlib import Path
import json,hashlib,datetime,shutil,html
from PIL import Image
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002';S=R/'assets_src/imagegen/nursery_wash_connected_v1_20261002'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
index=read(F/'current_visual_v3/INDEX.json')
assert len(index['boards'])==36 and len(index['native_details'])==36
assert all(sha(R/x['path'])==x['sha256'] for x in index['boards']+index['native_details'])
boundary=read(F/'SOURCE_CURRENT_MACHINE_V3.json')
assert all(sha(R/x['path'])==x['sha256'] for x in boundary['source_files'])
states={
 'ready':(4.5,'The connected wrists and body lead to a clearly bounded basin. Cream lip, aqua bowl and lilac pedestal retain painted broad values. The held hint lies inside the bowl rather than hiding a hand. The forward gaze is friendly but does not show attention to the wash.'),
 'wet':(4.5,'The gold spout reaches the actual joined hands with a visible aqua stream and small splash inside the bowl. The hand silhouettes remain readable at the mounted size. Turning on the faucet and moving into contact are not yet acted.'),
 'rub_palm':(4.5,'Palm02 reads as a near hand washing across a far cupped palm; bounded foam makes actual contact clearer than the rejected same-direction clasp. Fingers are partially occluded by lather. This is one contact pose, with no visible repeated rubbing stroke.'),
 'rub_back':(4.5,'The far hand turns over and the near palm contacts its back above the basin. The two connected forearms and reduced foam keep the task readable. The switch from the palm pose is abrupt and the head keeps the same forward gaze.'),
 'rinse':(4.5,'Water runs from spout through the joined hand area into the basin. The reduced lather includes a residual wrist bubble, so this can represent an intermediate rinse. It stays frozen until the clean pose; foam removal, wrist turning and tap closure need acting.'),
 'clean':(4.6,'Two separated foam-free palms, rounded five-digit silhouettes, an off faucet and restrained authored twinkles make the earned result readable. The unrelated boxing puff is absent. The lift from rinsing to displayed palms is an abrupt pose change and does not receive this still score as a movement score.')}
opinions=[]
for n,state in enumerate(states):
 score,note=states[state]
 evidence=[x for x in index['native_details'] if x['state']==state]
 opinions.append(dict(id='NUR-WASH-STATE-'+state.upper().replace('_','-'),name='Mounted '+state.replace('_',' '),lane='individual mounted state',score=score,artwork_score=score,priority=score<=4.5,evaluation=note,refinement='Preserve this static draft; refine the complete washing action and attention before final acceptance.',evidence=evidence))
more=[
 ('NUR-WASH-USE-BASIN','Basin, faucet and pedestal',4.6,'Painted cream, aqua and lavender forms have coherent authored outline/value bands. The spout, rim and hand contact stay at the same work area through all six selected states. Stable rendered scale and unobscured cavity meet the material draft bar; floor support and the room mount remain separately weak.','Reuse the painted basin identity; repair surrounding stage support without creating a duplicate prop.'),
 ('NUR-WASH-USE-HANDS','Hand contact across wash states',4.5,'Body-connected hands now contact water, the opposite palm and the hand back. The broad clean silhouettes remain legible at both aspects. Foam occludes fine tips during rubbing; meaningful rubbing and turning between contacts are still absent.','Add purposefully authored rubbing, wrist-turn and rinse/clean lift poses while keeping exact contact and body identity.'),
 ('NUR-WASH-USE-CONSEQUENCE','Earned clean consequence',4.6,'Clean palms appear only after held progress is earned, with the faucet off and no foam. The earlier chest-level boxing puff is absent in all six current clean captures and consecutive completion boards. The source twinkles are restrained.','Keep the unobstructed result and add a readable rinse-to-clean lift with attention returning to the child.'),
 ('NUR-WASH-USE-ACTION','Complete meaningful washing action',3.9,'All ordered frames show the correct wet, palm, back, rinse and clean order, plus a stable pause/resume hold. Six held paintings explain the contacts but do not show repeated scrubbing, tap operation or gradual foam removal. Abrupt hand jumps and an unchanged gaze prevent a complete action pass.','Author small connected strokes, deliberate wrist turns, tap operations and rinse-to-clean acting. Review a comparable movement study and recapture the real held route; do not raise the score from still quality.'),
 ('NUR-WASH-USE-ATTENTION','Attention and hand-change continuity',3.8,'The face remains almost identically forward-facing while the arms change. Ready-to-wet, cupped-palm-to-back and rinse-to-clean contacts change in one pose step. The eyes do not inspect hands or the faucet, and the clean lift has no anticipation.','Give Roshan a short attention-to-hands beat, contact-preserving hand changes and a gentle return gaze at the earned result.'),
 ('NUR-WASH-USE-ROOM','Whole mounted room and work focus',2.9,'The work itself is crisp and oversized, but the central detailed room plate is surrounded by blurred vertical copies, broad aqua bands and visible rectangular seams. The pedestal has no clear floor/contact support and the small caretaker is stranded in the blurred side area. Wide capture adds plain navy side regions. The source/material scores do not establish this composition.','Repair the room layering, focus grounding and caretaker placement using approved room sources with native per-screen coverage; preserve the background authority and avoid decorative overdraw.'),
 ('NUR-WASH-USE-TRANSITION','Entrance, completion and next-task presentation',4.0,'The route actor approaches the socket and yields to one complete work painting; no duplicated Roshan remains while washing. The normal small actor returns and the catch hint arms after earned clean hands. The large work portrait appearing and abruptly shrinking back into the room still needs a designed transition. Actual Back works in the recorded partial career; full-career earned return is outside this capture.','Refine the attention and settle transition without moving progress or reward ownership into animation; capture the whole career return separately.')]
for ident,name,score,note,refine in more:
 opinions.append(dict(id=ident,name=name,lane='mounted use' if ident not in ['NUR-WASH-USE-ACTION','NUR-WASH-USE-ATTENTION','NUR-WASH-USE-TRANSITION'] else 'complete action / continuity',score=score,artwork_score=None,priority=score<=4.5,evaluation=note,refinement=refine,evidence_index='current_visual_v3/INDEX.json'))
review=dict(schema='reef.nursery-connected-wash-current-review.v1',status='REVIEWED_STATIC_FLOOR_ACTION_AND_ROOM_REMAIN_WEAK',reviewed_utc=now,reviewer='Root direct visual drafting review; owner approval unassigned',source_boundary='SOURCE_CURRENT_MACHINE_V3.json',source_count=len(boundary['source_files']),source_boundary_unchanged=True,
 method='Directly inspected every one of 36 ordered QA boards covering all 1631 consecutive captured v3 frames, and all 36 unchanged full native state details. Thumbnail boards establish order, holds, subject visibility and presentation changes; fine hand/material judgement uses native details. No automated visual grading, interpolated frames or physical-device timing claim.',
 cases=index['cases'],boards=index['boards'],native_details=index['native_details'],individual_items=opinions,
 summary={'selected_static_states':6,'static_floor':4.5,'weak_preserved_clasp':4.4,'complete_action':3.9,'attention_continuity':3.8,'whole_room':2.9,'inclusive_priority_count':sum(x['priority'] for x in opinions)},
 route_qualification='Four direct training/authored catalog room fixtures and two real Bubble Bath card/caller partial-career routes. Nursery is absent from the live birthday roster. Earned first wash phase, pause/resume and normal Back are covered; no complete-career callback/reward, phone, child or owner acceptance.',
 machine_qualification='Current unmodified full suite is still running. This visual review cannot inherit earlier checkpoint CI or establish strict zero-debt satisfaction.',owner_approval=False,device_acceptance=False,child_acceptance=False)
assert not (F/'DIRECT_REVIEW_CURRENT_V3.json').exists()
write(F/'DIRECT_REVIEW_CURRENT_V3.json',review)
index['status']=review['status'];index['direct_review']='audit/job_nursery_wash_connected_v1_20261002/DIRECT_REVIEW_CURRENT_V3.json';write(F/'current_visual_v3/INDEX.json',index)
mapping={'ready_attempt01':'ready','wet_attempt01':'wet','rub_attempt01':'rub_palm','rub_back_attempt01':'rub_back','rinse_attempt01':'rinse','clean_attempt01':'clean','rub_palm_attempt02':'rub_palm02'}
for folder,stem in mapping.items():
 p=S/folder/'SOURCE_REVIEW.json';d=read(p);native=S/folder/'native.png';runtime=R/'assets/opera/worlds/nursery/wash_connected_v1_20261002'/(stem+'.png')
 with Image.open(native) as im: assert list(im.size)==d['native']['size']==[1254,1254]
 with Image.open(runtime) as im: assert im.size==(1024,1024) and im.mode=='RGBA'
 if d.get('runtime_normalization') is None:
  d['runtime_normalization']={'path':runtime.relative_to(R).as_posix(),'sha256':sha(runtime),'size':[1024,1024],'method':'Godot4.7.2 Image.resize, uniform whole-canvas 1254-square to1024-square INTERPOLATE_LANCZOS; no isolated subject/pixel repair. Native original preserved.','runtime_selected':folder!='rub_attempt01'}
 d['current_mounted_review']='audit/job_nursery_wash_connected_v1_20261002/DIRECT_REVIEW_CURRENT_V3.json' if folder!='rub_attempt01' else None
 d['current_mounted_static_score']=states['rub_palm' if stem=='rub_palm02' else stem][0] if folder!='rub_attempt01' else None
 d['complete_action_score']=3.9 if folder!='rub_attempt01' else None
 write(p,d)
table='<section id="scores"><h2>Individual current opinions</h2><p>Six selected stills meet the provisional 4.5 floor. The complete action remains 3.9 and room composition 2.9. All scores of 4.5 or lower remain priorities; device, child and owner review are outstanding.</p><table><thead><tr><th>Item</th><th>Score</th><th>Evaluation and next refinement</th></tr></thead><tbody>'
for o in opinions:
 table+='<tr id="'+o['id']+'"><td>'+html.escape(o['name'])+'</td><td>'+str(o['score'])+'/5</td><td>'+html.escape(o['evaluation'])+'<p>'+html.escape(o['refinement'])+'</p></td></tr>'
table+='</tbody></table><p><a href="DIRECT_REVIEW_CURRENT_V3.json">Complete written opinions, exact evidence hashes and scope</a></p></section>'
p=F/'index.html';s=p.read_text();s=s.replace('Direct current sequence scores are still pending.','Current direct review: static states 4.5–4.6, complete washing action 3.9, attention continuity 3.8, room 2.9.')
s=s.replace('<section><h2>Every current state in context</h2>',table+'<section><h2>Every current state in context</h2>')
s=s.replace('direct individual and sequence review pending.','directly inspected at native size; static and action opinions are separated in the table above.')
p.write_text(s,encoding='utf-8')
p=S/'index.html';s=p.read_text().replace('native1280 square originals','native 1254-square originals').replace('uniform1024 POT','uniform 1024 POT');p.write_text(s,encoding='utf-8')
p=F/'MOVEMENT_PROFILE_AND_CLIP_CONTRACT_V1.json';d=read(p);d['camera_and_pivot']=d['camera_and_pivot'].replace('normalized1280 to1024','normalized 1254 to1024');d['current_action_review']='DIRECT_REVIEW_CURRENT_V3.json';d['current_action_score']=3.9;write(p,d)
write(F/'NATIVE_DIMENSION_CLARIFICATION.json',{'native_dimensions':[1254,1254],'runtime_dimensions':[1024,1024],'method':'Source metadata and actual preserved PNG dimensions are authoritative. Earlier summary/gallery prose described intended1280 rather than observed1254; current prose corrected. Uniform whole-canvas runtime normalization preserves native originals.','sources':[{ 'path':(S/k/'native.png').relative_to(R).as_posix(),'sha256':sha(S/k/'native.png')} for k in mapping]})
for name in ['prepare_nursery_review_pages_v358.py',Path(__file__).name]:shutil.copyfile(Path(__file__).parent/name,F/'review_tools'/name)
p=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';d=read(p);d['files']=sorted(set(d['files'])|{p.relative_to(R).as_posix() for base in [F,S] for p in base.rglob('*') if p.is_file()});write(p,d)
print('Direct Nursery current v3: 36 boards / 1631 consecutive frames / 36 native details / 13 opinions; static floor4.5, complete action3.9, room2.9. Source dimension clarification1254 recorded.')
