extends SceneTree
## Isolated saved-state diagnostic of the production House/Act config path.
## Chapter state is injected. This is not a fresh-save visible room traversal.

const MAIN_SCENE := preload("res://scenes/main.tscn")

func _init() -> void:
	var main: ReefMain = MAIN_SCENE.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main.day_one_active = false
	main._skip_intro()
	main.chapter2_active = true
	main.chapter2_active_objective = ChapterTwoDirector.OBJECTIVE_PARTY_PREP
	main.chapter2_unlocked_opera_mask = ChapterTwoDirector.FIRST_WAVE_UNLOCK_MASK
	main.chapter2_party_piece_mask = 0
	main.chapter2_job_phase_masks = [0, 0, 0, 0, 0, 0, 0, 0]
	var director: ChapterTwoDirector = main._chapter_two_ref()
	var config: Dictionary = director.opera_config_overrides("", ChapterTwoDirector.ACT_FARMER)
	var supplied_phases: bool = "--supplied-phases" in OS.get_cmdline_user_args()
	if supplied_phases:
		config["phase_overrides"] = ChapterTwoCareerSceneAdapter.phase_set("farmer").get("phases", [])
	var house: OperaHouse = OperaHouse.new()
	main.add_child(house)
	var started: bool = house.start(main, ChapterTwoDirector.ACT_FARMER, Callable(), config)
	var world: OperaCareerWorld2D = house.act.career_world_2d if house.act != null else null
	var phase_count: int = world.phases.size() if world != null else 0
	var station_count: int = world.station_list.size() if world != null else 0
	var armed: int = world.armed_station if world != null else -1
	var has_surface: bool = world != null and world.surface != null
	print("FARMER_CONFIG_DIAGNOSTIC|", JSON.stringify({
		"director_allows_farmer": director.can_start_chapter2_act(ChapterTwoDirector.ACT_FARMER),
		"config_keys": config.keys(), "house_reports_started": started,
		"phase_count": phase_count, "station_count": station_count,
		"armed_station": armed, "has_surface": has_surface,
		"explicit_phases_supplied": supplied_phases,
		"fixture": "Injected post-boss chapter state; actual director/House/Act call chain; phase-supply mode declared separately."}))
	var healthy: bool = started and phase_count > 0 and station_count > 0 and armed >= 0 and has_surface
	print("FARMER_CONFIG_DIAGNOSTIC|Healthy first task: ", "OK" if healthy else "FAIL")
	quit(0 if healthy else 1)
