extends SceneTree
## Launch regression through ordinary callers with isolated progression fixtures.
## No phase override is injected and no input/gameplay completion is claimed.

const OUT := "res://audit/day2_authored_launch_20261001/"
var main: ReefMain
var failures: int = 0
var records: Array[Dictionary] = []
var label: String = "candidate"

func _init() -> void:
	call_deferred("_run")

func _frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame

func _check(name: String, condition: bool) -> void:
	records.append({"check": name, "pass": condition})
	if not condition:
		failures += 1
	print("AUTHORED_LAUNCH|", "OK" if condition else "FAIL", "|", name)

func _launch(slot: int, overrides: Dictionary, expected: Array) -> void:
	var stars: int = main.opera_stars
	var party: int = main.chapter2_party_piece_mask
	var house := OperaHouse.new()
	main.add_child(house)
	var started: bool = house.start(main, slot, Callable(), overrides)
	await _frames(4)
	var world: OperaCareerWorld2D = house.act.career_world_2d if house.act != null else null
	var built: bool = world != null and is_instance_valid(world.root)
	_check("slot%d %s builds world" % [slot, label], started and built)
	if built:
		_check("slot%d resolves exact authored phases" % slot, world.phases == expected)
		_check("slot%d opens with zero earned progress" % slot,
			world.phase_progress == 0.0 and not world.phase_advance_pending)
		_check("slot%d uses birthday policy exactly when requested" % slot,
			world.using_chapter_two_phases == (not overrides.is_empty()))
		if not overrides.is_empty():
			var callback: Callable = world.adapter_callbacks.get("phase_completed", Callable())
			_check("slot%d ordinary story callback still belongs to the actual main" % slot,
				callback.is_valid() and callback.get_object() == main)
	_check("slot%d passive launch cannot award stars or party contributions" % slot,
		main.opera_stars == stars and main.chapter2_party_piece_mask == party)
	house._leave_early()
	await _frames(3)
	_check("slot%d cancellation preserves earned state" % slot,
		main.opera_stars == stars and main.chapter2_party_piece_mask == party)

func _run() -> void:
	for arg: String in OS.get_cmdline_user_args():
		if arg == "baseline":
			label = "baseline"
	DirAccess.make_dir_recursive_absolute(OUT)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	main._save_state = SaveState.new(main, "res://tmp/day2_authored_launch_save.json")
	root.add_child(main)
	await _frames(4)
	main.day_one_active = false
	main._skip_intro()
	main.set_process(false)
	main.chapter2_active = false
	for slot: int in OperaHouse.LIVE_ACT_INDICES:
		var career: String = String((OperaHouse.ACTS[slot] as Dictionary)["costume"])
		var source: Array = OperaCareerWorld2D.PHASES[career]
		var plan: Dictionary = OperaPerformancePlan.build(career, source)
		var expected: Array = plan["phases"] if OperaPerformancePlan.enabled(career, OperaHouse.ACTS[slot]) else source
		await _launch(slot, {}, expected)
	main.chapter2_active = true
	main.chapter2_party_piece_mask = 0
	main.chapter2_job_phase_masks = [0, 0, 0, 0, 0, 0, 0, 0]
	main.chapter2_strawberry_mask = 0
	main.chapter2_cake_piece_mask = 0
	main.chapter2_party_started = false
	main.chapter2_ember_king_crashed = false
	main.chapter2_rainbow_candle_found = false
	main.chapter2_stuffie_ballet_done = false
	main.chapter2_farmer_strawberries_ready = false
	main.chapter2_chef_cake_baked = false
	main.chapter2_candy_cake_finished = false
	main.chapter2_unlocked_opera_mask = ChapterTwoDirector.FIRST_WAVE_UNLOCK_MASK
	var director: ChapterTwoDirector = main._chapter_two_ref()
	director._sync_objective()
	for slot: int in ChapterTwoDirector.JOB_PHASE_ACTS:
		var context: String = ""
		if slot == ChapterTwoDirector.ACT_BALLERINA:
			context = ChapterTwoDirector.PLOT_CONTEXT_STUFFIE_BALLET
		elif slot == ChapterTwoDirector.ACT_DETECTIVE:
			context = ChapterTwoDirector.PLOT_CONTEXT_DETECTIVE_CANDLE
		var overrides: Dictionary = director.opera_config_overrides(context, slot)
		_check("slot%d ordinary director supplies story policy without explicit phases" % slot,
			String(overrides.get("reward_policy", "")) == "chapter2_story"
			and not overrides.has("phase_overrides"))
		var career: String = String((OperaHouse.ACTS[slot] as Dictionary)["costume"])
		var expected: Array = ChapterTwoCareerSceneAdapter.phase_set(career)["phases"]
		await _launch(slot, overrides, expected)
		# Establish the next launch fixture using current director policy; this is
		# intentionally not evidence of played job completion.
		_check("fixture policy advances ordered slot%d" % slot,
			director.complete_stuffie_ballet(slot) if slot == ChapterTwoDirector.ACT_BALLERINA
			else director.complete_detective_search() if slot == ChapterTwoDirector.ACT_DETECTIVE
			else director.record_party_contribution(slot))
	for value: Variant in [[], "invalid", [{"name": "bad", "mode": "tap", "goal": 0.0}]]:
		_check("explicit invalid phases rejected by shared caller validator",
			not ChapterTwoCareerSceneAdapter.validate_config_overrides("chef", {"phase_overrides": value}))
	var report := {"label": label, "godot": Engine.get_version_info(),
		"world_sha256": FileAccess.get_sha256("res://scripts/opera_career_world_2d.gd"),
		"probe_sha256": FileAccess.get_sha256("res://tools/probe_day2_authored_launch.gd"),
		"qualification": "Ordinary director/house/act setup with isolated progression fixtures; no normal room traversal or action/context/device/child acceptance.",
		"records": records, "failures": failures}
	var file := FileAccess.open(OUT + label + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t") + "\n")
	file.close()
	main.queue_free()
	await _frames(3)
	print("AUTHORED_LAUNCH|RESULT|", "PASS" if failures == 0 else "FAIL", "|", failures)
	quit(1 if failures else 0)
