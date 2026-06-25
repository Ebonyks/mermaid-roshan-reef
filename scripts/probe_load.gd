extends SceneTree
# verifies a saved session restores trophies/stars on boot
func _init() -> void:
	var ps: PackedScene = load("res://scenes/main.tscn")
	root.add_child(ps.instantiate())
	await process_frame
	await process_frame
	var main: Node = root.get_child(root.get_child_count() - 1)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	print("loaded trophies: ", main.trophies, "/5  finale_done: ", main.finale_done)
	var stars := 0
	for f in main.friends:
		if f.has("star"):
			stars += 1
	print("won stars shown: ", stars, "/5")
	quit()
