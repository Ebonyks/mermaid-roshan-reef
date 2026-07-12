extends SceneTree
# Texture-seam verification probe: captures the castle keep, cobble path,
# grand hall and basement after the world-triplanar + scale-unification pass
# so the nano-banana sheets can be checked for splicing by eye.
# Saves PNGs to OUT when run with a display; prints OK lines (ci.sh convention).

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/4b731d89-dcfc-4376-9e9b-a5171faf67ef/scratchpad/live_castle"

var main: Node
var cam: Camera3D

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _shot(name: String, pos: Vector3, look: Vector3) -> void:
	if DisplayServer.get_name() == "headless":
		return
	cam.position = pos
	cam.look_at(look, Vector3.UP)
	await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + "/" + name + ".png")
	print("TEXSEAM|shot ", name, ": OK")

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
	cam = Camera3D.new()
	cam.fov = 70.0
	get_root().add_child(cam)
	cam.current = true
	DirAccess.make_dir_recursive_absolute(OUT)
	main._enter_level2()
	await _frames(40)
	var o: Vector3 = main.LEVEL2_POS if "LEVEL2_POS" in main else main.arena_center
	var c: Vector3 = o + Vector3(0, 0, -120.0)
	await _shot("live_keep_facade", c + Vector3(0, 20, 90), c + Vector3(0, 30, 0))
	await _shot("live_keep_corner", c + Vector3(55, 30, 60), c + Vector3(0, 30, 0))
	await _shot("live_path", o + Vector3(8, 12, 60), o + Vector3(0, 0, -20))
	main._enter_castle_interior()
	await _frames(40)
	var h: Vector3 = main.CASTLE_POS
	await _shot("live_hall_entrance", h + Vector3(0, 10, 40), h + Vector3(0, 14, -20))
	await _shot("live_hall_walls", h + Vector3(-20, 20, 20), h + Vector3(35, 16, -10))
	await _shot("live_hall_floor", h + Vector3(0, 22, 15), h + Vector3(0, 0, 5))
	print("TEXSEAM|done: OK")
	quit()
