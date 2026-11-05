class_name BubbleDuelCast
extends RefCounted
## Closed existing-art roster. The same geometry draws previews, worn gear and play.

const Shop := preload("res://scripts/bubble_duel_inventory.gd")
const ICONS := preload("res://assets/opera/bubble_duel_v2/items.png")
const ITEM_PINS: Array[Vector2] = [Vector2(0.851562, 0.238281), Vector2(0.500000, 0.500000), Vector2(0.519531, 0.871094), Vector2(0.269531, 0.781250), Vector2(0.500000, 0.500000), Vector2(0.500000, 0.500000), Vector2(0.550781, 0.121094), Vector2(0.500000, 0.500000)]
const PEOPLE: Array[String] = ["roshan", "rumi", "daddy_mermaid", "baby_eagle", "rainbow_dust_bunny", "marlo"]
const ROSTER: Array[Dictionary] = [
	{"id": "roshan", "name": "Roshan", "rest": "res://assets/characters/roshan_25d/roshan_base.png", "swim": "res://assets/characters/roshan_25d/roshan_swim_front.png", "cell": Vector2(256, 256), "columns": 4, "frames": 16},
	{"id": "rumi", "name": "Rumi", "rest": "res://assets/characters/rumi/rumi_pool_idle_swim_atlas.png", "swim": "res://assets/characters/rumi/rumi_pool_idle_swim_atlas.png", "cell": Vector2(256, 256), "columns": 4, "frames": 4},
	{"id": "daddy_mermaid", "name": "Daddy", "rest": "res://assets/fashion/skin_engine_v2/atlases/daddy_original.png", "swim": "res://assets/fashion/skin_engine_v2/atlases/daddy_original.png", "cell": Vector2(727, 1024), "columns": 1, "frames": 1},
	{"id": "baby_eagle", "name": "Baby Eagle", "rest": "res://assets/characters/companions/baby_eagle.png", "swim": "res://assets/characters/companions/baby_eagle.png", "cell": Vector2(290, 512), "columns": 1, "frames": 1},
	{"id": "rainbow_dust_bunny", "name": "Rainbow Friend", "rest": "res://assets/sprites/dust_bunnies/rainbow_friend.png", "swim": "res://assets/sprites/dust_bunnies/rainbow_friend.png", "cell": Vector2(512, 512), "columns": 1, "frames": 1},
	{"id": "marlo", "name": "Marlo", "rest": "res://assets/opera/bubble_duel_v2/marlo_swim.png", "swim": "res://assets/opera/bubble_duel_v2/marlo_swim.png", "cell": Vector2(256, 256), "columns": 2, "frames": 4},
]

var main: ReefMain
var textures: Dictionary = {}
var icons: Array[AtlasTexture] = []
var contacts: Dictionary = {}
var source_images: Dictionary = {}
var socket_cache: Dictionary = {}


func _init(owner_main: ReefMain) -> void:
	main = owner_main
	for index: int in range(8):
		var icon := AtlasTexture.new()
		icon.atlas = ICONS
		icon.region = Rect2((index % 4) * 256, (index / 4) * 256, 256, 256)
		icon.filter_clip = true
		icons.append(icon)


static func character(id: String) -> Dictionary:
	for entry: Dictionary in ROSTER:
		if entry["id"] == id:
			return entry
	return ROSTER[0]


func texture(profile: Dictionary, moving: bool) -> Texture2D:
	var person := String(profile.get("character", "roshan"))
	var entry := character(person)
	var source := String(entry["swim"] if moving else entry["rest"])
	var look := String(profile.get("look", "set:classic"))
	var key := source + ":" + look
	if textures.has(key):
		return textures[key] as Texture2D
	var path := source
	if person != "marlo":
		var spec := FashionSkinEngine.family(source)
		var outfit_id := look
		var parts := {"head": "head_original", "body": person + "_original", "tail": "tail_original"}
		if look.begins_with("set:"):
			var gear_id := look.trim_prefix("set:")
			var costume := String(Shop.item(gear_id)["outfit"])
			var kind := "original"
			if gear_id == "tidewing": kind = "ribbon"
			if gear_id == "moonpearl": kind = "party"
			if gear_id == "swiftconch": kind = "garden"
			if person in FashionParts.PEOPLE and costume in ["star", "blossom", "winter", "magician"]:
				parts = {"head": "head_" + costume + "_v1", "body": "body_" + costume + "_v1", "tail": "tail_original"}
			else:
				parts["body"] = person + "_" + kind + ("" if kind == "original" else "_v1")
			outfit_id = String(parts["body"])
		else:
			parts["body"] = look
		if person in FashionParts.PEOPLE:
			path = FashionParts.composed_path(main, spec, source, "", parts)
		else:
			path = FashionSkinEngine.path(main, source, outfit_id)
	var art: Texture2D = load(path) as Texture2D
	textures[key] = art
	if textures.size() > 16:
		textures.erase(textures.keys()[0])
	return art


func frame(profile: Dictionary, moving: bool, clock: float) -> Dictionary:
	var person := String(profile.get("character", "roshan"))
	var entry := character(person)
	var index := 0
	if person == "roshan" and moving: index = int(clock * 15.0) % 16
	if person == "rumi": index = (4 if moving else 0) + int(clock * 6.0) % 4
	if person == "marlo" and moving: index = int(clock * 5.0) % 4
	var source := String(entry["swim"] if moving else entry["rest"])
	var cell: Vector2 = entry["cell"]
	var columns := int(entry["columns"]) if (moving or person in ["rumi", "marlo"]) else 1
	var region := Rect2(Vector2((index % columns) * cell.x, (index / columns) * cell.y), cell)
	var spec := FashionSkinEngine.family(source)
	var body := Rect2(85, 86, 77, 74)
	if not spec.is_empty():
		var boxes: Array = spec["boxes"]
		var b: Array = boxes[mini(index, boxes.size() - 1)]
		body = Rect2(float(b[0]), float(b[1]), float(b[2]) - float(b[0]), float(b[3]) - float(b[1]))
	var anchor := cell * 0.5
	if person == "roshan" and moving: anchor = RoshanSpriteAnchors.anchor("swim_front", index)
	if person == "rumi": anchor = Vector2(body.get_center().x, body.end.y)
	if person == "daddy_mermaid": anchor = Vector2(388, 480)
	if person == "marlo": body = Rect2(84, 112, 90, 38)
	if person == "baby_eagle": body = Rect2(125, 245, 70, 85)
	if person == "rainbow_dust_bunny": body = Rect2(210, 405, 90, 75)
	var factor := 154.0 / maxf(cell.x, cell.y)
	return {"source": source, "region": region, "index": index, "anchor": anchor, "factor": factor, "body": body, "cell": cell}


func contact(profile: Dictionary, moving: bool, clock: float) -> Vector2:
	var spec := frame(profile, moving, clock)
	var key := String(spec["source"]) + ":" + str(spec["index"])
	if not contacts.has(key):
		# Source alpha is inspected once, never modified; contact stays on visible paint.
		var image := _source_image(String(spec["source"]))
		var region: Rect2 = spec["region"]
		var point := Vector2.ZERO
		var found := false
		var last_y := int(region.size.y) - 1
		while last_y >= 0 and not found:
			var xs: Array[int] = []
			for x: int in range(int(region.size.x)):
				if image.get_pixel(int(region.position.x) + x, int(region.position.y) + last_y).a > 0.65:
					xs.append(x)
			if xs.size() >= 3:
				point = Vector2(xs[xs.size() / 2], last_y)
				found = true
			last_y -= 1
		if String(profile.get("character", "roshan")) == "roshan" and not moving:
			point = Vector2(128.0 - 31.0 * 256.0 / 154.0, 128.0 + 49.0 * 256.0 / 154.0)
		contacts[key] = point
	return ((contacts[key] as Vector2) - (spec["anchor"] as Vector2)) * float(spec["factor"])


func attachment(profile: Dictionary, moving: bool, clock: float) -> Dictionary:
	var gear := String(profile.get("gear", "classic"))
	if gear == "classic": return {}
	var spec := frame(profile, moving, clock)
	var body: Rect2 = spec["body"]
	var factor := float(spec["factor"])
	body = Rect2((body.position - (spec["anchor"] as Vector2)) * factor, body.size * factor)
	var fit := clampf(body.size.x / 22.0, 0.85, 1.3)
	if String(profile.get("character", "")) in ["rainbow_dust_bunny", "marlo"]: fit *= 0.65
	var center := body.get_center()
	var span := Vector2(27, 27) * fit
	var pivot := Vector2(0.5, 0.5)
	var behind := false
	match gear:
		"tidewing":
			center = body.position + body.size * Vector2(0.2, 0.2)
			span = Vector2(52, 60) * fit
			pivot = ITEM_PINS[0]
			behind = false
			if String(profile.get("character", "")) == "rainbow_dust_bunny":
				center = (Vector2(110, 300) - (spec["anchor"] as Vector2)) * factor
		"moonpearl":
			center.y -= 2.0
		"swiftconch":
			center = Vector2(body.position.x - 8, body.get_center().y + 3)
			span = Vector2(39, 44) * fit
			pivot = Vector2(0.9, 0.5)
			behind = true
			match String(profile.get("character", "")):
				"baby_eagle": center = (Vector2(110, 290) - (spec["anchor"] as Vector2)) * factor
				"rainbow_dust_bunny": center = (Vector2(55, 400) - (spec["anchor"] as Vector2)) * factor
				"marlo":
					center = (Vector2(122, 112) - (spec["anchor"] as Vector2)) * factor
					pivot = ITEM_PINS[2]
		"rainbow":
			# A belt/wing-harness holster is honest even for portraits with no free hand.
			center = Vector2(body.end.x - 2, body.end.y - 3)
			span = Vector2(39, 60) * fit
			pivot = ITEM_PINS[3]
		"kelp":
			center.y += 4.0
			span = Vector2(44, 46) * fit
		"lullaby":
			center = Vector2(body.get_center().x, body.end.y)
			span = Vector2(26, 26) * fit
		"squid":
			center = Vector2(body.end.x - 1, body.end.y - 2)
			span = Vector2(25, 33) * fit
			pivot = ITEM_PINS[6]
	center = _snap_socket(spec, center)
	var rect := Rect2(center - span * pivot, span)
	return {"icon": int(Shop.item(gear)["icon"]), "rect": rect, "socket": center,
		"behind": behind, "tip": rect.position + rect.size * Vector2(0.86, 0.12)}


func tool_tip(profile: Dictionary, at: Vector2, facing: float, moving: bool, clock: float) -> Vector2:
	var wear := attachment(profile, moving, clock)
	var tip: Vector2 = wear.get("tip", Vector2(30, -30))
	return at + Vector2(tip.x * facing, tip.y)


func draw_actor(canvas: CanvasItem, profile: Dictionary, at: Vector2, facing: float,
		moving: bool, clock: float, magnify: float = 1.0) -> void:
	var spec := frame(profile, moving, clock)
	var wear := attachment(profile, moving, clock)
	var factor := float(spec["factor"])
	var body := Rect2(-(spec["anchor"] as Vector2) * factor, (spec["cell"] as Vector2) * factor)
	canvas.draw_set_transform(at, 0.0, Vector2(facing, 1.0) * magnify)
	if not wear.is_empty() and bool(wear["behind"]):
		canvas.draw_texture_rect(icons[int(wear["icon"])], wear["rect"], false)
	canvas.draw_texture_rect_region(texture(profile, moving), body, spec["region"])
	if not wear.is_empty() and not bool(wear["behind"]):
		canvas.draw_texture_rect(icons[int(wear["icon"])], wear["rect"], false)
	canvas.draw_set_transform(Vector2.ZERO)


func bounds(profile: Dictionary, moving: bool, clock: float) -> Rect2:
	var spec := frame(profile, moving, clock)
	var factor := float(spec["factor"])
	var result := Rect2(-(spec["anchor"] as Vector2) * factor, (spec["cell"] as Vector2) * factor)
	var wear := attachment(profile, moving, clock)
	if not wear.is_empty():
		result = result.merge(wear["rect"])
	return result


func _source_image(source: String) -> Image:
	if source_images.has(source):
		return source_images[source] as Image
	var image: Image = (load(source) as Texture2D).get_image()
	if image.is_compressed():
		image.decompress()
	image.convert(Image.FORMAT_RGBA8)
	source_images[source] = image
	return image


func _snap_socket(spec: Dictionary, requested: Vector2) -> Vector2:
	var key := String(spec["source"]) + ":" + str(spec["index"]) + ":" + str(requested)
	if socket_cache.has(key):
		return socket_cache[key] as Vector2
	var image := _source_image(String(spec["source"]))
	var factor := float(spec["factor"])
	var region: Rect2 = spec["region"]
	var desired := (spec["anchor"] as Vector2) + requested / factor
	var radius := ceili(14.0 / factor)
	var best := float(radius * radius + 1)
	var point := desired
	for y: int in range(maxi(0, floori(desired.y) - radius), mini(int(region.size.y), ceili(desired.y) + radius + 1)):
		for x: int in range(maxi(0, floori(desired.x) - radius), mini(int(region.size.x), ceili(desired.x) + radius + 1)):
			var distance := Vector2(x, y).distance_squared_to(desired)
			if distance < best and image.get_pixel(int(region.position.x) + x, int(region.position.y) + y).a > 0.65:
				best = distance
				point = Vector2(x, y)
	var result := (point - (spec["anchor"] as Vector2)) * factor
	socket_cache[key] = result
	return result
