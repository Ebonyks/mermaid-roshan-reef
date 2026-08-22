extends SceneTree
# Crown Star probe: entering the armed Royal Hall must CELEBRATE IN PLACE —
# win recorded, Roshan stays in her castle — instead of the old
# _finish_level2() ocean eject.
# The front-door exit must still return her to the courtyard when SHE chooses.
# Prints OK/FAIL lines (ci.sh convention).

var main: Node
var checks_failed := 0
const DEPTH_MANIFEST := "res://FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"
const ROYAL_HALL_ARRIVAL_SETTLE_MS := 1250
const EXPECTED_ROOM_ITEM_IDS := {
	"main_hall": ["sleepy_bunny", "shell_bunny", "runner_bunny"],
	"opera_hall": [
		"curtains", "chandelier", "stage_star", "footlights",
		"pearl_sconce_left", "pearl_sconce_right",
	],
	"kitchen": ["sink", "pan_1", "pan_2", "pan_3", "pan_4", "oven", "fridge"],
	"library": [
		"magic_book", "pearl_table", "pearl_lamp", "book_stack",
		"pearl_lamp_right", "ceiling_chandelier",
	],
	"playroom": [
		"stuffie_nook", "stacking_toy", "blocks", "play_tent",
		"tent_flaps_right", "shelf_sailboat",
	],
	"craft_room": [
		"idea_board", "paint_table", "palette", "ribbon_rack",
		"supply_cupboard_left",
	],
	"mermaid_pool": [
		"waterfall", "flower_float", "seahorse_fountain", "star_float",
	],
	"bubble_bath": [
		"bathtub", "sink", "toilet", "rubber_duck", "vanity_mirror",
	],
}
const PLAYROOM_RESCUE_ITEM_IDS := [
	"baby_eagle_rescue", "eagle_pin_left", "eagle_pin_right",
]
const EXPECTED_ROOM_HOTSPOT_NAMES := {
	"main_hall": [],
	"opera_hall": [
		"Touch_curtains", "Touch_chandelier", "Touch_stage_star",
		"Touch_footlights", "Touch_pearl_sconce_left",
		"Touch_pearl_sconce_right",
	],
	"kitchen": ["Touch_sink", "Touch_pan_rack", "Touch_oven", "Touch_fridge"],
	"library": [
		"Touch_magic_book", "Touch_pearl_table", "Touch_pearl_lamp",
		"Touch_book_stack", "Touch_pearl_lamp_right",
		"Touch_ceiling_chandelier",
	],
	"playroom": [
		"Touch_stuffie_nook", "Touch_stacking_toy", "Touch_blocks",
		"Touch_play_tent", "Touch_tent_flaps_right", "Touch_shelf_sailboat",
	],
	"craft_room": [
		"Touch_idea_board", "Touch_paint_table", "Touch_palette",
		"Touch_ribbon_rack", "Touch_supply_cupboard_left",
	],
	"mermaid_pool": [
		"Touch_waterfall", "Touch_flower_float", "Touch_seahorse_fountain",
		"Touch_star_float",
	],
	"bubble_bath": [
		"Touch_bathtub", "Touch_sink", "Touch_toilet", "Touch_rubber_duck",
		"Touch_vanity_mirror",
	],
}
const EXPECTED_NATIVE_V4_ITEM_IDS := {
	"main_hall": [],
	"opera_hall": ["pearl_sconce_left", "pearl_sconce_right"],
	"kitchen": ["fridge"],
	"library": ["pearl_lamp_right", "ceiling_chandelier"],
	"playroom": ["tent_flaps_right", "shelf_sailboat"],
	"craft_room": ["supply_cupboard_left"],
	"mermaid_pool": [
		"waterfall", "flower_float", "seahorse_fountain", "star_float",
	],
	"bubble_bath": ["vanity_mirror"],
}

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("CROWN|", label, ": ", ("OK" if ok else "FAIL"), (" " + detail if detail != "" else ""))

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _world_cards_conform(node: Node) -> bool:
	for child: Node in node.get_children():
		if child is Node3D:
			return false
		if child is Sprite2D:
			var sprite := child as Sprite2D
			if sprite.texture == null \
					or bool(sprite.get_meta("shaded", false)):
				return false
		elif child is CanvasItem and not child is Node2D:
			return false
		if not _world_cards_conform(child):
			return false
	return true

func _visible_sprite_card_count(node: Node) -> int:
	var count := 0
	for child: Node in node.get_children():
		if child is Sprite2D and (child as Sprite2D).visible:
			count += 1
		count += _visible_sprite_card_count(child)
	return count

func _all_children_follow_fixture_contract(node: Node2D) -> bool:
	if node == null:
		return false
	for child: Node in node.get_children():
		if child is Sprite2D:
			if (child as Sprite2D).texture == null \
					or bool((child as Sprite2D).get_meta("shaded", false)):
				return false
			continue
		if child is Node3D:
			return false
		if not child is Node2D:
			return false
	return true

func _dictionary_has_exact_keys(actual: Dictionary, expected: Array) -> bool:
	if actual.size() != expected.size():
		return false
	for key_value: Variant in expected:
		if not actual.has(String(key_value)):
			return false
	return true

func _children_have_exact_names(node: Node, expected: Array) -> bool:
	if node == null or node.get_child_count() != expected.size():
		return false
	var actual_names: Dictionary = {}
	for child: Node in node.get_children():
		actual_names[String(child.name)] = true
	return _dictionary_has_exact_keys(actual_names, expected)

func _native_v4_items_conform(room_id: String, expected: Array) -> bool:
	for item_id_value: Variant in expected:
		var item_id := String(item_id_value)
		var record: Dictionary = main.castle_room_item_sprites.get(
			item_id, {}) as Dictionary
		var sprite: Sprite2D = record.get("sprite") as Sprite2D
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		var visual: Dictionary = item_data.get("v2_visual", {}) as Dictionary
		var ownership: Dictionary = visual.get(
			"source_ownership", {}) as Dictionary
		var behavior: Dictionary = visual.get(
			"animation_behavior", {}) as Dictionary
		var rig: Dictionary = record.get("fixture_rig", {}) as Dictionary
		var frame_count := int(sprite.get_meta("animation_frame_count", 0)) \
			if sprite != null else 0
		if sprite == null \
				or String(visual.get("pack", "")) != "v4_native" \
				or not bool(ownership.get("passed", false)) \
				or not bool(ownership.get("verified", false)) \
				or not bool(ownership.get("background_healed", false)) \
				or not bool(ownership.get("duplicate_pixels_removed", false)) \
				or String(behavior.get("mode", "")) \
					!= "authored_object_states" \
				or bool(behavior.get("generic_transform_fallback", true)) \
				or frame_count < 4 or frame_count > 12 \
				or not bool(sprite.get_meta("source_owned_native", false)) \
				or not bool(sprite.get_meta(
					"source_ownership_verified", false)) \
				or not bool(sprite.get_meta(
					"native_authored_object_states", false)) \
				or not bool(sprite.get_meta(
					"generated_full_object_states", false)) \
				or bool(sprite.get_meta("primary_animation_is_overlay", true)) \
				or bool(sprite.get_meta("generic_transform_fallback", true)) \
				or String(sprite.get_meta("source_asset_role", "")) \
					!= "unique_object" \
				or String(sprite.get_meta("source_object_id", "")) \
					!= room_id + ":" + item_id \
				or rig.is_empty() or rig.get("sprite") != sprite:
			return false
	return true

func _native_background_tiles_conform(room_id: String) -> bool:
	var expected_count := 12 if room_id == "kitchen" else 8
	var expected_size := Vector2i(1024, 768) if room_id == "kitchen" \
		else Vector2i(910, 1024)
	if main.castle_room_detail_tiles.size() != expected_count:
		return false
	for tile_value: Variant in main.castle_room_detail_tiles:
		var tile := tile_value as Sprite2D
		if tile == null or tile.texture == null \
				or Vector2i(tile.texture.get_width(), tile.texture.get_height()) \
					!= expected_size \
				or String(tile.texture.resource_path).get_base_dir() \
					!= "res://assets/flats/castle/interactions_v4/background_tiles" \
				or String(tile.get_meta("source_asset_role", "")) \
					!= "source_owned_healed_background_tile" \
				or not bool(tile.get_meta(
					"native_source_ownership_background", false)) \
				or bool(tile.get_meta("transparent", false)) \
				or bool(tile.get_meta("shaded", false)):
			return false
	return true

func _stage_to_screen(stage: Control, point: Vector2) -> Vector2:
	return stage.get_global_transform_with_canvas() * point

func _depth_manifest() -> Dictionary:
	if not FileAccess.file_exists(DEPTH_MANIFEST):
		return {}
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string(DEPTH_MANIFEST))
	return parsed as Dictionary if parsed is Dictionary else {}

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.day_one_active = false
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main.level2_done_once = false
	main._enter_level2()
	await _frames(10)
	main._enter_castle_interior()
	await _frames(20)
	var o: Vector3 = main.CASTLE_POS
	var player: Node3D = main.player
	if main._castle_rooms_ref().is_open():
		var rooms: CastleRooms25D = main._castle_rooms_ref()
		_ck("room_shell_open", rooms.is_open())
		_ck("movement_does_not_award", not bool(main.g.get("crown_won", false)))
		var retired_hall_keys: Array[String] = [
			"hall_exit", "bed_pos", "stand_chest", "toilet", "dungeon_gate",
			"craft_easel", "wardrobe", "song_star", "secret_door",
			"hall_touch"]
		var retired_hall_absent := true
		for retired_key: String in retired_hall_keys:
			retired_hall_absent = retired_hall_absent \
				and not main.g.has(retired_key)
		_ck("legacy_3d_castle_hall_not_built",
			retired_hall_absent
			and main.game_nodes.is_empty()
			and main.arena_solids.is_empty()
			and main.arena_zones.is_empty())
		_ck("sprite_castle_is_only_interior_route",
			main.castle_room_layer != null
			and main.castle_room_layer.visible
			and not main.player.visible
			and main.touch_interactables.is_empty())
		_ck("opera_lives_behind_physical_door_not_3d_courtyard",
			main.castle_room_buttons.has("opera_hall")
			and not main.g.has("opera_gate"))
		_ck("canvas2d_world_root", main.castle_room_world_root is Node2D)
		_ck("direct_canvas_has_no_room_camera",
			main.castle_room_stage.find_children(
				"*", "Camera2D", true, false).is_empty()
			and main.castle_room_stage.find_children(
				"*", "Camera3D", true, false).is_empty())
		_ck("world_has_no_spatial_art",
			_world_cards_conform(main.castle_room_world_root))
		_ck("backdrop_is_unshaded_sprite2d",
			main.castle_room_background is Sprite2D
			and not bool(main.castle_room_background.get_meta("shaded", false)))
		var backdrop_size: Vector2 = main.castle_room_background.texture.get_size()
		_ck("reference_canvas_scale",
			main.castle_room_background.scale.is_equal_approx(
				Vector2.ONE * CastleRooms25D.ART_TO_STAGE),
			"scale=%s" % str(main.castle_room_background.scale))
		_ck("backdrop_aspect_preserved",
			is_equal_approx(backdrop_size.aspect(), 16.0 / 9.0))
		var manifest: Dictionary = _depth_manifest()
		var manifest_rooms: Dictionary = manifest.get("rooms", {}) as Dictionary
		var clean_plate_manifest_ok: bool = manifest_rooms.size() == 8 \
			and String(manifest.get("source_policy", "")).contains(
				"Approved room composites")
		for manifest_room_id: String in manifest_rooms:
			var manifest_room: Dictionary = manifest_rooms[manifest_room_id] \
				as Dictionary
			var manifest_cards: Array = manifest_room.get("cards", []) as Array
			var all_cards_owned := true
			for manifest_card_value: Variant in manifest_cards:
				var manifest_card: Dictionary = manifest_card_value as Dictionary
				all_cards_owned = all_cards_owned \
					and bool(manifest_card.get(
						"alpha_outline_refined", false)) \
					and (
						int(manifest_card.get("alpha_pixels", 0)) > 0
						or int(manifest_card.get(
							"depth_opaque_pixels", -1)) == 0
					)
			clean_plate_manifest_ok = clean_plate_manifest_ok \
				and String(manifest_room.get("background", "")).ends_with(
					"_background.png") \
				and int(manifest_room.get("card_overlap_pixels", -1)) == 0 \
				and float(manifest_room.get("changed_owned_ratio", 0.0)) > 0.80 \
				and float(manifest_room.get(
					"resting_reconstruction_mean_abs_error", 999.0)) < 1.0 \
				and all_cards_owned
		_ck("clean_background_unique_pixel_manifest",
			clean_plate_manifest_ok)
		var node_contract: Dictionary = manifest.get(
			"runtime_node_contract", {}) as Dictionary
		var forbidden_world_types: Array = node_contract.get(
			"canvas_art_forbidden", node_contract.get(
				"world_art_forbidden", [])) as Array
		var allowed_world_types: Array = node_contract.get(
			"canvas_art_allowed", node_contract.get(
				"world_art_allowed", [])) as Array
		var shaded_role_allowlist: Array = node_contract.get(
			"shaded_role_allowlist", []) as Array
		var manifest_root: String = String(node_contract.get(
			"world_root", node_contract.get("canvas_root", "")))
		_ck("manifest_sprite2d_node_contract",
			manifest_root == "Node2D"
			and String(node_contract.get("camera", "")) == "none"
			and String(node_contract.get("coordinate_system", "")) \
				in ["direct_canvas", "direct_canvas_coordinates"]
			and allowed_world_types.size() == 1
			and allowed_world_types.has("Sprite2D:unshaded")
			and shaded_role_allowlist.is_empty()
			and forbidden_world_types.has("Node3D")
			and forbidden_world_types.has("Sprite3D")
			and forbidden_world_types.has("Camera3D")
			and forbidden_world_types.has("MeshInstance3D")
			and forbidden_world_types.has("MultiMeshInstance3D")
			and forbidden_world_types.has("CSGShape3D")
			and forbidden_world_types.has("Decal"))
		var hall_manifest: Dictionary = manifest_rooms.get(
			"main_hall", {}) as Dictionary
		var hall_master_dimensions: Array = hall_manifest.get(
			"master_dimensions", []) as Array
		var hall_manifest_tiles: Array = hall_manifest.get(
			"runtime_tiles", []) as Array
		var hall_runtime_audit: Dictionary = hall_manifest.get(
			"current_runtime_audit", {}) as Dictionary
		var historical_hall_revision: Dictionary = manifest.get(
			"runtime_correction_2026_08_04", {}) as Dictionary
		var current_hall_revision: Dictionary = manifest.get(
			"runtime_correction_2026_08_22", {}) as Dictionary
		var current_runtime_contract: Dictionary = current_hall_revision.get(
			"runtime_node_contract", manifest.get(
				"runtime_node_contract", {})) as Dictionary
		var current_forbidden_nodes: Array = current_runtime_contract.get(
			"canvas_art_forbidden", current_runtime_contract.get(
				"world_art_forbidden", [])) as Array
		var current_allowed_nodes: Array = current_runtime_contract.get(
			"canvas_art_allowed", current_runtime_contract.get(
				"world_art_allowed", [])) as Array
		var current_hall_background: Dictionary = historical_hall_revision.get(
			"background_contract", {}) as Dictionary
		var hall_manifest_tiles_current := hall_manifest_tiles.size() == 16
		for hall_tile_value: Variant in hall_manifest_tiles:
			var hall_tile: Dictionary = hall_tile_value as Dictionary
			var hall_tile_dimensions: Array = hall_tile.get(
				"dimensions", []) as Array
			hall_manifest_tiles_current = hall_manifest_tiles_current \
				and String(hall_tile.get("path", "")).begins_with(
					"assets/flats/castle/main_hall_redraw_2026-08-03/tiles/") \
				and hall_tile_dimensions.size() == 2 \
				and int(hall_tile_dimensions[0]) == 910 \
				and int(hall_tile_dimensions[1]) == 1024
		var hall_master_dimensions_current: bool = \
			hall_master_dimensions.size() == 2 \
			and int(hall_master_dimensions[0]) == 7280 \
			and int(hall_master_dimensions[1]) == 2048
		var current_hall_bleed: Array = current_hall_background.get(
			"runtime_neighbor_bleed_pixels", []) as Array
		var current_hall_zero_bleed: bool = current_hall_bleed.size() == 2 \
			and int(current_hall_bleed[0]) == 0 \
			and int(current_hall_bleed[1]) == 0
		_ck("main_hall_manifest_points_to_current_strict_runtime",
			String(hall_manifest.get("active_runtime_status", ""))
				== "accepted_current_runtime"
			and hall_master_dimensions_current
			and String(hall_manifest.get("master_sha256", ""))
				== "297cd6d181288ef6cc364a71a89fdb4da168f688249ca910995e71f6f769a9dd"
			and hall_manifest_tiles_current
			and String(hall_runtime_audit.get("build_manifest", ""))
				== "assets_src/imagegen/castle_main_hall_redraw_2026-08-03/main_hall_strict_2k_build_manifest.json"
			and String(hall_runtime_audit.get("blocking_audit", ""))
				== "audit/castle_sprite3d/castle_main_hall_redraw_2026-08-04_2k_audit.json"
			and String(hall_runtime_audit.get("node_inventory", ""))
				== "audit/castle_sprite3d/castle_main_hall_redraw_2026-08-03_node_inventory.json"
			and String(historical_hall_revision.get("status", ""))
				== "historical_superseded"
			and String(current_hall_revision.get("status", ""))
				== "accepted_current_runtime"
			and bool(current_hall_background.get("all_cards_unshaded", false))
			and int(current_hall_background.get("runtime_tile_count", 0)) == 16
			and current_hall_zero_bleed
			and String(current_runtime_contract.get(
				"world_root", current_runtime_contract.get("canvas_root", "")))
				== "Node2D"
			and String(current_runtime_contract.get("camera", "")) == "none"
			and String(current_runtime_contract.get(
				"coordinate_system", "")) in [
				"direct_canvas", "direct_canvas_coordinates"]
			and current_allowed_nodes.has("Sprite2D:unshaded")
			and current_forbidden_nodes.has("Node" + "3D")
			and current_forbidden_nodes.has("Sprite3D")
			and current_forbidden_nodes.has("Camera3D")
			and current_forbidden_nodes.has("MeshInstance3D")
			and current_forbidden_nodes.has("MultiMeshInstance" + "3D")
			and current_forbidden_nodes.has("CSGShape" + "3D")
			and current_forbidden_nodes.has("Decal"))
		var native_contract: Dictionary = manifest.get(
			"owner_native_environment_contract", {}) as Dictionary
		var required_ratio: Array = native_contract.get(
			"required_reference_aspect_ratio", []) as Array
		var native_2k_ok: bool = String(native_contract.get(
			"status", "")) == "compliant"
		native_2k_ok = native_2k_ok \
			and int(native_contract.get(
				"required_minimum_long_edge", 0)) >= 2048 \
			and required_ratio.size() == 2 \
			and int(required_ratio[0]) == 16 \
			and int(required_ratio[1]) == 9 \
			and float(native_contract.get(
				"ratio_rounding_tolerance_pixels", 99.0)) <= 1.0 \
			and not bool(native_contract.get(
				"master_power_of_two_required", true)) \
			and int(native_contract.get(
				"runtime_tile_max_long_edge", 9999)) <= 1024 \
			and bool(native_contract.get(
				"runtime_tiles_lossless_no_scale", false))
		for manifest_room_id: String in manifest_rooms:
			var manifest_room: Dictionary = manifest_rooms[manifest_room_id] \
				as Dictionary
			var master_dimensions: Array = manifest_room.get(
				"master_dimensions", []) as Array
			var runtime_tiles: Array = manifest_room.get(
				"runtime_tiles", []) as Array
			var master_long_edge := 0
			var master_short_edge := 0
			if master_dimensions.size() == 2:
				master_long_edge = maxi(
					int(master_dimensions[0]), int(master_dimensions[1]))
				master_short_edge = mini(
					int(master_dimensions[0]), int(master_dimensions[1]))
			var expected_tile_count := 16 if manifest_room_id == "main_hall" \
				else (12 if manifest_room_id == "kitchen" else 8)
			var expected_tile_dimensions := Vector2i(1024, 768) \
				if manifest_room_id == "kitchen" else Vector2i(910, 1024)
			native_2k_ok = native_2k_ok \
				and bool(manifest_room.get(
					"native_master_compliant", false)) \
				and master_long_edge >= 2048 \
				and master_short_edge >= 2048 \
				and float(manifest_room.get(
					"aspect_ratio_pixel_delta", 99.0)) <= 1.0 \
				and bool(manifest_room.get(
					"tile_reconstruction_pixel_exact", false)) \
				and runtime_tiles.size() == expected_tile_count
			for tile_value: Variant in runtime_tiles:
				var tile: Dictionary = tile_value as Dictionary
				var dimensions: Array = tile.get("dimensions", []) as Array
				native_2k_ok = native_2k_ok and dimensions.size() == 2 \
					and Vector2i(int(dimensions[0]), int(dimensions[1])) \
						== expected_tile_dimensions
		_ck("native_2k_environment_gate", native_2k_ok,
			"native >=2K masters reconstruct through exact <=1024 tiles")
		rooms.show_room("library", false)
		await _frames(2)
		_ck("library_mid_layer", main.castle_room_mid_layer.get_child_count() == 0)
		_ck("library_front_layers", main.castle_room_front_layer.get_child_count() == 2)
		_ck("library_node_inventory",
			main.castle_room_background is Sprite2D
			and main.castle_room_background_tiles.size() == 16
			and main.castle_room_detail_tiles.size() == 8
			and _dictionary_has_exact_keys(
				main.castle_room_item_sprites,
				EXPECTED_ROOM_ITEM_IDS["library"] as Array)
			and main.castle_room_front_layer.get_child_count() == 2
			and main.castle_room_player_sprite is Sprite2D
			and main.castle_room_player_shadow is Sprite2D)
		var library_book: Sprite2D = (
			main.castle_room_item_sprites["magic_book"] as Dictionary
			).get("sprite") as Sprite2D
		var library_table: Sprite2D = (
			main.castle_room_item_sprites["pearl_table"] as Dictionary
			).get("sprite") as Sprite2D
		_ck("library_depth_bands",
			main.castle_room_background.z_index
				< library_book.z_index
			and library_book.z_index < library_table.z_index
			and library_table.z_index
				< (main.castle_room_front_layer.get_child(0) as Sprite2D).z_index)
		var room_items_ok := true
		var room_hotspots_ok := true
		var room_cards_ok := true
		var room_depth_ok := true
		var native_v4_items_ok := true
		var native_backgrounds_ok := true
		var overdraw_budget_ok := true
		for room_id: String in [
			"main_hall", "opera_hall", "kitchen", "library", "playroom",
			"craft_room", "mermaid_pool", "bubble_bath"]:
			rooms.show_room(room_id, false)
			await _frames(2)
			var hall_mode: bool = room_id == "main_hall"
			var expected_item_ids: Array = (
				EXPECTED_ROOM_ITEM_IDS[room_id] as Array).duplicate()
			if room_id == "playroom" and not rooms._playroom_rescue_done():
				expected_item_ids.append_array(PLAYROOM_RESCUE_ITEM_IDS)
			var expected_hotspot_names: Array = \
				EXPECTED_ROOM_HOTSPOT_NAMES[room_id] as Array
			var expected_native_v4_ids: Array = \
				EXPECTED_NATIVE_V4_ITEM_IDS[room_id] as Array
			room_items_ok = room_items_ok \
				and _dictionary_has_exact_keys(
					main.castle_room_item_sprites, expected_item_ids)
			room_hotspots_ok = room_hotspots_ok \
				and _children_have_exact_names(
					main.castle_room_item_hotspot_layer, expected_hotspot_names)
			native_v4_items_ok = native_v4_items_ok \
				and _native_v4_items_conform(room_id, expected_native_v4_ids)
			var item_depths: Dictionary = {}
			for item_id_value: Variant in main.castle_room_item_sprites:
				var item_record: Dictionary = main.castle_room_item_sprites[
					item_id_value] as Dictionary
				var item_sprite: Sprite2D = item_record.get("sprite") as Sprite2D
				item_depths[snappedf(float(item_sprite.z_index), 0.01)] = true
				room_depth_ok = room_depth_ok \
					and String(item_sprite.get_meta(
						"source_asset_role", "")) == "unique_object" \
					and String(item_sprite.get_meta(
						"source_object_id", "")) \
						== room_id + ":" + String(item_id_value)
			room_depth_ok = room_depth_ok and item_depths.size() >= 2
			if room_id == "main_hall":
				native_backgrounds_ok = native_backgrounds_ok \
					and main.castle_room_background_tiles.size() == 16 \
					and main.castle_room_detail_tiles.is_empty()
			else:
				native_backgrounds_ok = native_backgrounds_ok \
					and _native_background_tiles_conform(room_id) \
					and String(main.castle_room_background.texture.resource_path
						).ends_with("_background.png")
			room_cards_ok = room_cards_ok \
				and _all_children_follow_fixture_contract(
					main.castle_room_item_visual_layer) \
				and _all_children_follow_fixture_contract(
					main.castle_room_front_layer) \
				and _world_cards_conform(main.castle_room_world_root)
			overdraw_budget_ok = overdraw_budget_ok \
				and _visible_sprite_card_count(
					main.castle_room_world_root) <= 33
		_ck("room_item_inventory_matches_source_owned_design", room_items_ok)
		_ck("room_touch_inventory_matches_design", room_hotspots_ok)
		_ck("source_owned_v4_items_match_audited_design", native_v4_items_ok)
		_ck("native_healed_background_routes_match_design", native_backgrounds_ok)
		_ck("all_room_art_uses_sprite2d_contract", room_cards_ok)
		_ck("objects_have_authored_real_depth", room_depth_ok)
		_ck("speedy_visible_card_budget", overdraw_budget_ok)
		rooms.show_room("bubble_bath", false)
		await _frames(2)
		var toilet_button: Button = main.castle_room_item_hotspot_layer.get_node_or_null(
			"Touch_toilet") as Button
		var toilet_record: Dictionary = main.castle_room_item_sprites.get("toilet", {})
		var toilet_sprite: Sprite2D = toilet_record.get("sprite") as Sprite2D
		var toilet_rig: Dictionary = toilet_record.get(
			"fixture_rig", {}) as Dictionary
		var toilet_visual: Dictionary = toilet_rig.get(
			"visual", {}) as Dictionary
		var toilet_water: Array = toilet_rig.get("water", []) as Array
		var expected_toilet_sheet: String = "res://" + String(
			toilet_visual.get("sheet", ""))
		rooms._update_touch_hotspots()
		var toilet_screen: Vector2 = toilet_sprite.get_global_transform_with_canvas() \
			* Vector2.ZERO
		var toilet_stage: Vector2 = rooms._screen_to_stage(toilet_screen)
		_ck("projected_touch_hit_mapping",
			toilet_button != null
			and Rect2(toilet_button.position, toilet_button.size).has_point(
				toilet_stage),
			"stage=%s hit=%s" % [
				str(toilet_stage),
				str(Rect2(toilet_button.position, toilet_button.size))])
		var front_card: Sprite2D = main.castle_room_front_layer.get_child(0) as Sprite2D
		_ck("direct_canvas_depth_order", front_card.z_index
			> main.castle_room_background.z_index,
			"back=%d front=%d" % [main.castle_room_background.z_index,
				front_card.z_index])
		var walk_target := Vector2(260.0, 430.0)
		rooms._walk_cutout_to(_stage_to_screen(
			main.castle_room_stage, walk_target))
		var requested_foot: Vector2 = main.castle_room_player_sprite.get_meta(
			"stage_foot", Vector2.ZERO) as Vector2
		_ck("touch_navigation_maps_to_walk_lane",
			requested_foot.distance_to(walk_target) < 0.1)
		rooms._position_player_at_foot(requested_foot, false)
		var toilet_texture: Texture2D = toilet_sprite.texture
		var toilet_data: Dictionary = toilet_record.get("data", {}) as Dictionary
		var toilet_start_position: Vector2 = toilet_sprite.position
		var toilet_start_scale: Vector2 = toilet_sprite.scale
		var toilet_start_rotation: float = toilet_sprite.rotation
		main.castle_room_prop_sfx.stop()
		main.castle_room_prop_sfx.stream = null
		if toilet_button != null:
			toilet_button.emit_signal("pressed")
		await process_frame
		_ck("toilet_uses_semantic_flush_atlas",
			toilet_sprite != null
			and bool(toilet_sprite.get_meta("busy", false))
			and toilet_sprite.texture == toilet_texture
			and expected_toilet_sheet != "res://"
			and toilet_texture.resource_path == expected_toilet_sheet
			and toilet_sprite.hframes * toilet_sprite.vframes >= 8
			and int(toilet_sprite.get_meta(
				"animation_frame_count", 0)) == 8
			and String(toilet_sprite.get_meta(
				"semantic_action", "")) == "flap_seat_and_flush"
			and bool(toilet_sprite.get_meta(
				"generated_full_object_states", false))
			and not bool(toilet_sprite.get_meta(
				"primary_animation_is_overlay", true))
			and String(toilet_data.get("sound", ""))
				== "castle/toilet_flush.ogg")
		var effect_count: int = main.castle_room_item_effect_layer.get_child_count()
		var toilet_water_layer: Dictionary = toilet_water[0] as Dictionary \
			if toilet_water.size() == 1 else {}
		var toilet_water_node: Sprite2D = toilet_water_layer.get(
			"node") as Sprite2D
		_ck("toilet_uses_bounded_fixture_water_not_generic_overlay",
			effect_count == 0
			and toilet_water.size() == 1
			and String(toilet_water_layer.get("role", "")) == "vortex"
			and toilet_water_node != null
			and toilet_water_node.get_parent() \
				== main.castle_room_item_visual_layer
			and bool(toilet_water_node.get_meta(
				"castle_fixture_water", false))
			and bool(toilet_water_node.get_meta(
				"bounded_to_fixture", false))
			and toilet_water_node is Sprite2D
			and not bool(toilet_water_node.get_meta(
				"logic_authority", true)))
		if toilet_button != null:
			toilet_button.emit_signal("pressed")
		await process_frame
		_ck("toilet_busy_guard",
			main.castle_room_item_effect_layer.get_child_count() == effect_count)
		var toilet_fixed_transform := true
		var toilet_wait_frames := 0
		var toilet_deadline_ms: int = Time.get_ticks_msec() + 3000
		while bool(toilet_sprite.get_meta("busy", false)) \
				and Time.get_ticks_msec() < toilet_deadline_ms:
			await process_frame
			toilet_wait_frames += 1
			toilet_fixed_transform = toilet_fixed_transform \
				and toilet_sprite.position.is_equal_approx(
					toilet_start_position) \
				and toilet_sprite.scale.is_equal_approx(toilet_start_scale) \
				and is_equal_approx(toilet_sprite.rotation,
					toilet_start_rotation)
		var toilet_expected_frames: Array[int] = []
		for toilet_frame_value: Variant in toilet_data.get(
				"timeline_sequence", []) as Array:
			toilet_expected_frames.append(int(toilet_frame_value))
		var toilet_expected_steps: Array[int] = []
		for toilet_step: int in range(toilet_expected_frames.size()):
			toilet_expected_steps.append(toilet_step)
		var toilet_visited: Array = toilet_sprite.get_meta(
			"animation_frames_visited", []) as Array
		var toilet_steps_visited: Array = toilet_sprite.get_meta(
			"animation_timeline_steps_visited", []) as Array
		_ck("toilet_seat_flap_flush_sequence_completes",
			Time.get_ticks_msec() < toilet_deadline_ms
			and toilet_expected_frames.size() >= 4
			and toilet_expected_frames.size() <= 12
			and toilet_visited == toilet_expected_frames
			and toilet_steps_visited == toilet_expected_steps
			and toilet_sprite.frame == int(toilet_data.get("rest_frame", 0))
			and not bool(toilet_sprite.get_meta("busy", true)))
		_ck("toilet_animation_keeps_fixture_pivot_fixed",
			toilet_fixed_transform)
		_ck("toilet_flush_sound",
			main.castle_room_prop_sfx.stream != null
			and main.castle_room_prop_sfx.stream.resource_path \
				== "res://assets/audio/castle/toilet_flush.ogg")
		_ck("decorations_do_not_award",
			not bool(main.g.get("crown_won", false)))
		rooms.show_room("library", false)
		await _frames(2)
		var sprite: Sprite2D = main.castle_room_player_sprite
		var mid_card: Sprite2D = (
			main.castle_room_item_sprites["pearl_table"] as Dictionary
			).get("sprite") as Sprite2D
		rooms._position_player_at_foot(Vector2(640.0, 540.0), false)
		_ck("sorts_behind_midground", sprite.z_index < mid_card.z_index)
		rooms._position_player_at_foot(Vector2(640.0, 556.0), false)
		_ck("sorts_in_front_of_midground", sprite.z_index > mid_card.z_index)
		rooms.show_room("main_hall", false)
		var royal_hall_button: Button = null
		for portal_record: Dictionary in main.castle_room_door_hotspots:
			var portal_data: Dictionary = portal_record.get("data", {})
			if String(portal_data.get("id", "")) == "__royal_hall":
				royal_hall_button = portal_record.get("button") as Button
				break
		_ck("royal_hall_route_available", royal_hall_button != null)
		if royal_hall_button != null:
			royal_hall_button.pressed.emit()
			var arrival_deadline_ms: int = Time.get_ticks_msec() \
				+ ROYAL_HALL_ARRIVAL_SETTLE_MS
			while Time.get_ticks_msec() < arrival_deadline_ms:
				await process_frame
	_ck("crown_won_flag", bool(main.g.get("crown_won", false)))
	_ck("win_recorded", main.level2_done_once)
	_ck("still_in_castle", main.game == "level2" and String(main.g.get("phase", "")) == "hall", "game=%s phase=%s" % [main.game, str(main.g.get("phase", ""))])
	var near: bool = (player.position - o).length() < 90.0
	_ck("not_ejected_to_ocean", near, "dist=%.0f" % (player.position - o).length())
	# Linger after the Royal Hall welcome: no re-trigger and no teleport.
	await _frames(60)
	_ck("no_retrigger_teleport", main.game == "level2" and (player.position - o).length() < 90.0)
	# The child-selected exit still leaves the castle for the courtyard.
	main._castle_rooms_ref()._exit_to_courtyard()
	await _frames(2)
	_ck("front_door_exits", String(main.g.get("phase", "")) != "hall",
		"phase=%s" % str(main.g.get("phase", "")))
	print("CROWN|done: ", ("OK" if checks_failed == 0 else "FAIL (%d)" % checks_failed))
	main.queue_free()
	await _frames(2)
	quit()
