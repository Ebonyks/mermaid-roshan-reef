from pathlib import Path
import datetime,hashlib,json,shutil
from PIL import Image
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
N=B/'assets_src/imagegen/candy_neck_grip_pose_v1_20261003'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):
 t=p.with_name(p.name+'.v607_next');t.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());t.replace(p)
src=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-797e2541-e9d4-4060-a879-b28e661e5724.png')
dst=N/'attempt02/native.png';assert not dst.exists();shutil.copyfile(src,dst)
with Image.open(dst) as im:dims=list(im.size);mode=im.mode
plan=read(N/'PLAN.json');prompt_path=N/'attempt02/SENT_PROMPT.txt'
write(N/'attempt02/SOURCE.json',dict(method='built_in_imagegen_precise_object_edit',native_path=dst.relative_to(B).as_posix(),native_sha256=sha(dst.read_bytes()),native_dimensions=dims,native_mode=mode,default_generated_original=str(src),prompt_path=prompt_path.relative_to(B).as_posix(),prompt_sha256=sha(prompt_path.read_bytes()),references=plan['references'],copied_without_pixel_changes=True,recorded_utc=now(),runtime_bound=False))
reviews=[
('exactly_two_owned_mittens',4.6,'Two coral quilted mittens remain continuously attached to their original teal cuffs and cream sleeves; both thumb lobes are distinct.'),
('left_neck_contact',4.5,'The short left gold neck is clearly compressed between thumb above and palm below, immediately beside the oval body. The outer fan extends beyond the grip.'),
('right_neck_contact',4.5,'The original right mitten thumb and palm visibly oppose across the short right gold neck; the fan extends outward and the sweet stays supported.'),
('pre_twist_semantics',4.2,'Closed rings are gone, but diagonal overlapping folds, especially at the right neck, already suggest a rolled twist. A honest pre-twist gather still needs straighter open longitudinal pleats.'),
('single_continuous_gold_wrapper',4.5,'One opaque gold body with two connected short necks and two free fans remains legible. No extra mat or tied component.'),
('opaque_supported_small_oval',4.5,'One low covered oval remains at the same lavender table centre; no exposed red or extra sweet.'),
('outward_fan_ownership',4.5,'Both loose fans remain visible outside the mitten pinches, with natural connected folds and dark contours.'),
('character_table_registration',4.5,'Original full scene and character identity remain coherent. Wrists have changed purposefully within the same sleeve attachments.'),
('painted_gold_material',4.5,'Gold crinkles, broad painted highlights and plum outlines match the wrapper reference; no vector or realistic replacement.'),
('inherited_room_graphics',4.4,'Inherited detailed backdrop remains a separate weak source priority. No current runtime-room opinion.'),
('whole_pre_twist_pose',4.2,'Both contacts now meet the static drafting floor, but premature twist cues leave this intermediate pose below it.')]
write(N/'attempt02/DIRECT_REVIEW.json',dict(reviewed_utc=now(),review_method='direct_complete_native_original_imagegen_output',native_sha256=sha(dst.read_bytes()),status='CONTACTS_AT_FLOOR_PRETWIST_STAGE_REJECTED_DIAGONAL_FOLDS',components=[dict(id=k,score=s,evaluation=v) for k,s,v in reviews],source_pose_score=4.2,motion_score=None,current_game_wrap_score=2.8,runtime_bound=False,owner_acceptance=None,required_revision='Change only neck pleats to straight parallel open longitudinal folds, preserving both achieved contacts.'))
prompt="Use case: precise-object-edit\nImage 1 is the complete painted Candy Maker scene and edit target. Make a very small local correction to the GOLD PAPER NECKS BETWEEN ROSHAN'S MITTEN THUMBS AND PALMS. Preserve the entire landscape, her exact identity, all costume/background/table details, the original two attached coral mitten poses and readable thumb/palm pinches, the small supported gold oval belly, and the two loose outer fans.\nThe hands are GATHERING UNTWISTED PAPER. Redraw each short neck as straight, open accordion pleats running horizontally LENGTHWISE from oval body to loose fan through the mitten's pinch. Show several narrow straight parallel gold folds at each pinch: they converge inward to the mitten contact but do NOT cross, wind diagonally around the neck, spiral, braid, roll closed or become a ring. The near/front pleat lies visibly between the thumb above and palm below; the far pleats remain attached behind it. Both fans are loose and unsealed. Remove only the current diagonal overlapping gold folds at the necks that make them appear already twisted. No collar, band, tie, knot, string, closed ring or finished twist. The two sleeve-connected mittens keep grasping immediately beside the same oval; no extra hand/finger or fan-top substitution. Keep the broad satin gold value bands and restrained painted crinkles. Keep one continuous gold wrapper completely covering the same sweet on the same lavender table. No separate gold sheet, no exposed red, no candy or scene enlargement, no camera change, no photorealism, no flat vector, no text. Return the whole complete painting; one pre-twist grip pose, not an animation."
(N/'attempt03').mkdir();(N/'attempt03/SENT_PROMPT.txt').write_bytes(prompt.encode())
ref=dict(path=dst.relative_to(B).as_posix(),sha256=sha(dst.read_bytes()),role='edit_target_same_scene_achieved_owned_grips_with_failed_pretwist_neck_pleats')
write(N/'attempt03/PLAN.json',dict(status='TARGETED_OPEN_PARALLEL_NECK_PLEAT_CORRECTION_PLANNED',named_defect='A2 diagonal overlapping neck folds imply early twist',prompt_sha256=sha(prompt.encode()),references=[ref],runtime_bound=False))
plan['status']='ATTEMPT02_CONTACTS4_5_STAGE4_2_ATTEMPT03_LOCAL_PLEAT_CORRECTION_PLANNED';plan['attempts'].append(dict(attempt=2,source_pose_score=4.2,status='REJECTED_PRETWIST_STAGE',review='attempt02/DIRECT_REVIEW.json'));write(N/'PLAN.json',plan)
shutil.copyfile(__file__,N/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-neck-grip-pose-20261003.json';impact=read(ip);impact['files']=sorted(set(impact['files'])|{p.relative_to(B).as_posix() for p in N.rglob('*') if p.is_file()});impact['validation'][1]=dict(command='Native neck-grip generation and individual direct review',result='FAIL',evidence='assets_src/imagegen/candy_neck_grip_pose_v1_20261003/attempt02/DIRECT_REVIEW.json;both contacts4.5 but pre-twist/source pose4.2. A1 3.2 preserved; A3 local pleat correction planned.');write(ip,impact)
print('A2_PRESERVED_CONTACTS4_5_STAGE4_2',sha(dst.read_bytes()),'A3_PROMPT',sha(prompt.encode()),flush=True)
