extends SceneTree

var failures := 0
const STEP := 1.0 / 60.0

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

func drive_to(s: OperaRacerSurface, lateral: float, distance: float, maximum := 1200) -> bool:
	var origin := OperaRacerSurface.STEERING_RECT.get_center()
	touch(s, 71, true, origin)
	for frame in range(maximum):
		var steer: float = clampf((lateral - float(s.kart["lat"])) * 0.28 - float(s.kart.get("latv", 0.0)) * 0.08, -0.55, 0.55)
		drag(s, 71, origin + Vector2(steer * OperaRacerSurface.STEERING_RANGE, 0))
		s._process(STEP)
		if float(s._engine._pl["s"]) > distance:
			return true
	return false

func _run() -> void:
	var s := surface()
	var engine := s._engine
	check("full engine has eight racers and one owned presenter", engine._karts.size() == 8 and engine._canvas.get_parent() == engine and engine.get_parent() == s)
	check("only the owning surface clocks the simulation", not engine.is_processing())
	for frame in range(3600):
		s._process(STEP)
	check("sixty seconds unattended earns no distance, pearl or finish", is_zero_approx(float(s.kart["s"])) and s.race_pearls == 0 and not s.race_finished)
	touch(s, 71, true, OperaRacerSurface.STEERING_RECT.get_center())
	for frame in range(180):
		s._process(STEP)
	var previous_steer: float = s.race_steer
	drag(s, 99, Vector2(200, 600))
	check("foreign finger cannot steer", is_equal_approx(previous_steer, s.race_steer) and s.race_touch_owner == 71)
	touch(s, 72, true, OperaRacerSurface.TURBO_CENTER)
	check("optional turbo finger preserves steering owner", s.race_touch_owner == 71 and s.race_turbo_owner == 72)
	for frame in range(60):
		s._process(STEP)
	check("turbo is live during actual driving", s.race_turbo_fires >= 1)
	s.cancel_race_touch()
	var stopped: float = float(s.kart["s"])
	var pearls: int = s.race_pearls
	for frame in range(120):
		s._process(STEP)
	check("cancel immediately freezes earned distance and pearls", is_equal_approx(stopped, float(s.kart["s"])) and pearls == s.race_pearls)
	s.free()

	var contacts: Array[Dictionary] = []
	for target in [3.0, -8.4]:
		s = surface()
		engine = s._engine
		var row: Array = engine._pearls_live.slice(0, 4)
		var last: Node2D = row[-1]["node"]
		var arrived: bool = drive_to(s, target, float(last.get_meta("course_s")) + 12.0)
		var claims: int = 0
		for pearl: Dictionary in row:
			if bool(pearl["got"]):
				claims += 1
		contacts.append({"arrived": arrived, "claims": claims})
		s.cancel_race_touch()
		var saved: int = s.race_pearls
		for frame in range(60):
			s._process(STEP)
		check("collected pearls survive cancellation", saved == s.race_pearls)
		s.free()
	print("RACER_INTEGRATION|MEASURE|pearl_rows|", contacts)
	check("genuine steering hits versus misses actual pearl footprints", contacts[0]["arrived"] and contacts[1]["arrived"] and contacts[0]["claims"] > 0 and contacts[1]["claims"] == 0)

	var furniture_results: Array[bool] = []
	for target in [-5.0, 5.0]:
		s = surface()
		engine = s._engine
		var furniture: Dictionary = engine._furniture_live[0]
		var arrived: bool = drive_to(s, target, float(furniture["s"]) + 12.0)
		furniture_results.append(arrived and int(furniture["last_lap"]) >= 0)
		check("furniture contact keeps positive progress and no economy payout", arrived and float(s.kart["s"]) > 0 and engine._payout_banked == 0)
		s.free()
	check("whole couch is a real avoidable road obstacle", furniture_results[0] and not furniture_results[1])

	s = surface()
	engine = s._engine
	var seen: Dictionary = {}
	var origin := OperaRacerSurface.STEERING_RECT.get_center()
	touch(s, 71, true, origin)
	var frames := 0
	for frame in range(4200):
		var curvature: float = s.road_curvature(float(s.kart["s"]) + 10.0)
		var target: float = -signf(curvature) * 4.0 if absf(curvature) > 0.003 else 0.0
		var steer: float = clampf((target - float(s.kart["lat"])) * 0.28 - float(s.kart.get("latv", 0.0)) * 0.08, -0.55, 0.55)
		drag(s, 71, origin + Vector2(steer * OperaRacerSurface.STEERING_RANGE, 0))
		s._process(STEP)
		seen[engine._canvas.current_sector] = true
		frames = frame + 1
		if s.race_finished:
			break
	print("RACER_INTEGRATION|MEASURE|lap_seconds|", frames * STEP, "|pearls|", s.race_pearls)
	check("genuine input completes two laps within seventy seconds", s.race_finished and frames * STEP <= 70.0 and is_equal_approx(float(s.kart["s"]), 1600.0))
	check("natural complete laps traverse all five castle visits", seen.size() == 5)
	check("career engine cannot issue its own reward or completion", engine._payout_banked == 0 and not engine._completion_committed and engine._state == "external_finish")
	var earned: float = float(s.kart["s"])
	for frame in range(65):
		s._process(STEP)
	check("seated stop settles without manufactured earned distance", is_equal_approx(float(s.kart["s"]), earned) and is_zero_approx(float(engine._pl["speed"])))
	var old: WeakRef = weakref(engine)
	s.configure("circle", Color.WHITE)
	await process_frame
	await process_frame
	check("leaving race actually frees the old engine", old.get_ref() == null and s._rival_art == null)
	s.configure("kart_race", Color.WHITE)
	var fresh: WeakRef = weakref(s._engine)
	var presenter: WeakRef = weakref(s._engine._canvas)
	s.queue_free()
	await process_frame
	await process_frame
	check("teardown actually frees fresh engine and presenter", fresh.get_ref() == null and presenter.get_ref() == null)
	print("RACER_INTEGRATION|DONE|failures=", failures)
	quit(1 if failures else 0)
