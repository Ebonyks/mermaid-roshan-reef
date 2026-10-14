extends SceneTree
## R30 real menu touch/idle/Continue lifecycle; private saves, no art acceptance.
var m: ReefMain
var out_dir := ""
var variant := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var started_ms: int = 0
var profile := ""

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

func _button(node: Node, name: String) -> Button:
	if node.name == name:
		return node as Button
	for child: Node in node.get_children():
		var found: Button = _button(child,name)
		if found != null:
			return found
	return null

func _layers(node: Node, rows: Array[Dictionary]) -> void:
	var layer := node as CanvasLayer
	if layer != null:
		rows.append({"path":str(layer.get_path()),"layer":layer.layer,"visible":layer.visible})
	for child: Node in node.get_children():
		_layers(child,rows)

func _progress() -> Dictionary:
	return {"pearls":m.pearl_count,"won":m.save_data.get("won",{}),"found":m.save_data.get("found",{}),"opera_stars":m.save_data.get("opera_stars",0),"chapter2_job_phase_masks":m.save_data.get("chapter2_job_phase_masks",[]),"r30_keep_marker":m.save_data.get("r30_keep_marker",null)}.duplicate(true)

func _capture(id: String, expect_menu: bool = true, input_info: Dictionary = {}) -> void:
	await RenderingServer.frame_post_draw
	var frame: Image = get_root().get_texture().get_image()
	if frame == null or frame.get_size() != get_root().size:
		errors.append("wrong image backing " + id)
		return
	var present: Dictionary = {"boot_splash_present":m.get_node_or_null("BootSplashHandoff") != null,"start_menu_active":m.start_menu_active,"start_menu_layer_present":m.start_menu_layer != null,"intro_active":m.intro_active,"intro_overlay_present":m.intro_layer != null,"fade_alpha":m.fade_rect.modulate.a if m.fade_rect != null else 0.0}
	if bool(present["boot_splash_present"]) or float(present["fade_alpha"]) > 0.02:
		errors.append("blocking presentation " + id)
	if expect_menu:
		if not m.start_menu_active or not m.intro_active or m.living_layer.visible or m.living_canvas.is_visible_in_tree() or not m._living_world_ref()._suspended() or m.living_idle_time > 0.0 or m.living_event_time >= 0.0:
			errors.append("menu ambience retirement failed " + id)
	else:
		if m.start_menu_active or m.intro_active or not m.living_layer.visible or not m.living_canvas.is_visible_in_tree() or m._living_world_ref()._suspended():
			errors.append("sibling ambience restoration failed " + id)
	var path := out_dir.path_join(id+".png")
	if frame.save_png(path) != OK:
		errors.append("PNG write failed " + id)
		return
	var file := FileAccess.open(path,FileAccess.READ)
	var layers: Array[Dictionary] = []
	_layers(m,layers)
	var buttons: Array[Dictionary] = []
	if m.start_menu_layer != null:
		for name: String in ["StartMenuContinueButton","StartMenuNewGameButton","StartMenuOptionsButton","StartMenuMusicButton","StartMenuKeepGameButton","StartMenuConfirmNewGameButton"]:
			var button: Button = _button(m.start_menu_layer,name)
			if button != null:
				buttons.append({"name":name,"visible":button.is_visible_in_tree(),"disabled":button.disabled,"rect":str(button.get_global_rect()),"pressed":button.button_pressed})
	var menu: StartMenu = m._start_menu_ref()
	var backdrop: Dictionary = {}
	if m.start_menu_layer != null:
		var background := m.start_menu_layer.get_node_or_null("StartMenuRoot/StartMenuBackground") as TextureRect
		if background != null:
			backdrop = {"node":str(background.get_path()),"texture":background.texture.resource_path,"sha256":FileAccess.get_sha256(background.texture.resource_path),"visible":background.is_visible_in_tree(),"global_rect":str(background.get_global_rect())}
	states.append({"id":id,"variant":variant,"elapsed_seconds":float(Time.get_ticks_msec()-started_ms)/1000.0,"expect_menu":expect_menu,"image":{"file":id+".png","sha256":FileAccess.get_sha256(path),"bytes":file.get_length(),"dimensions":[frame.get_width(),frame.get_height()]},"presentation":present,"resolved_stage":m._living_world_ref().resolve_stage_id(),"active_stage":m.living_stage_id,"layer_visible":m.living_layer.visible,"layer_index":m.living_layer.layer,"canvas_visible":m.living_canvas.is_visible_in_tree(),"canvas_event_progress":m.living_canvas.get("event_progress"),"idle_time":m.living_idle_time,"event_time":m.living_event_time,"event_count":m.living_event_count,"probe_stage_override":m.living_probe_stage_override,"suspended":m._living_world_ref()._suspended(),"quality":m.quality,"has_saved_game":m.has_saved_game,"day_one_active":m.day_one_active,"game":m.game,"phase":m.g.get("phase",""),"progress":_progress(),"input":input_info,"layers":layers,"buttons":buttons,"background":backdrop,"options_visible":is_instance_valid(menu._options_root) and menu._options_root.visible,"confirmation_visible":is_instance_valid(menu._confirm_root) and menu._confirm_root.visible,"new_game_hold_active":menu._new_game_hold_active,"save_path":m._save_state.save_path})
	file.close()
	print("STARTUP_RETIREMENT|CAPTURE|"+variant+"|"+id)

func _raw(point: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = point
	event.pressed = pressed
	Input.parse_input_event(event)
	await _frames(1)

func _tap(name: String, prefix: String, capture_release: bool = true) -> void:
	var button: Button = _button(m.start_menu_layer,name)
	if button == null or not button.is_visible_in_tree():
		errors.append("missing visible button " + name)
		return
	var point: Vector2 = button.get_global_transform_with_canvas() * (button.size*0.5)
	await _raw(point,true)
	await _capture(prefix+"_pressed",true,{"event":"raw engine touch0 press","button":name,"point":[point.x,point.y]})
	await _raw(point,false)
	if capture_release:
		await _capture(prefix+"_released",true,{"event":"raw engine touch0 release","button":name,"point":[point.x,point.y]})

func _menu_ready() -> bool:
	var until: int = Time.get_ticks_msec()+25000
	while Time.get_ticks_msec() < until:
		await process_frame
		if m.start_menu_active and m.get_node_or_null("BootSplashHandoff") == null and m.fade_rect.modulate.a <= 0.02:
			return true
	return false

func _world_ready() -> bool:
	var until: int = Time.get_ticks_msec()+25000
	while Time.get_ticks_msec() < until:
		await process_frame
		if not m.start_menu_active and not m.intro_active and m.get_node_or_null("BootSplashHandoff") == null and m.fade_rect.modulate.a <= 0.02 and m.living_layer.visible and not m._living_world_ref()._suspended():
			return true
	return false

func _run_variant(target: Vector2i, base_out: String, kind: String) -> void:
	variant = kind
	out_dir = base_out.path_join("%dx%d" % [target.x,target.y]).path_join(kind)
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _aspect(target):
		errors.append("aspect readiness failed")
		return
	profile = out_dir.path_join("profiles/startup/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	if kind != "fresh":
		var data: Dictionary = {"schema_version":1,"won":{},"found":{},"pearls":23,"plays":2,"quality":"speedy","music":true,"day_one_active":false,"r30_keep_marker":12345}
		var seed := FileAccess.open(profile,FileAccess.WRITE)
		seed.store_string(JSON.stringify(data))
		seed.close()
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	m._save_state = SaveState.new(m,profile)
	started_ms = Time.get_ticks_msec()
	get_root().add_child(m)
	m._apply_quality("speedy")
	if not await _menu_ready():
		errors.append("natural menu did not settle")
		return
	var before: Dictionary = _progress()
	await _capture("normal_startup")
	await create_timer(2.0).timeout
	await _capture("passive_2s")
	await create_timer(24.0).timeout
	await _capture("passive_26s")
	if _progress() != before or m.living_event_count != 0:
		errors.append("passive menu changed progress/events")
	await _tap("StartMenuOptionsButton","options_open")
	await _tap("StartMenuMusicButton","music_off")
	await _tap("StartMenuMusicButton","music_on")
	await _tap("StartMenuOptionsCloseButton","options_close")
	m.propagate_notification(Node.NOTIFICATION_WM_WINDOW_FOCUS_OUT)
	await _frames(2)
	await _capture("declared_focus_out",true,{"scope":"Explicit engine notification diagnostic,not actualOS/device focus"})
	m.propagate_notification(Node.NOTIFICATION_WM_WINDOW_FOCUS_IN)
	await _frames(2)
	await _capture("declared_focus_in",true,{"scope":"Explicit engine notification diagnostic,not actualOS/device focus"})
	if kind != "fresh":
		await _tap("StartMenuNewGameButton","newgame_request")
		await create_timer(1.6).timeout
		await _capture("newgame_armed")
		var hold: Button = _button(m.start_menu_layer,"StartMenuConfirmNewGameButton")
		var point: Vector2 = hold.get_global_transform_with_canvas()*(hold.size*0.5)
		await _raw(point,true)
		await _capture("newgame_short_hold",true,{"event":"rawtouch0hold less than0.8second","point":[point.x,point.y]})
		await create_timer(0.12).timeout
		await _raw(point,false)
		await _capture("newgame_hold_cancelled",true,{"event":"rawtouch0release before0.8second;noresetcommitted"})
		await _tap("StartMenuKeepGameButton","keep_saved")
		if _progress() != before or m.save_data.get("r30_keep_marker") != 12345:
			errors.append("saved menu cancel changed progress")
		await _tap("StartMenuContinueButton","continue",false)
		if not await _world_ready():
			errors.append("natural Continue did not restore sibling")
		else:
			await _capture("natural_continue_world",false,{"entry":"Actual raw Continue release through production callback;legacy saveday_one_active false"})
			m._build_start_menu()
			await _frames(4)
			await _capture("declared_menu_reentry",true,{"entry":"Direct production menu builder diagnostic atop actual Continue world;not naturalreset/relaunchroute"})
			await create_timer(1.0).timeout
			await _capture("reentry_idle_1s")
			await _tap("StartMenuContinueButton","continue_again",false)
			if await _world_ready():
				await _capture("natural_continue_after_reentry",false)
			else:
				errors.append("Continue after declared reentry didnotsettle")
	var final_progress: Dictionary = _progress()
	var manifest: Dictionary = {"schema":"reef.startup_ambience_retirement_native/1","source_baseline":OS.get_environment("ROOTPIC_REV"),"production_director_sha256":FileAccess.get_sha256("res://scripts/living_world.gd"),"regression_probe_sha256":FileAccess.get_sha256("res://scripts/probe_living_world.gd"),"engine":Engine.get_version_info(),"display_server":DisplayServer.get_name(),"rendering_method":RenderingServer.get_current_rendering_method(),"quality":"speedy","aspect":[target.x,target.y],"variant":kind,"fixture":"Natural scene/newprivateSaveState BEFOREMain;rawviewporttouch input;explicit focus/reentry diagnostics labelled. No IntroOverlaybuild/probeStageoverride/scriptSwap/newart","normal_save_before":normal_before,"normal_save_after":_normal_hashes(),"private_profile_path":profile,"states":states.duplicate(true),"initial_progress":before,"final_progress":final_progress,"errors":errors.duplicate(),"all_game_reachability_complete":false,"human_acceptance":null}
	m.queue_free()
	await _frames(6)
	manifest["teardown_main_valid"] = is_instance_valid(m)
	manifest["normal_save_after_teardown"] = _normal_hashes()
	var json_file := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	json_file.store_string(JSON.stringify(manifest,"\t")+"\n")
	json_file.close()

func _run() -> void:
	normal_before = _normal_hashes()
	var base_out := OS.get_environment("ROOTPIC_OUT")
	if base_out == "":
		quit(2)
		return
	for target: Vector2i in [Vector2i(1280,720),Vector2i(1600,720)]:
		for kind: String in ["fresh","saved_legacy"]:
			await _run_variant(target,base_out,kind)
	if _normal_hashes() != normal_before:
		errors.append("normal save hash changed")
	print("STARTUP_RETIREMENT|FINAL|"+JSON.stringify({"errors":errors,"normal_save_unchanged":_normal_hashes()==normal_before}))
	quit(0 if errors.is_empty() else 1)
