extends SceneTree
const Whole := preload("res://scripts/arena/sky_lagoon_whole_scene_cels.gd")
var failures: int = 0
func check(label: String, value: bool) -> void:
	print("WHOLESCENE|%s|%s" % [label, "PASS" if value else "FAIL"])
	if not value:
		failures += 1
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var parent := Node2D.new()
	root.add_child(parent)
	var image := Image.create(2, 2, false, Image.FORMAT_RGBA8)
	image.fill(Color.WHITE)
	var original := ImageTexture.create_from_image(image)
	for r: int in range(2):
		for c: int in range(6):
			var tile := Sprite2D.new()
			tile.name = "SkyLagoonBackdrop_r%d_c%d" % [r, c]
			tile.texture = original
			parent.add_child(tile)
	var state: Dictionary = {"saved_progress": 17}
	check("opt_in_only", not Whole.build(state, parent, false) and parent.get_child_count() == 12)
	check("complete_build", Whole.build(state, parent, true) and parent.get_child_count() == 66
		and (state.get("lagoon_cloud_bank_cards", []) as Array).size() == 8
		and (state.get("lagoon_grass_groups", []) as Array).size() == 18)
	var rosette: Sprite2D = parent.get_node_or_null("WholeScene_castle_foreground_rosette") as Sprite2D
	check("rosette_six_cels_foreground", rosette != null and rosette.hframes == 2 and rosette.vframes == 4 and rosette.z_index == 4 and int((rosette.get_meta("definition") as Dictionary)["frames"]) == 6)
	var meadow: Sprite2D = parent.get_node_or_null("WholeScene_meadow_boundary_berry_fan") as Sprite2D
	check("meadow_eight_cels_one_boundary_card", meadow != null and meadow.hframes == 2 and meadow.vframes == 4 and int((meadow.get_meta("definition") as Dictionary)["frames"]) == 8)
	var tuft: Sprite2D = parent.get_node_or_null("WholeScene_arrival_front_edge") as Sprite2D
	check("arrival_tuft_four_complete_cels", tuft != null and tuft.hframes == 2 and tuft.vframes == 2 and tuft.z_index == 4 and int((tuft.get_meta("definition") as Dictionary)["frames"]) == 4)
	var shaped_clouds: int = 0
	var independent_clocks: bool = true
	for value: Variant in state.get("lagoon_whole_cards", []):
		var cloud: Sprite2D = value as Sprite2D
		var definition: Dictionary = cloud.get_meta("definition") as Dictionary
		if definition["family"] != "cloud" or int(definition["frames"]) not in [3, 4]:
			continue
		shaped_clouds += 1
		var phase: float = float(cloud.get_meta("phase"))
		var pose_cycle: float = float(definition["pose_cycle"])
		state["lagoon_whole_t"] = phase + pose_cycle * 0.4
		Whole.tick(state, 0.0, false)
		var first_position: Vector2 = cloud.position
		independent_clocks = independent_clocks and cloud.frame == 1 and float(definition["cycle"]) == 48.0
		state["lagoon_whole_t"] = phase + pose_cycle * 1.4
		Whole.tick(state, 0.0, false)
		independent_clocks = independent_clocks and cloud.frame == 1 and cloud.position.distance_to(first_position) > 0.1
	check("twelve_clouds_shape_cycle_independent_of_48s_drift", shaped_clouds == 12 and independent_clocks)
	state["lagoon_whole_t"] = 0.0
	Whole.tick(state, 0.0, false)
	var seen: Dictionary = {}
	var bounds_ok: bool = true
	for step: int in range(2400):
		Whole.tick(state, 0.016, false)
		for value: Variant in state.get("lagoon_whole_cards", []):
			var card: Sprite2D = value as Sprite2D
			var row: Dictionary = card.get_meta("definition") as Dictionary
			if not seen.has(card.name):
				seen[card.name] = {}
			(seen[card.name] as Dictionary)[card.frame] = true
			bounds_ok = bounds_ok and card.frame >= 0 and card.frame < int(row["frames"]) and card.rotation == 0.0
	var all_frames: bool = true
	for value: Variant in state.get("lagoon_whole_cards", []):
		var card: Sprite2D = value as Sprite2D
		var row: Dictionary = card.get_meta("definition") as Dictionary
		var declared_moving: bool = bool(row.get("motion_enabled", true))
		var expected_frames: int = int(row["frames"]) if declared_moving else 1
		all_frames = all_frames and (seen[card.name] as Dictionary).size() == expected_frames
		if str(row["id"]) in ["arrival_lawn", "meadow_upper_left", "meadow_upper_right", "meadow_lower_lawn", "castle_left_verge", "castle_right_verge", "arrival_bank_left", "arrival_bank_right", "meadow_hedge_left", "meadow_hedge_right", "castle_approach_bank", "castle_far_bank"]:
			check("rejected_deformations_rest_only_" + str(row["id"]), not declared_moving and card.frame == 0)
		else:
			check("complete_owner_remains_animated_" + str(row["id"]), declared_moving)
	check("2400_ticks_enabled_frames_and_static_fragment_rests", bounds_ok and all_frames)
	var time_before: float = float(state["lagoon_whole_t"])
	for step: int in range(600):
		Whole.tick(state, 0.016, true)
	check("pause_freezes_clock", state["lagoon_whole_t"] == time_before)
	state["lagoon_plants_motion_enabled"] = false
	Whole.tick(state, 0.1, false)
	check("tuft_plant_toggle_rest", tuft != null and tuft.frame == 0)
	check("rosette_plant_toggle_rest", rosette != null and rosette.frame == 0)
	check("meadow_plant_toggle_rest", meadow != null and meadow.frame == 0)
	state["lagoon_plants_motion_enabled"] = true
	time_before = float(state["lagoon_whole_t"])
	state["lagoon_environment_motion_enabled"] = false
	Whole.tick(state, 0.1, false)
	var at_rest: bool = true
	for value: Variant in state["lagoon_whole_cards"]:
		var card: Sprite2D = value as Sprite2D
		var row: Dictionary = card.get_meta("definition") as Dictionary
		at_rest = at_rest and card.frame == 0 and card.position == Vector2(float(row["position"][0]), float(row["position"][1]))
	check("static_returns_all_cards_to_rest", at_rest and state["lagoon_whole_t"] == time_before)
	Whole.clear(state)
	var restored: bool = parent.get_child_count() == 12
	for tile: Node in parent.get_children():
		restored = restored and (tile as Sprite2D).texture == original
	check("rollback_restores_original_texture_objects", restored)
	var document: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(Whole.PATH)) as Dictionary
	var bad_cases: Array = []
	var bad: Dictionary = document.duplicate(true)
	bad["cards"][25]["file"] = "missing.png"
	bad_cases.append(bad)
	bad = document.duplicate(true)
	bad["cards"][25]["family"] = "unknown"
	bad_cases.append(bad)
	bad = document.duplicate(true)
	bad["cards"][25]["position"] = ["bad", 0]
	bad_cases.append(bad)
	bad = document.duplicate(true)
	bad["cards"][25]["rows"] = 0
	bad_cases.append(bad)
	bad = document.duplicate(true)
	bad["tiles"][11]["node"] = "../foreign"
	bad_cases.append(bad)
	bad = document.duplicate(true)
	bad["cards"][26]["file"] = "missing-rosette.png"
	bad_cases.append(bad)
	bad = document.duplicate(true)
	bad["cards"][27]["file"] = "missing-meadow.png"
	bad_cases.append(bad)
	for invalid: Variant in [0.0, -1.0, "bad"]:
		bad = document.duplicate(true)
		for entry: Dictionary in bad["cards"]:
			if entry["id"] == "arrival_high_left":
				entry["pose_cycle"] = invalid
		bad_cases.append(bad)
	for invalid: Variant in [1, "false", null]:
		bad = document.duplicate(true)
		bad["cards"][0]["motion_enabled"] = invalid
		bad_cases.append(bad)
	var atomic: bool = true
	for value: Variant in bad_cases:
		var file := FileAccess.open("user://sky-whole-fault.json", FileAccess.WRITE)
		file.store_string(JSON.stringify(value))
		file.close()
		atomic = atomic and not Whole.build(state, parent, true, "user://sky-whole-fault.json") and parent.get_child_count() == 12
		for tile: Node in parent.get_children():
			atomic = atomic and (tile as Sprite2D).texture == original
	DirAccess.remove_absolute(ProjectSettings.globalize_path("user://sky-whole-fault.json"))
	check("thirteen_fault_cases_including_bad_motion_flags_no_partial_scene_mutation", atomic)
	var rebuilds: bool = true
	for cycle: int in range(40):
		rebuilds = rebuilds and Whole.build(state, parent, true)
		Whole.tick(state, 0.1, false)
		Whole.clear(state)
		rebuilds = rebuilds and parent.get_child_count() == 12
	check("40_rebuilds_no_orphan_cards_or_save_mutation", rebuilds and state["saved_progress"] == 17)
	Whole.build(state, parent, true)
	state["lagoon_environment_motion_enabled"] = true
	state["lagoon_plants_motion_enabled"] = true
	var cloud_cards: Array = state["lagoon_cloud_bank_cards"] as Array
	var grass_cards: Array = state["lagoon_grass_groups"] as Array
	(cloud_cards[0] as Sprite2D).free()
	(grass_cards[0] as Sprite2D).free()
	for step: int in range(20):
		Whole.tick(state, 0.1, false)
	check("surviving_cloud_and_grass_update_after_sibling_free",
		(cloud_cards[1] as Sprite2D).region_rect.position.x == 1026.0
		and (grass_cards[1] as Sprite2D).frame == 1)
	parent.free()
	Whole.tick(state, 0.1, false)
	Whole.clear(state)
	check("freed_parent_teardown", not state.has("lagoon_whole_cards"))
	quit(0 if failures == 0 else 1)
