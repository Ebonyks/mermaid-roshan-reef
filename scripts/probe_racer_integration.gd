extends SceneTree
## Focused probe for the Reef Grand Prix engine (scripts/racer/) and the owner's
## touch layout: green stick left, red brake and item bubble right. The trusted
## roster keeps the career-level Racer legs in probe_opera_2d.gd; this probe
## measures the engine itself. Every number printed is a measurement.

var failures := 0
const STEP := 1.0 / 60.0
var events: Array[String] = []


func _initialize() -> void:
	call_deferred("_run")


func check(label: String, condition: bool) -> void:
	print("RACER_INTEGRATION|", "PASS" if condition else "FAIL", "|", label)
	if not condition:
		failures += 1


func surface() -> OperaRacerSurface:
	var result := OperaRacerSurface.new()
	root.add_child(result)
	result.size = Vector2(1280, 720)
	result.configure("kart_race", Color.WHITE)
	result.set_process(false)
	events.clear()
	result.race_event.connect(func(kind: String, _value: float) -> void: events.append(kind))
	return result


func touch(s: OperaRacerSurface, index: int, down: bool, at: Vector2, canceled := false) -> void:
	var event := InputEventScreenTouch.new()
	event.index = index
	event.pressed = down
	event.position = at
	event.canceled = canceled
	s._gui_input(event)


func drag(s: OperaRacerSurface, index: int, at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = index
	event.position = at
	s._gui_input(event)


func run_frames(s: OperaRacerSurface, count: int) -> void:
	for _frame in range(count):
		s._process(STEP)


## Hold the stick and slide it so the wanted lane approaches `lane`.
func drive_lane(s: OperaRacerSurface, lane: float, until_s: float, maximum := 2400) -> bool:
	var origin := OperaRacerSurface.STEERING_RECT.get_center()
	touch(s, 71, true, origin)
	var pl: Dictionary = s._engine._pl
	for _frame in range(maximum):
		var stick := clampf((lane - float(pl["lat_goal"])) / 30.0, -1.0, 1.0)
		drag(s, 71, origin + Vector2(stick * OperaRacerSurface.STEERING_RANGE, 0.0))
		s._process(STEP)
		if float(pl["race_s"]) >= until_s:
			return true
	return false


func _run() -> void:
	_check_track()
	_check_structure_and_idle()
	_check_fingers_and_brake()
	_check_pearls()
	_check_items()
	_check_wrong_way()
	_check_imp_contest()
	_check_tie()
	_check_full_race()
	await _check_teardown()
	print("RACER_INTEGRATION|DONE|failures=", failures)
	quit(1 if failures else 0)


func _check_track() -> void:
	var track := ReefKartTrack.new()
	var spacing := track.length / float(ReefKartTrack.SAMPLES)
	var closing := track.center[0].distance_to(track.center[ReefKartTrack.SAMPLES - 1])
	var max_curve := 0.0
	for value: float in track.curvatures:
		max_curve = maxf(max_curve, absf(value))
	var tightest := 1.0 / maxf(0.00001, max_curve)
	var closest := INF
	for i in range(0, ReefKartTrack.SAMPLES, 4):
		for j in range(i + 4, ReefKartTrack.SAMPLES, 4):
			var along := absf(track.cumulative[j] - track.cumulative[i])
			along = minf(along, track.length - along)
			if along > 700.0:
				closest = minf(closest, track.center[i].distance_to(track.center[j]))
	var worst_s := 0.0
	var worst_lat := 0.0
	for i in range(0, ReefKartTrack.SAMPLES, 10):
		var s := track.cumulative[i]
		var edge := ReefKartTrack.RAIL - ReefKartRace.KART_RADIUS
		for lat: float in [-edge, -60.0, 0.0, 60.0, edge]:
			var back := track.project(track.point_at(s, lat), s)
			worst_s = maxf(worst_s, absf(wrapf(back.x - s, -track.length * 0.5, track.length * 0.5)))
			worst_lat = maxf(worst_lat, absf(back.y - lat))
	var inside := 1.0e9
	for p: Vector2 in track.center:
		inside = minf(inside, minf(minf(p.x, p.y), minf(ReefKartTrack.WORLD_SIZE - p.x, ReefKartTrack.WORLD_SIZE - p.y)))
	print("RACER_INTEGRATION|MEASURE|track|length=", snappedf(track.length, 0.1),
		"|tightest_radius=", snappedf(tightest, 0.1), "|closest_far_corridor=", snappedf(closest, 0.1),
		"|projection_err_s=", snappedf(worst_s, 0.01), "|projection_err_lat=", snappedf(worst_lat, 0.01),
		"|world_margin=", snappedf(inside, 0.1))
	check("course is one closed loop of evenly spaced samples", closing <= spacing * 1.5)
	check("tightest bend is drivable at speed (radius >= 120)", tightest >= 120.0)
	check("distant parts of the course never share a corridor",
		closest >= ReefKartTrack.RAIL * 2.0 + 24.0)
	check("projection round-trips every reachable position to within 3 units",
		worst_s < 3.0 and worst_lat < 2.0)
	check("course and its rails stay inside the painted world square",
		inside >= ReefKartTrack.RAIL + 40.0)
	var on_road := true
	for source: Array in [track.pearls, track.bubbles, track.buoys]:
		for item: Dictionary in source:
			on_road = on_road and absf(float(item["lat"])) <= ReefKartTrack.ROAD_HALF - 10.0
	check("every pearl, item bubble and gem buoy sits on the water lane", on_road
		and track.buoys.size() == 3 and track.bubbles.size() == 6)
	var lane_free := true
	for pearl: Dictionary in track.pearls:
		lane_free = lane_free and absf(float(pearl["lat"]) - (-36.0)) >= 55.0
	check("every pearl row is at least 55 units from Roshan's starting lane", lane_free)
	var landmarks_clear := true
	var spans := 0
	for landmark: Dictionary in track.landmarks:
		if bool(landmark.get("spans", false)):
			# Arches span the lane; the kart drives through their openings.
			spans += 1
			landmarks_clear = landmarks_clear and float(landmark["w"]) * 0.5 >= ReefKartTrack.RAIL
			continue
		var at: Vector2 = landmark["pos"]
		for p: Vector2 in track.center:
			landmarks_clear = landmarks_clear and at.distance_to(p) >= ReefKartTrack.RAIL + 30.0
	check("standing landmarks stay off the lane and the four arches span it",
		landmarks_clear and spans == 4)
	ReefKartTrack._field_cache = null
	var started := Time.get_ticks_usec()
	var field := track.floor_field()
	var field_ms := float(Time.get_ticks_usec() - started) / 1000.0
	print("RACER_INTEGRATION|MEASURE|floor_field_ms=", snappedf(field_ms, 0.1),
		"|size=", field.get_width(), "x", field.get_height())
	check("interim floor field is a single 128 px channel built once",
		field.get_width() == ReefKartTrack.FIELD_SIZE and track.floor_field() == field)


func _check_structure_and_idle() -> void:
	var s := surface()
	var engine := s._engine
	var canvas_only := true
	for child: Node in engine.get_children():
		canvas_only = canvas_only and child is CanvasItem
	check("engine is one owned Canvas node with five fixed drawn layers",
		engine.get_parent() == s and engine.get_child_count() == 5 and canvas_only)
	check("only the owning surface clocks the simulation", not engine.is_processing())
	check("two racers: Roshan and the imp", engine.karts.size() == 2
		and bool(engine.karts[0]["player"]) and String(engine.imp()["id"]) == "imp")
	run_frames(s, 3600)
	check("sixty seconds unattended earns no distance, pearl or finish",
		is_zero_approx(float(s.kart["s"])) and s.race_pearls == 0 and not s.race_finished
		and engine.state == "grid" and s.demo_active)
	check("the guide hand shows on the stick while she has not started",
		bool(engine.controls.get("guide", false)))
	s.free()


func _check_fingers_and_brake() -> void:
	var s := surface()
	var engine := s._engine
	var origin := OperaRacerSurface.STEERING_RECT.get_center()
	touch(s, 71, true, origin)
	check("first stick touch starts the countdown, not the race",
		engine.state == "countdown" and s.race_started and not s.demo_active)
	drag(s, 71, origin + Vector2(48.0, 0.0))
	var owned := s.race_steer
	drag(s, 99, Vector2(100, 600))
	check("a foreign finger cannot steer", is_equal_approx(owned, s.race_steer)
		and s.race_touch_owner == 71 and is_equal_approx(owned, 0.5))
	touch(s, 72, true, OperaRacerSurface.TURBO_CENTER)
	touch(s, 73, true, OperaRacerSurface.BRAKE_CENTER)
	check("stick, bubble and brake each keep their own finger",
		s.race_touch_owner == 71 and s.race_turbo_owner == 72 and s.race_brake_owner == 73
		and s.held and s.race_turbo_held and s.race_brake_held)
	touch(s, 73, false, OperaRacerSurface.BRAKE_CENTER)
	run_frames(s, 90 + 120)
	check("the bubble pressed during the countdown fires the start zoom",
		s.race_turbo_fires == 1 and "turbo" in events)
	var cruising := float(engine._pl["speed"])
	touch(s, 74, true, OperaRacerSurface.BRAKE_CENTER)
	run_frames(s, 60)
	var braked := float(engine._pl["speed"])
	print("RACER_INTEGRATION|MEASURE|brake|before=", snappedf(cruising, 0.1), "|after_1s=", snappedf(braked, 0.1))
	check("holding the red brake stops the kart and keeps the race live",
		cruising > 150.0 and braked < 5.0 and s.race_input_t > 0.0)
	touch(s, 74, false, OperaRacerSurface.BRAKE_CENTER)
	touch(s, 72, false, OperaRacerSurface.TURBO_CENTER)
	s.cancel_race_touch()
	var stopped := float(s.kart["s"])
	var stopped_imp := float(engine.imp()["race_s"])
	run_frames(s, 120)
	check("cancel freezes Roshan and the imp together",
		is_equal_approx(stopped, float(s.kart["s"]))
		and is_equal_approx(stopped_imp, float(engine.imp()["race_s"]))
		and s.race_touch_owner == -1 and s.race_turbo_owner == -1 and s.race_brake_owner == -1)
	touch(s, 75, true, Vector2(1240, 300))
	check("a touch away from every control claims nothing",
		s.race_touch_owner == -1 and s.race_turbo_owner == -1 and s.race_brake_owner == -1)
	s.free()


func _check_pearls() -> void:
	var track := ReefKartTrack.new()
	var count := int(ReefKartTrack.PEARL_ROWS[0]["count"])
	var row: Array[float] = []
	for index in range(count):
		row.append(float(track.pearls[index]["s"]))
	var lane := float(track.pearls[0]["lat"])
	var results: Array[int] = []
	for target: float in [lane, -36.0]:
		var s := surface()
		var arrived := drive_lane(s, target, row[-1] + 24.0)
		var claims := 0
		for index in range(count):
			if float(s._engine.track.pearls[index]["respawn_t"]) > 0.0:
				claims += 1
		results.append(claims if arrived else -1)
		s.cancel_race_touch()
		var saved := s.race_pearls
		run_frames(s, 60)
		check("collected pearls survive cancellation", saved == s.race_pearls)
		s.free()
	print("RACER_INTEGRATION|MEASURE|pearl_row|lane_hit=", results[0], "|lane_miss=", results[1])
	check("steering into the pearl row collects it; the starting lane misses it",
		results[0] >= 3 and results[1] == 0)


func _check_items() -> void:
	var s := surface()
	var engine := s._engine
	var imp_only := true
	for _roll in range(200):
		imp_only = imp_only and engine._pick_item(engine.imp()) in ["zoom", "kelp"]
	check("the imp is only ever dealt zoom or kelp, never anything aimed at Roshan", imp_only)
	var origin := OperaRacerSurface.STEERING_RECT.get_center()
	touch(s, 71, true, origin)
	touch(s, 73, true, OperaRacerSurface.BRAKE_CENTER)
	run_frames(s, 90 + 90)
	touch(s, 73, false, OperaRacerSurface.BRAKE_CENTER)
	var pl: Dictionary = engine._pl
	pl["roulette_t"] = 0.0
	pl["pending"] = ""
	pl["item"] = "sparkle"
	touch(s, 72, true, OperaRacerSurface.TURBO_CENTER)
	run_frames(s, 1)
	touch(s, 72, false, OperaRacerSurface.TURBO_CENTER)
	var spun := false
	for _frame in range(180):
		s._process(STEP)
		spun = spun or float(engine.imp()["spin_t"]) > 0.0
	check("a sparkle bubble homes in on the imp ahead and spins him", spun and "bonk" in events)
	var pearls_before := int(pl["pearls"])
	pl["roulette_t"] = 0.0
	pl["pending"] = ""
	pl["item"] = "pearls"
	touch(s, 72, true, OperaRacerSurface.TURBO_CENTER)
	run_frames(s, 1)
	touch(s, 72, false, OperaRacerSurface.TURBO_CENTER)
	check("a pearl bundle adds three pearls", int(pl["pearls"]) == mini(10, pearls_before + 3))
	pl["roulette_t"] = 0.0
	pl["pending"] = ""
	pl["item"] = "kelp"
	touch(s, 72, true, OperaRacerSurface.TURBO_CENTER)
	run_frames(s, 1)
	touch(s, 72, false, OperaRacerSurface.TURBO_CENTER)
	var hers: Array[Dictionary] = []
	for trap: Dictionary in engine.traps:
		if is_same(trap["owner"], pl):
			hers.append(trap)
	check("kelp drops behind the kart and is harmless to her while it settles",
		hers.size() == 1 and float(hers[0]["armed_t"]) > 0.0
		and float(pl["slow_t"]) <= 0.0)
	var held_item := String(pl["item"])
	touch(s, 72, true, OperaRacerSurface.TURBO_CENTER)
	run_frames(s, 1)
	check("an empty bubble press does nothing", held_item == "" and String(pl["item"]) == "")
	touch(s, 72, false, OperaRacerSurface.TURBO_CENTER)
	s.free()
	s = surface()
	engine = s._engine
	var item_s := float(engine.track.bubbles[1]["s"])
	touch(s, 72, true, OperaRacerSurface.TURBO_CENTER)
	touch(s, 72, false, OperaRacerSurface.TURBO_CENTER)
	var arrived := drive_lane(s, 0.0, item_s + 20.0)
	var rolled := "item_roll" in events
	run_frames(s, 70)
	check("driving through an item bubble under a pearl arch rolls and deals an item",
		arrived and rolled and "item_ready" in events
		and String(engine._pl["item"]) in ReefKartRace.ITEM_KINDS)
	s.free()
	s = surface()
	engine = s._engine
	var buoy_s := float(engine.track.buoys[0]["s"])
	touch(s, 72, true, OperaRacerSurface.TURBO_CENTER)
	touch(s, 72, false, OperaRacerSurface.TURBO_CENTER)
	var reached := drive_lane(s, ReefKartTrack.BUOY_LAT, buoy_s + 20.0)
	check("steering into a gem buoy pops its orb and deals an item",
		reached and "item_roll" in events
		and float(engine.track.buoys[0]["respawn_t"]) > 0.0)
	s.free()


func _check_wrong_way() -> void:
	var s := surface()
	var engine := s._engine
	var origin := OperaRacerSurface.STEERING_RECT.get_center()
	touch(s, 71, true, origin)
	run_frames(s, 90 + 60)
	var pl: Dictionary = engine._pl
	pl["heading"] = wrapf(engine.track.heading_at(float(pl["track_s"])) + PI, -PI, PI)
	run_frames(s, 2)
	var flagged := bool(pl["wrong_way"]) and "wrong_way" in events
	run_frames(s, 150)
	var error := absf(wrapf(engine.track.heading_at(float(pl["track_s"])) - float(pl["heading"]), -PI, PI))
	print("RACER_INTEGRATION|MEASURE|wrong_way|heading_error_after_2.5s=", snappedf(error, 0.01))
	check("facing backwards shows the arrow and turns her back toward the course",
		flagged and not bool(pl["wrong_way"]) and error < ReefKartRace.WRONG_WAY)
	s.free()


func _check_imp_contest() -> void:
	var s := surface()
	var engine := s._engine
	var origin := OperaRacerSurface.STEERING_RECT.get_center()
	touch(s, 71, true, origin)
	touch(s, 73, true, OperaRacerSurface.BRAKE_CENTER)
	engine._pl["pearls"] = 4
	var beat_frames: Array[int] = []
	var restart_paces: Array[float] = []
	var beat_start := -1
	var frame := 0
	while frame < 7200 and restart_paces.size() < 2:
		var wins_before := engine.imp_wins
		var attempt_before := engine.attempt
		s._process(STEP)
		frame += 1
		if engine.imp_wins > wins_before:
			beat_start = frame
		if engine.attempt > attempt_before:
			beat_frames.append(frame - beat_start)
			restart_paces.append(float(engine.imp()["skill"]) / float(engine.imp()["base_skill"]))
	print("RACER_INTEGRATION|MEASURE|imp_contest|beats_frames=", beat_frames, "|paces=", restart_paces,
		"|frames=", frame)
	check("when the imp wins only the race restarts, after a beat of at most two seconds",
		beat_frames.size() == 2 and beat_frames.max() <= 120 and engine.state == "countdown"
		and float(engine._pl["race_s"]) < 0.0 and is_zero_approx(float(s.kart["s"])))
	check("earned pearls are kept across imp restarts", int(engine._pl["pearls"]) == 4)
	check("the imp slows after one win and drives at half pace after two",
		restart_paces.size() == 2 and is_equal_approx(restart_paces[0], ReefKartRace.RETRY_PACE)
		and is_equal_approx(restart_paces[1], ReefKartRace.MERCY_PACE))
	touch(s, 73, false, OperaRacerSurface.BRAKE_CENTER)
	var finished := false
	for _frame in range(4200):
		s._process(STEP)
		if s.race_finished:
			finished = true
			break
	check("after mercy a held stick wins the third attempt", finished and engine.attempt == 3
		and is_equal_approx(float(s.kart["s"]), OperaRacerSurface.LAP_DISTANCE * 2.0))
	s.free()


func _check_tie() -> void:
	var s := surface()
	var engine := s._engine
	var origin := OperaRacerSurface.STEERING_RECT.get_center()
	touch(s, 71, true, origin)
	run_frames(s, 90 + 60)
	var goal := engine.track.length * float(ReefKartRace.LAPS)
	var imp_kart := engine.imp()
	engine._pl["race_s"] = goal - 0.5
	imp_kart["race_s"] = goal - 0.5
	imp_kart["speed"] = engine._pl["speed"]
	run_frames(s, 1)
	check("a dead heat goes to Roshan", engine.state == "finished" and bool(engine._pl["finished"])
		and not bool(imp_kart["finished"]) and engine.imp_wins == 0)
	s.free()


func _check_full_race() -> void:
	var s := surface()
	var engine := s._engine
	var origin := OperaRacerSurface.STEERING_RECT.get_center()
	touch(s, 71, true, origin)
	var frames := 0
	var nodes := _count(engine)
	var bounded := true
	var step_usec := 0
	for frame in range(4200):
		var started := Time.get_ticks_usec()
		s._process(STEP)
		step_usec += Time.get_ticks_usec() - started
		bounded = bounded and _count(engine) == nodes
		frames = frame + 1
		if s.race_finished:
			break
	var seconds := float(frames) * STEP
	print("RACER_INTEGRATION|MEASURE|held_stick_race|seconds=", snappedf(seconds, 0.01),
		"|attempts=", engine.attempt, "|pearls=", s.race_pearls, "|bumps=", s.race_wall_bumps,
		"|avg_step_usec=", step_usec / maxi(1, frames))
	check("a held stick finishes two laps ahead of the imp within seventy seconds",
		s.race_finished and seconds <= 70.0 and engine.attempt == 1
		and is_equal_approx(float(s.kart["s"]), OperaRacerSurface.LAP_DISTANCE * 2.0))
	check("the race never adds or removes nodes", bounded)
	var earned := float(s.kart["s"])
	s._process(STEP * 65.0)
	run_frames(s, 65)
	check("coasting after the line manufactures no distance", is_equal_approx(float(s.kart["s"]), earned))
	s.free()


func _check_teardown() -> void:
	var s := surface()
	var old: WeakRef = weakref(s._engine)
	s.configure("circle", Color.WHITE)
	await process_frame
	await process_frame
	check("leaving the race frees the old engine", old.get_ref() == null and s._rival_art == null
		and s._engine == null)
	s.configure("kart_race", Color.WHITE)
	var fresh: WeakRef = weakref(s._engine)
	s.queue_free()
	await process_frame
	await process_frame
	check("teardown frees the fresh engine", fresh.get_ref() == null)


func _count(node: Node) -> int:
	var total := 1
	for child: Node in node.get_children():
		total += _count(child)
	return total
