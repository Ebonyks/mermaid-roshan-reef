extends SceneTree
## Enumerate Bubble Duel's reachable wardrobe art through the production resolver.
## The receipt binds atlas regions and actual attachment pixels, not a visual score.
const Cast := preload("res://scripts/bubble_duel_cast.gd")
const Shop := preload("res://scripts/bubble_duel_inventory.gd")
const Duel := preload("res://scripts/opera_bubble_duel.gd")

var images: Dictionary = {}
var bindings: Array[Dictionary] = []
var fits: Array[Dictionary] = []
var failed := false
var active_texture: Texture2D
var active_bitmap: Image
var active_digest := ""
var output := OS.get_environment("DUEL_IMAGE_AUDIT_DIR")


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	if output.is_empty() or not DirAccess.dir_exists_absolute(output):
		printerr("DUEL_IMAGE|output directory required")
		quit(2)
		return
	var main := ReefMain.new()
	var owned: Array[String] = []
	for gear: Dictionary in Shop.ITEMS:
		owned.append(String(gear["id"]))
	main.save_data[Shop.SAVE_KEY] = {"owned": owned}
	var appearance := Cast.new(main)
	var item_bitmap := Duel.ITEMS.get_image()
	if item_bitmap.is_compressed(): item_bitmap.decompress()
	var originals := {}
	for person: Dictionary in Cast.ROSTER:
		for kind: String in ["rest", "swim"]:
			var path := String(person[kind])
			originals[path] = _decoded_hash(load(path) as Texture2D)
	for person: String in Cast.PEOPLE:
		for outfit: Dictionary in FashionParts.items(person, "body"):
			main.outfits_unlocked[String(outfit["id"])] = true
		var looks: Dictionary = {}
		for look: Dictionary in Shop.looks(main, person):
			looks[String(look["id"])] = true
		# The shop renders every set for the chosen person, even when the body
		# is the original and only the purchased prop is worn.
		for gear: String in owned:
			looks["set:" + gear] = true
		for look: String in looks:
			for moving: bool in [false, true]:
				var profile := {"character": person, "look": look, "gear": "classic"}
				var art: Texture2D = appearance.texture(profile, moving)
				var rate := 15 if person == "roshan" else (6 if person == "rumi" else 5)
				var count := 4 if person == "rumi" else (int(Cast.character(person)["frames"]) if moving else 1)
				for key: int in range(count):
					var clock := (float(key) + 0.01) / float(rate)
					var frame := appearance.frame(profile, moving, clock)
					var role := "%s/%s/%s/%d" % [person, look, "swim" if moving else "rest", key]
					var bitmap: Image = _register(role, art, Rect2i(frame["region"]))
					if bitmap == null: continue
					for gear: String in owned:
						if gear == "classic": continue
						profile["gear"] = gear
						var fit := appearance.attachment(profile, moving, clock)
						var socket: Vector2 = fit["socket"]
						var point := (frame["anchor"] as Vector2) + socket / float(frame["factor"])
						var pixel := Vector2i(point.round())
						var alpha := bitmap.get_pixelv(pixel).a if Rect2i(Vector2i.ZERO, bitmap.get_size()).has_point(pixel) else 0.0
						var worn: Rect2 = fit["rect"]
						var pin := Vector2i(((socket - worn.position) / worn.size * 256.0).round()).clamp(Vector2i.ZERO, Vector2i(255, 255))
						var item_pixel := _cell(int(fit["icon"])).position + pin
						var item_alpha := item_bitmap.get_pixelv(item_pixel).a
						if alpha < 0.65 or item_alpha < 0.65: failed = true
						fits.append({"role": role, "gear": gear, "socket": [pixel.x, pixel.y], "alpha": alpha,
							"item_pin": [pin.x, pin.y], "item_alpha": item_alpha})
	var shared := {
		"pearl_stock_reward_projectile_pickup": Duel.PEARL,
		"touch_pointer": Duel.HAND,
		"painted_button_surface": StorybookUI.NAVIGATION_CARD_TEXTURE,
		"wardrobe_shortcut": preload("res://assets/fashion/skin_engine_v2/garments/party.png"),
	}
	for row: int in range(2):
		for column: int in range(4):
			var tile := load(Duel.POOL_TILE_PATH % [row, column]) as Texture2D
			_register("arena_tile/%d/%d" % [row, column], tile, Rect2i(Vector2i.ZERO, Vector2i(Duel.POOL_TILE_SIZE)))
	for role: String in shared:
		var texture: Texture2D = shared[role]
		_register(role, texture, Rect2i(Vector2i.ZERO, Vector2i(texture.get_size())))
	_register("bubble_base_all_five_tints", Duel.BUBBLES, Rect2i(Duel.BUBBLE_REGION))
	for index: int in range(7):
		_register("item/" + String(Shop.ITEMS[index + 1]["id"]), Duel.ITEMS, _cell(index))
	for key: int in range(8):
		_register("bubble_pop/" + str(key), Duel.POP, _cell(key))
	var original_checks := {}
	for path: String in originals:
		var after := _decoded_hash(load(path) as Texture2D)
		original_checks[path] = {"before": originals[path], "after": after}
		if after != String(originals[path]):
			printerr("DUEL_IMAGE|decoded original was mutated ", path)
			failed = true
	var original_profile := {"character": "roshan", "look": "set:classic"}
	var moon_profile := {"character": "roshan", "look": "set:moonpearl"}
	for moving: bool in [false, true]:
		if _decoded_hash(appearance.texture(original_profile, moving)) == _decoded_hash(appearance.texture(moon_profile, moving)):
			printerr("DUEL_IMAGE|Moonpearl resolved to Original moving=", moving)
			failed = true
	var result := FileAccess.open(output.path_join("inventory.json"), FileAccess.WRITE)
	if result == null:
		quit(3)
		return
	result.store_string(JSON.stringify({"engine": Engine.get_version_info(), "images": images,
		"bindings": bindings, "fits": fits, "originals": original_checks, "failed": failed}, "\t") + "\n")
	result.close()
	appearance = null
	main.free()
	print("DUEL_IMAGE|", images.size(), " bitmaps, ", bindings.size(), " regions, ", fits.size(), " fits")
	quit(1 if failed else 0)


func _cell(index: int) -> Rect2i:
	return Rect2i((index % 4) * 256, (index / 4) * 256, 256, 256)


func _register(role: String, texture: Texture2D, region: Rect2i) -> Image:
	if texture == null:
		printerr("DUEL_IMAGE|missing texture ", role)
		failed = true
		return null
	if active_texture != texture:
		active_texture = texture
		active_bitmap = texture.get_image()
		if active_bitmap == null or (active_bitmap.is_compressed() and active_bitmap.decompress() != OK):
			printerr("DUEL_IMAGE|unreadable texture ", role)
			failed = true
			return null
		active_bitmap.convert(Image.FORMAT_RGBA8)
		var hash := HashingContext.new()
		hash.start(HashingContext.HASH_SHA256)
		hash.update(active_bitmap.get_data())
		active_digest = hash.finish().hex_encode()
	var bitmap := active_bitmap
	if not Rect2i(Vector2i.ZERO, bitmap.get_size()).encloses(region):
		printerr("DUEL_IMAGE|region outside texture ", role)
		failed = true
		return null
	var pixels := bitmap.get_region(region)
	if not pixels.get_used_rect().has_area():
		printerr("DUEL_IMAGE|empty texture region ", role)
		failed = true
	var digest := active_digest
	var path := texture.resource_path
	var source_sha := FileAccess.get_sha256(path) if FileAccess.file_exists(path) else ""
	if not images.has(digest):
		var filename := digest + ".png"
		if bitmap.save_png(output.path_join(filename)) != OK:
			failed = true
		images[digest] = {"bitmap": filename, "width": bitmap.get_width(), "height": bitmap.get_height()}
	bindings.append({"role": role, "rgba_sha256": digest, "resource": path, "source_sha256": source_sha,
		"region": [region.position.x, region.position.y, region.size.x, region.size.y]})
	return pixels


func _decoded_hash(texture: Texture2D) -> String:
	var bitmap: Image = texture.get_image().duplicate()
	if bitmap.is_compressed(): bitmap.decompress()
	bitmap.convert(Image.FORMAT_RGBA8)
	var hash := HashingContext.new()
	hash.start(HashingContext.HASH_SHA256)
	hash.update(bitmap.get_data())
	return hash.finish().hex_encode()
