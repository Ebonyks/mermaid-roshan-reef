extends Node3D
class_name KartGame

const StoryArtFactory = preload("res://scripts/story_art.gd")
# ============================================================================
# RACE ENGINE — Rainbow Road racer (N64-inspired) and a reusable arcade-racing
# base for future minigames.
#
# What the player gets:
#   * VEHICLE SELECT: motorcycle / go-kart / monster truck (real CC0/CC-BY
#     models in assets/vehicles/), each handling differently.
#   * Auto-cruise + steering, HELD second finger handled by main game (jump is
#     not used here); tap / SPACE / gamepad-A fires TURBO.
#   * TURBO METER charged by zoom strips, shells and stars — the player decides
#     when to spend it. Pearls float on the track in lines; collecting them
#     pays out real game pearls at the finish (placement bonus too).
#   * Kart-vs-kart bumping (mass-weighted: the truck shoves, the moto gets
#     shoved), banked corners, variable road width, bouncy slowing walls,
#     a slightly hidden shortcut, reverse-lap variant, podium celebration.
#
# REUSE (for future minigames): call configure({...}) BEFORE start(). Any of
# these keys can be overridden — everything else keeps its default:
#   laps:int, lap_target_sec:float, road_half:float, ctrl:Array[Vector3]
#   (loop control points), origin:Vector3, racers:Array (see RACERS),
#   vehicles:Dictionary (see VEHICLES), strips/pickups/pearl_rows (u/lat
#   placement tables), shortcut:bool, sky_colors:[Color,Color],
#   pearl_payout:bool, name:String (HUD title).
# Example — a lava canyon sprint:
#   var g := KartGame.new(); add_child(g)
#   g.configure({"name": "Lava Dash", "laps": 1, "sky_colors": [Color(0.1,0,0), Color(0.4,0.1,0)], "shortcut": false})
#   g.start(self, Callable(self, "_end_kart_game"))
# ============================================================================

# ------------------------------------------------------------ tunables (defaults)
var cfg := {}                      # overrides from configure()
const LAPS := 2
const LAP_TARGET_SEC := 30.0       # vmax is derived from measured track length
const ROAD_HALF := 11.0
const COLLIDE_R := 4.5
const WALL_SLOW := 0.82
const SAMPLES := 260
const ORIGIN := Vector3(0.0, 4000.0, 0.0)
const BOOST_MUL := 0.5             # speed bonus while turbo is burning
const TURBO_TIME := 1.4            # seconds of turbo per full fire
const SELECT_TIMEOUT := 5.0        # short unattended path: two choices + countdown in about 14s

const CTRL := [
	Vector3(0, 0, 150),
	Vector3(70, 6, 132),
	Vector3(122, 18, 72),
	Vector3(142, 16, -8),
	Vector3(112, 4, -78),
	Vector3(64, -8, -120),
	Vector3(-8, -6, -150),
	Vector3(-84, 8, -118),
	Vector3(-138, 22, -48),
	Vector3(-122, 14, 26),
	Vector3(-70, 0, 92),
	Vector3(-30, 12, 132),
]
const SHORTCUT_FROM_U := 0.34
const SHORTCUT_TO_U := 0.50

# the rainbow road gets its own loop: a floating road doesn't have to hug a
# seabed, so it ROLLERCOASTERS — 66 units of climb and dive around the
# Butterfly World (owner: "track design is repetitive" — the two races now
# share nothing but the engine). Keeps every point 100+ units from the loop
# centre so the planet, moons and butterflies stay clear of the racing line.
const RAINBOW_CTRL := [
	Vector3(0, 8, 158),
	Vector3(82, 26, 138),
	Vector3(132, 44, 66),
	Vector3(158, 18, -12),
	Vector3(128, -6, -86),
	Vector3(58, -20, -132),
	Vector3(-18, 2, -160),
	Vector3(-92, 30, -126),
	Vector3(-142, 46, -50),
	Vector3(-160, 22, 34),
	Vector3(-118, -12, 96),
	Vector3(-52, -4, 148),
]

# ------------------------------------------------------------ hazards
# Gentle, telegraphed, no fail states: every hazard slows or bounces — and
# one of them (the geyser) is secretly a free jump. u = loop fraction.
# VISUAL GRAMMAR (owner 2026-07-14: "it doesn't make sense that the star is
# the hazard"): stars/gold/cyan glow = COLLECT ME, always. Hazards are the
# opposite vocabulary — dark, plum, spiky, rocky or wobbly. Never a star.
const HAZARDS_OCEAN := [
	{"u": 0.12, "kind": "crab"},      # scuttles across the road — soft bonk
	{"u": 0.30, "kind": "geyser"},    # bubbly rhythm: erupting = free jump
	{"u": 0.42, "kind": "whirl"},     # sand whirlpool tugs you toward it
	{"u": 0.52, "kind": "kelp"},      # frond patch drags (turbo powers through)
	{"u": 0.68, "kind": "crab"},
	{"u": 0.88, "kind": "geyser"},
]
const HAZARDS_RAINBOW := [
	{"u": 0.10, "kind": "comet"},     # grumpy meteor sweeps the road
	{"u": 0.33, "kind": "cloud"},     # sleepy Zzz cloud — drag zone
	{"u": 0.45, "kind": "jelly"},     # wobbly jelly-moon parked on the road: BOING
	{"u": 0.55, "kind": "pendulum"},  # swinging spike ball
	{"u": 0.72, "kind": "cloud"},
	{"u": 0.90, "kind": "comet"},
]

# meter charge per source + placement tables (u = fraction along the loop)
const STRIPS := [
	{"u": 0.08, "lat": 0.0, "len": 16.0, "hw": 7.0},
	{"u": 0.20, "lat": 5.0, "len": 14.0, "hw": 7.0},
	{"u": 0.34, "lat": -5.0, "len": 14.0, "hw": 7.0},
	{"u": 0.50, "lat": 0.0, "len": 16.0, "hw": 7.0},
	{"u": 0.62, "lat": -4.0, "len": 16.0, "hw": 7.0},
	{"u": 0.78, "lat": 4.0, "len": 14.0, "hw": 7.0},
	{"u": 0.92, "lat": 0.0, "len": 16.0, "hw": 7.0},
]
const PICKUPS := [
	# shell = turbo charge, star = BIG charge, bubble = instant zip!,
	# rainbow = full meter + sparkles. Spread so something happens every few seconds.
	{"u": 0.10, "lat": 4.0, "kind": "bubble"},
	{"u": 0.22, "lat": -5.0, "kind": "shell"},
	{"u": 0.30, "lat": 0.0, "kind": "bubble"},
	{"u": 0.38, "lat": -4.0, "kind": "star"},
	{"u": 0.45, "lat": 5.0, "kind": "star"},
	{"u": 0.55, "lat": -3.0, "kind": "bubble"},
	{"u": 0.64, "lat": 3.0, "kind": "shell"},
	{"u": 0.72, "lat": 0.0, "kind": "shell"},
	{"u": 0.80, "lat": 5.0, "kind": "bubble"},
	{"u": 0.87, "lat": -5.0, "kind": "rainbow"},
	{"u": 0.93, "lat": -3.0, "kind": "star"},
]
# jump ramps (auto-trick, MK-Tour style: no input needed — driving one is the
# trick): u fraction along the loop + lat placement
const RAMPS := [
	{"u": 0.16, "lat": 0.0},
	{"u": 0.47, "lat": -3.0},
	{"u": 0.74, "lat": 3.0},
]
const AIR_DUR := 0.85              # seconds of hang time off a ramp
# rows of collectible pearls: u start, lat, count (spaced along s)
const PEARL_ROWS := [
	{"u": 0.05, "lat": 3.0, "n": 4},
	{"u": 0.15, "lat": -4.0, "n": 4},
	{"u": 0.28, "lat": 0.0, "n": 5},
	{"u": 0.42, "lat": -5.0, "n": 4},
	{"u": 0.56, "lat": 4.0, "n": 4},
	{"u": 0.68, "lat": -2.0, "n": 5},
	{"u": 0.82, "lat": 2.0, "n": 4},
	{"u": 0.95, "lat": -4.0, "n": 3},
]
const SHELL_GLB := "res://assets/aquatic/SpiralShell.glb"
const SHELL_GEN2 := "spiralshell"

# Butterfly World centerpiece (rainbow theme): the Level-2 rainbow legs are the
# road TO stage 3, so the track orbits the Butterfly World itself — the same
# meadow planet, crystal castle and butterflies the player lands on in
# galaxy.gd — instead of circling empty starfield.
const BW_PLANET_R := 70.0
const BW_CASTLE_GLB := "res://assets/galaxy/crystal_castle.glb"
const BW_CRYSTALS := ["res://assets/galaxy/crystal1.glb", "res://assets/galaxy/crystal2.glb"]
const BW_BUTTERFLY_GLBS := ["res://assets/galaxy/butterfly1.glb", "res://assets/galaxy/butterfly2.glb"]
const BW_BUTTERFLY_STORY_GLB := "res://assets/props/gen2/butterfly_story.glb"
const BW_BUTTERFLY_CARDS := ["butterfly1", "butterfly2"]
const BW_WING_COLS := [Color(1.0, 0.5, 0.15), Color(0.25, 0.45, 1.0), Color(0.75, 1.0, 0.85), Color(1.0, 0.85, 0.3), Color(0.95, 0.35, 0.4), Color(0.6, 0.4, 1.0), Color(0.4, 0.8, 1.0)]
# ------------------------------------------------------------ vehicles
# handling: vmax (x base), steer (lat u/s), wall (speed kept on scrape),
# mass (collision shove weight), turbo (x BOOST_MUL), slip (lat drift keep),
# scale/y_off/yaw_fix (model placement), blurb (select screen)
const VEHICLES := {
	# tuned by simulation (200k-token stress campaign): each ride has a REAL
	# identity — moto = raw speed but fragile, kart = turbo economy, truck =
	# bumper king (mass WINS every collision, walls barely slow it).
	"moto": {
		"label": "Zoom Cycle", "blurb": "PRO: fastest + super steering / CON: so light, bumps toss it!",
		"glb": "res://assets/vehicles/motorcycle.glb",
		"vmax": 1.08, "steer": 30.0, "wall": 0.62, "mass": 0.6,
		"turbo": 1.2, "slip": 0.45, "size": 5.0, "yaw_fix": 0.0,   # model faces -Z: correct as-is (verified render)
		"lean": 0.5,
	},
	"kart": {
		"label": "Rainbow Kart", "blurb": "PRO: turbo champ - pickups charge extra! / CON: no muscle",
		"glb": "res://assets/vehicles/gokart.glb",
		"vmax": 1.0, "steer": 22.0, "wall": 0.82, "mass": 1.0, "mcharge": 1.3,
		"turbo": 1.35, "slip": 0.12, "size": 6.0, "yaw_fix": -PI * 0.5,   # model faces -X: was riding sideways (verified render)
		"lean": 0.15,
	},
	"truck": {
		"label": "Monster Truck", "blurb": "PRO: BUMPER KING - shove everyone, walls can't stop it / CON: slowest",
		"glb": "res://assets/vehicles/monstertruck_story.glb",
		"legacy_glb": "res://assets/vehicles/monstertruck.glb",
		"vmax": 0.985, "steer": 16.0, "wall": 0.97, "mass": 2.2,
		"turbo": 0.9, "slip": 0.0, "size": 7.5, "yaw_fix": PI,   # model faces +Z: was driving backwards (verified render)
		"lean": 0.05,
	},
}
const VEHICLE_ORDER := ["moto", "kart", "truck"]

# paint jobs (second step of the select screen). "rainbow" uses a hue-cycling shader.
const PAINTS := [
	{"label": "Stock", "col": null},
	{"label": "Cherry", "col": Color(0.9, 0.15, 0.2)},
	{"label": "Sky", "col": Color(0.35, 0.65, 1.0)},
	{"label": "Bubblegum", "col": Color(1.0, 0.5, 0.8)},
	{"label": "Lime", "col": Color(0.45, 0.9, 0.35)},
	{"label": "Grape", "col": Color(0.6, 0.35, 0.95)},
	{"label": "Gold", "col": Color(1.0, 0.8, 0.25)},
	{"label": "RAINBOW!", "col": null, "rainbow": true},
]

# Racer roster: deliberately AVOIDS the reef friends (Faron, Harper & Fiona,
# Gabby, Wacky & Chuck, Evie & Lamb-a') — seeing them race past themselves
# standing in the ocean broke the fiction. These characters live in the toy
# nursery / story world instead, so they never appear twice at once.
const RACERS := [
	{"name": "Roshan", "col": Color(1.0, 0.4, 0.8), "sprite": "res://assets/characters/roshan_sprite.png", "player": true},
	{"name": "Sparkle", "col": Color(1.0, 0.85, 0.35), "sprite": "res://assets/book/baby_eagle.png"},
	{"name": "Princess Huluu", "col": Color(0.75, 0.55, 1.0), "sprite": "res://assets/characters/friends/huluu.png"},
	{"name": "Bunny", "col": Color(0.95, 0.95, 1.0), "sprite": "res://assets/book/doll_bunny.png"},
	{"name": "Kitty", "col": Color(1.0, 0.6, 0.4), "sprite": "res://assets/book/doll_cat.png"},
	{"name": "Baby Doll", "col": Color(0.45, 0.85, 1.0), "sprite": "res://assets/book/baby_doll.png"},
	{"name": "Dolly", "col": Color(0.6, 1.0, 0.7), "sprite": "res://assets/book/baby_doll2.png"},
	{"name": "Sleepy", "col": Color(0.8, 0.7, 1.0), "sprite": "res://assets/book/baby_doll3.png"},
]

# ------------------------------------------------------------ state
var _main: Node = null
var _player_node: Node3D = null
var _finish_cb: Callable
var _cam: Camera3D = null
var _prev_env: Environment = null
var _hud: CanvasLayer = null
var _lbl_place: Label = null
var _lbl_lap: Label = null
var _lbl_big: Label = null
var _lbl_pearls: Label = null
var _lbl_hint: Label = null
var _guide_pointer: Label = null
var _guide_mode := ""
var _guide_t := 0.0
var _meter_bg: ColorRect = null
var _meter_fill: ColorRect = null
var _btn_quit: Button = null

var _lut: PackedVector3Array = []
var _cum: PackedFloat32Array = []
var _len := 0.0
var _vmax := 40.0

var _karts: Array = []
var _pl = null
var _strip_data: Array = []
var _ramp_data: Array = []         # jump pads: {pos: Vector3}
var _pickups_live: Array = []
var _pearls_live: Array = []
var _state := "select"             # select -> countdown -> race -> podium -> done
var _clock := 0.0
var _race_t := 0.0
var _shortcut_used_lap := -1
var _rev := false
var _pearls_got := 0
var _payout_banked := 0
var _payout_dirty := false
var _completion_committed := false
var _fire_prev := false
var _rocket_armed := false
var _select_confirm_queued := false
var _sel_idx := 1                  # start highlight on the kart
var _sel_nodes: Array = []
var _sel_t := 0.0
var _sel_move_prev := 0
var _sel_phase := "ride"           # ride -> paint
var _paint_idx := 0
var _paint_orbs: Array = []
var _paint_prev := -1
var _quit_arm_t := 0.0
var _bw_centre := Vector3.ZERO     # Butterfly World planet centre (rainbow theme)
var _bw_planet: MeshInstance3D = null
var _bw_spin: Node3D = null        # landmark carrier — turns with the planet surface
var _bw_flyers: Array = []         # orbiting butterflies: {node, axis, dir0, alt, spd, ph, flap}
var _bw_moons: Array = []          # candy moons: {node, r, spd, ph, tilt}

# ------------------------------------------------------------ config access

const TouchUI := preload("res://scripts/touch_ui.gd")

func _touch_device() -> bool:
	return TouchUI.wants_touch()

func action_label() -> String:
	# what the touch action bubble should read right now (main polls this each frame)
	if _state == "select" or _state == "countdown":
		return "GO!"
	if _state == "race":
		return "TURBO"
	return "★"

func joy_axis(axis: int) -> float:
	# delegate to main's gamepad layer (multi-device + raw fallback for pads
	# Godot has no SDL mapping for, like the 8BitDo Lite family)
	var m: Node = _main
	if m != null and m.has_method("joy_axis"):
		return m.joy_axis(axis)
	return Input.get_joy_axis(0, axis)

func joy_pressed(btn: int) -> bool:
	var m: Node = _main
	if m != null and m.has_method("joy_pressed"):
		return m.joy_pressed(btn)
	return Input.is_joy_button_pressed(0, btn)

func configure(overrides: Dictionary) -> void:
	cfg = overrides

func _cv(key: String, dflt):
	return cfg[key] if cfg.has(key) else dflt

func _laps() -> int:
	return int(_cv("laps", LAPS))

func _theme() -> String:
	return String(_cv("theme", "ocean"))   # "ocean" (seabed race) or "rainbow" (orbiting the Butterfly World)

func _ground_mode() -> String:
	# "terrain": the track conforms to the REAL reef seabed in world 1 (default).
	# "float":   the classic floating course in its own pocket (Level-2 rainbow).
	return String(_cv("ground", "terrain"))

func _terrain_y(x: float, z: float) -> float:
	if _main != null and _main.has_method("seabed_y"):
		return float(_main.seabed_y(x, z))
	return 0.0

func _rhalf() -> float:
	return float(_cv("road_half", ROAD_HALF))

# ------------------------------------------------------------ spline maths
func _catmull(p0: Vector3, p1: Vector3, p2: Vector3, p3: Vector3, t: float) -> Vector3:
	var t2 := t * t
	var t3 := t2 * t
	return 0.5 * ((2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2 + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3)

func _ctrl_pts() -> Array:
	# the floating rainbow race rides its own rollercoaster loop; the seabed
	# race keeps the terrain-hugging line (its shape comes from the reef)
	var dflt: Array = RAINBOW_CTRL if (_theme() == "rainbow" and _ground_mode() == "float") else CTRL
	return _cv("ctrl", dflt)

func _origin() -> Vector3:
	if _ground_mode() == "terrain":
		return _cv("origin", Vector3.ZERO)   # world coordinates: the loop rings the real reef
	return _cv("origin", ORIGIN)

func _spline_u(u: float) -> Vector3:
	var pts: Array = _ctrl_pts()
	var n := pts.size()
	var f: float = fposmod(u, 1.0) * float(n)
	var i: int = int(floor(f))
	var t: float = f - float(i)
	var p0: Vector3 = pts[(i - 1 + n) % n]
	var p1: Vector3 = pts[i % n]
	var p2: Vector3 = pts[(i + 1) % n]
	var p3: Vector3 = pts[(i + 2) % n]
	var p := _origin() + _catmull(p0, p1, p2, p3, t)
	if _ground_mode() == "terrain":
		p.y = _terrain_y(p.x, p.z) + 1.4   # hug the ACTUAL sea floor
	return p

func _build_lut() -> void:
	_lut = PackedVector3Array()
	var raw: Array = []
	for i in range(SAMPLES + 1):
		raw.append(_spline_u(float(i) / float(SAMPLES)))
	if _ground_mode() == "terrain":
		# smooth the terrain-sampled heights (±4 samples ≈ ±14u) so bumps become
		# rollers, not cliffs — karts and the ribbon both use this smoothed line
		var sm: Array = []
		for i in range(SAMPLES + 1):
			var acc := 0.0
			for w in range(-4, 5):
				acc += (raw[(i + w + SAMPLES) % SAMPLES] as Vector3).y
			var p: Vector3 = raw[i]
			sm.append(Vector3(p.x, acc / 9.0, p.z))
		raw = sm
	_cum = PackedFloat32Array()
	var d := 0.0
	for i in range(SAMPLES + 1):
		if i > 0:
			d += (raw[i - 1] as Vector3).distance_to(raw[i])
		_lut.append(raw[i])
		_cum.append(d)
	_len = d
	_vmax = _len / float(_cv("lap_target_sec", LAP_TARGET_SEC))
	# curvature table (forward-travel sign): central difference of tangents,
	# Δs = 6 either side — sampled once so the per-frame lookup is O(log n)
	_kap = PackedFloat32Array()
	_kap.resize(SAMPLES + 1)
	for i in range(SAMPLES + 1):
		var t0 := _tangent_at(_cum[i] - 6.0)
		var t1 := _tangent_at(_cum[i] + 6.0)
		_kap[i] = signf(t0.cross(t1).y) * t0.angle_to(t1) / 12.0

var _kap: PackedFloat32Array = []

func _pos_at(s: float) -> Vector3:
	var ss := fposmod(s, _len)
	# binary search (bsearch = first index with _cum[i] >= ss, so the segment
	# is i-1) — this is the hottest function in the engine; the old linear walk
	# cost O(SAMPLES) per call, dozens of times a frame on the phone
	var i: int = clampi(_cum.bsearch(ss) - 1, 0, SAMPLES - 1)
	var seg: float = _cum[i + 1] - _cum[i]
	var t: float = 0.0 if seg <= 0.0001 else (ss - _cum[i]) / seg
	return _lut[i].lerp(_lut[i + 1], t)

func _tangent_at(s: float) -> Vector3:
	var a := _pos_at(s - 3.0)
	var b := _pos_at(s + 3.0)
	var dir := b - a
	if dir.length() < 0.001:
		return Vector3.FORWARD
	return dir.normalized()

func _width_at(s: float) -> float:
	var u := fposmod(s, _len) / _len
	return _rhalf() * (1.0 + 0.32 * sin(u * TAU * 2.0))

func _bank_at(s: float) -> float:
	var t0 := _tangent_at(s - 10.0)
	var t1 := _tangent_at(s + 10.0)
	return clampf(t0.cross(t1).y * 4.0, -0.4, 0.4)

func _frame_at(s: float, lat: float) -> Array:
	var fwd := _tangent_at(s)
	var flat_right := fwd.cross(Vector3.UP).normalized()
	var bank := _bank_at(s)
	var right := flat_right.rotated(fwd, bank)
	var up := Vector3.UP.rotated(fwd, bank)
	var pos := _pos_at(s) + right * lat
	return [pos, fwd, right, up]

func _eff(s: float) -> float:
	var m := fposmod(s, _len)
	return (_len - m) if _rev else m

func _curv_at(s: float) -> float:
	# signed curvature of the racing line in the kart's TRAVEL frame
	# (+ = the road bends left; the inside of the bend is then the -lat side).
	# Precomputed table (see _build_lut) — this runs for every kart every frame
	# on a 3-4-year-old phone, so no live spline sampling here.
	if _kap.is_empty():
		return 0.0
	var es := fposmod(_eff(s), _len)
	var i: int = clampi(_cum.bsearch(es), 0, SAMPLES)
	return (-_kap[i]) if _rev else _kap[i]

func _advance(k: Dictionary, delta: float) -> void:
	# curvature-coupled progress: the inside of a bend IS a shorter arc, so
	# hugging it moves you further along the track per metre driven. This is
	# what makes the racing line REAL (before this, lat was cosmetic and the
	# lap time of any line was identical). Invisible, no reading required,
	# physically truthful. Capped so the sharpest bend gives ~18 %.
	var kap := _curv_at(float(k["s"]))
	var line: float = clampf(float(k["lat"]) * kap, -0.18, 0.18)
	k["s"] = float(k["s"]) + float(k["speed"]) * (1.0 - line) * delta

func _kart_frame(s: float, lat: float) -> Array:
	var es := _eff(s)
	var fwd := _tangent_at(es)
	var bank := _bank_at(es)
	if _rev:
		fwd = -fwd
		bank = -bank
	var flat_right := fwd.cross(Vector3.UP).normalized()
	var right := flat_right.rotated(fwd, bank)
	var up := Vector3.UP.rotated(fwd, bank)
	var pos := _pos_at(es) + right * lat
	return [pos, fwd, right, up]

# ------------------------------------------------------------ lifecycle
func start(main: Node, finish_cb: Callable, reversed_track: bool = false) -> void:
	_main = main
	_finish_cb = finish_cb
	_rev = reversed_track
	_payout_banked = 0
	_payout_dirty = false
	_completion_committed = false
	_rocket_armed = false
	_select_confirm_queued = false
	_quit_arm_t = 0.0
	if "player" in main and main.player != null:
		_player_node = main.player
	_build_lut()
	_build_sky()
	if _theme() == "rainbow" and _ground_mode() == "float":
		_build_butterfly_world()
	_build_track()
	_build_strips()
	_build_pickups()
	_build_pearls()
	_build_ramps()
	_build_hazards()
	_build_engine()
	_build_camera()
	_build_hud()
	_build_select()
	_clear_corridor()
	_state = "select"
	_sel_t = 0.0

func _notification(what: int) -> void:
	# Android normally sends a pause notification before the process can be
	# evicted. Bank the pearls already collected at that point; the incremental
	# payout helper will add only the remainder and finish bonus if play resumes.
	if what == NOTIFICATION_APPLICATION_PAUSED and _main != null and (_payout_dirty or _pearls_got > _payout_banked):
		_commit_payout(0)

var _hidden_props: Array = []

func _clear_corridor() -> void:
	# hide world props (rocks, kelp, corals, sprites) that sit ON the racing line;
	# restored at teardown. Big-footprint nodes (terrain, water, caustics) are kept.
	if _ground_mode() != "terrain" or _main == null:
		return
	var pts: Array = []
	var centre := Vector2.ZERO
	for i in range(0, SAMPLES, 6):
		pts.append(_lut[i])
		centre += Vector2((_lut[i] as Vector3).x, (_lut[i] as Vector3).z)
	centre /= float(pts.size())
	var track_r := 0.0
	for q in pts:
		track_r = maxf(track_r, centre.distance_to(Vector2((q as Vector3).x, (q as Vector3).z)))
	for c in _main.get_children():
		if not (c is Node3D):
			continue
		if c == self or c == _player_node:
			continue
		if c is Camera3D or c is WorldEnvironment or c is DirectionalLight3D or c is CPUParticles3D:
			continue
		var n3 := c as Node3D
		var p := n3.global_position
		# cheap prefilter: skip anything far outside the track's bounding circle
		if centre.distance_to(Vector2(p.x, p.z)) > track_r + 25.0:
			continue
		var acc: Array = []
		_gather_aabbs(n3, Transform3D.IDENTITY, acc)
		if acc.size() > 0:
			var bb: AABB = acc[0]
			for k in range(1, acc.size()):
				bb = bb.merge(acc[k])
			if maxf(bb.size.x, bb.size.z) > 70.0:
				continue   # terrain / water / other huge meshes stay
		var hit := false
		for q in pts:
			if Vector2(p.x - (q as Vector3).x, p.z - (q as Vector3).z).length() < 21.0:
				hit = true
				break
		if hit and n3.visible:
			n3.visible = false
			_hidden_props.append(n3)

func _sky_defaults() -> Array:
	if _theme() == "ocean":
		return [Color(0.01, 0.08, 0.14), Color(0.06, 0.30, 0.42)]
	return [Color(0.02, 0.01, 0.06), Color(0.10, 0.04, 0.20)]

func _build_sky() -> void:
	if _ground_mode() == "terrain":
		return   # the race runs inside the real reef — its water, light and fog stay
	if "we_node" in _main and _main.we_node != null:
		_prev_env = _main.we_node.environment
		var e := Environment.new()
		e.background_mode = Environment.BG_COLOR
		var sky_cols: Array = _cv("sky_colors", _sky_defaults())
		e.background_color = sky_cols[0]
		e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		e.ambient_light_color = (Color(0.45, 0.65, 0.75) if _theme() == "ocean" else Color(0.5, 0.5, 0.7))
		e.ambient_light_energy = 1.0
		e.glow_enabled = not _speedy()
		e.glow_intensity = 0.5
		if _theme() == "ocean":
			e.fog_enabled = true
			e.fog_light_color = Color(0.08, 0.28, 0.38)
			e.fog_density = 0.004
		_main.we_node.environment = e
	# sun so the vehicle models are actually lit (the pocket had no light source)
	var sun := DirectionalLight3D.new()
	sun.light_energy = 1.3
	sun.light_color = (Color(0.85, 0.95, 1.0) if _theme() == "ocean" else Color(1.0, 0.95, 0.9))
	sun.rotation_degrees = Vector3(-52, 30, 0)
	add_child(sun)
	var sky := MeshInstance3D.new()
	var sm := SphereMesh.new()
	sm.radius = 900.0
	sm.height = 1800.0
	# NOTE: no flip_faces — the shader's cull_front already renders the inside.
	# (flip_faces + cull_front double-negated and made the dome invisible, letting
	# the real world's sky bleed through behind the course.)
	sky.mesh = sm
	var sh := Shader.new()
	if _theme() == "rainbow":
		# stage 3's own galaxy-and-aurora sky (same shader as galaxy.gd) — the
		# rainbow road pocket IS Butterfly World space, seen from orbit
		sh.code = """shader_type spatial;
render_mode unshaded, cull_front;
float h21(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5); }
float noise2(vec2 p){
	vec2 i = floor(p); vec2 f = fract(p);
	vec2 u = f * f * (3.0 - 2.0 * f);
	return mix(mix(h21(i), h21(i + vec2(1, 0)), u.x), mix(h21(i + vec2(0, 1)), h21(i + vec2(1, 1)), u.x), u.y);
}
void fragment(){
	vec2 uv = UV;
	vec3 col = mix(vec3(0.01, 0.005, 0.04), vec3(0.05, 0.02, 0.10), uv.y);
	vec2 g1 = uv * vec2(260.0, 140.0);
	float s1 = step(0.994, h21(floor(g1))) * (1.0 - smoothstep(0.0, 0.22, length(fract(g1) - 0.5)));
	vec2 g2 = uv * vec2(120.0, 70.0);
	float tw = 0.6 + 0.4 * sin(TIME * 2.0 + h21(floor(g2)) * 40.0);
	float s2 = step(0.990, h21(floor(g2) + 7.0)) * (1.0 - smoothstep(0.0, 0.3, length(fract(g2) - 0.5))) * tw;
	col += vec3(s1) + vec3(1.0, 0.9, 0.8) * s2;
	vec2 gc = (uv - vec2(0.72, 0.62)) * vec2(2.0, 3.6);
	float r = length(gc);
	float ang = atan(gc.y, gc.x);
	float arm = 0.5 + 0.5 * cos(ang * 2.0 - r * 9.0 + TIME * 0.02);
	float gal = exp(-r * 3.2) * (0.35 + 0.65 * arm);
	col += vec3(0.85, 0.7, 1.0) * gal * 0.9 + vec3(1.0, 0.9, 0.75) * exp(-r * 9.0);
	float band = uv.y - 0.32;
	float wob = noise2(vec2(uv.x * 6.0 + TIME * 0.05, TIME * 0.03)) * 0.14;
	float rib1 = exp(-pow((band - wob) * 9.0, 2.0));
	float rib2 = exp(-pow((band - wob - 0.06) * 12.0, 2.0));
	float rib3 = exp(-pow((band - wob + 0.07) * 14.0, 2.0));
	float flow = 0.6 + 0.4 * sin(uv.x * 24.0 + TIME * 0.4);
	col += vec3(0.2, 1.0, 0.55) * rib1 * 0.55 * flow;
	col += vec3(0.45, 0.35, 1.0) * rib2 * 0.4;
	col += vec3(1.0, 0.4, 0.75) * rib3 * 0.32;
	ALBEDO = col;
	EMISSION = col * 0.8;
}"""
	else:
		sh.code = """shader_type spatial;
render_mode unshaded, cull_front;
uniform vec3 col_lo = vec3(0.02, 0.01, 0.08);
uniform vec3 col_hi = vec3(0.10, 0.04, 0.20);
float h(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5); }
void fragment(){
	vec2 uv = UV * vec2(220.0, 120.0);
	vec2 c = floor(uv); vec2 f = fract(uv);
	float r = h(c);
	float star = step(0.992, r) * (1.0 - smoothstep(0.0, 0.18, length(f - 0.5)));
	vec3 sky = mix(col_lo, col_hi, UV.y);
	ALBEDO = sky + vec3(star);
	EMISSION = vec3(star) * 1.5;
}"""
	var smat := ShaderMaterial.new()
	smat.shader = sh
	if _theme() != "rainbow":
		var sky_cols2: Array = _cv("sky_colors", _sky_defaults())
		smat.set_shader_parameter("col_lo", Vector3(sky_cols2[0].r, sky_cols2[0].g, sky_cols2[0].b))
		smat.set_shader_parameter("col_hi", Vector3(sky_cols2[1].r, sky_cols2[1].g, sky_cols2[1].b))
	sky.material_override = smat
	sky.position = _origin()
	add_child(sky)
	# ocean: slow bubble columns drifting up through the course
	if _theme() == "ocean":
		var bub := CPUParticles3D.new()
		bub.amount = 70
		bub.lifetime = 9.0
		bub.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
		bub.emission_box_extents = Vector3(170, 10, 170)
		bub.direction = Vector3(0, 1, 0)
		bub.gravity = Vector3(0, 1.4, 0)
		bub.initial_velocity_min = 1.0
		bub.initial_velocity_max = 3.0
		bub.scale_amount_min = 0.15
		bub.scale_amount_max = 0.6
		var bm := SphereMesh.new()
		bm.radius = 0.5
		bm.height = 1.0
		bub.mesh = bm
		var bmat := StandardMaterial3D.new()
		bmat.albedo_color = Color(0.75, 0.92, 1.0, 0.5)
		bmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		bmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		bub.mesh.material = bmat
		bub.position = _origin() + Vector3(0, 0, 0)
		add_child(bub)

# ------------------------------------------------------------ Butterfly World (rainbow theme)
func _bw_tint(root: Node, col: Color, glow: float) -> void:
	# same pastel-glass tint galaxy.gd gives its props, so the world reads as ONE place
	var stack: Array = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch in n.get_children():
			stack.append(ch)
		if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
			var mi := n as MeshInstance3D
			for si in range(mi.mesh.get_surface_count()):
				var src: Material = mi.get_active_material(si)
				var m: BaseMaterial3D = (src.duplicate() if src is BaseMaterial3D else StandardMaterial3D.new())
				m.albedo_color = m.albedo_color.lerp(col, 0.5)
				m.emission_enabled = true
				m.emission = col
				m.emission_energy_multiplier = glow
				mi.set_surface_override_material(si, m)

func _bw_place(node: Node3D, dir: Vector3, sink: float = 1.5) -> void:
	# stand a landmark on the globe (LOCAL to the spin carrier): position on
	# the surface, local up = radially out (mirrors galaxy.gd's _place_on_planet)
	var d := dir.normalized()
	node.position = d * (BW_PLANET_R - sink)
	var any := Vector3.UP if absf(d.dot(Vector3.UP)) < 0.95 else Vector3.RIGHT
	var t := any.cross(d).normalized()
	node.transform.basis = Basis(t, d, t.cross(d).normalized() * -1.0).orthonormalized()

func _bw_fit(model: Node3D, target_long: float) -> void:
	# normalise a GLB to a footprint and centre it (mirrors galaxy.gd's _fit_small)
	if not model.has_meta("gen2") and _main != null and _main.has_method("_toonify"):
		_main._toonify(model)
	var acc: Array = []
	_gather_aabbs(model, Transform3D.IDENTITY, acc)
	if acc.is_empty():
		return
	var bb: AABB = acc[0]
	for i in range(1, acc.size()):
		bb = bb.merge(acc[i])
	var longest: float = maxf(maxf(bb.size.x, bb.size.z), maxf(bb.size.y, 0.001))
	var sc: float = target_long / longest
	model.scale = Vector3.ONE * sc
	var c: Vector3 = bb.position + bb.size * 0.5
	model.position = Vector3(-c.x * sc, -bb.position.y * sc, -c.z * sc)

func _build_butterfly_world() -> void:
	# centre the world inside the loop: track points ring it at ~105+ units, so a
	# 70-radius planet sunk 40 below the racing line fills the view without ever
	# touching the road, the karts or the chase camera
	var centroid := Vector3.ZERO
	for i in range(SAMPLES):
		centroid += _lut[i]
	centroid /= float(SAMPLES)
	# raised so the orb LOOMS over the inner horizon from track level (owner
	# feedback: it must read from every point of the loop, not just from above)
	_bw_centre = centroid + Vector3(0, -22.0, 0)
	# the meadow planet — same shader as galaxy.gd so it IS the stage-3 world
	_bw_planet = MeshInstance3D.new()
	var pm := SphereMesh.new()
	pm.radius = BW_PLANET_R
	pm.height = BW_PLANET_R * 2.0
	pm.radial_segments = 48 if _speedy() else 96
	pm.rings = 24 if _speedy() else 48
	_bw_planet.mesh = pm
	var sh := Shader.new()
	sh.code = """shader_type spatial;
float h21(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5); }
void fragment(){
	// flowering-meadow planet (the butterfly-house garden): soft grass with
	// sandy landscaped paths and thousands of tiny flower dots
	float band = sin(UV.y * 14.0) * 0.5 + 0.5;
	// deeper greens than the walk-on version: seen from orbit through the
	// storybook grade + bloom, the original pale meadow flattened to a
	// featureless cyan wall — richer bands keep the orb readable
	vec3 a = vec3(0.30, 0.62, 0.30);   // meadow green
	vec3 b = vec3(0.48, 0.80, 0.38);   // sunlit grass
	vec3 col = mix(a, b, band);
	// two winding garden paths circling the planet
	float wob = sin(UV.x * 12.566) * 0.03;
	float pathm = exp(-pow((UV.y - 0.36 + wob) * 34.0, 2.0)) + exp(-pow((UV.y - 0.66 - wob) * 34.0, 2.0));
	col = mix(col, vec3(0.86, 0.76, 0.52), clamp(pathm, 0.0, 1.0) * 0.85);
	// confetti of tiny flowers (bigger + denser than the walk-on version:
	// they must survive being seen from the racetrack)
	vec2 g = UV * vec2(220.0, 120.0);
	float fh = h21(floor(g));
	float dot2 = step(0.980, fh) * (1.0 - smoothstep(0.06, 0.36, length(fract(g) - 0.5)));
	vec3 fcol = 0.55 + 0.45 * cos(6.28 * (fh * 7.0 + vec3(0.0, 0.33, 0.67)));
	col = mix(col, fcol, dot2 * (1.0 - clamp(pathm, 0.0, 1.0)));
	// firefly sparkle at "night" side
	float sparkle = step(0.996, h21(floor(g) + 31.0)) * (0.5 + 0.5 * sin(TIME * 3.0 + fh * 50.0));
	ALBEDO = col;
	EMISSION = col * 0.08 + vec3(1.0, 0.95, 0.6) * sparkle * 0.5;
	ROUGHNESS = 0.85;
}"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	_bw_planet.material_override = mat
	_bw_planet.position = _bw_centre
	add_child(_bw_planet)
	# atmosphere: slightly larger fresnel shell. The additive full-screen shell
	# is costly fill on the phone and the planet remains clear without it.
	if not _speedy():
		var atmo := MeshInstance3D.new()
		var am := SphereMesh.new()
		am.radius = BW_PLANET_R * 1.06
		am.height = BW_PLANET_R * 2.12
		atmo.mesh = am
		var ash := Shader.new()
		ash.code = """shader_type spatial;
render_mode unshaded, blend_add, cull_back;
void fragment(){
	float f = pow(1.0 - clamp(dot(normalize(NORMAL), normalize(VIEW)), 0.0, 1.0), 2.5);
	ALBEDO = vec3(0.55, 0.5, 1.0) * f * 0.55;
	ALPHA = f * 0.55;
}"""
		var amat := ShaderMaterial.new()
		amat.shader = ash
		atmo.material_override = amat
		atmo.position = _bw_centre
		add_child(atmo)
	# landmark carrier: everything standing ON the globe is a child of this
	# node, which turns at the same rate as the planet mesh — so the castle
	# and jungle ride the surface instead of hovering while it spins
	_bw_spin = Node3D.new()
	_bw_spin.position = _bw_centre
	add_child(_bw_spin)
	# the crystal castle at the north pole, amethyst-tinted like stage 3
	var castle := Node3D.new()
	if ResourceLoader.exists(BW_CASTLE_GLB):
		var ck: Node3D = (load(BW_CASTLE_GLB) as PackedScene).instantiate()
		castle.add_child(ck)
		_bw_fit(ck, 40.0)
		StoryArtFactory.apply_triplanar(ck, "res://assets/terrain/up_crystal_col.png", 0.08, Color(0.96, 0.94, 1.0))
	for i in range(BW_CRYSTALS.size()):
		var path: String = BW_CRYSTALS[i]
		if not ResourceLoader.exists(path):
			continue
		var spire: Node3D = (load(path) as PackedScene).instantiate()
		spire.scale = Vector3.ONE * 4.5
		spire.position = Vector3([-15.0, 15.0][i], 0, 7.0)
		castle.add_child(spire)
		StoryArtFactory.apply_triplanar(spire, "res://assets/terrain/up_crystal_col.png", 0.16)
	# sunk a little so its base corners don't hover above the curving horizon
	castle.position = Vector3(0, BW_PLANET_R - 6.0, 0)
	_bw_spin.add_child(castle)
	# the rest of stage 3's landmarks, scattered around the globe: the tropical
	# jungle and the crystal outcrops (so the orb reads as THAT world from
	# orbit, not a generic green ball)
	var marks := [
		{"role": "trop_palm1", "dir": Vector3(0.9, 0.30, 0.3), "size": 17.0},
		{"role": "trop_palm2", "dir": Vector3(-0.7, 0.15, 0.7), "size": 16.0},
		{"role": "trop_monstera", "dir": Vector3(0.2, 0.5, -0.85), "size": 12.0},
		{"glb": "res://assets/galaxy/crystal1.glb", "dir": Vector3(-0.5, 0.45, -0.75), "size": 13.0, "tint": Color(0.8, 0.7, 1.0)},
		{"glb": "res://assets/galaxy/crystal2.glb", "dir": Vector3(0.6, -0.15, -0.8), "size": 12.0, "tint": Color(0.7, 0.85, 1.0)},
		{"glb": "res://assets/galaxy/crystal3.glb", "dir": Vector3(-0.9, -0.3, 0.25), "size": 12.0, "tint": Color(0.85, 0.7, 1.0)},
	]
	for md in marks:
		var holder := Node3D.new()
		var prop: Node3D = null
		if md.has("role"):
			prop = StoryArtFactory.plant(String(md["role"]), float(md["size"]))
		else:
			var mpath := String(md["glb"])
			if ResourceLoader.exists(mpath):
				prop = (load(mpath) as PackedScene).instantiate()
		if prop == null:
			continue
		holder.add_child(prop)
		if not md.has("role"):
			_bw_fit(prop, float(md["size"]))
			StoryArtFactory.apply_triplanar(prop, "res://assets/terrain/up_crystal_col.png", 0.16)
		_bw_place(holder, md["dir"])
		_bw_spin.add_child(holder)
	# the seven butterflies circle their world (they're what stage 3 is about)
	var butterfly_count: int = 4 if _speedy() else BW_WING_COLS.size()
	for i in range(butterfly_count):
		var holder := Node3D.new()
		var bf: Node3D = null
		if ResourceLoader.exists(BW_BUTTERFLY_STORY_GLB):
			bf = (load(BW_BUTTERFLY_STORY_GLB) as PackedScene).instantiate()
			holder.set_meta("wing_l", bf.find_child("wing_L", true, false))
			holder.set_meta("wing_r", bf.find_child("wing_R", true, false))
		elif ResourceLoader.exists("res://assets/props/gen2/%s.png" % BW_BUTTERFLY_CARDS[i % BW_BUTTERFLY_CARDS.size()]):
			bf = _gen2_card(BW_BUTTERFLY_CARDS[i % BW_BUTTERFLY_CARDS.size()], 7.0)
		else:
			var bpath: String = BW_BUTTERFLY_GLBS[i % BW_BUTTERFLY_GLBS.size()]
			if ResourceLoader.exists(bpath):
				bf = (load(bpath) as PackedScene).instantiate()
		if bf != null:
			holder.add_child(bf)
			_bw_fit(bf, 7.0)
			_bw_tint(bf, BW_WING_COLS[i], 0.3)
		else:
			var q := MeshInstance3D.new()
			var qm := QuadMesh.new()
			qm.size = Vector2(7.0, 4.9)
			q.mesh = qm
			var qmat := StandardMaterial3D.new()
			qmat.albedo_color = BW_WING_COLS[i]
			qmat.emission_enabled = true
			qmat.emission = BW_WING_COLS[i]
			qmat.emission_energy_multiplier = 0.3
			qmat.cull_mode = BaseMaterial3D.CULL_DISABLED
			q.material_override = qmat
			holder.add_child(q)
		add_child(holder)
		var d0 := Vector3(sin(float(i) * 2.4), cos(float(i) * 1.7), sin(float(i) * 3.1 + 1.0)).normalized()
		var ax := d0.cross(Vector3(cos(float(i) * 1.3), sin(float(i) * 2.1), cos(float(i) * 0.7 + 2.0)).normalized()).normalized()
		_bw_flyers.append({"node": holder, "axis": ax, "dir0": d0, "alt": 7.0 + fposmod(float(i) * 3.3, 10.0), "spd": 0.10 + fposmod(float(i) * 0.05, 0.14), "ph": float(i) * 0.9, "flap": 12.0 + fposmod(float(i) * 2.6, 8.0)})
	# two candy moons — kept INSIDE the loop (track rings the centre at ~105+)
	for i in range(2):
		var moon := MeshInstance3D.new()
		var mm := SphereMesh.new()
		mm.radius = [3.2, 2.4][i]
		mm.height = mm.radius * 2.0
		moon.mesh = mm
		var mmat := StandardMaterial3D.new()
		mmat.albedo_color = [Color(1.0, 0.62, 0.2), Color(0.45, 0.8, 0.35)][i]   # orange + melon moons
		mmat.emission_enabled = true
		mmat.emission = mmat.albedo_color
		mmat.emission_energy_multiplier = 0.5
		moon.material_override = mmat
		add_child(moon)
		_bw_moons.append({"node": moon, "r": BW_PLANET_R * (1.14 + 0.12 * float(i)), "spd": 0.15 - 0.05 * float(i), "ph": float(i) * 2.4, "tilt": 0.3 + 0.2 * float(i)})

func _tick_butterfly_world(tt: float) -> void:
	if _bw_planet == null:
		return
	_bw_planet.rotation.y = tt * 0.03   # the world turns slowly beneath the road
	if _bw_spin != null:
		_bw_spin.rotation.y = tt * 0.03   # castle + jungle ride the turning surface
	for md in _bw_moons:
		var ph: float = tt * float(md["spd"]) + float(md["ph"])
		var tilt: float = float(md["tilt"])
		(md["node"] as Node3D).position = _bw_centre + Vector3(cos(ph) * float(md["r"]), sin(ph * 0.7) * float(md["r"]) * tilt * 0.4, sin(ph) * float(md["r"]))
	for fd in _bw_flyers:
		var bn: Node3D = fd["node"]
		var ang: float = tt * float(fd["spd"]) + float(fd["ph"])
		var pdir: Vector3 = ((fd["dir0"] as Vector3).rotated(fd["axis"], ang)).normalized()
		var alt: float = float(fd["alt"]) + sin(tt * 1.3 + float(fd["ph"])) * 0.8
		var newp: Vector3 = _bw_centre + pdir * (BW_PLANET_R + alt)
		var vel: Vector3 = newp - bn.position
		bn.position = newp
		if vel.length() > 0.01:
			bn.look_at(newp + vel, pdir)
		var wing_l: Node3D = bn.get_meta("wing_l", null) as Node3D
		var wing_r: Node3D = bn.get_meta("wing_r", null) as Node3D
		if wing_l != null and wing_r != null:
			var flap_angle: float = deg_to_rad(12.0 - 54.0 * absf(sin(tt * float(fd["flap"]))))
			wing_l.rotation.y = flap_angle
			wing_r.rotation.y = -flap_angle
		else:
			bn.scale = Vector3(1.0 + 0.28 * sin(tt * float(fd["flap"])), 1.0, 1.0)

func _build_track() -> void:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in range(SAMPLES + 1):
		var s: float = (_cum[i] if i < _cum.size() else _len)
		var fr := _frame_at(s, 0.0)
		var right: Vector3 = fr[2]
		var c := _pos_at(s)
		var hw: float = _width_at(s)
		var l := c + right * hw
		var r := c - right * hw
		var v: float = float(i) / float(SAMPLES)
		st.set_uv(Vector2(0.0, v))
		st.add_vertex(l - _origin())
		st.set_uv(Vector2(1.0, v))
		st.add_vertex(r - _origin())
	for i in range(SAMPLES):
		var a := i * 2
		st.add_index(a); st.add_index(a + 1); st.add_index(a + 3)
		st.add_index(a); st.add_index(a + 3); st.add_index(a + 2)
	# l/r strip winding points down; flip the generated normals so the lit,
	# cull-disabled road has a correctly illuminated top face.
	st.generate_normals(true)
	var road := MeshInstance3D.new()
	road.mesh = st.commit()
	var rsh := Shader.new()
	if _theme() == "ocean":
		# sandy seabed track with drifting caustic light dapples + lane shimmer
		rsh.code = """shader_type spatial;
render_mode cull_disabled;
float h(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5); }
void fragment(){
	vec2 g = UV * vec2(9.0, 220.0);
	float grain = h(floor(g)) * 0.10;
	vec3 sand = vec3(0.68, 0.58, 0.38) - grain;   // deeper sand tone — no white blow-out
	float c1 = sin(UV.y * 90.0 + TIME * 1.3 + sin(UV.x * 12.0));
	float c2 = sin(UV.y * 55.0 - TIME * 0.9 + UV.x * 20.0);
	float caus = smoothstep(0.75, 1.0, c1 * c2);
	float edge = smoothstep(0.0, 0.12, UV.x) * (1.0 - smoothstep(0.88, 1.0, UV.x));
	ALBEDO = mix(vec3(0.28, 0.48, 0.52), sand, edge);
	EMISSION = vec3(0.45, 0.7, 0.75) * caus * 0.12;
	ROUGHNESS = 0.95;
}"""
	else:
		# Graphic painted-panel road, generated in the Mobile-safe shader. Bold
		# navy edge/seam ink gives the ribbon depth without a missing texture or
		# another sampled map in the phone's hot path.
		rsh.code = """shader_type spatial;
render_mode cull_disabled;
void fragment(){
	float b = fract(UV.y * 7.0);
	vec3 c;
	if(b<0.16) c=vec3(0.95,0.2,0.35);
	else if(b<0.33) c=vec3(1.0,0.6,0.2);
	else if(b<0.5) c=vec3(1.0,0.92,0.3);
	else if(b<0.66) c=vec3(0.3,0.85,0.45);
	else if(b<0.83) c=vec3(0.3,0.6,1.0);
	else c=vec3(0.65,0.4,0.95);
	float edge = smoothstep(0.015, 0.075, UV.x) * (1.0 - smoothstep(0.925, 0.985, UV.x));
	float seam_dist = min(b, 1.0-b);
	float seam = 1.0-smoothstep(0.0, 0.045, seam_dist);
	vec3 ink = vec3(0.12, 0.10, 0.28);
	vec3 shell = vec3(1.0, 0.93, 0.74);
	vec3 painted = mix(c, shell, seam * 0.34);
	ALBEDO = mix(ink, painted, edge);
	EMISSION = c * edge * (0.10 + 0.05*sin(TIME*2.0 + UV.y*40.0));
	ROUGHNESS = 0.72;
}"""
	var rmat := ShaderMaterial.new()
	rmat.shader = rsh
	road.material_override = rmat
	road.position = _origin()
	add_child(road)
	# glowing rails
	for sgn: float in [1.0, -1.0]:
		var rail := MeshInstance3D.new()
		var rst := SurfaceTool.new()
		rst.begin(Mesh.PRIMITIVE_TRIANGLES)
		for i in range(SAMPLES + 1):
			var s: float = (_cum[i] if i < _cum.size() else _len)
			var fr := _frame_at(s, 0.0)
			var right: Vector3 = fr[2]
			var rup: Vector3 = fr[3]
			var edge: Vector3 = _pos_at(s) - _origin() + right * (_width_at(s) * sgn)
			rst.add_vertex(edge)
			rst.add_vertex(edge + rup * 1.8)
		for i in range(SAMPLES):
			var a := i * 2
			rst.add_index(a); rst.add_index(a + 1); rst.add_index(a + 3)
			rst.add_index(a); rst.add_index(a + 3); rst.add_index(a + 2)
		rail.mesh = rst.commit()
		var em := StandardMaterial3D.new()
		em.albedo_color = Color(1.0, 1.0, 1.0)
		em.emission_enabled = true
		em.emission = (Color(0.35, 0.95, 0.6) if _theme() == "ocean" else Color(0.7, 0.9, 1.0))   # kelp-glow rails underwater
		em.emission_energy_multiplier = (0.7 if _theme() == "ocean" else 1.1)   # soft underwater; space rails were blooming the near road white at 2.0
		em.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		em.cull_mode = BaseMaterial3D.CULL_DISABLED
		rail.material_override = em
		rail.position = _origin()
		add_child(rail)
	_build_finish()
	if bool(_cv("shortcut", true)):
		_build_shortcut()
	if _theme() == "ocean":
		_build_ocean_props()
	else:
		# floating crystals (rainbow theme)
		var deco_count: int = 4 if _speedy() else 7
		for si2 in range(deco_count):
			var su: float = float(si2) / float(deco_count)
			var pf := _frame_at(su * _len, 0.0)
			var sp: Vector3 = pf[0]
			var rgt: Vector3 = pf[2]
			var side: float = 1.0 if si2 % 2 == 0 else -1.0
			var deco := MeshInstance3D.new()
			var dmsh := BoxMesh.new()
			dmsh.size = Vector3(7, 7, 7)
			deco.mesh = dmsh
			var dcm := StandardMaterial3D.new()
			dcm.albedo_color = Color.from_hsv(su, 0.55, 1.0)
			dcm.emission_enabled = true
			dcm.emission = dcm.albedo_color
			dcm.emission_energy_multiplier = 0.6
			deco.material_override = dcm
			deco.position = sp + rgt * ((_rhalf() + 16.0) * side) + Vector3(0, 4.0 + sin(su * TAU) * 8.0, 0)
			deco.rotation = Vector3(su * 6.0, su * 4.0, su * 2.0)
			add_child(deco)

const OCEAN_PROPS := [
	"Coral", "SeaWeed", "Coral1", "Rock3", "Coral2", "SeaWeed1", "FanShell",
	"Coral3", "Rock7", "Coral4", "SeaWeed2", "SpiralShell", "Coral5", "Rock9",
	"Coral6", "SandDollar",
]
const OCEAN_PROP_GEN2 := {
	"Coral": "coral", "Coral1": "coral1", "Coral2": "coral2",
	"Coral3": "coral3", "Coral4": "coral4", "Coral5": "coral5",
	"Coral6": "coral6", "Rock3": "rock3", "Rock7": "rock1",
	"Rock9": "rock3", "FanShell": "fanshell", "SpiralShell": "spiralshell",
	"SandDollar": "sanddollar",
}
const OCEAN_FISH_GEN2 := ["clownfish", "turtle", "stingray", "dolphin"]
var _deco_fish: Array = []

func _gen2_instance(name: String) -> Node3D:
	var path := "res://assets/props/gen2/%s.glb" % name
	if not ResourceLoader.exists(path):
		return null
	var scene: PackedScene = load(path)
	if scene == null:
		return null
	var instance := scene.instantiate() as Node3D
	if instance == null:
		return null
	instance.set_meta("gen2", true)
	return instance

func _gen2_card(name: String, target_width: float) -> Node3D:
	var path := "res://assets/props/gen2/%s.png" % name
	if not ResourceLoader.exists(path):
		return null
	var tex: Texture2D = load(path)
	var card := Sprite3D.new()
	card.texture = tex
	card.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	card.pixel_size = target_width / maxf(float(tex.get_width()), 1.0)
	var holder := Node3D.new()
	holder.add_child(card)
	holder.set_meta("fitted", true)
	return holder

func _gen2_grass_card(index: int, target_height: float) -> Node3D:
	var names := ["seagrass", "grasstuft", "kelp"]
	var name: String = names[index % names.size()]
	var path := "res://assets/props/gen2/%s.png" % name
	if not ResourceLoader.exists(path):
		return null
	var tex: Texture2D = load(path)
	var holder := Node3D.new()
	var aspect: float = float(tex.get_width()) / maxf(float(tex.get_height()), 1.0)
	for turn in [0.0, PI * 0.5]:
		var card := MeshInstance3D.new()
		var quad := QuadMesh.new()
		quad.size = Vector2(target_height * aspect, target_height)
		card.mesh = quad
		var mat := StandardMaterial3D.new()
		mat.albedo_texture = tex
		mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
		mat.alpha_scissor_threshold = 0.35
		mat.cull_mode = BaseMaterial3D.CULL_DISABLED
		mat.roughness = 1.0
		card.material_override = mat
		card.position.y = target_height * 0.5
		card.rotation.y = turn
		holder.add_child(card)
	holder.set_meta("fitted", true)
	return holder

func _play_first_anim(root: Node) -> void:
	var stack: Array = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is AnimationPlayer:
			var ap := n as AnimationPlayer
			var clips := ap.get_animation_list()
			if clips.size() > 0:
				var cname: String = clips[0]
				var anim := ap.get_animation(cname)
				if anim != null:
					anim.loop_mode = Animation.LOOP_LINEAR
				ap.play(cname)
			return
		for c in n.get_children():
			stack.append(c)

func _build_ocean_props() -> void:
	# seabed dressing: the game's own corals / seaweed / rocks / shells on little
	# sand mounds along both sides of the track
	for i in range(OCEAN_PROPS.size()):
		var su: float = float(i) / float(OCEAN_PROPS.size())
		# The first bend is the vehicle showroom. Dressing there sat directly
		# between its side-on camera and the podiums; leave that sightline clear.
		if su < 0.08 or (_speedy() and i % 2 == 1):
			continue
		var prop_name: String = OCEAN_PROPS[i]
		var prop: Node3D = null
		if prop_name.begins_with("SeaWeed"):
			prop = _gen2_grass_card(i, 1.0)
		elif OCEAN_PROP_GEN2.has(prop_name):
			prop = _gen2_instance(String(OCEAN_PROP_GEN2[prop_name]))
		else:
			var path: String = "res://assets/aquatic/%s.glb" % prop_name
			if ResourceLoader.exists(path):
				prop = (load(path) as PackedScene).instantiate()
		if prop == null:
			continue
		var pf := _frame_at(su * _len, 0.0)
		var sp: Vector3 = pf[0]
		var rgt: Vector3 = pf[2]
		var side: float = 1.0 if i % 2 == 0 else -1.0
		var base: Vector3 = sp + rgt * ((_width_at(su * _len) + 15.0 + fposmod(float(i) * 3.7, 8.0)) * side)
		if _ground_mode() == "terrain":
			base.y = _terrain_y(base.x, base.z)   # props stand on the real floor beside the track
		var mound := MeshInstance3D.new()
		var mm := CylinderMesh.new()
		mm.top_radius = 4.0
		mm.bottom_radius = 5.5
		mm.height = 1.2
		mm.radial_segments = 20
		mound.mesh = mm
		var smat := StandardMaterial3D.new()
		smat.albedo_color = Color(0.82, 0.72, 0.5)
		smat.roughness = 1.0
		mound.material_override = smat
		mound.position = base + Vector3(0, -0.6, 0)
		add_child(mound)
		var target_size: float = 4.0 + fposmod(float(i) * 1.9, 3.0)
		if prop.has_meta("fitted"):
			prop.scale = Vector3.ONE * target_size
		else:
			_bw_fit(prop, target_size)
		prop.position = base
		prop.rotation = Vector3(0, float(i) * 2.4, 0)
		add_child(prop)
	# a few animated fish cruising beside the course
	for i in range(OCEAN_FISH_GEN2.size()):
		if _speedy() and i % 2 == 1:
			continue
		var fish: Node3D = null
		fish = _gen2_instance(OCEAN_FISH_GEN2[i])
		if fish == null:
			continue
		var su2: float = (float(i) + 0.5) / float(OCEAN_FISH_GEN2.size())
		var pf2 := _frame_at(su2 * _len, 0.0)
		var side2: float = 1.0 if i % 2 == 0 else -1.0
		_bw_fit(fish, 4.4)
		var fbase: Vector3 = (pf2[0] as Vector3) + (pf2[2] as Vector3) * ((_rhalf() + 14.0) * side2) + Vector3(0, 6.0, 0)
		fish.position = fbase
		add_child(fish)
		_play_first_anim(fish)
		_deco_fish.append({"node": fish, "base": fbase, "ph": float(i) * 1.7})

func _build_finish() -> void:
	var sf := _frame_at(0.0, 0.0)
	var c0: Vector3 = sf[0]
	var ffwd: Vector3 = sf[1]
	var fright: Vector3 = sf[2]
	var line := MeshInstance3D.new()
	var lpm := PlaneMesh.new()
	lpm.size = Vector2(_rhalf() * 2.0, 4.0)
	line.mesh = lpm
	var lsh := Shader.new()
	lsh.code = """shader_type spatial;
render_mode unshaded, cull_disabled;
void fragment(){
	vec2 g = floor(UV * vec2(10.0, 2.0));
		float chk = mod(g.x + g.y, 2.0);
		vec3 navy = vec3(0.18, 0.20, 0.52);
		vec3 shell = vec3(1.0, 0.91, 0.70);
		ALBEDO = mix(navy, shell, chk);
}"""
	var lmat := ShaderMaterial.new()
	lmat.shader = lsh
	line.material_override = lmat
	line.transform = Transform3D(Basis(fright, Vector3.UP, ffwd).orthonormalized(), c0 + Vector3(0, 0.2, 0))
	add_child(line)
	for psgn: float in [1.0, -1.0]:
		var post := MeshInstance3D.new()
		var pbm := BoxMesh.new()
		pbm.size = Vector3(1.4, 15.0, 1.4)
		post.mesh = pbm
		var pmat := StandardMaterial3D.new()
		pmat.albedo_color = Color(0.30, 0.76, 0.78) if psgn > 0.0 else Color(0.68, 0.52, 0.84)
		pmat.roughness = 0.82
		post.material_override = pmat
		post.position = c0 + fright * (_rhalf() * psgn) + Vector3(0, 7.5, 0)
		add_child(post)
	var dome := MeshInstance3D.new()
	var dtm := TorusMesh.new()
	dtm.inner_radius = _rhalf() + 1.0
	dtm.outer_radius = _rhalf() + 4.0
	dtm.rings = 40
	dtm.ring_segments = 18
	dome.mesh = dtm
	var dsh := Shader.new()
	dsh.code = """shader_type spatial;
render_mode unshaded, cull_disabled;
void fragment(){
	float b = fract(UV.y);
	vec3 c;
	if(b<0.16) c=vec3(0.95,0.2,0.35);
	else if(b<0.33) c=vec3(1.0,0.6,0.2);
	else if(b<0.5) c=vec3(1.0,0.92,0.3);
	else if(b<0.66) c=vec3(0.3,0.85,0.45);
	else if(b<0.83) c=vec3(0.3,0.6,1.0);
	else c=vec3(0.65,0.4,0.95);
	ALBEDO=c; EMISSION=c*0.6;
}"""
	var dmat := ShaderMaterial.new()
	dmat.shader = dsh
	dome.material_override = dmat
	dome.transform = Transform3D(Basis(fright, ffwd, Vector3.UP).orthonormalized(), c0 + Vector3(0, 1.0, 0))
	add_child(dome)
	var finish_banner := Sprite3D.new()
	finish_banner.texture = load("res://assets/kart/finish_banner.png")
	finish_banner.pixel_size = 0.025
	finish_banner.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	finish_banner.position = c0 + Vector3(0, 11.0, 0)
	add_child(finish_banner)

func _build_shortcut() -> void:
	var gate_fr := _frame_at(SHORTCUT_FROM_U * _len, 0.0)
	var gate_pos: Vector3 = (gate_fr[0] as Vector3) + (gate_fr[2] as Vector3) * (_rhalf() * 0.78)
	var ring := MeshInstance3D.new()
	var tm := TorusMesh.new()
	tm.inner_radius = 3.5
	tm.outer_radius = 5.0
	ring.mesh = tm
	var gmat := StandardMaterial3D.new()
	gmat.albedo_color = Color(0.7, 1.0, 0.9)
	gmat.emission_enabled = true
	gmat.emission = Color(0.4, 1.0, 0.7)
	gmat.emission_energy_multiplier = 1.6
	gmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	ring.material_override = gmat
	ring.position = gate_pos + Vector3(0, 3.0, 0)
	ring.rotation = Vector3(deg_to_rad(90), 0, 0)
	ring.visible = not _rev
	add_child(ring)
	set_meta("gate_pos", gate_pos)

func _build_strips() -> void:
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode unshaded, cull_disabled;
void fragment(){
	float band = fract(UV.y * 5.0 - TIME * 2.5 + abs(UV.x - 0.5));
	float chev = smoothstep(0.78, 1.0, band);
	vec3 c = vec3(0.3, 0.9, 1.0);
	ALBEDO = c;
	EMISSION = c * (0.4 + chev * 1.6);
	ALPHA = 0.9;
}"""
	var table: Array = _cv("strips", STRIPS)
	for sd in table:
		var s0: float = float(sd["u"]) * _len
		var fr := _frame_at(s0 + float(sd["len"]) * 0.5, float(sd["lat"]))
		var pos: Vector3 = fr[0]
		var fwd: Vector3 = fr[1]
		var right: Vector3 = fr[2]
		var up: Vector3 = fr[3]
		var pm := PlaneMesh.new()
		pm.size = Vector2(float(sd["hw"]) * 2.0, float(sd["len"]))
		var mi := MeshInstance3D.new()
		mi.mesh = pm
		var mat := ShaderMaterial.new()
		mat.shader = sh
		mi.material_override = mat
		mi.transform = Transform3D(Basis(right, up, -fwd).orthonormalized(), pos + up * 0.18)
		add_child(mi)
		_strip_data.append({"pos": pos + up, "len": float(sd["len"])})

func _build_pickups() -> void:
	var table: Array = _cv("pickups", PICKUPS)
	for pd in table:
		var s0: float = float(pd["u"]) * _len
		var fr := _frame_at(s0, float(pd["lat"]))
		var pos: Vector3 = fr[0]
		var holder := Node3D.new()
		holder.position = pos + Vector3(0, 2.6, 0)
		var kind := String(pd["kind"])
		var rlab: Label3D = null
		if kind == "shell":
			var sm: Node3D = null
			if ResourceLoader.exists("res://assets/props/gen2/%s.glb" % SHELL_GEN2):
				sm = _gen2_instance(SHELL_GEN2)
			elif ResourceLoader.exists(SHELL_GLB):
				sm = (load(SHELL_GLB) as PackedScene).instantiate()
			if sm == null:
				continue
			sm.scale = Vector3.ONE * 2.4
			holder.add_child(sm)
			pass   # shell pickups glow via emission; no per-pickup realtime light
		elif kind == "bubble":
			# zoom bubble: translucent glowing sphere — drive through, POP, instant zip
			var bub := MeshInstance3D.new()
			var bs := SphereMesh.new()
			bs.radius = 2.0
			bs.height = 4.0
			bub.mesh = bs
			var bm := StandardMaterial3D.new()
			bm.albedo_color = Color(0.5, 0.95, 1.0, 0.4)
			bm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			bm.emission_enabled = true
			bm.emission = Color(0.4, 0.9, 1.0)
			bm.emission_energy_multiplier = 1.2
			bub.material_override = bm
			holder.add_child(bub)
			if not _speedy():
				var gl3 := OmniLight3D.new()
				gl3.light_color = Color(0.5, 0.95, 1.0)
				gl3.light_energy = 2.0
				gl3.omni_range = 9.0
				holder.add_child(gl3)
		else:
			var lab := Label3D.new()
			lab.text = "★"
			lab.font_size = 180 if kind == "star" else 220
			lab.pixel_size = 0.03
			lab.modulate = Color(1.0, 0.9, 0.3)
			lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			holder.add_child(lab)
			if kind == "rainbow":
				rlab = lab   # hue-cycled every frame — the jackpot pickup
			if not _speedy() and (kind == "star" or kind == "rainbow"):   # Speedy uses emission, no pickup realtime lights
				var gl2 := OmniLight3D.new()
				gl2.light_color = lab.modulate
				gl2.light_energy = 2.4
				gl2.omni_range = 10.0
				holder.add_child(gl2)
		add_child(holder)
		_pickups_live.append({"node": holder, "s": s0, "lat": float(pd["lat"]), "kind": kind, "cool": 0.0, "rlab": rlab})

func _build_ramps() -> void:
	# golden glowing wedges on the racing line: drive one, FLY, land with a
	# free zip — the auto-trick every one-finger mobile racer is built on
	var table: Array = _cv("ramps", RAMPS)
	for rd in table:
		var s0: float = float(rd["u"]) * _len
		var fr := _frame_at(s0, float(rd["lat"]))
		var pos: Vector3 = fr[0]
		var fwd: Vector3 = fr[1]
		var right: Vector3 = fr[2]
		var up: Vector3 = fr[3]
		var wedge := MeshInstance3D.new()
		var pm := PrismMesh.new()
		pm.size = Vector3(9.0, 2.2, 6.0)
		wedge.mesh = pm
		var gm := StandardMaterial3D.new()
		gm.albedo_color = Color(1.0, 0.85, 0.3)
		gm.emission_enabled = true
		gm.emission = Color(1.0, 0.8, 0.25)
		gm.emission_energy_multiplier = 0.8
		wedge.material_override = gm
		# tent-shaped pad with the slope aligned along the road — reads as a
		# jump bump from BOTH directions, so reverse laps get it for free. Follow
		# the full banked frame instead of floating horizontally through corners.
		wedge.transform = Transform3D(Basis(fwd, up, right).orthonormalized(), pos + up * 1.1)
		add_child(wedge)
		var ribbon := Sprite3D.new()
		ribbon.texture = load("res://assets/kart/boost_ribbon.png")
		ribbon.pixel_size = 0.012
		ribbon.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		ribbon.position = pos + up * 5.2
		add_child(ribbon)
		_ramp_data.append({"pos": pos})

func _check_ramps() -> void:
	for rd in _ramp_data:
		for k in _karts:
			if float(k.get("air_t", 0.0)) > 0.0:
				continue
			if (k["node"] as Node3D).position.distance_to(rd["pos"]) < 6.0:
				k["air_t"] = AIR_DUR
				if bool(k["is_player"]):
					_chime(1.15)
					_flash_big("WHEEE!")

# ------------------------------------------------------------ hazards
var _hazards_live: Array = []

func _hazard_table() -> Array:
	return _cv("hazards", HAZARDS_OCEAN if _theme() == "ocean" else HAZARDS_RAINBOW)

func _build_hazards() -> void:
	for hd in _hazard_table():
		var s0: float = float(hd["u"]) * _len
		var w: float = _width_at(s0)
		var kind := String(hd["kind"])
		var h := {"kind": kind, "s": s0, "w": w, "ph": s0 * 0.13, "lat": 0.0}
		var holder := Node3D.new()
		add_child(holder)
		h["node"] = holder
		match kind:
			"crab":
				var cb: Node3D = null
				if ResourceLoader.exists("res://assets/props/gen2/crab.glb"):
					cb = _gen2_instance("crab")
				elif ResourceLoader.exists("res://assets/aquatic/Crab.glb"):
					cb = (load("res://assets/aquatic/Crab.glb") as PackedScene).instantiate()
				if cb != null:
					holder.add_child(cb)
					_bw_fit(cb, 3.4)
				else:
					var q := MeshInstance3D.new()
					var qm := SphereMesh.new()
					qm.radius = 1.6
					qm.height = 2.2
					q.mesh = qm
					var qmat := StandardMaterial3D.new()
					qmat.albedo_color = Color(0.95, 0.4, 0.3)
					q.material_override = qmat
					holder.add_child(q)
			"kelp":
				# a forest patch ACROSS the road — drive through it and the
				# fronds drag you (turbo powers through: that's the counterplay)
				var base: Vector3 = _frame_at(s0, 0.0)[0]
				holder.position = base
				for i in range(3):
					var sw: Node3D = null
					if ResourceLoader.exists("res://assets/props/gen2/seagrass.png"):
						sw = _gen2_grass_card(i, 5.0)
					else:
						var kp: String = "res://assets/aquatic/SeaWeed%s.glb" % ["", "1", "2"][i]
						if ResourceLoader.exists(kp):
							sw = (load(kp) as PackedScene).instantiate()
					if sw == null:
						continue
					var kh := Node3D.new()
					holder.add_child(kh)
					kh.add_child(sw)
					if not sw.has_meta("fitted"):
						_bw_fit(sw, 5.0)
					var fr := _frame_at(s0 + float(i - 1) * 4.0, (float(i) - 1.0) * w * 0.55)
					kh.position = (fr[0] as Vector3) - base
			"geyser":
				# bubbly vent on a rhythm: quiet = safe, erupting = free JUMP —
				# the hazard a kid learns to chase, not fear
				var mound := MeshInstance3D.new()
				var mm := CylinderMesh.new()
				mm.top_radius = 2.2
				mm.bottom_radius = 3.4
				mm.height = 1.0
				mound.mesh = mm
				var smat := StandardMaterial3D.new()
				smat.albedo_color = Color(0.75, 0.65, 0.45)
				smat.roughness = 1.0
				mound.material_override = smat
				holder.add_child(mound)
				var bub := CPUParticles3D.new()
				bub.emitting = false
				bub.amount = 12 if _speedy() else 26
				bub.lifetime = 0.8
				bub.direction = Vector3.UP
				bub.spread = 8.0
				bub.initial_velocity_min = 14.0
				bub.initial_velocity_max = 20.0
				bub.gravity = Vector3.ZERO
				bub.scale_amount_min = 0.2
				bub.scale_amount_max = 0.55
				var bm := SphereMesh.new()
				bm.radius = 0.45
				bm.height = 0.9
				bub.mesh = bm
				var bmat := StandardMaterial3D.new()
				bmat.albedo_color = Color(0.7, 0.92, 1.0, 0.55)
				bmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
				bmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
				bub.mesh.material = bmat
				holder.add_child(bub)
				h["bub"] = bub
			"comet":
				# a grumpy METEOR — dark craggy rock with a fiery tail. Rocks
				# bonk; stars are treats (never reuse the pickup vocabulary)
				var rk: Node3D = null
				if ResourceLoader.exists("res://assets/props/gen2/rock3.glb"):
					rk = _gen2_instance("rock3")
				elif ResourceLoader.exists("res://assets/aquatic/Rock3.glb"):
					rk = (load("res://assets/aquatic/Rock3.glb") as PackedScene).instantiate()
				if rk != null:
					holder.add_child(rk)
					_bw_fit(rk, 3.2)
					_bw_tint(rk, Color(0.32, 0.26, 0.44), 0.3)   # dark slate-plum
				else:
					var rq := MeshInstance3D.new()
					var rqm := SphereMesh.new()
					rqm.radius = 1.5
					rqm.height = 3.0
					rq.mesh = rqm
					var rqmat := StandardMaterial3D.new()
					rqmat.albedo_color = Color(0.3, 0.25, 0.4)
					rq.material_override = rqmat
					holder.add_child(rq)
				var tail := CPUParticles3D.new()
				tail.amount = 8 if _speedy() else 18
				tail.lifetime = 0.45
				tail.local_coords = false   # embers hang in space behind the sweep
				tail.direction = Vector3(0, 0.4, 0)
				tail.spread = 30.0
				tail.initial_velocity_min = 1.0
				tail.initial_velocity_max = 3.0
				tail.gravity = Vector3.ZERO
				tail.scale_amount_min = 0.14
				tail.scale_amount_max = 0.4
				var tbm := BoxMesh.new()
				tbm.size = Vector3(0.3, 0.3, 0.3)
				tail.mesh = tbm
				var tmat := StandardMaterial3D.new()
				tmat.albedo_color = Color(1.0, 0.55, 0.2)
				tmat.emission_enabled = true
				tmat.emission = Color(1.0, 0.45, 0.1)
				tmat.emission_energy_multiplier = 1.2
				tmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
				tail.mesh.material = tmat
				holder.add_child(tail)
				h["side"] = 1.0 if int(s0) % 2 == 0 else -1.0
			"pendulum":
				# a swinging SPIKE BALL — blunt cartoon spikes read "don't
				# touch" in any language a 4yo speaks
				var ball := MeshInstance3D.new()
				var blm := SphereMesh.new()
				blm.radius = 1.5
				blm.height = 3.0
				ball.mesh = blm
				var bmat2 := StandardMaterial3D.new()
				bmat2.albedo_color = Color(0.42, 0.26, 0.5)   # deep plum
				bmat2.emission_enabled = true
				bmat2.emission = Color(0.75, 0.2, 0.3)
				bmat2.emission_energy_multiplier = 0.35
				ball.material_override = bmat2
				holder.add_child(ball)
				for i in range(8):
					var a: float = float(i) * TAU / 8.0
					var tilt: float = 0.55 if i % 2 == 0 else -0.55
					var d := Vector3(cos(a) * cos(tilt), sin(tilt), sin(a) * cos(tilt)).normalized()
					var spk := MeshInstance3D.new()
					var cm2 := CylinderMesh.new()
					cm2.top_radius = 0.0
					cm2.bottom_radius = 0.42
					cm2.height = 1.1
					spk.mesh = cm2
					spk.material_override = bmat2
					spk.position = d * 1.7
					var any := Vector3.UP if absf(d.dot(Vector3.UP)) < 0.95 else Vector3.RIGHT
					var tx := any.cross(d).normalized()
					spk.transform.basis = Basis(tx, d, tx.cross(d)).orthonormalized()
					holder.add_child(spk)
			"whirl":
				# a spinning sand-whirlpool set to one side of the road — it
				# TUGS you toward its middle; steering (or a turbo) escapes
				h["lat"] = w * 0.35 * (1.0 if int(s0) % 2 == 0 else -1.0)
				var frw := _frame_at(s0, float(h["lat"]))
				holder.position = (frw[0] as Vector3) + Vector3(0, 0.15, 0)
				var disc := MeshInstance3D.new()
				var dm := PlaneMesh.new()
				dm.size = Vector2(11.0, 11.0)
				disc.mesh = dm
				var wsh := Shader.new()
				wsh.code = """shader_type spatial;
render_mode unshaded, cull_disabled;
void fragment(){
	vec2 c = UV - 0.5;
	float r = length(c);
	float ang = atan(c.y, c.x);
	float sp = sin(ang * 3.0 + r * 28.0 - TIME * 4.0);
	float m = 1.0 - smoothstep(0.46, 0.5, r);
	ALBEDO = mix(vec3(0.14, 0.30, 0.36), vec3(0.5, 0.75, 0.8), step(0.0, sp));
	ALPHA = m * 0.85;
}"""
				var wmat := ShaderMaterial.new()
				wmat.shader = wsh
				disc.material_override = wmat
				holder.add_child(disc)
			"jelly":
				# a wobbly jelly-moon dome parked on the road: BOING — a big
				# bouncy shove, deliberately distinct from the bonk-spin
				h["lat"] = w * 0.4 * (1.0 if int(s0) % 2 == 0 else -1.0)
				var frj := _frame_at(s0, float(h["lat"]))
				holder.position = frj[0] as Vector3
				var dome := MeshInstance3D.new()
				var dsm := SphereMesh.new()
				dsm.radius = 2.6
				dsm.height = 2.6
				dsm.is_hemisphere = true
				dome.mesh = dsm
				var jmat := StandardMaterial3D.new()
				jmat.albedo_color = Color(0.95, 0.5, 0.8, 0.6)
				jmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
				jmat.emission_enabled = true
				jmat.emission = Color(0.9, 0.4, 0.75)
				jmat.emission_energy_multiplier = 0.3
				dome.material_override = jmat
				holder.add_child(dome)
			"cloud":
				for i in range(3):
					var cl := MeshInstance3D.new()
					var cm := SphereMesh.new()
					cm.radius = [2.6, 2.0, 1.7][i]
					cm.height = cm.radius * 2.0
					cl.mesh = cm
					var cmat := StandardMaterial3D.new()
					cmat.albedo_color = Color(0.7, 0.6, 0.95, 0.5)
					cmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
					cmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
					cl.material_override = cmat
					cl.position = Vector3([-2.2, 1.6, 0.2][i], [0.6, 0.4, 1.8][i], [0.4, -1.2, 0.9][i])
					holder.add_child(cl)
				# the "z Z z" makes it read SLEEPY, not decorative
				var zz := Label3D.new()
				zz.text = "z Z z"
				zz.font_size = 90
				zz.pixel_size = 0.03
				zz.outline_size = 12
				zz.modulate = Color(0.8, 0.75, 1.0)
				zz.billboard = BaseMaterial3D.BILLBOARD_ENABLED
				zz.position = Vector3(0, 3.4, 0)
				holder.add_child(zz)
				h["zz"] = zz
		_hazards_live.append(h)

func _hazard_bonk(k: Dictionary, slow: float, dir: float) -> void:
	# soft and silly, never punishing: a slow + a shove + a full spin
	if float(k.get("haz_cool", 0.0)) > 0.0 or float(k.get("air_t", 0.0)) > 0.0:
		return
	k["haz_cool"] = 1.5
	k["speed"] = float(k["speed"]) * slow
	k["latv"] = float(k["latv"]) + dir * 16.0
	k["squash"] = 0.3
	k["hop"] = 0.22
	k["spin_t"] = 0.6
	_drift_cancel(k)
	if bool(k["is_player"]):
		_shake = maxf(_shake, 0.3)
		if _thunk_cool <= 0.0:
			_chime(0.45)
			_thunk_cool = 0.35
		if _main != null and _main.has_method("_say"):
			_main._say("roshan", "bump", 7.0)

func _tick_hazards(delta: float) -> void:
	var tt: float = Time.get_ticks_msec() / 1000.0
	var racing: bool = _state == "race"
	for h in _hazards_live:
		var kind := String(h["kind"])
		var s0: float = float(h["s"])
		var w: float = float(h["w"])
		var node: Node3D = h["node"]
		match kind:
			"crab":
				h["lat"] = sin(tt * 0.55 + float(h["ph"])) * (w - 2.5)
				var fr := _frame_at(s0, float(h["lat"]))
				node.position = (fr[0] as Vector3) + Vector3(0, 0.3 + absf(sin(tt * 6.0)) * 0.3, 0)
				node.rotation.y = tt * 0.8
				if racing:
					for k in _karts:
						if (k["node"] as Node3D).position.distance_to(node.position) < 3.4:
							_hazard_bonk(k, 0.75, signf(float(k["lat"]) - float(h["lat"])))
			"pendulum":
				h["lat"] = sin(tt * 1.1 + float(h["ph"])) * (w - 2.0)
				var fr2 := _frame_at(s0, float(h["lat"]))
				node.position = (fr2[0] as Vector3) + Vector3(0, 1.6, 0)
				if racing:
					for k in _karts:
						if (k["node"] as Node3D).position.distance_to(node.position) < 3.6:
							_hazard_bonk(k, 0.75, signf(float(k["lat"]) - float(h["lat"])))
			"geyser":
				var cyc: float = fposmod(tt + float(h["ph"]), 4.2)
				var erupting: bool = cyc < 1.4
				var frg := _frame_at(s0, 0.0)
				node.position = frg[0] as Vector3
				if h.has("bub"):
					(h["bub"] as CPUParticles3D).emitting = erupting
				# pre-cue: the mound quivers half a second before it blows
				node.scale = Vector3.ONE * (1.0 + (0.18 * sin(tt * 30.0) if cyc > 3.7 else 0.0))
				if racing and erupting:
					for k in _karts:
						if float(k.get("air_t", 0.0)) > 0.0:
							continue
						if (k["node"] as Node3D).position.distance_to(node.position) < 4.5:
							k["air_t"] = AIR_DUR   # tossed sky-high — the fun kind of hazard
							if bool(k["is_player"]):
								_chime(1.15)
								_flash_big("WHEEE!")
			"comet":
				# the meteor sweeps the road on a 5s rhythm; first it hovers
				# and QUIVERS at the entry edge — the telegraph a 4yo can read
				var ccyc: float = fposmod(tt + float(h["ph"]), 5.0)
				var side: float = float(h["side"])
				if ccyc >= 3.8:
					var p: float = (ccyc - 3.8) / 1.2
					h["lat"] = lerpf(side * (w + 9.0), -side * (w + 9.0), p)
					var frx := _frame_at(s0, float(h["lat"]))
					node.position = (frx[0] as Vector3) + Vector3(0, 1.5, 0)
					node.visible = true
					node.scale = Vector3.ONE
					node.rotation.y = tt * 5.0   # tumbling rock
					if racing:
						for k in _karts:
							if (k["node"] as Node3D).position.distance_to(node.position) < 3.6:
								_hazard_bonk(k, 0.7, -side)
				elif ccyc >= 3.1:
					h["lat"] = side * (w + 9.0)
					var fre := _frame_at(s0, float(h["lat"]))
					node.position = (fre[0] as Vector3) + Vector3(0, 1.5, 0)
					node.visible = true
					node.scale = Vector3.ONE * (1.0 + 0.22 * absf(sin(tt * 12.0)))
				else:
					node.visible = false
			"whirl":
				# fixed position (set at build); the pull is the hazard
				if racing:
					for k in _karts:
						if float(k.get("air_t", 0.0)) > 0.0:
							continue
						if (k["node"] as Node3D).position.distance_to(node.position) < 6.5:
							# 6 u/s tug toward the swirl — steering (22-30 u/s)
							# always wins, so it pesters rather than traps
							_apply_lat(k, float(k["lat"]) + signf(float(h["lat"]) - float(k["lat"])) * 6.0 * delta)
							if float(k["boost_t"]) <= 0.0:
								k["speed"] = maxf(float(k["speed"]) * (1.0 - 0.9 * delta), _vmax * 0.55)
			"jelly":
				# wobble idle; BOING on contact — a big bouncy shove, no spin
				var kick: float = float(h.get("kick", 0.0))
				if kick > 0.0:
					h["kick"] = maxf(0.0, kick - delta)
				var wob: float = 0.06 + kick * 0.5
				node.scale = Vector3(1.0 + wob * sin(tt * 6.0), 1.0 - wob * sin(tt * 6.0), 1.0 + wob * cos(tt * 6.0))
				if racing:
					for k in _karts:
						if float(k.get("haz_cool", 0.0)) > 0.0 or float(k.get("air_t", 0.0)) > 0.0:
							continue
						if (k["node"] as Node3D).position.distance_to(node.position) < 3.9:
							k["haz_cool"] = 1.2
							k["speed"] = float(k["speed"]) * 0.55
							k["latv"] = signf(float(k["lat"]) - float(h["lat"])) * 34.0
							k["hop"] = 0.3
							k["squash"] = 0.35
							h["kick"] = 0.5
							if bool(k["is_player"]):
								_shake = maxf(_shake, 0.3)
								_chime(1.6)   # BOING, not thunk
			"kelp", "cloud":
				if kind == "cloud":
					h["lat"] = sin(tt * 0.35 + float(h["ph"])) * w * 0.55
					var frc := _frame_at(s0, float(h["lat"]))
					node.position = (frc[0] as Vector3) + Vector3(0, 1.2, 0)
					if h.has("zz"):
						(h["zz"] as Label3D).position.y = 3.4 + sin(tt * 2.0) * 0.4
				if racing:
					var rad: float = 7.5 if kind == "kelp" else 5.5
					for k in _karts:
						if (k["node"] as Node3D).position.distance_to(node.position) < rad:
							# drag, not a stop — and a burning turbo powers through
							if float(k["boost_t"]) <= 0.0:
								k["speed"] = maxf(float(k["speed"]) * (1.0 - 1.5 * delta), _vmax * 0.5)

func _build_pearls() -> void:
	var rows: Array = _cv("pearl_rows", PEARL_ROWS)
	var pearl_mesh := SphereMesh.new()
	pearl_mesh.radius = 0.9
	pearl_mesh.height = 1.8
	var pearl_mats: Array = []
	var hue_count: int = 3 if _speedy() else 6
	for i in range(hue_count):
		var shared_mat := StandardMaterial3D.new()
		shared_mat.albedo_color = Color.from_hsv(float(i) / float(hue_count), 0.4, 1.0)
		shared_mat.emission_enabled = true
		shared_mat.emission = shared_mat.albedo_color
		shared_mat.emission_energy_multiplier = 0.8 if _speedy() else 1.0
		shared_mat.metallic = 0.6
		shared_mat.roughness = 0.2
		pearl_mats.append(shared_mat)
	for row in rows:
		var s0: float = float(row["u"]) * _len
		for j in range(int(row["n"])):
			var s := s0 + float(j) * 6.0
			var fr := _frame_at(s, float(row["lat"]))
			var p := MeshInstance3D.new()
			p.mesh = pearl_mesh
			var hue_i: int = clampi(int(floor(fposmod(s / _len, 1.0) * float(hue_count))), 0, hue_count - 1)
			p.material_override = pearl_mats[hue_i]
			p.position = (fr[0] as Vector3) + Vector3(0, 2.0, 0)
			add_child(p)
			_pearls_live.append({"node": p, "got": false})

# ------------------------------------------------------------ paint jobs
var _rainbow_mats: Array = []   # hue-cycled from _process — renderer-proof rainbow paint

func _rainbow_orb_mat() -> StandardMaterial3D:
	# swatch orb for the RAINBOW option (animated with the same list)
	var m := StandardMaterial3D.new()
	m.albedo_color = Color(1.0, 0.4, 0.4)
	m.emission_enabled = true
	m.emission = m.albedo_color
	m.emission_energy_multiplier = 0.5
	_rainbow_mats.append(m)
	return m

func _apply_paint(root: Node, paint: Dictionary) -> void:
	# repaint every mesh surface; originals cached on the node so repainting the
	# live preview never compounds tints
	var stack: Array = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		if not mi.has_meta("orig_mats"):
			var orig: Array = []
			for si in range(mi.mesh.get_surface_count()):
				orig.append(mi.get_active_material(si))
			mi.set_meta("orig_mats", orig)
		var origs: Array = mi.get_meta("orig_mats")
		for si in range(mi.mesh.get_surface_count()):
			if bool(paint.get("rainbow", false)):
				# rainbow = plain StandardMaterial3D hue-cycled from _process — no custom
				# shader, so it can never fail/vanish on the Mobile renderer
				var src0: Material = origs[si] if si < origs.size() else null
				var rm: BaseMaterial3D = (src0.duplicate() if src0 is BaseMaterial3D else StandardMaterial3D.new())
				rm.emission_enabled = true
				_rainbow_mats.append(rm)
				mi.set_surface_override_material(si, rm)
			elif paint.get("col") == null:
				var stock_src: Material = origs[si] if si < origs.size() else null
				var stock: BaseMaterial3D = (stock_src.duplicate() if stock_src is BaseMaterial3D else StandardMaterial3D.new())
				stock.roughness = 1.0
				stock.metallic = 0.0
				stock.metallic_specular = 0.08
				mi.set_surface_override_material(si, stock)
			else:
				var col: Color = paint["col"]
				var src: Material = origs[si] if si < origs.size() else null
				var m: BaseMaterial3D = (src.duplicate() if src is BaseMaterial3D else StandardMaterial3D.new())
				m.albedo_color = m.albedo_color.lerp(col, 0.62)
				m.emission_enabled = true
				m.emission = col
				m.emission_energy_multiplier = 0.12
				mi.set_surface_override_material(si, m)

# ------------------------------------------------------------ vehicles & karts
func _gather_aabbs(n: Node, xf: Transform3D, acc: Array) -> void:
	if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
		acc.append(xf * (n as MeshInstance3D).get_aabb())
	for c in n.get_children():
		if c is Node3D:
			_gather_aabbs(c, xf * (c as Node3D).transform, acc)
		else:
			_gather_aabbs(c, xf, acc)

func _fit_model(model: Node3D, target_len: float) -> float:
	# measure the model's real bounds, scale so its footprint length == target_len,
	# and sit it on the ground. Returns the scaled top height (for sprite placement).
	var acc: Array = []
	_gather_aabbs(model, Transform3D.IDENTITY, acc)
	if acc.is_empty():
		return 2.5
	var bb: AABB = acc[0]
	for i in range(1, acc.size()):
		bb = bb.merge(acc[i])
	var longest: float = maxf(maxf(bb.size.x, bb.size.z), 0.001)
	var sc: float = target_len / longest
	model.scale = Vector3.ONE * sc
	model.position = Vector3(0, -bb.position.y * sc, 0)
	return (bb.position.y + bb.size.y) * sc

func _vehicle_body(vkey: String, col: Color, sprite_path: String, racer_name: String, paint: Dictionary = {}) -> Node3D:
	var root := Node3D.new()
	var vd: Dictionary = _vehicles_table()[vkey]
	var model: Node3D = null
	var glb_path: String = String(vd["glb"])
	if not ResourceLoader.exists(glb_path):
		glb_path = String(vd.get("legacy_glb", glb_path))
	if ResourceLoader.exists(glb_path):
		var ps: PackedScene = load(glb_path)
		if ps != null:
			model = ps.instantiate()
	var top_h := 2.5
	if model != null:
		top_h = _fit_model(model, float(vd["size"]))
		model.rotation = Vector3(0, float(vd["yaw_fix"]), 0)
		root.add_child(model)
		if _main != null and _main.has_method("_toonify"):
			_main._toonify(model)
		if paint.is_empty():
			_apply_paint(model, {"col": col.lerp(Color(0.55, 0.86, 0.92), 0.18)})
		else:
			_apply_paint(model, paint)
	else:
		# fallback: simple coloured box kart (never leaves a racer invisible)
		var chassis := MeshInstance3D.new()
		var cm := BoxMesh.new()
		cm.size = Vector3(3.0, 1.0, 4.4)
		chassis.mesh = cm
		var mat := StandardMaterial3D.new()
		mat.albedo_color = col
		chassis.material_override = mat
		chassis.position = Vector3(0, 1.0, 0)
		root.add_child(chassis)
	# driver sprite above the vehicle — normalised so every driver is ~3.2 units tall
	if sprite_path != "" and ResourceLoader.exists(sprite_path):
		var spr := Sprite3D.new()
		var tex: Texture2D = load(sprite_path)
		spr.texture = tex
		spr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		spr.pixel_size = 2.5 / maxf(float(tex.get_height()), 1.0)
		spr.position = Vector3(0, top_h + 1.5, 0)
		root.add_child(spr)
		root.set_meta("driver_spr", spr)
	var nl := Label3D.new()
	nl.text = racer_name
	nl.font_size = 54
	nl.outline_size = 12
	nl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	nl.modulate = col.lightened(0.4)
	nl.position = Vector3(0, top_h + 3.4, 0)
	root.add_child(nl)
	root.set_meta("name_lbl", nl)
	if racer_name == "Roshan" and not _speedy():
		var trail := OmniLight3D.new()
		trail.light_color = Color(1.0, 0.5, 0.9)
		trail.light_energy = 2.5
		trail.omni_range = 14.0
		trail.position = Vector3(0, 2.0, 2.5)
		root.add_child(trail)
	return root

func _vehicles_table() -> Dictionary:
	return _cv("vehicles", VEHICLES)

func _veh(k: Dictionary) -> Dictionary:
	return _vehicles_table()[String(k["veh"])]

func _build_karts(player_vehicle: String, paint: Dictionary = {}) -> void:
	var roster: Array = _cv("racers", RACERS)
	var n := roster.size()
	for idx in range(n):
		var r: Dictionary = roster[idx]
		var is_p: bool = bool(r.get("player", false))
		var vkey := player_vehicle
		if not is_p:
			vkey = VEHICLE_ORDER[idx % VEHICLE_ORDER.size()]
		# the driver on the player's kart wears the wardrobe skin (audit: it
		# was hardcoded classic Roshan no matter what she had dressed up as)
		var spath := String(r.get("sprite", ""))
		if is_p and _main != null and _main.has_method("skin_sprite_path"):
			spath = String(_main.skin_sprite_path())
		var node := _vehicle_body(vkey, r["col"], spath, String(r["name"]), paint if is_p else {})
		add_child(node)
		var start_s := -10.0 - float(idx) * 7.0   # longer grid so the pack doesn't pile into a totem
		var lane: float = [-0.3, 0.3, -0.6, 0.6][idx % 4] * _rhalf()
		var k := {
			"node": node, "name": String(r["name"]), "is_player": is_p, "veh": vkey,
			"s": start_s, "lat": lane, "latv": 0.0, "speed": 0.0,
			"boost_t": 0.0, "meter": 0.0,
			"ai_skill": 0.94 + 0.06 * (float(idx) / float(n)),
			"ai_phase": float(idx) * 1.3,
			"bumper": (idx % 2 == 1),   # half the pack trades paint with Roshan
		}
		_karts.append(k)
		if is_p:
			_pl = k

var _streaks: CPUParticles3D = null

func _build_camera() -> void:
	_cam = Camera3D.new()
	_cam.fov = 68.0
	_cam.far = 1500.0   # the course is a floating pocket; never render the distant real world
	add_child(_cam)
	_cam.make_current()
	# speed streaks: thin quads streaming past the camera at high speed / boost
	# (the near-field optic flow the empty air around the track can't provide)
	_streaks = CPUParticles3D.new()
	_streaks.emitting = false
	_streaks.amount = (12 if _speedy() else 26)
	_streaks.lifetime = 0.5
	_streaks.local_coords = false
	_streaks.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
	_streaks.emission_box_extents = Vector3(9.0, 6.0, 2.0)
	_streaks.direction = Vector3(0, 0, 1)   # spawned ahead, streaming back past the lens
	_streaks.spread = 2.0
	_streaks.initial_velocity_min = 55.0
	_streaks.initial_velocity_max = 75.0
	_streaks.gravity = Vector3.ZERO
	var sm := BoxMesh.new()
	sm.size = Vector3(0.05, 0.05, 1.7)
	_streaks.mesh = sm
	var smat := StandardMaterial3D.new()
	smat.albedo_color = Color(1, 1, 1, 0.4)
	smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	smat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	_streaks.mesh.material = smat
	_streaks.position = Vector3(0, 0, -16.0)
	_cam.add_child(_streaks)

# ------------------------------------------------------------ selection screen
func _select_slot_pos(i: int) -> Vector3:
	if _ground_mode() == "terrain":
		# stage the podiums ON the start straight — the road is always flat, wide
		# and clear, so the choice reads no matter what the seabed does around it
		var fr := _frame_at(16.0 + float(i) * 15.0, 0.0)
		return (fr[0] as Vector3) + Vector3(0, 0.3, 0)
	# float: staged outside the loop (the old spot, 60 under the origin, is now
	# inside the Butterfly World planet) — the camera faces the world hanging
	# in the sky behind the podiums
	return _origin() + Vector3(0, -60.0, 190.0) + Vector3((float(i) - 1.0) * 16.0, 0, 0)

func _build_select() -> void:
	for i in range(VEHICLE_ORDER.size()):
		var vkey: String = VEHICLE_ORDER[i]
		var vd: Dictionary = _vehicles_table()[vkey]
		var slot := Node3D.new()
		slot.position = _select_slot_pos(i)
		add_child(slot)
		var pod := MeshInstance3D.new()
		var pcm := CylinderMesh.new()
		pcm.top_radius = 5.5
		pcm.bottom_radius = 6.0
		pcm.height = 1.6
		pod.mesh = pcm
		var pmat := StandardMaterial3D.new()
		pmat.albedo_color = Color(0.25, 0.25, 0.4)
		pmat.emission_enabled = true
		pmat.emission = Color.from_hsv(float(i) / 3.0, 0.5, 1.0)
		pmat.emission_energy_multiplier = 0.3
		pod.material_override = pmat
		slot.add_child(pod)
		var body := _vehicle_body(vkey, Color(1, 1, 1), "", "")
		body.position = Vector3(0, 1.2, 0)
		slot.add_child(body)
		var lab := Label3D.new()
		# The models and glowing choice halo carry the selection for a non-reader;
		# keep the 3D card to one short name instead of covering it with a paragraph.
		lab.text = String(vd["label"])
		lab.font_size = 52
		lab.outline_size = 12
		lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		lab.position = Vector3(0, 8.5, 0)
		slot.add_child(lab)
		var halo := OmniLight3D.new()
		halo.light_color = Color(1, 1, 1)
		halo.light_energy = 0.0
		halo.omni_range = 18.0
		halo.position = Vector3(0, 4, 0)
		halo.visible = not _speedy()
		slot.add_child(halo)
		_sel_nodes.append({"slot": slot, "halo": halo, "body": body})
	_lbl_big.text = "Pick your ride!"
	_lbl_hint.text = ("slide a finger to choose  •  TAP to GO!" if _touch_device() else "LEFT/RIGHT to choose  •  SPACE or A to GO!")
	_set_guide_mode("steer")
	if _main != null and _main.has_method("_say"):
		_main._say("roshan", "intro4", 10.0)
	if _cam != null:
		var mid := _select_slot_pos(1)
		if _ground_mode() == "terrain":
			# view the podium row SIDE-ON (looking across the road) so all three
			# rides sit left-to-right instead of stacking behind each other
			var fr := _frame_at(31.0, 0.0)
			var right: Vector3 = fr[2]
			_cam.position = mid + right * 25.0 + Vector3(0, 7.5, 0)
			_cam.position.y = maxf(_cam.position.y, _terrain_y(_cam.position.x, _cam.position.z) + 5.0)
		else:
			_cam.position = mid + Vector3(0, 7.0, 26.0)
		_cam.look_at(mid + Vector3(0, 3.0, 0), Vector3.UP)

func _sel_move() -> int:
	var mv := 0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		mv = -1
	elif Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		mv = 1
	var jx: float = joy_axis(JOY_AXIS_LEFT_X)
	if absf(jx) > 0.4:
		mv = (1 if jx > 0.0 else -1)
	if joy_pressed(JOY_BUTTON_DPAD_LEFT):
		mv = -1
	elif joy_pressed(JOY_BUTTON_DPAD_RIGHT):
		mv = 1
	if _main != null and "touch_ui" in _main and _main.touch_ui != null:
		var tv: Vector2 = _main.touch_ui.stick_vec
		if absf(tv.x) > 0.4:
			mv = (1 if tv.x > 0.0 else -1)
	var edge := mv if (mv != 0 and _sel_move_prev == 0) else 0
	_sel_move_prev = mv
	return edge

func _build_paint_row() -> void:
	# swatch orbs floating above the chosen vehicle's podium
	var slot: Node3D = (_sel_nodes[_sel_idx] as Dictionary)["slot"]
	for i in range(PAINTS.size()):
		var pd: Dictionary = PAINTS[i]
		var orb := MeshInstance3D.new()
		var sm := SphereMesh.new()
		sm.radius = 1.1
		sm.height = 2.2
		orb.mesh = sm
		if bool(pd.get("rainbow", false)):
			orb.material_override = _rainbow_orb_mat()
		else:
			var m := StandardMaterial3D.new()
			var oc: Color = pd["col"] if pd.get("col") != null else Color(0.75, 0.75, 0.8)
			m.albedo_color = oc
			m.emission_enabled = true
			m.emission = oc
			m.emission_energy_multiplier = 0.4
			orb.material_override = m
		orb.position = Vector3((float(i) - float(PAINTS.size() - 1) * 0.5) * 3.2, 11.5, 0)
		slot.add_child(orb)
		_paint_orbs.append(orb)

func _tick_select(delta: float) -> void:
	_sel_t += delta
	for i in range(_sel_nodes.size()):
		var sn: Dictionary = _sel_nodes[i]
		var chosen: bool = (i == _sel_idx)
		(sn["body"] as Node3D).rotation.y += delta * (1.6 if chosen else 0.5)
		var want_e: float = 3.0 if chosen else 0.0
		var halo: OmniLight3D = sn["halo"]
		halo.light_energy = lerpf(halo.light_energy, want_e, delta * 8.0)
		var want_s: float = 1.15 if chosen else (0.6 if _sel_phase == "paint" else 1.0)
		(sn["slot"] as Node3D).scale = (sn["slot"] as Node3D).scale.lerp(Vector3.ONE * want_s, delta * 8.0)
	var edge := _sel_move()
	var confirm := _fire_just()
	if confirm and _sel_t < 0.6:
		_select_confirm_queued = true
		confirm = false
	elif _select_confirm_queued and _sel_t >= 0.6:
		confirm = true
		_select_confirm_queued = false
	if _sel_phase == "ride":
		if edge != 0:
			_sel_idx = clampi(_sel_idx + edge, 0, VEHICLE_ORDER.size() - 1)
		if confirm or _sel_t > SELECT_TIMEOUT:
			_sel_phase = "paint"
			_sel_t = 0.0
			_paint_prev = -1
			_build_paint_row()
			_lbl_big.text = "Pick your paint!"
		return
	# ---- paint phase ----
	var np := PAINTS.size()
	if edge != 0:
		_paint_idx = (_paint_idx + edge + np) % np
	for i in range(_paint_orbs.size()):
		var orb: Node3D = _paint_orbs[i]
		orb.scale = orb.scale.lerp(Vector3.ONE * (1.7 if i == _paint_idx else 1.0), delta * 10.0)
		orb.rotation.y += delta * 2.0
	if _sel_phase == "paint" and _cam != null:
		var focus_slot: Node3D = (_sel_nodes[_sel_idx] as Dictionary)["slot"]
		var focus: Vector3 = focus_slot.position
		var want_cam: Vector3
		if _ground_mode() == "terrain":
			var ffr := _frame_at(16.0 + float(_sel_idx) * 15.0, 0.0)
			want_cam = focus + (ffr[2] as Vector3) * 18.0 + Vector3(0, 6.5, 0)
			want_cam.y = maxf(want_cam.y, _terrain_y(want_cam.x, want_cam.z) + 5.0)
		else:
			want_cam = focus + Vector3(0, 6.0, 18.0)
		_cam.position = _cam.position.lerp(want_cam, minf(1.0, delta * 4.0))
		_cam.look_at(focus + Vector3(0, 3.2, 0), Vector3.UP)
	if _paint_idx != _paint_prev:
		_paint_prev = _paint_idx
		_apply_paint((_sel_nodes[_sel_idx] as Dictionary)["body"], PAINTS[_paint_idx])
		var confirm_hint := "TAP to GO!" if _touch_device() else "SPACE or A to GO!"
		_lbl_hint.text = String((PAINTS[_paint_idx] as Dictionary)["label"]) + "  •  " + confirm_hint
	if confirm or _sel_t > SELECT_TIMEOUT:
		var vkey: String = VEHICLE_ORDER[_sel_idx]
		var paint: Dictionary = PAINTS[_paint_idx]
		for sn2 in _sel_nodes:
			(sn2["slot"] as Node3D).queue_free()
		_sel_nodes.clear()
		_paint_orbs.clear()
		_build_karts(vkey, paint)
		_state = "countdown"
		_clock = 3.999
		_lbl_big.text = ""
		_lbl_hint.text = ("drag left/right to steer  •  TAP = TURBO when the bar is full!" if _touch_device() else "steer with LEFT/RIGHT  •  SPACE or A = TURBO!")
		_meter_bg.visible = true
		_set_guide_mode("action")
		# put the whole pack ON the grid right now (nodes used to sit at the
		# world origin until the first race frame — the countdown showed an
		# empty road) and SNAP the camera behind Roshan: the old 1s glide from
		# the podium shot passed nose-first through the Butterfly World
		# backdrop, so every race opened on a washed-out planet close-up
		for k2 in _karts:
			_place_kart(k2, 0.0)
		if _pl != null and _cam != null:
			var fr := _kart_frame(float(_pl["s"]), float(_pl["lat"]) * 0.35)
			var fwd0: Vector3 = fr[1]
			var dist0: float = 13.0 if _ground_mode() == "terrain" else 15.5
			_cam.position = (fr[0] as Vector3) - fwd0 * dist0 + Vector3(0, 8.5, 0)
			if _ground_mode() == "terrain":
				_cam.position.y = maxf(_cam.position.y, _terrain_y(_cam.position.x, _cam.position.z) + 5.0)
			_cam.look_at((_pl["node"] as Node3D).position + fwd0 * 6.0 + Vector3(0, 2.0, 0), Vector3.UP)

# ------------------------------------------------------------ input helpers
func _fire_just() -> bool:
	var now := Input.is_physical_key_pressed(KEY_SPACE) or joy_pressed(JOY_BUTTON_A) or joy_pressed(JOY_BUTTON_B) or Input.is_physical_key_pressed(KEY_ENTER)
	var just := now and not _fire_prev
	_fire_prev = now
	if not just and _main != null and "touch_ui" in _main and _main.touch_ui != null:
		if _main.touch_ui.has_method("consume_action_just"):
			just = bool(_main.touch_ui.consume_action_just())
	return just

func _steer_input() -> float:
	var steer := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		steer -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		steer += 1.0
	var jx: float = joy_axis(JOY_AXIS_LEFT_X)
	if absf(jx) > 0.2:
		steer += jx
	if joy_pressed(JOY_BUTTON_DPAD_LEFT):
		steer -= 1.0
	if joy_pressed(JOY_BUTTON_DPAD_RIGHT):
		steer += 1.0
	if _main != null and "touch_ui" in _main and _main.touch_ui != null:
		var tv: Vector2 = _main.touch_ui.stick_vec
		if tv.length() > 0.1:
			_touch_t = 3.0    # touch is the live input → co-pilot + pickup magnet on
		if absf(tv.x) > 0.15:
			steer += tv.x
	return clampf(steer, -1.0, 1.0)

func _brake_input() -> bool:
	if Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S):
		return true
	if joy_pressed(JOY_BUTTON_DPAD_DOWN) or joy_axis(JOY_AXIS_TRIGGER_LEFT) > 0.45:
		return true
	# Touch is deliberately steer-only. A preschool diagonal drag must never
	# silently cut auto-cruise to 45%; the course has no braking requirement.
	return false

# ------------------------------------------------------------ per-frame
func _process(delta: float) -> void:
	if _state == "done":
		return
	_tick_guide(delta)
	if _quit_arm_t > 0.0:
		_quit_arm_t = maxf(0.0, _quit_arm_t - delta)
		if _btn_quit != null:
			var quit_pulse: float = 1.0 + sin(_quit_arm_t * 10.0) * 0.08
			_btn_quit.pivot_offset = _btn_quit.size * 0.5
			_btn_quit.scale = Vector2.ONE * quit_pulse
		if _quit_arm_t <= 0.0 and _btn_quit != null:
			_btn_quit.text = "✕"
			_btn_quit.modulate = Color.WHITE
			_btn_quit.scale = Vector2.ONE
	# rainbow paint: cycle hue on plain materials (renderer-proof)
	var tt: float = Time.get_ticks_msec() / 1000.0
	if _rainbow_mats.size() > 0:
		var rc := Color.from_hsv(fmod(tt * 0.25, 1.0), 0.75, 1.0)
		for rm in _rainbow_mats:
			(rm as BaseMaterial3D).albedo_color = rc
			(rm as BaseMaterial3D).emission = rc * 0.5
	# the Butterfly World turns below the road (rainbow theme)
	_tick_butterfly_world(tt)
	# hazards animate in every state (crabs scuttle behind the pick screens
	# too); they only make CONTACT during the race
	_tick_hazards(delta)
	# ambient fish cruise gently beside the course (ocean theme)
	for fd in _deco_fish:
		var fn: Node3D = fd["node"]
		if is_instance_valid(fn):
			fn.position = (fd["base"] as Vector3) + Vector3(sin(tt * 0.8 + float(fd["ph"])) * 4.0, sin(tt * 1.3 + float(fd["ph"])) * 1.5, cos(tt * 0.6 + float(fd["ph"])) * 4.0)
			fn.rotation.y = tt * 0.5 + float(fd["ph"])
	if _state == "select":
		_tick_select(delta)
		return
	if _state == "podium":
		return
	_clock -= delta
	if _state == "countdown":
		if _fire_just():
			_rocket_armed = true
		var n := int(ceil(_clock))
		_lbl_big.text = ("GO!" if n <= 0 else str(n))
		if _clock <= 0.0:
			_state = "race"
			_lbl_big.text = ""
			# ROCKET START: already on the controls the instant GO fires —
			# teachable purely by feel, no reading required
			var hot: bool = _rocket_armed or absf(_steer_input()) > 0.05 or Input.is_physical_key_pressed(KEY_SPACE) or Input.is_physical_key_pressed(KEY_ENTER) or joy_pressed(JOY_BUTTON_A) or joy_pressed(JOY_BUTTON_B)
			if _main != null and "touch_ui" in _main and _main.touch_ui != null and (_main.touch_ui.stick_vec as Vector2).length() > 0.1:
				hot = true
			if hot and _pl != null:
				_pl["boost_t"] = 0.9
				_pl["squash"] = 0.3
				_chime(1.25)
				_flash_big("ROCKET START!")
			_rocket_armed = false
			if _main != null and _main.has_method("_say"):
				_main._say("roshan", "talk", 10.0)
		for k0 in _karts:
			_place_kart(k0, delta)   # pack idles ON the grid through 3-2-1
		_tick_engine()   # idle rumble builds anticipation through the count
		_update_camera(delta)
		return

	_race_t += delta
	var steer := _steer_input()
	var braking := _brake_input()
	var fired := _fire_just()

	for k in _karts:
		if k["is_player"]:
			_update_player(k, steer, braking, fired, delta)
		else:
			_update_ai(k, delta)
		_place_kart(k, delta)

	_check_strips(delta)
	_check_ramps()
	_check_pickups(delta)
	_check_pearls()
	_check_shortcut()
	_resolve_collisions()
	_tick_engine()
	_update_camera(delta)
	_update_hud()
	if _flash_t > 0.0:
		_flash_t -= delta
		if _flash_t <= 0.0 and _lbl_big != null:
			_lbl_big.text = ""

	if _pl != null and (float(_pl["s"]) >= _len * float(_laps()) or _race_t > 170.0):
		_finish()

func _update_player(k: Dictionary, steer: float, braking: bool, fired: bool, delta: float) -> void:
	var vd := _veh(k)
	k["boost_t"] = maxf(0.0, float(k["boost_t"]) - delta)
	# MK-Tour-style assist: a bar that sits FULL for a beat fires itself —
	# agency for the thumb that taps, a floor for the one that never does
	var want_fire := fired
	if float(k["meter"]) >= 0.99 and float(k["boost_t"]) <= 0.0:
		k["full_t"] = float(k.get("full_t", 0.0)) + delta
		if float(k["full_t"]) >= 2.5:
			want_fire = true
			_flash_big("TURBO!")
	else:
		k["full_t"] = 0.0
	# fire turbo (the interactive bit: player chooses the moment)
	if want_fire and float(k["meter"]) >= 0.5 and float(k["boost_t"]) <= 0.0:
		k["boost_t"] = TURBO_TIME * float(vd["turbo"])
		k["meter"] = maxf(0.0, float(k["meter"]) - 0.5)
		k["full_t"] = 0.0
		k["squash"] = 0.3       # launch squat
		_shake = maxf(_shake, 0.2)
		_chime(0.7)
		if _main != null and _main.has_method("_sparkle_burst"):
			_main._sparkle_burst((k["node"] as Node3D).position, Color(0.5, 1.0, 1.0))
	var boosting: bool = float(k["boost_t"]) > 0.0
	var bf: float = 1.0 + (BOOST_MUL if boosting else 0.0)
	var target: float = _vmax * float(vd["vmax"]) * bf
	# SLIPSTREAM: tuck in close behind a rival and the air tows you along —
	# rewards pack racing (which the bumper AI already creates) and slowly
	# tops up the turbo meter while in the tow
	if _draft_ahead(k):
		target *= 1.08
		_charge(k, 0.05 * delta)
	if braking and not boosting:
		target = _vmax * 0.45
	# launch punch: strong low-end pull that relaxes near top speed — the
	# kart-game acceleration curve (a linear ramp reads as a slow car; a fat
	# bottom end reads as a GO)
	var acc: float = (60.0 if boosting else 40.0)
	if float(k["speed"]) < target * 0.6:
		acc *= 1.8
	k["speed"] = move_toward(float(k["speed"]), target, acc * delta)
	_advance(k, delta)
	# ---- SPARKLE DRIFT (the kart-class skill ceiling, one thumb) ----
	# hold a hard steer INTO a bend for a beat to start carving; hold the carve
	# to charge SILVER -> GOLD -> RAINBOW; ease off and the charge releases as
	# turbo. Zero input still finishes the race — this only raises the ceiling.
	var kap := _curv_at(float(k["s"]))
	var bend: bool = absf(kap) > 0.006
	var into_bend: bool = bend and absf(steer) >= 0.6 and steer * kap < 0.0
	k["drift_arm"] = (float(k.get("drift_arm", 0.0)) + delta) if into_bend else 0.0
	if not bool(k.get("drift", false)) and float(k["drift_arm"]) >= 0.25:
		k["drift"] = true
		k["drift_t"] = 0.0
		k["drift_dir"] = signf(steer)
		k["hop"] = 0.22           # the entry hop — the classic drift signature
		_chime(1.05)
	if bool(k.get("drift", false)):
		var keep: bool = bend and absf(steer) >= 0.25 and signf(steer) == float(k["drift_dir"]) and steer * kap < 0.0
		if keep:
			k["drift_t"] = float(k["drift_t"]) + delta
			var tier := _drift_tier(float(k["drift_t"]))
			if tier > int(k.get("drift_tier_seen", 0)):
				k["drift_tier_seen"] = tier
				_chime(0.95 + 0.12 * float(tier))   # rising tier chime
			_drift_spray(k, tier)
		else:
			_drift_release(k)
	# steering with per-vehicle rate + slip (moto drifts, truck plants) — snappy response
	var slip: float = float(vd["slip"])
	var want_v: float = steer * float(vd["steer"])
	if bool(k.get("drift", false)):
		# the drift holds the carve FOR you: ease onto a clean line ~60 % of
		# the way to the inside rail (what a held drift does in kart games —
		# it locks an arc, it doesn't feed raw inward velocity, which would
		# grind the inside wall within half a second)
		var room: float = _width_at(_eff(float(k["s"]))) - 1.6
		var carve_lat: float = float(k["drift_dir"]) * room * 0.6
		want_v = clampf((carve_lat - float(k["lat"])) * 3.0, -float(vd["steer"]) * 1.4, float(vd["steer"]) * 1.4)
	# TOUCH CO-PILOT — 225-race platform sim: phone thumbs react ~4x slower
	# than pads and scraped the rails 2-3x as often (truck-touch: 35/race).
	# When the touch stick is the live input, a gentle assist eases the kart
	# off the wall BEFORE the scrape — unless the thumb is deliberately
	# pressed at the wall (bouncing off rails on purpose is part of the fun).
	_touch_t = maxf(0.0, _touch_t - delta)
	if _touch_t > 0.0:
		var rail: float = _width_at(_eff(float(k["s"]))) - 1.6
		var room: float = rail - absf(float(k["lat"]))
		var toward_wall: bool = float(k["lat"]) * steer > 0.3
		if room < 3.5 and not toward_wall:
			var aid: float = clampf((3.5 - room) / 3.5, 0.0, 1.0) * 0.7
			want_v = lerpf(want_v, -signf(float(k["lat"])) * float(vd["steer"]) * 0.6, aid)
	if float(k.get("air_t", 0.0)) > 0.0:
		want_v *= 0.5   # floaty mid-air: you can nudge the landing, not carve
	k["latv"] = lerpf(float(k["latv"]), want_v, minf(1.0, (1.0 - slip * 0.7) * 30.0 * delta + 0.14))
	_apply_lat(k, float(k["lat"]) + float(k["latv"]) * delta)

func _update_ai(k: Dictionary, delta: float) -> void:
	var vd := _veh(k)
	k["boost_t"] = maxf(0.0, float(k["boost_t"]) - delta)
	# AI charge meter slowly and fire when full-ish
	k["meter"] = minf(1.0, float(k["meter"]) + delta * 0.06)
	if float(k["meter"]) >= 0.9 and float(k["boost_t"]) <= 0.0 and randf() < delta * 0.6:
		k["boost_t"] = TURBO_TIME * float(vd["turbo"]) * 0.7
		k["meter"] = 0.2
	var bf: float = 1.0 + (BOOST_MUL if float(k["boost_t"]) > 0.0 else 0.0)
	# AI only gets a softened share of its vehicle's top-speed edge — the player
	# on ANY ride can out-drive the pack with clean lines + turbo timing
	var vveh: float = 1.0 + (float(vd["vmax"]) - 1.0) * 0.8
	var base: float = _vmax * float(k["ai_skill"]) * vveh * bf
	if _pl != null:
		# rubber band, kid-friendly asymmetric: leaders ease off a LOT, stragglers
		# catch up gently — losing stays close, winning stays possible
		var gap: float = float(_pl["s"]) - float(k["s"])
		base += clampf(gap * 0.08, -_vmax * 0.30, _vmax * 0.38)
		# PACK PRESENCE — 225-race sim: the band above settles rivals ~100u
		# behind, so the kid raced ALONE and bumper contact was literally zero.
		# Rivals within 25u keep real racing pace (bumpers more than the polite
		# half), so the pack stays on screen and trades paint. The ease-off
		# when they get ahead still hands the lead back — the win stays hers.
		if gap > 0.0:
			base += _vmax * (0.30 if bool(k.get("bumper", false)) else 0.18) * clampf(1.0 - gap / 25.0, 0.0, 1.0)
	if float(k.get("stun_t", 0.0)) > 0.0:
		k["stun_t"] = float(k["stun_t"]) - delta
		base *= 0.78   # just bounced off someone heavier — drop back and regroup
	k["speed"] = move_toward(float(k["speed"]), maxf(base, 0.0), 30.0 * delta)
	_advance(k, delta)
	var want: float = sin(_race_t * 0.3 + float(k["ai_phase"])) * _rhalf() * 0.16
	# rivals visibly dive for the inside of bends (same curvature-coupled
	# physics the player rides; the rubber band keeps the race fair)
	var kap := _curv_at(float(k["s"]))
	if absf(kap) > 0.004:
		want += -signf(kap) * _rhalf() * clampf(absf(kap) / 0.02, 0.0, 1.0) * 0.35
	# OVERTAKING LINE: swing wide around traffic instead of ploughing into
	# bumpers (the old jam-behind-the-truck). Sim finding: when EVERY rival
	# dodged the player too, player contact hit exactly 0.0 in 225 races and
	# the bumper-car game (the truck's whole identity) never happened. So the
	# pack splits personalities: half stay polite but cut a tighter line past
	# Roshan, half are BUMPERS who drift toward her lane and trade paint.
	for o in _karts:
		if o == k:
			continue
		var ds: float = float(o["s"]) - float(k["s"])
		if ds <= -1.0 or ds >= 10.0:
			continue
		if bool(o["is_player"]) and bool(k.get("bumper", false)):
			if ds < 6.0 and absf(float(o["lat"]) - float(k["lat"])) < 5.0:
				want = lerpf(float(k["lat"]), float(o["lat"]), 0.6)
				break
			continue
		var gap_w: float = 2.2 if bool(o["is_player"]) else 4.5
		var swing: float = 3.6 if bool(o["is_player"]) else 6.0
		if absf(float(o["lat"]) - float(k["lat"])) < gap_w:
			var side: float = 1.0 if float(k["lat"]) >= float(o["lat"]) else -1.0
			want = clampf(float(o["lat"]) + side * swing, -_rhalf() + 2.0, _rhalf() - 2.0)
			break
	_apply_lat(k, move_toward(float(k["lat"]), want, 7.0 * delta))

var _shake := 0.0
var _thunk_cool := 0.0
var _touch_t := 0.0   # >0 while the phone stick is the live input (sim: touch assists)

func _apply_lat(k: Dictionary, new_lat: float) -> void:
	var vd := _veh(k)
	var wall: float = _width_at(_eff(float(k["s"]))) - 1.6
	if absf(new_lat) > wall:
		new_lat = clampf(new_lat, -wall, wall) * 0.8
		k["latv"] = -float(k["latv"]) * 0.85     # bumper-car rebound off the rail
		k["speed"] = float(k["speed"]) * float(vd["wall"])
		k["squash"] = 0.3
		k["hop"] = 0.22
		_drift_cancel(k)                          # a scrape spills the drift charge
		if bool(k["is_player"]):
			_shake = maxf(_shake, 0.35)
			if _thunk_cool <= 0.0:
				_chime(0.5)                       # low thunk, not a pling
				_thunk_cool = 0.35
	k["lat"] = new_lat

func _place_kart(k: Dictionary, delta: float) -> void:
	var fr := _kart_frame(float(k["s"]), float(k["lat"]))
	var pos: Vector3 = fr[0]
	var fwd: Vector3 = fr[1]
	var up: Vector3 = fr[3]
	var node: Node3D = k["node"]
	# smooth ride; the bounce lives in IMPACTS (bumper-car hop), not a constant
	# gallop — the old speed bob read as a horse race
	var hop_t: float = float(k.get("hop", 0.0))
	var hop_h := 0.0
	if hop_t > 0.0:
		hop_t = maxf(0.0, hop_t - delta)
		k["hop"] = hop_t
		var hop_p: float = clampf(1.0 - hop_t / 0.25, 0.0, 1.0)
		hop_h = sin(hop_p * PI) * 0.9
	# ramp air: a real arc with hang time; the clean landing pays a free zip
	var air_t: float = float(k.get("air_t", 0.0))
	var air_p := 0.0
	var air_h := 0.0
	if air_t > 0.0:
		air_t = maxf(0.0, air_t - delta)
		k["air_t"] = air_t
		air_p = 1.0 - air_t / AIR_DUR
		air_h = sin(air_p * PI) * 5.0
		if air_t <= 0.0:
			k["boost_t"] = maxf(float(k["boost_t"]), 0.5)   # the auto-trick payout
			k["squash"] = 0.3
			if bool(k["is_player"]):
				_chime(1.25)
				_shake = maxf(_shake, 0.15)
				if _main != null and _main.has_method("_sparkle_burst"):
					_main._sparkle_burst(node.position, Color(1.0, 0.9, 0.4))
	k["haz_cool"] = maxf(0.0, float(k.get("haz_cool", 0.0)) - delta)
	node.position = pos + up * (1.2 + hop_h + air_h)
	if fwd.length() > 0.001:
		# Orient from the raised kart position toward the track tangent. Looking
		# from the airborne kart down at the ground-frame target pitched it almost
		# vertically nose-first at every jump apex.
		node.look_at(node.position + fwd, up)
		if air_p > 0.0:
			# nose lifts off the ramp, dips into the landing
			node.rotate_object_local(Vector3(1, 0, 0), -cos(air_p * PI) * 0.30)
		# hazard bonk: one silly full spin (visual only — steering unaffected)
		var spin_t: float = float(k.get("spin_t", 0.0))
		if spin_t > 0.0:
			spin_t = maxf(0.0, spin_t - delta)
			k["spin_t"] = spin_t
			node.rotate_object_local(Vector3(0, 1, 0), (1.0 - spin_t / 0.6) * TAU)
		# point the nose INTO the turn (the visual feedback that makes steering feel real)
		var vyaw: float = clampf(-float(k["latv"]) * 0.030, -0.55, 0.55)
		if bool(k.get("drift", false)):
			# drift counter-rotation: the nose swings INTO the bend beyond the
			# travel direction — the visual signature that says "drifting"
			vyaw += -float(k.get("drift_dir", 0.0)) * 0.30
		node.rotate_object_local(Vector3(0, 1, 0), vyaw)
		# lean/roll into steering (moto most, truck least)
		var vd := _veh(k)
		var lean: float = float(vd["lean"])
		if lean > 0.01:
			node.rotate_object_local(Vector3(0, 0, 1), clampf(float(k["latv"]) * 0.022 * lean, -0.4, 0.4))
	# rival billboards fade out as they close on the camera — a giant driver
	# face used to fill the screen whenever the pack pressed in behind you
	if _cam != null and not bool(k["is_player"]):
		var camd: float = node.position.distance_to(_cam.position)
		var fade: float = clampf((camd - 10.0) / 8.0, 0.0, 1.0)
		var dspr: Sprite3D = k["node"].get_meta("driver_spr", null)
		if dspr != null and is_instance_valid(dspr):
			dspr.modulate.a = fade
		var nlbl: Label3D = k["node"].get_meta("name_lbl", null)
		if nlbl != null and is_instance_valid(nlbl):
			nlbl.modulate.a = fade
	# squash & stretch pulse on impacts (bouncy!)
	var sq: float = float(k.get("squash", 0.0))
	if sq > 0.0:
		sq = maxf(0.0, sq - delta)
		k["squash"] = sq
		var pulse: float = sin((0.3 - sq) / 0.3 * PI) * (sq / 0.3 + 0.4)
		node.scale = Vector3(1.0 + 0.16 * pulse, 1.0, 1.0 - 0.10 * pulse)
	elif node.scale != Vector3.ONE:
		node.scale = node.scale.lerp(Vector3.ONE, minf(1.0, delta * 12.0))

# ------------------------------------------------------------ track interactions
func _charge(k: Dictionary, amt: float) -> void:
	# the Rainbow Kart's "mcharge" makes every pickup worth 30% more meter
	k["meter"] = minf(1.0, float(k["meter"]) + amt * float(_veh(k).get("mcharge", 1.0)))

# ------------------------------------------------------------ sparkle drift
const DRIFT_TIERS := [0.0, 0.8, 1.6, 2.4]          # seconds held -> tier
const DRIFT_BOOST := [0.0, 0.55, 0.95, 1.4]        # released turbo per tier
const DRIFT_COLS := [Color(1, 1, 1), Color(0.85, 0.9, 1.0), Color(1.0, 0.85, 0.3), Color(1.0, 0.5, 0.9)]
var _spray: CPUParticles3D = null                  # one persistent emitter, not per-burst nodes
var _spray_mat: StandardMaterial3D = null
var _flash_t := 0.0                                # short center-screen celebration text

func _drift_tier(t: float) -> int:
	for i in range(DRIFT_TIERS.size() - 1, 0, -1):
		if t >= float(DRIFT_TIERS[i]):
			return i
	return 0

func _drift_spray(k: Dictionary, tier: int) -> void:
	if _spray == null:
		_spray = CPUParticles3D.new()
		_spray.amount = (10 if _speedy() else 20)
		_spray.lifetime = 0.5
		_spray.direction = Vector3(0, 0.6, 1.0)
		_spray.spread = 25.0
		_spray.initial_velocity_min = 4.0
		_spray.initial_velocity_max = 9.0
		_spray.gravity = Vector3(0, -6.0, 0)
		_spray.scale_amount_min = 0.10
		_spray.scale_amount_max = 0.30
		var bm := BoxMesh.new()
		bm.size = Vector3(0.3, 0.3, 0.3)
		_spray.mesh = bm
		_spray_mat = StandardMaterial3D.new()
		_spray_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		_spray_mat.vertex_color_use_as_albedo = false
		_spray.mesh.material = _spray_mat
		(k["node"] as Node3D).add_child(_spray)
		_spray.position = Vector3(0, 0.4, 2.2)   # off the tail
	_spray.emitting = true
	var col: Color = DRIFT_COLS[tier]
	if tier >= 3:
		col = Color.from_hsv(fmod(Time.get_ticks_msec() / 1000.0 * 0.8, 1.0), 0.7, 1.0)   # RAINBOW tier
	_spray_mat.albedo_color = col
	_spray_mat.emission_enabled = true
	_spray_mat.emission = col
	_spray_mat.emission_energy_multiplier = 0.8

func _drift_release(k: Dictionary) -> void:
	var tier := _drift_tier(float(k.get("drift_t", 0.0)))
	k["drift"] = false
	k["drift_arm"] = 0.0
	k["drift_t"] = 0.0
	k["drift_tier_seen"] = 0
	if _spray != null:
		_spray.emitting = false
	if tier <= 0:
		return
	k["boost_t"] = maxf(float(k["boost_t"]), float(DRIFT_BOOST[tier]))
	k["squash"] = 0.3
	_shake = maxf(_shake, 0.12)
	_chime(1.0 + 0.15 * float(tier))
	if _main != null and _main.has_method("_sparkle_burst"):
		_main._sparkle_burst((k["node"] as Node3D).position, DRIFT_COLS[tier])
	if tier >= 2:
		_flash_big("SPARKLE DRIFT!" if tier == 2 else "RAINBOW DRIFT!!")

func _drift_cancel(k: Dictionary) -> void:
	# a wall scrape mid-drift spills the charge — that IS the drift lesson,
	# and it's gentle (the thump feedback already plays)
	if bool(k.get("drift", false)):
		k["drift"] = false
		k["drift_arm"] = 0.0
		k["drift_t"] = 0.0
		k["drift_tier_seen"] = 0
		if _spray != null:
			_spray.emitting = false

func _flash_big(txt: String) -> void:
	if _lbl_big != null and _state == "race":
		_lbl_big.text = txt
		_flash_t = 1.1

func _speedy() -> bool:
	return _main != null and "quality" in _main and String(_main.quality) == "speedy"

func _draft_ahead(k: Dictionary) -> bool:
	for o in _karts:
		if o == k:
			continue
		var ds: float = float(o["s"]) - float(k["s"])
		if ds > 2.5 and ds < 12.0 and absf(float(o["lat"]) - float(k["lat"])) < 2.6:
			return true
	return false

func _check_strips(delta: float) -> void:
	for k in _karts:
		var kn: Node3D = k["node"]
		for sd in _strip_data:
			if kn.position.distance_to(sd["pos"]) < float(sd["len"]) * 0.6 + 3.0:
				# strips: small instant zip + meter charge
				if float(k["boost_t"]) < 0.35:
					k["boost_t"] = 0.35
				_charge(k, 0.60 * delta)

func _check_pickups(delta: float) -> void:
	if _pl == null:
		return
	var pn: Node3D = _pl["node"]
	var t: float = Time.get_ticks_msec() / 1000.0
	for pu in _pickups_live:
		var node: Node3D = pu["node"]
		node.rotation.y = t * 1.6
		node.position.y = (_frame_at(float(pu["s"]), float(pu["lat"]))[0] as Vector3).y + 2.6 + sin(t * 2.0 + float(pu["s"])) * 0.5
		if pu.get("rlab") != null:
			(pu["rlab"] as Label3D).modulate = Color.from_hsv(fposmod(t * 0.5, 1.0), 0.65, 1.0)
		if float(pu["cool"]) > 0.0:
			pu["cool"] = float(pu["cool"]) - delta
			if float(pu["cool"]) <= 0.0:
				node.visible = true
			continue
		# touch magnet: sim showed phone thumbs miss pickups (boost uptime ~10
		# points under pad) — widen the grab so the fun stays platform-fair
		if node.position.distance_to(pn.position) < (8.5 if _touch_t > 0.0 else 6.5):
			var kind := String(pu["kind"])
			var col := Color(1.0, 0.7, 0.95)
			# every pickup pays out NOW (owner playtest: meter-only charges
			# were invisible to a 4yo — the chime played and nothing happened)
			match kind:
				"star":
					_charge(_pl, 0.7)
					_pl["boost_t"] = maxf(float(_pl["boost_t"]), 0.7)
					_pl["squash"] = 0.3
					col = Color(1.0, 0.9, 0.3)
					_chime(0.9)
					_shake = maxf(_shake, 0.1)
				"shell":
					_charge(_pl, 0.4)
					_pl["boost_t"] = maxf(float(_pl["boost_t"]), 0.4)
					_chime(0.9)
				"bubble":
					# POP! instant zip, no meter needed — keeps the race lively
					_pl["boost_t"] = maxf(float(_pl["boost_t"]), 0.8)
					_pl["squash"] = 0.3
					col = Color(0.5, 0.95, 1.0)
					_chime(1.1)
				"rainbow":
					# jackpot: full meter AND an immediate full-length turbo —
					# the guaranteed WHOOSH even if the tap never comes
					_pl["meter"] = 1.0
					_pl["boost_t"] = maxf(float(_pl["boost_t"]), TURBO_TIME * float(_veh(_pl)["turbo"]))
					_pl["squash"] = 0.3
					_flash_big("RAINBOW POWER!")
					col = Color.from_hsv(fposmod(t, 1.0), 0.7, 1.0)
					_chime(1.3)
					_shake = maxf(_shake, 0.15)
			node.visible = false
			pu["cool"] = 6.0
			if _main != null and _main.has_method("_sparkle_burst"):
				_main._sparkle_burst(pn.position, col)

func _check_pearls() -> void:
	if _pl == null:
		return
	var pn: Node3D = _pl["node"]
	for pd in _pearls_live:
		if bool(pd["got"]):
			continue
		var node: Node3D = pd["node"]
		if node.position.distance_to(pn.position) < (6.0 if _touch_t > 0.0 else 4.5):
			pd["got"] = true
			node.visible = false
			_pearls_got += 1
			_commit_payout(0)   # zero-lost-progress: each collected pearl is durable now
			_charge(_pl, 0.05)
			_chime(0.8 + 0.02 * float(_pearls_got % 8))
			if _main != null and _main.has_method("_sparkle_burst"):
				_main._sparkle_burst(node.position, Color(1.0, 0.8, 1.0))

func _check_shortcut() -> void:
	if _rev or _pl == null or not has_meta("gate_pos"):
		return
	var lap: int = int(float(_pl["s"]) / _len)
	if lap == _shortcut_used_lap:
		return
	var gate: Vector3 = get_meta("gate_pos")
	var pn: Node3D = _pl["node"]
	if pn.position.distance_to(gate + Vector3(0, 1.2, 0)) < 7.0:
		_shortcut_used_lap = lap
		var base: float = float(lap) * _len
		_pl["s"] = base + SHORTCUT_TO_U * _len
		_pl["boost_t"] = maxf(float(_pl["boost_t"]), 0.9)
		if _main != null and _main.has_method("_sparkle_burst"):
			_main._sparkle_burst(pn.position, Color(0.5, 1.0, 0.8))

func _resolve_collisions() -> void:
	for i in range(_karts.size()):
		for j in range(i + 1, _karts.size()):
			var a: Dictionary = _karts[i]
			var b: Dictionary = _karts[j]
			var an: Node3D = a["node"]
			var bn: Node3D = b["node"]
			var d: float = an.position.distance_to(bn.position)
			if d < COLLIDE_R and d > 0.01:
				var ma: float = float(_veh(a)["mass"])
				var mb: float = float(_veh(b)["mass"])
				var tot: float = ma + mb
				var sep: float = (COLLIDE_R - d)
				var dir: float = 1.0 if float(a["lat"]) >= float(b["lat"]) else -1.0
				var wa: float = _width_at(_eff(float(a["s"]))) - 1.4
				var wb: float = _width_at(_eff(float(b["s"]))) - 1.4
				# BUMPER CARS: MASS WINS the bump (sim-tuned). The heavier kart
				# keeps its pace and gets a satisfying shove-boost; the lighter one
				# is slowed, flung wide and loses its zip. Equal weights just trade
				# a fair thump. Positional shove keeps them from overlapping.
				a["lat"] = clampf(float(a["lat"]) + dir * sep * (mb / tot), -wa, wa)
				b["lat"] = clampf(float(b["lat"]) - dir * sep * (ma / tot), -wb, wb)
				a["latv"] = float(a["latv"]) + dir * 30.0 * (mb / tot)
				b["latv"] = float(b["latv"]) - dir * 30.0 * (ma / tot)
				var player_was_light := false
				if absf(ma - mb) < 0.001:
					# Equal rides trade the same fair thump. Do not let array order
					# crown `a` the winner and silently hand it a speed boost.
					var avg_speed: float = (float(a["speed"]) + float(b["speed"])) * 0.5
					a["speed"] = lerpf(float(a["speed"]), avg_speed, 0.35) * 0.96
					b["speed"] = lerpf(float(b["speed"]), avg_speed, 0.35) * 0.96
				else:
					var heavy: Dictionary = a if ma > mb else b
					var light: Dictionary = b if ma > mb else a
					player_was_light = bool(light["is_player"])
					var edge: float = maxf(ma, mb) / tot
					var fastest: float = maxf(float(a["speed"]), float(b["speed"]))
					heavy["speed"] = minf(maxf(float(heavy["speed"]), fastest) * (1.0 + 0.08 * edge), _vmax * 1.9)
					light["speed"] = float(light["speed"]) * (1.08 - 0.5 * edge)
					# a bump strips a RIVAL's zip, never hers — the bumper AI hunts
					# her lane, so this line was silently deleting almost every
					# boost she earned ("the items don't work")
					if not bool(light["is_player"]):
						light["boost_t"] = minf(float(light["boost_t"]), 0.1)
					light["stun_t"] = 0.45   # drop back instead of grinding inside the winner
					if float(light["s"]) > float(heavy["s"]):
						light["s"] = float(light["s"]) - sep * 0.15
				a["squash"] = 0.3
				b["squash"] = 0.3
				a["hop"] = 0.25
				b["hop"] = 0.25
				if bool(a["is_player"]) or bool(b["is_player"]):
					_shake = maxf(_shake, 0.3)
					if _thunk_cool <= 0.0:
						_chime(0.45)   # deep bumper thunk
						_thunk_cool = 0.3
						# Roshan whoops when SHE takes the shove ("Whoooaa!")
						if player_was_light and _main != null and _main.has_method("_say"):
							_main._say("roshan", "bump", 7.0)

func _chime(pitch: float) -> void:
	if _main != null and "chime" in _main and _main.chime != null:
		_main.chime.pitch_scale = pitch
		_main.chime.play()

# ------------------------------------------------------------ engine hum
# Procedural putt-putt via AudioStreamGenerator: pitch rides the speed — the
# strongest subconscious speed cue a racer has, and the one this game had
# none of. No OGG asset, no license line. VERIFY ON DEVICE: if frame drops
# make it crackle, lower the mix rate or gate it off.
var _eng: AudioStreamPlayer = null
var _eng_pb: AudioStreamGeneratorPlayback = null
var _eng_phase := 0.0

func _build_engine() -> void:
	if _speedy():
		return   # per-frame buffer fill is CPU the budget tier doesn't have
	_eng = AudioStreamPlayer.new()
	var gen := AudioStreamGenerator.new()
	gen.mix_rate = 22050.0
	gen.buffer_length = 0.15
	_eng.stream = gen
	_eng.volume_db = -18.0   # a quiet bed UNDER the music, not a race car
	add_child(_eng)
	_eng.play()
	_eng_pb = _eng.get_stream_playback()

func _tick_engine() -> void:
	if _eng_pb == null or _pl == null:
		return
	var spd_n: float = clampf(float(_pl["speed"]) / (_vmax * 1.5), 0.0, 1.0)
	var freq: float = 58.0 + 150.0 * spd_n + (26.0 if float(_pl["boost_t"]) > 0.0 else 0.0)
	var frames: int = _eng_pb.get_frames_available()
	if frames <= 0:
		return
	var buf := PackedVector2Array()
	buf.resize(frames)
	for i in range(frames):
		_eng_phase += freq / 22050.0
		var p: float = fposmod(_eng_phase, 1.0)
		# soft saw + an octave up — a friendly toy putt-putt
		var s: float = (p * 2.0 - 1.0) * 0.55 + sin(p * TAU * 2.0) * 0.3
		s *= 0.16 + 0.10 * spd_n
		buf[i] = Vector2(s, s)
	_eng_pb.push_buffer(buf)

# ------------------------------------------------------------ camera + HUD
func _update_camera(delta: float) -> void:
	if _cam == null or _pl == null:
		return
	var pn: Node3D = _pl["node"]
	# follow a partially-centred line so the kart visibly SLIDES across the screen
	# when steering (full-lat tracking pinned it dead-centre = steering felt dead)
	var fr := _kart_frame(float(_pl["s"]), float(_pl["lat"]) * 0.35)
	var fwd: Vector3 = fr[1]
	var right: Vector3 = fr[2]
	var boosting: bool = float(_pl["boost_t"]) > 0.0
	var terrain: bool = _ground_mode() == "terrain"
	# perceived speed is a continuous channel, not a boost on/off switch: the
	# camera pulls back and the FOV widens with actual speed, then boost kicks
	# a little extra on top (optic flow + edge stretch = "I'm going FAST")
	var spd_n: float = clampf(float(_pl["speed"]) / (_vmax * 1.5), 0.0, 1.0)
	var dist: float = (12.5 + 3.5 * spd_n) if terrain else (15.0 + 4.0 * spd_n)
	var want: Vector3 = (fr[0] as Vector3) - fwd * dist + Vector3(0, 8.5 if terrain else 8.0, 0)
	if terrain:
		# never sink the camera into a dune or ridge behind the kart
		want.y = maxf(want.y, _terrain_y(want.x, want.z) + 5.0)
		want.y = maxf(want.y, pn.position.y + 4.5)
	if _shake > 0.0:
		_shake = maxf(0.0, _shake - delta)
		want += right * sin(Time.get_ticks_msec() * 0.045) * _shake * 1.6
	_thunk_cool = maxf(0.0, _thunk_cool - delta)
	_cam.position = _cam.position.lerp(want, clampf(delta * 4.0, 0.0, 1.0))
	_cam.fov = lerpf(_cam.fov, 62.0 + 14.0 * spd_n + (7.0 if boosting else 0.0), delta * 5.0)
	# the horizon leans into the carve (tiny, but it makes steering feel physical)
	var up_roll := Vector3.UP.rotated(fwd, clampf(-float(_pl["latv"]) * 0.010, -0.10, 0.10))
	_cam.look_at(pn.position + fwd * 6.0 + Vector3(0, 2.0, 0), up_roll)
	if _streaks != null:
		_streaks.emitting = boosting or spd_n > 0.62

func _mk_label(parent: Control, pos: Vector2, size: int, col: Color = Color.WHITE) -> Label:
	var l := Label.new()
	l.position = pos
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", col)
	l.add_theme_color_override("font_outline_color", Color(0.10, 0.08, 0.28))
	l.add_theme_constant_override("outline_size", 6)
	parent.add_child(l)
	return l

func _set_guide_mode(mode: String) -> void:
	if _guide_mode == mode:
		return
	_guide_mode = mode
	if _guide_pointer == null:
		return
	_guide_pointer.visible = mode != ""
	_guide_pointer.scale = Vector2.ONE
	_guide_pointer.rotation = 0.0
	if mode == "action":
		if not _touch_device():
			# Desktop/gamepad has no bottom-right touch bubble to point at.
			_guide_pointer.visible = false
			return
		# Points directly into touch_ui's bottom-right action bubble.
		_guide_pointer.text = "➜"
		_guide_pointer.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
		_guide_pointer.offset_left = -300.0
		_guide_pointer.offset_top = -190.0
		_guide_pointer.offset_right = -190.0
		_guide_pointer.offset_bottom = -90.0
	elif mode == "steer":
		_guide_pointer.text = "↔"
		_guide_pointer.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
		_guide_pointer.offset_left = -92.0
		_guide_pointer.offset_top = -180.0
		_guide_pointer.offset_right = 92.0
		_guide_pointer.offset_bottom = -80.0

func _tick_guide(delta: float) -> void:
	if _guide_pointer == null or not _guide_pointer.visible:
		return
	_guide_t += delta
	_guide_pointer.pivot_offset = _guide_pointer.size * 0.5
	if _guide_mode == "action":
		var pulse: float = 1.0 + sin(_guide_t * 5.0) * 0.13
		_guide_pointer.scale = Vector2.ONE * pulse
	else:
		var slide: float = sin(_guide_t * 2.7) * 44.0
		_guide_pointer.offset_left = -92.0 + slide
		_guide_pointer.offset_right = 92.0 + slide
		_guide_pointer.rotation = sin(_guide_t * 2.7) * 0.05

func _build_hud() -> void:
	_hud = CanvasLayer.new()
	_hud.layer = 18
	add_child(_hud)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	# a plain Control defaults to MOUSE_FILTER_STOP — full-rect, that swallows
	# every tap/drag before touch_ui's stick can see it. Display only: IGNORE.
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hud.add_child(root)
	_lbl_lap = _mk_label(root, Vector2(24, 18), 38, Color(1, 0.95, 0.6))
	_lbl_place = _mk_label(root, Vector2(24, 66), 48, Color(0.7, 1.0, 1.0))
	_lbl_pearls = _mk_label(root, Vector2(24, 124), 30, Color(1.0, 0.85, 1.0))
	_lbl_big = _mk_label(root, Vector2.ZERO, 76, Color(1, 1, 1))
	# Reset both anchors AND offsets. Keeping the position offsets created by
	# _mk_label made this full-rect label clip into the top-left on Mobile.
	_lbl_big.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_lbl_big.offset_left = 150.0
	_lbl_big.offset_top = 80.0
	_lbl_big.offset_right = -150.0
	_lbl_big.offset_bottom = -90.0
	_lbl_big.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_lbl_big.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_lbl_big.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_guide_pointer = _mk_label(root, Vector2.ZERO, 78, Color(1.0, 0.92, 0.35))
	_guide_pointer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_guide_pointer.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_guide_pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_guide_pointer.visible = false
	_lbl_hint = _mk_label(root, Vector2(24, 0), 26, Color(0.9, 0.9, 1.0))
	_lbl_hint.anchor_top = 1.0
	_lbl_hint.position = Vector2(24, -56)
	# turbo meter (bottom centre)
	_meter_bg = ColorRect.new()
	_meter_bg.mouse_filter = Control.MOUSE_FILTER_IGNORE   # "TAP for TURBO!!" points right at it
	_meter_bg.color = Color(0, 0, 0, 0.45)
	_meter_bg.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	_meter_bg.position = Vector2(-180, -96)
	_meter_bg.size = Vector2(360, 30)
	_meter_bg.visible = false   # shown when the race starts
	root.add_child(_meter_bg)
	_meter_fill = ColorRect.new()
	_meter_fill.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_meter_fill.color = Color(0.3, 0.95, 1.0)
	_meter_fill.position = Vector2(3, 3)
	_meter_fill.size = Vector2(0, 24)
	_meter_bg.add_child(_meter_fill)
	# ✕ close (top-right): leave the race and pop back out where you launched
	# from. A real Button, so it gets first claim on its taps — touch_ui's
	# stick only ever sees touches nothing else wanted.
	_btn_quit = Button.new()
	_btn_quit.text = "✕"
	_btn_quit.add_theme_font_size_override("font_size", 40)
	_btn_quit.add_theme_color_override("font_color", Color(1, 1, 1, 0.9))
	var qsb := StyleBoxFlat.new()
	qsb.bg_color = Color(0.2, 0.15, 0.35, 0.55)
	qsb.set_corner_radius_all(20)
	_btn_quit.add_theme_stylebox_override("normal", qsb)
	_btn_quit.add_theme_stylebox_override("hover", qsb)
	_btn_quit.add_theme_stylebox_override("pressed", qsb)
	_btn_quit.focus_mode = Control.FOCUS_NONE
	_btn_quit.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	_btn_quit.offset_left = -140.0
	_btn_quit.offset_top = 16.0
	_btn_quit.offset_right = -20.0
	_btn_quit.offset_bottom = 92.0
	_btn_quit.pressed.connect(_quit_race)
	root.add_child(_btn_quit)

func _quit_race() -> void:
	if _state == "podium" or _state == "done":
		return   # already finishing — let the podium payout complete instead
	# Two icon taps prevent a stray preschool thumb from closing a run. No
	# reading is required: the button visibly becomes a pulsing double-X.
	if _quit_arm_t <= 0.0:
		_quit_arm_t = 2.2
		_btn_quit.text = "✕  ✕"
		_btn_quit.modulate = Color(1.0, 0.55, 0.55)
		_chime(0.8)
		return
	_commit_payout(0)
	_chime(0.6)
	_teardown(-1)

func _placement() -> int:
	if _pl == null:
		return 1
	var ahead := 1
	for k in _karts:
		if not k["is_player"] and float(k["s"]) > float(_pl["s"]):
			ahead += 1
	return ahead

func _placement_bonus(place: int) -> int:
	if place == 1:
		return 15
	if place == 2:
		return 10
	if place == 3:
		return 8
	return 5

func _commit_payout(bonus: int) -> int:
	# Incremental and idempotent: pearls are banked as collected, while finish
	# adds only the still-unbanked remainder plus the placement bonus.
	if not bool(_cv("pearl_payout", true)):
		return 0
	var wanted: int = maxi(0, _pearls_got) + maxi(0, bonus)
	var add_now: int = maxi(0, wanted - _payout_banked)
	if _main != null and "pearl_count" in _main:
		if add_now > 0:
			_main.pearl_count += add_now
			_payout_banked += add_now
			_payout_dirty = true
		# Keep the in-memory bank separate from persistence state. A failed open or
		# flush must not double-add pearls, but pause/quit should retry the same save.
		if _payout_dirty and _main.has_method("_write_save"):
			var save_result: Variant = _main._write_save()
			if save_result == true:
				_payout_dirty = false
	else:
		# Test/minimal hosts may not expose the economy. Still make repeated calls
		# idempotent within this race instance.
		_payout_banked = wanted
		_payout_dirty = false
	return wanted

func _commit_completion(place: int) -> void:
	if _completion_committed or place < 1:
		return
	_completion_committed = true
	if _main != null and _main.has_method("_kart_completion_committed"):
		_main._kart_completion_committed(place)

func _update_hud() -> void:
	if _pl == null:
		return
	var lap: int = clampi(int(float(_pl["s"]) / _len) + 1, 1, _laps())
	_lbl_lap.text = ("Lap %d / %d  ↺ REVERSE" % [lap, _laps()]) if _rev else ("Lap %d / %d" % [lap, _laps()])
	var place := _placement()
	var suffix: String = ["st", "nd", "rd", "th", "th", "th", "th", "th"][clampi(place - 1, 0, 7)]
	_lbl_place.text = "%d%s" % [place, suffix]
	_lbl_pearls.text = "◉ %d pearls" % _pearls_got
	var m: float = float(_pl["meter"])
	_meter_fill.size = Vector2(354.0 * m, 24)
	var rdy: bool = m >= 0.5 and float(_pl["boost_t"]) <= 0.0
	_meter_fill.color = (Color(1.0, 0.85, 0.2) if rdy else Color(0.3, 0.95, 1.0))
	var ready_hint := "TAP for TURBO!!" if _touch_device() else "SPACE or A for TURBO!!"
	_lbl_hint.text = ready_hint if rdy else ("TURBO!" if float(_pl["boost_t"]) > 0.0 else "shells & stars charge turbo • bubbles ZIP • rainbow star = FULL power!")
	if rdy:
		_set_guide_mode("action")
	elif _race_t < 7.0:
		_set_guide_mode("steer")
	else:
		_set_guide_mode("")

# ------------------------------------------------------------ finish + podium
func _finish() -> void:
	if _pl != null:
		_drift_cancel(_pl)   # stop the tail spray before the podium
	_state = "podium"
	var place := _placement()
	var suffix: String = ["st", "nd", "rd", "th", "th", "th", "th", "th"][clampi(place - 1, 0, 7)]
	# Finish is a positive completion at every placement. Commit durable economy
	# first, then let main atomically save sticker/Galaxy progression before the
	# purely presentational podium delay.
	var payout: int = _commit_payout(_placement_bonus(place))
	if _main != null and _main.has_method("_update_hud"):
		_main._update_hud()
	_commit_completion(place)
	_set_guide_mode("")
	_lbl_big.text = "YOU DID IT!"
	_lbl_hint.text = ("%d%s place  •  +%d pearls!" % [place, suffix, payout]) if bool(_cv("pearl_payout", true)) else ("Great racing — %d%s place!" % [place, suffix])
	if _main != null and _main.has_method("_say"):
		_main._say("roshan", "win", 2.0)
	# podium: top 3 by distance
	var order := _karts.duplicate()
	order.sort_custom(func(a, b): return float(a["s"]) > float(b["s"]))
	var sf := _frame_at(0.0, 0.0)
	var c0: Vector3 = sf[0]
	var fright: Vector3 = sf[2]
	var heights := [4.0, 2.6, 1.6]
	for i in range(mini(3, order.size())):
		var blk := MeshInstance3D.new()
		var bm := BoxMesh.new()
		bm.size = Vector3(7.0, heights[i], 7.0)
		blk.mesh = bm
		var mat := StandardMaterial3D.new()
		mat.albedo_color = [Color(1.0, 0.85, 0.3), Color(0.8, 0.8, 0.85), Color(0.8, 0.55, 0.3)][i]
		mat.emission_enabled = true
		mat.emission = mat.albedo_color
		mat.emission_energy_multiplier = 0.3
		blk.material_override = mat
		var slot_x: float = [0.0, -9.0, 9.0][i]
		blk.position = c0 + fright * slot_x + Vector3(0, heights[i] * 0.5 + 2.0, 0) + Vector3(0, 0, 0)
		add_child(blk)
		var kn: Node3D = (order[i] as Dictionary)["node"]
		kn.position = blk.position + Vector3(0, heights[i] * 0.5 + 1.2, 0)
		if _main != null and _main.has_method("_sparkle_burst"):
			_main._sparkle_burst(kn.position + Vector3(0, 3, 0), Color.from_hsv(randf(), 0.5, 1.0))
	# camera on the podium: back along the track axis so the three blocks read left-to-right
	if _cam != null:
		var pfwd: Vector3 = sf[1]
		_cam.position = c0 - pfwd * 28.0 + Vector3(0, 12.0, 0)
		if _ground_mode() == "terrain":
			_cam.position.y = maxf(_cam.position.y, _terrain_y(_cam.position.x, _cam.position.z) + 5.0)
		_cam.look_at(c0 + Vector3(0, 4.0, 0), Vector3.UP)
	var tw := create_tween()
	tw.tween_interval(3.6)
	tw.tween_callback(_teardown.bind(place))

func _teardown(place: int) -> void:
	# Covers explicit quit and any direct teardown caller. Both helpers are
	# idempotent, so the normal finish path cannot double-award anything.
	_commit_payout(_placement_bonus(place) if place > 0 else 0)
	if place > 0:
		_commit_completion(place)
	_state = "done"
	for n in _hidden_props:
		if is_instance_valid(n):
			(n as Node3D).visible = true
	_hidden_props.clear()
	if _prev_env != null and "we_node" in _main and _main.we_node != null:
		_main.we_node.environment = _prev_env
	if _player_node != null and "cam" in _player_node and _player_node.cam != null:
		(_player_node.cam as Camera3D).make_current()
	if _finish_cb.is_valid():
		_finish_cb.call(place)
	queue_free()
