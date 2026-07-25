extends SceneTree
# NAVIGATION_AUDIT_2026-07-25 regression probe.
#
# Everything here is driven through touch_ui.stick_vec — the child's actual
# control — instead of writing player.vel or player.position. That was the gap
# the audit found: not one probe in the suite exercised the input layer, so
# steering, turn rate, drag and the whole tank-vs-direction question were
# untested, and nothing anywhere asserted how big Roshan is on screen.
#
# Covers:
#   N1  stick is a DIRECTION, not a yaw rate (lateral input must translate)
#   C1  on-screen subject size stays in a sane band indoors and out
#   C2  she is never blinked out of frame by a collapsed boom
#   C3  the outdoor lens comes back at its boot height after a castle visit
#   C4  the zone table never resolves floor above ceiling
#   S1  the royal stairs land on a standable dais and win the Crown Star
#       with no position-writing magnet
#   S2  the hall's entrance facade is solid outside the doorway
# Prints OK/FAIL lines (ci.sh convention).

var main: ReefMain
var fails := 0

# Fraction of the viewport HEIGHT Roshan may occupy, measured by projection
# (see _watch). The defect this guards is the interior lens filling the screen
# with her back; the band is deliberately wide because the diorama look varies
# with speed and the boom-over lift.
const FRAME_MIN := 0.10
const FRAME_MAX := 0.75


func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		fails += 1
	print("NAV|%s: %s%s" % [label, "OK" if ok else "FAIL", (" (" + detail + ")") if detail != "" else ""])


func _frames(n: int) -> void:
	for i in range(n):
		await process_frame


# ---- framing / visibility watch -------------------------------------------

var worst_boom := 1e9
var worst_frac := 0.0
var best_frac := 1e9
var hidden_frames := 0


func _reset_watch() -> void:
	worst_boom = 1e9
	worst_frac = 0.0
	best_frac = 1e9
	hidden_frames = 0


func _watch() -> void:
	var p: Node3D = main.player
	var cam: Camera3D = p.cam
	if cam == null or not cam.is_inside_tree():
		return
	var focus: Vector3 = p.position + Vector3(0, 1.5, 0)
	var d: float = cam.position.distance_to(focus)
	worst_boom = minf(worst_boom, d)
	# Subject size by PROJECTION, not by trigonometry on cam.fov. Doing the
	# arithmetic by hand means guessing Godot's fov/keep_aspect convention and
	# the model's real extents; unproject_position answers with the pixels the
	# child actually sees. Roshan's v3/v4 GLB spans about -2.6..+4.4 in
	# player-local y (1.9u mesh at scale 3.7, child offset +0.89).
	var head: Vector2 = cam.unproject_position(p.position + Vector3(0, 4.4, 0))
	var feet: Vector2 = cam.unproject_position(p.position + Vector3(0, -2.6, 0))
	var view_h: float = float(get_root().get_visible_rect().size.y)
	if view_h > 1.0 and d > 0.01:
		var frac: float = absf(head.y - feet.y) / view_h
		worst_frac = maxf(worst_frac, frac)
		best_frac = minf(best_frac, frac)
	if not p.visible:
		hidden_frames += 1


# drive the virtual stick for `secs` of wall clock, watching the lens each frame
func _stick(v: Vector2, secs: float) -> void:
	var t0: int = Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < int(secs * 1000.0):
		main.touch_ui.stick_vec = v
		await process_frame
		_watch()
	main.touch_ui.stick_vec = Vector2.ZERO


func _cam_basis() -> Array:
	# [forward, right] on the xz plane, in the frame the stick is read in
	var p: Node3D = main.player
	var a: float = float(p.cam_yaw) + float(p.cam_orbit)
	return [Vector3(sin(a), 0.0, cos(a)), Vector3(-cos(a), 0.0, sin(a))]


func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(20)
	if main.touch_ui == null or main.player == null:
		_ck("boot", false, "no touch_ui or player")
		print("NAVPROBE FAIL")
		quit(1)
		return
	var p: Node3D = main.player

	# ---------- P0: the boot lens is the profile, not a hand-typed number ----
	_ck("boot lens is CameraKit.OUTDOOR",
		is_equal_approx(float(p.cam_back), float(CameraKit.OUTDOOR["back"]))
		and is_equal_approx(float(p.cam_high), float(CameraKit.OUTDOOR["high"])),
		"back=%.1f high=%.1f" % [float(p.cam_back), float(p.cam_high)])
	_ck("clip planes set from the profile",
		p.cam != null and p.cam.near > 0.2 and p.cam.far < 2000.0,
		"near=%.2f far=%.0f" % [p.cam.near, p.cam.far])

	# ---------- N1: the stick is a DIRECTION ----------
	# Settle first so the floor clamp and the chase lens are at rest.
	await _stick(Vector2.ZERO, 0.6)
	var base: Vector3 = p.position
	var bas: Array = _cam_basis()
	var fwd_v: Vector3 = bas[0]
	var right_v: Vector3 = bas[1]

	# push FORWARD: she should travel along the lens axis, barely turning
	_reset_watch()
	await _stick(Vector2(0.0, -1.0), 1.2)     # screen y is +down, so -1 is "up"
	var moved: Vector3 = p.position - base
	moved.y = 0.0
	_ck("stick up swims away from the lens",
		moved.length() > 3.0 and moved.normalized().dot(fwd_v) > 0.7,
		"d=%.1f dot=%.2f" % [moved.length(), moved.normalized().dot(fwd_v) if moved.length() > 0.01 else 0.0])

	# push RIGHT: under the old yaw-rate control this SPUN her on the spot and
	# translated almost nothing. As a direction it must actually move her right.
	await _stick(Vector2.ZERO, 0.8)
	base = p.position
	bas = _cam_basis()
	right_v = bas[1]
	await _stick(Vector2(1.0, 0.0), 1.4)
	moved = p.position - base
	moved.y = 0.0
	_ck("stick right translates instead of spinning",
		moved.length() > 3.0 and moved.normalized().dot(right_v) > 0.3,
		"d=%.1f dot=%.2f" % [moved.length(), moved.normalized().dot(right_v) if moved.length() > 0.01 else 0.0])
	_ck("open water keeps her in frame",
		hidden_frames == 0 and worst_frac < FRAME_MAX and best_frac > FRAME_MIN,
		"hidden=%d frac %.3f..%.3f" % [hidden_frames, best_frac, worst_frac])
	await _stick(Vector2.ZERO, 0.3)

	# ---------- open-water occlusion ----------
	# The reef keeps its structures in main.solids; arena_solids is empty out
	# here, so before this both the boom resolver and the fade system were blind
	# to every rock outcrop, the wreck and the landmarks.
	_ck("the reef registers open-water faders", main.world_faders.size() > 0,
		"%d faders" % main.world_faders.size())
	var reef_seen: bool = false
	for s in main.solids:
		var sy: float = (float(s["y0"]) + float(s["y1"])) * 0.5
		var f0: Vector3 = Vector3(float(s["x"]) - float(s["r"]) - 6.0, sy, float(s["z"]))
		var f1: Vector3 = Vector3(float(s["x"]) + float(s["r"]) + 6.0, sy, float(s["z"]))
		if CameraKit.boom_hit_t(main, f0, f1) < 1.0:
			reef_seen = true
			break
	_ck("the boom resolver sees reef structures in free swim", reef_seen,
		"%d reef solids" % main.solids.size())

	# ---------- oriented-box occlusion ----------
	# The northern gabled roof is a thin slab tilted ~30 deg. Its world AABB is
	# 7.82 units tall against a real half-thickness of 0.7, so an AABB fader
	# blanks the whole roof for shots that pass nowhere near it.
	var slab_half := Vector3(14.5, 0.7, 25.0)
	var slab_aabb := Vector3(12.94, 7.82, 25.0)
	var slab_b: Basis = Basis(Vector3(0, 0, 1), 0.52)
	var a0 := Vector3(-3.0, 6.0, 0.0)
	var a1 := Vector3(3.0, 6.0, 0.0)
	var aabb_says: bool = main._seg_box(a0, a1, Vector3.ZERO, slab_aabb)
	var obb_says: bool = main._seg_obb(a0, a1, Vector3.ZERO, slab_half, slab_b)
	_ck("oriented-box occlusion rejects what the world AABB over-triggered on",
		aabb_says and not obb_says, "aabb=%s obb=%s" % [str(aabb_says), str(obb_says)])
	_ck("oriented-box occlusion still catches a real crossing",
		main._seg_obb(Vector3(0, -10, 0), Vector3(0, 10, 0), Vector3.ZERO, slab_half, slab_b))

	# ---------- into the castle ----------
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main.level2_done_once = false
	main._enter_level2()
	var guard := 0
	while main.game != "level2" and guard < 300:
		guard += 1
		await process_frame
	# let the arrival cutscene finish before teleporting — cutting it short
	# leaves its tween chasing freed props and prints spurious script errors
	var tcut: int = Time.get_ticks_msec()
	while "l2_cutscene_t" in main and float(main.l2_cutscene_t) >= 0.0 \
			and Time.get_ticks_msec() - tcut < 30000:
		await process_frame
	main._enter_castle_interior()
	await _frames(20)
	var o: Vector3 = main.CASTLE_POS
	_ck("castle applied the interior profile",
		is_equal_approx(float(p.cam_back), float(CameraKit.INTERIOR["back"]))
		and is_equal_approx(float(main.move_profile.get("turn", 0.0)), float(main.MOVE_INDOOR["turn"])),
		"back=%.1f turn=%.1f" % [float(p.cam_back), float(main.move_profile.get("turn", 0.0))])
	_ck("she arrives facing the throne, not the exit door",
		cos(float(p.yaw)) < -0.5, "yaw=%.2f" % float(p.yaw))

	# ---------- C4: the zone table can never invert ----------
	var inverted := 0
	var probe_y: Array[float] = [-16.0, -3.0, 4.0, 16.0, 28.0, 35.0, 45.0, 52.0]
	for gx in range(-50, 51, 5):
		for gz in range(-62, 45, 5):
			for zy in probe_y:
				var sp: Vector3 = o + Vector3(float(gx), zy, float(gz))
				var zb: Vector2 = CameraKit.zone_bounds(main, sp, o.y + 2.5, o.y + main.arena_ceil)
				if zb.y < zb.x - 0.001:
					inverted += 1
	_ck("castle zone table never puts the floor above the ceiling",
		inverted == 0, "%d inverted samples" % inverted)

	# ---------- S1: walk the royal stairs to the dais, hands only ----------
	# Bottom of the flight, facing the throne. From here the ONLY input is the
	# stick — if the crown still needs the retired position-writing magnet to be
	# reachable, this fails.
	p.position = o + Vector3(0.0, 4.0, -6.0)
	p.yaw = PI
	p.vel = Vector3.ZERO
	p.snap_cam()
	await _frames(4)
	var pos_before: Vector3 = p.position
	_reset_watch()
	await _stick(Vector2(0.0, -1.0), 4.5)   # swim forward, up the steps
	_ck("royal stairs are climbable by stick alone",
		p.position.y - o.y > 12.0, "y=%.1f" % (p.position.y - o.y))
	_ck("the throne dais is standable",
		p.position.y - o.y > 15.5 and p.position.z - o.z < -22.0,
		"pos=%s" % str(p.position - o))
	_ck("the stair climb never blinks her out of frame",
		hidden_frames == 0, "%d hidden frames" % hidden_frames)
	_ck("the stair climb keeps the boom open",
		worst_boom > 1.8, "min boom %.2f" % worst_boom)
	_ck("interior framing is a third-person frame, not a close-up",
		worst_frac < FRAME_MAX and best_frac > FRAME_MIN,
		"frac %.3f..%.3f" % [best_frac, worst_frac])
	var climb_lo: float = best_frac
	var climb_hi: float = worst_frac
	_ck("no invisible hand moved her (position only changed by swimming)",
		pos_before.distance_to(p.position) < 60.0,
		"travelled %.1f" % pos_before.distance_to(p.position))

	# left along the dais to the Crown Star
	await _stick(Vector2(-1.0, 0.0), 2.5)
	await _stick(Vector2(-0.6, -0.4), 2.0)
	_ck("the Crown Star is won from the dais without a magnet",
		bool(main.g.get("crown_won", false)),
		"pos=%s" % str(p.position - o))

	# ---- DIAGNOSTIC (prints, never asserts): repeat the IDENTICAL stair climb
	# on the pre-fix lens, so the before/after is the same motion through the
	# same geometry rather than two different spots. The audit's headline number
	# was hand trigonometry on cam.fov; this is projected pixel height.
	p.cam_back = 10.0     # the pre-fix hand-tune
	p.cam_high = 4.2
	p.position = o + Vector3(0.0, 4.0, -6.0)
	p.yaw = PI
	p.vel = Vector3.ZERO
	p.snap_cam()
	await _frames(4)
	_reset_watch()
	await _stick(Vector2(0.0, -1.0), 4.5)
	print("NAV|framing diagnostic, same stair climb: lens 10.0/4.2 fills %.3f..%.3f of frame height, boom min %.2f; lens 18.0/8.0 fills %.3f..%.3f"
		% [best_frac, worst_frac, worst_boom, climb_lo, climb_hi])
	p.apply_cam_profile(CameraKit.INTERIOR)
	p.snap_cam()
	await _frames(4)

	# ---------- camera-occlusion fade ----------
	# Registration coverage first: the hall used to fade only _iwall boxes, so
	# every column, prop and slab was invisible to the system.
	var cyl_faders: int = 0
	for w in main.fade_walls:
		if int(w.get("kind", 0)) == 1:
			cyl_faders += 1
	_ck("the hall registers box AND cylinder occluders",
		main.fade_walls.size() > 40 and cyl_faders >= 8,
		"%d faders, %d cylindrical" % [main.fade_walls.size(), cyl_faders])
	# Every fader must resolve to at least one real mesh, or it is dead weight
	# doing a segment test per frame for nothing.
	var empty_faders: int = 0
	for w in main.fade_walls:
		if (w["meshes"] as Array).is_empty():
			empty_faders += 1
	_ck("no fader registered without meshes", empty_faders == 0,
		"%d empty" % empty_faders)
	# Drive it: stand behind the balcony deck slab looking up through it. The
	# deck carries no solid, so the boom resolver cannot route around it — the
	# fade is the only thing that can clear the shot.
	p.position = o + Vector3(0.0, 20.0, -27.0)
	p.yaw = 0.0
	p.vel = Vector3.ZERO
	p.snap_cam()
	await _stick(Vector2.ZERO, 1.6)
	var faded_max: float = 0.0
	for w in main.fade_walls:
		faded_max = maxf(faded_max, float(w["a"]))
	print("NAV|occlusion fade: peak instance transparency %.2f across %d faders"
		% [faded_max, main.fade_walls.size()])
	_ck("an occluder actually fades when it blocks the lens", faded_max > 0.3,
		"peak %.2f" % faded_max)

	# ---------- S2: the entrance facade is solid off-doorway ----------
	p.position = o + Vector3(24.0, 6.0, 34.0)
	p.yaw = 0.0
	p.vel = Vector3.ZERO
	p.snap_cam()
	await _frames(4)
	await _stick(Vector2(0.0, -1.0), 2.5)   # push straight at the facade
	_ck("the hall entrance wall is solid away from the doorway",
		p.position.z - o.z < 44.0 and String(main.g.get("phase", "")) == "hall",
		"z=%.1f phase=%s" % [p.position.z - o.z, String(main.g.get("phase", ""))])

	# ---------- C3: the outdoor lens comes back at its BOOT height ----------
	main._return_to_courtyard()
	await _frames(20)
	_ck("leaving the castle restores the boot outdoor lens",
		is_equal_approx(float(p.cam_high), float(CameraKit.OUTDOOR["high"]))
		and is_equal_approx(float(p.cam_back), float(CameraKit.OUTDOOR["back"])),
		"back=%.1f high=%.1f" % [float(p.cam_back), float(p.cam_high)])
	_ck("leaving the castle restores the open-water swim feel",
		is_equal_approx(float(main.move_profile.get("turn", 0.0)), float(main.MOVE_OPEN["turn"])),
		"turn=%.1f" % float(main.move_profile.get("turn", 0.0)))

	print("NAVPROBE %s" % ("PASS" if fails == 0 else "FAIL (%d)" % fails))
	quit(0 if fails == 0 else 1)
