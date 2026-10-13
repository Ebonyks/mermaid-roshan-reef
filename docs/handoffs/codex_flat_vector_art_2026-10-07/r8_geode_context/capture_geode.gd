extends SceneTree
## Geologist closed-shell diagnostics. Declared direct GEODE phase fixture; fresh isolated save; no production edits.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var act: OperaAct
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
	states.append({"id": id, "image": {"file": id+".png", "sha256":FileAccess.get_sha256(path), "bytes":image_file.get_length(), "dimensions":[frame.get_width(),frame.get_height()]}, "presentation":presentation, "phase_index":world.phase_index, "task_open":world.task_open, "mode":surface.mode, "surface_snapshot":surface.progress_snapshot(), "seams":surface.geode_seams.duplicate(), "pull":surface.geode_pull, "held":surface.held, "input":input_info, "surface_transform":str(surface.get_global_transform_with_canvas()), "visible_nodes":visible, "save_path":m._save_state.save_path})
	image_file.close()
	print("GEOCONTEXT|CAPTURE|" + id)

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

func _run_aspect(target: Vector2i, base_out: String) -> void:
	out_dir = base_out.path_join("%dx%d" % [target.x,target.y])
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _set_aspect(target):
		errors.append("aspect readiness failed")
		return
	var scene := load("res://scenes/main.tscn") as PackedScene
	m = scene.instantiate() as ReefMain
	var profile := out_dir.path_join("profiles/geode/reef_save.json")
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
		m.queue_free()
		await _wait_frames(4)
		return
	var config: Dictionary = (OperaHouse.ACTS[16] as Dictionary).duplicate(true)
	config["reward_policy"] = "dev_playtest"
	act = OperaAct.new()
	get_root().add_child(act)
	if not act.start(m,config,Callable()):
		errors.append("production career start failed")
		return
	await _wait_frames(4)
	world = act.career_world_2d
	# Explicit phase fixture: no earlier phase completion or natural route claim.
	world.phase_index = 3
	world._arm_phase()
	world.phase_gap = 0.0
	world._open_task()
	surface = world.surface as OperaGeologySurface
	await create_timer(0.45).timeout
	if surface == null or surface.mode != "geology_geode" or surface.geode_seams.count(true) != 0 or surface.geode_pull != 0.0:
		errors.append("fresh geode fixture mismatch")
		return
	await _capture("geode_closed_ready",{"entry":"OperaAct production start, dev_playtest; explicit phase_index=3 fixture followed by production _arm_phase/_open_task"})
	await create_timer(1.0).timeout
	await _capture("geode_closed_passive_1s",{"method":"no input, one second"})
	var miss := Vector2(570,550)
	await _raw(miss,true)
	await _raw(miss,false)
	await _capture("geode_wrong_tap",{"method":"Window.push_input touch press/release", "local_point":str(miss)})
	var pull_at := Vector2(860,340)
	await _raw(pull_at,true)
	await _capture("geode_early_pull_pressed")
	await _drag(pull_at+Vector2(60,0),pull_at)
	await _capture("geode_early_pull_dragged")
	await _raw(pull_at+Vector2(60,0),false)
	await _capture("geode_early_pull_released")
	if surface.geode_seams.count(true) != 0 or surface.geode_pull != 0.0:
		errors.append("negative input changed seam/pull")
	for i: int in range(5):
		var at := surface.geode_seam_spot(i)
		var info: Dictionary = {"method":"Window.push_input touch press/release", "seam_index":i, "local_point":str(at)}
		await _raw(at,true)
		await _capture("geode_seam%02d_pressed" % i,info)
		if surface.geode_seams.count(true) != i:
			errors.append("seam accepted before release")
		await _raw(at,false)
		await _wait_frames(3)
		await _capture("geode_seam%02d_released" % i,info)
		if surface.geode_seams.count(true) != i+1:
			errors.append("seam release transition failed %d" % i)
	await _raw(surface.geode_seam_spot(0),true)
	await _raw(surface.geode_seam_spot(0),false)
	await _capture("geode_seam_repeat",{"method":"repeat first accepted seam; no extra completion"})
	await create_timer(0.5).timeout
	await _capture("geode_all_seams_ready")
	await _raw(pull_at,true)
	await _drag(pull_at+Vector2(60,0),pull_at)
	await _capture("geode_partial_open_held",{"method":"raw touch drag", "delta":[60,0]})
	await _raw(pull_at+Vector2(60,0),false)
	await _wait_frames(3)
	await _capture("geode_partial_open_released")
	if surface.geode_pull < 59.0 or surface.geode_pull > 61.0:
		errors.append("partial pull transition failed")
	await _raw(pull_at+Vector2(60,0),true)
	await _capture("geode_cancel_pressed")
	surface.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	await _wait_frames(3)
	await _capture("geode_cancel_focus_notification",{"method":"explicit surface focus-out notification; diagnostic, not observed OS focus loss"})
	if surface.held or surface.geode_pull < 59.0:
		errors.append("cancel lost pull or retained input")
	act.cancel()
	await _wait_frames(4)
	if is_instance_valid(act):
		errors.append("act teardown failed")
	m.set_process(false)
	m.queue_free()
	await _wait_frames(4)
	var manifest: Dictionary = {"schema":"reef.geode_context/1", "source_revision":OS.get_environment("ROOTPIC_REV"), "capture_method":"same-process native viewport diagnostics", "engine":Engine.get_version_info(), "renderer":RenderingServer.get_current_rendering_method(), "quality":"speedy", "aspect":[target.x,target.y], "states":states, "normal_save_before":normal_before, "normal_save_after":_normal_hashes(), "errors":errors, "scope_limits":"Fresh isolated SaveState; production Geologist dev_playtest lifecycle; declared GEODE phase fixture. Actual Window touch press/release/drag, five seam changes and partial opening only. No earlier-phase completion, natural route, full opening/reward, restart/re-entry, actual OS-focus/device, child, owner or DL-QA-11 acceptance."}
	var file := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	file.close()

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major",0)) != 4 or int(engine.get("minor",0)) != 7 or int(engine.get("patch",0)) != 2 or String(engine.get("status","")) != "stable" or String(engine.get("build","")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		print("GEOCONTEXT|FAIL|engine/renderer/display")
		quit(1)
		return
	normal_before = _normal_hashes()
	var base_out := OS.get_environment("ROOTPIC_OUT")
	if base_out.is_empty() or DirAccess.dir_exists_absolute(base_out):
		print("GEOCONTEXT|FAIL|new output required")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(base_out)
	await _run_aspect(Vector2i(1280,720),base_out)
	await _run_aspect(Vector2i(1600,720),base_out)
	if normal_before != _normal_hashes():
		errors.append("normal save changed")
	print("GEOCONTEXT|RESULT|"+("PASS" if errors.is_empty() else "FAIL")+"|"+str(errors))
	quit(0 if errors.is_empty() else 1)
