extends SceneTree
## Targeted follow-up checks: grazing crossings near the true contact boundary,
## and what a lifted finger after guarding does in Title Imp.
## Numbers only; an evaluation harness, never shipped or committed.

var boxing: OperaBoxingSurface
var rng := RandomNumberGenerator.new()
var events: Array = []


func _initialize() -> void:
	call_deferred("_run")


func _on_gesture(kind: String, amount: float, _quality: float) -> void:
	events.append({"kind": kind, "amount": amount})
	# Mirrors OperaCareerWorld2D._on_boxing_gesture at 22df5b75.
	if kind != "boxing_contact" and amount <= 0.0:
		boxing.restart_demo()


func _setup(mode: String, side: int) -> void:
	boxing.set_control_layout(OperaBoxingSurface.TABLET_DIRECT)
	boxing.configure(mode, Color.WHITE)
	boxing.armed_only = false
	boxing._guard_side = side
	events.clear()


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


## Straight glove path crossing the guard-drill lane; the timing offset moves
## the crossing earlier/later relative to the fist.
func _path(centre: Vector2, heading: Vector2, speed: float, t_cross: float, t: float) -> Vector2:
	var at := centre + heading * speed * (t - t_cross)
	return Vector2(clampf(at.x, 62.0, 1218.0), clampf(at.y, 54.0, 682.0))


func _truth_gap(mode: String, side: int, hand: int, centre: Vector2, heading: Vector2,
		speed: float, t_cross: float, flight_start: float, flight_len: float) -> float:
	var best := INF
	# Only the part of the flight while the glove is within 350 px of its
	# crossing point can produce contact; sample that window at 0.25 ms.
	var t_lo := maxf(flight_start, t_cross - 350.0 / speed)
	var t_hi := minf(flight_start + flight_len, t_cross + 350.0 / speed)
	if t_hi < t_lo:
		return 999.0
	var steps := int((t_hi - t_lo) / 0.00025)
	for k in range(steps + 1):
		var tt := t_lo + float(k) * 0.00025
		var p := clampf((tt - flight_start) / flight_len, 0.0, 1.0)
		var g := _path(centre, heading, speed, t_cross, tt)
		best = minf(best, g.distance_to(boxing.incoming_position(p, side))
			- (boxing.glove_contact_radius(hand, g) + boxing.incoming_radius(p)))
	return best


func _engine_blocks(mode: String, side: int, hand: int, centre: Vector2, heading: Vector2,
		speed: float, t_cross: float, fps: float, hitch_at: float) -> bool:
	_setup(mode, side)
	_touch(7, boxing.control_press_position(hand), true)
	_drag_glove(7, hand, _path(centre, heading, speed, t_cross, 0.0))
	var t := 0.0
	var hitched := false
	while t < 8.0:
		var dt := 1.0 / fps
		if hitch_at >= 0.0 and not hitched and t + dt > hitch_at:
			dt = 0.25
			hitched = true
		_drag_glove(7, hand, _path(centre, heading, speed, t_cross, t))
		if mode == "boxing_guard" and boxing.round_index() > 0:
			return true
		boxing._process(dt)
		t += dt
		if mode == "boxing_guard":
			if boxing.round_index() > 0:
				return true
			if boxing.has_friendly_hit_feedback():
				return false
	return false


## For each random geometry, bisect the timing offset to the exact grazing
## point, then test the engine at signed true gaps of +/- 1, 3, 6, 12 px.
func _boundary(fps: float, hitch: bool, trials: int) -> void:
	var mode := "boxing_guard"
	var flight_start := 0.8
	var flight_len := 2.4
	var offsets: Array[float] = [-12.0, -6.0, -3.0, -1.0, 1.0, 3.0, 6.0, 12.0]
	var wrong := {}
	var tested := {}
	for o: float in offsets:
		wrong[o] = 0
		tested[o] = 0
	for trial in range(trials):
		var side := rng.randi_range(0, 1)
		_setup(mode, side)
		var hand := side
		var p_cross := rng.randf_range(0.1, 0.9)
		var speed := rng.randf_range(300.0, 3000.0)
		var angle := rng.randf_range(-0.6, 0.6)
		var heading := Vector2(cos(angle), sin(angle))
		if side == 1:
			heading = -heading
		var centre := boxing.incoming_position(p_cross, side)
		var nominal := flight_start + p_cross * flight_len
		# The glove crosses ahead of the fist when early: search the early side.
		var lo := nominal - 1.6
		var hi := nominal
		if _truth_gap(mode, side, hand, centre, heading, speed, lo, flight_start, flight_len) <= 0.0:
			continue
		for i in range(18):
			var mid := 0.5 * (lo + hi)
			if _truth_gap(mode, side, hand, centre, heading, speed, mid, flight_start, flight_len) > 0.0:
				lo = mid
			else:
				hi = mid
		var graze := 0.5 * (lo + hi)
		for o: float in offsets:
			# Find the timing whose true minimum gap equals the target offset.
			var a := graze - 1.0
			var b := graze + 0.5
			for i in range(18):
				var m := 0.5 * (a + b)
				var gap := _truth_gap(mode, side, hand, centre, heading, speed, m, flight_start, flight_len)
				if gap > o:
					a = m
				else:
					b = m
			var t_cross := 0.5 * (a + b)
			var gap_now := _truth_gap(mode, side, hand, centre, heading, speed, t_cross, flight_start, flight_len)
			if absf(gap_now - o) > 0.5:
				continue
			var hitch_at := t_cross + rng.randf_range(-0.25, 0.05) if hitch else -1.0
			var engine := _engine_blocks(mode, side, hand, centre, heading, speed, t_cross, fps, hitch_at)
			tested[o] += 1
			if engine != (gap_now <= 0.0):
				wrong[o] += 1
	var line := ""
	for o: float in offsets:
		line += " gap%+.0f:%d/%d" % [o, wrong[o], tested[o]]
	print("BOUNDARY|guard|fps=%d|hitch=%s|wrong_by_true_gap_px:%s" % [int(fps), str(hitch), line])


func _release_after_guard() -> void:
	for mode: String in ["boxing_imp", "boxing_guard"]:
		_setup(mode, 0)
		var before := boxing._assist_level
		_touch(5, boxing.control_press_position(0), true)
		_drag_glove(5, 0, boxing.incoming_position(0.55, 0))
		_touch(5, boxing.incoming_position(0.55, 0), false)
		var fails := 0
		for e: Dictionary in events:
			if String(e["kind"]) != "boxing_contact" and float(e["amount"]) <= 0.0:
				fails += 1
		print("RELEASE|%s|guard move then lift finger|failed_try_events=%d|assist %d->%d|demo_replayed=%s" % [
			mode, fails, before, boxing._assist_level, str(boxing.demo_active)])


func _run() -> void:
	rng.seed = 0xB0D7
	boxing = OperaBoxingSurface.new()
	boxing.size = Vector2(1280, 720)
	root.add_child(boxing)
	boxing.set_process(false)
	boxing.gesture.connect(_on_gesture)
	_release_after_guard()
	for fps: float in [30.0, 60.0]:
		_boundary(fps, false, 100)
	_boundary(60.0, true, 100)
	print("BOUNDARY|DONE")
	boxing.queue_free()
	await process_frame
	quit(0)
