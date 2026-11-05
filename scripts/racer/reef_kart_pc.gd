extends Control

const Catalog := preload("res://scripts/racer/reef_kart_catalog.gd")
const Courses := preload("res://scripts/racer/reef_kart_courses.gd")
const Race := preload("res://scripts/racer/reef_kart_race.gd")
const TITLE_SCENE := "res://scenes/main.tscn"
const ITEM_CAPSULE := preload("res://assets/racer/context_v2/item_capsule.png")
const VIEW := Vector2(1280, 720)
const STEP := 1.0 / 60.0
const STICK_DEADZONE := 0.10
const PC_IMP_PACE := 0.89
const VACANT := -1
const KEYBOARD := -2
const P_COLORS := [Color("#71dfeb"), Color("#ffc277")]
const ITEM_ICONS := {
	"zoom": preload("res://assets/racer/icons/zoom.png"),
	"sparkle": preload("res://assets/racer/icons/sparkle.png"),
	"kelp": preload("res://assets/racer/context_v2/kelp_trap.png"),
	"pearls": preload("res://assets/racer/icons/pearls.png"),
}

enum Screen { MODE, GARAGE, COURSE, RACE, RESULT }

var _screen := Screen.MODE
var _count := 1
var _mode_choice := 0
var _course_choice := 0
var _devices: Array[int] = [VACANT, VACANT]
var _drivers: Array[int] = [0, 1]
var _rides: Array[int] = [0, 0]
var _ready_players: Array[bool] = [false, false]
var _items_queued: Array[bool] = [false, false]
var _rearm: Array[bool] = [false, false]
var _race: ReefKartRace
var _second_view: ReefKartRace
var _paused := false
var _elapsed := 0.0
var _stage: Control
var _content: Control
var _panel_labels: Array[Label] = []
var _drive_labels: Array[Label] = []
var _item_icons: Array[TextureRect] = []
var _notice: Label
var _notice_plate: Panel
var _pause_button: Button
var _garage_button: Button


func _ready() -> void:
	var margin := ColorRect.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	margin.color = Color("#102e4c")
	margin.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(margin)
	_stage = Control.new()
	_stage.size = VIEW
	add_child(_stage)
	resized.connect(_fit)
	Input.joy_connection_changed.connect(_controller_connection)
	_fit()
	_show_mode()


func _fit() -> void:
	var factor := minf(size.x / VIEW.x, size.y / VIEW.y)
	_stage.scale = Vector2.ONE * factor
	_stage.position = (size - VIEW * factor) * 0.5


func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT and _screen == Screen.RACE:
		_pause()


func _input(event: InputEvent) -> void:
	if event is InputEventJoypadButton:
		var button := event as InputEventJoypadButton
		get_viewport().set_input_as_handled()
		if button.pressed:
			_pad(button.device, button.button_index)
	elif event is InputEventKey:
		var key := event as InputEventKey
		if key.pressed and not key.echo and _key(key.physical_keycode):
			get_viewport().set_input_as_handled()


func _pad(device: int, button: int) -> void:
	if _screen == Screen.MODE:
		if button in [JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT]:
			_mode_choice = 1 - _mode_choice
			_show_mode()
		elif button == JOY_BUTTON_A:
			_show_garage(_mode_choice + 1, device)
		elif button == JOY_BUTTON_B:
			_leave()
		return
	var slot := _devices.find(device)
	if slot < 0:
		if button == JOY_BUTTON_A:
			_join(device)
		return
	match _screen:
		Screen.GARAGE:
			match button:
				JOY_BUTTON_LEFT_SHOULDER: _choose(slot, true, -1)
				JOY_BUTTON_RIGHT_SHOULDER: _choose(slot, true, 1)
				JOY_BUTTON_DPAD_LEFT: _choose(slot, false, -1)
				JOY_BUTTON_DPAD_RIGHT: _choose(slot, false, 1)
				JOY_BUTTON_A: _toggle_ready(slot)
				JOY_BUTTON_B: _garage_back(slot)
		Screen.COURSE:
			if slot == 0:
				match button:
					JOY_BUTTON_DPAD_LEFT: _choose_course(_course_choice - 1)
					JOY_BUTTON_DPAD_RIGHT: _choose_course(_course_choice + 1)
					JOY_BUTTON_A: _start_race()
					JOY_BUTTON_B: _return_to_garage()
		Screen.RACE:
			if button == JOY_BUTTON_START:
				_toggle_pause()
			elif _paused and button == JOY_BUTTON_B and slot == 0:
				_return_to_garage()
			elif not _paused and button in [JOY_BUTTON_X, JOY_BUTTON_LEFT_SHOULDER]:
				_items_queued[slot] = true
		Screen.RESULT:
			if button == JOY_BUTTON_A:
				_return_to_garage()
			elif button == JOY_BUTTON_B and slot == 0:
				_show_mode()


func _key(key: int) -> bool:
	if _screen == Screen.MODE:
		match key:
			KEY_LEFT, KEY_RIGHT:
				_mode_choice = 1 - _mode_choice
				_show_mode()
			KEY_ENTER, KEY_SPACE: _show_garage(_mode_choice + 1, VACANT)
			KEY_ESCAPE: _leave()
			_: return false
		return true
	if key == KEY_ESCAPE:
		match _screen:
			Screen.GARAGE: _garage_back(0)
			Screen.COURSE: _return_to_garage()
			Screen.RACE:
				if _paused and not _has_all_players():
					_return_to_garage()
				else:
					_toggle_pause()
			Screen.RESULT: _return_to_garage()
		return true
	if _devices[0] != KEYBOARD:
		return false
	match _screen:
		Screen.GARAGE:
			match key:
				KEY_Q: _choose(0, true, -1)
				KEY_E: _choose(0, true, 1)
				KEY_LEFT: _choose(0, false, -1)
				KEY_RIGHT: _choose(0, false, 1)
				KEY_ENTER: _toggle_ready(0)
				_: return false
		Screen.COURSE:
			match key:
				KEY_LEFT: _choose_course(_course_choice - 1)
				KEY_RIGHT: _choose_course(_course_choice + 1)
				KEY_ENTER, KEY_SPACE: _start_race()
				_: return false
		Screen.RACE:
			if key in [KEY_SPACE, KEY_ENTER] and not _paused:
				_items_queued[0] = true
			else:
				return false
		Screen.RESULT:
			if key == KEY_ENTER:
				_return_to_garage()
			else:
				return false
	return true


func _controller_connection(device: int, connected: bool) -> void:
	if connected:
		return
	var slot := _devices.find(device)
	if slot < 0:
		return
	_devices[slot] = VACANT
	_ready_players[slot] = false
	_items_queued[slot] = false
	if _screen == Screen.GARAGE:
		_build_garage()
	elif _screen == Screen.COURSE:
		_return_to_garage()
	elif _screen == Screen.RACE:
		_pause()


func _join(device: int) -> void:
	if device < 0 or device in _devices:
		return
	for slot in range(_count):
		if _devices[slot] == VACANT or (_count == 1 and _devices[slot] == KEYBOARD and _screen == Screen.GARAGE):
			_devices[slot] = device
			if _screen == Screen.GARAGE:
				_ready_players[slot] = false
				_build_garage()
			elif _screen == Screen.RACE:
				_update_notice()
			return


func _has_all_players() -> bool:
	for slot in range(_count):
		if _devices[slot] == VACANT:
			return false
	return true


func _show_mode() -> void:
	_screen = Screen.MODE
	_reset_content()
	_menu_backdrop()
	_label(_content, "REEF GRAND PRIX", Rect2(0, 94, 1280, 86), 63)
	_label(_content, "Four room circuits", Rect2(0, 180, 1280, 55), 32)
	_button(_content, "1 PLAYER\nRace the Imp", Rect2(236, 292, 380, 155),
		_show_garage.bind(1, VACANT), _mode_choice == 0)
	_button(_content, "2 PLAYERS\nSplit-screen race", Rect2(664, 292, 380, 155),
		_show_garage.bind(2, VACANT), _mode_choice == 1)
	_label(_content, "D-pad to choose  ·  A to confirm  ·  Two controllers for split-screen",
		Rect2(0, 486, 1280, 58), 23)
	_button(_content, "Back", Rect2(34, 626, 180, 66), _leave)


func _show_garage(count: int, first_device: int) -> void:
	_count = count
	_devices = [first_device if first_device >= 0 else (KEYBOARD if count == 1 else VACANT), VACANT]
	_return_to_garage()


func _return_to_garage() -> void:
	_screen = Screen.GARAGE
	_ready_players = [false, false]
	_build_garage()


func _build_garage() -> void:
	_reset_content()
	_menu_backdrop()
	_label(_content, "CHOOSE YOUR DRIVER & RIDE", Rect2(0, 18, 1280, 76), 41)
	for slot in range(_count):
		_garage_panel(slot)
	_label(_content, "LB / RB  Driver    ·    D-pad  Ride    ·    A  Ready",
		Rect2(174, 628, 932, 32), 23)
	if _count == 1:
		_label(_content, "Keyboard  Q / E  Driver    ·    ← / →  Ride    ·    Enter  Ready",
			Rect2(174, 665, 932, 28), 20)
	_button(_content, "Back", Rect2(27, 631, 138, 63), _show_mode)


func _garage_panel(slot: int) -> void:
	var x := 366.0 if _count == 1 else 48.0 + slot * 616.0
	var area := Rect2(x, 103, 548, 501)
	_panel(_content, area, Color("#17405a"), P_COLORS[slot])
	var driver := Catalog.driver(_drivers[slot])
	var ride: Dictionary = Catalog.RIDES[_rides[slot]]
	var linked := _devices[slot] != VACANT
	var device_label := "Press A to join"
	if linked:
		device_label = "Keyboard / mouse" if _devices[slot] == KEYBOARD else "Controller connected"
	_label(_content, "PLAYER %d  ·  %s" % [slot + 1, device_label],
		Rect2(x + 12, 115, 524, 48), 21, P_COLORS[slot])
	_picture(_content, Catalog.portrait(driver), Rect2(x + 78, 172, 183, 190))
	var body := load("res://assets/kart/chase/empty_%s.png" % ride["id"]) as Texture2D
	_picture(_content, body, Rect2(x + 287, 174, 184, 185))
	_label(_content, String(driver["name"]), Rect2(x + 36, 366, 246, 46), 25)
	_label(_content, String(ride["name"]), Rect2(x + 278, 366, 235, 46), 25)
	_button(_content, "←", Rect2(x + 15, 235, 58, 64), _choose.bind(slot, true, -1))
	_button(_content, "→", Rect2(x + 228, 235, 55, 64), _choose.bind(slot, true, 1))
	_button(_content, "←", Rect2(x + 292, 424, 55, 53), _choose.bind(slot, false, -1))
	_button(_content, "→", Rect2(x + 472, 424, 55, 53), _choose.bind(slot, false, 1))
	_label(_content, "Speed  " + "●".repeat(int(ride["speed"])) + "○".repeat(5 - int(ride["speed"])),
		Rect2(x + 27, 422, 246, 29), 20)
	_label(_content, "Steering  " + "●".repeat(int(ride["steering"])) + "○".repeat(5 - int(ride["steering"])),
		Rect2(x + 27, 453, 246, 29), 20)
	_label(_content, String(ride["tip"]), Rect2(x + 24, 487, 500, 32), 19)
	var ready_label := "Ready ✓" if _ready_players[slot] else ("Ready" if linked else "Waiting for controller")
	var ready := _button(_content, ready_label, Rect2(x + 95, 534, 358, 54), _toggle_ready.bind(slot), _ready_players[slot])
	ready.disabled = not linked


func _choose(slot: int, driver: bool, delta: int) -> void:
	if _ready_players[slot]:
		return
	if driver:
		_drivers[slot] = posmod(_drivers[slot] + delta, Catalog.driver_count())
	else:
		_rides[slot] = posmod(_rides[slot] + delta, Catalog.RIDES.size())
	_build_garage()


func _garage_back(slot: int) -> void:
	if _ready_players[slot]:
		_ready_players[slot] = false
		_build_garage()
	elif slot == 0:
		_show_mode()


func _toggle_ready(slot: int) -> void:
	if _devices[slot] == VACANT:
		return
	_ready_players[slot] = not _ready_players[slot]
	if _ready_players[0] and (_count == 1 or _ready_players[1]) and _has_all_players():
		_show_courses()
	else:
		_build_garage()


func _choose_course(index: int) -> void:
	_course_choice = posmod(index, Courses.COURSES.size())
	_show_courses()


func _show_courses() -> void:
	_screen = Screen.COURSE
	_reset_content()
	_menu_backdrop()
	_label(_content, "CHOOSE A COURSE", Rect2(0, 25, 1280, 70), 47)
	_label(_content, "Player 1 chooses  ·  D-pad or ← / →  ·  A or Enter to race",
		Rect2(0, 97, 1280, 46), 24)
	for index in range(Courses.COURSES.size()):
		var course: Dictionary = Courses.COURSES[index]
		var x := 34.0 + float(index) * 307.0
		var selected := index == _course_choice
		var palette: Array = course["palette"]
		_button(_content, "", Rect2(x, 163, 291, 374), _choose_course.bind(index), selected)
		_label(_content, "%d  ·  %s" % [index + 1, course["room"]],
			Rect2(x + 10, 181, 271, 37), 22, Color("#332354"))
		_picture(_content, Courses.room_art(course), Rect2(x + 20, 218, 251, 142))
		_panel(_content, Rect2(x + 25, 372, 241, 105), Color("#193651"), palette[2])
		_draw_course_map(course["points"], Rect2(x + 50, 382, 191, 85), palette[2])
		_label(_content, String(course["name"]), Rect2(x + 7, 488, 277, 36), 22, Color("#332354"))
	var chosen: Dictionary = Courses.COURSES[_course_choice]
	_label(_content, String(chosen["hint"]), Rect2(168, 548, 944, 46), 26)
	_button(_content, "Back", Rect2(32, 629, 155, 62), _return_to_garage)
	_button(_content, "Race!", Rect2(490, 613, 300, 74), _start_race, true)


func _draw_course_map(points: Array, area: Rect2, paint: Color) -> void:
	var bounds := Rect2(points[0], Vector2.ZERO)
	for point: Vector2 in points:
		bounds = bounds.expand(point)
	var scale := minf(area.size.x / bounds.size.x, area.size.y / bounds.size.y)
	var offset := area.get_center() - bounds.get_center() * scale
	var route := Line2D.new()
	route.width = 4.0
	route.antialiased = true
	route.default_color = paint
	route.joint_mode = Line2D.LINE_JOINT_ROUND
	route.closed = true
	for point: Vector2 in points:
		route.add_point(offset + point * scale)
	_content.add_child(route)
	var start := offset + (points[0] as Vector2) * scale
	var dot := ColorRect.new()
	dot.color = Color.WHITE
	dot.size = Vector2(6, 6)
	dot.position = start - dot.size * 0.5
	dot.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_content.add_child(dot)


func _start_race() -> void:
	if not _has_all_players():
		_return_to_garage()
		return
	_screen = Screen.RACE
	_reset_content()
	_paused = false
	_elapsed = 0.0
	_items_queued = [false, false]
	_rearm = [false, false]
	var roster: Array = [Catalog.spec(_drivers[0], _rides[0], 0)]
	if _count == 2:
		roster.append(Catalog.spec(_drivers[1], _rides[1], 1))
	else:
		roster.append({"id": "imp", "player": false, "skill": PC_IMP_PACE})
	_race = Race.new()
	_race.setup({"racers": roster, "duel": _count == 2, "course": Courses.COURSES[_course_choice],
		"pc_handling": true})
	var pane := 640 if _count == 2 else 1280
	_race.use_pc_hud(pane)
	_add_view(_race, 0, pane)
	if _count == 2:
		_second_view = Race.new()
		_second_view.setup_camera_view(_race, 1)
		_second_view.use_pc_hud(pane)
		_add_view(_second_view, 1, pane)
		_panel(_content, Rect2(638, 0, 4, 720), Color("#b9eef0"), Color("#b9eef0"), 0)
	_panel_labels.clear()
	_drive_labels.clear()
	_item_icons.clear()
	for slot in range(_count):
		var x := float(slot * pane)
		_panel(_content, Rect2(x + 22, 16, 456, 64), Color("#183e61"), P_COLORS[slot])
		_panel_labels.append(_label(_content, "", Rect2(x + 34, 19, 428, 56), 23))
		_drive_labels.append(_label(_content, "", Rect2(x + 30, 80, 444, 34), 22, Color("#ffe6a4")))
		var item_x := x + (float(pane) - 114.0 if slot == 1 else 30.0)
		_panel(_content, Rect2(item_x, 609, 84, 84), Color("#183e61"), P_COLORS[slot], 42)
		_item_icons.append(_picture(_content, null, Rect2(item_x + 12, 621, 60, 60)))
	_notice_plate = _panel(_content, Rect2(216, 235, 848, 153), Color("#173653"), Color("#80d6ea"))
	_notice_plate.hide()
	_notice = _label(_content, "", Rect2(180, 229, 920, 170), 35)
	var guide := "Left stick  Steer   ·   A / RT  Gas   ·   B / LT  Brake & reverse   ·   RB  Drift   ·   X / LB  Item"
	if _devices[0] == KEYBOARD:
		guide = "← / →  Steer   ·   W / ↑  Gas   ·   S / ↓  Brake & reverse   ·   Shift  Drift   ·   Space  Item"
	_panel(_content, Rect2(220, 603, 840, 36), Color(0.08, 0.20, 0.30, 0.91), Color("#78abbf"), 13)
	_label(_content, guide, Rect2(220, 603, 840, 36), 19)
	_pause_button = _button(_content, "Pause", Rect2(546, 648, 188, 56), _toggle_pause)
	_garage_button = _button(_content, "Garage", Rect2(755, 648, 172, 56), _return_to_garage)
	_garage_button.hide()
	_race.begin()
	_update_race_ui()


func _add_view(view: ReefKartRace, slot: int, width: int) -> void:
	var viewport := SubViewport.new()
	viewport.size = Vector2i(width, 720)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	viewport.world_2d = World2D.new()
	var screen := SubViewportContainer.new()
	screen.position.x = float(slot * width)
	screen.size = Vector2(width, 720)
	screen.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_content.add_child(screen)
	screen.add_child(viewport)
	viewport.add_child(view)
	view.position.x = -(VIEW.x - float(width)) * 0.5


func _physics_process(delta: float) -> void:
	if _screen != Screen.RACE or _paused or not is_instance_valid(_race):
		return
	_elapsed += minf(delta, 0.1)
	while _elapsed >= STEP and _screen == Screen.RACE:
		_elapsed -= STEP
		var active := _race.state == "race"
		var command := _controls_for(0)
		if _count == 2:
			command["second"] = _controls_for(1)
		_race.step_race(STEP, command)
		if active:
			_items_queued = [false, false]
		if _second_view != null:
			_second_view.refresh_camera_view(_race, STEP)
		if _race.state == "finished":
			_show_result()
	_update_race_ui()


static func steer_from_axis(axis: float, deadzone: float = STICK_DEADZONE) -> float:
	return signf(axis) * clampf((absf(axis) - deadzone) / (1.0 - deadzone), 0.0, 1.0)


func _controls_for(slot: int) -> Dictionary:
	var device := _devices[slot]
	var steer := 0.0
	var brake := false
	var throttle := 0.0
	var drift := false
	if device == KEYBOARD:
		steer = float(int(Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D))
			- int(Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A)))
		brake = Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S)
		throttle = float(Input.is_physical_key_pressed(KEY_UP) or Input.is_physical_key_pressed(KEY_W))
		drift = Input.is_physical_key_pressed(KEY_SHIFT)
	elif device >= 0:
		steer = steer_from_axis(Input.get_joy_axis(device, JOY_AXIS_LEFT_X))
		var dpad := int(Input.is_joy_button_pressed(device, JOY_BUTTON_DPAD_RIGHT)) - int(Input.is_joy_button_pressed(device, JOY_BUTTON_DPAD_LEFT))
		if dpad != 0:
			steer = float(dpad)
		brake = Input.is_joy_button_pressed(device, JOY_BUTTON_B) or Input.get_joy_axis(device, JOY_AXIS_TRIGGER_LEFT) > 0.35
		throttle = 1.0 if Input.is_joy_button_pressed(device, JOY_BUTTON_A) else maxf(0.0, Input.get_joy_axis(device, JOY_AXIS_TRIGGER_RIGHT))
		drift = Input.is_joy_button_pressed(device, JOY_BUTTON_RIGHT_SHOULDER)
	if _rearm[slot]:
		_rearm[slot] = brake or throttle > 0.05 or drift or not is_zero_approx(steer)
		return {}
	return {"steer": steer, "brake": brake, "throttle": throttle, "drift": drift, "item_pressed": _items_queued[slot]}


func _pause() -> void:
	_paused = true
	_items_queued = [false, false]
	_rearm = [true, true]
	if is_instance_valid(_race):
		_race.cancel_pc_input()
	_elapsed = 0.0
	_update_notice()


func _toggle_pause() -> void:
	if not _paused:
		_pause()
	elif _has_all_players():
		_paused = false
		_update_notice()


func _update_notice() -> void:
	if not is_instance_valid(_notice):
		return
	_pause_button.text = "Resume" if _paused else "Pause"
	_pause_button.disabled = _paused and not _has_all_players()
	_notice_plate.visible = _paused
	_garage_button.visible = _paused
	if _paused:
		_notice.text = "PAUSED\nStart or Esc to resume  ·  P1 B for garage" if _has_all_players() else "CONTROLLER DISCONNECTED\nPress A to rejoin  ·  Esc for garage"
	else:
		_notice.text = ""


func _update_race_ui() -> void:
	if _screen != Screen.RACE:
		return
	for slot in range(_count):
		var kart: Dictionary = _race.karts[slot]
		var driver := Catalog.driver(_drivers[slot])
		var lap := mini(ReefKartRace.LAPS, int(kart["lap"]) + 1)
		_panel_labels[slot].text = "P%d  %s   ·   Lap %d/%d   ·   ◉ %d" % [
			slot + 1, driver["name"], lap, ReefKartRace.LAPS, int(kart["pearls"])]
		_item_icons[slot].texture = ITEM_CAPSULE if float(kart["roulette_t"]) > 0.0 else ITEM_ICONS.get(String(kart["item"])) as Texture2D
		var cue := "WRONG WAY" if bool(kart["wrong_way"]) else ""
		if _rearm[slot] and not _paused:
			cue = "RELEASE CONTROLS TO DRIVE"
		if float(kart["drift_dir"]) != 0.0:
			cue = "BOOST READY" if float(kart["drift_charge"]) >= float(_race._pc_tune["charge"]) else "DRIFT"
		_drive_labels[slot].text = cue
	if _paused:
		return
	match _race.state:
		"countdown": _notice.text = str(maxi(1, ceili(_race.clock * 2.0)))
		"imp_beat": _notice.text = "The Imp won this race!\nYour pearls are safe"
		_: _notice.text = "GO!" if _race.go_t > 0.0 else ""


func _show_result() -> void:
	_screen = Screen.RESULT
	_pause_button.hide()
	_garage_button.hide()
	_notice.hide()
	_notice_plate.hide()
	var winner := _race.winner_slot
	var driver := Catalog.driver(_drivers[winner])
	_panel(_content, Rect2(337, 174, 606, 340), Color("#17405a"), P_COLORS[winner])
	_picture(_content, Catalog.portrait(driver), Rect2(510, 185, 260, 150))
	_label(_content, "%s wins!" % driver["name"], Rect2(363, 326, 554, 56), 45)
	_label(_content, String(_race.track.room["name"]), Rect2(363, 380, 554, 31), 22)
	_button(_content, "Race again", Rect2(385, 424, 242, 66), _return_to_garage, true)
	_button(_content, "Menu", Rect2(653, 424, 242, 66), _show_mode)


func _leave() -> void:
	get_tree().change_scene_to_file(TITLE_SCENE)


func _reset_content() -> void:
	if is_instance_valid(_content):
		_stage.remove_child(_content)
		_content.queue_free()
	_race = null
	_second_view = null
	_notice = null
	_content = Control.new()
	_content.size = VIEW
	_stage.add_child(_content)


func _menu_backdrop() -> void:
	_panel(_content, Rect2(Vector2.ZERO, VIEW), Color("#102e4c"), Color("#102e4c"), 0)
	var sky := AtlasTexture.new()
	sky.atlas = load(ReefKartTrack.PAINTED_SKYLINE) as Texture2D
	sky.region = Rect2(0, 28, 2048, 228)
	var art := _picture(_content, sky, Rect2(0, 116, 1280, 420))
	art.stretch_mode = TextureRect.STRETCH_SCALE
	art.modulate = Color(1, 1, 1, 0.55)


func _panel(parent: Control, rect: Rect2, color: Color, line: Color, radius: int = 24) -> Panel:
	var node := Panel.new()
	node.position = rect.position
	node.size = rect.size
	node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.border_color = line
	style.set_border_width_all(2)
	style.set_corner_radius_all(radius)
	node.add_theme_stylebox_override("panel", style)
	parent.add_child(node)
	return node


func _picture(parent: Control, texture: Texture2D, rect: Rect2) -> TextureRect:
	var node := TextureRect.new()
	node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	node.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	node.texture = texture
	node.position = rect.position
	node.size = rect.size
	node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(node)
	return node


func _label(parent: Control, words: String, rect: Rect2, font_size: int, color: Color = Color.WHITE) -> Label:
	var node := Label.new()
	node.text = words
	node.position = rect.position
	node.size = rect.size
	node.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	node.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(node, font_size, color, 3)
	parent.add_child(node)
	return node


func _button(parent: Control, words: String, rect: Rect2, action: Callable, selected: bool = false) -> Button:
	var node := Button.new()
	node.text = words
	node.position = rect.position
	node.size = rect.size
	node.focus_mode = Control.FOCUS_NONE
	StorybookUI.style_button(node, "gold" if selected else "primary", 23, 20)
	node.pressed.connect(action)
	parent.add_child(node)
	return node
