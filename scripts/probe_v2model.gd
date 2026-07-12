extends SceneTree
# Visual QA for roshan_v2.glb: idle, swim, and turn shots from the chase cam.
# Run:  Godot_console.exe --path . --resolution 1600x900 -s res://scripts/probe_v2model.gd
const OUT := "res://../meshy_rebuild/shots/"

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	var player: Node3D = main.player
	print("PROBE model_v2=", player.model_v2, " skel=", player.skel != null,
		" hair_sim=", player.hair_sim != null)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	# settle: let the camera lerp into place
	for i in range(40):
		await process_frame
	await _shot("v2_idle.png")
	# swim forward ~3s, shots across the cycle
	for i in range(60):
		player.vel = Vector3(sin(player.yaw), 0, cos(player.yaw)) * 20.0
		await process_frame
	await _shot("v2_swim_a.png")
	for i in range(20):
		player.vel = Vector3(sin(player.yaw), 0, cos(player.yaw)) * 20.0
		await process_frame
	await _shot("v2_swim_b.png")
	for i in range(20):
		player.vel = Vector3(sin(player.yaw), 0, cos(player.yaw)) * 20.0
		await process_frame
	await _shot("v2_swim_c.png")
	# turn in place: shows her side to the camera briefly
	for i in range(50):
		player.yaw += 0.05
		await process_frame
	await _shot("v2_turn.png")
	print("PROBE done")
	quit()

func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + name)
	print("shot ", name)
