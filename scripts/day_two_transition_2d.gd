class_name DayTwoTransition2D
extends CanvasLayer

## Picture-first bridge from the cleaned-castle boss victory into Day Two.
## Dawn reveals the approved castle while three room medallions wake inside a
## shared pearl card. The painted assets carry the scene; code-native shapes
## stay limited to quiet StorybookUI surfaces, soft light and framing.

signal finished

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const EXIT_START := 3.70
const TOTAL_TIME := 4.18
const NIGHT_TOP := Color(0.16, 0.13, 0.40, 1.0)
const NIGHT_MIDDLE := Color(0.32, 0.28, 0.58, 1.0)
const NIGHT_BOTTOM := Color(0.54, 0.48, 0.70, 1.0)
const MORNING_TOP := Color(0.55, 0.86, 0.97, 1.0)
const MORNING_MIDDLE := Color(0.72, 0.89, 0.96, 1.0)
const MORNING_BOTTOM := Color(1.0, 0.84, 0.68, 1.0)
const INK := Color(0.20, 0.18, 0.48, 1.0)
const INK_DEEP := Color(0.12, 0.08, 0.34, 1.0)
const PURPLE := Color(0.43, 0.30, 0.76, 1.0)
const GOLD := Color(1.0, 0.78, 0.30, 1.0)
const CREAM := Color(0.97, 0.95, 1.0, 1.0)
const PAPER := Color(0.94, 0.98, 1.0, 0.97)
const CASTLE_TEXTURE := preload(
	"res://assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png")
const CLOUD_TEXTURE := preload(
	"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_family_v7_hd_grade.png")
const SINGLE_CLOUD_TEXTURE := preload(
	"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png")
const OPERA_TEXTURE := preload(
	"res://assets/ui/castle_room_buttons_v2/room_opera_hall.png")
const CRAFT_TEXTURE := preload(
	"res://assets/ui/castle_room_buttons_v2/room_craft_room.png")
const KITCHEN_TEXTURE := preload(
	"res://assets/ui/castle_room_buttons_v2/room_kitchen.png")
const SHELL_MOTIF_TEXTURE := preload(
	"res://assets/flats/castle/logo_studio_v2/castle_banner_motif_shell.png")

var _elapsed := 0.0
var _done := false
var _root: Control = null
var _stage: Control = null
var _sky_gradient: Gradient = null
var _stars: Array[Label] = []
var _sun_anchor: Control = null
var _sun_halo: TextureRect = null
var _moon_anchor: Control = null
var _moon_cutout: Panel = null
var _castle: TextureRect = null
var _castle_glow: TextureRect = null
var _title_group: Control = null
var _activity_panel: Control = null
var _activity_cards: Array[TextureRect] = []
var _sparkles: Array[Label] = []
var _clouds: Array[TextureRect] = []


func _ready() -> void:
	name = "DayTwoTransition2D"
	layer = 44
	process_mode = Node.PROCESS_MODE_ALWAYS
	_build_ui()


func _build_ui() -> void:
	_root = Control.new()
	_root.name = "DayTwoTransitionRoot"
	_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_root)

	var letterbox := ColorRect.new()
	letterbox.name = "DayTwoLetterbox"
	letterbox.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	letterbox.color = NIGHT_TOP
	letterbox.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_root.add_child(letterbox)

	_stage = StorybookUI.add_stage(
		_root, get_viewport().get_visible_rect().size)
	_stage.name = "DayTwoTransitionStage"
	_stage.mouse_filter = Control.MOUSE_FILTER_STOP
	_build_sky()
	_build_moon()
	_build_sun()
	_build_painted_clouds()
	_build_page()
	_build_castle()
	_build_title()
	_build_activity_cards()
	_build_frame()


func _build_sky() -> void:
	_sky_gradient = Gradient.new()
	_sky_gradient.colors = PackedColorArray([
		NIGHT_TOP, NIGHT_MIDDLE, NIGHT_BOTTOM,
	])
	var sky_texture := GradientTexture2D.new()
	sky_texture.gradient = _sky_gradient
	sky_texture.width = int(CANVAS_SIZE.x)
	sky_texture.height = int(CANVAS_SIZE.y)
	sky_texture.fill_from = Vector2(0.5, 0.0)
	sky_texture.fill_to = Vector2(0.5, 1.0)
	var sky := TextureRect.new()
	sky.name = "DayTwoSky"
	sky.position = Vector2.ZERO
	sky.size = CANVAS_SIZE
	sky.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	sky.texture = sky_texture
	sky.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(sky)

	var star_positions: Array[Vector2] = [
		Vector2(92.0, 94.0), Vector2(176.0, 144.0),
		Vector2(286.0, 76.0), Vector2(418.0, 150.0),
		Vector2(835.0, 92.0), Vector2(970.0, 142.0),
		Vector2(1126.0, 88.0), Vector2(1184.0, 196.0),
	]
	for index: int in star_positions.size():
		var star := _make_label(
			_stage, "DayTwoNightStar_%02d" % index,
			"✦" if index % 3 == 0 else "·",
			Rect2(star_positions[index], Vector2(34.0, 34.0)),
			21 if index % 3 == 0 else 28, CREAM, 2)
		star.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		star.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		star.add_theme_color_override("font_outline_color", INK)
		star.modulate.a = 0.72
		_stars.append(star)


func _build_moon() -> void:
	_moon_anchor = Control.new()
	_moon_anchor.name = "DayTwoMoon"
	_moon_anchor.position = Vector2(86.0, 62.0)
	_moon_anchor.size = Vector2.ONE * 84.0
	_stage.add_child(_moon_anchor)
	_make_circle(
		_moon_anchor, "DayTwoMoonDisc", Vector2.ZERO, 80.0,
		CREAM, Color(0.54, 0.45, 0.72, 1.0), 4)
	_moon_cutout = _make_circle(
		_moon_anchor, "DayTwoMoonCutout", Vector2(26.0, -10.0), 80.0,
		NIGHT_TOP, NIGHT_TOP, 0)


func _build_sun() -> void:
	_sun_anchor = Control.new()
	_sun_anchor.name = "DayTwoSun"
	_sun_anchor.position = Vector2(1025.0, 170.0)
	_sun_anchor.size = Vector2.ONE * 118.0
	_stage.add_child(_sun_anchor)
	_sun_halo = TextureRect.new()
	_sun_halo.name = "DayTwoSunHalo"
	_sun_halo.position = Vector2(-50.0, -50.0)
	_sun_halo.size = Vector2.ONE * 218.0
	_sun_halo.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_sun_halo.texture = _make_radial_gradient_texture(
		Color(1.0, 0.82, 0.33, 0.52))
	_sun_halo.pivot_offset = _sun_halo.size * 0.5
	_sun_halo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_sun_anchor.add_child(_sun_halo)
	_make_circle(
		_sun_anchor, "DayTwoSunDisc", Vector2.ZERO, 118.0,
		Color(1.0, 0.82, 0.34, 1.0), CREAM, 5)
	_make_circle(
		_sun_anchor, "DayTwoSunCore", Vector2(18.0, 15.0), 66.0,
		Color(1.0, 0.91, 0.58, 0.72), Color.TRANSPARENT, 0)


func _build_painted_clouds() -> void:
	var cloud_family := TextureRect.new()
	cloud_family.name = "DayTwoPaintedCloudBank"
	cloud_family.texture = CLOUD_TEXTURE
	cloud_family.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	cloud_family.position = Vector2(-36.0, 270.0)
	cloud_family.size = Vector2(1352.0, 380.0)
	cloud_family.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	cloud_family.modulate = Color(0.95, 0.96, 1.0, 0.72)
	cloud_family.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(cloud_family)
	_clouds.append(cloud_family)

	var cloud_left := TextureRect.new()
	cloud_left.name = "DayTwoPaintedCloudLeft"
	cloud_left.texture = SINGLE_CLOUD_TEXTURE
	cloud_left.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	cloud_left.position = Vector2(30.0, 238.0)
	cloud_left.size = Vector2(310.0, 148.0)
	cloud_left.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	cloud_left.modulate = Color(0.94, 0.96, 1.0, 0.70)
	cloud_left.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(cloud_left)
	_clouds.append(cloud_left)

	var cloud_right := TextureRect.new()
	cloud_right.name = "DayTwoPaintedCloudRight"
	cloud_right.texture = SINGLE_CLOUD_TEXTURE
	cloud_right.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	cloud_right.position = Vector2(950.0, 250.0)
	cloud_right.size = Vector2(270.0, 132.0)
	cloud_right.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	cloud_right.modulate = Color(0.94, 0.96, 1.0, 0.66)
	cloud_right.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(cloud_right)
	_clouds.append(cloud_right)


func _build_page() -> void:
	pass


func _build_castle() -> void:
	_castle_glow = TextureRect.new()
	_castle_glow.name = "DayTwoCastleGlow"
	_castle_glow.position = Vector2(132.0, 84.0)
	_castle_glow.size = Vector2(792.0, 620.0)
	_castle_glow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_castle_glow.texture = _make_radial_gradient_texture(
		Color(1.0, 0.90, 0.60, 0.42))
	_castle_glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(_castle_glow)

	_castle = TextureRect.new()
	_castle.name = "DayTwoCastle"
	_castle.texture = CASTLE_TEXTURE
	_castle.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_castle.position = Vector2(160.0, 128.0)
	_castle.size = Vector2(748.0, 590.0)
	_castle.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_castle.pivot_offset = _castle.size * 0.5
	_castle.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(_castle)


func _build_title() -> void:
	_title_group = Control.new()
	_title_group.name = "DayTwoTitleCard"
	_title_group.position = Vector2(346.0, 48.0)
	_title_group.size = Vector2(540.0, 104.0)
	_title_group.pivot_offset = _title_group.size * 0.5
	_stage.add_child(_title_group)
	var eyebrow := _make_label(
		_title_group, "DayTwoEyebrow", "✦  A NEW DAY  ✦",
		Rect2(47.0, 0.0, 446.0, 32.0), 19, GOLD, 3)
	eyebrow.add_theme_color_override("font_outline_color", INK)
	eyebrow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	eyebrow.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	var title := _make_label(
		_title_group, "DayTwoTitle", "DAY TWO!",
		Rect2(10.0, 25.0, 520.0, 74.0), 56, INK_DEEP, 6)
	title.add_theme_color_override("font_outline_color", CREAM)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER


func _build_activity_cards() -> void:
	_activity_panel = Control.new()
	_activity_panel.name = "DayTwoActivityTray"
	_activity_panel.position = Vector2(922.0, 292.0)
	_activity_panel.size = Vector2(280.0, 352.0)
	_activity_panel.pivot_offset = _activity_panel.size * 0.5
	_stage.add_child(_activity_panel)
	var tray_shell := TextureRect.new()
	tray_shell.name = "DayTwoPaintedShellAccent"
	tray_shell.texture = SHELL_MOTIF_TEXTURE
	tray_shell.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	tray_shell.position = Vector2(118.0, -11.0)
	tray_shell.size = Vector2(44.0, 44.0)
	tray_shell.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	tray_shell.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_activity_panel.add_child(tray_shell)
	var heading := _make_label(
		_activity_panel, "DayTwoActivityHeading", "NEW ADVENTURES",
		Rect2(24.0, 30.0, 232.0, 34.0), 16, PURPLE, 3)
	heading.add_theme_color_override("font_outline_color", CREAM)
	heading.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	heading.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

	var textures: Array[Texture2D] = [OPERA_TEXTURE, CRAFT_TEXTURE, KITCHEN_TEXTURE]
	var positions: Array[Vector2] = [
		Vector2(90.0, 54.0), Vector2(90.0, 151.0), Vector2(90.0, 248.0),
	]
	var names: Array[String] = ["Opera", "CraftJob", "KitchenJob"]
	for index: int in textures.size():
		var card := TextureRect.new()
		card.name = "DayTwoActivity" + names[index]
		card.texture = textures[index]
		card.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		card.position = positions[index]
		card.size = Vector2.ONE * 100.0
		card.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		card.pivot_offset = card.size * 0.5
		card.mouse_filter = Control.MOUSE_FILTER_IGNORE
		card.modulate.a = 0.0
		card.scale = Vector2.ONE * 0.64
		_activity_panel.add_child(card)
		_activity_cards.append(card)

	var sparkle_positions: Array[Vector2] = [
		Vector2(54.0, 112.0), Vector2(194.0, 235.0),
	]
	for index: int in sparkle_positions.size():
		var sparkle := _make_label(
			_activity_panel, "DayTwoUnlockSparkle_%02d" % index,
			"✦" if index % 2 == 0 else "·",
			Rect2(sparkle_positions[index], Vector2(34.0, 34.0)),
			22 if index % 2 == 0 else 28, GOLD, 2)
		sparkle.add_theme_color_override("font_outline_color", INK)
		sparkle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		sparkle.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		sparkle.modulate.a = 0.0
		_sparkles.append(sparkle)


func _build_frame() -> void:
	var frame := Panel.new()
	frame.name = "DayTwoFrame"
	frame.position = Vector2(14.0, 14.0)
	frame.size = Vector2(1252.0, 692.0)
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var frame_style := StyleBoxFlat.new()
	frame_style.bg_color = Color.TRANSPARENT
	frame_style.border_color = INK_DEEP
	frame_style.set_border_width_all(7)
	frame_style.set_corner_radius_all(58)
	frame.add_theme_stylebox_override("panel", frame_style)
	_stage.add_child(frame)


func _make_label(
		parent: Node, node_name: String, text: String, rect: Rect2,
		font_size: int, color: Color, outline_size: int) -> Label:
	var label := Label.new()
	label.name = node_name
	label.text = text
	label.position = rect.position
	label.size = rect.size
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(label, font_size, color, outline_size)
	parent.add_child(label)
	return label


func _make_circle(
		parent: Node, node_name: String, position: Vector2, diameter: float,
		fill: Color, border: Color, border_width: int) -> Panel:
	var panel := Panel.new()
	panel.name = node_name
	panel.position = position
	panel.size = Vector2.ONE * diameter
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = border
	style.set_border_width_all(border_width)
	style.set_corner_radius_all(int(diameter * 0.5))
	panel.add_theme_stylebox_override("panel", style)
	parent.add_child(panel)
	return panel


func _make_radial_gradient_texture(center_color: Color) -> GradientTexture2D:
	var gradient := Gradient.new()
	gradient.colors = PackedColorArray([
		center_color,
		Color(center_color.r, center_color.g, center_color.b, 0.0),
	])
	var texture := GradientTexture2D.new()
	texture.gradient = gradient
	texture.width = 512
	texture.height = 512
	texture.fill = GradientTexture2D.FILL_RADIAL
	texture.fill_from = Vector2(0.5, 0.5)
	texture.fill_to = Vector2(0.5, 0.0)
	return texture


func _process(delta: float) -> void:
	if _done or _root == null:
		return
	_elapsed += delta
	var dawn: float = smoothstep(0.0, 1.0,
		clampf((_elapsed - 0.18) / 1.72, 0.0, 1.0))
	if _sky_gradient != null:
		_sky_gradient.colors = PackedColorArray([
			NIGHT_TOP.lerp(MORNING_TOP, dawn),
			NIGHT_MIDDLE.lerp(MORNING_MIDDLE, dawn),
			NIGHT_BOTTOM.lerp(MORNING_BOTTOM, dawn),
		])
	for index: int in _stars.size():
		var star: Label = _stars[index]
		star.modulate.a = (1.0 - dawn) * (0.58 + 0.30 * sin(
			_elapsed * 3.0 + float(index) * 0.7))
	if _moon_anchor != null:
		_moon_anchor.position.y = lerpf(62.0, -104.0, dawn)
		_moon_anchor.modulate.a = 1.0 - dawn
	if _moon_cutout != null:
		var moon_style: StyleBoxFlat = \
			_moon_cutout.get_theme_stylebox("panel") as StyleBoxFlat
		if moon_style != null:
			moon_style.bg_color = NIGHT_TOP.lerp(MORNING_TOP, dawn)
			moon_style.border_color = moon_style.bg_color
	if _sun_anchor != null:
		_sun_anchor.position.y = lerpf(170.0, 70.0, dawn)
		_sun_anchor.scale = Vector2.ONE * lerpf(0.78, 1.0, dawn)
		_sun_anchor.modulate.a = 0.45 + dawn * 0.55
	if _sun_halo != null:
		var halo_pulse: float = 0.96 + 0.04 * sin(_elapsed * 4.0)
		_sun_halo.scale = Vector2.ONE * halo_pulse
	if _castle != null:
		var castle_pop: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 0.52) / 0.72, 0.0, 1.0))
		_castle.scale = Vector2.ONE * lerpf(0.91, 1.0, castle_pop)
		var castle_tint: Color = Color.WHITE.lerp(
			Color(1.0, 0.96, 0.84), dawn * 0.08)
		castle_tint.a = castle_pop
		_castle.modulate = castle_tint
	if _castle_glow != null:
		_castle_glow.modulate.a = dawn * (0.62 + 0.12 * sin(_elapsed * 3.0))
	if _title_group != null:
		var title_pop: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 0.70) / 0.48, 0.0, 1.0))
		_title_group.scale = Vector2.ONE * lerpf(0.88, 1.0, title_pop)
		_title_group.modulate.a = title_pop
	if _activity_panel != null:
		var tray_progress: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 1.18) / 0.46, 0.0, 1.0))
		_activity_panel.modulate.a = tray_progress
		_activity_panel.scale = Vector2.ONE * lerpf(0.92, 1.0, tray_progress)
	for index: int in _activity_cards.size():
		var card: TextureRect = _activity_cards[index]
		var card_progress: float = smoothstep(0.0, 1.0, clampf(
			(_elapsed - 1.38 - float(index) * 0.15) / 0.38, 0.0, 1.0))
		card.modulate.a = card_progress
		card.scale = Vector2.ONE * lerpf(0.64, 1.0, card_progress)
		if card_progress >= 1.0:
			var pulse: float = 0.5 + 0.5 * sin(_elapsed * 3.6 + float(index))
			card.scale = Vector2.ONE * (1.0 + pulse * 0.025)
	for index: int in _sparkles.size():
		var sparkle_progress: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 1.46) / 0.45, 0.0, 1.0))
		var sparkle: Label = _sparkles[index]
		var wave: float = 0.5 + 0.5 * sin(_elapsed * 4.6 + float(index) * 0.8)
		sparkle.modulate.a = sparkle_progress * wave * 0.78
		sparkle.scale = Vector2.ONE * (0.82 + wave * 0.22)
	for index: int in _clouds.size():
		_clouds[index].position.x += delta * (1.8 + float(index) * 0.7)

	var reveal: float = smoothstep(0.0, 1.0,
		clampf(_elapsed / 0.20, 0.0, 1.0))
	var exit_alpha: float = 1.0
	if _elapsed >= EXIT_START:
		exit_alpha = 1.0 - smoothstep(0.0, 1.0,
			clampf((_elapsed - EXIT_START) / (TOTAL_TIME - EXIT_START), 0.0, 1.0))
	_root.modulate.a = minf(reveal, exit_alpha)
	if _elapsed >= TOTAL_TIME:
		_complete()


func cancel() -> void:
	if _done:
		return
	_done = true
	queue_free()


func current_beat() -> String:
	if _elapsed < 1.20:
		return "dawn"
	if _elapsed < 2.20:
		return "unlock"
	if _elapsed < EXIT_START:
		return "open"
	return "exit"


func _complete() -> void:
	if _done:
		return
	_done = true
	finished.emit()
	queue_free()
