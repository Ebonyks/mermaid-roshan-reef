extends OperaGeologySurface
## Non-runtime visual pilot. All touch/progress/save behavior inherited.
var coherent_textures: Array[Texture2D] = []

func _load_textures() -> void:
	super._load_textures()
	if not coherent_textures.is_empty():
		return
	var file := FileAccess.open("res://assets_src/imagegen/geologist_geode_coherent_states_v1_20261002/SELECTED_PILOT_STATES.json",FileAccess.READ)
	var parsed: Dictionary = JSON.parse_string(file.get_as_text()) as Dictionary
	file.close()
	var source_cache: Dictionary = {}
	for raw: Dictionary in parsed["states"]:
		var path: String = "res://" + String(raw["path"])
		if not source_cache.has(path):
			var native_image := Image.load_from_file(path)
			assert(native_image != null and not native_image.is_empty())
			source_cache[path] = ImageTexture.create_from_image(native_image)
		var bounds: Array = raw["region"] as Array
		var texture := AtlasTexture.new()
		texture.atlas = source_cache[path] as Texture2D
		texture.region = Rect2(float(bounds[0]),float(bounds[1]),float(bounds[2]),float(bounds[3]))
		coherent_textures.append(texture)

func authored_state_index() -> int:
	if geode_pull <= 0.0:
		return 0
	return mini(6,1 + int(geode_pull / 20.0))

func _coherent_rect() -> Rect2:
	var texture := coherent_textures[authored_state_index()]
	var fit := Vector2(350.0 * texture.get_width() / float(texture.get_height()),350.0)
	return Rect2(Vector2(GEODE_RECT.get_center().x - fit.x * 0.5,GEODE_RECT.end.y - fit.y),fit)

func _geode_right_rect() -> Rect2:
	if coherent_textures.is_empty():
		return super._geode_right_rect()
	var pair := _coherent_rect()
	return Rect2(Vector2(pair.get_center().x,pair.position.y),Vector2(pair.size.x * 0.5,pair.size.y))

func _draw_geode() -> void:
	if coherent_textures.is_empty():
		return
	draw_texture_rect(coherent_textures[authored_state_index()],_coherent_rect(),false)
	if geode_pull <= 0.0:
		for index: int in range(GEODE_SEAM_SPOTS.size()):
			draw_circle(GEODE_SEAM_SPOTS[index],15.0,Color("#8ce6dd") if geode_seams[index] else Color("#ffe69a"))
