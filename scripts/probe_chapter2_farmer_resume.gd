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
	world.queue_free()
	await process_frame
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


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("CHAPTER2_FARMER_RESUME|", label, ": ", "OK" if ok else "FAIL")
