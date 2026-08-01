extends SceneTree
# Trusted structural/agency/stress probe for the complete living-world pass.
# The catalog is audited against an independent stage contract, then every
# stage is entered through the real director with idle input withheld.

var failed := false
var main: ReefMain
var director: LivingWorldDirector


func _check(label: String, ok: bool, detail: String = "") -> void:
	print("LIVING|%s: %s%s" % [
		label,
		"OK" if ok else "FAIL",
		"" if detail == "" else " " + detail,
	])
	if not ok:
		failed = true


func _frames(count: int) -> void:
	for _i in range(count):
		await process_frame


func _init() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	main = packed.instantiate()
	get_root().add_child(main)
	await _frames(2)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(2)
	director = main._living_world_ref()
	director.setup()
	_probe_inventory()
	_probe_all_stage_runtime()
	_probe_real_input_reset()
	_probe_long_idle_bounds()
	_probe_exit_cleanup()
	print("LIVING|result: ", "FAIL" if failed else "ALL OK")
	quit(1 if failed else 0)


func _probe_inventory() -> void:
	var specs: Dictionary = main.living_specs
	var expected_ids: Array[String] = _expected_stage_ids()
	var actual_ids: Array[String] = []
	for key: Variant in specs.keys():
		actual_ids.append(String(key))
	actual_ids.sort()
	expected_ids.sort()
	_check("complete_stage_count",
		specs.size() == LivingWorldCatalog.EXPECTED_STAGE_COUNT
		and specs.size() == expected_ids.size(),
		"catalog=%d expected=%d" % [specs.size(), expected_ids.size()])
	_check("exact_stage_inventory", actual_ids == expected_ids)
	var expected_groups := {
		"entry": 1,
		"reef": 6,
		"sky_promenade": 3,
		"sky_legacy": 8,
		"north": 7,
		"castle": 21,
		"overlay": 6,
		"minigame": 12,
		"picture_game": 4,
		"dance": 1,
		"kart": 2,
		"galaxy": 2,
		"combat": 2,
		"stuffie": 1,
		"ember": 1,
		"ice_dungeon": 10,
		"ember_dungeon": 6,
		"opera_lobby": 3,
		"opera_act": 16,
	}
	var actual_groups: Dictionary = {}
	var ambient_ids: Dictionary = {}
	var idle_ids: Dictionary = {}
	var contracts_ok := true
	for stage_id: String in actual_ids:
		var spec: Dictionary = specs[stage_id]
		var group: String = String(spec.get("group", ""))
		actual_groups[group] = int(actual_groups.get(group, 0)) + 1
		var animations: Array = spec.get("animations", [])
		var idle: Dictionary = spec.get("idle_event", {})
		contracts_ok = contracts_ok \
			and String(spec.get("id", "")) == stage_id \
			and String(spec.get("name", "")) != "" \
			and String(spec.get("source", "")) != "" \
			and animations.size() == 2 \
			and not idle.is_empty()
		for animation_value: Variant in animations:
			var animation: Dictionary = animation_value as Dictionary
			var animation_id: String = String(animation.get("id", ""))
			contracts_ok = contracts_ok \
				and animation_id != "" \
				and not ambient_ids.has(animation_id) \
				and String(animation.get("description", "")) != "" \
				and String(animation.get("motif", "")) != ""
			ambient_ids[animation_id] = true
		var idle_id: String = String(idle.get("id", ""))
		contracts_ok = contracts_ok \
			and idle_id != "" \
			and not idle_ids.has(idle_id) \
			and not ambient_ids.has(idle_id) \
			and String(idle.get("description", "")) != "" \
			and String(idle.get("motif", "")) != "" \
			and float(idle.get("delay", 0.0)) >= 15.0 \
			and float(idle.get("delay", 99.0)) <= 24.0 \
			and float(idle.get("duration", 0.0)) >= 2.0 \
			and float(idle.get("duration", 99.0)) <= 4.0 \
			and float(idle.get("cooldown", 0.0)) >= 28.0 \
			and float(idle.get("cooldown", 99.0)) <= 45.0
		idle_ids[idle_id] = true
	_check("stage_group_coverage", actual_groups == expected_groups,
		JSON.stringify(actual_groups))
	_check("two_ambient_plus_one_idle_contract", contracts_ok,
		"ambient=%d idle=%d" % [ambient_ids.size(), idle_ids.size()])
	_check("dynamic_builder_tables_covered",
		ReefDistricts.REGION_CENTERS.size() == 6
		and DungeonLevel.ROOMS.size() == 10
		and EmberFortressLevel.ROOMS.size() == 6
		and OperaHouse.ACTS.size() == 16)


func _probe_all_stage_runtime() -> void:
	var specs: Dictionary = main.living_specs
	var before_progress: Dictionary = _progress_snapshot()
	var baseline_tweens: int = get_processed_tweens().size()
	var event_start: int = main.living_event_count
	var all_events_played := true
	for pass_index in range(3):
		for stage_value: Variant in specs.keys():
			var stage_id := String(stage_value)
			director.set_probe_stage(stage_id)
			var counts: Dictionary = director.runtime_counts()
			all_events_played = all_events_played \
				and main.living_stage_id == stage_id \
				and int(counts["layers"]) == 1 \
				and int(counts["canvases"]) == 1 \
				and int(counts["timers"]) == 0 \
				and int(counts["tweens"]) == 0 \
				and int(counts["particles"]) == 0
			if pass_index == 0:
				director.force_idle_event_for_probe()
				director.tick(0.01)
				all_events_played = all_events_played and main.living_event_time >= 0.0
				var spec: Dictionary = specs[stage_id]
				var idle: Dictionary = spec["idle_event"]
				director.tick(float(idle["duration"]) + 0.02)
				all_events_played = all_events_played and main.living_event_time < 0.0
	var event_delta: int = main.living_event_count - event_start
	_check("every_stage_enters_and_idles",
		all_events_played and event_delta == specs.size(),
		"events=%d expected=%d generations=%d" % [
			event_delta, specs.size(), main.living_generation])
	_check("passive_idle_never_awards_progress",
		_progress_unchanged(before_progress))
	_check("reentry_node_and_tween_bounds",
		director.runtime_counts() == {
			"layers": 1,
			"canvases": 1,
			"timers": 0,
			"tweens": 0,
			"particles": 0,
		}
		and get_processed_tweens().size() == baseline_tweens,
		"tweens=%d baseline=%d" % [
			get_processed_tweens().size(), baseline_tweens])


func _probe_real_input_reset() -> void:
	director.set_probe_stage("reef.pearl_plaza")
	var screen_touch := InputEventScreenTouch.new()
	screen_touch.index = 0
	screen_touch.position = Vector2(320.0, 240.0)
	screen_touch.pressed = true
	_prime_idle_event()
	main._input(screen_touch)
	var touch_ok: bool = _idle_is_reset()

	var keyboard := InputEventKey.new()
	keyboard.physical_keycode = KEY_W
	keyboard.pressed = true
	_prime_idle_event()
	main._input(keyboard)
	var keyboard_ok: bool = _idle_is_reset()

	var controller := InputEventJoypadMotion.new()
	controller.axis = JOY_AXIS_LEFT_X
	controller.axis_value = 0.8
	_prime_idle_event()
	main._input(controller)
	var controller_ok: bool = _idle_is_reset()
	main.joy_ev_axis.clear()

	_prime_idle_event()
	main.touch_ui.stick_vec = Vector2.RIGHT
	director.tick(0.25)
	var virtual_stick_ok: bool = _idle_is_reset()
	main.touch_ui.stick_vec = Vector2.ZERO

	_prime_idle_event()
	main._on_touch_manual_move()
	var interaction_ok: bool = _idle_is_reset()

	var joy_button := InputEventJoypadButton.new()
	joy_button.button_index = JOY_BUTTON_A
	joy_button.pressed = true
	_prime_idle_event()
	main._input(joy_button)
	var button_ok: bool = _idle_is_reset()

	_check("real_input_resets_idle",
		touch_ok and keyboard_ok and controller_ok and virtual_stick_ok
		and interaction_ok and button_ok,
		"touch=%s key=%s axis=%s stick=%s interaction=%s button=%s" % [
			touch_ok, keyboard_ok, controller_ok, virtual_stick_ok,
			interaction_ok, button_ok])


func _probe_long_idle_bounds() -> void:
	director.set_probe_stage("north.magic_forest")
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	var before_progress: Dictionary = _progress_snapshot()
	var before_events: int = main.living_event_count
	var baseline_tweens: int = get_processed_tweens().size()
	for _step in range(480):
		director.tick(0.5)
	var events: int = main.living_event_count - before_events
	var counts: Dictionary = director.runtime_counts()
	_check("long_idle_bounded_repeats",
		events >= 2 and events <= 8
		and int(counts["layers"]) == 1
		and int(counts["canvases"]) == 1
		and get_processed_tweens().size() == baseline_tweens,
		"events=%d counts=%s" % [events, JSON.stringify(counts)])
	_check("long_idle_stays_passive", _progress_unchanged(before_progress))


func _probe_exit_cleanup() -> void:
	director.set_probe_stage("opera.act.14")
	director.force_idle_event_for_probe()
	director.tick(0.01)
	director.clear_probe_stage()
	var canvas_cleared: bool = main.living_canvas != null \
		and main.living_canvas.stage_spec.is_empty() \
		and main.living_canvas.event_progress < 0.0
	var layer_hidden: bool = main.living_layer != null and not main.living_layer.visible
	_check("stage_exit_cleanup",
		main.living_stage_id == ""
		and main.living_probe_stage_override == ""
		and main.living_event_time < 0.0
		and is_zero_approx(main.living_idle_time)
		and canvas_cleared and layer_hidden)
	for _i in range(40):
		director.setup()
	var counts: Dictionary = director.runtime_counts()
	_check("setup_idempotent",
		int(counts["layers"]) == 1 and int(counts["canvases"]) == 1)


func _prime_idle_event() -> void:
	main.living_idle_time = 9.0
	main.living_event_time = 1.0
	main.living_cooldown = 0.0


func _idle_is_reset() -> bool:
	return is_zero_approx(main.living_idle_time) and main.living_event_time < 0.0


func _progress_snapshot() -> Dictionary:
	return {
		"pearls": main.pearl_count,
		"pearls_ever": main.pearls_ever,
		"trophies": main.trophies,
		"medals": main.medals.duplicate(true),
		"stickers": main.stickers.duplicate(true),
		"critter_collection": main.critter_collection.duplicate(true),
		"shop_owned": main.shop_owned.duplicate(true),
		"animals_owned": main.animals_owned.duplicate(true),
		"care_points": main.care_points,
		"dungeon_progress": main.dungeon_progress,
		"dungeon_done": main.dungeon_done,
		"ember_progress": main.ember_progress,
		"ember_done": main.ember_done,
		"opera_progress": main.opera_progress,
		"opera_stars": main.opera_stars,
		"opera_done": main.opera_done,
		"bwd_done": main.bwd_done,
	}


func _progress_unchanged(before: Dictionary) -> bool:
	return _progress_snapshot() == before


func _expected_stage_ids() -> Array[String]:
	var ids: Array[String] = [
		"intro.storybook",
		"reef.pearl_plaza", "reef.kelp_gardens", "reef.wreck_canyon",
		"reef.moon_pool", "reef.rainbow_bazaar", "reef.ice_shelf",
		"sky.promenade_runway", "sky.promenade_playground", "sky.promenade_castle",
		"sky.gatehouse", "sky.courtyard", "sky.playground", "sky.fairy_pond",
		"sky.castle_exterior", "sky.rainbow_junction", "sky.alpine_village",
		"sky.alpine_mountain",
		"north.mountain_pass", "north.magic_forest", "north.spirit_clearing_a",
		"north.spirit_clearing_b", "north.riverside_town",
		"north.ice_castle_exterior", "north.grand_hall",
		"castle.grand_hall", "castle.music_room", "castle.royal_bedroom",
		"castle.upper_star_chamber", "castle.upper_cloud_lounge",
		"castle.upper_library", "castle.upper_toy_gallery", "castle.upper_gallery",
		"castle.dreaming_corridor", "castle.dream_huluu", "castle.dream_daddy",
		"castle.dream_mama_baby", "castle.dream_kareem", "castle.dream_evie",
		"castle.undercroft", "castle.basement_corridor", "castle.pantry",
		"castle.kitchen", "castle.bubble_bath", "castle.craft_room",
		"castle.royal_loo",
		"overlay.craft_studio", "overlay.wardrobe", "overlay.sticker_book",
		"overlay.critter_book", "overlay.companion_picker",
		"overlay.companion_care",
		"minigame.fetch", "minigame.dolls", "minigame.brawl", "minigame.seek",
		"minigame.race_sunset", "minigame.shop", "minigame.treasure",
		"minigame.melody", "minigame.slide_ice", "minigame.slide_rainbow",
		"minigame.fairy_flight", "minigame.fairy_boss",
		"picture.snowman", "picture.garden", "picture.trampoline", "picture.xmas",
		"dance.rhythm_stage",
		"kart.ocean_circuit", "kart.rainbow_road",
		"galaxy.butterfly_garden", "galaxy.star_hall",
		"combat.ice_berry", "combat.pepper",
		"stuffie.sparring_den", "ember.fortress_planet",
		"opera.lobby_floor_1", "opera.lobby_floor_2", "opera.lobby_floor_3",
	]
	for index in range(10):
		ids.append("dungeon.ice.%02d" % index)
	for index in range(6):
		ids.append("dungeon.ember.%02d" % index)
	for index in range(16):
		ids.append("opera.act.%02d" % index)
	return ids
