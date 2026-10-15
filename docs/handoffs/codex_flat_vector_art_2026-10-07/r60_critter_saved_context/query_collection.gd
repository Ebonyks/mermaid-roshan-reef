extends SceneTree
## Pure original CollectionSystem read queries on a bare Main outside the tree.
func _initialize() -> void:
	var main: ReefMain = (load("res://scripts/main.gd") as Script).new() as ReefMain
	var collection: CollectionSystem = CollectionSystem.new(main)
	var queries: Array[Dictionary] = []
	var failures := 0
	for entry: Array in [["", "", "ocean"], ["level2", "court", "lagoon"], ["level2", "promenade", ""], ["level2", "interior", ""], ["level2", "hall", ""], ["critters", "", ""], ["north", "", ""], ["fetch", "", ""]]:
		main.game = String(entry[0])
		main.g = {"phase": String(entry[1])}
		var actual: String = collection._context()
		var ok: bool = actual == String(entry[2])
		queries.append({"kind": "context_predicate", "game": main.game, "phase": main.g["phase"], "actual": actual, "expected": String(entry[2]), "pass": ok})
		if not ok:
			failures += 1
	for mode: String in ["partial", "full"]:
		var data: Dictionary = {"r60_future_species": false}
		for index: int in range(CollectionSystem.DEFS.size()):
			if mode == "full" or index in [0, 2, 6, 11, 13, 17]:
				var definition: Dictionary = CollectionSystem.DEFS[index]
				data[String(definition["id"])] = true
		main.critter_collection = data.duplicate(true)
		for category: String in ["", "fish", "insect", "bird"]:
			var expected: int = (18 if mode == "full" else 6) if category.is_empty() else (6 if mode == "full" else 2)
			var actual: int = collection.caught_count(category)
			var unchanged: bool = main.critter_collection == data
			var ok: bool = actual == expected and unchanged
			queries.append({"kind": "caught_count_read", "mode": mode, "category": category, "actual": actual, "expected": expected, "input_unchanged": unchanged, "pass": ok})
			if not ok:
				failures += 1
	var rows: Array[Dictionary] = []
	for definition: Dictionary in CollectionSystem.DEFS:
		rows.append({"id": String(definition["id"]), "name": String(definition["name"]), "category": String(definition["category"]), "habitat": String(definition["habitat"]), "context": String(definition["context"]), "category_icon": String(CollectionSystem.CATEGORY_ICON[String(definition["category"])]), "habitat_icon": String(CollectionSystem.HABITAT_ICON[String(definition["habitat"])])})
	var report := {"engine": Engine.get_version_info(), "display": DisplayServer.get_name(), "queries": queries, "definitions": rows, "failures": failures, "native_frames": 0, "scope": "Bare Main outside tree; no ready/process, world spawn/catch/action, save IO or rendering. Original read queries on declared synthetic inputs only. Predicate output never proves game.critters origin, normal catch route, source/native closure or art/medium acceptance."}
	main.free()
	var out_path: String = OS.get_environment("R60_COMPONENT_OUT")
	var output := FileAccess.open(out_path, FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("R60_COMPONENT|", failures)
	quit(0 if failures == 0 else 1)
