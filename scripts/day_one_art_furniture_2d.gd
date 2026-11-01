class_name DayOneArtFurniture2D
extends RefCounted
## Whole dirty/clean furniture cards. Original room cards are hidden exactly
## once for this visit and restored on teardown; saved state remains on main.

const ROOT := "res://assets/castle/day_one_art_studio/furniture/"
const FIXTURES := {
	"left_counter": {"asset": "left_counter", "rect": Rect2(0, 312, 256, 232),
		"contact_uv": Vector2(0.62, 0.34), "z": 400},
	"desk_counter": {"asset": "paint_table", "rect": Rect2(400, 260, 224, 102),
		"contact_uv": Vector2(0.50, 0.40), "z": 200},
	"right_counter": {"asset": "right_counter", "rect": Rect2(720, 300, 304, 250),
		"contact_uv": Vector2(0.45, 0.37), "z": 400},
}
const WIPE_SHADER := """
shader_type canvas_item;
render_mode unshaded;
uniform sampler2D clean_texture : source_color, filter_linear_mipmap;
uniform float clean_progress : hint_range(0.0, 1.0) = 0.0;
void fragment() {
	vec4 dirty = texture(TEXTURE, UV);
	vec4 clean = texture(clean_texture, UV);
	float wipe = 1.0 - smoothstep(clean_progress - 0.025,
		clean_progress + 0.025, UV.x);
	if (clean_progress <= 0.0) { wipe = 0.0; }
	if (clean_progress >= 1.0) { wipe = 1.0; }
	COLOR = mix(dirty, clean, wipe);
}
"""
var cards: Dictionary = {}
var hidden_cards: Array[Dictionary] = []
var layer: Node2D


func setup(main: ReefMain, canvas_scale: float) -> void:
	layer = Node2D.new()
	layer.name = "StudioFurnitureStates"
	main.castle_room_world_root.add_child(layer)
	for item_id: String in ["paint_table", "palette"]:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {})
		_hide(record.get("sprite") as CanvasItem)
	if main.castle_room_front_layer != null:
		for child: Node in main.castle_room_front_layer.get_children():
			if String(child.name) in ["room_craft_room_front_left",
					"room_craft_room_front_right"]:
				_hide(child as CanvasItem)
	var shader := Shader.new()
	shader.code = WIPE_SHADER
	for grime_id: String in FIXTURES:
		var spec: Dictionary = FIXTURES[grime_id] as Dictionary
		var asset_id := String(spec["asset"])
		var dirty: Texture2D = load(ROOT + asset_id + "_dirty.png") as Texture2D
		var clean: Texture2D = load(ROOT + asset_id + "_clean.png") as Texture2D
		var rect: Rect2 = spec["rect"] as Rect2
		var card := Sprite2D.new()
		card.name = "StudioFixture_" + grime_id
		card.texture = dirty
		card.position = rect.get_center() * canvas_scale
		card.scale = rect.size * canvas_scale / dirty.get_size()
		card.z_index = int(spec["z"])
		card.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
		var material := ShaderMaterial.new()
		material.shader = shader
		material.set_shader_parameter("clean_texture", clean)
		card.material = material
		card.set_meta("studio_surface_id", grime_id)
		layer.add_child(card)
		cards[grime_id] = card


func contact(grime_id: String) -> Vector2:
	var spec: Dictionary = FIXTURES.get(grime_id, {}) as Dictionary
	if spec.is_empty():
		return Vector2.ZERO
	var rect: Rect2 = spec["rect"] as Rect2
	return rect.position + rect.size * (spec["contact_uv"] as Vector2)


func scrub_start(grime_id: String) -> Vector2:
	var spec: Dictionary = FIXTURES[grime_id] as Dictionary
	var rect: Rect2 = spec["rect"] as Rect2
	return Vector2(rect.position.x, contact(grime_id).y)


func scrub_end(grime_id: String) -> Vector2:
	var spec: Dictionary = FIXTURES[grime_id] as Dictionary
	var rect: Rect2 = spec["rect"] as Rect2
	return Vector2(rect.end.x, contact(grime_id).y)


func set_progress(grime_id: String, value: float) -> void:
	var card: Sprite2D = cards.get(grime_id) as Sprite2D
	if card != null:
		(card.material as ShaderMaterial).set_shader_parameter(
			"clean_progress", clampf(value, 0.0, 1.0))


func refresh(cleaned: Dictionary) -> void:
	for grime_id: String in cards:
		set_progress(grime_id, 1.0 if bool(cleaned.get(grime_id, false)) else 0.0)


func teardown() -> void:
	if layer != null and is_instance_valid(layer):
		layer.queue_free()
	layer = null
	cards.clear()
	for record: Dictionary in hidden_cards:
		var original: CanvasItem = record.get("node") as CanvasItem
		if is_instance_valid(original):
			original.visible = bool(record["visible"])
	hidden_cards.clear()


func _hide(item: CanvasItem) -> void:
	if item == null:
		return
	hidden_cards.append({"node": item, "visible": item.visible})
	item.visible = false
