extends SceneTree
## Craft Studio source-context diagnostics; direct guarded entry, fresh isolated save, no production edits.
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

func _presentation() -> Dictionary:
	return {"boot_splash_present": m.get_node_or_null("BootSplashHandoff") != null, "start_menu_active": m.start_menu_active, "start_menu_layer_present": m.start_menu_layer != null, "intro_active": m.intro_active, "intro_layer_present": m.intro_layer != null, "fade_alpha": m.fade_rect.modulate.a if m.fade_rect != null else 0.0, "medal_present": m.get_node_or_null("MedalCelebrationLayer") != null}

func _wait_presentation() -> bool:
	for i: int in range(300):
		await process_frame
		var present := _presentation()
		if not bool(present["boot_splash_present"]) and not bool(present["start_menu_active"]) and not bool(present["start_menu_layer_present"]) and not bool(present["intro_active"]) and not bool(present["intro_layer_present"]) and float(present["fade_alpha"]) <= 0.02:
			return true
	return false

func _capture(id: String, input_info: Dictionary = {}) -> void:
	await RenderingServer.frame_post_draw
	var presentation := _presentation()
	if bool(presentation["boot_splash_present"]) or bool(presentation["start_menu_active"]) or bool(presentation["medal_present"]) or float(presentation["fade_alpha"]) > 0.02:
		errors.append("blocking/foreign presentation overlay " + id)
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
	if m.craft_layer != null:
		_visible_nodes(m.craft_layer, visible)
	var image_file := FileAccess.open(path, FileAccess.READ)
	states.append({"id": id, "image": {"file": id + ".png", "sha256": FileAccess.get_sha256(path), "bytes": image_file.get_length(), "dimensions": [frame.get_width(),frame.get_height()]}, "presentation": presentation, "kind": m.craft_kind, "part": m.craft_part, "body": str(m.craft_body), "accent": str(m.craft_fins), "third": str(m.craft_c3), "body_rainbow": m.craft_body_rb, "accent_rainbow": m.craft_fins_rb, "pearls": m.pearl_count, "input": input_info, "visible_nodes": visible, "main_hud_visible": m.hud_layer.visible if m.hud_layer != null else false, "save_path": m._save_state.save_path})
	image_file.close()
	print("ROOTPIC|CAPTURE|" + id)

func _swatch(index: int) -> Button:
	var want: Color = CraftStudio.PALETTE[index]
	for node: Node in get_nodes_in_group("craft_palette_button"):
		var button := node as Button
		if button == null or button.is_queued_for_deletion() or not m.craft_layer.is_ancestor_of(button):
			continue
		var style := button.get_theme_stylebox("normal") as StyleBoxFlat
		if style != null and style.bg_color.is_equal_approx(want):
			return button
	return null

func _find(name: String) -> Button:
	return m.craft_layer.find_child(name,true,false) as Button

func _raw_button(button: Button, pressed: bool) -> void:
	var where := button.get_global_rect().get_center()
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.position = where
	event.global_position = where
	get_root().push_input(event,true)
	await process_frame

func _tap(button: Button) -> void:
	if button == null:
		errors.append("current button missing")
		return
	await _raw_button(button,true)
	await _raw_button(button,false)
	await _wait_frames(3)

func _current_color() -> Color:
	return m.craft_body if m.craft_part == "body" else (m.craft_fins if m.craft_part == "accent" else m.craft_c3)

func _rainbow() -> Button:
	for node: Node in get_nodes_in_group("craft_palette_button"):
		var button := node as Button
		if button != null and not button.is_queued_for_deletion() and m.craft_layer.is_ancestor_of(button) and button.text == "🌈":
			return button
	return null

func _run_aspect(target: Vector2i, base_out: String) -> void:
	out_dir = base_out.path_join("%dx%d" % [target.x,target.y])
	DirAccess.make_dir_recursive_absolute(out_dir)
	states.clear()
	if not await _set_aspect(target):
		errors.append("aspect readiness failed")
		return
	var scene := load("res://scenes/main.tscn") as PackedScene
	m = scene.instantiate() as ReefMain
	var profile := out_dir.path_join("profiles/craft/reef_save.json")
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
	if not await _wait_presentation():
		errors.append("startup presentation did not settle")
		m.queue_free()
		await _wait_frames(4)
		return
	m._open_craft_studio()
	await _wait_frames(3)
	if m.craft_layer == null or m.craft_kind != "fish" or m.pearl_count != 0:
		errors.append("fresh Craft state mismatch")
	await _capture("craft_fresh_ready",{"entry":"production _open_craft_studio API; direct fixture, defaults preserved"})
	for kind: String in ["cat","bird"]:
		await _tap(_find("CraftKind_"+kind))
		if m.craft_kind != "fish" or m.pearl_count != 0:
			errors.append("locked kind changed unearned state")
		await _capture("craft_locked_"+kind+"_feedback",{"method":"raw pointer press/release, no pearls assigned"})
	for part: String in ["body","accent","third"]:
		await _tap(_find("CraftPart_"+part))
		if m.craft_part != part:
			errors.append("part pointer transition failed "+part)
		await _capture("craft_"+part+"_palette_ready")
		for i: int in range(8):
			var button := _swatch(i)
			if button == null:
				errors.append("color swatch missing %s%d" % [part,i])
				continue
			var input_info: Dictionary = {"method":"Window.push_input raw pointer", "part":part,"palette_index":i,"color":str(CraftStudio.PALETTE[i]),"target_rect":str(button.get_global_rect())}
			await _raw_button(button,true)
			if part == "body":
				await _capture("craft_body_color%02d_pressed" % i,input_info)
			await _raw_button(button,false)
			await _wait_frames(3)
			if not _current_color().is_equal_approx(CraftStudio.PALETTE[i]):
				errors.append("color pointer transition failed %s%d" % [part,i])
			await _capture("craft_%s_color%02d_selected" % [part,i],input_info)
		if part != "third":
			await _tap(_rainbow())
			if not (m.craft_body_rb if part == "body" else m.craft_fins_rb):
				errors.append("rainbow pointer transition failed "+part)
			await _capture("craft_"+part+"_rainbow_selected",{"method":"raw pointer press/release"})
	m._craft_ref()._close_craft()
	await _wait_frames(4)
	if m.craft_layer != null:
		errors.append("craft teardown did not close")
	m.set_process(false)
	m.queue_free()
	await _wait_frames(4)
	var manifest: Dictionary = {"schema":"reef.root_craft_context/1", "source_revision":OS.get_environment("ROOTPIC_REV"), "capture_method":"same-process viewport", "engine":Engine.get_version_info(), "renderer":RenderingServer.get_current_rendering_method(), "quality":"speedy", "aspect":[target.x,target.y], "states":states, "normal_save_before":normal_before, "normal_save_after":_normal_hashes(), "errors":errors, "scope_limits":"Fresh Main/SaveState and guarded direct Craft entry. Default fish, all eight exact colors for body/accent/detail, body pressed states, two rainbow choices, cat/bird locked feedback. No synthetic unlocks or progress counters. No natural castle route, purchased cat/bird preview, final crafting/save reward, full motion or hover/focus/disabled/device/child/owner/DL-QA-11 acceptance."}
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
