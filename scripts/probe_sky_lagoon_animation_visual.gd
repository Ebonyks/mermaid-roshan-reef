extends "res://scripts/probe_l2_living_cards.gd"
# Display-mode fixture: the legacy headless probe does not dismiss the start menu.
# Exercise the normal dismissal + launch sequence before running its same checks.
func _frames(count: int) -> void:
	await super._frames(count)
	if main != null and main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
		await process_frame
		await process_frame

func _capture(name: String) -> void:
	_check("capture_has_no_start_menu_%s" % name, not main.start_menu_active and main.start_menu_layer == null)
	_check("capture_has_live_stage_%s" % name, promenade.root() != null and promenade.canvas_root().is_visible_in_tree())
	await super._capture(name)
	if name == "canvas_screen_1_day":
		var bough: Sprite2D = main.g.get("lagoon_bough_card") as Sprite2D
		_check("arrival_bough_imported_and_source_anchored", bough != null and bough.texture.resource_path == promenade.BoughCels.ATLAS and bough.position == Vector2(0, 448) and bough.get_rect().size == Vector2(512, 256))
		if bough != null:
			var was_processing: bool = main.is_processing()
			var saved_frame: int = bough.frame
			main.set_process(false)
			for sample: int in range(3):
				bough.frame = sample
				await super._capture("arrival_bough_%d" % sample)
			bough.frame = saved_frame
			main.set_process(was_processing)
	if name == "canvas_screen_3_day":
		for value: Variant in main.g.get("lagoon_ambient_cards", []) as Array:
			var ambient: Sprite2D = value as Sprite2D
			if String(ambient.get_meta("ambient_kind", "")) == "foreground_tree":
				_check("conifer_uses_six_fixed_base_cels", ambient.hframes == 3 and ambient.vframes == 2 and ambient.get_rect().size == Vector2(256, 384) and ambient.rotation == 0.0)
				var planted_position: Vector2 = ambient.position
				var frames_seen: Dictionary = {}
				var saved_clock: float = float(main.g.get("lagoon_ambient_t", 0.0))
				for sample: int in range(150):
					promenade._tick_ambient_life(0.016)
					frames_seen[ambient.frame] = true
				_check("conifer_all_six_frames_and_fixed_base", frames_seen.size() == 6 and ambient.position == planted_position and ambient.rotation == 0.0)
				var pause_clock: float = float(main.g["lagoon_ambient_t"])
				paused = true
				promenade._tick_ambient_life(50.0)
				paused = false
				_check("ambient_pause_freezes", float(main.g["lagoon_ambient_t"]) == pause_clock)
				main.g["lagoon_environment_motion_enabled"] = false
				promenade._tick_ambient_life(50.0)
				_check("ambient_static_freezes_and_tree_rests", float(main.g["lagoon_ambient_t"]) == pause_clock and ambient.frame == 0)
				main.g["lagoon_environment_motion_enabled"] = true
				main.g["lagoon_ambient_t"] = saved_clock
				promenade._tick_ambient_life(0.0)
		var shimmer_cards: Array = main.g.get("lagoon_water_highlights", []) as Array
		_check("two_painted_water_clips", shimmer_cards.size() == 2)
		for sample: int in range(3):
			for step: int in range(6):
				promenade.WaterHighlights.tick(main.g, 0.1, false)
			await super._capture("water_shimmer_%d" % sample)
		var water_point := Vector2(5600, 1400)
		_check("water_visible_pool_accepts_tap", promenade.WaterCels.tap(main.g, water_point))
		for index: int in range(3):
			promenade.WaterCels.tick(main.g, 0.1, false)
		await super._capture("water_ripple_day")
		_check("water_path_rejects", not promenade.WaterCels.tap(main.g, Vector2(4520, 1668)))
		var patch: Sprite2D = main.g.get("lagoon_bridge_patch") as Sprite2D
		var rail: Sprite2D = main.g.get("lagoon_bridge_rail") as Sprite2D
		var actor_holder: Node2D = main.g.get("lagoon_actor_layer") as Node2D
		_check("bridge_near_rail_in_front_of_actor", rail != null and (rail.get_parent() as Node2D).z_index > actor_holder.z_index)
		_check("bridge_patch_loaded", patch != null and patch.get_rect().size == Vector2(256, 192))
		promenade.set_master_route_x(4875.0)
		main.g["lagoon_walk_goal_master"] = Vector2(5010, 1442)
		for step: int in range(14):
			promenade._tick_movement(0.016)
		main.g["lagoon_walk_goal_master"] = null
		_check("bridge_contact_requires_route_crossing", int(main.g.get("lagoon_bridge_play_count", 0)) > 0)
		_check("bridge_contact_samples_motion_cel", patch != null and patch.frame > 0 and patch.frame < 12)
		await super._capture("bridge_contact_day")


func _prime_idle_event(director: LivingWorldDirector) -> void:
	# GPU mode deliberately cannot use the headless-only force helper.
	# Advance the ordinary idle clock in bounded steps without mutating state.
	var spec: Dictionary = main.living_specs[main.living_stage_id]
	var idle: Dictionary = spec["idle_event"]
	var steps: int = ceili(float(idle["delay"]) / 0.1) + 2
	for _step: int in range(steps):
		director.tick(0.1)
		if main.living_event_time >= 0.0:
			break
