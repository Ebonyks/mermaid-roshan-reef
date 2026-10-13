class_name FashionSkinEngine
extends RefCounted
## Shared Godot texture adapter. Authored definitions are immutable resources;
## chosen outfits/progress remain on ReefMain and its transactional save.
const CATALOG: FashionSkinCatalog = preload("res://assets/fashion/skin_engine_v2/catalog.tres")

static func outfit(id: String) -> Dictionary:
	var entries: Array = CATALOG.data.get("outfits", []) as Array
	for raw: Variant in entries:
		if raw is Dictionary and String(raw.get("id", "")) == id:
			return (raw as Dictionary).duplicate(true)
	return FashionParts.definition(id)

static func outfits(person: String) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	var entries: Array = CATALOG.data.get("outfits", []) as Array
	for raw: Variant in entries:
		if raw is Dictionary and String(raw.get("character", "")) == person:
			result.append((raw as Dictionary).duplicate(true))
	return result

static func family(source: String) -> Dictionary:
	var entries: Dictionary = CATALOG.data.get("families", {}) as Dictionary
	for key: String in entries:
		var entry: Dictionary = entries[key] as Dictionary
		if "res://" + String(entry.get("source", "")) == source or source.begins_with("res://assets/fashion/slots_v1/cache/" + key + "/"):
			var bound: Dictionary = entry.duplicate(true)
			bound["family_id"] = key
			return bound
		var variants: Dictionary = entry.get("variants", {}) as Dictionary
		for kind: String in variants:
			if String(variants[kind]) == source:
				var bound: Dictionary = entry.duplicate(true)
				bound["family_id"] = key
				return bound
	return {}

static func path(main: ReefMain, source: String, preview_id: String = "") -> String:
	if main == null:
		return source
	var spec: Dictionary = family(source)
	if spec.is_empty():
		return source
	var base: String = String((spec.get("variants", {}) as Dictionary).get("original","res://" + String(spec["source"])))
	var person: String = String(spec["character"])
	if person in FashionParts.PEOPLE:
		return FashionParts.composed_path(main, spec, base, preview_id)
	var id: String = preview_id if not preview_id.is_empty() else FashionDesigner.selected(main, person)
	var outfit: Dictionary = FashionDesigner.outfit(id)
	if String(outfit.get("character", "")) != person:
		return base
	var kind: String = String(outfit.get("kind", "original"))
	var variants: Dictionary = spec.get("variants", {}) as Dictionary
	var chosen: String = String(variants.get(kind, base))
	# Paths only come from the authored resource, never reef_save.json.
	if not ResourceLoader.exists(chosen):
		return base
	var art: Texture2D = load(chosen) as Texture2D
	var dimensions: Array = spec["dimensions"] as Array
	if art == null or art.get_width() != int(dimensions[0]) or art.get_height() != int(dimensions[1]):
		return base
	return chosen

static func texture(main: ReefMain, source: Texture2D, person: String = "") -> Texture2D:
	if source == null:
		return null
	if source is AtlasTexture:
		var old: AtlasTexture = source as AtlasTexture
		var replacement: Texture2D = texture(main, old.atlas, person)
		if replacement == old.atlas:
			return old
		var atlas: AtlasTexture = old.duplicate() as AtlasTexture
		atlas.atlas = replacement
		return atlas
	var spec: Dictionary = family(source.resource_path)
	if spec.is_empty() or (not person.is_empty() and String(spec["character"]) != person):
		return source
	var selected_path: String = path(main, source.resource_path)
	return source if selected_path == source.resource_path else load(selected_path) as Texture2D

static func garment(id: String) -> Texture2D:
	var definition: Dictionary = FashionDesigner.outfit(id)
	var source: String = String(definition.get("garment", ""))
	return load(source) as Texture2D if not source.is_empty() and ResourceLoader.exists(source) else null

static func fit_rect(person: String, preview: TextureRect, slot: String = "body") -> Rect2:
	var character: Dictionary = FashionDesigner.character(person)
	var spec: Dictionary = family(String(character.get("source", "")))
	if spec.is_empty() or preview.texture == null:
		return Rect2(preview.position,preview.size)
	var boxes: Array = spec["boxes"] as Array
	var b: Array = boxes[0] as Array
	var fits: Dictionary = (FashionParts.CATALOG.data.get("fits", {}) as Dictionary).get(String(spec.get("family_id", "")), {}) as Dictionary
	if fits.has(slot): b = (fits[slot] as Array)[0] as Array
	var dimensions: Vector2 = preview.texture.get_size()
	var scale: float = minf(preview.size.x / dimensions.x,preview.size.y / dimensions.y)
	var offset: Vector2 = preview.position + (preview.size - dimensions * scale) * 0.5
	var box := Rect2(offset + Vector2(float(b[0]),float(b[1])) * scale,Vector2(float(b[2])-float(b[0]),float(b[3])-float(b[1])) * scale)
	# Generous target remains attached to the pictured torso at every aspect.
	return Rect2(box.get_center()-Vector2(75,75),Vector2(150,150))

static func animation_frames(main: ReefMain, source: SpriteFrames) -> SpriteFrames:
	# Bind a private resource BEFORE assigning/playing an AnimatedSprite2D.
	# Godot's SpriteFrames setter stops playback and resets its custom speed;
	# live wardrobe changes therefore edit frame textures in this owned copy.
	if source == null:
		return null
	var bound: SpriteFrames = source.duplicate() as SpriteFrames
	bound.set_meta("fashion_skin_instance", true)
	for raw_name: String in bound.get_animation_names():
		var name := StringName(raw_name)
		for index: int in range(bound.get_frame_count(name)):
			bound.set_frame(name,index,texture(main,source.get_frame_texture(name,index)),source.get_frame_duration(name,index))
	return bound

static func _animated(main: ReefMain, sprite: AnimatedSprite2D, person: String) -> void:
	var current: SpriteFrames = sprite.sprite_frames
	if current == null or not bool(current.get_meta("fashion_skin_instance",false)):
		return # Unregistered animations are never rewritten or stopped.
	for raw_name: String in current.get_animation_names():
		var name := StringName(raw_name)
		for index: int in range(current.get_frame_count(name)):
			var previous: Texture2D = current.get_frame_texture(name,index)
			var changed: Texture2D = texture(main,previous,person)
			if changed != previous:
				current.set_frame(name,index,changed,current.get_frame_duration(name,index))

static func refresh(main: ReefMain, person: String = "") -> void:
	if main == null:
		return
	var pending: Array[Node] = [main]
	while not pending.is_empty():
		var node: Node = pending.pop_back() as Node
		if bool(node.get_meta("fashion_fixed_preview", false)) or bool(node.get_meta("fashion_temporary_costume", false)):
			continue
		if node is AnimatedSprite2D:
			_animated(main, node as AnimatedSprite2D, person)
		else:
			# Existing Canvas portraits and legacy texture consumers use the same
			# adapter; no node, transform, animation or world logic is rebuilt.
			for property: Dictionary in node.get_property_list():
				if String(property["name"]) != "texture":
					continue
				var original: Texture2D = node.get("texture") as Texture2D
				var changed: Texture2D = texture(main, original, person)
				if changed != original:
					node.set("texture", changed)
				break
		for child: Node in node.get_children():
			pending.append(child)
