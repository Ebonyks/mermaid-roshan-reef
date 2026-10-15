extends SceneTree
## R60 original saved partial/full Critter Book; synthetic private checkpoint only.
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
var route_events: Array[Dictionary] = []
var saved_mode := ""
var expected_caught := 0

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
		var panel := node as Panel
		if panel != null:
			var panel_style: StyleBox = panel.get_theme_stylebox("panel")
			row["panel_style_class"] = panel_style.get_class()
			if panel_style is StyleBoxFlat:
				row["panel_fill"] = str((panel_style as StyleBoxFlat).bg_color)
				row["panel_border"] = str((panel_style as StyleBoxFlat).border_color)
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
	var value: Variant = JSON.parse_string(FileAccess.get_file_as_string(profile))
	if not value is Dictionary:
		return {}
	return {"critters": value.get("critters", value.get("critter_collection", {})), "unknown": value.get("flat_vector_private_unknown"), "save_generation": value.get("save_generation")}

func _snapshot() -> Dictionary:
	var result: Dictionary = {"normal_route_proved": false, "private_checkpoint": true, "time_scale": Engine.time_scale}
	if is_instance_valid(m):
		result.merge({"game": m.game, "phase": m.g.get("phase", ""), "room": m.castle_room_id, "quality": m.quality, "collection": m.critter_collection.duplicate(true), "category": m.collection_category, "caught_count": m._collection_ref().caught_count(), "book_exists": m.collection_layer != null, "stage_instance": m.collection_stage.get_instance_id() if m.collection_stage != null else 0, "book_layer_instance": m.collection_layer.get_instance_id() if m.collection_layer != null else 0, "collection_nodes": m.collection_nodes.size(), "retired_corner_button_null": m.collection_button == null and m.collection_button_layer == null, "pause_visible": m.pause_panel.visible, "tree_paused": paused, "navigation_top": m._navigation_ref().top_id(), "navigation_root": m.navigation_root_id, "global_navigation_mode": m.global_navigation_button.get_meta("global_navigation_mode", ""), "story_counters": [m.opera_stars, m.opera_progress, m.pearl_count], "world_control_blocks": m.touch_control_blocks.duplicate(true), "save_path": m._save_state.save_path, "disk": _disk(), "save_sha256": FileAccess.get_sha256(profile)})
	return result

func _capture(id: String, role := "CURRENT_ORIGINAL_CRITTER_BOOK_CONTEXT") -> void:
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var path: String = out_dir.path_join(id + ".png")
	if image == null or image.get_size() != root.size or image.save_png(path) != OK:
		errors.append("native capture failed " + id)
		return
	var nodes: Array[Dictionary] = []
	if is_instance_valid(m):
		for layer: CanvasLayer in [m.collection_layer, m.pause_layer]:
			if layer != null and is_instance_valid(layer):
				_nodes(layer, nodes)
		if m.global_navigation_button != null:
			_nodes(m.global_navigation_button, nodes)
		if m.castle_room_player_sprite != null:
			_nodes(m.castle_room_player_sprite, nodes)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path), "size": [image.get_width(), image.get_height()], "role": role, "snapshot": _snapshot(), "selected_canvas_nodes": nodes, "card_bindings": _book_rows(), "ticks_msec": Time.get_ticks_msec(), "node_inventory_scope": "Current book/pause roots, global navigation and Castle Roshan only; no full renderer/font/native/occlusion/QA11 closure."})
	print("CRITTER60|CAPTURE|", id)

func _check(label: String, ok: bool) -> void:
	checks.append({"label": label, "pass": ok, "ticks_msec": Time.get_ticks_msec()})
	if not ok:
		errors.append(label)

func _tab(category: String) -> Button:
	if m.collection_stage == null:
		return null
	for child: Node in m.collection_stage.get_children():
		var button: Button = child as Button
		if button != null and button.text.begins_with(String(CollectionSystem.CATEGORY_ICON[category])):
			return button
	return null

func _book_rows() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	if m.collection_stage == null:
		return result
	var defs: Array[Dictionary] = []
	for d: Dictionary in CollectionSystem.DEFS:
		if String(d["category"]) == m.collection_category:
			defs.append(d)
	for index: int in range(defs.size()):
		var expected := Vector2(82.0 + float(index % 3) * 388.0, 212.0 + float(index / 3) * 208.0)
		for child: Node in m.collection_stage.get_children():
			var panel: Panel = child as Panel
			if panel == null or panel.is_queued_for_deletion() or panel.position != expected or panel.size != Vector2(356.0, 192.0):
				continue
			var d: Dictionary = defs[index]
			var labels: Array[Dictionary] = []
			for node: Node in panel.get_children():
				var label: Label = node as Label
				if label == null:
					continue
				var role := "unbound"
				if label.position == Vector2(22.0, 23.0):
					role = "category_or_unknown_status"
				elif label.position == Vector2(122.0, 30.0):
					role = "species_name"
				elif label.position == Vector2(28.0, 134.0):
					role = "habitat"
				var font: Font = label.get_theme_font("font")
				labels.append({"role": role, "id": label.get_instance_id(), "path": str(label.get_path()), "text": label.text, "position": str(label.position), "size": str(label.size), "rect": str(label.get_global_rect()), "font_size": label.get_theme_font_size("font_size"), "font_class": font.get_class(), "font_path": font.resource_path, "text_width": font.get_string_size(label.text, HORIZONTAL_ALIGNMENT_LEFT, -1, label.get_theme_font_size("font_size")).x, "max_lines_visible": label.max_lines_visible})
			result.append({"id": String(d["id"]), "category": String(d["category"]), "name": String(d["name"]), "habitat": String(d["habitat"]), "caught": bool(m.critter_collection.get(String(d["id"]), false)), "source_index": index, "panel_id": panel.get_instance_id(), "panel_name": str(panel.name), "source_position": str(expected), "rect": str(panel.get_global_rect()), "style_class": panel.get_theme_stylebox("panel").get_class(), "labels": labels})
	return result

func _card_count() -> int:
	return _book_rows().size()

func _book_matches() -> bool:
	var rows := _book_rows()
	if rows.size() != 6:
		return false
	for row: Dictionary in rows:
		var labels: Array = row["labels"]
		if labels.size() != 3:
			return false
		for label: Dictionary in labels:
			var expected := ""
			if String(label["role"]) == "species_name":
				expected = String(row["name"]) if bool(row["caught"]) else "Mystery Friend"
			elif String(label["role"]) == "category_or_unknown_status":
				expected = String(CollectionSystem.CATEGORY_ICON[m.collection_category]) if bool(row["caught"]) else "?"
			elif String(label["role"]) == "habitat":
				expected = "%s  %s" % [String(CollectionSystem.HABITAT_ICON[String(row["habitat"])]), String(CollectionSystem.HABITAT_LABEL[String(row["habitat"])])]
			if expected.is_empty() or String(label["text"]) != expected:
				return false
	return true

func _open(id: String) -> bool:
	var nav: Button = m.global_navigation_button
	if String(nav.get_meta("global_navigation_mode", "")) != "menu":
		await _tap(nav, nav.size * 0.5)
		await _frames(45)
		await _capture(id + "_returned_root", "SOURCE_ASSISTED_ROOT_ROUTE_DIAGNOSTIC")
	if String(nav.get_meta("global_navigation_mode", "")) != "menu":
		errors.append("original navigation Menu unavailable " + id)
		return false
	await _tap(nav, nav.size * 0.5, id + "_menu")
	_check("original Menu opened " + id, m.pause_panel.visible and paused)
	var button: Button = m.pause_panel.find_child("MenuCritterBookButton", true, false) as Button
	if button == null or not button.is_visible_in_tree():
		errors.append("original Pause Critter Book button unavailable " + id)
		return false
	await _tap(button, button.size * 0.5, id + "_book")
	_check("Pause Critters callback owns live book " + id, m.collection_layer != null and m.collection_stage != null and m._navigation_ref().top_id() == "critter_book" and not paused and not m.pause_panel.visible)
	return m.collection_layer != null

func _back(id: String) -> void:
	var nav: Button = m.global_navigation_button
	_check("original Book Back visible " + id, nav.is_visible_in_tree() and String(nav.get_meta("global_navigation_mode", "")) == "back")
	await _tap(nav, nav.size * 0.5, id + "_back")
	await _frames(4)
	_check("original Book Back retires book " + id, m.collection_layer == null and m.collection_stage == null and m._navigation_ref().top_id() != "critter_book")

func _state_equal(left: Variant, right: Variant) -> bool:
	return JSON.parse_string(JSON.stringify(left)) == JSON.parse_string(JSON.stringify(right))

func _exercise() -> void:
	if not await _boot():
		return
	await _capture("castle_private_checkpoint", "BOOTSTRAP_DIAGNOSTIC")
	var collection_before: Dictionary = m.critter_collection.duplicate(true)
	var counters_before: Array = [m.opera_stars, m.opera_progress, m.pearl_count]
	_check("synthetic saved collection loaded through original SaveState", _state_equal(collection_before, seed["critters"]) and m._collection_ref().caught_count() == expected_caught)
	if not await _open("initial"):
		return
	_check("original initial category fish", m.collection_category == "fish" and _card_count() == 6)
	_check("initial saved-card labels bind exact source roles", _book_matches())
	await _capture("fish_ready")
	var selected_tab: Button = _tab("fish")
	await _tap(selected_tab, selected_tab.size * 0.5, "same_category_repeat")
	_check("same category repeat preserves original page and saved collection", m.collection_category == "fish" and m.critter_collection == collection_before)
	_check("same category repeat keeps six exact source-bound cards", _book_matches())
	await _capture("same_category_repeat_settled")
	for category: String in ["insect", "bird", "fish"]:
		var tab: Button = _tab(category)
		if tab == null or not tab.is_visible_in_tree():
			errors.append("original category tab absent " + category)
			return
		await _tap(tab, tab.size * 0.5, "category_" + category)
		_check("original tab updates category " + category, m.collection_category == category and _card_count() == 6)
		_check("saved-card labels bind category " + category, _book_matches())
		await _capture(category + "_settled")
		_check("category touch preserves collection " + category, m.critter_collection == collection_before)
	m.notification(MainLoop.NOTIFICATION_APPLICATION_PAUSED)
	await _frames(3)
	await _capture("book_application_pause_notification")
	m.notification(MainLoop.NOTIFICATION_APPLICATION_RESUMED)
	await _frames(3)
	await _capture("book_application_resume_notification")
	_check("notification preserves original book/category/progress", m.collection_layer != null and m.collection_category == "fish" and m.critter_collection == collection_before)
	await _back("initial")
	if not await _open("reopen"):
		return
	_check("reopen resets fish without collection loss", m.collection_category == "fish" and m.critter_collection == collection_before)
	_check("reopen saved-card labels bind exact source roles", _book_matches())
	await _capture("reopen_fish_ready")
	await _back("reopen")
	_check("book browsing preserves story counters", [m.opera_stars, m.opera_progress, m.pearl_count] == counters_before)
	await _retire()
	if not await _boot():
		return
	await _capture("fresh_main_private_checkpoint", "BOOTSTRAP_DIAGNOSTIC")
	_check("fresh Main preserves saved collection", m.critter_collection == collection_before)
	if not await _open("reload"):
		return
	_check("fresh Main saved-card labels bind exact source roles", _book_matches())
	await _capture("fresh_main_book_fish")
	_check("future critter save key retained false", m.critter_collection.has("r60_future_species") and m.critter_collection["r60_future_species"] == false)
	_check("private unknown key retained", _state_equal(_disk().get("unknown"), seed.get("flat_vector_private_unknown")))
	_check("no retired world critters constructed for book", m.collection_nodes.is_empty())
	await _back("reload")
	await _retire()

func _retire(flush := true) -> void:
	if is_instance_valid(m):
		if flush:
			m.notification(MainLoop.NOTIFICATION_APPLICATION_PAUSED)
		if current_scene == m:
			current_scene = null
		m.queue_free()
		await _frames(12)
	m = null

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
	# Explicit pre-activity world routing initialization; no measured action clock/phase/progress/target writes.
	m.game = "level2"
	m.g["t"] = 0.0
	m._enter_castle_interior_now(false)
	await _frames(40)
	return true

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless" or Engine.time_scale != 1.0:
		quit(1)
		return
	out_dir = OS.get_environment("R60_OUT")
	var width := int(OS.get_environment("R60_WIDTH"))
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	saved_mode = OS.get_environment("R60_COLLECTION_MODE")
	if saved_mode not in ["partial", "full"]:
		quit(1)
		return
	expected_caught = 6 if saved_mode == "partial" else 18
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "day_one_active": false, "day_one_giant_dust_bunny_boss_defeated": true, "day_one_completed_rooms": DayOneDirector.ROOM_ORDER, "day_one_cleaned_rooms": DayOneDirector.ROOM_ORDER, "day_one_giant_dust_bunny_boss_triggered": true, "chapter2_active": true, "chapter2_unlocked_opera_mask": 0x0449, "chapter2_job_phase_masks": [0, 0, 0, 0, 0, 0, 0, 0], "music": false, "mic": false, "quality": "speedy", "pearls": 23, "pearls_ever": 23, "flat_vector_private_unknown": {"token": "R60_PRIVATE_ONLY", "keep": [3, 7]}, "crafts": {}, "stickers": {}, "custom_fish": [], "custom_friends": []}
	var saved_critters: Dictionary = {"r60_future_species": false}
	for index: int in range(CollectionSystem.DEFS.size()):
		if saved_mode == "full" or index in [0, 2, 6, 11, 13, 17]:
			var definition: Dictionary = CollectionSystem.DEFS[index]
			saved_critters[String(definition["id"])] = true
	seed["critters"] = saved_critters
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
	var report := {"schema": "reef.critter_book_context/1", "source_revision": OS.get_environment("R60_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "quality_requested": "speedy", "aspect": [width, 720], "time_scale": Engine.time_scale, "states": states, "events": events, "seed": seed, "private_profile": profile, "boot_count": boot_count, "route_events": route_events, "mode": "ORIGINAL_PAUSE_CRITTER_BOOK_SAVED_STATE_INPUTS", "saved_mode": saved_mode, "expected_caught": expected_caught, "checks": checks, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors, "actual_child_data": false, "normal_route_proved": false, "scope": "Actual global Menu, Pause Critters callback, category tabs, Back/reopen and private same-engine Main reload after declared private postboss Castle bootstrap m.game=level2/m.g[t]=0. No collection/category/progress/target/geometry/visual/source writes around measured transitions. Partial/full synthetic critters dictionary written to private profile before Main instantiation; original SaveState consumes it. No catch-world route/award input is demonstrated. Actual child saves never copied/seeded. FreshMain same-engine profile reload isnotfreshOS/device/child/owner/QA11 orartacceptance."}
	var output := FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("CRITTER60|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
