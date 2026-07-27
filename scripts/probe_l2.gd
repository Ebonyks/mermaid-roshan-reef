extends SceneTree
# Structural and interaction probe for the three-screen 2.5D Sky Lagoon.

var failed := false

func _check(label: String, ok: bool, detail: String = "") -> void:
	print("LAGOON25D|%s: %s%s" % [
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
	var main: ReefMain = packed.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for friend_value in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main._enter_level2()
	await _frames(8)

	_check("promenade_phase",
		main.game == "level2" and String(main.g.get("phase", "")) == "promenade")
	var cfg: Dictionary = main.g.get("ss_cfg", {})
	_check("three_screen_width",
		is_equal_approx(float(cfg.get("half_w", 0.0)), 72.0)
		and is_equal_approx(float(cfg.get("cam_follow", 0.0)), 1.0))
	_check("shallow_2_5d_band", float(cfg.get("half_d", 99.0)) <= 2.6)
	_check("single_lagoon_light",
		main.sun_light != null and not main.sun_light.visible
		and main.arena_env != null
		and String(main.arena_env.get_meta("scene_grade_profile", "")) == "sky_lagoon")

	var required_assets: Array[String] = [
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_0.png",
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_1.png",
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_2.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_plane.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_slide.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_swing.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_seesaw.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_gate.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_activity_frame_v2.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_roshan.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_fir_sway.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_family_drift.png",
	]
	var assets_ok := true
	for path: String in required_assets:
		assets_ok = assets_ok and ResourceLoader.exists(path)
	_check("codex_sprite_assets", assets_ok)
	var master_path := "res://assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_3x1.png"
	var panorama_master: Image = Image.load_from_file(
		ProjectSettings.globalize_path(master_path))
	var native_master_ok := panorama_master != null and not panorama_master.is_empty()
	if native_master_ok:
		native_master_ok = (
			panorama_master.get_width() == 2172
			and panorama_master.get_height() == 724
			and panorama_master.get_width() >= 2048
			and absf(float(panorama_master.get_width())
				/ float(panorama_master.get_height()) - 3.0) <= 0.000001)
	_check("native_2k_exact_ratio_master", native_master_ok)
	var runtime_tiles_ok := true
	for tile_index: int in range(3):
		var tile: Texture2D = load(
			"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_%d.png"
			% tile_index)
		runtime_tiles_ok = (
			runtime_tiles_ok and tile != null
			and tile.get_size() == Vector2(724, 724))
	_check("lossless_native_runtime_tiles", runtime_tiles_ok)
	var stage_root: Node3D = main.g.get("ss_root") as Node3D
	var node_stack: Array[Node] = [stage_root]
	var sprite_count := 0
	var mesh_count := 0
	var canvas_count := 0
	var shaded_count := 0
	var bad_scale_count := 0
	var visible_sprite_count := 0
	var depth_layers: Dictionary = {}
	var backdrop_positions: Array[Vector3] = []
	var billboarded_backdrops := 0
	while not node_stack.is_empty():
		var stage_node: Node = node_stack.pop_back()
		if stage_node is Sprite3D:
			var stage_sprite := stage_node as Sprite3D
			sprite_count += 1
			visible_sprite_count += 1 if stage_sprite.visible else 0
			shaded_count += 1 if stage_sprite.shaded else 0
			bad_scale_count += 1 if stage_sprite.pixel_size <= 0.0 else 0
			depth_layers[snappedf(stage_sprite.global_position.z, 0.1)] = true
			if stage_sprite.name.begins_with("SkyLagoonBackdrop_"):
				backdrop_positions.append(stage_sprite.position)
				if stage_sprite.billboard != BaseMaterial3D.BILLBOARD_DISABLED:
					billboarded_backdrops += 1
		elif stage_node is MeshInstance3D:
			mesh_count += 1
		elif stage_node is CanvasItem:
			canvas_count += 1
		for child: Node in stage_node.get_children():
			node_stack.append(child)
	_check("world_art_is_unshaded_sprite3d",
		sprite_count == 29 and mesh_count == 0 and canvas_count == 0
		and shaded_count == 0 and bad_scale_count == 0,
		"sprites=%d meshes=%d canvas=%d shaded=%d bad_scale=%d" % [
			sprite_count, mesh_count, canvas_count, shaded_count, bad_scale_count])
	_check("real_depth_and_speedy_overdraw",
		depth_layers.size() >= 4 and visible_sprite_count <= 20,
		"depth_layers=%d visible_cards=%d" % [
			depth_layers.size(), visible_sprite_count])
	backdrop_positions.sort_custom(func(a: Vector3, b: Vector3) -> bool:
		return a.x < b.x)
	var mural_y: float = SkyLagoonPromenade.BACKDROP_CENTER_Y
	var seamless_cards_ok := backdrop_positions.size() == 3
	if seamless_cards_ok:
		seamless_cards_ok = (
			backdrop_positions[0] == Vector3(-48.0, mural_y, -18.0)
			and backdrop_positions[1] == Vector3(0.0, mural_y, -18.0)
			and backdrop_positions[2] == Vector3(48.0, mural_y, -18.0))
	_check("native_tiles_share_depth_and_meet_edges", seamless_cards_ok)
	# A billboarded card swings about its own centre, so the three tiles stop
	# being coplanar the instant the lens is off-centre and the environment sky
	# shows through the wedges between them. The wall must stay flat.
	_check("mural_cards_never_billboard", billboarded_backdrops == 0,
		"billboarded=%d" % billboarded_backdrops)

	# THE MURAL IS THE SCREEN. The promenade — not the free-swim chase cam —
	# must own the lens, and the frame it holds has to stay inside the painted
	# rectangle at both ends of the walk.
	var promenade := main._lagoon_promenade_ref()
	var stage_cfg: Dictionary = main.g.get("ss_cfg", {})
	var lens: Camera3D = main.player.cam
	var origin: Vector3 = main.LEVEL2_POS
	_check("stage_owns_the_lens",
		is_equal_approx(lens.fov, SkyLagoonPromenade.CAM_FOV)
		and absf(lens.position.y - (origin.y + SkyLagoonPromenade.CAM_H)) <= 0.35
		and absf(lens.position.z - (origin.z + SkyLagoonPromenade.CAM_DIST)) <= 0.35,
		"fov=%.1f y=%.2f z=%.2f" % [lens.fov,
			lens.position.y - origin.y, lens.position.z - origin.z])
	var mural_half_w: float = SkyLagoonPromenade.BACKDROP_TILE_SIZE.x * 1.5
	var mural_half_h: float = SkyLagoonPromenade.BACKDROP_TILE_SIZE.y * 0.5
	var covered := true
	var worst := ""
	for edge_x: float in [72.0, -72.0]:
		main.player.position.x = origin.x + edge_x
		for _i in range(6):
			promenade.tick(0.5)
		var view: Vector2 = promenade.stage.view_half_size(
			stage_cfg, lens, SkyLagoonPromenade.BACKDROP_Z)
		var cam_x: float = lens.position.x - origin.x
		var cam_y: float = lens.position.y - origin.y
		var inside: bool = (
			cam_x + view.x <= mural_half_w + 0.01
			and cam_x - view.x >= -mural_half_w - 0.01
			and cam_y + view.y <= mural_y + mural_half_h + 0.01
			and cam_y - view.y >= mural_y - mural_half_h - 0.01)
		covered = covered and inside
		if not inside:
			worst = "at x=%.0f frame=[%.1f,%.1f]x[%.1f,%.1f]" % [edge_x,
				cam_x - view.x, cam_x + view.x, cam_y - view.y, cam_y + view.y]
	_check("mural_fills_the_frame_at_both_ends", covered, worst)
	main.player.position.x = origin.x - 48.0
	for _i in range(6):
		promenade.tick(0.5)
	_check("roshan_is_sprite_card",
		not main.player.visible
		and main.g.get("lagoon_roshan_card") is Sprite3D)
	var ambient_cards: Array = main.g.get("lagoon_ambient_cards", [])
	var plane_card: Sprite3D = main.g.get("lagoon_plane_card") as Sprite3D
	var ambient_before := Vector3.ZERO
	var plane_before := Vector3.ZERO
	if ambient_cards.size() == 6:
		ambient_before = (ambient_cards[0] as Sprite3D).position
	if plane_card != null:
		plane_before = plane_card.position
	promenade._tick_ambient_life(0.75)
	var ambient_moves := (
		ambient_cards.size() == 6
		and (ambient_cards[0] as Sprite3D).position != ambient_before
		and plane_card != null and plane_card.visible
		and plane_card.position != plane_before)
	_check("low_cost_ambient_life_and_plane", ambient_moves)

	var targets: Array = main.g.get("lagoon_promenade_targets", [])
	var ids: Dictionary = {}
	var frame_screens: Dictionary = {}
	for value in targets:
		var target: Dictionary = value as Dictionary
		var id: String = String(target.get("id", ""))
		ids[id] = true
		if String(target.get("kind", "")) == "frame":
			var node: Node3D = target.get("node") as Node3D
			var local_x: float = node.position.x
			var screen_index := 1
			if local_x >= -24.0 and local_x < 24.0:
				screen_index = 2
			elif local_x >= 24.0:
				screen_index = 3
			frame_screens[screen_index] = int(frame_screens.get(screen_index, 0)) + 1
	_check("interactive_roster", targets.size() == 8
		and ids.has("plane") and ids.has("slide") and ids.has("swing")
		and ids.has("seesaw") and ids.has("castle_gate"))
	_check("one_frame_per_screen",
		int(frame_screens.get(1, 0)) == 1
		and int(frame_screens.get(2, 0)) == 1
		and int(frame_screens.get(3, 0)) == 1)

	var runway_frame: Dictionary = {}
	for value in targets:
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == "runway_frame":
			runway_frame = target
			break
	var frame_node: Node3D = runway_frame.get("node") as Node3D
	var cam: Camera3D = main.player.cam
	var frame_screen: Vector2 = cam.unproject_position(frame_node.global_position)
	main._lagoon_promenade_ref().handle_touch(frame_screen)
	var first_press_ok: bool = (
		String(main.g.get("lagoon_promenade_focus", "")) == "runway_frame"
		and main.mg_kind == "")
	_check("frame_first_press_highlights", first_press_ok)
	main._lagoon_promenade_ref().handle_touch(frame_screen)
	await process_frame
	_check("frame_second_press_opens", main.mg_kind == "snowman")
	if main.mg_kind != "":
		main._mg2d_close()
	await _frames(2)

	var castle_target: Dictionary = {}
	for value in (main.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == "castle_gate":
			castle_target = target
			break
	main._lagoon_promenade_ref()._focus(castle_target)
	main._lagoon_promenade_ref()._activate(castle_target)
	await _frames(8)
	_check("drawbridge_enters_castle",
		main.game == "level2" and String(main.g.get("phase", "")) == "hall")

	if failed:
		print("FAIL|Sky Lagoon 2.5D promenade regression")
	else:
		print("LAGOON25D|ALL: OK")
	quit()
