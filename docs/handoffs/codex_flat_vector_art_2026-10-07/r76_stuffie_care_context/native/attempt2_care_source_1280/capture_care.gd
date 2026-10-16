extends SceneTree
## R76 read-only observer / original viewport inputs; private synthetic SaveState before Ready.
var m: ReefMain
var out_dir := ""
var profile := ""
var states: Array[Dictionary] = []
var events: Array[Dictionary] = []
var checks: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var seed: Dictionary = {}
var boot_count := 0
func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var row: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
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


func _disk() -> Dictionary:
	if not FileAccess.file_exists(profile):
		return {}
	var d: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(profile))
	return {"care_points": d.get("care_points"), "companion": d.get("companion"), "unknown": d.get("flat_vector_private_unknown"), "pearls": d.get("pearls"), "custom_fish": d.get("custom_fish"), "custom_friends": d.get("custom_friends"), "save_generation": d.get("save_generation")}

func _nodes(node: Node, rows: Array[Dictionary]) -> void:
	var c := node as Control
	if c != null and c.is_visible_in_tree():
		var pos: Vector2 = c.get_global_transform_with_canvas() * Vector2.ZERO
		var end: Vector2 = c.get_global_transform_with_canvas() * c.size
		var row := {"path": str(c.get_path()), "name": str(c.name), "class": c.get_class(), "native_rect": [pos.x, pos.y, end.x-pos.x, end.y-pos.y], "scale": [c.scale.x, c.scale.y], "mouse_filter": c.mouse_filter}
		if c is Label or c is Button:
			var f: Font = c.get_theme_font("font")
			row["text"] = c.text
			row["font_class"] = f.get_class()
			row["font_path"] = f.resource_path
			row["font_size"] = c.get_theme_font_size("font_size")
			row["font_name"] = f.call("get_font_name") if f.has_method("get_font_name") else "not_exposed"
			row["font_authority"] = StorybookUI.TYPOGRAPHY_FONT_AUTHORITY
		if c is Button:
			row["disabled"] = c.disabled
		if c is TextureRect and c.texture != null:
			row["texture_path"] = c.texture.resource_path
			row["texture_size"] = [c.texture.get_width(), c.texture.get_height()]
		rows.append(row)
	for child: Node in node.get_children():
		_nodes(child, rows)

func _snapshot() -> Dictionary:
	var nodes: Array[Dictionary] = []
	if m.companion_care_layer != null:
		_nodes(m.companion_care_layer, nodes)
	return {"game": m.game, "phase": m.g.get("phase"), "nav": m._navigation_ref().top_id(), "care_open": m.companion_care_layer != null, "pause_open": m.pause_panel.visible, "companion": m.companion_id, "care_points": m.care_points, "want": m.companion_want, "queue": m.companion_want_queue.duplicate(), "want_cool": m.companion_want_cool, "care_t": m.companion_care_t, "bruises": m.companion_bruises, "stars": m._companion_ref()._star_pips(), "pearls": m.pearl_count, "disk": _disk(), "nodes": nodes, "ticks_msec": Time.get_ticks_msec()}

func _capture(id: String, lane := "BOUNDED_CURRENT_CARE_CONTEXT") -> void:
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != root.size or image.save_png(path) != OK:
		errors.append("framebuffer " + id)
		return
	states.append({"id": id, "path": id + ".png", "dimensions": [image.get_width(), image.get_height()], "sha256": FileAccess.get_sha256(path), "classification": lane, "snapshot": _snapshot()})
	print("CARE76|CAPTURE|", id)

func _tap(c: Control) -> bool:
	if not _check("original visible control", c != null and c.is_visible_in_tree() and not (c is Button and c.disabled)):
		return false
	var p: Vector2 = c.get_global_transform_with_canvas() * (c.size * 0.5)
	for down: bool in [true, false]:
		var e := InputEventScreenTouch.new()
		e.index = 76
		e.position = p
		e.pressed = down
		events.append({"target": str(c.get_path()), "down": down, "native": [p.x,p.y], "care_points_before": m.care_points, "want_before": m.companion_want, "ticks_msec": Time.get_ticks_msec()})
		root.push_input(e, true)
		await _frames(1)
	await _frames(3)
	return true

func _boot() -> bool:
	var scene := load("res://scenes/main.tscn") as PackedScene
	m = scene.instantiate() as ReefMain
	m._save_state = SaveState.new(m, profile)
	root.add_child(m)
	current_scene = m
	boot_count += 1
	await _frames(3)
	if not _check("private dependency before Ready", m._save_state.save_path == profile):
		return false
	if not await _wait(func() -> bool: return m.get_node_or_null("BootSplashHandoff") == null, 18.0):
		errors.append("splash timeout")
		return false
	var button: Button = m.start_menu_layer.find_child("StartMenuContinueButton", true, false) as Button if m.start_menu_layer != null else null
	if not await _tap(button):
		return false
	if not await _wait(func() -> bool: return not m.start_menu_active and not m.intro_active and m.fade_rect.modulate.a <= 0.02, 18.0):
		errors.append("startup timeout")
		return false
	# Declared source API startup seam only. No source/action/want/timer/state mutation after this entry.
	m._enter_level2_now(true, false, false)
	await _frames(35)
	return _check("production Canvas promenade root", m.game == "level2" and m.g.get("phase") == "promenade" and m._navigation_ref().top_id() == "")

func _open(prefix: String) -> bool:
	if not await _tap(m.global_navigation_button):
		return false
	if not await _wait(func() -> bool: return m.pause_panel.visible, 3.0):
		errors.append("Menu did not open")
		return false
	await _capture(prefix + "_root_menu", "EXCLUDED_ENTRY_LIFECYCLE_CONTEXT")
	var b := m.pause_panel.find_child("MenuStuffieButton", true, false) as Button
	if not await _tap(b):
		return false
	if not await _wait(func() -> bool: return m.companion_care_layer != null, 3.0):
		errors.append("Stuffie did not open care")
		return false
	return _check("original care nav owns overlay", m._navigation_ref().top_id() == "stuffie_care" and not m.pause_panel.visible)

func _back(prefix: String) -> bool:
	if not await _tap(m.global_navigation_button):
		return false
	if not await _wait(func() -> bool: return m.companion_care_layer == null, 3.0):
		errors.append("Back did not close care")
		return false
	await _capture(prefix + "_root_restored", "EXCLUDED_ENTRY_LIFECYCLE_CONTEXT")
	return _check("original Back returns promenade", m.game == "level2" and m.g.get("phase") == "promenade" and m._navigation_ref().top_id() == "")

func _action(id: String) -> bool:
	# Source redraw queues old children before building new ones: names may become automatic.
	# Resolve the original pressed callback's bound want ID; never invoke it directly.
	for node: Node in m.companion_care_stage.get_children():
		var button := node as Button
		if button == null or button.is_queued_for_deletion():
			continue
		for connection: Dictionary in button.get_signal_connection_list("pressed"):
			var action: Callable = connection["callable"]
			if action.get_method() == "_choose_menu_care" and action.get_bound_arguments() == [id]:
				return await _tap(button)
	return _check("original care callback for " + id, false)

func _retire() -> void:
	if is_instance_valid(m):
		m.set_process(false)
		m.queue_free()
		await _frames(12)
		m = null

func _exercise() -> void:
	if not await _boot():
		return
	await _capture("initial_root", "EXCLUDED_ENTRY_LIFECYCLE_CONTEXT")
	if not await _open("neutral"):
		return
	await _capture("neutral_points3")
	var before := m.care_points
	var cool := m.companion_want_cool
	await _frames(45)
	await _capture("neutral_passive_wait")
	_check("care overlay passive wait awards no progress", m.care_points == before and m.companion_want == "" and is_equal_approx(m.companion_want_cool, cool))
	if not await _back("neutral"):
		return
	if not await _wait(func() -> bool: return not m.companion_want.is_empty(), 35.0):
		errors.append("natural first want timeout")
		return
	var asked := m.companion_want
	await _capture("natural_want_root", "EXCLUDED_ENTRY_LIFECYCLE_CONTEXT")
	if not await _open("requested"):
		return
	await _capture("requested_" + asked)
	_check("natural first want freezes in menu", m.care_points == 3 and not asked.is_empty())
	for id: String in ["feed", "nap", "bath", "cuddle", "play"]:
		if id == asked:
			continue
		if not await _action(id):
			return
		await _capture("unasked_" + id + "_feedback")
		await _frames(16)
		await _capture("unasked_" + id + "_settled")
		_check("unasked care " + id + " awards no point", m.care_points == 3 and m.companion_want == asked)
	if not await _action(asked):
		return
	await _capture("requested_fulfilled_feedback")
	_check("one requested care crosses point3 to4 once", m.care_points == 4 and m.companion_want == "" and _disk().get("care_points") == 4)
	await _frames(16)
	await _capture("level_up_settled")
	if not await _back("level_up") or not await _open("reopen"):
		return
	await _capture("reopen_points4")
	if not await _action(asked):
		return
	await _capture("repeated_unasked_feedback")
	_check("repeated satisfied action does not farm progress", m.care_points == 4 and _disk().get("care_points") == 4)
	if not await _back("repeat"):
		return
	await _retire()
	if not await _boot() or not await _open("reload"):
		return
	await _capture("new_main_reload_points4")
	_check("original newMain reload preserves progress/identity/unknown/custom data", m.care_points == 4 and m.companion_id == "eagle" and _disk().get("unknown") == seed.flat_vector_private_unknown and _disk().get("custom_fish") == seed.custom_fish and _disk().get("custom_friends") == seed.custom_friends)
	if not await _back("reload"):
		return
	_check("care awards no pearls", m.pearl_count == 23)

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.major) != 4 or int(engine.minor) != 7 or int(engine.patch) != 2 or engine.status != "stable" or engine.build != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		quit(1)
		return
	var width := int(OS.get_environment("R76_WIDTH"))
	out_dir = OS.get_environment("R76_OUT")
	if width not in [1280,1600] or out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir):
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "day_one_active": false, "day_one_giant_dust_bunny_boss_defeated": true, "day_one_completed_rooms": DayOneDirector.ROOM_ORDER, "day_one_cleaned_rooms": DayOneDirector.ROOM_ORDER, "day_one_giant_dust_bunny_boss_triggered": true, "chapter2_active": true, "chapter2_unlocked_opera_mask": 0x0449, "skin": "classic", "music": false, "mic": false, "quality": "speedy", "pearls": 23, "pearls_ever": 23, "companion": "eagle", "care_points": 3, "stuffie_wins": {"rescued_eagle": true}, "crafts": {}, "stickers": {}, "custom_fish": [[0.9,0.3,0.3,1.0,0.8,0.2]], "custom_friends": [["cat",0.95,0.7,0.85,0.6,0.4,0.9]], "flat_vector_private_unknown": {"token": "R76_SYNTHETIC_ONLY", "keep": [4,7]}}
	var f := FileAccess.open(profile, FileAccess.WRITE)
	f.store_string(JSON.stringify(seed, "\t", true) + "\n")
	f.close()
	if await _aspect(width):
		await _exercise()
	else:
		errors.append("native viewport did not settle")
	await _retire()
	_check("normal eleven save-name hashes unchanged", normal_before == _normal_hashes())
	var report := {"schema": "reef.stuffie_care_context/1", "source_revision": OS.get_environment("R76_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "aspect": [width,720], "time_scale": Engine.time_scale, "seed": seed, "boot_count": boot_count, "normal_before": normal_before, "normal_after": _normal_hashes(), "states": states, "events": events, "checks": checks, "errors": errors, "observer_status": "PASS" if errors.is_empty() else "FAIL", "actual_child_data": false, "production_changes": [], "scope": "Original Main/private dependency before Ready, original Continue, declared production promenade API bootstrap, then original Menu/Stuffie/Back/care controls and natural timers. Five actions, one natural first want, unasked/repeated versus requested progress, growth point3-to4 and newMain reload. No queue/bruised/during-care state or earned full route, finalQA11/device/child/owner acceptance; no source/visual/timer override."}
	f = FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(report, "\t", true) + "\n")
	f.close()
	print("CARE76|RESULT|", report.observer_status, "|", errors)
	quit(0 if errors.is_empty() else 1)
