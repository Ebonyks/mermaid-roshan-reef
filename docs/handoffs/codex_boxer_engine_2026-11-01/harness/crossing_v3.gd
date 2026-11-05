extends SceneTree
## Simultaneous glove/fist motion in Godot's real frame order: the input event
## for a frame (finger position at that frame's time) is handled first, then
## _process(delta) advances the world to the same time. Paths stay inside the
## glove clamp, so differences come from the engine, not from edge clamping.
## Errors are binned by the true minimum gap. Numbers only; never shipped.

var boxing: OperaBoxingSurface
var rng := RandomNumberGenerator.new()


func _initialize() -> void:
	call_deferred("_run")


func _setup(mode: String, side: int) -> void:
	boxing.set_control_layout(OperaBoxingSurface.TABLET_DIRECT)
	boxing.configure(mode, Color.WHITE)
	boxing.armed_only = false
	boxing._guard_side = side


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


func _inside(at: Vector2) -> bool:
	return at.x >= 70.0 and at.x <= 1210.0 and at.y >= 62.0 and at.y <= 674.0


func _config(mode: String, fps: float, stutter: float, trials: int) -> void:
	var fist_speed := 475.2 / (2.4 if mode == "boxing_guard" else OperaBoxingSurface.IMP_TRAVEL_SECONDS)
	var frame_travel := fist_speed * maxf(1.0 / fps, stutter)
	var bins := ["deep_contact", "shallow_contact", "near_miss", "clear_miss"]
	var count := {}
	var wrong := {}
	for b: String in bins:
		count[b] = 0
		wrong[b] = 0
	var worst_miss := 0.0
	var worst_false := 0.0
	var phase_wrong := {"launch": 0, "mid": 0, "arrival": 0}
	var phase_worst := {"launch": 0.0, "mid": 0.0, "arrival": 0.0}
	var done := 0
	var attempts := 0
	while done < trials and attempts < trials * 20:
		attempts += 1
		var side := rng.randi_range(0, 1)
		var hand := side
		_setup(mode, side)
		var p_cross := rng.randf_range(0.05, 0.95)
		var speed := rng.randf_range(300.0, 3000.0)
		var angle := rng.randf_range(-0.6, 0.6)
		var heading := Vector2(cos(angle), sin(angle))
		if side == 1:
			heading = -heading
		var centre := boxing.incoming_position(p_cross, side)
		var reach := 400.0
		if not _inside(centre - heading * reach) or not _inside(centre + heading * reach):
			continue
		var nominal := (0.8 if mode == "boxing_guard" else 2.55) \
			+ p_cross * (2.4 if mode == "boxing_guard" else OperaBoxingSurface.IMP_TRAVEL_SECONDS)
		var t_cross := nominal + rng.randf_range(-0.35, 0.35)
		var t_enter := t_cross - reach / speed
		var t_leave := t_cross + reach / speed
		if t_enter < 0.2:
			continue
		var path := func(t: float) -> Vector2:
			var tt := clampf(t, t_enter, t_leave)
			return centre + heading * speed * (tt - t_cross)
		_touch(7, boxing.control_press_position(hand), true)
		_drag_glove(7, hand, path.call(0.0))
		var stutter_at := t_cross + rng.randf_range(-0.2, 0.05) if stutter > 0.0 else -1.0
		var stuttered := false
		var t := 0.0
		var blocked := false
		var resolved := false
		var flight_start := 0.8 if mode == "boxing_guard" else -1.0
		while t < 8.0 and not resolved:
			var dt := 1.0 / fps
			if stutter_at >= 0.0 and not stuttered and t + dt > stutter_at:
				dt = stutter
				stuttered = true
			var t_next := t + dt
			# Real order: this frame's input first, then the world advances.
			_drag_glove(7, hand, path.call(t_next))
			if mode == "boxing_guard" and boxing.round_index() > 0:
				blocked = true
				resolved = true
				break
			if mode == "boxing_imp" and boxing._imp_state == "recover":
				blocked = not boxing.has_friendly_hit_feedback()
				resolved = true
				break
			var assist_during := boxing._assist_level
			boxing._process(dt)
			t = t_next
			if mode == "boxing_imp" and flight_start < 0.0 and boxing._imp_state != "taunt":
				flight_start = 1.4 + 1.15 + (0.45 if assist_during >= 1 else 0.0)
			if mode == "boxing_guard":
				if boxing.round_index() > 0:
					blocked = true
					resolved = true
				elif boxing.has_friendly_hit_feedback():
					resolved = true
			elif boxing._imp_state == "recover":
				blocked = not boxing.has_friendly_hit_feedback()
				resolved = true
		if not resolved or flight_start < 0.0:
			continue
		var flight_len := 2.4 if mode == "boxing_guard" else OperaBoxingSurface.IMP_TRAVEL_SECONDS
		var t_lo := maxf(flight_start, t_enter)
		var t_hi := minf(flight_start + flight_len, t_leave)
		var gap := 999.0
		var gap_t := -1.0
		if t_hi >= t_lo:
			var steps := int((t_hi - t_lo) / 0.00025)
			boxing._guard_side = side
			for k in range(steps + 1):
				var tt := t_lo + float(k) * 0.00025
				var p := clampf((tt - flight_start) / flight_len, 0.0, 1.0)
				var g: Vector2 = path.call(tt)
				var gg := g.distance_to(boxing.incoming_position(p, side)) 					- (boxing.glove_contact_radius(hand, g) + boxing.incoming_radius(p))
				if gg < gap:
					gap = gg
					gap_t = tt
		var bin := "clear_miss"
		if gap < -frame_travel:
			bin = "deep_contact"
		elif gap <= 0.0:
			bin = "shallow_contact"
		elif gap < frame_travel:
			bin = "near_miss"
		count[bin] += 1
		if blocked != (gap <= 0.0):
			var frame := maxf(1.0 / fps, stutter)
			var when := "mid"
			if gap_t - flight_start <= frame + 0.0005:
				when = "launch"
			elif flight_start + flight_len - gap_t <= frame + 0.0005:
				when = "arrival"
			phase_wrong[when] += 1
			phase_worst[when] = maxf(float(phase_worst[when]), absf(gap))
			wrong[bin] += 1
			if gap <= 0.0:
				worst_miss = maxf(worst_miss, -gap)
			else:
				worst_false = maxf(worst_false, gap)
		done += 1
	var line := ""
	for b: String in bins:
		line += " %s=%d/%d" % [b, wrong[b], count[b]]
	print("CROSS3|%s|fps=%d|stutter=%.2fs|fist_px_per_frame=%.1f|trials=%d|wrong=%d|launch=%d(max %.1fpx)|mid=%d(max %.1fpx)|arrival=%d(max %.1fpx)|missed_max=%.1f|false_max=%.1f" % [
		mode, int(fps), stutter, frame_travel, done,
		int(phase_wrong["launch"]) + int(phase_wrong["mid"]) + int(phase_wrong["arrival"]),
		phase_wrong["launch"], phase_worst["launch"], phase_wrong["mid"], phase_worst["mid"],
		phase_wrong["arrival"], phase_worst["arrival"], worst_miss, worst_false])


func _run() -> void:
	rng.seed = 0xC2055
	boxing = OperaBoxingSurface.new()
	boxing.size = Vector2(1280, 720)
	root.add_child(boxing)
	boxing.set_process(false)
	var only := "boxing_imp"
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("mode="):
			only = arg.substr(5)
	for fps: float in [30.0, 60.0]:
		_config(only, fps, 0.0, 1500)
	_config(only, 60.0, 0.10, 1000)
	_config(only, 60.0, 0.25, 1000)
	print("CROSS3|DONE")
	boxing.queue_free()
	await process_frame
	quit(0)
