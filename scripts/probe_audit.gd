extends SceneTree
# AUDIT BOT — corrected version of probe_games.gd (fixes stale cosmetics/tiara/tail
# and ColorRect casts). Prints incrementally so timeouts never lose results.
var main: Node3D
var player: Node3D

const MELODY_TILE_PATHS: Array[String] = [
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c3.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c3.png",
]
const MELODY_TILE_NODES: Array[String] = [
	"SkyLagoonBackdrop_r0_c2", "SkyLagoonBackdrop_r0_c3",
	"SkyLagoonBackdrop_r1_c2", "SkyLagoonBackdrop_r1_c3",
]
const MELODY_TILE_SOURCE_RECTS: Array[Rect2i] = [
	Rect2i(0, 0, 1024, 1024), Rect2i(1024, 0, 1024, 1024),
	Rect2i(0, 1024, 1024, 1024), Rect2i(1024, 1024, 1024, 1024),
]
const MELODY_DADDY_PATH := "res://assets/characters/stickers/daddy.png"
const MELODY_ROSHAN_PATH := "res://assets/opera/worlds/actors/roshan_popstar.png"

func _init() -> void:
	var seed_str := OS.get_environment("AUDIT_SEED")
	if seed_str != "":
		seed(int(seed_str))
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	var ui_ok: bool = await _audit_storybook_ui()
	print("AUDIT|Storybook UI contract: ", "OK" if ui_ok else "FAIL")
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	player = main.player
	print("AUDIT|boot OK, seed=", seed_str)
	var patrol_x := 140.0
	var patrol_z := -115.0
	var patrol_y: float = main._aquatic_patrol_height(patrol_x, patrol_z, -100.0, 4.0)
	var aquatic_continuity: bool = (patrol_y >= main.seabed_y(patrol_x, patrol_z) + 3.99
		and patrol_y <= main.WATER_TOP - 3.0
		and is_equal_approx(main._aquatic_patrol_height(0.0, 0.0, 20.0), 20.0))
	print("AUDIT|Aquatic patrol terrain clearance: ", "OK" if aquatic_continuity else "FAIL")
	var seek_art_ready := true
	for seek_art_path: String in SeekGame.runtime_art_paths():
		seek_art_ready = seek_art_ready \
			and ResourceLoader.exists(seek_art_path)
	print("AUDIT|Seek Canvas authored atlas and v5 meadow art: ",
		"OK" if seek_art_ready else "FAIL")
	print("AUDIT|Penguin floe at water surface: ",
		"OK" if absf(main.slide_portal_pos.y - (main.WATER_TOP + 0.5)) < 0.01 else "FAIL")
	var t_start := Time.get_ticks_msec()
	# --- Critter Book: approach + one real touch-action edge catches exactly one ---
	main.critter_collection = {}
	var collection: CollectionSystem = main._collection_ref()
	var first_critter: Dictionary = main.collection_nodes[0]
	var critter_node: Node3D = first_critter["node"]
	var critter_def: Dictionary = first_critter["def"]
	player.position = critter_node.position
	player.vel = Vector3.ZERO
	main.touch_ui.action_down = false
	await process_frame
	main.touch_ui.action_down = true
	await process_frame
	main.touch_ui.action_down = false
	var critter_ok: bool = collection.caught_count() == 1 and bool(main.critter_collection.get(String(critter_def["id"]), false))
	print("AUDIT|Critter Book: ", ("OK" if critter_ok else "FAIL"))
	for fi in range(5):
		var f: Dictionary = main.friends[fi]
		var fname: String = f["fname"]
		var node: Node3D = f["node"]
		player.position = node.position + Vector3(3, 0, 0)
		player.vel = Vector3.ZERO
		await _frames(10)
		var guard := 0
		while float(f["cool"]) > 0.0 and guard < 3000:
			guard += 1
			await process_frame
		for k in range(10):
			player.position = node.position + Vector3(3, 0, 0)
			player.vel = Vector3.ZERO
			await process_frame
		var friend_route_position: Variant = player.position
		var friend_route_environment: Variant = main.we_node.environment
		if main.game == "" and main.touch_uses_explicit_interactions():
			main._activate_touch_interactable("friend:%d" % fi, fi)
			await _frames(10)
		if main.game == "":
			print("AUDIT|", fname, ": GAME DID NOT START")
			continue
		var gname: String = main.game
		var cutaway_ok: bool = player.position == friend_route_position \
			and main.we_node.environment == friend_route_environment \
			if gname == "melody" else \
			player.position.distance_to(main.ARENA_POS) <= 120.0
		if gname == "melody":
			var melody := main._game_obj("melody", MelodyGame) as MelodyGame
			var layer: CanvasLayer = melody.active_layer()
			var surface: Node2D = melody.surface()
			var stage_ok: bool = layer != null and surface != null \
				and layer.name == &"MelodyCanvasLayer" \
				and surface.name == &"RainbowTheaterCanvas" \
				and melody.stage_root() == surface \
				and _melody_surface_exact(surface) \
				and _melody_tile_bindings_exact(surface) \
				and _melody_spatial_descendant_count(layer) == 0 \
				and surface.find_child("LeftCurtainGeometry", true, false) != null \
				and surface.find_child("RightCurtainGeometry", true, false) != null \
				and surface.find_child("DaddyGuide", true, false) != null \
				and surface.find_child("PopstarRoshan", true, false) != null \
				and surface.find_child("TimingZone", true, false) != null \
				and surface.find_child("VisualPointer", true, false) != null \
				and melody.note_count() == 7 \
				and melody.progress_count() == 0
			print("AUDIT|Rainbow Canvas theater: ", ("OK" if stage_ok else "FAIL"))
		var f0 := Time.get_ticks_msec()
		var ok := await _drive_game(gname, f)
		var secs := float(Time.get_ticks_msec() - f0) / 1000.0
		print("AUDIT|", fname, " [", gname, "]: ", ("WON" if ok else "FAILED/TIMEOUT"),
			" cutaway=", cutaway_ok, " wall_s=%.1f" % secs)
		main._clear_game()
		await _frames(5)
	# --- toy castle brawler (two heroes: Roshan + AI Huluu) ---
	main.brawl_cool = 0.0
	player.position = main.brawl_portal_pos + Vector3(0, 2, 3)
	player.vel = Vector3.ZERO
	if main.touch_uses_explicit_interactions():
		main._activate_touch_interactable("reef:brawl")
	var bwait := 0
	while main.game == "" and bwait < 900:
		bwait += 1
		player.position = main.brawl_portal_pos + Vector3(0, 2, 3)
		player.vel = Vector3.ZERO
		await process_frame
	if main.game == "brawl":
		var okb := await _drive_game("brawl", main.brawl_fr)
		main.touch_ui.action_down = false
		print("AUDIT|Toy Castle [brawl]: ", ("WON co-op" if okb else "FAILED/TIMEOUT"))
	else:
		print("AUDIT|Toy Castle [brawl]: DID NOT START")
	# _end_game put her back beside the toy castle; with the short "again!"
	# re-entry cooldown (3s) the brawl would auto-restart mid-beans-test if
	# she stayed parked in the portal radius — park in open water instead
	player.position = main.ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	# --- beans consumable (current shop API) ---
	main.pearl_count = 5
	main._shop_buy("beans")
	# beans banjo is a SOUND EFFECT now (dedicated beans_sfx player, works with
	# music off — explicit behaviour change requested earlier), so assert that
	# instead of the old cur_track swap
	var beans_on: bool = main.speed_mult == 2.0 and main.beans_t > 0.0 and main.beans_sfx != null and main.beans_sfx.playing and main.pearl_count == 3
	main.beans_t = 0.01
	for i5 in range(30):
		await process_frame
	var beans_off: bool = main.speed_mult == 1.0 and (main.beans_sfx == null or not main.beans_sfx.playing)
	print("AUDIT|Can of Beans: ", ("OK" if beans_on and beans_off else "FAIL on=%s off=%s" % [beans_on, beans_off]))
	# --- tank idle rigs (the turtle skeleton must actually flap) ---
	main._start_game(main.shop_fr)
	await _frames(10)
	var tanks: Array = main.g.get("tanks", [])
	var turtle_rig: Dictionary = {}
	for tk in tanks:
		if String(tk["id"]) == "turtle":
			turtle_rig = tk.get("rig", {})
	var rig_skel: Skeleton3D = turtle_rig.get("skel", null)
	var flap0 := Quaternion.IDENTITY
	if rig_skel != null:
		flap0 = rig_skel.get_bone_pose_rotation(3)
	await _frames(30)
	var flapped := false
	if rig_skel != null and is_instance_valid(rig_skel):
		flapped = rig_skel.get_bone_pose_rotation(3).angle_to(flap0) > 0.02
	var rig_line: String = "FAIL tanks=%d skel=%s flapped=%s" % [tanks.size(), rig_skel != null, flapped]
	if tanks.size() == 4 and rig_skel != null and rig_skel.get_bone_count() == 7 and flapped:
		rig_line = "OK bones=%d flapped=true" % rig_skel.get_bone_count()
	print("AUDIT|Tank idle rig: ", rig_line)
	main._clear_game()
	await _frames(5)
	# --- animal tanks (the pearl sink: buy the turtle free, it joins the reef) ---
	main.pearl_count = 30
	var movers0: int = main.aquatic_movers.size()
	main._tank_buy("turtle")
	var pets := 0
	var pets_rigged := 0
	for mv0 in main.aquatic_movers:
		if String(mv0.get("shop_pet", "")) == "turtle":
			pets += 1
			if mv0.has("rig"):
				pets_rigged += 1
	var tank_ok: bool = main.pearl_count == 5 and bool(main.animals_owned.get("turtle", false)) \
		and main.aquatic_movers.size() > movers0 and pets >= 1 and pets_rigged == pets
	main._tank_buy("turtle")   # already free: must not charge or double-spawn
	var tank_once: bool = main.pearl_count == 5 and main.aquatic_movers.size() == movers0 + pets
	main.pearl_count = 3
	main._tank_buy("dolphin")  # too few pearls: must not sell
	var tank_poor: bool = main.pearl_count == 3 and not bool(main.animals_owned.get("dolphin", false))
	var tank_line: String = "OK swimming=%d rigged=%d" % [pets, pets_rigged]
	if not (tank_ok and tank_once and tank_poor):
		tank_line = "FAIL buy=%s once=%s poor=%s pets=%d rigged=%d" % [tank_ok, tank_once, tank_poor, pets, pets_rigged]
	print("AUDIT|Animal tanks: ", tank_line)
	# --- pearl respawn ---
	var p1: Node3D = main.pearls[0]
	player.position = p1.position
	player.vel = Vector3.ZERO
	for i6 in range(10):
		await process_frame
	var collected: bool = main.pearls.size() == 9
	main._respawn_pearls()
	print("AUDIT|Pearl respawn: ", ("OK" if collected and main.pearls.size() == 10 else "FAIL"))
	# --- level 2 ---
	main.portal_unlocked = false
	main.pearl_count = main.PEARL_TOTAL - 1
	main.pearls_ever = main.PEARL_TOTAL - 1
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	main._check_level2_unlock(player.position, 0.1)
	print("AUDIT|Level 2 nine-pearl lock: ", ("OK" if not main.portal_unlocked and main.portal_node == null else "FAIL"))
	main.pearl_count = main.PEARL_TOTAL
	var pf := 0
	while main.portal_node == null and pf < 300:
		pf += 1
		main._check_level2_unlock(player.position, 0.1)
		await process_frame
	print("AUDIT|Level 2 portal: ", ("OK" if main.portal_node != null else "FAIL"))
	main.pearl_count = 0
	main._check_level2_unlock(player.position, 0.1)
	print("AUDIT|Level 2 portal stays unlocked after spending: ", ("OK" if main.portal_unlocked and main.portal_node != null else "FAIL"))
	if main.portal_node != null:
		var portal_route_ok := true
		if main.touch_uses_explicit_interactions():
			# Hybrid uses the visible ENTER affordance; walking into its ring must
			# remain safe and must never bypass the child's deliberate tap.
			player.position = main.portal_node.position
			player.position.x += 20.0
			player.position.y += 6.0
			player.position.z += 20.0
			player.vel *= 0.0
			main._check_level2_unlock(player.position, 0.1)
			await process_frame
			player.position = main.portal_node.position
			player.vel *= 0.0
			main._check_level2_unlock(player.position, 0.1)
			await process_frame
			var hybrid_proximity_safe: bool = main.game == ""
			main._populate_touch_interactables()
			var lagoon_route_registered := false
			for item_value: Variant in main.touch_interactables:
				var item: Dictionary = item_value as Dictionary
				if String(item.get("id", "")) == "reef:lagoon" \
						and bool(item.get("enabled", false)):
					lagoon_route_registered = true
					break
			portal_route_ok = hybrid_proximity_safe \
				and lagoon_route_registered
			if portal_route_ok:
				main._activate_touch_interactable("reef:lagoon")
		else:
			# Classic/no-touch keep the original leave-to-arm, return-to-enter
			# proximity route.
			var rf := 0
			while main.game == "" and rf < 600:
				rf += 1
				if not main.portal_armed:
					player.position = main.portal_node.position + Vector3(20, 6, 20)
				else:
					player.position = main.portal_node.position
				player.vel = Vector3.ZERO
				main._check_level2_unlock(player.position, 0.1)
				await process_frame
			portal_route_ok = main.game == "level2"
		print("AUDIT|Level 2 courtyard: ",
			("OK" if portal_route_ok and main.game == "level2" else "FAIL"))
		var targets: Array = main.g.get("lagoon_promenade_targets", [])
		var target_ids: Dictionary = {}
		for target_value in targets:
			var target: Dictionary = target_value as Dictionary
			target_ids[String(target.get("id", ""))] = true
		var core_roster_ok: bool = true
		for required_id: String in ["slide", "swing", "seesaw", "castle_gate"]:
			core_roster_ok = core_roster_ok and target_ids.has(required_id)
		var promenade_ok: bool = (
			String(main.g.get("phase", "")) == "promenade"
			and targets.size() == 5
			and core_roster_ok
			and main._lagoon_promenade_ref().root() is CanvasLayer
			and main._lagoon_promenade_ref().camera_2d() is Camera2D
			and float(main.g.get("lagoon_master_x", -1.0)) >= 0.0
			and float(main.g.get("lagoon_master_x", -1.0)) <= 6144.0
			and not main.player.visible)
		print("AUDIT|Level 2 three-screen promenade: ",
			("OK" if promenade_ok else "FAIL"), " targets=", targets.size())
		# The castle drawbridge is an explicit two-press landmark in the new
		# promenade. The focused second press enters the existing castle hall.
		var castle_target: Dictionary = {}
		for target_value in targets:
			var target: Dictionary = target_value as Dictionary
			if String(target.get("id", "")) == "castle_gate":
				castle_target = target
				break
		if not castle_target.is_empty():
			main._lagoon_promenade_ref()._focus(castle_target)
			main._lagoon_promenade_ref()._activate(castle_target)
			await _frames(10)
		var hall_ok: bool = main.game == "level2" and String(main.g.get("phase","")) == "hall"
		var rooms_a: CastleRooms25D = main._castle_rooms_ref()
		var stage_ok: bool = hall_ok and rooms_a.is_open() \
			and main.castle_room_world_root != null \
			and main.castle_room_camera != null \
			and main.castle_room_camera.projection \
				== Camera3D.PROJECTION_PERSPECTIVE \
			and main.touch_interactables.is_empty()
		print("AUDIT|Level 2 castle Sprite3D stage: ",
			("OK" if stage_ok else "FAIL"),
			" game=", main.game, " phase=", String(main.g.get("phase","?")),
			" mg_kind=", main.mg_kind, " stars_got=", _stars_got(), " l2_open=", main.l2_open)
		# The hall phase must not construct the retired model-based interior or
		# its physical navigation/interaction state.
		var legacy_hall_absent: bool = main.game_nodes.is_empty() \
			and main.arena_solids.is_empty() \
			and main.arena_zones.is_empty()
		for retired_key: String in [
			"hall_exit", "bed_pos", "stand_chest", "toilet", "dungeon_gate",
			"craft_easel", "wardrobe", "song_star", "secret_door",
			"hall_touch", "bells", "opera_gate"]:
			legacy_hall_absent = legacy_hall_absent \
				and not main.g.has(retired_key)
		print("AUDIT|retired 3D castle absent: ",
			("OK" if legacy_hall_absent else "FAIL"))
		var room_routes_ok: bool = main.castle_room_buttons.size() == 8 \
			and main.castle_room_buttons.has("family_gallery") \
			and main.castle_room_buttons.has("opera_hall") \
			and main.castle_room_buttons.has("bubble_bath") \
			and main.castle_room_back_button != null \
			and main.castle_room_stage.get_node_or_null("ElevatorButton") != null \
			and main.castle_room_menu_buttons.size() == 12 \
			and main.castle_room_menu_buttons.has("dining_room") \
			and main.castle_room_menu_buttons.has("movie_lounge") \
			and not main.castle_room_menu_buttons.has("family_gallery")
		print("AUDIT|castle physical doors plus direct elevator routes: ",
			("OK" if room_routes_ok else "FAIL"))
		# The eligible Royal Hall event celebrates in place and records the win
		# without switching back to the free-roaming world.
		if stage_ok:
			rooms_a.show_room("main_hall", false)
			rooms_a.activate_current_room()
			var royal_hall_deadline_msec: int = Time.get_ticks_msec() + 3000
			while not bool(main.g.get("crown_won", false)) \
					and Time.get_ticks_msec() < royal_hall_deadline_msec:
				await process_frame
		print("AUDIT|Royal Hall Crown finish: ", ("OK" if bool(main.g.get("crown_won", false)) and bool(main.save_data.get("level2", false)) else "FAIL"))
	for i2 in range(60):
		await process_frame
	print("AUDIT|save file: ", ("OK" if FileAccess.file_exists("user://reef_save.json") else "MISSING"))
	print("AUDIT|finale: ", ("OK" if main.finale_done else "DID NOT TRIGGER"))
	var f3 := FileAccess.open("user://reef_save.json", FileAccess.READ)
	if f3 != null:
		var d3: Variant = JSON.parse_string(f3.get_as_text())
		if d3 is Dictionary:
			var wn: Dictionary = (d3 as Dictionary).get("won", {})
			var cnt := 0
			for k in wn:
				if bool(wn[k]):
					cnt += 1
			print("AUDIT|persisted wins: ", cnt, "/5")
	print("AUDIT|total wall time: %.1fs" % (float(Time.get_ticks_msec() - t_start) / 1000.0))
	quit()

func _audit_storybook_ui() -> bool:
	var ok := true
	if not main.intro_active:
		main._build_intro()
	await process_frame
	ok = _ui_named_count(main.intro_layer, "IntroNextButton") == 1 and ok
	ok = _ui_target_ok(main.intro_layer, "IntroNextButton", Vector2(150, 150)) and ok
	ok = _ui_target_ok(main.intro_layer, "IntroRepeatVoiceButton") and ok
	var skip := main.intro_layer.find_child("IntroHoldToSkipButton", true, false) as Control
	ok = skip != null and float(skip.get_meta("hold_seconds", 0.0)) >= 1.2 and ok
	ok = (main.intro_layer.get_meta("page_pips", []) as Array).size() == 4 and ok
	main._skip_intro()
	await process_frame

	ok = _ui_target_ok(main.pause_layer, "PauseCornerButton", Vector2(128, 128)) and ok
	main.toggle_pause()
	ok = main.pause_layer.layer == 29 and main.get_tree().paused and ok
	ok = _ui_target_ok(main.pause_panel, "PauseResumeButton", Vector2(300, 140)) and ok
	ok = _ui_target_ok(main.pause_panel, "PauseStickerButton") and ok
	ok = _ui_target_ok(main.pause_panel, "PauseMusicButton") and ok
	ok = _ui_target_ok(main.pause_panel, "PauseQualityButton") and ok
	var leave := main.pause_panel.find_child("PauseLeaveButton", true, false) as Button
	ok = leave != null and bool(leave.get_meta("neutral_exit", false)) and ok
	main.toggle_pause()
	ok = main.pause_layer.layer == 12 and not main.get_tree().paused and ok

	main._open_craft_studio()
	await process_frame
	ok = _ui_target_ok(main.craft_layer, "CraftBackButton") and ok
	ok = _ui_target_ok(main.craft_layer, "CraftFinishButton", Vector2(150, 150)) and ok
	ok = _ui_named_count(main.craft_layer, "CraftPart_*") == 3 and ok
	ok = _ui_named_count(main.craft_layer, "CraftSwatch_*") == 8 and ok
	ok = _ui_named_count(main.craft_layer, "CraftRainbowSwatch") == 1 and ok
	main._close_craft()

	main._open_castle_logo()
	await process_frame
	ok = _ui_target_ok(main.castle_logo_layer, "CastleLogoBackButton") and ok
	ok = _ui_target_ok(main.castle_logo_layer, "CastleLogoFinishButton", Vector2(150, 150)) and ok
	ok = _ui_named_count(main.castle_logo_layer, "CastleLogoColor_*") == 6 and ok
	ok = _ui_named_count(main.castle_logo_layer, "CastleLogoSymbol_*") == 8 and ok
	main._close_castle_logo()

	main._open_wardrobe()
	await process_frame
	ok = _ui_target_ok(main.wardrobe_layer, "WardrobeBackButton") and ok
	ok = _ui_target_ok(main.wardrobe_layer, "WardrobeFinishButton") and ok
	main._close_wardrobe()
	main._open_stickers()
	await process_frame
	ok = _ui_target_ok(main.stickers_layer, "StickerBookBackButton") and ok
	main._close_stickers()

	main._collection_ref().open_book()
	await process_frame
	ok = _ui_target_ok(main.collection_layer, "CritterBookBackButton") and ok
	main._collection_ref().close_book()

	main._companion_ref().open_picker(false)
	await process_frame
	ok = _ui_target_ok(main.companion_layer, "StuffiePickerBackButton") and ok
	ok = _ui_named_count(main.companion_layer, "StuffiePart_*") == 3 and ok
	ok = _ui_named_count(main.companion_layer, "StuffieSwatch_*") == 8 and ok
	main._companion_ref().close_picker()

	main._mg2d_open("garden")
	await process_frame
	var picture_back := main.mg2d_layer.find_child("PictureGameBackButton", true, false) as Button
	ok = picture_back != null and _ui_target_ok(main.mg2d_layer, "PictureGameBackButton") and ok
	ok = picture_back != null and bool(picture_back.get_meta("neutral_exit", false)) and ok
	main._mg2d_close()
	main.mg_cool = 0.0
	return ok

func _ui_named_count(from: Node, pattern: String) -> int:
	var count := 0
	for node: Node in from.find_children(pattern, "", true, false):
		if node is Control:
			count += 1
	return count

func _ui_target_ok(from: Node, pattern: String, minimum := Vector2(110, 110)) -> bool:
	var control := from.find_child(pattern, true, false) as Control
	if control == null:
		return false
	var touch_size := Vector2(
		maxf(control.size.x, control.custom_minimum_size.x),
		maxf(control.size.y, control.custom_minimum_size.y)
	)
	return touch_size.x >= minimum.x and touch_size.y >= minimum.y

func _stars_got() -> int:
	var got := 0
	for sd in main.l2_stars:
		if bool(sd["got"]):
			got += 1
	return got

func _frames(n: int):
	for i in range(n):
		await process_frame

func _drive_game(gname: String, f: Dictionary) -> bool:
	var deadline := 60.0 * 90.0
	var fcount := 0
	player.position = main.ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	while main.game != "" and fcount < deadline:
		fcount += 1
		var g: Dictionary = main.g
		if gname == "fetch":
			if g.has("phase") and String(g["phase"]) == "aim":
				var ad: Vector3 = g.get("aim_dir", Vector3.ZERO)
				main.touch_ui.action_down = ad != Vector3.ZERO and ad.x < 0.1 and fcount % 12 < 6
			else:
				main.touch_ui.action_down = false
		elif gname == "dolls":
			# Perform the real one-finger Canvas verb. A complete press/drag/release
			# gesture each frame follows the lowest baby and keeps the two-second
			# live-input memory honest without calling the surface's steering API.
			var dolls_surface := g.get("dolls_surface") as OperaNurseryCatch
			if dolls_surface != null and is_instance_valid(dolls_surface):
				var want_x: float = dolls_surface.lowest_baby_x()
				if want_x < 0.0:
					want_x = 0.5
				var local_point := Vector2(
					clampf(want_x, 0.1, 0.9) * dolls_surface.size.x,
					dolls_surface.size.y * 0.72)
				var drag_local := local_point + Vector2(0.5, 0.0)
				var screen_point: Vector2 = \
					dolls_surface.get_screen_transform() * local_point
				var drag_screen: Vector2 = \
					dolls_surface.get_screen_transform() * drag_local
				var viewport := dolls_surface.get_viewport()
				var touch_down := InputEventScreenTouch.new()
				touch_down.index = 51
				touch_down.position = screen_point
				touch_down.pressed = true
				viewport.push_input(touch_down, true)
				var touch_drag := InputEventScreenDrag.new()
				touch_drag.index = 51
				touch_drag.position = drag_screen
				touch_drag.relative = drag_screen - screen_point
				viewport.push_input(touch_drag, true)
				var touch_up := InputEventScreenTouch.new()
				touch_up.index = 51
				touch_up.position = drag_screen
				touch_up.pressed = false
				viewport.push_input(touch_up, true)
		elif gname == "brawl":
			# walk the plane to the nearest live imp (stick x AND depth y),
			# pulse fresh tap edges inside pop range — Huluu's AI stuns are
			# assists only, so the win must come from these taps
			var imps: Array = g.get("enemies", [])
			var btarget: Node3D = null
			var bbest := 1e9
			for e in imps:
				var en: Node3D = (e as Dictionary).get("node") as Node3D
				if en == null or not is_instance_valid(en):
					continue
				var bd: float = Vector2(en.global_position.x - main.player.global_position.x,
					en.global_position.z - main.player.global_position.z).length()
				if bd < bbest:
					bbest = bd
					btarget = en
			if btarget != null:
				var bdx: float = btarget.global_position.x - main.player.global_position.x
				var bdz: float = btarget.global_position.z - main.player.global_position.z
				main.touch_ui.stick_vec = Vector2(clampf(bdx / 3.6, -1.0, 1.0), clampf(bdz / 3.6, -1.0, 1.0))
				main.touch_ui.action_down = bbest < 5.0 and fcount % 14 < 7
			else:
				main.touch_ui.stick_vec = Vector2(0.5, 0.0)   # walk to the next gate
				main.touch_ui.action_down = false
		elif gname == "seek":
			var seek_surface := g.get("seek_surface") \
				as SeekGame.SeekMeadowSurface
			if seek_surface != null and is_instance_valid(seek_surface) \
					and not seek_surface.revealing:
				var seek_target := seek_surface.bush_hit_rect(
					int(g.get("which", 0))).get_center()
				var seek_touch := InputEventScreenTouch.new()
				seek_touch.index = 52
				var seek_viewport: Viewport = seek_surface.get_viewport()
				var seek_screen: Vector2 = seek_viewport.get_screen_transform() \
					* (seek_surface.get_screen_transform() * seek_target)
				seek_touch.position = seek_screen
				seek_touch.pressed = true
				seek_viewport.push_input(seek_touch, false)
				seek_touch.pressed = false
				seek_viewport.push_input(seek_touch, false)
		elif gname == "slide":
			# Exercise the deliberate lean that the downhill ride requires.
			var weave: float = 0.65 if int(fcount / 45) % 2 == 0 else -0.65
			main.touch_ui.stick_vec = Vector2(weave, 0.0)
		elif gname == "race" or gname == "treasure":
			if String(g.get("phase", "")) != "slide":
				var checks: Array = g.get("checks", [])
				for c in checks:
					if not c["hit"]:
						player.position = player.position.lerp((c["node"] as Node3D).position, 0.10)
						player.vel = Vector3.ZERO
						break
		elif gname == "melody":
			var melody := main._game_obj("melody", MelodyGame) as MelodyGame
			var note_point: Vector2 = melody.active_note_screen_point()
			var timing_zone: Rect2 = melody.timing_zone_screen_rect()
			if melody.active_note_id() >= 0 and timing_zone.has_point(note_point):
				var melody_touch := InputEventScreenTouch.new()
				melody_touch.index = 53
				melody_touch.position = note_point
				melody_touch.pressed = true
				# active_note_screen_point() is already in this Viewport's local
				# Canvas coordinates. The broad headless audit can expose a square
				# visible rect, so asking Viewport to reinterpret it as an external
				# window coordinate moves the press away from the note.
				main.get_viewport().push_input(melody_touch, true)
				var melody_release := InputEventScreenTouch.new()
				melody_release.index = 53
				melody_release.position = note_point
				melody_release.pressed = false
				main.get_viewport().push_input(melody_release, true)
		await process_frame
	main.touch_ui.stick_vec = Vector2.ZERO   # release the virtual hand
	return main.game == "" and bool(f["won"])


func _melody_surface_exact(surface: Node) -> bool:
	if surface == null:
		return false
	var expected: Array[String] = [
		"OpaqueTheaterFill", "ScenicBackcloth", "OperaProscenium",
		"StageFootlights", "StageStar", "DaddyGuide", "PopstarRoshan",
		"TimingZone", "VisualPointer",
	]
	for index in range(7):
		expected.append("RainbowNote%d" % index)
		expected.append("ProgressPip%d" % index)
	if surface.get_child_count() != expected.size():
		return false
	for index in range(expected.size()):
		var child: Node = surface.get_child(index)
		if String(child.name) != expected[index] or not (child is CanvasItem):
			return false
	var fill: Node = surface.find_child("OpaqueTheaterFill", true, false)
	var scenic: Node = surface.find_child("ScenicBackcloth", true, false)
	var proscenium: Node = surface.find_child("OperaProscenium", true, false)
	var footlights: Node = surface.find_child("StageFootlights", true, false)
	var star: Node = surface.find_child("StageStar", true, false)
	var daddy: Node = surface.find_child("DaddyGuide", true, false)
	var roshan: Node = surface.find_child("PopstarRoshan", true, false)
	var zone: Node = surface.find_child("TimingZone", true, false)
	var pointer: Node = surface.find_child("VisualPointer", true, false)
	var first_tile: Node = surface.find_child(MELODY_TILE_NODES[0], true, false)
	if not (fill is ColorRect) or not (scenic is ColorRect) \
			or not (proscenium is Control) or not (footlights is Control) \
			or not (star is Control) or not (zone is Control) \
			or not (pointer is Control) \
			or not _melody_actor_exact(daddy, surface, MELODY_DADDY_PATH) \
			or not _melody_actor_exact(roshan, surface, MELODY_ROSHAN_PATH):
		return false
	var ordered_z: bool = _melody_effective_z(fill) < _melody_effective_z(scenic) \
		and _melody_effective_z(scenic) < _melody_effective_z(first_tile) \
		and _melody_effective_z(first_tile) < _melody_effective_z(proscenium) \
		and _melody_effective_z(proscenium) < _melody_effective_z(footlights) \
		and _melody_effective_z(footlights) < _melody_effective_z(star) \
		and _melody_effective_z(star) < _melody_effective_z(daddy) \
		and _melody_effective_z(star) < _melody_effective_z(roshan) \
		and _melody_effective_z(daddy) < _melody_effective_z(zone) \
		and _melody_effective_z(roshan) < _melody_effective_z(zone) \
		and _melody_effective_z(zone) < _melody_effective_z(pointer)
	for index in range(7):
		var note: Node = surface.find_child("RainbowNote%d" % index, true, false)
		var pip: Node = surface.find_child("ProgressPip%d" % index, true, false)
		ordered_z = ordered_z and note is Control and pip is Control \
			and _melody_effective_z(pointer) <= _melody_effective_z(note) \
			and _melody_effective_z(note) < _melody_effective_z(pip)
	return ordered_z


func _melody_actor_exact(actor: Node, surface: Node,
		expected_path: String) -> bool:
	if not (actor is Sprite2D) or actor.get_parent() != surface:
		return false
	var sprite := actor as Sprite2D
	var texture: Texture2D = sprite.texture
	return texture != null and not (texture is AtlasTexture) \
		and texture.resource_path == expected_path \
		and String(sprite.get_meta("source_path", "")) == expected_path \
		and sprite.get_child_count() == 0 \
		and sprite.centered and not sprite.region_enabled \
		and not sprite.flip_h and not sprite.flip_v \
		and sprite.hframes == 1 and sprite.vframes == 1 and sprite.frame == 0 \
		and sprite.offset.is_zero_approx() \
		and sprite.scale.x > 0.0 and sprite.scale.y > 0.0 \
		and is_zero_approx(sprite.rotation) and is_zero_approx(sprite.skew)


func _melody_effective_z(node: Node) -> int:
	if not (node is CanvasItem):
		return -4096
	var total := 0
	var current: Node = node
	while current is CanvasItem:
		var item := current as CanvasItem
		total += item.z_index
		if not item.z_as_relative:
			break
		current = current.get_parent()
	return total


func _melody_tile_bindings_exact(surface: Node) -> bool:
	if surface == null:
		return false
	var scenic: Node = surface.find_child("ScenicBackcloth", true, false)
	if not (scenic is Control) or not (scenic as Control).clip_contents:
		return false
	var instance_ids: Dictionary = {}
	var rects: Array[Rect2] = []
	var common_scale := Vector2.ZERO
	for index in range(MELODY_TILE_NODES.size()):
		var node: Node = surface.find_child(MELODY_TILE_NODES[index], true, false)
		if not (node is Sprite2D) or node.get_parent() != scenic \
				or _melody_named_count(surface, MELODY_TILE_NODES[index]) != 1:
			return false
		var sprite := node as Sprite2D
		var texture: Texture2D = sprite.texture
		if texture == null or texture.resource_path != MELODY_TILE_PATHS[index] \
				or texture is AtlasTexture \
				or texture.get_size() != Vector2(1024, 1024) \
				or String(sprite.get_meta("source_path", "")) \
					!= MELODY_TILE_PATHS[index] \
				or sprite.get_meta("native_source_rect", Rect2i()) \
					!= MELODY_TILE_SOURCE_RECTS[index] \
				or sprite.get_child_count() != 0 \
				or not sprite.centered or sprite.flip_h or sprite.flip_v \
				or sprite.region_enabled or sprite.hframes != 1 or sprite.vframes != 1 \
				or sprite.frame != 0 or not sprite.offset.is_zero_approx() \
				or sprite.scale.x <= 0.0 or sprite.scale.y <= 0.0 \
				or not is_equal_approx(sprite.scale.x, sprite.scale.y) \
				or not is_zero_approx(sprite.rotation) \
				or not is_zero_approx(sprite.skew):
			return false
		if index == 0:
			common_scale = sprite.scale
		elif not sprite.scale.is_equal_approx(common_scale):
			return false
		rects.append(_melody_transform_rect(sprite.get_rect(),
			sprite.get_global_transform_with_canvas()))
		instance_ids[node.get_instance_id()] = true
	var tolerance := 1.5
	var union_rect: Rect2 = rects[0]
	for index in range(1, rects.size()):
		union_rect = union_rect.merge(rects[index])
	var scenic_rect: Rect2 = (scenic as Control).get_global_rect()
	return instance_ids.size() == MELODY_TILE_PATHS.size() \
		and rects.all(func(rect: Rect2) -> bool:
			return rect.has_area() and rect.size.is_equal_approx(rects[0].size)) \
		and absf(rects[0].size.x - rects[0].size.y) <= tolerance \
		and absf(rects[0].end.x - rects[1].position.x) <= tolerance \
		and absf(rects[2].end.x - rects[3].position.x) <= tolerance \
		and absf(rects[0].end.y - rects[2].position.y) <= tolerance \
		and absf(rects[1].end.y - rects[3].position.y) <= tolerance \
		and absf(union_rect.size.x - union_rect.size.y) <= tolerance \
		and union_rect.grow(tolerance).encloses(scenic_rect) \
		and union_rect.get_center().distance_to(scenic_rect.get_center()) <= tolerance


func _melody_transform_rect(rect: Rect2, xform: Transform2D) -> Rect2:
	var points := PackedVector2Array([
		xform * rect.position,
		xform * Vector2(rect.end.x, rect.position.y),
		xform * rect.end,
		xform * Vector2(rect.position.x, rect.end.y),
	])
	var min_point: Vector2 = points[0]
	var max_point: Vector2 = points[0]
	for point: Vector2 in points:
		min_point.x = minf(min_point.x, point.x)
		min_point.y = minf(min_point.y, point.y)
		max_point.x = maxf(max_point.x, point.x)
		max_point.y = maxf(max_point.y, point.y)
	return Rect2(min_point, max_point - min_point)


func _melody_named_count(node: Node, exact_name: String) -> int:
	if node == null:
		return 0
	var count := 1 if String(node.name) == exact_name else 0
	for child_value: Variant in node.get_children():
		count += _melody_named_count(child_value as Node, exact_name)
	return count


func _melody_spatial_descendant_count(node: Node) -> int:
	if node == null:
		return 0
	var total := 0
	for child_value: Variant in node.get_children():
		var child := child_value as Node
		if child is Node3D:
			total += 1
		total += _melody_spatial_descendant_count(child)
	return total
