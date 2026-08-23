extends Node2D
class_name CastleWaterFixture2D

# Canvas-only renderer for manifest-authored fixture water. The caller owns the
# fixture Sprite2D and this component owns only the Polygon2D/Line2D children it
# creates. Prefer adding the component as a child of the fixture before calling
# configure(), so transforms and scene teardown are inherited automatically.

signal configured(valid_layers: int, rejected_layers: int)
signal timeline_applied(timeline_step: int, timeline_count: int,
		atlas_frame: int, active_layers: int)

const ELLIPSE_SEGMENTS := 32
const MIN_VISIBLE_AMOUNT := 0.01
const DEFAULT_DEEP_COLOR := Color(0.10, 0.50, 0.76, 1.0)
const DEFAULT_SHALLOW_COLOR := Color(0.48, 0.90, 0.96, 1.0)
static var DEFAULT_FLOW_PROFILE := PackedFloat32Array([
	0.0, 0.18, 0.62, 1.0, 1.0, 0.68, 0.20, 0.0,
])
static var DEFAULT_VORTEX_PROFILE := PackedFloat32Array([
	0.0, 0.08, 0.52, 1.18, 1.72, 0.86, 0.24, 0.0,
])

var _fixture: Sprite2D
var _frame_size := Vector2.ZERO
var _frame_origin := Vector2.ZERO
var _layers: Array[Dictionary] = []
var _profiles: Dictionary = {}
var _rejected_layers := 0
var _active_layers := 0
var _timeline_step := 0
var _timeline_count := 1
var _atlas_frame := 0
var _flow_amount := 0.0
var _vortex_amount := 0.0


func configure(fixture_sprite: Sprite2D, water_layers: Array,
		frame_size_override: Vector2 = Vector2.ZERO,
		authored_profiles: Dictionary = {}) -> bool:
	_clear_generated_layers()
	_fixture = fixture_sprite
	_profiles = authored_profiles.duplicate(true)
	_rejected_layers = 0
	_active_layers = 0
	_timeline_step = 0
	_timeline_count = 1
	_atlas_frame = 0
	_flow_amount = 0.0
	_vortex_amount = 0.0
	if _fixture == null or not is_instance_valid(_fixture):
		_fixture = null
		_set_component_metadata(false)
		configured.emit(0, water_layers.size())
		return false
	_frame_size = frame_size_override if frame_size_override.x > 0.0 \
		and frame_size_override.y > 0.0 else _fixture_frame_size(_fixture)
	if _frame_size.x <= 0.0 or _frame_size.y <= 0.0:
		_set_component_metadata(false)
		configured.emit(0, water_layers.size())
		return false
	_frame_origin = _fixture.offset
	if _fixture.centered:
		_frame_origin -= _frame_size * 0.5
	_sync_to_fixture()
	for layer_value: Variant in water_layers:
		if not layer_value is Dictionary:
			_rejected_layers += 1
			continue
		_add_layer((layer_value as Dictionary).duplicate(true))
	_set_component_metadata(not _layers.is_empty())
	apply_timeline(0, 1, 0)
	configured.emit(_layers.size(), _rejected_layers)
	return not _layers.is_empty()


func apply_timeline(timeline_step: int, timeline_count: int,
		atlas_frame: int = -1) -> Dictionary:
	_timeline_count = maxi(1, timeline_count)
	_timeline_step = clampi(timeline_step, 0, _timeline_count - 1)
	_atlas_frame = atlas_frame if atlas_frame >= 0 else _timeline_step
	var timeline_t := float(_timeline_step) / float(maxi(1,
		_timeline_count - 1))
	_flow_amount = _sample_profile(_profile_for_role("flow"), timeline_t)
	_vortex_amount = _sample_profile(_profile_for_role("vortex"), timeline_t)
	_active_layers = 0
	_sync_to_fixture()
	for layer: Dictionary in _layers:
		_apply_layer(layer, timeline_t)
	_set_component_metadata(_fixture != null and is_instance_valid(_fixture)
		and not _layers.is_empty())
	var snapshot := stats()
	timeline_applied.emit(_timeline_step, _timeline_count, _atlas_frame,
		_active_layers)
	return snapshot


func reset_to_rest(rest_frame: int = 0) -> void:
	apply_timeline(0, 1, rest_frame)


func sync_to_fixture() -> void:
	_sync_to_fixture()


func stats() -> Dictionary:
	return {
		"configured": _fixture != null and is_instance_valid(_fixture)
			and not _layers.is_empty(),
		"canvas_only": true,
		"uses_shader": false,
		"physics_bodies": 0,
		"layer_count": _layers.size(),
		"polygon_count": _layers.size(),
		"line_count": _layers.size(),
		"rejected_layers": _rejected_layers,
		"active_layers": _active_layers,
		"timeline_step": _timeline_step,
		"timeline_count": _timeline_count,
		"atlas_frame": _atlas_frame,
		"flow_amount": _flow_amount,
		"vortex_amount": _vortex_amount,
		"frame_size": _frame_size,
		"roles": _role_names(),
		"fixture_instance_id": _fixture.get_instance_id() \
			if _fixture != null and is_instance_valid(_fixture) else 0,
	}


func layer_metadata() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for layer: Dictionary in _layers:
		var root: Node2D = layer.get("root") as Node2D
		result.append({
			"role": String(layer.get("role", "water")),
			"shape": String(layer.get("shape", "")),
			"active": root != null and root.visible,
			"flow_amount": float(layer.get("flow_amount", 0.0)),
			"flow_start": float(layer.get("flow_start", 0.0)),
			"bounds_normalized": layer.get("bounds_normalized", Rect2()),
			"outlet_normalized": layer.get("outlet_normalized",
				Vector2(0.5, 0.5)),
			"active_frames": (layer.get("active_frames", []) as Array).duplicate(),
			"render_priority": int(layer.get("render_priority", 0)),
		})
	return result


func teardown() -> void:
	# The fixture is intentionally not freed; ownership stays with the caller.
	queue_free()


func _add_layer(spec: Dictionary) -> void:
	var shape := String(spec.get("shape", ""))
	if shape not in ["polygon", "ellipse"]:
		_rejected_layers += 1
		return
	var normalized_points := _layer_polygon(spec, 0.0)
	if normalized_points.size() < 3 or not _finite_points(normalized_points):
		_rejected_layers += 1
		return
	var role := String(spec.get("role", "water"))
	var root := Node2D.new()
	root.name = "WaterLayer_%s_%02d" % [_safe_node_name(role), _layers.size()]
	root.z_as_relative = true
	var render_priority := int(spec.get("render_priority",
		roundi(float(spec.get("z_offset", 0.0)) * 1000.0)))
	root.z_index = clampi(render_priority, RenderingServer.CANVAS_ITEM_Z_MIN,
		RenderingServer.CANVAS_ITEM_Z_MAX)
	var polygon := Polygon2D.new()
	polygon.name = "Fill"
	var line := Line2D.new()
	line.name = "Edge"
	line.closed = true
	line.antialiased = false
	root.add_child(polygon)
	root.add_child(line)
	add_child(root)
	var layer: Dictionary = {
		"root": root,
		"polygon": polygon,
		"line": line,
		"spec": spec,
		"role": role,
		"shape": shape,
		"stream": bool(spec.get("stream", false))
			or role in ["stream", "waterfall_band"],
		"flow_start": clampf(float(spec.get("flow_start", 0.0)), 0.0,
			0.999),
		"active_frames": spec.get("active_frames", []),
		"render_priority": render_priority,
		"flow_amount": 0.0,
		"bounds_normalized": Rect2(),
		"outlet_normalized": Vector2(0.5, 0.5),
	}
	_layers.append(layer)
	_set_layer_geometry(layer, normalized_points)
	root.set_meta("castle_fixture_water_2d", true)
	root.set_meta("water_role", role)
	root.set_meta("water_shape", shape)
	root.set_meta("bounded_to_fixture", true)
	root.set_meta("logic_authority", false)
	root.visible = false


func _apply_layer(layer: Dictionary, timeline_t: float) -> void:
	var spec: Dictionary = layer.get("spec", {}) as Dictionary
	var points := _layer_polygon(spec, timeline_t)
	if points.size() >= 3 and _finite_points(points):
		_set_layer_geometry(layer, points)
	var role := String(layer.get("role", "water"))
	var amount := _sample_profile(_profile_for_layer(spec, role), timeline_t)
	var flow_start := float(layer.get("flow_start", 0.0))
	amount = clampf((amount - flow_start) / maxf(0.001, 1.0 - flow_start),
		0.0, 1.0)
	if not _frame_is_active(layer.get("active_frames", []) as Array,
		_atlas_frame):
		amount = 0.0
	if role == "ripple":
		amount = minf(1.0, amount * 1.15)
	var root: Node2D = layer.get("root") as Node2D
	var polygon: Polygon2D = layer.get("polygon") as Polygon2D
	var line: Line2D = layer.get("line") as Line2D
	if root == null or polygon == null or line == null:
		return
	var deep := _color_from_spec(spec, "deep", DEFAULT_DEEP_COLOR)
	var shallow := _color_from_spec(spec, "shallow", DEFAULT_SHALLOW_COLOR)
	var alpha_base := clampf(float(spec.get("alpha_base", 0.84)), 0.0, 1.0)
	var fill_color := deep.lerp(shallow, clampf(amount, 0.0, 1.0))
	fill_color.a = alpha_base * amount
	polygon.color = fill_color
	var edge_foam := clampf(float(spec.get("edge_foam", 0.35)), 0.0, 1.0)
	line.default_color = Color(shallow.r, shallow.g, shallow.b,
		fill_color.a * clampf(0.35 + edge_foam, 0.0, 1.0))
	line.width = maxf(1.0, minf(_frame_size.x, _frame_size.y)
		* (0.003 + edge_foam * 0.012))
	if bool(layer.get("stream", false)):
		root.scale = Vector2(1.0, maxf(0.02, amount))
	elif role in ["fill", "basin", "cup_fill", "ripple"]:
		root.scale = Vector2(lerpf(0.72, 1.0, amount),
			lerpf(0.24, 1.0, amount))
	else:
		root.scale = Vector2.ONE
	root.visible = amount > MIN_VISIBLE_AMOUNT
	if root.visible:
		_active_layers += 1
	layer["flow_amount"] = amount
	root.set_meta("fixture_timeline_step", _timeline_step)
	root.set_meta("fixture_timeline_count", _timeline_count)
	root.set_meta("fixture_water_atlas_frame", _atlas_frame)
	root.set_meta("fixture_water_active", root.visible)
	root.set_meta("flow_amount", amount)
	root.set_meta("vortex_amount", _vortex_amount if role == "vortex" else 0.0)


func _set_layer_geometry(layer: Dictionary,
		normalized_points: PackedVector2Array) -> void:
	var root: Node2D = layer.get("root") as Node2D
	var polygon: Polygon2D = layer.get("polygon") as Polygon2D
	var line: Line2D = layer.get("line") as Line2D
	if root == null or polygon == null or line == null:
		return
	var spec: Dictionary = layer.get("spec", {}) as Dictionary
	var pivot := _layer_outlet(spec, normalized_points)
	var local_points := PackedVector2Array()
	for point: Vector2 in normalized_points:
		local_points.append((point - pivot) * _frame_size)
	root.position = _frame_origin + pivot * _frame_size
	polygon.polygon = local_points
	line.points = local_points
	var bounds := _polygon_bounds(normalized_points)
	layer["bounds_normalized"] = bounds
	layer["outlet_normalized"] = pivot
	root.set_meta("fixture_bounds_normalized", bounds)
	root.set_meta("fixture_outlet_normalized", pivot)


func _layer_polygon(spec: Dictionary, timeline_t: float) \
		-> PackedVector2Array:
	var points := PackedVector2Array()
	if String(spec.get("shape", "")) == "ellipse":
		var center := _vector2(spec.get("center", []), Vector2(0.5, 0.5))
		var center_frames: Array = spec.get("center_frames", []) as Array
		if not center_frames.is_empty():
			center = _sample_vector_frames(center_frames, timeline_t, center)
		var radius := _vector2(spec.get("radius", []), Vector2(0.2, 0.08))
		var radius_frames: Array = spec.get("radius_frames", []) as Array
		if not radius_frames.is_empty():
			radius = _sample_vector_frames(radius_frames, timeline_t, radius)
		for step in range(ELLIPSE_SEGMENTS):
			var angle := TAU * float(step) / float(ELLIPSE_SEGMENTS)
			points.append(center + Vector2(cos(angle) * radius.x,
				sin(angle) * radius.y))
		return points
	var raw_points: Array = spec.get("points", []) as Array
	var points_frames: Array = spec.get("points_frames", []) as Array
	if not points_frames.is_empty():
		var frame_index := clampi(_atlas_frame, 0, points_frames.size() - 1)
		raw_points = points_frames[frame_index] as Array
	for point_value: Variant in raw_points:
		points.append(_vector2(point_value, Vector2.ZERO))
	return points


func _layer_outlet(spec: Dictionary,
		normalized_points: PackedVector2Array) -> Vector2:
	var outlet_bounds: Array = spec.get("outlet_bounds_normalized", []) as Array
	if outlet_bounds.size() >= 4:
		return Vector2(float(outlet_bounds[0]) + float(outlet_bounds[2]) * 0.5,
			float(outlet_bounds[1]) + float(outlet_bounds[3]) * 0.5)
	if String(spec.get("shape", "")) == "ellipse":
		return _polygon_bounds(normalized_points).get_center()
	if normalized_points.size() >= 2:
		return (normalized_points[0] + normalized_points[1]) * 0.5
	return Vector2(0.5, 0.5)


func _profile_for_layer(spec: Dictionary, role: String) \
		-> PackedFloat32Array:
	for key: String in ["flow_profile", "profile"]:
		var profile := _packed_profile(spec.get(key, []))
		if not profile.is_empty():
			return profile
	if _profiles.has(role):
		var role_profile := _packed_profile(_profiles.get(role, []))
		if not role_profile.is_empty():
			return role_profile
	return _profile_for_role("vortex" if role == "vortex" else "flow")


func _profile_for_role(role: String) -> PackedFloat32Array:
	var profile := _packed_profile(_profiles.get(role, []))
	if not profile.is_empty():
		return profile
	return DEFAULT_VORTEX_PROFILE if role == "vortex" else DEFAULT_FLOW_PROFILE


func _packed_profile(value: Variant) -> PackedFloat32Array:
	if value is PackedFloat32Array:
		return value as PackedFloat32Array
	var result := PackedFloat32Array()
	if value is Array:
		for sample: Variant in value as Array:
			if typeof(sample) in [TYPE_INT, TYPE_FLOAT]:
				result.append(float(sample))
	return result


func _sample_profile(profile: PackedFloat32Array, timeline_t: float) -> float:
	if profile.is_empty():
		return 0.0
	var scaled := clampf(timeline_t, 0.0, 1.0) * float(profile.size() - 1)
	var left := clampi(int(floor(scaled)), 0, profile.size() - 1)
	var right := mini(left + 1, profile.size() - 1)
	return lerpf(profile[left], profile[right], scaled - float(left))


func _sample_vector_frames(frames: Array, timeline_t: float,
		fallback: Vector2) -> Vector2:
	if frames.is_empty():
		return fallback
	var scaled := clampf(timeline_t, 0.0, 1.0) * float(frames.size() - 1)
	var left := clampi(int(floor(scaled)), 0, frames.size() - 1)
	var right := mini(left + 1, frames.size() - 1)
	return _vector2(frames[left], fallback).lerp(
		_vector2(frames[right], fallback), scaled - float(left))


func _frame_is_active(active_frames: Array, atlas_frame: int) -> bool:
	if active_frames.is_empty():
		return true
	for frame_value: Variant in active_frames:
		if int(frame_value) == atlas_frame:
			return true
	return false


func _fixture_frame_size(sprite: Sprite2D) -> Vector2:
	if sprite.region_enabled and sprite.region_rect.size.x > 0.0 \
		and sprite.region_rect.size.y > 0.0:
		return sprite.region_rect.size
	if sprite.texture == null:
		return Vector2.ZERO
	return Vector2(sprite.texture.get_width() / float(maxi(1, sprite.hframes)),
		sprite.texture.get_height() / float(maxi(1, sprite.vframes)))


func _sync_to_fixture() -> void:
	if _fixture == null or not is_instance_valid(_fixture):
		return
	if get_parent() == _fixture:
		transform = Transform2D.IDENTITY
	elif get_parent() != null and get_parent() == _fixture.get_parent():
		transform = _fixture.transform


func _set_component_metadata(is_configured: bool) -> void:
	set_meta("castle_fixture_water_2d", true)
	set_meta("canvas_only", true)
	set_meta("configured", is_configured)
	set_meta("water_layer_count", _layers.size())
	set_meta("rejected_water_layer_count", _rejected_layers)
	set_meta("active_water_layer_count", _active_layers)
	set_meta("fixture_timeline_step", _timeline_step)
	set_meta("fixture_timeline_count", _timeline_count)
	set_meta("fixture_water_atlas_frame", _atlas_frame)
	if _fixture != null and is_instance_valid(_fixture):
		_fixture.set_meta("castle_fixture_water_2d", is_configured)
		_fixture.set_meta("fixture_water_layer_count", _layers.size())
		_fixture.set_meta("fixture_water_active", _active_layers > 0)
		_fixture.set_meta("fixture_water_atlas_frame", _atlas_frame)


func _clear_generated_layers() -> void:
	for layer: Dictionary in _layers:
		var root: Node2D = layer.get("root") as Node2D
		if root != null and is_instance_valid(root):
			root.free()
	_layers.clear()


func _role_names() -> Array[String]:
	var result: Array[String] = []
	for layer: Dictionary in _layers:
		var role := String(layer.get("role", "water"))
		if role not in result:
			result.append(role)
	return result


func _polygon_bounds(points: PackedVector2Array) -> Rect2:
	var minimum := Vector2(INF, INF)
	var maximum := Vector2(-INF, -INF)
	for point: Vector2 in points:
		minimum.x = minf(minimum.x, point.x)
		minimum.y = minf(minimum.y, point.y)
		maximum.x = maxf(maximum.x, point.x)
		maximum.y = maxf(maximum.y, point.y)
	return Rect2(minimum, maximum - minimum)


func _finite_points(points: PackedVector2Array) -> bool:
	for point: Vector2 in points:
		if not is_finite(point.x) or not is_finite(point.y):
			return false
	return true


func _color_from_spec(spec: Dictionary, key: String,
		fallback: Color) -> Color:
	var value: Variant = spec.get(key, fallback)
	if value is Color:
		return value as Color
	if value is String:
		return Color.from_string(String(value), fallback)
	if value is Array:
		var channels: Array = value as Array
		if channels.size() >= 3:
			return Color(float(channels[0]), float(channels[1]),
				float(channels[2]), float(channels[3])
				if channels.size() >= 4 else 1.0)
	return fallback


func _vector2(value: Variant, fallback: Vector2) -> Vector2:
	if value is Vector2:
		return value as Vector2
	if value is Array:
		var values: Array = value as Array
		if values.size() >= 2:
			return Vector2(float(values[0]), float(values[1]))
	return fallback


func _safe_node_name(value: String) -> String:
	var result := value.strip_edges().replace(" ", "_").replace("/", "_")
	return result if result != "" else "water"
