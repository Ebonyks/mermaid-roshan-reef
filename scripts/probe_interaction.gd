extends SceneTree
# Interaction-language integration: proximity advertises, first tap selects,
# assisted movement approaches, and only a second explicit verb activates.

const Affordance := preload("res://scripts/interaction_affordance.gd")
const NATIVE_FALLBACK_ITEMS := {
	"opera_hall": ["pearl_sconce_left", "pearl_sconce_right"],
	"kitchen": ["fridge"],
	"library": ["pearl_lamp_right", "ceiling_chandelier"],
	"playroom": ["tent_flaps_right", "shelf_sailboat"],
	"craft_room": ["supply_cupboard_left"],
	"mermaid_pool": [
		"waterfall", "flower_float", "seahorse_fountain", "star_float"],
	"bubble_bath": ["vanity_mirror"],
}
const NATIVE_FALLBACK_TILE_COUNTS := {
	"opera_hall": 8,
	"kitchen": 12,
	"library": 8,
	"playroom": 8,
	"craft_room": 8,
	"mermaid_pool": 8,
	"bubble_bath": 8,
}

var main: Node3D
var failures := 0

func _init() -> void:
	Engine.time_scale = 4.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(8)
	main._set_touch_mode("hybrid", false)
	main._populate_touch_interactables()
	if main.touch_interactables.size() < main.friends.size():
		_bad("reef registry omitted core friends")
	for touch_target_value: Variant in main.touch_interactables:
		var touch_target: Dictionary = touch_target_value as Dictionary
		var target_id: String = String(touch_target.get("id", ""))
		var expected_affordance: String = Affordance.INTERACTION
		if target_id.begins_with("friend:"):
			var friend_index: int = int(touch_target.get("payload", -1))
			if friend_index >= 0 and friend_index < main.friends.size():
				var target_friend: Dictionary = main.friends[friend_index] as Dictionary
				if not bool(target_friend.get("won", false)):
					expected_affordance = Affordance.PLOT
		elif target_id == "reef:lagoon" and not main.level2_done_once:
			expected_affordance = Affordance.PLOT
		elif target_id == "reef:return" and main._all_friends_won():
			expected_affordance = Affordance.PLOT
		var actual_affordance: String = String(touch_target.get(
			"affordance_kind", ""))
		if actual_affordance != expected_affordance:
			_bad("world affordance category wrong for %s" % target_id)
			break
	if Affordance.RED_IDLE.a <= Affordance.BLUE_IDLE.a \
			or Affordance.emission_energy(Affordance.PLOT, false) \
				<= Affordance.emission_energy(Affordance.INTERACTION, false) \
			or Affordance.pulse_amount(Affordance.PLOT, false) \
				<= Affordance.pulse_amount(Affordance.INTERACTION, false):
		_bad("red plot beacon is not the most obvious affordance")

	var friend: Dictionary = main.friends[0]
	var friend_node: Node3D = friend["node"]
	main.player.position = friend_node.position + Vector3(3.0, 0.0, 0.0)
	main.player.vel = Vector3.ZERO
	await _frames(20)
	if main.game != "":
		_bad("proximity launched a friend activity")

	var camera: Camera3D = main.get_viewport().get_camera_3d()
	if camera == null:
		_bad("camera unavailable for screen-space selection")
	else:
		var tap: Vector2 = camera.unproject_position(friend_node.global_position)
		# An action press made before anything is selected must expire. It may
		# not be remembered and applied to the next focus, even in the same
		# rendered frame.
		main.touch_ui._on_action_button_down()
		main.touch_ui._on_action_button_up()
		main._interaction_ref().on_world_touch(tap)
		await process_frame
		if main.touch_focus_id != "friend:0" or not main.touch_focus_ready:
			_bad("first friend tap did not focus/ready")
		if main.game != "":
			_bad("first friend tap launched instead of acknowledging")
		main._interaction_ref().on_world_touch(tap)
		await _frames(12)
		if main.game == "":
			_bad("second friend tap did not activate")
	if main.game != "":
		main._clear_game()
		await _frames(6)

	# Open-space assisted movement feeds steering and yields to manual input.
	var travel_target: Vector3 = main.player.position + Vector3(25.0, 0.0, 18.0)
	main._tap_move_ref().start(travel_target)
	var direction: Vector3 = main.touch_auto_direction()
	if not bool(main.touch_auto_active) or direction.length() < 0.9:
		_bad("assisted movement produced no steering intent")
	main._on_touch_manual_move()
	if bool(main.touch_auto_active):
		_bad("manual override failed")

	# Fix regression: an ELEVATED target (the penguin floe rides just under the
	# surface) must become ready through assisted travel. Horizontal-only
	# steering once stopped short of the vertically-weighted readiness check
	# and looped "Tap again!" forever.
	if main.slide_portal_pos == Vector3.ZERO:
		_bad("penguin floe position unavailable for the elevated approach")
	else:
		var floe: Vector3 = main.slide_portal_pos
		main.player.position = Vector3(floe.x + 9.0, floe.y - 26.0, floe.z)
		main.player.vel = Vector3.ZERO
		main._populate_touch_interactables()
		main.touch_focus_id = "reef:slide"
		main.touch_focus_ready = false
		main._tap_move_ref().start(floe, "reef:slide", 14.0)
		var previous_scale: float = Engine.time_scale
		Engine.time_scale = 1.0
		var climb_start_y: float = main.player.position.y
		var deadline: int = Time.get_ticks_msec() + 12000
		while Time.get_ticks_msec() < deadline and not main.touch_focus_ready:
			await process_frame
		Engine.time_scale = previous_scale
		if not main.touch_focus_ready:
			_bad("elevated floe never became ready (vertical approach wedge)")
		if main.player.position.y - climb_start_y < 4.0:
			_bad("assisted travel did not climb toward the elevated floe")
		main._tap_move_ref().cancel("probe")
		main._interaction_ref().clear_focus()

	# Build the two navigation-heavy zones and assert that each important verb
	# has a touch target. This catches hidden-floor regressions without relying
	# on a camera-perfect scripted swim.
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(24)
	var promenade_targets: Array = main.g.get("lagoon_promenade_targets", [])
	var promenade_ids: Dictionary = {}
	for target_value in promenade_targets:
		var promenade_target: Dictionary = target_value as Dictionary
		var promenade_id: String = String(promenade_target.get("id", ""))
		promenade_ids[promenade_id] = true
		var expected_affordance: String = Affordance.PLOT \
			if promenade_id == "castle_gate" else Affordance.ANIMATION
		var highlight: Sprite3D = promenade_target.get("highlight") as Sprite3D
		if String(promenade_target.get(
				"affordance_kind", "")) != expected_affordance:
			_bad("promenade affordance category wrong for %s" % promenade_id)
		elif highlight == null or not highlight.visible:
			_bad("promenade idle affordance hidden for %s" % promenade_id)
	for expected: String in ["slide", "swing", "seesaw", "castle_gate"]:
		if not promenade_ids.has(expected):
			_bad("promenade interaction missing %s" % expected)
	for removed_frame: String in ["runway_frame", "playground_frame", "castle_frame"]:
		if promenade_ids.has(removed_frame):
			_bad("removed lawn picture still interactive: %s" % removed_frame)
	if promenade_targets.size() < 4 or promenade_targets.size() > 5:
		_bad("promenade roster must be four permanent toys/landmarks plus optional Day One plane")

	# Exercise the first-visit Crown Star target, not the already-won keepsake.
	# The castle is one picture-first Sprite3D stage, not a second free-roaming
	# 3D world. Room props use UI hit targets projected over their world cards;
	# the retired hall registry must therefore remain empty.
	main.level2_done_once = false
	# This probe audits the Crown route only. Companion re-offer behavior has
	# dedicated close/reopen and save-safe coverage in probe_throne.
	main.companion_id = "eagle"
	main._enter_castle_interior_now(false)
	await _frames(24)
	main._populate_touch_interactables()
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	if not rooms.is_open():
		_bad("castle Sprite3D room stage did not open")
	if rooms.has_method("_roleplay_prop_bounce"):
		_bad("castle role-play still exposes the rejected generic prop bounce")
	var rejected_native_tiles: Array[Texture2D] = \
		rooms.fixture_rigs.room_background_tile_textures(
			"kitchen", 4, 3, Vector2i(1024, 767))
	if not rejected_native_tiles.is_empty() \
			or not rooms.fixture_rigs.room_native_items("kitchen").is_empty():
		_bad("native castle route activated with wrong decoded tile dimensions")
	var complete_native_tiles: Array[Texture2D] = \
		rooms.fixture_rigs.room_background_tile_textures(
			"kitchen", 4, 3, Vector2i(1024, 768))
	if complete_native_tiles.size() != 12 \
			or rooms.fixture_rigs.room_native_items("kitchen").is_empty():
		_bad("complete decoded native castle route did not activate atomically")
	complete_native_tiles.clear()
	if not _ids().is_empty():
		_bad("retired 3D hall touch targets were populated")
	for retired_key: String in [
		"hall_exit", "bed_pos", "stand_chest", "toilet", "dungeon_gate",
		"craft_easel", "wardrobe", "song_star", "secret_door", "hall_touch",
		"bells", "opera_gate"]:
		if main.g.has(retired_key):
			_bad("retired 3D hall state rebuilt %s" % retired_key)
	for room_id: String in [
		"family_gallery", "opera_hall", "kitchen", "library", "playroom",
		"craft_room", "mermaid_pool", "bubble_bath"]:
		if not main.castle_room_buttons.has(room_id):
			_bad("castle physical doorway missing %s" % room_id)
	if main.castle_room_world_root == null \
			or main.castle_room_camera == null \
			or main.castle_room_camera.projection != Camera3D.PROJECTION_PERSPECTIVE:
		_bad("castle did not build its perspective Sprite3D stage")
	if main.touch_ui.world_controls_enabled or main.player.visible:
		_bad("free-roaming 3D controls remained active inside castle stage")
	if main.touch_discovery_ring == null or main.touch_focus_ring == null:
		_bad("shared glow/focus visuals were not built")
	var elevator_button: Button = main.castle_room_stage.get_node_or_null(
		"ElevatorButton") as Button
	if elevator_button == null or main.castle_room_back_button == null \
			or main.castle_room_menu_panel == null \
			or main.castle_room_menu_buttons.size() != 12 \
			or main.castle_room_menu_buttons.has("family_gallery"):
		_bad("storybook elevator or contextual Back was missing")
	elif elevator_button.size.x < StorybookUI.MIN_TOUCH.x \
			or elevator_button.size.y < StorybookUI.MIN_TOUCH.y:
		_bad("storybook elevator touch target is too small")
	else:
		elevator_button.pressed.emit()
		if not main.castle_room_menu_open \
				or not main.castle_room_menu_panel.visible:
			_bad("storybook elevator did not expand")
		rooms._set_elevator_menu_open(false, false)
	for dream_room_id: String in [
		"family_gallery", "dining_room", "royal_bedroom",
		"sleepover_bedroom", "movie_lounge"]:
		if rooms._room(dream_room_id).is_empty():
			_bad("dream-house room missing %s" % dream_room_id)
	if main.castle_room_link_layer == null:
		_bad("dream-house room-link layer was not built")
	elif main.castle_room_link_layer.get_child_count() != 0:
		_bad("floating dream-house route buttons remained")
	await _audit_native_route_fallback(rooms)

	rooms.show_room("family_gallery", false)
	await _frames(2)
	if main.castle_room_detail_tiles.size() != 4 \
			or main.castle_room_action_button.visible:
		_bad("Dream House Wing did not build as a native physical gallery")
	var castle_affordance: Sprite3D = main.g.get(
		"castle_room_affordance") as Sprite3D
	if castle_affordance == null:
		_bad("castle shared affordance card missing")
	var dream_routes: Array[Dictionary] = [
		{"item": "gallery_dining_door", "child": "dining_room"},
		{"item": "gallery_royal_bedroom_door", "child": "royal_bedroom"},
		{"item": "gallery_sleepover_door", "child": "sleepover_bedroom"},
		{"item": "gallery_movie_door", "child": "movie_lounge"},
	]
	for route: Dictionary in dream_routes:
		var item_id: String = String(route["item"])
		var child_id: String = String(route["child"])
		var route_record: Dictionary = main.castle_room_item_sprites.get(
			item_id, {}) as Dictionary
		var door_sprite: Sprite3D = route_record.get("sprite") as Sprite3D
		var door_hotspot: Button = route_record.get("hotspot") as Button
		if door_sprite == null \
				or String(route_record.get(
					"affordance_kind", "")) != Affordance.INTERACTION \
				or String(door_sprite.get_meta(
					"room_destination", "")) != child_id \
				or not bool(door_sprite.get_meta(
					"castle_physical_door", false)) \
				or door_hotspot == null \
				or String(door_hotspot.get_meta(
					"room_destination", "")) != child_id \
				or not bool(door_hotspot.get_meta("physical_door", false)):
			_bad("physical dream-house doorway missing %s -> %s" % [
				item_id, child_id])
			continue
		door_hotspot.pressed.emit()
		var entered_room: bool = await _wait_for_castle_room(child_id)
		if not entered_room:
			_bad("dream-house doorway did not enter %s" % child_id)
			rooms.show_room("family_gallery", false)
			await _frames(2)
			continue
		main.castle_room_back_button.pressed.emit()
		await _frames(2)
		if main.castle_room_id != "family_gallery":
			_bad("dream-house Back did not return %s to gallery" % child_id)

	main.castle_room_back_button.pressed.emit()
	await _frames(2)
	if main.castle_room_id != "main_hall":
		_bad("Dream House Wing Back did not return to Main Hall")

	# The four newest rooms retain their physical gallery doors, but the
	# omnipresent picture elevator also reaches each in one direct choice.
	for direct_room_id: String in [
		"dining_room", "royal_bedroom", "sleepover_bedroom", "movie_lounge"]:
		elevator_button = main.castle_room_stage.get_node_or_null(
			"ElevatorButton") as Button
		var direct_button: Button = main.castle_room_menu_buttons.get(
			direct_room_id) as Button
		if elevator_button == null or direct_button == null:
			_bad("direct elevator route missing %s" % direct_room_id)
			continue
		elevator_button.pressed.emit()
		if not main.castle_room_menu_open:
			_bad("elevator would not open from %s" % main.castle_room_id)
			continue
		direct_button.pressed.emit()
		if not await _wait_for_castle_room(direct_room_id):
			_bad("elevator did not directly enter %s" % direct_room_id)
	var main_hall_button: Button = main.castle_room_menu_buttons.get(
		"main_hall") as Button
	if main_hall_button != null:
		elevator_button.pressed.emit()
		main_hall_button.pressed.emit()
		await _wait_for_castle_room("main_hall")

	# The paint table, not the room-wide make-a-friend action, owns the new
	# castle-logo game. A confirmed choice saves and returns as board art.
	rooms.show_room("craft_room", false)
	await _frames(2)
	var logo_table_record: Dictionary = main.castle_room_item_sprites.get(
		"paint_table", {}) as Dictionary
	var logo_table_sprite: Sprite3D = logo_table_record.get(
		"sprite") as Sprite3D
	if logo_table_sprite == null or String(logo_table_sprite.get_meta(
			"launch_activity", "")) != "castle_logo":
		_bad("craft-room paint table is not the castle-logo station")
	rooms.activate_current_room()
	var logo_deadline: int = Time.get_ticks_msec() + 2500
	while main.castle_logo_layer == null \
			and Time.get_ticks_msec() < logo_deadline:
		await process_frame
	if main.castle_logo_layer == null:
		_bad("Craft Room action did not open its paint-table castle-logo game")
	elif main.craft_layer != null:
		_bad("Craft Room action opened the generic Creature Craft Studio")
	else:
		var dog_button := main.castle_logo_layer.find_child(
			"CastleLogoSymbol_dog", true, false) as Button
		var purple_button := main.castle_logo_layer.find_child(
			"CastleLogoColor_purple", true, false) as Button
		var finish_button := main.castle_logo_layer.find_child(
			"CastleLogoFinishButton", true, false) as Button
		if dog_button == null or purple_button == null or finish_button == null:
			_bad("castle-logo game is missing puppy, purple, or finish choices")
			main._close_castle_logo()
		else:
			dog_button.pressed.emit()
			purple_button.pressed.emit()
			await process_frame
			var live_preview: Control = main.castle_logo_preview
			if live_preview == null \
					or String(live_preview.get_meta("symbol_id", "")) != "dog" \
					or String(live_preview.get_meta("color_id", "")) != "purple":
				_bad("castle-logo preview did not follow the picture choices")
			finish_button.pressed.emit()
			await process_frame
			main._castle_logo_ref().close(true)
			await process_frame
			if main.castle_logo_layer != null \
					or main.castle_logo_color != "purple" \
					or main.castle_logo_symbol != "dog":
				_bad("confirmed castle logo did not close and keep its choice")
			elif String(main.save_data.get(
					"castle_logo_symbol", "")) != "dog":
				_bad("confirmed castle logo was not saved")
			else:
				var craft_display: Control = main.castle_logo_room_display
				var craft_banners: Array[Node] = craft_display.find_children(
					"CastleLogoBanner_*", "Control", true, false) \
					if craft_display != null else []
				var board_badge: Control = craft_display.find_child(
					"CastleLogoCraftBoardBadge", true, false) as Control \
					if craft_display != null else null
				if craft_display == null or craft_banners.size() != 2 \
						or board_badge == null \
						or String(craft_display.get_meta(
							"replaces_design", "")) != "purple_shell_banner":
					_bad("custom logo did not replace both Craft Room shell banners")

	rooms.show_room("playroom", false)
	await _frames(2)
	var playroom_display: Control = main.castle_logo_room_display
	var playroom_banners: Array[Node] = playroom_display.find_children(
		"CastleLogoBanner_*", "Control", true, false) \
		if playroom_display != null else []
	if playroom_display == null or playroom_banners.size() != 2 \
			or String(playroom_display.get_meta(
				"castle_room_id", "")) != "playroom":
		_bad("custom logo did not replace both Stuffie Playroom shell banners")
	else:
		for banner: Node in playroom_banners:
			if String(banner.get_meta("symbol_id", "")) != "dog" \
					or String(banner.get_meta("color_id", "")) != "purple" \
					or String(banner.get_meta(
						"replaces_design", "")) != "purple_shell_banner":
				_bad("Stuffie Playroom banner did not use the saved custom logo")
				break

	rooms.show_room("dining_room", false)
	await _frames(2)
	if main.castle_logo_room_display != null:
		_bad("custom banners appeared in a room with no purple shell banners")
	if main.castle_room_detail_tiles.size() != 4 \
			or not main.castle_room_item_sprites.has("dining_table") \
			or not main.castle_room_item_sprites.has("provisions_hutch"):
		_bad("family dining room did not build native tiles and meal furniture")
	var hutch_record: Dictionary = main.castle_room_item_sprites.get(
		"provisions_hutch", {}) as Dictionary
	var hutch_sprite: Sprite3D = hutch_record.get("sprite") as Sprite3D
	var hutch_transform: Transform3D = hutch_sprite.transform \
		if hutch_sprite != null else Transform3D.IDENTITY
	if String(hutch_record.get("affordance_kind", "")) != Affordance.ANIMATION \
			or castle_affordance == null \
			or String(castle_affordance.get_meta(
				"affordance_kind", "")) != Affordance.ANIMATION:
		_bad("local castle prop missing gold animation affordance")
	rooms._activate_room_item("provisions_hutch")
	await _frames(40)
	var all_six_plates_visible := int(
		main.g.get("castle_dining_plates", 0)) == 6
	for plate_index in range(6):
		var plate_record: Dictionary = main.castle_room_item_sprites.get(
			"meal_plate_%d" % plate_index, {}) as Dictionary
		var plate_sprite: Sprite3D = plate_record.get("sprite") as Sprite3D
		all_six_plates_visible = all_six_plates_visible \
			and plate_sprite != null and plate_sprite.visible \
			and bool(plate_sprite.get_meta("castle_soft_alpha", false)) \
			and plate_sprite.alpha_cut == SpriteBase3D.ALPHA_CUT_DISABLED \
			and int(plate_sprite.get_meta(
				"meal_plate_reveal_step", -1)) == plate_index
	if not all_six_plates_visible:
		_bad("serving dinner did not stagger six real visible plates")
	if hutch_sprite == null \
			or not hutch_sprite.transform.is_equal_approx(hutch_transform) \
			or int(hutch_sprite.get_meta(
				"roleplay_state_count", 0)) != 6 \
			or String(hutch_sprite.get_meta(
				"normalized_use_animation", "")) \
				!= "stagger_real_meal_plates":
		_bad("serving dinner deformed the buffet instead of sequencing plates")
	var table_record: Dictionary = main.castle_room_item_sprites.get(
		"dining_table", {}) as Dictionary
	var table_sprite: Sprite3D = table_record.get("sprite") as Sprite3D
	var table_transform: Transform3D = table_sprite.transform \
		if table_sprite != null else Transform3D.IDENTITY
	rooms._activate_room_item("dining_table")
	await _frames(24)
	var eaten_record: Dictionary = main.castle_room_item_sprites.get(
		"meal_plate_5", {}) as Dictionary
	var eaten_plate: Sprite3D = eaten_record.get("sprite") as Sprite3D
	if int(main.g.get("castle_dining_plates", 0)) != 5 \
			or eaten_plate == null or eaten_plate.visible \
			or String(eaten_plate.get_meta("meal_plate_state", "")) != "eaten":
		_bad("eating at the family table did not consume the real plate")
	if table_sprite == null \
			or not table_sprite.transform.is_equal_approx(table_transform) \
			or int(table_sprite.get_meta(
				"roleplay_state_count", 0)) != 4 \
			or String(table_sprite.get_meta(
				"normalized_use_animation", "")) \
				!= "consume_real_meal_plate":
		_bad("eating deformed the table instead of consuming its plate")
	# An empty table delegates to the provisions hutch; it must not pretend the
	# table itself can manufacture dinner.
	main.g["castle_dining_plates"] = 0
	rooms._sync_dining_plates()
	rooms._activate_room_item("dining_table")
	await _frames(40)
	if int(main.g.get("castle_dining_plates", 0)) != 6 \
			or not table_sprite.transform.is_equal_approx(table_transform) \
			or not hutch_sprite.transform.is_equal_approx(hutch_transform) \
			or String(hutch_sprite.get_meta(
				"normalized_use_animation", "")) \
				!= "stagger_real_meal_plates":
		_bad("empty dining table did not delegate serving to the real hutch")
	# A delayed serve sequence must belong to the exact room build that started
	# it. Leaving and re-entering dining must not let old callbacks reveal the
	# newly built plate sprites.
	main.g["castle_dining_plates"] = 0
	rooms._sync_dining_plates()
	rooms._activate_room_item("provisions_hutch")
	var serving_generation := rooms._room_build_generation
	rooms.show_room("royal_bedroom", false)
	rooms.show_room("dining_room", false)
	main.g["castle_dining_plates"] = 0
	rooms._sync_dining_plates()
	await _frames(12)
	var stale_plate_revealed := false
	for plate_index in range(6):
		var current_plate_record: Dictionary = \
			main.castle_room_item_sprites.get(
				"meal_plate_%d" % plate_index, {}) as Dictionary
		var current_plate: Sprite3D = current_plate_record.get(
			"sprite") as Sprite3D
		stale_plate_revealed = stale_plate_revealed \
			or (current_plate != null and current_plate.visible)
	if rooms._room_build_generation == serving_generation \
			or int(main.g.get("castle_dining_plates", 0)) != 0 \
			or stale_plate_revealed:
		_bad("stale dining callbacks crossed a room rebuild generation")
	await _frames(24)
	if int(main.g.get("castle_dining_plates", 0)) != 0:
		_bad("stale dining completion changed the re-entered room state")

	rooms.show_room("royal_bedroom", false)
	await _frames(2)
	for bedroom_item: String in [
		"canopy_bed", "shell_wardrobe",
		"bedside_table", "reading_cushion"]:
		if not main.castle_room_item_sprites.has(bedroom_item):
			_bad("royal bedroom missing role-play prop %s" % bedroom_item)
	var wardrobe_record: Dictionary = main.castle_room_item_sprites.get(
		"shell_wardrobe", {}) as Dictionary
	var wardrobe_sprite: Sprite3D = wardrobe_record.get("sprite") as Sprite3D
	var wardrobe_transform: Transform3D = wardrobe_sprite.transform \
		if wardrobe_sprite != null else Transform3D.IDENTITY
	rooms._activate_room_item("shell_wardrobe")
	await _frames(24)
	if main.wardrobe_layer == null \
			or (main.wd.get("btns", []) as Array).size() != main.SKINS.size() \
			or wardrobe_sprite == null \
			or not wardrobe_sprite.transform.is_equal_approx(wardrobe_transform) \
			or String(wardrobe_sprite.get_meta(
				"normalized_use_animation", "")) \
				!= "wardrobe_glint_then_real_picker" \
			or int(wardrobe_sprite.get_meta(
				"roleplay_state_count", 0)) != 4:
		_bad("bedroom wardrobe did not open its real contents without deforming")
	var original_skin: String = main.skin_id
	var test_skin := "classic" if original_skin != "classic" else "huluu"
	var look_button: Button = main.wardrobe_layer.find_child(
		"WardrobeLook_" + test_skin, true, false) as Button \
		if main.wardrobe_layer != null else null
	var wardrobe_done: Button = main.wardrobe_layer.find_child(
		"WardrobeFinishButton", true, false) as Button \
		if main.wardrobe_layer != null else null
	if look_button == null or wardrobe_done == null:
		_bad("real wardrobe picker is missing a selectable look or finish button")
		main._close_wardrobe()
	else:
		look_button.pressed.emit()
		await process_frame
		wardrobe_done.pressed.emit()
		await _frames(2)
		var expected_castle_skin_path: String = \
			"res://assets/characters/roshan_25d/roshan_directional.png" \
			if test_skin == "classic" else main.skin_sprite_path()
		if main.wardrobe_layer != null \
				or main.castle_room_player_sprite == null \
				or main.castle_room_player_sprite.texture == null \
				or main.castle_room_player_sprite.texture.resource_path \
					!= expected_castle_skin_path \
				or String(main.castle_room_player_sprite.get_meta(
					"wardrobe_skin_id", "")) != test_skin:
			_bad("wardrobe choice did not refresh the in-room Roshan cutout")
	main.skin_id = original_skin
	main._apply_skin()
	main._write_save()
	await _frames(2)
	var bedside_record: Dictionary = main.castle_room_item_sprites.get(
		"bedside_table", {}) as Dictionary
	var bedside_sprite: Sprite3D = bedside_record.get("sprite") as Sprite3D
	var bedside_transform: Transform3D = bedside_sprite.transform \
		if bedside_sprite != null else Transform3D.IDENTITY
	var bedside_was_on := bool(main.g.get("castle_bedside_light_on", false))
	rooms._activate_room_item("bedside_table")
	await _frames(24)
	if bool(main.g.get("castle_bedside_light_on", false)) == bedside_was_on \
			or bedside_sprite == null \
			or not bedside_sprite.transform.is_equal_approx(bedside_transform) \
			or int(bedside_sprite.get_meta("roleplay_state_count", 0)) != 4 \
			or String(bedside_sprite.get_meta(
				"normalized_use_animation", "")) \
				!= "actual_light_brightness" \
			or bool(bedside_sprite.get_meta("busy", false)):
		_bad("bedside light did not sequence its actual brightness")
	var was_night: bool = main.is_night
	var bed_record: Dictionary = main.castle_room_item_sprites.get(
		"canopy_bed", {}) as Dictionary
	var bed_sprite: Sprite3D = bed_record.get("sprite") as Sprite3D
	rooms._activate_room_item("canopy_bed")
	await process_frame
	var sleep_overlay: ColorRect = main.castle_room_stage.get_node_or_null(
		"DreamHouseSleepFade") as ColorRect
	var sleep_marks: Label = main.castle_room_stage.get_node_or_null(
		"DreamHouseSleepMarks") as Label
	if not bool(main.g.get("castle_roleplay_sleeping", false)) \
			or sleep_overlay == null or sleep_marks == null:
		_bad("touching a royal bed did not start the cosy sleep sequence")
	else:
		rooms._flip_roleplay_sleep_time()
		rooms._finish_roleplay_sleep(
			sleep_overlay, sleep_marks, bed_sprite)
		await process_frame
		if main.is_night == was_night \
				or bool(main.g.get("castle_roleplay_sleeping", false)):
			_bad("dream-house sleep did not wake and toggle time")

	rooms.show_room("sleepover_bedroom", false)
	await _frames(2)
	for dream_bed_id: String in [
		"dream_bed_0", "dream_bed_1", "dream_bed_2"]:
		var dream_bed_record: Dictionary = main.castle_room_item_sprites.get(
			dream_bed_id, {}) as Dictionary
		var dream_bed_sprite: Sprite3D = dream_bed_record.get(
			"sprite") as Sprite3D
		if dream_bed_sprite == null \
				or String(dream_bed_sprite.get_meta(
					"roleplay_action", "")) != "sleep":
			_bad("sleepover room missing working bed %s" % dream_bed_id)

	rooms.show_room("movie_lounge", false)
	await _frames(2)
	var picture_record: Dictionary = main.castle_room_item_sprites.get(
		"movie_picture", {}) as Dictionary
	var picture_sprite: Sprite3D = picture_record.get("sprite") as Sprite3D
	var screen_record: Dictionary = main.castle_room_item_sprites.get(
		"movie_screen", {}) as Dictionary
	var screen_sprite: Sprite3D = screen_record.get("sprite") as Sprite3D
	var screen_transform: Transform3D = screen_sprite.transform \
		if screen_sprite != null else Transform3D.IDENTITY
	var movie_before: int = int(main.g.get("castle_movie_index", 0))
	rooms._activate_room_item("movie_screen")
	await _frames(30)
	var expected_movie: int = posmod(
		movie_before + 1, CastleRooms25D.MOVIE_IMAGES.size())
	if picture_sprite == null \
			or int(main.g.get("castle_movie_index", -1)) != expected_movie \
			or not bool(picture_sprite.get_meta("castle_soft_alpha", false)) \
			or picture_sprite.alpha_cut != SpriteBase3D.ALPHA_CUT_DISABLED \
			or picture_sprite.texture.resource_path \
				!= CastleRooms25D.MOVIE_IMAGES[expected_movie] \
			or not bool(picture_sprite.get_meta(
				"protected_original_displayed_directly", false)) \
			or int(picture_sprite.get_meta("roleplay_state_count", 0)) != 4 \
			or String(picture_sprite.get_meta(
				"normalized_use_animation", "")) \
				!= "actual_picture_crossfade" \
			or screen_sprite == null \
			or not screen_sprite.transform.is_equal_approx(screen_transform):
		_bad("movie screen did not crossfade the actual protected picture")
	var popcorn_record: Dictionary = main.castle_room_item_sprites.get(
		"movie_popcorn", {}) as Dictionary
	var popcorn_data: Dictionary = popcorn_record.get("data", {}) as Dictionary
	var popcorn_sprite: Sprite3D = popcorn_record.get("sprite") as Sprite3D
	var movie_after_screen := int(main.g.get("castle_movie_index", -1))
	rooms._activate_room_item("movie_popcorn")
	await _frames(4)
	if popcorn_sprite == null \
			or popcorn_record.get("hotspot") != null \
			or not bool(popcorn_data.get("proximity_only", false)) \
			or String(popcorn_data.get("roleplay_action", "")) != "" \
			or int(main.g.get("castle_movie_index", -1)) != movie_after_screen:
		_bad("movie snack still controls the film instead of remaining honest set dressing")
	for lounge_item: String in [
		"cloud_settee_left", "cloud_settee_right", "cloud_pouf"]:
		var lounge_record: Dictionary = main.castle_room_item_sprites.get(
			lounge_item, {}) as Dictionary
		var lounge_sprite: Sprite3D = lounge_record.get("sprite") as Sprite3D
		if lounge_sprite == null \
				or String(lounge_sprite.get_meta(
					"roleplay_action", "")) != "relax":
			_bad("movie lounge missing relaxing seat %s" % lounge_item)
	var left_settee_record: Dictionary = main.castle_room_item_sprites.get(
		"cloud_settee_left", {}) as Dictionary
	var left_settee: Sprite3D = left_settee_record.get("sprite") as Sprite3D
	var left_settee_data: Dictionary = left_settee_record.get(
		"data", {}) as Dictionary
	var left_settee_transform: Transform3D = left_settee.transform \
		if left_settee != null else Transform3D.IDENTITY
	rooms._activate_room_item("cloud_settee_left")
	await _frames(60)
	var expected_seat_foot: Vector2 = left_settee_data.get(
		"roleplay_foot", Vector2.INF) as Vector2
	var seated_foot: Vector2 = main.castle_room_player_sprite.get_meta(
		"current_stage_foot", Vector2.INF) as Vector2 \
		if main.castle_room_player_sprite != null else Vector2.INF
	if left_settee == null \
			or not left_settee.transform.is_equal_approx(left_settee_transform) \
			or not seated_foot.is_equal_approx(expected_seat_foot) \
			or String(left_settee.get_meta(
				"normalized_use_animation", "")) != "player_moves_to_seat" \
			or left_settee.has_meta("roleplay_state_count"):
		_bad("cloud couch deformed instead of moving Roshan onto the seat")

	rooms.show_room("bubble_bath", false)
	await _frames(2)
	for prop_id: String in ["bathtub", "sink", "toilet"]:
		if not main.castle_room_item_sprites.has(prop_id):
			_bad("bubble bath missing separate Sprite3D prop %s" % prop_id)
	var toilet_record: Dictionary = main.castle_room_item_sprites.get("toilet", {})
	var toilet_sprite: Sprite3D = toilet_record.get("sprite") as Sprite3D
	rooms._activate_room_item("toilet")
	await process_frame
	if toilet_sprite == null or not bool(toilet_sprite.get_meta("busy", false)):
		_bad("touching the toilet did not animate its Sprite3D card")
	if main.castle_room_prop_sfx == null or main.castle_room_prop_sfx.stream == null:
		_bad("touching a room prop did not attach relevant sound")
	main.castle_room_back_button.pressed.emit()
	await _frames(2)
	if main.castle_room_id != "main_hall":
		_bad("room Back did not return to the Main Hall")
	rooms.activate_current_room()
	# Royal Hall is a real walk-then-arrive doorway now, not the retired
	# instant throne action. Wait for the authored approach callback.
	var royal_hall_deadline_ms: int = Time.get_ticks_msec() + 3000
	while not bool(main.g.get("crown_won", false)) \
			and Time.get_ticks_msec() < royal_hall_deadline_ms:
		await process_frame
	if not bool(main.g.get("crown_won", false)):
		_bad("eligible Royal Hall event did not award the Crown Star")

	# Pointer-driven activities may temporarily cover the castle, but closing a
	# nested overlay must return to the room stage rather than resurrecting the
	# retired free-roaming controls.
	main._mg2d_open("garden")
	await process_frame
	if main.touch_ui.world_controls_enabled or (main.touch_ui._act_button != null and main.touch_ui._act_button.visible):
		_bad("world action controls occluded a picture game")
	# Nested pause overlays must release only their own block; closing Sticker
	# Book while the picture game remains open cannot resurrect world controls.
	main._open_stickers()
	await process_frame
	main._close_stickers()
	await process_frame
	if main.touch_ui.world_controls_enabled or (main.touch_ui._act_button != null and main.touch_ui._act_button.visible):
		_bad("closing nested overlay re-enabled controls above picture game")
	main._mg2d_close()
	await process_frame
	if main.touch_ui.world_controls_enabled:
		_bad("picture game close enabled 3D controls over castle stage")

	# Leaving the picture stage clears stale assisted navigation and restores the
	# courtyard. The room overlay and its Sprite3D world must be fully released.
	main.touch_focus_id = "retired:hall"
	main.touch_auto_active = true
	rooms._exit_to_courtyard()
	main._on_touch_world(main.get_viewport().get_visible_rect().size * 0.5)
	if not main.touch_focus_id.is_empty() or main.touch_auto_active:
		_bad("rapid transition tap retained or created stale navigation")
	if main.fade_rect != null and main.fade_rect.mouse_filter != Control.MOUSE_FILTER_STOP:
		_bad("fade cover did not claim touches during transition")
	await _frames(8)

	# Leaving Level 2 directly from the castle must also tear down both UI and
	# world-card roots; otherwise the old stage can remain over the reef.
	main._enter_castle_interior_now(false)
	await _frames(12)
	main._exit_level2_now()
	await _frames(4)
	if not main.touch_ui.world_controls_enabled:
		_bad("leaving the castle left touch controls blocked")
	if rooms.is_open() or main.castle_room_world_root != null:
		_bad("leaving Level 2 retained the castle Sprite3D stage")

	# Fix regression (Hybrid contract): the sparring den may advertise by
	# proximity but must start ONLY from its explicit tap target.
	main.companion_id = "eagle"
	main.companion_resting = false
	main.stuffie_cool = 0.0
	await _frames(30)
	if main.companion_den == null or not is_instance_valid(main.companion_den):
		_bad("companion den never built for the contract check")
	else:
		main.player.position = main.companion_den.position + Vector3(1.0, 1.0, 0.0)
		main.player.vel = Vector3.ZERO
		await _frames(20)
		if main.game != "":
			_bad("Hybrid proximity auto-started the sparring battle")
		main._populate_touch_interactables()
		if not _ids().has("reef:den"):
			_bad("sparring den is not an explicit touch target in Hybrid")
		main._activate_touch_interactable("reef:den")
		await _frames(4)
		if main.game != "stuffie":
			_bad("explicit den target did not start the battle")
		if bool(main.touch_auto_active) or not main.touch_focus_id.is_empty():
			_bad("battle start kept stale focus/assisted travel")

	main._set_touch_mode("classic", false)
	if main.touch_uses_explicit_interactions() or main.touch_auto_active:
		_bad("Classic rollback left Hybrid systems active")
	_finish()

func _ids() -> Array[String]:
	var result: Array[String] = []
	for item_value: Variant in main.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		result.append(String(item.get("id", "")))
	return result

func _has_id_prefix(prefix: String) -> bool:
	for interactable_id: String in _ids():
		if interactable_id.begins_with(prefix):
			return true
	return false

func _wait_for_castle_room(expected_room: String,
		timeout_ms: int = 1500) -> bool:
	var deadline: int = Time.get_ticks_msec() + timeout_ms
	while main.castle_room_id != expected_room \
			and Time.get_ticks_msec() < deadline:
		await process_frame
	return main.castle_room_id == expected_room


func _audit_native_route_fallback(rooms: CastleRooms25D) -> void:
	# Force the same atomic rejection path used for a corrupt or wrongly decoded
	# native tile without changing any source asset. Every V4 room must render its
	# complete intact fallback plate and must omit all source-owned replacement
	# cards, including the overlapping refrigerator and four pool fixtures.
	rooms.fixture_rigs._ensure_manifest()
	var original_specs: Dictionary = \
		rooms.fixture_rigs._native_background_tile_specs.duplicate(true)
	for room_id_value: Variant in NATIVE_FALLBACK_ITEMS:
		var room_id := String(room_id_value)
		var original_spec: Dictionary = original_specs.get(room_id, {}) as Dictionary
		if original_spec.is_empty():
			_bad("native fallback probe has no route spec for %s" % room_id)
			continue
		var rejected_spec := original_spec.duplicate(true)
		var expected_dimensions: Vector2i = rejected_spec.get(
			"tile_dimensions", Vector2i.ZERO)
		rejected_spec["tile_dimensions"] = Vector2i(
			expected_dimensions.x, maxi(1, expected_dimensions.y - 1))
		rooms.fixture_rigs._native_background_tile_specs[room_id] = rejected_spec
		rooms.show_room(room_id, false)
		await _frames(2)
		var expected_tile_count := int(
			NATIVE_FALLBACK_TILE_COUNTS.get(room_id, 0))
		if main.castle_room_detail_tiles.size() != expected_tile_count:
			_bad("rejected native route lost fallback tiles for %s" % room_id)
		for tile: Sprite3D in main.castle_room_detail_tiles:
			if bool(tile.get_meta(
					"native_source_ownership_background", true)) \
					or String(tile.get_meta("runtime_background_tile_root", "")) \
						!= CastleRooms25D.ROOM_TILE_ROOT:
				_bad("rejected native route retained healed tiles for %s" % room_id)
				break
		var source_owned_items: Array = NATIVE_FALLBACK_ITEMS.get(
			room_id, []) as Array
		for item_id_value: Variant in source_owned_items:
			var item_id := String(item_id_value)
			if main.castle_room_item_sprites.has(item_id):
				_bad("rejected native route layered %s:%s over fallback paint" % [
					room_id, item_id])
		rooms.fixture_rigs._native_background_tile_specs[room_id] = \
			original_spec.duplicate(true)
	rooms.fixture_rigs._native_background_tile_specs = original_specs
	rooms.fixture_rigs._active_native_background_rooms.clear()

	# Native-route forcing must never change the unrelated Dream House 2 x 2
	# legacy grid. This also guards the default-grid regression explicitly.
	rooms.show_room("family_gallery", false)
	await _frames(2)
	if main.castle_room_detail_tiles.size() != 4:
		_bad("native rejection changed Dream House legacy tile count")
	for tile: Sprite3D in main.castle_room_detail_tiles:
		if String(tile.get_meta("source_master_grid", "")) != "2x2_2k" \
				or tile.get_meta("native_texture_size", Vector2.ZERO) \
					!= Vector2(1024.0, 576.0):
			_bad("native rejection changed Dream House legacy grid geometry")
			break

func _frames(count: int) -> void:
	for frame_index in range(count):
		await process_frame

func _bad(message: String) -> void:
	failures += 1
	print("INTERACTION|FAIL ", message)

func _finish() -> void:
	if failures == 0:
		print("INTERACTION|ALL OK")
		quit()
	else:
		print("INTERACTION|FAIL %d issue(s)" % failures)
		quit(1)
