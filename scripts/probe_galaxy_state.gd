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
	galaxy._main = main
	galaxy._lbl_big = Label.new()
	galaxy._lbl_hint = Label.new()
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
	first.queue_free()
	second.queue_free()

	# Individual rescued butterflies checkpoint through the compatible sticker
	# map; only the six still missing are rebuilt next visit.
	main.bwd_done = false
	main.stickers["_bwd_butterfly_0"] = true
	var partial := GalaxyLevel.new()
	partial._main = main
	get_root().add_child(partial)
	partial._build_shards()
	_ck("partial_rescue_restored", partial._shards_got == 1 and partial._shard_nodes.size() == GalaxyLevel.SHARDS - 1, "got=%d live=%d" % [partial._shards_got, partial._shard_nodes.size()])
	partial.queue_free()
	await _frames(2)

	# Direct ocean return restores the exact position and ocean environment.
	var ocean_origin := Vector3(31.0, 18.0, -42.0)
	main.game = "galaxy"
	main.galaxy_from = ""
	main.galaxy_return_set = true
	main.galaxy_return_pos = ocean_origin
	main.player.position = Vector3.ZERO
	main._end_galaxy(false)
	_ck("returns_to_ocean_origin", main.game == "" and main.player.position.distance_to(ocean_origin) < 0.1 and main.we_node.environment == main.world_env, "distance=%.2f" % main.player.position.distance_to(ocean_origin))

	# A Level-2 round trip rebuilds one clean lagoon, preserves closed/open state,
	# and restores Roshan beside the exact doorway she entered.
	var lagoon_origin: Vector3 = main.LEVEL2_POS + Vector3(42.0, 12.0, 35.0)
	main.level2_done_once = false
	main.l2_open = false
	main.l2_star_progress = [true, false, false]
	main.game = "galaxy"
	main.galaxy_from = "level2"
	main.galaxy_level2_open = false
	main.galaxy_return_set = true
	main.galaxy_return_pos = lagoon_origin
	main._end_galaxy(false)
	await _frames(30)
	_ck("returns_to_closed_lagoon", main.game == "level2" and not main.l2_open, "game=%s open=%s" % [main.game, str(main.l2_open)])
	_ck("lagoon_position_restored", main.player.position.distance_to(lagoon_origin) < 0.1, "distance=%.2f" % main.player.position.distance_to(lagoon_origin))
	_ck("partial_stars_preserved", main.l2_star_progress == [true, false, false], str(main.l2_star_progress))
	_ck("lagoon_environment_restored", main.we_node.environment == main.arena_env)

	print("GALAXY_STATE|RESULT: ", ("ALL OK" if checks_failed == 0 else "FAIL (%d)" % checks_failed))
	quit(checks_failed)
