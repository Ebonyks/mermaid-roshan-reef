extends SceneTree
## Real SaveState writes and fresh reloads, without advancing the debounce clock.

class SaveFixture extends ReefMain:
	func _update_hud() -> void:
		pass

	func _on_chapter_two_hook_event(_event_name: String, _payload: Dictionary) -> void:
		pass # Presentation only; milestone callbacks still use the real SaveState.

const SAVE_PATH := "user://alpha_milestones.json"
var bad: int = 0

func _init() -> void:
	var main: SaveFixture = _load_fixture()
	main.save_data["alpha_unknown_field"] = {"keep": 42}
	main._day_one_ref().restore_state({"day_one_active": false,
		"day_one_giant_dust_bunny_boss_defeated": true})
	main._chapter_two_ref().restore_state({"chapter2_active": true,
		"day_one_giant_dust_bunny_boss_defeated": true})
	main._write_save()
	for index: int in range(5):
		_check("berry accepted %d" % index, main.chapter2_record_strawberry_pick(index))
		_assert_saved(main, "chapter2_strawberry_mask", (1 << (index + 1)) - 1)
		_check("repeated berry cannot advance", not main.chapter2_record_strawberry_pick(index))
	var completed_mask: int = 0
	for entry: Dictionary in ChapterTwoPartyPlan.LIVE_CAREERS:
		var act_index: int = int(entry["act_index"])
		var phases: Array = ChapterTwoCareerSceneAdapter.phase_set(String(entry["career"]).replace("_", "")).get("phases", [])
		for phase_index: int in range(phases.size()):
			_check("phase accepted %d/%d" % [act_index, phase_index],
				main.chapter2_on_opera_phase_completed(act_index, phase_index))
			_assert_saved(main, "chapter2_job_phase_masks", main.chapter2_job_phase_masks)
			_assert_saved(main, "chapter2_cake_piece_mask", main.chapter2_cake_piece_mask)
		if act_index in [ChapterTwoDirector.ACT_BALLERINA, ChapterTwoDirector.ACT_DETECTIVE]:
			var context: String = ChapterTwoDirector.PLOT_CONTEXT_STUFFIE_BALLET \
				if act_index == ChapterTwoDirector.ACT_BALLERINA else ChapterTwoDirector.PLOT_CONTEXT_DETECTIVE_CANDLE
			main.chapter2_on_opera_completed(act_index, context)
			_check("plot contribution accepted %d" % act_index,
				(main.chapter2_party_piece_mask & (1 << act_index)) != 0)
		else:
			_check("party contribution accepted %d" % act_index,
				main.chapter2_record_party_contribution(act_index))
		completed_mask |= 1 << act_index
		_assert_saved(main, "chapter2_party_piece_mask", completed_mask)
	main._day_one_ref().restore_state({"day_one_active": true,
		"day_one_current_room": "art", "day_one_completed_rooms": ["bathroom", "pool", "stuffie"],
		"day_one_cleaned_rooms": ["bathroom", "pool", "stuffie"]})
	for material: String in DayOneDirector.ART_MATERIAL_IDS:
		_check("art material accepted " + material, main.day_one_record_art_cleanup("material", material))
		_assert_saved(main, "day_one_art_collected_materials", main.day_one_art_collected_materials)
	for grime: String in DayOneDirector.ART_GRIME_IDS:
		_check("art grime accepted " + grime, main.day_one_record_art_cleanup("grime", grime))
		_assert_saved(main, "day_one_art_cleaned_grime", main.day_one_art_cleaned_grime)
	main._day_one_ref().restore_state({"day_one_active": true, "day_one_current_room": "pool"})
	for index: int in range(6):
		main.day_one_record_pool_activity_progress(1 << index, 0, 0)
		_assert_saved(main, "day_one_pool_skimmer_mask", (1 << (index + 1)) - 1)
	var generation_before: int = main.save_generation
	for frame: int in range(120):
		main.day_one_record_pool_activity_progress(0, 0, 0)
	_check("continuous unearned pool updates do not rewrite the disk save", main.save_generation == generation_before)
	for index: int in range(3):
		main.day_one_record_pool_activity_progress(0, 1 << index, 0)
		_assert_saved(main, "day_one_pool_waterfall_mask", (1 << (index + 1)) - 1)
	for count: int in range(1, 9):
		main.day_one_record_pool_activity_progress(0, 0, count)
		_assert_saved(main, "day_one_pool_seahorse_tugs", count)
	main.free()
	print("ALPHA_SAVE|RESULT: ", "ALL OK" if bad == 0 else "%d FAILED" % bad)
	quit(1 if bad > 0 else 0)

func _load_fixture() -> SaveFixture:
	var fixture := SaveFixture.new()
	fixture.music = AudioStreamPlayer.new()
	fixture.add_child(fixture.music)
	fixture._save_state = SaveState.new(fixture, SAVE_PATH)
	fixture._load_save()
	return fixture

func _assert_saved(main: SaveFixture, key: String, expected: Variant) -> void:
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	var disk: Dictionary = JSON.parse_string(file.get_as_text()) as Dictionary
	file.close()
	_check("disk milestone " + key, disk.get(key) == JSON.parse_string(JSON.stringify(expected)) and not main.save_pending)
	var fresh: SaveFixture = _load_fixture()
	var state: Dictionary = fresh._chapter_two_ref().serialize_state() if key.begins_with("chapter2_") \
		else fresh._day_one_ref().serialize_state()
	_check("restart milestone " + key, state.get(key) == expected)
	_check("unknown keys retained", int((fresh.save_data.get("alpha_unknown_field", {}) as Dictionary).get("keep", -1)) == 42)
	fresh.free()

func _check(label: String, ok: bool) -> void:
	print("ALPHA_SAVE|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1
