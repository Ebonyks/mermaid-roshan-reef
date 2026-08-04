extends SceneTree
# ADVISORY arena stress test for the Dust Bunny Boss — TWENTY-FOUR encounters,
# measuring the two things the balance harness cannot see:
#
#   PACING   where the seconds actually go, and where the fight goes quiet.
#            Not "is it winnable" (probe_dust_boss_balance.gd answers that) but
#            "is anything happening" — dead air, window cadence, the share of
#            the fight spent watching a bunny hop with nothing to read.
#
#   STAGING  what the arena and the art are doing with those seconds, measured
#            through the REAL camera at the phone's 1280x720 canvas: how much of
#            the ring is ever used, how big the boss and his tell actually are
#            in pixels when she must read them, whether the tell clears the safe
#            area, whether the boss's silhouette lands on a same-coloured dust
#            prop at the exact moment it must be legible, and how much of the
#            frame is bare floor.
#
# Twenty-four encounters = six child archetypes x four seeds, so every archetype
# meets four different hop patterns and four different mercy ramps.
#
# ADVISORY: prints metrics and observations, never the gate's failure tokens.
# Run: godot --headless -s scripts/probe_dust_boss_arena.gd

const DT := 0.05
const TIME_CAP := 300.0
const CANVAS := Vector2(1280.0, 720.0)
const SAFE := 0.06                 # the 6% safe area the stage frames against
const GRID := 8                    # ring-occupancy grid (GRID x GRID over the ring)
const DEAD_AIR_QUIET := 0.001      # movement below this reads as "nothing moved"

# Six archetypes, four seeds each. Fields match probe_dust_boss_balance.gd so
# the two harnesses describe the same children.
const ARCHETYPES: Array[Dictionary] = [
	{"name": "speedy", "reaction": 0.60, "err": 0.06, "speed": 0.90, "wander": 0.05, "gawk": 0.5, "mash": 0.1},
	{"name": "casual", "reaction": 1.15, "err": 0.16, "speed": 0.70, "wander": 0.16, "gawk": 1.3, "mash": 0.08},
	{"name": "wander", "reaction": 1.70, "err": 0.12, "speed": 0.52, "wander": 0.58, "gawk": 1.9, "mash": 0.03},
	{"name": "masher", "reaction": 0.85, "err": 0.38, "speed": 0.74, "wander": 0.11, "gawk": 0.6, "mash": 1.60},
	{"name": "timid ", "reaction": 2.40, "err": 0.11, "speed": 0.42, "wander": 0.28, "gawk": 2.8, "mash": 0.0},
	{"name": "stroll", "reaction": 1.30, "err": 0.10, "speed": 0.30, "wander": 0.70, "gawk": 2.2, "mash": 0.0},
]
const SEEDS: Array[int] = [11, 202, 3703, 40904]

var main: ReefMain
var boss: DustBossGame
var persona: Dictionary = {}

# child sim
var gawk_t := 0.0
var react_t := -1.0
var armed := false
var wander_t := 0.0
var wander_dir := Vector2.ZERO
var mash_t := 0.0
var tap_hold := 0

# per-encounter
var t := 0.0
var fight_t0 := -1.0
var prev_state := ""
var prev_hits := 0
var capped := false
var windows := 0
var windows_hit := 0
var window_gaps: Array[float] = []
var last_window_t := -1.0
var state_t := {}
var phase_t := [0.0, 0.0, 0.0]
var dead_air := 0.0
var dead_air_max := 0.0
var prev_boss := Vector2.ZERO
var prev_player := Vector2.ZERO
var boss_cells := {}
var player_cells := {}
var boss_r_max := 0.0
var player_r_max := 0.0
var boss_near_wall := 0.0
var props: Array[Dictionary] = []
# staging samples, taken at the instant each window opens
var boss_px: Array[float] = []
var tell_px: Array[float] = []
var tell_margin_ok := 0
var pair_px: Array[float] = []
var prop_clash := 0
var clash_by_kind := {}
var card_overhang := 0
var boss_frame_share: Array[float] = []
var offscreen := 0

func _init() -> void:
	Engine.time_scale = 4.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	boss = main._game_obj("dustboss", DustBossGame) as DustBossGame
	print("DUSTARENA|header encounters=%d dt=%.2f canvas=%dx%d real_vp=%s ring_r=%.1f boss_h=%.1f rounds=%d taps=%d" % [
		ARCHETYPES.size() * SEEDS.size(), DT, int(CANVAS.x), int(CANVAS.y),
		str(get_root().get_visible_rect().size), DustBossGame.RADIUS, DustBossGame.BOSS_H, DustBossGame.HP,
		DustBossGame.TAPS_PER_ROUND])
	print("DUSTARENA|schema enc,persona,seed,fight_s,windows,hit,gap_med,deadair_max,ringuse_boss%,ringuse_child%,boss_px,tell_px_y,pair_px,frame%,clash,verdict")
	var all_fight: Array[float] = []
	var all_dead: Array[float] = []
	var all_gap: Array[float] = []
	var all_boss_px: Array[float] = []
	var all_pair_px: Array[float] = []
	var all_frame: Array[float] = []
	var all_ring_boss: Array[float] = []
	var all_ring_child: Array[float] = []
	var total_windows := 0
	var total_clash := 0
	var total_margin_ok := 0
	var total_offscreen := 0
	var total_overhang := 0
	var clash_kinds := {}
	var capped_n := 0
	var enc := 0
	for archetype: Dictionary in ARCHETYPES:
		for sd: int in SEEDS:
			seed(sd)
			persona = archetype
			await _play_one()
			var fight: float = (t - fight_t0) if fight_t0 >= 0.0 else t
			var ring_boss: float = 100.0 * float(boss_cells.size()) / float(_ring_cells())
			var ring_child: float = 100.0 * float(player_cells.size()) / float(_ring_cells())
			if capped:
				capped_n += 1
			else:
				all_fight.append(fight)
			all_dead.append(dead_air_max)
			all_gap.append_array(window_gaps)
			all_boss_px.append_array(boss_px)
			all_pair_px.append_array(pair_px)
			all_frame.append_array(boss_frame_share)
			all_ring_boss.append(ring_boss)
			all_ring_child.append(ring_child)
			total_windows += windows
			total_clash += prop_clash
			total_margin_ok += tell_margin_ok
			total_offscreen += offscreen
			total_overhang += card_overhang
			for k: String in clash_by_kind:
				clash_kinds[k] = int(clash_kinds.get(k, 0)) + int(clash_by_kind[k])
			_print_encounter(enc, sd, fight, ring_boss, ring_child)
			enc += 1
			await _settle()
	_print_summary(all_fight, all_dead, all_gap, all_boss_px, all_pair_px,
		all_frame, all_ring_boss, all_ring_child, total_windows, total_clash,
		total_margin_ok, total_offscreen, total_overhang, clash_kinds, capped_n)
	quit()

# ---- one encounter ---------------------------------------------------------
func _play_one() -> void:
	_reset()
	main.dust_boss_cool = 0.0
	main.game = ""
	main._start_game_now(main.dust_boss_fr)
	await process_frame
	main.set_process(false)     # this harness owns the clock; do NOT rename main.game
	_collect_props()
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

func _reset() -> void:
	t = 0.0
	fight_t0 = -1.0
	prev_state = ""
	prev_hits = 0
	capped = false
	windows = 0
	windows_hit = 0
	window_gaps = []
	last_window_t = -1.0
	state_t = {}
	phase_t = [0.0, 0.0, 0.0]
	dead_air = 0.0
	dead_air_max = 0.0
	prev_boss = Vector2.ZERO
	prev_player = Vector2.ZERO
	boss_cells = {}
	player_cells = {}
	boss_r_max = 0.0
	player_r_max = 0.0
	boss_near_wall = 0.0
	props = []
	boss_px = []
	tell_px = []
	tell_margin_ok = 0
	pair_px = []
	prop_clash = 0
	clash_by_kind = {}
	card_overhang = 0
	boss_frame_share = []
	offscreen = 0
	gawk_t = 0.0
	react_t = -1.0
	armed = false
	wander_t = 0.0
	wander_dir = Vector2.ZERO
	mash_t = 0.0
	tap_hold = 0

func _settle() -> void:
	for _i in range(6):
		await process_frame

# every solid the arena dresses the ring with, so a silhouette clash is
# measured against the real scenery instead of assumed
func _collect_props() -> void:
	var r: Node3D = main.g.get("oc_root") as Node3D
	if r == null:
		return
	var apo: float = OctagonStage.apothem(DustBossGame.RADIUS)
	for child: Node in r.get_children():
		if not (child is MeshInstance3D):
			continue
		var mi := child as MeshInstance3D
		var here := Vector2(mi.position.x, mi.position.z)
		if here.length() > apo + 0.5:
			continue                        # a wall or a post, not floor dressing
		var aabb: AABB = mi.get_aabb()
		var span: float = maxf(aabb.size.x, aabb.size.z) * 0.5
		if span < 1.5 or aabb.size.y < 1.5:
			continue                        # the deck and the duelling ring
		var kind := "crate"
		if mi.mesh is SphereMesh:
			kind = "nest" if here.length() > 8.0 and span > 5.0 else "mound"
		props.append({"xz": here, "r": span, "h": aabb.size.y, "kind": kind})

# ---- the simulated child ---------------------------------------------------
func _drive() -> void:
	var flashing: bool = float(main.g.get("db_flash", 0.0)) >= 0.99
	var here: Vector2 = _player_local()
	var him := Vector2(float(main.g.get("db_x", 0.0)), float(main.g.get("db_z", 0.0)))
	if gawk_t > 0.0:
		gawk_t -= DT
		main.touch_ui.stick_vec = Vector2.ZERO
		_release()
		return
	wander_t -= DT
	if wander_t <= 0.0:
		if randf() < float(persona["wander"]) * DT * 2.0:
			wander_dir = Vector2(randf_range(-1.0, 1.0), randf_range(-1.0, 1.0)).normalized()
			wander_t = randf_range(0.6, 1.6)
		else:
			wander_dir = Vector2.ZERO
	var want: Vector2 = him - here
	if wander_dir != Vector2.ZERO:
		want = wander_dir * 10.0
	var mag: float = clampf(want.length() / 6.0, 0.0, 1.0) * float(persona["speed"])
	var jitter := Vector2(randf_range(-0.12, 0.12), randf_range(-0.12, 0.12))
	main.touch_ui.stick_vec = (want.normalized() * mag + jitter).limit_length(1.0)
	if flashing and not armed:
		armed = true
		react_t = float(persona["reaction"]) * randf_range(0.8, 1.35)
		if randf() < float(persona["err"]):
			react_t += randf_range(0.8, 2.2)
	if not flashing:
		armed = false
		react_t = -1.0
	var want_tap := false
	if react_t > 0.0:
		react_t -= DT
		if react_t <= 0.0:
			want_tap = true
			react_t = 0.18
	if float(persona["mash"]) > 0.0:
		mash_t -= DT
		if mash_t <= 0.0:
			mash_t = 1.0 / float(persona["mash"])
			want_tap = true
	if not flashing and randf() < float(persona["err"]) * DT * 0.6:
		want_tap = true
	if want_tap:
		_press()
	else:
		_release()

func _press() -> void:
	if tap_hold <= 0:
		main.touch_ui.action_down = true
		tap_hold = 2
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

# ---- measurement ------------------------------------------------------------
func _ring_cells() -> int:
	# how many of the GRID x GRID cells over the ring's bounding square actually
	# lie inside the octagon — the honest denominator for "how much got used"
	var apo: float = OctagonStage.apothem(DustBossGame.RADIUS)
	var count := 0
	for iy in range(GRID):
		for ix in range(GRID):
			var p := Vector2(
				-apo + (float(ix) + 0.5) * (2.0 * apo / float(GRID)),
				-apo + (float(iy) + 0.5) * (2.0 * apo / float(GRID)))
			if boss.stage.clamp_point(p, 0.0).distance_to(p) < 0.01:
				count += 1
	return maxi(1, count)

func _cell(p: Vector2) -> int:
	var apo: float = OctagonStage.apothem(DustBossGame.RADIUS)
	var ix: int = clampi(int((p.x + apo) / (2.0 * apo) * float(GRID)), 0, GRID - 1)
	var iy: int = clampi(int((p.y + apo) / (2.0 * apo) * float(GRID)), 0, GRID - 1)
	return iy * GRID + ix

func _sample() -> void:
	var st: String = String(main.g.get("db_state", ""))
	var hits: int = int(main.g.get("db_hits", 0))
	state_t[st] = float(state_t.get(st, 0.0)) + DT
	phase_t[clampi(hits, 0, 2)] += DT
	if st == "prowl" and fight_t0 < 0.0:
		fight_t0 = t
	var him := Vector2(float(main.g.get("db_x", 0.0)), float(main.g.get("db_z", 0.0)))
	var her: Vector2 = _player_local()
	boss_cells[_cell(him)] = true
	player_cells[_cell(her)] = true
	boss_r_max = maxf(boss_r_max, him.length())
	player_r_max = maxf(player_r_max, her.length())
	if him.length() > OctagonStage.apothem(DustBossGame.RADIUS) - 8.0:
		boss_near_wall += DT
	# DEAD AIR: the fight is on, nothing is flashing, nobody has just been hit,
	# and neither body moved a measurable amount. This is the metric the balance
	# harness has no way to see — a fight can be perfectly winnable and still be
	# a child watching a still picture.
	var moved: float = him.distance_to(prev_boss) + her.distance_to(prev_player)
	var live: bool = st == "prowl" or st == "windup"
	if live and moved < DEAD_AIR_QUIET and float(main.g.get("db_flash", 0.0)) < 0.99:
		dead_air += DT
		dead_air_max = maxf(dead_air_max, dead_air)
	else:
		dead_air = 0.0
	prev_boss = him
	prev_player = her
	if st == "vuln" and prev_state != "vuln":
		windows += 1
		if last_window_t >= 0.0:
			window_gaps.append(t - last_window_t)
		last_window_t = t
		_stage_sample(him, her)
	if hits > prev_hits:
		windows_hit += 1
	prev_state = st
	prev_hits = hits

# THE STAGING SAMPLE — taken at the exact instant the child is asked to read
# something, against the PHONE'S canvas.
#
# No harness gives a 1280x720 root viewport (headless reports 1280x1280, xvfb
# 1280x1024), and OctagonStage.fit_camera() solves its framing from whatever
# viewport it finds — so a probe that trusts Camera3D.unproject_position is
# measuring a camera the phone will never have. This file therefore re-solves
# the shipped framing algorithm against 1280x720 and projects by hand, so every
# pixel number below is the number the child's phone produces.
func _phone_camera() -> Dictionary:
	var r: Node3D = main.g.get("oc_root") as Node3D
	var cfg: Dictionary = main.g.get("oc_cfg", {})
	var radius: float = float(cfg.get("radius", DustBossGame.RADIUS))
	var head: float = float(cfg.get("headroom", radius * 0.8))
	var apo: float = OctagonStage.apothem(radius)
	var stand: float = float(cfg.get("hover", 1.05)) + 1.5
	var fov: float = float(cfg.get("cam_fov", 55.0))
	var margin: float = CANVAS.y * SAFE
	var dist: float = radius * 1.55
	var high: float = radius * 1.15
	var pos := Vector3.ZERO
	var look := Vector3.ZERO
	for _step in range(26):
		pos = r.position + Vector3(0.0, high, dist)
		look = r.position + Vector3(0.0, head * 0.42, 0.0)
		var near_p: Vector2 = _project(pos, look, fov, r.position + Vector3(0.0, stand, apo))
		var far_p: Vector2 = _project(pos, look, fov, r.position + Vector3(0.0, stand, -apo))
		var top_p: Vector2 = _project(pos, look, fov, r.position + Vector3(0.0, head, 0.0))
		if near_p.y <= CANVAS.y - margin and top_p.y >= margin and far_p.y >= margin:
			break
		dist *= 1.07
		high *= 1.05
	return {"pos": pos, "look": look, "fov": fov}

func _project(pos: Vector3, look: Vector3, fov: float, point: Vector3) -> Vector2:
	var fwd: Vector3 = (look - pos).normalized()
	var right: Vector3 = fwd.cross(Vector3.UP).normalized()
	var up: Vector3 = right.cross(fwd)
	var d: Vector3 = point - pos
	var z: float = d.dot(fwd)
	if z <= 0.001:
		return Vector2(-99999.0, -99999.0)      # behind the lens
	var half_h: float = tan(deg_to_rad(fov) * 0.5)
	var aspect: float = CANVAS.x / CANVAS.y
	var nx: float = (d.dot(right) / z) / (half_h * aspect)
	var ny: float = (d.dot(up) / z) / half_h
	return Vector2((nx * 0.5 + 0.5) * CANVAS.x, (0.5 - ny * 0.5) * CANVAS.y)

func _stage_sample(him: Vector2, her: Vector2) -> void:
	var r: Node3D = main.g.get("oc_root") as Node3D
	if r == null:
		return
	var cam: Dictionary = _phone_camera()
	var cpos: Vector3 = cam["pos"]
	var clook: Vector3 = cam["look"]
	var fov: float = cam["fov"]
	var foot: Vector3 = r.position + Vector3(him.x, float(main.g.get("db_y", 0.0)), him.y)
	var head: Vector3 = foot + Vector3(0, DustBossGame.BOSS_H, 0)
	var tell: Vector3 = foot + Vector3(0, DustBossGame.BOSS_H + 1.5, 0)
	var foot_p: Vector2 = _project(cpos, clook, fov, foot)
	var head_p: Vector2 = _project(cpos, clook, fov, head)
	var tell_p: Vector2 = _project(cpos, clook, fov, tell)
	var her_p: Vector2 = _project(cpos, clook, fov, r.position + Vector3(her.x, 1.5, her.y))
	if foot_p.x < -9000.0 or tell_p.x < -9000.0:
		offscreen += 1
		return
	var h_px: float = absf(foot_p.y - head_p.y)
	boss_px.append(h_px)
	tell_px.append(tell_p.y)
	if tell_p.y >= CANVAS.y * SAFE and tell_p.x >= CANVAS.x * SAFE \
			and tell_p.x <= CANVAS.x * (1.0 - SAFE):
		tell_margin_ok += 1
	# The authored frames carry dust plumes and padding, so the BUNNY reads at
	# roughly the middle 60% of the card (dust_boss.gd BOSS_H comment). Judge
	# cropping on that body, not on the transparent card edge — and count the
	# card overhang separately so the two are never confused.
	var body_lo: Vector2 = _project(cpos, clook, fov,
		foot + Vector3(0, DustBossGame.BOSS_H * 0.20, 0))
	var body_hi: Vector2 = _project(cpos, clook, fov,
		foot + Vector3(0, DustBossGame.BOSS_H * 0.80, 0))
	if body_lo.y > CANVAS.y or body_hi.y < 0.0 \
			or foot_p.x < 0.0 or foot_p.x > CANVAS.x:
		offscreen += 1
	if foot_p.y > CANVAS.y:
		card_overhang += 1
	pair_px.append(foot_p.distance_to(her_p))
	boss_frame_share.append(100.0 * (h_px * h_px * 0.62) / (CANVAS.x * CANVAS.y))
	# SILHOUETTE CLASH: at the instant the tell must be read, is he standing in
	# front of a dust mound, a pearl crate or his own nest — soft pastel blobs in
	# the same family of shapes and values as the boss card itself?
	var cam_xz := Vector2(cpos.x - r.position.x, cpos.z - r.position.z)
	for prop: Dictionary in props:
		var p: Vector2 = prop["xz"]
		if float(prop["r"]) <= 2.5:
			continue
		if (p - cam_xz).length() <= (him - cam_xz).length():
			continue                       # in front of him, not behind him
		var p_p: Vector2 = _project(cpos, clook, fov,
			r.position + Vector3(p.x, float(prop["h"]) * 0.5, p.y))
		if p_p.x < -9000.0:
			continue
		if absf(p_p.x - foot_p.x) < h_px * 0.45 \
				and absf(p_p.y - (foot_p.y - h_px * 0.5)) < h_px * 0.75:
			prop_clash += 1
			var kind: String = String(prop.get("kind", "prop"))
			clash_by_kind[kind] = int(clash_by_kind.get(kind, 0)) + 1
			break

func _median(values: Array) -> float:
	if values.is_empty():
		return 0.0
	var copy: Array = values.duplicate()
	copy.sort()
	return float(copy[copy.size() / 2])

func _print_encounter(enc: int, sd: int, fight: float, ring_boss: float,
		ring_child: float) -> void:
	var verdict := "in-band"
	if capped:
		verdict = "capped"
	elif fight < 45.0:
		verdict = "quick"
	elif fight > 120.0:
		verdict = "long"
	print("DUSTARENA|enc=%02d persona=%s seed=%05d fight=%.1f windows=%d hit=%d gap=%.1f deadair=%.2f ring_boss=%.0f%% ring_child=%.0f%% boss_px=%.0f tell_y=%.0f pair_px=%.0f frame=%.1f%% clash=%d %s" % [
		enc, String(persona["name"]), sd, fight, windows, windows_hit,
		_median(window_gaps), dead_air_max, ring_boss, ring_child,
		_median(boss_px), _median(tell_px), _median(pair_px),
		_median(boss_frame_share), prop_clash, verdict])
	print("DUSTARENA|enc=%02d states showing=%.1f prowl=%.1f windup=%.1f vuln=%.1f struck=%.1f friends=%.1f | phases puffy=%.1f dizzy=%.1f angry=%.1f | wall_time=%.1f boss_rmax=%.1f child_rmax=%.1f" % [
		enc, float(state_t.get("showing", 0.0)), float(state_t.get("prowl", 0.0)),
		float(state_t.get("windup", 0.0)), float(state_t.get("vuln", 0.0)),
		float(state_t.get("struck", 0.0)), float(state_t.get("friends", 0.0)),
		phase_t[0], phase_t[1], phase_t[2], boss_near_wall, boss_r_max,
		player_r_max])

func _print_summary(fights: Array, dead: Array, gaps: Array, bpx: Array,
		ppx: Array, frame: Array, ring_b: Array, ring_c: Array, total_windows: int,
		clash: int, margin_ok: int, off: int, overhang: int, kinds: Dictionary,
		capped_n: int) -> void:
	fights.sort()
	print("DUSTARENA|pacing fights=%d capped=%d fight_med=%.1f fight_min=%.1f fight_max=%.1f window_gap_med=%.1f deadair_med=%.2f deadair_max=%.2f" % [
		fights.size(), capped_n, _median(fights),
		float(fights[0]) if not fights.is_empty() else 0.0,
		float(fights[fights.size() - 1]) if not fights.is_empty() else 0.0,
		_median(gaps), _median(dead), _max(dead)])
	print("DUSTARENA|ring boss_use_med=%.0f%% child_use_med=%.0f%% (of %d reachable cells)" % [
		_median(ring_b), _median(ring_c), _ring_cells()])
	print("DUSTARENA|screen boss_h_px_med=%.0f (%.0f%% of canvas height) frame_share_med=%.1f%% pair_px_med=%.0f tell_in_safe=%d/%d offscreen=%d" % [
		_median(bpx), 100.0 * _median(bpx) / CANVAS.y, _median(frame),
		_median(ppx), margin_ok, total_windows, off])
	var kind_bits: Array[String] = []
	for k: String in kinds:
		kind_bits.append("%s=%d" % [k, int(kinds[k])])
	kind_bits.sort()
	print("DUSTARENA|scenery prop_silhouette_clashes=%d of %d windows (%.0f%%) by_prop[%s] card_bottom_below_frame=%d" % [
		clash, total_windows,
		100.0 * float(clash) / maxf(1.0, float(total_windows)),
		", ".join(kind_bits), overhang])
	print("DUSTARENA|done encounters=%d" % [ARCHETYPES.size() * SEEDS.size()])

func _max(values: Array) -> float:
	var top := 0.0
	for v in values:
		top = maxf(top, float(v))
	return top
