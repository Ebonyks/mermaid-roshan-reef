class_name RoshanSpriteLoop
extends Node
# Lightweight always-on atlas player for cutaway modes that use their own
# Roshan standee instead of the primary Player node. Idle and swim are distinct:
# a living breath holds the directional pose while actual travel owns the full
# sixteen-frame swim stroke.

const ANCHORS := preload("res://scripts/roshan_sprite_anchors.gd")
const FRAMES := preload("res://scripts/roshan_sprite_frames.gd")
const TRANSITION_2D := preload("res://scripts/sprite_transition_2d.gd")
const DIRECTIONAL: Texture2D = preload(
	"res://assets/characters/roshan_25d/roshan_directional.png")
const SWIM_FRONT: Texture2D = preload(
	"res://assets/characters/roshan_25d/roshan_swim_front.png")
const SWIM_BACK: Texture2D = preload(
	"res://assets/characters/roshan_25d/roshan_swim_back.png")
const ATLAS_COLUMNS := 4
const DIRECTIONAL_ROWS := 2
const SWIM_ROWS := 4
const SWIM_FRAME_COUNT := 16
const CELL_SIZE := Vector2(256.0, 256.0)
const BASE_SWIM_FPS := 8.0
const MAX_FPS := 12.0
const STOP_SETTLE_SECONDS := 0.10
const SPEED_START_THRESHOLD := 0.15
const IDLE_BREATH_PIXELS := 1.8
const SMOOTHNESS_MULTIPLIER := 3

var _sprite: Sprite3D = null
var _sprite_2d: Sprite2D = null
var _texture_rect: TextureRect = null
var _atlas_texture: AtlasTexture = null
var _motion_node: Node3D = null
var _motion_node_2d: Node2D = null
var _last_position := Vector3.ZERO
var _last_position_2d := Vector2.ZERO
var _has_last_position := false
var _frame_cursor := 0.0
var _displayed_frame := -1
var _back_view := false
var _idle_frame := 0
var _state := "idle"
var _still_seconds := 0.0
var _life_phase := 0.0
var _paused := false
var _base_offset := Vector2.ZERO
var _base_rect_modulate := Color.WHITE
var _target_anchor := Vector2.ZERO
var _transition_2d: Variant = null
var _authored_frame_interval := 1.0 / BASE_SWIM_FPS

func setup_sprite_3d(sprite: Sprite3D, back_view: bool = false,
	motion_node: Node3D = null, idle_frame: int = -1) -> void:
	_sprite = sprite
	_motion_node = motion_node if motion_node != null else sprite
	_back_view = back_view
	_idle_frame = clampi(
		(4 if back_view else 0) if idle_frame < 0 else idle_frame, 0, 7)
	_base_offset = _sprite.offset
	_target_anchor = ANCHORS.anchor("directional", _idle_frame)
	_enter_idle()

func setup_texture_rect(texture_rect: TextureRect,
	back_view: bool = false, idle_frame: int = -1) -> void:
	_texture_rect = texture_rect
	_base_rect_modulate = _texture_rect.modulate
	_back_view = back_view
	_idle_frame = clampi(
		(4 if back_view else 0) if idle_frame < 0 else idle_frame, 0, 7)
	_target_anchor = ANCHORS.anchor("directional", _idle_frame)
	_atlas_texture = AtlasTexture.new()
	_texture_rect.texture = _atlas_texture
	_enter_idle()

func setup_sprite_2d(sprite: Sprite2D, back_view: bool = false,
		motion_node: Node2D = null, idle_frame: int = -1) -> void:
	_sprite_2d = sprite
	_motion_node_2d = motion_node if motion_node != null else sprite
	_back_view = back_view
	_idle_frame = clampi(
		(4 if back_view else 0) if idle_frame < 0 else idle_frame, 0, 7)
	_base_offset = _sprite_2d.offset
	_target_anchor = ANCHORS.anchor("directional", _idle_frame)
	# Establish the exact authored idle before the smoother exists; spawning a
	# Canvas actor must never dissolve in from an empty texture.
	_enter_idle()
	_transition_2d = TRANSITION_2D.new()
	_transition_2d.name = "TemporalSpriteTransition"
	_sprite_2d.add_child(_transition_2d)
	_transition_2d.setup(_sprite_2d, SMOOTHNESS_MULTIPLIER, false)
	_sprite_2d.set_meta("roshan_temporal_smoothing", SMOOTHNESS_MULTIPLIER)

func _process(delta: float) -> void:
	if not _has_target():
		queue_free()
		return
	if _paused:
		return
	var speed: float = _sample_speed(delta)
	var moving: bool = _explicit_moving(speed)
	if moving:
		_still_seconds = 0.0
		if _state != "swim":
			_enter_swim()
	else:
		_still_seconds += delta
		if _state == "swim" and _still_seconds >= STOP_SETTLE_SECONDS:
			_enter_idle()
	_life_phase = fposmod(_life_phase + delta * 1.65, TAU)
	if _state == "swim":
		var fps: float = minf(BASE_SWIM_FPS + speed * 0.25, MAX_FPS)
		_authored_frame_interval = 1.0 / maxf(fps, 1.0)
		_frame_cursor = fposmod(
			_frame_cursor + delta * fps, float(SWIM_FRAME_COUNT))
		_apply_frame(int(floor(_frame_cursor)))
	else:
		_apply_idle_breath()

func set_moving(moving: bool) -> void:
	if _sprite != null and is_instance_valid(_sprite):
		_sprite.set_meta("walking", moving)
	if _sprite_2d != null and is_instance_valid(_sprite_2d):
		_sprite_2d.set_meta("walking", moving)
	if moving:
		_still_seconds = 0.0
		if not _paused and _state != "swim":
			_enter_swim()

func set_paused(paused: bool) -> void:
	_paused = paused
	if not paused:
		_enter_idle()

func animation_state() -> String:
	return _state

func _has_target() -> bool:
	return (_sprite != null and is_instance_valid(_sprite)) \
		or (_sprite_2d != null and is_instance_valid(_sprite_2d)) \
		or (_texture_rect != null and is_instance_valid(_texture_rect))

func _sample_speed(delta: float) -> float:
	if _motion_node_2d != null and is_instance_valid(_motion_node_2d):
		var current_2d := _motion_node_2d.global_position
		if not _has_last_position:
			_last_position_2d = current_2d
			_has_last_position = true
			return 0.0
		var speed_2d := current_2d.distance_to(_last_position_2d) / maxf(delta, 0.001)
		_last_position_2d = current_2d
		return speed_2d
	if _motion_node == null or not is_instance_valid(_motion_node):
		return 0.0
	var current: Vector3 = _motion_node.global_position
	if not _has_last_position:
		_last_position = current
		_has_last_position = true
		return 0.0
	var speed: float = current.distance_to(_last_position) / maxf(delta, 0.001)
	_last_position = current
	return speed

func _explicit_moving(sampled_speed: float) -> bool:
	if _sprite_2d != null and is_instance_valid(_sprite_2d) \
			and _sprite_2d.has_meta("walking"):
		return bool(_sprite_2d.get_meta("walking"))
	if _sprite != null and is_instance_valid(_sprite) \
			and _sprite.has_meta("walking"):
		return bool(_sprite.get_meta("walking"))
	if _motion_node != null and is_instance_valid(_motion_node) \
			and _motion_node.has_meta("walking"):
		return bool(_motion_node.get_meta("walking"))
	return sampled_speed > SPEED_START_THRESHOLD

func _enter_idle() -> void:
	var captured_transition := _capture_canvas_transition()
	_state = "idle"
	_still_seconds = 0.0
	_frame_cursor = 0.0
	_displayed_frame = -1
	_authored_frame_interval = STOP_SETTLE_SECONDS
	_apply_sheet(DIRECTIONAL, DIRECTIONAL_ROWS)
	_apply_frame(_idle_frame, captured_transition)
	_set_state_meta()

func _enter_swim() -> void:
	var captured_transition := _capture_canvas_transition()
	_state = "swim"
	_still_seconds = 0.0
	_frame_cursor = 0.0
	_displayed_frame = -1
	_authored_frame_interval = 1.0 / BASE_SWIM_FPS
	_apply_sheet(SWIM_BACK if _back_view else SWIM_FRONT, SWIM_ROWS)
	_apply_frame(0, captured_transition)
	_set_state_meta()

func _apply_sheet(texture: Texture2D, rows: int) -> void:
	if _sprite != null and is_instance_valid(_sprite):
		_sprite.texture = texture
		_sprite.hframes = ATLAS_COLUMNS
		_sprite.vframes = rows
	if _sprite_2d != null and is_instance_valid(_sprite_2d):
		_sprite_2d.texture = texture
		_sprite_2d.hframes = ATLAS_COLUMNS
		_sprite_2d.vframes = rows
	if _atlas_texture != null:
		_atlas_texture.atlas = texture

func _apply_frame(frame_index: int,
		canvas_transition_captured: bool = false) -> void:
	var frame_count: int = 8 if _state == "idle" else SWIM_FRAME_COUNT
	var safe_frame: int = posmod(frame_index, frame_count)
	if safe_frame == _displayed_frame:
		if _sprite != null and is_instance_valid(_sprite):
			_apply_anchor_offset()
		if _sprite_2d != null and is_instance_valid(_sprite_2d):
			_apply_anchor_offset()
		return
	var should_smooth := canvas_transition_captured
	if not should_smooth:
		should_smooth = _capture_canvas_transition()
	_displayed_frame = safe_frame
	var sheet: String = _sheet_key()
	if _sprite != null and is_instance_valid(_sprite):
		_sprite.frame = safe_frame
		# The sheets pack their figures tighter than the nominal 256px grid;
		# sample the corrected window so the lower rows keep her whole head.
		FRAMES.apply_region(_sprite, sheet, safe_frame, ATLAS_COLUMNS)
		_apply_anchor_offset()
	if _sprite_2d != null and is_instance_valid(_sprite_2d):
		FRAMES.apply_region_2d(_sprite_2d, sheet, safe_frame, ATLAS_COLUMNS)
		_apply_anchor_offset()
		if should_smooth and _transition_2d != null:
			_transition_2d.play_captured(_authored_frame_interval)
	if _atlas_texture != null:
		_atlas_texture.region = FRAMES.region(sheet, safe_frame, ATLAS_COLUMNS)


func _capture_canvas_transition() -> bool:
	if _sprite_2d == null or not is_instance_valid(_sprite_2d) \
			or _transition_2d == null:
		return false
	_transition_2d.capture()
	return true

func _sheet_key() -> String:
	return "directional" if _state == "idle" \
		else "swim_back" if _back_view else "swim_front"

func _apply_anchor_offset() -> void:
	var sheet: String = _sheet_key()
	if _sprite_2d != null and is_instance_valid(_sprite_2d):
		_sprite_2d.offset = _base_offset + ANCHORS.correction(
			sheet, _displayed_frame, _target_anchor, _sprite_2d.flip_h) \
			+ FRAMES.offset_correction(sheet, _displayed_frame, _sprite_2d.flip_h)
		_sprite_2d.set_meta("roshan_anchor_offset", _sprite_2d.offset - _base_offset)
		return
	if _sprite == null or not is_instance_valid(_sprite):
		return
	_sprite.offset = _base_offset + ANCHORS.correction(
		sheet, _displayed_frame, _target_anchor, _sprite.flip_h) \
		+ FRAMES.offset_correction(sheet, _displayed_frame, _sprite.flip_h)
	_sprite.set_meta("roshan_anchor_offset", _sprite.offset - _base_offset)

func _apply_idle_breath() -> void:
	if _sprite_2d != null and is_instance_valid(_sprite_2d):
		_apply_anchor_offset()
		_sprite_2d.offset.y += sin(_life_phase) * IDLE_BREATH_PIXELS
		_sprite_2d.set_meta("roshan_life_phase", _life_phase)
		return
	if _sprite != null and is_instance_valid(_sprite):
		_apply_anchor_offset()
		_sprite.offset.y += sin(_life_phase) * IDLE_BREATH_PIXELS
		_sprite.set_meta("roshan_life_phase", _life_phase)
	if _texture_rect != null and is_instance_valid(_texture_rect):
		var glow: float = 0.985 + (sin(_life_phase) + 1.0) * 0.0075
		_texture_rect.modulate = Color(
			_base_rect_modulate.r * glow,
			_base_rect_modulate.g * glow,
			_base_rect_modulate.b * glow,
			_base_rect_modulate.a)

func _set_state_meta() -> void:
	if _sprite_2d != null and is_instance_valid(_sprite_2d):
		_sprite_2d.set_meta("roshan_animation_state", _state)
		return
	if _sprite != null and is_instance_valid(_sprite):
		_sprite.set_meta("roshan_animation_state", _state)
