extends SceneTree
# Visual QA for roshan_v3.glb in the live repo: idle / swim / turn shots.
const OUT := "res://probe_shots/"

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	var player: Node3D = main.player
	print("PROBE model_v3=", player.model_v3, " skel=", player.skel != null,
		" hair_sim=", player.hair_sim != null)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	for i in range(40):
		await process_frame
	await _shot("v3_idle.png")
	for i in range(60):
		player.vel = Vector3(sin(player.yaw), 0, cos(player.yaw)) * 20.0
		await process_frame
	await _shot("v3_swim_a.png")
	for i in range(20):
		player.vel = Vector3(sin(player.yaw), 0, cos(player.yaw)) * 20.0
		await process_frame
	await _shot("v3_swim_b.png")
	for i in range(50):
		player.yaw += 0.05
		await process_frame
	await _shot("v3_turn.png")
	print("PROBE done")
	quit()

func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + name)
	print("shot ", name)
