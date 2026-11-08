extends RefCounted
## Mid-distance set pieces and wall lighting for the four PC courses.

const ROOT := "res://assets/racer/stage_art_v1/"
const PICKUP_REGIONS := {
	"item_bubble": Rect2(12, 12, 232, 226),
	"pearl": Rect2(268, 12, 222, 232),
	"socket_empty": Rect2(12, 268, 232, 199),
	"socket_lit": Rect2(268, 268, 232, 195),
}
# Authored in race order. Width in world units, first choice of side, atlas crop.
const SET_PIECES := {
	"playroom": [
		["block_castle", 432.0, -1, Rect2(12, 12, 488, 458)],
		["reading_fort", 470.0, 1, Rect2(524, 12, 488, 391)],
		["star_tents", 455.0, -1, Rect2(12, 524, 488, 435)],
		["toy_station", 535.0, 1, Rect2(524, 524, 488, 421)],
	],
	"kitchen": [
		["tea_buffet", 465.0, 1, Rect2(524, 524, 446, 488)],
		["copper_bakehouse", 498.0, -1, Rect2(12, 12, 445, 488)],
		["preserves_hutch", 355.0, 1, Rect2(12, 524, 329, 488)],
		["shell_washhouse", 530.0, -1, Rect2(524, 12, 488, 420)],
	],
	"mermaid_pool": [
		["changing_cabanas", 480.0, -1, Rect2(12, 12, 488, 405)],
		["fountain_pavilion", 455.0, 1, Rect2(524, 12, 464, 488)],
		["lily_island", 512.0, -1, Rect2(12, 524, 488, 409)],
		["rainbow_grotto", 580.0, 1, Rect2(524, 524, 488, 418)],
	],
	"opera_hall": [
		["opera_box", 485.0, -1, Rect2(12, 12, 488, 452)],
		["rehearsal_organ", 425.0, 1, Rect2(524, 12, 460, 488)],
		["footlight_proscenium", 600.0, -1, Rect2(12, 524, 488, 438)],
		["moon_wing", 480.0, 1, Rect2(524, 524, 488, 410)],
	],
}
const WALL_LIGHT := {
	"playroom": [Color("#d4c0c6"), Color("#ceafbd"), Color("#aeb8ce"), Color("#e0cab0")],
	"kitchen": [Color("#c6bda8"), Color("#e0a778"), Color("#aabac3"), Color("#b1beb0")],
	"mermaid_pool": [Color("#c7aab9"), Color("#86b9c8"), Color("#8aacc8"), Color("#bca5d0")],
	"opera_hall": [Color("#bca3b9"), Color("#ad91bc"), Color("#d6ad91"), Color("#8d95bb")],
}


static func wall_light(course: String, phase: float) -> Color:
	var lights: Array = WALL_LIGHT[course]
	var section := phase * 4.0
	var zone := floori(section) % 4
	var light: Color = lights[zone]
	return light.lerp(lights[(zone + 1) % 4], smoothstep(0.72, 1.0, fposmod(section, 1.0)))


static func add_landmarks(track: ReefKartTrack, camera_back: float, focal: float) -> void:
	var specs: Array = SET_PIECES[track.id]
	var placed: Array[Dictionary] = []
	var quarter := track.length * 0.25
	for zone in range(specs.size()):
		var spec: Array = specs[zone]
		var width: float = spec[1]
		var crop: Rect2 = spec[3]
		var height := minf(390.0, width * crop.size.y / crop.size.x)
		width = height * crop.size.x / crop.size.y
		var radius := width * 0.5
		var start := float(zone) * quarter
		var best := {}
		var best_cost := INF
		for fraction: float in [0.28, 0.42, 0.56, 0.70, 0.84]:
			var s := start + quarter * fraction
			for side: int in [spec[2], -int(spec[2])]:
				for offset: float in [440.0, 565.0, 710.0, 875.0, 1060.0]:
					var center := track.point_at(s, offset * side)
					if not clears_course(track, center, radius, placed):
						continue
					for sample in range(17):
						var approach := start + quarter * float(sample) / 20.0
						var forward := track.tangent_at(approach)
						var delta := center - (track.point_at(approach) - forward * camera_back)
						var depth := delta.dot(forward)
						if depth < 370.0 or depth > 1650.0:
							continue
						var x := forward.cross(delta) * focal / depth
						var projected_width := width * focal / depth
						var cost := absf(absf(x) - 177.0) + absf(projected_width - 225.0) * 0.9
						cost += absf(float(sample) - 8.0) * 2.0 + (0.0 if side == int(spec[2]) else 12.0)
						if cost >= best_cost:
							continue
						var eye := track.point_at(approach) - forward * camera_back
						var cover := _foreground_cover(track, eye, forward, depth, x, projected_width, focal)
						cost += cover * 145.0
						if cost < best_cost:
							best_cost = cost
							best = {"id": "stage_" + String(spec[0]), "pos": center, "s": s,
								"w": width, "h": height, "max_h": height, "crop": crop,
								"path": ROOT + track.id + ".png", "stage_zone": zone, "approach": approach}
		if best.is_empty():
			push_warning("No clear stage set piece in %s zone %d" % [track.id, zone])
			continue
		placed.append(best)
		track.landmarks.append(best)


static func _foreground_cover(track: ReefKartTrack, eye: Vector2, forward: Vector2, depth: float,
		x: float, width: float, focal: float) -> float:
	var cover := 0.0
	var left := x - width * 0.5
	var right := x + width * 0.5
	for prop: Dictionary in track.landmarks:
		if prop.has("stage_zone") or bool(prop.get("spans", false)):
			continue
		var offset := (prop["pos"] as Vector2) - eye
		var prop_depth := offset.dot(forward)
		if prop_depth <= 110.0 or prop_depth >= depth:
			continue
		var center := forward.cross(offset) * focal / prop_depth
		var half := float(prop["w"]) * focal / prop_depth * 0.41
		var overlap := minf(right, center + half) - maxf(left, center - half)
		cover = maxf(cover, overlap / width)
	return cover


static func clears_course(track: ReefKartTrack, center: Vector2, radius: float,
		placed: Array[Dictionary]) -> bool:
	# Conservative circular footprint keeps even a camera-facing card behind
	# the rails when viewed from the far side of another bend.
	var road_margin := ReefKartTrack.RAIL + radius + 27.0 + track.length / ReefKartTrack.SAMPLES * 0.5
	for sample: Vector2 in track.center:
		if center.distance_squared_to(sample) < road_margin * road_margin:
			return false
	for deck: Dictionary in track.roadside:
		var offset := center - (deck["pos"] as Vector2)
		var half: Vector2 = deck["half"]
		var x := maxf(0.0, absf(offset.dot(deck["along"])) - half.x)
		var y := maxf(0.0, absf(offset.dot(deck["across"])) - half.y)
		if x * x + y * y < pow(radius + 18.0, 2.0):
			return false
	for other: Dictionary in placed:
		if center.distance_to(other["pos"]) < radius + float(other["w"]) * 0.5 + 44.0:
			return false
	return true
