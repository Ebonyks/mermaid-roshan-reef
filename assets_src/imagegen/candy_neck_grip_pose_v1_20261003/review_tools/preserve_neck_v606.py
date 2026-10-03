from pathlib import Path
import datetime,hashlib,json,shutil
from PIL import Image
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
N=B/'assets_src/imagegen/candy_neck_grip_pose_v1_20261003'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):
 t=p.with_name(p.name+'.v606_next');t.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());t.replace(p)
src=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-0904e499-56cb-4e6c-a98c-f82c60af97a4.png')
dst=N/'attempt01/native.png';assert not dst.exists();shutil.copyfile(src,dst)
with Image.open(dst) as im: dims=list(im.size);mode=im.mode
plan=read(N/'PLAN.json')
write(N/'attempt01/SOURCE.json',dict(method='built_in_imagegen_precise_object_edit',native_path=dst.relative_to(B).as_posix(),native_sha256=sha(dst.read_bytes()),native_dimensions=dims,native_mode=mode,default_generated_original=str(src),prompt_path=(N/'SENT_PROMPT.txt').relative_to(B).as_posix(),prompt_sha256=sha((N/'SENT_PROMPT.txt').read_bytes()),references=plan['references'],copied_without_pixel_changes=True,recorded_utc=now(),runtime_bound=False))
reviews=[
('exactly_two_owned_mittens',4.5,'Exactly two quilted coral mittens remain attached to the two teal cuffs and cream sleeves.'),
('left_neck_contact',3.2,'Left mitten rests broadly over the loose fan; its thumb does not visibly oppose its palm across the short neck.'),
('right_neck_contact',3.4,'Right thumb approaches the neck but the broad palm obscures the fan rather than displaying a two-sided neck pinch.'),
('pre_twist_semantics',2.7,'Both necks are already surrounded by closed gold rings/rolled collars. These supply an unearned completed seal before any twist.'),
('single_continuous_gold_wrapper',4.4,'The body and fans form a legible single wrapper, but the added circumferential rings read as separate tied components.'),
('opaque_supported_small_oval',4.5,'One low oval remains covered and rests at the same table centre with no red exposed; size is close to the reference.'),
('outward_fan_ownership',4.1,'Two gold fans extend outward, but both mitten palms hide their near folds and weaken grasp readability.'),
('character_table_registration',4.5,'Character, cuffs, factory and purple table remain recognizably stable in the full frame.'),
('painted_gold_material',4.5,'Gold retains broad highlights, crinkled bands and dark contours matching the contextual sheet.'),
('inherited_room_graphics',4.4,'Retained detailed machine backdrop remains a separate weak source priority; no new mounted-room opinion.'),
('whole_pre_twist_pose',3.2,'Rejected: the grip and unsealed stage are not demonstrated even though character/material continuity is useful.')]
write(N/'attempt01/DIRECT_REVIEW.json',dict(reviewed_utc=now(),review_method='direct_complete_native_original_imagegen_output',native_sha256=sha(dst.read_bytes()),status='REJECTED_PRETIED_NECK_RINGS_AND_FAN_TOP_CONTACT',components=[dict(id=k,score=s,evaluation=v) for k,s,v in reviews],source_pose_score=3.2,motion_score=None,current_game_wrap_score=2.8,runtime_bound=False,owner_acceptance=None,required_revision='Replace circumferential rings with open lengthwise pleats and show each short neck pinched between the original mitten thumb and palm.'))
prompt="Use case: precise-object-edit\nImage 1 is the complete existing Candy Maker painting and EDIT TARGET. Keep the whole scene, Roshan's exact identity/costume/coral quilted oven mittens, teal cuffs and attached cream sleeves, the lavender table, framing and painted satin-gold paper material. Edit only both forearm/mitten poses and the one sheet of gold paper around the SAME small low oval sweet at its original table centre and scale.\nShow the gathering stage BEFORE TWISTING. The covered small oval lies on the tabletop. One continuous gold sheet snugly covers it; no red shows and no separate flat sheet remains beneath it. A broad lengthwise seam is visible on the oval. On each side, loose open paper pleats taper directly from the oval into a short soft neck and then flare outward into a flat loose fan. The pleats run LENGTHWISE THROUGH EACH NECK from body to fan; absolutely no circumferential rings, cuffs, rolled collars, bands, ties, strings, knots, spirals or completed twists around either neck. These ends are not yet sealed.\nExactly TWO attached coral mitten hands gather the necks. Put the small existing THUMB lobe of each mitten ABOVE its corresponding short neck and its large PALM lobe BELOW/BEHIND that same neck, so the GOLD LENGTHWISE PLEATS are visibly trapped in the notch BETWEEN thumb and palm. The mittens pinch immediately beside the oval belly. The screen-left mitten pinches the LEFT neck; the screen-right mitten pinches the RIGHT neck. Each loose fan extends OUTWARD beyond the mitten and remains mostly unobscured. The mitten cannot merely rest on top of a fan or touch a finished collar. The existing wrists rotate naturally to create this two-sided grasp; every mitten remains visibly connected to its original cuff and sleeve. Keep both contact notches readable and the sweet supported on the same table. The tiny neck gathers are formed by pressure from the mittens, never by a separate tied ring. Preserve the sweet's small low oval shape and the restrained painted gold crinkles. No extra hands, fingers, arms, oversized candy, bag or new objects. Full landscape painting only, no text or diagram. No photorealism, vector art, crop or camera movement."
(N/'attempt02').mkdir();(N/'attempt02/SENT_PROMPT.txt').write_bytes(prompt.encode())
write(N/'attempt02/PLAN.json',dict(status='TARGETED_CONTACT_AND_UNTWISTED_PLEATS_REVISION_PLANNED',named_defect='A1 premature closed neck rings plus fan-top contacts',prompt_sha256=sha(prompt.encode()),references=plan['references'],reference_selection='Use the unchanged cover reference, not the defective pre-tied A1 pose.',runtime_bound=False))
plan['status']='ATTEMPT01_REJECTED_ATTEMPT02_TARGETED_REVISION_PLANNED';plan['attempts']=[dict(attempt=1,source_pose_score=3.2,status='REJECTED',review='attempt01/DIRECT_REVIEW.json')];write(N/'PLAN.json',plan)
shutil.copyfile(__file__,N/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-neck-grip-pose-20261003.json';impact=read(ip);impact['files']=sorted(p.relative_to(B).as_posix() for p in N.rglob('*') if p.is_file());impact['validation'][1]=dict(command='Fresh native neck-grip generation and individual direct review',result='FAIL',evidence=str((N/'attempt01/DIRECT_REVIEW.json').relative_to(B).as_posix())+';source pose3.2, premature closed rings and non-opposed contact. A2 planned.');write(ip,impact)
print('A1_PRESERVED_REJECTED',sha(dst.read_bytes()),dims,mode,'A2_PROMPT',sha(prompt.encode()),flush=True)
