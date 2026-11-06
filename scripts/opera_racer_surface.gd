class_name OperaRacerSurface
extends OperaGestureSurface
## The Reef Grand Prix runs inside the owning career surface. The world keeps
## phase, rewards, saves, Back and the later curtain call; this surface owns
## the touch interface and clocks the engine only while the child is playing.
##
## Owner layout (2026-11-05): the left of the screen is a green steering stick
## (a touch anywhere in STEERING_RECT grabs it where the finger lands); the
## right has a gold gas pedal button and a bubble button that uses the item she is
## holding (zoom is the boost). The stick also supports one-finger steer-and-go; releasing all gas
## sources coasts. Every control
## belongs to exactly one finger (DL-UI-04); pause and focus loss cancel all
## of them (DL-UI-05). After INPUT_GRACE seconds without a held control the
## whole race freezes, so nothing moves, wins or loses without her.

const EngineScript := preload("res://scripts/racer/reef_kart_race.gd")
signal race_event(kind: String, value: float)

const LAP_DISTANCE := 800.0
const INPUT_GRACE := 2.0
## Left steering zone and the floating green stick.
const STEERING_RECT := Rect2(0, 200, 580, 520)
const STEERING_RANGE := 96.0
const STICK_RADIUS := 104.0
const STICK_HOME := Vector2(230, 560)
const STICK_BASE_BOUNDS := Rect2(112, 330, 356, 290)
## Right-hand item/boost bubble and gold gas pedal.
const TURBO_CENTER := Vector2(1010, 505)
const TURBO_RADIUS := 70.0
const GAS_CENTER := Vector2(1175, 625)
const GAS_RADIUS := 80.0
const HIT_MARGIN := 16.0
const MAX_STEP := 1.0 / 60.0
## Existing flavour lines fit race moments; exact neutral Guide item cues
## own the required voice lane and suppress these reactions. None
## plays in the first VOICE_QUIET seconds so the RACE instruction is heard.
const VOICE_QUIET := 4.0
const RACE_VOICES := {
	"zoom": ["roshan", "op_racer_work", 12.0],
	"imp_leads": ["imp", "op_racer_steal", 15.0],
	"imp_spins": ["imp", "op_racer_copy", 10.0],
}

var kart: Dictionary = {}
var rival: Dictionary = {}
var race_started := false
var race_finished := false
var race_clock := 0.0
var race_input_t := 0.0
var race_touch_owner := -1
var race_turbo_owner := -1
var race_gas_owner := -1
var race_turbo_held := false
var race_gas_held := false
var race_steer := 0.0
var race_countdown := 0.0
var race_pearls := 0
var race_turbo_fires := 0
var race_wall_bumps := 0
var race_attempt := 1
var quality := "speedy"
var chime: AudioStreamPlayer = null
var _engine: ReefKartRace = null
var _owner_main: Node = null
var _rival_art: Texture2D = null
var _turbo_queued := false
var _finish_pending := false
var _stick_base := STICK_HOME
var _stick_finger := STICK_HOME
var _controls_state: Dictionary = {}
var _epoch := 0
var _career_active := true
var _application_suspended := false
var _keyboard_needs_release := false
var _keyboard_brake := false
var _keyboard_gas := false
var _pending_item_voice := ""
var _fire_previous := false


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
	race_attempt = 1
	_finish_pending = false
	_stick_base = STICK_HOME
	_stick_finger = STICK_HOME
	kart = {"s": 0.0, "lat": 0.0, "speed": 0.0, "pearls": 0, "item": "", "lap": 0}
	rival = {"s": 0.0, "lat": 0.0}
	_owner_main = _find_main_host()
	if _owner_main != null:
		quality = String(_owner_main.get("quality"))
		chime = _owner_main.get("chime") as AudioStreamPlayer
	_engine = EngineScript.new()
	_engine.name = "ReefGrandPrix"
	_engine.setup({})
	add_child(_engine)
	_engine.race_event.connect(_on_engine_event)
	_engine.item_awarded.connect(_on_item_awarded)
	_rival_art = load("res://assets/opera/worlds/actors/rival_racer.png") as Texture2D
	_sync_snapshot()
	_publish_controls()
	queue_redraw()


func _find_main_host() -> Node:
	var ancestor: Node = get_parent()
	while ancestor != null:
		var script: Script = ancestor.get_script() as Script
		if script != null and script.resource_path == "res://scripts/opera_career_world_2d.gd":
			return ancestor.get("m") as Node
		ancestor = ancestor.get_parent()
	return null


func _say(who: String, event: String, cooldown: float) -> void:
	if is_instance_valid(_owner_main) and _owner_main.has_method("_say"):
		_owner_main.call("_say", who, event, cooldown)


func _race_voice(moment: String) -> void:
	if race_clock < VOICE_QUIET or race_finished:
		return
	var line: Array = RACE_VOICES.get(moment, [])
	if line.size() == 3:
		_say(String(line[0]), String(line[1]), float(line[2]))


func _dispose_engine() -> void:
	if is_instance_valid(_engine):
		_engine.process_mode = Node.PROCESS_MODE_DISABLED
		if _engine.race_event.is_connected(_on_engine_event):
			_engine.race_event.disconnect(_on_engine_event)
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
			if touch.index in [race_touch_owner, race_turbo_owner, race_gas_owner]:
				cancel_race_touch()
		elif touch.pressed:
			_claim(touch.index, touch.position)
		else:
			_free_finger(touch.index)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == race_touch_owner:
			_drag(drag.position)
			accept_event()
	elif event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index == MOUSE_BUTTON_LEFT:
			if button.pressed:
				_claim(-2, button.position)
			else:
				_free_finger(-2)
			accept_event()
	elif event is InputEventMouseMotion and race_touch_owner == -2:
		_drag((event as InputEventMouseMotion).position)
		accept_event()


## Route a new finger to the first free control it lands on.
func _claim(finger: int, at: Vector2) -> void:
	if finger in [race_touch_owner, race_turbo_owner, race_gas_owner]:
		return
	if race_turbo_owner == -1 and at.distance_to(TURBO_CENTER) <= TURBO_RADIUS + HIT_MARGIN:
		# The familiar item bubble also skips a queued opening explanation.
		_clear_item_guidance()
		race_turbo_owner = finger
		race_turbo_held = true
		_turbo_queued = true
		_touch_race()
	elif race_gas_owner == -1 and at.distance_to(GAS_CENTER) <= GAS_RADIUS + HIT_MARGIN:
		race_gas_owner = finger
		race_gas_held = true
		_touch_race()
	elif race_touch_owner == -1 and STEERING_RECT.has_point(at):
		race_touch_owner = finger
		_press(at)


func _free_finger(finger: int) -> void:
	if finger == race_turbo_owner:
		race_turbo_owner = -1
		race_turbo_held = false
	if finger == race_gas_owner:
		race_gas_owner = -1
		race_gas_held = false
	if finger == race_touch_owner:
		_release(_stick_finger)
	_publish_controls()


## The stick's ring appears under the finger; steering is the sideways slide.
func _press(at: Vector2) -> void:
	if mode != "kart_race":
		super._press(at)
		return
	if armed_only or completion_accepted or race_finished:
		return
	held = true
	_stick_base = Vector2(clampf(at.x, STICK_BASE_BOUNDS.position.x, STICK_BASE_BOUNDS.end.x),
		clampf(at.y, STICK_BASE_BOUNDS.position.y, STICK_BASE_BOUNDS.end.y))
	_stick_finger = at
	race_steer = clampf((at.x - _stick_base.x) / STEERING_RANGE, -1.0, 1.0)
	_touch_race()
	_publish_controls()


func _drag(at: Vector2) -> void:
	if mode != "kart_race":
		super._drag(at)
		return
	if not held or armed_only or completion_accepted:
		return
	_stick_finger = at
	var reach := STEERING_RANGE * 1.25
	var dx := at.x - _stick_base.x
	if absf(dx) > reach:
		# The ring follows a finger that keeps sliding, so steering back the
		# other way answers at once.
		_stick_base.x = clampf(at.x - signf(dx) * reach,
			STICK_BASE_BOUNDS.position.x, STICK_BASE_BOUNDS.end.x)
		dx = at.x - _stick_base.x
	race_steer = clampf(dx / STEERING_RANGE, -1.0, 1.0)
	_touch_race()
	_publish_controls()


func _release(at: Vector2) -> void:
	if mode != "kart_race":
		super._release(at)
		return
	race_touch_owner = -1
	held = false
	race_steer = 0.0
	_stick_base = STICK_HOME
	_stick_finger = STICK_HOME
	_publish_controls()


func _touch_race() -> void:
	race_input_t = INPUT_GRACE
	input_started = true
	demo_active = false
	if not race_started:
		race_started = true
		race_countdown = ReefKartRace.COUNTDOWN
		if is_instance_valid(_engine):
			_engine.begin()
		race_event.emit("start", 0.0)


func _clear_item_guidance() -> void:
	_pending_item_voice = ""
	if is_instance_valid(_owner_main) and _owner_main.has_method("_audio_ref"):
		var audio: AudioDirector = _owner_main.call("_audio_ref") as AudioDirector
		if audio != null:
			audio.clear_kart_guidance()


func cancel_race_touch() -> void:
	_clear_item_guidance()
	_epoch += 1
	held = false
	race_turbo_held = false
	race_gas_held = false
	race_turbo_owner = -1
	race_gas_owner = -1
	race_touch_owner = -1
	race_input_t = 0.0
	race_steer = 0.0
	_turbo_queued = false
	_keyboard_needs_release = true
	_keyboard_brake = false
	_keyboard_gas = false
	_fire_previous = false
	_stick_base = STICK_HOME
	_stick_finger = STICK_HOME
	_publish_controls()


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


## Desktop and controller fallback: arrows/A/D steer, Space/Enter uses the
## item, Up/W or controller A/RT is gas; Down/S or B brakes. The stick is
## also a one-finger steer-and-go control for the original child touch mode.
func _keyboard_input() -> void:
	var left: bool = Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A)
	var right: bool = Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D)
	var fire: bool = Input.is_physical_key_pressed(KEY_SPACE) or Input.is_physical_key_pressed(KEY_ENTER)
	var gas: bool = Input.is_physical_key_pressed(KEY_UP) or Input.is_physical_key_pressed(KEY_W) or Input.is_joy_button_pressed(0, JOY_BUTTON_A) or Input.get_joy_axis(0, JOY_AXIS_TRIGGER_RIGHT) > 0.2
	var brake: bool = Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S)
	var axis: float = Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
	left = left or Input.is_joy_button_pressed(0, JOY_BUTTON_DPAD_LEFT)
	right = right or Input.is_joy_button_pressed(0, JOY_BUTTON_DPAD_RIGHT)
	fire = fire or Input.is_joy_button_pressed(0, JOY_BUTTON_X)
	brake = brake or Input.is_joy_button_pressed(0, JOY_BUTTON_B)
	if _keyboard_needs_release:
		if not left and not right and not fire and not brake and not gas and absf(axis) < 0.2:
			_keyboard_needs_release = false
		return
	_keyboard_gas = gas
	_keyboard_brake = brake
	if left or right or fire or brake or gas or absf(axis) > 0.2:
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
		_tick_finish(delta)
		return
	if armed_only or completion_accepted:
		return
	_keyboard_input()
	race_clock += delta
	if _pending_item_voice != "" and race_clock >= VOICE_QUIET:
		_say("guide", "kart_" + _pending_item_voice, 0.0)
		_pending_item_voice = ""
	demo_t += delta
	if held or race_turbo_held or race_gas_held:
		race_input_t = INPUT_GRACE
	else:
		race_input_t = maxf(0.0, race_input_t - delta)
	if not race_started or race_input_t <= 0.0:
		demo_active = true
		_publish_controls()
		return
	var remaining: float = minf(delta, 0.2)
	while remaining > 0.00001 and not race_finished:
		var step: float = minf(remaining, MAX_STEP)
		var current: ReefKartRace = _engine
		var epoch: int = _epoch
		_tick_driving(step)
		if _engine != current or _epoch != epoch:
			return
		remaining -= step
	_publish_controls()


func _tick_driving(delta: float) -> void:
	var engine: ReefKartRace = _engine
	var epoch: int = _epoch
	var before: float = float(kart.get("s", 0.0))
	var was_racing: bool = engine.state in ["race", "imp_beat", "finished"]
	engine.step_race(delta, {"steer": race_steer,
		"throttle": 1.0 if race_gas_held or _keyboard_gas or held else 0.0,
		"brake": _keyboard_brake, "item_pressed": _turbo_queued})
	if _engine != engine or _epoch != epoch:
		return
	if was_racing:
		# A bubble pressed during the countdown waits for the start.
		_turbo_queued = false
	_sync_snapshot()
	if _finish_pending:
		_finish_pending = false
		race_finished = true
	var progress: float = float(kart["s"])
	if progress > before:
		gesture.emit("kart_race", (progress - before) / LAP_DISTANCE, 1.0)
		if _engine != engine or _epoch != epoch:
			return
	if race_finished:
		cancel_race_touch()


## After the line the karts coast to a stop under confetti; nothing is scored.
func _tick_finish(delta: float) -> void:
	var remaining: float = minf(delta, 0.2)
	while remaining > 0.00001 and is_instance_valid(_engine):
		var step: float = minf(remaining, MAX_STEP)
		_engine.step_race(step, {})
		remaining -= step
	_sync_snapshot()


func _on_item_awarded(_slot: int, kind: String) -> void:
	if race_clock < VOICE_QUIET:
		_pending_item_voice = kind
	else:
		_say("guide", "kart_" + kind, 0.0)


func _on_engine_event(kind: String, value: float) -> void:
	match kind:
		"turbo":
			race_turbo_fires = int(value)
			_race_voice("zoom")
		"lead":
			if value > 0.5:
				_race_voice("imp_leads")
		"imp_flub":
			_race_voice("imp_spins")
		"bonk":
			if value > 0.5:
				_race_voice("imp_spins")
		"pearl":
			race_pearls = int(value)
		"bump":
			race_wall_bumps += 1
		"restart":
			_clear_item_guidance()
			race_attempt = int(value)
		"finish":
			_finish_pending = true
	if chime != null and kind in ["pearl", "item_ready", "turbo"]:
		chime.pitch_scale = 1.3 + 0.04 * clampf(float(race_pearls), 0.0, 10.0) \
			if kind == "pearl" else (1.7 if kind == "turbo" else 1.05)
		chime.play()
	race_event.emit(kind, value)


func _sync_snapshot() -> void:
	if not is_instance_valid(_engine) or _engine._pl.is_empty():
		return
	var pl: Dictionary = _engine._pl
	kart["s"] = _engine.player_progress() * LAP_DISTANCE
	kart["lat"] = float(pl["lat"])
	kart["speed"] = float(pl["speed"])
	kart["pearls"] = int(pl["pearls"])
	kart["item"] = String(pl["item"])
	kart["lap"] = mini(int(pl["lap"]), ReefKartRace.LAPS)
	var imp_kart: Dictionary = _engine.imp()
	rival["s"] = clampf(float(imp_kart["race_s"]) / _engine.track.length, 0.0,
		float(ReefKartRace.LAPS)) * LAP_DISTANCE
	rival["lat"] = float(imp_kart["lat"])
	race_countdown = maxf(0.0, _engine.clock) if _engine.state == "countdown" else 0.0
	race_pearls = int(pl["pearls"])


func _publish_controls() -> void:
	if not is_instance_valid(_engine):
		return
	var knob := STICK_HOME
	var base := STICK_HOME
	if held:
		base = _stick_base
		knob = _stick_base + Vector2(clampf(_stick_finger.x - _stick_base.x,
			-STEERING_RANGE, STEERING_RANGE), 0.0)
	_controls_state["stick_base"] = base
	_controls_state["stick_knob"] = knob
	_controls_state["stick_radius"] = STICK_RADIUS
	_controls_state["stick_held"] = held
	_controls_state["gas_center"] = GAS_CENTER
	_controls_state["gas_radius"] = GAS_RADIUS
	_controls_state["gas_held"] = race_gas_held or _keyboard_gas
	_controls_state["bubble_center"] = TURBO_CENTER
	_controls_state["bubble_radius"] = TURBO_RADIUS
	_controls_state["bubble_held"] = race_turbo_held
	_controls_state["guide"] = demo_active and not race_finished and not completion_accepted
	_engine.set_controls(_controls_state)


func road_curvature(distance: float) -> float:
	if not is_instance_valid(_engine):
		return 0.0
	return _engine.track.curvature_at(distance / LAP_DISTANCE * _engine.track.length)


func road_point(distance: float, lateral: float = 0.0) -> Vector2:
	if not is_instance_valid(_engine):
		return Vector2.ZERO
	return _engine.track.point_at(distance / LAP_DISTANCE * _engine.track.length, lateral)


func _draw() -> void:
	if mode != "kart_race":
		super._draw()


func _demo_finger_pose() -> Dictionary:
	if mode != "kart_race":
		return super._demo_finger_pose()
	var at := STICK_HOME + Vector2(sin(demo_t * 2.4) * STICK_RADIUS * 0.45, 0.0)
	return {"at": at, "pressing": true, "position": at, "pressed": true}


func _exit_tree() -> void:
	cancel_race_touch()
