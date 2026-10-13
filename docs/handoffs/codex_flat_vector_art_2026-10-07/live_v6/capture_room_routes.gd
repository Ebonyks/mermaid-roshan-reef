extends SceneTree
## R6 independent Castle room-route diagnostic extension; original sources and normal saves preserved.
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
  "cards": [
    "cards_unplayed_kitchen_idle",
    "cards_kitchen_00_hover",
    "cards_kitchen_00_pressed",
    "cards_kitchen_00_focus",
    "cards_kitchen_03_hover",
    "cards_kitchen_03_pressed",
    "cards_kitchen_03_focus",
    "cards_unplayed_opera_hall_idle",
    "cards_opera_hall_02_hover",
    "cards_opera_hall_02_pressed",
    "cards_opera_hall_02_focus",
    "cards_opera_hall_13_hover",
    "cards_opera_hall_13_pressed",
    "cards_opera_hall_13_focus",
    "cards_opera_hall_08_hover",
    "cards_opera_hall_08_pressed",
    "cards_opera_hall_08_focus",
    "cards_unplayed_library_idle",
    "cards_library_01_hover",
    "cards_library_01_pressed",
    "cards_library_01_focus",
    "cards_library_16_hover",
    "cards_library_16_pressed",
    "cards_library_16_focus",
    "cards_library_17_hover",
    "cards_library_17_pressed",
    "cards_library_17_focus",
    "cards_unplayed_craft_room_idle",
    "cards_craft_room_10_hover",
    "cards_craft_room_10_pressed",
    "cards_craft_room_10_focus",
    "cards_unplayed_playroom_idle",
    "cards_playroom_05_hover",
    "cards_playroom_05_pressed",
    "cards_playroom_05_focus",
    "cards_playroom_07_hover",
    "cards_playroom_07_pressed",
    "cards_playroom_07_focus",
    "cards_unplayed_bubble_bath_idle",
    "cards_bubble_bath_15_hover",
    "cards_bubble_bath_15_pressed",
    "cards_bubble_bath_15_focus",
    "cards_unplayed_mermaid_pool_idle",
    "cards_mermaid_pool_11_hover",
    "cards_mermaid_pool_11_pressed",
    "cards_mermaid_pool_11_focus",
    "cards_unplayed_dining_room_idle",
    "cards_dining_room_06_hover",
    "cards_dining_room_06_pressed",
    "cards_dining_room_06_focus",
    "cards_unplayed_movie_lounge_idle",
    "cards_movie_lounge_12_hover",
    "cards_movie_lounge_12_pressed",
    "cards_movie_lounge_12_focus",
    "cards_completed_kitchen_idle",
    "cards_completed_opera_hall_idle",
    "cards_completed_library_idle",
    "cards_completed_craft_room_idle",
    "cards_completed_playroom_idle",
    "cards_completed_bubble_bath_idle",
    "cards_completed_mermaid_pool_idle",
    "cards_completed_dining_room_idle",
    "cards_completed_movie_lounge_idle"
  ],
  "entry": [
    "route_00_before",
    "route_00_entered",
    "route_00_returned",
    "route_01_before",
    "route_01_entered",
    "route_01_returned",
    "route_02_before",
    "route_02_entered",
    "route_02_returned",
    "route_03_before",
    "route_03_entered",
    "route_03_returned",
    "route_05_before",
    "route_05_entered",
    "route_05_returned",
    "route_06_before",
    "route_06_entered",
    "route_06_returned",
    "route_07_before",
    "route_07_entered",
    "route_07_returned",
    "route_08_before",
    "route_08_entered",
    "route_08_returned",
    "route_10_before",
    "route_10_entered",
    "route_10_returned",
    "route_11_before",
    "route_11_entered",
    "route_11_returned",
    "route_12_before",
    "route_12_entered",
    "route_12_returned",
    "route_13_before",
    "route_13_entered",
    "route_13_returned",
    "route_15_before",
    "route_15_entered",
    "route_15_returned",
    "route_16_before",
    "route_16_entered",
    "route_16_returned",
    "route_17_before",
    "route_17_entered",
    "route_17_returned"
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
		"algorithm": "sha256_runtime_roots_room_routes_v1",
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

func _run() -> void:
	run_case = OS.get_environment("LIVE6RR_CASE")
	capture_root = OS.get_environment("LIVE6RR_OUT")
	var aspect := OS.get_environment("LIVE6RR_ASPECT").split("x")
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
	_check("measured source list complete", (capture_source_signature["missing"] as Array).is_empty())
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
		"cards": await _run_cards()
		"entry": await _run_entry()
	paused = false
	capture_main.queue_free()
	capture_main = null
	await _frames(8)
	var normal_after := _normal_save_fingerprints()
	var source_after := _source_signature()
	_check("normal child save/backups unchanged", normal_save_before == normal_after)
	_check("measured source list unchanged", capture_source_signature["sha256"] == source_after["sha256"])
	var ids: Array[String] = []
	for row: Dictionary in states:
		ids.append(String(row["id"]))
	_check("ordered exact matrix complete", ids == (EXPECTED_IDS[run_case] as Array))
	var manifest := {"schema": "reef.flat_vector.room_routes.v1", "source_revision": OS.get_environment("GITHUB_SHA"), "run_case": run_case, "engine": _engine_contract(), "renderer": RenderingServer.get_current_rendering_method(), "display_server": DisplayServer.get_name(), "quality": "speedy", "aspect": [aspect_size.x, aspect_size.y], "harness_sha256": FileAccess.get_sha256(get_script().resource_path), "source_signature": capture_source_signature, "source_unchanged": capture_source_signature["sha256"] == source_after["sha256"], "save_isolation": {"before": normal_save_before, "after": normal_after, "unchanged": normal_save_before == normal_after, "fresh_fixture_save": isolated_save, "normal_save_file": ProjectSettings.globalize_path("user://reef_save.json")}, "checks": checks, "expected_ids": EXPECTED_IDS[run_case], "states": states, "failures": failures, "result": "PASS" if failures == 0 else "FAIL", "scope": "Room-route diagnostic. Existing art and source-only Canvas behavior. Isolated normalized past-story saves and programmatic room selection; raw pointer career launch, source tween and owner leave observed. Saved completion markers are not earned wins. No DL-QA-11/full closure/device/child/owner acceptance."}
	var out := FileAccess.open(capture_root.path_join("capture_manifest.json"), FileAccess.WRITE)
	out.store_string(JSON.stringify(manifest, "	", true) + "\n")
	out.close()
	print("LIVE6|RESULT|%s|states=%d" % [manifest["result"], states.size()])
	quit(0 if failures == 0 else 1)

func _capture(id: String, required_name: String = "") -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var actual := _snapshot()
	actual["room_routes"] = _room_record()
	var valid: bool = actual["save_path"] == isolated_save and not actual["tree_paused"] and not actual["story_clip_present"] and float(actual["fade_alpha"]) <= 0.001 and not actual["start_menu_active"] and not actual["intro_active"]
	for key: String in variant_expect:
		valid = valid and actual.get(key) == variant_expect[key]
	if not required_name.is_empty():
		var found: Node = capture_main.find_child(required_name, true, false)
		valid = valid and found is CanvasItem and (found as CanvasItem).is_visible_in_tree()
	var image: Image = root.get_viewport().get_texture().get_image()
	var path := capture_root.path_join(id + ".png")
	_check("capture path fresh " + id, not FileAccess.file_exists(path))
	var err: Error = image.save_png(path)
	valid = valid and not image.is_empty() and image.get_size() == aspect_size and err == OK
	_check("native state/image " + id, valid, "required="+required_name)
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	states.append({"id":id,"sequence":states.size(),"status":"PASS" if valid else "FAIL","expected_top_target":required_name,"variant_expect":variant_expect.duplicate(),"actual":actual,"image":{"file":id+".png","width":image.get_width(),"height":image.get_height(),"bytes":file.get_length(),"sha256":FileAccess.get_sha256(path)}})
	file.close()

func _setup_route() -> void:
	var m: ReefMain = capture_main
	m._start_menu_ref()._dismiss_menu()
	await _frames(3)
	m._day_one_cancel_story_clips()
	m.day_one_active = false
	m.chapter2_active = false
	m._enter_level2_now(true, false, false)
	await _frames(18)
	m.day_one_giant_dust_bunny_boss_defeated = true
	m.chapter2_party_piece_mask = ChapterTwoPartyPlan.ALL_PARTY_MASK
	m.chapter2_ember_king_crashed = true
	m.chapter2_party_started = true
	m.chapter2_lawn_started = false
	m._chapter_two_ref().restore_state({"day_one_giant_dust_bunny_boss_defeated":true,"chapter2_party_piece_mask":ChapterTwoPartyPlan.ALL_PARTY_MASK,"chapter2_ember_king_crashed":true,"chapter2_party_started":true,"chapter2_lawn_started":false})
	m.opera_stars = 0
	m._write_save()
	m._save_state.load_save()
	_check("normalized past-story checkpoint survives reload", m.chapter2_story_complete and not m.chapter2_is_active() and not m.day_one_jobs_locked() and m.opera_stars == 0)
	m._enter_castle_interior_now(false)
	await _frames(24)

func _show_room(room: String) -> bool:
	var m: ReefMain = capture_main
	m._castle_career_routes_ref().close_opera_venue()
	m._castle_rooms_ref().show_room(room, false)
	await _frames(18)
	m._castle_career_routes_ref().sync()
	if room == "opera_hall":
		_check("actual guarded painted venue opens", m._castle_career_routes_ref().open_opera_venue())
	return await _wait_room(room)

func _wait_room(room: String) -> bool:
	for _frame: int in range(READY_FRAME_LIMIT):
		var m: ReefMain = capture_main
		if m.game == "level2" and m.castle_room_id == room and String(m.g.get("phase","")) == "hall" and m.opera_game == null and is_instance_valid(m.castle_room_layer) and m.castle_room_layer.visible and float(_snapshot()["fade_alpha"]) <= 0.001:
			return true
		await process_frame
	return false

func _route_button(act: int) -> Button:
	return capture_main._castle_career_routes_ref().button_for_act(act)

func _move_clear() -> void:
	var move := InputEventMouseMotion.new()
	move.position = Vector2(1255.0,710.0)
	move.global_position = move.position
	move.button_mask = 0
	root.push_input(move,true)

func _run_cards() -> void:
	var m: ReefMain = capture_main
	for profile: String in ["unplayed","completed"]:
		m.opera_stars = 0 if profile == "unplayed" else OperaHouse.ACTIVE_STAR_MASK
		m._write_save()
		m._save_state.load_save()
		_check("saved marker profile reload "+profile,m.opera_stars == (0 if profile=="unplayed" else OperaHouse.ACTIVE_STAR_MASK) and m.chapter2_story_complete)
		for room: String in CastleCareerRoutes.ROOM_ACT_INDICES:
			_check("room fixture ready "+room,await _show_room(room))
			variant_expect = {"game":"level2","castle_room":room,"phase":"hall","menu_open":false}
			_move_clear()
			await _capture("cards_"+profile+"_"+room+"_idle","CastleCareerRoutes")
			if profile == "completed":
				continue
			for act: int in CastleCareerRoutes.act_indices_for_room(room):
				var button: Button = _route_button(act)
				_check("route button reachable "+str(act),is_instance_valid(button) and button.is_visible_in_tree() and not button.disabled)
				if not is_instance_valid(button):
					continue
				for b: Button in m._castle_career_routes_ref().buttons:
					b.release_focus()
				_hover(button)
				await _capture("cards_%s_%02d_hover" % [room,act],button.name)
				_pointer(button,true)
				await _capture("cards_%s_%02d_pressed" % [room,act],button.name)
				_pointer(button,false,true)
				await _frames(3)
				_check("outside release cancelled actual launch "+str(act),m.opera_game==null and m.game=="level2")
				button.grab_focus()
				await _capture("cards_%s_%02d_focus" % [room,act],button.name)

func _career_ready(index: int, room: String) -> bool:
	var m: ReefMain = capture_main
	var opera: OperaHouse = m.opera_game as OperaHouse
	var act: OperaAct = opera.act if is_instance_valid(opera) else null
	return is_instance_valid(opera) and is_instance_valid(act) and opera.act_index==index and m.opera_active_act_index==index and m.game=="opera" and m.opera_return_room==room and m.castle_room_id==room and act.state=="play" and act.use_career_world_2d and is_instance_valid(act.career_world_2d) and act.career_world_2d.visible and act.career_world_2d.layer==10 and m.living_stage_id=="opera.act.%02d" % index and is_instance_valid(m.living_layer) and m.living_layer.visible and m.living_layer.layer==11 and is_instance_valid(m.hud_layer) and m.hud_layer.visible and m.hud_layer.layer==12 and is_instance_valid(m.castle_room_layer) and not m.castle_room_layer.visible and float(_snapshot()["fade_alpha"])<=0.001

func _run_entry() -> void:
	var m: ReefMain = capture_main
	for act: int in OperaHouse.LIVE_ACT_INDICES:
		var room: String = CastleCareerRoutes.room_for_act(act)
		_check("actual assigned room ready "+str(act),await _show_room(room))
		variant_expect = {"game":"level2","castle_room":room,"phase":"hall","menu_open":false}
		var button: Button = _route_button(act)
		_check("actual pointer target launchable "+str(act),is_instance_valid(button) and button.is_visible_in_tree() and not button.disabled)
		await _capture("route_%02d_before" % act,button.name)
		await _click(button)
		var ready: bool = false
		for _frame: int in range(READY_FRAME_LIMIT):
			if _career_ready(act,room):
				ready = true
				break
			await process_frame
		_check("actual pointer career entry "+str(act),ready)
		variant_expect = {"game":"opera","castle_room":room,"menu_open":false}
		await _capture("route_%02d_entered" % act)
		var opera: OperaHouse = m.opera_game as OperaHouse
		if is_instance_valid(opera):
			opera._leave_early()
		_check("source owner leave returns exact room "+str(act),await _wait_room(room))
		variant_expect = {"game":"level2","castle_room":room,"phase":"hall","menu_open":false}
		await _capture("route_%02d_returned" % act,"CastleCareerRoutes")

func _texture_record(texture: Texture2D) -> Dictionary:
	if texture == null:
		return {"present":false}
	var out: Dictionary = {"present":true,"class":texture.get_class(),"path":texture.resource_path,"size":texture.get_size()}
	if texture is AtlasTexture:
		var atlas: AtlasTexture = texture as AtlasTexture
		out["atlas"] = _texture_record(atlas.atlas)
		out["region"] = atlas.region
	return out

func _room_record() -> Dictionary:
	var m: ReefMain = capture_main
	var routes: CastleCareerRoutes = m._castle_career_routes_ref()
	var buttons: Array[Dictionary] = []
	for button: Button in routes.buttons:
		if not is_instance_valid(button):
			continue
		var row: Dictionary = {"path":String(m.get_path_to(button)),"act":int(button.get_meta("act_index",-1)),"visible":button.is_visible_in_tree(),"disabled":button.disabled,"rect":button.get_global_rect(),"draw_mode":button.get_draw_mode(),"focus":button.has_focus(),"presentation":String(button.get_meta("presentation","")),"painted_door_hit_region":bool(button.get_meta("painted_door_hit_region",false)),"styles":{}}
		for key: String in ["normal","hover","pressed","hover_pressed","disabled","focus"]:
			row["styles"][key] = _style(button.get_theme_stylebox(key))
		for child_name: String in ["RoshanActor","CareerCrest","CareerPearl"]:
			var node: CanvasItem = button.get_node_or_null(child_name) as CanvasItem
			if node is TextureRect:
				row[child_name] = {"visible":node.is_visible_in_tree(),"texture":_texture_record((node as TextureRect).texture)}
			elif node is Panel:
				row[child_name] = {"visible":node.is_visible_in_tree(),"complete":node.get_meta("complete",false),"style":_style((node as Panel).get_theme_stylebox("panel"))}
		buttons.append(row)
	var opera: OperaHouse = m.opera_game as OperaHouse
	var act: OperaAct = opera.act if is_instance_valid(opera) else null
	var world: OperaCareerWorld2D = act.career_world_2d if is_instance_valid(act) else null
	var venue: OperaHouseVenue2D = routes.opera_venue
	return {"chapter2_story_complete":m.chapter2_story_complete,"chapter2_active":m.chapter2_is_active(),"day_one_jobs_locked":m.day_one_jobs_locked(),"opera_stars":m.opera_stars,"buttons":buttons,"routes_visible":is_instance_valid(routes.root) and routes.root.is_visible_in_tree(),"route_room":routes.room_id,"venue_floor":venue.floor_index if is_instance_valid(venue) else -1,"venue_accepting":venue.accepting_input if is_instance_valid(venue) else false,"opera_present":is_instance_valid(opera),"opera_act":opera.act_index if is_instance_valid(opera) else -1,"act_state":act.state if is_instance_valid(act) else "","dev_playtest":opera.dev_playtest if is_instance_valid(opera) else false,"story_mode":opera.story_mode if is_instance_valid(opera) else false,"return_room":m.opera_return_room,"living_stage":m.living_stage_id,"world_phase":world.phase_index if is_instance_valid(world) else -1,"world_layer":world.layer if is_instance_valid(world) else -1,"world_visible":world.visible if is_instance_valid(world) else false}
