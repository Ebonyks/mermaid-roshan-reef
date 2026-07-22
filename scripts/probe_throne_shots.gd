extends SceneTree
# Visual repro for the "camera inside pink prop at the throne" report:
# pose Roshan at Huluu / Crown Star height with several facings, let the REAL
# chase camera settle, and save what it sees. Non-headless (needs a window).

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/3e011fc6-58cb-4ec8-9ff9-def06c922d14/scratchpad/throne_shots"

var main: Node

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _settle_and_shoot(name: String, pos: Vector3, yaw: float) -> void:
	var player: Node3D = main.player
	player.position = main.CASTLE_POS + pos
	player.yaw = yaw
	player.vel = Vector3.ZERO
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < 1600:   # real chase glide, no snap
		player.vel = Vector3.ZERO
		await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + "/" + name + ".png")
	var cam: Camera3D = player.cam
	print("THRONE|%s cam=%s boom=%.2f" % [name, cam.position - main.CASTLE_POS,
			cam.position.distance_to(player.position + Vector3(0, 1.5, 0))])

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
	var tcut := Time.get_ticks_msec()
	while "l2_cutscene_t" in main and float(main.l2_cutscene_t) >= 0.0 \
			and Time.get_ticks_msec() - tcut < 30000:
		await process_frame
	main._enter_castle_interior()
	await _frames(30)
	# at Huluu facing the hall (+z): chase cam swings to -z, into the throne
	await _settle_and_shoot("huluu_facing_hall", Vector3(0, 21.0, -25.0), 0.0)
	# at Huluu facing the throne (-z): cam behind at +z, open hall
	await _settle_and_shoot("huluu_facing_throne", Vector3(0, 21.0, -25.0), PI)
	# drifting above the dais facing sideways
	await _settle_and_shoot("dais_side", Vector3(2.0, 18.5, -26.5), PI * 0.5)
	# mid royal stairs facing up
	await _settle_and_shoot("stairs_up", Vector3(0, 9.5, -16.0), PI)
	quit()
