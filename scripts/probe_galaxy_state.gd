extends SceneTree
# Butterfly World persistence/origin regression probe. It exercises the state
# transitions directly so the trusted headless suite does not need to render an
# entire planet merely to prove that progress and return locations are sound.

var main: ReefMain
var checks_failed := 0

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("GALAXY_STATE|", label, ": ", ("OK" if ok else "FAIL"), (" " + detail if detail != "" else ""))

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _bare_galaxy() -> GalaxyLevel:
	var galaxy := GalaxyLevel.new()
	galaxy.process_mode = Node.PROCESS_MODE_DISABLED
	galaxy._main = main
	var big_label := Label.new()
	var hint_label := Label.new()
	galaxy.add_child(big_label)
	galaxy.add_child(hint_label)
	galaxy._lbl_big = big_label
	galaxy._lbl_hint = hint_label
	get_root().add_child(galaxy)
	return galaxy

func _init() -> void:
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(2)

	# The grand reward is paid once, and only once.
	main.bwd_done = false
	main.fairy_skin_unlocked = false
	main.pearl_count = 6
	var first: GalaxyLevel = _bare_galaxy()
	first._win()
	_ck("first_reward_paid", main.pearl_count == 46 and main.bwd_done and main.fairy_skin_unlocked)
	var second: GalaxyLevel = _bare_galaxy()
	second._win()
	_ck("completed_reward_not_repeated", main.pearl_count == 46 and second._state != "won", "pearls=%d state=%s" % [main.pearl_count, second._state])
	first.free()
	second.free()

	# A completed save builds the Butterfly World as a playground: the seven
	# babies and the grand reward must not be reconstructed at all.
	var completed := GalaxyLevel.new()
	completed.process_mode = Node.PROCESS_MODE_DISABLED
	get_root().add_child(completed)
	completed.start(main, Callable())
	_ck("completed_world_has_no_quest_rewards",
		completed._shards_got == GalaxyLevel.SHARDS
		and completed._shard_nodes.is_empty()
		and completed._grand == null
		and not completed._grand_active,
		"got=%d live=%d grand=%s active=%s" % [completed._shards_got, completed._shard_nodes.size(), str(completed._grand), str(completed._grand_active)])
	completed._teardown(false)
	await _frames(2)

	# Individual rescued butterflies checkpoint through the compatible sticker
	# map; only the six still missing are rebuilt next visit.
	main.bwd_done = false
	main.stickers["_bwd_butterfly_0"] = true
	var partial := GalaxyLevel.new()
	partial.process_mode = Node.PROCESS_MODE_DISABLED
	partial._main = main
	get_root().add_child(partial)
	partial._build_shards()
	_ck("partial_rescue_restored", partial._shards_got == 1 and partial._shard_nodes.size() == GalaxyLevel.SHARDS - 1, "got=%d live=%d" % [partial._shards_got, partial._shard_nodes.size()])
	partial.free()

	# Direct ocean return restores the exact position and ocean environment.
	var ocean_origin := Vector3(31.0, 18.0, -42.0)
	main.game = "galaxy"
	main.galaxy_from = ""
	main.galaxy_return_set = true
	main.galaxy_return_pos = ocean_origin
	main.player.position = Vector3.ZERO
	main._end_galaxy(false)
	_ck("returns_to_ocean_origin", main.game == "" and main.player.position.distance_to(ocean_origin) < 0.1 and main.we_node.environment == main.world_env, "distance=%.2f" % main.player.position.distance_to(ocean_origin))
	_ck("ocean_return_state_cleared",
		not main.galaxy_return_set
		and main.galaxy_from == ""
		and main.galaxy_return_pos == Vector3.ZERO
		and not main.galaxy_level2_open)

	# A Level-2 round trip rebuilds one clean lagoon, preserves closed/open state,
	# and restores Roshan beside the exact doorway she entered.
	main.process_mode = Node.PROCESS_MODE_DISABLED
	var lagoon_origin: Vector3 = main.LEVEL2_POS + Vector3(42.0, 3.0, 35.0)
	main.level2_done_once = false
	main.l2_open = false
	main.l2_star_progress = [true, false, false]
	main.game = "galaxy"
	main.galaxy_from = "level2"
	main.galaxy_level2_open = false
	main.galaxy_return_set = true
	main.galaxy_return_pos = lagoon_origin
	main.bw_cool = 0.0
	main.kart_cool = 0.0
	main._end_galaxy(false)
	await _frames(2)
	_ck("returns_to_closed_lagoon", main.game == "level2" and not main.l2_open, "game=%s open=%s" % [main.game, str(main.l2_open)])
	_ck("lagoon_position_restored", main.player.position.distance_to(lagoon_origin) < 0.1, "distance=%.2f" % main.player.position.distance_to(lagoon_origin))
	_ck("partial_stars_preserved", main.l2_star_progress == [true, false, false], str(main.l2_star_progress))
	_ck("lagoon_environment_restored", main.we_node.environment == main.arena_env)
	_ck("closed_return_state_cleared",
		not main.galaxy_return_set
		and main.galaxy_from == ""
		and main.galaxy_return_pos == Vector3.ZERO
		and not main.galaxy_level2_open
		and main.bw_cool >= 3.0
		and main.kart_cool >= 3.0)

	var open_origin: Vector3 = main.LEVEL2_POS + Vector3(-28.0, 4.0, -48.0)
	main.game = "galaxy"
	main.l2_open = true
	main.galaxy_from = "level2"
	main.galaxy_level2_open = true
	main.galaxy_return_set = true
	main.galaxy_return_pos = open_origin
	main.bw_cool = 0.0
	main.kart_cool = 0.0
	main._end_galaxy(false)
	await _frames(2)
	_ck("returns_to_open_lagoon", main.game == "level2" and main.l2_open and main.player.position.distance_to(open_origin) < 0.1, "open=%s distance=%.2f" % [str(main.l2_open), main.player.position.distance_to(open_origin)])
	_ck("open_return_state_cleared",
		not main.galaxy_return_set
		and main.galaxy_from == ""
		and main.galaxy_return_pos == Vector3.ZERO
		and not main.galaxy_level2_open
		and main.bw_cool >= 3.0
		and main.kart_cool >= 3.0)

	print("GALAXY_STATE|RESULT: ", ("ALL OK" if checks_failed == 0 else "FAIL (%d)" % checks_failed))
	quit(checks_failed)
