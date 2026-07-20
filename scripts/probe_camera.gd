extends SceneTree
# Camera regression probe — CAMERA_AUDIT_2026_07.md P0 verification.
# Drives the REAL player chase camera (processing stays enabled) along the
# routes that produced the three camera-inside-geometry screenshots in the
# Northern Kingdom, asserting every frame that the lens is legal:
#   (a) not inside any arena solid, (b) above the walk-height oracle,
#   (c) under the grand hall's ceiling zone while Roshan is inside the hall,
#   (d) a current camera always exists.
# With a window (no --headless) it also saves review PNGs of each scenario.

var ok := true
var main: ReefMain
var shots_dir := "C:/Users/Peter/AppData/Local/Temp/claude/probe_camera_shots"


func _ck(label: String, passed: bool, detail: String = "") -> void:
	print("CAM|%s: %s%s" % [label, "OK" if passed else "FAIL",
		(" (" + detail + ")") if detail != "" else ""])
	if not passed:
		ok = false


func _cam_in_solid(p: Vector3) -> String:
	# point-vs-solid with a small forgiveness shrink: resolve() deliberately
	# ignores a boom that STARTS inside a padded solid, so only a real breach
	# (deeper than the shrink) counts as a failure
	var shrink := 0.35
	for s in main.arena_solids:
		if p.y < float(s.y0) + shrink or p.y > float(s.y1) - shrink:
			continue
		if s.box:
			if absf(p.x - float(s.cx)) < float(s.hx) - shrink \
					and absf(p.z - float(s.cz)) < float(s.hz) - shrink:
				return "box@(%.0f,%.0f)" % [float(s.cx), float(s.cz)]
		else:
			var dx: float = p.x - float(s.x)
			var dz: float = p.z - float(s.z)
			if sqrt(dx * dx + dz * dz) < float(s.r) - shrink:
				return "cyl@(%.0f,%.0f)" % [float(s.x), float(s.z)]
	return ""


func _walk(label: String, dir: Vector3, seconds: float, hall_ceil: bool = false) -> void:
	# drive Roshan like a player would and police the lens every frame
	var worst_ground := 1e9
	var solid_hit := ""
	var no_cam := false
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < int(seconds * 1000.0):
		main.player.vel = dir * 16.0
		await process_frame
		var cam: Camera3D = main.player.cam
		if get_root().get_viewport().get_camera_3d() == null:
			no_cam = true
		if cam == null or not cam.is_inside_tree():
			continue
		var cp: Vector3 = cam.position
		var gh: float = main.northern_walk_h(cp.x, cp.z)
		worst_ground = minf(worst_ground, cp.y - gh)
		if solid_hit == "":
			solid_hit = _cam_in_solid(cp)
		if hall_ceil:
			var hall_top: float = main.NORTHERN_POS.y + 27.0
			if cp.y > hall_top + 0.3:
				solid_hit = "over hall roofline y=%.1f" % cp.y
	_ck(label + " lens above terrain", worst_ground > -0.3,
		"worst clearance %.2f" % worst_ground)
	_ck(label + " lens outside solids", solid_hit == "", solid_hit)
	_ck(label + " a camera is always current", not no_cam)


func _shot(name: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	DirAccess.make_dir_recursive_absolute(shots_dir)
	img.save_png(shots_dir + "/" + name + ".png")
	print("CAM|shot saved: " + name)


func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for friend: Dictionary in main.friends:
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main._enter_level2()
	await process_frame
	main.l2_cutscene_t = -1.0
	var sky_gate: Vector3 = main.g.get("northern_portal_pos", Vector3.ZERO)
	main._tick_level2(0.0, sky_gate)
	await process_frame
	_ck("entered northern world", main.game == "north" and main.northern_floor)
	var o: Vector3 = main.NORTHERN_POS

	# snap-on-entry: the portal must not leave the lens back in the lagoon
	var cam0: Camera3D = main.player.cam
	_ck("entry snapped the lens beside Roshan",
		cam0 != null and cam0.position.distance_to(main.player.position) < 40.0,
		"dist %.0f" % (cam0.position.distance_to(main.player.position) if cam0 != null else -1.0))

	# S1 — the downhill entry walk (screenshots 1 + 2: lens buried in the
	# hillside rising behind Roshan). Walk the pass descent into the forest.
	await _walk("S1 pass descent", Vector3(0, 0, -1), 14.0)
	await _shot("s1_pass_descent")

	# S2 — forest to town along the strip (long tracking walk)
	await _walk("S2 forest walk", Vector3(0.15, 0, -1).normalized(), 14.0)
	await _shot("s2_forest")

	# S3 — inside the grand hall (screenshot 3: lens inside the hall wall).
	# Teleport to the door, walk to the fountain, then press into a side wall
	# so the ideal boom position is INSIDE the wall solid.
	main.player.position = o + Vector3(0.0, 8.0, -305.0)
	main.player.yaw = PI
	main.player.vel = Vector3.ZERO
	main.player.snap_cam()
	await _walk("S3 hall entry", Vector3(0, 0, -1), 5.0, true)
	await _shot("s3_hall")
	main.player.yaw = PI * 0.5   # face +x-ish: back to the west wall
	await _walk("S3 wall press", Vector3(-1, 0, 0), 4.0, true)
	var cam1: Camera3D = main.player.cam
	_ck("S3 boom pulled in front of the wall",
		cam1.position.distance_to(main.player.position) < 27.0,
		"boom %.1f" % cam1.position.distance_to(main.player.position))
	await _shot("s3_wall_press")

	# S4 — mezzanine: lens must duck under the roofline zone
	main.player.position = o + Vector3(0.0, 19.0, -340.0)
	main.player.yaw = 0.0
	main.player.snap_cam()
	await _walk("S4 mezzanine", Vector3(0.6, 0, 1).normalized(), 4.0, true)
	await _shot("s4_mezzanine")

	print("CAMPROBE %s" % ("PASS" if ok else "FAIL"))
	quit(0 if ok else 1)
