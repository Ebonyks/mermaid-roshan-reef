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
	captures.append({"id": label, "path": label + ".png", "sha256": FileAccess.get_sha256(path), "size": [im.get_width(), im.get_height()], "snapshot": surface.progress_snapshot(), "pan_visual_x": surface.pan_visual_x, "pan_texture": {"path": surface.pan_texture.resource_path, "size": str(surface.pan_texture.get_size())} if surface.pan_texture != null else {}, "world_phase": world.phase_index, "start_menu_active": m.start_menu_active, "main_game": m.game, "castle_layer_visible": m.castle_room_layer.visible, "world_visible": world.visible, "root_canvas_size": str(surface.size)})

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
	phase = int(OS.get_environment("R110_PHASE"))
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
	var pools: Array[Texture2D] = [surface.river_source_texture, surface.river_sink_dry_texture, surface.river_sink_full_texture]
	for pool_index: int in range(pools.size()):
		var canvas: CanvasTexture = pools[pool_index] as CanvasTexture
		_check("required pool CanvasTexture " + str(pool_index), canvas != null)
		if canvas == null:
			quit(1)
			return
		var art: Image = canvas.diffuse_texture.get_image()
		_check("actual pool512 and mipmaps " + str(pool_index), art.get_size() == Vector2i(512,512) and art.has_mipmaps())
		_check("pool transparent corners " + str(pool_index), art.get_pixel(0,0).a == 0.0 and art.get_pixel(511,511).a == 0.0)
		_check("pool linear mipmap filter " + str(pool_index), canvas.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS)
	_check("original river brush/cells", surface.RIVER_BRUSH_RADIUS == 46.0 and surface.RIVER_COLS == 9 and surface.RIVER_ROWS == 5)
	_check("fixed shared hit geometry", surface.WORK_RECT == Rect2(330,130,860,490))
	await _capture("01_initial")
	var initial: Dictionary = surface.progress_snapshot().duplicate(true)
	await _frames(15)
	_check("passive cannot excavate or fill receiver", surface.progress_snapshot() == initial and not surface._river_connected())
	var finish: Vector2 = surface.river_path_point(surface.RIVER_PATH.size() - 1)
	_touch(true,finish)
	_touch(false,finish)
	_check("isolated receiver excavation stays dry", not surface._river_connected() and surface.river_wet[26])
	await _capture("02_isolated_receiver_dry")
	var isolated: Dictionary = surface.progress_snapshot().duplicate(true)
	var restored := OperaGeologySurface.new()
	restored.configure("geology_river",Color.WHITE,1,"R110_private_checkpoint")
	restored.restore_progress(JSON.parse_string(JSON.stringify(isolated)))
	_check("JSON retains isolated dry receiver excavation", restored.progress_snapshot() == isolated and not restored._river_connected())
	_check("restore has no transient owner", restored.touch_owner == -1 and not restored.held)
	restored.free()
	_touch(true,surface.river_path_point(0))
	var after_press: Dictionary = surface.progress_snapshot().duplicate(true)
	_drag(surface.river_path_point(1),1)
	_check("wrong finger cannot connect painted pools", surface.progress_snapshot() == after_press)
	_drag(surface.river_path_point(1))
	_touch(false,surface.pointer_pos)
	var released: Dictionary = surface.progress_snapshot().duplicate(true)
	surface.cancel_input()
	_check("cancel retains earned channel without owner", surface.progress_snapshot() == released and surface.touch_owner == -1 and not surface.held)
	await _capture("03_source_released_partial")
	_touch(true,surface.river_path_point(1))
	for path_index: int in range(2,surface.RIVER_PATH.size()):
		_drag(surface.river_path_point(path_index))
		if path_index == 5:
			_check("partial connected source leaves receiver dry", not surface._river_connected())
			await _capture("04_partial_channel")
		if path_index == 10:
			_check("near receiver gap still dry", not surface._river_connected())
			await _capture("05_near_receiver_dry")
	_touch(false,surface.pointer_pos)
	_check("connected route fills receiving basin", surface._river_connected())
	_check("original input completes selected activity", surface.progress() == 1.0 and surface._completion_emitted)
	await _capture("06_complete_connected")
	var final_snapshot: Dictionary = surface.progress_snapshot()
	house.queue_free()
	m.queue_free()
	await _frames(3)
	_check("normal eleven save/archive hashes unchanged", normal_before == _hashes())
	var ok: bool = true
	for row: Dictionary in checks:
		ok = ok and bool(row["pass"])
	file = FileAccess.open(out_dir.path_join("RESULT.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"status": "PASS" if ok else "FAIL", "source_revision": OS.get_environment("R95_REV"), "fixture": "Own saved-phase checkpoint, original Main/Opera/Geologist and real one-finger GUI events; not naturally earned/training/QA11 or device evidence", "phase": phase, "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "quality": "speedy", "checks": checks, "captures": captures, "normal_before": normal_before, "normal_after": _hashes(), "final_snapshot": final_snapshot}, "  "))
	file.close()
	print("R110|RESULT|", "PASS" if ok else "FAIL", "|CHECKS|", checks.size())
	quit(0 if ok else 1)
