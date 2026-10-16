extends SceneTree
## Original display entry / source-owned NewGame reload; private user:// namespace before Main.
var m: ReefMain
var out_dir := ""
var normal_path := ""
var private_path := ""
var states: Array[Dictionary] = []
var events: Array[Dictionary] = []
var checks: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var old_custom := false
var old_custom_name := ""
var pointer_samples: Array[Dictionary] = []
var root_id := 0
var settings_configured := false
func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var row: Dictionary = {}
	var base := normal_path
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old", ".before_new_game", ".before_new_game.tmp", ".before_new_game.old"]:
		var f := base + suffix
		row[suffix] = FileAccess.get_sha256(f) if FileAccess.file_exists(f) else "absent"
	return row

func _frames(count: int) -> void:
	for i: int in range(count):
		await process_frame

func _wait(predicate: Callable, seconds: float = 14.0) -> bool:
	var deadline := Time.get_ticks_msec() + int(seconds * 1000.0)
	while Time.get_ticks_msec() < deadline:
		if bool(predicate.call()):
			return true
		await process_frame
	return bool(predicate.call())

func _check(label: String, passed: bool) -> bool:
	checks.append({"label": label, "pass": passed})
	if not passed:
		errors.append(label)
	return passed

func _aspect(width: int) -> bool:
	root.mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		root.size = Vector2i(width, 720)
		DisplayServer.window_set_size(Vector2i(width, 720))
		await process_frame
		var image: Image = root.get_texture().get_image()
		if image != null and image.get_size() == Vector2i(width, 720):
			return true
	return false



func _private_hashes() -> Dictionary:
	var row: Dictionary = {}
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old", ".before_new_game", ".before_new_game.tmp", ".before_new_game.old"]:
		var f := private_path + suffix
		row[suffix] = FileAccess.get_sha256(f) if FileAccess.file_exists(f) else "absent"
	return row

func _disk() -> Dictionary:
	if not FileAccess.file_exists(private_path):
		return {}
	var d: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(private_path))
	return {"generation": d.get("save_generation"), "quality": d.get("quality"), "plays": d.get("plays"), "pearls": d.get("pearls"), "day_one_active": d.get("day_one_active"), "day_one_arrival_plane_media_seen": d.get("day_one_arrival_plane_media_seen"), "day_one_story_clips_seen": d.get("day_one_story_clips_seen"), "custom_fish": d.get("custom_fish"), "custom_friends": d.get("custom_friends")}

func _nodes(node: Node, rows: Array[Dictionary]) -> void:
	var item := node as CanvasItem
	if item != null and item.is_visible_in_tree():
		var row := {"path": str(node.get_path()), "class": node.get_class(), "name": str(node.name), "z_index": item.z_index}
		var c := node as Control
		if c != null:
			var p: Vector2 = c.get_global_transform_with_canvas() * Vector2.ZERO
			var end: Vector2 = c.get_global_transform_with_canvas() * c.size
			row["native_rect"] = [p.x,p.y,end.x-p.x,end.y-p.y]
		if node is Label or node is Button:
			row["text"] = node.text
		if node is Button:
			row["disabled"] = node.disabled
		if node is TextureRect and node.texture != null:
			row["texture_path"] = node.texture.resource_path
		if node is Sprite2D and node.texture != null:
			row["texture_path"] = node.texture.resource_path
			row["centered"] = node.centered
			row["scale"] = [node.scale.x,node.scale.y]
		rows.append(row)
	for child: Node in node.get_children():
		_nodes(child, rows)

func _snapshot() -> Dictionary:
	var rows: Array[Dictionary] = []
	for layer: CanvasLayer in [m.start_menu_layer,m.intro_layer,m._day_one_story_clip_layer]:
		if is_instance_valid(layer):
			_nodes(layer, rows)
	var clip: DayOneStoryClips = m._day_one_story_clip
	var clip_data: Dictionary = {"active": is_instance_valid(clip)}
	if is_instance_valid(clip):
		clip_data["id"] = clip.movie_id
		clip_data["playing"] = clip.player.is_playing() if clip.player != null else false
		clip_data["stream_path"] = clip.player.stream.resource_path if clip.player != null and clip.player.stream != null else ""
	return {"game": m.game,"phase": m.g.get("phase"),"quality":m.quality,"main_id":m.get_instance_id(),"first_session":m.first_session,"intro_active":m.intro_active,"intro_layer_present":is_instance_valid(m.intro_layer),"intro_overlay_constructed":m._intro_overlay != null,"start_menu_active":m.start_menu_active,"start_menu_layer_present":is_instance_valid(m.start_menu_layer),"has_saved_game":m.has_saved_game,"day_one_active":m.day_one_is_active(),"root_reset_marker":root.has_meta(StartMenu.DAY_ONE_AFTER_RESET_META),"normal_user_path":normal_path,"current_user_path":ProjectSettings.globalize_path("user://reef_save.json"),"save_dependency_path":m._save_state.save_path,"private_hashes":_private_hashes(),"disk":_disk(),"clip":clip_data,"tree_paused":paused,"living_stage":m.living_stage_id,"nodes":rows,"ticks_msec":Time.get_ticks_msec()}

func _capture(id: String, lane := "BOUNDED_CURRENT_DISPLAY_ENTRY") -> void:
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != root.size or image.save_png(path) != OK:
		errors.append("bad framebuffer " + id)
		return
	states.append({"id":id,"path":id+".png","dimensions":[image.get_width(),image.get_height()],"sha256":FileAccess.get_sha256(path),"classification":lane,"snapshot":_snapshot()})
	print("ENTRY77|CAPTURE|",id)

func _button(name: String) -> Button:
	return m.start_menu_layer.find_child(name,true,false) as Button if is_instance_valid(m.start_menu_layer) else null

func _point(c: Control) -> Vector2:
	return c.get_global_transform_with_canvas() * (c.size*0.5)

func _input_at(p: Vector2, down: bool, target: String) -> void:
	var e := InputEventScreenTouch.new()
	e.index = 77
	e.position = p
	e.pressed = down
	events.append({"down":down,"native":[p.x,p.y],"target":target,"ticks_msec":Time.get_ticks_msec(),"private_path":ProjectSettings.globalize_path("user://reef_save.json")})
	root.push_input(e,true)

func _tap(name: String) -> bool:
	var c := _button(name)
	if not _check("original visible button " + name,c != null and c.is_visible_in_tree() and not c.disabled):
		return false
	var p := _point(c)
	_input_at(p,true,name)
	await _frames(1)
	_input_at(p,false,name)
	await _frames(3)
	return true

func _boot() -> bool:
	var scene := load("res://scenes/main.tscn") as PackedScene
	m = scene.instantiate() as ReefMain
	root.add_child(m)
	current_scene = m
	root_id = m.get_instance_id()
	if not await _wait(func() -> bool: return is_instance_valid(m.start_menu_layer) and m.get_node_or_null("BootSplashHandoff") == null,18.0):
		errors.append("original display startup timeout")
		return false
	return _check("source display uses StartMenu not IntroOverlay",m.start_menu_active and m.intro_active and m.intro_layer == null and m._intro_overlay == null and ProjectSettings.globalize_path(m._save_state.save_path) == private_path)

func _hand_sample() -> Dictionary:
	var hand := m.start_menu_layer.find_child("StartMenuKeepGameGhostHand",true,false) as Sprite2D
	var keep := _button("StartMenuKeepGameButton")
	var p: Vector2 = hand.get_global_transform_with_canvas() * (Vector2(217,447)-hand.texture.get_size()*0.5)
	var inv: Transform2D = keep.get_global_transform_with_canvas().affine_inverse()
	var local := inv*p
	return {"native_tip":[p.x,p.y],"local_in_keep":[local.x,local.y],"keep_size":[keep.size.x,keep.size.y],"inside":Rect2(Vector2.ZERO,keep.size).has_point(local),"hand_position":[hand.position.x,hand.position.y],"hand_scale":[hand.scale.x,hand.scale.y],"centered":hand.centered,"texture_path":hand.texture.resource_path,"ticks_msec":Time.get_ticks_msec()}

func _confirm(prefix: String) -> bool:
	if not await _tap("StartMenuNewGameButton"):
		return false
	await _capture(prefix + "_arm_delay")
	var b := _button("StartMenuConfirmNewGameButton")
	if not _check("source newgame initially delayed",b != null and b.disabled):
		return false
	if not await _wait(func() -> bool: return not b.disabled,3.0):
		errors.append("source arm delay timeout")
		return false
	return true

func _retire() -> void:
	if is_instance_valid(m):
		m.queue_free()
		await _frames(14)
		m = null

func _exercise() -> void:
	if not await _boot():
		return
	await _capture("fresh_menu_default", "EXCLUDED_PRE_SPEEDY_DEFAULT")
	_check("fresh private profile has no saved adventure",not m.has_saved_game and _button("StartMenuContinueButton").disabled)
	if not await _tap("StartMenuOptionsTab"):
		return
	await _capture("fresh_options_default", "EXCLUDED_PRE_SPEEDY_DEFAULT")
	if m.quality != "speedy":
		if not await _tap("StartMenuQualityButton"):
			return
	if m.music_on:
		if not await _tap("StartMenuMusicButton"):
			return
	if m.mic_on:
		if not await _tap("StartMenuMicButton"):
			return
	_check("original options select persistedSpeedy and muted isolated run",m.quality=="speedy" and not m.music_on and not m.mic_on and _disk().get("quality")=="speedy")
	await _capture("options_speedy")
	if not await _tap("StartMenuOptionsCloseButton"):
		return
	await _capture("menu_speedy")
	if not await _confirm("keep"):
		return
	await _capture("keep_ready")
	var before: Dictionary = _private_hashes()
	var until := Time.get_ticks_msec()+1000
	while Time.get_ticks_msec() < until:
		await RenderingServer.frame_post_draw
		pointer_samples.append(_hand_sample())
	_check("natural source hand bob samples",pointer_samples.size()>20)
	var all_inside := true
	for row: Dictionary in pointer_samples:
		all_inside = all_inside and bool(row.inside)
	_check("source-projected hand tip inside KeepGame throughout natural bob",all_inside)
	var tip: Dictionary = _hand_sample()
	var p := Vector2(tip.native_tip[0],tip.native_tip[1])
	_input_at(p,true,"actual_keep_hand_tip")
	await _frames(1)
	await _capture("keep_tip_pressed")
	_input_at(p,false,"actual_keep_hand_tip")
	await _frames(5)
	await _capture("keep_tip_canceled_reset")
	_check("actual source hand-tip input cancels without reset",_private_hashes()==before and m.get_instance_id()==root_id and not _button("StartMenuKeepGameButton").is_visible_in_tree())
	if not await _confirm("start"):
		return
	var start := _button("StartMenuConfirmNewGameButton")
	p = _point(start)
	_input_at(p,true,"short_confirm")
	await create_timer(0.2).timeout
	await _capture("short_hold")
	_input_at(p,false,"short_confirm")
	await _frames(8)
	await _capture("short_release_no_reset")
	_check("short confirm leaves current private save exact",_private_hashes()==before and m.get_instance_id()==root_id)
	_input_at(p,true,"intentional_confirm_hold")
	await create_timer(0.4).timeout
	await _capture("intentional_hold_half")
	if not await _wait(func() -> bool: return current_scene is ReefMain and current_scene.get_instance_id()!=root_id,8.0):
		errors.append("original NewGame did not reload current scene")
		return
	m = current_scene as ReefMain
	_input_at(p,false,"intentional_confirm_hold")
	await _frames(8)
	_check("original reload keeps private user namespace/default SaveState",ProjectSettings.globalize_path(m._save_state.save_path)==private_path and m.quality=="speedy" and m._intro_overlay==null and m.intro_layer==null and not m.start_menu_active)
	await _capture("new_main_dayone_entry")
	if not await _wait(func() -> bool: return is_instance_valid(m._day_one_story_clip) or bool(m.g.get("day_one_media_request","")!=""),10.0):
		errors.append("opening clip or source fallback was not requested")
		return
	await _frames(14)
	await _capture("opening_or_fallback")
	await create_timer(2.0).timeout
	await _capture("opening_or_fallback_later")
	if is_instance_valid(m._day_one_story_clip):
		if not await _wait(func() -> bool: return not is_instance_valid(m._day_one_story_clip),42.0):
			errors.append("original opening did not terminate naturally")
			return
	await _frames(45)
	await _capture("after_opening")
	_check("source opening restores scene without legacy intro",not paused and m.intro_layer==null and m._intro_overlay==null and m.day_one_is_active() and m.game=="level2" and m.quality=="speedy")
	await _retire()
	if not await _boot():
		return
	await _capture("reentry_start_menu")
	_check("source reentry sees private saved adventure",m.has_saved_game and not _button("StartMenuContinueButton").disabled)
	if not await _tap("StartMenuContinueButton"):
		return
	await _frames(45)
	await _capture("continued_dayone")
	_check("original Continue preserves DayOne and skips legacy IntroOverlay",m.day_one_is_active() and not m.start_menu_active and m.intro_layer==null and m._intro_overlay==null and ProjectSettings.globalize_path(m._save_state.save_path)==private_path)

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.major)!=4 or int(engine.minor)!=7 or int(engine.patch)!=2 or engine.status!="stable" or engine.build!="official" or RenderingServer.get_current_rendering_method()!="mobile" or DisplayServer.get_name()=="headless":
		quit(1)
		return
	var width := int(OS.get_environment("R77_WIDTH"))
	out_dir = OS.get_environment("R77_OUT")
	var private_name := OS.get_environment("R77_PRIVATE_NAME")
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280,1600] or private_name.is_empty() or private_name.contains("/") or private_name.contains("\\") or private_name.contains(":"):
		quit(1)
		return
	normal_path = ProjectSettings.globalize_path("user://reef_save.json")
	normal_before = _normal_hashes()
	old_custom = bool(ProjectSettings.get_setting("application/config/use_custom_user_dir",false))
	old_custom_name = String(ProjectSettings.get_setting("application/config/custom_user_dir_name",""))
	ProjectSettings.set_setting("application/config/use_custom_user_dir",true)
	ProjectSettings.set_setting("application/config/custom_user_dir_name",private_name)
	private_path = ProjectSettings.globalize_path("user://reef_save.json")
	settings_configured = true
	var fresh := true
	for v: Variant in _private_hashes().values():
		fresh = fresh and v=="absent"
	var isolated := private_path!=normal_path and private_path.get_base_dir().get_file()==private_name and fresh
	_check("private user namespace remaps before any Main load and is fresh",isolated)
	DirAccess.make_dir_recursive_absolute(out_dir)
	if isolated:
		DirAccess.make_dir_recursive_absolute(private_path.get_base_dir())
		if await _aspect(width):
			await _exercise()
	await _retire()
	ProjectSettings.set_setting("application/config/use_custom_user_dir",old_custom)
	ProjectSettings.set_setting("application/config/custom_user_dir_name",old_custom_name)
	_check("normal user path restored after source teardown",ProjectSettings.globalize_path("user://reef_save.json")==normal_path)
	_check("normal eleven save-name hashes unchanged",_normal_hashes()==normal_before)
	var report := {"schema":"reef.intro_entry_ownership/1","source_revision":OS.get_environment("R77_REV"),"engine":engine,"renderer":RenderingServer.get_current_rendering_method(),"display":DisplayServer.get_name(),"aspect":[width,720],"time_scale":Engine.time_scale,"private_path":private_path,"normal_path":normal_path,"private_hashes_final":_private_hashes(),"normal_before":normal_before,"normal_after":_normal_hashes(),"states":states,"events":events,"checks":checks,"errors":errors,"pointer_samples":pointer_samples,"observer_status":"PASS" if errors.is_empty() else "FAIL","actual_child_data":false,"production_changes":[],"scope":"Global user-dir isolation before original Main and source NewGame reload; no SaveState injection or normal save-content snapshot/restore. Native original Options select Speedy/mute creating an owned private options save, then original delayed/canceled/short/hold NewGame, real reload toDayOne opening and original Continue. Initial desktop Sparkly/default views excluded. No forced game/world/action/timer/intro state or source/art edits. Named legacy IntroOverlay display absence in these actual entries is not global dynamic/native unreachability. Movie/source/context/QA11/device/child/owner acceptance stay separate."}
	var f := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	f.store_string(JSON.stringify(report,"\t",true)+"\n")
	f.close()
	print("ENTRY77|RESULT|",report.observer_status,"|",errors)
	quit(0 if errors.is_empty() else 1)
