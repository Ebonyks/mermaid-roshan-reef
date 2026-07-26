extends SceneTree

# Structural and visual acceptance probe for the pearl-castle art pass. The
# headless run audits import budgets and live placement; Xvfb additionally
# emits fixed Mobile-render review frames.

const KIT_DIR := "res://assets/castle/pearl_kit/"
const ASSET_NAMES: Array[String] = [
	"pearl_column",
	"pearl_balustrade",
	"pearl_shell_arch",
	"pearl_rainbow_window",
	"pearl_shell_sconce",
	"pearl_shell_chandelier",
	"pearl_floor_medallion",
	"pearl_throne_canopy",
	"pearl_shell_throne",
	"pearl_shell_planter",
	"pearl_shell_bench",
	"pearl_cloud_settee",
	"pearl_cloud_pouf",
	"pearl_shell_fountain",
	"pearl_rainbow_gate",
	"pearl_shell_banner_a",
	"pearl_shell_banner_b",
	"pearl_stair_rail",
	"pearl_ocean_portal",
	"pearl_shell_window",
	"pearl_story_cushion",
	"pearl_toy_block_stack",
	"pearl_toy_chest",
	"pearl_secret_chest",
	"pearl_rainbow_stacker",
	"pearl_shell_drum",
	"pearl_toy_sailboat",
	"pearl_library_table",
	"pearl_shell_hopscotch",
	"pearl_canopy_bed",
	"pearl_bedside_table",
	"pearl_shell_wardrobe",
	"pearl_music_rail",
	"pearl_music_bar_0",
	"pearl_music_bar_1",
	"pearl_music_bar_2",
	"pearl_music_bar_3",
	"pearl_music_bar_4",
	"pearl_music_bar_5",
	"pearl_music_bar_6",
	"pearl_music_mallet_stand",
	"pearl_opera_gate",
	"pearl_opera_vista",
	"pearl_storage_barrel",
	"pearl_storage_crate",
	"pearl_provisions_hutch",
	"pearl_storage_cart",
	"pearl_shell_lantern",
	"pearl_pantry_shelf",
	"pearl_craft_easel",
	"pearl_paint_rack",
	"pearl_craft_table",
	"pearl_bath_duck",
	"pearl_towel_stack",
	"pearl_keepsake_tiara",
	"pearl_keepsake_cradle",
	"pearl_pet_basket",
	"pearl_keepsake_music_box",
]
const MIN_RUNTIME_COUNTS := {
	"pearl_column": 8,
	"pearl_balustrade": 12,
	"pearl_shell_arch": 12,
	"pearl_rainbow_window": 1,
	"pearl_shell_sconce": 8,
	"pearl_shell_chandelier": 8,
	"pearl_floor_medallion": 2,
	"pearl_throne_canopy": 1,
	"pearl_shell_throne": 1,
	"pearl_shell_planter": 4,
	"pearl_shell_bench": 2,
	"pearl_cloud_settee": 2,
	"pearl_cloud_pouf": 3,
	"pearl_shell_fountain": 2,
	"pearl_rainbow_gate": 3,
	"pearl_shell_banner_a": 4,
	"pearl_shell_banner_b": 2,
	"pearl_stair_rail": 2,
	"pearl_ocean_portal": 1,
	"pearl_shell_window": 19,
	"pearl_story_cushion": 1,
	"pearl_toy_block_stack": 1,
	"pearl_toy_chest": 3,
	"pearl_secret_chest": 1,
	"pearl_rainbow_stacker": 1,
	"pearl_shell_drum": 1,
	"pearl_toy_sailboat": 1,
	"pearl_library_table": 1,
	"pearl_shell_hopscotch": 1,
	"pearl_canopy_bed": 1,
	"pearl_bedside_table": 6,
	"pearl_shell_wardrobe": 1,
	"pearl_music_rail": 1,
	"pearl_music_bar_0": 1,
	"pearl_music_bar_1": 1,
	"pearl_music_bar_2": 1,
	"pearl_music_bar_3": 1,
	"pearl_music_bar_4": 1,
	"pearl_music_bar_5": 1,
	"pearl_music_bar_6": 1,
	"pearl_music_mallet_stand": 1,
	"pearl_opera_gate": 1,
	"pearl_opera_vista": 1,
	"pearl_storage_barrel": 7,
	"pearl_storage_crate": 3,
	"pearl_provisions_hutch": 1,
	"pearl_storage_cart": 1,
	"pearl_shell_lantern": 15,
	"pearl_pantry_shelf": 1,
	"pearl_craft_easel": 1,
	"pearl_paint_rack": 1,
	"pearl_craft_table": 1,
	"pearl_bath_duck": 1,
	"pearl_towel_stack": 1,
	"pearl_keepsake_tiara": 1,
	"pearl_keepsake_cradle": 1,
	"pearl_pet_basket": 1,
	"pearl_keepsake_music_box": 1,
}
const MAX_ASSET_TRIANGLES := 10000
const MAX_ASSET_SURFACES := 12

var main: ReefMain
var camera: Camera3D
var out_dir := ""
var checks_failed := 0


func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("CASTLE_ART|", label, "|", "OK" if ok else "FAIL", "|", detail)


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _close_pool_story() -> void:
	var guard := 0
	while bool(main.g.get("pool_story_active", false)) and guard < 12:
		main._hall_ref().advance_pool_story()
		guard += 1
		await process_frame
	_ck("pool_story_closes", not bool(main.g.get("pool_story_active", false)),
		"advances=%d" % guard)


func _triangle_count(mesh: Mesh) -> int:
	var triangles := 0
	for surface_index in range(mesh.get_surface_count()):
		var arrays: Array = mesh.surface_get_arrays(surface_index)
		var indices: PackedInt32Array = arrays[Mesh.ARRAY_INDEX]
		if indices.is_empty():
			var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
			triangles += vertices.size() / 3
		else:
			triangles += indices.size() / 3
	return triangles


func _inspect_asset(node: Node, result: Dictionary) -> void:
	if node is Light3D or node is Skeleton3D or node is AnimationPlayer or node is CollisionObject3D:
		var forbidden: Array = result["forbidden"] as Array
		forbidden.append(String(node.get_class()) + ":" + String(node.name))
	if node is MeshInstance3D:
		var mesh_node: MeshInstance3D = node as MeshInstance3D
		if mesh_node.mesh != null:
			result["mesh_count"] = int(result["mesh_count"]) + 1
			result["triangles"] = int(result["triangles"]) + _triangle_count(mesh_node.mesh)
			result["surfaces"] = int(result["surfaces"]) + mesh_node.mesh.get_surface_count()
	for child in node.get_children():
		_inspect_asset(child, result)


func _audit_assets() -> void:
	for asset_name in ASSET_NAMES:
		var path := KIT_DIR + asset_name + ".glb"
		var exists := ResourceLoader.exists(path)
		_ck("asset_exists_" + asset_name, exists, path)
		if not exists:
			continue
		var packed: PackedScene = load(path) as PackedScene
		_ck("asset_load_" + asset_name, packed != null, path)
		if packed == null:
			continue
		var instance: Node = packed.instantiate()
		root.add_child(instance)
		var result := {
			"mesh_count": 0,
			"triangles": 0,
			"surfaces": 0,
			"forbidden": [],
		}
		_inspect_asset(instance, result)
		_ck("single_mesh_" + asset_name, int(result["mesh_count"]) == 1, str(result))
		_ck("triangle_budget_" + asset_name, int(result["triangles"]) <= MAX_ASSET_TRIANGLES, str(result))
		_ck("surface_budget_" + asset_name, int(result["surfaces"]) <= MAX_ASSET_SURFACES, str(result))
		_ck("static_only_" + asset_name, (result["forbidden"] as Array).is_empty(), str(result))
		instance.free()


func _collect_runtime_assets(node: Node, counts: Dictionary) -> void:
	if node.has_meta("pearl_castle_asset"):
		var asset_name: String = String(node.get_meta("pearl_castle_asset"))
		counts[asset_name] = int(counts.get(asset_name, 0)) + 1
	for child in node.get_children():
		_collect_runtime_assets(child, counts)

func _collect_story_hutches(node: Node, hutches: Array[Node3D]) -> void:
	if node is Node3D and node.has_meta("castle_story_hutch"):
		hutches.append(node as Node3D)
	for child in node.get_children():
		_collect_story_hutches(child, hutches)


func _collect_visible_layers(node: Node, layers: Array[CanvasLayer]) -> void:
	if node is CanvasLayer:
		var layer: CanvasLayer = node as CanvasLayer
		if layer.visible:
			layers.append(layer)
			layer.visible = false
	for child in node.get_children():
		_collect_visible_layers(child, layers)


func _shot(name_value: String, position: Vector3, target: Vector3, fov_value: float = 66.0) -> void:
	camera.fov = fov_value
	camera.position = position
	camera.look_at(target, Vector3.UP)
	await _frames(4)
	await RenderingServer.frame_post_draw
	var image: Image = root.get_viewport().get_texture().get_image()
	var error: Error = image.save_png(out_dir.path_join(name_value + ".png"))
	_ck("shot_" + name_value, error == OK, out_dir.path_join(name_value + ".png"))


func _capture_castle() -> void:
	if DisplayServer.get_name() == "headless":
		return
	var requested: String = OS.get_environment("CASTLE_SHOT_OUT")
	out_dir = requested if requested != "" else ProjectSettings.globalize_path("res://tmp/castle_pearl_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var hidden_layers: Array[CanvasLayer] = []
	_collect_visible_layers(root, hidden_layers)
	main.set_process(false)
	if main.player != null:
		main.player.set_process(false)
		main.player.visible = false
	camera = Camera3D.new()
	camera.fov = 66.0
	camera.far = 420.0
	root.add_child(camera)
	camera.current = true
	var o: Vector3 = main.CASTLE_POS
	await _shot("castle_01_hall_overview", o + Vector3(0, 14, 40), o + Vector3(0, 15, -24))
	await _shot("castle_02_throne_focal", o + Vector3(19, 20, -2), o + Vector3(0, 23, -29))
	await _shot("castle_03_entrance_motifs", o + Vector3(0, 12, 18), o + Vector3(0, 5, 40), 68.0)
	await _shot("castle_04_wall_fixture", o + Vector3(4, 17, 6), o + Vector3(33, 18, 4))
	await _shot("castle_05_toy_room", o + Vector3(38, 40, 12), o + Vector3(48, 38, -8), 66.0)
	await _shot("castle_06_cloud_lounge", o + Vector3(45, 40, -40), o + Vector3(26, 38, -53), 64.0)
	await _shot("castle_07_star_chamber", o + Vector3(-45, 41, -40), o + Vector3(-25, 39, -53), 64.0)
	await _shot("castle_08_royal_bedroom", o + Vector3(37.5, 9.0, -18.0), o + Vector3(50.0, 4.5, -19.0), 68.0)
	await _shot("castle_09_music_room", o + Vector3(-49, 10, 11), o + Vector3(-44, 6, -6), 68.0)
	await _shot("castle_10_royal_loo", o + Vector3(-27.5, -13.5, -23.5), o + Vector3(-32.0, -15.2, -28.0), 64.0)
	await _shot("castle_11_back_chamber", o + Vector3(12, 11, -38), o + Vector3(0, 7, -47), 66.0)
	await _shot("castle_12_royal_library", o + Vector3(-38, 40, 12), o + Vector3(-48, 38, -8), 66.0)
	await _shot("castle_13_undercroft", o + Vector3(0, -9.5, 13.5), o + Vector3(0, -14.5, 34.5), 74.0)
	await _shot("castle_14_dreaming_floor", o + Vector3(0, 58, -39), o + Vector3(10, 54, -58), 70.0)
	await _shot("castle_15_pantry", o + Vector3(-10, -9, 4), o + Vector3(-20, -14, -2), 70.0)
	await _shot("castle_16_craft_room", o + Vector3(10, -9, -22), o + Vector3(20, -14, -28), 70.0)
	await _shot("castle_17_bubble_bath", o + Vector3(-10, -9, -22), o + Vector3(-18, -14, -28), 70.0)
	await _shot("castle_18_opera_gate", o + Vector3(-39.0, 8.5, -5.0), o + Vector3(-50.2, 4.5, -5.0), 62.0)
	await _shot("castle_19_bedroom_wardrobe", o + Vector3(43.0, 8.0, -20.0), o + Vector3(40.0, 6.2, -8.0), 62.0)
	await _shot("castle_20_pool_entry", o + Vector3(30.0, 12.0, 18.0), o + Vector3(65.0, -2.0, 30.0), 70.0)
	await _shot("castle_21_royal_natatorium_dirty", o + Vector3(86.0, 20.0, 100.0), o + Vector3(68.5, -3.0, 55.0), 72.0)


func _run() -> void:
	_audit_assets()
	var main_scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = main_scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	main._skip_intro()
	for rescue_key in [
		"_castle_pool_whale_met",
		"_castle_pool_pump_0",
		"_castle_pool_pump_1",
		"_castle_pool_pump_2",
		"_castle_pool_whale_friend",
	]:
		main.stickers.erase(rescue_key)
	main.pearl_count = main.PEARL_TOTAL
	for friend_value in main.friends:
		var friend: Dictionary = friend_value
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	await _frames(8)
	main._enter_level2()
	await _frames(18)
	main._enter_castle_interior()
	await _frames(30)
	var counts := {}
	_collect_runtime_assets(main, counts)
	for asset_name in MIN_RUNTIME_COUNTS:
		var minimum: int = int(MIN_RUNTIME_COUNTS[asset_name])
		var actual: int = int(counts.get(asset_name, 0))
		_ck("runtime_" + String(asset_name), actual >= minimum, "actual=%d minimum=%d" % [actual, minimum])
	_ck("hall_exit_marker", main.g.has("hall_exit"), str(main.g.get("hall_exit", Vector3.ZERO)))
	_ck("toilet_contract_preserved", main.g.has("toilet"), "royal loo interaction remains active")
	_ck("music_contract_preserved", (main.g.get("bells", []) as Array).size() == 7, "seven independent playable keys remain")
	_ck("opera_contract_preserved", main.g.has("opera_gate"), "authored gate keeps the open Opera House trigger")
	_ck("bed_contract_preserved", main.g.has("bed_pos"), str(main.g.get("bed_pos", Vector3.ZERO)))
	_ck("wardrobe_contract_preserved", main.g.has("wardrobe"), str(main.g.get("wardrobe", Vector3.ZERO)))
	_ck("craft_contract_preserved", main.g.has("craft_easel"), str(main.g.get("craft_easel", Vector3.ZERO)))
	_ck("secret_stand_contract_preserved", main.g.has("stand_chest") and main.g.has("stand_lid"), "slide tween roots remain")
	var story_hutches: Array[Node3D] = []
	_collect_story_hutches(main, story_hutches)
	var hutch_zones: Dictionary = {}
	var hutches_reachable: bool = true
	var hutch_mesh_budget_ok: bool = true
	var shared_hutch_mesh: Mesh = null
	for story_hutch in story_hutches:
		var hutch_zone: String = String(story_hutch.get_meta("castle_story_hutch_zone", ""))
		hutch_zones[hutch_zone] = int(hutch_zones.get(hutch_zone, 0)) + 1
		hutches_reachable = hutches_reachable \
			and float(story_hutch.get_meta("castle_story_hutch_reach_height", 99.0)) <= 3.3 \
			and float(story_hutch.get_meta("castle_story_hutch_depth", 99.0)) <= 1.7 \
			and float(story_hutch.get_meta("castle_story_hutch_width", 99.0)) <= 6.4 \
			and bool(story_hutch.get_meta("castle_story_hutch_analytic_solid", false))
		if not story_hutch is MeshInstance3D:
			hutch_mesh_budget_ok = false
			continue
		var hutch_mesh: Mesh = (story_hutch as MeshInstance3D).mesh
		if hutch_mesh == null:
			hutch_mesh_budget_ok = false
			continue
		if shared_hutch_mesh == null:
			shared_hutch_mesh = hutch_mesh
		var hutch_bounds: AABB = hutch_mesh.get_aabb()
		hutch_mesh_budget_ok = hutch_mesh_budget_ok \
			and hutch_mesh == shared_hutch_mesh \
			and hutch_mesh.get_surface_count() == 7 \
			and _triangle_count(hutch_mesh) <= 600 \
			and hutch_bounds.size.x <= 1.71 \
			and hutch_bounds.size.y <= 3.31 \
			and hutch_bounds.size.z <= 6.41 \
			and hutch_bounds.position.y >= -0.01
	var reachable_storybook_count: int = 0
	for mesh_value: Variant in main.find_children("*", "MeshInstance3D", true, false):
		var mesh_node: MeshInstance3D = mesh_value as MeshInstance3D
		if mesh_node.has_meta("castle_storybook_reachable"):
			reachable_storybook_count += 1
			hutches_reachable = hutches_reachable \
				and mesh_node.position.y <= main.CASTLE_POS.y + 3.3
	_ck("castle_practical_story_hutches", story_hutches.size() == 4
		and int(hutch_zones.get("hall", 0)) == 1
		and int(hutch_zones.get("library", 0)) == 3
		and reachable_storybook_count == 1
		and hutches_reachable
		and hutch_mesh_budget_ok,
		"count=%d zones=%s storybooks=%d reachable=%s mesh_ok=%s" % [
			story_hutches.size(),
			hutch_zones,
			reachable_storybook_count,
			hutches_reachable,
			hutch_mesh_budget_ok,
		])
	var pool_texture: Texture2D = load(
		"res://assets/castle/pool_2d/mermaid_pool_atlas.png") as Texture2D
	var ornament_texture: Texture2D = load(
		"res://assets/castle/pool_2d/poolside_ornaments_atlas.png") as Texture2D
	var whale_texture: Texture2D = load(
		"res://assets/castle/pool_2d/whale_states_atlas.png") as Texture2D
	var storyboard_texture: Texture2D = load(
		"res://assets/castle/pool_2d/whale_rescue_storyboard.png") as Texture2D
	var pool_card_count: int = 0
	var pool_unique_cells: Dictionary = {}
	var ornament_card_count: int = 0
	for pool_node_value: Variant in main.find_children("*", "Sprite3D", true, false):
		var pool_node: Node = pool_node_value as Node
		if pool_node.has_meta("castle_pool_art_index"):
			pool_card_count += 1
			pool_unique_cells[int(pool_node.get_meta("castle_pool_art_index"))] = true
		if pool_node.has_meta("castle_pool_ornament_index"):
			ornament_card_count += 1
	var pool_rect: Rect2 = main.g.get("castle_pool_rect", Rect2()) as Rect2
	var pool_dimensions: Vector2 = main.g.get(
		"castle_pool_dimensions_m", Vector2.ZERO) as Vector2
	var pool_surface: float = main.water_surface_y(
		main.CASTLE_POS.x + 68.5, main.CASTLE_POS.z + 55.0)
	var hall_dry_surface: float = main.water_surface_y(
		main.CASTLE_POS.x, main.CASTLE_POS.z)
	var pool_zone_ok: bool = false
	for zone_value: Variant in main.arena_zones:
		var zone: Dictionary = zone_value as Dictionary
		if ((zone["rect"] as Rect2).has_point(Vector2(68.5, 55.0))
				and float(zone.get("floor", 99.0)) < -7.0):
			pool_zone_ok = true
	var pump_rows: Array = main.g.get("castle_pool_pumps", [])
	var pointer_count := 0
	for pump_value: Variant in pump_rows:
		var pump: Dictionary = pump_value as Dictionary
		var pointer_value: Variant = pump.get("pointer")
		if pointer_value is Label3D and is_instance_valid(pointer_value):
			pointer_count += 1
	var whale_value: Variant = main.g.get("castle_pool_whale")
	_ck("pool_atlas_runtime", pool_texture != null
		and pool_texture.get_width() == 1024
		and pool_texture.get_height() == 1024,
		"1024px RGBA atlas")
	_ck("pool_sprite_family", pool_card_count == 24
		and pool_unique_cells.size() == 16
		and int(main.g.get("castle_pool_2d_count", 0)) == 16,
		"runtime=%d unique=%d state=%d" % [
			pool_card_count,
			pool_unique_cells.size(),
			int(main.g.get("castle_pool_2d_count", 0)),
		])
	_ck("pool_olympic_footprint", pool_dimensions == Vector2(100.0, 50.0)
		and pool_rect.size == Vector2(50.0, 100.0)
		and is_equal_approx(pool_rect.size.x / pool_rect.size.y, 0.5),
		"dimensions=%s rect=%s" % [pool_dimensions, pool_rect])
	_ck("pool_water_oracle", is_equal_approx(
		pool_surface, main.CASTLE_POS.y + float(main.g.get("castle_pool_surface_y", 0.15)))
		and hall_dry_surface < -1e17,
		"pool=%.2f hall=%.2f" % [pool_surface, hall_dry_surface])
	_ck("pool_lowered_floor_zone", pool_zone_ok, "basin floor below deck")
	_ck("pool_ornament_atlas", ornament_texture != null
		and ornament_texture.get_width() == 1024
		and ornament_texture.get_height() == 768,
		"4x3 atlas=%s" % ornament_texture)
	_ck("pool_twelve_ornaments", ornament_card_count == 12
		and int(main.g.get("castle_pool_ornament_count", 0)) == 12,
		"runtime=%d state=%d" % [
			ornament_card_count, int(main.g.get("castle_pool_ornament_count", 0))])
	_ck("pool_three_pumps", pump_rows.size() == 3 and pointer_count == 3,
		"pumps=%d pointers=%d" % [pump_rows.size(), pointer_count])
	_ck("pool_whale_atlas", whale_texture != null
		and whale_texture.get_width() == 1024
		and whale_texture.get_height() == 512,
		"4x2 whale states")
	_ck("pool_sick_whale_runtime", whale_value is Sprite3D
		and is_instance_valid(whale_value)
		and int((whale_value as Sprite3D).get_meta("castle_pool_whale_cell", -1)) == 0,
		"initial generated whale cell")
	_ck("pool_storyboard_nine", storyboard_texture != null
		and storyboard_texture.get_width() == 768
		and storyboard_texture.get_height() == 768
		and main._hall_ref().pool_story_panel_count() == 9,
		"3x3 wordless story atlas")
	_ck("pool_initial_dirty_state", int(main.g.get("castle_pool_rescue_state", -1)) == 0,
		"state=%d" % int(main.g.get("castle_pool_rescue_state", -1)))

	# Meeting reveals the pointers and three wordless opening panels, but mere
	# proximity never repairs a pump. Capture this dirty rescue state first.
	main._hall_ref()._meet_pool_whale()
	_ck("pool_meeting_saved", bool(main.stickers.get("_castle_pool_whale_met", false)),
		"whale encounter is persistent")
	_ck("pool_meeting_no_auto_fix",
		not bool(main.stickers.get("_castle_pool_pump_0", false))
		and not bool(main.stickers.get("_castle_pool_pump_1", false))
		and not bool(main.stickers.get("_castle_pool_pump_2", false)),
		"meeting only starts the kindness quest")
	await _capture_castle()
	await _close_pool_story()
	main._hall_ref()._replay_pool_story()
	_ck("pool_meeting_story_replay", bool(main.g.get("pool_story_active", false))
		and int(main.g.get("pool_story_last_panel", -1)) == 0,
		"met-but-incomplete story can always be replayed")
	await _close_pool_story()

	# Agency contract: no input does nothing; a fresh action edge fixes one pump;
	# a held action cannot repair the next pump until released and pressed again.
	var hall: CastleHall = main._hall_ref()
	main.touch_ui.action_down = false
	var first_pos: Vector3 = (pump_rows[0] as Dictionary)["pos"] as Vector3
	hall.tick(0.016, first_pos)
	_ck("pool_pump_zero_input", hall._pool_fixed_count() == 0,
		"standing beside a pump is safe")
	main.touch_ui.action_down = true
	hall.tick(0.016, first_pos)
	_ck("pool_pump_first_edge", hall._pool_fixed_count() == 1,
		"one press fixes exactly one")
	await _close_pool_story()
	var second_pos: Vector3 = (pump_rows[1] as Dictionary)["pos"] as Vector3
	hall.tick(0.016, second_pos)
	_ck("pool_pump_held_edge", hall._pool_fixed_count() == 1,
		"holding cannot chain repairs")
	main.touch_ui.action_down = false
	hall.tick(0.016, second_pos)
	main.touch_ui.action_down = true
	hall.tick(0.016, second_pos)
	_ck("pool_pump_second_edge", hall._pool_fixed_count() == 2,
		"release and press fixes the second")
	await _close_pool_story()
	var third_pos: Vector3 = (pump_rows[2] as Dictionary)["pos"] as Vector3
	main.touch_ui.action_down = false
	hall.tick(0.016, third_pos)
	main.touch_ui.action_down = true
	hall.tick(0.016, third_pos)
	_ck("pool_pump_third_edge", hall._pool_fixed_count() == 3,
		"third deliberate press completes the clean")
	await _close_pool_story()
	await _frames(100)
	hall._apply_pool_rescue_state(false)

	var hidden_pointer_count := 0
	for pump_value: Variant in pump_rows:
		var pump: Dictionary = pump_value as Dictionary
		var pointer_value: Variant = pump.get("pointer")
		if pointer_value is Label3D and is_instance_valid(pointer_value) \
				and not (pointer_value as Label3D).visible:
			hidden_pointer_count += 1
	_ck("pool_friend_persistent", bool(main.stickers.get("_castle_pool_whale_friend", false))
		and int(main.g.get("castle_pool_rescue_state", -1)) == 3,
		"friend=%s state=%d" % [
			main.stickers.get("_castle_pool_whale_friend", false),
			int(main.g.get("castle_pool_rescue_state", -1)),
		])
	_ck("pool_healthy_whale", int(
		(whale_value as Sprite3D).get_meta("castle_pool_whale_cell", -1)) == 6,
		"healthy friendship state")
	_ck("pool_pointers_complete", hidden_pointer_count == 3,
		"hidden=%d" % hidden_pointer_count)
	_ck("pool_all_story_beats_seen", int(main.g.get("pool_story_seen_mask", 0)) == 511,
		"mask=%d" % int(main.g.get("pool_story_seen_mask", 0)))
	if DisplayServer.get_name() != "headless":
		var o: Vector3 = main.CASTLE_POS
		await _shot("castle_22_royal_natatorium_friend",
			o + Vector3(86.0, 20.0, 100.0),
			o + Vector3(68.5, -3.0, 55.0),
			72.0)
	print("CASTLE_ART|RESULT=", "FAIL" if checks_failed > 0 else "OK", " checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _init() -> void:
	call_deferred("_run")
