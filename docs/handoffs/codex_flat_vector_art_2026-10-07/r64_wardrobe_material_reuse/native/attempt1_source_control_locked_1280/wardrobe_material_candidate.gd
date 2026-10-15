extends "res://scripts/wardrobe_ui.gd"
# R64 ignored material candidate. Production source and every source pixel stay unchanged.
const PANEL_ART: Texture2D = preload("res://assets/fashion/skin_engine_v2/ui/wardrobe_panel.png")
const CARD_ART: Texture2D = preload("res://assets/fashion/skin_engine_v2/ui/wardrobe_card.png")
var r64_shell_binding: Dictionary = {}
var r64_open_count: int = 0
var r64_refresh_count: int = 0

func _init(main: ReefMain) -> void:
	super(main)

func _card_style(state: String, selected: bool = false) -> StyleBoxTexture:
	var painted := StyleBoxTexture.new()
	painted.texture = CARD_ART
	painted.texture_margin_left = 36
	painted.texture_margin_right = 36
	painted.texture_margin_top = 36
	painted.texture_margin_bottom = 36
	painted.content_margin_left = 12
	painted.content_margin_right = 12
	painted.content_margin_top = 12
	painted.content_margin_bottom = 12
	painted.modulate_color = Color(1.0, 0.86, 0.64) if state in ["pressed", "focus", "hover_pressed"] or (state == "normal" and selected) else (Color(1.0, 0.95, 0.83) if state == "hover" else Color.WHITE)
	return painted

func _wardrobe_refresh() -> void:
	super._wardrobe_refresh()
	_paint_picker_buttons()

func _paint_picker_buttons() -> void:
	if m.wardrobe_layer == null or not m.wd.has("btns"):
		return
	r64_refresh_count += 1
	var stage: Control = m.wd.get("stage") as Control
	if stage == null or stage.find_child("WardrobeLook_classic", true, false) == null:
		return
	for name: String in ["WardrobeLook_classic", "WardrobeLook_fairy", "WardrobeLook_huluu", "WardrobeFinishButton", "FashionWardrobeButton"]:
		var button: Button = stage.find_child(name, true, false) as Button
		if button == null:
			continue
		for state: String in ["normal", "hover", "pressed", "hover_pressed", "focus", "disabled"]:
			button.add_theme_stylebox_override(state, _card_style(state, bool(button.get_meta("selected", false))))

func _open_wardrobe() -> void:
	super._open_wardrobe()
	var stage: Control = m.wd.get("stage") as Control
	if stage == null or stage.find_child("WardrobeLook_classic", true, false) == null:
		return
	r64_open_count += 1
	var bindings: Array[Dictionary] = []
	for child: Node in stage.get_children():
		if child is Panel:
			var panel: Panel = child as Panel
			var texture: Texture2D = null
			var role: String = ""
			if panel.position == Vector2(28, 18) and panel.size == Vector2(1224, 684):
				texture = PANEL_ART
				role = "parent_panel"
			elif panel.position == Vector2(110, 110) and panel.size == Vector2(470, 560):
				texture = CARD_ART
				role = "preview_frame"
			if texture != null:
				var old: StyleBox = panel.get_theme_stylebox("panel")
				var replacement := StyleBoxTexture.new()
				replacement.texture = texture
				if role == "preview_frame":
					replacement = _card_style("normal")
				panel.add_theme_stylebox_override("panel", replacement)
				bindings.append({"role": role, "node_id": panel.get_instance_id(), "old_style": old.get_class(), "new_style": replacement.get_class(), "texture": texture.resource_path, "position": str(panel.position), "size": str(panel.size)})
	var removed: Array[Dictionary] = []
	for name: String in ["WardrobeShellCrest", "WardrobePearlTL", "WardrobePearlTR", "WardrobePearlBL", "WardrobePearlBR"]:
		var ornament: Node = stage.get_node_or_null(NodePath(name))
		if ornament != null:
			removed.append({"name": name, "node_id": ornament.get_instance_id(), "class": ornament.get_class()})
			stage.remove_child(ornament)
			ornament.queue_free()
	var heading: Dictionary = {}
	for child: Node in stage.get_children():
		if child is Label and (child as Label).text == "Pick your look!":
			var title: Label = child as Label
			heading = {"node_id": title.get_instance_id(), "text": title.text, "old_position": str(title.position), "old_size": str(title.size)}
			title.position = Vector2(165, 22)
			title.size = Vector2(430, 64)
			title.autowrap_mode = TextServer.AUTOWRAP_OFF
			title.max_lines_visible = 1
			title.clip_text = true
			title.add_theme_font_size_override("font_size", 42)
			heading.merge({"position": str(title.position), "size": str(title.size), "font_size": title.get_theme_font_size("font_size")})
	_paint_picker_buttons()
	r64_shell_binding = {"panels": bindings, "removed_ornaments": removed, "heading": heading, "open_count": r64_open_count, "refresh_count": r64_refresh_count}
