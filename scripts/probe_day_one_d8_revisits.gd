extends SceneTree
## Fail-closed source contract for the WP-D8 revisit polish.
##
## The runtime probes own the visual/interaction paths; this narrow contract
## prevents the bounded safety seams from silently disappearing when a later
## refactor moves them. It intentionally checks source authority, not prose.

var failures := 0


func _init() -> void:
	call_deferred("_run_probe")


func _run_probe() -> void:
	var castle := _read("res://scripts/arena/castle_rooms_25d.gd")
	var main := _read("res://scripts/main.gd")
	var audio := _read("res://scripts/audio_director.gd")
	var art := _read("res://scripts/day_one_art_studio.gd")
	var contextual_catalog := _read(
		"res://scripts/day_one_contextual_voice_catalog.gd")
	_check("blocked door has bounded constants",
		castle.contains("BLOCKED_DOOR_SFX_COOLDOWN_SECONDS := 1.2")
		and castle.contains("BLOCKED_DOOR_SECOND_TAP_WINDOW_SECONDS := 6.0"))
	_check("second blocked tap pulses and pans",
		castle.contains("cue.pulse_plot_feedback()")
		and castle.contains("_pan_to_blocked_door(destination_id)")
		and castle.contains("_blocked_door_last_tap.erase(destination_id)"))
	_check("blocked feedback SFX is cooldown guarded",
		castle.contains("if _blocked_door_feedback_cool <= 0.0:")
		and castle.contains("BLOCKED_DOOR_SFX_COOLDOWN_SECONDS"))
	var clean_voice_pos: int = main.find('"day_one_room_clean", 6.0)')
	var clean_response_pos: int = main.find(
		"play_day_one_completed_room_response(logical_room)")
	_check("completed room is one semantic voice at six seconds",
		clean_voice_pos >= 0
		and clean_response_pos > clean_voice_pos
		and main.contains("voice_min_gap: float = 0.5"))
	_check("completed fixture replay cannot reward or launch",
		castle.contains("play_day_one_completed_room_response")
		and castle.contains('playback_data.erase("launch_activity")')
		and castle.contains('m.g["day_one_completed_room_response_reward"] = false')
		and castle.contains('sprite.remove_meta("launch_activity_after_sequence")')
		and castle.contains(
			"_play_sprite_atlas_sequence(sprite, playback_data, false, false)"))
	_check("completed bathroom restores real navigation",
		main.contains("if bathroom_route_owned:")
		and main.contains("_restore_day_one_bathroom_controls()")
		and main.contains("and _day_one_pool_route_button != null"))
	_check("Rumi revisit is persistent and contextual",
		castle.contains("_sync_day_one_persistent_rumi()")
		and castle.contains("Pool completion flips the persistent-meeting latch")
		and castle.contains('name = "DayOnePersistentRumi"')
		and castle.contains('persistent_day_one_friend", true')
		and castle.contains('_say_day_one_context("day1_pool_rumi_reply"')
		and contextual_catalog.contains(
			'"cue_id":"day1_pool_rumi_reply"')
		and contextual_catalog.contains(
			'"audio_path":"assets/audio/voices/filler_v1/roshan_day1_pool_rumi_reply.ogg"')
		and contextual_catalog.contains('"route":"pool"')
		and contextual_catalog.contains('"status":"READY"')
		and not castle.contains(
			'm.show_msg("Roshan", "Hi Roshan!", "day_one_rumi_hi"'))
	_check("Rumi contextual route preserves protected speaker exclusions",
		audio.contains('var protected_speaker := speaker in ["faron", "daddy", "chuck"]')
		and audio.contains(
			'var allow_exact_filler := not protected_speaker or speaker == "daddy"')
		and audio.contains('if not protected_speaker:')
		and not audio.contains('"rumi_day_one_rumi_hi"'))
	_check("documented loose-brush typo is gone",
		art.contains('"Tap the %s!" % String(material["label"])')
		and not art.contains('"Tap the loose %s!" % String(material["label"])'))
	if failures == 0:
		print("DAY_ONE_D8_REVISITS|RESULT: ALL OK")
	else:
		print("DAY_ONE_D8_REVISITS|RESULT: ", failures, " failure(s)")
	quit(failures)


func _read(path: String) -> String:
	if not FileAccess.file_exists(path):
		return ""
	var file := FileAccess.open(path, FileAccess.READ)
	return file.get_as_text() if file != null else ""


func _check(label: String, passed: bool) -> void:
	if not passed:
		failures += 1
	print("DAY_ONE_D8_REVISITS|", label, ": ", "OK" if passed else "FAIL")
