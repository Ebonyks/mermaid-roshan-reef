extends SceneTree
# Focused acceptance probe for Sky Lagoon's two Canvas living systems: authored
# depth/parallax cards inside the stage and the quiet layer-6 global accents.

var failures := 0
var main: ReefMain
var promenade: SkyLagoonPromenade


func _check(label: String, condition: bool, detail: String = "") -> void:
	print("LIVINGCARD|%s|%s%s" % [
		label,
		"OK" if condition else "FAIL",
		"" if detail == "" else "|" + detail,
	])
	if not condition:
		failures += 1


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _capture(name: String) -> void:
	var out_dir := OS.get_environment("LIVING_CARD_SHOT_OUT")
	if out_dir == "":
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	_check("capture_%s" % name,
		image.save_jpg(out_dir.path_join(name + ".jpg"), 0.92) == OK)


func _hide_interface() -> void:
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.touch_ui != null:
		main.touch_ui.visible = false
	if main.pause_layer != null:
		main.pause_layer.visible = false


func _ambient_signature(cards: Array) -> String:
	var parts: Array[String] = []
	for value: Variant in cards:
		var card: Sprite2D = value as Sprite2D
		if card == null:
			continue
		var base: Vector2 = card.get_meta("ambient_base", Vector2.ZERO) as Vector2
		parts.append("%s:%d:%.3f,%.3f:%.6f:%s:%s" % [
			String(card.get_meta("ambient_kind", "")),
			int(card.get_meta("ambient_cycle_index", 0)),
			base.x, base.y,
			float(card.get_meta("ambient_phase", -1.0)),
			String(card.get_meta("motion_class", "")),
			String(card.get_meta("intensity_class", "")),
		])
	parts.sort()
	return "|".join(parts)


func _inventory(root_node: Node) -> Dictionary:
	var result := {
		"sprites": 0,
		"spatial": 0,
		"backdrops": 0,
		"contacts": 0,
		"ambient": 0,
	}
	var stack: Array[Node] = [root_node]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		if node is Sprite2D:
			result["sprites"] = int(result["sprites"]) + 1
			if node.name.begins_with("SkyLagoonBackdrop_"):
				result["backdrops"] = int(result["backdrops"]) + 1
			if String(node.get_meta("canvas_layer_role", "")) == "contact_shadow":
				result["contacts"] = int(result["contacts"]) + 1
			if String(node.get_meta("ambient_kind", "")) != "":
				result["ambient"] = int(result["ambient"]) + 1
		if node.is_class("Node" + "3D"):
			result["spatial"] = int(result["spatial"]) + 1
		for child: Node in node.get_children():
			stack.append(child)
	return result


func _visible_fraction(sprite: Sprite2D) -> float:
	if sprite == null or not sprite.is_visible_in_tree() or sprite.texture == null:
		return 0.0
	var texture_size: Vector2 = sprite.texture.get_size()
	var transform: Transform2D = sprite.get_global_transform_with_canvas()
	var corners: Array[Vector2] = [
		transform * (-texture_size * 0.5),
		transform * Vector2(texture_size.x * 0.5, -texture_size.y * 0.5),
		transform * (texture_size * 0.5),
		transform * Vector2(-texture_size.x * 0.5, texture_size.y * 0.5),
	]
	var bounds := Rect2(corners[0], Vector2.ZERO)
	for corner: Vector2 in corners:
		bounds = bounds.expand(corner)
	var clipped: Rect2 = bounds.intersection(get_root().get_visible_rect())
	return clipped.get_area() / maxf(1.0, get_root().get_visible_rect().get_area())


func _validate_stage_cards() -> String:
	var cards: Array = main.g.get("lagoon_ambient_cards", []) as Array
	var contract_ok := true
	var contract_failures: Array[String] = []
	var per_page: Array[Dictionary] = [{}, {}, {}]
	for value: Variant in cards:
		var card: Sprite2D = value as Sprite2D
		var card_ok: bool = card != null \
			and bool(card.get_meta("living_card", false)) \
			and String(card.get_meta("motion_class", "")) != "" \
			and String(card.get_meta("intensity_class", "")) != "" \
			and String(card.get_meta("canvas_layer_role", "")) != "" \
			and bool(card.get_meta("source_owned", false)) \
			and float(card.get_meta("source_aspect", 0.0)) > 0.0 \
			and float(card.get_meta("content_height_fraction", 0.0)) > 0.0 \
			and float(card.get_meta("target_master_height", 0.0)) > 0.0
		contract_ok = contract_ok and card_ok
		if not card_ok:
			contract_failures.append("null" if card == null else "%s:%s" % [
				card.name, JSON.stringify({
					"kind": card.get_meta("ambient_kind", ""),
					"role": card.get_meta("canvas_layer_role", ""),
					"living": card.get_meta("living_card", false),
					"motion": card.get_meta("motion_class", ""),
					"intensity": card.get_meta("intensity_class", ""),
					"owned": card.get_meta("source_owned", false),
					"aspect": card.get_meta("source_aspect", 0.0),
					"fraction": card.get_meta("content_height_fraction", 0.0),
					"height": card.get_meta("target_master_height", 0.0),
				})])
		if card != null:
			var base: Vector2 = card.get_meta("ambient_base", Vector2.ZERO) as Vector2
			var page: int = clampi(int(floor(base.x / 2048.0)), 0, 2)
			per_page[page][String(card.get_meta("ambient_kind", ""))] = true
	_check("canvas_living_card_contract", contract_ok, "cards=%d bad=%s" % [
		cards.size(), ";".join(contract_failures)])
	var budget_ok := true
	var detail: Array[String] = []
	for page: int in range(3):
		var count: int = per_page[page].size()
		budget_ok = budget_ok and count <= 3
		detail.append("p%d=%d" % [page + 1, count])
	_check("quiet_loop_budget_per_screen", budget_ok, ",".join(detail))
	return _ambient_signature(cards)


func _validate_parallax() -> void:
	var root_node: CanvasLayer = promenade.root()
	var rear: Node2D = root_node.find_child("SkyLagoonRear", true, false) as Node2D
	var base: Node2D = root_node.find_child("SkyLagoonBase", true, false) as Node2D
	var foreground: Node2D = root_node.find_child(
		"SkyLagoonForeground", true, false) as Node2D
	promenade.set_master_route_x(2048.0)
	var starts := Vector3(
		rear.position.x if rear != null else 0.0,
		base.position.x if base != null else 0.0,
		foreground.position.x if foreground != null else 0.0)
	promenade.set_master_route_x(4096.0)
	var deltas := Vector3(
		(rear.position.x if rear != null else 0.0) - starts.x,
		(base.position.x if base != null else 0.0) - starts.y,
		(foreground.position.x if foreground != null else 0.0) - starts.z)
	_check("real_rear_base_foreground_parallax",
		rear != null and base != null and foreground != null \
		and is_equal_approx(float(rear.get_meta("parallax_factor", -1.0)), 0.82) \
		and is_equal_approx(float(base.get_meta("parallax_factor", -1.0)), 1.0) \
		and is_equal_approx(float(foreground.get_meta("parallax_factor", -1.0)), 1.06) \
		and not is_equal_approx(deltas.x, deltas.y) \
		and not is_equal_approx(deltas.y, deltas.z),
		"deltas=%s" % deltas)


func _validate_layer_six() -> void:
	var director: LivingWorldDirector = main._living_world_ref()
	var expected_stages: Array[String] = [
		"sky.promenade_runway",
		"sky.promenade_playground",
		"sky.promenade_castle",
	]
	for page: int in range(3):
		promenade.set_master_route_x(float(page) * 2048.0 + 1024.0)
		director.tick(0.0)
		_check("living_stage_page_%d" % (page + 1),
			main.living_stage_id == expected_stages[page]
			and main.living_layer.layer == main.SKY_LAGOON_LIVING_CANVAS_LAYER \
			and main.living_layer.visible and main.living_canvas.visible \
			and main.living_canvas.mouse_filter == Control.MOUSE_FILTER_IGNORE)
	var generation: int = main.living_generation
	var runtime_counts: Dictionary = director.runtime_counts()
	director.force_idle_event_for_probe()
	director.tick(0.1)
	_check("idle_event_is_bounded_canvas_state",
		main.living_event_time >= 0.0 and main.living_canvas.event_progress >= 0.0 \
		and int(runtime_counts.get("layers", 0)) == 1 \
		and int(runtime_counts.get("canvases", 0)) == 1 \
		and int(runtime_counts.get("timers", -1)) == 0 \
		and int(runtime_counts.get("tweens", -1)) == 0 \
		and int(runtime_counts.get("particles", -1)) == 0)
	director.note_activity()
	_check("input_clears_idle_event_without_rebuild",
		main.living_event_time < 0.0 and main.living_generation == generation)


func _validate_speedy_coverage() -> void:
	var root_node: CanvasLayer = promenade.root()
	var coverage_ok := true
	var detail: Array[String] = []
	for master_x: float in [1024.0, 3072.0, 5120.0]:
		promenade.set_master_route_x(master_x)
		var coverage := 0.0
		var large := 0
		for value: Variant in main.g.get("lagoon_ambient_cards", []) as Array:
			var fraction: float = _visible_fraction(value as Sprite2D)
			coverage += fraction
			large += 1 if fraction > 0.10 else 0
		coverage_ok = coverage_ok and coverage <= 1.50 and large <= 8
		detail.append("%.0f:%.1f%%/%d" % [master_x, coverage * 100.0, large])
	_check("speedy_transparent_coverage", coverage_ok, ";".join(detail))
	var inventory: Dictionary = _inventory(root_node)
	_check("canvas_node_inventory",
		int(inventory["spatial"]) == 0 and int(inventory["backdrops"]) == 12 \
		and int(inventory["sprites"]) >= 12, JSON.stringify(inventory))


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
	_hide_interface()
	var day_signature: String = _validate_stage_cards()
	_validate_parallax()
	_validate_layer_six()
	_validate_speedy_coverage()
	for page: int in range(3):
		promenade.set_master_route_x(float(page) * 2048.0 + 1024.0)
		await _frames(3)
		await _capture("canvas_screen_%d_day" % (page + 1))

	var old_root: CanvasLayer = promenade.root()
	var old_cards: Array = (main.g.get("lagoon_ambient_cards", []) as Array).duplicate()
	main._exit_level2_now()
	var old_cards_freed := true
	for value: Variant in old_cards:
		old_cards_freed = old_cards_freed and not is_instance_valid(value)
	_check("lifecycle_teardown_is_synchronous",
		not is_instance_valid(old_root) and old_cards_freed \
		and not main.g.has("lagoon_ambient_cards") \
		and not main.g.has("lagoon_ambient_t") \
		and not main.g.has("lagoon_night_fireflies"))

	main.is_night = true
	main._enter_level2_now(true, false, false)
	await _frames(20)
	promenade = main._lagoon_promenade_ref()
	var night_cards: Array = main.g.get("lagoon_ambient_cards", []) as Array
	_check("cold_build_determinism",
		day_signature == _ambient_signature(night_cards))
	var night_ok := true
	for value: Variant in night_cards:
		var card: Sprite2D = value as Sprite2D
		night_ok = night_ok and card != null \
			and bool(card.get_meta("night_tinted", false)) \
			and card.modulate != Color.WHITE
	_check("night_canvas_congruence", night_ok)
	promenade.set_master_route_x(5120.0)
	await _capture("canvas_screen_3_night")

	if failures == 0:
		print("LIVINGCARD|ALL|OK")
		quit(0)
	else:
		print("LIVINGCARD|ALL|FAIL|count=%d" % failures)
		quit(1)
