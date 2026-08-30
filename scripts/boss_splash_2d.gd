class_name BossSplash2D
extends CanvasLayer

## Reusable, true-2D boss-introduction language.
##
## Every splash teaches the boss in three picture-first beats: a readable
## entrance action, an identity pose, then the exact gameplay tell. Approved
## character frames remain authoritative. The framing is drawn from cheap 2D
## Controls and polygons so it stays crisp and inexpensive on the target phone.

signal finished

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const JUMP_START := 0.12
const GRIN_START := 0.96
const FLASH_START := 1.42
const EXIT_START := 2.86
const TOTAL_TIME := 3.24
const INK := Color(0.105, 0.055, 0.27, 1.0)
const PLUM := Color(0.245, 0.105, 0.49, 1.0)
const VIOLET := Color(0.39, 0.19, 0.72, 1.0)
const MAGENTA := Color(0.93, 0.19, 0.52, 1.0)
const AQUA := Color(0.23, 0.78, 0.88, 1.0)
const CREAM := Color(1.0, 0.95, 0.78, 1.0)
const GOLD := Color(1.0, 0.72, 0.22, 1.0)

var _boss_frames: SpriteFrames = null
var _boss_name := "BOSS"
var _boss_kind := "A BIG ADVENTURE"
var _badge_texture: Texture2D = null
var _elapsed := 0.0
var _done := false
var _grin_started := false
var _root: Control = null
var _stage: Control = null
var _boss: AnimatedSprite2D = null
var _boss_anchor: Node2D = null
var _boss_shadow: Panel = null
var _badge: Sprite2D = null
var _badge_halo: Panel = null
var _title_panel: Control = null
var _intro_ribbon: Control = null
var _flare_labels: Array[Label] = []
var _burst_rays: Array[Polygon2D] = []
var _base_boss_position := Vector2(340.0, 468.0)


func configure(
		boss_frames: SpriteFrames,
		boss_name: String,
		boss_kind: String,
		badge_texture: Texture2D) -> void:
	_boss_frames = boss_frames
	_boss_name = boss_name
	_boss_kind = boss_kind
	_badge_texture = badge_texture


func _ready() -> void:
	name = "BossSplash2D"
	layer = 42
	process_mode = Node.PROCESS_MODE_ALWAYS
	_build_ui()
	_play_if_available(&"jump")


func _build_ui() -> void:
	_root = Control.new()
	_root.name = "BossSplashRoot"
	_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_root)

	var letterbox := ColorRect.new()
	letterbox.name = "BossSplashLetterbox"
	letterbox.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	letterbox.color = Color(0.02, 0.012, 0.08, 1.0)
	letterbox.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_root.add_child(letterbox)

	_stage = StorybookUI.add_stage(
		_root, get_viewport().get_visible_rect().size)
	_stage.name = "BossSplashStage"
	_stage.mouse_filter = Control.MOUSE_FILTER_STOP

	var field := ColorRect.new()
	field.name = "BossSplashField"
	field.position = Vector2.ZERO
	field.size = CANVAS_SIZE
	field.color = INK
	field.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(field)

	_build_radial_burst()
	_add_polygon("BossSplashMagentaSlash", PackedVector2Array([
		Vector2(-80.0, 548.0), Vector2(1280.0, 196.0),
		Vector2(1280.0, 322.0), Vector2(-80.0, 674.0)]), MAGENTA)
	_add_polygon("BossSplashAquaSlash", PackedVector2Array([
		Vector2(-80.0, 644.0), Vector2(1280.0, 292.0),
		Vector2(1280.0, 356.0), Vector2(-80.0, 708.0)]), AQUA)
	_add_polygon("BossSplashTitleFieldShadow", PackedVector2Array([
		Vector2(616.0, 104.0), Vector2(1305.0, 42.0),
		Vector2(1305.0, 720.0), Vector2(742.0, 720.0)]), Color(0.04, 0.02, 0.15, 0.58))
	_add_polygon("BossSplashTitleField", PackedVector2Array([
		Vector2(640.0, 88.0), Vector2(1305.0, 24.0),
		Vector2(1305.0, 720.0), Vector2(770.0, 720.0)]), PLUM)
	_add_polygon("BossSplashTitleFieldHighlight", PackedVector2Array([
		Vector2(667.0, 103.0), Vector2(1305.0, 43.0),
		Vector2(1305.0, 132.0), Vector2(684.0, 191.0)]), Color(0.55, 0.28, 0.86, 0.72))
	_build_halftone()
	_build_dust_cloud()
	_build_character()
	_build_title()
	_build_frame()


func _build_radial_burst() -> void:
	var origin := Vector2(338.0, 414.0)
	var ray_colors: Array[Color] = [
		Color(0.33, 0.14, 0.60, 0.48),
		Color(0.55, 0.22, 0.69, 0.32),
	]
	for index: int in range(14):
		var angle_a: float = -PI + float(index) * TAU / 14.0
		var angle_b: float = angle_a + TAU / 28.0
		var ray := _add_polygon("BossSplashRay_%d" % index, PackedVector2Array([
			origin,
			origin + Vector2(cos(angle_a), sin(angle_a)) * 1120.0,
			origin + Vector2(cos(angle_b), sin(angle_b)) * 1120.0,
		]), ray_colors[index % ray_colors.size()])
		_burst_rays.append(ray)


func _build_halftone() -> void:
	for row: int in range(6):
		for column: int in range(8):
			var diameter: float = 7.0 + float((row + column) % 3) * 3.0
			var dot := Panel.new()
			dot.name = "BossSplashDot_%d_%d" % [row, column]
			dot.position = Vector2(
				827.0 + float(column) * 53.0 + float(row) * 4.0,
				112.0 + float(row) * 49.0)
			dot.size = Vector2.ONE * diameter
			dot.mouse_filter = Control.MOUSE_FILTER_IGNORE
			var style := StyleBoxFlat.new()
			style.bg_color = Color(1.0, 0.87, 0.48, 0.27)
			style.set_corner_radius_all(12)
			dot.add_theme_stylebox_override("panel", style)
			_stage.add_child(dot)


func _build_dust_cloud() -> void:
	var cloud_centers: Array[Vector2] = [
		Vector2(168.0, 423.0), Vector2(229.0, 350.0),
		Vector2(323.0, 326.0), Vector2(415.0, 354.0),
		Vector2(493.0, 426.0), Vector2(419.0, 515.0),
		Vector2(298.0, 545.0), Vector2(188.0, 512.0),
	]
	var cloud_sizes: Array[float] = [152.0, 174.0, 184.0, 176.0, 152.0, 174.0, 184.0, 164.0]
	for index: int in cloud_centers.size():
		_add_circle(
			"BossSplashDustCloud_%d" % index,
			cloud_centers[index], cloud_sizes[index],
			Color(0.83, 0.72, 0.98, 0.82),
			Color(0.15, 0.07, 0.35, 0.94), 7)
	for index: int in range(9):
		var angle: float = float(index) * TAU / 9.0 + 0.18
		var center := Vector2(338.0, 432.0) + Vector2(cos(angle) * 255.0, sin(angle) * 190.0)
		_add_circle(
			"BossSplashDustPearl_%d" % index,
			center, 18.0 + float(index % 2) * 7.0,
			Color(1.0, 0.93, 0.73, 0.96),
			Color(0.25, 0.10, 0.48, 0.90), 3)

	_boss_shadow = Panel.new()
	_boss_shadow.name = "BossSplashGroundShadow"
	_boss_shadow.position = Vector2(142.0, 594.0)
	_boss_shadow.size = Vector2(394.0, 54.0)
	_boss_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var shadow_style := StyleBoxFlat.new()
	shadow_style.bg_color = Color(0.04, 0.02, 0.14, 0.64)
	shadow_style.set_corner_radius_all(28)
	_boss_shadow.add_theme_stylebox_override("panel", shadow_style)
	_stage.add_child(_boss_shadow)


func _build_character() -> void:
	_boss_anchor = Node2D.new()
	_boss_anchor.name = "BossSplashCharacterAnchor"
	_boss_anchor.position = _base_boss_position
	_stage.add_child(_boss_anchor)

	_boss = AnimatedSprite2D.new()
	_boss.name = "BossSplashCharacter"
	_boss.sprite_frames = _boss_frames if _boss_frames != null else SpriteFrames.new()
	_boss.scale = Vector2.ONE * 1.04
	_boss_anchor.add_child(_boss)

	_badge_halo = Panel.new()
	_badge_halo.name = "BossSplashVulnerabilityHalo"
	_badge_halo.position = Vector2(-98.0, -344.0)
	_badge_halo.size = Vector2.ONE * 196.0
	_badge_halo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_badge_halo.visible = false
	var halo_style := StyleBoxFlat.new()
	halo_style.bg_color = Color(1.0, 0.84, 0.30, 0.19)
	halo_style.border_color = Color(1.0, 0.95, 0.63, 0.62)
	halo_style.set_border_width_all(6)
	halo_style.set_corner_radius_all(98)
	_badge_halo.add_theme_stylebox_override("panel", halo_style)
	_boss_anchor.add_child(_badge_halo)

	_badge = Sprite2D.new()
	_badge.name = "BossSplashVulnerabilityFlash"
	_badge.texture = _badge_texture
	_badge.position = Vector2(0.0, -246.0)
	_badge.visible = false
	_badge.modulate = Color(1.0, 0.92, 0.45, 0.0)
	if _badge_texture != null:
		var badge_edge: float = maxf(1.0, float(maxi(
			_badge_texture.get_width(), _badge_texture.get_height())))
		_badge.scale = Vector2.ONE * (132.0 / badge_edge)
	_boss_anchor.add_child(_badge)

	for index: int in range(10):
		var flare := Label.new()
		flare.name = "BossSplashFlare_%d" % index
		flare.text = "✦" if index % 2 == 0 else "◆"
		var angle: float = TAU * float(index) / 10.0
		flare.position = Vector2(
			-28.0 + cos(angle) * 150.0,
			-274.0 + sin(angle) * 116.0)
		flare.size = Vector2(56.0, 56.0)
		flare.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		flare.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		flare.mouse_filter = Control.MOUSE_FILTER_IGNORE
		flare.modulate.a = 0.0
		StorybookUI.style_label(flare, 34 if index % 2 == 0 else 25, GOLD, 3)
		flare.add_theme_color_override("font_outline_color", INK)
		_boss_anchor.add_child(flare)
		_flare_labels.append(flare)


func _build_title() -> void:
	_intro_ribbon = Control.new()
	_intro_ribbon.name = "BossSplashIntroRibbon"
	_intro_ribbon.position = Vector2(762.0, 52.0)
	_intro_ribbon.size = Vector2(414.0, 74.0)
	_intro_ribbon.rotation_degrees = -5.0
	_intro_ribbon.pivot_offset = _intro_ribbon.size * 0.5
	_stage.add_child(_intro_ribbon)
	var ribbon_shadow := _make_panel(
		_intro_ribbon, Rect2(9.0, 10.0, 405.0, 62.0), INK, INK, 19, 0)
	ribbon_shadow.name = "BossSplashRibbonShadow"
	var ribbon := _make_panel(
		_intro_ribbon, Rect2(0.0, 0.0, 405.0, 62.0), GOLD, CREAM, 19, 5)
	ribbon.name = "BossSplashRibbon"
	var intro := _make_label(
		ribbon, "BossSplashIntro", "✦  A BOSS APPEARS!  ✦",
		Rect2(11.0, 4.0, 383.0, 52.0), 28, INK, 0)
	intro.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	intro.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

	_title_panel = Control.new()
	_title_panel.name = "BossSplashTitleSlab"
	_title_panel.position = Vector2(663.0, 183.0)
	_title_panel.size = Vector2(560.0, 422.0)
	_title_panel.rotation_degrees = -5.0
	_title_panel.pivot_offset = _title_panel.size * 0.5
	_stage.add_child(_title_panel)

	var kind_shadow := _make_label(
		_title_panel, "BossSplashKindShadow", "✦  " + _boss_kind + "  ✦",
		Rect2(22.0, 18.0, 520.0, 56.0), 27, INK, 7)
	kind_shadow.add_theme_color_override("font_outline_color", INK)
	kind_shadow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	kind_shadow.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	var kind := _make_label(
		_title_panel, "BossSplashKind", "✦  " + _boss_kind + "  ✦",
		Rect2(14.0, 10.0, 520.0, 56.0), 27, CREAM, 5)
	kind.add_theme_color_override("font_outline_color", PLUM)
	kind.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	kind.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

	var name_words: PackedStringArray = _boss_name.split(" ", false, 1)
	var top_word: String = name_words[0] if not name_words.is_empty() else _boss_name
	var bottom_word: String = name_words[1] if name_words.size() > 1 else ""
	_add_display_word(top_word, Rect2(9.0, 67.0, 531.0, 142.0), 106, CREAM)
	if bottom_word != "":
		_add_display_word(bottom_word, Rect2(65.0, 180.0, 482.0, 170.0), 139, GOLD)

	var tell_shadow := _make_panel(
		_title_panel, Rect2(139.0, 356.0, 354.0, 64.0), INK, INK, 25, 0)
	tell_shadow.position += Vector2(8.0, 9.0)
	var tell_panel := _make_panel(
		_title_panel, Rect2(139.0, 356.0, 354.0, 64.0), AQUA, Color(0.10, 0.05, 0.27, 0.94), 25, 5)
	var tell := _make_label(
		tell_panel, "BossSplashTell", "👆   ★   👆",
		Rect2(8.0, 1.0, 338.0, 58.0), 37, GOLD, 2)
	tell.add_theme_color_override("font_outline_color", INK)
	tell.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	tell.vertical_alignment = VERTICAL_ALIGNMENT_CENTER


func _build_frame() -> void:
	_add_polygon("BossSplashTopInk", PackedVector2Array([
		Vector2.ZERO, Vector2(1280.0, 0.0),
		Vector2(1280.0, 13.0), Vector2(0.0, 13.0)]), INK)
	_add_polygon("BossSplashBottomInk", PackedVector2Array([
		Vector2(0.0, 707.0), Vector2(1280.0, 707.0),
		Vector2(1280.0, 720.0), Vector2(0.0, 720.0)]), INK)
	_add_polygon("BossSplashLeftInk", PackedVector2Array([
		Vector2.ZERO, Vector2(13.0, 0.0),
		Vector2(13.0, 720.0), Vector2(0.0, 720.0)]), INK)
	_add_polygon("BossSplashRightInk", PackedVector2Array([
		Vector2(1267.0, 0.0), Vector2(1280.0, 0.0),
		Vector2(1280.0, 720.0), Vector2(1267.0, 720.0)]), INK)


func _add_display_word(
		word: String, rect: Rect2, font_size: int, fill: Color) -> void:
	var shadow := _make_label(
		_title_panel, "BossSplashNameShadow_" + word, word,
		Rect2(rect.position + Vector2(12.0, 14.0), rect.size),
		font_size, INK, 16)
	shadow.add_theme_color_override("font_outline_color", INK)
	shadow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	shadow.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	var title := _make_label(
		_title_panel, "BossSplashName_" + word, word, rect,
		font_size, fill, 13)
	title.add_theme_color_override("font_outline_color", INK)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER


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
		parent: Node, rect: Rect2, accent: Color, fill: Color,
		radius: int, border_width: int) -> Panel:
	var panel := Panel.new()
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


func _add_circle(
		node_name: String, center: Vector2, diameter: float,
		fill: Color, border: Color, border_width: int) -> Panel:
	var circle := Panel.new()
	circle.name = node_name
	circle.position = center - Vector2.ONE * diameter * 0.5
	circle.size = Vector2.ONE * diameter
	circle.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = border
	style.set_border_width_all(border_width)
	style.set_corner_radius_all(int(diameter * 0.5))
	circle.add_theme_stylebox_override("panel", style)
	_stage.add_child(circle)
	return circle


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
	var reveal: float = smoothstep(0.0, 1.0, clampf(_elapsed / 0.16, 0.0, 1.0))
	var exit_alpha: float = 1.0
	if _elapsed >= EXIT_START:
		exit_alpha = 1.0 - smoothstep(0.0, 1.0,
			clampf((_elapsed - EXIT_START) / (TOTAL_TIME - EXIT_START), 0.0, 1.0))
	_root.modulate.a = minf(reveal, exit_alpha)

	var title_progress: float = smoothstep(0.0, 1.0,
		clampf((_elapsed - 0.30) / 0.50, 0.0, 1.0))
	if _title_panel != null:
		_title_panel.position.x = lerpf(1275.0, 663.0, title_progress)
		_title_panel.scale = Vector2.ONE * lerpf(0.82, 1.0, title_progress)
	if _intro_ribbon != null:
		var ribbon_progress: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 0.08) / 0.40, 0.0, 1.0))
		_intro_ribbon.position.y = lerpf(-90.0, 52.0, ribbon_progress)

	if _boss_anchor != null:
		if _elapsed < GRIN_START:
			var jump_progress: float = clampf(
				(_elapsed - JUMP_START) / (GRIN_START - JUMP_START), 0.0, 1.0)
			_boss_anchor.position = _base_boss_position + Vector2(
				lerpf(-148.0, 0.0, jump_progress),
				-sin(jump_progress * PI) * 168.0)
			var squash: float = sin(jump_progress * PI)
			_boss_anchor.scale = Vector2(1.0 - squash * 0.06, 1.0 + squash * 0.08)
			if _boss_shadow != null:
				_boss_shadow.scale = Vector2(1.0 - squash * 0.42, 1.0 - squash * 0.20)
				_boss_shadow.modulate.a = 1.0 - squash * 0.48
		else:
			_boss_anchor.position = _base_boss_position
			_boss_anchor.scale = Vector2.ONE
			if _boss_shadow != null:
				_boss_shadow.scale = Vector2.ONE
				_boss_shadow.modulate.a = 1.0
			if not _grin_started:
				_grin_started = true
				_play_if_available(&"laugh_vulnerable")

	var flashing: bool = _elapsed >= FLASH_START and _elapsed < EXIT_START
	var strobe: float = 0.5 + 0.5 * sin((_elapsed - FLASH_START) * 22.0)
	if _badge != null:
		_badge.visible = flashing and _badge.texture != null
		if flashing:
			_badge.modulate = Color(1.0, 0.92, 0.45, 0.55 + 0.45 * strobe)
			var authored_scale := Vector2.ONE
			if _badge.texture != null:
				var badge_edge: float = maxf(1.0, float(maxi(
					_badge.texture.get_width(), _badge.texture.get_height())))
				authored_scale = Vector2.ONE * (132.0 / badge_edge)
			_badge.scale = authored_scale * (1.35 + 0.35 * strobe)
	if _badge_halo != null:
		_badge_halo.visible = flashing
		if flashing:
			_badge_halo.modulate.a = 0.38 + strobe * 0.55
			var halo_scale: float = 0.78 + strobe * 0.34
			_badge_halo.scale = Vector2.ONE * halo_scale
			_badge_halo.pivot_offset = _badge_halo.size * 0.5
	for index: int in _flare_labels.size():
		var flare: Label = _flare_labels[index]
		var wave: float = 0.5 + 0.5 * sin(
			(_elapsed - FLASH_START) * 8.0 + float(index) * 0.74)
		flare.modulate.a = wave if flashing else 0.0
		flare.scale = Vector2.ONE * (0.72 + wave * 0.42)
	for index: int in _burst_rays.size():
		var ray: Polygon2D = _burst_rays[index]
		var pulse: float = 0.88 + 0.12 * sin(_elapsed * 4.0 + float(index) * 0.6)
		ray.modulate.a = pulse + (strobe * 0.10 if flashing else 0.0)

	if _elapsed >= TOTAL_TIME:
		_complete()


func current_beat() -> String:
	if _elapsed < GRIN_START:
		return "jump"
	if _elapsed < FLASH_START:
		return "grin"
	if _elapsed < EXIT_START:
		return "flash"
	return "exit"


func cancel() -> void:
	if _done:
		return
	_done = true
	queue_free()


func _complete() -> void:
	if _done:
		return
	_done = true
	finished.emit()
	queue_free()


func _play_if_available(animation: StringName) -> void:
	if _boss == null or _boss.sprite_frames == null \
			or not _boss.sprite_frames.has_animation(animation):
		return
	_boss.play(animation)
