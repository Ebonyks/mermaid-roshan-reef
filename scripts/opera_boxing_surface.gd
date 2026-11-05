class_name OperaBoxingSurface
extends OperaGestureSurface
## Two independently finger-owned floating gloves for the Opera boxer career.
##
## This surface deliberately owns no career, score, health, or save state.
## It validates forward glove travel and emits accepted units to
## OperaCareerWorld2D. The opponent may make friendly contact, but that path
## changes only short-lived bubbles and sound: accepted work can never fall.

const SUPPORTED_MODES: Array[String] = [
	"boxing_guide", "boxing_jab", "boxing_guard", "boxing_imp", "boxing_belt",
]
const MODE_GOALS := {
	"boxing_guide": 2,
	"boxing_jab": 4,
	"boxing_guard": 3,
	"boxing_imp": 6,
	"boxing_belt": 1,
}
const MOUSE_FINGER := -101
const REDRAW_STEP := 0.033
const FIRST_ASSIST_SECONDS := 5.0
const STRONG_ASSIST_SECONDS := 10.0
const COUNTER_SECONDS := 3.2
const Contact := preload("res://scripts/opera_boxing_contact.gd")
const PHONE_EDGES := "phone_edges"
const TABLET_DIRECT := "tablet_direct"
const EDGE_GAIN := Vector2(2.4, 1.15)
const COUNTER_WINDUP := 0.8
const IMP_TRAVEL_SECONDS := 0.9
const IMP_PATH := "res://assets/opera/worlds/actors/rival_boxer"
const MITTS_PATH := \
	"res://assets/opera/worlds/boxer_quality_20261019/focus_mitt.png"
const BELT_PATH := "res://assets/opera/worlds/props/goal_boxer.png"
const PUFF_PATH := "res://assets/opera/worlds/boxer_quality_20261019/impact_puff.png"


const JAB_TARGETS: Array[Vector2] = [
	Vector2(0.43, 0.32), Vector2(0.57, 0.32),
	Vector2(0.47, 0.27), Vector2(0.54, 0.34),
]

## Probe-visible transient state. None of it is persisted.
var touch_owners: Dictionary = {}
var landed_punches := 0
var hit_feedback_t := 0.0
var finished := false

var glove_positions: Array[Vector2] = [Vector2.ZERO, Vector2.ZERO]
var glove_fingers: Array[int] = [-1, -1]
var _touch_offsets: Array[Vector2] = [Vector2.ZERO, Vector2.ZERO]
var _touch_origins: Array[Vector2] = [Vector2.ZERO, Vector2.ZERO]
var _touch_moved: Array[bool] = [false, false]
var _punch_latched: Array[bool] = [false, false]
var _returning: Array[bool] = [false, false]
var _guide_done: Array[bool] = [false, false]
var _round_index := 0
var _jab_target_index := 0
var _guard_side := 0
var _counter_t := COUNTER_SECONDS
var _imp_state := "taunt"
var _imp_state_t := 1.4
var _impact_t := 0.0
var _impact_position := Vector2.ZERO
var _assist_level := 0
var _stuck_t := 0.0
var _elapsed := 0.0
var _redraw_t := 0.0
var _saw_screen_touch := false
## AUTO uses Android's physical short side in density-independent pixels.
## The explicit override is also available to the desktop/test harness.
var control_layout := TABLET_DIRECT
var _layout_override := "auto"
var _touch_starts: Array[Vector2] = [Vector2.ZERO, Vector2.ZERO]
var _press_gloves: Array[Vector2] = [Vector2.ZERO, Vector2.ZERO]
var _frame_start_gloves: Array[Vector2] = [Vector2.ZERO, Vector2.ZERO]
var _counter_open_ready: Array[bool] = [false, false]
var _attack_resolved := false
var _attack_suspended := false
var _epoch := 0

var _painted_gloves: Array[Texture2D] = []
var _feedback_pictures: PaintedFeedbackArt = null
var _mitts_texture: Texture2D = null
var _belt_texture: Texture2D = null
var _puff_texture: Texture2D = null
var _imp_textures: Dictionary = {}
var _pop_player: AudioStreamPlayer = null
var _bonk_player: AudioStreamPlayer = null
var _ring_player: AudioStreamPlayer = null
var _bell_player: AudioStreamPlayer = null

func configure(next_mode: String, next_accent: Color, choice: int = 1,
		next_context: String = "") -> void:
	assert(next_mode in SUPPORTED_MODES,
		"OperaBoxingSurface received an unsupported gesture mode")
	super.configure(next_mode, next_accent, choice, next_context)
	_load_resources()
	_clear_touches(false)
	control_layout = _detect_control_layout() if _layout_override == "auto" else _layout_override
	_attack_suspended = false
	_attack_resolved = false
	landed_punches = 0
	finished = false
	hit_feedback_t = 0.0
	_guide_done = [false, false]
	_round_index = 0
	_jab_target_index = 0
	_guard_side = 0
	_counter_t = COUNTER_SECONDS
	_imp_state = "taunt"
	_imp_state_t = 1.4
	_impact_t = 0.0
	_impact_position = Vector2.ZERO
	_assist_level = 0
	_stuck_t = 0.0
	_elapsed = 0.0
	_redraw_t = 0.0
	_saw_screen_touch = false
	demo_active = true
	demo_t = 0.0
	input_started = false
	completion_accepted = false
	queue_redraw()


func set_fill(value: float) -> void:
	# The career is the authoritative progress owner. Synchronization only banks
	# accepted work; it can never rewind local glove or opponent state.
	super.set_fill(value)
	var external_round := clampi(
		floori(clampf(value, 0.0, 1.0) * float(_mode_goal()) + 0.001),
		0, _mode_goal())
	_round_index = maxi(_round_index, external_round)
	if value >= 0.999:
		finished = true
		demo_active = false
	queue_redraw()


func accept_completion() -> void:
	super.accept_completion()
	finished = true
	demo_active = false
	_clear_touches(false)
	if mode == "boxing_imp":
		_imp_state = "bow"
		_imp_state_t = 999.0
	queue_redraw()


func restart_demo() -> void:
	if completion_accepted or finished:
		return
	_assist_level = mini(2, _assist_level + 1)
	demo_active = true
	demo_t = 0.0
	queue_redraw()


func cancel_all_touches() -> void:
	_clear_touches(true)


func _clear_touches(stop_sounds: bool) -> void:
	_epoch += 1
	_attack_suspended = true
	_attack_resolved = false
	_counter_t = COUNTER_SECONDS
	_imp_state = "taunt"
	_imp_state_t = 1.4
	# Completion cancels input/attacks but lets earned one-shot feedback finish.
	# Explicit interruption and tree exit also silence the owned audio players.
	if stop_sounds:
		for player: AudioStreamPlayer in [_pop_player, _bonk_player, _ring_player, _bell_player]:
			if is_instance_valid(player):
				player.stop()
	touch_owners.clear()
	for hand in range(2):
		glove_fingers[hand] = -1
		_touch_offsets[hand] = Vector2.ZERO
		_touch_origins[hand] = Vector2.ZERO
		_touch_starts[hand] = Vector2.ZERO
		_press_gloves[hand] = Vector2.ZERO
		_counter_open_ready[hand] = false
		_touch_moved[hand] = false
		_punch_latched[hand] = false
		_returning[hand] = false
		glove_positions[hand] = glove_rest_position(hand)
		_frame_start_gloves[hand] = glove_positions[hand]
	held = false
	queue_redraw()


func receive_friendly_hit() -> void:
	# Intentionally no damage, miss, score, combo, progress, or input lock.
	hit_feedback_t = 0.78
	_impact_t = maxf(_impact_t, 0.42)
	_impact_position = Vector2(size.x * 0.5, size.y * 0.68)
	_play_player(_bonk_player, 0.86)
	var epoch := _epoch
	gesture.emit("boxing_contact", 0.0, 1.0)
	if epoch != _epoch:
		return
	if not completion_accepted:
		restart_demo()
	queue_redraw()


func glove_rest_position(side: int) -> Vector2:
	var hand := clampi(side, 0, 1)
	return Vector2(size.x * (0.31 if hand == 0 else 0.69), size.y * 0.84)


func glove_rest(side: int) -> Vector2:
	return glove_rest_position(side)


func guide_target_position(side: int) -> Vector2:
	var hand := clampi(side, 0, 1)
	return Vector2(size.x * (0.43 if hand == 0 else 0.57), size.y * 0.34)


func guard_target_position(side: int) -> Vector2:
	var hand := clampi(side, 0, 1)
	return incoming_position(0.58, hand)


func set_control_layout(layout: String) -> void:
	assert(layout in ["auto", PHONE_EDGES, TABLET_DIRECT])
	_layout_override = layout
	cancel_all_touches()
	control_layout = _detect_control_layout() if layout == "auto" else layout
	_attack_suspended = false
	queue_redraw()


func _detect_control_layout() -> String:
	if not OS.has_feature("android") and not OS.has_feature("ios"):
		return TABLET_DIRECT
	var pixels := DisplayServer.screen_get_size()
	var dpi := DisplayServer.screen_get_dpi()
	if dpi > 0:
		return PHONE_EDGES if float(mini(pixels.x, pixels.y)) * 160.0 / float(dpi) < 600.0 else TABLET_DIRECT
	return PHONE_EDGES


func edge_control_rect(hand: int) -> Rect2:
	var screen := _screen_bounds_local()
	var width := maxf(110.0, screen.size.x * 0.18)
	return Rect2(screen.position.x if hand == 0 else screen.end.x - width,
		screen.position.y + screen.size.y * 0.2, width, screen.size.y * 0.8)


func _screen_bounds_local() -> Rect2:
	if not is_inside_tree():
		return Rect2(Vector2.ZERO, size)
	var inverse := get_global_transform_with_canvas().affine_inverse()
	var screen := get_viewport_rect()
	var start := inverse * screen.position
	return Rect2(start, inverse * screen.end - start).abs()


func _has_point(at: Vector2) -> bool:
	# A fixed 1280x720 stage can have side margins on a wide phone. The visible
	# edge bays and their input extend into those margins without moving art.
	return Rect2(Vector2.ZERO, size).has_point(at) or (control_layout == PHONE_EDGES
		and (edge_control_rect(0).has_point(at) or edge_control_rect(1).has_point(at)))


func control_press_position(hand: int) -> Vector2:
	if control_layout == PHONE_EDGES:
		var bay := edge_control_rect(hand)
		return Vector2(bay.get_center().x, size.y * 0.84)
	return glove_positions[hand]


func control_drag_position(hand: int, glove_at: Vector2) -> Vector2:
	# Maps desired glove geometry back to an ordinary input-event position.
	# It never moves the glove or validates/awards a contact.
	if control_layout == PHONE_EDGES:
		return _touch_starts[hand] + (glove_at - _press_gloves[hand]) / EDGE_GAIN
	return glove_at - _touch_offsets[hand]


func incoming_position(progress: float, side: int = -1) -> Vector2:
	var hand := _guard_side if side < 0 else clampi(side, 0, 1)
	var origin := Vector2(size.x * (0.43 if hand == 0 else 0.57), size.y * 0.20)
	var endpoint := Vector2(size.x * (0.46 if hand == 0 else 0.54), size.y * 0.86)
	return origin.lerp(endpoint, clampf(progress, 0.0, 1.0))


func incoming_radius(progress: float) -> float:
	return 160.0 * (0.78 + clampf(progress, 0.0, 1.0) * 0.25) * 0.34


func incoming_progress() -> float:
	if mode == "boxing_guard":
		return clampf((COUNTER_SECONDS - _counter_t - COUNTER_WINDUP) /
			(COUNTER_SECONDS - COUNTER_WINDUP), 0.0, 1.0)
	if mode == "boxing_imp" and _imp_state == "charge":
		return clampf(1.0 - _imp_state_t / IMP_TRAVEL_SECONDS, 0.0, 1.0)
	return 0.0


func _incoming_active() -> bool:
	return not _attack_suspended and not _attack_resolved and (
		(mode == "boxing_guard" and _counter_t <= COUNTER_SECONDS - COUNTER_WINDUP)
		or (mode == "boxing_imp" and _imp_state == "charge"))


func punch_target(side: int = 0) -> Vector2:
	if mode == "boxing_guide":
		return guide_target_position(side)
	return active_target_position()


func active_target_position() -> Vector2:
	match mode:
		"boxing_guide":
			return guide_target_position(0 if not _guide_done[0] else 1)
		"boxing_jab":
			var normalized: Vector2 = JAB_TARGETS[_jab_target_index % JAB_TARGETS.size()]
			return Vector2(size.x * normalized.x, size.y * normalized.y)
		"boxing_guard":
			return guard_target_position(_guard_side)
		"boxing_imp":
			# Aim for the padded chest/gloves, never the friendly imp's face.
			return Vector2(size.x * 0.5, size.y * 0.43)
		"boxing_belt":
			return Vector2(size.x * 0.5, size.y * 0.39)
	return size * 0.5


func touch_owner_snapshot() -> Dictionary:
	return touch_owners.duplicate()


func landed_count() -> int:
	return landed_punches


func round_index() -> int:
	return _round_index


func is_demo_active() -> bool:
	return demo_active


func has_friendly_hit_feedback() -> bool:
	return hit_feedback_t > 0.0


func imp_is_open() -> bool:
	return mode == "boxing_imp" and _imp_state == "recover"


func _mode_goal() -> int:
	return int(MODE_GOALS.get(mode, 1))


func _load_texture(path: String) -> Texture2D:
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


func _load_resources() -> void:
	if _painted_gloves.is_empty():
		_painted_gloves.append(_load_texture("res://assets/opera/worlds/boxer_quality_20261019/glove_left.png"))
		_painted_gloves.append(_load_texture("res://assets/opera/worlds/boxer_quality_20261019/glove_right.png"))
	if _mitts_texture == null:
		_mitts_texture = _load_texture(MITTS_PATH)
		_belt_texture = _load_texture(BELT_PATH)
		_puff_texture = _load_texture(PUFF_PATH)
	for state: String in [
		"idle", "windup", "charge", "recover", "guard", "stagger",
		"taunt", "bopped", "bow",
	]:
		if _imp_textures.has(state):
			continue
		var suffix := "" if state == "idle" else "_%s" % state
		_imp_textures[state] = _load_texture("%s%s.png" % [IMP_PATH, suffix])
	_ensure_audio()


func _ensure_audio() -> void:
	if _pop_player != null:
		return
	_pop_player = _make_player("res://assets/audio/sfx/combat_pop.wav", -8.0)
	_bonk_player = _make_player("res://assets/audio/sfx/combat_bonk.wav", -11.0)
	_ring_player = _make_player("res://assets/audio/sfx/combat_charge_ring.wav", -12.0)
	_bell_player = _make_player("res://assets/audio/chime.ogg", -8.0)


func _make_player(path: String, volume_db: float) -> AudioStreamPlayer:
	var player := AudioStreamPlayer.new()
	if ResourceLoader.exists(path):
		player.stream = load(path) as AudioStream
	player.bus = "SFX"
	player.volume_db = volume_db
	add_child(player)
	return player


func _play_player(player: AudioStreamPlayer, pitch: float = 1.0) -> void:
	if player == null or player.stream == null or not player.is_inside_tree():
		return
	player.pitch_scale = pitch
	player.play()


func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT \
			or what == NOTIFICATION_WM_WINDOW_FOCUS_OUT \
			or what == NOTIFICATION_PAUSED or what == NOTIFICATION_EXIT_TREE \
			or (what == NOTIFICATION_VISIBILITY_CHANGED and not is_visible_in_tree()):
		cancel_all_touches()


func _process(delta: float) -> void:
	if not is_finite(delta) or delta <= 0.0:
		return
	var step := minf(10.0, delta)
	_elapsed += step
	if feedback_t > 0.0:
		feedback_t = maxf(0.0, feedback_t - step)
	if hit_feedback_t > 0.0:
		hit_feedback_t = maxf(0.0, hit_feedback_t - step)
	if _impact_t > 0.0:
		_impact_t = maxf(0.0, _impact_t - step)
	for hand in range(2):
		_frame_start_gloves[hand] = glove_positions[hand]
		if _returning[hand] and glove_fingers[hand] == -1:
			var rest := glove_rest_position(hand)
			glove_positions[hand] = glove_positions[hand].lerp(rest,
				1.0 - exp(-step * 12.0))
			if glove_positions[hand].distance_to(rest) < 1.0:
				glove_positions[hand] = rest
				_returning[hand] = false
	if not completion_accepted and not finished and not armed_only:
		_stuck_t += step
		if _stuck_t >= STRONG_ASSIST_SECONDS and _assist_level < 2:
			_assist_level = 2
			demo_active = true
			demo_t = 0.0
		elif _stuck_t >= FIRST_ASSIST_SECONDS and _assist_level < 1:
			_assist_level = 1
			demo_active = true
			demo_t = 0.0
		if demo_active:
			demo_t += step
		match mode:
			"boxing_guard":
				_tick_counter(step)
			"boxing_imp":
				_tick_imp(step)
	_redraw_t += step
	if _redraw_t >= REDRAW_STEP:
		_redraw_t = 0.0
		queue_redraw()


func _tick_counter(delta: float) -> void:
	if _attack_suspended:
		return
	var before := incoming_progress()
	var previous_t := _counter_t
	_counter_t -= delta
	if _counter_t <= COUNTER_SECONDS - COUNTER_WINDUP and not _attack_resolved:
		var from_fraction := clampf((previous_t - (COUNTER_SECONDS - COUNTER_WINDUP)) / delta, 0.0, 1.0)
		var to_fraction := clampf(previous_t / delta, 0.0, 1.0)
		if _sweep_incoming(before, incoming_progress(), from_fraction, to_fraction):
			return
	if _counter_t > 0.0:
		return
	if not _attack_resolved:
		_attack_resolved = true
		var epoch := _epoch
		receive_friendly_hit()
		if epoch != _epoch:
			return
	_start_counter()


func _start_counter() -> void:
	_guard_side = 1 - _guard_side
	_counter_t = COUNTER_SECONDS
	_attack_resolved = false


func _tick_imp(delta: float) -> void:
	if _attack_suspended:
		return
	var remaining := delta
	# Consume state boundaries in order, including a hitch spanning windup and
	# flight. Contact always resolves before expiry; no catch-up award loop.
	for transition in range(16):
		var from_fraction := 1.0 - remaining / delta
		var step := minf(remaining, maxf(0.0, _imp_state_t))
		var before := incoming_progress()
		_imp_state_t -= step
		remaining -= step
		if _imp_state == "charge" and _sweep_incoming(before, incoming_progress(),
				from_fraction, 1.0 - remaining / delta):
			return
		if _imp_state_t > 0.0:
			return
		match _imp_state:
			"taunt", "guard":
				_imp_state = "windup"
				_imp_state_t = 1.15 + (0.45 if _assist_level >= 1 else 0.0)
				_play_player(_ring_player, 1.0)
			"windup":
				_imp_state = "charge"
				_imp_state_t = IMP_TRAVEL_SECONDS
				_attack_resolved = false
			"charge":
				_attack_resolved = true
				_open_counter_window()
				var epoch := _epoch
				receive_friendly_hit()
				if epoch != _epoch:
					return
				return
			"recover":
				_imp_state = "guard"
				_imp_state_t = 0.85
				_guard_side = 1 - _guard_side
			"bopped", "stagger":
				_imp_state = "guard"
				_imp_state_t = 0.65
				_guard_side = 1 - _guard_side
			_:
				_imp_state = "taunt"
				_imp_state_t = 1.2
		if remaining <= 0.0:
			return


func _sweep_incoming(before: float, after: float, from_fraction: float = 0.0,
		to_fraction: float = 1.0) -> bool:
	if _attack_resolved or _attack_suspended:
		return false
	var first := -1.0
	var first_hand := -1
	for hand in range(2):
		var from := _frame_start_gloves[hand].lerp(glove_positions[hand], from_fraction)
		var to := _frame_start_gloves[hand].lerp(glove_positions[hand], to_fraction)
		var contact := _glove_sweep(hand, from, to,
			incoming_position(before), incoming_position(after),
			incoming_radius(before), incoming_radius(after))
		if contact >= 0.0 and (first < 0.0 or contact < first):
			first = contact
			first_hand = hand
	if first_hand < 0:
		return false
	_resolve_block(first_hand, incoming_position(lerpf(before, after, first)))
	return true


func _resolve_block(hand: int, at: Vector2) -> void:
	# Latch and finish local state BEFORE synchronous career callbacks.
	_attack_resolved = true
	_impact_position = at
	_impact_t = 0.45
	_stuck_t = 0.0
	demo_active = false
	_play_player(_pop_player, 1.12)
	if mode == "boxing_guard":
		var earned := glove_fingers[hand] != -1 and _round_index < _mode_goal()
		if earned:
			_round_index += 1
		_start_counter()
		gesture.emit("boxing_guard" if earned else "boxing_contact", 1.0 if earned else 0.0, 1.0)
	else:
		_open_counter_window()
		gesture.emit("boxing_contact", 0.0, 1.0)


func _open_counter_window() -> void:
	_imp_state = "recover"
	_imp_state_t = 1.7 + (0.5 if _assist_level >= 1 else 0.0)
	for hand in range(2):
		_touch_origins[hand] = glove_positions[hand]
		_counter_open_ready[hand] = glove_positions[hand].distance_to(active_target_position()) \
			> _target_radius() + glove_contact_radius(hand, glove_positions[hand]) + 24.0
		_punch_latched[hand] = false


func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.index < 0:
			return
		_saw_screen_touch = true
		if touch.canceled:
			_cancel_finger(touch.index)
		elif touch.pressed:
			_handle_press(touch.index, touch.position)
		else:
			_handle_release(touch.index, touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index < 0:
			return
		_saw_screen_touch = true
		_handle_drag(drag.index, drag.position)
		accept_event()
	elif event is InputEventMouseButton \
			and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		var button := event as InputEventMouseButton
		if button.device == InputEvent.DEVICE_ID_EMULATION and _saw_screen_touch:
			return
		if button.pressed:
			_handle_press(MOUSE_FINGER, button.position)
		else:
			_handle_release(MOUSE_FINGER, button.position)
		accept_event()
	elif event is InputEventMouseMotion and touch_owners.has(MOUSE_FINGER):
		var motion := event as InputEventMouseMotion
		if motion.device == InputEvent.DEVICE_ID_EMULATION and _saw_screen_touch:
			return
		_handle_drag(MOUSE_FINGER, motion.position)
		accept_event()


func _handle_press(finger_id: int, at: Vector2) -> void:
	if not at.is_finite() or completion_accepted or finished or armed_only or touch_owners.has(finger_id):
		return
	var hand := _choose_hand(at)
	if hand < 0:
		return
	note_input()
	_stuck_t = 0.0
	_attack_suspended = false
	touch_owners[finger_id] = hand
	glove_fingers[hand] = finger_id
	_touch_starts[hand] = at
	_press_gloves[hand] = glove_positions[hand]
	_touch_offsets[hand] = glove_positions[hand] - at
	_touch_origins[hand] = glove_positions[hand]
	_counter_open_ready[hand] = glove_positions[hand].distance_to(active_target_position()) \
		> _target_radius() + glove_contact_radius(hand, glove_positions[hand]) + 24.0
	_touch_moved[hand] = false
	_punch_latched[hand] = false
	_returning[hand] = false
	held = true
	queue_redraw()


func _handle_drag(finger_id: int, at: Vector2) -> void:
	if not at.is_finite() or not touch_owners.has(finger_id) or completion_accepted or finished or armed_only:
		return
	var hand := int(touch_owners[finger_id])
	var next := at + _touch_offsets[hand]
	if control_layout == PHONE_EDGES:
		next = _press_gloves[hand] + (at - _touch_starts[hand]) * EDGE_GAIN
	next.x = clampf(next.x, 62.0, size.x - 62.0)
	next.y = clampf(next.y, 54.0, size.y - 38.0)
	var before := glove_positions[hand]
	if next.distance_to(before) > 2.0:
		_touch_moved[hand] = true
	glove_positions[hand] = next
	pointer_pos = at
	if _incoming_active():
		var progress := incoming_progress()
		var incoming := incoming_position(progress)
		var radius := incoming_radius(progress)
		var contact := _glove_sweep(hand, before, next, incoming, incoming, radius, radius)
		if contact >= 0.0:
			_resolve_block(hand, incoming)
			queue_redraw()
			return
	if _punch_latched[hand] and next.distance_to(glove_rest_position(hand)) < 110.0:
		_punch_latched[hand] = false
		_touch_origins[hand] = next
	match mode:
		"boxing_guide":
			_try_guide(hand, before)
		"boxing_jab", "boxing_imp":
			_try_forward_punch(hand, before)
		"boxing_belt":
			_try_belt_punch(hand, before)
	queue_redraw()


func _handle_release(finger_id: int, _at: Vector2) -> void:
	if not touch_owners.has(finger_id):
		return
	var hand := int(touch_owners[finger_id])
	touch_owners.erase(finger_id)
	glove_fingers[hand] = -1
	var accepted := _punch_latched[hand]
	var moved := _touch_moved[hand]
	_touch_offsets[hand] = Vector2.ZERO
	_touch_moved[hand] = false
	_punch_latched[hand] = false
	if mode != "boxing_guide" or not _guide_done[hand]:
		_returning[hand] = true
	if not accepted and moved and mode != "boxing_guard":
		restart_demo()
		gesture.emit(mode, 0.0, 1.0)
	held = not touch_owners.is_empty()
	queue_redraw()


func _cancel_finger(finger_id: int) -> void:
	if not touch_owners.has(finger_id):
		return
	var hand := int(touch_owners[finger_id])
	touch_owners.erase(finger_id)
	glove_fingers[hand] = -1
	_touch_moved[hand] = false
	_punch_latched[hand] = false
	_counter_open_ready[hand] = false
	_returning[hand] = false
	glove_positions[hand] = glove_rest_position(hand)
	held = not touch_owners.is_empty()
	queue_redraw()


func _choose_hand(at: Vector2) -> int:
	var choices: Array[int] = []
	for hand in range(2):
		if glove_fingers[hand] != -1:
			continue
		if mode == "boxing_guide" and _guide_done[hand]:
			continue
		if control_layout == PHONE_EDGES:
			if not edge_control_rect(hand).has_point(at):
				continue
		elif at.distance_to(glove_positions[hand]) > 110.0:
			continue
		choices.append(hand)
	if choices.is_empty():
		return -1
	if choices.size() == 1:
		return choices[0]
	var first := choices[0]
	var second := choices[1]
	return first if at.distance_to(glove_positions[first]) \
		<= at.distance_to(glove_positions[second]) else second


func _forward_fraction(hand: int, target: Vector2) -> float:
	var origin := _touch_origins[hand]
	var route := target - origin
	if route.length_squared() < 1.0:
		return 0.0
	return (glove_positions[hand] - origin).dot(route.normalized()) / route.length()


func _try_guide(hand: int, before: Vector2) -> void:
	if _guide_done[hand] or _punch_latched[hand]:
		return
	var target := guide_target_position(hand)
	if not _target_contact(hand, before, target, _target_radius()):
		return
	_guide_done[hand] = true
	_punch_latched[hand] = true
	glove_positions[hand] = target
	landed_punches += 1
	_round_index += 1
	_accept_impact(target, 1.04)
	gesture.emit("boxing_guide", 1.0, 1.0)


func _try_forward_punch(hand: int, before: Vector2) -> void:
	if _punch_latched[hand] or _round_index >= _mode_goal():
		return
	var target := active_target_position()
	if mode == "boxing_imp" and imp_is_open() and not _counter_open_ready[hand]:
		if glove_positions[hand].distance_to(target) > _target_radius() \
				+ glove_contact_radius(hand, glove_positions[hand]) + 24.0:
			_counter_open_ready[hand] = true
			_touch_origins[hand] = glove_positions[hand]
		return
	if not _target_contact(hand, before, target, _target_radius()):
		return
	if mode == "boxing_imp" and not imp_is_open():
		_punch_latched[hand] = true
		_impact_position = target
		_impact_t = 0.28
		_play_player(_bonk_player, 1.05)
		restart_demo()
		gesture.emit("boxing_imp", 0.0, 1.0)
		return
	_punch_latched[hand] = true
	landed_punches += 1
	_round_index += 1
	_accept_impact(target, 1.0 + float(hand) * 0.08)
	if mode == "boxing_jab":
		_jab_target_index = (_jab_target_index + 1) % JAB_TARGETS.size()
		gesture.emit("boxing_jab", 1.0, 1.0)
	else:
		_imp_state = "bopped" if landed_punches % 2 == 0 else "stagger"
		_imp_state_t = 0.58
		if landed_punches % 2 == 0:
			_play_player(_bell_player, 0.92 + float(landed_punches) * 0.03)
		gesture.emit("boxing_imp", 1.0, 1.0)


func _try_belt_punch(hand: int, before: Vector2) -> void:
	if _punch_latched[hand] or _round_index >= 1:
		return
	var target := active_target_position()
	if not _target_contact(hand, before, target, 56.0):
		return
	_punch_latched[hand] = true
	landed_punches += 1
	_round_index = 1
	_accept_impact(target, 1.32)
	_play_player(_bell_player, 1.32)
	gesture.emit("boxing_belt", 1.0, 1.0)


func _target_contact(hand: int, before: Vector2, target: Vector2, radius: float) -> bool:
	var after := glove_positions[hand]
	var route := target - _touch_origins[hand]
	if route.length_squared() < 1.0:
		return false
	var direction := route.normalized()
	var forward := (after - before).dot(direction)
	if forward <= 0.01:
		return false
	var initial := (before - _touch_origins[hand]).dot(direction)
	if initial + forward < 40.0:
		return false
	var start := before.lerp(after, clampf((40.0 - initial) / forward, 0.0, 1.0))
	return _glove_sweep(hand, start, after, target, target, radius, radius) >= 0.0


func _glove_sweep(hand: int, before: Vector2, after: Vector2,
		other_before: Vector2, other_after: Vector2, radius_before: float, radius_after: float) -> float:
	# Glove size follows a clamped linear reach. Split exactly at its clamp
	# boundaries, rather than approximating a changing painted disc by endpoints.
	var rest := glove_rest_position(hand)
	var target := guide_target_position(hand) if mode == "boxing_guide" else active_target_position()
	var route := target - rest
	var cuts: Array[float] = [0.0, 1.0]
	if route.length_squared() > 1.0:
		var first_depth := (before - rest).dot(route) / route.length_squared()
		var change := (after - before).dot(route) / route.length_squared()
		if absf(change) > 0.000001:
			for boundary: float in [0.0, 1.0]:
				var split := (boundary - first_depth) / change
				if split > 0.0 and split < 1.0:
					cuts.append(split)
	cuts.sort()
	for index in range(cuts.size() - 1):
		var low := cuts[index]
		var high := cuts[index + 1]
		var a0 := before.lerp(after, low)
		var a1 := before.lerp(after, high)
		var contact := Contact.sweep(a0, a1, glove_contact_radius(hand, a0), glove_contact_radius(hand, a1),
			other_before.lerp(other_after, low), other_before.lerp(other_after, high),
			lerpf(radius_before, radius_after, low), lerpf(radius_before, radius_after, high))
		if contact >= 0.0:
			return lerpf(low, high, contact)
	return -1.0


func glove_contact_radius(hand: int, at: Vector2) -> float:
	return 168.0 * (0.92 + _glove_depth_at(hand, at) * 0.38) * 0.34


func _accept_impact(at: Vector2, pitch: float) -> void:
	_impact_position = at
	_impact_t = 0.52
	_stuck_t = 0.0
	demo_active = false
	feedback_positive = true
	feedback_t = 0.32
	_play_player(_pop_player, pitch)


func _target_radius() -> float:
	return 78.0 + float(_assist_level) * 18.0


func _belt_rect() -> Rect2:
	var side := minf(300.0, size.y * 0.46)
	# The approved square asset carries transparent headroom; its medallion is
	# at roughly 74% height. Align that medallion, not the texture bounds, to
	# the authoritative punch target.
	var target := active_target_position()
	return Rect2(Vector2(target.x - side * 0.5, target.y - side * 0.74),
		Vector2.ONE * side)


func _draw() -> void:
	# Authored pictures retain their own light. Invitation pixels sit behind
	# the actual mitt, opponent or buckle, never as ink over their faces.
	_draw_progress_lights()
	match mode:
		"boxing_guide":
			for hand in range(2):
				_draw_target(guide_target_position(hand), _guide_done[hand])
			_draw_mitts()
		"boxing_jab":
			_draw_target(active_target_position(), false)
			_draw_mitts()
		"boxing_guard":
			_draw_counter()
		"boxing_imp":
			if imp_is_open():
				_draw_target(active_target_position(), false)
			_draw_boxer_imp()
		"boxing_belt":
			_draw_belt()
	for hand in range(2):
		_draw_glove(hand)
	if control_layout == PHONE_EDGES:
		_draw_edge_controls()
	if _impact_t > 0.0:
		_draw_impact()
	if hit_feedback_t > 0.0:
		_draw_friendly_hit()
	if demo_active and not completion_accepted:
		_draw_demo()


func _pictures() -> PaintedFeedbackArt:
	if _feedback_pictures == null:
		_feedback_pictures = PaintedFeedbackArt.new()
	return _feedback_pictures


func _draw_progress_lights() -> void:
	var count := _mode_goal()
	var step := 34.0
	var start_x := (size.x - step * float(count - 1)) * 0.5
	var working := not touch_owners.is_empty() 		and maxf(_glove_depth(0), _glove_depth(1)) > 0.1
	for index in range(count):
		var at := Vector2(start_x + float(index) * step, 28.0)
		var state := "full" if index < _round_index else (
			"filling" if index == _round_index and working else "empty")
		_pictures().pearl(self, at, state, 30.0)





func _draw_mitts() -> void:
	if _mitts_texture == null:
		return
	var side := minf(180.0, size.y * 0.26)
	var targets: Array[Vector2] = [active_target_position()]
	if mode == "boxing_guide":
		targets = [guide_target_position(0), guide_target_position(1)]
	for target: Vector2 in targets:
		# The authored shell medallion is the actual existing hit centre.
		draw_texture_rect(_mitts_texture,
			Rect2(target - Vector2(0.5, 0.516) * side, Vector2.ONE * side), false)


func _draw_target(at: Vector2, completed: bool) -> void:
	var key := int(floor(_elapsed / 0.22)) % 4
	_pictures().invitation(self, at, _target_radius() * 2.2, key, completed)


func _draw_counter() -> void:
	var progress := incoming_progress()
	var at := incoming_position(progress)
	# The invitation travels with the fist. It is never a separate fixed
	# interception gate; its painted padding owns the collision circle.
	_draw_target(at, false)
	_paint_glove(_guard_side, at, incoming_radius(progress) / 0.34, 0.0)


func _draw_boxer_imp() -> void:
	# The owner requested floating hands and a counter opening. Reuse the
	# existing authored glove pair; no new imp identity or body is invented.
	for hand in range(2):
		var at := Vector2(size.x * (0.46 if hand == 0 else 0.54), size.y * 0.40)
		var side := 160.0 * 0.78
		if imp_is_open() or _imp_state in ["bopped", "stagger", "bow"]:
			at = Vector2(size.x * (0.36 if hand == 0 else 0.64), size.y * 0.32)
		elif hand == _guard_side and _imp_state in ["windup", "charge"]:
			var progress := incoming_progress()
			at = incoming_position(progress)
			side = incoming_radius(progress) / 0.34
			_draw_target(at, false)
		_paint_glove(hand, at, side, 0.0)
	if imp_is_open():
		_draw_mitts()


func _draw_belt() -> void:
	_draw_target(active_target_position(), finished)
	var rect := _belt_rect()
	if _belt_texture != null:
		draw_texture_rect(_belt_texture, rect, false)


func _glove_depth(hand: int) -> float:
	return _glove_depth_at(hand, glove_positions[hand])


func _glove_depth_at(hand: int, at: Vector2) -> float:
	var rest := glove_rest_position(hand)
	var target := guide_target_position(hand) if mode == "boxing_guide" \
		else active_target_position()
	var route := target - rest
	if route.length_squared() < 1.0:
		return 0.0
	return clampf((at - rest).dot(route.normalized()) / route.length(),
		0.0, 1.0)


func _paint_glove(hand: int, at: Vector2, side: float, angle: float) -> void:
	if hand < 0 or hand >= _painted_gloves.size() or _painted_gloves[hand] == null:
		return
	draw_set_transform(at, angle)
	draw_texture_rect(_painted_gloves[hand],
		Rect2(-Vector2(0.49, 0.43) * side, Vector2.ONE * side), false)
	draw_set_transform(Vector2.ZERO)


func _draw_glove(hand: int) -> void:
	var position := glove_positions[hand]
	var depth := _glove_depth(hand)
	var scale_value := 0.92 + depth * 0.38
	var angle := (-0.08 if hand == 0 else 0.08) 		+ clampf((pointer_pos.x - position.x) / maxf(1.0, size.x), -0.08, 0.08)
	# Separate original left/right art: no mirror or independently deformed cuff.
	_paint_glove(hand, position, 168.0 * scale_value, angle)


func _draw_edge_controls() -> void:
	for hand in range(2):
		var bay := edge_control_rect(hand)
		draw_rect(bay, Color(0.16, 0.12, 0.35, 0.12))
		var center_x := bay.get_center().x
		draw_line(Vector2(center_x, size.y * 0.32), Vector2(center_x, size.y * 0.76),
			Color(0.98, 0.86, 0.55, 0.4), 5.0, true)
		_paint_glove(hand, Vector2(center_x, size.y * 0.86), 74.0, 0.0)


func _draw_impact() -> void:
	var amount := 1.0 - clampf(_impact_t / 0.52, 0.0, 1.0)
	if _puff_texture != null:
		var side := 130.0 + amount * 90.0
		draw_texture_rect(_puff_texture,
			Rect2(_impact_position - Vector2.ONE * side * 0.5, Vector2.ONE * side),
			false, Color(1.0, 1.0, 1.0, 1.0 - amount * 0.55))


func _draw_friendly_hit() -> void:
	var amount := clampf(hit_feedback_t / 0.78, 0.0, 1.0)
	var center := Vector2(size.x * 0.5, size.y * 0.64)
	if _puff_texture != null:
		var side := 170.0 + (1.0 - amount) * 60.0
		draw_texture_rect(_puff_texture,
			Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side),
			false, Color(1.0, 1.0, 1.0, amount))


func _draw_demo() -> void:
	var cycle := fmod(demo_t, 2.4) / 2.4
	var hand := int(floor(fmod(demo_t, 4.8) / 2.4))
	var start := glove_rest_position(hand)
	var target := active_target_position()
	if mode == "boxing_guide":
		target = guide_target_position(hand)
	elif mode == "boxing_guard":
		hand = _guard_side
		start = glove_rest_position(hand)
		target = guard_target_position(hand)
	var travel := clampf(cycle / 0.72, 0.0, 1.0)
	travel = travel * travel * (3.0 - 2.0 * travel)
	var at := start.lerp(target, travel)
	if control_layout == PHONE_EDGES:
		at = control_press_position(hand) + (at - start) / EDGE_GAIN
	var texture := _pictures().art("res://assets/opera/worlds/teacher/guide_hand.png")
	if texture != null:
		var side := 58.0
		draw_set_transform(at, PI)
		draw_texture_rect(texture, Rect2(-Vector2(0.436523, 0.986328) * side,
			Vector2.ONE * side), false)
		draw_set_transform(Vector2.ZERO)




