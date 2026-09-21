extends RefCounted
# Authored raster differences: original cloud artwork stays intact at rest.
const BASE := "res://assets/sprites/sky_lagoon/whole_scene_v2/"
const CARDS: Array[Dictionary] = [
	{"id": "cloud_sea_near_0_add","file": "cloud_bank_near_0_add.png","size": [2048,512],"position": [300,950],"regions": [[2,2,1020,210],[1026,2,1020,210],[2,258,1020,210],[1026,258,1020,210]],"cycle": 4.8,"subtract": false},
	{"id": "cloud_sea_near_0_subtract","file": "cloud_bank_near_0_subtract.png","size": [2048,512],"position": [300,950],"regions": [[2,2,1020,210],[1026,2,1020,210],[2,258,1020,210],[1026,258,1020,210]],"cycle": 4.8,"subtract": true},
	{"id": "cloud_sea_near_1_add","file": "cloud_bank_near_1_add.png","size": [1024,512],"position": [2340,950],"regions": [[2,2,480,210],[514,2,480,210],[2,258,480,210],[514,258,480,210]],"cycle": 4.8,"subtract": false},
	{"id": "cloud_sea_near_1_subtract","file": "cloud_bank_near_1_subtract.png","size": [1024,512],"position": [2340,950],"regions": [[2,2,480,210],[514,2,480,210],[2,258,480,210],[514,258,480,210]],"cycle": 4.8,"subtract": true},
	{"id": "cloud_sea_far_0_add","file": "cloud_bank_far_0_add.png","size": [2048,256],"position": [600,900],"regions": [[2,2,1020,80],[1026,2,1020,80],[2,130,1020,80],[1026,130,1020,80]],"cycle": 8.0,"subtract": false},
	{"id": "cloud_sea_far_0_subtract","file": "cloud_bank_far_0_subtract.png","size": [2048,256],"position": [600,900],"regions": [[2,2,1020,80],[1026,2,1020,80],[2,130,1020,80],[1026,130,1020,80]],"cycle": 8.0,"subtract": true},
	{"id": "cloud_sea_far_1_add","file": "cloud_bank_far_1_add.png","size": [1024,256],"position": [2640,900],"regions": [[2,2,480,80],[514,2,480,80],[2,130,480,80],[514,130,480,80]],"cycle": 8.0,"subtract": false},
	{"id": "cloud_sea_far_1_subtract","file": "cloud_bank_far_1_subtract.png","size": [1024,256],"position": [2640,900],"regions": [[2,2,480,80],[514,2,480,80],[2,130,480,80],[514,130,480,80]],"cycle": 8.0,"subtract": true},
]

static func clear(state: Dictionary) -> void:
	for value: Variant in state.get("lagoon_cloud_bank_cards", []) as Array:
		if is_instance_valid(value):
			(value as Sprite2D).free()
	state.erase("lagoon_cloud_bank_cards")
	state.erase("lagoon_cloud_bank_t")
	state.erase("lagoon_cloud_bank_rejection")

static func build(state: Dictionary, parent: Node2D, tint: Color, texture_base: String = BASE) -> bool:
	clear(state)
	if not is_instance_valid(parent):
		return false
	var textures: Array[Texture2D] = []
	for definition: Dictionary in CARDS:
		var path: String = texture_base + str(definition["file"])
		if not ResourceLoader.exists(path):
			state["lagoon_cloud_bank_rejection"] = "Missing cloud difference atlas: " + path
			return false
		var texture: Texture2D = load(path) as Texture2D
		var size: Array = definition["size"] as Array
		if texture == null or texture.get_size() != Vector2(float(size[0]), float(size[1])):
			state["lagoon_cloud_bank_rejection"] = "Incorrect cloud difference atlas: " + path
			return false
		textures.append(texture)
	var add := CanvasItemMaterial.new()
	add.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	var subtract := CanvasItemMaterial.new()
	subtract.blend_mode = CanvasItemMaterial.BLEND_MODE_SUB
	var cards: Array[Sprite2D] = []
	for index: int in range(CARDS.size()):
		var definition: Dictionary = CARDS[index]
		var card := Sprite2D.new()
		card.name = "CloudBank_" + str(definition["id"])
		card.texture = textures[index]
		card.centered = false
		card.region_enabled = true
		card.region_filter_clip_enabled = false
		card.scale = Vector2.ONE * 2.0
		var position: Array = definition["position"] as Array
		card.position = Vector2(float(position[0]), float(position[1]))
		card.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		card.modulate = tint
		card.material = subtract if bool(definition["subtract"]) else add
		card.z_index = 0
		card.set_meta("canvas_layer_role", "authored_cloud_material_difference")
		card.set_meta("source_owned", true)
		parent.add_child(card)
		cards.append(card)
	state["lagoon_cloud_bank_cards"] = cards
	state["lagoon_cloud_bank_t"] = 0.0
	tick(state, 0.0, false)
	return true

static func tick(state: Dictionary, delta: float, paused: bool) -> void:
	if paused or not state.has("lagoon_cloud_bank_cards"):
		return
	var enabled: bool = bool(state.get("lagoon_environment_motion_enabled", true))
	var timer: float = float(state.get("lagoon_cloud_bank_t", 0.0))
	if enabled:
		timer = fposmod(timer + clampf(delta, 0.0, 0.1), 24.0)
		state["lagoon_cloud_bank_t"] = timer
	var cards: Array = state["lagoon_cloud_bank_cards"] as Array
	for index: int in range(cards.size()):
		var card: Sprite2D = cards[index] as Sprite2D
		if not is_instance_valid(card):
			continue
		var definition: Dictionary = CARDS[index]
		var cycle: float = float(definition["cycle"])
		var frame: int = mini(3, int(fposmod(timer, cycle) / cycle * 4.0)) if enabled else 0
		var rect: Array = definition["regions"][frame] as Array
		card.region_rect = Rect2(float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))
		card.visible = enabled
