extends SceneTree
## Focused true-2D contract for the Moonflower -> Rainbow Stage handoff.

const Handoff := preload("res://scripts/arena/fairy_conservatory_handoff_2d.gd")
const TILE_ROOT := "res://assets/flats/fairy_conservatory_handoff/background/"
const TILE_PREFIX := "handoff_background_r"

var _failures := 0
var _results: Array[String] = []
var _handoff: FairyConservatoryHandoff2D = null
var _completed: Array[String] = []
var _host: Node = null


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	_host = Node.new()
	get_root().add_child(_host)
	_handoff = Handoff.new()
	_handoff.start(_host, _on_finished)
	var first := _handoff.audit_snapshot()
	_check("controller starts active", bool(first.get("active", false)))
	_check("starts on rainbow stage", String(first.get("state", "")) == "rainbow_stage")
	_check("eight background slots declared",
		int(first.get("background_tile_paths", []).size()) == 8)
	_check("canvas-only contract",
		not bool(first.get("uses_spatial_runtime", true)))
	_check("no fail state", bool(first.get("no_fail_state", false)))
	_check("no gameplay timer", not bool(first.get("has_timer", true)))
	_check("handoff adds no local Back and relies on the game-wide control",
		bool(first.get("uses_global_navigation", false)))
	_check("house is not entered by zero input",
		String(first.get("state", "")) != "butterfly_house")
	_check("house remains visible at far end",
		bool(first.get("butterfly_house_visible", false)))
	_check("rainbow remains visible through handoff",
		bool(first.get("rainbow_walkway_visible", false)))
	_check("route uses centered one-point perspective",
		bool(first.get("one_point_route_centered", false)))

	# Taps that do not target the next waypoint never advance the route.
	_handoff.probe_tap(Vector2(90.0, 180.0))
	var idle_tap := _handoff.audit_snapshot()
	_check("off-route tap keeps progress", int(idle_tap.get("waypoint_index", -1)) == 0)

	# Every accepted step immediately moves Roshan and the pointer to the next
	# one-point target; they must never remain stale until the final tap.
	_handoff.probe_tap(Vector2(640.0, 600.0))
	var first_step := _handoff.audit_snapshot()
	_check("first step advances immediately",
		int(first_step.get("waypoint_index", -1)) == 1)
	_check("Roshan moves toward the horizon after first step",
		Vector2(first_step.get("roshan_position", Vector2.ZERO)).y
		< Vector2(first.get("roshan_position", Vector2.ZERO)).y)
	_check("pointer moves to the next target after first step",
		Vector2(first_step.get("pointer_base", Vector2.ZERO)).y
		< Vector2(first.get("pointer_base", Vector2.ZERO)).y)
	# The remaining explicit one-finger taps expose the house.
	for point: Vector2 in [Vector2(640.0, 500.0), Vector2(640.0, 375.0)]:
		_handoff.probe_tap(point)
	var reached := _handoff.audit_snapshot()
	_check("walk reaches house only after taps",
		String(reached.get("state", "")) == "butterfly_house"
		and int(reached.get("waypoint_index", -1)) == 3)
	var hotspot_size := Vector2(reached.get("house_hotspot_size", Vector2.ZERO))
	_check("house hotspot meets minimum touch size",
		hotspot_size.x >= 112.0 and hotspot_size.y >= 112.0)
	_check("house and rainbow remain visible at arrival",
		bool(reached.get("butterfly_house_visible", false))
		and bool(reached.get("rainbow_walkway_visible", false)))
	_handoff.probe_tap(Vector2(640.0, 180.0))
	_check("house completion result is explicit",
		_completed.has("butterfly_house"))

	_handoff.teardown()
	var return_handoff := Handoff.new()
	return_handoff.start(_host, _on_finished, true)
	var returning := return_handoff.audit_snapshot()
	_check("returning entry begins the guided home walk",
		String(returning.get("state", "")) == "rainbow_return"
		and bool(returning.get("returning_from_butterfly", false)))
	_check("returning keeps both art layers visible",
		bool(returning.get("butterfly_house_visible", false))
		and bool(returning.get("rainbow_walkway_visible", false)))
	_check("return hides the Butterfly House entry hotspot",
		not bool(returning.get("house_hotspot_visible", true)))
	return_handoff.probe_tap(Vector2(640.0, 180.0))
	_check("return pointer cannot loop back into Butterfly World",
		_completed.count("butterfly_house") == 1
		and int(return_handoff.audit_snapshot().get("waypoint_index", -1)) == 3)
	for point: Vector2 in [Vector2(640.0, 375.0), Vector2(640.0, 500.0),
			Vector2(640.0, 600.0)]:
		return_handoff.probe_tap(point)
	_check("guided reverse walk completes home",
		_completed.count("back") == 1)
	return_handoff.teardown()
	_host.queue_free()

	print("HANDOFF2D|RESULT=", "FAIL" if _failures > 0 else "OK",
		" failures=", _failures)
	quit(_failures)


func _on_finished(result: String) -> void:
	_completed.append(result)


func _check(label: String, passed: bool) -> void:
	_results.append(label)
	if passed:
		print("HANDOFF2D|OK|", label)
	else:
		_failures += 1
		print("HANDOFF2D|FAIL|", label)
