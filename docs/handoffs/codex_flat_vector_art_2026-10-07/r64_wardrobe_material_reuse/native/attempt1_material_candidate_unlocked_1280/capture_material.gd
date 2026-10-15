extends "res://export/flat_vector_r64/base_capture.gd"
const MATERIAL_OWNER: Script = preload("res://export/flat_vector_r64/wardrobe_material_candidate.gd")
var candidate_enabled: bool = false

func _boot() -> bool:
	var ok: bool = await super._boot()
	if ok and candidate_enabled:
		m._wardrobe_ui = MATERIAL_OWNER.new(m) as WardrobeUI
	return ok

func _style_info(style: StyleBox) -> Dictionary:
	var row: Dictionary = {"class": style.get_class()}
	if style is StyleBoxTexture:
		var painted: StyleBoxTexture = style as StyleBoxTexture
		row.merge({"texture": _tex(painted.texture), "modulate_color": str(painted.modulate_color), "texture_margins": [painted.texture_margin_left, painted.texture_margin_top, painted.texture_margin_right, painted.texture_margin_bottom]})
	return row

func _materials() -> Dictionary:
	var row: Dictionary = {"active_legacy_picker": false, "panels": [], "buttons": [], "ornaments": [], "heading": {}}
	var stage: Control = m.wd.get("stage") as Control if is_instance_valid(m) else null
	if stage == null:
		return row
	row["active_legacy_picker"] = stage.find_child("WardrobeLook_classic", true, false) != null
	for child: Node in stage.get_children():
		if child is Panel:
			var panel: Panel = child as Panel
			if (panel.position == Vector2(28, 18) and panel.size == Vector2(1224, 684)) or (panel.position == Vector2(110, 110) and panel.size == Vector2(470, 560)):
				(row["panels"] as Array).append({"id": panel.get_instance_id(), "position": str(panel.position), "size": str(panel.size), "style": _style_info(panel.get_theme_stylebox("panel"))})
		if str(child.name).begins_with("WardrobeShellCrest") or str(child.name).begins_with("WardrobePearl"):
			(row["ornaments"] as Array).append({"id": child.get_instance_id(), "name": str(child.name)})
		if child is Label and (child as Label).text == "Pick your look!":
			var label: Label = child as Label
			row["heading"] = {"id": label.get_instance_id(), "text": label.text, "position": str(label.position), "size": str(label.size), "font_size": label.get_theme_font_size("font_size"), "line_count": label.get_line_count(), "visible_line_count": label.get_visible_line_count(), "autowrap_mode": label.autowrap_mode}
	for name: String in ["WardrobeLook_classic", "WardrobeLook_fairy", "WardrobeLook_huluu", "WardrobeFinishButton", "FashionWardrobeButton"]:
		var button: Button = stage.find_child(name, true, false) as Button
		if button != null:
			var styles: Dictionary = {}
			for state: String in ["normal", "hover", "pressed", "hover_pressed", "focus", "disabled"]:
				styles[state] = _style_info(button.get_theme_stylebox(state))
			(row["buttons"] as Array).append({"name": name, "id": button.get_instance_id(), "position": str(button.position), "size": str(button.size), "styles": styles, "pressed_connections": button.pressed.get_connections().size(), "selected": bool(button.get_meta("selected", false)), "locked": bool(button.get_meta("locked", false)), "modulate": str(button.modulate)})
	return row

func _snapshot() -> Dictionary:
	var row: Dictionary = super._snapshot()
	row["r64_candidate_enabled"] = candidate_enabled
	row["r64_materials"] = _materials()
	if is_instance_valid(m) and m._wardrobe_ui != null:
		var owner_script: Script = m._wardrobe_ui.get_script() as Script
		row["r64_owner_script"] = owner_script.resource_path
		if candidate_enabled:
			row["r64_shell_binding"] = (m._wardrobe_ui.get("r64_shell_binding") as Dictionary).duplicate(true)
	return row

func _capture(id: String, role := "IGNORED_R64_MATERIAL_CANDIDATE_OR_SOURCE_CONTROL") -> void:
	await super._capture(id, role)

func _open_original_wardrobe(id: String) -> bool:
	var ok: bool = await super._open_original_wardrobe(id)
	if not ok:
		return false
	var material: Dictionary = _materials()
	var expected: String = "StyleBoxTexture" if candidate_enabled else "StyleBoxFlat"
	var styles_ok: bool = (material["panels"] as Array).size() == 2 and (material["buttons"] as Array).size() == 5
	for panel: Dictionary in material["panels"]:
		styles_ok = styles_ok and str((panel["style"] as Dictionary)["class"]) == expected
	for button: Dictionary in material["buttons"]:
		for style: Dictionary in (button["styles"] as Dictionary).values():
			styles_ok = styles_ok and str(style["class"]) == expected
	_check("R64 declared material states " + id, styles_ok)
	var geometry_ok: bool = true
	for button: Dictionary in material["buttons"]:
		var name: String = str(button["name"])
		var target: Button = _button(name) as Button
		geometry_ok = geometry_ok and int(button["pressed_connections"]) >= 1
		if name.begins_with("WardrobeLook_"):
			geometry_ok = geometry_ok and target.size == Vector2(480, 110)
		elif name == "WardrobeFinishButton":
			geometry_ok = geometry_ok and target.size == Vector2(330, 132)
		else:
			geometry_ok = geometry_ok and target.size == Vector2(132, 132)
	_check("R64 original target sizes and callbacks " + id, geometry_ok)
	var title: Dictionary = material["heading"] as Dictionary
	_check("R64 declared heading disposition " + id, str(title.get("text")) == "Pick your look!" and (not candidate_enabled or (str(title.get("size")) == "(430.0, 64.0)" and int(title.get("line_count", 0)) == 1)))
	_check("R64 duplicate ornament ownership " + id, (material["ornaments"] as Array).size() == (0 if candidate_enabled else 5))
	return true

func _run() -> void:
	candidate_enabled = OS.get_environment("R64_CANDIDATE") == "true"
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
	var report: Dictionary = {"schema": "reef.wardrobe_material_candidate/1", "candidate_enabled": candidate_enabled, "fixture_variant": "R64_IGNORED_SUBCLASS_ORIGINAL_BEHAVIOR", "source_revision": OS.get_environment("R63_REV"),
		"engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(),
		"quality_requested": "speedy", "aspect": [width, 720], "time_scale": Engine.time_scale,
		"states": states, "events": events, "seed": seed, "private_profile": profile, "boot_count": boot_count,
		"route_events": route_events, "mode": "IGNORED_MATERIAL_CANDIDATE" if candidate_enabled else "CURRENT_ORIGINAL_SOURCE_CONTROL", "fairy_unlocked_profile": fairy_unlocked,
		"checks": checks, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors,
		"actual_child_data": false, "normal_route_proved": false,
		"scope": "R64 explicit ignored WardrobeUI subclass bound after declared private boot, before original room/input route. Candidate changes only material/title/decorative ownership; inherited original choices/save/feedback/close. Source control retains original owner. Same exact private profiles and33checks, added material/heading/target/callback/ornament checks. Original R63 helper/env/unknown-key marker retained for exact behavior lineage. No production/source pixels/identity/save keys/progress/clock/camera or generation changes;Fashion entry only. NotfullQA11/freshOS/device/audio/performance/child/owner/newuse/creative acceptance."}
	var output: FileAccess = FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("WARDROBE64|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
