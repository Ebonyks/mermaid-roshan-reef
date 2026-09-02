extends SceneTree
## Regression guard: the rejected Mermaid Pool overlay must stay absent.
## The bathroom still unlocks the pool through DayOneDirector state only.

const DIRECTOR_SCRIPT: GDScript = preload("res://scripts/day_one_director.gd")

var checks_failed: int = 0


func _init() -> void:
	var rooms_source: String = FileAccess.get_file_as_string(
		"res://scripts/arena/castle_rooms_25d.gd")
	_check("no pool overlay runtime hook",
		not rooms_source.contains("CASTLE_POOL_SURFACE_LIFE")
		and not rooms_source.contains("_build_mermaid_pool_surface_life"))
	_check("rejected pool overlay resources are absent",
		not FileAccess.file_exists(
			"res://scripts/castle_pool_surface_life.gd")
		and not FileAccess.file_exists(
			"res://assets/shaders/castle_pool_surface_life.gdshader"))
	var main_source: String = FileAccess.get_file_as_string(
		"res://scripts/main.gd")
	var cleaning_source: String = FileAccess.get_file_as_string(
		"res://scripts/games/day_one_bathroom_cleaning.gd")
	var finale_start: int = main_source.find(
		"func _on_day_one_bathroom_finale_started()")
	var finale_end: int = main_source.find("\nfunc ", finale_start + 1)
	var finale_source: String = main_source.substr(finale_start,
		finale_end - finale_start) if finale_start >= 0 and finale_end > finale_start \
		else ""
	_check("bathroom finale owns distributed sparkle and pool picture handoff",
		cleaning_source.contains("SPARKLE_ANCHORS")
		and cleaning_source.contains("SPARKLE_ANCHOR_ROLES")
		and cleaning_source.contains("_spawn_whole_room_sparkles()")
		and cleaning_source.contains("fixture_associated_role")
		and not finale_source.contains("_burst(\"✦\"")
		and main_source.contains("ApprovedRoomPreview")
		and main_source.contains("approved_reused_room_imagery")
		and main_source.contains("actual_destination_room")
		and main_source.contains("_show_day_one_room_handoff"))
	_check("pool route preview is the approved actual room, not a droplet",
		main_source.contains("DAY_ONE_POOL_ROUTE_PREVIEW_TEXTURE")
		and main_source.contains(
			"res://assets/flats/castle/rooms/room_mermaid_pool.png")
		and not main_source.contains("sign_mermaid_pool.png"))

	var main: ReefMain = ReefMain.new()
	var director: DayOneDirector = DIRECTOR_SCRIPT.new(main) as DayOneDirector
	director.bathroom_supply_hunt_step = 2
	director.bathroom_tools_authorized = true
	director.bathroom_cleanup_step = 2
	_check("bathroom completion still unlocks the pool",
		director.current_room_id == "bathroom"
		and director.complete_tutorial("bathroom")
		and director.current_room_id == "pool"
		and director.can_enter_room("pool"))
	main.free()
	print("CASTLE_POOL_OVERLAY_ABSENCE|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		checks_failed += 1
	print("CASTLE_POOL_OVERLAY_ABSENCE|", label, ": ",
		"OK" if ok else "FAIL")
