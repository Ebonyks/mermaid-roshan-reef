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
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v2_tile_0.png",
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v2_tile_1.png",
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v2_tile_2.png",
		"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v2_tile_3.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_plane_v4_audited_360.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_swing_v3_compact.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_seesaw_v4_compact.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_castle_gate_v3.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_activity_frame_v3.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_fir_sway_v2.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_pnw_currant_sway_audited.png",
		"res://assets/sprites/sky_lagoon/sky_lagoon_cloud_family_v5_audited.png",
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
	var assets_ok := true
	for path: String in required_assets:
		assets_ok = assets_ok and ResourceLoader.exists(path)
	_check("codex_sprite_assets", assets_ok)
	var master_path := "res://assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v2_3x1.png"
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
	for tile_index: int in range(4):
		var tile: Texture2D = load(
			"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v2_tile_%d.png"
			% tile_index)
		runtime_tiles_ok = (
			runtime_tiles_ok and tile != null
			and tile.get_size() == Vector2(543, 724))
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
	var unanchored := 0
	var unanchored_worst := ""
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
				# every world card must share the mural's depth; a card in front
				# of it parallaxes faster than the art it stands on, so it slides
				# across the painted ground and its tap target drifts off the
				# thing it represents (owner report 2026-07-27)
				var off: float = absf(stage_sprite.global_position.z
					- (main.g.get("ss_root") as Node3D).position.z
					- SkyLagoonPromenade.BACKDROP_Z)
				if off > 0.7:
					unanchored += 1
					unanchored_worst = "%s off by %.1f" % [stage_sprite.name, off]
		elif stage_node is MeshInstance3D:
			mesh_count += 1
		elif stage_node is CanvasItem:
			canvas_count += 1
		for child: Node in stage_node.get_children():
			node_stack.append(child)
	_check("world_art_is_unshaded_sprite3d",
		sprite_count == 44 and mesh_count == 0 and canvas_count == 0
		and shaded_count == 0 and bad_scale_count == 0,
		"sprites=%d meshes=%d canvas=%d shaded=%d bad_scale=%d" % [
			sprite_count, mesh_count, canvas_count, shaded_count, bad_scale_count])
	_check("real_depth_and_speedy_overdraw",
		depth_layers.size() >= 4 and visible_sprite_count <= 34
		and contact_shadow_count == 14,
		"depth_layers=%d visible_cards=%d contact_shadows=%d" % [
			depth_layers.size(), visible_sprite_count, contact_shadow_count])
	backdrop_positions.sort_custom(func(a: Vector3, b: Vector3) -> bool:
		return a.x < b.x)
	var mural_y: float = SkyLagoonPromenade.BACKDROP_CENTER_Y
	var seamless_cards_ok := backdrop_positions.size() == 4
	if seamless_cards_ok:
		seamless_cards_ok = (
			backdrop_positions[0] == Vector3(-54.0, mural_y, -18.0)
			and backdrop_positions[1] == Vector3(-18.0, mural_y, -18.0)
			and backdrop_positions[2] == Vector3(18.0, mural_y, -18.0)
			and backdrop_positions[3] == Vector3(54.0, mural_y, -18.0))
	_check("native_tiles_share_depth_and_meet_edges", seamless_cards_ok)
	# A billboarded card swings about its own centre, so the four tiles stop
	# being coplanar the instant the lens is off-centre and the environment sky
	# shows through the wedges between them. The wall must stay flat.
	_check("mural_cards_never_billboard", billboarded_backdrops == 0,
		"billboarded=%d" % billboarded_backdrops)
	_check("world_cards_anchored_to_the_mural", unanchored == 0, unanchored_worst)

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
	var mural_half_w: float = SkyLagoonPromenade.BACKDROP_TILE_SIZE.x * 2.0
	var mural_half_h: float = SkyLagoonPromenade.BACKDROP_TILE_SIZE.y * 0.5
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
	# the bug this replaces measured 24%: cards 12 units in front of the mural
	_check("set_does_not_drift_across_the_pan", drift <= 0.02,
		"standee travelled %.1f%% differently from the painting" % (drift * 100.0))
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
		and slide_node.texture.get_height() * slide_node.pixel_size <= 13.81
		and swing_node.texture.get_height() * swing_node.pixel_size <= 13.31
		and compact_seesaw.texture.get_height() * compact_seesaw.pixel_size <= 6.81)
	_check("playground_equipment_fits_center_lawn", equipment_fits_lawn)
	var roshan_card: Sprite3D = main.g.get("lagoon_roshan_card") as Sprite3D
	var idle_texture: Texture2D = roshan_card.texture
	promenade._start_playground_animation("swing", toy_nodes.get("swing") as Node3D)
	var swing_start: Vector3 = roshan_card.position
	promenade._tick_playground_animation(0.55)
	var swing_animates: bool = (
		not (main.g.get("lagoon_play_anim", {}) as Dictionary).is_empty()
		and roshan_card.texture != idle_texture
		and roshan_card.position != swing_start
		and roshan_card.position.z > SkyLagoonPromenade.PLAY_Z)
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
	main.player.position.x = origin.x + 40.0
	for _i in range(6):
		promenade.tick(0.5)
	var gate_screen: Vector2 = lens.unproject_position(gate_node.global_position)
	var view_rect := Rect2(Vector2.ZERO, main.get_viewport().get_visible_rect().size)
	_check("castle_door_is_on_screen_from_the_walk", view_rect.has_point(gate_screen),
		"gate at %s in a %s viewport" % [gate_screen, view_rect.size])
	promenade.handle_touch(gate_screen)
	var gate_focus_ok: bool = (
		String(main.g.get("lagoon_promenade_focus", "")) == "castle_gate")
	_check("castle_door_first_tap_highlights", gate_focus_ok)
	promenade.handle_touch(gate_screen)
	await _frames(8)
	_check("drawbridge_enters_castle",
		main.game == "level2" and String(main.g.get("phase", "")) == "hall")

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
