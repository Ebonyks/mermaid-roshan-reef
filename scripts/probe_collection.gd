extends SceneTree
# Trusted Critter Book probe: assets, passive safety, catch interaction,
# immediate persistence, catalog overlay and habitat-specific spawn rosters.

var failed := false


func _check(ok: bool, label: String) -> void:
	if ok:
		print("COLLECTION|OK|", label)
	else:
		failed = true
		print("FAIL COLLECTION|", label)


func _init() -> void:
	var packed := load("res://scenes/main.tscn") as PackedScene
	var main := packed.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame

	main.critter_collection = {}
	var collection: CollectionSystem = main._collection_ref()
	collection._spawn_context("ocean")
	_check(collection.total_count() == 18, "catalog has 18 species")
	_check(main.collection_nodes.size() == 3, "Ocean Reef roster has three native fish")
	var unique := {}
	var assets_ok := true
	for d: Dictionary in collection.DEFS:
		var id := String(d["id"])
		unique[id] = true
		assets_ok = assets_ok and ResourceLoader.exists("res://assets/collectibles/%s.glb" % id)
	_check(unique.size() == 18, "all species ids are unique")
	_check(assets_ok and ResourceLoader.exists("res://assets/collectibles/catch_net.glb"), "all Blender GLBs import")

	# Zero input must never collect anything. The critters wait kindly forever.
	main.touch_ui.action_down = false
	for i in range(30):
		collection.tick(1.0 / 60.0, main.player.position)
	_check(collection.caught_count() == 0, "passive play earns no critters")

	# Exercise the same action edge used by touch/gamepad/keyboard gameplay.
	var first_row: Dictionary = main.collection_nodes[0]
	var first_def: Dictionary = first_row["def"]
	var first_node: Node3D = first_row["node"]
	main.player.position = first_node.position
	main.touch_ui.action_down = false
	collection.tick(1.0 / 60.0, main.player.position)
	main.touch_ui.action_down = true
	collection.tick(1.0 / 60.0, main.player.position)
	main.touch_ui.action_down = false
	await process_frame
	var first_id := String(first_def["id"])
	_check(bool(main.critter_collection.get(first_id, false)), "nearby CATCH tap records species")
	_check(collection.caught_count() == 1, "catch count advances exactly once")
	var saved_critters: Variant = main.save_data.get("critters", {})
	_check(saved_critters is Dictionary and bool((saved_critters as Dictionary).get(first_id, false)), "catch is written immediately")

	collection.open_book()
	await process_frame
	_check(main.collection_layer != null and main.collection_stage != null, "Critter Book touch overlay opens")
	collection._switch_category("bird")
	await process_frame
	_check(main.collection_category == "bird", "icon category tabs switch pages")
	collection.close_book()

	# Enter the Lagoon context without paying to build the full arena. The real
	# analytic heightfield remains available and is what production spawning uses.
	main.set_process(false)
	main.game = "level2"
	main.g = {"phase": "court", "t": 0.0}
	collection.tick(1.0 / 60.0, main.player.position)
	_check(main.collection_habitat == "lagoon", "Sky Lagoon context activates")
	_check(main.collection_nodes.size() == 15, "Lagoon spawns meadow, river and alpine rosters")
	var habitats := {}
	for row_value: Variant in main.collection_nodes:
		var row: Dictionary = row_value
		var d: Dictionary = row["def"]
		habitats[String(d["habitat"])] = true
	_check(habitats.has("meadow") and habitats.has("river") and habitats.has("alpine"), "environment-specific habitats are represented")

	print("COLLECTION|RESULT|", "FAIL" if failed else "ALL OK")
	quit(1 if failed else 0)
