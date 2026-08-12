extends SceneTree

# Acceptance probe for the authored Sky Lagoon animal habitat system.
# Set LAGOON_ANIMAL_SHOT_OUT to capture paired Mobile-renderer frames with and
# without each animal for the pixel-level lighting audit.

const EXPECTED_IDS := ["hare", "squirrel", "raccoon", "otter", "frog"]

var failures: int = 0
var main: ReefMain
var capture_manifest: Array[Dictionary] = []


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


func _color_values(color: Color) -> Array[float]:
	return [color.r, color.g, color.b, color.a]


func _capture_pair(label: String, actor: Dictionary,
		definition: Dictionary) -> void:
	var out_dir: String = OS.get_environment("LAGOON_ANIMAL_SHOT_OUT")
	if out_dir == "":
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	var node: Sprite3D = actor.get("node") as Sprite3D
	var shadow: Sprite3D = node.get_meta("contact_shadow") as Sprite3D
	var old_mode: Node.ProcessMode = main.process_mode
	main.process_mode = Node.PROCESS_MODE_DISABLED
	await process_frame
	await RenderingServer.frame_post_draw
	var viewport: Viewport = get_root().get_viewport()
	var with_image: Image = viewport.get_texture().get_image()
	var with_path: String = out_dir.path_join(label + "_with.png")
	_check("capture_%s_with" % label, with_image.save_png(with_path) == OK)
	node.visible = false
	shadow.visible = false
	await process_frame
	await RenderingServer.frame_post_draw
	var without_image: Image = viewport.get_texture().get_image()
	var without_path: String = out_dir.path_join(label + "_without.png")
	_check("capture_%s_without" % label,
		without_image.save_png(without_path) == OK)
	node.visible = true
	shadow.visible = true
	main.process_mode = old_mode
	var camera: Camera3D = viewport.get_camera_3d()
	var screen_point: Vector2 = camera.unproject_position(node.global_position)
	capture_manifest.append({
		"id": String(definition["id"]),
		"habitat": String(definition["habitat"]),
		"lighting": "night" if main.is_night else "day",
		"with": with_path.get_file(),
		"without": without_path.get_file(),
		"screen_point": [screen_point.x, screen_point.y],
		"world_height": float(definition["height"]),
		"modulate": _color_values(node.modulate),
		"shadow_modulate": _color_values(shadow.modulate),
	})


func _write_capture_manifest() -> void:
	var out_dir: String = OS.get_environment("LAGOON_ANIMAL_SHOT_OUT")
	if out_dir == "":
		return
	var file: FileAccess = FileAccess.open(
		out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	_check("capture_manifest_open", file != null)
	if file != null:
		file.store_string(JSON.stringify({"captures": capture_manifest}, "\t") + "\n")


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


func _validate_roster(promenade: SkyLagoonPromenade) -> void:
	var definitions: Array = main.g.get("lagoon_animals", [])
	_check("roster_count", definitions.size() == 5,
		"count=%d" % definitions.size())
	var ids: Dictionary = {}
	var page_counts := {0: 0, 1: 0, 2: 0}
	var paths_safe: bool = true
	var atlas_contract_ok: bool = true
	var lighting_authored: bool = true
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
	_check("expected_roster", ids.has_all(EXPECTED_IDS) and not ids.has("fawn"))
	_check("ecological_page_rosters",
		int(page_counts[0]) == 2 and int(page_counts[1]) == 2 \
		and int(page_counts[2]) == 1, str(page_counts))
	_check("authored_paths_clear_route_props_and_seams", paths_safe)
	_check("atlas_contract", atlas_contract_ok)
	_check("authored_day_night_lighting", lighting_authored)


func _validate_day_actor(promenade: SkyLagoonPromenade) -> void:
	var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
	var node: Sprite3D = actor.get("node") as Sprite3D
	var shadow: Sprite3D = node.get_meta("contact_shadow") as Sprite3D
	var stage_root: Node3D = main.g.get("ss_root") as Node3D
	_check("single_pooled_animal_card", _animal_nodes(stage_root).size() == 1)
	_check("single_pooled_contact_shadow", shadow != null \
		and bool(shadow.get_meta("sky_lagoon_contact_shadow", false)))
	var pooled_id: int = node.get_instance_id()
	for definition: Dictionary in SkyLagoonPromenade.ANIMAL_DEFS:
		var page: int = int(definition["page"])
		await _move_to_page(page)
		_check("bind_%s" % String(definition["id"]),
			promenade._bind_animal_id(String(definition["id"])))
		actor = main.g.get("lagoon_animal_actor", {}) as Dictionary
		node = actor.get("node") as Sprite3D
		shadow = node.get_meta("contact_shadow") as Sprite3D
		var start: Vector3 = actor["route_position"] as Vector3
		promenade._tick_animal_idle(actor, 0.6)
		var moved: Vector3 = actor["route_position"] as Vector3
		_check("%s_idle_follows_habitat" % String(definition["id"]),
			moved.distance_to(start) > 0.05)
		_check("%s_reuses_pool" % String(definition["id"]),
			node.get_instance_id() == pooled_id)
		_check("%s_render_and_lighting" % String(definition["id"]),
			not node.shaded and node.hframes == 2 and node.vframes == 2 \
			and node.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD \
			and node.modulate.is_equal_approx(definition["day_tint"] as Color) \
			and shadow.modulate.is_equal_approx(definition["shadow_day"] as Color) \
			and String(node.get_meta("animal_habitat", "")) \
				== String(definition["habitat"]))
		await _capture_pair("day_%s" % String(definition["id"]), actor, definition)
		promenade._startle_animal(actor)
		promenade._tick_animal_startle(actor, 0.10)
		var alert_frame: int = node.frame
		promenade._tick_animal_startle(actor, 0.20)
		var squash_frame: int = node.frame
		promenade._tick_animal_startle(actor, 0.20)
		var hop_frame: int = node.frame
		promenade._tick_animal_startle(actor, 0.30)
		_check("%s_cute_startle_sequence" % String(definition["id"]),
			alert_frame == 0 and squash_frame == 1 and hop_frame == 2 \
			and String(actor["state"]) == "startle" \
			and float(actor["exit_direction"]) == float(definition["safe_exit"]))


func _validate_continuity(promenade: SkyLagoonPromenade) -> void:
	await _move_to_page(0)
	var reef_route: Sprite3D = main.g.get("lagoon_reef_route_card") as Sprite3D
	var route_base: Vector3 = main.g.get(
		"lagoon_reef_route_base", Vector3.ZERO) as Vector3
	var route_bottom: float = route_base.y \
		- SkyLagoonPromenade.REEF_ROUTE_MARKER_H * 0.5 - 0.12
	var shore_top := -INF
	for definition: Dictionary in SkyLagoonPromenade.ANIMAL_DEFS:
		if int(definition["page"]) != 0:
			continue
		for point_value in (definition["path"] as Array):
			var point: Vector3 = point_value as Vector3
			shore_top = maxf(shore_top, point.y
				+ float(definition["height"]) * 0.5
				+ float(definition["bob"]))
	_check("reef_route_clears_shore_animals",
		reef_route != null and is_instance_valid(reef_route)
		and route_base.x >= -66.0 and route_bottom - shore_top >= 0.5,
		"route_base=%s vertical_gap=%.2f" % [route_base, route_bottom - shore_top])
	var route_screen: Vector2 = main.player.cam.unproject_position(
		reef_route.global_position) if reef_route != null else Vector2(-1.0, -1.0)
	_check("reef_route_visible_from_arrival_page",
		Rect2(Vector2.ZERO, main.get_viewport().get_visible_rect().size).has_point(
			route_screen), "screen=%s" % route_screen)
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
	var roshan_card: Sprite3D = main.g.get("lagoon_roshan_card") as Sprite3D
	var celebration_count: int = int(
		main.g.get("lagoon_visible_roshan_celebrations", 0))
	main.player.verb = ""
	promenade._startle_animal(actor)
	_check("animal_celebrates_on_visible_roshan_card",
		roshan_card != null and roshan_card.visible and not main.player.visible
		and not roshan_card.scale.is_equal_approx(Vector3.ONE)
		and int(main.g.get("lagoon_visible_roshan_celebrations", 0)) \
			== celebration_count + 1
		and main.player.verb != "giggle")
	for _step: int in range(240):
		promenade._tick_animal_startle(actor, 0.05)
		if String(actor["state"]) == "hidden":
			break
	_check("activation_exits_toward_safe_edge",
		String(actor["state"]) == "hidden" and not (actor["node"] as Sprite3D).visible)
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
		var shadow: Sprite3D = node.get_meta("contact_shadow") as Sprite3D
		_check("%s_night_lighting" % String(definition["id"]),
			node.modulate.is_equal_approx(definition["night_tint"] as Color) \
			and shadow.modulate.is_equal_approx(
				definition["shadow_night"] as Color) \
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
