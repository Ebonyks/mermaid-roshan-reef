extends SceneTree
## Non-runtime R5 diagnostic companion/logo/attack UI capture; isolated save; no child acceptance.
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
  "companion": [
    "picker_starters_eagle",
    "picker_starters_mewsha",
    "picker_unlocked_lamma",
    "picker_swap",
    "picker_studio_eagle",
    "picker_studio_lamma",
    "picker_studio_mewsha",
    "palette_0_0",
    "palette_0_1",
    "palette_0_2",
    "palette_0_3",
    "palette_0_4",
    "palette_0_5",
    "palette_0_6",
    "palette_0_7",
    "palette_1_0",
    "palette_1_1",
    "palette_1_2",
    "palette_1_3",
    "palette_1_4",
    "palette_1_5",
    "palette_1_6",
    "palette_1_7",
    "palette_2_0",
    "palette_2_1",
    "palette_2_2",
    "palette_2_3",
    "palette_2_4",
    "palette_2_5",
    "palette_2_6",
    "palette_2_7",
    "picker_rescue_current_step2",
    "care_eagle_idle",
    "care_lamma_idle",
    "care_mewsha_idle",
    "care_active_feed",
    "care_active_nap",
    "care_active_bath",
    "care_active_cuddle",
    "care_active_play",
    "care_queued_feed",
    "care_queued_nap",
    "care_queued_bath",
    "care_queued_cuddle",
    "care_queued_play",
    "care_bruises",
    "care_busy",
    "care_growth_1",
    "care_growth_2",
    "care_growth_3",
    "care_growth_4",
    "care_canvas_fulfilled"
  ],
  "logo": [
    "logo_pink_rainbow",
    "logo_pink_shell",
    "logo_pink_kitty",
    "logo_pink_dog",
    "logo_pink_star",
    "logo_pink_heart",
    "logo_pink_crown",
    "logo_pink_butterfly",
    "logo_gold_rainbow",
    "logo_gold_shell",
    "logo_gold_kitty",
    "logo_gold_dog",
    "logo_gold_star",
    "logo_gold_heart",
    "logo_gold_crown",
    "logo_gold_butterfly",
    "logo_mint_rainbow",
    "logo_mint_shell",
    "logo_mint_kitty",
    "logo_mint_dog",
    "logo_mint_star",
    "logo_mint_heart",
    "logo_mint_crown",
    "logo_mint_butterfly",
    "logo_ocean_rainbow",
    "logo_ocean_shell",
    "logo_ocean_kitty",
    "logo_ocean_dog",
    "logo_ocean_star",
    "logo_ocean_heart",
    "logo_ocean_crown",
    "logo_ocean_butterfly",
    "logo_purple_rainbow",
    "logo_purple_shell",
    "logo_purple_kitty",
    "logo_purple_dog",
    "logo_purple_star",
    "logo_purple_heart",
    "logo_purple_crown",
    "logo_purple_butterfly",
    "logo_rainbow_rainbow",
    "logo_rainbow_shell",
    "logo_rainbow_kitty",
    "logo_rainbow_dog",
    "logo_rainbow_star",
    "logo_rainbow_heart",
    "logo_rainbow_crown",
    "logo_rainbow_butterfly",
    "logo_hover",
    "logo_pressed",
    "logo_cancel_restored",
    "logo_commit_feedback",
    "logo_badge_pink",
    "logo_badge_gold",
    "logo_badge_mint",
    "logo_badge_ocean",
    "logo_badge_purple",
    "logo_badge_rainbow",
    "logo_playroom_banners",
    "logo_no_room_badge"
  ],
  "attack": [
    "attack_0_bubbles",
    "attack_0_splashes",
    "attack_1_bubbles",
    "attack_1_splashes",
    "attack_2_bubbles",
    "attack_2_splashes",
    "attack_3_bubbles",
    "attack_3_splashes",
    "attack_4_bubbles",
    "attack_4_splashes",
    "attack_hover",
    "attack_pressed",
    "attack_confirmed"
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
	print("LIVE5|%s|%s|%s|%s" % [run_case, "PASS" if ok else "FAIL", label, detail])

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
			for key: String in ["normal", "hover", "pressed", "disabled", "focus", "panel"]:
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

func _snapshot() -> Dictionary:
	var m: ReefMain = capture_main
	var canvas: Array[Dictionary] = []
	_collect_visible(m, canvas)
	return {"save_path": m._save_state.save_path, "tree_paused": paused, "start_menu_active": m.start_menu_active, "intro_active": m.intro_active, "story_clip_present": is_instance_valid(m._day_one_story_clip), "fade_alpha": m.fade_rect.color.a * m.fade_rect.modulate.a * m.fade_rect.self_modulate.a if m.fade_rect != null and m.fade_rect.visible else 0.0, "castle_room": m.castle_room_id, "game": m.game, "phase": String(m.g.get("phase", "")), "visible_canvas": canvas, "save_generation": m.save_generation, "companion_id": m.companion_id, "pick_id": m.companion_pick_id, "pick_mode": m.companion_pick_mode, "pick_slot": m.companion_pick_slot, "pick_colors": m.companion_pick_colors.duplicate(), "stuffie_wins": m.stuffie_wins.duplicate(), "care_points": m.care_points, "care_want": m.companion_want, "care_queue": m.companion_want_queue.duplicate(), "care_t": m.companion_care_t, "bruises": m.companion_bruises, "rescue_step": int(m.g.get("stuffie_rescue_tutorial_step", -1)), "rescue": bool(m.g.get("stuffie_rescue_tutorial", false)), "picker_visible": is_instance_valid(m.companion_layer) and m.companion_layer.visible, "care_visible": is_instance_valid(m.companion_care_layer) and m.companion_care_layer.visible, "logo_visible": is_instance_valid(m.castle_logo_layer) and m.castle_logo_layer.visible, "logo_color": m.castle_logo_color, "logo_symbol": m.castle_logo_symbol, "attack_color": m.attack_color.to_html(), "attack_effect": m.attack_effect, "attack_visible": m._attack_customizer_ref().is_open}

func _capture(id: String, required_name: String = "", expected_pause: bool = false) -> void:
	await _frames(3)
	await RenderingServer.frame_post_draw
	var actual := _snapshot()
	var valid: bool = actual["save_path"] == isolated_save and bool(actual["tree_paused"]) == expected_pause and not actual["story_clip_present"] and float(actual["fade_alpha"]) <= 0.001
	valid = valid and not actual["start_menu_active"] and not actual["intro_active"]
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
	_check("native state/image " + id, valid, "required=%s paused=%s" % [required_name, expected_pause])
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	states.append({"id": id, "sequence": states.size(), "status": "PASS" if valid else "FAIL", "expected_top_target": required_name, "variant_expect": variant_expect.duplicate(), "expected_pause": expected_pause, "actual": actual, "image": {"file": id + ".png", "width": image.get_width(), "height": image.get_height(), "bytes": file.get_length(), "sha256": FileAccess.get_sha256(path)}})
	file.close()

func _run() -> void:
	run_case = OS.get_environment("LIVE5_CASE")
	capture_root = OS.get_environment("LIVE5_OUT")
	var aspect := OS.get_environment("LIVE5_ASPECT").split("x")
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
		"companion": await _run_companion()
		"logo": await _run_logo()
		"attack": await _run_attack()
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
	var manifest := {"schema": "reef.flat_vector.live_companion_controls.v1", "source_revision": OS.get_environment("GITHUB_SHA"), "run_case": run_case, "engine": _engine_contract(), "renderer": RenderingServer.get_current_rendering_method(), "display_server": DisplayServer.get_name(), "quality": "speedy", "aspect": [aspect_size.x, aspect_size.y], "harness_sha256": FileAccess.get_sha256(get_script().resource_path), "source_signature": capture_source_signature, "source_unchanged": capture_source_signature["sha256"] == source_after["sha256"], "save_isolation": {"before": normal_save_before, "after": normal_after, "unchanged": normal_save_before == normal_after, "fresh_fixture_save": isolated_save, "normal_save_file": ProjectSettings.globalize_path("user://reef_save.json")}, "checks": checks, "expected_ids": EXPECTED_IDS[run_case], "states": states, "failures": failures, "result": "PASS" if failures == 0 else "FAIL", "scope": "Current diagnostic native desktop Mobile captures. Synthetic pointer/button/route fixtures; save flags isolated; no replacement pixels or device/child/owner acceptance."}
	var out := FileAccess.open(capture_root.path_join("capture_manifest.json"), FileAccess.WRITE)
	out.store_string(JSON.stringify(manifest, "\t", true) + "\n")
	out.close()
	print("LIVE5|RESULT|%s|states=%d" % [manifest["result"], states.size()])
	quit(0 if failures == 0 else 1)

func _setup_route() -> void:
	var m: ReefMain = capture_main
	m._start_menu_ref()._dismiss_menu()
	await _frames(3)
	m.day_one_active = false
	m.chapter2_active = false
	m._day_one_cancel_story_clips()
	m._enter_level2_now(true, false, false)
	await _frames(12)
	if run_case != "companion":
		m._enter_castle_interior_now(false)
		await _frames(18)
		m._castle_rooms_ref().show_room("craft_room", false)
		await _frames(8)

func _comp() -> CompanionSystem:
	return capture_main._companion_ref()

func _picker(id: String, mode: String, preselect: String) -> void:
	_comp().close_picker()
	await _frames(3)
	_comp().open_picker(true, preselect, mode)
	variant_expect = {"picker_visible": true, "care_visible": false, "pick_mode": mode, "pick_id": preselect}
	await _capture(id, "StuffieConfirmButton")

func _care(id: String, friend: String, want: String = "", queue: Array[String] = [], bruises: int = 0, busy: float = -1.0, points: int = 0) -> void:
	var m: ReefMain = capture_main
	_comp().close_care_menu()
	await _frames(3)
	m.companion_id = friend
	m.companion_want = want
	m.companion_want_queue = queue.duplicate()
	m.companion_bruises = bruises
	m.companion_care_t = busy
	m.companion_want_cool = 10000.0
	m.care_points = points
	_comp().open_care_menu()
	variant_expect = {"care_visible": true, "picker_visible": false, "companion_id": friend, "care_want": want, "care_queue": queue.duplicate(), "bruises": bruises, "care_points": points, "phase": "promenade"}
	await _capture(id, "StuffieCurrentNeed")

func _run_companion() -> void:
	var m: ReefMain = capture_main
	m.companion_want_cool = 10000.0
	m.stuffie_wins = {}
	await _picker("picker_starters_eagle", "adopt", "eagle")
	await _click(_find("StuffieCard_mewsha"))
	variant_expect["pick_id"] = "mewsha"
	await _capture("picker_starters_mewsha", "StuffiePart_0")
	m.stuffie_wins = {"friend_lamma": true}
	await _picker("picker_unlocked_lamma", "adopt", "lamma")
	await _picker("picker_swap", "swap", "mewsha")
	for friend: String in ["eagle", "lamma", "mewsha"]:
		m.companion_id = friend
		await _picker("picker_studio_" + friend, "studio", friend)
	for slot: int in range(3):
		await _click(_find("StuffiePart_%d" % slot))
		variant_expect["pick_slot"] = slot
		for color: int in range(8):
			await _click(_find("StuffieSwatch_%d" % color))
			await _capture("palette_%d_%d" % [slot, color], "StuffieSwatch_%d" % color)
	_comp().close_picker()
	await _frames(3)
	m.companion_id = ""
	m.companion_pick_id = ""
	m.day_one_active = false
	m._enter_castle_interior_now(false)
	await _frames(18)
	m._castle_rooms_ref().show_room("playroom", false)
	await _frames(8)
	m.day_one_active = true
	m._castle_rooms_ref()._open_playroom_stuffie_tutorial()
	variant_expect = {"picker_visible": true, "pick_id": "eagle", "pick_mode": "adopt", "rescue": true, "rescue_step": 2, "castle_room": "playroom", "phase": "hall"}
	await _capture("picker_rescue_current_step2", "StuffieRescueTutorialFocus")
	_comp().close_picker()
	m.g.erase("stuffie_rescue_tutorial")
	m.g.erase("stuffie_rescue_tutorial_step")
	m.day_one_active = false
	m._day_one_cancel_story_clips()
	m._enter_level2_now(true, false, false)
	await _frames(12)
	for friend: String in ["eagle", "lamma", "mewsha"]:
		await _care("care_" + friend + "_idle", friend)
	for want: String in ["feed", "nap", "bath", "cuddle", "play"]:
		await _care("care_active_" + want, "mewsha", want)
	for want: String in ["feed", "nap", "bath", "cuddle", "play"]:
		await _care("care_queued_" + want, "mewsha", "", [want])
	await _care("care_bruises", "mewsha", "", [], 2)
	await _care("care_busy", "mewsha", "feed", [], 0, 100.0)
	for points: int in [1, 2, 3, 4]:
		await _care("care_growth_%d" % points, "mewsha", "", [], 0, -1.0, points)
	_comp().close_care_menu()
	await _frames(3)
	m.companion_id = "mewsha"
	m.companion_want = "feed"
	m.companion_want_queue = []
	m.companion_care_t = -1.0
	m.companion_bruises = 0
	m.care_points = 0
	_comp().open_care_menu()
	await _frames(3)
	await _click(_find("StuffieCareAction_feed"))
	variant_expect = {"care_visible": true, "care_want": "", "care_points": 1, "phase": "promenade"}
	await _capture("care_canvas_fulfilled", "StuffieCurrentNeed")
	_comp().close_care_menu()

func _run_logo() -> void:
	var m: ReefMain = capture_main
	m.castle_logo_color = "rainbow"
	m.castle_logo_symbol = "rainbow"
	m._castle_logo_ref().refresh_room_display()
	m._castle_logo_ref().open()
	for color: String in ["pink", "gold", "mint", "ocean", "purple", "rainbow"]:
		await _click(_find("CastleLogoColor_" + color))
		for symbol: String in ["rainbow", "shell", "kitty", "dog", "star", "heart", "crown", "butterfly"]:
			await _click(_find("CastleLogoSymbol_" + symbol))
			variant_expect = {"logo_visible": true, "logo_color": color, "logo_symbol": symbol}
			await _capture("logo_%s_%s" % [color, symbol], "CastleLogoPreview")
	var swatch := _find("CastleLogoColor_pink")
	_hover(swatch)
	await _capture("logo_hover", "CastleLogoColor_pink")
	_pointer(swatch, true)
	await _capture("logo_pressed", "CastleLogoColor_pink")
	_pointer(swatch, false, true)
	m._castle_logo_ref().close(false)
	await _frames(4)
	variant_expect = {"logo_visible": false, "logo_color": "rainbow", "logo_symbol": "rainbow"}
	await _capture("logo_cancel_restored", "CastleLogoCraftBoardBadge")
	m._castle_logo_ref().open()
	await _click(_find("CastleLogoColor_gold"))
	variant_expect = {"logo_visible": true, "logo_color": "gold", "logo_symbol": "rainbow"}
	await _click(_find("CastleLogoFinishButton"))
	await _capture("logo_commit_feedback", "CastleLogoStatus")
	await _wait(1.0)
	for color: String in ["pink", "gold", "mint", "ocean", "purple", "rainbow"]:
		m.castle_logo_color = color
		m._castle_logo_ref().refresh_room_display()
		variant_expect = {"logo_visible": false, "logo_color": color, "castle_room": "craft_room"}
		await _capture("logo_badge_" + color, "CastleLogoCraftBoardBadge")
	m._castle_rooms_ref().show_room("playroom", false)
	await _frames(5)
	variant_expect = {"logo_visible": false, "castle_room": "playroom"}
	await _capture("logo_playroom_banners", "CastleLogoBanner_0")
	m._castle_rooms_ref().show_room("family_gallery", false)
	await _frames(5)
	variant_expect = {"logo_visible": false, "castle_room": "family_gallery"}
	await _capture("logo_no_room_badge", "CastleRoomsCanvasWorld")

func _run_attack() -> void:
	var m: ReefMain = capture_main
	m._open_attack_customizer()
	var ui: AttackCustomizer = m._attack_customizer_ref()
	for color: int in range(5):
		await _click(ui._color_buttons[color])
		for effect: int in range(2):
			await _click(ui._effect_buttons[effect])
			variant_expect = {"attack_visible": true, "attack_color": AttackCustomizer.COLORS[color].to_html(), "attack_effect": AttackCustomizer.EFFECTS[effect]}
			await _capture("attack_%d_%s" % [color, AttackCustomizer.EFFECTS[effect]], "AttackCustomizerCard")
	_hover(ui._color_buttons[0])
	await _capture("attack_hover", "AttackCustomizerCard")
	_pointer(ui._color_buttons[0], true)
	await _capture("attack_pressed", "AttackCustomizerCard")
	_pointer(ui._color_buttons[0], false, true)
	ui.close()
	await _frames(4)
	variant_expect = {"attack_visible": false}
	await _capture("attack_confirmed", "CastleLogoCraftBoardBadge")

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

