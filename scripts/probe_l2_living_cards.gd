extends SceneTree

# Focused acceptance probe for the reusable Living Card animation language.
# Set LIVING_CARD_SHOT_OUT to capture the child's real camera framings.

var failures: int = 0
var main: ReefMain


func _check(label: String, condition: bool, detail: String = "") -> void:
	print("LIVINGCARD|%s|%s%s" % [
		label,
		"OK" if condition else "FAIL",
		"" if detail == "" else "|%s" % detail,
	])
	if not condition:
		failures += 1


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _capture(name: String) -> void:
	var out_dir: String = OS.get_environment("LIVING_CARD_SHOT_OUT")
	if out_dir == "":
		return
	DirAccess.make_dir_recursive_absolute(out_dir)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var error: Error = image.save_jpg(out_dir.path_join(name + ".jpg"), 0.92)
	_check("capture_%s" % name, error == OK)


func _hide_interface() -> void:
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.touch_ui != null:
		main.touch_ui.visible = false
	if main.pause_layer != null:
		main.pause_layer.visible = false


func _ambient_signature(cards: Array) -> String:
	var parts: Array[String] = []
	for value in cards:
		var card: Sprite3D = value as Sprite3D
		if card == null:
			continue
		var base: Vector3 = card.get_meta("ambient_base", Vector3.ZERO) as Vector3
		parts.append("%s:%d:%.3f,%.3f,%.3f:%.6f:%s:%s" % [
			String(card.get_meta("ambient_kind", "")),
			int(card.get_meta("ambient_cycle_index", 0)),
			base.x, base.y, base.z,
			float(card.get_meta("ambient_phase", -1.0)),
			String(card.get_meta("motion_class", "")),
			String(card.get_meta("intensity_class", "")),
		])
	parts.sort()
	return "|".join(parts)


func _inventory(root: Node) -> Dictionary:
	var result := {
		"sprites": 0,
		"meshes": 0,
		"canvas": 0,
		"shaded": 0,
		"backdrops": 0,
		"contacts": 0,
	}
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		if node is Sprite3D:
			var sprite: Sprite3D = node as Sprite3D
			result["sprites"] = int(result["sprites"]) + 1
			result["shaded"] = int(result["shaded"]) + (1 if sprite.shaded else 0)
			if sprite.name.begins_with("SkyLagoonBackdrop_"):
				result["backdrops"] = int(result["backdrops"]) + 1
			if bool(sprite.get_meta("sky_lagoon_contact_shadow", false)):
				result["contacts"] = int(result["contacts"]) + 1
		elif node is MeshInstance3D:
			result["meshes"] = int(result["meshes"]) + 1
		elif node is CanvasItem:
			result["canvas"] = int(result["canvas"]) + 1
		for child: Node in node.get_children():
			stack.append(child)
	return result


func _sprite_coverage(sprite: Sprite3D, camera: Camera3D, viewport_size: Vector2) -> float:
	if not sprite.visible or sprite.texture == null:
		return 0.0
	if sprite.name.begins_with("SkyLagoonBackdrop_"):
		return 0.0
	var width: float = float(sprite.texture.get_width()) * sprite.pixel_size \
		* absf(sprite.scale.x)
	var height: float = float(sprite.texture.get_height()) * sprite.pixel_size \
		* absf(sprite.scale.y)
	var center: Vector3 = sprite.global_position
	var a: Vector2 = camera.unproject_position(
		center + Vector3(-width * 0.5, height * 0.5, 0.0))
	var b: Vector2 = camera.unproject_position(
		center + Vector3(width * 0.5, -height * 0.5, 0.0))
	var bounds := Rect2(
		Vector2(minf(a.x, b.x), minf(a.y, b.y)),
		Vector2(absf(b.x - a.x), absf(b.y - a.y)))
	var clipped: Rect2 = bounds.intersection(Rect2(Vector2.ZERO, viewport_size))
	return clipped.get_area() / maxf(1.0, viewport_size.x * viewport_size.y)

func _promenade_target(target_id: String) -> Sprite3D:
	for value in (main.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == target_id:
			return target.get("node") as Sprite3D
	return null


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
	await _frames(40)
	_hide_interface()
	main.player.position.x = main.LEVEL2_POS.x - 6.0
	main.g["ss_walk_goal"] = null
	await _frames(60)

	var promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
	var cards: Array = main.g.get("lagoon_ambient_cards", [])
	var smoke_count: int = 0
	var smoke_sockets: Dictionary = {}
	var living_contract_ok: bool = true
	var smoke_placement_ok: bool = true
	var grounded_contract_ok: bool = true
	var quiet_loops_by_screen: Array[Dictionary] = [{}, {}, {}]
	for value in cards:
		var card: Sprite3D = value as Sprite3D
		living_contract_ok = living_contract_ok \
			and card != null and card.shaded == false \
			and bool(card.get_meta("living_card", false)) \
			and String(card.get_meta("motion_class", "")) != "" \
			and String(card.get_meta("intensity_class", "")) != "" \
			and float(card.get_meta("source_aspect", 0.0)) > 0.0 \
			and float(card.get_meta("content_height_fraction", 0.0)) > 0.0 \
			and float(card.get_meta("target_world_height", 0.0)) > 0.0
		var kind: String = String(card.get_meta("ambient_kind", ""))
		var base: Vector3 = card.get_meta("ambient_base", Vector3.ZERO) as Vector3
		var screen_index: int = clampi(
			int(floor((base.x + SkyLagoonPromenade.HALF_W) / 48.0)), 0, 2)
		quiet_loops_by_screen[screen_index][kind] = true
		if kind == "tree":
			grounded_contract_ok = grounded_contract_ok \
				and card.get_meta("contact_shadow") is Sprite3D
		if card != null and String(card.get_meta("ambient_kind", "")) == "smoke":
			smoke_count += 1
			var matched_socket: int = -1
			for socket_index: int in range(
					SkyLagoonPromenade.CABIN_SMOKE_ANCHORS.size()):
				if base.distance_to(
						SkyLagoonPromenade.CABIN_SMOKE_ANCHORS[socket_index]) < 0.01:
					matched_socket = socket_index
					break
			if matched_socket >= 0:
				smoke_sockets[matched_socket] = true
			smoke_placement_ok = smoke_placement_ok \
				and matched_socket >= 0 \
				and base.y > SkyLagoonPromenade.BAND_Y + SkyLagoonPromenade.BAND_H
	_check("living_card_contract", living_contract_ok, "cards=%d" % cards.size())
	_check("one_wisp_per_cabin_chimney",
		smoke_count == 3 and smoke_sockets.size() == 3,
		"wisps=%d sockets=%s" % [smoke_count, str(smoke_sockets.keys())])
	_check("smoke_above_three_chimneys_and_walk_band", smoke_placement_ok)
	_check("chimneys_remain_baked_into_approved_mural",
		not main.g.has("lagoon_center_chimney_card"))
	_check("grounded_cards_have_contact_shadows", grounded_contract_ok)
	var quiet_budget_ok: bool = true
	var quiet_detail: Array[String] = []
	for screen_index: int in range(3):
		var loop_count: int = quiet_loops_by_screen[screen_index].size()
		quiet_budget_ok = quiet_budget_ok and loop_count <= 3
		quiet_detail.append("s%d=%d" % [screen_index + 1, loop_count])
	_check("quiet_loop_budget", quiet_budget_ok, ",".join(quiet_detail))
	var phase_anchor: Vector3 = SkyLagoonPromenade.CABIN_SMOKE_ANCHORS[0]
	_check("deterministic_phase",
		is_equal_approx(
			promenade._phase_token(phase_anchor),
			wrapf(
				phase_anchor.x * 0.73 + phase_anchor.z * 1.31,
				0.0, TAU)))
	_check("deterministic_gust_envelope",
		is_equal_approx(promenade._wind_gust_at(0.0), 1.0)
		and promenade._wind_gust_at(17.0) > 1.0
		and is_equal_approx(promenade._wind_gust_at(18.0), 1.5)
		and is_equal_approx(promenade._wind_gust_at(23.0), 1.0))
	var day_signature: String = _ambient_signature(cards)
	var stage_root: Node3D = main.g.get("ss_root") as Node3D
	var inventory: Dictionary = _inventory(stage_root)
	_check("node_type_inventory",
		int(inventory["sprites"]) == 31
		and int(inventory["meshes"]) == 0
		and int(inventory["canvas"]) == 0
		and int(inventory["shaded"]) == 0
		and int(inventory["backdrops"]) == 12
		and int(inventory["contacts"]) == 5,
		JSON.stringify(inventory))

	main.g["lagoon_castle_armed"] = false
	promenade._clear_focus()
	main.player.position.x = main.LEVEL2_POS.x - 48.0
	await _frames(20)
	await _capture("final_screen_1_runway_revisit")
	main.g["lagoon_castle_armed"] = false
	promenade._clear_focus()
	main.player.position.x = main.LEVEL2_POS.x
	await _frames(20)
	await _capture("attempt_04_playground_wide")
	await _capture("final_screen_2_playground")
	main.g["lagoon_castle_armed"] = false
	promenade._clear_focus()
	main.player.position.x = main.LEVEL2_POS.x + phase_anchor.x
	await _frames(30)
	await _capture("attempt_04_cabin_smoke_wisp_day")
	await _capture("final_screen_3_castle_smoke")

	var viewport: Viewport = get_root().get_viewport()
	var camera: Camera3D = viewport.get_camera_3d()
	var slide: Sprite3D = _promenade_target("slide")
	var mural_anchor_ok: bool = camera != null and slide != null
	var mural_anchor_detail: Array[String] = []
	for player_x: float in [-30.0, 30.0]:
		main.player.position.x = main.LEVEL2_POS.x + player_x
		main.g["lagoon_castle_armed"] = false
		for _index: int in range(6):
			promenade.tick(0.25)
		if camera == null or slide == null:
			mural_anchor_ok = false
			continue
		var camera_x: float = camera.position.x - stage_root.position.x
		var camera_z: float = camera.position.z - stage_root.position.z
		var backdrop_distance: float = absf(
			camera_z - SkyLagoonPromenade.BACKDROP_Z)
		var card_distance: float = absf(camera_z - slide.position.z)
		var reference_x: float = float(slide.get_meta(
			"mural_reference_x", slide.position.x))
		var reference_camera_x: float = float(slide.get_meta(
			"mural_reference_camera_x", 0.0))
		var socket_lock: float = float(slide.get_meta(
			"mural_socket_lock", 0.0))
		var expected_x: float = reference_x \
			+ (camera_x - reference_camera_x) \
			* (1.0 - card_distance / backdrop_distance) \
			* socket_lock
		var anchor_delta: float = absf(slide.position.x - expected_x)
		mural_anchor_ok = mural_anchor_ok and anchor_delta < 0.0001
		mural_anchor_detail.append("%.0f:%.6f" % [player_x, anchor_delta])
	_check("playground_mural_anchor_stability", mural_anchor_ok,
		";".join(mural_anchor_detail))

	var coverage_ok: bool = camera != null
	var coverage_detail: Array[String] = []
	for screen_x: float in [-48.0, 0.0, 48.0]:
		main.player.position.x = main.LEVEL2_POS.x + screen_x
		main.g["lagoon_castle_armed"] = false
		for _index: int in range(6):
			promenade.tick(0.25)
		var total_coverage: float = 0.0
		var large_cards: int = 0
		for child: Node in stage_root.get_children():
			if child is Sprite3D:
				var fraction: float = _sprite_coverage(
					child as Sprite3D, camera, viewport.get_visible_rect().size)
				total_coverage += fraction
				large_cards += 1 if fraction > 0.10 else 0
		coverage_ok = coverage_ok and total_coverage <= 1.50 and large_cards <= 8
		coverage_detail.append("%.0f:%.1f%%/%d" % [
			screen_x, total_coverage * 100.0, large_cards])
	_check("speedy_transparent_coverage", coverage_ok, ";".join(coverage_detail))

	var tick_started: int = Time.get_ticks_usec()
	for _index: int in range(2000):
		promenade._tick_ambient_life(1.0 / 60.0)
	var average_tick_usec: float = float(Time.get_ticks_usec() - tick_started) / 2000.0
	_check("speedy_tick_under_1ms", average_tick_usec < 1000.0,
		"average_usec=%.2f" % average_tick_usec)

	main.is_night = true
	main._enter_level2_now(true, false, false)
	await _frames(45)
	_hide_interface()
	main.g["lagoon_castle_armed"] = false
	promenade._clear_focus()
	main.player.position.x = main.LEVEL2_POS.x + phase_anchor.x
	main.g["ss_walk_goal"] = null
	await _frames(30)
	var night_cards: Array = main.g.get("lagoon_ambient_cards", [])
	var night_root: Node3D = main.g.get("ss_root") as Node3D
	var night_tint_ok: bool = night_cards.size() == 5
	var night_backdrops: int = 0
	for child: Node in night_root.get_children():
		if child is Sprite3D:
			var night_sprite: Sprite3D = child as Sprite3D
			if night_sprite.name.begins_with("SkyLagoonBackdrop_"):
				night_backdrops += 1
				night_tint_ok = night_tint_ok \
					and night_sprite.modulate.is_equal_approx(
						SkyLagoonPromenade.NIGHT_BACKDROP_TINT)
	for value in night_cards:
		var night_card: Sprite3D = value as Sprite3D
		night_tint_ok = night_tint_ok \
			and night_card.modulate.r <= SkyLagoonPromenade.NIGHT_WORLD_TINT.r + 0.01 \
			and night_card.modulate.g <= SkyLagoonPromenade.NIGHT_WORLD_TINT.g + 0.01 \
			and night_card.modulate.b <= SkyLagoonPromenade.NIGHT_WORLD_TINT.b + 0.01
	_check("night_congruence", night_tint_ok and night_backdrops == 12,
		"backdrops=%d cards=%d" % [night_backdrops, night_cards.size()])
	_check("cold_build_determinism",
		day_signature == _ambient_signature(night_cards))
	await _capture("attempt_04_cabin_smoke_wisp_night")

	var old_root: Node3D = night_root
	var old_cards: Array = night_cards.duplicate()
	main._exit_level2_now()
	await _frames(5)
	var old_cards_freed: bool = true
	for value in old_cards:
		old_cards_freed = old_cards_freed and not is_instance_valid(value)
	_check("lifecycle_teardown",
		not is_instance_valid(old_root)
		and old_cards_freed
		and not main.g.has("lagoon_ambient_cards")
		and not main.g.has("lagoon_ambient_t")
		and not main.g.has("lagoon_wind_gust")
		and not main.g.has("lagoon_wind_distance")
		and not main.g.has("lagoon_mural_socket_cards"))
	main.is_night = false
	main._enter_level2_now(true, false, false)
	await _frames(20)
	_check("lifecycle_rebuild",
		(main.g.get("lagoon_ambient_cards", []) as Array).size() == 5
		and main.g.has("lagoon_wind_distance")
		and not main.g.has("lagoon_center_chimney_card"))

	if failures == 0:
		print("LIVINGCARD|ALL|OK")
		quit(0)
	else:
		print("LIVINGCARD|ALL|FAIL|count=%d" % failures)
		quit(1)
