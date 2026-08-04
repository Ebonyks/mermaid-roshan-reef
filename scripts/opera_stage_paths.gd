class_name OperaStagePaths
extends RefCounted
## Per-career stage geography for the painted opera worlds.
##
## Every painted world (assets/opera/worlds/backdrops/world_<career>.png) was
## designed as a walkable district: entry at the left, a continuous route to
## the right. PATHS holds that route as normalized waypoints plus the task
## stations (anchored to painted landmarks) and magnifier clue spots, all in
## 0..1 coordinates of the full-bleed painting; helpers convert to the
## 1280x720 screen. Careers without derived data (or without a painting yet,
## like nursery) fall back to a gentle mid-stage arc so nothing breaks.
##
## Waypoint data is derived visually from each painting — see
## OPERA_STAGE_INTERACTION_2026-08-02.md for the derivation record.

const SCREEN := Vector2(1280.0, 720.0)

## career -> {path: Array[Vector2-as-arrays], stations: [{id, pos, landmark}],
## clue_spots: [[x,y]...]} — populated from the visual derivation pass.
const PATHS: Dictionary = {
	"chef": {
		"path": [[0.08, 0.62], [0.17, 0.625], [0.27, 0.615], [0.4, 0.59], [0.5, 0.565], [0.555, 0.52], [0.615, 0.565], [0.7, 0.545], [0.855, 0.55]],
		"stations": [
			{"id": "mixing_bowl", "pos": [0.28, 0.6], "landmark": "giant pink-and-cream mixing bowl with whisk, ringed by little step stools"},
			{"id": "hearth_oven", "pos": [0.475, 0.565], "landmark": "arched golden oven with glowing hearth, just left of the footbridge"},
			{"id": "cake_tower", "pos": [0.655, 0.545], "landmark": "gold etagere tower displaying yellow, pink, and purple cakes"},
			{"id": "macaron_cart", "pos": [0.75, 0.53], "landmark": "wheeled cart with macarons under a glass dome"},
			{"id": "grand_cake_stage", "pos": [0.86, 0.545], "landmark": "red-curtained stage with giant three-tier celebration cake at the top of carpeted steps"},
		],
		"clue_spots": [[0.42, 0.095], [0.728, 0.12], [0.483, 0.1], [0.073, 0.185], [0.25, 0.3], [0.74, 0.23], [0.085, 0.815], [0.94, 0.775]],
	},
	"detective": {
		"path": [[0.07, 0.44], [0.115, 0.5], [0.16, 0.555], [0.3, 0.56], [0.46, 0.555], [0.62, 0.545], [0.78, 0.54], [0.89, 0.555], [0.93, 0.56]],
		"stations": [
			{"id": "evidence_shelves", "pos": [0.2, 0.56], "landmark": "arched display shelf stacked with patterned evidence lockboxes"},
			{"id": "pedestal_display", "pos": [0.56, 0.555], "landmark": "round pedestal table holding purple and pink hat-box cases"},
			{"id": "magnifier_tower", "pos": [0.65, 0.545], "landmark": "tall tower topped with a giant golden magnifying glass, stained-glass window at its base"},
			{"id": "mirror_gallery", "pos": [0.755, 0.54], "landmark": "bookshelf wall with a row of three arched dressing mirrors"},
			{"id": "treasure_dais", "pos": [0.93, 0.56], "landmark": "giant open treasure chest with pearl tiara under the domed pavilion"},
		],
		"clue_spots": [[0.33, 0.08], [0.645, 0.095], [0.92, 0.1], [0.652, 0.31], [0.42, 0.4], [0.125, 0.48], [0.605, 0.71], [0.32, 0.88]],
	},
	"ballerina": {
		"path": [[0.03, 0.74], [0.11, 0.69], [0.22, 0.68], [0.38, 0.62], [0.49, 0.6], [0.62, 0.52], [0.7, 0.5], [0.85, 0.45], [0.91, 0.37]],
		"stations": [
			{"id": "curtain_alcove", "pos": [0.11, 0.68], "landmark": "gold-framed dressing alcove at far left with red drapes, teal inner curtains and a pearl scallop-shell crest"},
			{"id": "wave_tuffets", "pos": [0.24, 0.67], "landmark": "teal wave-embroidered practice tuffets sitting on the mosaic causeway"},
			{"id": "shell_bandstand", "pos": [0.44, 0.56], "landmark": "pearl-studded domed bandstand with a golden treble-clef shell stage on its tiered base"},
			{"id": "trifold_mirror", "pos": [0.67, 0.5], "landmark": "gold trifold rehearsal mirror standing at the walkway's edge past the bridge"},
			{"id": "rose_finale_stage", "pos": [0.91, 0.37], "landmark": "round pink finale dais crowned by a giant rose bouquet with a teal ribbon bow"},
		],
		"clue_spots": [[0.17, 0.13], [0.07, 0.33], [0.47, 0.28], [0.72, 0.22], [0.905, 0.26], [0.05, 0.81], [0.57, 0.83], [0.815, 0.72]],
	},
	"candymaker": {
		"path": [[0.05, 0.72], [0.13, 0.75], [0.245, 0.715], [0.33, 0.78], [0.42, 0.79], [0.54, 0.75], [0.63, 0.71], [0.75, 0.72], [0.87, 0.74]],
		"stations": [
			{"id": "gumball_vat", "pos": [0.245, 0.715], "landmark": "foot of the staircase under the giant glass gumball boiler full of pink candy spheres"},
			{"id": "taffy_press", "pos": [0.42, 0.79], "landmark": "red carousel-domed taffy press with the ball-topped lever on a round pedestal platform"},
			{"id": "candy_bag_cottage", "pos": [0.62, 0.705], "landmark": "cream candy-bag cottage with the big red bow and arched wooden door"},
			{"id": "sweet_display_shop", "pos": [0.84, 0.725], "landmark": "gold-arched display cabinet with shelves of shell, heart and swirl candies"},
			{"id": "candy_cart", "pos": [0.9, 0.755], "landmark": "wheeled vendor cart with pink striped canopy carrying giant gumballs (right-edge destination)"},
		],
		"clue_spots": [[0.2, 0.15], [0.03, 0.28], [0.39, 0.3], [0.55, 0.33], [0.86, 0.13], [0.76, 0.55], [0.17, 0.9], [0.93, 0.93]],
	},
	"doctor": {
		"path": [[0.025, 0.6], [0.1, 0.58], [0.21, 0.595], [0.35, 0.585], [0.46, 0.55], [0.578, 0.535], [0.655, 0.665], [0.745, 0.73], [0.855, 0.815]],
		"stations": [
			{"id": "starfish_triage", "pos": [0.075, 0.565], "landmark": "smiling starfish patient waiting on a purple cushion under the golden shell archway at the left entry"},
			{"id": "stethoscope_clinic", "pos": [0.21, 0.585], "landmark": "teal-domed clinic pavilion topped with a giant stethoscope, purple exam daybed inside"},
			{"id": "thermometer_garden", "pos": [0.462, 0.545], "landmark": "giant red-bulb thermometer standing in a scalloped flower planter beside the promenade"},
			{"id": "exam_booth", "pos": [0.578, 0.525], "landmark": "first heart-crowned curtained exam booth with a round purple patient bed (a row of five lines the upper walk)"},
			{"id": "recovery_bed", "pos": [0.86, 0.81], "landmark": "shell-backed recovery plaza at bottom right with a round sunken bed-basin and beach parasol"},
		],
		"clue_spots": [[0.062, 0.19], [0.317, 0.125], [0.21, 0.25], [0.39, 0.295], [0.474, 0.645], [0.765, 0.355], [0.68, 0.83], [0.963, 0.655]],
	},
	"farmer": {
		"path": [[0.11, 0.63], [0.24, 0.65], [0.39, 0.61], [0.45, 0.55], [0.55, 0.58], [0.64, 0.585], [0.74, 0.6], [0.845, 0.59], [0.9, 0.52]],
		"stations": [
			{"id": "flower_urn", "pos": [0.23, 0.6], "landmark": "stone pedestal urn overflowing with pink flowers at the first path bend"},
			{"id": "barn_door", "pos": [0.445, 0.47], "landmark": "red barn with green shingle roof and open arched wooden door at the top of the path spur"},
			{"id": "hay_steps", "pos": [0.585, 0.55], "landmark": "staircase of stacked golden hay bales climbing the hillside"},
			{"id": "mud_pen", "pos": [0.745, 0.61], "landmark": "round log-post fenced pen with churned mud floor (animal pen)"},
			{"id": "harvest_picnic", "pos": [0.9, 0.51], "landmark": "red gingham picnic blanket with woven baskets of corn, grapes and vegetables"},
		],
		"clue_spots": [[0.065, 0.475], [0.244, 0.286], [0.345, 0.33], [0.454, 0.274], [0.674, 0.252], [0.88, 0.24], [0.615, 0.77], [0.94, 0.92]],
	},
	"boxer": {
		"path": [[0.09, 0.63], [0.2, 0.645], [0.3, 0.685], [0.445, 0.69], [0.58, 0.685], [0.655, 0.7], [0.755, 0.67], [0.83, 0.615], [0.88, 0.685]],
		"stations": [
			{"id": "target_pads", "pos": [0.205, 0.635], "landmark": "red X-stitched target shields mounted on the domed training tunnel"},
			{"id": "punching_bags", "pos": [0.42, 0.675], "landmark": "rack of red, purple and teal punching bags hanging from the rope-lashed frame on the round platform"},
			{"id": "sparring_mats", "pos": [0.58, 0.685], "landmark": "the red circular sparring mat (last of three colored floor rings)"},
			{"id": "victory_bell", "pos": [0.815, 0.615], "landmark": "bell tower with the golden victory bell, at the top of the rope bridge"},
			{"id": "champion_belt", "pos": [0.885, 0.68], "landmark": "giant championship belt with golden scallop-shell buckle displayed on the tiered pedestal"},
		],
		"clue_spots": [[0.086, 0.3], [0.385, 0.165], [0.55, 0.285], [0.727, 0.19], [0.16, 0.47], [0.895, 0.525], [0.478, 0.615], [0.17, 0.92]],
	},
	"magician": {
		"path": [[0.07, 0.56], [0.16, 0.59], [0.24, 0.53], [0.36, 0.54], [0.45, 0.61], [0.56, 0.7], [0.64, 0.72], [0.74, 0.47], [0.84, 0.42]],
		"stations": [
			{"id": "stage_curtain", "pos": [0.08, 0.56], "landmark": "Golden scallop-shell proscenium arch with red velvet stage curtains at the left entry"},
			{"id": "purple_hat_door", "pos": [0.22, 0.52], "landmark": "Giant purple top-hat building with gold star band and round performer's door"},
			{"id": "red_hat_den", "pos": [0.43, 0.52], "landmark": "Red top-hat building with pink shell buckle and arched rabbit-den doorway beside the bridge"},
			{"id": "magic_door_gallery", "pos": [0.74, 0.48], "landmark": "Row of freestanding enchanted doors and open potion-shelf wardrobes where the star-tile trail bends"},
			{"id": "moon_pool", "pos": [0.84, 0.44], "landmark": "Large round scrying pool reflecting the crescent moon, ringed by rope fence and twin-lamp posts"},
		],
		"clue_spots": [[0.845, 0.08], [0.125, 0.12], [0.32, 0.08], [0.69, 0.165], [0.21, 0.385], [0.44, 0.4], [0.14, 0.86], [0.95, 0.7]],
	},
	"painter": {
		"path": [[0.06, 0.68], [0.19, 0.66], [0.34, 0.65], [0.47, 0.63], [0.565, 0.61], [0.65, 0.475], [0.71, 0.58], [0.8, 0.61], [0.9, 0.46]],
		"stations": [
			{"id": "purple_pot", "pos": [0.2, 0.63], "landmark": "giant purple paint pot with brush on its stepped pedestal, paint spilling onto the deck"},
			{"id": "coral_pot", "pos": [0.35, 0.62], "landmark": "giant coral-pink paint pot with brush, pink spill running down its steps"},
			{"id": "cream_pot", "pos": [0.48, 0.61], "landmark": "giant cream/gold paint pot with brush at the deck's right end before the bridge"},
			{"id": "splat_garden", "pos": [0.76, 0.6], "landmark": "rock-ringed garden bed of paint-splat topiaries (pink, mint, white splats on stems) across the bridge"},
			{"id": "arch_gallery", "pos": [0.9, 0.46], "landmark": "balustraded stone terrace beneath the grand scallop-shell archway at far right"},
		],
		"clue_spots": [[0.035, 0.03], [0.3, 0.1], [0.14, 0.27], [0.555, 0.32], [0.79, 0.25], [0.6, 0.42], [0.815, 0.93], [0.07, 0.86]],
	},
	"astronaut": {
		"path": [[0.07, 0.72], [0.17, 0.735], [0.3, 0.735], [0.42, 0.73], [0.5, 0.725], [0.615, 0.715], [0.72, 0.68], [0.83, 0.655], [0.92, 0.625]],
		"stations": [
			{"id": "observation_scope", "pos": [0.23, 0.73], "landmark": "giant brass-and-glass telescope tube mounted on a stone stand"},
			{"id": "zero_g_ring", "pos": [0.49, 0.72], "landmark": "giant upright glass ring (torus) with gold crown fitting, like a zero-g training loop"},
			{"id": "valve_tower", "pos": [0.615, 0.715], "landmark": "mint control tower with pink hand-wheel valve and shell emblem"},
			{"id": "oxygen_tanks", "pos": [0.735, 0.675], "landmark": "row of linked glass bubble tanks resting on arched bridge supports"},
			{"id": "rocket_pad", "pos": [0.915, 0.625], "landmark": "teal-and-pink rocket ship standing on the pier launch pad at far right"},
		],
		"clue_spots": [[0.07, 0.32], [0.32, 0.21], [0.4, 0.1], [0.71, 0.22], [0.625, 0.49], [0.127, 0.64], [0.205, 0.895], [0.35, 0.88]],
	},
	"racer": {
		"path": [[0.088, 0.69], [0.195, 0.72], [0.342, 0.69], [0.488, 0.675], [0.605, 0.64], [0.664, 0.54], [0.752, 0.535], [0.84, 0.48], [0.908, 0.445]],
		"stations": [
			{"id": "start_curtain", "pos": [0.09, 0.66], "landmark": "giant scallop-shell archway with purple velvet stage curtains (starting gate)"},
			{"id": "pit_garage", "pos": [0.34, 0.65], "landmark": "blue arched pit-garage bays stocked with tool racks, crates, and stacked tires"},
			{"id": "tire_depot", "pos": [0.6, 0.63], "landmark": "stacks of purple and teal race tires piled at the base of the track wall"},
			{"id": "grandstand", "pos": [0.64, 0.545], "landmark": "purple-seated spectator grandstand with scalloped white canopy"},
			{"id": "trophy_shell", "pos": [0.91, 0.44], "landmark": "giant scallop-shell trophy stage holding a huge pearl on a golden pedestal at the ramp summit"},
		],
		"clue_spots": [[0.07, 0.08], [0.38, 0.1], [0.22, 0.31], [0.63, 0.23], [0.41, 0.84], [0.94, 0.28], [0.92, 0.74], [0.61, 0.95]],
	},
	"popstar": {
		"path": [[0.04, 0.75], [0.13, 0.71], [0.24, 0.71], [0.42, 0.71], [0.52, 0.69], [0.58, 0.66], [0.66, 0.69], [0.75, 0.76], [0.89, 0.73]],
		"stations": [
			{"id": "stage_curtain", "pos": [0.1, 0.7], "landmark": "shell-arched stage doorway with magenta curtains, pearl garland and steps down to the deck"},
			{"id": "mic_row", "pos": [0.25, 0.68], "landmark": "row of golden vintage microphone stands lining the music-note railing walkway"},
			{"id": "dance_pads", "pos": [0.42, 0.68], "landmark": "circular stage plaza inlaid with four hexagonal arrow dance pads (teal up, purple left, pink right, cream down)"},
			{"id": "rainbow_bridge", "pos": [0.66, 0.66], "landmark": "S-curved rainbow road with gold pearl-topped railings and lamp posts"},
			{"id": "encore_balcony", "pos": [0.9, 0.71], "landmark": "round encore balcony with shell crest, gold railings and coral planters at the far right"},
		],
		"clue_spots": [[0.06, 0.62], [0.24, 0.27], [0.5, 0.16], [0.72, 0.13], [0.9, 0.22], [0.63, 0.3], [0.39, 0.92], [0.82, 0.76]],
	},
}

## Walkable roam envelope per career, as [t_min, t_max] along the route.
## The route's extreme ends are the painted entry and destination (arches,
## daises, carts) — scenery, not standing room — and several careers have
## mid-route hazards recorded in the derivation notes (chef's water inlet
## under the footbridge, doctor's canal descent, ballerina's bridge gap).
## Crew imps roam inside this envelope; Roshan still walks the full route.
const ROAM: Dictionary = {
	"chef": [0.14, 0.86],
	"detective": [0.16, 0.88],
	"ballerina": [0.14, 0.84],
	"candymaker": [0.12, 0.86],
	"doctor": [0.12, 0.80],
	"farmer": [0.14, 0.88],
	"boxer": [0.14, 0.86],
	"magician": [0.14, 0.86],
	"painter": [0.14, 0.86],
	"astronaut": [0.14, 0.86],
	"racer": [0.16, 0.84],
	"popstar": [0.14, 0.86],
	"nursery": [0.15, 0.85],
}


static func roam_range(career: String) -> Vector2:
	var entry: Array = ROAM.get(career, [0.14, 0.86])
	return Vector2(float(entry[0]), float(entry[1]))


const FALLBACK_PATH := [
	[0.08, 0.72], [0.22, 0.66], [0.38, 0.70], [0.52, 0.64],
	[0.66, 0.70], [0.80, 0.65], [0.92, 0.70],
]
const FALLBACK_STATION_T := [0.10, 0.34, 0.58, 0.82]


static func path_points(career: String) -> PackedVector2Array:
	var raw: Array = (PATHS.get(career, {}) as Dictionary).get("path", FALLBACK_PATH)
	var points := PackedVector2Array()
	for entry: Array in raw:
		points.append(Vector2(float(entry[0]), float(entry[1])) * SCREEN)
	return points


static func stations(career: String) -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	var raw: Array = (PATHS.get(career, {}) as Dictionary).get("stations", [])
	if raw.is_empty():
		var points := path_points(career)
		for index in range(FALLBACK_STATION_T.size()):
			out.append({
				"id": "station_%d" % index,
				"pos": point_along(points, float(FALLBACK_STATION_T[index])),
				"landmark": "stage landmark",
			})
		return out
	for entry: Dictionary in raw:
		var pos: Array = entry.get("pos", [0.5, 0.68])
		out.append({
			"id": String(entry.get("id", "station")),
			"pos": Vector2(float(pos[0]), float(pos[1])) * SCREEN,
			"landmark": String(entry.get("landmark", "")),
		})
	return out


static func clue_spots(career: String) -> PackedVector2Array:
	var out := PackedVector2Array()
	var raw: Array = (PATHS.get(career, {}) as Dictionary).get("clue_spots", [])
	if raw.is_empty():
		# spread fallback sparkle spots across the stage
		for index in range(8):
			out.append(Vector2(
				(0.12 + 0.76 * float(index) / 7.0) * SCREEN.x,
				(0.30 + 0.35 * float((index * 3) % 5) / 4.0) * SCREEN.y
			))
		return out
	for entry: Array in raw:
		out.append(Vector2(float(entry[0]), float(entry[1])) * SCREEN)
	return out


## Total polyline length in pixels.
static func path_length(points: PackedVector2Array) -> float:
	var total := 0.0
	for index in range(1, points.size()):
		total += points[index - 1].distance_to(points[index])
	return maxf(1.0, total)


## Point at parameter t (0..1) along the polyline, by arc length.
static func point_along(points: PackedVector2Array, t: float) -> Vector2:
	if points.is_empty():
		return SCREEN * 0.5
	if points.size() == 1:
		return points[0]
	var target := clampf(t, 0.0, 1.0) * path_length(points)
	var walked := 0.0
	for index in range(1, points.size()):
		var seg := points[index - 1].distance_to(points[index])
		if walked + seg >= target and seg > 0.0:
			return points[index - 1].lerp(points[index], (target - walked) / seg)
		walked += seg
	return points[points.size() - 1]


## Parameter t (0..1) of the polyline point nearest to pos.
static func nearest_t(points: PackedVector2Array, pos: Vector2) -> float:
	var best := 0.0
	var best_d := INF
	var walked := 0.0
	var total := path_length(points)
	for index in range(1, points.size()):
		var a := points[index - 1]
		var b := points[index]
		var seg := a.distance_to(b)
		var local := 0.0
		if seg > 0.0:
			local = clampf((pos - a).dot(b - a) / (seg * seg), 0.0, 1.0)
		var candidate := a.lerp(b, local)
		var d := candidate.distance_to(pos)
		if d < best_d:
			best_d = d
			best = (walked + local * seg) / total
		walked += seg
	return best
