extends RefCounted
# Original-pixel lower boughs; all state and rollback references belong to main.g.
const ATLAS := "res://assets/sprites/sky_lagoon/animated_v1/arrival_boughs.png"
const CLEAN_TILE := "res://assets/sprites/sky_lagoon/animated_v1/arrival_bough_base.png"

static func clear(state: Dictionary) -> void:
	var tile: Variant = state.get("lagoon_bough_tile")
	if is_instance_valid(tile) and tile is Sprite2D:
		(tile as Sprite2D).texture = state.get("lagoon_bough_original") as Texture2D
	var card: Variant = state.get("lagoon_bough_card")
	if is_instance_valid(card) and card is Sprite2D:
		(card as Sprite2D).free()
	for key: String in ["lagoon_bough_tile", "lagoon_bough_original", "lagoon_bough_card", "lagoon_bough_t"]:
		state.erase(key)

static func build(state: Dictionary, parent: Node2D, version: String) -> bool:
	clear(state)
	if version != "animated_v1" or not is_instance_valid(parent):
		return false
	var tile: Sprite2D = parent.get_node_or_null("SkyLagoonBackdrop_r0_c0") as Sprite2D
	if tile == null or tile.texture == null:
		return false
	var atlas: Texture2D = load(ATLAS) as Texture2D
	var clean: Texture2D = load(CLEAN_TILE) as Texture2D
	if atlas == null or clean == null or atlas.get_size() != Vector2(1024, 512) or clean.get_size() != Vector2(1024, 1024):
		return false
	state["lagoon_bough_tile"] = tile
	state["lagoon_bough_original"] = tile.texture
	tile.texture = clean
	var card := Sprite2D.new()
	card.name = "SkyLagoonArrivalBoughCels"
	card.texture = atlas
	card.hframes = 2
	card.vframes = 2
	card.centered = false
	card.position = Vector2(0, 448)
	card.modulate = tile.modulate
	card.texture_filter = tile.texture_filter
	card.set_meta("source_owned", true)
	card.set_meta("canvas_layer_role", "original_boughs_locked")
	parent.add_child(card)
	state["lagoon_bough_card"] = card
	state["lagoon_bough_t"] = 0.0
	return true

static func tick(state: Dictionary, delta: float, paused: bool) -> void:
	if paused:
		return
	var value: Variant = state.get("lagoon_bough_card")
	if not is_instance_valid(value) or not value is Sprite2D:
		return
	var enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true)) and bool(state.get("lagoon_plants_motion_enabled", true))
	var timer: float = float(state.get("lagoon_bough_t", 0.0))
	if enabled:
		timer = fposmod(timer + clampf(delta, 0.0, 0.1), 1.5)
		state["lagoon_bough_t"] = timer
	(value as Sprite2D).frame = mini(2, int(timer / 0.5)) if enabled else 0
