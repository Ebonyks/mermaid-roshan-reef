extends SceneTree
## Full-clock steering and boost exercises. All inputs go through the PC garage
## controller path, and every character/ride drives solo and in each pane.
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const SCENE := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const ART := preload("res://scripts/racer/reef_kart_rider_art.gd")
const CATALOG := preload("res://scripts/racer/reef_kart_catalog.gd")
const DEVICES := [6, 11]
const CASE_LENGTH := 3.58
const VIEWPORT := Vector2i(1280, 720)
var output: String
var pc: PC
var failures := 0
var reports: Array[Dictionary] = []

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	Engine.max_fps = 60
	root.title = "Reef Grand Prix rigid seated pose exercises"
	root.unresizable = true
	root.min_size = VIEWPORT
	root.max_size = VIEWPORT
	root.size = VIEWPORT
	root.content_scale_size = VIEWPORT
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	var args := OS.get_cmdline_user_args()
	output = ProjectSettings.globalize_path(args[0])
	DirAccess.make_dir_recursive_absolute(output)
	pc = SCENE.instantiate() as PC
	root.add_child(pc)
	var first := int(args[1]) if args.size() > 1 else 0
	var last := int(args[2]) if args.size() > 2 else 71
	for index in range(first, last + 1):
		await _case(1 + index / 36, index % 12, (index % 36) / 12)
	var report := FileAccess.open(output.path_join("report.json"), FileAccess.WRITE)
	report.store_string(JSON.stringify(reports))
	report.close()
	pc._reset_content()
	pc.queue_free()
	await process_frame
	print("POSE_PLAY|DONE|", reports.size(), "|failures=", failures)
	quit(failures)

func _case(players: int, driver: int, ride: int) -> void:
	pc._show_garage(players, DEVICES[0])
	if players == 2:
		pc._join(DEVICES[1])
	pc._drivers[0] = driver
	pc._rides[0] = ride
	pc._drivers[1] = (driver + 5) % CATALOG.driver_count()
	pc._rides[1] = (ride + 1) % CATALOG.RIDES.size()
	for slot in range(players):
		pc._toggle_ready(slot)
	pc._choose_course((driver + ride) % 4)
	pc._start_race()
	await process_frame
	await process_frame
	var race := pc._race
	var station := _straight(race.track)
	race.state = "race"
	race.go_t = 0.0
	race.race_time = 0.0
	for slot in range(race.karts.size()):
		var k: Dictionary = race.karts[slot]
		var at := station - (72.0 if slot >= players else 0.0)
		var lane := -27.0 if slot == 0 else 27.0
		var speed := 270.0 * float(k["pace"])
		k["race_s"] = at
		k["track_s"] = at
		k["lat"] = lane
		k["pos"] = race.track.point_at(at, lane)
		k["heading"] = race.track.heading_at(at)
		k["velocity"] = race.track.tangent_at(at) * speed
		k["speed"] = speed
		if slot < players:
			k["item"] = "zoom"
	race._update_camera(1.0, true)
	if players == 2:
		pc._second_view.refresh_camera_view(race, 1.0)
	var seen := [{}, {}]
	var sequences := [[], []]
	var prefix := "%dp-d%02d-r%d" % [players, driver, ride]
	var start := Time.get_ticks_msec()
	var max_speed := [0.0, 0.0]
	var boost_start := [0.0, 0.0]
	var boosted := [false, false]
	var boost_release := [false, false]
	var last_frame := [-1, -1]
	var simulation_start := race.race_time
	while race.race_time - simulation_start < CASE_LENGTH and Time.get_ticks_msec() - start < 14000:
		await process_frame
		if pc._paused:
			for slot in range(players):
				_axis(slot, JOY_AXIS_LEFT_X, 0.0)
				_axis(slot, JOY_AXIS_TRIGGER_RIGHT, 0.0)
				_button(slot, JOY_BUTTON_X, false)
			_button(0, JOY_BUTTON_START, true)
			await process_frame
			_button(0, JOY_BUTTON_START, false)
			await physics_frame
			await process_frame
		var t := race.race_time - simulation_start
		var requested := -1.0 if 0.18 < t and t < 0.42 else 0.0
		if 0.43 < t and t < 0.79:
			requested = 1.0
		if 0.80 < t and t < 1.01:
			requested = -0.62
		var to_capture: Array[Vector2i] = []
		for slot in range(players):
			var k: Dictionary = race.karts[slot]
			var steer := requested if slot == 0 else -requested
			if 1.01 <= t and t < 2.75:
				var lane := -27.0 if slot == 0 else 27.0
				var forward_point := race.track.point_at(float(k["track_s"]) + 92.0, lane)
				var target := forward_point - (k["pos"] as Vector2)
				steer = clampf(angle_difference(float(k["heading"]), atan2(target.x, -target.y)) * 2.0, -1.0, 1.0)
			_axis(slot, JOY_AXIS_TRIGGER_RIGHT, 1.0)
			_axis(slot, JOY_AXIS_LEFT_X, steer)
			_button(slot, JOY_BUTTON_X, 1.10 < t and t < 1.28)
			var frame := ART.motion_frame(k["rider_pose"])
			var speed := float(k["speed"])
			max_speed[slot] = maxf(float(max_speed[slot]), speed)
			if float(k["boost_t"]) > 0.0 and not boosted[slot]:
				boosted[slot] = true
				boost_start[slot] = t
			if boosted[slot] and t > float(boost_start[slot]) + 1.40 and frame == 0:
				boost_release[slot] = true
			if last_frame[slot] != frame:
				last_frame[slot] = frame
				sequences[slot].append([snappedf(t, 0.001), frame, snappedf(speed, 0.01)])
			if not seen[slot].has(frame):
				seen[slot][frame] = true
				to_capture.append(Vector2i(slot, frame))
		if not to_capture.is_empty():
			await RenderingServer.frame_post_draw
			var frame_image := root.get_texture().get_image()
			if frame_image.get_size() != VIEWPORT:
				failures += 1
			else:
				for view in to_capture:
					var x := 640 if players == 1 else 320 + view.x * 640
					var crop := frame_image.get_region(Rect2i(x - 128, 254, 256, 288))
					var file := "%s-p%d-f%d.jpg" % [prefix, view.x, view.y]
					if crop.save_jpg(output.path_join(file), 0.84) != OK:
						failures += 1
	for slot in range(players):
		_axis(slot, JOY_AXIS_TRIGGER_RIGHT, 0.0)
		_axis(slot, JOY_AXIS_LEFT_X, 0.0)
		_button(slot, JOY_BUTTON_X, false)
		var k: Dictionary = race.karts[slot]
		var expected := ART.MOTION_COUNT
		var reported_keys: Array = seen[slot].keys()
		reported_keys.sort()
		var passed: bool = seen[slot].size() == expected and boosted[slot] and boost_release[slot] 			and float(max_speed[slot]) >= 270.0 * float(k["pace"])
		if not passed:
			failures += 1
			print("POSE_PLAY|MISS|", prefix, "|p", slot, "|keys=", reported_keys,
				"|boosted=", boosted[slot], "|recovered=", boost_release[slot])
		reports.append({"case": prefix, "slot": slot, "driver": k["driver"], "ride": k["vehicle"],
			"course": race.track.id, "keys": reported_keys, "sequence": sequences[slot],
			"max_speed": max_speed[slot], "recovered": boost_release[slot], "pass": passed})
	if players == 2 and not is_same(race.karts, pc._second_view.karts):
		failures += 1
	print("POSE_PLAY|CASE|", prefix, "|", race.track.id, "|elapsed=", race.race_time, "|failures=", failures)

func _straight(track: ReefKartTrack) -> float:
	var best := 0.0
	var minimum := INF
	for i in range(120):
		var at := track.length * float(i) / 120.0
		var score := 0.0
		for j in range(10):
			score += absf(track.curvature_at(at + j * 42.0))
		if score < minimum:
			minimum = score
			best = at
	return best

func _axis(slot: int, channel: JoyAxis, value: float) -> void:
	var event := InputEventJoypadMotion.new()
	event.device = DEVICES[slot]
	event.axis = channel
	event.axis_value = value
	Input.parse_input_event(event)

func _button(slot: int, key: JoyButton, down: bool) -> void:
	if Input.is_joy_button_pressed(DEVICES[slot], key) == down:
		return
	var event := InputEventJoypadButton.new()
	event.device = DEVICES[slot]
	event.button_index = key
	event.pressed = down
	Input.parse_input_event(event)
