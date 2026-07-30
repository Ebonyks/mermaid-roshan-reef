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

func _opaque_world_rect(sprite: Sprite3D) -> Rect2:
	var image: Image = sprite.texture.get_image()
	var used: Rect2i = image.get_used_rect()
	var size := Vector2(image.get_width(), image.get_height())
	var left: float = sprite.position.x + (float(used.position.x) - size.x * 0.5) * sprite.pixel_size
	var right: float = sprite.position.x + (float(used.end.x) - size.x * 0.5) * sprite.pixel_size
	var top: float = sprite.position.y + (size.y * 0.5 - float(used.position.y)) * sprite.pixel_size
	var bottom: float = sprite.position.y + (size.y * 0.5 - float(used.end.y)) * sprite.pixel_size
	return Rect2(left, bottom, right - left, top - bottom)

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
	main.save_data["lagoon_plane_departed"] = false
	main._enter_level2()
	await _frames(8)

	_check("promenade_phase",
		main.game == "level2" and String(main.g.get("phase", "")) == "promenade")
	var cfg: Dictionary = main.g.get("ss_cfg", {})
	_check("three_screen_width",
		is_equal_approx(float(cfg.get("half_w", 0.0)), 72.0)
		and is_equal_approx(float(cfg.get("cam_follow", 0.0)), 1.0)
		and bool(cfg.get("side_on_axis_lock", false)))
	_check("shallow_2_5d_band", float(cfg.get("half_d", 99.0)) <= 2.6)
	_check("single_lagoon_light",
		main.sun_light != null and not main.sun_light.visible
		and main.arena_env != null
		and String(main.arena_env.get_meta("scene_grade_profile", "")) == "sky_lagoon")

	var required_assets: Array[String] = [
		"res://assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_swing_single_mermaid_v1.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_tall_v1.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_0.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_1.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_2.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_3.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_0.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_1.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_2.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_3.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_0.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_1.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_2.png",
		"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_3.png",
	]
	for row: int in range(2):
		for column: int in range(6):
			required_assets.append(
				"res://assets/flats/sky_lagoon/main/"
				+ "flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png"
				% [row, column])
	var assets_ok := true
	for path: String in required_assets:
		assets_ok = assets_ok and ResourceLoader.exists(path)
	_check("codex_sprite_assets", assets_ok)
	var castle_card: Sprite3D = main.g.get("lagoon_castle_card") as Sprite3D
	var castle_fit_ok := castle_card != null
	var castle_fit_detail := ""
	if castle_card != null:
		var castle_image: Image = castle_card.texture.get_image()
		var castle_world_width := (
			castle_image.get_width() * castle_card.pixel_size
		)
		var castle_reference_position: Vector3 = castle_card.get_meta(
			"mural_reference_position", castle_card.position) as Vector3
		var castle_base_y := castle_reference_position.y - (
			castle_image.get_height() * castle_card.pixel_size * 0.5
		)
		# Interactive depth cards shift slightly as the camera pans so they stay
		# socketed to their painted mural landmarks. Audit the authored socket,
		# not the expected runtime parallax offset at this probe's camera x.
		var castle_reference_x := float(
			castle_card.get_meta("mural_reference_x", INF)
		)
		castle_fit_ok = (
			not castle_card.shaded
			and castle_card.cast_shadow
				== GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			and not castle_card.has_meta("contact_shadow")
			and is_equal_approx(castle_reference_x, 51.572852)
			and is_equal_approx(castle_world_width, 28.37504)
			and is_equal_approx(castle_base_y, -3.193)
		)
		castle_fit_detail = "socket_x=%.5f width=%.5f base=%.5f" % [
			castle_reference_x,
			castle_world_width,
			castle_base_y,
		]
	_check("four_tower_castle_neutral_fit_contract",
		castle_fit_ok, castle_fit_detail)
	var master_path := "res://assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png"
	var panorama_master: Image = Image.load_from_file(
		ProjectSettings.globalize_path(master_path))
	var native_master_ok := panorama_master != null and not panorama_master.is_empty()
	if native_master_ok:
		native_master_ok = (
			panorama_master.get_width() == 6144
			and panorama_master.get_height() == 2048
			and panorama_master.get_width() >= 2048
			and absf(float(panorama_master.get_width())
				/ float(panorama_master.get_height()) - 3.0) <= 0.000001)
	_check("native_2k_exact_ratio_master", native_master_ok)
	var runtime_tiles_ok := true
	for row: int in range(2):
		for column: int in range(6):
			var tile: Texture2D = load(
				"res://assets/flats/sky_lagoon/main/"
				+ "flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png"
				% [row, column])
			runtime_tiles_ok = (
				runtime_tiles_ok and tile != null
				and tile.get_size() == Vector2(1024, 1024))
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
	var mural_card: Sprite3D = null
	var contact_shadow_count := 0
	var tree_cards: Array[Sprite3D] = []
	var cloud_card: Sprite3D = null
	var smoke_cards: Array[Sprite3D] = []
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
				mural_card = stage_sprite
				if stage_sprite.billboard != BaseMaterial3D.BILLBOARD_DISABLED:
					billboarded_backdrops += 1
			elif bool(stage_sprite.get_meta("sky_lagoon_contact_shadow", false)):
				contact_shadow_count += 1
			elif stage_sprite != main.g.get("lagoon_roshan_card"):
				var ambient_kind: String = String(
					stage_sprite.get_meta("ambient_kind", ""))
				if ambient_kind == "tree":
					tree_cards.append(stage_sprite)
				elif ambient_kind == "cloud":
					cloud_card = stage_sprite
				elif ambient_kind == "smoke":
					smoke_cards.append(stage_sprite)
		elif stage_node is MeshInstance3D:
			mesh_count += 1
		elif stage_node is CanvasItem:
			canvas_count += 1
		for child: Node in stage_node.get_children():
			node_stack.append(child)
	_check("world_art_is_unshaded_sprite3d",
		sprite_count == 34 and mesh_count == 0 and canvas_count == 0
		and shaded_count == 0 and bad_scale_count == 0,
		"sprites=%d meshes=%d canvas=%d shaded=%d bad_scale=%d" % [
			sprite_count, mesh_count, canvas_count, shaded_count, bad_scale_count])
	_check("real_depth_and_speedy_overdraw",
		depth_layers.size() >= 6 and visible_sprite_count <= 29
		and contact_shadow_count == 6
		and SkyLagoonPromenade.NEAR_Z > -SkyLagoonPromenade.HALF_D
		and SkyLagoonPromenade.BACKDROP_Z - SkyLagoonPromenade.NEAR_Z < -16.0,
		"depth_layers=%d visible_cards=%d contact_shadows=%d" % [
			depth_layers.size(), visible_sprite_count, contact_shadow_count])
	var tree_placement_ok := tree_cards.size() == 1
	var tree_detail := "cards=%d" % tree_cards.size()
	for index: int in range(tree_cards.size()):
		var tree: Sprite3D = tree_cards[index]
		var tree_rect: Rect2 = _opaque_world_rect(tree)
		# The lagoon water is confined to the arrival apron. Every movable tree
		# belongs on the dry rear lawn, to its right and above the play lane.
		tree_placement_ok = (
			tree_placement_ok and tree_rect.position.x > -38.0
			and tree_rect.position.y > 1.0)
		for other_index: int in range(index):
			var other_rect: Rect2 = _opaque_world_rect(tree_cards[other_index])
			tree_placement_ok = tree_placement_ok and not tree_rect.intersects(other_rect)
		tree_detail += " %s=%s" % [tree.name, tree_rect]
	_check("tree_stickers_are_dry_and_non_overlapping", tree_placement_ok, tree_detail)
	var cloud_clear_ok := cloud_card != null
	if cloud_card != null:
		var cloud_probe_promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
		for _i in range(90):
			cloud_probe_promenade.tick(0.5)
		cloud_clear_ok = (
			cloud_card.position.x >= SkyLagoonPromenade.CLOUD_DRIFT_MIN_X
			and cloud_card.position.x <= SkyLagoonPromenade.CLOUD_DRIFT_MAX_X
			and cloud_card.position.y >= 28.2)
	_check("single_cloud_uses_clear_sky_corridor", cloud_clear_ok,
		"position=%s" % (cloud_card.position if cloud_card != null else Vector3.ZERO))
	_check("day_one_plane_departs_and_stays_gone",
		main.g.get("lagoon_plane_card") == null
		and bool(main.save_data.get("lagoon_plane_departed", false)),
		"departed=%s" % main.save_data.get("lagoon_plane_departed", false))
	var seamless_cards_ok := backdrop_positions.size() == 12
	for row: int in range(2):
		for column: int in range(6):
			seamless_cards_ok = (
				seamless_cards_ok
				and backdrop_positions.has(Vector3(
					-60.0 + float(column) * 24.0,
					21.5 - float(row) * 24.0,
					-18.0)))
	_check("native_tiles_share_depth_and_meet_edges", seamless_cards_ok)
	# A billboarded card swings about its own centre, so the mural tiles stop
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
	# Reproduce the owner-reported left-edge bounce from a cold centre frame.
	# The camera must approach its mural clamp monotonically and keep a
	# perpendicular optical axis while its position is still easing.
	var left_edge_stable := lens != null
	var left_edge_detail := "no camera"
	if lens != null:
		lens.position = origin + Vector3(
			0.0, SkyLagoonPromenade.CAM_H, SkyLagoonPromenade.CAM_DIST)
		lens.look_at(origin + Vector3(
			0.0, SkyLagoonPromenade.CAM_H, 0.0))
		var pan_limit: float = promenade.stage.screen_pan_limit(stage_cfg, lens)
		var previous_camera_x := 0.0
		var worst_axis_x := 0.0
		for _edge_frame: int in range(120):
			promenade.stage._glide_camera(
				1.0 / 60.0, stage_cfg, stage_root, -SkyLagoonPromenade.HALF_W)
			var camera_x: float = lens.position.x - origin.x
			var camera_forward: Vector3 = -lens.global_transform.basis.z.normalized()
			worst_axis_x = maxf(worst_axis_x, absf(camera_forward.x))
			left_edge_stable = left_edge_stable \
				and camera_x <= previous_camera_x + 0.00001 \
				and camera_x >= -pan_limit - 0.00001
			previous_camera_x = camera_x
		left_edge_stable = left_edge_stable \
			and absf(previous_camera_x + pan_limit) <= 0.01 \
			and worst_axis_x <= 0.00001
		left_edge_detail = "x=%.3f clamp=%.3f axis_x=%.7f" % [
			previous_camera_x, -pan_limit, worst_axis_x]
	_check("left_edge_camera_has_no_bounce", left_edge_stable, left_edge_detail)
	var mural_half_w: float = (
		SkyLagoonPromenade.BACKDROP_TILE_SIZE.x
		* float(SkyLagoonPromenade.BACKDROP_COLUMNS) * 0.5)
	var mural_half_h: float = (
		SkyLagoonPromenade.BACKDROP_TILE_SIZE.y
		* float(SkyLagoonPromenade.BACKDROP_ROWS) * 0.5)
	var mural_y: float = SkyLagoonPromenade.BACKDROP_CENTER_Y
	var covered := true
	var worst := ""
	var drift_gaps: Array[float] = []
	var slide_card: Node3D = null
	for value in (main.g.get("lagoon_promenade_targets", []) as Array):
		if String((value as Dictionary).get("id", "")) == "slide":
			slide_card = (value as Dictionary).get("node") as Node3D
	# the framing sweep teleports her to both ends; disarm the castle doorstep
	# for it, or arriving at the right-hand end walks her straight indoors
	main.g["lagoon_castle_armed"] = false
	var walk_edges: Array[float] = [72.0, -72.0]
	for edge_x in walk_edges:
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
		if slide_card != null and mural_card != null:
			# THE anchoring regression: a standee must travel across the screen
			# at the same rate as the painting behind it. Measured as a RATIO,
			# not in pixels — the headless viewport is square, so its lens pans
			# more than twice as far as a phone's and the same geometry shows a
			# proportionally larger pixel figure.
			drift_gaps.append(lens.unproject_position(slide_card.global_position).x)
			drift_gaps.append(lens.unproject_position(mural_card.global_position).x)
		covered = covered and inside
		if not inside:
			worst = "at x=%.0f frame=[%.1f,%.1f]x[%.1f,%.1f]" % [edge_x,
				cam_x - view.x, cam_x + view.x, cam_y - view.y, cam_y + view.y]
	_check("mural_fills_the_frame_at_both_ends", covered, worst)
	var drift: float = 1.0
	if drift_gaps.size() == 4:
		var standee_travel: float = absf(drift_gaps[0] - drift_gaps[2])
		var mural_travel: float = absf(drift_gaps[1] - drift_gaps[3])
		drift = absf(standee_travel - mural_travel) / maxf(1.0, mural_travel)
	# Playground equipment was extracted from exact painted lawn sockets. It
	# remains a real-depth Sprite3D for occlusion, but may not visibly skate
	# against those sockets during a full three-page camera pan.
	_check("playground_cards_stay_on_mural_sockets",
		drift <= 0.01,
		"slide travelled %.2f%% differently from the painting" % (drift * 100.0))
	# THE ROUTE: the promenade is a path, and the path has to end at the door.
	var route: Array = (main.g.get("ss_cfg", {}) as Dictionary).get("route", [])
	var route_span: Vector2 = promenade.stage.route_span(main.g.get("ss_cfg", {}))
	var door_walk_x: float = promenade._walk_x(SkyLagoonPromenade.CASTLE_DOOR_X)
	var reach: float = promenade.stage.keep_on_screen(
		main.g.get("ss_cfg", {}), door_walk_x)
	_check("route_runs_the_level_and_ends_at_the_door",
		route.size() == SkyLagoonPromenade.ROUTE_PAINTED.size()
		and absf(route_span.y - door_walk_x) <= 0.01
		and route_span.x < -40.0
		and absf(reach - door_walk_x) <= 0.01,
		"waypoints=%d span=%s door=%.1f reachable=%.1f" % [
			route.size(), route_span, door_walk_x, reach])
	main.player.position.x = origin.x - 48.0
	for _i in range(6):
		promenade.tick(0.5)
	_check("roshan_is_sprite_card",
		not main.player.visible
		and main.g.get("lagoon_roshan_card") is Sprite3D)
	var ambient_cards: Array = main.g.get("lagoon_ambient_cards", [])
	var ambient_before := Vector3.ZERO
	if ambient_cards.size() == 5:
		ambient_before = (ambient_cards[0] as Sprite3D).position
	promenade._tick_ambient_life(0.75)
	var ambient_moves := (
		ambient_cards.size() == 5
		and (ambient_cards[0] as Sprite3D).position != ambient_before)
	_check("low_cost_ambient_life",
		ambient_moves and smoke_cards.size() == 3,
		"cards=%d smoke_wisps=%d" % [ambient_cards.size(), smoke_cards.size()])
	var shore_firs_ok := true
	for ambient_value in ambient_cards:
		var ambient_card: Sprite3D = ambient_value as Sprite3D
		if String(ambient_card.get_meta("ambient_kind", "")) == "fir":
			var fir_base: Vector3 = ambient_card.get_meta(
				"ambient_base", ambient_card.position) as Vector3
			shore_firs_ok = shore_firs_ok and fir_base.x >= -50.0
	_check("pnw_firs_are_rooted_on_land", shore_firs_ok)

	var targets: Array = main.g.get("lagoon_promenade_targets", [])
	var ids: Dictionary = {}
	for value in targets:
		var target: Dictionary = value as Dictionary
		var id: String = String(target.get("id", ""))
		ids[id] = true
	_check("interactive_roster", targets.size() == 4
		and not ids.has("plane") and ids.has("slide") and ids.has("swing")
		and ids.has("seesaw") and ids.has("castle_gate"))
	_check("mismatched_lawn_picture_frames_removed",
		not ids.has("runway_frame")
		and not ids.has("playground_frame")
		and not ids.has("castle_frame"))

	# Each playground toy owns a purpose-built four-frame Roshan sequence.
	# The one existing Roshan Sprite3D swaps textures, so the animation adds
	# no world cards or overdraw. Exercise the real state machine, including
	# rung bounce, seated chute frames, and repeated seesaw direction changes.
	var toy_nodes: Dictionary = {}
	for value in targets:
		var toy_target: Dictionary = value as Dictionary
		if String(toy_target.get("kind", "")) == "playground":
			toy_nodes[String(toy_target.get("payload", ""))] = toy_target.get("node")
	var slide_node: Sprite3D = toy_nodes.get("slide") as Sprite3D
	var swing_node: Sprite3D = toy_nodes.get("swing") as Sprite3D
	var compact_seesaw: Sprite3D = toy_nodes.get("seesaw") as Sprite3D
	var equipment_fits_lawn := (
		slide_node != null and swing_node != null and compact_seesaw != null
		and slide_node.texture.get_height() * slide_node.pixel_size <= 11.41
		and swing_node.texture.get_height() * swing_node.pixel_size <= 11.81
		and compact_seesaw.texture.get_height() * compact_seesaw.pixel_size <= 4.51)
	_check("playground_equipment_fits_center_lawn", equipment_fits_lawn)
	_check("playground_cutouts_are_opaque_depth_cards",
		slide_node.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD
		and swing_node.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD
		and compact_seesaw.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD
		and is_equal_approx(float(slide_node.get_meta("mural_socket_lock", 0.0)),
			SkyLagoonPromenade.GROUND_SOCKET_LOCK)
		and is_equal_approx(float(swing_node.get_meta("mural_socket_lock", 0.0)),
			SkyLagoonPromenade.GROUND_SOCKET_LOCK))
	var slide_rect: Rect2 = _opaque_world_rect(slide_node)
	var swing_rect: Rect2 = _opaque_world_rect(swing_node)
	var seesaw_rect: Rect2 = _opaque_world_rect(compact_seesaw)
	var silhouette_gaps_ok := (
		swing_rect.position.x - slide_rect.end.x >= 0.5
		and seesaw_rect.position.x - swing_rect.end.x >= 0.5)
	_check("playground_opaque_silhouettes_do_not_overlap", silhouette_gaps_ok,
		"slide_swing_gap=%.2f swing_seesaw_gap=%.2f" % [
			swing_rect.position.x - slide_rect.end.x,
			seesaw_rect.position.x - swing_rect.end.x])
	var roshan_card: Sprite3D = main.g.get("lagoon_roshan_card") as Sprite3D
	var idle_texture: Texture2D = roshan_card.texture
	promenade._start_playground_animation("swing", toy_nodes.get("swing") as Node3D)
	var swing_start: Vector3 = roshan_card.position
	promenade._tick_playground_animation(0.55)
	var swing_animates: bool = (
		not (main.g.get("lagoon_play_anim", {}) as Dictionary).is_empty()
		and roshan_card.texture != idle_texture
		and roshan_card.position != swing_start
		and roshan_card.position.z > SkyLagoonPromenade.PLAY_Z
		and is_equal_approx(roshan_card.scale.x, 1.38)
		and absf(roshan_card.position.x - swing_node.position.x) < 0.2)
	promenade._finish_playground_animation()
	_check("swing_has_grip_pose_arc_animation", swing_animates)

	promenade._start_playground_animation("slide", toy_nodes.get("slide") as Node3D)
	var ladder_start: Vector3 = roshan_card.position
	promenade._tick_playground_animation(0.30)
	var rung_bounce_y: float = roshan_card.position.y
	promenade._tick_playground_animation(0.25)
	var climbed_step_y: float = roshan_card.position.y
	promenade._tick_slide_animation(
		roshan_card, toy_nodes.get("slide") as Node3D, 2.80)
	var seated_texture: String = roshan_card.texture.resource_path
	promenade._tick_slide_animation(
		roshan_card, toy_nodes.get("slide") as Node3D, 3.70)
	var riding_texture: String = roshan_card.texture.resource_path
	var slide_animates: bool = (
		rung_bounce_y > ladder_start.y
		and climbed_step_y > rung_bounce_y
		and seated_texture.ends_with("roshan_slide_2.png")
		and riding_texture.ends_with("roshan_slide_3.png")
		and roshan_card.rotation.z < -0.1)
	promenade._finish_playground_animation()
	_check("slide_has_bouncy_steps_and_seated_ride", slide_animates)

	var seesaw_node: Node3D = toy_nodes.get("seesaw") as Node3D
	promenade._start_playground_animation("seesaw", seesaw_node)
	var saw_high := false
	var saw_low := false
	var saw_motion_samples := 0
	var prior_saw_rotation: float = seesaw_node.rotation.z
	for _sample in range(8):
		promenade._tick_playground_animation(0.48)
		saw_high = saw_high or seesaw_node.rotation.z > 0.08
		saw_low = saw_low or seesaw_node.rotation.z < -0.08
		if not is_equal_approx(seesaw_node.rotation.z, prior_saw_rotation):
			saw_motion_samples += 1
		prior_saw_rotation = seesaw_node.rotation.z
	var seesaw_animates: bool = (
		saw_high and saw_low and saw_motion_samples >= 5
		and roshan_card.texture != idle_texture)
	promenade._finish_playground_animation()
	_check("seesaw_rocks_back_and_forth_three_times", seesaw_animates)
	_check("playground_animation_reuses_one_sprite3d",
		roshan_card.texture == idle_texture
		and (main.g.get("lagoon_play_anim", {}) as Dictionary).is_empty())

	var swing_screen: Vector2 = lens.unproject_position(swing_node.global_position)
	main._lagoon_promenade_ref().handle_touch(swing_screen)
	var first_press_ok: bool = (
		String(main.g.get("lagoon_promenade_focus", "")) == "swing"
		and (main.g.get("lagoon_play_anim", {}) as Dictionary).is_empty())
	_check("toy_first_press_highlights", first_press_ok)
	main._lagoon_promenade_ref().handle_touch(swing_screen)
	await process_frame
	_check("toy_second_press_plays",
		String((main.g.get("lagoon_play_anim", {}) as Dictionary).get(
			"kind", "")) == "swing")
	promenade._finish_playground_animation()
	await _frames(2)

	# Walk to the castle end and enter it THE WAY THE CHILD DOES: two taps at
	# the door's own place on screen. The old probe called _focus/_activate
	# directly, so it never noticed that the gate's tap target had drifted
	# 237 px off the painted door and tapping the door did nothing at all.
	var castle_target: Dictionary = {}
	for value in (main.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == "castle_gate":
			castle_target = target
			break
	var gate_node: Node3D = castle_target.get("node") as Node3D
	var gate_highlight: Sprite3D = castle_target.get("highlight") as Sprite3D
	main.player.position.x = origin.x + 40.0
	for _i in range(6):
		promenade.tick(0.5)
	var gate_screen: Vector2 = lens.unproject_position(gate_node.global_position)
	var view_rect := Rect2(Vector2.ZERO, main.get_viewport().get_visible_rect().size)
	_check("castle_door_is_on_screen_from_the_walk", view_rect.has_point(gate_screen),
		"gate at %s in a %s viewport" % [gate_screen, view_rect.size])
	promenade.handle_touch(gate_screen)
	var gate_focus_ok: bool = (
		String(main.g.get("lagoon_promenade_focus", "")) == "castle_gate"
		and gate_highlight != null and gate_highlight.visible)
	_check("castle_door_first_tap_highlights", gate_focus_ok)
	var door_only_highlight_ok: bool = (
		gate_node == main.g.get("lagoon_castle_door_focus")
		and gate_node != castle_card
		and gate_highlight != null
		and gate_highlight.texture != castle_card.texture
		and gate_highlight.texture.get_size() == Vector2(199, 228)
		and gate_node.position.y < castle_card.position.y
		and gate_highlight.scale == Vector3.ONE)
	_check("castle_focus_is_door_only_not_full_castle",
		door_only_highlight_ok,
		"focus_size=%s door_y=%.2f castle_y=%.2f scale=%s" % [
			gate_highlight.texture.get_size() if gate_highlight != null
				else Vector2.ZERO,
			gate_node.position.y,
			castle_card.position.y,
			gate_highlight.scale if gate_highlight != null else Vector3.ZERO])
	promenade.handle_touch(gate_screen)
	await _frames(8)
	_check("drawbridge_enters_castle",
		main.game == "level2" and String(main.g.get("phase", "")) == "hall")
	var castle_rooms: CastleRooms25D = main._castle_rooms_ref()
	_check("drawbridge_opens_visible_2_5d_castle_not_legacy_hall",
		castle_rooms.is_open()
		and main.castle_room_world_root != null
		and main.castle_room_world_root.visible
		and main.castle_room_camera != null
		and main.castle_room_camera.current
		and main.castle_room_background_tiles.size() == 8
		and main.arena_solids.is_empty()
		and not main.g.has("hall_exit"),
		"open=%s world=%s camera=%s tiles=%d solids=%d" % [
			str(castle_rooms.is_open()),
			str(main.castle_room_world_root != null
				and main.castle_room_world_root.visible),
			str(main.castle_room_camera != null and main.castle_room_camera.current),
			main.castle_room_background_tiles.size(),
			main.arena_solids.size()])

	# ...and the other road in: follow the painted way to its end. Rebuild the
	# promenade, walk to the far end of the route, and she should step inside
	# without any tap at all ("she won't touch the drawbridge for the castle").
	main._enter_level2()
	await _frames(8)
	var promenade2 := main._lagoon_promenade_ref()
	var span2: Vector2 = promenade2.stage.route_span(main.g.get("ss_cfg", {}))
	main.player.position.x = main.LEVEL2_POS.x + span2.y
	for _i in range(4):
		promenade2.tick(0.2)
	await _frames(10)
	_check("walking_the_path_enters_the_castle",
		main.game == "level2" and String(main.g.get("phase", "")) == "hall",
		"phase=%s" % String(main.g.get("phase", "?")))

	if failed:
		print("FAIL|Sky Lagoon 2.5D promenade regression")
	else:
		print("LAGOON25D|ALL: OK")
	quit()
