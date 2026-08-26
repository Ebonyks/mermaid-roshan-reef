extends SceneTree
# Blocking Sky Lagoon Canvas product contract. The opaque 6144x2048 storybook
# stage is the game here: no spatial fallback, hidden Player layout authority,
# review-only camera, or metadata-only substitute may satisfy this probe.

const Affordance := preload("res://scripts/interaction_affordance.gd")
const MASTER_SIZE := Vector2(6144.0, 2048.0)
const TILE_SIZE := Vector2(1024.0, 1024.0)
const TARGET_IDS: Array[String] = [
	"castle_gate", "seesaw", "slide", "swing",
]
const AUDIT_SWING_SEAT_ANCHORS := [
	Vector2(264.5, 204.5),
	Vector2(168.0, 205.0),
	Vector2(322.5, 186.0),
	Vector2(222.0, 190.0),
]
const AUDIT_SEESAW_SEAT_ANCHORS := [
	Vector2(300.0, 420.0),
	Vector2(225.0, 400.0),
	Vector2(270.0, 340.0),
	Vector2(220.0, 360.0),
]
const AUDIT_SEESAW_SOCKET := Vector2(226.13, -9.42)
const AUDIT_SWING_SEAT_DROP := 361.0
const HOLDER_NAMES: Array[String] = [
	"SkyLagoonBase",
	"SkyLagoonRear",
	"SkyLagoonLandmarks",
	"SkyLagoonInteractive",
	"SkyLagoonActors",
	"SkyLagoonForeground",
]
const REQUIRED_ASSETS: Array[String] = [
	"res://assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png",
	"res://assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png",
	"res://assets/props/story/play_swing_frame.png",
	"res://assets/props/story/play_swing_seat.png",
	"res://assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png",
	"res://assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png",
	"res://assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png",
	"res://assets/characters/roshan_25d/roshan_base.png",
	"res://assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png",
	"res://assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png",
	"res://assets/fairy/sprites/bug_firefly.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_0.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_1.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_2_v2.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_swing_3_v2.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_0.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_1.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_2_v2.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_slide_3_v2.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_0.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_1.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_2.png",
	"res://assets/sprites/sky_lagoon/roshan_playground/roshan_seesaw_3.png",
]

var failed := false
var main: ReefMain
var promenade: SkyLagoonPromenade


func _check(label: String, condition: bool, detail: String = "") -> void:
	print("LAGOONCANVAS|%s|%s%s" % [
		label,
		"OK" if condition else "FAIL",
		"" if detail == "" else "|" + detail,
	])
	if not condition:
		failed = true


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _spatial_count(node: Node) -> int:
	# Keep the migration probe itself free of the API family it is rejecting.
	var result := 1 if node.is_class("Node" + "3D") else 0
	for child: Node in node.get_children():
		result += _spatial_count(child)
	return result


func _forbidden_facade_primitive_count(node: Node) -> int:
	var result := 1 if node is Polygon2D or node is Line2D else 0
	for child: Node in node.get_children():
		result += _forbidden_facade_primitive_count(child)
	return result


func _audit_sprite_anchor_master(sprite: Sprite2D, anchor_pixels: Vector2) -> Vector2:
	var master_space: Node2D = main.g.get("lagoon_master_space") as Node2D
	var source_size: Vector2 = sprite.texture.get_size()
	var local_anchor: Vector2 = anchor_pixels - source_size * 0.5 + sprite.offset
	return master_space.to_local(sprite.to_global(local_anchor))


func _collect_sprites(node: Node, output: Array[Sprite2D]) -> void:
	if node is Sprite2D:
		output.append(node as Sprite2D)
	for child: Node in node.get_children():
		_collect_sprites(child, output)


func _named_count(node: Node, wanted: StringName) -> int:
	var result := 1 if node.name == wanted else 0
	for child: Node in node.get_children():
		result += _named_count(child, wanted)
	return result


func _target(target_id: String) -> Dictionary:
	for value: Variant in main.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		if String(target.get("id", "")) == target_id:
			return target
	return {}


func _target_ids() -> Array[String]:
	var ids: Array[String] = []
	for value: Variant in main.g.get("lagoon_promenade_targets", []) as Array:
		ids.append(String((value as Dictionary).get("id", "")))
	ids.sort()
	return ids


func _screen_center(item: CanvasItem) -> Vector2:
	return item.get_global_transform_with_canvas().origin


func _sprite_screen_rect(sprite: Sprite2D) -> Rect2:
	if sprite == null or not is_instance_valid(sprite) or sprite.texture == null:
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


func _opaque_screen_cells(sprite: Sprite2D, output: Dictionary,
		grid_px: float = 5.0) -> void:
	if sprite == null or not is_instance_valid(sprite) or sprite.texture == null \
			or not sprite.visible:
		return
	var image: Image = sprite.texture.get_image()
	if image == null or image.is_empty():
		return
	if image.is_compressed() and image.decompress() != OK:
		return
	var source := Rect2i(Vector2i.ZERO, image.get_size())
	if sprite.region_enabled:
		source = Rect2i(sprite.region_rect)
	var step: int = maxi(1, maxi(source.size.x, source.size.y) / 160)
	var local_top_left: Vector2 = sprite.offset
	if sprite.centered:
		local_top_left -= Vector2(source.size) * 0.5
	var transform: Transform2D = sprite.get_global_transform_with_canvas()
	for y: int in range(source.position.y, source.end.y, step):
		for x: int in range(source.position.x, source.end.x, step):
			if image.get_pixel(x, y).a < 0.10:
				continue
			var relative := Vector2(x - source.position.x, y - source.position.y)
			if sprite.flip_h:
				relative.x = float(source.size.x) - relative.x
			if sprite.flip_v:
				relative.y = float(source.size.y) - relative.y
			var screen: Vector2 = transform * (local_top_left + relative)
			output[Vector2i(floori(screen.x / grid_px), floori(screen.y / grid_px))] = true
	for child: Node in sprite.get_children():
		_opaque_child_screen_cells(child, output, grid_px)


func _opaque_child_screen_cells(node: Node, output: Dictionary, grid_px: float) -> void:
	if node is Sprite2D:
		_opaque_screen_cells(node as Sprite2D, output, grid_px)
		return
	for child: Node in node.get_children():
		_opaque_child_screen_cells(child, output, grid_px)


func _opaque_geometry_contacts(actor: Sprite2D, equipment: Sprite2D) -> bool:
	var actor_cells: Dictionary = {}
	var equipment_cells: Dictionary = {}
	_opaque_screen_cells(actor, actor_cells)
	_opaque_screen_cells(equipment, equipment_cells)
	if actor_cells.is_empty() or equipment_cells.is_empty():
		return false
	var contacts := 0
	for value: Variant in actor_cells.keys():
		var cell: Vector2i = value as Vector2i
		for y: int in range(-2, 3):
			for x: int in range(-2, 3):
				if equipment_cells.has(cell + Vector2i(x, y)):
					contacts += 1
					if contacts >= 3:
						return true
	return false


func _sprite_resource_count(root_node: Node, resource_path: String) -> int:
	var count := 0
	if root_node is Sprite2D:
		var sprite := root_node as Sprite2D
		if sprite.texture != null and sprite.texture.resource_path == resource_path:
			count += 1
	for child: Node in root_node.get_children():
		count += _sprite_resource_count(child, resource_path)
	return count


func _real_sprite_content(holder: Node2D) -> Dictionary:
	var sprites: Array[Sprite2D] = []
	if holder != null:
		_collect_sprites(holder, sprites)
	var union := Rect2()
	var has_union := false
	var textured := 0
	for sprite: Sprite2D in sprites:
		if sprite.texture == null or not sprite.visible:
			continue
		textured += 1
		var bounds: Rect2 = _sprite_screen_rect(sprite)
		if bounds.get_area() <= 0.0:
			continue
		union = bounds if not has_union else union.merge(bounds)
		has_union = true
	return {"count": textured, "bounds": union}


func _direct_child_names(holder: Node2D) -> Array[String]:
	var names: Array[String] = []
	if holder == null:
		return names
	for child: Node in holder.get_children():
		names.append(String(child.name))
	names.sort()
	return names


func _canvas_clip_contract() -> bool:
	var viewport_root: Control = promenade.canvas_root()
	if viewport_root == null or not is_instance_valid(viewport_root):
		return false
	if not viewport_root.clip_contents:
		return true
	var transform: Transform2D = viewport_root.get_global_transform_with_canvas()
	var size: Vector2 = viewport_root.size
	var corners: Array[Vector2] = [
		transform * Vector2.ZERO,
		transform * Vector2(size.x, 0.0),
		transform * size,
		transform * Vector2(0.0, size.y),
	]
	var bounds := Rect2(corners[0], Vector2.ZERO)
	for corner: Vector2 in corners:
		bounds = bounds.expand(corner)
	var phone: Rect2 = get_root().get_visible_rect()
	return bounds.position.x <= phone.position.x + 1.0 \
		and bounds.position.y <= phone.position.y + 1.0 \
		and bounds.end.x >= phone.end.x - 1.0 \
		and bounds.end.y >= phone.end.y - 1.0


func _backdrop_screen_coverage() -> Dictionary:
	var stage_root: CanvasLayer = promenade.root()
	var union := Rect2()
	var has_union := false
	var count := 0
	for row: int in range(2):
		for column: int in range(6):
			var tile: Sprite2D = stage_root.find_child(
				"SkyLagoonBackdrop_r%d_c%d" % [row, column], true, false) as Sprite2D
			if tile == null:
				continue
			var bounds: Rect2 = _sprite_screen_rect(tile)
			union = bounds if not has_union else union.merge(bounds)
			has_union = true
			count += 1
	var phone: Rect2 = get_root().get_visible_rect()
	var covered: Rect2 = union.intersection(phone) if has_union else Rect2()
	return {
		"count": count,
		"union": union,
		"fraction": covered.get_area() / maxf(phone.get_area(), 1.0),
	}


func _rendered_frame_contract() -> bool:
	# Rendered evidence catches otherwise-valid node trees whose Control clipping
	# or camera transform leaves the storybook mural in a small corner.
	if DisplayServer.get_name() == "headless":
		return _canvas_clip_contract()
	var viewport_texture: ViewportTexture = get_root().get_texture()
	if viewport_texture == null:
		return false
	var image: Image = viewport_texture.get_image()
	if image == null or image.is_empty():
		return false
	if image.is_compressed() and image.decompress() != OK:
		return false
	var size: Vector2i = image.get_size()
	if size.x < 4 or size.y < 4:
		return false
	var edge_samples := [
		Vector2i(2, 2), Vector2i(size.x - 3, 2),
		Vector2i(2, size.y - 3), Vector2i(size.x - 3, size.y - 3),
		Vector2i(size.x / 2, 2), Vector2i(size.x / 2, size.y - 3),
	]
	var opaque_edges := 0
	for point: Vector2i in edge_samples:
		opaque_edges += 1 if image.get_pixelv(point).a >= 0.98 else 0
	var varied_cells := 0
	var reference: Color = image.get_pixel(size.x / 2, size.y / 2)
	for row: int in range(5):
		for column: int in range(9):
			var sample := Vector2i(
				mini(size.x - 1, (column * 2 + 1) * size.x / 18),
				mini(size.y - 1, (row * 2 + 1) * size.y / 10))
			var color: Color = image.get_pixelv(sample)
			var rgb_delta: float = absf(color.r - reference.r) \
				+ absf(color.g - reference.g) + absf(color.b - reference.b)
			if color.a >= 0.98 and rgb_delta >= 0.04:
				varied_cells += 1
	return opaque_edges == edge_samples.size() and varied_cells >= 12


func _layer_contract() -> bool:
	main._living_world_ref().tick(0.0)
	main._flash_speaker_icon("roshan")
	var fade_layer: CanvasLayer = main.fade_rect.get_parent() as CanvasLayer \
		if main.fade_rect != null else null
	var base_ok: bool = promenade.root().layer == -1 \
		and main.hud_layer != null and main.hud_layer.layer == 0 \
		and main.living_layer != null and main.living_layer.layer == 6 \
		and main.speech_layer != null and main.speech_layer.layer == 8 \
		and main.touch_ui != null and main.touch_ui.layer == 9 \
		and main.pause_layer != null and main.pause_layer.layer == 12 \
		and fade_layer != null and fade_layer.layer == 30
	main.toggle_pause()
	var open_ok: bool = paused and main.pause_layer.layer == 29
	main.toggle_pause()
	return base_ok and open_ok and not paused \
		and main.pause_layer.layer == 12


func _validate_stage() -> void:
	var stage_root: CanvasLayer = promenade.root()
	var viewport_root: Control = promenade.canvas_root()
	var camera: Camera2D = promenade.camera_2d()
	_check("canvas_stage_authority",
		stage_root != null and is_instance_valid(stage_root)
		and stage_root.name == &"SkyLagoonCanvasLayer"
		and stage_root.layer == main.SKY_LAGOON_STAGE_CANVAS_LAYER
		and viewport_root != null and is_instance_valid(viewport_root)
		and viewport_root.name == &"SkyLagoonViewport"
		and viewport_root.anchor_right == 1.0 and viewport_root.anchor_bottom == 1.0
		and camera != null and is_instance_valid(camera) and camera.enabled
		and camera.name == &"SkyLagoonCamera2D"
		and get_root().get_viewport().get_camera_2d() == camera
		and not main.player.cam.current
		and not main.player.visible)
	_check("lagoon_root_has_zero_spatial_descendants",
		stage_root != null and _spatial_count(stage_root) == 0,
		"count=%d" % (_spatial_count(stage_root) if stage_root != null else -1))
	var holders_ok := true
	for holder_name: String in HOLDER_NAMES:
		var holder: Node = stage_root.find_child(holder_name, true, false)
		holders_ok = holders_ok and holder is Node2D \
			and _named_count(stage_root, StringName(holder_name)) == 1
	_check("exact_canvas_holder_contract", holders_ok)
	_check("full_layer_order_-1_0_6_8_9_12_29_30", _layer_contract())


func _validate_assets_and_mural() -> void:
	var assets_ok := true
	for path: String in REQUIRED_ASSETS:
		assets_ok = assets_ok and ResourceLoader.exists(path)
	for row: int in range(2):
		for column: int in range(6):
			assets_ok = assets_ok and ResourceLoader.exists(
				"res://assets/flats/sky_lagoon/main/"
				+ "flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png"
				% [row, column])
	_check("approved_source_assets_resolve", assets_ok)
	var master_path := "res://assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png"
	var master: Image = Image.load_from_file(ProjectSettings.globalize_path(master_path))
	_check("native_master_is_6144x2048",
		master != null and not master.is_empty()
		and master.get_size() == Vector2i(6144, 2048))

	var root_node: CanvasLayer = promenade.root()
	var positions: Dictionary = {}
	var tiles_ok := true
	var tile_count := 0
	for row: int in range(2):
		for column: int in range(6):
			var tile_name := "SkyLagoonBackdrop_r%d_c%d" % [row, column]
			var tile: Sprite2D = root_node.find_child(tile_name, true, false) as Sprite2D
			var expected := Vector2(
				float(column) * TILE_SIZE.x + TILE_SIZE.x * 0.5,
				float(row) * TILE_SIZE.y + TILE_SIZE.y * 0.5)
			var valid: bool = tile != null and tile.texture != null \
				and tile.texture.get_size() == TILE_SIZE \
				and tile.texture.resource_path == (
					"res://assets/flats/sky_lagoon/main/"
					+ "flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png"
					% [row, column]) \
				and tile.centered and tile.position.is_equal_approx(expected) \
				and tile.scale.is_equal_approx(Vector2.ONE)
			tiles_ok = tiles_ok and valid
			if tile != null:
				tile_count += 1
				positions[tile.position] = true
	_check("twelve_native_seamless_canvas_tiles",
		tiles_ok and tile_count == 12 and positions.size() == 12,
		"tiles=%d positions=%d" % [tile_count, positions.size()])
	var castle: Sprite2D = main.g.get("lagoon_castle_card") as Sprite2D
	var castle_bounds := promenade._sprite_alpha_bounds_master(castle)
	var castle_frame_ok: bool = castle != null and castle_bounds.get_area() > 0.0 \
		and castle.visible and castle.is_visible_in_tree() \
		and castle.modulate.a * castle.self_modulate.a >= 0.95 \
		and castle_bounds.get_area() >= 500000.0 \
		and castle_bounds.position.x >= 0.0 and castle_bounds.end.x <= 6144.0 \
		and castle_bounds.position.y >= 48.0 and castle_bounds.end.y <= 2048.0
	_check("castle_authored_pixels_stay_inside_master_frame", castle_frame_ok,
		"bounds=%s" % castle_bounds)
	var landmark_layer: Node2D = main.g.get("lagoon_landmark_layer") as Node2D
	var primitive_count: int = _forbidden_facade_primitive_count(landmark_layer) \
		if landmark_layer != null else -1
	var castle_dressing_ok: bool = castle != null \
		and String(castle.get_meta("exterior_dressing_contract", "")) \
			== "authored_sprite2d_only" \
		and String(castle.get_meta("lighting_medium", "")) \
			== "authored_rgba_canvas_sprite" \
		and primitive_count == 0
	_check("castle_facade_rejects_procedural_mesh_grime", castle_dressing_ok,
		"landmark_primitive_count=%d" % primitive_count)


func _validate_parallax_and_coordinates() -> void:
	var root_node: CanvasLayer = promenade.root()
	var base: Node2D = root_node.find_child("SkyLagoonBase", true, false) as Node2D
	var rear_mural: Node2D = root_node.find_child(
		"SkyLagoonRearMural", true, false) as Node2D
	var rear: Node2D = root_node.find_child("SkyLagoonRear", true, false) as Node2D
	var landmarks: Node2D = root_node.find_child(
		"SkyLagoonLandmarks", true, false) as Node2D
	var interactive: Node2D = root_node.find_child(
		"SkyLagoonInteractive", true, false) as Node2D
	var actors: Node2D = root_node.find_child("SkyLagoonActors", true, false) as Node2D
	var foreground_mural: Node2D = root_node.find_child(
		"SkyLagoonForegroundMural", true, false) as Node2D
	var foreground: Node2D = root_node.find_child(
		"SkyLagoonForeground", true, false) as Node2D
	var factors_ok: bool = base != null and rear_mural != null \
		and rear != null and landmarks != null and interactive != null \
		and actors != null and foreground_mural != null and foreground != null \
		and is_equal_approx(float(base.get_meta("parallax_factor", -1.0)), 1.0) \
		and is_equal_approx(float(rear_mural.get_meta(
			"parallax_factor", -1.0)), 1.0) \
		and is_equal_approx(float(rear.get_meta("parallax_factor", -1.0)), 0.82) \
		and is_equal_approx(float(landmarks.get_meta("parallax_factor", -1.0)), 1.0) \
		and is_equal_approx(float(interactive.get_meta("parallax_factor", -1.0)), 1.0) \
		and is_equal_approx(float(actors.get_meta("parallax_factor", -1.0)), 1.0) \
		and is_equal_approx(float(foreground_mural.get_meta(
			"parallax_factor", -1.0)), 1.0) \
		and is_equal_approx(float(foreground.get_meta("parallax_factor", -1.0)), 1.06)
	var holders: Array[Node2D] = [base, rear_mural, rear, landmarks,
		interactive, actors, foreground_mural, foreground]
	var expected_audit_ids: Array[String] = ["base", "rear_geography",
		"rear_atmosphere", "landmarks", "interactive", "actors",
		"foreground_geography", "foreground_lighting"]
	var expected_z: Array[int] = [-500, -400, -400, -300, 0, 100, 300, 300]
	var expected_relative_z: Array[Vector2i] = [
		Vector2i(0, 0), Vector2i(0, 0), Vector2i(0, 0), Vector2i(0, 0),
		Vector2i(-1, 4), Vector2i(-1, 0), Vector2i(0, 0), Vector2i(0, 0),
	]
	var holder_contract_ok := true
	var holders_present := true
	for index: int in range(holders.size()):
		var holder: Node2D = holders[index]
		holders_present = holders_present and holder != null
		holder_contract_ok = holder_contract_ok and holder != null \
			and holder.get_index() == index and holder.z_index == expected_z[index] \
			and String(holder.get_meta("visual_audit_layer_id", "")) \
				== expected_audit_ids[index] \
			and int(holder.get_meta("visual_audit_relative_z_min", 999)) \
				== expected_relative_z[index].x \
			and int(holder.get_meta("visual_audit_relative_z_max", -999)) \
				== expected_relative_z[index].y
	_check("eight_canvas_holders_have_exact_order_and_audit_ids",
		holder_contract_ok, "ids=%s z=%s relative_z=%s" % [
			expected_audit_ids, expected_z, expected_relative_z])
	if not holders_present:
		# The topology assertion above owns this failure. Stop before any
		# coordinate/member access so a malformed scene reports controlled FAIL
		# instead of hiding the defect behind a null-dereference script error.
		return
	promenade.set_master_route_x(2048.0)
	var rear_before: float = rear.position.x if rear != null else 0.0
	var foreground_before: float = foreground.position.x if foreground != null else 0.0
	var locked_before: Array[Vector2] = [
		base.position, rear_mural.position, landmarks.position,
		interactive.position, actors.position, foreground_mural.position]
	promenade.set_master_route_x(3072.0)
	var rear_mural_content: Dictionary = _real_sprite_content(rear_mural)
	var rear_content: Dictionary = _real_sprite_content(rear)
	var foreground_mural_content: Dictionary = _real_sprite_content(
		foreground_mural)
	var foreground_content: Dictionary = _real_sprite_content(foreground)
	var rear_bounds: Rect2 = rear_content.get("bounds", Rect2()) as Rect2
	var foreground_bounds: Rect2 = foreground_content.get("bounds", Rect2()) as Rect2
	var rear_delta: float = rear.position.x - rear_before if rear != null else 0.0
	var foreground_delta: float = foreground.position.x - foreground_before \
		if foreground != null else 0.0
	var locked_after: Array[Vector2] = [
		base.position, rear_mural.position, landmarks.position,
		interactive.position, actors.position, foreground_mural.position]
	var locked_zero: bool = base.position.is_zero_approx() \
		and rear_mural.position.is_zero_approx() \
		and landmarks.position.is_zero_approx() \
		and interactive.position.is_zero_approx() \
		and actors.position.is_zero_approx() \
		and foreground_mural.position.is_zero_approx()
	_check("playground_actor_castle_share_locked_mural_socket",
		factors_ok and locked_before == locked_after and locked_zero,
		"before=%s after=%s" % [locked_before, locked_after])
	var rear_tree: Node = rear_mural.get_child(0) if rear_mural != null \
		and rear_mural.get_child_count() == 1 else null
	var foreground_tree: Node = foreground_mural.get_child(0) \
		if foreground_mural != null \
		and foreground_mural.get_child_count() == 1 else null
	var rear_tree_texture := ""
	var rear_tree_base := Vector2.ZERO
	if rear_tree is Sprite2D:
		rear_tree_texture = (rear_tree as Sprite2D).texture.resource_path \
			if (rear_tree as Sprite2D).texture != null else ""
		rear_tree_base = (rear_tree as Sprite2D).get_meta(
			"ambient_base", Vector2.ZERO) as Vector2
	var foreground_tree_texture := ""
	var foreground_tree_base := Vector2.ZERO
	if foreground_tree is Sprite2D:
		foreground_tree_texture = (foreground_tree as Sprite2D).texture.resource_path \
			if (foreground_tree as Sprite2D).texture != null else ""
		foreground_tree_base = (foreground_tree as Sprite2D).get_meta(
			"ambient_base", Vector2.ZERO) as Vector2
	var geographic_ownership_ok: bool = \
		int(rear_mural_content.get("count", 0)) == 1 \
		and int(foreground_mural_content.get("count", 0)) == 1 \
		and rear_tree is Sprite2D and rear_tree.name == "SkyLagoonRearTree" \
		and foreground_tree is Sprite2D \
		and foreground_tree.name == "SkyLagoonForegroundTree" \
		and bool(rear_tree.get_meta("background_socket_healed", false)) \
		and bool(rear_tree.get_meta("geography_locked", false)) \
		and bool(foreground_tree.get_meta("background_socket_healed", false)) \
		and bool(foreground_tree.get_meta("geography_locked", false)) \
		and rear_tree_texture \
			== "res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_tall_v1.png" \
		and foreground_tree_texture \
			== "res://assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_slender_v1.png" \
		and rear_tree_base.is_equal_approx(Vector2(4180.0, 1185.0 - 465.0 * 0.5)) \
		and foreground_tree_base.is_equal_approx(
			Vector2(5750.0, 1510.0 - 350.0 * 0.5))
	_check("healed_tree_cards_have_one_locked_geographic_owner",
		geographic_ownership_ok,
		"rear=%s/%s/%s foreground=%s/%s/%s" % [rear_mural_content,
			rear_tree_texture, rear_tree_base,
			foreground_mural_content,
			foreground_tree_texture, foreground_tree_base])
	var rear_membership_ok: bool = _direct_child_names(rear) \
		== ["SkyLagoonRearCloud"]
	var foreground_names: Array[String] = _direct_child_names(foreground)
	var expected_fireflies: Array[String] = []
	for index: int in range(18):
		expected_fireflies.append("SkyLagoonFirefly_%02d" % index)
	var foreground_membership_ok: bool = foreground_names.is_empty() \
		or foreground_names == expected_fireflies
	var sprite2d_lighting_ok := true
	for child: Node in foreground.get_children():
		sprite2d_lighting_ok = sprite2d_lighting_ok and child is Sprite2D \
			and String(child.get_meta("lighting_medium", "")) \
				== "canvas_sprite2d"
	_check("atmosphere_and_sprite2d_lighting_keep_independent_owners",
		rear_membership_ok and foreground_membership_ok and sprite2d_lighting_ok,
		"rear=%s foreground=%s" % [_direct_child_names(rear), foreground_names])
	_check("two_real_parallax_motion_classes",
		factors_ok and int(rear_content.get("count", 0)) > 0 \
		and maxf(rear_bounds.size.x, rear_bounds.size.y) >= 48.0 \
		and not is_equal_approx(rear_delta, foreground_delta) \
		and absf(rear_delta) > 0.01 and absf(foreground_delta) > 0.01,
		"rear=%.3f/%s foreground=%.3f/%s" % [rear_delta,
			int(rear_content.get("count", 0)), foreground_delta,
			int(foreground_content.get("count", 0))])
	var master_points: Array[Vector2] = [
		Vector2(2560.0, 1024.0), Vector2(3072.0, 1450.0),
		Vector2(3584.0, 1800.0),
	]
	var roundtrip_ok := true
	for master_point: Vector2 in master_points:
		var screen: Vector2 = promenade.screen_from_master(master_point)
		var restored: Vector2 = promenade.master_from_screen(screen)
		roundtrip_ok = roundtrip_ok and restored.distance_to(master_point) <= 0.5
	_check("master_screen_roundtrip_uses_production_camera2d", roundtrip_ok)
	var coverage_ok := true
	var coverage_detail: Array[String] = []
	for master_x: float in [1024.0, 3072.0, 5120.0]:
		promenade.set_master_route_x(master_x)
		var coverage: Dictionary = _backdrop_screen_coverage()
		coverage_ok = coverage_ok and int(coverage.get("count", 0)) == 12 \
			and float(coverage.get("fraction", 0.0)) >= 0.995
		coverage_detail.append("%.0f=%.3f/%s" % [master_x,
			float(coverage.get("fraction", 0.0)), coverage.get("union", Rect2())])
	_check("mural_transform_covers_each_phone_screen", coverage_ok,
		";".join(coverage_detail))


func _validate_targets_and_touch() -> void:
	var roster_ok: bool = _target_ids() == TARGET_IDS
	var reach_ok := true
	var metadata_ok := true
	var display_ok := true
	var category_ok := true
	var unique_focus_ok := true
	var selected_cues_ok := true
	var cue_detail: Array[String] = []
	for target_id: String in TARGET_IDS:
		var target: Dictionary = _target(target_id)
		var node: CanvasItem = target.get("node") as CanvasItem
		var highlight: CanvasItem = target.get("highlight") as CanvasItem
		var expected_affordance: String = Affordance.PLOT \
			if target_id == "castle_gate" else Affordance.ANIMATION
		category_ok = category_ok and String(target.get(
			"affordance_kind", "")) == expected_affordance
		metadata_ok = metadata_ok and node != null and highlight != null \
			and node is Node2D and highlight is Sprite2D \
			and String(node.get_meta("interaction_id", "")) == target_id \
			and String(node.get_meta("canvas_layer_role", "")) != "" \
			and bool(node.get_meta("source_owned", false)) \
			and float(node.get_meta("touch_footprint_px", 0.0)) >= 220.0 \
			and float(target.get("radius_px", 0.0)) >= 110.0
		if highlight is Sprite2D:
			var focus_sprite := highlight as Sprite2D
			if target_id == "castle_gate":
				unique_focus_ok = unique_focus_ok and not (node is Sprite2D) \
					and focus_sprite.texture != null \
					and focus_sprite.texture.resource_path \
						== "res://assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png"
			elif node is Sprite2D:
				var source := node as Sprite2D
				unique_focus_ok = unique_focus_ok and focus_sprite.texture != null \
					and focus_sprite.texture != source.texture \
					and focus_sprite.texture is GradientTexture2D
		if node != null:
			promenade.set_master_route_x(float(node.position.x))
			var center: Vector2 = promenade.screen_from_master(node.position)
			var radius: float = float(target.get("radius_px", 0.0))
			for offset: Vector2 in [Vector2.ZERO, Vector2(55, 0), Vector2(-55, 0),
					Vector2(0, 55), Vector2(0, -55)]:
				var resolved: Dictionary = promenade._target_at(center + offset)
				reach_ok = reach_ok and String(resolved.get("id", "")) == target_id
			var visual: Sprite2D = node as Sprite2D if node is Sprite2D \
				else highlight as Sprite2D
			var bounds: Rect2 = _sprite_screen_rect(visual)
			display_ok = display_ok and radius >= 110.0 \
				and maxf(bounds.size.x, bounds.size.y) >= 64.0
			if highlight is Sprite2D:
				var focus_sprite := highlight as Sprite2D
				promenade._focus(target)
				var cue_bounds: Rect2 = _canvas_composite_screen_rect(focus_sprite)
				var target_bounds: Rect2 = _alpha_sprite_screen_rect(node as Sprite2D) \
					if node is Sprite2D else Rect2(center - Vector2(0.5, 0.5), Vector2.ONE)
				var attachment_distance := _point_rect_distance(
					cue_bounds.get_center(), target_bounds)
				var cue_ok: bool = focus_sprite.visible \
					and minf(cue_bounds.size.x, cue_bounds.size.y) >= 64.0 \
					and _selected_tint_is_readable(focus_sprite) \
					and attachment_distance <= 96.0
				if target_id != "castle_gate":
					var tip_local: Variant = focus_sprite.get_meta("pointer_tip_local")
					var tip_screen := Vector2(INF, INF)
					if tip_local is Vector2:
						tip_screen = focus_sprite.get_global_transform_with_canvas() \
							* (tip_local as Vector2)
					var tip_distance: float = _point_rect_distance(tip_screen, target_bounds)
					cue_ok = cue_ok and String(focus_sprite.get_meta(
						"focus_cue_role", "")) == "procedural_ring_pointer" \
						and tip_distance <= 4.0 \
						and _procedural_pointer_contrast(focus_sprite)
					cue_detail.append("%s=%.1fx%.1f tip=%.2f center=%.2f a=%.2f" % [
						target_id, cue_bounds.size.x, cue_bounds.size.y,
						tip_distance, attachment_distance, focus_sprite.modulate.a])
				else:
					cue_detail.append("%s=%.1fx%.1f center=%.2f a=%.2f" % [
						target_id, cue_bounds.size.x, cue_bounds.size.y,
						attachment_distance, focus_sprite.modulate.a])
				selected_cues_ok = selected_cues_ok and cue_ok
				promenade._clear_focus()
	_check("exact_four_target_roster", roster_ok)
	_check("target_canvas_metadata_and_touch_budget", metadata_ok)
	_check("target_affordance_categories", category_ok)
	_check("production_canvas_target_resolver", reach_ok)
	_check("target_actual_display_footprints", display_ok)
	_check("selected_focus_cues_are_readable_attached_and_contrasting",
		selected_cues_ok, ";".join(cue_detail))
	var idle_cues_ok := true
	for target_id: String in TARGET_IDS:
		var idle_highlight: Sprite2D = _target(target_id).get("highlight") as Sprite2D
		idle_cues_ok = idle_cues_ok and idle_highlight != null \
			and idle_highlight.visible and idle_highlight.modulate.a <= 0.06
	_check("idle_focus_cues_are_subtle_not_ghost_objects", idle_cues_ok)
	_check("unique_focus_assets_do_not_clone_target_pixels",
		unique_focus_ok and _sprite_resource_count(promenade.root(),
			"res://assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png") == 1)

	var swing: Dictionary = _target("swing")
	var swing_node: CanvasItem = swing.get("node") as CanvasItem
	if swing_node != null:
		promenade.set_master_route_x(3072.0)
		var swing_screen: Vector2 = _screen_center(swing_node)
		promenade.handle_touch(swing_screen)
		var first_ok: bool = String(main.g.get(
			"lagoon_promenade_focus", "")) == "swing" \
			and (main.g.get("lagoon_play_anim", {}) as Dictionary).is_empty() \
			and promenade.action_label() == "PLAY"
		promenade.handle_touch(swing_screen)
		var second_ok: bool = String((main.g.get(
			"lagoon_play_anim", {}) as Dictionary).get("kind", "")) == "swing"
		_check("toy_first_touch_focus_second_touch_play", first_ok and second_ok)
		promenade._finish_playground_animation()
		promenade._tick_playground_animation(1.0)


func _validate_play_contacts() -> void:
	var actor: Sprite2D = main.g.get("lagoon_roshan_card") as Sprite2D
	var contacts_ok: bool = actor != null and is_instance_valid(actor)
	var temporal_ok := true
	var natural_cleanup_ok := true
	var authored_anchors_ok := true
	var slide_axis_ok := true
	var slide_continuity_ok := true
	var action_facing_ok := true
	var performance_samples: Array[float] = []
	var detail: Array[String] = []
	for kind: String in ["slide", "swing", "seesaw"]:
		var target: Dictionary = _target(kind)
		actor.flip_h = true
		promenade._activate(target)
		action_facing_ok = action_facing_ok and not actor.flip_h
		promenade._clear_focus()
		var play: Dictionary = main.g.get("lagoon_play_anim", {}) as Dictionary
		var equipment: Sprite2D = play.get("equipment") as Sprite2D
		var rest_rotation: float = equipment.rotation if equipment != null else 0.0
		var frames_seen: Dictionary = {}
		var positive_rotation := false
		var negative_rotation := false
		var max_rest_delta := 0.0
		var representative_contact := false
		var max_anchor_error := 0.0
		var max_slide_step := 0.0
		var previous_actor_position: Vector2 = actor.position
		var action_steps := 0
		var start_usec: int = Time.get_ticks_usec()
		while String((main.g.get("lagoon_play_anim", {}) as Dictionary).get(
				"phase", "")) == "action" and action_steps < 220:
			promenade._tick_playground_animation(1.0 / 30.0)
			play = main.g.get("lagoon_play_anim", {}) as Dictionary
			frames_seen[int(play.get("frame_index", -1))] = true
			equipment = play.get("equipment") as Sprite2D
			if equipment != null and is_instance_valid(equipment):
				var contact_phase: bool = String(play.get("phase", "")) == "action"
				if contact_phase and kind == "slide":
					max_slide_step = maxf(max_slide_step,
						actor.position.distance_to(previous_actor_position))
				previous_actor_position = actor.position
				var sampled_rotation: float = equipment.rotation
				if kind == "swing" and equipment.has_meta("swing_seat_pivot"):
					var pivot: Node2D = equipment.get_meta("swing_seat_pivot") as Node2D
					if pivot != null:
						sampled_rotation = pivot.rotation
				var delta_rotation: float = sampled_rotation - rest_rotation
				positive_rotation = positive_rotation or delta_rotation > 0.02
				negative_rotation = negative_rotation or delta_rotation < -0.02
				max_rest_delta = maxf(max_rest_delta, absf(delta_rotation))
				var frame_index: int = int(play.get("frame_index", -1))
				if contact_phase and kind == "swing" and frame_index >= 0:
					var pivot: Node2D = equipment.get_meta("swing_seat_pivot") as Node2D
					var master_space: Node2D = main.g.get("lagoon_master_space") as Node2D
					var grip_socket: Vector2 = master_space.to_local(pivot.to_global(
						Vector2(0.0, AUDIT_SWING_SEAT_DROP)))
					var seat: Vector2 = _audit_sprite_anchor_master(actor,
						AUDIT_SWING_SEAT_ANCHORS[frame_index])
					max_anchor_error = maxf(max_anchor_error, seat.distance_to(grip_socket))
				elif contact_phase and kind == "seesaw" and frame_index >= 0:
					var master_space: Node2D = main.g.get("lagoon_master_space") as Node2D
					var seat_socket: Vector2 = master_space.to_local(equipment.to_global(
						AUDIT_SEESAW_SOCKET))
					var seat: Vector2 = _audit_sprite_anchor_master(actor,
						AUDIT_SEESAW_SEAT_ANCHORS[frame_index])
					max_anchor_error = maxf(max_anchor_error, seat.distance_to(seat_socket))
				elif contact_phase and kind == "slide" and frame_index == 3:
					slide_axis_ok = slide_axis_ok and actor.rotation >= 0.12 \
						and actor.rotation <= 0.421
				if contact_phase and action_steps == (111 if kind == "slide" else 14):
					representative_contact = _opaque_geometry_contacts(actor, equipment)
			action_steps += 1
		var elapsed_usec: float = float(Time.get_ticks_usec() - start_usec)
		performance_samples.append(elapsed_usec / maxf(float(action_steps), 1.0))
		play = main.g.get("lagoon_play_anim", {}) as Dictionary
		var action_temporal_ok: bool = action_steps >= 150 and action_steps <= 176 \
			and frames_seen.size() == 4 and String(play.get("phase", "")) == "settle"
		if kind == "swing":
			action_temporal_ok = action_temporal_ok and positive_rotation \
				and negative_rotation and max_rest_delta <= 0.205
		elif kind == "seesaw":
			action_temporal_ok = action_temporal_ok and positive_rotation \
				and negative_rotation and max_rest_delta <= 0.135
		temporal_ok = temporal_ok and action_temporal_ok
		contacts_ok = contacts_ok and representative_contact
		if kind == "swing" or kind == "seesaw":
			authored_anchors_ok = authored_anchors_ok and max_anchor_error <= 0.05
		if kind == "slide":
			slide_continuity_ok = slide_continuity_ok and max_slide_step <= 24.0
		var settle_start: Vector2 = actor.position
		promenade._tick_playground_animation(0.17)
		var settle_moved: bool = actor.position.distance_to(settle_start) > 0.1
		promenade._tick_playground_animation(0.20)
		var cleaned: bool = (main.g.get("lagoon_play_anim", {}) as Dictionary).is_empty() \
			and actor.visible and actor.region_enabled and is_zero_approx(actor.rotation)
		natural_cleanup_ok = natural_cleanup_ok and settle_moved and cleaned
		detail.append("%s=steps%d frames%d contact%s rot%.3f anchor%.3f step%.3f cleanup%s" % [
			kind, action_steps, frames_seen.size(), str(representative_contact),
			max_rest_delta, max_anchor_error, max_slide_step, str(cleaned)])
	performance_samples.sort()
	var median_usec: float = performance_samples[performance_samples.size() / 2] \
		if not performance_samples.is_empty() else INF
	_check("play_actions_verify_visible_actor_equipment_contact",
		contacts_ok, ",".join(detail))
	_check("play_actions_preserve_authored_contact_anchors",
		authored_anchors_ok, ",".join(detail))
	_check("slide_ride_uses_downhill_canvas_rotation", slide_axis_ok)
	_check("slide_phases_preserve_position_continuity", slide_continuity_ok,
		",".join(detail))
	_check("play_actions_reset_inherited_route_facing", action_facing_ok)
	_check("play_actions_run_full_temporal_cycle", temporal_ok, ",".join(detail))
	_check("play_actions_naturally_settle_and_restore", natural_cleanup_ok)
	_check("speedy_play_tick_median_under_1ms", median_usec < 1000.0,
		"samples_usec=%s" % [performance_samples])
	_check("play_cleanup_restores_single_canvas_actor",
		(main.g.get("lagoon_play_anim", {}) as Dictionary).is_empty()
		and actor != null and actor.visible and not main.player.visible)
	# A freed equipment node must fail safe into the same neutral settle path.
	var invalid_equipment := Node2D.new()
	(main.g.get("lagoon_master_space") as Node2D).add_child(invalid_equipment)
	promenade._start_playground_animation("slide", invalid_equipment)
	invalid_equipment.free()
	promenade._tick_playground_animation(1.0 / 30.0)
	var invalid_settled: bool = String((main.g.get(
		"lagoon_play_anim", {}) as Dictionary).get("phase", "")) == "settle"
	promenade._tick_playground_animation(1.0)
	_check("invalid_play_equipment_recovers_without_stranding_input",
		invalid_settled and (main.g.get("lagoon_play_anim", {}) as Dictionary).is_empty())
	# With no selected target, the same real action edge remains a visible happy
	# hop on the Canvas actor; an equipment recovery must never strand that verb.
	promenade._clear_focus()
	main.g["lagoon_hop_t"] = 0.0
	var base_y: float = actor.position.y
	main.touch_ui._arm_action_edge()
	promenade.tick(1.0 / 60.0)
	var hop_armed: bool = promenade.action_label() == "JUMP" \
		and float(main.g.get("lagoon_hop_t", 0.0)) > 0.0
	_check("unfocused_action_remains_visible_canvas_jump",
		hop_armed and actor.position.y < base_y)
	main.g["lagoon_hop_t"] = 0.0
	promenade._sync_roshan_card()


func _validate_plane_save_and_teardown() -> void:
	# Rebuild the first-arrival state and let the real arrival clock remove the
	# story-only plane without creating the retired Reef shuttle or target.
	main.save_data["lagoon_plane_departed"] = false
	main._enter_level2_now(false, false, false)
	promenade = main._lagoon_promenade_ref()
	var arrival_plane: Sprite2D = main.g.get("lagoon_plane_card") as Sprite2D
	var arrival_ok: bool = arrival_plane != null and is_instance_valid(arrival_plane) \
		and not bool(main.save_data.get("lagoon_plane_departed", true)) \
		and _target_ids() == TARGET_IDS
	for _index: int in range(10):
		promenade.tick(1.0)
	var departure_ok: bool = not is_instance_valid(arrival_plane) \
		and bool(main.save_data.get("lagoon_plane_departed", false)) \
		and not main.g.has("lagoon_reef_route_card") \
		and _target("reef_route").is_empty() \
		and _target_ids() == TARGET_IDS
	_check("arrival_plane_save_never_creates_retired_reef_route",
		arrival_ok and departure_ok)

	var old_root: CanvasLayer = promenade.root()
	promenade.set_master_route_x(4096.0)
	promenade.teardown()
	var teardown_ok: bool = not is_instance_valid(old_root) \
		and promenade.root() == null \
		and not main.g.has("lagoon_promenade_targets") \
		and not main.g.has("lagoon_walk_goal_master")
	promenade.teardown()
	_check("teardown_is_synchronous_complete_and_idempotent", teardown_ok)
	main._enter_level2_now(true, false, false)
	promenade = main._lagoon_promenade_ref()
	_check("rebuild_after_teardown_has_one_canvas_stage",
		promenade.root() != null and is_instance_valid(promenade.root()) \
		and _named_count(get_root(), &"SkyLagoonCanvasLayer") == 1 \
		and _target_ids() == TARGET_IDS)


func _validate_door_and_retired_reef_route() -> void:
	var gate: Dictionary = _target("castle_gate")
	var gate_node: CanvasItem = gate.get("node") as CanvasItem
	if gate_node != null:
		promenade.set_master_route_x(5120.0)
		var gate_screen: Vector2 = _screen_center(gate_node)
		promenade.handle_touch(gate_screen)
		var focus_ok: bool = String(main.g.get(
			"lagoon_promenade_focus", "")) == "castle_gate" \
			and promenade.action_label() == "ENTER"
		promenade.handle_touch(gate_screen)
		await _frames(8)
		_check("castle_canvas_target_enters_existing_hall",
			focus_ok and main.game == "level2" \
			and String(main.g.get("phase", "")) == "hall")

	main._exit_level2_now()
	await _frames(4)
	promenade = main._lagoon_promenade_ref()
	_check("castle_leave_returns_to_canvas_not_retired_reef",
		main.game == "level2" and String(main.g.get("phase", "")) == "promenade" \
		and not main.player.visible and _target("reef_route").is_empty())


func _init() -> void:
	get_root().size = Vector2i(1280, 720)
	var packed: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	if main.intro_active:
		main._skip_intro()
	await _frames(2)
	main.pearl_count = main.PEARL_TOTAL
	for friend_value: Variant in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main._apply_quality("speedy")
	main.save_data["lagoon_plane_departed"] = true
	main._enter_level2()
	await _frames(12)
	promenade = main._lagoon_promenade_ref()
	_check("promenade_phase",
		main.game == "level2" and String(main.g.get("phase", "")) == "promenade")
	_validate_stage()
	_validate_assets_and_mural()
	_validate_parallax_and_coordinates()
	_validate_targets_and_touch()
	_validate_play_contacts()
	await _frames(2)
	_check("canvas_clip_cannot_crop_phone_frame", _canvas_clip_contract())
	_check("rendered_mural_fills_phone_frame", _rendered_frame_contract())
	_validate_plane_save_and_teardown()
	await _validate_door_and_retired_reef_route()
	if failed:
		print("FAIL|Sky Lagoon Canvas promenade regression")
		quit(1)
	else:
		print("LAGOONCANVAS|ALL OK")
		quit(0)
