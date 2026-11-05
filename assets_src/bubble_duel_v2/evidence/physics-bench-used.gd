extends SceneTree

const BASE := preload("res://scripts/opera_bubble_duel.gd")
const MODES := ["tap", "imprecise", "drag", "interrupt", "hitch"]
const MAX_TIME := 25.0
const MAX_TRIES := 8
var main: ReefMain
var venue: OperaHouseVenue2D
var rng := RandomNumberGenerator.new()
var scratch := OS.get_environment("DUEL_STRESS_DIR")
var settings: Dictionary
var rows: Array[Dictionary] = []


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	settings = {"start_seed":1000, "count":100, "variants":["current"], "output":"v2-physics.json"}
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	Engine.time_scale = 8.0
	await process_frame
	await process_frame
	main._start_menu_ref()._dismiss_menu()
	main.day_one_active = false
	main._skip_intro()
	main.game = "level2"
	main.g["t"] = 0.0
	main._enter_castle_interior_now(false)
	for tick: int in range(12):
		await process_frame
	main._castle_rooms_ref().show_room("opera_hall", false)
	for tick: int in range(3):
		await process_frame
	var routes := main._castle_career_routes_ref()
	if not routes.open_opera_venue():
		quit(2)
		return
	venue = routes.opera_venue
	venue.open_bubble_duel()
	if venue.bubble_duel == null:
		quit(3)
		return
	venue._close_bubble_duel()
	await process_frame
	var base_state := _progress()
	for variant: String in settings.variants:
		var logic: Script = BASE if variant == "current" else (
			load(scratch.path_join(variant + "_traced.gd")) as Script)
		if logic == null or not logic.can_instantiate():
			quit(4)
			return
		var d: Control = logic.new()
		d.setup(main)
		venue.add_child(d)
		d.set_process(false)
		for seed_index: int in range(settings.start_seed, settings.start_seed + settings.count):
			var result := _bout(d, seed_index)
			result["variant"] = variant
			result["save_ok"] = _progress() == base_state
			rows.append(result)
			if seed_index % 10 == 0:
				await process_frame
		d.shutdown()
		venue.remove_child(d)
		d.queue_free()
		await process_frame
		print("DUELBENCH|", variant, "|", settings.count)
	var f := FileAccess.open(scratch.path_join(settings.output), FileAccess.WRITE)
	f.store_string(JSON.stringify({"engine": Engine.get_version_info().string, "settings": settings,
		"rows": rows}, "  "))
	f.close()
	venue.close()
	main.queue_free()
	await process_frame
	quit(0)


func _progress() -> Array:
	return [main.opera_stars, main.opera_progress, main.pearl_count,
		main.medals.duplicate(true), main.chapter2_party_piece_mask,
		main.chapter2_job_phase_masks.duplicate()]


func _pos(d: Control, at: Vector2) -> Vector2:
	return root.get_screen_transform() * (d.get_screen_transform() * at)


func _touch(d: Control, at: Vector2, down: bool, index: int = 1) -> void:
	var event := InputEventScreenTouch.new()
	event.index = index
	event.pressed = down
	event.position = _pos(d, at)
	root.push_input(event, false)


func _drag(d: Control, at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 1
	event.position = _pos(d, at)
	root.push_input(event, false)


func _bout(d: Control, seed_index: int) -> Dictionary:
	rng.seed = 27291 + seed_index * 7531
	var profile: String = MODES[seed_index % MODES.size()]
	d._begin(BASE.Mode.DUEL)
	var dt := 1.0 / (30.0 if seed_index % 2 else 60.0)
	for frame: int in range(12):
		d._process(dt)
	var idle_ok: bool = d.score == 0 and d.swimmer == BASE.START and not d.armed
	_touch(d, Vector2(230, 420), true)
	_drag(d, Vector2(190, 520))
	_touch(d, Vector2(190, 520), false)
	for frame: int in range(85):
		d._process(dt)
	var miss_ok: bool = d.score == 0 and d.rival_bubbles == 2
	d._begin(BASE.Mode.DUEL)
	var elapsed := 0.0
	var taps := 0
	var losses := 0
	var resurfaces := 0
	var cancelled_ok := true
	var first_pop := -1.0
	var pop_gap_max := 0.0
	var max_up_speed := 0.0
	var max_drop_speed := 0.0
	var max_landing_shift := 0.0
	var hit_slots: Array[int] = []
	var attempts_by_pop: Array[int] = []
	var last_pop_at := 0
	var side_identity_ok := true
	var steps := 0
	var raw_owned := 0
	while d.mode == BASE.Mode.DUEL and taps < MAX_TRIES and elapsed < MAX_TIME:
		for settle_frame: int in range(45):
			if d.return_cooldown <= 0.0:
				break
			d._process(dt)
			elapsed += dt
		taps += 1
		var target_slot: int = (seed_index + taps) % int(d.rival_bubbles)
		var target: Vector2 = d._target(target_slot)
		var at := target
		var steering: bool = profile == "drag" and taps <= 5
		if profile == "imprecise" and taps <= 5:
			var radius := rng.randf_range(31.0, 69.0)
			at += Vector2.from_angle(rng.randf_range(0.0, TAU)) * radius
		elif profile == "hitch":
			at += Vector2(rng.randf_range(-25, 25), rng.randf_range(-21, 21))
		if steering:
			at = d.swimmer + Vector2(-30, -12)
		_touch(d, at, true)
		if d.touch_id == 1:
			raw_owned += 1
		if steering:
			var side: float = signf(target.x - d.swimmer.x)
			_drag(d, target + Vector2(side * (BASE.FIN_X + rng.randf_range(-35, 35)),
				-124.0 + rng.randf_range(-18, 18)))
		var held := rng.randf_range(0.05, 0.44)
		if profile == "interrupt" and taps == 1:
			d._process(dt)
			elapsed += dt
			d.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
			_touch(d, at, false)
			var before: Vector2 = d.swimmer
			for frame: int in range(10):
				d._process(dt)
				elapsed += dt
			cancelled_ok = d.swimmer == before and d.score == 0 and not d.armed
			continue
		var holding := true
		var waited := 0.0
		var start_score: int = d.score
		while waited < 3.5 and elapsed < MAX_TIME:
			var step := dt
			if profile == "hitch" and steps % 12 == 7:
				step = 0.115
			var from: Vector2 = d.swimmer
			var before_loss: int = d.player_bubbles
			var old_targets: Array[Vector2] = [d._target(0), d._target(1)]
			var descending: bool = not d.climbing
			d._process(step)
			steps += 1
			waited += step
			elapsed += step
			if holding and waited >= held:
				_touch(d, at, false)
				holding = false
			losses += maxi(0, before_loss - int(d.player_bubbles))
			if from.y > BASE.ARENA.end.y - 20.0 and d.swimmer.y < from.y - 75.0:
				resurfaces += 1
			else:
				max_up_speed = maxf(max_up_speed, (from.y - d.swimmer.y) / step)
				max_drop_speed = maxf(max_drop_speed, (d.swimmer.y - from.y) / step)
				if descending:
					max_landing_shift = maxf(max_landing_shift, absf(d.swimmer.x - from.x) / step)
			if d.score > start_score:
				if first_pop < 0:
					first_pop = elapsed
				var hit: Vector2 = d.pop_at
				if d.score == 1:
					side_identity_ok = hit.distance_to(d._target(0)) > 60.0
				hit_slots.append(0 if hit.distance_to(old_targets[0]) <
					hit.distance_to(old_targets[1]) else 1)
				# Gap against the visible 68px-diameter bubble, using the
				# authored gameplay fin socket and the swept segment.
				var old_fin := from + Vector2(-d.direction * BASE.FIN_X, BASE.FIN_Y)
				var new_fin: Vector2 = d.swimmer + Vector2(-d.direction * BASE.FIN_X, BASE.FIN_Y)
				var nearest := Geometry2D.get_closest_point_to_segment(hit, old_fin, new_fin)
				var frame_gap := hit.distance_to(nearest) - BASE.TARGET_RADIUS
				if d.has_meta(&"bench_swept_gap_px"):
					frame_gap = float(d.get_meta(&"bench_swept_gap_px"))
					d.remove_meta(&"bench_swept_gap_px")
				pop_gap_max = maxf(pop_gap_max, frame_gap)
				attempts_by_pop.append(taps - last_pop_at)
				last_pop_at = taps
				break
			if not holding and not d.armed:
				break
		if holding:
			_touch(d, at, false)
	return {"seed": seed_index, "profile": profile, "fps": roundi(1.0 / dt), "won": d.mode == BASE.Mode.CELEBRATE,
		"pops": d.score, "taps": taps, "seconds": elapsed, "first_pop_s": first_pop,
		"raw_touches_owned": raw_owned, "idle_ok": idle_ok, "cancel_ok": cancelled_ok, "miss_ok": miss_ok, "side_identity_ok": side_identity_ok,
		"losses": losses, "resurfaces": resurfaces, "max_gap_px": pop_gap_max,
		"max_up_px_s": max_up_speed, "max_drop_px_s": max_drop_speed,
		"max_landing_shift_px_s": max_landing_shift,
		"hit_slots": hit_slots, "attempts_by_pop": attempts_by_pop}

