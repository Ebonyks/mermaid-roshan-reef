from pathlib import Path
import datetime,hashlib,json,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
A=P/'attempt01'
S=R/'assets_src/imagegen/nursery_palm_attention_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
index=read(A/'INDEX.json')
assert len(index['frames'])==41 and all(sha(R/x['path'])==x['sha256'] for x in index['frames'])
review={'status':'REJECTED_REFERENCE_ACTION_BELOW_FLOOR','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'Root direct visual drafting review','method':'Directly inspected both corrected complete-canvas QA boards and each of all41 unchanged decoded native896x512 frames at original resolution. No automated aesthetic grade.','evidence':index['frames'],'overall_reference_action_score':3.6,'individual_items':[
 {'id':'NUR-MOTION-A1-IDENTITY','score':4.4,'evaluation':'Nursery costume, joined torso/tail and painted palette remain recognizable, but patterned scales, hair edge and fine outlines crawl between frames. This does not match static-source clarity.'},
 {'id':'NUR-MOTION-A1-PALM-CONTACT','score':3.8,'evaluation':'Both wrists remain body-connected. The far cupped palm and near hand change toward a shared clasp; there are brief visible gaps/blur at the finger contact. The requested near-palm slide across a fixed opposite palm is not consistently readable.'},
 {'id':'NUR-MOTION-A1-RUB-ACTION','score':3.6,'evaluation':'Hands lift and gather into one clasp-like arc, then largely hold. Two distinct reciprocal rubbing strokes are not shown. A foam/water-like trail extends horizontally toward the off faucet in early/middle frames rather than staying solely at palm contact.'},
 {'id':'NUR-MOTION-A1-ATTENTION','score':3.1,'evaluation':'The head tilts slightly but the eyes remain largely forward-facing; the character does not establish a deliberate look at the washing hands.'},
 {'id':'NUR-MOTION-A1-FIXTURES','score':3.9,'evaluation':'Basin, lip, pedestal and faucet remain identifiable but have small contour and gold-highlight changes; incidental motion marks spread toward the faucet despite the off-faucet constraint.'},
 {'id':'NUR-MOTION-A1-ENTRY-EXIT','score':3.6,'evaluation':'The final hands remain gathered higher than the original palm-up contact. No unchanged resting-pose return or approved seamless loop is established.'}],
 'native_render_pass':True,'runtime_integration':False,'cinematic_delivery':False,'owner_acceptance':None,'current_game_action_score_unchanged':3.9,
 'next_refinement':'Author the missing look-to-hands pose from the preserved palm02 source, then test one simple short contact-preserving rubbing phrase. Keep existing current game binding untouched until a fresh contextual action review. Preserve this failed motion study.'}
assert not (A/'DIRECT_REVIEW.json').exists();write(A/'DIRECT_REVIEW.json',review)
index['status']=review['status'];index['direct_review']='assets_src/local_motion/nursery_connected_scrub_v1_20261002/attempt01/DIRECT_REVIEW.json';write(A/'INDEX.json',index)
p=P/'index.html';s=p.read_text();s=s.replace('Current render and frame review pending. All failed attempts will remain available.','First native render passes machine execution but fails the action floor: reference action 3.6, contact 3.8, attention 3.1. Every one of 41 native frames directly inspected. The failed study is preserved; current gameplay action 3.9 is unchanged.')
s=s.replace('</article>','<p><a href="attempt01/DIRECT_REVIEW.json">Every individual motion evaluation</a> · <a href="attempt01/INDEX.json">All native frames and exact hashes</a></p><video controls preload="metadata" src="'+next(Path(x['path']).name for x in index['outputs'] if x['path'].endswith('.mp4'))+'"></video></article>')
# Video URL remains relative to its preserved attempt, never external machine paths.
video=next(Path(x['path']).name for x in index['outputs'] if x['path'].endswith('.mp4'))
s=s.replace('src="'+video+'"','src="attempt01/'+video+'"')
p.write_text(s,encoding='utf-8',newline='\n')
p=F/'index.html';s=p.read_text();s=s.replace('Motion reference only; every native frame still needs review. Current gameplay action 3.9 and attention 3.8 are unchanged.','All 41 native frames reviewed: first reference action 3.6 and attention 3.1 fail the floor. Motion reference only; preserve the failed study. Current gameplay action 3.9 and attention 3.8 are unchanged.')
# Move the new section inside the existing report main, before its scripts.
start=s.index('<section id="motion-study">');end=s.index('</section>',start)+len('</section>');section=s[start:end];s=s[:start]+s[end:];s=s.replace('<script>',section+'<script>',1)
p.write_text(s,encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip)
imp['scope']+=' The local Nursery motion A1 fails action3.6/contact3.8/attention3.1 after direct inspection of all41 native frames. Generate one targeted connected palm-wash attention pose to address the explicit missing eyes-to-hands source gap, preserving the complete body/costume/tail/basin and all previous candidates. Unbound imagegen source only; no current game/static/motion score transfer.'
for v in imp['validation']:
    if v['command']=='Connected Nursery ComfyUI scrubbing reference study v1':v.update(result='FAIL',evidence='assets_src/local_motion/nursery_connected_scrub_v1_20261002/attempt01/DIRECT_REVIEW.json; machine render passes, all41 native frames inspected, action3.6 and attention3.1 rejected.')
write(ip,imp)
assert not S.exists();S.mkdir();(S/'.gdignore').write_text('',encoding='utf-8')
ref='assets_src/imagegen/nursery_wash_connected_v1_20261002/rub_palm_attempt02/native.png'
prompt='''Use case: precise-object-edit. IMAGE_1 is the full connected Nursery Roshan palm-wash pose and is the sole identity, painted style, costume, body, tail, prop, canvas and layout authority. Generate ONE complete transparent next working pose. Change only her attention: gently lower both eyes to the touching palms, with a small natural head inclination toward her hands. Her eye line must visibly target the actual hand contact, not face the viewer. Preserve her childlike face identity, brown eyes, warm quiet smile, hair volume, rainbow ribbon, flower, aqua Nursery apron, lilac gingham sleeves, crescent pocket, complete rainbow tail and every basin/faucet/pedestal contour and position. Keep the near palm flat against the far cupped palm at exactly the current washing contact, both wrists joined to their own forearms and body. Preserve the small bounded soap lather only between the palms, faucet OFF, no water bridge or motion marks. Same rounded painted 2D storybook broad shade bands and purple contours; no lifelike skin, vector, 3D, background, labels, new prop, extra hand or limb. Exact square composition and complete freshly generated RGBA cutout with true transparent alpha. This is an attentive washing source pose, not a new character design.'''
write(S/'PROMPT.json',{'prompt':prompt,'method':'built-in imagegen','transparent_background':True,'references':[ref],'reference_sha256':sha(R/ref),'attempt':1,'role':'Unbound attentive contact pose; source/material/mounted/motion acceptance unassigned.'})
write(S/'PLAN.json',{'status':'TARGETED_ATTENTION_SOURCE_GENERATION_PENDING','baseline':imp['baseline'],'inventory':[{'path':ref,'sha256':sha(R/ref),'reuse_gap':'Preserved source is forward-facing; failed local motion does not establish eyes-to-hands attention. Reuse entire identity/layout; target only attention.'}],'rules':imp['rules'],'findings':imp['findings'],'source_opinion':None,'runtime_integration':False,'owner_acceptance':None})
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for base in [F,P,S] for p in base.rglob('*') if p.is_file()});write(ip,imp)
print('Motion A1 rejected3.6 with all41 native frames directly reviewed. One targeted attention-source prompt recorded before generation.')
