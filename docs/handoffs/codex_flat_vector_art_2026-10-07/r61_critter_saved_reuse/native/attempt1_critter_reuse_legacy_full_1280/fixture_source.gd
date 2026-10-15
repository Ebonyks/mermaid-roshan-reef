extends "res://export/flat_vector_r61/legacy_visual.gd"

const INSECT_SOURCE := "res://assets/mg/butterfly.png"
var insect_picture: Texture2D = preload(INSECT_SOURCE)
var case_mode := ""
var observation_metrics: Dictionary = {}

func _run() -> void:
	case_mode = OS.get_environment("R61_CASE_MODE")
	if case_mode not in ["legacy", "fixed", "insect"]:
		quit(1)
		return
	await super._run()

func _remember(control: Control) -> Dictionary:
	var rec: Dictionary = super._remember(control)
	if not rec.has("source_text"):
		if control is Label or control is Button:
			rec["source_text"] = control.get("text")
		if control is Button:
			var pos: Vector2 = rec["local_position"]
			rec["category"] = ""
			for index: int in range(CollectionSystem.CATEGORY_ORDER.size()):
				var category: String = CollectionSystem.CATEGORY_ORDER[index]
				if pos.x == 88.0 + float(index) * 270.0 and String(rec["source_text"]).begins_with(String(CollectionSystem.CATEGORY_ICON[category])):
					rec["category"] = category
		originals[control.get_instance_id()] = rec
	return rec

func _is_source_card(panel: Panel, rec: Dictionary) -> bool:
	var pos: Vector2 = rec["local_position"]
	return panel != null and rec["local_size"] == Vector2(356.0, 192.0) and pos.x in [82.0, 470.0, 858.0] and pos.y in [212.0, 420.0]

func _role(rec: Dictionary) -> String:
	var pos: Vector2 = rec["local_position"]
	if pos == Vector2(22.0, 23.0):
		return "category_or_unknown_status"
	if pos == Vector2(122.0, 30.0):
		return "species_name"
	if pos == Vector2(28.0, 134.0):
		return "habitat"
	return "unbound"

func _tab(category: String) -> Button:
	if not is_instance_valid(m) or m.collection_stage == null:
		return null
	for node: Node in m.collection_stage.get_children():
		var button: Button = node as Button
		if button != null and not button.is_queued_for_deletion() and String(_remember(button).get("category", "")) == category:
			return button
	return null

func _refresh_candidate() -> void:
	if not is_instance_valid(m) or m.collection_stage == null:
		return
	# Capture source constructor roles before the inherited presentation changes them.
	for node: Node in m.collection_stage.get_children():
		var control: Control = node as Control
		if control == null or node.is_queued_for_deletion():
			continue
		_remember(control)
		if control is Panel:
			for child: Node in control.get_children():
				if child is Label and not child.is_queued_for_deletion():
					_remember(child as Label)
	super._refresh_candidate()
	if case_mode == "legacy":
		return
	for node: Node in m.collection_stage.get_children():
		var control: Control = node as Control
		if control == null or node.is_queued_for_deletion():
			continue
		var rec: Dictionary = _remember(control)
		var panel: Panel = control as Panel
		if panel != null and _is_source_card(panel, rec):
			var source_pos: Vector2 = rec["local_position"]
			panel.position.y = 462.0 if source_pos.y > 300.0 else 318.0
			panel.size.y = 132.0
			_empty_panel(panel)
			_card_picture(panel, "R59PaintedCard")
			for child: Node in panel.get_children():
				var label: Label = child as Label
				if label == null:
					continue
				var label_rec: Dictionary = _remember(label)
				var role: String = _role(label_rec)
				if role == "species_name":
					label.add_theme_font_size_override("font_size", 24)
					label.position = Vector2(98.0, 32.0)
					label.size = Vector2(232.0, 44.0)
				elif role == "habitat":
					label.add_theme_font_size_override("font_size", 22)
					label.position = Vector2(64.0, 74.0)
					label.size = Vector2(264.0, 32.0)
				elif role == "category_or_unknown_status":
					label.add_theme_font_size_override("font_size", 52)
					label.position = Vector2(16.0, 18.0)
					label.size = Vector2(76.0, 80.0)
					var target: bool = case_mode == "insect" and m.collection_category == "insect" and label.text == String(CollectionSystem.CATEGORY_ICON["insect"])
					label.visible = not target
					var picture: TextureRect = panel.get_node_or_null("R61InsectCard") as TextureRect
					if target:
						picture = _full_picture(panel, "R61InsectCard", insect_picture)
						picture.show_behind_parent = false
						picture.position = label.position
						picture.size = label.size
					if picture != null:
						picture.visible = target
		var button: Button = control as Button
		if button != null:
			var category: String = String(rec.get("category", ""))
			var badge: TextureRect = button.get_node_or_null("R59SelectedShell") as TextureRect
			if badge != null:
				badge.visible = category == m.collection_category
			if case_mode == "insect" and category == "insect":
				if not button.get_meta("R61_numeric_layout", false):
					var blank := StyleBoxEmpty.new()
					var margins: Array = rec["content_margins"]
					blank.content_margin_left = 112.0
					blank.content_margin_right = 16.0
					blank.content_margin_top = float(margins[1])
					blank.content_margin_bottom = float(margins[3])
					for state: String in ["normal", "hover", "pressed", "hover_pressed", "focus", "disabled"]:
						button.add_theme_stylebox_override(state, blank)
					button.set_meta("R61_numeric_layout", true)
				button.text = String(rec["source_text"]).trim_prefix(String(CollectionSystem.CATEGORY_ICON["insect"])).strip_edges()
				var picture: TextureRect = _full_picture(button, "R61InsectTab", insect_picture)
				var offset := Vector2(0.0, 2.0) if button.is_pressed() else Vector2.ZERO
				var inset := Vector2(4.0, 4.0) if button.has_focus() else Vector2.ZERO
				picture.position = Vector2(44.0, 34.0) + offset + inset
				picture.size = Vector2(64.0, 42.0) - inset * 2.0
				picture.modulate.a = 0.55 if button.disabled else 1.0

func _picture(picture: TextureRect) -> Dictionary:
	if picture == null:
		return {}
	return {"id": picture.get_instance_id(), "path": str(picture.get_path()), "source": picture.texture.resource_path, "texture": _tex(picture.texture), "visible": picture.is_visible_in_tree(), "position": str(picture.position), "size": str(picture.size), "rect": str(picture.get_global_rect()), "mouse_filter": picture.mouse_filter, "modulate": str(picture.modulate), "stretch_mode": picture.stretch_mode}

func _book_rows() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	if not is_instance_valid(m) or m.collection_stage == null:
		return result
	var defs: Array[Dictionary] = []
	for definition: Dictionary in CollectionSystem.DEFS:
		if String(definition["category"]) == m.collection_category:
			defs.append(definition)
	for index: int in range(defs.size()):
		var expected := Vector2(82.0 + float(index % 3) * 388.0, 212.0 + float(index / 3) * 208.0)
		for node: Node in m.collection_stage.get_children():
			var panel: Panel = node as Panel
			if panel == null or panel.is_queued_for_deletion():
				continue
			var rec: Dictionary = _remember(panel)
			if rec["local_position"] != expected or not _is_source_card(panel, rec):
				continue
			var definition: Dictionary = defs[index]
			var labels: Array[Dictionary] = []
			for child: Node in panel.get_children():
				var label: Label = child as Label
				if label == null:
					continue
				var original: Dictionary = _remember(label)
				var font: Font = label.get_theme_font("font")
				labels.append({"role": _role(original), "id": label.get_instance_id(), "source_id": original["id"], "path": str(label.get_path()), "text": label.text, "source_text": original.get("source_text"), "visible": label.is_visible_in_tree(), "source_position": str(original["local_position"]), "position": str(label.position), "size": str(label.size), "rect": str(label.get_global_rect()), "font_size": label.get_theme_font_size("font_size"), "font_class": font.get_class(), "font_path": font.resource_path, "text_width": font.get_string_size(label.text, HORIZONTAL_ALIGNMENT_LEFT, -1, label.get_theme_font_size("font_size")).x})
			result.append({"id": String(definition["id"]), "name": String(definition["name"]), "category": String(definition["category"]), "habitat": String(definition["habitat"]), "caught": bool(m.critter_collection.get(String(definition["id"]), false)), "source_index": index, "panel_id": panel.get_instance_id(), "source_id": rec["id"], "panel_name": str(panel.name), "source_position": str(expected), "position": str(panel.position), "size": str(panel.size), "rect": str(panel.get_global_rect()), "style_class": panel.get_theme_stylebox("panel").get_class(), "labels": labels, "category_picture": _picture(panel.get_node_or_null("R61InsectCard") as TextureRect)})
	return result

func _candidate_summary() -> Dictionary:
	var result: Dictionary = super._candidate_summary()
	result["case_mode"] = case_mode
	result["category_image_source"] = INSECT_SOURCE
	if not is_instance_valid(m) or m.collection_stage == null:
		return result
	for invariant: Dictionary in result["button_invariants"]:
		for node: Node in m.collection_stage.get_children():
			var button: Button = node as Button
			if button == null or button.get_instance_id() != int(invariant["id"]):
				continue
			var rec: Dictionary = _remember(button)
			var badge: TextureRect = button.get_node_or_null("R59SelectedShell") as TextureRect
			invariant["legacy_text_selected"] = invariant["selected"]
			invariant["selected"] = String(rec.get("category", "")) == m.collection_category
			invariant["selection_picture_visible"] = badge.is_visible_in_tree() if badge != null else false
			invariant["source_category"] = rec.get("category", "")
			invariant["source_text"] = rec.get("source_text", "")
			invariant["display_text"] = button.text
			invariant["category_picture"] = _picture(button.get_node_or_null("R61InsectTab") as TextureRect)
	return result

func _exercise() -> void:
	await super._exercise()
	var books := 0
	var collisions := 0
	var flat_cards := 0
	var inputs_ok := true
	var roles_ok := true
	var names_fit := true
	var frames_ok := true
	var pictures_ok := true
	var counts_ok := true
	var selection_ok := true
	var geometry_ok := true
	for state: Dictionary in states:
		var rows: Array = state["card_bindings"]
		if rows.is_empty():
			continue
		books += 1
		var snapshot: Dictionary = state["snapshot"]
		var candidate: Dictionary = snapshot["candidate"]
		for invariant: Dictionary in candidate["button_invariants"]:
			inputs_ok = inputs_ok and bool(invariant["declared_trial_rect_matches"]) and bool(invariant["callbacks_unchanged"]) and bool(invariant["size_unchanged"]) and bool(invariant["mouse_filter_unchanged"])
			selection_ok = selection_ok and bool(invariant["selected"]) == bool(invariant["selection_picture_visible"])
			var target: bool = case_mode == "insect" and String(invariant["source_category"]) == "insect"
			var expected: String = String(invariant["source_text"])
			if target:
				expected = expected.trim_prefix(String(CollectionSystem.CATEGORY_ICON["insect"])).strip_edges()
			counts_ok = counts_ok and String(invariant["display_text"]) == expected
			var picture: Dictionary = invariant["category_picture"]
			pictures_ok = pictures_ok and (bool(picture.get("visible", false)) == target)
			if target:
				pictures_ok = pictures_ok and String(picture.get("source", "")) == INSECT_SOURCE and int(picture["mouse_filter"]) == Control.MOUSE_FILTER_IGNORE
		for row: Dictionary in rows:
			var labels: Dictionary = {}
			for label: Dictionary in row["labels"]:
				labels[String(label["role"])] = label
				roles_ok = roles_ok and label["id"] == label["source_id"] and String(label["text"]) == String(label["source_text"])
			var name: Dictionary = labels.get("species_name", {})
			var habitat: Dictionary = labels.get("habitat", {})
			var icon: Dictionary = labels.get("category_or_unknown_status", {})
			if bool(row["caught"]) and name.get("position") == habitat.get("position"):
				collisions += 1
			if String(row["style_class"]) != "StyleBoxEmpty":
				flat_cards += 1
			roles_ok = roles_ok and name.get("position") == "(98.0, 32.0)" and habitat.get("position") == "(64.0, 74.0)" and icon.get("position") == "(16.0, 18.0)"
			names_fit = names_fit and float(name.get("text_width", 9999.0)) <= 232.0
			frames_ok = frames_ok and String(row["style_class"]) == "StyleBoxEmpty"
			geometry_ok = geometry_ok and row["size"] == "(356.0, 132.0)"
			var target: bool = case_mode == "insect" and String(row["category"]) == "insect" and bool(row["caught"])
			var picture: Dictionary = row["category_picture"]
			pictures_ok = pictures_ok and bool(icon.get("visible", false)) == (not target) and bool(picture.get("visible", false)) == target
			if target:
				pictures_ok = pictures_ok and String(picture.get("source", "")) == INSECT_SOURCE and int(picture["mouse_filter"]) == Control.MOUSE_FILTER_IGNORE
	observation_metrics = {"books": books, "caught_role_collisions": collisions, "source_flat_card_observations": flat_cards, "inputs_ok": inputs_ok, "roles_ok": roles_ok, "names_fit": names_fit, "frames_ok": frames_ok, "pictures_ok": pictures_ok, "counts_ok": counts_ok, "selection_ok": selection_ok, "geometry_ok": geometry_ok}
	if case_mode == "legacy":
		_check("legacy negative caught-role collision observed", collisions > 0)
		return
	_check("twenty original source-bound book snapshots", books == 20)
	_check("declared native tab rect callback size mouse owner invariants", inputs_ok)
	_check("source label identities text and corrected structural roles", roles_ok and collisions == 0)
	_check("all original names fit232px at font24", names_fit)
	_check("all original card backgrounds replaced in ignored candidate", frames_ok)
	_check("source insect pictures and original status glyph visibility", pictures_ok)
	_check("native tab count text and source-bound selection preserved", counts_ok and selection_ok)
	_check("all source-bound cards use declared356x132 bounds", geometry_ok)
