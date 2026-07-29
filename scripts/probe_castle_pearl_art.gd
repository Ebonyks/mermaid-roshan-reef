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
		elif child is MeshInstance3D or child is MultiMeshInstance3D \
				or child is CSGShape3D or child is Decal:
			counts["modeled"] = int(counts.get("modeled", 0)) + 1
		elif child is CanvasItem:
			counts["canvas_world"] = int(
				counts.get("canvas_world", 0)) + 1
		_audit_world_node(child, counts)

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

	var all_rooms_ok := true
	var all_depth_ok := true
	var all_touch_animation_ok := true
	var all_touch_audio_ok := true
	var approved_composite_backdrops_ok := true
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
		var background_ready: bool = (
			main.castle_room_background_tiles.size() == 8
			and main.castle_room_background_tiles.all(
				func(tile: Sprite3D) -> bool:
					return tile.visible and tile.texture != null)
			and not main.castle_room_background.visible
		) if hall_mode else (
			main.castle_room_background.visible
			and main.castle_room_background.texture != null
			and main.castle_room_background_tiles.all(
				func(tile: Sprite3D) -> bool:
					return not tile.visible)
		)
		var room_ok: bool = main.castle_room_id == room_id \
			and main.castle_room_background is Sprite3D \
			and not main.castle_room_background.shaded \
			and main.castle_room_item_sprites.size() \
				== (11 if hall_mode else 3) \
			and background_ready \
			and int(counts.get("modeled", 0)) == 0 \
			and int(counts.get("canvas_world", 0)) == 0 \
			and int(counts.get("shaded", 0)) \
				== (9 if hall_mode else 8) \
			and int(counts.get("missing_texture", 0)) == 0
		var depths: Dictionary = {}
		if hall_mode:
			depths[snappedf(
				main.castle_room_background_tiles[0].position.z, 0.01)] = true
		else:
			depths[snappedf(
				main.castle_room_background.position.z, 0.01)] = true
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
				and not main.castle_room_background.texture.resource_path \
					.contains("_background")
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
		all_touch_animation_ok = all_touch_animation_ok \
			and bool(first_sprite.get_meta("busy", false)) \
			and (
				first_sprite.position.distance_to(start_position) > 0.0001
				or first_sprite.scale.distance_to(start_scale) > 0.0001
				or absf(first_sprite.rotation.z - start_rotation) > 0.0001
			)
		all_touch_audio_ok = all_touch_audio_ok \
			and main.castle_room_prop_sfx != null \
			and main.castle_room_prop_sfx.stream != null
	_ck("all_eight_rooms_sprite3d_only", all_rooms_ok)
	_ck("all_rooms_use_multiple_real_depths", all_depth_ok)
	_ck("approved_room_composites_preserved", approved_composite_backdrops_ok)
	_ck("all_rooms_touch_animation_live", all_touch_animation_ok)
	_ck("all_rooms_touch_audio_live", all_touch_audio_ok)
	_ck("speedy_visible_card_budget", max_visible_world_cards <= 26,
		"maximum visible cards=%d" % max_visible_world_cards)

	rooms.show_room("main_hall", false)
	var tile_paths_ok := true
	for tile: Sprite3D in main.castle_room_background_tiles:
		tile_paths_ok = tile_paths_ok \
			and tile.texture != null \
			and tile.texture.resource_path.contains(
				"main_hall_2screen/tiles/main_hall_room_led_") \
			and tile.shaded
	_ck("main_hall_native_2x4_sprite3d_grid",
		main.castle_room_background_tiles.size() == 8 and tile_paths_ok)
	var bridge: Sprite3D = main.castle_room_mid_layer.get_node_or_null(
		"HallStructure_playroom_portal_bridge") as Sprite3D
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
	_ck("main_hall_screen_join_architectural_bridge",
		bridge != null and bridge.texture != null and bridge.shaded
		and bridge.texture.resource_path.ends_with(
			"castle_playroom_portal_reuse.png")
		and playroom_marker != null and playroom_marker.texture != null
		and not playroom_marker.shaded and playroom_portal_ok)
	var light_inventory_ok: bool = main.castle_room_light_nodes.size() == 5
	var visible_lights := 0
	var visible_shadow_lights := 0
	for light: Light3D in main.castle_room_light_nodes:
		light_inventory_ok = light_inventory_ok \
			and light != null and is_instance_valid(light)
		if light.visible:
			visible_lights += 1
			if light.shadow_enabled:
				visible_shadow_lights += 1
	_ck("main_hall_mobile_light_pool",
		light_inventory_ok and visible_lights <= 3
		and visible_shadow_lights >= 1 and visible_shadow_lights <= 2,
		"visible=%d shadowed=%d" % [visible_lights, visible_shadow_lights])
	var fixture_asset_path := ""
	var fixture_continuity_ok := true
	for fixture_id: String in [
			"sconce_a0", "sconce_a1", "sconce_a2",
			"sconce_b0", "sconce_b1", "sconce_b2"]:
		var fixture_record: Dictionary = main.castle_room_item_sprites.get(
			fixture_id, {})
		var fixture: Sprite3D = fixture_record.get("sprite") as Sprite3D
		if fixture == null or fixture.texture == null:
			fixture_continuity_ok = false
			continue
		var path: String = fixture.texture.resource_path
		if fixture_asset_path == "":
			fixture_asset_path = path
			fixture_continuity_ok = fixture_continuity_ok \
				and path.ends_with("castle_sconce_glow_reuse.png")
		else:
			fixture_continuity_ok = fixture_continuity_ok \
				and path == fixture_asset_path
	for tapestry_id: String in ["tapestry_right"]:
		var tapestry_record: Dictionary = main.castle_room_item_sprites.get(
			tapestry_id, {})
		var tapestry: Sprite3D = tapestry_record.get("sprite") as Sprite3D
		fixture_continuity_ok = fixture_continuity_ok \
			and tapestry != null and tapestry.texture != null \
			and tapestry.texture.resource_path.ends_with(
				"castle_royal_tapestry_reuse.png")
	_ck("main_hall_fixture_and_tapestry_continuity", fixture_continuity_ok)
	rooms._position_player_at_foot(Vector2(1672.0, 835.0), false)
	await _frames(2)
	rooms.tick(1.0)
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
	await _capture("main_hall_lights_off")
	_ck("main_hall_physical_portal_inventory",
		main.castle_room_door_hotspots.size() == 8
		and main.castle_room_door_hotspot_layer != null
		and main.castle_room_door_hotspot_layer.visible)
	var bunny_assets_ok := true
	for item_id: String in [
			"sleepy_bunny", "shell_bunny", "hop_bunny", "bunny_family"]:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {})
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		bunny_assets_ok = bunny_assets_ok \
			and sprite != null \
			and sprite.texture != null \
			and sprite.texture.resource_path.contains("dust_bunnies/") \
			and not sprite.shaded
	_ck("main_hall_lower_lane_interactions", bunny_assets_ok)
	var elevator_clearance_ok := true
	var elevator_art_rects: Array[Rect2] = [
		Rect2(1450.0, 700.0, 200.0, 230.0),
		Rect2(3122.0, 700.0, 200.0, 230.0),
	]
	for item_id: String in [
			"sleepy_bunny", "shell_bunny", "hop_bunny", "bunny_family"]:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {})
		var art_rect: Rect2 = record.get("art_rect", Rect2())
		for elevator_rect: Rect2 in elevator_art_rects:
			elevator_clearance_ok = elevator_clearance_ok \
				and not art_rect.intersects(elevator_rect)
	_ck("main_hall_interactions_clear_fixed_elevator", elevator_clearance_ok)
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

	print("CASTLE_ART|RESULT=", "FAIL" if checks_failed > 0 else "OK",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)

func _init() -> void:
	call_deferred("_run")
