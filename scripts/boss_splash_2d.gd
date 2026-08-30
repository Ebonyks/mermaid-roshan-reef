class_name BossSplash2D
extends CanvasLayer

## Reusable, true-2D boss introduction in Mermaid Roshan's pearl-storybook UI.
##
## Every splash teaches the boss in three picture-first beats: a readable
## entrance action, an identity pose, then the exact gameplay tell. Approved
## character frames and battle tell art remain authoritative. The quiet page,
## shell ornament and restrained saturation keep the boss—not the frame—the
## single focal action.

signal finished

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const JUMP_START := 0.12
const GRIN_START := 0.96
const FLASH_START := 1.42
const EXIT_START := 2.86
const TOTAL_TIME := 3.24
const INK := Color(0.20, 0.18, 0.48, 1.0)
const INK_DEEP := Color(0.12, 0.08, 0.34, 1.0)
const PURPLE := Color(0.43, 0.30, 0.76, 1.0)
const LILAC := Color(0.82, 0.76, 1.0, 1.0)
const PAPER := Color(0.94, 0.98, 1.0, 0.98)
const PAPER_COOL := Color(0.78, 0.95, 0.96, 0.98)
const PEARL := Color(0.97, 0.95, 1.0, 1.0)
const GOLD := Color(1.0, 0.78, 0.30, 1.0)
const CLOUD_TEXTURE := preload(
	"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_family_v7_hd_grade.png")
const SHELL_MOTIF_TEXTURE := preload(
	"res://assets/flats/castle/logo_studio_v2/castle_banner_motif_shell.png")

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
var _badge_halo: TextureRect = null
var _title_panel: Control = null
var _intro_ribbon: Control = null
var _tell_card: Control = null
var _flare_labels: Array[Label] = []
var _base_boss_position := Vector2(348.0, 488.0)


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
	letterbox.color = INK_DEEP
	letterbox.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_root.add_child(letterbox)

	_stage = StorybookUI.add_stage(
		_root, get_viewport().get_visible_rect().size)
	_stage.name = "BossSplashStage"
	_stage.mouse_filter = Control.MOUSE_FILTER_STOP
	_build_backdrop()
	_build_page()
	_build_character()
	_build_title()
	_build_frame()


func _build_backdrop() -> void:
	var field := TextureRect.new()
	field.name = "BossSplashField"
	field.position = Vector2.ZERO
	field.size = CANVAS_SIZE
	field.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	field.texture = _make_linear_gradient_texture([
		Color(0.30, 0.30, 0.57, 1.0),
		Color(0.48, 0.52, 0.73, 1.0),
		Color(0.64, 0.73, 0.82, 1.0),
	])
	field.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(field)

	var clouds := TextureRect.new()
	clouds.name = "BossSplashPaintedClouds"
	clouds.texture = CLOUD_TEXTURE
	clouds.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	clouds.position = Vector2(-42.0, 465.0)
	clouds.size = Vector2(1364.0, 286.0)
	clouds.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	clouds.modulate = Color(0.86, 0.83, 1.0, 0.38)
	clouds.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(clouds)

	var bubble_positions: Array[Vector2] = [
		Vector2(92.0, 106.0), Vector2(166.0, 178.0),
		Vector2(1154.0, 126.0), Vector2(1088.0, 578.0),
		Vector2(1190.0, 520.0), Vector2(86.0, 592.0),
	]
	for index: int in bubble_positions.size():
		StorybookUI.add_pearl(
			_stage, bubble_positions[index], 13.0 + float(index % 3) * 5.0,
			"BossSplashBackdropPearl_%d" % index)


func _build_page() -> void:
	var portrait_glow := TextureRect.new()
	portrait_glow.name = "BossSplashPortraitGlow"
	portrait_glow.position = Vector2(72.0, 112.0)
	portrait_glow.size = Vector2(560.0, 520.0)
	portrait_glow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait_glow.texture = _make_radial_gradient_texture(
		Color(1.0, 0.90, 0.58, 0.38))
	portrait_glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(portrait_glow)
	var title_glow := TextureRect.new()
	title_glow.name = "BossSplashTitleGlow"
	title_glow.position = Vector2(636.0, 120.0)
	title_glow.size = Vector2(594.0, 500.0)
	title_glow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	title_glow.texture = _make_radial_gradient_texture(
		Color(0.94, 0.98, 1.0, 0.55))
	title_glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(title_glow)


func _build_character() -> void:
	_boss_shadow = Panel.new()
	_boss_shadow.name = "BossSplashGroundShadow"
	_boss_shadow.position = Vector2(142.0, 603.0)
	_boss_shadow.size = Vector2(410.0, 48.0)
	_boss_shadow.pivot_offset = _boss_shadow.size * 0.5
	_boss_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var shadow_style := StyleBoxFlat.new()
	shadow_style.bg_color = Color(0.20, 0.26, 0.48, 0.22)
	shadow_style.set_corner_radius_all(24)
	_boss_shadow.add_theme_stylebox_override("panel", shadow_style)
	_stage.add_child(_boss_shadow)

	_boss_anchor = Node2D.new()
	_boss_anchor.name = "BossSplashCharacterAnchor"
	_boss_anchor.position = _base_boss_position
	_stage.add_child(_boss_anchor)

	_boss = AnimatedSprite2D.new()
	_boss.name = "BossSplashCharacter"
	_boss.sprite_frames = _boss_frames if _boss_frames != null else SpriteFrames.new()
	_boss.scale = Vector2.ONE * 0.98
	_boss_anchor.add_child(_boss)

	_badge_halo = TextureRect.new()
	_badge_halo.name = "BossSplashVulnerabilityHalo"
	_badge_halo.position = Vector2(-70.0, -314.0)
	_badge_halo.size = Vector2.ONE * 140.0
	_badge_halo.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_badge_halo.texture = _make_radial_gradient_texture(
		Color(1.0, 0.83, 0.28, 0.54))
	_badge_halo.pivot_offset = _badge_halo.size * 0.5
	_badge_halo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_badge_halo.visible = false
	_boss_anchor.add_child(_badge_halo)

	_badge = Sprite2D.new()
	_badge.name = "BossSplashVulnerabilityFlash"
	_badge.texture = _badge_texture
	_badge.position = Vector2(0.0, -244.0)
	_badge.visible = false
	_badge.modulate = Color(1.0, 0.92, 0.45, 0.0)
	_badge.scale = _badge_authored_scale()
	_boss_anchor.add_child(_badge)

	for index: int in range(6):
		var flare := Label.new()
		flare.name = "BossSplashFlare_%d" % index
		flare.text = "✦" if index % 2 == 0 else "·"
		var angle: float = TAU * float(index) / 6.0 - PI * 0.5
		flare.position = Vector2(
			-20.0 + cos(angle) * 102.0,
			-264.0 + sin(angle) * 78.0)
		flare.size = Vector2(40.0, 40.0)
		flare.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		flare.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		flare.mouse_filter = Control.MOUSE_FILTER_IGNORE
		flare.modulate.a = 0.0
		StorybookUI.style_label(flare, 24 if index % 2 == 0 else 30, GOLD, 2)
		flare.add_theme_color_override("font_outline_color", INK)
		_boss_anchor.add_child(flare)
		_flare_labels.append(flare)


func _build_title() -> void:
	_intro_ribbon = Control.new()
	_intro_ribbon.name = "BossSplashIntroRibbon"
	_intro_ribbon.position = Vector2(744.0, 86.0)
	_intro_ribbon.size = Vector2(370.0, 52.0)
	_intro_ribbon.pivot_offset = _intro_ribbon.size * 0.5
	_stage.add_child(_intro_ribbon)
	var intro_panel := StorybookUI.add_panel(
		_intro_ribbon, Rect2(Vector2.ZERO, _intro_ribbon.size),
		GOLD, Color(0.97, 0.95, 1.0, 0.92), 25)
	intro_panel.name = "BossSplashRibbon"
	intro_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var intro := _make_label(
		intro_panel, "BossSplashIntro", "✦  A BOSS APPEARS  ✦",
		Rect2(10.0, 1.0, 350.0, 45.0), 21, INK, 2)
	intro.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	intro.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

	_title_panel = Control.new()
	_title_panel.name = "BossSplashTitleSlab"
	_title_panel.position = Vector2(690.0, 174.0)
	_title_panel.size = Vector2(470.0, 382.0)
	_title_panel.pivot_offset = _title_panel.size * 0.5
	_stage.add_child(_title_panel)
	var shell := TextureRect.new()
	shell.name = "BossSplashPaintedShellAccent"
	shell.texture = SHELL_MOTIF_TEXTURE
	shell.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	shell.position = Vector2(211.0, -12.0)
	shell.size = Vector2(48.0, 48.0)
	shell.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	shell.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_title_panel.add_child(shell)
	var kind := _make_label(
		_title_panel, "BossSplashKind", _boss_kind,
		Rect2(30.0, 40.0, 410.0, 42.0), 22, PURPLE, 2)
	kind.add_theme_color_override("font_outline_color", Color(0.94, 0.98, 1.0))
	kind.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	kind.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

	var name_words: PackedStringArray = _boss_name.split(" ", false, 1)
	var top_word: String = name_words[0] if not name_words.is_empty() else _boss_name
	var bottom_word: String = name_words[1] if name_words.size() > 1 else ""
	_add_display_word(top_word, Rect2(24.0, 88.0, 422.0, 88.0), 70, INK_DEEP)
	if bottom_word != "":
		_add_display_word(bottom_word, Rect2(24.0, 164.0, 422.0, 94.0), 78, PURPLE)

	_tell_card = Control.new()
	_tell_card.name = "BossSplashTellCard"
	_tell_card.position = Vector2(76.0, 292.0)
	_tell_card.size = Vector2(318.0, 62.0)
	_tell_card.pivot_offset = _tell_card.size * 0.5
	_title_panel.add_child(_tell_card)
	var tell_panel := StorybookUI.add_panel(
		_tell_card, Rect2(Vector2.ZERO, _tell_card.size),
		PURPLE, PAPER_COOL, 30)
	tell_panel.name = "BossSplashTellSurface"
	tell_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var tell := _make_label(
		tell_panel, "BossSplashTell", "☝     ★     ☝",
		Rect2(8.0, 2.0, 302.0, 54.0), 29, GOLD, 2)
	tell.add_theme_color_override("font_outline_color", INK)
	tell.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	tell.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	var rule := Panel.new()
	rule.name = "BossSplashTitleRule"
	rule.position = Vector2(102.0, 276.0)
	rule.size = Vector2(266.0, 3.0)
	rule.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var rule_style := StyleBoxFlat.new()
	rule_style.bg_color = Color(0.43, 0.30, 0.76, 0.34)
	rule_style.set_corner_radius_all(2)
	rule.add_theme_stylebox_override("panel", rule_style)
	_title_panel.add_child(rule)
	StorybookUI.add_pearl(
		_title_panel, Vector2(96.0, 277.5), 11.0, "BossSplashRulePearlLeft")
	StorybookUI.add_pearl(
		_title_panel, Vector2(374.0, 277.5), 11.0, "BossSplashRulePearlRight")
	_intro_ribbon.move_to_front()


func _build_frame() -> void:
	var frame := Panel.new()
	frame.name = "BossSplashFrame"
	frame.position = Vector2(18.0, 18.0)
	frame.size = Vector2(1244.0, 684.0)
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = Color.TRANSPARENT
	style.border_color = INK_DEEP
	style.set_border_width_all(7)
	style.set_corner_radius_all(56)
	frame.add_theme_stylebox_override("panel", style)
	_stage.add_child(frame)


func _add_display_word(
		word: String, rect: Rect2, font_size: int, fill: Color) -> void:
	var title := _make_label(
		_title_panel, "BossSplashName_" + word, word, rect,
		font_size, fill, 7)
	title.add_theme_color_override("font_outline_color", PEARL)
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


func _make_linear_gradient_texture(colors: Array[Color]) -> GradientTexture2D:
	var gradient := Gradient.new()
	gradient.colors = PackedColorArray(colors)
	var texture := GradientTexture2D.new()
	texture.gradient = gradient
	texture.width = int(CANVAS_SIZE.x)
	texture.height = int(CANVAS_SIZE.y)
	texture.fill_from = Vector2(0.5, 0.0)
	texture.fill_to = Vector2(0.5, 1.0)
	return texture


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


func _badge_authored_scale() -> Vector2:
	if _badge_texture == null:
		return Vector2.ONE
	var badge_edge: float = maxf(1.0, float(maxi(
		_badge_texture.get_width(), _badge_texture.get_height())))
	return Vector2.ONE * (74.0 / badge_edge)


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
		_title_panel.scale = Vector2.ONE * lerpf(0.88, 1.0, title_progress)
		_title_panel.modulate.a = title_progress
	if _intro_ribbon != null:
		var ribbon_progress: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 0.08) / 0.40, 0.0, 1.0))
		_intro_ribbon.position.y = lerpf(58.0, 86.0, ribbon_progress)
		_intro_ribbon.modulate.a = ribbon_progress

	if _boss_anchor != null:
		if _elapsed < GRIN_START:
			var jump_progress: float = clampf(
				(_elapsed - JUMP_START) / (GRIN_START - JUMP_START), 0.0, 1.0)
			_boss_anchor.position = _base_boss_position + Vector2(
				lerpf(-118.0, 0.0, jump_progress),
				-sin(jump_progress * PI) * 148.0)
			var squash: float = sin(jump_progress * PI)
			_boss_anchor.scale = Vector2(1.0 - squash * 0.05, 1.0 + squash * 0.07)
			if _boss_shadow != null:
				_boss_shadow.scale = Vector2(1.0 - squash * 0.38, 1.0 - squash * 0.18)
				_boss_shadow.modulate.a = 1.0 - squash * 0.46
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
			_badge.modulate = Color(1.0, 0.92, 0.45, 0.58 + 0.42 * strobe)
			_badge.scale = _badge_authored_scale() * (1.16 + 0.22 * strobe)
	if _badge_halo != null:
		_badge_halo.visible = flashing
		if flashing:
			_badge_halo.modulate.a = 0.38 + strobe * 0.46
			_badge_halo.scale = Vector2.ONE * (0.82 + strobe * 0.22)
	if _tell_card != null:
		_tell_card.modulate = Color.WHITE.lerp(Color(1.0, 0.92, 0.55),
			strobe * 0.16 if flashing else 0.0)
		_tell_card.scale = Vector2.ONE * (1.0 + strobe * 0.025 if flashing else 1.0)
	for index: int in _flare_labels.size():
		var flare: Label = _flare_labels[index]
		var wave: float = 0.5 + 0.5 * sin(
			(_elapsed - FLASH_START) * 8.0 + float(index) * 0.74)
		flare.modulate.a = wave * 0.82 if flashing else 0.0
		flare.scale = Vector2.ONE * (0.78 + wave * 0.26)

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
