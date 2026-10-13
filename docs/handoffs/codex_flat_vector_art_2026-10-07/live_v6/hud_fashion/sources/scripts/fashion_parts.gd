class_name FashionParts
extends RefCounted
## Independent clothing policy; durable choices and transient texture cache stay on main.
const PEOPLE: Array[String] = ["roshan", "rumi", "daddy_mermaid"]
const SLOTS: Array[String] = ["head", "body", "tail"]
const CATALOG: FashionSkinCatalog = preload("res://assets/fashion/slots_v1/catalog.tres")

static func definition(id: String) -> Dictionary:
	for entry: Dictionary in CATALOG.data.get("items", []):
		if String(entry["id"]) == id:
			return entry.duplicate(true)
	return {}

static func fits(item: Dictionary, person: String) -> bool:
	var owner: String = String(item.get("character", ""))
	return owner == person or (owner == "*" and person in PEOPLE)

static func raw_parts(main: ReefMain, person: String) -> Dictionary:
	var raw: Variant = main.character_clothing_parts.get(person, {})
	return (raw as Dictionary).duplicate(true) if raw is Dictionary else {}

static func selected(main: ReefMain, person: String, slot: String) -> String:
	var fallback: String = person + "_original" if slot == "body" else slot + "_original"
	var legacy: Variant = main.character_outfits.get(person, fallback) if slot == "body" else fallback
	var raw: Variant = raw_parts(main, person).get(slot, legacy)
	if raw is String:
		var item: Dictionary = FashionDesigner.outfit(String(raw))
		if fits(item, person) and String(item.get("slot", "body")) == slot and FashionDesigner.owned(main, String(raw)):
			return String(raw)
	# Presentation fallback never overwrites a future slot, ID or character.
	return fallback

static func selections(main: ReefMain, person: String) -> Dictionary:
	var result: Dictionary = {}
	for slot: String in SLOTS:
		result[slot] = selected(main, person, slot)
	return result

static func items(person: String, slot: String) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	if slot == "body":
		result = FashionSkinEngine.outfits(person)
	for entry: Dictionary in CATALOG.data.get("items", []):
		if fits(entry, person) and String(entry["slot"]) == slot:
			result.append(entry.duplicate(true))
	result.sort_custom(func(a: Dictionary,b: Dictionary) -> bool: return _rank(a) < _rank(b))
	return result

static func _rank(item: Dictionary) -> int:
	var kinds: Array[String] = ["original","royal","pearl","ribbon","party","garden","disguise","star","blossom","winter","strawberry","chef","painter"]
	return kinds.find(String(item["kind"]))

static func refresh_unlocks(main: ReefMain) -> void:
	for item: Dictionary in CATALOG.data.get("items", []):
		var theme: String = String(item.get("kind", ""))
		var earned: bool = (main.chapter2_farmer_strawberries_ready or (main.opera_stars & (1 << ChapterTwoDirector.ACT_FARMER)) != 0 or FashionDesigner.owned(main,"roshan_garden_v1")) if theme == "strawberry" else false
		if theme == "chef": earned = main.chapter2_chef_cake_baked or (main.opera_stars & (1 << ChapterTwoDirector.ACT_CHEF)) != 0
		if theme == "painter": earned = (main.opera_stars & (1 << ChapterTwoDirector.ACT_PAINTER)) != 0
		if earned:
			FashionDesigner.grant(main, String(item["id"]))

static func composed_path(main: ReefMain, spec: Dictionary, base: String, preview_id: String = "", preview_parts: Dictionary = {}) -> String:
	var person: String = String(spec["character"])
	if person not in PEOPLE:
		return base
	var parts: Dictionary = selections(main, person)
	if not preview_id.is_empty():
		parts = {"head":"head_original", "body":preview_id, "tail":"tail_original"}
	if not preview_parts.is_empty(): parts = preview_parts
	var body: Dictionary = FashionDesigner.outfit(String(parts["body"]))
	var body_base: String = String((spec["variants"] as Dictionary).get(String(body.get("kind", "original")), base)) if definition(String(parts["body"])).is_empty() else base
	var layers: Dictionary = (CATALOG.data.get("layers", {}) as Dictionary).get(String(spec["family_id"]), {}) as Dictionary
	var active: Array[String] = []
	for slot: String in SLOTS:
		var id: String = String(parts[slot])
		if layers.has(id): active.append(String(layers[id]))
	if active.is_empty():
		return body_base
	var key: String = String(spec["family_id"]) + ("_preview" if not preview_id.is_empty() or not preview_parts.is_empty() else "")
	var signature: String = (body_base + str(active)).sha256_text()
	var cached: Dictionary = main.fashion_composed_textures.get(key, {}) as Dictionary
	if String(cached.get("signature", "")) == signature:
		return (cached["texture"] as Texture2D).resource_path
	var started: int = Time.get_ticks_usec()
	var original: Texture2D = load(body_base) as Texture2D
	var image: Image = original.get_image()
	if image.is_compressed() and image.decompress() != OK:
		push_error("Cannot decompress wardrobe source: " + body_base)
		return body_base
	image.convert(Image.FORMAT_RGBA8)
	for layer_path: String in active:
		var layer_texture: Texture2D = load(layer_path) as Texture2D
		var layer: Image = layer_texture.get_image()
		if layer.is_compressed() and layer.decompress() != OK:
			push_error("Cannot decompress wardrobe layer: " + layer_path)
			return body_base
		layer.convert(Image.FORMAT_RGBA8)
		image.blend_rect(layer, Rect2i(Vector2i.ZERO, layer.get_size()), Vector2i.ZERO)
	var texture: ImageTexture = ImageTexture.create_from_image(image)
	var path: String = "res://assets/fashion/slots_v1/cache/" + String(spec["family_id"]) + "/" + signature + "-" + str(texture.get_instance_id()) + ".tres"
	texture.take_over_path(path) # Unique live path keeps an identical goal preview from stealing a bound texture path.
	main.fashion_composed_textures[key] = {"signature":signature,"texture":texture,"bytes":image.get_data_size(),"compose_usec":Time.get_ticks_usec()-started}
	# One current mix per family and one explicit goal preview; no Cartesian atlas cache.
	return path

static func icon(id: String) -> Texture2D:
	var garment: Texture2D = FashionSkinEngine.garment(id)
	if garment != null:
		return garment
	return load("res://assets/fashion/slots_v1/items/original_return.png") as Texture2D

static func face(main: ReefMain, person: String) -> Texture2D:
	var picture: Texture2D = FashionOutfitRenderer.portrait(main, person, person + "_original")
	var bounds: Rect2 = Rect2(106,12,109,88) if person == "roshan" else (Rect2(82,10,122,104) if person == "rumi" else Rect2(278,0,209,204))
	var cropped := AtlasTexture.new()
	cropped.atlas = picture
	cropped.region = bounds
	return cropped

static func goal(main: ReefMain, person: String, parts: Dictionary) -> Texture2D:
	var spec: Dictionary = FashionSkinEngine.family(String(FashionDesigner.character(person)["source"]))
	var base: String = String((spec["variants"] as Dictionary).get("original","res://"+String(spec["source"])))
	var picture: Texture2D = load(composed_path(main,spec,base,"",parts)) as Texture2D
	if person == "rumi":
		var cropped := AtlasTexture.new()
		cropped.atlas = picture
		cropped.region = Rect2(0,0,256,384)
		return cropped
	return picture
