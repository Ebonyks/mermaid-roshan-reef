class_name DayTwoTransition2D
extends CanvasLayer

## Picture-first bridge from the cleaned-castle boss victory into Day Two.
## Dawn physically reveals the approved castle and newly lit room medallions;
## the large title and voice event reinforce the change for a grown-up helper.

signal finished

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const EXIT_START := 3.70
const TOTAL_TIME := 4.18
const NIGHT_TOP := Color(0.055, 0.035, 0.20, 1.0)
const NIGHT_BOTTOM := Color(0.29, 0.15, 0.48, 1.0)
const MORNING_TOP := Color(0.22, 0.66, 0.91, 1.0)
const MORNING_BOTTOM := Color(1.0, 0.66, 0.46, 1.0)
const INK := Color(0.12, 0.06, 0.31, 1.0)
const GOLD := Color(1.0, 0.76, 0.26, 1.0)
const CREAM := Color(1.0, 0.96, 0.79, 1.0)
const CASTLE_TEXTURE := preload(
	"res://assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png")
const OPERA_TEXTURE := preload(
	"res://assets/ui/castle_room_buttons_v2/room_opera_hall.png")
const CRAFT_TEXTURE := preload(
	"res://assets/ui/castle_room_buttons_v2/room_craft_room.png")
const KITCHEN_TEXTURE := preload(
	"res://assets/ui/castle_room_buttons_v2/room_kitchen.png")

var _elapsed := 0.0
var _done := false
var _root: Control = null
var _stage: Control = null
var _sky_bands: Array[ColorRect] = []
var _stars: Array[Label] = []
var _sun_anchor: Control = null
var _sun_halo: Panel = null
var _sun_disc: Panel = null
var _sun_rays: Array[Polygon2D] = []
var _moon_anchor: Control = null
var _moon_cutout: Panel = null
var _castle: TextureRect = null
var _castle_glow: Panel = null
var _title_group: Control = null
var _activity_cards: Array[TextureRect] = []
var _sparkles: Array[Label] = []
var _clouds: Array[Panel] = []


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
	_build_landscape()
	_build_castle()
	_build_title()
	_build_activity_cards()
	_build_frame()


func _build_sky() -> void:
	for index: int in range(12):
		var band := ColorRect.new()
		band.name = "DayTwoSkyBand_%02d" % index
		band.position = Vector2(0.0, float(index) * 60.0)
		band.size = Vector2(1280.0, 61.0)
		band.color = NIGHT_TOP.lerp(NIGHT_BOTTOM, float(index) / 11.0)
		band.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_stage.add_child(band)
		_sky_bands.append(band)
	for index: int in range(18):
		var star := Label.new()
		star.name = "DayTwoNightStar_%02d" % index
		star.text = "✦" if index % 3 == 0 else "·"
		star.position = Vector2(
			42.0 + float((index * 103) % 1170),
			35.0 + float((index * 67) % 290))
		star.size = Vector2(34.0, 34.0)
		star.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		star.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		star.mouse_filter = Control.MOUSE_FILTER_IGNORE
		StorybookUI.style_label(star, 24 if index % 3 == 0 else 31, CREAM, 2)
		star.add_theme_color_override("font_outline_color", INK)
		_stage.add_child(star)
		_stars.append(star)


func _build_moon() -> void:
	_moon_anchor = Control.new()
	_moon_anchor.name = "DayTwoMoon"
	_moon_anchor.position = Vector2(102.0, 84.0)
	_moon_anchor.size = Vector2.ONE * 134.0
	_stage.add_child(_moon_anchor)
	_make_circle(
		_moon_anchor, "DayTwoMoonDisc", Vector2(0.0, 0.0), 128.0,
		CREAM, Color(0.45, 0.29, 0.68, 1.0), 6)
	_moon_cutout = _make_circle(
		_moon_anchor, "DayTwoMoonCutout", Vector2(38.0, -18.0), 128.0,
		NIGHT_TOP, NIGHT_TOP, 0)


func _build_sun() -> void:
	# The open-beat composition is the visual destination, so rays converge on
	# the sun's final center rather than the below-horizon starting position.
	var origin := Vector2(304.0, 330.0)
	for index: int in range(14):
		var angle_a: float = float(index) * TAU / 14.0 - 0.04
		var angle_b: float = angle_a + TAU / 30.0
		var ray := _add_polygon(
			"DayTwoSunRay_%02d" % index,
			PackedVector2Array([
				origin,
				origin + Vector2(cos(angle_a), sin(angle_a)) * 430.0,
				origin + Vector2(cos(angle_b), sin(angle_b)) * 430.0,
			]), Color(1.0, 0.83, 0.35, 0.22))
		_sun_rays.append(ray)
	_sun_anchor = Control.new()
	_sun_anchor.name = "DayTwoSun"
	_sun_anchor.position = Vector2(184.0, 454.0)
	_sun_anchor.size = Vector2.ONE * 240.0
	_stage.add_child(_sun_anchor)
	_sun_halo = _make_circle(
		_sun_anchor, "DayTwoSunHalo", Vector2(-42.0, -42.0), 324.0,
		Color(1.0, 0.79, 0.28, 0.18), Color(1.0, 0.90, 0.55, 0.16), 5)
	_sun_disc = _make_circle(
		_sun_anchor, "DayTwoSunDisc", Vector2(0.0, 0.0), 240.0,
		Color(1.0, 0.72, 0.18, 1.0), CREAM, 8)
	var sun_core := _make_circle(
		_sun_anchor, "DayTwoSunCore", Vector2(28.0, 24.0), 150.0,
		Color(1.0, 0.87, 0.34, 0.74), Color.TRANSPARENT, 0)
	sun_core.mouse_filter = Control.MOUSE_FILTER_IGNORE


func _build_landscape() -> void:
	_add_cloud(Vector2(30.0, 356.0), 1.08, "DayTwoCloudLeft")
	_add_cloud(Vector2(860.0, 315.0), 0.88, "DayTwoCloudRight")
	_add_polygon("DayTwoFarHill", PackedVector2Array([
		Vector2(-40.0, 610.0), Vector2(130.0, 492.0),
		Vector2(328.0, 585.0), Vector2(570.0, 470.0),
		Vector2(824.0, 594.0), Vector2(1090.0, 474.0),
		Vector2(1320.0, 602.0), Vector2(1320.0, 720.0),
		Vector2(-40.0, 720.0),
	]), Color(0.36, 0.28, 0.67, 0.88))
	_add_polygon("DayTwoNearHill", PackedVector2Array([
		Vector2(-40.0, 655.0), Vector2(184.0, 568.0),
		Vector2(420.0, 640.0), Vector2(711.0, 545.0),
		Vector2(968.0, 630.0), Vector2(1160.0, 559.0),
		Vector2(1320.0, 631.0), Vector2(1320.0, 720.0),
		Vector2(-40.0, 720.0),
	]), Color(0.27, 0.69, 0.66, 1.0))
	_add_polygon("DayTwoForeground", PackedVector2Array([
		Vector2(-30.0, 690.0), Vector2(235.0, 642.0),
		Vector2(558.0, 686.0), Vector2(858.0, 627.0),
		Vector2(1080.0, 675.0), Vector2(1310.0, 640.0),
		Vector2(1310.0, 730.0), Vector2(-30.0, 730.0),
	]), Color(0.18, 0.48, 0.49, 1.0))


func _build_castle() -> void:
	_castle_glow = _make_circle(
		_stage, "DayTwoCastleGlow", Vector2(343.0, 182.0), 540.0,
		Color(1.0, 0.88, 0.53, 0.17), Color(1.0, 0.94, 0.69, 0.22), 6)
	_castle = TextureRect.new()
	_castle.name = "DayTwoCastle"
	_castle.texture = CASTLE_TEXTURE
	_castle.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_castle.position = Vector2(347.0, 205.0)
	_castle.size = Vector2(530.0, 530.0)
	_castle.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_castle.pivot_offset = _castle.size * 0.5
	_castle.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(_castle)


func _build_title() -> void:
	_title_group = Control.new()
	_title_group.name = "DayTwoTitleCard"
	_title_group.position = Vector2(405.0, 34.0)
	_title_group.size = Vector2(700.0, 168.0)
	_title_group.pivot_offset = _title_group.size * 0.5
	_stage.add_child(_title_group)
	var eyebrow := _make_label(
		_title_group, "DayTwoEyebrow", "✦  A NEW DAY!  ✦",
		Rect2(86.0, 0.0, 520.0, 55.0), 28, GOLD, 4)
	eyebrow.add_theme_color_override("font_outline_color", INK)
	eyebrow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	eyebrow.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	var title_shadow := _make_label(
		_title_group, "DayTwoTitleShadow", "DAY TWO!",
		Rect2(16.0, 45.0, 684.0, 116.0), 88, INK, 15)
	title_shadow.add_theme_color_override("font_outline_color", INK)
	title_shadow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_shadow.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	var title := _make_label(
		_title_group, "DayTwoTitle", "DAY TWO!",
		Rect2(5.0, 34.0, 684.0, 116.0), 88, CREAM, 11)
	title.add_theme_color_override("font_outline_color", Color(0.31, 0.16, 0.61, 1.0))
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER


func _build_activity_cards() -> void:
	var textures: Array[Texture2D] = [OPERA_TEXTURE, CRAFT_TEXTURE, KITCHEN_TEXTURE]
	var positions: Array[Vector2] = [
		Vector2(952.0, 273.0), Vector2(1074.0, 415.0), Vector2(941.0, 510.0),
	]
	var names: Array[String] = ["Opera", "CraftJob", "KitchenJob"]
	for index: int in textures.size():
		var card := TextureRect.new()
		card.name = "DayTwoActivity" + names[index]
		card.texture = textures[index]
		card.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		card.position = positions[index]
		card.size = Vector2.ONE * 122.0
		card.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		card.pivot_offset = card.size * 0.5
		card.mouse_filter = Control.MOUSE_FILTER_IGNORE
		card.modulate.a = 0.0
		card.scale = Vector2.ONE * 0.45
		_stage.add_child(card)
		_activity_cards.append(card)
	for index: int in range(8):
		var sparkle := _make_label(
			_stage, "DayTwoUnlockSparkle_%02d" % index,
			"✦" if index % 2 == 0 else "◆",
			Rect2(
				808.0 + float((index * 71) % 310),
				294.0 + float((index * 89) % 315),
				46.0, 46.0),
			28 if index % 2 == 0 else 20, GOLD, 3)
		sparkle.add_theme_color_override("font_outline_color", INK)
		sparkle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		sparkle.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		sparkle.modulate.a = 0.0
		_sparkles.append(sparkle)
	var caption_shadow := _make_panel(
		_stage, "DayTwoCaptionShadow", Rect2(764.0, 646.0, 470.0, 58.0),
		INK, INK, 24, 0)
	caption_shadow.position += Vector2(7.0, 8.0)
	var caption_panel := _make_panel(
		_stage, "DayTwoCaption", Rect2(764.0, 646.0, 470.0, 58.0),
		GOLD, Color(0.12, 0.06, 0.31, 0.94), 24, 4)
	var caption := _make_label(
		caption_panel, "DayTwoCaptionText", "JOBS + OPERA OPEN!",
		Rect2(8.0, 1.0, 454.0, 53.0), 25, CREAM, 2)
	caption.add_theme_color_override("font_outline_color", INK)
	caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	caption.vertical_alignment = VERTICAL_ALIGNMENT_CENTER


func _build_frame() -> void:
	_make_panel(
		_stage, "DayTwoFrame", Rect2(10.0, 10.0, 1260.0, 700.0),
		INK, Color.TRANSPARENT, 0, 12)
	for index: int in range(4):
		var pearl := _make_circle(
			_stage, "DayTwoFramePearl_%d" % index,
			Vector2(27.0 if index % 2 == 0 else 1225.0,
				27.0 if index < 2 else 674.0),
			28.0, CREAM, INK, 4)
		pearl.mouse_filter = Control.MOUSE_FILTER_IGNORE


func _add_cloud(position: Vector2, scale_value: float, cloud_name: String) -> void:
	var sizes: Array[Vector2] = [
		Vector2(145.0, 58.0), Vector2(105.0, 78.0), Vector2(125.0, 70.0),
	]
	var offsets: Array[Vector2] = [
		Vector2(0.0, 34.0), Vector2(50.0, 4.0), Vector2(112.0, 25.0),
	]
	for index: int in sizes.size():
		var cloud := _make_panel(
			_stage, cloud_name + "_%d" % index,
			Rect2(position + offsets[index] * scale_value, sizes[index] * scale_value),
			Color.TRANSPARENT, Color(0.96, 0.93, 1.0, 0.60),
			int(38.0 * scale_value), 0)
		_clouds.append(cloud)


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


func _make_panel(
		parent: Node, node_name: String, rect: Rect2,
		accent: Color, fill: Color, radius: int, border_width: int) -> Panel:
	var panel := Panel.new()
	panel.name = node_name
	panel.position = rect.position
	panel.size = rect.size
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = accent
	style.set_border_width_all(border_width)
	style.set_corner_radius_all(radius)
	panel.add_theme_stylebox_override("panel", style)
	parent.add_child(panel)
	return panel


func _make_circle(
		parent: Node, node_name: String, position: Vector2, diameter: float,
		fill: Color, border: Color, border_width: int) -> Panel:
	return _make_panel(
		parent, node_name, Rect2(position, Vector2.ONE * diameter),
		border, fill, int(diameter * 0.5), border_width)


func _add_polygon(
		node_name: String, points: PackedVector2Array, color: Color) -> Polygon2D:
	var polygon := Polygon2D.new()
	polygon.name = node_name
	polygon.polygon = points
	polygon.color = color
	_stage.add_child(polygon)
	return polygon


func _process(delta: float) -> void:
	if _done or _root == null:
		return
	_elapsed += delta
	var dawn: float = smoothstep(0.0, 1.0,
		clampf((_elapsed - 0.18) / 1.72, 0.0, 1.0))
	for index: int in _sky_bands.size():
		var vertical: float = float(index) / maxf(1.0, float(_sky_bands.size() - 1))
		var night_color: Color = NIGHT_TOP.lerp(NIGHT_BOTTOM, vertical)
		var morning_color: Color = MORNING_TOP.lerp(MORNING_BOTTOM, vertical)
		_sky_bands[index].color = night_color.lerp(morning_color, dawn)
	for index: int in _stars.size():
		var star: Label = _stars[index]
		star.modulate.a = (1.0 - dawn) * (0.62 + 0.38 * sin(
			_elapsed * 3.2 + float(index) * 0.7))
	if _moon_anchor != null:
		_moon_anchor.position.y = lerpf(84.0, -185.0, dawn)
		_moon_anchor.modulate.a = 1.0 - dawn
	if _moon_cutout != null:
		var moon_style: StyleBoxFlat = _moon_cutout.get_theme_stylebox("panel") as StyleBoxFlat
		if moon_style != null:
			moon_style.bg_color = NIGHT_TOP.lerp(MORNING_TOP, dawn)
			moon_style.border_color = moon_style.bg_color
	if _sun_anchor != null:
		_sun_anchor.position.y = lerpf(454.0, 210.0, dawn)
		_sun_anchor.scale = Vector2.ONE * lerpf(0.72, 1.0, dawn)
	if _sun_halo != null:
		var halo_pulse: float = 0.96 + 0.06 * sin(_elapsed * 4.0)
		_sun_halo.scale = Vector2.ONE * halo_pulse
		_sun_halo.pivot_offset = _sun_halo.size * 0.5
	for index: int in _sun_rays.size():
		var ray: Polygon2D = _sun_rays[index]
		ray.modulate.a = dawn * (0.70 + 0.24 * sin(_elapsed * 2.8 + float(index)))
	if _castle != null:
		var castle_pop: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 0.52) / 0.72, 0.0, 1.0))
		_castle.scale = Vector2.ONE * lerpf(0.76, 1.0, castle_pop)
		var castle_tint: Color = Color.WHITE.lerp(
			Color(1.0, 0.94, 0.76), dawn * 0.14)
		castle_tint.a = castle_pop
		_castle.modulate = castle_tint
	if _castle_glow != null:
		_castle_glow.modulate.a = dawn * (0.72 + 0.18 * sin(_elapsed * 3.0))
	if _title_group != null:
		var title_pop: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 0.70) / 0.48, 0.0, 1.0))
		_title_group.scale = Vector2.ONE * lerpf(0.74, 1.0, title_pop)
		_title_group.modulate.a = title_pop
	for index: int in _activity_cards.size():
		var card: TextureRect = _activity_cards[index]
		var card_progress: float = smoothstep(0.0, 1.0, clampf(
			(_elapsed - 1.42 - float(index) * 0.16) / 0.40, 0.0, 1.0))
		card.modulate.a = card_progress
		card.scale = Vector2.ONE * lerpf(0.45, 1.0, card_progress)
		if card_progress >= 1.0:
			var pulse: float = 0.5 + 0.5 * sin(_elapsed * 4.0 + float(index))
			card.scale = Vector2.ONE * (1.0 + pulse * 0.035)
	for index: int in _sparkles.size():
		var sparkle_progress: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 1.45) / 0.45, 0.0, 1.0))
		var sparkle: Label = _sparkles[index]
		var wave: float = 0.5 + 0.5 * sin(_elapsed * 5.0 + float(index) * 0.8)
		sparkle.modulate.a = sparkle_progress * wave
		sparkle.scale = Vector2.ONE * (0.74 + wave * 0.34)
	for index: int in _clouds.size():
		_clouds[index].position.x += delta * (5.0 + float(index % 3) * 2.0)

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
