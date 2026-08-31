extends SceneTree

## Adversarial Chapter 2 Farmer resume probe.
##
## This intentionally builds the real OperaCareerWorld2D Farmer scene, opens
## its actual gather phase, and presses the actual TextureButtons after a
## partial saved mask. It is not a director callback-only test: every case
## verifies the scene's local progress, button state, and exact completion.

const MAIN_SCENE := preload("res://scenes/main.tscn")
const WORLD_SCRIPT := preload("res://scripts/opera_career_world_2d.gd")
const COMPETITION_SCRIPT := preload("res://scripts/opera_competition.gd")
const ADAPTER_SCRIPT := preload("res://scripts/chapter_two_career_scene_adapter.gd")
const DIRECTOR_SCRIPT := preload("res://scripts/chapter_two_director.gd")
const TABLE_SCRIPT := preload("res://scripts/chapter_two_party_table_2d.gd")
const SINGLE_BERRY_PATH := "res://assets/chapter2/birthday/sky_lagoon_strawberry_single.png"
const CLUSTER_BERRY_PATH := "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png"

var failures := 0
var main: ReefMain
var world: OperaCareerWorld2D
var cake_result_win_count := 0


func _init() -> void:
	main = MAIN_SCENE.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	main.chapter2_active = true
	main.chapter2_active_objective = ChapterTwoDirector.OBJECTIVE_PARTY_PREP
	main.chapter2_unlocked_opera_mask = ChapterTwoDirector.FIRST_WAVE_UNLOCK_MASK
	main.chapter2_party_piece_mask = 0
	main.chapter2_cake_piece_mask = 0
	main.chapter2_job_phase_masks = [0, 0, 0, 0, 0, 0, 0, 0]
	var competition := OperaCompetition.new() as OperaCompetition
	competition.configure("farmer")
	var farmer_set := ADAPTER_SCRIPT.phase_set("farmer")
	world = WORLD_SCRIPT.new() as OperaCareerWorld2D
	main.add_child(world)
	world.setup(main, {"costume": "farmer", "chapter": "chapter2",
		"phase_overrides": farmer_set.get("phases", []), "finale_start": 2},
		competition, Callable(), [], ADAPTER_SCRIPT.adapter_config("farmer"),
		{"chapter": "chapter2"})
	await process_frame
	_check("real Farmer scene builds five independent pickup buttons",
		world.chapter2_strawberry_pickups.size() == 5)
	var single_berry := world.chapter2_single_strawberry_texture as Texture2D
	_check("Farmer buttons use the approved single-berry resource",
		world.get_meta("chapter2_strawberry_pickup_texture", "")
			== SINGLE_BERRY_PATH
		and single_berry != null
		and (single_berry as AtlasTexture) == null
		and world.get_meta("chapter2_strawberry_cluster_asset", "")
			== CLUSTER_BERRY_PATH
		and world.chapter2_strawberry_pickups.all(
			func(pickup: TextureButton) -> bool:
				return pickup.texture_normal == single_berry))
	for saved_count in range(1, 5):
		_run_partial_resume_case(saved_count)
	world.queue_free()
	await process_frame
	await _run_final_cake_hold_case("chef", 0x0F, 0x1F,
		"chef_frosted_rainbow_cake")
	await _run_final_cake_hold_case("candymaker", 0x3F, 0x7F,
		"placed_final")
	main.chapter2_strawberry_mask = ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK
	var table := TABLE_SCRIPT.new() as ChapterTwoPartyTable2D
	main.add_child(table)
	table.setup(main)
	_check("Main Hall summary suppresses legacy corn, bag, crown and clue cards",
		table.prop_for_act(ChapterTwoDirector.ACT_CHEF) == null
		and table.prop_for_act(ChapterTwoDirector.ACT_DETECTIVE) == null
		and table.prop_for_act(ChapterTwoDirector.ACT_CANDY_MAKER) == null
		and table.prop_for_act(ChapterTwoDirector.ACT_FARMER) == null
		and bool(table.get_meta("chapter2_no_legacy_corn_bag_crown", false)))
	_check("Main Hall keeps one persistent cake authority and five berry tokens",
		table.giant_cake != null
		and table.get_meta("chapter2_single_cake_authority", "") == "giant_cake"
		and int(table.get_meta("chapter2_single_strawberry_token_count", 0)) == 5
		and bool(table.get_meta("chapter2_summary_icons_avoid_cake", false)))
	table.free()
	main.free()
	print("CHAPTER2_FARMER_RESUME|RESULT: ",
		"PASS" if failures == 0 else "FAIL",
		" failures=", failures)
	quit(1 if failures > 0 else 0)


func _run_partial_resume_case(saved_count: int) -> void:
	var saved_mask := (1 << saved_count) - 1
	main.chapter2_strawberry_mask = saved_mask
	world.phase_index = 0
	world.phase_progress = 0.0
	world.phase_advance_pending = false
	world.phase_complete_t = 0.0
	world.active = true
	world._arm_phase()
	world._open_task()
	var label := "resume %d/5" % saved_count
	_check("%s derives scene progress from saved mask" % label,
		is_equal_approx(world.phase_progress, float(saved_count)))
	var remaining_index := saved_count
	var remaining_button := world.chapter2_strawberry_pickups[remaining_index]
	_check("%s leaves only the next pickup enabled" % label,
		remaining_button.visible and not remaining_button.disabled
		and world.chapter2_strawberry_pickups[saved_count - 1].disabled)
	for pick_index in range(saved_count, 5):
		world.chapter2_strawberry_pickups[pick_index].emit_signal("pressed")
	_check("%s reaches exactly five through remaining real button presses" % label,
		main.chapter2_strawberry_mask == ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK
		and is_equal_approx(world.phase_progress, 5.0)
		and world.phase_advance_pending)
	remaining_button.emit_signal("pressed")
	_check("%s ignores duplicate press without double credit" % label,
		main.chapter2_strawberry_mask == ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK
		and is_equal_approx(world.phase_progress, 5.0))


func _run_final_cake_hold_case(career: String, initial_mask: int,
		expected_mask: int, expected_stage: String) -> void:
	var act_index := ChapterTwoDirector.ACT_CHEF \
		if career == "chef" else ChapterTwoDirector.ACT_CANDY_MAKER
	var prior_party_mask := 1 << ChapterTwoDirector.ACT_FARMER
	var phase_masks := [0x0F, 0x0F, 0, 0, 0, 0, 0, 0]
	if career == "candymaker":
		prior_party_mask |= 1 << ChapterTwoDirector.ACT_CHEF
		phase_masks[1] = 0x1F
		phase_masks[2] = 0x07
	var chapter_two: ChapterTwoDirector = main._chapter_two_ref()
	chapter_two.restore_state({
		"day_one_giant_dust_bunny_boss_defeated": true,
		"chapter2_party_piece_mask": prior_party_mask,
		"chapter2_strawberry_mask": ChapterTwoDirector.STRAWBERRY_REQUIRED_MASK,
		"chapter2_cake_piece_mask": initial_mask,
		"chapter2_job_phase_masks": phase_masks,
	})
	main.opera_active_act_index = act_index
	cake_result_win_count = 0
	var competition := OperaCompetition.new() as OperaCompetition
	competition.configure(career)
	var phase_set := ADAPTER_SCRIPT.phase_set(career)
	world = WORLD_SCRIPT.new() as OperaCareerWorld2D
	main.add_child(world)
	world.setup(main, {"costume": career, "chapter": "chapter2",
		"phase_overrides": phase_set.get("phases", []),
		"finale_start": int(phase_set.get("finale_start", 0))},
		competition, Callable(self, "_on_cake_result_win"), [],
		ADAPTER_SCRIPT.adapter_config(career), chapter_two._story_run_context())
	await process_frame
	var phase_callback: Variant = world.adapter_callbacks.get(
		"phase_completed", Callable())
	_check("%s owns a valid production-shaped phase callback" % career,
		phase_callback is Callable and (phase_callback as Callable).is_valid())
	if career == "candymaker":
		var candy_berry_texture := \
			world.chapter2_single_strawberry_texture as Texture2D
		_check("Candy Maker binds the approved single-strawberry art",
			candy_berry_texture != null and candy_berry_texture.resource_path \
				== "res://assets/chapter2/birthday/sky_lagoon_strawberry_single.png")
		var expected_actions: Array[String] = [
			"pitcher_stream_coats_five_berries",
			"five_berries_move_into_matching_lanes",
			"glaze_crank_shines_five_berries",
			"five_berries_move_from_tray_toward_cake",
		]
		var visible_mechanics_are_bound := true
		for candy_phase in range(expected_actions.size()):
			world.phase_index = candy_phase
			world._show_phase()
			world.phase_fill.value = 50.0
			world.action_panel.queue_redraw()
			await process_frame
			visible_mechanics_are_bound = visible_mechanics_are_bound \
				and world.action_panel.visible \
				and world.surface.visible \
				and world.surface.mouse_filter == Control.MOUSE_FILTER_STOP \
				and String(world.action_panel.get_meta(
					"chapter2_candy_visible_action", "")) \
					== expected_actions[candy_phase] \
				and int(world.action_panel.get_meta(
					"chapter2_candy_visible_berry_count", 0)) == 5 \
				and is_equal_approx(float(world.action_panel.get_meta(
					"chapter2_candy_visual_progress", 0.0)), 0.5)
		_check("Candy Maker renders four distinct input-causal berry actions",
			visible_mechanics_are_bound)
	world.phase_index = world.phases.size() - 1
	world.phase_advance_pending = true
	world._advance_completed_phase()
	_check("%s persists its final cake mask before closing" % career,
		main.chapter2_cake_piece_mask == expected_mask)
	_check("%s refreshes the committed cake picture before closing" % career,
		world.chapter2_cake_scene != null
		and world.chapter2_cake_scene.stage_id() == expected_stage)
	_check("%s starts a plot-owned result hold before closing" % career,
		world.chapter2_final_result_hold_pending
		and bool(world.get_meta("chapter2_final_result_hold_active", false))
		and cake_result_win_count == 0)
	world._process(1.0)
	_check("%s keeps the completed cake visible during the result hold" % career,
		world.chapter2_final_result_hold_pending
		and world.chapter2_cake_scene.visible
		and cake_result_win_count == 0)
	world._process(1.3)
	_check("%s closes only after the committed cake has held on screen" % career,
		not world.chapter2_final_result_hold_pending
		and cake_result_win_count == 1)
	world.queue_free()
	await process_frame


func _on_cake_result_win() -> void:
	cake_result_win_count += 1


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("CHAPTER2_FARMER_RESUME|", label, ": ", "OK" if ok else "FAIL")
