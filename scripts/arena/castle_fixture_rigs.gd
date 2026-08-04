class_name CastleFixtureRigs
extends RefCounted

# Object-local mechanics for the Pearl Castle interaction pass. Authored state
# sheets animate the real fixture. This helper adds only manifest-measured fluid
# emitted from the real outlet/cavity and capped Jolt secondary motion for
# appropriate solids. Objective and menu logic never depend on body settling.

const MANIFEST_PATH := "res://assets/flats/castle/interactions_v3/castle_interactions_v3.json"
const WATER_SHADER := preload("res://assets/shaders/castle_fixture_water.gdshader")
const RIPPLE_TEXTURE := preload("res://assets/terrain/up_water_nrm.jpg")
const CAUSTICS_TEXTURE := preload("res://assets/terrain/caustics.png")
const MAX_JOLT_BODIES := 12
const MAX_AWAKE_BODIES := 8
const WATER_MASK_SIZE := 96
const HINGE_TORQUE_IMPULSE := 0.0045
const BUOYANT_VERTICAL_IMPULSE := 0.045
const BUOYANT_TORQUE_IMPULSE := 0.0018
const MAX_HINGE_ANGLE := 0.21
const MAX_BUOYANT_ANGLE := 0.12
const MAX_HINGE_DISPLACEMENT := 0.35
const MAX_BUOYANT_DISPLACEMENT := 0.06
const JOLT_SETTLE_GRACE_TICKS := 6
const JOLT_FORCE_SETTLE_TICKS := 300
const JOLT_ANGULAR_SPRING := 0.16
const JOLT_ANGULAR_DAMPING := 0.022

var _flow_profile: PackedFloat32Array = PackedFloat32Array([
	0.0, 0.18, 0.62, 1.0, 1.0, 0.68, 0.20, 0.0,
])
var _vortex_profile: PackedFloat32Array = PackedFloat32Array([
	0.0, 0.08, 0.52, 1.18, 1.72, 0.86, 0.24, 0.0,
])

var m: ReefMain
var _water_mask_cache: Dictionary = {}
var _additive_items_by_room: Dictionary = {}


func _init(main: ReefMain) -> void:
	m = main


func visual_spec(room_id: String, item_id: String) -> Dictionary:
	_ensure_manifest()
	return (m.castle_room_fixture_manifest.get(
		room_id + ":" + item_id, {}) as Dictionary).duplicate(true)


func room_additions(room_id: String) -> Array:
	_ensure_manifest()
	return (_additive_items_by_room.get(room_id, []) as Array).duplicate(true)


func _ensure_manifest() -> void:
	if not m.castle_room_fixture_manifest.is_empty():
		return
	if not FileAccess.file_exists(MANIFEST_PATH):
		return
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string(MANIFEST_PATH))
	if not parsed is Dictionary:
		return
	var index: Dictionary = {}
	var additions: Dictionary = {}
	for entry_value: Variant in (parsed as Dictionary).get("assets", []):
		var entry: Dictionary = entry_value as Dictionary
		var room_id: String = String(entry.get("room", ""))
		for instance_value: Variant in entry.get("instances", []):
			var item_id: String = String(instance_value)
			index[room_id + ":" + item_id] = entry
			if String(entry.get("pack", "")) == "v3_addition":
				var room_items: Array = additions.get(room_id, []) as Array
				room_items.append(_runtime_item(entry, item_id))
				additions[room_id] = room_items
	m.castle_room_fixture_manifest = index
	_additive_items_by_room = additions
	_prewarm_water_masks((parsed as Dictionary).get("assets", []))


func _runtime_item(entry: Dictionary, item_id: String) -> Dictionary:
	var position := _vector2(entry.get("placement_position", []), Vector2.ZERO)
	var size := _vector2(entry.get("placement_size", []), Vector2(112.0, 112.0))
	var hotspot_size := _vector2(entry.get("hotspot_size", []), size)
	var hotspot_offset := _vector2(
		entry.get("hotspot_offset", []), Vector2.ZERO)
	var color_values: Array = entry.get("color", [0.72, 0.90, 1.0]) as Array
	var color := Color(0.72, 0.90, 1.0)
	if color_values.size() >= 3:
		color = Color(float(color_values[0]), float(color_values[1]),
			float(color_values[2]))
	return {
		"id": item_id,
		"name": String(entry.get("name", item_id)),
		"pos": position,
		"z": float(entry.get("z", 0.82)),
		"hotspot_offset": hotspot_offset,
		"hotspot_size": hotspot_size,
		"color": color,
	}


func _prewarm_water_masks(asset_values: Array) -> void:
	for asset_value: Variant in asset_values:
		var asset: Dictionary = asset_value as Dictionary
		for layer_value: Variant in asset.get("water_layers", []):
			var layer: Dictionary = layer_value as Dictionary
			if String(layer.get("role", "")) == "bubble_emitter":
				_cache_layer_mask({
					"shape": "ellipse",
					"center": [0.5, 0.5],
					"radius": [0.25, 0.25],
				})
				continue
			var points_frames: Array = layer.get("points_frames", []) as Array
			if points_frames.is_empty():
				_cache_layer_mask(layer)
			else:
				for frame_index in range(points_frames.size()):
					_cache_layer_mask(_layer_geometry_for_frame(
						layer, frame_index))


func _cache_layer_mask(layer: Dictionary) -> void:
	var points := _layer_polygon(layer)
	if points.size() < 3:
		return
	var bounds := _polygon_bounds(points)
	if bounds.size.x <= 0.0001 or bounds.size.y <= 0.0001:
		return
	_polygon_mask(points, bounds)

func rebuild_begin() -> void:
	teardown()


func build(interaction_key: String, piece: Sprite3D, item_data: Dictionary,
		source_position: Vector2, placement_size: Vector2, depth_z: float,
		to_world: Callable) -> Dictionary:
	var visual: Dictionary = item_data.get("v2_visual", {}) as Dictionary
	if visual.is_empty() or piece == null:
		return {}
	var rig: Dictionary = {
		"key": interaction_key,
		"sprite": piece,
		"visual": visual,
		"water": [],
		"body": null,
		"physics_mode": String(visual.get("physics_mode", "none")),
		"base_sprite_position": piece.position,
		"base_sprite_rotation": piece.rotation.z,
	}
	var rig_mode: String = String(rig["physics_mode"])
	rig["peak_angle_radians"] = 0.0
	rig["peak_displacement"] = 0.0
	var default_max_angle := (
		MAX_HINGE_ANGLE if rig_mode == "hinge_z" else MAX_BUOYANT_ANGLE)
	var configured_max_angle := float(visual.get(
		"physics_max_angle_radians", 0.0))
	rig["max_angle_radians"] = configured_max_angle \
		if configured_max_angle > 0.0 else default_max_angle
	rig["impulse_scale"] = clampf(float(visual.get(
		"physics_impulse_scale", 1.0)), 0.05, 1.0)
	rig["max_displacement"] = (
		MAX_HINGE_DISPLACEMENT if rig_mode == "hinge_z"
		else MAX_BUOYANT_DISPLACEMENT)
	piece.set_meta("castle_component_rig_v2", true)
	piece.set_meta("castle_component_rig_v3",
		String(visual.get("pack", "")) == "v3_addition")
	piece.set_meta("primary_animation_is_overlay", false)
	piece.set_meta("generated_full_object_states",
		String(visual.get("render_mode", "")) == "generated_full_object_states")
	piece.set_meta("fixture_water_shader", WATER_SHADER.resource_path)
	piece.set_meta("fixture_water_ripple_texture", RIPPLE_TEXTURE.resource_path)
	piece.set_meta("fixture_water_caustics_texture", CAUSTICS_TEXTURE.resource_path)
	var water_layers: Array = visual.get("water_layers", []) as Array
	_add_water_layers(rig, water_layers, source_position, placement_size,
		depth_z, to_world)
	_add_jolt_driver(rig, source_position, placement_size, depth_z, to_world)
	m.castle_room_fixture_rigs[interaction_key] = rig
	return rig


func activate(interaction_key: String) -> void:
	var rig: Dictionary = m.castle_room_fixture_rigs.get(
		interaction_key, {}) as Dictionary
	if rig.is_empty():
		return
	var body: RigidBody3D = rig.get("body") as RigidBody3D
	if body == null or not is_instance_valid(body):
		return
	var already_awake := not body.freeze and not body.sleeping
	if not already_awake and _awake_count() >= MAX_AWAKE_BODIES:
		return
	rig["peak_angle_radians"] = 0.0
	rig["peak_displacement"] = 0.0
	body.freeze = false
	body.sleeping = false
	var direction := -1.0 if abs(interaction_key.hash()) % 2 == 0 else 1.0
	rig["jolt_direction"] = direction
	rig["jolt_phase"] = "wake"
	rig["jolt_active_ticks"] = 0


func apply_frame(interaction_key: String, timeline_step: int,
		timeline_count: int, atlas_frame: int = -1) -> void:
	var rig: Dictionary = m.castle_room_fixture_rigs.get(
		interaction_key, {}) as Dictionary
	if rig.is_empty():
		return
	var timeline_t := float(timeline_step) / float(maxi(1, timeline_count - 1))
	var water_frame_index := atlas_frame if atlas_frame >= 0 else timeline_step
	var amount := _sample_profile(_flow_profile, timeline_t)
	var vortex := _sample_profile(_vortex_profile, timeline_t)
	var any_water_active := false
	for water_value: Variant in rig.get("water", []):
		var water: Dictionary = water_value as Dictionary
		var material: ShaderMaterial = water.get("material") as ShaderMaterial
		var node: Sprite3D = water.get("node") as Sprite3D
		if material == null or node == null:
			continue
		_update_polygon_water_for_frame(water, water_frame_index)
		var role: String = String(water.get("role", "water"))
		var flow_start: float = float(water.get("flow_start", 0.0))
		var layer_amount := clampf(
			(amount - flow_start) / maxf(0.001, 1.0 - flow_start), 0.0, 1.0)
		var active_frames: Array = water.get("active_frames", []) as Array
		var active_frame_matches: bool = active_frames.is_empty()
		for active_frame_value: Variant in active_frames:
			if int(active_frame_value) == water_frame_index:
				active_frame_matches = true
				break
		if not active_frame_matches:
			layer_amount = 0.0
		if role == "ripple":
			layer_amount = minf(1.0, layer_amount * 1.15)
		material.set_shader_parameter("flow_amount", layer_amount)
		var progressive_fill := bool(water.get("stream", false)) or role in [
			"stream", "waterfall_band", "fill", "basin", "cup_fill",
		]
		material.set_shader_parameter("fill_amount",
			maxf(0.02, layer_amount) if progressive_fill else 1.0)
		material.set_shader_parameter("vortex_strength",
			vortex if role == "vortex" else 0.0)
		_position_water_for_frame(water, timeline_t)
		node.visible = layer_amount > 0.01
		any_water_active = any_water_active or node.visible
		water["flow_amount"] = layer_amount
	var sprite: Sprite3D = rig.get("sprite") as Sprite3D
	if sprite != null:
		sprite.set_meta("fixture_timeline_frame", timeline_step)
		sprite.set_meta("fixture_timeline_frame_count", timeline_count)
		sprite.set_meta("fixture_water_atlas_frame", water_frame_index)
		sprite.set_meta("fixture_water_active", any_water_active)


func tick(_delta: float) -> void:
	var alive: Array[RigidBody3D] = []
	var awake := 0
	for body: RigidBody3D in m.castle_room_fixture_physics:
		if body == null or not is_instance_valid(body):
			continue
		alive.append(body)
		if not body.sleeping and not body.freeze:
			awake += 1
	m.castle_room_fixture_physics = alive
	m.g["castle_fixture_jolt_allocated"] = alive.size()
	m.g["castle_fixture_jolt_awake"] = awake
	for rig_value: Variant in m.castle_room_fixture_rigs.values():
		_tick_bubbles(rig_value as Dictionary)


func physics_tick(_delta: float) -> void:
	for rig_value: Variant in m.castle_room_fixture_rigs.values():
		_tick_body(rig_value as Dictionary)


func stats() -> Dictionary:
	return {
		"rigs": m.castle_room_fixture_rigs.size(),
		"allocated": m.castle_room_fixture_physics.size(),
		"awake": _awake_count(),
		"body_cap": MAX_JOLT_BODIES,
		"awake_cap": MAX_AWAKE_BODIES,
		"water_mask_cache_entries": _water_mask_cache.size(),
	}


func teardown() -> void:
	for body: RigidBody3D in m.castle_room_fixture_physics:
		if body != null and is_instance_valid(body):
			body.free()
	for rig_value: Variant in m.castle_room_fixture_rigs.values():
		var rig: Dictionary = rig_value as Dictionary
		for water_value: Variant in rig.get("water", []):
			var water: Dictionary = water_value as Dictionary
			var node: Sprite3D = water.get("node") as Sprite3D
			if node != null and is_instance_valid(node):
				node.free()
	m.castle_room_fixture_physics.clear()
	m.castle_room_fixture_rigs.clear()
	m.g.erase("castle_fixture_jolt_allocated")
	m.g.erase("castle_fixture_jolt_awake")


func _add_water_layers(rig: Dictionary, layers: Array,
		source_position: Vector2, placement_size: Vector2, depth_z: float,
		to_world: Callable) -> void:
	if m.castle_room_item_visual_layer == null:
		return
	for layer_value: Variant in layers:
		var layer: Dictionary = layer_value as Dictionary
		if String(layer.get("role", "")) == "bubble_emitter":
			_add_bubble_emitter(rig, layer, source_position, placement_size,
				depth_z, to_world)
		else:
			_add_water_layer(rig, layer, source_position, placement_size,
				depth_z, to_world)


func _add_bubble_emitter(rig: Dictionary, emitter: Dictionary,
		source_position: Vector2, placement_size: Vector2, depth_z: float,
		to_world: Callable) -> void:
	var outlet_frames: Array = emitter.get("outlet_frames", []) as Array
	if outlet_frames.is_empty():
		return
	var relative_centers: Array = emitter.get("relative_centers", []) as Array
	for index in range(relative_centers.size()):
		var relative := _vector2(relative_centers[index], Vector2.ZERO)
		var center_frames: Array = []
		for outlet_value: Variant in outlet_frames:
			var outlet := _vector2(outlet_value, Vector2.ZERO)
			center_frames.append([outlet.x + relative.x, outlet.y + relative.y])
		var radius_value: float = 0.028 + float(index % 2) * 0.010
		var layer := {
			"role": "bubble",
			"shape": "ellipse",
			"center": center_frames[0],
			"radius": [radius_value, radius_value],
			"center_frames": center_frames,
			"flow_start": float(emitter.get("flow_start", 0.15)),
			"z_offset": float(emitter.get("z_offset", 0.010))
				+ float(index) * 0.0002,
		}
		_add_water_layer(rig, layer, source_position, placement_size,
			depth_z, to_world)
		var water_layers: Array = rig["water"] as Array
		var water: Dictionary = water_layers[water_layers.size() - 1] as Dictionary
		water["bubble_index"] = index


func _add_water_layer(rig: Dictionary, layer: Dictionary,
		source_position: Vector2, placement_size: Vector2, depth_z: float,
		to_world: Callable) -> void:
	var geometry_layer := _layer_geometry_for_frame(layer, 0)
	var normalized_points := _layer_polygon(geometry_layer)
	if normalized_points.size() < 3:
		return
	var bounds := _polygon_bounds(normalized_points)
	if bounds.size.x <= 0.0001 or bounds.size.y <= 0.0001:
		return
	var mask_texture := _polygon_mask(normalized_points, bounds)
	var z_offset: float = float(layer.get("z_offset", 0.010))
	var center_normalized := bounds.position + bounds.size * 0.5
	var center_art := source_position + center_normalized * placement_size
	var center_world: Vector3 = to_world.call(center_art, depth_z + z_offset)
	var left_world: Vector3 = to_world.call(
		Vector2(source_position.x + bounds.position.x * placement_size.x,
			center_art.y), depth_z + z_offset)
	var right_world: Vector3 = to_world.call(
		Vector2(source_position.x + bounds.end.x * placement_size.x,
			center_art.y), depth_z + z_offset)
	var top_world: Vector3 = to_world.call(
		Vector2(center_art.x,
			source_position.y + bounds.position.y * placement_size.y),
		depth_z + z_offset)
	var bottom_world: Vector3 = to_world.call(
		Vector2(center_art.x,
			source_position.y + bounds.end.y * placement_size.y),
		depth_z + z_offset)
	var node := Sprite3D.new()
	node.name = "FixtureWater_" + String(layer.get("role", "water"))
	node.texture = mask_texture
	node.centered = true
	node.shaded = false
	node.no_depth_test = false
	node.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	node.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
	node.pixel_size = 0.01
	node.scale = Vector3(
		absf(right_world.x - left_world.x)
			/ (float(WATER_MASK_SIZE) * node.pixel_size),
		absf(top_world.y - bottom_world.y)
			/ (float(WATER_MASK_SIZE) * node.pixel_size),
		1.0)
	node.position = center_world
	node.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var material := ShaderMaterial.new()
	material.shader = WATER_SHADER
	material.set_shader_parameter("shape_mask", mask_texture)
	material.set_shader_parameter("ripple", RIPPLE_TEXTURE)
	material.set_shader_parameter("caustics", CAUSTICS_TEXTURE)
	material.set_shader_parameter("flow_amount", 0.0)
	material.set_shader_parameter("fill_amount", 1.0)
	var role: String = String(layer.get("role", "water"))
	var stream_mode := bool(layer.get("stream", false)) \
		or role in ["stream", "waterfall_band"]
	material.set_shader_parameter("stream_mode", stream_mode)
	material.set_shader_parameter("reveal_from_top", stream_mode)
	material.set_shader_parameter("flow_axis",
		Vector2(0.0, 1.0) if stream_mode else Vector2(1.0, 0.15))
	material.set_shader_parameter("deep_color",
		_layer_color(layer, "deep", Color(0.10, 0.50, 0.76)))
	material.set_shader_parameter("shallow_color",
		_layer_color(layer, "shallow", Color(0.48, 0.90, 0.96)))
	material.render_priority = int(layer.get("render_priority", 1))
	node.material_override = material
	node.visible = false
	node.set_meta("castle_fixture_water", true)
	node.set_meta("water_role", role)
	node.set_meta("bounded_to_fixture", true)
	node.set_meta("sprite_masked_water", true)
	node.set_meta("depth_write_disabled", true)
	node.set_meta("logic_authority", false)
	node.set_meta("fixture_bounds_normalized", bounds)
	node.set_meta("fixture_outlet_normalized", _layer_outlet(geometry_layer))
	node.set_meta("water_shape", String(layer.get("shape", "")))
	m.castle_room_item_visual_layer.add_child(node)
	var water: Dictionary = {
		"node": node,
		"material": material,
		"role": role,
		"shape": String(layer.get("shape", "")),
		"stream": bool(layer.get("stream", false)),
		"base_position": node.position,
		"flow_amount": 0.0,
		"flow_start": float(layer.get("flow_start", 0.0)),
		"center_frames": layer.get("center_frames", []),
		"points_frames": layer.get("points_frames", []),
		"active_frames": layer.get("active_frames", []),
		"layer_spec": layer.duplicate(true),
		"source_position": source_position,
		"placement_size": placement_size,
		"depth_z": depth_z + z_offset,
		"to_world": to_world,
		"base_center_normalized": center_normalized,
		"bounds_normalized": bounds,
		"outlet_normalized": _layer_outlet(geometry_layer),
	}
	(rig["water"] as Array).append(water)


func _layer_geometry_for_frame(layer: Dictionary,
		frame_index: int) -> Dictionary:
	var geometry := layer.duplicate(true)
	var points_frames: Array = layer.get("points_frames", []) as Array
	if not points_frames.is_empty():
		var index := clampi(frame_index, 0, points_frames.size() - 1)
		geometry["points"] = points_frames[index]
	return geometry


func _update_polygon_water_for_frame(water: Dictionary,
		frame_index: int) -> void:
	var points_frames: Array = water.get("points_frames", []) as Array
	if points_frames.is_empty():
		return
	var layer: Dictionary = water.get("layer_spec", {}) as Dictionary
	var geometry := _layer_geometry_for_frame(layer, frame_index)
	var points := _layer_polygon(geometry)
	if points.size() < 3:
		return
	var bounds := _polygon_bounds(points)
	if bounds.size.x <= 0.0001 or bounds.size.y <= 0.0001:
		return
	var node: Sprite3D = water.get("node") as Sprite3D
	var material: ShaderMaterial = water.get("material") as ShaderMaterial
	if node == null or material == null:
		return
	var mask_texture := _polygon_mask(points, bounds)
	node.texture = mask_texture
	material.set_shader_parameter("shape_mask", mask_texture)
	var source_position: Vector2 = water.get(
		"source_position", Vector2.ZERO) as Vector2
	var placement_size: Vector2 = water.get(
		"placement_size", Vector2.ONE) as Vector2
	var to_world: Callable = water.get("to_world") as Callable
	var depth_z: float = float(water.get("depth_z", 0.0))
	var center_normalized := bounds.position + bounds.size * 0.5
	var center_art := source_position + center_normalized * placement_size
	var center_world: Vector3 = to_world.call(center_art, depth_z)
	var left_world: Vector3 = to_world.call(Vector2(
		source_position.x + bounds.position.x * placement_size.x,
		center_art.y), depth_z)
	var right_world: Vector3 = to_world.call(Vector2(
		source_position.x + bounds.end.x * placement_size.x,
		center_art.y), depth_z)
	var top_world: Vector3 = to_world.call(Vector2(center_art.x,
		source_position.y + bounds.position.y * placement_size.y), depth_z)
	var bottom_world: Vector3 = to_world.call(Vector2(center_art.x,
		source_position.y + bounds.end.y * placement_size.y), depth_z)
	node.position = center_world
	node.scale = Vector3(
		absf(right_world.x - left_world.x)
			/ (float(WATER_MASK_SIZE) * node.pixel_size),
		absf(top_world.y - bottom_world.y)
			/ (float(WATER_MASK_SIZE) * node.pixel_size),
		1.0)
	var outlet := _layer_outlet(geometry)
	node.set_meta("fixture_bounds_normalized", bounds)
	node.set_meta("fixture_outlet_normalized", outlet)
	water["base_position"] = node.position
	water["base_center_normalized"] = center_normalized
	water["bounds_normalized"] = bounds
	water["outlet_normalized"] = outlet


func _layer_polygon(layer: Dictionary) -> PackedVector2Array:
	var points := PackedVector2Array()
	if String(layer.get("shape", "")) == "ellipse":
		var center := _vector2(layer.get("center", []), Vector2(0.5, 0.5))
		var radius := _vector2(layer.get("radius", []), Vector2(0.2, 0.08))
		for step in range(32):
			var angle := TAU * float(step) / 32.0
			points.append(center + Vector2(
				cos(angle) * radius.x, sin(angle) * radius.y))
		return points
	var raw_points: Array = layer.get("points", []) as Array
	for point_value: Variant in raw_points:
		points.append(_vector2(point_value, Vector2.ZERO))
	return points


func _layer_outlet(layer: Dictionary) -> Vector2:
	if String(layer.get("shape", "")) == "ellipse":
		return _vector2(layer.get("center", []), Vector2(0.5, 0.5))
	var raw_points: Array = layer.get("points", []) as Array
	if raw_points.size() >= 2:
		return (_vector2(raw_points[0], Vector2.ZERO)
			+ _vector2(raw_points[1], Vector2.ZERO)) * 0.5
	return Vector2(0.5, 0.5)

func _polygon_bounds(points: PackedVector2Array) -> Rect2:
	var minimum := Vector2(INF, INF)
	var maximum := Vector2(-INF, -INF)
	for point: Vector2 in points:
		minimum.x = minf(minimum.x, point.x)
		minimum.y = minf(minimum.y, point.y)
		maximum.x = maxf(maximum.x, point.x)
		maximum.y = maxf(maximum.y, point.y)
	return Rect2(minimum, maximum - minimum)


func _polygon_mask(points: PackedVector2Array, bounds: Rect2) -> ImageTexture:
	var cache_key := _mask_cache_key(points, bounds)
	var cached: ImageTexture = _water_mask_cache.get(cache_key) as ImageTexture
	if cached != null:
		return cached
	var image := Image.create_empty(
		WATER_MASK_SIZE, WATER_MASK_SIZE, false, Image.FORMAT_RGBA8)
	var offsets := [
		Vector2(0.25, 0.25), Vector2(0.75, 0.25),
		Vector2(0.25, 0.75), Vector2(0.75, 0.75),
	]
	for y in range(WATER_MASK_SIZE):
		for x in range(WATER_MASK_SIZE):
			var coverage := 0.0
			for offset: Vector2 in offsets:
				var uv := (Vector2(float(x), float(y)) + offset) \
					/ float(WATER_MASK_SIZE)
				var sample := bounds.position + uv * bounds.size
				if Geometry2D.is_point_in_polygon(sample, points):
					coverage += 0.25
			if coverage > 0.0:
				image.set_pixel(x, y, Color(1.0, 1.0, 1.0, coverage))
	var texture := ImageTexture.create_from_image(image)
	_water_mask_cache[cache_key] = texture
	return texture


func _mask_cache_key(points: PackedVector2Array, bounds: Rect2) -> String:
	var parts := PackedStringArray()
	for point: Vector2 in points:
		var normalized := (point - bounds.position) / bounds.size
		parts.append("%.5f,%.5f" % [normalized.x, normalized.y])
	return "|".join(parts)

func _position_water_for_frame(water: Dictionary, timeline_t: float) -> void:
	var center_frames: Array = water.get("center_frames", []) as Array
	if center_frames.is_empty():
		return
	var center := _sample_vector_frames(center_frames, timeline_t)
	var base_center: Vector2 = water.get(
		"base_center_normalized", center) as Vector2
	var source_position: Vector2 = water.get(
		"source_position", Vector2.ZERO) as Vector2
	var placement_size: Vector2 = water.get(
		"placement_size", Vector2.ONE) as Vector2
	var to_world: Callable = water.get("to_world") as Callable
	var depth_z: float = float(water.get("depth_z", 0.0))
	var art_position := source_position + center * placement_size
	var node: Sprite3D = water.get("node") as Sprite3D
	if node == null:
		return
	node.position = to_world.call(art_position, depth_z)
	water["base_position"] = node.position
	water["base_center_normalized"] = base_center


func _sample_profile(profile: PackedFloat32Array, timeline_t: float) -> float:
	if profile.is_empty():
		return 0.0
	var scaled := clampf(timeline_t, 0.0, 1.0) * float(profile.size() - 1)
	var left := clampi(int(floor(scaled)), 0, profile.size() - 1)
	var right := mini(left + 1, profile.size() - 1)
	return lerpf(profile[left], profile[right], scaled - float(left))


func _sample_vector_frames(frames: Array, timeline_t: float) -> Vector2:
	if frames.is_empty():
		return Vector2.ZERO
	var scaled := clampf(timeline_t, 0.0, 1.0) * float(frames.size() - 1)
	var left := clampi(int(floor(scaled)), 0, frames.size() - 1)
	var right := mini(left + 1, frames.size() - 1)
	return _vector2(frames[left], Vector2.ZERO).lerp(
		_vector2(frames[right], Vector2.ZERO), scaled - float(left))


func _vector2(value: Variant, fallback: Vector2) -> Vector2:
	if value is Array:
		var values: Array = value as Array
		if values.size() >= 2:
			return Vector2(float(values[0]), float(values[1]))
	return fallback


func _layer_color(layer: Dictionary, key: String, fallback: Color) -> Color:
	var value: Variant = layer.get(key, [])
	if value is Array:
		var values: Array = value as Array
		if values.size() >= 3:
			return Color(float(values[0]), float(values[1]), float(values[2]),
				float(values[3]) if values.size() >= 4 else 1.0)
	return fallback


func _add_jolt_driver(rig: Dictionary, source_position: Vector2,
		placement_size: Vector2, depth_z: float, to_world: Callable) -> void:
	var mode: String = String(rig.get("physics_mode", "none"))
	if mode == "none" or m.castle_room_fixture_physics.size() >= MAX_JOLT_BODIES:
		return
	var visual: Dictionary = rig.get("visual", {}) as Dictionary
	var pivot_array: Array = visual.get("physics_pivot", [0.5, 0.5]) as Array
	var pivot_normalized := Vector2(
		float(pivot_array[0]), float(pivot_array[1]))
	var pivot_art := source_position + pivot_normalized * placement_size
	var pivot_world: Vector3 = to_world.call(pivot_art, depth_z)
	var sprite: Sprite3D = rig.get("sprite") as Sprite3D
	var body := RigidBody3D.new()
	body.name = "CastleFixtureJolt_" + String(rig.get("key", "fixture"))
	body.collision_layer = 0
	body.collision_mask = 0
	body.mass = 0.65
	body.gravity_scale = 0.0
	body.linear_damp = 2.8
	body.angular_damp = 3.8
	body.can_sleep = true
	body.axis_lock_linear_x = true
	body.axis_lock_linear_z = true
	body.axis_lock_angular_x = true
	body.axis_lock_angular_y = true
	body.axis_lock_angular_z = false
	body.axis_lock_linear_y = mode == "hinge_z"
	var collision := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(0.12, 0.12, 0.05)
	collision.shape = shape
	body.add_child(collision)
	body.position = pivot_world if mode == "hinge_z" else sprite.position
	body.freeze = true
	body.set_meta("castle_fixture_jolt_garnish", true)
	body.set_meta("logic_authority", false)
	body.set_meta("sleep_required", true)
	body.set_meta("depth_axis_locked", true)
	m.castle_room_item_visual_layer.add_child(body)
	m.castle_room_fixture_physics.append(body)
	rig["body"] = body
	rig["rest_body_position"] = body.position
	rig["pivot_offset"] = sprite.position - body.position
	rig["base_sprite_position"] = sprite.position
	rig["jolt_direction"] = 1.0
	rig["jolt_phase"] = "idle"
	rig["jolt_active_ticks"] = 0


func _tick_body(rig: Dictionary) -> void:
	var body: RigidBody3D = rig.get("body") as RigidBody3D
	var sprite: Sprite3D = rig.get("sprite") as Sprite3D
	if body == null or sprite == null or not is_instance_valid(body):
		return
	var rest_position: Vector3 = rig.get(
		"rest_body_position", body.position) as Vector3
	var jolt_phase: String = String(rig.get("jolt_phase", "idle"))
	if body.freeze:
		if jolt_phase == "idle":
			return
		body.freeze = false
	if jolt_phase == "wake":
		body.sleeping = false
		rig["jolt_phase"] = "kick"
		return
	if jolt_phase == "kick":
		body.sleeping = false
		_apply_jolt_impulse(rig)
		rig["jolt_phase"] = "observe"
		rig["jolt_active_ticks"] = 0
		return
	var active_ticks: int = int(rig.get("jolt_active_ticks", 0)) + 1
	rig["jolt_active_ticks"] = active_ticks
	if body.sleeping:
		if active_ticks < JOLT_SETTLE_GRACE_TICKS:
			body.sleeping = false
			return
		_settle_body(rig, rest_position)
		return
	var mode: String = String(rig.get("physics_mode", "none"))
	var max_angle: float = float(rig.get("max_angle_radians", 0.12))
	if mode == "hinge_z":
		var hinge_displacement_limit: float = float(
			rig.get("max_displacement", MAX_HINGE_DISPLACEMENT))
		var pivot_offset: Vector3 = rig.get("pivot_offset", Vector3.ZERO)
		var pivot_radius := Vector2(pivot_offset.x, pivot_offset.y).length()
		if pivot_radius > hinge_displacement_limit * 0.5:
			var displacement_ratio := clampf(
				(hinge_displacement_limit - 0.001) / (2.0 * pivot_radius),
				0.0, 1.0)
			max_angle = minf(max_angle, 2.0 * asin(displacement_ratio))
	var angle: float = clampf(body.rotation.z, -max_angle, max_angle)
	if not is_equal_approx(angle, body.rotation.z):
		var clamped_rotation: Vector3 = body.rotation
		clamped_rotation.z = angle
		body.rotation = clamped_rotation
		var angular_velocity: Vector3 = body.angular_velocity
		angular_velocity.z = clampf(angular_velocity.z, -4.0, 4.0)
		body.angular_velocity = angular_velocity
	body.apply_torque(Vector3(
		0.0, 0.0, -angle * JOLT_ANGULAR_SPRING
			- body.angular_velocity.z * JOLT_ANGULAR_DAMPING))
	if mode == "buoyant":
		var max_displacement: float = float(rig.get("max_displacement", 0.06))
		var displacement: float = body.position.y - rest_position.y
		if absf(displacement) > max_displacement:
			var clamped_position: Vector3 = body.position
			clamped_position.y = rest_position.y + clampf(
				displacement, -max_displacement, max_displacement)
			body.position = clamped_position
			var linear_velocity: Vector3 = body.linear_velocity
			linear_velocity.y = clampf(linear_velocity.y, -0.32, 0.32)
			body.linear_velocity = linear_velocity
			displacement = body.position.y - rest_position.y
		body.apply_central_force(Vector3(
			0.0, -displacement * 7.0 - body.linear_velocity.y * 2.2, 0.0))
	_sync_body_sprite(rig)
	_record_body_peak(rig)
	var position_error: float = body.position.distance_to(rest_position)
	var recorded_motion: bool = \
		float(rig.get("peak_angle_radians", 0.0)) > 0.001 \
		and float(rig.get("peak_displacement", 0.0)) > 0.001
	var naturally_settled: bool = absf(angle) < 0.008 \
			and position_error < 0.008 \
			and body.angular_velocity.length() < 0.012 \
			and body.linear_velocity.length() < 0.012
	if active_ticks >= JOLT_FORCE_SETTLE_TICKS \
			or (active_ticks >= JOLT_SETTLE_GRACE_TICKS \
				and recorded_motion and naturally_settled):
		_settle_body(rig, rest_position)


func _apply_jolt_impulse(rig: Dictionary) -> void:
	var body: RigidBody3D = rig.get("body") as RigidBody3D
	if body == null:
		return
	var mode: String = String(rig.get("physics_mode", "none"))
	var direction: float = float(rig.get("jolt_direction", 1.0))
	var impulse_scale: float = float(rig.get("impulse_scale", 1.0))
	if mode == "hinge_z":
		body.apply_torque_impulse(Vector3(
			0.0, 0.0, direction * HINGE_TORQUE_IMPULSE * impulse_scale))
	elif mode == "buoyant":
		body.apply_central_impulse(Vector3(
			0.0, BUOYANT_VERTICAL_IMPULSE * impulse_scale, 0.0))
		body.apply_torque_impulse(Vector3(
			0.0, 0.0, direction * BUOYANT_TORQUE_IMPULSE * impulse_scale))


func _settle_body(rig: Dictionary, rest_position: Vector3) -> void:
	var body: RigidBody3D = rig.get("body") as RigidBody3D
	if body == null:
		return
	body.position = rest_position
	body.rotation.z = 0.0
	body.linear_velocity = Vector3.ZERO
	body.angular_velocity = Vector3.ZERO
	_sync_body_sprite(rig)
	body.freeze = true
	body.sleeping = true
	rig["jolt_phase"] = "idle"
	rig["jolt_active_ticks"] = 0


func _record_body_peak(rig: Dictionary) -> void:
	var body: RigidBody3D = rig.get("body") as RigidBody3D
	var sprite: Sprite3D = rig.get("sprite") as Sprite3D
	if body == null or sprite == null:
		return
	var base_position: Vector3 = rig.get(
		"base_sprite_position", sprite.position) as Vector3
	rig["peak_angle_radians"] = maxf(
		float(rig.get("peak_angle_radians", 0.0)), absf(body.rotation.z))
	rig["peak_displacement"] = maxf(
		float(rig.get("peak_displacement", 0.0)),
		sprite.position.distance_to(base_position))

func _sync_body_sprite(rig: Dictionary) -> void:
	var body: RigidBody3D = rig.get("body") as RigidBody3D
	var sprite: Sprite3D = rig.get("sprite") as Sprite3D
	if body == null or sprite == null:
		return
	var mode: String = String(rig.get("physics_mode", "none"))
	var angle := body.rotation.z
	if mode == "hinge_z":
		var pivot_offset: Vector3 = rig.get("pivot_offset", Vector3.ZERO)
		var rotated := Vector2(pivot_offset.x, pivot_offset.y).rotated(angle)
		sprite.position = body.position + Vector3(
			rotated.x, rotated.y, pivot_offset.z)
	else:
		sprite.position = body.position
	sprite.rotation.z = angle


func _tick_bubbles(rig: Dictionary) -> void:
	var now := float(Time.get_ticks_msec()) * 0.001
	for water_value: Variant in rig.get("water", []):
		var water: Dictionary = water_value as Dictionary
		if String(water.get("role", "")) != "bubble":
			continue
		var node: Sprite3D = water.get("node") as Sprite3D
		if node == null or not is_instance_valid(node):
			continue
		var base: Vector3 = water.get("base_position", Vector3.ZERO)
		var index: int = int(water.get("bubble_index", 0))
		var amount: float = float(water.get("flow_amount", 0.0))
		node.position = base + Vector3(
			sin(now * 1.7 + float(index)) * 0.012 * amount,
			fmod(now * (0.05 + float(index) * 0.009), 0.11) * amount,
			0.0)


func _awake_count() -> int:
	var awake := 0
	for body: RigidBody3D in m.castle_room_fixture_physics:
		if body != null and is_instance_valid(body) \
				and not body.freeze and not body.sleeping:
			awake += 1
	return awake
