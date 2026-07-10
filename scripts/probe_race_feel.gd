extends SceneTree
# RACE FEEL TELEMETRY — run with: godot --headless --fixed-fps 60 -s scripts/probe_race_feel.gd
# Measures the quantifiable components of "game feel" for the slide racer and
# prints FEEL| metrics for comparison against feel_targets.json.
var main: Node3D
var player: Node3D
const DT := 1.0 / 60.0

func _init() -> void:
	Engine.time_scale = 1.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	player = main.player
	# ---------- RUN 1: fish mode, no input (baseline physics) ----------
	var m0 := await _run_slide("fish", "none")
	_report("fish/no-input", m0)
	# ---------- RUN 2: fish mode, bang-bang steering (response/agency) ----------
	var m1 := await _run_slide("fish", "bangbang")
	_report("fish/bang-bang", m1)
	# ---------- RUN 3: fish mode, reactive fish-seeker ----------
	var m2 := await _run_slide("fish", "seek")
	_report("fish/seeker", m2)
	print("FEEL|fish_all_collected_by_seeker=", m2["got"], "/5")
	# ---------- RUNS 4-8: chase mode fairness under a toddler policy ----------
	var wins := 0
	var catch_times: Array = []
	for i in range(5):
		var mc := await _run_slide("chase", "toddler", i)
		if bool(mc["won"]):
			wins += 1
			catch_times.append(mc["dur"])
	print("FEEL|chase_toddler_winrate=", wins, "/5  catch_times=", catch_times)
	# ---------- RUN 9: chase, perfect play ----------
	var mp := await _run_slide("chase", "perfect")
	print("FEEL|chase_perfect_won=", mp["won"], " dur=%.1f" % mp["dur"])
	# ---------- static track metrics ----------
	# ---------- line advantage: inside vs outside cornering ----------
	var mi := await _run_slide("fish", "inside")
	var mo := await _run_slide("fish", "outside")
	print("FEEL|line_advantage: inside=%.2fs outside=%.2fs delta=%.2fs (0.00 = lateral position is cosmetic = autopilot)" %
		[mi["dur"], mo["dur"], mo["dur"] - mi["dur"]])
	# ---------- drift system exercise (meaningful after R2.5 lands) ----------
	var md := await _run_slide("fish", "drifter")
	print("FEEL|drifter: dur=%.2fs vs no-input %.2fs -> skill_time_delta=%.2fs (target >= 2.0 after R2.5)" %
		[md["dur"], m0["dur"], m0["dur"] - md["dur"]])
	print("FEEL|drifter: drift_uptime=%.1fs boost_peak=%.1f tiers=%s" %
		[md.get("drift_t", 0.0), md.get("boost_max", 0.0), str(md.get("tiers", 0))])
	# ---------- drift system metrics (all 0/absent until implemented) ----------
	print("FEEL|drift: state_exists=", main.g.has("drift") if main.game == "slide" else "n/a",
		" (expect drift/meter/boost keys after R2.5)")
	await _track_metrics()
	# machine-readable summary for diffing between tuning iterations
	var summary := {"no_input": m0, "bangbang": m1, "seeker": m2,
		"chase_toddler_wins": wins, "chase_catch_times": catch_times,
		"chase_perfect": mp}
	var f := FileAccess.open("user://race_feel.json", FileAccess.WRITE)
	if f != null:
		f.store_string(JSON.stringify(summary, "  "))
		print("FEEL|json_written=user://race_feel.json")
	quit()

func _steer_for(policy: String, t: float, seed_i: int) -> float:
	var g: Dictionary = main.g
	match policy:
		"none":
			return 0.0
		"bangbang":
			return 1.0 if fmod(t, 2.0) < 1.0 else -1.0
		"seek":
			var pos: Vector3 = player.position
			for fd in g.get("fish", []):
				if not bool(fd["got"]):
					var fp: Vector3 = fd["pos"]
					var right: Vector3 = main._slide_sample(float(g["s"]))[2]
					var lat: float = (fp - pos).dot(right)
					return clampf(-lat * 0.5, -1.0, 1.0)   # steer input is screen-space (negated in tick)
			return 0.0
		"toddler":
			# 300ms reaction lag, noisy, over/under-corrects — approximates a 4yo
			var px: float = float(g.get("peng_x", 0.0))
			var x: float = float(g.get("x", 0.0))
			var err: float = px - x
			var noisy: float = err + sin(t * 3.1 + float(seed_i)) * 3.0
			return clampf(-signf(noisy) * (0.0 if absf(noisy) < 1.5 else 1.0), -1.0, 1.0) \
				if fmod(t + float(seed_i) * 0.13, 0.45) > 0.3 else 0.0   # intermittent input
		"inside", "outside":
			# steer toward the inside (or outside) of the current curve
			var s_now: float = float(g.get("s", 0.0))
			var t0: Vector3 = main._slide_sample(s_now)[1]
			var t1: Vector3 = main._slide_sample(s_now + 6.0)[1]
			var curve_sign: float = signf(t0.cross(t1).y)   # + = curving left
			if curve_sign == 0.0:
				return 0.0
			var want: float = curve_sign if policy == "inside" else -curve_sign
			# steer input is screen-space (negated in tick vs 'right' vector)
			return clampf(want, -1.0, 1.0)
		"drifter":
			var s_d: float = float(g.get("s", 0.0))
			var td0: Vector3 = main._slide_sample(s_d)[1]
			var td1: Vector3 = main._slide_sample(s_d + 6.0)[1]
			var cs: float = signf(td0.cross(td1).y)
			return cs   # full commit into every bend, releases automatically between bends
		"perfect":
			var px2: float = float(g.get("peng_x", 0.0))
			var x2: float = float(g.get("x", 0.0))
			return clampf(-(px2 - x2) * 2.0, -1.0, 1.0)
	return 0.0

func _run_slide(mode: String, policy: String, seed_i: int = 0) -> Dictionary:
	if main.game != "":
		main._clear_game()
	for i in range(90):
		await process_frame
	var fr := {"fname": "FeelTest", "game": "slide", "theme": "rainbow" if mode == "fish" else "ice",
		"mode": mode, "won": true, "cool": 0.0}
	main._start_game(fr)
	await process_frame
	var g: Dictionary = main.g
	var t := 0.0
	var frames := 0
	var vmin := 1e9; var vmax := -1e9
	var yaw_prev: float = player.yaw
	var yaw_jerk_max := 0.0
	var yaw_jerks_over_2deg := 0
	var cam_prev: Vector3 = player.cam.global_position if player.cam else Vector3.ZERO
	var wall_bounces := 0
	var vx_prev := 0.0
	var steer_on_t := -1.0
	var vx_63_t := -1.0
	var steer_speed_corr_n := 0.0
	var flow_count := 0
	var last_s := 0.0
	var drift_t := 0.0
	var boost_max := 0.0
	var tiers := 0
	while main.game == "slide" and t < 60.0:
		var steer := _steer_for(policy, t, seed_i)
		# inject steering through the real touch path
		main.touch_ui.stick_vec = Vector2(steer, 0.0)
		# --- latency measurement: first sustained steer -> 63% of terminal vx ---
		if policy == "bangbang":
			if steer_on_t < 0.0 and absf(steer) > 0.5:
				steer_on_t = t
			var term: float = 38.0 * 0.26   # SLIDE_STEER * tau
			if steer_on_t >= 0.0 and vx_63_t < 0.0 and absf(float(g.get("vx", 0.0))) > term * 0.63:
				vx_63_t = t - steer_on_t
		await process_frame
		t += DT; frames += 1
		var v: float = float(g.get("v", 0.0)) + float(g.get("boost", 0.0))
		vmin = minf(vmin, v); vmax = maxf(vmax, v)
		if bool(g.get("drift", false)):
			drift_t += DT
		boost_max = maxf(boost_max, float(g.get("boost", 0.0)))
		tiers = maxi(tiers, int(g.get("drift_tier", 0)))
		# yaw jerk (deg per frame) — polyline heading snap
		var dyaw: float = absf(wrapf(player.yaw - yaw_prev, -PI, PI)) * 180.0 / PI
		yaw_jerk_max = maxf(yaw_jerk_max, dyaw)
		if dyaw > 2.0:
			yaw_jerks_over_2deg += 1
		yaw_prev = player.yaw
		# wall bounce detect (vx sign flip while |x| at limit)
		var vx: float = float(g.get("vx", 0.0))
		if signf(vx) != signf(vx_prev) and absf(float(g.get("x", 0.0))) > (18.0 * 0.5 - 2.1):
			wall_bounces += 1
		vx_prev = vx
		# does steering ever change forward speed? (agency check)
		steer_speed_corr_n += absf(steer) * absf(v - clampf(v, 13.0, 26.0))
		last_s = float(g.get("s", 0.0))
	var dur := t
	# visual flow density: nodes within 25m lateral of track per 100m of run
	return {"dur": dur, "vmin": vmin, "vmax": vmax, "yaw_jerk_max": yaw_jerk_max,
		"yaw_jerks": yaw_jerks_over_2deg, "bounces": wall_bounces,
		"latency63": vx_63_t, "speed_agency": steer_speed_corr_n,
		"won": (main.trophies > 0 or bool(g.get("caught", false))), "got": int(g.get("got", 0)),
		"frames": frames, "s_end": last_s,
		"drift_t": drift_t, "boost_max": boost_max, "tiers": tiers}

func _report(label: String, m: Dictionary) -> void:
	print("FEEL|", label, ": dur=%.1fs v=[%.1f..%.1f] speed_range_ratio=%.2f" %
		[m["dur"], m["vmin"], m["vmax"], (m["vmax"] / maxf(m["vmin"], 0.01))])
	print("FEEL|", label, ": yaw_jerk_max=%.2fdeg/frame yaw_snaps=%d wall_bounces=%d steer_latency63=%.2fs speed_agency=%.3f" %
		[m["yaw_jerk_max"], m["yaw_jerks"], m["bounces"], m["latency63"], m["speed_agency"]])

func _track_metrics() -> void:
	# rebuild a slide to inspect static properties
	if main.game != "":
		main._clear_game()
	for i in range(90):
		await process_frame
	var fr := {"fname": "T", "game": "slide", "theme": "ice", "mode": "fish", "won": true, "cool": 0.0}
	main._start_game(fr)
	for i in range(5):
		await process_frame
	if main.game != "slide":
		print("FEEL|track: REBUILD FAILED (game=", main.game, ")")
		return
	var g: Dictionary = main.g
	var path: Array = g["path"]
	var total: float = g["total"]
	var seg_lens: Array = []
	var max_kink := 0.0
	for i in range(path.size() - 2):
		var a: Vector3 = (path[i + 1] - path[i]).normalized()
		var b: Vector3 = (path[i + 2] - path[i + 1]).normalized()
		max_kink = maxf(max_kink, rad_to_deg(acos(clampf(a.dot(b), -1.0, 1.0))))
		seg_lens.append((path[i + 1] - path[i]).length())
	var trackside := 0
	for n in main.game_nodes:
		if n is Node3D and is_instance_valid(n):
			trackside += 1
	print("FEEL|track: total_len=%.0fm segments=%d avg_seg=%.1fm max_kink=%.1fdeg" %
		[total, path.size() - 1, total / float(path.size() - 1), max_kink])
	print("FEEL|track: trackside_nodes=%d density=%.1f per 100m" %
		[trackside, float(trackside) / total * 100.0])
	print("FEEL|track: countdown_present=", float(g.get("timer", -1.0)) > 0.0)
	main._clear_game()
	await process_frame
