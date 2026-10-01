extends SceneTree
## Contest protocol falsification: passive, idle, tie, loss, mercy and rematch.

const Contest := preload("res://scripts/opera_imp_contest.gd")
const Child := preload("res://scripts/probe_opera_child_driver.gd")
var failures := 0
var captures: Array[Dictionary] = []


func _initialize() -> void:
	call_deferred("_run")


func _check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
		print("OPERA_CONTEST|FAIL|", label)


func _run() -> void:
	var logical := 0
	var expanded := 0
	var modes: Dictionary = {}
	for career: String in OperaCareerWorld2D.PHASES:
		var source: Array = OperaCareerWorld2D.PHASES[career]
		logical += Contest.apply(career, source, false).size()
		var phases: Array = (OperaPerformancePlan.build(career, source)["phases"] as Array) \
			if OperaPerformancePlan.enabled(career, {}) else source
		for phase: Dictionary in Contest.apply(career, phases, career in OperaPerformancePlan.ENABLED):
			expanded += 1
			modes[String(phase["mode"])] = true
	_check(logical == 65 and expanded == 74 and modes.size() == 36 \
		and OperaCareerWorld2D.PHASES.size() == 15, "current catalog counts")
	print("OPERA_CONTEST|catalog|careers=15|definitions=%d|instances=%d|modes=%d" % [logical, expanded, modes.size()])
	for career: String in Contest.CONTESTS:
		var attempt := Contest.new()
		attempt.configure(career)
		for frame in range(1800):
			_check(attempt.tick(1.0 / 30.0, 0.0, false).is_empty(), career + " passive event")
		_check(attempt.his_units == 0.0 and attempt.state == "waiting", career + " C8 passive")
		attempt.tick(0.0, 0.0, true)
		for frame in range(180):
			attempt.tick(1.0 / 30.0, 0.0, false)
		var frozen: float = attempt.his_units
		attempt.tick(60.0, 0.0, false)
		_check(is_equal_approx(frozen, attempt.his_units) and attempt.state == "idle", career + " idle freeze")
		_check("idle_resume" in attempt.tick(0.0, 0.0, true), career + " idle resume")
		attempt.his_units = attempt.rival_target()
		var tied: Array[String] = attempt.tick(0.0, attempt.player_target(), true)
		_check(tied == ["player_won"], career + " C6 tie")
		_check(attempt.tick(10.0, 0.0, true).is_empty(), career + " terminal once")
		attempt.reset_attempt()
		_check(attempt.her_units == 0.0 and attempt.his_units == 0.0 and not attempt.flub_done, career + " C7 reset")
		_check(attempt.rematches == 1 and attempt.state == "waiting", career + " rematch")
		if bool(attempt.spec.get("points", false)):
			_check(attempt.rival_target() == attempt.player_target() + 1.0, career + " C9 points mercy")
		else:
			_check(is_equal_approx(attempt.his_rate, 0.9 if career == "racer" else 0.8), career + " C9 rate mercy")
		attempt.configure(career)
		var flubs := 0
		var lost := 0
		for frame in range(6000):
			attempt.note_touch()
			if bool(attempt.spec.get("points", false)) and frame % 30 == 0:
				attempt.rival_point()
			if career == "racer":
				attempt.observe_rival(attempt.his_units + 0.01)
			var events: Array[String] = attempt.tick(1.0 / 30.0, 0.0, true)
			flubs += events.count("flub_start")
			lost += events.count("imp_won")
			if lost > 0:
				break
		_check(flubs == 1 and lost == 1, career + " C6/C9 one flub and real loss")
		attempt.reset_attempt()
		_check(not attempt.flub_done, career + " flub rearmed")
		attempt.her_units = attempt.player_target()
		attempt.margin = 0.8
		_check(int(attempt.result()["tier"]) == 2, career + " rematch tier cap")
		attempt.state = "stopped"
		_check(attempt.tick(100.0, 0.0, true).is_empty(), career + " C14 stop")
		for config: Dictionary in [{"reward_policy": "chapter2_story"}, {"chapter2_tutorial": true}, {"tutorial": true}, {"phase_overrides": []}, {"scene_adapter": {}}]:
			_check(not Contest.enabled(career, config), career + " C13 opt-out")
		_check(Contest.enabled(career, {}), career + " enabled freeplay")
	for career: String in ["nursery", "geologist", "teacher"]:
		_check(not Contest.enabled(career, {}), career + " remains cooperative")
	var source: Array = [{"name": "TRACK", "performance_part": "practice"}, {"name": "PORTAL", "performance_part": "stage"}]
	var phases: Array = Contest.apply("magician", source, true)
	_check(phases.size() == 3 and phases[1]["name"] == "HAT DUEL" and not phases[0].has("contest"), "one inserted stage contest")
	_check(not source[0].has("contest") and source.size() == 2, "source table preserved")
	await _teacher_preparation()
	await _connected()
	if not captures.is_empty():
		var output := OS.get_environment("OPERA_CONTEST_CAPTURE_OUT")
		var file := FileAccess.open(output.path_join("manifest.json"), FileAccess.WRITE)
		file.store_string(JSON.stringify({"engine": Engine.get_version_info()["string"],
			"renderer": RenderingServer.get_current_rendering_method(), "status": "DIAGNOSTIC",
			"captures": captures}, "\t", true) + "\n")
	print("OPERA_CONTEST|", "ALL OK" if failures == 0 else "FAILURES %d" % failures)
	quit(0 if failures == 0 else 1)


func _teacher_preparation() -> void:
	var plan := preload("res://scripts/opera_teacher_imp_plan.gd")
	var lessons := preload("res://scripts/teacher_lesson_plan.gd")
	for kind: String in lessons.KINDS:
		for tier in range(3):
			for sequence in range(12):
				var progress := lessons.normalise_progress({})
				progress["kinds"][kind] = {"tier": tier, "rounds": sequence, "clean_successes": 0}
				var lesson := lessons.make_lesson(kind, progress)
				var near := lessons.imp_answer(lesson)
				var far := lessons.imp_answer(lesson, true)
				_check(near >= 0 and far >= 0 and near != int(lesson["answer"]) and far != int(lesson["answer"]), "Teacher imp always chooses a wrong answer")
				if kind in ["count", "add"]:
					var choices: Array = lesson["choices"]
					_check(absf(float(choices[near]) - float(lesson["target"])) <= absf(float(choices[far]) - float(lesson["target"])), "Teacher mercy uses a more obvious numeric error")
	for id: String in plan.SILLY:
		for sequence in range(5):
			var round_data: Dictionary = plan.silly_round(id, sequence)
			_check((round_data["correct_indices"] as Array).size() == 4 and (round_data["choices"] as Array).size() == 5 \
				and int(round_data["imp_answer"]) not in (round_data["correct_indices"] as Array), "Silly round has four fitting choices and one imp misfit")
	var attempt := Contest.new()
	attempt.configure_inverted()
	for frame in range(1800):
		_check(attempt.tick(1.0 / 30.0, 0.0, false).is_empty(), "Teacher has no time-based event")
	_check(attempt.her_units == 0 and attempt.his_units == 0 and not attempt.flub_done, "Teacher passive no score or flub")
	attempt.score_round("hinted")
	_check(attempt.her_units == 0 and attempt.his_units == 0, "Teacher hint scores nobody")
	for index in range(3):
		attempt.score_round("tricked")
	_check(attempt.state == "imp_won", "Teacher first-to-three real wrong rounds can lose")
	attempt.reset_attempt()
	_check(attempt.rival_target() == 4.0 and attempt.his_units == 0.0, "Teacher rematch points mercy")
	for index in range(3):
		attempt.score_round("fixed")
	_check(attempt.state == "player_won" and int(attempt.result()["tier"]) <= 2, "Teacher clean rematch can win with capped cheer")
	var board := OperaTeacherSurface.new()
	board.size = Vector2(1280, 720)
	get_root().add_child(board)
	board.set_process(false)
	var picks: Array[String] = []
	var closes: Array[String] = []
	var records: Array[String] = []
	board.round_pick.connect(func(result_name: String) -> void: picks.append(result_name))
	board.round_completed.connect(func(_kind: String, _help: bool, result_name: String) -> void: closes.append(result_name))
	board.lesson_completed.connect(func(kind: String, _help: bool) -> void: records.append(kind))
	for kind: String in lessons.KINDS:
		picks.clear()
		closes.clear()
		var lesson := lessons.make_lesson(kind, {})
		lesson["imp_answer"] = lessons.imp_answer(lesson)
		board.set_inverted_lesson(lesson)
		board._process(2.0)
		if kind in ["count", "add"]:
			Child.tap(board, board.choice_rect(board.answer_index()).get_center())
			_check(not board.solved and picks.is_empty(), "Teacher cannot bypass one-to-one counting")
			for index in range(board.counted.size()):
				Child.tap(board, board.counter_position(index))
		Child.tap(board, board.choice_rect(board.imp_choice).get_center())
		_check(picks == ["tricked"] and closes.is_empty() and not board.solved and board.help_visible, "Teacher wrong first pick waits for truth")
		Child.tap(board, board.choice_rect(board.imp_choice).get_center())
		_check(picks.size() == 1 and closes.is_empty(), "Teacher repeated wrong pick scores once")
		Child.tap(board, board.choice_rect(board.answer_index()).get_center())
		_check(board.solved and board.assisted and closes == ["tricked"], "Teacher child closes round with the right answer")
	_check(records == ["pattern", "count", "add", "match"], "Teacher records each real lesson exactly once")
	for correct in range(4):
		var silly: Dictionary = plan.silly_round("smell", 0)
		board.set_inverted_lesson(silly)
		board._process(2.0)
		Child.tap(board, board.choice_rect(correct).get_center())
		_check(board.solved and board.chosen == correct, "Each fitting silly picture is accepted")
	_check(records.size() == 4, "Silly pictures never update maths mastery")
	board.set_inverted_lesson(plan.silly_round("smell", 0))
	board._process(2.0)
	Child.tap(board, OperaTeacherSurface.HINT_CENTER)
	Child.tap(board, board.choice_rect(0).get_center())
	_check(board.solved and board.first_pick == "hinted" and board.assisted, "Teacher hinted round requires a child placement and awards nobody")
	board.queue_free()
	await process_frame
	print("OPERA_CONTEST|Teacher preparation logic/surface PASS; production activation and pictures remain owner-gated")


func _connected() -> void:
	var scene := load("res://scenes/main.tscn") as PackedScene
	_check(scene != null, "main scene loads after required import")
	if scene == null:
		return
	var main := scene.instantiate() as ReefMain
	_check(main != null, "main fixture compiles and instantiates")
	if main == null:
		return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://tmp/contest_probe"))
	main._save_state = SaveState.new(main, "res://tmp/contest_probe/reef_save.json")
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		await process_frame
	main._skip_intro()
	main.game = "opera"
	main.quality = "speedy"
	main.save_data["quality"] = "speedy"
	main.set_process(false)
	for career: String in Contest.CONTESTS:
		main.save_data["opera_phase_checkpoints"] = {}
		main.save_data["opera_performance_checkpoints"] = {}
		var config: Dictionary = {}
		for source: Dictionary in OperaHouse.ACTS:
			if String(source.get("costume", "")) == career:
				config = source.duplicate(true)
		var act := OperaAct.new()
		get_root().add_child(act)
		act.process_mode = Node.PROCESS_MODE_DISABLED
		_check(act.start(main, config, Callable()), career + " starts")
		var world: OperaCareerWorld2D = act.career_world_2d
		_check(not world.rival_actor.visible and world.performance_rival_surface == null \
			and not world.contest_rows.visible, career + " C1 hidden")
		var index := -1
		var contests := 0
		for phase_index in range(world.phases.size()):
			if (world.phases[phase_index] as Dictionary).has("contest"):
				index = phase_index
				contests += 1
		_check(contests == 1 and index >= world._finale_start(), career + " C3 one final contest")
		world.phase_index = index
		world._arm_phase()
		world._contest_tick(0.01)
		_check(world.rival_actor.texture == world._state_texture("rival_%s_flee" % career), career + " entrance flee")
		world._contest_tick(0.8)
		_check(world.rival_actor.texture == world._state_texture("rival_%s_hop_a" % career), career + " entrance crouch")
		world._contest_tick(0.25)
		_check(world.rival_actor.texture == world._state_texture("rival_%s_hop_b" % career), career + " entrance jump")
		world._contest_tick(0.35)
		_check(world.contest_entrance_t < 0.0, career + " entrance within 3 seconds")
		if not world.task_open:
			world.phase_gap = 0.0
			world._on_hotspot_pressed(world.armed_station)
			for step in range(150):
				world._process(0.1)
				for hotspot: OperaWorldHotspot2D in world.station_nodes:
					hotspot._process(0.1)
				if world.task_open:
					break
		_check(world.task_open, career + " C5 physical station opens")
		# A fast phase/re-prompt must replace an older required route recording,
		# even when the route also has a queued successor.
		main._audio_ref().chapter_two_prompt("chapter2_route_chef")
		main._say("roshan", "chapter2_route_farmer")
		world._repeat_phase_prompt()
		var voice_index := posmod(main.voice_i - 1, main.voice_pool.size())
		var voice_player := main.voice_pool[voice_index] as AudioStreamPlayer
		var current_instruction_key := "roshan_" + String((world.phases[world.phase_index] as Dictionary)["vo"])
		_check(main._audio_ref()._required_voice_queue.is_empty() and voice_player.stream != null \
			and voice_player.stream.resource_path.ends_with(current_instruction_key + ".ogg"),
			career + " current contest instruction owns actual speech")
		main.clear_dialogue()
		world.surface.set_process(false)
		for frame in range(1800):
			world.surface._process(1.0 / 30.0)
			world._contest_tick(1.0 / 30.0)
		_check(world.contest.state == "waiting" and world.phase_progress == 0.0 \
			and world.contest.his_units == 0.0, career + " C8 connected passive")
		await _capture(world, career + "_waiting")
		var position: Vector2 = world.player_actor.position
		var pearls: int = main.pearl_count
		var stars: int = main.opera_stars
		world.contest.note_touch()
		world.contest.flub_done = true
		world.contest.his_units = world.contest.rival_target()
		world._contest_apply(world.contest.tick(0.0, 0.0, false))
		_check(world.contest.state == "imp_won" and world.surface.armed_only, career + " C6 loss locks input")
		world._on_gesture("probe", 100.0, 1.0)
		_check(world.phase_progress == 0.0, career + " late finish rejected")
		world._contest_tick(1.41)
		await _capture(world, career + "_rematch")
		_check(world.task_open and not world.surface.armed_only \
			and world.contest.state == "waiting" and world.contest.rematches == 1 \
			and world.contest.his_units == 0.0 and world.phase_progress == 0.0 \
			and world.player_actor.position == position, career + " C7 immediate stationary rematch")
		_check(main.pearl_count == pearls and main.opera_stars == stars, career + " rewards preserved")
		main.say_sequence([{"who": "Roshan", "text": "Again! I can do it this time!", "vo": "op_contest_again"}])
		var instruction_key := String(main.hud_msg.get_meta("requested_voice_key", ""))
		world.contest_voice_cool = 0.0
		world._contest_voice("op_%s_copy" % career)
		_check(main.dialogue_active and String(main.hud_msg.get_meta("requested_voice_key", "")) == instruction_key,
			career + " lower-priority reaction cannot interrupt instruction")
		main.clear_dialogue()
		var pooled_nodes := world.root.get_child_count()
		_check(world.contest_confetti_age.size() == 36, career + " Speedy three-burst pool budget")
		world.cheer_tier = 3
		world.cheer_beats_remaining = 3
		world.cheer_beat_index = 0
		world.cheer_beat_t = 0.0
		for beat in range(3):
			world._tick_contest_cheer(0.45)
		_check(world.cheer_beat_index == 3 and world.cheer_beats_remaining == 0 \
			and world.root.get_child_count() == pooled_nodes,
			career + " tier-three feedback reuses pool for all three bursts")
		world._tick_contest_confetti(3.0)
		for age: float in world.contest_confetti_age:
			_check(age < 0.0, career + " confetti expires")
		act.cancel()
		await process_frame
		var resumed := OperaAct.new()
		get_root().add_child(resumed)
		resumed.process_mode = Node.PROCESS_MODE_DISABLED
		resumed.start(main, config, Callable())
		world = resumed.career_world_2d
		_check(world.phase_index == index and world.phase_progress == 0.0 \
			and world.contest_entered and world.contest.rematches == 0, career + " checkpoint resumes fresh")
		if not world.task_open:
			world._open_task()
		world._notification(Node.NOTIFICATION_APPLICATION_FOCUS_OUT)
		_check(world.contest_suspended and world.contest.state == "stopped" \
			and not world.surface.is_processing() and not world.surface.held, career + " C14 focus stops")
		world._notification(Node.NOTIFICATION_APPLICATION_FOCUS_IN)
		world._on_gesture("probe", 100.0, 1.0)
		_check(world.contest.state == "player_won" and world.phase_advance_pending, career + " accepted winner")
		resumed.cancel()
		await process_frame
		await _real_attempt(main, config, career)
		await _slow_attempt(main, config, career)


func _real_attempt(main: ReefMain, config: Dictionary, career: String) -> void:
	main.save_data["opera_phase_checkpoints"] = {}
	main.save_data["opera_performance_checkpoints"] = {}
	var act := OperaAct.new()
	get_root().add_child(act)
	act.process_mode = Node.PROCESS_MODE_DISABLED
	act.start(main, config, Callable())
	var world: OperaCareerWorld2D = act.career_world_2d
	for index in range(world.phases.size()):
		if (world.phases[index] as Dictionary).has("contest"):
			world.phase_index = index
			break
	world._arm_phase()
	var child := Child.new()
	var seconds := 0.0
	while seconds < 90.0 and world.contest.state != "player_won":
		child.step(world, 1.0 / 30.0, 0.25)
		world.surface._process(1.0 / 30.0)
		world._process(1.0 / 30.0)
		for hotspot: OperaWorldHotspot2D in world.station_nodes:
			hotspot._process(1.0 / 30.0)
		seconds += 1.0 / 30.0
		if world.contest.rematches > 0:
			break
	print("OPERA_CONTEST|real_child|%s|seconds=%.2f|state=%s|her=%.3f|his=%.3f" % [career, seconds, world.contest.state, world.phase_progress, world.contest.his_units])
	_check(world.contest.state == "player_won" and world.contest.rematches == 0,
		career + " fast genuine one-finger winner")
	await _capture(world, career + "_won")
	act.cancel()
	await process_frame


func _capture(world: OperaCareerWorld2D, label: String) -> void:
	var output := OS.get_environment("OPERA_CONTEST_CAPTURE_OUT")
	if output.is_empty() or DisplayServer.get_name() == "headless":
		return
	DirAccess.make_dir_recursive_absolute(output)
	world.m.clear_dialogue()
	# Allow real reveal tweens to settle while the deterministic controller
	# remains frozen. The capture must include the child's visible activity.
	var was_processing := world.surface.is_processing()
	world.surface.set_process(false)
	world.action_panel.process_mode = Node.PROCESS_MODE_ALWAYS
	get_root().mode = Window.MODE_WINDOWED
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	await process_frame
	var height := 800 if OS.get_environment("OPERA_CONTEST_CAPTURE_HEIGHT") == "800" else 720
	var wanted := Vector2i(1280, height)
	for frame in range(60):
		get_root().size = wanted
		DisplayServer.window_set_size(wanted)
		await process_frame
		var check := get_root().get_texture().get_image()
		if check != null and check.get_size() == wanted:
			break
	for frame in range(24):
		await process_frame
	await RenderingServer.frame_post_draw
	var pixels := get_root().get_texture().get_image()
	var path := output.path_join(label + ".png")
	_check(pixels != null and pixels.save_png(path) == OK, label + " capture")
	if pixels == null:
		return
	world.surface.set_process(was_processing)
	_check(world.action_panel.modulate.a >= 0.99 or not world.action_panel.visible, label + " activity reveal settled")
	_check(pixels.get_size() == wanted and not world.m.start_menu_active, label + " semantic viewport readiness")
	captures.append({"name": label, "path": path.get_file(), "sha256": FileAccess.get_sha256(path),
		"width": pixels.get_width(), "height": pixels.get_height(), "state": world.contest.state,
		"player_position": str(world.player_actor.position), "rival_position": str(world.rival_actor.position),
		"her_units": world.phase_progress, "his_units": world.contest.his_units})


func _slow_attempt(main: ReefMain, config: Dictionary, career: String) -> void:
	main.save_data["opera_phase_checkpoints"] = {}
	main.save_data["opera_performance_checkpoints"] = {}
	var act := OperaAct.new()
	get_root().add_child(act)
	act.process_mode = Node.PROCESS_MODE_DISABLED
	act.start(main, config, Callable())
	var world := act.career_world_2d
	for index in range(world.phases.size()):
		if (world.phases[index] as Dictionary).has("contest"):
			world.phase_index = index
			break
	world._arm_phase()
	var opener := Child.new()
	var seconds := 0.0
	var next_touch := 0.0
	var contact_captured := false
	var detective_contacts: Array[int] = []
	while seconds < 120.0 and world.contest.state not in ["imp_won", "player_won"]:
		if not world.task_open:
			opener.step(world, 1.0 / 30.0)
		elif career == "racer":
			var at := OperaRacerSurface.STEERING_RECT.position + Vector2(8, 60)
			if not world.surface.held:
				Child.touch(world.surface, at, true)
			Child.drag(world.surface, at)
		elif seconds >= next_touch:
			next_touch = seconds + 1.5
			if career == "detective":
				var event := InputEventScreenTouch.new()
				event.index = 0
				event.position = Vector2(130, 640)
				event.pressed = true
				world._lens_input(event)
			elif career == "magician":
				Child.tap(world.surface, world.surface.size * Vector2((float((world.surface.target_choice + 1) % 3) + 0.5) / 3.0, 0.5))
			elif career == "popstar":
				if world.surface.echo_listening:
					Child.tap(world.surface, world.surface._echo_star_center(1))
			elif career == "boxer":
				Child.tap(world.surface, (world.surface as OperaBoxingSurface).glove_rest(0))
			else:
				Child.tap(world.surface, Vector2(4, 4))
		world.surface._process(1.0 / 30.0)
		world._process(1.0 / 30.0)
		if career == "detective" and world.contest_contact_t > 0.20 \
				and world.contest_contact_index not in detective_contacts:
			detective_contacts.append(world.contest_contact_index)
			var indices: Array[int] = [6, 7, 1]
			var clue: Vector2 = OperaStagePaths.clue_spots(career)[indices[world.contest_contact_index]]
			var glass := world.rival_actor.position + world._contest_hand_offset(world.rival_actor.flip_h)
			_check(glass.distance_to(clue) < 0.01, "Detective held magnifier reaches the actual paid clue")
		if world.contest_contact_t > 0.20 and not contact_captured and career not in ["boxer", "racer"]:
			contact_captured = true
			_check(world.rival_actor.texture == world._state_texture("rival_%s_slash" % career), career + " unit uses the authored tool-contact pose")
			var hand := world.rival_actor.position + world._contest_hand_offset(world.rival_actor.flip_h)
			_check(hand.distance_to(world.contest_contact_point) < 0.01, career + " visible unit is at his hand or tool")
			await _capture(world, career + "_contact")
		for hotspot: OperaWorldHotspot2D in world.station_nodes:
			hotspot._process(1.0 / 30.0)
		seconds += 1.0 / 30.0
	print("OPERA_CONTEST|slow_active|%s|seconds=%.2f|state=%s" % [career, seconds, world.contest.state])
	_check(contact_captured or career in ["boxer", "racer"], career + " exercised a real own-work contact")
	if career == "detective":
		_check(detective_contacts.size() == 3, "Detective touches all three own clues before winning")
	_check(world.contest.state == "imp_won", career + " slow off-target genuine input can lose")
	if world.contest.state == "imp_won":
		world._contest_tick(0.1)
		await _capture(world, career + "_imp_won")
		var at := world.player_actor.position
		var pearls: int = main.pearl_count
		var stars: int = main.opera_stars
		world._process(1.41)
		_check(world.player_actor.position == at and main.pearl_count == pearls and main.opera_stars == stars,
			career + " actual loss preserves position and earned rewards")
		var child := Child.new()
		seconds = 0.0
		while seconds < 90.0 and world.contest.state != "player_won":
			child.step(world, 1.0 / 30.0, 0.25)
			world.surface._process(1.0 / 30.0)
			world._process(1.0 / 30.0)
			seconds += 1.0 / 30.0
		_check(world.contest.state == "player_won" and int(world.contest.result()["tier"]) <= 2,
			career + " genuine rematch wins with mercy and capped cheer")
	act.cancel()
	await process_frame
