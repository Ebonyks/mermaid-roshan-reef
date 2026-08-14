extends SceneTree
# Acceptance probe for the authored five-species Canvas habitat system.
# Optional paired captures use the production Camera2D/viewport composition.

const EXPECTED_IDS: Array[String] = [
	"frog", "hare", "otter", "raccoon", "squirrel",
]
const PAGE_CENTERS: Array[float] = [1024.0, 3072.0, 5120.0]
const REVIEW_ROUTE_X := {
	"otter": 610.0,
	"frog": 610.0,
	"hare": 2300.0,
	"squirrel": 2300.0,
	"raccoon": 4510.0,
}

var failures := 0
var main: ReefMain
var promenade: SkyLagoonPromenade
var capture_manifest: Array[Dictionary] = []


func _check(label: String, condition: bool, detail: String = "") -> void:
	print("LAGOONANIMALS|%s|%s%s" % [
		label,
		"OK" if condition else "FAIL",
		"" if detail == "" else "|" + detail,
	])
	if not condition:
		failures += 1


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _color_values(color: Color) -> Array[float]:
	return [color.r, color.g, color.b, color.a]


func _atlas_frame(node: Sprite2D) -> int:
	if node == null or not node.region_enabled \
			or node.region_rect.size.x <= 0.0 or node.region_rect.size.y <= 0.0:
		return node.frame if node != null else -1
	var column: int = roundi(node.region_rect.position.x / node.region_rect.size.x)
	var row: int = roundi(node.region_rect.position.y / node.region_rect.size.y)
	return row * SkyLagoonPromenade.ANIMAL_ATLAS_COLUMNS + column


func _alpha_screen_rect(sprite: Sprite2D) -> Rect2:
	if sprite == null or not is_instance_valid(sprite) or not sprite.visible \
			or sprite.texture == null:
		return Rect2()
	var image: Image = sprite.texture.get_image()
	if image == null or image.is_empty():
		return Rect2()
	if image.is_compressed() and image.decompress() != OK:
		return Rect2()
	var source := Rect2i(Vector2i.ZERO, image.get_size())
	if sprite.region_enabled:
		source = Rect2i(sprite.region_rect)
	var alpha_min := Vector2i(source.size)
	var alpha_max := Vector2i(-1, -1)
	for y: int in range(source.position.y, source.end.y):
		for x: int in range(source.position.x, source.end.x):
			if image.get_pixel(x, y).a >= 0.10:
				var local := Vector2i(x, y) - source.position
				alpha_min.x = mini(alpha_min.x, local.x)
				alpha_min.y = mini(alpha_min.y, local.y)
				alpha_max.x = maxi(alpha_max.x, local.x)
				alpha_max.y = maxi(alpha_max.y, local.y)
	if alpha_max.x < alpha_min.x or alpha_max.y < alpha_min.y:
		return Rect2()
	var used := Rect2i(alpha_min, alpha_max - alpha_min + Vector2i.ONE)
	var draw_size := Vector2(source.size)
	var local_origin := Vector2(used.position) + sprite.offset
	if sprite.centered:
		local_origin -= draw_size * 0.5
	var local_size := Vector2(used.size)
	var transform: Transform2D = sprite.get_global_transform_with_canvas()
	var corners: Array[Vector2] = [
		transform * local_origin,
		transform * (local_origin + Vector2(local_size.x, 0.0)),
		transform * (local_origin + local_size),
		transform * (local_origin + Vector2(0.0, local_size.y)),
	]
	var bounds := Rect2(corners[0], Vector2.ZERO)
	for corner: Vector2 in corners:
		bounds = bounds.expand(corner)
	return bounds


func _overlap_fraction(first: Rect2, second: Rect2) -> float:
	if first.get_area() <= 0.0 or second.get_area() <= 0.0:
		return 0.0
	return first.intersection(second).get_area() / minf(first.get_area(), second.get_area())


func _production_hit_radius_ok(actor: Dictionary, center: Vector2) -> bool:
	var expected_id: String = String((actor.get("definition", {}) as Dictionary).get("id", ""))
	for offset: Vector2 in [
		Vector2.ZERO, Vector2(110.0, 0.0), Vector2(-110.0, 0.0),
		Vector2(0.0, 110.0), Vector2(0.0, -110.0),
	]:
		var hit: Dictionary = promenade._animal_at(center + offset)
		if String((hit.get("definition", {}) as Dictionary).get("id", "")) != expected_id:
			return false
	return true


func _animal_clear_of_actor_and_props(node: Sprite2D) -> bool:
	return _animal_max_overlap(node) <= 0.20


func _animal_max_overlap(node: Sprite2D) -> float:
	var animal_rect: Rect2 = _alpha_screen_rect(node)
	var roshan: Sprite2D = main.g.get("lagoon_roshan_card") as Sprite2D
	var highest: float = _overlap_fraction(animal_rect, _alpha_screen_rect(roshan))
	for value: Variant in main.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		var prop: Sprite2D = target.get("node") as Sprite2D
		if prop != null:
			highest = maxf(highest, _overlap_fraction(
				animal_rect, _alpha_screen_rect(prop)))
	return highest


func _animal_nodes(root_node: Node) -> Array[Sprite2D]:
	var result: Array[Sprite2D] = []
	var stack: Array[Node] = [root_node]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		if node is Sprite2D and String(
				(node as Sprite2D).get_meta("ambient_kind", "")) == "animal":
			result.append(node as Sprite2D)
		for child: Node in node.get_children():
			stack.append(child)
	return result


func _move_to_page(page: int) -> void:
	main.g["lagoon_castle_armed"] = false
	main.g["lagoon_walk_goal_master"] = null
	var center_x: float = PAGE_CENTERS[page]
	promenade.set_master_route_x(center_x)
	await _frames(4)


func _capture_pair(label: String, actor: Dictionary,
		definition: Dictionary) -> void:
	var out_dir := OS.get_environment("LAGOON_ANIMAL_SHOT_OUT")
	if out_dir == "":
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	var node: Sprite2D = actor.get("node") as Sprite2D
	var shadow: Sprite2D = node.get_meta("contact_shadow") as Sprite2D \
		if node != null and node.has_meta("contact_shadow") else null
	var old_mode: Node.ProcessMode = main.process_mode
	main.process_mode = Node.PROCESS_MODE_DISABLED
	await process_frame
	await RenderingServer.frame_post_draw
	var image_with: Image = get_root().get_texture().get_image()
	var with_path := out_dir.path_join(label + "_with.png")
	_check("capture_%s_with" % label, image_with.save_png(with_path) == OK)
	node.visible = false
	if shadow != null:
		shadow.visible = false
	await process_frame
	await RenderingServer.frame_post_draw
	var image_without: Image = get_root().get_texture().get_image()
	var without_path := out_dir.path_join(label + "_without.png")
	_check("capture_%s_without" % label,
		image_without.save_png(without_path) == OK)
	node.visible = true
	if shadow != null:
		shadow.visible = true
	main.process_mode = old_mode
	var screen_point: Vector2 = node.get_global_transform_with_canvas().origin
	capture_manifest.append({
		"id": String(definition["id"]),
		"habitat": String(definition["habitat"]),
		"lighting": "night" if main.is_night else "day",
		"with": with_path.get_file(),
		"without": without_path.get_file(),
		"screen_point": [screen_point.x, screen_point.y],
		"master_height": float(definition["height"]),
		"modulate": _color_values(node.modulate),
		"shadow_modulate": _color_values(shadow.modulate) if shadow != null else [],
	})


func _write_capture_manifest() -> void:
	var out_dir := OS.get_environment("LAGOON_ANIMAL_SHOT_OUT")
	if out_dir == "":
		return
	var file: FileAccess = FileAccess.open(
		out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	_check("capture_manifest_open", file != null)
	if file != null:
		file.store_string(JSON.stringify({"captures": capture_manifest}, "\t") + "\n")


func _validate_roster() -> void:
	var definitions: Array = main.g.get("lagoon_animals", []) as Array
	var ids: Array[String] = []
	var page_counts := {0: 0, 1: 0, 2: 0}
	var paths_safe := true
	var atlases_ok := true
	var lighting_ok := true
	for value: Variant in definitions:
		var definition: Dictionary = value as Dictionary
		ids.append(String(definition.get("id", "")))
		var page: int = int(definition.get("page", -1))
		page_counts[page] = int(page_counts.get(page, 0)) + 1
		paths_safe = paths_safe and promenade._animal_path_is_safe(definition)
		var idle: Texture2D = load(String(definition.get("idle", ""))) as Texture2D
		var startle: Texture2D = load(
			String(definition.get("startle", ""))) as Texture2D
		atlases_ok = atlases_ok and idle != null and startle != null \
			and idle.get_size() == Vector2(512.0, 512.0) \
			and startle.get_size() == Vector2(512.0, 512.0)
		lighting_ok = lighting_ok and definition.get("day_tint") is Color \
			and definition.get("night_tint") is Color
	ids.sort()
	_check("exact_five_species_roster", definitions.size() == 5 and ids == EXPECTED_IDS)
	_check("ecological_page_rosters", int(page_counts[0]) == 2
		and int(page_counts[1]) == 2 and int(page_counts[2]) == 1,
		str(page_counts))
	_check("authored_paths_clear_route_props_and_seams", paths_safe)
	_check("animal_atlas_contract", atlases_ok)
	_check("authored_day_night_lighting", lighting_ok)


func _validate_day_actor() -> void:
	var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
	var node: Sprite2D = actor.get("node") as Sprite2D
	var shadow: Sprite2D = node.get_meta("contact_shadow") as Sprite2D \
		if node != null else null
	_check("single_pooled_canvas_animal",
		node != null and _animal_nodes(promenade.root()).size() == 1)
	_check("single_pooled_canvas_contact_shadow",
		shadow != null and String(shadow.get_meta("canvas_layer_role", "")) != "")
	var pooled_id: int = node.get_instance_id() if node != null else -1
	for definition: Dictionary in SkyLagoonPromenade.ANIMAL_DEFS:
		var animal_id := String(definition["id"])
		promenade.set_master_route_x(float(REVIEW_ROUTE_X[animal_id]))
		await _frames(4)
		_check("bind_%s" % animal_id, promenade._bind_animal_id(animal_id))
		actor = main.g.get("lagoon_animal_actor", {}) as Dictionary
		node = actor.get("node") as Sprite2D
		shadow = node.get_meta("contact_shadow") as Sprite2D
		var start: Vector2 = actor.get("route_position", Vector2.ZERO) as Vector2
		promenade._tick_animals(0.6)
		var moved: Vector2 = actor.get("route_position", Vector2.ZERO) as Vector2
		var screen: Vector2 = promenade.screen_from_master(node.position)
		var visual_bounds: Rect2 = _alpha_screen_rect(node)
		var max_overlap: float = _animal_max_overlap(node)
		_check("%s_reuses_canvas_pool" % animal_id,
			node.get_instance_id() == pooled_id and node is Sprite2D \
			and shadow is Sprite2D)
		_check("%s_idle_path_and_production_touch" % animal_id,
			moved.distance_to(start) > 0.05 \
			and _production_hit_radius_ok(actor, screen))
		_check("%s_actual_phone_readability_and_clear_staging" % animal_id,
			minf(visual_bounds.size.x, visual_bounds.size.y) >= 64.0 \
			and max_overlap <= 0.20,
			"bounds=%s overlap=%.3f" % [visual_bounds, max_overlap])
		_check("%s_canvas_metadata_and_lighting" % animal_id,
			node.region_enabled and node.region_rect.size == Vector2(256.0, 256.0) \
			and node.modulate.is_equal_approx(definition["day_tint"] as Color) \
			and shadow != null and shadow.modulate.a > 0.0 \
			and String(node.get_meta("animal_id", "")) == animal_id \
			and String(node.get_meta("animal_lighting_profile", "")) \
				== "canvas_day_night_tint" \
			and String(node.get_meta("canvas_layer_role", "")) != "" \
			and bool(node.get_meta("source_owned", false)) \
			and float(node.get_meta("touch_footprint_px", 0.0)) >= 228.0 \
			and SkyLagoonPromenade.ANIMAL_TOUCH_RADIUS_PX >= 110.0)
		await _capture_pair("day_%s" % animal_id, actor, definition)
		promenade._startle_animal(actor)
		promenade._tick_animals(0.10)
		var alert_frame: int = _atlas_frame(node)
		promenade._tick_animals(0.20)
		var squash_frame: int = _atlas_frame(node)
		promenade._tick_animals(0.20)
		var hop_frame: int = _atlas_frame(node)
		_check("%s_cute_startle_sequence" % animal_id,
			alert_frame == 0 and squash_frame == 1 and hop_frame == 2 \
			and String(actor.get("state", "")) == "startle")


func _validate_continuity() -> void:
	await _move_to_page(0)
	var route: Sprite2D = main.g.get("lagoon_reef_route_card") as Sprite2D
	var route_screen: Vector2 = route.get_global_transform_with_canvas().origin \
		if route != null else Vector2(-1.0, -1.0)
	_check("reef_route_visible_from_arrival_page",
		route != null and Rect2(Vector2.ZERO,
			get_root().get_visible_rect().size).has_point(route_screen))
	var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
	_check("shore_starts_with_otter", promenade._bind_next_animal(0)
		and String((actor.get("definition", {}) as Dictionary).get("id", "")) == "otter")
	main.save_data["lagoon_plane_departed"] = false
	promenade._hide_animal(actor, 0.0, false)
	_check("arrival_plane_excludes_shore_animals",
		not promenade._bind_animal_id("otter") \
		and String(actor.get("state", "")) == "hidden" \
		and not (actor.get("node") as Sprite2D).visible)
	main.save_data["lagoon_plane_departed"] = true
	_check("shore_returns_after_plane_departure_bind",
		promenade._bind_animal_id("otter"))
	_check("shore_returns_after_plane_departure",
		String(actor.get("state", "")) in ["idle", "pause"]
		and (actor.get("node") as Sprite2D).visible)
	promenade._startle_animal(actor)
	for _step: int in range(240):
		promenade._tick_animals(0.05)
		if String(actor.get("state", "")) == "hidden":
			break
	_check("activation_exits_toward_safe_edge",
		String(actor.get("state", "")) == "hidden"
		and not (actor.get("node") as Sprite2D).visible)
	actor["spawn_t"] = 0.0
	promenade._tick_animals(0.05)
	_check("shore_roster_advances_otter_to_frog",
		String((actor.get("definition", {}) as Dictionary).get("id", "")) == "frog")


func _validate_night() -> void:
	for definition: Dictionary in SkyLagoonPromenade.ANIMAL_DEFS:
		var animal_id := String(definition["id"])
		promenade.set_master_route_x(float(REVIEW_ROUTE_X[animal_id]))
		await _frames(4)
		promenade._bind_animal_id(animal_id)
		var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
		var node: Sprite2D = actor.get("node") as Sprite2D
		var shadow: Sprite2D = node.get_meta("contact_shadow") as Sprite2D
		_check("%s_night_lighting" % String(definition["id"]),
			node.modulate.is_equal_approx(definition["night_tint"] as Color) \
			and shadow.modulate.a > 0.0 \
			and String(node.get_meta("animal_lighting_profile", "")) \
				== "canvas_day_night_tint")
		await _capture_pair("night_%s" % String(definition["id"]), actor, definition)


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	get_root().size = Vector2i(1280, 720)
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
	await _frames(24)
	promenade = main._lagoon_promenade_ref()
	_validate_roster()
	await _validate_day_actor()
	await _validate_continuity()
	main._exit_level2_now()
	await _frames(5)
	main.is_night = true
	main._enter_level2_now(true, false, false)
	await _frames(24)
	promenade = main._lagoon_promenade_ref()
	await _validate_night()
	_write_capture_manifest()
	print("SKY_LAGOON_ANIMALS|ALL OK" if failures == 0 \
		else "SKY_LAGOON_ANIMALS|FAIL|count=%d" % failures)
	quit(0 if failures == 0 else 1)
