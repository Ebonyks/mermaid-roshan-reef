extends SceneTree
# ADVISORY stress test / balance playtest for the Dust Bunny Boss — the first
# boss encounter in the game (DUST_BUNNY_BOSS_2026-08-02.md).
#
# Twenty-five simulated children fight Grand Puff on the OctagonStage. Each
# persona has a real reaction delay to the flash, a real walking speed on the
# virtual stick, a wrong-tap rate, a wander rate, and GAWK — the pause to
# stare at the sparkles after landing a bonk. Every tap goes through
# touch_ui exactly like a finger, so nothing here can win without input.
#
# The encounter is pumped with a FIXED timestep (main's own tick is parked on
# an inert branch) so the numbers are reproducible on any machine.
#
# This probe is ADVISORY: it prints metrics and a verdict and never the
# gate's failure tokens.

const DT := 0.05                  # 20 simulated ticks per second
const TIME_CAP := 300.0           # per-run simulated cap
const BAND_LO := 45.0             # target fight length, showing excluded
const BAND_HI := 120.0
const RUNS := 25

# Personas calibrated to a real 3-5 year old on a phone, not to an optimal
# bot. reaction = seconds from the star lighting up to the finger landing;
# err = chance a tap goes off at the wrong moment; speed = fraction of full
# stick deflection she actually holds; wander = chance per second of walking
# somewhere else entirely; gawk = seconds frozen watching her own sparkles;
# mash = taps per second she throws regardless of what the boss is doing.
const PERSONAS: Array[Dictionary] = [
	{"name": "speedy", "reaction": 0.55, "err": 0.06, "speed": 0.90, "wander": 0.05, "gawk": 0.5, "mash": 0.0},
	{"name": "speedy", "reaction": 0.65, "err": 0.08, "speed": 0.88, "wander": 0.06, "gawk": 0.6, "mash": 0.0},
	{"name": "speedy", "reaction": 0.60, "err": 0.05, "speed": 0.92, "wander": 0.04, "gawk": 0.4, "mash": 0.1},
	{"name": "speedy", "reaction": 0.70, "err": 0.10, "speed": 0.85, "wander": 0.08, "gawk": 0.7, "mash": 0.0},
	{"name": "speedy", "reaction": 0.58, "err": 0.07, "speed": 0.90, "wander": 0.05, "gawk": 0.5, "mash": 0.2},
	{"name": "casual", "reaction": 1.10, "err": 0.15, "speed": 0.70, "wander": 0.15, "gawk": 1.2, "mash": 0.05},
	{"name": "casual", "reaction": 1.25, "err": 0.18, "speed": 0.68, "wander": 0.18, "gawk": 1.4, "mash": 0.05},
	{"name": "casual", "reaction": 1.00, "err": 0.14, "speed": 0.72, "wander": 0.12, "gawk": 1.0, "mash": 0.10},
	{"name": "casual", "reaction": 1.35, "err": 0.20, "speed": 0.65, "wander": 0.20, "gawk": 1.6, "mash": 0.05},
	{"name": "casual", "reaction": 1.15, "err": 0.16, "speed": 0.70, "wander": 0.16, "gawk": 1.3, "mash": 0.08},
	{"name": "wander", "reaction": 1.60, "err": 0.12, "speed": 0.55, "wander": 0.55, "gawk": 1.8, "mash": 0.02},
	{"name": "wander", "reaction": 1.80, "err": 0.10, "speed": 0.50, "wander": 0.62, "gawk": 2.0, "mash": 0.02},
	{"name": "wander", "reaction": 1.45, "err": 0.14, "speed": 0.58, "wander": 0.50, "gawk": 1.6, "mash": 0.04},
	{"name": "wander", "reaction": 2.00, "err": 0.12, "speed": 0.48, "wander": 0.68, "gawk": 2.2, "mash": 0.02},
	{"name": "wander", "reaction": 1.70, "err": 0.11, "speed": 0.52, "wander": 0.58, "gawk": 1.9, "mash": 0.03},
	{"name": "masher", "reaction": 0.80, "err": 0.35, "speed": 0.75, "wander": 0.10, "gawk": 0.6, "mash": 1.30},
	{"name": "masher", "reaction": 0.90, "err": 0.40, "speed": 0.72, "wander": 0.12, "gawk": 0.7, "mash": 1.60},
	{"name": "masher", "reaction": 0.75, "err": 0.32, "speed": 0.78, "wander": 0.08, "gawk": 0.5, "mash": 2.00},
	{"name": "masher", "reaction": 0.85, "err": 0.38, "speed": 0.74, "wander": 0.11, "gawk": 0.6, "mash": 1.10},
	{"name": "masher", "reaction": 0.95, "err": 0.42, "speed": 0.70, "wander": 0.14, "gawk": 0.8, "mash": 1.80},
	{"name": "timid ", "reaction": 2.20, "err": 0.10, "speed": 0.45, "wander": 0.25, "gawk": 2.6, "mash": 0.0},
	{"name": "timid ", "reaction": 2.60, "err": 0.12, "speed": 0.40, "wander": 0.30, "gawk": 3.0, "mash": 0.0},
	{"name": "timid ", "reaction": 2.00, "err": 0.08, "speed": 0.50, "wander": 0.22, "gawk": 2.4, "mash": 0.0},
	{"name": "timid ", "reaction": 3.00, "err": 0.14, "speed": 0.38, "wander": 0.35, "gawk": 3.4, "mash": 0.0},
	{"name": "timid ", "reaction": 2.40, "err": 0.11, "speed": 0.42, "wander": 0.28, "gawk": 2.8, "mash": 0.0},
]

# Control extremes, run with `-- --controls`: the edges the persona spread
# cannot reach. They answer "what happens if she puts the phone down", "does
# never looking at the star still win", and "is the ceiling a real ceiling".
const CONTROLS: Array[Dictionary] = [
	{"name": "asleep", "reaction": 999.0, "err": 0.0, "speed": 0.0, "wander": 0.0, "gawk": 0.0, "mash": 0.0},
	{"name": "blind ", "reaction": 999.0, "err": 0.0, "speed": 0.7, "wander": 0.1, "gawk": 0.0, "mash": 2.0},
	{"name": "robot ", "reaction": 0.15, "err": 0.0, "speed": 1.0, "wander": 0.0, "gawk": 0.0, "mash": 0.0},
	{"name": "slowpk", "reaction": 4.00, "err": 0.15, "speed": 0.35, "wander": 0.4, "gawk": 4.0, "mash": 0.0},
	{"name": "rooted", "reaction": 0.80, "err": 0.05, "speed": 0.0, "wander": 0.0, "gawk": 0.5, "mash": 0.0},
]

var main: ReefMain
var boss: DustBossGame
var roster: Array[Dictionary] = PERSONAS
var run_count := RUNS
var roster_label: String = "PERSONAS"

# ---- per-run persona state -------------------------------------------------
var persona: Dictionary = {}
var gawk_t := 0.0                 # frozen, staring at sparkles
var react_t := -1.0               # countdown to the finger landing on the flash
var armed := false                # this window's reaction has been scheduled
var wander_t := 0.0
var wander_dir := Vector2.ZERO
var mash_t := 0.0
var tap_hold := 0                 # ticks the finger stays down (a real press)

# ---- per-run metrics -------------------------------------------------------
var t := 0.0
var fight_t0 := -1.0              # when the showing handed over to the fight
var prev_state := ""
var prev_hits := 0
var windows_open := 0
var windows_hit := 0
var windows_missed := 0
var miss_total := 0
var miss_streak_current := 0
var miss_streak_max := 0
var taps := 0
var taps_shielded := 0            # tapped while he was not open
var taps_open_far := 0            # tapped on the flash but out of reach
var open_too_far_distances: Array[float] = []
var open_too_far_reach_deficits: Array[float] = []
var latencies: Array[float] = []  # flash-on → landing tap, per landed hit
var flash_to_first_tap: Array[float] = []
var shield_flash_to_open: Array[float] = []
var shield_tap_latency: Array[float] = []
var shield_flash_tap_latency: Array[float] = []
var reach_at_hit: Array[float] = []
var in_reach_at_open := 0         # windows where she was already close enough
var window_open_t := -1.0
var last_hit_t := 0.0
var longest_dry := 0.0
var phase_t := [0.0, 0.0, 0.0]
var state_t := {}                 # state name -> simulated seconds spent
var bumps := 0
var bump_displacements: Array[float] = []
var prev_bump_cd := 0.0
var prev_bump_count := 0
var prev_player_local := Vector2.ZERO
var assisted_taps := 0
var assisted_tap_times: Array[float] = []
var pending_player_accepts := 0
var prev_accepted_taps := 0
var assist_tier_current := 0
var assist_tier_max := 0
var assist_transitions: Array[String] = []
var effective_window_min := INF
var effective_window_max := 0.0
var effective_window_current := 0.0
var effective_reach_min := INF
var effective_reach_max := 0.0
var effective_reach_current := 0.0
var effective_windup_min := INF
var effective_windup_max := 0.0
var effective_windup_current := 0.0
var effective_speed_min := INF
var effective_speed_max := 0.0
var effective_speed_current := 0.0
var flash_open_count := 0
var flash_durations: Array[float] = []
var shield_flash_count := 0
var shield_flash_durations: Array[float] = []
var flash_open_t := -1.0
var shield_flash_t := -1.0
var last_flash_close_t := -1.0
var prev_flash_open := false
var prev_shield_flash := false
var flash_first_tap_recorded := false
var capped := false

func _init() -> void:
	Engine.time_scale = 4.0        # only affects tween/particle cleanup
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	boss = main._game_obj("dustboss", DustBossGame) as DustBossGame
	var user_args: PackedStringArray = OS.get_cmdline_user_args()
	if "--controls" in user_args:
		roster = CONTROLS
		run_count = CONTROLS.size()
		roster_label = "CONTROLS"
	for raw_arg: String in user_args:
		if raw_arg.begins_with("--control="):
			var control_index: int = clampi(
				raw_arg.trim_prefix("--control=").to_int(), 0, CONTROLS.size() - 1)
			roster = [CONTROLS[control_index]]
			run_count = 1
			roster_label = "CONTROL_%d" % control_index
	print("DUSTBAL|header runs=%d dt=%.2f band=%d-%ds rounds=%d taps_per_round=%d window_base=%.2f set=%s" % [
		run_count, DT, int(BAND_LO), int(BAND_HI), DustBossGame.HP,
		DustBossGame.TAPS_PER_ROUND, DustBunnyBossSprite.VULNERABILITY_WINDOW,
		roster_label])
	print("DUSTBAL|schema run,persona,fight_s,total_s,windows,hit,missed,miss_total,miss_streak_current,miss_streak_max,taps,shielded,open_too_far_count,open_too_far_cause,assist_tier_current,assist_tier_max,assist_tier_transitions,assisted_taps,helper_taps,window_eff_current,window_eff_min,window_eff_max,reach_eff_current,reach_eff_min,reach_eff_max,windup_eff_current,windup_eff_min,windup_eff_max,speed_eff_current,speed_eff_min,speed_eff_max,flash_open_count,flash_duration_med,flash_to_first_tap_med,flash_to_hit_med,shield_flash_count,shield_flash_duration_med,shield_flash_to_open_med,shield_tap_count,shield_tap_latency_med,open_too_far_distance_med,bump_count,bump_displacement_med,bump_displacement_max,verdict")
	var fights: Array[float] = []
	var misses: Array[int] = []
	var tap_counts: Array[int] = []
	var lat_all: Array[float] = []
	var unfinished := 0
	for run in range(run_count):
		seed(770000 + run * 31)
		persona = roster[run % roster.size()]
		await _play_one(run)
		if capped:
			unfinished += 1
		else:
			fights.append(t - fight_t0)
		misses.append(miss_total)
		tap_counts.append(taps)
		lat_all.append_array(latencies)
		_print_run(run)
		await _settle_between_runs()
	_print_summary(fights, misses, tap_counts, lat_all, unfinished)
	quit()

# ---- one encounter ---------------------------------------------------------
func _play_one(_run: int) -> void:
	_reset_run()
	main.dust_boss_cool = 0.0
	main.game = ""
	main._start_game_now(main.dust_boss_fr)
	await process_frame
	# This harness owns the clock, so stop MAIN's own _process rather than
	# renaming main.game — player.gd hands the camera to a stage BY GAME ID,
	# and a sentinel id would quietly restore the free-swim chase cam.
	main.set_process(false)
	var fr: Dictionary = main.dust_boss_fr
	while main.g.has("db_state") and t < TIME_CAP:
		_drive()
		boss.tick(DT, fr, main.player.position)
		if not main.g.has("db_state"):
			break
		_sample()
		t += DT
		await process_frame
	if t >= TIME_CAP and main.g.has("db_state"):
		capped = true
	main.touch_ui.action_down = false
	main.touch_ui.stick_vec = Vector2.ZERO
	if main.g.has("db_state"):
		main._clear_game()
	main.game = ""
	main.set_process(true)
	_close_timing_intervals()

func _reset_run() -> void:
	t = 0.0
	fight_t0 = -1.0
	prev_state = ""
	prev_hits = 0
	windows_open = 0
	windows_hit = 0
	windows_missed = 0
	miss_total = 0
	miss_streak_current = 0
	miss_streak_max = 0
	taps = 0
	taps_shielded = 0
	taps_open_far = 0
	open_too_far_distances = []
	open_too_far_reach_deficits = []
	latencies = []
	flash_to_first_tap = []
	shield_flash_to_open = []
	shield_tap_latency = []
	shield_flash_tap_latency = []
	reach_at_hit = []
	in_reach_at_open = 0
	window_open_t = -1.0
	last_hit_t = 0.0
	longest_dry = 0.0
	phase_t = [0.0, 0.0, 0.0]
	state_t = {}
	bumps = 0
	bump_displacements = []
	prev_bump_cd = 0.0
	prev_bump_count = 0
	prev_player_local = Vector2.ZERO
	assisted_taps = 0
	assisted_tap_times = []
	pending_player_accepts = 0
	prev_accepted_taps = 0
	assist_tier_current = 0
	assist_tier_max = 0
	assist_transitions = []
	effective_window_min = INF
	effective_window_max = 0.0
	effective_window_current = 0.0
	effective_reach_min = INF
	effective_reach_max = 0.0
	effective_reach_current = 0.0
	effective_windup_min = INF
	effective_windup_max = 0.0
	effective_windup_current = 0.0
	effective_speed_min = INF
	effective_speed_max = 0.0
	effective_speed_current = 0.0
	flash_open_count = 0
	flash_durations = []
	shield_flash_count = 0
	shield_flash_durations = []
	flash_open_t = -1.0
	shield_flash_t = -1.0
	last_flash_close_t = -1.0
	prev_flash_open = false
	prev_shield_flash = false
	flash_first_tap_recorded = false
	capped = false
	gawk_t = 0.0
	react_t = -1.0
	armed = false
	wander_t = 0.0
	wander_dir = Vector2.ZERO
	mash_t = 0.0
	tap_hold = 0

func _settle_between_runs() -> void:
	for i in range(6):
		await process_frame

# ---- the simulated child ---------------------------------------------------
func _drive() -> void:
	var flashing: bool = float(main.g.get("db_flash", 0.0)) >= 0.99
	var here: Vector2 = _player_local()
	var him := Vector2(float(main.g.get("db_x", 0.0)), float(main.g.get("db_z", 0.0)))
	# 1. gawking at her own sparkles: no hands on the glass at all
	if gawk_t > 0.0:
		gawk_t -= DT
		main.touch_ui.stick_vec = Vector2.ZERO
		_release()
		return
	# 2. walking. Default intent is to follow the big fluffy thing; wander
	#    fires as a whole-second detour somewhere else.
	wander_t -= DT
	if wander_t <= 0.0:
		if randf() < float(persona["wander"]) * DT * 2.0:
			wander_dir = Vector2(randf_range(-1.0, 1.0), randf_range(-1.0, 1.0)).normalized()
			wander_t = randf_range(0.6, 1.6)
		else:
			wander_dir = Vector2.ZERO
	var want: Vector2 = (him - here)
	if wander_dir != Vector2.ZERO:
		want = wander_dir * 10.0
	var mag: float = clampf(want.length() / 6.0, 0.0, 1.0) * float(persona["speed"])
	# a small hand is never steady on a virtual stick
	var jitter := Vector2(randf_range(-0.12, 0.12), randf_range(-0.12, 0.12))
	main.touch_ui.stick_vec = (want.normalized() * mag + jitter).limit_length(1.0)
	# 3. tapping. The star is the cue; the reaction is scheduled the moment
	#    she notices it, and a wrong-tap roll can throw the finger early.
	if flashing and not armed:
		armed = true
		react_t = float(persona["reaction"]) * randf_range(0.8, 1.35)
		if randf() < float(persona["err"]):
			react_t += randf_range(0.8, 2.2)   # she looked away / hesitated
	if not flashing:
		armed = false
		react_t = -1.0
	var want_tap := false
	if react_t > 0.0:
		react_t -= DT
		if react_t <= 0.0:
			want_tap = true
			# a damage round is THREE quick taps inside one 0.75s window, so a
			# child who has noticed the flash drums as fast as her hand goes.
			# 0.18s between taps is a brisk but real preschool double/triple tap.
			react_t = 0.18
	# the masher: a steady drum of taps whatever the boss is doing
	if float(persona["mash"]) > 0.0:
		mash_t -= DT
		if mash_t <= 0.0:
			mash_t = 1.0 / float(persona["mash"])
			want_tap = true
	# a stray wrong-moment tap from excitement
	if not flashing and randf() < float(persona["err"]) * DT * 0.6:
		want_tap = true
	if want_tap:
		_press()
	else:
		_release()

func _press() -> void:
	# a real finger: down for two ticks, then up, so the engine sees one edge
	if tap_hold <= 0:
		main.touch_ui.action_down = true
		tap_hold = 2
		taps += 1
		var flashing: bool = _flash_is_open()
		if flashing:
			var d: float = (Vector2(float(main.g.get("db_x", 0.0)),
				float(main.g.get("db_z", 0.0))) - _player_local()).length()
			if not flash_first_tap_recorded and flash_open_t >= 0.0:
				flash_to_first_tap.append(t - flash_open_t)
				flash_first_tap_recorded = true
			if d > _effective_reach():
				taps_open_far += 1
				open_too_far_distances.append(d)
				open_too_far_reach_deficits.append(d - _effective_reach())
			else:
				pending_player_accepts += 1
		else:
			taps_shielded += 1
			if last_flash_close_t >= 0.0:
				shield_tap_latency.append(t - last_flash_close_t)
			if _shield_flash_is_visible() and shield_flash_t >= 0.0:
				shield_flash_tap_latency.append(t - shield_flash_t)
	else:
		tap_hold -= 1
		if tap_hold <= 0:
			main.touch_ui.action_down = false

func _release() -> void:
	if tap_hold > 0:
		tap_hold -= 1
		if tap_hold <= 0:
			main.touch_ui.action_down = false
	else:
		main.touch_ui.action_down = false

func _player_local() -> Vector2:
	var r: Node3D = main.g.get("oc_root") as Node3D
	if r == null:
		return Vector2.ZERO
	return Vector2(main.player.position.x - r.position.x,
		main.player.position.z - r.position.z)

func _g_float(keys: Array[String], fallback: float) -> float:
	for key: String in keys:
		if main.g.has(key):
			var value: Variant = main.g[key]
			if typeof(value) == TYPE_FLOAT or typeof(value) == TYPE_INT:
				return float(value)
	return fallback

func _effective_assist_tier() -> int:
	if boss != null and boss.has_method("mercy_tier"):
		return maxi(0, int(boss.mercy_tier()))
	return maxi(0, int(main.g.get("db_mercy_tier", 0)))

func _effective_window() -> float:
	var fallback: float = _g_float(["db_win_len", "db_effective_window"],
		DustBunnyBossSprite.VULNERABILITY_WINDOW)
	if main.g.has("db_effective_window"):
		return maxf(0.0, fallback)
	if boss != null and boss.has_method("window_len"):
		return maxf(0.0, float(boss.window_len()))
	return maxf(0.0, fallback)

func _effective_reach() -> float:
	var fallback: float = _g_float(["db_effective_reach"], 0.0)
	if fallback > 0.0:
		return fallback
	if boss != null and boss.has_method("reach"):
		return maxf(0.0, float(boss.reach()))
	return fallback

func _effective_windup() -> float:
	var fallback: float = _g_float(["db_effective_windup"], 0.0)
	if fallback > 0.0:
		return fallback
	if boss != null and boss.has_method("windup_len"):
		return maxf(0.0, float(boss.windup_len()))
	return fallback

func _effective_speed() -> float:
	var fallback: float = _g_float(["db_effective_speed"], 0.0)
	if fallback > 0.0:
		return fallback
	if boss != null and boss.has_method("hop_speed"):
		return maxf(0.0, float(boss.hop_speed()))
	return fallback

func _flash_is_open() -> bool:
	return String(main.g.get("db_state", "")) == "vuln" \
		and float(main.g.get("db_flash", 0.0)) >= 0.99

func _shield_flash_is_visible() -> bool:
	var flash: float = float(main.g.get("db_flash", 0.0))
	return flash > 0.01 and flash < 0.99

func _gameplay_assisted_taps() -> int:
	for key: String in ["db_assisted_taps_total", "db_helper_taps_total"]:
		if main.g.has(key):
			return maxi(0, int(main.g[key]))
	return -1

# ---- metrics ---------------------------------------------------------------
func _sample() -> void:
	var st: String = String(main.g.get("db_state", ""))
	var hits: int = int(main.g.get("db_hits", 0))
	var current_miss: int = int(main.g.get("db_miss", windows_missed))
	var current_streak: int = int(main.g.get("db_miss_streak", 0))
	miss_total = maxi(miss_total, current_miss)
	miss_streak_current = maxi(0, current_streak)
	miss_streak_max = maxi(miss_streak_max, miss_streak_current)
	state_t[st] = float(state_t.get(st, 0.0)) + DT
	phase_t[clampi(hits, 0, 2)] += DT
	var tier: int = _effective_assist_tier()
	if tier != assist_tier_current:
		assist_transitions.append("%d>%d@%.2f" % [assist_tier_current, tier, t])
	assist_tier_current = tier
	assist_tier_max = maxi(assist_tier_max, tier)
	var effective_window: float = _effective_window()
	var effective_reach: float = _effective_reach()
	var effective_windup: float = _effective_windup()
	var effective_speed: float = _effective_speed()
	effective_window_current = effective_window
	effective_reach_current = effective_reach
	effective_windup_current = effective_windup
	effective_speed_current = effective_speed
	if effective_window > 0.0:
		effective_window_min = minf(effective_window_min, effective_window)
		effective_window_max = maxf(effective_window_max, effective_window)
	if effective_reach > 0.0:
		effective_reach_min = minf(effective_reach_min, effective_reach)
		effective_reach_max = maxf(effective_reach_max, effective_reach)
	if effective_windup > 0.0:
		effective_windup_min = minf(effective_windup_min, effective_windup)
		effective_windup_max = maxf(effective_windup_max, effective_windup)
	if effective_speed > 0.0:
		effective_speed_min = minf(effective_speed_min, effective_speed)
		effective_speed_max = maxf(effective_speed_max, effective_speed)
	if st == "prowl" and fight_t0 < 0.0:
		fight_t0 = t
		last_hit_t = t
	if st == "vuln" and prev_state != "vuln":
		windows_open += 1
		window_open_t = t
		var d: float = (Vector2(float(main.g["db_x"]), float(main.g["db_z"]))
			- _player_local()).length()
		if d <= boss.reach():
			in_reach_at_open += 1
	if hits > prev_hits:
		windows_hit += 1
		if window_open_t >= 0.0:
			latencies.append(t - window_open_t)
		reach_at_hit.append((Vector2(float(main.g["db_x"]), float(main.g["db_z"]))
			- _player_local()).length())
		longest_dry = maxf(longest_dry, t - last_hit_t)
		last_hit_t = t
	if prev_state == "vuln" and st != "vuln" and hits == prev_hits:
		windows_missed += 1
	miss_total = maxi(miss_total, windows_missed)
	var flash_now: bool = _flash_is_open()
	if flash_now and not prev_flash_open:
		flash_open_count += 1
		flash_open_t = t
		flash_first_tap_recorded = false
		if shield_flash_t >= 0.0:
			shield_flash_to_open.append(t - shield_flash_t)
			shield_flash_t = -1.0
	if not flash_now and prev_flash_open:
		if flash_open_t >= 0.0:
			flash_durations.append(maxf(0.0, t - flash_open_t))
		last_flash_close_t = t
		flash_open_t = -1.0
	prev_flash_open = flash_now
	var shield_flash_now: bool = _shield_flash_is_visible()
	if shield_flash_now and not prev_shield_flash:
		shield_flash_count += 1
		shield_flash_t = t
	if not shield_flash_now and prev_shield_flash:
		if shield_flash_t >= 0.0:
			shield_flash_durations.append(maxf(0.0, t - shield_flash_t))
		shield_flash_t = -1.0
	prev_shield_flash = shield_flash_now
	var kit: DustBunnyBossSprite = main.g.get("db_kit") as DustBunnyBossSprite
	var accepted_now: int = int(main.g.get(
		"db_taps_this_round", kit.accepted_taps if kit != null else 0))
	var accepted_delta: int = accepted_now - prev_accepted_taps
	if accepted_delta < 0:
		accepted_delta = accepted_now
	var player_accepts: int = mini(accepted_delta, pending_player_accepts)
	var assisted_delta: int = maxi(0, accepted_delta - player_accepts)
	assisted_taps += assisted_delta
	for _assisted in range(assisted_delta):
		assisted_tap_times.append(t)
	pending_player_accepts = maxi(0, pending_player_accepts - player_accepts)
	prev_accepted_taps = accepted_now
	var gameplay_assisted: int = _gameplay_assisted_taps()
	if gameplay_assisted >= 0:
		assisted_taps = maxi(assisted_taps, gameplay_assisted)
	if st != "vuln":
		pending_player_accepts = 0
	var bump_count_now: int = int(main.g.get("db_bumps", -1))
	var current_player_local: Vector2 = _player_local()
	if bump_count_now >= 0:
		var bump_delta: int = bump_count_now - prev_bump_count
		if bump_delta > 0:
			var displacement: float = current_player_local.distance_to(prev_player_local)
			for _bump in range(bump_delta):
				bump_displacements.append(displacement)
		bumps = maxi(bumps, bump_count_now)
		prev_bump_count = bump_count_now
	else:
		var bump_cd: float = float(main.g.get("db_bump_cd", 0.0))
		if bump_cd > prev_bump_cd + 0.5:
			bumps += 1
			bump_displacements.append(current_player_local.distance_to(prev_player_local))
		prev_bump_cd = bump_cd
	prev_player_local = current_player_local
	prev_state = st
	prev_hits = hits

func _close_timing_intervals() -> void:
	if prev_flash_open and flash_open_t >= 0.0:
		flash_durations.append(maxf(0.0, t - flash_open_t))
		flash_open_t = -1.0
	if prev_shield_flash and shield_flash_t >= 0.0:
		shield_flash_durations.append(maxf(0.0, t - shield_flash_t))
		shield_flash_t = -1.0

func _median(values: Array) -> float:
	if values.is_empty():
		return 0.0
	var copy: Array = values.duplicate()
	copy.sort()
	return float(copy[copy.size() / 2])

func _finite_metric(value: float) -> float:
	return 0.0 if value >= INF * 0.5 else value

func _max_metric(values: Array[float]) -> float:
	var result := 0.0
	for value: float in values:
		result = maxf(result, value)
	return result

func _transition_text() -> String:
	return "none" if assist_transitions.is_empty() else ",".join(assist_transitions)

func _print_run(run: int) -> void:
	var fight: float = (t - fight_t0) if fight_t0 >= 0.0 else t
	var verdict := "in-band"
	if capped:
		verdict = "capped"
	elif fight < BAND_LO:
		verdict = "quick"
	elif fight > BAND_HI:
		verdict = "long"
	print("DUSTBAL|run=%02d persona=%s fight=%.1f total=%.1f windows=%d hit=%d missed=%d miss_total=%d miss_streak_current=%d miss_streak_max=%d taps=%d shielded=%d openfar=%d open_too_far_count=%d open_too_far_cause=distance_gt_effective_reach assist_tier_current=%d assist_tier_max=%d assist_tier_transitions=%s assisted_taps=%d helper_taps=%d window_eff_current=%.2f window_eff_min=%.2f window_eff_max=%.2f reach_eff_current=%.2f reach_eff_min=%.2f reach_eff_max=%.2f windup_eff_current=%.2f windup_eff_min=%.2f windup_eff_max=%.2f speed_eff_current=%.2f speed_eff_min=%.2f speed_eff_max=%.2f flash_open_count=%d flash_duration_med=%.2f flash_to_first_tap_med=%.2f flash_to_hit_med=%.2f shield_flash_count=%d shield_flash_duration_med=%.2f shield_flash_to_open_med=%.2f shield_tap_count=%d shield_tap_latency_med=%.2f open_too_far_distance_med=%.2f bump_count=%d bump_displacement_med=%.2f bump_displacement_max=%.2f %s" % [
		run, String(persona["name"]), fight, t, windows_open, windows_hit,
		windows_missed, miss_total, miss_streak_current, miss_streak_max, taps,
		taps_shielded, taps_open_far, taps_open_far, assist_tier_current,
		assist_tier_max, _transition_text(), assisted_taps, assisted_taps,
		effective_window_current, _finite_metric(effective_window_min), effective_window_max,
		effective_reach_current, _finite_metric(effective_reach_min), effective_reach_max,
		effective_windup_current, _finite_metric(effective_windup_min), effective_windup_max,
		effective_speed_current, _finite_metric(effective_speed_min), effective_speed_max,
		flash_open_count, _median(flash_durations), _median(flash_to_first_tap),
		_median(latencies), shield_flash_count, _median(shield_flash_durations),
		_median(shield_flash_to_open), taps_shielded, _median(shield_tap_latency),
		_median(open_too_far_distances), bumps, _median(bump_displacements),
		_max_metric(bump_displacements), verdict])
	print("DUSTBAL|run=%02d phases puffy=%.1f dizzy=%.1f angry=%.1f states showing=%.1f prowl=%.1f windup=%.1f vuln=%.1f struck=%.1f" % [
		run, phase_t[0], phase_t[1], phase_t[2],
		float(state_t.get("showing", 0.0)), float(state_t.get("prowl", 0.0)),
		float(state_t.get("windup", 0.0)), float(state_t.get("vuln", 0.0)),
		float(state_t.get("struck", 0.0))])

func _print_summary(fights: Array[float], misses: Array[int], tap_counts: Array[int],
		lat_all: Array[float], unfinished: int) -> void:
	fights.sort()
	var lo: float = fights[0] if not fights.is_empty() else 0.0
	var hi: float = fights[fights.size() - 1] if not fights.is_empty() else 0.0
	var total_taps := 0
	for c in tap_counts:
		total_taps += c
	var total_miss := 0
	for mv in misses:
		total_miss += mv
	print("DUSTBAL|summary runs=%d finished=%d capped=%d fight_med=%.1f fight_min=%.1f fight_max=%.1f miss_total_avg=%.2f miss_avg=%.2f taps_avg=%.1f lat_med=%.2f" % [
		run_count, run_count - unfinished, unfinished, _median(fights), lo, hi,
		float(total_miss) / float(run_count), float(total_miss) / float(run_count),
		float(total_taps) / float(run_count),
		_median(lat_all)])
	var in_band := 0
	for f in fights:
		if f >= BAND_LO and f <= BAND_HI:
			in_band += 1
	print("DUSTBAL|verdict in_band=%d/%d band=%d-%ds" % [in_band, run_count, int(BAND_LO), int(BAND_HI)])
