class_name FashionOutfitRenderer
extends RefCounted
## Closed 2D texture lookup. Saves contain IDs, never paths or textures.
const ROOT := "res://assets/fashion/outfits/"

static func character_for(source: String) -> String:
	var base: String = source.get_file().get_basename()
	for character_id: String in FashionDesigner.SOURCES:
		if base in FashionDesigner.SOURCES[character_id]:
			return character_id
	return ""

static func path(main: ReefMain, source: String, preview_id: String = "") -> String:
	return FashionSkinEngine.path(main, source, preview_id)

static func texture(main: ReefMain, source: Texture2D) -> Texture2D:
	return FashionSkinEngine.texture(main, source)

static func portrait(main: ReefMain, person: String, outfit_id: String = "") -> Texture2D:
	var entry: Dictionary = FashionDesigner.character(person)
	if entry.is_empty():
		return null
	var art: Texture2D = load(path(main, String(entry["source"]), outfit_id)) as Texture2D
	if person == "rumi":
		var first := AtlasTexture.new()
		first.atlas = art
		first.region = Rect2(0, 0, 256, 384)
		return first
	return art
