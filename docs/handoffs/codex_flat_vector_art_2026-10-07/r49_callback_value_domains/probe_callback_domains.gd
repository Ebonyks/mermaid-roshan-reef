extends SceneTree
## R49 unchanged TouchUI component protocol with synthetic receivers, headless only.
class EchoTarget:
	extends RefCounted
	var events: Array[String] = []
	var positions: Array[String] = []
	var consume: bool = true
	func press(point: Vector2) -> void:
		events.append("press")
		positions.append(str(point))
	func cancel() -> void:
		events.append("cancel")
	func motion(point: Vector2) -> void:
		events.append("motion")
		positions.append(str(point))
	func probe(point: Vector2) -> bool:
		events.append("probe")
		positions.append(str(point))
		return consume
	func release() -> void:
		events.append("release")
	func drag() -> void:
		events.append("drag")
	func finish_drag(from: Vector2, to: Vector2) -> void:
		events.append("finish_drag")
		positions.append(str(from) + "->" + str(to))
	func bound_cancel(payload: String) -> void:
		events.append("bound:" + payload)

var checks: Array[Dictionary] = []
var errors: Array[String] = []
var ui: Variant

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var result: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old"]:
		var path := base + suffix
		result[suffix] = FileAccess.get_sha256(path) if FileAccess.file_exists(path) else "absent"
	return result

func _check(ok: bool, id: String, detail: Dictionary = {}) -> void:
	checks.append({"id": id, "pass": ok, "detail": detail})
	if not ok:
		errors.append(id)
	print("CALLBACK49|" + ("PASS|" if ok else "FAIL|") + id)

func _touch(pressed: bool, index: int, point: Vector2) -> InputEventScreenTouch:
	var event := InputEventScreenTouch.new()
	event.index = index
	event.pressed = pressed
	event.position = point
	return event

func _drag(index: int, point: Vector2) -> InputEventScreenDrag:
	var event := InputEventScreenDrag.new()
	event.index = index
	event.position = point
	return event

func _mouse(pressed: bool, point: Vector2, device_id: int = 0) -> InputEventMouseButton:
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.position = point
	event.device = device_id
	return event

func _motion(point: Vector2) -> InputEventMouseMotion:
	var event := InputEventMouseMotion.new()
	event.position = point
	return event

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official":
		quit(1)
		return
	var out_dir: String = OS.get_environment("R49_OUT")
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir):
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	var before := _normal_hashes()
	ui = load("res://scripts/touch_ui.gd").new()
	get_root().add_child(ui)
	ui.set_process(false)
	await process_frame
	var fields: Array[String] = ["encounter_press", "encounter_cancel", "encounter_motion", "world_press_probe", "world_press_release", "world_press_drag", "world_drag_end", "world_press_cancel"]
	var defaults: Dictionary = {}
	for field: String in fields:
		var callback: Callable = ui.get(field)
		defaults[field] = callback.is_valid()
	_check(defaults.values().all(func(value: Variant) -> bool: return not bool(value)), "all_eight_callbacks_default_empty", defaults)
	var first := EchoTarget.new()
	var second := EchoTarget.new()
	ui.world_press_probe = first.probe
	ui.world_press_release = first.release
	ui.world_press_drag = first.drag
	ui.world_drag_end = first.finish_drag
	ui.world_press_cancel = first.cancel
	ui.set_encounter_controls(first.press, first.cancel, first.motion)
	_check(first.events == ["cancel"], "setter_cancels_previous_world_hold_before_binding", {"events": first.events.duplicate()})
	var cb_press: Callable = ui.encounter_press
	var cb_cancel: Callable = ui.encounter_cancel
	var cb_motion: Callable = ui.encounter_motion
	_check(cb_press.get_object() == first and cb_press.get_method() == &"press" and cb_cancel.get_object() == first and cb_cancel.get_method() == &"cancel" and cb_motion.get_object() == first and cb_motion.get_method() == &"motion", "setter_preserves_exact_object_and_method_identity")
	first.events.clear()
	ui._encounter_unhandled_input(_touch(true, 7, Vector2(500, 200)))
	ui._encounter_unhandled_input(_touch(true, 8, Vector2(550, 200)))
	_check(first.events == ["press"], "second_finger_cannot_replace_primary_press")
	ui._encounter_unhandled_input(_drag(8, Vector2(600, 230)))
	_check(first.events == ["press"], "foreign_finger_motion_is_ignored")
	ui._encounter_unhandled_input(_drag(7, Vector2(600, 240)))
	_check(first.events == ["press", "motion"], "primary_finger_motion_routes_to_bound_method")
	ui._encounter_unhandled_input(_touch(false, 8, Vector2(600, 230)))
	_check(int(ui._encounter_finger) == 7, "foreign_release_does_not_release_primary")
	ui._encounter_unhandled_input(_touch(false, 7, Vector2(600, 240)))
	_check(int(ui._encounter_finger) == -1 and first.events == ["press", "motion"], "primary_release_clears_owner_without_new_press")
	first.events.clear()
	ui._encounter_unhandled_input(_mouse(true, Vector2(500, 200), InputEvent.DEVICE_ID_EMULATION))
	_check(first.events.is_empty(), "emulated_mouse_does_not_duplicate_touch")
	ui._encounter_unhandled_input(_mouse(true, Vector2(500, 200)))
	ui._encounter_unhandled_input(_motion(Vector2(560, 220)))
	ui._encounter_unhandled_input(_mouse(false, Vector2(560, 220)))
	_check(first.events == ["press", "motion"] and int(ui._encounter_finger) == -1, "real_mouse_press_motion_release_routes_same_protocol")
	first.events.clear()
	ui.set_encounter_controls(second.press, second.cancel, second.motion)
	_check(first.events == ["cancel", "cancel"] and second.events.is_empty(), "rebind_calls_old_encounter_and_world_cancels_before_new_owner")
	ui._encounter_unhandled_input(_touch(true, 1, Vector2(500, 200)))
	ui._encounter_unhandled_input(_touch(false, 1, Vector2(500, 200)))
	_check(second.events == ["press"] and first.events == ["cancel", "cancel"], "new_presses_reach_new_owner_only")
	ui.set_encounter_controls()
	var empty_press: Callable = ui.encounter_press
	var empty_cancel: Callable = ui.encounter_cancel
	var empty_motion: Callable = ui.encounter_motion
	_check(not empty_press.is_valid() and not empty_cancel.is_valid() and not empty_motion.is_valid(), "default_reset_empties_all_encounter_callbacks")
	_check(second.events == ["press", "cancel"], "reset_delivers_old_cancel_once")
	first.events.clear()
	ui._hybrid_unhandled_input(_touch(true, 2, Vector2(900, 200)))
	ui._hybrid_unhandled_input(_drag(2, Vector2(950, 240)))
	ui._hybrid_unhandled_input(_touch(false, 2, Vector2(950, 240)))
	_check(first.events == ["probe", "drag", "release"], "consumed_touch_delivers_probe_drag_release_without_swipe", {"events": first.events.duplicate()})
	first.events.clear()
	ui._hybrid_unhandled_input(_mouse(true, Vector2(1000, 200)))
	ui._hybrid_unhandled_input(_motion(Vector2(1050, 240)))
	ui._hybrid_unhandled_input(_mouse(false, Vector2(1050, 240)))
	_check(first.events == ["probe", "drag", "release"], "consumed_mouse_delivers_probe_drag_release_without_swipe", {"events": first.events.duplicate()})
	first.events.clear()
	first.consume = false
	ui._hybrid_unhandled_input(_touch(true, 3, Vector2(900, 200)))
	ui._hybrid_unhandled_input(_drag(3, Vector2(970, 250)))
	ui._hybrid_unhandled_input(_touch(false, 3, Vector2(970, 250)))
	_check(first.events == ["probe", "finish_drag"], "unconsumed_drag_reaches_swipe_callback_once", {"events": first.events.duplicate()})
	first.events.clear()
	ui._clear_touch_state()
	_check(first.events == ["cancel"], "world_cancel_has_priority_over_release_on_reset")
	first.events.clear()
	ui.world_press_cancel = Callable()
	ui._clear_touch_state()
	_check(first.events == ["release"], "world_release_is_reset_fallback_when_cancel_empty")
	ui.world_press_release = Callable()
	first.events.clear()
	ui.set_encounter_controls(Callable(), Callable(first, "bound_cancel").bind("literal_payload"), Callable())
	ui._clear_touch_state()
	_check(first.events == ["bound:literal_payload"], "bound_literal_remains_callback_data_in_actual_component")
	ui.set_encounter_controls()
	ui.queue_free()
	await process_frame
	ui = null
	var after := _normal_hashes()
	_check(before == after, "normal_eight_save_suffix_hashes_unchanged", {"before": before, "after": after})
	var result: Dictionary = {"schema": "reef.callback_component_evidence/1", "source_revision": OS.get_environment("R49_REV"), "engine": engine, "display": DisplayServer.get_name(), "renderer_requested": "mobile", "renderer_reported": RenderingServer.get_current_rendering_method(), "scope": "Actual unchanged TouchUI component methods with synthetic receivers in headless SceneTree. No Main/game instance, game render, art/route or QA11/device/child/owner acceptance.", "fixture_sha256": FileAccess.get_sha256("res://docs/handoffs/codex_flat_vector_art_2026-10-07/r49_callback_value_domains/probe_callback_domains.gd"), "checks": checks, "errors": errors, "normal_before": before, "normal_after": after, "game_instantiated": false, "art_captures": 0, "accepted_removed": 0, "mission_complete": false}
	var file := FileAccess.open(out_dir.path_join("COMPONENT_PROOF.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify(result, "\t", true) + "\n")
	file.close()
	print("CALLBACK49|RESULT|" + ("PASS" if errors.is_empty() else "FAIL") + "|checks=" + str(checks.size()))
	quit(0 if errors.is_empty() else 1)
