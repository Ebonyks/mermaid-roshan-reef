extends SceneTree
# Shared combat-engine probe: both arenas require input, resolve their bespoke
# enemy states, save completion, and return control without a fail state.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260714)
	Engine.time_scale = 6.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	await _ice_case()
	await _fire_case()
	await _dual_case()
	await _malformed_checkpoint_case()
	print("COMBAT|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _ck(label: String, ok: bool) -> void:
	print("COMBAT|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _ice_case() -> void:
	main.combat_ice_done = false
	main.game = "galaxy"
	main._start_combat("ice")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("ice arena starts with eight surrounding imps", arena != null and arena.enemies.size() == 8)
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	for i in range(30):
		await process_frame
	_ck("ice battle cannot win passively", arena.state == "play" and not main.combat_ice_done)
	for enemy: Dictionary in arena.enemies:
		arena._freeze_imp(enemy)
		enemy["timer"] = 0.0
	await process_frame
	await process_frame
	_ck("frozen imps melt into popcorn", arena.state == "won")
	arena.win_t = 0.0
	await process_frame
	await process_frame
	_ck("ice completion saves", main.combat_ice_done)

func _fire_case() -> void:
	# Fire combat is entered from the live Pearl Castle hall. Build that source
	# state instead of only labelling an empty probe dictionary as "level2": the
	# main loop resumes the owning arena on the same frame the combat child exits.
	main.game = "level2"
	main.g["t"] = 0.0
	main._start_combat("fire")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("pepper boss arena builds", arena != null and not arena.boss.is_empty())
	var hp_before: int = int(arena.boss["hp"])
	_ck("pepper uses shared no-death encounter", arena.boss_encounter != null
		and arena.boss_telegraph != null)
	_ck("pepper warning is visible on Canvas", arena.boss_telegraph._visible
		and arena.boss_telegraph._points.size() >= 3)
	# Measure encounter time, not a frame count: uncapped headless CI can run
	# 45 frames before the full warning has elapsed on a fast machine.
	var passive_until: float = arena.elapsed + 6.0
	var passive_frames := 0
	while arena.elapsed < passive_until and passive_frames < 6000:
		passive_frames += 1
		await process_frame
	_ck("pepper cannot win without input", int(arena.boss["hp"]) == hp_before)
	_ck("stationary play receives a harmless shield bump",
		arena.boss_encounter.damage_taken > 0 and arena.state == "play")
	for _spam in range(8):
		arena._hit_boss("fire")
	_ck("shell-tap spam cannot skip avoidance", int(arena.boss["hp"]) == hp_before)
	await _earn_opening(arena)
	arena.elapsed = 37.0
	arena._hit_boss("fire")
	await process_frame
	var checkpoint_map: Dictionary = main.save_data.get("boss_encounter_checkpoints", {}) as Dictionary
	var checkpoint_key := "fire:%s" % String(arena.room_tag)
	_ck("pepper saves an earned round before interruption", int(checkpoint_map.get(checkpoint_key, {}).get("rounds", 0)) == 1)
	var fire_config: Dictionary = arena.encounter
	var fire_callback: Callable = arena.finish_cb
	arena.elapsed = 42.0  # include time spent after the last earned checkpoint
	arena.cancel(false)
	await process_frame
	arena = CombatArena.new()
	main.add_child(arena)
	arena.start(main, "fire", fire_callback, fire_config)
	var restored_elapsed: float = arena.elapsed
	await process_frame
	_ck("pepper re-entry restores earned rounds and assistance", arena.boss_encounter.completed_rounds == 1
		and arena.boss_encounter.opening_misses == int(checkpoint_map.get(checkpoint_key, {}).get("misses", -1))
		and is_equal_approx(restored_elapsed, 42.0))
	for _round in range(maxi(0, hp_before - 1)):
		await _earn_opening(arena)
		arena._hit_boss("fire")
		await process_frame
	_ck("pepper fire tames boss after earned openings", arena.state == "won")
	checkpoint_map = main.save_data.get("boss_encounter_checkpoints", {}) as Dictionary
	_ck("final accepted Pepper round is checkpointed before victory delay",
		int(checkpoint_map.get(checkpoint_key, {}).get("rounds", 0)) == hp_before)
	var pearls_before_finish: int = main.pearl_count
	# Simulate an app kill: dispose the scene without calling its completion
	# callback, then reconstruct it from the persisted final-round checkpoint.
	main.hit_engines.erase(arena.he)
	arena.he.teardown()
	arena._disarm_mic()
	if arena.pa != null:
		arena.pa.detach()
	arena.state = "done"
	arena.queue_free()
	await process_frame
	arena = CombatArena.new()
	main.add_child(arena)
	main.combat_game = arena
	arena.start(main, "fire", fire_callback, fire_config)
	await process_frame
	_ck("final Pepper checkpoint resumes the normal victory boundary",
		arena.state == "won" and arena.boss_encounter.finished())
	arena._finish()
	arena._finish()
	await process_frame
	_ck("fire completion saves and returns", main.combat_fire_done and main.game == "level2")
	_ck("resumed Pepper victory grants its reward exactly once",
		main.pearl_count == pearls_before_finish + 20)
	_ck("finished Pepper callback is guarded against a second reward",
		main.pearl_count == pearls_before_finish + 20)
	var checkpoints: Dictionary = main.save_data.get("boss_encounter_checkpoints", {}) as Dictionary
	_ck("normal Pepper finish clears its replay checkpoint", not checkpoints.has("fire:"))
	var replay := CombatArena.new()
	main.add_child(replay)
	replay.start(main, "fire", Callable(), fire_config)
	await process_frame
	_ck("Pepper replay starts from round zero after completed reward",
		replay.boss_encounter.completed_rounds == 0)
	replay.cancel(false)
	await process_frame

func _dual_case() -> void:
	main.game = "level2"
	var arena := CombatArena.new()
	main.add_child(arena)
	arena.start(main, "dual", Callable())
	await process_frame
	await _earn_opening(arena)
	var hp_before: int = int(arena.boss["hp"])
	arena._hit_boss("fire")
	_ck("dual shell rejects fire before ice", int(arena.boss["hp"]) == hp_before
		and arena.boss_encounter.state == BossEncounter2D.State.COUNTER_READY)
	arena._hit_boss("ice")
	_ck("dual ice opens the flashing head", arena.boss_encounter.state
		== BossEncounter2D.State.OPENING and String(arena.boss["phase"]) == "peek")
	arena._hit_boss("fire")
	_ck("dual fire lands only after the earned ice opening",
		int(arena.boss["hp"]) == hp_before - 1)
	var checkpoints: Dictionary = main.save_data.get("boss_encounter_checkpoints", {}) as Dictionary
	_ck("dual progress uses a separate checkpoint key",
		int(checkpoints.get("dual:", {}).get("rounds", 0)) == 1
		and int(checkpoints.get("fire:", {}).get("rounds", 0)) == 0)
	arena.cancel(false)
	await process_frame

func _malformed_checkpoint_case() -> void:
	var checkpoints: Dictionary = main.save_data.get("boss_encounter_checkpoints", {}) as Dictionary
	checkpoints["fire:malformed_room"] = "not a checkpoint"
	checkpoints["fire:other_room"] = {"rounds": 2, "damage": 3, "misses": 1,
		"elapsed": 22.0}
	checkpoints["dual:malformed_room"] = {"rounds": 4, "damage": 1,
		"misses": 0, "elapsed": 12.0}
	main.save_data["boss_encounter_checkpoints"] = checkpoints
	var arena := CombatArena.new()
	main.add_child(arena)
	arena.start(main, "fire", Callable(), {"room_tag": "malformed_room"})
	await process_frame
	_ck("malformed Pepper checkpoint defaults safely",
		arena.boss_encounter.completed_rounds == 0 and arena.elapsed < 1.0)
	_ck("Pepper checkpoint selection is isolated by room and kind",
		int((checkpoints["fire:other_room"] as Dictionary)["rounds"]) == 2
		and int((checkpoints["dual:malformed_room"] as Dictionary)["rounds"]) == 4)
	arena.cancel(false)
	await process_frame

func _earn_opening(arena: CombatArena) -> void:
	var guard := 0
	while arena.state == "play" and arena.boss_encounter.state \
			!= BossEncounter2D.State.COUNTER_READY \
			and arena.boss_encounter.state != BossEncounter2D.State.OPENING \
			and guard < 20:
		guard += 1
		if arena.boss_encounter.state == BossEncounter2D.State.TELL:
			var safe: Vector2 = arena.boss_encounter.patterns.readout().get(
				"safe_point", Vector2.ZERO) as Vector2
			arena._set_pepper_player_2d(safe)
			arena.boss_encounter.patterns.tick(20.0)
			arena._tick_boss(0.01)
		elif arena.boss_encounter.state == BossEncounter2D.State.STRIKE:
			arena._tick_boss(1.0)
		elif arena.boss_encounter.state in [BossEncounter2D.State.RECOVERY,
				BossEncounter2D.State.CELEBRATE]:
			arena.boss_recovery_t = 0.0
			arena._tick_boss(0.01)
		else:
			await process_frame
	_ck("adaptive movement earns a counter opening", arena.boss_encounter.state \
		in [BossEncounter2D.State.COUNTER_READY, BossEncounter2D.State.OPENING])

func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame
