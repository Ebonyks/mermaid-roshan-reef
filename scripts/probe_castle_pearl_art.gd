extends SceneTree
# Structural and visual acceptance probe for the picture-first Pearl Castle.
# The historical filename remains so CI callers do not change, but modeled
# pearl-kit geometry is now a regression: world art must remain Sprite3D. The
# main hall background is intentionally shaded so its touch-controlled
# SpotLight3D clusters can produce real depth and shadows.

const ROOM_IDS: Array[String] = [
	"main_hall", "opera_hall", "kitchen", "library", "playroom",
	"craft_room", "mermaid_pool", "bubble_bath",
]
const ROSHAN_ANCHORS := preload("res://scripts/roshan_sprite_anchors.gd")

var main: ReefMain
var checks_failed := 0

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("CASTLE_ART|", label, "|", "OK" if ok else "FAIL", "|", detail)

func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _audit_world_node(node: Node, counts: Dictionary) -> void:
	for child: Node in node.get_children():
		if child is Sprite3D:
			counts["sprite3d"] = int(counts.get("sprite3d", 0)) + 1
			var sprite := child as Sprite3D
			if sprite.visible:
				counts["visible_sprite3d"] = int(
					counts.get("visible_sprite3d", 0)) + 1
			if sprite.shaded:
				counts["shaded"] = int(counts.get("shaded", 0)) + 1
			if sprite.texture == null:
				counts["missing_texture"] = int(
					counts.get("missing_texture", 0)) + 1
			if bool(sprite.get_meta("castle_world_sprite3d", false)):
				var source_role: String = String(sprite.get_meta(
					"source_asset_role", ""))
				var alpha_ok: bool = (
					sprite.alpha_cut == SpriteBase3D.ALPHA_CUT_DISABLED
					if source_role == "portal_glow" else
					sprite.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD
					and is_equal_approx(
						sprite.alpha_scissor_threshold, 0.5)
				)
				if not alpha_ok:
					counts["bad_alpha_depth"] = int(
						counts.get("bad_alpha_depth", 0)) + 1
		elif child is MeshInstance3D or child is MultiMeshInstance3D \
				or child is CSGShape3D or child is Decal:
			counts["modeled"] = int(counts.get("modeled", 0)) + 1
		elif child is CanvasItem:
			counts["canvas_world"] = int(
				counts.get("canvas_world", 0)) + 1
		_audit_world_node(child, counts)

func _room_detail_tile_ready(tile: Sprite3D) -> bool:
	var native_size: Vector2 = tile.get_meta(
		"native_texture_size", Vector2.ZERO) as Vector2
	return (
		tile.visible
		and tile.texture != null
		and tile.texture.get_size() == native_size
		and maxf(native_size.x, native_size.y) <= 1024.0
		and tile.texture.resource_path.contains("rooms/background_tiles/")
	)

func _capture(room_id: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	# Capture the settled stage, not the intentional 0.24-second room fade.
	await _frames(20)
	await RenderingServer.frame_post_draw
	var output_dir := ProjectSettings.globalize_path(
		"res://audit/castle_sprite3d")
	DirAccess.make_dir_recursive_absolute(output_dir)
	var output_path := output_dir.path_join(room_id + ".png")
	var save_error: Error = root.get_viewport().get_texture().get_image() \
		.save_png(output_path)
	print("CASTLE_ART|capture|", output_path, "|error=", save_error)

func _run() -> void:
	var main_scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = main_scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	main._skip_intro()
	main.pearl_count = main.PEARL_TOTAL
	for friend_value: Variant in main.friends:
		var friend: Dictionary = friend_value
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(18)

	var rooms: CastleRooms25D = main._castle_rooms_ref()
	_ck("room_stage_open", rooms.is_open())
	_ck("perspective_depth_camera",
		main.castle_room_camera != null
		and main.castle_room_camera.projection
			== Camera3D.PROJECTION_PERSPECTIVE)
	_ck("legacy_3d_hall_not_instantiated",
		main.game_nodes.is_empty()
		and main.arena_solids.is_empty()
		and main.arena_zones.is_empty()
		and not main.g.has("hall_exit")
		and not main.g.has("opera_gate"))
	_ck("storybook_elevator_inventory",
		main.castle_room_buttons.size() == ROOM_IDS.size())
	var preview_count: int = 0
	for room_id: String in ROOM_IDS:
		var room_button: Button = main.castle_room_buttons.get(room_id) as Button
		var preview: TextureRect = null
		if room_button != null:
			preview = room_button.get_node_or_null(
				"RoomPreview") as TextureRect
		if preview != null and preview.texture != null \
				and preview.texture.get_size() == Vector2(400.0, 224.0) \
				and preview.texture.resource_path == (
					"res://assets/ui/castle_room_buttons/room_"
					+ room_id + ".png"):
			preview_count += 1
	_ck("storybook_elevator_room_previews",
		preview_count == ROOM_IDS.size(),
		"ready=%d/%d" % [preview_count, ROOM_IDS.size()])
	var castle_roshan: Sprite3D = main.castle_room_player_sprite
	var castle_roshan_loop: RoshanSpriteLoop = castle_roshan.get_node_or_null(
		"AlwaysAliveSpriteLoop") as RoshanSpriteLoop
	var castle_frame_height: float = castle_roshan.texture.get_height() \
		/ float(maxi(1, castle_roshan.vframes))
	_ck("castle_roshan_uses_primary_animated_sprite",
		castle_roshan_loop != null
		and castle_roshan.texture.resource_path.ends_with(
			"roshan_directional.png")
		and castle_roshan.hframes == 4
		and castle_roshan.vframes == 2
		and is_equal_approx(castle_frame_height, 256.0))
	var idle_offset: Vector2 = castle_roshan.offset
	castle_roshan_loop._process(0.3)
	_ck("castle_roshan_idle_never_freezes",
		castle_roshan_loop.animation_state() == "idle"
		and castle_roshan.offset != idle_offset,
		"state=%s offset=%s->%s" % [
			castle_roshan_loop.animation_state(), idle_offset,
			castle_roshan.offset])
	var walk_target := Vector2(500.0, 835.0)
	rooms._position_player_at_foot(walk_target, true)
	castle_roshan_loop._process(0.01)
	var moving_frame: int = castle_roshan.frame
	castle_roshan_loop._process(0.3)
	_ck("castle_roshan_swims_when_moving",
		bool(castle_roshan.get_meta("walking", false))
		and castle_roshan_loop.animation_state() == "swim"
		and castle_roshan.texture.resource_path.ends_with(
			"roshan_swim_front.png")
		and castle_roshan.vframes == 4
		and castle_roshan.frame != moving_frame,
		"state=%s frame=%d->%d" % [
			castle_roshan_loop.animation_state(),
			moving_frame, castle_roshan.frame])
	castle_roshan.flip_h = false
	var target_anchor: Vector2 = ROSHAN_ANCHORS.anchor("directional", 0)
	var max_anchor_drift := 0.0
	for frame_index: int in range(16):
		castle_roshan_loop._apply_frame(frame_index)
		var frame_anchor: Vector2 = ROSHAN_ANCHORS.anchor(
			"swim_front", frame_index)
		var frame_offset: Vector2 = castle_roshan.get_meta(
			"roshan_anchor_offset", Vector2.ZERO) as Vector2
		var corrected_anchor := Vector2(
			frame_anchor.x + frame_offset.x,
			frame_anchor.y - frame_offset.y)
		max_anchor_drift = maxf(
			max_anchor_drift, corrected_anchor.distance_to(target_anchor))
	_ck("castle_roshan_frames_share_anatomical_anchor",
		max_anchor_drift <= 0.11,
		"max_torso_drift_px=%.3f" % max_anchor_drift)
	rooms._position_player_at_foot(Vector2(380.0, 835.0), false)
	castle_roshan_loop._process(0.2)
	_ck("castle_roshan_swim_finishes_at_arrival",
		castle_roshan_loop.animation_state() == "idle"
		and castle_roshan.texture.resource_path.ends_with(
			"roshan_directional.png")
		and castle_roshan.vframes == 2,
		"state=%s texture=%s" % [
			castle_roshan_loop.animation_state(),
			castle_roshan.texture.resource_path])

	var all_rooms_ok := true
	var all_depth_ok := true
	var all_touch_animation_ok := true
	var all_touch_audio_ok := true
	var approved_composite_backdrops_ok := true
	var all_detail_tile_grids_ok := true
	var all_room_object_bounds_ok := true
	var kitchen_prop_set_ok := false
	var kitchen_individual_animation_ok := false
	var kitchen_fridge_glow_ok := false
	var kitchen_menu_empty_filter_ok := false
	var kitchen_menu_inventory_ok := false
	var kitchen_cooking_portal_ok := false
	var playroom_rescue_cards_ok := false
	var playroom_rescue_ray_ok := false
	var playroom_rescue_route_ok := false
	var max_visible_world_cards := 0
	for room_id: String in ROOM_IDS:
		rooms.show_room(room_id, false)
		await _frames(2)
		var counts: Dictionary = {}
		_audit_world_node(main.castle_room_world_root, counts)
		var visible_sprite_count := int(counts.get("visible_sprite3d", 0))
		max_visible_world_cards = maxi(
			max_visible_world_cards, visible_sprite_count)
		var hall_mode: bool = room_id == "main_hall"
		var expected_room_tiles: int = (
			12 if room_id == "kitchen" else 4)
		var expected_room_items: int = 7 if room_id == "kitchen" else (
			6 if room_id == "playroom"
				and not rooms._playroom_rescue_done() else 3)
		var background_ready: bool = (
			main.castle_room_background_tiles.size() == 8
			and main.castle_room_background_tiles.all(
				func(tile: Sprite3D) -> bool:
					return tile.visible and tile.texture != null)
			and not main.castle_room_background.visible
		) if hall_mode else (
			not main.castle_room_background.visible
			and main.castle_room_background.texture != null
			and main.castle_room_detail_tiles.size() == expected_room_tiles
			and main.castle_room_detail_tiles.all(_room_detail_tile_ready)
			and main.castle_room_background_tiles.all(
				func(tile: Sprite3D) -> bool:
					return not tile.visible)
		)
		var room_ok: bool = main.castle_room_id == room_id \
			and main.castle_room_background is Sprite3D \
			and not main.castle_room_background.shaded \
			and main.castle_room_item_sprites.size() \
				== (10 if hall_mode else expected_room_items) \
			and background_ready \
			and int(counts.get("modeled", 0)) == 0 \
			and int(counts.get("canvas_world", 0)) == 0 \
			and int(counts.get("bad_alpha_depth", 0)) == 0 \
			and int(counts.get("shaded", 0)) \
				== (9 if hall_mode else 8) \
			and int(counts.get("missing_texture", 0)) == 0
		var depths: Dictionary = {}
		if hall_mode:
			depths[snappedf(
				main.castle_room_background_tiles[0].position.z, 0.01)] = true
		else:
			depths[snappedf(
				main.castle_room_detail_tiles[0].position.z, 0.01)] = true
		for item_id_value: Variant in main.castle_room_item_sprites:
			var record: Dictionary = main.castle_room_item_sprites[
				item_id_value] as Dictionary
			var sprite: Sprite3D = record.get("sprite") as Sprite3D
			if sprite != null:
				depths[snappedf(sprite.position.z, 0.01)] = true
		for foreground: Node in main.castle_room_front_layer.get_children():
			depths[snappedf((foreground as Sprite3D).position.z, 0.01)] = true
		all_rooms_ok = all_rooms_ok and room_ok
		all_depth_ok = all_depth_ok and depths.size() >= 3
		if not hall_mode:
			approved_composite_backdrops_ok = \
				approved_composite_backdrops_ok \
				and main.castle_room_background.texture.resource_path \
					.ends_with("_background.png")
			var logical_rects: Array[Rect2] = []
			var logical_area := 0.0
			for detail_tile: Sprite3D in main.castle_room_detail_tiles:
				var logical_rect: Rect2 = detail_tile.get_meta(
					"source_art_rect", Rect2()) as Rect2
				for prior_rect: Rect2 in logical_rects:
					all_detail_tile_grids_ok = all_detail_tile_grids_ok \
						and not logical_rect.intersects(prior_rect)
				logical_rects.append(logical_rect)
				logical_area += logical_rect.get_area()
			all_detail_tile_grids_ok = all_detail_tile_grids_ok \
				and logical_rects.size() == expected_room_tiles \
				and is_equal_approx(logical_area, 1024.0 * 576.0)
			var canvas_rect := Rect2(0.0, 0.0, 1024.0, 576.0)
			for item_id_value: Variant in main.castle_room_item_sprites:
				var item_record: Dictionary = main.castle_room_item_sprites[
					item_id_value] as Dictionary
				var art_rect: Rect2 = item_record.get("art_rect", Rect2())
				all_room_object_bounds_ok = all_room_object_bounds_ok \
					and canvas_rect.encloses(art_rect)
		if room_id == "playroom":
			var eagle_record: Dictionary = main.castle_room_item_sprites.get(
				"baby_eagle_rescue", {}) as Dictionary
			var left_record: Dictionary = main.castle_room_item_sprites.get(
				"eagle_pin_left", {}) as Dictionary
			var right_record: Dictionary = main.castle_room_item_sprites.get(
				"eagle_pin_right", {}) as Dictionary
			var eagle: Sprite3D = eagle_record.get("sprite") as Sprite3D
			var left_bunny: Sprite3D = left_record.get("sprite") as Sprite3D
			var right_bunny: Sprite3D = right_record.get("sprite") as Sprite3D
			var rescue_pointer: Sprite3D = \
				main.castle_room_item_effect_layer.get_node_or_null(
					"BabyEagleRescuePointer") as Sprite3D
			playroom_rescue_cards_ok = (
				eagle != null
				and left_bunny != null
				and right_bunny != null
				and rescue_pointer != null
				and not eagle.shaded
				and not left_bunny.shaded
				and not right_bunny.shaded
				and not eagle.no_depth_test
				and not left_bunny.no_depth_test
				and not right_bunny.no_depth_test
				and eagle.position.z < left_bunny.position.z
				and eagle.position.z < right_bunny.position.z
				and left_record.get("hotspot") == null
				and right_record.get("hotspot") == null
				and String(left_bunny.get_meta(
					"dust_bunny_role", "")) == "playroom_pin_left"
				and String(right_bunny.get_meta(
					"dust_bunny_role", "")) == "playroom_pin_right"
				and String(eagle.texture.resource_path).ends_with(
					"assets/book/baby_eagle.png")
				and String(left_bunny.texture.resource_path).ends_with(
					"dust_bunnies/dust_bunny_hop.png")
				and String(right_bunny.texture.resource_path).ends_with(
					"dust_bunnies/dust_bunny_hop.png")
				and String(rescue_pointer.get_meta(
					"source_asset_role", "")) == "tutorial_pointer"
				and not main.castle_room_action_button.visible
			)
			playroom_rescue_ray_ok = true
			var playroom_walk: Rect2 = (
				CastleRooms25D.ROOM_LAYOUTS["playroom"] as Dictionary).get(
					"walk", Rect2()) as Rect2
			playroom_rescue_route_ok = true
			for bunny_record: Dictionary in [left_record, right_record]:
				var bunny: Sprite3D = bunny_record.get("sprite") as Sprite3D
				if bunny == null:
					playroom_rescue_ray_ok = false
					playroom_rescue_route_ok = false
					continue
				var screen_center: Vector2 = \
					main.castle_room_camera.unproject_position(
						bunny.global_position)
				var mapped_foot: Vector2 = \
					rooms._dust_bunny_foot_from_camera_ray(screen_center)
				var contact_foot: Vector2 = bunny_record.get(
					"contact_foot", Vector2.INF) as Vector2
				playroom_rescue_ray_ok = playroom_rescue_ray_ok \
					and mapped_foot != Vector2.INF \
					and mapped_foot.distance_to(contact_foot) <= 0.01
				playroom_rescue_route_ok = playroom_rescue_route_ok \
					and playroom_walk.has_point(contact_foot)
		await _capture(room_id)
		var item_keys: Array = main.castle_room_item_sprites.keys()
		var first_item_id: String = String(item_keys[0])
		var first_record: Dictionary = main.castle_room_item_sprites[
			first_item_id] as Dictionary
		var first_sprite: Sprite3D = first_record.get("sprite") as Sprite3D
		var start_position: Vector3 = first_sprite.position
		var start_scale: Vector3 = first_sprite.scale
		var start_rotation: float = first_sprite.rotation.z
		rooms._activate_room_item(first_item_id)
		await _frames(3)
		var first_item_animated: bool = \
			bool(first_sprite.get_meta("busy", false)) \
			and (
				first_sprite.position.distance_to(start_position) > 0.0001
				or first_sprite.scale.distance_to(start_scale) > 0.0001
				or absf(first_sprite.rotation.z - start_rotation) > 0.0001
			)
		all_touch_animation_ok = all_touch_animation_ok \
			and first_item_animated
		all_touch_audio_ok = all_touch_audio_ok \
			and main.castle_room_prop_sfx != null \
			and main.castle_room_prop_sfx.stream != null
		if room_id == "kitchen":
			var kitchen_ids: Array[String] = [
				"sink", "pan_1", "pan_2", "pan_3", "pan_4", "oven",
				"fridge",
			]
			kitchen_prop_set_ok = kitchen_ids.all(
				func(kitchen_id: String) -> bool:
					return main.castle_room_item_sprites.has(kitchen_id))
			kitchen_individual_animation_ok = first_item_animated
			var fridge_glow: Sprite3D = \
				main.castle_room_item_visual_layer.get_node_or_null(
					"PortalGlow_fridge") as Sprite3D
			kitchen_fridge_glow_ok = (
				fridge_glow != null
				and fridge_glow.texture != null
				and not fridge_glow.shaded
				and String(fridge_glow.get_meta(
					"source_asset_role", "")) == "portal_glow"
				and fridge_glow.modulate.a >= 0.12
				and fridge_glow.modulate.a <= 0.31
			)
			main.opera_pantry.erase("carrots")
			main.opera_pantry["sugar"] = 2
			for kitchen_id: String in kitchen_ids:
				if kitchen_id == first_item_id:
					continue
				var kitchen_record: Dictionary = \
					main.castle_room_item_sprites[kitchen_id] as Dictionary
				var kitchen_sprite: Sprite3D = \
					kitchen_record.get("sprite") as Sprite3D
				var kitchen_start_position: Vector3 = kitchen_sprite.position
				var kitchen_start_scale: Vector3 = kitchen_sprite.scale
				var kitchen_start_rotation: float = kitchen_sprite.rotation.z
				rooms._activate_room_item(kitchen_id)
				await _frames(3)
				kitchen_individual_animation_ok = \
					kitchen_individual_animation_ok \
					and bool(kitchen_sprite.get_meta("busy", false)) \
					and (
						kitchen_sprite.position.distance_to(
							kitchen_start_position) > 0.0001
						or kitchen_sprite.scale.distance_to(
							kitchen_start_scale) > 0.0001
						or absf(kitchen_sprite.rotation.z
							- kitchen_start_rotation) > 0.0001
					)
			var empty_pantry_label: Label = \
				rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenPantryInventory") as Label \
				if rooms.kitchen_menu_stage != null else null
			var empty_pantry_counts: Dictionary = empty_pantry_label.get_meta(
				"food_counts", {}) as Dictionary \
				if empty_pantry_label != null else {}
			kitchen_menu_empty_filter_ok = (
				rooms.kitchen_menu_layer != null
				and rooms.kitchen_menu_stage != null
				and rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenRecipe_pearl_cake") != null
				and rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenRecipe_carrot_cake") == null
				and int(empty_pantry_counts.get("carrots", 0)) == 0
				and int(empty_pantry_counts.get("sugar", 0)) == 2
			)
			rooms._close_kitchen_menu()
			await _frames(1)
			main.opera_pantry["carrots"] = 1
			rooms._open_kitchen_menu()
			await _frames(1)
			var pantry_label: Label = \
				rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenPantryInventory") as Label \
				if rooms.kitchen_menu_stage != null else null
			var pantry_counts: Dictionary = pantry_label.get_meta(
				"food_counts", {}) as Dictionary \
				if pantry_label != null else {}
			kitchen_menu_inventory_ok = (
				rooms.kitchen_menu_layer != null
				and rooms.kitchen_menu_stage != null
				and rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenRecipe_pearl_cake") != null
				and rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenRecipe_carrot_cake") != null
				and int(pantry_counts.get("carrots", 0)) == 1
				and int(pantry_counts.get("sugar", 0)) == 2
			)
			rooms._launch_kitchen_recipe("carrot_cake")
			await _frames(2)
			var kitchen_act: OperaAct = rooms.kitchen_act
			kitchen_cooking_portal_ok = (
				main.game == "kitchen_cooking"
				and kitchen_act != null
				and kitchen_act.kind == "order"
				and String(kitchen_act.config.get("uses", "")) == "carrots"
				and kitchen_act.stage_phase == "puzzle"
			)
			if kitchen_act != null:
				kitchen_act.cancel()
			await _frames(3)
			kitchen_cooking_portal_ok = kitchen_cooking_portal_ok \
				and rooms.kitchen_act == null \
				and main.game == "level2" \
				and main.castle_room_id == "kitchen" \
				and main.castle_room_layer.visible
	_ck("all_eight_rooms_sprite3d_only", all_rooms_ok)
	_ck("all_rooms_use_multiple_real_depths", all_depth_ok)
	_ck("approved_room_composites_preserved", approved_composite_backdrops_ok)
	_ck("all_destination_rooms_use_2k_exact_tile_grids",
		all_detail_tile_grids_ok)
	_ck("all_destination_room_objects_within_authored_canvas",
		all_room_object_bounds_ok)
	_ck("all_rooms_touch_animation_live", all_touch_animation_ok)
	_ck("all_rooms_touch_audio_live", all_touch_audio_ok)
	_ck("kitchen_seven_independent_props", kitchen_prop_set_ok)
	_ck("kitchen_each_prop_animation_live",
		kitchen_individual_animation_ok)
	_ck("kitchen_fridge_subtle_portal_glow", kitchen_fridge_glow_ok)
	_ck("kitchen_fridge_filters_missing_food",
		kitchen_menu_empty_filter_ok)
	_ck("kitchen_fridge_inventory_menu", kitchen_menu_inventory_ok)
	_ck("kitchen_fridge_launches_cooking_portal",
		kitchen_cooking_portal_ok)
	_ck("playroom_baby_eagle_rescue_depth_cards",
		playroom_rescue_cards_ok)
	_ck("playroom_bunny_camera_ray_touch_mapping",
		playroom_rescue_ray_ok)
	_ck("playroom_bunny_contacts_inside_navigation",
		playroom_rescue_route_ok)
	_ck("speedy_visible_card_budget", max_visible_world_cards <= 26,
		"maximum visible cards=%d" % max_visible_world_cards)

	rooms.show_room("main_hall", false)
	var castle_environment: Environment = main.castle_room_environment
	var expected_glow: float = 0.95 if main.quality == "speedy" else 1.28
	var expected_bloom: float = 0.18 if main.quality == "speedy" else 0.30
	var glow_on: float = castle_environment.glow_intensity \
		if castle_environment != null else 0.0
	var bloom_on: float = castle_environment.glow_bloom \
		if castle_environment != null else 0.0
	_ck("main_hall_dramatic_glow_environment",
		castle_environment != null
		and main.we_node != null
		and main.we_node.environment == castle_environment
		and castle_environment.glow_enabled
		and castle_environment.glow_blend_mode
			== Environment.GLOW_BLEND_MODE_SCREEN
		and is_equal_approx(glow_on, expected_glow)
		and is_equal_approx(bloom_on, expected_bloom)
		and castle_environment.glow_hdr_threshold <= 0.59
		and castle_environment.glow_hdr_scale >= 4.1
		and castle_environment.adjustment_contrast >= 1.13
		and castle_environment.adjustment_brightness >= 1.04
		and castle_environment.ambient_light_energy <= 0.33,
		"quality=%s glow=%.3f bloom=%.3f threshold=%.3f" % [
			main.quality, glow_on, bloom_on,
			castle_environment.glow_hdr_threshold
				if castle_environment != null else 0.0])
	var original_quality: String = main.quality
	main.quality = "speedy"
	rooms._sync_hall_lighting()
	var speedy_shadow_count := 0
	for speedy_light: Light3D in main.castle_room_light_nodes:
		if speedy_light.visible and speedy_light.shadow_enabled:
			speedy_shadow_count += 1
	_ck("main_hall_speedy_glow_budget",
		castle_environment.glow_intensity <= 0.951
		and castle_environment.glow_bloom <= 0.181
		and speedy_shadow_count <= 1,
		"glow=%.3f bloom=%.3f shadows=%d" % [
			castle_environment.glow_intensity,
			castle_environment.glow_bloom, speedy_shadow_count])
	main.quality = original_quality
	rooms._sync_hall_lighting()
	var tile_paths_ok := true
	var tile_registration_ok := true
	var tile_index := 0
	for tile: Sprite3D in main.castle_room_background_tiles:
		var tile_row: int = tile_index / 4
		var tile_column: int = tile_index % 4
		var source_rect: Rect2 = tile.get_meta(
			"source_art_rect", Rect2()) as Rect2
		var master_rect: Rect2 = tile.get_meta(
			"source_master_rect", Rect2()) as Rect2
		var render_rect: Rect2 = tile.get_meta(
			"render_art_rect", Rect2()) as Rect2
		var bleed_pixels: int = int(tile.get_meta(
			"runtime_seam_bleed_pixels", -1))
		var source_path: String = tile.texture.resource_path
		tile_paths_ok = tile_paths_ok \
			and tile.texture != null \
			and source_path.contains("main_hall_2screen/tiles/") \
			and (
				source_path.contains("/runtime_bleed/") \
				and source_path.ends_with("_bleed.png")
				if tile_row == 0 else
				not source_path.contains("/runtime_bleed/")
			) \
			and tile.texture.get_size() == Vector2(836.0, 471.0) \
			and source_rect.size == Vector2(
				836.0, 470.0 if tile_row == 0 else 471.0) \
			and render_rect.size == Vector2(836.0, 471.0) \
			and bleed_pixels == (1 if tile_row == 0 else 0) \
			and tile.shaded and tile.transparent \
			and tile.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD \
			and is_equal_approx(tile.alpha_scissor_threshold, 0.5) \
			and tile.texture_filter == BaseMaterial3D.TEXTURE_FILTER_LINEAR
		var expected_master_y: float = (
			212.0 if tile_column < 2 else 147.0
		) + (0.0 if tile_row == 0 else 470.0)
		var expected_master_x: float = 376.0 \
			+ float(tile_column % 2) * 836.0
		tile_registration_ok = tile_registration_ok \
			and master_rect == Rect2(
				expected_master_x, expected_master_y,
				836.0, 470.0 if tile_row == 0 else 471.0) \
			and String(tile.get_meta("source_screen_id", "")) \
				== ("a" if tile_column < 2 else "b")
		tile_index += 1
	_ck("main_hall_native_2x4_sprite3d_grid",
		main.castle_room_background_tiles.size() == 8 and tile_paths_ok)
	_ck("main_hall_lossless_screen_registration",
		tile_registration_ok,
		"A_y=212 B_y=147 fixture_and_walkway_delta=65")
	var bridge: Sprite3D = main.castle_room_mid_layer.get_node_or_null(
		"HallStructure_playroom_portal_bridge") as Sprite3D
	var join_column: Sprite3D = main.castle_room_mid_layer.get_node_or_null(
		"HallStructure_screen_join_column") as Sprite3D
	var join_inlay: Sprite3D = main.castle_room_mid_layer.get_node_or_null(
		"HallStructure_screen_join_floor_inlay") as Sprite3D
	var playroom_marker: Sprite3D = main.castle_room_mid_layer.get_node_or_null(
		"HallStructure_playroom_portal_marker") as Sprite3D
	var playroom_portal_ok := false
	for portal_record: Dictionary in main.castle_room_door_hotspots:
		var portal_data: Dictionary = portal_record.get("data", {})
		if String(portal_data.get("id", "")) == "playroom":
			var portal_rect: Rect2 = portal_data.get("rect", Rect2())
			playroom_portal_ok = portal_rect.size.x >= 224.0 \
				and portal_rect.size.y >= 380.0
			break
	var bridge_material: ShaderMaterial = bridge.material_override \
		as ShaderMaterial if bridge != null else null
	_ck("main_hall_screen_join_uses_transparent_portal_cutout",
		bridge != null and bridge.texture != null and not bridge.shaded
		and bridge_material != null and bridge_material.shader != null
		and bridge_material.shader.resource_path.ends_with(
			"castle_portal_cutout.gdshader")
		and bool(bridge.get_meta("castle_transparent_portal_cutout", false))
		and join_column == null
		and join_inlay != null and join_inlay.texture != null
		and join_inlay.texture.resource_path.ends_with(
			"castle_join_floor_inlay_reuse.png")
		and playroom_marker != null and playroom_marker.texture != null
		and not playroom_marker.shaded and playroom_portal_ok)
	var light_inventory_ok: bool = main.castle_room_light_nodes.size() == 5
	var visible_lights := 0
	var visible_shadow_lights := 0
	var touch_light_energy_ok := true
	var fill_on_energy := 0.0
	for light: Light3D in main.castle_room_light_nodes:
		light_inventory_ok = light_inventory_ok \
			and light != null and is_instance_valid(light)
		var light_role: String = String(light.get_meta(
			"castle_light_role", ""))
		if light_role == "ambient_fill":
			fill_on_energy = light.light_energy
		elif light_role == "touch_cluster":
			touch_light_energy_ok = touch_light_energy_ok \
				and is_equal_approx(float(
					light.get_meta("max_energy", 0.0)), 4.6)
		if light.visible:
			visible_lights += 1
			if light.shadow_enabled:
				visible_shadow_lights += 1
	_ck("main_hall_mobile_light_pool",
		light_inventory_ok and visible_lights <= 3
		and visible_shadow_lights >= 1 and visible_shadow_lights <= 2,
		"visible=%d shadowed=%d" % [visible_lights, visible_shadow_lights])
	_ck("main_hall_equal_cluster_energy",
		touch_light_energy_ok and is_equal_approx(fill_on_energy, 0.78),
		"fill=%.3f" % fill_on_energy)
	var fixture_asset_path := ""
	var fixture_continuity_ok := true
	var fixture_y: float = -1.0
	var fixture_height_ok := true
	var fixture_bloom_emitters_ok := true
	var fixture_single_card_ok := true
	for fixture_id: String in [
			"sconce_a0", "sconce_a1", "sconce_a2",
			"sconce_b0", "sconce_b1", "sconce_b2"]:
		var fixture_record: Dictionary = main.castle_room_item_sprites.get(
			fixture_id, {})
		var fixture: Sprite3D = fixture_record.get("sprite") as Sprite3D
		if fixture == null or fixture.texture == null:
			fixture_continuity_ok = false
			fixture_bloom_emitters_ok = false
			fixture_single_card_ok = false
			continue
		var fixture_material: ShaderMaterial = \
			fixture.material_override as ShaderMaterial
		var emission_energy: float = float(
			fixture_material.get_shader_parameter("emission_energy")) \
			if fixture_material != null else 0.0
		fixture_bloom_emitters_ok = fixture_bloom_emitters_ok \
			and bool(fixture.get_meta("castle_bloom_emitter", false)) \
			and emission_energy >= 3.8 \
			and is_equal_approx(float(fixture.get_meta(
				"castle_emission_energy", 0.0)), emission_energy) \
			and fixture_material != null \
			and fixture_material.shader != null \
			and fixture_material.shader.resource_path.ends_with(
				"castle_fixture_bloom.gdshader")
		fixture_single_card_ok = fixture_single_card_ok \
			and fixture.get_child_count() == 0 \
			and fixture.modulate == Color.WHITE \
			and not fixture.shaded \
			and fixture.cast_shadow \
				== GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		var path: String = fixture.texture.resource_path
		if fixture_asset_path == "":
			fixture_asset_path = path
			fixture_continuity_ok = fixture_continuity_ok \
				and path.ends_with(
					"castle_shell_sconce_touchable.png")
		else:
			fixture_continuity_ok = fixture_continuity_ok \
				and path == fixture_asset_path
		var fixture_record_data: Dictionary = fixture_record.get("data", {})
		var fixture_position: Vector2 = fixture_record_data.get(
			"pos", Vector2.ZERO)
		if fixture_y < 0.0:
			fixture_y = fixture_position.y
		else:
			fixture_height_ok = fixture_height_ok \
				and is_equal_approx(fixture_position.y, fixture_y)
	for tapestry_id: String in ["tapestry_right"]:
		var tapestry_record: Dictionary = main.castle_room_item_sprites.get(
			tapestry_id, {})
		var tapestry: Sprite3D = tapestry_record.get("sprite") as Sprite3D
		fixture_continuity_ok = fixture_continuity_ok \
			and tapestry != null and tapestry.texture != null \
			and tapestry.texture.resource_path.ends_with(
				"castle_royal_tapestry_reuse.png")
	_ck("main_hall_fixture_and_tapestry_continuity", fixture_continuity_ok)
	_ck("main_hall_fixture_height_alignment",
		fixture_height_ok and is_equal_approx(fixture_y, 215.0),
		"shared_y=%.1f" % fixture_y)
	_ck("main_hall_fixture_hdr_bloom_emitters",
		fixture_bloom_emitters_ok)
	_ck("main_hall_fixture_single_sprite3d_cards",
		fixture_single_card_ok)
	var hall_door_clearance_ok := true
	var hall_door_conflicts: Array[String] = []
	for item_id_value: Variant in main.castle_room_item_sprites:
		var item_record: Dictionary = main.castle_room_item_sprites[
			item_id_value] as Dictionary
		var item_rect: Rect2 = item_record.get("art_rect", Rect2())
		for portal_index: int in main.castle_room_door_hotspots.size():
			var portal_record: Dictionary = main.castle_room_door_hotspots[
				portal_index]
			var portal_data: Dictionary = portal_record.get("data", {})
			var portal_rect: Rect2 = portal_data.get("rect", Rect2())
			var approach_rect := Rect2(
				portal_rect.position.x,
				maxf(315.0, portal_rect.position.y),
				portal_rect.size.x,
				720.0 - maxf(315.0, portal_rect.position.y))
			if item_rect.intersects(approach_rect):
				hall_door_clearance_ok = false
				hall_door_conflicts.append(
					"%s:%s:portal_%d" % [
						String(item_id_value), item_rect, portal_index])
	_ck("main_hall_objects_clear_all_door_approaches",
		hall_door_clearance_ok, ",".join(hall_door_conflicts))
	rooms._position_player_at_foot(Vector2(1672.0, 835.0), false)
	await _frames(2)
	rooms.tick(1.0)
	var seam_a_lights := 0
	var seam_b_lights := 0
	for seam_light: Light3D in main.castle_room_light_nodes:
		if not seam_light.visible \
				or String(seam_light.get_meta(
					"castle_light_role", "")) != "touch_cluster":
			continue
		if String(seam_light.get_meta("hall_half", "")) == "a":
			seam_a_lights += 1
		elif String(seam_light.get_meta("hall_half", "")) == "b":
			seam_b_lights += 1
	_ck("main_hall_seam_uses_cross_screen_lights",
		seam_a_lights == 1 and seam_b_lights == 1,
		"A=%d B=%d" % [seam_a_lights, seam_b_lights])
	await _capture("main_hall_seam_bridge")
	rooms._position_player_at_foot(Vector2(380.0, 835.0), false)
	await _frames(2)
	rooms.tick(1.0)
	var sconce_record: Dictionary = main.castle_room_item_sprites.get(
		"sconce_a0", {})
	var sconce: Sprite3D = sconce_record.get("sprite") as Sprite3D
	var sconce_started_on: bool = sconce != null \
		and bool(sconce.get_meta("castle_light_on", false))
	rooms._activate_room_item("sconce_a0")
	await _frames(3)
	var sconce_toggled_off: bool = sconce != null \
		and not bool(sconce.get_meta("castle_light_on", true)) \
		and not bool(main.castle_room_light_states.get("sconce_a0", true))
	_ck("main_hall_touch_lighting_engine",
		sconce_started_on and sconce_toggled_off)
	rooms._activate_room_item("sconce_a1")
	rooms._activate_room_item("sconce_a2")
	await _frames(3)
	rooms._sync_hall_lighting()
	var a_spotlights_visible := 0
	for light: Light3D in main.castle_room_light_nodes:
		if light.visible and String(light.get_meta("hall_half", "")) == "a":
			a_spotlights_visible += 1
	_ck("main_hall_all_lights_off_affects_engine",
		a_spotlights_visible == 0)
	var fill_off_energy := 1.0
	for light: Light3D in main.castle_room_light_nodes:
		if String(light.get_meta("castle_light_role", "")) == "ambient_fill":
			fill_off_energy = light.light_energy
	var glow_off: float = castle_environment.glow_intensity
	var bloom_off: float = castle_environment.glow_bloom
	_ck("main_hall_bloom_tracks_light_state",
		glow_off <= 0.25 and bloom_off <= 0.02
		and glow_off < glow_on and bloom_off < bloom_on
		and fill_off_energy < fill_on_energy,
		"on=%.3f/%.3f off=%.3f/%.3f fill=%.3f->%.3f" % [
			glow_on, bloom_on, glow_off, bloom_off,
			fill_on_energy, fill_off_energy])
	await _capture("main_hall_lights_off")
	_ck("main_hall_physical_portal_inventory",
		main.castle_room_door_hotspots.size() == 8
		and main.castle_room_door_hotspot_layer != null
		and main.castle_room_door_hotspot_layer.visible)
	var bunny_ids: Array[String] = [
		"sleepy_bunny", "shell_bunny", "runner_bunny"]
	var expected_bunny_roles := {
		"sleepy_bunny": "sleeping_static",
		"shell_bunny": "shell_static",
		"runner_bunny": "runner",
	}
	var bunny_assets_ok := true
	var bunny_start_positions: Dictionary = {}
	for item_id: String in bunny_ids:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {})
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		bunny_assets_ok = bunny_assets_ok \
			and sprite != null \
			and sprite.texture != null \
			and sprite.texture.resource_path.contains("dust_bunnies/") \
			and not sprite.shaded \
			and not sprite.no_depth_test \
			and record.get("hotspot") == null \
			and String(sprite.get_meta("dust_bunny_role", "")) \
				== String(expected_bunny_roles[item_id]) \
			and String(sprite.get_meta("spawn_guide_id", "")) == item_id
		if sprite != null:
			bunny_start_positions[item_id] = sprite.position
	_ck("main_hall_three_depth_card_dust_bunnies", bunny_assets_ok)
	_ck("main_hall_bunnies_are_proximity_only",
		main.castle_room_item_hotspot_layer.get_child_count() == 7)
	var camera_ray_touch_ok := true
	var camera_ray_details: Array[String] = []
	for item_id: String in bunny_ids:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {}) \
			as Dictionary
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		if sprite == null:
			camera_ray_touch_ok = false
			camera_ray_details.append(item_id + ":missing")
			continue
		var center_screen: Vector2 = main.castle_room_camera.unproject_position(
			sprite.global_position)
		var ray_origin: Vector3 = main.castle_room_camera.project_ray_origin(
			center_screen)
		var ray_direction: Vector3 = main.castle_room_camera.project_ray_normal(
			center_screen)
		var sprite_distance: float = (
			sprite.global_position - ray_origin).dot(ray_direction)
		var sprite_ray_point: Vector3 = \
			ray_origin + ray_direction * sprite_distance
		var ray_error: float = sprite_ray_point.distance_to(
			sprite.global_position)
		var contact_foot: Vector2 = record.get(
			"contact_foot", Vector2.ZERO) as Vector2
		var mapped_foot: Vector2 = rooms._dust_bunny_foot_from_camera_ray(
			center_screen)
		var foot_error: float = mapped_foot.distance_to(contact_foot)
		camera_ray_touch_ok = camera_ray_touch_ok \
			and ray_error <= 0.01 \
			and mapped_foot != Vector2.INF \
			and foot_error <= 0.01
		camera_ray_details.append(
			"%s:ray=%.4f foot=%.4f mapped=%s" % [
				item_id, ray_error, foot_error, mapped_foot])
	_ck("main_hall_bunny_camera_ray_touch_mapping", camera_ray_touch_ok,
		";".join(camera_ray_details))
	var elevator_clearance_ok := true
	var elevator_art_rects: Array[Rect2] = [
		Rect2(1450.0, 700.0, 200.0, 230.0),
		Rect2(3122.0, 700.0, 200.0, 230.0),
	]
	for item_id: String in bunny_ids:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {})
		var art_rect: Rect2 = record.get("art_rect", Rect2())
		for elevator_rect: Rect2 in elevator_art_rects:
			elevator_clearance_ok = elevator_clearance_ok \
				and not art_rect.intersects(elevator_rect)
	_ck("main_hall_dust_bunnies_clear_fixed_elevator", elevator_clearance_ok)
	rooms.tick(0.5)
	var sleepy_record: Dictionary = main.castle_room_item_sprites.get(
		"sleepy_bunny", {}) as Dictionary
	var shell_record: Dictionary = main.castle_room_item_sprites.get(
		"shell_bunny", {}) as Dictionary
	var runner_record: Dictionary = main.castle_room_item_sprites.get(
		"runner_bunny", {}) as Dictionary
	var sleepy_now: Sprite3D = sleepy_record.get("sprite") as Sprite3D
	var shell_now: Sprite3D = shell_record.get("sprite") as Sprite3D
	var runner_now: Sprite3D = runner_record.get("sprite") as Sprite3D
	var static_bunnies_ok: bool = sleepy_now != null and shell_now != null
	if static_bunnies_ok:
		var sleepy_start: Vector3 = bunny_start_positions.get(
			"sleepy_bunny", Vector3.INF) as Vector3
		var shell_start: Vector3 = bunny_start_positions.get(
			"shell_bunny", Vector3.INF) as Vector3
		static_bunnies_ok = sleepy_now.position == sleepy_start \
			and shell_now.position == shell_start
	_ck("main_hall_two_static_dust_bunnies", static_bunnies_ok)
	var runner_moves_ok: bool = runner_now != null
	if runner_moves_ok:
		var runner_start: Vector3 = bunny_start_positions.get(
			"runner_bunny", Vector3.INF) as Vector3
		runner_moves_ok = runner_now.position.distance_to(runner_start) > 0.01
	_ck("main_hall_third_dust_bunny_runs", runner_moves_ok)
	var explosion_effects_before: int = \
		main.castle_room_item_effect_layer.get_child_count()
	var one_touch_explosions_ok := true
	for item_id: String in bunny_ids:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {})
		var bunny_sprite: Sprite3D = record.get("sprite") as Sprite3D
		var contact_foot: Vector2 = record.get(
			"contact_foot", Vector2.ZERO) as Vector2
		rooms._position_player_at_foot(contact_foot, false)
		rooms.tick(0.016)
		one_touch_explosions_ok = one_touch_explosions_ok \
			and bunny_sprite != null \
			and bool(bunny_sprite.get_meta("exploding", false)) \
			and not main.castle_room_item_sprites.has(item_id) \
			and bool((main.g.get(
				"castle_dust_bunnies_cleared", {}) as Dictionary).get(
					item_id, false))
	_ck("main_hall_one_touch_dust_bunny_explosions",
		one_touch_explosions_ok \
		and main.castle_room_item_effect_layer.get_child_count() \
			>= explosion_effects_before + bunny_ids.size() * 12)
	var cleared_count_before_repeat: int = (
		main.g.get("castle_dust_bunnies_cleared", {}) as Dictionary).size()
	for item_id: String in bunny_ids:
		rooms._explode_dust_bunny(item_id)
	_ck("main_hall_dust_bunny_explosions_exactly_once",
		(main.g.get("castle_dust_bunnies_cleared", {}) as Dictionary).size()
			== cleared_count_before_repeat
		and cleared_count_before_repeat == 3)
	rooms.show_room("library", false)
	rooms.show_room("main_hall", false)
	_ck("main_hall_dust_bunnies_do_not_respawn_this_visit",
		main.castle_room_item_sprites.size() == 7
		and main.castle_room_item_hotspot_layer.get_child_count() == 7)
	rooms._position_player_at_foot(Vector2(2500.0, 835.0), false)
	await _frames(2)
	rooms.tick(1.0)
	_ck("main_hall_two_screen_camera_travel",
		main.castle_room_camera.position.x > 5.0,
		"camera_x=%.2f" % main.castle_room_camera.position.x)
	await _capture("main_hall_screen_b")
	rooms._toggle_menu()
	await _capture("elevator_menu")
	rooms._toggle_menu()

	# Opera has exactly one route: its room button/action in the elevator. The
	# activity must return to the same Sprite3D room when it closes.
	rooms.show_room("opera_hall", false)
	rooms.activate_current_room()
	await _frames(40)
	var opera_opened: bool = main.game == "opera" and main.opera_game != null
	_ck("opera_opens_from_elevator", opera_opened)
	if opera_opened:
		main.opera_game._leave_early()
		await _frames(6)
	_ck("opera_returns_to_sprite_room",
		main.game == "level2"
		and String(main.g.get("phase", "")) == "hall"
		and rooms.is_open()
		and main.castle_room_id == "opera_hall")
	var environment_before_suspend: Environment = \
		main.castle_room_previous_environment
	rooms.suspend()
	_ck("castle_environment_restores_on_suspend",
		main.we_node.environment == environment_before_suspend)
	rooms.resume()
	_ck("castle_environment_reactivates_on_resume",
		main.we_node.environment == main.castle_room_environment)

	print("CASTLE_ART|RESULT=", "FAIL" if checks_failed > 0 else "OK",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)

func _init() -> void:
	call_deferred("_run")
