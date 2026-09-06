extends SceneTree

## Chapter 2's director-first progression probe.
##
## This deliberately exercises the eight-career causal chain without starting
## a rendered Opera game. The individual Opera mechanics have their own
## probes; this one owns ordering, rejection, save healing, and the candle
## handoff to the Ember King.

const DAY_ONE_SCRIPT: GDScript = preload("res://scripts/day_one_director.gd")
const CHAPTER_TWO_SCRIPT: GDScript = preload(
	"res://scripts/chapter_two_director.gd")
const SAVE_STATE_SCRIPT: GDScript = preload("res://scripts/save_state.gd")
const OPERA_WORLD_SCRIPT: GDScript = preload(
	"res://scripts/opera_career_world_2d.gd")

const INITIAL_ACTS: Array[int] = []
const STORY_ORDER: Array[int] = [6, 0, 3, 10, 2, 13, 11, 1]

var checks_failed: int = 0
var main: ReefMain
var day_one: DayOneDirector
var chapter_two: ChapterTwoDirector


func _init() -> void:
	main = ReefMain.new()
	day_one = DAY_ONE_SCRIPT.new(main) as DayOneDirector
	chapter_two = CHAPTER_TWO_SCRIPT.new(main) as ChapterTwoDirector
	main._chapter_two_director = chapter_two

	_audit_boss_boundary()
	_audit_tutorial_boundary()
	_audit_foyer_routes()
	_audit_cake_visual_progression()
	_audit_eight_career_sequence()
	_audit_save_healing()
	_audit_ember_protection_contract()

	_print_result()
	main.free()
	quit(1 if checks_failed > 0 else 0)


func _audit_ember_protection_contract() -> void:
	var host := ReefMain.new()
	host.chapter2_party_started = true
	host.chapter2_candle_lit = true
	var battle := ChapterTwoEmberEncounter.new(host)
	var engine := battle.begin()
	_check("Ember protection uses valid shared boss rules",
		engine.profile.is_valid() and engine.profile.phases.size() == 3)
	for round_index: int in range(3):
		engine.begin_attack(Vector2.ZERO, Vector2(0.0, -12.0), 26.0)
		var guard := 0
		while engine.state == BossEncounter2D.State.TELL and guard < 4:
			guard += 1
			engine.tick_tell(10.0)
			engine.begin_strike()
			var safe: Vector2 = engine.patterns.readout().get("safe_point", Vector2.ZERO)
			engine.resolve_impact(safe, Vector2(0.0, -12.0), 26.0)
		_check("Ember round %d offers a counter after safe dodges" % round_index,
			engine.state == BossEncounter2D.State.COUNTER_READY)
		engine.open_counter()
		_check("held and off-target input cannot protect a round",
			not battle.accept_counter(false, true, true)
			and not battle.accept_counter(true, false, true)
			and not battle.accept_counter(true, true, false)
			and host.chapter2_protection_rounds == round_index)
		_check("one visible fresh counter saves exactly one protection round",
			battle.accept_counter(true, true, true)
			and host.chapter2_protection_rounds == round_index + 1
			and not battle.accept_counter(true, true, true))
		battle.teardown()
		engine = battle.begin()
		_check("Ember re-entry preserves completed rounds",
			engine.completed_rounds == round_index + 1)
	_check("protecting friends does not itself steal the candle or finish the story",
		battle.friends_are_safe() and not host.chapter2_candle_taken
		and not host.chapter2_story_complete)
	var malformed := ChapterTwoEmberEncounter.normalise_checkpoint({
		"chapter2_protection_rounds": true, "chapter2_protection_bumps": "8",
		"chapter2_protection_misses": -1, "chapter2_lawn_started": "true",
	}, true, true, false)
	_check("Ember checkpoint rejects malformed types",
		malformed["chapter2_protection_rounds"] == 0
		and malformed["chapter2_protection_bumps"] == 0
		and malformed["chapter2_protection_misses"] == 0
		and not malformed["chapter2_lawn_started"])
	var early := ChapterTwoEmberEncounter.normalise_checkpoint({
		"chapter2_protection_rounds": 3, "chapter2_lawn_started": true,
	}, false, false, false)
	_check("Ember cannot pre-win before party preparation",
		early["chapter2_protection_rounds"] == 0
		and not early["chapter2_lawn_started"])
	battle.teardown()
	host.free()


func _audit_boss_boundary() -> void:
	_check("boss defeat is blocked before the boss trigger",
		not day_one.complete_giant_dust_bunny_boss()
		and day_one.day_one_active
		and not main.chapter2_active)
	day_one.bathroom_supply_hunt_step = 2
	day_one.bathroom_tools_authorized = true
	day_one.bathroom_cleanup_step = 2
	_check("the four clean rooms arm the boss door",
		day_one.complete_tutorial("bathroom")
		and day_one.complete_placeholder("pool", "pool_activity")
		and day_one.complete_activity("stuffie", "stuffie_activity")
		and day_one.complete_activity("art", "art_activity")
		and day_one.boss_door_glow)
	_check("boss defeat starts Chapter 2",
		day_one.trigger_giant_dust_bunny_boss()
		and day_one.complete_giant_dust_bunny_boss()
		and chapter_two.start_after_boss()
		and main.chapter2_active
		and chapter_two.active_objective
		== ChapterTwoDirector.OBJECTIVE_PARTY_PREP
		and chapter_two.next_party_act() == ChapterTwoDirector.ACT_FARMER)


func _audit_tutorial_boundary() -> void:
	_check("Detective telemetry names the accepted unlit candle asset",
		String(OPERA_WORLD_SCRIPT.CHAPTER2_DETECTIVE_RESULT_ASSET)
		== ChapterTwoRainbowCandle2D.UNLIT_TEXTURE
		and ResourceLoader.exists(
			String(OPERA_WORLD_SCRIPT.CHAPTER2_DETECTIVE_RESULT_ASSET)))
	_check("there is no standalone tutorial prelude",
		chapter_two.initial_tutorial_act_indices() == INITIAL_ACTS
		and chapter_two.unlocked_opera_mask
		== ChapterTwoDirector.FIRST_WAVE_UNLOCK_MASK
		and not chapter_two.tutorial_phase_is_active())
	_check("chapter starts at Farmer, not Detective",
		chapter_two.active_objective == ChapterTwoDirector.OBJECTIVE_PARTY_PREP
		and chapter_two.next_party_act() == ChapterTwoDirector.ACT_FARMER
		and chapter_two.room_plot_action("library").is_empty())


func _audit_foyer_routes() -> void:
	var expected_rooms: Dictionary = {
		ChapterTwoDirector.ACT_FARMER: "dining_room",
		ChapterTwoDirector.ACT_CHEF: "kitchen",
		ChapterTwoDirector.ACT_CANDY_MAKER: "kitchen",
		ChapterTwoDirector.ACT_PAINTER: "craft_room",
		ChapterTwoDirector.ACT_POP_STAR: "opera_hall",
		ChapterTwoDirector.ACT_ASTRONAUT: "mermaid_pool",
	}
	var routes_truthful := true
	for act_value: Variant in expected_rooms:
		var act_index := int(act_value)
		var owner_room := CastleCareerRoutes.chapter2_foyer_owner_room(act_index)
		routes_truthful = routes_truthful \
			and owner_room == String(expected_rooms[act_value])
		# A foyer card may guide the child to its room owner, but it must never
		# pretend that every career is launched from opera_hall.
		routes_truthful = routes_truthful \
			and (owner_room == "opera_hall" \
				or not main.chapter2_opera_route_matches("opera_hall", act_index))
	_check("foyer cards resolve to truthful Castle launch owners",
		routes_truthful)
	_check("foyer rejects a non-Opera career from hardcoded opera_hall",
		not main.chapter2_opera_route_matches("opera_hall",
		ChapterTwoDirector.ACT_FARMER)
		and main.chapter2_opera_route_matches("dining_room",
			ChapterTwoDirector.ACT_FARMER))
	_check("plot-only Ballerina and Detective keep their room owners",
		CastleCareerRoutes.chapter2_foyer_owner_room(
			ChapterTwoDirector.ACT_BALLERINA) == "playroom"
		and CastleCareerRoutes.chapter2_foyer_owner_room(
			ChapterTwoDirector.ACT_DETECTIVE) == "library")


func _audit_cake_visual_progression() -> void:
	var cake := ChapterTwoGiantCake2D.new()
	cake.setup()
	cake.apply_milestone_masks(
		ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK, 0)
	_check("Farmer hands the same five visible strawberries to the kitchen",
		cake.stage_id() == "farmer_strawberry_ingredients"
		and cake.current_cake_accessory_art_path()
		== ChapterTwoGiantCake2D.STRAWBERRY_SINGLE_TEXTURE
		and int(cake.get_meta("farmer_ingredient_sprite_count", 0))
		== ChapterTwoGiantCake2D.FINAL_CANDIED_STRAWBERRY_COUNT)
	var expected: Array[Dictionary] = [
		{"mask": 0x01, "stage": "chef_batter_unstirred",
			"phase": "mix_batter", "path":
			ChapterTwoGiantCake2D.BATTER_UNSTIRRED_TEXTURE},
		{"mask": 0x03, "stage": "chef_batter_stirred",
			"phase": "stir_batter", "path":
			ChapterTwoGiantCake2D.BATTER_STIRRED_TEXTURE},
		{"mask": 0x07, "stage": "chef_baked_tiers_unstacked",
			"phase": "bake_six_rainbow_tiers", "path":
			ChapterTwoGiantCake2D.BAKED_TIERS_UNSTACKED_TEXTURE},
		{"mask": 0x0F, "stage": "chef_stacked_unfrosted_cake",
			"phase": "stack_six_rainbow_tiers", "path":
			ChapterTwoGiantCake2D.STACKED_UNFROSTED_TEXTURE},
		{"mask": 0x1F, "stage": "chef_frosted_rainbow_cake",
			"phase": "frost_six_rainbow_tiers", "path":
			ChapterTwoGiantCake2D.FROSTED_RAINBOW_TEXTURE},
	]
	var staged_art_is_complete := true
	for stage: Dictionary in expected:
		cake.apply_milestone_masks(
			ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK,
			int(stage.get("mask", 0)))
		var path := String(stage.get("path", ""))
		staged_art_is_complete = staged_art_is_complete \
			and cake.stage_id() == String(stage.get("stage", "")) \
			and cake.visual_phase_id() == String(stage.get("phase", "")) \
			and cake.current_cake_stage_art_path() == path \
			and ResourceLoader.exists(path)
	_check("Chef visibly builds one persistent cake through five distinct states",
		staged_art_is_complete
		and int(cake.get_meta("stage_art_source_count", 0)) == 5
		and bool(cake.get_meta("stage_art_renderer_is_sprite2d", false))
		and not bool(cake.get_meta("cake_stage_contains_candle", true)))
	cake.apply_milestone_masks(
		ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK, 0x3F)
	_check("Candy Maker keeps the frosted cake and stages five glazed berries",
		cake.stage_id() == "candied_strawberries_preplacement"
		and cake.current_cake_stage_art_path()
		== ChapterTwoGiantCake2D.FROSTED_RAINBOW_TEXTURE
		and cake.current_cake_accessory_art_path()
		== ChapterTwoGiantCake2D.CANDIED_STRAWBERRY_TRAY_TEXTURE
		and bool(cake.get_meta("candied_tray_is_sprite2d", false)))
	cake.apply_milestone_masks(
		ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK, 0x7F)
	_check("Candy placement reveals the selected runtime cake without a candle",
		cake.stage_id() == "placed_final"
		and cake.current_cake_stage_art_path()
		== ChapterTwoGiantCake2D.FINAL_CAKE_TEXTURE
		and cake.current_cake_accessory_art_path().is_empty()
		and bool(cake.get_meta("final_cake_sprite_visible", false))
		and int(cake.get_meta("final_candied_strawberry_count", 0))
		== ChapterTwoGiantCake2D.FINAL_CANDIED_STRAWBERRY_COUNT
		and not bool(cake.get_meta("cake_stage_contains_candle", true)))
	var chef := ChapterTwoCareerSceneAdapter.resolve("chef")
	var chef_phases := chef.get("phases", []) as Array
	var candy := ChapterTwoCareerSceneAdapter.resolve("candymaker")
	var candy_phases := candy.get("phases", []) as Array
	var phase_assets_are_truthful := chef_phases.size() == 5 \
		and candy_phases.size() == 4
	for phase_index in range(chef_phases.size()):
		var phase := chef_phases[phase_index] as Dictionary
		phase_assets_are_truthful = phase_assets_are_truthful \
			and String(phase.get("cake_stage_asset", "")) \
			== String(expected[phase_index].get("path", ""))
	phase_assets_are_truthful = phase_assets_are_truthful \
		and String((candy_phases[2] as Dictionary).get(
			"cake_accessory_asset", "")) \
		== ChapterTwoGiantCake2D.CANDIED_STRAWBERRY_TRAY_TEXTURE \
		and String((candy_phases[3] as Dictionary).get(
			"cake_stage_asset", "")) \
		== ChapterTwoGiantCake2D.FINAL_CAKE_TEXTURE
	_check("Chef and Candy Maker phase data names the actual resulting art",
		phase_assets_are_truthful)
	cake.free()


func _audit_eight_career_sequence() -> void:
	_check("the Chapter 2 party roster is exactly eight stable Opera bits",
		ChapterTwoPartyPlan.ALL_PARTY_MASK == 0x2C4F
		and ChapterTwoPartyPlan.all_act_indices() == STORY_ORDER)
	_check("Chef cannot precede Farmer",
		not chapter_two.can_start_chapter2_act(ChapterTwoDirector.ACT_CHEF)
		and not chapter_two.record_party_contribution(
			ChapterTwoDirector.ACT_CHEF)
		and chapter_two.next_party_act() == ChapterTwoDirector.ACT_FARMER)
	_check("stale phase callbacks cannot award the wrong act",
		not chapter_two.record_opera_phase_event(
			ChapterTwoDirector.ACT_CHEF, 0, "MIX")
		and chapter_two.cake_piece_mask == 0
		and (chapter_two.skill_mask & (1 << ChapterTwoDirector.ACT_CHEF)) == 0)
	var farmer_overrides: Dictionary = chapter_two.opera_config_overrides(
		"", ChapterTwoDirector.ACT_FARMER)
	var farmer_context: Dictionary = farmer_overrides.get(
		"run_context", {}) as Dictionary
	var farmer_callbacks: Dictionary = farmer_context.get(
		"callbacks", {}) as Dictionary
	var farmer_phase_callback: Callable = farmer_callbacks.get(
		"phase_completed", Callable())
	main.opera_active_act_index = ChapterTwoDirector.ACT_FARMER
	_check("Farmer phase callback fills exactly five strawberries",
		farmer_phase_callback.is_valid()
		and farmer_phase_callback.call({"phase_index": 0,
			"phase_name": "GATHER STRAWBERRIES"})
		and chapter_two.strawberry_mask
		== ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK
		and chapter_two.job_phase_masks[0] == 1
		and (chapter_two.skill_mask &
			(1 << ChapterTwoDirector.ACT_FARMER)) != 0
		and main.opera_stars == 0)
	main.opera_active_act_index = -1

	_check("ordered party act %d completes" % ChapterTwoDirector.ACT_FARMER,
		chapter_two.can_start_chapter2_act(ChapterTwoDirector.ACT_FARMER)
		and chapter_two.record_party_contribution(ChapterTwoDirector.ACT_FARMER)
		and not chapter_two.record_party_contribution(
			ChapterTwoDirector.ACT_FARMER))
	var chef_overrides: Dictionary = chapter_two.opera_config_overrides(
		"", ChapterTwoDirector.ACT_CHEF)
	var chef_context: Dictionary = chef_overrides.get(
		"run_context", {}) as Dictionary
	var chef_callbacks: Dictionary = chef_context.get(
		"callbacks", {}) as Dictionary
	var chef_phase_callback: Callable = chef_callbacks.get(
		"phase_completed", Callable())
	main.opera_active_act_index = ChapterTwoDirector.ACT_CHEF
	_check("Chef phase callback records the bottom cake piece",
		chef_phase_callback.is_valid()
		and chef_phase_callback.call({"phase_index": 0, "phase_name": "MIX"})
		and chapter_two.cake_piece_mask == 1
		and chapter_two.job_phase_masks[1] == 1
		and main.opera_stars == 0)
	main.opera_active_act_index = -1
	var normal_acts: Array[int] = [
		ChapterTwoDirector.ACT_CHEF,
		ChapterTwoDirector.ACT_CANDY_MAKER,
		ChapterTwoDirector.ACT_PAINTER,
	]
	for act_index: int in normal_acts:
		_check("ordered party act %d completes" % act_index,
			chapter_two.can_start_chapter2_act(act_index)
			and chapter_two.record_party_contribution(act_index)
			and not chapter_two.record_party_contribution(act_index))
	_check("Farmer ingredient and Chef cake milestones persist",
		chapter_two.farmer_strawberries_ready
		and chapter_two.chef_cake_baked
		and chapter_two.candy_cake_finished
		and chapter_two.strawberry_mask
		== ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK
		and chapter_two.cake_piece_mask
		== ChapterTwoDirector.CAKE_PIECE_REQUIRED_MASK
		and chapter_two.next_party_act() == ChapterTwoDirector.ACT_BALLERINA)
	_check("Painter unlocks the second four story careers",
		chapter_two.unlocked_opera_mask
		== ChapterTwoPartyPlan.ALL_PARTY_MASK)

	_check("Ballerina remains a plot-owned room action",
		chapter_two.active_objective == ChapterTwoDirector.OBJECTIVE_STUFFIE_BALLET
		and chapter_two.room_plot_action("playroom")
		== ChapterTwoDirector.ACTION_STUFFIE_BALLET
		and not chapter_two.can_start_chapter2_act(
			ChapterTwoDirector.ACT_BALLERINA))
	_check("Ballerina completes after Painter",
		chapter_two.complete_stuffie_ballet(ChapterTwoDirector.ACT_BALLERINA)
		and chapter_two.stuffie_ballet_done
		and chapter_two.next_party_act() == ChapterTwoDirector.ACT_POP_STAR)

	_check("Pop Star sound check follows Ballerina",
		chapter_two.record_party_contribution(ChapterTwoDirector.ACT_POP_STAR)
		and chapter_two.next_party_act() == ChapterTwoDirector.ACT_ASTRONAUT)
	_check("Astronaut parks the rocket before the final candle search",
		chapter_two.record_party_contribution(ChapterTwoDirector.ACT_ASTRONAUT)
		and chapter_two.next_party_act() == ChapterTwoDirector.ACT_DETECTIVE
		and chapter_two.active_objective
		== ChapterTwoDirector.OBJECTIVE_FIND_RAINBOW_CANDLE)
	var every_skill_named := true
	for story_act: int in STORY_ORDER:
		every_skill_named = every_skill_named \
			and not chapter_two._skill_for_act(story_act).is_empty()
	_check("all eight Chapter 2 careers teach a nonempty truthful skill",
		every_skill_named
		and (chapter_two.skill_mask & ChapterTwoPartyPlan.ALL_PARTY_MASK)
		== (ChapterTwoPartyPlan.ALL_PARTY_MASK
			& ~(1 << ChapterTwoDirector.ACT_DETECTIVE)))
	_audit_story_voice_routing()

	_check("Detective waits until every earlier preparation is ready",
		chapter_two.active_objective
		== ChapterTwoDirector.OBJECTIVE_FIND_RAINBOW_CANDLE
		and chapter_two.room_plot_action("library")
		== ChapterTwoDirector.ACTION_DETECTIVE_SEARCH
		and not chapter_two.party_is_ready())
	_check("Detective finds the last missing candle unlit",
		chapter_two.complete_detective_search()
		and chapter_two.rainbow_candle_found
		and not chapter_two.candle_lit
		and chapter_two.party_piece_mask == ChapterTwoPartyPlan.ALL_PARTY_MASK
		and chapter_two.party_is_ready()
		and chapter_two.active_objective
		== ChapterTwoDirector.OBJECTIVE_MAIN_HALL_PARTY)
	_check("party event phase stays at candle-found until ignition",
		chapter_two.party_event_phase
		== ChapterTwoDirector.PARTY_EVENT_CANDLE_FOUND)
	_check("party cannot start in unrelated rooms",
		not chapter_two.start_main_hall_party("library")
		and not chapter_two.trigger_ember_king_crash("main_hall"))
	_check("party ignition starts only after all eight milestones",
		chapter_two.start_main_hall_party("main_hall")
		and chapter_two.candle_lit
		and chapter_two.party_event_phase
		== ChapterTwoDirector.PARTY_EVENT_IGNITION
		and chapter_two.party_started
		and not chapter_two.candle_taken)
	var room_plot := ChapterTwoRoomPlot.new()
	room_plot.setup(main)
	room_plot.sync("main_hall", false)
	_check("Main Hall offers the lawn route without advancing the story on a timer",
		not room_plot.is_processing()
		and room_plot.get_meta("party_sequence_route", "") == "sky_lagoon_lawn")
	room_plot.sync("library", false)
	_check("leaving Main Hall cancels party beat timing without progress",
		not room_plot.is_processing()
		and chapter_two.party_event_phase
		== ChapterTwoDirector.PARTY_EVENT_IGNITION)
	room_plot.free()
	_check("the safe ember scout beat precedes the King take",
		chapter_two.record_ember_scout()
		and chapter_two.party_event_phase
		== ChapterTwoDirector.PARTY_EVENT_SCOUT_SEEN)
	main.chapter2_lawn_started = true
	main.chapter2_lawn_beat = 5
	_check("King theft rejects missing protection and Main Hall callers",
		not chapter_two.trigger_ember_king_crash("sky_lagoon_lawn")
		and not chapter_two.trigger_ember_king_crash("main_hall"))
	main.chapter2_protection_rounds = 3
	var king_take_ok := chapter_two.trigger_ember_king_crash("sky_lagoon_lawn")
	_check("Ember King takes the lit candle for his birthday",
		king_take_ok
		and chapter_two.ember_king_crashed
		and chapter_two.ember_son_seen
		and chapter_two.party_event_phase
		== ChapterTwoDirector.PARTY_EVENT_KING_TAKE_COMPLETE
		and not chapter_two.candle_lit
		and chapter_two.candle_taken
		and not chapter_two.story_complete)
	var party_table := ChapterTwoPartyTable2D.new()
	party_table.setup(main)
	_check("Main Hall does not reintroduce the departed Prince placeholder",
		not bool(party_table.get_meta("ember_son_visually_depicted", true)))
	_check("Ember take removes only the candle and leaves the cake",
		bool(party_table.get_meta("rainbow_candle_taken", false))
		and bool(party_table.get_meta("cake_remains_after_candle_taken", false))
		and bool(party_table.get_meta("final_cake_ready", false)))
	party_table.free()


func _audit_story_voice_routing() -> void:
	var all_rewritten_jobs_silent := true
	for career_id: String in ["farmer", "candymaker", "painter"]:
		var resolved := ChapterTwoCareerSceneAdapter.resolve(career_id)
		for phase_value: Variant in resolved.get("phases", []):
			var phase := phase_value as Dictionary
			all_rewritten_jobs_silent = all_rewritten_jobs_silent \
				and String(phase.get("vo", "")).is_empty()
	var detective := ChapterTwoCareerSceneAdapter.resolve("detective")
	var detective_phases := detective.get("phases", []) as Array
	var final_detective := detective_phases[detective_phases.size() - 1] \
		as Dictionary
	_check("rewritten story phases never route false legacy recordings",
		all_rewritten_jobs_silent
		and String(final_detective.get("vo", "")).is_empty())
	var pop_star := ChapterTwoCareerSceneAdapter.resolve("popstar")
	var pop_phases := pop_star.get("phases", []) as Array
	_check("truthful existing sound-check recording remains routed",
		String((pop_phases[0] as Dictionary).get("vo", ""))
		== "op_popstar_sound_check")


func _audit_save_healing() -> void:
	var malformed: Dictionary = ChapterTwoDirector.normalise_save_patch({
		"day_one_giant_dust_bunny_boss_defeated": true,
		"chapter2_skill_mask": 0x0F,
		"chapter2_party_piece_mask": (1 << ChapterTwoDirector.ACT_FARMER)
			| (1 << ChapterTwoDirector.ACT_ASTRONAUT),
		"chapter2_party_started": true,
		"chapter2_ember_king_crashed": true,
	}, 0)
	_check("save healing rejects skipped milestones and early crash",
		int(malformed.get("chapter2_party_piece_mask", -1))
		== (1 << ChapterTwoDirector.ACT_FARMER)
		and not bool(malformed.get("chapter2_party_started", true))
		and not bool(malformed.get("chapter2_ember_king_crashed", true))
		and bool(malformed.get("chapter2_farmer_strawberries_ready", false))
		and not bool(malformed.get("chapter2_chef_cake_baked", true)))
	var complete: Dictionary = chapter_two.serialize_state()
	complete["day_one_giant_dust_bunny_boss_defeated"] = true
	var save_state: SaveState = SAVE_STATE_SCRIPT.new(main) as SaveState
	var normalised: Dictionary = save_state._normalise_save(complete)
	_check("save normalization retains all eight milestones",
		int(normalised.get("chapter2_party_piece_mask", 0))
		== ChapterTwoPartyPlan.ALL_PARTY_MASK
		and bool(normalised.get("chapter2_farmer_strawberries_ready", false))
		and bool(normalised.get("chapter2_chef_cake_baked", false))
		and bool(normalised.get("chapter2_candy_cake_finished", false))
		and bool(normalised.get("chapter2_candle_taken", false)))
	_check("new milestone fields have strict boolean validation",
		not save_state._known_types_are_valid({
			"chapter2_farmer_strawberries_ready": "yes"})
		and not save_state._progress_types_are_valid({
			"chapter2_candy_cake_finished": 1}))
	var partial: Dictionary = ChapterTwoDirector.normalise_save_patch({
		"day_one_giant_dust_bunny_boss_defeated": true,
		"chapter2_strawberry_mask": 0x1F,
		"chapter2_cake_piece_mask": 0x7F,
		"chapter2_job_phase_masks": [0xFFFF, "bad", 0, 0, 0, 0, 0, 0],
		"chapter2_party_event_phase": 99,
	}, 0)
	_check("new masks are fixed, typed, and heal future bits",
		int(partial.get("chapter2_strawberry_mask", 0))
		== ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK
		and int(partial.get("chapter2_cake_piece_mask", 0))
		== ChapterTwoDirector.CAKE_PIECE_REQUIRED_MASK
		and (partial.get("chapter2_job_phase_masks", []) as Array).size() == 8
		and int((partial.get("chapter2_job_phase_masks", []) as Array)[0])
		== 0x0F
		and int(partial.get("chapter2_party_event_phase", -1))
		== ChapterTwoDirector.PARTY_EVENT_PREP)
	var skipped_cake_piece: Dictionary = ChapterTwoDirector.normalise_save_patch({
		"day_one_giant_dust_bunny_boss_defeated": true,
		"chapter2_party_piece_mask": 1 << ChapterTwoDirector.ACT_FARMER,
		"chapter2_cake_piece_mask": 0x5F,
	}, 0)
	_check("save healing stores the same contiguous cake rendered after load",
		int(skipped_cake_piece.get("chapter2_cake_piece_mask", -1)) == 0x1F)
	var resumable: Dictionary = ChapterTwoDirector.normalise_save_patch({
		"day_one_giant_dust_bunny_boss_defeated": true,
		"chapter2_party_piece_mask": 1 << ChapterTwoDirector.ACT_FARMER,
		"chapter2_cake_piece_mask": 3,
		"chapter2_job_phase_masks": [3, 31, 7, 7, 7, 15, 15, 7],
	}, 0)
	chapter_two.restore_state(resumable)
	var resumable_masks: Array = resumable.get(
		"chapter2_job_phase_masks", []) as Array
	_check("phase healing preserves the current job and prunes later jobs",
		int(resumable_masks[0]) == 3
		and int(resumable_masks[1]) == 3
		and int(resumable_masks[2]) == 0
		and chapter_two.resume_phase_index_for_act(
			ChapterTwoDirector.ACT_FARMER) == 2)


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("CHAPTER2|", label, ": ", ("OK" if ok else "FAIL"))


func _print_result() -> void:
	print("CHAPTER2|RESULT: ",
		("PASS" if checks_failed == 0 else "FAIL"),
		" checks_failed=", checks_failed)
