extends SceneTree
# QA for the dev-mode Animation Lab: panel builds, verbs fire from it,
# soak loop advances, serpentine drives motion. Screenshots for the record.
const OUT := "res://probe_shots/"

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	var dm: Node = main.dev_mode
	print("PROBE dev_mode=", dm != null)
	dm.toggle()
	await process_frame
	await _shot("lab_panel.png")
	# fire a verb through the lab helper
	dm._play_lab_verb("cheer")
	for i in range(66):
		await process_frame
	await _shot("lab_cheer.png")
	# soak loop
	dm.anim_loop = true
	var seen := {}
	for i in range(600):
		if String(main.player.verb) != "":
			seen[String(main.player.verb)] = true
		await process_frame
	print("PROBE soak verbs seen: ", seen.keys())
	dm.anim_loop = false
	# serpentine stress
	dm.anim_serpentine = true
	for i in range(120):
		await process_frame
	await _shot("lab_serpentine.png")
	dm.anim_serpentine = false
	print("PROBE done")
	quit()

func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + name)
	print("shot ", name)
