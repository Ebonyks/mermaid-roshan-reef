class_name BossSplash2D
extends CanvasLayer

## Reusable picture-first boss introduction. The scene backdrop and accepted
## character frames remain authoritative; the splash only teaches the shared
## anticipation -> weak marker -> tap sequence.

signal finished

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const JUMP_START := 0.12
const IDENTITY_START := 0.96
const FLASH_START := 1.42
const EXIT_START := 2.86
const TOTAL_TIME := 3.24
const INK := Color("#302854")
const PAPER := Color(0.97, 0.96, 1.0, 0.92)
const GOLD := Color("#FFC94A")
const GHOST_HAND := preload("res://assets/castle/training/ghost_hand.png")

var _boss_frames: SpriteFrames
var _boss_name := "BOSS"
var _badge_texture: Texture2D
var _scene_backdrop: Texture2D
var _animation_ids: Dictionary = {
	"entrance": &"jump",
	"identity": &"laugh_vulnerable",
	"vulnerable": &"laugh_vulnerable",
}
var _elapsed := 0.0
var _done := false
var _identity_started := false
var _vulnerable_started := false
var _root: Control
var _stage: Control
var _boss: AnimatedSprite2D
var _boss_anchor: Node2D
var _boss_shadow: Panel
var _badge: Sprite2D
var _badge_halo: Panel
var _hand: TextureRect
var _name_card: Control
var _base_boss_position := Vector2(640.0, 500.0)


func configure(
		boss_frames: SpriteFrames,
		boss_name: String,
		_boss_kind: String,
		badge_texture: Texture2D,
		scene_backdrop: Texture2D = null,
		animation_ids: Dictionary = {}) -> void:
	_boss_frames = boss_frames
	_boss_name = boss_name
	_badge_texture = badge_texture
	_scene_backdrop = scene_backdrop
	for key: Variant in animation_ids.keys():
		_animation_ids[key] = animation_ids[key]


func _ready() -> void:
	name = "BossSplash2D"
	layer = 42
	process_mode = Node.PROCESS_MODE_PAUSABLE
	_build_ui()
	_play_role("entrance")


func _build_ui() -> void:
	_root = Control.new()
	_root.name = "BossSplashRoot"
	_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_root)
	_stage = StorybookUI.add_stage(_root, get_viewport().get_visible_rect().size)
	_stage.name = "BossSplashStage"
	_stage.mouse_filter = Control.MOUSE_FILTER_STOP
	_build_backdrop()
	_build_character()
	_build_name()


func _build_backdrop() -> void:
	var field := TextureRect.new()
	field.name = "BossSplashSceneBackdrop"
	field.position = Vector2.ZERO
	field.size = CANVAS_SIZE
	field.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	field.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	field.texture = _scene_backdrop
	field.modulate = Color(0.78, 0.80, 0.90) if _scene_backdrop != null \
		else Color(0.58, 0.62, 0.78)
	field.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(field)
	if _scene_backdrop == null:
		var fallback := ColorRect.new()
		fallback.name = "BossSplashFallbackField"
		fallback.position = Vector2.ZERO
		fallback.size = CANVAS_SIZE
		fallback.color = Color("#BFCBE0")
		fallback.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_stage.add_child(fallback)
	var veil := ColorRect.new()
	veil.name = "BossSplashQuietVeil"
	veil.position = Vector2.ZERO
	veil.size = CANVAS_SIZE
	veil.color = Color(0.92, 0.91, 1.0, 0.20)
	veil.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_stage.add_child(veil)


func _build_character() -> void:
	_boss_shadow = Panel.new()
	_boss_shadow.name = "BossSplashGroundShadow"
	_boss_shadow.position = Vector2(466.0, 600.0)
	_boss_shadow.size = Vector2(348.0, 44.0)
	_boss_shadow.pivot_offset = _boss_shadow.size * 0.5
	_boss_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var shadow_style := StyleBoxFlat.new()
	shadow_style.bg_color = Color(0.20, 0.18, 0.38, 0.22)
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
	_boss.scale = Vector2.ONE * 1.10
	_boss_anchor.add_child(_boss)
	_badge_halo = Panel.new()
	_badge_halo.name = "BossSplashVulnerabilityHalo"
	_badge_halo.position = Vector2(-70.0, -314.0)
	_badge_halo.size = Vector2.ONE * 140.0
	_badge_halo.pivot_offset = _badge_halo.size * 0.5
	_badge_halo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var halo_style := StyleBoxFlat.new()
	halo_style.bg_color = Color(1.0, 0.82, 0.24, 0.28)
	halo_style.set_corner_radius_all(70)
	_badge_halo.add_theme_stylebox_override("panel", halo_style)
	_badge_halo.visible = false
	_boss_anchor.add_child(_badge_halo)
	_badge = Sprite2D.new()
	_badge.name = "BossSplashVulnerabilityFlash"
	_badge.texture = _badge_texture
	_badge.position = Vector2(0.0, -244.0)
	_badge.visible = false
	_badge.scale = _badge_scale()
	_boss_anchor.add_child(_badge)
	_hand = TextureRect.new()
	_hand.name = "BossSplashTapHand"
	_hand.texture = GHOST_HAND
	_hand.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hand.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_hand.position = Vector2(-42.0, -382.0)
	_hand.size = Vector2(84.0, 84.0)
	_hand.pivot_offset = _hand.size * 0.5
	_hand.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hand.visible = false
	_boss_anchor.add_child(_hand)


func _build_name() -> void:
	_name_card = Control.new()
	_name_card.name = "BossSplashNameCard"
	_name_card.position = Vector2(440.0, 46.0)
	_name_card.size = Vector2(400.0, 70.0)
	_name_card.pivot_offset = _name_card.size * 0.5
	_stage.add_child(_name_card)
	var panel := StorybookUI.add_panel(_name_card,
		Rect2(Vector2.ZERO, _name_card.size), INK, PAPER, 35)
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var label := Label.new()
	label.name = "BossSplashName"
	label.text = _boss_name
	label.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(label, 34, INK, 2)
	panel.add_child(label)


func _process(delta: float) -> void:
	if _done or _root == null:
		return
	_elapsed += delta
	var reveal: float = smoothstep(0.0, 1.0, clampf(_elapsed / 0.16, 0.0, 1.0))
	var exit_alpha := 1.0
	if _elapsed >= EXIT_START:
		exit_alpha = 1.0 - smoothstep(0.0, 1.0,
			clampf((_elapsed - EXIT_START) / (TOTAL_TIME - EXIT_START), 0.0, 1.0))
	_root.modulate.a = minf(reveal, exit_alpha)
	if _name_card != null:
		var name_progress: float = smoothstep(0.0, 1.0,
			clampf((_elapsed - 0.22) / 0.42, 0.0, 1.0))
		_name_card.modulate.a = name_progress
		_name_card.scale = Vector2.ONE * lerpf(0.92, 1.0, name_progress)
	if _boss_anchor != null:
		_animate_boss()
	var flashing: bool = _elapsed >= FLASH_START and _elapsed < EXIT_START
	var pulse: float = 0.5 + 0.5 * sin((_elapsed - FLASH_START) * 8.0)
	if flashing and not _vulnerable_started:
		_vulnerable_started = true
		_play_role("vulnerable")
	if _badge != null:
		_badge.visible = flashing and _badge.texture != null
		_badge.modulate = Color(1.0, 0.94, 0.52, 0.76 + pulse * 0.24)
		_badge.scale = _badge_scale() * (1.10 + pulse * 0.18)
	if _badge_halo != null:
		_badge_halo.visible = flashing
		_badge_halo.scale = Vector2.ONE * (0.88 + pulse * 0.18)
	if _hand != null:
		_hand.visible = flashing
		_hand.position.y = -390.0 + pulse * 28.0
	if _elapsed >= TOTAL_TIME:
		_complete()


func _animate_boss() -> void:
	if _elapsed < IDENTITY_START:
		var progress: float = clampf(
			(_elapsed - JUMP_START) / (IDENTITY_START - JUMP_START), 0.0, 1.0)
		_boss_anchor.position = _base_boss_position + Vector2(
			lerpf(-90.0, 0.0, progress), -sin(progress * PI) * 126.0)
		var squash: float = sin(progress * PI)
		_boss_anchor.scale = Vector2(1.0 - squash * 0.05, 1.0 + squash * 0.07)
		_boss_shadow.scale = Vector2(1.0 - squash * 0.34, 1.0 - squash * 0.18)
		_boss_shadow.modulate.a = 1.0 - squash * 0.44
		return
	_boss_anchor.position = _base_boss_position
	_boss_anchor.scale = Vector2.ONE
	_boss_shadow.scale = Vector2.ONE
	_boss_shadow.modulate.a = 1.0
	if not _identity_started:
		_identity_started = true
		_play_role("identity")


func _badge_scale() -> Vector2:
	if _badge_texture == null:
		return Vector2.ONE
	var edge: float = maxf(1.0, float(maxi(
		_badge_texture.get_width(), _badge_texture.get_height())))
	return Vector2.ONE * (74.0 / edge)


func _play_role(role: String) -> void:
	if _boss == null or _boss.sprite_frames == null:
		return
	var animation := StringName(_animation_ids.get(role, &"idle"))
	if _boss.sprite_frames.has_animation(animation):
		_boss.play(animation)


func current_beat() -> String:
	if _elapsed < IDENTITY_START:
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
