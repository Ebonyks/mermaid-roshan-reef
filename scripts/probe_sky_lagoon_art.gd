extends SceneTree

# Fixed Mobile-render review set for the complete Sky Lagoon presentation.
# Set SKY_LAGOON_SHOT_OUT to an absolute output folder in CI.

var cam: Camera3D
var main: ReefMain
var out_dir := ""

const REVIEW_TREE_ROLES := [
	"lagoon_tree_douglas_fir",
	"lagoon_tree_western_redcedar",
	"lagoon_tree_western_hemlock",
	"lagoon_tree_sitka_spruce",
	"lagoon_tree_shore_pine",
	"lagoon_tree_pacific_yew",
	"lagoon_tree_bigleaf_maple",
	"lagoon_tree_red_alder",
	"lagoon_tree_black_cottonwood",
	"lagoon_tree_pacific_madrone",
	"lagoon_tree_garry_oak",
	"lagoon_tree_pacific_dogwood",
]


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


func _find_review_role(role: String, occurrence: int = 0,
	prefer_anchor: bool = false) -> Node3D:
	if prefer_anchor:
		var stack: Array[Node] = [main]
		while not stack.is_empty():
			var node: Node = stack.pop_back()
			if (node is Node3D and node.has_meta("lagoon_art_role")
					and String(node.get_meta("lagoon_art_role")) == role
					and bool(node.get_meta("lagoon_art_review_anchor", false))):
				return node as Node3D
			for child: Node in node.get_children():
				stack.append(child)
	return _find_meta("lagoon_art_role", role, occurrence)


func _visual_bounds(node: Node3D) -> AABB:
	var stack: Array[Node] = [node]
	var has_point := false
	var minimum := Vector3.ZERO
	var maximum := Vector3.ZERO
	while not stack.is_empty():
		var current: Node = stack.pop_back()
		if current is MeshInstance3D:
			var mesh_instance := current as MeshInstance3D
			if mesh_instance.mesh != null and mesh_instance.is_visible_in_tree():
				var local_bounds: AABB = mesh_instance.get_aabb()
				for endpoint_index in range(8):
					var point: Vector3 = mesh_instance.global_transform * local_bounds.get_endpoint(endpoint_index)
					if not has_point:
						minimum = point
						maximum = point
						has_point = true
					else:
						minimum = minimum.min(point)
						maximum = maximum.max(point)
		for child: Node in current.get_children():
			stack.append(child)
	if not has_point:
		return AABB(node.global_position - Vector3.ONE, Vector3.ONE * 2.0)
	return AABB(minimum, maximum - minimum)


func _hide_tree_audit_occluders(target: Node3D) -> Array[Node3D]:
	var hidden: Array[Node3D] = []
	var stack: Array[Node] = [main]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		if node is Node3D:
			var node_3d := node as Node3D
			var is_other_tree: bool = (node_3d != target
				and node_3d.has_meta("lagoon_art_role")
				and String(node_3d.get_meta("lagoon_art_role")) in REVIEW_TREE_ROLES)
			var is_smoke: bool = node_3d is GPUParticles3D or node_3d is CPUParticles3D
			if (is_other_tree or is_smoke) and node_3d.visible:
				node_3d.visible = false
				hidden.append(node_3d)
		for child: Node in node.get_children():
			stack.append(child)
	return hidden


func _restore_hidden(nodes: Array[Node3D]) -> void:
	for node: Node3D in nodes:
		if is_instance_valid(node):
			node.visible = true


func _shot_role(name: String, role: String, offset: Vector3, target_offset: Vector3,
	fov: float = 56.0, occurrence: int = 0) -> void:
	var node: Node3D = _find_meta("lagoon_art_role", role, occurrence)
	if node == null:
		print("LAGOONSHOT|", name, "|FAIL missing role ", role)
		return
	await _shot(name, node.global_position + offset,
		node.global_position + target_offset, fov)


func _shot_role_framed(name: String, role: String, view_direction: Vector3,
	fov: float = 50.0, occurrence: int = 0, prefer_anchor: bool = false,
	is_tree: bool = false) -> void:
	var node: Node3D = _find_review_role(role, occurrence, prefer_anchor)
	if node == null:
		print("LAGOONSHOT|", name, "|FAIL missing role ", role)
		return
	var hidden: Array[Node3D] = []
	if is_tree:
		hidden = _hide_tree_audit_occluders(node)
	await _settle(2)
	var bounds: AABB = _visual_bounds(node)
	var center: Vector3 = bounds.get_center()
	var horizontal_half: float = maxf(maxf(bounds.size.x, bounds.size.z) * 0.5, 0.65)
	var vertical_half: float = maxf(bounds.size.y * 0.5, 0.65)
	var frame_radius: float = sqrt(horizontal_half * horizontal_half
		+ vertical_half * vertical_half)
	var distance: float = maxf(3.2,
		frame_radius / tan(deg_to_rad(fov * 0.5)) * 1.28)
	var direction: Vector3 = view_direction.normalized()
	await _shot(name, center + direction * distance, center, fov)
	_restore_hidden(hidden)


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
	# Save-state time of day varies on developer machines and previously turned
	# the full evidence set into a night-only review. Force the binding family
	# views to daylight so grass-level silhouettes and palette separation remain
	# scoreable; dedicated comparison frames still cover the alternate tier.
	main._set_night(false)
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
	await _shot_role_framed("lagoon_04_complete_baby_plant", "lagoon_baby_rosette",
		Vector3(1.2, 0.72, 1.45), 47.0, 0, true)
	await _shot_role_framed("lagoon_05a_shrub_salal", "lagoon_shrub_salal",
		Vector3(1.2, 0.62, 1.45), 48.0, 0, true)
	await _shot_role_framed("lagoon_05b_shrub_oregon_grape", "lagoon_shrub_oregon_grape",
		Vector3(1.2, 0.62, 1.45), 48.0, 0, true)
	await _shot_role_framed("lagoon_05c_shrub_red_flowering_currant",
		"lagoon_shrub_red_flowering_currant", Vector3(1.2, 0.62, 1.45), 48.0, 0, true)
	await _shot_role_framed("lagoon_05d_shrub_oceanspray", "lagoon_shrub_oceanspray",
		Vector3(1.2, 0.62, 1.45), 48.0, 0, true)
	await _shot_role_framed("lagoon_05e_shrub_salmonberry", "lagoon_shrub_salmonberry",
		Vector3(1.2, 0.62, 1.45), 48.0, 0, true)
	await _shot_role_framed("lagoon_05f_shrub_evergreen_huckleberry",
		"lagoon_shrub_evergreen_huckleberry", Vector3(1.2, 0.62, 1.45), 48.0, 0, true)
	await _shot_role_framed("lagoon_06_flower_cluster_coral", "lagoon_flower_cluster_coral",
		Vector3(1.2, 0.72, 1.45), 47.0, 0, true)
	await _shot_role_framed("lagoon_07_flower_cluster_lavender", "lagoon_flower_cluster_lavender",
		Vector3(1.2, 0.72, 1.45), 47.0, 0, true)
	await _shot_role_framed("lagoon_08_mushroom_cluster", "lagoon_mushroom_cluster",
		Vector3(1.2, 0.68, 1.45), 47.0, 0, true)
	await _shot_role_framed("lagoon_09_rooted_pond_reeds", "lagoon_pond_reeds",
		Vector3(1.2, 0.56, 1.45), 49.0, 0, true)
	await _shot_role_framed("lagoon_10_riverbank_stones", "lagoon_river_stones",
		Vector3(1.2, 0.72, 1.45), 51.0, 0, true)
	await _shot("lagoon_11_fairy_pond_near", main.fairy_pond_pos + Vector3(24, 13, 26),
		main.fairy_pond_pos + Vector3(0, -2, 0), 62.0)
	await _shot("lagoon_12_fairy_pond_context", main.fairy_pond_pos + Vector3(-34, 24, 38),
		main.fairy_pond_pos + Vector3(0, 0, 0), 68.0)
	await _shot("lagoon_13_playground", o + Vector3(120, 36, 125),
		o + Vector3(74, 7, 92), 64.0)
	await _shot_role_framed("lagoon_14_rainbow_race_gate_a", "lagoon_rainbow_race_arch",
		Vector3(0.35, 0.40, 1.35), 49.0, 0)
	await _shot_role_framed("lagoon_15_rainbow_race_gate_b", "lagoon_rainbow_race_arch",
		Vector3(-1.20, 0.42, -1.25), 49.0, 1)
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
	# Every Seattle-area species receives its own fixed daylight review and must
	# remain individually legible by branch graph, crown profile, and signature cues.
	await _shot_role_framed("lagoon_36_tree_douglas_fir", "lagoon_tree_douglas_fir",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_37_tree_western_redcedar", "lagoon_tree_western_redcedar",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_38_tree_western_hemlock", "lagoon_tree_western_hemlock",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_39_tree_sitka_spruce", "lagoon_tree_sitka_spruce",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_40_tree_shore_pine", "lagoon_tree_shore_pine",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_41_tree_pacific_yew", "lagoon_tree_pacific_yew",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_42_tree_bigleaf_maple", "lagoon_tree_bigleaf_maple",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_43_tree_red_alder", "lagoon_tree_red_alder",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_44_tree_black_cottonwood", "lagoon_tree_black_cottonwood",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_45_tree_pacific_madrone", "lagoon_tree_pacific_madrone",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_46_tree_garry_oak", "lagoon_tree_garry_oak",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot_role_framed("lagoon_47_tree_pacific_dogwood", "lagoon_tree_pacific_dogwood",
		Vector3(1.25, 0.32, 1.45), 49.0, 0, true, true)
	await _shot("lagoon_48_roshan_stained_glass", o + Vector3(0, 42, -75),
		o + Vector3(0, 38, -106.95), 42.0)
	await _shot_role_framed("lagoon_52_ember_gateway", "lagoon_ember_gateway",
		Vector3(1.15, 0.18, 1.35), 50.0)
	# A smaller Sparkly comparison set catches quality-toggle exposure drift while
	# keeping the complete phone-default review above as the primary artifact.
	main._apply_quality("sparkly")
	await _settle(6)
	await _shot("lagoon_49_sparkly_arrival", o + Vector3(54, 25, 182),
		o + Vector3(0, 7, 98), 66.0)
	await _shot("lagoon_50_sparkly_fairy_pond", main.fairy_pond_pos + Vector3(24, 13, 26),
		main.fairy_pond_pos + Vector3(0, -2, 0), 62.0)
	await _shot("lagoon_51_sparkly_castle", o + Vector3(0, 26, -42),
		o + Vector3(0, 30, -120), 62.0)
	print("LAGOONSHOT|DONE|", out_dir)
	quit()
