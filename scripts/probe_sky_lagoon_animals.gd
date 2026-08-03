extends SceneTree

# Acceptance probe for the authored Sky Lagoon animal habitat system.
# Set LAGOON_ANIMAL_SHOT_OUT to capture paired Mobile-renderer frames with and
# without each animal for the pixel-level lighting audit.

const EXPECTED_IDS := ["hare", "squirrel", "raccoon", "otter", "frog"]

var failures: int = 0
var main: ReefMain
var capture_manifest: Array[Dictionary] = []
var refuge_manifest: Array[Dictionary] = []


func _check(label: String, condition: bool, detail: String = "") -> void:
	print("LAGOONANIMALS|%s|%s%s" % [
		label,
		"OK" if condition else "FAIL",
		"" if detail == "" else "|%s" % detail,
	])
	if not condition:
		failures += 1


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _physics_frames(count: int) -> void:
	for _index: int in range(count):
		await physics_frame


func _color_values(color: Color) -> Array[float]:
	return [color.r, color.g, color.b, color.a]


func _stage_capture_camera(page: int) -> void:
	var page_x: float = float(SkyLagoonPromenade.ANIMAL_PAGE_CENTERS[page])
	var camera: Camera3D = get_root().get_viewport().get_camera_3d()
	if camera == null:
		camera = main.player.cam
	camera.global_position = main.LEVEL2_POS + Vector3(
		page_x, SkyLagoonPromenade.CAM_H, SkyLagoonPromenade.CAM_DIST)
	camera.look_at(main.LEVEL2_POS + Vector3(
		page_x, SkyLagoonPromenade.CAM_H, 0.0))
	camera.reset_physics_interpolation()


func _capture_pair(label: String, actor: Dictionary,
		definition: Dictionary) -> void:
	var out_dir: String = OS.get_environment("LAGOON_ANIMAL_SHOT_OUT")
	if out_dir == "":
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	var node: Sprite3D = actor.get("node") as Sprite3D
	var body: RigidBody3D = actor.get("body") as RigidBody3D
	var waterline: Sprite3D = actor.get("waterline") as Sprite3D
	var shadow: Sprite3D = node.get_meta("contact_shadow") as Sprite3D
	var capture_path: Array = definition["path"] as Array
	var capture_position: Vector3 = capture_path[0] as Vector3
	var original_freeze: bool = body.freeze
	body.freeze = true
	body.position = capture_position
	body.linear_velocity = Vector3.ZERO
	actor["route_position"] = capture_position
	node.position = Vector3.ZERO
	node.frame = 0
	if String(definition["support"]) == "water_jolt":
		waterline.position = Vector3(capture_position.x,
			float(definition["water_surface_y"]) - 0.05, capture_position.z + 0.045)
	else:
		var height: float = float(definition["height"])
		shadow.position = Vector3(capture_position.x,
			capture_position.y - height * 0.5 + maxf(0.08, height * 0.025),
			capture_position.z - 0.035)
	var original_main_processing: bool = main.is_processing()
	main.set_process(false)
	var old_tree_paused: bool = paused
	paused = true
	var old_time_scale: float = Engine.time_scale
	Engine.time_scale = 0.0
	_stage_capture_camera(int(definition["page"]))
	await process_frame
	_stage_capture_camera(int(definition["page"]))
	RenderingServer.force_draw(false)
	var viewport: Viewport = get_root().get_viewport()
	var with_image: Image = viewport.get_texture().get_image()
	if with_image == null:
		_check("capture_%s_render_target" % label, false)
		Engine.time_scale = old_time_scale
		paused = old_tree_paused
		main.set_process(original_main_processing)
		body.freeze = original_freeze
		if not original_freeze:
			body.sleeping = false
		return
	var with_path: String = out_dir.path_join(label + "_with.png")
	_check("capture_%s_with" % label, with_image.save_png(with_path) == OK)
	node.visible = false
	var baseline_water: bool = String(definition["support"]) == "water_jolt"
	shadow.visible = not baseline_water
	waterline.visible = baseline_water
	await process_frame
	_stage_capture_camera(int(definition["page"]))
	RenderingServer.force_draw(false)
	var without_image: Image = viewport.get_texture().get_image()
	var without_path: String = out_dir.path_join(label + "_without.png")
	if without_image == null:
		node.visible = true
		var restore_water: bool = String(definition["support"]) == "water_jolt"
		shadow.visible = not restore_water
		waterline.visible = restore_water
		_check("capture_%s_without_render_target" % label, false)
		Engine.time_scale = old_time_scale
		main.set_process(original_main_processing)
		paused = old_tree_paused
		body.freeze = original_freeze
		if not original_freeze:
			body.sleeping = false
		return

	_check("capture_%s_without" % label,
		without_image.save_png(without_path) == OK)
	node.visible = true
	var water_supported: bool = String(definition["support"]) == "water_jolt"
	shadow.visible = not water_supported
	waterline.visible = water_supported
	Engine.time_scale = old_time_scale
	main.set_process(original_main_processing)
	paused = old_tree_paused
	body.freeze = original_freeze
	if not original_freeze:
		body.sleeping = false
	var camera: Camera3D = viewport.get_camera_3d()
	var screen_point: Vector2 = camera.unproject_position(node.global_position)
	var support: String = String(definition["support"])
	var support_rect: Rect2 = SkyLagoonPromenade.ANIMAL_SUPPORT_RECTS[
		String(definition["support_zone"])] as Rect2
	var support_point: Vector2 = Vector2(body.position.x, body.position.y) \
		if support == "water_jolt" else Vector2(body.position.x,
			body.position.y - float(definition["height"]) * 0.5)
	var solver_span: float = 0.0
	if support == "water_jolt":
		solver_span = float(body.get("max_solver_y")) \
			- float(body.get("min_solver_y"))
	capture_manifest.append({
		"id": String(definition["id"]),
		"habitat": String(definition["habitat"]),
		"lighting": "night" if main.is_night else "day",
		"support": support,
		"support_zone": String(definition["support_zone"]),
		"support_point": [support_point.x, support_point.y],
		"support_rect": [support_rect.position.x, support_rect.position.y,
			support_rect.size.x, support_rect.size.y],
		"with": with_path.get_file(),
		"without": without_path.get_file(),
		"screen_point": [screen_point.x, screen_point.y],
		"body_position": [body.position.x, body.position.y, body.position.z],
		"physics_engine": String(ProjectSettings.get_setting("physics/3d/physics_engine")),
		"body_frozen": body.freeze,
		"water_enabled": bool(body.get("water_enabled")),
		"solver_steps": int(body.get("solver_steps")),
		"solver_bob_span": solver_span,
		"waterline_visible": waterline.visible,
		"shadow_visible": shadow.visible,
		"world_height": float(definition["height"]),
		"modulate": _color_values(node.modulate),
		"shadow_modulate": _color_values(shadow.modulate),
	})


func _capture_refuge_review(label: String, actor: Dictionary,
		definition: Dictionary) -> void:
	var out_dir: String = OS.get_environment("LAGOON_ANIMAL_SHOT_OUT")
	if out_dir == "":
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	var node: Sprite3D = actor["node"] as Sprite3D
	var body: RigidBody3D = actor["body"] as RigidBody3D
	var refuge_fx: Sprite3D = actor["refuge_fx"] as Sprite3D
	var old_hud_visible: bool = main.hud_msg.visible
	var old_tree_paused: bool = paused
	main.hud_msg.visible = false
	paused = true
	_stage_capture_camera(int(definition["page"]))
	var old_time_scale: float = Engine.time_scale
	Engine.time_scale = 0.0
	await process_frame
	main.hud_msg.visible = false
	_stage_capture_camera(int(definition["page"]))
	RenderingServer.force_draw(false)
	var viewport: Viewport = get_root().get_viewport()
	var image: Image = viewport.get_texture().get_image()
	var path: String = out_dir.path_join(label + "_refuge.png")
	if image == null:
		_check("capture_%s_refuge_render_target" % label, false)
		Engine.time_scale = old_time_scale
		main.hud_msg.visible = old_hud_visible
		paused = old_tree_paused
		return
	_check("capture_%s_refuge" % label, image.save_png(path) == OK)
	var camera: Camera3D = viewport.get_camera_3d()
	var refuge_point: Vector3 = definition["refuge_point"] as Vector3
	var stage_root: Node3D = main.g["ss_root"] as Node3D
	var screen_point: Vector2 = camera.unproject_position(
		stage_root.to_global(refuge_point))
	refuge_manifest.append({
		"id": String(definition["id"]),
		"refuge_kind": String(definition["refuge_kind"]),
		"file": path.get_file(),
		"screen_point": [screen_point.x, screen_point.y],
		"refuge_point": [refuge_point.x, refuge_point.y, refuge_point.z],
		"body_position": [body.position.x, body.position.y, body.position.z],
		"effect_visible": refuge_fx.visible,
		"effect_played": bool(actor.get("refuge_effect_played", false)),
		"state": String(actor.get("state", "")),
	})
	Engine.time_scale = old_time_scale

	main.hud_msg.visible = old_hud_visible
	paused = old_tree_paused


func _write_capture_manifest() -> void:
	var out_dir: String = OS.get_environment("LAGOON_ANIMAL_SHOT_OUT")
	if out_dir == "":
		return
	var file: FileAccess = FileAccess.open(
		out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	_check("capture_manifest_open", file != null)
	if file != null:
		file.store_string(JSON.stringify({"captures": capture_manifest,
			"refuges": refuge_manifest}, "\t") + "\n")


func _move_to_page(page: int) -> void:
	main.g["lagoon_castle_armed"] = false
	main.g["ss_walk_goal"] = null
	var page_x: float = float(SkyLagoonPromenade.ANIMAL_PAGE_CENTERS[page])
	main.player.position.x = main.LEVEL2_POS.x + page_x
	var camera: Camera3D = main.player.cam
	camera.position = main.LEVEL2_POS + Vector3(
		page_x, SkyLagoonPromenade.CAM_H, SkyLagoonPromenade.CAM_DIST)
	camera.look_at(main.LEVEL2_POS + Vector3(
		page_x, SkyLagoonPromenade.CAM_H, 0.0))
	await _frames(4)


func _animal_nodes(root: Node) -> Array[Sprite3D]:
	var result: Array[Sprite3D] = []
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		if node is Sprite3D and String(
				(node as Sprite3D).get_meta("ambient_kind", "")) == "animal":
			result.append(node as Sprite3D)
		for child: Node in node.get_children():
			stack.append(child)
	return result


func _animal_water_bodies(root: Node) -> Array[RigidBody3D]:
	var result: Array[RigidBody3D] = []
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		if node is RigidBody3D and String(
				(node as RigidBody3D).get_meta("support_medium", "")) == "water":
			result.append(node as RigidBody3D)
		for child: Node in node.get_children():
			stack.append(child)
	return result


func _validate_roster(promenade: SkyLagoonPromenade) -> void:
	var definitions: Array = main.g.get("lagoon_animals", [])
	_check("roster_count", definitions.size() == 5,
		"count=%d" % definitions.size())
	var ids: Dictionary = {}
	var page_counts := {0: 0, 1: 0, 2: 0}
	var paths_safe: bool = true
	var atlas_contract_ok: bool = true
	var lighting_authored: bool = true
	var support_counts := {"water_jolt": 0, "ground": 0}
	var support_contract_ok: bool = true
	for value: Variant in definitions:
		var definition: Dictionary = value as Dictionary
		var animal_id: String = String(definition.get("id", ""))
		ids[animal_id] = true
		var page: int = int(definition.get("page", -1))
		page_counts[page] = int(page_counts.get(page, 0)) + 1
		paths_safe = paths_safe and promenade._animal_path_is_safe(definition)
		var idle_texture: Texture2D = load(String(definition["idle"])) as Texture2D
		var startle_texture: Texture2D = load(
			String(definition["startle"])) as Texture2D
		atlas_contract_ok = atlas_contract_ok \
			and idle_texture != null and startle_texture != null \
			and idle_texture.get_size() == Vector2(512.0, 512.0) \
			and startle_texture.get_size() == Vector2(512.0, 512.0)
		lighting_authored = lighting_authored \
			and definition.get("day_tint") is Color \
			and definition.get("night_tint") is Color \
			and definition.get("shadow_day") is Color \
			and definition.get("shadow_night") is Color
		var support: String = String(definition.get("support", ""))
		support_counts[support] = int(support_counts.get(support, 0)) + 1
		support_contract_ok = support_contract_ok \
			and SkyLagoonPromenade.ANIMAL_SUPPORT_RECTS.has(
				String(definition.get("support_zone", ""))) \
			and (support != "water_jolt" \
				or definition.get("water_surface_y") is float)
		support_contract_ok = (support_contract_ok
			and definition.get("refuge_point") is Vector3
			and definition.get("refuge_fx_point") is Vector3
			and definition.get("refuge_speed") is float
			and String(definition.get("refuge_kind", "")) in ["brush", "tree"]
			and (String(definition.get("refuge_kind", "")) != "tree"
				or definition.get("refuge_climb_point") is Vector3))
	_check("expected_roster", ids.has_all(EXPECTED_IDS) and not ids.has("fawn"))
	_check("ecological_page_rosters",
		int(page_counts[0]) == 2 and int(page_counts[1]) == 1 \
		and int(page_counts[2]) == 2, str(page_counts))
	_check("authored_paths_clear_route_props_and_seams", paths_safe)
	_check("atlas_contract", atlas_contract_ok)
	_check("authored_day_night_lighting", lighting_authored)
	_check("support_roster_is_two_water_three_ground",
		int(support_counts["water_jolt"]) == 2 \
		and int(support_counts["ground"]) == 3, str(support_counts))
	_check("support_contract_is_explicit", support_contract_ok)


func _validate_day_actor(promenade: SkyLagoonPromenade) -> void:
	var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
	var node: Sprite3D = actor.get("node") as Sprite3D
	var body: RigidBody3D = actor.get("body") as RigidBody3D
	var waterline: Sprite3D = actor.get("waterline") as Sprite3D
	var refuge_fx: Sprite3D = actor.get("refuge_fx") as Sprite3D
	var shadow: Sprite3D = node.get_meta("contact_shadow") as Sprite3D
	var stage_root: Node3D = main.g.get("ss_root") as Node3D
	_check("single_pooled_animal_card", _animal_nodes(stage_root).size() == 1)
	_check("single_pooled_jolt_water_body",
		_animal_water_bodies(stage_root).size() == 1 and body != null \
		and String(body.get_meta("physics_engine", "")) == "Jolt Physics")
	_check("single_pooled_contact_shadow", shadow != null \
		and bool(shadow.get_meta("sky_lagoon_contact_shadow", false)))
	_check("single_pooled_refuge_rustle", refuge_fx != null
		and String(refuge_fx.get_meta("animal_refuge_effect", ""))
			== "brush_rustle")
	var pooled_id: int = node.get_instance_id()
	var pooled_body_id: int = body.get_instance_id()
	for definition: Dictionary in SkyLagoonPromenade.ANIMAL_DEFS:
		var page: int = int(definition["page"])
		await _move_to_page(page)
		_check("bind_%s" % String(definition["id"]),
			promenade._bind_animal_id(String(definition["id"])))
		actor = main.g.get("lagoon_animal_actor", {}) as Dictionary
		node = actor.get("node") as Sprite3D
		body = actor.get("body") as RigidBody3D
		waterline = actor.get("waterline") as Sprite3D
		refuge_fx = actor.get("refuge_fx") as Sprite3D
		shadow = node.get_meta("contact_shadow") as Sprite3D
		var start: Vector3 = body.position
		await _physics_frames(50)
		var moved: Vector3 = actor["route_position"] as Vector3
		_check("%s_idle_follows_habitat" % String(definition["id"]),
			moved.distance_to(start) > 0.05)
		_check("%s_reuses_pool" % String(definition["id"]),
			node.get_instance_id() == pooled_id \
			and body.get_instance_id() == pooled_body_id)
		var support: String = String(definition["support"])
		var support_rect: Rect2 = SkyLagoonPromenade.ANIMAL_SUPPORT_RECTS[
			String(definition["support_zone"])] as Rect2
		var foot := Vector2(body.position.x,
			body.position.y - float(definition["height"]) * 0.5)
		var support_point := Vector2(body.position.x, body.position.y) \
			if support == "water_jolt" else foot
		_check("%s_has_real_support" % String(definition["id"]),
			support_rect.has_point(support_point) \
			and String(node.get_meta("animal_support", "")) == support,
			"point=%s rect=%s" % [support_point, support_rect])
		if support == "water_jolt":
			_check("%s_uses_jolt_buoyancy" % String(definition["id"]),
				String(ProjectSettings.get_setting("physics/3d/physics_engine")) \
					== "Jolt Physics" \
				and not body.freeze and bool(body.get("water_enabled")) \
				and int(body.get("solver_steps")) >= 20 \
				and absf(body.position.y - float(definition["water_surface_y"])) < 0.24 \
				and float(body.get("max_solver_y")) \
					- float(body.get("min_solver_y")) > 0.004,
				"pos=%s surface=%.3f steps=%d span=%.4f freeze=%s enabled=%s" % [
					body.position, float(definition["water_surface_y"]),
					int(body.get("solver_steps")), float(body.get("max_solver_y"))
						- float(body.get("min_solver_y")), body.freeze,
					bool(body.get("water_enabled"))])
			_check("%s_reads_as_in_water" % String(definition["id"]),
				waterline.visible and not shadow.visible \
				and String(waterline.get_meta("animal_support_effect", "")) \
					== "jolt_waterline")
		else:
			_check("%s_is_grounded_not_on_foliage" % String(definition["id"]),
				body.freeze and shadow.visible and not waterline.visible \
				and foot.y <= 0.0)
		_check("%s_render_and_lighting" % String(definition["id"]),
			not node.shaded and node.hframes == 2 and node.vframes == 2 \
			and node.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD \
			and node.modulate.is_equal_approx(definition["day_tint"] as Color) \
			and (support == "water_jolt" or shadow.modulate.is_equal_approx(
				definition["shadow_day"] as Color)) \
			and String(node.get_meta("animal_habitat", "")) \
				== String(definition["habitat"]))
		await _capture_pair("day_%s" % String(definition["id"]), actor, definition)
		var activation_start_x: float = body.position.x
		var expected_refuge_direction: float = signf((definition["refuge_point"] as Vector3).x - activation_start_x)
		promenade._startle_animal(actor)
		promenade._tick_animal_startle(actor, 0.10)
		var alert_frame: int = node.frame
		promenade._tick_animal_startle(actor, 0.20)
		var squash_frame: int = node.frame
		promenade._tick_animal_startle(actor, 0.20)
		var hop_frame: int = node.frame
		promenade._tick_animal_startle(actor, 0.30)
		_check("%s_cute_startle_sequence" % String(definition["id"]),
			(alert_frame == 0 and squash_frame == 1 and hop_frame == 2
			and String(actor["state"]) in ["startle", "refuge"]
			and is_equal_approx(float(actor["refuge_direction"]),
				expected_refuge_direction)
			and (support != "water_jolt"
				or bool(body.get("received_escape_impulse")))))

		_check("rebind_%s_for_refuge" % String(definition["id"]),
			promenade._bind_animal_id(String(definition["id"])))
		actor = main.g.get("lagoon_animal_actor", {}) as Dictionary
		node = actor["node"] as Sprite3D
		body = actor["body"] as RigidBody3D
		promenade._startle_animal(actor)
		var refuge_reviewed: bool = false
		for _step: int in range(600):
			await physics_frame
			if String(actor["state"]) == "refuge":
				var refuge_duration: float = SkyLagoonPromenade.ANIMAL_TREE_CLIMB_S \
					if String(definition["refuge_kind"]) == "tree" \
					else SkyLagoonPromenade.ANIMAL_BRUSH_ENTRY_S
				var review_fraction: float = 0.62 \
					if String(definition["refuge_kind"]) == "tree" else 0.45
				if not refuge_reviewed and float(actor["state_t"]) >= refuge_duration * review_fraction:
					await _capture_refuge_review("day_%s" % String(definition["id"]),
						actor, definition)
					refuge_reviewed = true
			if String(actor["state"]) == "hidden":
				break
		var refuge_point: Vector3 = definition["refuge_point"] as Vector3
		var entry_position: Vector3 = actor["refuge_entry_position"] as Vector3
		var entry_support: Vector2
		if support == "water_jolt":
			entry_support = Vector2(entry_position.x, entry_position.y)
		else:
			entry_support = Vector2(entry_position.x,
				entry_position.y - float(definition["height"]) * 0.5)
		var camera: Camera3D = main.player.cam
		var refuge_screen: Vector2 = camera.unproject_position(
			stage_root.to_global(refuge_point))
		var inner_viewport: Rect2 = main.get_viewport().get_visible_rect().grow(-32.0)
		var page_center: float = float(SkyLagoonPromenade.ANIMAL_PAGE_CENTERS[page])
		var screen_safe: bool = absf(refuge_point.x - page_center) <= 23.5
		if DisplayServer.get_name() != "headless":
			screen_safe = inner_viewport.has_point(refuge_screen)
		_check("%s_activation_reaches_authored_refuge" % String(definition["id"]),
			String(actor["state"]) == "hidden" and refuge_reviewed
			and bool(actor.get("refuge_contacted", false))
			and bool(actor.get("refuge_completed", false))
			and entry_position.distance_to(refuge_point) <= 0.28)
		_check("%s_refuge_stays_on_screen_and_in_medium" % String(definition["id"]),
			screen_safe
			and support_rect.has_point(entry_support),
			"screen=%s entry=%s support=%s" % [
				refuge_screen, entry_support, support_rect])
		_check("%s_refuge_disrupts_foliage" % String(definition["id"]),
			bool(actor.get("refuge_effect_played", false)))
		if String(definition["refuge_kind"]) == "tree":
			var climb_point: Vector3 = definition["refuge_climb_point"] as Vector3
			_check("%s_climbs_existing_tree" % String(definition["id"]),
				body.position.distance_to(climb_point) <= 0.15
				and climb_point.y - refuge_point.y >= 5.0)


func _validate_continuity(promenade: SkyLagoonPromenade) -> void:
	await _move_to_page(0)
	var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
	_check("shore_starts_with_otter", promenade._bind_next_animal(0) \
		and String((actor["definition"] as Dictionary)["id"]) == "otter")
	var fake_plane := Sprite3D.new()
	main.g["lagoon_plane_card"] = fake_plane
	promenade._tick_animals(0.1)
	_check("arrival_plane_excludes_shore_animals",
		String(actor["state"]) == "hidden" and not (actor["node"] as Sprite3D).visible)
	main.g["lagoon_plane_card"] = null
	fake_plane.free()
	actor["spawn_t"] = 0.0
	promenade._tick_animals(0.05)
	_check("shore_returns_after_plane_departure",
		String(actor["state"]) in ["idle", "pause"] \
		and (actor["node"] as Sprite3D).visible)
	promenade._startle_animal(actor)
	for _step: int in range(360):
		await physics_frame
		if String(actor["state"]) == "hidden":
			break
	_check("activation_resolves_into_shoreline_refuge",
		String(actor["state"]) == "hidden" \
		and not (actor["node"] as Sprite3D).visible \
		and bool((actor["body"] as RigidBody3D).get("received_escape_impulse")) \
		and bool(actor.get("refuge_contacted", false)) \
		and bool(actor.get("refuge_effect_played", false)) \
		and bool(actor.get("refuge_completed", false)))
	actor["spawn_t"] = 0.0
	promenade._tick_animals(0.05)
	_check("shore_roster_advances_otter_to_frog",
		String((actor["definition"] as Dictionary)["id"]) == "frog",
		"active=%s page=%d camera_page=%d" % [
			String((actor["definition"] as Dictionary)["id"]),
			int(actor["page"]), promenade._animal_page_index()])


func _validate_night(promenade: SkyLagoonPromenade) -> void:
	for definition: Dictionary in SkyLagoonPromenade.ANIMAL_DEFS:
		await _move_to_page(int(definition["page"]))
		promenade._bind_animal_id(String(definition["id"]))
		var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
		var node: Sprite3D = actor["node"] as Sprite3D
		var waterline: Sprite3D = actor["waterline"] as Sprite3D
		var shadow: Sprite3D = node.get_meta("contact_shadow") as Sprite3D
		var water_supported: bool = String(definition["support"]) == "water_jolt"
		if water_supported:
			await _physics_frames(50)
		_check("%s_night_lighting" % String(definition["id"]),
			node.modulate.is_equal_approx(definition["night_tint"] as Color) \
			and (water_supported and waterline.visible and not shadow.visible \
				or not water_supported and shadow.modulate.is_equal_approx(
					definition["shadow_night"] as Color)) \
			and String(node.get_meta("animal_lighting_profile", "")) == "night")
		await _capture_pair("night_%s" % String(definition["id"]), actor, definition)


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	if main.intro_active:
		main._skip_intro()
	main._apply_quality("speedy")
	main._set_night(false)
	main.save_data["lagoon_plane_departed"] = true
	main._enter_level2_now(true, false, false)
	await _frames(45)

	var promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
	_validate_roster(promenade)
	await _validate_day_actor(promenade)
	await _validate_continuity(promenade)

	main._exit_level2_now()
	await _frames(5)
	main.is_night = true
	main._enter_level2_now(true, false, false)
	await _frames(45)
	promenade = main._lagoon_promenade_ref()
	await _validate_night(promenade)
	_write_capture_manifest()

	print("SKY_LAGOON_ANIMALS|ALL OK" if failures == 0 \
		else "SKY_LAGOON_ANIMALS|FAIL|count=%d" % failures)
	quit(0 if failures == 0 else 1)
