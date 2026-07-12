extends SceneTree
# Hand/arm clipping audit for the playground play-moments: triggers every
# moment and captures a tight hand-cam + a side profile at dense timestamps,
# so arm poses can be verified frame-by-frame against toy and body geometry.
# Dev-only; not part of the trusted CI gate.

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/22c09d23-46ce-44d9-974a-d6891729ae81/scratchpad/hands"

var main: Node
var cam: Camera3D

func _shot(cpos: Vector3, look: Vector3, fname: String) -> void:
	cam.position = cpos
	cam.look_at(look)
	await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + "/" + fname)
	print("  shot: " + fname)

func _until(target: float) -> void:
	while not (main.toy_play as Dictionary).is_empty() and float(main.toy_play.get("t", 99.0)) < target:
		await process_frame

func _play(kind: String, marks: Array) -> void:
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
	var pl: Node3D = main.player
	pl.position = a + (toy["fwd"] as Vector3) * 3.0 + Vector3(0, 1.0, 0)
	pl.vel = Vector3.ZERO
	var ph := 0.0
	if kind == "merry" and is_instance_valid(toy["node"]):
		var dp: Vector3 = pl.position - base
		ph = atan2(dp.x, dp.z) - (toy["node"] as Node3D).rotation.y
	main.toy_play = {"kind": kind, "toy": toy, "t": 0.0, "dur": toy["dur"], "ph": ph,
		"from": pl.position, "yaw0": float(pl.yaw)}
	for mk: Array in marks:
		await _until(float(mk[0]))
		var lbl: String = String(mk[1])
		var pp: Vector3 = pl.position
		# her CURRENT facing (model faces -Z; lean is on rotation.x, so use yaw)
		var fc := Vector3(-sin(pl.rotation.y), 0.0, -cos(pl.rotation.y)).normalized()
		var sd: Vector3 = fc.cross(Vector3.UP).normalized()
		# tight 3/4 hand-cam from her front-left, aimed at the chest
		await _shot(pp + fc * 4.2 + sd * 2.4 + Vector3(0, 2.3, 0), pp + Vector3(0, 1.3, 0), "h_%s_%s_hand.png" % [kind, lbl])
		# side profile, arm silhouette against the toy
		await _shot(pp + sd * 6.0 + fc * 0.8 + Vector3(0, 1.6, 0), pp + Vector3(0, 1.0, 0), "h_%s_%s_prof.png" % [kind, lbl])
	while not (main.toy_play as Dictionary).is_empty():
		await process_frame
	print("  %s complete" % kind)

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
	cam.fov = 45.0
	get_root().add_child(cam)
	cam.make_current()
	print("=== HAND AUDIT ===")
	await _play("slide", [[0.30, "hop1mid"], [0.55, "hop1land"], [0.95, "hop2mid"], [1.65, "hop3"],
		[2.30, "duck"], [2.65, "lip"], [3.10, "ride_a"], [3.60, "ride_b"], [4.20, "bottom"], [4.80, "settle"]])
	await _play("swing", [[1.20, "ramp"], [2.05, "back"], [2.55, "mid"], [3.05, "fwd"], [3.55, "back2"], [4.20, "fwd2"]])
	await _play("sandbox", [[0.50, "scoopL"], [0.85, "cross"], [1.20, "scoopR"], [1.90, "scoopL2"], [2.60, "scoopR2"], [3.40, "late"]])
	await _play("seesaw", [[0.55, "rise"], [1.05, "press"], [1.57, "top"], [2.10, "press2"], [2.60, "top2"]])
	await _play("merry", [[1.00, "early"], [2.20, "mid"], [3.40, "late"]])
	await _play("horse", [[0.70, "start"], [1.20, "fwd"], [1.70, "back"], [2.20, "fwd2"], [2.70, "back2"]])
	print("=== DONE ===")
	quit()
