extends SceneTree
var m: ReefMain
var profile: String
var out_dir: String
var checks: Array[Dictionary] = []
var captures: Array[Dictionary] = []
var surface: OperaGeologySurface
var normal_before: Dictionary
var normal_base: String
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
	var seed: Dictionary = {"schema_version": 1, "save_generation": 7, "won": {}, "found": {}, "pearls": 23, "plays": 3, "skin": "classic", "quality": "speedy", "music": false, "mic": false, "day_one_active": false, "opera_done": false, "custom_fish": [], "custom_friends": [], "opera_geology_checkpoint": {"version": 1, "phase_index": 2}, "flat_vector_private_unknown": {"token": "R95_SYNTHETIC", "keep": [3,7]}}
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
	m.save_data["opera_geology_checkpoint"] = {"version": 1, "phase_index": 2}
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
	_check("own saved PAN checkpoint restored", world.phase_index == 2)
	if world.phase_index != 2:
		quit(1)
		return
	world._open_task()
	await _frames(4)
	surface = world.surface as OperaGeologySurface
	_check("original PAN surface opened", surface != null and surface.mode == "geology_pan" and world.task_open)
	_check("Speedy own profile", m.quality == "speedy" and m._save_state.save_path == profile)
	_check("original touch rect", surface.PAN_RECT == Rect2(520, 220, 520, 320))
	_check("required painted mint Canvas texture", surface.mineral_mint_texture is CanvasTexture)
	var mint_canvas: CanvasTexture = surface.mineral_mint_texture as CanvasTexture
	if mint_canvas == null:
		quit(1)
		return
	var mint_image: Image = mint_canvas.diffuse_texture.get_image()
	_check("actual imported mint texture512square", mint_image.get_size() == Vector2i(512, 512))
	_check("actual imported mint mipmaps", mint_image.has_mipmaps())
	_check("actual imported mint transparent corner", mint_image.get_pixel(0, 0).a == 0.0)
	_check("actual imported mint opaque body", mint_image.get_pixel(256, 256).a > 0.9)
	_check("current mint Canvas linear mipmap filter", mint_canvas.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS)

	for variant: String in ["blue", "lavender"]:
		var tex: Texture2D = surface.mineral_blue_texture if variant == "blue" else surface.mineral_lavender_texture
		_check("required painted " + variant + " Canvas texture", tex is CanvasTexture)
		if not tex is CanvasTexture:
			quit(1)
			return
		var canvas: CanvasTexture = tex as CanvasTexture
		var specimen: Image = canvas.diffuse_texture.get_image()
		_check(variant + " actual imported512square", specimen.get_size() == Vector2i(512, 512))
		_check(variant + " actual imported mipmaps", specimen.has_mipmaps())
		# The preserved blue source has one alpha1 corner pixel, measured CUTOUT_OK.
		_check(variant + " measured neartransparent corner", specimen.get_pixel(0, 0).a <= 1.0 / 255.0 + 0.0001)
		_check(variant + " opaque authored body", specimen.get_pixel(256, 256).a > 0.9)
		_check(variant + " linear mipmap filter", canvas.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS)

	var expected: bool = OS.get_environment("R95_VARIANT") == "candidate"
	_check("expected source or painted texture", (surface.pan_texture != null) == expected)
	if expected:
		_check("runtime texture <=1024", surface.pan_texture.get_width() <= 1024 and surface.pan_texture.get_height() <= 1024)
	await _capture("01_pan_start")
	var center: Vector2 = surface.PAN_RECT.get_center()
	_touch(true, center)
	_drag(center + Vector2(150,0), 1)
	_check("second finger cannot wash", surface.pan_reversals == 0)
	for swing: int in range(surface.PAN_REQUIRED_REVERSALS + 1):
		_drag(center + Vector2(150.0 if swing % 2 == 0 else -150.0, 0))
		await _frames(1)
		if swing == 4:
			_check("real washing progresses", surface.pan_reversals == 4 and surface.pan_wash > 0)
			await _capture("02_pan_partial")
		if swing == 8:
			await _capture("03_pan_near_complete")
	_touch(false, surface.pointer_pos)
	_check("original washing completion", surface.pan_reversals >= 9 and surface.pan_wash == 1.0 and surface.pan_minerals == 3)
	_check("original completion signal state", surface._completion_emitted)
	await _capture("04_pan_complete")
	var final_snapshot: Dictionary = surface.progress_snapshot()
	house.queue_free()
	m.queue_free()
	await _frames(3)
	_check("normal eleven save/archive hashes unchanged", normal_before == _hashes())
	var ok: bool = true
	for row: Dictionary in checks:
		ok = ok and bool(row["pass"])
	file = FileAccess.open(out_dir.path_join("RESULT.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"status": "PASS" if ok else "FAIL", "source_revision": OS.get_environment("R95_REV"), "variant": OS.get_environment("R95_VARIANT"), "fixture": "Own saved-PAN checkpoint; original Main/OperaAct/Geologist world and one-finger GUI events, not naturally earned route proof or QA11", "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "quality": "speedy", "checks": checks, "captures": captures, "final_snapshot": final_snapshot, "normal_before": normal_before, "normal_after": _hashes(), "actual_child_data": false, "generation_calls": 0}, "  "))
	file.close()
	print("R95|RESULT|", "PASS" if ok else "FAIL", "|CHECKS|", checks.size())
	quit(0 if ok else 1)
