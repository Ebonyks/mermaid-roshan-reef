from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
S=R/'assets_src/imagegen/nursery_wash_connected_v1_20261002'
assert json.loads((F/'baseline_capture/PROCESS_RECEIPT.json').read_text())['source_unchanged']
P=R/'scripts/opera_career_world_2d.gd'
original=P.read_text(encoding='utf-8')
(F/'career_world_baseline.gd.txt').write_text(original,encoding='utf-8')
text=original
changes=[('const NurseryCatch := preload("res://scripts/opera_nursery_catch.gd")','const NurseryCatch := preload("res://scripts/opera_nursery_catch.gd")\nconst NurserySurface := preload("res://scripts/opera_nursery_surface.gd")'),('if career_id in ["teacher", "geologist"] or _racer_is_driving():','if career_id in ["teacher", "geologist"] or _racer_is_driving() \\\n\t\t\tor _is_nursery_wash_phase():'),('\telif career_id == "racer":\n\t\tsurface = RacerSurface.new() as OperaGestureSurface','\telif career_id == "nursery":\n\t\tsurface = NurserySurface.new() as OperaGestureSurface\n\telif career_id == "racer":\n\t\tsurface = RacerSurface.new() as OperaGestureSurface'),('\tif career_id == "boxer" and player_actor != null:\n\t\t# The walk-in is third person;', '\tif _is_nursery_wash_phase() and player_actor != null:\n\t\t# The connected wash painting owns Roshan only while this lesson is open.\n\t\t# The unmodified room actor returns at the approached socket next phase.\n\t\tplayer_actor.visible = false\n\tif career_id == "boxer" and player_actor != null:\n\t\t# The walk-in is third person;'),('\tif career_id == "boxer":\n\t\t# Both glove fingers share', '\tif _is_nursery_wash_phase():\n\t\t# A full connected body keeps the hands at readable phone scale.\n\t\t# No framed clipboard or generic dark focus under this painting.\n\t\taction_panel.visible = true\n\t\taction_panel.position = Vector2(320, 24)\n\t\taction_panel.size = Vector2(660, 660)\n\t\tsurface.position = Vector2.ZERO\n\t\tsurface.size = action_panel.size\n\t\tphase_fill.visible = false\n\t\taction_panel.queue_redraw()\n\t\treturn\n\tif career_id == "boxer":\n\t\t# Both glove fingers share')]
for old,new in changes:
    assert text.count(old)==1,old
    text=text.replace(old,new)
where='func _draw_activity_focus() -> void:'
helper='func _is_nursery_wash_phase() -> bool:\n\treturn career_id == "nursery" and phase_index >= 0 and phase_index < phases.size() \\\n\t\tand String((phases[phase_index] as Dictionary).get("name", "")) == "WASH HANDS"\n\n\n'
text=text.replace(where,helper+where)
surface='''class_name OperaNurserySurface
extends OperaGestureSurface
## Connected washing presentation only. CareerWorld owns hold progress,
## completion, route, score and saves. Other Nursery phases keep shared input/drawing.

const WASH_ROOT := "res://assets/opera/worlds/nursery/wash_connected_v1_20261002/"
const WASH_STATES: Array[String] = ["ready", "wet", "rub_palm", "rub_back", "rinse", "clean"]
var wash_textures: Array[Texture2D] = []
var wash_state := "ready"


func _is_wash() -> bool:
	return mode == "hold" and visual_context in ["nursery_wash", "basin_nursery"]


func configure(next_mode: String, next_accent: Color, choice: int = 1,
		next_context: String = "") -> void:
	super.configure(next_mode, next_accent, choice, next_context)
	wash_state = "ready"
	if not _is_wash():
		return
	# The historical nursery prefix selected an empty generic widget family.
	# This specialist binds the same hold to the connected painted action.
	widget_template = ""
	if wash_textures.is_empty():
		for state: String in WASH_STATES:
			wash_textures.append(load(WASH_ROOT + state + ".png") as Texture2D)
	queue_redraw()


func _wash_state_index() -> int:
	if completion_accepted:
		return 5
	if widget_fill <= 0.0 or armed_only:
		return 0
	if widget_fill < 0.18:
		return 1
	if widget_fill < 0.42:
		return 2
	if widget_fill < 0.68:
		return 3
	return 4


func _demo_finger_pose() -> Dictionary:
	if not _is_wash():
		return super._demo_finger_pose()
	return {"at": size * Vector2(0.74, 0.55), "pressing": fmod(demo_t, 2.8) < 1.8}


func _draw() -> void:
	if not _is_wash():
		super._draw()
		return
	var index := _wash_state_index()
	wash_state = WASH_STATES[index]
	last_contextual_draw_route = "nursery_connected_wash:" + wash_state
	last_specialist_subject_route = "nursery_connected_wash"
	last_widget_ground_route = "painted_connected_nursery"
	if wash_textures.size() != WASH_STATES.size() or wash_textures[index] == null:
		push_error("Nursery wash: missing reviewed whole-canvas action painting")
		return
	draw_texture_rect(wash_textures[index], Rect2(Vector2.ZERO, size), false)
	if demo_active and not completion_accepted:
		_draw_demo_finger()
'''
N=R/'scripts/opera_nursery_surface.gd';assert not N.exists()
# Extend the recorded scope before changing dependent production files.
impactp=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json'
impact=json.loads(impactp.read_text());impact['files'] += ['scripts/opera_career_world_2d.gd','scripts/opera_nursery_surface.gd','ASSET_LICENSES.md',F.relative_to(R).as_posix()+'/career_world_baseline.gd.txt']
impact['validation'].append({'command':'Connected wash specialist and whole-canvas source normalization','result':'PENDING','evidence':'Six fixed-layout painted source states; preserve shared input and natural progress. Full mounted sequence and technical gates pending.'})
impactp.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
P.write_text(text,encoding='utf-8');N.write_text(surface,encoding='utf-8')
dest=R/'assets/opera/worlds/nursery/wash_connected_v1_20261002';assert not dest.exists();dest.mkdir(parents=True)
mapping={'ready':'ready_attempt01','wet':'wet_attempt01','rub_palm':'rub_attempt01','rub_back':'rub_back_attempt01','rinse':'rinse_attempt01','clean':'clean_attempt01'}
script='extends SceneTree\n\nfunc _initialize() -> void:\n'
rows=[]
for name,folder in mapping.items():
    src='assets_src/imagegen/nursery_wash_connected_v1_20261002/'+folder+'/native.png'
    output='assets/opera/worlds/nursery/wash_connected_v1_20261002/'+name+'.png'
    script += '\tvar image_'+name+': Image = Image.load_from_file("res://'+src+'")\n\tassert(not image_'+name+'.is_empty())\n\timage_'+name+'.resize(1024, 1024, Image.INTERPOLATE_LANCZOS)\n\tassert(image_'+name+'.save_png("res://'+output+'") == OK)\n'
    rows.append({'native':src,'native_sha256':hashlib.sha256((R/src).read_bytes()).hexdigest(),'runtime':output,'transform':'Uniform whole-canvas 1280x1280 to1024x1024 Lanczos. No crop, isolated subject move, mask, paint repair or alpha replacement; preserve native RGBA.'})
    impact['files'] += [output,output+'.import']
script+='\tprint("NURSERY_WASH|WHOLE_CANVAS_POT_NORMALIZATION|PASS")\n\tquit(0)\n'
(F/'review_tools/normalize_runtime_v350.gd').write_text(script,encoding='utf-8')
(F/'NORMALIZATION_PLAN.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
impactp.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
old=F/'review_tools/capture_baseline_v343.gd'
fixture=old.read_text().replace('/baseline_capture/native_frames/','/candidate_capture_v1/native_frames/')
fixture=fixture.replace('"player_animation":actor.current_animation,','"wash_state": (world.surface as OperaNurserySurface).wash_state if world.surface is OperaNurserySurface else "shared_control",\n\t\t"player_visible":world.player_actor.visible,\n\t\t"player_animation":actor.current_animation,')
(R/'tmp/capture_nursery_wash_candidate_v350.gd').write_text(fixture,encoding='utf-8')
(F/'review_tools/capture_candidate_v350.gd').write_text(fixture,encoding='utf-8')
run=(F/'review_tools/run_baseline_v343.py').read_text().replace('/baseline_capture\'','/candidate_capture_v1\'').replace('capture_nursery_wash_baseline_v343.gd','capture_nursery_wash_candidate_v350.gd')
run=run.replace("paths += ['assets/opera/worlds/props/fx_bop_puff.png'", "paths += ['scripts/opera_nursery_surface.gd'] + [p.relative_to(r).as_posix() for p in (r/'assets/opera/worlds/nursery/wash_connected_v1_20261002').glob('*') if p.is_file()]\npaths += ['assets/opera/worlds/props/fx_bop_puff.png'")
(F/'review_tools/run_candidate_v350.py').write_text(run,encoding='utf-8')
print('Wrote connected wash presentation; import and direct capture pending.')
