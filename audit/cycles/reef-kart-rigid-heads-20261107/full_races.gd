extends SceneTree

const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Pilot := preload("res://scripts/probe_reef_kart_handling.gd")
const DEVICES := [6, 11]
# Each entry is course, first driver/ride, second driver/ride.
const CASES := [
	[0, 2, 1, -1, 0], [1, 7, 0, -1, 0],
	[2, 8, 1, 11, 2], [3, 4, 2, 9, 0],
]
var pc: PC
var race: ReefKartRace
var slots := 1
var target_dir: String
var leg_dir: String
var frames: Array[Dictionary] = []
var events: Array[Dictionary] = []
var changed_voices := ""
var award_time := [-100.0, -100.0]
var item_sent := ["", ""]
var leg_start := 0
var recorded := 0
var last_frame := 0
var last_status := 0

func _initialize() -> void:
	call_deferred("_run")

func axis(slot: int, channel: JoyAxis, value: float) -> void:
	var event := InputEventJoypadMotion.new()
	event.device = DEVICES[slot]
	event.axis = channel
	event.axis_value = value
	Input.parse_input_event(event)

func button(slot: int, key: JoyButton, down: bool) -> void:
	if Input.is_joy_button_pressed(DEVICES[slot], key) == down:
		return
	var event := InputEventJoypadButton.new()
	event.device = DEVICES[slot]
	event.button_index = key
	event.pressed = down
	Input.parse_input_event(event)

func elapsed() -> float:
	return (Time.get_ticks_msec() - leg_start) * 0.001

func on_award(slot: int, kind: String) -> void:
	award_time[slot] = elapsed()
	item_sent[slot] = ""
	events.append({"event": "award", "slot": slot, "kind": kind, "t": elapsed(), "race": race.race_time})

func race_event(kind: String, value: float) -> void:
	if kind in ["finish", "restart", "imp_win", "turbo", "item_used", "item_roll"]:
		events.append({"event": kind, "value": value, "t": elapsed(), "race": race.race_time})

func drive(slot: int) -> void:
	var kart: Dictionary = race.karts[slot]
	var s := float(kart["track_s"])
	var speed := float(kart["speed"])
	var cmd := Pilot.pilot(race, kart)
	var lat := 0.0 if slots == 1 else (-20.0 if slot == 0 else 20.0)
	if String(kart["item"]).is_empty() and float(kart["roulette_t"]) <= 0.0:
		var ahead := 160.0
		for pickup: Dictionary in race.track.bubbles:
			var gap := fposmod(float(pickup["s"]) - s, race.track.length)
			if gap < ahead and gap > 7.0 and float(pickup["respawn_t"]) <= 0.0:
				var pickup_lat := float(pickup["lat"])
				if slots == 2 and absf(pickup_lat - lat) > 60.0:
					continue
				ahead = gap
				lat = pickup_lat
	var look := clampf(speed * 0.25, 40.0, 76.0)
	var direction := race.track.point_at(s + look, lat) - (kart["pos"] as Vector2)
	var yaw := atan2(direction.x, -direction.y)
	var steer := clampf(angle_difference(float(kart["heading"]), yaw) * 3.2, -1.0, 1.0)
	axis(slot, JOY_AXIS_LEFT_X, signf(steer) * (0.10 + 0.90 * absf(steer)) if absf(steer) > 0.01 else 0.0)
	var t := race.race_time
	var gas := float(cmd["throttle"]) > 0.0
	if t < 1.30:
		gas = t > 0.32 and not (0.78 < t and t < 1.05)
	var digital := (t < 1.05) == (slot == 0)
	button(slot, JOY_BUTTON_A, gas and digital)
	axis(slot, JOY_AXIS_TRIGGER_RIGHT, 0.03 if t < 0.32 else float(gas and not digital))
	axis(slot, JOY_AXIS_TRIGGER_LEFT, float(cmd["brake"]))
	var use: bool = t > 1.30 and String(kart["item"]) != "" and elapsed() - float(award_time[slot]) > (0.6 if int(s) % 2 == 0 else 3.4) and item_sent[slot] == ""
	if use:
		item_sent[slot] = String(kart["item"])
		events.append({"event": "use_button", "slot": slot, "kind": item_sent[slot], "t": elapsed(), "race": t})
	button(slot, JOY_BUTTON_X, use)

func _sample() -> void:
	var snapshot: Array[Dictionary] = []
	for slot in range(slots):
		var k: Dictionary = race.karts[slot]
		var cam := race if slot == 0 else pc._second_view
		snapshot.append({"s": k["race_s"], "lat": k["lat"], "speed": k["speed"], "lap": k["lap"],
			"heading": k["heading"], "item": k["item"], "gas": pc._controls_for(slot).get("throttle", 0.0),
			"zone": floori(4.0 * race.track.wrap_s(float(k["track_s"])) / race.track.length),
			"camera": [cam.cam_pos.x, cam.cam_pos.y, cam.cam_heading]})
	var frame := {"t": elapsed(), "race": race.race_time, "fps": Engine.get_frames_per_second(), "state": race.state, "attempt": race.attempt, "karts": snapshot}
	var picture := root.get_texture().get_image()
	if picture != null:
		frame["capture_size"] = [picture.get_width(), picture.get_height()]
		if picture.get_size() != Vector2i(1280, 720):
			push_error("Motion capture window resized: %s" % picture.get_size())
		picture.resize(640, 360, Image.INTERPOLATE_BILINEAR)
		var name := "%05d.jpg" % recorded
		if picture.save_jpg(leg_dir.path_join(name), 0.78) == OK:
			frame["file"] = name
			recorded += 1
	frames.append(frame)

func _run() -> void:
	Engine.max_fps = 60
	root.title = "Reef Grand Prix full race pose review"
	root.unresizable = true
	root.min_size = Vector2i(1280, 720)
	root.max_size = Vector2i(1280, 720)
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	var args := OS.get_cmdline_user_args()
	target_dir = ProjectSettings.globalize_path(args[0])
	DirAccess.make_dir_recursive_absolute(target_dir)
	pc = Scene.instantiate() as PC
	root.add_child(pc)
	var first := int(args[1]) if args.size() > 1 else 0
	var last := int(args[2]) if args.size() > 2 else CASES.size() - 1
	var errors := 0
	for leg in range(first, last + 1):
		var entry: Array = CASES[leg]
		slots = 1 if int(entry[3]) < 0 else 2
		var course := int(entry[0])
		pc._show_garage(slots, DEVICES[0])
		if slots == 2:
			pc._join(DEVICES[1])
		pc._drivers[0] = int(entry[1])
		pc._rides[0] = int(entry[2])
		if slots == 2:
			pc._drivers[1] = int(entry[3])
			pc._rides[1] = int(entry[4])
		for slot in range(slots):
			pc._toggle_ready(slot)
		pc._choose_course(course)
		pc._start_race()
		race = pc._race
		race.rng.seed = 77201 + leg
		leg_dir = target_dir.path_join("%02d-%s-%dp" % [leg, race.track.id, slots])
		DirAccess.make_dir_recursive_absolute(leg_dir)
		frames.clear()
		events.clear()
		changed_voices = ""
		item_sent = ["", ""]
		award_time = [-100.0, -100.0]
		recorded = 0
		last_frame = 0
		last_status = 0
		race.item_awarded.connect(on_award)
		race.race_event.connect(race_event)
		var props: Array[Dictionary] = []
		for p: Dictionary in race.track.landmarks:
			var pos: Vector2 = p["pos"]
			props.append({"id": p["id"], "s": p["s"], "pos": [pos.x, pos.y], "zone": p.get("zone", -1), "w": p["w"]})
		leg_start = Time.get_ticks_msec()
		print("RUN|", leg, "|", race.track.id, "|", slots, "p|length=", race.track.length)
		while race.state != "finished" and elapsed() < 245.0:
			await process_frame
			if pc._paused:
				for slot in range(slots):
					button(slot, JOY_BUTTON_A, false)
					button(slot, JOY_BUTTON_X, false)
					axis(slot, JOY_AXIS_LEFT_X, 0.0)
					axis(slot, JOY_AXIS_TRIGGER_RIGHT, 0.0)
					axis(slot, JOY_AXIS_TRIGGER_LEFT, 0.0)
				events.append({"event": "resume", "t": elapsed(), "race": race.race_time})
				button(0, JOY_BUTTON_START, true)
				await process_frame
				button(0, JOY_BUTTON_START, false)
				await physics_frame
				await process_frame
			for slot in range(slots):
				if race.state == "race":
					drive(slot)
				else:
					button(slot, JOY_BUTTON_A, false)
					button(slot, JOY_BUTTON_X, false)
					axis(slot, JOY_AXIS_TRIGGER_RIGHT, 0.0)
					axis(slot, JOY_AXIS_TRIGGER_LEFT, 0.0)
			var v: Node = race.item_voice
			var active := "" if not v.playing else str(v.active) + str(v.stream.resource_path)
			if changed_voices != active:
				events.append({"event": "voice", "active": v.active.duplicate() if v.playing else {},
					"t": elapsed(), "race": race.race_time, "stream": v.stream.resource_path if v.playing else ""})
				changed_voices = active
			if int(elapsed()) >= last_status + 15:
				last_status = int(elapsed())
				print("LIVE|", leg, "|wall=", elapsed(), "|game=", race.race_time, "|attempt=", race.attempt, "|state=", race.state)
			if Time.get_ticks_msec() - last_frame >= 1150:
				last_frame = Time.get_ticks_msec()
				await RenderingServer.frame_post_draw
				_sample()
		await RenderingServer.frame_post_draw
		_sample()
		for slot in range(slots):
			button(slot, JOY_BUTTON_A, false)
			button(slot, JOY_BUTTON_X, false)
			axis(slot, JOY_AXIS_TRIGGER_RIGHT, 0.0)
			axis(slot, JOY_AXIS_TRIGGER_LEFT, 0.0)
			axis(slot, JOY_AXIS_LEFT_X, 0.0)
		var report := {"mode": slots, "course": race.track.id, "length": race.track.length, "wall": elapsed(),
			"cast": entry.slice(1), "finish": race.state == "finished", "winner": race.winner_slot, "attempt": race.attempt,
			"frames": frames, "events": events, "props": props}
		var file := FileAccess.open(leg_dir.path_join("run.json"), FileAccess.WRITE)
		file.store_string(JSON.stringify(report))
		file.close()
		print("END|", leg, "|", race.track.id, "|finish=", report["finish"], "|game=", race.race_time,
			"|wall=", elapsed(), "|frames=", recorded, "|events=", events.size())
		if not bool(report["finish"]):
			errors += 1
		await process_frame
	pc._reset_content()
	pc.queue_free()
	await process_frame
	print("DONE|", errors)
	quit(errors)
