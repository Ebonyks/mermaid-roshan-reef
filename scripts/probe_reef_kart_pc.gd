extends SceneTree

const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const Catalog := preload("res://scripts/racer/reef_kart_catalog.gd")
const Courses := preload("res://scripts/racer/reef_kart_courses.gd")
const Handling := preload("res://scripts/probe_reef_kart_handling.gd")
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


func axis(device: int, value: float, channel: int = JOY_AXIS_LEFT_X) -> void:
	var event := InputEventJoypadMotion.new()
	event.device = device
	event.axis = channel
	event.axis_value = value
	Input.parse_input_event(event)
	Input.flush_buffered_events()


func key_input(code: int, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)
	Input.flush_buffered_events()


func apply_pilot(device: int, race: ReefKartRace, kart: Dictionary) -> void:
	var command := Handling.pilot(race, kart)
	var steer := float(command["steer"])
	var raw := signf(steer) * (PC.STICK_DEADZONE + (1.0 - PC.STICK_DEADZONE) * absf(steer))
	axis(device, raw)
	axis(device, float(command["throttle"]), JOY_AXIS_TRIGGER_RIGHT)
	button(device, JOY_BUTTON_B, bool(command["brake"]))


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
	check("both ready opens the four-course picker", pc._screen == PC.Screen.COURSE
		and Courses.COURSES.size() == 4 and pc._race == null)
	tap(11, JOY_BUTTON_DPAD_RIGHT)
	tap(11, JOY_BUTTON_A)
	check("P2 cannot change or start P1's course", pc._course_choice == 0 and pc._race == null)
	tap(6, JOY_BUTTON_DPAD_RIGHT)
	check("P1 can select the next course", pc._course_choice == 1)
	tap(6, JOY_BUTTON_DPAD_LEFT)
	tap(6, JOY_BUTTON_A)
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
	check("simultaneous starting boosts share one spoken instruction",
		race.item_voice != null and race.item_voice.playing and race.item_voice.pending.is_empty()
		and race.item_voice.starts.size() == 1 and race.item_voice.active["kind"] == "zoom")
	for kind: String in ReefKartRace.ITEM_KINDS:
		race.item_voice.clear()
		race.item_voice.award(0, "pearls" if kind == "zoom" else "zoom")
		b["item"] = ""
		b["pending"] = kind
		b["roulette_t"] = STEP * 0.5
		race._contact_features(b, STEP)
		var pending: Array = race.item_voice.pending
		check("P2 receives exact spoken explanation for " + kind,
			not pending.is_empty() and pending[-1]["kind"] == kind and pending[-1]["slot"] == 1)
	b["item"] = "pearls"
	tap(11, JOY_BUTTON_X)
	pc._physics_process(STEP)
	check("using P2's item removes its waiting instruction without interrupting P1",
		String(b["item"]).is_empty() and race.item_voice.pending.is_empty()
		and race.item_voice.playing and race.item_voice.active["slot"] == 0)
	b["pearls"] = 0
	race.item_voice.award(1, "sparkle")
	race.item_voice.skip()
	check("two-human sparkle guidance names a racer rather than an absent imp",
		race.item_voice.playing and race.item_voice.stream.resource_path.ends_with("guide_kart_sparkle_duel.ogg"))
	var skip_touch := InputEventScreenTouch.new()
	skip_touch.pressed = true
	skip_touch.position = pc._item_icons[1].get_global_rect().get_center()
	pc._input(skip_touch)
	check("touching P2's actual item icon skips the shared explanation",
		not race.item_voice.playing and race.item_voice.pending.is_empty())
	race.item_voice.award(0, "zoom")
	b["item"] = "zoom"
	check("PC countdown ends with both unpowered karts stationary",
		is_zero_approx(float(a["speed"])) and is_zero_approx(float(b["speed"])))
	axis(11, 0.03, JOY_AXIS_TRIGGER_RIGHT)
	var idle_pos: Vector2 = b["pos"]
	for i in range(60):
		pc._physics_process(STEP)
	check("resting trigger noise leaves P2 stationary",
		is_zero_approx(float(pc._controls_for(1)["throttle"])) and idle_pos.is_equal_approx(b["pos"]))
	axis(11, 0.5, JOY_AXIS_TRIGGER_RIGHT)
	check("partial trigger travel remains analog above the deadzone",
		is_equal_approx(float(pc._controls_for(1)["throttle"]), (0.5 - 0.05) / 0.95))
	axis(11, 0.0, JOY_AXIS_TRIGGER_RIGHT)
	axis(6, 0.18)
	check("small stick input survives the new controller deadzone", float(pc._controls_for(0)["steer"]) > 0.08)
	axis(6, -0.85)
	axis(11, 0.78)
	check("stick axes are read by device", float(pc._controls_for(0)["steer"]) < -0.5
		and float(pc._controls_for(1)["steer"]) > 0.5)
	button(6, JOY_BUTTON_A, true)
	axis(11, 1.0, JOY_AXIS_TRIGGER_RIGHT)
	check("A and RT supply throttle to separate seats", pc._controls_for(0)["throttle"] == 1.0
		and pc._controls_for(1)["throttle"] == 1.0)
	button(6, JOY_BUTTON_B, true)
	tap(11, JOY_BUTTON_X)
	for i in range(24):
		pc._physics_process(STEP)
	button(6, JOY_BUTTON_B, false)
	button(6, JOY_BUTTON_A, false)
	axis(11, 0.0, JOY_AXIS_TRIGGER_RIGHT)
	check("P1 braking and P2 item fire affect only their own kart",
		float(a["speed"]) < float(b["speed"]) and String(a["item"]) == "zoom"
		and String(b["item"]) == "" and float(b["boost_t"]) > 0.0)
	axis(6, 0.0)
	button(11, JOY_BUTTON_RIGHT_SHOULDER, true)
	pc._physics_process(STEP)
	check("P2 can initiate drift with RB", float(b["drift_dir"]) != 0.0 and float(a["drift_dir"]) == 0.0)
	axis(11, 0.0)
	pc._controller_connection(11, false)
	button(11, JOY_BUTTON_RIGHT_SHOULDER, false)
	check("disconnect clears playing and queued item explanations",
		not race.item_voice.playing and race.item_voice.pending.is_empty())
	check("disconnect clears an active drift", float(b["drift_dir"]) == 0.0 and float(b["drift_charge"]) == 0.0)
	var before := race.race_time
	for i in range(15):
		pc._physics_process(STEP)
	check("disconnect pauses both racers without advancing time",
		pc._paused and pc._devices[1] == -1 and is_equal_approx(before, race.race_time))
	tap(6, JOY_BUTTON_A)
	check("P1 cannot claim P2's missing seat", pc._devices == [6, -1])
	tap(13, JOY_BUTTON_A)
	check("replacement controller rejoins the vacant seat while paused", pc._devices == [6, 13] and pc._paused)
	button(13, JOY_BUTTON_A, true)
	tap(13, JOY_BUTTON_START)
	check("both reconnected players resume on Start", not pc._paused)
	check("held accelerator is ignored until released after resume", pc._controls_for(1).is_empty())
	button(13, JOY_BUTTON_A, false)
	axis(13, 0.06, JOY_AXIS_TRIGGER_RIGHT)
	check("partly held trigger cannot rearm the accelerator on resume",
		pc._controls_for(1).is_empty() and pc._rearm[1])
	axis(13, 0.0, JOY_AXIS_TRIGGER_RIGHT)
	# The same simulated gamepad events available to a real player drive two laps.
	pc._physics_process(STEP)
	for i in range(4200):
		apply_pilot(13, race, b)
		pc._physics_process(STEP)
		if race.winner_slot >= 0:
			break
	axis(13, 0.0)
	axis(13, 0.0, JOY_AXIS_TRIGGER_RIGHT)
	button(13, JOY_BUTTON_B, false)
	check("P2 can finish the complete race and reach the results screen",
		race.winner_slot == 1 and bool(b["finished"]) and pc._screen == PC.Screen.RESULT)
	tap(13, JOY_BUTTON_A)
	check("race again preserves device assignments and returns to a fresh garage",
		pc._screen == PC.Screen.GARAGE and pc._devices == [6, 13]
		and pc._race == null and pc._ready_players == [false, false])
	tap(6, JOY_BUTTON_A)
	tap(13, JOY_BUTTON_A)
	pc._controller_connection(13, false)
	check("controller loss on course selection returns to garage",
		pc._screen == PC.Screen.GARAGE and pc._devices == [6, -1])
	tap(13, JOY_BUTTON_A)
	tap(6, JOY_BUTTON_A)
	tap(13, JOY_BUTTON_A)
	tap(6, JOY_BUTTON_A)
	pc._controller_connection(6, false)
	pc._controller_connection(13, false)
	pc._key(KEY_ESCAPE)
	check("keyboard can return to garage when both controllers are disconnected",
		pc._screen == PC.Screen.GARAGE and pc._race == null)
	pc._show_garage(1, -1)
	check("solo has keyboard fallback", pc._devices == [-2, -1])
	pc._key(KEY_ENTER)
	pc._key(KEY_ENTER)
	key_input(KEY_W, true)
	check("W controls keyboard throttle", pc._controls_for(0)["throttle"] == 1.0)
	key_input(KEY_W, false)
	for index in range(Courses.COURSES.size()):
		pc._show_mode()
		pc._show_garage(1, 6)
		tap(6, JOY_BUTTON_A)
		while pc._course_choice != index:
			tap(6, JOY_BUTTON_DPAD_RIGHT)
		tap(6, JOY_BUTTON_A)
		var solo: ReefKartRace = pc._race
		var spec: Dictionary = Courses.COURSES[index]
		var track := solo.track
		var course_ok: bool = track.id == spec["id"] and solo._room_art != null \
			and track.landmarks.size() >= 8 and track.gate_s.size() == spec["items"].size()
		for landmark: Dictionary in track.landmarks:
			course_ok = course_ok and solo._landmark_tex.has(String(landmark["id"]))
		for item: Dictionary in track.bubbles:
			var road_pos := track.project(item["pos"], item["s"], 50.0)
			course_ok = course_ok and absf(road_pos.y - float(item["lat"])) < 4.0
		check("%s uses its own art, landmarks and road-aligned item rows" % track.id, course_ok)
		var zone_counts := [0, 0, 0, 0]
		var distinct: Dictionary = {}
		var towel_count := 0
		for landmark: Dictionary in track.landmarks:
			if landmark.has("zone"):
				zone_counts[int(landmark["zone"])] += 1
				distinct[String(landmark["id"])] = true
				towel_count += int(String(landmark["id"]) == "pool_towel_cabinet")
		check("%s has four authored sections with room fixtures" % track.id,
			track.room["zones"].size() == 4 and zone_counts.min() >= 2 and distinct.size() >= 5)
		var phase_field := track.floor_field().get_image()
		var phase_matches := true
		for sample in range(0, ReefKartTrack.SAMPLES, 17):
			var pixel: Vector2i = Vector2i(track.center[sample] / track.world_size * float(phase_field.get_width()))
			var encoded := phase_field.get_pixelv(pixel)
			var decoded := atan2(encoded.b * 2.0 - 1.0, encoded.g * 2.0 - 1.0)
			var expected := TAU * float(sample) / float(ReefKartTrack.SAMPLES)
			phase_matches = phase_matches and absf(wrapf(decoded - expected, -PI, PI)) < 0.035
		check("%s floor sections follow the driven route, including the lap seam" % track.id, phase_matches)
		if track.id == "mermaid_pool":
			check("pool towel cabinet is a world fixture in the changing alcove",
				distinct.has("pool_towel_cabinet") and towel_count == 1 and zone_counts[0] >= 2)
		var field := track.floor_field().get_image()
		var field_ok := field.get_width() == 512
		var outside_count := 0
		for sample in range(0, ReefKartTrack.SAMPLES, 24):
			var center: Vector2 = track.center[sample]
			var cx := clampi(int(center.x / track.world_size * field.get_width()), 0, field.get_width() - 1)
			var cy := clampi(int(center.y / track.world_size * field.get_height()), 0, field.get_height() - 1)
			field_ok = field_ok and field.get_pixel(cx, cy).r < 0.10
			for side: float in [-1.0, 1.0]:
				var point := track.point_at(track.cumulative[sample], side * 180.0)
				var x := clampi(int(point.x / track.world_size * field.get_width()), 0, field.get_width() - 1)
				var y := clampi(int(point.y / track.world_size * field.get_height()), 0, field.get_height() - 1)
				outside_count += int(field.get_pixel(x, y).r > 0.60)
		check("%s road field covers the whole map and distinguishes both shoulders" % track.id,
			field_ok and outside_count >= 54)
		for step in range(15000):
			apply_pilot(6, solo, solo.karts[0])
			pc._physics_process(STEP)
			if solo.winner_slot >= 0:
				break
		axis(6, 0.0)
		axis(6, 0.0, JOY_AXIS_TRIGGER_RIGHT)
		button(6, JOY_BUTTON_B, false)
		var finished := solo.winner_slot == 0 and pc._screen == PC.Screen.RESULT
		if not finished:
			print("REEF_KART_PC|DIAG|", track.id, "|attempt=", solo.attempt, "|state=", solo.state,
				"|time=", solo.race_time, "|P1=", _summary(solo.karts[0]), "|Imp=", _summary(solo.karts[1]))
		check("%s finishes two laps in solo" % track.id, finished and solo.karts[1]["id"] == "imp")
		pc._show_mode()
		pc._show_garage(2, 6)
		tap(11, JOY_BUTTON_A)
		tap(6, JOY_BUTTON_A)
		tap(11, JOY_BUTTON_A)
		tap(6, JOY_BUTTON_A)
		check("%s binds the same course and art to both players" % track.id,
			pc._race.track.id == track.id and is_same(pc._race.track, pc._second_view.track)
			and is_same(pc._race._room_art, pc._second_view._room_art))
		await process_frame
	pc._show_garage(1, 6)
	tap(6, JOY_BUTTON_A)
	pc._choose_course(0)
	tap(6, JOY_BUTTON_A)
	var idle_race: ReefKartRace = pc._race
	for step in range(4200):
		pc._physics_process(STEP)
		if idle_race.imp_wins > 0:
			break
	check("the Imp can win against an idle driver without moving their kart",
		idle_race.imp_wins == 1 and is_zero_approx(float(idle_race.karts[0]["speed"])))
	pc._show_mode()
	await create_timer(0.3).timeout
	pc.queue_free()
	await process_frame
	# Allow the audio server to retire stopped Ogg playback after scene teardown.
	await create_timer(0.1).timeout
	print("REEF_KART_PC|DONE|failures=", failures)
	quit(0 if failures == 0 else 1)


func _summary(kart: Dictionary) -> Array:
	return [kart["race_s"], kart["lat"], kart["speed"], kart["heading"], kart["wrong_way"], kart["spin_t"]]
