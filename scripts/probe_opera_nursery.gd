extends SceneTree
## Focused contract for Opera job #12: Nurse Roshan and Nurse Faron care for
## babies together on a five-beat care arc with no pasted-in combat. Falling
## babies require fresh input, misses are pillow-safe, mercy converges, and
## every beat remains a distinct one-finger nursery verb.

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
		world.phases.size() == 5
		and _phase_names(world) == ["WASH HANDS", "CATCH BABIES", "FEED", "BURP", "BEDTIME"])
	_check("hand washing opens with no passive progress or copied combat",
		world.phase_index == 0 and is_equal_approx(world.progress(), 0.0)
		and String((world.phases[0] as Dictionary).get("mode", "")) == "hold"
		and world.surface.visual_context == "basin_nursery")

	_pump(world)
	var catcher := world.nursery_catch
	_check("catch phase reuses and expands the falling-baby grammar",
		world.phase_index == 1 and catcher != null and catcher.active
		and catcher.goal == 5 and catcher.textures.size() == 3
		and bool(catcher.get_meta("no_fail", false)))
	var passive_guard := 0
	while catcher.missed < 2 and passive_guard < 140:
		catcher._process(0.20)
		passive_guard += 1
	_check("falling babies never catch themselves without fresh touch",
		catcher.caught == 0 and catcher.missed >= 2 and world.phase_index == 1)
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
	while world.phase_index == 1 and hold_guard < 40:
		world._process(0.1)
		hold_guard += 1
	_check("one-finger steering catches all five babies after safe misses",
		catcher.caught == 5 and world.phase_index == 2)
	world.phase_gap = 0.0
	_check("feeding uses a bottle hold tableau", world.surface.visual_context == "pour_nursery")
	_pump(world)
	_check("feeding clears into the gentle burp-pat beat without an imp chase",
		world.phase_index == 3 and world.steal_index < 0
		and String((world.phases[3] as Dictionary).get("name", "")) == "BURP")
	# gentle pats: a pat inside the pace window pays nothing, so a drumming
	# finger cannot rush the baby — the probe waits between pats like a child
	var pat_guard := 0
	while world.phase_index == 3 and pat_guard < 40:
		world._on_gesture("tap", 1.0, 1.0)
		world._process(0.6)
		pat_guard += 1
	if world.phase_advance_pending:
		world._on_gesture("probe", 0.0, 1.0)
	_check("four gentle pats advance to bedtime",
		world.phase_index == 4 and world.surface.visual_context == "push_nursery")
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
