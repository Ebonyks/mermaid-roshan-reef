extends SceneTree
## Advisory captures of the shipping Castle Canvas rooms, separate from the
## trusted probe_castle_pearl_art runtime gate. These images are diagnostic;
## they grant no visual, owner, device, or child acceptance.

const SIZE := Vector2i(1280, 720)
const SAVE_SUFFIXES: Array[String] = ["", ".tmp0", ".tmp1", ".tmp", ".old", ".bak", ".bak.tmp", ".bak.old"]
var main: ReefMain
var out_dir := ""
var captures: Array[Dictionary] = []
var failures: Array[String] = []


func _init() -> void:
	call_deferred("_run")


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _fingerprints(path: String) -> Array[String]:
	var values: Array[String] = []
	for suffix: String in SAVE_SUFFIXES:
		var filename := path + suffix
		values.append(FileAccess.get_sha256(filename) if FileAccess.file_exists(filename) else "absent")
	return values


func _nonblank(image: Image) -> bool:
	if image == null or image.is_empty() or image.get_size() != SIZE:
		return false
	var lo := 1.0
	var hi := 0.0
	for y: int in range(36):
		for x: int in range(64):
			var color := image.get_pixel(x * 20 + 10, y * 20 + 10)
			var luma := color.r * 0.2126 + color.g * 0.7152 + color.b * 0.0722
			lo = minf(lo, luma)
			hi = maxf(hi, luma)
	return hi - lo >= 0.20


func _capture(room_id: String) -> void:
	main._castle_rooms_ref().show_room(room_id, false)
	await _frames(4)
	var correct_room := main.castle_room_id == room_id \
		and main.castle_room_stage != null and main.castle_room_stage.is_visible_in_tree() \
		and main.castle_room_world_root != null and not main.start_menu_active
	if not correct_room:
		failures.append("room_not_visible:%s" % room_id)
		return
	await RenderingServer.frame_post_draw
	var image := get_root().get_texture().get_image()
	var filename := "castle_%s.png" % room_id
	var path := out_dir.path_join(filename)
	var ok := _nonblank(image)
	var write_error := image.save_png(path) if ok else ERR_INVALID_DATA
	if write_error != OK:
		failures.append("capture:%s:%s" % [room_id, str(write_error)])
	captures.append({"room_id": room_id, "file": filename,
		"width": image.get_width() if image != null else 0,
		"height": image.get_height() if image != null else 0,
		"sha256": FileAccess.get_sha256(path) if write_error == OK else "",
		"result": "PASS" if write_error == OK else "FAIL"})
	print("CASTLESHOT|%s|%s|%s" % [room_id,
		"PASS" if write_error == OK else "FAIL", path])


func _run() -> void:
	if DisplayServer.get_name() == "headless":
		print("CASTLESHOT|RESULT|NOT_MEASURED|reason=requires_rendered_viewport|written=0")
		quit()
		return
	out_dir = OS.get_environment("CASTLE_SHOT_OUT").strip_edges()
	if out_dir.is_empty():
		out_dir = ProjectSettings.globalize_path("res://tmp/castle_shots_2d")
	if DirAccess.make_dir_recursive_absolute(out_dir) != OK:
		print("CASTLESHOT|RESULT|FAIL|reason=output_directory|written=0")
		quit(1)
		return
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = SIZE
	var normal_save := ProjectSettings.globalize_path("user://reef_save.json")
	var before := _fingerprints(normal_save)
	var isolated_save := out_dir.path_join(".castle_capture_probe_save.json")
	# Remove only this harness's previous derivatives; never read or load a
	# normal child save as a fixture for the visual packet.
	for suffix: String in SAVE_SUFFIXES:
		DirAccess.remove_absolute(isolated_save + suffix)
	for room: Dictionary in CastleRooms25D.ROOMS:
		DirAccess.remove_absolute(out_dir.path_join("castle_%s.png" % String(room["id"])))
	var packed := load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	main._save_state = SaveState.new(main, isolated_save)
	get_root().add_child(main)
	if main.dev_mode != null and is_instance_valid(main.dev_mode):
		main.dev_mode.process_mode = Node.PROCESS_MODE_DISABLED
		main.dev_mode.queue_free()
		main.dev_mode = null
	await _frames(3)
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
		await _frames(3)
	if main.intro_active:
		main._skip_intro()
	await _frames(2)
	main._apply_quality("speedy")
	main.day_one_active = false
	main._enter_castle_interior_now(false)
	await _frames(3)
	for room: Dictionary in CastleRooms25D.ROOMS:
		await _capture(String(room["id"]))
	main.process_mode = Node.PROCESS_MODE_DISABLED
	var unchanged := before == _fingerprints(normal_save)
	if not unchanged:
		failures.append("normal_save_mutated")
	for suffix: String in SAVE_SUFFIXES:
		DirAccess.remove_absolute(isolated_save + suffix)
	var version := Engine.get_version_info()
	var exact_engine := int(version.get("major", 0)) == 4 \
		and int(version.get("minor", 0)) == 7 and int(version.get("patch", 0)) == 2 \
		and String(version.get("status", "")) == "stable" \
		and String(version.get("build", "")) == "official"
	var renderer := String(RenderingServer.get_current_rendering_method())
	if not exact_engine:
		failures.append("engine_version:%s" % String(version.get("string", "")))
	if renderer != "mobile":
		failures.append("rendering_method:%s" % renderer)
	var written := 0
	for capture: Dictionary in captures:
		if capture["result"] == "PASS":
			written += 1
	var result := "PASS" if failures.is_empty() and written == CastleRooms25D.ROOMS.size() else "FAIL"
	var manifest_path := out_dir.path_join("castle_review_manifest.json")
	var file := FileAccess.open(manifest_path, FileAccess.WRITE)
	if file == null:
		result = "FAIL"
		failures.append("manifest_write")
	else:
		file.store_string(JSON.stringify({"schema": "reef.castle.visual_review.v1",
			"probe": "res://scripts/probe_castle_shots_2d.gd",
			"probe_sha256": FileAccess.get_sha256("res://scripts/probe_castle_shots_2d.gd"),
			"engine": version, "rendering_method": renderer, "quality": "speedy",
			"expected": CastleRooms25D.ROOMS.size(), "written": written,
			"captures": captures, "failures": failures, "save_unchanged": unchanged,
			"result": result, "acceptance": "DIAGNOSTIC_ONLY"}, "\t"))
		file.close()
	print("CASTLESHOT|RESULT|%s|written=%d|expected=%d|%s" % [
		result, written, CastleRooms25D.ROOMS.size(), manifest_path])
	main.queue_free()
	await _frames(3)
	quit(0 if result == "PASS" else 1)
