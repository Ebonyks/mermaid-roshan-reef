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
var taps := 0
var taps_shielded := 0            # tapped while he was not open
var taps_open_far := 0            # tapped on the flash but out of reach
var latencies: Array[float] = []  # flash-on → landing tap, per landed hit
var reach_at_hit: Array[float] = []
var in_reach_at_open := 0         # windows where she was already close enough
var window_open_t := -1.0
var last_hit_t := 0.0
var longest_dry := 0.0
var phase_t := [0.0, 0.0, 0.0]
var state_t := {}                 # state name -> simulated seconds spent
var bumps := 0
var prev_bump_cd := 0.0
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
	if "--controls" in OS.get_cmdline_user_args():
		roster = CONTROLS
		run_count = CONTROLS.size()
	print("DUSTBAL|header runs=%d dt=%.2f band=%d-%ds rounds=%d taps_per_round=%d window_base=%.2f set=%s" % [
		run_count, DT, int(BAND_LO), int(BAND_HI), DustBossGame.HP,
		DustBossGame.TAPS_PER_ROUND, DustBunnyBossSprite.VULNERABILITY_WINDOW,
		"controls" if roster == CONTROLS else "personas"])
	print("DUSTBAL|schema run,persona,fight_s,total_s,windows,hit,missed,taps,shielded,openfar,mercy,lat_med,dry_max,inreach_open,bumps,verdict")
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
		misses.append(windows_missed)
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

func _reset_run() -> void:
	t = 0.0
	fight_t0 = -1.0
	prev_state = ""
	prev_hits = 0
	windows_open = 0
	windows_hit = 0
	windows_missed = 0
	taps = 0
	taps_shielded = 0
	taps_open_far = 0
	latencies = []
	reach_at_hit = []
	in_reach_at_open = 0
	window_open_t = -1.0
	last_hit_t = 0.0
	longest_dry = 0.0
	phase_t = [0.0, 0.0, 0.0]
	state_t = {}
	bumps = 0
	prev_bump_cd = 0.0
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
		if float(main.g.get("db_flash", 0.0)) >= 0.99:
			var d: float = (Vector2(float(main.g.get("db_x", 0.0)),
				float(main.g.get("db_z", 0.0))) - _player_local()).length()
			if d > boss.reach():
				taps_open_far += 1
		else:
			taps_shielded += 1
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

# ---- metrics ---------------------------------------------------------------
func _sample() -> void:
	var st: String = String(main.g.get("db_state", ""))
	var hits: int = int(main.g.get("db_hits", 0))
	state_t[st] = float(state_t.get(st, 0.0)) + DT
	phase_t[clampi(hits, 0, 2)] += DT
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
	var bump_cd: float = float(main.g.get("db_bump_cd", 0.0))
	if bump_cd > prev_bump_cd + 0.5:
		bumps += 1
	prev_bump_cd = bump_cd
	prev_state = st
	prev_hits = hits

func _median(values: Array) -> float:
	if values.is_empty():
		return 0.0
	var copy: Array = values.duplicate()
	copy.sort()
	return float(copy[copy.size() / 2])

func _print_run(run: int) -> void:
	var fight: float = (t - fight_t0) if fight_t0 >= 0.0 else t
	var verdict := "in-band"
	if capped:
		verdict = "capped"
	elif fight < BAND_LO:
		verdict = "quick"
	elif fight > BAND_HI:
		verdict = "long"
	print("DUSTBAL|run=%02d persona=%s fight=%.1f total=%.1f windows=%d hit=%d missed=%d taps=%d shielded=%d openfar=%d mercy=%d lat=%.2f dry=%.1f inreach=%d/%d bumps=%d %s" % [
		run, String(persona["name"]), fight, t, windows_open, windows_hit,
		windows_missed, taps, taps_shielded, taps_open_far,
		int(main.g.get("db_miss", windows_missed)) if main.g.has("db_miss") else windows_missed,
		_median(latencies), longest_dry, in_reach_at_open, windows_open, bumps, verdict])
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
	print("DUSTBAL|summary runs=%d finished=%d capped=%d fight_med=%.1f fight_min=%.1f fight_max=%.1f miss_avg=%.2f taps_avg=%.1f lat_med=%.2f" % [
		run_count, run_count - unfinished, unfinished, _median(fights), lo, hi,
		float(total_miss) / float(run_count), float(total_taps) / float(run_count),
		_median(lat_all)])
	var in_band := 0
	for f in fights:
		if f >= BAND_LO and f <= BAND_HI:
			in_band += 1
	print("DUSTBAL|verdict in_band=%d/%d band=%d-%ds" % [in_band, run_count, int(BAND_LO), int(BAND_HI)])
