extends "res://export/flat_vector_r58/capture_critter_book.gd"

func _snapshot() -> Dictionary:
	var result: Dictionary = super._snapshot()
	if is_instance_valid(m):
		result["message_timer"] = m.msg_timer
		result["message_text"] = m.hud_msg.text
		if m.castle_voice_caption != null:
			result["castle_caption"] = {"instance": m.castle_voice_caption.get_instance_id(), "visible": m.castle_voice_caption.is_visible_in_tree(), "rect": str(m.castle_voice_caption.get_global_rect()), "text": m.castle_voice_caption.text, "parent": str(m.castle_voice_caption.get_parent().get_path())}
	return result

func _exercise() -> void:
	if not await _boot():
		return
	await _capture("passive_private_checkpoint", "BOOTSTRAP_DIAGNOSTIC")
	if not await _open("passive"):
		return
	var before: Dictionary = m.critter_collection.duplicate(true)
	var started: int = Time.get_ticks_msec()
	await create_timer(10.0).timeout
	await _capture("book_after_10_real_seconds")
	_check("natural passive interval at least10seconds", Time.get_ticks_msec() - started >= 9900)
	_check("original caption expires naturally", m.msg_timer <= 0.0 and not m.castle_voice_caption.is_visible_in_tree())
	_check("passive book preserves category and collection", m.collection_category == "fish" and m.critter_collection == before)
	await _back("passive")
	await _retire()
