class_name CastleFixtureRigs
extends RefCounted

# Object-local mechanics for the Pearl Castle interaction pass. Authored state
# sheets animate the real fixture. This helper adds only manifest-measured fluid
# emitted from the real outlet/cavity and capped analytic spring motion for
# appropriate solids. Objective and menu logic never depend on spring settling.

const V2_BASE_MANIFEST_PATH := \
	"res://assets/flats/castle/interactions_v2/castle_interactions_v2.json"
const MANIFEST_PATH := "res://assets/flats/castle/interactions_v4/castle_interactions_v4.json"
const NATIVE_V4_TILE_ROOT := \
	"res://assets/flats/castle/interactions_v4/background_tiles/"
const NATIVE_V4_TILE_MANIFEST_ROOT := \
	"assets/flats/castle/interactions_v4/background_tiles"
const V2_BASE_PACK := "v2_base"
const NATIVE_V4_PACK := "v4_native"
const NATIVE_V4_BEHAVIOR_MODE := "authored_object_states"
const NATIVE_V4_BACKGROUND_ROUTE := \
	"generated_full_frame_pixel_ownership_tiles"
const RETIRED_V2_ASSET_IDS: Array[String] = [
	"main_hall_sconce",
	"main_hall_tapestry",
]
const WATER_SHADER := preload("res://assets/shaders/castle_fixture_water.gdshader")
const RIPPLE_TEXTURE := preload("res://assets/terrain/up_water_nrm.jpg")
const CAUSTICS_TEXTURE := preload("res://assets/terrain/caustics.png")
const MAX_SPRING_BODIES := 12
const MAX_AWAKE_SPRINGS := 8
const WATER_MASK_SIZE := 96
const HINGE_TORQUE_IMPULSE := 0.0045
const BUOYANT_VERTICAL_IMPULSE := 0.045
const BUOYANT_TORQUE_IMPULSE := 0.0018
const MAX_HINGE_ANGLE := 0.21
const MAX_BUOYANT_ANGLE := 0.12
const MAX_HINGE_DISPLACEMENT := 0.35
const MAX_BUOYANT_DISPLACEMENT := 0.06
const SPRING_SETTLE_GRACE_TICKS := 6
const SPRING_FORCE_SETTLE_TICKS := 300
const SPRING_ANGULAR_STIFFNESS := 18.0
const SPRING_ANGULAR_DAMPING := 7.5
const SPRING_LINEAR_STIFFNESS := 7.0
const SPRING_LINEAR_DAMPING := 2.2
const SPRING_HINGE_INITIAL_VELOCITY := 1.08
const SPRING_BUOYANT_INITIAL_ANGULAR_VELOCITY := 0.72
const SPRING_BUOYANT_INITIAL_VERTICAL_VELOCITY := 0.45
const WORLD_TO_CANVAS_PIXELS := 64.0

var _flow_profile: PackedFloat32Array = PackedFloat32Array([
	0.0, 0.18, 0.62, 1.0, 1.0, 0.68, 0.20, 0.0,
])
var _vortex_profile: PackedFloat32Array = PackedFloat32Array([
	0.0, 0.08, 0.52, 1.18, 1.72, 0.86, 0.24, 0.0,
])

var m: ReefMain
var _water_mask_cache: Dictionary = {}
var _native_items_by_room: Dictionary = {}
var _declared_native_source_items: Dictionary = {}
var _native_background_tile_roots: Dictionary = {}
var _native_background_tile_specs: Dictionary = {}
var _active_native_background_rooms: Dictionary = {}
var _spring_rigs: Dictionary = {}


func _init(main: ReefMain) -> void:
	m = main


func visual_spec(room_id: String, item_id: String) -> Dictionary:
	_ensure_manifest()
	var spec: Dictionary = m.castle_room_fixture_manifest.get(
		room_id + ":" + item_id, {}) as Dictionary
	if String(spec.get("pack", "")) == NATIVE_V4_PACK \
			and not _active_native_background_rooms.has(room_id):
		return {}
	return spec.duplicate(true)


func room_native_items(room_id: String) -> Array:
	_ensure_manifest()
	if not _active_native_background_rooms.has(room_id):
		return []
	return (_native_items_by_room.get(room_id, []) as Array).duplicate(true)


func native_source_item_uses_fallback_paint(
		room_id: String, item_id: String) -> bool:
	_ensure_manifest()
	return _declared_native_source_items.has(room_id + ":" + item_id) \
		and not _active_native_background_rooms.has(room_id)


func room_background_tile_root(room_id: String) -> String:
	_ensure_manifest()
	return String(_native_background_tile_roots.get(room_id, ""))


func room_background_tile_textures(room_id: String, columns: int, rows: int,
		expected_dimensions: Vector2i) -> Array[Texture2D]:
	_ensure_manifest()
	# A native route is active only after every tile has decoded at the exact
	# dimensions declared by the room. Never expose a partial set: source-owned
	# object cards are unsafe over a fallback background that still owns them.
	_active_native_background_rooms.erase(room_id)
	var textures: Array[Texture2D] = []
	var tile_root := String(_native_background_tile_roots.get(room_id, ""))
	var route_spec: Dictionary = _native_background_tile_specs.get(
		room_id, {}) as Dictionary
	var route_dimensions: Vector2i = route_spec.get(
		"tile_dimensions", Vector2i.ZERO)
	if tile_root == "" or columns <= 0 or rows <= 0 \
			or expected_dimensions.x <= 0 or expected_dimensions.y <= 0 \
			or columns != int(route_spec.get("columns", 0)) \
			or rows != int(route_spec.get("rows", 0)) \
			or expected_dimensions != route_dimensions:
		return textures
	for row in range(rows):
		for column in range(columns):
			var file_name := "room_%s_background_r%d_c%d.png" % [
				room_id, row, column]
			var path := tile_root + file_name
			if not ResourceLoader.exists(path):
				return []
			var texture: Texture2D = load(path) as Texture2D
			if texture == null or Vector2i(
					texture.get_width(), texture.get_height()) \
					!= expected_dimensions:
				return []
			textures.append(texture)
	if textures.size() != columns * rows:
		return []
	_active_native_background_rooms[room_id] = true
	return textures


func _ensure_manifest() -> void:
	if not m.castle_room_fixture_manifest.is_empty():
		return
	var index: Dictionary = {}
	var native_items: Dictionary = {}
	var declared_native_source_items: Dictionary = {}
	var native_entries_by_room: Dictionary = {}
	var accepted_assets: Array = []
	var rejected_native_v4 := 0
	for entry_value: Variant in _manifest_assets(V2_BASE_MANIFEST_PATH):
		var raw_entry: Dictionary = entry_value as Dictionary
		var declared_pack: String = String(raw_entry.get("pack", ""))
		if declared_pack != "" and declared_pack != V2_BASE_PACK:
			continue
		var entry := raw_entry.duplicate(true)
		entry["pack"] = V2_BASE_PACK
		if String(entry.get("id", "")) in RETIRED_V2_ASSET_IDS:
			continue
		_index_entry(index, entry)
		accepted_assets.append(entry)
	var native_manifest := _manifest_data(MANIFEST_PATH)
	var native_manifest_assets: Array = native_manifest.get("assets", []) as Array
	var declared_native_counts: Dictionary = {}
	for entry_value: Variant in native_manifest_assets:
		var raw_entry: Dictionary = entry_value as Dictionary
		var declared_room_id: String = String(raw_entry.get("room", ""))
		if declared_room_id != "":
			declared_native_counts[declared_room_id] = int(
				declared_native_counts.get(declared_room_id, 0)) + 1
		if String(raw_entry.get("pack", "")) == NATIVE_V4_PACK \
				and declared_room_id != "":
			for instance_value: Variant in raw_entry.get("instances", []):
				var declared_item_id := String(instance_value)
				if declared_item_id != "":
					declared_native_source_items[
						declared_room_id + ":" + declared_item_id] = true
		if not _valid_native_v4_entry(raw_entry):
			rejected_native_v4 += 1
			continue
		var entry := _normalized_native_v4_entry(raw_entry)
		var room_id: String = String(entry.get("room", ""))
		var room_entries: Array = native_entries_by_room.get(room_id, []) as Array
		room_entries.append(entry)
		native_entries_by_room[room_id] = room_entries
	var native_background_roots := _validated_native_background_tile_roots(
		native_manifest, declared_native_counts, native_entries_by_room)
	for room_id_value: Variant in native_entries_by_room:
		var room_id := String(room_id_value)
		var room_entries: Array = native_entries_by_room.get(room_id, []) as Array
		# A source-owned card is safe only with the matching complete full-frame
		# clean room route. Gate the whole room so a partial delivery can neither erase a
		# pending fixture nor draw an animated card over its baked original.
		if not native_background_roots.has(room_id):
			rejected_native_v4 += room_entries.size()
			continue
		for entry_value: Variant in room_entries:
			var entry: Dictionary = entry_value as Dictionary
			_index_entry(index, entry)
			accepted_assets.append(entry)
			for instance_value: Variant in entry.get("instances", []):
				var item_id: String = String(instance_value)
				var room_items: Array = native_items.get(room_id, []) as Array
				room_items.append(_native_runtime_item(entry, item_id))
				native_items[room_id] = room_items
	m.castle_room_fixture_manifest = index
	_native_items_by_room = native_items
	_declared_native_source_items = declared_native_source_items
	_native_background_tile_roots = native_background_roots
	m.g["castle_fixture_native_v4_loaded"] = _native_item_count(native_items)
	m.g["castle_fixture_native_v4_rejected"] = rejected_native_v4
	m.g["castle_fixture_native_v4_background_rooms"] = \
		native_background_roots.size()
	_prewarm_water_masks(accepted_assets)


func _manifest_assets(path: String) -> Array:
	return _manifest_data(path).get("assets", []) as Array


func _manifest_data(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary:
		return {}
	return parsed as Dictionary


func _validated_native_background_tile_roots(manifest: Dictionary,
		declared_counts: Dictionary, valid_entries_by_room: Dictionary
		) -> Dictionary:
	var validated: Dictionary = {}
	_native_background_tile_specs.clear()
	var routes: Dictionary = manifest.get(
		"runtime_background_tiles", {}) as Dictionary
	for room_id_value: Variant in routes:
		var room_id := String(room_id_value)
		var declared_count := int(declared_counts.get(room_id, 0))
		var valid_entries: Array = valid_entries_by_room.get(room_id, []) as Array
		if declared_count <= 0 or valid_entries.size() != declared_count:
			continue
		var route: Dictionary = routes.get(room_id, {}) as Dictionary
		if String(route.get("route", "")) != NATIVE_V4_BACKGROUND_ROUTE \
				or bool(route.get(
					"derived_from_low_resolution_audit_plate", true)) \
				or String(route.get("source_tile_root", "")) \
					!= "assets/flats/castle/rooms/background_tiles" \
				or String(route.get("runtime_tile_root", "")) \
				!= NATIVE_V4_TILE_MANIFEST_ROOT:
			continue
		var grid: Array = route.get("grid", []) as Array
		if grid.size() != 2:
			continue
		var columns := int(grid[0])
		var rows := int(grid[1])
		if columns <= 0 or rows <= 0:
			continue
		var dimensions: Array = route.get("tile_dimensions", []) as Array
		if dimensions.size() != 2 or int(dimensions[0]) <= 0 \
				or int(dimensions[1]) <= 0 or int(dimensions[0]) > 1024 \
				or int(dimensions[1]) > 1024:
			continue
		var native_canvas: Array = route.get("native_canvas_size", []) as Array
		if native_canvas.size() != 2 \
				or int(native_canvas[0]) != columns * int(dimensions[0]) \
				or int(native_canvas[1]) != rows * int(dimensions[1]):
			continue
		var tiles: Array = route.get("tiles", []) as Array
		if tiles.size() != columns * rows:
			continue
		var all_tiles_ready := true
		for row in range(rows):
			for column in range(columns):
				var tile_index := row * columns + column
				var tile: Dictionary = tiles[tile_index] as Dictionary
				var file_name := "room_%s_background_r%d_c%d.png" % [
					room_id, row, column]
				var expected_path := NATIVE_V4_TILE_MANIFEST_ROOT \
					+ "/" + file_name
				if String(tile.get("path", "")) != expected_path \
						or not bool(tile.get("opaque", false)) \
						or not ResourceLoader.exists("res://" + expected_path):
					all_tiles_ready = false
					break
			if not all_tiles_ready:
				break
		if all_tiles_ready:
			validated[room_id] = NATIVE_V4_TILE_ROOT
			_native_background_tile_specs[room_id] = {
				"columns": columns,
				"rows": rows,
				"tile_dimensions": Vector2i(
					int(dimensions[0]), int(dimensions[1])),
			}
	return validated


func _index_entry(index: Dictionary, entry: Dictionary) -> void:
	var room_id: String = String(entry.get("room", ""))
	if room_id == "":
		return
	for instance_value: Variant in entry.get("instances", []):
		var item_id: String = String(instance_value)
		if item_id != "":
			index[room_id + ":" + item_id] = entry


func _valid_native_v4_entry(entry: Dictionary) -> bool:
	if String(entry.get("pack", "")) != NATIVE_V4_PACK:
		return false
	var room_id: String = String(entry.get("room", ""))
	var instances: Array = entry.get("instances", []) as Array
	var semantic_action: String = String(entry.get("semantic_action", ""))
	if room_id == "" or instances.size() != 1 or semantic_action == "":
		return false
	for instance_value: Variant in instances:
		if String(instance_value) == "":
			return false
	var ownership: Dictionary = entry.get("source_ownership", {}) as Dictionary
	if not bool(ownership.get("passed", false)) \
			or not bool(ownership.get("verified", false)) \
			or not bool(ownership.get("background_healed", false)) \
			or not bool(ownership.get("duplicate_pixels_removed", false)):
		return false
	var source_rect: Array = ownership.get("source_rect", []) as Array
	if not _valid_source_rect(source_rect, room_id):
		return false
	var behavior: Dictionary = entry.get("animation_behavior", {}) as Dictionary
	if String(behavior.get("mode", "")) != NATIVE_V4_BEHAVIOR_MODE \
			or String(behavior.get("action", "")) != semantic_action \
			or bool(behavior.get("generic_transform_fallback", true)):
		return false
	var physics_mode: String = String(entry.get("physics_mode", "none"))
	if physics_mode != "none":
		if physics_mode not in ["hinge_z", "buoyant"] \
				or not bool(behavior.get("secondary_physics", false)) \
				or String(behavior.get("physics_role", "")) == "":
			return false
	if String(entry.get("render_mode", "")) \
			!= "generated_full_object_states" \
			or bool(entry.get("primary_animation_is_overlay", true)):
		return false
	var frame_count := int(entry.get("authored_frame_count",
		entry.get("frame_count", 0)))
	if frame_count < 4 or frame_count > 12:
		return false
	var rest_frame := int(entry.get("rest_frame", 0))
	if rest_frame < 0 or rest_frame >= frame_count:
		return false
	var grid: Array = entry.get("grid", []) as Array
	if grid.size() < 2 or int(grid[0]) <= 0 or int(grid[1]) <= 0 \
			or int(grid[0]) * int(grid[1]) < frame_count:
		return false
	var timeline: Array = entry.get("timeline_sequence", []) as Array
	if timeline.size() < 4 or timeline.size() > 12:
		return false
	if entry.has("timeline_frame_count") \
			and int(entry.get("timeline_frame_count", 0)) != timeline.size():
		return false
	for frame_value: Variant in timeline:
		var frame_index := int(frame_value)
		if frame_index < 0 or frame_index >= frame_count:
			return false
	var sheet_path: String = String(entry.get("sheet", ""))
	if sheet_path == "" or not ResourceLoader.exists("res://" + sheet_path):
		return false
	return true


func _valid_source_rect(source_rect: Array, room_id: String) -> bool:
	if source_rect.size() < 4:
		return false
	for value_index in range(4):
		if typeof(source_rect[value_index]) not in [TYPE_INT, TYPE_FLOAT]:
			return false
	var rect := Rect2(float(source_rect[0]), float(source_rect[1]),
		float(source_rect[2]), float(source_rect[3]))
	var room_size := Vector2(3344.0, 941.0) \
		if room_id == "main_hall" else Vector2(1024.0, 576.0)
	return rect.position.x >= 0.0 and rect.position.y >= 0.0 \
		and rect.size.x > 0.0 and rect.size.y > 0.0 \
		and rect.end.x <= room_size.x and rect.end.y <= room_size.y


func _normalized_native_v4_entry(entry: Dictionary) -> Dictionary:
	var normalized := entry.duplicate(true)
	var ownership: Dictionary = normalized.get(
		"source_ownership", {}) as Dictionary
	var source_rect: Array = ownership.get("source_rect", []) as Array
	normalized["placement_position"] = [
		float(source_rect[0]), float(source_rect[1])]
	normalized["placement_size"] = [
		float(source_rect[2]), float(source_rect[3])]
	return normalized


func _native_item_count(items_by_room: Dictionary) -> int:
	var count := 0
	for room_items_value: Variant in items_by_room.values():
		count += (room_items_value as Array).size()
	return count


func _native_runtime_item(entry: Dictionary, item_id: String) -> Dictionary:
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
		"source_owned_native": true,
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


func build(interaction_key: String, piece: Node, item_data: Dictionary,
		source_position: Vector2, placement_size: Vector2, depth_z: float,
		to_world: Callable) -> Dictionary:
	var visual: Dictionary = item_data.get("v2_visual", {}) as Dictionary
	if visual.is_empty() or piece == null:
		return {}
	var visual_pack: String = String(visual.get("pack", ""))
	var behavior: Dictionary = visual.get("animation_behavior", {}) as Dictionary
	var rig: Dictionary = {
		"key": interaction_key,
		"sprite": piece,
		"visual": visual,
		"water": [],
		"body": null,
		"spring": null,
		"physics_mode": String(visual.get("physics_mode", "none")),
		"base_sprite_position": _node_position(piece),
		"base_sprite_rotation": _node_rotation(piece),
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
	piece.set_meta("castle_component_rig_v2", visual_pack == V2_BASE_PACK)
	piece.set_meta("castle_component_rig_v4", visual_pack == NATIVE_V4_PACK)
	piece.set_meta("native_authored_object_states",
		visual_pack == NATIVE_V4_PACK
		and String(behavior.get("mode", "")) == NATIVE_V4_BEHAVIOR_MODE)
	piece.set_meta("primary_animation_is_overlay",
		bool(visual.get("primary_animation_is_overlay", false)))
	piece.set_meta("generated_full_object_states",
		String(visual.get("render_mode", "")) == "generated_full_object_states")
	piece.set_meta("fixture_water_shader", WATER_SHADER.resource_path)
	piece.set_meta("fixture_water_ripple_texture", RIPPLE_TEXTURE.resource_path)
	piece.set_meta("fixture_water_caustics_texture", CAUSTICS_TEXTURE.resource_path)
	var water_layers: Array = visual.get("water_layers", []) as Array
	_add_water_layers(rig, water_layers, source_position, placement_size,
		depth_z, to_world)
	_add_spring_driver(rig, source_position, placement_size, depth_z, to_world)
	m.castle_room_fixture_rigs[interaction_key] = rig
	return rig


func activate(interaction_key: String) -> void:
	var rig: Dictionary = m.castle_room_fixture_rigs.get(
		interaction_key, {}) as Dictionary
	if rig.is_empty():
		return
	var spring := _spring_record(rig)
	if spring.is_empty():
		return
	var already_awake := String(spring.get("phase", "idle")) != "idle"
	if not already_awake and _awake_count() >= MAX_AWAKE_SPRINGS:
		return
	rig["peak_angle_radians"] = 0.0
	rig["peak_displacement"] = 0.0
	var direction := -1.0 if abs(interaction_key.hash()) % 2 == 0 else 1.0
	spring["direction"] = direction
	spring["phase"] = "wake"
	spring["active_ticks"] = 0
	var mode := String(rig.get("physics_mode", "none"))
	spring["angle_velocity"] = direction * (
		SPRING_HINGE_INITIAL_VELOCITY if mode == "hinge_z"
		else SPRING_BUOYANT_INITIAL_ANGULAR_VELOCITY)
	spring["vertical_velocity"] = direction * (
		SPRING_BUOYANT_INITIAL_VERTICAL_VELOCITY if mode == "buoyant" else 0.0)
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
		var node: Sprite2D = water.get("node") as Sprite2D
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
	var sprite: Node = rig.get("sprite") as Node
	if sprite != null:
		sprite.set_meta("fixture_timeline_frame", timeline_step)
		sprite.set_meta("fixture_timeline_frame_count", timeline_count)
		sprite.set_meta("fixture_water_atlas_frame", water_frame_index)
		sprite.set_meta("fixture_water_active", any_water_active)


func tick(_delta: float) -> void:
	var awake := _awake_count()
	m.g["castle_fixture_spring_allocated"] = _spring_rigs.size()
	m.g["castle_fixture_spring_awake"] = awake
	# Compatibility telemetry for older callers; these are analytic springs now.
	m.g["castle_fixture_jolt_allocated"] = _spring_rigs.size()
	m.g["castle_fixture_jolt_awake"] = awake
	for rig_value: Variant in m.castle_room_fixture_rigs.values():
		_tick_bubbles(rig_value as Dictionary)


func physics_tick(_delta: float) -> void:
	for rig_value: Variant in m.castle_room_fixture_rigs.values():
		_tick_spring(rig_value as Dictionary, _delta)


func stats() -> Dictionary:
	return {
		"rigs": m.castle_room_fixture_rigs.size(),
		"allocated": _spring_rigs.size(),
		"awake": _awake_count(),
		"body_cap": MAX_SPRING_BODIES,
		"awake_cap": MAX_AWAKE_SPRINGS,
		"spring_cap": MAX_SPRING_BODIES,
		"spring_awake_cap": MAX_AWAKE_SPRINGS,
		"water_mask_cache_entries": _water_mask_cache.size(),
		"native_v4_loaded": int(m.g.get(
			"castle_fixture_native_v4_loaded", 0)),
		"native_v4_rejected": int(m.g.get(
			"castle_fixture_native_v4_rejected", 0)),
		"native_v4_background_rooms": int(m.g.get(
			"castle_fixture_native_v4_background_rooms", 0)),
	}


func teardown() -> void:
	for rig_value: Variant in m.castle_room_fixture_rigs.values():
		var rig: Dictionary = rig_value as Dictionary
		for water_value: Variant in rig.get("water", []):
			var water: Dictionary = water_value as Dictionary
			var node: Sprite2D = water.get("node") as Sprite2D
			if node != null and is_instance_valid(node):
				node.visible = false
				if node.get_parent() != null:
					node.get_parent().remove_child(node)
				node.free()
	_spring_rigs.clear()
	m.castle_room_fixture_rigs.clear()
	m.g.erase("castle_fixture_spring_allocated")
	m.g.erase("castle_fixture_spring_awake")
	m.g.erase("castle_fixture_jolt_allocated")
	m.g.erase("castle_fixture_jolt_awake")


func _add_water_layers(rig: Dictionary, layers: Array,
		source_position: Vector2, placement_size: Vector2, depth_z: float,
		to_world: Callable) -> void:
	if m.castle_room_item_visual_layer == null:
		return
	for layer_value: Variant in layers:
		var layer: Dictionary = layer_value as Dictionary
		# The authored bathtub already carries its faucet hardware and stream
		# contact in the complete source-owned atlas. The old quad stream added a
		# conspicuous rectangular cyan strip on Mobile, so keep the basin water
		# only and preserve the interaction/timeline unchanged.
		if String(rig.get("key", "")) == "bubble_bath:bathtub" \
				and String(layer.get("role", "")) == "stream":
			continue
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
	var center_canvas := _canvas_point(to_world.call(center_art, depth_z + z_offset))
	var left_canvas := _canvas_point(to_world.call(Vector2(
		source_position.x + bounds.position.x * placement_size.x,
		center_art.y), depth_z + z_offset))
	var right_canvas := _canvas_point(to_world.call(Vector2(
		source_position.x + bounds.end.x * placement_size.x,
		center_art.y), depth_z + z_offset))
	var top_canvas := _canvas_point(to_world.call(Vector2(center_art.x,
		source_position.y + bounds.position.y * placement_size.y),
		depth_z + z_offset))
	var bottom_canvas := _canvas_point(to_world.call(Vector2(center_art.x,
		source_position.y + bounds.end.y * placement_size.y),
		depth_z + z_offset))
	var node := Sprite2D.new()
	node.name = "FixtureWater_" + String(layer.get("role", "water"))
	node.texture = mask_texture
	node.centered = true
	node.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	node.scale = Vector2(
		absf(right_canvas.x - left_canvas.x) / float(WATER_MASK_SIZE),
		absf(bottom_canvas.y - top_canvas.y) / float(WATER_MASK_SIZE))
	node.position = center_canvas
	node.z_index = int(round((depth_z + z_offset) * 100.0))
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
	var alpha_base := float(layer.get("alpha_base", 0.84))
	if String(rig.get("key", "")) == "bubble_bath:bathtub" \
			and role == "fill":
		alpha_base = minf(alpha_base, 0.24)
	material.set_shader_parameter("alpha_base", alpha_base)
	material.set_shader_parameter("turbulence",
		float(layer.get("turbulence", 0.65)))
	material.set_shader_parameter("edge_foam",
		float(layer.get("edge_foam", 0.35)))
	material.set_shader_parameter("flow_speed",
		float(layer.get("flow_speed", 1.0)))
	material.render_priority = int(layer.get("render_priority", 1))
	node.material = material
	node.visible = false
	node.set_meta("castle_fixture_water", true)
	node.set_meta("water_role", role)
	node.set_meta("bounded_to_fixture", true)
	node.set_meta("sprite_masked_water", true)
	node.set_meta("depth_write_disabled", true)
	node.set_meta("logic_authority", false)
	node.set_meta("fixture_bounds_normalized", bounds)
	node.set_meta("fixture_outlet_normalized", _layer_outlet(geometry_layer))
	node.set_meta("fixture_z_offset", z_offset)
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
		"z_offset": z_offset,
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
	var node: Sprite2D = water.get("node") as Sprite2D
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
	var depth_z: float = float(water.get("depth_z", 0.0))
	var to_world: Callable = water.get("to_world") as Callable
	var center_normalized := bounds.position + bounds.size * 0.5
	var center_art := source_position + center_normalized * placement_size
	var center_canvas := _canvas_point(to_world.call(center_art, depth_z))
	var left_canvas := _canvas_point(to_world.call(Vector2(
		source_position.x + bounds.position.x * placement_size.x,
		center_art.y), depth_z))
	var right_canvas := _canvas_point(to_world.call(Vector2(
		source_position.x + bounds.end.x * placement_size.x,
		center_art.y), depth_z))
	var top_canvas := _canvas_point(to_world.call(Vector2(center_art.x,
		source_position.y + bounds.position.y * placement_size.y), depth_z))
	var bottom_canvas := _canvas_point(to_world.call(Vector2(center_art.x,
		source_position.y + bounds.end.y * placement_size.y), depth_z))
	node.position = center_canvas
	node.scale = Vector2(
		absf(right_canvas.x - left_canvas.x) / float(WATER_MASK_SIZE),
		absf(bottom_canvas.y - top_canvas.y) / float(WATER_MASK_SIZE))
	node.z_index = int(round(depth_z * 100.0))
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
	var depth_z: float = float(water.get("depth_z", 0.0))
	var art_position := source_position + center * placement_size
	var to_world: Callable = water.get("to_world") as Callable
	var node: Sprite2D = water.get("node") as Sprite2D
	if node == null:
		return
	node.position = _canvas_point(to_world.call(art_position, depth_z))
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


func _add_spring_driver(rig: Dictionary, source_position: Vector2,
		placement_size: Vector2, depth_z: float, to_world: Callable) -> void:
	var mode := String(rig.get("physics_mode", "none"))
	if mode == "none" or _spring_rigs.size() >= MAX_SPRING_BODIES:
		return
	var visual: Dictionary = rig.get("visual", {}) as Dictionary
	var pivot_array: Array = visual.get("physics_pivot", [0.5, 0.5]) as Array
	var pivot_normalized := Vector2(float(pivot_array[0]), float(pivot_array[1]))
	var sprite: Node = rig.get("sprite") as Node
	var rest_position := _node_position(sprite)
	var pivot_art := source_position + pivot_normalized * placement_size
	var pivot_position := _canvas_point(to_world.call(pivot_art, depth_z))
	var spring := {
		"phase": "idle", "active_ticks": 0, "direction": 1.0,
		"angle": 0.0, "angle_velocity": 0.0, "displacement": 0.0,
		"vertical_velocity": 0.0, "rest_position": rest_position,
		"pivot_offset": rest_position - pivot_position,
	}
	rig["spring"] = spring
	rig["rest_body_position"] = rest_position
	rig["pivot_offset"] = spring["pivot_offset"]
	rig["base_sprite_position"] = rest_position
	# The source interaction contract retains its legacy world displacement key.
	# Expose a Canvas-space cap per rig so probes can enforce containment without
	# mixing units. Buoyant rigs translate the legacy linear cap directly; hinge
	# rigs use the actual pivot arc at their configured maximum angle, while still
	# honoring the legacy cap when it is tighter.
	var legacy_canvas_cap := float(
		rig.get("max_displacement", 0.0)) * WORLD_TO_CANVAS_PIXELS
	if mode == "hinge_z":
		var pivot_offset: Vector2 = spring["pivot_offset"] as Vector2
		var max_angle := float(rig.get(
			"max_angle_radians", MAX_HINGE_ANGLE))
		var pivot_arc_canvas := 2.0 * pivot_offset.length() \
			* sin(max_angle * 0.5)
		rig["max_displacement_canvas"] = minf(
			pivot_arc_canvas, legacy_canvas_cap)
	else:
		rig["max_displacement_canvas"] = legacy_canvas_cap
	rig["jolt_direction"] = 1.0
	rig["jolt_phase"] = "idle"
	rig["jolt_active_ticks"] = 0
	_spring_rigs[String(rig.get("key", "fixture"))] = spring


func _tick_spring(rig: Dictionary, delta: float) -> void:
	var spring := _spring_record(rig)
	var sprite: Node = rig.get("sprite") as Node
	if spring.is_empty() or sprite == null:
		return
	var phase := String(spring.get("phase", "idle"))
	if phase == "idle":
		return
	if phase == "wake":
		spring["phase"] = "kick"
		rig["jolt_phase"] = "kick"
		return
	if phase == "kick":
		spring["phase"] = "observe"
		rig["jolt_phase"] = "observe"
		spring["active_ticks"] = 0
		return
	var step := clampf(delta, 0.001, 0.05)
	var active_ticks := int(spring.get("active_ticks", 0)) + 1
	spring["active_ticks"] = active_ticks
	var mode := String(rig.get("physics_mode", "none"))
	var angle := float(spring.get("angle", 0.0))
	var angle_velocity := float(spring.get("angle_velocity", 0.0))
	var displacement := float(spring.get("displacement", 0.0))
	var vertical_velocity := float(spring.get("vertical_velocity", 0.0))
	angle_velocity += (-angle * SPRING_ANGULAR_STIFFNESS
		- angle_velocity * SPRING_ANGULAR_DAMPING) * step
	angle += angle_velocity * step
	var max_angle := float(rig.get("max_angle_radians", MAX_BUOYANT_ANGLE))
	if mode == "hinge_z":
		var pivot_offset: Vector2 = spring.get(
			"pivot_offset", Vector2.ZERO) as Vector2
		var pivot_radius := pivot_offset.length()
		var displacement_cap := float(rig.get(
			"max_displacement_canvas", 0.0))
		if pivot_radius > displacement_cap * 0.5 and displacement_cap > 0.001:
			var displacement_ratio := clampf(
				(displacement_cap - 0.001) / (2.0 * pivot_radius),
				0.0, 1.0)
			max_angle = minf(max_angle, 2.0 * asin(displacement_ratio))
	angle = clampf(angle, -max_angle, max_angle)
	if mode == "buoyant":
		var max_displacement := float(rig.get(
			"max_displacement", MAX_BUOYANT_DISPLACEMENT))
		vertical_velocity += (-displacement * SPRING_LINEAR_STIFFNESS
			- vertical_velocity * SPRING_LINEAR_DAMPING) * step
		displacement += vertical_velocity * step
		displacement = clampf(displacement, -max_displacement, max_displacement)
	else:
		displacement = 0.0
	spring["angle"] = angle
	spring["angle_velocity"] = angle_velocity
	spring["displacement"] = displacement
	spring["vertical_velocity"] = vertical_velocity
	_sync_spring_sprite(rig)
	var current_position := _node_position(sprite)
	var base_position: Vector2 = rig.get(
		"base_sprite_position", current_position) as Vector2
	rig["peak_angle_radians"] = maxf(
		float(rig.get("peak_angle_radians", 0.0)), absf(angle))
	rig["peak_displacement"] = maxf(
		float(rig.get("peak_displacement", 0.0)),
		current_position.distance_to(base_position))
	var settled := absf(angle) < 0.008 \
		and current_position.distance_to(base_position) < 0.008 \
		and absf(angle_velocity) < 0.012 and absf(vertical_velocity) < 0.012
	if active_ticks >= SPRING_FORCE_SETTLE_TICKS \
			or (active_ticks >= SPRING_SETTLE_GRACE_TICKS \
			and float(rig.get("peak_angle_radians", 0.0)) > 0.001 \
			and float(rig.get("peak_displacement", 0.0)) > 0.001
			and settled):
		_settle_spring(rig)


func _settle_spring(rig: Dictionary) -> void:
	var spring := _spring_record(rig)
	var sprite: Node = rig.get("sprite") as Node
	if spring.is_empty() or sprite == null:
		return
	_set_node_position(sprite,
		spring.get("rest_position", Vector2.ZERO) as Vector2)
	_set_node_rotation(sprite, float(rig.get("base_sprite_rotation", 0.0)))
	spring["phase"] = "idle"
	spring["active_ticks"] = 0
	spring["angle"] = 0.0
	spring["angle_velocity"] = 0.0
	spring["displacement"] = 0.0
	spring["vertical_velocity"] = 0.0
	rig["jolt_phase"] = "idle"
	rig["jolt_active_ticks"] = 0


func _tick_bubbles(rig: Dictionary) -> void:
	var now := float(Time.get_ticks_msec()) * 0.001
	for water_value: Variant in rig.get("water", []):
		var water: Dictionary = water_value as Dictionary
		if String(water.get("role", "")) != "bubble":
			continue
		var node: Sprite2D = water.get("node") as Sprite2D
		if node == null or not is_instance_valid(node):
			continue
		var base: Vector2 = water.get("base_position", Vector2.ZERO) as Vector2
		var index: int = int(water.get("bubble_index", 0))
		var amount: float = float(water.get("flow_amount", 0.0))
		node.position = base + Vector2(
			sin(now * 1.7 + float(index)) * 0.012
				* WORLD_TO_CANVAS_PIXELS * amount,
			fmod(now * (0.05 + float(index) * 0.009), 0.11)
				* WORLD_TO_CANVAS_PIXELS * amount)


func _awake_count() -> int:
	var awake := 0
	for value: Variant in _spring_rigs.values():
		var spring: Dictionary = value as Dictionary
		if String(spring.get("phase", "idle")) != "idle":
			awake += 1
	return awake


func _spring_record(rig: Dictionary) -> Dictionary:
	var value: Variant = rig.get("spring", null)
	return value as Dictionary if value is Dictionary else {}


func _sync_spring_sprite(rig: Dictionary) -> void:
	var spring := _spring_record(rig)
	var sprite: Node = rig.get("sprite") as Node
	if spring.is_empty() or sprite == null:
		return
	var angle := float(spring.get("angle", 0.0))
	var rest: Vector2 = spring.get("rest_position", Vector2.ZERO) as Vector2
	var offset: Vector2 = spring.get("pivot_offset", Vector2.ZERO) as Vector2
	if String(rig.get("physics_mode", "none")) == "hinge_z":
		_set_node_position(sprite, rest + offset.rotated(angle) - offset)
	else:
		_set_node_position(sprite, rest + Vector2(
			0.0, float(spring.get("displacement", 0.0))
				* WORLD_TO_CANVAS_PIXELS))
	_set_node_rotation(sprite,
		float(rig.get("base_sprite_rotation", 0.0)) + angle)


func _node_position(node: Node) -> Vector2:
	if node == null:
		return Vector2.ZERO
	var value: Variant = node.get("position")
	if value is Vector2:
		return value as Vector2
	if value == null:
		return Vector2.ZERO
	return Vector2(float(value.x), float(value.y))


func _canvas_point(value: Variant) -> Vector2:
	if value is Vector2:
		return value as Vector2
	if value == null:
		return Vector2.ZERO
	return Vector2(float(value.x), float(value.y))


func _set_node_position(node: Node, position: Vector2) -> void:
	if node == null:
		return
	var current: Variant = node.get("position")
	if current is Vector2:
		node.set("position", position)
		return
	if current == null:
		return
	current.x = position.x
	current.y = position.y
	node.set("position", current)


func _node_rotation(node: Node) -> float:
	if node == null:
		return 0.0
	var value: Variant = node.get("rotation")
	if value is float or value is int:
		return float(value)
	return float(value.z)


func _set_node_rotation(node: Node, angle: float) -> void:
	if node == null:
		return
	var current: Variant = node.get("rotation")
	if current is float or current is int:
		node.set("rotation", angle)
		return
	current.z = angle
	node.set("rotation", current)
