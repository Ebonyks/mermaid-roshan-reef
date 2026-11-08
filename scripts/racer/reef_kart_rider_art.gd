extends RefCounted
## Whole seated sprites. Each ride atlas has a 4×4 grid of 256px keys.
const ROOT := "res://assets/racer/riders_v1/"
const MOTION_ROOT := "res://assets/racer/rider_poses_v3/"
const MOTION_CELL := 200
const MOTION_COLS := 5
const MOTION_COUNT := 7
const VEHICLE_INDEX := {"kart": 0, "moto": 1, "truck": 2}
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


static func motion_atlas(driver: String) -> Texture2D:
	var path := MOTION_ROOT + driver + ".png"
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


static func motion_region(ride: String, frame: int) -> Rect2:
	var index := int(VEHICLE_INDEX[ride]) * MOTION_COUNT + frame
	return Rect2(Vector2(index % MOTION_COLS, index / MOTION_COLS) * MOTION_CELL,
		Vector2(MOTION_CELL, MOTION_CELL))


static func advance_motion(kart: Dictionary, delta: float, driving: bool) -> void:
	if kart.get("motion_sheet") == null:
		return
	var pose_mix: Vector2 = kart["rider_pose"]
	var active := driving and float(kart["spin_t"]) <= 0.0
	var boosting := active and float(kart["boost_t"]) > 0.0
	var steer := float(kart["steer_vis"]) if active and not boosting and pose_mix.y < 0.24 else 0.0
	pose_mix.x = move_toward(pose_mix.x, steer, 14.0 * delta)
	# Return through the middle before switching between a lean and a tuck.
	var tuck := 1.0 if boosting and absf(pose_mix.x) < 0.24 else 0.0
	pose_mix.y = move_toward(pose_mix.y, tuck, (12.0 if tuck > 0.0 else 9.0) * delta)
	kart["rider_pose"] = pose_mix


static func motion_frame(pose_mix: Vector2) -> int:
	if pose_mix.y >= 0.24:
		return 6 if pose_mix.y >= 0.72 else 5
	if absf(pose_mix.x) < 0.24:
		return 0
	var half_turn := 1 if pose_mix.x < 0.0 else 3
	return half_turn + int(absf(pose_mix.x) >= 0.70)
