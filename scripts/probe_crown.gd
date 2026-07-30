extends SceneTree
# Crown Star probe: touching the crown must CELEBRATE IN PLACE — win recorded,
# Roshan stays in her castle — instead of the old _finish_level2() ocean eject.
# The front-door exit must still return her to the courtyard when SHE chooses.
# Prints OK/FAIL lines (ci.sh convention).

var main: Node
var checks_failed := 0
const DEPTH_MANIFEST := "res://FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("CROWN|", label, ": ", ("OK" if ok else "FAIL"), (" " + detail if detail != "" else ""))

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _world_cards_conform(node: Node) -> bool:
	for child: Node in node.get_children():
		if child is CanvasItem:
			return false
		if child is MeshInstance3D or child is MultiMeshInstance3D \
				or child is CSGShape3D or child is Decal:
			return false
		if child is SpriteBase3D:
			if not child is Sprite3D:
				return false
			var sprite := child as Sprite3D
			var role := String(sprite.get_meta("source_asset_role", ""))
			if sprite.shaded and role not in [
				"clean_background_tile",
				"architectural_join_divider",
				"architectural_join_inlay",
				"architectural_bridge",
			]:
				return false
		if not _world_cards_conform(child):
			return false
	return true

func _visible_sprite_card_count(node: Node) -> int:
	var count := 0
	for child: Node in node.get_children():
		if child is Sprite3D and (child as Sprite3D).visible:
			count += 1
		count += _visible_sprite_card_count(child)
	return count

func _all_children_are_unshaded_cards(node: Node3D) -> bool:
	if node == null:
		return false
	for child: Node in node.get_children():
		if not child is Sprite3D or (child as Sprite3D).shaded:
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
		_ck("opera_lives_in_elevator_not_3d_courtyard",
			main.castle_room_buttons.has("opera_hall")
			and not main.g.has("opera_gate"))
		_ck("sprite3d_world_root", main.castle_room_world_root is Node3D)
		_ck("perspective_room_camera",
			main.castle_room_camera is Camera3D
			and main.castle_room_camera.projection
				== Camera3D.PROJECTION_PERSPECTIVE)
		_ck("world_has_no_canvas_or_mesh_art",
			_world_cards_conform(main.castle_room_world_root))
		_ck("backdrop_is_unshaded_sprite3d",
			main.castle_room_background is Sprite3D
			and not main.castle_room_background.shaded)
		var reference_ppm: float = 1.0 / main.castle_room_background.pixel_size
		var backdrop_size: Vector2 = main.castle_room_background.texture.get_size()
		_ck("reference_pixels_per_meter", absf(reference_ppm - 51.2) < 0.01,
			"ppm=%.3f" % reference_ppm)
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
			"world_art_forbidden", []) as Array
		_ck("manifest_sprite3d_node_contract",
			String(node_contract.get("world_root", "")) == "Node3D"
			and String(node_contract.get("camera", ""))
				== "Camera3D:perspective"
			and (node_contract.get("world_art_allowed", []) as Array).has(
				"Sprite3D:unshaded")
			and (node_contract.get("world_art_allowed", []) as Array).has(
				"Sprite3D:shaded lighting receiver")
			and forbidden_world_types.has("Sprite2D")
			and forbidden_world_types.has("TextureRect")
			and forbidden_world_types.has("MeshInstance3D"))
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
			var expected_tile_count := 8 if manifest_room_id == "main_hall" \
				else (12 if manifest_room_id == "kitchen" else 4)
			native_2k_ok = native_2k_ok \
				and bool(manifest_room.get(
					"native_master_compliant", false)) \
				and master_long_edge >= 2048 \
				and (manifest_room_id != "kitchen" \
					or master_short_edge >= 2048) \
				and float(manifest_room.get(
					"aspect_ratio_pixel_delta", 99.0)) <= 1.0 \
				and bool(manifest_room.get(
					"tile_reconstruction_pixel_exact", false)) \
				and runtime_tiles.size() == expected_tile_count
			for tile_value: Variant in runtime_tiles:
				var tile: Dictionary = tile_value as Dictionary
				var dimensions: Array = tile.get("dimensions", []) as Array
				native_2k_ok = native_2k_ok and dimensions.size() == 2 \
					and maxi(int(dimensions[0]), int(dimensions[1])) <= 1024
		_ck("native_2k_environment_gate", native_2k_ok,
			"native >=2K masters reconstruct through exact <=1024 tiles")
		rooms.show_room("library", false)
		await _frames(2)
		_ck("library_mid_layer", main.castle_room_mid_layer.get_child_count() == 0)
		_ck("library_front_layers", main.castle_room_front_layer.get_child_count() == 2)
		_ck("library_node_inventory",
			main.castle_room_background is Sprite3D
			and main.castle_room_background_tiles.size() == 8
			and main.castle_room_detail_tiles.size() == 4
			and main.castle_room_item_sprites.size() == 3
			and main.castle_room_front_layer.get_child_count() == 2
			and main.castle_room_player_sprite is Sprite3D
			and main.castle_room_player_shadow is Sprite3D)
		var library_book: Sprite3D = (
			main.castle_room_item_sprites["magic_book"] as Dictionary
			).get("sprite") as Sprite3D
		var library_table: Sprite3D = (
			main.castle_room_item_sprites["pearl_table"] as Dictionary
			).get("sprite") as Sprite3D
		_ck("library_depth_bands",
			main.castle_room_background.position.z
				< library_book.position.z
			and library_book.position.z < library_table.position.z
			and library_table.position.z
				< (main.castle_room_front_layer.get_child(0) as Sprite3D).position.z)
		var room_items_ok := true
		var room_cards_ok := true
		var room_depth_ok := true
		var overdraw_budget_ok := true
		for room_id: String in [
			"main_hall", "opera_hall", "kitchen", "library", "playroom",
			"craft_room", "mermaid_pool", "bubble_bath"]:
			rooms.show_room(room_id, false)
			await _frames(2)
			var hall_mode: bool = room_id == "main_hall"
			var expected_items: int = 11 if hall_mode else (
				7 if room_id == "kitchen" else 3)
			room_items_ok = room_items_ok \
				and main.castle_room_item_sprites.size() == expected_items \
				and main.castle_room_item_hotspot_layer.get_child_count() \
					== expected_items
			var item_depths: Dictionary = {}
			for item_id_value: Variant in main.castle_room_item_sprites:
				var item_record: Dictionary = main.castle_room_item_sprites[
					item_id_value] as Dictionary
				var item_sprite: Sprite3D = item_record.get("sprite") as Sprite3D
				item_depths[snappedf(item_sprite.position.z, 0.01)] = true
				room_depth_ok = room_depth_ok \
					and String(item_sprite.get_meta(
						"source_asset_role", "")) == "unique_object"
			room_depth_ok = room_depth_ok and item_depths.size() >= 2
			if room_id == "main_hall":
				room_depth_ok = room_depth_ok \
					and main.castle_room_background_tiles.size() == 8 \
					and main.castle_room_detail_tiles.is_empty()
			else:
				var expected_room_tiles: int = (
					12 if room_id == "kitchen" else 4)
				room_depth_ok = room_depth_ok \
					and main.castle_room_detail_tiles.size() \
						== expected_room_tiles \
					and String(main.castle_room_background.texture.resource_path
						).ends_with("_background.png")
			room_cards_ok = room_cards_ok \
				and _all_children_are_unshaded_cards(
					main.castle_room_item_visual_layer) \
				and _all_children_are_unshaded_cards(
					main.castle_room_front_layer) \
				and _world_cards_conform(main.castle_room_world_root)
			overdraw_budget_ok = overdraw_budget_ok \
				and _visible_sprite_card_count(
					main.castle_room_world_root) <= 26
		_ck("room_touch_inventory_matches_design", room_items_ok)
		_ck("all_room_art_uses_sprite3d_contract", room_cards_ok)
		_ck("objects_have_authored_real_depth", room_depth_ok)
		_ck("speedy_visible_card_budget", overdraw_budget_ok)
		rooms.show_room("bubble_bath", false)
		await _frames(2)
		var toilet_button: Button = main.castle_room_item_hotspot_layer.get_node_or_null(
			"Touch_toilet") as Button
		var toilet_record: Dictionary = main.castle_room_item_sprites.get("toilet", {})
		var toilet_sprite: Sprite3D = toilet_record.get("sprite") as Sprite3D
		main.castle_room_camera.position = Vector3(
			0.0, 0.0, CastleRooms25D.CAMERA_DISTANCE)
		rooms._update_touch_hotspots()
		var toilet_screen: Vector2 = main.castle_room_camera.unproject_position(
			toilet_sprite.global_position)
		var toilet_stage: Vector2 = rooms._screen_to_stage(toilet_screen)
		_ck("projected_touch_hit_mapping",
			toilet_button != null
			and Rect2(toilet_button.position, toilet_button.size).has_point(
				toilet_stage),
			"stage=%s hit=%s" % [
				str(toilet_stage),
				str(Rect2(toilet_button.position, toilet_button.size))])
		var front_card: Sprite3D = main.castle_room_front_layer.get_child(0) as Sprite3D
		var backdrop_x_before: float = main.castle_room_camera.unproject_position(
			main.castle_room_background.global_position).x
		var front_x_before: float = main.castle_room_camera.unproject_position(
			front_card.global_position).x
		main.castle_room_camera.position.x = 0.12
		var backdrop_shift: float = absf(
			main.castle_room_camera.unproject_position(
				main.castle_room_background.global_position).x
			- backdrop_x_before)
		var front_shift: float = absf(
			main.castle_room_camera.unproject_position(
				front_card.global_position).x - front_x_before)
		_ck("real_depth_parallax", front_shift > backdrop_shift + 0.05,
			"back=%.2f front=%.2f" % [backdrop_shift, front_shift])
		main.castle_room_camera.position = Vector3(
			0.0, 0.0, CastleRooms25D.CAMERA_DISTANCE)
		var walk_target := Vector2(260.0, 430.0)
		rooms._walk_cutout_to(_stage_to_screen(
			main.castle_room_stage, walk_target))
		var requested_foot: Vector2 = main.castle_room_player_sprite.get_meta(
			"stage_foot", Vector2.ZERO) as Vector2
		_ck("touch_navigation_maps_to_walk_lane",
			requested_foot.distance_to(walk_target) < 0.1)
		rooms._position_player_at_foot(requested_foot, false)
		var toilet_texture: Texture2D = toilet_sprite.texture
		if toilet_button != null:
			toilet_button.emit_signal("pressed")
		await process_frame
		_ck("toilet_button_animates", toilet_sprite != null
			and bool(toilet_sprite.get_meta("busy", false)))
		_ck("toilet_animation_preserves_frame",
			toilet_sprite.texture == toilet_texture)
		_ck("toilet_button_effects",
			main.castle_room_item_effect_layer.get_child_count() > 0
			and _all_children_are_unshaded_cards(
				main.castle_room_item_effect_layer))
		_ck("toilet_button_sound", main.castle_room_prop_sfx.stream != null
			and main.castle_room_prop_sfx.playing)
		var effect_count: int = main.castle_room_item_effect_layer.get_child_count()
		if toilet_button != null:
			toilet_button.emit_signal("pressed")
		await process_frame
		_ck("toilet_busy_guard",
			main.castle_room_item_effect_layer.get_child_count() == effect_count)
		_ck("decorations_do_not_award",
			not bool(main.g.get("crown_won", false)))
		rooms.show_room("library", false)
		await _frames(2)
		var sprite: Sprite3D = main.castle_room_player_sprite
		var mid_card: Sprite3D = (
			main.castle_room_item_sprites["pearl_table"] as Dictionary
			).get("sprite") as Sprite3D
		rooms._position_player_at_foot(Vector2(640.0, 540.0), false)
		_ck("sorts_behind_midground", sprite.position.z < mid_card.position.z)
		rooms._position_player_at_foot(Vector2(640.0, 556.0), false)
		_ck("sorts_in_front_of_midground", sprite.position.z > mid_card.position.z)
		rooms.show_room("main_hall", false)
		rooms.activate_current_room()
		await _frames(2)
	_ck("crown_won_flag", bool(main.g.get("crown_won", false)))
	_ck("win_recorded", main.level2_done_once)
	_ck("still_in_castle", main.game == "level2" and String(main.g.get("phase", "")) == "hall", "game=%s phase=%s" % [main.game, str(main.g.get("phase", ""))])
	var near: bool = (player.position - o).length() < 90.0
	_ck("not_ejected_to_ocean", near, "dist=%.0f" % (player.position - o).length())
	# linger near the throne — no re-trigger, no teleport
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
