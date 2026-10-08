extends SceneTree
## Non-runtime R4 diagnostic shared UI capture; isolated save; no child acceptance.
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
		".jpg", ".json", ".ktx", ".mp3", ".ogg", ".png", ".svg", ".tga",
		".uid", ".wav", ".webp",
	],
	"scenes": [".res", ".tres", ".tscn", ".uid"],
	"scripts": [".gd", ".uid"],
	"shaders": [".gdshader", ".uid"],
}

const EXPECTED_IDS := {
  "fresh": [
    "fresh_default",
    "fresh_options_on",
    "fresh_options_off"
  ],
  "saved": [
    "saved_default",
    "saved_hover",
    "saved_pressed",
    "saved_options_on",
    "saved_options_off",
    "confirm_disarmed",
    "confirm_armed",
    "confirm_holding",
    "confirm_cancelled",
    "saved_kept"
  ],
  "overlays": [
    "pause_castle",
    "craft_locked",
    "craft_need_pearls",
    "craft_rainbow",
    "craft_cat",
    "craft_bird_detail",
    "wardrobe_locked",
    "wardrobe_locked_feedback",
    "wardrobe_unlocked",
    "wardrobe_fairy_selected",
    "stickers_empty",
    "stickers_earned",
    "critter_fish_empty",
    "critter_insect_empty",
    "critter_bird_empty",
    "critter_fish_caught",
    "critter_insect_caught",
    "critter_bird_caught"
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

func _init() -> void:
	call_deferred("_run")

func _check(label: String, ok: bool, detail: String = "") -> void:
	checks.append({"label": label, "pass": ok, "detail": detail})
	if not ok:
		failures += 1
	print("LIVE4|%s|%s|%s|%s" % [run_case, "PASS" if ok else "FAIL", label, detail])

func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame

func _wait(seconds: float) -> void:
	await create_timer(seconds, true).timeout

func _find(name: String) -> Button:
	return capture_main.find_child(name, true, false) as Button

func _pointer(button: Button, pressed: bool, outside: bool = false) -> void:
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.button_mask = MOUSE_BUTTON_MASK_LEFT if pressed else 0
	event.position = Vector2(2.0, 2.0) if outside else button.get_global_rect().get_center()
	event.global_position = event.position
	root.push_input(event, true)

func _hover(button: Button) -> void:
	var event := InputEventMouseMotion.new()
	event.position = button.get_global_rect().get_center()
	event.global_position = event.position
	root.push_input(event, true)

func _click(button: Button) -> void:
	_check("pointer target exists", button != null)
	if button == null:
		return
	_pointer(button, true)
	await _frames(2)
	_pointer(button, false)
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
			for key: String in ["normal", "hover", "pressed", "disabled", "focus", "panel"]:
				if control.has_theme_stylebox(key):
					styles[key] = _style(control.get_theme_stylebox(key))
			row["styles"] = styles
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
		if item.material is ShaderMaterial:
			var material: ShaderMaterial = item.material as ShaderMaterial
			if material.shader != null:
				row["shader"] = material.shader.resource_path
				row["shader_code_sha256"] = material.shader.code.sha256_text()
		rows.append(row)
	for child: Node in node.get_children():
		_collect_visible(child, rows, layer, layer_visible)

func _snapshot() -> Dictionary:
	var m: ReefMain = capture_main
	var canvas: Array[Dictionary] = []
	_collect_visible(m, canvas)
	var menu: StartMenu = m._start_menu_ref()
	var s: Dictionary = {"save_path": m._save_state.save_path, "has_saved_game": m.has_saved_game, "save_generation": m.save_generation, "start_menu_active": m.start_menu_active, "intro_active": m.intro_active, "tree_paused": paused, "story_clip_present": is_instance_valid(m._day_one_story_clip), "fade_alpha": m.fade_rect.color.a * m.fade_rect.modulate.a * m.fade_rect.self_modulate.a if m.fade_rect != null and m.fade_rect.visible else 0.0, "castle_room": m.castle_room_id, "visible_canvas": canvas, "music_on": m.music_on, "mic_on": m.mic_on, "quality": m.quality, "craft_kind": m.craft_kind, "craft_part": m.craft_part, "craft_unlocks": m.craft_unlocks.duplicate(), "craft_body_rainbow": m.craft_body_rb, "skin_id": m.skin_id, "fairy_unlocked": m.fairy_skin_unlocked, "stickers": m.stickers.duplicate(), "critter_category": m.collection_category, "critters": m.critter_collection.duplicate(), "pause_visible": m.pause_panel.is_visible_in_tree(), "confirm_visible": menu._confirm_root.is_visible_in_tree(), "options_visible": menu._options_root.is_visible_in_tree(), "hold_active": menu._new_game_hold_active, "hold_fill_width": menu._new_game_hold_fill.size.x}
	return s

func _capture(id: String, required_name: String = "", expected_pause: bool = false) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var actual := _snapshot()
	var valid: bool = actual["save_path"] == isolated_save and bool(actual["tree_paused"]) == expected_pause and not actual["story_clip_present"] and float(actual["fade_alpha"]) <= 0.001
	if run_case in ["fresh", "saved"]:
		valid = valid and bool(actual["start_menu_active"]) and bool(actual["intro_active"])
	else:
		valid = valid and not actual["start_menu_active"] and not actual["intro_active"]
	if not required_name.is_empty():
		var found: Node = capture_main.find_child(required_name, true, false)
		valid = valid and found is CanvasItem and (found as CanvasItem).is_visible_in_tree()
	var image: Image = root.get_viewport().get_texture().get_image()
	var path := capture_root.path_join(id + ".png")
	_check("capture path fresh " + id, not FileAccess.file_exists(path))
	var err: Error = image.save_png(path)
	valid = valid and not image.is_empty() and image.get_size() == aspect_size and err == OK
	_check("native state/image " + id, valid, "required=%s paused=%s" % [required_name, expected_pause])
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	states.append({"id": id, "sequence": states.size(), "status": "PASS" if valid else "FAIL", "expected_top_target": required_name, "expected_pause": expected_pause, "actual": actual, "image": {"file": id + ".png", "width": image.get_width(), "height": image.get_height(), "bytes": file.get_length(), "sha256": FileAccess.get_sha256(path)}})
	file.close()

func _run() -> void:
	run_case = OS.get_environment("LIVE4_CASE")
	capture_root = OS.get_environment("LIVE4_OUT")
	var aspect := OS.get_environment("LIVE4_ASPECT").split("x")
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
	if run_case == "saved":
		var seed := FileAccess.open(isolated_save, FileAccess.WRITE)
		seed.store_string(JSON.stringify({"schema_version": 1, "save_generation": 7, "won": {}, "found": {}, "pearls": 0, "plays": 1, "music": true, "mic": true, "quality": "speedy", "day_one_active": true}))
		seed.close()
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	capture_main = scene.instantiate() as ReefMain
	capture_main._save_state = SaveState.new(capture_main, isolated_save)
	root.add_child(capture_main)
	capture_main._apply_quality("speedy")
	await _frames(6)
	generation_before = capture_main.save_generation
	if run_case == "overlays":
		await _run_overlays()
	else:
		await _run_menu()
	paused = false
	await _frames(4)
	var normal_after := _normal_save_fingerprints()
	var source_after := _source_signature()
	_check("normal child save/backups unchanged", normal_save_before == normal_after)
	_check("source closure unchanged", capture_source_signature["sha256"] == source_after["sha256"])
	var ids: Array[String] = []
	for row: Dictionary in states:
		ids.append(String(row["id"]))
	_check("ordered exact matrix complete", ids == (EXPECTED_IDS[run_case] as Array))
	var manifest := {"schema": "reef.flat_vector.live_shared_ui.v1", "source_revision": OS.get_environment("GITHUB_SHA"), "run_case": run_case, "engine": _engine_contract(), "renderer": RenderingServer.get_current_rendering_method(), "display_server": DisplayServer.get_name(), "quality": "speedy", "aspect": [aspect_size.x, aspect_size.y], "harness_sha256": FileAccess.get_sha256(get_script().resource_path), "source_signature": capture_source_signature, "source_unchanged": capture_source_signature["sha256"] == source_after["sha256"], "save_isolation": {"before": normal_save_before, "after": normal_after, "unchanged": normal_save_before == normal_after, "fresh_fixture_save": isolated_save, "normal_save_file": ProjectSettings.globalize_path("user://reef_save.json")}, "checks": checks, "expected_ids": EXPECTED_IDS[run_case], "states": states, "failures": failures, "result": "PASS" if failures == 0 else "FAIL", "scope": "Current diagnostic native desktop Mobile captures. Synthetic pointer/button/route fixtures; save flags isolated; no replacement pixels or device/child/owner acceptance."}
	var out := FileAccess.open(capture_root.path_join("capture_manifest.json"), FileAccess.WRITE)
	out.store_string(JSON.stringify(manifest, "\t", true) + "\n")
	out.close()
	print("LIVE4|RESULT|%s|states=%d" % [manifest["result"], states.size()])
	quit(0 if failures == 0 else 1)

func _run_menu() -> void:
	var menu: StartMenu = capture_main._start_menu_ref()
	_check("startup save state matches fixture", capture_main.has_saved_game == (run_case == "saved"))
	await _capture(run_case + "_default", "StartMenuLaunchPanel")
	if run_case == "saved":
		_hover(menu._options_button)
		await _capture("saved_hover", "StartMenuOptionsTab")
		_pointer(menu._options_button, true)
		await _capture("saved_pressed", "StartMenuOptionsTab")
		_pointer(menu._options_button, false, true)
		await _frames(2)
		menu._close_options()
	await _click(menu._options_button)
	await _capture(run_case + "_options_on", "StartMenuOptionsShell")
	await _click(menu._music_button)
	await _click(menu._mic_button)
	await _capture(run_case + "_options_off", "StartMenuOptionsShell")
	await _click(_find("StartMenuOptionsCloseButton"))
	if run_case == "fresh":
		return
	await _click(menu._new_game_button)
	await _capture("confirm_disarmed", "StartMenuNewGameShell")
	var start: Button = _find("StartMenuConfirmNewGameButton")
	_check("confirmation initially disarmed", start.disabled)
	await _wait(1.65)
	await _capture("confirm_armed", "StartMenuNewGameShell")
	_check("confirmation armed", not start.disabled)
	var before: int = capture_main.save_generation
	_pointer(start, true)
	await _wait(0.18)
	await _capture("confirm_holding", "StartMenuNewGameHoldFill")
	_check("partial hold is visible", menu._new_game_hold_fill.size.x > 0.0 and menu._new_game_hold_active)
	_pointer(start, false)
	await _capture("confirm_cancelled", "StartMenuNewGameHoldCaption")
	await _wait(0.85)
	_check("partial hold preserves isolated progress", capture_main.save_generation == before and not FileAccess.file_exists(isolated_save + ".before_new_game"))
	await _click(_find("StartMenuKeepGameButton"))
	await _capture("saved_kept", "StartMenuLaunchPanel")

func _run_overlays() -> void:
	var m: ReefMain = capture_main
	m._start_menu_ref()._dismiss_menu()
	await _frames(3)
	m.day_one_active = false
	m.chapter2_active = false
	m._day_one_cancel_story_clips()
	m._enter_level2_now(true, false, false)
	await _frames(12)
	m._enter_castle_interior_now(false)
	await _frames(18)
	m._castle_rooms_ref().show_room("craft_room", false)
	await _frames(8)
	m.toggle_pause()
	await _capture("pause_castle", "PauseOverlay", true)
	m.toggle_pause()
	m.pearl_count = 0
	m.craft_unlocks = {}
	m._open_craft_studio()
	await _capture("craft_locked", "CraftPreviewPanel")
	await _click(_find("CraftKind_cat"))
	await _capture("craft_need_pearls", "CraftPreviewPanel")
	await _click(_find("CraftRainbowSwatch"))
	await _capture("craft_rainbow", "CraftPreviewPanel")
	m.pearl_count = 20
	await _click(_find("CraftKind_cat"))
	await _capture("craft_cat", "CraftPreviewPanel")
	await _click(_find("CraftKind_bird"))
	await _click(_find("CraftPart_third"))
	await _capture("craft_bird_detail", "CraftPreviewPanel")
	m._close_craft()
	await _frames(4)
	m.fairy_skin_unlocked = false
	m.skin_id = "classic"
	m._open_wardrobe()
	await _capture("wardrobe_locked", "WardrobeFeedbackLayer")
	var fairy_id := ""
	for entry: Dictionary in m.SKINS:
		if String(entry["id"]).begins_with("fairy"):
			fairy_id = String(entry["id"])
			break
	_check("fairy look exists", not fairy_id.is_empty())
	await _click(_find("WardrobeLook_" + fairy_id))
	await _capture("wardrobe_locked_feedback", "WardrobeFeedbackLayer")
	m.fairy_skin_unlocked = true
	m._wardrobe_ref()._wardrobe_refresh()
	await _capture("wardrobe_unlocked", "WardrobeFeedbackLayer")
	await _click(_find("WardrobeLook_" + fairy_id))
	await _capture("wardrobe_fairy_selected", "WardrobeFeedbackLayer")
	m._close_wardrobe()
	await _frames(4)
	m.stickers = {}
	m._open_stickers()
	await _capture("stickers_empty")
	m._close_stickers()
	await _frames(4)
	for d: Dictionary in m.STICKER_DEFS:
		m.stickers[String(d["id"])] = true
	m._open_stickers()
	await _capture("stickers_earned")
	m._close_stickers()
	await _frames(4)
	m.critter_collection = {}
	m._collection_ref().open_book()
	for category: String in ["fish", "insect", "bird"]:
		m._collection_ref()._switch_category(category)
		await _capture("critter_" + category + "_empty")
	for d: Dictionary in CollectionSystem.DEFS:
		m.critter_collection[String(d["id"])] = true
	for category: String in ["fish", "insect", "bird"]:
		m._collection_ref()._switch_category(category)
		await _capture("critter_" + category + "_caught")
	m._collection_ref().close_book()

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
		"algorithm": "sha256_opera_capture_source_closure_v2",
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

