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
	var routes: CastleCareerRoutes = m._castle_career_routes_ref()
	var button: Button = routes.button_for_act(16)
	var crest: TextureRect = button.get_node("CareerCrest") as TextureRect if button != null else null
	captures.append({"id": label,"path": label + ".png","sha256": FileAccess.get_sha256(path),"size": [im.get_width(),im.get_height()],"source_revision":OS.get_environment("R95_REV"),"main_game":m.game,"start_menu_active":m.start_menu_active,"castle_room":m.castle_room_id,"castle_visible":m.castle_room_layer.visible,"button_global_rect":str(button.get_global_rect()) if button != null else "absent","crest_global_rect":str(crest.get_global_rect()) if crest != null else "absent","crest_resource":crest.texture.resource_path if crest != null and crest.texture != null else "absent","stars":m.opera_stars})

func _finish() -> void:
	_check("normal11 files unchanged", _hashes() == normal_before)
	var failed: Array = checks.filter(func(x: Dictionary) -> bool:return not bool(x["pass"]))
	var result: Dictionary = {"status":"PASS" if failed.is_empty() else "FAIL","checks":checks,"captures":captures,"normal_before":normal_before,"normal_after":_hashes(),"scope":"OriginalMain synthetic freeplay Library room card and Geologist launcher; no natural/child/device/formalQA11 claim.","formal_QA11":null,"device":null,"child":null,"owner":null}
	var file: FileAccess = FileAccess.open(out_dir.path_join("RESULT.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(result,"\t"))
	file.close()
	print("R113_NATIVE_RESULT ",result["status"]," checks=",checks.size()," frames=",captures.size())
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
	phase = int(OS.get_environment("R113_PHASE"))
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
	await _frames(16)
	var routes: CastleCareerRoutes = m._castle_career_routes_ref()
	routes.sync()
	var button: Button = routes.button_for_act(16)
	_check("original Library three picture cards visible", routes.root.visible and routes.buttons.size() == 3)
	_check("original geologist route button", button != null and not button.disabled and button.visible and int(button.get_meta("act_index")) == 16)
	if button == null:
		_finish()
		return
	_check("same button generous hit geometry", button.size == CastleCareerRoutes.CARD_SIZE and button.size.x >= 48 and button.size.y >= 48)
	var crest: TextureRect = button.get_node("CareerCrest") as TextureRect
	_check("same crest50px geometry", crest != null and crest.position == Vector2(52,98) and crest.size == Vector2(50,50) and crest.mouse_filter == Control.MOUSE_FILTER_IGNORE and crest.stretch_mode == TextureRect.STRETCH_KEEP_ASPECT_CENTERED)
	_check("real bound crest exists", crest.texture != null)
	var candidate: bool = OS.get_environment("R113_LANE") == "candidate"
	var expected: String = "res://assets/opera/worlds/ui/crests/opera_crest_geologist.png" if candidate else "res://assets/opera/worlds/ui/crests/opera_crest_geologist.svg"
	_check("exact expected crest bound", crest.texture.resource_path == expected)
	_check("original owner room mapping", CastleCareerRoutes.room_for_act(16) == "library" and CastleCareerRoutes.route_matches("library",16))
	_check("Speedy own profile", m.quality == "speedy" and m._save_state.save_path == profile)
	var original_stars: int = m.opera_stars
	await _frames(30)
	_check("passive card cannot earn star", m.opera_stars == original_stars and m.opera_game == null)
	await _capture("01_library_unearned")
	if not candidate:
		_finish()
		return
	var art: Image = crest.texture.get_image()
	_check("whole256 lossless imported image with mipmaps", art.get_size() == Vector2i(256,256) and art.has_mipmaps())
	_check("painted crest transparent corners", art.get_pixel(0,0).a == 0.0 and art.get_pixel(255,255).a == 0.0)
	_check("painted crest linear mipmap filter", crest.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS)
	button.grab_focus()
	await _frames(5)
	await _capture("02_library_focused")
	_check("focus cannot earn star", m.opera_stars == original_stars)
	m.opera_stars = 1 << 16
	routes.sync()
	await _frames(5)
	_check("earned state uses same whole crest", (button.get_node("CareerCrest") as TextureRect).texture.resource_path == expected)
	_check("earned pearl visible", bool((button.get_node("CareerPearl") as Panel).get_meta("complete")))
	await _capture("03_library_earned")
	m.opera_stars = original_stars
	routes.clear()
	await _frames(3)
	routes.sync()
	await _frames(16)
	button = routes.button_for_act(16)
	_check("teardown reentry restores same card and crest", routes.root.visible and button != null and (button.get_node("CareerCrest") as TextureRect).texture.resource_path == expected)
	await _capture("04_library_reentry")
	button.pressed.emit()
	for wait_frame: int in range(180):
		if m.opera_game != null and m.game == "opera":
			break
		await process_frame
	await _frames(16)
	_check("original card signal launches same Geologist owner route", m.opera_game != null and m.game == "opera" and not m.castle_room_layer.visible)
	if m.opera_game != null:
		var house: OperaHouse = m.opera_game as OperaHouse
		world = house.act.career_world_2d
		_check("original Geologist world and saved phase", world != null and world.career_id == "geologist" and world.phase_index == phase)
		_check("launch gives no unearned reward", m.opera_stars == original_stars)
		await _capture("05_geologist_launched")
	_finish()
