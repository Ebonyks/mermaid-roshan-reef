extends RefCounted
# Validate the entire opt-in pack before any original art or route is replaced.
const BASE := "res://assets/sprites/sky_lagoon/animated_v1/"
const PATH := BASE + "manifest.json"
const REQUIRED := {
	"arrival_bough_base.png": Vector2i(1024, 1024),
	"arrival_boughs.png": Vector2i(1024, 512),
	"bellflower_breeze.png": Vector2i(2048, 1024),
	"bridge_chains.png": Vector2i(896, 576),
	"bridge_contact.png": Vector2i(1024, 576),
	"bridge_front_rail_fixed.png": Vector2i(304, 286),
	"castle_fixed.png": Vector2i(1022, 1024),
	"cloud_painted.png": Vector2i(327, 167),
	"conifer_breeze.png": Vector2i(768, 768),
	"grass_breeze.png": Vector2i(640, 640),
	"huckleberry_breeze.png": Vector2i(2048, 1024),
	"water_arrival_highlights.png": Vector2i(1024, 768),
	"water_arrival_shore.png": Vector2i(1024, 512),
	"water_castle_highlights.png": Vector2i(2048, 1024),
	"water_castle_shore.png": Vector2i(2048, 512),
	"water_surface_mask.png": Vector2i(1024, 512),
}
const SHARED_RIPPLE := "res://assets/sprites/fx_water/fx_water_ripple_ring_atlas.png"

static func clear(state: Dictionary) -> void:
	state.erase("lagoon_candidate_resources")
	state.erase("lagoon_candidate_rejection")

static func validate_document(document: Variant) -> String:
	if not document is Dictionary:
		return "Manifest must be an object"
	var data: Dictionary = document as Dictionary
	if typeof(data.get("schema")) not in [TYPE_INT, TYPE_FLOAT]:
		return "Manifest schema is not numeric"
	if data.get("schema") != 1 or data.get("art_version") != "animated_v1" or not data.get("assets") is Array:
		return "Manifest schema or version is invalid"
	var rows: Array = data["assets"] as Array
	if rows.size() != REQUIRED.size():
		return "Manifest does not cover the complete candidate"
	var seen: Dictionary = {}
	for value: Variant in rows:
		if not value is Dictionary:
			return "Invalid asset row"
		var row: Dictionary = value as Dictionary
		var file: Variant = row.get("file")
		if not file is String or not REQUIRED.has(file) or seen.has(file):
			return "Unknown or duplicate asset"
		var size: Variant = row.get("size")
		if not size is Array or (size as Array).size() != 2:
			return "Invalid asset dimensions"
		if typeof(size[0]) not in [TYPE_INT, TYPE_FLOAT] or typeof(size[1]) not in [TYPE_INT, TYPE_FLOAT]:
			return "Asset dimensions must be numeric"
		var expected: Vector2i = REQUIRED[file]
		if size[0] != expected.x or size[1] != expected.y:
			return "Unexpected asset dimensions: " + String(file)
		seen[file] = true
	return ""

static func select_version(requested: String, state: Dictionary, manifest_path: String = PATH, texture_loader: Callable = Callable()) -> String:
	clear(state)
	if requested != "animated_v1":
		return "original"
	var rejection := "Manifest is missing"
	if FileAccess.file_exists(manifest_path):
		var parser := JSON.new()
		if parser.parse(FileAccess.get_file_as_string(manifest_path)) == OK:
			rejection = validate_document(parser.data)
		else:
			rejection = "Manifest JSON is malformed"
	var textures: Dictionary = {}
	var resolver: Callable = texture_loader if texture_loader.is_valid() else _load_checked
	if rejection.is_empty():
		for file: String in REQUIRED:
			var texture: Texture2D = resolver.call(BASE + file, REQUIRED[file]) as Texture2D
			if texture == null:
				rejection = "Missing or invalid texture: " + file
				break
			textures[file] = texture
	if rejection.is_empty():
		var ripple: Texture2D = resolver.call(SHARED_RIPPLE, Vector2i(1024, 512)) as Texture2D
		if ripple == null:
			rejection = "Shared ripple texture is missing or invalid"
		else:
			textures["shared_ripple"] = ripple
	if not rejection.is_empty():
		state["lagoon_candidate_rejection"] = rejection
		return "original"
	# Hold decoded resources on main.g so validation does not cause a second load.
	state["lagoon_candidate_resources"] = textures
	return "animated_v1"

static func _load_checked(path: String, size: Vector2i) -> Texture2D:
	if not ResourceLoader.exists(path, "Texture2D"):
		return null
	var texture: Texture2D = load(path) as Texture2D
	return texture if texture != null and texture.get_size() == Vector2(size) else null
