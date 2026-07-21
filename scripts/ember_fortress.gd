extends Node3D
class_name EmberFortressLevel

# ============================================================================
# THE EMBER FORTRESS — the Volcanic Throne Planet. A later-game "scary" world:
# a small artificial fortress-planet wrapped around volcanic energy, in the
# spirit of the classic infernal citadel at the edge of space (generic homage —
# no branded characters, symbols or assets). Dark basalt, glowing lava rivers,
# obsidian towers, oversized gates, dragon-turtle statues — theatrical menace,
# zero real threat: lava only makes Roshan hop, nothing can be lost.
#
# Reached at the RAINBOW JUNCTION in the Sky Lagoon: a dark ember gateway
# stands beyond the two rainbow-race legs. Swimming in launches the floating
# rainbow kart race — and this time the road dives DOWN off the rainbow into
# the dark planet instead of soaring on to the galaxy.
#
# Self-contained (same pattern as GalaxyLevel): builds its own planet, sky,
# avatar, camera, HUD and objective; freezes the main player while active;
# calls finish_cb(completed: bool) and frees itself on exit.
#
# GOAL: light the 5 EMBER LANTERNS around the planet; the Ember King's GREAT
# GATE at the north-pole fortress then opens — inside waits the six-room
# FORTRESS DUNGEON (DungeonLevel machinery, volcanic room table, its own
# ember_progress/ember_done checkpoints). A rainbow home-ring at the south
# pole exits at any time.
#
# Movement is the galaxy vocabulary: stick/arrows = run & turn on the sphere,
# tap / SPACE / gamepad-A = JUMP (radial, floaty). Gravity is the planet's.
#
# Light budget: 7 OmniLights total (5 lanterns + king + avatar trail) — far
# below the Butterfly World's existing per-scene peak, and this level never
# coexists with another outdoor world, so no new global maximum. Lava glow
# leans on emissive materials + the shared bloom, not lights.
# ============================================================================

const PLANET_R := 40.0
const ORIGIN := Vector3(0.0, 15000.0, 0.0)   # own pocket, clear of galaxy (9000) and hall (9300)
const GRAV := 26.0
const JUMP_V := 17.0
const RUN_SPD := 13.5
const TURN_SPD := 2.4
const LANTERNS := 5
const GATE_DIR := Vector3(0.0, 0.92, 0.4)      # the Great Gate, on the fortress hill's south face
const KING_DIR := Vector3(0.0, 0.985, 0.17)    # the Ember King watches from above his gate
const CRYSTALS := ["res://assets/galaxy/crystal1.glb", "res://assets/galaxy/crystal2.glb", "res://assets/galaxy/crystal3.glb"]
const ROCKS := ["res://assets/aquatic/Rock1.glb", "res://assets/aquatic/Rock4.glb", "res://assets/aquatic/Rock7.glb", "res://assets/aquatic/Rock10.glb"]
const GATE_GLB := "res://assets/art35/castle/dungeon_gate.glb"
const LANTERN_GLB := "res://assets/dungeon/pepper_lantern.glb"
const DRAGON_GLB := "res://assets/dungeon/dragon_turtle.glb"
const STATUE_GLB := "res://assets/dungeon/turtle_statue.glb"
const TOWER_GLB := "res://assets/kits/castle/tower-square.glb"
const WALL_GLB := "res://assets/kits/castle/wall.glb"
const FLAG_GLB := "res://assets/kits/castle/flag.glb"
# lantern spots dodge the two lava-river latitude bands (see _lava_mix)
const LANTERN_DIRS := [
	Vector3(0.6, 0.55, 0.58), Vector3(-0.8, 0.05, 0.6), Vector3(0.75, -0.05, -0.66),
	Vector3(-0.5, -0.65, -0.57), Vector3(-0.15, 0.5, -0.85),
]
const VENT_DIRS := [Vector3(1.0, 0.3, 0.4), Vector3(-0.6, -0.35, 0.7), Vector3(0.3, -0.8, -0.5)]
const EMBER_COL := Color(1.0, 0.5, 0.16)
const LAVA_COL := Color(1.0, 0.36, 0.08)

# The six-room FORTRESS DUNGEON: the Ember King's defensive layers. Same data
# schema as DungeonLevel.ROOMS — CombatArena battles + DungeonPuzzleRoom
# puzzles — restyled to charcoal stone and lava trim. Roshan's ICE magic is
# the counter to the fire fortress; the King himself is the dual-element
# finale on his molten throne.
const ROOMS := [
	{"name": "Cinder Gate Imps", "type": "combat", "kind": "ice", "enemy_count": 4, "layout": "ring", "imp_speed": 1.2, "attack_gap": 3.6, "popcorn_count": 5, "win_spark_gap": 0.4, "background": Color(0.09, 0.045, 0.05), "floor": Color(0.30, 0.22, 0.24), "trim": Color(1.0, 0.55, 0.25)},
	{"name": "Lava Stepping Stones", "type": "puzzle", "puzzle": "path", "solution": [1, 0, 0, 1], "voice": "The little glowing stones show a path across the lava. Swim to the left or right arrow and freeze each step!", "background": Color(0.10, 0.04, 0.04), "floor": Color(0.26, 0.16, 0.16), "trim": Color(1.0, 0.48, 0.2)},
	{"name": "Ember Chimes", "type": "puzzle", "puzzle": "sequence", "choices": ["◆", "●", "▲"], "solution": [2, 0, 1], "choice_count": 3, "voice": "Look at the three big fire crystal pictures. Swim to those crystal pads in the same order!", "background": Color(0.08, 0.05, 0.07), "floor": Color(0.28, 0.20, 0.26), "trim": Color(1.0, 0.62, 0.3)},
	{"name": "Ash Imp Ambush", "type": "combat", "kind": "ice", "enemy_count": 6, "layout": "spiral", "imp_speed": 1.5, "attack_gap": 3.2, "popcorn_count": 5, "win_spark_gap": 0.4, "background": Color(0.07, 0.05, 0.06), "floor": Color(0.24, 0.20, 0.22), "trim": Color(0.95, 0.5, 0.28)},
	{"name": "Door of Fire and Ice", "type": "puzzle", "puzzle": "elemental", "choices": ["❄", "🔥"], "solution": [1, 0, 1, 1, 0], "button_count": 2, "voice": "The King's big door shows fire and ice. Copy its magic picture order!", "background": Color(0.09, 0.05, 0.08), "floor": Color(0.30, 0.22, 0.30), "trim": Color(1.0, 0.66, 0.34)},
	{"name": "The Molten Throne", "type": "combat", "kind": "dual", "dual_phase": true, "boss_hp": 4, "peek_time": 3.2, "shell_time": 5.0, "shell_speed": 5.2, "attack_gap": 1.25, "win_spark_gap": 0.4, "background": Color(0.10, 0.03, 0.03), "floor": Color(0.30, 0.10, 0.10), "trim": Color(1.0, 0.42, 0.15)},
]
const FLAVOR := {
	"hero_title": "FORTRESS\nHERO!",
	"complete_msg": "All six rooms! The Ember Fortress is sparkling and safe!",
	"leave_done_msg": "All six fortress rooms are safe!",
}

var _main: Node = null
var _player_node: Node3D = null
var _finish_cb: Callable
var _cam: Camera3D = null
var _prev_env: Environment = null
var _hud: CanvasLayer = null
var _lbl_lanterns: Label = null
var _lbl_big: Label = null
var _lbl_hint: Label = null

# avatar state on the sphere (same scheme as GalaxyLevel)
var _dir := Vector3(0, 0, 1)
var _fwd := Vector3(1, 0, 0)
var _h := 0.0
var _vy := 0.0
var _avatar: Node3D = null
var _fire_prev := false
var _bob_t := 0.0
var _last_move := 0.0

# look-around peek — same feel as galaxy.gd / player.gd chase camera
var _cam_orbit := 0.0
var _cam_pitch := 0.0
var _mlook_dx := 0.0
var _mlook_dy := 0.0

var _lanterns: Array = []         # {node, dir, lit, flame, beam, light, idx}
var _lit := 0
var _gate_open := false
var _gate_cool := 0.0
var _gate_node: Node3D = null
var _gate_veil: MeshInstance3D = null
var _king: Node3D = null
var _king_cool := 0.0
var _blockers: Array = []         # {dir, r, cool} — solid footprints (surface metres)
var _vents: Array = []            # lava geysers: {dir, cool}
var _sizzle_cool := 0.0
var _sizzle_say := 0.0
var _moon: Node3D = null
var _flags: Array = []            # banner nodes for a slow ripple
var _state := "play"              # play -> done
var _celebrated := false          # first-completion fanfare shown this visit

# ---------------------------------------------------------------- lifecycle

func joy_axis(axis: int) -> float:
	var m: Node = _main
	if m != null and m.has_method("joy_axis"):
		return m.joy_axis(axis)
	return Input.get_joy_axis(0, axis)

func joy_pressed(btn: int) -> bool:
	var m: Node = _main
	if m != null and m.has_method("joy_pressed"):
		return m.joy_pressed(btn)
	return Input.is_joy_button_pressed(0, btn)

func _input(ev: InputEvent) -> void:
	if ev is InputEventMouseMotion and (ev.button_mask & MOUSE_BUTTON_MASK_RIGHT) != 0:
		_mlook_dx += ev.relative.x
		_mlook_dy += ev.relative.y

func start(main: Node, finish_cb: Callable) -> void:
	_main = main
	_finish_cb = finish_cb
	if "player" in main and main.player != null:
		_player_node = main.player
	_build_env_sky()
	_build_planet()
	_build_fortress()
	_build_lanterns()
	_build_decor()
	_build_home_ring()
	_build_avatar()
	_build_camera()
	_build_hud()
	var done: bool = "ember_done" in main and bool(main.ember_done)
	_lbl_big.text = "🌋 The Ember Fortress 🌋"
	if done:
		_lbl_hint.text = "The fortress is friendly now! Visit the Ember King — or knock on his gate to play the dungeon again!"
	elif _lit >= LANTERNS:
		_lbl_hint.text = "The Great Gate is OPEN — walk in when you feel brave!"
	elif _lit > 0:
		_lbl_hint.text = "%d lanterns are already burning — follow the red beacons to the rest!" % _lit
	else:
		_lbl_hint.text = "Ooh, a spooky planet! Light the 5 ember lanterns to open the King's Great Gate!"
	if _main != null and _main.has_method("show_msg"):
		if done:
			_main.show_msg("Ember King", "My favourite little hero is back! My fortress is your playground!", "greet")
		else:
			_main.show_msg("Ember King", "RRRUMBLE! Who dares visit my volcano fortress? Light my five lanterns... if you are brave enough!", "talk")
	var tw := create_tween()
	tw.tween_interval(3.0)
	tw.tween_callback(func():
		if _lbl_big != null and _state == "play" and not _celebrated:
			_lbl_big.text = "")

# ---------------------------------------------------------------- sky & env

func _build_env_sky() -> void:
	if "we_node" in _main and _main.we_node != null:
		_prev_env = _main.we_node.environment
		var e := Environment.new()
		e.background_mode = Environment.BG_COLOR
		e.background_color = Color(0.02, 0.008, 0.01)
		e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		e.ambient_light_color = Color(0.52, 0.36, 0.34)
		e.ambient_light_energy = 0.6
		# low bloom threshold so the lava rivers and lantern flames bleed light
		_main._wind_waker_bloom(e, 0.7, 0.1, 0.95)
		_main._apply_scene_grade(e, "ember")
		_main.we_node.environment = e
	# a dim smoulder sun + a hot lava rim from below the horizon
	var sun := DirectionalLight3D.new()
	sun.light_energy = 0.55
	sun.light_color = Color(1.0, 0.78, 0.62)
	sun.rotation_degrees = Vector3(-38, 40, 0)
	add_child(sun)
	var rim := DirectionalLight3D.new()
	rim.light_energy = 0.4
	rim.light_color = Color(1.0, 0.4, 0.18)
	rim.rotation_degrees = Vector3(24, 215, 0)
	add_child(rim)
	# the storm-and-ember sky: one huge inside-out sphere, pure shader —
	# dark smoke bands, sparse stars, drifting sparks rising past the planet
	var sky := MeshInstance3D.new()
	var sm := SphereMesh.new()
	sm.radius = 750.0
	sm.height = 1500.0
	sky.mesh = sm
	var sh := Shader.new()
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
	// deep charcoal space with a smouldering maroon glow low on the sky
	vec3 col = mix(vec3(0.015, 0.006, 0.010), vec3(0.10, 0.030, 0.022), pow(1.0 - abs(uv.y - 0.42) * 2.0, 3.0));
	// slow rolling smoke bands
	float smoke = noise2(vec2(uv.x * 5.0 + TIME * 0.02, uv.y * 9.0));
	col = mix(col, vec3(0.05, 0.028, 0.032), smoke * 0.5);
	// sparse cold stars peeking through the smoke
	vec2 g1 = uv * vec2(220.0, 120.0);
	float s1 = step(0.996, h21(floor(g1))) * smoothstep(0.24, 0.0, length(fract(g1) - 0.5));
	col += vec3(0.7, 0.65, 0.8) * s1 * (1.0 - smoke * 0.8);
	// drifting embers rising slowly all around the planet
	vec2 g2 = vec2(uv.x * 90.0, uv.y * 50.0 - TIME * 0.06);
	float eh = h21(floor(g2));
	float ember = step(0.988, eh) * smoothstep(0.34, 0.0, length(fract(g2) - 0.5));
	float pulse = 0.55 + 0.45 * sin(TIME * 3.0 + eh * 40.0);
	col += vec3(1.0, 0.42, 0.10) * ember * pulse * 0.8;
	// a distant angry red vortex — the storm that keeps this world alone
	vec2 gc = (uv - vec2(0.26, 0.60)) * vec2(2.2, 3.8);
	float r = length(gc);
	float ang = atan(gc.y, gc.x);
	float arm = 0.5 + 0.5 * cos(ang * 3.0 - r * 8.0 + TIME * 0.03);
	col += vec3(0.55, 0.10, 0.06) * exp(-r * 3.4) * (0.3 + 0.7 * arm);
	ALBEDO = col;
	EMISSION = col * 0.8;
}"""
	var smat := ShaderMaterial.new()
	smat.shader = sh
	sky.material_override = smat
	sky.position = ORIGIN
	add_child(sky)

# ---------------------------------------------------------------- planet

func _build_planet() -> void:
	var planet := MeshInstance3D.new()
	var pm := SphereMesh.new()
	pm.radius = PLANET_R
	pm.height = PLANET_R * 2.0
	pm.radial_segments = 96
	pm.rings = 48
	planet.mesh = pm
	var sh := Shader.new()
	sh.code = """shader_type spatial;
// basalt fortress-planet: painted cliff sheets sampled model-space triplanar
// (no pole pinch), cut by two glowing lava rivers circling the world. The
// lava writes EMISSION so the low bloom threshold makes it bleed light.
uniform sampler2D rock_tex : source_color, repeat_enable, filter_linear_mipmap;
uniform sampler2D cobble_tex : source_color, repeat_enable, filter_linear_mipmap;
varying vec3 mpos;
varying vec3 mnrm;
float h21(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5); }
vec3 triplanar(sampler2D t, vec3 p, vec3 n, float s){
	vec3 w = abs(n); w /= (w.x + w.y + w.z);
	return texture(t, p.yz * s).rgb * w.x + texture(t, p.xz * s).rgb * w.y
			+ texture(t, p.xy * s).rgb * w.z;
}
void fragment(){
	// dark toy-basalt with faint warm banding
	float band = sin(UV.y * 11.0) * 0.5 + 0.5;
	vec3 rock = triplanar(rock_tex, mpos, mnrm, 0.05);
	vec3 col = rock * mix(vec3(0.26, 0.20, 0.24), vec3(0.36, 0.26, 0.26), band);
	// a cobbled parade path ring near the fortress pole
	float polar = UV.y;
	float parade = exp(-pow((polar - 0.16) * 26.0, 2.0));
	vec3 cob = triplanar(cobble_tex, mpos, mnrm, 0.07) * vec3(0.5, 0.42, 0.44);
	col = mix(col, cob, clamp(parade, 0.0, 1.0) * 0.85);
	// two glowing lava rivers circling the planet (mirrored by _lava_mix)
	float wob = sin(UV.x * 12.566) * 0.03;
	float lava1 = exp(-pow((UV.y - 0.42 + wob) * 30.0, 2.0));
	float lava2 = exp(-pow((UV.y - 0.62 - wob) * 30.0, 2.0));
	float lava = clamp(lava1 + lava2, 0.0, 1.0);
	float flow = 0.75 + 0.25 * sin(UV.x * 40.0 + TIME * 1.6);
	vec3 lcol = mix(vec3(1.0, 0.36, 0.08), vec3(1.0, 0.78, 0.25), flow * lava);
	col = mix(col, lcol, lava);
	// scattered cooling embers on the dark rock
	vec2 g = UV * vec2(200.0, 110.0);
	float eh = h21(floor(g));
	float fleck = step(0.99, eh) * smoothstep(0.3, 0.05, length(fract(g) - 0.5));
	float pulse = 0.5 + 0.5 * sin(TIME * 2.4 + eh * 50.0);
	ALBEDO = col;
	EMISSION = lcol * lava * (0.9 + 0.3 * flow) + vec3(1.0, 0.45, 0.12) * fleck * pulse * (1.0 - lava) * 0.7;
	ROUGHNESS = 0.9;
}"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("rock_tex", load("res://assets/terrain/up_cliff_col.jpg"))
	mat.set_shader_parameter("cobble_tex", load("res://assets/terrain/up_cobble_col.jpg"))
	planet.material_override = mat
	planet.position = ORIGIN
	add_child(planet)
	# heat-haze atmosphere: a faint warm fresnel shell
	var atmo := MeshInstance3D.new()
	var am := SphereMesh.new()
	am.radius = PLANET_R * 1.06
	am.height = PLANET_R * 2.12
	atmo.mesh = am
	var ash := Shader.new()
	ash.code = """shader_type spatial;
render_mode unshaded, blend_add, cull_back;
void fragment(){
	float f = pow(1.0 - clamp(dot(normalize(NORMAL), normalize(VIEW)), 0.0, 1.0), 2.5);
	ALBEDO = vec3(1.0, 0.30, 0.10) * f * 0.45;
	ALPHA = f * 0.45;
}"""
	var amat := ShaderMaterial.new()
	amat.shader = ash
	atmo.material_override = amat
	atmo.position = ORIGIN
	add_child(atmo)

func _surf(dir: Vector3, h: float = 0.0) -> Vector3:
	return ORIGIN + dir.normalized() * (PLANET_R + h)

func _lava_mix(dir: Vector3) -> float:
	# Mirrors the two lava rivers in _build_planet's shader so gameplay (the
	# harmless hot-foot hop) and placement agree with the visuals.
	var d: Vector3 = dir.normalized()
	var u: float = fposmod(atan2(d.x, d.z) / TAU, 1.0)
	var v: float = acos(clampf(d.y, -1.0, 1.0)) / PI
	var wob: float = sin(u * 12.566) * 0.03
	return clampf(exp(-pow((v - 0.42 + wob) * 30.0, 2.0))
		+ exp(-pow((v - 0.62 - wob) * 30.0, 2.0)), 0.0, 1.0)

func _safe_look(n: Node3D, dir: Vector3, up: Vector3) -> void:
	# look_at() hardened for the y=15000 world offset (same reasoning as
	# galaxy.gd: relative epsilon + colinear up would error out here)
	if dir.length_squared() < 0.000004:
		return
	var d: Vector3 = dir.normalized()
	var u: Vector3 = up.normalized()
	if absf(d.dot(u)) > 0.99:
		u = Vector3.BACK if absf(d.dot(Vector3.BACK)) < 0.99 else Vector3.RIGHT
	n.look_at(n.global_position + d * 2.0, u)

func _place_on_planet(node: Node3D, dir: Vector3, h: float = 0.0) -> void:
	var d := dir.normalized()
	node.position = _surf(d, h)
	var up := d
	var any := Vector3.UP if absf(up.dot(Vector3.UP)) < 0.95 else Vector3.RIGHT
	var t := any.cross(up).normalized()
	node.transform.basis = Basis(t, up, t.cross(up).normalized() * -1.0).orthonormalized()

func _gather_aabbs(n: Node, xf: Transform3D, acc: Array) -> void:
	if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
		acc.append(xf * (n as MeshInstance3D).get_aabb())
	for c in n.get_children():
		if c is Node3D:
			_gather_aabbs(c, xf * (c as Node3D).transform, acc)
		else:
			_gather_aabbs(c, xf, acc)

func _fit_small(model: Node3D, target_long: float) -> float:
	# normalise a GLB to a footprint. Deliberately NOT _toonify'd: the pastel
	# pass lifts blacks (+0.16 value floor) and this world's soul is dark
	# stone — props get the obsidian restyle from _dark_stone instead.
	var acc: Array = []
	_gather_aabbs(model, Transform3D.IDENTITY, acc)
	if acc.is_empty():
		return 0.0
	var bb: AABB = acc[0]
	for i in range(1, acc.size()):
		bb = bb.merge(acc[i])
	var longest: float = maxf(maxf(bb.size.x, bb.size.z), maxf(bb.size.y, 0.001))
	var sc: float = target_long / longest
	model.scale = Vector3.ONE * sc
	var c: Vector3 = bb.position + bb.size * 0.5
	model.position = Vector3(-c.x * sc, -bb.position.y * sc, -c.z * sc)
	return bb.size.y * sc

func _dark_stone(root: Node, tint: Color, glow: Color = Color.BLACK, glow_e: float = 0.0) -> void:
	# the obsidian restyle: flatten imported materials toward dark toy-stone,
	# with an optional ember glow. Per-surface duplicates are safe here — the
	# whole subtree is freed together at _teardown (same idiom as
	# galaxy.gd's _tint_meshes).
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
				m.normal_enabled = false
				m.roughness = 1.0
				m.metallic = 0.0
				m.albedo_color = m.albedo_color.lerp(tint, 0.72)
				if glow_e > 0.0:
					m.emission_enabled = true
					m.emission = glow
					m.emission_energy_multiplier = glow_e
				mi.set_surface_override_material(si, m)

func _authored_prop(path: String, parent: Node3D, pos: Vector3, target_long: float, yaw: float = 0.0) -> Node3D:
	if not ResourceLoader.exists(path):
		return null
	var packed: PackedScene = load(path) as PackedScene
	if packed == null:
		return null
	var holder := Node3D.new()
	var model: Node3D = packed.instantiate() as Node3D
	if model == null:
		holder.free()
		return null
	holder.add_child(model)
	parent.add_child(holder)
	_fit_small(model, target_long)
	holder.position = pos
	holder.rotation.y = yaw
	return holder

# ---------------------------------------------------------------- fortress

func _build_fortress() -> void:
	# The north-pole citadel: a ring of obsidian towers and battlement walls
	# around the GREAT GATE — deliberately oversized, a monument that makes
	# every visitor feel small (and a four-year-old feel giddy).
	var fort := Node3D.new()
	add_child(fort)
	_place_on_planet(fort, Vector3.UP)
	# sink the ring base below the tangent plane so wall corners don't hover
	fort.position = _surf(Vector3.UP, -1.5)
	_blockers.append({"dir": Vector3.UP, "r": 8.5, "cool": 0.0})
	var obsidian := Color(0.16, 0.11, 0.16)
	var rampart := Color(0.22, 0.15, 0.18)
	for i in range(4):
		var ta: float = float(i) / 4.0 * TAU + TAU * 0.125
		var tower: Node3D = _authored_prop(TOWER_GLB, fort, Vector3(sin(ta) * 8.0, 0.0, cos(ta) * 8.0), 4.2, -ta)
		if tower != null:
			_dark_stone(tower, obsidian)
		var flag: Node3D = _authored_prop(FLAG_GLB, fort, Vector3(sin(ta) * 8.0, 6.4, cos(ta) * 8.0), 2.4, -ta)
		if flag != null:
			_dark_stone(flag, Color(0.62, 0.14, 0.10), Color(0.9, 0.2, 0.1), 0.35)
			_flags.append(flag)
	for i in range(4):
		var wa: float = float(i) / 4.0 * TAU
		if i == 0:
			continue   # the south face is the Great Gate's wall
		var wall: Node3D = _authored_prop(WALL_GLB, fort, Vector3(sin(wa) * 8.0, 0.0, cos(wa) * 8.0), 5.6, -wa)
		if wall != null:
			_dark_stone(wall, rampart)
	# THE GREAT GATE — the authored ten-pearl undercroft gate, giant-sized,
	# facing down the parade path. Its veil drops when the 5 lanterns burn.
	var gh := Node3D.new()
	add_child(gh)
	_place_on_planet(gh, GATE_DIR.normalized())
	_gate_node = _authored_prop(GATE_GLB, gh, Vector3.ZERO, 9.0)
	if _gate_node != null:
		_dark_stone(_gate_node, Color(0.20, 0.13, 0.15), EMBER_COL, 0.18)
	_blockers.append({"dir": GATE_DIR.normalized(), "r": 2.6, "cool": 0.0})
	# the veil: a glowing ember curtain filling the arch while the gate is shut
	_gate_veil = MeshInstance3D.new()
	var vq := QuadMesh.new()
	vq.size = Vector2(5.2, 6.4)
	_gate_veil.mesh = vq
	var vmat := StandardMaterial3D.new()
	vmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	vmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	vmat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	vmat.albedo_color = Color(1.0, 0.32, 0.10, 0.5)
	vmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	_gate_veil.material_override = vmat
	_gate_veil.position = Vector3(0, 3.4, 0.6)
	gh.add_child(_gate_veil)
	# two dragon-turtle sentries flank the gate
	for s in [-1.0, 1.0]:
		var sentry: Node3D = _authored_prop(STATUE_GLB, gh, Vector3(4.6 * s, 0.0, 1.2), 3.4, PI)
		if sentry != null:
			_dark_stone(sentry, Color(0.24, 0.17, 0.19), EMBER_COL, 0.10)
	# THE EMBER KING himself: the great dragon-turtle perched above his gate,
	# huge and theatrical — all growl, zero bite
	var kh := Node3D.new()
	add_child(kh)
	_place_on_planet(kh, KING_DIR.normalized())
	_king = _authored_prop(DRAGON_GLB, kh, Vector3(0, 4.6, 0), 7.5, PI)
	if _king != null:
		_dark_stone(_king, Color(0.30, 0.14, 0.12), Color(1.0, 0.3, 0.1), 0.35)
	var kl := OmniLight3D.new()
	kl.light_color = Color(1.0, 0.42, 0.16)
	kl.light_energy = 2.2
	kl.omni_range = 26.0
	kl.position = Vector3(0, 7.0, 0)
	kh.add_child(kl)

# ---------------------------------------------------------------- objective

func _build_lanterns() -> void:
	var done: bool = _main != null and "ember_done" in _main and bool(_main.ember_done)
	for i in range(LANTERNS):
		var ldir: Vector3 = (LANTERN_DIRS[i] as Vector3).normalized()
		# lit lanterns persist through hidden sticker keys, exactly like the
		# galaxy's rescued butterflies — a save-schema-free checkpoint
		var lit: bool = done or (_main != null and "stickers" in _main and bool(_main.stickers.get("_ember_lantern_%d" % i, false)))
		var lh := Node3D.new()
		add_child(lh)
		_place_on_planet(lh, ldir)
		_blockers.append({"dir": ldir, "r": 1.3, "cool": 0.0})
		var lant: Node3D = _authored_prop(LANTERN_GLB, lh, Vector3.ZERO, 3.2)
		if lant != null:
			_dark_stone(lant, Color(0.26, 0.18, 0.18))
		# the flame orb above the lantern: grey ash when cold, blazing when lit
		var flame := MeshInstance3D.new()
		var fm := SphereMesh.new()
		fm.radius = 0.7
		fm.height = 1.4
		flame.mesh = fm
		var fmat := StandardMaterial3D.new()
		fmat.albedo_color = Color(0.35, 0.32, 0.34)
		flame.material_override = fmat
		flame.position = Vector3(0, 4.0, 0)
		lh.add_child(flame)
		var ll := OmniLight3D.new()
		ll.light_color = EMBER_COL
		ll.light_energy = 0.0
		ll.omni_range = 15.0
		ll.position = Vector3(0, 4.4, 0)
		lh.add_child(ll)
		# BEACON: a tall additive pillar so far lanterns show over the horizon
		var beam := MeshInstance3D.new()
		var bc := CylinderMesh.new()
		bc.top_radius = 0.4
		bc.bottom_radius = 1.4
		bc.height = 32.0
		bc.radial_segments = 8
		beam.mesh = bc
		var bmt := StandardMaterial3D.new()
		bmt.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		bmt.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		bmt.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		bmt.albedo_color = Color(1.0, 0.35, 0.12, 0.30)
		beam.material_override = bmt
		beam.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		var bup := ldir
		var bany := Vector3.UP if absf(bup.dot(Vector3.UP)) < 0.95 else Vector3.RIGHT
		var bt := bany.cross(bup).normalized()
		beam.transform.basis = Basis(bt, bup, bt.cross(bup).normalized() * -1.0).orthonormalized()
		beam.position = _surf(ldir, 18.0)
		add_child(beam)
		var entry := {"node": lh, "dir": ldir, "lit": false, "flame": flame, "beam": beam, "light": ll, "idx": i}
		_lanterns.append(entry)
		if lit:
			_apply_lantern_lit(entry)
			_lit += 1
	if _lit >= LANTERNS:
		_set_gate_open(true, false)

func _apply_lantern_lit(entry: Dictionary) -> void:
	entry["lit"] = true
	var flame: MeshInstance3D = entry["flame"]
	var fmat := StandardMaterial3D.new()
	fmat.albedo_color = Color(1.0, 0.66, 0.24)
	fmat.emission_enabled = true
	fmat.emission = EMBER_COL
	fmat.emission_energy_multiplier = 2.2
	flame.material_override = fmat
	(entry["light"] as OmniLight3D).light_energy = 1.6
	if entry.get("beam") != null and is_instance_valid(entry["beam"]):
		(entry["beam"] as Node3D).visible = false

func _light_lantern(idx: int) -> void:
	# Deterministic single entry point for lighting lantern `idx`: gameplay
	# proximity and the headless probe both land here.
	if idx < 0 or idx >= _lanterns.size():
		return
	var entry: Dictionary = _lanterns[idx]
	if bool(entry["lit"]):
		return
	_apply_lantern_lit(entry)
	_lit += 1
	if _main != null and "stickers" in _main:
		_main.stickers["_ember_lantern_%d" % idx] = true
		if _main.has_method("_write_save"):
			_main._write_save()
	_update_lantern_hud()
	_chime(0.6 + 0.09 * float(_lit))
	if _main != null and _main.has_method("_sparkle_burst"):
		_main._sparkle_burst(_surf(entry["dir"], 4.0), EMBER_COL)
	if _lit == LANTERNS - 1:
		for other in _lanterns:
			if not bool(other["lit"]) and other.get("beam") != null and is_instance_valid(other["beam"]):
				(other["beam"] as Node3D).scale = Vector3(3.0, 2.0, 3.0)
				var bmm: StandardMaterial3D = (other["beam"] as MeshInstance3D).material_override
				if bmm != null:
					bmm.albedo_color.a = 0.55
		if _lbl_hint != null:
			_lbl_hint.text = "ONE lantern left — follow the GIANT red beacon!"
	if _lit >= LANTERNS:
		_set_gate_open(true, true)

func _set_gate_open(is_open: bool, celebrate: bool) -> void:
	_gate_open = is_open
	if _gate_veil != null and is_instance_valid(_gate_veil):
		_gate_veil.visible = not is_open
	if not is_open or not celebrate:
		return
	_gate_cool = 3.0
	_chime(1.35)
	if _lbl_hint != null:
		_lbl_hint.text = "ALL 5 lanterns! The GREAT GATE is open — walk in when you feel brave!"
	if _main != null and _main.has_method("_sparkle_burst"):
		_main._sparkle_burst(_surf(GATE_DIR.normalized(), 5.0), Color(1.0, 0.8, 0.3))
	if _main != null and _main.has_method("show_msg"):
		_main.show_msg("Ember King", "WHAT?! All five lanterns?! Fine, little mermaid... my GATE IS OPEN. Come and try my fortress dungeon!", "talk")

# ---------------------------------------------------------------- decor

func _build_decor() -> void:
	# jagged obsidian crags — the volcanic body the fortress was wrapped around
	for i in range(14):
		var rdir := Vector3(sin(float(i) * 2.4) * cos(float(i) * 0.83), sin(float(i) * 0.9) * 0.8,
			cos(float(i) * 2.4) * cos(float(i) * 0.83)).normalized()
		if _lava_mix(rdir) > 0.25 or rdir.angle_to(Vector3.UP) < 0.5:
			continue   # keep the rivers and the citadel hill clear
		var rh := Node3D.new()
		add_child(rh)
		_place_on_planet(rh, rdir)
		var rock: Node3D = _authored_prop(ROCKS[i % ROCKS.size()], rh, Vector3.ZERO, 2.6 + fposmod(float(i) * 1.7, 2.6))
		if rock == null:
			rh.queue_free()
			continue
		_dark_stone(rock, Color(0.20, 0.15, 0.19))
		rh.rotate(rdir, fposmod(float(i) * 2.1, TAU))
		if i % 3 == 0:
			_blockers.append({"dir": rdir, "r": 1.5, "cool": 0.0})
	# fire crystals: the King's power source, humming with heat
	for i in range(4):
		var cdir := Vector3(sin(float(i) * 1.7 + 0.8), cos(float(i) * 1.2) * 0.6, cos(float(i) * 1.7 - 0.4)).normalized()
		if _lava_mix(cdir) > 0.25:
			continue
		var ch := Node3D.new()
		add_child(ch)
		_place_on_planet(ch, cdir)
		var crystal: Node3D = _authored_prop(CRYSTALS[i % CRYSTALS.size()], ch, Vector3.ZERO, 3.0)
		if crystal == null:
			ch.queue_free()
			continue
		_dark_stone(crystal, Color(0.5, 0.12, 0.10), Color(1.0, 0.25, 0.10), 0.8)
		_blockers.append({"dir": cdir, "r": 1.4, "cool": 0.0})
	# LAVA GEYSERS on the rivers: step on one and WHOOSH — a friendly launch
	for vdir_raw in VENT_DIRS:
		var vdir: Vector3 = (vdir_raw as Vector3).normalized()
		var pad := MeshInstance3D.new()
		var ptm := TorusMesh.new()
		ptm.inner_radius = 1.8
		ptm.outer_radius = 3.0
		pad.mesh = ptm
		var pmat := StandardMaterial3D.new()
		pmat.albedo_color = Color(1.0, 0.5, 0.2)
		pmat.emission_enabled = true
		pmat.emission = LAVA_COL
		pmat.emission_energy_multiplier = 1.8
		pad.material_override = pmat
		var holder := Node3D.new()
		add_child(holder)
		holder.add_child(pad)
		pad.position = Vector3(0, 0.5, 0)
		_place_on_planet(holder, vdir)
		_vents.append({"dir": vdir, "cool": 0.0})
	# one cracked ash moon keeps lonely watch
	_moon = MeshInstance3D.new()
	var mm := SphereMesh.new()
	mm.radius = 5.0
	mm.height = 10.0
	(_moon as MeshInstance3D).mesh = mm
	var mmat := StandardMaterial3D.new()
	mmat.albedo_color = Color(0.30, 0.24, 0.26)
	mmat.emission_enabled = true
	mmat.emission = Color(0.6, 0.25, 0.15)
	mmat.emission_energy_multiplier = 0.25
	(_moon as MeshInstance3D).material_override = mmat
	add_child(_moon)
	# rising spark motes all around the planet
	var sparks := CPUParticles3D.new()
	sparks.amount = 50
	sparks.lifetime = 9.0
	sparks.emission_shape = CPUParticles3D.EMISSION_SHAPE_SPHERE
	sparks.emission_sphere_radius = PLANET_R * 1.8
	sparks.gravity = Vector3.ZERO
	sparks.initial_velocity_min = 0.4
	sparks.initial_velocity_max = 1.4
	sparks.scale_amount_min = 0.08
	sparks.scale_amount_max = 0.3
	var sm2 := SphereMesh.new()
	sm2.radius = 0.35
	sm2.height = 0.7
	sparks.mesh = sm2
	var smt := StandardMaterial3D.new()
	smt.albedo_color = Color(1.0, 0.5, 0.2)
	smt.emission_enabled = true
	smt.emission = EMBER_COL
	smt.emission_energy_multiplier = 1.6
	smt.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	sparks.mesh.material = smt
	sparks.position = ORIGIN
	add_child(sparks)

var _home_pos := Vector3.ZERO

func _build_home_ring() -> void:
	# the friendly way home at the south pole — the one rainbow-bright thing
	# on the whole dark planet, unmissable and always available
	_home_pos = _surf(Vector3.DOWN, 4.0)
	var ring := MeshInstance3D.new()
	var tm := TorusMesh.new()
	tm.inner_radius = 2.4
	tm.outer_radius = 3.4
	ring.mesh = tm
	if _main != null and _main.has_method("_rainbow_mat"):
		ring.material_override = _main._rainbow_mat()
	var holder := Node3D.new()
	add_child(holder)
	holder.add_child(ring)
	ring.position = Vector3(0, 3.2, 0)
	ring.rotation_degrees = Vector3(90, 0, 0)
	_place_on_planet(holder, Vector3.DOWN)

# ---------------------------------------------------------------- avatar

var _av_skel: Skeleton3D = null
var _av_bones := {}
var _av_rest := {}
var _av_run := 0.0

func _build_avatar() -> void:
	# same wardrobe-aware avatar as GalaxyLevel: v4/v3 mermaid GLB, the huluu
	# cutout, or the fairy skin — whatever Roshan is wearing travels here too
	_avatar = Node3D.new()
	add_child(_avatar)
	var glb := "res://assets/characters/roshan.glb"
	var cutout: Sprite3D = null
	for vpath in ["res://assets/characters/roshan_v4.glb",
			"res://assets/characters/roshan_v3.glb"]:
		if ResourceLoader.exists(vpath):
			glb = vpath
			break
	if _main != null and "skin_id" in _main:
		var sid := String(_main.skin_id)
		if sid == "huluu":
			glb = ""
			cutout = Sprite3D.new()
			cutout.texture = load("res://assets/characters/friends/huluu.png")
			cutout.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			cutout.pixel_size = 0.011
			cutout.position = Vector3(0, 2.2, 0)
		elif sid == "fairy" and ResourceLoader.exists("res://assets/characters/fairy_v2.glb"):
			glb = "res://assets/characters/fairy_v2.glb"
	if cutout != null:
		_avatar.add_child(cutout)
	if glb != "" and ResourceLoader.exists(glb):
		var inst: Node3D = (load(glb) as PackedScene).instantiate()
		var acc: Array = []
		_gather_aabbs(inst, Transform3D.IDENTITY, acc)
		if acc.size() > 0:
			var bb: AABB = acc[0]
			for k in range(1, acc.size()):
				bb = bb.merge(acc[k])
			var sc: float = 4.2 / maxf(bb.size.y, 0.001)
			inst.scale = Vector3.ONE * sc
			inst.position = Vector3(0, -bb.position.y * sc, 0)
		_avatar.add_child(inst)
		_av_skel = _find_av_skel(inst)
		_av_bones.clear()
		_av_rest.clear()
		if _av_skel != null:
			for bn: String in ["spine1", "chest", "neck", "head", "hair1", "hair2", "hair3",
					"tail1", "tail2", "tail3", "tail4", "tail5", "tail6", "tail7", "tail8"]:
				var bi := _av_skel.find_bone(bn)
				if bi >= 0:
					_av_bones[bn] = bi
					_av_rest[bi] = _av_skel.get_bone_pose_rotation(bi)
	var trail := OmniLight3D.new()
	trail.light_color = Color(0.6, 0.85, 1.0)   # Roshan's cool glow vs the warm world
	trail.light_energy = 1.6
	trail.omni_range = 10.0
	trail.position = Vector3(0, 2.0, 0)
	_avatar.add_child(trail)
	_dir = Vector3(0, -0.2, 1).normalized()
	_fwd = Vector3(1, 0, 0)
	_project_fwd()
	_update_avatar_transform()

func _find_av_skel(n: Node) -> Skeleton3D:
	if n is Skeleton3D:
		return n
	for c in n.get_children():
		var r := _find_av_skel(c)
		if r != null:
			return r
	return null

func _av_rot(bi: int, axis: Vector3, ang: float) -> void:
	var rq: Quaternion = _av_rest.get(bi, Quaternion.IDENTITY)
	_av_skel.set_bone_pose_rotation(bi, rq * Quaternion((rq.inverse() * axis).normalized(), ang))

func _animate_avatar(delta: float, moving: float) -> void:
	if _av_skel == null:
		return
	_av_run += delta * (2.4 + moving * 4.2)
	var amp: float = 0.10 + moving * 0.17
	for i in range(8):
		var bi: int = int(_av_bones.get("tail%d" % (i + 1), -1))
		if bi >= 0:
			_av_rot(bi, Vector3(1, 0, 0), sin(_av_run - float(i) * 0.55) * amp * (0.55 + float(i) * 0.11))
	for hi in range(3):
		var hb: int = int(_av_bones.get("hair%d" % (hi + 1), -1))
		if hb >= 0:
			_av_rot(hb, Vector3(0, 0, 1), sin(_av_run * 0.8 - float(hi) * 0.7) * 0.12)
	var head: int = int(_av_bones.get("head", -1))
	if head >= 0:
		_av_rot(head, Vector3(1, 0, 0), sin(_av_run * 0.5) * 0.06)
	var chest: int = int(_av_bones.get("chest", -1))
	if chest >= 0:
		_av_rot(chest, Vector3(0, 1, 0), sin(_av_run * 0.7) * 0.05 * (0.4 + moving))

func _project_fwd() -> void:
	_fwd = (_fwd - _dir * _fwd.dot(_dir))
	if _fwd.length() < 0.001:
		_fwd = _dir.cross(Vector3.RIGHT)
		if _fwd.length() < 0.001:
			_fwd = _dir.cross(Vector3.FORWARD)
	_fwd = _fwd.normalized()

func _update_avatar_transform() -> void:
	if _avatar == null:
		return
	_avatar.position = _surf(_dir, _h + sin(_bob_t * 3.0) * 0.12)
	var up := _dir
	var right := _fwd.cross(up).normalized()
	_avatar.transform.basis = Basis(right, up, -_fwd).orthonormalized()

# ---------------------------------------------------------------- camera & HUD

func _build_camera() -> void:
	_cam = Camera3D.new()
	_cam.fov = 70.0
	_cam.far = 2500.0
	add_child(_cam)
	_cam.make_current()
	_cam.position = _surf(_dir, 8.0) - _fwd * 12.0
	_cam.look_at(_surf(_dir, 2.0), _dir)

func _cam_peek(delta: float) -> void:
	var mdx: float = _mlook_dx
	var mdy: float = _mlook_dy
	_mlook_dx = 0.0
	_mlook_dy = 0.0
	var rx: float = joy_axis(JOY_AXIS_RIGHT_X)
	var ry: float = joy_axis(JOY_AXIS_RIGHT_Y)
	var mlook: bool = Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT)
	if _main != null and "touch_ui" in _main and _main.touch_ui != null and _main.touch_ui.has_method("consume_look"):
		var tl: Vector2 = _main.touch_ui.consume_look()
		mdx += tl.x
		mdy += tl.y
		mlook = mlook or bool(_main.touch_ui.look_active())
	if absf(rx) > 0.25:
		_cam_orbit = clampf(_cam_orbit - rx * 2.6 * delta, -PI * 0.9, PI * 0.9)
	elif mlook:
		_cam_orbit = clampf(_cam_orbit - mdx * 0.005, -PI * 0.9, PI * 0.9)
	else:
		_cam_orbit = lerpf(_cam_orbit, 0.0, 1.0 - pow(0.35, delta))
	if absf(ry) > 0.25:
		_cam_pitch = clampf(_cam_pitch + ry * 9.0 * delta, -4.0, 7.0)
	elif mlook:
		_cam_pitch = clampf(_cam_pitch + mdy * 0.02, -4.0, 7.0)
	else:
		_cam_pitch = lerpf(_cam_pitch, 0.0, 1.0 - pow(0.35, delta))

func _build_hud() -> void:
	_hud = CanvasLayer.new()
	_hud.layer = 18
	add_child(_hud)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	# display only — a full-rect STOP control would swallow the touch stick
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hud.add_child(root)
	_lbl_lanterns = Label.new()
	_lbl_lanterns.position = Vector2(24, 18)
	_lbl_lanterns.add_theme_font_size_override("font_size", 40)
	_lbl_lanterns.add_theme_color_override("font_color", Color(1.0, 0.72, 0.4))
	_lbl_lanterns.add_theme_color_override("font_outline_color", Color(0.14, 0.05, 0.06))
	_lbl_lanterns.add_theme_constant_override("outline_size", 6)
	root.add_child(_lbl_lanterns)
	_lbl_big = Label.new()
	_lbl_big.set_anchors_preset(Control.PRESET_FULL_RECT)
	_lbl_big.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_lbl_big.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_lbl_big.add_theme_font_size_override("font_size", 84)
	_lbl_big.add_theme_color_override("font_color", Color(1, 1, 1))
	_lbl_big.add_theme_color_override("font_outline_color", Color(0.18, 0.03, 0.03))
	_lbl_big.add_theme_constant_override("outline_size", 12)
	root.add_child(_lbl_big)
	_lbl_hint = Label.new()
	_lbl_hint.anchor_top = 1.0
	_lbl_hint.anchor_bottom = 1.0
	_lbl_hint.position = Vector2(24, -56)
	_lbl_hint.add_theme_font_size_override("font_size", 26)
	_lbl_hint.add_theme_color_override("font_color", Color(1.0, 0.9, 0.82))
	_lbl_hint.add_theme_color_override("font_outline_color", Color(0.14, 0.05, 0.06))
	_lbl_hint.add_theme_constant_override("outline_size", 5)
	root.add_child(_lbl_hint)
	_update_lantern_hud()

func _update_lantern_hud() -> void:
	_lbl_lanterns.text = "🔥 %d / %d" % [_lit, LANTERNS]

# ---------------------------------------------------------------- input

func _move_input() -> Vector2:
	var v := Vector2.ZERO
	if Input.is_physical_key_pressed(KEY_UP) or Input.is_physical_key_pressed(KEY_W):
		v.y += 1.0
	if Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S):
		v.y -= 0.6
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		v.x -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		v.x += 1.0
	var jx: float = joy_axis(JOY_AXIS_LEFT_X)
	var jy: float = joy_axis(JOY_AXIS_LEFT_Y)
	if absf(jx) > 0.2:
		v.x += jx
	if absf(jy) > 0.2:
		v.y -= jy
	if joy_pressed(JOY_BUTTON_DPAD_UP):
		v.y += 1.0
	if joy_pressed(JOY_BUTTON_DPAD_DOWN):
		v.y -= 0.6
	if joy_pressed(JOY_BUTTON_DPAD_LEFT):
		v.x -= 1.0
	if joy_pressed(JOY_BUTTON_DPAD_RIGHT):
		v.x += 1.0
	if _main != null and "touch_ui" in _main and _main.touch_ui != null:
		var tv: Vector2 = _main.touch_ui.stick_vec
		if absf(tv.x) > 0.15:
			v.x += tv.x
		if absf(tv.y) > 0.15:
			v.y -= tv.y
	v.x = clampf(v.x, -1.0, 1.0)
	v.y = clampf(v.y, -0.6, 1.0)
	return v

func _jump_pressed() -> bool:
	var now := Input.is_physical_key_pressed(KEY_SPACE) or joy_pressed(JOY_BUTTON_A) or joy_pressed(JOY_BUTTON_B)
	var just := now and not _fire_prev
	_fire_prev = now
	if not just and _main != null and "touch_ui" in _main and _main.touch_ui != null:
		if _main.touch_ui.action_down and _h <= 0.05:
			just = true
	return just

# ---------------------------------------------------------------- per-frame

func _process(delta: float) -> void:
	if _state == "done":
		return
	_bob_t += delta
	var tt: float = Time.get_ticks_msec() / 1000.0
	# the ash moon on its lonely orbit
	if _moon != null:
		var ph: float = tt * 0.12
		_moon.position = ORIGIN + Vector3(cos(ph) * PLANET_R * 2.2, sin(ph * 0.7) * PLANET_R * 0.5, sin(ph) * PLANET_R * 2.2)
	# battlement banners ripple; lit lantern flames flicker
	for i in range(_flags.size()):
		var flag: Node3D = _flags[i]
		if is_instance_valid(flag):
			flag.rotation.z = sin(tt * 2.2 + float(i) * 1.7) * 0.08
	for ld in _lanterns:
		if bool(ld["lit"]):
			var flame: Node3D = ld["flame"]
			flame.scale = Vector3.ONE * (1.0 + 0.14 * sin(tt * 9.0 + float(ld["idx"]) * 2.0))
	# the Ember King sways and grumbles a greeting when Roshan comes close
	if _king != null and is_instance_valid(_king):
		_king.rotation.z = sin(tt * 0.9) * 0.05
		_king_cool = maxf(0.0, _king_cool - delta)
		if _king_cool <= 0.0 and _surf(KING_DIR.normalized(), 4.0).distance_to(_surf(_dir, _h)) < 14.0:
			_king_cool = 18.0
			_chime(0.5)
			if _main != null and _main.has_method("show_msg"):
				if "ember_done" in _main and bool(_main.ember_done):
					_main.show_msg("Ember King", "My little hero friend! Play in my fortress as long as you like!", "greet")
				elif _gate_open:
					_main.show_msg("Ember King", "Grrr... the gate is open. Show me how brave you are, tiny mermaid!", "talk")
				else:
					_main.show_msg("Ember King", "RRRUMBLE! Light all five of my lanterns first, little one!", "talk")
	_animate_avatar(delta, _last_move)
	# ---- movement on the sphere ----
	var mv := _move_input()
	if absf(mv.x) > 0.01:
		_fwd = _fwd.rotated(_dir, -mv.x * TURN_SPD * delta)
		_project_fwd()
	if absf(mv.y) > 0.01:
		var step: float = mv.y * RUN_SPD * delta / PLANET_R
		_dir = (_dir.rotated(_fwd.cross(_dir).normalized(), -step)).normalized()
		_project_fwd()
	_last_move = minf(1.0, absf(mv.y) + absf(mv.x) * 0.4)
	# soft collision with towers, crags and crystals (jump clears them)
	if _h < 4.0:
		for b in _blockers:
			var bdir: Vector3 = b["dir"]
			var min_ang: float = float(b["r"]) / PLANET_R
			var bang: float = _dir.angle_to(bdir)
			if bang < min_ang and bang > 0.0005:
				var pax: Vector3 = bdir.cross(_dir)
				if pax.length() > 0.0005:
					_dir = bdir.rotated(pax.normalized(), min_ang).normalized()
					_project_fwd()
					b["cool"] = float(b.get("cool", 0.0)) - delta
					if float(b["cool"]) <= 0.0:
						b["cool"] = 0.6
						_chime(0.7 + fposmod(bdir.x * 7.0, 0.4))
						if _main != null and _main.has_method("_sparkle_burst"):
							_main._sparkle_burst(_surf(bdir, 3.0), Color(1.0, 0.5, 0.3))
	# lava geysers: step on one and WHOOSH
	for vd in _vents:
		vd["cool"] = maxf(0.0, float(vd["cool"]) - delta)
		if _h < 0.6 and float(vd["cool"]) <= 0.0:
			var vang: float = _dir.angle_to(vd["dir"]) * PLANET_R
			if vang < 3.2:
				vd["cool"] = 1.0
				_sizzle_cool = maxf(_sizzle_cool, 0.8)
				_vy = JUMP_V * 1.9
				_h = maxf(_h, 0.06)
				_chime(1.3)
				if _main != null and _main.has_method("_sparkle_burst"):
					_main._sparkle_burst(_surf(_dir, 2.0), Color(1.0, 0.6, 0.2))
	# the lava rivers are warm, not dangerous: a hot-foot hop and a giggle,
	# never harm — the "scary" world keeps the whole game's no-fail promise
	_sizzle_cool = maxf(0.0, _sizzle_cool - delta)
	_sizzle_say = maxf(0.0, _sizzle_say - delta)
	if _h <= 0.05 and _sizzle_cool <= 0.0 and _lava_mix(_dir) > 0.45:
		_sizzle_cool = 1.2
		_vy = JUMP_V * 0.75
		_h = maxf(_h, 0.04)
		_chime(0.45)
		if _main != null and _main.has_method("_sparkle_burst"):
			_main._sparkle_burst(_surf(_dir, 1.2), LAVA_COL)
		if _sizzle_say <= 0.0:
			_sizzle_say = 9.0
			if _main != null and _main.has_method("show_msg"):
				_main.show_msg("Roshan", "Hot hot hot! Hop hop hop!", "giggle")
	# lanterns light by simple proximity — walking up is the whole puzzle
	var feet := _surf(_dir, _h)
	if _h < 2.0:
		for ld2 in _lanterns:
			if not bool(ld2["lit"]) and _dir.angle_to(ld2["dir"]) * PLANET_R < 4.0:
				_light_lantern(int(ld2["idx"]))
	# the GREAT GATE: when open, walking in starts the fortress dungeon
	_gate_cool = maxf(0.0, _gate_cool - delta)
	if _gate_open and _gate_cool <= 0.0 and _h < 1.5 and _dir.angle_to(GATE_DIR.normalized()) * PLANET_R < 4.5:
		_gate_cool = 6.0
		if _main != null and _main.has_method("_start_ember_dungeon"):
			_main.call_deferred("_start_ember_dungeon")
			return
	# jump / gravity (radial)
	if _jump_pressed() and _h <= 0.05:
		_vy = JUMP_V
		if _main != null and _main.has_method("_sparkle_burst"):
			_main._sparkle_burst(_surf(_dir, 1.0), Color(0.7, 0.85, 1.0))
	_vy -= GRAV * delta
	_h = maxf(0.0, _h + _vy * delta)
	if _h <= 0.0:
		_vy = 0.0
	_update_avatar_transform()
	# camera: behind & above along the local up (+ look-around peek)
	_cam_peek(delta)
	var up := _dir
	var cam_fwd := _fwd.rotated(up, _cam_orbit)
	var want: Vector3 = _surf(_dir, _h + 7.5 + _cam_pitch) - cam_fwd * 13.0
	_cam.position = _cam.position.lerp(want, clampf(delta * 5.0, 0.0, 1.0))
	_cam.look_at(_surf(_dir, _h + 2.2) + cam_fwd * 3.0, up)
	# the rainbow home ring: leave at any time, never a loss
	if _home_pos.distance_to(feet) < 5.5:
		_teardown(false)

# ---------------------------------------------------------------- dungeon glue

func resume_from_dungeon(completed: bool) -> void:
	# Main re-enables this level after the fortress dungeon closes; put Roshan
	# back outside the Great Gate and re-take the camera.
	_gate_cool = 8.0
	_dir = GATE_DIR.normalized().rotated(Vector3.RIGHT, 0.12).normalized()
	_project_fwd()
	_h = 0.0
	_vy = 0.0
	_update_avatar_transform()
	if _cam != null:
		_cam.make_current()
	var done: bool = _main != null and "ember_done" in _main and bool(_main.ember_done)
	if completed and done and not _celebrated:
		_celebrated = true
		if _lbl_big != null:
			_lbl_big.text = "⭐ FORTRESS HERO! ⭐\nThe Ember King is your friend now!"
		if _lbl_hint != null:
			_lbl_hint.text = "The whole fortress is safe and sparkling — the home ring waits at the south pole!"
		if _main != null and _main.has_method("_sparkle_burst"):
			for i in range(6):
				_main._sparkle_burst(_surf(GATE_DIR.normalized(), 3.0 + float(i) * 1.5), Color.from_hsv(fposmod(float(i) * 0.17, 1.0), 0.6, 1.0))
		var tw := create_tween()
		tw.tween_interval(4.0)
		tw.tween_callback(func():
			if _lbl_big != null and _state == "play":
				_lbl_big.text = "")
	elif _lbl_hint != null:
		if done:
			_lbl_hint.text = "Welcome back outside! The fortress is your playground now."
		else:
			_lbl_hint.text = "Checkpoint safe! The Great Gate stays open — walk back in whenever you feel brave."

# ---------------------------------------------------------------- misc

func _chime(pitch: float) -> void:
	if _main != null and "chime" in _main and _main.chime != null:
		_main.chime.pitch_scale = pitch
		_main.chime.play()

func _teardown(completed: bool) -> void:
	_state = "done"
	if _prev_env != null and "we_node" in _main and _main.we_node != null:
		_main.we_node.environment = _prev_env
	if _player_node != null and "cam" in _player_node and _player_node.cam != null:
		(_player_node.cam as Camera3D).make_current()
	if _finish_cb.is_valid():
		_finish_cb.call(completed)
	queue_free()
