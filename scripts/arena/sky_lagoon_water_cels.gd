extends RefCounted
# Gameplay water taps; uses the approved eight-cel vocabulary without spatial FX.
const ATLAS := "res://assets/sprites/fx_water/fx_water_ripple_ring_atlas.png"
const MASK := "res://assets/sprites/sky_lagoon/animated_v1/water_surface_mask.png"
const CLIP := preload("res://shaders/sky_lagoon_water_clip.gdshader")
const MASTER := Vector2(6144, 2048)
const CAP := 3
const FRAME_S := 0.12
const LIFE_S := 0.96
const SIZE := Vector2(192, 192)

static func clear(state: Dictionary) -> void:
	for slot: Dictionary in state.get("lagoon_water_slots", []) as Array:
		var value: Variant = slot.get("node")
		if is_instance_valid(value) and value is Sprite2D:
			(value as Sprite2D).free()
	for key: String in ["lagoon_water_slots", "lagoon_water_mask_image", "lagoon_water_blockers", "lagoon_water_parent", "lagoon_water_cooldown", "lagoon_water_emit_count"]:
		state.erase(key)

static func build(state: Dictionary, parent: Node2D, version: String, blockers: Array[Sprite2D]) -> bool:
	clear(state)
	if version != "animated_v1" or not is_instance_valid(parent) or not ResourceLoader.exists(MASK):
		return false
	var atlas: Texture2D = load(ATLAS) as Texture2D
	var mask: Texture2D = load(MASK) as Texture2D
	if atlas == null or mask == null or atlas.get_size() != Vector2(1024, 512) or mask.get_size() != Vector2(1024, 512):
		return false
	var mask_image: Image = mask.get_image()
	if mask_image == null or mask_image.is_empty():
		return false
	var slots: Array[Dictionary] = []
	for index: int in range(CAP):
		var card := Sprite2D.new()
		card.name = "SkyLagoonWaterTap_%d" % index
		card.texture = atlas
		card.hframes = 4
		card.vframes = 2
		card.scale = SIZE / Vector2(256, 256)
		card.visible = false
		card.set_meta("source_owned", true)
		card.set_meta("canvas_layer_role", "water_surface_response")
		var material := ShaderMaterial.new()
		material.shader = CLIP
		material.set_shader_parameter("water_mask", mask)
		material.set_shader_parameter("sprite_size", SIZE)
		card.material = material
		parent.add_child(card)
		slots.append({"node": card, "time": -1.0})
	var occluders: Array[Dictionary] = []
	for card: Sprite2D in blockers:
		if not is_instance_valid(card) or card.texture == null:
			continue
		var texture: Texture2D = state.get("lagoon_bridge_original", card.texture) as Texture2D if card == state.get("lagoon_castle_card") else card.texture
		if texture != null:
			var blocker_image: Image = texture.get_image()
			if blocker_image != null and (card.hframes > 1 or card.vframes > 1):
				blocker_image = blocker_image.get_region(Rect2i(Vector2i.ZERO, Vector2i(texture.get_size() / Vector2(card.hframes, card.vframes))))
			occluders.append({"node": card, "image": blocker_image})
	state["lagoon_water_slots"] = slots
	state["lagoon_water_mask_image"] = mask_image
	state["lagoon_water_blockers"] = occluders
	state["lagoon_water_parent"] = parent
	state["lagoon_water_cooldown"] = 0.0
	state["lagoon_water_emit_count"] = 0
	return true

static func is_water(state: Dictionary, point: Vector2) -> bool:
	var mask: Image = state.get("lagoon_water_mask_image") as Image
	if mask == null or point.x < 0.0 or point.y < 0.0 or point.x >= MASTER.x or point.y >= MASTER.y:
		return false
	var pixel: Vector2i = Vector2i(point / MASTER * Vector2(mask.get_size()))
	if mask.get_pixelv(pixel).a < 0.85:
		return false
	var parent_value: Variant = state.get("lagoon_water_parent")
	if not is_instance_valid(parent_value):
		return false
	var parent: Node2D = parent_value as Node2D
	for blocker: Dictionary in state.get("lagoon_water_blockers", []) as Array:
		var value: Variant = blocker.get("node")
		if not is_instance_valid(value) or not value is Sprite2D:
			continue
		var card: Sprite2D = value as Sprite2D
		var image: Image = blocker.get("image") as Image
		if image == null or not card.is_visible_in_tree():
			continue
		var local: Vector2 = card.to_local(parent.to_global(point)) + Vector2(image.get_size()) * 0.5 - card.offset
		if Rect2(Vector2.ZERO, Vector2(image.get_size())).has_point(local) and image.get_pixelv(Vector2i(local)).a > 0.1:
			return false
	return true

static func tap(state: Dictionary, point: Vector2) -> bool:
	if not is_water(state, point):
		return false
	if not bool(state.get("lagoon_environment_motion_enabled", true)) or not bool(state.get("lagoon_water_motion_enabled", true)):
		return true
	if float(state.get("lagoon_water_cooldown", 0.0)) > 0.0:
		return true
	var slots: Array = state.get("lagoon_water_slots", []) as Array
	var chosen: Dictionary = slots[0] as Dictionary
	for slot: Dictionary in slots:
		if float(slot["time"]) < 0.0:
			chosen = slot
			break
		if float(slot["time"]) > float(chosen["time"]):
			chosen = slot
	var card: Sprite2D = chosen["node"] as Sprite2D
	if not is_instance_valid(card):
		return true
	chosen["time"] = 0.0
	card.position = point
	card.frame = 0
	card.modulate = Color(0.85, 0.97, 1.0, 0.75)
	card.visible = true
	var material: ShaderMaterial = card.material as ShaderMaterial
	material.set_shader_parameter("surface_center", point)
	material.set_shader_parameter("atlas_cell", Vector2.ZERO)
	state["lagoon_water_cooldown"] = 0.18
	state["lagoon_water_emit_count"] = int(state.get("lagoon_water_emit_count", 0)) + 1
	return true

static func tick(state: Dictionary, delta: float, paused: bool) -> void:
	if paused or not state.has("lagoon_water_slots"):
		return
	var step: float = clampf(delta, 0.0, 0.1)
	state["lagoon_water_cooldown"] = maxf(0.0, float(state.get("lagoon_water_cooldown", 0.0)) - step)
	var enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true)) and bool(state.get("lagoon_water_motion_enabled", true))
	for slot: Dictionary in state["lagoon_water_slots"] as Array:
		var value: Variant = slot.get("node")
		if not is_instance_valid(value) or not value is Sprite2D:
			continue
		var card: Sprite2D = value as Sprite2D
		var timer: float = float(slot["time"])
		if timer < 0.0:
			continue
		timer += step
		if timer >= LIFE_S or not enabled:
			card.visible = false
			card.modulate.a = 0.0
			slot["time"] = -1.0
			continue
		slot["time"] = timer
		card.frame = mini(7, int(timer / FRAME_S))
		card.modulate.a = 0.75 * (1.0 - smoothstep(0.60, LIFE_S, timer))
		var material: ShaderMaterial = card.material as ShaderMaterial
		material.set_shader_parameter("atlas_cell", Vector2(card.frame % 4, floori(float(card.frame) / 4.0)))
