extends SceneTree

## Deterministic Mobile-render evidence for the shipping Sky Lagoon promenade.
##
## This probe uses the child's production camera and current promenade states.
## It never creates a second review camera, follows retired courtyard roles, enters
## the Reef/Castle, or writes progress. Set SKY_LAGOON_SHOT_OUT to an absolute
## output folder. The workflow currently treats these artifacts as diagnostic.

const SCHEMA := "reef.sky_lagoon.visual_review.v1"
const PROBE_PATH := "res://scripts/probe_sky_lagoon_art.gd"
const VIEWPORT_SIZE := Vector2i(1280, 720)
const EXPECTED_TARGET_IDS: Array[String] = [
	"castle_gate", "reef_route", "seesaw", "slide", "swing",
]
const EXPECTED_CAPTURE_IDS: Array[String] = [
	"lagoon_01_arrival_plane_day",
	"lagoon_02_reef_route_return_day",
	"lagoon_03_reef_route_focus_day",
	"lagoon_04_otter_idle_day",
	"lagoon_05_frog_idle_day",
	"lagoon_06_hare_idle_day",
	"lagoon_07_squirrel_idle_day",
	"lagoon_08_playground_overview_day",
	"lagoon_09_slide_focus_day",
	"lagoon_10_slide_action_day",
	"lagoon_11_swing_focus_day",
	"lagoon_12_swing_action_day",
	"lagoon_13_seesaw_focus_day",
	"lagoon_14_seesaw_action_day",
	"lagoon_15_castle_overview_day",
	"lagoon_16_castle_focus_day",
	"lagoon_17_raccoon_idle_day",
	"lagoon_18_raccoon_startle_day",
	"lagoon_19_playground_overview_night",
	"lagoon_20_castle_focus_night",
]
const SAVE_SUFFIXES: Array[String] = [
	"", ".tmp0", ".tmp1", ".tmp", ".old", ".bak", ".bak.tmp", ".bak.old",
]
const GRID_W := 64
const GRID_H := 36
const NON_CLEAR_DISTANCE := 0.12
const MIN_NON_CLEAR_FRACTION := 0.35
const MIN_LUMA_SPAN := 0.20

var main: ReefMain
var promenade: SkyLagoonPromenade
var out_dir := ""
var captures: Array[Dictionary] = []
var global_failures: Array[Dictionary] = []
var abort_remaining := false
var manifest_written := false
var current_expected_index := 0
var normal_save_path := ""
var save_before: Dictionary = {}
var save_after: Dictionary = {}
var probe_save_before: Array[Dictionary] = []
var probe_save_after: Array[Dictionary] = []
var original_is_night := false
var original_had_plane_departed := false
var original_plane_departed: Variant = null
var restored_in_memory := false
var restored_time_of_day := false
var probe_write_calls := 0
var previous_process_mode := Node.PROCESS_MODE_INHERIT
var probe_save_path := ""
var save_was_remapped := false
var isolated_cleanup_ok := false
var dev_mode_neutralized := false


func _init() -> void:
	call_deferred("_run")


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _visible_named_node_exists(node: Node, wanted: StringName) -> bool:
	if node.name == wanted:
		if node is CanvasLayer and (node as CanvasLayer).visible:
			return true
		if node is CanvasItem and (node as CanvasItem).is_visible_in_tree():
			return true
	for child: Node in node.get_children():
		if _visible_named_node_exists(child, wanted):
			return true
	return false


func _object_has_property(object: Object, wanted: StringName) -> bool:
	for property_info: Dictionary in object.get_property_list():
		if StringName(property_info.get("name", "")) == wanted:
			return true
	return false


func _fail(capture_id: String, code: String, detail: String) -> void:
	global_failures.append({"capture_id": capture_id, "code": code, "detail": detail})
	print("LAGOONSHOT|%s|FAIL|%s|%s" % [capture_id, code, detail])


func _file_fingerprint(path: String) -> Dictionary:
	var exists := FileAccess.file_exists(path)
	return {
		"path": path.get_file(),
		"exists": exists,
		"sha256": FileAccess.get_sha256(path) if exists else "",
		"modified_time": FileAccess.get_modified_time(path) if exists else 0,
	}


func _artifact_fingerprints(base_path: String) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for suffix: String in SAVE_SUFFIXES:
		result.append(_file_fingerprint(base_path + suffix))
	return result


func _clear_prior_outputs() -> void:
	var directory := DirAccess.open(out_dir)
	if directory == null:
		return
	directory.list_dir_begin()
	while true:
		var name := directory.get_next()
		if name == "":
			break
		if not directory.current_is_dir() and ((name.begins_with("lagoon_") \
				and name.ends_with(".png")) \
				or name == "sky_lagoon_review_manifest.json"):
			DirAccess.remove_absolute(out_dir.path_join(name))
	directory.list_dir_end()


func _output_png_names() -> Array[String]:
	var names: Array[String] = []
	var directory := DirAccess.open(out_dir)
	if directory == null:
		return names
	directory.list_dir_begin()
	while true:
		var name := directory.get_next()
		if name == "":
			break
		if not directory.current_is_dir() and name.ends_with(".png"):
			names.append(name)
	directory.list_dir_end()
	names.sort()
	return names


func _expected_png_names() -> Array[String]:
	var names: Array[String] = []
	for capture_id: String in EXPECTED_CAPTURE_IDS:
		names.append(capture_id + ".png")
	names.sort()
	return names


func _same_fingerprints(before: Array, after: Array) -> bool:
	if before.size() != after.size():
		return false
	for index: int in range(before.size()):
		var a: Dictionary = before[index] as Dictionary
		var b: Dictionary = after[index] as Dictionary
		if bool(a.get("exists", false)) != bool(b.get("exists", false)) \
				or String(a.get("sha256", "")) != String(b.get("sha256", "")) \
				or int(a.get("modified_time", 0)) != int(b.get("modified_time", 0)):
			return false
	return true


func _target_by_id(target_id: String) -> Dictionary:
	for value: Variant in main.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == target_id:
			return target
	return {}


func _target_ids() -> Array[String]:
	var ids: Array[String] = []
	for value: Variant in main.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		ids.append(String(target.get("id", "")))
	ids.sort()
	return ids


func _node_on_screen(node: Variant) -> bool:
	if not (node is CanvasItem) or not is_instance_valid(node) \
			or not (node as CanvasItem).is_visible_in_tree():
		return false
	var point: Vector2 = (node as CanvasItem).get_global_transform_with_canvas().origin
	return Rect2(Vector2.ZERO, Vector2(VIEWPORT_SIZE)).has_point(
		point)


func _animal_atlas_frame(node: Sprite2D) -> int:
	if node == null or not node.region_enabled \
			or node.region_rect.size.x <= 0.0 or node.region_rect.size.y <= 0.0:
		return node.frame if node != null else -1
	var column: int = roundi(node.region_rect.position.x / node.region_rect.size.x)
	var row: int = roundi(node.region_rect.position.y / node.region_rect.size.y)
	return row * SkyLagoonPromenade.ANIMAL_ATLAS_COLUMNS + column


func _sprite_screen_rect(sprite: Sprite2D) -> Rect2:
	if sprite == null or not is_instance_valid(sprite) or sprite.texture == null \
			or not sprite.is_visible_in_tree():
		return Rect2()
	var draw_size: Vector2 = sprite.region_rect.size if sprite.region_enabled \
		else sprite.texture.get_size()
	var local_origin: Vector2 = sprite.offset
	if sprite.centered:
		local_origin -= draw_size * 0.5
	var transform: Transform2D = sprite.get_global_transform_with_canvas()
	var corners: Array[Vector2] = [
		transform * local_origin,
		transform * (local_origin + Vector2(draw_size.x, 0.0)),
		transform * (local_origin + draw_size),
		transform * (local_origin + Vector2(0.0, draw_size.y)),
	]
	var bounds := Rect2(corners[0], Vector2.ZERO)
	for corner: Vector2 in corners:
		bounds = bounds.expand(corner)
	return bounds


func _alpha_sprite_screen_rect(sprite: Sprite2D) -> Rect2:
	if sprite == null or not is_instance_valid(sprite) or sprite.texture == null \
			or not sprite.is_visible_in_tree():
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
			if image.get_pixel(x, y).a < 0.10:
				continue
			var local := Vector2i(x, y) - source.position
			alpha_min.x = mini(alpha_min.x, local.x)
			alpha_min.y = mini(alpha_min.y, local.y)
			alpha_max.x = maxi(alpha_max.x, local.x)
			alpha_max.y = maxi(alpha_max.y, local.y)
	if alpha_max.x < alpha_min.x or alpha_max.y < alpha_min.y:
		return Rect2()
	var used := Rect2i(alpha_min, alpha_max - alpha_min + Vector2i.ONE)
	var local_origin := Vector2(used.position) + sprite.offset
	if sprite.centered:
		local_origin -= Vector2(source.size) * 0.5
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


func _polygon_screen_rect(polygon: Polygon2D) -> Rect2:
	if polygon == null or not is_instance_valid(polygon) \
			or not polygon.is_visible_in_tree() or polygon.polygon.is_empty():
		return Rect2()
	var transform: Transform2D = polygon.get_global_transform_with_canvas()
	var bounds := Rect2(transform * polygon.polygon[0], Vector2.ZERO)
	for point: Vector2 in polygon.polygon:
		bounds = bounds.expand(transform * point)
	return bounds


func _canvas_composite_screen_rect(node: Node) -> Rect2:
	var bounds := Rect2()
	var has_bounds := false
	var own_bounds := Rect2()
	if node is Sprite2D:
		own_bounds = _sprite_screen_rect(node as Sprite2D)
	elif node is Polygon2D:
		own_bounds = _polygon_screen_rect(node as Polygon2D)
	if own_bounds.get_area() > 0.0:
		bounds = own_bounds
		has_bounds = true
	for child: Node in node.get_children():
		var child_bounds: Rect2 = _canvas_composite_screen_rect(child)
		if child_bounds.get_area() <= 0.0:
			continue
		bounds = child_bounds if not has_bounds else bounds.merge(child_bounds)
		has_bounds = true
	return bounds if has_bounds else Rect2()


func _point_rect_distance(point: Vector2, bounds: Rect2) -> float:
	if bounds.get_area() <= 0.0:
		return INF
	var nearest := Vector2(
		clampf(point.x, bounds.position.x, bounds.end.x),
		clampf(point.y, bounds.position.y, bounds.end.y))
	return point.distance_to(nearest)


func _color_luma(color: Color) -> float:
	return color.r * 0.2126 + color.g * 0.7152 + color.b * 0.0722


func _selected_tint_is_readable(highlight: Sprite2D) -> bool:
	var tint: Color = highlight.modulate
	var high: float = maxf(tint.r, maxf(tint.g, tint.b))
	var low: float = minf(tint.r, minf(tint.g, tint.b))
	return tint.a >= 0.80 and tint.a <= 1.001 \
		and high >= 0.80 and high - low >= 0.35


func _procedural_pointer_contrast(highlight: Sprite2D) -> bool:
	var outline: Polygon2D = highlight.find_child(
		"PointerOutline", false, false) as Polygon2D
	var fill: Polygon2D = highlight.find_child(
		"PointerFill", false, false) as Polygon2D
	if outline == null or fill == null:
		return false
	var tint: Color = highlight.modulate
	var outline_tinted := Color(
		outline.color.r * tint.r, outline.color.g * tint.g,
		outline.color.b * tint.b, outline.color.a * tint.a)
	var fill_tinted := Color(
		fill.color.r * tint.r, fill.color.g * tint.g,
		fill.color.b * tint.b, fill.color.a * tint.a)
	return absf(_color_luma(fill_tinted) - _color_luma(outline_tinted)) >= 0.35


func _animal_overlap_fraction() -> float:
	var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
	var animal: Sprite2D = actor.get("node") as Sprite2D
	var animal_rect: Rect2 = _sprite_screen_rect(animal)
	if animal_rect.get_area() <= 0.0:
		return 0.0
	var highest := 0.0
	var roshan: Sprite2D = main.g.get("lagoon_roshan_card") as Sprite2D
	for sprite: Sprite2D in [roshan]:
		var other: Rect2 = _sprite_screen_rect(sprite)
		if other.get_area() > 0.0:
			highest = maxf(highest, animal_rect.intersection(other).get_area() \
				/ minf(animal_rect.get_area(), other.get_area()))
	for value: Variant in main.g.get("lagoon_promenade_targets", []) as Array:
		var prop: Sprite2D = (value as Dictionary).get("node") as Sprite2D
		var other: Rect2 = _sprite_screen_rect(prop)
		if other.get_area() > 0.0:
			highest = maxf(highest, animal_rect.intersection(other).get_area() \
				/ minf(animal_rect.get_area(), other.get_area()))
	return highest


func _highlight_contract() -> bool:
	var focus_id: String = String(main.g.get("lagoon_promenade_focus", ""))
	for target_id: String in EXPECTED_TARGET_IDS:
		var target: Dictionary = _target_by_id(target_id)
		var highlight: Sprite2D = target.get("highlight") as Sprite2D
		if highlight == null or highlight.texture == null:
			return false
		var alpha: float = highlight.modulate.a
		if target_id == focus_id:
			var cue_bounds: Rect2 = _canvas_composite_screen_rect(highlight)
			if minf(cue_bounds.size.x, cue_bounds.size.y) < 64.0 \
					or not _selected_tint_is_readable(highlight):
				return false
			var node: CanvasItem = target.get("node") as CanvasItem
			var target_anchor: Vector2 = (node as Node2D).get_global_transform_with_canvas().origin \
				if node is Node2D else Vector2(INF, INF)
			var target_bounds: Rect2 = _alpha_sprite_screen_rect(node as Sprite2D) \
				if node is Sprite2D else Rect2(
					target_anchor - Vector2(0.5, 0.5), Vector2.ONE)
			if _point_rect_distance(cue_bounds.get_center(), target_bounds) > 96.0:
				return false
			if target_id != "castle_gate":
				if String(highlight.get_meta("focus_cue_role", "")) \
						!= "procedural_ring_pointer" \
						or not _procedural_pointer_contrast(highlight):
					return false
				var tip_local: Variant = highlight.get_meta("pointer_tip_local")
				if not (tip_local is Vector2):
					return false
				var tip_screen: Vector2 = highlight.get_global_transform_with_canvas() \
					* (tip_local as Vector2)
				if _point_rect_distance(tip_screen, target_bounds) > 4.0:
					return false
		elif alpha > 0.06:
			return false
		if target_id != "castle_gate" \
				and String(highlight.get_meta("focus_cue_role", "")) \
					!= "procedural_ring_pointer":
			return false
	return true


func _target_screen_state() -> Dictionary:
	var result := {}
	for target_id: String in EXPECTED_TARGET_IDS:
		var target := _target_by_id(target_id)
		result[target_id] = _node_on_screen(target.get("node") as CanvasItem)
	return result


func _route_state() -> String:
	var plane: Variant = main.g.get("lagoon_plane_card")
	var marker: Variant = main.g.get("lagoon_reef_route_card")
	var plane_valid := plane != null and is_instance_valid(plane)
	var marker_valid := marker != null and is_instance_valid(marker)
	if plane_valid and not marker_valid:
		return "arrival_plane"
	if marker_valid and not plane_valid:
		return "reef_return"
	return "invalid"


func _review_layers_hidden() -> bool:
	return (main.hud_layer == null or not main.hud_layer.visible) \
		and (main.touch_ui == null or not main.touch_ui.visible) \
		and (main.pause_layer == null or not main.pause_layer.visible)


func _actual_state() -> Dictionary:
	var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
	var animal_node: Node = actor.get("node") as Node
	var play: Dictionary = main.g.get("lagoon_play_anim", {}) as Dictionary
	var stage_root: CanvasLayer = promenade.root() if promenade != null else null
	var roshan_card: CanvasItem = main.g.get("lagoon_roshan_card") as CanvasItem
	var camera: Camera2D = promenade.camera_2d() if promenade != null else null
	var fireflies: Variant = main.g.get("lagoon_night_fireflies")
	var camera_page := clampi(floori(float(
		main.g.get("lagoon_camera_x", -1.0)) / 2048.0), 0, 2)
	var target_nodes_valid := true
	var target_highlights_valid := true
	for target_id: String in EXPECTED_TARGET_IDS:
		var target := _target_by_id(target_id)
		var target_node: CanvasItem = target.get("node") as CanvasItem
		var highlight: CanvasItem = target.get("highlight") as CanvasItem
		target_nodes_valid = target_nodes_valid and target_node != null \
			and is_instance_valid(target_node)
		target_highlights_valid = target_highlights_valid and highlight != null \
			and is_instance_valid(highlight)
	var animal_texture := ""
	var animal_lighting_profile := ""
	if animal_node != null and is_instance_valid(animal_node):
		var texture: Texture2D = animal_node.get("texture") as Texture2D
		animal_texture = texture.resource_path if texture != null else ""
		animal_lighting_profile = String(animal_node.get_meta("animal_lighting_profile", ""))
	var equipment: CanvasItem = play.get("equipment") as CanvasItem
	return {
		"game": main.game,
		"phase": String(main.g.get("phase", "")),
		"mg_kind": main.mg_kind,
		"time_of_day": "night" if main.is_night else "day",
		"route_state": _route_state(),
		"active_canvas_camera": camera != null and is_instance_valid(camera) \
			and camera.enabled and get_root().get_viewport().get_camera_2d() == camera \
			and get_root().get_viewport().get_camera_3d() == null,
		"target_ids": _target_ids(),
		"target_nodes_valid": target_nodes_valid,
		"target_highlights_valid": target_highlights_valid,
		"target_on_screen": _target_screen_state(),
		"stage_root_valid": stage_root != null and is_instance_valid(stage_root),
		"roshan_card_valid": roshan_card != null and is_instance_valid(roshan_card),
		"roshan_card_visible": roshan_card != null and is_instance_valid(roshan_card) \
			and roshan_card.visible,
		"camera_page": camera_page,
		"master_x": float(main.g.get("lagoon_master_x", INF)),
		"camera_master_x": float(main.g.get("lagoon_camera_x", INF)),
		"focus": String(main.g.get("lagoon_promenade_focus", "")),
		"action_label": promenade.action_label() if promenade != null else "",
		"play_kind": String(play.get("kind", "")),
		"play_phase": String(play.get("phase", "")),
		"play_t": float(play.get("t", 0.0)),
		"play_frame_index": int(play.get("frame_index", -1)),
		"play_subject_on_screen": not play.is_empty() and _node_on_screen(roshan_card) \
			and equipment != null and is_instance_valid(equipment) and _node_on_screen(equipment),
		"animal_id": String((actor.get("definition", {}) as Dictionary).get("id", "")),
		"animal_state": String(actor.get("state", "")),
		"animal_page": int(actor.get("page", -1)),
		"animal_frame": _animal_atlas_frame(animal_node as Sprite2D) \
			if animal_node is Sprite2D and is_instance_valid(animal_node) else -1,
		"animal_visible": animal_node != null and is_instance_valid(animal_node) \
			and bool(animal_node.get("visible")),
		"animal_on_screen": _node_on_screen(animal_node),
		"animal_texture": animal_texture,
		"animal_lighting_profile": animal_lighting_profile,
		"animal_overlap_fraction": _animal_overlap_fraction(),
		"highlight_contract": _highlight_contract(),
		"castle_armed": bool(main.g.get("lagoon_castle_armed", false)),
		"fireflies_present": main.g.get("lagoon_night_fireflies") is Array \
			and not (main.g.get("lagoon_night_fireflies") as Array).is_empty(),
		"review_layers_hidden": _review_layers_hidden(),
		"dev_mode_neutralized": dev_mode_neutralized and main.dev_mode == null,
	}


func _assertion(code: String, passed: bool, expected: Variant,
		actual: Variant) -> Dictionary:
	return {"code": code, "passed": passed, "expected": expected, "actual": actual}


func _semantic_assertions(expected: Dictionary, actual: Dictionary) -> Array[Dictionary]:
	var assertions: Array[Dictionary] = []
	for key: String in ["game", "phase", "mg_kind", "time_of_day", "route_state",
			"focus", "action_label", "play_kind", "play_phase", "animal_id",
			"animal_state", "animal_page", "animal_frame", "animal_visible", "castle_armed",
			"animal_on_screen", "animal_texture", "animal_lighting_profile",
			"play_frame_index", "play_subject_on_screen", "fireflies_present"]:
		if expected.has(key):
			assertions.append(_assertion(key, actual.get(key) == expected[key],
				expected[key], actual.get(key)))
	assertions.append(_assertion("active_canvas_camera",
		bool(actual.get("active_canvas_camera", false)), true,
		actual.get("active_canvas_camera")))
	assertions.append(_assertion("target_ids",
		actual.get("target_ids") == EXPECTED_TARGET_IDS, EXPECTED_TARGET_IDS,
		actual.get("target_ids")))
	for integrity_key: String in ["target_nodes_valid", "target_highlights_valid",
			"stage_root_valid", "roshan_card_valid", "roshan_card_visible",
			"dev_mode_neutralized", "highlight_contract"]:
		assertions.append(_assertion(integrity_key,
			bool(actual.get(integrity_key, false)), true, actual.get(integrity_key)))
	assertions.append(_assertion("review_layers_hidden",
		bool(actual.get("review_layers_hidden", false)), true,
		actual.get("review_layers_hidden")))
	if expected.has("camera_page"):
		assertions.append(_assertion("camera_page",
			int(actual.get("camera_page", -1)) == int(expected["camera_page"]),
			expected["camera_page"], actual.get("camera_page")))
	if expected.has("play_t"):
		assertions.append(_assertion("play_t",
			is_equal_approx(float(actual.get("play_t", -1.0)), float(expected["play_t"])),
			expected["play_t"], actual.get("play_t")))
	if expected.has("onscreen_targets"):
		var target_screen: Dictionary = actual.get("target_on_screen", {}) as Dictionary
		for target_id: String in expected["onscreen_targets"] as Array:
			assertions.append(_assertion("onscreen_target_%s" % target_id,
				bool(target_screen.get(target_id, false)), true,
				target_screen.get(target_id)))
	if expected.get("animal_visible", false):
		assertions.append(_assertion("animal_clear_of_roshan_and_props",
			float(actual.get("animal_overlap_fraction", 1.0)) <= 0.20, "<=0.20",
			actual.get("animal_overlap_fraction")))
	return assertions


func _all_assertions_pass(assertions: Array[Dictionary]) -> bool:
	for assertion: Dictionary in assertions:
		if not bool(assertion.get("passed", false)):
			return false
	return true


func _median(values: Array[float]) -> float:
	values.sort()
	if values.is_empty():
		return 0.0
	var middle: int = values.size() / 2
	if values.size() % 2 == 0:
		return (values[middle - 1] + values[middle]) * 0.5
	return values[middle]


func _nonblank_metrics(source: Image) -> Dictionary:
	var image: Image = source.duplicate()
	image.convert(Image.FORMAT_RGBA8)
	var width: int = image.get_width()
	var height: int = image.get_height()
	var refs_r: Array[float] = []
	var refs_g: Array[float] = []
	var refs_b: Array[float] = []
	for gy: int in range(GRID_H):
		for gx: int in range(GRID_W):
			if not ((gx < 4 or gx >= GRID_W - 4) and (gy < 4 or gy >= GRID_H - 4)):
				continue
			var x: int = clampi(floori((float(gx) + 0.5) * float(width) / float(GRID_W)), 0, width - 1)
			var y: int = clampi(floori((float(gy) + 0.5) * float(height) / float(GRID_H)), 0, height - 1)
			var color: Color = image.get_pixel(x, y)
			refs_r.append(color.r)
			refs_g.append(color.g)
			refs_b.append(color.b)
	var reference: Color = Color(_median(refs_r), _median(refs_g), _median(refs_b), 1.0)
	var lumas: Array[float] = []
	var non_clear: int = 0
	for gy: int in range(GRID_H):
		for gx: int in range(GRID_W):
			var x: int = clampi(floori((float(gx) + 0.5) * float(width) / float(GRID_W)), 0, width - 1)
			var y: int = clampi(floori((float(gy) + 0.5) * float(height) / float(GRID_H)), 0, height - 1)
			var color: Color = image.get_pixel(x, y)
			var dr: float = color.r - reference.r
			var dg: float = color.g - reference.g
			var db: float = color.b - reference.b
			if sqrt(dr * dr + dg * dg + db * db) >= NON_CLEAR_DISTANCE:
				non_clear += 1
			lumas.append(0.2126 * color.r + 0.7152 * color.g + 0.0722 * color.b)
	lumas.sort()
	var sample_count: int = GRID_W * GRID_H
	var p05: float = lumas[floori(float(sample_count - 1) * 0.05)]
	var p95: float = lumas[floori(float(sample_count - 1) * 0.95)]
	var fraction: float = float(non_clear) / float(sample_count)
	var span: float = p95 - p05
	return {
		"method": "corner_reference_grid_64x36_v1",
		"sample_count": sample_count,
		"reference_sample_count": refs_r.size(),
		"reference_rgb": [reference.r, reference.g, reference.b],
		"distance_threshold": NON_CLEAR_DISTANCE,
		"minimum_non_clear_fraction": MIN_NON_CLEAR_FRACTION,
		"minimum_luma_span": MIN_LUMA_SPAN,
		"non_clear_fraction": fraction,
		"luma_p05": p05,
		"luma_p95": p95,
		"luma_span": span,
		"passed": width == VIEWPORT_SIZE.x and height == VIEWPORT_SIZE.y \
			and fraction >= MIN_NON_CLEAR_FRACTION and span >= MIN_LUMA_SPAN,
	}


func _capture(capture_id: String, expected: Dictionary,
		coverage: Array[String]) -> void:
	if current_expected_index >= EXPECTED_CAPTURE_IDS.size() \
			or EXPECTED_CAPTURE_IDS[current_expected_index] != capture_id:
		_fail(capture_id, "capture_order", "expected index %d" % current_expected_index)
		abort_remaining = true
		return
	current_expected_index += 1
	main.g["lagoon_castle_armed"] = false if expected.get("castle_armed") == false \
		else main.g.get("lagoon_castle_armed", false)
	var before_state := _actual_state()
	var assertions := _semantic_assertions(expected, before_state)
	var prior_mode := main.process_mode
	main.process_mode = Node.PROCESS_MODE_DISABLED
	await process_frame
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var file_name := capture_id + ".png"
	var file_path := out_dir.path_join(file_name)
	if FileAccess.file_exists(file_path):
		DirAccess.remove_absolute(file_path)
	var save_error := image.save_png(file_path)
	var after_state := _actual_state()
	main.process_mode = prior_mode
	var after_assertions := _semantic_assertions(expected, after_state)
	for assertion: Dictionary in after_assertions:
		var copied := assertion.duplicate(true)
		copied["code"] = "post_%s" % String(assertion["code"])
		assertions.append(copied)
	var nonblank := _nonblank_metrics(image)
	assertions.append(_assertion("viewport_dimensions",
		image.get_size() == VIEWPORT_SIZE, [VIEWPORT_SIZE.x, VIEWPORT_SIZE.y],
		[image.get_width(), image.get_height()]))
	assertions.append(_assertion("png_write", save_error == OK, OK, save_error))
	assertions.append(_assertion("nonblank", bool(nonblank.get("passed", false)), true,
		nonblank.get("passed")))
	var failures: Array[Dictionary] = []
	for assertion: Dictionary in assertions:
		if not bool(assertion.get("passed", false)):
			failures.append({
				"code": assertion.get("code", "assertion"),
				"detail": "expected=%s actual=%s" % [
					str(assertion.get("expected")), str(assertion.get("actual"))],
			})
	var passed := failures.is_empty()
	var row := {
		"id": capture_id,
		"file": file_name,
		"status": "PASS" if passed else "FAIL",
		"coverage": coverage,
		"expected_state": expected,
		"actual_state": after_state,
		"assertions": assertions,
		"image": {
			"width": image.get_width(),
			"height": image.get_height(),
			"sha256": FileAccess.get_sha256(file_path) if save_error == OK else "",
			"save_error": save_error,
			"nonblank": nonblank,
		},
		"failures": failures,
	}
	captures.append(row)
	if passed:
		print("LAGOONSHOT|%s|PASS" % capture_id)
	else:
		for failure: Dictionary in failures:
			_fail(capture_id, String(failure["code"]), String(failure["detail"]))
		abort_remaining = true


func _record_root_failure(capture_id: String, code: String, detail: String,
		expected: Dictionary = {}) -> void:
	if current_expected_index >= EXPECTED_CAPTURE_IDS.size() \
			or EXPECTED_CAPTURE_IDS[current_expected_index] != capture_id:
		_fail(capture_id, "capture_order", "root failure at index %d" % current_expected_index)
		abort_remaining = true
		return
	current_expected_index += 1
	_fail(capture_id, code, detail)
	captures.append({
		"id": capture_id,
		"file": capture_id + ".png",
		"status": "FAIL",
		"coverage": [],
		"expected_state": expected,
		"actual_state": _actual_state() if main != null and promenade != null else {},
		"assertions": [],
		"image": {},
		"failures": [{"code": code, "detail": detail}],
	})
	abort_remaining = true


func _skip_remaining(reason: String) -> void:
	while current_expected_index < EXPECTED_CAPTURE_IDS.size():
		var capture_id := EXPECTED_CAPTURE_IDS[current_expected_index]
		current_expected_index += 1
		captures.append({
			"id": capture_id,
			"file": capture_id + ".png",
			"status": "SKIPPED",
			"coverage": [],
			"expected_state": {},
			"actual_state": _actual_state() if main != null and promenade != null else {},
			"assertions": [],
			"image": {},
			"failures": [{"code": "prior_failure", "detail": reason}],
		})
		print("LAGOONSHOT|%s|SKIPPED|prior_failure|%s" % [capture_id, reason])


func _hide_interface() -> void:
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.touch_ui != null:
		main.touch_ui.visible = false
	if main.pause_layer != null:
		main.pause_layer.visible = false


func _move_to_mural_x(mural_x: float, castle_guard := false) -> void:
	main.g["lagoon_walk_goal_master"] = null
	if castle_guard:
		main.g["lagoon_castle_armed"] = false
	promenade.set_master_route_x(mural_x)
	await _frames(2)
	if castle_guard:
		main.g["lagoon_castle_armed"] = false
	promenade._sync_target_mural_anchors()


func _suppress_animal() -> void:
	var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
	if not actor.is_empty():
		promenade._hide_animal(actor, 3600.0, false)


func _finish_play_action() -> bool:
	promenade._finish_playground_animation()
	promenade._tick_playground_animation(1.0)
	return (main.g.get("lagoon_play_anim", {}) as Dictionary).is_empty()


func _focus_target(target_id: String) -> bool:
	var target := _target_by_id(target_id)
	if target.is_empty():
		return false
	promenade._focus(target)
	return true


func _animal_definition(animal_id: String) -> Dictionary:
	for definition: Dictionary in SkyLagoonPromenade.ANIMAL_DEFS:
		if String(definition.get("id", "")) == animal_id:
			return definition
	return {}


func _expect_animal(expected: Dictionary, animal_id: String,
		state: String, frame: int, lighting: String) -> void:
	var definition := _animal_definition(animal_id)
	expected["animal_id"] = animal_id
	expected["animal_state"] = state
	expected["animal_page"] = int(definition.get("page", -1))
	expected["animal_frame"] = frame
	expected["animal_visible"] = true
	expected["animal_on_screen"] = true
	expected["animal_lighting_profile"] = "canvas_day_night_tint"
	expected["animal_texture"] = String(definition.get(
		"startle" if state == "startle" else "idle", ""))


func _validate_scene(expect_departed: bool, night: bool) -> bool:
	var stage_root: CanvasLayer = promenade.root()
	var card: CanvasItem = main.g.get("lagoon_roshan_card") as CanvasItem
	var ok: bool = main.game == "level2" and String(main.g.get("phase", "")) == "promenade" \
		and main.mg_kind == "" and main.quality == "speedy" \
		and main.is_night == night and stage_root != null and is_instance_valid(stage_root) \
		and card != null and is_instance_valid(card) and _target_ids() == EXPECTED_TARGET_IDS \
		and _route_state() == ("reef_return" if expect_departed else "arrival_plane") \
		and promenade.camera_2d() != null \
		and get_root().get_viewport().get_camera_2d() == promenade.camera_2d() \
		and get_root().get_viewport().get_camera_3d() == null \
		and not _visible_named_node_exists(get_root(), &"StartMenu") \
		and main.player != null and not main.player.visible
	for target_id: String in EXPECTED_TARGET_IDS:
		var target := _target_by_id(target_id)
		var node: CanvasItem = target.get("node") as CanvasItem
		var highlight: CanvasItem = target.get("highlight") as CanvasItem
		ok = ok and not target.is_empty() and node != null and is_instance_valid(node) \
			and highlight != null and is_instance_valid(highlight)
	var fireflies: Variant = main.g.get("lagoon_night_fireflies")
	if night:
		ok = ok and fireflies is Array and not (fireflies as Array).is_empty()
	else:
		ok = ok and not main.g.has("lagoon_night_fireflies")
	return ok


func _build_promenade(expect_departed: bool, night: bool) -> bool:
	main.is_night = night
	main.save_data["lagoon_plane_departed"] = expect_departed
	main.save_pending = false
	main.save_dirty = false
	main._enter_level2_now(false, false, false)
	await _frames(8)
	promenade = main._lagoon_promenade_ref()
	_hide_interface()
	main.save_pending = false
	main.save_dirty = false
	return _validate_scene(expect_departed, night)


func _base_expected(route: String, night := false) -> Dictionary:
	return {
		"game": "level2",
		"phase": "promenade",
		"mg_kind": "",
		"time_of_day": "night" if night else "day",
		"route_state": route,
		"focus": "",
		"action_label": "JUMP",
		"play_kind": "",
		"play_phase": "",
		"animal_visible": false,
		"castle_armed": false,
		"fireflies_present": night,
	}


func _capture_base(capture_id: String, expected: Dictionary,
		coverage: Array[String]) -> bool:
	await _capture(capture_id, expected, coverage)
	return not abort_remaining


func _run_capture_sequence() -> void:
	if not await _build_promenade(false, false):
		_record_root_failure(EXPECTED_CAPTURE_IDS[0], "scene_readiness",
			"arrival promenade not ready")
		return
	await _move_to_mural_x(610.0)
	_suppress_animal()
	promenade._clear_focus()
	var expected := _base_expected("arrival_plane")
	expected["camera_page"] = 0
	expected["onscreen_targets"] = ["reef_route"]
	if not await _capture_base(EXPECTED_CAPTURE_IDS[0], expected,
			["arrival", "plane", "production_camera", "day"]):
		return

	if not await _build_promenade(true, false):
		_record_root_failure(EXPECTED_CAPTURE_IDS[1], "scene_readiness",
			"return promenade not ready")
		return
	await _move_to_mural_x(610.0)
	_suppress_animal()
	promenade._clear_focus()
	expected = _base_expected("reef_return")
	expected["camera_page"] = 0
	expected["onscreen_targets"] = ["reef_route"]
	if not await _capture_base(EXPECTED_CAPTURE_IDS[1], expected,
			["reef_route", "return", "production_camera", "day"]):
		return

	if not _focus_target("reef_route"):
		_record_root_failure(EXPECTED_CAPTURE_IDS[2], "missing_target", "reef_route")
		return
	expected = _base_expected("reef_return")
	expected["camera_page"] = 0
	expected["focus"] = "reef_route"
	expected["action_label"] = "FLY"
	expected["onscreen_targets"] = ["reef_route"]
	if not await _capture_base(EXPECTED_CAPTURE_IDS[2], expected,
			["reef_route", "focus", "FLY", "day"]):
		return
	promenade._clear_focus()

	for animal_id: String in ["otter", "frog"]:
		await _move_to_mural_x(610.0)
		if not promenade._bind_animal_id(animal_id):
			_record_root_failure(EXPECTED_CAPTURE_IDS[current_expected_index],
				"animal_bind", animal_id)
			return
		expected = _base_expected("reef_return")
		expected["camera_page"] = 0
		_expect_animal(expected, animal_id, "idle", 0, "day")
		if not await _capture_base(EXPECTED_CAPTURE_IDS[current_expected_index], expected,
				["animal", animal_id, "idle", "day"]):
			return

	for animal_id: String in ["hare", "squirrel"]:
		await _move_to_mural_x(2300.0)
		if not promenade._bind_animal_id(animal_id):
			_record_root_failure(EXPECTED_CAPTURE_IDS[current_expected_index],
				"animal_bind", animal_id)
			return
		expected = _base_expected("reef_return")
		expected["camera_page"] = 1
		_expect_animal(expected, animal_id, "idle", 0, "day")
		if not await _capture_base(EXPECTED_CAPTURE_IDS[current_expected_index], expected,
				["animal", animal_id, "idle", "day"]):
			return

	await _move_to_mural_x(3072.0)
	_suppress_animal()
	expected = _base_expected("reef_return")
	expected["camera_page"] = 1
	expected["onscreen_targets"] = ["slide", "swing", "seesaw"]
	if not await _capture_base(EXPECTED_CAPTURE_IDS[7], expected,
			["playground", "overview", "day"]):
		return

	for play_id: String in ["slide", "swing", "seesaw"]:
		var x := {"slide": 2655.0, "swing": 3200.0, "seesaw": 3760.0}[play_id] as float
		await _move_to_mural_x(x)
		_suppress_animal()
		if not _focus_target(play_id):
			_record_root_failure(EXPECTED_CAPTURE_IDS[current_expected_index],
				"missing_target", play_id)
			return
		expected = _base_expected("reef_return")
		expected["camera_page"] = 1
		expected["focus"] = play_id
		expected["action_label"] = "PLAY"
		expected["onscreen_targets"] = [play_id]
		if not await _capture_base(EXPECTED_CAPTURE_IDS[current_expected_index], expected,
				["playground", play_id, "focus", "day"]):
			return
		var target := _target_by_id(play_id)
		promenade._activate(target)
		promenade._clear_focus()
		var sample_t := 4.15 if play_id == "slide" else 0.43 if play_id == "swing" else 0.48
		promenade._tick_playground_animation(sample_t)
		expected = _base_expected("reef_return")
		expected["camera_page"] = 1
		expected["play_kind"] = play_id
		expected["play_phase"] = "action"
		expected["play_t"] = sample_t
		expected["play_frame_index"] = 3 if play_id == "slide" else 1 \
			if play_id == "swing" else 2
		expected["play_subject_on_screen"] = true
		expected["onscreen_targets"] = [play_id]
		if not await _capture_base(EXPECTED_CAPTURE_IDS[current_expected_index], expected,
				["playground", play_id, "action", "day"]):
			return
		if not _finish_play_action():
			_fail(EXPECTED_CAPTURE_IDS[current_expected_index - 1],
				"play_cleanup", play_id)
			abort_remaining = true
			return

	await _move_to_mural_x(4905.0, true)
	_suppress_animal()
	promenade._clear_focus()
	expected = _base_expected("reef_return")
	expected["camera_page"] = 2
	expected["onscreen_targets"] = ["castle_gate"]
	if not await _capture_base(EXPECTED_CAPTURE_IDS[14], expected,
			["castle", "overview", "promenade", "day"]):
		return
	if not _focus_target("castle_gate"):
		_record_root_failure(EXPECTED_CAPTURE_IDS[15], "missing_target", "castle_gate")
		return
	expected = _base_expected("reef_return")
	expected["camera_page"] = 2
	expected["focus"] = "castle_gate"
	expected["action_label"] = "ENTER"
	expected["onscreen_targets"] = ["castle_gate"]
	if not await _capture_base(EXPECTED_CAPTURE_IDS[15], expected,
			["castle", "focus", "ENTER", "promenade", "day"]):
		return
	promenade._clear_focus()

	await _move_to_mural_x(4510.0, true)
	if not promenade._bind_animal_id("raccoon"):
		_record_root_failure(EXPECTED_CAPTURE_IDS[16], "animal_bind", "raccoon")
		return
	expected = _base_expected("reef_return")
	expected["camera_page"] = 2
	_expect_animal(expected, "raccoon", "idle", 0, "day")
	if not await _capture_base(EXPECTED_CAPTURE_IDS[16], expected,
			["animal", "raccoon", "idle", "day"]):
		return
	var actor: Dictionary = main.g.get("lagoon_animal_actor", {}) as Dictionary
	promenade._startle_animal(actor)
	promenade._tick_animal_startle(actor, 0.48)
	_expect_animal(expected, "raccoon", "startle", 2, "day")
	if not await _capture_base(EXPECTED_CAPTURE_IDS[17], expected,
			["animal", "raccoon", "startle", "frame_2", "day"]):
		return

	if not await _build_promenade(true, true):
		_record_root_failure(EXPECTED_CAPTURE_IDS[18], "scene_readiness",
			"night promenade not ready")
		return
	await _move_to_mural_x(3072.0)
	_suppress_animal()
	promenade._clear_focus()
	expected = _base_expected("reef_return", true)
	expected["camera_page"] = 1
	expected["onscreen_targets"] = ["slide", "swing", "seesaw"]
	if not await _capture_base(EXPECTED_CAPTURE_IDS[18], expected,
			["playground", "overview", "night", "fireflies"]):
		return
	await _move_to_mural_x(4905.0, true)
	_suppress_animal()
	if not _focus_target("castle_gate"):
		_record_root_failure(EXPECTED_CAPTURE_IDS[19], "missing_target", "castle_gate")
		return
	expected = _base_expected("reef_return", true)
	expected["camera_page"] = 2
	expected["focus"] = "castle_gate"
	expected["action_label"] = "ENTER"
	expected["onscreen_targets"] = ["castle_gate"]
	await _capture_base(EXPECTED_CAPTURE_IDS[19], expected,
		["castle", "focus", "ENTER", "promenade", "night", "fireflies"])


func _restore_runtime_state() -> void:
	if main == null:
		return
	if original_had_plane_departed:
		main.save_data["lagoon_plane_departed"] = original_plane_departed
	else:
		main.save_data.erase("lagoon_plane_departed")
	main.is_night = original_is_night
	main.save_pending = false
	main.save_dirty = false
	restored_in_memory = original_had_plane_departed \
		and main.save_data.get("lagoon_plane_departed") == original_plane_departed \
		or not original_had_plane_departed \
		and not main.save_data.has("lagoon_plane_departed")
	restored_time_of_day = main.is_night == original_is_night


func _summary() -> Dictionary:
	var passed := 0
	var failed := 0
	var skipped := 0
	var written := 0
	for row: Dictionary in captures:
		match String(row.get("status", "")):
			"PASS": passed += 1
			"FAIL": failed += 1
			"SKIPPED": skipped += 1
		var image: Dictionary = row.get("image", {}) as Dictionary
		if String(image.get("sha256", "")) != "":
			written += 1
	return {
		"expected": EXPECTED_CAPTURE_IDS.size(),
		"rows": captures.size(),
		"written": written,
		"passed": passed,
		"failed": failed,
		"skipped": skipped,
	}


func _write_manifest(save_guard: Dictionary, result: String) -> bool:
	var version := Engine.get_version_info()
	var probe_sha256 := FileAccess.get_sha256(PROBE_PATH)
	var manifest := {
		"schema": SCHEMA,
		"probe": PROBE_PATH,
		"probe_sha256": probe_sha256,
		"source_revision": OS.get_environment("GITHUB_SHA") \
			if OS.get_environment("GITHUB_SHA") != "" else "unknown",
		"godot_version": String(version.get("string", "")),
		"rendering_method": String(RenderingServer.get_current_rendering_method()),
		"quality": "speedy",
		"viewport": {"width": VIEWPORT_SIZE.x, "height": VIEWPORT_SIZE.y},
		"expected_capture_ids": EXPECTED_CAPTURE_IDS,
		"save_guard": save_guard,
		"captures": captures,
		"global_failures": global_failures,
		"summary": _summary(),
		"result": result,
	}
	var path := out_dir.path_join("sky_lagoon_review_manifest.json")
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		_fail("MANIFEST", "manifest_open", "error=%d" % FileAccess.get_open_error())
		return false
	file.store_string(JSON.stringify(manifest, "\t") + "\n")
	file.close()
	return true


func _remove_probe_save_artifacts() -> bool:
	if probe_save_path == "":
		return true
	var removed_all := true
	for suffix: String in SAVE_SUFFIXES:
		var path := probe_save_path + suffix
		if FileAccess.file_exists(path):
			removed_all = DirAccess.remove_absolute(path) == OK and removed_all
	return removed_all


func _begin_save_isolation() -> bool:
	normal_save_path = ProjectSettings.globalize_path("user://reef_save.json")
	probe_save_path = out_dir.path_join(".sky_lagoon_probe_save.json")
	save_was_remapped = probe_save_path != normal_save_path
	if not save_was_remapped:
		return false
	return _remove_probe_save_artifacts()


func _end_save_isolation() -> void:
	isolated_cleanup_ok = _remove_probe_save_artifacts()


func _run() -> void:
	get_root().mode = Window.MODE_WINDOWED
	get_root().size = VIEWPORT_SIZE
	var requested := OS.get_environment("SKY_LAGOON_SHOT_OUT")
	out_dir = requested if requested != "" else ProjectSettings.globalize_path(
		"res://tmp/sky_lagoon_shots")
	var directory_error := DirAccess.make_dir_recursive_absolute(out_dir)
	if directory_error != OK:
		_fail("GLOBAL", "output_directory", str(directory_error))
		abort_remaining = true
	else:
		_clear_prior_outputs()
	if not _begin_save_isolation():
		_fail("GLOBAL", "save_isolation", "user directory could not be redirected")
		abort_remaining = true
	save_before = {
		"path": normal_save_path,
		"artifacts": _artifact_fingerprints(normal_save_path),
	}
	probe_save_before = _artifact_fingerprints(probe_save_path)

	var packed := load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	# Main reuses a preinstalled SaveState. The explicit path override isolates
	# both load recovery and any unexpected writes without remapping user://,
	# whose shader-cache root is initialized before this script starts.
	main._save_state = SaveState.new(main, probe_save_path)
	get_root().add_child(main)
	# Editor-capable builds install a developer look lab whose deferred startup
	# reads normal user://look_config.json and can override the production lens,
	# lighting, grade and render scale. It has no authority over review evidence.
	if main.dev_mode != null and is_instance_valid(main.dev_mode):
		var look_lab: Node = main.dev_mode
		main.dev_mode = null
		look_lab.process_mode = Node.PROCESS_MODE_DISABLED
		look_lab.get_parent().remove_child(look_lab)
		look_lab.free()
	dev_mode_neutralized = main.dev_mode == null
	await _frames(2)
	# Newer builds open on the production launch menu. Enter through that menu's
	# real continuation seam before selecting the Lagoon; otherwise a full-screen
	# menu can satisfy generic nonblank-image checks while hiding the whole stage.
	if _object_has_property(main, &"start_menu_active") \
			and bool(main.get("start_menu_active")):
		var start_menu: Variant = main.call("_start_menu_ref")
		if start_menu is Object and (start_menu as Object).has_method("_enter_game"):
			(start_menu as Object).call("_enter_game")
			await _frames(2)
	if main.intro_active:
		main._skip_intro()
	await _frames(2)
	main._apply_quality("speedy")
	original_is_night = main.is_night
	original_had_plane_departed = main.save_data.has("lagoon_plane_departed")
	original_plane_departed = main.save_data.get("lagoon_plane_departed")
	previous_process_mode = main.process_mode
	if not abort_remaining:
		await _run_capture_sequence()
	if abort_remaining:
		_skip_remaining("capture sequence aborted")
	_restore_runtime_state()
	main.process_mode = previous_process_mode
	await _frames(2)
	save_after = {
		"path": normal_save_path,
		"artifacts": _artifact_fingerprints(normal_save_path),
	}
	main.process_mode = Node.PROCESS_MODE_DISABLED
	probe_save_after = _artifact_fingerprints(probe_save_path)
	probe_write_calls = 0
	for artifact: Dictionary in probe_save_after:
		if bool(artifact.get("exists", false)):
			probe_write_calls += 1
	_end_save_isolation()
	var disk_unchanged := _same_fingerprints(
		save_before["artifacts"] as Array, save_after["artifacts"] as Array)
	var primary_before: Dictionary = (save_before["artifacts"] as Array)[0] as Dictionary
	var primary_after: Dictionary = (save_after["artifacts"] as Array)[0] as Dictionary
	var save_guard := {
		"path": normal_save_path,
		"probe_path": probe_save_path,
		"remapped": save_was_remapped,
		"existed_before": primary_before["exists"],
		"sha256_before": primary_before["sha256"],
		"modified_time_before": primary_before["modified_time"],
		"existed_after": primary_after["exists"],
		"sha256_after": primary_after["sha256"],
		"modified_time_after": primary_after["modified_time"],
		"artifacts_before": save_before["artifacts"],
		"artifacts_after": save_after["artifacts"],
		"isolated_artifacts_before": probe_save_before,
		"isolated_artifacts_after": probe_save_after,
		"disk_unchanged": disk_unchanged,
		"had_plane_departed_key": original_had_plane_departed,
		"original_plane_departed": original_plane_departed,
		"restored_in_memory": restored_in_memory,
		"restored_time_of_day": restored_time_of_day,
		"probe_write_calls": probe_write_calls,
		"isolated_cleanup_ok": isolated_cleanup_ok,
	}
	if not disk_unchanged:
		_fail("SAVE", "disk_mutation", "normal save artifacts changed")
	if not restored_in_memory:
		_fail("SAVE", "memory_restore", "lagoon_plane_departed was not restored")
	if not restored_time_of_day:
		_fail("SAVE", "time_restore", "is_night was not restored")
	if probe_write_calls != 0:
		_fail("SAVE", "isolated_write", "%d isolated save artifacts created" % probe_write_calls)
	if not isolated_cleanup_ok:
		_fail("SAVE", "isolated_cleanup", "isolated save artifacts could not be removed")
	var summary := _summary()
	var output_pngs := _output_png_names()
	var output_set_exact := output_pngs == _expected_png_names()
	if not output_set_exact:
		_fail("OUTPUT", "png_set", "expected=%s actual=%s" % [
			str(_expected_png_names()), str(output_pngs)])
	var version := Engine.get_version_info()
	var exact_engine := int(version.get("major", 0)) == 4 \
		and int(version.get("minor", 0)) == 7 and int(version.get("patch", 0)) == 1 \
		and String(version.get("status", "")) == "stable" \
		and String(version.get("build", "")) == "official"
	var mobile_renderer := String(RenderingServer.get_current_rendering_method()) == "mobile"
	if not exact_engine:
		_fail("GLOBAL", "engine_version", String(version.get("string", "")))
	if not mobile_renderer:
		_fail("GLOBAL", "rendering_method",
			String(RenderingServer.get_current_rendering_method()))
	var complete := captures.size() == EXPECTED_CAPTURE_IDS.size() \
		and int(summary["rows"]) == 20 and int(summary["written"]) == 20 \
		and int(summary["passed"]) == 20 and int(summary["failed"]) == 0 \
		and int(summary["skipped"]) == 0 and global_failures.is_empty() \
		and disk_unchanged and restored_in_memory and restored_time_of_day \
		and probe_write_calls == 0 and isolated_cleanup_ok and dev_mode_neutralized \
		and exact_engine and mobile_renderer and output_set_exact
	manifest_written = _write_manifest(save_guard, "PASS" if complete else "FAIL")
	complete = complete and manifest_written
	print("LAGOONSHOT|PROBE_SHA256|%s" % FileAccess.get_sha256(PROBE_PATH))
	print("LAGOONSHOT|SUMMARY|expected=%d|rows=%d|written=%d|passed=%d|failed=%d|skipped=%d" % [
		20, summary["rows"], summary["written"], summary["passed"],
		summary["failed"], summary["skipped"],
	])
	print("LAGOONSHOT|RESULT|%s|%s" % [
		"PASS" if complete else "FAIL",
		out_dir.path_join("sky_lagoon_review_manifest.json"),
	])
	main.set_process(false)
	main.queue_free()
	await _frames(3)
	main = null
	quit(0 if complete else 1)
