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
	if main.intro_active:
		main._skip_intro()
	# This probe owns the post-Day-One retired-world contract.  The production
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
	var promenade_roster_ok: bool = promenade_targets.size() == 4 and not promenade_ids.has("reef_route")
	for required_id: String in ["slide", "swing", "seesaw", "castle_gate"]:
		promenade_roster_ok = promenade_roster_ok and promenade_ids.has(required_id)
	_check(promenade_roster_ok, "promenade_interactions_present")
	_check(not state.has("ocean_kingdom_gates"),
		"blocked_water_has_no_active_ocean_gate")

	var saved_pearls: int = main.pearl_count
	var saved_stickers: Dictionary = main.stickers.duplicate(true)
	for kingdom: String in [ReefDistricts.KINGDOM_CARIBBEAN,
			ReefDistricts.KINGDOM_NORWEGIAN, "", "unknown"]:
		main._exit_level2_now(kingdom)
		await process_frame
		_check(main.game == "level2" and String(main.g.get("phase", "")) == "promenade"
			and not main.player.visible and not main.ocean_routes_enabled,
			"retired_entry_stays_on_canvas_%s" % kingdom)
	_check(main.pearl_count == saved_pearls and main.stickers == saved_stickers,
		"retired_entries_preserve_progress")
	main._prepare_start_menu_launch(false)
	main.game = "" # A stale activity return must not restore free swimming.
	main._process(0.0)
	_check(main.game == "level2" and not main.player.visible,
		"authored_session_recovers_stale_empty_world")
	main._navigation_ref().press()
	_check(main.pause_panel.visible and main.game == "level2",
		"root_back_opens_menu_without_ocean")
	main._pause_ref().toggle_pause()
	for kingdom: String in [ReefDistricts.KINGDOM_CARIBBEAN, ReefDistricts.KINGDOM_NORWEGIAN]:
		main._enter_ocean_kingdom(kingdom)
		_check(main.game == "level2" and not main.player.visible,
			"public_ocean_callback_stays_on_canvas_%s" % kingdom)
	main._exit_level2()
	_check(main.game == "level2" and not main.player.visible,
		"legacy_back_callback_stays_on_canvas")
	main._do_finish_level2()
	_check(main.level2_done_once and main.game == "level2" and not main.player.visible,
		"castle_completion_preserves_canvas_and_reward")

	_finish()


func _finish() -> void:
	if failures == 0:
		print("RESULT|PASS")
		quit(0)
	else:
		print("RESULT|FAIL|%d" % failures)
		quit(1)
