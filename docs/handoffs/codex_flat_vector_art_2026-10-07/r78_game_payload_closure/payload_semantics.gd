extends SceneTree
# Diagnostic language fixture only. No Main, scenes, world, game labels or source art loaded.
var checks: Array[Dictionary] = []
var received: Dictionary = {}
var seen: Array[String] = []
var invoked: int = 0
var output: String = ""
var normal_before: Dictionary = {}
var normal_path: String = ""
const SAVE_NAMES: Array[String] = ["reef_save.json", "reef_save.json.bak", "reef_save.json.tmp", "reef_save.json.tmp0", "reef_save.json.tmp1", "reef_save.json.old", "reef_save.json.bak.tmp", "reef_save.json.bak.old", "reef_save.json.before_new_game", "reef_save.json.before_new_game.tmp", "reef_save.json.before_new_game.old"]
func _initialize() -> void:
	output = OS.get_environment("FV_PAYLOAD_OUT")
	normal_path = ProjectSettings.globalize_path("user://")
	normal_before = _save_hashes()
	call_deferred("_run")
func _save_hashes() -> Dictionary:
	var result: Dictionary = {}
	for name in SAVE_NAMES:
		var path: String = normal_path.path_join(name)
		result[name] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "ABSENT"
	return result
func _check(name: String, value: bool) -> void:
	checks.append({"name": name, "pass": value})
func _receive(value: Dictionary) -> void:
	invoked += 1
	received = value
	seen.append(String(value["game"]))
func _deliver(cb: Callable) -> void:
	cb.call()
func _run() -> void:
	var version: Dictionary = Engine.get_version_info()
	_check("exact_approved_engine", String(version["string"]) == "4.7.2-stable (official)" and String(version["hash"]) == "ed1daf0bf001b61586d9930840f2f1394092c079")
	_check("project_mobile_config", String(ProjectSettings.get_setting("rendering/renderer/rendering_method")) == "mobile")
	var payload: Dictionary = {"game": "before", "nested": {"value": 1}}
	_check("literal_dictionary_initial_value", payload["game"] == "before")
	var bound: Callable = _receive.bind(payload)
	_check("bind_does_not_invoke", invoked == 0)
	payload["game"] = "after_bind"
	bound.call()
	_check("bound_dictionary_is_reference", invoked == 1 and seen == ["after_bind"] and is_same(payload, received))
	payload["game"] = "after_call"
	_check("delivered_dictionary_remains_aliased", received["game"] == "after_call")
	var shallow: Dictionary = payload.duplicate()
	payload["game"] = "new_root"
	_check("shallow_duplicate_root_independent", shallow["game"] == "after_call")
	payload["nested"]["value"] = 2
	_check("shallow_duplicate_nested_still_alias", shallow["nested"]["value"] == 2)
	var deep: Dictionary = payload.duplicate(true)
	payload["nested"]["value"] = 3
	_check("deep_duplicate_nested_independent", deep["nested"]["value"] == 2)
	bound.call_deferred()
	_check("deferred_not_immediate", invoked == 1)
	payload["game"] = "changed_before_deferred_delivery"
	await process_frame
	_check("deferred_delivery_observes_alias_change", invoked == 2 and seen[1] == "changed_before_deferred_delivery")
	var before: int = invoked
	_deliver(bound)
	_check("plain_callback_call_synchronous", invoked == before + 1)
	var after: Dictionary = _save_hashes()
	_check("normal_eleven_names_hash_only_unchanged", after == normal_before)
	var passed: bool = true
	for row in checks:
		if not bool(row["pass"]):
			passed = false
	var result: Dictionary = {"schema": "reef.payload_language_semantics/1", "status": "PASS" if passed else "FAIL", "engine": version, "checks": checks, "normal_save_hashes_before": normal_before, "normal_save_hashes_after": after, "normal_save_names": SAVE_NAMES, "main_instantiated": false, "production_methods_executed": [], "native_frames": 0, "limits": "Generic Dictionary/Callable semantics only. No execution of _fade_cut/_start_game, no source payload reachability, Speedy rendered context, QA11/device/child/owner or artwork acceptance."}
	var f: FileAccess = FileAccess.open(output, FileAccess.WRITE)
	if f == null:
		quit(2)
		return
	f.store_string(JSON.stringify(result, "\t") + "\n")
	f.close()
	print("R78_PAYLOAD_SEMANTICS ", "PASS" if passed else "FAIL", " checks=", checks.size())
	quit(0 if passed else 1)
