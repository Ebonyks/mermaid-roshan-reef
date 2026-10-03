from pathlib import Path
import json,hashlib,shutil,datetime
from PIL import Image
B=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');N=B/'assets_src/imagegen/candy_wrap_contact_v1_20261003';A=N/'attempt03';A.mkdir(exist_ok=True)
src=Path(r'C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-5279c211-52a1-48f2-b8a8-26df18734aad.png');shutil.copyfile(src,A/'native.png');im=Image.open(src);w,h=im.size
regions=[]
for i in range(4):
 x=(i%2)*(w//2);y=(i//2)*(h//2);mask=im.getchannel('A').crop((x,y,x+w//2,y+h//2)).point(lambda a:255 if a>=128 else 0);regions.append({'index':i,'region':[x,y,w//2,h//2],'alpha128_bounds':mask.getbbox()})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
meta={'method':'builtin_imagegen_targeted_contact_edit','sha256':sha(src),'native_path':str((A/'native.png').relative_to(B)).replace('\\','/'),'dimensions':[w,h],'mode':im.mode,'alpha_extrema':im.getchannel('A').getextrema(),'regions':regions,'prompt_sha256':sha(N/'PROMPT_A3.txt'),'reference_path':str((N/'attempt02/native.png').relative_to(B)).replace('\\','/'),'reference_sha256':sha(N/'attempt02/native.png'),'native_preserved':True,'runtime_bound':False,'runtime_ready':False,'status':'STATIC_POSE_CONTACT_PROVISIONAL_RUNTIME_ACTION_UNREVIEWED','owner_acceptance':None}
(A/'SOURCE.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
review={'direct_native_review':True,'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'Codex visual drafting review','source_sha256':meta['sha256'],'opinions':[{'item':'identity/costume/painted material','score':4.5,'evaluation':'Child identity/costume and coral quilted two mittens conserved, broad painted gold paper agrees with commissioned wrapper. Two continuously connected arms, no whisk.'},{'item':'open paper contact','score':4.5,'evaluation':'Two mittens grasp the long edges, one exposed coral sweet supported on the same sheet.'},{'item':'long edge folding contact','score':4.5,'evaluation':'Both mittens press attached long flaps over belly; material fold is explicit.'},{'item':'pinch-neck contact','score':4.5,'evaluation':'Thumb lobes oppose palms at both narrow necks; paper fans extend freely outside grips.'},{'item':'opposite wrist-roll static meaning','score':4.5,'evaluation':'Final left thumb rolls upward, right mitten rotates to a distinct downward grasp. Neck pinches remain connected to paper, unlike A1 fan grasps/A2 repeated neutral wrists. This score covers visible endpoint meaning, not motion.'},{'item':'fixed cell sequence continuity','score':4.2,'evaluation':'Four source keys still differ in candy center, face and table placement. Not chronological in-betweens. Exact runtime sampling and transitions need independent review; no whole-action pass or interpolation to hide missing motion.'}],'whole_action_score':None,'device_acceptance':None,'child_acceptance':None,'owner_acceptance':None,'runtime_bound':False}
(A/'DIRECT_REVIEW.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
D=B/'audit/job_candy_wrap_contact_runtime_v1_20261003';D.mkdir(exist_ok=True);(D/'.gdignore').write_text('',encoding='utf-8');(D/'review_tools').mkdir(exist_ok=True)
source='''extends "res://scripts/opera_gesture_surface.gd"
## NON_RUNTIME_WRAPPER_CONTACT_STUDY. Native complete source keys; no interpolation,
## pixel repairs, runtime asset binding or claim of temporal in-betweens.
const CONTACT_NATIVE := "res://assets_src/imagegen/candy_wrap_contact_v1_20261003/attempt03/native.png"
var contact_texture: Texture2D
var last_source_region := Rect2()
var last_source_key := -1
var last_draw_rect := Rect2()

func _draw_candymaker_crank(progress: float) -> void:
	if contact_texture == null:
		var image := Image.new()
		assert(image.load(CONTACT_NATIVE) == OK)
		assert(image.get_size() == Vector2i(1254, 1254))
		contact_texture = ImageTexture.create_from_image(image)
	var key := 0 if progress < 0.22 else (1 if progress < 0.54 else (2 if progress < 0.82 else 3))
	var side := minf(size.x, size.y) * 0.96
	var target := Rect2(size * 0.5 - Vector2.ONE * side * 0.5, Vector2.ONE * side)
	var source := Rect2(Vector2(float(key % 2) * 627.0, float(key / 2) * 627.0), Vector2(627, 627))
	assert(source.position.x >= 0 and source.position.y >= 0 and source.end.x <= 1254 and source.end.y <= 1254)
	last_source_key = key
	last_source_region = source
	last_draw_rect = target
	draw_texture_rect_region(contact_texture, target, source)
'''
source=source.replace('float(key / 2)', 'float(key >> 1)')
(D/'contact_surface.gd').write_text(source,encoding='utf-8',newline='\n')
C=B/'audit/job_candy_workflow_current_v1_20261003';capture=(C/'capture.gd').read_text(encoding='utf-8')
capture=capture.replace('res://audit/job_candy_workflow_current_v1_20261003/attempt03/','res://audit/job_candy_wrap_contact_runtime_v1_20261003/attempt01/')
capture=capture.replace('## Review only. Actual Kitchen card, inherited input and earned phases/return.','## NON_RUNTIME_CONTACT_COUNTERFACTUAL. Surface drawing and phase2 actor visibility only.\n## Actual Kitchen card, inherited input/progress and earned phases/return.')
capture=capture.replace('"actor_position":world.player_actor.position,','"source_key":s.get("last_source_key"),"source_region":s.get("last_source_region"),"draw_rect":s.get("last_draw_rect"),"actor_visible":world.player_actor.visible,\n\t\t"actor_position":world.player_actor.position,')
capture=capture.replace('await _wait(8)\n\tawait _view("phase%d_task_open" % world.phase_index)','if world.phase_index==2:\n\t\tworld.player_actor.visible=false\n\tawait _wait(8)\n\tawait _view("phase%d_task_open" % world.phase_index)')
insertion='''
	# Explicit drawing-only surface substitution. Copy all inherited script state,
	# transforms and actual signal callables; validate snapshot before opening.
	var original := world.surface as OperaGestureSurface
	var replacement := (load("res://audit/job_candy_wrap_contact_runtime_v1_20261003/contact_surface.gd") as GDScript).new() as OperaGestureSurface
	var parent := original.get_parent()
	parent.add_child(replacement)
	parent.move_child(replacement,original.get_index())
	var snapshot := original.progress_snapshot()
	for property: Dictionary in original.get_property_list():
		if int(property.get("usage",0)) & PROPERTY_USAGE_SCRIPT_VARIABLE:
			var value: Variant = original.get(property["name"])
			if value is Array or value is Dictionary:
				value=value.duplicate(true)
			replacement.set(property["name"],value)
	for key: String in ["position","size","visible","mouse_filter","texture_filter","process_mode","modulate"]:
		replacement.set(key,original.get(key))
	for signal_name: String in ["gesture","progress_changed"]:
		for connection: Dictionary in original.get_signal_connection_list(signal_name):
			replacement.connect(signal_name,connection["callable"],int(connection["flags"]))
		assert(replacement.get_signal_connection_list(signal_name).size()==original.get_signal_connection_list(signal_name).size())
	world.surface=replacement
	assert(replacement.progress_snapshot()==snapshot)
	assert(replacement.get_global_transform_with_canvas()==original.get_global_transform_with_canvas())
	original.queue_free()
	await _wait(4)
	events.append({"event":"EXPLICIT_NON_RUNTIME_DRAWING_ONLY_CONTACT_SURFACE_SUBSTITUTION","source":FileAccess.get_sha256("res://assets_src/imagegen/candy_wrap_contact_v1_20261003/attempt03/native.png"),"snapshot_unchanged":replacement.progress_snapshot()==snapshot,"original_input_pivot_retained":true,"production_binding":false})
'''
capture=capture.replace('\tfor phase: int in range(world.phases.size()):',insertion+'\tfor phase: int in range(world.phases.size()):')
capture=capture.replace('assert(world.phase_index==phase)\n\t\tvar full_action', 'assert(world.phase_index==phase)\n\t\tworld.player_actor.visible=true\n\t\tvar full_action')
capture=capture.replace('Current unmodified production Kitchen picture-card route, actual finger0 input, all career phases earned and normal Kitchen return.','Explicit NON_RUNTIME contact source-key drawing substitute and phase2 room actor hidden to avoid duplicate Roshan. Four static authored keys, not temporal in-betweens. Original circle pivot and input intentionally retained to expose any visual/input mismatch. Actual production Kitchen picture-card route, finger0 input, all career phases earned and normal Kitchen return.')
capture=capture.replace('No surface replacement, phase forcing, manual ticks, signal completion or patched callbacks.','Explicit declared surface replacement; no phase forcing, manual ticks, signal completion or patched callbacks.')
(D/'capture.gd').write_text(capture,encoding='utf-8',newline='\n')
contract={'id':'CANDY_WRAP_CONTACT_A3_STUDY_V1','lane':'interactive gameplay non-runtime counterfactual','baseline':'c5977ebb29bb2011b20fc149ad350290f045045c','movement_profile':'design/animation/ROSHAN_MOVEMENT_LANGUAGE.md','intent':'Roshan concentrates on one supported sweet, folds its golden paper, pinches both attached necks, counter-rolls the ends and inspects the result.','register':'Ribbon Glide quiet useful work','scene':'Actual Kitchen career act3, training current four phases; story GLAZE is a different berry action and must not bind wrapping artwork.','sources':[meta], 'entry':'Actual picture card/approach/arrival, original full-tail room actor and saved state; substitute only source rendering; hide room actor at phase2 task-open because connected close-up owns Roshan.','exit':'Original room actor restored at following phase; ordinary input-earned completion and Kitchen callback; no new rewards or save keys.','geometry':{'unit':'logical surface pixels on1280x720, same416x292 normal activity dock','atlas_cell':[627,627],'draw_side':'0.96*min(surface.size.x,surface.size.y)','draw_pivot':'surface.size*0.5','source_keys':['open','fold','pinch','counter_roll'],'candy_anchors_unresolved':'Raw fixed-cell sampler deliberately exposes native center/table drift; no per-key subject pixel manipulation.','original_circle_pivot':'Inherited _crank_action_rect().get_center; fixed. Any mismatch blocks quality acceptance.'},'timeline':{'phase_goal':1.8,'progress_key_boundaries':[0,0.22,0.54,0.82],'policy':'Key selection from true inherited widget_fill. No timer advancement, looping, blending or claim that four pose keys cover continuous motion.'},'translation':'Original navigation/approach owner; cosmetic study only, no actor crossing furniture.','events':'Inherited finger0 circular gesture→world progress→earned callback owns awards, at most once. Source key reaching3 grants nothing.','interruptions':'Inherited touch ownership/release/pause/back/teardown; no new delayed jobs. Explicit runtime interruption/re-entry tests pending, no acceptance claim.','readability':'Actual1280/1600 native full canvases plus original details required; no enlarged capture can pass the small dock on its own.','verification':'Parser/inference/official4.7.2analyzer, full inherited circle sequence both widths and all4 earned return, exact source/region assertions, direct full-frame review; device/child/owner remain separate.','predicted_score':None,'owner_acceptance':None}
(D/'CLIP_CONTRACT_V1.json').write_text(json.dumps(contract,indent=2)+'\n',encoding='utf-8')
I=B/'design/audit_impacts/job-candy-workflow-current-20261003.json';impact=json.loads(I.read_text());impact['scope']+=' Non-runtime contact counterfactual copies inherited surface state/signals, replaces only drawing and hides room Roshan during WRAP to avoid duplication. Raw fixed-cell source intentionally exposes continuity and original finger-pivot mismatch; no input geometry change or production art binding.';impact['files']=sorted(set(impact['files']+[str(p.relative_to(B)).replace('\\','/') for folder in [D,N] for p in folder.rglob('*') if p.is_file()]));impact['acceptance_gaps']='Fresh Candy route repair machine verified; current/source action reviews in progress. Contact A1/A2 failures preserved; A3 native static contact4.5 but fixed-key continuity4.2, whole runtime action unreviewed. No device/child/owner/all-job acceptance, finding closure, integration or release.';I.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8');shutil.copyfile(Path(__file__),D/'review_tools'/Path(__file__).name)
print(json.dumps({'source_a3':meta['sha256'],'study':str(D),'static_contact':4.5,'fixed_source_continuity':4.2,'whole_action':None}))
