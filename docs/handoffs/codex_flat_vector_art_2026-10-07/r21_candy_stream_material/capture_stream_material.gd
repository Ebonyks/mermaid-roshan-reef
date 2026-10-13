extends SceneTree
## R21 isolated whole stream material; raw partial holds/release; no art acceptance.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var act: OperaAct
var world: OperaCareerWorld2D
var surface: OperaGestureSurface

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
	var pose: Dictionary = surface.call("_demo_finger_pose")
	states.append({"id":id,"image":{"file":id+".png","sha256":FileAccess.get_sha256(path),"bytes":image_file.get_length(),"dimensions":[frame.get_width(),frame.get_height()]},"presentation":presentation,"phase_index":world.phase_index,"task_open":world.task_open,"mode":surface.mode,"visual_context":surface.visual_context,"demo_active":surface.demo_active,"demo_t":surface.demo_t,"demo_pose":str(pose),"stream_contract":surface.call("stream_contract"),"pointer_present":surface.pour_demo_hand_texture != null,"pointer_path":surface.pour_demo_hand_texture.resource_path if surface.pour_demo_hand_texture != null else "","pour_level":surface.pour_level,"pour_reserve":surface.pour_reserve,"pour_tilt":surface.pour_tilt,"pour_hold":surface.pour_hold,"held":surface.held,"widget_fill":surface.widget_fill,"input":input_info,"surface_transform":str(surface.get_global_transform_with_canvas()),"visible_nodes":visible,"save_path":m._save_state.save_path})
	image_file.close()
	print("CANDY_STREAM|CAPTURE|" + id)

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

func _run_aspect(target: Vector2i, base_out: String, trial: bool) -> void:
	var branch := "candidate" if trial else "baseline"
	out_dir = base_out.path_join("%dx%d" % [target.x,target.y]).path_join(branch)
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _set_aspect(target):
		errors.append("aspect readiness failed")
		return
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	var profile := out_dir.path_join("profiles/candy/reef_save.json")
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
	var config: Dictionary = (OperaHouse.ACTS[3] as Dictionary).duplicate(true)
	config["reward_policy"] = "dev_playtest"
	act = OperaAct.new()
	get_root().add_child(act)
	if not act.start(m,config,Callable()):
		errors.append("career start failed")
		return
	await _wait_frames(4)
	world = act.career_world_2d
	world.surface.set_script(load("res://.godot/r21_candy_stream_surface.gd"))
	world._arm_phase()
	world.phase_gap = 0.0
	world._open_task()
	surface = world.surface
	surface.set("trial_enabled",trial)
	await create_timer(0.2).timeout
	await _capture("ready",{"entry":"Declared isolated derived-script swap/re-arm at production default first SYRUP phase; dev_playtest. Trial false delegates original draw helper."})
	await create_timer(0.3).timeout
	await _capture("passive_03s")
	var wrong := Vector2(20,20)
	await _raw(wrong,true)
	await _capture("wrong_pressed")
	await _raw(wrong,false)
	await _capture("wrong_released")
	if surface.pour_level != 0.0 or surface.pour_hold:
		errors.append("passive/wrong advanced fill")
	var ladle: Rect2 = surface.call("_pour_pitcher_rect")
	var at := ladle.get_center()
	await _raw(at,true)
	await _capture("ladle_pressed")
	await create_timer(0.2).timeout
	await _capture("held_02s")
	await create_timer(0.6).timeout
	await _capture("held_08s")
	await create_timer(0.6).timeout
	await _capture("held_14s")
	await create_timer(0.8).timeout
	await _capture("held_22s")
	await _drag(at+Vector2(12,0),at)
	await _capture("dragged_12px")
	if not surface.pour_hold or not surface.held or surface.pour_level <= 0.0 or surface.pour_level >= 1.0:
		errors.append("partial-release precondition failed")
	await _raw(at+Vector2(12,0),false)
	await _capture("released")
	await create_timer(0.3).timeout
	await _capture("released_passive_03s")
	if surface.held or surface.pour_hold or world.phase_index != 0:
		errors.append("release/phase scope mismatch")
	act.cancel()
	await _wait_frames(4)
	if is_instance_valid(act):
		errors.append("teardown failed")
	m.set_process(false)
	m.queue_free()
	await _wait_frames(4)
	var manifest: Dictionary = {"schema":"reef.candy_stream_material/1","source_revision":OS.get_environment("ROOTPIC_REV"),"capture_method":"Same-process native viewport diagnostics","engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"quality":"speedy","aspect":[target.x,target.y],"branch":branch,"states":states,"normal_save_before":normal_before,"normal_save_after":_normal_hashes(),"errors":errors,"scope_limits":"Default first-phase private dev-playtest entry and declared script swap/re-arm. Actual passive/wrong/partial holds/drag/release/teardown. No natural Castle/Chapter2,complete award/save reload/re-entry/OSfocus/QA11/device/child/owner acceptance. Painted source glow/S bend remain unresolved; current route is partial,not accepted art."}
	var file := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	file.close()

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major",0)) != 4 or int(engine.get("minor",0)) != 7 or int(engine.get("patch",0)) != 2 or String(engine.get("status","")) != "stable" or String(engine.get("build","")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		print("CANDY_STREAM|FAIL|engine/renderer/display")
		quit(1)
		return
	normal_before = _normal_hashes()
	var base_out := OS.get_environment("ROOTPIC_OUT")
	if base_out.is_empty() or DirAccess.dir_exists_absolute(base_out):
		print("CANDY_STREAM|FAIL|new output required")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(base_out)
	await _run_aspect(Vector2i(1280,720),base_out,false)
	await _run_aspect(Vector2i(1280,720),base_out,true)
	await _run_aspect(Vector2i(1600,720),base_out,false)
	await _run_aspect(Vector2i(1600,720),base_out,true)
	if normal_before != _normal_hashes():
		errors.append("normal save changed")
	print("CANDY_STREAM|RESULT|"+("PASS" if errors.is_empty() else "FAIL")+"|"+str(errors))
	quit(0 if errors.is_empty() else 1)
