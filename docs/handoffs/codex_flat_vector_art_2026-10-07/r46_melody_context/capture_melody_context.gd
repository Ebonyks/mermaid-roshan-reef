extends SceneTree
## R46 current-source Melody context; direct production API entry, not natural route proof.
var m: ReefMain
var melody: MelodyGame
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var active_profile := "R46"
var normal_before: Dictionary = {}

func _init() -> void:
	call_deferred("_run")


func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var path := base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result


func _wait_frames(count: int) -> void:
	for i: int in range(count):
		await process_frame


func _set_aspect(target: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		get_root().size = target
		DisplayServer.window_set_size(target)
		await process_frame
		var test: Image = get_root().get_texture().get_image()
		if test != null and test.get_size() == target:
			return true
	return false


func _presentation() -> Dictionary:
	return {"boot_splash_present": m.get_node_or_null("BootSplashHandoff") != null, "start_menu_active": m.start_menu_active, "start_menu_layer_present": m.start_menu_layer != null, "intro_active": m.intro_active, "intro_layer_present": m.intro_layer != null, "fade_alpha": m.fade_rect.modulate.a if m.fade_rect != null else 0.0, "medal_present": m.get_node_or_null("MedalCelebrationLayer") != null}


func _wait_presentation() -> bool:
	for i: int in range(300):
		await process_frame
		var present := _presentation()
		if not bool(present["boot_splash_present"]) and not bool(present["start_menu_active"]) and not bool(present["start_menu_layer_present"]) and not bool(present["intro_active"]) and not bool(present["intro_layer_present"]) and float(present["fade_alpha"]) <= 0.02:
			return true
	return false


func _new_main(profile: String) -> bool:
	var scene := load("res://scenes/main.tscn") as PackedScene
	m = scene.instantiate() as ReefMain
	m._save_state = SaveState.new(m,profile)
	get_root().add_child(m)
	await _wait_frames(3)
	m._apply_quality("speedy")
	m.day_one_active = false
	if m.start_menu_active:
		m._start_menu_ref()._dismiss_menu()
	if m.intro_active:
		m._skip_intro()
	if not await _wait_presentation():
		errors.append("startup presentation did not settle "+active_profile)
		return false
	return true


func _retire_main() -> void:
	m.set_process(false)
	m.queue_free()
	await _wait_frames(10)
	m = null



func _nodes(node: Node, rows: Array[Dictionary]) -> void:
	var item := node as CanvasItem
	if item != null and item.is_visible_in_tree():
		var row: Dictionary = {"path": str(node.get_path()), "class": node.get_class(), "z_index": item.z_index, "modulate": str(item.modulate)}
		var control := node as Control
		if control != null:
			row["global_rect"] = str(control.get_global_rect())
		var sprite := node as Sprite2D
		if sprite != null and sprite.texture != null:
			row["texture"] = sprite.texture.resource_path
			row["texture_size"] = str(sprite.texture.get_size())
		var polygon := node as Polygon2D
		if polygon != null:
			row["polygon"] = str(polygon.polygon)
			row["color"] = str(polygon.color)
		rows.append(row)
	for child: Node in node.get_children():
		_nodes(child, rows)

func _capture(id: String, role: String, input: Dictionary = {}) -> void:
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != get_root().size or image.save_png(path) != OK:
		errors.append("native framebuffer capture failed " + id)
		return
	var nodes: Array[Dictionary] = []
	if melody != null and melody.active_layer() != null:
		_nodes(melody.active_layer(), nodes)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path), "width": image.get_width(), "height": image.get_height(), "role": role, "normal_route_proved": false, "game": m.game, "paused": paused, "progress": melody.progress_count() if melody != null else -1, "snapshot": melody.audit_snapshot() if melody != null else {}, "nodes": nodes, "input": input, "presentation": _presentation()})
	print("MELODY46|CAPTURE|" + id)

func _pointer(pressed: bool, point: Vector2) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.pressed = pressed
	event.position = point
	get_root().push_input(event, true)
	await process_frame

func _launch() -> void:
	var fr: Dictionary = {}
	for candidate: Dictionary in m.friends:
		if String(candidate.get("game", "")) == "melody":
			fr = candidate
	if fr.is_empty():
		errors.append("canonical Daddy friend dictionary missing")
		return
	m._start_game(fr)
	for i: int in range(300):
		await process_frame
		if m.game == "melody" and m.fade_rect.modulate.a <= 0.02:
			break
	melody = m._game_obj("melody", MelodyGame) as MelodyGame
	await _wait_frames(5)
	if m.game != "melody" or melody.active_layer() == null:
		errors.append("production API did not open Melody")

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		quit(1)
		return
	out_dir = OS.get_environment("R46_OUT")
	var width: int = int(OS.get_environment("R46_WIDTH"))
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	if not await _set_aspect(Vector2i(width, 720)):
		quit(1)
		return
	var profile := out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	var seed: Dictionary = {"schema_version": 1, "won": {}, "found": {}, "plays": 0, "pearls": 23, "pearls_ever": 23, "music": false, "mic": false, "quality": "speedy", "crafts": {}, "stickers": {}, "custom_fish": [], "custom_friends": []}
	var seed_file := FileAccess.open(profile, FileAccess.WRITE)
	seed_file.store_string(JSON.stringify(seed, "\t", true) + "\n")
	seed_file.close()
	if not await _new_main(profile):
		await _retire_main()
		quit(1)
		return
	await _capture("boot_promenade", "EXCLUDED_ENTRY_DIAGNOSTIC")
	await _launch()
	await _capture("ready", "CURRENT_SOURCE_API_ART_CONTEXT")
	await _wait_frames(60)
	await _capture("passive_cycle", "CURRENT_SOURCE_API_ART_CONTEXT")
	m._pause_ref().toggle_pause()
	await _wait_frames(3)
	await _capture("pause", "EXCLUDED_PAUSE_DIAGNOSTIC")
	m._pause_ref().toggle_pause()
	await _wait_frames(8)
	await _capture("resumed", "CURRENT_SOURCE_API_ART_CONTEXT")
	for note: int in range(7):
		var ready := false
		for frame: int in range(720):
			await process_frame
			if m.game != "melody":
				break
			var zone := melody.timing_zone_screen_rect().grow(-18.0)
			if zone.has_point(melody.active_note_screen_point()) and not bool(melody.audit_snapshot().get("blocked_until_release", true)):
				ready = true
				break
		if not ready:
			errors.append("note never became actionable " + str(note))
			break
		var point := melody.active_note_screen_point()
		await _capture("note_%d_green" % note, "CURRENT_SOURCE_API_ART_CONTEXT")
		await _pointer(true, point)
		await _capture("note_%d_pressed" % note, "CURRENT_SOURCE_API_ART_CONTEXT", {"type": "InputEventScreenTouch", "index": 0, "pressed": true, "point": str(point)})
		await _pointer(false, point)
		await _wait_frames(2)
		await _capture("note_%d_released" % note, "CURRENT_SOURCE_API_ART_CONTEXT", {"type": "InputEventScreenTouch", "index": 0, "pressed": false, "point": str(point)})
		if note < 6 and melody.progress_count() != note + 1:
			errors.append("real release did not advance note " + str(note))
			break
	await _wait_frames(75)
	await _capture("after_input_settle", "EXCLUDED_RETURN_DIAGNOSTIC")
	if m.game == "melody":
		m._leave_current_activity()
		await _wait_frames(30)
	await _launch()
	await _capture("reentry", "CURRENT_SOURCE_API_ART_CONTEXT")
	m._leave_current_activity()
	await _wait_frames(30)
	await _capture("voluntary_exit", "EXCLUDED_RETURN_DIAGNOSTIC")
	await _retire_main()
	if _normal_hashes() != normal_before:
		errors.append("normal save artifacts changed")
	var report: Dictionary = {"schema": "reef.melody_context/1", "source_revision": OS.get_environment("R46_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "quality": "speedy", "aspect": [width, 720], "states": states, "seed": seed, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors, "normal_route_proved": false, "actual_child_data": false, "scope": "Direct current production API launch; actual touch press/release continuation, no target/progress/timing writes. Not natural entry, DL-QA-11, human/device/child/owner or replacement acceptance."}
	var output := FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("MELODY46|RESULT|" + ("PASS" if errors.is_empty() else "FAIL") + "|" + str(errors))
	quit(0 if errors.is_empty() else 1)
