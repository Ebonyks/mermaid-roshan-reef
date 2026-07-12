extends SceneTree
# Facing convention ground truth: place Riley creatures via the game's own
# _place_aq at rotation.y = 0 and photograph from +X and -Z.

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/9cd01dfa-2251-46bc-b596-91d73214aec8/scratchpad/aquatic_survey"

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
	var cam := Camera3D.new()
	cam.fov = 60.0
	get_root().add_child(cam)
	cam.current = true
	var specs := [["Dolphin", 2.6, 16.0], ["Shark", 4.0, 26.0], ["ClownFish", 1.8, 8.0], ["Turtle", 1.6, 8.0]]
	for i in range(specs.size()):
		var nm: String = specs[i][0]
		var scl: float = specs[i][1]
		var r: float = specs[i][2]
		var pos := Vector3(0, 60, 0)
		var inst: Node3D = main._place_aq(nm, pos, scl, false)
		inst.rotation.y = 0.0
		for f in range(8):
			await process_frame
		cam.position = pos + Vector3(r, r * 0.2, 0)
		cam.look_at(pos, Vector3.UP)
		await process_frame
		await RenderingServer.frame_post_draw
		get_root().get_viewport().get_texture().get_image().save_png(OUT + "/g2_" + nm + "_fromX.png")
		cam.position = pos + Vector3(0, r * 0.2, -r)
		cam.look_at(pos, Vector3.UP)
		await process_frame
		await RenderingServer.frame_post_draw
		get_root().get_viewport().get_texture().get_image().save_png(OUT + "/g2_" + nm + "_fromNegZ.png")
		print("shot ", nm)
		inst.position = Vector3(0, -500, 0)
	quit()
