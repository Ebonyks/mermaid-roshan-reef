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

const SLIDE_VIEW_SIZE := Vector2i(1280, 720)
const SLIDE_TALL_SIZE := Vector2i(1280, 800)
const SLIDE_TOUCH_INDEX := 91
const SLIDE_OBJECTIVE := "Come slide with us! Grab the fishies!"
const SLIDE_RETURN_AXIS_VALUES: Array[float] = [0.61, 0.72, -0.63, -0.74]
const SLIDE_MASTER_PATH := \
	"res://assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png"
const SLIDE_MASTER_SHA256 := \
	"017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41"
const SLIDE_TILE_PATHS: Array[String] = [
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c3.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c2.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c3.png",
]
const SLIDE_TILE_NAMES: Array[String] = [
	"SkyLagoonBackdrop_r0_c2", "SkyLagoonBackdrop_r0_c3",
	"SkyLagoonBackdrop_r1_c2", "SkyLagoonBackdrop_r1_c3",
]
const SLIDE_TILE_RECTS: Array[Rect2i] = [
	Rect2i(0, 0, 1024, 1024), Rect2i(1024, 0, 1024, 1024),
	Rect2i(0, 1024, 1024, 1024), Rect2i(1024, 1024, 1024, 1024),
]
const SLIDE_TILE_SHA256: Array[String] = [
	"a5e0dc1e71031ade14059722885bf7905d88f3ea45e9b04e5994cb09ece88850",
	"b423c7c320377e15a38d684d4cec4499c81fa9a31e20bdf4d7dbf051d63c1959",
	"2c095349af8d05bb11e43f2115406ce55f583eb885f2abf5b7b4faf7cb8b1e28",
	"1f84c75cdfc85923b2a18011e50ac60e78145ed6a9703f7c99ae26592bb6edb7",
]
const SLIDE_ACTOR_PATHS: Array[String] = [
	"res://assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png",
	"res://assets/characters/friends/two_friends.png",
	"res://assets/props/gen2/clownfish_side.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_0.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_1.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_2_v2.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_3_v2.png",
]
const SLIDE_ACTOR_SHA256: Array[String] = [
	"3b917608d9e3067d9fe68bbd260eba045acc0a15074795f4649f40ee0c69a3e4",
	"85f2cc1bc7247d0877ff7bb6a97a44b711c757c497d36c215bc70fb74e548f58",
	"0b9df739ab132f88178f1ac2052a3b8a4a7c9497ba1456eb151c8849989cba88",
	"023a1bfefb4393c6d9f7373f29f337b7fff0a83049e81c71a73aecc233f14bf3",
	"9011deb46e28fdcc533bb6482510902f651ecce723e86c6b985bd255a1cb4e62",
	"cb6cd27d5357bb59542bbdf95ef3fbf751759ce07046ea3607ec449c6a5d9613",
	"8ec11afaf899b21548e4fdeeabc945cb90f5b62e6410a6319afaf22834e03271",
]
const SLIDE_ACTOR_SIZES: Array[Vector2i] = [
	Vector2i(425, 412), Vector2i(480, 460), Vector2i(256, 256),
	Vector2i(512, 512), Vector2i(512, 512), Vector2i(512, 512),
	Vector2i(512, 512),
]

var slide_bad := 0
var slide_alpha_cache: Dictionary = {}


class SlideReturnGuardObserver extends Node:
	var main_ref: Node
	var player_ref: Node
	var samples: Array[Dictionary] = []


	func _process(_delta: float) -> void:
		if main_ref == null or player_ref == null \
				or not main_ref.has_method(&"_slide_canvas_return_guard_snapshot"):
			return
		var guard: Dictionary = main_ref.call(
			"_slide_canvas_return_guard_snapshot") as Dictionary
		samples.append({
			"guard": guard.duplicate(true),
			# Reuse the probe's already-inventoried player seam without adding a
			# second spatial type marker solely for this late-process observer.
			"position": player_ref.get(&"position"),
			"rotation": player_ref.get(&"rotation"),
			"vel": player_ref.get("vel"),
		})
		if samples.size() > 240:
			samples.pop_front()

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
	await _audit_slide_canvas()
	print("AUDIT|Harper/Fiona Canvas trusted suite: ",
		"OK" if slide_bad == 0 else "FAIL (%d checks)" % slide_bad)
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
		var canvas_cutaway: bool = gname == "melody" \
			or (gname == "slide" and String(main.g.get("mode", "")) == "fish")
		var cutaway_ok: bool = player.position == friend_route_position \
			and main.we_node.environment == friend_route_environment \
			if canvas_cutaway else \
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
				and melody.progress_count() == 0 \
				and (melody.audit_snapshot().get(
					"blocked_sources", {}) as Dictionary).is_empty()
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


func _audit_slide_canvas() -> void:
	_slide_check_assets()
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = SLIDE_VIEW_SIZE
	await _frames(3)

	var route: Dictionary = _slide_friend_route()
	var friend: Dictionary = route.get("friend", {}) as Dictionary
	var friend_index: int = int(route.get("index", -1))
	_slide_check("one Harper/Fiona fish route is present and initially unawarded",
		friend_index >= 0 and not friend.is_empty()
		and String(friend.get("fname", "")) == "Harper and Fiona"
		and not bool(friend.get("won", false))
		and int(main.medals.get("slide", 0)) == 0)
	if friend.is_empty():
		main._set_touch_mode(main.TOUCH_MODE_CLASSIC, false)
		return

	# Enter through the child's actual two-tap Hybrid friend route. Discovery
	# may persist its one found flag; flush that before the neutral-leave
	# fingerprint so the lifecycle check isolates the activity itself.
	main._set_touch_mode(main.TOUCH_MODE_HYBRID, false)
	var friend_node: Variant = friend.get("node")
	player.position = friend_node.position
	player.position.x += 3.0
	player.vel *= 0.0
	await _frames(10)
	_slide_check("Hybrid proximity discovers Harper and Fiona without launching",
		bool(friend.get("found", false)) and main.game == "")
	main._populate_touch_interactables()
	var target: Dictionary = _slide_touch_target("friend:%d" % friend_index)
	_slide_check("Hybrid exposes the visible child-facing PLAY target",
		not target.is_empty() and String(target.get("label", "")) \
			== "Harper and Fiona" and String(target.get("verb", "")) == "PLAY")
	var camera: Variant = player.cam
	var friend_point := Vector2(-1.0, -1.0)
	if camera != null:
		friend_point = camera.unproject_position(friend_node.global_position)
	_slide_push_touch(friend_point, true, SLIDE_TOUCH_INDEX)
	_slide_push_touch(friend_point, false, SLIDE_TOUCH_INDEX)
	await process_frame
	_slide_check("first real Hybrid tap focuses PLAY without launching",
		friend_point.x >= 0.0 and friend_point.y >= 0.0
		and main.touch_focus_id == "friend:%d" % friend_index
		and main.touch_focus_ready and main.game == "")
	_slide_parse_mouse_button(Vector2(640.0, 360.0), MOUSE_BUTTON_RIGHT,
		true, 58)
	_slide_push_mouse_look(Vector2(-78.0, 44.0), 58)
	await process_frame
	await process_frame
	_slide_parse_mouse_button(Vector2(640.0, 360.0), MOUSE_BUTTON_RIGHT,
		false, 58)
	if camera != null:
		friend_point = camera.unproject_position(friend_node.global_position)
	var route_camera: Dictionary = _slide_camera_snapshot()
	_slide_check("real nondefault camera peek is live before fish entry",
		absf(float(route_camera.get("orbit", 0.0))) > 0.10
		and absf(float(route_camera.get("pitch", 0.0))) > 0.20
		and bool(route_camera.get("current", false))
		and bool(route_camera.get("active", false)))
	main._write_save()
	var neutral_generation: int = main.save_generation
	var neutral_fingerprint: String = _slide_save_fingerprint()
	var neutral_progress: Dictionary = _slide_progress_snapshot(friend)
	var route_position: Variant = player.position
	var route_rotation: Variant = player.rotation
	var route_environment: Variant = main.we_node.environment
	var route_track: String = main.cur_track
	var route_music: Dictionary = _slide_music_context()
	var reef_chime_before: Dictionary = _slide_chime_context()
	_slide_set_chime(-9.25, 0.73)
	var neutral_entry_chime: Dictionary = _slide_chime_context()
	_slide_check("neutral fixture starts from an exact nondefault chime context",
		main.chime != null
		and is_equal_approx(float(neutral_entry_chime.get(
			"volume_db", 0.0)), -9.25)
		and is_equal_approx(float(neutral_entry_chime.get(
			"pitch_scale", 0.0)), 0.73))
	var route_living_live_before: Dictionary = _slide_living_world_snapshot()
	_slide_check("living-world layer is genuinely live before fish entry",
		bool(route_living_live_before.get("layer_visible", false))
		and main.living_layer != null and main.living_layer.visible)
	var direct_before: Dictionary = _slide_direct_child_ids()
	var neutral_collection_visible: bool = main.collection_button_layer != null \
		and main.collection_button_layer.visible
	_slide_check("Critter Book corner is genuinely visible before fish entry",
		neutral_collection_visible and main.collection_button != null
		and main.collection_button.is_visible_in_tree())
	var neutral_joy_unmapped_before: bool = main.joy_has_unmapped
	_slide_check("unmapped axis and d-pad fallback is genuinely live before Canvas entry",
		_slide_seed_unmapped_pad(60, 0.82, JOY_BUTTON_DPAD_LEFT))
	# The deliberate pre-entry pad events above are real Reef input and therefore
	# legitimately reset LivingWorld idle/event bytes. Snapshot the exact state
	# the Canvas entry is about to hide, after that input has been observed.
	var route_living_before: Dictionary = _slide_living_world_snapshot()

	_slide_push_touch(friend_point, true, SLIDE_TOUCH_INDEX + 1)
	_slide_push_touch(friend_point, false, SLIDE_TOUCH_INDEX + 1)
	var slide := main._game_obj("race", SlideRaceGame) as SlideRaceGame
	var layer: CanvasLayer = slide.active_layer()
	var layer_ref: WeakRef = weakref(layer)
	_slide_check("second real Hybrid tap synchronously enters only fish Canvas",
		main.game == "slide" and String(main.g.get("mode", "")) == "fish"
		and layer != null and slide.stage_root() != null
		and player.position.is_equal_approx(route_position)
		and player.rotation.is_equal_approx(route_rotation)
		and main.we_node.environment == route_environment
		and not player.visible and not main.touch_ui.world_controls_enabled)
	_slide_push_axis(0.0, 60)
	_slide_push_pad(JOY_BUTTON_DPAD_LEFT, false, 60)
	_slide_check("fish entry and real terminal pad events retire every raw fallback",
		_slide_raw_pad_values_neutral(JOY_BUTTON_DPAD_LEFT)
		and not main._slide_canvas_held_sources.has(
			StringName("pad:60:%d" % JOY_BUTTON_DPAD_LEFT))
		and not main._slide_canvas_held_sources.has(
			StringName("pad:60:axis:%d" % JOY_AXIS_LEFT_X)))
	_slide_check_entry_contract(
		slide, direct_before, route_camera, route_living_before)
	_slide_check("opening black cover owns the exact 1280x720 viewport above fish Canvas",
		_slide_fade_cover_contract(slide, SLIDE_VIEW_SIZE, true))
	_slide_check("controller exposes the exact completion-reward chime handoff seam",
		slide.has_method(&"handoff_fish_chime_to_completion_reward"))
	var living_world_before_traffic: Dictionary = _slide_living_world_snapshot()
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, 0.76, 62)
	_slide_push_pad(JOY_BUTTON_A, true, 62)
	_slide_check("live fish Canvas can hold unclaimed real raw RIGHT_X and A fallback",
		_slide_unclaimed_raw_pad_live(0.76))
	var opening_context: Dictionary = _slide_begin_opening_context_cross_product(
		slide)

	# A complete gesture under black is swallowed. Readiness belongs to the
	# actual fade callback, which restores both transparency and input filtering.
	var fade_progress: int = slide.progress_count()
	_slide_push_touch(Vector2(180.0, 430.0), true, SLIDE_TOUCH_INDEX + 2, 2)
	_slide_push_touch(Vector2(180.0, 430.0), false, SLIDE_TOUCH_INDEX + 2, 2)
	await process_frame
	_slide_check("opening black cover swallows a complete touch neutrally",
		main.fade_rect != null and main.fade_rect.mouse_filter \
			== Control.MOUSE_FILTER_STOP
		and slide.progress_count() == fade_progress
		and (slide.audit_snapshot().get("input_sources", {}) as Dictionary).is_empty())
	await _slide_finish_opening_context_cross_product(slide, opening_context)
	await _slide_wait_until_ready(slide)
	_slide_check("startup becomes ready only after the fade callback boundary",
		main.fade_rect == null or (main.fade_rect.modulate.a <= 0.02
		and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE))
	_slide_check("revealed cover remains full-viewport and input-transparent at 1280x720",
		_slide_fade_cover_contract(slide, SLIDE_VIEW_SIZE, false))
	_slide_check("return poll vocabulary owns Enter, keypad Enter, X, and Y",
		_slide_return_poll_vocabulary_contract())
	_slide_check("first live fish Canvas frame disables hidden 3D camera rendering",
		main.active_viewport_camera() == null)

	await _slide_check_layouts(slide)
	await _slide_exercise_context_resize(slide, friend)
	await _slide_check_tick_once(slide)
	await _slide_exercise_dual_steer_cues(slide)
	await _slide_exercise_source_ownership(slide)
	await _slide_exercise_pause_and_overlay(slide, friend)
	await _slide_exercise_system_context(slide)
	_slide_check("claimed, unclaimed, Pause, overlay, and OS traffic preserve living-world bytes",
		_slide_living_world_snapshot() == living_world_before_traffic)
	_slide_reset_run_state()
	# Context-loss checks above deliberately clear raw fallback state. Re-arm an
	# unclaimed axis + face button immediately before the neutral exit so this
	# assertion proves teardown itself owns the cleanup at the synchronous seam.
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, 0.73, 64)
	_slide_push_pad(JOY_BUTTON_A, true, 64)
	_slide_check("neutral-exit fixture holds unclaimed raw RIGHT_X and A until teardown",
		_slide_unclaimed_raw_pad_live(0.73))
	# Make teardown's restoration observable rather than passing because no game
	# code happened to retune the shared player on this neutral route.
	_slide_set_chime(-1.75, 1.67)

	# Leave through the real pause sheet and focused BACK control. Detachment is
	# synchronous; queued deletion may finish on the following frames.
	await _slide_open_pause(SLIDE_TOUCH_INDEX + 30)
	_slide_check("real pause sheet exposes a neutral visible BACK control",
		paused and main.pause_panel.visible and main.pause_leave_btn.visible
		and bool(main.pause_leave_btn.get_meta("neutral_exit", false)))
	main.pause_leave_btn.grab_focus()
	_slide_push_action(&"ui_accept", true)
	_slide_push_action(&"ui_accept", false)
	var neutral_guard_sync: Dictionary = main.call(
		"_slide_canvas_return_guard_snapshot") as Dictionary
	var neutral_raw_return: bool = main.game == "" \
		and bool(neutral_guard_sync.get("active", false)) \
		and bool(neutral_guard_sync.get("control_blocked", false)) \
		and is_equal_approx(main.joy_axis(JOY_AXIS_RIGHT_X), 0.73) \
		and main.joy_pressed(JOY_BUTTON_A) \
		and not main.touch_ui.world_controls_enabled
	var neutral_collection_return: bool = main.game == "" \
		and main.collection_button_layer != null \
		and main.collection_button != null \
		and main.collection_button_layer.visible == neutral_collection_visible \
		and main.collection_button.is_visible_in_tree() \
			== neutral_collection_visible
	var neutral_camera_return: bool = main.game == "" \
		and _slide_camera_matches(route_camera, true)
	var neutral_living_return: bool = main.game == "" \
		and _slide_living_world_snapshot() == route_living_before
	var neutral_chime_return: bool = main.game == "" \
		and _slide_chime_matches(neutral_entry_chime)
	_slide_check("focused real BACK synchronously restores the exact Reef context",
		main.game == "" and main.g.is_empty() and slide.active_layer() == null
		and slide.stage_root() == null and player.visible
		and not main.touch_ui.world_controls_enabled
		and player.position.is_equal_approx(route_position)
		and player.rotation.is_equal_approx(route_rotation)
		and main.we_node.environment == route_environment
		and main.cur_track == route_track
		and _slide_music_matches(route_music)
		and _slide_camera_matches(route_camera, true))
	_slide_check("neutral BACK changes no reward bytes and preserves held raw levels under guard",
		_slide_progress_snapshot(friend) == neutral_progress
		and main.save_generation == neutral_generation + 1
		and _slide_save_fingerprint() == neutral_fingerprint
		and neutral_raw_return
		and neutral_collection_return
		and neutral_camera_return
		and neutral_living_return
		and neutral_chime_return
		and main.collection_button_layer != null
		and main.collection_button_layer.visible == neutral_collection_visible
		and main.collection_button != null
		and main.collection_button.is_visible_in_tree())
	_slide_check("neutral stage_close exact-restores pre-entry chime volume and pitch",
		neutral_chime_return)
	var neutral_return_guard: Dictionary = await _slide_exercise_return_guard(
		friend, "neutral Leave", false, Vector2(310.0, 510.0),
		SLIDE_TOUCH_INDEX + 400, 64, 64, false,
		{},
		neutral_joy_unmapped_before)
	await _frames(2)
	_slide_check("fish Canvas teardown is synchronous, idempotent, and fully freed",
		slide.active_layer() == null and slide.audit_snapshot().is_empty()
		and layer_ref.get_ref() == null
		and bool(neutral_return_guard.get("exact", false))
		and bool(neutral_return_guard.get("raw_neutral", false))
		and main.touch_ui.world_controls_enabled)
	_slide_check("Hybrid touch and native mouse stick/action releases retire both entry censuses",
		_slide_consumed_entry_release_contract())
	_slide_restore_chime_context(reef_chime_before)

	# Classic's real linger route starts the same exact fish activity without a
	# second-tap affordance. The first deliberate run collects all five.
	await _slide_wait_return_guard_clear("Classic first-win reentry")
	main._set_touch_mode(main.TOUCH_MODE_CLASSIC, false)
	friend["cool"] = 0.0
	player.position = friend_node.position
	player.position.x += 3.0
	player.vel *= 0.0
	route_position = player.position
	route_rotation = player.rotation
	route_environment = main.we_node.environment
	route_track = main.cur_track
	route_music = _slide_music_context()
	route_camera = _slide_camera_snapshot()
	var first_generation: int = main.save_generation
	var first_trophies: int = main.trophies
	var first_collection_visible: bool = main.collection_button_layer != null \
		and main.collection_button_layer.visible
	var first_joy_unmapped_before: bool = main.joy_has_unmapped
	_slide_check("gold-run unmapped pad fallback is live before exact fish entry",
		_slide_seed_unmapped_pad(61, -0.84, JOY_BUTTON_DPAD_RIGHT))
	var classic_guard := 0
	while main.game == "" and classic_guard < 180:
		classic_guard += 1
		await process_frame
	_slide_check("Classic proximity enters the same exact fish Canvas route",
		main.game == "slide" and String(main.g.get("mode", "")) == "fish"
		and slide.active_layer() != null
		and first_collection_visible and _slide_collection_suppressed())
	var first_living_expected: Dictionary = _slide_living_world_snapshot()
	first_living_expected["layer_visible"] = bool(
		main.g.get("slide_canvas_living_was_visible", false))
	_slide_check("Classic entry hides the exact captured living-world layer",
		_slide_living_hidden_matches(first_living_expected))
	_slide_push_axis(0.0, 61)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, false, 61)
	_slide_check("gold entry terminal pad events stay Canvas-owned and raw-neutral",
		_slide_raw_pad_values_neutral(JOY_BUTTON_DPAD_RIGHT))
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, -0.78, 63)
	_slide_push_pad(JOY_BUTTON_A, true, 63)
	_slide_check("gold run holds real unclaimed raw fallback until exact teardown",
		_slide_unclaimed_raw_pad_live(-0.78))
	var sticker_freeze: Dictionary = await _slide_exercise_sticker_freeze(
		slide, friend)
	var first_run: Dictionary = await _slide_drive_run(
		slide, 5, first_living_expected, friend)
	var first_fingerprint: String = _slide_save_fingerprint()
	var first_star: Variant = friend.get("star")
	_slide_check("post-overlay deliberate Classic steering collects five and wins gold",
		bool(sticker_freeze.get("ready_for_completion", false))
		and int(first_run.get("start_layer_id", 0)) \
			== int(sticker_freeze.get("layer_id", -1))
		and int(first_run.get("start_surface_id", 0)) \
			== int(sticker_freeze.get("surface_id", -1))
		and int(first_run.get("got", -1)) == 5
		and int(first_run.get("tier", 0)) == MedalSystem.GOLD
		and bool(first_run.get("collection_hidden_during_run", false))
		and bool(first_run.get("living_hidden_during_run", false))
		and bool(first_run.get("context_hold_exact", false))
		and bool(first_run.get("fresh_after_context_hold", false))
		and bool(first_run.get("return_guard_exact", false))
		and bool(first_run.get("return_pose_armed_sync", false))
		and bool(first_run.get("return_pose_lock_tested_if_live", false))
		and main.game == "" and bool(friend.get("won", false))
		and main.trophies == first_trophies + 1
		and int(main.medals.get("slide", 0)) == MedalSystem.GOLD
		and bool(first_run.get("raw_neutral_on_exit", false))
		and bool(first_run.get("collection_restored_on_exit", false))
		and bool(first_run.get("living_restored_on_exit", false))
		and main.collection_button_layer.visible == first_collection_visible
		and main.collection_button.is_visible_in_tree()
		and _slide_raw_pad_neutral(JOY_BUTTON_DPAD_RIGHT))
	main.joy_has_unmapped = first_joy_unmapped_before
	_slide_check("first win persists medal and friend exactly once per write owner",
		main.save_generation == first_generation + 2
		and not first_fingerprint.is_empty()
		and _slide_saved_medal() == MedalSystem.GOLD
		and _slide_saved_friend_won())
	_slide_check("first-win teardown hands chime to the 0.90 fanfare instead of restoring entry tuning",
		_slide_chime_snapshot_matches(first_run.get(
			"chime_on_synchronous_exit", {}) as Dictionary, -4.0, 0.90))
	_slide_check("first win restores position, pose, environment, and music",
		player.position.is_equal_approx(route_position)
		and player.rotation.is_equal_approx(route_rotation)
		and main.we_node.environment == route_environment
		and main.cur_track == route_track
		and _slide_music_matches(route_music)
		and _slide_camera_matches(route_camera, true))

	# A real replay deliberately collects three. It earns silver for this run,
	# keeps the best gold, adds no trophy/star, and rewrites identical save bytes.
	await _frames(4)
	await _slide_wait_return_guard_clear("three-fish replay reentry")
	var post_first_win_chime: Dictionary = _slide_chime_context()
	_slide_set_chime(-12.25, 0.61)
	var replay_entry_chime: Dictionary = _slide_chime_context()
	_slide_check("already-won replay enters from deliberately nondefault chime tuning",
		_slide_chime_snapshot_matches(replay_entry_chime, -12.25, 0.61))
	friend["cool"] = 0.0
	player.position = friend_node.position
	player.position.x += 3.0
	player.vel *= 0.0
	route_position = player.position
	route_rotation = player.rotation
	route_environment = main.we_node.environment
	route_track = main.cur_track
	route_music = _slide_music_context()
	route_camera = _slide_camera_snapshot()
	var replay_generation: int = main.save_generation
	var replay_trophies: int = main.trophies
	classic_guard = 0
	while main.game == "" and classic_guard < 180:
		classic_guard += 1
		await process_frame
	var replay_living_expected: Dictionary = _slide_living_world_snapshot()
	replay_living_expected["layer_visible"] = bool(
		main.g.get("slide_canvas_living_was_visible", false))
	var replay_run: Dictionary = await _slide_drive_run(
		slide, 3, replay_living_expected, friend)
	_slide_check("deliberate three-fish replay earns silver without downgrading gold",
		int(replay_run.get("got", -1)) == 3
		and int(replay_run.get("tier", 0)) == MedalSystem.SILVER
		and int(main.medals.get("slide", 0)) == MedalSystem.GOLD
		and main.trophies == replay_trophies
		and friend.get("star") == first_star
		and bool(replay_run.get("return_guard_exact", false)))
	_slide_check("silver replay handoff survives synchronous stage_close and its next frame",
		_slide_chime_snapshot_matches(replay_run.get(
			"chime_on_synchronous_exit", {}) as Dictionary, -4.0, 1.30)
		and _slide_chime_snapshot_matches(replay_run.get(
			"chime_after_next_frame", {}) as Dictionary, -4.0, 1.30))
	_slide_check("replay writes once, preserves exact save bytes, and restores context",
		main.save_generation == replay_generation + 1
		and _slide_save_fingerprint() == first_fingerprint
		and bool(replay_run.get("living_hidden_during_run", false))
		and bool(replay_run.get("living_restored_on_exit", false))
		and player.position.is_equal_approx(route_position)
		and player.rotation.is_equal_approx(route_rotation)
		and main.we_node.environment == route_environment
		and main.cur_track == route_track
		and _slide_music_matches(route_music)
		and _slide_camera_matches(route_camera, true))
	await _frames(3)
	_slide_check("silver celebration volume and pitch remain live across following frames",
		_slide_chime_snapshot_matches(_slide_chime_context(), -4.0, 1.30))
	_slide_restore_chime_context(post_first_win_chime)

	# Zero fish is still a successful, child-safe ride when the child deliberately
	# leans away from every collectible. It earns bronze with no loss branch.
	await _frames(4)
	await _slide_wait_return_guard_clear("zero-fish mercy reentry")
	_slide_set_chime(-10.75, 0.67)
	var zero_entry_chime: Dictionary = _slide_chime_context()
	_slide_check("zero-fish replay also enters from nondefault chime tuning",
		_slide_chime_snapshot_matches(zero_entry_chime, -10.75, 0.67))
	friend["cool"] = 0.0
	player.position = friend_node.position
	player.position.x += 3.0
	player.vel *= 0.0
	route_position = player.position
	route_rotation = player.rotation
	route_environment = main.we_node.environment
	route_track = main.cur_track
	route_music = _slide_music_context()
	route_camera = _slide_camera_snapshot()
	var zero_generation: int = main.save_generation
	var zero_trophies: int = main.trophies
	var zero_star: Variant = friend.get("star")
	classic_guard = 0
	while main.game == "" and classic_guard < 180:
		classic_guard += 1
		await process_frame
	var zero_living_expected: Dictionary = _slide_living_world_snapshot()
	zero_living_expected["layer_visible"] = bool(
		main.g.get("slide_canvas_living_was_visible", false))
	var zero_run: Dictionary = await _slide_drive_run(
		slide, 0, zero_living_expected, friend)
	_slide_check("deliberate zero-fish mercy ride completes successfully for bronze",
		int(zero_run.get("got", -1)) == 0
		and int(zero_run.get("tier", 0)) == MedalSystem.BRONZE
		and bool(zero_run.get("mercy", false))
		and main.game == "" and bool(friend.get("won", false))
		and int(main.medals.get("slide", 0)) == MedalSystem.GOLD
		and main.trophies == zero_trophies
		and friend.get("star") == zero_star
		and bool(zero_run.get("return_guard_exact", false)))
	_slide_check("bronze replay handoff survives synchronous stage_close and its next frame",
		_slide_chime_snapshot_matches(zero_run.get(
			"chime_on_synchronous_exit", {}) as Dictionary, -4.0, 1.15)
		and _slide_chime_snapshot_matches(zero_run.get(
			"chime_after_next_frame", {}) as Dictionary, -4.0, 1.15))
	_slide_check("zero-fish replay has no fail/timer path and preserves save/context",
		main.save_generation == zero_generation + 1
		and _slide_save_fingerprint() == first_fingerprint
		and bool(zero_run.get("living_hidden_during_run", false))
		and bool(zero_run.get("living_restored_on_exit", false))
		and player.position.is_equal_approx(route_position)
		and player.rotation.is_equal_approx(route_rotation)
		and main.we_node.environment == route_environment
		and main.cur_track == route_track
		and _slide_music_matches(route_music)
		and _slide_camera_matches(route_camera, true))
	_slide_check("slide medal thresholds remain exact at zero, three, and five fish",
		main._medal_ref().evaluate("slide", {"got": 0}) == MedalSystem.BRONZE
		and main._medal_ref().evaluate("slide", {"got": 3}) == MedalSystem.SILVER
		and main._medal_ref().evaluate("slide", {"got": 5}) == MedalSystem.GOLD)

	await _slide_wait_return_guard_clear("Penguin and race regressions")
	await _slide_check_route_regressions(slide)
	main._set_touch_mode(main.TOUCH_MODE_CLASSIC, false)
	get_root().size = SLIDE_VIEW_SIZE
	await _frames(3)


func _slide_check(label: String, ok: bool) -> void:
	print("AUDIT|Slide Canvas|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		slide_bad += 1


func _slide_check_assets() -> void:
	var master := Image.load_from_file(SLIDE_MASTER_PATH)
	_slide_check("approved panorama master remains exact 6144x2048 source",
		master != null and master.get_size() == Vector2i(6144, 2048)
		and FileAccess.get_sha256(SLIDE_MASTER_PATH) == SLIDE_MASTER_SHA256)
	var tiles_exact: bool = master != null
	for index in range(SLIDE_TILE_PATHS.size()):
		var path: String = SLIDE_TILE_PATHS[index]
		var tile := Image.load_from_file(path)
		var row: int = index / 2
		var column: int = 2 + index % 2
		var crop := master.get_region(Rect2i(
			column * 1024, row * 1024, 1024, 1024)) if master != null else null
		tiles_exact = tiles_exact and tile != null and crop != null \
			and tile.get_size() == Vector2i(1024, 1024) \
			and FileAccess.get_sha256(path) == SLIDE_TILE_SHA256[index] \
			and tile.get_format() == crop.get_format() \
			and tile.get_data() == crop.get_data()
	_slide_check("four lossless center tiles pixel-reconstruct one native screen",
		tiles_exact)
	var actors_exact := true
	for index in range(SLIDE_ACTOR_PATHS.size()):
		var path: String = SLIDE_ACTOR_PATHS[index]
		var image := Image.load_from_file(path)
		actors_exact = actors_exact and image != null \
			and image.get_size() == SLIDE_ACTOR_SIZES[index] \
			and image.get_used_rect().has_area() \
			and FileAccess.get_sha256(path) == SLIDE_ACTOR_SHA256[index]
	_slide_check("slide, protected friends, fish, and four Roshan frames are immutable",
		actors_exact)
	var expected_runtime: Array[String] = SLIDE_TILE_PATHS.duplicate()
	expected_runtime.append_array(SLIDE_ACTOR_PATHS)
	_slide_check("controller runtime census names only the approved reused art",
		SlideRaceGame.canvas_runtime_art_paths() == expected_runtime)
	var licenses := FileAccess.get_file_as_string("res://ASSET_LICENSES.md")
	_slide_check("all reused art families retain repository provenance",
		licenses.contains("assets/characters/friends/*")
		and licenses.contains("sky_lagoon_panorama_master_v5_hd_3x1.png")
		and licenses.contains(
			"flat_sky_lagoon_main_panorama_v5_tile_r{0..1}_c{0..5}.png")
		and licenses.contains("sky_lagoon_slide_v3_compact.png")
		and licenses.contains("clownfish_side.png")
		and licenses.contains("roshan_slide_0.png")
		and licenses.contains("roshan_slide_1.png")
		and licenses.contains("roshan_slide_2_v2.png")
		and licenses.contains("roshan_slide_3_v2.png"))


func _slide_friend_route() -> Dictionary:
	var out: Dictionary = {}
	var count := 0
	for index in range(main.friends.size()):
		var friend: Dictionary = main.friends[index]
		if String(friend.get("game", "")) == "slide" \
				and String(friend.get("mode", "")) == "fish":
			count += 1
			if out.is_empty():
				out = {"friend": friend, "index": index}
	if count != 1:
		return {}
	return out


func _slide_touch_target(target_id: String) -> Dictionary:
	for value: Variant in main.touch_interactables:
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == target_id:
			return target
	return {}


func _slide_progress_snapshot(friend: Dictionary) -> Dictionary:
	return {
		"pearls": int(main.pearl_count),
		"trophies": int(main.trophies),
		"stickers": main.stickers.duplicate(true),
		"medals": main.medals.duplicate(true),
		"found": bool(friend.get("found", false)),
		"won": bool(friend.get("won", false)),
		"star": friend.get("star"),
	}


func _slide_living_world_snapshot() -> Dictionary:
	var canvas: LivingWorldCanvas = main.living_canvas
	return {
		"stage_id": main.living_stage_id,
		"probe_stage_override": main.living_probe_stage_override,
		"time": main.living_time,
		"idle_time": main.living_idle_time,
		"cooldown": main.living_cooldown,
		"event_time": main.living_event_time,
		"event_count": main.living_event_count,
		"generation": main.living_generation,
		"layer_id": main.living_layer.get_instance_id()
			if main.living_layer != null else 0,
		"layer_visible": main.living_layer.visible
			if main.living_layer != null else false,
		"canvas_id": canvas.get_instance_id() if canvas != null else 0,
		"canvas_visible": canvas.visible if canvas != null else false,
		"canvas_stage_spec": canvas.stage_spec.duplicate(true)
			if canvas != null else {},
		"canvas_motion_time": canvas.motion_time if canvas != null else -1.0,
		"canvas_event_progress": canvas.event_progress
			if canvas != null else -2.0,
	}


func _slide_living_suppressed() -> bool:
	return main.living_layer != null and main.living_canvas != null \
		and not main.living_layer.visible


func _slide_living_hidden_matches(expected_visible_state: Dictionary) -> bool:
	if not _slide_living_suppressed():
		return false
	var current: Dictionary = _slide_living_world_snapshot()
	current["layer_visible"] = bool(expected_visible_state.get(
		"layer_visible", false))
	return current == expected_visible_state


func _slide_return_world_snapshot(friend: Dictionary) -> Dictionary:
	var pearl: Variant = main.pearls[0] if not main.pearls.is_empty() else null
	return {
		"position": player.position,
		"rotation": player.rotation,
		"yaw": player.yaw,
		"vel": player.vel,
		"visible": player.visible,
		"camera": _slide_camera_snapshot(),
		"environment": main.we_node.environment,
		"living": _slide_living_world_snapshot(),
		"reward": _slide_progress_snapshot(friend),
		"generation": main.save_generation,
		"fingerprint": _slide_save_fingerprint(),
		"trophies": main.trophies,
		"pearls": main.pearl_count,
		"medals": main.medals.duplicate(true),
		"friend_won": bool(friend.get("won", false)),
		"friend_star": friend.get("star"),
		"collection_layer_visible": main.collection_button_layer != null \
			and main.collection_button_layer.visible,
		"collection_button_visible": main.collection_button != null \
			and main.collection_button.is_visible_in_tree(),
		"fxw_probe": main.fxw_cool.get(&"slide_return_probe"),
		"pearl_id": pearl.get_instance_id() if pearl != null else 0,
		"pearl_transform": pearl.transform if pearl != null else null,
		"pearl_rotation": pearl.rotation if pearl != null else null,
	}


func _slide_return_world_matches(expected: Dictionary,
		friend: Dictionary) -> bool:
	var pearl: Variant = main.pearls[0] if not main.pearls.is_empty() else null
	return player.position == expected.get("position") \
		and player.rotation == expected.get("rotation") \
		and is_equal_approx(player.yaw, float(expected.get("yaw", INF))) \
		and player.vel == expected.get("vel") \
		and player.visible == bool(expected.get("visible", false)) \
		and _slide_camera_snapshot() == (expected.get("camera", {}) as Dictionary) \
		and main.we_node.environment == expected.get("environment") \
		and _slide_living_world_snapshot() \
			== (expected.get("living", {}) as Dictionary) \
		and _slide_progress_snapshot(friend) \
			== (expected.get("reward", {}) as Dictionary) \
		and main.save_generation == int(expected.get("generation", -1)) \
		and _slide_save_fingerprint() == String(expected.get("fingerprint", "")) \
		and main.trophies == int(expected.get("trophies", -1)) \
		and main.pearl_count == int(expected.get("pearls", -1)) \
		and main.medals == (expected.get("medals", {}) as Dictionary) \
		and bool(friend.get("won", false)) \
			== bool(expected.get("friend_won", false)) \
		and friend.get("star") == expected.get("friend_star") \
		and main.collection_button_layer != null \
		and main.collection_button_layer.visible \
			== bool(expected.get("collection_layer_visible", false)) \
		and main.collection_button != null \
		and main.collection_button.is_visible_in_tree() \
			== bool(expected.get("collection_button_visible", false)) \
		and main.fxw_cool.get(&"slide_return_probe") \
			== expected.get("fxw_probe") \
		and (pearl.get_instance_id() if pearl != null else 0) \
			== int(expected.get("pearl_id", -1)) \
		and (pearl.transform if pearl != null else null) \
			== expected.get("pearl_transform") \
		and (pearl.rotation if pearl != null else null) \
			== expected.get("pearl_rotation")


func _slide_save_fingerprint() -> String:
	var save: Dictionary = _slide_read_save()
	if save.is_empty():
		return ""
	save.erase("save_generation")
	return JSON.stringify(save).sha256_text()


func _slide_read_save() -> Dictionary:
	var path := "user://reef_save.json"
	if not FileAccess.file_exists(path):
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return parsed as Dictionary if parsed is Dictionary else {}


func _slide_saved_medal() -> int:
	var save: Dictionary = _slide_read_save()
	return int((save.get("medals", {}) as Dictionary).get("slide", 0))


func _slide_saved_friend_won() -> bool:
	var save: Dictionary = _slide_read_save()
	return bool((save.get("won", {}) as Dictionary).get(
		"Harper and Fiona", false))


func _slide_music_context() -> Dictionary:
	if main.music == null:
		return {}
	return {
		"track": main.cur_track,
		"stream": main.music.stream,
		"playing": main.music.playing,
		"pitch": main.music.pitch_scale,
	}


func _slide_music_matches(expected: Dictionary) -> bool:
	return main.music != null and main.cur_track == String(expected.get("track", "")) \
		and main.music.stream == expected.get("stream") \
		and main.music.playing == bool(expected.get("playing", false)) \
		and is_equal_approx(main.music.pitch_scale,
			float(expected.get("pitch", 1.0)))


func _slide_chime_context() -> Dictionary:
	if main.chime == null:
		return {}
	return {
		"volume_db": main.chime.volume_db,
		"pitch_scale": main.chime.pitch_scale,
	}


func _slide_chime_matches(expected: Dictionary) -> bool:
	return main.chime != null and not expected.is_empty() \
		and is_equal_approx(main.chime.volume_db,
			float(expected.get("volume_db", INF))) \
		and is_equal_approx(main.chime.pitch_scale,
			float(expected.get("pitch_scale", INF)))


func _slide_chime_snapshot_matches(actual: Dictionary,
		volume_db: float, pitch_scale: float) -> bool:
	return not actual.is_empty() \
		and is_equal_approx(float(actual.get("volume_db", INF)), volume_db) \
		and is_equal_approx(float(actual.get(
			"pitch_scale", INF)), pitch_scale)


func _slide_set_chime(volume_db: float, pitch_scale: float) -> void:
	if main.chime == null:
		return
	main.chime.volume_db = volume_db
	main.chime.pitch_scale = pitch_scale


func _slide_restore_chime_context(expected: Dictionary) -> void:
	if main.chime == null or expected.is_empty():
		return
	main.chime.volume_db = float(expected.get("volume_db", main.chime.volume_db))
	main.chime.pitch_scale = float(expected.get(
		"pitch_scale", main.chime.pitch_scale))


func _slide_camera_snapshot() -> Dictionary:
	var camera: Variant = player.cam
	if camera == null:
		return {}
	return {
		"transform": camera.transform,
		"fov": camera.fov,
		"orbit": player.cam_orbit,
		"pitch": player.cam_pitch_off,
		"current": camera.current,
		"active": main.active_viewport_camera() == camera,
	}


func _slide_camera_matches(expected: Dictionary,
		require_current: bool) -> bool:
	var camera: Variant = player.cam
	return camera != null and camera.transform == expected.get("transform") \
		and is_equal_approx(camera.fov, float(expected.get("fov", -1.0))) \
		and is_equal_approx(player.cam_orbit,
			float(expected.get("orbit", 99.0))) \
		and is_equal_approx(player.cam_pitch_off,
			float(expected.get("pitch", 99.0))) \
		and (not require_current or (camera.current \
			and main.active_viewport_camera() == camera))


func _slide_restore_camera_snapshot(expected: Dictionary) -> void:
	var camera: Variant = player.cam
	if camera == null or expected.is_empty():
		return
	camera.transform = expected.get("transform")
	camera.fov = float(expected.get("fov", camera.fov))
	player.cam_orbit = float(expected.get("orbit", player.cam_orbit))
	player.cam_pitch_off = float(expected.get("pitch", player.cam_pitch_off))
	if bool(expected.get("current", false)):
		camera.make_current()
	else:
		camera.clear_current(false)


func _slide_direct_child_ids() -> Dictionary:
	var ids: Dictionary = {}
	for value: Variant in main.get_children():
		var child := value as Node
		ids[child.get_instance_id()] = String(child.name)
	return ids


func _slide_active_layer_count() -> int:
	var count := 0
	for value: Variant in main.get_children():
		var child := value as Node
		if child is CanvasLayer \
				and child.name == &"HarperFionaFishSlideCanvasLayer":
			count += 1
	return count


func _slide_collection_suppressed() -> bool:
	return main.collection_button_layer != null \
		and main.collection_button != null \
		and not main.collection_button_layer.visible \
		and not main.collection_button.is_visible_in_tree() \
		and not _slide_control_pointer_live(main.collection_button)


func _slide_control_pointer_live(control: Control) -> bool:
	if control == null or not control.is_visible_in_tree() \
			or control.mouse_filter == Control.MOUSE_FILTER_IGNORE:
		return false
	return not (control is BaseButton) or not (control as BaseButton).disabled


func _slide_canvas_layer_census(slide: SlideRaceGame,
		allow_sticker: bool = false, allow_dev: bool = false) -> Dictionary:
	var known_layers: Dictionary = {}
	for layer_value: Variant in [
		main.hud_layer, main.touch_ui, main.pause_layer, main.speech_layer,
	]:
		var known := layer_value as CanvasLayer
		if known != null:
			known_layers[known.get_instance_id()] = true
	if main.fade_rect != null:
		var fade_layer := main.fade_rect.get_parent() as CanvasLayer
		if fade_layer != null:
			known_layers[fade_layer.get_instance_id()] = true
	if allow_sticker and main.stickers_layer != null:
		known_layers[main.stickers_layer.get_instance_id()] = true
	# A deliberate fresh stick move may reveal the production's noninteractive
	# star cursor over Sticker Book. Admit only that exact active/visible layer;
	# its descendants still pass through the pointer-live census below.
	if allow_sticker and main.pad_cursor_layer != null \
			and main.pad_cursor_active and main.pad_cursor_layer.visible:
		known_layers[main.pad_cursor_layer.get_instance_id()] = true
	if allow_dev and main.dev_mode is CanvasLayer:
		known_layers[(main.dev_mode as CanvasLayer).get_instance_id()] = true
	var unknown_layers: Array[String] = []
	var unexpected_controls: Array[String] = []
	var visible_layers: Array[String] = []
	for child_value: Variant in main.get_children():
		var layer := child_value as CanvasLayer
		if layer == null or layer == slide.active_layer() \
				or layer.layer <= SlideRaceGame.FISH_CANVAS_LAYER \
				or not layer.visible:
			continue
		visible_layers.append("%s@%d" % [String(layer.name), layer.layer])
		if not known_layers.has(layer.get_instance_id()):
			unknown_layers.append("%s@%d" % [String(layer.name), layer.layer])
		var pending: Array[Node] = [layer]
		while not pending.is_empty():
			var node: Node = pending.pop_back()
			for descendant_value: Variant in node.get_children():
				var descendant := descendant_value as Node
				if descendant != null:
					pending.append(descendant)
			var control := node as Control
			if not _slide_control_pointer_live(control):
				continue
			var allowed := false
			if layer == main.pause_layer:
				var corner: Variant = main.pause_layer.get_meta("corner_button")
				allowed = control == corner and not main.get_tree().paused \
					and not main.pause_panel.visible
				allowed = allowed or (main.get_tree().paused \
					and main.pause_panel.visible)
			elif control == main.fade_rect:
				allowed = main.fade_rect.mouse_filter \
					== Control.MOUSE_FILTER_STOP
			elif allow_sticker and layer == main.stickers_layer:
				allowed = true
			elif allow_dev and layer == main.dev_mode:
				allowed = true
			if not allowed:
				unexpected_controls.append("%s/%s" % [
					String(layer.name), String(control.name)])
	return {
		"exact": unknown_layers.is_empty()
			and unexpected_controls.is_empty()
			and _slide_collection_suppressed()
			and _slide_living_suppressed(),
		"visible_layers": visible_layers,
		"unknown_layers": unknown_layers,
		"unexpected_controls": unexpected_controls,
	}


func _slide_check_entry_contract(slide: SlideRaceGame,
		direct_before: Dictionary, return_camera: Dictionary,
		return_living: Dictionary) -> void:
	var layer: CanvasLayer = slide.active_layer()
	var surface: Node2D = slide.stage_root()
	var snapshot: Dictionary = slide.audit_snapshot()
	var direct_after: Dictionary = _slide_direct_child_ids()
	var baseline_preserved := true
	for id_value: Variant in direct_before.keys():
		baseline_preserved = baseline_preserved and direct_after.has(id_value)
	_slide_check("entry owns one stable Canvas layer below pause and above HUD",
		layer != null and surface != null
		and layer.name == &"HarperFionaFishSlideCanvasLayer"
		and surface.name == &"HarperFionaFishSlideCanvas"
		and layer.layer == 7 and layer.layer < main.pause_layer.layer
		and layer.layer > main.hud_layer.layer
		and not direct_before.has(layer.get_instance_id())
		and direct_after.has(layer.get_instance_id()) and baseline_preserved
		and _slide_active_layer_count() == 1)
	var camera: Variant = player.cam
	_slide_check("entry snapshots the exact nondefault lens and clears viewport ownership",
		camera != null and main.active_viewport_camera() == null
		and main.g.get("slide_canvas_return_camera") == camera
		and bool(main.g.get("slide_canvas_camera_was_current", false))
		and main.g.get("slide_canvas_player_cam_transform") \
			== return_camera.get("transform")
		and is_equal_approx(float(main.g.get(
			"slide_canvas_player_cam_fov", -1.0)),
			float(return_camera.get("fov", -2.0)))
		and is_equal_approx(float(main.g.get(
			"slide_canvas_player_cam_orbit", 99.0)),
			float(return_camera.get("orbit", -99.0)))
		and is_equal_approx(float(main.g.get(
			"slide_canvas_player_cam_pitch", 99.0)),
			float(return_camera.get("pitch", -99.0))))
	var layer_census: Dictionary = _slide_canvas_layer_census(slide)
	_slide_check("entry hides the Critter Book and leaves no persistent click target over the stage",
		_slide_collection_suppressed()
		and bool(layer_census.get("exact", false))
		and bool(main.g.get("slide_canvas_collection_was_visible", false)))
	_slide_check("entry snapshots and removes the living-world layer from lower drawing",
		bool(main.g.get("slide_canvas_living_was_visible", false))
			== bool(return_living.get("layer_visible", false))
		and _slide_living_hidden_matches(return_living))
	_slide_check("stage tree contains only the exact backdrop, actors, fish, pips, and dual steer cues",
		_slide_surface_structure_exact(surface)
		and _melody_spatial_descendant_count(layer) == 0
		and int(snapshot.get("spatial_descendants", -1)) == 0
		and main.game_nodes.is_empty())
	_slide_check("controller route and mercy semantics are exact",
		bool(snapshot.get("route_exact", false))
		and String(snapshot.get("game", "")) == "slide"
		and String(snapshot.get("mode", "")) == "fish"
		and slide.fish_count() == 5 and slide.progress_count() == 0
		and float(main.g.get("timer", 0.0)) < 0.0
		and bool(snapshot.get("no_fail_state", false))
		and not bool(snapshot.get("has_controller_timer_increment", true))
		and not bool(snapshot.get("completed", true))
		and not main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 0)
	_slide_check("post-Canvas census maps every touch, mouse, key, pad, and axis terminal exactly",
		_slide_return_source_token_contract())
	_slide_check("opening objective is exact voice plus persistent non-reader steer cues",
		SlideRaceGame.FISH_OBJECTIVE == SLIDE_OBJECTIVE
		and main.hud_msg.text.is_empty() and not main.hud_msg.visible
		and is_zero_approx(main.msg_timer)
		and bool(snapshot.get("steer_cues_persistent", false))
		and _slide_steer_cue_contract(slide, surface, snapshot))
	_slide_check("runtime binds exact native tiles through one common transform",
		_slide_runtime_tile_contract(surface, snapshot))
	_slide_check("runtime binds protected friends, slide, Roshan, five fish and five pips",
		_slide_runtime_actor_contract(surface))
	var resources: Dictionary = _slide_runtime_resource_contract(slide, surface)
	_slide_check("live Canvas owns exactly eleven reused texture resources within 24 MiB",
		bool(resources.get("exact", false))
		and int(resources.get("decoded_bytes", 0)) <= 24 * 1024 * 1024
		and bool(resources.get("fish_reused", false)))


func _slide_surface_structure_exact(surface: Node2D) -> bool:
	if surface == null or not _slide_exact_direct_names(surface, [
		"OpaqueSkyFill", "SkyLagoonCenterTilesCommonTransform",
		"SkyReadabilityWash", "FishSlideResponsiveStage",
		"FishSlideStorybookTrim", "PersistentLeftSteerCue",
		"PersistentRightSteerCue",
	]):
		return false
	var backdrop := surface.get_node_or_null(
		"SkyLagoonCenterTilesCommonTransform") as Node2D
	var play := surface.get_node_or_null("FishSlideResponsiveStage") as Node2D
	if backdrop == null or play == null \
			or not _slide_exact_direct_names(backdrop, SLIDE_TILE_NAMES):
		return false
	var play_names: Array[String] = [
		"ApprovedCompactSlide", "HarperAndFionaProtectedArt", "RoshanSliding",
	]
	for index in range(5):
		play_names.append("Clownfish%d" % index)
		play_names.append("FishProgressPip%d" % index)
	return _slide_exact_direct_names(play, play_names)


func _slide_exact_direct_names(node: Node, expected: Array) -> bool:
	if node == null or node.get_child_count() != expected.size():
		return false
	for index in range(expected.size()):
		if String(node.get_child(index).name) != String(expected[index]):
			return false
	return true


func _slide_runtime_tile_contract(surface: Node2D,
		snapshot: Dictionary) -> bool:
	var backdrop := surface.get_node_or_null(
		"SkyLagoonCenterTilesCommonTransform") as Node2D
	if backdrop == null or backdrop.get_child_count() != 4:
		return false
	var viewport_size: Vector2 = snapshot.get("viewport_size", Vector2.ZERO)
	var expected_scale: float = maxf(
		viewport_size.x / 2048.0, viewport_size.y / 2048.0)
	var expected_positions: Array[Vector2] = [
		Vector2(-512.0, -512.0), Vector2(512.0, -512.0),
		Vector2(-512.0, 512.0), Vector2(512.0, 512.0),
	]
	var rects: Array[Rect2] = []
	var exact: bool = backdrop.position.is_equal_approx(viewport_size * 0.5) \
		and backdrop.scale.is_equal_approx(Vector2.ONE * expected_scale) \
		and backdrop.get_meta("native_size", Vector2i()) \
			== Vector2i(2048, 2048) \
		and is_equal_approx(float(backdrop.get_meta("common_scale", -1.0)),
			expected_scale) \
		and snapshot.get("tile_paths", []) == SLIDE_TILE_PATHS \
		and snapshot.get("tile_source_rects", []) == SLIDE_TILE_RECTS \
		and snapshot.get("tile_native_reconstruction", Vector2i()) \
			== Vector2i(2048, 2048)
	for index in range(4):
		var tile := backdrop.get_child(index) as Sprite2D
		if tile == null or tile.texture == null:
			return false
		exact = exact and tile.name == StringName(SLIDE_TILE_NAMES[index]) \
			and tile.texture.resource_path == SLIDE_TILE_PATHS[index] \
			and String(tile.get_meta("source_path", "")) \
				== SLIDE_TILE_PATHS[index] \
			and tile.get_meta("native_source_rect", Rect2i()) \
				== SLIDE_TILE_RECTS[index] \
			and tile.texture.get_size() == Vector2(1024, 1024) \
			and tile.position.is_equal_approx(expected_positions[index]) \
			and tile.scale.is_equal_approx(Vector2.ONE) \
			and tile.centered and not tile.region_enabled \
			and tile.get_child_count() == 0 \
			and _melody_effective_z(tile) == -90
		rects.append(_slide_sprite_rect(tile))
	var tolerance := 1.5
	var union_rect: Rect2 = rects[0]
	for index in range(1, rects.size()):
		union_rect = union_rect.merge(rects[index])
	var seams := absf(rects[0].end.x - rects[1].position.x) <= tolerance \
		and absf(rects[2].end.x - rects[3].position.x) <= tolerance \
		and absf(rects[0].end.y - rects[2].position.y) <= tolerance \
		and absf(rects[1].end.y - rects[3].position.y) <= tolerance
	return exact and seams and union_rect.grow(tolerance).encloses(
		Rect2(Vector2.ZERO, viewport_size))


func _slide_runtime_actor_contract(surface: Node2D) -> bool:
	var play := surface.get_node_or_null("FishSlideResponsiveStage") as Node2D
	if play == null:
		return false
	var slide := play.get_node_or_null("ApprovedCompactSlide") as Sprite2D
	var friends := play.get_node_or_null(
		"HarperAndFionaProtectedArt") as Sprite2D
	var roshan := play.get_node_or_null("RoshanSliding") as Sprite2D
	if not _slide_sprite_source_exact(slide, SLIDE_ACTOR_PATHS[0], 12) \
			or not _slide_sprite_source_exact(friends, SLIDE_ACTOR_PATHS[1], 14) \
			or roshan == null or roshan.texture == null \
			or roshan.texture.resource_path not in SLIDE_ACTOR_PATHS.slice(3) \
			or _melody_effective_z(roshan) != 24 \
			or not bool(friends.get_meta("protected_original_unchanged", false)):
		return false
	for index in range(5):
		var fish := play.get_node_or_null("Clownfish%d" % index) as Sprite2D
		var pip := play.get_node_or_null("FishProgressPip%d" % index) as Sprite2D
		if not _slide_sprite_source_exact(fish, SLIDE_ACTOR_PATHS[2], 20) \
				or not _slide_sprite_source_exact(pip, SLIDE_ACTOR_PATHS[2], 31) \
				or int(fish.get_meta("fish_index", -1)) != index \
				or int(pip.get_meta("fish_index", -1)) != index:
			return false
	return true


func _slide_runtime_resource_contract(slide: SlideRaceGame,
		surface: Node2D) -> Dictionary:
	var sprites: Array[Sprite2D] = _slide_canvas_sprites(surface)
	var texture_by_path: Dictionary = {}
	for sprite: Sprite2D in sprites:
		if sprite.texture == null or sprite.texture.resource_path.is_empty():
			continue
		texture_by_path[sprite.texture.resource_path] = sprite.texture
	# Roshan's other three accepted poses are controller-cached so a frame swap
	# allocates nothing. They are live Canvas resources even while only one pose
	# is attached to the visible subtree at a time.
	var cached_value: Variant = slide.get("_fish_roshan_textures")
	if cached_value is Array:
		for texture_value: Variant in cached_value as Array:
			var texture := texture_value as Texture2D
			if texture != null and not texture.resource_path.is_empty():
				texture_by_path[texture.resource_path] = texture
	var actual_paths: Array[String] = []
	for path_value: Variant in texture_by_path.keys():
		actual_paths.append(String(path_value))
	actual_paths.sort()
	var expected_paths: Array[String] = []
	expected_paths.append_array(SLIDE_TILE_PATHS)
	expected_paths.append_array(SLIDE_ACTOR_PATHS)
	expected_paths.sort()
	var decoded_bytes := 0
	for path: String in actual_paths:
		var texture := texture_by_path.get(path) as Texture2D
		if texture == null:
			continue
		var size: Vector2 = texture.get_size()
		# Every accepted source is PNG/RGBA-compatible. Four bytes per native
		# texel is a conservative decoded runtime budget without double-counting
		# the ten fish/pip nodes that share one cached Texture2D.
		decoded_bytes += int(size.x) * int(size.y) * 4
	var play := surface.get_node_or_null("FishSlideResponsiveStage") as Node2D
	var shared_fish: Texture2D = null
	var fish_reused := play != null
	if play != null:
		for index in range(5):
			var fish := play.get_node_or_null("Clownfish%d" % index) as Sprite2D
			var pip := play.get_node_or_null(
				"FishProgressPip%d" % index) as Sprite2D
			if fish == null or pip == null or fish.texture == null \
					or pip.texture == null:
				fish_reused = false
				continue
			if shared_fish == null:
				shared_fish = fish.texture
			fish_reused = fish_reused and fish.texture == shared_fish \
				and pip.texture == shared_fish \
				and shared_fish.resource_path == SLIDE_ACTOR_PATHS[2]
	return {
		"exact": sprites.size() == 17 and actual_paths == expected_paths,
		"paths": actual_paths,
		"decoded_bytes": decoded_bytes,
		"fish_reused": fish_reused,
	}


func _slide_canvas_sprites(surface: Node2D) -> Array[Sprite2D]:
	var sprites: Array[Sprite2D] = []
	if surface == null:
		return sprites
	var pending: Array[Node] = [surface]
	while not pending.is_empty():
		var node: Node = pending.pop_back()
		if node is Sprite2D:
			sprites.append(node as Sprite2D)
		for child_value: Variant in node.get_children():
			var child := child_value as Node
			if child != null:
				pending.append(child)
	return sprites


func _slide_visible_sprite_texture_coverage_screens(surface: Node2D,
		viewport_rect: Rect2) -> float:
	if surface == null or not viewport_rect.has_area():
		return INF
	var area := 0.0
	for sprite: Sprite2D in _slide_canvas_sprites(surface):
		if not sprite.is_visible_in_tree() or sprite.texture == null \
				or sprite.modulate.a <= 0.0 or sprite.self_modulate.a <= 0.0:
			continue
		var clipped: Rect2 = _slide_sprite_rect(sprite).intersection(viewport_rect)
		if clipped.has_area():
			area += clipped.get_area()
	return area / viewport_rect.get_area()


func _slide_full_screen_color_rect_contract(surface: Node2D,
		viewport_rect: Rect2) -> bool:
	if surface == null or not viewport_rect.has_area():
		return false
	var color_rects: Array[ColorRect] = []
	var pending: Array[Node] = [surface]
	while not pending.is_empty():
		var node: Node = pending.pop_back()
		if node is ColorRect:
			color_rects.append(node as ColorRect)
		for child_value: Variant in node.get_children():
			var child := child_value as Node
			if child != null:
				pending.append(child)
	if color_rects.size() != 2:
		return false
	var names: Array[String] = []
	for rect: ColorRect in color_rects:
		names.append(String(rect.name))
		if not rect.is_visible_in_tree() \
				or rect.mouse_filter != Control.MOUSE_FILTER_IGNORE \
				or not _slide_rect_approximately_equal(
					rect.get_global_rect(), viewport_rect, 1.5):
			return false
	names.sort()
	return names == ["OpaqueSkyFill", "SkyReadabilityWash"]


func _slide_sprite_source_exact(sprite: Sprite2D, path: String,
		expected_z: int) -> bool:
	return sprite != null and sprite.texture != null \
		and sprite.texture.resource_path == path \
		and String(sprite.get_meta("source_path", "")) == path \
		and _melody_effective_z(sprite) == expected_z \
		and sprite.centered and not sprite.region_enabled \
		and sprite.get_child_count() == 0 \
		and sprite.modulate.a > 0.5 and sprite.self_modulate.a > 0.5


func _slide_sprite_rect(sprite: Sprite2D) -> Rect2:
	return _melody_transform_rect(sprite.get_rect(),
		sprite.get_global_transform_with_canvas()) if sprite != null else Rect2()


func _slide_texture_alpha_used_rect(texture: Texture2D) -> Rect2i:
	if texture == null:
		return Rect2i()
	var key: String = texture.resource_path
	if key.is_empty():
		key = "instance:%d" % texture.get_instance_id()
	if slide_alpha_cache.has(key):
		return slide_alpha_cache[key] as Rect2i
	var used: Rect2i = _slide_image_alpha_rect(texture.get_image())
	slide_alpha_cache[key] = used
	return used


func _slide_image_alpha_rect(image: Image) -> Rect2i:
	if image == null or image.is_empty():
		return Rect2i()
	var scan: Image = image
	if scan.is_compressed():
		scan = image.duplicate()
		if scan.decompress() != OK:
			return Rect2i()
	var min_point := Vector2i(scan.get_width(), scan.get_height())
	var max_point := Vector2i(-1, -1)
	for y in range(scan.get_height()):
		for x in range(scan.get_width()):
			if scan.get_pixel(x, y).a <= 0.05:
				continue
			min_point.x = mini(min_point.x, x)
			min_point.y = mini(min_point.y, y)
			max_point.x = maxi(max_point.x, x)
			max_point.y = maxi(max_point.y, y)
	if max_point.x < min_point.x or max_point.y < min_point.y:
		return Rect2i()
	return Rect2i(min_point, max_point - min_point + Vector2i.ONE)


func _slide_cue_screen_rect(cue: Node2D) -> Rect2:
	if cue == null or not cue.has_method(&"screen_rect"):
		return Rect2()
	var local_rect: Rect2 = cue.call("screen_rect") as Rect2
	return _melody_transform_rect(
		local_rect, cue.get_global_transform_with_canvas())


func _slide_cue_screen_center(cue: Node2D) -> Vector2:
	if cue == null:
		return Vector2(-99.0, -99.0)
	var local_center: Vector2 = cue.get("cue_center") as Vector2
	return cue.get_global_transform_with_canvas() * local_center


func _slide_cue_screen_tip(cue: Node2D) -> Vector2:
	if cue == null or not cue.has_method(&"arrow_tip"):
		return Vector2(-99.0, -99.0)
	var local_tip: Vector2 = cue.call("arrow_tip") as Vector2
	return cue.get_global_transform_with_canvas() * local_tip


func _slide_steer_cue_contract(slide: SlideRaceGame, surface: Node2D,
		snapshot: Dictionary) -> bool:
	if slide == null or surface == null:
		return false
	var play := surface.get_node_or_null("FishSlideResponsiveStage") as Node2D
	var left := surface.get_node_or_null("PersistentLeftSteerCue") as Node2D
	var right := surface.get_node_or_null("PersistentRightSteerCue") as Node2D
	if play == null or left == null or right == null:
		return false
	var viewport_size: Vector2 = snapshot.get("viewport_size", Vector2.ZERO)
	var viewport_rect := Rect2(Vector2.ZERO, viewport_size)
	var left_rect: Rect2 = _slide_cue_screen_rect(left)
	var right_rect: Rect2 = _slide_cue_screen_rect(right)
	var left_center: Vector2 = _slide_cue_screen_center(left)
	var right_center: Vector2 = _slide_cue_screen_center(right)
	var left_tip: Vector2 = _slide_cue_screen_tip(left)
	var right_tip: Vector2 = _slide_cue_screen_tip(right)
	var expected_left: Vector2 = play.get_global_transform_with_canvas() \
		* Vector2(120.0, 650.0)
	var expected_right: Vector2 = play.get_global_transform_with_canvas() \
		* Vector2(1160.0, 650.0)
	var left_axis: float = float(slide.call("_touch_axis", left_tip))
	var right_axis: float = float(slide.call("_touch_axis", right_tip))
	var left_center_axis: float = float(slide.call(
		"_touch_axis", left_center))
	var right_center_axis: float = float(slide.call(
		"_touch_axis", right_center))
	var combined: float = float(snapshot.get("combined_steer", 0.0))
	var left_active: bool = bool(left.get("cue_active"))
	var right_active: bool = bool(right.get("cue_active"))
	return left.get_parent() == surface and right.get_parent() == surface \
		and left.get_child_count() == 0 and right.get_child_count() == 0 \
		and left.visible and right.visible \
		and _melody_effective_z(left) == 30 \
		and _melody_effective_z(right) == 30 \
		and is_equal_approx(float(left.get("cue_direction")), -1.0) \
		and is_equal_approx(float(right.get("cue_direction")), 1.0) \
		and float(left.get("cue_scale")) > 0.0 \
		and is_equal_approx(float(left.get("cue_scale")), \
			float(right.get("cue_scale"))) \
		and left_rect.has_area() and right_rect.has_area() \
		and viewport_rect.encloses(left_rect) \
		and viewport_rect.encloses(right_rect) \
		and left_rect.end.x < viewport_size.x * 0.5 \
		and right_rect.position.x > viewport_size.x * 0.5 \
		and not left_rect.intersects(right_rect, true) \
		and viewport_rect.has_point(left_center) \
		and viewport_rect.has_point(right_center) \
		and viewport_rect.has_point(left_tip) \
		and viewport_rect.has_point(right_tip) \
		and left_center.distance_to(expected_left) <= 1.5 \
		and right_center.distance_to(expected_right) <= 1.5 \
		and left_tip.x < left_center.x and right_tip.x > right_center.x \
		and left_center_axis < -SlideRaceGame.FISH_STEER_DEAD_ZONE \
		and right_center_axis > SlideRaceGame.FISH_STEER_DEAD_ZONE \
		and left_axis < -SlideRaceGame.FISH_STEER_DEAD_ZONE \
		and right_axis > SlideRaceGame.FISH_STEER_DEAD_ZONE \
		and (snapshot.get("steer_cue_names", []) as Array) \
			== ["PersistentLeftSteerCue", "PersistentRightSteerCue"] \
		and bool(snapshot.get("steer_cues_persistent", false)) \
		and _slide_rect_approximately_equal(left_rect, \
			snapshot.get("left_steer_cue_rect", Rect2()), 1.5) \
		and _slide_rect_approximately_equal(right_rect, \
			snapshot.get("right_steer_cue_rect", Rect2()), 1.5) \
		and left_center.distance_to(snapshot.get(
			"left_steer_cue_center", Vector2(-99.0, -99.0))) <= 1.5 \
		and right_center.distance_to(snapshot.get(
			"right_steer_cue_center", Vector2(-99.0, -99.0))) <= 1.5 \
		and left_tip.distance_to(snapshot.get(
			"left_steer_cue_tip", Vector2(-99.0, -99.0))) <= 1.5 \
		and right_tip.distance_to(snapshot.get(
			"right_steer_cue_tip", Vector2(-99.0, -99.0))) <= 1.5 \
		and left_active == (combined < -SlideRaceGame.FISH_STEER_DEAD_ZONE) \
		and right_active == (combined > SlideRaceGame.FISH_STEER_DEAD_ZONE)


func _slide_begin_opening_context_cross_product(
		slide: SlideRaceGame) -> Dictionary:
	var snapshot: Dictionary = slide.audit_snapshot()
	var baseline := {
		"t": float(main.g.get("t", -1.0)),
		"progress": float(snapshot.get("progress", -1.0)),
		"got": int(snapshot.get("got", -1)),
		"tick": int(snapshot.get("tick_count", -1)),
	}
	_slide_check("entry OS-loss fixture begins before the real fade callback",
		main.fade_rect != null and main.fade_rect.modulate.a > 0.02
		and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_STOP
		and is_zero_approx(float(snapshot.get("progress", -1.0)))
		and int(snapshot.get("got", -1)) == 0)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	var lost: Dictionary = slide.audit_snapshot()
	_slide_check("entry focus-out plus app-paused nests both reasons under black",
		bool(lost.get("input_context_lost", false))
		and (lost.get("input_context_loss_reasons", []) as Array).size() == 2
		and bool(lost.get("input_context_restore_guard", false))
		and _slide_owner_tokens(lost).is_empty()
		and is_equal_approx(float(main.g.get("t", -2.0)),
			float(baseline.get("t", -1.0))))
	main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	_slide_check("entry partial restore cannot override remaining focus loss",
		slide.input_context_lost()
		and is_equal_approx(float(slide.audit_snapshot().get(
			"progress", -2.0)), float(baseline.get("progress", -1.0)))
		and int(slide.audit_snapshot().get("got", -2))
			== int(baseline.get("got", -1)))
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	_slide_check("entry full restore retains a guard while fade still owns input",
		not slide.input_context_lost()
		and bool(slide.audit_snapshot().get(
			"input_context_restore_guard", false))
		and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_STOP)
	return baseline


func _slide_finish_opening_context_cross_product(slide: SlideRaceGame,
		baseline: Dictionary) -> void:
	var first_restored: Dictionary = slide.audit_snapshot()
	_slide_check("first restored frame retires only context guard under black",
		not bool(first_restored.get("input_context_restore_guard", true))
		and is_equal_approx(float(first_restored.get("progress", -2.0)),
			float(baseline.get("progress", -1.0)))
		and int(first_restored.get("got", -2))
			== int(baseline.get("got", -1))
		and int(first_restored.get("tick_count", -2))
			== int(baseline.get("tick", -1))
		and float(main.g.get("t", -2.0)) >= float(baseline.get("t", -1.0)))
	await _slide_wait_for_fade_callback(slide)
	var at_callback: Dictionary = slide.audit_snapshot()
	_slide_check("opening restore holds ride progress through the fade callback",
		is_zero_approx(float(at_callback.get("progress", -1.0)))
		and int(at_callback.get("got", -1)) == int(baseline.get("got", -2))
		and main.fade_rect != null
		and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE
		and main.fade_rect.modulate.a <= 0.02)
	await process_frame
	var first_active: Dictionary = slide.audit_snapshot()
	_slide_check("first active boundary after callback is still source-free at the shell",
		is_zero_approx(float(first_active.get("progress", -1.0)))
		and int(first_active.get("got", -1)) == int(baseline.get("got", -2))
		and _slide_owner_tokens(first_active).is_empty()
		and not bool(first_active.get("input_context_restore_guard", true)))


func _slide_wait_for_fade_callback(slide: SlideRaceGame) -> void:
	var reached := false
	var boundary_safe := true
	for _index in range(180):
		if main.fade_rect == null:
			reached = true
			break
		var alpha_clear: bool = main.fade_rect.modulate.a <= 0.02
		var callback_clear: bool = main.fade_rect.mouse_filter \
			== Control.MOUSE_FILTER_IGNORE
		if alpha_clear and not callback_clear:
			var before: Dictionary = slide.audit_snapshot()
			_slide_push_key(KEY_LEFT, true, 20)
			var during: Dictionary = slide.audit_snapshot()
			_slide_push_key(KEY_LEFT, false, 20)
			boundary_safe = boundary_safe \
				and (during.get("input_sources", {}) as Dictionary).is_empty() \
				and int(during.get("got", -1)) == int(before.get("got", -2)) \
				and is_equal_approx(float(during.get("lane", 99.0)),
					float(before.get("lane", -99.0)))
		if alpha_clear and callback_clear:
			reached = true
			break
		await process_frame
	_slide_check("fade reveal restores input only at the real callback boundary",
		reached and boundary_safe and (main.fade_rect == null \
		or main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE))


func _slide_wait_until_ready(slide: SlideRaceGame) -> void:
	var ready := false
	for _index in range(30):
		var snapshot: Dictionary = slide.audit_snapshot()
		if not bool(snapshot.get("blocked_until_release", true)) \
				and not bool(snapshot.get("input_context_restore_guard", true)):
			ready = true
			break
		await process_frame
	if not ready:
		var blocked: Dictionary = slide.audit_snapshot()
		var fade_alpha := -1.0
		var fade_filter := -1
		if main.fade_rect != null:
			fade_alpha = main.fade_rect.modulate.a
			fade_filter = int(main.fade_rect.mouse_filter)
		print(("SLIDE_DIAG|startup-ready|blocked_until_release=%s" \
			+ "|blocked_sources=%s|restore_guard=%s|lost=%s|reasons=%s" \
			+ "|startup_guard=%s|fade_alpha=%.4f|fade_filter=%d" \
			+ "|main_held=%s|return_held=%s|axis_wait=%s|poll_neutral=%d") % [
			bool(blocked.get("blocked_until_release", true)),
			blocked.get("blocked_sources", {}),
			bool(blocked.get("input_context_restore_guard", true)),
			bool(blocked.get("input_context_lost", true)),
			blocked.get("input_context_loss_reasons", []),
			bool(slide.get("_fish_startup_release_guard")),
			fade_alpha, fade_filter, main._slide_canvas_held_sources,
			main._slide_canvas_return_held_sources,
			main._slide_canvas_overlay_axis_wait_neutral,
			main._slide_canvas_overlay_poll_neutral_frames,
		])
	_slide_check("bounded first active tick retires the startup release guard", ready)


func _slide_check_layouts(slide: SlideRaceGame) -> void:
	_slide_reset_run_state()
	await process_frame
	var layer_id: int = slide.active_layer().get_instance_id()
	var standard: Dictionary = _slide_layout_contract(slide)
	var standard_pips: bool = _slide_pip_fill_states_contract(slide)
	var standard_roshan: bool = _slide_roshan_pose_envelope_contract(slide)
	_slide_layout_diagnostic("1280x720", standard, standard_pips,
		standard_roshan)
	_slide_check(("1280x720 visible sprite texture coverage %.3f screens; " \
			+ "estimated painter coverage %.3f screens includes exactly two ColorRects; " \
			+ "native Mobile fill/FPS capture remains authoritative") % [
		float(standard.get("visible_sprite_texture_coverage_screens", INF)),
		float(standard.get("estimated_canvas_painter_screens", INF))],
		bool(standard.get("sprite_texture_coverage_bounded", false))
		and bool(standard.get("full_screen_color_rects_exact", false))
		and bool(standard.get("canvas_painter_estimate_exact", false)))
	_slide_check("actual 1280x720 stage is opaque, readable, and fully contained",
		Vector2i(standard.get("viewport", Vector2.ZERO)) == SLIDE_VIEW_SIZE
		and bool(standard.get("opaque", false))
		and bool(standard.get("actors", false))
		and bool(standard.get("progress", false))
		and bool(standard.get("z_order", false))
		and bool(standard.get("tiles", false))
		and bool(standard.get("resources", false))
		and bool(standard.get("sprite_texture_coverage_bounded", false))
		and bool(standard.get("full_screen_color_rects_exact", false))
		and bool(standard.get("canvas_painter_estimate_exact", false))
		and bool(standard.get("trim", false))
		and bool(standard.get("layers", false))
		and standard_pips and standard_roshan
		and bool(standard.get("camera_null", false)))
	get_root().size = SLIDE_TALL_SIZE
	await _frames(4)
	var tall: Dictionary = _slide_layout_contract(slide)
	var tall_pips: bool = _slide_pip_fill_states_contract(slide)
	var tall_roshan: bool = _slide_roshan_pose_envelope_contract(slide)
	_slide_layout_diagnostic("1280x800", tall, tall_pips, tall_roshan)
	_slide_check(("1280x800 visible sprite texture coverage %.3f screens; " \
			+ "estimated Canvas painter coverage %.3f screens") % [
		float(tall.get("visible_sprite_texture_coverage_screens", INF)),
		float(tall.get("estimated_canvas_painter_screens", INF))],
		bool(tall.get("sprite_texture_coverage_bounded", false))
		and bool(tall.get("full_screen_color_rects_exact", false))
		and bool(tall.get("canvas_painter_estimate_exact", false)))
	_slide_check("same live stage reflows safely to 1280x800",
		Vector2i(tall.get("viewport", Vector2.ZERO)) == SLIDE_TALL_SIZE
		and slide.active_layer() != null
		and slide.active_layer().get_instance_id() == layer_id
		and bool(tall.get("opaque", false))
		and bool(tall.get("actors", false))
		and bool(tall.get("progress", false))
		and bool(tall.get("z_order", false))
		and bool(tall.get("tiles", false))
		and bool(tall.get("resources", false))
		and bool(tall.get("sprite_texture_coverage_bounded", false))
		and bool(tall.get("full_screen_color_rects_exact", false))
		and bool(tall.get("canvas_painter_estimate_exact", false))
		and bool(tall.get("trim", false))
		and bool(tall.get("layers", false))
		and tall_pips and tall_roshan
		and bool(tall.get("camera_null", false)))
	_slide_check("clear fade cover reflows to the exact 1280x800 viewport without rebuilding",
		_slide_fade_cover_contract(slide, SLIDE_TALL_SIZE, false))
	get_root().size = SLIDE_VIEW_SIZE
	await _frames(4)
	var restored: Dictionary = _slide_layout_contract(slide)
	var restored_pips: bool = _slide_pip_fill_states_contract(slide)
	var restored_roshan: bool = _slide_roshan_pose_envelope_contract(slide)
	_slide_layout_diagnostic("restored-1280x720", restored, restored_pips,
		restored_roshan)
	_slide_check(("restored 1280x720 visible sprite texture coverage %.3f screens; " \
			+ "estimated Canvas painter coverage %.3f screens") % [
		float(restored.get("visible_sprite_texture_coverage_screens", INF)),
		float(restored.get("estimated_canvas_painter_screens", INF))],
		bool(restored.get("sprite_texture_coverage_bounded", false))
		and bool(restored.get("full_screen_color_rects_exact", false))
		and bool(restored.get("canvas_painter_estimate_exact", false)))
	_slide_check("1280x720 restore needs no rebuild and retains all semantics",
		Vector2i(restored.get("viewport", Vector2.ZERO)) == SLIDE_VIEW_SIZE
		and slide.active_layer() != null
		and slide.active_layer().get_instance_id() == layer_id
		and bool(restored.get("opaque", false))
		and bool(restored.get("actors", false))
		and bool(restored.get("progress", false))
		and bool(restored.get("z_order", false))
		and bool(restored.get("tiles", false))
		and bool(restored.get("resources", false))
		and bool(restored.get("sprite_texture_coverage_bounded", false))
		and bool(restored.get("full_screen_color_rects_exact", false))
		and bool(restored.get("canvas_painter_estimate_exact", false))
		and bool(restored.get("trim", false))
		and bool(restored.get("layers", false))
		and restored_pips and restored_roshan
		and bool(restored.get("camera_null", false)))
	_slide_check("clear fade cover restores the exact 1280x720 viewport without rebuilding",
		_slide_fade_cover_contract(slide, SLIDE_VIEW_SIZE, false))
	_slide_reset_run_state()


func _slide_layout_diagnostic(label: String, contract: Dictionary,
		pips: bool, roshan: bool) -> void:
	var failed: Array[String] = []
	for key: String in ["opaque", "actors", "progress", "z_order", "tiles",
			"resources", "sprite_texture_coverage_bounded",
			"full_screen_color_rects_exact", "canvas_painter_estimate_exact",
			"trim", "layers", "camera_null", "_diag_points_inside",
			"_diag_fish_geometry", "_diag_steer_cues", "_diag_pip_geometry"]:
		if not bool(contract.get(key, false)):
			failed.append(key)
	if not pips:
		failed.append("pip_fill_states")
	if not roshan:
		failed.append("roshan_pose_envelope")
	if not failed.is_empty():
		print("SLIDE_DIAG|layout|%s|failed=%s|viewport=%s|sprite=%.4f|painter=%.4f" % [
			label, failed, contract.get("viewport", Vector2.ZERO),
			float(contract.get("visible_sprite_texture_coverage_screens", INF)),
			float(contract.get("estimated_canvas_painter_screens", INF)),
		])


func _slide_exercise_context_resize(slide: SlideRaceGame,
		friend: Dictionary) -> void:
	# Resize in both directions while two OS loss reasons own input. Renderer-only
	# layout must update on the first fully restored process boundary even though
	# course progress, collections, rewards, and the controller tick stay frozen.
	for tall_value: Variant in [true, false]:
		var tall := bool(tall_value)
		var target_size: Vector2i = SLIDE_TALL_SIZE if tall else SLIDE_VIEW_SIZE
		_slide_reset_run_state()
		await process_frame
		var before: Dictionary = slide.audit_snapshot()
		var before_reward: Dictionary = _slide_progress_snapshot(friend)
		var before_elapsed: float = float(main.g.get("t", 0.0)) \
			- float(main.g.get("canvas_run_start_t", 0.0))
		var layer: CanvasLayer = slide.active_layer()
		var surface: Node2D = slide.stage_root()
		var layer_id: int = layer.get_instance_id() if layer != null else 0
		var surface_id: int = surface.get_instance_id() if surface != null else 0
		if tall:
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
			main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
		else:
			main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
		get_root().size = target_size
		_slide_check("viewport resize remains gameplay-frozen while nested OS loss owns input",
			slide.input_context_lost()
			and (slide.audit_snapshot().get(
				"input_context_loss_reasons", []) as Array).size() == 2
			and int(slide.audit_snapshot().get("tick_count", -2)) \
				== int(before.get("tick_count", -1))
			and int(slide.audit_snapshot().get("got", -2)) \
				== int(before.get("got", -1))
			and is_equal_approx(float(slide.audit_snapshot().get(
				"progress", -2.0)), float(before.get("progress", -1.0)))
			and _slide_progress_snapshot(friend) == before_reward)
		if tall:
			main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
		else:
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
			main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
		_slide_check("full resize restore starts with the source-free controller guard",
			not slide.input_context_lost()
			and bool(slide.audit_snapshot().get(
				"input_context_restore_guard", false)))
		await process_frame
		var first: Dictionary = slide.audit_snapshot()
		var contract: Dictionary = _slide_layout_contract(slide)
		var first_elapsed: float = float(main.g.get("t", 0.0)) \
			- float(main.g.get("canvas_run_start_t", 0.0))
		_slide_check(("first restored resize boundary is fully laid out at %dx%d " \
				+ "without advancing the course") % [target_size.x, target_size.y],
			Vector2i(contract.get("viewport", Vector2.ZERO)) == target_size
			and bool(contract.get("opaque", false))
			and bool(contract.get("tiles", false))
			and bool(contract.get("trim", false))
			and bool(contract.get("progress", false))
			and bool(contract.get("full_screen_color_rects_exact", false))
			and slide.active_layer() != null and slide.stage_root() != null
			and slide.active_layer().get_instance_id() == layer_id
			and slide.stage_root().get_instance_id() == surface_id
			and not bool(first.get("input_context_restore_guard", true))
			and int(first.get("tick_count", -2)) \
				== int(before.get("tick_count", -1))
			and int(first.get("got", -2)) == int(before.get("got", -1))
			and is_equal_approx(float(first.get("progress", -2.0)),
				float(before.get("progress", -1.0)))
			and is_equal_approx(first_elapsed, before_elapsed)
			and _slide_progress_snapshot(friend) == before_reward
			and _slide_living_suppressed()
			and main.active_viewport_camera() == null)
		# The controller guard retires on the first boundary; its independent raw-
		# poll latch still requires two later trustworthy neutral process samples.
		await process_frame
		_slide_check("first post-resize neutral poll retains the independent latch",
			main._slide_canvas_overlay_axis_wait_neutral
			and main._slide_canvas_overlay_poll_neutral_frames == 1)
		await process_frame
		_slide_check("second post-resize neutral poll retires the independent latch",
			not main._slide_canvas_overlay_axis_wait_neutral
			and main._slide_canvas_overlay_poll_neutral_frames == 0)
	_slide_reset_run_state()


func _slide_layout_contract(slide: SlideRaceGame) -> Dictionary:
	var surface: Node2D = slide.stage_root()
	var snapshot: Dictionary = slide.audit_snapshot()
	if surface == null:
		return {}
	var viewport_size: Vector2 = snapshot.get("viewport_size", Vector2.ZERO)
	var viewport_rect := Rect2(Vector2.ZERO, viewport_size)
	var fill := surface.get_node_or_null("OpaqueSkyFill") as ColorRect
	var wash := surface.get_node_or_null("SkyReadabilityWash") as ColorRect
	var trim := surface.get_node_or_null("FishSlideStorybookTrim") as Node2D
	var left_cue := surface.get_node_or_null(
		"PersistentLeftSteerCue") as Node2D
	var right_cue := surface.get_node_or_null(
		"PersistentRightSteerCue") as Node2D
	var play := surface.get_node_or_null("FishSlideResponsiveStage") as Node2D
	if fill == null or wash == null or trim == null or left_cue == null \
			or right_cue == null or play == null:
		return {}
	var slide_sprite := play.get_node_or_null("ApprovedCompactSlide") as Sprite2D
	var friends := play.get_node_or_null(
		"HarperAndFionaProtectedArt") as Sprite2D
	var roshan := play.get_node_or_null("RoshanSliding") as Sprite2D
	var slide_rect: Rect2 = snapshot.get("slide_rect", Rect2())
	var friends_rect: Rect2 = snapshot.get("friends_rect", Rect2())
	var roshan_point: Vector2 = snapshot.get("roshan_point", Vector2.ZERO)
	var fish_points: Array = snapshot.get("fish_points", []) as Array
	var pip_points: Array = snapshot.get("pip_points", []) as Array
	var points_inside := fish_points.size() == 5 and pip_points.size() == 5
	for point_value: Variant in fish_points:
		points_inside = points_inside and viewport_rect.has_point(point_value as Vector2)
	for point_value: Variant in pip_points:
		points_inside = points_inside and viewport_rect.has_point(point_value as Vector2)
	var fish_geometry := fish_points.size() == 5
	for index in range(5):
		var fish := play.get_node_or_null("Clownfish%d" % index) as Sprite2D
		var fish_rect: Rect2 = _slide_sprite_rect(fish)
		var fish_center: Vector2 = fish_rect.get_center()
		var declared_fish_center: Vector2 = fish_points[index] as Vector2 \
			if index < fish_points.size() else Vector2(-99.0, -99.0)
		fish_geometry = fish_geometry and fish != null and fish_rect.has_area() \
			and viewport_rect.encloses(fish_rect) \
			and fish_center.distance_to(declared_fish_center) <= 1.5
	var trim_band_top: float = float(snapshot.get("trim_band_top", -1.0))
	var trim_scale: float = float(trim.get("stage_scale"))
	var pip_geometry := trim_band_top >= 0.0 and trim_scale > 0.0 \
		and pip_points.size() == 5
	for index in range(5):
		var pip := play.get_node_or_null(
			"FishProgressPip%d" % index) as Sprite2D
		var pip_rect: Rect2 = _slide_sprite_rect(pip)
		var pip_center: Vector2 = pip_rect.get_center()
		var declared_center: Vector2 = pip_points[index] as Vector2 \
			if index < pip_points.size() else Vector2(-99.0, -99.0)
		pip_geometry = pip_geometry and pip != null and pip_rect.has_area() \
			and viewport_rect.encloses(pip_rect) \
			and pip_rect.position.y >= trim_band_top + 11.0 * trim_scale \
			and absf(pip_center.y - (trim_band_top + 40.0 * trim_scale)) \
				<= 1.5 \
			and pip_center.distance_to(declared_center) <= 1.5
	var actual_slide_rect: Rect2 = _slide_sprite_rect(slide_sprite)
	var actual_friends_rect: Rect2 = _slide_sprite_rect(friends)
	var actual_roshan_rect: Rect2 = _slide_sprite_rect(roshan)
	var actors := (
		slide_rect.has_area() and friends_rect.has_area()
		and actual_slide_rect.has_area() and actual_friends_rect.has_area()
		and actual_roshan_rect.has_area()
		and viewport_rect.encloses(actual_slide_rect)
		and viewport_rect.encloses(actual_friends_rect)
		and viewport_rect.encloses(actual_roshan_rect)
		and _slide_rect_approximately_equal(actual_slide_rect, slide_rect)
		and _slide_rect_approximately_equal(actual_friends_rect, friends_rect)
		and viewport_rect.has_point(roshan_point)
		and actual_roshan_rect.has_point(roshan_point)
	)
	var steer_cues_exact: bool = _slide_steer_cue_contract(
		slide, surface, snapshot)
	var z_order := _melody_effective_z(fill) == -100 \
		and _melody_effective_z(
			surface.get_node("SkyLagoonCenterTilesCommonTransform")) == -90 \
		and _melody_effective_z(wash) == -80 \
		and _melody_effective_z(trim) == 4 \
		and _melody_effective_z(slide_sprite) == 12 \
		and _melody_effective_z(friends) == 14 \
		and _melody_effective_z(roshan) == 24 \
		and _melody_effective_z(left_cue) == 30 \
		and _melody_effective_z(right_cue) == 30
	var opaque: bool = fill.color.a >= 1.0 and fill.modulate.a >= 0.98 \
		and fill.position.is_zero_approx() \
		and fill.size.is_equal_approx(viewport_size) \
		and snapshot.get("touch_hit_rect", Rect2()) == viewport_rect
	var resources: Dictionary = _slide_runtime_resource_contract(slide, surface)
	var sprite_texture_coverage: float = \
		_slide_visible_sprite_texture_coverage_screens(
		surface, viewport_rect)
	var full_screen_color_rects_exact: bool = \
		_slide_full_screen_color_rect_contract(surface, viewport_rect)
	# This is a conservative Canvas painter estimate, not measured GPU overdraw:
	# visible Sprite2D texture rectangles plus the two exact full-screen paints.
	# A native Mobile capture remains authoritative for fill rate and FPS.
	var canvas_painter_screens: float = sprite_texture_coverage + 2.0
	var layer_census: Dictionary = _slide_canvas_layer_census(slide)
	return {
		"viewport": viewport_size,
		"opaque": opaque,
		"actors": actors,
		"progress": points_inside and fish_geometry and steer_cues_exact,
		"trim": pip_geometry and trim_band_top < viewport_size.y,
		"z_order": z_order,
		"tiles": _slide_runtime_tile_contract(surface, snapshot),
		"resources": bool(resources.get("exact", false))
			and bool(resources.get("fish_reused", false))
			and int(resources.get("decoded_bytes", 0)) <= 24 * 1024 * 1024,
		"sprite_texture_coverage_bounded": sprite_texture_coverage >= 1.0
			and sprite_texture_coverage <= 1.75,
		"visible_sprite_texture_coverage_screens": sprite_texture_coverage,
		"full_screen_color_rects_exact": full_screen_color_rects_exact,
		"canvas_painter_estimate_exact": full_screen_color_rects_exact
			and is_equal_approx(canvas_painter_screens,
				sprite_texture_coverage + 2.0)
			and canvas_painter_screens >= 3.0
			and canvas_painter_screens <= 3.75,
		"estimated_canvas_painter_screens": canvas_painter_screens,
		"layers": bool(layer_census.get("exact", false))
			and _slide_collection_suppressed(),
		"camera_null": main.active_viewport_camera() == null,
		"_diag_points_inside": points_inside,
		"_diag_fish_geometry": fish_geometry,
		"_diag_steer_cues": steer_cues_exact,
		"_diag_pip_geometry": pip_geometry,
	}


func _slide_rect_approximately_equal(a: Rect2, b: Rect2,
		tolerance: float = 9.0) -> bool:
	return a.position.distance_to(b.position) <= tolerance \
		and a.size.distance_to(b.size) <= tolerance


func _slide_fade_cover_contract(slide: SlideRaceGame,
		expected_size: Vector2i, expect_black: bool) -> bool:
	var rect := main.fade_rect as ColorRect
	var fish_layer: CanvasLayer = slide.active_layer()
	if rect == null or fish_layer == null:
		return false
	var fade_layer := rect.get_parent() as CanvasLayer
	if fade_layer == null:
		return false
	var viewport_rect := Rect2(Vector2.ZERO, Vector2(expected_size))
	var state_exact: bool
	if expect_black:
		state_exact = rect.modulate.a >= 0.98 \
			and rect.mouse_filter == Control.MOUSE_FILTER_STOP
	else:
		state_exact = rect.modulate.a <= 0.02 \
			and rect.mouse_filter == Control.MOUSE_FILTER_IGNORE
	return get_root().size == expected_size \
		and rect.visible and rect.is_visible_in_tree() \
		and rect.color == Color.BLACK and state_exact \
		and is_zero_approx(rect.anchor_left) \
		and is_zero_approx(rect.anchor_top) \
		and is_equal_approx(rect.anchor_right, 1.0) \
		and is_equal_approx(rect.anchor_bottom, 1.0) \
		and is_zero_approx(rect.offset_left) \
		and is_zero_approx(rect.offset_top) \
		and is_zero_approx(rect.offset_right) \
		and is_zero_approx(rect.offset_bottom) \
		and _slide_rect_approximately_equal(
			rect.get_global_rect(), viewport_rect, 0.01) \
		and fade_layer.visible and fade_layer.layer == 30 \
		and fish_layer.visible and fish_layer.layer == SlideRaceGame.FISH_CANVAS_LAYER \
		and fade_layer.layer > fish_layer.layer


func _slide_pip_fill_states_contract(slide: SlideRaceGame) -> bool:
	var surface: Node2D = slide.stage_root()
	if surface == null:
		return false
	var play := surface.get_node_or_null("FishSlideResponsiveStage") as Node2D
	var trim := surface.get_node_or_null("FishSlideStorybookTrim") as Node2D
	if play == null or trim == null:
		return false
	var original_flags: Array = (main.g.get(
		"canvas_fish_got", []) as Array).duplicate()
	var original_got: int = int(main.g.get("got", 0))
	var exact := true
	for filled_value: Variant in [false, true]:
		var filled := bool(filled_value)
		main.g["canvas_fish_got"] = [filled, filled, filled, filled, filled]
		main.g["got"] = 5 if filled else 0
		slide._refresh_canvas_fish()
		var snapshot: Dictionary = slide.audit_snapshot()
		var band_top: float = float(snapshot.get("trim_band_top", -1.0))
		var stage_scale: float = float(trim.get("stage_scale"))
		var pip_points: Array = snapshot.get("pip_points", []) as Array
		var expected_alpha := 1.0 if filled else 0.52
		var expected_local_scale := 0.22 if filled else 0.18
		exact = exact and band_top >= 0.0 and stage_scale > 0.0 \
			and pip_points.size() == 5
		for index in range(5):
			var pip := play.get_node_or_null(
				"FishProgressPip%d" % index) as Sprite2D
			var rect: Rect2 = _slide_sprite_rect(pip)
			var declared_center: Vector2 = pip_points[index] as Vector2 \
				if index < pip_points.size() else Vector2(-99.0, -99.0)
			exact = exact and pip != null and rect.has_area() \
				and rect.get_center().distance_to(declared_center) <= 1.5 \
				and absf(rect.get_center().y \
					- (band_top + 40.0 * stage_scale)) <= 1.5 \
				and rect.position.y >= band_top + 11.0 * stage_scale \
				and pip.scale.is_equal_approx(
					Vector2.ONE * expected_local_scale) \
				and is_equal_approx(pip.modulate.a, expected_alpha) \
				and pip.self_modulate.a >= 0.99
	main.g["canvas_fish_got"] = original_flags
	main.g["got"] = original_got
	slide._refresh_canvas_fish()
	return exact


func _slide_roshan_pose_envelope_contract(slide: SlideRaceGame) -> bool:
	var surface: Node2D = slide.stage_root()
	if surface == null:
		return false
	var play := surface.get_node_or_null("FishSlideResponsiveStage") as Node2D
	var roshan := play.get_node_or_null("RoshanSliding") as Sprite2D \
		if play != null else null
	var finish_slide := play.get_node_or_null(
		"ApprovedCompactSlide") as Sprite2D if play != null else null
	var right_cue := surface.get_node_or_null(
		"PersistentRightSteerCue") as Node2D
	if roshan == null or finish_slide == null or right_cue == null:
		return false
	var viewport_size: Vector2 = slide.audit_snapshot().get(
		"viewport_size", Vector2.ZERO)
	var viewport_rect := Rect2(Vector2.ZERO, viewport_size)
	var original_t: float = float(main.g.get("t", 0.0))
	var original_start: float = float(main.g.get(
		"canvas_run_start_t", original_t))
	var original_lane: float = float(main.g.get("canvas_lane", 0.0))
	var original_velocity: float = float(main.g.get(
		"canvas_lane_velocity", 0.0))
	var late_step: int = ceili(original_t * 4.5)
	if late_step % 2 != 0:
		late_step += 1
	var progress := 0.94
	var native_centers: Array[Vector2] = []
	var screen_centers: Array[Vector2] = []
	var finish_slide_rect: Rect2 = _slide_sprite_rect(finish_slide)
	var right_cue_bounds: Rect2 = _slide_cue_screen_rect(right_cue)
	var right_cue_center: Vector2 = _slide_cue_screen_center(right_cue)
	var right_cue_scale: float = float(right_cue.get("cue_scale"))
	var exact := true
	var early_paths_exact := true
	var early_held_exact := true
	var late_frames_exact := true
	var bracket_exact := true
	var cue_edge_exact := true
	var late_details: Array[Dictionary] = []
	var bracket_details: Array[Dictionary] = []
	var cue_details: Array[Dictionary] = []
	# Ladder poses are a one-way authored action: pose 0, then pose 1, then the
	# seated 2/3 family. They may never ping-pong with the clock at fixed progress.
	var early_progresses: Array[float] = [0.055, 0.065, 0.115, 0.125]
	var early_expected_paths: Array[String] = [
		SLIDE_ACTOR_PATHS[3], SLIDE_ACTOR_PATHS[4],
		SLIDE_ACTOR_PATHS[4], SLIDE_ACTOR_PATHS[5],
	]
	var fixed_early_time: float = (float(late_step) + 0.05) / 4.5
	for index in range(early_progresses.size()):
		var threshold_progress: float = early_progresses[index]
		main.g["t"] = fixed_early_time
		main.g["canvas_run_start_t"] = fixed_early_time \
			- threshold_progress * SlideRaceGame.FISH_RUN_SECONDS
		main.g["canvas_lane"] = 0.0
		main.g["canvas_lane_velocity"] = 0.0
		slide._refresh_canvas_fish()
		var early_path_exact: bool = roshan.texture != null \
			and roshan.texture.resource_path == early_expected_paths[index]
		early_paths_exact = early_paths_exact and early_path_exact
		exact = exact and early_path_exact
	for index in range(3):
		var held_progress: float = early_progresses[index]
		for held_time: float in [fixed_early_time, fixed_early_time + 0.37]:
			main.g["t"] = held_time
			main.g["canvas_run_start_t"] = held_time \
				- held_progress * SlideRaceGame.FISH_RUN_SECONDS
			slide._refresh_canvas_fish()
			var held_path_exact: bool = roshan.texture != null \
				and roshan.texture.resource_path == early_expected_paths[index]
			early_held_exact = early_held_exact and held_path_exact
			exact = exact and held_path_exact
	for pose_index in range(2):
		var pose_time: float = (float(late_step + pose_index) + 0.05) / 4.5
		main.g["t"] = pose_time
		main.g["canvas_run_start_t"] = pose_time \
			- progress * SlideRaceGame.FISH_RUN_SECONDS
		main.g["canvas_lane"] = 0.0
		main.g["canvas_lane_velocity"] = 0.0
		slide._refresh_canvas_fish()
		var texture: Texture2D = roshan.texture
		var used: Rect2i = _slide_texture_alpha_used_rect(texture)
		var texture_size: Vector2 = texture.get_size() \
			if texture != null else Vector2.ZERO
		var alpha_local := Rect2(
			Vector2(used.position) - texture_size * 0.5,
			Vector2(used.size))
		var alpha_screen: Rect2 = _melody_transform_rect(
			alpha_local, roshan.get_global_transform_with_canvas())
		var full_screen: Rect2 = _slide_sprite_rect(roshan)
		var snapshot: Dictionary = slide.audit_snapshot()
		var declared_point: Vector2 = snapshot.get(
			"roshan_point", Vector2(-99.0, -99.0))
		var late_frame_exact: bool = texture != null \
			and texture.resource_path == SLIDE_ACTOR_PATHS[5 + pose_index] \
			and used.has_area() and alpha_screen.has_area() \
			and full_screen.has_area() \
			and viewport_rect.encloses(full_screen) \
			and viewport_rect.encloses(alpha_screen) \
			and finish_slide_rect.grow(2.0).encloses(alpha_screen) \
			and full_screen.has_point(declared_point)
		late_frames_exact = late_frames_exact and late_frame_exact
		exact = exact and late_frame_exact
		late_details.append({
			"pose": pose_index,
			"path": texture.resource_path if texture != null else "<null>",
			"used": used,
			"alpha": alpha_screen,
			"full": full_screen,
			"slide": finish_slide_rect,
			"point": declared_point,
			"exact": late_frame_exact,
		})
		native_centers.append(Vector2(used.get_center()))
		screen_centers.append(alpha_screen.get_center())
	# The old implementation changed back to ladder poses at .90. Hold the same
	# two late-frame clock phases immediately before and after that retired seam:
	# both sides must remain in the seated lip/chute family with only continuous
	# course motion, never a semantic texture-family jump.
	for pose_index in range(2):
		var pose_time: float = (float(late_step + pose_index) + 0.05) / 4.5
		var bracket_points: Array[Vector2] = []
		var bracket_alpha_centers: Array[Vector2] = []
		for threshold_progress: float in [0.895, 0.905]:
			main.g["t"] = pose_time
			main.g["canvas_run_start_t"] = pose_time \
				- threshold_progress * SlideRaceGame.FISH_RUN_SECONDS
			main.g["canvas_lane"] = 0.0
			main.g["canvas_lane_velocity"] = 0.0
			slide._refresh_canvas_fish()
			var texture: Texture2D = roshan.texture
			var used: Rect2i = _slide_texture_alpha_used_rect(texture)
			var texture_size: Vector2 = texture.get_size() \
				if texture != null else Vector2.ZERO
			var alpha_local := Rect2(
				Vector2(used.position) - texture_size * 0.5,
				Vector2(used.size))
			var alpha_screen: Rect2 = _melody_transform_rect(
				alpha_local, roshan.get_global_transform_with_canvas())
			var full_screen: Rect2 = _slide_sprite_rect(roshan)
			var point: Vector2 = slide.audit_snapshot().get(
				"roshan_point", Vector2(-99.0, -99.0))
			var bracket_frame_exact: bool = texture != null \
				and texture.resource_path == SLIDE_ACTOR_PATHS[5 + pose_index] \
				and used.has_area() and alpha_screen.has_area() \
				and viewport_rect.encloses(full_screen) \
				and viewport_rect.encloses(alpha_screen) \
				and finish_slide_rect.grow(2.0).encloses(alpha_screen) \
				and full_screen.has_point(point)
			bracket_exact = bracket_exact and bracket_frame_exact
			exact = exact and bracket_frame_exact
			bracket_points.append(point)
			bracket_alpha_centers.append(alpha_screen.get_center())
		var bracket_shift_exact: bool = bracket_points.size() == 2 \
			and bracket_points[0].distance_to(bracket_points[1]) <= 8.0 \
			and bracket_alpha_centers.size() == 2 \
			and bracket_alpha_centers[0].distance_to(
				bracket_alpha_centers[1]) <= 8.0
		bracket_exact = bracket_exact and bracket_shift_exact
		exact = exact and bracket_shift_exact
		bracket_details.append({
			"pose": pose_index,
			"points": bracket_points,
			"alpha_centers": bracket_alpha_centers,
			"shift_exact": bracket_shift_exact,
		})
	# The right steer cue lives in the clear right margin. HALF_EXTENT includes
	# ten bookkeeping pixels for its outward arrow tip; on the actor-facing side
	# the closest painted shape is the 57px circle. Both seated alpha envelopes
	# must remain horizontally separate from that live painted edge even at +1.
	for lane_value: Variant in [0.0, 1.0]:
		var overlap_lane := float(lane_value)
		for pose_index in range(2):
			var pose_time: float = (float(late_step + pose_index) + 0.05) / 4.5
			main.g["t"] = pose_time
			main.g["canvas_run_start_t"] = pose_time \
				- 0.98 * SlideRaceGame.FISH_RUN_SECONDS
			main.g["canvas_lane"] = overlap_lane
			main.g["canvas_lane_velocity"] = 0.0
			slide._refresh_canvas_fish()
			var texture: Texture2D = roshan.texture
			var used: Rect2i = _slide_texture_alpha_used_rect(texture)
			var texture_size: Vector2 = texture.get_size() \
				if texture != null else Vector2.ZERO
			var alpha_local := Rect2(
				Vector2(used.position) - texture_size * 0.5,
				Vector2(used.size))
			var alpha_screen: Rect2 = _melody_transform_rect(
				alpha_local, roshan.get_global_transform_with_canvas())
			var cue_frame_exact: bool = right_cue_bounds.has_area() \
				and right_cue_scale > 0.0 \
				and texture != null and used.has_area() \
				and texture.resource_path \
					== SLIDE_ACTOR_PATHS[5 + pose_index] \
				and viewport_rect.encloses(alpha_screen) \
				and alpha_screen.end.x \
					< right_cue_center.x - 57.0 * right_cue_scale
			cue_edge_exact = cue_edge_exact and cue_frame_exact
			exact = exact and cue_frame_exact
			cue_details.append({
				"lane": overlap_lane,
				"pose": pose_index,
				"alpha_end_x": alpha_screen.end.x,
				"paint_edge_x": right_cue_center.x - 57.0 * right_cue_scale,
				"exact": cue_frame_exact,
			})
	main.g["t"] = original_t
	main.g["canvas_run_start_t"] = original_start
	main.g["canvas_lane"] = original_lane
	main.g["canvas_lane_velocity"] = original_velocity
	slide._refresh_canvas_fish()
	var stage_scale: float = viewport_size.x / 1280.0
	var native_shift: float = native_centers[0].distance_to(native_centers[1]) \
		if native_centers.size() == 2 else -1.0
	var screen_shift: float = screen_centers[0].distance_to(screen_centers[1]) \
		if screen_centers.size() == 2 else -1.0
	var shifts_exact: bool = native_shift >= 0.0 and native_shift <= 40.0 \
		and screen_shift >= 0.0 and screen_shift <= 15.0 * stage_scale
	var final_exact: bool = exact and shifts_exact
	if not final_exact:
		print(("SLIDE_DIAG|roshan|early=%s|held=%s|late=%s|bracket=%s" \
			+ "|cue=%s|shifts=%s|native_shift=%.4f|screen_shift=%.4f" \
			+ "|stage_scale=%.4f|late_details=%s|bracket_details=%s" \
			+ "|cue_details=%s") % [
			early_paths_exact, early_held_exact, late_frames_exact,
			bracket_exact, cue_edge_exact, shifts_exact, native_shift,
			screen_shift, stage_scale, late_details, bracket_details,
			cue_details,
		])
	return final_exact


func _slide_check_tick_once(slide: SlideRaceGame) -> void:
	_slide_reset_run_state()
	await process_frame
	var before: Dictionary = slide.audit_snapshot()
	var tick_before: int = int(before.get("tick_count", -1))
	var progress_before: float = float(before.get("progress", -1.0))
	var game_before: float = float(main.g.get("t", -1.0))
	await process_frame
	var after: Dictionary = slide.audit_snapshot()
	var tick_after: int = int(after.get("tick_count", -1))
	var progress_after: float = float(after.get("progress", -1.0))
	var game_after: float = float(main.g.get("t", -1.0))
	var game_delta: float = game_after - game_before
	var motion_delta: float = (progress_after - progress_before) \
		* SlideRaceGame.FISH_RUN_SECONDS
	_slide_check("one rendered frame produces exactly one fish controller tick",
		tick_before >= 0 and tick_after == tick_before + 1)
	_slide_check("ranking clock and slide motion consume the same delta once",
		game_delta > 0.0 and motion_delta > 0.0
		and is_equal_approx(game_delta, motion_delta))
	_slide_reset_run_state()


func _slide_reset_run_state() -> void:
	if main.game != "slide" or String(main.g.get("mode", "")) != "fish":
		return
	main.g["canvas_run_start_t"] = float(main.g.get("t", 0.0))
	main.g["canvas_lane"] = 0.0
	main.g["canvas_lane_velocity"] = 0.0
	main.g["canvas_fish_got"] = [false, false, false, false, false]
	main.g["got"] = 0
	main.g["steered"] = false


func _slide_cue_active_state(slide: SlideRaceGame) -> Vector2i:
	var surface: Node2D = slide.stage_root()
	if surface == null:
		return Vector2i(-1, -1)
	var left := surface.get_node_or_null("PersistentLeftSteerCue") as Node2D
	var right := surface.get_node_or_null("PersistentRightSteerCue") as Node2D
	if left == null or right == null:
		return Vector2i(-1, -1)
	return Vector2i(1 if bool(left.get("cue_active")) else 0,
		1 if bool(right.get("cue_active")) else 0)


func _slide_exercise_dual_steer_cues(slide: SlideRaceGame) -> void:
	_slide_reset_run_state()
	await process_frame
	var surface: Node2D = slide.stage_root()
	var snapshot: Dictionary = slide.audit_snapshot()
	var left := surface.get_node_or_null(
		"PersistentLeftSteerCue") as Node2D if surface != null else null
	var right := surface.get_node_or_null(
		"PersistentRightSteerCue") as Node2D if surface != null else null
	if left == null or right == null:
		_slide_check("dual steer cue behavior fixture finds both live renderers", false)
		return
	var left_tip: Vector2 = _slide_cue_screen_tip(left)
	var right_tip: Vector2 = _slide_cue_screen_tip(right)
	var left_lane_before: float = float(snapshot.get("lane", 0.0))
	_slide_push_touch(left_tip, true, SLIDE_TOUCH_INDEX + 300, 111)
	var left_pressed: Dictionary = slide.audit_snapshot()
	var left_immediate: bool = _slide_cue_active_state(slide) == Vector2i(1, 0) \
		and float(left_pressed.get("combined_steer", 0.0)) < 0.0 \
		and (left_pressed.get("input_sources", {}) as Dictionary).has(
			&"touch:111:391")
	await _frames(3)
	var left_lane_after: float = float(slide.audit_snapshot().get("lane", 0.0))
	_slide_push_touch(left_tip, false, SLIDE_TOUCH_INDEX + 300, 111)
	var left_released: bool = _slide_cue_active_state(slide) == Vector2i.ZERO \
		and _slide_owner_tokens(slide.audit_snapshot()).is_empty()
	_slide_reset_run_state()
	await process_frame
	right_tip = _slide_cue_screen_tip(right)
	var right_lane_before: float = float(slide.audit_snapshot().get("lane", 0.0))
	_slide_push_touch(right_tip, true, SLIDE_TOUCH_INDEX + 301, 112)
	var right_pressed: Dictionary = slide.audit_snapshot()
	var right_immediate: bool = _slide_cue_active_state(slide) == Vector2i(0, 1) \
		and float(right_pressed.get("combined_steer", 0.0)) > 0.0 \
		and (right_pressed.get("input_sources", {}) as Dictionary).has(
			&"touch:112:392")
	await _frames(3)
	var right_lane_after: float = float(slide.audit_snapshot().get("lane", 0.0))
	_slide_push_touch(right_tip, false, SLIDE_TOUCH_INDEX + 301, 112)
	var right_released: bool = _slide_cue_active_state(slide) == Vector2i.ZERO \
		and _slide_owner_tokens(slide.audit_snapshot()).is_empty()
	_slide_check("real Viewport presses at each actual outward tip light only that cue",
		left_immediate and right_immediate
		and float(slide.call("_touch_axis", left_tip)) < 0.0
		and float(slide.call("_touch_axis", right_tip)) > 0.0)
	_slide_check("tip steering moves the lane in its matching direction and releases neutrally",
		left_lane_after < left_lane_before and right_lane_after > right_lane_before
		and left_released and right_released)

	# A device disappearance and an explicit controller cancellation must both
	# clear the renderer synchronously, not merely clear snapshot bookkeeping.
	_slide_push_pad(JOY_BUTTON_DPAD_LEFT, true, 113)
	var device_left_live: bool = _slide_cue_active_state(slide) == Vector2i(1, 0)
	main._forget_slide_canvas_pad_device(113)
	var device_clear: bool = _slide_cue_active_state(slide) == Vector2i.ZERO
	_slide_push_pad(JOY_BUTTON_DPAD_LEFT, false, 113)
	_slide_push_key(KEY_RIGHT, true, 114)
	var cancel_right_live: bool = _slide_cue_active_state(slide) == Vector2i(0, 1)
	slide.cancel_input()
	var cancel_clear: bool = _slide_cue_active_state(slide) == Vector2i.ZERO
	_slide_push_key(KEY_RIGHT, false, 114)
	await process_frame
	var source_free_clear: bool = _slide_cue_active_state(slide) \
		== Vector2i.ZERO
	_slide_check("device forget and controller cancel clear active cue pixels immediately",
		device_left_live and device_clear and cancel_right_live and cancel_clear
		and source_free_clear)
	_slide_reset_run_state()


func _slide_exercise_source_ownership(slide: SlideRaceGame) -> void:
	_slide_reset_run_state()
	await process_frame
	var touch_point := Vector2(180.0, 430.0)
	var mouse_point := Vector2(1100.0, 430.0)
	_slide_push_touch(touch_point, true, SLIDE_TOUCH_INDEX + 10, 11)
	_slide_push_mouse(mouse_point, true, 12)
	_slide_push_key(KEY_LEFT, true, 13)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, true, 14)
	_slide_push_axis(0.72, 15)
	var snapshot: Dictionary = slide.audit_snapshot()
	var expected: Dictionary = {
		&"touch:11:101": true,
		&"mouse:12:left": true,
		StringName("key:13:%d" % KEY_LEFT): true,
		StringName("pad:14:%d" % JOY_BUTTON_DPAD_RIGHT): true,
		StringName("pad:15:axis:%d" % JOY_AXIS_LEFT_X): true,
	}
	_slide_check("real touch, mouse, key, pad, and axis own distinct sources",
		_slide_owner_tokens(snapshot) == expected
		and main._slide_canvas_held_sources == expected
		and bool(main.g.get("steered", false)))
	_slide_push_touch(touch_point, false, SLIDE_TOUCH_INDEX + 10, 99)
	_slide_push_mouse(mouse_point, false, 99)
	_slide_push_key(KEY_LEFT, false, 99)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, false, 99)
	_slide_push_axis(0.0, 99)
	snapshot = slide.audit_snapshot()
	_slide_check("wrong-device releases cannot retire any concrete owner",
		_slide_owner_tokens(snapshot) == expected)
	main._forget_slide_canvas_pad_device(14)
	expected.erase(StringName("pad:14:%d" % JOY_BUTTON_DPAD_RIGHT))
	snapshot = slide.audit_snapshot()
	_slide_check("pad disconnect retires only that device's concrete owners",
		_slide_owner_tokens(snapshot) == expected
		and not main._slide_canvas_held_sources.has(
			StringName("pad:14:%d" % JOY_BUTTON_DPAD_RIGHT)))
	_slide_push_touch(touch_point, false, SLIDE_TOUCH_INDEX + 10, 11)
	_slide_push_mouse(mouse_point, false, 12)
	_slide_push_key(KEY_LEFT, false, 13)
	_slide_push_axis(0.0, 15)
	await process_frame
	snapshot = slide.audit_snapshot()
	_slide_check("matching releases clear every controller and global owner",
		_slide_owner_tokens(snapshot).is_empty()
		and main._slide_canvas_held_sources.is_empty()
		and not bool(snapshot.get("blocked_until_release", true)))
	var lane_before: float = float(snapshot.get("lane", 0.0))
	_slide_push_key(KEY_RIGHT, true, 16)
	await _frames(3)
	_slide_push_key(KEY_RIGHT, false, 16)
	var lane_after: float = float(slide.audit_snapshot().get("lane", 0.0))
	_slide_check("fresh distinct input deliberately steers after census cleanup",
		lane_after > lane_before and bool(main.g.get("steered", false)))
	_slide_reset_run_state()


func _slide_owner_tokens(snapshot: Dictionary) -> Dictionary:
	var owners: Dictionary = {}
	for value: Variant in (snapshot.get("input_sources", {}) as Dictionary).keys():
		owners[StringName(String(value))] = true
	for value: Variant in (snapshot.get("blocked_sources", {}) as Dictionary).keys():
		owners[StringName(String(value))] = true
	return owners


func _slide_seed_unmapped_pad(device: int, axis_value: float,
		button: JoyButton) -> bool:
	main.joy_ev_axis.clear()
	main.joy_ev_btn.clear()
	main.joy_has_unmapped = true
	_slide_push_axis(axis_value, device)
	_slide_push_pad(button, true, device)
	return is_equal_approx(main.joy_axis(JOY_AXIS_LEFT_X), axis_value) \
		and main.joy_pressed(button) \
		and is_equal_approx(float(main.joy_ev_axis.get(
			int(JOY_AXIS_LEFT_X), 0.0)), axis_value) \
		and bool(main.joy_ev_btn.get(int(button), false))


func _slide_raw_pad_neutral(button: JoyButton) -> bool:
	return main.joy_ev_axis.is_empty() and main.joy_ev_btn.is_empty() \
		and is_zero_approx(main.joy_axis(JOY_AXIS_LEFT_X)) \
		and is_zero_approx(main.joy_axis(JOY_AXIS_RIGHT_X)) \
		and not main.joy_pressed(button) \
		and not main.joy_pressed(JOY_BUTTON_A)


func _slide_raw_pad_values_neutral(button: JoyButton) -> bool:
	# Claimed terminal events are mirrored into the legacy fallback before Main
	# returns, so neutral 0.0/false entries are expected here. Dictionary
	# emptiness belongs only to entry-before-terminal and teardown retirement.
	var exact := true
	for axis_value: Variant in main.joy_ev_axis.values():
		exact = exact and absf(float(axis_value)) <= 0.18
	for button_value: Variant in main.joy_ev_btn.values():
		exact = exact and not bool(button_value)
	for axis: JoyAxis in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y,
			JOY_AXIS_RIGHT_X, JOY_AXIS_RIGHT_Y]:
		exact = exact and absf(main.joy_axis(axis)) <= 0.18
	return exact and not main.joy_pressed(button) \
		and not main.joy_pressed(JOY_BUTTON_A)


func _slide_unclaimed_raw_pad_live(axis_value: float) -> bool:
	return is_equal_approx(float(main.joy_ev_axis.get(
		int(JOY_AXIS_RIGHT_X), 0.0)), axis_value) \
		and bool(main.joy_ev_btn.get(int(JOY_BUTTON_A), false)) \
		and is_equal_approx(main.joy_axis(JOY_AXIS_RIGHT_X), axis_value) \
		and main.joy_pressed(JOY_BUTTON_A)


func _slide_push_touch(position: Vector2, pressed: bool, index: int,
		device: int = 0, canceled: bool = false) -> void:
	var event := InputEventScreenTouch.new()
	event.device = device
	event.index = index
	event.position = position
	event.pressed = pressed
	event.canceled = canceled
	main.get_viewport().push_input(event, false)


func _slide_push_drag(position: Vector2, relative: Vector2, index: int,
		device: int = 0) -> void:
	var event := InputEventScreenDrag.new()
	event.device = device
	event.index = index
	event.position = position
	event.relative = relative
	main.get_viewport().push_input(event, false)


func _slide_push_mouse(position: Vector2, pressed: bool,
		device: int = 0, canceled: bool = false) -> void:
	_slide_push_mouse_button(position, MOUSE_BUTTON_LEFT, pressed,
		device, canceled)


func _slide_push_mouse_button(position: Vector2, button: MouseButton,
		pressed: bool, device: int = 0, canceled: bool = false) -> void:
	var event := InputEventMouseButton.new()
	event.device = device
	event.button_index = button
	event.position = position
	event.pressed = pressed
	event.canceled = canceled
	main.get_viewport().push_input(event, false)


func _slide_push_mouse_drag(position: Vector2, relative: Vector2,
		device: int = 0) -> void:
	var event := InputEventMouseMotion.new()
	event.device = device
	event.position = position
	event.relative = relative
	event.button_mask = MOUSE_BUTTON_MASK_LEFT
	main.get_viewport().push_input(event, false)


func _slide_push_mouse_look(relative: Vector2, device: int = 0) -> void:
	var event := InputEventMouseMotion.new()
	event.device = device
	event.position = Vector2(640.0, 360.0)
	event.relative = relative
	event.button_mask = MOUSE_BUTTON_MASK_RIGHT
	Input.parse_input_event(event)


func _slide_parse_mouse_button(position: Vector2, button: MouseButton,
		pressed: bool, device: int = 0) -> void:
	var event := InputEventMouseButton.new()
	event.device = device
	event.button_index = button
	event.position = position
	event.pressed = pressed
	event.button_mask = (MOUSE_BUTTON_MASK_RIGHT \
		if button == MOUSE_BUTTON_RIGHT and pressed else 0)
	Input.parse_input_event(event)


func _slide_push_key(keycode: Key, pressed: bool, device: int = 0) -> void:
	var event := InputEventKey.new()
	event.device = device
	event.keycode = keycode
	event.physical_keycode = keycode
	event.pressed = pressed
	main.get_viewport().push_input(event, false)


func _slide_push_pad(button: JoyButton, pressed: bool,
		device: int = 0) -> void:
	var event := InputEventJoypadButton.new()
	event.device = device
	event.button_index = button
	event.pressed = pressed
	main.get_viewport().push_input(event, false)


func _slide_push_axis(value: float, device: int = 0) -> void:
	_slide_push_axis_for(JOY_AXIS_LEFT_X, value, device)


func _slide_push_axis_for(axis: JoyAxis, value: float,
		device: int = 0) -> void:
	var event := InputEventJoypadMotion.new()
	event.device = device
	event.axis = axis
	event.axis_value = value
	main.get_viewport().push_input(event, false)


func _slide_push_action(action: StringName, pressed: bool) -> void:
	var event := InputEventAction.new()
	event.action = action
	event.pressed = pressed
	main.get_viewport().push_input(event, false)


func _slide_set_return_nonpointer_holds(pressed: bool, device: int) -> void:
	for axis: JoyAxis in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y,
			JOY_AXIS_RIGHT_X, JOY_AXIS_RIGHT_Y]:
		_slide_push_axis_for(axis,
			SLIDE_RETURN_AXIS_VALUES[int(axis)] if pressed else 0.0, device)
	for button: JoyButton in [JOY_BUTTON_A, JOY_BUTTON_B,
			JOY_BUTTON_X, JOY_BUTTON_Y,
			JOY_BUTTON_DPAD_UP, JOY_BUTTON_DPAD_DOWN,
			JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT]:
		_slide_push_pad(button, pressed, device)
	for key_code: Key in [KEY_W, KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
		_slide_push_key(key_code, pressed, device)
	_slide_push_mouse_button(Vector2(980.0, 500.0), MOUSE_BUTTON_RIGHT,
		pressed, device)


func _slide_retire_return_holds_exact(expected_sources: Dictionary,
		touch_point: Vector2, touch_index: int, touch_device: int,
		pad_device: int) -> bool:
	var exact: bool = main._slide_canvas_return_held_sources == expected_sources
	# A disconnected second pad may retire only its own exact prefix.
	var auxiliary_device: int = pad_device + 400
	_slide_push_pad(JOY_BUTTON_A, true, auxiliary_device)
	var expected_with_aux: Dictionary = expected_sources.duplicate()
	var auxiliary_token := StringName("return:pad:%d:button:%d" % [
		auxiliary_device, JOY_BUTTON_A])
	expected_with_aux[auxiliary_token] = true
	exact = exact and main._slide_canvas_return_held_sources == expected_with_aux
	main._forget_slide_canvas_pad_device(auxiliary_device)
	exact = exact and main._slide_canvas_return_held_sources == expected_sources \
		and bool(main.call("_slide_canvas_return_guard_active"))

	var remaining: Dictionary = expected_sources.duplicate()
	for axis: JoyAxis in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y,
			JOY_AXIS_RIGHT_X, JOY_AXIS_RIGHT_Y]:
		_slide_push_axis_for(axis, 0.0, pad_device)
		remaining.erase(StringName("return:pad:%d:axis:%d" % [
			pad_device, axis]))
	exact = exact and main._slide_canvas_return_held_sources == remaining \
		and bool(main.call("_slide_canvas_return_guard_active"))
	for button: JoyButton in [JOY_BUTTON_A, JOY_BUTTON_B,
			JOY_BUTTON_X, JOY_BUTTON_Y,
			JOY_BUTTON_DPAD_UP, JOY_BUTTON_DPAD_DOWN,
			JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT]:
		_slide_push_pad(button, false, pad_device)
		remaining.erase(StringName("return:pad:%d:button:%d" % [
			pad_device, button]))
	exact = exact and main._slide_canvas_return_held_sources == remaining \
		and bool(main.call("_slide_canvas_return_guard_active"))
	for key_code: Key in [KEY_W, KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
		_slide_push_key(key_code, false, pad_device)
		remaining.erase(StringName("return:key:%d:%d" % [
			pad_device, key_code]))
	_slide_push_mouse_button(Vector2(980.0, 500.0), MOUSE_BUTTON_RIGHT,
		false, pad_device)
	remaining.erase(StringName("return:mouse:%d:%d" % [
		pad_device, MOUSE_BUTTON_RIGHT]))
	exact = exact and main._slide_canvas_return_held_sources == remaining \
		and bool(main.call("_slide_canvas_return_guard_active"))
	# The wrong device cannot retire the final touch owner.
	_slide_push_touch(touch_point, false, touch_index, touch_device + 1)
	exact = exact and main._slide_canvas_return_held_sources == remaining \
		and remaining.size() == 1 \
		and bool(main.call("_slide_canvas_return_guard_active"))
	_slide_push_touch(touch_point, false, touch_index, touch_device)
	remaining.erase(StringName("return:touch:%d:%d" % [
		touch_device, touch_index]))
	return exact and remaining.is_empty() \
		and main._slide_canvas_return_held_sources.is_empty() \
		and main._slide_canvas_held_sources.is_empty() \
		and bool(main.call("_slide_canvas_return_guard_active"))


func _slide_expected_return_sources(touch_index: int, touch_device: int,
		pad_device: int) -> Dictionary:
	var expected: Dictionary = {
		StringName("return:touch:%d:%d" % [touch_device, touch_index]): true,
		StringName("return:mouse:%d:%d" % [pad_device,
			MOUSE_BUTTON_RIGHT]): true,
		StringName("return:key:%d:%d" % [pad_device, KEY_W]): true,
		StringName("return:key:%d:%d" % [pad_device, KEY_SPACE]): true,
		StringName("return:key:%d:%d" % [pad_device, KEY_ENTER]): true,
		StringName("return:key:%d:%d" % [pad_device, KEY_KP_ENTER]): true,
	}
	for axis: JoyAxis in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y,
			JOY_AXIS_RIGHT_X, JOY_AXIS_RIGHT_Y]:
		expected[StringName("return:pad:%d:axis:%d" % [
			pad_device, axis])] = true
	for button: JoyButton in [JOY_BUTTON_A, JOY_BUTTON_B,
			JOY_BUTTON_X, JOY_BUTTON_Y,
			JOY_BUTTON_DPAD_UP, JOY_BUTTON_DPAD_DOWN,
			JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT]:
		expected[StringName("return:pad:%d:button:%d" % [
			pad_device, button])] = true
	return expected


func _slide_expected_precontext_melody_sources(touch_index: int,
		touch_device: int, pad_device: int, full_family: bool) -> Dictionary:
	var expected: Dictionary = {}
	if full_family:
		expected[StringName("touch:%d:%d" % [
			touch_device, touch_index])] = true
		for key_code: Key in [KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
			expected[StringName("key:%d:%d" % [
				pad_device, key_code])] = true
		for button: JoyButton in [JOY_BUTTON_A, JOY_BUTTON_B,
				JOY_BUTTON_X, JOY_BUTTON_Y]:
			expected[StringName("pad:%d:%d" % [
				pad_device, button])] = true
	else:
		# The neutral-Leave route deliberately holds one raw A before teardown;
		# later completion routes hold the complete eight-source family above.
		expected[StringName("pad:%d:%d" % [
			pad_device, JOY_BUTTON_A])] = true
	return expected


func _slide_retire_precontext_melody_holds_exact(
		return_expected: Dictionary, touch_point: Vector2,
		touch_index: int, touch_device: int, pad_device: int,
		full_family: bool) -> bool:
	var melody_remaining: Dictionary = \
		_slide_expected_precontext_melody_sources(touch_index,
			touch_device, pad_device, full_family)
	var return_remaining: Dictionary = return_expected.duplicate()
	var exact: bool = bool(main.call("_slide_canvas_return_guard_active")) \
		and main._melody_held_sources == melody_remaining \
		and main._slide_canvas_return_held_sources == return_remaining

	# Retire every source through the real guard input boundary before any focus
	# or app notification can clear the global Melody census and mask a leak.
	_slide_push_touch(touch_point, false, touch_index, touch_device)
	melody_remaining.erase(StringName("touch:%d:%d" % [
		touch_device, touch_index]))
	return_remaining.erase(StringName("return:touch:%d:%d" % [
		touch_device, touch_index]))
	exact = exact and main._melody_held_sources == melody_remaining \
		and main._slide_canvas_return_held_sources == return_remaining \
		and bool(main.call("_slide_canvas_return_guard_active"))
	for key_code: Key in [KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
		_slide_push_key(key_code, false, pad_device)
		melody_remaining.erase(StringName("key:%d:%d" % [
			pad_device, key_code]))
		return_remaining.erase(StringName("return:key:%d:%d" % [
			pad_device, key_code]))
		exact = exact and main._melody_held_sources == melody_remaining \
			and main._slide_canvas_return_held_sources == return_remaining \
			and bool(main.call("_slide_canvas_return_guard_active"))
	for button: JoyButton in [JOY_BUTTON_A, JOY_BUTTON_B,
			JOY_BUTTON_X, JOY_BUTTON_Y]:
		_slide_push_pad(button, false, pad_device)
		melody_remaining.erase(StringName("pad:%d:%d" % [
			pad_device, button]))
		return_remaining.erase(StringName("return:pad:%d:button:%d" % [
			pad_device, button]))
		exact = exact and main._melody_held_sources == melody_remaining \
			and main._slide_canvas_return_held_sources == return_remaining \
			and bool(main.call("_slide_canvas_return_guard_active"))
	exact = exact and melody_remaining.is_empty() \
		and main._melody_held_sources.is_empty()

	# Re-publish the same physical owners for the remaining fade/context/final
	# retirement proof. Guard presses rebuild only its broad return census; they
	# must never resurrect Melody's now-retired entry-source ledger.
	_slide_push_touch(touch_point, true, touch_index, touch_device)
	for key_code: Key in [KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
		_slide_push_key(key_code, true, pad_device)
	for button: JoyButton in [JOY_BUTTON_A, JOY_BUTTON_B,
			JOY_BUTTON_X, JOY_BUTTON_Y]:
		_slide_push_pad(button, true, pad_device)
	return exact and main._melody_held_sources.is_empty() \
		and main._slide_canvas_return_held_sources == return_expected \
		and bool(main.call("_slide_canvas_return_guard_active"))


func _slide_return_terminal_event(pressed_event: InputEvent,
		device_override: int = -1) -> InputEvent:
	var terminal: InputEvent
	if pressed_event is InputEventScreenTouch \
			or pressed_event is InputEventScreenDrag:
		var touch := InputEventScreenTouch.new()
		touch.index = int(pressed_event.get("index"))
		touch.position = pressed_event.get("position") as Vector2
		touch.pressed = false
		terminal = touch
	elif pressed_event is InputEventMouseButton \
			or pressed_event is InputEventMouseMotion:
		var mouse := InputEventMouseButton.new()
		if pressed_event is InputEventMouseButton:
			mouse.button_index = (pressed_event as InputEventMouseButton).button_index
		else:
			var mask: MouseButtonMask = (
				pressed_event as InputEventMouseMotion).button_mask
			mouse.button_index = MOUSE_BUTTON_LEFT \
				if (mask & MOUSE_BUTTON_MASK_LEFT) != 0 \
				else MOUSE_BUTTON_RIGHT
		mouse.pressed = false
		terminal = mouse
	elif pressed_event is InputEventKey:
		var key := InputEventKey.new()
		key.keycode = (pressed_event as InputEventKey).keycode
		key.physical_keycode = (pressed_event as InputEventKey).physical_keycode
		key.pressed = false
		terminal = key
	elif pressed_event is InputEventJoypadButton:
		var button := InputEventJoypadButton.new()
		button.button_index = (
			pressed_event as InputEventJoypadButton).button_index
		button.pressed = false
		terminal = button
	else:
		var motion := InputEventJoypadMotion.new()
		motion.axis = (pressed_event as InputEventJoypadMotion).axis
		motion.axis_value = 0.0
		terminal = motion
	terminal.device = device_override if device_override >= 0 \
		else pressed_event.device
	return terminal


func _slide_return_source_token_contract() -> bool:
	var cases: Array[Dictionary] = []
	var touch := InputEventScreenTouch.new()
	touch.device = 201
	touch.index = 7
	touch.position = Vector2(220.0, 420.0)
	touch.pressed = true
	cases.append({"event": touch, "token": &"return:touch:201:7"})
	var drag := InputEventScreenDrag.new()
	drag.device = 201
	drag.index = 8
	drag.position = Vector2(260.0, 420.0)
	cases.append({"event": drag, "token": &"return:touch:201:8"})
	for mouse_button: MouseButton in [MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT]:
		var mouse := InputEventMouseButton.new()
		mouse.device = 202
		mouse.button_index = mouse_button
		mouse.pressed = true
		cases.append({
			"event": mouse,
			"token": StringName("return:mouse:202:%d" % mouse_button),
		})
	for mask_value: MouseButtonMask in [MOUSE_BUTTON_MASK_LEFT,
			MOUSE_BUTTON_MASK_RIGHT]:
		var mouse_motion := InputEventMouseMotion.new()
		mouse_motion.device = 202
		mouse_motion.button_mask = mask_value
		var motion_button: MouseButton = MOUSE_BUTTON_LEFT \
			if mask_value == MOUSE_BUTTON_MASK_LEFT else MOUSE_BUTTON_RIGHT
		cases.append({
			"event": mouse_motion,
			"token": StringName("return:mouse:202:%d" % motion_button),
		})
	for key_code: Key in [KEY_W, KEY_A, KEY_S, KEY_D, KEY_UP, KEY_LEFT,
			KEY_DOWN, KEY_RIGHT, KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
		var key := InputEventKey.new()
		key.device = 203
		key.keycode = key_code
		key.physical_keycode = key_code
		key.pressed = true
		cases.append({
			"event": key,
			"token": StringName("return:key:203:%d" % key_code),
		})
	for button: JoyButton in [JOY_BUTTON_A, JOY_BUTTON_B,
			JOY_BUTTON_X, JOY_BUTTON_Y,
			JOY_BUTTON_DPAD_UP, JOY_BUTTON_DPAD_DOWN,
			JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT]:
		var pad := InputEventJoypadButton.new()
		pad.device = 204
		pad.button_index = button
		pad.pressed = true
		cases.append({
			"event": pad,
			"token": StringName("return:pad:204:button:%d" % button),
		})
	for axis: JoyAxis in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y,
			JOY_AXIS_RIGHT_X, JOY_AXIS_RIGHT_Y]:
		var motion := InputEventJoypadMotion.new()
		motion.device = 205
		motion.axis = axis
		motion.axis_value = 0.73
		cases.append({
			"event": motion,
			"token": StringName("return:pad:205:axis:%d" % axis),
		})
	var original_sources: Dictionary = \
		main._slide_canvas_return_held_sources.duplicate()
	main._slide_canvas_return_held_sources.clear()
	var expected_pad_vocabulary: Array[JoyButton] = [
		JOY_BUTTON_A, JOY_BUTTON_B, JOY_BUTTON_X, JOY_BUTTON_Y,
		JOY_BUTTON_DPAD_UP, JOY_BUTTON_DPAD_DOWN,
		JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT,
	]
	var expected_pad_set: Dictionary = {}
	for button: JoyButton in expected_pad_vocabulary:
		expected_pad_set[int(button)] = true
	var actual_pad_set: Dictionary = {}
	for button: JoyButton in ReefMain.SLIDE_CANVAS_RETURN_PAD_BUTTONS:
		actual_pad_set[int(button)] = true
	var expected_key_vocabulary: Array[Key] = [
		KEY_W, KEY_A, KEY_S, KEY_D, KEY_UP, KEY_LEFT, KEY_DOWN, KEY_RIGHT,
		KEY_SPACE, KEY_ENTER, KEY_KP_ENTER,
	]
	var expected_key_set: Dictionary = {}
	for key_code: Key in expected_key_vocabulary:
		expected_key_set[int(key_code)] = true
	var actual_key_set: Dictionary = {}
	for key_code: Key in ReefMain.SLIDE_CANVAS_RETURN_KEYS:
		actual_key_set[int(key_code)] = true
	var exact: bool = cases.size() == 29 \
		and ReefMain.SLIDE_CANVAS_RETURN_PAD_BUTTONS.size() == 8 \
		and actual_pad_set == expected_pad_set \
		and ReefMain.SLIDE_CANVAS_RETURN_KEYS.size() == 11 \
		and actual_key_set == expected_key_set
	for case_value: Dictionary in cases:
		var event: InputEvent = case_value.get("event") as InputEvent
		var expected: StringName = case_value.get("token", &"") as StringName
		exact = exact and event != null \
			and main.call("_slide_canvas_return_source_token", event) == expected
		main.call("_observe_slide_canvas_return_source", event)
		var one_expected: Dictionary = {expected: true}
		exact = exact \
			and main._slide_canvas_return_held_sources == one_expected
		var wrong_terminal: InputEvent = _slide_return_terminal_event(
			event, event.device + 50)
		main.call("_observe_slide_canvas_return_source", wrong_terminal)
		exact = exact \
			and main._slide_canvas_return_held_sources == one_expected
		var terminal: InputEvent = _slide_return_terminal_event(event)
		exact = exact and main.call(
			"_slide_canvas_return_source_token", terminal) == expected
		main.call("_observe_slide_canvas_return_source", terminal)
		exact = exact and main._slide_canvas_return_held_sources.is_empty()
	var negative_cases: Array[InputEvent] = []
	var emulated_mouse := InputEventMouseButton.new()
	emulated_mouse.device = InputEvent.DEVICE_ID_EMULATION
	emulated_mouse.button_index = MOUSE_BUTTON_LEFT
	emulated_mouse.pressed = true
	negative_cases.append(emulated_mouse)
	var middle_mouse := InputEventMouseButton.new()
	middle_mouse.device = 202
	middle_mouse.button_index = MOUSE_BUTTON_MIDDLE
	middle_mouse.pressed = true
	negative_cases.append(middle_mouse)
	var other_key := InputEventKey.new()
	other_key.device = 203
	other_key.keycode = KEY_ESCAPE
	other_key.physical_keycode = KEY_ESCAPE
	other_key.pressed = true
	negative_cases.append(other_key)
	var other_button := InputEventJoypadButton.new()
	other_button.device = 204
	other_button.button_index = JOY_BUTTON_BACK
	other_button.pressed = true
	negative_cases.append(other_button)
	var other_axis := InputEventJoypadMotion.new()
	other_axis.device = 205
	other_axis.axis = JOY_AXIS_TRIGGER_LEFT
	other_axis.axis_value = 0.73
	negative_cases.append(other_axis)
	var action := InputEventAction.new()
	action.action = &"ui_accept"
	action.pressed = true
	negative_cases.append(action)
	for negative: InputEvent in negative_cases:
		exact = exact and StringName(main.call(
			"_slide_canvas_return_source_token", negative)).is_empty()
		main.call("_observe_slide_canvas_return_source", negative)
		exact = exact and main._slide_canvas_return_held_sources.is_empty()
	main._slide_canvas_return_held_sources.merge(original_sources, true)
	return exact


func _slide_return_poll_vocabulary_contract() -> bool:
	var return_before: Dictionary = \
		main._slide_canvas_return_held_sources.duplicate()
	var slide_before: Dictionary = main._slide_canvas_held_sources.duplicate()
	var melody_before: Dictionary = main._melody_held_sources.duplicate()
	var axis_before: Dictionary = main.joy_ev_axis.duplicate()
	var button_before: Dictionary = main.joy_ev_btn.duplicate()
	var joy_unmapped_before: bool = main.joy_has_unmapped
	main._slide_canvas_return_held_sources.clear()
	main._slide_canvas_held_sources.clear()
	main._melody_held_sources.clear()
	main.joy_ev_axis.clear()
	main.joy_ev_btn.clear()
	main.joy_has_unmapped = true
	var expected_pad_set: Dictionary = {}
	for button: JoyButton in [JOY_BUTTON_A, JOY_BUTTON_B,
			JOY_BUTTON_X, JOY_BUTTON_Y,
			JOY_BUTTON_DPAD_UP, JOY_BUTTON_DPAD_DOWN,
			JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT]:
		expected_pad_set[int(button)] = true
	var actual_pad_set: Dictionary = {}
	for button: JoyButton in ReefMain.SLIDE_CANVAS_RETURN_PAD_BUTTONS:
		actual_pad_set[int(button)] = true
	var expected_key_set: Dictionary = {}
	for key_code: Key in [KEY_W, KEY_A, KEY_S, KEY_D,
			KEY_UP, KEY_LEFT, KEY_DOWN, KEY_RIGHT,
			KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
		expected_key_set[int(key_code)] = true
	var actual_key_set: Dictionary = {}
	for key_code: Key in ReefMain.SLIDE_CANVAS_RETURN_KEYS:
		actual_key_set[int(key_code)] = true
	var constant_exact: bool = \
		ReefMain.SLIDE_CANVAS_RETURN_PAD_BUTTONS.size() == 8 \
		and actual_pad_set == expected_pad_set \
		and ReefMain.SLIDE_CANVAS_RETURN_KEYS.size() == 11 \
		and actual_key_set == expected_key_set
	var initial_neutral: bool = bool(main.call(
		"_slide_canvas_return_sources_neutral"))
	var exact: bool = constant_exact and initial_neutral
	var pad_diagnostics: Array[Dictionary] = []

	# Synthetic pad events are also mirrored into the production unmapped-pad
	# fallback. Prove each raw level stays nonneutral with the broad owner removed;
	# the exact production-owned size/set vocabulary above separately prevents the
	# any-face A/B compatibility fallback from masking an omitted X or Y entry.
	for button: JoyButton in [JOY_BUTTON_X, JOY_BUTTON_Y]:
		var return_token := StringName("return:pad:207:button:%d" % button)
		var melody_token := StringName("pad:207:%d" % button)
		var expected_return: Dictionary = {}
		expected_return[return_token] = true
		var expected_melody: Dictionary = {}
		expected_melody[melody_token] = true
		_slide_push_pad(button, true, 207)
		var press_return_exact: bool = \
			main._slide_canvas_return_held_sources == expected_return
		var press_melody_exact: bool = \
			main._melody_held_sources == expected_melody
		var raw_pressed: bool = bool(main.joy_ev_btn.get(int(button), false))
		var pressed_level: bool = main.joy_pressed(button)
		main._slide_canvas_return_held_sources.clear()
		var pressed_blocks_neutral: bool = not bool(main.call(
			"_slide_canvas_return_sources_neutral"))
		main._slide_canvas_return_held_sources[return_token] = true
		_slide_push_pad(button, false, 207)
		var raw_released: bool = not bool(main.joy_ev_btn.get(
			int(button), false))
		var released_level: bool = not main.joy_pressed(button)
		var release_return_exact: bool = \
			main._slide_canvas_return_held_sources.is_empty()
		var release_melody_exact: bool = main._melody_held_sources.is_empty()
		var release_neutral: bool = bool(main.call(
			"_slide_canvas_return_sources_neutral"))
		var pad_exact: bool = press_return_exact and press_melody_exact \
			and raw_pressed and pressed_level and pressed_blocks_neutral \
			and raw_released and released_level and release_return_exact \
			and release_melody_exact and release_neutral
		exact = exact and pad_exact
		pad_diagnostics.append({
			"button": int(button),
			"press_return": press_return_exact,
			"press_melody": press_melody_exact,
			"raw_pressed": raw_pressed,
			"pressed_level": pressed_level,
			"pressed_blocks_neutral": pressed_blocks_neutral,
			"raw_released": raw_released,
			"released_level": released_level,
			"release_return": release_return_exact,
			"release_melody": release_melody_exact,
			"release_neutral": release_neutral,
		})

	main._slide_canvas_return_held_sources.clear()
	main._slide_canvas_return_held_sources.merge(return_before, true)
	main._slide_canvas_held_sources.clear()
	main._slide_canvas_held_sources.merge(slide_before, true)
	main._melody_held_sources.clear()
	main._melody_held_sources.merge(melody_before, true)
	main.joy_ev_axis.clear()
	main.joy_ev_axis.merge(axis_before, true)
	main.joy_ev_btn.clear()
	main.joy_ev_btn.merge(button_before, true)
	main.joy_has_unmapped = joy_unmapped_before
	if not exact:
		print(("SLIDE_DIAG|return-poll|constant=%s|initial_neutral=%s" \
			+ "|pads=%s|initial_touch_stick=%s" \
			+ "|initial_action_down=%s|initial_action_just=%s" \
			+ "|initial_touch_owners=%s|initial_drag=%s") % [
			constant_exact, initial_neutral, pad_diagnostics,
			main.touch_ui.stick_vec, main.touch_ui.action_down,
			main.touch_ui.action_just, main.touch_ui.touch_owners,
			main.touch_ui.drag_active,
		])
	return exact


func _slide_wait_return_guard_clear(label: String) -> bool:
	var frame_guard := 0
	while bool(main.call("_slide_canvas_return_guard_active")) \
			and frame_guard < 360:
		frame_guard += 1
		await process_frame
	var clear: bool = not bool(main.call(
		"_slide_canvas_return_guard_active"))
	_slide_check("bounded return guard is clear before " + label, clear)
	return clear


func _slide_exercise_return_guard(friend: Dictionary, label: String,
		reverse_context_order: bool, touch_point: Vector2, touch_index: int,
		touch_device: int, pad_device: int, holds_prearmed: bool,
		extra_synchronous_sources: Dictionary,
		joy_unmapped_before: bool) -> Dictionary:
	var synchronous_guard: Dictionary = main.call(
		"_slide_canvas_return_guard_snapshot") as Dictionary
	var fx_water_live: bool = main.call("_fx_water_ref") != null \
		and main._fx_water != null
	var fx_probe_had_value: bool = main.fxw_cool.has(&"slide_return_probe")
	var fx_probe_old_value: Variant = main.fxw_cool.get(&"slide_return_probe")
	main.fxw_cool[&"slide_return_probe"] = 37.25
	var baseline: Dictionary = _slide_return_world_snapshot(friend)
	main.joy_has_unmapped = true
	if not holds_prearmed:
		_slide_set_return_nonpointer_holds(true, pad_device)
		_slide_push_touch(touch_point, true, touch_index, touch_device)
	var generated_sources: Dictionary = _slide_expected_return_sources(
		touch_index, touch_device, pad_device)
	var synchronous_expected: Dictionary = generated_sources.duplicate()
	synchronous_expected.merge(extra_synchronous_sources, true)
	var synchronous_sources_exact: bool = \
		main._slide_canvas_return_held_sources == synchronous_expected
	# Claimed LX/D-pad traffic was intentionally excluded from legacy raw fallback
	# while Canvas owned it. Once the distinct return guard exists, simulate the
	# backend's still-held level publication before asserting all polled values.
	_slide_set_return_nonpointer_holds(true, pad_device)
	var held_guard: Dictionary = main.call(
		"_slide_canvas_return_guard_snapshot") as Dictionary
	var armed_exact: bool = bool(synchronous_guard.get("active", false)) \
		and bool(synchronous_guard.get("control_blocked", false)) \
		and fx_water_live \
		and synchronous_sources_exact \
		and bool(held_guard.get("active", false)) \
		and int(held_guard.get("held_sources", 0)) \
			== synchronous_expected.size() \
		and main._slide_canvas_return_held_sources == synchronous_expected \
		and main.joy_pressed(JOY_BUTTON_A) \
		and main.joy_pressed(JOY_BUTTON_B) \
		and main.joy_pressed(JOY_BUTTON_X) \
		and main.joy_pressed(JOY_BUTTON_Y) \
		and main.joy_pressed(JOY_BUTTON_DPAD_UP) \
		and main.joy_pressed(JOY_BUTTON_DPAD_DOWN) \
		and main.joy_pressed(JOY_BUTTON_DPAD_LEFT) \
		and main.joy_pressed(JOY_BUTTON_DPAD_RIGHT) \
		and absf(main.joy_axis(JOY_AXIS_LEFT_X) \
			- SLIDE_RETURN_AXIS_VALUES[int(JOY_AXIS_LEFT_X)]) <= 0.001 \
		and absf(main.joy_axis(JOY_AXIS_LEFT_Y) \
			- SLIDE_RETURN_AXIS_VALUES[int(JOY_AXIS_LEFT_Y)]) <= 0.001 \
		and absf(main.joy_axis(JOY_AXIS_RIGHT_X) \
			- SLIDE_RETURN_AXIS_VALUES[int(JOY_AXIS_RIGHT_X)]) <= 0.001 \
		and absf(main.joy_axis(JOY_AXIS_RIGHT_Y) \
			- SLIDE_RETURN_AXIS_VALUES[int(JOY_AXIS_RIGHT_Y)]) <= 0.001 \
		and not main.touch_ui.world_controls_enabled \
		and _slide_return_world_matches(baseline, friend)
	var pre_context_melody_terminal_exact: bool = \
		_slide_retire_precontext_melody_holds_exact(
			synchronous_expected, touch_point, touch_index, touch_device,
			pad_device, holds_prearmed)
	armed_exact = armed_exact and pre_context_melody_terminal_exact \
		and _slide_return_world_matches(baseline, friend)

	# Keep every physical family held beyond the real return fade callback. The
	# callback's IGNORE boundary is necessary but cannot retire this guard alone.
	var fade_frames := 0
	var frozen_through_fade := true
	while bool(main.call("_slide_canvas_return_guard_active")) \
			and not bool((main.call(
				"_slide_canvas_return_guard_snapshot") as Dictionary).get(
				"fade_clear", false)) and fade_frames < 360:
		fade_frames += 1
		frozen_through_fade = frozen_through_fade \
			and _slide_return_world_matches(baseline, friend)
		await process_frame
	await process_frame
	var after_fade: Dictionary = main.call(
		"_slide_canvas_return_guard_snapshot") as Dictionary
	frozen_through_fade = frozen_through_fade \
		and bool(after_fade.get("active", false)) \
		and bool(after_fade.get("fade_clear", false)) \
		and int(after_fade.get("neutral_frames", -1)) == 0 \
		and _slide_return_world_matches(baseline, friend)

	# Context loss may clear event censuses, but it may never retire the return
	# quarantine or let the returned world consume a delayed held level.
	if reverse_context_order:
		main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
		main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	else:
		main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
		main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	await process_frame
	var lost_guard: Dictionary = main.call(
		"_slide_canvas_return_guard_snapshot") as Dictionary
	var context_frozen: bool = bool(lost_guard.get("active", false)) \
		and bool(lost_guard.get("context_lost", false)) \
		and int(lost_guard.get("neutral_frames", -1)) == 0 \
		and _slide_return_world_matches(baseline, friend)
	if reverse_context_order:
		main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	else:
		main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	await process_frame
	context_frozen = context_frozen \
		and bool(main.call("_slide_canvas_return_guard_active")) \
		and bool((main.call(
			"_slide_canvas_return_guard_snapshot") as Dictionary).get(
			"context_lost", false)) \
		and _slide_return_world_matches(baseline, friend)
	if reverse_context_order:
		main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	else:
		main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	# Re-publish still-held levels after the untrustworthy absent interval. The
	# guard must observe them again and remain armed source-free.
	_slide_set_return_nonpointer_holds(true, pad_device)
	_slide_push_touch(touch_point, true, touch_index, touch_device)
	await process_frame
	var restored_held: Dictionary = main.call(
		"_slide_canvas_return_guard_snapshot") as Dictionary
	context_frozen = context_frozen \
		and bool(restored_held.get("active", false)) \
		and not bool(restored_held.get("context_lost", true)) \
		and int(restored_held.get("neutral_frames", -1)) == 0 \
		and int(restored_held.get("held_sources", 0)) \
			== generated_sources.size() \
		and main._slide_canvas_return_held_sources == generated_sources \
		and _slide_return_world_matches(baseline, friend)

	# Observe late in Node processing. At neutral frame two Main has scheduled the
	# deferred retirement, but Player must still see active=true and stay frozen.
	var observer := SlideReturnGuardObserver.new()
	observer.name = &"SlideReturnGuardLateObserver"
	observer.main_ref = main
	observer.player_ref = player
	observer.process_mode = Node.PROCESS_MODE_ALWAYS
	observer.process_priority = 100000
	get_root().add_child(observer)
	var sample_start: int = observer.samples.size()
	var terminal_identity_exact: bool = _slide_retire_return_holds_exact(
		generated_sources, touch_point, touch_index, touch_device, pad_device)
	await process_frame
	await process_frame
	var saw_first_neutral := false
	var saw_second_pending := false
	for sample_index in range(sample_start, observer.samples.size()):
		var sample: Dictionary = observer.samples[sample_index]
		var guard: Dictionary = sample.get("guard", {}) as Dictionary
		var player_frozen: bool = sample.get("position") == baseline.get("position") \
			and sample.get("rotation") == baseline.get("rotation") \
			and sample.get("vel") == baseline.get("vel")
		if bool(guard.get("active", false)) \
				and int(guard.get("neutral_frames", 0)) == 1:
			saw_first_neutral = player_frozen \
				and not bool(guard.get("retire_pending", true))
		if bool(guard.get("active", false)) \
				and int(guard.get("neutral_frames", 0)) >= 2 \
				and bool(guard.get("retire_pending", false)):
			saw_second_pending = player_frozen
	var guard_retired: bool = not bool(main.call(
		"_slide_canvas_return_guard_active")) \
		and main.touch_ui.world_controls_enabled \
		and main.joy_ev_axis.is_empty() and main.joy_ev_btn.is_empty() \
		and _slide_return_world_matches(baseline, friend)
	observer.queue_free()

	# A first-win trophy pose remains an independent, valid movement lock after
	# the return quarantine. Prove a fresh gesture still cannot bypass it, wait
	# for its normal bounded retirement, then require a second fresh source edge.
	var move_origin := Vector2(150.0, 520.0)
	var move_point := Vector2(250.0, 520.0)
	var fresh_index: int = touch_index + 1
	var pose_lock_exact := true
	var pose_lock_exercised := false
	if main.pose_t >= 0.0:
		pose_lock_exercised = true
		var pose_position: Variant = player.position
		_slide_push_touch(move_origin, true, fresh_index, touch_device + 1)
		_slide_push_drag(move_point, move_point - move_origin,
			fresh_index, touch_device + 1)
		await process_frame
		pose_lock_exact = player.position == pose_position \
			and player.vel.is_zero_approx() \
			and not bool(main.call("_slide_canvas_return_guard_active"))
		_slide_push_touch(move_point, false, fresh_index, touch_device + 1)
		var pose_wait := 0
		while main.pose_t >= 0.0 and pose_wait < 360:
			pose_wait += 1
			await process_frame
		pose_lock_exact = pose_lock_exact and main.pose_t < 0.0
		fresh_index += 1
	var fresh_before: Variant = player.position
	_slide_push_touch(move_origin, true, fresh_index, touch_device + 1)
	_slide_push_drag(move_point, move_point - move_origin,
		fresh_index, touch_device + 1)
	await process_frame
	var fresh_moved: bool = not bool(main.call(
		"_slide_canvas_return_guard_active")) \
		and (player.position.distance_to(fresh_before) > 0.0001 \
			or player.vel.length() > 0.0001)
	_slide_push_touch(move_point, false, fresh_index, touch_device + 1)
	var fresh_terminal_census_exact: bool = \
		main._slide_canvas_held_sources.is_empty() \
		and main._melody_held_sources.is_empty()
	player.position = baseline.get("position")
	player.rotation = baseline.get("rotation")
	player.yaw = float(baseline.get("yaw", player.yaw))
	player.vel = baseline.get("vel")
	_slide_restore_camera_snapshot(baseline.get("camera", {}) as Dictionary)
	if fx_probe_had_value:
		main.fxw_cool[&"slide_return_probe"] = fx_probe_old_value
	else:
		main.fxw_cool.erase(&"slide_return_probe")
	main.joy_has_unmapped = joy_unmapped_before
	var exact: bool = armed_exact and frozen_through_fade and context_frozen \
		and pre_context_melody_terminal_exact \
		and terminal_identity_exact \
		and saw_first_neutral and saw_second_pending and guard_retired \
		and pose_lock_exact and fresh_moved and fresh_terminal_census_exact
	_slide_check(label + " return guard freezes world through fade and nested context loss",
		armed_exact and frozen_through_fade and context_frozen)
	_slide_check(label + " guard terminals retire Melody sources before any context loss",
		pre_context_melody_terminal_exact)
	_slide_check(label + " neutral frame two remains Player-frozen until deferred retirement",
		terminal_identity_exact and saw_first_neutral \
		and saw_second_pending and guard_retired)
	_slide_check(label + " only a fresh next-frame gesture moves after quarantine",
		pose_lock_exact and fresh_moved and fresh_terminal_census_exact)
	return {
		"exact": exact,
		"raw_neutral": main.joy_ev_axis.is_empty() and main.joy_ev_btn.is_empty(),
		"guard_retired": guard_retired,
		"fresh_terminal_census_exact": fresh_terminal_census_exact,
		"pre_context_melody_terminal_exact": \
			pre_context_melody_terminal_exact,
		"pose_lock_exercised": pose_lock_exercised,
		"pose_lock_tested_if_live": pose_lock_exact,
	}


func _slide_consumed_entry_release_contract() -> bool:
	if main.game != "" or main.touch_mode != main.TOUCH_MODE_HYBRID \
			or not main.touch_ui.world_controls_enabled \
			or not main.touch_ui.wants_touch():
		return false
	var movement_start: Vector2 = main.touch_ui.movement_zone().get_center()
	var movement_end: Vector2 = movement_start + Vector2(90.0, 0.0)
	var action_point: Vector2 = main.touch_ui.action_zone().get_center()
	var sibling_start := Vector2(520.0, 220.0)
	var sibling_end := sibling_start + Vector2(0.0, -40.0)
	var exact: bool = main._slide_canvas_held_sources.is_empty() \
		and main._melody_held_sources.is_empty()

	# Touch STICK: its consumed terminal retires only the target token while an
	# unrelated held world finger remains in both entry ledgers and TouchUI.
	var touch_stick_sibling := &"touch:75:620"
	var touch_stick_target := &"touch:71:610"
	var touch_stick_sibling_map: Dictionary = {}
	touch_stick_sibling_map[touch_stick_sibling] = true
	var touch_stick_pair: Dictionary = touch_stick_sibling_map.duplicate()
	touch_stick_pair[touch_stick_target] = true
	_slide_push_touch(sibling_start, true, 620, 75)
	_slide_push_drag(sibling_end, sibling_end - sibling_start, 620, 75)
	_slide_push_touch(movement_start, true, 610, 71)
	_slide_push_drag(movement_end, movement_end - movement_start, 610, 71)
	exact = exact and main._slide_canvas_held_sources == touch_stick_pair \
		and main._melody_held_sources == touch_stick_pair \
		and main.touch_ui.touch_owners.has(620) \
		and main.touch_ui.touch_owners.has(610)
	_slide_push_touch(movement_end, false, 610, 71)
	exact = exact \
		and main._slide_canvas_held_sources == touch_stick_sibling_map \
		and main._melody_held_sources == touch_stick_sibling_map \
		and main.touch_ui.touch_owners.has(620) \
		and not main.touch_ui.touch_owners.has(610)
	_slide_push_touch(sibling_end, false, 620, 75)
	exact = exact and main._slide_canvas_held_sources.is_empty() \
		and main._melody_held_sources.is_empty() \
		and not main.touch_ui.touch_owners.has(620)

	# Touch ACTION is claimed in TouchUI's early input phase, so it must never
	# create a ledger token; its terminal must leave the unrelated sibling exact.
	var touch_action_sibling := &"touch:76:621"
	var touch_action_sibling_map: Dictionary = {}
	touch_action_sibling_map[touch_action_sibling] = true
	_slide_push_touch(sibling_start, true, 621, 76)
	_slide_push_drag(sibling_end, sibling_end - sibling_start, 621, 76)
	_slide_push_touch(action_point, true, 611, 72)
	exact = exact \
		and main._slide_canvas_held_sources == touch_action_sibling_map \
		and main._melody_held_sources == touch_action_sibling_map \
		and main.touch_ui.touch_owners.has(621) \
		and main.touch_ui.touch_owners.has(611)
	_slide_push_touch(action_point, false, 611, 72)
	exact = exact \
		and main._slide_canvas_held_sources == touch_action_sibling_map \
		and main._melody_held_sources == touch_action_sibling_map \
		and main.touch_ui.touch_owners.has(621) \
		and not main.touch_ui.touch_owners.has(611)
	_slide_push_touch(sibling_end, false, 621, 76)
	exact = exact and main._slide_canvas_held_sources.is_empty() \
		and main._melody_held_sources.is_empty()

	# Native left-mouse STICK follows the same exact-owner relay while a real
	# sibling world finger remains held in both process-wide ledgers.
	var mouse_stick_sibling := &"touch:77:622"
	var mouse_stick_target := &"mouse:73:left"
	var mouse_stick_sibling_map: Dictionary = {}
	mouse_stick_sibling_map[mouse_stick_sibling] = true
	var mouse_stick_pair: Dictionary = mouse_stick_sibling_map.duplicate()
	mouse_stick_pair[mouse_stick_target] = true
	_slide_push_touch(sibling_start, true, 622, 77)
	_slide_push_drag(sibling_end, sibling_end - sibling_start, 622, 77)
	_slide_push_mouse(movement_start, true, 73)
	_slide_push_mouse_drag(movement_end, movement_end - movement_start, 73)
	exact = exact and main._slide_canvas_held_sources == mouse_stick_pair \
		and main._melody_held_sources == mouse_stick_pair \
		and main.touch_ui.touch_owners.has(622) \
		and main.touch_ui.touch_owners.has(99)
	_slide_push_mouse(movement_end, false, 73)
	exact = exact \
		and main._slide_canvas_held_sources == mouse_stick_sibling_map \
		and main._melody_held_sources == mouse_stick_sibling_map \
		and main.touch_ui.touch_owners.has(622) \
		and not main.touch_ui.touch_owners.has(99)
	_slide_push_touch(sibling_end, false, 622, 77)
	exact = exact and main._slide_canvas_held_sources.is_empty() \
		and main._melody_held_sources.is_empty()

	# Native left-mouse ACTION likewise stays absent from both ledgers and cannot
	# erase a sibling world touch when its consumed terminal is relayed.
	var mouse_action_sibling := &"touch:78:623"
	var mouse_action_sibling_map: Dictionary = {}
	mouse_action_sibling_map[mouse_action_sibling] = true
	_slide_push_touch(sibling_start, true, 623, 78)
	_slide_push_drag(sibling_end, sibling_end - sibling_start, 623, 78)
	_slide_push_mouse(action_point, true, 74)
	exact = exact \
		and main._slide_canvas_held_sources == mouse_action_sibling_map \
		and main._melody_held_sources == mouse_action_sibling_map \
		and main.touch_ui.touch_owners.has(623) \
		and main.touch_ui.touch_owners.has(99)
	_slide_push_mouse(action_point, false, 74)
	exact = exact \
		and main._slide_canvas_held_sources == mouse_action_sibling_map \
		and main._melody_held_sources == mouse_action_sibling_map \
		and main.touch_ui.touch_owners.has(623) \
		and not main.touch_ui.touch_owners.has(99)
	_slide_push_touch(sibling_end, false, 623, 78)
	main.touch_ui.consume_action()
	main.touch_ui.cancel_all_touches()
	return exact and main._slide_canvas_held_sources.is_empty() \
		and main._melody_held_sources.is_empty()


func _slide_open_pause(index: int) -> void:
	var gear: Variant = main.pause_layer.get_meta("corner_button")
	var pause_rect: Rect2 = main.touch_ui.pause_zone()
	var point: Vector2 = pause_rect.get_center()
	_slide_check("pause fixture is the real visible corner control",
		gear is Button and gear.is_visible_in_tree()
		and (gear as Button).get_global_rect().has_point(point))
	_slide_push_touch(point, true, index)
	_slide_push_touch(point, false, index)
	await process_frame
	_slide_check("real pause-corner touch raises the production sheet",
		main.get_tree().paused and main.pause_panel.visible)


func _slide_exercise_pause_and_overlay(slide: SlideRaceGame,
		friend: Dictionary) -> void:
	_slide_reset_run_state()
	await process_frame
	var held_point := Vector2(1060.0, 430.0)
	_slide_push_touch(held_point, true, SLIDE_TOUCH_INDEX + 20, 17)
	_slide_check("touch source is live before pause",
		_slide_owner_tokens(slide.audit_snapshot()).has(
			&"touch:17:111")
		and _slide_cue_active_state(slide) == Vector2i(0, 1))
	await _slide_open_pause(SLIDE_TOUCH_INDEX + 21)
	var paused_snapshot: Dictionary = slide.audit_snapshot()
	_slide_check("pause converts the exact held source to a neutral latch",
		main.pause_resume_btn.has_focus()
		and (paused_snapshot.get("input_sources", {}) as Dictionary).is_empty()
		and (paused_snapshot.get("blocked_sources", {}) as Dictionary).has(
			&"touch:17:111")
		and bool(paused_snapshot.get("blocked_until_release", false))
		and _slide_cue_active_state(slide) == Vector2i.ZERO
		and _slide_collection_suppressed()
		and bool(_slide_canvas_layer_census(slide).get("exact", false)))
	_slide_push_touch(held_point, false, SLIDE_TOUCH_INDEX + 20, 18)
	_slide_check("wrong paused release cannot clear another finger",
		_slide_owner_tokens(slide.audit_snapshot()).has(&"touch:17:111"))
	_slide_push_touch(held_point, false, SLIDE_TOUCH_INDEX + 20, 17)
	await process_frame
	_slide_check("matching release clears its latch while the sheet remains open",
		main.get_tree().paused
		and _slide_owner_tokens(slide.audit_snapshot()).is_empty())
	main.pause_resume_btn.grab_focus()
	_slide_push_action(&"ui_accept", true)
	_slide_push_action(&"ui_accept", false)
	await process_frame
	_slide_check("focused real Resume restores the same live stage neutrally",
		not main.get_tree().paused and not main.pause_panel.visible
		and main.game == "slide" and slide.active_layer() != null
		and not bool(slide.audit_snapshot().get(
			"blocked_until_release", true)))
	var lane_before: float = float(slide.audit_snapshot().get("lane", 0.0))
	_slide_push_mouse(held_point, true, 18)
	await _frames(3)
	_slide_push_mouse(held_point, false, 18)
	_slide_check("fresh mouse gesture steers after real Resume",
		float(slide.audit_snapshot().get("lane", 0.0)) > lane_before)

	# Open the real Sticker doorway while another source is held. The higher
	# sheet receives its controls; the slide receives only neutral cancellation.
	_slide_reset_run_state()
	await process_frame
	_slide_push_touch(held_point, true, SLIDE_TOUCH_INDEX + 22, 19)
	await _slide_open_pause(SLIDE_TOUCH_INDEX + 23)
	var sticker_button := main.find_child(
		"PauseStickerButton", true, false) as Button
	_slide_check("pause sheet exposes the visible Sticker doorway",
		sticker_button != null and sticker_button.is_visible_in_tree())
	if sticker_button != null:
		var sticker_point: Vector2 = sticker_button.get_global_rect().get_center()
		_slide_push_touch(sticker_point, true, SLIDE_TOUCH_INDEX + 24)
		_slide_push_touch(sticker_point, false, SLIDE_TOUCH_INDEX + 24)
		await process_frame
	var sticker_back: Button = null
	if main.stickers_layer != null:
		sticker_back = main.stickers_layer.find_child(
			"StickerBookBackButton", true, false) as Button
	_slide_check("higher Sticker sheet opens without closing or steering the slide",
		not main.get_tree().paused and main.game == "slide"
		and main.stickers_layer != null
		and main.stickers_layer.layer > slide.active_layer().layer
		and sticker_back != null
		and (slide.audit_snapshot().get("input_sources", {}) as Dictionary).is_empty()
		and bool(slide.audit_snapshot().get("blocked_until_release", false))
		and _slide_cue_active_state(slide) == Vector2i.ZERO
		and _slide_collection_suppressed()
		and bool(_slide_canvas_layer_census(slide, true).get("exact", false)))
	_slide_push_touch(held_point, false, SLIDE_TOUCH_INDEX + 22, 19)
	await process_frame
	_slide_check("held release clears neutrally through the higher overlay",
		_slide_owner_tokens(slide.audit_snapshot()).is_empty())
	if sticker_back != null:
		var back_point: Vector2 = sticker_back.get_global_rect().get_center()
		_slide_push_touch(back_point, true, SLIDE_TOUCH_INDEX + 25)
		_slide_push_touch(back_point, false, SLIDE_TOUCH_INDEX + 25)
		await process_frame
	_slide_check("real Sticker Back returns to the untouched live slide",
		main.stickers_layer == null and main.game == "slide"
		and not main.get_tree().paused and slide.active_layer() != null
		and _slide_owner_tokens(slide.audit_snapshot()).is_empty()
		and _slide_cue_active_state(slide) == Vector2i.ZERO)
	if main.stickers_layer != null:
		main._close_stickers()
	await _slide_exercise_overlay_context_restore_orders(slide, friend)
	await _slide_exercise_polled_overlay_restore_guard(slide, friend)
	await _slide_exercise_paused_restore_resume(slide, friend)
	await _slide_exercise_dev_overlay_freeze(slide, friend)
	_slide_reset_run_state()


func _slide_overlay_snapshot_unchanged(slide: SlideRaceGame,
		friend: Dictionary, baseline: Dictionary,
		layer_id: int, surface_id: int) -> bool:
	var snapshot: Dictionary = slide.audit_snapshot()
	var layer: CanvasLayer = slide.active_layer()
	var surface: Node2D = slide.stage_root()
	return main.game == "slide" and main.stickers_layer != null \
		and not main.get_tree().paused \
		and layer != null and surface != null \
		and layer.get_instance_id() == layer_id \
		and surface.get_instance_id() == surface_id \
		and is_equal_approx(float(main.g.get("t", -2.0)),
			float(baseline.get("t", -1.0))) \
		and is_equal_approx(float(snapshot.get("progress", -2.0)),
			float(baseline.get("progress", -1.0))) \
		and int(snapshot.get("tick_count", -2)) \
			== int(baseline.get("tick", -1)) \
		and int(snapshot.get("got", -2)) == int(baseline.get("got", -1)) \
		and _slide_progress_snapshot(friend) \
			== (baseline.get("reward", {}) as Dictionary) \
		and main.save_generation == int(baseline.get("generation", -1)) \
		and _slide_save_fingerprint() \
			== String(baseline.get("fingerprint", "missing")) \
		and _slide_collection_suppressed() \
		and bool(_slide_canvas_layer_census(slide, true).get("exact", false))


func _slide_exercise_polled_overlay_restore_guard(slide: SlideRaceGame,
		friend: Dictionary) -> void:
	_slide_reset_run_state()
	await process_frame
	await _slide_open_pause(SLIDE_TOUCH_INDEX + 155)
	var sticker_button := main.find_child(
		"PauseStickerButton", true, false) as Button
	if sticker_button == null:
		_slide_check("polled overlay fixture reaches the real Sticker doorway",
			false)
		if main.get_tree().paused:
			main.pause_resume_btn.grab_focus()
			_slide_push_action(&"ui_accept", true)
			_slide_push_action(&"ui_accept", false)
		await process_frame
		return
	var sticker_point: Vector2 = sticker_button.get_global_rect().get_center()
	_slide_push_touch(sticker_point, true, SLIDE_TOUCH_INDEX + 156)
	_slide_push_touch(sticker_point, false, SLIDE_TOUCH_INDEX + 156)
	await process_frame
	await _slide_wait_equivalent_sim_seconds(0.8)
	var sticker_back: Button = null
	if main.stickers_layer != null:
		sticker_back = main.stickers_layer.find_child(
			"StickerBookBackButton", true, false) as Button
	if sticker_back != null:
		sticker_back.grab_focus()
	_slide_check("polled restore fixture owns a real focused Sticker Back control",
		sticker_back != null and sticker_back.has_focus())
	var joy_unmapped_before: bool = main.joy_has_unmapped
	main.joy_has_unmapped = true
	# An overlay sees these press levels and leaves them in the unmapped raw
	# fallback. Close by touch while both are held; the claimed terminal events
	# after close must still mirror neutral into that fallback before returning.
	_slide_push_axis(0.77, 95)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, true, 95)
	await process_frame
	var overlay_raw_hold_live: bool = main.stickers_layer != null \
		and absf(main.joy_axis(JOY_AXIS_LEFT_X) - 0.77) <= 0.001 \
		and main.joy_pressed(JOY_BUTTON_DPAD_RIGHT)
	var back_point: Vector2 = sticker_back.get_global_rect().get_center() \
		if sticker_back != null else Vector2.ZERO
	_slide_push_touch(back_point, true, SLIDE_TOUCH_INDEX + 157)
	_slide_push_touch(back_point, false, SLIDE_TOUCH_INDEX + 157)
	await process_frame
	var closed_while_raw_held: bool = main.stickers_layer == null \
		and main.game == "slide" and slide.active_layer() != null \
		and absf(main.joy_axis(JOY_AXIS_LEFT_X) - 0.77) <= 0.001 \
		and main.joy_pressed(JOY_BUTTON_DPAD_RIGHT)
	_slide_push_axis(0.0, 95)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, false, 95)
	var claimed_terminal_neutral: bool = is_zero_approx(float(
		main.joy_ev_axis.get(int(JOY_AXIS_LEFT_X), INF))) \
		and not bool(main.joy_ev_btn.get(int(JOY_BUTTON_DPAD_RIGHT), true)) \
		and is_zero_approx(main.joy_axis(JOY_AXIS_LEFT_X)) \
		and not main.joy_pressed(JOY_BUTTON_DPAD_RIGHT)
	await process_frame
	var cursor_before_reopen: Vector2 = main.pad_cursor_pos
	await _slide_open_pause(SLIDE_TOUCH_INDEX + 158)
	sticker_button = main.find_child(
		"PauseStickerButton", true, false) as Button
	if sticker_button != null:
		sticker_point = sticker_button.get_global_rect().get_center()
		_slide_push_touch(sticker_point, true, SLIDE_TOUCH_INDEX + 159)
		_slide_push_touch(sticker_point, false, SLIDE_TOUCH_INDEX + 159)
	await _frames(3)
	sticker_back = null
	if main.stickers_layer != null:
		sticker_back = main.stickers_layer.find_child(
			"StickerBookBackButton", true, false) as Button
	if sticker_back != null:
		sticker_back.grab_focus()
	var reopened_neutral_asleep: bool = main.stickers_layer != null \
		and sticker_back != null and sticker_back.has_focus() \
		and not main.pad_cursor_active \
		and (main.pad_cursor_layer == null or not main.pad_cursor_layer.visible) \
		and main.pad_cursor_pos.is_equal_approx(cursor_before_reopen)
	_slide_check("claimed terminal axis and D-pad releases neutralize raw overlay state",
		overlay_raw_hold_live and closed_while_raw_held \
		and claimed_terminal_neutral and reopened_neutral_asleep)
	var layer: CanvasLayer = slide.active_layer()
	var surface: Node2D = slide.stage_root()
	var layer_id: int = layer.get_instance_id() if layer != null else 0
	var surface_id: int = surface.get_instance_id() if surface != null else 0
	var snapshot: Dictionary = slide.audit_snapshot()
	var baseline := {
		"t": float(main.g.get("t", -1.0)),
		"progress": float(snapshot.get("progress", -1.0)),
		"tick": int(snapshot.get("tick_count", -1)),
		"got": int(snapshot.get("got", -1)),
		"reward": _slide_progress_snapshot(friend),
		"generation": main.save_generation,
		"fingerprint": _slide_save_fingerprint(),
	}
	# First prove the real raw-axis path can wake and move the overlay cursor.
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, 0.74, 96)
	await _frames(2)
	var cursor_was_live: bool = main.pad_cursor_active \
		and main.pad_cursor_layer != null and main.pad_cursor_layer.visible
	var cursor_before_loss: Vector2 = main.pad_cursor_pos
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	get_root().size = SLIDE_TALL_SIZE
	await process_frame
	var neutralized_lost: bool = main.stickers_layer != null \
		and not main.pad_cursor_active \
		and (main.pad_cursor_layer == null or not main.pad_cursor_layer.visible) \
		and main._slide_canvas_overlay_axis_wait_neutral \
		and main.joy_ev_axis.is_empty() and main.joy_ev_btn.is_empty() \
		and absf(main.joy_axis(JOY_AXIS_LEFT_X)) <= 0.18 \
		and absf(main.joy_axis(JOY_AXIS_LEFT_Y)) <= 0.18 \
		and absf(main.joy_axis(JOY_AXIS_RIGHT_X)) <= 0.18 \
		and absf(main.joy_axis(JOY_AXIS_RIGHT_Y)) <= 0.18 \
		and not main._pad_prev_a and not main._pad_prev_b \
		and not main._pc_prev_a \
		and main.pad_cursor_pos.is_equal_approx(cursor_before_loss) \
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id)
	_slide_check("lost-context neutral polling cannot retire the axis latch or revive the cursor",
		cursor_was_live and neutralized_lost)
	main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	await process_frame
	_slide_check("partial polling restore cannot close or save the Sticker overlay",
		slide.input_context_lost()
		and main._slide_canvas_overlay_axis_wait_neutral
		and main.pad_cursor_pos.is_equal_approx(cursor_before_loss)
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id))
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	_slide_check("neutral full restore initially owns both controller and axis guards",
		not slide.input_context_lost()
		and main._slide_canvas_overlay_axis_wait_neutral
		and bool(slide.audit_snapshot().get(
			"input_context_restore_guard", false)))
	await process_frame
	var sticker_tall_contract: Dictionary = _slide_layout_contract(slide)
	_slide_check("Sticker-owned first restore frame lays out opaque 1280x800 without ride motion",
		Vector2i(sticker_tall_contract.get("viewport", Vector2.ZERO)) \
			== SLIDE_TALL_SIZE
		and bool(sticker_tall_contract.get("opaque", false))
		and bool(sticker_tall_contract.get("tiles", false))
		and bool(sticker_tall_contract.get("trim", false))
		and bool(sticker_tall_contract.get("progress", false))
		and bool(sticker_tall_contract.get(
			"full_screen_color_rects_exact", false))
		and not bool(slide.audit_snapshot().get(
			"input_context_restore_guard", true))
		and main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 0
		and not main.pad_cursor_active
		and main.pad_cursor_pos.is_equal_approx(cursor_before_loss)
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id))
	await process_frame
	_slide_check("first trustworthy post-guard neutral poll retains the axis latch",
		main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 1
		and not main.pad_cursor_active
		and main.pad_cursor_pos.is_equal_approx(cursor_before_loss)
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id))
	await process_frame
	_slide_check("second trustworthy post-guard neutral poll clears the axis latch",
		not main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 0
		and not main.pad_cursor_active
		and main.pad_cursor_pos.is_equal_approx(cursor_before_loss)
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id))

	# Repeat the nested loss with the raw axis neutral while absent. This time a
	# polled-equivalent held level appears on restoration; it must remain latched
	# until a later explicit neutral sample.
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	get_root().size = SLIDE_VIEW_SIZE
	await process_frame
	_slide_check("second lost frame observes neutral axes and re-arms the latch",
		slide.input_context_lost()
		and main._slide_canvas_overlay_axis_wait_neutral
		and main.joy_ev_axis.is_empty() and main.joy_ev_btn.is_empty()
		and absf(main.joy_axis(JOY_AXIS_RIGHT_X)) <= 0.18
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id))
	main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	await process_frame
	_slide_check("second partial restore still cannot retire the axis latch",
		slide.input_context_lost()
		and main._slide_canvas_overlay_axis_wait_neutral
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id))
	# Intentional polling seam/test double: hardware can be neutral on a lost
	# frame, then be physically held when focus returns without delivering a new
	# terminal/input edge. These levels must become baselines, never actions.
	main.joy_ev_axis[int(JOY_AXIS_RIGHT_X)] = 0.74
	main.joy_ev_btn[int(JOY_BUTTON_B)] = true
	main.joy_ev_btn[int(JOY_BUTTON_DPAD_RIGHT)] = true
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	_slide_check("held-high polling restore initially keeps both guards",
		not slide.input_context_lost()
		and main._slide_canvas_overlay_axis_wait_neutral
		and main.joy_pressed(JOY_BUTTON_DPAD_RIGHT)
		and bool(slide.audit_snapshot().get(
			"input_context_restore_guard", false)))
	await process_frame
	var held_restore_layout: Dictionary = _slide_layout_contract(slide)
	var held_restore_guard_exact: bool = not bool(slide.audit_snapshot().get(
		"input_context_restore_guard", true)) \
		and main._slide_canvas_overlay_axis_wait_neutral \
		and main._slide_canvas_overlay_poll_neutral_frames == 0
	# Unmapped-pad fallback deliberately treats any raw face button as either
	# logical A or B, so a held raw B is baselined into all three edge sentinels.
	var held_restore_levels_exact: bool = main._pad_prev_a \
		and main._pad_prev_b \
		and main.joy_pressed(JOY_BUTTON_DPAD_RIGHT) \
		and main._pc_prev_a
	var held_restore_cursor_exact: bool = not main.pad_cursor_active \
		and (main.pad_cursor_layer == null or not main.pad_cursor_layer.visible) \
		and main.pad_cursor_pos.is_equal_approx(cursor_before_loss)
	var held_restore_layout_exact: bool = \
		Vector2i(held_restore_layout.get("viewport", Vector2.ZERO)) \
			== SLIDE_VIEW_SIZE \
		and bool(held_restore_layout.get("opaque", false)) \
		and bool(held_restore_layout.get("tiles", false)) \
		and bool(held_restore_layout.get("trim", false)) \
		and bool(held_restore_layout.get("progress", false))
	var held_restore_world_exact: bool = _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id)
	var held_restore_quarantined: bool = held_restore_guard_exact \
		and held_restore_levels_exact and held_restore_cursor_exact \
		and held_restore_layout_exact and held_restore_world_exact
	if not held_restore_quarantined:
		print(("SLIDE_DIAG|poll-held-restore|guard=%s|levels=%s|cursor=%s" \
			+ "|layout=%s|world=%s|guard_now=%s|axis_wait=%s|neutral=%d" \
			+ "|a=%s|b=%s|dpad_right=%s|pc_a=%s") % [
			held_restore_guard_exact, held_restore_levels_exact,
			held_restore_cursor_exact, held_restore_layout_exact,
			held_restore_world_exact,
			bool(slide.audit_snapshot().get(
				"input_context_restore_guard", true)),
			main._slide_canvas_overlay_axis_wait_neutral,
			main._slide_canvas_overlay_poll_neutral_frames,
			main._pad_prev_a, main._pad_prev_b,
			main.joy_pressed(JOY_BUTTON_DPAD_RIGHT), main._pc_prev_a,
		])
	_slide_check("first source-free restore frame emits no held poll edge, cursor motion, or save",
		held_restore_quarantined)
	# A delayed physical A level arrives through the Viewport while the focused
	# Back button is armed. Main/TouchUI must record it for neutral draining but
	# consume it before GUI acceptance can close the book.
	_slide_push_pad(JOY_BUTTON_A, true, 97)
	await process_frame
	_slide_check("delayed real A press is recorded but cannot activate focused Back during poll wait",
		main.stickers_layer != null and sticker_back != null
		and sticker_back.has_focus()
		and bool(main.joy_ev_btn.get(int(JOY_BUTTON_A), false))
		and main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 0
		and main._pad_prev_a and main._pad_prev_b and main._pc_prev_a
		and not main.pad_cursor_active
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id))
	await _frames(3)
	_slide_check("held restored axis, buttons, and D-pad remain quarantined until explicit neutral",
		not bool(slide.audit_snapshot().get(
			"input_context_restore_guard", true))
		and main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 0
		and main._pad_prev_a and main._pad_prev_b and main._pc_prev_a
		and main.joy_pressed(JOY_BUTTON_DPAD_RIGHT)
		and not main.pad_cursor_active
		and main.pad_cursor_pos.is_equal_approx(cursor_before_loss)
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id))
	_slide_push_pad(JOY_BUTTON_A, false, 97)
	_slide_push_pad(JOY_BUTTON_B, false, 96)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, false, 96)
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, 0.0, 96)
	await process_frame
	_slide_check("first real neutral drain sample keeps the two-frame latch armed",
		not main.joy_pressed(JOY_BUTTON_A)
		and not main.joy_pressed(JOY_BUTTON_B)
		and not main.joy_pressed(JOY_BUTTON_DPAD_RIGHT)
		and not main._pad_prev_a and not main._pad_prev_b
		and not main._pc_prev_a
		and main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 1
		and not main.pad_cursor_active
		and main.pad_cursor_pos.is_equal_approx(cursor_before_loss)
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id))
	await process_frame
	var released: bool = not main.joy_pressed(JOY_BUTTON_A) \
		and not main.joy_pressed(JOY_BUTTON_B) \
		and not main.joy_pressed(JOY_BUTTON_DPAD_RIGHT) \
		and not main._pad_prev_a and not main._pad_prev_b \
		and not main._pc_prev_a \
		and not main._slide_canvas_overlay_axis_wait_neutral \
		and main._slide_canvas_overlay_poll_neutral_frames == 0 \
		and not main.pad_cursor_active \
		and main.pad_cursor_pos.is_equal_approx(cursor_before_loss) \
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id)
	var cursor_before_fresh_motion: Vector2 = main.pad_cursor_pos
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, 0.62, 96)
	await process_frame
	var fresh_motion_woke_cursor: bool = main.pad_cursor_active \
		and main.pad_cursor_layer != null and main.pad_cursor_layer.visible \
		and main.pad_cursor_pos.distance_to(cursor_before_fresh_motion) > 0.01 \
		and main.stickers_layer != null \
		and main.save_generation == int(baseline.get("generation", -1)) \
		and _slide_save_fingerprint() \
			== String(baseline.get("fingerprint", "missing"))
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, 0.0, 96)
	await process_frame
	# Overlay A/B shortcuts intentionally have a 0.6s reopen grace. Context and
	# poll quarantine do not age that grace, so wait for its real boundary while
	# continuing to prove the visible Sticker owns a byte-frozen ride.
	var overlay_grace_wait := 0
	var overlay_grace_frozen := true
	while main._overlay_age <= 0.6 and overlay_grace_wait < 120:
		overlay_grace_frozen = overlay_grace_frozen \
			and _slide_overlay_snapshot_unchanged(
				slide, friend, baseline, layer_id, surface_id)
		overlay_grace_wait += 1
		await process_frame
	var overlay_grace_exact: bool = main._overlay_age > 0.6 \
		and overlay_grace_frozen \
		and _slide_overlay_snapshot_unchanged(
			slide, friend, baseline, layer_id, surface_id)
	_slide_check("fresh overlay shortcut waits through its real grace without ride motion",
		overlay_grace_exact)
	_slide_push_pad(JOY_BUTTON_B, true, 96)
	await process_frame
	var fresh_edge_closed: bool = main.stickers_layer == null \
		and main.game == "slide" and slide.active_layer() != null \
		and slide.active_layer().get_instance_id() == layer_id \
		and main.save_generation == int(baseline.get("generation", -1)) \
		and _slide_save_fingerprint() \
			== String(baseline.get("fingerprint", "missing"))
	_slide_push_pad(JOY_BUTTON_B, false, 96)
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, 0.0, 96)
	await process_frame
	var lane_before_fresh_dpad: float = float(slide.audit_snapshot().get(
		"lane", 0.0))
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, true, 96)
	_slide_check("fresh post-neutral D-pad is a real owned steering source",
		not _slide_owner_tokens(slide.audit_snapshot()).is_empty())
	await _frames(4)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, false, 96)
	await process_frame
	var fresh_dpad_acted: bool = float(slide.audit_snapshot().get(
		"lane", 0.0)) > lane_before_fresh_dpad \
		and not main.joy_pressed(JOY_BUTTON_DPAD_RIGHT)
	var collection_still_suppressed: bool = _slide_collection_suppressed()
	if not (released and fresh_motion_woke_cursor and overlay_grace_exact \
			and fresh_edge_closed \
			and fresh_dpad_acted and collection_still_suppressed):
		print(("SLIDE_DIAG|poll-final|released=%s|motion=%s|edge=%s" \
			+ "|grace=%s|dpad=%s|collection=%s|axis_wait=%s|neutral=%d" \
			+ "|stickers_open=%s|lane_before=%.4f|lane_after=%.4f") % [
			released, fresh_motion_woke_cursor, fresh_edge_closed,
			overlay_grace_exact, fresh_dpad_acted,
			collection_still_suppressed,
			main._slide_canvas_overlay_axis_wait_neutral,
			main._slide_canvas_overlay_poll_neutral_frames,
			main.stickers_layer != null, lane_before_fresh_dpad,
			float(slide.audit_snapshot().get("lane", 0.0)),
		])
	_slide_check("neutral then fresh axis, B, and D-pad affect only their intended owners",
		released and fresh_motion_woke_cursor and overlay_grace_exact \
		and fresh_edge_closed
		and fresh_dpad_acted and collection_still_suppressed)
	if main.stickers_layer != null:
		main._close_stickers()
	main.joy_ev_btn.erase(int(JOY_BUTTON_A))
	main.joy_ev_btn.erase(int(JOY_BUTTON_B))
	main.joy_ev_btn.erase(int(JOY_BUTTON_DPAD_RIGHT))
	main.joy_ev_axis.erase(int(JOY_AXIS_LEFT_X))
	main.joy_ev_axis.erase(int(JOY_AXIS_RIGHT_X))
	main.joy_has_unmapped = joy_unmapped_before


func _slide_exercise_paused_restore_resume(slide: SlideRaceGame,
		friend: Dictionary) -> void:
	for reverse_value: Variant in [false, true]:
		var reverse := bool(reverse_value)
		var target_size: Vector2i = SLIDE_VIEW_SIZE if reverse \
			else SLIDE_TALL_SIZE
		_slide_reset_run_state()
		await process_frame
		var order_index: int = 190 if reverse else 180
		await _slide_open_pause(SLIDE_TOUCH_INDEX + order_index)
		main.pause_leave_btn.grab_focus()
		var before: Dictionary = slide.audit_snapshot()
		var before_t: float = float(main.g.get("t", -1.0))
		var before_reward: Dictionary = _slide_progress_snapshot(friend)
		var layer: CanvasLayer = slide.active_layer()
		var surface: Node2D = slide.stage_root()
		var layer_id: int = layer.get_instance_id() if layer != null else 0
		var surface_id: int = surface.get_instance_id() \
			if surface != null else 0
		_slide_check("paused restore fixture focuses the dangerous real Leave control",
			main.get_tree().paused and main.pause_panel.visible
			and main.pause_leave_btn.has_focus())
		if reverse:
			main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
		else:
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
			main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
		get_root().size = target_size
		await process_frame
		var paused_lost_layout: Dictionary = _slide_layout_contract(slide)
		_slide_check("paused nested OS loss preserves stage and Leave focus in either order",
			slide.input_context_lost() and main.get_tree().paused
			and main.pause_leave_btn.has_focus()
			and slide.active_layer() != null and slide.stage_root() != null
			and slide.active_layer().get_instance_id() == layer_id
			and slide.stage_root().get_instance_id() == surface_id
			and is_equal_approx(float(main.g.get("t", -2.0)), before_t)
			and int(slide.audit_snapshot().get("tick_count", -2)) \
				== int(before.get("tick_count", -1))
			and _slide_progress_snapshot(friend) == before_reward
			and Vector2i(paused_lost_layout.get("viewport", Vector2.ZERO)) \
				== target_size
			and bool(paused_lost_layout.get("opaque", false))
			and bool(paused_lost_layout.get("tiles", false))
			and bool(paused_lost_layout.get("trim", false))
			and bool(paused_lost_layout.get("progress", false)))
		if reverse:
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
			await process_frame
			main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
		else:
			main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
			await process_frame
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
		var restored_generation: int = main.save_generation
		var restored_fingerprint: String = _slide_save_fingerprint()
		_slide_check("paused full restore retains controller and two-poll guards",
			not slide.input_context_lost() and main.get_tree().paused
			and bool(slide.audit_snapshot().get(
				"input_context_restore_guard", false))
			and main._slide_canvas_overlay_axis_wait_neutral
			and main._slide_canvas_overlay_poll_neutral_frames == 0)
		# These real viewport events would accept focused Leave or toggle Pause if
		# they leaked. The ALWAYS relay must consume them while retaining their raw
		# levels for the later neutral drain.
		_slide_push_pad(JOY_BUTTON_A, true, 98 + order_index)
		_slide_push_key(KEY_ENTER, true, 98 + order_index)
		_slide_push_pad(JOY_BUTTON_START, true, 98 + order_index)
		await process_frame
		var stale: Dictionary = slide.audit_snapshot()
		var paused_restored_layout: Dictionary = _slide_layout_contract(slide)
		_slide_check("stale A, Enter, and Start cannot activate focused Leave before neutral",
			main.get_tree().paused and main.pause_panel.visible
			and main.pause_leave_btn.has_focus() and main.game == "slide"
			and slide.active_layer() != null and slide.stage_root() != null
			and slide.active_layer().get_instance_id() == layer_id
			and slide.stage_root().get_instance_id() == surface_id
			and not bool(stale.get("input_context_restore_guard", true))
			and main._slide_canvas_overlay_axis_wait_neutral
			and main._slide_canvas_overlay_poll_neutral_frames == 0
			and bool(main.joy_ev_btn.get(int(JOY_BUTTON_A), false))
			and bool(main.joy_ev_btn.get(int(JOY_BUTTON_START), false))
			and is_equal_approx(float(main.g.get("t", -2.0)), before_t)
			and int(stale.get("tick_count", -2)) \
				== int(before.get("tick_count", -1))
			and int(stale.get("got", -2)) == int(before.get("got", -1))
			and _slide_progress_snapshot(friend) == before_reward
			and main.save_generation == restored_generation
			and _slide_save_fingerprint() == restored_fingerprint
			and Vector2i(paused_restored_layout.get(
				"viewport", Vector2.ZERO)) == target_size
			and bool(paused_restored_layout.get("opaque", false))
			and bool(paused_restored_layout.get("tiles", false))
			and bool(paused_restored_layout.get("trim", false))
			and bool(paused_restored_layout.get("progress", false))
			and bool(paused_restored_layout.get(
				"full_screen_color_rects_exact", false)))
		_slide_push_pad(JOY_BUTTON_A, false, 98 + order_index)
		_slide_push_key(KEY_ENTER, false, 98 + order_index)
		_slide_push_pad(JOY_BUTTON_START, false, 98 + order_index)
		await process_frame
		_slide_check("first trustworthy paused neutral frame keeps the poll latch",
			main.get_tree().paused and main.pause_leave_btn.has_focus()
			and main._slide_canvas_overlay_axis_wait_neutral
			and main._slide_canvas_overlay_poll_neutral_frames == 1
			and is_equal_approx(float(main.g.get("t", -2.0)), before_t)
			and _slide_progress_snapshot(friend) == before_reward
			and main.save_generation == restored_generation
			and _slide_save_fingerprint() == restored_fingerprint)
		await process_frame
		var neutral: Dictionary = slide.audit_snapshot()
		_slide_check("second trustworthy paused neutral frame releases only the poll latch",
			main.get_tree().paused and main.pause_leave_btn.has_focus()
			and not main._slide_canvas_overlay_axis_wait_neutral
			and main._slide_canvas_overlay_poll_neutral_frames == 0
			and is_equal_approx(float(main.g.get("t", -2.0)), before_t)
			and int(neutral.get("tick_count", -2)) \
				== int(before.get("tick_count", -1))
			and is_equal_approx(float(neutral.get("progress", -2.0)),
				float(before.get("progress", -1.0)))
			and _slide_progress_snapshot(friend) == before_reward
			and main.save_generation == restored_generation
			and _slide_save_fingerprint() == restored_fingerprint)
		main.pause_resume_btn.grab_focus()
		_slide_push_action(&"ui_accept", true)
		_slide_push_action(&"ui_accept", false)
		var synchronous_resume: bool = not main.get_tree().paused \
			and not main.pause_panel.visible and main.game == "slide" \
			and slide.active_layer() != null and slide.stage_root() != null \
			and slide.active_layer().get_instance_id() == layer_id \
			and slide.stage_root().get_instance_id() == surface_id \
			and is_equal_approx(float(slide.audit_snapshot().get(
				"progress", -2.0)), float(before.get("progress", -1.0)))
		await process_frame
		_slide_check("fresh focused Resume works only after both paused neutral frames",
			synchronous_resume and not main.get_tree().paused
			and main.game == "slide" and _slide_living_suppressed()
			and _slide_progress_snapshot(friend) == before_reward
			and main.save_generation == restored_generation
			and _slide_save_fingerprint() == restored_fingerprint)


func _slide_exercise_dev_overlay_freeze(slide: SlideRaceGame,
		friend: Dictionary) -> void:
	if main.dev_mode == null:
		_slide_check("Developer overlay fixture is conditional outside editor/dev builds",
			true)
		return
	_slide_reset_run_state()
	await process_frame
	await _slide_open_pause(SLIDE_TOUCH_INDEX + 170)
	var developer_button := main.find_child(
		"PauseDeveloperButton", true, false) as Button
	_slide_check("pause sheet exposes its real parent-only Developer doorway",
		developer_button != null and developer_button.is_visible_in_tree()
		and bool(developer_button.get_meta("parent_only", false)))
	if developer_button == null:
		if main.get_tree().paused:
			main.pause_resume_btn.grab_focus()
			_slide_push_action(&"ui_accept", true)
			_slide_push_action(&"ui_accept", false)
		await process_frame
		return
	var developer_point: Vector2 = developer_button.get_global_rect().get_center()
	_slide_push_touch(developer_point, true, SLIDE_TOUCH_INDEX + 171)
	_slide_push_touch(developer_point, false, SLIDE_TOUCH_INDEX + 171)
	await process_frame
	var panel := main.dev_mode.get("panel") as Panel
	var close_button: Button = null
	if panel != null:
		for child_value: Variant in panel.get_children():
			var candidate := child_value as Button
			if candidate != null and candidate.text == "X":
				close_button = candidate
				break
	var layer: CanvasLayer = slide.active_layer()
	var surface: Node2D = slide.stage_root()
	var layer_id: int = layer.get_instance_id() if layer != null else 0
	var surface_id: int = surface.get_instance_id() if surface != null else 0
	var before: Dictionary = slide.audit_snapshot()
	var before_t: float = float(main.g.get("t", -1.0))
	var before_progress: float = float(before.get("progress", -1.0))
	var before_tick: int = int(before.get("tick_count", -1))
	var before_got: int = int(before.get("got", -1))
	var before_reward: Dictionary = _slide_progress_snapshot(friend)
	var before_generation: int = main.save_generation
	var before_fingerprint: String = _slide_save_fingerprint()
	_slide_check("real Developer panel resumes above the same source-free fish stage",
		bool(main.dev_mode.get("open")) and main.dev_mode.visible
		and not main.get_tree().paused and close_button != null
		and _slide_owner_tokens(before).is_empty()
		and _slide_collection_suppressed()
		and bool(_slide_canvas_layer_census(slide, false, true).get(
			"exact", false)))
	var overlay_seconds: float = await _slide_wait_equivalent_sim_seconds(
		SlideRaceGame.FISH_RUN_SECONDS + 1.0)
	var after: Dictionary = slide.audit_snapshot()
	var frozen: bool = overlay_seconds > SlideRaceGame.FISH_RUN_SECONDS \
		and is_equal_approx(float(main.g.get("t", -2.0)), before_t) \
		and is_equal_approx(float(after.get("progress", -2.0)), before_progress) \
		and int(after.get("tick_count", -2)) == before_tick \
		and int(after.get("got", -2)) == before_got \
		and _slide_progress_snapshot(friend) == before_reward \
		and main.save_generation == before_generation \
		and _slide_save_fingerprint() == before_fingerprint \
		and slide.active_layer() != null and slide.stage_root() != null \
		and slide.active_layer().get_instance_id() == layer_id \
		and slide.stage_root().get_instance_id() == surface_id \
		and bool(main.dev_mode.get("open")) \
		and _slide_collection_suppressed() \
		and bool(_slide_canvas_layer_census(slide, false, true).get(
			"exact", false))
	_slide_check("Developer panel stays open beyond one ride with time, catch, reward, save, and stage frozen",
		frozen)
	if close_button != null:
		var close_point: Vector2 = close_button.get_global_rect().get_center()
		_slide_push_touch(close_point, true, SLIDE_TOUCH_INDEX + 172)
		_slide_push_touch(close_point, false, SLIDE_TOUCH_INDEX + 172)
		await process_frame
	_slide_check("real Developer close returns to the same untouched fish stage",
		not bool(main.dev_mode.get("open")) and not main.dev_mode.visible
		and main.game == "slide" and slide.active_layer() != null
		and slide.active_layer().get_instance_id() == layer_id
		and int(slide.audit_snapshot().get("got", -2)) == before_got
		and _slide_collection_suppressed()
		and bool(_slide_canvas_layer_census(slide).get("exact", false)))
	if bool(main.dev_mode.get("open")):
		main.dev_mode.call("toggle")
	var fresh_before: Dictionary = slide.audit_snapshot()
	var lane_before: float = float(fresh_before.get("lane", 0.0))
	var fresh_key: Key = KEY_LEFT if lane_before >= 0.0 else KEY_RIGHT
	_slide_push_key(fresh_key, true, 173)
	await _frames(3)
	_slide_push_key(fresh_key, false, 173)
	await process_frame
	var fresh_after: Dictionary = slide.audit_snapshot()
	_slide_check("fresh steer resumes only after the real Developer panel closes",
		frozen and not is_equal_approx(
			float(fresh_after.get("lane", 0.0)), lane_before)
		and int(fresh_after.get("tick_count", -1))
			> int(fresh_before.get("tick_count", -1))
		and _slide_owner_tokens(fresh_after).is_empty())


func _slide_exercise_overlay_context_restore_orders(slide: SlideRaceGame,
		friend: Dictionary) -> void:
	for reverse_value: Variant in [false, true]:
		var reverse := bool(reverse_value)
		_slide_reset_run_state()
		await process_frame
		var order_index: int = 70 if reverse else 60
		await _slide_open_pause(SLIDE_TOUCH_INDEX + order_index)
		var sticker_button := main.find_child(
			"PauseStickerButton", true, false) as Button
		_slide_check("context-order fixture reaches the real Sticker doorway",
			sticker_button != null and sticker_button.is_visible_in_tree())
		if sticker_button == null:
			if main.get_tree().paused:
				main.pause_resume_btn.grab_focus()
				_slide_push_action(&"ui_accept", true)
				_slide_push_action(&"ui_accept", false)
			await process_frame
			continue
		var sticker_point: Vector2 = sticker_button.get_global_rect().get_center()
		_slide_push_touch(sticker_point, true,
			SLIDE_TOUCH_INDEX + order_index + 1)
		_slide_push_touch(sticker_point, false,
			SLIDE_TOUCH_INDEX + order_index + 1)
		await process_frame
		var sticker_back: Button = null
		if main.stickers_layer != null:
			sticker_back = main.stickers_layer.find_child(
				"StickerBookBackButton", true, false) as Button
		var layer: CanvasLayer = slide.active_layer()
		var surface: Node2D = slide.stage_root()
		var layer_id: int = layer.get_instance_id() if layer != null else 0
		var surface_id: int = surface.get_instance_id() \
			if surface != null else 0
		var snapshot: Dictionary = slide.audit_snapshot()
		var baseline := {
			"t": float(main.g.get("t", -1.0)),
			"progress": float(snapshot.get("progress", -1.0)),
			"tick": int(snapshot.get("tick_count", -1)),
			"got": int(snapshot.get("got", -1)),
			"reward": _slide_progress_snapshot(friend),
			"generation": main.save_generation,
			"fingerprint": _slide_save_fingerprint(),
		}
		_slide_check("Sticker context fixture is source-free with collection UI suppressed",
			main.stickers_layer != null and sticker_back != null
			and _slide_owner_tokens(snapshot).is_empty()
			and _slide_collection_suppressed()
			and bool(_slide_canvas_layer_census(slide, true).get("exact", false)))

		if reverse:
			main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
		else:
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
			main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
		var lost: Dictionary = slide.audit_snapshot()
		_slide_check("Sticker plus nested OS loss arms both reasons in either order",
			bool(lost.get("input_context_lost", false))
			and (lost.get("input_context_loss_reasons", []) as Array).size() == 2
			and bool(lost.get("input_context_restore_guard", false))
			and _slide_owner_tokens(lost).is_empty())
		await process_frame
		_slide_check("nested OS loss leaves the resumed Sticker stage byte-frozen",
			_slide_overlay_snapshot_unchanged(
				slide, friend, baseline, layer_id, surface_id))

		if reverse:
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
		else:
			main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
		await process_frame
		_slide_check("partial OS restore cannot unlock the Sticker-backed ride",
			slide.input_context_lost()
			and _slide_overlay_snapshot_unchanged(
				slide, friend, baseline, layer_id, surface_id))
		if reverse:
			main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
		else:
			main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
		_slide_check("full OS restore initially retains its source-free guard",
			not slide.input_context_lost()
			and bool(slide.audit_snapshot().get(
				"input_context_restore_guard", false)))
		await process_frame
		_slide_check("overlay housekeeping retires the guard without one ride tick",
			not bool(slide.audit_snapshot().get(
				"input_context_restore_guard", true))
			and main._slide_canvas_overlay_axis_wait_neutral
			and main._slide_canvas_overlay_poll_neutral_frames == 0
			and _slide_overlay_snapshot_unchanged(
				slide, friend, baseline, layer_id, surface_id))
		await process_frame
		var first_neutral_poll: bool = \
			main._slide_canvas_overlay_axis_wait_neutral \
			and main._slide_canvas_overlay_poll_neutral_frames == 1 \
			and _slide_overlay_snapshot_unchanged(
				slide, friend, baseline, layer_id, surface_id)
		await process_frame
		_slide_check("two trustworthy neutral polls reopen Sticker controls source-free",
			first_neutral_poll
			and not main._slide_canvas_overlay_axis_wait_neutral
			and main._slide_canvas_overlay_poll_neutral_frames == 0
			and _slide_overlay_snapshot_unchanged(
				slide, friend, baseline, layer_id, surface_id))

		if sticker_back != null:
			var back_point: Vector2 = sticker_back.get_global_rect().get_center()
			_slide_push_touch(back_point, true,
				SLIDE_TOUCH_INDEX + order_index + 2)
			_slide_push_touch(back_point, false,
				SLIDE_TOUCH_INDEX + order_index + 2)
			await process_frame
		_slide_check("real Sticker Back remains usable after either OS restore order",
			main.stickers_layer == null and main.game == "slide"
			and slide.active_layer() != null and slide.stage_root() != null
			and slide.active_layer().get_instance_id() == layer_id
			and slide.stage_root().get_instance_id() == surface_id
			and not main.touch_control_blocks.has("stickers")
			and _slide_collection_suppressed())
		if main.stickers_layer != null:
			main._close_stickers()
		var fresh_before: Dictionary = slide.audit_snapshot()
		var lane_before: float = float(fresh_before.get("lane", 0.0))
		var fresh_key: Key = KEY_LEFT if lane_before >= 0.0 else KEY_RIGHT
		_slide_push_key(fresh_key, true, 80 + order_index)
		await _frames(3)
		_slide_push_key(fresh_key, false, 80 + order_index)
		await process_frame
		var fresh_after: Dictionary = slide.audit_snapshot()
		_slide_check("fresh source works only after the restored overlay closes",
			not is_equal_approx(float(fresh_after.get("lane", 0.0)), lane_before)
			and int(fresh_after.get("tick_count", -1))
				> int(fresh_before.get("tick_count", -1))
			and float(main.g.get("t", -1.0)) > float(baseline.get("t", 0.0))
			and _slide_owner_tokens(fresh_after).is_empty())


func _slide_exercise_sticker_freeze(slide: SlideRaceGame,
		friend: Dictionary) -> Dictionary:
	# Exercise the dangerous resumed-overlay seam on the same run that later
	# finishes for gold. Sticker Book unpauses SceneTree so its own UI animates;
	# the fish controller must still remain byte-for-byte frozen for longer than
	# an entire 11.5-second ride, then resume only from a fresh concrete source.
	await _slide_wait_for_fade_callback(slide)
	await _slide_wait_until_ready(slide)
	_slide_reset_run_state()
	await process_frame
	var held_point := Vector2(1060.0, 430.0)
	var held_index: int = SLIDE_TOUCH_INDEX + 50
	var held_device := 41
	var lane_initial: float = float(slide.audit_snapshot().get("lane", 0.0))
	_slide_push_touch(held_point, true, held_index, held_device)
	await _frames(4)
	var before: Dictionary = slide.audit_snapshot()
	_slide_check("Sticker freeze fixture begins with deliberate real steering",
		float(before.get("lane", 0.0)) > lane_initial
		and bool(main.g.get("steered", false))
		and _slide_owner_tokens(before).has(
			StringName("touch:%d:%d" % [held_device, held_index])))
	var before_t: float = float(main.g.get("t", -1.0))
	var before_progress: float = float(before.get("progress", -1.0))
	var before_tick: int = int(before.get("tick_count", -1))
	var before_got: int = int(before.get("got", -1))
	var before_reward: Dictionary = _slide_progress_snapshot(friend)
	var before_generation: int = main.save_generation
	var before_fingerprint: String = _slide_save_fingerprint()
	var layer: CanvasLayer = slide.active_layer()
	var surface: Node2D = slide.stage_root()
	var layer_id: int = layer.get_instance_id() if layer != null else 0
	var surface_id: int = surface.get_instance_id() if surface != null else 0

	await _slide_open_pause(SLIDE_TOUCH_INDEX + 51)
	var sticker_button := main.find_child(
		"PauseStickerButton", true, false) as Button
	_slide_check("freeze fixture uses the visible Pause Sticker doorway",
		sticker_button != null and sticker_button.is_visible_in_tree())
	if sticker_button == null:
		if main.get_tree().paused:
			main.pause_resume_btn.grab_focus()
			_slide_push_action(&"ui_accept", true)
			_slide_push_action(&"ui_accept", false)
		_slide_push_touch(held_point, false, held_index, held_device)
		return {}
	var sticker_point: Vector2 = sticker_button.get_global_rect().get_center()
	_slide_push_touch(sticker_point, true, SLIDE_TOUCH_INDEX + 52)
	_slide_push_touch(sticker_point, false, SLIDE_TOUCH_INDEX + 52)
	await process_frame
	var sticker_back: Button = null
	if main.stickers_layer != null:
		sticker_back = main.stickers_layer.find_child(
			"StickerBookBackButton", true, false) as Button
	_slide_check("resumed higher Sticker sheet retains the exact live slide stage",
		not main.get_tree().paused and main.game == "slide"
		and main.stickers_layer != null and sticker_back != null
		and slide.active_layer() != null and slide.stage_root() != null
		and slide.active_layer().get_instance_id() == layer_id
		and slide.stage_root().get_instance_id() == surface_id
		and _slide_owner_tokens(slide.audit_snapshot()).has(
			StringName("touch:%d:%d" % [held_device, held_index]))
		and _slide_collection_suppressed()
		and bool(_slide_canvas_layer_census(slide, true).get("exact", false)))
	# The precise held release may retire its neutral latch through the book,
	# but no book traffic may become slide motion.
	_slide_push_touch(held_point, false, held_index, held_device)
	await process_frame
	_slide_check("held source releases neutrally through the resumed Sticker sheet",
		_slide_owner_tokens(slide.audit_snapshot()).is_empty())
	var overlay_equivalent_seconds: float = await \
		_slide_wait_equivalent_sim_seconds(
			SlideRaceGame.FISH_RUN_SECONDS + 1.0)
	var after: Dictionary = slide.audit_snapshot()
	var freeze_exact: bool = overlay_equivalent_seconds \
			> SlideRaceGame.FISH_RUN_SECONDS \
		and is_equal_approx(float(main.g.get("t", -2.0)), before_t) \
		and is_equal_approx(float(after.get("progress", -2.0)), before_progress) \
		and int(after.get("tick_count", -2)) == before_tick \
		and int(after.get("got", -2)) == before_got \
		and _slide_progress_snapshot(friend) == before_reward \
		and main.save_generation == before_generation \
		and _slide_save_fingerprint() == before_fingerprint \
		and main.game == "slide" and main.stickers_layer != null \
		and slide.active_layer() != null and slide.stage_root() != null \
		and slide.active_layer().get_instance_id() == layer_id \
		and slide.stage_root().get_instance_id() == surface_id \
		and _slide_active_layer_count() == 1 \
		and _slide_collection_suppressed() \
		and bool(_slide_canvas_layer_census(slide, true).get("exact", false))
	_slide_check("Sticker stays open beyond a full ride with time, catch, reward, save, and stage frozen",
		freeze_exact)
	var overlap_exact := false
	if sticker_back != null:
		var back_point: Vector2 = sticker_back.get_global_rect().get_center()
		var pause_zone: Rect2 = main.touch_ui.pause_zone()
		overlap_exact = sticker_back.get_global_rect().intersects(pause_zone) \
			and pause_zone.has_point(back_point)
		_slide_push_touch(back_point, true, SLIDE_TOUCH_INDEX + 53)
		_slide_push_touch(back_point, false, SLIDE_TOUCH_INDEX + 53)
		await process_frame
	var back_exact: bool = (
		overlap_exact and main.stickers_layer == null
		and not main.get_tree().paused and main.game == "slide"
		and not main.touch_control_blocks.has("stickers")
		and main.touch_control_blocks.has("slide_canvas")
		and slide.active_layer() != null and slide.stage_root() != null
		and slide.active_layer().get_instance_id() == layer_id
		and slide.stage_root().get_instance_id() == surface_id
		and int(slide.audit_snapshot().get("got", -2)) == before_got
		and _slide_collection_suppressed()
		and bool(_slide_canvas_layer_census(slide).get("exact", false))
	)
	_slide_check("real overlapping Sticker Back returns to the same frozen slide",
		back_exact)
	if main.stickers_layer != null:
		main._close_stickers()
	var fresh_before: Dictionary = slide.audit_snapshot()
	var fresh_lane: float = float(fresh_before.get("lane", 0.0))
	var fresh_key: Key = KEY_LEFT if fresh_lane >= 0.0 else KEY_RIGHT
	_slide_push_key(fresh_key, true, 42)
	await _frames(4)
	_slide_push_key(fresh_key, false, 42)
	await process_frame
	var fresh_after: Dictionary = slide.audit_snapshot()
	var fresh_steer: bool = not is_equal_approx(
		float(fresh_after.get("lane", 0.0)), fresh_lane) \
		and _slide_owner_tokens(fresh_after).is_empty() \
		and int(fresh_after.get("tick_count", -1)) \
			> int(fresh_before.get("tick_count", -1)) \
		and float(main.g.get("t", 0.0)) > before_t
	_slide_check("fresh source resumes the same ride after the overlapping Back",
		fresh_steer)
	return {
		"ready_for_completion": freeze_exact and back_exact and fresh_steer,
		"layer_id": layer_id,
		"surface_id": surface_id,
	}


func _slide_wait_equivalent_sim_seconds(sim_seconds: float) -> float:
	var time_scale: float = maxf(float(Engine.time_scale), 0.001)
	var start_msec: int = Time.get_ticks_msec()
	var wall_msec: int = ceili(sim_seconds * 1000.0 / time_scale)
	var deadline_msec: int = start_msec + wall_msec
	while Time.get_ticks_msec() < deadline_msec:
		await process_frame
	return float(Time.get_ticks_msec() - start_msec) / 1000.0 * time_scale


func _slide_exercise_system_context(slide: SlideRaceGame) -> void:
	_slide_reset_run_state()
	await process_frame
	_slide_push_key(KEY_LEFT, true, 21)
	var focus_left_live: bool = _slide_cue_active_state(slide) == Vector2i(1, 0)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	var lost: Dictionary = slide.audit_snapshot()
	var lost_t: float = float(main.g.get("t", -1.0))
	var lost_progress: float = float(lost.get("progress", -1.0))
	var lost_tick: int = int(lost.get("tick_count", -1))
	_slide_check("focus-out then app-paused nests two loss reasons behind one guard",
		bool(lost.get("input_context_lost", false))
		and (lost.get("input_context_loss_reasons", []) as Array).size() == 2
		and bool(lost.get("input_context_restore_guard", false))
		and _slide_owner_tokens(lost).is_empty()
		and main._slide_canvas_held_sources.is_empty()
		and focus_left_live
		and _slide_cue_active_state(slide) == Vector2i.ZERO)
	var pause_point: Vector2 = main.touch_ui.pause_zone().get_center()
	_slide_push_touch(pause_point, true, SLIDE_TOUCH_INDEX + 40, 22)
	_slide_push_touch(pause_point, false, SLIDE_TOUCH_INDEX + 40, 22)
	_slide_push_mouse(Vector2(1040.0, 430.0), true, 23)
	_slide_push_mouse(Vector2(1040.0, 430.0), false, 23)
	_slide_push_key(KEY_RIGHT, true, 24)
	_slide_push_key(KEY_RIGHT, false, 24)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, true, 25)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, false, 25)
	_slide_push_axis(0.9, 26)
	_slide_push_axis(0.0, 26)
	_slide_push_action(&"ui_accept", true)
	_slide_push_action(&"ui_accept", false)
	await _frames(5)
	var still_lost: Dictionary = slide.audit_snapshot()
	_slide_check("lost-context traffic cannot pause, steer, advance, or enter a census",
		not main.get_tree().paused and not main.pause_panel.visible
		and is_equal_approx(float(main.g.get("t", 0.0)), lost_t)
		and is_equal_approx(float(still_lost.get("progress", 0.0)), lost_progress)
		and int(still_lost.get("tick_count", -2)) == lost_tick
		and _slide_owner_tokens(still_lost).is_empty()
		and main._slide_canvas_held_sources.is_empty()
		and _slide_cue_active_state(slide) == Vector2i.ZERO)
	main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	await process_frame
	_slide_check("partial app restore cannot override remaining focus loss",
		slide.input_context_lost()
		and is_equal_approx(float(main.g.get("t", 0.0)), lost_t))
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	var restored: Dictionary = slide.audit_snapshot()
	_slide_check("full restore retains a source-free first-tick guard",
		not slide.input_context_lost()
		and bool(restored.get("input_context_restore_guard", false)))
	_slide_push_key(KEY_RIGHT, true, 27)
	_slide_push_key(KEY_RIGHT, false, 27)
	_slide_check("pre-tick restored traffic is swallowed without a source",
		_slide_owner_tokens(slide.audit_snapshot()).is_empty())
	await process_frame
	var first_tick: Dictionary = slide.audit_snapshot()
	_slide_check("first restored frame clears only the controller guard and preserves motion",
		not bool(first_tick.get("input_context_restore_guard", true))
		and int(first_tick.get("tick_count", -2)) == lost_tick
		and is_equal_approx(float(first_tick.get("progress", 0.0)), lost_progress)
		and is_equal_approx(float(main.g.get("t", 0.0)), lost_t)
		and _slide_cue_active_state(slide) == Vector2i.ZERO
		and main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 0)
	await process_frame
	_slide_check("first no-overlay neutral poll keeps the restored ride frozen",
		main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 1
		and int(slide.audit_snapshot().get("tick_count", -2)) == lost_tick
		and is_equal_approx(float(slide.audit_snapshot().get(
			"progress", 0.0)), lost_progress)
		and is_equal_approx(float(main.g.get("t", 0.0)), lost_t))
	await process_frame
	var after_neutral: Dictionary = slide.audit_snapshot()
	_slide_check("second no-overlay neutral poll releases the ride to normal ticking",
		not main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 0
		and int(after_neutral.get("tick_count", -2)) > lost_tick)
	var lane_before: float = float(after_neutral.get("lane", 0.0))
	_slide_push_key(KEY_RIGHT, true, 28)
	var fresh_right_only: bool = _slide_cue_active_state(slide) \
		== Vector2i(0, 1)
	await _frames(3)
	_slide_push_key(KEY_RIGHT, false, 28)
	_slide_push_key(KEY_LEFT, false, 21)
	_slide_check("fresh different source works after missing old releases",
		fresh_right_only
		and float(slide.audit_snapshot().get("lane", 0.0)) > lane_before
		and _slide_cue_active_state(slide) == Vector2i.ZERO)

	# Reverse the mobile ordering and prove neither single restore is sufficient.
	_slide_reset_run_state()
	_slide_push_key(KEY_RIGHT, true, 29)
	var reverse_right_live: bool = _slide_cue_active_state(slide) \
		== Vector2i(0, 1)
	main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	await process_frame
	_slide_check("reverse ordering remains lost until the app reason restores",
		slide.input_context_lost() and reverse_right_live
		and _slide_cue_active_state(slide) == Vector2i.ZERO)
	main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	_slide_check("reverse full restore arms the same first-tick guard",
		not slide.input_context_lost()
		and bool(slide.audit_snapshot().get(
			"input_context_restore_guard", false)))
	await process_frame
	var reverse_first: Dictionary = slide.audit_snapshot()
	var reverse_t: float = float(main.g.get("t", -1.0))
	_slide_check("reverse first frame clears only the guard without stale input",
		not bool(slide.audit_snapshot().get(
			"input_context_restore_guard", true))
		and _slide_owner_tokens(slide.audit_snapshot()).is_empty()
		and main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 0)
	await process_frame
	_slide_check("reverse first neutral poll remains clock- and source-free",
		main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 1
		and int(slide.audit_snapshot().get("tick_count", -2)) \
			== int(reverse_first.get("tick_count", -1))
		and is_equal_approx(float(main.g.get("t", -2.0)), reverse_t))
	await process_frame
	_slide_check("reverse second neutral poll clears the independent latch",
		not main._slide_canvas_overlay_axis_wait_neutral
		and main._slide_canvas_overlay_poll_neutral_frames == 0
		and _slide_cue_active_state(slide) == Vector2i.ZERO)
	_slide_push_key(KEY_RIGHT, false, 29)
	_slide_reset_run_state()


func _slide_near_finish_context_hold(slide: SlideRaceGame,
		friend: Dictionary) -> bool:
	var before: Dictionary = slide.audit_snapshot()
	var before_t: float = float(main.g.get("t", -1.0))
	var before_reward: Dictionary = _slide_progress_snapshot(friend)
	var layer: CanvasLayer = slide.active_layer()
	var surface: Node2D = slide.stage_root()
	var layer_id: int = layer.get_instance_id() if layer != null else 0
	var surface_id: int = surface.get_instance_id() if surface != null else 0
	var joy_unmapped_before: bool = main.joy_has_unmapped
	main.joy_has_unmapped = true
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
	main.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	main.notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	await process_frame
	var partial_exact: bool = slide.input_context_lost() \
		and is_equal_approx(float(main.g.get("t", -2.0)), before_t) \
		and int(slide.audit_snapshot().get("tick_count", -2)) \
			== int(before.get("tick_count", -1)) \
		and is_equal_approx(float(slide.audit_snapshot().get(
			"progress", -2.0)), float(before.get("progress", -1.0)))
	main.notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
	await process_frame
	var restored: Dictionary = slide.audit_snapshot()
	var restore_boundary_exact: bool = not slide.input_context_lost() \
		and not bool(restored.get("input_context_restore_guard", true)) \
		and main._slide_canvas_overlay_axis_wait_neutral \
		and main._slide_canvas_overlay_poll_neutral_frames == 0 \
		and is_equal_approx(float(main.g.get("t", -2.0)), before_t) \
		and int(restored.get("tick_count", -2)) \
			== int(before.get("tick_count", -1)) \
		and is_equal_approx(float(restored.get("progress", -2.0)),
			float(before.get("progress", -1.0))) \
		and int(restored.get("got", -2)) == int(before.get("got", -1)) \
		and _slide_progress_snapshot(friend) == before_reward
	var hold_generation: int = main.save_generation
	var hold_fingerprint: String = _slide_save_fingerprint()
	# These are real Viewport events, recorded into the raw fallback while the
	# poll latch owns input. Explicit joy_pressed proves the test seam is live.
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, 0.81, 99)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, true, 99)
	var raw_hold_live: bool = main.joy_has_unmapped \
		and main.joy_pressed(JOY_BUTTON_DPAD_RIGHT) \
		and absf(main.joy_axis(JOY_AXIS_RIGHT_X) - 0.81) <= 0.001
	var remaining_seconds: float = (1.0 - float(before.get(
		"progress", 0.0))) * SlideRaceGame.FISH_RUN_SECONDS
	var held_sim_seconds: float = await _slide_wait_equivalent_sim_seconds(
		remaining_seconds + 1.0)
	var held: Dictionary = slide.audit_snapshot()
	var held_exact: bool = held_sim_seconds > remaining_seconds \
		and main._slide_canvas_overlay_axis_wait_neutral \
		and main._slide_canvas_overlay_poll_neutral_frames == 0 \
		and main.joy_pressed(JOY_BUTTON_DPAD_RIGHT) \
		and absf(main.joy_axis(JOY_AXIS_RIGHT_X) - 0.81) <= 0.001 \
		and is_equal_approx(float(main.g.get("t", -2.0)), before_t) \
		and int(held.get("tick_count", -2)) == int(before.get("tick_count", -1)) \
		and is_equal_approx(float(held.get("progress", -2.0)),
			float(before.get("progress", -1.0))) \
		and int(held.get("got", -2)) == int(before.get("got", -1)) \
		and _slide_progress_snapshot(friend) == before_reward \
		and main.save_generation == hold_generation \
		and _slide_save_fingerprint() == hold_fingerprint \
		and slide.active_layer() != null and slide.stage_root() != null \
		and slide.active_layer().get_instance_id() == layer_id \
		and slide.stage_root().get_instance_id() == surface_id \
		and _slide_living_suppressed() and _slide_collection_suppressed()
	_slide_push_axis_for(JOY_AXIS_RIGHT_X, 0.0, 99)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, false, 99)
	await process_frame
	var first_neutral: Dictionary = slide.audit_snapshot()
	var first_neutral_exact: bool = main._slide_canvas_overlay_axis_wait_neutral \
		and main._slide_canvas_overlay_poll_neutral_frames == 1 \
		and not main.joy_pressed(JOY_BUTTON_DPAD_RIGHT) \
		and absf(main.joy_axis(JOY_AXIS_RIGHT_X)) <= 0.18 \
		and is_equal_approx(float(main.g.get("t", -2.0)), before_t) \
		and int(first_neutral.get("tick_count", -2)) \
			== int(before.get("tick_count", -1)) \
		and is_equal_approx(float(first_neutral.get("progress", -2.0)),
			float(before.get("progress", -1.0))) \
		and _slide_progress_snapshot(friend) == before_reward \
		and main.save_generation == hold_generation \
		and _slide_save_fingerprint() == hold_fingerprint
	await process_frame
	var second_neutral_exact: bool = not main._slide_canvas_overlay_axis_wait_neutral \
		and main._slide_canvas_overlay_poll_neutral_frames == 0 \
		and main.game == "slide" and slide.active_layer() != null \
		and slide.active_layer().get_instance_id() == layer_id
	main.joy_ev_axis.erase(int(JOY_AXIS_RIGHT_X))
	main.joy_ev_btn.erase(int(JOY_BUTTON_DPAD_RIGHT))
	main.joy_has_unmapped = joy_unmapped_before
	_slide_check("near-finish held RIGHT_X and D-pad cannot outlast the remaining ride",
		partial_exact and restore_boundary_exact and raw_hold_live and held_exact)
	_slide_check("release requires one frozen and one retiring neutral poll before resuming",
		first_neutral_exact and second_neutral_exact)
	return partial_exact and restore_boundary_exact and raw_hold_live \
		and held_exact and first_neutral_exact and second_neutral_exact


func _slide_drive_run(slide: SlideRaceGame,
		desired_catches: int, expected_living: Dictionary,
		friend: Dictionary) -> Dictionary:
	if main.game != "slide" or slide.active_layer() == null:
		return {}
	var start_layer_id: int = slide.active_layer().get_instance_id()
	var start_surface: Node2D = slide.stage_root()
	var start_surface_id: int = start_surface.get_instance_id() \
		if start_surface != null else 0
	var expected_collection_visible: bool = bool(
		main.g.get("slide_canvas_collection_was_visible", false))
	var collection_hidden_during_run: bool = _slide_collection_suppressed()
	var living_hidden_during_run: bool = _slide_living_hidden_matches(
		expected_living)
	var expect_return_pose_lock: bool = not bool(friend.get("won", false))
	await _slide_wait_for_fade_callback(slide)
	await _slide_wait_until_ready(slide)
	var source_index: int = 140 + desired_catches
	var source_device: int = 30 + desired_catches
	var held := false
	var last_point := Vector2(640.0, 440.0)
	var last_got := 0
	var caught_ids: Array[int] = []
	var mercy := true
	var frame_count := 0
	var context_hold_done: bool = desired_catches != 5
	var context_hold_exact := true
	var fresh_after_context_hold := desired_catches != 5
	var awaiting_fresh_after_context_hold := false
	var return_holds_armed := false
	var return_joy_unmapped_before: bool = main.joy_has_unmapped
	var return_device: int = 230 + desired_catches
	var return_prearm_sources_exact := false
	while main.game == "slide" and frame_count < 1200:
		frame_count += 1
		var snapshot: Dictionary = slide.audit_snapshot()
		var got: int = int(snapshot.get("got", 0))
		last_got = got
		var flags: Array = main.g.get("canvas_fish_got", []) as Array
		for index in range(flags.size()):
			if bool(flags[index]) and index not in caught_ids:
				caught_ids.append(index)
		mercy = mercy and bool(snapshot.get("no_fail_state", false)) \
			and float(main.g.get("timer", 0.0)) < 0.0
		var progress: float = float(snapshot.get("progress", 0.0))
		if not context_hold_done and progress >= 0.90 and got >= 5:
			context_hold_done = true
			context_hold_exact = await _slide_near_finish_context_hold(
				slide, friend)
			# Context loss canceled the pre-loss touch owner. The next loop must
			# establish a genuinely fresh source before the final course segment.
			held = false
			awaiting_fresh_after_context_hold = true
			continue
		if not return_holds_armed and progress >= 0.96:
			# The live steering finger plus these unclaimed physical families must
			# survive synchronous completion into the distinct Reef-return guard.
			main.joy_has_unmapped = true
			var driving_touch := StringName("return:touch:%d:%d" % [
				source_device, source_index])
			var expected_prearm_sources: Dictionary = {driving_touch: true}
			return_prearm_sources_exact = \
				main._slide_canvas_return_held_sources == expected_prearm_sources
			_slide_set_return_nonpointer_holds(true, return_device)
			return_holds_armed = true
		var points: Array = snapshot.get("fish_progress_points", []) as Array
		var lanes: Array = snapshot.get("fish_lanes", []) as Array
		var target_index := -1
		var target_lane := 0.0
		if desired_catches == 0:
			# One deliberate, low-amplitude nudge marks agency while the center gap
			# safely misses fish 0/1. A short +0.32 shelf clears center-lane fish 2,
			# then center again safely clears fish 3/4. This avoids risky full-lane
			# crossings through the next fish's catch window.
			if progress < 0.40:
				target_lane = 0.06
			elif progress < 0.58:
				target_lane = 0.32
			else:
				target_lane = 0.0
		else:
			for index in range(mini(desired_catches, points.size())):
				if index < flags.size() and not bool(flags[index]) \
						and progress <= float(points[index]) \
							+ SlideRaceGame.FISH_CATCH_PROGRESS:
					target_index = index
					break
			if target_index >= 0 and target_index < lanes.size():
				target_lane = float(lanes[target_index])
			elif desired_catches <= last_got:
				# Center is outside both remaining outer-fish catch bands.
				target_lane = 0.0
		var current_lane: float = float(snapshot.get("lane", 0.0))
		var axis: float = clampf((target_lane - current_lane) * 3.2, -1.0, 1.0)
		var width: float = maxf(
			float((snapshot.get("viewport_size", Vector2(1280.0, 720.0)) as Vector2).x),
			1.0)
		var point := Vector2((axis + 1.0) * 0.5 * width, 440.0)
		if not held:
			_slide_push_touch(point, true, source_index, source_device)
			held = true
			if awaiting_fresh_after_context_hold:
				fresh_after_context_hold = not _slide_owner_tokens(
					slide.audit_snapshot()).is_empty()
				awaiting_fresh_after_context_hold = false
		else:
			_slide_push_drag(point, point - last_point, source_index, source_device)
		last_point = point
		await process_frame
	# process_frame resumes before the returned world's Node._process pass. This
	# snapshot therefore binds synchronous Canvas teardown, not a later cleanup.
	var synchronous_return_guard: Dictionary = main.call(
		"_slide_canvas_return_guard_snapshot") as Dictionary
	var held_on_exit: bool = main.game == "" \
		and return_holds_armed \
		and bool(synchronous_return_guard.get("active", false)) \
		and bool(synchronous_return_guard.get("control_blocked", false)) \
		and int(synchronous_return_guard.get("held_sources", 0)) >= 5 \
		and absf(main.joy_axis(JOY_AXIS_LEFT_Y) \
			- SLIDE_RETURN_AXIS_VALUES[int(JOY_AXIS_LEFT_Y)]) <= 0.001 \
		and main.joy_pressed(JOY_BUTTON_DPAD_UP) \
		and main.joy_pressed(JOY_BUTTON_A) \
		and not main.touch_ui.world_controls_enabled
	var collection_restored_on_exit: bool = main.game == "" \
		and main.collection_button_layer != null \
		and main.collection_button != null \
		and main.collection_button_layer.visible == expected_collection_visible \
		and main.collection_button.is_visible_in_tree() \
			== expected_collection_visible
	var living_restored_on_exit: bool = main.game == "" \
		and _slide_living_world_snapshot() == expected_living
	var chime_on_synchronous_exit: Dictionary = _slide_chime_context()
	var pose_lock_on_synchronous_exit: bool = main.game == "" \
		and main.pose_t >= 0.0
	await process_frame
	var chime_after_next_frame: Dictionary = _slide_chime_context()
	var tier := 0
	var celebration := main.find_child(
		MedalSystem.CELEBRATION_LAYER_NAME, true, false)
	if celebration != null:
		tier = int(celebration.get_meta("celebration_tier", 0))
	var return_guard: Dictionary = {}
	if main.game == "" and return_holds_armed and held:
		return_guard = await _slide_exercise_return_guard(friend,
			"%d-fish completion" % desired_catches, true, last_point,
			source_index, source_device, return_device, true,
			{},
			return_joy_unmapped_before)
	var raw_neutral_on_exit: bool = held_on_exit \
		and bool(return_guard.get("raw_neutral", false)) \
		and bool(return_guard.get("guard_retired", false))
	collection_restored_on_exit = collection_restored_on_exit \
		and main.collection_button_layer != null \
		and main.collection_button_layer.visible == expected_collection_visible
	return {
		"got": last_got,
		"caught_ids": caught_ids,
		"tier": tier,
		"completed": main.game == "",
		"mercy": mercy and main.game == "",
		"frames": frame_count,
		"start_layer_id": start_layer_id,
		"start_surface_id": start_surface_id,
		"raw_neutral_on_exit": raw_neutral_on_exit,
		"collection_hidden_during_run": collection_hidden_during_run,
		"collection_restored_on_exit": collection_restored_on_exit,
		"living_hidden_during_run": living_hidden_during_run,
		"living_restored_on_exit": living_restored_on_exit,
		"context_hold_exact": context_hold_done and context_hold_exact,
		"fresh_after_context_hold": fresh_after_context_hold,
		"return_guard_exact": return_prearm_sources_exact \
			and (not expect_return_pose_lock or pose_lock_on_synchronous_exit) \
			and bool(return_guard.get("exact", false)),
		"return_pose_lock_exercised": bool(return_guard.get(
			"pose_lock_exercised", false)),
		"return_pose_armed_sync": pose_lock_on_synchronous_exit,
		"return_pose_lock_tested_if_live": bool(return_guard.get(
			"pose_lock_tested_if_live", false)),
		"chime_on_synchronous_exit": chime_on_synchronous_exit,
		"chime_after_next_frame": chime_after_next_frame,
	}


func _slide_check_route_regressions(slide: SlideRaceGame) -> void:
	var route_position: Variant = player.position
	var route_rotation: Variant = player.rotation
	var route_environment: Variant = main.we_node.environment
	var route_track: String = main.cur_track
	var route_music: Dictionary = _slide_music_context()
	var joy_unmapped_before: bool = main.joy_has_unmapped
	main._start_game_now(main.slide_fr)
	_slide_check("Penguin chase remains the non-Canvas shared slide course",
		main.game == "slide" and String(main.g.get("mode", "")) == "chase"
		and not bool(main.call("_slide_canvas_return_guard_active"))
		and slide.active_layer() == null and slide.audit_snapshot().is_empty()
		and (main.g.get("path", []) as Array).size() > 2
		and not main.game_nodes.is_empty() and player.visible
		and main.touch_ui.world_controls_enabled)
	main.joy_ev_axis.clear()
	main.joy_ev_btn.clear()
	main.joy_has_unmapped = true
	_slide_push_axis(0.63, 70)
	_slide_push_pad(JOY_BUTTON_DPAD_LEFT, true, 70)
	var chase_press_normal: bool = is_equal_approx(
		main.joy_axis(JOY_AXIS_LEFT_X), 0.63) \
		and main.joy_pressed(JOY_BUTTON_DPAD_LEFT)
	_slide_push_axis(0.0, 70)
	_slide_push_pad(JOY_BUTTON_DPAD_LEFT, false, 70)
	var chase_release_normal: bool = main.joy_ev_axis.has(
		int(JOY_AXIS_LEFT_X)) and main.joy_ev_btn.has(
		int(JOY_BUTTON_DPAD_LEFT)) \
		and is_zero_approx(float(main.joy_ev_axis.get(
			int(JOY_AXIS_LEFT_X), 99.0))) \
		and not bool(main.joy_ev_btn.get(int(JOY_BUTTON_DPAD_LEFT), true))
	_slide_check("Penguin chase retains ordinary raw axis and d-pad bookkeeping",
		chase_press_normal and chase_release_normal
		and slide.active_layer() == null)
	main._leave_arena_now()
	main._clear_game()
	player.rotation = route_rotation
	_slide_check("Penguin cleanup restores its captured world context",
		player.position.is_equal_approx(route_position)
		and main.we_node.environment == route_environment
		and main.cur_track == route_track
		and _slide_music_matches(route_music))

	var race_fr := {
		"fname": "Shared Play Place Regression",
		"game": "race",
		"won": true,
		"cool": 0.0,
	}
	main._start_game_now(race_fr)
	_slide_check("game equals race still builds only the shared play-place course",
		main.game == "race" and slide.active_layer() == null
		and not bool(main.call("_slide_canvas_return_guard_active"))
		and slide.audit_snapshot().is_empty()
		and (main.g.get("checks", []) as Array).size() > 0
		and not main.game_nodes.is_empty() and player.visible
		and main.touch_ui.world_controls_enabled)
	main.joy_ev_axis.clear()
	main.joy_ev_btn.clear()
	_slide_push_axis(-0.67, 71)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, true, 71)
	var race_press_normal: bool = is_equal_approx(
		main.joy_axis(JOY_AXIS_LEFT_X), -0.67) \
		and main.joy_pressed(JOY_BUTTON_DPAD_RIGHT)
	_slide_push_axis(0.0, 71)
	_slide_push_pad(JOY_BUTTON_DPAD_RIGHT, false, 71)
	var race_release_normal: bool = main.joy_ev_axis.has(
		int(JOY_AXIS_LEFT_X)) and main.joy_ev_btn.has(
		int(JOY_BUTTON_DPAD_RIGHT)) \
		and is_zero_approx(float(main.joy_ev_axis.get(
			int(JOY_AXIS_LEFT_X), 99.0))) \
		and not bool(main.joy_ev_btn.get(int(JOY_BUTTON_DPAD_RIGHT), true))
	_slide_check("game=race retains ordinary raw axis and d-pad bookkeeping",
		race_press_normal and race_release_normal
		and slide.active_layer() == null)
	main._leave_arena_now()
	main._clear_game()
	player.rotation = route_rotation
	_slide_check("shared race cleanup leaves no fish Canvas or context drift",
		slide.active_layer() == null and main.game == "" and main.g.is_empty()
		and player.position.is_equal_approx(route_position)
		and main.we_node.environment == route_environment
		and main.cur_track == route_track
		and _slide_music_matches(route_music))
	main.joy_ev_axis.clear()
	main.joy_ev_btn.clear()
	main.joy_has_unmapped = joy_unmapped_before

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
	if gname == "slide" and String(main.g.get("mode", "")) == "fish":
		var slide := main._game_obj("race", SlideRaceGame) as SlideRaceGame
		var expected_living: Dictionary = _slide_living_world_snapshot()
		expected_living["layer_visible"] = bool(
			main.g.get("slide_canvas_living_was_visible", false))
		var run: Dictionary = await _slide_drive_run(
			slide, 5, expected_living, f)
		return main.game == "" and bool(f["won"]) \
			and int(run.get("got", -1)) == 5
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
