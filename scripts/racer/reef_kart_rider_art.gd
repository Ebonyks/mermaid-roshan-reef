extends RefCounted
## Whole seated sprites. Each ride atlas has a 4×4 grid of 256px keys.
const ROOT := "res://assets/racer/riders_v1/"
const CHASE := "res://assets/kart/chase/"
const CELL := 256
const STRAIGHT := 0
const LEFT := 1
const RIGHT := 2
const BOOST := 3
const POSES := ["straight", "left", "right", "boost"]
const SLOTS := {
	"sparkle": 0, "huluu": 1, "bunny": 2, "kitty": 3, "baby_doll": 4, "dolly": 5,
	"sleepy": 6, "imp": 7, "rumi": 8, "daddy": 9, "mama_baby": 10,
}

# Existing authored Roshan keys share 627px source space. Match the rear tire
# anchors from assets/kart/chase/anchors.json to the projected ground point.
const AXLES := {
	"kart": [Vector2(335, 546.5), Vector2(350, 549.5), Vector2(278, 534), Vector2(315, 531)],
	"moto": [Vector2(310.5, 621), Vector2(329.5, 623), Vector2(293.5, 585), Vector2(303.5, 580)],
	"truck": [Vector2(330.25, 594.5), Vector2(348, 600.5), Vector2(294.75, 565), Vector2(313, 562)],
}

static func atlas(ride: String) -> Texture2D:
	var path := ROOT + ride + ".png"
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


static func region(driver: String, pose: int) -> Rect2:
	var slot := int(SLOTS[driver])
	if driver == "sparkle" and pose in [LEFT, RIGHT]:
		slot = 10 + pose
	return Rect2(Vector2(slot % 4, slot / 4) * CELL, Vector2(CELL, CELL))


static func pose(kart: Dictionary, allow_boost: bool) -> int:
	if allow_boost and float(kart["boost_t"]) > 0.0:
		return BOOST
	var steer := float(kart["steer_vis"])
	if steer < -0.35:
		return LEFT
	if steer > 0.35:
		return RIGHT
	return STRAIGHT


static func registered(ride: String, motion: int, rect: Rect2) -> Rect2:
	if not AXLES.has(ride):
		return rect
	var axle: Vector2 = AXLES[ride][motion]
	var shift := Vector2(0.5, 0.86) - axle / 627.0
	return Rect2(rect.position + rect.size * shift, rect.size)


static func preview(driver: String, ride: String) -> Texture2D:
	if driver == "roshan" and AXLES.has(ride):
		return load(CHASE + ride + "_straight.png") as Texture2D
	if SLOTS.has(driver):
		var sheet := atlas(ride)
		if sheet != null:
			var frame := AtlasTexture.new()
			frame.atlas = sheet
			frame.region = region(driver, STRAIGHT)
			frame.filter_clip = true
			return frame
	return load(CHASE + "empty_%s.png" % ride) as Texture2D
