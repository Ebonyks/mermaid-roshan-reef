extends SceneTree
const Pack := preload("res://scripts/arena/sky_lagoon_candidate_manifest.gd")
var failures: int = 0
var missing_path: String = ""

func check(label: String, okay: bool) -> void:
	print("SKYPACK|%s|%s" % [label, "OK" if okay else "FAIL"])
	if not okay:
		failures += 1

func _initialize() -> void:
	call_deferred("run")

func fault_loader(path: String, size: Vector2i) -> Texture2D:
	return null if path == missing_path else Pack._load_checked(path, size)

func run() -> void:
	var document: Variant = JSON.parse_string(FileAccess.get_file_as_string(Pack.PATH))
	check("real_manifest_schema", Pack.validate_document(document).is_empty())
	var good: Dictionary = {"save_sentinel": 11}
	check("real_imported_pack_ready", Pack.select_version("animated_v1", good) == "animated_v1" and (good.get("lagoon_candidate_resources", {}) as Dictionary).size() == 17)
	var state: Dictionary = {"save_sentinel": 11}
	check("missing_manifest_falls_back", Pack.select_version("animated_v1", state, "user://missing_sky_manifest.json") == "original" and state.has("lagoon_candidate_rejection"))
	var temporary: String = "user://malformed_sky_manifest.json"
	var file: FileAccess = FileAccess.open(temporary, FileAccess.WRITE)
	file.store_string("{ not valid json")
	file.close()
	check("malformed_json_falls_back", Pack.select_version("animated_v1", state, temporary) == "original" and not state.has("lagoon_candidate_resources"))
	DirAccess.remove_absolute(ProjectSettings.globalize_path(temporary))
	var malformed: Array = [null, [], {}, {"schema": {}, "assets": []}]
	for mutation: int in range(6):
		var copy: Dictionary = (document as Dictionary).duplicate(true)
		var rows: Array = copy["assets"] as Array
		match mutation:
			0: rows.pop_back()
			1: rows[1] = rows[0].duplicate(true)
			2: rows[0]["file"] = "../../unrelated.png"
			3: rows[0]["size"] = [1, 1]
			4: rows[0]["size"] = [{}, "bad"]
			5: copy["art_version"] = "unknown"
		malformed.append(copy)
	var rejects_all: bool = true
	for item: Variant in malformed:
		rejects_all = rejects_all and not Pack.validate_document(item).is_empty()
	check("ten_malformed_document_cases_rejected", rejects_all and malformed.size() == 10)
	var faults: Array[String] = []
	for name: String in Pack.REQUIRED:
		faults.append(Pack.BASE + name)
	faults.append(Pack.SHARED_RIPPLE)
	var failure_atomic: bool = true
	for path: String in faults:
		missing_path = path
		failure_atomic = failure_atomic and Pack.select_version("animated_v1", state, Pack.PATH, fault_loader) == "original" and not state.has("lagoon_candidate_resources") and state.has("lagoon_candidate_rejection")
	check("all17_missing_resource_cases_fall_back_without_partial_pack", failure_atomic)
	check("real_wrong_texture_size_rejected", Pack._load_checked(Pack.BASE + "grass_breeze.png", Vector2i(1, 1)) == null)
	check("real_missing_texture_rejected", Pack._load_checked(Pack.BASE + "does_not_exist.png", Vector2i(1, 1)) == null)
	check("recovery_after_fault", Pack.select_version("animated_v1", state) == "animated_v1" and not state.has("lagoon_candidate_rejection"))
	check("explicit_original_skips_missing_manifest", Pack.select_version("original", state, "user://missing_sky_manifest.json") == "original" and not state.has("lagoon_candidate_rejection") and not state.has("lagoon_candidate_resources"))
	Pack.clear(good)
	Pack.clear(state)
	check("save_state_untouched", state == {"save_sentinel": 11} and good == {"save_sentinel": 11})
	print("SKYPACK|RESULT|%s" % ("ALL OK" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)
