extends SceneTree
## R45 pure engine semantics. No game scene, artwork, profile, camera or world is instantiated.

class AuditTarget:
	extends RefCounted
	var payloads: Array[String] = []
	func record(value: Variant) -> void:
		payloads.append(str(value))

class DefaultTarget:
	var unused: int = 0

var errors: Array[String] = []
var checks: Array[Dictionary] = []
var local_payloads: Array[String] = []

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base: String = ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var path: String = base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result

func _check(ok: bool, id: String, evidence: Variant) -> void:
	checks.append({"id": id, "pass": ok, "evidence": evidence})
	if not ok:
		errors.append(id)

func _write_json(path: String, data: Dictionary) -> void:
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		errors.append("write " + path.get_file())
		return
	file.store_string(JSON.stringify(data, "\t", true) + "\n")
	file.close()

func _local_record(value: String) -> void:
	local_payloads.append(value)

func _run() -> void:
	var engine: Dictionary = Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official" or String(engine.get("hash", "")) != "ed1daf0bf001b61586d9930840f2f1394092c079":
		print("DISPATCH45|FAIL|approved engine required")
		quit(1)
		return
	var out_dir: String = OS.get_environment("R45_OUT")
	var input_path: String = OS.get_environment("R45_CLASS_INPUT")
	if out_dir.is_empty() or input_path.is_empty() or DirAccess.dir_exists_absolute(out_dir):
		print("DISPATCH45|FAIL|new exact output/input required")
		quit(1)
		return
	var before: Dictionary = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir.path_join("native_classes"))
	var target: AuditTarget = AuditTarget.new()
	var empty: Callable = Callable()
	_check(not empty.is_valid() and target.payloads.is_empty(), "empty_constructor_is_not_invocation", {"valid": empty.is_valid(), "payload_count": target.payloads.size()})
	var callback: Callable = Callable(target, "record")
	_check(callback.is_valid() and target.payloads.is_empty(), "named_constructor_binds_without_invoking", {"valid": callback.is_valid(), "payload_count": target.payloads.size()})
	var object_receiver: RefCounted = target
	object_receiver.call(&"record", "object_selector_data")
	_check(target.payloads == ["object_selector_data"], "Object_StringName_first_argument_is_selector", {"payloads": target.payloads.duplicate()})
	callback.call("_start_stuffie_battle")
	_check(target.payloads == ["object_selector_data", "_start_stuffie_battle"], "Callable_first_literal_is_payload_not_selector", {"payloads": target.payloads.duplicate()})
	var bound: Callable = callback.bind("bound_data")
	_check(target.payloads.size() == 2, "bind_does_not_invoke", {"payload_count": target.payloads.size()})
	bound.call()
	_check(target.payloads.back() == "bound_data" and target.payloads.size() == 3, "bound_arguments_delivered_on_invocation", {"payloads": target.payloads.duplicate()})
	var member: Callable = target.record
	member.call_deferred("member_deferred_data")
	object_receiver.call_deferred(&"record", "object_deferred_data")
	_local_record.call_deferred("local_method_deferred_data")
	_check(target.payloads.size() == 3 and local_payloads.is_empty(), "deferred_calls_are_not_immediate", {"target_count": target.payloads.size(), "local_count": local_payloads.size()})
	var lambda_payloads: Array[String] = []
	var lambda_callback: Callable = func(value: String) -> void: lambda_payloads.append(value)
	lambda_callback.call("record")
	_check(lambda_payloads == ["record"], "lambda_literal_is_payload", {"payloads": lambda_payloads.duplicate()})
	var default_target: DefaultTarget = DefaultTarget.new()
	_check(default_target is RefCounted, "default_script_class_is_RefCounted", {"native_class": default_target.get_class()})
	await process_frame
	await process_frame
	_check(target.payloads == ["object_selector_data", "_start_stuffie_battle", "bound_data", "member_deferred_data", "object_deferred_data"], "Object_and_bound_Callable_deferred_delivery", {"payloads": target.payloads.duplicate()})
	_check(local_payloads == ["local_method_deferred_data"], "unqualified_method_reference_is_Callable", {"payloads": local_payloads.duplicate()})
	var input_data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(input_path)) as Dictionary
	var query_names: Array = input_data.get("class_names", []) as Array
	var classes: Array[Dictionary] = []
	var not_registered: Array[String] = []
	for name_variant: Variant in query_names:
		var type_name: String = str(name_variant)
		if not ClassDB.class_exists(StringName(type_name)):
			not_registered.append(type_name)
			continue
		var is_object: bool = type_name == "Object" or ClassDB.is_parent_class(StringName(type_name), &"Object")
		var methods: Dictionary = {}
		var ambiguous_returns: Array[String] = []
		for method: Dictionary in ClassDB.class_get_method_list(StringName(type_name), false):
			var method_name: String = str(method.get("name", ""))
			var return_info: Dictionary = method.get("return", {}) as Dictionary
			var return_class: String = str(return_info.get("class_name", ""))
			var return_type: String = return_class if not return_class.is_empty() else type_string(int(return_info.get("type", TYPE_NIL)))
			if methods.has(method_name) and str(methods[method_name]) != return_type:
				ambiguous_returns.append(method_name)
			methods[method_name] = return_type
		for method_name: String in ambiguous_returns:
			methods[method_name] = ""
		var file_name: String = "native_classes/class_" + type_name.sha256_text().substr(0, 16) + ".json"
		var path: String = out_dir.path_join(file_name)
		_write_json(path, {"class_name": type_name, "is_object": is_object, "parent_class": str(ClassDB.get_parent_class(StringName(type_name))), "methods": methods, "ambiguous_return_names": ambiguous_returns, "scope": "Actual Native ClassDB ancestry/signatures only; queried class not instantiated."})
		classes.append({"class_name": type_name, "file": file_name, "bytes": FileAccess.get_file_as_bytes(path).size(), "sha256": FileAccess.get_sha256(path)})
	_check(not classes.is_empty(), "Native_ClassDB_evidence_collected", {"native_class_count": classes.size(), "not_registered_count": not_registered.size()})
	var after: Dictionary = _normal_hashes()
	_check(after == before, "normal_save_suffix_hashes_unchanged", {"before": before, "after": after})
	_write_json(out_dir.path_join("NATIVE_CLASS_INDEX.json"), {"schema": "reef.native_classdb_query_index/1", "source_revision": OS.get_environment("R45_REV"), "engine": engine, "input_sha256": FileAccess.get_sha256(input_path), "query_count": query_names.size(), "classes": classes, "not_native_registered": not_registered, "queried_classes_instantiated": 0, "game_instantiated": false, "art_captures": 0})
	_write_json(out_dir.path_join("SEMANTIC_PROOF.json"), {"schema": "reef.dispatch_engine_semantics/1", "source_revision": OS.get_environment("R45_REV"), "engine": engine, "display": DisplayServer.get_name(), "renderer_requested": "mobile", "renderer_reported": RenderingServer.get_current_rendering_method(), "scope": "Headless engine/language semantics, not a rendered Mobile scene/gameplay/art/QA11/device/child/owner pass.", "fixture_sha256": FileAccess.get_sha256("res://docs/handoffs/codex_flat_vector_art_2026-10-07/r45_dispatch_semantics_audit/probe_dispatch_semantics.gd"), "input_sha256": FileAccess.get_sha256(input_path), "checks": checks, "errors": errors, "normal_before": before, "normal_after": after, "normal_save_base": ProjectSettings.globalize_path("user://reef_save.json"), "game_instantiated": false, "art_captures": 0, "new_generation_calls": 0, "accepted_removed": 0, "mission_complete": false})
	print("DISPATCH45|RESULT|" + ("PASS" if errors.is_empty() else "FAIL") + "|checks=" + str(checks.size()) + "|classes=" + str(classes.size()))
	quit(0 if errors.is_empty() else 1)
