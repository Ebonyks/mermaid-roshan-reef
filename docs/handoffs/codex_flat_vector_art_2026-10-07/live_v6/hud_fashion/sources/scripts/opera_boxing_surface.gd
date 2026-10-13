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
const IMP_PATH := "res://assets/opera/worlds/actors/rival_boxer"
const MITTS_PATH := \
	"res://assets/opera/worlds/widgets/widget_track_boxer_mover.png"
const TARGET_PATH := \
	"res://assets/opera/worlds/widgets/widget_target_boxer_mark.png"
const BELT_PATH := "res://assets/opera/worlds/props/goal_boxer.png"
const PUFF_PATH := "res://assets/opera/worlds/props/fx_bop_puff.png"
const TELEGRAPH_PATH := \
	"res://assets/opera/worlds/props/fx_telegraph_ring.png"

const GLOVE_CORAL := Color("#f27e77")
const GLOVE_LIGHT := Color("#ffaaa0")
const GLOVE_SHADOW := Color("#d75f68")
const CUFF_TEAL := Color("#4ca9a6")
const CUFF_CORAL := Color("#df716f")
const PEARL_GOLD := Color("#ffd46a")
const INK := Color("#382485")
const BUBBLE := Color("#b9f6ff")

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

var _mitts_texture: Texture2D = null
var _target_texture: Texture2D = null
var _belt_texture: Texture2D = null
var _puff_texture: Texture2D = null
var _telegraph_texture: Texture2D = null
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
	cancel_all_touches()
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
	cancel_all_touches()
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
	touch_owners.clear()
	for hand in range(2):
		glove_fingers[hand] = -1
		_touch_offsets[hand] = Vector2.ZERO
		_touch_origins[hand] = Vector2.ZERO
		_touch_moved[hand] = false
		_punch_latched[hand] = false
		_returning[hand] = false
		glove_positions[hand] = glove_rest_position(hand)
	held = false
	queue_redraw()


func receive_friendly_hit() -> void:
	# Intentionally no damage, miss, score, combo, progress, or input lock.
	hit_feedback_t = 0.78
	_impact_t = maxf(_impact_t, 0.42)
	_impact_position = Vector2(size.x * 0.5, size.y * 0.68)
	_play_player(_bonk_player, 0.86)
	gesture.emit("boxing_contact", 0.0, 1.0)
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
	return Vector2(size.x * (0.42 if hand == 0 else 0.58), size.y * 0.58)


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
	if _mitts_texture == null:
		_mitts_texture = _load_texture(MITTS_PATH)
		_target_texture = _load_texture(TARGET_PATH)
		_belt_texture = _load_texture(BELT_PATH)
		_puff_texture = _load_texture(PUFF_PATH)
		_telegraph_texture = _load_texture(TELEGRAPH_PATH)
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
			or what == NOTIFICATION_WM_WINDOW_FOCUS_OUT:
		cancel_all_touches()


func _process(delta: float) -> void:
	var step := maxf(0.0, delta)
	_elapsed += step
	if feedback_t > 0.0:
		feedback_t = maxf(0.0, feedback_t - step)
	if hit_feedback_t > 0.0:
		hit_feedback_t = maxf(0.0, hit_feedback_t - step)
	if _impact_t > 0.0:
		_impact_t = maxf(0.0, _impact_t - step)
	for hand in range(2):
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
	_counter_t -= delta
	if _counter_t > 0.0:
		return
	var target := guard_target_position(_guard_side)
	var blocked := false
	for hand in range(2):
		if glove_positions[hand].distance_to(target) <= _target_radius() * 1.08:
			blocked = true
			break
	if blocked:
		_round_index += 1
		_impact_position = target
		_impact_t = 0.45
		_stuck_t = 0.0
		_play_player(_pop_player, 1.18)
		gesture.emit("boxing_guard", 1.0, 1.0)
		_guard_side = 1 - _guard_side
	else:
		receive_friendly_hit()
	_counter_t = COUNTER_SECONDS + (0.7 if _assist_level >= 1 else 0.0)


func _tick_imp(delta: float) -> void:
	_imp_state_t -= delta
	if _imp_state_t > 0.0:
		return
	match _imp_state:
		"taunt", "guard":
			_imp_state = "windup"
			_imp_state_t = 1.15 + (0.45 if _assist_level >= 1 else 0.0)
			_play_player(_ring_player, 1.0)
		"windup":
			_imp_state = "charge"
			_imp_state_t = 0.38
		"charge":
			_resolve_imp_counter()
			_imp_state = "recover"
			_imp_state_t = 1.7 + (0.5 if _assist_level >= 1 else 0.0)
		"recover":
			_imp_state = "guard"
			_imp_state_t = 0.85
		"bopped", "stagger":
			_imp_state = "guard"
			_imp_state_t = 0.65
		_:
			_imp_state = "taunt"
			_imp_state_t = 1.2


func _resolve_imp_counter() -> void:
	var blocked := false
	for hand in range(2):
		if glove_positions[hand].distance_to(guard_target_position(hand)) \
				<= _target_radius() * 1.12:
			blocked = true
			_impact_position = glove_positions[hand]
			break
	if blocked:
		_impact_t = 0.34
		_play_player(_pop_player, 0.92)
		gesture.emit("boxing_contact", 0.0, 1.0)
	else:
		receive_friendly_hit()


func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		_saw_screen_touch = true
		if touch.pressed:
			_handle_press(touch.index, touch.position)
		else:
			_handle_release(touch.index, touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
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
	if completion_accepted or finished or armed_only or touch_owners.has(finger_id):
		return
	note_input()
	_stuck_t = 0.0
	var hand := _choose_hand(at)
	if hand < 0:
		return
	touch_owners[finger_id] = hand
	glove_fingers[hand] = finger_id
	_touch_offsets[hand] = glove_positions[hand] - at
	_touch_origins[hand] = glove_positions[hand]
	_touch_moved[hand] = false
	_punch_latched[hand] = false
	_returning[hand] = false
	held = true
	queue_redraw()


func _handle_drag(finger_id: int, at: Vector2) -> void:
	if not touch_owners.has(finger_id) or completion_accepted or finished:
		return
	var hand := int(touch_owners[finger_id])
	var next := at + _touch_offsets[hand]
	next.x = clampf(next.x, 62.0, size.x - 62.0)
	next.y = clampf(next.y, 54.0, size.y - 38.0)
	if next.distance_to(glove_positions[hand]) > 2.0:
		_touch_moved[hand] = true
	glove_positions[hand] = next
	pointer_pos = at
	match mode:
		"boxing_guide":
			_try_guide(hand)
		"boxing_jab", "boxing_imp":
			_try_forward_punch(hand)
		"boxing_belt":
			_try_belt_punch(hand)
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
		gesture.emit(mode, 0.0, 1.0)
		restart_demo()
	held = not touch_owners.is_empty()
	queue_redraw()


func _choose_hand(at: Vector2) -> int:
	var choices: Array[int] = []
	for hand in range(2):
		if glove_fingers[hand] != -1:
			continue
		if mode == "boxing_guide" and _guide_done[hand]:
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


func _try_guide(hand: int) -> void:
	if _guide_done[hand] or _punch_latched[hand]:
		return
	var target := guide_target_position(hand)
	if glove_positions[hand].distance_to(target) > _target_radius():
		return
	if _forward_fraction(hand, target) < 0.62:
		return
	_guide_done[hand] = true
	_punch_latched[hand] = true
	glove_positions[hand] = target
	landed_punches += 1
	_round_index += 1
	_accept_impact(target, 1.04)
	gesture.emit("boxing_guide", 1.0, 1.0)


func _try_forward_punch(hand: int) -> void:
	if _punch_latched[hand]:
		return
	var target := active_target_position()
	if glove_positions[hand].distance_to(target) > _target_radius():
		return
	if _forward_fraction(hand, target) < 0.70:
		return
	if mode == "boxing_imp" and not imp_is_open():
		_punch_latched[hand] = true
		_impact_position = target
		_impact_t = 0.28
		_play_player(_bonk_player, 1.05)
		gesture.emit("boxing_imp", 0.0, 1.0)
		restart_demo()
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


func _try_belt_punch(hand: int) -> void:
	if _punch_latched[hand] or not _belt_rect().grow(28.0).has_point(glove_positions[hand]):
		return
	var target := active_target_position()
	if _forward_fraction(hand, target) < 0.62:
		return
	_punch_latched[hand] = true
	landed_punches += 1
	_round_index = 1
	_accept_impact(target, 1.32)
	_play_player(_bell_player, 1.32)
	gesture.emit("boxing_belt", 1.0, 1.0)


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
	# The approved 2K boxer painting remains the stage. This surface adds only
	# interaction ink, targets, two vector gloves, the approved imp, and FX.
	draw_rect(Rect2(Vector2.ZERO, size), Color(0.02, 0.03, 0.14, 0.06), true)
	_draw_progress_lights()
	_draw_punch_lanes()
	match mode:
		"boxing_guide":
			_draw_mitts()
			for hand in range(2):
				_draw_target(guide_target_position(hand), _guide_done[hand])
		"boxing_jab":
			_draw_mitts()
			_draw_target(active_target_position(), false)
		"boxing_guard":
			_draw_counter()
		"boxing_imp":
			_draw_boxer_imp()
			if imp_is_open():
				_draw_target(active_target_position(), false)
		"boxing_belt":
			_draw_belt()
	for hand in range(2):
		_draw_glove(hand)
	if _impact_t > 0.0:
		_draw_impact()
	if hit_feedback_t > 0.0:
		_draw_friendly_hit()
	if demo_active and not completion_accepted:
		_draw_demo()


func _draw_progress_lights() -> void:
	var count := _mode_goal()
	var step := 34.0
	var start_x := (size.x - step * float(count - 1)) * 0.5
	for index in range(count):
		var at := Vector2(start_x + float(index) * step, 28.0)
		var done := index < _round_index
		draw_circle(at, 11.0, Color(INK, 0.82))
		draw_circle(at, 7.0, PEARL_GOLD if done else Color(BUBBLE, 0.38))
		if done:
			draw_circle(at - Vector2(2.0, 2.0), 2.2, Color.WHITE)


func _draw_punch_lanes() -> void:
	if mode == "boxing_guard":
		return
	for hand in range(2):
		var start := glove_rest_position(hand)
		var target := guide_target_position(hand) if mode == "boxing_guide" \
			else active_target_position()
		var color := Color(BUBBLE, 0.23 if glove_fingers[hand] == -1 else 0.42)
		draw_line(start, target, color, 8.0, true)
		for marker in range(1, 4):
			var amount := float(marker) / 4.0
			var at := start.lerp(target, amount)
			draw_circle(at, 10.0 + amount * 10.0, Color(color, color.a * 0.55), false, 3.0, true)


func _draw_mitts() -> void:
	if _mitts_texture == null:
		return
	var side := minf(350.0, size.y * 0.52)
	var rect := Rect2(Vector2(size.x * 0.5 - side * 0.5, size.y * 0.31 - side * 0.5),
		Vector2.ONE * side)
	draw_texture_rect(_mitts_texture, rect, false, Color.WHITE)


func _draw_target(at: Vector2, completed: bool) -> void:
	var pulse := 1.0 + sin(_elapsed * 5.0) * 0.08
	var radius := _target_radius() * pulse
	var color := PEARL_GOLD if completed else Color("#fff1a6")
	draw_circle(at, radius * 0.82, Color(color, 0.13))
	draw_arc(at, radius, 0.0, TAU, 48, Color(color, 0.82), 7.0, true)
	draw_arc(at, radius * 0.68, 0.0, TAU, 40, Color(BUBBLE, 0.54), 4.0, true)
	if _target_texture != null:
		var side := radius * 0.92
		draw_texture_rect(_target_texture,
			Rect2(at - Vector2.ONE * side * 0.5, Vector2.ONE * side), false,
			Color(color, 0.92 if not completed else 0.62))
	if completed:
		_draw_star(at, 28.0, Color.WHITE)


func _draw_counter() -> void:
	var target := guard_target_position(_guard_side)
	_draw_target(target, false)
	var origin := Vector2(size.x * 0.5, size.y * 0.18)
	var amount := clampf(1.0 - _counter_t / COUNTER_SECONDS, 0.0, 1.0)
	var eased := amount * amount * (3.0 - 2.0 * amount)
	var counter := origin.lerp(target, eased)
	if _telegraph_texture != null:
		var ring_side := 120.0 + amount * 50.0
		draw_texture_rect(_telegraph_texture,
			Rect2(counter - Vector2.ONE * ring_side * 0.5, Vector2.ONE * ring_side),
			false, Color(PEARL_GOLD, 0.46))
	draw_circle(counter, 34.0 + amount * 18.0, Color(GLOVE_CORAL, 0.92))
	draw_arc(counter, 34.0 + amount * 18.0, 0.0, TAU, 32, INK, 6.0, true)
	var arrow_end := target - Vector2(0.0, 76.0)
	draw_line(origin, arrow_end, Color(PEARL_GOLD, 0.62), 8.0, true)
	var direction := (arrow_end - origin).normalized()
	var perpendicular := Vector2(-direction.y, direction.x)
	var arrow := PackedVector2Array([
		arrow_end, arrow_end - direction * 28.0 + perpendicular * 18.0,
		arrow_end - direction * 28.0 - perpendicular * 18.0,
	])
	draw_colored_polygon(arrow, PEARL_GOLD)


func _draw_boxer_imp() -> void:
	var texture := _imp_textures.get(_imp_state) as Texture2D
	if texture == null:
		texture = _imp_textures.get("idle") as Texture2D
	var side := minf(380.0, size.y * 0.57)
	var bob := sin(_elapsed * 3.4) * 5.0 if _imp_state in ["idle", "taunt"] else 0.0
	var center := Vector2(size.x * 0.5, size.y * 0.36 + bob)
	if texture != null:
		draw_texture_rect(texture,
			Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side), false)
	if _imp_state == "windup" and _telegraph_texture != null:
		var pulse := 190.0 + sin(_elapsed * 10.0) * 20.0
		draw_texture_rect(_telegraph_texture,
			Rect2(center - Vector2.ONE * pulse * 0.5, Vector2.ONE * pulse), false,
			Color(PEARL_GOLD, 0.66))
	if _imp_state == "recover":
		draw_arc(active_target_position(), _target_radius() + 24.0,
			0.0, TAU, 48, Color(PEARL_GOLD, 0.84), 9.0, true)


func _draw_belt() -> void:
	var rect := _belt_rect()
	if _belt_texture != null:
		draw_texture_rect(_belt_texture, rect, false)
	_draw_target(active_target_position(), finished)


func _glove_depth(hand: int) -> float:
	var rest := glove_rest_position(hand)
	var target := guide_target_position(hand) if mode == "boxing_guide" \
		else active_target_position()
	var route := target - rest
	if route.length_squared() < 1.0:
		return 0.0
	return clampf((glove_positions[hand] - rest).dot(route.normalized()) / route.length(),
		0.0, 1.0)


func _draw_glove(hand: int) -> void:
	var position := glove_positions[hand]
	var depth := _glove_depth(hand)
	var scale_value := 0.92 + depth * 0.38
	if _impact_t > 0.0 and position.distance_to(_impact_position) < 130.0:
		scale_value += sin((_impact_t / 0.52) * PI) * 0.10
	var mirror := 1.0 if hand == 0 else -1.0
	var angle := (-0.08 if hand == 0 else 0.08) \
		+ clampf((pointer_pos.x - position.x) / maxf(1.0, size.x), -0.08, 0.08)
	draw_set_transform(position + Vector2(0.0, 15.0), angle,
		Vector2(mirror * scale_value, scale_value))
	draw_circle(Vector2(-4.0, -12.0), 54.0, Color(0.06, 0.03, 0.16, 0.20))
	draw_circle(Vector2(23.0, -32.0), 35.0, Color(0.06, 0.03, 0.16, 0.20))
	draw_circle(Vector2(38.0, 5.0), 28.0, Color(0.06, 0.03, 0.16, 0.20))
	draw_set_transform(position, angle, Vector2(mirror * scale_value, scale_value))
	# Compound circles give the fist a smooth storybook silhouette without
	# deriving or regenerating the approved fused glove bitmap.
	draw_circle(Vector2(-4.0, -12.0), 55.0, INK)
	draw_circle(Vector2(22.0, -34.0), 36.0, INK)
	draw_circle(Vector2(37.0, 5.0), 29.0, INK)
	draw_rect(Rect2(-34.0, 18.0, 61.0, 35.0), INK, true)
	draw_circle(Vector2(-4.0, -12.0), 49.0, GLOVE_CORAL)
	draw_circle(Vector2(20.0, -33.0), 30.0, GLOVE_CORAL)
	draw_circle(Vector2(35.0, 5.0), 23.0, GLOVE_SHADOW)
	draw_rect(Rect2(-28.0, 17.0, 53.0, 34.0), GLOVE_CORAL, true)
	draw_arc(Vector2(35.0, 5.0), 23.0, -1.3, 1.8, 20, INK, 4.0, true)
	draw_arc(Vector2(-5.0, -28.0), 28.0, -2.8, -0.25, 20,
		Color(GLOVE_LIGHT, 0.68), 5.0, true)
	draw_line(Vector2(-17.0, -10.0), Vector2(18.0, -6.0),
		Color(GLOVE_SHADOW, 0.74), 3.5, true)
	var cuff := CUFF_CORAL if hand == 0 else CUFF_TEAL
	draw_rect(Rect2(-35.0, 32.0, 70.0, 31.0), INK, true)
	draw_rect(Rect2(-30.0, 36.0, 60.0, 22.0), cuff, true)
	draw_line(Vector2(-30.0, 36.0), Vector2(30.0, 36.0),
		Color("#fff1c9"), 2.0, true)
	draw_circle(Vector2.ZERO + Vector2(0.0, 47.0), 12.0, PEARL_GOLD)
	draw_arc(Vector2(0.0, 47.0), 12.0, 0.0, TAU, 20, INK, 3.2, true)
	for ray in [-0.75, -0.25, 0.25, 0.75]:
		var direction := Vector2(sin(float(ray)), -cos(float(ray)))
		draw_line(Vector2(0.0, 49.0), Vector2(0.0, 49.0) + direction * 7.0,
			Color("#fff0bd"), 2.4, true)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _draw_impact() -> void:
	var amount := 1.0 - clampf(_impact_t / 0.52, 0.0, 1.0)
	if _puff_texture != null:
		var side := 130.0 + amount * 90.0
		draw_texture_rect(_puff_texture,
			Rect2(_impact_position - Vector2.ONE * side * 0.5, Vector2.ONE * side),
			false, Color(1.0, 1.0, 1.0, 1.0 - amount * 0.55))
	else:
		draw_arc(_impact_position, 42.0 + amount * 80.0, 0.0, TAU, 32,
			Color(BUBBLE, 1.0 - amount), 8.0, true)


func _draw_friendly_hit() -> void:
	var amount := clampf(hit_feedback_t / 0.78, 0.0, 1.0)
	var center := Vector2(size.x * 0.5, size.y * 0.64)
	for index in range(8):
		var angle := float(index) / 8.0 * TAU + _elapsed * 0.8
		var radius := 100.0 + float(index % 3) * 28.0
		var bubble := center + Vector2.from_angle(angle) * radius
		draw_circle(bubble, 10.0 + float(index % 2) * 6.0,
			Color(BUBBLE, amount * 0.62), false, 4.0, true)
	for index in range(5):
		var star_angle := float(index) / 5.0 * TAU - _elapsed
		_draw_star(center + Vector2.from_angle(star_angle) * 76.0,
			13.0, Color(PEARL_GOLD, amount))


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
	elif mode == "boxing_belt":
		target = active_target_position()
	var travel := clampf(cycle / 0.72, 0.0, 1.0)
	travel = travel * travel * (3.0 - 2.0 * travel)
	var at := start.lerp(target, travel)
	draw_line(start, target, Color(PEARL_GOLD, 0.34), 6.0, true)
	draw_circle(at, 31.0, Color(PEARL_GOLD, 0.24))
	draw_circle(at, 18.0, Color(1.0, 0.97, 0.82, 0.92))
	draw_arc(at, 31.0 + sin(_elapsed * 7.0) * 4.0,
		0.0, TAU, 28, Color(PEARL_GOLD, 0.82), 5.0, true)


func _draw_star(center: Vector2, radius: float, color: Color) -> void:
	var points := PackedVector2Array()
	for index in range(10):
		var use_radius := radius if index % 2 == 0 else radius * 0.45
		points.append(center + Vector2.from_angle(-PI * 0.5 + float(index) * PI / 5.0)
			* use_radius)
	draw_colored_polygon(points, color)
