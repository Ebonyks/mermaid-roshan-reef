extends SceneTree
# Castle-hall camera regression (2026-07-21 report: "camera stuck inside
# Roshan" climbing to Princess Huluu). Root cause: solids store their body
# pad inflated in, and standing ON one (under-stair blocks) put the chase
# focus inside the pad ring -> boom collapsed to MIN_BOOM for the whole
# climb. Walks the royal stairs to the throne and the dreaming stairs while
# monitoring the boom every frame. Prints OK/FAIL lines (ci.sh convention).

var main: Node
var fails := 0
var min_boom := 1e9
var core_hits := 0

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		fails += 1
	print("CASTLECAM|%s: %s %s" % [label, "OK" if ok else "FAIL", detail])

func _inside_core(p: Vector3) -> bool:
	for s in main.arena_solids:
		var pad: float = float(s.get("pad", 0.0))
		if bool(s.box):
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

func _in_pad_ring(p: Vector3) -> bool:
	# inside a solid's stored (padded) bounds but NOT inside its core
	for s in main.arena_solids:
		var pad: float = float(s.get("pad", 0.0))
		if pad <= 0.0:
			continue
		if bool(s.box):
			if absf(p.x - float(s.cx)) < float(s.hx) \
					and absf(p.z - float(s.cz)) < float(s.hz) \
					and p.y > float(s.y0) and p.y < float(s.y1):
				if not _inside_core(p):
					return true
		else:
			var dx: float = p.x - float(s.x)
			var dz: float = p.z - float(s.z)
			if dx * dx + dz * dz < float(s.r) * float(s.r) \
					and p.y > float(s.y0) and p.y < float(s.y1):
				if not _inside_core(p):
					return true
	return false

func _swim(dir: Vector3, frames60: int) -> void:
	# wall-clock paced (headless frame rates vary); sample the boom each frame
	var player: Node3D = main.player
	var cam: Camera3D = player.cam
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < int(float(frames60) * 1000.0 / 60.0):
		player.vel = dir
		await process_frame
		var boom: float = cam.position.distance_to(player.position + Vector3(0, 1.5, 0))
		min_boom = minf(min_boom, boom)
		if _inside_core(cam.position):
			core_hits += 1

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
		await process_frame   # let the entry cutscene finish — teleporting mid-
		# cutscene leaves its tween chasing freed props (spurious script errors)
	main._enter_castle_interior()
	for i in range(20):
		await process_frame
	var o: Vector3 = main.CASTLE_POS
	var player: Node3D = main.player

	# ---- route 1: standing ON the royal stairs and the throne platform ----
	# The reported failure: standing on the under-stair blocks puts the chase
	# FOCUS inside a solid's pad ring and the boom collapsed to MIN_BOOM.
	var pad_ring_seen := false
	for spot: Vector3 in [Vector3(0.0, 8.9, -16.0), Vector3(0.0, 15.4, -22.5), Vector3(0.0, 21.5, -25.0)]:
		player.position = o + spot
		player.yaw = PI   # facing -z, camera behind at +z
		player.snap_cam()
		await process_frame
		var focus: Vector3 = player.position + Vector3(0, 1.5, 0)
		if _in_pad_ring(focus):
			pad_ring_seen = true
		min_boom = 1e9
		core_hits = 0
		await _swim(Vector3.ZERO, 45)   # hold still, let the chase settle
		print("CASTLECAM|royal spot=%s boom=%.2f" % [spot, min_boom])
		_ck("royal spot %s boom open" % spot, min_boom > 2.0, "min=%.2f" % min_boom)
		_ck("royal spot %s cam outside cores" % spot, core_hits == 0, "hits=%d" % core_hits)
	# informational: the pad-ring rule (CameraKit core-vs-pad) has no natural
	# trigger on this route — the 2026-07-21 bug proved to be the throne prop
	print("CASTLECAM|info pad_ring_seen=%s" % pad_ring_seen)

	# ---- the ACTUAL reported failure: perched at Huluu FACING THE HALL, the
	# chase cam swings behind her INTO the shell throne (it had no solid) ----
	player.position = o + Vector3(0.0, 21.0, -25.0)
	player.yaw = 0.0   # facing +z: camera seeks -z, straight at the throne
	player.snap_cam()
	await process_frame
	min_boom = 1e9
	core_hits = 0
	await _swim(Vector3.ZERO, 60)
	var cam_z: float = (player.cam.position - o).z
	print("CASTLECAM|huluu_facing_hall boom=%.2f cam_z=%.2f" % [min_boom, cam_z])
	_ck("throne blocks the boom (cam stays out of the shell)", cam_z > -26.5, "cam_z=%.2f" % cam_z)
	_ck("huluu perch cam outside cores", core_hits == 0, "hits=%d" % core_hits)

	# ---- route 2: dreaming stairs (x-axis ramp, tight ceil 52.5) ----
	player.position = o + Vector3(-19.0, 35.5, -41.0)
	player.yaw = -PI * 0.5
	player.snap_cam()
	await process_frame
	min_boom = 1e9
	core_hits = 0
	await _swim(Vector3(7.0, 2.0, 0.0), 150)         # up the dreaming ramp x -20 -> -4
	print("CASTLECAM|dreaming min_boom=%.2f pos=%s" % [min_boom, player.position - o])
	_ck("dreaming stairs boom never collapses", min_boom > 1.2, "min=%.2f" % min_boom)
	_ck("dreaming stairs cam outside solid cores", core_hits == 0, "hits=%d" % core_hits)

	# ---- cornering must STILL collapse: press into the throne-room back wall ----
	# (the pad rule must not have broken the never-inside-mesh guarantee)
	player.position = o + Vector3(0.0, 22.0, -30.0)
	player.yaw = PI
	player.snap_cam()
	min_boom = 1e9
	core_hits = 0
	await _swim(Vector3(0, 0, -10.0), 90)            # shove her into the back wall
	_ck("cornered cam still outside cores", core_hits == 0, "hits=%d" % core_hits)

	print("CASTLECAM|done fails=%d" % fails)
	if fails > 0:
		print("FAIL castle camera")
	quit()
