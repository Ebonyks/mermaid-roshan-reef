from pathlib import Path
import shutil
R=Path.cwd();H=R/'docs/handoffs/codex_flat_vector_art_2026-10-07';P=H/'r65_wardrobe_cached_fit';O=H/'r64_wardrobe_material_reuse';W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-wardrobe-cached-fit-20261015')
t=(O/'capture_material.gd').read_text(encoding='utf-8-sig').replace('export/flat_vector_r64/','export/flat_vector_r65/').replace('wardrobe_material_candidate.gd','wardrobe_cached_fit_candidate.gd')
t=t.replace('var candidate_enabled: bool = false','const PREVIOUS_OWNER: Script = preload("res://export/flat_vector_r65/wardrobe_previous_candidate.gd")\nvar candidate_enabled: bool = true\nvar refined_enabled: bool = false\nvar retired_owners: Array[Dictionary] = []')
t=t.replace('if ok and candidate_enabled:\n\t\tm._wardrobe_ui = MATERIAL_OWNER.new(m) as WardrobeUI','if ok:\n\t\tm._wardrobe_ui = MATERIAL_OWNER.new(m) as WardrobeUI if refined_enabled else PREVIOUS_OWNER.new(m) as WardrobeUI')
t=t.replace('var row: Dictionary = {"class": style.get_class()}','var row: Dictionary = {"class": style.get_class(), "resource_id": style.get_instance_id(), "content_margins": [style.content_margin_left, style.content_margin_top, style.content_margin_right, style.content_margin_bottom]}')
t=t.replace('"texture_margins": [painted.texture_margin_left, painted.texture_margin_top, painted.texture_margin_right, painted.texture_margin_bottom]','"texture_margins": [painted.texture_margin_left, painted.texture_margin_top, painted.texture_margin_right, painted.texture_margin_bottom], "region_rect": str(painted.region_rect)')
t=t.replace('row["r64_candidate_enabled"] = candidate_enabled','row["r64_candidate_enabled"] = candidate_enabled\n\trow["r65_refined_enabled"] = refined_enabled\n\trow["r65_fit"] = _fit_details()\n\trow["r65_retired_owners"] = retired_owners.duplicate(true)')
t=t.replace('row["r64_owner_script"] = owner_script.resource_path','row["r64_owner_script"] = owner_script.resource_path\n\t\tif refined_enabled:\n\t\t\trow["r65_cache"] = m._wardrobe_ui.call("r65_stats")')
a=t.index('func _open_original_wardrobe(');b=t.index('func _run()',a)
base=(P/'base_capture.gd').read_text(encoding='utf-8-sig');func=base[base.index('func _open_original_wardrobe('):base.index('func _pick_original(')]
func=func.replace('\treturn true\n','''	var details: Dictionary = _fit_details()
	_check("R65 expected frame/input ownership " + id, _fit_valid(details))
	_check("R65 unchanged original targets and portraits " + id, _targets_valid(details))
	_check("R65 cached resources or prior exact owner " + id, not refined_enabled or int((m._wardrobe_ui.call("r65_stats") as Dictionary)["style_creations"]) == 5)
	var material: Dictionary = _materials()
	_check("R65 original one-line heading retained " + id, str((material["heading"] as Dictionary).get("size")) == "(430.0, 64.0)" and int((material["heading"] as Dictionary).get("line_count", 0)) == 1)
	return true
''')
extra='''func _fit_details() -> Dictionary:
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
	var ref: WeakRef = weakref(m._wardrobe_ui) if is_instance_valid(m) and m._wardrobe_ui != null else null
	var cache_before: Dictionary = m._wardrobe_ui.call("r65_stats") if refined_enabled and is_instance_valid(m) else {}
	await super._retire(flush)
	await _frames(3)
	retired_owners.append({"owner_valid_after_3frames": ref != null and ref.get_ref() != null, "cache_before": cache_before, "scope": "Observed weak owner lifetime; no strong test reference retained, not a global leak/profile proof."})

'''
t=t[:a]+extra+func+t[b:]
t=t.replace('candidate_enabled = OS.get_environment("R64_CANDIDATE") == "true"','candidate_enabled = true\n\trefined_enabled = OS.get_environment("R65_REFINED") == "true"')
t=t.replace('"reef.wardrobe_material_candidate/1"','"reef.wardrobe_cached_fit/1", "refined_enabled": refined_enabled')
t=t.replace('"R64_IGNORED_SUBCLASS_ORIGINAL_BEHAVIOR"','"R65_CACHED_FIT_OR_IMMUTABLE_R64_CONTROL"').replace('"IGNORED_MATERIAL_CANDIDATE" if candidate_enabled else "CURRENT_ORIGINAL_SOURCE_CONTROL"','"R65_REFINED_CANDIDATE" if refined_enabled else "IMMUTABLE_R64_CANDIDATE_CONTROL"')
i=t.index('\t\t"scope": ');j=t.index('\n\tvar output:',i);t=t[:i]+'''\t\t"scope": "R65 ignored cache/fit refinement or exact R64candidate control. Original source targets96x94portraits/choices/save/feedback/Done/Back and33behavior checks preserved; source refresh data/typography semantics retained withoutallocatingstylehelper. Visibleframe is owned painted child behindemptyinputowner, one-third sourceborder scale,14pxtotalvertical draw expansion, text inset36. Fiveimmutable candidate style resources perMain owner; inheritedbaseopen allocations/unmeasuredGPU/phone/QA11/child/owner remainopen. OriginalR63privateprofile/envmarker retained. No production/sourcepixels/identity/savekeys/clock/progress/camera/newart/acceptedremoval."}''' +t[j:]
t=t.replace('WARDROBE64|RESULT','WARDROBE65|RESULT');(P/'capture_fit.gd').write_text(t,encoding='utf-8',newline='\n')
tear=(O/'capture_teardown.gd').read_text(encoding='utf-8-sig').replace('extends "res://export/flat_vector_r64/capture_material.gd"','extends "res://export/flat_vector_r65/capture_fit.gd"');(P/'capture_teardown.gd').write_text(tear,encoding='utf-8',newline='\n')
E=W/'export/flat_vector_r65';E.mkdir(parents=True,exist_ok=True);(E/'.gdignore').write_text('',encoding='utf-8')
for n in ['base_capture.gd','wardrobe_cached_fit_candidate.gd','wardrobe_previous_candidate.gd','capture_fit.gd','capture_teardown.gd']:shutil.copyfile(P/n,E/n)
print('R65_FIXTURE_BUILT')
