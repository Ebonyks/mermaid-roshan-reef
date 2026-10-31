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
	captures.append({"id":label,"path":label+".png","sha256":FileAccess.get_sha256(path),"size":[im.get_width(),im.get_height()],"source_revision":OS.get_environment("R95_REV"),"phase":world.phase_index,"task_open":world.task_open,"geology_work_open":world.backdrop_node.get_meta("geology_work_open",false),"backdrop_rect":str(world.backdrop_node.get_global_rect()),"painting":world.backdrop_node.painting != null,"tiles":world.backdrop_node.world_tiles.size(),"station_count":world.station_nodes.size(),"stars":m.opera_stars,"surface_snapshot":surface.progress_snapshot() if surface != null else {}})

func _finish() -> void:
	_check("normal saves unchanged", _hashes() == normal_before)
	var failed: Array = checks.filter(func(x:Dictionary) -> bool:return not bool(x["pass"]))
	var result: Dictionary = {"status":"PASS" if failed.is_empty() else "FAIL","checks":checks,"captures":captures,"normal_before":normal_before,"normal_after":_hashes(),"scope":"OriginalMain/Library/Geologist synthetic phase0/2 checkpoint; real room overview to activity visibility transition at two aspects. No natural allcareer or formal/device/child/owner claim."}
	var file: FileAccess = FileAccess.open(out_dir.path_join("RESULT.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(result,"\t"))
	file.close()
	print("R116_NATIVE_RESULT ",result["status"]," checks=",checks.size()," frames=",captures.size())
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
	phase = int(OS.get_environment("R116_PHASE"))
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
	_check("closed room overview owns foreground", not world.task_open and not bool(world.backdrop_node.get_meta("geology_work_open",false)))
	_check("actual current code room owns pixels", world.backdrop_node.painting == null and world.backdrop_node.world_tiles.is_empty())
	_check("original four station nodes", world.station_nodes.size() == 4)
	_check("Speedy private profile", m.quality == "speedy" and m._save_state.save_path == profile)
	var rock_path: String = "res://assets/opera/worlds/hotspots/geologist_layered_rock_painted.png"
	_check("retired flat SVG cannot load", not ResourceLoader.exists("res://assets/opera/worlds/hotspots/geologist_layered_rock.svg"))
	_check("unchanged catalog validation", OperaHotspotCatalog.validate_specs().is_empty())
	var hotspot: OperaWorldHotspot2D = world.station_nodes[phase] as OperaWorldHotspot2D
	_check("original current station armed", hotspot != null and hotspot.armed)
	_check("actual layered rock source", hotspot.source_path == rock_path and hotspot.object_texture != null and hotspot.object_texture.resource_path == rock_path)
	_check("whole512 lossless mipmapped cutout", hotspot.object_texture.get_size() == Vector2(512,512) and hotspot.object_texture.get_image().has_mipmaps())
	_check("unchanged phase presentation", hotspot.presentation == ("painted" if phase == 0 else "overlay"))
	_check("unchanged phase motion", hotspot.motion == ("pulse" if phase == 0 else "bounce"))
	_check("unchanged phase object size", hotspot.object_size.is_equal_approx(Vector2(128,128) if phase == 0 else Vector2(112,112)))
	_check("original onefinger hit size", hotspot.touch_button != null and hotspot.hit_size.x >= 112 and hotspot.hit_size.y >= 112)
	await _capture("01_station_overview")
	await _frames(10)
	_check("passive overview cannot progress", world.phase_index == phase and not world.task_open and m.opera_stars == 0)
	world._open_task()
	await _frames(16)
	surface = world.surface as OperaGeologySurface
	_check("original activity opened", surface != null and surface.mode == ["geology_river","geology_fossil","geology_pan","geology_geode"][phase] and world.task_open)
	_check("original guard hides foreground during task", bool(world.backdrop_node.get_meta("geology_work_open",false)))
	_check("activity loaded-only source exact", surface.rock_texture != null and surface.rock_texture.resource_path == rock_path)
	await _capture("02_task_foreground_hidden")
	_finish()
