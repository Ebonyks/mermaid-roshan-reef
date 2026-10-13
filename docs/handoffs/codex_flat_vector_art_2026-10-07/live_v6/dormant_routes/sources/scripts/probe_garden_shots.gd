extends SceneTree
# Visual probe for the garden minigame layout rework: captures the seed,
# sprout, and flower stages so scaling/overlap can be eyeballed at real
# render resolution. Run WITHOUT --headless (needs a viewport texture):
#   Godot_console.exe --path . --resolution 1920x1080 -s res://scripts/probe_garden_shots.gd
var out_dir: String = OS.get_environment("GARDEN_SHOT_DIR")


func _shot(name: String) -> void:
	for _i in range(4):
		await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(out_dir.path_join(name))
	print("saved ", name)


func _init() -> void:
	if out_dir == "":
		out_dir = OS.get_user_data_dir()
	var ms: PackedScene = load("res://scenes/main.tscn")
	var main: Node = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._mg2d_open("garden")
	await _shot("garden_stage_seed.png")
	var btns: Array = main.mg.get("btns", [])
	for b in btns:
		if is_instance_valid(b) and not b.disabled:
			b.pressed.emit()
	await _shot("garden_stage_sprout.png")
	# grow pots 3..5 to full flowers, leave 1-2 as sprouts for a mixed shot
	var i := 0
	for b in btns:
		if is_instance_valid(b) and not b.disabled and i >= 2:
			b.pressed.emit()
		i += 1
	await _shot("garden_stage_mixed.png")
	for b in btns:
		if is_instance_valid(b) and not b.disabled:
			b.pressed.emit()
	await _shot("garden_stage_flowers.png")
	quit()
