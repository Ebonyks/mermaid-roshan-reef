extends SceneTree
# Diagnostic companion to probe_castle_cam_audit: at each STUCK spot, name
# the solid(s) that contain the focus / collapse the boom.

const SPOTS := [
	["hall", Vector3(25.35, 3.36, 27.26)],
	["balcony_R", Vector3(31.36, 4.48, -21.48)],
	["upstairs_back", Vector3(-2.35, 36.25, -60.0)],
	["dreaming_floor", Vector3(-47.35, 53.01, -60.0)],
]

var main: Node

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
	var t0 := Time.get_ticks_msec()
	while "l2_cutscene_t" in main and float(main.l2_cutscene_t) >= 0.0 and Time.get_ticks_msec() - t0 < 30000:
		await process_frame
	main._enter_castle_interior()
	for i in range(25):
		await process_frame
	var o: Vector3 = main.CASTLE_POS
	for sp in SPOTS:
		var pos: Vector3 = o + (sp[1] as Vector3)
		var focus: Vector3 = pos + Vector3(0, 1.5, 0)
		print("DIAG|==== %s player=%s" % [sp[0], sp[1]])
		for i in range(main.arena_solids.size()):
			var s: Dictionary = main.arena_solids[i]
			var pad: float = float(s.get("pad", 0.0))
			var inside_pad := false
			var inside_core := false
			if bool(s.get("box", false)):
				if absf(focus.x - float(s.cx)) < float(s.hx) and absf(focus.z - float(s.cz)) < float(s.hz) and focus.y > float(s.y0) and focus.y < float(s.y1):
					inside_pad = true
					if absf(focus.x - float(s.cx)) < float(s.hx) - pad and absf(focus.z - float(s.cz)) < float(s.hz) - pad and focus.y > float(s.y0) + pad and focus.y < float(s.y1) - pad:
						inside_core = true
			else:
				var dx: float = focus.x - float(s.x)
				var dz: float = focus.z - float(s.z)
				if dx * dx + dz * dz < float(s.r) * float(s.r) and focus.y > float(s.y0) and focus.y < float(s.y1):
					inside_pad = true
					var rr: float = float(s.r) - pad
					if rr > 0.0 and dx * dx + dz * dz < rr * rr and focus.y > float(s.y0) + pad and focus.y < float(s.y1) - pad:
						inside_core = true
			if inside_pad:
				var desc: String
				if bool(s.get("box", false)):
					desc = "box c=(%.1f,%.1f) h=(%.1f,%.1f) y=%.1f..%.1f pad=%.1f" % [float(s.cx) - o.x, float(s.cz) - o.z, s.hx, s.hz, float(s.y0) - o.y, float(s.y1) - o.y, pad]
				else:
					desc = "cyl c=(%.1f,%.1f) r=%.1f y=%.1f..%.1f pad=%.1f" % [float(s.x) - o.x, float(s.z) - o.z, s.r, float(s.y0) - o.y, float(s.y1) - o.y, pad]
				print("DIAG|  focus inside %s of solid[%d] %s" % ["CORE" if inside_core else "pad ring", i, desc])
		# where does the boom hit? name the solid responsible per direction
		for yaw_deg in [0, 90, 180, 270]:
			var yr: float = deg_to_rad(float(yaw_deg))
			var want: Vector3 = pos + Vector3(-sin(yr) * 10.0, 4.2, -cos(yr) * 10.0)
			var d: Vector3 = want - focus
			var t: float = 1.0
			var who := -1
			for i in range(main.arena_solids.size()):
				var s: Dictionary = main.arena_solids[i]
				var st: float
				if bool(s.get("box", false)):
					st = CameraKit._seg_box_t(focus, d, s, 0.0)
				else:
					st = CameraKit._seg_cyl_t(focus, d, s, 0.0)
				if st < t:
					t = st
					who = i
			var sdesc := ""
			if who >= 0:
				var s2: Dictionary = main.arena_solids[who]
				if bool(s2.get("box", false)):
					sdesc = "box[%d] c=(%.1f,%.1f) h=(%.1f,%.1f) y=%.1f..%.1f" % [who, float(s2.cx) - o.x, float(s2.cz) - o.z, s2.hx, s2.hz, float(s2.y0) - o.y, float(s2.y1) - o.y]
				else:
					sdesc = "cyl[%d] c=(%.1f,%.1f) r=%.1f y=%.1f..%.1f" % [who, float(s2.x) - o.x, float(s2.z) - o.z, s2.r, float(s2.y0) - o.y, float(s2.y1) - o.y]
			print("DIAG|  yaw %d boom_hit_t=%.3f %s" % [yaw_deg, t, sdesc])
	# any degenerate solids? (inverted or absurd extents break the slab test)
	for i in range(main.arena_solids.size()):
		var s: Dictionary = main.arena_solids[i]
		if bool(s.get("box", false)):
			if float(s.hx) <= 0.0 or float(s.hz) <= 0.0 or float(s.y0) >= float(s.y1) or float(s.hx) > 200.0 or float(s.hz) > 200.0:
				print("DIAG|DEGENERATE box[%d] cx=%.1f cz=%.1f hx=%.2f hz=%.2f y=%.1f..%.1f" % [i, float(s.cx) - o.x, float(s.cz) - o.z, s.hx, s.hz, float(s.y0) - o.y, float(s.y1) - o.y])
		else:
			if float(s.r) <= 0.0 or float(s.y0) >= float(s.y1) or float(s.r) > 200.0:
				print("DIAG|DEGENERATE cyl[%d] x=%.1f z=%.1f r=%.2f y=%.1f..%.1f" % [i, float(s.x) - o.x, float(s.z) - o.z, s.r, float(s.y0) - o.y, float(s.y1) - o.y])
	quit()
