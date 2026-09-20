extends RefCounted
# Candidate cel playback. All mutable state remains in ReefMain.g.
# The original stage remains the default until the complete rebuild is accepted.
const GRASS_PATH := "res://assets/sprites/sky_lagoon/animated_v1/grass_breeze.png"
const ROOT_IN_CELL := Vector2(160.0, 292.0)
const CELL_SIZE := Vector2(320.0, 320.0)
const FRAME_DURATIONS := [0.24, 0.20, 0.24, 0.26]
const CYCLE_S := 0.94
const GRASS_SCALE := 0.30
# Intentional small groups in grass, below the stone walk lane. No route targets.
const GRASS_ANCHORS: Array[Vector2] = [
	Vector2(610, 1895), Vector2(705, 1878), Vector2(1350, 1855),
	Vector2(2250, 1875), Vector2(2340, 1900), Vector2(3065, 1890),
	Vector2(3620, 1860), Vector2(3730, 1895), Vector2(4500, 1900),
	Vector2(4580, 1880), Vector2(5620, 1920), Vector2(5720, 1900),
]

static func clear(state: Dictionary) -> void:
	clear_bridge(state)
	for value: Variant in state.get("lagoon_environment_cels", []) as Array:
		if is_instance_valid(value) and value is Sprite2D:
			(value as Sprite2D).free()
	state.erase("lagoon_environment_cels")
	state.erase("lagoon_environment_cel_t")

static func build(state: Dictionary, parent: Node2D, version: String, night: bool = false) -> bool:
	clear(state)
	if version != "animated_v1" or not is_instance_valid(parent):
		return false
	if not ResourceLoader.exists(GRASS_PATH):
		return false
	var texture: Texture2D = load(GRASS_PATH) as Texture2D
	if texture == null or texture.get_size() != CELL_SIZE * 2.0:
		return false
	var cards: Array[Sprite2D] = []
	for index: int in range(GRASS_ANCHORS.size()):
		var card := Sprite2D.new()
		card.name = "SkyLagoonGrassCels_%02d" % index
		card.texture = texture
		card.hframes = 2
		card.vframes = 2
		card.frame = 0
		if night:
			card.modulate = Color(0.48, 0.56, 0.82)
		card.scale = Vector2.ONE * GRASS_SCALE
		card.position = GRASS_ANCHORS[index] - (ROOT_IN_CELL - CELL_SIZE * 0.5) * GRASS_SCALE
		card.set_meta("source_owned", true)
		card.set_meta("placement_role", "new_ground_cover")
		card.set_meta("canvas_layer_role", "foreground_geography_locked")
		card.set_meta("root_anchor", GRASS_ANCHORS[index])
		card.set_meta("cel_phase", float(index % 4) * 0.11)
		parent.add_child(card)
		cards.append(card)
	state["lagoon_environment_cels"] = cards
	state["lagoon_environment_cel_t"] = 0.0
	return true

static func frame_at(seconds: float) -> int:
	var remaining: float = fposmod(seconds, CYCLE_S)
	for index: int in range(FRAME_DURATIONS.size()):
		remaining -= float(FRAME_DURATIONS[index])
		if remaining < 0.0:
			return index
	return 0

static func tick(state: Dictionary, delta: float, paused: bool) -> void:
	if paused or not state.has("lagoon_environment_cels"):
		return
	var motion_enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true))
	var timer: float = float(state.get("lagoon_environment_cel_t", 0.0))
	if motion_enabled:
		timer = fposmod(timer + clampf(delta, 0.0, 0.1), CYCLE_S)
		state["lagoon_environment_cel_t"] = timer
	for value: Variant in state["lagoon_environment_cels"] as Array:
		if not is_instance_valid(value) or not value is Sprite2D:
			continue
		var card: Sprite2D = value as Sprite2D
		if card != null:
			card.frame = frame_at(timer + float(card.get_meta("cel_phase", 0.0))) if motion_enabled else 0

const BRIDGE_ATLAS := "res://assets/sprites/sky_lagoon/animated_v1/bridge_contact.png"
const BRIDGE_RAIL := "res://assets/sprites/sky_lagoon/animated_v1/bridge_front_rail_fixed.png"
const CHAIN_ATLAS := "res://assets/sprites/sky_lagoon/animated_v1/bridge_chains.png"
const CASTLE_FIXED := "res://assets/sprites/sky_lagoon/animated_v1/castle_fixed.png"
const BRIDGE_DURATIONS := [0.05, 0.05, 0.04, 0.05, 0.07, 0.07, 0.06, 0.06, 0.05, 0.06, 0.06, 0.10]
const BRIDGE_CONTACT: Array[Vector2] = [
 Vector2(100, 949), Vector2(222, 875), Vector2(302, 888), Vector2(302, 993)]

static func clear_bridge(state: Dictionary) -> void:
	var castle_value: Variant = state.get("lagoon_bridge_castle")
	if is_instance_valid(castle_value) and castle_value is Sprite2D:
		(castle_value as Sprite2D).texture = state.get("lagoon_bridge_original") as Texture2D
	var rail_value: Variant = state.get("lagoon_bridge_rail")
	if is_instance_valid(rail_value) and rail_value is Sprite2D:
		(rail_value as Sprite2D).free()
	var patch_value: Variant = state.get("lagoon_bridge_patch")
	if is_instance_valid(patch_value) and patch_value is Sprite2D:
		(patch_value as Sprite2D).free()
	for key: String in ["lagoon_bridge_castle", "lagoon_bridge_original", "lagoon_bridge_patch", "lagoon_bridge_rail",
		"lagoon_bridge_chains", "lagoon_bridge_t", "lagoon_bridge_last_contact", "lagoon_bridge_was_on_deck", "lagoon_bridge_was_moving", "lagoon_bridge_play_count"]:
		state.erase(key)

static func build_bridge(state: Dictionary, castle: Sprite2D, version: String, foreground: Node2D = null) -> bool:
	clear_bridge(state)
	if version != "animated_v1" or not is_instance_valid(castle):
		return false
	if not ResourceLoader.exists(BRIDGE_ATLAS) or not ResourceLoader.exists(CASTLE_FIXED) or not ResourceLoader.exists(BRIDGE_RAIL) or not ResourceLoader.exists(CHAIN_ATLAS):
		return false
	if foreground == null:
		foreground = castle.get_parent() as Node2D
	if not is_instance_valid(foreground):
		return false
	var chain_texture: Texture2D = load(CHAIN_ATLAS) as Texture2D
	if chain_texture == null or chain_texture.get_size() != Vector2(896, 576):
		return false
	var rail_texture: Texture2D = load(BRIDGE_RAIL) as Texture2D
	if rail_texture == null or rail_texture.get_size() != Vector2(304, 286):
		return false
	var atlas: Texture2D = load(BRIDGE_ATLAS) as Texture2D
	var fixed: Texture2D = load(CASTLE_FIXED) as Texture2D
	if atlas == null or fixed == null or atlas.get_size() != Vector2(1024, 576) or fixed.get_size() != Vector2(1022, 1024):
		return false
	state["lagoon_bridge_original"] = castle.texture
	state["lagoon_bridge_castle"] = castle
	castle.texture = fixed
	var patch := Sprite2D.new()
	patch.name = "BridgeContactCels"
	patch.texture = atlas
	patch.hframes = 4
	patch.vframes = 3
	patch.position = Vector2(64, 832) + Vector2(256, 192) * 0.5 - fixed.get_size() * 0.5
	patch.set_meta("source_owned", true)
	castle.add_child(patch)
	var rail := Sprite2D.new()
	rail.name = "BridgeFrontRail"
	rail.texture = rail_texture
	rail.position = castle.position + (Vector2(320, 710) + Vector2(304, 286) * 0.5 - Vector2(511, 512)) * castle.scale
	rail.scale = castle.scale
	rail.modulate = castle.modulate
	rail.set_meta("source_owned", true)
	rail.set_meta("canvas_layer_role", "foreground_geography_locked")
	rail.set_meta("occlusion_role", "near_bridge_rail")
	foreground.add_child(rail)
	var chains := Sprite2D.new()
	chains.name = "BridgeChainResponseCels"
	chains.texture = chain_texture
	chains.hframes = 4
	chains.vframes = 3
	chains.position = Vector2(8, -19)
	chains.set_meta("source_owned", true)
	chains.set_meta("occlusion_role", "near_bridge_chain")
	rail.add_child(chains)
	state["lagoon_bridge_chains"] = chains
	state["lagoon_bridge_rail"] = rail
	state["lagoon_bridge_patch"] = patch
	state["lagoon_bridge_t"] = -1.0
	state["lagoon_bridge_was_on_deck"] = false
	state["lagoon_bridge_play_count"] = 0
	return true

static func tick_bridge(state: Dictionary, delta: float, contact_master: Vector2, moving: bool, paused: bool) -> void:
	if paused:
		return
	var castle_value: Variant = state.get("lagoon_bridge_castle")
	var patch_value: Variant = state.get("lagoon_bridge_patch")
	if not is_instance_valid(castle_value) or not is_instance_valid(patch_value):
		return
	var castle: Sprite2D = castle_value as Sprite2D
	var patch: Sprite2D = patch_value as Sprite2D
	if castle == null or patch == null:
		return
	var chains: Sprite2D = state.get("lagoon_bridge_chains") as Sprite2D
	var local: Vector2 = (contact_master - castle.position) / castle.scale + Vector2(511, 512)
	var on_deck: bool = Geometry2D.is_point_in_polygon(local, PackedVector2Array(BRIDGE_CONTACT))
	var was_on: bool = bool(state.get("lagoon_bridge_was_on_deck", false))
	var was_moving: bool = bool(state.get("lagoon_bridge_was_moving", false))
	state["lagoon_bridge_was_moving"] = moving
	state["lagoon_bridge_was_on_deck"] = on_deck
	var enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true)) and bool(state.get("lagoon_bridge_motion_enabled", true))
	var timer: float = float(state.get("lagoon_bridge_t", -1.0))
	if not enabled:
		patch.frame = 0
		if is_instance_valid(chains):
			chains.frame = 0
		state["lagoon_bridge_t"] = -1.0
		state["lagoon_bridge_last_contact"] = local
		return
	var last: Vector2 = state.get("lagoon_bridge_last_contact", local) as Vector2
	if timer < 0.0 and on_deck and moving and (not was_on or not was_moving or local.distance_to(last) >= 32.0):
		timer = 0.0
		state["lagoon_bridge_last_contact"] = local
		state["lagoon_bridge_play_count"] = int(state.get("lagoon_bridge_play_count", 0)) + 1
	if timer >= 0.0:
		timer += clampf(delta, 0.0, 0.1)
		var remainder: float = timer
		var frame: int = 0
		for index: int in range(BRIDGE_DURATIONS.size()):
			remainder -= float(BRIDGE_DURATIONS[index])
			if remainder < 0.0:
				frame = index
				break
		if remainder >= 0.0:
			timer = -1.0
		patch.frame = frame
		if is_instance_valid(chains):
			chains.frame = frame
	state["lagoon_bridge_t"] = timer
