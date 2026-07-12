extends SceneTree
# gen2 aquatic verification: lineup of rigged swimmers (texture + orientation +
# animation over time), bottom dwellers, and a top-down heading check of the
# mover fix (nose must align with the circle tangent).

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/9cd01dfa-2251-46bc-b596-91d73214aec8/scratchpad/aquatic2_check"

var cam: Camera3D

func _settle(frames: int) -> void:
	for i in range(frames):
		await process_frame

func _shot(name: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	get_root().get_viewport().get_texture().get_image().save_png(OUT + "/" + name + ".png")
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
	cam = Camera3D.new()
	cam.fov = 62.0
	get_root().add_child(cam)
	cam.current = true
	# row 1: swimmers at y=46
	var row1 := ["Shark", "Hammerhead", "Whale", "Dolphin", "Turtle", "StingRay", "ClownFish", "Squid"]
	var scls := [4.0, 4.0, 9.0, 2.6, 1.6, 2.4, 1.8, 2.0]
	for i in range(row1.size()):
		var inst: Node3D = main._place_aq(row1[i], Vector3(-70.0 + i * 20.0, 46.0, 0.0), scls[i], true)
		if inst != null:
			inst.rotation.y = 0.0
	# row 2: bottom dwellers on a shelf below
	var row2 := ["Octopus", "Crab", "Lobster"]
	for i in range(row2.size()):
		var inst2: Node3D = main._place_aq(row2[i], Vector3(-20.0 + i * 16.0, 30.0, 4.0), 2.2, true)
		if inst2 != null:
			inst2.rotation.y = 0.0
	await _settle(25)
	# three time samples of the lineup (front = -Z side... models face +Z so
	# shoot from +Z to see faces)
	cam.position = Vector3(0, 47, 60)
	cam.look_at(Vector3(0, 44, 0), Vector3.UP)
	for s in range(3):
		await _shot("lineup_t%d" % s)
		await _settle(25)
	# closeups: shark + stingray + whale
	cam.position = Vector3(-70, 48, 22)
	cam.look_at(Vector3(-70, 46, 0), Vector3.UP)
	await _shot("close_shark_a")
	await _settle(16)
	await _shot("close_shark_b")
	cam.position = Vector3(30, 48, 20)
	cam.look_at(Vector3(30, 46, 0), Vector3.UP)
	await _shot("close_stingray_a")
	await _settle(20)
	await _shot("close_stingray_b")
	cam.position = Vector3(-20, 34, 18)
	cam.look_at(Vector3(-14, 30, 4), Vector3.UP)
	await _shot("close_bottom_a")
	await _settle(20)
	await _shot("close_bottom_b")
	# heading check: one dolphin on a fast mover circle, top-down
	var dol: Node3D = main._place_aq("Dolphin", Vector3.ZERO, 2.6, true)
	main.aquatic_movers.append({"node": dol, "rad": 25.0, "spd": 0.5, "y": 55.0, "ph": 0.0})
	cam.position = Vector3(0, 110, 0.1)
	cam.look_at(Vector3(0, 55, 0), Vector3.UP)
	await _settle(10)
	await _shot("heading_t0")
	await _settle(30)
	await _shot("heading_t1")
	await _settle(30)
	await _shot("heading_t2")
	quit()
