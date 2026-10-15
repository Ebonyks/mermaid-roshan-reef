extends "res://export/flat_vector_r65/capture_fit.gd"
## Additional original-input early-close evidence; no source/visual overrides.
var teardown_marks: Array[Dictionary] = []

func _snapshot() -> Dictionary:
	var result: Dictionary = super._snapshot()
	result["fixture_variant"] = "ORIGINAL_PICK_BURST_EARLY_CLOSE"
	result["teardown_marks"] = teardown_marks.duplicate(true)
	return result

func _close_live_feedback(use_done: bool, id: String) -> void:
	var layer: Control = m.wd.get("feedback_layer") as Control
	var tween: Tween = m.wd.get("feedback_tween") as Tween
	var burst: Node = layer.get_child(0) if layer != null and layer.get_child_count() == 1 else null
	var old_frame_ids: Array[int] = []
	for row: Dictionary in (_fit_details()["buttons"] as Array):
		if row.has("frame"):
			old_frame_ids.append(int((row["frame"] as Dictionary)["id"]))
	var mark: Dictionary = {"id": id, "use_done": use_done, "before_burst_count": int(_feedback()["burst_count"]),
		"old_burst_id": burst.get_instance_id() if burst != null else 0,
		"source_tween_valid_before": tween != null and tween.is_valid(), "source_closed": false, "owned_frame_ids": old_frame_ids}
	teardown_marks.append(mark)
	_check("live14shape source burst before close " + id, burst != null and burst.get_child_count() == 14 and tween != null and tween.is_valid())
	await _capture(id + "_feedback_live_before_close")
	var target: Control = _button("WardrobeFinishButton") if use_done else m.global_navigation_button
	if target == null:
		errors.append("original early-close target missing " + id)
		return
	await _tap(target, target.size * 0.5, id)
	await _frames(12)
	var surviving_frames: Array[int] = []
	for node_id: int in old_frame_ids:
		if is_instance_id_valid(node_id):
			surviving_frames.append(node_id)
	mark["surviving_frame_ids_after_12frames"] = surviving_frames
	_check("R65 owned five frames disposed by original close " + id, not refined_enabled or (old_frame_ids.size() == 5 and surviving_frames.is_empty()))
	mark["source_closed"] = m.wardrobe_layer == null and m.wd.is_empty()
	mark["source_tween_valid_after"] = tween != null and tween.is_valid()
	mark["old_burst_valid_after"] = is_instance_valid(burst)
	mark["wardrobe_block_after"] = m.touch_control_blocks.has("wardrobe")
	_check("original close cancels live tween " + id, tween != null and not tween.is_valid())
	_check("original close disposes burst/layer/state " + id, not is_instance_valid(burst) and bool(mark["source_closed"]))
	_check("original close releases wardrobe world block " + id, not m.touch_control_blocks.has("wardrobe"))
	await _capture(id + "_source_disposed")

func _exercise() -> void:
	if not await _boot():
		return
	await _capture("main_hall_checkpoint", "ORIGINAL_ROUTE_DIAGNOSTIC")
	if not await _go_room("royal_bedroom") or not await _open_original_wardrobe("early_close_initial"):
		return
	if not await _pick_original("huluu", "early_huluu_pick"):
		return
	await _close_live_feedback(false, "back_during_huluu_burst")
	_check("source Back retains privately saved source choice", m.skin_id == "huluu" and str(_disk().get("skin", "")) == "huluu")
	if not await _open_original_wardrobe("early_close_reopen"):
		return
	if not await _pick_original("classic", "early_restore_classic"):
		return
	await _close_live_feedback(true, "done_during_classic_burst")
	_check("source Done restores classic without unlock change", m.skin_id == "classic" and str(_disk().get("skin", "")) == "classic" and m.fairy_skin_unlocked == fairy_unlocked)
	_check("unknown private key retained during earlyclose", _state_equal(_disk().get("unknown"), seed.get("flat_vector_private_unknown")))
	await _capture("final_early_close_royal_bedroom")
	await _retire()
