extends SceneTree
## R27 independent Teacher four-kind tier0 sequence0 context; actual partial input; no art acceptance.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var act: OperaAct
var world: OperaCareerWorld2D
var surface: OperaTeacherSurface

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var path := base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result

func _wait_frames(count: int) -> void:
	for i: int in range(count):
		await process_frame

func _set_aspect(target: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		get_root().size = target
		DisplayServer.window_set_size(target)
		await process_frame
		var test: Image = get_root().get_texture().get_image()
		if test != null and test.get_size() == target:
			return true
	return false

func _visible_nodes(node: Node, output: Array[Dictionary]) -> void:
	var item := node as CanvasItem
	if item != null and item.is_visible_in_tree():
		var row: Dictionary = {"path": str(node.get_path()), "class": node.get_class(), "modulate": str(item.modulate), "z_index": item.z_index}
		var control := node as Control
		if control != null:
			row["global_rect"] = str(control.get_global_rect())
		var texture := node as TextureRect
		if texture != null and texture.texture != null:
			row["texture"] = texture.texture.resource_path
		var button := node as Button
		if button != null:
			row["disabled"] = button.disabled
		output.append(row)
	for child: Node in node.get_children():
		_visible_nodes(child, output)

func _presentation() -> Dictionary:
	return {"boot_splash_present": m.get_node_or_null("BootSplashHandoff") != null, "start_menu_active": m.start_menu_active, "start_menu_layer_present": m.start_menu_layer != null, "intro_active": m.intro_active, "intro_layer_present": m.intro_layer != null, "fade_alpha": m.fade_rect.modulate.a if m.fade_rect != null else 0.0, "medal_present": m.get_node_or_null("MedalCelebrationLayer") != null}

func _wait_presentation() -> bool:
	for i: int in range(300):
		await process_frame
		var present := _presentation()
		if not bool(present["boot_splash_present"]) and not bool(present["start_menu_active"]) and not bool(present["start_menu_layer_present"]) and not bool(present["intro_active"]) and not bool(present["intro_layer_present"]) and float(present["fade_alpha"]) <= 0.02:
			return true
	return false

func _capture(id: String, input_info: Dictionary = {}) -> void:
	await RenderingServer.frame_post_draw
	var presentation := _presentation()
	if bool(presentation["boot_splash_present"]) or bool(presentation["start_menu_active"]) or bool(presentation["medal_present"]) or float(presentation["fade_alpha"]) > 0.02:
		errors.append("blocking presentation overlay " + id)
	var frame: Image = get_root().get_texture().get_image()
	if frame == null or frame.get_size() != get_root().size:
		errors.append("image backing mismatch " + id)
		return
	var path := out_dir.path_join(id + ".png")
	if frame.save_png(path) != OK:
		errors.append("save failed " + id)
		return
	var visible: Array[Dictionary] = []
	_visible_nodes(world, visible)
	var image_file := FileAccess.open(path, FileAccess.READ)
	var guide: Dictionary = {"expected_visible":false,"target_role":"NONE","at":[],"limit":"Exact source formula introspection;not callback/QA11 live projection. _draw_demo does not consult demo_active."}
	var target := Vector2.ZERO
	if surface.lesson_kind() == "add" and not surface.joined:
		target = surface.JOIN_CENTER
		guide["target_role"] = "JOIN_BUTTON"
	elif surface.counted.has(false):
		target = surface.counter_position(surface.counted.find(false))
		guide["target_role"] = "NEXT_UNTOUCHED_COUNTER"
	elif surface.help_visible:
		target = surface.choice_rect(surface.answer_index()).get_center()
		guide["target_role"] = "CORRECT_ANSWER_CARD"
	if guide["target_role"] != "NONE" and not surface.solved:
		guide["expected_visible"] = true
		guide["at"] = [target.x,target.y]
	guide["pulse_radius"] = 41.0 * (1.0 + sin(surface.idle_demo_t * 4) * 0.12)
	var tiles: Array[String] = []
	for tile: Texture2D in world.backdrop_node.get("room_variant_tiles"):
		tiles.append(tile.resource_path)
	states.append({"id":id,"image":{"file":id+".png","sha256":FileAccess.get_sha256(path),"bytes":image_file.get_length(),"dimensions":[frame.get_width(),frame.get_height()]},"presentation":presentation,"phase_index":world.phase_index,"task_open":world.task_open,"mode":surface.mode,"lesson":surface.lesson.duplicate(true),"snapshot":surface.progress_snapshot().duplicate(true),"counted":surface.counted.duplicate(true),"joined":surface.joined,"join_t":surface.join_t,"can_answer":surface.can_answer(),"chosen":surface.chosen,"solved":surface.solved,"help_visible":surface.help_visible,"demo_active":surface.demo_active,"idle_demo_t":surface.idle_demo_t,"guide_formula":guide,"touch_owner":surface.touch_owner,"held":surface.held,"completion_accepted":surface.completion_accepted,"wrong_attempts":surface.wrong_attempts,"assisted":surface.assisted,"phase_progress":world.get("phase_progress"),"input_started":surface.input_started,"actor_visible":world.player_actor.is_visible_in_tree(),"actor_atlas":world.player_animator.get("_sheet").resource_path if world.player_animator.get("_sheet") != null else "","actor_animation":world.player_animator.current_animation,"actor_frame":world.player_animator.current_frame,"backdrop_tiles":tiles,"input":input_info,"surface_transform":str(surface.get_global_transform_with_canvas()),"visible_nodes":visible,"save_path":m._save_state.save_path})
	image_file.close()
	print("TEACHER_CONTEXT|CAPTURE|" + id)

func _raw(local: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.pressed = pressed
	event.position = surface.get_global_transform_with_canvas() * local
	get_root().push_input(event,true)
	await process_frame

func _drag(local: Vector2, previous: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = surface.get_global_transform_with_canvas() * local
	event.relative = surface.get_global_transform_with_canvas().basis_xform(local-previous)
	get_root().push_input(event,true)
	await process_frame

func _tap(at: Vector2, prefix: String, note: String) -> void:
	await _raw(at,true)
	await _capture(prefix+"_pressed",{"local":str(at),"kind":note,"event":"raw viewport touch0 press"})
	await _raw(at,false)
	await _capture(prefix+"_released",{"local":str(at),"kind":note,"event":"raw viewport touch0 release"})

func _run_phase(target: Vector2i, base_out: String, phase: int) -> void:
	out_dir = base_out.path_join("%dx%d" % [target.x,target.y]).path_join("phase_%02d" % phase)
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _set_aspect(target):
		errors.append("aspect readiness failed")
		return
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	var profile := out_dir.path_join("profiles/teacher/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	m._save_state = SaveState.new(m,profile)
	get_root().add_child(m)
	await _wait_frames(3)
	m._apply_quality("speedy")
	m.day_one_active = false
	if m.start_menu_active:
		m._start_menu_ref()._dismiss_menu()
	if m.intro_active:
		m._skip_intro()
	if not await _wait_presentation():
		errors.append("startup presentation did not settle")
		return
	var config: Dictionary = (OperaHouse.ACTS[17] as Dictionary).duplicate(true)
	config["reward_policy"] = "dev_playtest"
	act = OperaAct.new()
	get_root().add_child(act)
	if not act.start(m,config,Callable()):
		errors.append("career start failed")
		return
	await _wait_frames(4)
	world = act.career_world_2d
	world.phase_index = phase
	world._arm_phase()
	world.phase_gap = 0.0
	world._open_task()
	surface = world.surface as OperaTeacherSurface
	if surface == null:
		errors.append("Teacher factory mismatch")
		return
	await create_timer(0.4).timeout
	await _capture("opened_04s",{"entry":"Declared isolated phase private dev_playtest;unmodified native specialist;tier0 sequence0;not natural route."})
	await create_timer(9.2).timeout
	await _capture("passive_96s")
	if surface.solved or surface.counted.has(true) or (phase == 2 and surface.joined):
		errors.append("passive advanced lesson")
	var wrong := surface.choice_rect((surface.answer_index()+1) % (surface.lesson.get("choices",[]) as Array).size()).get_center()
	await _tap(wrong,"wrong_choice","Wrong answer-card tap; ignored while counters/join incomplete,assistance otherwise")
	await _tap(surface.HINT_CENTER,"hint","Actual hint-button tap; no lesson completion")
	if phase == 2:
		await _tap(surface.JOIN_CENTER,"join","Actual join tap only; source0.4second combination")
		await create_timer(0.16).timeout
		await _capture("join_moving")
		await create_timer(0.30).timeout
		await _capture("join_settled")
	if phase in [1,2]:
		await _tap(surface.counter_position(0),"counter0","Actual first counter tap; count phase reaches answer eligibility,add remains one of two")
		await _tap(surface.counter_position(0),"counter0_repeat","Actual repeated counted-counter tap; no duplicate progress")
		if phase == 1:
			await _tap(wrong,"count_answer_wrong","Actual wrong count-answer after eligibility; counted state retained")
	await _capture("final_partial")
	if surface.held or surface.touch_owner != -1 or world.phase_index != phase or surface.solved or surface.completion_accepted or float(world.get("phase_progress")) != 0.0:
		errors.append("partial/release/phase scope mismatch")
	act.cancel()
	await _wait_frames(4)
	var teardown_ok := not is_instance_valid(act)
	if not teardown_ok:
		errors.append("teardown failed")
	m.set_process(false)
	m.queue_free()
	await _wait_frames(4)
	var manifest: Dictionary = {"schema":"reef.teacher_pointer_context/1","source_revision":OS.get_environment("ROOTPIC_REV"),"capture_method":"Same-process native viewport diagnostics","engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"quality":"speedy","aspect":[target.x,target.y],"phase":phase,"states":states,"normal_save_before":normal_before,"normal_save_after":_normal_hashes(),"teardown_verified":teardown_ok,"errors":errors.duplicate(),"scope_limits":"Four isolated tier0 sequence0 phases;unmodified source;raw actual passive/wrong/hint/join/counter/repeated touches without lesson completion. Natural route,higher tiers/sequences/fullcareer/award/reload/reentry/focus/QA11/device/child/owner open."}
	var file := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	file.close()

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major",0)) != 4 or int(engine.get("minor",0)) != 7 or int(engine.get("patch",0)) != 2 or String(engine.get("status","")) != "stable" or String(engine.get("build","")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		print("TEACHER_CONTEXT|FAIL|engine/renderer/display")
		quit(1)
		return
	normal_before = _normal_hashes()
	var base_out := OS.get_environment("ROOTPIC_OUT")
	if base_out.is_empty() or DirAccess.dir_exists_absolute(base_out):
		print("TEACHER_CONTEXT|FAIL|new output required")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(base_out)
	for target: Vector2i in [Vector2i(1280,720),Vector2i(1600,720)]:
		for phase: int in range(4):
			await _run_phase(target,base_out,phase)
	if normal_before != _normal_hashes():
		errors.append("normal save changed")
	print("TEACHER_CONTEXT|RESULT|"+("PASS" if errors.is_empty() else "FAIL")+"|"+str(errors))
	quit(0 if errors.is_empty() else 1)
