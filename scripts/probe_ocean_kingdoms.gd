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
	# She used to spawn at a fixed x -48; the promenade now has a walkable route
	# (owner request 2026-07-27) and she starts ON it, beside the pearl plane.
	# The invariant that matters is that: screen one, standing on the path, not
	# a magic coordinate that the route's projection legitimately moves.
	var promenade := main._lagoon_promenade_ref()
	var promenade_cfg: Dictionary = main.g.get("ss_cfg", {})
	var spawn_x: float = player.position.x - level2_pos.x
	var spawn_y: float = player.position.y - level2_pos.y
	var route_span: Vector2 = promenade.stage.route_span(promenade_cfg)
	_check(spawn_x < -24.0
		and spawn_x >= route_span.x - 0.01
		and absf(spawn_y - promenade.stage.route_y(promenade_cfg, spawn_x, -999.0)) < 0.05
		and absf(player.position.z - level2_pos.z) < 0.5,
		"promenade_screen_one_spawn")
	_check(String(state.get("phase", "")) == "promenade",
		"castle_gate_hub_uses_promenade")
	_check((state.get("lagoon_promenade_targets", []) as Array).size() == 8,
		"promenade_interactions_present")
	_check(not state.has("ocean_kingdom_gates"),
		"blocked_water_has_no_active_ocean_gate")

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

	# The SceneTree coroutine can resume before ReefMain's next _process tick.
	# Drive the patrol once explicitly so the assertion cannot mistake each
	# newly-built mover's Vector3.ZERO staging transform for a habitat result.
	main._tick_aquatic(0.0)
	var movers: Array = main.aquatic_movers
	for mover_variant: Variant in movers:
		var mover: Dictionary = mover_variant as Dictionary
		if not mover.has("kingdom"):
			continue
		var mover_node: Node3D = mover.get("node") as Node3D
		if mover_node == null:
			continue
		var mover_point := Vector2(mover_node.position.x, mover_node.position.z)
		var mover_center := Vector2(float(mover.get("cx", 0.0)), float(mover.get("cz", 0.0)))
		_check(absf(mover_point.distance_to(mover_center) - float(mover["rad"])) < 0.1,
			"hero_fauna_patrol_initialized_%s" % String(mover.get("kingdom", "")))
		_check(ReefDistricts.kingdom_at(mover_point) == String(mover.get("kingdom", "")), "hero_fauna_stays_%s" % String(mover.get("kingdom", "")))

	_finish()


func _finish() -> void:
	if failures == 0:
		print("RESULT|PASS")
		quit(0)
	else:
		print("RESULT|FAIL|%d" % failures)
		quit(1)
