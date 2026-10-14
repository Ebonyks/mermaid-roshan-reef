extends SceneTree
## R25 independent Boxing first-phase context; actual partial input; no art acceptance.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var act: OperaAct
var world: OperaCareerWorld2D
var surface: OperaBoxingSurface

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
	var cycle := fmod(surface.demo_t, 2.4) / 2.4
	var hand := int(floor(fmod(surface.demo_t, 4.8) / 2.4))
	var start := surface.glove_rest_position(hand)
	var target := surface.guide_target_position(hand)
	var travel := clampf(cycle / 0.72, 0.0, 1.0)
	travel = travel * travel * (3.0 - 2.0 * travel)
	var at := start.lerp(target, travel)
	states.append({"id":id,"image":{"file":id+".png","sha256":FileAccess.get_sha256(path),"bytes":image_file.get_length(),"dimensions":[frame.get_width(),frame.get_height()]},"presentation":presentation,"phase_index":world.phase_index,"task_open":world.task_open,"mode":surface.mode,"demo_active":surface.demo_active,"demo_t":surface.demo_t,"guide_expected_visible":surface.demo_active and not surface.completion_accepted,"guide_dependency":"Independent procedural _draw_demo;no shared hand texture","guide_formula":{"hand":hand,"cycle":cycle,"travel":travel,"start":[start.x,start.y],"target":[target.x,target.y],"at":[at.x,at.y],"limit":"Source formula introspection,not helper callback/QA11 projection;hidden guide geometry is hypothetical"},"round_index":surface.round_index(),"landed_count":surface.landed_count(),"guide_done":surface.get("_guide_done"),"touch_owners":surface.touch_owner_snapshot(),"held":surface.held,"finished":surface.finished,"completion_accepted":surface.completion_accepted,"assist_level":surface.get("_assist_level"),"input_started":surface.input_started,"phase_progress":world.get("phase_progress"),"glove_positions":[str(surface.glove_positions[0]),str(surface.glove_positions[1])],"mitt_texture":surface.get("_mitts_texture").resource_path if surface.get("_mitts_texture") != null else "","actor_atlas":world.player_actor.get("_sheet").resource_path if world.player_actor != null and world.player_actor.get("_sheet") != null else "","input":input_info,"surface_transform":str(surface.get_global_transform_with_canvas()),"visible_nodes":visible,"save_path":m._save_state.save_path})
	image_file.close()
	print("BOXING_CONTEXT|CAPTURE|" + id)

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
	out_dir = base_out.path_join("%dx%d" % [target.x,target.y]).path_join("phase_00")
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _set_aspect(target):
		errors.append("aspect readiness failed")
		return
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	var profile := out_dir.path_join("profiles/boxing/reef_save.json")
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
	var config: Dictionary = (OperaHouse.ACTS[7] as Dictionary).duplicate(true)
	config["reward_policy"] = "dev_playtest"
	act = OperaAct.new()
	get_root().add_child(act)
	if not act.start(m,config,Callable()):
		errors.append("career start failed")
		return
	await _wait_frames(4)
	world = act.career_world_2d
	world.phase_index = 0
	world._arm_phase()
	world.phase_gap = 0.0
	world._open_task()
	surface = world.surface as OperaBoxingSurface
	if surface == null:
		errors.append("Boxing factory mismatch")
		return
	await create_timer(0.4).timeout
	await _capture("opened_demo_04s",{"entry":"Declared isolated first-phase private dev_playtest;unmodified native specialist;not natural route or fullcareer."})
	await create_timer(0.8).timeout
	await _capture("demo_left_12s")
	await create_timer(1.0).timeout
	await _capture("demo_left_22s")
	await create_timer(0.6).timeout
	await _capture("demo_right_28s")
	await create_timer(1.0).timeout
	await _capture("demo_right_38s")
	await create_timer(1.8).timeout
	await _capture("passive_assist_56s")
	if surface.round_index() != 0 or surface.landed_count() != 0:
		errors.append("passive advanced Boxing progress")
	var at: Vector2 = surface.glove_positions[0]
	await _raw(at,true)
	await _capture("wrong_pressed",{"local":str(at),"kind":"Claim left glove"})
	var wrong := at+Vector2(-30.0,20.0)
	await _drag(wrong,at)
	await _capture("wrong_moved",{"local":str(wrong),"kind":"Actual backward/sideways drag;no forward target contact"})
	await _raw(wrong,false)
	await _capture("wrong_released")
	await create_timer(0.25).timeout
	await _capture("wrong_returned_025s")
	if surface.round_index() != 0 or surface.landed_count() != 0:
		errors.append("wrong advanced Boxing progress")
	at = surface.glove_positions[0]
	await _raw(at,true)
	await _capture("correct_pressed",{"local":str(at),"kind":"Actual left-glove press only;one accepted unit maximum"})
	var to := surface.guide_target_position(0)
	var mid := at.lerp(to,0.45)
	await _drag(mid,at)
	await _capture("correct_mid",{"local":str(mid),"kind":"45percent forward drag;below accepted target threshold"})
	if surface.round_index() != 0:
		errors.append("midpoint advanced Boxing progress")
	await _drag(to,mid)
	await _capture("correct_target",{"local":str(to),"kind":"Actual target;one of two gloves only,no full phase/award"})
	await _raw(to,false)
	await _capture("correct_released")
	await create_timer(0.4).timeout
	await _capture("post_release_04s")
	if surface.held or not surface.touch_owner_snapshot().is_empty() or world.phase_index != 0 or surface.completion_accepted or surface.round_index() != 1 or surface.landed_count() != 1:
		errors.append("partial progress/release/phase scope mismatch")
	act.cancel()
	await _wait_frames(4)
	var teardown_ok := not is_instance_valid(act)
	if not teardown_ok:
		errors.append("teardown failed")
	m.set_process(false)
	m.queue_free()
	await _wait_frames(4)
	var manifest: Dictionary = {"schema":"reef.boxing_pointer_context/1","source_revision":OS.get_environment("ROOTPIC_REV"),"capture_method":"Same-process native viewport diagnostics","engine":Engine.get_version_info(),"renderer":RenderingServer.get_current_rendering_method(),"quality":"speedy","aspect":[target.x,target.y],"phase":0,"states":states,"normal_save_before":normal_before,"normal_save_after":_normal_hashes(),"teardown_verified":teardown_ok,"errors":errors,"scope_limits":"First mode only;current five-mode sourcecaller list separate. Isolated private dev-playtest forced entry,unmodified specialist. Actual bothhand demo timers/5second assistance/passive/backward wrong/one accepted left glove/release. No natural fullroute,second glove/fullphase/award/reload/reentry/focus/QA11/device/child/owner."}
	var file := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest,"	",true)+"\n")
	file.close()

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major",0)) != 4 or int(engine.get("minor",0)) != 7 or int(engine.get("patch",0)) != 2 or String(engine.get("status","")) != "stable" or String(engine.get("build","")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		print("BOXING_CONTEXT|FAIL|engine/renderer/display")
		quit(1)
		return
	normal_before = _normal_hashes()
	var base_out := OS.get_environment("ROOTPIC_OUT")
	if base_out.is_empty() or DirAccess.dir_exists_absolute(base_out):
		print("BOXING_CONTEXT|FAIL|new output required")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(base_out)
	for target: Vector2i in [Vector2i(1280,720),Vector2i(1600,720)]:
		await _run_aspect(target,base_out)
	if normal_before != _normal_hashes():
		errors.append("normal save changed")
	print("BOXING_CONTEXT|RESULT|"+("PASS" if errors.is_empty() else "FAIL")+"|"+str(errors))
	quit(0 if errors.is_empty() else 1)
