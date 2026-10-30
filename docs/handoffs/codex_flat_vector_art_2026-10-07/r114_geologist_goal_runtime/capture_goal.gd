extends SceneTree
var m: ReefMain
var profile: String
var out_dir: String
var checks: Array[Dictionary] = []
var captures: Array[Dictionary] = []
var surface: OperaGeologySurface
var normal_before: Dictionary
var normal_base: String
var phase: int
var world: OperaCareerWorld2D

func _init() -> void:
	call_deferred("_run")

func _check(label: String, ok: bool) -> void:
	checks.append({"label": label, "pass": ok})
	if not ok:
		push_error(label)

func _hashes() -> Dictionary:
	var result: Dictionary = {}
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old", ".before_new_game", ".before_new_game.bak", ".before_new_game.tmp"]:
		var path: String = normal_base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result

func _frames(n: int) -> void:
	for i: int in range(n):
		await process_frame

func _bind(node: Node) -> void:
	if node is ReefMain:
		m = node as ReefMain
		_check("private dependency bound before ready", not m.is_node_ready())
		m._save_state = SaveState.new(m, profile)

func _capture(label: String) -> void:
	await RenderingServer.frame_post_draw
	var im: Image = root.get_texture().get_image()
	var path: String = out_dir.path_join(label + ".png")
	_check("native frame dimensions " + label, im.get_size() == root.size)
	_check("native save " + label, im.save_png(path) == OK)
	captures.append({"id":label,"path":label + ".png","sha256":FileAccess.get_sha256(path),"size":[im.get_width(),im.get_height()],"source_revision":OS.get_environment("R95_REV"),"goal_resource":world.prop_rect.texture.resource_path,"goal_visible":world.prop_rect.is_visible_in_tree(),"goal_stretch_mode":world.prop_rect.stretch_mode,"goal_mouse_filter":world.prop_rect.mouse_filter,"goal_global_rect":str(world.prop_rect.get_global_rect()),"goal_position":str(world.prop_rect.position),"goal_size":str(world.prop_rect.size),"goal_scale":str(world.prop_rect.scale),"goal_modulate":str(world.prop_rect.modulate),"goal_rotation":world.prop_rect.rotation,"phase":world.phase_index,"task_open":world.task_open,"active":world.active,"surface_snapshot":surface.progress_snapshot(),"main_game":m.game,"stars":m.opera_stars})

func _finish() -> void:
	_check("normal saves unchanged", _hashes() == normal_before)
	var failed: Array = checks.filter(func(x:Dictionary) -> bool:return not bool(x["pass"]))
	var result: Dictionary = {"status":"PASS" if failed.is_empty() else "FAIL","checks":checks,"captures":captures,"normal_before":normal_before,"normal_after":_hashes(),"scope":"OriginalMain synthetic phase3 checkpoint; real seam taps/pull through original completion and curtain-call; not natural wholecareer/formalQA11/device/child/owner evidence."}
	var file: FileAccess = FileAccess.open(out_dir.path_join("RESULT.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(result,"\t"))
	file.close()
	print("R114_NATIVE_RESULT ",result["status"]," checks=",checks.size()," frames=",captures.size())
	quit(0 if failed.is_empty() else 1)

func _touch(pressed: bool, at: Vector2, finger: int = 0) -> void:
	var event := InputEventScreenTouch.new()
	event.index = finger
	event.position = at
	event.pressed = pressed
	surface._gui_input(event)

func _drag(at: Vector2, finger: int = 0) -> void:
	var event := InputEventScreenDrag.new()
	event.index = finger
	event.position = at
	surface._gui_input(event)

func _run() -> void:
	out_dir = OS.get_environment("R95_OUT")
	normal_base = OS.get_environment("R95_NORMAL_BASE")
	var width: int = int(OS.get_environment("R95_WIDTH"))
	phase = int(OS.get_environment("R114_PHASE"))
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600] or normal_base.is_empty():
		quit(2)
		return
	var engine: Dictionary = Engine.get_version_info()
	_check("exact approved engine hash", str(engine.get("hash")) == "ed1daf0bf001b61586d9930840f2f1394092c079")
	_check("Mobile native Windows time1", RenderingServer.get_current_rendering_method() == "mobile" and DisplayServer.get_name() == "Windows" and Engine.time_scale == 1.0)
	normal_before = _hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	var seed: Dictionary = {"schema_version": 1, "save_generation": 7, "won": {}, "found": {}, "pearls": 23, "plays": 3, "skin": "classic", "quality": "speedy", "music": false, "mic": false, "day_one_active": false, "opera_done": false, "custom_fish": [], "custom_friends": [], "opera_geology_checkpoint": {"version": 1, "phase_index": phase}, "flat_vector_private_unknown": {"token": "R95_SYNTHETIC", "keep": [3,7]}}
	var file: FileAccess = FileAccess.open(profile, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed))
	file.close()
	root.mode = Window.MODE_WINDOWED
	root.size = Vector2i(width, 720)
	DisplayServer.window_set_position(Vector2i(-2400, 0))
	DisplayServer.window_set_size(root.size)
	node_added.connect(_bind)
	var packed: PackedScene = load("res://scenes/main.tscn") as PackedScene
	root.add_child(packed.instantiate())
	current_scene = m
	await _frames(12)
	var continue_button: Button = m.find_child("StartMenuContinueButton", true, false) as Button
	_check("original Continue available", continue_button != null and not continue_button.disabled)
	continue_button.pressed.emit()
	await _frames(45)
	_check("start menu retired before world", not m.start_menu_active)
	if m.start_menu_active:
		quit(1)
		return
	m.day_one_active = false
	m._skip_intro()
	m.game = "level2"
	m.g["phase"] = "hall"
	m.g["t"] = 0.0
	m.opera_stars = 0
	# Declared synthetic saved-checkpoint fixture; no naturally earned route claim.
	m.save_data["opera_geology_checkpoint"] = {"version": 1, "phase_index": phase}
	m._castle_rooms_ref().open("library")
	await _frames(8)
	m._start_opera_from_room(16, "library")
	for wait_frame: int in range(180):
		if m.opera_game != null and m.game == "opera":
			break
		await process_frame
	_check("original Main owner-room launcher reached Opera", m.opera_game != null and m.game == "opera")
	if m.opera_game == null:
		quit(1)
		return
	var house: OperaHouse = m.opera_game as OperaHouse
	var act: OperaAct = house.act
	world = act.career_world_2d
	await _frames(8)
	_check("castle room suspended beneath original Opera", not m.castle_room_layer.visible)
	_check("original full Geologist world", world != null and world.career_id == "geologist")
	_check("own saved activity checkpoint restored", world.phase_index == phase)
	if world.phase_index != phase:
		quit(1)
		return
	world._open_task()
	await _frames(16)
	surface = world.surface as OperaGeologySurface
	_check("original activity surface opened", surface != null and surface.mode == ["geology_river", "geology_fossil", "geology_pan", "geology_geode"][phase] and world.task_open)
	_check("Speedy own profile", m.quality == "speedy" and m._save_state.save_path == profile)
	_check("original touch rect", surface.PAN_RECT == Rect2(520, 220, 520, 320))
	var candidate: bool = OS.get_environment("R114_LANE") == "candidate"
	var expected: String = "res://assets/opera/worlds/props/goal_geologist.tres" if candidate else "res://assets/opera/worlds/props/goal_geologist.svg"
	_check("actual required goal source loaded", world.prop_rect != null and world.prop_rect.texture != null and world.prop_rect.texture.resource_path == expected)
	if world.prop_rect == null or world.prop_rect.texture == null:
		_finish()
		return
	var spec: Dictionary = OperaHotspotCatalog.spec("geologist","GEODE")
	_check("same hotspot spec size and presentation", spec.get("size") == Vector2(150,150) and spec.get("presentation") == "painted")
	_check("catalog same correct resource", spec.get("path") == expected)
	_check("goal frame geometry and aspect unchanged", world.prop_rect.size.is_equal_approx(Vector2(220,220)) and world.prop_rect.stretch_mode == TextureRect.STRETCH_KEEP_ASPECT_CENTERED and world.prop_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	_check("goal hidden during actual task", not world.prop_rect.is_visible_in_tree())
	if candidate:
		var goal_alias: AtlasTexture = world.prop_rect.texture as AtlasTexture
		_check("whole native AtlasTexture alias required", goal_alias != null)
		if goal_alias == null:
			_finish()
			return
		_check("alias reuses unchanged whole512 source and full region", goal_alias.atlas.resource_path == "res://assets/opera/worlds/props/geologist_crystal_gallery_painted.png" and goal_alias.region == Rect2(0,0,512,512))
		var art: Image = goal_alias.get_image()
		var source_art: Image = goal_alias.atlas.get_image()
		_check("actual reused source512 with lossless mipmaps", source_art.get_size() == Vector2i(512,512) and source_art.has_mipmaps() and art.get_size() == Vector2i(512,512))
		var source_base: Image = source_art.duplicate() as Image
		source_base.clear_mipmaps()
		var alias_base: Image = art.duplicate() as Image
		alias_base.clear_mipmaps()
		_check("whole alias preserves every RGBA byte", source_base.get_format() == alias_base.get_format() and source_base.get_data() == alias_base.get_data())
		_check("whole transparent corners", art.get_pixel(0,0).a == 0.0 and art.get_pixel(511,511).a == 0.0)
	await _capture("00_task_goal_hidden")
	var before: Dictionary = surface.progress_snapshot().duplicate(true)
	await _frames(10)
	_check("passive cannot complete", surface.progress_snapshot() == before and not world.prop_rect.is_visible_in_tree())
	for index: int in range(surface.GEODE_SEAM_SPOTS.size()):
		var point: Vector2 = surface.geode_seam_spot(index)
		_touch(true,point)
		_touch(false,point)
	_check("five original seam taps mark all", surface._seam_count() == 5)
	var half: Vector2 = surface.geode_half_center()
	_touch(true,half)
	_drag(half + Vector2(100,0))
	_check("partial pull does not reveal goal", not world.prop_rect.is_visible_in_tree() and not surface._completion_emitted)
	_drag(half + Vector2(120,0))
	_touch(false,half + Vector2(120,0))
	_check("ordinary pull completes surface exactly", surface._completion_emitted and is_equal_approx(surface.geode_pull,120.0))
	for wait_frame: int in range(480):
		if world.prop_rect.is_visible_in_tree():break
		await process_frame
	_check("original world completion reveals goal", world.prop_rect.is_visible_in_tree() and not world.active and not world.task_open)
	if not world.prop_rect.is_visible_in_tree():
		_finish()
		return
	await _capture("01_finale_appearance")
	await _frames(12)
	await _capture("02_finale_bounce")
	await _frames(36)
	await _capture("03_finale_settled")
	_check("settled goal same source/frame/white material", world.prop_rect.texture.resource_path == expected and world.prop_rect.size == Vector2(220,220) and world.prop_rect.modulate == Color.WHITE and is_zero_approx(world.prop_rect.rotation))
	_check("original curtain call anchor", str(world.prop_rect.get_meta("anchor_station")) == "curtain_call_spotlight")
	_finish()
