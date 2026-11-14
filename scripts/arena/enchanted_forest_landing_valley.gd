extends RefCounted
## Passive scenery for the Forest route. The caller owns terrain and the actor.

const ART := "res://assets/sprites/enchanted_forest/landing_valley/"
const TRUNK := preload(ART + "fir_trunk.png")
const CROWN := preload(ART + "fir_crown.png")
const BOUGH := preload(ART + "fir_near_bough.png")
const ROCK := preload(ART + "granite.png")
const GRASS := preload(ART + "golden_grass.png")
const FLOWER := preload(ART + "buttercup.png")
const SHADOW := preload("res://assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png")
const WIND := preload("res://assets/shaders/sky_lagoon_grove_foliage.gdshader")

const FIR_FEET: Array[Vector2] = [
	Vector2(328, 1150), Vector2(448, 1052), Vector2(598, 1028),
	Vector2(918, 1375), Vector2(1005, 1318),
	Vector2(1178, 1055), Vector2(1282, 991), Vector2(1490, 1274),
	Vector2(1582, 1314), Vector2(1696, 990),
]
const FIR_HEIGHTS := [278.0, 242.0, 179.0, 335.0, 242.0, 245.0, 196.0, 274.0, 203.0, 214.0]
const ROCK_FEET: Array[Vector2] = [
	Vector2(372, 1176), Vector2(505, 1085), Vector2(481, 1355),
	Vector2(725, 1054), Vector2(857, 1360), Vector2(966, 1400),
	Vector2(1089, 1260), Vector2(1182, 1026), Vector2(1320, 1238),
	Vector2(1550, 1276), Vector2(1737, 1011),
]
const PLANT_POCKETS: Array[Vector2] = [
	Vector2(376, 1193), Vector2(485, 1340), Vector2(680, 1070), Vector2(736, 1347),
	Vector2(853, 1361), Vector2(981, 1347), Vector2(1088, 1246), Vector2(1160, 1026),
	Vector2(1301, 1259), Vector2(1454, 1278), Vector2(1542, 1323), Vector2(1721, 1038),
]

var _roots: Array[Node2D] = []
var _trees: Array[Node2D] = []
var _trunk_cards: Array[Sprite2D] = []
var _crown_cards: Array[Sprite2D] = []
var _near_cards: Array[Sprite2D] = []
var _wind: Array[ShaderMaterial] = []


## The callback accepts a point in the shared ground's local coordinates.
func build(ground: Node2D, can_place: Callable) -> void:
	teardown()
	for index: int in range(FIR_FEET.size()):
		var foot: Vector2 = FIR_FEET[index]
		if not can_place.call(foot):
			continue
		var height: float = FIR_HEIGHTS[index]
		var tree: Node2D = _root(ground, foot, "ValleyFir")
		_shadow(tree, height * 0.48)
		var trunk := _card(tree, TRUNK, Vector2.ZERO, height * 0.81, "RootAndTrunk")
		var crown := _card(tree, CROWN, Vector2(0, -height * 0.33), height * 0.73, "RearCrown")
		var side: float = -1.0 if index % 2 == 0 else 1.0
		var near := _card(tree, BOUGH, Vector2(side * height * 0.085, -height * 0.24),
			height * 0.31, "NearBough")
		near.flip_h = side < 0.0
		var tint := Color("#a6bd95") if foot.y < 1100.0 else Color("#eddfb9")
		tree.modulate = tint
		_trees.append(tree)
		_trunk_cards.append(trunk)
		_crown_cards.append(crown)
		_near_cards.append(near)

	for index: int in range(ROCK_FEET.size()):
		var foot: Vector2 = ROCK_FEET[index]
		if not can_place.call(foot):
			continue
		var height: float = 23.0 + 8.0 * (index % 4)
		var root: Node2D = _root(ground, foot, "ValleyGranite")
		_shadow(root, height * 1.5)
		var stone: Sprite2D = _card(root, ROCK, Vector2.ZERO, height, "MossGranite")
		stone.flip_h = index % 2 == 0

	for index: int in range(3):
		var material := ShaderMaterial.new()
		material.shader = WIND
		material.set_shader_parameter("reach", 3.5 + index)
		_wind.append(material)
	for index: int in range(PLANT_POCKETS.size()):
		var center: Vector2 = PLANT_POCKETS[index]
		for item: int in range(7):
			var offset := Vector2((item - 3) * 12.0, sin(item * 2.6 + index) * 20.0)
			var foot: Vector2 = center + offset
			if not can_place.call(foot):
				continue
			var root: Node2D = _root(ground, foot, "ValleyUnderstory")
			var bloom: bool = (item + index) % 4 == 0
			var card: Sprite2D = _card(root, FLOWER if bloom else GRASS, Vector2.ZERO,
				23.0 + float((index + item) % 4) * 6.0, "Buttercup" if bloom else "SeedGrass")
			card.flip_h = item % 2 == 0
			card.material = _wind[(index + item) % _wind.size()]
			card.modulate = Color("#e8e4c7") if index % 3 == 0 else Color.WHITE


func teardown() -> void:
	for root: Node2D in _roots:
		if is_instance_valid(root):
			root.free()
	_roots.clear()
	_trees.clear()
	_trunk_cards.clear()
	_crown_cards.clear()
	_near_cards.clear()
	_wind.clear()


func tick(time: float, actor: Vector2, delta: float) -> void:
	for index: int in range(_wind.size()):
		_wind[index].set_shader_parameter("breeze", time * 1.45 + index * 1.8)
	for index: int in range(_trees.size()):
		var tree: Node2D = _trees[index]
		var crown: Sprite2D = _crown_cards[index]
		var near: Sprite2D = _near_cards[index]
		var sway: float = sin(time * 1.2 + index * 0.8)
		crown.rotation = sway * 0.015
		near.rotation = sway * 0.041
		# The bough has its own footprint. Fade it locally while Roshan is behind it.
		var trunk: Sprite2D = _trunk_cards[index]
		var easing: float = 1.0 - exp(-delta * 16.0)
		near.modulate.a = lerpf(near.modulate.a, 0.14 if _overlaps_actor(near, tree, actor) else 1.0, easing)
		crown.modulate.a = lerpf(crown.modulate.a, 0.22 if _overlaps_actor(crown, tree, actor) else 1.0, easing)
		trunk.modulate.a = lerpf(trunk.modulate.a, 0.24 if _overlaps_actor(trunk, tree, actor) else 1.0, easing)


func _overlaps_actor(card: Sprite2D, tree: Node2D, actor: Vector2) -> bool:
	if actor.y >= tree.position.y:
		return false
	var size: Vector2 = card.texture.get_size() * card.scale
	var base: Vector2 = tree.position + card.position
	var bounds := Rect2(base - Vector2(size.x * 0.5, size.y), size)
	var silhouette := Rect2(actor - Vector2(36.0, 145.0), Vector2(72.0, 145.0))
	return bounds.intersects(silhouette)


func _root(parent: Node2D, foot: Vector2, label: String) -> Node2D:
	var root := Node2D.new()
	root.name = label
	root.position = foot
	parent.add_child(root, true)
	_roots.append(root)
	return root


func _card(root: Node2D, art: Texture2D, foot: Vector2, height: float, label: String) -> Sprite2D:
	var card := Sprite2D.new()
	card.name = label
	card.texture = art
	card.position = foot
	card.centered = false
	card.offset = Vector2(-art.get_width() * 0.5, -art.get_height())
	card.scale = Vector2.ONE * (height / art.get_height())
	root.add_child(card)
	return card


func _shadow(root: Node2D, width: float) -> void:
	var shadow := Sprite2D.new()
	shadow.texture = SHADOW
	shadow.scale = Vector2(width, width * 0.42) / SHADOW.get_size()
	shadow.modulate.a = 0.50
	shadow.z_index = -1
	root.add_child(shadow)
