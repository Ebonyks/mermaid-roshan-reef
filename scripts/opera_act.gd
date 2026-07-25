class_name OperaAct
extends Node3D
# One act of the Pearl Opera House (Peach Showtime-inspired). Roshan puts on a
# career costume and performs a little show on a toy theatre stage. Six
# engines cover all ten acts: "order" (bring props in the pictured order),
# "echo" (repeat the lit dance/bell sequence), "shuffle" (follow the bunny-fish
# under the magic hats), "fix" (carry pipe pieces into their shape-matched
# slots, then spin the valve), "press" (stamp candy faces when the sliding
# star crosses the sweet spot) and "boss" (sparkle showdown with a shy stage
# puppet). No fail states anywhere: mistakes wobble, giggle and re-show the
# answer. Props come from the job GLB kits in assets/opera/jobs/ with primitive
# fallbacks. Careers listed in STAGE_SETS perform on their OWN dressed stage;
# the rest share the toy proscenium until their set is built.

const CENTER := Vector3(0.0, -2600.0, 0.0)
const RADIUS := 22.0
const MOVE_SPEED := 13.0
const PAD_REACH := 4.5

var m: ReefMain
var config: Dictionary = {}
var kind := "order"
var finish_cb: Callable
var state := "play"                # play | won | done
var win_t := 0.0
var elapsed := 0.0
var progress_t := 0.0              # seconds since the last happy step (gentle re-hint)
var prev_env: Environment = null
var cam: Camera3D = null
var hud: CanvasLayer = null
var objective: Label = null
var pointer: Label3D = null
var player_pos := Vector3.ZERO
var fire_prev := false
var act_tag := ""
var materials := {}
var audience: Array[Node3D] = []

# ---- "order" engine ----
# Three flavors share the pad core but play differently: "deliver" (chef)
# taps layers to the bowl then STIRS it; "hidden" (detective) makes each
# clue pop out only when Roshan swims close — a real search; "carry_paint"
# (painter) loads the brush at a pot then SWIPES the canvas to paint.
var pads: Array[Dictionary] = []
var order_steps: Array[int] = []
var step := 0
var goal: Node3D = null
var reveal_one := false
var order_flow := "deliver"        # deliver | carry_paint
var order_hidden := false          # clues hide until Roshan is near
var order_phase := "steps"         # steps | stir
var chef_bowl_art: Node3D = null   # pastry-chef GLB kit (null = primitive fallback)
var chef_oven_art: Node3D = null
var sleuth_chest_art: Node3D = null  # detective tiara-chest GLB kit
var doctor_patient_art: Node3D = null  # coral starfish plush GLB kit
var boxer_dressing_art: Node3D = null  # ring dressing GLB kit (lamps, bell, belt) | decorate
var stir_done := 0
var deco_spots: Array[Dictionary] = []
var deco_done := 0
var brush_loaded := -1
var brush_node: Node3D = null
# ---- drag-to-paint canvas (owner 2026-07-25) ----
# The Painter act is played by actually PAINTING: a loaded brush plus a finger
# dragged across the canvas, stamping into a live Image. A band "sets" once it
# is covered enough — coverage, never precision, so it cannot be failed.
const PAINT_RES := 96
const PAINT_BRUSH := 7
var paint_img: Image = null
var paint_tex: ImageTexture = null
var paint_canvas: MeshInstance3D = null
var paint_size := Vector2(11.0, 8.0)
var paint_hits: PackedByteArray = PackedByteArray()
var paint_band_done := 0
var paint_band_need := 0
var paint_dirty := false
var paint_easel := false        # at the easel, finger painting instead of swimming
var paint_easel_t := 0.0
var canvas_pos := Vector3.ZERO

# ---- "echo" engine ----
var echo_rounds: Array[int] = []
var echo_round := 0
var echo_seq: Array[int] = []
var echo_pos := 0
var echo_phase := "show"           # show | repeat
var echo_show_i := 0
var echo_show_t := 0.0
var last_pad := -1
var dwell_pad := -1                # tile currently being stood on (pre-fire)
var pad_dwell := 0.0               # playtest fix: tiles fire on a short STILL
var echo_prev_pos := Vector3.ZERO  # dwell — standing nearly still commits a
                                   # tile; swimming across at any speed is free

# ---- "shuffle" engine ----
var hats: Array[Dictionary] = []
var bunny: Node3D = null
var bunny_at := 0
var shuffle_round := 0
var shuffle_phase := "watch"       # watch | pick | wait
var shuffle_t := 0.0
var shuffle_wait_t := 0.0          # countdown between rounds (timer-driven)
var shuffle_next := 0
var swap_plan: Array[Dictionary] = []

# ---- "fix" engine ----
var pieces: Array[Dictionary] = []
var slots: Array[Dictionary] = []
var fix_step := 0
var carried := -1
var fix_phase := "pipes"           # pipes | valve
var valve: Node3D = null
var valve_spins := 0
var rocket_window: MeshInstance3D = null

# ---- "press" engine ----
var press_x := 0.0                 # slider position, -1..1
var press_zone := 0.34             # sweet-spot half-width (generous, shrinks a little)
var press_busy := 0.0              # stamp animation lockout
var press_next_t := 0.0            # countdown to the next candy rolling in
var candies_done := 0
var candies_goal := 4
var candy_node: Node3D = null
var press_block: Node3D = null
var press_slider: Node3D = null
var press_zone_box: Node3D = null
var shelf_candies: Array[Node3D] = []

# ---- "box" engine (boxer: ring combat in rounds) ----
var box_round := 0
var box_wait := 0.0
var box_phase := "rounds"          # warmup | rounds | belt
var box_bag: Node3D = null         # the swinging training bag (beat 1)
var box_bag_hits := 0
var box_bag_goal := 0
var box_belt: Node3D = null        # the championship belt (beat 3)

# ---- "sleuth" engine (detective: peek-in-props search) ----
var sleuth_props: Array[Dictionary] = []
var clues_found := 0
var chest_ready := false

# ---- "doctor" engine ----
var doc_targets: Array[Dictionary] = []
var doc_step := 0
var doc_wait := 0.0                # care moment: taps rest while the plushy reacts
var patient: Node3D = null

# ---- "scroll" engine (2D farm overlay; piggy art is a pending art-wing pass) ----
const FARM_SPEED := 120.0
var farm_layer: CanvasLayer = null
var farm_t := 0.0
var farm_fed := 0
var farm_toss_cool := 0.0
var farm_roshan: Control = null
var piggies: Array[Dictionary] = []

# ---- "race" engine (KartGame exhibition reuse) ----
# kart.gd / dance_engine.gd are loaded by PATH at runtime, never by class
# name: a typed reference here would pull them into every script's load
# graph and closes a load cycle (OperaAct -> DanceEngine -> ReefMain ->
# OperaHouse -> OperaAct) that destabilised engine teardown in CI — two
# probe processes hung at exit until the load edges were cut.
var kart: Node = null
var race_flag: Node3D = null
var race_prev_track := ""

# ---- "dance" engine (DanceEngine guest spot) ----
var dance: CanvasLayer = null
var mic: Node3D = null

# ---- "boss" engine ----
var boss: Dictionary = {}
var lanterns: Array[Dictionary] = []
var lantern_i := 0
var puffs: Array[Dictionary] = []
var bump_cool := 0.0
var spotlight: Node3D = null
var peek_spots: Array[float] = [-12.0, 0.0, 12.0, -18.0, 18.0]   # the dragon roams the curtain (outer two unlock as he gets bolder)
var peek_i := 0
var far_hint_cool := 0.0

# ---- shared: the rescue arrow ----
# The golden pointer is a RESCUE, not the answer: for guessing games it only
# appears after ~5s without progress (or right after a mistake), so the child
# gets a real "I did it myself!" moment before help arrives.
const RESCUE_DELAY := 5.0

# ---- the Showtime shell (Peach Showtime level framework) ----
# Most show acts open BACKSTAGE: a corridor where the dungeon's mischief
# imps have snuck in after the props. Roshan sparkle-pops them brawler-style (bumps
# only, never a fail), the side curtain sweeps open, and the act's puzzle
# waits on the main stage. Traversal -> light brawl -> puzzle -> bow keeps
# every act a 1-2 minute performance.
const BACKSTAGE_X0 := -58.0        # corridor west wall (relative to CENTER.x)
const BACKSTAGE_X1 := -26.0        # curtain gate line
var imp_count := 4                 # config "imps" can tune per act
var stage_phase := "puzzle"        # brawl | puzzle
var imps: Array[Dictionary] = []
var imps_left := 0
var gate_curtain: Node3D = null
var brawl_bump_cool := 0.0

func start(main: ReefMain, act_config: Dictionary, done_cb: Callable) -> void:
	m = main
	config = act_config
	finish_cb = done_cb
	kind = String(config.get("kind", "order"))
	reveal_one = bool(config.get("reveal_one", false))
	act_tag = String(config.get("act_tag", ""))
	stage_phase = "brawl" if bool(config.get("shell", false)) else "puzzle"
	player_pos = CENTER + Vector3(0, 1.1, 14.0)
	if stage_phase == "brawl":
		player_pos = CENTER + Vector3(-50.0, 1.1, 3.0)
	_build_environment()
	_build_theatre()
	_dress_world()
	if stage_phase == "brawl":
		_build_backstage()
	_build_avatar()
	_build_camera()
	_build_hud()
	match kind:
		"order", "paint":
			_build_order()
		"echo":
			_build_echo()
		"shuffle":
			_build_shuffle()
		"fix":
			_build_fix()
		"press":
			_build_press()
		"box":
			_build_box()
		"sleuth":
			_build_sleuth()
		"doctor":
			_build_doctor()
		"scroll":
			_build_farm()
		"race":
			_build_race()
		"dance":
			_build_dance()
		"boss":
			_build_boss()
	# the Showtime transformation moment: sparkles + the career announcement.
	# Shelled acts open with the backstage story instead — the act's own
	# instructions arrive when the curtain sweeps open in _open_gate().
	m._sparkle_burst(player_pos + Vector3(0, 2.5, 0), Color(1.0, 0.85, 1.0))
	m._sparkle_burst(player_pos + Vector3(0, 0.8, 0), Color(0.72, 0.95, 1.0))
	if stage_phase == "brawl":
		m.show_msg("Roshan", "Oh no — mischief imps snuck backstage! Pop them with SPARKLE so the show can start!", "talk")
	else:
		m.show_msg("Roshan", String(config.get("voice", "It's showtime! Follow the golden sparkle!")), "talk")
	_update_hud()

# ---------------- shared toy-theatre set ----------------

func _build_environment() -> void:
	prev_env = m.we_node.environment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(config.get("background", Color(0.06, 0.045, 0.12)))
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.9, 0.82, 1.0)
	env.ambient_light_energy = 1.0
	env.glow_enabled = true
	env.glow_intensity = 0.55
	env.glow_bloom = 0.1
	m._speedy_glow_clamp(env)
	m.we_node.environment = env
	var sun := DirectionalLight3D.new()
	sun.light_color = Color(1.0, 0.9, 0.78)
	sun.light_energy = 1.1
	sun.shadow_enabled = m.quality != "speedy"
	sun.rotation_degrees = Vector3(-50, -20, 0)
	add_child(sun)

func _mat(col: Color, glow: float = 0.0) -> StandardMaterial3D:
	var key := "%s:%.2f" % [col.to_html(true), glow]
	if materials.has(key):
		return materials[key]
	var mat := StandardMaterial3D.new()
	mat.albedo_color = col
	mat.roughness = 0.68
	if glow > 0.0:
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = glow
	materials[key] = mat
	return mat

func _mesh(mesh: Mesh, pos: Vector3, col: Color, glow: float = 0.0, parent: Node3D = null) -> MeshInstance3D:
	var node := MeshInstance3D.new()
	node.mesh = mesh
	node.position = pos
	node.material_override = _mat(col, glow)
	var target: Node3D = self if parent == null else parent
	target.add_child(node)
	return node

func _box(pos: Vector3, size: Vector3, col: Color, glow: float = 0.0, parent: Node3D = null) -> MeshInstance3D:
	var mesh := BoxMesh.new()
	mesh.size = size
	return _mesh(mesh, pos, col, glow, parent)

func _sphere(pos: Vector3, radius: float, col: Color, glow: float = 0.0, parent: Node3D = null) -> MeshInstance3D:
	var mesh := SphereMesh.new()
	mesh.radius = radius
	mesh.height = radius * 2.0
	mesh.radial_segments = 10
	mesh.rings = 5
	return _mesh(mesh, pos, col, glow, parent)

func _cyl(pos: Vector3, radius: float, height: float, col: Color, glow: float = 0.0, parent: Node3D = null) -> MeshInstance3D:
	var mesh := CylinderMesh.new()
	mesh.top_radius = radius
	mesh.bottom_radius = radius
	mesh.height = height
	mesh.radial_segments = 12
	return _mesh(mesh, pos, col, glow, parent)

# Per-act world dressing from the converted card library (Codex guide:
# CODEX_ASSET_REQUESTS_2026-07-21.md). Cards are flat cutouts exported lying
# down; _card() stands them upright facing the audience. Positions hug the
# backdrop and wings so gameplay props keep the centre stage.
const DRESS := {
	"chef": [["style3/fruit_apple", -19.0, -12.0, 2.2], ["style3/fruit_banana", -14.5, -13.0, 2.0],
		["style3/fruit_melon", 14.5, -13.0, 2.4], ["style3/fruit_orange", 19.0, -12.0, 2.0], ["mg/sun", 0.0, -15.5, 3.0]],
	"detective": [["style3/crystal_facet", -18.0, -12.5, 2.2], ["mg/star", 18.0, -12.5, 2.4], ["style3/shipwood", 0.0, -15.5, 3.2]],
	"ballerina": [["mg/flower2", -19.0, -12.5, 2.2], ["mg/flower3", 19.0, -12.5, 2.2],
		["mg/flower4", -14.0, -14.0, 1.8], ["mg/flower", 14.0, -14.0, 1.8], ["mg/star", 0.0, -15.5, 2.6]],
	"candymaker": [["mg/orn1", -18.0, -12.5, 2.4], ["mg/orn2", -12.5, -14.0, 2.0], ["mg/orn3", 12.5, -14.0, 2.0],
		["mg/orn4", 18.0, -12.5, 2.4], ["mg/rainbow_swatch", 0.0, -15.5, 3.0]],
	"doctor": [["mg/flower", -18.0, -12.5, 2.0], ["mg/butterfly", 18.0, -12.5, 2.0], ["mg/sun", 0.0, -15.5, 2.8]],
	"boxer": [["mg/star", -18.0, -12.5, 2.6], ["mg/star", 18.0, -12.5, 2.6], ["mg/sun", 0.0, -15.5, 3.0]],
	"magician": [["mg/star", -18.0, -12.5, 2.4], ["style3/crystal_facet", 18.0, -12.5, 2.2], ["mg/xtree", 0.0, -15.5, 3.0]],
	"painter": [["mg/rainbow_swatch", -18.0, -12.5, 2.6], ["style3/leaf_broad", 18.0, -12.5, 2.2],
		["style3/leaf_fern", 13.0, -14.0, 1.9], ["mg/sun", 0.0, -15.5, 2.8]],
	"astronaut": [["mg/star", -18.0, -12.5, 2.4], ["mg/coal", 18.0, -12.5, 2.0], ["mg/star", 13.0, -14.5, 1.7]],
	"popstar": [["mg/star", -18.0, -12.5, 2.6], ["mg/rainbow_swatch", 18.0, -12.5, 2.4], ["mg/orn5", 0.0, -15.5, 2.6]],
	"knight_boss": [["mg/star", -18.0, -12.5, 2.4], ["mg/star", 18.0, -12.5, 2.4]],
}

# Per-job stages. Palettes and scenery come from the accepted stage_states
# sheets in codex's opera_jobs_flat_2026-07-21 set (see
# OPERA_JOB_FLAT_ART_AUDIT_2026-07-21.md). A career listed here performs on its
# own dressed set instead of the shared recoloured proscenium; a career left
# out keeps the shared stage, so this table can be filled in one job at a time.
# Scenery lives outside the play box (|x| >= 19, z <= -14 or z >= 17) so no
# dressing can ever sit on top of an act's gameplay props.
const STAGE_SETS := {
	"candymaker": {                                  # "the Candy Workshop"
		"set": "candy_workshop",
		"deck": Color(0.72, 0.6, 0.75),
		"pillar": Color(0.42, 0.72, 0.72),           # mint-teal pearl columns
		"beam": Color(0.98, 0.74, 0.76),             # coral-rose arch band
		"backdrop": Color(0.5, 0.4, 0.63),           # warm lilac workshop wall
		"wing": Color(0.86, 0.42, 0.52),
		"crest": Color(1.0, 0.9, 0.72),
		"pool": Color(1.0, 0.88, 0.72, 0.13),
	},
	"detective": {                                   # "the Prop Library"
		"set": "prop_library",
		"deck": Color(0.3, 0.28, 0.45),
		"pillar": Color(0.86, 0.56, 0.56),           # coral arch legs
		"beam": Color(0.9, 0.6, 0.62),
		"backdrop": Color(0.16, 0.18, 0.35),         # deep indigo night library
		"wing": Color(0.4, 0.3, 0.45),
		"crest": Color(1.0, 0.88, 0.7),
		"pool": Color(1.0, 0.86, 0.6, 0.16),         # the searchlight pool
	},
	"chef": {                                        # "the Pastry Kitchen"
		"set": "pastry_kitchen",
		"deck": Color(0.85, 0.7, 0.5),               # honey wood boards
		"pillar": Color(0.93, 0.86, 0.82),           # cream-blush columns
		"beam": Color(0.96, 0.9, 0.84),
		"backdrop": Color(0.35, 0.62, 0.72),         # painted reef seascape
		"wing": Color(0.72, 0.17, 0.23),             # crimson drapes
		"crest": Color(1.0, 0.9, 0.72),
		"pool": Color(1.0, 0.9, 0.72, 0.12),
	},
	"ballerina": {                                   # "the Recital Hall"
		"set": "recital_hall",
		"deck": Color(0.8, 0.76, 0.86),              # pale lilac dance floor
		"pillar": Color(0.78, 0.5, 0.56),            # dusty rose columns
		"beam": Color(1.0, 0.86, 0.56),
		"backdrop": Color(0.9, 0.78, 0.81),          # blush scallop-shell fan
		"wing": Color(0.35, 0.62, 0.68),             # teal gathers
		"crest": Color(1.0, 0.88, 0.66),
		"pool": Color(1.0, 0.92, 0.85, 0.15),
	},
	"doctor": {                                      # "the Plushy Clinic"
		"set": "plushy_clinic",
		"deck": Color(0.92, 0.87, 0.82),             # clean cream floor
		"pillar": Color(0.62, 0.55, 0.78),           # lavender columns
		"beam": Color(1.0, 0.88, 0.62),
		"backdrop": Color(0.25, 0.55, 0.6),          # quilted teal panel
		"wing": Color(0.2, 0.45, 0.5),
		"crest": Color(1.0, 0.9, 0.68),
		"pool": Color(0.9, 0.95, 1.0, 0.14),
	},
	"farmer": {                                      # "the Meadow Flat"
		"set": "meadow_flat",
		"deck": Color(0.82, 0.66, 0.46),
		"pillar": Color(0.94, 0.9, 0.84),            # cream stone arch
		"beam": Color(0.96, 0.92, 0.86),
		"backdrop": Color(0.52, 0.72, 0.86),         # painted meadow sky
		"wing": Color(0.75, 0.25, 0.28),
		"crest": Color(1.0, 0.9, 0.7),
	},
	"boxer": {                                       # "the Toy Ring"
		"set": "toy_ring",
		"deck": Color(0.85, 0.62, 0.62),             # blush canvas mat
		"pillar": Color(0.55, 0.45, 0.62),           # mauve columns
		"beam": Color(0.66, 0.55, 0.7),
		"backdrop": Color(0.18, 0.18, 0.32),         # dark hall, string lights
		"wing": Color(0.8, 0.34, 0.34),
		"crest": Color(1.0, 0.9, 0.72),
	},
	"magician": {                                    # "the Conjuring Parlour"
		"set": "conjuring_parlour",
		"deck": Color(0.82, 0.68, 0.5),
		"pillar": Color(0.85, 0.68, 0.42),           # amber-gold arch
		"beam": Color(0.9, 0.74, 0.46),
		"backdrop": Color(0.42, 0.3, 0.5),           # plum velvet
		"wing": Color(0.36, 0.25, 0.45),
		"crest": Color(0.95, 0.62, 0.6),             # coral shell crest
		"pool": Color(1.0, 0.94, 0.8, 0.14),
	},
	"painter": {                                     # "the Sunrise Gallery"
		"set": "sunrise_gallery",
		"deck": Color(0.86, 0.72, 0.52),
		"pillar": Color(0.88, 0.88, 0.82),           # cream-sage columns
		"beam": Color(0.92, 0.92, 0.86),
		"backdrop": Color(0.95, 0.6, 0.35),          # the sunrise being painted
		"wing": Color(0.72, 0.18, 0.24),
		"crest": Color(1.0, 0.9, 0.7),
	},
	"astronaut": {                                   # "the Launch Pad"
		"set": "launch_pad",
		"deck": Color(0.4, 0.55, 0.62),              # teal launch platform
		"pillar": Color(0.85, 0.5, 0.45),            # coral columns
		"beam": Color(0.96, 0.9, 0.78),
		"backdrop": Color(0.16, 0.2, 0.4),           # starfield with planets
		"wing": Color(0.45, 0.32, 0.6),
		"crest": Color(1.0, 0.92, 0.78),
		"pool": Color(0.75, 0.9, 1.0, 0.12),
	},
	"racer": {                                       # "the Grand Prix Circuit"
		"set": "grand_prix",
		"deck": Color(0.65, 0.6, 0.78),              # lavender apron
		"pillar": Color(0.85, 0.6, 0.65),            # coral-pink columns
		"beam": Color(1.0, 0.86, 0.58),
		"backdrop": Color(0.2, 0.22, 0.45),          # deep blue swirl night
		"wing": Color(0.42, 0.3, 0.52),
		"crest": Color(1.0, 0.9, 0.72),
	},
	"popstar": {                                     # "the Starlight Concert"
		"set": "starlight_concert",
		"deck": Color(0.55, 0.42, 0.6),              # plum concert platform
		"pillar": Color(0.9, 0.72, 0.78),            # blush columns
		"beam": Color(0.95, 0.8, 0.84),
		"backdrop": Color(0.5, 0.42, 0.68),          # lavender rainbow wall
		"wing": Color(0.85, 0.5, 0.68),              # pink + teal ribbons
		"crest": Color(1.0, 0.92, 0.8),
		"pool": Color(1.0, 0.85, 0.95, 0.16),
	},
}

func _build_job_stage(spec: Dictionary) -> void:
	# the gold scallop-shell crest every dressed set wears over its arch
	var crest_col := Color(spec.get("crest", Color(1.0, 0.9, 0.72)))
	var crest := Node3D.new()
	crest.name = "StageCrest"
	crest.position = CENTER + Vector3(0, 18.3, 12.0)
	add_child(crest)
	for i in range(5):
		var a := lerpf(-1.0, 1.0, float(i) / 4.0)
		var petal := _sphere(Vector3(a * 3.3, 1.0 - absf(a) * 0.85, 0), 1.15 - absf(a) * 0.26, crest_col, 0.25, crest)
		petal.scale = Vector3(0.9, 1.3, 0.5)
	_sphere(Vector3(0, -0.35, 0.4), 0.9, Color(1.0, 0.98, 0.95), 0.45, crest)
	# the warm light pool the act plays inside (flat, unshaded — no OmniLights)
	if spec.has("pool"):
		var disc := CylinderMesh.new()
		disc.top_radius = 13.5
		disc.bottom_radius = 13.5
		disc.height = 0.12
		var pool := _mesh(disc, CENTER + Vector3(0, 0.38, -2.0), Color(spec["pool"]), 0.5)
		var pm := pool.material_override as StandardMaterial3D
		pm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		pm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	match String(spec.get("set", "")):
		"candy_workshop":
			_stage_candy_workshop(spec)
		"prop_library":
			_stage_prop_library(spec)
		"pastry_kitchen":
			_stage_pastry_kitchen(spec)
		"recital_hall":
			_stage_recital_hall(spec)
		"plushy_clinic":
			_stage_plushy_clinic(spec)
		"meadow_flat":
			_stage_meadow_flat(spec)
		"toy_ring":
			_stage_toy_ring(spec)
		"conjuring_parlour":
			_stage_conjuring_parlour(spec)
		"sunrise_gallery":
			_stage_sunrise_gallery(spec)
		"launch_pad":
			_stage_launch_pad(spec)
		"grand_prix":
			_stage_grand_prix(spec)
		"starlight_concert":
			_stage_starlight_concert(spec)

func _footlights(col: Color, n: int = 7) -> void:
	# the row of gold bulbs along the apron edge — the shared signature of the
	# dressed sets that draw one in their card (chef, ballerina, magician...)
	if m.quality == "speedy":
		return
	for i in range(n):
		var fx := -20.0 + float(i) * (40.0 / maxf(1.0, float(n - 1)))
		_sphere(CENTER + Vector3(fx, 0.75, 15.2), 0.5, col, 1.1)

func _backdrop_panel(col: Color, glow: float = 0.15) -> MeshInstance3D:
	# a painted flat hung just in front of the back curtain — every set that
	# shows a picture upstage (seascape, meadow, sunrise, starfield) uses one
	return _box(CENTER + Vector3(0, 8.0, -17.1), Vector3(34.0, 14.0, 0.4), col, glow)

func _stage_candy_workshop(_spec: Dictionary) -> void:
	# Candy Maker's set: a sweet-shop wall of jars upstage, a scalloped mixing
	# counter in each wing, and swirl lollipops hanging over the gathers.
	var jar_cols: Array[Color] = [Color(1.0, 0.66, 0.74), Color(0.68, 0.88, 1.0),
		Color(1.0, 0.88, 0.56), Color(0.8, 0.72, 1.0), Color(0.72, 0.94, 0.78)]
	var lush := m.quality != "speedy"      # Speedy phones get one jar tier, no pops
	for tier in range(2 if lush else 1):
		var sy := 4.2 + float(tier) * 4.4
		_box(CENTER + Vector3(0, sy - 0.9, -16.4), Vector3(30.0, 0.5, 1.8), Color(0.86, 0.66, 0.58), 0.08)
		for i in range(7):
			var jx := -12.6 + float(i) * 4.2
			var col := jar_cols[(i + tier * 3) % jar_cols.size()]
			_cyl(CENTER + Vector3(jx, sy + 0.5, -16.4), 1.15, 2.3, Color(0.95, 0.94, 1.0), 0.12)
			_sphere(CENTER + Vector3(jx, sy + 0.4, -16.4), 0.95, col, 0.3)
			_sphere(CENTER + Vector3(jx, sy + 1.9, -16.4), 0.5, Color(1.0, 0.93, 0.8), 0.25)
	for sx: float in [-19.5, 19.5]:
		# the mixing counter: scalloped skirt, marble top, a pot and a swirl
		_box(CENTER + Vector3(sx, 1.4, -13.5), Vector3(6.4, 2.8, 4.6), Color(0.86, 0.5, 0.6), 0.06)
		_box(CENTER + Vector3(sx, 3.0, -13.5), Vector3(7.0, 0.6, 5.2), Color(0.98, 0.95, 1.0), 0.14)
		for i in range(4):
			_sphere(CENTER + Vector3(sx - 2.4 + float(i) * 1.6, 0.3, -11.2), 0.85, Color(1.0, 0.86, 0.9), 0.1)
		_cyl(CENTER + Vector3(sx, 4.2, -13.5), 1.5, 1.8, Color(0.72, 0.5, 0.72), 0.12)
		_sphere(CENTER + Vector3(sx, 5.4, -13.5), 1.1, Color(1.0, 0.78, 0.86), 0.35)
	for i in range(6 if lush else 0):
		# swirl lollipops on their sticks, hung high in the wings
		var lx := -20.5 if i < 3 else 20.5
		var ly := 9.0 + float(i % 3) * 3.4
		_box(CENTER + Vector3(lx, ly - 1.5, -6.0), Vector3(0.28, 3.0, 0.28), Color(0.98, 0.96, 0.92), 0.1)
		var pop := _cyl(CENTER + Vector3(lx, ly, -6.0), 1.7, 0.4, jar_cols[i % jar_cols.size()], 0.3)
		pop.rotation_degrees = Vector3(90, 0, 0)
		_sphere(CENTER + Vector3(lx, ly, -5.7), 0.6, Color(1.0, 0.98, 0.94), 0.35)

func _stage_prop_library(spec: Dictionary) -> void:
	# Detective's set: the theatre's own prop library after dark — crated
	# shelves, a leaning ladder, pillar lanterns and a crescent moon window.
	var crate_col := Color(0.5, 0.42, 0.58)
	var lid_col := Color(0.62, 0.52, 0.66)
	var lush := m.quality != "speedy"      # Speedy phones get half the shelving
	for sx: float in [-19.8, 19.8]:
		# tall archive shelving stacked with wrapped prop silhouettes
		_box(CENTER + Vector3(sx, 6.5, -12.0), Vector3(6.6, 13.0, 5.0), Color(0.34, 0.3, 0.48), 0.04)
		for tier in range(4 if lush else 2):
			var sy := 2.2 + float(tier) * 3.2
			_box(CENTER + Vector3(sx, sy, -9.6), Vector3(6.8, 0.4, 0.6), lid_col, 0.08)
			for i in range(2):
				var bx := sx - 1.5 + float(i) * 3.0
				_box(CENTER + Vector3(bx, sy + 1.1, -10.4), Vector3(2.0, 1.8, 2.0), crate_col, 0.05)
				_box(CENTER + Vector3(bx, sy + 2.1, -10.4), Vector3(2.3, 0.35, 2.3), lid_col, 0.08)
		# a warm lantern globe on top of each proscenium pillar
		var lantern_x := -23.0 if sx < 0.0 else 23.0
		_cyl(CENTER + Vector3(lantern_x, 16.9, 12.0), 0.7, 0.5, Color(0.95, 0.8, 0.55), 0.2)
		_sphere(CENTER + Vector3(lantern_x, 18.0, 12.0), 1.1, Color(1.0, 0.9, 0.65), 1.5)
	# stacked crates tucked into the downstage corners, downstage of the
	# furthest search box (z = +5) so a clue can never hide behind one
	for i in range(4):
		var cx := -21.0 if i < 2 else 21.0
		var cz := 9.0 + float(i % 2) * 5.0
		_box(CENTER + Vector3(cx, 1.3, cz), Vector3(3.4, 2.6, 3.4), crate_col, 0.05)
		_box(CENTER + Vector3(cx, 2.75, cz), Vector3(3.7, 0.4, 3.7), lid_col, 0.08)
	# the leaning ladder against the upstage-left shelf
	var ladder := Node3D.new()
	ladder.name = "LibraryLadder"
	ladder.position = CENTER + Vector3(-15.5, 4.5, -14.5)
	ladder.rotation_degrees = Vector3(-14.0, 0, 0)
	add_child(ladder)
	for side: float in [-0.9, 0.9]:
		_box(Vector3(side, 0, 0), Vector3(0.35, 9.5, 0.35), Color(0.78, 0.62, 0.45), 0.05, ladder)
	for i in range(5):
		_box(Vector3(0, -3.6 + float(i) * 1.9, 0), Vector3(2.1, 0.28, 0.28), Color(0.86, 0.7, 0.5), 0.05, ladder)
	# the crescent moon window: a glowing disc bitten by one in the backdrop's
	# own colour, so the crescent stays cut no matter how the palette is tuned
	_sphere(CENTER + Vector3(0, 12.0, -17.2), 3.1, Color(1.0, 0.95, 0.78), 1.4)
	_sphere(CENTER + Vector3(1.5, 12.7, -17.0), 2.7, Color(spec.get("backdrop", Color(0.16, 0.18, 0.35))), 0.0)
	for i in range(9 if lush else 0):
		# a scatter of little stars around the window
		var a := float(i) * 0.7
		_sphere(CENTER + Vector3(sin(a) * (7.0 + float(i)), 12.0 + cos(a) * 4.5, -17.3), 0.32, Color(1.0, 0.97, 0.85), 1.2)

func _stage_pastry_kitchen(spec: Dictionary) -> void:
	# Pastry Chef: a painted reef seascape flat, an ingredient shelf either
	# side, the oven alcove glowing warm, and gold footlights on the apron.
	var lush := m.quality != "speedy"
	_backdrop_panel(Color(spec.get("backdrop", Color(0.35, 0.62, 0.72))), 0.1)
	# coral and kelp painted onto the flat, in front of it
	for i in range(5 if lush else 2):
		var cx := -13.0 + float(i) * 6.5
		var ch := 3.0 + float(i % 3) * 1.6
		_cyl(CENTER + Vector3(cx, ch * 0.5 + 1.0, -16.7), 0.6, ch,
			Color(0.95, 0.5, 0.55) if i % 2 == 0 else Color(0.4, 0.75, 0.7), 0.15)
	# the oven alcove: a warm arch glowing upstage-left
	_box(CENTER + Vector3(-19.5, 4.0, -15.5), Vector3(6.0, 8.0, 3.0), Color(0.72, 0.55, 0.44), 0.05)
	_box(CENTER + Vector3(-19.5, 3.4, -14.1), Vector3(4.2, 4.6, 0.4), Color(1.0, 0.72, 0.35), 0.9)
	# the ingredient shelf upstage-right: flour sacks, bowls, a rolling pin
	for tier in range(2):
		var sy := 3.2 + float(tier) * 3.2
		_box(CENTER + Vector3(19.5, sy, -15.0), Vector3(6.4, 0.45, 3.0), Color(0.8, 0.62, 0.44), 0.06)
		for i in range(3):
			_sphere(CENTER + Vector3(17.4 + float(i) * 2.1, sy + 0.9, -15.0), 0.8,
				[Color(0.98, 0.95, 0.88), Color(0.95, 0.72, 0.55), Color(0.85, 0.6, 0.72)][i], 0.12)
	_footlights(Color(1.0, 0.88, 0.6))

func _stage_recital_hall(spec: Dictionary) -> void:
	# Ballerina: a huge blush scallop fan upstage, a practice barre in each
	# wing, mirror panels, and a slow mirror-ball above centre stage.
	var lush := m.quality != "speedy"
	var fan_col := Color(spec.get("backdrop", Color(0.9, 0.78, 0.81)))
	# the scallop fan: petals radiating from the backdrop centre
	for i in range(11 if lush else 6):
		var ang := lerpf(-1.25, 1.25, float(i) / float((11 if lush else 6) - 1))
		var petal := _box(CENTER + Vector3(sin(ang) * 9.0, 8.0 + cos(ang) * 5.0, -16.9),
			Vector3(2.6, 9.0, 0.35), fan_col.lightened(0.06 * float(i % 3)), 0.14)
		petal.rotation_degrees = Vector3(0, 0, -rad_to_deg(ang))
	_sphere(CENTER + Vector3(0, 3.4, -16.6), 3.2, Color(1.0, 0.94, 0.9), 0.2)
	# a practice barre along each wing
	for sx: float in [-19.5, 19.5]:
		_box(CENTER + Vector3(sx, 3.4, -4.0), Vector3(0.5, 0.5, 22.0), Color(0.86, 0.68, 0.5), 0.1)
		for i in range(3):
			_box(CENTER + Vector3(sx, 1.7, -13.0 + float(i) * 9.0), Vector3(0.4, 3.4, 0.4), Color(0.78, 0.6, 0.45), 0.05)
		# tall mirror panels behind the barre
		_box(CENTER + Vector3(sx + (1.6 if sx > 0.0 else -1.6), 6.0, -6.0), Vector3(0.3, 11.0, 16.0),
			Color(0.82, 0.88, 0.95), 0.22)
	# the mirror ball, hung over centre stage
	var ball := _sphere(CENTER + Vector3(0, 13.0, 2.0), 1.6, Color(0.9, 0.94, 1.0), 0.7)
	ball.name = "MirrorBall"
	for i in range(10 if lush else 0):
		var a := float(i) * 0.63
		_sphere(CENTER + Vector3(sin(a) * 1.5, 13.0 + cos(a) * 1.5, 2.0), 0.3, Color(1.0, 0.95, 0.85), 1.3)
	_footlights(Color(1.0, 0.9, 0.68))

func _stage_plushy_clinic(spec: Dictionary) -> void:
	# Doctor: a quilted teal wall with a big gold shell medallion, a tool
	# trolley, a handwashing basin, and the waiting bench of plush patients.
	var quilt := Color(spec.get("backdrop", Color(0.25, 0.55, 0.6)))
	_backdrop_panel(quilt, 0.08)
	# the quilting: a lattice of raised seams on the panel
	for i in range(5):
		_box(CENTER + Vector3(-13.0 + float(i) * 6.5, 8.0, -16.85), Vector3(0.25, 13.0, 0.2), quilt.lightened(0.16), 0.1)
	for j in range(3):
		_box(CENTER + Vector3(0, 3.4 + float(j) * 4.2, -16.85), Vector3(33.0, 0.25, 0.2), quilt.lightened(0.16), 0.1)
	# the gold scallop medallion at the centre of the wall
	for i in range(5):
		var a := lerpf(-1.0, 1.0, float(i) / 4.0)
		var petal := _sphere(CENTER + Vector3(a * 3.6, 9.0 - absf(a) * 1.0, -16.5), 1.25 - absf(a) * 0.28,
			Color(1.0, 0.9, 0.68), 0.3)
		petal.scale = Vector3(0.85, 1.3, 0.5)
	# tool trolley upstage-left, basin upstage-right
	_box(CENTER + Vector3(-19.0, 2.6, -14.0), Vector3(5.0, 0.4, 3.2), Color(0.95, 0.96, 1.0), 0.16)
	for i in range(2):
		_box(CENTER + Vector3(-20.6 + float(i) * 3.2, 1.3, -14.0), Vector3(0.35, 2.6, 0.35), Color(0.7, 0.74, 0.85), 0.08)
	for i in range(3):
		_sphere(CENTER + Vector3(-20.4 + float(i) * 1.6, 3.2, -14.0), 0.5,
			[Color(0.95, 0.6, 0.65), Color(0.7, 0.9, 1.0), Color(1.0, 0.9, 0.6)][i], 0.3)
	_cyl(CENTER + Vector3(19.0, 2.2, -14.0), 2.0, 1.4, Color(0.95, 0.97, 1.0), 0.18)
	_cyl(CENTER + Vector3(19.0, 0.9, -14.0), 0.7, 2.0, Color(0.72, 0.78, 0.9), 0.08)
	_sphere(CENTER + Vector3(19.0, 3.2, -14.0), 0.7, Color(0.8, 0.95, 1.0), 0.5)
	# the waiting bench: three plush patients queued in the wing
	_box(CENTER + Vector3(20.0, 1.2, 4.0), Vector3(3.2, 1.6, 11.0), Color(0.75, 0.62, 0.85), 0.06)
	for i in range(3):
		_sphere(CENTER + Vector3(20.0, 2.8, 0.0 + float(i) * 4.0), 1.1,
			[Color(1.0, 0.66, 0.6), Color(0.7, 0.85, 1.0), Color(1.0, 0.88, 0.6)][i], 0.2)

func _stage_meadow_flat(spec: Dictionary) -> void:
	# Farmer: the 2D picnic plays on a CanvasLayer, so this whole set is the
	# painted backing it plays against — rolling hills, a red barn, orchard.
	var lush := m.quality != "speedy"
	_backdrop_panel(Color(spec.get("backdrop", Color(0.52, 0.72, 0.86))), 0.12)
	# rolling green hills across the bottom of the flat
	for i in range(3):
		var hill := _sphere(CENTER + Vector3(-11.0 + float(i) * 11.0, 1.0, -16.8), 8.0 - float(i) * 0.8,
			Color(0.45, 0.68, 0.4).lightened(0.07 * float(i)), 0.08)
		hill.scale = Vector3(1.6, 0.55, 0.12)
	# the little red barn on the right hill
	_box(CENTER + Vector3(9.5, 4.4, -16.6), Vector3(4.6, 4.0, 0.5), Color(0.8, 0.28, 0.28), 0.1)
	_box(CENTER + Vector3(9.5, 7.0, -16.6), Vector3(5.4, 1.6, 0.5), Color(0.65, 0.22, 0.24), 0.1)
	_box(CENTER + Vector3(9.5, 3.6, -16.4), Vector3(1.6, 2.4, 0.3), Color(0.95, 0.9, 0.82), 0.1)
	# clouds
	for i in range(5 if lush else 2):
		var cl := _sphere(CENTER + Vector3(-14.0 + float(i) * 7.0, 11.5 + float(i % 2) * 1.6, -16.8),
			2.0 + float(i % 3) * 0.5, Color(1.0, 0.99, 0.96), 0.25)
		cl.scale = Vector3(1.7, 0.7, 0.15)
	# orchard trees and flower borders framing the wings
	for sx: float in [-19.5, 19.5]:
		for i in range(2):
			var tz := -13.0 + float(i) * 7.0
			_cyl(CENTER + Vector3(sx, 2.0, tz), 0.6, 4.0, Color(0.55, 0.4, 0.3), 0.05)
			_sphere(CENTER + Vector3(sx, 5.4, tz), 2.8, Color(0.42, 0.66, 0.38), 0.12)
			_sphere(CENTER + Vector3(sx, 6.2, tz + 1.2), 1.9, Color(0.5, 0.74, 0.44), 0.12)
		for i in range(5 if lush else 0):
			var fz := -15.0 + float(i) * 4.0
			_sphere(CENTER + Vector3(sx + (1.6 if sx < 0.0 else -1.6), 0.9, fz), 0.7,
				[Color(1.0, 0.75, 0.8), Color(1.0, 0.9, 0.55), Color(0.9, 0.7, 1.0)][i % 3], 0.3)

func _stage_toy_ring(spec: Dictionary) -> void:
	# Boxer: a dark toy hall strung with lights, corner stools, pennants and
	# the championship belt waiting on its podium. The ring itself is _build_box.
	var lush := m.quality != "speedy"
	_backdrop_panel(Color(spec.get("backdrop", Color(0.18, 0.18, 0.32))), 0.05)
	# strings of warm bulbs swagging across the dark hall
	for row in range(2 if lush else 1):
		var ry := 12.5 - float(row) * 2.6
		for i in range(9):
			var bx := -16.0 + float(i) * 4.0
			var sag := sin(float(i) / 8.0 * PI) * 1.3
			_sphere(CENTER + Vector3(bx, ry - sag, -13.0 + float(row) * 3.0), 0.42,
				Color.from_hsv(0.08 + 0.02 * float(i % 3), 0.3, 1.0), 1.4)
	# corner stools, one coral one teal, tucked outside the ring posts
	_box(CENTER + Vector3(-19.5, 1.1, -13.0), Vector3(3.0, 2.2, 3.0), Color(0.9, 0.45, 0.45), 0.1)
	_box(CENTER + Vector3(19.5, 1.1, -13.0), Vector3(3.0, 2.2, 3.0), Color(0.4, 0.72, 0.75), 0.1)
	# pennant bunting over the wings
	for i in range(10 if lush else 0):
		var px := -20.0 + float(i) * 4.5
		var pen := _box(CENTER + Vector3(px, 14.0 - absf(float(i) - 4.5) * 0.35, 10.0), Vector3(1.4, 1.8, 0.15),
			Color.from_hsv(float(i) / 10.0, 0.45, 1.0), 0.35)
		pen.rotation_degrees = Vector3(0, 0, 180.0)
	# the belt on its victory podium, downstage-right
	_cyl(CENTER + Vector3(20.0, 1.4, 8.0), 2.4, 2.8, Color(0.62, 0.5, 0.7), 0.1)
	var belt := _cyl(CENTER + Vector3(20.0, 3.1, 8.0), 1.7, 0.5, Color(0.55, 0.35, 0.3), 0.12)
	belt.rotation_degrees = Vector3(90, 0, 0)
	_sphere(CENTER + Vector3(20.0, 3.1, 8.6), 0.9, Color(1.0, 0.85, 0.4), 0.9)

func _stage_conjuring_parlour(spec: Dictionary) -> void:
	# Magician: plum velvet, amber arch, coral and teal fronds in the wings,
	# a trick cabinet, and a rolling mirror that catches the spotlight.
	var lush := m.quality != "speedy"
	_backdrop_panel(Color(spec.get("backdrop", Color(0.42, 0.3, 0.5))), 0.06)
	# swagged velvet valance across the top of the flat
	for i in range(5 if lush else 3):
		var vx := -13.0 + float(i) * 6.5
		var swag := _sphere(CENTER + Vector3(vx, 12.6, -16.7), 2.4, Color(0.5, 0.34, 0.58), 0.1)
		swag.scale = Vector3(1.0, 0.85, 0.2)
	# coral and teal seaweed fronds standing in both wings
	for sx: float in [-19.5, 19.5]:
		for i in range(3):
			var fz := -14.0 + float(i) * 5.0
			var fh := 5.0 + float(i % 2) * 2.2
			var frond := _cyl(CENTER + Vector3(sx, fh * 0.5 + 0.8, fz), 0.75, fh,
				Color(0.95, 0.5, 0.5) if i % 2 == 0 else Color(0.4, 0.78, 0.72), 0.16)
			frond.rotation_degrees = Vector3(0, 0, 7.0 * (1.0 if sx < 0.0 else -1.0))
	# the trick cabinet upstage-left, star-studded
	_box(CENTER + Vector3(-16.5, 4.0, -15.2), Vector3(5.0, 8.0, 2.6), Color(0.34, 0.24, 0.44), 0.08)
	for i in range(4 if lush else 2):
		_sphere(CENTER + Vector3(-16.5, 2.0 + float(i) * 2.0, -13.8), 0.42, Color(1.0, 0.9, 0.5), 1.2)
	# the rolling mirror upstage-right on its gold frame
	_box(CENTER + Vector3(16.5, 5.0, -15.2), Vector3(4.6, 8.4, 0.35), Color(0.88, 0.72, 0.45), 0.2)
	_box(CENTER + Vector3(16.5, 5.0, -15.0), Vector3(3.6, 7.4, 0.2), Color(0.86, 0.9, 0.98), 0.3)
	_footlights(Color(1.0, 0.86, 0.55), 9)

func _stage_sunrise_gallery(spec: Dictionary) -> void:
	# Painter: the backdrop IS the sunrise the act paints — it starts pale and
	# the act's own canvas stripes fill in. Plus a paint cart and drop cloth.
	var lush := m.quality != "speedy"
	var sky := Color(spec.get("backdrop", Color(0.95, 0.6, 0.35)))
	_backdrop_panel(sky.darkened(0.35), 0.1)
	# the rising sun and its rays, low on the flat
	_sphere(CENTER + Vector3(0, 4.5, -16.8), 4.2, Color(1.0, 0.86, 0.42), 0.9)
	for i in range(9 if lush else 5):
		var a := lerpf(-1.35, 1.35, float(i) / float((9 if lush else 5) - 1))
		var ray := _box(CENTER + Vector3(sin(a) * 7.5, 4.5 + cos(a) * 7.5, -16.9), Vector3(0.7, 6.0, 0.2),
			Color(1.0, 0.78, 0.42), 0.55)
		ray.rotation_degrees = Vector3(0, 0, -rad_to_deg(a))
	# the water below the sun, in bands
	for i in range(3):
		_box(CENTER + Vector3(0, 1.6 - float(i) * 0.9, -16.85), Vector3(32.0, 0.7, 0.2),
			Color(0.55, 0.4, 0.72).lightened(0.1 * float(i)), 0.2)
	# the paint cart in the left wing, the rinse station in the right
	_box(CENTER + Vector3(-19.5, 2.2, -12.0), Vector3(5.2, 0.5, 3.4), Color(0.72, 0.55, 0.42), 0.06)
	for i in range(4):
		_cyl(CENTER + Vector3(-21.2 + float(i) * 1.2, 2.9, -12.0), 0.5, 1.0,
			[Color(0.6, 0.32, 0.55), Color(0.95, 0.5, 0.45), Color(0.98, 0.94, 0.88), Color(0.4, 0.7, 0.8)][i], 0.25)
	_cyl(CENTER + Vector3(19.5, 1.6, -12.0), 1.8, 2.4, Color(0.85, 0.9, 0.95), 0.15)
	_sphere(CENTER + Vector3(19.5, 3.0, -12.0), 1.2, Color(0.55, 0.75, 0.9), 0.35)
	# the drop cloth under the easel, paint-spattered
	var cloth := _box(CENTER + Vector3(9.0, 0.42, -12.5), Vector3(12.0, 0.12, 9.0), Color(0.92, 0.9, 0.86), 0.08)
	cloth.name = "DropCloth"
	for i in range(7 if lush else 0):
		var a2 := float(i) * 1.3
		_sphere(CENTER + Vector3(9.0 + sin(a2) * 4.5, 0.52, -12.5 + cos(a2) * 3.2), 0.45,
			[Color(0.6, 0.32, 0.55), Color(0.95, 0.5, 0.45), Color(0.98, 0.9, 0.7)][i % 3], 0.2)

func _stage_launch_pad(spec: Dictionary) -> void:
	# Astronaut Engineer: a starfield with ringed planets, a teal deco skyline,
	# the circular launch platform and a mobile gantry beside the pipe wall.
	var lush := m.quality != "speedy"
	_backdrop_panel(Color(spec.get("backdrop", Color(0.16, 0.2, 0.4))), 0.05)
	# stars scattered across the flat
	for i in range(16 if lush else 7):
		var a := float(i) * 2.399
		_sphere(CENTER + Vector3(sin(a) * (3.0 + float(i) * 0.95), 4.0 + fmod(float(i) * 4.7, 10.0), -16.85),
			0.28 + fmod(float(i), 3.0) * 0.07, Color(1.0, 0.98, 0.9), 1.3)
	# a ringed planet upstage-left and a small moon upstage-right
	_sphere(CENTER + Vector3(-10.5, 11.0, -16.7), 2.4, Color(0.95, 0.72, 0.5), 0.35)
	var ring := _cyl(CENTER + Vector3(-10.5, 11.0, -16.6), 4.0, 0.2, Color(0.85, 0.8, 0.95), 0.4)
	ring.rotation_degrees = Vector3(74, 0, 18)
	_sphere(CENTER + Vector3(11.5, 12.2, -16.7), 1.5, Color(0.8, 0.88, 1.0), 0.4)
	# the teal deco skyline along the bottom of the flat
	for i in range(9 if lush else 5):
		var bh := 2.4 + fmod(float(i) * 3.1, 4.0)
		_box(CENTER + Vector3(-14.0 + float(i) * 3.5, bh * 0.5 + 0.9, -16.75), Vector3(2.4, bh, 0.3),
			Color(0.28, 0.55, 0.6).lightened(0.05 * float(i % 3)), 0.14)
	# the circular launch platform under centre stage, with its gold ring
	var pad := _cyl(CENTER + Vector3(0, 0.5, -6.0), 9.0, 0.35, Color(0.34, 0.5, 0.58), 0.12)
	pad.name = "LaunchPad"
	var pad_ring := _cyl(CENTER + Vector3(0, 0.66, -6.0), 9.4, 0.18, Color(1.0, 0.88, 0.55), 0.5)
	pad_ring.name = "LaunchPadRing"
	# the mobile gantry standing in the right wing
	for i in range(2):
		_box(CENTER + Vector3(19.0 + float(i) * 2.4, 5.5, -12.0), Vector3(0.5, 11.0, 0.5), Color(0.75, 0.5, 0.45), 0.08)
	for i in range(4):
		_box(CENTER + Vector3(20.2, 1.8 + float(i) * 3.0, -12.0), Vector3(3.0, 0.35, 2.4), Color(0.68, 0.46, 0.42), 0.08)

func _stage_grand_prix(spec: Dictionary) -> void:
	# Racecar Driver: the kart race takes over, so this set is the start-line
	# tableau — striped track running upstage, grandstand flats, zoom strips.
	var lush := m.quality != "speedy"
	_backdrop_panel(Color(spec.get("backdrop", Color(0.2, 0.22, 0.45))), 0.07)
	# swirling night sky on the flat
	for i in range(10 if lush else 4):
		var a := float(i) * 0.9
		var sw := _sphere(CENTER + Vector3(sin(a) * (4.0 + float(i)), 9.5 + cos(a) * 3.5, -16.8),
			1.5 + fmod(float(i), 3.0) * 0.4, Color(0.35, 0.4, 0.68), 0.3)
		sw.scale = Vector3(1.5, 0.6, 0.12)
	# the striped track: coral / teal / lavender / cream lanes running upstage
	var lane_cols: Array[Color] = [Color(0.95, 0.62, 0.62), Color(0.45, 0.78, 0.78),
		Color(0.72, 0.66, 0.9), Color(0.97, 0.94, 0.88)]
	for i in range(4):
		_box(CENTER + Vector3(-4.5 + float(i) * 3.0, 0.42, -6.0), Vector3(2.9, 0.12, 20.0), lane_cols[i], 0.16)
	# the starting arch over the track
	for sx: float in [-7.5, 7.5]:
		_box(CENTER + Vector3(sx, 4.5, 3.0), Vector3(1.0, 9.0, 1.0), Color(0.9, 0.62, 0.66), 0.1)
	_box(CENTER + Vector3(0, 9.3, 3.0), Vector3(16.0, 1.4, 1.2), Color(1.0, 0.86, 0.58), 0.2)
	for i in range(8 if lush else 0):
		_box(CENTER + Vector3(-7.0 + float(i) * 2.0, 8.4, 3.0), Vector3(1.8, 1.2, 0.3),
			Color(0.12, 0.12, 0.16) if i % 2 == 0 else Color(0.97, 0.96, 0.92), 0.1)
	# grandstand flats packed into the wings, plus padded barriers
	for sx: float in [-19.5, 19.5]:
		for tier in range(3):
			_box(CENTER + Vector3(sx, 2.0 + float(tier) * 2.0, -6.0), Vector3(5.0, 1.6, 16.0),
				Color(0.6, 0.52, 0.72).lightened(0.06 * float(tier)), 0.06)
		for i in range(4 if lush else 0):
			_sphere(CENTER + Vector3(sx, 6.6, -12.0 + float(i) * 4.5), 0.9,
				Color.from_hsv(float(i) / 4.0, 0.4, 1.0), 0.3)
		_box(CENTER + Vector3(sx - (2.9 if sx > 0.0 else -2.9), 1.2, -6.0), Vector3(1.0, 2.0, 16.0),
			Color(0.95, 0.55, 0.55), 0.12)

func _stage_starlight_concert(spec: Dictionary) -> void:
	# Pop Star: the dance overlay takes the screen, so this set is the concert
	# tableau — rainbow wall, speaker stacks, catwalk, glow-stick rails.
	var lush := m.quality != "speedy"
	_backdrop_panel(Color(spec.get("backdrop", Color(0.5, 0.42, 0.68))), 0.1)
	# the rainbow arcs across the flat
	var bow: Array[Color] = [Color(1.0, 0.62, 0.68), Color(1.0, 0.85, 0.55), Color(0.6, 0.9, 0.7),
		Color(0.55, 0.8, 1.0), Color(0.78, 0.66, 1.0)]
	for i in range(bow.size()):
		var arc := _cyl(CENTER + Vector3(0, 5.0, -16.8), 12.0 - float(i) * 1.7, 0.5, bow[i], 0.45)
		arc.rotation_degrees = Vector3(90, 0, 0)
	_box(CENTER + Vector3(0, 1.4, -16.7), Vector3(34.0, 8.0, 0.35), Color(spec.get("backdrop", Color(0.5, 0.42, 0.68))), 0.1)
	# speaker stacks in both wings
	for sx: float in [-19.5, 19.5]:
		for tier in range(3):
			_box(CENTER + Vector3(sx, 2.0 + float(tier) * 3.6, -11.0), Vector3(5.0, 3.2, 4.0),
				Color(0.28, 0.24, 0.36), 0.05)
			_cyl(CENTER + Vector3(sx + (2.1 if sx < 0.0 else -2.1), 2.0 + float(tier) * 3.6, -11.0), 1.1, 0.4,
				Color(0.6, 0.55, 0.7), 0.15)
		# the glow-stick rail the crowd waves from
		_box(CENTER + Vector3(sx, 2.4, 6.0), Vector3(0.5, 0.5, 14.0), Color(0.9, 0.75, 0.85), 0.2)
		for i in range(6 if lush else 0):
			_cyl(CENTER + Vector3(sx, 3.6, 0.5 + float(i) * 2.2), 0.22, 1.8,
				Color.from_hsv(float(i) / 6.0, 0.45, 1.0), 1.4)
	# the catwalk running downstage into the house
	var walk := _box(CENTER + Vector3(0, 0.5, 12.0), Vector3(7.0, 0.4, 14.0), Color(0.62, 0.48, 0.68), 0.14)
	walk.name = "Catwalk"
	for i in range(7 if lush else 3):
		_sphere(CENTER + Vector3(-3.2, 0.9, 6.0 + float(i) * 2.0), 0.32, Color(1.0, 0.9, 0.95), 1.2)
		_sphere(CENTER + Vector3(3.2, 0.9, 6.0 + float(i) * 2.0), 0.32, Color(1.0, 0.9, 0.95), 1.2)
	_footlights(Color(1.0, 0.8, 0.92))

func _card(fname: String, pos: Vector3, yaw: float = 0.0, card_scale: float = 2.0, parent: Node3D = null) -> Node3D:
	var full := "res://assets/art35/cards/" + fname + ".glb"
	if not ResourceLoader.exists(full):
		return null
	var packed := load(full) as PackedScene
	if packed == null:
		return null
	var prop := packed.instantiate() as Node3D
	if prop == null:
		return null
	prop.position = pos
	prop.rotation_degrees = Vector3(90.0, yaw, 0.0)
	prop.scale = Vector3.ONE * card_scale
	var target: Node3D = self if parent == null else parent
	target.add_child(prop)
	return prop

func _dress_world() -> void:
	var key := String(config.get("costume", ""))
	if key == "" and kind == "boss" and not bool(config.get("dual", false)) and not bool(config.get("finale", false)):
		key = "knight_boss"
	# a career with its own stage brings its own scenery — these generic wing
	# cards are the stopgap for careers still on the shared proscenium, and
	# they stand exactly where a dressed set puts its counters and shelving
	if STAGE_SETS.has(key):
		return
	if not DRESS.has(key):
		return
	for entry: Array in (DRESS[key] as Array):
		var pos := CENTER + Vector3(float(entry[1]), 0.4 + float(entry[3]), float(entry[2]))
		_card(String(entry[0]), pos, 0.0, float(entry[3]))

func _act_prop(fname: String, pos: Vector3, yaw: float = 0.0, parent: Node3D = null) -> Node3D:
	# authored opera GLBs (tools/build_opera_house_art.py) with null fallback
	var full := "res://assets/art35/opera/" + fname
	if not ResourceLoader.exists(full):
		return null
	var packed := load(full) as PackedScene
	if packed == null:
		return null
	var prop := packed.instantiate() as Node3D
	if prop == null:
		return null
	prop.position = pos
	prop.rotation_degrees.y = yaw
	var target: Node3D = self if parent == null else parent
	target.add_child(prop)
	return prop

func _build_theatre() -> void:
	# Owner 2026-07-25: a career listed in STAGE_SETS performs on its OWN set —
	# the proscenium, backdrop and deck take that job's palette and the job's
	# scenery is dressed in on top. Every career without an entry keeps the
	# shared toy theatre exactly as it was, so an undressed act can never break.
	var spec: Dictionary = STAGE_SETS.get(String(config.get("costume", "")), {})
	var trim: Color = Color(config.get("trim", Color(1.0, 0.85, 0.55)))
	var curtain: Color = Color(config.get("curtain", Color(0.78, 0.24, 0.34)))
	var floor_col := Color(spec.get("deck", config.get("floor_col", Color(0.52, 0.4, 0.62))))
	var pillar_col := Color(spec.get("pillar", trim))
	var beam_col := Color(spec.get("beam", trim))
	var back_col := Color(spec.get("backdrop", curtain))
	var wing_col := Color(spec.get("wing", curtain.darkened(0.12)))
	# stage deck + front apron edge
	_box(CENTER + Vector3(0, -0.3, -2.0), Vector3(52, 1.2, 34), floor_col)
	_box(CENTER + Vector3(0, 0.15, 15.2), Vector3(52, 0.5, 1.6), trim, 0.2)
	# proscenium: two gold pillars + top beam
	_box(CENTER + Vector3(-23.0, 8.0, 12.0), Vector3(2.2, 17, 2.2), pillar_col, 0.12)
	_box(CENTER + Vector3(23.0, 8.0, 12.0), Vector3(2.2, 17, 2.2), pillar_col, 0.12)
	_box(CENTER + Vector3(0, 16.6, 12.0), Vector3(48.2, 2.6, 2.4), beam_col, 0.12)
	# back curtain + gathered side curtains
	_box(CENTER + Vector3(0, 7.5, -18.0), Vector3(46, 16, 1.4), back_col)
	_box(CENTER + Vector3(-21.0, 7.5, -3.0), Vector3(2.6, 16, 30), wing_col)
	_box(CENTER + Vector3(21.0, 7.5, -3.0), Vector3(2.6, 16, 30), wing_col)
	# string lights along the beam (emissive spheres only — zero OmniLights)
	for i in range(6):
		var hue := Color.from_hsv(float(i) / 6.0, 0.4, 1.0)
		_sphere(CENTER + Vector3(-15.0 + float(i) * 6.0, 15.0, 12.8), 0.55, hue, 1.4)
	# two soft spotlight cones aimed at centre stage
	for sx in [-14.0, 14.0]:
		var cone := CylinderMesh.new()
		cone.top_radius = 0.3
		cone.bottom_radius = 3.4
		cone.height = 12.0
		var beam := _mesh(cone, CENTER + Vector3(sx, 9.0, 4.0), Color(1.0, 0.95, 0.7, 0.16), 0.5)
		var bm := beam.material_override as StandardMaterial3D
		bm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		bm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		beam.rotation_degrees = Vector3(0, 0, signf(sx) * -16.0)
	# the audience: four friend cutouts on toy benches past the apron
	var seat_col := Color(0.32, 0.26, 0.5)
	var guests: Array[String] = ["pearl_friend", "two_friends", "mama_baby", "wacky_chuck"]
	for i in range(guests.size()):
		var gx := -13.5 + float(i) * 9.0
		_box(CENTER + Vector3(gx, 0.9, 21.5), Vector3(6.5, 1.4, 3.2), seat_col)
		var spr := Sprite3D.new()
		var tex := m._cutout_tex(guests[i])
		spr.texture = tex
		spr.pixel_size = 5.4 / maxf(float(tex.get_height()), 1.0) if tex != null else 0.01
		spr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		spr.position = CENTER + Vector3(gx, 4.0, 22.4)
		add_child(spr)
		audience.append(spr)
	if not spec.is_empty():
		_build_job_stage(spec)

func _build_backstage() -> void:
	# the corridor: warm wooden boards, prop crates, string lights, and the
	# big side curtain that opens onto the main stage once the imps pop
	_box(CENTER + Vector3((BACKSTAGE_X0 + BACKSTAGE_X1) * 0.5, -0.3, 3.0), Vector3(BACKSTAGE_X1 - BACKSTAGE_X0 + 4.0, 1.2, 20.0), Color(0.5, 0.36, 0.28))
	_box(CENTER + Vector3(BACKSTAGE_X0 - 1.0, 5.0, 3.0), Vector3(1.2, 12.0, 20.0), Color(0.32, 0.24, 0.3))
	for cx in [-52.0, -44.0, -33.0]:
		_box(CENTER + Vector3(cx, 1.3, -4.5), Vector3(3.0, 2.6, 3.0), Color(0.62, 0.46, 0.3))
		_box(CENTER + Vector3(cx, 3.1, -4.5), Vector3(2.2, 1.0, 2.2), Color(0.55, 0.4, 0.27))
	for i in range(4):
		_sphere(CENTER + Vector3(-54.0 + float(i) * 8.0, 10.0, 3.0), 0.45, Color.from_hsv(float(i) / 4.0, 0.35, 1.0), 1.2)
	# the gate: a tall crimson curtain wall blocking the way to the stage
	gate_curtain = _box(CENTER + Vector3(BACKSTAGE_X1 + 1.0, 6.5, 3.0), Vector3(1.6, 14.0, 20.0), Color(config.get("curtain", Color(0.78, 0.24, 0.34))))
	# three mischief imps between Roshan and the curtain — the same little
	# demons from the dungeon, reused on purpose (they get everywhere)
	imp_count = int(config.get("imps", 4))
	# Imps must spawn INSIDE the stretch of corridor _clamp_player() lets Roshan
	# reach (BACKSTAGE_X0 + 2 .. BACKSTAGE_X1 - 1.5). The old fixed 5.5 spacing
	# put the last two imps of a six-imp act past the far wall, where she could
	# only ever swat at them from the clamp line.
	var imp_x0 := BACKSTAGE_X0 + 6.0
	var imp_x1 := BACKSTAGE_X1 - 4.0
	for g in range(imp_count):
		var t := float(g) / maxf(1.0, float(imp_count - 1))
		var pos := CENTER + Vector3(lerpf(imp_x0, imp_x1, t), 1.0, -1.0 + float(g % 2) * 7.0)
		# the LAST imp is the captain: bigger, wears a gold bow, and shrugs off
		# the first sparkle with a giggle-dash — every brawl ends on a mini-chase
		_spawn_imp(pos, g == imp_count - 1)
	imps_left = imp_count

func _spawn_imp(pos: Vector3, captain: bool) -> void:
	var root := Node3D.new()
	root.name = "MischiefImp%d" % imps.size()
	root.position = pos
	add_child(root)
	var imp := DungeonArt.spawn("imp", root)
	if imp.name.begins_with("MissingDungeonArt"):
		_sphere(Vector3(0, 1.2, 0), 0.9, Color(0.55, 0.35, 0.75), 0.3, root)
		_sphere(Vector3(-0.3, 1.9, 0.5), 0.2, Color(1.0, 0.9, 0.4), 0.8, root)
		_sphere(Vector3(0.3, 1.9, 0.5), 0.2, Color(1.0, 0.9, 0.4), 0.8, root)
	if captain:
		root.scale = Vector3.ONE * 1.45
		_sphere(Vector3(0, 2.4, 0.3), 0.28, Color(1.0, 0.85, 0.4), 0.7, root)
	imps.append({"index": imps.size(), "node": root, "pos": pos, "popped": false,
		"phase": float(imps.size()) * 2.1, "hp": 2 if captain else 1})

func _brawl_action() -> void:
	# the brawler verb: a sparkle star pops the nearest imp into confetti.
	# Out of reach = the star falls short, exactly like the boss fights.
	if state != "play" or stage_phase != "brawl":
		return
	var best := -1
	var best_d := 8.0
	for g in imps:
		if bool(g["popped"]):
			continue
		var d: float = (g["pos"] as Vector3).distance_to(player_pos)
		if d < best_d:
			best_d = d
			best = int(g["index"])
	if best < 0:
		m._sparkle_burst(player_pos + Vector3(0, 2.5, 0), Color(0.8, 0.85, 1.0))
		return
	var imp: Dictionary = imps[best]
	progress_t = 0.0
	imp["hp"] = int(imp.get("hp", 1)) - 1
	if int(imp["hp"]) > 0:
		# the captain giggles off the first star and dashes down the corridor
		var gpos0: Vector3 = imp["pos"] as Vector3
		m._sparkle_burst(gpos0 + Vector3(0, 2.5, 0), Color(1.0, 0.85, 0.4))
		var mid := CENTER.x + (BACKSTAGE_X0 + BACKSTAGE_X1) * 0.5
		var dash_x := CENTER.x + BACKSTAGE_X0 + 7.0 if player_pos.x > mid else CENTER.x + BACKSTAGE_X1 - 7.0
		var dash := Vector3(dash_x, 1.0, CENTER.z + randf_range(-1.0, 6.0))
		imp["pos"] = dash
		(imp["node"] as Node3D).position = dash
		if m.chime != null:
			m.chime.pitch_scale = 0.8
			m.chime.play()
		m.show_msg("Roshan", "The big imp captain giggled and dashed away — chase him! One more SPARKLE!", "talk")
		_update_hud()
		return
	imp["popped"] = true
	imps_left -= 1
	var node := imp["node"] as Node3D
	var gpos: Vector3 = imp["pos"] as Vector3
	m._sparkle_burst(gpos + Vector3(0, 2.5, 0), Color(1.0, 0.85, 0.4))
	for c in range(5):
		var a := float(c) * TAU / 5.0
		var confetti := _sphere(gpos + Vector3(cos(a) * 0.8, 1.5, sin(a) * 0.8), 0.35, Color.from_hsv(float(c) / 5.0, 0.6, 1.0), 0.5)
		var tw := confetti.create_tween()
		tw.tween_property(confetti, "position", confetti.position + Vector3(cos(a) * 2.5, 3.0, sin(a) * 2.5), 0.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(confetti, "scale", Vector3.ZERO, 0.3)
		tw.tween_callback(confetti.queue_free)
	node.visible = false
	if m.chime != null:
		m.chime.pitch_scale = 1.0 + 0.2 * float(imp_count - imps_left)
		m.chime.play()
	if imps_left <= 0:
		_open_gate()
	else:
		_update_hud()

# ---------------- "box" engine (boxer: friendly ring combat in rounds) ----------------

func _build_box() -> void:
	# a toy boxing ring mid-stage: canvas deck, corner posts, gold ropes.
	# Straightforward combat (owner 2026-07-21): rounds of mischief imps hop
	# the ropes, Roshan bops them with PUNCH, the bell rings the next round.
	_box(CENTER + Vector3(0, 0.35, -2.0), Vector3(24, 0.7, 20), Color(0.94, 0.9, 0.82))
	for cx: float in [-11.0, 11.0]:
		for cz: float in [-11.0, 7.0]:
			_cyl(CENTER + Vector3(cx, 2.4, cz), 0.45, 4.8, Color(0.85, 0.3, 0.4), 0.2)
	for ry: float in [1.7, 3.1]:
		_box(CENTER + Vector3(0, ry, -12.0), Vector3(22.6, 0.26, 0.26), Color(1.0, 0.85, 0.45), 0.3)
		_box(CENTER + Vector3(0, ry, 8.0), Vector3(22.6, 0.26, 0.26), Color(1.0, 0.85, 0.45), 0.3)
		_box(CENTER + Vector3(-11.0, ry, -2.0), Vector3(0.26, 0.26, 20.6), Color(1.0, 0.85, 0.45), 0.3)
		_box(CENTER + Vector3(11.0, ry, -2.0), Vector3(0.26, 0.26, 20.6), Color(1.0, 0.85, 0.45), 0.3)
	# card kit: padded caps, shell bell, progress lamps, belt pedestal —
	# dressing only, laid over the SAME gameplay-authoritative footprint
	boxer_dressing_art = _job_art("boxer/opera_boxer_dressing.glb", self)
	if boxer_dressing_art != null:
		boxer_dressing_art.position = CENTER
		for lamp in range(3):
			_job_state(boxer_dressing_art, "StateLamp%d" % lamp, false)
		_job_state(boxer_dressing_art, "StateComplete", false)
	else:
		# the round bell on the front post
		_sphere(CENTER + Vector3(-11.0, 5.2, 7.0), 0.7, Color(1.0, 0.85, 0.4), 0.5)
	player_pos = CENTER + Vector3(0, 1.1, 4.0)
	box_round = 0
	box_wait = 0.0
	# Beat 1 (owner pacing standard 2026-07-25): a training-bag warm-up before
	# the bell. Different verb from the rounds — the bag never runs away, it
	# swings back, so this beat is about timing instead of chasing.
	box_bag_goal = int(config.get("warmup", 0))
	if box_bag_goal <= 0:
		box_phase = "rounds"
		_box_wave()
		return
	box_phase = "warmup"
	box_bag = Node3D.new()
	box_bag.name = "TrainingBag"
	box_bag.position = CENTER + Vector3(0, 0, -6.0)
	add_child(box_bag)
	_cyl(Vector3(0, 6.2, 0), 0.16, 3.2, Color(0.82, 0.72, 0.52), 0.1, box_bag)
	_cyl(Vector3(0, 3.0, 0), 1.5, 4.4, Color(0.86, 0.42, 0.44), 0.14, box_bag)
	_sphere(Vector3(0, 5.1, 0), 1.5, Color(0.92, 0.54, 0.54), 0.16, box_bag)
	_sphere(Vector3(0, 0.9, 0), 1.5, Color(0.92, 0.54, 0.54), 0.16, box_bag)
	m.show_msg("Roshan", "Warm up first, champ! Bop the big swinging bag %d times with PUNCH!" % box_bag_goal, "talk")

func _box_wave() -> void:
	box_phase = "rounds"
	var waves: Array = config.get("rounds", [3, 4, 5])
	var count := int(waves[mini(box_round, waves.size() - 1)])
	imps.clear()
	var last_round := box_round >= waves.size() - 1
	for g in range(count):
		var a := float(g) * TAU / float(count)
		var pos := CENTER + Vector3(cos(a) * 7.5, 1.0, -2.0 + sin(a) * 6.5)
		_spawn_imp(pos, last_round and g == count - 1)
	imps_left = count
	if m.chime != null:
		m.chime.pitch_scale = 1.5
		m.chime.play()
	m.show_msg("Roshan", "DING DING! Round %d — bop the mischief imps with PUNCH!" % (box_round + 1), "talk")
	_update_hud()

func _punch_action() -> void:
	if state != "play" or kind != "box" or box_wait > 0.0:
		return
	if box_phase == "warmup":
		_bag_action()
		return
	if box_phase == "belt":
		return
	var best := -1
	var best_d := 6.5
	for g in imps:
		if bool(g["popped"]):
			continue
		var d: float = (g["pos"] as Vector3).distance_to(player_pos)
		if d < best_d:
			best_d = d
			best = int(g["index"])
	if best < 0:
		m._sparkle_burst(player_pos + Vector3(0, 2.5, 0), Color(0.8, 0.85, 1.0))
		return
	var imp: Dictionary = imps[best]
	progress_t = 0.0
	imp["hp"] = int(imp.get("hp", 1)) - 1
	var gpos: Vector3 = imp["pos"] as Vector3
	if int(imp["hp"]) > 0:
		# the captain bounces off the ropes and comes back for one more
		m._sparkle_burst(gpos + Vector3(0, 2.5, 0), Color(1.0, 0.85, 0.4))
		var away := gpos - player_pos
		away.y = 0.0
		if away.length() < 0.1:
			away = Vector3.FORWARD
		var dash := gpos + away.normalized() * 9.0
		dash.x = clampf(dash.x, CENTER.x - 9.5, CENTER.x + 9.5)
		dash.z = clampf(dash.z, CENTER.z - 10.5, CENTER.z + 6.5)
		imp["pos"] = dash
		(imp["node"] as Node3D).position = dash
		m.show_msg("Roshan", "The captain bounced off the ropes — one more PUNCH!", "talk")
		_update_hud()
		return
	imp["popped"] = true
	imps_left -= 1
	(imp["node"] as Node3D).visible = false
	m._sparkle_burst(gpos + Vector3(0, 2.5, 0), Color(1.0, 0.7, 0.4))
	if m.chime != null:
		m.chime.pitch_scale = 1.0 + 0.15 * float(box_round + 1)
		m.chime.play()
	if imps_left <= 0:
		var waves: Array = config.get("rounds", [3, 4, 5])
		box_round += 1
		_job_state(boxer_dressing_art, "StateLamp%d" % (box_round - 1), true)
		if box_round >= waves.size():
			_begin_belt()
			return
		box_wait = 1.6
		m.show_msg("Roshan", "Round %d won! Shake it out, champ..." % box_round, "talk")
	_update_hud()

func _bag_action() -> void:
	# out of reach = the punch swishes, exactly like every other act's verb
	if box_bag == null or box_bag.position.distance_to(player_pos) > 8.0:
		m._sparkle_burst(player_pos + Vector3(0, 2.5, 0), Color(0.85, 0.9, 1.0))
		return
	box_bag_hits += 1
	progress_t = 0.0
	var away := signf(box_bag.position.x - player_pos.x)
	if absf(away) < 0.1:
		away = 1.0
	var tw := box_bag.create_tween()
	tw.tween_property(box_bag, "rotation:z", -0.5 * away, 0.18).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(box_bag, "rotation:z", 0.22 * away, 0.3)
	tw.tween_property(box_bag, "rotation:z", 0.0, 0.35)
	m._sparkle_burst(box_bag.position + Vector3(0, 3.4, 0), Color(1.0, 0.82, 0.5))
	if m.chime != null:
		m.chime.pitch_scale = 0.9 + 0.12 * float(box_bag_hits)
		m.chime.play()
	if box_bag_hits >= box_bag_goal:
		box_phase = "rounds"
		var fade := box_bag.create_tween()
		fade.tween_property(box_bag, "scale", Vector3.ZERO, 0.4).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
		m.show_msg("Roshan", "Warmed up and ready! Here comes the bell...", "talk")
		box_wait = 1.4
	else:
		m.show_msg("Roshan", "POW! %d more!" % (box_bag_goal - box_bag_hits), "hint")
	_update_hud()

func _begin_belt() -> void:
	# Beat 3: the belt descends over the ring and Roshan swims up to take it.
	# A pure victory-lap beat — nothing to get wrong, and nothing to wait on.
	box_phase = "belt"
	_job_state(boxer_dressing_art, "StateIdle", false)
	_job_state(boxer_dressing_art, "StateComplete", true)
	box_belt = Node3D.new()
	box_belt.name = "ChampionBelt"
	box_belt.position = CENTER + Vector3(0, 12.0, -2.0)
	add_child(box_belt)
	var strap := _cyl(Vector3.ZERO, 1.8, 0.55, Color(0.55, 0.34, 0.3), 0.15, box_belt)
	strap.rotation_degrees = Vector3(90, 0, 0)
	_sphere(Vector3(0, 0, 0.6), 1.0, Color(1.0, 0.86, 0.42), 0.9, box_belt)
	var drop := box_belt.create_tween()
	drop.tween_property(box_belt, "position", CENTER + Vector3(0, 4.2, -2.0), 1.1).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	m.show_msg("Roshan", "CHAMPION! Swim up and take your championship belt!", "talk")
	_update_hud()

func _tick_box(delta: float) -> void:
	if box_phase == "belt":
		if box_belt != null:
			box_belt.rotation.y += delta * 1.2
			box_belt.position.y = CENTER.y + 4.2 + sin(elapsed * 2.0) * 0.35
			if Vector2(box_belt.position.x - player_pos.x, box_belt.position.z - player_pos.z).length() < 4.5:
				m._sparkle_burst(box_belt.position, Color(1.0, 0.9, 0.5))
				_win()
		return
	if box_phase == "warmup":
		if box_wait > 0.0:
			box_wait -= delta
			if box_wait <= 0.0:
				_box_wave()
			return
		if box_bag != null:
			box_bag.position.y = CENTER.y + sin(elapsed * 1.6) * 0.2
		_tick_pointer()
		return
	if box_wait > 0.0:
		box_wait -= delta
		if box_wait <= 0.0:
			_box_wave()
		return
	brawl_bump_cool = maxf(0.0, brawl_bump_cool - delta)
	for g in imps:
		if bool(g["popped"]):
			continue
		var node := g["node"] as Node3D
		var pos: Vector3 = g["pos"] as Vector3
		var toward: Vector3 = player_pos - pos
		toward.y = 0.0
		if toward.length() > 4.0:
			pos += toward.normalized() * delta * 2.0
		g["pos"] = pos
		node.position = pos + Vector3(0, sin(elapsed * 3.0 + float(g["phase"])) * 0.3, 0)
		node.rotation.y = sin(elapsed * 2.0 + float(g["phase"])) * 0.4
		if pos.distance_to(player_pos) < 2.5:
			var away2: Vector3 = player_pos - pos
			away2.y = 0.0
			if away2.length() < 0.1:
				away2 = Vector3.FORWARD
			player_pos += away2.normalized() * 2.5
			m._sparkle_burst(player_pos + Vector3(0, 2.0, 0), Color(0.55, 0.92, 1.0))
			if brawl_bump_cool <= 0.0:
				brawl_bump_cool = 4.0
				m.show_msg("Roshan", "My bubble shield! Tap PUNCH to bop those silly imps!", "talk")

# ---------------- "sleuth" engine (detective: peek-in-props search) ----------------

func _build_sleuth() -> void:
	# six oversized prop boxes hide three clues — peek inside each one. A
	# wrong box giggles a silly fish out (never a fail); the right ones float
	# their clue to the tiara chest, and three clues open the case.
	var prop_count := int(config.get("props_n", 6))
	var clue_count := int(config.get("clues", 3))
	var clue_cols := _order_colors("clue")
	goal = Node3D.new()
	goal.name = "TiaraChest"
	goal.position = CENTER + Vector3(0, 1.0, -12.0)
	add_child(goal)
	sleuth_chest_art = _job_art("detective/opera_detective_chest.glb", goal)
	if sleuth_chest_art != null:
		_job_state(sleuth_chest_art, "StateActive", false)
		_job_state(sleuth_chest_art, "StateComplete", false)
	else:
		_box(Vector3(0, 0.8, 0), Vector3(3.4, 1.6, 2.2), Color(0.55, 0.38, 0.22), 0.05, goal)
		_box(Vector3(0, 1.8, -0.6), Vector3(3.4, 0.6, 1.0), Color(0.62, 0.44, 0.26), 0.05, goal)
	var clue_picks: Array[int] = []
	while clue_picks.size() < clue_count:
		var pick := randi() % prop_count
		if not clue_picks.has(pick):
			clue_picks.append(pick)
	for i in range(prop_count):
		var px := -18.0 + float(i) * (36.0 / maxf(1.0, float(prop_count - 1)))
		var pos := CENTER + Vector3(px, 1.0, -7.0 + float(i % 2) * 12.0)
		var root := Node3D.new()
		root.name = "SearchProp%d" % i
		root.position = pos
		add_child(root)
		# card kits: six DIFFERENT box silhouettes, each with a tweenable Lid
		var lid: Node3D = null
		var kit := _job_art("detective/opera_detective_box_%d.glb" % i, root)
		if kit != null:
			lid = kit.find_child("Lid", true, false) as Node3D
		if lid == null:
			_box(Vector3(0, 1.1, 0), Vector3(2.6, 2.2, 2.6), Color(0.72, 0.56, 0.4), 0.05, root)
			lid = _box(Vector3(0, 2.4, 0), Vector3(2.9, 0.5, 2.9), Color(0.6, 0.44, 0.3), 0.1, root)
		var has_clue := clue_picks.has(i)
		sleuth_props.append({"index": i, "pos": pos, "node": root, "lid": lid,
			"opened": false, "clue": has_clue, "col": clue_cols[clue_picks.find(i) % clue_cols.size()] if has_clue else Color.WHITE})

func _sleuth_action(idx: int) -> void:
	if state != "play" or kind != "sleuth":
		return
	var prop: Dictionary = sleuth_props[idx]
	if bool(prop["opened"]):
		return
	prop["opened"] = true
	progress_t = 0.0
	var lid := prop["lid"] as Node3D
	var lt := lid.create_tween()
	lt.tween_property(lid, "position:y", lid.position.y + 1.6, 0.25).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	lt.tween_property(lid, "rotation:z", 0.5, 0.2)
	if bool(prop["clue"]):
		clues_found += 1
		var clue := _sphere((prop["pos"] as Vector3) + Vector3(0, 3.0, 0), 0.65, Color(prop["col"]), 0.7)
		var ct := clue.create_tween()
		ct.tween_property(clue, "position", goal.position + Vector3(-1.0 + float(clues_found) * 1.0, 3.2, 0), 0.8).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
		m._sparkle_burst((prop["pos"] as Vector3) + Vector3(0, 3.0, 0), Color(1.0, 0.9, 0.5))
		if m.chime != null:
			m.chime.pitch_scale = 1.0 + 0.2 * float(clues_found)
			m.chime.play()
		if clues_found >= 3:
			chest_ready = true
			_job_state(sleuth_chest_art, "StateActive", true)
			m._sparkle_burst(goal.position + Vector3(0, 3.0, 0), Color(1.0, 0.85, 0.4))
			m.show_msg("Roshan", "All three clues! Now tap the treasure chest to solve the case!", "talk")
		else:
			m.show_msg("Roshan", "A clue! %d more to find!" % (3 - clues_found), "talk")
	else:
		# a silly fish hides in the wrong boxes — a giggle, never a fail
		var fish: Node3D = _act_prop("opera_silly_fish.glb", (prop["pos"] as Vector3) + Vector3(0, 2.6, 0))
		if fish == null:
			fish = _sphere((prop["pos"] as Vector3) + Vector3(0, 2.6, 0), 0.55, Color(0.5, 0.85, 1.0), 0.4)
		var ft := fish.create_tween()
		ft.tween_property(fish, "position:y", fish.position.y + 2.2, 0.4).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		ft.tween_property(fish, "scale", Vector3.ZERO, 0.3)
		ft.tween_callback(fish.queue_free)
		if m.chime != null:
			m.chime.pitch_scale = 0.7
			m.chime.play()
		m.show_msg("Roshan", "Just a silly fish! Keep looking, detective!", "hint")
	_update_hud()

func _sleuth_chest() -> void:
	if state != "play" or kind != "sleuth" or not chest_ready:
		return
	# the tiara reveal: the chest bursts open in gold
	m._sparkle_burst(goal.position + Vector3(0, 3.5, 0), Color(1.0, 0.9, 0.4))
	m._sparkle_burst(goal.position + Vector3(0, 5.0, 0), Color(1.0, 0.75, 0.9))
	if sleuth_chest_art != null:
		# the kit's open lid + risen pearl tiara IS the reveal
		_job_state(sleuth_chest_art, "StateIdle", false)
		_job_state(sleuth_chest_art, "StateComplete", true)
	else:
		var crown := _sphere(goal.position + Vector3(0, 3.0, 0), 0.8, Color(1.0, 0.88, 0.4), 0.8)
		var tw := crown.create_tween()
		tw.tween_property(crown, "position:y", crown.position.y + 2.0, 0.6).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	_win()

func _open_gate() -> void:
	stage_phase = "puzzle"
	progress_t = 0.0
	if gate_curtain != null:
		var tw := gate_curtain.create_tween()
		tw.tween_property(gate_curtain, "position:y", gate_curtain.position.y + 13.0, 1.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
	m._sparkle_burst(CENTER + Vector3(BACKSTAGE_X1 + 1.0, 4.0, 3.0), Color(1.0, 0.9, 0.5))
	if m.chime != null:
		m.chime.pitch_scale = 1.4
		m.chime.play()
	m.show_msg("Roshan", String(config.get("voice", "The stage is clear — on with the show!")), "talk")
	_update_hud()

func _tick_brawl(delta: float) -> void:
	brawl_bump_cool = maxf(0.0, brawl_bump_cool - delta)
	for g in imps:
		if bool(g["popped"]):
			continue
		var node := g["node"] as Node3D
		var pos: Vector3 = g["pos"] as Vector3
		var toward: Vector3 = player_pos - pos
		toward.y = 0.0
		if toward.length() > 4.5:
			pos += toward.normalized() * delta * 1.6
		g["pos"] = pos
		node.position = pos + Vector3(0, sin(elapsed * 3.0 + float(g["phase"])) * 0.3, 0)
		node.rotation.y = sin(elapsed * 2.0 + float(g["phase"])) * 0.4
		# an imp that reaches Roshan just bounces off her bubble shield
		if pos.distance_to(player_pos) < 2.5:
			var away: Vector3 = player_pos - pos
			away.y = 0.0
			if away.length() < 0.1:
				away = Vector3.FORWARD
			player_pos += away.normalized() * 2.5
			m._sparkle_burst(player_pos + Vector3(0, 2.0, 0), Color(0.55, 0.92, 1.0))
			if brawl_bump_cool <= 0.0:
				brawl_bump_cool = 4.0
				m.show_msg("Roshan", "My bubble shield! Tap SPARKLE to pop those silly mischief imps!", "talk")

func _build_avatar() -> void:
	# The stage Roshan is the REAL rigged 3D player in puppet mode: the act
	# drives her position/yaw while player.gd's procedural swim keeps her
	# alive, and the career costume rides her bones (BoneAttachment3D) — so
	# every career look reuses the one animation set, exactly like the
	# plushie skins do. The lobby's cutout stays a cutout; walking through a
	# door is the transformation moment.
	m.player.visible = true
	m.player.puppet = true
	m.player.puppet_speed = 0.0
	m.player.vel = Vector3.ZERO
	m.player.rotation = Vector3(0, PI, 0)   # face the audience side (+Z)
	m.player.position = player_pos
	m.player.set_costume(String(config.get("costume", "")))

func _release_avatar() -> void:
	# hand Roshan back: costume off, puppet strings cut, hidden again until
	# the lobby (cutout) or the reef (main._end_opera flips her visible)
	if m == null or m.player == null or not is_instance_valid(m.player):
		return
	m.player.puppet = false
	m.player.puppet_speed = 0.0
	m.player.clear_costume()
	m.player.visible = false

func _place_avatar(delta: float) -> void:
	# drive the puppet: bob like the old cutout did, face the way she moves,
	# and report her speed so the tail beat matches the act's pace
	var target: Vector3 = player_pos + Vector3(0, sin(elapsed * 4.0) * 0.12, 0)
	var dp: Vector3 = target - m.player.position
	var planar := Vector2(dp.x, dp.z)
	# clamped so a stage teleport (brawl warp, probe drive) reads as a dash,
	# not a one-frame tail scramble
	m.player.puppet_speed = minf(planar.length() / maxf(delta, 0.001), MOVE_SPEED * 2.0)
	if planar.length() > 0.04:
		m.player.rotation.y = lerp_angle(m.player.rotation.y, atan2(planar.x, planar.y) + PI, 1.0 - pow(0.002, delta))
	m.player.position = target

func _build_camera() -> void:
	cam = Camera3D.new()
	cam.fov = 56.0
	cam.position = CENTER + Vector3(0, 24.0, 34.0)
	add_child(cam)
	cam.look_at(CENTER + Vector3(0, 2.5, -2.0), Vector3.UP)
	cam.make_current()

func _build_hud() -> void:
	hud = CanvasLayer.new()
	hud.layer = 14
	add_child(hud)
	var banner := Panel.new()
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.07, 0.045, 0.14, 0.88)
	style.border_color = Color(config.get("trim", Color(1.0, 0.85, 0.55)))
	style.set_border_width_all(4)
	style.set_corner_radius_all(22)
	banner.add_theme_stylebox_override("panel", style)
	banner.position = Vector2(220, 22)
	banner.size = Vector2(840, 112)
	banner.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(banner)
	objective = Label.new()
	objective.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	objective.add_theme_font_size_override("font_size", 28)
	objective.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.08))
	objective.add_theme_constant_override("outline_size", 8)
	objective.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	objective.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	objective.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	objective.mouse_filter = Control.MOUSE_FILTER_IGNORE
	banner.add_child(objective)
	pointer = Label3D.new()
	pointer.text = "▼"
	pointer.font_size = 150
	pointer.pixel_size = 0.022
	pointer.outline_size = 24
	pointer.modulate = Color(1.0, 0.94, 0.25)
	pointer.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(pointer)

# ------- shared pad core: "order" (chef) and "paint" (painter) -------
# Two distinct acts share this builder because both walk a pictured sequence,
# but they diverge immediately: chef DELIVERS layers then stirs and tops the
# cake, painter LOADS a brush then swipes and splatters the canvas. They carry
# separate kinds so the roster reads one engine per career.

func _is_order_kind() -> bool:
	return kind == "order" or kind == "paint"


func _build_order() -> void:
	var steps: Array = config.get("order", [0, 1, 2])
	for v in steps:
		order_steps.append(int(v))
	order_flow = String(config.get("flow", "deliver"))
	order_hidden = bool(config.get("hide_props", false))
	var theme := String(config.get("props", "cake"))
	var cols := _order_colors(theme)
	for i in range(cols.size()):
		var pos := CENTER + Vector3(-12.0 + float(i) * 12.0, 1.0, 5.0)
		var root := Node3D.new()
		root.name = "OperaPad%d" % i
		root.position = pos
		add_child(root)
		_cyl(Vector3(0, -0.4, 0), 2.6, 0.5, cols[i].darkened(0.4), 0.0, root)
		var prop := _order_prop(theme, i, cols[i], root)
		if order_hidden:
			prop.visible = false   # pops out with a sparkle when Roshan swims close
		pads.append({"index": i, "node": root, "pos": pos, "prop": prop, "revealed": not order_hidden})
	# the goal prop at centre-back: bowl / tiara chest / easel canvas
	goal = Node3D.new()
	goal.name = "OperaGoal"
	goal.position = CENTER + Vector3(0, 1.0, -11.0)
	add_child(goal)
	match theme:
		"clue":
			_box(Vector3(0, 0.7, 0), Vector3(3.0, 1.4, 2.0), Color(0.62, 0.42, 0.2), 0.0, goal)
			_box(Vector3(0, 1.5, 0), Vector3(3.0, 0.5, 2.0), Color(1.0, 0.85, 0.4), 0.3, goal)
		"paint":
			if _job_art("painter/opera_painter_easel.glb", goal) == null:
				_box(Vector3(0, 2.6, 0), Vector3(6.4, 4.6, 0.4), Color(0.96, 0.94, 0.88), 0.1, goal)
				_box(Vector3(0, 0.3, 0.6), Vector3(5.0, 0.6, 0.6), Color(0.55, 0.38, 0.24), 0.0, goal)
		_:
			chef_bowl_art = _job_art("pastry_chef/opera_pastry_chef_bowl.glb", goal)
			if chef_bowl_art != null:
				_job_state(chef_bowl_art, "StateActive", false)
				_job_state(chef_bowl_art, "StateComplete", false)
				# scenic oven alcove behind the stage (closed until the win)
				chef_oven_art = _job_art("pastry_chef/opera_pastry_chef_oven.glb", self)
				if chef_oven_art != null:
					chef_oven_art.position = CENTER + Vector3(10.5, 1.0, -14.0)
					chef_oven_art.rotation.y = -0.35
					_job_state(chef_oven_art, "StateActive", false)
			else:
				var bowl := CylinderMesh.new()
				bowl.top_radius = 2.4
				bowl.bottom_radius = 1.5
				bowl.height = 1.6
				_mesh(bowl, Vector3(0, 0.8, 0), Color(0.85, 0.9, 1.0), 0.1, goal)
	# the picture recipe: small copies above the goal, left-to-right = the order
	if not reveal_one:
		for s in range(order_steps.size()):
			var ci := order_steps[s]
			_sphere(goal.position + Vector3((float(s) - float(order_steps.size() - 1) * 0.5) * 3.2, 5.8, 0), 0.8, cols[ci], 0.5)
	if order_flow == "carry_paint":
		canvas_pos = goal.position + Vector3(0, 3.6, 0)
		_build_paint_canvas()
		brush_node = Node3D.new()
		brush_node.name = "PaintBrush"
		brush_node.visible = false
		add_child(brush_node)
		_box(Vector3(0, 0, 0), Vector3(0.2, 1.4, 0.2), Color(0.6, 0.4, 0.25), 0.0, brush_node)
		_box(Vector3(0, 0.9, 0), Vector3(0.32, 0.5, 0.32), Color(0.9, 0.9, 0.95), 0.3, brush_node)

func _order_colors(theme: String) -> Array[Color]:
	match theme:
		"clue":
			return [Color(0.62, 0.45, 0.3), Color(0.55, 0.85, 1.0), Color(1.0, 0.6, 0.8)]
		"paint":
			# LOCKED cue palette (handoff continuity): coral / cream / plum,
			# so the live [2, 0, 1, 2] order reads plum, coral, cream, plum
			return [Color(0.86, 0.42, 0.38), Color(0.93, 0.87, 0.78), Color(0.55, 0.36, 0.66)]
		_:
			# the accepted card palette (vanilla / coral / plum) — the recipe
			# tokens must match the 3D layer art so a non-reader can pair them
			return [Color(0.94, 0.8, 0.52), Color(0.86, 0.42, 0.38), Color(0.55, 0.36, 0.66)]

# ---------------- opera job 3D art (flat-card interpretations) ----------------
# GLB kits built from the accepted 1024 cards (see
# CLAUDE_OPERA_JOB_3D_CONTINUATION_2026-07-21.md). Every hook keeps its
# primitive fallback so an unfinished batch can never break an act.
const JOB_ART_DIR := "res://assets/opera/jobs/"

func _job_art(rel: String, parent: Node3D) -> Node3D:
	var path := JOB_ART_DIR + rel
	if not ResourceLoader.exists(path):
		return null
	var ps := load(path) as PackedScene
	if ps == null:
		return null
	var inst := ps.instantiate() as Node3D
	parent.add_child(inst)
	return inst

func _job_state(root: Node3D, state: String, on: bool) -> void:
	# toggle a named State* group inside a job GLB (visibility-state pattern)
	if root == null:
		return
	var n := root.find_child(state, true, false)
	if n is Node3D:
		(n as Node3D).visible = on

func _order_prop(theme: String, i: int, col: Color, parent: Node3D) -> Node3D:
	var prop := Node3D.new()
	prop.name = "PadProp"
	prop.position = Vector3(0, 0.6, 0)
	parent.add_child(prop)
	if theme == "cake":
		# vanilla / coral / plum layer kits on their doily pedestals
		var layer := _job_art("pastry_chef/opera_pastry_chef_layer_%s.glb" % ["vanilla", "coral", "plum"][i], prop)
		if layer != null:
			return prop
	if theme == "paint":
		if _job_art("painter/opera_painter_pot_%d.glb" % i, prop) != null:
			return prop
	match theme:
		"clue":
			# paw print / feather / ribbon — chunky clue shapes a non-reader can tell apart
			if i == 0:
				_sphere(Vector3(0, 0.4, 0), 0.7, col, 0.2, prop)
				_sphere(Vector3(-0.6, 1.1, 0), 0.32, col, 0.2, prop)
				_sphere(Vector3(0, 1.25, 0), 0.32, col, 0.2, prop)
				_sphere(Vector3(0.6, 1.1, 0), 0.32, col, 0.2, prop)
			elif i == 1:
				var feather := _box(Vector3(0, 0.9, 0), Vector3(0.28, 1.8, 0.5), col, 0.2, prop)
				feather.rotation_degrees = Vector3(0, 0, 24.0)
			else:
				var loop := TorusMesh.new()
				loop.inner_radius = 0.3
				loop.outer_radius = 0.75
				_mesh(loop, Vector3(0, 0.9, 0), col, 0.2, prop)
		"paint":
			_cyl(Vector3(0, 0.5, 0), 0.9, 1.0, Color(0.8, 0.8, 0.85), 0.0, prop)
			_cyl(Vector3(0, 1.1, 0), 0.75, 0.25, col, 0.6, prop)
		_:
			_cyl(Vector3(0, 0.5, 0), 1.2, 1.0, col, 0.15, prop)
			if i == 2:
				_sphere(Vector3(0, 1.3, 0), 0.35, Color(0.9, 0.15, 0.25), 0.4, prop)
	return prop

func _order_action(choice: int) -> void:
	if state != "play" or not _is_order_kind() or order_phase != "steps" or step >= order_steps.size():
		return
	var want := order_steps[step]
	var pad: Dictionary = pads[choice]
	if choice != want:
		_wobble(pad["node"] as Node3D)
		if m.chime != null:
			m.chime.pitch_scale = 0.55
			m.chime.play()
		m.show_msg("Roshan", "Hmm, not that one yet — follow the golden sparkle!", "hint")
		progress_t = maxf(progress_t, RESCUE_DELAY)   # summon the rescue arrow now
		return
	if order_flow == "carry_paint":
		# the pot loads the brush; the stripe paints when Roshan swipes the canvas
		brush_loaded = choice
		brush_node.visible = true
		var cols := _order_colors(String(config.get("props", "cake")))
		_apply_brush_tint(cols[choice])
		m._sparkle_burst((pad["pos"] as Vector3) + Vector3(0, 2.0, 0), cols[choice])
		if m.chime != null:
			m.chime.pitch_scale = 1.05
			m.chime.play()
		m.show_msg("Roshan", "Brush loaded! Swipe it across the big canvas!", "talk")
		_update_hud()
		return
	step += 1
	progress_t = 0.0
	var prop: Node3D = pad["prop"] as Node3D
	var to: Vector3 = goal.position + Vector3(0, 1.6 + float(step) * 1.1, 0) - (pad["node"] as Node3D).position
	var tw := prop.create_tween()
	tw.tween_property(prop, "position", to, 0.55).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
	m._sparkle_burst((pad["pos"] as Vector3) + Vector3(0, 2.0, 0), Color(1.0, 0.9, 0.5))
	if m.chime != null:
		m.chime.pitch_scale = 0.9 + 0.18 * float(step)
		m.chime.play()
	var gt := goal.create_tween()
	gt.tween_property(goal, "scale", Vector3.ONE * (1.0 + 0.12 * float(step)), 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	if step >= order_steps.size():
		if String(config.get("finale", "")) == "stir":
			order_phase = "stir"
			m.show_msg("Roshan", "Every layer is in! Now swim to the big bowl and STIR, one, two, three!", "talk")
			_update_hud()
		else:
			_win()
	else:
		_update_hud()

func _apply_brush_tint(col: Color) -> void:
	var tip := brush_node.get_child(1) as MeshInstance3D
	if tip != null:
		tip.material_override = _mat(col, 0.6)

func _stir_action() -> void:
	# the chef finale: three big stirs spin the bowl faster and faster
	if state != "play" or not _is_order_kind() or order_phase != "stir":
		return
	stir_done += 1
	progress_t = 0.0
	if stir_done == 1:
		# the bowl wakes up: whisk in, batter swirling
		_job_state(chef_bowl_art, "StateIdle", false)
		_job_state(chef_bowl_art, "StateActive", true)
	var tw := goal.create_tween()
	tw.tween_property(goal, "rotation:y", goal.rotation.y + TAU * float(stir_done), 0.55).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	m._sparkle_burst(goal.position + Vector3(0, 3.0, 0), Color(1.0, 0.85, 0.6))
	if m.chime != null:
		m.chime.pitch_scale = 0.85 + 0.25 * float(stir_done)
		m.chime.play()
	if stir_done >= 3:
		# stirred to perfection: calm cream on top, oven glows open backstage
		_job_state(chef_bowl_art, "StateActive", false)
		_job_state(chef_bowl_art, "StateComplete", true)
		_job_state(chef_oven_art, "StateIdle", false)
		_job_state(chef_oven_art, "StateActive", true)
		var pop := goal.create_tween()
		pop.tween_property(goal, "scale", goal.scale * 1.25, 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		m._sparkle_burst(goal.position + Vector3(0, 4.5, 0), Color(1.0, 0.75, 0.9))
		if int(config.get("decorate", 0)) > 0:
			_open_decorate()
		else:
			_win()
	else:
		_update_hud()

func _open_decorate() -> void:
	# the chef's last beat: twinkling topping spots ring the cake — tap each
	# one to plop a cherry on. A third phase keeps the show building instead
	# of repeating the same fetch to the end.
	order_phase = "decorate"
	progress_t = 0.0
	var count := int(config.get("decorate", 3))
	var splatter := String(config.get("decorate_theme", "cherry")) == "splatter"
	var anchor: Vector3 = canvas_pos if splatter else goal.position
	for i in range(count):
		var pos := anchor + Vector3(-4.0 + float(i) * 4.0, 0.0, 4.5)
		if not splatter:
			var a := -0.8 + float(i) * (1.6 / maxf(1.0, float(count - 1)))
			pos = anchor + Vector3(sin(a) * 5.5, 0.0, cos(a) * 5.5)
		var spot := _cyl(pos + Vector3(0, 0.3, 0), 1.1, 0.4, Color(1.0, 0.6, 0.75), 0.5)
		var land: Vector3 = anchor + Vector3(-2.2 + float(i) * 2.2, 3.4 + float(i % 2) * 1.4, 0.35) if splatter \
			else anchor + Vector3(-2.2 + float(i) * 2.2, 4.6 + float(i % 2) * 0.5, 0.4)
		deco_spots.append({"index": i, "pos": pos, "done": false, "node": spot, "topping": land})
	if splatter:
		m.show_msg("Roshan", "Now the fun part! Tap each twinkling spot to SPLAT sparkle paint on your masterpiece!", "talk")
	else:
		m.show_msg("Roshan", "Now the toppings! Tap each twinkling spot to plop a cherry on the cake!", "talk")
	_update_hud()

func _deco_action(idx: int) -> void:
	if state != "play" or not _is_order_kind() or order_phase != "decorate":
		return
	var spot: Dictionary = deco_spots[idx]
	if bool(spot["done"]):
		return
	spot["done"] = true
	deco_done += 1
	progress_t = 0.0
	(spot["node"] as MeshInstance3D).visible = false
	var splatter := String(config.get("decorate_theme", "cherry")) == "splatter"
	var splat_cols: Array[Color] = [Color(1.0, 0.55, 0.3), Color(1.0, 0.85, 0.35), Color(0.6, 0.5, 0.95)]
	var topping: MeshInstance3D
	if splatter:
		# a flat paint splat pops onto the canvas in one of the pot colors
		topping = _sphere(spot["topping"] as Vector3, 0.85, splat_cols[deco_done % splat_cols.size()], 0.5)
		topping.scale = Vector3(1.0, 1.0, 0.18)
	else:
		topping = _sphere(spot["topping"] as Vector3, 0.7, Color(0.9, 0.2, 0.3), 0.4)
	var final_scale := topping.scale
	topping.scale = Vector3.ZERO
	var tw := topping.create_tween()
	tw.tween_property(topping, "scale", final_scale, 0.45).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	m._sparkle_burst((spot["pos"] as Vector3) + Vector3(0, 2.5, 0), Color(1.0, 0.7, 0.8))
	if m.chime != null:
		m.chime.pitch_scale = 1.0 + 0.2 * float(deco_done)
		m.chime.play()
	if deco_done >= deco_spots.size():
		_win()
	else:
		_update_hud()

func _tick_easel(delta: float) -> void:
	# Standing at the easel with a loaded brush hands the finger over to the
	# canvas: the stick goes quiet and a drag paints. She can always leave —
	# the band sets on coverage, and a stuck painter is finished for her.
	var near := canvas_pos.distance_to(player_pos) < 7.0
	if near and not paint_easel:
		paint_easel = true
		paint_easel_t = 0.0
		if m.touch_ui != null:
			m.touch_ui.set_drag_mode(true)
		m.show_msg("Roshan", "Now PAINT! Drag your finger across the big canvas!", "talk")
	elif not near and paint_easel:
		_leave_easel()
	if not paint_easel:
		return
	paint_easel_t += delta
	if m.touch_ui != null and m.touch_ui.drag_active:
		_paint_screen(m.touch_ui.drag_pos)
	elif Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		_paint_screen(m.get_viewport().get_mouse_position())
	_paint_flush()
	if paint_easel_t > 28.0 and brush_loaded >= 0:
		# a gentle rescue, never a fail: the brush finishes the band itself
		_fill_band_rest()
		m.show_msg("Roshan", "There it is — what a beautiful colour!", "hint")

func _leave_easel() -> void:
	paint_easel = false
	paint_easel_t = 0.0
	if m != null and m.touch_ui != null:
		m.touch_ui.set_drag_mode(false)

func _fill_band_rest() -> void:
	if paint_img == null or step >= order_steps.size():
		return
	var cols := _order_colors(String(config.get("props", "cake")))
	var col: Color = cols[order_steps[step]]
	var band := _paint_band_rows()
	for y in range(band.x, band.y):
		for x in range(PAINT_RES):
			paint_img.set_pixel(x, y, col)
			paint_hits[y * PAINT_RES + x] = 1
	paint_band_done = paint_band_need
	paint_dirty = true
	_paint_touch()

func _build_paint_canvas() -> void:
	# a blank primed canvas on its easel, and the live Image the finger paints
	paint_img = Image.create(PAINT_RES, PAINT_RES, false, Image.FORMAT_RGBA8)
	paint_img.fill(Color(0.97, 0.95, 0.9))
	paint_tex = ImageTexture.create_from_image(paint_img)
	paint_hits = PackedByteArray()
	paint_hits.resize(PAINT_RES * PAINT_RES)
	var quad := QuadMesh.new()
	quad.size = paint_size
	paint_canvas = MeshInstance3D.new()
	paint_canvas.name = "PaintCanvas"
	paint_canvas.mesh = quad
	paint_canvas.position = canvas_pos + Vector3(0, 0, 0.3)
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = paint_tex
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	paint_canvas.material_override = mat
	add_child(paint_canvas)
	# the easel frame around it
	_box(canvas_pos + Vector3(0, 0, 0.1), Vector3(paint_size.x + 0.9, paint_size.y + 0.9, 0.35), Color(0.72, 0.55, 0.4), 0.06)
	_band_target()

func _band_target() -> void:
	# each step paints one horizontal band; a band sets at 55% coverage
	paint_band_done = 0
	var rows := int(PAINT_RES / maxi(1, order_steps.size()))
	paint_band_need = int(float(rows * PAINT_RES) * 0.55)

func _paint_band_rows() -> Vector2i:
	var rows := int(PAINT_RES / maxi(1, order_steps.size()))
	# band 0 is the SKY at the top, so paint top-down as the picture builds
	var y0 := step * rows
	return Vector2i(y0, mini(PAINT_RES, y0 + rows))

func _paint_stroke_uv(u: float, v: float) -> void:
	# stamp a soft round brush and count only NEW pixels inside the live band
	if paint_img == null or brush_loaded < 0 or state != "play":
		return
	var cols := _order_colors(String(config.get("props", "cake")))
	var col: Color = cols[order_steps[step]] if step < order_steps.size() else cols[0]
	var band := _paint_band_rows()
	var cx := int(u * float(PAINT_RES))
	var cy := int(v * float(PAINT_RES))
	var gained := 0
	for dy in range(-PAINT_BRUSH, PAINT_BRUSH + 1):
		for dx in range(-PAINT_BRUSH, PAINT_BRUSH + 1):
			if dx * dx + dy * dy > PAINT_BRUSH * PAINT_BRUSH:
				continue
			var px := cx + dx
			var py := cy + dy
			if px < 0 or py < 0 or px >= PAINT_RES or py >= PAINT_RES:
				continue
			paint_img.set_pixel(px, py, col)
			var idx := py * PAINT_RES + px
			if paint_hits[idx] == 0:
				paint_hits[idx] = 1
				if py >= band.x and py < band.y:
					gained += 1
	if gained > 0:
		paint_band_done += gained
		progress_t = 0.0
		paint_dirty = true
	if paint_band_done >= paint_band_need:
		_paint_touch()

func _paint_flush() -> void:
	if paint_dirty and paint_tex != null:
		paint_tex.update(paint_img)
		paint_dirty = false

func _paint_screen(screen: Vector2) -> void:
	# project the finger onto the canvas plane and paint where it lands
	if cam == null or paint_canvas == null:
		return
	var from := cam.project_ray_origin(screen)
	var dir := cam.project_ray_normal(screen)
	var plane := Plane(Vector3(0, 0, 1), paint_canvas.position.z)
	var hit: Variant = plane.intersects_ray(from, dir)
	if hit == null:
		return
	var local: Vector3 = (hit as Vector3) - paint_canvas.position
	var u := local.x / paint_size.x + 0.5
	var v := 0.5 - local.y / paint_size.y
	if u < 0.0 or u > 1.0 or v < 0.0 or v > 1.0:
		return
	_paint_stroke_uv(u, v)

func _paint_touch() -> void:
	# a band is covered: it sets, the brush empties, the picture grows
	if state != "play" or kind != "paint" or brush_loaded < 0:
		return
	_paint_flush()
	_leave_easel()
	brush_node.visible = false
	brush_loaded = -1
	m._sparkle_burst(canvas_pos + Vector3(0, 3.0, 1.0), Color(1.0, 0.9, 0.6))
	if m.chime != null:
		m.chime.pitch_scale = 0.95 + 0.18 * float(step)
		m.chime.play()
	step += 1
	progress_t = 0.0
	if kind == "paint":
		_band_target()
	if step >= order_steps.size():
		if int(config.get("decorate", 0)) > 0:
			_open_decorate()
		else:
			_win()
	else:
		_update_hud()

# ---------------- "echo" engine (ballerina / singer) ----------------

func _build_echo() -> void:
	var count := int(config.get("pads", 4))
	var rounds: Array = config.get("rounds", [1, 2, 3])
	for v in rounds:
		echo_rounds.append(int(v))
	var palette: Array[Color] = [Color(0.36, 0.78, 1.0), Color(1.0, 0.56, 0.78), Color(0.55, 0.94, 0.62), Color(1.0, 0.83, 0.34)]
	var bells := kind == "echo" and String(config.get("props", "pads")) == "bells"
	for i in range(count):
		var x := (float(i) - float(count - 1) * 0.5) * 9.0
		var pos := CENTER + Vector3(x, 1.0, 3.0)
		var root := Node3D.new()
		root.name = "OperaPad%d" % i
		root.position = pos
		add_child(root)
		if bells:
			_cyl(Vector3(0, -0.4, 0), 2.2, 0.5, palette[i].darkened(0.45), 0.0, root)
			var bell := CylinderMesh.new()
			bell.top_radius = 0.5
			bell.bottom_radius = 1.5
			bell.height = 2.2
			_mesh(bell, Vector3(0, 1.4, 0), palette[i], 0.25, root)
		else:
			# ballerina dance tiles: color+icon paired kits from the accepted cards
			var tile := _job_art("ballerina/opera_ballerina_tile_%d.glb" % i, root)
			if tile != null:
				_job_state(tile, "StateActive", false)
			else:
				_cyl(Vector3(0, -0.3, 0), 3.0, 0.6, palette[i], 0.2, root)
		pads.append({"index": i, "node": root, "pos": pos, "lit": false})
	_echo_start_round()

func _echo_start_round() -> void:
	echo_seq = []
	var length := echo_rounds[echo_round]
	for i in range(length):
		echo_seq.append((echo_round + i * 2) % pads.size())
	echo_pos = 0
	echo_show_i = 0
	echo_show_t = 0.6
	echo_phase = "show"
	last_pad = -1
	_update_hud()

func _echo_light(i: int, strong: bool) -> void:
	var node: Node3D = pads[i]["node"] as Node3D
	# tile kit: pulse the emissive glow ring with the scale bounce
	_job_state(node, "StateActive", true)
	var off := node.create_tween()
	off.tween_interval(0.4)
	off.tween_callback(func() -> void: _job_state(node, "StateActive", false))
	var tw := node.create_tween()
	tw.tween_property(node, "scale", Vector3(1.25, 1.5, 1.25), 0.18).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(node, "scale", Vector3.ONE, 0.22)
	m._sparkle_burst((pads[i]["pos"] as Vector3) + Vector3(0, 2.5, 0), Color(1.0, 0.95, 0.6) if strong else Color(0.8, 0.9, 1.0))
	if m.chime != null:
		m.chime.pitch_scale = float(config.get("pitch", 0.7)) + 0.16 * float(i)
		m.chime.play()

func _tick_echo(delta: float) -> void:
	if echo_phase != "show":
		return
	echo_show_t -= delta
	if echo_show_t > 0.0:
		return
	if echo_show_i < echo_seq.size():
		_echo_light(echo_seq[echo_show_i], false)
		echo_show_i += 1
		echo_show_t = 0.85
	else:
		echo_phase = "repeat"
		_update_hud()

func _pad_touch(i: int) -> void:
	if state != "play" or kind != "echo" or echo_phase != "repeat":
		return
	if i == echo_seq[echo_pos]:
		echo_pos += 1
		progress_t = 0.0
		_echo_light(i, true)
		if echo_pos >= echo_seq.size():
			echo_round += 1
			if echo_round >= echo_rounds.size():
				_win()
			else:
				m.show_msg("Roshan", "Beautiful! Now a longer one — watch closely!", "talk")
				_echo_start_round()
		else:
			_update_hud()
	else:
		_wobble(pads[i]["node"] as Node3D)
		if m.chime != null:
			m.chime.pitch_scale = 0.55
			m.chime.play()
		m.show_msg("Roshan", "Almost! Watch the twinkles one more time!", "hint")
		echo_pos = 0
		echo_show_i = 0
		echo_show_t = 1.0
		echo_phase = "show"
		last_pad = i

# ---------------- "shuffle" engine (magician) ----------------

func _build_shuffle() -> void:
	for i in range(3):
		var pos := CENTER + Vector3(-10.0 + float(i) * 10.0, 1.0, 3.0)
		var root := Node3D.new()
		root.name = "OperaHat%d" % i
		root.position = pos
		add_child(root)
		# card kits: one shared hat silhouette, coral/teal/cream band colors
		if _job_art("magician/opera_magician_hat_%d.glb" % i, root) == null:
			_cyl(Vector3(0, -0.4, 0), 2.4, 0.5, Color(0.3, 0.24, 0.45), 0.0, root)
			var cone := CylinderMesh.new()
			cone.top_radius = 0.35
			cone.bottom_radius = 1.7
			cone.height = 2.6
			_mesh(cone, Vector3(0, 1.7, 0), Color(0.42, 0.26, 0.62), 0.2, root)
			_cyl(Vector3(0, 0.45, 0), 2.1, 0.3, Color(0.42, 0.26, 0.62), 0.2, root)
		hats.append({"index": i, "node": root, "pos": pos, "home": pos})
	bunny = Node3D.new()
	bunny.name = "BunnyFish"
	add_child(bunny)
	# always a pink FISH with long rabbit ears, never a rabbit body
	if _job_art("magician/opera_magician_bunnyfish.glb", bunny) == null:
		_sphere(Vector3(0, 0, 0), 0.8, Color(0.97, 0.62, 0.72), 0.2, bunny)
		_sphere(Vector3(-0.3, 1.0, 0), 0.28, Color(1.0, 0.75, 0.85), 0.3, bunny)
		_sphere(Vector3(0.3, 1.0, 0), 0.28, Color(1.0, 0.75, 0.85), 0.3, bunny)
	_shuffle_hide(0)

func _shuffle_hide(target: int) -> void:
	bunny_at = target
	bunny.position = (hats[bunny_at]["pos"] as Vector3) + Vector3(0, 1.2, 1.8)
	bunny.visible = true
	var tw := bunny.create_tween()
	tw.tween_property(bunny, "position", (hats[bunny_at]["pos"] as Vector3) + Vector3(0, 0.8, 0), 0.9).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
	tw.tween_callback(func() -> void: bunny.visible = false)
	# plan slow, watchable swaps — one MORE each round so the trick escalates
	# (round 1: two swaps, round 2: three). Hats swap PLACES but keep their
	# identity (each dict's "pos" follows its node), so the bunny stays with
	# hat `target` wherever it slides — picking is by proximity to the hat's
	# current pos, which makes the reveal honest automatically.
	swap_plan = []
	var swap_total := 2 + shuffle_round
	for k in range(swap_total):
		swap_plan.append({"a": (target + k) % 3, "b": (target + k + 1) % 3})
	shuffle_phase = "watch"
	shuffle_t = 0.0
	_update_hud()

func _tick_shuffle(delta: float) -> void:
	if shuffle_phase == "wait":
		shuffle_wait_t -= delta
		if shuffle_wait_t <= 0.0:
			_shuffle_hide(shuffle_next)
		return
	if shuffle_phase != "watch":
		return
	shuffle_t += delta
	var intro := 1.2                      # let the hop-under finish first
	var swap_len := 1.4
	if shuffle_t < intro:
		return
	if swap_plan.is_empty():
		shuffle_phase = "pick"
		m.show_msg("Roshan", "Where did the bunny-fish go? Swim to a hat and tap USE!", "talk")
		_update_hud()
		return
	# animate only the FIRST pending swap; commit it (swap the dicts' "pos"
	# fields, snap both nodes) the moment it completes so the next segment
	# always starts from real, current positions
	var f := clampf((shuffle_t - intro) / swap_len, 0.0, 1.0)
	var sw: Dictionary = swap_plan[0]
	var ha: Dictionary = hats[int(sw["a"])]
	var hb: Dictionary = hats[int(sw["b"])]
	var pa: Vector3 = ha["pos"] as Vector3
	var pb: Vector3 = hb["pos"] as Vector3
	var lift := sin(f * PI) * 1.6
	(ha["node"] as Node3D).position = pa.lerp(pb, f) + Vector3(0, lift, 0)
	(hb["node"] as Node3D).position = pb.lerp(pa, f) + Vector3(0, lift, 0)
	if f >= 1.0:
		ha["pos"] = pb
		hb["pos"] = pa
		(ha["node"] as Node3D).position = pb
		(hb["node"] as Node3D).position = pa
		swap_plan.remove_at(0)
		shuffle_t = intro   # next segment starts fresh

func _shuffle_action(choice: int) -> void:
	if state != "play" or kind != "shuffle" or shuffle_phase != "pick":
		return
	var hat: Node3D = hats[choice]["node"] as Node3D
	if choice == bunny_at:
		bunny.position = (hats[choice]["pos"] as Vector3) + Vector3(0, 0.8, 0)
		bunny.visible = true
		var tw := bunny.create_tween()
		tw.tween_property(bunny, "position", bunny.position + Vector3(0, 3.2, 0), 0.4).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		m._sparkle_burst(bunny.position + Vector3(0, 2.0, 0), Color(1.0, 0.85, 1.0))
		if m.chime != null:
			m.chime.pitch_scale = 1.3
			m.chime.play()
		shuffle_round += 1
		progress_t = 0.0
		if shuffle_round >= int(config.get("rounds", 2)):
			_win()
		else:
			m.show_msg("Roshan", "You found him! One more time — watch the hats!", "talk")
			shuffle_phase = "wait"   # timer-driven pause while the reveal plays out
			shuffle_next = (bunny_at + 1) % 3
			shuffle_wait_t = 0.9
	else:
		# mercy peek: the empty hat lifts, giggles, and the right hat wiggles
		var tw3 := hat.create_tween()
		tw3.tween_property(hat, "position", (hats[choice]["pos"] as Vector3) + Vector3(0, 2.4, 0), 0.3)
		tw3.tween_property(hat, "position", hats[choice]["pos"] as Vector3, 0.3)
		if m.chime != null:
			m.chime.pitch_scale = 0.55
			m.chime.play()
		_wobble(hats[bunny_at]["node"] as Node3D)
		m._sparkle_burst((hats[bunny_at]["pos"] as Vector3) + Vector3(0, 3.0, 0), Color(1.0, 0.9, 0.5))
		m.show_msg("Roshan", "Empty! Look — that hat is wiggling!", "hint")

# ------------- "fix" engine (astronaut engineer: the bubble pipes) -------------
# Rough demo props: a bubble tank feeds a star rocket through a pipe run with
# three missing pieces. Roshan carries each glowing piece into the slot whose
# ghost shows the same shape, then spins the valve to launch the bubbles.

func _build_fix() -> void:
	# bubble tank (left) and star rocket (right) joined by a pipe run at the back
	var tank := Node3D.new()
	tank.name = "BubbleTank"
	tank.position = CENTER + Vector3(-16.0, 1.0, -12.0)
	add_child(tank)
	if _job_art("astronaut/opera_astronaut_tank.glb", tank) == null:
		_cyl(Vector3(0, 2.2, 0), 2.2, 4.4, Color(0.55, 0.85, 0.95), 0.15, tank)
		_sphere(Vector3(0, 5.0, 0), 1.4, Color(0.75, 0.95, 1.0), 0.3, tank)
	var rocket := Node3D.new()
	rocket.name = "StarRocket"
	rocket.position = CENTER + Vector3(14.0, 1.0, -12.0)
	add_child(rocket)
	if _job_art("astronaut/opera_astronaut_rocket.glb", rocket) == null:
		_cyl(Vector3(0, 3.0, 0), 1.8, 6.0, Color(0.92, 0.9, 0.98), 0.1, rocket)
		var nose := CylinderMesh.new()
		nose.top_radius = 0.1
		nose.bottom_radius = 1.8
		nose.height = 2.6
		_mesh(nose, Vector3(0, 7.3, 0), Color(1.0, 0.55, 0.5), 0.2, rocket)
	# the live window sphere stays in both cases: the kit frames it with a
	# brass port ring at the same spot, and the launch glow toggles it
	rocket_window = _sphere(Vector3(0, 3.6, 1.5), 0.8, Color(0.2, 0.22, 0.4), 0.05, rocket)
	rocket_window.material_override = rocket_window.material_override.duplicate() as StandardMaterial3D
	# fixed pipe stubs along the run, with three gaps between them
	for px in [-12.0, -4.0, 4.0, 12.0]:
		var stub := _cyl(CENTER + Vector3(px, 3.0, -12.0), 0.55, 2.6, Color(0.75, 0.78, 0.88), 0.1)
		stub.rotation_degrees = Vector3(0, 0, 90.0)
	# the three gaps: each slot ghost shows the SHAPE it needs (picture clue)
	var needs: Array[int] = [2, 0, 1]
	for i in range(3):
		var sx := -8.0 + float(i) * 8.0
		var slot_root := Node3D.new()
		slot_root.name = "PipeSlot%d" % i
		slot_root.position = CENTER + Vector3(sx, 3.0, -12.0)
		add_child(slot_root)
		var ghost := _box(Vector3.ZERO, Vector3(2.6, 2.0, 1.2), Color(0.95, 0.95, 0.6, 0.3), 0.3, slot_root)
		var gm := ghost.material_override as StandardMaterial3D
		gm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		var hint := _make_pipe_shape(needs[i], Color(1.0, 0.92, 0.5))
		hint.scale = Vector3.ONE * 0.45
		hint.position = Vector3(0, 3.0, 0)
		slot_root.add_child(hint)
		slots.append({"index": i, "node": slot_root, "ghost": ghost, "hint": hint,
			"pos": CENTER + Vector3(sx, 1.0, -12.0), "need": needs[i], "filled": false})
	# the three loose pieces wait on pads at the front of the stage
	var piece_cols: Array[Color] = [Color(0.45, 0.85, 1.0), Color(1.0, 0.62, 0.78), Color(0.6, 0.95, 0.65)]
	for i in range(3):
		var px2 := -12.0 + float(i) * 12.0
		var home := CENTER + Vector3(px2, 1.0, 5.0)
		var pad_root := Node3D.new()
		pad_root.name = "PiecePad%d" % i
		pad_root.position = home
		add_child(pad_root)
		_cyl(Vector3(0, -0.4, 0), 2.4, 0.5, piece_cols[i].darkened(0.45), 0.0, pad_root)
		var piece := _make_pipe_shape(i, piece_cols[i])
		piece.position = home + Vector3(0, 1.4, 0)
		add_child(piece)
		pieces.append({"index": i, "node": piece, "home": piece.position, "pos": home, "placed": false})
	# the valve appears on the tank once every pipe is in place
	valve = Node3D.new()
	valve.name = "BubbleValve"
	valve.position = CENTER + Vector3(-16.0, 4.6, -10.4)
	add_child(valve)
	var valve_kit := _job_art("astronaut/opera_astronaut_valve.glb", valve)
	if valve_kit != null:
		valve_kit.position = Vector3(0, -2.0, 0)   # pedestal reaches the deck
	else:
		var wheel := TorusMesh.new()
		wheel.inner_radius = 0.5
		wheel.outer_radius = 1.0
		var wheel_mesh := _mesh(wheel, Vector3.ZERO, Color(1.0, 0.7, 0.3), 0.15, valve)
		wheel_mesh.rotation_degrees = Vector3(90, 0, 0)
		_box(Vector3.ZERO, Vector3(1.8, 0.3, 0.3), Color(1.0, 0.7, 0.3), 0.15, valve)

func _make_pipe_shape(shape: int, col: Color) -> Node3D:
	# 0 = straight pipe, 1 = elbow pipe, 2 = ring coupler — chunky and distinct
	var root := Node3D.new()
	root.name = "PipePiece%d" % shape
	match shape:
		1:
			var a := _cyl(Vector3(-0.5, 0, 0), 0.55, 1.6, col, 0.25, root)
			a.rotation_degrees = Vector3(0, 0, 90.0)
			_cyl(Vector3(0.3, 0.7, 0), 0.55, 1.6, col, 0.25, root)
		2:
			var ring := TorusMesh.new()
			ring.inner_radius = 0.45
			ring.outer_radius = 1.0
			_mesh(ring, Vector3.ZERO, col, 0.25, root)
		_:
			var straight := _cyl(Vector3.ZERO, 0.55, 2.4, col, 0.25, root)
			straight.rotation_degrees = Vector3(0, 0, 90.0)
	return root

func _nearest_piece() -> int:
	var best := -1
	var best_d := PAD_REACH
	for piece in pieces:
		if bool(piece["placed"]):
			continue
		var d: float = (piece["pos"] as Vector3).distance_to(player_pos)
		if d < best_d:
			best_d = d
			best = int(piece["index"])
	return best

func _pick_piece(i: int) -> void:
	if state != "play" or kind != "fix" or fix_phase != "pipes" or carried >= 0:
		return
	if bool(pieces[i]["placed"]):
		return
	carried = i
	progress_t = 0.0
	m._sparkle_burst(((pieces[i]["node"] as Node3D)).position + Vector3(0, 1.0, 0), Color(0.8, 0.95, 1.0))
	if m.chime != null:
		m.chime.pitch_scale = 1.05
		m.chime.play()
	m.show_msg("Roshan", "Got it! Now carry it to the glowing pipe gap!", "talk")
	_update_hud()

func _place_piece() -> void:
	if state != "play" or kind != "fix" or fix_phase != "pipes" or carried < 0:
		return
	var slot: Dictionary = slots[fix_step]
	var piece: Dictionary = pieces[carried]
	var node: Node3D = piece["node"] as Node3D
	if carried == int(slot["need"]):
		piece["placed"] = true
		slot["filled"] = true
		node.position = (slot["node"] as Node3D).position
		(slot["ghost"] as Node3D).visible = false
		(slot["hint"] as Node3D).visible = false
		carried = -1
		fix_step += 1
		progress_t = 0.0
		m._sparkle_burst(node.position + Vector3(0, 1.5, 0), Color(1.0, 0.9, 0.5))
		if m.chime != null:
			m.chime.pitch_scale = 0.95 + 0.18 * float(fix_step)
			m.chime.play()
		if fix_step >= slots.size():
			fix_phase = "valve"
			m.show_msg("Roshan", "Every pipe is fixed! Now spin the big valve to send the bubbles!", "talk")
		_update_hud()
	else:
		# gentle bounce home: wrong shape never fails, the ghost just wiggles
		var tw := node.create_tween()
		tw.tween_property(node, "position", piece["home"] as Vector3, 0.4).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		carried = -1
		_wobble(slot["node"] as Node3D)
		if m.chime != null:
			m.chime.pitch_scale = 0.55
			m.chime.play()
		m.show_msg("Roshan", "That shape doesn't fit this gap — look at the little picture above it!", "hint")

func _turn_valve() -> void:
	# three big spins build the bubble pressure, then the rocket lights up
	if state != "play" or kind != "fix" or fix_phase != "valve":
		return
	valve_spins += 1
	progress_t = 0.0
	var tw := valve.create_tween()
	tw.tween_property(valve, "rotation:z", TAU * float(valve_spins), 0.7).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
	for i in range(1 + valve_spins):
		m._sparkle_burst(CENTER + Vector3(-14.0 + float(i) * 7.0, 4.0, -12.0), Color(0.7, 0.95, 1.0))
	if m.chime != null:
		m.chime.pitch_scale = 0.9 + 0.2 * float(valve_spins)
		m.chime.play()
	if valve_spins < 3:
		m.show_msg("Roshan", "The bubbles are building — spin it again!", "talk")
		_update_hud()
		return
	if rocket_window != null:
		var wm := rocket_window.material_override as StandardMaterial3D
		wm.albedo_color = Color(1.0, 0.95, 0.6)
		wm.emission = Color(1.0, 0.95, 0.6)
		wm.emission_enabled = true
		wm.emission_energy_multiplier = 1.5
	_win()

func _tick_fix(_delta: float) -> void:
	if carried >= 0:
		var node: Node3D = pieces[carried]["node"] as Node3D
		node.position = player_pos + Vector3(0, 3.4, 0)
		node.rotation.y = elapsed * 1.5
	if fix_phase == "valve" and valve != null:
		valve.scale = Vector3.ONE * (1.0 + 0.08 * sin(elapsed * 5.0))

# ------------- "press" engine (candy maker: the face-stamp machine) -------------
# Rough demo props: a candy press with a sliding star gauge. Tap PRESS when
# the star crosses the glowing middle and the press stamps a smiley face on
# the candy. Misses just squish a silly wobble — the candy always survives.

func _build_press() -> void:
	candies_goal = int(config.get("candies", 4))
	var machine := Node3D.new()
	machine.name = "CandyPress"
	machine.position = CENTER + Vector3(0, 1.0, -10.0)
	add_child(machine)
	# card kit: the coral gazebo press with its descending PressBlock stamp
	var press_kit := _job_art("candymaker/opera_candymaker_press.glb", machine)
	if press_kit != null:
		press_block = press_kit.find_child("PressBlock", true, false) as Node3D
	if press_block == null:
		_box(Vector3(-4.2, 3.5, 0), Vector3(1.2, 7.0, 1.6), Color(0.85, 0.55, 0.75), 0.1, machine)
		_box(Vector3(4.2, 3.5, 0), Vector3(1.2, 7.0, 1.6), Color(0.85, 0.55, 0.75), 0.1, machine)
		_box(Vector3(0, 7.2, 0), Vector3(9.6, 1.2, 1.6), Color(0.85, 0.55, 0.75), 0.1, machine)
		_cyl(Vector3(0, 0.5, 0), 2.0, 1.0, Color(0.95, 0.9, 0.98), 0.1, machine)
		press_block = _box(Vector3(0, 5.4, 0), Vector3(2.6, 1.6, 2.0), Color(1.0, 0.75, 0.85), 0.2, machine)
	# the timing gauge floats in front: track, sweet-spot glow, sliding star
	var track_y := 8.9
	_box(CENTER + Vector3(0, track_y, -8.5), Vector3(11.0, 0.5, 0.5), Color(0.4, 0.34, 0.55), 0.1)
	press_zone_box = _box(CENTER + Vector3(0, track_y, -8.4), Vector3(11.0 * press_zone, 1.0, 0.7), Color(0.55, 0.95, 0.6), 0.7)
	press_slider = _sphere(CENTER + Vector3(0, track_y, -8.2), 0.65, Color(1.0, 0.9, 0.4), 1.2)
	# a little shelf where the finished smiley candies line up
	_box(CENTER + Vector3(11.0, 1.2, -6.0), Vector3(6.0, 0.5, 3.0), Color(0.6, 0.45, 0.65), 0.1)
	_candy_next()

func _candy_next() -> void:
	var candy_cols: Array[Color] = [Color(1.0, 0.62, 0.7), Color(0.62, 0.85, 1.0), Color(1.0, 0.85, 0.45)]
	candy_node = Node3D.new()
	candy_node.name = "Candy%d" % candies_done
	candy_node.position = CENTER + Vector3(0, 2.4, -10.0)
	add_child(candy_node)
	# seven card-kit candies with different outer silhouettes, in batch order
	if _job_art("candymaker/opera_candymaker_candy_%d.glb" % (candies_done % 7), candy_node) == null:
		_sphere(Vector3.ZERO, 1.3, candy_cols[candies_done % candy_cols.size()], 0.25, candy_node)
	candy_node.scale = Vector3.ZERO
	var tw := candy_node.create_tween()
	tw.tween_property(candy_node, "scale", Vector3.ONE, 0.35).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

func _press_action() -> void:
	if state != "play" or kind != "press" or press_busy > 0.0 or candy_node == null:
		return
	press_busy = 0.9
	var stamp_down := press_block.position + Vector3(0, -2.4, 0)
	var stamp_home := press_block.position
	var tw := press_block.create_tween()
	tw.tween_property(press_block, "position", stamp_down, 0.16).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw.tween_property(press_block, "position", stamp_home, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	if absf(press_x) <= press_zone:
		# every candy gets its own face: dot eyes, then starry eyes, then a
		# blushing heart-mouth — collecting the trio is half the fun
		match candies_done:
			1:
				_sphere(Vector3(-0.4, 0.35, 1.05), 0.24, Color(1.0, 0.85, 0.35), 0.8, candy_node)
				_sphere(Vector3(0.4, 0.35, 1.05), 0.24, Color(1.0, 0.85, 0.35), 0.8, candy_node)
				_box(Vector3(0, -0.25, 1.15), Vector3(0.7, 0.16, 0.16), Color(0.15, 0.12, 0.25), 0.0, candy_node)
			2:
				_sphere(Vector3(-0.4, 0.35, 1.05), 0.18, Color(0.15, 0.12, 0.25), 0.0, candy_node)
				_sphere(Vector3(0.4, 0.35, 1.05), 0.18, Color(0.15, 0.12, 0.25), 0.0, candy_node)
				_sphere(Vector3(-0.7, 0.0, 1.0), 0.16, Color(1.0, 0.55, 0.6), 0.3, candy_node)
				_sphere(Vector3(0.7, 0.0, 1.0), 0.16, Color(1.0, 0.55, 0.6), 0.3, candy_node)
				_sphere(Vector3(0, -0.3, 1.15), 0.22, Color(0.95, 0.35, 0.5), 0.4, candy_node)
			_:
				_sphere(Vector3(-0.4, 0.35, 1.05), 0.18, Color(0.15, 0.12, 0.25), 0.0, candy_node)
				_sphere(Vector3(0.4, 0.35, 1.05), 0.18, Color(0.15, 0.12, 0.25), 0.0, candy_node)
				_box(Vector3(0, -0.25, 1.15), Vector3(0.7, 0.16, 0.16), Color(0.15, 0.12, 0.25), 0.0, candy_node)
		shelf_candies.append(candy_node)
		m._sparkle_burst(candy_node.position + Vector3(0, 2.0, 0), Color(1.0, 0.85, 1.0))
		if m.chime != null:
			m.chime.pitch_scale = 1.0 + 0.15 * float(candies_done)
			m.chime.play()
		candies_done += 1
		progress_t = 0.0
		var done := candy_node
		var shelf := CENTER + Vector3(8.0 + float(candies_done) * 2.4, 1.9, -6.0)
		var tw2 := done.create_tween()
		tw2.tween_interval(0.35)
		tw2.tween_property(done, "position", shelf, 0.55).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
		candy_node = null
		# the sweet spot narrows a touch each candy, but stays generous
		press_zone = maxf(0.2, 0.34 - 0.045 * float(candies_done))
		if press_zone_box != null:
			press_zone_box.scale.x = press_zone / 0.34
		if candies_done >= candies_goal:
			_win()
		else:
			press_next_t = 0.8   # timer-driven so headless playtests can pump time
			_update_hud()
	else:
		# a miss just squishes a giggle-wobble — the candy is always fine
		var squish := candy_node.create_tween()
		squish.tween_property(candy_node, "scale", Vector3(1.25, 0.7, 1.25), 0.15)
		squish.tween_property(candy_node, "scale", Vector3.ONE, 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		if m.chime != null:
			m.chime.pitch_scale = 0.55
			m.chime.play()
		m.show_msg("Roshan", "Squish! Wait until the star slides into the green middle, then PRESS!", "hint")

func _tick_press(delta: float) -> void:
	press_busy = maxf(0.0, press_busy - delta)
	if press_next_t > 0.0:
		press_next_t -= delta
		if press_next_t <= 0.0:
			_candy_next()
	press_x = sin(elapsed * 1.6)
	if press_slider != null:
		press_slider.position.x = CENTER.x + press_x * 5.5

# ------------- "doctor" engine (one-touch surgery on a plush patient) -------------
# Rough demo props: a poorly plush starfish on the operating table. Four
# one-touch steps in a guided order: thermometer, two boo-boos that turn into
# hearts, then the bandage. Taps out of order just wobble and re-point.

func _build_doctor() -> void:
	_box(CENTER + Vector3(0, 1.2, -2.0), Vector3(7.0, 1.6, 4.4), Color(0.9, 0.93, 0.98), 0.05)
	_box(CENTER + Vector3(0, 0.4, -2.0), Vector3(5.6, 0.8, 3.4), Color(0.75, 0.8, 0.9), 0.0)
	patient = Node3D.new()
	patient.name = "PlushPatient"
	patient.position = CENTER + Vector3(0, 2.6, -2.0)
	add_child(patient)
	# species lock: the patient is always the coral five-armed starfish plush
	doctor_patient_art = _job_art("doctor/opera_doctor_patient.glb", patient)
	if doctor_patient_art != null:
		_job_state(doctor_patient_art, "StateComplete", false)
	else:
		_sphere(Vector3.ZERO, 1.6, Color(0.95, 0.55, 0.45), 0.1, patient)
		for i in range(5):
			var a := float(i) * TAU / 5.0 + 0.3
			_sphere(Vector3(cos(a) * 1.7, 0.2, sin(a) * 1.7), 0.62, Color(0.98, 0.68, 0.58), 0.1, patient)
		_sphere(Vector3(-0.45, 0.8, 1.15), 0.2, Color(0.12, 0.1, 0.25), 0.0, patient)
		_sphere(Vector3(0.45, 0.8, 1.15), 0.2, Color(0.12, 0.1, 0.25), 0.0, patient)
	# step 0: the stethoscope — listen to the plushy's little heart first
	var scope := Node3D.new()
	scope.name = "Stethoscope"
	scope.position = CENTER + Vector3(-9.0, 1.0, 4.0)
	add_child(scope)
	if _job_art("doctor/opera_doctor_scope.glb", scope) == null:
		_cyl(Vector3(0, 0.2, 0), 1.2, 0.4, Color(0.8, 0.85, 0.92), 0.05, scope)
		var ring := TorusMesh.new()
		ring.inner_radius = 0.55
		ring.outer_radius = 0.75
		_mesh(ring, Vector3(0, 1.5, 0), Color(0.35, 0.4, 0.55), 0.1, scope)
		_cyl(Vector3(0, 0.7, 0.4), 0.3, 0.16, Color(0.85, 0.9, 0.98), 0.4, scope)
	doc_targets.append({"index": 0, "node": scope, "pos": scope.position, "kind": "scope"})
	# step 1: the thermometer on its little stand
	var thermo := Node3D.new()
	thermo.name = "Thermometer"
	thermo.position = CENTER + Vector3(9.0, 1.0, 4.0)
	add_child(thermo)
	if _job_art("doctor/opera_doctor_thermo.glb", thermo) == null:
		_cyl(Vector3(0, 0.2, 0), 1.2, 0.4, Color(0.8, 0.85, 0.92), 0.05, thermo)
		var stem := _box(Vector3(0, 1.4, 0), Vector3(0.3, 2.2, 0.3), Color(0.95, 0.97, 1.0), 0.3, thermo)
		stem.rotation_degrees = Vector3(0, 0, 18.0)
		_sphere(Vector3(-0.35, 0.55, 0), 0.34, Color(1.0, 0.35, 0.3), 0.5, thermo)
	doc_targets.append({"index": 1, "node": thermo, "pos": thermo.position, "kind": "thermo"})
	# steps 2-6: glowing boo-boos on the plush that become hearts when tended.
	# The reach points alternate sides so each kiss is a little swim, not a
	# stand-still tap chain.
	var boo_spots: Array[Vector3] = [Vector3(-1.1, 0.9, 0.8), Vector3(1.2, 0.5, 0.9),
		Vector3(-0.5, 0.3, 1.25), Vector3(0.9, 0.85, 1.1), Vector3(0.1, 0.3, 1.35)]
	var boo_reaches: Array[Vector3] = [Vector3(-2.4, 1.0, 1.4), Vector3(2.4, 1.0, 1.4),
		Vector3(-1.5, 1.0, 2.2), Vector3(1.5, 1.0, 2.2), Vector3(0.0, 1.0, 2.4)]
	for b in range(boo_spots.size()):
		var boo := _sphere(boo_spots[b], 0.4, Color(1.0, 0.3, 0.25), 0.9, patient)
		var heart := _sphere(boo_spots[b] + Vector3(0, 0.15, 0.1), 0.42, Color(1.0, 0.55, 0.75), 0.7, patient)
		heart.visible = false
		doc_targets.append({"index": 2 + b, "node": boo, "heart": heart, "pos": CENTER + boo_reaches[b], "kind": "boo"})
	# step 7: the bandage roll, which wraps a soft white band around the plush
	var roll := Node3D.new()
	roll.name = "BandageRoll"
	roll.position = CENTER + Vector3(0.0, 1.0, 6.5)
	add_child(roll)
	if _job_art("doctor/opera_doctor_bandage.glb", roll) == null:
		var loop := TorusMesh.new()
		loop.inner_radius = 0.4
		loop.outer_radius = 0.9
		_mesh(loop, Vector3(0, 0.9, 0), Color(0.97, 0.97, 0.94), 0.15, roll)
	var band := _box(Vector3(0, 0.1, 0), Vector3(3.6, 0.5, 3.6), Color(0.98, 0.98, 0.95), 0.2, patient)
	band.visible = false
	doc_targets.append({"index": 7, "node": roll, "band": band, "pos": roll.position, "kind": "bandage"})

func _doctor_action(choice: int) -> void:
	if state != "play" or kind != "doctor" or doc_step >= doc_targets.size():
		return
	if doc_wait > 0.0:
		return   # the plushy is still giggling from the last step — taps rest kindly
	var target: Dictionary = doc_targets[choice]
	if choice != doc_step:
		_wobble(target["node"] as Node3D)
		if m.chime != null:
			m.chime.pitch_scale = 0.55
			m.chime.play()
		m.show_msg("Roshan", "Not that one yet, doctor — follow the golden sparkle!", "hint")
		return
	progress_t = 0.0
	var node: Node3D = target["node"] as Node3D
	match String(target["kind"]):
		"scope":
			# two soft heart-thumps while the plushy's chest pulses
			var beat := create_tween()
			beat.tween_callback(_heart_thump)
			beat.tween_interval(0.4)
			beat.tween_callback(_heart_thump)
			var pulse := patient.create_tween()
			pulse.tween_property(patient, "scale", Vector3.ONE * 1.08, 0.35).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			pulse.tween_property(patient, "scale", Vector3.ONE, 0.35)
			pulse.tween_property(patient, "scale", Vector3.ONE * 1.08, 0.35)
			pulse.tween_property(patient, "scale", Vector3.ONE, 0.35)
			m.show_msg("Roshan", "Bum-bum... bum-bum... a strong little heart! Now the thermometer!", "talk")
		"thermo":
			var tw := node.create_tween()
			tw.tween_property(node, "position", patient.position + Vector3(0, 2.4, 1.2), 0.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
			tw.tween_interval(0.4)
			tw.tween_property(node, "position", target["pos"] as Vector3, 0.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
			m.show_msg("Roshan", "Just a tiny fever — the boo-boos need some love!", "talk")
		"boo":
			node.visible = false
			var heart := target["heart"] as Node3D
			heart.visible = true
			heart.scale = Vector3.ZERO
			var tw2 := heart.create_tween()
			tw2.tween_property(heart, "scale", Vector3.ONE, 0.4).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		"bandage":
			var tw3 := node.create_tween()
			tw3.tween_property(node, "position", patient.position + Vector3(0, 1.0, 0), 0.5).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
			tw3.tween_callback(func() -> void: node.visible = false)
			var band := target["band"] as Node3D
			band.visible = true
			band.scale = Vector3.ZERO
			var tw4 := band.create_tween()
			tw4.tween_property(band, "scale", Vector3.ONE, 0.45).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	m._sparkle_burst((target["pos"] as Vector3) + Vector3(0, 2.5, 0), Color(0.7, 0.95, 1.0))
	if m.chime != null:
		m.chime.pitch_scale = 0.95 + 0.15 * float(doc_step)
		m.chime.play()
	doc_step += 1
	if doc_step >= doc_targets.size():
		# recovered pose: worried face off, happy face + blush on
		_job_state(doctor_patient_art, "StateIdle", false)
		_job_state(doctor_patient_art, "StateComplete", true)
		# magic-kiss finale: a fountain of hearts, then the plush pops up better
		for h in range(3):
			m._sparkle_burst(patient.position + Vector3(-1.5 + float(h) * 1.5, 2.5 + float(h) * 0.8, 1.0), Color(1.0, 0.6, 0.8))
		var hop := patient.create_tween()
		hop.tween_property(patient, "position:y", patient.position.y + 1.6, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		hop.tween_property(patient, "position:y", patient.position.y, 0.35).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
		_win()
	else:
		# let each little animation finish before the next tap counts — the
		# checkup is a story, not a tap race
		match String(target["kind"]):
			"scope":
				doc_wait = 3.0
			"thermo":
				doc_wait = 2.4
			_:
				doc_wait = 2.0
		_update_hud()

func _heart_thump() -> void:
	if m.chime != null:
		m.chime.pitch_scale = 0.45
		m.chime.play()
	m._sparkle_burst(patient.position + Vector3(0, 1.5, 1.2), Color(1.0, 0.55, 0.7))

func _nearest_doc_target() -> int:
	var best := -1
	var best_d := PAD_REACH
	for target in doc_targets:
		var d: float = (target["pos"] as Vector3).distance_to(player_pos)
		if d < best_d:
			best_d = d
			best = int(target["index"])
	return best

# ------------- "scroll" engine (farmer: the 2D piggy-feeding meadow) -------------
# A one-touch side-scroller played on a flat overlay: the meadow slides past,
# hungry piggies drift toward Roshan, and a tap tosses a veggie to the nearest
# one. Unfed piggies loop back around, so every piggy gets fed eventually.
# ALL piggy/meadow art here is a rough placeholder (circle-panels) — the
# owner's authored farm art replaces these panels in a later pass.

func _panel_circle(parent: Control, pos: Vector2, size: float, col: Color) -> Panel:
	var panel := Panel.new()
	var style := StyleBoxFlat.new()
	style.bg_color = col
	style.set_corner_radius_all(int(size * 0.5))
	panel.add_theme_stylebox_override("panel", style)
	panel.position = pos
	panel.size = Vector2(size, size)
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(panel)
	return panel

func _build_farm() -> void:
	farm_layer = CanvasLayer.new()
	farm_layer.layer = 13   # below the act banner (14) so the objective stays visible
	add_child(farm_layer)
	var root := Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	farm_layer.add_child(root)
	var sky := ColorRect.new()
	sky.color = Color(0.62, 0.85, 0.98)
	sky.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	sky.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(sky)
	_panel_circle(root, Vector2(1050, 40), 130, Color(1.0, 0.92, 0.55))
	for h in range(3):
		_panel_circle(root, Vector2(-100.0 + float(h) * 460.0, 380.0), 420, Color(0.6, 0.85, 0.55))
	var ground := ColorRect.new()
	ground.color = Color(0.52, 0.78, 0.45)
	ground.position = Vector2(0, 520)
	ground.size = Vector2(1280, 200)
	ground.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(ground)
	var roshan := TextureRect.new()
	roshan.texture = load("res://assets/characters/roshan_sprite.png") as Texture2D
	roshan.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	roshan.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	roshan.position = Vector2(190, 330)
	roshan.size = Vector2(150, 190)
	roshan.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(roshan)
	farm_roshan = roshan
	for i in range(int(config.get("piggies", 7))):
		var pig := Control.new()
		pig.position = Vector2(900.0 + float(i) * 560.0, 420.0)
		pig.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(pig)
		# placeholder circle-piggy (art pending): body, ears, snout
		_panel_circle(pig, Vector2(0, 0), 96, Color(1.0, 0.72, 0.78))
		_panel_circle(pig, Vector2(8, -16), 28, Color(0.98, 0.62, 0.7))
		_panel_circle(pig, Vector2(60, -16), 28, Color(0.98, 0.62, 0.7))
		_panel_circle(pig, Vector2(30, 34), 38, Color(0.98, 0.6, 0.68))
		var bubble := _panel_circle(pig, Vector2(20, -74), 56, Color(1.0, 1.0, 1.0, 0.92))
		var want := Label.new()
		# every piggy dreams of a different snack — small variety, big charm
		want.text = ["🥕", "🍎", "🌽", "🍓", "🎃"][i % 5]
		want.add_theme_font_size_override("font_size", 34)
		want.position = Vector2(8, 4)
		want.mouse_filter = Control.MOUSE_FILTER_IGNORE
		bubble.add_child(want)
		piggies.append({"index": i, "node": pig, "bubble": bubble, "want": want,
			"x": 900.0 + float(i) * 560.0, "sx": 900.0 + float(i) * 560.0, "fed": false})

func _tick_farm(delta: float) -> void:
	farm_t += delta
	farm_toss_cool = maxf(0.0, farm_toss_cool - delta)
	if farm_roshan != null:
		farm_roshan.position.y = 330.0 + sin(elapsed * 3.2) * 14.0
	var wrap := 600.0 + 560.0 * float(piggies.size())
	for pig in piggies:
		var sx: float = float(pig["x"]) - farm_t * FARM_SPEED
		while sx < -160.0:
			# unfed piggies trot back around; fed ones park happily off-screen
			if bool(pig["fed"]):
				break
			pig["x"] = float(pig["x"]) + wrap
			sx = float(pig["x"]) - farm_t * FARM_SPEED
		pig["sx"] = sx
		var node := pig["node"] as Control
		node.position.x = sx
		if not bool(pig["fed"]):
			(pig["bubble"] as Control).scale = Vector2.ONE * (1.0 + 0.12 * sin(elapsed * 5.0 + float(pig["index"])))
			node.rotation = sin(elapsed * 5.5 + float(pig["index"]) * 1.7) * 0.06   # trotting wiggle

func _toss_action() -> void:
	if state != "play" or kind != "scroll" or farm_toss_cool > 0.0:
		return
	farm_toss_cool = 0.5
	var best := -1
	var best_d := 170.0
	for pig in piggies:
		if bool(pig["fed"]):
			continue
		var d: float = absf(float(pig["sx"]) - 250.0)
		if d < best_d:
			best_d = d
			best = int(pig["index"])
	if best >= 0:
		var pig2: Dictionary = piggies[best]
		pig2["fed"] = true
		(pig2["want"] as Label).text = "❤"
		var node := pig2["node"] as Control
		node.rotation = 0.0
		var tw := node.create_tween()
		tw.tween_property(node, "position:y", 390.0, 0.2).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(node, "position:y", 420.0, 0.25).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
		if farm_roshan != null:
			# Roshan does a happy throw-squash so every toss FEELS thrown
			var squash := farm_roshan.create_tween()
			squash.tween_property(farm_roshan, "scale", Vector2(1.15, 0.85), 0.12)
			squash.tween_property(farm_roshan, "scale", Vector2.ONE, 0.2).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		if m.chime != null:
			m.chime.pitch_scale = 1.0 + 0.12 * float(farm_fed)
			m.chime.play()
		farm_fed += 1
		progress_t = 0.0
		if farm_fed >= piggies.size():
			_win()
		else:
			_update_hud()
	else:
		# a toss with nobody close is just a bouncing veggie — never a fail
		if m.chime != null:
			m.chime.pitch_scale = 0.6
			m.chime.play()
		if farm_roshan != null:
			var tw2 := farm_roshan.create_tween()
			tw2.tween_property(farm_roshan, "rotation", 0.12, 0.1)
			tw2.tween_property(farm_roshan, "rotation", 0.0, 0.15)

# ------------- "race" engine (racecar driver: KartGame exhibition) -------------
# Real reuse of the kart engine via its documented configure()/start() hooks:
# a one-lap Opera Grand Prix. Quitting with ✕ returns to the stage where the
# checkered flag restarts the race — finishing in any place wins the act.

func _build_race() -> void:
	race_flag = Node3D.new()
	race_flag.name = "RaceFlag"
	race_flag.position = CENTER + Vector3(0, 1.0, 2.0)
	add_child(race_flag)
	_box(Vector3(0, 2.6, 0), Vector3(0.25, 5.2, 0.25), Color(0.75, 0.78, 0.88), 0.1, race_flag)
	_box(Vector3(1.1, 4.4, 0), Vector3(2.0, 1.5, 0.12), Color(0.95, 0.95, 0.95), 0.25, race_flag)
	_box(Vector3(0.6, 4.4, 0.02), Vector3(0.9, 0.72, 0.12), Color(0.12, 0.12, 0.18), 0.0, race_flag)
	_box(Vector3(1.55, 3.7, 0.02), Vector3(0.9, 0.72, 0.12), Color(0.12, 0.12, 0.18), 0.0, race_flag)
	_launch_race()

func _launch_race() -> void:
	if state != "play" or kind != "race" or kart != null:
		return
	race_prev_track = m.cur_track
	m._play_music("race")
	var kart_script: GDScript = load("res://scripts/kart.gd") as GDScript
	kart = kart_script.new() as Node
	add_child(kart)
	kart.call("configure", {"name": "Opera Grand Prix", "laps": 1})
	kart.call("start", m, Callable(self, "_race_finished"))

func _race_finished(place: int) -> void:
	if kart != null and is_instance_valid(kart):
		kart.queue_free()
	kart = null
	if state != "play":
		return
	if cam != null:
		cam.make_current()
	m._play_music(race_prev_track if race_prev_track != "" else "level2")
	if place > 0:
		_win()
	else:
		m.show_msg("Roshan", "The Grand Prix is waiting! Tap the checkered flag when you're ready to race!", "talk")
		_update_hud()

# ------------- "dance" engine (pop star: the DanceEngine guest spot) -------------
# Reuses the beat-synced rhythm playground as-is: tapping the sparkling
# microphone opens the dance stage in guest mode, and the first round with
# any happy hits takes the act's bow. Closing early just returns to the mic.

func _build_dance() -> void:
	mic = Node3D.new()
	mic.name = "StarMicrophone"
	mic.position = CENTER + Vector3(0, 1.0, 2.0)
	add_child(mic)
	var mic_kit := _job_art("popstar/opera_popstar_microphone.glb", mic)
	if mic_kit != null:
		_job_state(mic_kit, "StateActive", false)
	else:
		_cyl(Vector3(0, 0.2, 0), 1.3, 0.4, Color(0.4, 0.36, 0.6), 0.1, mic)
		_box(Vector3(0, 2.0, 0), Vector3(0.22, 3.6, 0.22), Color(0.8, 0.82, 0.92), 0.15, mic)
		_sphere(Vector3(0, 4.2, 0), 0.75, Color(1.0, 0.85, 0.4), 0.7, mic)
	_open_dance()

func _open_dance() -> void:
	if state != "play" or kind != "dance":
		return
	if dance == null:
		var dance_script: GDScript = load("res://scripts/games/dance_engine.gd") as GDScript
		dance = dance_script.new(m) as CanvasLayer
		dance.set("guest_mode", true)
		add_child(dance)
		dance.connect("closed", _dance_closed)
	dance.call("open_demo")

func _dance_closed() -> void:
	if state != "play":
		return
	if dance != null and int(dance.get("happy_hits")) > 0:
		_win()
	else:
		m.show_msg("Roshan", "The stage is yours whenever you're ready — tap the sparkling microphone!", "talk")

# ---------------- "boss" engine (curtain dragon / shadow phantom) ----------------

func _build_boss() -> void:
	var finale := bool(config.get("finale", false))
	var dual := bool(config.get("dual", false)) or finale
	var root := Node3D.new()
	root.name = "OperaBoss"
	root.position = CENTER + Vector3(0, 1.0, -14.0)
	add_child(root)
	if finale:
		# THE THEATRE STAGE is where the grand finale happens (owner
		# 2026-07-21): the authored proscenium, swagged curtains and footlit
		# apron dress the boards for the Maestro's showdown
		_act_prop("opera_arch.glb", CENTER + Vector3(0, 0.7, -17.0))
		_act_prop("opera_curtain.glb", CENTER + Vector3(-8.6, 0.7, -18.0))
		_act_prop("opera_curtain.glb", CENTER + Vector3(8.6, 0.7, -18.0), 180.0)
		_act_prop("opera_stage_apron.glb", CENTER + Vector3(0, 0.4, 14.4))
		# the Midnight Maestro: authored conductor puppet, primitive fallback
		if _act_prop("opera_maestro.glb", Vector3.ZERO, 180.0, root) == null:
			var gown := CylinderMesh.new()
			gown.top_radius = 0.35
			gown.bottom_radius = 2.8
			gown.height = 6.0
			_mesh(gown, Vector3(0, 3.0, 0), Color(0.13, 0.11, 0.28), 0.12, root)
			_sphere(Vector3(0, 6.2, 0.7), 1.05, Color(0.9, 0.88, 1.0), 0.25, root)
			_sphere(Vector3(-0.4, 6.4, 1.5), 0.22, Color(0.1, 0.1, 0.25), 0.0, root)
			_sphere(Vector3(0.4, 6.4, 1.5), 0.22, Color(0.1, 0.1, 0.25), 0.0, root)
			var baton := _box(Vector3(2.0, 5.4, 0.8), Vector3(0.18, 2.4, 0.18), Color(1.0, 0.85, 0.4), 0.6, root)
			baton.rotation_degrees = Vector3(0, 0, -34.0)
			_sphere(Vector3(0, 4.4, 1.6), 0.4, Color(1.0, 0.85, 0.4), 0.6, root)
	elif dual:
		# Codex phantom puppet, primitive fallback
		if _act_prop("opera_phantom.glb", Vector3.ZERO, 180.0, root) == null:
			var cone := CylinderMesh.new()
			cone.top_radius = 0.3
			cone.bottom_radius = 2.4
			cone.height = 5.2
			_mesh(cone, Vector3(0, 2.6, 0), Color(0.16, 0.13, 0.3), 0.1, root)
			_sphere(Vector3(0, 5.2, 0.8), 1.0, Color(0.94, 0.94, 1.0), 0.25, root)
			_sphere(Vector3(-0.4, 5.4, 1.55), 0.22, Color(0.1, 0.1, 0.25), 0.0, root)
			_sphere(Vector3(0.4, 5.4, 1.55), 0.22, Color(0.1, 0.1, 0.25), 0.0, root)
	else:
		# Codex dragon puppet-on-stick, primitive fallback
		if _act_prop("opera_dragon.glb", Vector3.ZERO, 180.0, root) == null:
			_cyl(Vector3(0, 1.8, 0), 1.1, 3.6, Color(0.35, 0.7, 0.45), 0.1, root)
			_sphere(Vector3(0, 4.4, 0.6), 1.5, Color(0.4, 0.78, 0.5), 0.15, root)
			var snout := CylinderMesh.new()
			snout.top_radius = 0.5
			snout.bottom_radius = 1.0
			snout.height = 1.6
			var sn := _mesh(snout, Vector3(0, 4.1, 2.0), Color(0.55, 0.88, 0.6), 0.15, root)
			sn.rotation_degrees = Vector3(90, 0, 0)
			_sphere(Vector3(-0.6, 5.3, 1.4), 0.28, Color(0.1, 0.1, 0.25), 0.0, root)
			_sphere(Vector3(0.6, 5.3, 1.4), 0.28, Color(0.1, 0.1, 0.25), 0.0, root)
	var first_phase := "shadow" if dual else "hide"
	boss = {"node": root, "home": root.position, "hp": int(config.get("boss_hp", 3)), "phase": first_phase,
		"timer": float(config.get("hide_time", 2.2)), "attack": 1.6, "dual": dual,
		"finale": finale, "mode": "lantern"}
	root.position = (boss["home"] as Vector3) + Vector3(0, -6.5, 0)
	if dual:
		root.position = boss["home"] as Vector3
		root.scale = Vector3.ONE * 0.85
		for i in range(3):
			var lp := CENTER + Vector3(-14.0 + float(i) * 14.0, 1.0, -7.0)
			var lroot := Node3D.new()
			lroot.name = "OperaLantern%d" % i
			lroot.position = lp
			add_child(lroot)
			# Codex lantern post + cage; the glass sphere stays a live primitive
			# below so the flicker can keep pulsing its private material
			if _act_prop("opera_lantern.glb", Vector3.ZERO, 0.0, lroot) == null:
				_box(Vector3(0, 2.0, 0), Vector3(0.4, 4.0, 0.4), Color(0.5, 0.42, 0.3), 0.0, lroot)
			var glass := _sphere(Vector3(0, 4.4, 0), 0.75, Color(1.0, 0.85, 0.45), 0.25, lroot)
			# a private material per lantern so the flicker can pulse emission
			# in place instead of minting cache entries every frame
			glass.material_override = glass.material_override.duplicate() as StandardMaterial3D
			lanterns.append({"index": i, "node": lroot, "pos": lp, "glass": glass, "lit": false})
		lantern_i = 0
		var beam := CylinderMesh.new()
		beam.top_radius = 0.4
		beam.bottom_radius = 3.6
		beam.height = 11.0
		spotlight = _mesh(beam, (boss["home"] as Vector3) + Vector3(0, 7.0, 0), Color(1.0, 0.95, 0.7, 0.22), 0.7)
		var sm := (spotlight as MeshInstance3D).material_override as StandardMaterial3D
		sm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		sm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		spotlight.visible = false

func _light_lantern() -> void:
	if state != "play" or kind != "boss" or not bool(boss.get("dual", false)):
		return
	if String(boss["phase"]) != "shadow":
		return
	var lant: Dictionary = lanterns[lantern_i]
	lant["lit"] = true
	var lit_mat := (lant["glass"] as MeshInstance3D).material_override as StandardMaterial3D
	lit_mat.emission_energy_multiplier = 1.6
	m._sparkle_burst((lant["pos"] as Vector3) + Vector3(0, 4.5, 0), Color(1.0, 0.95, 0.6))
	if m.chime != null:
		m.chime.pitch_scale = 1.2
		m.chime.play()
	# the phantom is caught right beside the lantern the child just lit —
	# the spatial payoff lands exactly where they are standing
	var lant_pos: Vector3 = lant["pos"] as Vector3
	var caught := Vector3(lant_pos.x, CENTER.y + 1.0, CENTER.z - 12.0)
	boss["home"] = caught
	(boss["node"] as Node3D).position = caught
	boss["phase"] = "peek"
	boss["timer"] = float(config.get("peek_time", 5.0))
	boss["attack"] = 1.2
	if spotlight != null:
		spotlight.visible = true
		spotlight.position = caught + Vector3(0, 7.0, 0)
	m.show_msg("Roshan", "The light found him! Tap SPARKLE, quick!", "talk")
	_update_hud()

func _hit_boss() -> void:
	if state != "play" or kind != "boss":
		return
	var phase := String(boss["phase"])
	if phase != "peek":
		# sparkles fizzle kindly against the curtain — never a punishment
		m._sparkle_burst(player_pos + Vector3(0, 3.0, 0), Color(0.7, 0.8, 1.0))
		return
	boss["hp"] = int(boss["hp"]) - 1
	progress_t = 0.0
	var bpos: Vector3 = (boss["node"] as Node3D).position
	m._sparkle_burst(bpos + Vector3(0, 5.0, 1.5), Color(1.0, 0.85, 0.3))
	if m.chime != null:
		m.chime.pitch_scale = 1.1 + 0.15 * float(3 - int(boss["hp"]))
		m.chime.play()
	if int(boss["hp"]) <= 0:
		_win()
		return
	if bool(boss.get("finale", false)):
		# the grand finale remixes both learned verbs: lantern SHINE cycles
		# and curtain-chase SPARKLE cycles alternate with every star
		var lantern_next: bool = String(boss.get("mode", "lantern")) != "lantern"
		boss["mode"] = "lantern" if lantern_next else "roam"
		if spotlight != null:
			spotlight.visible = false
		if lantern_next:
			boss["phase"] = "shadow"
			boss["timer"] = float(config.get("hide_time", 2.0))
			lantern_i = (lantern_i + 1) % lanterns.size()
			m.show_msg("Roshan", "He slipped into the shadows! Find the twinkling lantern with SHINE!", "talk")
		else:
			boss["phase"] = "hide"
			boss["timer"] = float(config.get("hide_time", 2.2))
			m.show_msg("Roshan", "He's dashing along the curtains — SPARKLE when he peeks!", "talk")
	elif bool(boss.get("dual", false)):
		boss["phase"] = "shadow"
		boss["timer"] = float(config.get("hide_time", 2.0))
		lantern_i = (lantern_i + 1) % lanterns.size()
		if spotlight != null:
			spotlight.visible = false
		m.show_msg("Roshan", "He slipped back into the shadows! Find the twinkling lantern!", "talk")
	else:
		boss["phase"] = "hide"
		boss["timer"] = float(config.get("hide_time", 2.2))
	_update_hud()

func _tick_boss(delta: float) -> void:
	if boss.is_empty() or state != "play":
		return
	var root: Node3D = boss["node"] as Node3D
	var home: Vector3 = boss["home"] as Vector3
	boss["timer"] = float(boss["timer"]) - delta
	boss["attack"] = float(boss["attack"]) - delta
	var phase := String(boss["phase"])
	if phase == "hide":
		root.position = root.position.lerp(home + Vector3(0, -6.5, 0), delta * 4.0)
		if float(boss["timer"]) <= 0.0:
			# whack-a-mole roam with a RISING TEMPO: every three stars the
			# dragon gets bolder — quicker peeks and two wider curtain spots
			# unlock, so the chase escalates instead of repeating flat
			var max_hp := int(config.get("boss_hp", 3))
			var tier := clampi((max_hp - int(boss["hp"])) / 3, 0, 2)
			var spots_n := peek_spots.size() if tier >= 1 else mini(3, peek_spots.size())
			peek_i = (peek_i + 1) % spots_n
			var new_home := Vector3(CENTER.x + peek_spots[peek_i], home.y, home.z)
			boss["home"] = new_home
			root.position = new_home + Vector3(0, -6.5, 0)
			boss["phase"] = "peek"
			boss["timer"] = float(config.get("peek_time", 4.5)) * (1.0 - 0.2 * float(tier))
			boss["attack"] = 1.0
			m._sparkle_burst(new_home + Vector3(0, 5.0, 1.0), Color(0.6, 0.95, 0.7))
	elif phase == "peek":
		root.position = root.position.lerp(home, delta * 5.0)
		root.rotation.y = sin(elapsed * 1.6) * 0.2
		if float(boss["attack"]) <= 0.0:
			boss["attack"] = 2.0
			_spawn_puff(root.position + Vector3(0, 4.5, 1.5))
		if float(boss["timer"]) <= 0.0:
			# no fail on a missed peek: a lantern cycle re-hides into shadow (the
			# same lantern twinkles again); a roam cycle just dives back behind
			# the curtains — the finale keeps whichever mode this cycle is in
			var relight: bool = (bool(boss.get("dual", false))
				and (not bool(boss.get("finale", false)) or String(boss.get("mode", "lantern")) == "lantern"))
			if relight:
				boss["phase"] = "shadow"
				boss["timer"] = 1.0
				if spotlight != null:
					spotlight.visible = false
				m.show_msg("Roshan", "He's hiding again! Light the twinkling lantern with SHINE!", "hint")
			else:
				boss["phase"] = "hide"
				boss["timer"] = float(config.get("hide_time", 2.2))
	else:
		# "shadow" (dual only): flicker the target lantern until it is lit
		root.position = root.position.lerp(home, delta * 4.0)
		var lant: Dictionary = lanterns[lantern_i]
		var flicker_mat := (lant["glass"] as MeshInstance3D).material_override as StandardMaterial3D
		flicker_mat.emission_energy_multiplier = 0.35 + 0.3 * sin(elapsed * 9.0)
	_tick_puffs(delta)
	_update_hud()

func _spawn_puff(from: Vector3) -> void:
	var dir: Vector3 = player_pos - from
	dir.y = 0.0
	if dir.length() < 0.1:
		return
	var orb := _sphere(from, 0.6, Color(0.7, 0.85, 1.0, 0.8), 0.8)
	puffs.append({"node": orb, "vel": dir.normalized() * 8.0, "life": 3.5})

func _tick_puffs(delta: float) -> void:
	bump_cool = maxf(0.0, bump_cool - delta)
	far_hint_cool = maxf(0.0, far_hint_cool - delta)
	for i in range(puffs.size() - 1, -1, -1):
		var puff: Dictionary = puffs[i]
		var node: Node3D = puff["node"] as Node3D
		node.position += (puff["vel"] as Vector3) * delta
		puff["life"] = float(puff["life"]) - delta
		if node.position.distance_to(player_pos + Vector3(0, 1.5, 0)) < 2.0:
			var away: Vector3 = player_pos - node.position
			away.y = 0.0
			if away.length() < 0.1:
				away = Vector3.FORWARD
			player_pos += away.normalized() * 3.0
			m._sparkle_burst(player_pos + Vector3(0, 2.0, 0), Color(0.55, 0.92, 1.0))
			if bump_cool <= 0.0:
				bump_cool = 4.0
				m.show_msg("Roshan", "My bubble shield bounced it away! Keep going!", "talk")
			puff["life"] = 0.0
		if float(puff["life"]) <= 0.0:
			node.queue_free()
			puffs.remove_at(i)

func _fire_star() -> void:
	# sparkles only reach a nearby boss: chasing him across the stage is the
	# game. Far shots fall short with a kindly hint instead of failing.
	var bpos: Vector3 = (boss["node"] as Node3D).position
	if String(boss["phase"]) == "peek" and bpos.distance_to(player_pos) > 18.0:
		var short := _sphere(player_pos + Vector3(0, 2.2, 0), 0.45, Color(1.0, 0.9, 0.4), 1.2)
		var tw_s := short.create_tween()
		tw_s.tween_property(short, "position", player_pos.lerp(bpos, 0.4) + Vector3(0, 2.0, 0), 0.35).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw_s.tween_property(short, "scale", Vector3.ZERO, 0.2)
		tw_s.tween_callback(short.queue_free)
		if far_hint_cool <= 0.0:
			far_hint_cool = 5.0
			m.show_msg("Roshan", "Almost! Swim closer so the sparkles can reach him!", "hint")
		return
	var target: Vector3 = bpos + Vector3(0, 4.5, 0)
	var orb := _sphere(player_pos + Vector3(0, 2.2, 0), 0.5, Color(1.0, 0.9, 0.4), 1.6)
	var tw := orb.create_tween()
	tw.tween_property(orb, "position", target, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw.tween_callback(orb.queue_free)
	_hit_boss()

# ---------------- input, tick, win ----------------

func _move_input() -> Vector2:
	var value := Vector2.ZERO
	if Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT):
		value.x -= 1.0
	if Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT):
		value.x += 1.0
	if Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP):
		value.y -= 1.0
	if Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN):
		value.y += 1.0
	var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
	var jy: float = m.joy_axis(JOY_AXIS_LEFT_Y)
	if absf(jx) > 0.18:
		value.x = jx
	if absf(jy) > 0.18:
		value.y = jy
	if m.touch_ui != null and m.touch_ui.stick_vec.length() > 0.12:
		value = m.touch_ui.stick_vec
	return value.limit_length(1.0)

func _action_pressed() -> bool:
	var held: bool = Input.is_physical_key_pressed(KEY_SPACE) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
	var just: bool = held and not fire_prev
	fire_prev = held
	if m.touch_ui != null and m.touch_ui.consume_action_just():
		just = true
	return just

func _nearest_pad() -> int:
	var group: Array[Dictionary] = hats if kind == "shuffle" else pads
	var best := -1
	var best_d := PAD_REACH
	for entry in group:
		var d: float = (entry["pos"] as Vector3).distance_to(player_pos)
		if d < best_d:
			best_d = d
			best = int(entry["index"])
	return best

func _act_action(choice: int) -> void:
	match kind:
		"order", "paint":
			_order_action(choice)
		"shuffle":
			_shuffle_action(choice)

func _process(delta: float) -> void:
	if m == null or state == "done":
		return
	elapsed += delta
	progress_t += delta
	if doc_wait > 0.0:
		doc_wait -= delta
	if state == "won":
		win_t -= delta
		if fmod(win_t, 0.35) < delta:
			m._sparkle_burst(CENTER + Vector3(randf_range(-12.0, 12.0), randf_range(1.0, 8.0), randf_range(-8.0, 10.0)), Color.from_hsv(randf(), 0.5, 1.0))
		if kind == "echo":
			# free-dance encore: during the applause every tile still lights up
			# under Roshan — a pure toy moment with no goal at all
			var move2 := _move_input()
			player_pos += Vector3(move2.x, 0, move2.y) * MOVE_SPEED * delta
			_place_avatar(delta)
			var on_pad := -1
			for pad in pads:
				if (pad["pos"] as Vector3).distance_to(player_pos) < 3.2:
					on_pad = int(pad["index"])
			if on_pad >= 0 and on_pad != last_pad:
				last_pad = on_pad
				_echo_light(on_pad, true)
			elif on_pad < 0:
				last_pad = -1
		if win_t <= 0.0:
			_finish()
		return
	if kind == "race" and kart != null:
		# KartGame owns the camera, HUD and every input while the race runs —
		# consuming taps here would steal the TURBO button
		return
	if kind == "scroll":
		_tick_farm(delta)
		if _action_pressed():
			_toss_action()
		if progress_t > 22.0:
			progress_t = 0.0
			m.show_msg("Roshan", String(config.get("voice", "Follow the golden sparkle!")), "hint")
		return
	var move := _move_input()
	player_pos += Vector3(move.x, 0, move.y) * MOVE_SPEED * delta
	_clamp_player()
	_place_avatar(delta)
	for i in range(audience.size()):
		audience[i].position.y = CENTER.y + 4.0 + sin(elapsed * 2.2 + float(i) * 1.4) * 0.18
	if stage_phase == "brawl":
		_tick_brawl(delta)
		if _action_pressed():
			_brawl_action()
		if progress_t > 22.0:
			progress_t = 0.0
			m.show_msg("Roshan", "Tap SPARKLE to pop the mischief imps, then the curtain opens!", "hint")
		_tick_pointer()
		return
	if _action_pressed():
		match kind:
			"order", "paint":
				if order_phase == "stir":
					if goal.position.distance_to(player_pos) < 5.5:
						_stir_action()
				elif order_phase == "decorate":
					for spot in deco_spots:
						if not bool(spot["done"]) and (spot["pos"] as Vector3).distance_to(player_pos) < 4.5:
							_deco_action(int(spot["index"]))
							break
				else:
					var near_pad := _nearest_pad()
					if near_pad >= 0:
						_act_action(near_pad)
			"shuffle":
				var near := _nearest_pad()
				if near >= 0:
					_act_action(near)
			"fix":
				if fix_phase == "valve":
					if valve.position.distance_to(player_pos) < 6.0:
						_turn_valve()
					else:
						m._sparkle_burst(player_pos + Vector3(0, 2.5, 0), Color(0.8, 0.85, 1.0))
				elif carried < 0:
					var near_piece := _nearest_piece()
					if near_piece >= 0:
						_pick_piece(near_piece)
				elif fix_step < slots.size() and (slots[fix_step]["pos"] as Vector3).distance_to(player_pos) < 5.0:
					_place_piece()
			"press":
				_press_action()
			"box":
				_punch_action()
			"sleuth":
				if chest_ready and goal.position.distance_to(player_pos) < 5.5:
					_sleuth_chest()
				else:
					var near_prop := -1
					var near_prop_d := 4.5
					for prop: Dictionary in sleuth_props:
						if bool(prop["opened"]):
							continue
						var pd: float = (prop["pos"] as Vector3).distance_to(player_pos)
						if pd < near_prop_d:
							near_prop_d = pd
							near_prop = int(prop["index"])
					if near_prop >= 0:
						_sleuth_action(near_prop)
			"doctor":
				var near_doc := _nearest_doc_target()
				if near_doc >= 0:
					_doctor_action(near_doc)
			"race":
				if race_flag != null and race_flag.position.distance_to(player_pos) < 5.5:
					_launch_race()
			"dance":
				if mic != null and mic.position.distance_to(player_pos) < 5.5:
					_open_dance()
			"boss":
				if bool(boss.get("dual", false)) and String(boss["phase"]) == "shadow":
					var lant: Dictionary = lanterns[lantern_i]
					if (lant["pos"] as Vector3).distance_to(player_pos) < 5.5:
						_light_lantern()
					else:
						m._sparkle_burst(player_pos + Vector3(0, 2.5, 0), Color(0.8, 0.85, 1.0))
				else:
					_fire_star()
	match kind:
		"box":
			_tick_box(delta)
		"order", "paint":
			if order_hidden:
				# the detective search: clues pop out when Roshan swims close
				for pad in pads:
					if not bool(pad["revealed"]) and (pad["pos"] as Vector3).distance_to(player_pos) < 6.5:
						pad["revealed"] = true
						var prop := pad["prop"] as Node3D
						prop.visible = true
						prop.scale = Vector3.ZERO
						var tw_r := prop.create_tween()
						tw_r.tween_property(prop, "scale", Vector3.ONE, 0.4).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
						m._sparkle_burst((pad["pos"] as Vector3) + Vector3(0, 2.5, 0), Color(0.8, 0.95, 1.0))
						if m.chime != null:
							m.chime.pitch_scale = 1.25
							m.chime.play()
			if order_flow == "carry_paint" and brush_loaded >= 0:
				brush_node.position = player_pos + Vector3(0, 3.2, 0)
				brush_node.rotation.z = sin(elapsed * 6.0) * 0.25
				_tick_easel(delta)
			elif paint_easel:
				_leave_easel()
		"echo":
			_tick_echo(delta)
			if echo_phase == "repeat":
				var touched := -1
				var near_any := false
				for pad in pads:
					var d: float = (pad["pos"] as Vector3).distance_to(player_pos)
					if d < 3.2:
						near_any = true
						touched = int(pad["index"])
				var echo_speed := (player_pos - echo_prev_pos).length() / maxf(delta, 0.001)
				echo_prev_pos = player_pos
				if not near_any:
					last_pad = -1
					dwell_pad = -1
					pad_dwell = 0.0
				elif touched >= 0 and touched != last_pad:
					# stand STILL on a tile a beat to dance it — swimming
					# across the row at any speed never commits a step
					if touched == dwell_pad and echo_speed < 3.0:
						pad_dwell += delta
						if pad_dwell >= 0.25:
							last_pad = touched
							dwell_pad = -1
							pad_dwell = 0.0
							_pad_touch(touched)
					else:
						dwell_pad = touched
						pad_dwell = 0.0 if touched != dwell_pad else pad_dwell
		"shuffle":
			_tick_shuffle(delta)
		"fix":
			_tick_fix(delta)
		"press":
			_tick_press(delta)
		"boss":
			_tick_boss(delta)
	if progress_t > 22.0:
		progress_t = 0.0
		m.show_msg("Roshan", String(config.get("voice", "Follow the golden sparkle!")), "hint")
	_tick_pointer()

func _clamp_player() -> void:
	if stage_phase == "brawl":
		player_pos.x = clampf(player_pos.x, CENTER.x + BACKSTAGE_X0 + 2.0, CENTER.x + BACKSTAGE_X1 - 1.5)
		player_pos.z = clampf(player_pos.z, CENTER.z - 6.0, CENTER.z + 12.0)
		return
	if bool(config.get("shell", false)) and player_pos.x < CENTER.x + BACKSTAGE_X1:
		# the opened corridor stays swimmable — clamp to its walls instead
		player_pos.x = maxf(player_pos.x, CENTER.x + BACKSTAGE_X0 + 2.0)
		player_pos.z = clampf(player_pos.z, CENTER.z - 6.0, CENTER.z + 12.0)
		return
	var flat := Vector2(player_pos.x - CENTER.x, player_pos.z - CENTER.z)
	if flat.length() > RADIUS - 2.0:
		flat = flat.normalized() * (RADIUS - 2.0)
		player_pos.x = CENTER.x + flat.x
		player_pos.z = CENTER.z + flat.y

func _pointer_target() -> Vector3:
	if stage_phase == "brawl":
		var best_d := INF
		var best := player_pos
		var any := false
		for g in imps:
			if bool(g["popped"]):
				continue
			var d: float = (g["pos"] as Vector3).distance_to(player_pos)
			if d < best_d:
				best_d = d
				best = (g["pos"] as Vector3)
				any = true
		if any:
			return best + Vector3(0, 5.5, 0)
		return player_pos + Vector3(0, 7.0, 0)
	match kind:
		"box":
			if box_phase == "belt" and box_belt != null:
				return box_belt.position + Vector3(0, 2.2, 0)
			if box_phase == "warmup" and box_bag != null:
				return box_bag.position + Vector3(0, 7.2, 0)
			for g in imps:
				if not bool(g["popped"]):
					return (g["pos"] as Vector3) + Vector3(0, 5.0, 0)
			return CENTER + Vector3(0, 8.0, -2.0)
		"sleuth":
			if chest_ready:
				return goal.position + Vector3(0, 6.0, 0)
			for prop: Dictionary in sleuth_props:
				if not bool(prop["opened"]) and bool(prop["clue"]):
					return (prop["pos"] as Vector3) + Vector3(0, 5.5, 0)
			return CENTER + Vector3(0, 8.0, 3.0)
		"order", "paint":
			if order_phase == "stir":
				return goal.position + Vector3(0, 7.5, 0)
			if order_phase == "decorate":
				for spot in deco_spots:
					if not bool(spot["done"]):
						return (spot["pos"] as Vector3) + Vector3(0, 4.5, 0)
				return goal.position + Vector3(0, 7.5, 0)
			if brush_loaded >= 0:
				return canvas_pos + Vector3(0, 7.5, 0)
			if step < order_steps.size():
				var pad: Dictionary = pads[order_steps[step]]
				return (pad["pos"] as Vector3) + Vector3(0, 5.5, 0)
		"echo":
			if echo_phase == "repeat" and echo_pos < echo_seq.size():
				return (pads[echo_seq[echo_pos]]["pos"] as Vector3) + Vector3(0, 5.5, 0)
			return CENTER + Vector3(0, 9.0, 3.0)
		"shuffle":
			if shuffle_phase == "watch":
				return CENTER + Vector3(0, 8.0, 3.0)
			return player_pos + Vector3(0, 7.0, 0)
		"fix":
			if fix_phase == "valve":
				return valve.position + Vector3(0, 4.5, 0)
			if carried >= 0 and fix_step < slots.size():
				return ((slots[fix_step]["node"] as Node3D)).position + Vector3(0, 6.0, 0)
			if fix_step < slots.size():
				var need := int(slots[fix_step]["need"])
				return (pieces[need]["pos"] as Vector3) + Vector3(0, 5.5, 0)
		"press":
			return CENTER + Vector3(0, 12.5, -8.5)
		"doctor":
			if doc_step < doc_targets.size():
				return (doc_targets[doc_step]["pos"] as Vector3) + Vector3(0, 5.5, 0)
		"race":
			if race_flag != null:
				return race_flag.position + Vector3(0, 7.0, 0)
		"dance":
			if mic != null:
				return mic.position + Vector3(0, 7.0, 0)
		"boss":
			if bool(boss.get("dual", false)) and String(boss["phase"]) == "shadow":
				return (lanterns[lantern_i]["pos"] as Vector3) + Vector3(0, 7.5, 0)
			return ((boss["node"] as Node3D).position) + Vector3(0, 9.0, 0)
	return player_pos + Vector3(0, 7.0, 0)

func _tick_pointer() -> void:
	var show := state == "play" and not (kind == "shuffle" and shuffle_phase == "pick")
	# guessing games earn a moment without the answer: the arrow is a rescue
	# that arrives after RESCUE_DELAY without progress (mistakes summon it).
	# The brawl arrow is directional, not an answer — always on.
	if stage_phase == "brawl":
		pass
	elif _is_order_kind() and not order_hidden:
		show = show and progress_t > RESCUE_DELAY
	elif kind == "echo" and echo_phase == "repeat":
		show = show and progress_t > RESCUE_DELAY
	elif kind == "sleuth" and not chest_ready:
		# searching IS the game — the arrow only rescues a stuck detective
		show = show and progress_t > RESCUE_DELAY
	pointer.visible = show
	pointer.position = _pointer_target() + Vector3(0, sin(elapsed * 4.0) * 0.45, 0)

func _wobble(node: Node3D) -> void:
	var tw := node.create_tween()
	tw.tween_property(node, "rotation:z", 0.14, 0.09)
	tw.tween_property(node, "rotation:z", -0.14, 0.09)
	tw.tween_property(node, "rotation:z", 0.0, 0.09)

func _update_hud() -> void:
	if objective == null:
		return
	var tag := act_tag + "  •  " if act_tag != "" else ""
	if stage_phase == "brawl":
		objective.text = tag + "✨  Pop the mischief imps!  %d / %d" % [imp_count - imps_left, imp_count]
		return
	match kind:
		"order", "paint":
			if order_phase == "stir":
				objective.text = tag + "🥄  STIR the big bowl!  %d / 3" % stir_done
			elif order_phase == "decorate":
				objective.text = tag + "🍒  Plop the toppings on!  %d / %d" % [deco_done, deco_spots.size()]
			elif brush_loaded >= 0:
				if paint_easel:
					var pct := int(clampf(float(paint_band_done) / maxf(1.0, float(paint_band_need)), 0.0, 1.0) * 100.0)
					objective.text = tag + "🖌  DRAG to paint!  %d%%" % pct
				else:
					objective.text = tag + "🖌  Carry the brush to the canvas!  %d / %d" % [step, order_steps.size()]
			else:
				objective.text = tag + "✨  Match the pictures!  %d / %d" % [step, order_steps.size()]
		"box":
			if box_phase == "belt":
				objective.text = tag + "🏆  CHAMPION! Swim up and take the belt!"
			elif box_phase == "warmup":
				objective.text = tag + "🥊  Warm up on the bag!  %d / %d" % [box_bag_hits, box_bag_goal]
			elif box_wait > 0.0:
				objective.text = tag + "🥊  Round won! Get ready..."
			else:
				var waves: Array = config.get("rounds", [3, 4, 5])
				objective.text = tag + "🥊  ROUND %d / %d — bop the imps!  %d left" % [box_round + 1, waves.size(), imps_left]
		"sleuth":
			if chest_ready:
				objective.text = tag + "💎  Tap the treasure chest!"
			else:
				objective.text = tag + "🔍  Peek in the boxes!  %d / 3 clues" % clues_found
		"echo":
			if echo_phase == "show":
				objective.text = tag + "👀  WATCH the twinkling tiles!"
			else:
				objective.text = tag + "🩰  YOUR TURN!  %d / %d" % [echo_pos, echo_seq.size()]
		"shuffle":
			if shuffle_phase == "watch":
				objective.text = tag + "👀  WATCH the hats dance!"
			else:
				objective.text = tag + "🎩  PICK the bunny-fish hat!  %d / %d" % [shuffle_round, int(config.get("rounds", 2))]
		"fix":
			if fix_phase == "valve":
				objective.text = tag + "💨  Spin the big valve — tap USE!  %d / 3" % valve_spins
			elif carried >= 0:
				objective.text = tag + "🔧  Carry it to the glowing gap!  %d / %d" % [fix_step, slots.size()]
			else:
				objective.text = tag + "🔧  Grab the pipe piece under the arrow!  %d / %d" % [fix_step, slots.size()]
		"press":
			objective.text = tag + "🍬  PRESS when the star is in the green middle!  %d / %d" % [candies_done, candies_goal]
		"doctor":
			objective.text = tag + "🩺  Help the plushy feel better!  %d / %d" % [doc_step, doc_targets.size()]
		"scroll":
			objective.text = tag + "🐷  TOSS veggies to the hungry piggies!  %d / %d" % [farm_fed, piggies.size()]
		"race":
			objective.text = tag + "🏁  Race the Opera Grand Prix!"
		"dance":
			objective.text = tag + "🎤  Tap the microphone and dance the arrows!"
		"boss":
			var hearts := ""
			for i in range(maxi(0, int(boss.get("hp", 0)))):
				hearts += "★"
			if bool(boss.get("dual", false)) and String(boss.get("phase", "")) == "shadow":
				objective.text = tag + "🏮  Find the twinkling lantern — tap SHINE!  " + hearts
			else:
				objective.text = tag + "✨  Tap SPARKLE when he peeks!  " + hearts

func _win() -> void:
	if state != "play":
		return
	state = "won"
	win_t = 2.6
	pointer.visible = false
	objective.text = "🎉  TA-DAAA!  🎉"
	if farm_layer != null:
		farm_layer.visible = false   # lift the 2D meadow so the stage bow shows
	# curtain-call bow: the audience hops and the star of the show gets confetti
	for spr: Node3D in audience:
		var tw := spr.create_tween()
		tw.tween_property(spr, "position:y", spr.position.y + 0.9, 0.25).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(spr, "position:y", spr.position.y, 0.3)
	m._sparkle_burst(player_pos + Vector3(0, 3.0, 0), Color(1.0, 0.85, 1.0))
	if kind == "press":
		# the three smiley candies do a little parade hop down the shelf
		# (relative hops, delayed past the last candy's slide onto the shelf)
		for i in range(shelf_candies.size()):
			var c := shelf_candies[i]
			if not is_instance_valid(c):
				continue
			var hop := c.create_tween()
			hop.tween_interval(1.1 + float(i) * 0.25)
			hop.tween_property(c, "position:y", 1.2, 0.22).as_relative().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			hop.tween_property(c, "position:y", -1.2, 0.28).as_relative().set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
	if kind == "boss":
		var root: Node3D = boss["node"] as Node3D
		var tw2 := root.create_tween()
		tw2.tween_property(root, "position", (boss["home"] as Vector3) + Vector3(0, 0, 4.0), 0.8).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
		tw2.tween_property(root, "rotation:x", 0.35, 0.4)
		tw2.tween_property(root, "rotation:x", 0.0, 0.4)
	m.show_msg("Roshan", String(config.get("win_line", "What a show! Everybody is cheering!")), "win")

func _finish() -> void:
	if state == "done":
		return
	state = "done"
	_leave_easel()
	_release_avatar()
	if prev_env != null:
		m.we_node.environment = prev_env
	if finish_cb.is_valid():
		finish_cb.call()
	queue_free()

func cancel() -> void:
	_leave_easel()
	if state == "done":
		return
	if state == "won":
		_finish()   # the applause was already earned; leaving skips only the delay
		return
	state = "done"
	_release_avatar()
	# guest engines clean up their own borrowed state (music, pause) first
	if kart != null and is_instance_valid(kart):
		kart.queue_free()
		kart = null
		m._play_music(race_prev_track if race_prev_track != "" else "level2")
	if dance != null and is_instance_valid(dance) and bool(dance.get("active")):
		dance.call("close_demo")
	if prev_env != null:
		m.we_node.environment = prev_env
	queue_free()

func action_label() -> String:
	if stage_phase == "brawl":
		return "SPARKLE"
	match kind:
		"echo":
			return "DANCE"
		"press":
			return "PRESS"
		"box":
			return "PUNCH"
		"sleuth":
			return "PEEK"
		"scroll":
			return "TOSS"
		"race":
			if kart != null:
				return String(kart.call("action_label"))
			return "GO!"
		"dance":
			return "SING"
		"boss":
			if bool(boss.get("dual", false)) and String(boss.get("phase", "")) == "shadow":
				return "SHINE"
			return "SPARKLE"
	return "USE"
