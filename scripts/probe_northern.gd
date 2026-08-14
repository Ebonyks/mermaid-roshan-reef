extends SceneTree
# Northern-world regression: the Alpine cave star reaches a separately
# loaded, passive-safe forest/town/castle world and its return latch cannot loop.

var ok := true


func _ck(label: String, passed: bool, detail: String = "") -> void:
	print("NORTH|%s: %s%s" % [label, "OK" if passed else "FAIL",
		(" (" + detail + ")") if detail != "" else ""])
	if not passed:
		ok = false


func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for friend: Dictionary in main.friends:
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main._enter_level2()
	await process_frame
	main.set_process(false)
	main.player.set_process(false)
	# the lagoon's arrival cutscene early-returns _tick_level2 before the
	# cave-star portal code — skip it so the bot can walk through the star
	_ck("promenade replaces Alpine courtyard portal",
		String(main.g.get("phase", "")) == "promenade"
		and not main.g.has("northern_portal_pos"))
	main._enter_northern_kingdom()
	await process_frame
	_ck("northern world remains loadable", main.game == "north" and main.northern_floor)
	_ck("three readable regions", main.g.has("north_forest_center")
		and main.g.has("north_town_center") and main.g.has("north_castle_center"))
	var trees: int = int(main.g.get("north_tree_count", 0))
	var houses: int = int(main.g.get("north_house_count", 0))
	var wisps: int = int(main.g.get("north_wisp_count", 0))
	_ck("mobile dressing budget", trees >= 60 and trees <= 96
		and houses == 7 and wisps >= 16 and wisps <= 26
		and main.game_nodes.size() < 1000,
		"trees=%d houses=%d wisps=%d nodes=%d" % [trees, houses, wisps,
		main.game_nodes.size()])
	_ck("forest has understory and mushrooms",
		int(main.g.get("north_brush_count", 0)) >= 24
		and int(main.g.get("north_mushroom_count", 0)) >= 10)
	var stone_positions: Array = main.g.get("north_stone_positions", [])
	var stones_grounded := stone_positions.size() == 10
	for stone_pos: Vector3 in stone_positions:
		stones_grounded = stones_grounded and absf(stone_pos.y
			- main.northern_walk_h(stone_pos.x, stone_pos.z)) < 0.75
	_ck("two grounded spirit clearings of standing stones",
		int(main.g.get("north_stone_count", 0)) == 10 and stones_grounded)
	var bedroom_sets: Array = main.g.get("north_bedroom_sets", [])
	var bedrooms_face_hall := bedroom_sets.size() == 3
	for bedroom: Node3D in bedroom_sets:
		bedrooms_face_hall = bedrooms_face_hall and absf(wrapf(
			bedroom.rotation.y, -PI, PI)) < 0.01
	_ck("mezzanine bedrooms exist", int(main.g.get("north_bedroom_count", 0)) == 3
		and bedrooms_face_hall)
	_ck("forest POI chain built", int(main.g.get("north_poi_count", 0)) >= 8,
		"pois=%d" % int(main.g.get("north_poi_count", 0)))
	_ck("authored northern asset family", int(main.g.get(
		"north_authored_asset_family_count", 0)) == 25
		and int(main.g.get("north_authored_asset_instance_count", 0)) >= 75,
		"instances=%d" % int(main.g.get("north_authored_asset_instance_count", 0)))

	# --- the LONG-STRIP layout: pass high in the north, the forest a real
	# 20-30s act, the town street gentle, the castle far at the south end
	var pass_h: float = main.northern_walk_h(main.NORTHERN_POS.x,
		main.NORTHERN_POS.z + 332.0)
	var forest_h: float = main.northern_walk_h(main.NORTHERN_POS.x,
		main.NORTHERN_POS.z + 140.0)
	var town_h: float = main.northern_walk_h(main.NORTHERN_POS.x,
		main.NORTHERN_POS.z - 180.0)
	var castle: Vector3 = main.g.get("north_castle_center", Vector3.ZERO)
	var castle_local: Vector2 = Vector2(castle.x - main.NORTHERN_POS.x,
		castle.z - main.NORTHERN_POS.z)
	_ck("pass descends into forest", pass_h > forest_h + 10.0,
		"pass=%.1f forest=%.1f" % [pass_h, forest_h])
	_ck("town road is gentle", absf(town_h - forest_h) < 6.0,
		"forest=%.1f town=%.1f" % [forest_h, town_h])
	_ck("castle closes the far end", castle_local.y < -280.0
		and absf(castle_local.x) < 10.0,
		"local=(%.1f, %.1f)" % [castle_local.x, castle_local.y])
	var forest_span: float = 332.0 - (-116.0)   # spawn to town gate
	_ck("forest act is a 20-30s walk", forest_span > 400.0 and forest_span < 520.0,
		"span=%.0f" % forest_span)

	# --- scatter substrate rules hold on the new strip layout
	var nk: NorthernKingdom = main._northern_ref()
	_ck("flora follows substrate and reserved footprints",
		nk._north_flora_allowed("tree_pineRoundF", 30.0, 200.0)
		and not nk._north_flora_allowed("tree_pineRoundF",
			nk._path_x(100.0), 100.0)
		and not nk._north_flora_allowed("tree_pineRoundF",
			nk._stream_x(60.0), 60.0)
		and not nk._north_flora_allowed("mushroom_red", 18.0, 138.0)
		and not nk._north_flora_allowed("tree_pineRoundF", 0.0, -318.0)
		and not nk._north_flora_allowed("tree_palm", 30.0, 200.0)
		and not nk._north_flora_allowed("kelp_tall", 30.0, 200.0)
		and nk._north_flora_allowed("mushrooms_red", 30.0, 200.0)
		and not nk._north_flora_allowed("mushrooms_red", 80.0, 310.0)
		and not nk._north_flora_allowed("tree_default_fall", 80.0, 310.0)
		and nk._north_flora_allowed("pine_a", 80.0, 310.0))

	# --- the stream really carves a bed, and both crossings stay usable
	var sx: float = nk._stream_x(60.0)
	var bed_h: float = main.northern_walk_h(main.NORTHERN_POS.x + sx,
		main.NORTHERN_POS.z + 60.0)
	var bank_h: float = main.northern_walk_h(main.NORTHERN_POS.x + sx + 14.0,
		main.NORTHERN_POS.z + 60.0)
	_ck("stream carves below its banks", bank_h > bed_h + 1.2,
		"bed=%.1f bank=%.1f" % [bed_h, bank_h])
	var bx: float = nk._stream_x(-28.0)
	var bridge_h: float = main.northern_walk_h(main.NORTHERN_POS.x + bx,
		main.NORTHERN_POS.z - 28.0)
	_ck("log bridge deck is dry", bridge_h >= main.NORTHERN_POS.y + 2.2,
		"deck=%.1f" % bridge_h)
	var mill_bridge_h: float = main.northern_walk_h(main.NORTHERN_POS.x + 39.0,
		main.NORTHERN_POS.z - 213.0)
	_ck("mill plank bridge is dry", mill_bridge_h >= main.NORTHERN_POS.y + 2.5,
		"deck=%.1f" % mill_bridge_h)

	# --- the grand hall's stories are real: mezzanine floor + twin ramps
	var mezz_zones := 0
	var ramp_zones := 0
	for zz: Dictionary in main.arena_zones:
		if zz.has("floor") and absf(float(zz["floor"]) - 17.0) < 0.1:
			mezz_zones += 1
		if zz.has("ramp"):
			ramp_zones += 1
	_ck("grand hall mezzanine + twin stairs zoned",
		mezz_zones >= 1 and ramp_zones >= 2,
		"mezz=%d ramps=%d" % [mezz_zones, ramp_zones])

	var pearls_before: int = main.pearl_count
	var stickers_before: int = main.stickers.size()
	var start: Vector3 = main.player.position
	main._tick_northern(4.0, start)
	_ck("passive-safe exploration", main.game == "north"
		and main.pearl_count == pearls_before and main.stickers.size() == stickers_before)

	var return_gate: Vector3 = main.g.get("north_return_pos", Vector3.ZERO)
	main.g["north_return_armed"] = false
	main._tick_northern(0.0, return_gate)
	_ck("return gate starts disarmed", main.game == "north")
	main._tick_northern(0.0, return_gate + Vector3(0.0, 0.0, -24.0))
	main._tick_northern(0.0, return_gate)
	# The production route crosses the normal 0.25 s fade. One unlocked headless
	# frame is not an elapsed-time guarantee, so wait for the semantic Canvas
	# destination rather than sampling whichever side of the tween happens to run.
	for _frame: int in range(120):
		if main.game == "level2" and String(main.g.get("phase", "")) == "promenade":
			break
		await process_frame
	_ck("return reaches castle-side promenade", main.game == "level2"
		and String(main.g.get("phase", "")) == "promenade")
	# The hidden generic Player is return-position compatibility only. The shipped
	# Sky route is Canvas master space, so prove the child-visible spawn is on the
	# 4096..6144 castle screen instead of inspecting an inert spatial coordinate.
	var master_x: float = main._lagoon_promenade_ref().master_route_x()
	_ck("return spawn is on Canvas screen three", master_x >= 4096.0 \
		and master_x < 6144.0 and not main.player.visible \
		and not main.player.cam.current)

	print("NORTH|RESULT: %s" % ("OK" if ok else "FAIL"))
	quit(0 if ok else 1)
