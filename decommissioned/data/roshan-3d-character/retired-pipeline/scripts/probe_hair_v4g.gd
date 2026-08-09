extends SceneTree
# Visual QA for the v4g rainbow-hair repaint: rear (follow-cam), rear swim,
# and a free-camera front shot. Run:
#   godot --path . --script res://scripts/probe_hair_v4g.gd
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
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	for i in range(50):
		await process_frame
	await _shot("v4g_hair_rear_idle.png")
	for i in range(50):
		player.vel = Vector3(sin(player.yaw), 0, cos(player.yaw)) * 18.0
		await process_frame
	await _shot("v4g_hair_rear_swim.png")
	# free-camera closeups: rear and front of the head/swath
	var cam := Camera3D.new()
	get_root().add_child(cam)
	var fwd := Vector3(sin(player.yaw), 0, cos(player.yaw))
	var head := player.global_position + Vector3(0, 2.2, 0)
	cam.make_current()
	cam.global_position = head - fwd * 9.0 + Vector3(0, 0.8, 0)
	cam.look_at(head)
	for i in range(12):
		await process_frame
	await _shot("v4g_hair_rear_close.png")
	cam.global_position = head + fwd * 9.0 + Vector3(0, 0.8, 0)
	cam.look_at(head)
	for i in range(12):
		await process_frame
	await _shot("v4g_hair_front.png")
	print("PROBE done")
	quit()

func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + name)
	print("shot ", name)
