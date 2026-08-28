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

	var main: ReefMain = ReefMain.new()
	var director: DayOneDirector = DIRECTOR_SCRIPT.new(main) as DayOneDirector
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
