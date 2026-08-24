extends SceneTree
# Runtime half of the game-wide visual design audit.
#
# tools/audit_visual_design.py can read every PNG and every builder constant,
# but it cannot see the assembled scene: which Canvas layers actually exist,
# how they move under a real Camera2D sample, how big a tap target lands on the
# child's screen, or whether a target silhouette separates in the flattened
# viewport composite. This probe records those facts. Legacy spatial counts
# remain debt-only evidence; they never satisfy a Canvas check.
#
# Generator, not a gate: it asserts nothing about art direction and never
# fails a build on a judgement call.  It DOES fail if the scene it was told to
# measure never built, because facts nobody collected must not read as a pass.

const DEFAULT_OUT_PATH := "res://audit/visual_runtime_facts.json"
const SPEC_PATH := "res://tools/visual_audit_spec.json"
const CANVAS_SAMPLE_PX := 240.0
const CANVAS_LAYER_META := "visual_audit_layer_id"
const CANVAS_COVERAGE_METHOD := "viewport_grid_effective_canvas_alpha_64x36_v2"
const CANVAS_COMPOSITE_SIGNATURE_METHOD := "viewport_grid_effective_canvas_rgba_64x36_v1"
const CANVAS_MOTION_METHOD := "viewport_canvas_transform_delta"
const CANVAS_DRAW_ORDER_METHOD := \
	"deterministic_effective_canvas_z_verified_descendants_v3"
const RENDERED_DIFF_METHOD := "visible_minus_target_hidden_rgba8_exact_v1"
const SOURCE_PROJECTION_METHOD := "independent_source_alpha_inverse_canvas_v1"
const CANVAS_OCCLUSION_METHOD := "live_canvas_alpha_overlap_samples_v2"
const CANVAS_OCCLUSION_SAMPLE_STEP := 4.0
const CANVAS_OCCLUSION_ALPHA_THRESHOLD := 0.5
const TEMPORAL_FREEZE_METHOD := "engine_time_scale_zero_alternating_visibility_v1"
const CAPTURE_ADAPTER_METHOD := "explicit_live_state_assertions_v1"
const EVIDENCE_SCHEMA_VERSION := 2
# the storybook UI's minimum touch size, in 1280x720 base-canvas pixels
const MIN_TOUCH_PX := 110.0

var failed := false
var zones: Dictionary = {}
var out_path := DEFAULT_OUT_PATH
var visual_spec: Dictionary = {}
var run_identity := ""
var run_nonce := ""
var run_started_utc := ""
var source_revision := ""
var runtime_source_manifest: Dictionary = {}
var git_revision := ""
var git_tree := ""
var git_dependencies_clean := false
var fresh_challenge := ""
var current_canvas_global_effects := 0


func _log(label: String, ok: bool, detail: String = "") -> void:
	print("VISUALFACTS|%s: %s%s" % [
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
	out_path = _requested_out_path()
	visual_spec = _load_visual_spec()
	fresh_challenge = _requested_challenge()
	run_started_utc = Time.get_datetime_string_from_system(true, false) + "Z"
	run_nonce = ("%s|%d|%d" % [
		run_started_utc, Time.get_ticks_usec(), randi()]).sha256_text()
	runtime_source_manifest = _source_manifest()
	source_revision = _source_revision(runtime_source_manifest)
	var git_identity := _git_source_identity()
	git_revision = String(git_identity.get("revision", ""))
	git_tree = String(git_identity.get("tree", ""))
	git_dependencies_clean = bool(git_identity.get("dependencies_clean", false))
	var version := Engine.get_version_info()
	run_identity = "|".join([
		git_revision, git_tree, fresh_challenge, source_revision,
		run_nonce, run_started_utc,
		String(version.get("string", "")),
		String(RenderingServer.get_current_rendering_method()),
	]).sha256_text()
	# Authoring and touch budgets are defined in the 1280x720 base canvas.
	# Pin this generator to that viewport so projected visual sizes are directly
	# comparable and do not depend on a headless runner's default square window.
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(1280, 720)
	var packed: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = packed.instantiate()
	get_root().add_child(main)
	await _frames(2)
	# Project startup applies the desktop maximized-mode override after _init().
	# Reapply the audit window once the root Window is live so the flattened
	# capture and the attested viewport use the same canonical pixel grid.
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = Vector2i(1280, 720)
	await _frames(2)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(2)

	await _measure(main, "reef")

	# unlock the lagoon the way probe_l2 does, then measure the promenade
	main.pearl_count = main.PEARL_TOTAL
	for friend_value in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	# Keep the audited holder membership deterministic: daylight has no optional
	# fireflies, while the arrival plane is the stable route landmark.
	main.is_night = false
	main.save_data["lagoon_plane_departed"] = false
	# The trusted Lagoon probe enters the target state synchronously. The public
	# fade wrapper is intentionally asynchronous and eight headless frames are
	# not a contract for its completion; sampling it here can bind "Sky Lagoon"
	# facts to the outgoing legacy reef/spatial tree instead of the promenade.
	main._enter_level2_now(false, false, false)
	await _frames(8)
	var promenade: SkyLagoonPromenade = main.call(
		"_lagoon_promenade_ref") as SkyLagoonPromenade
	promenade.set_master_route_x(3600.0)
	promenade.cancel_navigation()
	await _frames(2)
	await _measure(main, "sky_lagoon")

	_write()
	print("VISUALFACTS|result: ", "FAIL" if failed else "ALL OK")
	quit(1 if failed else 0)


# --------------------------------------------------------------------------

func _measure(main: ReefMain, zone_id: String) -> void:
	# Legacy cards are debt telemetry only. Keep collection class-string/property
	# based so this 2D probe does not add or normalize forbidden spatial APIs.
	var legacy_cards: Array[Node] = []
	_collect_legacy_cards(get_root(), legacy_cards)
	_refresh_canvas_global_effects()
	var legacy_visible := _visible_node_count(legacy_cards)
	var alpha_cards := 0
	var shaded_cards := 0
	var texture_px := 0
	for card in legacy_cards:
		if not _node_visible(card):
			continue
		var alpha_cut: Variant = card.get("alpha_cut")
		var transparent: Variant = card.get("transparent")
		if alpha_cut is int and int(alpha_cut) == 0 \
				and transparent is bool and bool(transparent):
			alpha_cards += 1
		var shaded: Variant = card.get("shaded")
		if shaded is bool and bool(shaded):
			shaded_cards += 1
		var texture := _visual_texture(card)
		if texture != null:
			texture_px += texture.get_width() * texture.get_height()

	var capture_targets: Array = []
	var facts: Dictionary = {
		"sprite3d_visible": legacy_visible,
		"sprite3d_total": legacy_cards.size(),
		"legacy_depth_metrics_authoritative": false,
		"blend_alpha_cards": alpha_cards,
		"shaded_world_cards": shaded_cards,
		"texture_megapixels": snappedf(float(texture_px) / 1000000.0, 0.01),
		"targets": _targets(main, zone_id, capture_targets),
	}
	facts.merge(_runtime_block_provenance(main, zone_id))
	facts["canvas_parallax"] = await _canvas_parallax_facts(
		main, zone_id, legacy_visible)
	facts["canvas_occlusion"] = _canvas_occlusion_facts(
		main, zone_id, legacy_visible, capture_targets)
	facts["rendered_composites"] = await _capture_rendered_states(
		main, zone_id, capture_targets)
	zones[zone_id] = facts
	var canvas_backend := String((facts["canvas_parallax"] as Dictionary).get(
		"backend", "missing"))
	var built_ok := zone_id == "reef" or legacy_cards.size() > 0 \
		or canvas_backend == "canvas_2d"
	_log("%s_built" % zone_id, built_ok,
		"legacy_cards=%d canvas_backend=%s" % [
			legacy_cards.size(), canvas_backend])


func _visible_node_count(nodes: Array[Node]) -> int:
	var n := 0
	for node in nodes:
		if _node_visible(node):
			n += 1
	return n


func _node_visible(node: Node) -> bool:
	var value: Variant = node.get("visible")
	return value is bool and bool(value)


func _collect_legacy_cards(node: Node, out: Array[Node]) -> void:
	if node.get_class() == "Sprite" + "3D":
		out.append(node)
	for child in node.get_children():
		_collect_legacy_cards(child, out)


func _visible_canvas_global_effect_count(node: Node) -> int:
	var count := 0
	if node is CanvasModulate and (node as CanvasModulate).is_visible_in_tree() \
			and node.get_viewport() == get_root():
		count += 1
	elif node is Light2D and (node as Light2D).is_visible_in_tree() \
			and (node as Light2D).enabled and node.get_viewport() == get_root():
		count += 1
	for child in node.get_children():
		count += _visible_canvas_global_effect_count(child)
	return count


func _refresh_canvas_global_effects() -> int:
	current_canvas_global_effects = _visible_canvas_global_effect_count(get_root())
	return current_canvas_global_effects


func _targets(main: ReefMain, zone_id: String, capture_targets: Array) -> Array:
	# The forgiving hit diameter and the visible composite are separate facts.
	# Capture sources are restricted to the zone's declared foreground art so a
	# glow/contact-shadow cannot masquerade as the child's target silhouette.
	var out: Array = []
	if zone_id != "sky_lagoon":
		return out
	_refresh_canvas_global_effects()
	var approved: Array[String] = _zone_paths(zone_id, ["standees", "characters"])
	var registered: Array = main.g.get("lagoon_promenade_targets", []) as Array
	var resolver: Object = main.call("_lagoon_promenade_ref") as Object
	for value in registered:
		var target: Dictionary = value as Dictionary
		var node: Node = target.get("node") as Node
		if node == null or not is_instance_valid(node):
			continue
		var target_id := String(target.get("id", ""))
		var visual_nodes: Array[Node] = []
		_collect_visual_nodes(node, visual_nodes)
		var approved_nodes: Array[Node] = []
		var visual_rect := Rect2()
		var has_rect := false
		var painted_image_cache := {}
		for visual in visual_nodes:
			if not (visual is CanvasItem) or not (visual as CanvasItem).is_visible_in_tree():
				continue
			if not _visual_is_in_audited_viewport(visual) \
					or _visual_has_unresolved_alpha_effect(visual) \
					or _effective_canvas_opacity(visual) < CANVAS_OCCLUSION_ALPHA_THRESHOLD:
				continue
			var path := _visual_texture_path(visual)
			if path == "" or path not in approved:
				continue
			var rect := _painted_visual_screen_rect(visual, painted_image_cache)
			if rect.size.x <= 0.0 or rect.size.y <= 0.0:
				continue
			approved_nodes.append(visual)
			visual_rect = rect if not has_rect else visual_rect.merge(rect)
			has_rect = true
		var hit_diameter_px: float = float(target.get("radius_px", 0.0)) * 2.0
		var visual_height := visual_rect.size.y if has_rect else 0.0
		if not has_rect or approved_nodes.is_empty():
			continue
		var hit_center := Vector2(-1.0, -1.0)
		if node is CanvasItem:
			hit_center = (node as CanvasItem).get_global_transform_with_canvas().origin
		var center_in_viewport := Rect2(
			Vector2.ZERO, Vector2(get_root().size)).has_point(hit_center)
		var nearest_painted := _nearest_painted_distance(
			approved_nodes, hit_center, maxf(16.0, hit_diameter_px * 0.5))
		var proven_reach_radius := minf(hit_diameter_px * 0.5, MIN_TOUCH_PX * 0.5)
		var reach_samples := _production_resolver_reach_samples(
			resolver, hit_center, target_id, proven_reach_radius)
		var resolver_id := ""
		var resolver_confirmed := reach_samples.size() == 9
		var reach_index := 0
		for sample_value in reach_samples:
			var reach_sample: Dictionary = sample_value as Dictionary
			if reach_index == 0:
				resolver_id = String(reach_sample.get("returned_id", ""))
			if not bool(reach_sample.get("inside_viewport", false)) \
					or String(reach_sample.get("returned_id", "")) != target_id:
				resolver_confirmed = false
			reach_index += 1
		out.append({
			"id": target_id,
			"instance_path": String(node.get_path()),
			"screen_px": snappedf(hit_diameter_px, 0.1),
			"hit_diameter_px": snappedf(hit_diameter_px, 0.1),
			"visual_screen_px": snappedf(visual_height, 0.1),
			"visual_width_px": snappedf(visual_rect.size.x if has_rect else 0.0, 0.1),
			"visual_screen_rect": [snappedf(visual_rect.position.x, 0.1),
				snappedf(visual_rect.position.y, 0.1),
				snappedf(visual_rect.size.x, 0.1),
				snappedf(visual_rect.size.y, 0.1)],
			"audited_viewport": true,
			"visible_canvas_visual_count": approved_nodes.size(),
			"interaction_registry": "lagoon_promenade_targets_v1",
			"resolver_method": "production_target_at_radial_reach_v2",
			"resolver_hit_screen_px": [snappedf(hit_center.x, 0.1),
				snappedf(hit_center.y, 0.1)],
			"resolver_returned_id": resolver_id,
			"resolver_hit_confirmed": resolver_confirmed,
			"resolver_reach_radius_px": snappedf(proven_reach_radius, 0.1),
			"resolver_reach_samples": reach_samples,
			"resolver_center_in_viewport": center_in_viewport,
			"resolver_nearest_painted_px": snappedf(nearest_painted, 0.1),
			"meets_min_touch": hit_diameter_px >= MIN_TOUCH_PX,
		})
		if has_rect and not approved_nodes.is_empty():
			capture_targets.append({
				"id": target_id,
				"target_instance_path": String(node.get_path()),
				"nodes": approved_nodes,
				"figure_rect": visual_rect,
			})
	return out


func _painted_visual_screen_rect(node: Node, image_cache: Dictionary) -> Rect2:
	var bounds := _visual_screen_rect(node).intersection(Rect2(
		Vector2.ZERO, Vector2(get_root().size)))
	if bounds.size.x <= 0.0 or bounds.size.y <= 0.0:
		return Rect2()
	var min_x := 2147483647
	var min_y := 2147483647
	var max_x := -1
	var max_y := -1
	for y in range(floori(bounds.position.y), ceili(bounds.end.y)):
		for x in range(floori(bounds.position.x), ceili(bounds.end.x)):
			var point := Vector2(float(x) + 0.5, float(y) + 0.5)
			if _visual_alpha_at_screen_point(
					node, point, image_cache) < CANVAS_OCCLUSION_ALPHA_THRESHOLD:
				continue
			min_x = mini(min_x, x)
			min_y = mini(min_y, y)
			max_x = maxi(max_x, x)
			max_y = maxi(max_y, y)
	if max_x < min_x or max_y < min_y:
		return Rect2()
	return Rect2(float(min_x), float(min_y),
		float(max_x - min_x + 1), float(max_y - min_y + 1))


func _production_resolver_reach_samples(resolver: Object, center: Vector2,
		target_id: String, radius: float) -> Array:
	var out: Array = []
	if resolver == null or not resolver.has_method("_target_at"):
		return out
	var diagonal := radius / sqrt(2.0)
	var offsets: Array[Vector2] = [
		Vector2.ZERO,
		Vector2(radius, 0.0), Vector2(-radius, 0.0),
		Vector2(0.0, radius), Vector2(0.0, -radius),
		Vector2(diagonal, diagonal), Vector2(diagonal, -diagonal),
		Vector2(-diagonal, diagonal), Vector2(-diagonal, -diagonal),
	]
	var viewport_rect := Rect2(Vector2.ZERO, Vector2(get_root().size))
	for offset in offsets:
		var point := center + offset
		var returned_id := ""
		var resolved_value: Variant = resolver.call("_target_at", point)
		if resolved_value is Dictionary:
			returned_id = String((resolved_value as Dictionary).get("id", ""))
		out.append({
			"offset_px": [snappedf(offset.x, 0.1), snappedf(offset.y, 0.1)],
			"screen_px": [snappedf(point.x, 0.1), snappedf(point.y, 0.1)],
			"returned_id": returned_id,
			"inside_viewport": viewport_rect.has_point(point),
			"matches_target": returned_id == target_id,
		})
	return out


func _nearest_painted_distance(visuals: Array[Node], center: Vector2,
		max_distance: float) -> float:
	if center.x < 0.0 or center.y < 0.0:
		return -1.0
	var best := INF
	var cache := {}
	for visual in visuals:
		var rect := _visual_screen_rect(visual).intersection(Rect2(
			center - Vector2.ONE * max_distance,
			Vector2.ONE * max_distance * 2.0))
		if rect.size.x <= 0.0 or rect.size.y <= 0.0:
			continue
		var y := floorf(rect.position.y)
		while y <= ceilf(rect.end.y):
			var x := floorf(rect.position.x)
			while x <= ceilf(rect.end.x):
				var point := Vector2(x, y)
				var distance := point.distance_to(center)
				if distance <= max_distance and distance < best \
						and _visual_alpha_at_screen_point(
							visual, point, cache) >= CANVAS_OCCLUSION_ALPHA_THRESHOLD:
					best = distance
				x += CANVAS_OCCLUSION_SAMPLE_STEP
			y += CANVAS_OCCLUSION_SAMPLE_STEP
	return best if is_finite(best) else -1.0


func _collect_visual_nodes(node: Node, out: Array[Node]) -> void:
	if node is Sprite2D or node is TextureRect:
		out.append(node)
	for child in node.get_children():
		_collect_visual_nodes(child, out)


func _visual_texture(node: Node) -> Texture2D:
	var value: Variant = node.get("texture")
	if value is Texture2D:
		return value as Texture2D
	return null


func _visual_texture_path(node: Node) -> String:
	var texture := _visual_texture(node)
	if texture == null:
		return ""
	return texture.resource_path.trim_prefix("res://").replace("\\", "/")


func _visual_screen_rect(node: Node) -> Rect2:
	if node is Sprite2D:
		var sprite2d := node as Sprite2D
		var local_rect := sprite2d.get_rect()
		var transform := sprite2d.get_global_transform_with_canvas()
		return _transformed_rect(local_rect, transform)
	if node is TextureRect:
		var texture_rect := node as TextureRect
		return _transformed_rect(Rect2(Vector2.ZERO, texture_rect.size),
			texture_rect.get_global_transform_with_canvas())
	return Rect2()


func _transformed_rect(rect: Rect2, transform: Transform2D) -> Rect2:
	var points: Array[Vector2] = [
		transform * rect.position,
		transform * Vector2(rect.end.x, rect.position.y),
		transform * rect.end,
		transform * Vector2(rect.position.x, rect.end.y),
	]
	var out := Rect2(points[0], Vector2.ZERO)
	for point in points:
		out = out.expand(point)
	return out


func _canvas_parallax_facts(main: ReefMain, zone_id: String,
		_legacy_visible: int) -> Dictionary:
	var nodes: Array[Node] = []
	_collect_canvas_layers(main, nodes)
	var provenance := _runtime_block_provenance(main, zone_id)
	var canvas_audit_root: Node = get_root()
	var zone_promenade: SkyLagoonPromenade = null
	if zone_id == "sky_lagoon" \
			and String(main.g.get("phase", "")) == "promenade":
		zone_promenade = main.call(
			"_lagoon_promenade_ref") as SkyLagoonPromenade
		if zone_promenade != null and zone_promenade.canvas_root() != null:
			canvas_audit_root = zone_promenade.canvas_root()
	var spatial_count := _non_canvas_spatial_count(canvas_audit_root)
	if nodes.is_empty():
		var missing := {
			"backend": "legacy_spatial" if spatial_count > 0 else "missing",
			"root_canvas_item": false,
			"non_canvas_spatial_nodes": spatial_count,
			"camera_sample_px": 0.0,
			"motion_method": CANVAS_MOTION_METHOD,
			"layers": [],
		}
		missing.merge(provenance)
		return missing
	var before: Dictionary = {}
	for node in nodes:
		before[String(node.get_path())] = _canvas_origin(node)
	var camera := main.get_viewport().get_camera_2d()
	var sample_px := 0.0
	if camera != null:
		var original := camera.global_position
		var before_canvas := main.get_viewport().get_canvas_transform()
		var promenade: SkyLagoonPromenade = zone_promenade
		var original_route_x := 0.0
		if promenade != null:
			original_route_x = promenade.master_route_x()
			var origin_screen: float = promenade.screen_from_master(
				Vector2(original_route_x, 0.0)).x
			var unit_screen: float = promenade.screen_from_master(
				Vector2(original_route_x + 1.0, 0.0)).x
			var pixels_per_master := maxf(0.001, unit_screen - origin_screen)
			promenade.set_master_route_x(
				original_route_x + CANVAS_SAMPLE_PX / pixels_per_master)
		else:
			camera.global_position.x += CANVAS_SAMPLE_PX
		await _frames(2)
		_refresh_canvas_global_effects()
		var after_canvas := main.get_viewport().get_canvas_transform()
		sample_px = (after_canvas.origin - before_canvas.origin).length()
		var rows: Array = []
		for node in nodes:
			rows.append(_canvas_layer_row(
				node, (_canvas_origin(node) -
					(before[String(node.get_path())] as Vector2)).length()))
		if promenade != null:
			promenade.set_master_route_x(original_route_x)
		else:
			camera.global_position = original
		await _frames(2)
		var captured := {
			"backend": "canvas_2d",
			"root_canvas_item": true,
			"non_canvas_spatial_nodes": _non_canvas_spatial_count(
				canvas_audit_root),
			"camera_requested_px": CANVAS_SAMPLE_PX,
			"camera_sample_px": snappedf(sample_px, 0.01),
			"motion_method": CANVAS_MOTION_METHOD,
			"layers": rows,
		}
		captured.merge(provenance)
		return captured
	var static_rows: Array = []
	_refresh_canvas_global_effects()
	for node in nodes:
		static_rows.append(_canvas_layer_row(node, 0.0))
	var no_camera := {
		"backend": "canvas_2d",
		"root_canvas_item": true,
		"non_canvas_spatial_nodes": _non_canvas_spatial_count(canvas_audit_root),
		"camera_sample_px": sample_px,
		"motion_method": CANVAS_MOTION_METHOD,
		"layers": static_rows,
	}
	no_camera.merge(provenance)
	return no_camera


func _collect_canvas_layers(node: Node, out: Array[Node]) -> void:
	if node.has_meta(CANVAS_LAYER_META) and (node is CanvasItem or node is CanvasLayer):
		out.append(node)
	for child in node.get_children():
		_collect_canvas_layers(child, out)


func _canvas_layer_row(node: Node, screen_delta: float) -> Dictionary:
	var assets: Array[String] = []
	_collect_canvas_assets(node, assets)
	assets.sort()
	var visuals := _canvas_visual_list(node)
	var coverage := _canvas_painted_coverage(node)
	var z_index := 0
	var visible := true
	if node is CanvasItem:
		z_index = _canvas_draw_order(node)
		visible = (node as CanvasItem).is_visible_in_tree()
	elif node is CanvasLayer:
		z_index = _canvas_draw_order(node)
		visible = (node as CanvasLayer).visible
	return {
		"id": String(node.get_meta(CANVAS_LAYER_META, "")),
		"instance_path": String(node.get_path()),
		"node_type": node.get_class(),
		"instantiated": is_instance_valid(node),
		"visible": visible,
		"canvas_item": true,
		"non_canvas_spatial_descendants": _non_canvas_spatial_count(node),
		"assets": assets,
		"content_signature": _content_signature(assets),
		"painted_composite_method": CANVAS_COMPOSITE_SIGNATURE_METHOD,
		"painted_composite_signature": _canvas_painted_composite_signature(visuals),
		"coverage_method": CANVAS_COVERAGE_METHOD,
		"screen_coverage_ratio": snappedf(coverage, 0.0001),
		"unresolved_alpha_effects": _unresolved_alpha_effect_count(visuals),
		"screen_delta_px": snappedf(screen_delta, 0.01),
		"parallax_factor": float(node.get_meta("parallax_factor", 1.0)),
		"z_index": z_index,
		"draw_order": z_index,
		"draw_order_method": CANVAS_DRAW_ORDER_METHOD,
		"unresolved_draw_order_effects": _draw_order_effect_count(
			node, visuals, z_index),
	}


func _canvas_draw_order(node: Node) -> int:
	if node is CanvasLayer:
		return (node as CanvasLayer).layer * 1000000
	if not (node is CanvasItem):
		return 0
	var item := node as CanvasItem
	var order := item.z_index
	# Godot 4.7 does not expose CanvasItem's effective relative z as a public
	# method. Reconstruct the documented z_as_relative chain so an ordinary
	# Sprite2D child at local z=0 inherits its tagged holder's draw band.
	var current_item := item
	while current_item.z_as_relative:
		var canvas_parent := current_item.get_parent()
		if not (canvas_parent is CanvasItem):
			break
		current_item = canvas_parent as CanvasItem
		order += current_item.z_index
	var parent := node.get_parent()
	while parent != null:
		if parent is CanvasLayer:
			order += (parent as CanvasLayer).layer * 1000000
			break
		parent = parent.get_parent()
	return order


func _draw_order_effect_count(root: Node, visuals: Array[Node],
		_expected_order: int) -> int:
	var count := 0
	for visual in visuals:
		# A child's explicit relative z offset is deterministic and commonly used
		# for contact shadows and focus cues. Only ordering modes that make the
		# tagged holder's effective band insufficient remain unresolved.
		if _visual_has_ambiguous_draw_order(visual, root):
			count += 1
	return count


func _visual_has_ambiguous_draw_order(visual: Node, stop: Node = null) -> bool:
	var current: Node = visual
	while current != null:
		if current is CanvasItem:
			var show_behind: Variant = current.get("show_behind_parent")
			var y_sorted: Variant = current.get("y_sort_enabled")
			if (show_behind is bool and bool(show_behind)) \
					or (y_sorted is bool and bool(y_sorted)):
				return true
		if current == stop:
			return false
		current = current.get_parent()
	return stop != null


func _canvas_origin(node: Node) -> Vector2:
	if node is CanvasItem:
		return (node as CanvasItem).get_global_transform_with_canvas().origin
	for child in node.get_children():
		var child_node := child as Node
		if child_node is CanvasItem:
			return (child_node as CanvasItem).get_global_transform_with_canvas().origin
	return Vector2.ZERO


func _collect_canvas_assets(node: Node, out: Array[String]) -> void:
	if node is CanvasItem and not (node as CanvasItem).is_visible_in_tree():
		return
	if node is CanvasLayer and not (node as CanvasLayer).visible:
		return
	var path := _visual_texture_path(node)
	if path != "" and path not in out:
		out.append(path)
	for child in node.get_children():
		_collect_canvas_assets(child, out)


func _visual_color_at_screen_point(node: Node, point: Vector2,
		image_cache: Dictionary) -> Color:
	if not (node is CanvasItem) or not (node as CanvasItem).is_visible_in_tree():
		return Color(0.0, 0.0, 0.0, 0.0)
	if _visual_has_unresolved_alpha_effect(node) \
			or not _point_inside_canvas_clips(node, point):
		return Color(0.0, 0.0, 0.0, 0.0)
	var texture := _visual_texture(node)
	if texture == null:
		return Color(0.0, 0.0, 0.0, 0.0)
	var cache_key := node.get_instance_id()
	var image: Image = image_cache.get(cache_key) as Image
	if image == null:
		image = texture.get_image()
		if image == null or image.is_empty():
			return Color(0.0, 0.0, 0.0, 0.0)
		# VRAM-compressed POT textures are valid production inputs, but Image
		# sampling requires a CPU-readable copy. Decompress only the probe cache;
		# the imported/runtime texture and its Mobile memory policy stay untouched.
		if image.is_compressed():
			image = image.duplicate()
			if image.decompress() != OK:
				return Color(0.0, 0.0, 0.0, 0.0)
		image_cache[cache_key] = image
	var local := (node as CanvasItem).get_global_transform_with_canvas().affine_inverse() * point
	var source := Vector2.ZERO
	if node is Sprite2D:
		var sprite := node as Sprite2D
		var local_rect := sprite.get_rect()
		if local_rect.size.x <= 0.0 or local_rect.size.y <= 0.0 \
				or not local_rect.has_point(local):
			return Color(0.0, 0.0, 0.0, 0.0)
		var base := Rect2(Vector2.ZERO, Vector2(image.get_width(), image.get_height()))
		if sprite.region_enabled:
			base = sprite.region_rect
		var frame_size := Vector2(
			base.size.x / float(maxi(1, sprite.hframes)),
			base.size.y / float(maxi(1, sprite.vframes)))
		var uv := (local - local_rect.position) / local_rect.size
		if sprite.flip_h:
			uv.x = 1.0 - uv.x
		if sprite.flip_v:
			uv.y = 1.0 - uv.y
		source = base.position + Vector2(
			float(sprite.frame_coords.x) * frame_size.x + uv.x * frame_size.x,
			float(sprite.frame_coords.y) * frame_size.y + uv.y * frame_size.y)
	elif node is TextureRect:
		var texture_rect := node as TextureRect
		var control_size := texture_rect.size
		if control_size.x <= 0.0 or control_size.y <= 0.0 \
				or not Rect2(Vector2.ZERO, control_size).has_point(local):
			return Color(0.0, 0.0, 0.0, 0.0)
		var source_size := Vector2(image.get_width(), image.get_height())
		var draw_size := control_size
		var draw_origin := Vector2.ZERO
		var mode := int(texture_rect.stretch_mode)
		if mode == TextureRect.STRETCH_TILE:
			source = Vector2(fposmod(local.x, source_size.x),
				fposmod(local.y, source_size.y))
		else:
			if mode == TextureRect.STRETCH_KEEP:
				draw_size = source_size
			elif mode == TextureRect.STRETCH_KEEP_CENTERED:
				draw_size = source_size
				draw_origin = (control_size - draw_size) * 0.5
			elif mode in [TextureRect.STRETCH_KEEP_ASPECT,
					TextureRect.STRETCH_KEEP_ASPECT_CENTERED,
					TextureRect.STRETCH_KEEP_ASPECT_COVERED]:
				var scale_value := minf(control_size.x / source_size.x,
					control_size.y / source_size.y)
				if mode == TextureRect.STRETCH_KEEP_ASPECT_COVERED:
					scale_value = maxf(control_size.x / source_size.x,
						control_size.y / source_size.y)
				draw_size = source_size * scale_value
				if mode != TextureRect.STRETCH_KEEP_ASPECT:
					draw_origin = (control_size - draw_size) * 0.5
			if not Rect2(draw_origin, draw_size).has_point(local):
				return Color(0.0, 0.0, 0.0, 0.0)
			var uv := (local - draw_origin) / draw_size
			source = uv * source_size
		if bool(texture_rect.get("flip_h")):
			source.x = source_size.x - source.x
		if bool(texture_rect.get("flip_v")):
			source.y = source_size.y - source.y
	else:
		return Color(0.0, 0.0, 0.0, 0.0)
	var source_x := clampi(int(floor(source.x)), 0, image.get_width() - 1)
	var source_y := clampi(int(floor(source.y)), 0, image.get_height() - 1)
	return image.get_pixel(source_x, source_y) * _effective_canvas_modulate(node)


func _visual_alpha_at_screen_point(node: Node, point: Vector2,
		image_cache: Dictionary) -> float:
	return _visual_color_at_screen_point(node, point, image_cache).a


func _visual_has_unresolved_alpha_effect(node: Node) -> bool:
	# Source alpha is only authoritative when no material or group can discard,
	# recolor, or time-modulate those pixels. Unsupported render effects are
	# surfaced as a coverage gap by the caller, never sampled as if opaque.
	if not _visual_is_in_audited_viewport(node) or current_canvas_global_effects > 0:
		return true
	var current: Node = node
	while current != null:
		if current is CanvasGroup:
			return true
		if current is CanvasItem:
			var item := current as CanvasItem
			if item.material != null:
				return true
			if item.use_parent_material:
				return true
			# clip_children affects descendants. Control clip_contents is handled
			# geometrically below; other clipping modes need flattened evidence.
			if current != node and int(item.clip_children) \
					!= CanvasItem.CLIP_CHILDREN_DISABLED:
				return true
		elif current is CanvasLayer:
			var custom_viewport: Variant = current.get("custom_viewport")
			if custom_viewport is Viewport and custom_viewport != get_root():
				return true
		current = current.get_parent()
	return false


func _visual_is_in_audited_viewport(node: Node) -> bool:
	if not (node is CanvasItem) or node.get_viewport() != get_root():
		return false
	var viewport := node.get_viewport()
	var cull_value: Variant = viewport.get("canvas_cull_mask")
	var visibility_value: Variant = node.get("visibility_layer")
	if cull_value is int and visibility_value is int \
			and (int(cull_value) & int(visibility_value)) == 0:
		return false
	return true


func _effective_canvas_modulate(node: Node) -> Color:
	var tint := Color.WHITE
	var current: Node = node
	while current != null:
		if current is CanvasItem:
			var item := current as CanvasItem
			tint *= item.modulate
			if current == node:
				tint *= item.self_modulate
		# CanvasLayer contributes visibility and layer ordering, but it does not
		# expose CanvasItem.modulate/self_modulate. Treating it as a tinted
		# ancestor floods a fresh audit with invalid-property errors and prevents
		# the capture bundle from being written.
		current = current.get_parent()
	return tint


func _effective_canvas_opacity(node: Node) -> float:
	return clampf(_effective_canvas_modulate(node).a, 0.0, 1.0)


func _point_inside_canvas_clips(node: Node, point: Vector2) -> bool:
	# Control clip_contents is deterministic in Canvas space. Generic
	# CanvasItem clip_children was already marked unresolved above.
	var current := node.get_parent()
	while current != null:
		if current is Control and (current as Control).clip_contents:
			var control := current as Control
			var local := control.get_global_transform_with_canvas().affine_inverse() * point
			if not Rect2(Vector2.ZERO, control.size).has_point(local):
				return false
		current = current.get_parent()
	return true


func _unresolved_alpha_effect_count(visuals: Array[Node]) -> int:
	var count := 0
	for visual in visuals:
		if _visual_has_unresolved_alpha_effect(visual):
			count += 1
	return count


func _canvas_visual_list(node: Node) -> Array[Node]:
	var visuals: Array[Node] = []
	_collect_canvas_visuals(node, visuals)
	return visuals


func _painted_overlap(target_visuals: Array[Node], layer_visuals: Array[Node],
		target_rect: Rect2) -> Dictionary:
	var unresolved := _unresolved_alpha_effect_count(target_visuals) \
		+ _unresolved_alpha_effect_count(layer_visuals)
	if unresolved > 0:
		return {
			"overlap_px2": 0.0,
			"painted_sample_count": 0,
			"target_painted_sample_count": 0,
			"target_overlap_ratio": 0.0,
			"alpha_threshold": CANVAS_OCCLUSION_ALPHA_THRESHOLD,
			"unresolved_alpha_effects": unresolved,
		}
	var viewport := get_root().get_visible_rect()
	var sample_rect := target_rect.intersection(viewport)
	if sample_rect.size.x <= 0.0 or sample_rect.size.y <= 0.0:
		return {
			"overlap_px2": 0.0,
			"painted_sample_count": 0,
			"target_painted_sample_count": 0,
			"target_overlap_ratio": 0.0,
			"alpha_threshold": CANVAS_OCCLUSION_ALPHA_THRESHOLD,
			"unresolved_alpha_effects": 0,
		}
	var images: Dictionary = {}
	var overlap := 0.0
	var painted_samples := 0
	var target_painted_samples := 0
	var target_painted_area := 0.0
	var y := sample_rect.position.y + CANVAS_OCCLUSION_SAMPLE_STEP * 0.5
	while y < sample_rect.end.y:
		var x := sample_rect.position.x + CANVAS_OCCLUSION_SAMPLE_STEP * 0.5
		while x < sample_rect.end.x:
			var point := Vector2(x, y)
			var target_alpha := 0.0
			for visual in target_visuals:
				target_alpha = maxf(target_alpha,
					_visual_alpha_at_screen_point(visual, point, images))
			var layer_alpha := 0.0
			for visual in layer_visuals:
				layer_alpha = maxf(layer_alpha,
					_visual_alpha_at_screen_point(visual, point, images))
			if target_alpha >= CANVAS_OCCLUSION_ALPHA_THRESHOLD:
				target_painted_samples += 1
				target_painted_area += target_alpha \
					* CANVAS_OCCLUSION_SAMPLE_STEP * CANVAS_OCCLUSION_SAMPLE_STEP
			if target_alpha >= CANVAS_OCCLUSION_ALPHA_THRESHOLD \
					and layer_alpha >= CANVAS_OCCLUSION_ALPHA_THRESHOLD:
				painted_samples += 1
				overlap += target_alpha * layer_alpha \
					* CANVAS_OCCLUSION_SAMPLE_STEP * CANVAS_OCCLUSION_SAMPLE_STEP
			x += CANVAS_OCCLUSION_SAMPLE_STEP
		y += CANVAS_OCCLUSION_SAMPLE_STEP
	return {
		"overlap_px2": snappedf(overlap, 0.1),
		"painted_sample_count": painted_samples,
		"target_painted_sample_count": target_painted_samples,
		"target_overlap_ratio": snappedf(
			overlap / target_painted_area if target_painted_area > 0.0 else 0.0,
			0.0001),
		"alpha_threshold": CANVAS_OCCLUSION_ALPHA_THRESHOLD,
		"unresolved_alpha_effects": 0,
	}


func _canvas_painted_coverage(node: Node) -> float:
	var visuals: Array[Node] = []
	_collect_canvas_visuals(node, visuals)
	var grid_w := 64
	var grid_h := 36
	var viewport := get_root().get_visible_rect()
	if viewport.size.x <= 0.0 or viewport.size.y <= 0.0:
		return 0.0
	var painted := 0
	var image_cache: Dictionary = {}
	for gy in range(grid_h):
		for gx in range(grid_w):
			var point := Vector2(
				(float(gx) + 0.5) * viewport.size.x / float(grid_w),
				(float(gy) + 0.5) * viewport.size.y / float(grid_h))
			var hit := false
			for visual in visuals:
				if _visual_alpha_at_screen_point(visual, point, image_cache) >= 0.5:
					hit = true
					break
			if hit:
				painted += 1
	return float(painted) / float(grid_w * grid_h)


func _canvas_painted_composite_signature(visuals: Array[Node]) -> String:
	# Canonicalize what this layer paints at the same grid used for meaningful
	# coverage. File hashes alone can be gamed by transparent assets, PNG
	# encoding, crop, tiling, or transforms that render the same composition.
	var grid_w := 64
	var grid_h := 36
	var viewport := get_root().get_visible_rect()
	if viewport.size.x <= 0.0 or viewport.size.y <= 0.0:
		return ""
	var image_cache: Dictionary = {}
	var pixels := PackedByteArray()
	for gy in range(grid_h):
		for gx in range(grid_w):
			var point := Vector2(
				(float(gx) + 0.5) * viewport.size.x / float(grid_w),
				(float(gy) + 0.5) * viewport.size.y / float(grid_h))
			var premultiplied_r := 0.0
			var premultiplied_g := 0.0
			var premultiplied_b := 0.0
			var alpha := 0.0
			for visual in visuals:
				var sample := _visual_color_at_screen_point(visual, point, image_cache)
				var sample_alpha := clampf(sample.a, 0.0, 1.0)
				premultiplied_r = sample.r * sample_alpha \
					+ premultiplied_r * (1.0 - sample_alpha)
				premultiplied_g = sample.g * sample_alpha \
					+ premultiplied_g * (1.0 - sample_alpha)
				premultiplied_b = sample.b * sample_alpha \
					+ premultiplied_b * (1.0 - sample_alpha)
				alpha = sample_alpha + alpha * (1.0 - sample_alpha)
			var straight_r := premultiplied_r / alpha if alpha > 0.000001 else 0.0
			var straight_g := premultiplied_g / alpha if alpha > 0.000001 else 0.0
			var straight_b := premultiplied_b / alpha if alpha > 0.000001 else 0.0
			pixels.append(clampi(roundi(clampf(straight_r, 0.0, 1.0) * 255.0), 0, 255))
			pixels.append(clampi(roundi(clampf(straight_g, 0.0, 1.0) * 255.0), 0, 255))
			pixels.append(clampi(roundi(clampf(straight_b, 0.0, 1.0) * 255.0), 0, 255))
			pixels.append(clampi(roundi(alpha * 255.0), 0, 255))
	var context := HashingContext.new()
	context.start(HashingContext.HASH_SHA256)
	context.update(("%dx%d:" % [grid_w, grid_h]).to_utf8_buffer())
	context.update(pixels)
	return context.finish().hex_encode()


func _collect_canvas_visuals(node: Node, out: Array[Node]) -> void:
	if node is CanvasItem and not (node as CanvasItem).is_visible_in_tree():
		return
	if node is CanvasLayer and not (node as CanvasLayer).visible:
		return
	if node is Sprite2D or node is TextureRect:
		out.append(node)
	for child in node.get_children():
		_collect_canvas_visuals(child, out)


func _content_signature(paths: Array[String]) -> String:
	var hashes: Array[String] = []
	for path in paths:
		var image := Image.new()
		if image.load(ProjectSettings.globalize_path("res://" + path)) != OK:
			return ""
		image.convert(Image.FORMAT_RGBA8)
		var pixels := image.get_data()
		var has_visible_pixel := false
		for index in range(0, pixels.size(), 4):
			if pixels[index + 3] == 0:
				pixels[index] = 0
				pixels[index + 1] = 0
				pixels[index + 2] = 0
			else:
				has_visible_pixel = true
		if not has_visible_pixel:
			continue
		var context := HashingContext.new()
		context.start(HashingContext.HASH_SHA256)
		context.update(("%dx%d:" % [image.get_width(), image.get_height()]).to_utf8_buffer())
		context.update(pixels)
		hashes.append(context.finish().hex_encode())
	hashes.sort()
	return "|".join(hashes).sha256_text() if not hashes.is_empty() else ""


func _non_canvas_spatial_count(node: Node) -> int:
	# is_class follows native inheritance, so spatial descendants whose names
	# lack the usual suffix cannot masquerade as Canvas.
	var count := 1 if node.is_class("Node" + "3D") else 0
	for child in node.get_children():
		count += _non_canvas_spatial_count(child)
	return count


func _canvas_occlusion_facts(main: ReefMain, zone_id: String,
		_legacy_visible: int, capture_targets: Array) -> Dictionary:
	_refresh_canvas_global_effects()
	var layer_nodes: Array[Node] = []
	_collect_canvas_layers(main, layer_nodes)
	var samples: Array = []
	var unresolved_alpha_visuals: Dictionary = {}
	var unresolved_draw_visuals: Dictionary = {}
	for target_value in capture_targets:
		var target := target_value as Dictionary
		var target_nodes: Array = target.get("nodes", []) as Array
		var target_item: CanvasItem = null
		var target_rect := Rect2()
		var has_target_rect := false
		for node_value in target_nodes:
			var node := node_value as Node
			if not (node is CanvasItem) or not (node as CanvasItem).is_visible_in_tree():
				continue
			var rect := _visual_screen_rect(node)
			if rect.size.x <= 0.0 or rect.size.y <= 0.0:
				continue
			if target_item == null:
				target_item = node as CanvasItem
			target_rect = rect if not has_target_rect else target_rect.merge(rect)
			has_target_rect = true
		if target_item == null or not has_target_rect:
			continue
		var target_visuals: Array[Node] = []
		for target_node in target_nodes:
			_collect_canvas_visuals(target_node as Node, target_visuals)
		if target_visuals.is_empty():
			continue
		var target_order := _canvas_draw_order(target_visuals[0])
		for target_visual in target_visuals:
			if _visual_has_unresolved_alpha_effect(target_visual):
				unresolved_alpha_visuals[target_visual.get_instance_id()] = true
			if _canvas_draw_order(target_visual) != target_order \
					or _visual_has_ambiguous_draw_order(target_visual):
				unresolved_draw_visuals[target_visual.get_instance_id()] = true
		var behind: Array = []
		var front: Array = []
		for layer_node in layer_nodes:
			var layer_path := String(layer_node.get_path())
			var target_path := String(target.get("target_instance_path", ""))
			if target_path.begins_with(layer_path + "/") \
					or layer_path.begins_with(target_path + "/"):
				continue
			var layer_visuals: Array[Node] = []
			_collect_canvas_visuals(layer_node, layer_visuals)
			for layer_visual in layer_visuals:
				if _visual_has_unresolved_alpha_effect(layer_visual):
					unresolved_alpha_visuals[layer_visual.get_instance_id()] = true
			var layer_order := _canvas_draw_order(layer_node)
			if _draw_order_effect_count(layer_node, layer_visuals, layer_order) > 0:
				for layer_visual in layer_visuals:
					if _visual_has_ambiguous_draw_order(layer_visual, layer_node):
						unresolved_draw_visuals[layer_visual.get_instance_id()] = true
				continue
			var overlap_facts := _painted_overlap(
				target_visuals, layer_visuals, target_rect)
			var overlap := float(overlap_facts.get("overlap_px2", 0.0))
			if overlap <= 0.0 or int(overlap_facts.get("painted_sample_count", 0)) <= 0:
				continue
			var row := {
				"instance_path": layer_path,
				"draw_order": layer_order,
				"overlap_px2": snappedf(overlap, 0.1),
				"painted_sample_count": int(overlap_facts.get(
					"painted_sample_count", 0)),
				"target_painted_sample_count": int(overlap_facts.get(
					"target_painted_sample_count", 0)),
				"target_overlap_ratio": float(overlap_facts.get(
					"target_overlap_ratio", 0.0)),
				"alpha_threshold": float(overlap_facts.get(
					"alpha_threshold", 0.0)),
				"unresolved_alpha_effects": int(overlap_facts.get(
					"unresolved_alpha_effects", 0)),
				"overlap_method": CANVAS_OCCLUSION_METHOD,
				"sample_step_px": CANVAS_OCCLUSION_SAMPLE_STEP,
			}
			if layer_order < target_order:
				behind.append(row)
			elif layer_order > target_order:
				front.append(row)
		samples.append({
			"id": String(target.get("id", "")),
			"target_instance_path": String(target.get("target_instance_path", "")),
			"target_canvas_item": true,
			"target_visible": target_item.is_visible_in_tree(),
			"target_draw_order": target_order,
			"behind": behind,
			"front": front,
		})
	var facts := {
		"backend": "legacy_spatial" if _non_canvas_spatial_count(get_root()) > 0 else (
			"canvas_2d" if not layer_nodes.is_empty() else "missing"),
		"method": CANVAS_OCCLUSION_METHOD,
		"non_canvas_spatial_nodes": _non_canvas_spatial_count(get_root()),
		"unresolved_alpha_effects": unresolved_alpha_visuals.size(),
		"unresolved_draw_order_effects": unresolved_draw_visuals.size(),
		"samples": samples,
	}
	facts.merge(_runtime_block_provenance(main, zone_id))
	return facts


func _capture_rendered_states(main: ReefMain, zone_id: String,
		capture_targets: Array) -> Array:
	var config := _zone_config(zone_id)
	var required: Array = config.get("rendered_readability_states", []) as Array
	if required.is_empty():
		return []
	var current_states: Array[Dictionary] = []
	for value in required:
		var state: Dictionary = (value as Dictionary).duplicate(true)
		var state_id := String(state.get("id", ""))
		var adapter := String(state.get("capture_adapter", ""))
		var adapter_evidence := _capture_adapter_state(
			main, zone_id, state_id, adapter)
		if not adapter_evidence.is_empty():
			state["_adapter_evidence"] = adapter_evidence
			current_states.append(state)
	if current_states.is_empty():
		var live_state := {
			"focus": String(main.g.get("lagoon_promenade_focus", "")),
			"game": String(main.game),
			"intro_active": main.intro_active,
			"mg_kind": String(main.mg_kind),
			"phase": String(main.g.get("phase", "")),
			"play_animation_empty": (main.g.get(
				"lagoon_play_anim", {}) as Dictionary).is_empty(),
			"tree_paused": main.get_tree().paused,
			"world_controls_enabled": main.touch_ui != null \
				and bool(main.touch_ui.world_controls_enabled),
		}
		_log("%s_composite" % zone_id, true,
			"COVERAGE_GAP no adapter for live state %s" % live_state)
		return []
	if current_states.size() != 1:
		_log("%s_composite" % zone_id, true,
			"COVERAGE_GAP current probe implements exactly one asserted live-state adapter")
		return []
	if capture_targets.is_empty():
		_log("%s_composite" % zone_id, true,
			"COVERAGE_GAP no visible registered Canvas target instances")
		return []
	if DisplayServer.get_name() == "headless":
		_log("%s_composite" % zone_id, true,
			"COVERAGE_GAP headless display has no flattened viewport pixels")
		return []

	var original_process_mode := main.process_mode
	var original_time_scale := Engine.time_scale
	main.process_mode = Node.PROCESS_MODE_DISABLED
	Engine.time_scale = 0.0
	await _frames(2)
	if _refresh_canvas_global_effects() > 0:
		main.process_mode = original_process_mode
		Engine.time_scale = original_time_scale
		_log("%s_composite" % zone_id, true,
			"COVERAGE_GAP live root Canvas effects invalidate source-alpha reconstruction")
		return []
	var image := get_root().get_texture().get_image()
	if image == null or image.is_empty():
		main.process_mode = original_process_mode
		Engine.time_scale = original_time_scale
		_log("%s_composite" % zone_id, false, "viewport capture is empty")
		return []
	image.convert(Image.FORMAT_RGBA8)
	var out: Array = []
	for state in current_states:
		var state_id := String(state.get("id", "state"))
		var adapter_evidence: Dictionary = state.get(
			"_adapter_evidence", {}) as Dictionary
		var capture_write := _capture_path("%s_%s.png" % [zone_id, state_id])
		if image.save_png(capture_write) != OK:
			_log("%s_composite" % zone_id, false, "could not save flattened capture")
			continue
		var samples: Array = []
		for target_value in capture_targets:
			var target: Dictionary = target_value as Dictionary
			var sample := await _capture_target_difference(
				zone_id, state_id, target, image)
			if not sample.is_empty():
				samples.append(sample)
		var row: Dictionary = {
			"id": state_id,
			"capture_adapter": String(state.get("capture_adapter", "")),
			"adapter_method": String(adapter_evidence.get("method", "")),
			"adapter_state": adapter_evidence.get("state", {}),
			"adapter_state_signature": String(
				adapter_evidence.get("state_signature", "")),
			"source": "viewport_composite",
			"capture_path": _evidence_path(capture_write),
			"capture_sha256": FileAccess.get_sha256(capture_write),
			"viewport": [image.get_width(), image.get_height()],
			"art_sha256": _hash_map(_zone_paths(
				zone_id, ["murals", "standees", "characters"])),
			"samples": samples,
		}
		row.merge(_runtime_block_provenance(main, zone_id))
		row["provenance"] = {
			"builder_sha256": row["builder_sha256"],
			"art_sha256": row["art_sha256"],
		}
		out.append(row)
	main.process_mode = original_process_mode
	Engine.time_scale = original_time_scale
	await _frames(2)
	return out


func _capture_adapter_state(main: ReefMain, zone_id: String, state_id: String,
		adapter: String) -> Dictionary:
	# This is an executable dispatch, not a string-pattern acceptance rule.
	# Each added state needs its own transition/assertion branch here and a
	# verifier contract.  The current probe explicitly enters level 2 before
	# measuring and can therefore assert only the live promenade idle state.
	if zone_id != "sky_lagoon" or state_id != "promenade_idle" \
			or adapter != "probe_visual_audit:sky_lagoon_promenade_idle":
		return {}
	var play_animation: Dictionary = main.g.get(
		"lagoon_play_anim", {}) as Dictionary
	var world_controls_enabled := main.touch_ui != null \
		and bool(main.touch_ui.world_controls_enabled)
	if String(main.game) != "level2" \
			or String(main.g.get("phase", "")) != "promenade" \
			or String(main.mg_kind) != "" \
			or String(main.g.get("lagoon_promenade_focus", "")) != "" \
			or not play_animation.is_empty() or main.intro_active \
			or main.get_tree().paused or not world_controls_enabled:
		return {}
	var asserted_state := {
		"focus": "",
		"game": "level2",
		"intro_active": false,
		"mg_kind": "",
		"phase": "promenade",
		"play_animation_empty": true,
		"tree_paused": false,
		"world_controls_enabled": true,
		"zone": "sky_lagoon",
	}
	return {
		"method": CAPTURE_ADAPTER_METHOD,
		"state": asserted_state,
		"state_signature": JSON.stringify(
			asserted_state, "", true).sha256_text(),
	}


func _capture_target_difference(zone_id: String, state_id: String,
		target: Dictionary, visible_image: Image) -> Dictionary:
	var nodes: Array = target.get("nodes", []) as Array
	var bound_nodes: Array[CanvasItem] = []
	var original_visibility: Array[bool] = []
	var visuals: Array[Dictionary] = []
	var source_paths: Array[String] = []
	for value in nodes:
		var node := value as Node
		if not (node is CanvasItem):
			continue
		var item := node as CanvasItem
		if not item.is_visible_in_tree():
			continue
		var binding := _visual_binding(node)
		if binding.is_empty():
			continue
		bound_nodes.append(item)
		original_visibility.append(item.visible)
		visuals.append(binding)
		var path := String(binding.get("texture_path", ""))
		if path != "" and path not in source_paths:
			source_paths.append(path)
	if bound_nodes.is_empty():
		return {}
	var global_effect_seen := _refresh_canvas_global_effects() > 0
	for item in bound_nodes:
		item.visible = false
	await _frames(1)
	global_effect_seen = global_effect_seen or _refresh_canvas_global_effects() > 0
	var hidden := get_root().get_texture().get_image()
	await _frames(2)
	global_effect_seen = global_effect_seen or _refresh_canvas_global_effects() > 0
	var hidden_stable := get_root().get_texture().get_image()
	for index in range(bound_nodes.size()):
		bound_nodes[index].visible = original_visibility[index]
	await _frames(1)
	global_effect_seen = global_effect_seen or _refresh_canvas_global_effects() > 0
	var restored := get_root().get_texture().get_image()
	await _frames(3)
	global_effect_seen = global_effect_seen or _refresh_canvas_global_effects() > 0
	var restored_stable := get_root().get_texture().get_image()
	for item in bound_nodes:
		item.visible = false
	await _frames(2)
	global_effect_seen = global_effect_seen or _refresh_canvas_global_effects() > 0
	var hidden_repeat := get_root().get_texture().get_image()
	for index in range(bound_nodes.size()):
		bound_nodes[index].visible = original_visibility[index]
	await _frames(1)
	global_effect_seen = global_effect_seen or _refresh_canvas_global_effects() > 0
	var restored_repeat := get_root().get_texture().get_image()
	if global_effect_seen:
		return {}
	var temporal_images: Array[Image] = [hidden, hidden_stable, restored,
		restored_stable, hidden_repeat, restored_repeat]
	for temporal_image in temporal_images:
		if temporal_image == null or temporal_image.is_empty():
			return {}
		temporal_image.convert(Image.FORMAT_RGBA8)
	if hidden == null or hidden.is_empty() or restored == null or restored.is_empty():
		return {}
	var visible := visible_image.duplicate()
	visible.convert(Image.FORMAT_RGBA8)
	for temporal_image in temporal_images:
		if temporal_image.get_size() != visible.get_size():
			return {}
	if not (_images_equal(visible, restored)
			and _images_equal(visible, restored_stable)
			and _images_equal(visible, restored_repeat)
			and _images_equal(hidden, hidden_stable)
			and _images_equal(hidden, hidden_repeat)):
		_log("%s_%s_stability" % [zone_id, String(target.get("id", "target"))],
			true, "COVERAGE_GAP alternating visible/hidden frames are temporally unstable")
		return {}
	var mask := Image.create(visible.get_width(), visible.get_height(),
		false, Image.FORMAT_RGBA8)
	mask.fill(Color(0, 0, 0, 0))
	var wrote := false
	for y in range(visible.get_height()):
		for x in range(visible.get_width()):
			if visible.get_pixel(x, y) != hidden.get_pixel(x, y):
				mask.set_pixel(x, y, Color.WHITE)
				wrote = true
	if not wrote:
		return {}
	var rect := _mask_bounds(mask)
	if rect.size.x <= 0.0 or rect.size.y <= 0.0:
		return {}
	var safe_id := String(target.get("id", "target")).validate_filename()
	var stem := "%s_%s_%s" % [zone_id, state_id, safe_id]
	var hidden_write := _capture_path(stem + "_target_hidden.png")
	var hidden_stable_write := _capture_path(stem + "_target_hidden_stable.png")
	var hidden_repeat_write := _capture_path(stem + "_target_hidden_repeat.png")
	var restored_write := _capture_path(stem + "_target_restored.png")
	var restored_stable_write := _capture_path(stem + "_target_restored_stable.png")
	var restored_repeat_write := _capture_path(stem + "_target_restored_repeat.png")
	var mask_write := _capture_path(stem + "_mask.png")
	if hidden.save_png(hidden_write) != OK \
			or hidden_stable.save_png(hidden_stable_write) != OK \
			or hidden_repeat.save_png(hidden_repeat_write) != OK \
			or restored.save_png(restored_write) != OK \
			or restored_stable.save_png(restored_stable_write) != OK \
			or restored_repeat.save_png(restored_repeat_write) != OK \
			or mask.save_png(mask_write) != OK:
		return {}
	source_paths.sort()
	return {
		"id": String(target.get("id", "")),
		"target_instance_path": String(target.get("target_instance_path", "")),
		"visuals": visuals,
		"figure_rect": [int(rect.position.x), int(rect.position.y),
			int(rect.size.x), int(rect.size.y)],
		"target_hidden_source": "viewport_composite_target_hidden",
		"target_hidden_capture_path": _evidence_path(hidden_write),
		"target_hidden_capture_sha256": FileAccess.get_sha256(hidden_write),
		"target_hidden_stability_captures": [
			_capture_binding(hidden_stable_write),
			_capture_binding(hidden_repeat_write),
		],
		"target_restored_source": "viewport_composite_target_restored",
		"target_restored_capture_path": _evidence_path(restored_write),
		"target_restored_capture_sha256": FileAccess.get_sha256(restored_write),
		"target_visible_stability_captures": [
			_capture_binding(restored_stable_write),
			_capture_binding(restored_repeat_write),
		],
		"temporal_schedule_frames": [1, 2, 1, 3, 2, 1],
		"temporal_freeze_method": TEMPORAL_FREEZE_METHOD,
		"shader_time_scale": 0.0,
		"mask_path": _evidence_path(mask_write),
		"mask_sha256": FileAccess.get_sha256(mask_write),
		"mask_source": RENDERED_DIFF_METHOD,
		"projection_method": SOURCE_PROJECTION_METHOD,
		"mask_source_art": source_paths,
		"mask_source_sha256": _hash_map(source_paths),
	}


func _images_equal(first: Image, second: Image) -> bool:
	if first.get_size() != second.get_size() or first.get_format() != second.get_format():
		return false
	return first.get_data() == second.get_data()


func _capture_binding(path: String) -> Dictionary:
	return {"path": _evidence_path(path), "sha256": FileAccess.get_sha256(path)}


func _visual_binding(node: Node) -> Dictionary:
	if not (node is Sprite2D or node is TextureRect):
		return {}
	var item := node as CanvasItem
	var texture := _visual_texture(node)
	var texture_path := _visual_texture_path(node)
	if texture == null or texture_path == "" or not item.is_visible_in_tree():
		return {}
	var transform := item.get_global_transform_with_canvas()
	var local_rect := Rect2()
	var projection: Dictionary = {}
	if node is Sprite2D:
		var sprite := node as Sprite2D
		local_rect = sprite.get_rect()
		projection = {
			"kind": "Sprite2D",
			"region_enabled": sprite.region_enabled,
			"region_rect": _rect_values(sprite.region_rect),
			"hframes": sprite.hframes,
			"vframes": sprite.vframes,
			"frame_coords": [sprite.frame_coords.x, sprite.frame_coords.y],
			"flip_h": sprite.flip_h,
			"flip_v": sprite.flip_v,
			"centered": sprite.centered,
			"offset": [sprite.offset.x, sprite.offset.y],
		}
	else:
		var texture_rect := node as TextureRect
		local_rect = Rect2(Vector2.ZERO, texture_rect.size)
		projection = {
			"kind": "TextureRect",
			"stretch_mode": texture_rect.stretch_mode,
			"expand_mode": texture_rect.expand_mode,
			"flip_h": texture_rect.flip_h,
			"flip_v": texture_rect.flip_v,
			"control_size": [texture_rect.size.x, texture_rect.size.y],
			"clip_contents": texture_rect.clip_contents,
		}
	return {
		"instance_path": String(node.get_path()),
		"node_type": node.get_class(),
		"visible_in_tree": item.is_visible_in_tree(),
		"texture_path": texture_path,
		"texture_sha256": FileAccess.get_sha256("res://" + texture_path),
		"canvas_transform": [transform.x.x, transform.x.y,
			transform.y.x, transform.y.y, transform.origin.x, transform.origin.y],
		"local_rect": _rect_values(local_rect),
		"projection": projection,
	}


func _rect_values(rect: Rect2) -> Array:
	return [rect.position.x, rect.position.y, rect.size.x, rect.size.y]


func _mask_bounds(mask: Image) -> Rect2:
	var min_x := mask.get_width()
	var min_y := mask.get_height()
	var max_x := -1
	var max_y := -1
	for y in range(mask.get_height()):
		for x in range(mask.get_width()):
			if mask.get_pixel(x, y).a < 0.5:
				continue
			min_x = mini(min_x, x)
			min_y = mini(min_y, y)
			max_x = maxi(max_x, x)
			max_y = maxi(max_y, y)
	if max_x < min_x or max_y < min_y:
		return Rect2()
	return Rect2(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)


func _load_visual_spec() -> Dictionary:
	var file := FileAccess.open(SPEC_PATH, FileAccess.READ)
	if file == null:
		_log("spec", false, "could not read %s" % SPEC_PATH)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	file.close()
	if parsed is not Dictionary:
		_log("spec", false, "invalid JSON")
		return {}
	return parsed as Dictionary


func _zone_config(zone_id: String) -> Dictionary:
	var configs: Array = visual_spec.get("zones", []) as Array
	for value in configs:
		var config := value as Dictionary
		if String(config.get("id", "")) == zone_id:
			return config
	return {}


func _zone_paths(zone_id: String, keys: Array[String]) -> Array[String]:
	var config := _zone_config(zone_id)
	var out: Array[String] = []
	for key in keys:
		var patterns: Array = config.get(key, []) as Array
		for value in patterns:
			for path in _expand_pattern(String(value)):
				if path not in out:
					out.append(path)
	out.sort()
	return out


func _expand_pattern(pattern: String) -> Array[String]:
	var clean := pattern.trim_prefix("res://").replace("\\", "/")
	if "*" not in clean and "?" not in clean:
		return [clean] if FileAccess.file_exists("res://" + clean) else []
	var directory := clean.get_base_dir()
	var filename_pattern := clean.get_file()
	var out: Array[String] = []
	for filename in DirAccess.get_files_at("res://" + directory):
		if filename.match(filename_pattern):
			out.append(directory.path_join(filename).replace("\\", "/"))
	out.sort()
	return out


func _hash_map(paths: Array) -> Dictionary:
	var out: Dictionary = {}
	for value in paths:
		var path := String(value).trim_prefix("res://").replace("\\", "/")
		out[path] = FileAccess.get_sha256("res://" + path)
	return out


func _runtime_block_provenance(main: ReefMain, zone_id: String) -> Dictionary:
	var config := _zone_config(zone_id)
	return {
		"zone_id": zone_id,
		"root_instance_path": String(main.get_path()),
		"builder_sha256": _hash_map(config.get("builders", []) as Array),
		"run_identity": run_identity,
	}


func _evidence_contract() -> Dictionary:
	var version := Engine.get_version_info()
	return {
		"schema_version": EVIDENCE_SCHEMA_VERSION,
		"run_identity": run_identity,
		"run_nonce": run_nonce,
		"run_started_utc": run_started_utc,
		"fresh_challenge": fresh_challenge,
		"source_revision": source_revision,
		"git_revision": git_revision,
		"git_tree": git_tree,
		"git_dependencies_clean": git_dependencies_clean,
		"source_manifest": runtime_source_manifest,
		"files": {
			"probe": _file_binding("scripts/probe_visual_audit.gd"),
			"spec": _file_binding("tools/visual_audit_spec.json"),
			"scene": _file_binding("scenes/main.tscn"),
			"project": _file_binding("project.godot"),
			"main_script": _file_binding("scripts/main.gd"),
			"player_script": _file_binding("scripts/player.gd"),
			"game_2d_taxonomy": _file_binding("tools/audit_game_2d.py"),
			"auditor": _file_binding("tools/audit_visual_design.py"),
		},
		"engine": {
			"major": int(version.get("major", -1)),
			"minor": int(version.get("minor", -1)),
			"patch": int(version.get("patch", -1)),
			"status": String(version.get("status", "")),
			"version_string": String(version.get("string", "")),
		},
		"renderer": {
			"actual": String(RenderingServer.get_current_rendering_method()),
			"project_setting": String(ProjectSettings.get_setting(
				"rendering/renderer/rendering_method", "")),
		},
		"capture_context": {
			"viewport": [get_root().size.x, get_root().size.y],
			"stretch_mode": String(ProjectSettings.get_setting(
				"display/window/stretch/mode", "")),
			"stretch_aspect": String(ProjectSettings.get_setting(
				"display/window/stretch/aspect", "")),
		},
	}


func _file_binding(path: String) -> Dictionary:
	return {"path": path, "sha256": FileAccess.get_sha256("res://" + path)}


func _source_manifest() -> Dictionary:
	var paths: Array[String] = []
	_collect_source_files("res://", [
		".cs", ".gd", ".gdc", ".gde", ".gdextension", ".gdnlib",
		".gdshader", ".gdshaderinc", ".json", ".lua", ".tscn", ".tres",
	], paths)
	paths.sort()
	var entries: Array[String] = []
	for resource_path in paths:
		entries.append("%s:%s" % [resource_path.trim_prefix("res://"),
			FileAccess.get_sha256(resource_path)])
	return {
		"algorithm": "sha256_project_runtime_candidates_v2",
		"file_count": entries.size(),
		"sha256": "\n".join(entries).sha256_text(),
	}


func _source_revision(manifest: Dictionary) -> String:
	var paths: Array[String] = [
		"scripts/probe_visual_audit.gd",
		"tools/visual_audit_spec.json",
		"scenes/main.tscn",
		"project.godot",
		"scripts/main.gd",
		"scripts/player.gd",
		"tools/audit_game_2d.py",
		"tools/audit_visual_design.py",
	]
	paths.sort()
	var entries: Array[String] = [String(manifest.get("sha256", ""))]
	for path in paths:
		entries.append("%s:%s" % [path, FileAccess.get_sha256("res://" + path)])
	return "|".join(entries).sha256_text()


func _collect_source_files(directory: String, suffixes: Array[String],
		out: Array[String]) -> void:
	if not DirAccess.dir_exists_absolute(directory):
		return
	for filename in DirAccess.get_files_at(directory):
		for suffix in suffixes:
			if filename.ends_with(suffix):
				out.append(directory.path_join(filename))
				break
	for child_directory in DirAccess.get_directories_at(directory):
		if child_directory in [".git", ".godot", "__pycache__", "audit", "tmp"]:
			continue
		_collect_source_files(directory.path_join(child_directory), suffixes, out)


func _git_source_identity() -> Dictionary:
	var project_root := ProjectSettings.globalize_path("res://")
	var revision_result := _git_output(PackedStringArray([
		"-C", project_root, "rev-parse", "--verify", "HEAD",
	]))
	var tree_result := _git_output(PackedStringArray([
		"-C", project_root, "rev-parse", "HEAD^{tree}",
	]))
	var status_result := _git_output(PackedStringArray([
		"-C", project_root, "status", "--porcelain=v1", "--untracked-files=all",
	]))
	return {
		"revision": String(revision_result.get("output", "")),
		"tree": String(tree_result.get("output", "")),
		"dependencies_clean": int(status_result.get("exit_code", -1)) == 0 \
			and String(status_result.get("output", "")) == "",
	}


func _git_output(arguments: PackedStringArray) -> Dictionary:
	var output: Array = []
	var exit_code := OS.execute("git", arguments, output, true, false)
	var lines: Array[String] = []
	for value in output:
		lines.append(String(value).strip_edges())
	return {"exit_code": exit_code, "output": "\n".join(lines).strip_edges()}


func _requested_out_path() -> String:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--visual-facts-out="):
			return arg.trim_prefix("--visual-facts-out=")
	return DEFAULT_OUT_PATH


func _requested_challenge() -> String:
	for arg_value in OS.get_cmdline_user_args():
		var arg := String(arg_value)
		if arg.begins_with("--visual-audit-challenge="):
			var value: String = arg.trim_prefix(
				"--visual-audit-challenge=").to_lower()
			if value.length() == 64 and value.is_valid_hex_number(false):
				return value
	return ""


func _capture_path(filename: String) -> String:
	var directory := out_path.get_base_dir().path_join("visual_runtime_captures")
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(directory))
	return directory.path_join(filename)


func _evidence_path(path: String) -> String:
	if path.begins_with("res://"):
		return path.trim_prefix("res://")
	if path.begins_with("user://"):
		return ProjectSettings.globalize_path(path).replace("\\", "/")
	return path.replace("\\", "/")


func _write() -> void:
	var payload: Dictionary = {
		"_comment": "Generated by scripts/probe_visual_audit.gd. Consumed by tools/audit_visual_design.py.",
		"evidence_contract": _evidence_contract(),
		"zones": zones,
	}
	var text: String = JSON.stringify(payload, "\t", false)
	DirAccess.make_dir_recursive_absolute(
		ProjectSettings.globalize_path(out_path.get_base_dir()))
	var file := FileAccess.open(out_path, FileAccess.WRITE)
	if file == null:
		_log("write", false, "could not open %s" % out_path)
		return
	file.store_string(text + "\n")
	file.close()
	print("VISUALFACTS|written %s (%d zones)" % [out_path, zones.size()])
