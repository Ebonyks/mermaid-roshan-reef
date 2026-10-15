extends "res://export/flat_vector_r65/base_capture.gd"
const MATERIAL_OWNER: Script = preload("res://export/flat_vector_r65/wardrobe_cached_fit_candidate.gd")
const PREVIOUS_OWNER: Script = preload("res://export/flat_vector_r65/wardrobe_previous_candidate.gd")
var candidate_enabled: bool = true
var refined_enabled: bool = false
var retired_owners: Array[Dictionary] = []

func _boot() -> bool:
	var ok: bool = await super._boot()
	if ok:
		m._wardrobe_ui = MATERIAL_OWNER.new(m) as WardrobeUI if refined_enabled else PREVIOUS_OWNER.new(m) as WardrobeUI
	return ok

func _style_info(style: StyleBox) -> Dictionary:
	var row: Dictionary = {"class": style.get_class(), "resource_id": style.get_instance_id(), "content_margins": [style.content_margin_left, style.content_margin_top, style.content_margin_right, style.content_margin_bottom]}
	if style is StyleBoxTexture:
		var painted: StyleBoxTexture = style as StyleBoxTexture
		row.merge({"texture": _tex(painted.texture), "modulate_color": str(painted.modulate_color), "texture_margins": [painted.texture_margin_left, painted.texture_margin_top, painted.texture_margin_right, painted.texture_margin_bottom], "region_rect": str(painted.region_rect)})
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
	row["r65_refined_enabled"] = refined_enabled
	row["r65_fit"] = _fit_details()
	row["r65_retired_owners"] = retired_owners.duplicate(true)
	row["r64_materials"] = _materials()
	if is_instance_valid(m) and m._wardrobe_ui != null:
		var owner_script: Script = m._wardrobe_ui.get_script() as Script
		row["r64_owner_script"] = owner_script.resource_path
		if refined_enabled:
			row["r65_cache"] = m._wardrobe_ui.call("r65_stats")
		if candidate_enabled:
			row["r64_shell_binding"] = (m._wardrobe_ui.get("r64_shell_binding") as Dictionary).duplicate(true)
	return row

func _capture(id: String, role := "IGNORED_R65_CACHED_FIT_OR_IMMUTABLE_R64_CONTROL") -> void:
	await super._capture(id, role)

func _fit_details() -> Dictionary:
	var result: Dictionary = {"active": false, "buttons": []}
	var stage: Control = m.wd.get("stage") as Control if is_instance_valid(m) else null
	if stage == null or stage.find_child("WardrobeLook_classic", true, false) == null:
		return result
	result["active"] = true
	for name: String in ["WardrobeLook_classic", "WardrobeLook_fairy", "WardrobeLook_huluu", "WardrobeFinishButton", "FashionWardrobeButton"]:
		var button: Button = stage.find_child(name, true, false) as Button
		if button == null:
			continue
		var styles: Dictionary = {}
		for state: String in ["normal", "hover", "pressed", "hover_pressed", "focus", "disabled"]:
			styles[state] = _style_info(button.get_theme_stylebox(state))
		var frame: Panel = button.get_node_or_null("R65PaintedFrame") as Panel
		var row: Dictionary = {"name": name, "id": button.get_instance_id(), "position": str(button.position), "size": str(button.size), "global_rect": str(button.get_global_rect()), "styles": styles, "pressed_connections": button.pressed.get_connections().size(), "selected": bool(button.get_meta("selected", false)), "locked": bool(button.get_meta("locked", false)), "pressed": button.is_pressed(), "hovered": button.is_hovered(), "focus": button.has_focus(), "text": button.text}
		var font: Font = button.get_theme_font("font")
		var font_size: int = button.get_theme_font_size("font_size")
		row["font_size"] = font_size
		row["font_text_size"] = str(font.get_string_size(button.text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size))
		if name.begins_with("WardrobeLook_"):
			var portrait: TextureRect = button.get_node_or_null("WardrobeLookPreview_" + name.trim_prefix("WardrobeLook_")) as TextureRect
			row["portrait"] = {"id": portrait.get_instance_id(), "position": str(portrait.position), "size": str(portrait.size), "texture": _texture_evidence(portrait.texture), "stretch_mode": portrait.stretch_mode}
		if frame != null:
			row["frame"] = {"id": frame.get_instance_id(), "position": str(frame.position), "size": str(frame.size), "scale": str(frame.scale), "global_rect": str(frame.get_global_rect()), "mouse_filter": frame.mouse_filter, "behind_parent": frame.show_behind_parent, "style": _style_info(frame.get_theme_stylebox("panel")), "mode": str(frame.get_meta("r65_frame_mode", ""))}
		(result["buttons"] as Array).append(row)
	return result

func _fit_valid(details: Dictionary) -> bool:
	if not bool(details["active"]) or (details["buttons"] as Array).size() != 5:
		return false
	for button: Dictionary in details["buttons"]:
		for style: Dictionary in (button["styles"] as Dictionary).values():
			if str(style["class"]) != ("StyleBoxEmpty" if refined_enabled else "StyleBoxTexture"):
				return false
		if refined_enabled:
			var frame: Dictionary = button.get("frame", {}) as Dictionary
			if frame.is_empty() or not bool(frame["behind_parent"]) or int(frame["mouse_filter"]) != Control.MOUSE_FILTER_IGNORE or str((frame["style"] as Dictionary)["class"]) != "StyleBoxTexture":
				return false
	return true

func _targets_valid(details: Dictionary) -> bool:
	for row: Dictionary in details["buttons"]:
		var name: String = str(row["name"])
		var button: Button = _button(name) as Button
		if int(row["pressed_connections"]) < 1:
			return false
		if name.begins_with("WardrobeLook_"):
			if button.size != Vector2(480, 110) or str((row["portrait"] as Dictionary)["size"]) != "(96.0, 94.0)" or str((row["portrait"] as Dictionary)["position"]) != "(10.0, 8.0)":
				return false
		elif name == "WardrobeFinishButton":
			if button.size != Vector2(330, 132):
				return false
		elif button.size != Vector2(132, 132):
			return false
	return true

func _retire(flush := true) -> void:
	if not is_instance_valid(m):
		return
	var ref: WeakRef = weakref(m._wardrobe_ui) if is_instance_valid(m) and m._wardrobe_ui != null else null
	var cache_before: Dictionary = m._wardrobe_ui.call("r65_stats") if refined_enabled and is_instance_valid(m) else {}
	await super._retire(flush)
	await _frames(3)
	retired_owners.append({"owner_valid_after_3frames": ref != null and ref.get_ref() != null, "cache_before": cache_before, "scope": "Observed weak owner lifetime; no strong test reference retained, not a global leak/profile proof."})

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
	var details: Dictionary = _fit_details()
	_check("R65 expected frame/input ownership " + id, _fit_valid(details))
	_check("R65 unchanged original targets and portraits " + id, _targets_valid(details))
	_check("R65 cached resources or prior exact owner " + id, not refined_enabled or int((m._wardrobe_ui.call("r65_stats") as Dictionary)["style_creations"]) == 5)
	var material: Dictionary = _materials()
	_check("R65 original one-line heading retained " + id, str((material["heading"] as Dictionary).get("size")) == "(430.0, 64.0)" and int((material["heading"] as Dictionary).get("line_count", 0)) == 1)
	if id == "initial":
		await _native_state_diagnostic()
	return true

func _native_state_diagnostic() -> void:
	var target: Button = _button("WardrobeLook_fairy") as Button
	var motion := InputEventMouseMotion.new()
	motion.position = _point(target, target.size * 0.5)
	events.append({"type": "mouse_motion", "point": str(motion.position), "target": str(target.get_path()), "scope": "Native GUI state diagnostic only; no choice/hover/focus flags written."})
	target.get_viewport().push_input(motion, true)
	await _frames(3)
	await _capture("native_fairy_hover_diagnostic")
	_check("native mouse hover reaches original Fairy target", target.is_hovered())
	var key := InputEventKey.new()
	key.keycode = KEY_TAB
	key.pressed = true
	events.append({"type": "key", "key": "TAB", "pressed": true, "scope": "Native focus navigation diagnostic; no direct grab_focus or focus flag writes."})
	target.get_viewport().push_input(key, true)
	await _frames(1)
	key = InputEventKey.new()
	key.keycode = KEY_TAB
	key.pressed = false
	target.get_viewport().push_input(key, true)
	events.append({"type": "key", "key": "TAB", "pressed": false})
	await _frames(3)
	await _capture("native_tab_focus_diagnostic")

func _run() -> void:
	candidate_enabled = true
	refined_enabled = OS.get_environment("R65_REFINED") == "true"
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
	var report: Dictionary = {"schema": "reef.wardrobe_cached_fit/1", "refined_enabled": refined_enabled, "candidate_enabled": candidate_enabled, "fixture_variant": "R65_CACHED_FIT_OR_IMMUTABLE_R64_CONTROL", "source_revision": OS.get_environment("R63_REV"),
		"engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(),
		"quality_requested": "speedy", "aspect": [width, 720], "time_scale": Engine.time_scale,
		"states": states, "events": events, "r65_retired_owners": retired_owners, "seed": seed, "private_profile": profile, "boot_count": boot_count,
		"route_events": route_events, "mode": "R65_REFINED_CANDIDATE" if refined_enabled else "IMMUTABLE_R64_CANDIDATE_CONTROL", "fairy_unlocked_profile": fairy_unlocked,
		"checks": checks, "normal_before": normal_before, "normal_after": _normal_hashes(), "errors": errors,
		"actual_child_data": false, "normal_route_proved": false,
		"scope": "R65 ignored cache/fit refinement or exact R64candidate control. Original source targets96x94portraits/choices/save/feedback/Done/Back and33behavior checks preserved; source refresh data/typography semantics retained withoutallocatingstylehelper. Visibleframe is owned painted child behindemptyinputowner, one-third sourceborder scale,14pxtotalvertical draw expansion, text inset36. Fiveimmutable candidate style resources perMain owner; inheritedbaseopen allocations/unmeasuredGPU/phone/QA11/child/owner remainopen. OriginalR63privateprofile/envmarker retained. No production/sourcepixels/identity/savekeys/clock/progress/camera/newart/acceptedremoval."}
	var output: FileAccess = FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("WARDROBE65|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
