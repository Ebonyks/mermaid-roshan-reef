extends "res://export/flat_vector_r72/capture_skyway.gd"
const PointerRegistration = preload("res://export/flat_vector_r72/pointer_registration.gd")
var tip_candidate: RefCounted
var pointer_comparisons: Array[Dictionary] = []
var hint_cycles: Array[Dictionary] = []
var hint_inputs: Array[Dictionary] = []
var witness_events: Array[Dictionary] = []
var input_witness: InputWitness

class InputWitness extends Node:
	var observations: Array[Dictionary] = []
	func _input(event: InputEvent) -> void:
		if event is InputEventScreenTouch or event is InputEventMouseButton or event is InputEventKey:
			observations.append({"event": event.as_text(), "ticks_msec": Time.get_ticks_msec()})

func _boot() -> bool:
	if input_witness == null:
		input_witness = InputWitness.new()
		input_witness.name = "R72ReadOnlyInputWitness"
		root.add_child(input_witness)
	return await super()

func _witness_navigation() -> void:
	witness_events.append({"event": "source_global_navigation_pressed", "ticks_msec": Time.get_ticks_msec(), "stack": get_stack()})


func _tip_state() -> Dictionary:
	if not is_instance_valid(m) or m.fairy_conservatory_handoff == null:
		return {}
	var handoff: RefCounted = m.fairy_conservatory_handoff
	var pointer: Sprite2D = handoff.get("_pointer") as Sprite2D
	var world: Node2D = handoff.get("_world") as Node2D
	if pointer == null or world == null:
		return {}
	var snap: Dictionary = handoff.call("audit_snapshot") as Dictionary
	var tip_region: Vector2 = Vector2(1.0, 6.5) if OS.get_environment("R72_HAND") == "painted" else Vector2(217.0, 447.0)
	var draw_rect: Rect2 = pointer.get_rect()
	var source_point: Vector2 = draw_rect.position + tip_region
	var native_tip: Vector2 = pointer.get_global_transform_with_canvas() * source_point
	var target: Vector2 = handoff.call("_next_waypoint") as Vector2
	var native_target: Vector2 = world.get_global_transform_with_canvas() * target
	var rect: Rect2
	if str(snap["state"]) == "butterfly_house":
		var button: Control = handoff.get("_house_button") as Control
		rect = button.get_global_rect()
	else:
		var half: Vector2 = FairyConservatoryHandoff2D.MIN_TOUCH * 0.5
		var top: Vector2 = world.get_global_transform_with_canvas() * (target - half)
		var bottom: Vector2 = world.get_global_transform_with_canvas() * (target + half)
		rect = Rect2(top, bottom - top)
	return {"state": snap["state"], "index": snap["waypoint_index"], "phase": float(handoff.get("_pointer_phase")), "native_tip": _safe(native_tip), "native_target": _safe(native_target), "target_rect": [rect.position.x, rect.position.y, rect.size.x, rect.size.y], "inside": rect.has_point(native_tip), "pointer_position": _safe(pointer.position), "pointer_offset": _safe(pointer.offset), "pointer_scale": _safe(pointer.scale), "texture": _tex(pointer.texture), "hand_variant": OS.get_environment("R72_HAND"), "pointer_region_enabled": pointer.region_enabled, "pointer_region_rect": [pointer.region_rect.position.x, pointer.region_rect.position.y, pointer.region_rect.size.x, pointer.region_rect.size.y], "pointer_rotation": pointer.rotation, "pointer_draw_rect": [draw_rect.position.x, draw_rect.position.y, draw_rect.size.x, draw_rect.size.y], "tip_region": _safe(tip_region), "ticks_msec": Time.get_ticks_msec()}

func _store_hint_evidence() -> void:
	var file: FileAccess = FileAccess.open(out_dir.path_join("hint_cycles.json"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"schema": "reef.pointer_hint_cycles/1", "input_witness": input_witness.observations if input_witness != null else [], "navigation_witness": witness_events, "variant": OS.get_environment("R72_HINT"), "source_revision": OS.get_environment("R72_REV"), "cycles": hint_cycles, "inputs": hint_inputs, "pointer_comparisons": pointer_comparisons, "source_tip_alpha64": [1.0, 6.5] if OS.get_environment("R72_HAND") == "painted" else [217, 447], "hand_variant": OS.get_environment("R72_HAND"), "generation_calls": 0, "new_art_status": "EXISTING_ART_REUSE_NO_GENERATION_OR_EXPORT"}, "\t", true) + "\n")
	file.close()

func _sample_hint_cycle() -> bool:
	var first: Dictionary = _tip_state()
	if first.is_empty():
		errors.append("source pointer absent before cue cycle")
		return false
	var samples: Array[Dictionary] = []
	var start_phase: float = float(first["phase"])
	for index: int in range(100):
		var sample: Dictionary = _tip_state()
		if sample.is_empty():
			errors.append("source handoff disappeared during passive cue cycle")
			hint_cycles.append({"state": first["state"], "index": first["index"], "phase_span": float(samples[-1]["phase"]) - start_phase if not samples.is_empty() else 0.0, "bob_phase_span_radians": (float(samples[-1]["phase"]) - start_phase) * 4.0 if not samples.is_empty() else 0.0, "samples": samples, "outside_count": 0, "registration_status": "ABORTED_SOURCE_EXIT_NO_REGISTRATION_CREDIT"})
			_store_hint_evidence()
			return false
		samples.append(sample)
		if (float(sample["phase"]) - start_phase) * 4.0 >= TAU + 0.1:
			break
		await process_frame
	var outside: int = 0
	for sample: Dictionary in samples:
		if not bool(sample["inside"]):
			outside += 1
	var span: float = float(samples[-1]["phase"]) - start_phase
	var summary: Dictionary = {"state": first["state"], "index": first["index"], "phase_span": span, "phase_span_seconds": span, "bob_phase_span_radians": span * 4.0, "samples": samples, "outside_count": outside, "inside_count": samples.size() - outside, "registration_status": "FAIL_SOURCE_TIP_OUTSIDE_TOUCH_TARGET" if outside > 0 else "BOUNDED_TIP_INSIDE_TARGET", "artwork_status": "EXISTING_PAINTED_REGION_UNACCEPTED" if OS.get_environment("R72_HAND") == "painted" else "EXISTING_FLAT_CONTROL"}
	hint_cycles.append(summary)
	_check("full natural bob cycle observed " + str(first["index"]), span * 4.0 >= TAU)
	_check("zero-input cue cycle keeps source progress " + str(first["index"]), int((_tip_state())["index"]) == int(first["index"]))
	if OS.get_environment("R72_HINT") == "registered":
		_check("registered visual tip stays in original target " + str(first["index"]), outside == 0)
	elif str(first["state"]) != "butterfly_house":
		_check("source cycle reproduces cue registration weakness " + str(first["index"]), outside > 0)
	_store_hint_evidence()
	return true

func _snapshot() -> Dictionary:
	var result: Dictionary = super()
	result["input_witness"] = input_witness.observations if input_witness != null else []
	result["navigation_witness"] = witness_events.duplicate(true)
	result["hand_variant"] = OS.get_environment("R72_HAND")
	result["hint_variant"] = OS.get_environment("R72_HINT")
	result["tip_state"] = _tip_state()
	result["pointer_comparisons"] = pointer_comparisons.duplicate(true)
	var summaries: Array[Dictionary] = []
	for cycle: Dictionary in hint_cycles:
		summaries.append({"state": cycle["state"], "index": cycle["index"], "phase_span_seconds": cycle["phase_span"], "bob_phase_span_radians": cycle["bob_phase_span_radians"], "sample_count": (cycle["samples"] as Array).size(), "outside_count": cycle["outside_count"], "registration_status": cycle["registration_status"]})
	result["hint_cycle_summaries"] = summaries
	result["pointer_registration"] = tip_candidate.call("audit_snapshot") if tip_candidate != null else {}
	return result

func _enter_handoff(prefix: String) -> bool:
	if not await super(prefix):
		return false
	var navigation: Button = _button("GlobalNavigationButton") as Button
	if not navigation.pressed.is_connected(_witness_navigation):
		navigation.pressed.connect(_witness_navigation)
	var before: Dictionary = _preserved_signature()
	var pointer: Sprite2D = m.fairy_conservatory_handoff.get("_pointer") as Sprite2D
	var original_offset: Vector2 = pointer.offset
	if OS.get_environment("R72_HINT") == "registered":
		tip_candidate = PointerRegistration.new()
		var applied: bool = bool(tip_candidate.call("apply", m.fairy_conservatory_handoff))
		_check("registration uses original node and bound artwork " + prefix, applied)
		if not applied:
			return false
	var after: Dictionary = _preserved_signature()
	pointer_comparisons.append({"entry": prefix, "variant": OS.get_environment("R72_HINT"), "before": before, "after": after, "unchanged_except_declared_pointer_draw_properties": before == after, "original_offset": _safe(original_offset), "new_offset": _safe(pointer.offset), "actual_texture": _tex(pointer.texture), "declared_pointer_draw_delta": tip_candidate.call("audit_snapshot") if tip_candidate != null else {}})
	_check("pointer patch preserves source/controller/control/other geometry " + prefix, before == after)
	await _frames(3)
	await _capture(prefix + "_hint_" + OS.get_environment("R72_HINT"))
	_store_hint_evidence()
	return true

func _waypoint_tap(returning: bool) -> bool:
	if returning:
		return await super(returning)
	if not await _sample_hint_cycle():
		return false
	var before: Dictionary = _tip_state()
	if OS.get_environment("R72_HINT") == "source":
		if not await _wait(func() -> bool: return not bool(_tip_state().get("inside", true)), 3.0):
			errors.append("source cue outside phase not observed")
			return false
		before = _tip_state()
		var point: Array = before["native_tip"] as Array
		hint_inputs.append({"role": "original_rendered_fingertip", "before": before, "expected": "NO_ADVANCE_OUTSIDE_SOURCE_TARGET"})
		await _raw_tap(Vector2(float(point[0]), float(point[1])))
		await _frames(4)
		_check("source displayed-tip tap misses original target " + str(before["index"]), int((_tip_state())["index"]) == int(before["index"]))
		await _capture("hint_source_miss_%02d" % int(before["index"]))
		_store_hint_evidence()
		return await super(returning)
	var point: Array = before["native_tip"] as Array
	hint_inputs.append({"role": "registered_rendered_fingertip", "before": before, "expected": "ADVANCE_ORIGINAL_TARGET"})
	await _raw_tap(Vector2(float(point[0]), float(point[1])))
	await _frames(4)
	var after: Dictionary = _tip_state()
	_check("registered rendered-tip input advances source " + str(before["index"]), not after.is_empty() and int(after["index"]) == int(before["index"]) + 1)
	_store_hint_evidence()
	return not after.is_empty()

func _tap(control: Control, local_point: Vector2, id: String = "") -> void:
	if control != null and str(control.name) == "ButterflyHouseHotspot":
		if not await _sample_hint_cycle():
			return
		var tip: Dictionary = _tip_state()
		_check("house displayed tip lies within original Button", bool(tip["inside"]))
		var point: Array = tip["native_tip"] as Array
		hint_inputs.append({"role": "rendered_fingertip_house_button", "before": tip, "expected": "ORIGINAL_HOUSE_BUTTON_CALLBACK"})
		_store_hint_evidence()
		await _raw_tap(Vector2(float(point[0]), float(point[1])))
		return
	await super(control, local_point, id)

func _preserved_signature() -> Dictionary:
	var result: Dictionary = super()
	if result.has("pointer"):
		var pointer: Dictionary = result["pointer"] as Dictionary
		# Intended draw delta: original pointer texture/scale plus region/rotation/offset.
		# Preserve source node identity/position/z/visibility/modulation and all other fields.
		pointer.erase("texture")
		pointer.erase("scale")
	return result
