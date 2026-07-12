extends SceneTree
# Playground audit camera probe: enters the Sky Lagoon, prints water
# diagnostics for every toy, then triggers each play-moment and captures
# screenshots mid-animation. Dev-only; not part of the trusted CI gate.

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/22c09d23-46ce-44d9-974a-d6891729ae81/scratchpad/shots"

var main: Node
var cam: Camera3D

func _marker(pos: Vector3, col: Color, r: float = 0.45) -> void:
	var mi := MeshInstance3D.new()
	var sm := SphereMesh.new()
	sm.radius = r
	sm.height = r * 2.0
	mi.mesh = sm
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.albedo_color = col
	mi.material_override = mat
	mi.position = pos
	main.add_child(mi)

func _extents(node: Node3D, base: Vector3, fwd: Vector3, left: Vector3) -> void:
	# merged world AABB of every mesh, printed as extents along fwd/left/up
	var have := false
	var box := AABB()
	var stack: Array = [node]
	while stack.size() > 0:
		var n: Node = stack.pop_back()
		if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
			var mi := n as MeshInstance3D
			var gb: AABB = mi.global_transform * mi.mesh.get_aabb()
			box = box.merge(gb) if have else gb
			have = true
		for c in n.get_children():
			stack.append(c)
	if not have:
		return
	var fmin := 1e9
	var fmax := -1e9
	var lmin := 1e9
	var lmax := -1e9
	for i in range(8):
		var c: Vector3 = box.get_endpoint(i) - base
		fmin = minf(fmin, c.dot(fwd))
		fmax = maxf(fmax, c.dot(fwd))
		lmin = minf(lmin, c.dot(left))
		lmax = maxf(lmax, c.dot(left))
	print("    extents fwd[%.2f, %.2f] left[%.2f, %.2f] up[%.2f, %.2f]" % [
		fmin, fmax, lmin, lmax, box.position.y - base.y, box.end.y - base.y])

func _shot(cpos: Vector3, look: Vector3, fname: String) -> void:
	cam.position = cpos
	cam.look_at(look)
	await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + "/" + fname)
	print("  shot: " + fname)

func _until(target: float) -> void:
	# run frames until the active play-moment reaches sim-time `target`
	while not (main.toy_play as Dictionary).is_empty() and float(main.toy_play.get("t", 99.0)) < target:
		await process_frame

func _play(kind: String, marks: Array, cam_fwd: float = 1.3, cam_left: float = 0.7, cam_up: float = 0.5, look_up: float = 0.45, cl: float = 9.0, cf: float = -2.0) -> void:
	var toys: Array = main.g.get("toys", [])
	var toy: Dictionary = {}
	for td in toys:
		if String(td["kind"]) == kind:
			toy = td
			break
	if toy.is_empty():
		print("  MISSING toy: " + kind)
		return
	var a: Vector3 = toy["anchor"]
	var base: Vector3 = toy["base"]
	var fwd: Vector3 = toy["fwd"]
	var left: Vector3 = toy["left"]
	var tgt: float = float(toy["tgt"])
	var pl: Node3D = main.player
	pl.position = a + fwd * 3.0 + Vector3(0, 1.0, 0)
	pl.vel = Vector3.ZERO
	var ph := 0.0
	if kind == "merry" and is_instance_valid(toy["node"]):
		var dp: Vector3 = pl.position - base
		ph = atan2(dp.x, dp.z) - (toy["node"] as Node3D).rotation.y
	main.toy_play = {"kind": kind, "toy": toy, "t": 0.0, "dur": toy["dur"], "ph": ph,
		"from": pl.position, "yaw0": float(pl.yaw)}
	var side_eye: Vector3 = base + Vector3(0, tgt * look_up, 0)
	for mk: Array in marks:
		await _until(float(mk[0]))
		var lbl: String = String(mk[1])
		var pp: Vector3 = (main.player as Node3D).position
		var mcl: float = float(mk[2]) if mk.size() > 2 else cl
		var mcf: float = float(mk[3]) if mk.size() > 3 else cf
		await _shot(base + fwd * (tgt * cam_fwd) + left * (tgt * cam_left) + Vector3(0, tgt * cam_up, 0), side_eye, "pg_play_%s_%s_a.png" % [kind, lbl])
		# close profile follow-cam: guaranteed framing on HER
		await _shot(pp + left * mcl + fwd * mcf + Vector3(0, 2.5, 0), pp + Vector3(0, 1.0, 0), "pg_play_%s_%s_c.png" % [kind, lbl])
	# let the moment finish + verify clean exit
	while not (main.toy_play as Dictionary).is_empty():
		await process_frame
	print("  %s done: pos=(%.1f %.1f %.1f) rotx=%.2f" % [kind, pl.position.x - main.LEVEL2_POS.x, pl.position.y - main.LEVEL2_POS.y, pl.position.z - main.LEVEL2_POS.z, pl.rotation.x])

func _init() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
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
	for i in range(10):
		await process_frame
	cam = Camera3D.new()
	cam.fov = 50.0
	get_root().add_child(cam)
	cam.make_current()

	var o: Vector3 = main.LEVEL2_POS
	print("=== PLAYGROUND DIAGNOSTICS (local coords rel LEVEL2_POS) ===")
	var toys: Array = main.g.get("toys", [])
	for toy in toys:
		var lb: Vector3 = (toy["base"] as Vector3) - o
		print("  %-8s base=(%.1f, %.1f, %.1f)  ground_y=%.2f %s" % [
			String(toy["kind"]), lb.x, lb.y, lb.z, lb.y,
			("<-- SUNK (river/moat)" if lb.y < -1.5 else "OK")])
	var ctr: Vector3 = o + Vector3(74, 6, 92)
	main.player.position = o + Vector3(0, 10, 175)
	await _shot(ctr + Vector3(-30, 60, -60), ctr, "pg_after_overview.png")
	await _shot(ctr + Vector3(60, 45, 35), ctr, "pg_after_overview2.png")

	print("=== TOY EXTENTS ===")
	for toy in toys:
		print("  %s:" % String(toy["kind"]))
		_extents(toy["node"], toy["base"], toy["fwd"], toy["left"])
	# marker trail: the slide choreography path (magenta = climb, green = chute)
	for toy in toys:
		if String(toy["kind"]) != "slide":
			continue
		var b: Vector3 = toy["base"]
		var fw: Vector3 = toy["fwd"]
		var tg: float = float(toy["tgt"])
		var lfoot: Vector3 = toy["anchor"]
		var ltop: Vector3 = b - fw * (tg * 0.17) + Vector3(0, tg * 0.52, 0)
		var lip: Vector3 = b + fw * (tg * 0.02) + Vector3(0, tg * 0.50 + 0.9, 0)
		var mid: Vector3 = b + fw * (tg * 0.24) + Vector3(0, tg * 0.28 + 0.9, 0)
		var out: Vector3 = b + fw * (tg * 0.46) + Vector3(0, 1.5, 0)
		for k in range(5):
			_marker(lfoot.lerp(ltop, float(k) / 4.0), Color(1, 0.2, 1))
		_marker(lip, Color(0.2, 1, 0.3))
		_marker(mid, Color(0.2, 1, 0.3))
		_marker(out, Color(0.2, 1, 0.3))
		await _shot(b + toy["left"] * (tg * 1.35) + Vector3(0, tg * 0.45, 0), b + Vector3(0, tg * 0.3, 0), "pg_slide_markers_side.png")
		await _shot(b - fw * (tg * 1.15) + toy["left"] * (tg * 0.55) + Vector3(0, tg * 0.45, 0), b + Vector3(0, tg * 0.3, 0), "pg_slide_markers_ladder.png")
	print("=== PLAY MOMENTS ===")
	await _play("slide", [[0.6, "climb1", 4.0, -11.0], [1.7, "climb2", 4.0, -11.0], [2.55, "top", 4.0, -11.0], [3.3, "ride1"], [4.0, "ride2"], [5.0, "land"]], 1.2, 0.9, 0.42, 0.32, 13.0, -5.0)
	await _play("swing", [[2.55, "arc1"], [3.2, "arc2", 2.0, 9.5], [3.85, "arc3"]], 0.45, 1.3, 0.3, 0.25, 8.5, 8.5)
	await _play("sandbox", [[0.85, "dig1"], [2.3, "dig2"]], 0.95, 0.55, 0.5, 0.12)
	await _play("seesaw", [[1.05, "press"], [1.57, "hop"]], 1.35, 0.15, 0.38, 0.16)
	await _play("merry", [[1.6, "ride1"], [3.2, "ride2"]], 1.1, 0.8, 0.5, 0.2)
	await _play("horse", [[1.45, "rockf"], [2.4, "rockb"]], 0.4, 1.7, 0.42, 0.36)
	print("=== DONE ===")
	quit()
