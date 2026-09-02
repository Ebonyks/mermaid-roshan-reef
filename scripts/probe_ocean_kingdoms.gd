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
	# This probe owns the post-Day-One ocean-kingdom contract.  The production
	# gate correctly keeps ordinary reef exits pointed at the castle during Day
	# One, so make the later-content fixture explicit before entering the Lagoon.
	main.day_one_active = false
	main._day_one_ref().clear_day_one_routing()

	_check(main.START_AT_CASTLE_GATE, "display_build_starts_at_castle_gate")
	main._enter_level2_now(false, false, true)
	await process_frame

	var state: Dictionary = main.g
	var player: Node3D = main.player
	_check(main.game == "level2", "castle_gate_hub_is_level2")
	_check(bool(state.get("ocean_gate_hub", false)), "castle_gate_hub_flag")
	# She used to spawn at a fixed x -48; the promenade now has a walkable route
	# (owner request 2026-07-27) and she starts ON it, beside the pearl plane.
	# The invariant that matters is that: screen one, standing on the path, not
	# a magic coordinate that the route's projection legitimately moves.
	var promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
	var spawn_x: float = promenade.master_route_x()
	var spawn_y: float = float(state.get("lagoon_master_y", -1.0))
	var actor_screen: Vector2 = promenade.screen_from_master(Vector2(spawn_x, spawn_y))
	var viewport_rect := Rect2(Vector2.ZERO,
		root.get_viewport().get_visible_rect().size)
	_check(spawn_x >= 0.0 and spawn_x < 2048.0 and spawn_y >= 0.0
		and spawn_y <= 2048.0 and viewport_rect.has_point(actor_screen)
		and promenade.root() is CanvasLayer and promenade.camera_2d() is Camera2D
		and not player.visible,
		"promenade_screen_one_spawn")
	_check(String(state.get("phase", "")) == "promenade",
		"castle_gate_hub_uses_promenade")
	var promenade_targets: Array = state.get("lagoon_promenade_targets", [])
	var promenade_ids: Dictionary = {}
	for target_value in promenade_targets:
		var target: Dictionary = target_value as Dictionary
		promenade_ids[String(target.get("id", ""))] = true
	var promenade_roster_ok: bool = promenade_targets.size() == 5
	for required_id: String in ["reef_route", "slide", "swing", "seesaw", "castle_gate"]:
		promenade_roster_ok = promenade_roster_ok and promenade_ids.has(required_id)
	_check(promenade_roster_ok, "promenade_interactions_present")
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
	var caribbean_before_game: String = main.game
	var caribbean_cool: float = main.ocean_return_gate_cool
	var caribbean_bounced: bool = main._tick_ocean_return_gate(0.0, player.position)
	_check(caribbean_cool > 0.0 and not caribbean_bounced \
		and main.game == caribbean_before_game,
		"caribbean_return_gate_debounced")

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
	var norwegian_before_game: String = main.game
	var norwegian_cool: float = main.ocean_return_gate_cool
	var norwegian_bounced: bool = main._tick_ocean_return_gate(0.0, player.position)
	_check(norwegian_cool > 0.0 and not norwegian_bounced \
		and main.game == norwegian_before_game,
		"norway_return_gate_debounced")

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
