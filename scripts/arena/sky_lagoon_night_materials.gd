extends RefCounted
# Material-only night treatment for the opt-in whole-scene preview.
const LEAF_SHADER := "res://shaders/sky_lagoon_night_leaf_material.gdshader"
const WINDOWS := "res://assets/sprites/sky_lagoon/whole_scene_v2/castle_window_material.png"

static func clear(state: Dictionary) -> void:
	var material: Material = state.get("lagoon_night_leaf_material") as Material
	for value: Variant in state.get("lagoon_night_leaf_cards", []) as Array:
		if is_instance_valid(value) and (value as Sprite2D).material == material:
			(value as Sprite2D).material = null
	var window: Variant = state.get("lagoon_window_material_card")
	if is_instance_valid(window):
		(window as Sprite2D).free()
	for key: String in ["lagoon_night_leaf_material", "lagoon_night_leaf_cards", "lagoon_window_material_card", "lagoon_night_material_rejection"]:
		state.erase(key)

static func build(state: Dictionary, night: bool) -> bool:
	clear(state)
	if not night or (state.get("lagoon_whole_cards", []) as Array).is_empty():
		return false
	var holder: Node2D = state.get("lagoon_base_layer") as Node2D
	var castle: Sprite2D = state.get("lagoon_castle_card") as Sprite2D
	if not is_instance_valid(holder) or not is_instance_valid(castle) or castle.texture == null:
		return false
	if not ResourceLoader.exists(LEAF_SHADER) or not ResourceLoader.exists(WINDOWS):
		state["lagoon_night_material_rejection"] = "Missing night material resource"
		return false
	var shader: Shader = load(LEAF_SHADER) as Shader
	var texture: Texture2D = load(WINDOWS) as Texture2D
	if shader == null or texture == null or texture.get_size() != Vector2(898, 471) or minf(castle.modulate.r, minf(castle.modulate.g, castle.modulate.b)) <= 0.0:
		state["lagoon_night_material_rejection"] = "Invalid night material resource or castle tint"
		return false
	var cards: Array[Sprite2D] = []
	for child: Node in holder.get_children():
		if child is Sprite2D and (child as Sprite2D).material == null:
			cards.append(child as Sprite2D)
	for key: String in ["lagoon_plant_cels", "lagoon_huckleberry_cels"]:
		for value: Variant in state.get(key, []) as Array:
			if is_instance_valid(value) and value is Sprite2D and (value as Sprite2D).material == null and not cards.has(value):
				cards.append(value as Sprite2D)
	for value: Variant in state.get("lagoon_ambient_cards", []) as Array:
		if is_instance_valid(value) and value is Sprite2D and str((value as Sprite2D).get_meta("ambient_kind", "")) == "foreground_tree" and (value as Sprite2D).material == null:
			cards.append(value as Sprite2D)
	var material := ShaderMaterial.new()
	material.shader = shader
	for card: Sprite2D in cards:
		card.material = material
	state["lagoon_night_leaf_material"] = material
	state["lagoon_night_leaf_cards"] = cards
	var glass := Sprite2D.new()
	glass.name = "SkyLagoonCastleWindowMaterial"
	glass.texture = texture
	glass.centered = false
	glass.position = -castle.texture.get_size() * 0.5 + Vector2(58, 234)
	glass.z_index = 1
	glass.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	glass.modulate = Color(0.90 / castle.modulate.r, 0.95 / castle.modulate.g, 1.0 / castle.modulate.b, 1.0)
	castle.add_child(glass)
	state["lagoon_window_material_card"] = glass
	return true
