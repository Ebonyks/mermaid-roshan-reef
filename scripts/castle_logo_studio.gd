class_name CastleLogoStudio
extends RefCounted
# Picture-first castle-logo maker. Persistent and temporary state stays on
# ReefMain; this satellite owns the full-screen layout and emblem rendering.

const COLOR_CHOICES: Array[Dictionary] = [
	{"id": "pink", "name": "Pink", "color": Color(1.0, 0.48, 0.72)},
	{"id": "gold", "name": "Sunny gold", "color": Color(1.0, 0.79, 0.28)},
	{"id": "mint", "name": "Mint", "color": Color(0.43, 0.90, 0.68)},
	{"id": "ocean", "name": "Ocean blue", "color": Color(0.30, 0.72, 1.0)},
	{"id": "purple", "name": "Purple", "color": Color(0.66, 0.47, 0.95)},
	{"id": "rainbow", "name": "Rainbow", "color": Color.WHITE},
]
const SYMBOL_CHOICES: Array[Dictionary] = [
	{"id": "rainbow", "name": "Rainbow", "icon": "🌈"},
	{"id": "shell", "name": "Shell", "icon": "🐚"},
	{"id": "kitty", "name": "Kitty", "icon": "🐱"},
	{"id": "dog", "name": "Puppy", "icon": "🐶"},
	{"id": "star", "name": "Star", "icon": "⭐"},
	{"id": "heart", "name": "Heart", "icon": "💖"},
	{"id": "crown", "name": "Crown", "icon": "👑"},
	{"id": "butterfly", "name": "Butterfly", "icon": "🦋"},
]
const RAINBOW_COLORS: Array[Color] = [
	Color(1.0, 0.35, 0.42), Color(1.0, 0.67, 0.25),
	Color(1.0, 0.87, 0.30), Color(0.38, 0.86, 0.54),
	Color(0.30, 0.73, 1.0), Color(0.68, 0.46, 0.94),
]

class LogoPreview extends Control:
	var color_id := "rainbow"
	var symbol_id := "rainbow"
	var symbol_label: Label

	func _init() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		symbol_label = Label.new()
		symbol_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		symbol_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		symbol_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		add_child(symbol_label)
		resized.connect(_layout_symbol)

	func configure(next_color_id: String, next_symbol_id: String) -> void:
		color_id = next_color_id
		symbol_id = next_symbol_id
		set_meta("color_id", color_id)
		set_meta("symbol_id", symbol_id)
		symbol_label.text = CastleLogoStudio.symbol_icon(symbol_id)
		_layout_symbol()
		queue_redraw()

	func _layout_symbol() -> void:
		if symbol_label == null:
			return
		symbol_label.position = Vector2(0.0, size.y * 0.10)
		symbol_label.size = Vector2(size.x, size.y * 0.72)
		var font_size: int = maxi(34, int(minf(size.x, size.y) * 0.46))
		StorybookUI.style_label(symbol_label, font_size, Color.WHITE,
			maxi(3, int(float(font_size) / 12.0)))

	func _draw() -> void:
		var points := PackedVector2Array([
			Vector2(size.x * 0.16, size.y * 0.08),
			Vector2(size.x * 0.84, size.y * 0.08),
			Vector2(size.x * 0.92, size.y * 0.47),
			Vector2(size.x * 0.82, size.y * 0.72),
			Vector2(size.x * 0.50, size.y * 0.94),
			Vector2(size.x * 0.18, size.y * 0.72),
			Vector2(size.x * 0.08, size.y * 0.47),
		])
		var shield_center := Vector2(size.x * 0.50, size.y * 0.50)
		if color_id == "rainbow":
			for i in range(points.size()):
				var triangle := PackedVector2Array([
					shield_center, points[i],
					points[(i + 1) % points.size()]])
				draw_colored_polygon(
					triangle, CastleLogoStudio.RAINBOW_COLORS[
						i % CastleLogoStudio.RAINBOW_COLORS.size()])
		else:
			draw_colored_polygon(points,
				CastleLogoStudio.color_value(color_id))
		var outline := points.duplicate()
		outline.append(points[0])
		draw_polyline(outline, StorybookUI.PURPLE_DEEP,
			maxf(5.0, minf(size.x, size.y) * 0.045), true)
		var inner_outline := PackedVector2Array()
		for point: Vector2 in points:
			inner_outline.append(shield_center.lerp(point, 0.87))
		inner_outline.append(inner_outline[0])
		draw_polyline(inner_outline, Color(1.0, 0.94, 0.72, 0.92),
			maxf(3.0, minf(size.x, size.y) * 0.022), true)

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

static func has_color(color_id: String) -> bool:
	for choice: Dictionary in COLOR_CHOICES:
		if String(choice["id"]) == color_id:
			return true
	return false

static func has_symbol(symbol_id: String) -> bool:
	for choice: Dictionary in SYMBOL_CHOICES:
		if String(choice["id"]) == symbol_id:
			return true
	return false

static func normalise_color(color_id: String) -> String:
	return color_id if has_color(color_id) else "rainbow"

static func normalise_symbol(symbol_id: String) -> String:
	return symbol_id if has_symbol(symbol_id) else "rainbow"

static func color_value(color_id: String) -> Color:
	for choice: Dictionary in COLOR_CHOICES:
		if String(choice["id"]) == color_id:
			return Color(choice["color"])
	return Color.WHITE

static func symbol_icon(symbol_id: String) -> String:
	for choice: Dictionary in SYMBOL_CHOICES:
		if String(choice["id"]) == symbol_id:
			return String(choice["icon"])
	return "🌈"

func open() -> void:
	if m.castle_logo_layer != null:
		return
	m._set_world_controls_enabled(false, "castle_logo")
	m.castle_logo_color = normalise_color(m.castle_logo_color)
	m.castle_logo_symbol = normalise_symbol(m.castle_logo_symbol)
	m.castle_logo_layer = CanvasLayer.new()
	m.castle_logo_layer.name = "CastleLogoStudioLayer"
	m.castle_logo_layer.layer = 18
	m.castle_logo_layer.set_meta("original_color", m.castle_logo_color)
	m.castle_logo_layer.set_meta("original_symbol", m.castle_logo_symbol)
	m.add_child(m.castle_logo_layer)

	var root := Control.new()
	root.name = "CastleLogoStudio"
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	m.castle_logo_layer.add_child(root)
	var bg := ColorRect.new()
	bg.color = Color(0.10, 0.28, 0.43, 0.985)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(bg)
	var stage := StorybookUI.add_stage(
		root, m.get_viewport().get_visible_rect().size)
	m.castle_logo_layer.set_meta("stage", stage)

	var title := Label.new()
	title.name = "CastleLogoTitle"
	title.text = "🏰  CASTLE LOGO"
	title.position = Vector2(32.0, 18.0)
	title.size = Vector2(570.0, 82.0)
	StorybookUI.style_label(title, 40, Color.WHITE, 6)
	stage.add_child(title)

	var back := Button.new()
	back.name = "CastleLogoBackButton"
	StorybookUI.style_back_button(back, "Back to the craft room")
	back.position = Vector2(1140.0, 18.0)
	back.pressed.connect(close.bind(false))
	stage.add_child(back)

	var preview_rect := Rect2(55.0, 125.0, 400.0, 405.0)
	var preview_panel := StorybookUI.add_panel(stage, preview_rect,
		StorybookUI.PURPLE, Color(0.95, 0.98, 1.0, 0.99), 44)
	preview_panel.name = "CastleLogoPreviewPanel"
	StorybookUI.adorn_panel(stage, preview_rect, "CastleLogo")
	m.castle_logo_preview = _make_preview(
		"CastleLogoPreview", Vector2(300.0, 325.0))
	m.castle_logo_preview.position = Vector2(50.0, 42.0)
	preview_panel.add_child(m.castle_logo_preview)

	var picture_cue := Label.new()
	picture_cue.text = "☝  ✨"
	picture_cue.position = Vector2(505.0, 82.0)
	picture_cue.size = Vector2(180.0, 70.0)
	StorybookUI.style_label(picture_cue, 48, StorybookUI.GOLD, 4)
	stage.add_child(picture_cue)
	_pulse_pointer(picture_cue)

	var symbol_buttons: Array[Dictionary] = []
	for i in range(SYMBOL_CHOICES.size()):
		var choice: Dictionary = SYMBOL_CHOICES[i]
		var symbol_id: String = String(choice["id"])
		var button := Button.new()
		button.name = "CastleLogoSymbol_" + symbol_id
		button.position = Vector2(
			500.0 + float(i % 4) * 176.0,
			135.0 + float(i / 4) * 174.0)
		StorybookUI.style_icon_button(button, String(choice["icon"]),
			"secondary", Vector2(158.0, 150.0), String(choice["name"]))
		button.pressed.connect(_pick_symbol.bind(symbol_id))
		stage.add_child(button)
		symbol_buttons.append({"button": button, "id": symbol_id})
	m.castle_logo_layer.set_meta("symbol_buttons", symbol_buttons)

	var paint_cue := Label.new()
	paint_cue.text = "☝  🎨"
	paint_cue.position = Vector2(42.0, 526.0)
	paint_cue.size = Vector2(180.0, 62.0)
	StorybookUI.style_label(paint_cue, 44, StorybookUI.GOLD, 4)
	stage.add_child(paint_cue)
	_pulse_pointer(paint_cue)

	var color_buttons: Array[Dictionary] = []
	for i in range(COLOR_CHOICES.size()):
		var choice: Dictionary = COLOR_CHOICES[i]
		var color_id: String = String(choice["id"])
		var swatch := Button.new()
		swatch.name = "CastleLogoColor_" + color_id
		swatch.position = Vector2(40.0 + float(i) * 126.0, 585.0)
		swatch.custom_minimum_size = Vector2(112.0, 112.0)
		swatch.size = Vector2(112.0, 112.0)
		swatch.tooltip_text = String(choice["name"])
		_style_color_button(swatch, color_id,
			color_id == m.castle_logo_color)
		swatch.pressed.connect(_pick_color.bind(color_id))
		stage.add_child(swatch)
		color_buttons.append({"button": swatch, "id": color_id})
	m.castle_logo_layer.set_meta("color_buttons", color_buttons)

	var done := Button.new()
	done.name = "CastleLogoFinishButton"
	done.position = Vector2(985.0, 535.0)
	StorybookUI.style_icon_button(done, "💖\n✓", "primary",
		Vector2(240.0, 162.0), "Keep this castle logo")
	done.pressed.connect(finish)
	stage.add_child(done)

	var status := Label.new()
	status.name = "CastleLogoStatus"
	status.position = Vector2(780.0, 538.0)
	status.size = Vector2(190.0, 150.0)
	status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_label(status, 27, Color.WHITE, 5)
	stage.add_child(status)
	m.castle_logo_layer.set_meta("status", status)

	_refresh_controls()
	m._hook_button_taps(stage)
	m._say("roshan", "talk", 0.0)

func _make_preview(preview_name: String, preview_size: Vector2) -> LogoPreview:
	var preview := LogoPreview.new()
	preview.name = preview_name
	preview.custom_minimum_size = preview_size
	preview.size = preview_size
	preview.configure(m.castle_logo_color, m.castle_logo_symbol)
	return preview

func _pulse_pointer(pointer: Label) -> void:
	pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var start_y: float = pointer.position.y
	var pulse := pointer.create_tween().set_loops()
	pulse.tween_property(pointer, "position:y", start_y + 10.0,
		0.55).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	pulse.tween_property(pointer, "position:y", start_y,
		0.55).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)

func _pick_symbol(symbol_id: String) -> void:
	m.castle_logo_symbol = normalise_symbol(symbol_id)
	_refresh_controls()
	_set_status("✨  " + symbol_icon(m.castle_logo_symbol))

func _pick_color(color_id: String) -> void:
	m.castle_logo_color = normalise_color(color_id)
	_refresh_controls()
	_set_status("🎨  ✨")

func _set_status(message: String) -> void:
	if m.castle_logo_layer == null:
		return
	var status: Label = m.castle_logo_layer.get_meta("status", null) as Label
	if status != null:
		status.text = message

func _refresh_controls() -> void:
	if m.castle_logo_layer == null:
		return
	for entry: Dictionary in m.castle_logo_layer.get_meta(
			"symbol_buttons", []):
		var button: Button = entry["button"] as Button
		StorybookUI.set_selected(button,
			String(entry["id"]) == m.castle_logo_symbol)
	for entry: Dictionary in m.castle_logo_layer.get_meta(
			"color_buttons", []):
		var button: Button = entry["button"] as Button
		var color_id: String = String(entry["id"])
		_style_color_button(button, color_id,
			color_id == m.castle_logo_color)
	var preview: LogoPreview = m.castle_logo_preview as LogoPreview
	if preview != null:
		preview.configure(m.castle_logo_color, m.castle_logo_symbol)

func _style_color_button(button: Button, color_id: String,
		selected: bool) -> void:
	if color_id == "rainbow":
		StorybookUI.style_icon_button(button, "🌈",
			"selected" if selected else "secondary",
			Vector2(112.0, 112.0), "Rainbow")
		button.set_meta("selected", selected)
		button.set_meta("color_id", color_id)
		return
	var color: Color = color_value(color_id)
	var normal := StyleBoxFlat.new()
	normal.bg_color = color
	normal.border_color = StorybookUI.GOLD if selected \
		else Color(1.0, 1.0, 1.0, 0.92)
	normal.set_border_width_all(9 if selected else 5)
	normal.set_corner_radius_all(42)
	normal.shadow_color = Color(0.08, 0.06, 0.22, 0.34)
	normal.shadow_size = 7
	normal.shadow_offset = Vector2(0.0, 4.0)
	var hover: StyleBoxFlat = normal.duplicate()
	hover.bg_color = color.lightened(0.08)
	var pressed: StyleBoxFlat = normal.duplicate()
	pressed.bg_color = color.darkened(0.12)
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", pressed)
	button.add_theme_stylebox_override("focus", normal)
	button.set_meta("selected", selected)
	button.set_meta("color_id", color_id)
	button.set_meta("touch_target", true)
	button.set_meta("picture_first", true)

func finish() -> void:
	if m.castle_logo_layer == null \
			or bool(m.castle_logo_layer.get_meta("closing", false)):
		return
	m.castle_logo_layer.set_meta("closing", true)
	m.castle_logo_layer.set_meta("committed", true)
	m._write_save()
	_set_status("🏰  ✨  💖")
	if m.chime != null:
		m.chime.pitch_scale = 1.35
		m.chime.play()
	m._say("roshan", "win", 0.0)
	var preview: Control = m.castle_logo_preview
	if preview != null:
		preview.pivot_offset = preview.size * 0.5
		var celebrate := preview.create_tween()
		celebrate.tween_property(preview, "scale", Vector2(1.12, 1.12),
			0.28).set_trans(Tween.TRANS_BACK)
		celebrate.tween_property(preview, "scale", Vector2.ONE,
			0.24).set_trans(Tween.TRANS_BOUNCE)
	m.get_tree().create_timer(0.85).timeout.connect(close.bind(true))

func close(committed: bool = false) -> void:
	var layer: CanvasLayer = m.castle_logo_layer
	if layer == null:
		return
	var keep: bool = committed or bool(layer.get_meta("committed", false))
	if not keep:
		m.castle_logo_color = normalise_color(String(
			layer.get_meta("original_color", "rainbow")))
		m.castle_logo_symbol = normalise_symbol(String(
			layer.get_meta("original_symbol", "rainbow")))
	layer.queue_free()
	m.castle_logo_layer = null
	m.castle_logo_preview = null
	m._set_world_controls_enabled(true, "castle_logo")
	refresh_room_display()

func clear_room_display() -> void:
	if m.castle_logo_room_display != null \
			and is_instance_valid(m.castle_logo_room_display):
		m.castle_logo_room_display.queue_free()
	m.castle_logo_room_display = null

func refresh_room_display() -> void:
	clear_room_display()
	if m.castle_room_stage == null or m.castle_room_id != "craft_room":
		return
	var display := _make_preview(
		"CastleLogoRoomDisplay", Vector2(88.0, 88.0))
	# Keep the personalized logo as a small pinned badge on the painted board.
	# It is UI-only and ignores input, so the board keeps its full hotspot.
	display.position = Vector2(578.0, 158.0)
	display.z_index = 22
	display.set_meta("display_location", "craft_room_idea_board_pinned_badge")
	m.castle_room_stage.add_child(display)
	m.castle_logo_room_display = display
