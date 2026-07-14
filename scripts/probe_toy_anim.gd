extends SceneTree
# Ambient toy animation check: timed close-ups of the empty swing (pendulum
# extremes) and a numeric spin check on the merry-go-round. Dev-only.

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/22c09d23-46ce-44d9-974a-d6891729ae81/scratchpad/toyanim"

var main: Node
var cam: Camera3D

func _shot(fname: String) -> void:
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + "/" + fname)
	print("  shot: " + fname)

func _wait(sec: float) -> void:
	var t := 0.0
	while t < sec:
		t += 1.0 / 60.0
		await process_frame

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
	for i in range(20):
		await process_frame
	var swing: Dictionary = {}
	var merry: Dictionary = {}
	for td in (main.g.get("toys", []) as Array):
		if String(td["kind"]) == "swing":
			swing = td
		elif String(td["kind"]) == "merry":
			merry = td
	cam = Camera3D.new()
	cam.fov = 45.0
	get_root().add_child(cam)
	cam.make_current()
	# profile view: the seats pendulum along the swing's fwd axis, so shoot
	# from the LEFT side where the arc is fully visible
	var sb: Vector3 = swing["base"]
	var sleft: Vector3 = swing["left"]
	cam.position = sb + sleft * 20.0 + Vector3(0, 5.5, 0)
	cam.look_at(sb + Vector3(0, 4.5, 0))
	for k in range(4):
		await _shot("swing_t%d.png" % k)
		await _wait(0.75)
	var m0: float = (merry["node"] as Node3D).rotation.y
	await _wait(2.0)
	var m1: float = (merry["node"] as Node3D).rotation.y
	print("MERRY|rotation.y delta over 2s = %.2f rad (expect ~1.80)" % absf(m1 - m0))
	print("=== DONE ===")
	quit()
