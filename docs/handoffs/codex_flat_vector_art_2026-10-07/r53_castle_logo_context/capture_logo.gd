extends SceneTree
## R53 source-exact Castle logo context. Original input; private synthetic data only.
var m: ReefMain
var out_dir := ""
var profile := ""
var states: Array[Dictionary] = []
var events: Array[Dictionary] = []
var errors: Array[String] = []
var checks: Array[Dictionary] = []
var normal_before: Dictionary = {}
var seed: Dictionary = {}
var boot_count := 0

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var p := base + suffix
		result[suffix] = FileAccess.get_sha256(p) if FileAccess.file_exists(p) else "absent"
	return result

func _frames(count: int) -> void:
	for i: int in range(count):
		await process_frame

func _wait(predicate: Callable, seconds: float = 12.0) -> bool:
	var deadline := Time.get_ticks_msec() + int(seconds * 1000.0)
	while Time.get_ticks_msec() < deadline:
		if bool(predicate.call()):
			return true
		await process_frame
	return bool(predicate.call())

func _aspect(size: Vector2i) -> bool:
	root.mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		root.size = size
		DisplayServer.window_set_size(size)
		await process_frame
		var frame: Image = root.get_texture().get_image()
		if frame != null and frame.get_size() == size:
			return true
	return false

func _tex(t: Texture2D) -> Dictionary:
	if t == null:
		return {}
	var row := {"class": t.get_class(), "path": t.resource_path, "size": str(t.get_size())}
	if t is AtlasTexture:
		var atlas := t as AtlasTexture
		row["atlas_path"] = atlas.atlas.resource_path if atlas.atlas != null else ""
		row["region"] = str(atlas.region)
	return row

func _nodes(node: Node, rows: Array[Dictionary]) -> void:
	var item := node as CanvasItem
	if item != null and item.is_visible_in_tree():
		var row := {"path": str(node.get_path()), "class": node.get_class(), "script": node.get_script().resource_path if node.get_script() != null else "", "z_index": item.z_index, "modulate": str(item.modulate), "self_modulate": str(item.self_modulate)}
		var c := node as Control
		if c != null:
			row["global_rect"] = str(c.get_global_rect())
			row["mouse_filter"] = c.mouse_filter
		var sprite := node as Sprite2D
		if sprite != null:
			row["texture"] = _tex(sprite.texture)
		var rect := node as TextureRect
		if rect != null:
			row["texture"] = _tex(rect.texture)
		var button := node as TextureButton
		if button != null:
			row["texture"] = _tex(button.texture_normal)
			row["disabled"] = button.disabled
		var text_label := node as Label
		if text_label != null:
			row["text"] = text_label.text
			row["font_size"] = text_label.get_theme_font_size("font_size")
		var plain_button := node as Button
		if plain_button != null:
			row["text"] = plain_button.text
			row["disabled"] = plain_button.disabled
			row["selected"] = plain_button.get_meta("selected", false)
			var style := plain_button.get_theme_stylebox("normal")
			row["normal_style_class"] = style.get_class()
			if style is StyleBoxFlat:
				row["normal_color"] = str((style as StyleBoxFlat).bg_color)
		var color := node as ColorRect
		if color != null:
			row["color"] = str(color.color)
		var poly := node as Polygon2D
		if poly != null:
			row["polygon"] = str(poly.polygon)
			row["color"] = str(poly.color)
		rows.append(row)
	for child: Node in node.get_children():
		_nodes(child, rows)

func _disk() -> Dictionary:
	if not FileAccess.file_exists(profile):
		return {}
	var value: Variant = JSON.parse_string(FileAccess.get_file_as_string(profile))
	if not value is Dictionary:
		return {}
	return {"color": value.get("castle_logo_color", "rainbow"),
		"symbol": value.get("castle_logo_symbol", "rainbow"),
		"save_generation": value.get("save_generation"),
		"unknown": value.get("flat_vector_private_unknown")}

func _display() -> Dictionary:
	var result := {"exists": false, "banners": []}
	var display := m.castle_logo_room_display
	if display == null or not is_instance_valid(display):
		return result
	result["exists"] = true
	result["room"] = display.get_meta("castle_room_id", "")
	result["replaces"] = display.get_meta("replaces_design", "")
	result["mouse_filter"] = display.mouse_filter
	var banners: Array[Dictionary] = []
	for node: Node in display.get_meta("banner_nodes", []):
		var banner := node as CastleLogoStudio.BannerPreview
		if banner != null:
			banners.append({"name": banner.name, "color": banner.color_id,
				"symbol": banner.symbol_id, "rect": str(banner.get_global_rect()),
				"banner_texture": _tex(banner.banner_image.texture),
				"motif_texture": _tex(banner.symbol_image.texture),
				"mouse_filter": banner.mouse_filter})
	result["banners"] = banners
	var badge := display.find_child("CastleLogoCraftBoardBadge", true, false) as CastleLogoStudio.LogoPreview
	result["badge"] = {"exists": badge != null,
		"color": badge.color_id if badge != null else "",
		"symbol": badge.symbol_id if badge != null else ""}
	return result

func _snapshot() -> Dictionary:
	var result := {"normal_route_proved": false, "private_checkpoint": true,
		"time_scale": Engine.time_scale, "paused": paused}
	if is_instance_valid(m):
		result.merge({"game": m.game, "quality": m.quality, "room": m.castle_room_id,
			"logo_open": m.castle_logo_layer != null,
			"color": m.castle_logo_color, "symbol": m.castle_logo_symbol,
			"save_path": m._save_state.save_path,
			"save_sha256": FileAccess.get_sha256(profile) if FileAccess.file_exists(profile) else "absent",
			"disk": _disk(), "save_pending": m.save_pending, "save_dirty": m.save_dirty,
			"freeplay": [m.opera_stars, m.opera_progress, m.pearl_count],
			"navigation_top": m._navigation_ref().top_id(), "display": _display()})
		if m.castle_logo_preview != null:
			var preview := m.castle_logo_preview as CastleLogoStudio.LogoPreview
			result["preview"] = {"is_source_logo_preview": preview != null,
				"color": preview.color_id, "symbol": preview.symbol_id,
				"rect": str(preview.get_global_rect()), "motif": _tex(preview.symbol_image.texture)}
	return result

func _capture(id: String, role := "CURRENT_PRIVATE_CHECKPOINT_CONTEXT") -> void:
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != root.size or image.save_png(path) != OK:
		errors.append("native capture failed " + id)
		return
	var nodes: Array[Dictionary] = []
	if is_instance_valid(m):
		if m.castle_logo_layer != null:
			_nodes(m.castle_logo_layer, nodes)
		elif m.castle_room_stage != null:
			_nodes(m.castle_room_stage, nodes)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path),
		"size": [image.get_width(), image.get_height()], "role": role,
		"snapshot": _snapshot(), "selected_canvas_nodes": nodes,
		"node_inventory_scope": "Selected current logo layer orCastle stage;visibility flags only,notallpixel/occlusion/native/wholegameclosure",
		"ticks_msec": Time.get_ticks_msec()})
	print("LOGO53|CAPTURE|", id)

func _check(label: String, ok: bool) -> void:
	checks.append({"label": label, "pass": ok, "ticks_msec": Time.get_ticks_msec()})
	if not ok:
		errors.append(label)

func _open_logo(prefix: String) -> bool:
	var record: Dictionary = m.castle_room_item_sprites.get("paint_table", {})
	var hotspot := record.get("hotspot") as Button
	var sprite := record.get("sprite") as Sprite2D
	if hotspot == null or sprite == null or m.castle_room_id != "craft_room":
		errors.append("original paint-table target unavailable")
		return false
	_check("original paint-table launch binding", String(sprite.get_meta("launch_activity", "")) == "castle_logo")
	await _capture(prefix + "_paint_table_before")
	await _tap(hotspot, hotspot.size * 0.5)
	if not await _wait(func() -> bool: return m.castle_logo_layer != null, 20.0):
		errors.append("original paint-table tap/walk/sequence did not open logo")
		return false
	await _frames(5)
	await _capture(prefix + "_logo_ready")
	return true

func _button(name: String) -> Button:
	return m.castle_logo_layer.find_child(name, true, false) as Button if m.castle_logo_layer != null else null

func _choose(color: String, symbol: String) -> void:
	var c := _button("CastleLogoColor_" + color)
	var s := _button("CastleLogoSymbol_" + symbol)
	if c == null or s == null:
		errors.append("original choice buttons unavailable")
		return
	await _tap(c, c.size * 0.5)
	await _tap(s, s.size * 0.5)
	_check("choice " + color + "/" + symbol,
		m.castle_logo_color == color and m.castle_logo_symbol == symbol)

func _back() -> bool:
	var button := m.global_navigation_button
	if button == null or not button.visible or button.disabled:
		errors.append("original global Back unavailable")
		return false
	await _tap(button, button.size * 0.5)
	return await _wait(func() -> bool: return m.castle_logo_layer == null, 5.0)

func _retire(flush := true) -> void:
	if is_instance_valid(m):
		if flush:
			m.notification(MainLoop.NOTIFICATION_APPLICATION_PAUSED)
		if current_scene == m:
			current_scene = null
		m.queue_free()
		await _frames(12)
	m = null

func _exercise() -> void:
	if not await _boot() or not await _open_logo("first"):
		return
	var original := [m.castle_logo_color, m.castle_logo_symbol]
	var rewards := [m.opera_stars, m.opera_progress, m.pearl_count]
	await _frames(30)
	await _capture("logo_passive")
	_check("passive doesnotchangechoice", [m.castle_logo_color, m.castle_logo_symbol] == original)
	for color: Dictionary in CastleLogoStudio.COLOR_CHOICES:
		for symbol: Dictionary in CastleLogoStudio.SYMBOL_CHOICES:
			var cid := String(color["id"])
			var sid := String(symbol["id"])
			await _choose(cid, sid)
			await _capture("choice_" + cid + "_" + sid)
	var pressed := _button("CastleLogoSymbol_heart")
	_touch(pressed, pressed.size * 0.5, true)
	await _frames(2)
	await _capture("symbol_heart_pressed")
	_touch(pressed, pressed.size * 0.5, false)
	await _frames(2)
	await _capture("symbol_heart_released")
	_check("actualBackclosesuncommitted", await _back())
	await _capture("cancel_restored")
	_check("cancelrestoresoriginalchoice", [m.castle_logo_color, m.castle_logo_symbol] == original)
	if not await _open_logo("commit"):
		return
	await _choose("purple", "dog")
	var finish := _button("CastleLogoFinishButton")
	await _tap(finish, finish.size * 0.5)
	await _capture("keep_feedback")
	_check("originalKeepcloses", await _wait(func() -> bool: return m.castle_logo_layer == null, 8.0))
	await _frames(4)
	await _capture("craft_committed_display")
	_check("actualKeepwriteschoice", _disk().get("color") == "purple" and _disk().get("symbol") == "dog")
	# JSON numbers load as floats; compare both unknown structures in the same JSON domain.
	var expected_unknown: Variant = JSON.parse_string(JSON.stringify(seed.get("flat_vector_private_unknown")))
	_check("unknownsavefieldpreserved", _disk().get("unknown") == expected_unknown)
	m._castle_rooms_ref().show_room("playroom", false)
	await _frames(5)
	await _capture("playroom_committed_display")
	m._castle_rooms_ref().show_room("library", false)
	await _frames(5)
	await _capture("library_unregistered_absence")
	_check("unregisteredlibraryhasnodisplay", m.castle_logo_room_display == null)
	m._castle_rooms_ref().show_room("craft_room", false)
	await _frames(5)
	if not await _open_logo("background_cancel"):
		return
	await _choose("gold", "star")
	await _capture("draft_before_background")
	m.notification(MainLoop.NOTIFICATION_APPLICATION_PAUSED)
	await _frames(3)
	await _capture("draft_after_background")
	m.notification(MainLoop.NOTIFICATION_APPLICATION_RESUMED)
	_check("Backafterbackgroundcloses", await _back())
	await _capture("background_cancel_restored")
	_check("backgroundcancelrestoresmemory", m.castle_logo_color == "purple" and m.castle_logo_symbol == "dog")
	var before_reload := FileAccess.get_sha256(profile)
	# Separate abrupt owned Main free: no extra lifecycle flush conceals disk state.
	await _retire(false)
	_check("abruptMainfreepreservesprivatediskbytes", FileAccess.get_sha256(profile) == before_reload)
	if not await _boot():
		return
	await _capture("fresh_main_loaded_display")
	_check("freshMainloadscommittedchoice", m.castle_logo_color == "purple" and m.castle_logo_symbol == "dog")
	if not await _open_logo("reload"):
		return
	await _capture("fresh_main_logo_reopened")
	_check("actualreopenpreviewkeepschoice", m.castle_logo_preview.get_meta("color_id") == "purple" and m.castle_logo_preview.get_meta("symbol_id") == "dog")
	_check("finalBackcloses", await _back())
	_check("norewardcounterchange", [m.opera_stars, m.opera_progress, m.pearl_count] == rewards)
	await _capture("final_craft_restored")
	await _retire()

func _point(c: Control, at: Vector2) -> Vector2:
	return c.get_global_transform_with_canvas() * at

func _touch(c: Control, at: Vector2, pressed: bool) -> void:
	var e := InputEventScreenTouch.new()
	e.index = 71
	e.position = _point(c, at)
	e.pressed = pressed
	events.append({"type": "touch", "pressed": pressed, "point": str(e.position), "local": str(at), "target": str(c.get_path()), "ticks_msec": Time.get_ticks_msec()})
	c.get_viewport().push_input(e, true)

func _drag(c: Control, at: Vector2) -> void:
	var e := InputEventScreenDrag.new()
	e.index = 71
	e.position = _point(c, at)
	events.append({"type": "drag", "point": str(e.position), "local": str(at), "target": str(c.get_path()), "ticks_msec": Time.get_ticks_msec()})
	c.get_viewport().push_input(e, true)

func _tap(c: Control, at: Vector2, id := "") -> void:
	_touch(c, at, true)
	await _frames(1)
	if not id.is_empty():
		await _capture(id + "_pressed")
	_touch(c, at, false)
	await _frames(2)
	if not id.is_empty():
		await _capture(id + "_released")

func _boot() -> bool:
	var packed := load("res://scenes/main.tscn") as PackedScene
	m = packed.instantiate() as ReefMain
	m._save_state = SaveState.new(m, profile)
	root.add_child(m)
	current_scene = m
	boot_count += 1
	await _frames(3)
	m._apply_quality("speedy")
	if not await _wait(func() -> bool: return m.get_node_or_null("BootSplashHandoff") == null, 15.0):
		errors.append("boot splash did not release")
		return false
	var button := m.start_menu_layer.find_child("StartMenuContinueButton", true, false) as Button if m.start_menu_layer != null else null
	if button != null and button.is_visible_in_tree() and not button.disabled:
		await _tap(button, button.size * 0.5)
	else:
		errors.append("actual Continue button unavailable")
		return false
	if m.intro_active:
		m._skip_intro()
	if not await _wait(func() -> bool: return not m.start_menu_active and not m.intro_active and m.fade_rect.modulate.a <= 0.02, 15.0):
		errors.append("startup presentation did not settle")
		return false
	if m._save_state.save_path != profile:
		errors.append("private save dependency did not remain bound")
		return false
	# The unchanged current probe uses this declared startup routing seam.
	# No phase,progress,target,clock or geometry is written by this fixture.
	m.game = "level2"
	m.g["t"] = 0.0
	m._enter_castle_interior_now(false)
	await _frames(3)
	m._castle_rooms_ref().show_room("craft_room", false)
	await _frames(3)
	return true

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless" or Engine.time_scale != 1.0:
		quit(1)
		return
	out_dir = OS.get_environment("R53_OUT")
	var width := int(OS.get_environment("R53_WIDTH"))
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "day_one_active": false, "day_one_giant_dust_bunny_boss_defeated": true, "day_one_completed_rooms": DayOneDirector.ROOM_ORDER, "day_one_cleaned_rooms": DayOneDirector.ROOM_ORDER, "day_one_giant_dust_bunny_boss_triggered": true, "chapter2_active": true, "chapter2_unlocked_opera_mask": 0x0449, "chapter2_job_phase_masks": [0, 0, 0, 0, 0, 0, 0, 0], "music": false, "mic": false, "quality": "speedy", "pearls": 23, "pearls_ever": 23, "flat_vector_private_unknown": {"token": "R53_PRIVATE_ONLY", "keep": [3, 7]}, "crafts": {}, "stickers": {}, "custom_fish": [], "custom_friends": []}
	var file := FileAccess.open(profile, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed, "\t", true) + "\n")
	file.close()
	if not await _aspect(Vector2i(width, 720)):
		errors.append("native viewport size did not settle")
	else:
		await _exercise()
	await _retire()
	if _normal_hashes() != normal_before:
		errors.append("normal eight save suffixes changed")
	var report := {"schema": "reef.castle_logo_context/1", "source_revision": OS.get_environment("R53_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "quality_requested": "speedy", "aspect": [width, 720], "time_scale": Engine.time_scale, "states": states, "events": events, "seed": seed, "private_profile": profile, "boot_count": boot_count, "mode": "ORIGINAL_CASTLE_LOGO_CONTROLS_PRIVATE_CHOICES", "checks": checks, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors, "actual_child_data": false, "normal_route_proved": false, "scope": "Actual original CraftRoom paint-table touch/walk/animation and crest buttons fromdeclaredprivate postboss/startup room API seam. No directopen/logo-state/phase/progress/clock/target/geometry/visual/source writes. Syntheticchoicecontentonly;actualchildsavesnevercopied. FreshMain same-engine profile reload isnotfreshOS/device/child/owner/QA11 orartacceptance."}
	var output := FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("LOGO53|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
