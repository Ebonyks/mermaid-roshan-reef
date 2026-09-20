extends RefCounted
# Light-only authored cels, anchored to the existing painted pools.
const BASE := "res://assets/sprites/sky_lagoon/animated_v1/water_"
const CLIPS := [
	{"id": "arrival", "rect": Rect2(0, 1180, 640, 400), "cell": Vector2(256, 256), "rows": 3},
	{"id": "castle", "rect": Rect2(4520, 1000, 1624, 640), "cell": Vector2(512, 256), "rows": 4},
]
const PERIOD := 2.16
static func clear(state: Dictionary) -> void:
	for value: Variant in state.get("lagoon_water_highlights", []) as Array:
		if is_instance_valid(value) and value is Sprite2D:
			(value as Sprite2D).free()
	state.erase("lagoon_water_highlights")
	state.erase("lagoon_water_highlight_t")
static func build(state: Dictionary, parent: Node2D, version: String, night: bool) -> bool:
	clear(state)
	if version != "animated_v1" or not is_instance_valid(parent):
		return false
	var cards: Array[Sprite2D] = []
	for spec: Dictionary in CLIPS:
		var texture: Texture2D = load(BASE + String(spec["id"]) + "_highlights.png") as Texture2D
		var cell: Vector2 = spec["cell"] as Vector2
		if texture == null or texture.get_size() != cell * Vector2(4, int(spec["rows"])):
			for card: Sprite2D in cards:
				card.free()
			return false
		var card := Sprite2D.new()
		card.name = "SkyLagoonPaintedWater_" + String(spec["id"])
		card.texture = texture
		card.hframes = 4
		card.vframes = int(spec["rows"])
		var rect: Rect2 = spec["rect"] as Rect2
		card.position = rect.get_center()
		card.scale = rect.size / cell
		card.set_meta("master_rect", rect)
		card.set_meta("canvas_layer_role", "painted_water_light")
		card.set_meta("source_owned", true)
		if night:
			card.modulate = Color(0.48, 0.56, 0.82, 0.7)
		parent.add_child(card)
		cards.append(card)
	state["lagoon_water_highlights"] = cards
	state["lagoon_water_highlight_t"] = 0.0
	return true
static func tick(state: Dictionary, delta: float, paused: bool) -> void:
	if paused or not state.has("lagoon_water_highlights"):
		return
	var enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true)) and bool(state.get("lagoon_water_motion_enabled", true))
	var timer: float = float(state.get("lagoon_water_highlight_t", 0.0))
	if enabled:
		timer = fposmod(timer + clampf(delta, 0.0, 0.1), PERIOD)
		state["lagoon_water_highlight_t"] = timer
	for value: Variant in state["lagoon_water_highlights"] as Array:
		if is_instance_valid(value) and value is Sprite2D:
			var card: Sprite2D = value as Sprite2D
			card.visible = enabled
			card.frame = mini(11, int(timer / 0.18)) if enabled else 0
