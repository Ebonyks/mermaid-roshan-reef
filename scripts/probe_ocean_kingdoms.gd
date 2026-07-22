extends SceneTree

var failures: int = 0


func _initialize() -> void:
	call_deferred("_run")


func _check(condition: bool, label: String) -> void:
	if condition:
		print("OCEANKINGDOM|%s|OK" % label)
	else:
		failures += 1
		print("OCEANKINGDOM|%s|FAIL" % label)


func _xz_distance(a: Vector3, b: Vector2) -> float:
	return Vector2(a.x, a.z).distance_to(b)


func _run() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn") as PackedScene
	_check(packed != null, "main_scene_loads")
	if packed == null:
		_finish()
		return

	var main: ReefMain = packed.instantiate() as ReefMain
	_check(main != null, "main_is_reef_main")
	if main == null:
		_finish()
		return
	root.add_child(main)
	await process_frame
	await process_frame

	_check(main.START_AT_CASTLE_GATE, "display_build_starts_at_castle_gate")
	main._enter_level2_now(false, false, true)
	await process_frame

	var state: Dictionary = main.g
	var player: Node3D = main.player
	var level2_pos: Vector3 = main.LEVEL2_POS
	_check(main.game == "level2", "castle_gate_hub_is_level2")
	_check(bool(state.get("ocean_gate_hub", false)), "castle_gate_hub_flag")
	_check(player.position.distance_to(level2_pos + Vector3(0.0, 8.0, 175.0)) < 0.5, "castle_gate_spawn_position")

	var gates: Array = state.get("ocean_kingdom_gates", []) as Array
	_check(gates.size() == 2, "two_ocean_kingdom_gates")
	var seen_caribbean: bool = false
	var seen_norwegian: bool = false
	for gate_variant: Variant in gates:
		var gate: Dictionary = gate_variant as Dictionary
		var kingdom: String = String(gate.get("kingdom", ""))
		var gate_pos: Vector3 = gate.get("pos", Vector3.ZERO) as Vector3
		_check(player.position.distance_to(gate_pos) > 9.0, "%s_gate_not_auto_triggered" % kingdom)
		if kingdom == ReefDistricts.KINGDOM_CARIBBEAN:
			seen_caribbean = true
		elif kingdom == ReefDistricts.KINGDOM_NORWEGIAN:
			seen_norwegian = true
	_check(seen_caribbean, "caribbean_gate_present")
	_check(seen_norwegian, "norwegian_gate_present")

	main._exit_level2_now(ReefDistricts.KINGDOM_CARIBBEAN)
	await process_frame
	state = main.g
	player = main.player
	var caribbean_entry: Vector2 = ReefDistricts.kingdom_entry_point(ReefDistricts.KINGDOM_CARIBBEAN)
	_check(main.game == "", "caribbean_enters_open_ocean")
	_check(main.ocean_kingdom == ReefDistricts.KINGDOM_CARIBBEAN, "caribbean_runtime_state")
	_check(main.ocean_routes_enabled, "caribbean_enables_kingdom_routes")
	_check(_xz_distance(player.position, caribbean_entry) < 0.5, "caribbean_entry_position")
	_check(ReefDistricts.kingdom_at(caribbean_entry) == ReefDistricts.KINGDOM_CARIBBEAN, "caribbean_entry_ecology")
	_check(not main.ocean_return_gate_armed, "caribbean_return_gate_debounced")

	main._enter_level2_now(false, false, true)
	await process_frame
	main._exit_level2_now(ReefDistricts.KINGDOM_NORWEGIAN)
	await process_frame
	state = main.g
	player = main.player
	var norwegian_entry: Vector2 = ReefDistricts.kingdom_entry_point(ReefDistricts.KINGDOM_NORWEGIAN)
	_check(main.game == "", "norway_enters_open_ocean")
	_check(main.ocean_kingdom == ReefDistricts.KINGDOM_NORWEGIAN, "norway_runtime_state")
	_check(main.ocean_routes_enabled, "norway_enables_kingdom_routes")
	_check(_xz_distance(player.position, norwegian_entry) < 0.5, "norway_entry_position")
	_check(ReefDistricts.kingdom_at(norwegian_entry) == ReefDistricts.KINGDOM_NORWEGIAN, "norway_entry_ecology")
	_check(not main.ocean_return_gate_armed, "norway_return_gate_debounced")

	var movers: Array = main.aquatic_movers
	for mover_variant: Variant in movers:
		var mover: Dictionary = mover_variant as Dictionary
		if not mover.has("kingdom"):
			continue
		var mover_node: Node3D = mover.get("node") as Node3D
		if mover_node == null:
			continue
		var mover_point := Vector2(mover_node.position.x, mover_node.position.z)
		_check(ReefDistricts.kingdom_at(mover_point) == String(mover.get("kingdom", "")), "hero_fauna_stays_%s" % String(mover.get("kingdom", "")))

	_finish()


func _finish() -> void:
	if failures == 0:
		print("RESULT|PASS")
		quit(0)
	else:
		print("RESULT|FAIL|%d" % failures)
		quit(1)
