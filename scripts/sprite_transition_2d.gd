class_name SpriteTransition2D
extends Node
# Canvas-only temporal smoothing for authored Sprite2D atlas frames.
#
# The target keeps the newly selected authored frame while one reusable child
# card holds the prior frame.  Their alpha weights cross over at display rate,
# so a four-frame source can present two-to-four meaningful intermediate visual
# states without generating textures, allocating Tweens, or changing gameplay
# timing.  Both endpoints remain the exact approved source pixels.

signal transition_started
signal transition_finished(render_samples: int)

const MIN_SMOOTHNESS_MULTIPLIER := 2
const MAX_SMOOTHNESS_MULTIPLIER := 4
const DEFAULT_SMOOTHNESS_MULTIPLIER := 3
const MIN_TRANSITION_SECONDS := 1.0 / 120.0
const MAX_TRANSITION_SECONDS := 0.10

var _target: Sprite2D = null
var _ghost: Sprite2D = null
var _smoothness_multiplier := DEFAULT_SMOOTHNESS_MULTIPLIER
var _copy_material := true
var _enabled := true
var _captured := false
var _active := false
var _elapsed := 0.0
var _duration := 0.0
var _render_samples := 0
var _target_base_modulate := Color.WHITE
var _ghost_base_modulate := Color.WHITE
var _motion_hint := Vector2.ZERO


func setup(target: Sprite2D,
		smoothness_multiplier: int = DEFAULT_SMOOTHNESS_MULTIPLIER,
		copy_material: bool = true) -> void:
	_target = target
	_smoothness_multiplier = clampi(smoothness_multiplier,
		MIN_SMOOTHNESS_MULTIPLIER, MAX_SMOOTHNESS_MULTIPLIER)
	_copy_material = copy_material
	_ensure_ghost()
	# Keep the reusable idle ghost a complete Sprite2D card from setup onward.
	# The castle canvas audit walks hidden cards too, and a just-created ghost
	# must not temporarily expose a null texture before the first capture.
	_copy_target_visual_to_ghost()
	set_process(false)
	_set_target_meta(false, 1.0)


func set_smoothing_enabled(enabled: bool) -> void:
	_enabled = enabled
	if not _enabled:
		cancel()


func smoothing_enabled() -> bool:
	return _enabled


func smoothness_multiplier() -> int:
	return _smoothness_multiplier


func is_transition_active() -> bool:
	return _active


func transition_progress() -> float:
	if not _active or _duration <= 0.0:
		return 1.0
	return clampf(_elapsed / _duration, 0.0, 1.0)


func rendered_transition_samples() -> int:
	return _render_samples


func transition_ghost() -> Sprite2D:
	return _ghost


func estimated_intermediate_samples(authored_interval: float,
		render_fps: float = 30.0) -> int:
	var duration := _transition_duration(authored_interval)
	return maxi(1, int(round(duration * maxf(render_fps, 1.0))))


# Capture must run immediately before the caller changes texture, atlas region,
# frame, flip, or anatomical offset.  play_captured() starts the blend after all
# new-frame properties are in place.
func capture() -> void:
	if not _has_target():
		return
	if _active:
		_finish_transition(false)
	_ensure_ghost()
	_copy_target_visual_to_ghost()
	_captured = true


func play_captured(authored_interval: float,
		motion_hint: Vector2 = Vector2.ZERO) -> void:
	if not _captured or not _has_target():
		return
	if not _enabled or authored_interval <= 0.0 \
			or not _target.visible:
		_finish_transition(false)
		return
	_duration = _transition_duration(authored_interval)
	_elapsed = 0.0
	_render_samples = 0
	_motion_hint = motion_hint.limit_length(2.0)
	_target_base_modulate = _target.self_modulate
	_target.self_modulate = _with_alpha(_target_base_modulate, 0.0)
	_ghost.self_modulate = _ghost_base_modulate
	_ghost.position = Vector2.ZERO
	_ghost.visible = true
	_active = true
	_captured = false
	set_process(true)
	_set_target_meta(true, 0.0)
	transition_started.emit()


func transition_to_frame(frame_index: int, authored_interval: float,
		motion_hint: Vector2 = Vector2.ZERO) -> void:
	if not _has_target():
		return
	var frame_count: int = maxi(1, _target.hframes * _target.vframes)
	var safe_frame := clampi(frame_index, 0, frame_count - 1)
	if _target.frame == safe_frame and not _active:
		return
	capture()
	_target.frame = safe_frame
	play_captured(authored_interval, motion_hint)


func snap_to_frame(frame_index: int) -> void:
	if not _has_target():
		return
	cancel()
	var frame_count: int = maxi(1, _target.hframes * _target.vframes)
	_target.frame = clampi(frame_index, 0, frame_count - 1)


func cancel() -> void:
	_finish_transition(false)


func _process(delta: float) -> void:
	if not _has_target():
		set_process(false)
		queue_free()
		return
	if not _active:
		set_process(false)
		return
	_elapsed = minf(_elapsed + maxf(delta, 0.0), _duration)
	var linear_progress := transition_progress()
	# Smoothstep has zero velocity at both approved poses.  It avoids the muddy
	# midpoint linger produced by a linear dissolve while keeping the motion calm.
	var eased_progress := linear_progress * linear_progress \
		* (3.0 - 2.0 * linear_progress)
	_target.self_modulate = _with_alpha(
		_target_base_modulate, _target_base_modulate.a * eased_progress)
	_ghost.self_modulate = _with_alpha(
		_ghost_base_modulate, _ghost_base_modulate.a * (1.0 - eased_progress))
	# Optional two-pixel arc creates directional follow-through without moving
	# either endpoint or touching the gameplay-owned target transform.
	var trail_envelope := 4.0 * eased_progress * (1.0 - eased_progress)
	_ghost.position = -_motion_hint * trail_envelope
	_render_samples += 1
	_set_target_meta(true, eased_progress)
	if _elapsed >= _duration:
		_finish_transition(true)


func _transition_duration(authored_interval: float) -> float:
	var interval := maxf(authored_interval, MIN_TRANSITION_SECONDS)
	var generated_fraction := float(_smoothness_multiplier - 1) \
		/ float(_smoothness_multiplier)
	return clampf(interval * generated_fraction,
		MIN_TRANSITION_SECONDS, MAX_TRANSITION_SECONDS)


func _ensure_ghost() -> void:
	if _ghost != null and is_instance_valid(_ghost):
		return
	_ghost = Sprite2D.new()
	_ghost.name = "TemporalTransitionGhost"
	_ghost.position = Vector2.ZERO
	_ghost.rotation = 0.0
	_ghost.scale = Vector2.ONE
	_ghost.z_as_relative = true
	_ghost.z_index = -1
	_ghost.visible = false
	if _target != null and is_instance_valid(_target):
		_target.add_child(_ghost)


func _copy_target_visual_to_ghost() -> void:
	if not _has_target() or _ghost == null:
		return
	_ghost.texture = _target.texture
	_ghost.centered = _target.centered
	_ghost.offset = _target.offset
	_ghost.flip_h = _target.flip_h
	_ghost.flip_v = _target.flip_v
	_ghost.region_enabled = _target.region_enabled
	_ghost.region_rect = _target.region_rect
	_ghost.hframes = _target.hframes
	_ghost.vframes = _target.vframes
	_ghost.frame = _target.frame
	_ghost.texture_filter = _target.texture_filter
	_ghost.texture_repeat = _target.texture_repeat
	_ghost.material = _target.material if _copy_material else null
	_ghost_base_modulate = _target.self_modulate
	_ghost.self_modulate = _ghost_base_modulate
	_ghost.position = Vector2.ZERO


func _finish_transition(emit_finished: bool) -> void:
	var was_active := _active
	if _target != null and is_instance_valid(_target):
		_target.self_modulate = _target_base_modulate
	if _ghost != null and is_instance_valid(_ghost):
		_ghost.visible = false
		_ghost.position = Vector2.ZERO
	_active = false
	_captured = false
	_elapsed = 0.0
	_duration = 0.0
	_motion_hint = Vector2.ZERO
	set_process(false)
	_set_target_meta(false, 1.0)
	if emit_finished and was_active:
		transition_finished.emit(_render_samples)


func _set_target_meta(active: bool, progress: float) -> void:
	if not _has_target():
		return
	_target.set_meta("sprite_transition_active", active)
	_target.set_meta("sprite_transition_progress", progress)
	_target.set_meta("sprite_smoothness_multiplier", _smoothness_multiplier)
	_target.set_meta("sprite_transition_draws", 2 if active else 1)


func _has_target() -> bool:
	return _target != null and is_instance_valid(_target)


func _with_alpha(color: Color, alpha: float) -> Color:
	return Color(color.r, color.g, color.b, alpha)
