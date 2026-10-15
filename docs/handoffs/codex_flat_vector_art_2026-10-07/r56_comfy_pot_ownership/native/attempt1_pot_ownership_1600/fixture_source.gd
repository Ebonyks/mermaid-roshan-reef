extends SceneTree
## R56 source-exact Kitchen pot ownership. Original input; synthetic private data only.
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
		var row := {"path": str(node.get_path()), "class": node.get_class(), "script": node.get_script().resource_path if node.get_script() != null else "", "z_index": item.z_index, "z_as_relative": item.z_as_relative, "global_transform_with_canvas": str(item.get_global_transform_with_canvas()), "modulate": str(item.modulate), "self_modulate": str(item.self_modulate)}
		var c := node as Control
		if c != null:
			row["global_rect"] = str(c.get_global_rect())
			row["mouse_filter"] = c.mouse_filter
		var sprite := node as Sprite2D
		if sprite != null:
			row["texture"] = _tex(sprite.texture)
			row["frame"] = sprite.frame
			row["hframes"] = sprite.hframes
			row["vframes"] = sprite.vframes
			row["region_enabled"] = sprite.region_enabled
			row["region_rect"] = str(sprite.region_rect)
			row["source_rect"] = str(sprite.get_rect())
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
		var metadata: Dictionary = {}
		for key: StringName in node.get_meta_list():
			metadata[String(key)] = str(node.get_meta(key))
		row["metadata_as_strings"] = metadata
		rows.append(row)
	for child: Node in node.get_children():
		_nodes(child, rows)

func _disk() -> Dictionary:
	var value: Variant = JSON.parse_string(FileAccess.get_file_as_string(profile))
	if not value is Dictionary:
		return {}
	return {"comfy": value.get("comfy_games", {}), "stickers": value.get("stickers", {}),
		"unknown": value.get("flat_vector_private_unknown"), "save_generation": value.get("save_generation")}

func _snapshot() -> Dictionary:
	var result := {"normal_route_proved": false, "private_checkpoint": true, "time_scale": Engine.time_scale}
	if is_instance_valid(m):
		result.merge({"game": m.game, "room": m.castle_room_id, "quality": m.quality,
			"comfy": m.comfy_games_state.duplicate(true), "stickers": m.stickers.duplicate(true),
			"story_counters": [m.opera_stars, m.opera_progress, m.pearl_count],
			"castle_dust_bunnies_cleared": (m.g.get("castle_dust_bunnies_cleared", {}) as Dictionary).duplicate(true),
			"navigation_top": m._navigation_ref().top_id(), "day_one_active": m.day_one_is_active(),
			"save_pending": m.save_pending, "save_dirty": m.save_dirty, "save_path": m._save_state.save_path,
			"disk": _disk(), "save_sha256": FileAccess.get_sha256(profile),
			"player_foot": str(m.castle_room_player_sprite.get_meta("current_stage_foot", Vector2.INF)) if m.castle_room_player_sprite != null else "absent"})
	return result

func _capture(id: String, role := "CURRENT_ORIGINAL_POT_OWNERSHIP_CONTEXT") -> void:
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != root.size or image.save_png(path) != OK:
		errors.append("native capture failed " + id)
		return
	var nodes: Array[Dictionary] = []
	var draw_owners: Array[Dictionary] = []
	if is_instance_valid(m):
		if m.castle_room_stage != null:
			_nodes(m.castle_room_stage, draw_owners)
		var comfy := m._comfy_games_ref().castle_root
		if comfy != null and is_instance_valid(comfy):
			_nodes(comfy, nodes)
		if m.castle_room_player_sprite != null:
			_nodes(m.castle_room_player_sprite, nodes)
		if m.global_navigation_button != null:
			_nodes(m.global_navigation_button, nodes)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path),
		"size": [image.get_width(), image.get_height()], "role": role, "snapshot": _snapshot(),
		"selected_canvas_nodes": nodes, "visible_stage_nodes": draw_owners, "ticks_msec": Time.get_ticks_msec(),
		"node_inventory_scope": "Visible Castle room stage Canvas tree plus Comfy/player/Back; hidden/native/dynamic resource closure and QA11 remain open."})
	print("POT56|CAPTURE|", id)

func _check(label: String, ok: bool) -> void:
	checks.append({"label": label, "pass": ok, "ticks_msec": Time.get_ticks_msec()})
	if not ok:
		errors.append(label)

func _button(name: String) -> Control:
	return m.find_child(name, true, false) as Control

func _screen_touch(point: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 71
	event.position = point
	event.pressed = pressed
	events.append({"type": "floor_touch", "pressed": pressed, "point": str(point), "ticks_msec": Time.get_ticks_msec()})
	root.push_input(event, true)

func _door(room: String) -> bool:
	var pearl_before := m.pearl_count
	var dust_before: Dictionary = (m.g.get("castle_dust_bunnies_cleared", {}) as Dictionary).duplicate(true)
	for attempt: int in range(15):
		var button := _button("HallDoor_" + room)
		if button == null:
			errors.append("original hall door absent " + room)
			return false
		var point := _point(button, button.size * 0.5)
		if button.is_visible_in_tree() and point.x > 35.0 and point.x < float(root.size.x) - 35.0 and point.y > 20.0 and point.y < 700.0:
			await _tap(button, button.size * 0.5)
			if not await _wait(func() -> bool: return m.castle_room_id == room, 25.0):
				errors.append("original hall door did not enter " + room)
				return false
			await _frames(12)
			route_events.append({"type": "ORIGINAL_HALL_DOOR", "room": room, "button": "HallDoor_" + room, "pearl_before": pearl_before, "pearl_after": m.pearl_count, "dust_before": dust_before, "dust_after": (m.g.get("castle_dust_bunnies_cleared", {}) as Dictionary).duplicate(true)})
			await _capture("entered_" + room + "_" + str(route_events.size()))
			return true
		var target_foot := Vector2.INF
		for record: Dictionary in m.castle_room_door_hotspots:
			var data: Dictionary = record.get("data", {})
			if String(data.get("id", "")) == room:
				target_foot = data.get("foot", Vector2.INF) as Vector2
				break
		var current_foot: Vector2 = m.castle_room_player_sprite.get_meta("current_stage_foot", Vector2.INF) as Vector2
		if not target_foot.is_finite() or not current_foot.is_finite():
			errors.append("source portal/player foot unavailable " + room)
			return false
		var walk_point := Vector2(float(root.size.x) * (0.84 if target_foot.x > current_foot.x else 0.16), 650.0)
		_screen_touch(walk_point, true)
		await _frames(1)
		_screen_touch(walk_point, false)
		await _frames(90)
	errors.append("original floor walking did not reach door " + room)
	return false

func _go_room(room: String) -> bool:
	if m.castle_room_id == room:
		return true
	for attempt: int in range(4):
		if m.castle_room_id == "main_hall":
			break
		var before := m.castle_room_id
		var back := m.global_navigation_button
		if back == null or not back.visible or back.disabled:
			errors.append("original global Back unavailable from " + before)
			return false
		await _tap(back, back.size * 0.5)
		if not await _wait(func() -> bool: return m.castle_room_id != before, 8.0):
			errors.append("original Back did not leave " + before)
			return false
		await _frames(6)
		route_events.append({"type": "ORIGINAL_GLOBAL_BACK", "from": before, "to": m.castle_room_id})
	if m.castle_room_id != "main_hall":
		errors.append("original Back did not reach Main Hall")
		return false
	if room in ["movie_lounge", "sleepover_bedroom"]:
		if not await _door("family_gallery"):
			return false
		var id := "gallery_movie_door" if room == "movie_lounge" else "gallery_sleepover_door"
		var record: Dictionary = m.castle_room_item_sprites.get(id, {})
		var hotspot := record.get("hotspot") as Button
		if hotspot == null:
			errors.append("original gallery door unavailable " + id)
			return false
		await _tap(hotspot, hotspot.size * 0.5)
		if not await _wait(func() -> bool: return m.castle_room_id == room, 25.0):
			errors.append("original gallery door did not enter " + room)
			return false
		await _frames(12)
		route_events.append({"type": "ORIGINAL_GALLERY_DOOR", "room": room, "item": id})
		await _capture("entered_" + room + "_" + str(route_events.size()))
		return true
	return await _door(room)

func _act(name: String, id: String) -> bool:
	var counters_before := [m.opera_stars, m.opera_progress, m.pearl_count]
	var button := _button(name)
	if button == null or not button.is_visible_in_tree():
		errors.append("original Comfy target unavailable " + name)
		await _capture(id + "_target_absent", "FAILED_ORIGINAL_TARGET_DIAGNOSTIC")
		return false
	await _capture(id + "_before")
	_touch(button, button.size * 0.5, true)
	await _frames(1)
	await _capture(id + "_pressed")
	_touch(button, button.size * 0.5, false)
	await _frames(3)
	await _capture(id + "_released")
	_check("Comfy action preserves story counters " + id, [m.opera_stars, m.opera_progress, m.pearl_count] == counters_before)
	return true

func _state_equal(left: Variant, right: Variant) -> bool:
	return JSON.parse_string(JSON.stringify(left)) == JSON.parse_string(JSON.stringify(right))

func _exercise() -> void:
	if not await _boot():
		return
	await _capture("main_hall_checkpoint", "ORIGINAL_ROUTE_DIAGNOSTIC")
	if not await _go_room("kitchen"):
		return
	var initial := m.comfy_games_state.duplicate(true)
	_check("private checkpoint leaves dinner incomplete", not bool(initial[ComfyGames.DAY_TWO_FAMILY_EVENING]["dinner"]["completed"]))
	_check("original pot target exists", _button("ComfyDinnerSoupPot") != null)
	await _capture("pot_original_owners")
	await _frames(45)
	_check("passive pot state unchanged", m.comfy_games_state == initial)
	await _capture("pot_original_passive")
	m.notification(MainLoop.NOTIFICATION_APPLICATION_PAUSED)
	await _frames(3)
	await _capture("pot_background")
	m.notification(MainLoop.NOTIFICATION_APPLICATION_RESUMED)
	_check("background preserves incomplete dinner", m.comfy_games_state == initial and _state_equal(_disk().get("comfy"), initial))
	var before := FileAccess.get_sha256(profile)
	await _retire(false)
	_check("owned Main free keeps private disk exact", FileAccess.get_sha256(profile) == before)
	if not await _boot() or not await _go_room("kitchen"):
		return
	_check("same engine reload preserves incomplete dinner", m.comfy_games_state == initial)
	await _capture("pot_reloaded_owners")
	if not await _act("ComfyDinnerSoupPot", "original_stir"):
		return
	_check("original stir completes dinner", bool(m.comfy_games_state[ComfyGames.DAY_TWO_FAMILY_EVENING]["dinner"]["completed"]))
	_check("pot target retired after original completion", _button("ComfyDinnerSoupPot") == null)
	await _frames(25)
	await _capture("completed_underlay_owners")
	var complete := m.comfy_games_state.duplicate(true)
	_check("original completion persisted", _state_equal(_disk().get("comfy"), complete))
	_check("private unknown key survives", _state_equal(_disk().get("unknown"), seed.get("flat_vector_private_unknown")))
	if not await _go_room("library") or not await _go_room("kitchen"):
		return
	_check("return keeps completed state and target absent", m.comfy_games_state == complete and _button("ComfyDinnerSoupPot") == null)
	await _capture("repeat_completed_underlay")
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
	out_dir = OS.get_environment("R56_OUT")
	var width := int(OS.get_environment("R56_WIDTH"))
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "day_one_active": false, "day_one_giant_dust_bunny_boss_defeated": true, "day_one_completed_rooms": DayOneDirector.ROOM_ORDER, "day_one_cleaned_rooms": DayOneDirector.ROOM_ORDER, "day_one_giant_dust_bunny_boss_triggered": true, "chapter2_active": true, "chapter2_unlocked_opera_mask": 0x0449, "chapter2_job_phase_masks": [0, 0, 0, 0, 0, 0, 0, 0], "music": false, "mic": false, "quality": "speedy", "pearls": 23, "pearls_ever": 23, "flat_vector_private_unknown": {"token": "R56_PRIVATE_ONLY", "keep": [3, 7]}, "crafts": {}, "stickers": {}, "custom_fish": [], "custom_friends": []}
	seed["comfy_games"] = JSON.parse_string(FileAccess.get_file_as_string("res://export/flat_vector_r56/pot_checkpoint.json"))
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
	var report := {"schema": "reef.comfy_pot_ownership/1", "source_revision": OS.get_environment("R56_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "quality_requested": "speedy", "aspect": [width, 720], "time_scale": Engine.time_scale, "states": states, "events": events, "seed": seed, "private_profile": profile, "boot_count": boot_count, "route_events": route_events, "mode": "ORIGINAL_KITCHEN_POT_OWNERSHIP", "checks": checks, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors, "actual_child_data": false, "normal_route_proved": false, "scope": "Current Kitchen pot visible Canvas draw owners and original controls after declared private pot-ready checkpoint and startup m.game=level2,m.g[t]=0. No measured action-clock/progress/target/visual/source writes. Current runtime ownership may differ from historical V4 rejected cutout scope. Same-engine reload is not cold OS/device/child/owner/QA11/art acceptance."}
	var output := FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("POT56|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
