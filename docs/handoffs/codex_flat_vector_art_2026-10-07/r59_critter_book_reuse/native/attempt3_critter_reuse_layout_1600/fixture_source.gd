extends "res://export/flat_vector_r59/base_capture_critter.gd"

const PANEL_PATH := "res://assets/fashion/skin_engine_v2/ui/wardrobe_panel.png"
const CARD_PATH := "res://assets/fashion/skin_engine_v2/ui/wardrobe_card.png"
var panel_picture: Texture2D = preload(PANEL_PATH)
var card_picture: Texture2D = preload(CARD_PATH)
var selected_badge: AtlasTexture
var trial_mode := ""
var originals: Dictionary = {}
var applied_frames: int = 0

func _run() -> void:
	trial_mode = OS.get_environment("R59_MODE")
	if trial_mode not in ["layout", "painted"]:
		quit(1)
		return
	selected_badge = AtlasTexture.new()
	selected_badge.atlas = panel_picture
	selected_badge.region = Rect2(430.0, 0.0, 165.0, 116.0)
	process_frame.connect(_refresh_candidate)
	await super._run()

func _callbacks(button: Button) -> Array[String]:
	var result: Array[String] = []
	for row: Dictionary in button.get_signal_connection_list("pressed"):
		result.append(str(row["callable"]))
	return result

func _remember(control: Control) -> Dictionary:
	var key: int = control.get_instance_id()
	if not originals.has(key):
		var record: Dictionary = {"id": key, "name": str(control.name), "class": control.get_class(), "rect": control.get_global_rect(), "mouse_filter": control.mouse_filter, "visible": control.visible, "local_position": control.position, "local_size": control.size}
		var button: Button = control as Button
		if button != null:
			var style: StyleBox = button.get_theme_stylebox("normal")
			record["callbacks"] = _callbacks(button)
			record["normal_style_class"] = style.get_class()
			record["content_margins"] = [style.get_content_margin(SIDE_LEFT), style.get_content_margin(SIDE_TOP), style.get_content_margin(SIDE_RIGHT), style.get_content_margin(SIDE_BOTTOM)]
		originals[key] = record
	return originals[key] as Dictionary

func _empty_button(button: Button, record: Dictionary) -> void:
	if button.get_meta("R59_empty_applied", false):
		return
	var blank: StyleBoxEmpty = StyleBoxEmpty.new()
	var margins: Array = record["content_margins"]
	blank.content_margin_left = float(margins[0])
	blank.content_margin_top = float(margins[1])
	blank.content_margin_right = float(margins[2])
	blank.content_margin_bottom = float(margins[3])
	for state: String in ["normal", "hover", "pressed", "hover_pressed", "focus", "disabled"]:
		button.add_theme_stylebox_override(state, blank)
	button.set_meta("R59_empty_applied", true)

func _empty_panel(panel: Panel) -> void:
	if not panel.get_meta("R59_empty_applied", false):
		panel.add_theme_stylebox_override("panel", StyleBoxEmpty.new())
		panel.set_meta("R59_empty_applied", true)

func _full_picture(control: Control, name: String, texture: Texture2D) -> TextureRect:
	var picture: TextureRect = control.get_node_or_null(NodePath(name)) as TextureRect
	if picture == null:
		picture = TextureRect.new()
		picture.name = name
		picture.texture = texture
		picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
		picture.show_behind_parent = true
		control.add_child(picture)
	picture.position = Vector2.ZERO
	picture.size = control.size
	return picture

func _card_picture(control: Control, name: String) -> NinePatchRect:
	var picture: NinePatchRect = control.get_node_or_null(NodePath(name)) as NinePatchRect
	if picture == null:
		picture = NinePatchRect.new()
		picture.name = name
		picture.texture = card_picture
		picture.region_rect = Rect2(9.0, 8.0, 223.0, 224.0)
		picture.patch_margin_left = 48
		picture.patch_margin_top = 48
		picture.patch_margin_right = 48
		picture.patch_margin_bottom = 48
		picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
		picture.show_behind_parent = true
		control.add_child(picture)
	picture.position = Vector2.ZERO
	picture.size = control.size
	return picture

func _refresh_candidate() -> void:
	if not is_instance_valid(m) or m.collection_stage == null or m.collection_layer == null:
		return
	applied_frames += 1
	m.collection_layer.layer = 28
	for node: Node in m.collection_stage.get_children():
		if node.is_queued_for_deletion():
			continue
		var control: Control = node as Control
		if control == null:
			continue
		var record: Dictionary = _remember(control)
		var label: Label = control as Label
		if label != null:
			if label.text.contains("My Critter Book"):
				label.position = Vector2(88.0, 144.0)
				label.size = Vector2(1104.0, 46.0)
				label.autowrap_mode = TextServer.AUTOWRAP_OFF
				label.max_lines_visible = 1
				label.add_theme_font_size_override("font_size", 36)
			elif label.text.contains("Swim close"):
				label.position = Vector2(88.0, 602.0)
				label.size = Vector2(1104.0, 32.0)
				label.autowrap_mode = TextServer.AUTOWRAP_OFF
				label.max_lines_visible = 1
				label.add_theme_font_size_override("font_size", 22)
		var panel: Panel = control as Panel
		if panel != null:
			if String(panel.name).begins_with("CritterCard_"):
				var source_position: Vector2 = record["local_position"]
				panel.position.y = 462.0 if source_position.y > 300.0 else 318.0
				panel.size.y = 132.0
				for child: Node in panel.get_children():
					var text: Label = child as Label
					if text != null and text.text == "Mystery Friend":
						text.position = Vector2(108.0, 32.0)
						text.size = Vector2(220.0, 44.0)
						text.add_theme_font_size_override("font_size", 24)
					elif text != null and text.text == "?":
						text.position = Vector2(20.0, 18.0)
						text.size = Vector2(80.0, 80.0)
						text.add_theme_font_size_override("font_size", 52)
					elif text != null:
						text.position = Vector2(64.0, 74.0)
						text.size = Vector2(264.0, 32.0)
						text.add_theme_font_size_override("font_size", 22)
				if trial_mode == "painted":
					_empty_panel(panel)
					_card_picture(panel, "R59PaintedCard")
			elif trial_mode == "painted" and panel.position == Vector2(34.0, 24.0):
				_empty_panel(panel)
				_full_picture(panel, "R59PaintedPanel", panel_picture)
		var tab_button: Button = control as Button
		if tab_button != null:
			tab_button.position.y = 196.0
		if trial_mode != "painted":
			continue
		if String(control.name).begins_with("CritterBookShellCrest") or String(control.name).begins_with("CritterBookPearl"):
			control.visible = false
		var button: Button = control as Button
		if button != null:
			_empty_button(button, record)
			var selected: bool = button.text.begins_with(String(CollectionSystem.CATEGORY_ICON[m.collection_category]))
			var whole: TextureRect = _full_picture(button, "R59SelectedShell", selected_badge)
			var card: NinePatchRect = _card_picture(button, "R59TabCard")
			whole.visible = selected
			card.visible = true
			var offset: Vector2 = Vector2(0.0, 2.0) if button.is_pressed() else Vector2.ZERO
			var inset: Vector2 = Vector2(4.0, 4.0) if button.has_focus() else Vector2.ZERO
			card.position = offset + inset
			card.size = button.size - inset * 2.0 - Vector2(0.0, offset.y)
			whole.position = Vector2((button.size.x - 42.0) * 0.5, 0.0) + offset
			whole.size = Vector2(42.0, 32.0)
			whole.z_index = 1
			for picture: Control in [whole, card]:
				picture.modulate.a = 0.55 if button.disabled else 1.0

func _candidate_summary() -> Dictionary:
	var result: Dictionary = {"mode": trial_mode, "applied_frames": applied_frames, "nodes": [], "button_invariants": [], "caption_source_scope": "Original caption flags/timer/text never assigned; own book layer28 above caption27, Back29 retained."}
	if not is_instance_valid(m) or m.collection_stage == null:
		return result
	result["book_layer"] = m.collection_layer.layer
	result["caption_visible_flag"] = m.castle_voice_caption.is_visible_in_tree() if m.castle_voice_caption != null else false
	result["caption_timer"] = m.msg_timer
	for node: Node in m.collection_stage.get_children():
		if node.is_queued_for_deletion():
			continue
		var control: Control = node as Control
		if control == null:
			continue
		var rec: Dictionary = _remember(control)
		var row: Dictionary = {"id": control.get_instance_id(), "path": str(control.get_path()), "class": control.get_class(), "rect": str(control.get_global_rect()), "visible": control.visible, "source_id": rec["id"]}
		var label: Label = control as Label
		if label != null:
			row["text"] = label.text
			row["font_size"] = label.get_theme_font_size("font_size")
			row["text_width"] = label.get_theme_font("font").get_string_size(label.text, HORIZONTAL_ALIGNMENT_LEFT, -1, label.get_theme_font_size("font_size")).x
		var panel: Panel = control as Panel
		if panel != null:
			row["panel_style"] = panel.get_theme_stylebox("panel").get_class()
		var button: Button = control as Button
		if button != null:
			var old_pos: Vector2 = rec["local_position"]
			var transform: Transform2D = m.collection_stage.get_global_transform_with_canvas()
			var expected_rect: Rect2 = Rect2(transform * Vector2(old_pos.x, 196.0), (rec["local_size"] as Vector2) * transform.get_scale())
			var invariant: Dictionary = {"id": button.get_instance_id(), "source_rect": str(rec["rect"]), "candidate_rect": str(button.get_global_rect()), "expected_candidate_rect": str(expected_rect), "declared_trial_rect_matches": button.get_global_rect().is_equal_approx(expected_rect), "size_unchanged": button.size == rec["local_size"], "rect_unchanged": button.get_global_rect() == rec["rect"], "callbacks_unchanged": _callbacks(button) == rec["callbacks"], "mouse_filter_unchanged": button.mouse_filter == int(rec["mouse_filter"]), "normal_style": button.get_theme_stylebox("normal").get_class(), "selected": button.text.begins_with(String(CollectionSystem.CATEGORY_ICON[m.collection_category])), "pressed": button.is_pressed(), "focus": button.has_focus(), "disabled": button.disabled}
			(result["button_invariants"] as Array).append(invariant)
		var pictures: Array[Dictionary] = []
		for child: Node in control.get_children():
			if String(child.name).begins_with("R59"):
				var picture: Control = child as Control
				pictures.append({"id": child.get_instance_id(), "class": child.get_class(), "name": str(child.name), "visible": picture.visible, "rect": str(picture.get_global_rect()), "mouse_filter": picture.mouse_filter, "source_texture": _tex(child.get("texture") as Texture2D), "source": (child.get("texture") as AtlasTexture).atlas.resource_path if child.get("texture") is AtlasTexture else child.get("texture").resource_path, "region_rect": str(child.get("region_rect")) if child is NinePatchRect else "full-source uniform-aspect", "patch_margin": 48 if child is NinePatchRect else 0, "show_behind_parent": picture.show_behind_parent})
		row["pictures"] = pictures
		(result["nodes"] as Array).append(row)
	return result

func _snapshot() -> Dictionary:
	var result: Dictionary = super._snapshot()
	result["candidate"] = _candidate_summary()
	return result

func _capture(id: String, role := "CURRENT_CRITTER_BOOK_REUSE_TRIAL") -> void:
	_refresh_candidate()
	await super._capture(id, role)
