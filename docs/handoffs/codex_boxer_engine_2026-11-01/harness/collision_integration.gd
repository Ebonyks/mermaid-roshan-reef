extends SceneTree
## Independent integration checks of Boxer guard contact through the real
## OperaBoxingSurface input/process path, compared with continuous geometry.
## Numbers only; an evaluation harness, never shipped or committed.

var boxing: OperaBoxingSurface
var rng := RandomNumberGenerator.new()
var events: Array = []
var career_mock := false
var mock_progress := 0.0


func _initialize() -> void:
	call_deferred("_run")


func _on_gesture(kind: String, amount: float, quality: float) -> void:
	events.append({"kind": kind, "amount": amount, "quality": quality,
		"assist": boxing._assist_level})
	if not career_mock:
		return
	# Mirrors OperaCareerWorld2D._on_boxing_gesture at 22df5b75: cosmetic contact
	# is ignored; a zero-amount try calls surface.restart_demo() again.
	if kind == "boxing_contact":
		return
	if amount <= 0.0:
		boxing.restart_demo()
		return
	mock_progress += amount


func _setup(layout: String, mode: String, side: int) -> void:
	boxing.set_control_layout(layout)
	boxing.configure(mode, Color.WHITE)
	boxing.armed_only = false
	boxing._guard_side = side
	events.clear()
	mock_progress = 0.0


func _touch(finger: int, at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = finger
	event.position = at
	event.pressed = pressed
	boxing._gui_input(event)


func _drag_glove(finger: int, hand: int, glove_at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = finger
	event.position = boxing.control_drag_position(hand, glove_at)
	boxing._gui_input(event)


## Continuous expectation for a stationary glove: minimum over the flight of
## centre distance minus the summed padded radii (negative = overlap).
func _held_min_gap(hand: int, glove: Vector2) -> float:
	var rg := boxing.glove_contact_radius(hand, glove)
	var best := INF
	for k in range(4001):
		var p := float(k) / 4000.0
		var gap := glove.distance_to(boxing.incoming_position(p)) - (rg + boxing.incoming_radius(p))
		best = minf(best, gap)
	return best


## Runs until the current attack resolves. Returns [resolved, blocked, seconds].
func _run_attack(mode: String, fps: float, hitch_at: float = -1.0, limit: float = 7.0) -> Array:
	var t := 0.0
	var start_side := boxing._guard_side
	var start_round := boxing.round_index()
	var hitched := false
	while t < limit:
		var dt := 1.0 / fps
		if hitch_at >= 0.0 and not hitched and t >= hitch_at:
			dt = 0.25
			hitched = true
		boxing._process(dt)
		t += dt
		if mode == "boxing_guard":
			if boxing.round_index() > start_round:
				return [true, true, t]
			if boxing.has_friendly_hit_feedback():
				return [true, false, t]
			if boxing._guard_side != start_side:
				return [true, true, t]
		else:
			if boxing._imp_state == "recover":
				return [true, not boxing.has_friendly_hit_feedback(), t]
	return [false, false, t]


func _held_guard_map(fps: float, step: int, label: String, hitch: bool) -> Dictionary:
	var out := {"runs": 0, "agree": 0, "engine_only": 0, "analytic_only": 0, "unresolved": 0,
		"borderline": 0, "miss_examples": [], "false_examples": [],
		"both_lane_cells": {}, "block_cells": {}}
	for mode: String in ["boxing_guard", "boxing_imp"]:
		for side in range(2):
			for hand in range(2):
				for y in range(90, 691, step):
					for x in range(260, 1021, step):
						_setup(OperaBoxingSurface.TABLET_DIRECT, mode, side)
						_touch(7, boxing.control_press_position(hand), true)
						_drag_glove(7, hand, Vector2(x, y))
						var glove := boxing.glove_positions[hand]
						var gap := _held_min_gap(hand, glove)
						var hitch_at := rng.randf_range(0.5, 3.0) if hitch else -1.0
						var result := _run_attack(mode, fps, hitch_at)
						out["runs"] += 1
						if not bool(result[0]):
							out["unresolved"] += 1
							continue
						var engine_block := bool(result[1])
						var expected := gap <= 0.0
						if absf(gap) < 1.0:
							out["borderline"] += 1
						if engine_block == expected:
							out["agree"] += 1
						elif engine_block:
							out["engine_only"] += 1
							if (out["false_examples"] as Array).size() < 4:
								(out["false_examples"] as Array).append("%s side=%d hand=%d at=%s gap=%.2f" % [mode, side, hand, glove, gap])
						else:
							out["analytic_only"] += 1
							if (out["miss_examples"] as Array).size() < 4:
								(out["miss_examples"] as Array).append("%s side=%d hand=%d at=%s gap=%.2f" % [mode, side, hand, glove, gap])
						var key := "%s|%d|%d|%d" % [mode, hand, x, y]
						if engine_block:
							var cells: Dictionary = out["block_cells"]
							cells[key] = int(cells.get(key, 0)) | (1 << side)
	print("HELD|%s|runs=%d|agree=%d|engine_only=%d|analytic_only=%d|unresolved=%d|borderline=%d" % [
		label, out["runs"], out["agree"], out["engine_only"], out["analytic_only"], out["unresolved"], out["borderline"]])
	for e: String in out["miss_examples"]:
		print("HELD|%s|miss_example|%s" % [label, e])
	for e: String in out["false_examples"]:
		print("HELD|%s|false_example|%s" % [label, e])
	return out


func _parking_summary(map: Dictionary) -> void:
	var cells: Dictionary = map["block_cells"]
	for mode: String in ["boxing_guard", "boxing_imp"]:
		for hand in range(2):
			var any := 0
			var both := 0
			for key: String in cells:
				if not key.begins_with("%s|%d|" % [mode, hand]):
					continue
				var bits := int(cells[key])
				any += 1
				if bits == 3:
					both += 1
			print("PARK|%s|hand=%d|cells_blocking_any_lane=%d|cells_blocking_both_lanes=%d|share_both=%.3f" % [
				mode, hand, any, both, float(both) / maxf(1.0, float(any))])
	# Can one glove parked on the centre line block every attack of a drill?
	for mode: String in ["boxing_guard", "boxing_imp"]:
		var line := ""
		for y in [250, 330, 410, 490, 570]:
			var blocks := 0
			for side in range(2):
				_setup(OperaBoxingSurface.TABLET_DIRECT, mode, side)
				_touch(7, boxing.control_press_position(0), true)
				_drag_glove(7, 0, Vector2(640, y))
				if bool(_run_attack(mode, 60.0)[1]):
					blocks += 1
			line += " y%d=%d/2" % [y, blocks]
		print("PARK|%s|left glove parked at x=640 blocks:%s" % [mode, line])


## Simultaneous motion: a glove crossing the lane while the fist travels.
## Ground truth samples continuous time; the engine sees one accumulated drag
## event per frame followed by _process(dt), as Godot delivers them.
func _crossing(mode: String, fps: float, trials: int, hitch: bool) -> void:
	var stats := {"truth_contact": 0, "engine_block": 0, "agree": 0, "missed": 0, "false": 0,
		"borderline_disagree": 0, "unresolved": 0}
	var miss_depths: Array[float] = []
	var false_gaps: Array[float] = []
	var flight_len := 2.4 if mode == "boxing_guard" else OperaBoxingSurface.IMP_TRAVEL_SECONDS
	var nominal_start := 0.8 if mode == "boxing_guard" else 2.55
	for trial in range(trials):
		var side := rng.randi_range(0, 1)
		_setup(OperaBoxingSurface.TABLET_DIRECT, mode, side)
		var hand := side
		var p_cross := rng.randf_range(0.05, 0.95)
		var speed := rng.randf_range(100.0, 3000.0)
		var angle := rng.randf_range(-0.7, 0.7)
		var heading := Vector2(cos(angle), sin(angle))
		if side == 1:
			heading = -heading
		var centre := boxing.incoming_position(p_cross, side)
		var t_cross := nominal_start + p_cross * flight_len + rng.randf_range(-0.35, 0.35)
		var path := func(t: float) -> Vector2:
			var at: Vector2 = centre + heading * speed * (t - t_cross)
			return Vector2(clampf(at.x, 62.0, 1218.0), clampf(at.y, 54.0, 682.0))
		_touch(7, boxing.control_press_position(hand), true)
		var t := 0.0
		_drag_glove(7, hand, path.call(0.0))
		var hitch_at := t_cross + rng.randf_range(-0.2, 0.05) if hitch else -1.0
		var hitched := false
		var blocked := false
		var resolved := false
		var start_round := boxing.round_index()
		# The guard drill's flight always starts at 0.8 s. The imp's windup can
		# lengthen if a stray drag reaches its closed guard, so its exact start is
		# read back from the engine's own state clock.
		var flight_start := 0.8 if mode == "boxing_guard" else -1.0
		while t < 8.0:
			var dt := 1.0 / fps
			if hitch_at >= 0.0 and not hitched and t + dt > hitch_at:
				dt = 0.25
				hitched = true
			_drag_glove(7, hand, path.call(t))
			if mode == "boxing_guard" and boxing.round_index() > start_round:
				blocked = true
				resolved = true
				break
			if mode == "boxing_imp" and boxing._imp_state == "recover":
				blocked = not boxing.has_friendly_hit_feedback()
				resolved = true
				break
			var assist_during_frame := boxing._assist_level
			boxing._process(dt)
			t += dt
			if mode == "boxing_imp" and flight_start < 0.0 and boxing._imp_state != "taunt":
				# Taunt always lasts 1.4 s from configure; the windup length is
				# fixed at that boundary from the assist level of that frame.
				flight_start = 1.4 + 1.15 + (0.45 if assist_during_frame >= 1 else 0.0)
			if mode == "boxing_guard":
				if boxing.round_index() > start_round:
					blocked = true
					resolved = true
					break
				if boxing.has_friendly_hit_feedback():
					resolved = true
					break
			elif boxing._imp_state == "recover":
				blocked = not boxing.has_friendly_hit_feedback()
				resolved = true
				break
		if not resolved or flight_start < 0.0:
			stats["unresolved"] += 1
			continue
		# Continuous truth over the actual flight interval, sampled at 0.5 ms.
		boxing._guard_side = side
		var truth_min := INF
		var steps := int(flight_len / 0.0005)
		for k in range(steps + 1):
			var tt := flight_start + float(k) * 0.0005
			var p := clampf((tt - flight_start) / flight_len, 0.0, 1.0)
			var g: Vector2 = path.call(tt)
			var gap := g.distance_to(boxing.incoming_position(p, side)) \
				- (boxing.glove_contact_radius(hand, g) + boxing.incoming_radius(p))
			truth_min = minf(truth_min, gap)
		var truth := truth_min <= 0.0
		if truth:
			stats["truth_contact"] += 1
		if blocked:
			stats["engine_block"] += 1
		if blocked == truth:
			stats["agree"] += 1
		elif absf(truth_min) < 2.0:
			stats["borderline_disagree"] += 1
		elif truth:
			stats["missed"] += 1
			miss_depths.append(-truth_min)
		else:
			stats["false"] += 1
			false_gaps.append(truth_min)
	miss_depths.sort()
	false_gaps.sort()
	var miss_max := miss_depths[-1] if not miss_depths.is_empty() else 0.0
	var false_max := false_gaps[-1] if not false_gaps.is_empty() else 0.0
	print("CROSS|%s|fps=%d|hitch=%s|trials=%d|truth_contact=%d|engine_block=%d|agree=%d|missed=%d|false=%d|borderline_disagree=%d|unresolved=%d|max_true_overlap_missed_px=%.2f|max_true_gap_falsely_blocked_px=%.2f" % [
		mode, int(fps), str(hitch), trials, stats["truth_contact"], stats["engine_block"], stats["agree"],
		stats["missed"], stats["false"], stats["borderline_disagree"], stats["unresolved"], miss_max, false_max])


func _imp_counter_gate() -> void:
	# Unblocked: the glove never leaves rest.
	_setup(OperaBoxingSurface.TABLET_DIRECT, "boxing_imp", 0)
	var t := 0.0
	var open_at := -1.0
	var hit_at := -1.0
	while t < 6.0 and open_at < 0.0:
		boxing._process(1.0 / 60.0)
		t += 1.0 / 60.0
		if boxing.has_friendly_hit_feedback() and hit_at < 0.0:
			hit_at = t
		if boxing._imp_state == "recover":
			open_at = t
	print("IMPGATE|unblocked|counter_window_opens_at=%.3f|friendly_contact=%s|window_seconds=%.2f" % [
		open_at, str(hit_at >= 0.0), boxing._imp_state_t])
	# Blocked with a held guard at three points along the lane.
	for p: float in [0.2, 0.5, 0.8]:
		_setup(OperaBoxingSurface.TABLET_DIRECT, "boxing_imp", 0)
		_touch(7, boxing.control_press_position(0), true)
		_drag_glove(7, 0, boxing.incoming_position(p, 0))
		var result := _run_attack("boxing_imp", 60.0)
		print("IMPGATE|held_guard_p=%.1f|counter_window_opens_at=%.3f|blocked=%s|assist=%d" % [
			p, float(result[2]), str(result[1]), boxing._assist_level])


func _assist_ladder() -> void:
	career_mock = true
	# One short sideways jab attempt, released.
	_setup(OperaBoxingSurface.TABLET_DIRECT, "boxing_jab", 0)
	var rest := boxing.control_press_position(0)
	_touch(7, rest, true)
	_drag_glove(7, 0, rest + Vector2(-60, -10))
	_touch(7, rest + Vector2(-60, -10), false)
	print("ASSIST|jab one sideways try released|assist_level=%d|target_radius=%.0f" % [
		boxing._assist_level, boxing._target_radius()])
	# One punch into the imp's closed guard.
	_setup(OperaBoxingSurface.TABLET_DIRECT, "boxing_imp", 0)
	rest = boxing.control_press_position(1)
	_touch(8, rest, true)
	_drag_glove(8, 1, boxing.active_target_position())
	print("ASSIST|imp one punch on closed guard|assist_level=%d|windup_after=%.2f|counter_window_after=%.2f" % [
		boxing._assist_level, 1.15 + (0.45 if boxing._assist_level >= 1 else 0.0),
		1.7 + (0.5 if boxing._assist_level >= 1 else 0.0)])
	# One unblocked guard-drill punch.
	_setup(OperaBoxingSurface.TABLET_DIRECT, "boxing_guard", 0)
	_run_attack("boxing_guard", 60.0)
	print("ASSIST|guard one unblocked punch|assist_level=%d" % boxing._assist_level)
	# Does assist ever decay within a phase after successes?
	_setup(OperaBoxingSurface.TABLET_DIRECT, "boxing_jab", 0)
	boxing.restart_demo()
	boxing.restart_demo()
	var before := boxing._assist_level
	for i in range(3):
		var r := boxing.control_press_position(0)
		_touch(9, r, true)
		_drag_glove(9, 0, boxing.active_target_position())
		_touch(9, boxing.active_target_position(), false)
		for k in range(30):
			boxing._process(1.0 / 60.0)
	print("ASSIST|after three accepted jabs|assist_before=%d|assist_after=%d|accepted=%d" % [
		before, boxing._assist_level, boxing.round_index()])
	career_mock = false


func _run() -> void:
	rng.seed = 0xB0BB1E5
	boxing = OperaBoxingSurface.new()
	boxing.size = Vector2(1280, 720)
	root.add_child(boxing)
	boxing.set_process(false)
	boxing.gesture.connect(_on_gesture)
	var started := Time.get_ticks_msec()
	var map := _held_guard_map(60.0, 16, "fps60_step16", false)
	_parking_summary(map)
	_held_guard_map(30.0, 32, "fps30_step32_hitch", true)
	for mode: String in ["boxing_guard", "boxing_imp"]:
		for fps: float in [30.0, 60.0]:
			_crossing(mode, fps, 3000, false)
		_crossing(mode, 60.0, 2000, true)
	_imp_counter_gate()
	_assist_ladder()
	print("INTEG|elapsed_s=%.1f" % (float(Time.get_ticks_msec() - started) / 1000.0))
	print("INTEG|DONE")
	boxing.queue_free()
	await process_frame
	quit(0)
