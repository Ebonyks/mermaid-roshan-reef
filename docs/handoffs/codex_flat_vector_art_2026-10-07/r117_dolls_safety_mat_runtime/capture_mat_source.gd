extends SceneTree
var m: ReefMain
var surface: DollsGame.DollsNurserySurface
var profile: String
var out_dir: String
var normal_base: String
var normal_before: Dictionary
var checks: Array[Dictionary] = []
var captures: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")

func _check(label: String, ok: bool) -> void:
	checks.append({"label":label,"pass":ok})
	if not ok:
		push_error(label)

func _hashes() -> Dictionary:
	var result: Dictionary = {}
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old", ".before_new_game", ".before_new_game.bak", ".before_new_game.tmp"]:
		var path: String = normal_base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result

func _frames(n: int) -> void:
	for index: int in range(n):
		await process_frame

func _bind(node: Node) -> void:
	if node is ReefMain:
		m = node as ReefMain
		_check("private save bound before ready", not m.is_node_ready())
		m._save_state = SaveState.new(m, profile)

func _capture(label: String, fixture: String) -> void:
	surface.queue_redraw()
	await _frames(2)
	await RenderingServer.frame_post_draw
	var im: Image = root.get_texture().get_image()
	var path: String = out_dir.path_join(label + ".png")
	_check("native dimensions " + label, im.get_size() == root.size)
	_check("native PNG " + label, im.save_png(path) == OK)
	captures.append({"id":label,"path":label+".png","sha256":FileAccess.get_sha256(path),"dimensions":[im.get_width(),im.get_height()],"source_revision":OS.get_environment("R117_REV"),"fixture":fixture,"game":m.game,"caught":surface.caught,"missed":surface.missed,"normal_time_scale":Engine.time_scale,"safe_mat_rect":str(surface.safe_mat_rect()),"panel_global_rect":str(surface.get_global_rect()),"safe_landings":surface.safe_landings.duplicate(true),"input_live_t":surface.input_live_t})

func _finish() -> void:
	_check("normal11 save hashes unchanged", _hashes() == normal_before)
	var failed: Array = checks.filter(func(x:Dictionary) -> bool:return not bool(x["pass"]))
	var result: Dictionary = {"status":"PASS" if failed.is_empty() else "FAIL","checks":checks,"captures":captures,"normal_before":normal_before,"normal_after":_hashes(),"scope":"OriginalMain/Faron/Dolls with configured deterministic faller/edge positions and real engine-driven miss/owned catch. No natural allroutes, formalQA11/device/child/owner claim."}
	var file: FileAccess = FileAccess.open(out_dir.path_join("RESULT.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(result,"\t"))
	file.close()
	print("R117_NATIVE_RESULT ",result["status"]," checks=",checks.size()," frames=",captures.size())
	quit(0 if failed.is_empty() else 1)

func _run() -> void:
	out_dir = OS.get_environment("R117_OUT")
	normal_base = OS.get_environment("R117_NORMAL_BASE")
	var width: int = int(OS.get_environment("R117_WIDTH"))
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280,1600] or normal_base.is_empty():
		quit(2)
		return
	_check("exact approved engine", str(Engine.get_version_info().get("hash")) == "ed1daf0bf001b61586d9930840f2f1394092c079")
	_check("native Mobile Windows normal time", RenderingServer.get_current_rendering_method() == "mobile" and DisplayServer.get_name() == "Windows" and Engine.time_scale == 1.0)
	normal_before = _hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	var data: Dictionary = {"schema_version":1,"save_generation":7,"won":{},"found":{},"pearls":23,"plays":3,"skin":"classic","quality":"speedy","music":false,"mic":false,"day_one_active":false,"opera_done":false,"custom_fish":[],"custom_friends":[],"flat_vector_private_unknown":{"token":"R117_CONFIGURED_ONLY","keep":[3,7]}}
	var file: FileAccess = FileAccess.open(profile,FileAccess.WRITE)
	file.store_string(JSON.stringify(data))
	file.close()
	root.mode = Window.MODE_WINDOWED
	root.size = Vector2i(width,720)
	DisplayServer.window_set_position(Vector2i(-2400,0))
	DisplayServer.window_set_size(root.size)
	node_added.connect(_bind)
	var packed: PackedScene = load("res://scenes/main.tscn") as PackedScene
	root.add_child(packed.instantiate())
	current_scene = m
	await _frames(12)
	var button: Button = m.find_child("StartMenuContinueButton",true,false) as Button
	_check("original Continue available", button != null and not button.disabled)
	button.pressed.emit()
	await _frames(45)
	_check("original start menu retired", not m.start_menu_active)
	if m.start_menu_active:
		_finish()
		return
	m.day_one_active = false
	m._skip_intro()
	# Use the original owner return before the configured legacy Faron caller.
	m._exit_level2()
	await _frames(12)
	_check("original Castle room owner retired before Faron", m.castle_room_layer == null or not m.castle_room_layer.visible)
	var friend: Dictionary = {}
	for candidate: Dictionary in m.friends:
		if String(candidate.get("game","")) == "dolls":
			friend = candidate
			break
	_check("original Faron caller found", not friend.is_empty())
	friend["found"] = true
	m._start_game(friend)
	for index: int in range(180):
		if m.game == "dolls" and m.g.get("dolls_surface") != null:
			break
		await process_frame
	surface = m.g.get("dolls_surface") as DollsGame.DollsNurserySurface
	_check("original Faron Dolls surface reached", m.game == "dolls" and surface != null)
	if surface == null:
		_finish()
		return
	await _frames(6)
	_check("private Speedy and Canvas panel", m.quality == "speedy" and m._save_state.save_path == profile and surface.size == Vector2(1024,608))
	_check("original threegoal and nofail", surface.goal == 3 and bool(surface.get_meta("no_fail",false)) and surface.cradle_texture == null and surface.pillows_texture == null)
	_check("original exact safe mat envelope", surface.safe_mat_rect().is_equal_approx(Rect2(35.84,471.2,952.32,136.8)))
	_check("same selected skin behind parent", m.g.get("dolls_catcher") is TextureRect and (m.g["dolls_catcher"] as TextureRect).show_behind_parent and (m.g["dolls_catcher"] as TextureRect).texture.resource_path == m.skin_sprite_path())
	if OS.get_environment("R117_LANE") == "candidate":
		var texture: Texture2D = surface.get("safe_mat_texture") as Texture2D
		_check("whole painted mat loaded", texture != null and texture.resource_path == "res://assets/dolls/safety_mat_painted.png")
		_check("whole lossless mipmapped1024x256", texture.get_size() == Vector2(1024,256) and texture.get_image().has_mipmaps())
	surface.set_process(false)
	surface.fallers.clear()
	surface._spawn_baby()
	var entry: Dictionary = surface.fallers[0]
	entry["x"] = 0.5
	entry["base_x"] = 0.5
	entry["sway"] = 0.0
	entry["y"] = 0.44
	surface.fallers[0] = entry
	await _capture("01_falling_mat", "Configured centre faller at0.44; original live Main/Faron game and authored tiles")
	entry["y"] = 0.905
	surface.fallers[0] = entry
	surface.set_process(true)
	for index: int in range(30):
		if surface.missed >= 1 and not surface.safe_landings.is_empty():
			break
		await process_frame
	surface.set_process(false)
	_check("real passive miss never scores or wins", surface.missed == 1 and surface.caught == 0 and m.game == "dolls" and surface.active)
	_check("real safe landing bounded by original mat", not surface.safe_landings.is_empty() and surface.safe_mat_rect().encloses(surface.safe_landing_rect(surface.safe_landings[0])))
	await _capture("02_passive_safe_landing", "Original engine-driven passive miss from configured0.905 faller; no reward")
	surface.fallers.clear()
	surface.safe_landings.clear()
	surface.safe_landings.append({"x":0.08,"texture":1,"time":1.25})
	_check("leftmost valid landing geometry contained", surface.safe_mat_rect().encloses(surface.safe_landing_rect(surface.safe_landings[0])))
	await _capture("03_left_safe_edge", "Configured legal x0.08 extreme safe landing; frozen physics for contact inspection")
	surface.safe_landings[0] = {"x":0.92,"texture":2,"time":1.25}
	_check("rightmost valid landing geometry contained", surface.safe_mat_rect().encloses(surface.safe_landing_rect(surface.safe_landings[0])))
	await _capture("04_right_safe_edge", "Configured legal x0.92 extreme safe landing; frozen physics for contact inspection")
	surface.safe_landings.clear()
	surface.fallers.clear()
	surface._spawn_baby()
	entry = surface.fallers[0]
	entry["x"] = 0.55
	entry["base_x"] = 0.55
	entry["sway"] = 0.0
	entry["y"] = 0.72
	surface.fallers[0] = entry
	var touch := InputEventScreenTouch.new()
	touch.index = 37
	touch.position = Vector2(0.55*surface.size.x,0.72*surface.size.y)
	touch.pressed = true
	surface._gui_input(touch)
	surface.set_process(true)
	for index: int in range(30):
		if surface.caught == 1:
			break
		await process_frame
	surface.set_process(false)
	touch.pressed = false
	surface._gui_input(touch)
	_check("real onefinger input catches exactlyone", surface.caught == 1 and surface.input_live_t > 0.0 and surface.settled.size() == 1 and m.game == "dolls")
	await _capture("05_owned_catch_mat_remains", "Actual native engine catch after owned single touch; private session below goal")
	_check("no medal or whole goal awarded", int(m.medals.get("dolls",0)) == 0 and not bool(friend.get("won",false)))
	m._leave_current_activity()
	_check("original synchronous neutral teardown restores control ownership", m.game == "" and not m.touch_control_blocks.has("dolls_game") and m.find_child("DollsCatchLayer",true,false) == null)
	await _frames(3)
	_check("original automatic courtyard return keeps Dolls retired", m.game == "level2" and not m.touch_control_blocks.has("dolls_game") and m.find_child("DollsCatchLayer",true,false) == null)
	_finish()
