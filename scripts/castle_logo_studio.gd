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
const BANNER_TEXTURES: Dictionary = {
	"pink": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_pink.png"),
	"gold": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_gold.png"),
	"mint": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_mint.png"),
	"ocean": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_ocean.png"),
	"purple": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_purple.png"),
	"rainbow": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png"),
}
const SYMBOL_TEXTURES: Dictionary = {
	"rainbow": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_rainbow.png"),
	"shell": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_shell.png"),
	"kitty": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_kitty.png"),
	"dog": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_dog.png"),
	"star": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_star.png"),
	"heart": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_heart.png"),
	"crown": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_crown.png"),
	"butterfly": preload("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_butterfly.png"),
}
const RAINBOW_COLORS: Array[Color] = [
	Color(1.0, 0.35, 0.42), Color(1.0, 0.67, 0.25),
	Color(1.0, 0.87, 0.30), Color(0.38, 0.86, 0.54),
	Color(0.30, 0.73, 1.0), Color(0.68, 0.46, 0.94),
]
# Stage-space rectangles cover every baked purple shell banner in the active
# castle room art. The other rooms were audited and contain no copies of this
# design; keeping the registry here makes a future room addition explicit.
const ROOM_BANNER_RECTS: Dictionary = {
	"craft_room": [
		Rect2(140.0, 115.0, 95.0, 185.0),
		Rect2(1047.0, 115.0, 95.0, 185.0),
	],
	"playroom": [
		Rect2(122.0, 145.0, 86.0, 176.0),
		Rect2(1074.0, 145.0, 86.0, 176.0),
	],
}
const CRAFT_BOARD_BADGE_RECT := Rect2(578.0, 158.0, 88.0, 88.0)

class LogoPreview extends Control:
	var color_id := "rainbow"
	var symbol_id := "rainbow"
	var symbol_image: TextureRect

	func _init() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		symbol_image = TextureRect.new()
		symbol_image.mouse_filter = Control.MOUSE_FILTER_IGNORE
		symbol_image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		symbol_image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		add_child(symbol_image)
		resized.connect(_layout_symbol)

	func configure(next_color_id: String, next_symbol_id: String) -> void:
		color_id = next_color_id
		symbol_id = next_symbol_id
		set_meta("color_id", color_id)
		set_meta("symbol_id", symbol_id)
		symbol_image.texture = CastleLogoStudio.SYMBOL_TEXTURES.get(
			symbol_id, CastleLogoStudio.SYMBOL_TEXTURES["rainbow"]) as Texture2D
		_layout_symbol()
		queue_redraw()

	func _layout_symbol() -> void:
		if symbol_image == null:
			return
		var symbol_side: float = minf(size.x, size.y) * 0.58
		symbol_image.position = Vector2(
			(size.x - symbol_side) * 0.5, size.y * 0.20)
		symbol_image.size = Vector2(symbol_side, symbol_side)

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

class BannerPreview extends Control:
	var color_id := "rainbow"
	var symbol_id := "rainbow"
	var banner_image: TextureRect
	var symbol_image: TextureRect

	func _init() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		banner_image = _new_canvas_card()
		banner_image.name = "AuthoredBannerArt"
		add_child(banner_image)
		symbol_image = _new_canvas_card()
		symbol_image.name = "AuthoredBannerMotif"
		add_child(symbol_image)

	func _new_canvas_card() -> TextureRect:
		var card := TextureRect.new()
		card.mouse_filter = Control.MOUSE_FILTER_IGNORE
		card.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		card.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		return card

	func configure(next_color_id: String, next_symbol_id: String) -> void:
		color_id = next_color_id
		symbol_id = next_symbol_id
		set_meta("color_id", color_id)
		set_meta("symbol_id", symbol_id)
		set_meta("art_style", "pearl_castle_storybook_v2")
		banner_image.texture = CastleLogoStudio.BANNER_TEXTURES.get(
			color_id, CastleLogoStudio.BANNER_TEXTURES["rainbow"]) as Texture2D
		symbol_image.texture = CastleLogoStudio.SYMBOL_TEXTURES.get(
			symbol_id, CastleLogoStudio.SYMBOL_TEXTURES["rainbow"]) as Texture2D

	func place(stage_rect: Rect2) -> void:
		if banner_image.texture == null or symbol_image.texture == null:
			return
		set_meta("stage_rect", stage_rect)
		position = stage_rect.position
		size = stage_rect.size
		banner_image.position = Vector2.ZERO
		banner_image.size = stage_rect.size
		var symbol_side: float = stage_rect.size.x * 0.54
		symbol_image.position = Vector2(
			(stage_rect.size.x - symbol_side) * 0.5,
			stage_rect.size.y * 0.275)
		symbol_image.size = Vector2(symbol_side, symbol_side)

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

func _make_banner(preview_name: String,
		stage_rect: Rect2) -> BannerPreview:
	var preview := BannerPreview.new()
	preview.name = preview_name
	preview.configure(m.castle_logo_color, m.castle_logo_symbol)
	preview.place(stage_rect)
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
		m.castle_logo_room_display.free()
	m.castle_logo_room_display = null

func refresh_room_display() -> void:
	clear_room_display()
	if m.castle_room_stage == null:
		return
	var banner_rects: Array = ROOM_BANNER_RECTS.get(m.castle_room_id, [])
	if banner_rects.is_empty() and m.castle_room_id != "craft_room":
		return
	var display := Control.new()
	display.name = "CastleLogoRoomDisplay"
	display.mouse_filter = Control.MOUSE_FILTER_IGNORE
	display.position = Vector2.ZERO
	display.size = Vector2(1280.0, 720.0)
	display.z_index = 22
	display.set_meta("display_location", "castle_room_personalized_banners")
	display.set_meta("castle_room_id", m.castle_room_id)
	display.set_meta("replaces_design", "purple_shell_banner")
	m.castle_room_stage.add_child(display)
	var banner_nodes: Array[Node] = []
	for index: int in range(banner_rects.size()):
		var banner_rect: Rect2 = banner_rects[index] as Rect2
		var banner := _make_banner(
			"CastleLogoBanner_%d" % index, banner_rect)
		banner.set_meta("display_location",
			m.castle_room_id + "_purple_shell_banner_replacement")
		banner.set_meta("replaces_design", "purple_shell_banner")
		banner.set_meta("banner_index", index)
		display.add_child(banner)
		banner_nodes.append(banner)
	display.set_meta("banner_nodes", banner_nodes)
	if m.castle_room_id == "craft_room":
		# Keep the personalized logo as a small pinned badge on the painted board.
		# It remains input-transparent, so the board keeps its full hotspot.
		var badge := _make_preview(
			"CastleLogoCraftBoardBadge", CRAFT_BOARD_BADGE_RECT.size)
		badge.position = CRAFT_BOARD_BADGE_RECT.position
		badge.set_meta("display_location",
			"craft_room_idea_board_pinned_badge")
		display.add_child(badge)
	m.castle_logo_room_display = display
