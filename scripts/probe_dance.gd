extends SceneTree
# Smoke test for the touch rhythm demo. It checks that an exploratory tap is
# harmless, real notes can be judged in every lane, song switching rebuilds the
# chart, and closing restores the world instead of awarding passive progress.


func _init() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	var trophies_before: int = main.trophies
	main._open_dance_demo()
	await process_frame
	var dance: DanceEngine = main.dance_engine as DanceEngine
	var bad := 0
	if dance == null or not dance.active or dance.notes.is_empty():
		print("DANCE|open: FAIL demo did not start")
		quit()
		return
	print("DANCE|open: OK %d-note beginner chart" % dance.notes.size())

	var hits_before: int = dance.happy_hits
	dance.song_time = 0.0
	dance._press_lane(0)
	if dance.happy_hits != hits_before:
		print("DANCE|forgiveness: FAIL exploratory tap changed score")
		bad += 1
	else:
		print("DANCE|forgiveness: OK exploratory tap is harmless")

	var lanes_hit := {}
	for data in dance.notes:
		var lane := int(data["lane"])
		if lanes_hit.has(lane):
			continue
		dance.song_time = float(data["time"])
		dance._press_lane(lane)
		lanes_hit[lane] = true
		if lanes_hit.size() == 4:
			break
	if dance.happy_hits != 4 or lanes_hit.size() != 4:
		print("DANCE|input: FAIL arrows were not judged in all four lanes")
		bad += 1
	else:
		print("DANCE|input: OK touch/keyboard lane path judges all arrows")

	var old_song: int = dance.song_index
	dance._change_song(1)
	await process_frame
	if dance.song_index == old_song or dance.notes.is_empty():
		print("DANCE|songs: FAIL song switch did not rebuild the chart")
		bad += 1
	else:
		print("DANCE|songs: OK existing-song selector rebuilt the chart")

	dance.close_demo()
	await process_frame
	if paused or main.trophies != trophies_before:
		print("DANCE|close: FAIL world state/progress was not restored")
		bad += 1
	else:
		print("DANCE|close: OK world resumed with no passive reward")

	# Castle placement contract: no butterfly count may gate the hall, and the
	# central star rug must launch the same tested rhythm engine.
	main._start_galaxy()
	await process_frame
	var galaxy: GalaxyLevel = main.galaxy_game as GalaxyLevel
	galaxy._shards_got = 0
	galaxy._enter_castle_gate()
	if galaxy._mode != "hall" or not galaxy._hall_built:
		print("DANCE|castle: FAIL zero-butterfly castle entry was blocked")
		bad += 1
	else:
		print("DANCE|castle: OK castle is open with zero butterflies")
	galaxy._cpos = Vector3.ZERO
	galaxy._dance_t = 0.0
	galaxy._tick_hall(1.0 / 60.0)
	await process_frame
	if not dance.active:
		print("DANCE|rug: FAIL Butterfly Castle rug did not launch rhythm engine")
		bad += 1
	else:
		print("DANCE|rug: OK Butterfly Castle rug launches rhythm engine")
		dance.close_demo()
		await process_frame
	galaxy._teardown(false)
	await process_frame
	print("DANCE|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()
