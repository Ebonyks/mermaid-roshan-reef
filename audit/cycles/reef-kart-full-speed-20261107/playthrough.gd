extends SceneTree

const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Pilot := preload("res://scripts/probe_reef_kart_handling.gd")
const DEVICES := [6, 11]
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
var recorder := AudioEffectRecord.new()

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
	var frame := {"t": elapsed(), "race": race.race_time, "state": race.state, "attempt": race.attempt, "karts": snapshot}
	var picture := root.get_texture().get_image()
	if picture != null:
		picture.resize(960, 540, Image.INTERPOLATE_BILINEAR)
		var name := "%05d.jpg" % recorded
		if picture.save_jpg(leg_dir.path_join(name), 0.83) == OK:
			frame["file"] = name
			recorded += 1
	frames.append(frame)

func _run() -> void:
	Engine.max_fps = 60
	root.title = "Reef Grand Prix full-speed review"
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	var args := OS.get_cmdline_user_args()
	target_dir = ProjectSettings.globalize_path(args[0])
	DirAccess.make_dir_recursive_absolute(target_dir)
	recorder.format = AudioStreamWAV.FORMAT_16_BITS
	AudioServer.add_bus_effect(0, recorder)
	pc = Scene.instantiate() as PC
	root.add_child(pc)
	var first := int(args[1]) if args.size() > 1 else 0
	var last := int(args[2]) if args.size() > 2 else 7
	var errors := 0
	for leg in range(first, last + 1):
		slots = 1 + leg / 4
		var course := leg % 4
		pc._show_garage(slots, DEVICES[0])
		if slots == 2:
			pc._join(DEVICES[1])
		for slot in range(slots):
			pc._toggle_ready(slot)
		pc._choose_course(course)
		pc._start_race()
		race = pc._race
		race.rng.seed = 77201 + leg
		leg_dir = target_dir.path_join(race.track.id + "-" + str(slots) + "p")
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
		recorder.set_recording_active(true)
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
			if Time.get_ticks_msec() - last_frame >= 82:
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
		recorder.set_recording_active(false)
		var wav := recorder.get_recording()
		if wav != null:
			wav.save_to_wav(leg_dir.path_join("master.wav"))
		var report := {"mode": slots, "course": race.track.id, "length": race.track.length, "wall": elapsed(),
			"finish": race.state == "finished", "winner": race.winner_slot, "attempt": race.attempt,
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
	AudioServer.remove_bus_effect(0, AudioServer.get_bus_effect_count(0) - 1)
	print("DONE|", errors)
	quit(errors)
