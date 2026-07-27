extends SceneTree
# The 3D courtyard train retired with the 2.5D Sky Lagoon conversion. This
# probe now guards the replacement promenade's assisted traversal and cleanup.

func _frames(count: int) -> void:
	for _i in range(count):
		await process_frame

func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = scene.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for friend_value in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main._enter_level2()
	await _frames(4)
	var phase_ok: bool = String(main.g.get("phase", "")) == "promenade"
	print("TRAIN|2.5D promenade replaces courtyard train: ",
		"OK" if phase_ok else "FAIL")
	var start_x: float = main.player.position.x
	main.g["ss_walk_goal"] = Vector2(0.0, 0.0)
	for _i in range(150):
		main._lagoon_promenade_ref().tick(1.0 / 60.0)
	var travelled: float = main.player.position.x - start_x
	var travel_ok: bool = travelled > 20.0
	print("TRAIN|assisted promenade crossing moved %.1f: %s" % [
		travelled, "OK" if travel_ok else "FAIL"])
	var old_root: Node3D = main.g.get("ss_root") as Node3D
	main._enter_castle_interior()
	await _frames(8)
	var cleanup_ok: bool = not is_instance_valid(old_root) \
		and String(main.g.get("phase", "")) == "hall"
	print("TRAIN|promenade clears on castle entry: ",
		"OK" if cleanup_ok else "FAIL")
	main._enter_level2(true)
	await _frames(8)
	var rebuild_ok: bool = String(main.g.get("phase", "")) == "promenade" \
		and (main.g.get("lagoon_promenade_targets", []) as Array).size() == 8
	print("TRAIN|promenade rebuilds at screen three: ",
		"OK" if rebuild_ok else "FAIL")
	if not (phase_ok and travel_ok and cleanup_ok and rebuild_ok):
		print("FAIL|Sky Lagoon promenade traversal regression")
	print("=== TRAIN PROBE DONE ===")
	quit()
