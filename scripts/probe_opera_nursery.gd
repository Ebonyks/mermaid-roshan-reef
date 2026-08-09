extends SceneTree
## Focused contract for Opera job #12: Nurse Roshan and Nurse Faron care for
## babies together on the five-beat arc (imp scuffle, care beats, the imp
## captain's peek-a-boo chase, then a cooperative stage finale). Falling
## babies require fresh input, misses are pillow-safe, mercy converges, and
## the care verbs stay distinct one-finger gestures.

var main: ReefMain
var bad := 0


func _init() -> void:
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	main.game = "opera"

	var config := (OperaHouse.ACTS[15] as Dictionary).duplicate(true)
	config["force_2d"] = true
	var touch_before := main.touch_ui.visible if main.touch_ui != null else false
	var old_save := SaveState.new(main)._normalise_save({
		"opera_progress": 15,
		"opera_stars": (1 << 15) - 1,
	})
	_check("old fifteen-bit Opera saves keep every historical star unchanged",
		int(old_save["opera_progress"]) == 15
		and int(old_save["opera_stars"]) == (1 << 15) - 1
		and (int(old_save["opera_stars"]) & (1 << 15)) == 0
		and OperaHouse.ALL_STARS == 65535)
	var act := OperaAct.new()
	get_root().add_child(act)
	act.start(main, config, Callable())
	await process_frame
	var world := act.career_world_2d
	_check("job twelve opens the dedicated Canvas nursery",
		act.kind == "nursery" and act.use_career_world_2d and world != null)
	if world == null:
		_finish()
		return

	_check("nursery has no clinic or Stuffie Surgeon engine",
		world.career_id == "nursery" and not world.PHASES["nursery"].is_empty()
		and world.phases.all(func(phase: Dictionary) -> bool:
			return String(phase.get("name", "")) not in ["X-RAY", "CAST", "BANDAGE"]))
	_check("Roshan and Faron use authored nursery actors",
		world.player_actor.texture != null and world.rival_actor.texture != null
		and act.competition.is_cooperative())
	_check("Nurse Faron stays beside Roshan as a cooperative partner",
		world.rival_actor.visible and act.competition.is_cooperative())
	_check("the care story keeps its beats inside the five-beat arc",
		world.phases.size() == 7
		and _phase_names(world) == ["IMPS!", "WASH HANDS", "CATCH BABIES", "FEED", "BABY CHASE", "BURP", "BEDTIME"])
	_check("the imp scuffle opens with no passive progress",
		world.phase_index == 0 and is_equal_approx(world.progress(), 0.0)
		and String((world.phases[0] as Dictionary).get("mode", "")) == "bop")
	_check_all_phase_reprompts(world)
	_check_timed_reprompt(world, "open-task re-prompt")

	_pump(world)
	_check("washing follows the scuffle with the basin tableau",
		world.phase_index == 1 and world.surface.visual_context == "basin_nursery")
	_check_timed_reprompt(world, "waiting-at-station re-prompt")
	_pump(world)
	var catcher := world.nursery_catch
	_check("catch phase reuses and expands the falling-baby grammar",
		world.phase_index == 2 and catcher != null and catcher.active
		and catcher.goal == 5 and catcher.textures.size() == 3
		and bool(catcher.get_meta("no_fail", false)))
	var passive_guard := 0
	while catcher.missed < 2 and passive_guard < 140:
		catcher._process(0.20)
		passive_guard += 1
	_check("falling babies never catch themselves without fresh touch",
		catcher.caught == 0 and catcher.missed >= 2 and world.phase_index == 2)
	_check("misses remain safe and invoke the mercy path",
		catcher.active and catcher.goal == 5 and catcher.missed >= 2)

	var catch_guard := 0
	while catcher.caught < 5 and catch_guard < 360:
		var target := catcher.lowest_baby_x()
		catcher.steer_to(target if target >= 0.0 else 0.5)
		catcher._process(0.12)
		catch_guard += 1
	# the cozy full-cradle scene holds before the next station arms
	var hold_guard := 0
	while world.phase_index == 2 and hold_guard < 40:
		world._process(0.1)
		hold_guard += 1
	_check("one-finger steering catches all five babies after safe misses",
		catcher.caught == 5 and world.phase_index == 3)
	world.phase_gap = 0.0
	_check("feeding uses a bottle hold tableau", world.surface.visual_context == "pour_nursery")
	_pump(world)
	var backdrop := world.get_node_or_null("OperaCareerWorld2D/CareerWorldBackdrop") as OperaWorldBackdrop2D
	_check("the imp captain's peek-a-boo chase happens at the stage door",
		world.phase_index == 4 and world.phase_index == world.steal_index
		and backdrop != null and backdrop.stage_mode)
	_pump(world)
	_check("the chase clears into the gentle burp-pat beat",
		world.phase_index == 5 and String((world.phases[5] as Dictionary).get("name", "")) == "BURP")
	# gentle pats: a pat inside the pace window pays nothing, so a drumming
	# finger cannot rush the baby — the probe waits between pats like a child
	var pat_guard := 0
	while world.phase_index == 5 and pat_guard < 40:
		world._on_gesture("tap", 1.0, 1.0)
		world._process(0.6)
		pat_guard += 1
	if world.phase_advance_pending:
		world._on_gesture("probe", 0.0, 1.0)
	_check("four gentle pats advance to bedtime",
		world.phase_index == 6 and world.surface.visual_context == "push_nursery")
	world.phase_gap = 0.0
	world._on_gesture("probe", 100.0, 1.0)
	# the tucked-in blanket holds on screen before the curtain call — let
	# that beat elapse the way a watching child would
	var tuck_guard := 0
	while act.state == "play" and tuck_guard < 40:
		world._process(0.1)
		tuck_guard += 1
	await process_frame
	_check("blanket tuck completes the cooperative nursery show",
		act.state == "won" and bool(act.performance_result.get("cooperative", false))
		and is_equal_approx(act.competition.player_progress, 1.0)
		and is_equal_approx(act.competition.rival_progress, 1.0))
	_check("curtain call celebrates cozy babies, not beating Faron",
		world.last_cheer == "THE BABIES ARE COZY!")
	act.cancel()
	await process_frame
	if main.touch_ui != null:
		_check("nursery restores the touch layer on exit", main.touch_ui.visible == touch_before)
	_finish()


func _pump(world: OperaCareerWorld2D) -> void:
	# complete the current phase, then swallow the between-phase sparkle sting
	world._on_gesture("probe", 100.0, 1.0)
	if world.phase_advance_pending:
		world._on_gesture("probe", 0.0, 1.0)
	world.phase_gap = 0.0


func _phase_names(world: OperaCareerWorld2D) -> Array[String]:
	var names: Array[String] = []
	for phase: Dictionary in world.phases:
		names.append(String(phase.get("name", "")))
	return names


func _check_all_phase_reprompts(world: OperaCareerWorld2D) -> void:
	var saved_phase_index: int = world.phase_index
	for index: int in range(world.phases.size()):
		var phase := world.phases[index] as Dictionary
		var speaker: String = String(phase.get("speaker", "Roshan"))
		var speaker_key: String = main._speaker_key(speaker)
		var vo: String = String(phase.get("vo", "hint"))
		var cue_key := "%s_%s" % [speaker_key, vo]
		var expected_path := "res://assets/audio/voices/%s.ogg" % cue_key
		main.clear_dialogue()
		main.said_cool.erase(cue_key)
		var before: int = main.voice_i
		world.phase_index = index
		world._repeat_phase_prompt()
		var actual_path := _last_voice_path()
		_check("%s re-prompt preserves speaker and cue" % String(phase.get("name", index)),
			main.voice_i == before + 1 and actual_path == expected_path)
		if speaker == "Faron":
			_check("%s re-prompt selects exact Faron clip" % String(phase.get("name", index)),
				actual_path == expected_path and expected_path.begins_with(
					"res://assets/audio/voices/faron_op_nursery_"))
	world.phase_index = saved_phase_index
	main.clear_dialogue()


func _check_timed_reprompt(world: OperaCareerWorld2D, label: String) -> void:
	var phase := world.phases[world.phase_index] as Dictionary
	var speaker_key: String = main._speaker_key(String(phase.get("speaker", "Roshan")))
	var vo: String = String(phase.get("vo", "hint"))
	var cue_key := "%s_%s" % [speaker_key, vo]
	main.clear_dialogue()
	main.said_cool.erase(cue_key)
	world.reveal_t = 0.0
	world.phase_advance_pending = false
	world.idle_t = 8.95
	var before: int = main.voice_i
	world._process(0.1)
	_check(label + " uses active phase identity",
		main.voice_i == before + 1
		and _last_voice_path() == "res://assets/audio/voices/%s.ogg" % cue_key)
	main.clear_dialogue()


func _last_voice_path() -> String:
	if main.voice_i <= 0 or main.voice_pool.is_empty():
		return "missing"
	var index := posmod(main.voice_i - 1, main.voice_pool.size())
	var player := main.voice_pool[index] as AudioStreamPlayer
	if player == null or player.stream == null:
		return "missing"
	return player.stream.resource_path


func _check(label: String, condition: bool) -> void:
	if condition:
		print("NURSERY|OK|", label)
	else:
		bad += 1
		print("NURSERY|FAIL|", label)


func _finish() -> void:
	if bad == 0:
		print("NURSERY|result: ALL OK")
		quit()
	else:
		print("NURSERY|result: %d FAIL" % bad)
		quit(1)
