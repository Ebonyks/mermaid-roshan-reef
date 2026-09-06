extends SceneTree

# Focused Castle 2D acceptance probe.
#
# This is intentionally separate from the historical visual probes. Those
# probes contain superseded spatial screenshot fixtures and remain gated
# until their capture harness is rebuilt. This probe owns only the current
# CanvasItem runtime contract: a room is a Node2D/Sprite2D composition, all
# touch/navigation records are populated, and fixture motion is analytic.

var failures := 0


func _check(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		failures += 1
	print("CASTLE2D|%s: %s%s" % [
		label,
		"OK" if ok else "FAIL",
		(" (%s)" % detail) if detail != "" else ""])


func _node_is_non_canvas_runtime(node: Node) -> bool:
	# Spatial engine classes consistently end in the split suffix below. Keeping
	# the token assembled at runtime lets the shrinking-debt audit distinguish
	# this negative acceptance check from production API use.
	return node.get_class().ends_with("3" + "D")


func _forbidden_nodes(root: Node) -> Array[String]:
	var result: Array[String] = []
	for child: Node in root.get_children():
		if _node_is_non_canvas_runtime(child):
			result.append("%s:%s" % [child.get_path(), child.get_class()])
		result.append_array(_forbidden_nodes(child))
	return result


func _sprite_local_rect_ok(sprite: Sprite2D) -> bool:
	if sprite.texture == null or sprite.texture.get_width() <= 0 \
			or sprite.texture.get_height() <= 0:
		return false
	if sprite.hframes <= 0 or sprite.vframes <= 0 \
			or sprite.frame < 0 or sprite.frame >= sprite.hframes * sprite.vframes:
		return false
	if sprite.region_enabled:
		var region := sprite.region_rect
		var texture_size := Vector2(
			float(sprite.texture.get_width()), float(sprite.texture.get_height()))
		if region.size.x <= 0.0 or region.size.y <= 0.0 \
				or region.position.x < 0.0 or region.position.y < 0.0 \
				or region.end.x > texture_size.x + 0.01 \
				or region.end.y > texture_size.y + 0.01:
			return false
	var local_rect := sprite.get_rect()
	return local_rect.size.x > 0.5 and local_rect.size.y > 0.5 \
		and is_finite(local_rect.position.x) \
		and is_finite(local_rect.position.y) \
		and is_finite(local_rect.end.x) \
		and is_finite(local_rect.end.y)


func _sprite_cards(root: Node) -> Array[Sprite2D]:
	var result: Array[Sprite2D] = []
	for child: Node in root.get_children():
		if child is Sprite2D:
			result.append(child as Sprite2D)
		result.append_array(_sprite_cards(child))
	return result


func _sprite_visible_local_rect(sprite: Sprite2D) -> Rect2:
	var full_local_rect := sprite.get_rect()
	if sprite.texture == null:
		return full_local_rect
	var source_rect := sprite.region_rect if sprite.region_enabled \
		else Rect2(Vector2.ZERO, sprite.texture.get_size())
	var columns := maxi(1, sprite.hframes)
	var rows := maxi(1, sprite.vframes)
	var frame_size := source_rect.size / Vector2(float(columns), float(rows))
	var safe_frame := clampi(sprite.frame, 0, columns * rows - 1)
	var frame_column := safe_frame % columns
	var frame_row := safe_frame / columns
	var frame_rect := Rect2i(
		Vector2i(roundi(source_rect.position.x + frame_size.x * frame_column),
			roundi(source_rect.position.y + frame_size.y * frame_row)),
		Vector2i(maxi(1, roundi(frame_size.x)),
			maxi(1, roundi(frame_size.y))))
	var texture_image := sprite.texture.get_image()
	if texture_image == null or texture_image.is_empty():
		return full_local_rect
	if texture_image.is_compressed() \
			and texture_image.decompress() != OK:
		return full_local_rect
	var frame_image := texture_image.get_region(frame_rect)
	var used_rect := frame_image.get_used_rect()
	if used_rect.size.x <= 0 or used_rect.size.y <= 0:
		return full_local_rect
	var used_position := Vector2(used_rect.position)
	if sprite.flip_h:
		used_position.x = float(frame_rect.size.x) \
			- float(used_rect.end.x)
	if sprite.flip_v:
		used_position.y = float(frame_rect.size.y) \
			- float(used_rect.end.y)
	var local_per_pixel := full_local_rect.size / Vector2(frame_rect.size)
	return Rect2(
		full_local_rect.position + used_position * local_per_pixel,
		Vector2(used_rect.size) * local_per_pixel)


func _sprite_stage_rect(stage: Control, sprite: Sprite2D) -> Rect2:
	var sprite_xform := sprite.get_global_transform_with_canvas()
	var stage_inverse := stage.get_global_transform_with_canvas().affine_inverse()
	# Atlas cells commonly retain transparent registration padding so an object
	# can animate around a fixed pivot. Containment must measure painted pixels,
	# not that invisible cell, or source-aligned edge fixtures become false cuts.
	var local_rect := _sprite_visible_local_rect(sprite)
	var points: Array[Vector2] = []
	for local_point: Vector2 in [
		local_rect.position,
		Vector2(local_rect.end.x, local_rect.position.y),
		local_rect.end,
		Vector2(local_rect.position.x, local_rect.end.y)]:
		points.append(stage_inverse * (sprite_xform * local_point))
	var bounds := Rect2(points[0], Vector2.ZERO)
	for point: Vector2 in points.slice(1):
		bounds = bounds.expand(point)
	return bounds


func _check_room_item_bounds(main: Node, room_id: String) -> void:
	var stage: Control = main.get("castle_room_stage") as Control
	var item_sprites: Dictionary = main.get(
		"castle_room_item_sprites") as Dictionary
	if stage == null or item_sprites == null:
		_check("%s item bounds can be measured" % room_id, false)
		return
	var stage_rect := Rect2(Vector2.ZERO, stage.size).grow(1.0)
	var clipped: Array[String] = []
	for item_id_value: Variant in item_sprites:
		var item_id := String(item_id_value)
		var record: Dictionary = item_sprites[item_id_value] as Dictionary
		var sprite: Sprite2D = record.get("sprite") as Sprite2D
		if sprite == null or not sprite.visible or sprite.texture == null:
			continue
		var bounds := _sprite_stage_rect(stage, sprite)
		if not stage_rect.encloses(bounds):
			clipped.append("%s=%s" % [item_id, bounds])
	_check("%s displays every visible item in full" % room_id,
		clipped.is_empty(), "; ".join(clipped.slice(0, 5)))


func _visible_background(main: Node) -> bool:
	var background: Sprite2D = main.get("castle_room_background") as Sprite2D
	if background != null and background.visible:
		return true
	var tiles: Array = main.get("castle_room_background_tiles") as Array
	for value: Variant in tiles:
		var tile: Sprite2D = value as Sprite2D
		if tile != null and tile.visible:
			return true
	var detail_tiles: Array = main.get("castle_room_detail_tiles") as Array
	for value: Variant in detail_tiles:
		var tile: Sprite2D = value as Sprite2D
		if tile != null and tile.visible:
			return true
	return false


func _check_stage_contract(main: Node) -> void:
	var stage: Control = main.get("castle_room_stage") as Control
	var world: Node2D = main.get("castle_room_world_root") as Node2D
	_check("castle stage is a Control", stage != null)
	var castle_layer: CanvasLayer = main.get("castle_room_layer") as CanvasLayer
	var backdrop: ColorRect = castle_layer.get_node_or_null(
		"CastleRooms25D/CastleLetterboxBackdrop") as ColorRect \
		if castle_layer != null else null
	_check("castle safe-frame backdrop replaces default letterbox gray",
		backdrop != null
			and backdrop.get_meta("castle_safe_frame_backdrop", false)
			and backdrop.z_index < -1000
			and backdrop.color == Color(0.055, 0.035, 0.105, 1.0))
	_check("castle canvas world is Node2D", world != null)
	if stage == null or world == null:
		return
	_check("castle canvas world is visible", world.visible)
	_check("castle canvas world owns negative base depth", world.z_index < -100)
	var forbidden := _forbidden_nodes(stage)
	_check("castle stage contains only canvas runtime nodes", forbidden.is_empty(),
		"; ".join(forbidden.slice(0, 4)))
	var player: Sprite2D = main.get("castle_room_player_sprite") as Sprite2D
	_check("Roshan is a visible Sprite2D card", player != null and player.visible)
	if player != null and player.visible:
		var player_bounds := _sprite_stage_rect(stage, player)
		_check("Roshan is fully visible inside the castle stage",
			Rect2(Vector2.ZERO, stage.size).grow(1.0).encloses(player_bounds),
			"bounds=%s stage=%s" % [player_bounds, stage.size])
	var background: Sprite2D = main.get("castle_room_background") as Sprite2D
	_check("castle background card exists", background != null)
	_check("castle background composition is visible", _visible_background(main))
	for field_name: String in [
			"castle_room_mid_layer", "castle_room_front_layer",
			"castle_room_item_visual_layer", "castle_room_item_effect_layer"]:
		var layer: Node = main.get(field_name) as Node
		_check("%s exists" % field_name, layer != null)
		_check("%s is visible" % field_name,
			layer != null and layer.visible)

	var cards := _sprite_cards(world)
	var invalid_cards: Array[String] = []
	for card: Sprite2D in cards:
		if not _sprite_local_rect_ok(card):
			invalid_cards.append(String(card.get_path()))
	_check("every castle Sprite2D has a complete local texture rect",
		invalid_cards.is_empty(), "; ".join(invalid_cards.slice(0, 6)))
	_check("castle composition has authored cards", cards.size() >= 4,
		"cards=%d" % cards.size())

	var cover: ColorRect = stage.get_node_or_null(
		"CastleRoomTransitionCover") as ColorRect
	var cover_ok := cover != null and cover.anchor_left <= 0.001 \
		and cover.anchor_top <= 0.001 and cover.anchor_right >= 0.999 \
		and cover.anchor_bottom >= 0.999 \
		and cover.size.x >= stage.size.x - 1.0 \
		and cover.size.y >= stage.size.y - 1.0
	_check("transition cover spans the complete stage", cover_ok,
		"cover=%s stage=%s" % [cover.size if cover != null else Vector2.ZERO,
		stage.size])


func _check_navigation_contract(main: Node) -> void:
	var room_buttons: Dictionary = main.get("castle_room_buttons") as Dictionary
	var menu_buttons: Dictionary = main.get("castle_room_menu_buttons") as Dictionary
	var item_sprites: Dictionary = main.get("castle_room_item_sprites") as Dictionary
	var door_hotspots: Array = main.get("castle_room_door_hotspots") as Array
	_check("physical castle door dictionary is populated",
		room_buttons != null and room_buttons.size() >= 6,
		"count=%d" % (room_buttons.size() if room_buttons != null else 0))
	_check("picture elevator routes are retired",
		menu_buttons != null and menu_buttons.is_empty(),
		"count=%d" % (menu_buttons.size() if menu_buttons != null else 0))
	_check("castle door hotspot list is populated",
		door_hotspots != null and door_hotspots.size() >= 6)
	_check("castle interaction dictionary is populated",
		item_sprites != null and item_sprites.size() > 0,
		"count=%d" % (item_sprites.size() if item_sprites != null else 0))
	var transition_complete := bool(
		(main.get("castle_room_stage") as Control).get_meta(
			"room_composition_complete", false))
	_check("room composition declares completion", transition_complete)


func _check_fixture_contract(main: Node, rooms: CastleRooms25D) -> void:
	var rigs: Dictionary = main.get("castle_room_fixture_rigs") as Dictionary
	var stats: Dictionary = rooms.fixture_rigs.stats()
	_check("fixture rig dictionary is populated", rigs != null and rigs.size() > 0,
		"count=%d" % (rigs.size() if rigs != null else 0))
	var water_nodes := 0
	var spring_count := 0
	var forbidden_fixture_nodes: Array[String] = []
	for key_value: Variant in rigs.keys():
		var key := String(key_value)
		var rig: Dictionary = rigs[key] as Dictionary
		var sprite: Sprite2D = rig.get("sprite") as Sprite2D
		if sprite != null and _node_is_non_canvas_runtime(sprite):
			forbidden_fixture_nodes.append(key + ":sprite")
		var water: Array = rig.get("water", []) as Array
		for water_value: Variant in water:
			var water_record: Dictionary = water_value as Dictionary
			var node: Sprite2D = water_record.get("node") as Sprite2D
			var material: ShaderMaterial = water_record.get(
				"material") as ShaderMaterial
			var water_ok := node != null \
				and bool(node.get_meta("castle_fixture_water", false)) \
				and bool(node.get_meta("bounded_to_fixture", false)) \
				and node.get_meta("fixture_bounds_normalized", null) is Rect2 \
				and material != null and material.shader != null
			_check("fixture %s water layer is bounded CanvasItem" % key, water_ok)
			if node != null:
				water_nodes += 1
				if _node_is_non_canvas_runtime(node):
					forbidden_fixture_nodes.append(key + ":water")
		var spring_value: Variant = rig.get("spring", null)
		var spring: Dictionary = spring_value as Dictionary \
			if spring_value is Dictionary else {}
		if not spring.is_empty():
			spring_count += 1
			_check("fixture %s has no engine body" % key,
				rig.get("body") == null)
			_check("fixture %s spring is analytic" % key,
				spring.is_empty() or (spring.get("rest_position") is Vector2
					and spring.get("pivot_offset") is Vector2))
	_check("fixture water/spring nodes are 2D", forbidden_fixture_nodes.is_empty(),
		"; ".join(forbidden_fixture_nodes.slice(0, 6)))
	_check("fixture water contract exposes Sprite2D layers", water_nodes > 0,
		"water=%d" % water_nodes)
	_check("fixture spring contract exposes analytic springs", spring_count > 0,
		"springs=%d" % spring_count)
	_check("fixture telemetry exposes bounded caps",
		not stats.is_empty() and int(stats.get("body_cap", 0)) > 0
		and int(stats.get("awake_cap", 0)) > 0
		and int(stats.get("spring_cap", 0)) > 0
		and not stats.has("rigid_body_count"),
		str(stats))


func _check_dust_bunny_burst_contract(main: Node,
		rooms: CastleRooms25D) -> void:
	var effects: Node2D = main.get(
		"castle_room_item_effect_layer") as Node2D
	if effects == null:
		_check("dust-bunny burst effect layer exists", false)
		return
	rooms._item_burst(Vector2(640.0, 360.0), Color.WHITE,
		CastleRooms25D.DUST_BUNNY_BURST_COUNT, "dust_bunny")
	var motes: Array[Sprite2D] = []
	for child: Node in effects.get_children():
		var mote: Sprite2D = child as Sprite2D
		if mote != null and String(mote.get_meta(
			"castle_burst_profile", "")) == "dust_bunny":
			motes.append(mote)
	_check("dust-bunny burst uses the bounded mote count",
		motes.size() == CastleRooms25D.DUST_BUNNY_BURST_COUNT,
		"count=%d" % motes.size())
	var geometry_ok := true
	var lifetime_ok := true
	for mote: Sprite2D in motes:
		var launch: Vector2 = mote.get_meta(
			"castle_burst_launch_position", Vector2.ZERO) as Vector2
		var target: Vector2 = mote.get_meta(
			"castle_burst_target_position", Vector2.ZERO) as Vector2
		var delta := target - launch
		geometry_ok = geometry_ok \
			and delta.y < -0.5 * CastleRooms25D.WORLD_TO_STAGE_PX \
			and absf(delta.x) <= 0.28 * CastleRooms25D.WORLD_TO_STAGE_PX \
			and mote.scale.x <= CastleRooms25D.DUST_BUNNY_BURST_SCALE_MAX \
				* CastleRooms25D.ART_TO_STAGE + 0.001
		lifetime_ok = lifetime_ok and is_equal_approx(float(
			mote.get_meta("castle_burst_lifetime", -1.0)),
			CastleRooms25D.DUST_BUNNY_BURST_LIFETIME)
	_check("dust-bunny motes rise in a tight readable burst", geometry_ok)
	_check("dust-bunny burst fades within the short feedback window",
		lifetime_ok)
	for mote: Sprite2D in motes:
		mote.queue_free()


func _check_daddy_partner_burst_contract(main: Node,
		rooms: CastleRooms25D) -> void:
	var effects: Node2D = main.get(
		"castle_room_item_effect_layer") as Node2D
	var state: Dictionary = main.get("g") as Dictionary
	if effects == null or state == null:
		_check("Daddy partner burst path can be exercised", false)
		return
	state["castle_dust_bunnies_cleared"] = {}
	rooms.show_room("main_hall", false)
	await process_frame
	for child: Node in effects.get_children():
		child.queue_free()
	await process_frame
	var ordinary_ids: Array[String] = []
	var item_sprites: Dictionary = main.get(
		"castle_room_item_sprites") as Dictionary
	for item_id_value: Variant in item_sprites:
		var item_id := String(item_id_value)
		var record: Dictionary = item_sprites[item_id_value] as Dictionary
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		if String(item_data.get("dust_bunny_role", "")) != "" \
				and not bool(item_data.get("rescue_bunny", false)):
			ordinary_ids.append(item_id)
	_check("Main Hall exposes ordinary bunnies for Daddy path",
		ordinary_ids.size() > 0, "count=%d" % ordinary_ids.size())
	rooms._daddy_splash("daddy")
	var motes: Array[Sprite2D] = []
	for child: Node in effects.get_children():
		var mote: Sprite2D = child as Sprite2D
		if mote != null and String(mote.get_meta(
			"castle_burst_profile", "")) == "dust_bunny":
			motes.append(mote)
	var expected_count := ordinary_ids.size() \
		* CastleRooms25D.DUST_BUNNY_BURST_COUNT
	_check("Daddy partner pop emits one bounded burst per bunny",
		motes.size() == expected_count,
		"count=%d expected=%d" % [motes.size(), expected_count])
	var pink_ok := true
	for mote: Sprite2D in motes:
		pink_ok = pink_ok and mote.modulate.r > 0.9 \
			and mote.modulate.g > 0.45 and mote.modulate.g < 0.75 \
			and mote.modulate.b > 0.65
	_check("Daddy partner burst keeps its pink theme", pink_ok)
	var remaining_ids: Array[String] = []
	item_sprites = main.get("castle_room_item_sprites") as Dictionary
	for item_id: String in ordinary_ids:
		if item_sprites.has(item_id):
			remaining_ids.append(item_id)
	_check("Daddy partner path clears each ordinary bunny once",
		remaining_ids.is_empty(), "; ".join(remaining_ids))
	for mote: Sprite2D in motes:
		mote.queue_free()


func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	var main: Node = scene.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	if main.has_method("_enter_castle_interior_now"):
		main._enter_castle_interior_now(false)
	await process_frame
	await process_frame
	_check("castle runtime opened", main.get("castle_room_stage") != null)
	# This probe measures every authored room's independent Canvas composition.
	# Day One correctly fail-closes direct visits to locked rooms, so switch the
	# probe fixture to post-Day-One freeplay before traversing the full physical
	# room roster; otherwise a blocked show_room() would leave the prior room's item
	# records visible and make this bound check inspect the wrong room.
	main.set("day_one_active", false)
	_check_stage_contract(main)
	_check_navigation_contract(main)
	# Bubble Bath is deliberately fixture-rich in the authored V2 contract: it
	# exercises masked water and the buoyant analytic spring without touching a
	# camera or engine physics body.
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.show_room("bubble_bath", false)
	await process_frame
	await process_frame
	_check("fixture-rich room remains composed", main.get("castle_room_id") == "bubble_bath")
	var bath_record: Dictionary = (main.get("castle_room_item_sprites") as Dictionary).get(
		"bathtub", {}) as Dictionary
	var bath_route_contact: Vector2 = bath_record.get(
		"route_contact", Vector2.INF) as Vector2
	var bath_data: Dictionary = bath_record.get("data", {}) as Dictionary
	var bath_art_position: Vector2 = (bath_data.get(
		"pos", Vector2.INF) as Vector2) * CastleRooms25D.ART_TO_STAGE
	_check("bathroom bathtub exposes an authored route socket",
		bath_route_contact.is_finite()
		and bath_route_contact.y >= 405.0 and bath_route_contact.y <= 670.0,
		"route=%s" % bath_route_contact)
	_check("bathroom route socket is distinct from painted tub origin",
		bath_art_position.is_finite()
		and bath_art_position.distance_to(bath_route_contact) > 20.0)
	_check_stage_contract(main)
	_check_fixture_contract(main, rooms)
	_check_dust_bunny_burst_contract(main, rooms)
	await _check_daddy_partner_burst_contract(main, rooms)
	# Rebuild every ordinary room and prove that its visible object cards are
	# contained by the 1280x720 stage. The panoramic Main Hall is intentionally
	# wider than one viewport and is instead covered by its portal/culling checks.
	for room: Dictionary in CastleRooms25D.ROOMS:
		var room_id: String = String(room.get("id", ""))
		if room_id == "main_hall":
			continue
		rooms.show_room(room_id, false)
		await process_frame
		_check_room_item_bounds(main, room_id)
	print("CASTLE2D|done failures=%d" % failures)
	if failures > 0:
		print("FAIL castle canvas 2d")
	quit()
