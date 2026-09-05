extends SceneTree

const AUDIO_DIRECTOR_SCRIPT: GDScript = preload("res://scripts/audio_director.gd")
const MAIN_SCRIPT: GDScript = preload("res://scripts/main.gd")

var checks_failed: int = 0


func _init() -> void:
	var main = MAIN_SCRIPT.new()
	main.hud_msg = Label.new()
	main.add_child(main.hud_msg)
	var voice_player := AudioStreamPlayer.new()
	main.add_child(voice_player)
	main.voice_pool = [voice_player]
	var director: AudioDirector = AUDIO_DIRECTOR_SCRIPT.new(main) as AudioDirector
	var catalog: Dictionary = director.day_one_context_catalog()
	var rows: Variant = catalog.get("rows", [])
	_check("export-safe runtime catalog loaded", catalog.get("allow_generic", true) == false
		and rows is Array and (rows as Array).size() >= 40
		and director.day_one_context_catalog().has("rows"))
	_check("kitchen mandatory cues present", _has_cue(rows, "day1_fridge_open")
		and _has_cue(rows, "day1_fridge_close")
		and _has_cue(rows, "day1_recipe_ready"))
	_check("exact cue plays", director.say_day_one_context(
		"day1_bathroom_tub_drain", "Bye-bye bath water!", "bathroom", "probe"))
	_check("exact cue retains its contextual caption", main.hud_msg.visible
		and main.hud_msg.text == "Bye-bye bath water!")
	_check("same session cue is deduplicated", not director.say_day_one_context(
		"day1_bathroom_tub_drain", "Bye-bye bath water!", "bathroom", "probe"))
	_check("missing cue retains caption and does not play", not director.say_day_one_context(
		"day1_intentionally_missing", "Keep showing this helpful caption.", "kitchen", "probe")
		and main.hud_msg.text == "Keep showing this helpful caption."
		and main.hud_msg.visible
		and bool(main.hud_msg.get_meta("contextual_audio_missing", false)))
	_check("generic override fails closed", not director.say_day_one_context(
		"day1_bathroom_tub_drain", "Read this caption", "bathroom", "other", 0, true))
	_check("unknown cue fails closed", not director.say_day_one_context(
		"day1_unknown", "A helpful caption", "bathroom", "unknown"))
	main.free()
	_print_result()
	quit(1 if checks_failed > 0 else 0)


func _has_cue(rows: Array, cue_id: String) -> bool:
	for value: Variant in rows:
		if value is Dictionary and String((value as Dictionary).get("cue_id", "")) == cue_id:
			return true
	return false


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_CONTEXT|", label, ": ", "OK" if ok else "FAIL")


func _print_result() -> void:
	print("DAY_ONE_CONTEXT|RESULT: ", "PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
