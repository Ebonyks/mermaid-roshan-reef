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


func _shot_node_local(name: String, node: Node3D, local_offset: Vector3,
	local_target: Vector3, fov: float = 56.0) -> void:
	if node == null or not is_instance_valid(node):
		print("LAGOONSHOT|", name, "|FAIL missing node")
		return
	await _shot(name, node.to_global(local_offset), node.to_global(local_target), fov)


func _train_car(index: int) -> Node3D:
	var train_state: Dictionary = main.g.get("train", {})
	var cars: Array = train_state.get("cars", [])
	if index < 0 or index >= cars.size():
		return null
	var car_data: Dictionary = cars[index]
	return car_data.get("node") as Node3D


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
	# Speedy is the phone default and therefore the binding presentation tier.
	main._apply_quality("speedy")
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
	await _shot("lagoon_02_meadow_overview", o + Vector3(0, 105, 105),
		o + Vector3(0, 3, 0), 72.0)
	await _shot_role("lagoon_03_memory_frame", "lagoon_memory_frame",
		Vector3(18, 2, 0), Vector3(0, 0, 0), 53.0, 1)
	await _shot_role("lagoon_04_complete_baby_plant", "lagoon_baby_rosette",
		Vector3(7, 4, 9), Vector3(0, 1, 0), 49.0)
	await _shot_role("lagoon_05_developed_shrub", "lagoon_meadow_shrub",
		Vector3(8, 5, 11), Vector3(0, 1.5, 0), 50.0)
	await _shot_role("lagoon_06_flower_cluster_coral", "lagoon_flower_cluster_coral",
		Vector3(8, 5, 10), Vector3(0, 1.2, 0), 49.0)
	await _shot_role("lagoon_07_flower_cluster_lavender", "lagoon_flower_cluster_lavender",
		Vector3(8, 5, 10), Vector3(0, 1.2, 0), 49.0)
	await _shot_role("lagoon_08_mushroom_cluster", "lagoon_mushroom_cluster",
		Vector3(7, 4, 9), Vector3(0, 1.0, 0), 48.0)
	await _shot_role("lagoon_09_rooted_pond_reeds", "lagoon_pond_reeds",
		Vector3(9, 5, 12), Vector3(0, 1.5, 0), 52.0, 2)
	await _shot_role("lagoon_10_riverbank_stones", "lagoon_river_stones",
		Vector3(12, 6, 14), Vector3(0, 0.5, 0), 55.0, 2)
	await _shot("lagoon_11_fairy_pond_near", main.fairy_pond_pos + Vector3(24, 13, 26),
		main.fairy_pond_pos + Vector3(0, -2, 0), 62.0)
	await _shot("lagoon_12_fairy_pond_context", main.fairy_pond_pos + Vector3(-34, 24, 38),
		main.fairy_pond_pos + Vector3(0, 0, 0), 68.0)
	await _shot("lagoon_13_playground", o + Vector3(120, 36, 125),
		o + Vector3(74, 7, 92), 64.0)
	await _shot("lagoon_14_rainbow_race_gate_a", main.kart_legA + Vector3(0, 5, 20),
		main.kart_legA + Vector3(0, 3, 0), 54.0)
	await _shot("lagoon_15_rainbow_race_gate_b", main.kart_legB + Vector3(0, 5, 20),
		main.kart_legB + Vector3(0, 3, 0), 54.0)
	await _shot("lagoon_16_butterfly_world_gate", main.bw_portal_pos + Vector3(0, 4, 34),
		main.bw_portal_pos + Vector3(0, 1, 0), 55.0)
	await _shot("lagoon_17_castle_approach", o + Vector3(0, 26, -42),
		o + Vector3(0, 30, -120), 62.0)
	await _shot("lagoon_18_castle_bridge", o + Vector3(25, 13, -62),
		o + Vector3(0, 5, -82), 58.0)
	await _shot("lagoon_19_castle_three_quarter", o + Vector3(78, 40, -66),
		o + Vector3(0, 27, -120), 63.0)
	var cloud: Node3D = _find_meta("landmark_art", "storybook_cloud", 1)
	if cloud != null:
		await _shot("lagoon_20_cloud_family", cloud.global_position + Vector3(22, 5, 32),
			cloud.global_position, 54.0)
	else:
		print("LAGOONSHOT|lagoon_20_cloud_family|FAIL missing cloud")
	await _shot_role("lagoon_21_train_station", "lagoon_train_station",
		Vector3(0, 5, 18), Vector3(0, 2.5, 0), 58.0)
	var engine: Node3D = _train_car(0)
	var tender: Node3D = _train_car(1)
	var coach: Node3D = _train_car(2)
	var gondola: Node3D = _train_car(3)
	var caboose: Node3D = _train_car(4)
	await _shot_node_local("lagoon_22_train_consist", coach, Vector3(24, 12, 15),
		Vector3(0, 3.8, 0), 64.0)
	await _shot_node_local("lagoon_23_train_locomotive", engine, Vector3(15, 7, 13),
		Vector3(0, 3.8, 0), 55.0)
	await _shot_node_local("lagoon_24_train_tender", tender, Vector3(12, 6, 9),
		Vector3(0, 3.0, 0), 52.0)
	await _shot_node_local("lagoon_25_train_coach", coach, Vector3(14, 8, 9),
		Vector3(0, 4.5, 0), 54.0)
	await _shot_node_local("lagoon_26_train_gondola", gondola, Vector3(12, 6, 9),
		Vector3(0, 3.0, 0), 52.0)
	await _shot_node_local("lagoon_27_train_caboose", caboose, Vector3(13, 7, 10),
		Vector3(0, 4.0, 0), 53.0)
	if engine != null:
		await _shot("lagoon_28_track_ties_and_rails", engine.global_position + Vector3(8, 3, 18),
			engine.global_position + Vector3(0, 0.2, 7), 50.0)
	await _shot("lagoon_29_alpine_overview", o + Vector3(-30, 40, -226),
		o + Vector3(-96, 10, -180), 64.0)
	var house_entries: Array = main.g.get("alpine_house_entries", [])
	if not house_entries.is_empty():
		var house_a: Dictionary = house_entries[0]
		var house_entry: Vector3 = house_a.get("entry", Vector3.ZERO)
		await _shot("lagoon_30_alpine_chalet", house_entry + Vector3(18, 9, 20),
			house_entry + Vector3(0, 5, -2), 58.0)
	else:
		print("LAGOONSHOT|lagoon_30_alpine_chalet|FAIL missing house entry")
	var village_center: Vector3 = main.g.get("alpine_village_center", o)
	await _shot("lagoon_31_alpine_village", village_center + Vector3(36, 24, 38),
		village_center + Vector3(-6, 5, -4), 64.0)
	var cave_entrance: Vector3 = main.g.get("alpine_cave_entrance", o)
	await _shot("lagoon_32_alpine_cave", cave_entrance + Vector3(20, 8, 1),
		cave_entrance + Vector3(-6, 2, 0), 56.0)
	await _shot("lagoon_33_alpine_pines", o + Vector3(-34, 18, -213),
		o + Vector3(-68, 7, -188), 58.0)
	var opera_gate: Dictionary = main.g.get("opera_gate", {})
	var opera_node: Node3D = opera_gate.get("node") as Node3D
	await _shot_node_local("lagoon_34_opera_courtyard_gate", opera_node,
		Vector3(0, 8, 22), Vector3(0, 6, 0), 56.0)
	await _shot_role("lagoon_35_story_lantern", "lagoon_story_lantern",
		Vector3(8, 5, 10), Vector3(0, 2.5, 0), 49.0, 1)
	# A smaller Sparkly comparison set catches quality-toggle exposure drift while
	# keeping the complete phone-default review above as the primary artifact.
	main._apply_quality("sparkly")
	await _settle(6)
	await _shot("lagoon_36_sparkly_arrival", o + Vector3(54, 25, 182),
		o + Vector3(0, 7, 98), 66.0)
	await _shot("lagoon_37_sparkly_fairy_pond", main.fairy_pond_pos + Vector3(24, 13, 26),
		main.fairy_pond_pos + Vector3(0, -2, 0), 62.0)
	await _shot("lagoon_38_sparkly_castle", o + Vector3(0, 26, -42),
		o + Vector3(0, 30, -120), 62.0)
	print("LAGOONSHOT|DONE|", out_dir)
	quit()
