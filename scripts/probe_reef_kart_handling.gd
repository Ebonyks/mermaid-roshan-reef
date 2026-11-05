extends SceneTree
## Ten sequential tuning runs against the published PC handling path.
## Usage: --headless -s scripts/probe_reef_kart_handling.gd -- [first] [last]
const Race := preload("res://scripts/racer/reef_kart_race.gd")
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Drive := preload("res://scripts/racer/reef_kart_drive.gd")
const Courses := preload("res://scripts/racer/reef_kart_courses.gd")
const STEP := 1.0 / 60.0
const PROFILES := [
	["Published assist", {}],
	["Manual chassis", {"steer_rate": 12.0, "turn": 2.65, "grip": 14.0, "crawl_grip": 0.0,
		"drift_grip": 8.0, "coast": 145.0, "rail_rebound": 0.02, "camera": 7.5, "deadzone": 0.22, "charge": 0.80}],
	["Smaller stick deadzone", {"deadzone": 0.10}],
	["Faster steering rack", {"steer_rate": 22.0}],
	["Stronger yaw", {"turn": 3.0}],
	["More normal tire grip", {"grip": 18.0}],
	["Looser drift grip", {"drift_grip": 5.5}],
	["Longer coast", {"coast": 112.0}],
	["Softer rail rebound", {"rail_rebound": 0.12}],
	["Faster chase camera", {"camera": 18.0}],
	["Crawl steering and earlier drift reward", {"crawl_grip": 0.24, "charge": 0.68}],
]


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	var args := OS.get_cmdline_user_args()
	var first := int(args[0]) if args.size() > 0 else 0
	var last := int(args[1]) if args.size() > 1 else 10
	var tune: Dictionary = {}
	var failures := 0
	for index in range(PROFILES.size()):
		tune.merge(PROFILES[index][1], true)
		if index < first or index > last:
			continue
		var sample := _new_race(0, index != 0, tune)
		var signals := _measure(sample, float(tune.get("deadzone", 0.22)))
		sample.queue_free()
		var laps: Array[Dictionary] = []
		for course in range(Courses.COURSES.size()):
			var race := _new_race(course, index != 0, tune)
			laps.append(_lap_test(race))
			race.queue_free()
			await process_frame
		var result := {"id": index, "variant": PROFILES[index][0], "tune": tune, "measures": signals, "courses": laps}
		print("HANDLING|", JSON.stringify(result))
		if index == 10 and (not laps.all(func(lap: Dictionary) -> bool: return bool(lap["finished"]))
				or float(signals["idle_distance"]) > 0.01 or float(signals["rail_yaw_deg"]) > 0.01
				or not bool(signals["drift_boost"]) or bool(signals["short_drift_boost"])
				or bool(signals["cancelled_drift_boost"]) or float(signals["reverse_speed"]) < 30.0):
			failures += 1
	if last >= 10:
		for course in range(Courses.COURSES.size()):
			var stress := _new_race(course, true, {})
			var outcome := _stress_test(stress, course)
			print("HANDLING_STRESS|", JSON.stringify(outcome))
			if not bool(outcome["bounded"]):
				failures += 1
			stress.queue_free()
			await process_frame
	print("HANDLING|DONE|failures=", failures)
	quit(0 if failures == 0 else 1)


func _new_race(course: int, manual: bool, tune: Dictionary) -> ReefKartRace:
	var race := Race.new()
	race.setup({"course": Courses.COURSES[course], "pc_handling": manual, "pc_tune": tune, "duel": true,
		"racers": [{"id": "test_driver", "player": true}, {"id": "parked_rival", "player": true}]})
	root.add_child(race)
	return race


func _fixture(race: ReefKartRace, speed: float = 0.0, along: float = 70.0,
		lat: float = 0.0, turn: float = 0.0) -> Dictionary:
	race._place_grid()
	race.state = "race"
	race.winner_slot = -1
	race.race_time = 0.0
	var kart: Dictionary = race.karts[0]
	kart["track_s"] = along
	kart["race_s"] = along
	kart["lat"] = lat
	kart["lat_goal"] = lat
	kart["pos"] = race.track.point_at(along, lat)
	kart["heading"] = race.track.heading_at(along) + turn
	kart["speed"] = speed
	if race.pc_handling:
		kart["velocity"] = Drive.forward(float(kart["heading"])) * speed
	race._update_camera(1.0, true)
	return kart


func _advance(race: ReefKartRace, frames: int, command: Dictionary) -> void:
	for i in range(frames):
		race.step_race(STEP, command)


func _measure(race: ReefKartRace, deadzone: float) -> Dictionary:
	var k := _fixture(race)
	var start: Vector2 = k["pos"]
	_advance(race, 120, {})
	var idle := start.distance_to(k["pos"])
	k = _fixture(race, 220.0)
	start = k["pos"]
	_advance(race, 45, {})
	var coast := start.distance_to(k["pos"])
	var coast_speed := float(k["speed"])
	k = _fixture(race, 210.0)
	var heading := float(k["heading"])
	var small_frames := -1
	var stick := PC.steer_from_axis(0.18, deadzone)
	for i in range(18):
		_advance(race, 1, {"steer": stick, "throttle": 1.0})
		if absf(angle_difference(heading, float(k["heading"]))) >= deg_to_rad(0.6) and small_frames < 0:
			small_frames = i + 1
	k = _fixture(race, 210.0)
	heading = float(k["heading"])
	_advance(race, 10, {"steer": 0.72, "throttle": 1.0})
	var turn_10 := absf(rad_to_deg(angle_difference(heading, float(k["heading"]))))
	var turn_slip := 0.0
	if race.pc_handling:
		turn_slip = absf(rad_to_deg(Drive.forward(float(k["heading"])).angle_to(k["velocity"])))
	var reversal := -1
	for i in range(18):
		heading = float(k["heading"])
		_advance(race, 1, {"steer": -0.72, "throttle": 1.0})
		if angle_difference(heading, float(k["heading"])) < -0.0005 and reversal < 0:
			reversal = i + 1
	k = _fixture(race)
	k["heading"] = float(k["heading"]) + 0.5
	var cam_start := race.cam_heading
	var camera_frames := 0
	while camera_frames < 30 and absf(angle_difference(cam_start, race.cam_heading)) < 0.25:
		race._update_camera(STEP, false)
		camera_frames += 1
	k = _fixture(race, 220.0, 90.0, 122.0, 0.78)
	heading = float(k["heading"])
	var rail_start := float(k["race_s"])
	_advance(race, 1, {"throttle": 1.0})
	var rail_yaw := absf(rad_to_deg(angle_difference(heading, float(k["heading"]))))
	var rail_speed := float(k["speed"])
	var rail_outward := 0.0
	if race.pc_handling:
		var tangent := race.track.tangent_at(float(k["track_s"]))
		rail_outward = (k["velocity"] as Vector2).dot(Vector2(-tangent.y, tangent.x))
	var rail_distance := absf(float(k["race_s"]) - rail_start)
	k = _fixture(race, 160.0, 90.0, 121.0, PI * 0.5)
	_advance(race, 15, {"throttle": 1.0})
	var recovery := -1
	for i in range(180):
		_advance(race, 1, {"throttle": 1.0, "steer": -1.0})
		if absf(float(k["lat"])) < 103.0 and recovery < 0:
			recovery = i + 1
	k = _fixture(race)
	_advance(race, 30, {"brake": true})
	var reverse := float(k["speed"]) if float(k["race_s"]) < 70.0 else 0.0
	var short_drift := _drift_release(race, 12, false)
	var medium := _drift_release(race, 50, false)
	var charged := _drift_release(race, 62, false)
	var cancelled := _drift_release(race, 62, true)
	return {"idle_distance": snappedf(idle, 0.01), "coast_distance": snappedf(coast, 0.01),
		"coast_speed": snappedf(coast_speed, 0.01), "small_stick_ms": -1 if small_frames < 0 else roundi(small_frames * STEP * 1000),
		"turn_10_deg": snappedf(turn_10, 0.01), "normal_slip_deg": snappedf(turn_slip, 0.01), "reverse_steer_ms": -1 if reversal < 0 else roundi(reversal * STEP * 1000),
		"camera_half_ms": roundi(camera_frames * STEP * 1000), "rail_yaw_deg": snappedf(rail_yaw, 0.01),
		"rail_speed": snappedf(rail_speed, 0.01), "rail_progress": snappedf(rail_distance, 0.01),
		"rail_outward_speed": snappedf(rail_outward, 0.01), "wall_escape_ms": -1 if recovery < 0 else roundi(recovery * STEP * 1000),
		"medium_drift_boost": medium["boost"],
		"reverse_speed": snappedf(reverse, 0.01), "drift_slip_deg": charged["slip"], "drift_boost": charged["boost"],
		"short_drift_boost": short_drift["boost"], "cancelled_drift_boost": cancelled["boost"]}


func _drift_release(race: ReefKartRace, frames: int, cancel: bool) -> Dictionary:
	if not race.pc_handling:
		return {"slip": 0.0, "boost": false}
	var along := race.track.s_of(3, -22.0)
	var k := _fixture(race, 234.0, along)
	_advance(race, 3, {"throttle": 0.70, "steer": -0.29, "drift": true})
	var peak := 0.0
	for i in range(frames):
		_advance(race, 1, {"throttle": 0.70, "steer": 0.53, "drift": true})
		var velocity: Vector2 = k["velocity"]
		peak = maxf(peak, absf(rad_to_deg(Drive.forward(float(k["heading"])).angle_to(velocity))))
	if cancel:
		race.cancel_pc_input()
	_advance(race, 1, {"throttle": 0.70})
	return {"slip": snappedf(peak, 0.01), "boost": float(k["boost_t"]) > 0.0}


## A deterministic test driver presses the same inputs available to the user.
## Full race legs enter through begin() and never write driving state.
static func pilot(race: ReefKartRace, k: Dictionary) -> Dictionary:
	var s := float(k["track_s"])
	var speed := float(k["speed"])
	var pos: Vector2 = k["pos"]
	var look := clampf(speed * 0.25, 40.0, 76.0)
	var direction := (race.track.point_at(s + look) - pos).normalized()
	var target := atan2(direction.x, -direction.y)
	var error := angle_difference(float(k["heading"]), target)
	var turn := clampf(error * 3.2, -1.0, 1.0)
	var curvature := 0.0
	for ahead: float in [25.0, 54.0, 88.0]:
		curvature = maxf(curvature, absf(race.track.curvature_at(s + ahead)))
	var pace := clampf(sqrt(380.0 / maxf(curvature, 0.0001)), 116.0, 302.0)
	var brake := speed > pace + 20.0
	return {"steer": turn, "throttle": 1.0 if speed < pace else 0.0, "brake": brake}


func _lap_test(race: ReefKartRace) -> Dictionary:
	race.begin()
	var k: Dictionary = race.karts[0]
	var bumps := 0
	var max_advance := 0.0
	var worst_lat := 0.0
	var old_bump := 0.0
	var ticks := 0
	for i in range(14000):
		var before := float(k["race_s"])
		var command := pilot(race, k) if race.pc_handling else {"second": {"brake": true}}
		race.step_race(STEP, command)
		ticks += 1
		max_advance = maxf(max_advance, absf(float(k["race_s"]) - before))
		worst_lat = maxf(worst_lat, absf(float(k["lat"])))
		if float(k["bump_t"]) > old_bump + STEP:
			bumps += 1
		old_bump = float(k["bump_t"])
		if race.state == "finished":
			break
	return {"id": race.track.id, "finished": race.winner_slot == 0,
		"seconds": snappedf(ticks * STEP, 0.01), "bumps": bumps,
		"max_lat": snappedf(worst_lat, 0.01), "max_progress_tick": snappedf(max_advance, 0.01)}



## Alternating high/low grip and conflicting buttons in both seats, using
## a seeded sequence so an extreme rail contact can be reproduced.
func _stress_test(race: ReefKartRace, course: int) -> Dictionary:
	race.begin()
	var rng := RandomNumberGenerator.new()
	rng.seed = 60261104 + course
	var bounded := true
	var peaks := Vector2.ZERO
	var rail_ticks := 0
	var commands: Array[Dictionary] = [{}, {}]
	for tick in range(2400):
		if tick % 13 == 0:
			for seat in range(2):
				commands[seat] = {"throttle": rng.randf_range(0.2, 1.0),
					"steer": rng.randf_range(-1.0, 1.0), "brake": rng.randf() < 0.19,
					"drift": rng.randf() < 0.35, "item_pressed": rng.randf() < 0.10}
		var before := Vector2(float(race.karts[0]["race_s"]), float(race.karts[1]["race_s"]))
		var input := commands[0].duplicate()
		input["second"] = commands[1]
		race.step_race(STEP, input)
		for seat in range(2):
			var k: Dictionary = race.karts[seat]
			var pos: Vector2 = k["pos"]
			var velocity: Vector2 = k["velocity"]
			var jump := absf(float(k["race_s"]) - before[seat])
			var lat := absf(float(k["lat"]))
			peaks.x = maxf(peaks.x, jump)
			peaks.y = maxf(peaks.y, velocity.length())
			rail_ticks += int(lat >= 123.5)
			bounded = bounded and pos.is_finite() and velocity.is_finite() \
				and jump <= 32.0 and lat <= 124.1 and int(k["lap"]) == 0
	return {"course": race.track.id, "ticks": 2400, "bounded": bounded, "rail_ticks": rail_ticks,
		"peak_progress_per_tick": snappedf(peaks.x, 0.01), "peak_speed": snappedf(peaks.y, 0.01)}
