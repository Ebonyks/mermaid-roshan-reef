extends RefCounted
# Painted water cels; the prior light-only profile remains the fallback.
const BASE := "res://assets/sprites/sky_lagoon/animated_v1/water_"
const CLIPS := [
	{"id": "arrival", "rect": Rect2(0, 1180, 640, 400), "cell": Vector2(256, 256), "rows": 3},
	{"id": "castle", "rect": Rect2(4520, 1000, 1624, 640), "cell": Vector2(512, 256), "rows": 4},
]
const PERIOD := 2.16
const SURFACE_PERIOD := 1.92
const SURFACE_BASE := "res://assets/sprites/sky_lagoon/whole_scene_v2/water_surface_"
const SURFACE_CLIPS := [
	{"id": "arrival", "cell": Vector2(256, 256), "position": Vector2(-4.920634920634921, 1175.079365079365), "scale": 2.4603174603174605, "rect": Rect2(0, 1180, 620, 400)},
	{"id": "castle", "cell": Vector2(512, 256), "position": Vector2(4513.606299212598, 993.6062992125984), "scale": 3.1968503937007875, "rect": Rect2(4520, 1000, 1624, 620)},
]
static func clear(state: Dictionary) -> void:
	for value: Variant in state.get("lagoon_water_highlights", []) as Array:
		if is_instance_valid(value) and value is Sprite2D:
			(value as Sprite2D).free()
	state.erase("lagoon_water_highlights")
	state.erase("lagoon_water_highlight_t")
	state.erase("lagoon_water_surface_active")
static func build(state: Dictionary, parent: Node2D, version: String, night: bool) -> bool:
	clear(state)
	if version != "animated_v1" or not is_instance_valid(parent):
		return false
	if not (state.get("lagoon_whole_cards", []) as Array).is_empty() and _build_surface(state, parent, night):
		return true
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
static func _build_surface(state: Dictionary, parent: Node2D, night: bool) -> bool:
	var textures: Array[Texture2D] = []
	for spec: Dictionary in SURFACE_CLIPS:
		var path: String = SURFACE_BASE + str(spec["id"]) + ".png"
		if not ResourceLoader.exists(path):
			return false
		var texture: Texture2D = load(path) as Texture2D
		if texture == null or texture.get_size() != (spec["cell"] as Vector2) * 4.0:
			return false
		textures.append(texture)
	var cards: Array[Sprite2D] = []
	for index: int in range(SURFACE_CLIPS.size()):
		var spec: Dictionary = SURFACE_CLIPS[index]
		var card := Sprite2D.new()
		card.name = "SkyLagoonPaintedWater_" + str(spec["id"])
		card.texture = textures[index]
		card.centered = false
		card.hframes = 4
		card.vframes = 4
		card.position = spec["position"] as Vector2
		card.scale = Vector2.ONE * float(spec["scale"])
		card.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		card.set_meta("master_rect", spec["rect"])
		card.set_meta("canvas_layer_role", "painted_water_surface")
		card.set_meta("source_owned", true)
		if night:
			card.modulate = Color(0.48, 0.56, 0.82)
		parent.add_child(card)
		cards.append(card)
	state["lagoon_water_highlights"] = cards
	state["lagoon_water_highlight_t"] = 0.0
	state["lagoon_water_surface_active"] = true
	return true
static func tick(state: Dictionary, delta: float, paused: bool) -> void:
	if paused or not state.has("lagoon_water_highlights"):
		return
	var enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true)) and bool(state.get("lagoon_water_motion_enabled", true))
	var timer: float = float(state.get("lagoon_water_highlight_t", 0.0))
	var period: float = SURFACE_PERIOD if bool(state.get("lagoon_water_surface_active", false)) else PERIOD
	if enabled:
		timer = fposmod(timer + clampf(delta, 0.0, 0.1), period)
		state["lagoon_water_highlight_t"] = timer
	for value: Variant in state["lagoon_water_highlights"] as Array:
		if is_instance_valid(value) and value is Sprite2D:
			var card: Sprite2D = value as Sprite2D
			card.visible = enabled
			card.frame = mini(11, int(timer / period * 12.0)) if enabled else 0
