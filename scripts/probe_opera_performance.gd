extends SceneTree
## Connected contract for the three literal Opera Hall two-act performances.

const Mastery := preload("res://scripts/opera_mastery.gd")
const PerformancePlan := preload("res://scripts/opera_performance_plan.gd")
const BalletSurface := preload("res://scripts/opera_ballet_surface.gd")

const VENUE_CAREERS: Array[String] = ["ballerina", "magician", "popstar"]

var main: ReefMain
var failures := 0
var house_completions: Array[bool] = []


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	main.game = "opera"
	main.save_data["opera_mastery"] = Mastery.normalise({})
	main.save_data["opera_performance_checkpoints"] = {}
	for career: String in VENUE_CAREERS:
		main.medals.erase("opera_" + career)

	await _probe_three_runtime_plans()
	await _probe_story_opt_out()
	await _probe_stage_checkpoint_and_rival()
	await _probe_current_mechanic_restore()
	await _probe_award_and_replay()
	if failures == 0:
		print("OPERAPERFORMANCE|result: ALL OK")
		quit(0)
	else:
		print("OPERAPERFORMANCE|result: %d FAIL" % failures)
		quit(1)


func _probe_three_runtime_plans() -> void:
	var all_three_exact := PerformancePlan.ENABLED == VENUE_CAREERS
	var no_practice_stats := true
	var ballet_touch_real := false
	for career: String in VENUE_CAREERS:
		var config := _career_config(career)
		var act := OperaAct.new()
		get_root().add_child(act)
		var started := act.start(main, config, Callable())
		await process_frame
		var world: OperaCareerWorld2D = act.career_world_2d
		var base: Array = OperaCareerWorld2D.PHASES[career]
		all_three_exact = all_three_exact and started and world != null \
			and world.two_act_enabled and world.performance_stage_start == 3 \
			and world.phases.size() == base.size() + 3 \
			and world.performance_overlay != null \
			and world.performance_overlay.mouse_filter == Control.MOUSE_FILTER_IGNORE \
			and world.performance_overlay.find_children("*", "Button", true, false).is_empty()
		if world == null:
			act.cancel()
			continue
		for index in range(world.phases.size()):
			var phase: Dictionary = world.phases[index]
			var source_index := int(phase.get("source_phase", -1))
			var expected: Dictionary = base[source_index] if source_index >= 0 \
				and source_index < base.size() else {}
			all_three_exact = all_three_exact and not expected.is_empty() \
				and String(phase.get("name", "")) == String(expected.get("name", "")) \
				and String(phase.get("mode", "")) == String(expected.get("mode", "")) \
				and is_equal_approx(float(phase.get("goal", 0.0)),
					float(expected.get("goal", -1.0))) \
				and String(phase.get("performance_part", "")) \
					== ("practice" if index < 3 else "stage")

		world._performance_input("choice", 0.0)
		world._performance_record_progress(1.0, "choice", 1.0)
		world._performance_tick(12.0)
		no_practice_stats = no_practice_stats \
			and world.performance_stats == {
				"actions": 0, "misses": 0, "assists": 0, "active_seconds": 0.0} \
			and Mastery.evaluate(career, world.performance_result_stats()) == Mastery.NONE
		if career == "ballerina":
			world._open_task()
			var ballet: Variant = world.surface
			ballet._process(BalletSurface.POSE_DEMO_SECONDS + 0.1)
			var frames: Array[int] = ballet.pose_option_frames()
			var rects: Array[Rect2] = ballet.pose_option_rects()
			var target_index := frames.find(ballet.pose_target_frame())
			var before := world.phase_progress
			if target_index >= 0:
				_touch(ballet, rects[target_index].get_center())
			ballet_touch_real = target_index >= 0 and world.phase_progress > before \
				and int(world.performance_stats["actions"]) == 0 \
				and int(world.performance_stats["misses"]) == 0
		act.cancel()
		await process_frame
	_check("all three Opera Hall careers repeat their exact verbs from practice on stage",
		all_three_exact)
	_check("practice input, misses, time, and completion cannot enter mastery",
		no_practice_stats)
	_check("Ballerina practice accepts a genuine touch without creating stage stats",
		ballet_touch_real)


func _probe_story_opt_out() -> void:
	var before: Dictionary = main.save_data["opera_mastery"].duplicate(true)
	var config := _career_config("ballerina")
	config["reward_policy"] = "chapter2_story"
	var act := OperaAct.new()
	get_root().add_child(act)
	act.start(main, config, Callable())
	await process_frame
	var world := act.career_world_2d
	var untouched := world != null and not world.two_act_enabled \
		and world.phases.size() == (OperaCareerWorld2D.PHASES["ballerina"] as Array).size()
	act._win()
	untouched = untouched and main.save_data["opera_mastery"] == before \
		and not main.medals.has("opera_ballerina")
	act.cancel()
	await process_frame
	_check("scripted story lessons neither expand nor award Opera mastery", untouched)


func _probe_stage_checkpoint_and_rival() -> void:
	var config := _career_config("magician")
	var act := OperaAct.new()
	get_root().add_child(act)
	act.start(main, config, Callable())
	await process_frame
	var world := act.career_world_2d
	var choice_source := _source_phase_with_mode("magician", "choice")
	world.phase_index = world.performance_stage_start + choice_source
	world._arm_phase()
	var hotspots_hidden := not world.wander_layer.visible and world.task_open \
		and world.backdrop_node.stage_mode and world.performance_overlay.on_stage
	for hotspot: OperaWorldHotspot2D in world.station_nodes:
		hotspots_hidden = hotspots_hidden and not hotspot.armed
	var mastery_before: Dictionary = main.save_data["opera_mastery"].duplicate(true)
	world._performance_tick(15.0)
	var passive_safe: bool = not world.performance_started and not world.competition.active \
		and is_zero_approx(float(world.performance_stats["active_seconds"])) \
		and is_zero_approx(world.competition.rival_progress) \
		and main.save_data["opera_mastery"] == mastery_before

	var progress_before := world.phase_progress
	_touch_choice(world)
	var real_choice_started := world.phase_progress > progress_before \
		and world.performance_started and world.competition.active
	world._performance_tick(1.25)
	var active_before_pause := float(world.performance_stats["active_seconds"])
	world._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	world._performance_tick(30.0)
	var pause_safe := active_before_pause > 0.0 \
		and is_equal_approx(float(world.performance_stats["active_seconds"]),
			active_before_pause)

	_touch_choice(world)
	act._process(float(world.competition.spec["par_time"]) * 3.0)
	var imp_finishes_honestly: bool = world.competition.rival_progress >= 0.999 \
		and act.state == "play" and world.phase_index < world.phases.size() \
		and main.save_data["opera_mastery"] == mastery_before
	world._performance_note_help()
	world._performance_record_progress(0.5, "choice", 1.0)
	world._performance_checkpoint(false)
	var saved_phase := world.phase_index
	var saved_stats: Dictionary = world.performance_stats.duplicate(true)
	var saved_milestones: Dictionary = world.performance_milestones.duplicate(true)
	act.cancel()
	await process_frame

	var resumed := OperaAct.new()
	get_root().add_child(resumed)
	resumed.start(main, config, Callable())
	await process_frame
	var restored := resumed.career_world_2d
	var restore_exact := restored != null and restored.phase_index == saved_phase \
		and restored.performance_stats == saved_stats \
		and restored.performance_milestones == saved_milestones \
		and restored.task_open and restored.backdrop_node.stage_mode \
		and restored.performance_overlay.on_stage
	resumed.cancel()
	await process_frame
	_check("stage opens on its painting with every room hotspot hidden", hotspots_hidden)
	_check("stage remains passive until a genuine choice touch", passive_safe)
	_check("a genuine stage choice starts both measured performers", real_choice_started)
	_check("paused time never enters the active performance clock", pause_safe)
	_check("the imp may finish first without forcing a loss, retry, or award",
		imp_finishes_honestly)
	_check("stage phase, metrics, quarters, and help resume from checkpoint",
		restore_exact and int(saved_stats["assists"]) == 1)


func _probe_award_and_replay() -> void:
	main.save_data["opera_performance_checkpoints"] = {}
	var first := await _run_house_performance("popstar")
	var first_ledger: Dictionary = main.save_data["opera_mastery"]
	var first_wallet: Dictionary = first_ledger["encore_tokens"]
	var first_ok := bool(first.get("completed", false)) \
		and int(first.get("token_delta", -1)) == 6 \
		and int(first_wallet["balance"]) == 6 \
		and int(first_ledger["best_tiers"]["popstar"]) == Mastery.GOLD \
		and int(main.medals.get("opera_popstar", 0)) == Mastery.GOLD \
		and not (main.save_data["opera_performance_checkpoints"] as Dictionary).has("popstar")
	var replay := await _run_house_performance("popstar")
	var replay_wallet: Dictionary = main.save_data["opera_mastery"]["encore_tokens"]
	var replay_ok := bool(replay.get("completed", false)) \
		and int(replay.get("token_delta", -1)) == 0 \
		and int(replay_wallet["balance"]) == 6 \
		and int(replay_wallet["total_earned"]) == 6
	_check("final world completion awards mastery once and clears its checkpoint",
		first_ok)
	_check("a full replay keeps the best medal and awards zero token delta",
		replay_ok)


func _probe_current_mechanic_restore() -> void:
	main.save_data["opera_performance_checkpoints"] = {}
	var magic_config := _career_config("magician")
	var practice := OperaAct.new()
	get_root().add_child(practice)
	practice.start(main, magic_config, Callable())
	await process_frame
	var practice_world := practice.career_world_2d
	practice_world.reveal_t = 0.0
	practice_world.phase_gap = 0.0
	practice_world._open_task()
	var magic_surface: OperaGestureSurface = practice_world.surface
	var wand := magic_surface._magic_vanish_wand_hit_rect().get_center()
	_touch_down(magic_surface, wand)
	practice_world._process(0.9)
	_touch_up(magic_surface, wand)
	practice_world._performance_checkpoint(false)
	var partial_progress := practice_world.phase_progress
	var saved_magic: Dictionary = main.save_data[
		"opera_performance_checkpoints"]["magician"]
	var saved_current: Dictionary = saved_magic["current"]
	var partial_saved := partial_progress > 0.1 and partial_progress < 3.7 \
		and String(saved_current.get("part", "")) == "practice" \
		and String(saved_current.get("mode", "")) == "hold" \
		and float(saved_current.get("progress", 0.0)) > 0.0 \
		and not bool(saved_current.get("completed", true))
	practice.cancel()
	await process_frame

	var practice_resume := OperaAct.new()
	get_root().add_child(practice_resume)
	practice_resume.start(main, magic_config, Callable())
	await process_frame
	var practice_restored := practice_resume.career_world_2d
	var pending_before_open := practice_restored.phase_index == 0 \
		and not practice_restored.task_open \
		and not practice_restored.performance_pending_current.is_empty()
	practice_restored._performance_checkpoint(false)
	var closed_current: Dictionary = main.save_data[
		"opera_performance_checkpoints"]["magician"]["current"]
	var closed_preserved := is_equal_approx(float(closed_current.get("progress", 0.0)),
		float(saved_current.get("progress", -1.0)))
	practice_resume.cancel()
	await process_frame
	var practice_reopen := OperaAct.new()
	get_root().add_child(practice_reopen)
	practice_reopen.start(main, magic_config, Callable())
	await process_frame
	var reopened_world := practice_reopen.career_world_2d
	reopened_world._open_task()
	var partial_restored := reopened_world.phase_index == 0 \
		and is_equal_approx(reopened_world.phase_progress, partial_progress) \
		and is_equal_approx(reopened_world.surface.widget_fill,
			partial_progress / float(reopened_world.phases[0]["goal"])) \
		and not reopened_world.surface.held
	practice_reopen.cancel()
	await process_frame
	_check("a genuine practice hold restores its visible partial material",
		partial_saved and pending_before_open and closed_preserved and partial_restored)

	var malformed := saved_magic.duplicate(true)
	malformed["phase_index"] = 0
	malformed["current"] = {"part": "stage", "source_phase": "0",
		"mode": "hold", "progress": "1.0", "completed": true,
		"mechanic": {"echo_verse": 99, "echo_input_i": "2"}}
	main.save_data["opera_performance_checkpoints"] = {"magician": malformed}
	var rejected := OperaAct.new()
	get_root().add_child(rejected)
	rejected.start(main, magic_config, Callable())
	await process_frame
	var rejected_world := rejected.career_world_2d
	rejected_world._open_task()
	var malformed_rejected := rejected_world.phase_index == 0 \
		and is_zero_approx(rejected_world.phase_progress) \
		and is_zero_approx(rejected_world.surface.widget_fill) \
		and not rejected_world.phase_advance_pending
	rejected.cancel()
	await process_frame
	_check("malformed or mismatched current identity grants no progress or skip",
		malformed_rejected)

	main.save_data["opera_performance_checkpoints"] = {}
	var pop_config := _career_config("popstar")
	var echo_act := OperaAct.new()
	get_root().add_child(echo_act)
	echo_act.start(main, pop_config, Callable())
	await process_frame
	var echo_world := echo_act.career_world_2d
	echo_world.phase_index = echo_world.performance_stage_start \
		+ _source_phase_with_mode("popstar", "echo")
	echo_world._arm_phase()
	var echo_surface: OperaGestureSurface = echo_world.surface
	var echo_guard := 0
	while not echo_surface.echo_listening and echo_guard < 12:
		echo_surface._process(0.6)
		echo_guard += 1
	var first_note := int(OperaGestureSurface.ECHO_VERSES[0][0])
	_touch(echo_surface, echo_surface._echo_star_center(first_note))
	await process_frame
	echo_world._performance_checkpoint(false)
	var saved_echo: Dictionary = main.save_data[
		"opera_performance_checkpoints"]["popstar"]["current"]
	var echo_mechanic: Dictionary = saved_echo.get("mechanic", {})
	var prefix_saved := echo_surface.echo_listening and echo_surface.echo_input_i == 1 \
		and int(echo_mechanic.get("echo_verse", -1)) == 0 \
		and int(echo_mechanic.get("echo_input_i", -1)) == 1
	var echo_phase := echo_world.phase_index
	echo_act.cancel()
	await process_frame

	var echo_resume := OperaAct.new()
	get_root().add_child(echo_resume)
	echo_resume.start(main, pop_config, Callable())
	await process_frame
	var echo_restored := echo_resume.career_world_2d
	var restored_surface: OperaGestureSurface = echo_restored.surface
	var prefix_restored := echo_restored.phase_index == echo_phase \
		and restored_surface.mode == "echo" and restored_surface.echo_listening \
		and restored_surface.echo_verse == 0 and restored_surface.echo_input_i == 1
	var second_note := int(OperaGestureSurface.ECHO_VERSES[0][1])
	_touch(restored_surface, restored_surface._echo_star_center(second_note))
	var prefix_continues := restored_surface.echo_verse == 1 \
		and is_equal_approx(echo_restored.phase_progress, 1.0)
	echo_resume.cancel()
	await process_frame
	_check("a real Echo note prefix restores and continues the same verse",
		prefix_saved and prefix_restored and prefix_continues)

	main.save_data["opera_performance_checkpoints"] = {}
	var complete_act := OperaAct.new()
	get_root().add_child(complete_act)
	complete_act.start(main, magic_config, Callable())
	await process_frame
	var complete_world := complete_act.career_world_2d
	var choice_phase := complete_world.performance_stage_start \
		+ _source_phase_with_mode("magician", "choice")
	complete_world.phase_index = choice_phase
	complete_world._arm_phase()
	for _choice in range(5):
		_touch_choice(complete_world)
	var completed_current: Dictionary = main.save_data[
		"opera_performance_checkpoints"]["magician"]["current"]
	var completion_saved := complete_world.phase_advance_pending \
		and bool(completed_current.get("completed", false)) \
		and float(completed_current.get("progress", 0.0)) >= 0.999
	complete_act.cancel()
	await process_frame
	var promoted_act := OperaAct.new()
	get_root().add_child(promoted_act)
	promoted_act.start(main, magic_config, Callable())
	await process_frame
	var promoted_world := promoted_act.career_world_2d
	var completion_promoted := promoted_world.phase_index == choice_phase + 1 \
		and not promoted_world.phase_advance_pending \
		and is_zero_approx(promoted_world.phase_progress)
	promoted_act.cancel()
	await process_frame
	_check("a saved completed hold promotes once instead of replaying its payout",
		completion_saved and completion_promoted)


func _run_house_performance(career: String) -> Dictionary:
	var index := _career_index(career)
	var house := OperaHouse.new()
	get_root().add_child(house)
	var before_callbacks := house_completions.size()
	var started := house.start(main, index, Callable(self, "_on_house_finished"))
	await process_frame
	var act := house.act
	if not started or act == null or act.career_world_2d == null:
		return {"completed": false, "token_delta": -1}
	var world := act.career_world_2d
	var guard := 0
	while act.state == "play" and guard < 80:
		if world.phase_advance_pending:
			world._advance_completed_phase()
		elif world.phase_index < world.phases.size():
			if not world.task_open:
				world._open_task()
			if world.phase_index >= world.performance_stage_start:
				var mode := String((world.phases[world.phase_index] as Dictionary).get(
					"mode", "tap"))
				world._performance_input(mode, 1.0)
				world._performance_record_progress(1.0, mode, 1.0)
				world._performance_tick(0.25)
			world._on_gesture("probe", 100.0, 1.0)
		act._process(0.02)
		guard += 1
	var award := act.performance_result.duplicate(true)
	var balance_after_win := int(main.save_data["opera_mastery"]["encore_tokens"]["balance"])
	act._win()
	var idempotent_win := int(main.save_data["opera_mastery"]["encore_tokens"]["balance"]) \
		== balance_after_win
	act._process(3.3)
	await process_frame
	await process_frame
	return {"completed": house_completions.size() == before_callbacks + 1 \
		and house_completions[-1] and idempotent_win,
		"token_delta": int(award.get("token_delta", -1))}


func _touch_choice(world: OperaCareerWorld2D) -> void:
	var surface := world.surface
	var count := maxi(1, surface.choice_count)
	var target := clampi(surface.target_choice, 0, count - 1)
	_touch(surface, Vector2(surface.size.x * (float(target) + 0.5) / float(count),
		surface.size.y * 0.5))


func _touch(surface: Control, position: Vector2) -> void:
	_touch_down(surface, position)
	_touch_up(surface, position)


func _touch_down(surface: Control, position: Vector2) -> void:
	var press := InputEventScreenTouch.new()
	press.index = 0
	press.position = position
	press.pressed = true
	surface._gui_input(press)


func _touch_up(surface: Control, position: Vector2) -> void:
	var release := InputEventScreenTouch.new()
	release.index = 0
	release.position = position
	release.pressed = false
	surface._gui_input(release)


func _source_phase_with_mode(career: String, mode: String) -> int:
	var phases: Array = OperaCareerWorld2D.PHASES[career]
	for index in range(phases.size()):
		if String((phases[index] as Dictionary).get("mode", "")) == mode:
			return index
	return -1


func _career_config(career: String) -> Dictionary:
	for source: Dictionary in OperaHouse.ACTS:
		if String(source.get("costume", "")) == career:
			return source.duplicate(true)
	return {}


func _career_index(career: String) -> int:
	for index in range(OperaHouse.ACTS.size()):
		if String((OperaHouse.ACTS[index] as Dictionary).get("costume", "")) == career:
			return index
	return -1


func _on_house_finished(completed: bool) -> void:
	house_completions.append(completed)


func _check(label: String, condition: bool) -> void:
	if condition:
		print("OPERAPERFORMANCE|OK|%s" % label)
	else:
		failures += 1
		print("OPERAPERFORMANCE|FAIL|%s" % label)
