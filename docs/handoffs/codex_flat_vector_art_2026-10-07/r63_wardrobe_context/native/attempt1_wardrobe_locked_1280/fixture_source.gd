extends SceneTree
## R63 original Wardrobe current-context audit. Private synthetic profile, original inputs only.
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
var fairy_unlocked := false

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
	var value: Variant = JSON.parse_string(FileAccess.get_file_as_string(profile))
	if not value is Dictionary:
		return {}
	return {"comfy": value.get("comfy_games", {}), "stickers": value.get("stickers", {}),
		"unknown": value.get("flat_vector_private_unknown"), "save_generation": value.get("save_generation")}

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
	if room in ["movie_lounge", "sleepover_bedroom", "royal_bedroom"]:
		if not await _door("family_gallery"):
			return false
		var id: String = "gallery_movie_door" if room == "movie_lounge" else ("gallery_royal_bedroom_door" if room == "royal_bedroom" else "gallery_sleepover_door")
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

func _state_equal(left: Variant, right: Variant) -> bool:
	return JSON.parse_string(JSON.stringify(left)) == JSON.parse_string(JSON.stringify(right))

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

func _texture_evidence(texture: Texture2D) -> Dictionary:
	var row: Dictionary = _tex(texture)
	if texture is ImageTexture:
		var image: Image = texture.get_image()
		if image != null:
			var hash := HashingContext.new()
			hash.start(HashingContext.HASH_SHA256)
			hash.update(image.get_data())
			row["runtime_pixel_sha256"] = hash.finish().hex_encode()
			row["pixel_format"] = image.get_format()
	return row

func _feedback() -> Dictionary:
	var layer: Control = m.wd.get("feedback_layer") as Control
	var rows: Array[Dictionary] = []
	if layer != null and is_instance_valid(layer):
		for child: Node in layer.get_children():
			var burst := child as Control
			if burst == null or not is_instance_valid(burst):
				continue
			var shapes: Array[Dictionary] = []
			for index: int in range(burst.get_child_count()):
				var poly := burst.get_child(index) as Polygon2D
				if poly != null:
					shapes.append({"logical_instance": "wardrobe.feedback.star.%02d" % index,
						"id": poly.get_instance_id(), "polygon": str(poly.polygon),
						"position": str(poly.position), "rotation": poly.rotation,
						"scale": str(poly.scale), "color": str(poly.color),
						"modulate": str(poly.modulate), "visible": poly.is_visible_in_tree(),
						"endpoint": str(poly.get_meta("feedback_endpoint", Vector2.ZERO))})
			rows.append({"id": burst.get_instance_id(), "name": burst.name,
				"position": str(burst.position), "visible": burst.is_visible_in_tree(),
				"kind": str(burst.get_meta("feedback_kind", "")), "shapes": shapes})
	return {"burst_count": rows.size(), "bursts": rows}

func _snapshot() -> Dictionary:
	if not is_instance_valid(m):
		return {}
	var looks: Array[Dictionary] = []
	var value: Variant = m.wd.get("btns", [])
	if value is Array:
		for entry_value: Variant in value:
			if not entry_value is Dictionary:
				continue
			var entry: Dictionary = entry_value as Dictionary
			var button: Button = entry.get("btn") as Button
			if button == null or not is_instance_valid(button):
				continue
			var callbacks: Array[Dictionary] = []
			for connection: Dictionary in button.get_signal_connection_list("pressed"):
				var callback: Callable = connection["callable"] as Callable
				callbacks.append({"method": str(callback.get_method()), "object_id": callback.get_object_id()})
			var style: StyleBox = button.get_theme_stylebox("normal")
			var portrait: TextureRect = button.find_child("WardrobeLookPreview_" + String(entry["id"]), false, false) as TextureRect
			looks.append({"skin": entry["id"], "id": button.get_instance_id(),
				"name": button.name, "text": button.text, "rect": str(button.get_global_rect()),
				"size": str(button.size), "minimum_size": str(button.custom_minimum_size),
				"visible": button.is_visible_in_tree(), "pressed": button.is_pressed(),
				"focus": button.has_focus(), "disabled": button.disabled,
				"mouse_filter": button.mouse_filter, "selected": button.get_meta("selected", false),
				"locked": button.get_meta("locked", false), "style": style.get_class(),
				"callbacks": callbacks, "portrait": _texture_evidence(portrait.texture) if portrait != null else {}})
	var preview_value: Variant = m.wd.get("preview")
	var preview: TextureRect = preview_value as TextureRect if is_instance_valid(preview_value) else null
	var items: Array[Dictionary] = []
	for id_value: Variant in m.castle_room_item_sprites:
		var record: Dictionary = m.castle_room_item_sprites[id_value] as Dictionary
		var sprite: Sprite2D = record.get("sprite") as Sprite2D
		var hotspot: Button = record.get("hotspot") as Button
		var data: Dictionary = record.get("data", {}) as Dictionary
		items.append({"id": str(id_value), "sprite_id": sprite.get_instance_id() if sprite != null else 0,
			"texture": _texture_evidence(sprite.texture) if sprite != null else {},
			"sprite_rect": str(sprite.get_rect()) if sprite != null else "",
			"sprite_position": str(sprite.position) if sprite != null else "",
			"sprite_scale": str(sprite.scale) if sprite != null else "",
			"busy": sprite.get_meta("busy", false) if sprite != null else false,
			"source_object_id": str(sprite.get_meta("source_object_id", "")) if sprite != null else "",
			"hotspot_id": hotspot.get_instance_id() if hotspot != null else 0,
			"hotspot_rect": str(hotspot.get_global_rect()) if hotspot != null else "",
			"hotspot_visible": hotspot.is_visible_in_tree() if hotspot != null else false,
			"roleplay_action": str(data.get("roleplay_action", "")),
			"room_destination": str(data.get("room_destination", "")),
			"launch_activity": str(data.get("launch_activity", "")),
			"native_pack": str((data.get("v2_visual", {}) as Dictionary).get("pack", ""))})
	var figure: Sprite2D = m.castle_room_player_sprite
	return {"game": m.game, "phase": str(m.g.get("phase", "")), "room": m.castle_room_id,
		"skin": m.skin_id, "fairy_unlocked": m.fairy_skin_unlocked,
		"wardrobe_exists": m.wardrobe_layer != null, "wardrobe_layer_id": m.wardrobe_layer.get_instance_id() if m.wardrobe_layer != null else 0,
		"wardrobe_layer": m.wardrobe_layer.layer if m.wardrobe_layer != null else 0,
		"wd_keys": m.wd.keys(), "fashion_child": m.wd.has(FashionWardrobe.PERSON),
		"looks": looks, "preview": _texture_evidence(preview.texture) if preview != null else {},
		"preview_rect": str(preview.get_global_rect()) if preview != null else "",
		"feedback": _feedback(), "room_items": items,
		"room_player": {"visible": figure.is_visible_in_tree(), "texture": _texture_evidence(figure.texture),
			"position": str(figure.position), "scale": str(figure.scale),
			"foot": str(figure.get_meta("current_stage_foot", Vector2.INF))} if figure != null else {},
		"navigation_top": m._navigation_ref().top_id(), "caption_timer": m.msg_timer, "story_counters": [m.opera_stars, m.opera_progress, m.pearl_count],
		"disk": _disk(), "save_path": m._save_state.save_path, "save_sha256": FileAccess.get_sha256(profile),
		"normal_route_proved": false, "private_checkpoint": true,
		"quality": str(m.quality), "time_scale": Engine.time_scale,
		"world_control_blocks": m.touch_control_blocks.duplicate(true)}

func _capture(id: String, role := "CURRENT_ORIGINAL_WARDROBE_CONTEXT") -> void:
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != root.size or image.save_png(path) != OK:
		errors.append("native capture failed " + id)
		return
	var nodes: Array[Dictionary] = []
	if is_instance_valid(m):
		if m.wardrobe_layer != null:
			_nodes(m.wardrobe_layer, nodes)
		if m.castle_room_player_sprite != null:
			_nodes(m.castle_room_player_sprite, nodes)
		if m.global_navigation_button != null:
			_nodes(m.global_navigation_button, nodes)
	states.append({"id": id, "path": id + ".png", "sha256": FileAccess.get_sha256(path),
		"size": [image.get_width(), image.get_height()], "role": role, "snapshot": _snapshot(),
		"selected_canvas_nodes": nodes, "ticks_msec": Time.get_ticks_msec(),
		"node_inventory_scope": "Original Wardrobe layer/player/Back plus room-item metadata; full PNG retained. No full compositor/resource/occlusion/QA11 closure."})
	print("WARDROBE63|CAPTURE|", id)

func _open_original_wardrobe(id: String) -> bool:
	var record: Dictionary = m.castle_room_item_sprites.get("shell_wardrobe", {}) as Dictionary
	var hotspot: Button = record.get("hotspot") as Button
	if hotspot == null or not hotspot.is_visible_in_tree():
		errors.append("original shell wardrobe hotspot missing")
		return false
	await _tap(hotspot, hotspot.size * 0.5, id + "_world_target")
	if not await _wait(func() -> bool: return m.wardrobe_layer != null, 25.0):
		errors.append("original source hotspot did not open Wardrobe")
		return false
	await _capture(id + "_opened")
	if not await _wait(func() -> bool: return m.msg_timer <= 0.0, 15.0):
		errors.append("original caption did not naturally expire")
		return false
	await _frames(3)
	await _capture(id + "_caption_settled")
	_check("original wardrobe has3look buttons " + id, (m.wd.get("btns", []) as Array).size() == 3)
	return true

func _pick_original(skin: String, id: String) -> bool:
	var button: Button = _button("WardrobeLook_" + skin) as Button
	if button == null or not button.is_visible_in_tree() or button.disabled:
		errors.append("original look button missing " + skin)
		return false
	var counters: Array = [m.opera_stars, m.opera_progress, m.pearl_count]
	await _tap(button, button.size * 0.5, id)
	_check("look input preserves story counters " + id, [m.opera_stars, m.opera_progress, m.pearl_count] == counters)
	return true

func _exercise() -> void:
	if not await _boot():
		return
	_check("synthetic original skin/unlock profile loaded", m.skin_id == "classic" and m.fairy_skin_unlocked == fairy_unlocked)
	await _capture("main_hall_checkpoint", "ORIGINAL_ROUTE_DIAGNOSTIC")
	if not await _go_room("royal_bedroom"):
		return
	_check("original Royal Bedroom route entered", m.castle_room_id == "royal_bedroom" and m.wardrobe_layer == null)
	await _capture("royal_bedroom_before_wardrobe")
	await _frames(30)
	_check("passive room does not select or open Wardrobe", m.skin_id == "classic" and m.wardrobe_layer == null)
	if not await _open_original_wardrobe("initial"):
		return
	var fairy_button: Button = _button("WardrobeLook_fairy") as Button
	_check("original fairy lock matches saved profile", fairy_button != null and bool(fairy_button.get_meta("locked", false)) == (not fairy_unlocked))
	if not await _pick_original("fairy", "fairy_choice"):
		return
	if fairy_unlocked:
		_check("unlocked original Fairy choice selected/saved", m.skin_id == "fairy" and str(_disk().get("skin", "")) == "fairy")
		_check("source pick uses one14instance feedback burst", int(_feedback()["burst_count"]) == 1 and ((_feedback()["bursts"] as Array)[0]["shapes"] as Array).size() == 14)
	else:
		_check("locked choice does not grant skin/unlock", m.skin_id == "classic" and not m.fairy_skin_unlocked and str(_disk().get("skin", "classic")) != "fairy")
		_check("locked choice has no pick feedback burst", int(_feedback()["burst_count"]) == 0)
	await _frames(9)
	await _capture("fairy_choice_early")
	await _frames(90)
	await _capture("fairy_choice_settled")
	_check("source pick feedback naturally retires", int(_feedback()["burst_count"]) == 0)
	if not await _pick_original("huluu", "huluu_choice"):
		return
	_check("existing Huluu option selected via originalUI only", m.skin_id == "huluu" and str(_disk().get("skin", "")) == "huluu")
	_check("source feedback count bounded after Huluu", int(_feedback()["burst_count"]) <= 1)
	await _frames(9)
	await _capture("huluu_choice_early")
	await _frames(30)
	await _capture("huluu_choice_settled")
	for index: int in range(3):
		if not await _pick_original("huluu", "repeat_huluu_" + str(index)):
			return
		_check("rapid repeat retains atmostone original burst " + str(index), int(_feedback()["burst_count"]) <= 1)
	await _frames(30)
	await _capture("rapid_repeat_settled")
	var done: Control = _button("WardrobeFinishButton")
	if done == null:
		errors.append("source Done missing")
		return
	await _tap(done, done.size * 0.5, "done_huluu")
	_check("source Done closes Wardrobe and retains saved look", m.wardrobe_layer == null and m.castle_room_id == "royal_bedroom" and m.skin_id == "huluu" and not m.touch_control_blocks.has("wardrobe"))
	await _capture("huluu_world_after_done")
	if not await _open_original_wardrobe("reopen"):
		return
	_check("source reopen retains chosen look", m.skin_id == "huluu")
	m.notification(MainLoop.NOTIFICATION_APPLICATION_PAUSED)
	await _frames(3)
	await _capture("wardrobe_application_pause_notification")
	m.notification(MainLoop.NOTIFICATION_APPLICATION_RESUMED)
	await _frames(3)
	await _capture("wardrobe_application_resume_notification")
	_check("source notifications retain private look/unlock", str(_disk().get("skin", "")) == "huluu" and bool(_disk().get("fairyskin", false)) == fairy_unlocked)
	var disk_before: String = FileAccess.get_sha256(profile)
	await _retire(false)
	_check("ownedMainretirement preserves saved disk", FileAccess.get_sha256(profile) == disk_before)
	if not await _boot():
		return
	_check("fresh same-engine Main loads original chosen look", m.skin_id == "huluu" and m.fairy_skin_unlocked == fairy_unlocked)
	await _capture("fresh_main_checkpoint", "PRIVATE_RELOAD_ROUTE_DIAGNOSTIC")
	if not await _go_room("royal_bedroom") or not await _open_original_wardrobe("reload"):
		return
	_check("source reload book retains same selected look", m.skin_id == "huluu")
	if not await _pick_original("classic", "restore_classic"):
		return
	_check("originalUI restores classic/saves without unlock change", m.skin_id == "classic" and str(_disk().get("skin", "")) == "classic" and m.fairy_skin_unlocked == fairy_unlocked)
	await _frames(30)
	await _capture("classic_restored_settle")
	var clothes: Control = _button("FashionWardrobeButton")
	if clothes == null:
		errors.append("source Fashion entry button missing")
		return
	await _tap(clothes, clothes.size * 0.5, "fashion_child")
	_check("source Fashion child entry uses existing owner", m.wardrobe_layer != null and m.wd.has(FashionWardrobe.PERSON))
	await _capture("fashion_child_entry_only")
	var back: Control = m.global_navigation_button
	await _tap(back, back.size * 0.5, "fashion_child_back")
	_check("source Back closes child and releases wardrobe block", m.wardrobe_layer == null and not m.touch_control_blocks.has("wardrobe"))
	if not await _open_original_wardrobe("final_reopen"):
		return
	await _tap(m.global_navigation_button, m.global_navigation_button.size * 0.5, "parent_global_back")
	_check("source globalBack closes parent with classic retained", m.wardrobe_layer == null and m.skin_id == "classic" and m.wd.is_empty())
	_check("unknown private key retained", _state_equal(_disk().get("unknown"), seed.get("flat_vector_private_unknown")))
	await _capture("final_royal_bedroom_classic")
	await _retire()

func _run() -> void:
	var engine: Dictionary = Engine.get_version_info()
	if str(engine.get("hash", "")) != "ed1daf0bf001b61586d9930840f2f1394092c079" or int(engine.get("patch", 0)) != 2 or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless" or Engine.time_scale != 1.0:
		quit(1)
		return
	out_dir = OS.get_environment("R63_OUT")
	var width: int = int(OS.get_environment("R63_WIDTH"))
	fairy_unlocked = OS.get_environment("R63_UNLOCKED") == "true"
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "day_one_active": false,
		"day_one_giant_dust_bunny_boss_defeated": true, "day_one_completed_rooms": DayOneDirector.ROOM_ORDER,
		"day_one_cleaned_rooms": DayOneDirector.ROOM_ORDER, "day_one_giant_dust_bunny_boss_triggered": true,
		"chapter2_active": true, "chapter2_unlocked_opera_mask": 0x0449,
		"chapter2_job_phase_masks": [0, 0, 0, 0, 0, 0, 0, 0],
		"skin": "classic", "fairyskin": fairy_unlocked, "music": false, "mic": false,
		"quality": "speedy", "pearls": 23, "pearls_ever": 23,
		"flat_vector_private_unknown": {"token": "R63_PRIVATE_ONLY", "keep": [3, 7]},
		"crafts": {}, "stickers": {}, "custom_fish": [], "custom_friends": []}
	var file: FileAccess = FileAccess.open(profile, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed, "\t", true) + "\n")
	file.close()
	if not await _aspect(Vector2i(width, 720)):
		errors.append("native viewport size did not settle")
	else:
		await _exercise()
	await _retire()
	if _normal_hashes() != normal_before:
		errors.append("normal eight save suffixes changed")
	var report: Dictionary = {"schema": "reef.wardrobe_context/1", "source_revision": OS.get_environment("R63_REV"),
		"engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(),
		"quality_requested": "speedy", "aspect": [width, 720], "time_scale": Engine.time_scale,
		"states": states, "events": events, "seed": seed, "private_profile": profile, "boot_count": boot_count,
		"route_events": route_events, "mode": "ORIGINAL_ROYAL_BEDROOM_WARDROBE_INPUTS", "fairy_unlocked_profile": fairy_unlocked,
		"checks": checks, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors,
		"actual_child_data": false, "normal_route_proved": false,
		"scope": "Original actual MainHall/DreamHouseWing/RoyalBedroom doors and shell wardrobe hotspot/full-skin UI after declared private postboss Castle bootstrap eachMain. Original locked/unlocked choices/Huluu as-is source option/feedback/Done/Back/reopen/notifications/privateMain reload; nested Fashion entry/Back only, itsvariantsopen. No measured target/skin/unlock/progress/clock/visual/source writes by harness;restoreclassic viaoriginalUI. No protected-original edits/newuse/identity acceptance. Dummy desktopMobile/Speedy is notfreshOS/device/audio/child/owner/QA11/art acceptance."}
	var output: FileAccess = FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("WARDROBE63|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
