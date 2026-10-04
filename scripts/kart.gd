extends Node2D
class_name KartGame

const CanvasPresenter := preload("res://scripts/kart_canvas_2d.gd")
const Driving := preload("res://scripts/kart_driving.gd")
# ============================================================================
# RACE ENGINE — Rainbow Road racer (N64-inspired) and a reusable arcade-racing
# base for future minigames.
#
# What the player gets:
#   * VEHICLE SELECT: motorcycle / go-kart / monster truck (real CC0/CC-BY
#     authored 2D source views), each handling differently.
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
#   laps:int, lap_target_sec:float, road_half:float, ctrl:Array[Vector2]
#   (loop control points), origin:Vector2, ctrl_height:Array, origin_height:float, racers:Array (see RACERS),
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
const LAPS := Driving.LAPS
const LAP_TARGET_SEC := 30.0       # vmax is derived from measured track length
const ROAD_HALF := 11.0
const COLLIDE_R := 4.5
const WALL_SLOW := 0.82
const SAMPLES := 260
const ORIGIN := Vector2.ZERO
const CTRL_HEIGHT := [0.0, 6.0, 18.0, 16.0, 4.0, -8.0, -6.0, 8.0, 22.0, 14.0, 0.0, 12.0]
const RAINBOW_HEIGHT := [8.0, 26.0, 44.0, 18.0, -6.0, -20.0, 2.0, 30.0, 46.0, 22.0, -12.0, -4.0]
const BOOST_MUL := Driving.BOOST_MUL
const TURBO_TIME := Driving.TURBO_TIME
const SELECT_TIMEOUT := 5.0        # short unattended path: two choices + countdown in about 14s

const CTRL := [
	Vector2(0, 150),
	Vector2(70, 132),
	Vector2(122, 72),
	Vector2(142, -8),
	Vector2(112, -78),
	Vector2(64, -120),
	Vector2(-8, -150),
	Vector2(-84, -118),
	Vector2(-138, -48),
	Vector2(-122, 26),
	Vector2(-70, 92),
	Vector2(-30, 132),
]
const SHORTCUT_FROM_U := 0.34
const SHORTCUT_TO_U := 0.50

# the rainbow road gets its own loop: a floating road doesn't have to hug a
# seabed, so it ROLLERCOASTERS — 66 units of climb and dive around the
# Butterfly World (owner: "track design is repetitive" — the two races now
# share nothing but the engine). Keeps every point 100+ units from the loop
# centre so the planet, moons and butterflies stay clear of the racing line.
const RAINBOW_CTRL := [
	Vector2(0, 158),
	Vector2(82, 138),
	Vector2(132, 66),
	Vector2(158, -12),
	Vector2(128, -86),
	Vector2(58, -132),
	Vector2(-18, -160),
	Vector2(-92, -126),
	Vector2(-142, -50),
	Vector2(-160, 34),
	Vector2(-118, 96),
	Vector2(-52, 148),
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
const SHELL_GEN2 := "spiralshell"

# Butterfly World centerpiece (rainbow theme): the Level-2 rainbow legs are the
# road TO stage 3, so the track orbits the Butterfly World itself — the same
# meadow planet, crystal castle and butterflies the player lands on in
# galaxy.gd — instead of circling empty starfield.
const BW_PLANET_R := 70.0
const BW_BUTTERFLY_CARDS := ["butterfly1", "butterfly2"]
const BW_WING_COLS := [Color(1.0, 0.5, 0.15), Color(0.25, 0.45, 1.0), Color(0.75, 1.0, 0.85), Color(1.0, 0.85, 0.3), Color(0.95, 0.35, 0.4), Color(0.6, 0.4, 1.0), Color(0.4, 0.8, 1.0)]
# ------------------------------------------------------------ vehicles
# handling: vmax (x base), steer (lat u/s), wall (speed kept on scrape),
# mass (collision shove weight), turbo (x BOOST_MUL), slip (lat drift keep),
# scale/y_off/yaw_fix (legacy handling metadata), blurb (select screen)
const VEHICLES := {
	# tuned by simulation (200k-token stress campaign): each ride has a REAL
	# identity — moto = raw speed but fragile, kart = turbo economy, truck =
	# bumper king (mass WINS every collision, walls barely slow it).
	"moto": {
		"label": "Zoom Cycle", "blurb": "PRO: fastest + super steering / CON: so light, bumps toss it!",
		"vmax": 1.08, "steer": 30.0, "wall": 0.62, "mass": 0.6,
		"turbo": 1.2, "slip": 0.45, "size": 5.0, "yaw_fix": 0.0,
		"lean": 0.5,
	},
	"kart": Driving.KART_HANDLING,
	"truck": {
		"label": "Monster Truck", "blurb": "PRO: BUMPER KING - shove everyone, walls can't stop it / CON: slowest",
		"vmax": 0.985, "steer": 16.0, "wall": 0.97, "mass": 2.2,
		"turbo": 0.9, "slip": 0.0, "size": 7.5, "yaw_fix": PI,
		"lean": 0.05,
	},
}
const VEHICLE_ORDER := ["moto", "kart", "truck"]

# paint jobs (second step of the select screen). "rainbow" cycles only the paint trim.
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
# Daddy Mermaid, Wacky & Chuck, Evie & Lamb-a') — seeing them race past themselves
# standing in the ocean broke the fiction. These characters live in the toy
# nursery / story world instead, so they never appear twice at once.
const RACERS := [
	{"name": "Roshan", "col": Color(1.0, 0.4, 0.8), "sprite": "res://assets/characters/roshan_25d/roshan_base.png", "player": true},
	{"name": "Sparkle", "col": Color(1.0, 0.85, 0.35), "sprite": "res://assets/characters/companions/baby_eagle.png"},
	{"name": "Princess Huluu", "col": Color(0.75, 0.55, 1.0), "sprite": "res://assets/characters/friends/huluu.png"},
	{"name": "Bunny", "col": Color(0.95, 0.95, 1.0), "sprite": "res://assets/book/doll_bunny.png"},
	{"name": "Kitty", "col": Color(1.0, 0.6, 0.4), "sprite": "res://assets/book/doll_cat.png"},
	{"name": "Baby Doll", "col": Color(0.45, 0.85, 1.0), "sprite": "res://assets/book/baby_doll.png"},
	{"name": "Dolly", "col": Color(0.6, 1.0, 0.7), "sprite": "res://assets/book/baby_doll2.png"},
	{"name": "Sleepy", "col": Color(0.8, 0.7, 1.0), "sprite": "res://assets/book/baby_doll3.png"},
]

# ------------------------------------------------------------ state
var _main: Node = null
var _finish_cb: Callable
var _hud: CanvasLayer = null
var _hud_root: Control = null
var _ride_choice_buttons: Array[Button] = []
var _paint_choice_buttons: Array[Button] = []
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

var _lut: PackedVector2Array = []
var _cum: PackedFloat32Array = []
var _len := 0.0
var _vmax := 40.0

var _karts: Array = []
var _pl = null
var _strip_data: Array = []
var _ramp_data: Array = []         # jump pads: {pos: Vector2, height: float}
var _pickups_live: Array = []
var _pearls_live: Array = []
var _state := "select"             # select -> countdown -> race -> podium -> done
var _clock := 0.0
var _race_t := 0.0
var _shortcut_used_lap := -1
var _rev := false
var _pearls_got := 0
var _player_acted := false
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


# Presentation is Canvas-only. Height is a scalar road/contact measurement,
# retained from the original course; it is never a spatial scene or model.
var _canvas: Control
var _height_lut: PackedFloat32Array = []
var _kap: PackedFloat32Array = []
var _hazards_live: Array = []
var _hidden_props: Array = []
var _shake := 0.0
var _thunk_cool := 0.0
var _touch_t := 0.0
var _flash_t := 0.0
var _eng: AudioStreamPlayer = null
var _eng_pb: AudioStreamGeneratorPlayback = null
var _eng_phase := 0.0
const DRIFT_TIERS := Driving.DRIFT_TIERS
const DRIFT_BOOST := Driving.DRIFT_BOOST
const DRIFT_COLS := [Color(1, 1, 1), Color(0.85, 0.9, 1.0), Color(1.0, 0.85, 0.3), Color(1.0, 0.5, 0.9)]
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

func _minimal() -> bool:
	# opera career races run wordless: the child cannot read, and the career
	# worlds are full-screen art — icons and sparkle FX carry everything
	return bool(_cv("minimal_hud", false))

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

func _catmull(p0: Vector2, p1: Vector2, p2: Vector2, p3: Vector2, t: float) -> Vector2:
	var t2 := t * t
	var t3 := t2 * t
	return 0.5 * ((2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2 + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3)

func _ctrl_pts() -> Array:
	# the floating rainbow race rides its own rollercoaster loop; the seabed
	# race keeps the terrain-hugging line (its shape comes from the reef)
	var dflt: Array = RAINBOW_CTRL if (_theme() == "rainbow" and _ground_mode() == "float") else CTRL
	return _cv("ctrl", dflt)

func _origin() -> Vector2:
	return _cv("origin", ORIGIN)

func _ctrl_heights() -> Array:
	var defaults: Array = RAINBOW_HEIGHT if (_theme() == "rainbow" and _ground_mode() == "float") else CTRL_HEIGHT
	return _cv("ctrl_height", defaults)

func _height_u(u: float) -> float:
	var pts := _ctrl_heights()
	var n := pts.size()
	var f: float = fposmod(u, 1.0) * float(n)
	var i := int(floor(f))
	var t: float = f - float(i)
	var p0: float = float(pts[(i - 1 + n) % n])
	var p1: float = float(pts[i % n])
	var p2: float = float(pts[(i + 1) % n])
	var p3: float = float(pts[(i + 2) % n])
	return float(_cv("origin_height", 4000.0)) + 0.5 * ((2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t * t + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t * t * t)

func _spline_u(u: float) -> Vector2:
	var pts: Array = _ctrl_pts()
	var n := pts.size()
	var f: float = fposmod(u, 1.0) * float(n)
	var i: int = int(floor(f))
	var t: float = f - float(i)
	var p0: Vector2 = pts[(i - 1 + n) % n]
	var p1: Vector2 = pts[i % n]
	var p2: Vector2 = pts[(i + 1) % n]
	var p3: Vector2 = pts[(i + 2) % n]
	var p := _origin() + _catmull(p0, p1, p2, p3, t)
	return p

func _build_lut() -> void:
	_lut = PackedVector2Array()
	_height_lut = PackedFloat32Array()
	for i in range(SAMPLES + 1):
		var u: float = float(i) / float(SAMPLES)
		var p := _spline_u(u)
		_lut.append(p)
		_height_lut.append(_terrain_y(p.x, p.y) + 1.4 if _ground_mode() == "terrain" else _height_u(u))
	if _ground_mode() == "terrain":
		var raw := _height_lut.duplicate()
		for i in range(SAMPLES + 1):
			var acc := 0.0
			for w in range(-4, 5):
				acc += raw[(i + w + SAMPLES) % SAMPLES]
			_height_lut[i] = acc / 9.0
	_cum = PackedFloat32Array()
	var d := 0.0
	for i in range(SAMPLES + 1):
		if i > 0:
			var dh: float = _height_lut[i] - _height_lut[i - 1]
			d += sqrt(_lut[i - 1].distance_squared_to(_lut[i]) + dh * dh)
		_cum.append(d)
	_len = d
	_vmax = _len / float(_cv("lap_target_sec", LAP_TARGET_SEC))
	_kap = PackedFloat32Array()
	_kap.resize(SAMPLES + 1)
	for i in range(SAMPLES + 1):
		var a := _tangent_metric(_cum[i] - 6.0)
		var b := _tangent_metric(_cum[i] + 6.0)
		var ap: Vector2 = a[0]
		var bp: Vector2 = b[0]
		_kap[i] = signf(-ap.cross(bp)) * acos(clampf(ap.dot(bp) + float(a[1]) * float(b[1]), -1.0, 1.0)) / 12.0

func _height_at(s: float) -> float:
	var ss := fposmod(s, _len)
	var i: int = clampi(_cum.bsearch(ss) - 1, 0, SAMPLES - 1)
	var seg: float = _cum[i + 1] - _cum[i]
	var t: float = 0.0 if seg <= 0.0001 else (ss - _cum[i]) / seg
	return lerpf(_height_lut[i], _height_lut[i + 1], t)

func _tangent_metric(s: float) -> Array:
	var plane := _pos_at(s + 3.0) - _pos_at(s - 3.0)
	var rise := _height_at(s + 3.0) - _height_at(s - 3.0)
	var length := sqrt(plane.length_squared() + rise * rise)
	return [plane / maxf(0.001, length), rise / maxf(0.001, length)]

func _pos_at(s: float) -> Vector2:
	var ss := fposmod(s, _len)
	# binary search (bsearch = first index with _cum[i] >= ss, so the segment
	# is i-1) — this is the hottest function in the engine; the old linear walk
	# cost O(SAMPLES) per call, dozens of times a frame on the phone
	var i: int = clampi(_cum.bsearch(ss) - 1, 0, SAMPLES - 1)
	var seg: float = _cum[i + 1] - _cum[i]
	var t: float = 0.0 if seg <= 0.0001 else (ss - _cum[i]) / seg
	return _lut[i].lerp(_lut[i + 1], t)

func _tangent_at(s: float) -> Vector2:
	var a := _pos_at(s - 3.0)
	var b := _pos_at(s + 3.0)
	var dir := b - a
	if dir.length() < 0.001:
		return Vector2.UP
	return dir.normalized()

func _width_at(s: float) -> float:
	var u := fposmod(s, _len) / _len
	return _rhalf() * (1.0 + 0.32 * sin(u * TAU * 2.0))

func _bank_at(s: float) -> float:
	var a := _tangent_metric(s - 10.0)
	var b := _tangent_metric(s + 10.0)
	return clampf(-(a[0] as Vector2).cross(b[0]) * 4.0, -0.4, 0.4)

func _frame_at(s: float, lat: float) -> Array:
	return _track_frame(s, lat, false)

func _track_frame(s: float, lat: float, reverse: bool) -> Array:
	var metric := _tangent_metric(s)
	var plane: Vector2 = metric[0]
	var rise: float = metric[1]
	var bank := _bank_at(s)
	if reverse:
		plane = -plane
		rise = -rise
		bank = -bank
	var flat: float = maxf(0.001, plane.length())
	var side := Vector2(-plane.y, plane.x) / flat
	var right := side * cos(bank) + plane * (rise / flat) * sin(bank)
	var up := Vector2(-plane.y, plane.x) * sin(bank) + plane * rise * (1.0 - cos(bank))
	var right_height := -flat * sin(bank)
	var up_height := cos(bank) + rise * rise * (1.0 - cos(bank))
	return [_pos_at(s) + right * lat, plane.normalized(), right, up, _height_at(s) + right_height * lat, up_height]

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
	Driving.advance(k, _curv_at(float(k["s"])), delta)

func _kart_frame(s: float, lat: float) -> Array:
	return _track_frame(_eff(s), lat, _rev)

func _set_contact(node: Node2D, frame: Array, height_offset: float = 0.0) -> void:
	node.position = frame[0]
	node.set_meta("height", float(frame[4]) + height_offset)

func _point_distance(node: Node2D, point: Vector2, height: float) -> float:
	var dh: float = float(node.get_meta("height", height)) - height
	return sqrt(node.position.distance_squared_to(point) + dh * dh)

func _contact_distance(a: Node2D, b: Node2D) -> float:
	return _point_distance(a, b.position, float(b.get_meta("height", 0.0)))

func _burst(point: Vector2, color: Color) -> void:
	if _canvas != null:
		_canvas.call("burst", point, color)

func start(main: Node, finish_cb: Callable, reversed_track: bool = false) -> void:
	_main = main
	if _main.has_method("_navigation_push"):
		_main.call("_navigation_push", "kart_race", self,
			Callable(self, "_quit_race"))
	_finish_cb = finish_cb
	_rev = reversed_track
	_player_acted = bool(_cv("assume_acted", false))
	_payout_banked = 0
	_payout_dirty = false
	_completion_committed = false
	_rocket_armed = false
	_select_confirm_queued = false
	_build_lut()
	var canvas_layer := CanvasLayer.new()
	canvas_layer.layer = 17
	add_child(canvas_layer)
	_canvas = CanvasPresenter.new()
	canvas_layer.add_child(_canvas)
	_canvas.call("setup", self)
	if bool(_cv("shortcut", true)):
		_build_shortcut()
	_build_strips()
	_build_pickups()
	_build_pearls()
	_build_ramps()
	_build_hazards()
	_build_engine()
	_build_hud()
	_build_select()
	_build_select_controls()
	_state = "select"
	_sel_t = 0.0

func _notification(what: int) -> void:
	# Android normally sends a pause notification before the process can be
	# evicted. Bank the pearls already collected at that point; the incremental
	# payout helper will add only the remainder and finish bonus if play resumes.
	if what == NOTIFICATION_APPLICATION_PAUSED and _player_acted and _main != null and (_payout_dirty or _pearls_got > _payout_banked):
		_commit_payout(0)

func _sky_defaults() -> Array:
	if _theme() == "ocean":
		return [Color(0.01, 0.08, 0.14), Color(0.06, 0.30, 0.42)]
	return [Color(0.02, 0.01, 0.06), Color(0.10, 0.04, 0.20)]

func _build_shortcut() -> void:
	var frame := _frame_at(SHORTCUT_FROM_U * _len, _rhalf() * 0.78)
	set_meta("gate_pos", frame[0])
	set_meta("gate_height", frame[4])

func _build_strips() -> void:
	var table: Array = _cv("strips", STRIPS)
	for sd in table:
		var s0: float = float(sd["u"]) * _len
		var fr := _frame_at(s0 + float(sd["len"]) * 0.5, float(sd["lat"]))
		_strip_data.append({"pos": (fr[0] as Vector2) + (fr[3] as Vector2), "height": float(fr[4]) + float(fr[5]), "len": float(sd["len"]), "hw": float(sd["hw"]), "s": s0, "lat": float(sd["lat"])})

func _build_pickups() -> void:
	var table: Array = _cv("pickups", PICKUPS)
	for pd in table:
		var s0: float = float(pd["u"]) * _len
		var holder := Node2D.new()
		_set_contact(holder, _frame_at(s0, float(pd["lat"])), 2.6)
		add_child(holder)
		_pickups_live.append({"node": holder, "s": s0, "lat": float(pd["lat"]), "kind": String(pd["kind"]), "cool": 0.0})

func _build_ramps() -> void:
	var table: Array = _cv("ramps", RAMPS)
	for rd in table:
		var s0: float = float(rd["u"]) * _len
		var fr := _frame_at(s0, float(rd["lat"]))
		_ramp_data.append({"pos": fr[0], "height": fr[4], "s": s0, "lat": float(rd["lat"])})

func _check_ramps() -> void:
	for rd in _ramp_data:
		for k in _karts:
			if float(k.get("air_t", 0.0)) > 0.0:
				continue
			if _point_distance(k["node"], rd["pos"], float(rd["height"])) < 6.0:
				k["air_t"] = AIR_DUR
				if bool(k["is_player"]):
					_chime(1.15)
					_flash_big("WHEEE!")

func _hazard_table() -> Array:
	return _cv("hazards", HAZARDS_OCEAN if _theme() == "ocean" else HAZARDS_RAINBOW)

func _build_hazards() -> void:
	for hd in _hazard_table():
		var s0: float = float(hd["u"]) * _len
		var w := _width_at(s0)
		var kind := String(hd["kind"])
		var h := {"kind": kind, "s": s0, "w": w, "ph": s0 * 0.13, "lat": 0.0}
		var holder := Node2D.new()
		add_child(holder)
		h["node"] = holder
		if kind == "comet":
			h["side"] = 1.0 if int(s0) % 2 == 0 else -1.0
		elif kind == "whirl":
			h["lat"] = w * 0.35 * (1.0 if int(s0) % 2 == 0 else -1.0)
		elif kind == "jelly":
			h["lat"] = w * 0.4 * (1.0 if int(s0) % 2 == 0 else -1.0)
		_set_contact(holder, _frame_at(s0, float(h["lat"])), 0.15 if kind == "whirl" else 0.0)
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
		var node: Node2D = h["node"]
		match kind:
			"crab":
				h["lat"] = sin(tt * 0.55 + float(h["ph"])) * (w - 2.5)
				var fr := _frame_at(s0, float(h["lat"]))
				_set_contact(node, fr, 0.3 + absf(sin(tt * 6.0)) * 0.3)
				node.rotation = tt * 0.8
				if racing:
					for k in _karts:
						if _contact_distance(k["node"], node) < 3.4:
							_hazard_bonk(k, 0.75, signf(float(k["lat"]) - float(h["lat"])))
			"pendulum":
				h["lat"] = sin(tt * 1.1 + float(h["ph"])) * (w - 2.0)
				var fr2 := _frame_at(s0, float(h["lat"]))
				_set_contact(node, fr2, 1.6)
				if racing:
					for k in _karts:
						if _contact_distance(k["node"], node) < 3.6:
							_hazard_bonk(k, 0.75, signf(float(k["lat"]) - float(h["lat"])))
			"geyser":
				var cyc: float = fposmod(tt + float(h["ph"]), 4.2)
				var erupting: bool = cyc < 1.4
				h["erupting"] = erupting
				var frg := _frame_at(s0, 0.0)
				_set_contact(node, frg)
				# pre-cue: the mound quivers half a second before it blows
				node.scale = Vector2.ONE * (1.0 + (0.18 * sin(tt * 30.0) if cyc > 3.7 else 0.0))
				if racing and erupting:
					for k in _karts:
						if float(k.get("air_t", 0.0)) > 0.0:
							continue
						if _contact_distance(k["node"], node) < 4.5:
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
					_set_contact(node, frx, 1.5)
					node.visible = true
					node.scale = Vector2.ONE
					node.rotation = tt * 5.0   # tumbling rock
					if racing:
						for k in _karts:
							if _contact_distance(k["node"], node) < 3.6:
								_hazard_bonk(k, 0.7, -side)
				elif ccyc >= 3.1:
					h["lat"] = side * (w + 9.0)
					var fre := _frame_at(s0, float(h["lat"]))
					_set_contact(node, fre, 1.5)
					node.visible = true
					node.scale = Vector2.ONE * (1.0 + 0.22 * absf(sin(tt * 12.0)))
				else:
					node.visible = false
			"whirl":
				# fixed position (set at build); the pull is the hazard
				if racing:
					for k in _karts:
						if float(k.get("air_t", 0.0)) > 0.0:
							continue
						if _contact_distance(k["node"], node) < 6.5:
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
				node.scale = Vector2(1.0 + wob * sin(tt * 6.0), 1.0 - wob * sin(tt * 6.0))
				if racing:
					for k in _karts:
						if float(k.get("haz_cool", 0.0)) > 0.0 or float(k.get("air_t", 0.0)) > 0.0:
							continue
						if _contact_distance(k["node"], node) < 3.9:
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
					_set_contact(node, frc, 1.2)
				if racing:
					var rad: float = 7.5 if kind == "kelp" else 5.5
					for k in _karts:
						if _contact_distance(k["node"], node) < rad:
							# drag, not a stop — and a burning turbo powers through
							if float(k["boost_t"]) <= 0.0:
								k["speed"] = maxf(float(k["speed"]) * (1.0 - 1.5 * delta), _vmax * 0.5)

func _build_pearls() -> void:
	var rows: Array = _cv("pearl_rows", PEARL_ROWS)
	for row in rows:
		var s0: float = float(row["u"]) * _len
		for j in range(int(row["n"])):
			var pearl := Node2D.new()
			var s: float = s0 + float(j) * 6.0
			_set_contact(pearl, _frame_at(s, float(row["lat"])), 2.0)
			add_child(pearl)
			_pearls_live.append({"node": pearl, "got": false})

func _vehicle_body(vkey: String, col: Color, sprite_path: String, racer_name: String, paint: Dictionary = {}) -> Node2D:
	var node := Node2D.new()
	node.set_meta("vehicle", vkey)
	node.set_meta("color", col)
	node.set_meta("sprite_path", sprite_path)
	node.set_meta("racer_name", racer_name)
	_apply_paint(node, paint)
	return node

func _apply_paint(root: Node, paint: Dictionary) -> void:
	root.set_meta("paint", paint.duplicate())

func _vehicles_table() -> Dictionary:
	return _cv("vehicles", VEHICLES)

func _vehicle_keys() -> Array:
	# configure() documents `vehicles` as overridable, but VEHICLE_ORDER is a
	# const, so a caller offering a subset could make _build_select and the AI
	# roster index a key the table does not have. Order by VEHICLE_ORDER where
	# possible, then honour
	# whatever the table actually holds.
	var table := _vehicles_table()
	var keys: Array = []
	for k: String in VEHICLE_ORDER:
		if table.has(k):
			keys.append(k)
	for k2 in table.keys():
		if not keys.has(k2):
			keys.append(k2)
	return keys if not keys.is_empty() else VEHICLE_ORDER

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
			var vkeys := _vehicle_keys()
			vkey = String(vkeys[idx % vkeys.size()])
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

func _build_select() -> void:
	var order := _vehicle_keys()
	for i in range(order.size()):
		var slot := Node2D.new()
		add_child(slot)
		var body := _vehicle_body(String(order[i]), Color.WHITE, "", "")
		slot.add_child(body)
		_sel_nodes.append({"slot": slot, "body": body})
	_lbl_big.text = "" if _minimal() else "Pick your ride!"
	_lbl_big.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	_lbl_hint.text = "" if _minimal() else ("slide a finger to choose • TAP to GO!" if _touch_device() else "LEFT/RIGHT to choose • SPACE or A to GO!")
	_set_guide_mode("steer")
	if _main != null and _main.has_method("_say"):
		_main._say("roshan", "intro4", 10.0)

func _build_select_controls() -> void:
	if _hud_root == null:
		return
	var order := _vehicle_keys()
	for i in range(order.size()):
		var vehicle_key: String = String(order[i])
		var button := Button.new()
		button.name = "KartRideChoice_" + vehicle_key
		button.text = ""
		button.position = Vector2(188.0 + float(i) * 302.0, 264.0)
		button.custom_minimum_size = Vector2(278.0, 430.0)
		button.size = Vector2(278.0, 430.0)
		button.pressed.connect(_choose_ride_by_touch.bind(i))
		_hud_root.add_child(button)
		_ride_choice_buttons.append(button)
	for i in range(PAINTS.size()):
		var paint: Dictionary = PAINTS[i]
		var swatch := Button.new()
		swatch.name = "KartPaintChoice_%d" % i
		swatch.position = Vector2(132.0 + float(i) * 126.0, 574.0)
		swatch.custom_minimum_size = Vector2(112.0, 112.0)
		swatch.size = Vector2(112.0, 112.0)
		swatch.tooltip_text = String(paint["label"])
		swatch.text = "*" if bool(paint.get("rainbow", false)) else ""
		swatch.pressed.connect(_choose_paint_by_touch.bind(i))
		_hud_root.add_child(swatch)
		_paint_choice_buttons.append(swatch)
	_refresh_select_controls()

func _choose_ride_by_touch(index: int) -> void:
	if _state != "select" or _sel_phase != "ride":
		return
	_sel_idx = clampi(index, 0, _vehicle_keys().size() - 1)
	_select_confirm_queued = true
	_refresh_select_controls()

func _choose_paint_by_touch(index: int) -> void:
	if _state != "select" or _sel_phase != "paint":
		return
	_paint_idx = clampi(index, 0, PAINTS.size() - 1)
	_select_confirm_queued = true
	_refresh_select_controls()

func _paint_choice_fill(index: int) -> Color:
	var paint: Dictionary = PAINTS[index]
	if bool(paint.get("rainbow", false)):
		return StorybookUI.LILAC
	var color_value: Variant = paint.get("col")
	return StorybookUI.PAPER if color_value == null else Color(color_value)

func _refresh_select_controls() -> void:
	for i in range(_ride_choice_buttons.size()):
		var selected: bool = i == _sel_idx
		var ride_button: Button = _ride_choice_buttons[i]
		ride_button.visible = _state == "select" and _sel_phase == "ride"
		# The Canvas picture/footer is the visible button; the native Button
		# owns the same complete target, without painting over its artwork.
		for role in ["normal", "hover", "pressed", "focus"]:
			ride_button.add_theme_stylebox_override(role, StyleBoxEmpty.new())
		ride_button.set_meta("selected", selected)
		ride_button.set_meta("picture_context", "authored_2d_vehicle")
	for i in range(_paint_choice_buttons.size()):
		var paint_selected: bool = i == _paint_idx
		var paint_button: Button = _paint_choice_buttons[i]
		paint_button.visible = _state == "select" and _sel_phase == "paint"
		StorybookUI.style_picture_button(paint_button, _paint_choice_fill(i),
			StorybookUI.GOLD if paint_selected else StorybookUI.PURPLE, 52,
			StorybookUI.ROLE_DECORATIVE_GLYPH, 58)
		paint_button.set_meta("selected", paint_selected)

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
	# Swatch Buttons carry the choices; the Canvas renders the selected ride.
	pass

func _tick_select(delta: float) -> void:
	_sel_t += delta
	_refresh_select_controls()
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
			_sel_idx = clampi(_sel_idx + edge, 0, _vehicle_keys().size() - 1)
		if confirm or _sel_t > SELECT_TIMEOUT:
			_sel_phase = "paint"
			_sel_t = 0.0
			_paint_prev = -1
			_build_paint_row()
			_lbl_big.text = "" if _minimal() else "Pick your paint!"
		return
	# ---- paint phase ----
	var np := PAINTS.size()
	if edge != 0:
		_paint_idx = (_paint_idx + edge + np) % np
	if _paint_idx != _paint_prev:
		_paint_prev = _paint_idx
		_apply_paint((_sel_nodes[_sel_idx] as Dictionary)["body"], PAINTS[_paint_idx])
		var confirm_hint := "TAP to GO!" if _touch_device() else "SPACE or A to GO!"
		_lbl_hint.text = "" if _minimal() else (String((PAINTS[_paint_idx] as Dictionary)["label"]) + "  •  " + confirm_hint)
	if confirm or _sel_t > SELECT_TIMEOUT:
		var vkey: String = String(_vehicle_keys()[_sel_idx])
		var paint: Dictionary = PAINTS[_paint_idx]
		for sn2 in _sel_nodes:
			(sn2["slot"] as Node2D).queue_free()
		_sel_nodes.clear()
		_paint_orbs.clear()
		_build_karts(vkey, paint)
		_state = "countdown"
		_refresh_select_controls()
		_clock = 3.999
		_lbl_big.text = ""
		_lbl_hint.text = "" if _minimal() else ("drag left/right to steer  •  TAP = TURBO when the bar is full!" if _touch_device() else "steer with LEFT/RIGHT  •  SPACE or A = TURBO!")
		_meter_bg.visible = true
		_set_guide_mode("action")
		# put the whole pack ON the grid right now (nodes used to sit at the
		# world origin until the first race frame — the countdown showed an
		# empty road) and SNAP the camera behind Roshan: the old 1s glide from
		# the podium shot passed nose-first through the Butterfly World
		# backdrop, so every race opened on a washed-out planet close-up
		for k2 in _karts:
			_place_kart(k2, 0.0)
		_lbl_big.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		_update_camera(1.0)

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

func _process(delta: float) -> void:
	if _state == "done":
		return
	_tick_guide(delta)
	_tick_hazards(delta)
	if _canvas != null:
		_canvas.queue_redraw()
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
				_player_acted = true
				_pl["boost_t"] = 0.9
				_pl["squash"] = 0.3
				_chime(1.25)
				_flash_big("ROCKET START!")
			_rocket_armed = false
			if _main != null and _main.has_method("_say"):
				_main._say("roshan", "kart_rocket_start", 10.0)
		for k0 in _karts:
			_place_kart(k0, delta)   # pack idles ON the grid through 3-2-1
		_tick_engine()   # idle rumble builds anticipation through the count
		_update_camera(delta)
		return

	_race_t += delta
	var steer := _steer_input()
	var braking := _brake_input()
	var fired := _fire_just()
	var acted_now: bool = absf(steer) > 0.05 or braking or fired
	if acted_now and not _player_acted:
		_player_acted = true
		# Pearls swept up by auto-cruise become earned only when Roshan performs
		# a deliberate race verb. Bank that pending progress at the first input.
		_commit_payout(0)

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
	# Preserve the existing auto-fire announcement; scalar charge/fire state is
	# shared with the Opera circuit, while this presenter still owns its FX.
	var auto_flash := float(k["meter"]) >= 0.99 \
		and maxf(0.0, float(k["boost_t"]) - delta) <= 0.0 \
		and float(k.get("full_t", 0.0)) + delta >= (0.2 if _touch_t > 0.0 else 2.5)
	if auto_flash:
		_flash_big("TURBO!")
	if Driving.tick_turbo(k, vd, fired, _touch_t > 0.0, delta):
		_shake = maxf(_shake, 0.2)
		_chime(0.7)
		if _canvas != null:
			_burst((k["node"] as Node2D).position, Color(0.5, 1.0, 1.0))
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
	Driving.accelerate(k, target, boosting, delta)
	_advance(k, delta)
	# ---- SPARKLE DRIFT (the kart-class skill ceiling, one thumb) ----
	# hold a hard steer INTO a bend for a beat to start carving; hold the carve
	# to charge SILVER -> GOLD -> RAINBOW; ease off and the charge releases as
	# turbo. Zero input still finishes the race — this only raises the ceiling.
	var drift_event := Driving.tick_drift(k, steer, _curv_at(float(k["s"])), delta)
	if bool(drift_event["entered"]):
		_chime(1.05)
	if bool(k.get("drift", false)):
		if bool(drift_event["release"]):
			_drift_release(k)
		else:
			var tier := _drift_tier(float(k["drift_t"]))
			if bool(drift_event["tier_up"]):
				_chime(0.95 + 0.12 * float(tier))
			_drift_spray(k, tier)
	var slip: float = float(vd["slip"])
	_touch_t = maxf(0.0, _touch_t - delta)
	var want_v := Driving.steering_target(k, vd, steer,
		_width_at(_eff(float(k["s"]))) - 1.6, _touch_t > 0.0)
	Driving.steer_velocity(k, want_v, slip, delta)
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
	var pos: Vector2 = fr[0]
	var fwd: Vector2 = fr[1]
	var node: Node2D = k["node"]
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
				if _canvas != null:
					_burst(node.position, Color(1.0, 0.9, 0.4))
	k["haz_cool"] = maxf(0.0, float(k.get("haz_cool", 0.0)) - delta)
	node.position = pos + (fr[3] as Vector2) * (1.2 + hop_h + air_h)
	node.set_meta("height", float(fr[4]) + float(fr[5]) * (1.2 + hop_h + air_h))
	k["lift"] = hop_h + air_h
	var spin_t: float = float(k.get("spin_t", 0.0))
	if spin_t > 0.0:
		spin_t = maxf(0.0, spin_t - delta)
		k["spin_t"] = spin_t
	var yaw: float = clampf(float(k["latv"]) * 0.030, -0.55, 0.55)
	if bool(k.get("drift", false)):
		yaw += float(k.get("drift_dir", 0.0)) * 0.30
	node.rotation = fwd.angle() + yaw + ((1.0 - spin_t / 0.6) * TAU if spin_t > 0.0 else 0.0)
	# squash & stretch pulse on impacts (bouncy!)
	var sq: float = float(k.get("squash", 0.0))
	if sq > 0.0:
		sq = maxf(0.0, sq - delta)
		k["squash"] = sq
		var pulse: float = sin((0.3 - sq) / 0.3 * PI) * (sq / 0.3 + 0.4)
		node.scale = Vector2(1.0 + 0.16 * pulse, 1.0 - 0.10 * pulse)
	elif node.scale != Vector2.ONE:
		node.scale = node.scale.lerp(Vector2.ONE, minf(1.0, delta * 12.0))

func _charge(k: Dictionary, amt: float) -> void:
	# the Rainbow Kart's "mcharge" makes every pickup worth 30% more meter
	Driving.charge(k, _veh(k), amt)

func _drift_tier(t: float) -> int:
	return Driving.drift_tier(t)

func _drift_spray(k: Dictionary, tier: int) -> void:
	k["spray_tier"] = tier

func _drift_release(k: Dictionary) -> void:
	var tier := Driving.release_drift(k)
	if tier <= 0:
		return
	_shake = maxf(_shake, 0.12)
	_chime(1.0 + 0.15 * float(tier))
	if _canvas != null:
		_burst((k["node"] as Node2D).position, DRIFT_COLS[tier])
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

func _flash_big(txt: String) -> void:
	if _minimal():
		return
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
		var kn: Node2D = k["node"]
		for sd in _strip_data:
			if _point_distance(kn, sd["pos"], float(sd.get("height", kn.get_meta("height", 0.0)))) < float(sd["len"]) * 0.6 + 3.0:
				# strips: small instant zip + meter charge
				if float(k["boost_t"]) < 0.35:
					k["boost_t"] = 0.35
				_charge(k, 0.60 * delta)

func _check_pickups(delta: float) -> void:
	if _pl == null:
		return
	var pn: Node2D = _pl["node"]
	var t: float = Time.get_ticks_msec() / 1000.0
	for pu in _pickups_live:
		var node: Node2D = pu["node"]
		_set_contact(node, _frame_at(float(pu["s"]), float(pu["lat"])), 2.6 + sin(t * 2.0 + float(pu["s"])) * 0.5)
		if float(pu["cool"]) > 0.0:
			pu["cool"] = float(pu["cool"]) - delta
			if float(pu["cool"]) <= 0.0:
				node.visible = true
			continue
		# touch magnet: sim showed phone thumbs miss pickups (boost uptime ~10
		# points under pad) — widen the grab so the fun stays platform-fair
		if _contact_distance(node, pn) < (8.5 if _touch_t > 0.0 else 6.5):
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
			if _canvas != null:
				_burst(pn.position, col)

func _check_pearls() -> void:
	if _pl == null:
		return
	var pn: Node2D = _pl["node"]
	for pd in _pearls_live:
		if bool(pd["got"]):
			continue
		var node: Node2D = pd["node"]
		if _contact_distance(node, pn) < (6.0 if _touch_t > 0.0 else 4.5):
			pd["got"] = true
			node.visible = false
			_pearls_got += 1
			if _player_acted:
				_commit_payout(0)   # zero-lost-progress after deliberate participation
			_charge(_pl, 0.05)
			_chime(0.8 + 0.02 * float(_pearls_got % 8))
			if _canvas != null:
				_burst(node.position, Color(1.0, 0.8, 1.0))

func _check_shortcut() -> void:
	if _rev or _pl == null or not has_meta("gate_pos"):
		return
	var lap: int = int(float(_pl["s"]) / _len)
	if lap == _shortcut_used_lap:
		return
	var gate: Vector2 = get_meta("gate_pos")
	var pn: Node2D = _pl["node"]
	if _point_distance(pn, gate, float(get_meta("gate_height")) + 1.2) < 7.0:
		_shortcut_used_lap = lap
		var base: float = float(lap) * _len
		_pl["s"] = base + SHORTCUT_TO_U * _len
		_pl["boost_t"] = maxf(float(_pl["boost_t"]), 0.9)
		if _canvas != null:
			_burst(pn.position, Color(0.5, 1.0, 0.8))

func _resolve_collisions() -> void:
	for i in range(_karts.size()):
		for j in range(i + 1, _karts.size()):
			var a: Dictionary = _karts[i]
			var b: Dictionary = _karts[j]
			var an: Node2D = a["node"]
			var bn: Node2D = b["node"]
			var d: float = _contact_distance(an, bn)
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

func _build_engine() -> void:
	if _speedy():
		return   # per-frame buffer fill is CPU the budget tier doesn't have
	_eng = AudioStreamPlayer.new()
	_eng.bus = "SFX"
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

func _update_camera(delta: float) -> void:
	if _canvas != null:
		_canvas.call("follow", delta)
	_shake = maxf(0.0, _shake - delta)
	_thunk_cool = maxf(0.0, _thunk_cool - delta)

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
	var holder := Control.new()
	holder.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	holder.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hud.add_child(holder)
	var root := StorybookUI.add_stage(holder, get_viewport().get_visible_rect().size)
	_hud_root = root
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	get_viewport().size_changed.connect(_sync_hud_stage)
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
	_lbl_hint.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	_lbl_hint.offset_left = 24.0
	_lbl_hint.offset_top = -56.0
	_lbl_hint.offset_right = -24.0
	_lbl_hint.offset_bottom = -12.0
	# turbo meter (bottom centre)
	_meter_bg = ColorRect.new()
	_meter_bg.mouse_filter = Control.MOUSE_FILTER_IGNORE   # "TAP for TURBO!!" points right at it
	_meter_bg.color = Color(0, 0, 0, 0.45)
	_meter_bg.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	_meter_bg.offset_left = -180.0
	_meter_bg.offset_top = -96.0
	_meter_bg.offset_right = 180.0
	_meter_bg.offset_bottom = -66.0
	_meter_bg.visible = false   # shown when the race starts
	root.add_child(_meter_bg)
	_meter_fill = ColorRect.new()
	_meter_fill.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_meter_fill.color = Color(0.3, 0.95, 1.0)
	_meter_fill.position = Vector2(3, 3)
	_meter_fill.size = Vector2(0, 24)
	_meter_bg.add_child(_meter_fill)

func _quit_race() -> void:
	if _state == "podium" or _state == "done":
		return   # already finishing — let the podium payout complete instead
	_player_acted = true
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
	if _minimal():
		_lbl_lap.text = ""
		_lbl_place.text = ""
		_lbl_pearls.text = ""
		_lbl_hint.text = ""
	if rdy:
		_set_guide_mode("action")
	elif _race_t < 7.0:
		_set_guide_mode("steer")
	else:
		_set_guide_mode("")

func _finish() -> void:
	if _pl != null:
		_drift_cancel(_pl)   # stop the tail spray before the podium
	_state = "podium"
	var place := _placement()
	var suffix: String = ["st", "nd", "rd", "th", "th", "th", "th", "th"][clampi(place - 1, 0, 7)]
	# A finish at every placement is positive after one deliberate race verb.
	# Auto-cruise remains a gentle assist, but an unattended kart cannot farm
	# pearls, stickers, or Galaxy progression.
	var payout := 0
	if _player_acted:
		payout = _commit_payout(_placement_bonus(place))
	if _main != null and _main.has_method("_update_hud"):
		_main._update_hud()
	if _player_acted:
		_commit_completion(place)
	_set_guide_mode("")
	_lbl_big.text = ""
	_lbl_hint.text = (("%d%s place  •  +%d pearls!" % [place, suffix, payout]) if bool(_cv("pearl_payout", true)) else ("Great racing — %d%s place!" % [place, suffix])) if _player_acted else "Steer or tap TURBO next race to join in!"
	if _minimal():
		_lbl_big.text = ""
		_lbl_hint.text = ""
	if _main != null and _main.has_method("_say"):
		_main._say("roshan", "win", 2.0)
	if _canvas != null:
		_canvas.queue_redraw()
	var tw := create_tween()
	tw.tween_interval(0.65)
	tw.tween_callback(_show_finish_result)
	tw.tween_interval(2.95)
	tw.tween_callback(_teardown.bind(place if _player_acted else -1))

func _show_finish_result() -> void:
	if _lbl_big != null and not _minimal():
		_lbl_big.text = "YOU DID IT!" if _player_acted else "YOUR TURN!"
		_lbl_big.offset_top = 4.0
		_lbl_big.add_theme_font_size_override("font_size", 54)

func _teardown(place: int) -> void:
	if _main != null and _main.has_method("_navigation_remove"):
		_main.call("_navigation_remove", "kart_race")
	# Covers explicit quit and any direct teardown caller. Both helpers are
	# idempotent, so the normal finish path cannot double-award anything.
	if place > 0:
		_commit_payout(_placement_bonus(place))
		_commit_completion(place)
	_state = "done"
	if _finish_cb.is_valid():
		_finish_cb.call(place)
	queue_free()


func _sync_hud_stage() -> void:
	if _hud_root == null:
		return
	var viewport_size := get_viewport().get_visible_rect().size
	var fit: float = minf(viewport_size.x / 1280.0, viewport_size.y / 720.0)
	_hud_root.scale = Vector2.ONE * fit
	_hud_root.position = (viewport_size - Vector2(1280, 720) * fit) * 0.5
