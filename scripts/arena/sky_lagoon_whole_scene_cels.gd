extends RefCounted
# Optional whole-scene source trial. All mutable state belongs to main.g.
const BASE := "res://assets/sprites/sky_lagoon/whole_scene_v2/"
const PATH := BASE + "manifest.json"

static func clear(state: Dictionary) -> void:
	for value: Variant in state.get("lagoon_whole_cards", []):
		if is_instance_valid(value):
			(value as Sprite2D).free()
	for value: Variant in state.get("lagoon_whole_tiles", []):
		var row: Array = value as Array
		if is_instance_valid(row[0]):
			(row[0] as Sprite2D).texture = row[1] as Texture2D
	for key: String in ["lagoon_whole_cards", "lagoon_whole_tiles", "lagoon_whole_t"]:
		state.erase(key)

static func build(state: Dictionary, parent: Node2D, requested: bool, manifest_path: String = PATH) -> bool:
	clear(state)
	state.erase("lagoon_whole_rejection")
	if not requested or not is_instance_valid(parent):
		return false
	var parser := JSON.new()
	if not FileAccess.file_exists(manifest_path) or parser.parse(FileAccess.get_file_as_string(manifest_path)) != OK or not parser.data is Dictionary:
		state["lagoon_whole_rejection"] = "Missing or malformed manifest"
		return false
	var data: Dictionary = parser.data as Dictionary
	if data.get("schema") != 1 or not data.get("tiles") is Array or not data.get("cards") is Array:
		return false
	var tiles: Array = data["tiles"] as Array
	var cards: Array = data["cards"] as Array
	if tiles.size() != 12 or cards.size() != 28:
		return false
	state["lagoon_whole_rejection"] = "Invalid whole-scene resource contract"
	var textures: Dictionary = {}
	var tile_nodes: Dictionary = {}
	for value: Variant in tiles + cards:
		if not value is Dictionary:
			return false
		var row: Dictionary = value as Dictionary
		var file: String = str(row.get("file", ""))
		if not file.ends_with(".png") or file.get_file() != file or textures.has(file):
			return false
		var size: Variant = row.get("size")
		if not size is Array or (size as Array).size() != 2:
			return false
		if typeof(size[0]) not in [TYPE_INT, TYPE_FLOAT] or typeof(size[1]) not in [TYPE_INT, TYPE_FLOAT] or not ResourceLoader.exists(BASE + file):
			return false
		var texture: Texture2D = load(BASE + file) as Texture2D
		if texture == null or texture.get_size() != Vector2(float(size[0]), float(size[1])):
			state["lagoon_whole_rejection"] = "Missing or incorrect texture: " + file
			return false
		textures[file] = texture
	for value: Variant in tiles:
		var row: Dictionary = value as Dictionary
		var node_name: String = str(row.get("node", ""))
		var allowed: bool = false
		for r: int in range(2):
			for c: int in range(6):
				allowed = allowed or node_name == "SkyLagoonBackdrop_r%d_c%d" % [r, c]
		if not allowed:
			return false
		var node: Sprite2D = parent.get_node_or_null(NodePath(node_name)) as Sprite2D
		if node == null or node.texture == null or tile_nodes.has(node_name) or node_name.is_empty():
			return false
		tile_nodes[node_name] = node
	for value: Variant in cards:
		var row: Dictionary = value as Dictionary
		if not row.get("id") is String or not row.get("family") in ["tree", "grass", "shrubs", "cloud", "foreground"]:
			return false
		for key: String in ["frames", "columns", "rows", "scale", "cycle", "drift"]:
			if typeof(row.get(key)) not in [TYPE_INT, TYPE_FLOAT] or not is_finite(float(row[key])):
				return false
		if row.has("pose_cycle"):
			if typeof(row["pose_cycle"]) not in [TYPE_INT, TYPE_FLOAT] or not is_finite(float(row["pose_cycle"])) or float(row["pose_cycle"]) <= 0.0:
				return false
		var position: Variant = row.get("position")
		if not position is Array or (position as Array).size() != 2:
			return false
		for component: Variant in position:
			if typeof(component) not in [TYPE_INT, TYPE_FLOAT] or not is_finite(float(component)):
				return false
		var count: int = int(row.get("frames", 0))
		var columns: int = int(row.get("columns", 0))
		var rows: int = int(row.get("rows", 0))
		if count < 1 or count > 24 or columns < 1 or columns > 16 or rows < 1 or rows > 16 or count > columns * rows or float(row.get("scale", 0.0)) <= 0.0 or float(row.get("cycle", 0.0)) <= 0.0:
			return false
	state.erase("lagoon_whole_rejection")
	# All resources and destinations are checked before changing any stage pixels.
	state["lagoon_whole_tiles"] = []
	state["lagoon_whole_cards"] = []
	state["lagoon_whole_t"] = 0.0
	for value: Variant in tiles:
		var row: Dictionary = value as Dictionary
		var tile: Sprite2D = tile_nodes[str(row["node"])] as Sprite2D
		(state["lagoon_whole_tiles"] as Array).append([tile, tile.texture])
		tile.texture = textures[str(row["file"])] as Texture2D
	var index: int = 0
	for value: Variant in cards:
		var row: Dictionary = value as Dictionary
		var card := Sprite2D.new()
		card.name = "WholeScene_" + str(row["id"])
		card.texture = textures[str(row["file"])] as Texture2D
		card.centered = false
		card.hframes = int(row["columns"])
		card.vframes = int(row["rows"])
		card.position = Vector2(float(row["position"][0]), float(row["position"][1]))
		card.scale = Vector2.ONE * float(row["scale"])
		card.modulate = (tile_nodes["SkyLagoonBackdrop_r0_c0"] as Sprite2D).modulate
		card.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		card.z_index = 4 if str(row["family"]) in ["tree", "foreground"] else 1
		card.set_meta("definition", row)
		card.set_meta("phase", float(index % 7) * 0.09)
		card.set_meta("source_owned", true)
		card.set_meta("canvas_layer_role", "whole_scene_" + str(row["family"]))
		parent.add_child(card)
		(state["lagoon_whole_cards"] as Array).append(card)
		index += 1
	return true

static func tick(state: Dictionary, delta: float, paused: bool) -> void:
	if paused or not state.has("lagoon_whole_cards"):
		return
	var enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true))
	var timer: float = float(state.get("lagoon_whole_t", 0.0))
	if enabled:
		timer += clampf(delta, 0.0, 0.1)
		state["lagoon_whole_t"] = timer
	for value: Variant in state["lagoon_whole_cards"]:
		if not is_instance_valid(value):
			continue
		var card: Sprite2D = value as Sprite2D
		var row: Dictionary = card.get_meta("definition") as Dictionary
		var cloud: bool = str(row["family"]) == "cloud"
		var moving: bool = enabled and (cloud or bool(state.get("lagoon_plants_motion_enabled", true)))
		var phase: float = float(card.get_meta("phase"))
		var count: int = int(row["frames"])
		var cycle: float = float(row["cycle"])
		var pose_cycle: float = float(row.get("pose_cycle", cycle))
		card.frame = mini(count - 1, int(fposmod(maxf(0.0, timer - phase), pose_cycle) / pose_cycle * count)) if moving else 0
		var home := Vector2(float(row["position"][0]), float(row["position"][1]))
		card.position = home
		if moving and cloud:
			card.position.x += (sin(timer * TAU / cycle + phase) - sin(phase)) * float(row["drift"])
