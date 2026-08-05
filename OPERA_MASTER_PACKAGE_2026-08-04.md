# THE OPERA PROGRAMME — master package (2026-08-04)

One document over four open workstreams. It supersedes the coordinate rulings in
`OPERA_WORLD_OBJECT_CENSUS_2026-08-03.md` §0(c)/§5(a) and
`CODEX_OPERA_EXPLORATION_HANDOFF_2026-08-03.md` §1 P0 (§2 below), lands the
re-derived geography for the seven replaced careers (§3), states the two binding
contracts against every new object class in the three open art packages (§4),
adds ten further contemplative tasks that need **zero** new art (§5), merges all
four workstreams into one build order (§6), and lists what only the owner can
decide (§7).

Audience of the game, unchanged and binding on every line below: **one
four-year-old non-reader, one finger, a tablet, no fail states, nothing counted
at her.**

---

## 1. STATUS BOARD

| # | Workstream | Spec | Files outstanding | State | Owner |
|---|---|---|---:|---|---|
| 1 | **Runtime animation pass** | `CODEX_OPERA_ANIMATION_HANDOFF_2026-08-03.md` §14 | **0** | **DELIVERED** — impl `d0a35d3e`, review kit `6325c981`, on `dev`. Owner identity/topology/style review and a real Android Speedy-tier frame capture **still pending** (`adb devices -l` found no device) | Codex → owner |
| 2 | **Integration half** (framing repair, 100 themed audio clips, scale contract, imp roam envelopes, widget ledger, Chapter 2 bible, exploration package) | this run | **0** | **MERGED** — `claude/opera-integration-20260804` → `dev` at `5f5d386c`, probes green (run 30927887299) | us |
| 3 | **Widget art** | `CODEX_OPERA_WIDGET_ART_FULL_AMBITION_2026-08-03.md` + `assets_src/concepts/OPERA_WIDGET_ASSET_LEDGER_2026-08-03.csv` (**221 rows**, verified: P1 8 / P2 27 / P3 180 / P4 6) | **221** | **REQUESTED, 0 delivered.** Engine side is finished and merged (`192122c2`, `cd624567`, `8f10da7d`) — no row waits on code | Codex |
| 4 | **Roshan animation, sheets a + b** | `CODEX_OPERA_ROSHAN_ANIMATION_HANDOFF_2026-08-03.md` | **26** | **REQUESTED, 0 delivered.** 13 × `sheet_a` 2048², 13 × `sheet_b` 2048×1024 | Codex |
| 5 | **Roshan animation, `sheet_c`** | same, proposed by `OPERA_EXPLORATION_DESIGN_2026-08-03.md` §9 | **13** | **PROPOSED — not owner-accepted.** T3/Q1/H4/Y-series all ship without it on `ActorMotion` | owner decides (§7 Q2) |
| 6 | **Exploration art** | `CODEX_OPERA_EXPLORATION_HANDOFF_2026-08-03.md` + `assets_src/concepts/OPERA_EXPLORATION_ASSET_LEDGER_2026-08-03.csv` (**57 rows**, verified: 56 NEW + 1 REUSE; P1 6 / P2 15 / P3 36) | **56** | **REQUESTED, 0 delivered.** `assets/opera/worlds/explore/` does not exist yet; no `helper_*.png` on disk | Codex |
| 7 | **Exploration engine + data** | `OPERA_EXPLORATION_DESIGN_2026-08-03.md` §8, §10 | 0 art | **NOT STARTED.** ~310 lines new engine + 7 new data tables. All line numbers in that document are against the 1755-line `opera_career_world_2d.gd`; it is **2046 lines** today after the animation pass | us |
| 8 | **Coordinate re-derivation** | this document §2, §3 | 0 art | **DERIVED, NOT LANDED.** 7 careers' paths/stations/clue spots + ROAM; the P0 ruling | us |
| 9 | Ambient loops (13 × 2–3 s) + short VO (~130 lines) | exploration handoff §3.8 | 0 art | **DEFERRED, optional.** `AudioDirector._say` degrades to the speaker's generic clip and then to the pitched "yay" | family / us |

**Total outstanding art files: 316** (221 + 26 + 13 + 56). §6 sequences them.

Superseded and dead — do not act on these again:
- census §0(c) and §5(a): "the composed master is 2048×1152" and "apply `0.10 + 0.80×` to **both** u and v". **Both wrong.** §2.
- exploration handoff §1 P0's constants `0.10 + 0.80`. The *decision* (fix in code, not by re-rendering 104 tiles) stands; the constants and the axis do not. §2.
- exploration handoff §6 "Total outstanding 316" — the number is still 316, but the table there predates the runtime animation pass landing. Use §1 above.

---

## 2. THE P0 RULING — settled, not to be re-litigated

**The transform is real, it is horizontal only, and it goes in `OperaStagePaths`.**

```
screen_u = 0.091 + 0.817 * recorded_u        # apply
screen_v = recorded_v                        # identity — already handled
```

### Why horizontal only

`opera_world_backdrop_2d.gd:66-75` composes the four 1024² tiles into a
2048×**2048** master and draws `Rect2(0, 448, 1024, 576)` from each row-0 tile
and `Rect2(0, 0, 1024, 576)` from each row-1 tile — i.e. it already crops master
`y = 448 .. 1600` and maps that 2048×1152 band to the full 1280×720 screen. The
bleed margin is a roughly uniform ~187 px frame on all four sides of the 2048
master; the top margin (0..187) and the bottom margin (1861..2048) both fall
**outside** that crop. Vertical bleed was never on screen. Only the ~187 px
horizontal margin each side was ever in question. The census's "2048×1152
master" was reading the drawn band as if it were the file.

### Why the transform (mapping B, SHARP_RELATIVE) and not identity (mapping A)

Independent verification across 3 agents and 10 stations on two careers, each
landmark centre re-measured on 4–5× ruler-gridded zoom crops rather than
estimated off the overview:

- **8 of 10 stations favour B, and every high-separation station does.**
- **The decider is `doctor/starfish_triage`** (recorded 0.075, mappings 99 px
  apart). The smiling starfish on its purple cushion under the golden shell
  archway occupies screen x 160..208, centre 185; the archway spans 127..233.
  B = 195, dead on the starfish. A = 96 — not merely off the archway but
  **inside the blur**, and column-wise 2nd-derivative energy on the composed
  frame puts sharp content at x 116..1157 (chef) and 119..1157 (doctor), i.e.
  0.091..0.904. A station cannot be anchored to a landmark that is not painted.
  A is refused outright.
- `doctor/stethoscope_clinic` (0.21, 67 px apart): teal dome spans 258..423,
  purple daybed and shell keystone centred 343. B = 336 dead centre; A = 269 off
  the pavilion's left shoulder.
- chef agrees on left/mid: mixing-bowl shell medallion at 403 (B 409 / A 358);
  étagère cakes centred 798 (B 801 / A 838, which lands on the right post);
  glass-domed macaron cart spans 875..950 (B 901 on it / A 960 past it onto the
  blue column).
- **Least squares over all 10 measured centres: `0.081 + 0.861 × recorded`.**
  B is `0.091 + 0.817`. A is `0.0 + 1.0`. RMS error B 26.3 px vs A 49.6 px
  (doctor alone B 20.7 / A 59.0; chef alone B 31.0 / A 37.9).

**The one genuine dissent, reported rather than averaged away:**
`chef/grand_cake_stage` (0.86, 85 px separation). The three-tier cake spans
1020..1140, centre 1080; A = 1101 sits on the cake, B = 1016 sits at the foot of
the carpeted steps ~64 px left. It does not overturn the verdict because
`doctor/recovery_bed` at the *identical* recorded 0.86 goes the other way — the
sunken purple bed-basin spans 1015..1082, centre 1048, so B = 1016 beats
A = 1101 — and because three left-edge stations refuse A outright while nothing
refuses B outright. `doctor/exam_booth` (0.578) and both "ties"
(`chef/hearth_oven` 5 px apart, `doctor/thermometer_garden` 9 px apart) sit in
the centre region where the two mappings agree; they are non-probative by
construction.

### Third confirmation, from the freshly re-derived farmer data

§3's farmer rows were read off the shipped art independently of the above. Their
high-separation stations agree with B and disagree with A:

| Station | recorded u | A (identity) | **B (transform)** | painted truth (census §1 farmer) | winner |
|---|---:|---:|---:|---|---|
| `hay_bales` | 0.8929 | 1143 px | **1050 px** | three round bales span x 0.77–0.88 → 986..1126, centre 1056 | **B by 87 px** |
| `seed_beds` | 0.7092 | 908 px | **858 px** | front-centre tilled oval, column x ≈ 0.655 → 838 | **B by 50 px** |
| `pearl_clam` | 0.1035 | 132 px | **225 px** | tide pool and its rock ledge span screen x 0.15–0.36 → 192..461 | **B — A is 60 px outside the pool** |

Vertical needs no correction on the same rows: `barn_doors` v 0.4556 against a
barn painted at y 0.13–0.42 with the station on the sand apron below it;
`hay_bales` v 0.3889 against bales at y 0.24–0.40; `seed_beds` v 0.6764 against
the front bed row at y ≈ 0.645. Identity, every time.

**Therefore: the seven careers' data in §3 is recorded (painting) space, exactly
like the six shipped rows, and is consumed through the same transform.** Do not
"pre-apply" it. The `unwalkable` prose in §3 is the opposite — it is written in
**screen** fractions and pixels, because it was measured on the composed,
cropped, 1280×720 frame.

### Implementation

One private helper, three call sites, no new public API:

```gdscript
const SHARP_U := Vector2(0.091, 0.817)   # bleed-corrected horizontal span of
                                          # the composed 2048 master (P0, 2026-08-04)

static func _to_screen(u: float, v: float) -> Vector2:
	return Vector2((SHARP_U.x + SHARP_U.y * u) * SCREEN.x, v * SCREEN.y)
```

Called from `path_points()` (`opera_stage_paths.gd:190`), `stations()` (`:198`)
and `clue_spots()` (`:220`), replacing the bare `* SCREEN`. `roam_range()`,
`point_along()` and `nearest_t()` need no change — ROAM is a `t` parameter along
the polyline, not a coordinate, and the other two consume already-converted
points.

Do **not** delete `opera_world_backdrop_2d.gd:103-111` (the single-`painting`
branch). All 13 careers resolve a complete 4-tile set today so it is unreachable,
but it is the correct degradation path if a tile ever fails to import. Add the
comment and a probe assertion that all 13 careers return `world_tiles.size() == 4`;
that is what stops the next derivation pass measuring the wrong file.

### Refinement, recorded and deliberately deferred

The fitted slope 0.861 is wider than B's 0.817 and the fitted offset 0.081
smaller than 0.091, which is why B still drifts 40–65 px left of truth at the
far-right stations of both careers. Widening to `0.081 + 0.861` fits the ten
measured points better. **That is a second-order tune, not a reason to delay
B.** §7 Q1.

---

## 3. THE SEVEN REPLACED CAREERS — re-derived geography

`farmer, boxer, magician, painter, astronaut, racer, popstar` were regenerated as
*different places*, not variations (census §0(b)). Every `landmark` string in the
shipped rows for these seven describes furniture that no longer exists. The
following replaces `PATHS` and `ROAM` rows for all seven, read off the shipped
tiles. Ten waypoints each (shipped rows have nine; `path_points()` is
count-agnostic). Landmark strings are compressed to the shipped register.

Splice these blocks over the existing rows in `scripts/opera_stage_paths.gd:76-152`
(farmer at `:76`, boxer `:87`, magician `:98`, painter `:109`, astronaut `:120`,
racer `:131`, popstar `:142`) and the seven matching keys in `ROAM` (`:161-175`).

```gdscript
	# UNWALKABLE: bottom-left tide pool + rock ledge (screen x 0.15-0.36,
	# y 0.62-0.90); bottom-right coral bank (x 0.63-0.90, y 0.76-0.92); the
	# bottom-left purple/yellow tube-coral thicket (x 0.05-0.15, y 0.48-0.75);
	# the aqua meltwater puddle under the bales (x 0.80-0.90, y 0.44-0.52);
	# everything above the rail fence (y < 0.42) is raised orchard; the nine
	# tilled ovals are planting beds — the route threads the sand lane in front.
	"farmer": {
		"path": [[0.0795, 0.4833], [0.1752, 0.5028], [0.2901, 0.5361], [0.4528, 0.6111], [0.4738, 0.7014], [0.558, 0.7569], [0.6824, 0.7542], [0.8068, 0.7333], [0.9063, 0.7139], [0.9236, 0.6361]],
		"stations": [
			{"id": "barn_doors", "pos": [0.1542, 0.4556], "landmark": "sand apron below the red coral-shingled barn's white cross-braced double doors, fish weathervane on the ridge"},
			{"id": "pearl_clam", "pos": [0.1035, 0.75], "landmark": "giant pink scallop clam holding a glowing pearl on the rock rim of the bottom-left tide pool"},
			{"id": "blossom_arch", "pos": [0.4585, 0.4417], "landmark": "sand at the foot of the coral-flower arch where the rail-fenced orchard lane opens onto the yard"},
			{"id": "seed_beds", "pos": [0.7092, 0.6764], "landmark": "front-centre tilled oval of the 3x3 seedbed grid, rimmed with pebbles and little corals"},
			{"id": "hay_bales", "pos": [0.8929, 0.3889], "landmark": "stack of three giant round golden hay bales at the right edge, one red starfish on the front bale"},
		],
		"clue_spots": [[0.1398, 0.125], [0.0604, 0.5444], [0.1676, 0.8333], [0.3571, 0.3278], [0.625, 0.2611], [0.7877, 0.2333], [0.7637, 0.8028], [0.9714, 0.6528]],
	},
	# UNWALKABLE: no water anywhere — a dry pale-aqua tiled gym floor. Off-limits
	# are the three raised ring platforms (x 0.08-0.40 / y 0.57-0.77;
	# x 0.41-0.60 / y 0.61-0.73; x 0.79-0.94 / y 0.63-0.75), the pavilion stage
	# and its rope railing (x 0.55-0.80 / y 0.40-0.56), the rope-ring fence and
	# pearl-topped posts above y 0.56, the bottom-right coral/kelp thicket
	# (x > 0.83 below y 0.78), the bottom-left teal coral (x < 0.06 below
	# y 0.75), and the blurred strip below y 0.92.
	"boxer": {
		"path": [[0.0225, 0.694], [0.0799, 0.833], [0.2042, 0.882], [0.3189, 0.889], [0.4289, 0.854], [0.5245, 0.813], [0.6297, 0.833], [0.7397, 0.84], [0.8401, 0.771], [0.9453, 0.688]],
		"stations": [
			{"id": "glove_wall_shelf", "pos": [0.0273, 0.667], "landmark": "far-left pearl-crowned pink coral shelf holding three rows of red, purple and teal boxing gloves"},
			{"id": "purple_sparring_mat", "pos": [0.1755, 0.813], "landmark": "low round purple sparring mat with a cream scallop emblem on its orange coral-and-pearl ring base"},
			{"id": "teal_heavy_bag", "pos": [0.5102, 0.792], "landmark": "tall teal heavy bag with drum-laced cream top on the pink coral-and-pearl ring platform at frame centre"},
			{"id": "shell_pavilion_stage", "pos": [0.6488, 0.611], "landmark": "raised tiled stage before the purple scallop-dome pavilion with pearl-studded rim and teal curtains"},
			{"id": "red_heavy_bag", "pos": [0.8047, 0.781], "landmark": "tall coral-red heavy bag in a gold-trimmed purple cradle on the purple ring platform right of centre"},
		],
		"clue_spots": [[0.121, 0.194], [0.2233, 0.486], [0.3161, 0.275], [0.5503, 0.236], [0.7062, 0.403], [0.9596, 0.34], [0.8831, 0.833], [0.2137, 0.872]],
	},
	# UNWALKABLE: an undersea plaza with three curtained shell stages — NOT the
	# old top-hat/moon-pool town. Off-limits: the blue stepping-stone tide pool
	# (screen x 256-576, y 480-640); the left-edge coral-and-kelp bed (x < ~250
	# below y 430); the gold-filigree lavender coral bed across the right
	# foreground (right of the gold ribbon from ~x 760,y 528 to the edge); the
	# small gold-rimmed teal rock pools (notably x 930-1030, y 465-510); all
	# three daises and their steps; the soft-focus band below y ~660.
	"magician": {
		"path": [[0.145, 0.628], [0.204, 0.635], [0.281, 0.643], [0.357, 0.654], [0.434, 0.667], [0.51, 0.675], [0.577, 0.679], [0.644, 0.676], [0.703, 0.668], [0.746, 0.658]],
		"stations": [
			{"id": "violet_shell_stage", "pos": [0.154, 0.631], "landmark": "pale sand before the violet curtained shell stage, domed canopy topped by a pearl-set pink scallop"},
			{"id": "pearl_tide_pool", "pos": [0.324, 0.647], "landmark": "gold-rimmed edge of the blue stepping-stone tide pool with loose pearls, ringed by purple kelp"},
			{"id": "teal_shell_stage", "pos": [0.508, 0.653], "landmark": "sand before the centre teal curtained shell stage with gold-swagged curtains and pearl newel posts"},
			{"id": "pearl_lamp_avenue", "pos": [0.644, 0.676], "landmark": "foot of the tall gold lamppost with a glowing pearl globe in the kelp bed between the teal and rose stages"},
			{"id": "rose_shell_stage", "pos": [0.743, 0.658], "landmark": "sand at the foot of the rose curtained shell stage with pearl-collared pink columns (right-edge destination)"},
		],
		"clue_spots": [[0.037, 0.479], [0.083, 0.774], [0.219, 0.287], [0.242, 0.794], [0.508, 0.297], [0.633, 0.447], [0.827, 0.832], [0.94, 0.733]],
	},
	# UNWALKABLE: the foreground reef bank below y ~0.70 (table corals, purple
	# and red tube corals, orange blooms, kelp) — the promenade must not be left
	# toward the viewer; the rainbow paint rivers and the raised rock shelf they
	# run over (x 0.55-0.72, y 0.38-0.50); the three paint-pot pedestals; the
	# coral borders hugging both daises. Left of x ~0.03 and right of x ~0.96 is
	# blurred bleed.
	"painter": {
		"path": [[0.0464, 0.6278], [0.1181, 0.6556], [0.2185, 0.6667], [0.3237, 0.675], [0.4289, 0.6792], [0.5312, 0.6792], [0.6326, 0.6667], [0.7186, 0.6278], [0.754, 0.5167], [0.8888, 0.4889]],
		"stations": [
			{"id": "purple_paint_pot", "pos": [0.1631, 0.6417], "landmark": "giant purple paint pot with drip glaze and a pink starfish badge on its round pedestal, left of centre"},
			{"id": "gazebo_easel", "pos": [0.3744, 0.4583], "landmark": "foot of the stepped pink dais under the coral-domed gazebo sheltering a blank wooden easel"},
			{"id": "coral_paint_pot", "pos": [0.5083, 0.6417], "landmark": "giant coral paint pot with drip glaze and flower badge on its stone pedestal, dead centre of the sand plaza"},
			{"id": "rainbow_brush", "pos": [0.6709, 0.4069], "landmark": "stepped plum pedestal of the giant paintbrush whose rainbow bristles pour paint rivers across the seabed"},
			{"id": "arch_easel", "pos": [0.8888, 0.4889], "landmark": "cream dais under the pearl-crested scallop arch beside the tall easel and its palette, far right"},
		],
		"clue_spots": [[0.0588, 0.4069], [0.1095, 0.1319], [0.2912, 0.8056], [0.3744, 0.3167], [0.536, 0.2083], [0.5695, 0.4472], [0.7904, 0.8125], [0.9529, 0.4472]],
	},
	# UNWALKABLE: the sunken foreground reef below the stone-cobble rim (y >
	# ~0.70 at the frame edges, ~0.73 at centre) — purple boulders, tube
	# sponges, kelp, spiral shells, a stone cave arch, a drop below the plaza;
	# the mossy teal shelf behind the sand (y < ~0.44) holding the three domed
	# habitats, pipe-junction planters and the shell tower; the teal ledge with
	# blue bubble-stones right of the rocket dais (x > ~0.83, y 0.46-0.60). The
	# rocket dais is reachable only by the sand ramp at x ~0.78-0.83.
	"astronaut": {
		"path": [[0.0168, 0.5944], [0.0942, 0.6528], [0.1946, 0.675], [0.3094, 0.6667], [0.4624, 0.6792], [0.5771, 0.675], [0.6727, 0.6625], [0.7492, 0.6472], [0.8544, 0.5347], [0.8975, 0.4278]],
		"stations": [
			{"id": "coolant_tank_pad", "pos": [0.1707, 0.6778], "landmark": "long chrome cylinder tank clamped in studded purple flanges on the left round dais, teal flower hatch in front"},
			{"id": "pipe_arch_planter", "pos": [0.3237, 0.5486], "landmark": "tiered purple-stone planter of orange and yellow tube corals under the blue glass pipe arch"},
			{"id": "periscope_elbow", "pos": [0.4719, 0.6778], "landmark": "tall chrome elbow pipe with riveted purple collars on the centre round dais, pink flower hatch in front"},
			{"id": "airlock_ring", "pos": [0.7492, 0.6472], "landmark": "giant white airlock torus banded with four studded purple straps on the right dais, blue flower hatch"},
			{"id": "rocket_launch_dais", "pos": [0.8946, 0.425], "landmark": "foot of the blue steps to the cream rocket with red nose cone and fins on the raised oval launch dais"},
		],
		"clue_spots": [[0.0722, 0.8083], [0.1726, 0.2514], [0.2711, 0.1417], [0.4002, 0.8056], [0.4738, 0.375], [0.6087, 0.8028], [0.7645, 0.1639], [0.9357, 0.5]],
	},
	# UNWALKABLE: the whole aqua ribbon is WATER — a looping race canal with
	# ripple rings around three floating gate buoys, spanned by the start and
	# finish arches. Never place a walker on it and never cross it. The pale
	# stone kerb on its near bank is a wall ledge, not a walkway. The sand
	# paddock around the pearl-domed pavilion (y ~0.47-0.57) is an island and
	# is not reachable from the front beach. x < 0.13 and the extreme bottom
	# corners are packed coral and boulders. The only continuous ground is the
	# beach in front of the canal wall, x ~0.14 to the terrace at x 0.86.
	"racer": {
		"path": [[0.145, 0.701], [0.175, 0.728], [0.242, 0.75], [0.318, 0.758], [0.399, 0.761], [0.481, 0.758], [0.564, 0.767], [0.639, 0.803], [0.717, 0.81], [0.844, 0.761]],
		"stations": [
			{"id": "pearl_start_arch", "pos": [0.156, 0.711], "landmark": "giant cream scallop start arch rimmed with pearls spanning the race canal at the far left"},
			{"id": "teal_gem_buoy", "pos": [0.304, 0.757], "landmark": "beach before the first gate marker, a gold ring buoy on a lilac float crowned with a teal gemstone"},
			{"id": "pearl_dome_pavilion", "pos": [0.481, 0.758], "landmark": "beach below the purple pearl-domed rotunda on the infield, white columns and steps to the paddock sand"},
			{"id": "rose_gem_buoy", "pos": [0.671, 0.811], "landmark": "beach before the third gate marker's magenta gemstone, beside a ribbed urchin and a teal-coral mound"},
			{"id": "ribbon_finish_arch", "pos": [0.844, 0.761], "landmark": "scallop finish arch tied with a pink checkered ribbon banner over the purple rock terrace at the right"},
		],
		"clue_spots": [[0.159, 0.181], [0.176, 0.817], [0.285, 0.176], [0.432, 0.869], [0.534, 0.199], [0.498, 0.535], [0.733, 0.261], [0.883, 0.718]],
	},
	# UNWALKABLE: everything below the wavy lavender rim fronting the promenade
	# is deep-water foreground reef — never step below y ~0.70-0.73 (the rim
	# dips lowest, y ~0.735, around x 0.45-0.55). Above the promenade's back
	# edge (y < ~0.62) are raised ledges, coral beds and the three daises: the
	# shell-stage deck and steps (x 0.19-0.32), the gazebo platform and steps
	# (x 0.44-0.57), the record-floor dais and steps (x 0.655-0.82). The
	# promenade itself is unbroken from x ~0.105 to ~0.895 with no water
	# crossing; kelp fronds overhang at x ~0.865-0.90, so do not route past 0.86.
	"popstar": {
		"path": [[0.038, 0.648], [0.094, 0.658], [0.18, 0.667], [0.299, 0.662], [0.409, 0.672], [0.504, 0.68], [0.605, 0.678], [0.69, 0.672], [0.8, 0.666], [0.929, 0.656]],
		"stations": [
			{"id": "shell_stage", "pos": [0.182, 0.666], "landmark": "giant cream scallop concert stage with pearl swags, flanked by stacks of round teal-and-gold speaker cabinets"},
			{"id": "clam_coral_bed", "pos": [0.299, 0.66], "landmark": "violet fan clam with a gold clasp and an orange starfish on the lavender ledge left of the gazebo"},
			{"id": "mic_gazebo", "pos": [0.504, 0.68], "landmark": "centre bandstand gazebo with pearl-finialled pink dome, red coral columns and a gold vintage microphone"},
			{"id": "pink_clam_reef", "pos": [0.688, 0.672], "landmark": "large pink fan clam with a pearl in its hinge on the reef ledge between the gazebo and the dome"},
			{"id": "record_dais", "pos": [0.809, 0.664], "landmark": "round vinyl-record dance floor on the raised dais before the aqua glass dome with its gold treble clef"},
		],
		"clue_spots": [[0.035, 0.285], [0.192, 0.82], [0.262, 0.226], [0.319, 0.824], [0.504, 0.257], [0.635, 0.86], [0.833, 0.256], [0.962, 0.286]],
	},
```

```gdscript
	"farmer": [0.12, 0.86],
	"boxer": [0.12, 0.88],
	"magician": [0.14, 0.85],
	"painter": [0.10, 0.82],
	"astronaut": [0.10, 0.87],
	"racer": [0.18, 0.82],
	"popstar": [0.10, 0.82],
```

All seven derivations are marked **high confidence**. Two consequences to carry
forward:

- **racer's canal is water across the whole frame.** It is the only career where
  the route's own visual centre line is unwalkable. `_stage_feet_at_x()`
  (`opera_career_world_2d.gd:1551`) already snaps every brain-space position back
  onto the polyline, so no imp and no helper can enter it — but any *tap target*
  placed on the canal (the three buoys, the ripple rings) must be registered as a
  detail spot, never as a walk destination. §4 PATHFINDING, and §5 Y7.
- **magician's walkable sand is a narrow strip**, y ~438..478 px between the left
  stage base and the tide pool, widening only in the centre-right. Its ROAM
  narrows to `[0.14, 0.85]` for that reason. Do not spread five crew imps across
  it without checking the spawn spread at `opera_career_world_2d.gd:969-973`.

Still outstanding on this workstream and **not** in §3: the `nursery` `PATHS`
row (the only career with no derived geography at all — `clue_spots()` falls
through to the synthetic 8-point spread at `:224-230`), and a `WORKBENCH` point
per career to replace the hardcoded `prop_rect.position = Vector2(890, 330)`
(`opera_career_world_2d.gd:414`).

---

## 4. THE CONDITIONS

Two contracts. They are not style guidance; they are the reason the game is
legible to a four-year-old, and the reason a walking figure cannot end up
standing in a canal.

### 4.1 SCALE — Roshan is a bit taller than the imps and **never more than 1.5×**

Owner rule, 2026-08-03. Shipped today, in code:

| Figure | Box | Site | Ratio to Roshan |
|---|---:|---|---:|
| **Roshan** | 250 × 250 | `opera_career_world_2d.gd:392` | — |
| crew imp | 180 × 180 | `:988` | **1.39×** |
| imp captain | 200 × 200 | `:988` | **1.25×** |
| career rival | 190 × 190 | `:399` | **1.32×** |

**Every new figure inherits it.** Applied to each new object class:

| New object class | Ledger rows / engine slot | Scale ruling |
|---|---|---|
| **Helper stage cards** `helper_<career>.png` ×12 NEW + `faron_nursery.png` REUSE | exploration ledger rows `helper_chef` … `helper_nursery` (family D-helpers, 26 rows total) → new `helper_actor` slot, ~12 lines mirroring `_actor()` (`:508`) + `_place_on_stage()` (`:521`) | **190 × 190**, the rival's number → 1.32×. Author the figure to the same body proportion as `rival_<career>.png` so the ratio holds with no per-file tuning. Gate G7 already states this; it is now binding, not advisory. |
| **Helper pointing poses** `helper_<career>_point.png` ×13 | same family, P3 | Same 190 box and the **same baseline as the D1 card of the same character** — a point pose that raises the figure inside the cell silently changes the ratio when the engine swaps textures mid-act. |
| **Peekaboo imp** `imp_mischief_peek.png`, `imp_mischief_wave.png` | ledger rows `imp_mischief_peek`, `imp_mischief_wave` (family F) → `_spawn_stage_imp()` (`:979`) with **no `ImpAI`** | It is an imp: **180 × 180**, the crew number, **never 200**. The captain box is reserved for the captain. The flat bottom crop must sit at the cell's lower third so the visible head-and-shoulder still reads at a 180 box. |
| **Roshan sheets a / b / c** ×26 (+13) | animation handoff; `player_actor` at `:392` | The box does not change — 250 × 250. **The binding requirement is inside the cell:** the figure must occupy the same proportion of its 512 cell as the accepted `roshan_<career>.png` costume portrait does, with feet-or-tail contact on a common baseline (row 500 ± 2 px). A sheet whose figure is drawn 8% larger than the portrait silently pushes her to 1.5× the crew the moment the walk cycle starts, and no runtime number would show it. This is the single most likely way for the scale contract to break. |
| **`explore_ambient_shoal`** (5 reef fish) | exploration ledger row `explore_ambient_shoal` (family C) | Not a figure — **exempt, and must stay exempt.** The shoal draws in the discovery layer above the backdrop and below the actors, at an authored size unrelated to the actor boxes. It must never gain feet, a ground contact, or a route position (§5 Y9). |
| **Audience portraits** ×6 | now finale-only (integration half) | Exempt: they are portraits in the upper frame band, not stage actors. They must not gain feet. |
| **Widget creature subjects** — piggies (farmer HERD), plushy starfish patients (doctor CAST / BANDAGE), babies (nursery FEED / BEDTIME / catch), the lamb (magician VANISH) | widget ledger, `template ∈ {push, target, trace, pour, catch}` | **Exempt** — they live inside the task card, at card scale, in TASK state, and never touch the stage's ground plane. Widget lock G11 already forbids baked Roshan and baked imps, so there is no scale exposure. Say this out loud so nobody "fixes" a piggy to 180 px. **One watch item:** the `widget_*_state_*` strips (N × 256). If the future ingredient-surface mode ever lifts a state cell onto the stage, that cell inherits both contracts on the spot. |

**Nothing** in the three open packages may introduce a walking figure taller than
166 px of Roshan's 250 (1.5×) or shorter than ~140 px (below which she stops
reading as "a bit taller" and starts reading as a giant). The band is
**166 ≥ figure ≥ 140**; 180 and 190 sit comfortably inside it.

### 4.2 PATHFINDING — every walking figure is confined to `roam_range()`

`OperaStagePaths.roam_range()` (`opera_stage_paths.gd:178`) returns the
`[t_min, t_max]` span of the derived route that is actually standing room. Its
own docstring states the asymmetry and it is binding: **crew imps roam inside the
envelope; Roshan alone walks the full route**, because the route's extreme ends
are the painted entry arch and the destination dais — scenery she is *meant* to
arrive at, and scenery nobody else may stand on.

The clamp is `_stage_feet_at_x()` (`opera_career_world_2d.gd:1551`), which snaps
any brain-space x back onto the polyline. Off entry arches, off destination
daises, off water inlets, off foreground ledges — by construction, not by
per-career tuning.

| New object class | Ledger rows / engine slot | Pathfinding ruling |
|---|---|---|
| **Helper** `helper_<career>.png` | family D → `helper_actor`, H1 follow at 0.8× speed, 140 px trailing offset | **Confined to `roam_range()`, not to the route.** When Roshan walks past `roam.y` to her destination dais, the helper **stops at `roam.y`** and waits. Concretely: racer `roam.y = 0.82` while `ribbon_finish_arch` sits at t ≈ 0.97 — Harper and Fiona stop on the beach and do not climb the terrace. This is correct behaviour, not a bug, and it must be written into H1 or the first playtest will report it as one. |
| **Peekaboo imp** | family F → `_spawn_stage_imp()` without a brain | Spawns only at a `station_list` entry whose `pos.x` maps inside the career's `roam_range()` span, and renders **occluded** at that landmark rather than standing on the route. Excluded by this rule today: boxer `glove_wall_shelf` (u 0.0273 → t below `roam.x`), racer `pearl_start_arch` and `ribbon_finish_arch` (start/finish arches span water and terrace), astronaut `rocket_launch_dais` (raised platform), magician `rose_shell_stage` (destination dais). Every career retains at least three legal hiding places. |
| **Roshan, walk integrator W1** | design §1 W1 → `move_toward` in `_process`, destination `_stage_feet_at_x(tap.x)` | Full route, both ends, clamped ±40 px inside the first and last waypoint by `_stage_feet_at_x` (`:1556-1558`). She is the **only** figure exempt from `roam_range()`. `sheet_a` row 0 WALK drives the body; the animation never owns position. |
| **`explore_here_ring`** (walk destination mark) | family A, P1 | Drawn at the destination `_stage_feet_at_x()` already returned — on-route by construction. It can never mark unwalkable ground because it never sees an unclamped point. |
| **`explore_breadcrumb`** (pull-back ladder, 11 s rung) | family A, P2 | Repeated along `point_along()` between `nearest_t(points, _hero_feet())` and the station's `t`. On-route by construction. |
| **`explore_rest_cushion`** (Q1 sit, H4 sit-with-me) | family C, P2 | Fades in **under her** and under the helper — inherits their clamped positions. No independent placement. |
| **`explore_favour_pouch`** (C1 favours) | family B, P1 | Orbits her body; no ground contact. **But the pickup rule needs a placement gate:** C1 requires the favour be taken "by standing under it", so a favour may only be attached to a clue spot whose transformed x lies inside `roam_range()` **and** whose distance to the nearest route point is ≤ 220 px. Worked example — farmer clue spot `[0.1398, 0.125]` maps to screen (263, 90); the route at x = 263 sits at y ≈ 353; distance 263 px > 220. **That spot cannot carry a favour.** It stays a far-touch sparkle, or the favour goes to H3 (the helper fetches it). Run this filter over all 104 clue spots when building the `DETAILS` table. |
| **`explore_sprout`** (farmer's nine beds, ballerina bloom, painter splat) | family E, P2 | Anchored to painted objects that are **explicitly unwalkable** — farmer's own derivation says "the nine tilled soil ovals are planting beds, not walking surface; the route threads the sand lane in front of them." Registered as **detail spots (hit-test step 4)**, never walk destinations. Touching a bed fires the response where she stands; it does not route her into the soil. |
| **`explore_curtain_open`** (magician booths, barn doors, lockboxes, cottage doors, dressing alcove) | family E, P2 | Same rule: static touch target on unwalkable scenery, hit-test step 4 only. The design's step 6 fallback (`walk to _stage_feet_at_x(tap.x)`) is the safety net — even a mis-tap on a booth interior clamps her back to the sand. |
| **`explore_prop_mat`** + the `WORKBENCH` row | family G, P2 + 13 data rows replacing `prop_rect.position = Vector2(890, 330)` (`:414`) | X3 asks her to **walk to the prop and touch it**, so unlike the two rows above, **the workbench point must lie inside `roam_range()`**. It is the one new placement that is walk-bearing. Derive it as a station-adjacent standing spot, not as the prop's own centre. |
| **`explore_ambient_shoal`** | family C, P2 | Not a walker and **must not be tappable at all** — a tappable shoal becomes a chase, and a chase is a fast beat wearing a slow beat's clothes. §5 Y9 rewards standing still instead. |
| **Widget layers** (all 221 rows) | TASK state, inside the card | **Exempt.** The card's gesture surface STOPs input, the walk integrator is off in TASK, and no widget layer has a stage position. The only crossing requirement is the state split itself: `_open_task()` must disable `wander_layer` before the card draws, or a tap that misses the surface will walk her while she is cooking. |

**The one-line test for anything new:** *does it stand on the ground plane?* If
yes, it inherits `roam_range()` and one of the four boxes. If no, it is exempt
from both — but if it **asks her to walk somewhere**, the destination it asks for
inherits `roam_range()` even though the object itself does not.

---

## 5. ADDITIONAL EXPLORATION TASKS

The owner's direction, verbatim: *"using the same assets, but applying them in a
slower, more contemplative way."* The exploration design's 22 tasks (W1–3,
T1–4, C1–4, Q1–4, H1–5, X1–3) cover free walk, touch-the-world, collecting,
quiet beats and helpers. These ten go further, and **all ten need zero new art
files** — they consume only what is painted, what already ships, and the
exploration package's own P1/P2 shared effects.

Numbered `Y1`–`Y10` so they do not collide with anything.

Every one of them is checked against four disqualifiers before it appears here:
**no fail state, no reading, no second finger, no timed precision.**

### Y1 — FOLLOW THE TRAIL THAT IS ALREADY PAINTED
- **She does:** taps the first glowing paw print on detective's mid walkway. It
  brightens and stays lit; the next print along the trail begins to breathe. She
  works along ~14 prints at whatever pace she likes. When the last one lights,
  the whole trail pulses once head-to-tail and the shaking box at the end of it
  wiggles.
- **Art:** **none.** Census §2: detective has a glowing paw-print trail (purple →
  teal → pink, ~14 prints) running the full width of the mid walkway; magician
  has glowing star tiles scattered on the sand and a winding gold-edged path;
  painter has three rainbow paint rivers pouring from the giant brush. All three
  are painted *sequences* that nothing currently uses. Response is the T1 patch
  `light` motion plus `explore_glow_warm` / `explore_glow_cool` (exploration P1).
- **Data:** one new `TRAILS` table — career → ordered array of `[x, y]`. Three
  careers, ~30 points total, read off the tiles.
- **Serves:** detective, magician, painter.
- **Why contemplative:** it is the only mechanic in the set with an **order that
  is not a goal**. Taps out of sequence light anyway — order only decides which
  print breathes next — so there is no wrong answer, no timer and nothing to
  lose. The reward is watching a painting slowly turn itself on.
- **Ruled safe:** one finger, no reading (the trail *is* the instruction), no
  fail state (every tap lights something), never counted.

### Y2 — THE LAMPLIGHTER'S ROUND
- **She does:** nothing. She walks, and every lamp she passes within 220 px
  lights **by itself**. By the end of a wander window the promenade behind her is
  lit and the promenade ahead is not.
- **Art:** **none.** `explore_glow_warm` for chef's two hanging lanterns,
  ballerina's lamp-post globes, popstar's gold lamp posts and racer's terrace;
  `explore_glow_cool` for detective's city windows, magician's six pearl lamp
  posts and astronaut's habitat domes. Both are exploration P1 files already
  requested.
- **Data:** a `lamp: true` flag on the relevant `DETAILS` rows. No new table.
- **Serves:** magician (6 posts), popstar, ballerina, detective, chef, racer,
  astronaut — 7 careers.
- **Why contemplative:** it is the only feedback in the game that rewards
  **travel** instead of touch. A child who walks slowly sees more of it than a
  child who taps fast, and that is the whole lesson stated without a word. It
  also turns W2's abstract "progress you read by looking at the world" into
  something she can see she caused with her feet.
- **Ruled safe:** zero input required, so it cannot be got wrong; no counter, and
  an unlit lamp is never marked as missed.

### Y3 — NINE BEDS, AND THEY GROW WHILE SHE IS AWAY
- **She does:** taps one of farmer's nine empty planting beds. A seedling appears
  — stage 1 of `explore_sprout`. It does **not** grow while she watches. Every
  later act she plays, each planted bed advances one stage: seedling → bud →
  bloom.
- **Art:** `explore_sprout` (exploration P2, 768 × 256, three cells, already
  requested for exactly this). Nothing new. The same three-stage rule re-skins to
  painter's three blank easels (a shipped `goal_<career>.png` drops into a frame,
  one per visit) and magician's three curtained booths (`explore_curtain_open`,
  one per visit).
- **Data:** `m.opera_pantry["farmer_bed_%d"] = stage` — the dictionary already
  exists (`main.gd:295`), already saves (`save_state.gd:132/207/465`) and is
  already asserted to round-trip by `probe_load.gd:6`. No save-schema change, no
  removed keys.
- **Serves:** farmer (9 beds), painter (3 easels), magician (3 booths). Census
  §2: "Nine beds = nine touches = a complete, countable act" and "three blank
  easels… the best 'your touch made a thing' beat in the set."
- **Why contemplative:** it is the only thing in the game she cannot rush. It is
  *literally* slower than a session. Coming back tomorrow and finding the garden
  further along than she left it is the strongest argument the game can make for
  stopping.
- **Ruled safe:** nothing wilts, nothing dies, nothing reverts, no bed is wrong,
  and the count is never shown as X of 9. **Owner decision required** — this is
  the first world state that changes between sessions (§7 Q5).

### Y4 — PASS IT DOWN THE LINE
- **She does:** touches one of candymaker's seven faced candies riding the
  overhead rail. It boops — squash, blink — and then passes the boop to its
  neighbour 0.18 s later, and that one to the next, left to right. Touching the
  leftmost gives the longest wave.
- **Art:** **none.** Census §2 calls the seven faced candies "the single best
  untapped asset in the whole set" — they are already painted smiling, at
  y ≈ 0.26, x 0.55–0.93. Response is T1 `bulge` chained.
- **Data:** a `chain: [ids…]` field on the `DETAILS` rows that form a row.
- **Serves:** candymaker (7 faces), doctor (5 heart medallions over 5 exam
  booths), ballerina (5 wave-embroidered practice tuffets in a row), astronaut
  (3 flower hatches, 3 star windows), popstar (4 speaker cones), racer (3 gate
  buoys, using §3's re-derived positions).
- **Why contemplative:** the wave takes ~1.3 s to cross and she cannot speed it
  up. It teaches "touch once, then watch" — the same anti-mashing lesson the
  reserved green go-zone teaches in the widget layer, taught here for free with
  no timing window and nothing to fail.
- **Ruled safe:** any candy is a valid start, mid-wave taps just start a second
  wave, nothing is scored.

### Y5 — THE WORLD BREATHES WHEN SHE DOES NOT
- **She does:** nothing, for four seconds. The ambience gains one layer. Four
  more, a second. Four more, a third — a single career melody note every ~2.5 s.
  Any touch drops it back to the base loop, gently.
- **Art:** **none.** **Audio: none new** — the layers are built from
  `_set_ambience` plus the `_fanfare()` pitch-scaled chime trick already shipped
  at `audio_director.gd:127-142`, which makes a 5-note career melody out of one
  chime player.
- **Data:** none.
- **Serves:** all 13.
- **Why contemplative:** it is a reward that exists **only** in silence, only for
  the child who stopped. It cannot be scored, shown or failed, and it is the only
  proposal here that works on a muted tablet's *opposite* — it is the reason to
  turn the sound on.
- **Ruled safe:** no input, no state, no persistence. Delete-able in one line if
  it proves annoying.

### Y6 — THE ROLL CALL
- **She does:** stands within 220 px of one of the painted things that already
  has a face and touches it. It greets her, and then **stays awake** — a slow
  blink every ~6 s for the rest of the act, wherever she goes.
- **Art:** **none.** Painted faces already in the set: doctor's smiling starfish
  patient (≈ 0.05, 0.50), detective's fish inside a bubble cloud (C7 at 0.605,
  0.71), candymaker's seven candy characters, farmer's fish weathervane, the
  nursery babies, and the two shipped creature props `goal_magician.png` (the
  lamb) and `goal_doctor.png` (the starfish) at their workbenches.
- **Data:** an `awake: bool` beside `touched` in the X1 discovery state.
- **Serves:** doctor, detective, candymaker, farmer, magician, nursery — 6
  careers directly, and every career indirectly through X3's workbench prop.
- **Why contemplative:** the world gets **less empty the longer she stays in
  it**, and nothing hurries her toward that. It also answers the census's
  sharpest complaint — *"a farm with nothing alive in it is the weakest world in
  the set"* — without a single new sprite, because the fish weathervane and the
  clam were always alive; they were just never asked.
- **Ruled safe:** no fail (a face she never greets simply stays asleep, unmarked),
  no reading, one finger, near-touch only so it teaches walking.

### Y7 — DROP A PEARL IN THE WATER
- **She does:** stands on the rim of water she cannot enter and touches it. One
  ripple ring travels out across the surface. A second touch inside the first
  makes them cross.
- **Art:** **none** — `explore_touch_ring` (exploration P1) tinted per career.
- **Data:** one `water: true` clue spot per career that has water.
- **Serves:** racer (the whole aqua canal — §3), farmer (bottom-left teal tide
  pool), magician (blue stepping-stone tide pool), doctor (waterfall spill and
  shell fountain), chef (the water inlet under the footbridge), astronaut (blue
  bubble-stone ledge).
- **Why contemplative:** it is the one place a touch produces something that
  **keeps moving after she stops touching it**, and the only use of the water
  that does not require walking into it. It also does the pathfinding teaching
  for free: the rim is the best seat, so she learns the water is not floor
  without ever being stopped at its edge.
- **Ruled safe:** registered as a **detail spot, hit-test step 4** — it fires the
  ripple and does **not** route a walk (§4.2). Even a stray tap that falls
  through to step 6 clamps her back onto the route via `_stage_feet_at_x()`, so
  she cannot end up in racer's canal.

### Y8 — THE ONE THAT WAS ALWAYS SHUT
- **She does:** touches the one openable thing in the career. It opens over
  **2.2 s** — an ease, never a snap. Behind it sits that career's own
  `goal_<career>.png` at 40%. Touching it again closes it, also over 2.2 s. It
  gives nothing, counts nothing, and can be opened and closed forever.
- **Art:** **none** — `explore_curtain_open` (exploration P2, tintable white with
  a transparent centre, already requested) plus the 13 shipped goal props.
- **Data:** one `openable` clue spot per career.
- **Serves:** magician (3 booths), farmer (barn doors), detective (evidence
  lockboxes and the treasure chest), candymaker (three cottage doors), ballerina
  (dressing alcove), chef (the domed cake) — the handoff's own six, extendable to
  all 13 by tint.
- **Why contemplative:** it is the **only reversible, rewardless interaction in
  the game**. Everything else accumulates. A four-year-old will open and close a
  cupboard forty times, and this is that cupboard — for zero files, because the
  census's finding was that every openable object in the set is painted in
  exactly one state, and this package already commissioned the second state once.
- **Ruled safe:** no state is gained or lost in either direction, so there is
  nothing to fail; unwalkable-scenery target, hit-test step 4 only.

### Y9 — THE SHOAL ONLY STOPS FOR SOMEONE STANDING STILL
- **She does:** nothing. The five-fish shoal crosses the frame once every ~22 s
  regardless. If she is **standing still** when it reaches her x, it slows and
  loops around her for 3 s before moving on. If she is walking, it passes
  straight by.
- **Art:** **none** — `explore_ambient_shoal` (exploration P2, five pastel reef
  fish, already requested as the set's only crossing creature).
- **Data:** her velocity, which the W1 integrator already has.
- **Serves:** all 13 — every career painting is underwater now, which is the
  reason one shoal covers the set.
- **Why contemplative:** it is the clearest possible statement that **stopping is
  a thing you can do**. A child discovers it by accident exactly once and then
  pursues it forever, and the only way to pursue it is to stand still.
- **Ruled safe:** **the shoal is not tappable** (§4.2) — a tappable shoal is a
  chase, and a chase is a fast beat in slow clothing. Missing it costs nothing
  and is never noted.

### Y10 — WHAT SHE SEES FROM HERE
- **She does:** stands at any station for 2.5 s. She turns to face its landmark,
  and the **landmark itself** takes a slow 0.9 s bloom — a light, not a sparkle
  — and she says its name, the first clause of the `landmark` string.
- **Art:** **none** — `explore_glow_warm` / `explore_glow_cool` (exploration P1).
- **Data:** a second `object_pos` per station — **exactly what census §5 step 4
  asked for**: 65 rows (13 × 5). Today the pulsing station marker breathes over
  bare pavement 60–120 px below the thing it means, because `pos` is a standing
  spot and nothing points at the object.
- **Serves:** all 13, all 65 stations, and every `landmark` string already
  written in `opera_stage_paths.gd` and in §3 above becomes readable content.
- **Why contemplative:** it gives the standing spot a reason to exist that is not
  "the card opens here". It is the only beat in the whole design that rewards
  standing exactly where the game already wanted her to stand — and it lands
  *before* the task, so arriving is its own small event rather than a trigger.
- **Ruled safe:** it fires on dwell, and the task's own 0.35 s open dwell is
  shorter, so it never blocks the card. Any touch cancels it.

### What was considered and rejected

| Idea | Why not |
|---|---|
| Drag a favour from the painting into a basket | Drag from a moving target, and the basket is a counter. Both banned. |
| Memory / matching pairs on the candymaker's seven faces | Has a wrong answer, therefore a fail state, however softly dressed. |
| Fishing at racer's canal or farmer's tide pool | Every fishing verb needs a miss to be worth anything. |
| Hide-and-seek with the peekaboo imp on a timer | X2 already gives the imp; a timer converts it into a fast beat. |
| A maze through magician's plaza | The whole design's safety argument is one dimension of freedom (`_stage_feet_at_x`). A maze needs two, and then she can be lost. |
| Painting the three easels with a colour picker | Two-step selection, reading-adjacent, and it introduces a "wrong" colour. Y3 drops a shipped `goal_<career>.png` in instead. |
| Any "collect all N" framing on Y1/Y3/Y4 | The no-fail contract's hardest line: nothing is ever counted at her. |

---

## 6. THE BUILD ORDER

One merged sequence over all four workstreams. **316 art files outstanding**,
plus engine and data work that ships no files at all. `‖` marks work that runs in
parallel from the start; `→` marks a hard dependency.

| # | Work | Lane | Files | Blocking |
|---:|---|---|---:|---|
| **0** | **P0 transform** — `_to_screen()` helper in `OperaStagePaths`, three call sites (§2) | engine | 0 | **Blocks 1, 2, 10, 11, 16.** Four lines; nothing else positional is true until it lands. |
| **1** | Land the 7 re-derived `PATHS` + `ROAM` rows (§3) | data | 0 | → 0. Blocks 2, 10, 12(part), 16. |
| **2** | **Render check** — farmer, racer, magician at 1280 × 720 with station markers drawn; confirm `hay_bales` lands on the bales and `ribbon_finish_arch` under the arch | QA | 0 | → 1. **Blocks everything downstream.** This is the one check that catches a coordinate-space inversion before 316 files are placed against it. |
| **3** | **Widget P1** (8 files: `widget_pour_chef` + `_mover` + `_fill`, `widget_crank_chef` + `_mover` + `_progress`, `widget_trace_chef` + `_lit`) → **stop, get owner sign-off** | art-W | **8** | ‖ from t=0. Proves all three animation grammars (G1–G3 bottom-up, G5 cross-fade, G6 chronological wipe). If one is wrong, that rule is wrong for a third of the set. |
| **4** | **Exploration P1** (6 shared files) | art-E | **6** | ‖ from t=0. Nothing in family A depends on anything. Highest coverage-per-file in the programme: 6 files light 104 painted details across 13 careers. |
| **5** | **`roshan_chef_sheet_a`** (1 file) → style proof, owner sign-off | art-R | **1** | ‖ from t=0. |
| **6** | `ActorMotion` three-node stack + per-actor rest-transform ownership | engine | 0 | ‖. Half-delivered already by the animation pass's B1 (`d0a35d3e`); finish it. Also fixes the live `_bounce_actor` stale-`home_y` bug. Blocks T3, Q1, H4 and Y1–Y10. |
| **7** | **W1 walk integrator + `wander_layer`** with the 6-step hit-test order | engine | 0 | → 0, 6. **Blocks every T / C / Q / H / X / Y task.** ~140 lines. |
| **8** | Split `_show_phase()` → `_arm_phase()` / `_open_task()`; 150 px / 0.35 s dwell; delete the blank `phase_gap`; add the probe auto-open guard so `probe_opera_2d_balance.gd`'s 287 assertions hold unedited | engine | 0 | → 7. |
| **9** | **Widget P2** (27 rows — pour ×3, basin ×2, shared shine, crank ×8, charge ×5, trace ×5, push ×4, shared arrows) | art-W | **27** | → 3 sign-off. ‖ with everything in the engine lane. |
| **10** | Data tables: `DETAILS` 104 rows, `WORKBENCH` 13, `PATHS["nursery"]` 1, `OBJECT_POS` 65 (Y10), `HELPER` 13, `FAVOUR` 13, `TRAILS` 3 (Y1). Run the 220 px favour-placement filter over all 104 clue spots (§4.2) | data | 0 | → 1, 2. Blocks 11, 12(part), 16. |
| **11** | T1 tile-quadrant patch sampler (seam-clipping helper, ~60 lines) → T2 → T3; then C1/C2 favours on `opera_pantry` + the orbiting-sparkle draw | engine | 0 | → 7, 10. |
| **12** | **Exploration P2** (14 new files: quiet-beat props ×4, dwell arc, breadcrumb, favour glint, prop mat, sprout, curtain-open, peek imp, **4 Path-B helper cards** — Sparkle, Mewsha, Rosalina, Lamba) | art-E | **14** | `explore_sprout` + `explore_curtain_open` promotion → 1. The other 12 are unblocked. The 4 Path-B cards are the only rows in the exploration package that block whole careers. |
| **13** | `helper_actor` engine slot (~12 lines, hides when the file is missing) + H1/H2/H3 | engine | 0 | → 7. Art-independent: a promoted card with no slot is inert, and a slot with no card is hidden. |
| **14** | **Animation sheets a + b**, remaining 25 | art-R | **25** | → 5 sign-off. ‖ with the whole engine lane. |
| **15** | Q1–Q4, X1–X3 | engine | 0 | → 7, 11. |
| **16** | **Y1–Y10** (§5) — `TRAILS`, lamp flag, nine beds on `opera_pantry`, chain wave, ambience layers, roll call, water ripples, open/close, shoal-stops-for-stillness, station long-look | engine + data | **0** | → 7, 10, 11, and 12 for `sprout`/`curtain_open`. **Zero art files.** |
| **17** | **Widget P3 + P4** (186 rows — target ×8 sets, gauge ×3, track ×8, lanes ×10, catch, and the long tail) | art-W | **186** | → 3, 9. |
| **18** | **Exploration P3** (36 files — 8 Path-A helper restages, 13 point poses, 13 favour tokens, ambient bubbles, imp wave) | art-E | **36** | Every row is an upgrade to something that already works. |
| **19** | Retune non-combat goals −20–25% and crew counts (5→3 opening, 8→6 chase); re-run `probe_opera_2d`, `probe_opera_nursery`, `probe_opera_2d_balance`, `probe_load`, `probe_passive`; report the new sim band | QA | 0 | → 8, 11, 15, 16. Expect the balance probe's measured time to **drop** to ~85–100 s (it pumps gestures and never wanders) — still inside `BAND_LO 70` / `BAND_HI 150`. **Say this in the commit or it reads as a regression.** |
| **20** | **`roshan_<career>_sheet_c`** ×13 | art-R | **13** | Last, and **owner-gated** (§7 Q2). T3, Q1, H4 and the whole Y-series play without it. |
| **21** | Close out the animation pass: owner identity/topology/style review against `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/` + a real Android Speedy-tier frame capture | QA | 0 | ‖ from t=0 — needs only a device. It is the **oldest** open item in the programme. |

**File arithmetic:** 8 + 6 + 1 + 27 + 14 + 25 + 186 + 36 + 13 = **316**.

**Three lanes run in parallel from t=0 and never block each other:** art-W lives
inside the task card in TASK state; art-E lives on the painting in WANDER; art-R
is the player actor in every state. Their one shared constraint is the **green
lock** — reserved success green (≈ RGB 117,240,158) exists only in T1/T2 go-zones,
and an exploration or animation asset carrying it silently breaks the
anti-mashing signal across all 60 widget phases.

**The critical path is short and cheap:** items 0, 1, 2, 7, 8, 10, 11 ship no art
at all and unlock everything else. **Item 2 is the single highest-leverage hour
in the programme.**

---

## 7. OPEN QUESTIONS FOR THE OWNER

1. **The second-order coordinate tune.** Ship `0.091 + 0.817` now (verdict B,
   RMS 26.3 px), or ship the empirical least-squares fit `0.081 + 0.861` in the
   same commit? B is decisively right versus identity; the fit is measurably
   better than B at the far-right stations of both careers, where B still drifts
   40–65 px left. Recommendation: **B now**, re-measure after the item-2 render
   check, tune in a separate one-line commit if the drift is visible on a tablet.

2. **`sheet_c` — 13 files, ~20 MB, at the end of a 316-file queue.** T3, Q1, H4
   and all ten Y tasks ship without it on `ActorMotion` transforms plus
   `explore_rest_cushion`. It is the difference between "readable but stiff" and
   "she looks like she is looking at things." Commission it, or close the request?

3. **The four Path-B helper cards** (Sparkle, Mewsha, Rosalina, Lamba — no art
   exists anywhere in the repo). Without them, candymaker, astronaut, ballerina
   and magician ship with **no walking friend**: the act plays, the VO plays, H2's
   show-me falls back to the marker ladder. Generate at P2 as the ledger asks, or
   accept four helper-less careers for this edition?

4. **Act length.** The exploration design lands chef at **≈ 2:04**, up from
   today's ≈ 1:49, with self-paced time going from ~4% to **45%**. The levers to
   come back down are chase 16→13 s, arrival 12→10 s, curtain call 11→9 s →
   **≈ 1:56**. Do not cut the wander windows. Which do you want on the phone?

5. **World state that changes between sessions (Y3).** Farmer's nine beds advance
   one growth stage per *later act played*, persisted in `opera_pantry`. It is the
   strongest contemplative beat in §5 and the only one that makes coming back
   tomorrow visibly worth it — and it is the first thing in this game that changes
   while she is not playing. Yes or no?

6. **APK budget.** 316 files: 221 widget layers (mostly 1024 × 576), 56
   exploration files, 39 Roshan sheets at 2048² (~58 MB for the sheets alone
   before `sheet_c`). The boot audit already flags a 30–40 s tablet boot. Do you
   want a size cap and a staged shipping order (P1 art on the stable channel,
   P3 tail on `android-dev` only), or ship everything as it lands?

7. **The pending review from the last pass.** Owner identity/topology/style review
   against the five masters in `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/` and
   a real Android Speedy-tier frame capture (`adb devices -l` found no device on
   the build host) are the **only** things standing between the delivered runtime
   animation pass and art acceptance. Can a phone be attached, or should the
   capture move to the family tablet?

---

## FILES REFERENCED (absolute)

Repo root: `C:/Users/Peter/Documents/mermaid-roshan-reef/`

**This programme's four specs**
- `.../CODEX_OPERA_WIDGET_ART_FULL_AMBITION_2026-08-03.md` + `.../assets_src/concepts/OPERA_WIDGET_ASSET_LEDGER_2026-08-03.csv` (221 rows)
- `.../CODEX_OPERA_ROSHAN_ANIMATION_HANDOFF_2026-08-03.md` (26 sheets + proposed `sheet_c` ×13)
- `.../CODEX_OPERA_EXPLORATION_HANDOFF_2026-08-03.md` + `.../assets_src/concepts/OPERA_EXPLORATION_ASSET_LEDGER_2026-08-03.csv` (57 rows)
- `.../CODEX_OPERA_ANIMATION_HANDOFF_2026-08-03.md` §14 — the delivered runtime pass

**Design and evidence**
- `.../OPERA_EXPLORATION_DESIGN_2026-08-03.md` — W/T/C/Q/H/X, the 22 tasks §5 extends
- `.../OPERA_WORLD_OBJECT_CENSUS_2026-08-03.md` — what is actually painted; §0(c) and §5(a) superseded by §2 here
- `.../FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/README.md` + `review_masters/` (5 masters) + `manifest.json`
- `.../CHAPTER2_PARTY_ROLES_2026-08-03.md` §2 — the helper cast and the 13 already-written wish lines

**Code this document binds to**
- `.../scripts/opera_stage_paths.gd` (279 lines) — `PATHS:20`, `ROAM:161`, `roam_range:178`, `path_points:190`, `stations:198`, `clue_spots:220`, `point_along:245`, `nearest_t:261`
- `.../scripts/opera_career_world_2d.gd` (**2046 lines** — every line number in the exploration design is against the older 1755-line file) — `player_actor.size:392`, `rival_actor.size:399`, `prop_rect.position:414`, `_glide_roshan_to:741`, `imp roam spread:969-973`, `imp size:988`, `_bop_burst_at:1321`, `celebrate:1458`, `_hero_feet:1543`, `_stage_feet_at_x:1551`, lens catch 96 px `:1934`, dwell 0.45 s `:1942`, reveal 118 px `:1959`
- `.../scripts/opera_world_backdrop_2d.gd` — `_load_tile_set:50`, `_draw_tile_set:66-75` (the y 448..1600 crop), `_draw:93`, the unreachable `painting` fallback `:103-111`
- `.../scripts/opera_gesture_surface.gd` — `_ink_bounds:426`, `_cover_rect:454`, `_draw_progress_overlay:463`
- `.../scripts/audio_director.gd` — `_say:13-38`, `_speaker_key:95-113` (all 13 helper names verified routed), `_fanfare:127-142`
- `.../scripts/main.gd:295` (`opera_pantry`), `.../scripts/save_state.gd:132/207/465`, `.../scripts/probe_load.gd:6`, `.../scripts/opera_act.gd:1558/3219` (the shipped carrot-cake precedent)

**Integration state**
- `dev` at `5f5d386c` — the integration half merged, probes green (run 30927887299)
- `6325c981` — review kit; `d0a35d3e` — runtime animation implementation
- Work branch: `claude/opera-integration-20260804`

---

## 8. THE REVIEW KIT — three corrections to the evidence protocol

Added 2026-08-04 after inspecting `FABLE_OPERA_ANIMATION_REVIEW_KIT_2026-08-03/`
against the gates it claims to serve. The kit is genuine evidence and the
animation pass it documents is good; these are defects in the *protocol*, and
they matter because the next capture round will otherwise repeat them.

**8.1 The family master cannot carry its stated gate.** Each capture cell is
200x120 native for a full 1280x720 frame — a 6.4x downscale. The kit's README
directs the reviewer to use it for "foot registration"; the handoff's visual
gate is *feet remain locked within 3 runtime pixels*. Three runtime pixels is
0.47px in that sheet. Codex's §14 record claims 56 live full-viewport frames
and 14 per-family sheets, but only the five composited masters were committed —
the full-resolution frames stayed under the ignored `.godot/` tree, so nobody
downstream can check the gate at all.
**Correction:** capture cropped to the actor's bounding box at gameplay scale,
and commit the per-family sheets, not only the masters.

**8.2 The drift gate is asserted, not evidenced.** The gate is *no actor, prop,
audience member or widget mover accumulates transform drift after twenty
repeated triggers*. Demonstrating that needs a rest frame before the twenty taps
and one after, differenced. The kit ships one frame, and §14's own wording gives
it away: "one twenty-tap rest frame", singular. The five early-exit/re-entry
frames in the same master do genuinely evidence lifecycle cleanup — that half
stands.
**Correction:** paired before/after frames plus the pixel delta for anything
claiming a drift gate.

**8.3 Every capture predates the framing repair.** All five masters still show
the near-black `<CAREER> MINIGAMES` header and the six-portrait audience row
along the painted foreground — the exact chrome removed in the framing work now
on dev at `5f5d386c`. The kit remains valid for identity, pose and registration
*inside* the painting, which is what it was made for; it is stale as framing or
composition evidence and should not be cited as either.
**Correction:** recapture after `5f5d386c` before the owner's composition review.

One incidental confirmation: the stress master shows Roshan standing roughly
twice the height of the toque'd crew imps around her. That is the 2.12x the
scale contract brings to 1.39x, so those frames are a usable *before* picture
for it.
