extends "res://export/flat_vector_r71/base_capture.gd"
## R66 original display entry observer; no gameplay/visual overrides or route bootstrap.
var mode: String = ""
var bindings: Array[Dictionary] = []
var normal_base: String = ""
var source_main: PackedScene

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base: String = normal_base if not normal_base.is_empty() else ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old", ".before_new_game", ".before_new_game.tmp", ".before_new_game.old"]:
		result[suffix] = FileAccess.get_sha256(base + suffix) if FileAccess.file_exists(base + suffix) else "absent"
	return result

func _bind_private_before_ready(node: Node) -> void:
	if node is ReefMain:
		var main: ReefMain = node as ReefMain
		if main.is_node_ready() or profile.is_empty():
			errors.append("private dependency hook did not precede Main ready")
			quit(1)
			return
		main._save_state = SaveState.new(main, profile)
		m = main
		boot_count += 1
		bindings.append({"main_id": main.get_instance_id(), "before_ready": not main.is_node_ready(), "private_path": main._save_state.save_path, "scene_file_path": main.scene_file_path, "ticks_msec": Time.get_ticks_msec()})

func _boot() -> bool:
	var main: ReefMain = source_main.instantiate() as ReefMain
	root.add_child(main)
	current_scene = main
	if not await _wait(func() -> bool: return is_instance_valid(m) and m.is_node_ready() and m.start_menu_layer != null and m.get_node_or_null("BootSplashHandoff") == null, 20.0):
		errors.append("original display menu did not settle")
		return false
	_check("original configured Main loaded with preReady private dependency", m.scene_file_path == "res://scenes/main.tscn" and m._save_state.save_path == profile and bindings.size() == 1 and bool(bindings[0]["before_ready"]))
	return true

func _private_document(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {"exists": false}
	var raw: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not raw is Dictionary:
		return {"exists": true, "valid_json_dictionary": false}
	var value: Dictionary = raw as Dictionary
	return {"exists": true, "sha256": FileAccess.get_sha256(path), "save_generation": value.get("save_generation"), "day_one_active": value.get("day_one_active"), "plays": value.get("plays"), "pearls": value.get("pearls"), "skin": value.get("skin"), "quality": value.get("quality"), "unknown": value.get("flat_vector_private_unknown"), "keys": value.keys()}

func _snapshot() -> Dictionary:
	if not is_instance_valid(m):
		return {"main_valid": false}
	var movie: Dictionary = {"active": false}
	var clip: DayOneStoryClips = m._day_one_story_clip
	if clip != null and is_instance_valid(clip):
		movie = {"active": true, "id": clip.movie_id, "finished": clip._finished, "playing": clip.player.is_playing() if clip.player != null else false, "stream_position": clip.player.stream_position if clip.player != null else -1.0, "stream": clip.player.stream.resource_path if clip.player != null and clip.player.stream != null else ""}
	var controls: Array[Dictionary] = []
	for name: String in ["StartMenuContinueButton", "StartMenuNewGameButton", "StartMenuOptionsTab", "StartMenuQualityButton", "StartMenuMusicButton", "StartMenuMicButton", "StartMenuOptionsCloseButton", "StartMenuKeepGameButton", "StartMenuConfirmNewGameButton"]:
		var b: Button = _button(name) as Button
		if b == null:
			continue
		var styles: Dictionary = {}
		for state: String in ["normal", "hover", "pressed", "hover_pressed", "focus", "disabled"]:
			var style: StyleBox = b.get_theme_stylebox(state)
			styles[state] = {"class": style.get_class(), "resource_id": style.get_instance_id()}
		controls.append({"name": name, "id": b.get_instance_id(), "text": b.text, "position": str(b.position), "size": str(b.size), "global_rect": str(b.get_global_rect()), "visible": b.is_visible_in_tree(), "disabled": b.disabled, "pressed": b.is_pressed(), "focus": b.has_focus(), "focus_mode": b.focus_mode, "pressed_connections": b.pressed.get_connections().size(), "button_down_connections": b.button_down.get_connections().size(), "font_size": b.get_theme_font_size("font_size"), "styles": styles})
	var route: Dictionary = {}
	for key: String in ["phase", "day_one_media_request", "day_one_last_event", "lagoon_promenade_focus", "lagoon_hub", "lagoon_promenade"]:
		if m.g.has(key):
			route[key] = str(m.g[key])
	var director: Dictionary = m._day_one_director.serialize_state() if m._day_one_director != null else {}
	return {"main_valid": true, "main_id": m.get_instance_id(), "scene_file_path": m.scene_file_path, "current_scene_id": current_scene.get_instance_id() if is_instance_valid(current_scene) else 0, "quality": m.quality, "game": m.game, "phase": str(m.g.get("phase", "")), "route": route, "castle_room": m.castle_room_id, "skin": m.skin_id, "day_one": director, "start_menu_active": m.start_menu_active, "intro_active": m.intro_active, "has_saved_game": m.has_saved_game, "save_generation": m.save_generation, "private_path": m._save_state.save_path, "disk": _private_document(profile), "archive": _private_document(profile + ".before_new_game"), "movie": movie, "tree_paused": paused, "time_scale": Engine.time_scale, "caption_timer": m.msg_timer, "controls": controls, "bindings": bindings.duplicate(true), "first_session": m.first_session, "reset_marker": root.has_meta(StartMenu.DAY_ONE_AFTER_RESET_META)}

func _capture(id: String, role := "ORIGINAL_DISPLAY_ENTRY_DIAGNOSTIC_NOT_QA11") -> void:
	await RenderingServer.frame_post_draw
	var frame: Image = root.get_texture().get_image()
	if frame == null or frame.get_size() != root.size or frame.save_png(out_dir.path_join(id + ".png")) != OK:
		errors.append("native capture failed " + id)
		return
	var nodes: Array[Dictionary] = []
	if is_instance_valid(m):
		_nodes(m, nodes)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(out_dir.path_join(id + ".png")), "size": [frame.get_width(), frame.get_height()], "snapshot": _snapshot(), "selected_canvas_nodes": nodes, "node_inventory_scope": "Visible Canvas hierarchy traversed from original Main; not full native/compositor/resource/projection/QA11 closure", "role": role, "ticks_msec": Time.get_ticks_msec()})
	print("ENTRY66|CAPTURE|", id)

func _safe_quick_tap(button: Button, id: String) -> void:
	_touch(button, button.size * 0.5, true)
	await _frames(1)
	_touch(button, button.size * 0.5, false)
	await _frames(2)
	await _capture(id + "_released")

func _menu_options() -> void:
	await _tap(_button("StartMenuOptionsTab"), _button("StartMenuOptionsTab").size * 0.5, "options_open")
	var options: Control = _button("StartMenuOptionsPanel")
	_check("original Options opens sheet", options != null and options.is_visible_in_tree())
	await _capture("options_visible")
	if mode == "missing":
		_check("fresh desktop source default is honestly Sparkly", m.quality == "sparkly")
		await _tap(_button("StartMenuQualityButton"), _button("StartMenuQualityButton").size * 0.5, "quality_to_speedy")
		_check("original option selects Speedy and creates only private save", m.quality == "speedy" and m.has_saved_game and str(_private_document(profile).get("quality")) == "speedy")
	await _tap(_button("StartMenuOptionsCloseButton"), _button("StartMenuOptionsCloseButton").size * 0.5, "options_close")
	_check("original Options closes sheet", not options.is_visible_in_tree())

func _saved_confirmation(cancel_only: bool) -> void:
	var generation: int = m.save_generation
	await _tap(_button("StartMenuNewGameButton"), _button("StartMenuNewGameButton").size * 0.5, "new_game_request")
	var sheet: Control = _button("StartMenuNewGameConfirmation")
	var start: Button = _button("StartMenuConfirmNewGameButton") as Button
	_check("original NewGame opens protected confirmation disarmed", sheet != null and sheet.is_visible_in_tree() and start != null and start.disabled)
	await _safe_quick_tap(start, "disarmed_quick_tap")
	_check("disarmed quick tap leaves generation/archive unchanged", m.save_generation == generation and not FileAccess.file_exists(profile + ".before_new_game"))
	if not await _wait(func() -> bool: return not start.disabled, 5.0):
		errors.append("original confirm arm timer did not expire")
		return
	await _capture("confirmation_armed")
	await _safe_quick_tap(start, "armed_short_lift")
	await _frames(30)
	_check("armed short lift cannot reset private adventure", m.save_generation == generation and not FileAccess.file_exists(profile + ".before_new_game") and sheet.is_visible_in_tree())
	await _capture("confirmation_short_lift_settled")
	if cancel_only:
		await _tap(_button("StartMenuKeepGameButton"), _button("StartMenuKeepGameButton").size * 0.5, "keep_game")
		_check("KeepGame closes confirmation and retains private save", not sheet.is_visible_in_tree() and m.save_generation == generation)
		return
	var old_id: int = m.get_instance_id()
	var press_point: Vector2 = _point(start, start.size * 0.5)
	_touch(start, start.size * 0.5, true)
	await _frames(6)
	await _capture("full_hold_live_fill")
	if not await _wait(func() -> bool: return is_instance_valid(m) and m.get_instance_id() != old_id and m.is_node_ready(), 30.0):
		errors.append("actual source NewGame reload did not create a new Main")
		return
	# The old input owner is gone. Send only the terminal release to the viewport.
	var release := InputEventScreenTouch.new()
	release.index = 71
	release.position = press_point
	release.pressed = false
	root.push_input(release, true)
	events.append({"type": "touch", "pressed": false, "scope": "Terminal release after original input owner was disposed by actual NewGame reload"})
	_check("actual NewGame reloaded private dependency before ready", bindings.size() == 2 and bool(bindings[1]["before_ready"]) and m._save_state.save_path == profile)
	_check("original NewGame archives synthetic adventure and preserves unknown key", int(_private_document(profile + ".before_new_game").get("save_generation", -1)) >= int(seed["save_generation"]) and _state_equal(_private_document(profile + ".before_new_game").get("unknown"), seed["flat_vector_private_unknown"]))
	_check("original NewGame consumes one-shot marker and chooses DayOne", m.day_one_active and not m.start_menu_active and not root.has_meta(StartMenu.DAY_ONE_AFTER_RESET_META))
	await _observe_route("newgame")

func _observe_route(prefix: String) -> void:
	await _frames(6)
	await _capture(prefix + "_route_onset")
	var clip_started: bool = m._day_one_story_clip != null and is_instance_valid(m._day_one_story_clip)
	if clip_started:
		await _frames(90)
		await _capture(prefix + "_natural_clip_mid")
		if not await _wait(func() -> bool: return m._day_one_story_clip == null and not paused, 65.0):
			errors.append("original clip did not naturally finish " + prefix)
			return
		await _capture(prefix + "_natural_clip_finished")
	await _frames(60)
	await _capture(prefix + "_world_settled")
	_check("original launch chooses level2 Canvas world without observer routing " + prefix, m.game == "level2" and not m.start_menu_active and not m.intro_active and not m.first_session)
	_check("private path remains original dependency " + prefix, m._save_state.save_path == profile)
	if mode == "legacy":
		_check("legacy Continue remains outside DayOne and no opening movie", not m.day_one_active and not clip_started)
	else:
		_check("active DayOne route remains DayOne " + prefix, m.day_one_active)

func _exercise() -> void:
	if not await _boot():
		return
	await _capture("original_menu_settled")
	if mode == "dependency":
		var old_id: int = m.get_instance_id()
		var result: Error = reload_current_scene()
		_check("owned engine reload request accepted", result == OK)
		if not await _wait(func() -> bool: return is_instance_valid(m) and m.get_instance_id() != old_id and m.is_node_ready() and m.start_menu_layer != null, 25.0):
			errors.append("preReady private dependency reload proof failed")
			return
		await _frames(20)
		_check("actual engine reload injects private dependency before Main ready", bindings.size() == 2 and bool(bindings[1]["before_ready"]) and m._save_state.save_path == profile and current_scene == m)
		await _capture("dependency_reload_private_menu")
		return
	var continue_button: Button = _button("StartMenuContinueButton") as Button
	_check("Continue availability reflects genuine profile", continue_button.disabled == (mode == "missing"))
	await _frames(30)
	await _capture("menu_passive_settle")
	_check("passive original menu does not launch", m.start_menu_active)
	await _menu_options()
	if mode in ["legacy", "newgame"]:
		await _saved_confirmation(mode == "legacy")
		if mode == "newgame":
			return
	if mode == "missing":
		await _capture("fresh_profile_speedy_menu")
		_check("only real settings action created saved Continue", m.has_saved_game and not continue_button.disabled)
		return
	await _tap(continue_button, continue_button.size * 0.5, "continue_original")
	await _observe_route("continue")

func _run() -> void:
	mode = OS.get_environment("R66_MODE")
	out_dir = OS.get_environment("R66_OUT")
	normal_base = OS.get_environment("R66_NORMAL_BASE")
	var width: int = int(OS.get_environment("R66_WIDTH"))
	if mode not in ["missing", "legacy", "dayone", "newgame", "dependency"] or out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	var engine: Dictionary = Engine.get_version_info()
	if str(engine.get("hash", "")) != "ed1daf0bf001b61586d9930840f2f1394092c079" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() != "Windows" or Engine.time_scale != 1.0:
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "won": {}, "found": {}, "pearls": 23, "plays": 3, "skin": "classic", "quality": "speedy", "music": false, "mic": false, "flat_vector_private_unknown": {"token": "R66_PRIVATE_ONLY", "keep": [3, 7]}}
	if mode == "dayone":
		seed["day_one_active"] = true
		seed["day_one_arrival_plane_media_seen"] = false
		seed["day_one_dirty_castle_discovered"] = false
	if mode != "missing":
		var file: FileAccess = FileAccess.open(profile, FileAccess.WRITE)
		file.store_string(JSON.stringify(seed, "\t", true) + "\n")
		file.close()
	node_added.connect(_bind_private_before_ready)
	source_main = load("res://scenes/main.tscn") as PackedScene
	if await _aspect(Vector2i(width, 720)):
		await _exercise()
	else:
		errors.append("native viewport did not settle")
	var final_snapshot: Dictionary = _snapshot()
	await _retire()
	if _normal_hashes() != normal_before:
		errors.append("normal save/archive hashes changed")
	var report: Dictionary = {"schema": "reef.original_display_entry/1", "mode": mode, "source_revision": OS.get_environment("R66_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "aspect": [width, 720], "time_scale": Engine.time_scale, "states": states, "events": events, "checks": checks, "errors": errors, "bindings": bindings, "boot_count": boot_count, "seed": seed if mode != "missing" else {}, "private_profile": profile, "normal_before": normal_before, "normal_after": _normal_hashes(), "final_snapshot_before_retire": final_snapshot, "actual_child_data": false, "authored_world_bootstrap": false, "source_route_forced": false, "production_changes": [], "scope": "Original configured Main/native StartMenu inputs and natural route. PreReady SaveState path substitution isolates every Main including actual reload; no gameplay/visual/quality/route/clock/camera writes. Missing-save desktopSparkly states explicitly diagnostic/excluded until actual Options selectsSpeedy. Original source movie is unskipped, Dummy audio. Same-process desktop evidence is notfreshOS/QA11/device/performance/child/owner/art or full route/fallback closure."}
	var output: FileAccess = FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("ENTRY66|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
