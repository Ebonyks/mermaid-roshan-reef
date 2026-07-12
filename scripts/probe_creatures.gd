extends SceneTree
# Craft-creature idle animation verification: spawns Fishy / rainbow Fishy /
# Kitty / Birdie in open water and captures a time series to show motion.

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/9cd01dfa-2251-46bc-b596-91d73214aec8/scratchpad/creature_anim"

var cam: Camera3D

func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame

func _shot(name: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + "/" + name + ".png")
	print("saved ", name)

func _init() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.is_night = false
	main._apply_time_of_day()
	# spawn the three hand-drawn creatures in a row, well above the seabed
	var fish: Node3D = main._make_creature_node("fish", Color(0.4, 0.7, 1.0), Color(1.0, 0.6, 0.2))
	var fish_rb: Node3D = main._make_creature_node("fish", Color(1, 1, 1), Color(1.0, 0.9, 0.3), true, false)
	var cat: Node3D = main._make_creature_node("cat", Color(0.95, 0.7, 0.85), Color(0.6, 0.4, 0.9))
	var bird: Node3D = main._make_creature_node("bird", Color(1.0, 0.85, 0.3), Color(0.3, 0.8, 0.9))
	var xs := [-21.0, -7.0, 7.0, 21.0]
	var row := [fish, fish_rb, cat, bird]
	for i in range(4):
		var n: Node3D = row[i]
		n.position = Vector3(xs[i], 34.0, 0.0)
		main.add_child(n)
	cam = Camera3D.new()
	cam.fov = 70.0
	get_root().add_child(cam)
	cam.current = true
	cam.position = Vector3(0, 34, 38)
	cam.look_at(Vector3(0, 34, 0), Vector3.UP)
	await _settle(20)
	for s in range(6):
		await _shot("t%d" % s)
		await _settle(30)   # ~0.5 s of tween time between frames
	quit()
