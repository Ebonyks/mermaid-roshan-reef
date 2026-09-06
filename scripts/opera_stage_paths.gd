class_name OperaStagePaths
extends RefCounted
## Per-career stage geography for the painted opera worlds.
##
## Every painted world (assets/opera/worlds/backdrops/world_<career>.png) was
## designed as a walkable district: entry at the left, a continuous route to
## the right. PATHS holds that route as normalized waypoints plus the task
## stations (anchored to painted landmarks) and magnifier clue spots.
##
## COORDINATE SPACE: 0..1 across the SHARP ARTWORK, not the full drawn frame.
## The composed tiles inset the painting inside a blurred bleed margin, so
## to_screen() remaps x onto the span the artwork actually occupies (see BLEED
## below). Read a coordinate off the painting and record it as-is; do not
## pre-compensate. Getting this wrong drifts every station outward — nothing at
## centre, up to ~115px at the edges.
##
## Careers without derived data (or without a painting yet, like nursery) fall
## back to a gentle mid-stage arc so nothing breaks.
##
## Waypoint data is derived visually from each painting — see
## OPERA_STAGE_INTERACTION_2026-08-02.md for the derivation record, and
## OPERA_MASTER_PACKAGE_2026-08-04.md §2-§3 for the 2026-08-04 re-derivation of
## farmer, boxer, magician, painter, astronaut, racer and popstar, whose worlds
## were repainted as different places.

const SCREEN := Vector2(1280.0, 720.0)

## career -> {path: Array[Vector2-as-arrays], stations: [{id, pos, landmark}],
## clue_spots: [[x,y]...]} — populated from the visual derivation pass.
const PATHS: Dictionary = {
	"teacher": {
		"path": [[0.08, 0.72], [0.30, 0.72], [0.49, 0.72], [0.70, 0.72], [0.90, 0.72]],
		"stations": [
			{"id": "lesson_desk", "pos": [0.49, 0.72], "landmark": "large cream learning board in the Library"},
		],
		"clue_spots": [],
	},
	"geologist": {
		"path": [[0.06, 0.70], [0.17, 0.69], [0.30, 0.66], [0.43, 0.64], [0.56, 0.66], [0.70, 0.64], [0.83, 0.61], [0.93, 0.58]],
		"stations": [
			{"id": "layer_wall", "pos": [0.20, 0.68], "object": [0.20, 0.40], "visual_size": [166.0, 152.0], "hotspot_size": [194.0, 180.0], "spur": [[0.17, 0.69], [0.20, 0.68]], "landmark": "broad striped rock wall with three bright sediment layers"},
			{"id": "fossil_table", "pos": [0.38, 0.64], "object": [0.38, 0.43], "visual_size": [154.0, 124.0], "hotspot_size": [182.0, 156.0], "spur": [[0.30, 0.66], [0.38, 0.64]], "landmark": "rounded stone inspection table holding a large spiral fossil"},
			{"id": "specimen_trays", "pos": [0.65, 0.64], "object": [0.65, 0.43], "visual_size": [166.0, 116.0], "hotspot_size": [194.0, 150.0], "spur": [[0.56, 0.66], [0.65, 0.64]], "landmark": "three dark pearl-rimmed specimen trays"},
			{"id": "crystal_gallery", "pos": [0.91, 0.58], "object": [0.91, 0.30], "visual_size": [154.0, 166.0], "hotspot_size": [182.0, 194.0], "spur": [[0.83, 0.61], [0.91, 0.58]], "landmark": "tall aqua and lavender crystal cluster glowing at the cave gallery"},
		],
		"clue_spots": [[0.12, 0.22], [0.25, 0.38], [0.36, 0.20], [0.50, 0.42], [0.64, 0.24], [0.76, 0.38], [0.87, 0.20], [0.94, 0.48]],
	},
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
		"path": [[0.0795, 0.4833], [0.1752, 0.5028], [0.2901, 0.5361], [0.4528, 0.6111], [0.4738, 0.7014], [0.558, 0.7569], [0.6824, 0.7542], [0.8068, 0.7333], [0.9063, 0.7139], [0.9236, 0.6361]],
		"stations": [
			{"id": "barn_doors", "pos": [0.1542, 0.4556], "landmark": "sand apron directly below the big red coral-shingled barn's white cross-braced double doors (fish weathervane on the ridge, pink scallop shell under the round loft window)"},
			{"id": "pearl_clam", "pos": [0.1035, 0.75], "landmark": "giant pink scallop clam shell holding a glowing pearl, sitting on the rock rim of the teal tide pool at bottom-left"},
			{"id": "blossom_arch", "pos": [0.4585, 0.4417], "landmark": "sand at the foot of the coral-flower arch where the rail-fenced orchard lane opens onto the yard (arch wreathed in orange starfish and pink blossoms)"},
			{"id": "seed_beds", "pos": [0.7092, 0.6764], "landmark": "the front-centre tilled oval seedbed of the 3x3 field, rimmed with pebbles and little corals"},
			{"id": "hay_bales", "pos": [0.8929, 0.3889], "landmark": "stack of three giant round golden hay bales at the right edge (one red starfish stuck to the front bale)"},
		],
		"clue_spots": [[0.1398, 0.125], [0.0604, 0.5444], [0.1676, 0.8333], [0.3571, 0.3278], [0.625, 0.2611], [0.7877, 0.2333], [0.7637, 0.8028], [0.9714, 0.6528]],
	},
	"boxer": {
		"path": [[0.0225, 0.694], [0.0799, 0.833], [0.2042, 0.882], [0.3189, 0.889], [0.4289, 0.854], [0.5245, 0.813], [0.6297, 0.833], [0.7397, 0.84], [0.8401, 0.771], [0.9453, 0.688]],
		"stations": [
			{"id": "glove_wall_shelf", "pos": [0.0273, 0.667], "landmark": "far-left pearl-crowned pink coral shelf unit holding three rows of red, purple and teal boxing gloves"},
			{"id": "purple_sparring_mat", "pos": [0.1755, 0.813], "landmark": "low round purple sparring mat with a cream scallop-shell emblem, sitting on an orange coral-and-pearl ring base"},
			{"id": "teal_heavy_bag", "pos": [0.5102, 0.792], "landmark": "tall teal heavy bag with cream drum-laced top and scallop-shell crest, on the pink coral-and-pearl ring platform at frame centre"},
			{"id": "shell_pavilion_stage", "pos": [0.6488, 0.611], "landmark": "raised tiled stage in front of the purple scallop-dome pavilion with pearl-studded rim and teal curtains"},
			{"id": "red_heavy_bag", "pos": [0.8047, 0.781], "landmark": "tall coral-red heavy bag in a gold-trimmed purple cradle frame, on the purple coral-and-pearl ring platform right of centre"},
		],
		"clue_spots": [[0.121, 0.194], [0.2233, 0.486], [0.3161, 0.275], [0.5503, 0.236], [0.7062, 0.403], [0.9596, 0.34], [0.8831, 0.833], [0.2137, 0.872]],
	},
	"magician": {
		"path": [[0.145, 0.628], [0.204, 0.635], [0.281, 0.643], [0.357, 0.654], [0.434, 0.667], [0.51, 0.675], [0.577, 0.679], [0.644, 0.676], [0.703, 0.668], [0.746, 0.658]],
		"stations": [
			{"id": "violet_shell_stage", "pos": [0.154, 0.631], "landmark": "Pale sand in front of the violet/plum curtained shell stage on the left - domed canopy topped by a pink scallop shell with a big pearl, gold-scrolled base with a scallop medallion, pearl-knobbed steps on its right"},
			{"id": "pearl_tide_pool", "pos": [0.324, 0.647], "landmark": "Gold-rimmed edge of the blue stepping-stone tide pool in the left foreground - flat lavender-blue stones and loose pearls set in dark water, ringed by purple kelp and pink tube coral"},
			{"id": "teal_shell_stage", "pos": [0.508, 0.653], "landmark": "Sand directly in front of the centre teal/turquoise curtained shell stage - mint shell crown with a pearl, gold-swagged teal curtains, three-step teal stair with pearl newel posts"},
			{"id": "pearl_lamp_avenue", "pos": [0.644, 0.676], "landmark": "Foot of the tall gold lamppost with a glowing white pearl globe that stands in the kelp bed between the teal and rose stages, just above the gold-filigree border of the right-hand coral bed"},
			{"id": "rose_shell_stage", "pos": [0.743, 0.658], "landmark": "Sand at the foot of the rose/coral curtained shell stage on the right - salmon shell crown with a pearl, pink columns with pearl collars, cream-and-coral steps (the destination dais)"},
		],
		"clue_spots": [[0.037, 0.479], [0.083, 0.774], [0.219, 0.287], [0.242, 0.794], [0.508, 0.297], [0.633, 0.447], [0.827, 0.832], [0.94, 0.733]],
	},
	"painter": {
		"path": [[0.0464, 0.6278], [0.1181, 0.6556], [0.2185, 0.6667], [0.3237, 0.675], [0.4289, 0.6792], [0.5312, 0.6792], [0.6326, 0.6667], [0.7186, 0.6278], [0.754, 0.5167], [0.8888, 0.4889]],
		"stations": [
			{"id": "purple_paint_pot", "pos": [0.1631, 0.6417], "landmark": "giant purple paint pot with drip glaze and a pink starfish badge, on a round purple stone pedestal ringed by purple paint-splat pebbles, left of centre"},
			{"id": "gazebo_easel", "pos": [0.3744, 0.4583], "landmark": "foot of the stepped pink dais under the coral-domed gazebo that shelters a blank wooden easel canvas"},
			{"id": "coral_paint_pot", "pos": [0.5083, 0.6417], "landmark": "giant salmon/coral paint pot with drip glaze and flower badge on its round stone pedestal, dead centre of the sand plaza"},
			{"id": "rainbow_brush", "pos": [0.6709, 0.4069], "landmark": "stepped plum pedestal of the giant wooden paintbrush whose rainbow bristles pour coloured paint rivers across the seabed"},
			{"id": "arch_easel", "pos": [0.8888, 0.4889], "landmark": "cream dais under the pearl-crested scallop arch, beside the tall wooden easel and its palette, far right"},
		],
		"clue_spots": [[0.0588, 0.4069], [0.1095, 0.1319], [0.2912, 0.8056], [0.3744, 0.3167], [0.536, 0.2083], [0.5695, 0.4472], [0.7904, 0.8125], [0.9529, 0.4472]],
	},
	"astronaut": {
		"path": [[0.0168, 0.5944], [0.0942, 0.6528], [0.1946, 0.675], [0.3094, 0.6667], [0.4624, 0.6792], [0.5771, 0.675], [0.6727, 0.6625], [0.7492, 0.6472], [0.8544, 0.5347], [0.8975, 0.4278]],
		"stations": [
			{"id": "coolant_tank_pad", "pos": [0.1707, 0.6778], "landmark": "long horizontal chrome cylinder tank clamped in two studded purple flanges, standing on the left round dais with a teal five-petal flower hatch in front of it"},
			{"id": "pipe_arch_planter", "pos": [0.3237, 0.5486], "landmark": "tiered round purple-stone planter mounded with orange and yellow tube corals, directly under the big blue glass pipe arch that runs down from the left dome habitat"},
			{"id": "periscope_elbow", "pos": [0.4719, 0.6778], "landmark": "tall chrome elbow/periscope pipe with riveted purple collars on the centre round dais, pink flower hatch in front of it"},
			{"id": "airlock_ring", "pos": [0.7492, 0.6472], "landmark": "giant white torus / airlock hoop banded with four studded purple straps, on the right round dais with the blue flower hatch"},
			{"id": "rocket_launch_dais", "pos": [0.8946, 0.425], "landmark": "cream rocket with red nose cone and red fins, blue star porthole and arched red doorway, standing on the raised oval launch dais at the far right, at the foot of its blue steps"},
		],
		"clue_spots": [[0.0722, 0.8083], [0.1726, 0.2514], [0.2711, 0.1417], [0.4002, 0.8056], [0.4738, 0.375], [0.6087, 0.8028], [0.7645, 0.1639], [0.9357, 0.5]],
	},
	"racer": {
		"path": [[0.145, 0.701], [0.175, 0.728], [0.242, 0.75], [0.318, 0.758], [0.399, 0.761], [0.481, 0.758], [0.564, 0.767], [0.639, 0.803], [0.717, 0.81], [0.844, 0.761]],
		"stations": [
			{"id": "pearl_start_arch", "pos": [0.156, 0.711], "landmark": "giant cream scallop-shell start arch rimmed with pearls, spanning the aqua race canal at the far left; its foot stands on dark purple rock slabs behind a big red-coral cluster"},
			{"id": "teal_gem_buoy", "pos": [0.304, 0.757], "landmark": "first floating gate marker in the canal - a gold ring buoy on a pearl-studded lilac float, crowned with a large teal gemstone (station stands on the sand beach directly in front of it)"},
			{"id": "pearl_dome_pavilion", "pos": [0.481, 0.758], "landmark": "purple pearl-domed rotunda pavilion on the sand infield across the canal, white columns and a short flight of steps down to the paddock sand"},
			{"id": "rose_gem_buoy", "pos": [0.671, 0.811], "landmark": "third floating gate marker - gold ring buoy with a big magenta/rose gemstone; the beach in front of it holds a pale ribbed urchin and a purple rock mound with teal tube corals"},
			{"id": "ribbon_finish_arch", "pos": [0.844, 0.761], "landmark": "big scallop-shell finish arch tied with a pink-and-white checkered ribbon banner and a fat pink bow, rising over the purple rock terrace at the right"},
		],
		"clue_spots": [[0.159, 0.181], [0.176, 0.817], [0.285, 0.176], [0.432, 0.869], [0.534, 0.199], [0.498, 0.535], [0.733, 0.261], [0.883, 0.718]],
	},
	"popstar": {
		"path": [[0.038, 0.648], [0.094, 0.658], [0.18, 0.667], [0.299, 0.662], [0.409, 0.672], [0.504, 0.68], [0.605, 0.678], [0.69, 0.672], [0.8, 0.666], [0.929, 0.656]],
		"stations": [
			{"id": "shell_stage", "pos": [0.182, 0.666], "landmark": "giant scallop-shell concert stage on the left: cream shell arch studded with pearls over a purple fan interior, pearl-swag garland, a big pearl on a blue cushion at its lip, flanked by two stacks of round teal-and-gold speaker cabinets, cream steps down to the sand"},
			{"id": "clam_coral_bed", "pos": [0.299, 0.66], "landmark": "violet fan clam with a gold clasp and an orange starfish on the lavender rock ledge between the shell stage and the gazebo, orange branch coral rising behind it"},
			{"id": "mic_gazebo", "pos": [0.504, 0.68], "landmark": "centre bandstand gazebo: pink domed roof with a pearl finial, pearl-shell trim and pearl swags, red coral columns, a gold vintage microphone standing on a blue disc in front of a purple scallop backdrop, cream steps to the sand"},
			{"id": "pink_clam_reef", "pos": [0.688, 0.672], "landmark": "large pink fan clam with a pearl in its hinge on the reef ledge between the gazebo and the dome, orange branch coral and a purple fan shell beside it"},
			{"id": "record_dais", "pos": [0.809, 0.664], "landmark": "round vinyl-record dance floor (purple and blue disc with a swirl label) on the raised dais in front of the aqua glass dome pavilion with its ivory scrolled archway and gold treble clef on top"},
		],
		"clue_spots": [[0.035, 0.285], [0.192, 0.82], [0.262, 0.226], [0.319, 0.824], [0.504, 0.257], [0.635, 0.86], [0.833, 0.256], [0.962, 0.286]],
	},
	"nursery": {
		"path": [[0.07, 0.73], [0.16, 0.70], [0.28, 0.68], [0.42, 0.69], [0.55, 0.70], [0.68, 0.67], [0.80, 0.69], [0.91, 0.72]],
		"stations": [
			{"id": "wash_basin", "pos": [0.18, 0.70], "landmark": "pearl wash basin beside the small moon-shell nursery"},
			{"id": "cuddle_cushions", "pos": [0.43, 0.69], "landmark": "soft moon and star cushions in the open central play space"},
			{"id": "bottle_nook", "pos": [0.66, 0.67], "landmark": "round bottle nook with four warm bottles under its lavender canopy"},
			{"id": "moon_bed", "pos": [0.88, 0.70], "landmark": "large moon-and-star bed inside the right shell room"},
		],
		"clue_spots": [[0.12, 0.28], [0.28, 0.43], [0.42, 0.35], [0.56, 0.24], [0.66, 0.50], [0.79, 0.32], [0.88, 0.52], [0.93, 0.78]],
	},
}

## Explicit diegetic anchors audited against all thirteen painted rooms at
## 1280x720 (2026-08-09). PHASE_STATIONS has 53 playable phase bindings sharing
## 45 physical landmarks; every one of those landmarks has an authored object
## centre, conservative maximum hotspot-art size, and safe feet approach here.
## This prevents a bowl, bed, stage, arch, or raised machine from inheriting the
## old generic `feet - 82px` guess and floating over unrelated scenery.
##
## Coordinates remain normalized to the sharp painting and receive the same
## BLEED transform as every other Opera landmark. `object` is the centre of the
## isolated glowing object art. `visual_size` is the largest playable phase art
## shown at that landmark. The final `spur` point is Roshan's safe feet position;
## the first point is on PATHS[path], and intermediate points follow painted
## floor, stairs, or apron space.
const STATION_NAV: Dictionary = {
	"teacher": {
		"lesson_desk": {"object": [0.58, 0.46], "visual_size": [190.0, 190.0],
			"hotspot_size": [220.0, 220.0], "spur": [[0.49, 0.72], [0.49, 0.70]]},
	},
	"geologist": {
		"layer_wall": {
			"object": [0.20, 0.40], "visual_size": [166.0, 152.0],
			"spur": [[0.30, 0.66], [0.35, 0.69]],
		},
		"fossil_table": {
			"object": [0.38, 0.43], "visual_size": [154.0, 124.0],
			"spur": [[0.56, 0.66], [0.57, 0.68]],
		},
		"specimen_trays": {
			"object": [0.65, 0.43], "visual_size": [166.0, 116.0],
			"spur": [[0.56, 0.66], [0.51, 0.69]],
		},
		"crystal_gallery": {
			"object": [0.91, 0.30], "visual_size": [154.0, 166.0],
			"spur": [[0.83, 0.61], [0.76, 0.64]],
		},
	},
	"chef": {
		"mixing_bowl": {
			"object": [0.28, 0.42], "visual_size": [126.0, 126.0],
			"spur": [[0.4, 0.59], [0.41, 0.61]],
		},
		"hearth_oven": {
			"object": [0.475, 0.45], "visual_size": [150.0, 150.0],
			"spur": [[0.615, 0.565], [0.62, 0.59]],
		},
		"grand_cake_stage": {
			"object": [0.86, 0.40], "visual_size": [150.0, 150.0],
			"spur": [[0.7, 0.545], [0.72, 0.57]],
		},
	},
	"detective": {
		"magnifier_tower": {
			"object": [0.65, 0.15], "visual_size": [136.0, 136.0],
			"spur": [[0.78, 0.54], [0.79, 0.57]],
		},
		"evidence_shelves": {
			"object": [0.20, 0.38], "visual_size": [210.0, 70.0],
			"spur": [[0.3, 0.56], [0.38, 0.59]],
		},
		"treasure_dais": {
			"object": [0.93, 0.44], "visual_size": [148.0, 148.0],
			"spur": [[0.78, 0.54], [0.79, 0.57]],
		},
	},
	"ballerina": {
		"shell_bandstand": {
			"object": [0.44, 0.37], "visual_size": [210.0, 70.0],
			"spur": [[0.62, 0.52], [0.61, 0.55]],
		},
		"trifold_mirror": {
			"object": [0.67, 0.36], "visual_size": [140.0, 140.0],
			"spur": [[0.49, 0.6], [0.51, 0.56]],
		},
		"wave_tuffets": {
			"object": [0.24, 0.63], "visual_size": [142.0, 142.0],
			"spur": [[0.38, 0.62], [0.37, 0.65]],
		},
		"rose_finale_stage": {
			"object": [0.91, 0.27], "visual_size": [142.0, 142.0],
			"spur": [[0.7, 0.5], [0.75, 0.48]],
		},
	},
	"candymaker": {
		"gumball_vat": {
			"object": [0.245, 0.35], "visual_size": [120.0, 120.0],
			"spur": [[0.245, 0.715], [0.27, 0.74]],
		},
		"taffy_press": {
			"object": [0.42, 0.57], "visual_size": [104.0, 104.0],
			"spur": [[0.54, 0.75], [0.56, 0.78]],
		},
		"candy_bag_cottage": {
			"object": [0.62, 0.57], "visual_size": [124.0, 124.0],
			"spur": [[0.54, 0.75], [0.49, 0.77]],
		},
		"candy_cart": {
			"object": [0.9, 0.68], "visual_size": [112.0, 112.0],
			"spur": [[0.75, 0.72], [0.77, 0.76]],
		},
	},
	"doctor": {
		"stethoscope_clinic": {
			"object": [0.21, 0.30], "visual_size": [220.0, 131.0],
			"spur": [[0.35, 0.585], [0.39, 0.61]],
		},
		"starfish_triage": {
			"object": [0.075, 0.52], "visual_size": [136.0, 136.0],
			"spur": [[0.21, 0.595], [0.22, 0.62]],
		},
		"exam_booth": {
			"object": [0.578, 0.46], "visual_size": [136.0, 136.0],
			"spur": [[0.745, 0.73], [0.72, 0.75]],
		},
		"recovery_bed": {
			"object": [0.86, 0.79], "visual_size": [112.0, 112.0],
			"spur": [[0.745, 0.73], [0.73, 0.75]],
		},
	},
	"farmer": {
		"barn_doors": {
			"object": [0.1542, 0.32], "visual_size": [126.0, 126.0],
			"spur": [[0.2901, 0.5361], [0.30, 0.56]],
		},
		"pearl_clam": {
			"object": [0.1035, 0.75],
			"visual_size": [124.0, 124.0],
			"hotspot_size": [196.0, 176.0],
			"spur": [[0.0795, 0.4833], [0.09, 0.58], [0.115, 0.69]],
		},
		"blossom_arch": {
			"object": [0.4585, 0.35],
			"visual_size": [120.0, 120.0],
			"hotspot_size": [188.0, 184.0],
			"spur": [[0.4528, 0.6111], [0.52, 0.63], [0.60, 0.65]],
		},
		"seed_beds": {
			"object": [0.7092, 0.68],
			"visual_size": [104.0, 104.0],
			"hotspot_size": [184.0, 148.0],
			"spur": [[0.558, 0.7569], [0.56, 0.79]],
		},
		"hay_bales": {
			"object": [0.8929, 0.35],
			"visual_size": [100.0, 100.0],
			"hotspot_size": [196.0, 216.0],
			"spur": [[0.8068, 0.7333], [0.78, 0.65], [0.74, 0.58]],
		},
	},
	"boxer": {
		"glove_wall_shelf": {
			"object": [0.075, 0.50],
			"visual_size": [154.0, 176.0],
			"hotspot_size": [196.0, 216.0],
			"spur": [[0.3189, 0.889], [0.29, 0.86]],
		},
		"purple_sparring_mat": {
			"object": [0.1755, 0.64], "visual_size": [128.0, 128.0],
			"spur": [[0.3189, 0.889], [0.32, 0.86]],
		},
		"teal_heavy_bag": {
			"object": [0.5102, 0.62],
			"visual_size": [116.0, 176.0],
			"hotspot_size": [176.0, 212.0],
			"spur": [[0.7397, 0.84], [0.72, 0.82]],
		},
		"shell_pavilion_stage": {
			"object": [0.6488, 0.40],
			"visual_size": [154.0, 154.0],
			"hotspot_size": [216.0, 188.0],
			"spur": [[0.8401, 0.771], [0.80, 0.79]],
		},
	},
	"magician": {
		"violet_shell_stage": {
			"object": [0.154, 0.43], "visual_size": [138.0, 138.0],
			"spur": [[0.281, 0.643], [0.30, 0.67]],
		},
		"pearl_tide_pool": {
			"object": [0.324, 0.78], "visual_size": [120.0, 120.0],
			"spur": [[0.281, 0.643], [0.324, 0.647]],
		},
		"teal_shell_stage": {
			"object": [0.508, 0.43], "visual_size": [208.0, 52.0],
			"spur": [[0.357, 0.654], [0.34, 0.68]],
		},
		"rose_shell_stage": {
			"object": [0.743, 0.43], "visual_size": [150.0, 150.0],
			"spur": [[0.577, 0.679], [0.59, 0.70]],
		},
	},
	"painter": {
		"gazebo_easel": {
			"object": [0.3744, 0.29],
			"visual_size": [136.0, 136.0],
			"hotspot_size": [196.0, 208.0],
			"spur": [[0.5312, 0.6792], [0.52, 0.70]],
		},
		"rainbow_brush": {
			"object": [0.6709, 0.25],
			"visual_size": [88.0, 88.0],
			"hotspot_size": [192.0, 224.0],
			"spur": [[0.754, 0.5167], [0.79, 0.54]],
		},
		"arch_easel": {
			"object": [0.8888, 0.35], "visual_size": [142.0, 142.0],
			"spur": [[0.7186, 0.6278], [0.74, 0.65]],
		},
	},
	"astronaut": {
		"coolant_tank_pad": {
			"object": [0.1707, 0.50], "visual_size": [124.0, 124.0],
			"spur": [[0.3094, 0.6667], [0.31, 0.69]],
		},
		"pipe_arch_planter": {
			"object": [0.3237, 0.43],
			"visual_size": [98.0, 98.0],
			"hotspot_size": [196.0, 184.0],
			"spur": [[0.4624, 0.6792], [0.46, 0.70]],
		},
		"periscope_elbow": {
			"object": [0.4719, 0.49], "visual_size": [124.0, 124.0],
			"spur": [[0.5771, 0.675], [0.61, 0.70]],
		},
		"rocket_launch_dais": {
			"object": [0.8946, 0.25], "visual_size": [144.0, 144.0],
			"spur": [[0.7492, 0.6472], [0.76, 0.67]],
		},
	},
	"racer": {
		"pearl_dome_pavilion": {
			"object": [0.481, 0.38], "visual_size": [110.0, 110.0],
			"spur": [[0.481, 0.758], [0.50, 0.78]],
		},
		"pearl_start_arch": {
			"object": [0.156, 0.52], "visual_size": [138.0, 138.0],
			"spur": [[0.318, 0.758], [0.31, 0.78]],
		},
		"ribbon_finish_arch": {
			"object": [0.844, 0.52], "visual_size": [140.0, 140.0],
			"spur": [[0.717, 0.81], [0.70, 0.83]],
		},
	},
	"nursery": {
		"wash_basin": {
			"object": [0.18, 0.55], "visual_size": [220.0, 131.0],
			"spur": [[0.28, 0.68], [0.36, 0.72]],
		},
		"cuddle_cushions": {
			"object": [0.43, 0.57], "visual_size": [118.0, 118.0],
			"spur": [[0.55, 0.70], [0.57, 0.72]],
		},
		"bottle_nook": {
			"object": [0.66, 0.46], "visual_size": [108.0, 108.0],
			"spur": [[0.55, 0.70], [0.52, 0.72]],
		},
		"moon_bed": {
			"object": [0.86, 0.43], "visual_size": [150.0, 150.0],
			"spur": [[0.68, 0.67], [0.70, 0.70]],
		},
	},
	"popstar": {
		"mic_gazebo": {
			"object": [0.504, 0.52], "visual_size": [142.0, 142.0],
			"spur": [[0.605, 0.678], [0.65, 0.70]],
		},
		"record_dais": {
			"object": [0.809, 0.56], "visual_size": [120.0, 120.0],
			"spur": [[0.69, 0.672], [0.67, 0.70]],
		},
		"shell_stage": {
			"object": [0.182, 0.47], "visual_size": [142.0, 142.0],
			"spur": [[0.299, 0.662], [0.32, 0.69]],
		},
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
	"farmer": [0.12, 0.86],
	"boxer": [0.12, 0.88],
	"magician": [0.14, 0.85],
	"painter": [0.1, 0.82],
	"astronaut": [0.1, 0.87],
	"racer": [0.18, 0.82],
	"popstar": [0.1, 0.82],
	"nursery": [0.15, 0.85],
}


static func roam_range(career: String) -> Vector2:
	var entry: Array = ROAM.get(career, [0.14, 0.86])
	return Vector2(float(entry[0]), float(entry[1]))


## Horizontal span the painting actually occupies on screen, per career.
##
## The four world_<career>_c{0,1}r{0,1}.png tiles compose into a 2048-square
## master, and opera_world_backdrop_2d.gd:66-75 draws master y=448..1600 across
## the whole 1280x720 screen. Vertically that crop IS the sharp band, so a
## painting-normalized y maps straight through. Horizontally the artwork is
## inset inside a blurred bleed margin of roughly 9% a side, so a coordinate
## derived from the painting has to be remapped onto the span the painting
## really covers — otherwise every station drifts outward, by nothing at centre
## and up to ~115px at the edges (measured against 30 stations across five
## careers, 2026-08-04).
##
## Regenerate with tools/measure_opera_bleed.py after any world repaint.
const BLEED: Dictionary = {
	"chef": [0.0913, 0.9077],
	"detective": [0.0913, 0.9077],
	"ballerina": [0.0942, 0.9038],
	"candymaker": [0.0942, 0.9038],
	"doctor": [0.0913, 0.9077],
	"farmer": [0.0952, 0.9038],
	"boxer": [0.0938, 0.9043],
	"magician": [0.0947, 0.9038],
	"painter": [0.0947, 0.9048],
	"astronaut": [0.0913, 0.9028],
	"racer": [0.0947, 0.9038],
	"popstar": [0.0957, 0.9023],
	"nursery": [0.0947, 0.9077],
}


static func bleed_span(career: String) -> Vector2:
	var entry: Array = BLEED.get(career, [0.0936, 0.9049])
	return Vector2(float(entry[0]), float(entry[1]))


## Painting-normalized (0..1 across the sharp artwork) -> screen pixels.
static func to_screen(career: String, normalized: Vector2) -> Vector2:
	var span := bleed_span(career)
	return Vector2(
		(span.x + (span.y - span.x) * normalized.x) * SCREEN.x,
		normalized.y * SCREEN.y
	)


const FALLBACK_PATH := [
	[0.08, 0.72], [0.22, 0.66], [0.38, 0.70], [0.52, 0.64],
	[0.66, 0.70], [0.80, 0.65], [0.92, 0.70],
]
const FALLBACK_STATION_T := [0.10, 0.34, 0.58, 0.82]


static func path_points(career: String) -> PackedVector2Array:
	var raw: Array = (PATHS.get(career, {}) as Dictionary).get("path", FALLBACK_PATH)
	var points := PackedVector2Array()
	for entry: Array in raw:
		points.append(to_screen(career, Vector2(float(entry[0]), float(entry[1]))))
	return points


static func stations(career: String) -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	var raw: Array = (PATHS.get(career, {}) as Dictionary).get("stations", [])
	if raw.is_empty():
		var points: PackedVector2Array = path_points(career)
		for index in range(FALLBACK_STATION_T.size()):
			var station_id := "station_%d" % index
			var legacy_pos := point_along(
				points, float(FALLBACK_STATION_T[index]))
			var navigation := _station_navigation(
				career, station_id, legacy_pos)
			out.append({
				"id": station_id,
				# Compatibility contract: `pos` remains the exact value returned by
				# this API before station navigation was added.
				"pos": legacy_pos,
				"landmark": "stage landmark",
				"approach_pos": navigation["approach_pos"],
				"object_pos": navigation["object_pos"],
				"visual_size": navigation["visual_size"],
				"hotspot_size": navigation["hotspot_size"],
				"spine_t": navigation["spine_t"],
				"spur": navigation["spur"],
				"route": navigation["spur"],
				"authored_object": navigation["authored_object"],
				"authored_spur": navigation["authored_spur"],
			})
		return out
	for entry: Dictionary in raw:
		var pos: Array = entry.get("pos", [0.5, 0.68])
		var station_id := String(entry.get("id", "station"))
		var legacy_pos := to_screen(
			career, Vector2(float(pos[0]), float(pos[1])))
		var navigation := _station_navigation(
			career, station_id, legacy_pos)
		out.append({
			"id": station_id,
			# Keep existing callers stable while new movement uses approach_pos
			# and new hotspot art uses object_pos.
			"pos": legacy_pos,
			"landmark": String(entry.get("landmark", "")),
			"approach_pos": navigation["approach_pos"],
			"object_pos": navigation["object_pos"],
			"visual_size": navigation["visual_size"],
			"hotspot_size": navigation["hotspot_size"],
			"spine_t": navigation["spine_t"],
			"spur": navigation["spur"],
			"route": navigation["spur"],
			"authored_object": navigation["authored_object"],
			"authored_spur": navigation["authored_spur"],
		})
	return out


static func clue_spots(career: String) -> PackedVector2Array:
	var out := PackedVector2Array()
	var raw: Array = (PATHS.get(career, {}) as Dictionary).get("clue_spots", [])
	if raw.is_empty():
		# spread fallback sparkle spots across the stage
		for index in range(8):
			out.append(to_screen(career, Vector2(
				0.12 + 0.76 * float(index) / 7.0,
				0.30 + 0.35 * float((index * 3) % 5) / 4.0
			)))
		return out
	for entry: Array in raw:
		out.append(to_screen(career, Vector2(float(entry[0]), float(entry[1]))))
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


## Complete navigation record for one station. This is deliberately generated
## from the same fixed-space data as `stations()` so gameplay, hit-testing and
## probes cannot quietly disagree about a landmark's coordinate transform.
static func _station_navigation(career: String, station_id: String,
		legacy_pos: Vector2) -> Dictionary:
	var career_navigation: Dictionary = STATION_NAV.get(career, {})
	var authored: Dictionary = career_navigation.get(station_id, {})
	# Non-playable/fallback stations retain a conservative estimate. Every
	# PHASE_STATIONS landmark is required by the focused probe to override it
	# with a painted semantic centre and an authored safe approach.
	var object_pos := Vector2(
		clampf(legacy_pos.x, 92.0, SCREEN.x - 92.0),
		clampf(legacy_pos.y - 82.0, 92.0, SCREEN.y - 92.0))
	var raw_object: Array = authored.get("object", [])
	var authored_object := raw_object.size() >= 2
	if authored_object:
		object_pos = to_screen(career, Vector2(
			float(raw_object[0]), float(raw_object[1])))
	var visual_size := Vector2(124.0, 124.0)
	var raw_visual: Array = authored.get("visual_size", [])
	if raw_visual.size() >= 2:
		visual_size = Vector2(
			clampf(float(raw_visual[0]), 48.0, 220.0),
			clampf(float(raw_visual[1]), 48.0, 220.0))
	# The hit target encloses the complete visual with padding while retaining a
	# generous square minimum for small objects and one-finger phone use.
	var hotspot_size := Vector2(
		maxf(156.0, visual_size.x + 28.0),
		maxf(156.0, visual_size.y + 28.0))
	var raw_hotspot: Array = authored.get("hotspot_size", [])
	if raw_hotspot.size() >= 2:
		hotspot_size = Vector2(
			maxf(visual_size.x + 24.0,
				maxf(112.0, float(raw_hotspot[0]))),
			maxf(visual_size.y + 24.0,
				maxf(112.0, float(raw_hotspot[1]))))

	var spine := path_points(career)
	var spur := PackedVector2Array()
	var raw_spur: Array = authored.get("spur", [])
	for raw_point: Array in raw_spur:
		if raw_point.size() >= 2:
			spur.append(to_screen(career, Vector2(
				float(raw_point[0]), float(raw_point[1]))))
	var authored_spur := not spur.is_empty()
	if authored_spur:
		# Lock the connection to the mathematical spine. Authored values name an
		# existing spine point, but this projection also absorbs decimal/export
		# noise and makes the probe invariant exact.
		var connection_t := nearest_t(spine, spur[0])
		spur[0] = point_along(spine, connection_t)
	else:
		var connection_t := nearest_t(spine, legacy_pos)
		var connection := point_along(spine, connection_t)
		spur.append(connection)
		if connection.distance_to(legacy_pos) > 0.01:
			spur.append(legacy_pos)
	if spur.is_empty():
		spur.append(legacy_pos)
	var approach_pos: Vector2 = spur[spur.size() - 1]
	var spine_t := nearest_t(spine, spur[0])
	return {
		"approach_pos": approach_pos,
		"object_pos": object_pos,
		"visual_size": visual_size,
		"hotspot_size": hotspot_size,
		"spine_t": spine_t,
		"spur": spur,
		"authored_object": authored_object,
		"authored_spur": authored_spur,
	}


static func station_by_id(career: String, station_id: String) -> Dictionary:
	for entry: Dictionary in stations(career):
		if String(entry.get("id", "")) == station_id:
			return entry
	return {}


static func station_approach(career: String, station_id: String) -> Vector2:
	var entry := station_by_id(career, station_id)
	return entry.get("approach_pos", SCREEN * 0.5) as Vector2 \
		if not entry.is_empty() else SCREEN * 0.5


static func station_object_position(career: String,
		station_id: String) -> Vector2:
	var entry := station_by_id(career, station_id)
	return entry.get("object_pos", SCREEN * 0.5) as Vector2 \
		if not entry.is_empty() else SCREEN * 0.5


static func station_visual_size(career: String,
		station_id: String) -> Vector2:
	var entry := station_by_id(career, station_id)
	return entry.get("visual_size", Vector2(124.0, 124.0)) as Vector2 \
		if not entry.is_empty() else Vector2(124.0, 124.0)


static func station_spur(career: String,
		station_id: String) -> PackedVector2Array:
	var entry := station_by_id(career, station_id)
	return entry.get("spur", PackedVector2Array()) as PackedVector2Array \
		if not entry.is_empty() else PackedVector2Array()


## Approved network branches in screen space. The first branch is always the
## ordered promenade spine; every following branch begins exactly on that spine
## and ends at a station's safe approach.
static func approved_route_branches(career: String) -> Array[Dictionary]:
	var branches: Array[Dictionary] = [{
		"id": "__spine",
		"points": path_points(career),
		"spine_t": 0.0,
	}]
	for entry: Dictionary in stations(career):
		var spur: PackedVector2Array = entry.get(
			"spur", PackedVector2Array()) as PackedVector2Array
		if spur.size() < 2:
			continue
		branches.append({
			"id": String(entry.get("id", "")),
			"points": spur,
			"spine_t": float(entry.get("spine_t", 0.0)),
		})
	return branches


## Point, parameter and branch nearest to an arbitrary screen-space touch.
## Callers should move to the returned point instead of to the untrusted touch.
static func nearest_approved_point(career: String,
		position: Vector2) -> Dictionary:
	var best: Dictionary = {}
	var best_distance := INF
	for branch: Dictionary in approved_route_branches(career):
		var points: PackedVector2Array = branch.get(
			"points", PackedVector2Array()) as PackedVector2Array
		var candidate := _nearest_on_polyline(points, position)
		var distance := float(candidate.get("distance", INF))
		if distance < best_distance:
			best_distance = distance
			best = candidate
			best["branch_id"] = String(branch.get("id", "__spine"))
			best["points"] = points
			best["spine_t"] = float(branch.get("spine_t", 0.0))
	return best


## Deterministic player route for an empty-floor touch. Both endpoints are
## projected to the approved network, then connected through the full ordered
## spine and any required station spurs. No direct start/end chord is emitted.
static func player_route_to_point(career: String, from: Vector2,
		target: Vector2) -> PackedVector2Array:
	var source := nearest_approved_point(career, from)
	var destination := nearest_approved_point(career, target)
	if source.is_empty() or destination.is_empty():
		return PackedVector2Array()
	return _route_between(career, source, destination)


## Deterministic route to a station's safe feet position. The object centre is
## never used as a walk target because many landmarks are raised scenery.
static func player_route_to_station(career: String, from: Vector2,
		station_id: String) -> PackedVector2Array:
	var entry := station_by_id(career, station_id)
	if entry.is_empty():
		return PackedVector2Array()
	var source := nearest_approved_point(career, from)
	if source.is_empty():
		return PackedVector2Array()
	var spur: PackedVector2Array = entry.get(
		"spur", PackedVector2Array()) as PackedVector2Array
	var destination: Dictionary
	if spur.size() >= 2:
		destination = {
			"branch_id": station_id,
			"points": spur,
			"point": spur[spur.size() - 1],
			"t": 1.0,
			"distance": 0.0,
			"spine_t": float(entry.get("spine_t", 0.0)),
		}
	else:
		destination = nearest_approved_point(
			career, entry.get("approach_pos", entry["pos"]) as Vector2)
	return _route_between(career, source, destination)


## Probe helper: a point passes only when it lies on a declared spine/spur
## edge, within the supplied screen-pixel tolerance.
static func point_is_on_approved_route(career: String, point: Vector2,
		tolerance: float = 1.0) -> bool:
	var nearest := nearest_approved_point(career, point)
	return not nearest.is_empty() \
		and float(nearest.get("distance", INF)) <= maxf(0.01, tolerance)


## Probe helper: samples every emitted segment, not just its endpoints. This
## catches the old failure where two valid route points were joined by an
## invalid chord across a curved bridge or pool.
static func route_is_approved(career: String, route: PackedVector2Array,
		tolerance: float = 1.0) -> bool:
	if route.is_empty():
		return false
	if not point_is_on_approved_route(career, route[0], tolerance):
		return false
	for index in range(1, route.size()):
		var start := route[index - 1]
		var finish := route[index]
		var samples := maxi(1, int(ceilf(start.distance_to(finish) / 12.0)))
		for sample_index in range(1, samples + 1):
			var sample := start.lerp(
				finish, float(sample_index) / float(samples))
			if not point_is_on_approved_route(career, sample, tolerance):
				return false
	return true


static func _nearest_on_polyline(points: PackedVector2Array,
		position: Vector2) -> Dictionary:
	if points.is_empty():
		return {}
	if points.size() == 1:
		return {
			"point": points[0],
			"t": 0.0,
			"distance": points[0].distance_to(position),
			"segment": 0,
		}
	var best_point := points[0]
	var best_t := 0.0
	var best_distance := INF
	var best_segment := 0
	var walked := 0.0
	var total := path_length(points)
	for index in range(1, points.size()):
		var start := points[index - 1]
		var finish := points[index]
		var segment_length := start.distance_to(finish)
		var local_t := 0.0
		if segment_length > 0.0:
			local_t = clampf(
				(position - start).dot(finish - start)
					/ (segment_length * segment_length), 0.0, 1.0)
		var candidate := start.lerp(finish, local_t)
		var distance := candidate.distance_to(position)
		if distance < best_distance:
			best_point = candidate
			best_distance = distance
			best_t = (walked + local_t * segment_length) / total
			best_segment = index - 1
		walked += segment_length
	return {
		"point": best_point,
		"t": best_t,
		"distance": best_distance,
		"segment": best_segment,
	}


static func _route_between(career: String, source: Dictionary,
		destination: Dictionary) -> PackedVector2Array:
	var source_id := String(source.get("branch_id", "__spine"))
	var destination_id := String(destination.get("branch_id", "__spine"))
	var source_points: PackedVector2Array = source.get(
		"points", PackedVector2Array()) as PackedVector2Array
	var destination_points: PackedVector2Array = destination.get(
		"points", PackedVector2Array()) as PackedVector2Array
	if source_points.is_empty() or destination_points.is_empty():
		return PackedVector2Array()
	if source_id == destination_id:
		return _polyline_slice(source_points,
			float(source.get("t", 0.0)), float(destination.get("t", 0.0)))

	var route_points: Array[Vector2] = []
	var source_spine_t: float
	if source_id == "__spine":
		source_spine_t = float(source.get("t", 0.0))
	else:
		_append_route_points(route_points, _polyline_slice(
			source_points, float(source.get("t", 0.0)), 0.0))
		source_spine_t = float(source.get("spine_t", 0.0))

	var destination_spine_t: float
	if destination_id == "__spine":
		destination_spine_t = float(destination.get("t", 0.0))
	else:
		destination_spine_t = float(destination.get("spine_t", 0.0))
	_append_route_points(route_points, _polyline_slice(
		path_points(career), source_spine_t, destination_spine_t))
	if destination_id != "__spine":
		_append_route_points(route_points, _polyline_slice(
			destination_points, 0.0, float(destination.get("t", 0.0))))
	return PackedVector2Array(route_points)


## Ordered slice of a polyline. Intermediate authored vertices are retained in
## both directions, which is the invariant that prevents corner-cutting.
static func _polyline_slice(points: PackedVector2Array, from_t: float,
		to_t: float) -> PackedVector2Array:
	if points.is_empty():
		return PackedVector2Array()
	if points.size() == 1:
		return PackedVector2Array([points[0]])
	var start_t := clampf(from_t, 0.0, 1.0)
	var finish_t := clampf(to_t, 0.0, 1.0)
	var total := path_length(points)
	var vertex_t: Array[float] = [0.0]
	var walked := 0.0
	for index in range(1, points.size()):
		walked += points[index - 1].distance_to(points[index])
		vertex_t.append(walked / total)
	var ordered: Array[Vector2] = []
	_push_unique(ordered, point_along(points, start_t))
	if start_t < finish_t:
		for index in range(1, points.size() - 1):
			if vertex_t[index] > start_t + 0.000001 \
					and vertex_t[index] < finish_t - 0.000001:
				_push_unique(ordered, points[index])
	elif start_t > finish_t:
		for index in range(points.size() - 2, 0, -1):
			if vertex_t[index] < start_t - 0.000001 \
					and vertex_t[index] > finish_t + 0.000001:
				_push_unique(ordered, points[index])
	_push_unique(ordered, point_along(points, finish_t))
	return PackedVector2Array(ordered)


static func _append_route_points(target: Array[Vector2],
		points: PackedVector2Array) -> void:
	for point: Vector2 in points:
		_push_unique(target, point)


static func _push_unique(points: Array[Vector2], point: Vector2) -> void:
	if points.is_empty() or points[points.size() - 1].distance_to(point) > 0.01:
		points.append(point)
