class_name DaddySpriteLoop
extends Node
# Shared atlas player for Daddy Mermaid's 2.5D standees. Actions are one-shot
# and always outrank travel; travel resumes after an action, then settles back
# to the quiet idle loop when the owning standee stops.

const IDLE: Texture2D = preload(
	"res://assets/characters/daddy_25d/daddy_idle.png")
const SWIM: Texture2D = preload(
	"res://assets/characters/daddy_25d/daddy_swim.png")
const GESTURES: Texture2D = preload(
	"res://assets/characters/daddy_25d/daddy_gesture_a.png")
const VICTORY: Texture2D = preload(
	"res://assets/characters/daddy_25d/daddy_victory.png")

const ATLAS_COLUMNS := 4
const IDLE_ROWS := 2
const SWIM_ROWS := 4
const GESTURE_ROWS := 4
const VICTORY_ROWS := 2
const IDLE_FRAME_COUNT := 8
const SWIM_FRAME_COUNT := 16
const GESTURE_FRAME_COUNT := 4
const VICTORY_FRAME_COUNT := 8
const IDLE_FPS := 4.0
const SWIM_FPS := 8.0
const GESTURE_FPS := 6.0
const VICTORY_FPS := 8.0
const VICTORY_FINAL_HOLD := 0.30
const STOP_SETTLE_SECONDS := 0.10
const SPEED_START_THRESHOLD := 0.15

const ACTION_NONE := 0
const ACTION_GESTURE := 1
const ACTION_VICTORY := 2

var _sprite: Sprite3D = null
var _motion_node: Node3D = null
var _last_position := Vector3.ZERO
var _has_last_position := false
var _frame_cursor := 0.0
var _displayed_frame := -1
var _state := "idle"
var _still_seconds := 0.0
var _moving_override_enabled := false
var _moving_override := false
var _action_priority := ACTION_NONE
var _action_start_frame := 0
var _action_frame_count := 0
var _action_fps := 0.0
var _action_final_hold := 0.0
var _action_elapsed := 0.0


func setup_sprite_3d(sprite: Sprite3D, motion_node: Node3D = null) -> void:
	_sprite = sprite
	_motion_node = motion_node if motion_node != null else sprite
	_sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	_sprite.shaded = false
	_sprite.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_enter_idle()


func _process(delta: float) -> void:
	if _sprite == null or not is_instance_valid(_sprite):
		queue_free()
		return
	# Combat prebuilds its cameo hidden; avoid even lightweight frame work until
	# the success reveal makes the standee visible.
	if not _sprite.is_visible_in_tree():
		return
	var speed: float = _sample_speed(delta)
	var moving: bool = _moving_override if _moving_override_enabled \
		else speed > SPEED_START_THRESHOLD
	if _action_priority != ACTION_NONE:
		_tick_action(delta, moving)
		return
	if moving:
		_still_seconds = 0.0
		if _state != "swim":
			_enter_swim()
		_frame_cursor = fposmod(
			_frame_cursor + delta * SWIM_FPS, float(SWIM_FRAME_COUNT))
		_apply_frame(int(floor(_frame_cursor)))
	else:
		_still_seconds += delta
		if _state == "swim" and _still_seconds >= STOP_SETTLE_SECONDS:
			_enter_idle()
		if _state == "idle":
			_frame_cursor = fposmod(
				_frame_cursor + delta * IDLE_FPS, float(IDLE_FRAME_COUNT))
			_apply_frame(int(floor(_frame_cursor)))


func set_moving(moving: bool) -> void:
	_moving_override_enabled = true
	_moving_override = moving
	if moving:
		_still_seconds = 0.0


func clear_moving_override() -> void:
	_moving_override_enabled = false


func play_wave() -> void:
	_play_gesture("wave", 0)


func play_invite() -> void:
	_play_gesture("invite", 1)


func play_clap() -> void:
	_play_gesture("clap", 2)


func play_hug() -> void:
	_play_gesture("hug", 3)


func play_victory() -> void:
	_start_action(
		"victory", VICTORY, VICTORY_ROWS, 0, VICTORY_FRAME_COUNT,
		VICTORY_FPS, VICTORY_FINAL_HOLD, ACTION_VICTORY)


func animation_state() -> String:
	return _state


func is_action_playing() -> bool:
	return _action_priority != ACTION_NONE


func _play_gesture(action_name: String, row: int) -> void:
	_start_action(
		action_name, GESTURES, GESTURE_ROWS, row * ATLAS_COLUMNS,
		GESTURE_FRAME_COUNT, GESTURE_FPS, 0.0, ACTION_GESTURE)


func _start_action(action_name: String, texture: Texture2D, rows: int,
	start_frame: int, frame_count: int, fps: float, final_hold: float,
	priority: int) -> void:
	if priority < _action_priority:
		return
	_state = action_name
	_action_priority = priority
	_action_start_frame = start_frame
	_action_frame_count = frame_count
	_action_fps = fps
	_action_final_hold = final_hold
	_action_elapsed = 0.0
	_frame_cursor = 0.0
	_displayed_frame = -1
	_apply_sheet(texture, rows)
	_apply_frame(start_frame)
	_set_state_meta()


func _tick_action(delta: float, moving: bool) -> void:
	_action_elapsed += delta
	var animated_seconds: float = float(_action_frame_count) / _action_fps
	var total_seconds: float = animated_seconds + _action_final_hold
	if _action_elapsed >= total_seconds:
		_action_priority = ACTION_NONE
		if moving:
			_enter_swim()
		else:
			_enter_idle()
		return
	var local_frame: int = mini(
		int(floor(_action_elapsed * _action_fps)), _action_frame_count - 1)
	_apply_frame(_action_start_frame + local_frame)


func _sample_speed(delta: float) -> float:
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


func _enter_idle() -> void:
	_state = "idle"
	_still_seconds = 0.0
	_frame_cursor = 0.0
	_displayed_frame = -1
	_apply_sheet(IDLE, IDLE_ROWS)
	_apply_frame(0)
	_set_state_meta()


func _enter_swim() -> void:
	_state = "swim"
	_still_seconds = 0.0
	_frame_cursor = 0.0
	_displayed_frame = -1
	_apply_sheet(SWIM, SWIM_ROWS)
	_apply_frame(0)
	_set_state_meta()


func _apply_sheet(texture: Texture2D, rows: int) -> void:
	_sprite.texture = texture
	_sprite.hframes = ATLAS_COLUMNS
	_sprite.vframes = rows


func _apply_frame(frame_index: int) -> void:
	if frame_index == _displayed_frame:
		return
	_displayed_frame = frame_index
	_sprite.frame = frame_index
	_sprite.set_meta("daddy_animation_frame", frame_index)


func _set_state_meta() -> void:
	_sprite.set_meta("daddy_animation_state", _state)
