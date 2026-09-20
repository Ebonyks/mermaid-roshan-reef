extends RefCounted
# Sparse authored plant cels. Mutable state stays on ReefMain.g.
const ATLAS := "res://assets/sprites/sky_lagoon/animated_v1/bellflower_breeze.png"
const WHOLE_SCENE_ATLAS := "res://assets/sprites/sky_lagoon/whole_scene_v2/bellflower_leaf_grade.png"
const ROOT := Vector2(308, 468)
const CELL := Vector2(512, 512)
const DURATIONS := [0.26, 0.24, 0.30, 0.26, 0.22, 0.24, 0.30, 0.26]
const CYCLE := 2.08
const ANCHORS: Array[Vector2] = [Vector2(1120, 1970), Vector2(5820, 1980)]
const SCALES := [0.72, 0.95]

static func clear(state: Dictionary) -> void:
	for value: Variant in state.get("lagoon_plant_cels", []) as Array:
		if is_instance_valid(value) and value is Sprite2D:
			(value as Sprite2D).free()
	state.erase("lagoon_plant_cels")
	state.erase("lagoon_plant_cel_t")

static func build(state: Dictionary, parent: Node2D, version: String, night: bool) -> bool:
	clear(state)
	if version != "animated_v1" or not is_instance_valid(parent) or not ResourceLoader.exists(ATLAS):
		return false
	var texture: Texture2D = null
	if not (state.get("lagoon_whole_cards", []) as Array).is_empty() and ResourceLoader.exists(WHOLE_SCENE_ATLAS):
		texture = load(WHOLE_SCENE_ATLAS) as Texture2D
		if texture != null and texture.get_size() != Vector2(2048, 1024):
			texture = null
	if texture == null:
		texture = load(ATLAS) as Texture2D
	if texture == null or texture.get_size() != Vector2(2048, 1024):
		return false
	var cards: Array[Sprite2D] = []
	for index: int in range(ANCHORS.size()):
		var card := Sprite2D.new()
		card.name = "SkyLagoonBellflower_%d" % index
		card.texture = texture
		card.hframes = 4
		card.vframes = 2
		card.scale = Vector2.ONE * float(SCALES[index])
		card.position = ANCHORS[index] - (ROOT - CELL * 0.5) * card.scale
		card.set_meta("root_anchor", ANCHORS[index])
		card.set_meta("cel_phase", float(index) * 0.67)
		card.set_meta("source_owned", true)
		card.set_meta("placement_role", "new_sparse_foreground_bellflower")
		card.set_meta("canvas_layer_role", "foreground_geography_locked")
		if night:
			card.modulate = Color(0.48, 0.56, 0.82)
		parent.add_child(card)
		cards.append(card)
	state["lagoon_plant_cels"] = cards
	state["lagoon_plant_cel_t"] = 0.0
	return true

static func frame_at(time: float) -> int:
	var remainder: float = fposmod(time, CYCLE)
	for index: int in range(DURATIONS.size()):
		remainder -= float(DURATIONS[index])
		if remainder < 0.0:
			return index
	return 0

static func tick(state: Dictionary, delta: float, paused: bool) -> void:
	if paused or not state.has("lagoon_plant_cels"):
		return
	var enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true)) and bool(state.get("lagoon_plants_motion_enabled", true))
	var timer: float = float(state.get("lagoon_plant_cel_t", 0.0))
	if enabled:
		timer = fposmod(timer + clampf(delta, 0.0, 0.1), CYCLE)
		state["lagoon_plant_cel_t"] = timer
	for value: Variant in state["lagoon_plant_cels"] as Array:
		if is_instance_valid(value) and value is Sprite2D:
			var card: Sprite2D = value as Sprite2D
			card.frame = frame_at(timer + float(card.get_meta("cel_phase", 0.0))) if enabled else 0
