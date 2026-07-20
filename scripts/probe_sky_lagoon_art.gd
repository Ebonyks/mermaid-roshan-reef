extends SceneTree

# Fixed Mobile-render review set for the complete Sky Lagoon presentation.
# Set SKY_LAGOON_SHOT_OUT to an absolute output folder in CI.

var cam: Camera3D
var main: ReefMain
var out_dir := ""


func _settle(frames: int) -> void:
	for frame_index in range(frames):
		await process_frame


func _shot(name: String, pos: Vector3, target: Vector3, fov: float = 62.0) -> void:
	cam.fov = fov
	cam.global_position = pos
	cam.look_at(target, Vector3.UP)
	await _settle(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var error: Error = image.save_png(out_dir.path_join(name + ".png"))
	print("LAGOONSHOT|", name, "|", "OK" if error == OK else "FAIL")


func _find_meta(key: String, value: String, occurrence: int = 0) -> Node3D:
	var stack: Array[Node] = [main]
	var found_count := 0
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		if node is Node3D and node.has_meta(key) and String(node.get_meta(key)) == value:
			if found_count == occurrence:
				return node as Node3D
			found_count += 1
		for child: Node in node.get_children():
			stack.append(child)
	return null


func _shot_role(name: String, role: String, offset: Vector3, target_offset: Vector3,
	fov: float = 56.0, occurrence: int = 0) -> void:
	var node: Node3D = _find_meta("lagoon_art_role", role, occurrence)
	if node == null:
		print("LAGOONSHOT|", name, "|FAIL missing role ", role)
		return
	await _shot(name, node.global_position + offset,
		node.global_position + target_offset, fov)


func _init() -> void:
	var requested: String = OS.get_environment("SKY_LAGOON_SHOT_OUT")
	out_dir = requested if requested != "" else ProjectSettings.globalize_path(
		"res://tmp/sky_lagoon_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	if main.intro_active:
		main._skip_intro()
	main.galaxy_unlocked = true
	main.l2_star_progress = [false, false, false]
	main._enter_level2()
	await _settle(40)
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.touch_ui != null:
		main.touch_ui.visible = false
	if main.pause_layer != null:
		main.pause_layer.visible = false
	cam = Camera3D.new()
	cam.far = 800.0
	get_root().add_child(cam)
	cam.current = true
	await _settle(6)

	var o: Vector3 = main.LEVEL2_POS
	await _shot("lagoon_01_arrival_path", o + Vector3(54, 25, 182),
		o + Vector3(0, 7, 98), 66.0)
	await _shot_role("lagoon_02_memory_frame", "lagoon_memory_frame",
		Vector3(18, 2, 0), Vector3(0, 0, 0), 53.0, 1)
	await _shot_role("lagoon_03_complete_baby_plant", "lagoon_baby_rosette",
		Vector3(7, 4, 9), Vector3(0, 1, 0), 49.0)
	await _shot_role("lagoon_04_developed_shrub", "lagoon_meadow_shrub",
		Vector3(8, 5, 11), Vector3(0, 1.5, 0), 50.0)
	await _shot_role("lagoon_05_rooted_pond_reeds", "lagoon_pond_reeds",
		Vector3(9, 5, 12), Vector3(0, 1.5, 0), 52.0, 2)
	await _shot_role("lagoon_06_riverbank_stones", "lagoon_river_stones",
		Vector3(12, 6, 14), Vector3(0, 0.5, 0), 55.0, 2)
	await _shot("lagoon_07_fairy_pond", main.fairy_pond_pos + Vector3(24, 13, 26),
		main.fairy_pond_pos + Vector3(0, -2, 0), 62.0)
	await _shot("lagoon_08_playground", o + Vector3(120, 36, 125),
		o + Vector3(74, 7, 92), 64.0)
	await _shot("lagoon_09_rainbow_race_gate", main.kart_legA + Vector3(0, 5, 20),
		main.kart_legA + Vector3(0, 3, 0), 54.0)
	await _shot("lagoon_10_butterfly_world_gate", main.bw_portal_pos + Vector3(0, 4, 34),
		main.bw_portal_pos + Vector3(0, 1, 0), 55.0)
	await _shot("lagoon_11_castle_facade", o + Vector3(0, 26, -42),
		o + Vector3(0, 30, -120), 62.0)
	var cloud: Node3D = _find_meta("landmark_art", "storybook_cloud", 1)
	if cloud != null:
		await _shot("lagoon_12_cloud_family", cloud.global_position + Vector3(22, 5, 32),
			cloud.global_position, 54.0)
	else:
		print("LAGOONSHOT|lagoon_12_cloud_family|FAIL missing cloud")
	await _shot("lagoon_13_alpine_edge", o + Vector3(-25, 30, -112),
		o + Vector3(-96, 8, -180), 64.0)
	await _shot_role("lagoon_14_train_station", "lagoon_train_station",
		Vector3(0, 5, 18), Vector3(0, 2.5, 0), 58.0)
	print("LAGOONSHOT|DONE|", out_dir)
	quit()
