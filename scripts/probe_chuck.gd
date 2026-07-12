extends SceneTree
const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/95e90298-f74a-40cb-b3b4-6e45745fdde0/scratchpad/"
var cam: Camera3D

func _shot(fname: String) -> void:
	await RenderingServer.frame_post_draw
	root.get_viewport().get_texture().get_image().save_png(OUT + fname)
	var main: Node = root.get_child(root.get_child_count() - 1)
	var ap: AnimationPlayer = main.g.get("chuck_ap")
	print("saved ", fname, "  anim=", ap.current_animation if ap != null else "none")

func _aim_at_chuck(main: Node) -> void:
	var chuck: Node3D = main.g["chuck"]
	cam.position = chuck.position + Vector3(4.5, 3.0, 6.0)
	cam.look_at(chuck.position + Vector3(0, 1.2, 0), Vector3.UP)

func _init() -> void:
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	var fr: Dictionary = {}
	for f in main.friends:
		if String(f["game"]) == "fetch":
			fr = f
	main._start_game(fr)
	await process_frame
	cam = Camera3D.new()
	main.add_child(cam)
	cam.make_current()
	# --- 1) sitting during aim ---
	for i in range(25):
		await process_frame
	_aim_at_chuck(main)
	await _shot("chuck_sit.png")
	# --- 2) running to the ball ---
	var ball: Node3D = main.g["ball"]
	ball.position = main.ARENA_POS + Vector3(-25.0, 0.9, 10.0)
	main.g["phase"] = "fetch"
	for i in range(14):
		await process_frame
		_aim_at_chuck(main)
	await _shot("chuck_run.png")
	# --- 3) returning with the ball ---
	var fcount := 0
	while String(main.g.get("phase", "?")) != "return" and fcount < 600:
		fcount += 1
		await process_frame
	for i in range(10):
		await process_frame
		_aim_at_chuck(main)
	await _shot("chuck_return.png")
	print("END phase=", main.g.get("phase"), " round=", main.g.get("round"))
	quit()
