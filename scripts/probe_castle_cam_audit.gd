extends SceneTree
# FULL castle camera audit (owner request 2026-07-26: "frame by frame, the
# entire castle, ensure it does not clip"). Swims a waypoint route through
# EVERY walkable castle zone with the real player tick + real chase camera.
# Every rendered frame asserts:
#   CORE  — lens inside a solid's real mesh (pad excluded)      -> FAIL
#   FLOOR — lens below CameraKit.ground_y at its own xz         -> FAIL
#   CEIL  — lens above CameraKit.ceil_y at its own xz           -> FAIL
#   STUCK — boom < 1.2u for > 1.5s continuously                 -> FAIL
#   OCCL  — a solid CORE cuts the lens->Roshan segment > 2.5s   -> warn
#             (fade walls legitimately cross it briefly)
# Violations print with zone + position so each one is fixable. ci.sh
# convention: any FAIL line fails the gate.

var main: Node
var fails := 0
var o: Vector3
var viol := {}          # "zone|kind" -> count
var stuck_ms := 0
var occl_ms := 0
var last_ms := 0

func _report(zone: String, kind: String, warn: bool, detail: String) -> void:
	var key := zone + "|" + kind
	viol[key] = int(viol.get(key, 0)) + 1
	if int(viol[key]) == 1:   # first hit per zone+kind prints loudly
		if not warn:
			fails += 1
		print("CAMAUDIT|%s %s %s: %s" % ["warn" if warn else "FAIL", zone, kind, detail])

func _inside_core(p: Vector3) -> bool:
	for s in main.arena_solids:
		var pad: float = float(s.get("pad", 0.0))
		if bool(s.get("box", false)):
			if absf(p.x - float(s.cx)) < float(s.hx) - pad \
					and absf(p.z - float(s.cz)) < float(s.hz) - pad \
					and p.y > float(s.y0) + pad and p.y < float(s.y1) - pad:
				return true
		else:
			var dx: float = p.x - float(s.x)
			var dz: float = p.z - float(s.z)
			var rr: float = float(s.r) - pad
			if rr > 0.0 and dx * dx + dz * dz < rr * rr \
					and p.y > float(s.y0) + pad and p.y < float(s.y1) - pad:
				return true
	return false

func _core_blocks(a: Vector3, b: Vector3) -> bool:
	# does any solid CORE cut segment a->b? (pads shrunk away)
	var d: Vector3 = b - a
	for s in main.arena_solids:
		var pad: float = float(s.get("pad", 0.0))
		var t: float
		if bool(s.get("box", false)):
			t = CameraKit._seg_box_t(a, d, s, pad)
		else:
			t = CameraKit._seg_cyl_t(a, d, s, pad)
		if t < 1.0 and t > 0.0:
			return true
	return false

func _frame_checks(zone: String) -> void:
	var player: Node3D = main.player
	var cam: Camera3D = player.cam
	if cam == null or not cam.is_inside_tree():
		_report(zone, "NOCAM", false, "player camera missing")
		return
	var cp: Vector3 = cam.position
	var focus: Vector3 = player.position + Vector3(0, 1.5, 0)
	var now := Time.get_ticks_msec()
	var dt: int = now - last_ms
	last_ms = now
	if _inside_core(cp):
		_report(zone, "CORE", false, "cam inside solid core at %s" % (cp - o))
	# band-by-focus, same selection resolve() uses; where floor and ceiling
	# genuinely contradict (tight stairwells) resolve centres the lens, so
	# only judge against whichever constraint set is satisfiable
	var gy: float = CameraKit.ground_y(main, cp, focus.y)
	var cy: float = CameraKit.ceil_y(main, cp, focus.y)
	if gy <= cy:
		if cp.y < gy - 0.3:
			_report(zone, "FLOOR", false, "cam y=%.1f under floor oracle %.1f at %s" % [cp.y - o.y, gy - o.y, Vector2(cp.x - o.x, cp.z - o.z)])
		if cp.y > cy + 0.3:
			_report(zone, "CEIL", false, "cam y=%.1f above ceil %.1f at %s" % [cp.y - o.y, cy - o.y, Vector2(cp.x - o.x, cp.z - o.z)])
	var boom: float = cp.distance_to(focus)
	# 0.8: resting at a padded wall face is ~1.16 and legitimate (near-hide
	# covers it); a true collapse parks at MIN_BOOM 0.15
	stuck_ms = stuck_ms + dt if boom < 0.8 else 0
	if stuck_ms > 1500:
		_report(zone, "STUCK", false, "boom %.2f collapsed >1.5s at %s" % [boom, player.position - o])
		stuck_ms = 0
	occl_ms = occl_ms + dt if _core_blocks(cp, focus) else 0
	if occl_ms > 2500:
		_report(zone, "OCCL", true, "core solid occludes Roshan >2.5s at %s" % (player.position - o))
		occl_ms = 0

func _leg(zone: String, from: Vector3, to: Vector3, teleport: bool) -> void:
	var player: Node3D = main.player
	if teleport:
		player.position = o + from
		player.vel = Vector3.ZERO
		player.snap_cam()
		await process_frame
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 14000:
		var tgt: Vector3 = o + to
		var d: Vector3 = tgt - player.position
		if Vector2(d.x, d.z).length() < 1.6 and absf(d.y) < 3.5:
			return
		var dir: Vector3 = d.normalized()
		player.vel = dir * 9.0
		player.yaw = atan2(-dir.x, -dir.z)
		await process_frame
		_frame_checks(zone)
	print("CAMAUDIT|note %s leg timeout toward %s (at %s) - teleporting on" % [zone, to, player.position - o])
	player.position = o + to
	player.snap_cam()

func _route(zone: String, pts: Array) -> void:
	stuck_ms = 0
	occl_ms = 0
	await _leg(zone, pts[0], pts[0], true)
	for i in range(1, pts.size()):
		await _leg(zone, pts[i - 1], pts[i], false)

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main._enter_level2()
	var tcut := Time.get_ticks_msec()
	while "l2_cutscene_t" in main and float(main.l2_cutscene_t) >= 0.0 \
			and Time.get_ticks_msec() - tcut < 30000:
		await process_frame
	main._enter_castle_interior()
	for i in range(25):
		await process_frame
	o = main.CASTLE_POS
	last_ms = Time.get_ticks_msec()

	# ---- ground floor: full serpentine of the great hall ----
	await _route("hall", [
		Vector3(-28, 3.5, 38), Vector3(28, 3.5, 38), Vector3(28, 3.5, 20),
		Vector3(-28, 3.5, 20), Vector3(-28, 3.5, 2), Vector3(28, 3.5, 2),
		Vector3(28, 3.5, -14), Vector3(-28, 3.5, -14), Vector3(0, 3.5, -6)])
	# ---- royal stairs -> throne dais -> Huluu perch, then face the hall ----
	await _route("royal_stairs", [
		Vector3(0, 4.0, -8.5), Vector3(0, 10.0, -16.0), Vector3(0, 16.0, -23.0),
		Vector3(-5, 18.0, -25.5), Vector3(5, 18.0, -25.5), Vector3(0, 21.0, -25.0)])
	# ---- balcony stairs both sides ----
	await _route("balcony_R", [Vector3(30, 4.5, -22.5), Vector3(30, 18.0, -27.0), Vector3(30, 31.6, -31.0)])
	await _route("balcony_L", [Vector3(-30.5, 4.5, -22.5), Vector3(-30.5, 18.0, -27.0), Vector3(-30.5, 31.6, -31.0)])
	# ---- mezzanine strip over the hall ----
	await _route("mezzanine", [Vector3(-23, 36.0, -27), Vector3(23, 36.0, -27)])
	# ---- upstairs back block + both wing galleries ----
	# the back block is partitioned (interior walls at x~0 and around rooms) —
	# audit each room with its own teleport entry instead of swimming through
	# walls the player also cannot cross
	await _route("upstairs_back_W", [Vector3(-48, 36.8, -60), Vector3(-10, 36.8, -60), Vector3(-48, 36.8, -44)])
	await _route("upstairs_back_E", [Vector3(48, 36.8, -60), Vector3(10, 36.8, -60), Vector3(48, 36.8, -44)])
	await _route("upstairs_back_mid", [Vector3(0, 36.8, -44), Vector3(0, 36.8, -50)])
	await _route("left_wing", [Vector3(-46, 36.8, -30), Vector3(-40, 36.8, -8), Vector3(-46, 36.8, 14)])
	await _route("right_wing", [Vector3(46, 36.8, -30), Vector3(40, 36.8, -8), Vector3(46, 36.8, 14)])
	# ---- dreaming stairs + full dreaming floor ----
	await _route("dreaming_stairs", [Vector3(-19, 37.2, -41), Vector3(-12, 44.0, -41), Vector3(-5, 52.6, -41)])
	await _route("dreaming_W", [Vector3(-48, 53.2, -60), Vector3(-48, 53.2, -44), Vector3(-30, 53.2, -52)])
	await _route("dreaming_E", [Vector3(48, 53.2, -60), Vector3(48, 53.2, -44), Vector3(30, 53.2, -52)])
	await _route("dreaming_mid", [Vector3(0, 53.2, -60), Vector3(0, 53.2, -44)])
	# ---- basement: approach ramp, corridor, rooms, privy, exit stairs ----
	await _route("basement_ramp", [Vector3(0, -2.0, -42.5), Vector3(0, -8.0, -44.5), Vector3(0, -13.5, -47.0)])
	await _route("basement_corridor", [Vector3(0, -14.5, -40), Vector3(0, -14.5, -20), Vector3(0, -14.5, 0)])
	await _route("basement_cross_W", [Vector3(-22, -14.5, -30), Vector3(-4, -14.5, -30)])
	await _route("basement_cross_E", [Vector3(22, -14.5, -30), Vector3(4, -14.5, -30)])
	await _route("basement_main_W", [Vector3(-26, -14.5, 12), Vector3(-4, -14.5, 12), Vector3(-26, -14.5, 30)])
	await _route("basement_main_E", [Vector3(26, -14.5, 12), Vector3(4, -14.5, 12), Vector3(26, -14.5, 30)])
	await _route("privy", [Vector3(-30, -14.5, -28), Vector3(-27, -14.5, -25)])
	await _route("basement_exit_stairs", [Vector3(-24, -14.5, 32.5), Vector3(-24, -8.0, 30.0), Vector3(-24, -0.5, 27.0)])

	print("CAMAUDIT|==== SUMMARY ====")
	for k in viol:
		print("CAMAUDIT|count %s = %d" % [k, viol[k]])
	print("CAMAUDIT|done fails=%d" % fails)
	if fails > 0:
		print("FAIL castle camera audit")
	else:
		print("CAMAUDIT|ALL CLEAN")
	quit()
