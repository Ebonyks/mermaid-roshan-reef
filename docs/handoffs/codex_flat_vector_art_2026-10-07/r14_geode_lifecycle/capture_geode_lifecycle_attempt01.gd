extends SceneTree
## Original production Geode lifecycle diagnostic. Explicit seeded legacy checkpoint; two engine processes; no replacement or QA11 claim.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var house: OperaHouse
var return_events: Array[bool] = []
var lifecycle: Array[Dictionary] = []
var profile_path := ""
var run_part := ""
var world: OperaCareerWorld2D
var surface: OperaGeologySurface

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

func _returned(completed: bool) -> void:
	return_events.append(completed)

func _fact(id: String) -> Dictionary:
	var checkpoint: Variant = m.save_data.get("opera_geology_checkpoint", {})
	var row: Dictionary = {"id":id,"checkpoint":checkpoint,"opera_stars":m.opera_stars,"pearls":m.pearl_count,"sentinel_preserved":m.save_data.get("fvr14_isolated_sentinel","") == "preserve-unknown-field","save_sha256":FileAccess.get_sha256(profile_path) if FileAccess.file_exists(profile_path) else "absent","backup_sha256":FileAccess.get_sha256(profile_path+".bak") if FileAccess.file_exists(profile_path+".bak") else "absent","return_events":return_events.duplicate()}
	lifecycle.append(row)
	return row

func _capture(id: String, input_info: Dictionary = {}) -> void:
	await RenderingServer.frame_post_draw
	var presentation := _presentation()
	if bool(presentation["boot_splash_present"]) or bool(presentation["start_menu_active"]) or float(presentation["fade_alpha"]) > 0.02:
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
	_visible_nodes(world if is_instance_valid(world) else m,visible)
	var row: Dictionary = {"id":id,"image":{"file":id+".png","sha256":FileAccess.get_sha256(path),"bytes":FileAccess.open(path,FileAccess.READ).get_length(),"dimensions":[frame.get_width(),frame.get_height()]},"presentation":presentation,"input":input_info,"visible_nodes":visible,"save_facts":_fact(id),"original_production_draw":true,"replacement_drawn":false,"world_live":is_instance_valid(world),"surface_live":is_instance_valid(surface)}
	if is_instance_valid(world):
		row["phase_index"] = world.phase_index
		row["task_open"] = world.task_open
		row["active"] = world.active
		row["phase_advance_pending"] = world.phase_advance_pending
		row["phase_complete_t"] = world.phase_complete_t
	if is_instance_valid(surface):
		row["mode"] = surface.mode
		row["surface_snapshot"] = surface.progress_snapshot()
		row["seams"] = surface.geode_seams.duplicate()
		row["pull"] = surface.geode_pull
		row["held"] = surface.held
		row["completion_accepted"] = surface.completion_accepted
		row["surface_transform"] = str(surface.get_global_transform_with_canvas())
	states.append(row)
	print("GEO_LIFECYCLE|CAPTURE|"+run_part+"|"+id)

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

func _enter(open_task: bool = true) -> void:
	house = OperaHouse.new()
	get_root().add_child(house)
	if not house.start(m,16,Callable(self,"_returned")):
		errors.append("production house entry failed")
		return
	await _wait_frames(5)
	world = house.act.career_world_2d
	surface = world.surface as OperaGeologySurface
	if world.two_act_enabled or world.using_chapter_two_phases or world._is_dev_playtest():
		errors.append("unexpected policy/phase family")
	if open_task:
		world.phase_gap = 0.0
		world._open_task()
		await create_timer(0.2).timeout

func _leave(id: String) -> void:
	house._leave_early()
	await _wait_frames(5)
	if is_instance_valid(house) or is_instance_valid(world):
		errors.append("early leave did not tear down owned nodes")
	await _capture(id,{"method":"production OperaHouse._leave_early API; not physical Back touch or Castle-room route"})

func _run_aspect(target: Vector2i, base_out: String) -> void:
	var aspect_dir := base_out.path_join("%dx%d" % [target.x,target.y])
	out_dir = aspect_dir.path_join(run_part)
	if DirAccess.dir_exists_absolute(out_dir):
		errors.append("fresh part directory required")
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	lifecycle.clear()
	return_events.clear()
	if not await _set_aspect(target):
		errors.append("aspect readiness failed")
		return
	profile_path = aspect_dir.path_join("profiles/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile_path.get_base_dir())
	if (run_part == "prepare" and FileAccess.file_exists(profile_path)) or (run_part == "resume" and not FileAccess.file_exists(profile_path)):
		errors.append("profile preparation/reload precondition failed")
		return
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	m._save_state = SaveState.new(m,profile_path)
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
	if run_part == "prepare":
		m.save_data["fvr14_isolated_sentinel"] = "preserve-unknown-field"
		m.save_data["opera_geology_checkpoint"] = {"version":1,"phase_index":3,"mechanic":{}}
		if not m._write_save():
			errors.append("seeded isolated checkpoint write failed")
		await _enter(false)
		await _capture("geode_room_armed",{"fixture":"Only initial fresh profile phase3 checkpoint seeded; first three phases not played; ordinary policy"})
		world.phase_gap = 0.0
		world._open_task()
		await create_timer(0.2).timeout
		await _capture("geode_closed_ready")
		await create_timer(1.0).timeout
		await _capture("geode_passive_1s",{"method":"no input"})
		await _raw(Vector2(570,550),true)
		await _raw(Vector2(570,550),false)
		await _capture("geode_wrong_tap")
		var early := Vector2(860,340)
		await _raw(early,true)
		await _drag(early+Vector2(60,0),early)
		await _raw(early+Vector2(60,0),false)
		await _capture("geode_early_pull_ignored")
		if surface.geode_pull != 0.0 or surface.geode_seams.count(true) != 0 or m.opera_stars != 0:
			errors.append("negative input granted progress/reward")
		for i: int in range(5):
			var at := surface.geode_seam_spot(i)
			await _raw(at,true)
			if surface.geode_seams.count(true) != i:
				errors.append("seam accepted before release")
			await _raw(at,false)
			await _capture("geode_seam%02d_released" % i,{"method":"Window synthetic press/release at original visible guide/hit center","seam_index":i})
			if surface.geode_seams.count(true) != i+1:
				errors.append("seam release count mismatch")
		var start: Vector2 = surface.geode_half_center()
		await _raw(start,true)
		await _drag(start+Vector2(60,0),start)
		await _capture("geode_pull060_held")
		await _raw(start+Vector2(60,0),false)
		await _capture("geode_pull060_released")
		await _raw(surface.geode_half_center(),true)
		surface.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
		world.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
		await _wait_frames(3)
		await _capture("geode_focus060_flushed",{"method":"explicit surface/world focus-out notifications; no real OS/device focus claim"})
		if surface.held or surface.geode_pull != 60.0 or m.opera_stars != 0:
			errors.append("focus lost partial progress or granted star")
		await _leave("geode_partial_leave_return")
	else:
		if not m.has_saved_game or m.save_data.get("fvr14_isolated_sentinel","") != "preserve-unknown-field":
			errors.append("separate-process disk reload lost valid profile/unknown field")
		await _enter(false)
		await _capture("geode_disk_resume_room_armed")
		world.phase_gap = 0.0
		world._open_task()
		await create_timer(0.2).timeout
		await _capture("geode_disk_resume060_task")
		if world.phase_index != 3 or surface.geode_seams.count(true) != 5 or surface.geode_pull != 60.0 or surface.held:
			errors.append("disk checkpoint restore mismatch")
		var start: Vector2 = surface.geode_half_center()
		await _raw(start,true)
		await _drag(start+Vector2(59,0),start)
		await _capture("geode_pull119_held")
		await _raw(start+Vector2(59,0),false)
		await _capture("geode_pull119_released")
		world.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
		await _leave("geode_119_leave_return")
		await _enter(false)
		await _capture("geode_119_reentry_room_armed")
		world.phase_gap = 0.0
		world._open_task()
		await create_timer(0.2).timeout
		await _capture("geode_119_reentry_task")
		if world.phase_index != 3 or surface.geode_pull != 119.0 or surface.geode_seams.count(true) != 5:
			errors.append("reentry119 mismatch")
		var finish_start: Vector2 = surface.geode_half_center()
		await _raw(finish_start,true)
		await _drag(finish_start+Vector2(2,0),finish_start)
		await _capture("geode_completed120_held",{"method":"actual two-pixel synthetic drag; remaining pull1 clamped to original120 threshold"})
		await _raw(finish_start+Vector2(2,0),false)
		await _raw(finish_start,true)
		await _raw(finish_start,false)
		await _capture("geode_completion_repeat_ignored")
		if surface.geode_pull != 120.0 or not surface.completion_accepted or not world.phase_advance_pending or m.opera_stars != 0:
			errors.append("completion threshold/hold mismatch")
		await create_timer(0.75).timeout
		await _capture("geode_completion_hold")
		await create_timer(6.0).timeout
		await _capture("geode_completion_reward_return")
		if is_instance_valid(house) or (m.opera_stars & (1<<16)) == 0 or m.pearl_count != 3 or not return_events.has(true) or not (m.save_data.get("opera_geology_checkpoint",{}) as Dictionary).is_empty():
			errors.append("production completion/reward/checkpoint cleanup mismatch")
		await _enter(false)
		await _capture("geode_post_reward_reentry_room")
		if world.phase_index != 0:
			errors.append("post-reward checkpoint failed to clear")
		world.phase_gap = 0.0
		world._open_task()
		await create_timer(0.2).timeout
		await _capture("geode_post_reward_reentry_river")
		if surface.mode != "geology_river" or surface.progress() != 0.0 or m.pearl_count != 3:
			errors.append("post-reward replay start mismatch")
		await _leave("geode_replay_leave_return")
	var final_facts := _fact("final_before_main_free")
	m.set_process(false)
	m.queue_free()
	await _wait_frames(5)
	var manifest: Dictionary = {"schema":"reef.geode_original_lifecycle/1","source_revision":OS.get_environment("ROOTPIC_REV"),"script_sha256":FileAccess.get_sha256("res://.godot/r14_capture_geode_lifecycle.gd"),"part":run_part,"engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"quality":"speedy","aspect":[target.x,target.y],"states":states,"lifecycle":lifecycle,"final_facts":final_facts,"normal_save_before":normal_before,"normal_save_after":_normal_hashes(),"errors":errors,"scope_limits":"Original-production diagnostic,ordinary legacy policy. Initial phase3 checkpoint seeded once; first three phases and natural Castle/Chapter2 route not played. Second engine process reloads isolated disk profile. Actual synthetic Window input,API early leave and explicit focus notifications; not QA11,device,child,owner or replacement acceptance."}
	var file := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	file.close()

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major",0)) != 4 or int(engine.get("minor",0)) != 7 or int(engine.get("patch",0)) != 2 or String(engine.get("status","")) != "stable" or String(engine.get("build","")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		quit(1)
		return
	normal_before = _normal_hashes()
	var base_out := OS.get_environment("ROOTPIC_OUT")
	run_part = OS.get_environment("ROOTPIC_PART")
	if base_out.is_empty() or run_part not in ["prepare","resume"] or (run_part == "prepare" and DirAccess.dir_exists_absolute(base_out)) or (run_part == "resume" and not DirAccess.dir_exists_absolute(base_out)):
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(base_out)
	await _run_aspect(Vector2i(1280,720),base_out)
	await _run_aspect(Vector2i(1600,720),base_out)
	if normal_before != _normal_hashes():
		errors.append("normal save changed")
	print("GEO_LIFECYCLE|RESULT|"+run_part+"|"+("PASS" if errors.is_empty() else "FAIL")+"|"+str(errors))
	quit(0 if errors.is_empty() else 1)
