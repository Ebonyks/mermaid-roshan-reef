class_name OperaBalletSurface
extends OperaGestureSurface
## Full-stage, one-finger ballet interactions for Mermaid Roshan's recital.
##
## This specialist deliberately bypasses the generic Opera widget pictures.
## The same geometry that is painted is also used for demonstrations and hit
## testing, so the child never has to reconcile a decorative path with a
## different invisible rule.

const SUPPORTED_MODES: Array[String] = [
	"ballet_pose", "ballet_ribbon", "ballet_twirl",
]
const BALLERINA_ATLAS_PATH := \
	"res://assets/opera/worlds/actors/animation/roshan_ballerina_sheet_a.png"
const MUSIC_BOX_PATH := "res://assets/opera/worlds/props/goal_ballerina.png"
const ATLAS_CELL := Vector2(256.0, 256.0)
const WORK_ROW := 2
## Deliberate port-de-bras phrase: heart/low, open/second, crown/fifth.
## Values are the zero-based atlas columns emitted to the career-world actor.
const POSE_FRAMES: Array[int] = [2, 1, 0]
const POSE_OPTIONS: Array = [
	[2, 0],
	[1, 2, 0],
	[0, 1, 2],
]
const POSE_ROUNDS := 3
const DEMO_SECONDS := 1.55
const DEMO_CUE_SECONDS := 0.12
const FIRST_ASSIST_SECONDS := 5.0
const STRONG_ASSIST_SECONDS := 10.0
const REDRAW_STEP := 0.05
const RIBBON_SAMPLES := 64
const RIBBON_NEAREST_SAMPLES := 64
const RIBBON_MAX_FORWARD_STEP := 0.16
const RIBBON_BASE_WIDTH := 116.0
const RIBBON_COLOR_WIDTH := 88.0
const RIBBON_RESUME_DIAMETER := 128.0
const TWIRL_RING_WIDTH := 116.0
const TWIRL_HANDLE_DIAMETER := 112.0
const TWIRL_MAX_ANGLE_STEP := 0.78

var pose_round: int = 0
var ribbon_progress: float = 0.0
var twirl_progress: float = 0.0
var twirl_direction: int = 0

var _ballerina_atlas: Texture2D = null
var _music_box: Texture2D = null
var _demo_cue_emitted := false
var _ready_emitted := false
var _assist_level := 0
var _stuck_t := 0.0
var _wrong_count := 0
var _elapsed := 0.0
var _redraw_t := 0.0
var _ribbon_engaged := false
var _twirl_engaged := false
var _twirl_previous_angle := 0.0
var _twirl_handle_angle := -PI * 0.5
var _twirl_arc_origin := -PI * 0.5
var _twirl_pose_band := -1


func configure(next_mode: String, next_accent: Color, choice: int = 1,
		next_context: String = "") -> void:
	assert(next_mode in SUPPORTED_MODES,
		"OperaBalletSurface supports only ballet_pose, ballet_ribbon, and ballet_twirl")
	super.configure(next_mode, next_accent, choice, next_context)
	_load_ballet_textures()
	pose_round = 0
	ribbon_progress = 0.0
	twirl_progress = 0.0
	twirl_direction = 0
	_ribbon_engaged = false
	_twirl_engaged = false
	_twirl_previous_angle = 0.0
	_twirl_handle_angle = -PI * 0.5
	_twirl_arc_origin = -PI * 0.5
	_twirl_pose_band = -1
	_assist_level = 0
	_stuck_t = 0.0
	_wrong_count = 0
	_elapsed = 0.0
	_redraw_t = 0.0
	held = false
	input_started = false
	_begin_demo()
	queue_redraw()


func set_fill(value: float) -> void:
	# The career world remains the score/state owner. Synchronization can only
	# bank progress; it may never erase a partially completed child gesture.
	super.set_fill(value)
	var normalized := clampf(value, 0.0, 1.0)
	match mode:
		"ballet_pose":
			var external_round := clampi(floori(normalized * float(POSE_ROUNDS) + 0.001),
				0, POSE_ROUNDS)
			pose_round = maxi(pose_round, external_round)
		"ballet_ribbon":
			ribbon_progress = maxf(ribbon_progress, normalized)
		"ballet_twirl":
			twirl_progress = maxf(twirl_progress, normalized)
	if _mode_complete():
		demo_active = false
	queue_redraw()


func restart_demo() -> void:
	# Re-teach only the unresolved round/path/orbit. Accepted work is banked.
	if completion_accepted or _mode_complete():
		return
	_assist_level = maxi(_assist_level, 1)
	_begin_demo()
	queue_redraw()


func pose_target_frame() -> int:
	return POSE_FRAMES[clampi(pose_round, 0, POSE_FRAMES.size() - 1)]


func pose_option_frames() -> Array[int]:
	var result: Array[int] = []
	var source: Array = POSE_OPTIONS[clampi(pose_round, 0, POSE_OPTIONS.size() - 1)]
	for value: Variant in source:
		result.append(int(value))
	return result


func pose_option_rects() -> Array[Rect2]:
	var frames := pose_option_frames()
	var count := maxi(1, frames.size())
	var gap := 34.0
	var horizontal_margin := 54.0
	var available := size.x - horizontal_margin * 2.0 - gap * float(count - 1)
	var side := clampf(minf(size.y * 0.30, available / float(count)), 180.0, 220.0)
	var total := side * float(count) + gap * float(count - 1)
	var start_x := (size.x - total) * 0.5
	var y := maxf(size.y * 0.62, size.y - side - 24.0)
	var result: Array[Rect2] = []
	for index in range(count):
		result.append(Rect2(Vector2(start_x + float(index) * (side + gap), y),
			Vector2.ONE * side))
	return result


func pose_target_rect() -> Rect2:
	var side := clampf(size.y * 0.36, 220.0, 300.0)
	return Rect2(Vector2((size.x - side) * 0.5, maxf(24.0, size.y * 0.07)),
		Vector2.ONE * side)


func ribbon_point(progress: float) -> Vector2:
	# One authoritative pearl-current curve for paint, demo, and collision.
	var amount := clampf(progress, 0.0, 1.0)
	var margin := maxf(72.0, size.x * 0.075)
	return Vector2(
		lerpf(margin, size.x - margin, amount),
		size.y * (0.52 + sin(amount * TAU) * 0.19)
	)


func ribbon_corridor_width() -> float:
	return RIBBON_BASE_WIDTH + (28.0 if _assist_level >= 2 else 0.0)


func ribbon_resume_rect() -> Rect2:
	var diameter := RIBBON_RESUME_DIAMETER * (1.20 if _assist_level >= 2 else 1.0)
	return Rect2(ribbon_point(ribbon_progress) - Vector2.ONE * diameter * 0.5,
		Vector2.ONE * diameter)


func twirl_center() -> Vector2:
	return Vector2(size.x * 0.66, size.y * 0.50)


func twirl_radius() -> float:
	return clampf(minf(size.x * 0.18, size.y * 0.27), 150.0, 190.0)


func twirl_ring_width() -> float:
	return TWIRL_RING_WIDTH + (30.0 if _assist_level >= 2 else 0.0)


func twirl_handle_position() -> Vector2:
	return twirl_center() + Vector2.from_angle(_twirl_handle_angle) * twirl_radius()


func assist_level() -> int:
	return _assist_level


func _load_ballet_textures() -> void:
	if _ballerina_atlas == null and ResourceLoader.exists(BALLERINA_ATLAS_PATH):
		_ballerina_atlas = load(BALLERINA_ATLAS_PATH) as Texture2D
	if _music_box == null and ResourceLoader.exists(MUSIC_BOX_PATH):
		_music_box = load(MUSIC_BOX_PATH) as Texture2D


func _begin_demo() -> void:
	demo_active = true
	demo_t = 0.0
	_demo_cue_emitted = false
	_ready_emitted = false


func _finish_demo() -> void:
	if not _ready_emitted:
		_ready_emitted = true
		gesture.emit("ballet_ready", 0.0, 1.0)
	demo_active = false
	demo_t = DEMO_SECONDS
	queue_redraw()


func _emit_demo_cue() -> void:
	if _demo_cue_emitted:
		return
	_demo_cue_emitted = true
	match mode:
		"ballet_pose":
			gesture.emit("ballet_pose_cue", float(pose_target_frame()), 1.0)
		"ballet_twirl":
			var band := clampi(floori(twirl_progress * 3.0), 0, POSE_FRAMES.size() - 1)
			_twirl_pose_band = maxi(_twirl_pose_band, band)
			gesture.emit("ballet_pose_cue", float(POSE_FRAMES[band]), 1.0)


func _process(delta: float) -> void:
	_elapsed += maxf(0.0, delta)
	if feedback_t > 0.0:
		feedback_t = maxf(0.0, feedback_t - delta)
	if completion_accepted or _mode_complete() or armed_only:
		_redraw_t += delta
		if _redraw_t >= REDRAW_STEP:
			_redraw_t = 0.0
			queue_redraw()
		return

	_stuck_t += maxf(0.0, delta)
	if _stuck_t >= STRONG_ASSIST_SECONDS and _assist_level < 2:
		_assist_level = 2
		_begin_demo()
	elif _stuck_t >= FIRST_ASSIST_SECONDS and _assist_level < 1:
		_assist_level = 1
		_begin_demo()

	if demo_active:
		demo_t += maxf(0.0, delta)
		if demo_t >= DEMO_CUE_SECONDS:
			_emit_demo_cue()
		if demo_t >= DEMO_SECONDS:
			_finish_demo()

	_redraw_t += maxf(0.0, delta)
	if _redraw_t >= REDRAW_STEP:
		_redraw_t = 0.0
		queue_redraw()


func _mode_complete() -> bool:
	match mode:
		"ballet_pose":
			return pose_round >= POSE_ROUNDS
		"ballet_ribbon":
			return ribbon_progress >= 0.999
		"ballet_twirl":
			return twirl_progress >= 0.999
	return false


func _note_meaningful_progress() -> void:
	_stuck_t = 0.0
	_wrong_count = 0
	_assist_level = 0
	input_started = true
	demo_active = false


func _note_wrong(kind: String, at: Vector2, replay_demo: bool) -> void:
	feedback_positive = false
	feedback_t = 0.34
	feedback_anchor = at
	_wrong_count += 1
	gesture.emit(kind, 0.0, 0.32)
	if _wrong_count >= 2:
		_assist_level = maxi(_assist_level, 1)
	if replay_demo:
		_begin_demo()
	queue_redraw()


func _input_blocked() -> bool:
	return armed_only or completion_accepted or _mode_complete() \
		or (mode == "ballet_pose" and demo_active)


func _prepare_real_input() -> bool:
	if _input_blocked():
		return false
	if demo_active:
		# Ribbon and twirl remain interruptible: touching the demonstrated object
		# immediately hands control to the child without waiting out the ghost.
		_finish_demo()
	input_started = true
	return true


func _press(at: Vector2) -> void:
	if not _prepare_real_input():
		return
	held = true
	pointer_pos = at
	previous_pos = at
	match mode:
		"ballet_pose":
			_pose_press(at)
		"ballet_ribbon":
			_ribbon_press(at)
		"ballet_twirl":
			_twirl_press(at)
	queue_redraw()


func _drag(at: Vector2) -> void:
	if not held or armed_only or completion_accepted or _mode_complete():
		return
	pointer_pos = at
	match mode:
		"ballet_ribbon":
			_ribbon_drag(at)
		"ballet_twirl":
			_twirl_drag(at)
	previous_pos = at
	queue_redraw()


func _release(at: Vector2) -> void:
	var was_ribbon_engaged := _ribbon_engaged
	var was_twirl_engaged := _twirl_engaged
	held = false
	pointer_pos = at
	_ribbon_engaged = false
	_twirl_engaged = false
	if completion_accepted or _mode_complete():
		queue_redraw()
		return
	if mode == "ballet_ribbon" and was_ribbon_engaged:
		gesture.emit("ballet_ribbon", 0.0, 0.72)
		_begin_demo()
	elif mode == "ballet_twirl" and was_twirl_engaged:
		gesture.emit("ballet_twirl", 0.0, 0.72)
		_begin_demo()
	queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_press(touch.position)
		else:
			_release(touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		_drag((event as InputEventScreenDrag).position)
		accept_event()
	elif event is InputEventMouseButton \
			and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		var button := event as InputEventMouseButton
		if button.device == InputEvent.DEVICE_ID_EMULATION:
			return
		if button.pressed:
			_press(button.position)
		else:
			_release(button.position)
		accept_event()
	elif event is InputEventMouseMotion and held:
		var motion := event as InputEventMouseMotion
		if motion.device == InputEvent.DEVICE_ID_EMULATION:
			return
		_drag(motion.position)
		accept_event()


func _pose_press(at: Vector2) -> void:
	var frames := pose_option_frames()
	var rects := pose_option_rects()
	var target := pose_target_frame()
	for index in range(rects.size()):
		var hit_rect: Rect2 = rects[index]
		if int(frames[index]) == target and _assist_level >= 2:
			hit_rect = hit_rect.grow(hit_rect.size.x * 0.10)
		if not hit_rect.has_point(at):
			continue
		if int(frames[index]) != target:
			_note_wrong("ballet_pose", at, true)
			return
		pose_round += 1
		_note_meaningful_progress()
		feedback_positive = true
		feedback_t = 0.42
		feedback_anchor = hit_rect.get_center()
		gesture.emit("ballet_pose", 1.0, 1.0)
		if pose_round < POSE_ROUNDS:
			_begin_demo()
		queue_redraw()
		return
	_note_wrong("ballet_pose", at, true)


func _ribbon_press(at: Vector2) -> void:
	_ribbon_engaged = ribbon_resume_rect().has_point(at)
	if not _ribbon_engaged:
		_note_wrong("ballet_ribbon", at, true)
		return
	previous_pos = at
	feedback_anchor = at


func _ribbon_drag(at: Vector2) -> void:
	if not _ribbon_engaged:
		return
	var travel := previous_pos.distance_to(at)
	var input_samples := clampi(ceili(travel / 28.0), 1, 14)
	var candidate := ribbon_progress
	for sample_index in range(1, input_samples + 1):
		var sample := previous_pos.lerp(at, float(sample_index) / float(input_samples))
		var nearest := _ribbon_nearest(sample, candidate)
		var nearest_progress := nearest.x
		var nearest_distance := nearest.y
		if nearest_distance <= ribbon_corridor_width() * 0.5 \
				and nearest_progress > candidate + 0.0005 \
				and nearest_progress <= candidate + RIBBON_MAX_FORWARD_STEP:
			candidate = nearest_progress
	if candidate <= ribbon_progress + 0.0005:
		if travel >= 18.0:
			_note_wrong("ballet_ribbon", at, false)
		return
	var delta := minf(1.0, candidate) - ribbon_progress
	ribbon_progress = minf(1.0, candidate)
	widget_fill = ribbon_progress
	_note_meaningful_progress()
	feedback_positive = true
	feedback_t = 0.22
	feedback_anchor = ribbon_point(ribbon_progress)
	gesture.emit("ballet_ribbon", delta, 1.0)


func _ribbon_nearest(at: Vector2, floor_progress: float) -> Vector2:
	var start := maxf(0.0, floor_progress - 0.025)
	var best_progress := start
	var best_distance := INF
	var previous_t := start
	var previous_curve := ribbon_point(start)
	for index in range(1, RIBBON_NEAREST_SAMPLES + 1):
		var amount := lerpf(start, 1.0, float(index) / float(RIBBON_NEAREST_SAMPLES))
		var curve := ribbon_point(amount)
		var closest := Geometry2D.get_closest_point_to_segment(at, previous_curve, curve)
		var distance := at.distance_to(closest)
		if distance < best_distance:
			var segment_length := previous_curve.distance_to(curve)
			var segment_amount := 0.0
			if segment_length > 0.001:
				segment_amount = previous_curve.distance_to(closest) / segment_length
			best_progress = lerpf(previous_t, amount, clampf(segment_amount, 0.0, 1.0))
			best_distance = distance
		previous_t = amount
		previous_curve = curve
	return Vector2(best_progress, best_distance)


func _twirl_press(at: Vector2) -> void:
	var offset := at - twirl_center()
	var radial_error := absf(offset.length() - twirl_radius())
	if radial_error > twirl_ring_width() * 0.5:
		_note_wrong("ballet_twirl", at, true)
		return
	_twirl_engaged = true
	_twirl_previous_angle = offset.angle()
	_twirl_handle_angle = _twirl_previous_angle
	if twirl_direction != 0:
		_twirl_arc_origin = _twirl_previous_angle \
			- float(twirl_direction) * TAU * twirl_progress


func _twirl_drag(at: Vector2) -> void:
	if not _twirl_engaged:
		return
	var offset := at - twirl_center()
	var radial_error := absf(offset.length() - twirl_radius())
	if radial_error > twirl_ring_width() * 0.5:
		_note_wrong("ballet_twirl", at, false)
		return
	var angle := offset.angle()
	var change := wrapf(angle - _twirl_previous_angle, -PI, PI)
	if absf(change) < 0.012:
		return
	if absf(change) > TWIRL_MAX_ANGLE_STEP:
		_note_wrong("ballet_twirl", at, false)
		_twirl_previous_angle = angle
		return
	var direction := 1 if change > 0.0 else -1
	if twirl_direction == 0:
		twirl_direction = direction
		_twirl_arc_origin = _twirl_previous_angle \
			- float(twirl_direction) * TAU * twirl_progress
	elif direction != twirl_direction:
		_note_wrong("ballet_twirl", at, false)
		_twirl_previous_angle = angle
		return
	var delta := minf(absf(change) / TAU, 1.0 - twirl_progress)
	if delta <= 0.0001:
		return
	twirl_progress = minf(1.0, twirl_progress + delta)
	widget_fill = twirl_progress
	_twirl_previous_angle = angle
	_twirl_handle_angle = angle
	_note_meaningful_progress()
	feedback_positive = true
	feedback_t = 0.22
	feedback_anchor = twirl_handle_position()
	gesture.emit("ballet_twirl", delta, 1.0)
	var pose_band := clampi(floori(twirl_progress * 3.0), 0, POSE_FRAMES.size() - 1)
	if pose_band > _twirl_pose_band:
		_twirl_pose_band = pose_band
		gesture.emit("ballet_pose_cue", float(POSE_FRAMES[pose_band]), 1.0)


func _draw() -> void:
	match mode:
		"ballet_pose":
			_draw_pose_game()
		"ballet_ribbon":
			_draw_ribbon_game()
		"ballet_twirl":
			_draw_twirl_game()
	if feedback_t > 0.0:
		_draw_feedback()
	if demo_active and not armed_only and not completion_accepted and not _mode_complete():
		_draw_ballet_demo()
	if completion_accepted:
		_draw_completion_halo()


func _draw_pose_game() -> void:
	var target_rect := pose_target_rect()
	var pulse := 0.5 + 0.5 * sin(_elapsed * 4.2)
	_draw_shell_frame(target_rect, true, false,
		Color(1.0, 0.86, 0.42, 0.30 + pulse * 0.20))
	_draw_pose_portrait(pose_target_frame(), target_rect.grow(-18.0), true)
	var frames := pose_option_frames()
	var rects := pose_option_rects()
	for index in range(rects.size()):
		var frame := int(frames[index])
		var correct := frame == pose_target_frame()
		var rect: Rect2 = rects[index]
		if correct and _assist_level >= 2:
			rect = rect.grow(rect.size.x * 0.10)
		var dimmed := _assist_level >= 2 and not correct
		var halo := Color(1.0, 0.88, 0.46,
			0.44 + pulse * 0.28) if correct and _assist_level >= 1 else Color.TRANSPARENT
		_draw_shell_frame(rect, correct and _assist_level >= 1, dimmed, halo)
		_draw_pose_portrait(frame, rect.grow(-15.0), false)
		if dimmed:
			draw_circle(rect.get_center(), rect.size.x * 0.43,
				Color(0.12, 0.16, 0.31, 0.44))
	_draw_round_pearls()


func _draw_shell_frame(rect: Rect2, highlighted: bool, dimmed: bool,
		halo: Color) -> void:
	var center := rect.get_center()
	var radius := rect.size.x * 0.46
	if halo.a > 0.0:
		draw_circle(center, radius * 1.16, halo)
	var outline := Color("#5a327f")
	var shell := Color("#f4b4c8") if not dimmed else Color("#9c8ca9")
	for petal_index in range(9):
		var angle := PI + float(petal_index) / 8.0 * PI
		var petal := center + Vector2.from_angle(angle) * radius * 0.56
		draw_circle(petal, radius * 0.35, shell)
	draw_circle(center, radius, outline)
	draw_circle(center, radius - 7.0,
		Color("#fff2df") if not highlighted else Color("#fff7c9"))
	draw_arc(center, radius, 0.0, TAU, 44,
		Color("#ffe483") if highlighted else Color("#d798b7"), 7.0, true)
	draw_circle(center + Vector2(0.0, radius * 0.73), radius * 0.10,
		Color("#fff4ba"))


func _draw_pose_portrait(frame: int, rect: Rect2, upper_body: bool) -> void:
	if _ballerina_atlas == null:
		draw_circle(rect.get_center(), minf(rect.size.x, rect.size.y) * 0.28, accent)
		return
	var crop_height := 205.0 if upper_body else 214.0
	var source := Rect2(Vector2(float(frame) * ATLAS_CELL.x,
		float(WORK_ROW) * ATLAS_CELL.y), Vector2(ATLAS_CELL.x, crop_height))
	var destination := rect
	destination.size.y = destination.size.x * crop_height / ATLAS_CELL.x
	destination.position.y = rect.position.y + (rect.size.y - destination.size.y) * 0.42
	draw_texture_rect_region(_ballerina_atlas, destination, source)


func _draw_round_pearls() -> void:
	var gap := 38.0
	var origin := Vector2(size.x * 0.5 - gap, maxf(24.0, size.y * 0.055))
	for round_index in range(POSE_ROUNDS):
		var center := origin + Vector2(float(round_index) * gap, 0.0)
		var done := round_index < pose_round
		draw_circle(center, 13.0, Color("#704a91"))
		draw_circle(center, 9.0,
			Color("#fff0a8") if done else Color(0.69, 0.80, 0.88, 0.72))
		if done:
			draw_circle(center - Vector2(3.0, 3.0), 3.0, Color.WHITE)


func _draw_ribbon_game() -> void:
	var previous := ribbon_point(0.0)
	for index in range(1, RIBBON_SAMPLES + 1):
		var amount := float(index) / float(RIBBON_SAMPLES)
		var point := ribbon_point(amount)
		draw_line(previous, point, Color(0.13, 0.14, 0.34, 0.58),
			ribbon_corridor_width() + 12.0, true)
		previous = point
	previous = ribbon_point(0.0)
	for index in range(1, RIBBON_SAMPLES + 1):
		var amount := float(index) / float(RIBBON_SAMPLES)
		var point := ribbon_point(amount)
		var hue := fposmod(0.94 + amount * 0.58, 1.0)
		var ribbon_color := Color.from_hsv(hue, 0.42, 1.0, 0.82)
		draw_line(previous, point, ribbon_color,
			RIBBON_COLOR_WIDTH + (18.0 if _assist_level >= 2 else 0.0), true)
		previous = point
	previous = ribbon_point(0.0)
	for index in range(1, RIBBON_SAMPLES + 1):
		var amount := float(index) / float(RIBBON_SAMPLES)
		var point := ribbon_point(amount)
		if amount <= ribbon_progress + 0.0001:
			draw_line(previous, point, Color("#fff2a6"), 26.0, true)
			draw_line(previous, point, Color.WHITE, 8.0, true)
		previous = point
	for pearl_index in range(6):
		var amount := float(pearl_index) / 5.0
		var center := ribbon_point(amount)
		var reached := amount <= ribbon_progress + 0.015
		draw_circle(center, 27.0,
			Color(1.0, 0.83, 0.47, 0.62) if reached else Color(0.48, 0.82, 0.90, 0.52))
		draw_circle(center, 16.0,
			Color("#fff4bd") if reached else Color("#d5f5ff"))
	var resume := ribbon_point(ribbon_progress)
	var resume_radius := ribbon_resume_rect().size.x * 0.5
	var pulse := 0.5 + 0.5 * sin(_elapsed * 5.0)
	draw_circle(resume, resume_radius * (0.82 + pulse * 0.12),
		Color(1.0, 0.88, 0.45, 0.25 + pulse * 0.22))
	draw_circle(resume, 31.0, Color("#fff0a8"))
	draw_circle(resume - Vector2(8.0, 8.0), 8.0, Color.WHITE)


func _draw_twirl_game() -> void:
	var center := twirl_center()
	var radius := twirl_radius()
	draw_circle(center, radius * 1.22, Color(0.20, 0.13, 0.39, 0.30))
	draw_arc(center, radius, 0.0, TAU, 72, Color(0.14, 0.14, 0.36, 0.72),
		twirl_ring_width() + 14.0, true)
	draw_arc(center, radius, 0.0, TAU, 72, Color(0.43, 0.86, 0.88, 0.52),
		twirl_ring_width(), true)
	var direction := twirl_direction if twirl_direction != 0 else 1
	var finish_angle := _twirl_arc_origin + float(direction) * TAU * twirl_progress
	if twirl_progress > 0.001:
		draw_arc(center, radius, _twirl_arc_origin, finish_angle, 72,
			Color("#ffe789"), 76.0, true)
		draw_arc(center, radius, _twirl_arc_origin, finish_angle, 72,
			Color.WHITE, 12.0, true)
	var box_side := radius * 1.23
	if _music_box != null:
		draw_texture_rect(_music_box,
			Rect2(center - Vector2.ONE * box_side * 0.5, Vector2.ONE * box_side), false)
	else:
		draw_circle(center, box_side * 0.35, Color("#e99aae"))
	for pearl_index in range(8):
		var angle := -PI * 0.5 + float(pearl_index) / 8.0 * TAU
		var pearl := center + Vector2.from_angle(angle) * radius
		draw_circle(pearl, 15.0, Color(1.0, 0.94, 0.72, 0.88))
	var handle := twirl_handle_position()
	var handle_radius := TWIRL_HANDLE_DIAMETER * 0.5 \
		* (1.18 if _assist_level >= 2 else 1.0)
	var pulse := 0.5 + 0.5 * sin(_elapsed * 5.2)
	draw_circle(handle, handle_radius * (1.08 + pulse * 0.10),
		Color(1.0, 0.84, 0.38, 0.24 + pulse * 0.22))
	draw_circle(handle, handle_radius, Color("#f5b6d0"))
	draw_circle(handle, handle_radius - 8.0, Color("#fff0bd"))
	draw_circle(handle - Vector2(handle_radius * 0.23, handle_radius * 0.23),
		handle_radius * 0.18, Color.WHITE)


func _draw_feedback() -> void:
	var alpha := clampf(feedback_t / 0.34, 0.0, 1.0)
	if feedback_positive:
		for ring_index in range(3):
			draw_arc(feedback_anchor, 34.0 + float(ring_index) * 18.0,
				0.0, TAU, 32, Color(1.0, 0.92, 0.46, alpha * 0.55), 6.0, true)
	else:
		for bubble_index in range(4):
			var angle := float(bubble_index) / 4.0 * TAU
			var bubble := feedback_anchor + Vector2.from_angle(angle) * (26.0 + 18.0 * alpha)
			draw_arc(bubble, 9.0 + float(bubble_index), 0.0, TAU, 20,
				Color(0.70, 0.91, 1.0, alpha * 0.72), 3.0, true)


func _draw_ballet_demo() -> void:
	var travel := clampf((demo_t - 0.18) / 1.05, 0.0, 1.0)
	travel = travel * travel * (3.0 - 2.0 * travel)
	var at := size * 0.5
	match mode:
		"ballet_pose":
			var frames := pose_option_frames()
			var rects := pose_option_rects()
			var correct := 0
			for index in range(frames.size()):
				if int(frames[index]) == pose_target_frame():
					correct = index
					break
			at = pose_target_rect().get_center().lerp(rects[correct].get_center(), travel)
		"ballet_ribbon":
			var end := minf(1.0, ribbon_progress + 0.30)
			at = ribbon_point(lerpf(ribbon_progress, end, travel))
		"ballet_twirl":
			var direction := twirl_direction if twirl_direction != 0 else 1
			var angle := _twirl_handle_angle + float(direction) * TAU * 0.30 * travel
			at = twirl_center() + Vector2.from_angle(angle) * twirl_radius()
	_draw_ghost_finger(at, travel >= 0.72)


func _draw_ghost_finger(at: Vector2, pressing: bool) -> void:
	var radius := 34.0 if not pressing else 29.0
	draw_circle(at, radius + 15.0, Color(1.0, 0.89, 0.39, 0.28))
	draw_line(at + Vector2(15.0, 18.0), at + Vector2(44.0, 56.0),
		Color(1.0, 0.98, 0.91, 0.94), 23.0, true)
	draw_circle(at, radius, Color(1.0, 0.98, 0.91, 0.96))
	draw_circle(at - Vector2(9.0, 10.0), 8.0, Color.WHITE)
	draw_arc(at, radius, 0.0, TAU, 28, Color("#8d6aaa"), 4.0, true)


func _draw_completion_halo() -> void:
	var center := size * 0.5
	var pulse := 0.5 + 0.5 * sin(_elapsed * 4.0)
	for ring_index in range(4):
		draw_arc(center, minf(size.x, size.y) * (0.25 + float(ring_index) * 0.055),
			0.0, TAU, 64, Color(1.0, 0.88, 0.42,
			0.18 + pulse * 0.12 - float(ring_index) * 0.025), 7.0, true)
