extends Node2D
## One actor, one Skeleton2D, one AnimationPlayer. Skins are strictly art/data.

const PREFIX: String = "assets_src/animation/roshan_shared_swim_20261101/"
const VIEW: String = "swim_right_quarter"
const PERIOD: float = 1.9
const SEQUENCE_SECONDS: float = 7.6

var skeleton: Skeleton2D
var player: AnimationPlayer
var bones: Dictionary = {}
var rest_world: Dictionary = {}
var anatomy_nodes: Dictionary = {}
var slot_nodes: Dictionary = {}
var textures: Dictionary = {}
var geometry_cache: Dictionary = {}
var prepared_skins: Dictionary = {}
var rest_data: Dictionary = {}
var rig: Dictionary = {}
var anatomy: Dictionary = {}
var catalog: Dictionary = {}
var rig_sha: String = ""
var skin_id: String = ""
var last_error: String = ""
var core_ready: bool = false
var paused: bool = false
var tail_motion_enabled: bool = true
var velocity: Vector2 = Vector2.ZERO
var thrust_acceleration: float = 0.0
var _previous_fin: Vector2 = Vector2.ZERO
var _have_fin_sample: bool = false
var _source_hashes: Dictionary = {}
var fin_state: String = "fin_broad":
	set(value):
		fin_state = value
		if core_ready:
			_show_fin(value)


func _ready() -> void:
	rig = _read_json("res://rig/rig_binding.json")
	rest_data = _read_json("res://rig/skeleton.json")
	anatomy = _read_json("res://rig/anatomy.json")
	catalog = _read_json("res://skins/catalog.json")
	rig_sha = FileAccess.get_sha256("res://rig/rig_binding.json")
	skeleton = Skeleton2D.new()
	skeleton.name = "Skeleton"
	add_child(skeleton)
	for item: Dictionary in rest_data["bones"]:
		var bone: Bone2D = Bone2D.new()
		var name_string: String = str(item["name"])
		bone.name = name_string
		bone.set_autocalculate_length_and_angle(false)
		var parent: Node2D = skeleton if item["parent"] == null else bones[str(item["parent"])]
		parent.add_child(bone)
		var head: Vector2 = _point(item["head"])
		var tail: Vector2 = _point(item["tail"])
		var parent_rest: Transform2D = Transform2D.IDENTITY if parent == skeleton else rest_world[str(item["parent"])]
		var world_rest: Transform2D = Transform2D((tail - head).angle(), head)
		bone.transform = parent_rest.affine_inverse() * world_rest
		bone.rest = bone.transform
		bone.set_length(head.distance_to(tail))
		bone.set_bone_angle(0.0)
		bones[name_string] = bone
		rest_world[name_string] = world_rest
	for reference: Dictionary in rig["identity_assets"]:
		assert(_checked_reference(reference) != "", "Canonical anatomy reference failed")
	for part: Dictionary in anatomy["parts"]:
		var name_string: String = str(part["id"])
		var payload: Dictionary = _prepare_attachment(part)
		assert(not payload.is_empty(), "Canonical anatomy could not load: " + last_error)
		anatomy_nodes[name_string] = {"payload": payload, "node": null}
		if name_string.begins_with("fin_"):
			continue
		var polygon: Polygon2D = _new_polygon(name_string, int(part["layer"]))
		_assign(polygon, payload)
		anatomy_nodes[name_string]["node"] = polygon
	var fin: Polygon2D = _new_polygon("SharedFin", 1)
	anatomy_nodes["fin_node"] = {"node": fin}
	var slots: Dictionary = rig["views"][VIEW]["slots"]
	for slot: String in slots:
		slot_nodes[slot] = _new_polygon("Slot_" + slot, int(slots[slot]["layer"]))
	for name_string: String in catalog["skins"]:
		var document: Dictionary = _read_json("res://" + str(catalog["skins"][name_string]))
		var payload: Dictionary = _prepare_skin(document)
		assert(not payload.is_empty(), "Skin preparation failed: " + last_error)
		prepared_skins[name_string] = payload
	player = AnimationPlayer.new()
	player.name = "AnimationPlayer"
	player.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	add_child(player)
	var library: AnimationLibrary = AnimationLibrary.new()
	library.add_animation("sequence", _build_animation(false))
	library.add_animation("cycle", _build_animation(true))
	player.add_animation_library("", library)
	core_ready = true
	_show_fin("fin_broad")
	assert(apply_skin("ballet"))
	player.play("sequence")
	player.seek(0.0, true)
	set_process(false)


func _read_json(path: String) -> Dictionary:
	var result: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return result if typeof(result) == TYPE_DICTIONARY else {}


func _fields(value: Variant, required: Array, optional: Array = []) -> bool:
	if typeof(value) != TYPE_DICTIONARY:
		return false
	for key: String in required:
		if not value.has(key):
			return false
	for key: Variant in value:
		if not required.has(key) and not optional.has(key):
			return false
	return true


func _number(value: Variant) -> bool:
	return (typeof(value) == TYPE_FLOAT or typeof(value) == TYPE_INT) and is_finite(float(value))


func _valid_point(value: Variant) -> bool:
	return typeof(value) == TYPE_ARRAY and value.size() == 2 and _number(value[0]) and _number(value[1])


func _point(value: Array) -> Vector2:
	return Vector2(float(value[0]), float(value[1]))


func _reject(reason: String) -> Dictionary:
	last_error = reason
	return {}


func _checked_reference(reference: Variant) -> String:
	if not _fields(reference, ["path", "sha256"]):
		return ""
	var path: String = str(reference["path"])
	if not path.begins_with(PREFIX) or path.contains("..") or path.contains("\\") or path.contains(":"):
		return ""
	var local: String = "res://" + path.trim_prefix(PREFIX)
	if not FileAccess.file_exists(local):
		return ""
	# Packaged assets are immutable. Hash each actual resident source once, then pin it.
	if not _source_hashes.has(local):
		_source_hashes[local] = FileAccess.get_sha256(local)
	if str(reference["sha256"]) != str(_source_hashes[local]):
		return ""
	return local


func _prepare_mesh(reference: Dictionary) -> Dictionary:
	var path: String = _checked_reference(reference)
	if path == "" or not path.ends_with(".json"):
		return _reject("Missing or mismatched geometry")
	if geometry_cache.has(path):
		return geometry_cache[path]
	var mesh: Dictionary = _read_json(path)
	if not _fields(mesh, ["format", "space", "vertices", "uv", "triangles", "weights"], ["seams"]):
		return _reject("Unknown geometry fields")
	if mesh["format"] != "roshan.attachment-mesh/1" or mesh["space"] != "canonical_canvas_px":
		return _reject("Unsupported geometry contract")
	if typeof(mesh["vertices"]) != TYPE_ARRAY or typeof(mesh["uv"]) != TYPE_ARRAY:
		return _reject("Invalid point arrays")
	var vertices: PackedVector2Array = PackedVector2Array()
	var uv: PackedVector2Array = PackedVector2Array()
	for value: Variant in mesh["vertices"]:
		if not _valid_point(value):
			return _reject("Invalid vertex")
		vertices.append(_point(value))
	for value: Variant in mesh["uv"]:
		if not _valid_point(value):
			return _reject("Invalid UV")
		uv.append(_point(value))
	if vertices.size() < 3 or vertices.size() != uv.size():
		return _reject("Point count mismatch")
	if typeof(mesh["triangles"]) != TYPE_ARRAY or mesh["triangles"].is_empty():
		return _reject("Missing triangles")
	var triangles: Array = []
	for triangle: Variant in mesh["triangles"]:
		if typeof(triangle) != TYPE_ARRAY or triangle.size() != 3:
			return _reject("Invalid triangle")
		var indices: PackedInt32Array = PackedInt32Array()
		for index: Variant in triangle:
			if not _number(index) or float(index) != floor(float(index)) or int(index) < 0 or int(index) >= vertices.size():
				return _reject("Triangle index outside mesh")
			indices.append(int(index))
		if absf((vertices[indices[1]] - vertices[indices[0]]).cross(vertices[indices[2]] - vertices[indices[0]])) < 0.00000001:
			return _reject("Degenerate triangle")
		triangles.append(indices)
	if typeof(mesh["weights"]) != TYPE_DICTIONARY or mesh["weights"].is_empty():
		return _reject("Missing weight map")
	var weights: Dictionary = {}
	var totals: PackedFloat64Array = PackedFloat64Array()
	totals.resize(vertices.size())
	for bone_name: String in mesh["weights"]:
		if not bones.has(bone_name):
			return _reject("Unknown binding bone")
		var values: Variant = mesh["weights"][bone_name]
		if typeof(values) != TYPE_ARRAY or values.size() != vertices.size():
			return _reject("Weight count mismatch")
		var packed: PackedFloat32Array = PackedFloat32Array()
		for i in range(values.size()):
			if not _number(values[i]) or float(values[i]) < 0.0 or float(values[i]) > 1.0:
				return _reject("Invalid weight")
			packed.append(float(values[i]))
			totals[i] += float(values[i])
		weights[bone_name] = packed
	for total: float in totals:
		if absf(total - 1.0) > 0.000001:
			return _reject("Unnormalized weights")
	var payload: Dictionary = {"vertices": vertices, "uv": uv, "triangles": triangles, "weights": weights, "path": path}
	geometry_cache[path] = payload
	return payload


func _prepare_attachment(item: Dictionary) -> Dictionary:
	var texture_path: String = _checked_reference(item.get("texture"))
	if texture_path == "" or not texture_path.ends_with(".png"):
		return _reject("Missing or mismatched RGBA artwork")
	var mesh: Dictionary = _prepare_mesh(item["geometry"]) if typeof(item.get("geometry")) == TYPE_DICTIONARY else {}
	if mesh.is_empty():
		return _reject("Invalid garment mesh")
	var texture: ImageTexture
	if textures.has(texture_path):
		texture = textures[texture_path]
	else:
		var image: Image = Image.load_from_file(ProjectSettings.globalize_path(texture_path))
		if image == null or image.get_format() != Image.FORMAT_RGBA8:
			return _reject("Artwork must be RGBA8")
		var width: int = image.get_width()
		var height: int = image.get_height()
		if maxi(width, height) > 1024 and not ((width & (width - 1)) == 0 and (height & (height - 1)) == 0):
			return _reject("Artwork exceeds source texture rule")
		texture = ImageTexture.create_from_image(image)
		textures[texture_path] = texture
	for uv: Vector2 in mesh["uv"]:
		if uv.x < 0 or uv.y < 0 or uv.x > texture.get_width() or uv.y > texture.get_height():
			return _reject("UV outside artwork")
	return {"texture": texture, "mesh": mesh, "texture_path": texture_path}


func _prepare_skin(document: Dictionary) -> Dictionary:
	if not _fields(document, ["format", "skin_id", "rig", "views", "attachments", "coverage", "provenance"]):
		return _reject("Skin contains unknown or missing fields")
	if document["format"] != "roshan.skin/1" or typeof(document["skin_id"]) != TYPE_STRING:
		return _reject("Unsupported skin identity/format")
	if not _fields(document["rig"], ["id", "version", "contract_sha256"]):
		return _reject("Invalid rig pin")
	var pin: Dictionary = document["rig"]
	if pin["id"] != rig["rig_id"] or pin["version"] != rig["version"] or pin["contract_sha256"] != rig_sha:
		return _reject("Skin targets another rig")
	if typeof(document["views"]) != TYPE_ARRAY or document["views"] != [VIEW]:
		return _reject("Unsupported garment view")
	if typeof(document["coverage"]) != TYPE_DICTIONARY or document["coverage"].keys() != [VIEW]:
		return _reject("Invalid view coverage")
	var slots: Dictionary = rig["views"][VIEW]["slots"]
	if not _fields(document["coverage"][VIEW], slots.keys()):
		return _reject("Incomplete slot coverage")
	if typeof(document["attachments"]) != TYPE_ARRAY or document["attachments"].size() != slots.size():
		return _reject("Invalid attachment count")
	var payload: Dictionary = {"skin_id": document["skin_id"], "slots": {}}
	var names: Dictionary = {}
	for item: Variant in document["attachments"]:
		if not _fields(item, ["id", "view", "slot", "mode", "texture", "geometry"]):
			return _reject("Code/unknown attachment fields forbidden")
		if typeof(item["id"]) != TYPE_STRING or names.has(item["id"]):
			return _reject("Duplicate/invalid attachment ID")
		names[item["id"]] = true
		if item["view"] != VIEW or not slots.has(item["slot"]) or payload["slots"].has(item["slot"]):
			return _reject("Unknown or duplicate garment slot")
		if item["mode"] != "weighted" or document["coverage"][VIEW][item["slot"]] != item["id"]:
			return _reject("Unsupported binding or coverage mismatch")
		var prepared: Dictionary = _prepare_attachment(item)
		if prepared.is_empty():
			return {}
		payload["slots"][item["slot"]] = prepared
	if not _fields(document["provenance"], ["sources", "edits", "generator_calls"]):
		return _reject("Missing provenance")
	var provenance: Dictionary = document["provenance"]
	if typeof(provenance["sources"]) != TYPE_ARRAY or provenance["sources"].is_empty():
		return _reject("Missing source scope")
	for source: Variant in provenance["sources"]:
		if not _fields(source, ["asset", "license", "role", "acceptance_scope"]):
			return _reject("Invalid source provenance")
		if str(source["license"]) == "" or str(source["acceptance_scope"]) == "" or _checked_reference(source["asset"]) == "":
			return _reject("Source scope/hash missing")
	return payload


func _new_polygon(node_name: String, layer: int) -> Polygon2D:
	var polygon: Polygon2D = Polygon2D.new()
	polygon.name = node_name
	polygon.z_index = layer
	polygon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	add_child(polygon)
	polygon.skeleton = polygon.get_path_to(skeleton)
	return polygon


func _assign(polygon: Polygon2D, payload: Dictionary) -> void:
	var mesh: Dictionary = payload["mesh"]
	polygon.texture = payload["texture"]
	polygon.polygon = mesh["vertices"]
	polygon.uv = mesh["uv"]
	polygon.polygons = mesh["triangles"]
	polygon.clear_bones()
	for bone_name: String in mesh["weights"]:
		polygon.add_bone(skeleton.get_path_to(bones[bone_name]), mesh["weights"][bone_name])


func _show_fin(value: String) -> void:
	assert(anatomy_nodes.has(value), "Unknown shared anatomical pose state")
	_assign(anatomy_nodes["fin_node"]["node"], anatomy_nodes[value]["payload"])


func apply_skin(name_string: String) -> bool:
	if not prepared_skins.has(name_string):
		last_error = "Unknown skin ID"
		return false
	return _commit_skin(prepared_skins[name_string])


func try_skin_document(document: Dictionary) -> bool:
	# Validation completes before any resident slot changes; invalid state is atomic.
	var old_textures: Array = textures.keys()
	var old_geometry: Array = geometry_cache.keys()
	var old_hashes: Array = _source_hashes.keys()
	var payload: Dictionary = _prepare_skin(document)
	if payload.is_empty():
		for key: String in textures.keys():
			if not old_textures.has(key):
				textures.erase(key)
		for key: String in geometry_cache.keys():
			if not old_geometry.has(key):
				geometry_cache.erase(key)
		for key: String in _source_hashes.keys():
			if not old_hashes.has(key):
				_source_hashes.erase(key)
		return false
	return _commit_skin(payload)


func _commit_skin(payload: Dictionary) -> bool:
	for slot: String in slot_nodes:
		_assign(slot_nodes[slot], payload["slots"][slot])
	skin_id = str(payload["skin_id"])
	# No player.play/seek/stop, bone/rest edits, root transform, or anatomy mutation.
	return true


func _ease(value: float) -> float:
	var t: float = clampf(value, 0.0, 1.0)
	return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


func strength_at(t: float, cycle: bool = false) -> float:
	if cycle:
		return 1.0
	return _ease(t / 0.85) * (1.0 - _ease((t - 5.65) / 1.25))


func angles_at(t: float, cycle: bool) -> Dictionary:
	var phase: float = TAU * t / PERIOD
	var force: float = strength_at(t, cycle)
	var hips: float = 2.4 * sin(phase)
	var result: Dictionary = {"Hips": hips, "Spine": -1.5 * sin(phase - 0.15),
		"Chest": -1.0 * sin(phase - 0.3), "Neck": 0.35 * sin(phase - 0.4),
		"Head": -0.25 * sin(phase - 0.5), "HairRoot": 0.0,
		"HairA": 1.8 * sin(phase - 0.6), "HairB": 2.4 * sin(phase - 0.95),
		"TailA": 5.5 * sin(phase - 0.25), "TailB": 7.0 * sin(phase - 0.80),
		"TailC": 8.0 * sin(phase - 1.35), "TailD": 8.5 * sin(phase - 1.90),
		"Fin": 6.5 * sin(phase - 2.30),
		"LeftUpper": 2.0 * sin(phase - 0.6), "LeftFore": -1.0 * sin(phase - 0.9),
		"LeftHand": 0.4 * sin(phase - 1.0), "RightUpper": -1.8 * sin(phase - 0.5),
		"RightFore": 0.9 * sin(phase - 0.8), "RightHand": -0.4 * sin(phase - 1.0)}
	for name_string: String in result:
		result[name_string] = float(result[name_string]) * force
	# One readable opposing sweep during the braking window, then exact rest.
	if not cycle:
		var brake: float = _ease((t - 5.5) / 0.6) * (1.0 - _ease((t - 6.35) / 0.85))
		result["TailB"] += -4.0 * brake
		result["TailC"] += -4.0 * brake
		result["TailD"] += 3.0 * brake
	return result


func state_at(t: float, cycle: bool) -> String:
	if not cycle and t > 5.75 and t < 6.9:
		return "fin_cup"
	var phase: float = fposmod(t, PERIOD) / PERIOD
	if strength_at(t, cycle) > 0.2 and phase > 0.67 and phase < 0.74:
		return "fin_edge"
	return "fin_broad"


func _build_animation(cycle: bool) -> Animation:
	var animation: Animation = Animation.new()
	animation.length = PERIOD if cycle else SEQUENCE_SECONDS
	animation.loop_mode = Animation.LOOP_LINEAR if cycle else Animation.LOOP_NONE
	var tracks: Dictionary = {}
	for name_string: String in bones:
		var track: int = animation.add_track(Animation.TYPE_VALUE)
		animation.track_set_path(track, NodePath("Skeleton/" + str(skeleton.get_path_to(bones[name_string])) + ":rotation"))
		animation.track_set_interpolation_type(track, Animation.INTERPOLATION_LINEAR)
		tracks[name_string] = track
	var state_track: int = animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(state_track, NodePath(".:fin_state"))
	animation.value_track_set_update_mode(state_track, Animation.UPDATE_DISCRETE)
	var previous: String = ""
	var count: int = int(round(animation.length * 120.0))
	for index in range(count + 1):
		var t: float = float(index) / 120.0
		var angles: Dictionary = angles_at(t, cycle)
		for name_string: String in bones:
			var bone: Bone2D = bones[name_string]
			animation.track_insert_key(tracks[name_string], t, bone.rest.get_rotation() + deg_to_rad(float(angles[name_string])))
		var state: String = state_at(t, cycle)
		if state != previous:
			animation.track_insert_key(state_track, t, state)
			previous = state
	return animation


func pose_at(t: float, clip: String = "sequence") -> void:
	if str(player.assigned_animation) != clip:
		player.play(clip)
	player.seek(t, true)
	if not tail_motion_enabled:
		for name_string: String in ["Hips", "TailA", "TailB", "TailC", "TailD", "Fin"]:
			var bone: Bone2D = bones[name_string]
			bone.transform = bone.rest


func local_bone_transform(name_string: String) -> Transform2D:
	# Compose actor-local transforms directly, avoiding world-translation roundoff.
	var bone: Bone2D = bones[name_string]
	var result: Transform2D = bone.transform
	var parent: Node = bone.get_parent()
	while parent is Bone2D:
		result = (parent as Bone2D).transform * result
		parent = parent.get_parent()
	return result


func reset_travel() -> void:
	position = Vector2.ZERO
	velocity = Vector2.ZERO
	thrust_acceleration = 0.0
	_have_fin_sample = false


func advance_motion(dt: float) -> void:
	if paused or dt <= 0.0:
		return
	var clip: String = str(player.assigned_animation)
	var current: float = player.current_animation_position
	var amount: float = dt if clip == "cycle" else minf(dt, maxf(0.0, SEQUENCE_SECONDS - current))
	if amount > 0.0:
		player.advance(amount)
		if not tail_motion_enabled:
			for name_string: String in ["Hips", "TailA", "TailB", "TailC", "TailD", "Fin"]:
				var bone: Bone2D = bones[name_string]
				bone.transform = bone.rest
		integrate_travel(amount, player.current_animation_position, clip == "cycle")


func integrate_travel(dt: float, t: float, cycle: bool = false) -> void:
	if dt <= 0.0:
		return
	var fin: Vector2 = local_bone_transform("Fin") * Vector2(70, 0)
	var axis: Vector2 = Vector2(145, -52).normalized()
	var lateral: Vector2 = Vector2(-axis.y, axis.x)
	var relative_velocity: Vector2 = (fin - _previous_fin) / dt if _have_fin_sample else Vector2.ZERO
	_previous_fin = fin
	_have_fin_sample = true
	var phase: float = fposmod(t, PERIOD) / PERIOD
	var power_window: float = _ease((phase - 0.12) / 0.12) * (1.0 - _ease((phase - 0.44) / 0.12))
	var normal_speed: float = relative_velocity.dot(lateral)
	thrust_acceleration = 0.018 * normal_speed * normal_speed * power_window * strength_at(t, cycle)
	var drag: float = 1.8 + (6.0 if not cycle and t > 5.75 else 0.0)
	velocity += (axis * thrust_acceleration - velocity * drag) * dt
	position += velocity * dt


func identity_snapshot() -> Dictionary:
	var ids: Array = []
	var pose: Array = []
	var rests: Array = []
	for name_string: String in bones:
		var bone: Bone2D = bones[name_string]
		ids.append([name_string, bone.get_instance_id()])
		pose.append(var_to_str(bone.transform))
		rests.append(var_to_str(bone.rest))
	var nodes: Array = []
	for name_string: String in anatomy_nodes:
		var node: Variant = anatomy_nodes[name_string].get("node")
		if node != null:
			nodes.append([name_string, node.get_instance_id()])
	var slots: Array = []
	for name_string: String in slot_nodes:
		slots.append([name_string, slot_nodes[name_string].get_instance_id()])
	return {"actor_id": get_instance_id(), "skeleton_id": skeleton.get_instance_id(),
		"animator_id": player.get_instance_id(), "bone_ids": ids, "anatomy_nodes": nodes,
		"slot_nodes": slots, "rest_hash": var_to_str(rests).sha256_text(),
		"pose_hash": var_to_str(pose).sha256_text(), "rig_hash": rig_sha,
		"identity_asset_hash": JSON.stringify(rig["identity_assets"]).sha256_text(),
		"animation": str(player.assigned_animation), "phase": player.current_animation_position,
		"root_transform": var_to_str(transform), "velocity": var_to_str(velocity),
		"fin_state": fin_state, "paused": paused, "texture_count": textures.size(),
		"mesh_count": geometry_cache.size(), "node_count": get_child_count() + bones.size()}
