extends RefCounted
# Whole grass crowns at curated planting edges; all mutable state stays on main.g.
const BASE := "res://assets/sprites/sky_lagoon/whole_scene_v2/"
const ROOT := Vector2(128, 220)
const CYCLE := 1.4
const GROUPS: Array[Dictionary] = [
	{"tuft": 0, "root": Vector2(666, 1872), "scale": 0.387, "phase": 0.048535156249999996},
	{"tuft": 1, "root": Vector2(710, 1880), "scale": 0.43, "phase": 0.048535156249999996},
	{"tuft": 2, "root": Vector2(745, 1890), "scale": 0.34400000000000003, "phase": 0.048535156249999996},
	{"tuft": 2, "root": Vector2(2791, 1240), "scale": 0.24, "phase": 0.19345703125},
	{"tuft": 0, "root": Vector2(2837, 1249), "scale": 0.3, "phase": 0.19345703125},
	{"tuft": 1, "root": Vector2(2874, 1226), "scale": 0.24, "phase": 0.19345703125},
	{"tuft": 0, "root": Vector2(3497, 1277), "scale": 0.23800000000000002, "phase": 0.24199218749999998},
	{"tuft": 2, "root": Vector2(3540, 1288), "scale": 0.28, "phase": 0.24199218749999998},
	{"tuft": 1, "root": Vector2(3579, 1273), "scale": 0.23800000000000002, "phase": 0.24199218749999998},
	{"tuft": 1, "root": Vector2(2570, 1903), "scale": 0.45599999999999996, "phase": 0.17841796875},
	{"tuft": 0, "root": Vector2(2619, 1919), "scale": 0.432, "phase": 0.17841796875},
	{"tuft": 2, "root": Vector2(2661, 1909), "scale": 0.48, "phase": 0.17841796875},
	{"tuft": 2, "root": Vector2(3259, 1906), "scale": 0.36000000000000004, "phase": 0.22490234375},
	{"tuft": 1, "root": Vector2(3297, 1894), "scale": 0.32000000000000006, "phase": 0.22490234375},
	{"tuft": 0, "root": Vector2(3338, 1912), "scale": 0.4, "phase": 0.22490234375},
	{"tuft": 0, "root": Vector2(5182, 1726), "scale": 0.324, "phase": 0.3568359375},
	{"tuft": 2, "root": Vector2(5228, 1716), "scale": 0.288, "phase": 0.3568359375},
	{"tuft": 1, "root": Vector2(5265, 1728), "scale": 0.252, "phase": 0.3568359375},
]

static func clear(state: Dictionary) -> void:
	for value: Variant in state.get("lagoon_grass_groups", []) as Array:
		if is_instance_valid(value):
			(value as Sprite2D).free()
	state.erase("lagoon_grass_groups")
	state.erase("lagoon_grass_group_t")

static func build(state: Dictionary, parent: Node2D, tint: Color, texture_base: String = BASE) -> bool:
	clear(state)
	state.erase("lagoon_grass_group_rejection")
	if not is_instance_valid(parent):
		return false
	var textures: Array[Texture2D] = []
	for index: int in range(3):
		var path: String = texture_base + "grass_tuft_%d.png" % index
		if not ResourceLoader.exists(path):
			state["lagoon_grass_group_rejection"] = "Missing grass atlas: " + path
			return false
		var texture: Texture2D = load(path) as Texture2D
		if texture == null or texture.get_size() != Vector2(512, 512):
			state["lagoon_grass_group_rejection"] = "Incorrect grass atlas: " + path
			return false
		textures.append(texture)
	var cards: Array[Sprite2D] = []
	for index: int in range(GROUPS.size()):
		var row: Dictionary = GROUPS[index]
		var card := Sprite2D.new()
		card.name = "WholeGrass_%d" % index
		card.texture = textures[int(row["tuft"])]
		card.hframes = 2
		card.vframes = 2
		card.centered = false
		card.scale = Vector2.ONE * float(row["scale"])
		card.position = (row["root"] as Vector2) - ROOT * card.scale
		card.modulate = tint
		card.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		card.z_index = 2
		card.set_meta("source_owned", true)
		card.set_meta("canvas_layer_role", "whole_grass_planting_edge")
		parent.add_child(card)
		cards.append(card)
	state["lagoon_grass_groups"] = cards
	state["lagoon_grass_group_t"] = 0.0
	return true

static func tick(state: Dictionary, delta: float, paused: bool) -> void:
	if paused or not state.has("lagoon_grass_groups"):
		return
	var enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true)) and bool(state.get("lagoon_plants_motion_enabled", true))
	var timer: float = float(state.get("lagoon_grass_group_t", 0.0))
	if enabled:
		timer = fposmod(timer + clampf(delta, 0.0, 0.1), CYCLE)
		state["lagoon_grass_group_t"] = timer
	var cards: Array = state["lagoon_grass_groups"] as Array
	for index: int in range(cards.size()):
		var card: Sprite2D = cards[index] as Sprite2D
		if is_instance_valid(card):
			card.frame = int(fposmod(timer - float(GROUPS[index]["phase"]), CYCLE) / 0.35) if enabled else 0
