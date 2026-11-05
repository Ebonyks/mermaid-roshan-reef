extends SceneTree

const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const Catalog := preload("res://scripts/racer/reef_kart_catalog.gd")
const STEP := 1.0 / 60.0
var failures := 0


func _initialize() -> void:
	call_deferred("_run")


func check(name: String, passed: bool) -> void:
	print("REEF_KART_PC|", "PASS" if passed else "FAIL", "|", name)
	if not passed:
		failures += 1


func button(device: int, key: int, pressed: bool) -> void:
	var event := InputEventJoypadButton.new()
	event.device = device
	event.button_index = key
	event.pressed = pressed
	Input.parse_input_event(event)
	Input.flush_buffered_events()


func tap(device: int, key: int) -> void:
	button(device, key, true)
	button(device, key, false)


func axis(device: int, value: float) -> void:
	var event := InputEventJoypadMotion.new()
	event.device = device
	event.axis = JOY_AXIS_LEFT_X
	event.axis_value = value
	Input.parse_input_event(event)
	Input.flush_buffered_events()


func _run() -> void:
	var pc := Scene.instantiate() as PC
	root.add_child(pc)
	pc.set_physics_process(false)
	await process_frame
	var catalog_ok := true
	for i in range(Catalog.driver_count()):
		var driver := Catalog.driver(i)
		catalog_ok = catalog_ok and ResourceLoader.exists(driver["sprite"])
		var texture := load(String(driver["sprite"])) as Texture2D
		var crop: Rect2 = driver["crop"]
		catalog_ok = catalog_ok and Rect2(Vector2.ZERO, texture.get_size()).encloses(crop)
	check("all twelve existing drivers have valid selection art and cockpit crops", catalog_ok)
	tap(6, JOY_BUTTON_DPAD_RIGHT)
	tap(6, JOY_BUTTON_A)
	tap(11, JOY_BUTTON_A)
	check("two separate devices claim the two seats", pc._devices == [6, 11])
	tap(6, JOY_BUTTON_DPAD_RIGHT)
	tap(11, JOY_BUTTON_DPAD_LEFT)
	tap(11, JOY_BUTTON_RIGHT_SHOULDER)
	check("vehicle and driver choices stay on their own side",
		pc._rides == [1, 2] and pc._drivers == [0, 2])
	tap(6, JOY_BUTTON_A)
	check("one player cannot launch a two-player race", pc._race == null and pc._ready_players == [true, false])
	tap(11, JOY_BUTTON_A)
	var race: ReefKartRace = pc._race
	var second: ReefKartRace = pc._second_view
	check("two cameras are bound to the same race and different drivers",
		second != null and is_same(race.track, second.track)
		and is_same(second._pl, race.karts[1]) and not is_same(second._pl, race._pl))
	var a: Dictionary = race.karts[0]
	var b: Dictionary = race.karts[1]
	a["track_s"] = race.track.s_of(4)
	b["track_s"] = a["track_s"]
	check("cycle has more straight-line speed and truck has more steering authority",
		race._top_speed(a, ReefKartTrack.Terrain.ROAD) > race._top_speed(b, ReefKartTrack.Terrain.ROAD)
		and float(a["turn_rate"]) < float(b["turn_rate"]))
	race._place_grid()
	for i in range(96):
		pc._physics_process(STEP)
	axis(6, -0.85)
	axis(11, 0.78)
	check("stick axes are read by device", float(pc._controls_for(0)["steer"]) < -0.5
		and float(pc._controls_for(1)["steer"]) > 0.5)
	button(6, JOY_BUTTON_B, true)
	tap(11, JOY_BUTTON_A)
	for i in range(24):
		pc._physics_process(STEP)
	button(6, JOY_BUTTON_B, false)
	check("P1 braking and P2 item fire affect only their own kart",
		float(a["speed"]) < float(b["speed"]) and String(a["item"]) == "zoom"
		and String(b["item"]) == "" and float(b["boost_t"]) > 0.0)
	axis(6, 0.0)
	axis(11, 0.0)
	pc._controller_connection(11, false)
	var before := race.race_time
	for i in range(15):
		pc._physics_process(STEP)
	check("disconnect pauses both racers without advancing time",
		pc._paused and pc._devices[1] == -1 and is_equal_approx(before, race.race_time))
	tap(6, JOY_BUTTON_A)
	check("P1 cannot claim P2's missing seat", pc._devices == [6, -1])
	tap(13, JOY_BUTTON_A)
	check("replacement controller rejoins the vacant seat while paused", pc._devices == [6, 13] and pc._paused)
	tap(13, JOY_BUTTON_START)
	check("both reconnected players resume on Start", not pc._paused)
	# Keep the faster P1 stopped long enough for P2 to win by driving the
	# complete course. This exercises the public race loop and result screen.
	button(6, JOY_BUTTON_B, true)
	for i in range(3600):
		pc._physics_process(STEP)
		if race.winner_slot >= 0:
			break
	button(6, JOY_BUTTON_B, false)
	check("P2 can finish the complete race and reach the results screen",
		race.winner_slot == 1 and bool(b["finished"]) and pc._screen == PC.Screen.RESULT)
	tap(13, JOY_BUTTON_A)
	check("race again preserves device assignments and returns to a fresh garage",
		pc._screen == PC.Screen.GARAGE and pc._devices == [6, 13]
		and pc._race == null and pc._ready_players == [false, false])
	tap(6, JOY_BUTTON_A)
	tap(13, JOY_BUTTON_A)
	pc._controller_connection(6, false)
	pc._controller_connection(13, false)
	pc._key(KEY_ESCAPE)
	check("keyboard can return to garage when both controllers are disconnected",
		pc._screen == PC.Screen.GARAGE and pc._race == null)
	pc._show_mode()
	pc._show_garage(1, -1)
	check("solo has keyboard fallback", pc._devices == [-2, -1])
	pc._toggle_ready(0)
	var solo: ReefKartRace = pc._race
	for i in range(4200):
		pc._physics_process(STEP)
		if solo.winner_slot >= 0:
			break
	check("solo keeps the Imp opponent and completes a real two-lap race",
		solo.winner_slot == 0 and solo.karts[1]["id"] == "imp" and pc._screen == PC.Screen.RESULT)
	pc.queue_free()
	await process_frame
	print("REEF_KART_PC|DONE|failures=", failures)
	quit(0 if failures == 0 else 1)
