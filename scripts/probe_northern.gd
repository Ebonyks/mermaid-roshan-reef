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

	_ck("Alpine cave star is entrance", main.g.has("northern_portal_pos")
		and main.g.has("alpine_secret_pos")
		and (main.g["northern_portal_pos"] as Vector3).is_equal_approx(
			main.g["alpine_secret_pos"] as Vector3))
	var sky_gate: Vector3 = main.g.get("northern_portal_pos", Vector3.ZERO)
	main._tick_level2(0.0, sky_gate)
	await process_frame
	_ck("cave star enters northern world", main.game == "north" and main.northern_floor)
	_ck("three readable regions", main.g.has("north_forest_center")
		and main.g.has("north_town_center") and main.g.has("north_castle_center"))
	_ck("mobile dressing budget", int(main.g.get("north_tree_count", 0)) == 16
		and int(main.g.get("north_house_count", 0)) == 6
		and int(main.g.get("north_wisp_count", 0)) == 8
		and int(main.g.get("north_mushroom_count", 0)) == 8)
	var northern: NorthernKingdom = main._northern_ref()
	_ck("flora follows substrate and reserved footprints",
		northern._north_flora_allowed("tree_pineRoundF", -23.0, 174.0)
		and not northern._north_flora_allowed("mushroom_red", -23.0, 174.0)
		and northern._north_flora_allowed("mushroom_red", -18.0, 137.0)
		and not northern._north_flora_allowed("tree_pineRoundF", 0.0, 80.0)
		and not northern._north_flora_allowed("tree_pineRoundF", 150.0, 0.0)
		and not northern._north_flora_allowed("tree_pineRoundF", 0.0, -55.0))

	var pass_h: float = main.northern_walk_h(main.NORTHERN_POS.x,
		main.NORTHERN_POS.z + 184.0)
	var forest_h: float = main.northern_walk_h(main.NORTHERN_POS.x,
		main.NORTHERN_POS.z + 92.0)
	var town_h: float = main.northern_walk_h(main.NORTHERN_POS.x,
		main.NORTHERN_POS.z + 4.0)
	var castle: Vector3 = main.g.get("north_castle_center", Vector3.ZERO)
	var castle_local: Vector2 = Vector2(castle.x - main.NORTHERN_POS.x,
		castle.z - main.NORTHERN_POS.z)
	_ck("pass descends into forest", pass_h > forest_h + 10.0,
		"pass=%.1f forest=%.1f" % [pass_h, forest_h])
	_ck("town road is gentle", absf(town_h - forest_h) < 12.0,
		"forest=%.1f town=%.1f" % [forest_h, town_h])
	_ck("castle anchors the center", castle_local.length() < 70.0,
		"local=(%.1f, %.1f)" % [castle_local.x, castle_local.y])

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
	await process_frame
	_ck("return reaches Alpine cave", main.game == "level2"
		and not bool(main.g.get("northern_portal_armed", true)))
	var rebuilt_gate: Vector3 = main.g.get("northern_portal_pos", Vector3.ZERO)
	var cave_mouth: Vector3 = main.g.get("alpine_cave_entrance", Vector3.ZERO)
	_ck("return spawn clears star at cave mouth",
		main.player.position.distance_to(rebuilt_gate) >= 15.0
		and main.player.position.distance_to(cave_mouth) < 4.0)

	print("NORTH|RESULT: %s" % ("OK" if ok else "FAIL"))
	quit(0 if ok else 1)
