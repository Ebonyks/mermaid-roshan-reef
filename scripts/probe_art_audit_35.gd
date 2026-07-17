extends SceneTree
# Game-wide visual evidence for the 3.5 art pass. This is intentionally not a
# CI probe: it needs a display renderer and writes stable Mobile-renderer views
# used by the human-review ledger and before/after contact sheets.

const OUT := "res://audit/runtime_shots_2026-07-16/pass_35"
const DUNGEON_CENTER := Vector3(0.0, -2200.0, 0.0)

var main: ReefMain = null
var camera: Camera3D = null


func _frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame


func _hide_audit_ui() -> void:
	if main == null:
		return
	for layer_value: Variant in [main.hud_layer, main.speech_layer, main.collection_button_layer,
		main.touch_ui, main.pause_layer]:
		var layer: CanvasItem = layer_value as CanvasItem
		if layer != null:
			layer.visible = false


func _shot(name: String, position: Vector3, target: Vector3, fov: float = 62.0) -> void:
	camera.fov = fov
	camera.position = position
	camera.look_at(target, Vector3.UP)
	camera.make_current()
	await _frames(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var err: Error = image.save_png(OUT + "/" + name + ".png")
	print("ART35|", name, "|", error_string(err))


func _native_shot(name: String) -> void:
	await _frames(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var err: Error = image.save_png(OUT + "/" + name + ".png")
	print("ART35|", name, "|", error_string(err))


func _fresh_main() -> ReefMain:
	if main != null and is_instance_valid(main):
		main.queue_free()
		await _frames(5)
	var packed: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(3)
	main._skip_intro()
	await _frames(18)
	main.pearl_count = main.PEARL_TOTAL
	main.trophies = 5
	for friend: Dictionary in main.friends:
		friend["found"] = true
		friend["won"] = true
	_hide_audit_ui()
	return main


func _friend_for(kind: String) -> Dictionary:
	for friend: Dictionary in main.friends:
		if String(friend.get("game", "")) == kind:
			return friend
	return {"fname": kind.capitalize(), "game": kind, "won": true, "cool": 0.0}


func _capture_reef() -> void:
	await _fresh_main()
	await _shot("01_reef_hub_wide", Vector3(35, 23, 58), Vector3(0, 2, 0), 66.0)
	await _shot("02_reef_hub_child", Vector3(9, 6, 25), Vector3(0, 2, 0), 68.0)
	await _shot("03_reef_pearl_garden", Vector3(-22, 12, 71), Vector3(-42, 1, 33), 64.0)
	await _shot("04_reef_kelp_cathedral", Vector3(34, 12, 82), Vector3(62, 2, 35), 64.0)
	await _shot("05_reef_wreck_ravine", Vector3(80, 18, -8), Vector3(66, -2, -52), 64.0)
	await _shot("06_reef_moon_grotto", Vector3(28, 12, -78), Vector3(-6, -2, -78), 64.0)
	await _shot("07_reef_rainbow_flats", Vector3(-73, 14, -22), Vector3(-59, 0, 17), 64.0)
	await _shot("08_reef_ice_current", Vector3(-70, 16, 58), Vector3(-92, 2, 84), 64.0)


func _capture_lagoon_and_north() -> void:
	main._enter_level2()
	await _frames(35)
	_hide_audit_ui()
	var o: Vector3 = main.LEVEL2_POS
	await _shot("10_lagoon_world_wide", o + Vector3(95, 62, 104), o + Vector3(0, 12, -48), 67.0)
	await _shot("11_lagoon_castle_facade", o + Vector3(0, 26, -42), o + Vector3(0, 30, -120), 62.0)
	await _shot("12_lagoon_cloud_family", o + Vector3(16, 58, -58), o + Vector3(-8, 48, -128), 65.0)
	await _shot("13_lagoon_playground", o + Vector3(120, 36, 125), o + Vector3(74, 7, 92), 64.0)
	await _shot("14_lagoon_dream_star", o + Vector3(-9, 12, 114), o + main.L2_STAR_SPOTS[0] + Vector3(0, 3, 0), 58.0)
	await _shot("15_lagoon_star_two", o + Vector3(36, 12, 37), o + main.L2_STAR_SPOTS[1] + Vector3(0, 3, 0), 58.0)
	await _shot("16_lagoon_butterfly_gate", o + Vector3(18, 12, -8), main.bw_portal_pos + Vector3(0, 3, 0), 58.0)

	var collection: CollectionSystem = main._collection_ref()
	collection._spawn_context("lagoon")
	await _frames(8)
	await _shot("17_collection_meadow", o + Vector3(-42, 15, 112), o + Vector3(-62, 5, 126), 54.0)
	await _shot("18_collection_river", o + Vector3(114, 13, 82), o + Vector3(126, 4, 62), 54.0)
	await _shot("19_collection_alpine", o + Vector3(-142, 18, -150), o + Vector3(-158, 6, -170), 54.0)

	main._enter_northern_kingdom()
	await _frames(32)
	_hide_audit_ui()
	var n: Vector3 = main.NORTHERN_POS
	var pass_pos: Vector3 = main.g.get("north_pass_pos", n + Vector3(0, 18, 184))
	var forest: Vector3 = main.g.get("north_forest_center", n + Vector3(0, 0, 92))
	var town: Vector3 = main.g.get("north_town_center", n)
	var castle: Vector3 = main.g.get("north_castle_center", n + Vector3(0, 0, -55))
	await _shot("20_north_pass", pass_pos + Vector3(28, 22, 34), pass_pos + Vector3(0, 5, -8), 64.0)
	await _shot("21_north_forest", forest + Vector3(45, 25, 58), forest + Vector3(0, 6, -12), 64.0)
	await _shot("22_north_town", town + Vector3(112, 38, 72), town + Vector3(0, 8, -10), 66.0)
	await _shot("23_north_castle", castle + Vector3(68, 38, 68), castle + Vector3(0, 13, 0), 62.0)


func _capture_castle() -> void:
	await _fresh_main()
	main._enter_level2()
	await _frames(18)
	main._enter_castle_interior()
	await _frames(32)
	_hide_audit_ui()
	var h: Vector3 = main.CASTLE_POS
	await _shot("30_castle_hall_wide", h + Vector3(0, 14, 42), h + Vector3(0, 13, -24), 66.0)
	await _shot("31_castle_throne_and_stairs", h + Vector3(18, 16, 4), h + Vector3(0, 17, -31), 62.0)
	await _shot("32_castle_crown_star", h + Vector3(12, 25, -9), h + Vector3(0, 24, -28), 58.0)
	await _shot("33_castle_music_room", h + Vector3(-34, 12, -16), h + Vector3(-47, 5, -8), 62.0)
	await _shot("34_castle_royal_bedroom", h + Vector3(35, 11, -16), h + Vector3(48, 4, -16), 62.0)
	await _shot("35_castle_kitchen_wide", h + Vector3(9, -8, 3), h + Vector3(20, -14, -6), 63.0)
	await _shot("36_castle_kitchen_props", h + Vector3(17, -10, 5), h + Vector3(19, -14, -8), 54.0)
	await _shot("37_castle_bubble_bath", h + Vector3(-8, -8, 3), h + Vector3(-20, -14, -5), 62.0)
	await _shot("38_castle_secret_privy", h + Vector3(-27, -12, -23), h + Vector3(-32, -16, -28), 56.0)
	await _shot("39_castle_undercroft", h + Vector3(0, -8, 6), h + Vector3(0, -16, -25), 65.0)
	await _shot("40_castle_upper_library", h + Vector3(-43, 43, 13), h + Vector3(-47, 36, -17), 62.0)
	await _shot("41_castle_toy_room", h + Vector3(43, 43, 13), h + Vector3(47, 36, -14), 62.0)
	await _shot("42_castle_dreaming_floor", h + Vector3(-6, 56, -39), h + Vector3(-20, 51, -57), 64.0)
	await _shot("43_castle_star_chamber", h + Vector3(-15, 41, -34), h + Vector3(-28, 42, -58), 58.0)


func _capture_arena(kind: String, file_name: String, pos: Vector3, target: Vector3) -> void:
	await _fresh_main()
	var friend: Dictionary
	if kind == "shop":
		friend = main.shop_fr
	elif kind == "treasure":
		friend = main.treasure_fr
	elif kind == "slide":
		friend = main.slide_fr
	elif kind == "fairyshoot":
		friend = main.fairy_fr
	else:
		friend = _friend_for(kind)
	main._start_game(friend)
	await _frames(28)
	_hide_audit_ui()
	await _shot(file_name, main.ARENA_POS + pos, main.ARENA_POS + target, 62.0)


func _capture_arenas() -> void:
	await _capture_arena("fetch", "50_arena_fetch", Vector3(18, 13, 27), Vector3(0, 3, 0))
	await _capture_arena("dolls", "51_arena_dolls", Vector3(18, 13, 27), Vector3(0, 4, 0))
	await _capture_arena("seek", "52_arena_seek", Vector3(18, 13, 27), Vector3(0, 3, 0))
	await _capture_arena("melody", "53_gabby_theater", Vector3(22, 13, 26), Vector3(0, 7, -15))
	await _capture_arena("shop", "54_pearl_shop", Vector3(12, 10, 18), Vector3(0, 6, -5))
	await _capture_arena("treasure", "55_treasure_cavern", Vector3(18, 13, 27), Vector3(0, 4, 0))
	await _capture_arena("slide", "56_penguin_slide", Vector3(28, 22, 30), Vector3(0, 5, 18))
	await _capture_arena("fairyshoot", "57_fairy_pond", Vector3(34, 30, 38), Vector3(0, 1, 55))


func _capture_galaxy() -> void:
	await _fresh_main()
	main._start_galaxy()
	await _frames(42)
	var galaxy: GalaxyLevel = main.galaxy_game as GalaxyLevel
	if galaxy == null:
		return
	if galaxy._hud != null:
		galaxy._hud.visible = false
	var origin: Vector3 = GalaxyLevel.ORIGIN
	await _shot("60_butterfly_planet_wide", origin + Vector3(108, 72, 118), origin, 60.0)
	var home: Vector3 = galaxy._home_pos
	await _shot("61_butterfly_home_gate", home + Vector3(13, -18, 15), home, 55.0)
	var gate_dir: Vector3 = GalaxyLevel.GATE_DIR.normalized()
	var gate: Vector3 = origin + gate_dir * (GalaxyLevel.PLANET_R + 5.0)
	await _shot("62_butterfly_castle_gate", gate + gate_dir * 22.0 + Vector3(10, 2, 8), gate, 55.0)
	galaxy._enter_castle_gate()
	await _frames(25)
	if galaxy._hud != null:
		galaxy._hud.visible = false
	var hall: Vector3 = GalaxyLevel.HALL_C
	await _shot("63_butterfly_castle_hall", hall + Vector3(0, 16, 29), hall + Vector3(0, 5, -4), 62.0)
	await _shot("64_butterfly_castle_ice_gate", hall + Vector3(-2, 9, 24), hall + Vector3(-14, 4, 11), 56.0)


func _capture_dungeon() -> void:
	for room_index: int in range(DungeonLevel.ROOMS.size()):
		await _fresh_main()
		main.dungeon_progress = room_index
		main._start_dungeon()
		await _frames(32)
		if main.dungeon_game == null:
			continue
		if main.dungeon_game.hud != null:
			main.dungeon_game.hud.visible = false
		var room: Dictionary = DungeonLevel.ROOMS[room_index]
		var room_name: String = String(room["name"]).to_lower().replace(" ", "_").replace("-", "_")
		if main.dungeon_game.arena != null and main.dungeon_game.arena.cam != null:
			main.dungeon_game.arena.cam.make_current()
		else:
			var viewport_camera: Camera3D = get_root().get_viewport().get_camera_3d()
			if viewport_camera == camera:
				await _shot("70_dungeon_%02d_%s" % [room_index + 1, room_name],
					DUNGEON_CENTER + Vector3(0, 28, 33), DUNGEON_CENTER + Vector3(0, 3, -3), 60.0)
				continue
		await _native_shot("70_dungeon_%02d_%s" % [room_index + 1, room_name])


func _capture_picture_games() -> void:
	await _fresh_main()
	for kind: String in ["snowman", "garden", "trampoline", "xmas"]:
		main._mg2d_open(kind)
		await _frames(8)
		await _native_shot("80_picture_" + kind)
		main._mg2d_close()
		await _frames(5)


func _capture_kart() -> void:
	await _fresh_main()
	main._start_kart_game(false, "terrain")
	await _frames(35)
	await _native_shot("90_kart_ocean_select")
	var kart: KartGame = main.kart_game as KartGame
	if kart != null:
		kart._sel_t = KartGame.SELECT_TIMEOUT + 0.1
		await _frames(3)
		kart._sel_t = KartGame.SELECT_TIMEOUT + 0.1
		await _frames(10)
		await _native_shot("91_kart_ocean_countdown")
	await _fresh_main()
	main.game = "level2"
	main._start_kart_game(false, "float")
	await _frames(35)
	await _native_shot("92_kart_rainbow_select")


func _init() -> void:
	if DisplayServer.get_name() == "headless":
		print("ART35|RESULT|DISPLAY REQUIRED")
		quit(2)
		return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	camera = Camera3D.new()
	camera.name = "ArtAudit35Camera"
	get_root().add_child(camera)
	await _capture_reef()
	await _capture_lagoon_and_north()
	await _capture_castle()
	await _capture_arenas()
	await _capture_galaxy()
	await _capture_dungeon()
	await _capture_picture_games()
	await _capture_kart()
	print("ART35|RESULT|DONE")
	quit()
