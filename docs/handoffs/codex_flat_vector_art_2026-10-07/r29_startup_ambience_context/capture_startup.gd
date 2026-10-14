extends SceneTree
## R29 natural StartMenu audit; no route/event override, production edit or acceptance.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var started_ms: int = 0

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var path := base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result

func _frames(count: int) -> void:
	for i: int in range(count):
		await process_frame

func _aspect(target: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400,0))
		get_root().size = target
		DisplayServer.window_set_size(target)
		await process_frame
		var image: Image = get_root().get_texture().get_image()
		if image != null and image.get_size() == target:
			return true
	return false

func _layers(node: Node, rows: Array[Dictionary]) -> void:
	var layer := node as CanvasLayer
	if layer != null:
		rows.append({"path":str(layer.get_path()),"layer":layer.layer,"visible":layer.visible})
	for child: Node in node.get_children():
		_layers(child,rows)

func _capture(id: String, input_info: Dictionary = {}) -> void:
	await RenderingServer.frame_post_draw
	var frame: Image = get_root().get_texture().get_image()
	var present: Dictionary = {"boot_splash_present":m.get_node_or_null("BootSplashHandoff") != null,"start_menu_active":m.start_menu_active,"start_menu_layer_present":m.start_menu_layer != null,"intro_active":m.intro_active,"intro_overlay_present":m.intro_layer != null,"fade_alpha":m.fade_rect.modulate.a if m.fade_rect != null else 0.0}
	if not m.start_menu_active or not m.intro_active or m.intro_layer != null or bool(present["boot_splash_present"]) or float(present["fade_alpha"]) > 0.02:
		errors.append("normal startup presentation contract failed " + id)
	if frame == null or frame.get_size() != get_root().size:
		errors.append("wrong image backing " + id)
		return
	var path := out_dir.path_join(id+".png")
	if frame.save_png(path) != OK:
		errors.append("PNG write failed " + id)
		return
	var file := FileAccess.open(path,FileAccess.READ)
	var layers: Array[Dictionary] = []
	_layers(m,layers)
	var background := m.get_node_or_null("StartMenu/StartMenuRoot/StartMenuBackground") as TextureRect
	var background_info: Dictionary = {}
	if background != null:
		background_info = {"node":str(background.get_path()),"texture":background.texture.resource_path,"texture_sha256":FileAccess.get_sha256(background.texture.resource_path),"global_rect":str(background.get_global_rect()),"visible":background.is_visible_in_tree()}
	states.append({"id":id,"elapsed_seconds":float(Time.get_ticks_msec()-started_ms)/1000.0,"image":{"file":id+".png","sha256":FileAccess.get_sha256(path),"bytes":file.get_length(),"dimensions":[frame.get_width(),frame.get_height()]},"presentation":present,"resolved_stage":m._living_world_ref().resolve_stage_id(),"active_stage":m.living_stage_id,"layer_visible":m.living_layer.visible,"layer_index":m.living_layer.layer,"canvas_visible":m.living_canvas.is_visible_in_tree(),"canvas_stage":m.living_canvas.get("stage_spec"),"canvas_motion_time":m.living_canvas.get("motion_time"),"canvas_event_progress":m.living_canvas.get("event_progress"),"canvas_rect":str(m.living_canvas.get_global_rect()),"idle_time":m.living_idle_time,"event_time":m.living_event_time,"event_count":m.living_event_count,"cooldown":m.living_cooldown,"probe_stage_override":m.living_probe_stage_override,"suspended":m._living_world_ref()._suspended(),"quiet_group_nodes":get_nodes_in_group("living_world_quiet").size(),"quality":m.quality,"first_session":m.first_session,"game":m.game,"mg_kind":m.mg_kind,"input":input_info,"layers":layers,"background":background_info,"save_path":m._save_state.save_path})
	file.close()
	print("STARTUP_AMBIENCE|CAPTURE|"+id)

func _wait_progress(progress: float) -> bool:
	var until: int = Time.get_ticks_msec()+45000
	while Time.get_ticks_msec() < until:
		await process_frame
		if m.living_canvas != null and float(m.living_canvas.get("event_progress")) >= progress:
			return true
	return false

func _run_aspect(target: Vector2i, base_out: String) -> void:
	out_dir = base_out.path_join("%dx%d" % [target.x,target.y])
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _aspect(target):
		errors.append("aspect not ready")
		return
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	var profile := out_dir.path_join("profiles/startup/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	m._save_state = SaveState.new(m,profile)
	started_ms = Time.get_ticks_msec()
	get_root().add_child(m)
	m._apply_quality("speedy")
	var ready_deadline: int = Time.get_ticks_msec()+25000
	while Time.get_ticks_msec() < ready_deadline:
		await process_frame
		if m.start_menu_active and m.get_node_or_null("BootSplashHandoff") == null and m.living_layer.visible and m.fade_rect.modulate.a <= 0.02:
			break
	await _capture("normal_startup")
	await create_timer(2.0).timeout
	await _capture("continuous_2s")
	for progress: float in [0.0,0.25,0.5,0.75]:
		if not await _wait_progress(progress):
			errors.append("natural idle event timeout "+str(progress))
			break
		await _capture("idle_%02d" % int(progress*100.0))
	var until: int = Time.get_ticks_msec()+6000
	while m.living_event_time >= 0.0 and Time.get_ticks_msec() < until:
		await process_frame
	await _capture("idle_settled")
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = Vector2(30,30)
	event.pressed = true
	get_root().push_input(event,true)
	await _frames(1)
	event = InputEventScreenTouch.new()
	event.index = 0
	event.position = Vector2(30,30)
	event.pressed = false
	get_root().push_input(event,true)
	await _frames(1)
	await _capture("background_touch_released",{"event":"raw viewport touch0 press/release at safe background (30,30)","menu_button_targeted":false})
	var profile_sha: String = FileAccess.get_sha256(profile) if FileAccess.file_exists(profile) else "absent"
	var raw_catalog: Dictionary = LivingWorldCatalog.build()
	for stage: String in raw_catalog:
		var colors: Array = []
		for c: Color in raw_catalog[stage]["palette"]:
			colors.append([c.r,c.g,c.b,c.a])
		raw_catalog[stage]["palette_rgba"] = colors
	var manifest: Dictionary = {"schema":"reef.startup_ambience_native/1","source_revision":OS.get_environment("ROOTPIC_REV"),"engine":Engine.get_version_info(),"display_server":DisplayServer.get_name(),"rendering_method":RenderingServer.get_current_rendering_method(),"quality":"speedy","aspect":[target.x,target.y],"fixture":"Natural scene instantiation with empty private SaveState BEFORE Main; no menu dismissal, IntroOverlay build, forced game route, timer/event mutation, probe override or script swap","normal_save_before":normal_before,"normal_save_after":_normal_hashes(),"private_profile_path":profile,"private_profile_sha256":profile_sha,"states":states.duplicate(true),"errors":errors.duplicate(),"catalogue":raw_catalog,"catalogue_registered_stage_count":raw_catalog.size(),"all_game_reachability_complete":false,"human_acceptance":null}
	m.queue_free()
	await _frames(6)
	manifest["teardown_main_valid"] = is_instance_valid(m)
	manifest["normal_save_after_teardown"] = _normal_hashes()
	var json_file := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	json_file.store_string(JSON.stringify(manifest,"	")+"\n")
	json_file.close()

func _run() -> void:
	normal_before = _normal_hashes()
	var base_out := OS.get_environment("ROOTPIC_OUT")
	if base_out == "":
		quit(2)
		return
	for target: Vector2i in [Vector2i(1280,720),Vector2i(1600,720)]:
		await _run_aspect(target,base_out)
	if _normal_hashes() != normal_before:
		errors.append("normal save hash changed")
	print("STARTUP_AMBIENCE|FINAL|"+JSON.stringify({"errors":errors,"normal_save_unchanged":_normal_hashes()==normal_before}))
	quit(0 if errors.is_empty() else 1)
