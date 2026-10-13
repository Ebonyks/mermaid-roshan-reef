extends SceneTree
## Independent diagnostic picture-game capture; no production edits.
var m: ReefMain
var out_dir := ""
var states: Array[Dictionary] = []
var errors: Array[String] = []
var normal_before: Dictionary = {}
var fresh_state_ids: Array[String] = []

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

func _visible_nodes(node: Node, output: Array[Dictionary]) -> void:
	var item := node as CanvasItem
	if item != null and item.is_visible_in_tree():
		var row: Dictionary = {"path": str(node.get_path()), "class": node.get_class(), "modulate": str(item.modulate), "z_index": item.z_index}
		var control := node as Control
		if control != null:
			row["global_rect"] = str(control.get_global_rect())
		var texture := node as TextureRect
		if texture != null and texture.texture != null:
			row["texture"] = texture.texture.resource_path
		var button := node as Button
		if button != null:
			row["disabled"] = button.disabled
		output.append(row)
	for child: Node in node.get_children():
		_visible_nodes(child, output)

func _capture(id: String, input_info: Dictionary = {}) -> void:
	await RenderingServer.frame_post_draw
	var frame: Image = get_root().get_texture().get_image()
	var target := get_root().size
	if frame == null or frame.get_size() != target:
		errors.append("image backing mismatch " + id)
		return
	var path := out_dir.path_join(id + ".png")
	if frame.save_png(path) != OK:
		errors.append("save failed " + id)
		return
	var visible: Array[Dictionary] = []
	if m.mg2d_root != null:
		_visible_nodes(m.mg2d_root, visible)
	var image_file := FileAccess.open(path, FileAccess.READ)
	states.append({"id": id, "image": {"file": id + ".png", "sha256": FileAccess.get_sha256(path), "bytes": image_file.get_length(), "dimensions": [frame.get_width(),frame.get_height()]}, "kind": m.mg_kind, "stage": (m.mg.get("stage", []) as Array).duplicate(), "grown": int(m.mg.get("grown",0)), "won": bool(m.mg.get("won",false)), "input": input_info, "visible_nodes": visible, "main_hud_visible": m.hud_layer.visible if m.hud_layer != null else false, "save_path": m._save_state.save_path})
	image_file.close()
	print("ROOTPIC|CAPTURE|" + id)

func _tap_garden(index: int, expected: int) -> Dictionary:
	var buttons: Array = m.mg.get("btns", [])
	var b := buttons[index] as Button
	var where := b.get_global_rect().get_center()
	var press := InputEventMouseButton.new()
	press.button_index = MOUSE_BUTTON_LEFT
	press.pressed = true
	press.position = where
	press.global_position = where
	get_root().push_input(press, true)
	await process_frame
	var release := InputEventMouseButton.new()
	release.button_index = MOUSE_BUTTON_LEFT
	release.pressed = false
	release.position = where
	release.global_position = where
	get_root().push_input(release, true)
	await process_frame
	var stage: Array = m.mg.get("stage", [])
	var observed := int(stage[index])
	if observed != expected:
		errors.append("actual pointer did not progress slot%d expected%d got%d" % [index, expected, observed])
	return {"method":"Window.push_input raw mouse press/release", "slot":index, "position":str(where), "expected_stage":expected, "observed_stage":observed, "target_rect":str(b.get_global_rect())}

func _run_aspect(target: Vector2i, base_out: String) -> void:
	out_dir = base_out.path_join("%dx%d" % [target.x,target.y])
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _set_aspect(target):
		errors.append("aspect readiness failed")
		return
	for kind: String in ["garden", "snowman", "trampoline", "xmas"]:
		var scene := load("res://scenes/main.tscn") as PackedScene
		m = scene.instantiate() as ReefMain
		var profile := out_dir.path_join("profiles/" + kind + "/reef_save.json")
		DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
		m._save_state = SaveState.new(m,profile)
		get_root().add_child(m)
		await _wait_frames(3)
		m._apply_quality("speedy")
		m.day_one_active = false
		if m.start_menu_active:
			m._start_menu_ref()._dismiss_menu()
		if m.intro_active:
			m._skip_intro()
		await _wait_frames(3)
		m._mg2d_open(kind)
		await _wait_frames(3)
		await _capture(kind + "_fresh_ready", {"entry":"production _mg2d_open API; fresh Main and isolated save per game; direct route fixture"})
		m._mg2d_close()
		m.set_process(false)
		m.queue_free()
		await _wait_frames(4)
	var manifest: Dictionary = {"schema":"reef.root_picture_context/1", "source_revision":OS.get_environment("ROOTPIC_REV"), "capture_method":"same-process viewport", "engine":Engine.get_version_info(), "renderer":RenderingServer.get_current_rendering_method(), "quality":"speedy", "aspect":[target.x,target.y], "states":states, "normal_save_before":normal_before, "normal_save_after":_normal_hashes(), "errors":errors, "scope_limits":"Fresh Main and SaveState per game; direct guarded API entry; ready stills only, no natural castle route, action/save/motion/device/child/owner acceptance."}
	var file := FileAccess.open(out_dir.path_join("capture_manifest.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest,"\t",true)+"\n")
	file.close()

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major",0)) != 4 or int(engine.get("minor",0)) != 7 or int(engine.get("patch",0)) != 2 or String(engine.get("status","")) != "stable" or String(engine.get("build","")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless":
		print("ROOTPIC|FAIL|engine/renderer/display")
		quit(1)
		return
	normal_before = _normal_hashes()
	var base_out := OS.get_environment("ROOTPIC_OUT")
	if base_out.is_empty() or DirAccess.dir_exists_absolute(base_out):
		print("ROOTPIC|FAIL|new output required")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(base_out)
	await _run_aspect(Vector2i(1280,720),base_out)
	await _run_aspect(Vector2i(1600,720),base_out)
	if normal_before != _normal_hashes():
		errors.append("normal save changed")
	print("ROOTPIC|RESULT|" + ("PASS" if errors.is_empty() else "FAIL") + "|" + str(errors))
	quit(0 if errors.is_empty() else 1)
