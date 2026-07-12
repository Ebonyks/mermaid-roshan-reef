extends SceneTree
# Verb + galaxy-avatar QA on the v3 rig: screenshot each gesture at its peak.
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
	print("PROBE v3=", player.model_v3)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	for i in range(30):
		await process_frame
	for vname in ["cheer", "wave", "clap", "twirl", "look", "sleep"]:
		player.play_verb(vname)
		var vlen: float = player.VERB_LIB[vname]["len"]
		var mid_frames: int = int(vlen * 0.5 * 60.0)
		for i in range(mid_frames):
			_front_cam(player)
			await process_frame
		await _shot("verb_%s.png" % vname)
		var rest_frames: int = int(vlen * 0.6 * 60.0) + 20
		for i in range(rest_frames):
			_front_cam(player)
			await process_frame
	# galaxy avatar check
	main._start_galaxy()
	for i in range(90):
		await process_frame
	await _shot("galaxy_avatar.png")
	print("PROBE done")
	quit()

func _front_cam(player: Node3D) -> void:
	if player.cam != null and player.cam.is_inside_tree():
		var fwd := Vector3(sin(player.yaw), 0, cos(player.yaw))
		player.cam.position = player.position + fwd * 14.0 + Vector3(0, 2.5, 0)
		player.cam.look_at(player.position + Vector3(0, 1.5, 0))

func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + name)
	print("shot ", name)
