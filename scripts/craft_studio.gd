class_name CraftStudio
extends RefCounted
# Picture-first craft studio. All state remains on main; this satellite owns
# only layout and interaction logic.

const PALETTE := [
	Color(0.92, 0.26, 0.30), Color(1.0, 0.60, 0.20),
	Color(1.0, 0.85, 0.25), Color(0.35, 0.80, 0.40),
	Color(0.30, 0.80, 0.90), Color(0.30, 0.55, 1.0),
	Color(0.60, 0.40, 0.90), Color(0.95, 0.50, 0.80)]

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _craft_build_preview() -> void:
	if m.craft_fishbox == null:
		return
	for child: Node in m.craft_fishbox.get_children():
		child.queue_free()
	var layers: Array = m.CREATURE_LAYERS.get(m.craft_kind, m.CREATURE_LAYERS["fish"])
	var order := [String(layers[1]), String(layers[0]), String(layers[2])]
	var roles := ["body", "accent", "line"]
	var colors := [m.craft_body, Color(m.craft_fins.r, m.craft_fins.g, m.craft_fins.b, 1.0), Color.WHITE]
	var rainbows := [m.craft_body_rb, m.craft_fins_rb, false]
	for i in range(3):
		var texture_rect := TextureRect.new()
		texture_rect.texture = load("res://assets/mg/" + order[i] + ".png")
		texture_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		texture_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		texture_rect.size = m.craft_fishbox.size
		texture_rect.modulate = colors[i]
		texture_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
		texture_rect.set_meta("role", roles[i])
		m.craft_fishbox.add_child(texture_rect)
		if roles[i] != "line":
			m._layer_fx(texture_rect, roles[i], colors[i], rainbows[i], m.craft_kind)

func _open_craft_studio() -> void:
	if m.craft_layer != null:
		return
	m.craft_kind = "fish"
	m.craft_part = "body"
	m.craft_body = Color(0.4, 0.7, 1.0)
	m.craft_fins = Color(1.0, 0.6, 0.2)
	m.craft_body_rb = false
	m.craft_fins_rb = false
	m.craft_c3 = Color(0, 0, 0, 0)
	m.craft_layer = CanvasLayer.new()
	m.craft_layer.layer = 18
	m.add_child(m.craft_layer)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.craft_layer.add_child(root)
	var bg := ColorRect.new()
	bg.color = Color(0.12, 0.34, 0.48, 0.98)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(bg)
	var stage := StorybookUI.add_stage(root, m.get_viewport().get_visible_rect().size)
	m.craft_layer.set_meta("stage", stage)

	var title := Label.new()
	title.name = "CraftTitle"
	title.text = "✦  COLOR A FRIEND"
	title.position = Vector2(34, 20)
	StorybookUI.style_label(title, 38, Color.WHITE, 6)
	stage.add_child(title)
	title.add_to_group("craft_top")
	m.craft_pearl_lbl = Label.new()
	m.craft_pearl_lbl.text = "◉  %d" % m.pearl_count
	m.craft_pearl_lbl.position = Vector2(42, 78)
	StorybookUI.style_label(m.craft_pearl_lbl, 32, StorybookUI.GOLD, 5)
	stage.add_child(m.craft_pearl_lbl)
	m.craft_pearl_lbl.add_to_group("craft_top")

	var back := Button.new()
	back.name = "CraftBackButton"
	StorybookUI.style_back_button(back, "Back to the castle")
	back.position = Vector2(1140, 18)
	back.pressed.connect(_close_craft)
	stage.add_child(back)
	back.add_to_group("craft_top")

	var kinds := [["fish", "◉\nFISH", 0], ["cat", "♧\nKITTY", 5], ["bird", "♢\nBIRDIE", 8]]
	var kind_buttons: Array[Dictionary] = []
	for i in range(kinds.size()):
		var kind_id: String = String(kinds[i][0])
		var kind_name: String = String(kinds[i][1])
		var price: int = int(kinds[i][2])
		var locked: bool = price > 0 and not bool(m.craft_unlocks.get(kind_id, false))
		var button := Button.new()
		button.name = "CraftKind_" + kind_id
		var unlocked_text := kind_name
		button.text = ("▣  " + "◉".repeat(mini(price, 3)) + "\n" + kind_name) if locked else unlocked_text
		button.position = Vector2(620.0 + float(i) * 164.0, 18.0)
		button.custom_minimum_size = Vector2(150, 112)
		button.size = Vector2(150, 112)
		StorybookUI.style_button(button, "locked" if locked else "secondary", 24, 28)
		button.set_meta("locked", locked)
		button.set_meta("price", price)
		button.set_meta("unlocked_text", unlocked_text)
		button.pressed.connect(_craft_pick_kind.bind(kind_id, kind_name.replace("\n", " "), price, button))
		stage.add_child(button)
		button.add_to_group("craft_top")
		kind_buttons.append({"button": button, "id": kind_id})
	m.craft_layer.set_meta("kind_buttons", kind_buttons)

	var preview_panel := StorybookUI.add_panel(stage, Rect2(80, 145, 650, 390), StorybookUI.LAVENDER, Color(0.95, 0.97, 1.0, 0.98), 44)
	preview_panel.name = "CraftPreviewPanel"
	m.craft_fishbox = Control.new()
	m.craft_fishbox.size = Vector2(590, 350)
	m.craft_fishbox.position = Vector2(30, 18)
	preview_panel.add_child(m.craft_fishbox)
	_craft_build_preview()

	var part_specs := [["body", "●   BODY"], ["accent", "◒   FINS"], ["third", "✦   DETAIL"]]
	var part_buttons: Array[Dictionary] = []
	for i in range(part_specs.size()):
		var part_id: String = String(part_specs[i][0])
		var part_button := Button.new()
		part_button.name = "CraftPart_" + part_id
		part_button.text = String(part_specs[i][1])
		part_button.position = Vector2(770, 160.0 + float(i) * 122.0)
		part_button.custom_minimum_size = Vector2(290, 110)
		part_button.size = Vector2(290, 110)
		StorybookUI.style_button(part_button, "secondary", 28, 28)
		part_button.pressed.connect(_craft_pick_part.bind(part_id))
		stage.add_child(part_button)
		part_buttons.append({"button": part_button, "id": part_id})
	m.craft_layer.set_meta("part_buttons", part_buttons)

	m.craft_status = Label.new()
	m.craft_status.position = Vector2(1080, 390)
	m.craft_status.size = Vector2(175, 150)
	m.craft_status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	m.craft_status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	StorybookUI.style_label(m.craft_status, 21, Color.WHITE, 5)
	stage.add_child(m.craft_status)
	var done := Button.new()
	done.name = "CraftFinishButton"
	done.text = "≋◉✦\nSWIM!"
	done.position = Vector2(1080, 205)
	done.custom_minimum_size = Vector2(170, 160)
	done.size = Vector2(170, 160)
	StorybookUI.style_button(done, "primary", 30, 44)
	done.pressed.connect(_craft_done)
	stage.add_child(done)

	_craft_rebuild_palette()
	_craft_refresh_controls()
	m._hook_button_taps(stage)

func _craft_pick_part(part: String) -> void:
	m.craft_part = part
	_craft_rebuild_palette()
	_craft_refresh_controls()

func _craft_rebuild_palette() -> void:
	if m.craft_layer == null:
		return
	var stage: Control = m.craft_layer.get_meta("stage", null)
	if stage == null:
		return
	for old: Node in stage.get_tree().get_nodes_in_group("craft_palette_button"):
		if old.is_ancestor_of(stage) or stage.is_ancestor_of(old):
			old.queue_free()
	for i in range(PALETTE.size()):
		var color: Color = PALETTE[i]
		var swatch := Button.new()
		swatch.name = "CraftSwatch_%d" % i
		swatch.position = Vector2(22.0 + float(i) * 122.0, 584)
		swatch.custom_minimum_size = Vector2(112, 112)
		swatch.size = Vector2(112, 112)
		_style_swatch(swatch, color, _craft_color_matches(color))
		swatch.pressed.connect(_craft_set.bind(m.craft_part, color, false))
		stage.add_child(swatch)
		swatch.add_to_group("craft_palette_button")
	if m.craft_part != "third":
		var rainbow := Button.new()
		rainbow.name = "CraftRainbowSwatch"
		rainbow.position = Vector2(998, 584)
		rainbow.custom_minimum_size = Vector2(112, 112)
		rainbow.size = Vector2(112, 112)
		StorybookUI.style_button(rainbow, "selected" if _craft_rainbow_selected() else "secondary", 24, 30)
		rainbow.text = "🌈"
		rainbow.pressed.connect(_craft_set.bind(m.craft_part, Color.WHITE, true))
		stage.add_child(rainbow)
		rainbow.add_to_group("craft_palette_button")

func _style_swatch(button: Button, color: Color, selected: bool) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = color
	normal.border_color = StorybookUI.GOLD if selected else Color(1.0, 1.0, 1.0, 0.86)
	normal.set_border_width_all(8 if selected else 4)
	normal.set_corner_radius_all(34)
	normal.shadow_color = Color(0.08, 0.06, 0.22, 0.30)
	normal.shadow_size = 7
	normal.shadow_offset = Vector2(0, 4)
	var pressed: StyleBoxFlat = normal.duplicate()
	pressed.bg_color = color.darkened(0.12)
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", normal)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("focus", normal)
	button.set_meta("touch_target", true)
	button.set_meta("selected", selected)

func _craft_color_matches(color: Color) -> bool:
	var current := m.craft_body if m.craft_part == "body" else (m.craft_fins if m.craft_part == "accent" else m.craft_c3)
	return not _craft_rainbow_selected() and current.is_equal_approx(color)

func _craft_rainbow_selected() -> bool:
	return (m.craft_part == "body" and m.craft_body_rb) or (m.craft_part == "accent" and m.craft_fins_rb)

func _craft_refresh_controls() -> void:
	if m.craft_layer == null:
		return
	for entry: Dictionary in m.craft_layer.get_meta("kind_buttons", []):
		var button: Button = entry["button"]
		var id: String = String(entry["id"])
		StorybookUI.set_selected(button, id == m.craft_kind, bool(button.get_meta("locked", false)))
	for entry: Dictionary in m.craft_layer.get_meta("part_buttons", []):
		var button: Button = entry["button"]
		StorybookUI.set_selected(button, String(entry["id"]) == m.craft_part)

func _craft_pick_kind(kind: String, kind_name: String, price: int, button: Button) -> void:
	if price > 0 and not bool(m.craft_unlocks.get(kind, false)):
		if m.pearl_count < price:
			m.craft_status.text = "▣  ◉◉◉\nExplore for more pearls"
			m._say("roshan", "talk")
			if m.chime != null:
				m.chime.pitch_scale = 0.7
				m.chime.play()
			return
		m.pearl_count -= price
		m.craft_unlocks[kind] = true
		m._write_save()
		m._update_hud()
		if m.chime != null:
			m.chime.pitch_scale = 1.5
			m.chime.play()
		button.set_meta("locked", false)
		button.text = String(button.get_meta("unlocked_text", button.text))
		m.craft_pearl_lbl.text = "◉  %d" % m.pearl_count
		m.craft_status.text = "✦  " + kind_name + "!"
	m.craft_kind = kind
	_craft_build_preview()
	_craft_refresh_controls()

func _craft_set(part: String, color: Color, rainbow: bool = false) -> void:
	if part == "body":
		m.craft_body = color
		m.craft_body_rb = rainbow
	elif part == "third":
		m.craft_c3 = color
	else:
		m.craft_fins = color
		m.craft_fins_rb = rainbow
	_craft_build_preview()
	_craft_rebuild_palette()
	_craft_refresh_controls()

func _craft_done() -> void:
	if m.craft_layer == null or bool(m.get_meta("craft_closing", false)):
		return
	m.set_meta("craft_closing", true)
	m.stickers["_c_" + m.craft_kind] = true
	if bool(m.stickers.get("_c_fish", false)) and bool(m.stickers.get("_c_cat", false)) and bool(m.stickers.get("_c_bird", false)):
		m.award_sticker("artist")
	var fishy: bool = m.craft_kind == "fish"
	var message: String
	if fishy:
		m.custom_fish.append([m.craft_body.r, m.craft_body.g, m.craft_body.b, m.craft_fins.r, m.craft_fins.g, m.craft_fins.b, 1 if m.craft_body_rb else 0, 1 if m.craft_fins_rb else 0])
		m._spawn_crafted_fish()
		message = "Swim away, little fish! Find me in the ocean!"
	else:
		var third_color: Color = m.craft_c3
		if third_color.a <= 0.0 and m.CRAFT_RIGGED.has(m.craft_kind):
			third_color = (m.CRAFT_RIGGED[m.craft_kind] as Array)[2]
		m.custom_friends.append([m.craft_kind, m.craft_body.r, m.craft_body.g, m.craft_body.b, m.craft_fins.r, m.craft_fins.g, m.craft_fins.b, 1 if m.craft_body_rb else 0, 1 if m.craft_fins_rb else 0, third_color.r, third_color.g, third_color.b])
		message = "Off to the courtyard! Find me when you visit!"
	m._write_save()
	if m.chime != null:
		m.chime.pitch_scale = 1.3
		m.chime.play()
	m._say("roshan", "win", 0.5)
	for top_node: Node in m.get_tree().get_nodes_in_group("craft_top"):
		if top_node is CanvasItem:
			(top_node as CanvasItem).visible = false
	if m.craft_fishbox != null:
		var box := m.craft_fishbox
		var banner := Label.new()
		banner.text = "✦  " + message
		banner.position = Vector2(150, 26)
		banner.size = Vector2(900, 110)
		banner.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		StorybookUI.style_label(banner, 38, StorybookUI.GOLD, 7)
		box.get_parent().get_parent().add_child(banner)
		box.pivot_offset = box.size * 0.5
		var tween := box.create_tween()
		tween.tween_property(box, "scale", Vector2(1.25, 1.25), 0.4).set_trans(Tween.TRANS_BACK)
		tween.tween_interval(0.5)
		tween.parallel().tween_property(box, "position:x", 1500.0, 1.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		tween.parallel().tween_property(box, "scale", Vector2(0.5, 0.5), 1.0)
	m.get_tree().create_timer(2.6).timeout.connect(_close_craft)

func _close_craft() -> void:
	m.set_meta("craft_closing", false)
	if m.craft_layer != null and is_instance_valid(m.craft_layer):
		m.craft_layer.queue_free()
	m.craft_status = null
	m.craft_pearl_lbl = null
	m.craft_layer = null
	m.craft_fishbox = null
	m.mg_cool = 10.0
