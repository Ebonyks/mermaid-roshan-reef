extends SceneTree
## Bot playthroughs of all five Boxer phases with child-like timing models.
## Numbers only: an evaluation harness, never shipped or committed.
##
## The career is mocked exactly as OperaCareerWorld2D._on_boxing_gesture does at
## 22df5b75: cosmetic contact is ignored, a zero-amount try calls
## surface.restart_demo() again, accepted work banks toward the phase goal and
## completion holds 1.1 s (2.2 s for the belt).

const PHASES: Array[Dictionary] = [
	{"mode": "boxing_guide", "goal": 2, "vo": "op_boxer_work"},
	{"mode": "boxing_jab", "goal": 4, "vo": "op_boxer_jab_stage"},
	{"mode": "boxing_guard", "goal": 3, "vo": "op_boxer_duck_stage"},
	{"mode": "boxing_imp", "goal": 6, "vo": "op_boxer_bell_chase_stage"},
	{"mode": "boxing_belt", "goal": 1, "vo": "op_boxer_belt_stage"},
]
const DT := 1.0 / 60.0
## Stage pixels to millimetres: Lenovo Tab M11 (1920x1200, 10.95 in) and a
## typical 6.4 in 2400x1080 phone, both scaled 1.5 physical px per stage px.
const MM_PER_PX := {"tablet_direct": 0.1842, "phone_edges": 0.0927}
const PROFILES := {
	"quick": {"rt": 0.60, "rt_sigma": 0.20, "speed_mm": 180.0, "err_mm": 2.0,
		"pause_p": 0.03, "anticipate": 0.6, "guard_p": 0.95, "early_p": 0.05,
		"orient": 1.0, "understands_retract": 0.9},
	"typical": {"rt": 0.76, "rt_sigma": 0.30, "speed_mm": 120.0, "err_mm": 3.0,
		"pause_p": 0.10, "anticipate": 0.4, "guard_p": 0.85, "early_p": 0.15,
		"orient": 2.0, "understands_retract": 0.6},
	"slow": {"rt": 1.10, "rt_sigma": 0.35, "speed_mm": 80.0, "err_mm": 4.5,
		"pause_p": 0.25, "anticipate": 0.2, "guard_p": 0.70, "early_p": 0.25,
		"orient": 3.0, "understands_retract": 0.35},
}

var boxing: OperaBoxingSurface
var rng := RandomNumberGenerator.new()
var now := 0.0
var queue: Array[Dictionary] = []
var finger_down := false
var finger_hand := -1
var finger_pos := Vector2.ZERO
var layout := "tablet_direct"
var prof: Dictionary = {}
var phase_goal := 1
var progress := 0.0
var complete_at := -1.0
var log_events: Array[Dictionary] = []
var finger_id := 20
var special := ""


func _initialize() -> void:
	call_deferred("_run")


# ---------------------------------------------------------------- career mock
func _on_gesture(kind: String, amount: float, quality: float) -> void:
	var friendly := kind == "boxing_contact" and boxing.hit_feedback_t > 0.7
	log_events.append({"t": now, "kind": kind, "amount": amount, "friendly": friendly,
		"assist": boxing._assist_level, "imp_state": boxing._imp_state})
	if kind == "boxing_contact":
		return
	if complete_at >= 0.0:
		return
	if amount <= 0.0:
		boxing.restart_demo()
		return
	progress = minf(float(phase_goal), progress + amount)
	boxing.set_fill(progress / float(phase_goal))
	if progress >= float(phase_goal):
		boxing.accept_completion()
		complete_at = now


# ---------------------------------------------------------------- input model
func _lognormal(median: float, sigma: float) -> float:
	return median * exp(rng.randfn(0.0, sigma))


func _rt() -> float:
	var t := _lognormal(float(prof["rt"]), float(prof["rt_sigma"]))
	if rng.randf() < float(prof["pause_p"]):
		t += rng.randf_range(1.0, 4.0)
	return t


func _push(t: float, type: String, pos: Vector2 = Vector2.ZERO, hand: int = -1) -> void:
	queue.append({"t": t, "type": type, "pos": pos, "hand": hand})


func _busy() -> bool:
	return not queue.is_empty()


func _px(mm: float) -> float:
	return mm / float(MM_PER_PX[layout])


func _press_point(hand: int) -> Vector2:
	var base := boxing.control_press_position(hand)
	var jitter := Vector2(rng.randfn(0.0, _px(2.0)), rng.randfn(0.0, _px(2.0)))
	if layout == OperaBoxingSurface.PHONE_EDGES:
		var bay := boxing.edge_control_rect(hand)
		var at := base + jitter
		return Vector2(clampf(at.x, bay.position.x + 4.0, bay.end.x - 4.0),
			clampf(at.y, bay.position.y + 4.0, bay.end.y - 4.0))
	return base + jitter.limit_length(60.0)


## Finger position that would put `hand`'s glove at `glove_goal` for the current claim.
func _finger_for(hand: int, glove_goal: Vector2) -> Vector2:
	return boxing.control_drag_position(hand, glove_goal)


## Schedules a press (if needed) and a noisy minimum-jerk drag that aims the
## glove at `glove_goal`. Returns the scheduled end time.
func _plan_reach(hand: int, glove_goal: Vector2, start_t: float, aim_error: bool = true) -> float:
	var t := start_t
	if finger_down and finger_hand != hand:
		_push(t, "release")
		t += _lognormal(0.25, 0.25)
	if not finger_down or finger_hand != hand:
		_push(t, "press", Vector2.INF, hand)
		t += _lognormal(0.12, 0.3)
	# The drag path is generated when the press has landed (offsets known).
	_push(t, "reach", glove_goal, hand)
	var dist_mm := 60.0
	var duration := 0.15 + dist_mm / float(prof["speed_mm"])
	return t + duration


func _execute_reach(hand: int, glove_goal: Vector2) -> void:
	# A new reach supersedes any unfinished one: one finger follows one intent.
	var kept: Array[Dictionary] = []
	for action: Dictionary in queue:
		if String(action["type"]) != "drag":
			kept.append(action)
	queue = kept
	# Convert the glove goal to the finger goal for this claim, add the child's
	# endpoint error in finger space, then emit one drag per frame.
	var start := finger_pos
	var goal := _finger_for(hand, glove_goal)
	goal += Vector2(rng.randfn(0.0, _px(float(prof["err_mm"]))), rng.randfn(0.0, _px(float(prof["err_mm"]))))
	var dist_mm := start.distance_to(goal) * float(MM_PER_PX[layout])
	var duration := maxf(0.2, (0.15 + dist_mm / float(prof["speed_mm"])) * exp(rng.randfn(0.0, 0.15)))
	var overshoot := rng.randf() < 0.3
	var wobble := rng.randfn(0.0, _px(1.0))
	var normal := (goal - start).orthogonal().normalized() if start.distance_to(goal) > 1.0 else Vector2.ZERO
	var frames := maxi(1, int(ceil(duration / DT)))
	var peak := goal + (goal - start) * 0.12 if overshoot else goal
	for k in range(1, frames + 1):
		var tau := float(k) / float(frames)
		var s := 10.0 * pow(tau, 3) - 15.0 * pow(tau, 4) + 6.0 * pow(tau, 5)
		var at := start.lerp(peak, s) + normal * wobble * sin(PI * tau)
		_push(now + float(k) * DT, "drag", at, hand)
	if overshoot:
		var back := maxi(1, int(ceil(0.25 / DT)))
		for k in range(1, back + 1):
			var tau := float(k) / float(back)
			var s := 10.0 * pow(tau, 3) - 15.0 * pow(tau, 4) + 6.0 * pow(tau, 5)
			_push(now + float(frames + k) * DT, "drag", peak.lerp(goal, s), hand)
	queue.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return float(a["t"]) < float(b["t"]))


func _apply_due() -> void:
	while not queue.is_empty() and float(queue[0]["t"]) <= now + 0.00001:
		var action: Dictionary = queue.pop_front()
		var type := String(action["type"])
		match type:
			"press":
				if not finger_down:
					var at: Vector2 = action["pos"]
					if not at.is_finite():
						at = _press_point(int(action["hand"]))
					var event := InputEventScreenTouch.new()
					finger_id += 1
					event.index = finger_id
					event.position = at
					event.pressed = true
					boxing._gui_input(event)
					finger_down = boxing.touch_owners.has(finger_id)
					finger_hand = int(boxing.touch_owners.get(finger_id, -1))
					finger_pos = at
			"reach":
				if finger_down:
					_execute_reach(int(action["hand"]), action["pos"])
			"drag":
				if finger_down:
					var event := InputEventScreenDrag.new()
					event.index = finger_id
					event.position = action["pos"]
					boxing._gui_input(event)
					finger_pos = action["pos"]
			"release":
				if finger_down:
					var event := InputEventScreenTouch.new()
					event.index = finger_id
					event.position = finger_pos
					event.pressed = false
					boxing._gui_input(event)
				finger_down = false
				finger_hand = -1
			"wait":
				pass


# ---------------------------------------------------------------- behaviours
var guide_state := {}
var cue_seen := {}


func _decide(mode: String) -> void:
	if _busy() or complete_at >= 0.0:
		return
	if special == "masher":
		# Random scribbling: no reading of the screen at all.
		if finger_down and rng.randf() < 0.5:
			_push(now + 0.05, "release")
			return
		var any_hand := rng.randi_range(0, 1)
		var goal := Vector2(rng.randf_range(80.0, 1200.0), rng.randf_range(80.0, 680.0))
		_plan_reach(any_hand, goal, now + rng.randf_range(0.05, 0.4))
		return
	match mode:
		"boxing_guide":
			for hand in range(2):
				if boxing._guide_done[hand]:
					continue
				if finger_down and finger_hand == hand:
					# Still holding after a short try: adjust toward the mitt or let go.
					if rng.randf() < 0.65:
						_push(now + _rt() * 0.5, "reach", boxing.guide_target_position(hand), hand)
					else:
						_push(now + 0.1, "release")
					return
				_plan_reach(hand, boxing.guide_target_position(hand), now + _rt())
				return
			if finger_down:
				_push(now + 0.1, "release")
		"boxing_jab", "boxing_belt":
			var target := boxing.active_target_position()
			if finger_down and boxing._punch_latched[finger_hand]:
				# Landed: most children let go; some pull the glove home while holding.
				if rng.randf() < 0.8:
					_push(now + _lognormal(0.2, 0.3), "release")
				else:
					_push(now + _lognormal(0.25, 0.3), "reach", boxing.glove_rest_position(finger_hand), finger_hand)
				return
			if finger_down:
				# Short of the pad: push again or let go and retry.
				if rng.randf() < 0.6:
					_push(now + _rt() * 0.5, "reach", target, finger_hand)
				else:
					_push(now + 0.1, "release")
				return
			var hand := 0 if target.x < boxing.size.x * 0.5 else 1
			if rng.randf() < 0.25:
				hand = 1 - hand
			_plan_reach(hand, target, now + _rt())
		"boxing_guard":
			_decide_guard(OperaBoxingSurface.COUNTER_SECONDS - boxing._counter_t,
				OperaBoxingSurface.COUNTER_WINDUP, 2.4)
		"boxing_imp":
			_decide_imp()


## Guard reaction, once per attack. `since_cue` is time since its windup began.
func _decide_guard(since_cue: float, windup: float, flight: float) -> void:
	if cue_seen.get("guard_attack", -1) == _attack_serial:
		return
	cue_seen["guard_attack"] = _attack_serial
	_plan_guard(windup, flight, since_cue)


var _attack_serial := 0
var imp_windup_started_at := 0.0


func _plan_guard(windup: float, flight: float, since_cue: float) -> void:
	var side := boxing._guard_side
	var react := maxf(0.0, _rt() + rng.randfn(0.08, 0.04) - since_cue)
	var decide_at := now + react
	var expected_mt := 0.15 + 50.0 / float(prof["speed_mm"])
	var p_now := clampf((since_cue + react - windup) / flight, 0.0, 1.0)
	var p_aim := clampf(p_now + float(prof["anticipate"]) * expected_mt / flight, 0.25, 0.9)
	var aim := boxing.incoming_position(p_aim, side)
	if special == "turtle":
		# Parks one glove in the middle and never follows the lane.
		aim = Vector2(640.0, 420.0)
	var hand := finger_hand if finger_down else side
	_plan_reach(hand, aim, decide_at)


func _decide_imp() -> void:
	var state := boxing._imp_state
	if state == "windup" and cue_seen.get("imp_windup", -1) != _attack_serial:
		cue_seen["imp_windup"] = _attack_serial
		if rng.randf() < float(prof["guard_p"]):
			_plan_guard(1.15 + (0.45 if boxing._assist_level >= 1 else 0.0),
				OperaBoxingSurface.IMP_TRAVEL_SECONDS, now - imp_windup_started_at)
			return
		if rng.randf() < float(prof["early_p"]):
			# Impatient: punches the imp while its guard is closed.
			var hand := 1 if rng.randf() < 0.5 else 0
			_plan_reach(hand, boxing.active_target_position(), now + _rt())
			return
	if state == "recover" and cue_seen.get("imp_open", -1) != _attack_serial:
		cue_seen["imp_open"] = _attack_serial
		var start := now + _rt()
		if finger_down and rng.randf() < 0.35:
			# Many children lift the finger once the punch is stopped.
			var lift_hand := 0 if rng.randf() < 0.5 else 1
			_push(now + _lognormal(0.2, 0.3), "release")
			_push(start + 0.2, "press", Vector2.INF, lift_hand)
			_push(start + 0.32, "reach", boxing.active_target_position(), lift_hand)
			return
		var hand := finger_hand if finger_down else (0 if rng.randf() < 0.5 else 1)
		var glove := boxing.glove_positions[hand]
		var target := boxing.active_target_position()
		var ready_gap := boxing._target_radius() + boxing.glove_contact_radius(hand, glove) + 24.0
		if finger_down and glove.distance_to(target) <= ready_gap:
			if rng.randf() > float(prof["understands_retract"]):
				# A futile push from too close first: nothing registers.
				_push(start, "reach", target, hand)
				start += 0.6 + _rt() * 0.5
			_push(start, "reach", boxing.glove_rest_position(hand), hand)
			start += 0.55
		_plan_reach(hand, target, start)


# ---------------------------------------------------------------- run loop
func _run_phase(phase: Dictionary, limit: float) -> Dictionary:
	boxing.set_control_layout(layout)
	boxing.configure(String(phase["mode"]), Color.WHITE)
	boxing.armed_only = false
	phase_goal = int(phase["goal"])
	progress = 0.0
	complete_at = -1.0
	queue.clear()
	finger_down = false
	finger_hand = -1
	log_events.clear()
	cue_seen.clear()
	_attack_serial = 0
	var start := now
	var mode := String(phase["mode"])
	var assist_two_at := -1.0
	var last_imp_state := boxing._imp_state
	var last_counter_t := boxing._counter_t
	var windows := 0
	var windows_used := 0
	var accepted_in_window := false
	var cycle_starts: Array[float] = []
	# Orientation: listening to the instruction and finding the glowing thing.
	_push(now + _lognormal(float(prof["orient"]), 0.3), "wait")
	while now - start < limit:
		_apply_due()
		if complete_at < 0.0:
			_decide(mode)
		boxing._process(DT)
		now += DT
		if boxing._assist_level >= 2 and assist_two_at < 0.0:
			assist_two_at = now - start
		if mode == "boxing_guard" and boxing._counter_t > last_counter_t + 0.5:
			_attack_serial += 1
		last_counter_t = boxing._counter_t
		if mode == "boxing_imp":
			var state := boxing._imp_state
			if state != last_imp_state:
				if state == "windup":
					cycle_starts.append(now - start)
					imp_windup_started_at = now
					_attack_serial += 1
				if state == "recover":
					windows += 1
					accepted_in_window = false
				if last_imp_state == "recover" and state in ["bopped", "stagger"]:
					windows_used += 1
				last_imp_state = state
		if complete_at >= 0.0 and now - complete_at >= (2.2 if mode == "boxing_belt" else 1.1):
			break
	if finger_down:
		_push(now, "release")
		_apply_due()
	var accepted := 0
	var failed := 0
	var friendly := 0
	var blocks := 0
	var accept_times: Array[float] = []
	for e: Dictionary in log_events:
		var kind := String(e["kind"])
		if kind == "boxing_contact":
			if bool(e["friendly"]):
				friendly += 1
			else:
				blocks += 1
		elif float(e["amount"]) > 0.0:
			accepted += 1
			accept_times.append(float(e["t"]) - start)
		else:
			failed += 1
	if mode == "boxing_guard":
		blocks = accepted
	var gaps: Array[float] = []
	for i in range(1, accept_times.size()):
		gaps.append(accept_times[i] - accept_times[i - 1])
	var periods: Array[float] = []
	for i in range(1, cycle_starts.size()):
		periods.append(cycle_starts[i] - cycle_starts[i - 1])
	return {"mode": mode, "done": complete_at >= 0.0,
		"seconds": (complete_at - start) if complete_at >= 0.0 else limit,
		"accepted": accepted, "failed": failed, "friendly": friendly, "blocks": blocks,
		"assist_final": boxing._assist_level, "assist_two_at": assist_two_at,
		"first_accept": accept_times[0] if not accept_times.is_empty() else -1.0,
		"gaps": gaps, "windows": windows, "windows_used": windows_used, "periods": periods}


func _pct(values: Array, q: float) -> float:
	if values.is_empty():
		return -1.0
	var sorted := values.duplicate()
	sorted.sort()
	var index := clampi(int(round(q * float(sorted.size() - 1))), 0, sorted.size() - 1)
	return float(sorted[index])


func _summarise(label: String, runs: Array) -> void:
	var totals: Array = []
	for run: Array in runs:
		var total := 0.0
		for r: Dictionary in run:
			total += float(r["seconds"])
		totals.append(total)
	print("PLAY|%s|runs=%d|in_phase_total_s p10=%.1f p50=%.1f p90=%.1f" % [
		label, runs.size(), _pct(totals, 0.1), _pct(totals, 0.5), _pct(totals, 0.9)])
	for index in range(PHASES.size()):
		var secs: Array = []
		var done := 0
		var failed: Array = []
		var friendly: Array = []
		var blocks: Array = []
		var assist2: Array = []
		var assist_final_two := 0
		var first: Array = []
		var gaps: Array = []
		var windows: Array = []
		var used: Array = []
		var periods: Array = []
		for run: Array in runs:
			var r: Dictionary = run[index]
			secs.append(float(r["seconds"]))
			if bool(r["done"]):
				done += 1
			failed.append(float(r["failed"]))
			friendly.append(float(r["friendly"]))
			blocks.append(float(r["blocks"]))
			if float(r["assist_two_at"]) >= 0.0:
				assist2.append(float(r["assist_two_at"]))
			if int(r["assist_final"]) >= 2:
				assist_final_two += 1
			first.append(float(r["first_accept"]))
			gaps.append_array(r["gaps"])
			windows.append(float(r["windows"]))
			used.append(float(r["windows_used"]))
			periods.append_array(r["periods"])
		print("PLAY|%s|%s|done=%d/%d|secs p10=%.1f p50=%.1f p90=%.1f|first_unit p50=%.1f|gap_between_units p50=%.2f p90=%.2f|fails p50=%.0f p90=%.0f|friendly p50=%.0f|blocks p50=%.0f|assist_max_share=%.2f|assist2_at p50=%.1f|windows p50=%.0f used p50=%.0f|imp_cycle p50=%.2f p90=%.2f" % [
			label, String(PHASES[index]["mode"]), done, runs.size(), _pct(secs, 0.1), _pct(secs, 0.5), _pct(secs, 0.9),
			_pct(first, 0.5), _pct(gaps, 0.5), _pct(gaps, 0.9), _pct(failed, 0.5), _pct(failed, 0.9),
			_pct(friendly, 0.5), _pct(blocks, 0.5), float(assist_final_two) / float(runs.size()),
			_pct(assist2, 0.5), _pct(windows, 0.5), _pct(used, 0.5), _pct(periods, 0.5), _pct(periods, 0.9)])


func _voice_lengths() -> void:
	var total := 0.0
	var line := ""
	for phase: Dictionary in PHASES:
		var path := "res://assets/audio/voices/filler_v1/roshan_%s.ogg" % String(phase["vo"])
		var length := -1.0
		if ResourceLoader.exists(path):
			var stream := load(path) as AudioStream
			if stream != null:
				length = stream.get_length()
		total += maxf(0.0, length)
		line += " %s=%.2f" % [String(phase["vo"]), length]
	print("VOICE|instruction_seconds|%s|total=%.2f" % [line, total])


func _run() -> void:
	rng.seed = 0xB0C5E12
	boxing = OperaBoxingSurface.new()
	boxing.size = Vector2(1280, 720)
	root.add_child(boxing)
	boxing.set_process(false)
	boxing.gesture.connect(_on_gesture)
	boxing.set_control_layout(OperaBoxingSurface.PHONE_EDGES)
	print("LAYOUT|phone_bays|left=%s|right=%s|press_left=%s" % [
		boxing.edge_control_rect(0), boxing.edge_control_rect(1), boxing.control_press_position(0)])
	_voice_lengths()
	var started := Time.get_ticks_msec()
	var runs_per := 120
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("runs="):
			runs_per = int(arg.substr(5))
	for profile_name: String in ["quick", "typical", "slow"]:
		for layout_name: String in [OperaBoxingSurface.TABLET_DIRECT, OperaBoxingSurface.PHONE_EDGES]:
			prof = PROFILES[profile_name]
			layout = layout_name
			var runs: Array = []
			for run_index in range(runs_per):
				var run: Array = []
				for phase: Dictionary in PHASES:
					run.append(_run_phase(phase, 240.0))
				runs.append(run)
			_summarise("%s|%s" % [profile_name, layout_name], runs)
	for extra: Array in [["masher", "typical", OperaBoxingSurface.TABLET_DIRECT],
			["masher", "typical", OperaBoxingSurface.PHONE_EDGES],
			["turtle", "typical", OperaBoxingSurface.TABLET_DIRECT]]:
		special = String(extra[0])
		prof = PROFILES[String(extra[1])]
		layout = String(extra[2])
		var extra_runs: Array = []
		for run_index in range(maxi(4, runs_per / 2)):
			var run: Array = []
			for phase: Dictionary in PHASES:
				run.append(_run_phase(phase, 240.0))
			extra_runs.append(run)
		_summarise("%s|%s" % [special, layout], extra_runs)
	special = ""
	print("PLAY|elapsed_s=%.1f" % (float(Time.get_ticks_msec() - started) / 1000.0))
	print("PLAY|DONE")
	boxing.queue_free()
	await process_frame
	quit(0)
