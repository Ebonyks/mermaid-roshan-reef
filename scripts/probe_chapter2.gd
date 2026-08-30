extends SceneTree

## Chapter 2 progression probe.
##
## This is deliberately director-first: the boss combat itself has a dedicated
## trusted probe, while this probe owns the irreversible story handoff and its
## save contract. It never calls write_save(), so it cannot modify a player's
## save while exercising normalization and round-trip state.

const DAY_ONE_SCRIPT: GDScript = preload("res://scripts/day_one_director.gd")
const CHAPTER_TWO_SCRIPT: GDScript = preload(
	"res://scripts/chapter_two_director.gd")
const SAVE_STATE_SCRIPT: GDScript = preload("res://scripts/save_state.gd")

const INITIAL_ACTS: Array[int] = [0, 1, 2, 3]
const INITIAL_SKILLS: Array[String] = ["chef", "detective", "ballerina",
	"candy_maker"]

var checks_failed: int = 0
var main: ReefMain
var day_one: DayOneDirector
var chapter_two: ChapterTwoDirector
var defeated_payload: Dictionary = {}


func _init() -> void:
	main = ReefMain.new()
	day_one = DAY_ONE_SCRIPT.new(main) as DayOneDirector
	chapter_two = CHAPTER_TWO_SCRIPT.new(main) as ChapterTwoDirector
	main._chapter_two_director = chapter_two
	day_one.hook_event.connect(_on_day_one_event.bind(chapter_two))

	_audit_boss_boundary()
	_audit_opening_tutorials()
	_audit_detective_plot()
	_audit_ballerina_plot()
	_audit_candle_flame()
	_audit_save_round_trip()

	_print_result()
	main.free()
	quit(1 if checks_failed > 0 else 0)


func _audit_boss_boundary() -> void:
	_check("boss defeat is blocked before the boss trigger",
		not day_one.complete_giant_dust_bunny_boss()
		and day_one.day_one_active
		and not main.chapter2_active)

	# Match the real four-room director contract without starting the arena. The
	# boss combat and its touch mechanics are covered by probe_dust_boss.gd.
	day_one.bathroom_supply_hunt_step = 2
	day_one.bathroom_tools_authorized = true
	day_one.bathroom_cleanup_step = 2
	_check("the four clean rooms arm the boss door",
		day_one.complete_tutorial("bathroom")
		and day_one.complete_placeholder("pool", "pool_activity")
		and day_one.complete_activity("stuffie", "stuffie_activity")
		and day_one.complete_activity("art", "art_activity")
		and day_one.boss_door_glow
		and day_one.giant_dust_bunny_boss_triggered == false)

	var triggered: bool = day_one.trigger_giant_dust_bunny_boss()
	_check("boss trigger does not count as defeat",
		triggered
		and day_one.giant_dust_bunny_boss_triggered
		and not day_one.giant_dust_bunny_boss_defeated
		and day_one.day_one_active
		and not main.chapter2_active)

	var defeated: bool = day_one.complete_giant_dust_bunny_boss()
	_check("boss defeat starts Chapter 2 and disables Day One",
		defeated
		and day_one.giant_dust_bunny_boss_defeated
		and not day_one.day_one_active
		and main.chapter2_active
		and not defeated_payload.is_empty()
		and bool(defeated_payload.get("castle_clean", false)))
	_check("boss defeat is one-shot",
		not day_one.complete_giant_dust_bunny_boss()
		and not chapter_two.start_after_boss())

	_check("Chapter 2 opens the Opera priority objective",
		chapter_two.is_opera_priority()
		and chapter_two.active_objective
		== ChapterTwoDirector.OBJECTIVE_OPERA_TUTORIALS)


func _audit_opening_tutorials() -> void:
	_check("exactly acts 0 through 3 unlock first",
		chapter_two.initial_tutorial_act_indices() == INITIAL_ACTS
		and chapter_two.unlocked_opera_mask == 0x0F
		and main.chapter2_initial_tutorial_act_indices() == INITIAL_ACTS)
	for act_index: int in range(16):
		var expected: bool = INITIAL_ACTS.has(act_index)
		_check("tutorial gate act %d" % act_index,
			chapter_two.can_start_opera_tutorial(act_index) == expected
			and main.chapter2_opera_route_matches("opera_hall", act_index)
			== expected)
	_check("tutorial objective has no room ability yet",
		chapter_two.room_plot_action("library").is_empty()
		and chapter_two.room_plot_action("playroom").is_empty()
		and chapter_two.room_plot_action("opera_hall").is_empty())
	_check("non-Opera routes are absent during Chapter 2 tutorials",
		not main.chapter2_opera_route_matches("library", 1)
		and not main.chapter2_opera_route_matches("playroom", 2))
	_audit_opening_opera_surface()

	for act_index: int in INITIAL_ACTS:
		var skill_id: String = INITIAL_SKILLS[act_index]
		var learned: bool = chapter_two.record_opera_completion(act_index)
		_check("tutorial act %d grants %s skill" % [act_index, skill_id],
			learned and chapter_two.has_skill(skill_id)
			and (chapter_two.skill_mask & (1 << act_index)) != 0)
	_check("all four tutorials move to candle search",
		chapter_two.skill_mask == 0x0F
		and chapter_two.active_objective
		== ChapterTwoDirector.OBJECTIVE_FIND_RAINBOW_CANDLE)


func _audit_detective_plot() -> void:
	_check("detective ability is only in the Library",
		chapter_two.room_plot_action("library")
		== ChapterTwoDirector.ACTION_DETECTIVE_SEARCH
		and chapter_two.room_plot_action("playroom").is_empty()
		and chapter_two.room_plot_action("kitchen").is_empty()
		and chapter_two.room_plot_action("opera_hall").is_empty())
	_check("wrong-room detective activation is rejected",
		not chapter_two.can_launch_plot_act(
			"playroom", ChapterTwoDirector.ACT_DETECTIVE,
			ChapterTwoDirector.PLOT_CONTEXT_STUFFIE_BALLET)
		and not chapter_two.should_show_candle("playroom"))
	_check("candle is hidden until detective search",
		not chapter_two.should_show_candle("library")
		and not chapter_two.rainbow_candle_found)
	_check("plot ability cannot be invoked without a live matching room",
		not main.chapter2_activate_room_plot(
			"library", ChapterTwoDirector.ACTION_DETECTIVE_SEARCH))
	var room_surface := ChapterTwoRoomPlot.new()
	root.add_child(room_surface)
	room_surface.setup(main)
	room_surface.sync("library", false)
	_check("Library sync renders only the plot Detective button",
		room_surface.ability_button != null
		and room_surface.candle == null
		and bool(room_surface.ability_button.get_meta("plot_only", false))
		and String(room_surface.ability_button.get_meta(
			"plot_action", "")) == ChapterTwoDirector.ACTION_DETECTIVE_SEARCH)

	_check("detective search finds an unlit candle",
		chapter_two.complete_detective_search()
		and chapter_two.rainbow_candle_found
		and chapter_two.should_show_candle("library")
		and chapter_two.active_objective
		== ChapterTwoDirector.OBJECTIVE_STUFFIE_BALLET)
	_check("detective search cannot repeat",
		not chapter_two.complete_detective_search())
	room_surface.sync("library", false)
	_check("Library reveal renders the candle unlit inside the magic book",
		room_surface.ability_button == null
		and room_surface.candle != null
		and not room_surface.candle.lit
		and String(room_surface.candle.get_meta("hidden_place", ""))
		== "library_magic_book"
		and room_surface.candle.position == Vector2(588.0, 200.0)
		and room_surface.candle.scale == Vector2.ONE * 0.70)
	root.remove_child(room_surface)
	room_surface.free()


func _audit_ballerina_plot() -> void:
	_check("Ballerina plot ability is only in the Stuffie Playroom",
		chapter_two.room_plot_action("playroom")
		== ChapterTwoDirector.ACTION_STUFFIE_BALLET
		and chapter_two.room_plot_action("library").is_empty()
		and chapter_two.room_plot_action("opera_hall").is_empty())
	_check("only the Stuffie Room can launch the plot Ballerina",
		chapter_two.can_start_stuffie_ballet()
		and chapter_two.can_launch_plot_act(
			"playroom", ChapterTwoDirector.ACT_BALLERINA,
			ChapterTwoDirector.PLOT_CONTEXT_STUFFIE_BALLET)
		and not chapter_two.can_launch_plot_act(
			"library", ChapterTwoDirector.ACT_BALLERINA,
			ChapterTwoDirector.PLOT_CONTEXT_STUFFIE_BALLET)
		and not chapter_two.can_launch_plot_act(
			"playroom", ChapterTwoDirector.ACT_CHEF,
			ChapterTwoDirector.PLOT_CONTEXT_STUFFIE_BALLET))
	_audit_stuffie_hotspot_route()
	var room_surface := ChapterTwoRoomPlot.new()
	root.add_child(room_surface)
	room_surface.setup(main)
	room_surface.sync("playroom", false)
	_check("Stuffie Room sync renders only its plot Ballerina button",
		room_surface.ability_button != null
		and room_surface.candle == null
		and String(room_surface.ability_button.get_meta(
			"plot_action", "")) == ChapterTwoDirector.ACTION_STUFFIE_BALLET)

	_check("ballet completion ends current Chapter 2 goals with candle unlit",
		chapter_two.complete_stuffie_ballet(ChapterTwoDirector.ACT_BALLERINA)
		and chapter_two.stuffie_ballet_done
		and chapter_two.active_objective.is_empty()
		and chapter_two.room_plot_action("playroom").is_empty()
		and chapter_two.room_plot_action("library").is_empty())
	_check("ballet completion is one-shot",
		not chapter_two.complete_stuffie_ballet(
			ChapterTwoDirector.ACT_BALLERINA))
	room_surface.sync("library", false)
	_check("post-ballet Library keeps the candle unlit with no plot action",
		room_surface.ability_button == null
		and room_surface.candle != null
		and not room_surface.candle.lit
		and bool(room_surface.candle.get_meta("chapter2_locked_unlit", false)))
	root.remove_child(room_surface)
	room_surface.free()


func _audit_opening_opera_surface() -> void:
	var venue := OperaHouseVenue2D.new()
	root.add_child(venue)
	venue.setup(main, 0, Callable(self, "_noop_opera_launch"))
	venue.open(0)
	var buttons: Array[Button] = venue.career_buttons()
	var act_indices: Array[int] = []
	var all_enabled := true
	for button: Button in buttons:
		act_indices.append(int(button.get_meta("act_index", -1)))
		all_enabled = all_enabled and not button.disabled
	_check("opening Opera surface renders four enabled painted-door tutorials",
		buttons.size() == 4 and act_indices == INITIAL_ACTS and all_enabled)
	_check("opening Opera surface visibly points to the first tutorial door",
		venue.guide_button != null
		and int(venue.guide_button.get_meta("act_index", -1)) == 0
		and venue.guide_pointer != null and venue.guide_pointer.visible
		and bool(venue.guide_pointer.get_meta("visual_pointer", false)))
	venue.close()
	root.remove_child(venue)
	venue.free()


func _noop_opera_launch(_act_index: int) -> void:
	pass


func _audit_stuffie_hotspot_route() -> void:
	var world := OperaCareerWorld2D.new()
	world.config = {"chapter2_scene": "stuffie_room"}
	world.career_id = "ballerina"
	world.stage_points = PackedVector2Array([
		Vector2(86.0, 590.0), Vector2(245.0, 575.0),
		Vector2(420.0, 560.0), Vector2(610.0, 550.0),
		Vector2(810.0, 565.0), Vector2(1050.0, 585.0),
	])
	world.station_list = world._chapter2_stuffie_ballet_stations()
	world.active = true
	world.task_open = false
	world.reveal_t = 0.0
	world.phase_gap = 0.0
	world.armed_station = 0
	world.wander_feet = Vector2(108.0, 588.0)
	var station: Dictionary = world.station_list[0]
	var hotspot := OperaWorldHotspot2D.new()
	hotspot.setup(0, String(station.get("id", "")),
		station.get("object_pos", Vector2.ZERO) as Vector2, "", "breathe")
	hotspot.set_armed(true)
	world.station_nodes.append(hotspot)
	world._on_hotspot_pressed(0)
	var approach: Vector2 = station.get("approach_pos", Vector2.ZERO)
	var legacy_station: Dictionary = OperaStagePaths.station_by_id(
		"ballerina", String(station.get("id", "")))
	var legacy_approach: Vector2 = legacy_station.get(
		"approach_pos", Vector2.ZERO)
	_check("Stuffie Ballet hotspot accepts the current custom station",
		world.interaction_requested and world.interaction_station == 0)
	_check("Stuffie Ballet hotspot route ends at its custom room approach",
		not world.wander_route.is_empty()
		and world.wander_route[world.wander_route.size() - 1]
			.is_equal_approx(approach))
	_check("Stuffie Ballet custom approach differs from the legacy Opera room",
		not approach.is_equal_approx(legacy_approach))
	hotspot.free()
	world.free()


func _audit_candle_flame() -> void:
	var candle: ChapterTwoRainbowCandle2D = ChapterTwoRainbowCandle2D.new()
	candle.setup(false)
	_check("found candle visual starts unlit",
		not candle.lit
		and not bool(candle.get_meta("lit", true))
		and String(candle.get_meta("flame_kind", "bad")) == "none"
		and String(candle.get_meta("ordinary_state", "bad")) == "unlit")
	candle.set_lit(true)
	_check("future chapter renderer supports the accepted large rainbow flame",
		candle.lit
		and bool(candle.get_meta("lit", false))
		and String(candle.get_meta("flame_kind", "bad")) == "rainbow"
		and int(candle.get_meta("rainbow_flame_band_count", 0)) == 8
		and float(candle.get_meta(
			"rainbow_flame_body_height_ratio", 0.0)) >= 0.70)
	candle.free()

	_check("Chapter 2 exposes no action that can light the candle",
		chapter_two.active_objective.is_empty()
		and chapter_two.room_plot_action("library").is_empty())


func _audit_save_round_trip() -> void:
	var serialized_chapter: Dictionary = chapter_two.serialize_state()
	var serialized_day_one: Dictionary = day_one.serialize_state()
	var raw: Dictionary = serialized_day_one.duplicate(true)
	for key: String in serialized_chapter:
		raw[key] = serialized_chapter[key]
	raw["opera_stars"] = 0
	raw["opera_pantry"] = {"chapter2_probe": "kept"}

	var save_state: SaveState = SAVE_STATE_SCRIPT.new(main) as SaveState
	var normalised: Dictionary = save_state._normalise_save(raw)
	_check("normalization keeps boss defeat and Chapter 2 fields",
		bool(normalised.get("day_one_giant_dust_bunny_boss_defeated", false))
		and not bool(normalised.get("day_one_active", true))
		and bool(normalised.get("chapter2_active", false))
		and int(normalised.get("chapter2_unlocked_opera_mask", 0)) == 0x0F
		and int(normalised.get("chapter2_skill_mask", 0)) == 0x0F
		and String(normalised.get("chapter2_active_objective", "bad")) == ""
		and bool(normalised.get("chapter2_rainbow_candle_found", false))
		and bool(normalised.get("chapter2_stuffie_ballet_done", false)))
	_check("normalization preserves unrelated Opera pantry data",
		(normalised.get("opera_pantry", {}) as Dictionary)
		.get("chapter2_probe", "") == "kept")

	var impossible_active: Dictionary = ChapterTwoDirector.normalise_save_patch({
		"day_one_giant_dust_bunny_boss_defeated": false,
		"chapter2_active": true,
		"chapter2_unlocked_opera_mask": -1,
		"chapter2_skill_mask": -1,
	}, 0)
	_check("normalization rejects Chapter 2 before a real boss defeat",
		not bool(impossible_active.get("chapter2_active", true))
		and int(impossible_active.get(
			"chapter2_unlocked_opera_mask", -1)) == 0
		and int(impossible_active.get("chapter2_skill_mask", -1)) == 0)
	var interrupted_start: Dictionary = ChapterTwoDirector.normalise_save_patch({
		"day_one_giant_dust_bunny_boss_defeated": true,
		"chapter2_active": false,
	}, 0)
	_check("normalization heals a save interrupted at the Chapter 2 handoff",
		bool(interrupted_start.get("chapter2_active", false))
		and int(interrupted_start.get(
			"chapter2_unlocked_opera_mask", 0)) == 0x0F
		and String(interrupted_start.get("chapter2_active_objective", ""))
		== ChapterTwoDirector.OBJECTIVE_OPERA_TUTORIALS)
	_check("save validation rejects malformed Chapter 2 field types",
		not save_state._progress_types_are_valid({
			"chapter2_active": "yes",
		})
		and not save_state._known_types_are_valid({
			"chapter2_skill_mask": -1,
		}))

	var restored_main: ReefMain = ReefMain.new()
	var restored_day_one: DayOneDirector = DAY_ONE_SCRIPT.new(
		restored_main) as DayOneDirector
	var restored_chapter: ChapterTwoDirector = restored_main._chapter_two_ref()
	restored_day_one.restore_state(normalised)
	restored_chapter.restore_state(normalised)
	_check("normalized state round-trips into both directors",
		not restored_day_one.day_one_active
		and restored_day_one.giant_dust_bunny_boss_defeated
		and restored_chapter.active
		and restored_chapter.skill_mask == 0x0F
		and restored_chapter.rainbow_candle_found
		and restored_chapter.stuffie_ballet_done
		and restored_chapter.active_objective.is_empty())
	restored_main.free()


func _on_day_one_event(event_name: String, payload: Dictionary,
		chapter: ChapterTwoDirector) -> void:
	if event_name == DayOneDirector.EVENT_GIANT_DUST_BUNNY_BOSS_DEFEATED:
		defeated_payload = payload.duplicate(true)
		chapter.start_after_boss()


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("CHAPTER2|", label, ": ", ("OK" if ok else "FAIL"))


func _print_result() -> void:
	print("CHAPTER2|RESULT: ",
		("PASS" if checks_failed == 0 else "FAIL"),
		" checks_failed=", checks_failed)
