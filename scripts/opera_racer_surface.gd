class_name OperaRacerSurface
extends OperaGestureSurface
## The existing full Canvas racer runs inside the owning career surface.
## World retains phase, rewards, saves, Back and the later curtain call.

const EngineResource := preload("res://scripts/racer_game_2d.gd")
const Driving := preload("res://scripts/kart_driving.gd")
signal race_event(kind: String, value: float)

const LAP_DISTANCE := 800.0
const LAP_SECONDS := 24.0
const ROAD_WALL := 8.0
const INPUT_GRACE := 2.0
const STEERING_RANGE := 180.0
const STEERING_RECT := Rect2(175, 430, 830, 250)
const TURBO_CENTER := Vector2(1120, 635)
const TURBO_RADIUS := 62.0
const STOP_SECONDS := 0.9

var kart: Dictionary = {}
var rival: Dictionary = {}
var race_started := false
var race_finished := false
var race_clock := 0.0
var race_input_t := 0.0
var race_touch_owner := -1
var race_turbo_owner := -1
var race_turbo_held := false
var race_steer := 0.0
var race_countdown := 0.0
var race_flash := 0.0
var race_pearls := 0
var race_turbo_fires := 0
var race_wall_bumps := 0
var quality := "speedy"
var chime: AudioStreamPlayer = null
var _engine: RacerGame2D = null
var _owner_main: Node = null
var _rival_art: Texture2D = null
var _turbo_queued := false
var _drag_origin := Vector2.ZERO
var _epoch := 0
var _career_active := true
var _application_suspended := false
var _keyboard_needs_release := false
var _fire_previous := false
var _stop_t := 0.0
var _stop_speed := 0.0
var _stop_distance := 0.0


func configure(next_mode: String, next_accent: Color, choice: int = 1,
		next_context: String = "") -> void:
	cancel_race_touch()
	_dispose_engine()
	super.configure(next_mode, next_accent, choice, next_context)
	if next_mode != "kart_race":
		return
	_career_active = true
	race_started = false
	race_finished = false
	race_clock = 0.0
	race_countdown = 0.0
	race_pearls = 0
	race_turbo_fires = 0
	race_wall_bumps = 0
	_stop_t = 0.0
	_owner_main = _find_main_host()
	if _owner_main != null:
		quality = String(_owner_main.get("quality"))
		chime = _owner_main.get("chime") as AudioStreamPlayer
	_engine = EngineResource.new()
	_engine.name = "CastleRacerEngine"
	var roster: Array = EngineResource.RACERS.duplicate(true)
	roster[1]["name"] = "Imp Racer"
	roster[1]["sprite"] = "res://assets/opera/worlds/actors/rival_racer.png"
	var castle_line: Array = []
	for point: Vector2 in EngineResource.CTRL:
		castle_line.append(point * 0.75)
	_engine.configure({"external_input": true, "external_finish": true,
		"minimal_hud": true, "pearl_payout": false, "world_route": true,
		"laps": Driving.LAPS, "lap_target_sec": LAP_SECONDS,
		"shortcut": false, "racers": roster, "ctrl": castle_line})
	add_child(_engine)
	_engine.start(self, Callable())
	_engine.set_process(false)
	_rival_art = load(String(roster[1]["sprite"])) as Texture2D
	_sync_snapshot()
	queue_redraw()


func _find_main_host() -> Node:
	var ancestor: Node = get_parent()
	while ancestor != null:
		var script: Script = ancestor.get_script() as Script
		if script != null and script.resource_path == "res://scripts/opera_career_world_2d.gd":
			return ancestor.get("m") as Node
		ancestor = ancestor.get_parent()
	return null


func _say(who: String, event: String, cooldown: float = 1.0) -> void:
	if is_instance_valid(_owner_main) and _owner_main.has_method("_say"):
		_owner_main.call("_say", who, event, cooldown)


func _dispose_engine() -> void:
	if is_instance_valid(_engine):
		_engine.process_mode = Node.PROCESS_MODE_DISABLED
		if _engine._eng != null:
			_engine._eng.stop()
		remove_child(_engine)
		_engine.queue_free()
	_engine = null
	_rival_art = null


func set_career_active(active_now: bool) -> void:
	if _career_active and not active_now:
		cancel_race_touch()
	_career_active = active_now
	if is_instance_valid(_engine):
		var live: bool = active_now and not _application_suspended
		_engine.process_mode = Node.PROCESS_MODE_INHERIT if live else Node.PROCESS_MODE_DISABLED
		_engine.set_process(false)
		if _engine._eng != null:
			_engine._eng.stream_paused = not live or (not held and race_input_t <= 0.0)


func _gui_input(event: InputEvent) -> void:
	if mode != "kart_race":
		super._gui_input(event)
		return
	if armed_only or completion_accepted or race_finished or not _career_active \
			or _application_suspended:
		return
	if event is InputEventMouse and event.device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.canceled:
			if touch.index in [race_touch_owner, race_turbo_owner]:
				cancel_race_touch()
		elif touch.pressed:
			if touch.index not in [race_touch_owner, race_turbo_owner]:
				if touch.position.distance_to(TURBO_CENTER) <= TURBO_RADIUS and race_turbo_owner == -1:
					race_turbo_owner = touch.index
					race_turbo_held = true
					_turbo_queued = true
					_touch_race()
				elif race_touch_owner == -1 and race_turbo_owner == -1:
					race_touch_owner = touch.index
					_press(touch.position)
		elif touch.index == race_turbo_owner:
			race_turbo_owner = -1
			race_turbo_held = false
		elif touch.index == race_touch_owner:
			_release(touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == race_touch_owner:
			_drag(drag.position)
			accept_event()
	elif event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index == MOUSE_BUTTON_LEFT:
			if button.pressed and race_touch_owner == -1 and race_turbo_owner == -1:
				if button.position.distance_to(TURBO_CENTER) <= TURBO_RADIUS:
					race_turbo_owner = -2
				else:
					race_touch_owner = -2
				_press(button.position)
			elif not button.pressed and -2 in [race_touch_owner, race_turbo_owner]:
				_release(button.position)
			accept_event()
	elif event is InputEventMouseMotion and race_touch_owner == -2:
		_drag((event as InputEventMouseMotion).position)
		accept_event()


func _press(at: Vector2) -> void:
	if mode != "kart_race":
		super._press(at)
		return
	if armed_only or completion_accepted or race_finished:
		return
	if at.distance_to(TURBO_CENTER) <= TURBO_RADIUS:
		race_turbo_held = true
		_turbo_queued = true
	else:
		held = true
		_drag_origin = at
		race_steer = 0.0
	_touch_race()


func _drag(at: Vector2) -> void:
	if mode != "kart_race":
		super._drag(at)
		return
	if not held or armed_only or completion_accepted:
		return
	race_steer = clampf((at.x - _drag_origin.x) / STEERING_RANGE, -1.0, 1.0)
	_touch_race()


func _release(at: Vector2) -> void:
	if mode != "kart_race":
		super._release(at)
		return
	if race_touch_owner == -2 or race_turbo_owner == -2:
		race_turbo_owner = -1
		race_turbo_held = false
	race_touch_owner = -1
	held = false
	race_steer = 0.0


func _touch_race() -> void:
	race_input_t = INPUT_GRACE
	input_started = true
	demo_active = false
	if not race_started:
		race_started = true
		race_countdown = 1.5
		race_event.emit("start", 0.0)


func cancel_race_touch() -> void:
	_epoch += 1
	held = false
	race_turbo_held = false
	race_turbo_owner = -1
	race_touch_owner = -1
	race_input_t = 0.0
	race_steer = 0.0
	_turbo_queued = false
	_keyboard_needs_release = true
	_fire_previous = false
	if is_instance_valid(_engine):
		_engine._canvas_held = false
		_engine._canvas_steer = 0.0
		_engine._canvas_fire = false
		if _engine._eng != null:
			_engine._eng.stream_paused = true


func _notification(what: int) -> void:
	if what in [NOTIFICATION_PAUSED, NOTIFICATION_APPLICATION_PAUSED,
			NOTIFICATION_APPLICATION_FOCUS_OUT, NOTIFICATION_WM_CLOSE_REQUEST]:
		cancel_race_touch()
		if what in [NOTIFICATION_APPLICATION_PAUSED, NOTIFICATION_APPLICATION_FOCUS_OUT]:
			_application_suspended = true
	elif what in [NOTIFICATION_UNPAUSED, NOTIFICATION_APPLICATION_RESUMED,
			NOTIFICATION_APPLICATION_FOCUS_IN]:
		_application_suspended = false
		cancel_race_touch()


func _keyboard_input() -> void:
	var left: bool = Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A)
	var right: bool = Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D)
	var fire: bool = Input.is_physical_key_pressed(KEY_SPACE) or Input.is_physical_key_pressed(KEY_ENTER)
	var axis: float = Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
	left = left or Input.is_joy_button_pressed(0, JOY_BUTTON_DPAD_LEFT)
	right = right or Input.is_joy_button_pressed(0, JOY_BUTTON_DPAD_RIGHT)
	fire = fire or Input.is_joy_button_pressed(0, JOY_BUTTON_A) or Input.is_joy_button_pressed(0, JOY_BUTTON_B)
	if _keyboard_needs_release:
		if not left and not right and not fire and absf(axis) < 0.2:
			_keyboard_needs_release = false
		return
	if left or right or fire or absf(axis) > 0.2:
		if race_touch_owner == -1:
			race_steer = clampf(float(int(right) - int(left)) + (axis if absf(axis) > 0.2 else 0.0), -1.0, 1.0)
		if fire and not _fire_previous:
			_turbo_queued = true
		_touch_race()
	elif race_touch_owner == -1:
		race_steer = 0.0
	_fire_previous = fire


func _process(delta: float) -> void:
	if mode != "kart_race":
		super._process(delta)
		return
	if not is_instance_valid(_engine) or not _career_active or _application_suspended:
		return
	if race_finished:
		_tick_stop(delta)
		return
	if armed_only or completion_accepted:
		return
	_keyboard_input()
	race_clock += delta
	demo_t += delta
	if held or race_turbo_held:
		race_input_t = INPUT_GRACE
	else:
		race_input_t = maxf(0.0, race_input_t - delta)
	if not race_started or race_input_t <= 0.0:
		demo_active = true
		if _engine._eng != null:
			_engine._eng.stream_paused = true
		return
	var remaining: float = minf(delta, 0.2)
	while remaining > 0.00001 and not race_finished:
		var step: float = minf(remaining, 1.0 / 60.0)
		var current: RacerGame2D = _engine
		var epoch: int = _epoch
		_tick_driving(step)
		if _engine != current or _epoch != epoch:
			return
		remaining -= step


func _tick_driving(delta: float) -> void:
	var engine: RacerGame2D = _engine
	var epoch: int = _epoch
	var before: float = float(kart.get("s", 0.0))
	var boost_before: float = float(engine._pl["boost_t"])
	var pearls_before: int = engine._pearls_got
	var count_before: int = ceili(engine._clock * 2.0) if engine._state == "countdown" else 0
	engine._canvas_steer = race_steer
	engine._canvas_held = true
	engine._canvas_fire = _turbo_queued or race_turbo_held
	engine._touch_t = 3.0
	_turbo_queued = false
	if engine._eng != null:
		engine._eng.stream_paused = false
	engine.step_race(delta)
	if _engine != engine or _epoch != epoch:
		return
	_sync_snapshot()
	var count_now: int = ceili(engine._clock * 2.0) if engine._state == "countdown" else 0
	if count_now < count_before:
		race_event.emit("countdown", float(3 - count_now))
		if _engine != engine or _epoch != epoch:
			return
	if boost_before <= 0.0 and float(engine._pl["boost_t"]) > 0.0:
		race_turbo_fires += 1
		race_event.emit("turbo", float(race_turbo_fires))
		if _engine != engine or _epoch != epoch:
			return
	if engine._pearls_got > pearls_before:
		race_event.emit("pearl", float(engine._pearls_got))
		if _engine != engine or _epoch != epoch:
			return
	var progress: float = float(kart["s"])
	var lap_before: int = floori(before / LAP_DISTANCE)
	var lap_now: int = floori(progress / LAP_DISTANCE)
	if lap_now > lap_before:
		race_event.emit("lap", float(lap_now))
		if _engine != engine or _epoch != epoch:
			return
	if engine._state == "external_finish":
		race_finished = true
		_stop_t = STOP_SECONDS
		_stop_speed = float(engine._pl["speed"])
		_stop_distance = float(engine._pl["s"])
		cancel_race_touch()
	if progress > before:
		gesture.emit("kart_race", (progress - before) / LAP_DISTANCE, 1.0)


func _sync_snapshot() -> void:
	if not is_instance_valid(_engine) or _engine._pl == null:
		return
	kart = (_engine._pl as Dictionary).duplicate()
	kart["s"] = clampf(float(_engine._pl["s"]) / _engine._len, 0.0, float(Driving.LAPS)) * LAP_DISTANCE
	if _engine._karts.size() > 1:
		rival = (_engine._karts[1] as Dictionary).duplicate()
		rival["s"] = float(rival["s"]) / _engine._len * LAP_DISTANCE
	race_countdown = maxf(0.0, _engine._clock) if _engine._state == "countdown" else 0.0
	race_pearls = _engine._pearls_got


func _tick_stop(delta: float) -> void:
	if _stop_t <= 0.0:
		return
	_stop_t = maxf(0.0, _stop_t - delta)
	var fraction: float = _stop_t / STOP_SECONDS
	_engine._pl["speed"] = _stop_speed * fraction * fraction
	_engine._pl["s"] = _stop_distance + _stop_speed * STOP_SECONDS / 3.0 * (1.0 - fraction * fraction * fraction)
	_engine._place_kart(_engine._pl, delta)
	_engine._update_camera(delta)
	if _engine._canvas != null:
		_engine._canvas.queue_redraw()


func road_curvature(distance: float) -> float:
	if not is_instance_valid(_engine):
		return 0.0
	return _engine._curv_at(distance / LAP_DISTANCE * _engine._len)


func road_point(distance: float, lateral: float = 0.0) -> Vector2:
	if not is_instance_valid(_engine):
		return Vector2.ZERO
	return _engine._frame_at(distance / LAP_DISTANCE * _engine._len, lateral)[0]


func _draw() -> void:
	if mode != "kart_race":
		super._draw()


func _demo_finger_pose() -> Dictionary:
	if mode != "kart_race":
		return super._demo_finger_pose()
	return {"position": STEERING_RECT.get_center() + Vector2(sin(demo_t * 2.0) * 90.0, 0.0),
		"pressed": true}


func _exit_tree() -> void:
	cancel_race_touch()
