extends SceneTree
var main: ReefMain
var failures: int = 0

func check(label: String, okay: bool) -> void:
	print("SKYFALLBACK|%s|%s" % [label, "OK" if okay else "FAIL"])
	if not okay:
		failures += 1

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	root.size = Vector2i(1280, 720)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	for index: int in range(4):
		await process_frame
	if main.intro_active:
		main._skip_intro()
	main.day_one_active = false
	main._day_one_ref().clear_day_one_routing()
	main.save_data["lagoon_plane_departed"] = true
	main.g["lagoon_art_version"] = "animated_v1"
	main._enter_level2_now(true, false, false)
	main.set_process(false)
	var promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
	var save_before: String = JSON.stringify(main.save_data)
	var temporary: String = "user://invalid_stage_pack.json"
	var file: FileAccess = FileAccess.open(temporary, FileAccess.WRITE)
	file.store_string("{broken")
	file.close()
	for manifest_path: String in ["user://missing_stage_pack.json", temporary]:
		promenade.build(true, false, false, manifest_path)
		var base: Node2D = main.g.get("lagoon_base_layer") as Node2D
		var tile: Sprite2D = base.get_node("SkyLagoonBackdrop_r0_c0") as Sprite2D
		var castle: Sprite2D = main.g.get("lagoon_castle_card") as Sprite2D
		check("original_art_and_route_" + manifest_path.get_file(), String(main.g.get("lagoon_art_version_active", "")) == "original" and promenade._route_points() == promenade.ROUTE_MASTER and tile.texture.resource_path.ends_with("flat_sky_lagoon_main_panorama_v5_tile_r0_c0.png") and castle.texture.resource_path.ends_with("sky_lagoon_castle_four_tower_v4.png"))
		var no_partial: bool = true
		for key: String in ["lagoon_bough_card", "lagoon_environment_cels", "lagoon_plant_cels", "lagoon_huckleberry_cels", "lagoon_water_slots", "lagoon_water_highlights", "lagoon_shoreline_cels", "lagoon_bridge_patch", "lagoon_candidate_resources"]:
			no_partial = no_partial and not main.g.has(key)
		check("no_partial_candidate_" + manifest_path.get_file(), no_partial and main.g.has("lagoon_candidate_rejection"))
		promenade.build(true, false, false)
		check("healthy_pack_recovers_" + manifest_path.get_file(), String(main.g.get("lagoon_art_version_active", "")) == "animated_v1" and promenade._route_points() == promenade.ANIMATED_ROUTE_MASTER and main.g.has("lagoon_bough_card") and main.g.has("lagoon_bridge_patch") and main.g.has("lagoon_water_slots") and not main.g.has("lagoon_candidate_rejection"))
	DirAccess.remove_absolute(ProjectSettings.globalize_path(temporary))
	check("save_progress_unchanged", JSON.stringify(main.save_data) == save_before)
	print("SKYFALLBACK|RESULT|%s" % ("ALL OK" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)
