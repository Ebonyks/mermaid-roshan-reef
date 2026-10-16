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
var cache_directories: Array[String] = []
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



func _prepare_cache_tree(source: String, relative: String = "", depth: int = 0) -> bool:
	# Directory structure only, via the same engine filesystem that owns user://.
	# Normal cache file/save contents are never copied or parsed.
	if depth > 4 or cache_directories.size() > 4096:
		return _check("cache directory bound", false)
	var base := private_path.get_base_dir().simplify_path()
	var target := base.path_join("shader_cache").path_join(relative).simplify_path()
	if not target.begins_with(base + "/shader_cache"):
		return _check("private engine cache containment", false)
	if DirAccess.make_dir_recursive_absolute(target) != OK:
		return _check("private engine cache directory creation", false)
	cache_directories.append(relative)
	for name: String in DirAccess.get_directories_at(source.path_join(relative)):
		if name == "." or name == ".." or name.validate_filename() != name:
			return _check("cache directory name validation", false)
		if not _prepare_cache_tree(source, relative.path_join(name), depth + 1):
			return false
	return true

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
	return {"game": m.game,"phase": m.g.get("phase"),"quality":m.quality,"main_id":m.get_instance_id(),"first_session":m.first_session,"intro_active":m.intro_active,"intro_layer_present":is_instance_valid(m.intro_layer),"intro_overlay_constructed":m._intro_overlay != null,"start_menu_active":m.start_menu_active,"start_menu_layer_present":is_instance_valid(m.start_menu_layer),"has_saved_game":m.has_saved_game,"day_one_active":m.day_one_is_active(),"root_reset_marker":root.has_meta(StartMenu.DAY_ONE_AFTER_RESET_META),"normal_user_path":normal_path,"current_user_path":ProjectSettings.globalize_path("user://reef_save.json"),"save_dependency_path":m._save_state.save_path,"private_hashes":_private_hashes(),"disk":_disk(),"clip":clip_data,"tree_paused":paused,"living_stage":m.living_stage_id,"nodes":rows,"world":_world_snapshot(),"ticks_msec":Time.get_ticks_msec()}

func _capture_now(id: String, lane := "BOUNDED_CURRENT_PROMENADE_ORIGINAL_INPUT") -> void:
	var image: Image = root.get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != root.size or image.save_png(path) != OK:
		errors.append("bad framebuffer " + id)
		return
	states.append({"id":id,"path":id+".png","dimensions":[image.get_width(),image.get_height()],"sha256":FileAccess.get_sha256(path),"classification":lane,"snapshot":_snapshot()})
	print("PROMENADE79|CAPTURE|",id)
func _capture(id: String, lane := "BOUNDED_CURRENT_PROMENADE_ORIGINAL_INPUT") -> void:
	await RenderingServer.frame_post_draw
	_capture_now(id,lane)
func _v(v: Vector2) -> Array:
	return [v.x,v.y]
func _world_snapshot() -> Dictionary:
	var targets: Array[Dictionary] = []
	var rows: Array[Dictionary] = []
	var layer: CanvasLayer = m.g.get("lagoon_canvas_layer") as CanvasLayer
	if is_instance_valid(layer):
		_nodes(layer,rows)
	for value: Variant in m.g.get("lagoon_promenade_targets",[]) as Array:
		var target: Dictionary = value as Dictionary
		var node: Node2D = target.get("node") as Node2D
		var glow: Sprite2D = target.get("highlight") as Sprite2D
		var row: Dictionary = {"id":target.get("id"),"kind":target.get("kind"),"payload":target.get("payload"),"radius_px":target.get("radius_px")}
		if is_instance_valid(node):
			row["node_path"] = str(node.get_path())
			row["position_master"] = _v(node.position)
			row["source_hit_point"] = _v(m._lagoon_promenade_ref().screen_from_master(node.position))
			row["source_texture"] = node.texture.resource_path if node is Sprite2D and node.texture != null else ""
		if is_instance_valid(glow):
			row["highlight_path"] = str(glow.get_path())
			row["highlight_scale"] = _v(glow.scale)
			row["highlight_position"] = _v(glow.position)
			row["highlight_native_origin"] = _v(glow.get_global_transform_with_canvas()*Vector2.ZERO)
			row["highlight_color"] = [glow.modulate.r,glow.modulate.g,glow.modulate.b,glow.modulate.a]
			row["highlight_texture_class"] = glow.texture.get_class() if glow.texture != null else ""
			var pointers: Array[Dictionary] = []
			for child: Node in glow.get_children():
				if child is Polygon2D:
					var points: Array = []
					for point: Vector2 in child.polygon:
						points.append(_v(child.get_global_transform_with_canvas()*point))
					pointers.append({"name":str(child.name),"native_vertices":points,"color":[child.color.r,child.color.g,child.color.b,child.color.a]})
			row["pointers"] = pointers
		targets.append(row)
	var play: Dictionary = m.g.get("lagoon_play_anim",{}) as Dictionary
	var card: Sprite2D = m.g.get("lagoon_roshan_card") as Sprite2D
	var actor: Dictionary = {}
	if is_instance_valid(card):
		actor = {"texture":card.texture.resource_path if card.texture != null else "","position":_v(card.position),"native_origin":_v(card.get_global_transform_with_canvas()*Vector2.ZERO),"scale":_v(card.scale),"rotation":card.rotation,"flip_h":card.flip_h,"visible":card.is_visible_in_tree()}
	return {"phase":m.g.get("phase"),"game":m.game,"wall_pics_count":m.wall_pics.size(),"legacy_lagoon_constructed":m._sky_lagoon != null,"promenade_constructed":m._sky_lagoon_promenade != null,"focus":m.g.get("lagoon_promenade_focus",""),"master_x":m.g.get("lagoon_master_x"),"walk_goal":str(m.g.get("lagoon_walk_goal_master")),"targets":targets,"actor":actor,"play":{"kind":play.get("kind",""),"phase":play.get("phase",""),"frame_index":play.get("frame_index",-1),"t":play.get("t"),"dur":play.get("dur")},"nodes":rows}
func _world_tap(p: Vector2, label: String) -> void:
	_input_at(p,true,label)
	await _frames(2)
	_input_at(p,false,label)
	await _frames(4)
func _slide_target() -> Dictionary:
	for value: Variant in m.g.get("lagoon_promenade_targets",[]) as Array:
		var target: Dictionary = value as Dictionary
		if String(target.get("id","")) == "slide":
			return target
	return {}
func _slide_point() -> Vector2:
	var node: Node2D = _slide_target().get("node") as Node2D
	return m._lagoon_promenade_ref().screen_from_master(node.position)
func _observe_slide() -> void:
	await create_timer(4.0).timeout
	await _capture("promenade_entry")
	if not _check("source NewGame selects live promenade and empty legacy wall array",m.game=="level2" and String(m.g.get("phase"))=="promenade" and m.wall_pics.is_empty() and m._sky_lagoon==null and m._sky_lagoon_promenade!=null and not _slide_target().is_empty()):
		return
	var walk_steps := 0
	while walk_steps < 8 and (_slide_point().x < 210.0 or _slide_point().x > root.size.x-180.0):
		var direction: float = 0.25 if _slide_point().x < 210.0 else 0.75
		await _world_tap(Vector2(float(root.size.x)*direction,520.0),"original_ground_travel")
		await create_timer(1.25).timeout
		walk_steps += 1
		await _capture("travel_"+str(walk_steps))
	if not _check("source-owned travel exposes slide target",Rect2(Vector2(150,130),Vector2(root.size.x-300,420)).has_point(_slide_point())):
		return
	await _capture("slide_idle")
	await _world_tap(_slide_point(),"original_slide_focus")
	await _capture("slide_focused")
	if not _check("original tap focuses slide",String(m.g.get("lagoon_promenade_focus",""))=="slide"):
		return
	await _world_tap(_slide_point(),"original_slide_activate")
	var play: Dictionary = m.g.get("lagoon_play_anim",{}) as Dictionary
	if not _check("second original tap starts current slide action without race entry",String(play.get("kind",""))=="slide" and m.game=="level2" and String(m.g.get("phase"))=="promenade"):
		return
	var observed: Dictionary = {}
	var deadline := Time.get_ticks_msec()+15000
	while not (m.g.get("lagoon_play_anim",{}) as Dictionary).is_empty() and Time.get_ticks_msec()<deadline:
		await RenderingServer.frame_post_draw
		play = m.g.get("lagoon_play_anim",{}) as Dictionary
		if not play.is_empty():
			var key := String(play.get("phase",""))+"_"+str(play.get("frame_index",-1))
			if not observed.has(key):
				observed[key] = true
				_capture_now("slide_"+key)
	await _frames(12)
	await _capture("slide_completed")
	_check("current action returns naturally to source promenade",(m.g.get("lagoon_play_anim",{}) as Dictionary).is_empty() and m.game=="level2" and String(m.g.get("phase"))=="promenade" and m.wall_pics.is_empty())
	_check("four source pose indices observed",observed.has("action_0") and observed.has("action_1") and observed.has("action_2") and observed.has("action_3"))

func _observe_neighbor(kind: String) -> void:
	var target: Dictionary = {}
	for value: Variant in m.g.get("lagoon_promenade_targets",[]) as Array:
		var row: Dictionary = value as Dictionary
		if String(row.get("id","")) == kind:
			target = row
	if not _check("source neighbor target exists "+kind,not target.is_empty()):
		return
	var node: Node2D = target.get("node") as Node2D
	var p: Vector2 = m._lagoon_promenade_ref().screen_from_master(node.position)
	if not _check("source neighbor target on current screen "+kind,Rect2(Vector2(150,130),Vector2(root.size.x-300,420)).has_point(p)):
		return
	await _capture(kind+"_idle")
	await _world_tap(p,"original_"+kind+"_focus")
	await _capture(kind+"_focused")
	if not _check("original neighbor focus "+kind,String(m.g.get("lagoon_promenade_focus",""))==kind):
		return
	await _world_tap(p,"original_"+kind+"_activate")
	var play: Dictionary = m.g.get("lagoon_play_anim",{}) as Dictionary
	if not _check("original neighbor action "+kind,String(play.get("kind",""))==kind and m.game=="level2" and String(m.g.get("phase"))=="promenade"):
		return
	var observed: Dictionary = {}
	var deadline := Time.get_ticks_msec()+20000
	while not (m.g.get("lagoon_play_anim",{}) as Dictionary).is_empty() and Time.get_ticks_msec()<deadline:
		await RenderingServer.frame_post_draw
		play = m.g.get("lagoon_play_anim",{}) as Dictionary
		if not play.is_empty():
			var key := String(play.get("phase",""))+"_"+str(play.get("frame_index",-1))
			if not observed.has(key):
				observed[key] = true
				_capture_now(kind+"_"+key)
	await _frames(12)
	await _capture(kind+"_completed")
	_check("source neighbor natural return "+kind,(m.g.get("lagoon_play_anim",{}) as Dictionary).is_empty() and m.game=="level2" and String(m.g.get("phase"))=="promenade" and m.wall_pics.is_empty())
	_check("four source neighbor pose indices "+kind,observed.has("action_0") and observed.has("action_1") and observed.has("action_2") and observed.has("action_3"))

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
	await _capture(prefix + "_arm_delay", "EXCLUDED_BOOTSTRAP_CONTROL")
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
	if not await _tap("StartMenuOptionsTab"):
		return
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
	if not await _tap("StartMenuOptionsCloseButton"):
		return
	await _capture("bootstrap_menu", "EXCLUDED_BOOTSTRAP_CONTROL")
	if not await _confirm("bootstrap_newgame"):
		return
	var start := _button("StartMenuConfirmNewGameButton")
	var p := _point(start)
	_input_at(p,true,"original_confirm_hold")
	if not await _wait(func() -> bool: return current_scene is ReefMain and current_scene.get_instance_id()!=root_id,8.0):
		errors.append("original held NewGame did not reload")
		return
	m = current_scene as ReefMain
	_input_at(p,false,"original_confirm_hold")
	await _frames(8)
	_check("real reload keeps source SaveState private andSpeedy",ProjectSettings.globalize_path(m._save_state.save_path)==private_path and m.quality=="speedy" and not m.start_menu_active)
	if not await _wait(func() -> bool: return is_instance_valid(m._day_one_story_clip) or bool(m.g.get("day_one_media_request","")!=""),10.0):
		errors.append("opening clip/fallback not requested")
		return
	if is_instance_valid(m._day_one_story_clip):
		if not await _wait(func() -> bool: return not is_instance_valid(m._day_one_story_clip),42.0):
			errors.append("source opening did not end naturally")
			return
	await _frames(45)
	await _observe_slide()
	if errors.is_empty():
		await _observe_neighbor("swing")
	if errors.is_empty():
		await _observe_neighbor("seesaw")

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.major)!=4 or int(engine.minor)!=7 or int(engine.patch)!=2 or engine.status!="stable" or engine.build!="official" or RenderingServer.get_current_rendering_method()!="mobile" or DisplayServer.get_name()=="headless":
		quit(1)
		return
	var width := int(OS.get_environment("R79_WIDTH"))
	out_dir = OS.get_environment("R79_OUT")
	var private_name := OS.get_environment("R79_PRIVATE_NAME")
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
		if _prepare_cache_tree(normal_path.get_base_dir().path_join("shader_cache")) and await _aspect(width):
			await _exercise()
	await _retire()
	ProjectSettings.set_setting("application/config/use_custom_user_dir",old_custom)
	ProjectSettings.set_setting("application/config/custom_user_dir_name",old_custom_name)
	_check("normal user path restored after source teardown",ProjectSettings.globalize_path("user://reef_save.json")==normal_path)
	_check("normal eleven save-name hashes unchanged",_normal_hashes()==normal_before)
	var report := {"schema":"reef.promenade_slide_ownership/1","source_revision":OS.get_environment("R79_REV"),"engine":engine,"renderer":RenderingServer.get_current_rendering_method(),"display":DisplayServer.get_name(),"aspect":[width,720],"time_scale":Engine.time_scale,"private_path":private_path,"normal_path":normal_path,"private_hashes_final":_private_hashes(),"cache_directory_structure_only":cache_directories,"normal_before":normal_before,"normal_after":_normal_hashes(),"states":states,"events":events,"checks":checks,"errors":errors,"pointer_samples":pointer_samples,"observer_status":"PASS" if errors.is_empty() else "FAIL","actual_child_data":false,"production_changes":[],"scope":"Global user-dir isolation before original Main and source NewGame reload; no SaveState injection or normal save-content snapshot/restore. Native original Options select Speedy/mute creating an owned private options save, then original delayed/canceled/short/hold NewGame, real reload toDayOne opening and original Continue. Initial desktop Sparkly/default views excluded. No forced game/world/action/timer/intro state or source/art edits. Named legacy IntroOverlay display absence in these actual entries is not global dynamic/native unreachability. Movie/source/context/QA11/device/child/owner acceptance stay separate."}
	var f := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	f.store_string(JSON.stringify(report,"\t",true)+"\n")
	f.close()
	print("PROMENADE79|RESULT|",report.observer_status,"|",errors)
	quit(0 if errors.is_empty() else 1)
