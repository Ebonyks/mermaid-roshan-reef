extends RefCounted

# Keep the existing eight Racer characters, the Canal rival and the family.
# Crops are retained for callers without a seated chase sprite. The original
# images remain the identity portraits in the garage.
const PORTRAIT_CROPS := [
	Rect2(102, 10, 115, 96), Rect2(12, 0, 236, 218),
	Rect2(260, 0, 361, 340), Rect2(59, 8, 161, 133),
	Rect2(38, 0, 182, 149), Rect2(39, 4, 271, 224),
	Rect2(67, 5, 280, 241), Rect2(37, 3, 220, 226),
]
const DRIVER_IDS := ["roshan", "sparkle", "huluu", "bunny", "kitty", "baby_doll", "dolly", "sleepy"]
const RIDES := [
	{"id": "kart", "name": "Go-Kart", "pace": 1.0, "lane_rate": 1.0, "turn_rate": 1.0,
		"speed": 3, "steering": 3, "tip": "Balanced speed and steering"},
	{"id": "moto", "name": "Zoom Cycle", "pace": 1.12, "lane_rate": 0.88, "turn_rate": 0.84,
		"speed": 5, "steering": 2, "tip": "Fast on straights · Wider turns"},
	{"id": "truck", "name": "Monster Truck", "pace": 0.90, "lane_rate": 1.12, "turn_rate": 1.12,
		"speed": 2, "steering": 5, "tip": "Tight steering · Lower top speed"},
]
const EXTRA_DRIVERS := [
	{"id": "imp", "name": "Imp", "sprite": "res://assets/opera/worlds/actors/rival_racer.png",
		"crop": Rect2(119, 19, 273, 246)},
	{"id": "rumi", "name": "Rumi", "sprite": "res://assets/characters/rumi/rumi_eight_pose_runtime.png",
		"pose": Rect2(512, 0, 256, 384), "crop": Rect2(560, 30, 132, 135)},
	{"id": "daddy", "name": "Daddy Mermaid", "sprite": "res://assets/characters/friends/daddy.webp",
		"crop": Rect2(286, 0, 271, 255)},
	{"id": "mama_baby", "name": "Mama & Baby", "sprite": "res://assets/characters/friends/mama_baby.png",
		"crop": Rect2(58, 0, 178, 158)},
]


static func driver_count() -> int:
	return DRIVER_IDS.size() + EXTRA_DRIVERS.size()

static func driver(index: int) -> Dictionary:
	if index >= DRIVER_IDS.size():
		return EXTRA_DRIVERS[index - DRIVER_IDS.size()]
	var prior: Dictionary = RacerGame2D.RACERS[index]
	var name := "Baby Eagle" if DRIVER_IDS[index] == "sparkle" else String(prior["name"])
	return {"id": DRIVER_IDS[index], "name": name, "sprite": prior["sprite"], "crop": PORTRAIT_CROPS[index]}


static func portrait(cast_member: Dictionary) -> Texture2D:
	var source := load(String(cast_member["sprite"])) as Texture2D
	if not cast_member.has("pose"):
		return source
	var pose := AtlasTexture.new()
	pose.atlas = source
	pose.region = cast_member["pose"]
	return pose


static func spec(driver_index: int, ride_index: int, slot: int) -> Dictionary:
	var cast_member := driver(driver_index)
	var ride: Dictionary = RIDES[ride_index]
	return {
		"id": "player_%d" % (slot + 1), "player": true,
		"driver": cast_member["id"], "driver_art": cast_member["sprite"], "portrait_crop": cast_member["crop"],
		"vehicle": ride["id"], "pace": ride["pace"], "lane_rate": ride["lane_rate"], "turn_rate": ride["turn_rate"],
		"player_color": Color("#71dfeb") if slot == 0 else Color("#ffc277"),
		"ride_tint": ReefKartRace.IMP_TINT if cast_member["id"] == "imp" and ride["id"] == "kart" else Color.WHITE,
	}
