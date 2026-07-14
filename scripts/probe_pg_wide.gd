extends SceneTree
# Wide shots of the playground meadow + east river for flood checking. Dev-only.

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/22c09d23-46ce-44d9-974a-d6891729ae81/scratchpad/pgwide"

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
	var o: Vector3 = main.LEVEL2_POS
	cam = Camera3D.new()
	cam.fov = 55.0
	get_root().add_child(cam)
	cam.make_current()
	# the user's angle: low south of the merry looking north over the playground
	await _shot(o + Vector3(45, 9, 155), o + Vector3(75, 2, 90), "pg_user_angle.png")
	# high oblique over the whole east meadow + river
	await _shot(o + Vector3(120, 55, 170), o + Vector3(80, 0, 90), "pg_high.png")
	# down the river channel at the old hump (76,136)
	await _shot(o + Vector3(40, 12, 130), o + Vector3(90, -2, 128), "pg_river.png")
	print("=== DONE ===")
	quit()
