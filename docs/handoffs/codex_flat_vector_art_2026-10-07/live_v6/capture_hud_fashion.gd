extends SceneTree
## R6 independent HUD/fashion diagnostic extension; original sources and normal saves preserved.
const GODOT_BASELINE_PATH := "res://tools/godot_baseline.json"
const READY_FRAME_LIMIT := 240
const SOURCE_FIXED_FILES: Array[String] = [
	"project.godot",
	"tools/audit_opera_capture.py",
	"tools/audit_godot_baseline.py",
	"tools/godot_baseline.json",
]
const SOURCE_TREE_ROOTS: Array[String] = [
	"assets", "scenes", "scripts", "shaders",
]
const SOURCE_TREE_SUFFIXES := {
	"assets": [
		".bmp", ".dds", ".exr", ".gdshader", ".hdr", ".import", ".jpeg",
		".jpg", ".json", ".ktx", ".mp3", ".ogg", ".ogv", ".png", ".res", ".tres", ".svg", ".tga",
		".uid", ".wav", ".webp",
	],
	"scenes": [".res", ".tres", ".tscn", ".uid"],
	"scripts": [".gd", ".uid"],
	"shaders": [".gdshader", ".uid"],
}

const EXPECTED_IDS := {
  "fashion": [
    "fashion_launcher",
    "fashion_launcher_feedback",
    "fashion_starter_entry",
    "fashion_starter_roshan_head_p00",
    "fashion_starter_roshan_head_p01",
    "fashion_starter_roshan_head_p02",
    "fashion_starter_roshan_body_p00",
    "fashion_starter_roshan_body_p01",
    "fashion_starter_roshan_body_p02",
    "fashion_starter_roshan_body_p03",
    "fashion_starter_roshan_tail_p00",
    "fashion_starter_roshan_tail_p01",
    "fashion_starter_roshan_tail_p02",
    "fashion_starter_rumi_head_p00",
    "fashion_starter_rumi_head_p01",
    "fashion_starter_rumi_head_p02",
    "fashion_starter_rumi_body_p00",
    "fashion_starter_rumi_body_p01",
    "fashion_starter_rumi_body_p02",
    "fashion_starter_rumi_body_p03",
    "fashion_starter_rumi_tail_p00",
    "fashion_starter_rumi_tail_p01",
    "fashion_starter_rumi_tail_p02",
    "fashion_starter_daddy_mermaid_head_p00",
    "fashion_starter_daddy_mermaid_head_p01",
    "fashion_starter_daddy_mermaid_head_p02",
    "fashion_starter_daddy_mermaid_body_p00",
    "fashion_starter_daddy_mermaid_body_p01",
    "fashion_starter_daddy_mermaid_body_p02",
    "fashion_starter_daddy_mermaid_body_p03",
    "fashion_starter_daddy_mermaid_tail_p00",
    "fashion_starter_daddy_mermaid_tail_p01",
    "fashion_starter_daddy_mermaid_tail_p02",
    "fashion_locked_pressed",
    "fashion_locked_released",
    "fashion_locked_settled",
    "fashion_unlocked_roshan_head_p00",
    "fashion_unlocked_roshan_head_p01",
    "fashion_unlocked_roshan_head_p02",
    "fashion_unlocked_roshan_body_p00",
    "fashion_unlocked_roshan_body_p01",
    "fashion_unlocked_roshan_body_p02",
    "fashion_unlocked_roshan_body_p03",
    "fashion_unlocked_roshan_tail_p00",
    "fashion_unlocked_roshan_tail_p01",
    "fashion_unlocked_roshan_tail_p02",
    "fashion_unlocked_rumi_head_p00",
    "fashion_unlocked_rumi_head_p01",
    "fashion_unlocked_rumi_head_p02",
    "fashion_unlocked_rumi_body_p00",
    "fashion_unlocked_rumi_body_p01",
    "fashion_unlocked_rumi_body_p02",
    "fashion_unlocked_rumi_body_p03",
    "fashion_unlocked_rumi_tail_p00",
    "fashion_unlocked_rumi_tail_p01",
    "fashion_unlocked_rumi_tail_p02",
    "fashion_unlocked_daddy_mermaid_head_p00",
    "fashion_unlocked_daddy_mermaid_head_p01",
    "fashion_unlocked_daddy_mermaid_head_p02",
    "fashion_unlocked_daddy_mermaid_body_p00",
    "fashion_unlocked_daddy_mermaid_body_p01",
    "fashion_unlocked_daddy_mermaid_body_p02",
    "fashion_unlocked_daddy_mermaid_body_p03",
    "fashion_unlocked_daddy_mermaid_tail_p00",
    "fashion_unlocked_daddy_mermaid_tail_p01",
    "fashion_unlocked_daddy_mermaid_tail_p02",
    "fashion_roshan_ribbon_picked",
    "fashion_roshan_ribbon_settled",
    "fashion_rumi_ribbon_picked",
    "fashion_rumi_ribbon_settled",
    "fashion_daddy_mermaid_ribbon_picked",
    "fashion_daddy_mermaid_ribbon_settled",
    "fashion_drag_held",
    "fashion_drag_moved",
    "fashion_drag_focus_cancelled",
    "fashion_saved_reload",
    "fashion_closed",
    "fashion_party_entry",
    "fashion_party_closed"
  ],
  "hud": [
    "hud_idle",
    "hud_library_objective",
    "hud_library_after_4seconds",
    "hud_playroom_objective",
    "hud_main_hall_objective",
    "hud_north_objective",
    "hud_party_farmer",
    "hud_party_chef",
    "hud_party_candy_maker",
    "hud_party_painter",
    "hud_party_ballerina",
    "hud_party_popstar",
    "hud_party_astronaut",
    "hud_party_detective",
    "hud_objective_cleared",
    "hud_save_reload",
    "hud_fade_black_held",
    "hud_fade_revealing",
    "hud_fade_restored"
  ],
  "practice": [
    "fashion_practice_saved_phase0",
    "fashion_practice_phase0_after_pointer",
    "fashion_practice_saved_phase1",
    "fashion_practice_saved_phase2",
    "fashion_practice_saved_complete",
    "fashion_final_closed"
  ]
}

var failures: int = 0
var capture_root := ""
var aspect_size := Vector2i.ZERO
var run_case := ""
var capture_main: ReefMain
var isolated_save := ""
var states: Array[Dictionary] = []
var checks: Array[Dictionary] = []
var capture_source_signature: Dictionary = {}
var normal_save_before: Dictionary = {}
var generation_before: int = 0
var variant_expect: Dictionary = {}

func _init() -> void:
	call_deferred("_run")

func _check(label: String, ok: bool, detail: String = "") -> void:
	checks.append({"label": label, "pass": ok, "detail": detail})
	if not ok:
		failures += 1
	print("LIVE6|%s|%s|%s|%s" % [run_case, "PASS" if ok else "FAIL", label, detail])

func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame

func _wait(seconds: float) -> void:
	await create_timer(seconds, true).timeout

func _find(name: String) -> Button:
	return capture_main.find_child(name, true, false) as Button

func _pointer(button: Button, pressed: bool, outside: bool = false) -> void:
	if outside:
		var move := InputEventMouseMotion.new()
		move.position = Vector2(1255.0, 710.0)
		move.global_position = move.position
		root.push_input(move, true)
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.button_mask = MOUSE_BUTTON_MASK_LEFT if pressed else 0
	event.position = Vector2(1255.0, 710.0) if outside else button.get_global_rect().get_center()
	event.global_position = event.position
	root.push_input(event, true)

func _hover(button: Button) -> void:
	var event := InputEventMouseMotion.new()
	event.position = button.get_global_rect().get_center()
	event.global_position = event.position
	root.push_input(event, true)

func _mouse_point(point: Vector2, pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.button_index=MOUSE_BUTTON_LEFT
	event.pressed=pressed
	event.button_mask=MOUSE_BUTTON_MASK_LEFT if pressed else 0
	event.position=point
	event.global_position=point
	root.push_input(event,true)

func _click(button: Button) -> void:
	_check("pointer target exists", is_instance_valid(button))
	if not is_instance_valid(button):
		return
	# Capture coordinates before input: callbacks can remove/rebuild this control.
	var point: Vector2 = button.get_global_rect().get_center()
	_hover(button)
	await _frames(1)
	_mouse_point(point,true)
	await _frames(2)
	_mouse_point(point,false)
	await _frames(3)

func _style(style: StyleBox) -> Dictionary:
	var out := {"class": style.get_class(), "path": style.resource_path}
	if style is StyleBoxFlat:
		var flat: StyleBoxFlat = style as StyleBoxFlat
		out["bg_color"] = flat.bg_color
		out["border_color"] = flat.border_color
		out["border_widths"] = [flat.border_width_left, flat.border_width_top, flat.border_width_right, flat.border_width_bottom]
		out["corner_radii"] = [flat.corner_radius_top_left, flat.corner_radius_top_right, flat.corner_radius_bottom_left, flat.corner_radius_bottom_right]
		out["shadow_size"] = flat.shadow_size
	elif style is StyleBoxTexture:
		var textured: StyleBoxTexture = style as StyleBoxTexture
		if textured.texture != null:
			out["texture"] = textured.texture.resource_path
		out["modulate"] = textured.modulate_color
		out["texture_margins"] = [textured.texture_margin_left, textured.texture_margin_top, textured.texture_margin_right, textured.texture_margin_bottom]
	return out

func _collect_visible(node: Node, rows: Array[Dictionary], layer: int = 0, layer_visible: bool = true) -> void:
	if node is CanvasLayer:
		layer = (node as CanvasLayer).layer
		layer_visible = layer_visible and (node as CanvasLayer).visible
	if node is CanvasItem and (node as CanvasItem).is_visible_in_tree() and layer_visible:
		var item: CanvasItem = node as CanvasItem
		var row: Dictionary = {"path": String(capture_main.get_path_to(node)), "class": String(node.get_class()), "modulate": item.modulate, "self_modulate": item.self_modulate, "z_index": item.z_index, "canvas_layer": layer}
		var script: Script = node.get_script() as Script
		if script != null:
			row["script"] = script.resource_path
		if node is Control:
			var control: Control = node as Control
			row["rect"] = control.get_global_rect()
			row["mouse_filter"] = control.mouse_filter
			row["clip_contents"] = control.clip_contents
			var styles: Dictionary = {}
			for key: String in ["normal", "hover", "pressed", "hover_pressed", "disabled", "focus", "panel"]:
				if control.has_theme_stylebox(key):
					styles[key] = _style(control.get_theme_stylebox(key))
			row["styles"] = styles
			row["font"] = _font_record(control.get_theme_font("font"))
			row["font_size"] = control.get_theme_font_size("font_size")
			row["typography_role"] = String(control.get_meta("typography_role", ""))
			row["properties"] = {}
			for property: Dictionary in node.get_property_list():
				if String(property["name"]) in ["selected", "choice_color", "choice_effect", "choice_texture", "atlas_grid", "atlas_frame", "color_id", "symbol_id"]:
					var value: Variant = node.get(String(property["name"]))
					row["properties"][String(property["name"])] = value.resource_path if value is Resource else value
		if node is Label:
			row["text"] = (node as Label).text
		if node is Button:
			var button: Button = node as Button
			row["text"] = button.text
			row["disabled"] = button.disabled
			row["pressed"] = button.button_pressed
			row["draw_mode"] = button.get_draw_mode()
			row["focus"] = button.has_focus()
			row["selected"] = button.get_meta("selected", false)
			row["locked"] = button.get_meta("locked", false)
			var callbacks: Array[Dictionary] = []
			for connection: Dictionary in button.get_signal_connection_list("pressed"):
				var callback: Callable = connection["callable"] as Callable
				var target: Object = callback.get_object()
				callbacks.append({"method":String(callback.get_method()),"valid":callback.is_valid(),"target_id":callback.get_object_id(),"target_class":target.get_class() if is_instance_valid(target) else "missing"})
			row["pressed_callbacks"] = callbacks
		if node is TextureRect:
			var tr: TextureRect = node as TextureRect
			if tr.texture != null:
				row["texture"] = tr.texture.resource_path
		if node is Sprite2D:
			var sprite: Sprite2D = node as Sprite2D
			if sprite.texture != null:
				row["texture"] = sprite.texture.resource_path
		if node is ColorRect:
			row["color"] = (node as ColorRect).color
		if node is Polygon2D:
			var polygon: Polygon2D = node as Polygon2D
			row["polygon"] = polygon.polygon
			row["color"] = polygon.color
			row["position"] = polygon.position
			row["scale"] = polygon.scale
			row["rotation"] = polygon.rotation
		if item.material is ShaderMaterial:
			var material: ShaderMaterial = item.material as ShaderMaterial
			if material.shader != null:
				row["shader"] = material.shader.resource_path
				row["shader_code_sha256"] = material.shader.code.sha256_text()
		rows.append(row)
	for child: Node in node.get_children():
		_collect_visible(child, rows, layer, layer_visible)

func _font_record(font: Font, depth: int = 0) -> Dictionary:
	if font == null or depth > 4:
		return {}
	var out := {"class": font.get_class(), "path": font.resource_path, "family": font.get_font_name(), "style": font.get_font_style_name(), "fallbacks": []}
	if font.resource_path.begins_with("res://") and FileAccess.file_exists(font.resource_path):
		out["source_sha256"] = FileAccess.get_sha256(font.resource_path)
	else:
		out["source_limit"] = "Embedded/OS runtime font; no standalone source path exposed; Android fallback and exact font licensing unresolved."
	for fallback: Font in font.fallbacks:
		out["fallbacks"].append(_font_record(fallback, depth + 1))
	return out

func _touch_record() -> Dictionary:
	var t: CanvasLayer = capture_main.touch_ui
	var circles: Array[Dictionary] = []
	for role: String in ["hint", "base", "knob"]:
		var p: Panel = t._stick_hint if role == "hint" else (t._base if role == "base" else t._knob)
		circles.append({"role": role, "path": String(capture_main.get_path_to(p)), "visible": p.visible, "in_tree": p.is_visible_in_tree(), "size": p.size, "style": _style(p.get_theme_stylebox("panel"))})
	var flashes: Array[Dictionary] = []
	for child: Node in t._root.get_children():
		if child is Panel and child not in [t._stick_hint,t._base,t._knob]:
			var p: Panel = child as Panel
			flashes.append({"path": String(capture_main.get_path_to(p)), "visible": p.is_visible_in_tree(), "rect": p.get_global_rect(), "alpha": p.modulate.a, "style": _style(p.get_theme_stylebox("panel"))})
	return {"mode": t.control_mode, "world_enabled": t.world_controls_enabled, "touch_idx": t._touch_idx, "press_elapsed_ms": Time.get_ticks_msec() - t._press_ms, "owners": t.touch_owners.duplicate(), "stick_vec": t.stick_vec, "action_down": t.action_down, "circles": circles, "flashes": flashes}

func _snapshot() -> Dictionary:
	var m: ReefMain = capture_main
	var canvas: Array[Dictionary] = []
	_collect_visible(m, canvas)
	var venue: OperaHouseVenue2D = m._castle_career_routes_ref().opera_venue
	var menu: OperaJobPlaytestMenu = venue.job_playtest_menu if is_instance_valid(venue) else null
	return {"save_path": m._save_state.save_path, "tree_paused": paused, "start_menu_active": m.start_menu_active, "intro_active": m.intro_active, "story_clip_present": is_instance_valid(m._day_one_story_clip), "fade_alpha": m.fade_rect.color.a * m.fade_rect.modulate.a * m.fade_rect.self_modulate.a if m.fade_rect != null and m.fade_rect.visible else 0.0, "castle_room": m.castle_room_id, "game": m.game, "phase": String(m.g.get("phase", "")), "visible_canvas": canvas, "save_generation": m.save_generation, "castle_layer_present": is_instance_valid(m.castle_room_layer), "saved_touch_mode": m.touch_mode, "touch": _touch_record(), "menu_visible": is_instance_valid(menu) and menu.visible, "menu_open": is_instance_valid(menu) and menu.session_open, "menu_running": is_instance_valid(menu) and menu.running, "menu_guard": is_instance_valid(menu) and menu._owns_venue(), "venue_open": is_instance_valid(venue) and venue.is_open()}

func _capture(id: String, required_name: String = "", expected_pause: bool = false) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var actual := _snapshot()
	actual["hud_fashion"] = _hud_fashion_record()
	var valid: bool = actual["save_path"] == isolated_save and bool(actual["tree_paused"]) == expected_pause and not actual["story_clip_present"] and (float(actual["fade_alpha"]) >= 0.99 if id == "hud_fade_black_held" else (float(actual["fade_alpha"]) > 0.0 if id == "hud_fade_revealing" else float(actual["fade_alpha"]) <= 0.001))
	valid = valid and not actual["start_menu_active"] and not actual["intro_active"]
	for key: String in variant_expect:
		valid = valid and actual.get(key) == variant_expect[key]
	if not required_name.is_empty():
		var found: Node = capture_main.find_child(required_name, true, false)
		valid = valid and found is CanvasItem and (found as CanvasItem).is_visible_in_tree()
	if run_case == "touch":
		var touch: Dictionary = actual["touch"]
		for circle: Dictionary in touch["circles"]:
			valid = valid and not circle["visible"] and not circle["in_tree"]
		if id.ends_with("_flash"):
			valid = valid and (touch["flashes"] as Array).size() == 1
		if id.ends_with("world_release_after_hold"):
			valid = valid and int(touch["press_elapsed_ms"]) > 300 and (touch["flashes"] as Array).size() == (1 if touch["mode"] == "hybrid" else 0)
		if id.ends_with("settled") or id.ends_with("cancelled"):
			valid = valid and (touch["flashes"] as Array).is_empty() and touch["touch_idx"] == -1
	if id.begins_with("fashion_practice_saved_phase"):
		valid = valid and FashionDesigner.next_disguise_phase(capture_main)==int(id.right(1)) and bool(capture_main.wd.get("fashion_practice",false))
	if id=="fashion_practice_saved_complete":
		valid = valid and FashionDesigner.next_disguise_phase(capture_main)==3 and not bool(capture_main.wd.get("fashion_practice",false))
	var image: Image = root.get_viewport().get_texture().get_image()
	var path := capture_root.path_join(id + ".png")
	_check("capture path fresh " + id, not FileAccess.file_exists(path))
	var err: Error = image.save_png(path)
	valid = valid and not image.is_empty() and image.get_size() == aspect_size and err == OK
	_check("native state/image " + id, valid, "required=%s paused=%s" % [required_name, expected_pause])
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	states.append({"id": id, "sequence": states.size(), "status": "PASS" if valid else "FAIL", "expected_top_target": required_name, "variant_expect": variant_expect.duplicate(), "expected_pause": expected_pause, "actual": actual, "image": {"file": id + ".png", "width": image.get_width(), "height": image.get_height(), "bytes": file.get_length(), "sha256": FileAccess.get_sha256(path)}})
	file.close()

func _run() -> void:
	run_case = OS.get_environment("LIVE6HF_CASE")
	capture_root = OS.get_environment("LIVE6HF_OUT")
	var aspect := OS.get_environment("LIVE6HF_ASPECT").split("x")
	if aspect.size() != 2 or run_case not in EXPECTED_IDS or capture_root.is_empty():
		quit(1)
		return
	aspect_size = Vector2i(int(aspect[0]), int(aspect[1]))
	if aspect_size not in [Vector2i(1280, 720), Vector2i(1600, 720)] or not _exact_engine() or DisplayServer.get_name() == "headless" or RenderingServer.get_current_rendering_method() != "mobile":
		quit(1)
		return
	if DirAccess.dir_exists_absolute(capture_root):
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(capture_root)
	isolated_save = capture_root.get_base_dir().path_join("profiles").path_join(capture_root.get_file()).path_join("reef_save.json")
	DirAccess.make_dir_recursive_absolute(isolated_save.get_base_dir())
	_check("fresh profile", not FileAccess.file_exists(isolated_save))
	normal_save_before = _normal_save_fingerprints()
	capture_source_signature = _source_signature()
	_check("source closure complete", (capture_source_signature["missing"] as Array).is_empty())
	_check("real client/backing aspect", await _set_aspect(aspect_size))
	Engine.max_fps = 60
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	capture_main = scene.instantiate() as ReefMain
	capture_main._save_state = SaveState.new(capture_main, isolated_save)
	root.add_child(capture_main)
	capture_main._apply_quality("speedy")
	await _frames(6)
	generation_before = capture_main.save_generation
	await _setup_route()
	match run_case:
		"fashion": await _run_fashion()
		"practice": await _run_practice()
		"hud": await _run_hud()
	paused = false
	capture_main.queue_free()
	capture_main = null
	await _frames(8)
	var normal_after := _normal_save_fingerprints()
	var source_after := _source_signature()
	_check("normal child save/backups unchanged", normal_save_before == normal_after)
	_check("source closure unchanged", capture_source_signature["sha256"] == source_after["sha256"])
	var ids: Array[String] = []
	for row: Dictionary in states:
		ids.append(String(row["id"]))
	_check("ordered exact matrix complete", ids == (EXPECTED_IDS[run_case] as Array))
	var manifest := {"schema": "reef.flat_vector.hud_fashion.v1", "source_revision": OS.get_environment("GITHUB_SHA"), "run_case": run_case, "engine": _engine_contract(), "renderer": RenderingServer.get_current_rendering_method(), "display_server": DisplayServer.get_name(), "quality": "speedy", "aspect": [aspect_size.x, aspect_size.y], "harness_sha256": FileAccess.get_sha256(get_script().resource_path), "source_signature": capture_source_signature, "source_unchanged": capture_source_signature["sha256"] == source_after["sha256"], "save_isolation": {"before": normal_save_before, "after": normal_after, "unchanged": normal_save_before == normal_after, "fresh_fixture_save": isolated_save, "normal_save_file": ProjectSettings.globalize_path("user://reef_save.json")}, "checks": checks, "expected_ids": EXPECTED_IDS[run_case], "states": states, "failures": failures, "result": "PASS" if failures == 0 else "FAIL", "scope": "HUD/fashion diagnostic extension. Existing art only. Synthetic route and unlock/story seeds isolated; actual GUI choices and save/load logged. No natural progression, creative, DL-QA-11, device, child or owner acceptance. Fade uses declared source tween hold/reveal."}
	var out := FileAccess.open(capture_root.path_join("capture_manifest.json"), FileAccess.WRITE)
	out.store_string(JSON.stringify(manifest, "\t", true) + "\n")
	out.close()
	print("LIVE6|RESULT|%s|states=%d" % [manifest["result"], states.size()])
	quit(0 if failures == 0 else 1)

func _setup_route() -> void:
	var m: ReefMain = capture_main
	m._start_menu_ref()._dismiss_menu()
	await _frames(3)
	m.day_one_active = false
	m.chapter2_active = false
	m._day_one_cancel_story_clips()
	m._enter_level2_now(true, false, false)
	await _frames(18)
	if run_case == "menu":
		m._enter_castle_interior_now(false)
		await _frames(18)
		m._castle_rooms_ref().show_room("opera_hall", false)
		await _frames(18)

func _run_menu() -> void:
	var m: ReefMain = capture_main
	_check("actual guarded venue opens", m._castle_career_routes_ref().open_opera_venue())
	await _frames(18)
	variant_expect = {"menu_visible": false, "venue_open": true, "castle_room": "opera_hall"}
	await _capture("menu_venue", "OperaLeftElevatorPlaytest")
	await _click(_find("OperaLeftElevatorPlaytest"))
	variant_expect = {"menu_visible": true, "menu_open": true, "menu_running": false, "menu_guard": true}
	await _capture("menu_open", "OperaJobPlaytestMenu")
	var venue: OperaHouseVenue2D = m._castle_career_routes_ref().opera_venue
	var menu: OperaJobPlaytestMenu = venue.job_playtest_menu
	for act: int in OperaHouse.LIVE_ACT_INDICES:
		var button: Button = _find("PlaytestJob_%02d" % act)
		for b: Button in menu.job_buttons:
			b.release_focus()
		_hover(button)
		await _capture("menu_hover_%02d" % act, button.name)
		_pointer(button, true)
		await _capture("menu_pressed_%02d" % act, button.name)
		_pointer(button, false, true)
		await _frames(2)
		_check("outside release does not launch", menu.session_open and not menu.running)
		button.grab_focus()
		await _capture("menu_focus_%02d" % act, button.name)
	menu.close()
	variant_expect = {"menu_visible": false, "menu_open": false, "venue_open": true}
	await _capture("menu_closed", "OperaLeftElevatorPlaytest")
	venue.close()
	menu.open()
	variant_expect = {"menu_visible": false, "menu_open": false, "venue_open": false, "menu_guard": false}
	await _capture("menu_venue_closed", "CastleRoomsCanvasWorld")

func _touch_event(pos: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = pos
	event.pressed = pressed
	root.push_input(event, true)

func _touch_drag(pos: Vector2, relative: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = pos
	event.relative = relative
	root.push_input(event, true)

func _run_touch() -> void:
	var m: ReefMain = capture_main
	var t: CanvasLayer = m.touch_ui
	for mode: String in ["hybrid", "classic"]:
		m._set_touch_mode(mode, true)
		m._save_state.load_save()
		await _frames(3)
		variant_expect = {"saved_touch_mode": mode, "phase": "promenade", "castle_layer_present": false}
		await _capture("touch_" + mode + "_saved_reload_idle")
		var low := Vector2(60, 630)
		_touch_event(low, true)
		await _capture("touch_" + mode + "_press_lowerleft")
		_touch_drag(low + Vector2(68, -12), Vector2(68,-12))
		await _capture("touch_" + mode + "_drag_lowerleft")
		_touch_event(low + Vector2(68,-12), false)
		await _capture("touch_" + mode + "_released_drag")
		_touch_event(low, true)
		await _frames(2)
		_touch_event(low, false)
		await _capture("touch_" + mode + "_tap_lowerleft_flash")
		await _wait(0.42)
		await _capture("touch_" + mode + "_flash_settled")
		var world := Vector2(1200, 100)
		_touch_event(world, true)
		await _capture("touch_" + mode + "_world_press")
		await _wait(0.35)
		_touch_event(world, false)
		await _capture("touch_" + mode + "_world_release_after_hold")
		await _wait(0.42)
		await _capture("touch_" + mode + "_world_flash_settled")
		_touch_event(world, true)
		await _frames(2)
		_touch_event(world, false)
		await _capture("touch_" + mode + "_world_shorttap_flash")
		await _wait(0.42)
		await _capture("touch_" + mode + "_world_shorttap_settled")
		_touch_event(low, true)
		await _capture("touch_" + mode + "_held_before_focusloss")
		t.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
		await _capture("touch_" + mode + "_focusloss_cancelled")
		_check("focus loss releases stick", t._touch_idx == -1 and t.stick_vec == Vector2.ZERO)
func _set_aspect(size: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	await process_frame
	for _frame: int in range(READY_FRAME_LIMIT):
		# Windows applies a maximized-to-windowed transition asynchronously.
		# Reassert the requested client size after that transition instead of
		# accepting the monitor-sized backing texture as capture evidence.
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		get_root().size = size
		DisplayServer.window_set_size(size)
		await process_frame
		var image: Image = get_root().get_viewport().get_texture().get_image()
		if image != null and image.get_size() == size:
			return true
	return false


func _engine_contract() -> Dictionary:
	var version := Engine.get_version_info()
	return {
		"major": int(version.get("major", -1)),
		"minor": int(version.get("minor", -1)),
		"patch": int(version.get("patch", -1)),
		"status": String(version.get("status", "")),
		"build": String(version.get("build", "")),
		"version_string": String(version.get("string", "")),
	}


func _exact_engine() -> bool:
	var engine := _engine_contract()
	if not FileAccess.file_exists(GODOT_BASELINE_PATH):
		return false
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(GODOT_BASELINE_PATH))
	if not parsed is Dictionary:
		return false
	var baseline: Dictionary = parsed
	var parts: PackedStringArray = String(baseline.get("version", "")).split(".")
	if parts.size() != 3:
		return false
	for part: String in parts:
		if not part.is_valid_int():
			return false
	var status: String = String(baseline.get("status", ""))
	var release: String = String(baseline.get("release", ""))
	if status != "stable" or release != "%s-%s" % [String(baseline.get("version", "")), status]:
		return false
	return int(engine["major"]) == int(parts[0]) and int(engine["minor"]) == int(parts[1]) \
		and int(engine["patch"]) == int(parts[2]) and String(engine["status"]) == status \
		and String(engine["build"]) == "official" \
		and String(engine["version_string"]) == "%s (official)" % release


func _source_suffixes(root_name: String) -> Array[String]:
	var suffixes: Array[String] = []
	var raw_suffixes: Array = SOURCE_TREE_SUFFIXES.get(root_name, []) as Array
	for value: Variant in raw_suffixes:
		suffixes.append(String(value))
	return suffixes


func _source_file_matches(file_name: String, suffixes: Array[String]) -> bool:
	var lower_name := file_name.to_lower()
	for suffix: String in suffixes:
		if lower_name.ends_with(suffix):
			return true
	return false


func _collect_source_tree(relative_dir: String, suffixes: Array[String],
		paths: Array[String], missing: Array[String]) -> void:
	var resource_dir := "res://" + relative_dir
	if not DirAccess.dir_exists_absolute(resource_dir):
		missing.append(relative_dir + "/")
		return
	var file_names := DirAccess.get_files_at(resource_dir)
	file_names.sort()
	for file_name: String in file_names:
		if _source_file_matches(file_name, suffixes):
			paths.append(relative_dir + "/" + file_name)
	var directory_names := DirAccess.get_directories_at(resource_dir)
	directory_names.sort()
	for directory_name: String in directory_names:
		_collect_source_tree(
			relative_dir + "/" + directory_name, suffixes, paths, missing)


func _source_path_contract() -> Dictionary:
	var paths: Array[String] = SOURCE_FIXED_FILES.duplicate()
	var missing: Array[String] = []
	var tree_rules: Array[Dictionary] = []
	for root_name: String in SOURCE_TREE_ROOTS:
		var suffixes := _source_suffixes(root_name)
		tree_rules.append({"root": root_name, "suffixes": suffixes})
		_collect_source_tree(root_name, suffixes, paths, missing)
	paths.sort()
	missing.sort()
	return {
		"paths": paths,
		"missing": missing,
		"tree_rules": tree_rules,
	}


func _source_signature() -> Dictionary:
	var contract := _source_path_contract()
	var source_paths: Array = contract.get("paths", []) as Array
	var file_hashes: Dictionary = {}
	var missing: Array = contract.get("missing", []) as Array
	var entries: Array[String] = []
	for relative_value: Variant in source_paths:
		var relative := String(relative_value)
		var resource_path := "res://" + relative
		var digest := ""
		if FileAccess.file_exists(resource_path):
			digest = FileAccess.get_sha256(resource_path)
		if digest.is_empty():
			missing.append(relative)
		else:
			file_hashes[relative] = digest
		entries.append("%s:%s" % [relative, digest])
	missing.sort()
	return {
		"algorithm": "sha256_runtime_roots_hud_fashion_v3",
		"tree_rules": contract.get("tree_rules", []),
		"paths": source_paths,
		"files": file_hashes,
		"missing": missing,
		"sha256": "\n".join(entries).sha256_text(),
	}


func _normal_save_fingerprints() -> Dictionary:
	var values: Dictionary = {}
	var normal := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".tmp0", ".tmp1", ".tmp", ".old", ".bak", ".bak.tmp", ".bak.old"]:
		var path := normal + suffix
		values[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return values



func _node_record(node: CanvasItem) -> Dictionary:
	if not is_instance_valid(node):
		return {"present":false}
	var out: Dictionary = {"present":true,"path":String(capture_main.get_path_to(node)),"visible":node.visible,"in_tree":node.is_visible_in_tree(),"modulate":node.modulate,"self_modulate":node.self_modulate}
	if node is Control:
		out["rect"] = (node as Control).get_global_rect()
	if node is Label:
		out["text"] = (node as Label).text
	if node is TextureRect and (node as TextureRect).texture != null:
		var texture: Texture2D = (node as TextureRect).texture
		out["texture"] = texture.resource_path
		out["size"] = texture.get_size()
	return out

func _hud_fashion_record() -> Dictionary:
	var m: ReefMain = capture_main
	var compositions: Array[Dictionary] = []
	for key: String in m.fashion_composed_textures:
		var row: Dictionary = m.fashion_composed_textures[key] as Dictionary
		var texture: Texture2D = row["texture"] as Texture2D
		var image: Image = texture.get_image()
		var context := HashingContext.new()
		context.start(HashingContext.HASH_SHA256)
		context.update(image.get_data())
		compositions.append({"family":key,"signature":row["signature"],"resource_path":texture.resource_path,"image_size":image.get_size(),"image_format":image.get_format(),"pixel_sha256":context.finish().hex_encode(),"bytes":row["bytes"]})
	var drag: Dictionary = m.wd.get("fashion_drag", {}) as Dictionary
	var burst: Control = m.find_child("WardrobePreviewFeedbackBurst",true,false) as Control
	return {"wardrobe_present":is_instance_valid(m.wardrobe_layer),"person":String(m.wd.get("fashion_person","")),"slot":String(m.wd.get("fashion_slot","")),"page":int(m.wd.get("fashion_page",0)),"party":bool(m.wd.get("fashion_party",false)),"practice":bool(m.wd.get("fashion_practice",false)),"selected_parts":m.character_clothing_parts.duplicate(true),"legacy_outfits":m.character_outfits.duplicate(true),"unlocked":m.outfits_unlocked.duplicate(true),"dressing_progress":m.fashion_dressing_progress.duplicate(true),"disguise_progress":m.fashion_disguise_progress.duplicate(true),"story_complete_seed":m.chapter2_story_complete,"drag_active":not drag.is_empty(),"drag_id":String(drag.get("id","")),"drag_moved":bool(drag.get("moved",false)),"burst_children":burst.get_child_count() if is_instance_valid(burst) else 0,"compositions":compositions,"objective_key":m.obj_key,"objective_seen_t":m.obj_seen_t,"objective_card":_node_record(m.obj_card),"objective_texture":_node_record(m.obj_icon),"objective_fallback":_node_record(m.obj_icon_lbl),"caption":_node_record(m.hud_msg),"status_tray":_node_record(m.find_child("HudStatusTray",true,false) as CanvasItem),"pearls":_node_record(m.hud_pearls),"stars":_node_record(m.hud_stars),"sentence_objective":_node_record(m.hud_game),"world_enabled":m.touch_ui.world_controls_enabled,"save_generation":m.save_generation}

func _move_pointer(point: Vector2) -> void:
	var event := InputEventMouseMotion.new()
	event.position = point
	event.global_position = point
	event.button_mask = MOUSE_BUTTON_MASK_LEFT
	root.push_input(event,true)

func _fashion_gallery(profile: String) -> void:
	var m: ReefMain = capture_main
	for person: String in FashionParts.PEOPLE:
		await _click(_find("FashionCharacter_"+person))
		for slot: String in FashionParts.SLOTS:
			await _click(_find("FashionSlot_"+slot))
			var entries: Array[Dictionary] = FashionParts.items(person,slot)
			for page: int in range(ceili(entries.size()/3.0)):
				_check("source page matches "+person+slot+str(page),int(m.wd["fashion_page"])==page and String(m.wd["fashion_person"])==person and String(m.wd["fashion_slot"])==slot)
				await _capture("fashion_"+profile+"_"+person+"_"+slot+"_p%02d"%page,"FashionCurrentLook")
				if page+1<ceili(entries.size()/3.0):
					await _click(_find("FashionNextPage"))

func _run_fashion() -> void:
	var m: ReefMain = capture_main
	m._wardrobe_ref()._open_wardrobe()
	await _capture("fashion_launcher","FashionWardrobeButton")
	await _click(_find("WardrobeLook_classic"))
	await _capture("fashion_launcher_feedback","WardrobePreviewFeedbackBurst")
	_check("legacy burst exactly14",(m.find_child("WardrobePreviewFeedbackBurst",true,false) as Control).get_child_count()==14)
	await _wait(0.82)
	await _click(_find("FashionWardrobeButton"))
	await _capture("fashion_starter_entry","FashionCurrentLook")
	await _fashion_gallery("starter")
	await _click(_find("FashionCharacter_roshan"))
	await _click(_find("FashionSlot_body"))
	var locked: Button = _find("FashionOutfit_roshan_party_dress_v1")
	var selected_before: Dictionary = m.character_clothing_parts.duplicate(true)
	_hover(locked)
	await _frames(1)
	_pointer(locked,true)
	await _capture("fashion_locked_pressed",locked.name)
	_pointer(locked,false)
	await _capture("fashion_locked_released",locked.name)
	_check("locked card unchanged",m.character_clothing_parts==selected_before)
	await _wait(0.82)
	await _capture("fashion_locked_settled",locked.name)
	m._wardrobe_ref()._close_wardrobe()
	for person: String in FashionParts.PEOPLE:
		for slot: String in FashionParts.SLOTS:
			for item: Dictionary in FashionParts.items(person,slot):
				FashionDesigner.grant(m,String(item["id"]))
	m._write_save()
	FashionWardrobe.new(m).open()
	await _fashion_gallery("unlocked")
	for person: String in FashionParts.PEOPLE:
		await _click(_find("FashionCharacter_"+person))
		await _click(_find("FashionSlot_body"))
		await _click(_find("FashionOutfit_"+person+"_ribbon_v1"))
		await _capture("fashion_"+person+"_ribbon_picked","WardrobePreviewFeedbackBurst")
		_check("fashion burst exactly14 "+person,(m.find_child("WardrobePreviewFeedbackBurst",true,false) as Control).get_child_count()==14)
		await _wait(0.82)
		await _capture("fashion_"+person+"_ribbon_settled","FashionCurrentLook")
	await _click(_find("FashionCharacter_roshan"))
	await _click(_find("FashionSlot_head"))
	var card: Button = _find("FashionOutfit_head_royal_v1")
	_hover(card)
	await _frames(1)
	_pointer(card,true)
	await _capture("fashion_drag_held","FashionDraggedGarment")
	var stage: Control = m.wd["stage"] as Control
	var fit: Rect2 = m.wd["fashion_fit_rect"] as Rect2
	_move_pointer(stage.get_global_transform_with_canvas()*fit.get_center())
	await _capture("fashion_drag_moved","FashionDraggedGarment")
	var dressing: FashionDressingInput = m.wd["dressing_input"] as FashionDressingInput
	dressing.notification(Node.NOTIFICATION_WM_WINDOW_FOCUS_OUT)
	await _capture("fashion_drag_focus_cancelled","FashionCurrentLook")
	_check("dressing drag cancelled",(m.wd.get("fashion_drag",{}) as Dictionary).is_empty())
	_pointer(card,false,true)
	var saved: Dictionary = m.character_clothing_parts.duplicate(true)
	m._write_save()
	m.character_clothing_parts.clear()
	m.character_outfits.clear()
	m._save_state.load_save()
	_check("actual clothing reload",m.character_clothing_parts==saved)
	FashionWardrobe.new(m).open()
	await _capture("fashion_saved_reload","FashionCurrentLook")
	await _click(_find("FashionFinish"))
	await _capture("fashion_closed")
	m._wardrobe_ref().open_party_dress()
	await _capture("fashion_party_entry","FashionVisualPointer")
	await _click(_find("FashionFinish"))
	await _capture("fashion_party_closed")

func _run_practice() -> void:
	var m: ReefMain = capture_main
	# Declared normalized past-story fixture; no earned-progression claim.
	m.day_one_giant_dust_bunny_boss_defeated=true
	m.chapter2_party_piece_mask=ChapterTwoPartyPlan.ALL_PARTY_MASK
	m.chapter2_ember_king_crashed=true
	m.chapter2_party_started=true
	m.chapter2_lawn_started=false
	m._chapter_two_ref().restore_state({"day_one_giant_dust_bunny_boss_defeated":true,"chapter2_party_piece_mask":ChapterTwoPartyPlan.ALL_PARTY_MASK,"chapter2_ember_king_crashed":true,"chapter2_party_started":true,"chapter2_lawn_started":false})
	FashionDesigner.grant(m,"roshan_garden_v1")
	FashionDesigner.grant(m,"tail_strawberry_v1")
	_check("canonical story fixture ready",m.chapter2_story_complete)
	for phase: int in range(4):
		m.fashion_disguise_progress={"completed_mask":[0,1,3,7][phase]}
		m._write_save()
		m._save_state.load_save()
		_check("canonical story survives actual reload "+str(phase),m.chapter2_story_complete)
		FashionWardrobe.new(m).open()
		await _click(_find("FashionDisguisePlay"))
		if phase<3:
			await _capture("fashion_practice_saved_phase"+str(phase),"FashionGoalPicture")
			if phase==0:
				await _click(_find("FashionOutfit_roshan_garden_v1"))
				await _capture("fashion_practice_phase0_after_pointer","FashionGoalPicture")
		else:
			await _capture("fashion_practice_saved_complete","FashionCurrentLook")
		await _click(_find("FashionFinish"))
	await _capture("fashion_final_closed")

func _run_hud() -> void:
	var m: ReefMain = capture_main
	await _capture("hud_idle")
	m._on_chapter_two_hook_event(ChapterTwoDirector.EVENT_OBJECTIVE_CHANGED,{"objective":ChapterTwoDirector.OBJECTIVE_FIND_RAINBOW_CANDLE})
	await _capture("hud_library_objective","HudPictureTargetCard")
	await _wait(4.1)
	await _capture("hud_library_after_4seconds")
	m._on_chapter_two_hook_event(ChapterTwoDirector.EVENT_OBJECTIVE_CHANGED,{"objective":ChapterTwoDirector.OBJECTIVE_STUFFIE_BALLET})
	await _capture("hud_playroom_objective","HudPictureTargetCard")
	m._on_chapter_two_hook_event(ChapterTwoDirector.EVENT_OBJECTIVE_CHANGED,{"objective":ChapterTwoDirector.OBJECTIVE_MAIN_HALL_PARTY})
	await _capture("hud_main_hall_objective","HudPictureTargetCard")
	m._on_chapter_two_hook_event(ChapterTwoDirector.EVENT_EMBER_KING_CRASHED,{})
	await _capture("hud_north_objective","HudPictureTargetCard")
	var mask: int = 0
	for entry: Dictionary in ChapterTwoPartyPlan.LIVE_CAREERS:
		m.chapter2_party_piece_mask=mask
		m._chapter_two_guide_next_party_piece()
		await _capture("hud_party_"+String(entry["career"]),"HudPictureTargetCard")
		mask |= 1<<int(entry["act_index"])
	m._set_objective("",null,"")
	await _capture("hud_objective_cleared")
	m._write_save()
	m._save_state.load_save()
	await _capture("hud_save_reload")
	m._fade_cut(func(): pass)
	m.fade_tween.pause()
	await _capture("hud_fade_black_held")
	m.fade_tween.play()
	await _capture("hud_fade_revealing")
	await _wait(0.35)
	await _capture("hud_fade_restored")
