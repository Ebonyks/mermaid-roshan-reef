extends Node3D
class_name GalaxyLevel
# ============================================================================
# LEVEL 3 — ROSHAN'S BUTTERFLY WORLD. A Mario-Galaxy-style mini-planet themed
# after the book's Milwaukee-museum butterfly vivarium: glass conservatory dome,
# lush garden + corals, fruit trays that call the butterfly swarm, crawling
# beetles, hanging lanterns — under the galaxy-and-aurora sky.
#
# Reached THROUGH the rainbow world: finishing the floating Rainbow Road race
# (the Level-2 rainbow gateway) soars on into the galaxy.
#
# Self-contained (same pattern as KartGame): builds its own planet, sky, avatar,
# camera, HUD and objective; freezes the main player while active; calls
# finish_cb(completed: bool) and frees itself on exit.
#
# GOAL: find the 7 LOST BABY BUTTERFLIES around the planet; the GREAT RAINBOW
# BUTTERFLY then appears at the Butterfly Palace on the north pole — touch it
# to save the world. A rainbow home-ring at the south pole exits at any time.
#
# Movement (same vocabulary as swimming): stick/arrows = run & turn,
# tap / second finger / SPACE / gamepad-A = JUMP (radial, floaty).
# ============================================================================

const PLANET_R := 42.0            # tightened from 55 — the round-world physics read better small
const ORIGIN := Vector3(0.0, 9000.0, 0.0)
const GRAV := 26.0
const JUMP_V := 17.0
const RUN_SPD := 13.5
const TURN_SPD := 2.4
const SHARDS := 7
const CRYSTALS := ["res://assets/galaxy/crystal1.glb", "res://assets/galaxy/crystal2.glb", "res://assets/galaxy/crystal3.glb"]
const FLORA := ["flower_purpleA", "flower_redA", "flower_yellowB", "mushroom_red", "mushroom_tanGroup"]
# tropical foliage (palms, monstera, ferns, big leaves) — the butterfly house
# is a greenhouse full of tropical plants, not a pine forest
const TROPICAL := [
	"res://assets/galaxy/trop_palm1.glb", "res://assets/galaxy/trop_palm2.glb",
	"res://assets/galaxy/trop_monstera.glb", "res://assets/galaxy/trop_bigleaf.glb",
	"res://assets/galaxy/trop_fern.glb",
	"res://assets/nature/plant_bush.glb", "res://assets/nature/grass_leafsLarge.glb"]
const CASTLE_GLB := "res://assets/galaxy/crystal_castle.glb"
const GATE_DIR := Vector3(0.30, 1.0, 0.0)   # (normalized on use) the castle gate on the planet
const HALL_C := Vector3(0.0, 9300.0, 0.0)   # the Star Hall floats high above the planet
const BUTTERFLY_GLBS := ["res://assets/galaxy/butterfly1.glb", "res://assets/galaxy/butterfly2.glb"]
const FRUIT_GLBS := ["res://assets/galaxy/fruit_apple.glb", "res://assets/galaxy/fruit_banana.glb", "res://assets/galaxy/fruit_orange.glb", "res://assets/galaxy/fruit_melon.glb"]
const TRAY_GLB := "res://assets/galaxy/tray.glb"
# butterfly wing palettes — "all the colours and styles" from the butterfly-house photo
const WING_COLS := [Color(1.0, 0.5, 0.15), Color(0.25, 0.45, 1.0), Color(0.75, 1.0, 0.85), Color(1.0, 0.85, 0.3), Color(0.95, 0.35, 0.4), Color(0.6, 0.4, 1.0), Color(0.4, 0.8, 1.0)]
const BUG_GLBS := ["res://assets/galaxy/beetle.glb", "res://assets/galaxy/ladybug.glb"]
const CORALS := ["res://assets/aquatic/Coral1.glb", "res://assets/aquatic/Coral2.glb", "res://assets/aquatic/Coral3.glb", "res://assets/aquatic/Coral4.glb", "res://assets/aquatic/Coral5.glb", "res://assets/aquatic/Coral6.glb"]

var _main: Node = null
var _player_node: Node3D = null
var _finish_cb: Callable
var _cam: Camera3D = null
var _prev_env: Environment = null
var _hud: CanvasLayer = null
var _lbl_shards: Label = null
var _lbl_big: Label = null
var _lbl_hint: Label = null

# avatar state on the sphere
var _dir := Vector3(0, 0, 1)      # unit vector from planet centre to feet
var _fwd := Vector3(1, 0, 0)      # unit tangent facing
var _h := 0.0                     # height above surface
var _vy := 0.0                    # radial velocity
var _avatar: Node3D = null
var _fire_prev := false
var _bob_t := 0.0

var _shard_nodes: Array = []
var _shards_got := 0
var _grand: Node3D = null
var _grand_active := false
var _home_pos := Vector3.ZERO
var _moons: Array = []
var _blockers: Array = []         # crystal footprints: {dir, r, cool} (surface metres)
var _pads: Array = []             # flower bounce pads: {dir: Vector3, cool: float}
var _flyers: Array = []           # ambient butterflies: {node, axis, dir0, alt, spd, ph, flap}
var _trays: Array = []            # fruit feeding trays: {dir: Vector3, cool: float, node}
var _idle_t := 0.0                # stand still and a butterfly comes to visit
var _bugs: Array = []             # crawling beetles/ladybugs: {node, axis, dir0, spd, ph, cool}
var _rosalina: Sprite3D = null
var _rosa_cool := 0.0
# ---- Star Hall (castle interior) state ----
var _mode := "planet"             # "planet" | "hall"
var _hall_built := false
var _hall_root: Node3D = null
var _cpos := Vector3.ZERO         # local position on the hall floor
var _cyaw := 0.0
var _ch := 0.0
var _cvy := 0.0
var _hall_flies: Array = []       # indoor butterflies: {node, r, spd, ph, h}
var _bells: Array = []            # star bells: {node, pos, cool}
var _fount_cool := 0.0
var _gate_cool := 0.0
var _state := "play"              # play -> won -> done
var _won_t := 0.0

# ---------------------------------------------------------------- lifecycle

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

func start(main: Node, finish_cb: Callable) -> void:
	_main = main
	_finish_cb = finish_cb
	if "player" in main and main.player != null:
		_player_node = main.player
	_build_env_sky()
	_build_planet()
	_build_decor()
	_build_shards()
	_build_home_ring()
	_build_avatar()
	_build_camera()
	_build_hud()
	_lbl_big.text = "🦋 Roshan's Butterfly World 🦋"
	_lbl_hint.text = "Find the 7 lost butterflies — follow their beacons!  •  fruit trays call the swarm!"
	var tw := create_tween()
	tw.tween_interval(3.0)
	tw.tween_callback(func():
		if _lbl_big != null and _state == "play":
			_lbl_big.text = "")

# ---------------------------------------------------------------- sky & env
func _build_env_sky() -> void:
	if "we_node" in _main and _main.we_node != null:
		_prev_env = _main.we_node.environment
		var e := Environment.new()
		e.background_mode = Environment.BG_COLOR
		e.background_color = Color(0.01, 0.005, 0.03)
		e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		e.ambient_light_color = Color(0.55, 0.45, 0.75)
		e.ambient_light_energy = 1.0
		e.glow_enabled = true
		e.glow_intensity = 0.7
		e.glow_bloom = 0.1
		_main.we_node.environment = e
	# key light: soft starlight sun + a cool rim from the opposite side
	var sun := DirectionalLight3D.new()
	sun.light_energy = 1.1
	sun.light_color = Color(1.0, 0.92, 0.95)
	sun.rotation_degrees = Vector3(-40, 35, 0)
	add_child(sun)
	var rim := DirectionalLight3D.new()
	rim.light_energy = 0.5
	rim.light_color = Color(0.5, 0.8, 1.0)
	rim.rotation_degrees = Vector3(30, 215, 0)
	add_child(rim)
	# the galaxy-and-aurora sky: one huge inside-out sphere, pure shader
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
	// deep space gradient
	vec3 col = mix(vec3(0.01, 0.005, 0.04), vec3(0.05, 0.02, 0.10), uv.y);
	// star layers
	vec2 g1 = uv * vec2(260.0, 140.0);
	float s1 = step(0.994, h21(floor(g1))) * smoothstep(0.22, 0.0, length(fract(g1) - 0.5));
	vec2 g2 = uv * vec2(120.0, 70.0);
	float tw = 0.6 + 0.4 * sin(TIME * 2.0 + h21(floor(g2)) * 40.0);
	float s2 = step(0.990, h21(floor(g2) + 7.0)) * smoothstep(0.3, 0.0, length(fract(g2) - 0.5)) * tw;
	col += vec3(s1) + vec3(1.0, 0.9, 0.8) * s2;
	// distant spiral galaxy (swirled brightness blob)
	vec2 gc = (uv - vec2(0.72, 0.62)) * vec2(2.0, 3.6);
	float r = length(gc);
	float ang = atan(gc.y, gc.x);
	float arm = 0.5 + 0.5 * cos(ang * 2.0 - r * 9.0 + TIME * 0.02);
	float gal = exp(-r * 3.2) * (0.35 + 0.65 * arm);
	col += vec3(0.85, 0.7, 1.0) * gal * 0.9 + vec3(1.0, 0.9, 0.75) * exp(-r * 9.0);
	// aurora borealis ribbons around the lower sky
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
float h21(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5); }
void fragment(){
	// flowering-meadow planet (the butterfly-house garden): soft grass with
	// sandy landscaped paths and thousands of tiny flower dots
	float band = sin(UV.y * 14.0) * 0.5 + 0.5;
	vec3 a = vec3(0.45, 0.76, 0.42);   // meadow green
	vec3 b = vec3(0.58, 0.86, 0.48);   // sunlit grass
	vec3 col = mix(a, b, band);
	// two winding garden paths circling the planet
	float wob = sin(UV.x * 12.566) * 0.03;
	float pathm = exp(-pow((UV.y - 0.36 + wob) * 34.0, 2.0)) + exp(-pow((UV.y - 0.66 - wob) * 34.0, 2.0));
	col = mix(col, vec3(0.90, 0.83, 0.62), clamp(pathm, 0.0, 1.0) * 0.85);
	// confetti of tiny flowers
	vec2 g = UV * vec2(220.0, 120.0);
	float fh = h21(floor(g));
	float dot2 = step(0.986, fh) * smoothstep(0.3, 0.05, length(fract(g) - 0.5));
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
	planet.material_override = mat
	planet.position = ORIGIN
	add_child(planet)
	# atmosphere: slightly larger fresnel shell
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
	ALBEDO = vec3(0.55, 0.5, 1.0) * f * 0.55;
	ALPHA = f * 0.55;
}"""
	var amat := ShaderMaterial.new()
	amat.shader = ash
	atmo.material_override = amat
	atmo.position = ORIGIN
	add_child(atmo)

func _surf(dir: Vector3, h: float = 0.0) -> Vector3:
	return ORIGIN + dir.normalized() * (PLANET_R + h)

func _tint_meshes(root: Node, col: Color, glow: float) -> void:
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

func _place_on_planet(node: Node3D, dir: Vector3, h: float = 0.0) -> void:
	# stand `node` on the sphere: position on surface, local up = radial out
	var d := dir.normalized()
	node.position = _surf(d, h)
	var up := d
	var any := Vector3.UP if absf(up.dot(Vector3.UP)) < 0.95 else Vector3.RIGHT
	var t := any.cross(up).normalized()
	node.transform.basis = Basis(t, up, t.cross(up).normalized() * -1.0).orthonormalized()

func _fit_small(model: Node3D, target_long: float) -> float:
	# normalise a GLB to a footprint (assets range from 0.14 to 98 units raw)
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

func _make_butterfly(tint: Color, wingspan: float) -> Node3D:
	# a tinted butterfly from the CC set (two body styles x seven wing colours)
	var holder := Node3D.new()
	var path: String = BUTTERFLY_GLBS[randi() % BUTTERFLY_GLBS.size()]
	if ResourceLoader.exists(path):
		var bf: Node3D = (load(path) as PackedScene).instantiate()
		holder.add_child(bf)
		_fit_small(bf, wingspan)
		_tint_meshes(bf, tint, 0.25)
	else:
		var q := MeshInstance3D.new()
		var qm := QuadMesh.new()
		qm.size = Vector2(wingspan, wingspan * 0.7)
		q.mesh = qm
		var m := StandardMaterial3D.new()
		m.albedo_color = tint
		m.cull_mode = BaseMaterial3D.CULL_DISABLED
		q.material_override = m
		holder.add_child(q)
	return holder

# ---------------------------------------------------------------- decor
func _build_decor() -> void:
	var pastels := [Color(0.85, 0.6, 1.0), Color(0.55, 0.9, 1.0), Color(1.0, 0.6, 0.85), Color(0.6, 1.0, 0.75), Color(1.0, 0.9, 0.5)]
	# ---- LUSH TROPICAL GARDEN, 3-4x dense: palms, monstera, big leaves, ferns
	# all around the little planet (natural colours — no candy tint) ----
	for i in range(32):
		var gpath: String = TROPICAL[i % TROPICAL.size()]
		if not ResourceLoader.exists(gpath):
			continue
		var gr: Node3D = (load(gpath) as PackedScene).instantiate()
		var dir := Vector3(sin(float(i) * 2.4) * cos(float(i) * 0.83), sin(float(i) * 0.9) * 0.85, cos(float(i) * 2.4) * cos(float(i) * 0.83)).normalized()
		var holder := Node3D.new()
		add_child(holder)
		holder.add_child(gr)
		var tall: bool = i % TROPICAL.size() < 2   # the two palm species
		_fit_small(gr, (10.0 + fposmod(float(i) * 1.7, 4.0)) if tall else (3.2 + fposmod(float(i) * 1.3, 2.4)))
		_place_on_planet(holder, dir)
		holder.rotate(dir, randf() * TAU)
		if tall and i % 3 == 0:   # a handful of solid palm trunks; the rest is soft
			_blockers.append({"dir": dir, "r": 1.8, "cool": 0.0})
	# flower beds (bright, chest-high) between the palms
	for i in range(28):
		var fpath := "res://assets/nature/%s.glb" % FLORA[i % FLORA.size()]
		if not ResourceLoader.exists(fpath):
			continue
		var fl: Node3D = (load(fpath) as PackedScene).instantiate()
		var holder2 := Node3D.new()
		add_child(holder2)
		fl.scale = Vector3.ONE * (4.0 + fposmod(float(i) * 2.3, 3.0))
		holder2.add_child(fl)
		_tint_meshes(fl, pastels[(i + 2) % pastels.size()], 0.20)
		var dir2 := Vector3(sin(float(i) * 1.1 + 2.0), cos(float(i) * 1.7), sin(float(i) * 0.6 - 1.0)).normalized()
		_place_on_planet(holder2, dir2)
	# ---- FRUIT FEEDING TRAYS: walk up and the butterflies swarm in to feast ----
	var tray_dirs := [Vector3(0.8, 0.15, -0.6), Vector3(-0.75, 0.4, 0.5), Vector3(0.1, -0.55, 0.83), Vector3(-0.4, -0.75, -0.55)]
	for ti in range(tray_dirs.size()):
		var tdir: Vector3 = (tray_dirs[ti] as Vector3).normalized()
		var th := Node3D.new()
		add_child(th)
		if ResourceLoader.exists("res://assets/aquatic/Rock2.glb"):
			var ped: Node3D = (load("res://assets/aquatic/Rock2.glb") as PackedScene).instantiate()
			var ph2 := Node3D.new()
			th.add_child(ph2)
			ph2.add_child(ped)
			_fit_small(ped, 3.6)
			ph2.position = Vector3(0, -0.4, 0)
		for ci in range(5):
			var cube := MeshInstance3D.new()
			var cbm := BoxMesh.new()
			cbm.size = Vector3(0.42, 0.42, 0.42)
			cube.mesh = cbm
			var cmat := StandardMaterial3D.new()
			cmat.albedo_color = [Color(1.0, 0.6, 0.2), Color(1.0, 0.85, 0.3), Color(0.6, 0.9, 0.4), Color(1.0, 0.5, 0.5), Color(0.95, 0.75, 0.4)][ci]
			cmat.roughness = 0.4
			cube.material_override = cmat
			cube.position = Vector3(cos(float(ci) * 1.25) * 0.7, 0.75, sin(float(ci) * 1.25) * 0.7)
			th.add_child(cube)
		if ResourceLoader.exists(TRAY_GLB):
			var tr: Node3D = (load(TRAY_GLB) as PackedScene).instantiate()
			th.add_child(tr)
			_fit_small(tr, 4.2)
		else:
			var cyl := MeshInstance3D.new()
			var cm := CylinderMesh.new()
			cm.top_radius = 2.1
			cm.bottom_radius = 2.1
			cm.height = 0.5
			cyl.mesh = cm
			th.add_child(cyl)
		for fi in range(3):
			var fpath2: String = FRUIT_GLBS[(ti + fi) % FRUIT_GLBS.size()]
			if not ResourceLoader.exists(fpath2):
				continue
			var fr: Node3D = (load(fpath2) as PackedScene).instantiate()
			var fh := Node3D.new()
			th.add_child(fh)
			fh.add_child(fr)
			_fit_small(fr, 1.5)
			fh.position = Vector3(cos(float(fi) * TAU / 3.0) * 1.1, 0.5, sin(float(fi) * TAU / 3.0) * 1.1)
		var tl := OmniLight3D.new()
		tl.light_color = Color(1.0, 0.9, 0.6)
		tl.light_energy = 1.2
		tl.omni_range = 9.0
		tl.position = Vector3(0, 2.4, 0)
		th.add_child(tl)
		_place_on_planet(th, tdir)
		_trays.append({"dir": tdir, "cool": 0.0, "node": th})
	# ---- AMBIENT BUTTERFLIES: a living cloud of colour around the whole garden ----
	for i in range(20):
		var wc: Color = WING_COLS[i % WING_COLS.size()]
		var bfly := _make_butterfly(wc, 1.6 + randf() * 1.2)
		add_child(bfly)
		var d0 := Vector3(randf() * 2 - 1, randf() * 2 - 1, randf() * 2 - 1).normalized()
		var ax := d0.cross(Vector3(randf() * 2 - 1, randf() * 2 - 1, randf() * 2 - 1).normalized()).normalized()
		_flyers.append({"node": bfly, "axis": ax, "dir0": d0, "alt": 2.2 + randf() * 4.0, "spd": 0.10 + randf() * 0.14, "ph": randf() * TAU, "flap": 12.0 + randf() * 8.0})
	# CRYSTAL CASTLE at the north pole (real CC0 castle model, crystal-tinted),
	# flanked by two of the old crystals — Mermaid Rosalina watches over it
	var castle := Node3D.new()
	add_child(castle)
	if ResourceLoader.exists(CASTLE_GLB):
		var ck: Node3D = (load(CASTLE_GLB) as PackedScene).instantiate()
		castle.add_child(ck)
		_fit_small(ck, 36.0)   # the pole landmark — big enough to walk INTO
		_tint_meshes(ck, Color(0.72, 0.68, 1.0), 0.45)   # amethyst-glass glow
	_blockers.append({"dir": Vector3.UP, "r": 8.0, "cool": 0.0})   # castle core is solid; enter via the GATE
	for i in range(2):
		var path3: String = CRYSTALS[i % CRYSTALS.size()]
		if not ResourceLoader.exists(path3):
			continue
		var spire: Node3D = (load(path3) as PackedScene).instantiate()
		spire.scale = Vector3.ONE * 4.0
		spire.position = Vector3([-13.0, 13.0][i], 0, 6.0)
		castle.add_child(spire)
		_tint_meshes(spire, Color(0.8, 0.7, 1.0), 0.5)
	_place_on_planet(castle, Vector3.UP)
	# the glowing GATE — walk into it to step inside the crystal castle
	var gatel := Label3D.new()
	gatel.text = "✨ Crystal Castle ✨\ncome in!"
	gatel.font_size = 50
	gatel.pixel_size = 0.03
	gatel.outline_size = 12
	gatel.modulate = Color(0.85, 0.8, 1.0)
	gatel.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	gatel.position = _surf(GATE_DIR, 6.5)
	add_child(gatel)
	var gatehalo := MeshInstance3D.new()
	var ghm := TorusMesh.new()
	ghm.inner_radius = 2.4
	ghm.outer_radius = 3.2
	gatehalo.mesh = ghm
	var ghmat := StandardMaterial3D.new()
	ghmat.albedo_color = Color(0.8, 0.7, 1.0)
	ghmat.emission_enabled = true
	ghmat.emission = Color(0.75, 0.65, 1.0)
	ghmat.emission_energy_multiplier = 1.6
	gatehalo.material_override = ghmat
	var gh_holder := Node3D.new()
	add_child(gh_holder)
	gh_holder.add_child(gatehalo)
	gatehalo.position = Vector3(0, 2.6, 0)
	gatehalo.rotation_degrees = Vector3(90, 0, 0)
	_place_on_planet(gh_holder, GATE_DIR)
	# Mermaid Rosalina, keeper of the crystal castle
	var rosa := Sprite3D.new()
	if ResourceLoader.exists("res://assets/characters/skins/fairy_mermaid.png"):
		var rtex: Texture2D = load("res://assets/characters/skins/fairy_mermaid.png")
		rosa.texture = rtex
		rosa.pixel_size = 7.0 / maxf(float(rtex.get_height()), 1.0)
	rosa.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	rosa.position = _surf(Vector3(0.16, 1.0, 0.13).normalized(), 4.0)
	add_child(rosa)
	_rosalina = rosa
	var rl := Label3D.new()
	rl.text = "Mermaid Rosalina"
	rl.font_size = 52
	rl.pixel_size = 0.03
	rl.outline_size = 12
	rl.modulate = Color(0.8, 0.9, 1.0)
	rl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	rl.position = rosa.position + Vector3(0, 5.0, 0)
	add_child(rl)
	var claby := Label3D.new()
	claby.text = "Butterfly Palace"
	claby.font_size = 72
	claby.outline_size = 16
	claby.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	claby.modulate = Color(0.95, 0.85, 1.0)
	claby.position = _surf(Vector3.UP, 14.0)
	add_child(claby)
	var cl := OmniLight3D.new()
	cl.light_color = Color(0.85, 0.7, 1.0)
	cl.light_energy = 2.5
	cl.omni_range = 30.0
	cl.position = _surf(Vector3.UP, 8.0)
	add_child(cl)
	# ---- FLOWER BOUNCE PADS: glowing blossom rings that fling Roshan sky-high ----
	for pdir_raw in [Vector3(1.0, 0.35, 0.5), Vector3(-0.55, -0.45, 0.75), Vector3(0.25, -0.85, -0.55)]:
		var pdir: Vector3 = (pdir_raw as Vector3).normalized()
		var pad := MeshInstance3D.new()
		var ptm := TorusMesh.new()
		ptm.inner_radius = 2.0
		ptm.outer_radius = 3.2
		pad.mesh = ptm
		var pmat := StandardMaterial3D.new()
		pmat.albedo_color = Color(1.0, 0.6, 0.8)
		pmat.emission_enabled = true
		pmat.emission = Color(1.0, 0.55, 0.75)
		pmat.emission_energy_multiplier = 1.6
		pad.material_override = pmat
		var holder3 := Node3D.new()
		add_child(holder3)
		holder3.add_child(pad)
		pad.position = Vector3(0, 0.6, 0)
		_place_on_planet(holder3, pdir)
		var pl := OmniLight3D.new()
		pl.light_color = Color(1.0, 0.85, 0.4)
		pl.light_energy = 1.4
		pl.omni_range = 10.0
		pl.position = Vector3(0, 2.0, 0)
		holder3.add_child(pl)
		_pads.append({"dir": pdir, "cool": 0.0})
	# two candy moons that orbit the planet
	for i in range(2):
		var moon := MeshInstance3D.new()
		var mm := SphereMesh.new()
		mm.radius = 6.0 - float(i) * 2.0
		mm.height = mm.radius * 2.0
		moon.mesh = mm
		var mmat := StandardMaterial3D.new()
		mmat.albedo_color = [Color(1.0, 0.62, 0.2), Color(0.45, 0.8, 0.35)][i]   # orange + melon moons
		mmat.emission_enabled = true
		mmat.emission = mmat.albedo_color
		mmat.emission_energy_multiplier = 0.35
		moon.material_override = mmat
		add_child(moon)
		_moons.append({"node": moon, "r": PLANET_R * (1.9 + 0.7 * float(i)), "spd": 0.15 - 0.05 * float(i), "ph": float(i) * 2.4, "tilt": 0.4 + 0.5 * float(i)})
	# ---- GLASS CONSERVATORY DOME: the vivarium's window-grid wraps the whole
	# planet (the museum butterfly room's glass walls from the book) ----
	var dome := MeshInstance3D.new()
	var dsm := SphereMesh.new()
	dsm.radius = PLANET_R * 2.7
	dsm.height = PLANET_R * 5.4
	dsm.radial_segments = 48
	dsm.rings = 24
	dome.mesh = dsm
	var dsh := Shader.new()
	dsh.code = """shader_type spatial;
render_mode unshaded, cull_front;
void fragment(){
	vec2 grid = abs(fract(UV * vec2(26.0, 13.0)) - 0.5);
	float line = smoothstep(0.035, 0.012, min(grid.x, grid.y));
	ALBEDO = mix(vec3(0.75, 0.9, 0.95), vec3(0.93, 0.97, 1.0), line);
	ALPHA = mix(0.05, 0.45, line);
}"""
	var dmat := ShaderMaterial.new()
	dmat.shader = dsh
	dome.material_override = dmat
	dome.position = ORIGIN
	add_child(dome)
	# ---- hanging-lantern posts along the garden paths (page-two paper lantern) ----
	for ldir_raw in [Vector3(0.6, 0.55, 0.55), Vector3(-0.7, 0.5, -0.4), Vector3(0.2, 0.6, -0.75), Vector3(-0.5, -0.6, 0.6), Vector3(0.75, -0.5, -0.35)]:
		var ldir: Vector3 = (ldir_raw as Vector3).normalized()
		var lp := Node3D.new()
		add_child(lp)
		var pole := MeshInstance3D.new()
		var pcm := CylinderMesh.new()
		pcm.top_radius = 0.16
		pcm.bottom_radius = 0.22
		pcm.height = 6.5
		pole.mesh = pcm
		var pom := StandardMaterial3D.new()
		pom.albedo_color = Color(0.35, 0.26, 0.2)
		pole.material_override = pom
		pole.position = Vector3(0, 3.25, 0)
		lp.add_child(pole)
		var lant := MeshInstance3D.new()
		var lsm := SphereMesh.new()
		lsm.radius = 1.0
		lsm.height = 1.7
		lant.mesh = lsm
		var lam := StandardMaterial3D.new()
		lam.albedo_color = Color(1.0, 0.9, 0.78)
		lam.emission_enabled = true
		lam.emission = Color(1.0, 0.85, 0.6)
		lam.emission_energy_multiplier = 1.8
		lant.material_override = lam
		lant.position = Vector3(0, 6.8, 0)
		lp.add_child(lant)
		var ll := OmniLight3D.new()
		ll.light_color = Color(1.0, 0.85, 0.6)
		ll.light_energy = 1.5
		ll.omni_range = 13.0
		ll.position = Vector3(0, 6.4, 0)
		lp.add_child(ll)
		_place_on_planet(lp, ldir)
	# ---- corals nestled among the plants (the book's underwater-garden mashup) ----
	for i in range(18):
		var cpath: String = CORALS[i % CORALS.size()]
		if not ResourceLoader.exists(cpath):
			continue
		var co: Node3D = (load(cpath) as PackedScene).instantiate()
		var ch := Node3D.new()
		add_child(ch)
		ch.add_child(co)
		_fit_small(co, 2.6 + randf() * 1.8)
		_tint_meshes(co, [Color(1.0, 0.6, 0.7), Color(0.6, 0.8, 1.0), Color(1.0, 0.8, 0.5), Color(0.8, 0.6, 1.0)][i % 4], 0.15)
		var cdir := Vector3(sin(float(i) * 1.9 + 1.0), cos(float(i) * 1.3 + 0.5) * 0.9, sin(float(i) * 0.8 - 2.0)).normalized()
		_place_on_planet(ch, cdir)
	# ---- friendly beetles + ladybugs crawl the paths (the museum beetle drawer!) ----
	for i in range(8):
		var bpath: String = BUG_GLBS[i % BUG_GLBS.size()]
		if not ResourceLoader.exists(bpath):
			continue
		var bug: Node3D = (load(bpath) as PackedScene).instantiate()
		var bh2 := Node3D.new()
		add_child(bh2)
		bh2.add_child(bug)
		_fit_small(bug, 1.6 if i % BUG_GLBS.size() == 0 else 1.1)
		if i % BUG_GLBS.size() == 0:
			_tint_meshes(bug, [Color(0.4, 0.9, 0.5), Color(0.9, 0.6, 0.2), Color(0.5, 0.6, 1.0)][i % 3], 0.30)   # jewel-beetle shine
		var bd0 := Vector3(randf() * 2 - 1, randf() * 2 - 1, randf() * 2 - 1).normalized()
		var bax := bd0.cross(Vector3(randf() * 2 - 1, randf() * 2 - 1, randf() * 2 - 1).normalized()).normalized()
		_bugs.append({"node": bh2, "axis": bax, "dir0": bd0, "spd": 0.02 + randf() * 0.02, "ph": randf() * TAU, "cool": 0.0})
	# drifting star sparkles all around
	var stars := CPUParticles3D.new()
	stars.amount = 60
	stars.lifetime = 12.0
	stars.emission_shape = CPUParticles3D.EMISSION_SHAPE_SPHERE
	stars.emission_sphere_radius = PLANET_R * 2.2
	stars.gravity = Vector3.ZERO
	stars.initial_velocity_min = 0.2
	stars.initial_velocity_max = 1.0
	stars.scale_amount_min = 0.1
	stars.scale_amount_max = 0.35
	var sm2 := SphereMesh.new()
	sm2.radius = 0.4
	sm2.height = 0.8
	stars.mesh = sm2
	var smt := StandardMaterial3D.new()
	smt.albedo_color = Color(1.0, 0.95, 0.8)
	smt.emission_enabled = true
	smt.emission = Color(1.0, 0.95, 0.7)
	smt.emission_energy_multiplier = 1.5
	smt.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	stars.mesh.material = smt
	stars.position = ORIGIN
	add_child(stars)

# ---------------------------------------------------------------- objective
func _build_shards() -> void:
	for i in range(SHARDS):
		var a: float = float(i) / float(SHARDS) * TAU
		var dir := Vector3(cos(a) * 0.9, sin(a * 3.0) * 0.75 - 0.1, sin(a) * 0.9).normalized()
		# a LOST BABY BUTTERFLY, one of each wing colour (the objective, re-themed
		# from star shards to match the butterfly-house book page)
		var wing: Color = WING_COLS[i % WING_COLS.size()]
		var star := _make_butterfly(wing, 2.6)
		star.position = _surf(dir, 2.6)
		add_child(star)
		var gl := OmniLight3D.new()
		gl.light_color = wing
		gl.light_energy = 1.6
		gl.omni_range = 14.0
		star.add_child(gl)
		# BEACON: a tall additive light pillar so far-away shards show over the horizon
		var beam := MeshInstance3D.new()
		var bc := CylinderMesh.new()
		bc.top_radius = 0.4
		bc.bottom_radius = 1.5
		bc.height = 34.0
		bc.radial_segments = 8
		beam.mesh = bc
		var bmt := StandardMaterial3D.new()
		bmt.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		bmt.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		bmt.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		bmt.albedo_color = Color(wing.r, wing.g, wing.b, 0.30)
		beam.material_override = bmt
		beam.position = _surf(dir, 19.0)
		var bup := dir
		var bany := Vector3.UP if absf(bup.dot(Vector3.UP)) < 0.95 else Vector3.RIGHT
		var bt := bany.cross(bup).normalized()
		beam.transform.basis = Basis(bt, bup, bt.cross(bup).normalized() * -1.0).orthonormalized()
		beam.position = _surf(dir, 19.0)
		add_child(beam)
		_shard_nodes.append({"node": star, "dir": dir, "got": false, "ph": float(i) * 1.3, "beam": beam})

func _build_home_ring() -> void:
	_home_pos = _surf(Vector3.DOWN, 4.0)
	var ring := MeshInstance3D.new()
	var tm := TorusMesh.new()
	tm.inner_radius = 3.0
	tm.outer_radius = 4.2
	ring.mesh = tm
	var m := StandardMaterial3D.new()
	m.albedo_color = Color(0.6, 0.95, 0.8)
	m.emission_enabled = true
	m.emission = Color(0.4, 1.0, 0.7)
	m.emission_energy_multiplier = 1.2
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	ring.material_override = m
	ring.position = _home_pos
	add_child(ring)
	var lab := Label3D.new()
	lab.text = "🏠 home"
	lab.font_size = 56
	lab.outline_size = 12
	lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lab.position = _surf(Vector3.DOWN, 9.0)
	add_child(lab)

func _spawn_grand_star() -> void:
	_grand_active = true
	_grand = Node3D.new()
	add_child(_grand)
	var star := _make_butterfly(Color(1.0, 0.85, 0.4), 7.5)   # the GREAT golden butterfly
	_grand.add_child(star)
	var gl := OmniLight3D.new()
	gl.light_color = Color(1.0, 0.9, 0.4)
	gl.light_energy = 5.0
	gl.omni_range = 50.0
	_grand.add_child(gl)
	_grand.position = _surf(Vector3.UP, 9.0)
	_lbl_big.text = "The GREAT RAINBOW BUTTERFLY!\nRace to the Butterfly Palace!"
	var tw := create_tween()
	tw.tween_interval(2.6)
	tw.tween_callback(func():
		if _lbl_big != null and _state == "play":
			_lbl_big.text = "")
	if _main != null and _main.has_method("_sparkle_burst"):
		_main._sparkle_burst(_grand.position, Color(1.0, 0.9, 0.4))

# ---------------------------------------------------------------- avatar
func _build_avatar() -> void:
	_avatar = Node3D.new()
	add_child(_avatar)
	var glb := "res://assets/characters/roshan.glb"
	if ResourceLoader.exists(glb):
		var inst: Node3D = (load(glb) as PackedScene).instantiate()
		# reuse the race engine's fit idea: measure and normalise to ~4.2 tall
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
	var trail := OmniLight3D.new()
	trail.light_color = Color(1.0, 0.6, 0.9)
	trail.light_energy = 1.6
	trail.omni_range = 10.0
	trail.position = Vector3(0, 2.0, 0)
	_avatar.add_child(trail)
	_dir = Vector3(0, -0.2, 1).normalized()
	_fwd = Vector3(1, 0, 0)
	_project_fwd()
	_update_avatar_transform()

func _gather_aabbs(n: Node, xf: Transform3D, acc: Array) -> void:
	if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
		acc.append(xf * (n as MeshInstance3D).get_aabb())
	for c in n.get_children():
		if c is Node3D:
			_gather_aabbs(c, xf * (c as Node3D).transform, acc)
		else:
			_gather_aabbs(c, xf, acc)

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

func _build_camera() -> void:
	_cam = Camera3D.new()
	_cam.fov = 70.0
	_cam.far = 2500.0
	add_child(_cam)
	_cam.make_current()
	_cam.position = _surf(_dir, 8.0) - _fwd * 12.0
	_cam.look_at(_surf(_dir, 2.0), _dir)

func _build_hud() -> void:
	_hud = CanvasLayer.new()
	_hud.layer = 18
	add_child(_hud)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_hud.add_child(root)
	_lbl_shards = Label.new()
	_lbl_shards.position = Vector2(24, 18)
	_lbl_shards.add_theme_font_size_override("font_size", 40)
	_lbl_shards.add_theme_color_override("font_color", Color(1.0, 0.95, 0.6))
	_lbl_shards.add_theme_color_override("font_outline_color", Color(0, 0, 0))
	_lbl_shards.add_theme_constant_override("outline_size", 8)
	root.add_child(_lbl_shards)
	_lbl_big = Label.new()
	_lbl_big.set_anchors_preset(Control.PRESET_FULL_RECT)
	_lbl_big.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_lbl_big.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_lbl_big.add_theme_font_size_override("font_size", 84)
	_lbl_big.add_theme_color_override("font_color", Color(1, 1, 1))
	_lbl_big.add_theme_color_override("font_outline_color", Color(0.1, 0.0, 0.2))
	_lbl_big.add_theme_constant_override("outline_size", 12)
	root.add_child(_lbl_big)
	_lbl_hint = Label.new()
	_lbl_hint.anchor_top = 1.0
	_lbl_hint.anchor_bottom = 1.0
	_lbl_hint.position = Vector2(24, -56)
	_lbl_hint.add_theme_font_size_override("font_size", 26)
	_lbl_hint.add_theme_color_override("font_color", Color(0.92, 0.9, 1.0))
	_lbl_hint.add_theme_color_override("font_outline_color", Color(0, 0, 0))
	_lbl_hint.add_theme_constant_override("outline_size", 6)
	root.add_child(_lbl_hint)
	_update_shard_hud()

func _update_shard_hud() -> void:
	_lbl_shards.text = "🦋 %d / %d" % [_shards_got, SHARDS]

# ---------------------------------------------------------------- input
func _move_input() -> Vector2:
	# x = turn, y = forward
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
	# moons orbit; shards spin & bob
	for md in _moons:
		var ph: float = tt * float(md["spd"]) + float(md["ph"])
		var tilt: float = float(md["tilt"])
		(md["node"] as Node3D).position = ORIGIN + Vector3(cos(ph) * float(md["r"]), sin(ph * 0.7) * float(md["r"]) * tilt * 0.4, sin(ph) * float(md["r"]))
	# ---- ambient butterflies flutter around the garden (feast when called) ----
	for fd in _flyers:
		var bn: Node3D = fd["node"]
		var ang2: float = tt * float(fd["spd"]) + float(fd["ph"])
		var pdir: Vector3 = ((fd["dir0"] as Vector3).rotated(fd["axis"], ang2)).normalized()
		var alt: float = float(fd["alt"]) + sin(tt * 1.3 + float(fd["ph"])) * 0.8
		var ft: float = float(fd.get("feast_t", 0.0))
		if ft > 0.0:
			fd["feast_t"] = ft - delta
			var fdir: Vector3 = fd["feast_dir"]
			var swirl: Vector3 = (fdir.cross(Vector3.UP) if absf(fdir.dot(Vector3.UP)) < 0.95 else fdir.cross(Vector3.RIGHT)).normalized()
			pdir = (fdir + swirl.rotated(fdir, ang2 * 6.0) * 0.09).normalized()
			alt = 1.4 + sin(tt * 5.0 + float(fd["ph"])) * 0.5
		var newp: Vector3 = _surf(pdir, alt)
		var vel2: Vector3 = newp - bn.position
		bn.position = newp
		if vel2.length() > 0.01:
			bn.look_at(newp + vel2, pdir)
		bn.scale = Vector3(1.0 + 0.28 * sin(tt * float(fd["flap"])), 1.0, 1.0)
	# beetles + ladybugs crawl slowly along the garden (poke one — it chirps!)
	for bd2 in _bugs:
		bd2["cool"] = maxf(0.0, float(bd2["cool"]) - delta)
		var bn2: Node3D = bd2["node"]
		var bang2: float = tt * float(bd2["spd"]) + float(bd2["ph"])
		var bdir2: Vector3 = ((bd2["dir0"] as Vector3).rotated(bd2["axis"], bang2)).normalized()
		var prevbp: Vector3 = bn2.position
		var newbp: Vector3 = _surf(bdir2, 0.1)
		var bvel: Vector3 = newbp - prevbp
		bn2.position = newbp
		if bvel.length() > 0.001:
			bn2.look_at(newbp + bvel, bdir2)
		if float(bd2["cool"]) <= 0.0 and _h < 1.5 and _mode == "planet" and newbp.distance_to(_surf(_dir, _h)) < 3.2:
			bd2["cool"] = 3.0
			_chime(1.05 + randf() * 0.2)
			if _main != null and _main.has_method("_sparkle_burst"):
				_main._sparkle_burst(newbp + bdir2 * 1.5, Color(0.6, 1.0, 0.6))
	# stand still a moment and a butterfly comes to say hello
	if _idle_t > 2.5 and not _flyers.is_empty():
		var visitor: Node3D = (_flyers[0] as Dictionary)["node"]
		visitor.position = visitor.position.lerp(_surf(_dir, 3.0 + sin(tt * 2.0) * 0.3), minf(1.0, delta * 2.5))
	# Mermaid Rosalina floats gently and greets Roshan
	if _rosalina != null and is_instance_valid(_rosalina):
		_rosalina.position = _surf(Vector3(0.16, 1.0, 0.13).normalized(), 4.0 + sin(tt * 1.4) * 0.5)
		_rosa_cool = maxf(0.0, _rosa_cool - delta)
		if _rosa_cool <= 0.0 and _mode == "planet" and _rosalina.position.distance_to(_surf(_dir, _h)) < 8.0:
			_rosa_cool = 16.0
			_chime(1.15)
			if _main != null and _main.has_method("show_msg"):
				_main.show_msg("Mermaid Rosalina", "Welcome to my crystal castle, little star! Bring my baby butterflies home!", "greet")
	# ---- fruit trays: stand close and the whole swarm dives in to feast ----
	for td in _trays:
		td["cool"] = maxf(0.0, float(td["cool"]) - delta)
		if float(td["cool"]) <= 0.0 and _h < 2.0 and _state == "play" and _mode == "planet":
			var tang: float = _dir.angle_to(td["dir"]) * PLANET_R
			if tang < 4.5:
				td["cool"] = 9.0
				_chime(1.2)
				for fd2 in _flyers:
					fd2["feast_t"] = 3.0
					fd2["feast_dir"] = td["dir"]
				if _main != null and _main.has_method("_sparkle_burst"):
					_main._sparkle_burst(_surf(td["dir"], 2.5), Color(1.0, 0.9, 0.5))
				if _main != null and "pearl_count" in _main:
					_main.pearl_count += 1
					if _main.has_method("_update_hud"):
						_main._update_hud()
				if _lbl_hint != null:
					_lbl_hint.text = "The butterflies LOVE the fruit!  +1 pearl"
	for sd in _shard_nodes:
		if bool(sd["got"]):
			continue
		var n: Node3D = sd["node"]
		n.position = _surf(sd["dir"], 2.6 + sin(tt * 2.0 + float(sd["ph"])) * 0.6)
	if _grand != null and _grand_active:
		_grand.position = _surf(Vector3.UP, 9.0 + sin(tt * 1.5) * 1.0)
		_grand.rotate_y(delta * 1.2)
	if _state == "won":
		_won_t -= delta
		if fmod(_won_t, 0.3) < delta and _main != null and _main.has_method("_sparkle_burst"):
			_main._sparkle_burst(_surf(_dir, 4.0 + randf() * 6.0), Color.from_hsv(randf(), 0.5, 1.0))
		if _won_t <= 0.0:
			_teardown(true)
		return
	if _mode == "hall":
		_tick_hall(delta)
		return
	# ---- movement on the sphere ----
	var mv := _move_input()
	# turn: rotate facing around the radial axis
	if absf(mv.x) > 0.01:
		_fwd = _fwd.rotated(_dir, -mv.x * TURN_SPD * delta)
		_project_fwd()
	# run: slide the surface direction along the facing great-circle
	if absf(mv.y) > 0.01:
		var step: float = mv.y * RUN_SPD * delta / PLANET_R   # angle along the great circle
		var new_dir := (_dir.rotated(_fwd.cross(_dir).normalized(), -step)).normalized()
		_dir = new_dir
		_project_fwd()
	# soft collision with the crystal gardens: push Roshan back to a crystal's
	# rim along the same great circle (jumping high enough clears them)
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
						_chime(0.9 + fposmod(bdir.x * 7.0, 0.5))   # each crystal sings its own note
						if _main != null and _main.has_method("_sparkle_burst"):
							_main._sparkle_burst(_surf(bdir, 3.0), Color(0.8, 0.7, 1.0))
	# star bounce pads: step on one and WHEEE
	for pd in _pads:
		pd["cool"] = maxf(0.0, float(pd["cool"]) - delta)
		if _h < 0.6 and float(pd["cool"]) <= 0.0:
			var pang: float = _dir.angle_to(pd["dir"]) * PLANET_R
			if pang < 3.4:
				pd["cool"] = 1.0
				_vy = JUMP_V * 1.9
				_h = maxf(_h, 0.06)
				_chime(1.4)
				if _main != null and _main.has_method("_sparkle_burst"):
					_main._sparkle_burst(_surf(_dir, 2.0), Color(1.0, 0.9, 0.4))
	# the castle gate: step into the glowing ring to enter the Star Hall
	_gate_cool = maxf(0.0, _gate_cool - delta)
	if _gate_cool <= 0.0 and _h < 1.5 and _dir.angle_to(GATE_DIR.normalized()) * PLANET_R < 4.5:
		_enter_hall()
		return
	# idle timer (a butterfly visits Roshan when she stands still)
	if absf(mv.x) < 0.05 and absf(mv.y) < 0.05 and _h <= 0.05:
		_idle_t += delta
	else:
		_idle_t = 0.0
	# jump / gravity (radial)
	if _jump_pressed() and _h <= 0.05:
		_vy = JUMP_V
		if _main != null and _main.has_method("_sparkle_burst"):
			_main._sparkle_burst(_surf(_dir, 1.0), Color(0.8, 0.9, 1.0))
	_vy -= GRAV * delta
	_h = maxf(0.0, _h + _vy * delta)
	if _h <= 0.0:
		_vy = 0.0
	_update_avatar_transform()
	# ---- camera: behind & above along the local up ----
	var up := _dir
	var want: Vector3 = _surf(_dir, _h + 7.5) - _fwd * 13.0
	_cam.position = _cam.position.lerp(want, clampf(delta * 5.0, 0.0, 1.0))
	_cam.look_at(_surf(_dir, _h + 2.2) + _fwd * 3.0, up)
	# ---- pickups ----
	var feet := _surf(_dir, _h)
	for sd in _shard_nodes:
		if bool(sd["got"]):
			continue
		if ((sd["node"] as Node3D).position).distance_to(feet) < 5.0:
			sd["got"] = true
			(sd["node"] as Node3D).visible = false
			if sd.get("beam") != null and is_instance_valid(sd["beam"]):
				(sd["beam"] as Node3D).visible = false
			_shards_got += 1
			_update_shard_hud()
			_chime(0.7 + 0.06 * float(_shards_got))
			if _main != null and _main.has_method("_sparkle_burst"):
				_main._sparkle_burst(feet + up * 2.0, Color(1.0, 0.95, 0.5))
			if _shards_got == SHARDS - 1:
				# one left: super-size its beacon so it dominates the horizon
				for sd2 in _shard_nodes:
					if not bool(sd2["got"]) and sd2.get("beam") != null and is_instance_valid(sd2["beam"]):
						(sd2["beam"] as Node3D).scale = Vector3(3.2, 2.2, 3.2)
						var bmm: StandardMaterial3D = (sd2["beam"] as MeshInstance3D).material_override
						if bmm != null:
							bmm.albedo_color.a = 0.55
				if _lbl_hint != null:
					_lbl_hint.text = "ONE butterfly left — follow the GIANT beacon!"
			if _shards_got >= SHARDS and not _grand_active:
				_spawn_grand_star()
	if _grand_active and _grand != null and _grand.position.distance_to(feet) < 7.0:
		_grand_active = false
		_grand.visible = false
		_win()
	if _home_pos.distance_to(feet) < 5.5:
		_teardown(false)

# ---------------------------------------------------------------- Star Hall
func _build_hall() -> void:
	# the castle interior: a round amethyst-glass hall floating high above the
	# planet. Same IDEA as the Pearl Castle's grand hall, different soul —
	# crystal + starlight instead of stone + red carpet, and the galaxy glitters
	# straight through the translucent floor.
	_hall_built = true
	_hall_root = Node3D.new()
	_hall_root.position = HALL_C
	add_child(_hall_root)
	var floor := MeshInstance3D.new()
	var fcm := CylinderMesh.new()
	fcm.top_radius = 26.0
	fcm.bottom_radius = 26.0
	fcm.height = 1.0
	floor.mesh = fcm
	var fmat := StandardMaterial3D.new()
	fmat.albedo_color = Color(0.72, 0.66, 0.95, 0.6)
	fmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	fmat.emission_enabled = true
	fmat.emission = Color(0.5, 0.45, 0.85)
	fmat.emission_energy_multiplier = 0.25
	fmat.roughness = 0.12
	fmat.metallic = 0.3
	floor.material_override = fmat
	_hall_root.add_child(floor)
	# star rug in the middle
	var rug := MeshInstance3D.new()
	var rcm := CylinderMesh.new()
	rcm.top_radius = 8.0
	rcm.bottom_radius = 8.0
	rcm.height = 0.2
	rug.mesh = rcm
	var rmat := StandardMaterial3D.new()
	rmat.albedo_color = Color(0.30, 0.22, 0.55)
	rmat.emission_enabled = true
	rmat.emission = Color(0.6, 0.5, 1.0)
	rmat.emission_energy_multiplier = 0.2
	rug.material_override = rmat
	rug.position = Vector3(0, 0.6, 0)
	_hall_root.add_child(rug)
	# amethyst-glass wall panels (door gap at +z)
	for i in range(12):
		if i == 0:
			continue   # the doorway
		var pa: float = (float(i) + 0.5) / 12.0 * TAU
		var wp := MeshInstance3D.new()
		var wbm := BoxMesh.new()
		wbm.size = Vector3(13.0, 13.0, 1.0)
		wp.mesh = wbm
		var wmat := StandardMaterial3D.new()
		wmat.albedo_color = Color(0.68, 0.62, 0.95, 0.35)
		wmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		wmat.emission_enabled = true
		wmat.emission = Color(0.55, 0.5, 0.9)
		wmat.emission_energy_multiplier = 0.3
		wp.material_override = wmat
		wp.position = Vector3(sin(pa) * 25.0, 6.5, cos(pa) * 25.0)
		wp.rotation.y = pa
		_hall_root.add_child(wp)
	# crystal columns
	for i in range(6):
		var cpath: String = CRYSTALS[i % CRYSTALS.size()]
		if not ResourceLoader.exists(cpath):
			continue
		var col: Node3D = (load(cpath) as PackedScene).instantiate()
		var chh := Node3D.new()
		_hall_root.add_child(chh)
		chh.add_child(col)
		_fit_small(col, 3.4)
		var ca: float = float(i) / 6.0 * TAU + 0.26
		chh.position = Vector3(sin(ca) * 18.0, 0.5, cos(ca) * 18.0)
		_tint_meshes(col, Color(0.8, 0.7, 1.0), 0.5)
	# star chandeliers
	for i in range(3):
		var star := Label3D.new()
		star.text = "★"
		star.font_size = 240
		star.pixel_size = 0.03
		star.outline_size = 22
		star.modulate = Color(1.0, 0.92, 0.55)
		star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		star.position = Vector3(sin(float(i) * TAU / 3.0) * 9.0, 10.0, cos(float(i) * TAU / 3.0) * 9.0)
		_hall_root.add_child(star)
		var sl := OmniLight3D.new()
		sl.light_color = Color(1.0, 0.9, 0.6)
		sl.light_energy = 1.6
		sl.omni_range = 20.0
		sl.position = star.position
		_hall_root.add_child(sl)
	# the Moon Throne at the back, Rosalina's indoor seat
	var seat := MeshInstance3D.new()
	var scm := SphereMesh.new()
	scm.radius = 2.6
	scm.height = 2.6
	seat.mesh = scm
	var smat := StandardMaterial3D.new()
	smat.albedo_color = Color(0.95, 0.93, 1.0)
	smat.emission_enabled = true
	smat.emission = Color(0.85, 0.85, 1.0)
	smat.emission_energy_multiplier = 0.5
	seat.material_override = smat
	seat.position = Vector3(0, 1.6, -20.0)
	_hall_root.add_child(seat)
	if ResourceLoader.exists("res://assets/characters/skins/fairy_mermaid.png"):
		var rosa2 := Sprite3D.new()
		var rtex2: Texture2D = load("res://assets/characters/skins/fairy_mermaid.png")
		rosa2.texture = rtex2
		rosa2.pixel_size = 6.5 / maxf(float(rtex2.get_height()), 1.0)
		rosa2.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		rosa2.position = Vector3(0, 5.6, -20.0)
		_hall_root.add_child(rosa2)
	# three star bells (play a note when touched)
	for i in range(3):
		var bell := Label3D.new()
		bell.text = "★"
		bell.font_size = 170
		bell.pixel_size = 0.03
		bell.outline_size = 18
		bell.modulate = [Color(1.0, 0.5, 0.6), Color(0.5, 0.9, 1.0), Color(0.7, 1.0, 0.6)][i]
		bell.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		var bpos := Vector3(14.0, 2.2, -6.0 + float(i) * 6.0)
		bell.position = bpos
		_hall_root.add_child(bell)
		_bells.append({"node": bell, "pos": HALL_C + bpos, "cool": 0.0, "pitch": 0.7 + float(i) * 0.18})
	# the wish fountain (+2 pearls, slow cooldown)
	var fring := MeshInstance3D.new()
	var ftm := TorusMesh.new()
	ftm.inner_radius = 1.8
	ftm.outer_radius = 2.6
	fring.mesh = ftm
	var fmat2 := StandardMaterial3D.new()
	fmat2.albedo_color = Color(0.5, 0.85, 1.0)
	fmat2.emission_enabled = true
	fmat2.emission = Color(0.4, 0.8, 1.0)
	fmat2.emission_energy_multiplier = 1.2
	fring.material_override = fmat2
	fring.position = Vector3(-14.0, 1.0, -2.0)
	_hall_root.add_child(fring)
	var flab := Label3D.new()
	flab.text = "wish fountain"
	flab.font_size = 40
	flab.pixel_size = 0.025
	flab.outline_size = 10
	flab.modulate = Color(0.7, 0.9, 1.0)
	flab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	flab.position = Vector3(-14.0, 4.4, -2.0)
	_hall_root.add_child(flab)
	# doorway arch + label
	var arch := MeshInstance3D.new()
	var atm := TorusMesh.new()
	atm.inner_radius = 3.2
	atm.outer_radius = 4.0
	arch.mesh = atm
	arch.material_override = fmat2
	arch.position = Vector3(0, 3.4, 24.6)
	_hall_root.add_child(arch)
	var dlab := Label3D.new()
	dlab.text = "back to the garden"
	dlab.font_size = 44
	dlab.pixel_size = 0.025
	dlab.outline_size = 10
	dlab.modulate = Color(0.8, 1.0, 0.85)
	dlab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	dlab.position = Vector3(0, 8.0, 24.6)
	_hall_root.add_child(dlab)
	# indoor butterflies circling the chandeliers
	for i in range(4):
		var bf := _make_butterfly(WING_COLS[(i * 2) % WING_COLS.size()], 1.8)
		_hall_root.add_child(bf)
		_hall_flies.append({"node": bf, "r": 6.0 + float(i) * 2.5, "spd": 0.5 + randf() * 0.4, "ph": randf() * TAU, "h": 5.0 + float(i) * 1.4})

func _enter_hall() -> void:
	if not _hall_built:
		_build_hall()
	_mode = "hall"
	_cpos = Vector3(0, 0, 21.0)
	_cyaw = PI
	_ch = 0.0
	_cvy = 0.0
	_chime(1.2)
	if _lbl_hint != null:
		_lbl_hint.text = "The STAR HALL!  •  ring the star bells — make a wish at the fountain!"
	if _main != null and _main.has_method("show_msg"):
		_main.show_msg("Mermaid Rosalina", "Come in, come in! This is my Star Hall — the whole galaxy shines under the floor!", "greet")

func _exit_hall() -> void:
	_mode = "planet"
	_gate_cool = 2.0
	_dir = Vector3(0.55, 1.0, 0.0).normalized()
	_project_fwd()
	_h = 0.0
	_vy = 0.0
	if _lbl_hint != null:
		_lbl_hint.text = "Find the 7 lost butterflies — follow their beacons!  •  fruit trays call the swarm!"

func _tick_hall(delta: float) -> void:
	var mv := _move_input()
	if absf(mv.x) > 0.01:
		_cyaw -= mv.x * TURN_SPD * delta
	var fwd := Vector3(sin(_cyaw), 0.0, cos(_cyaw))
	if absf(mv.y) > 0.01:
		_cpos += fwd * mv.y * RUN_SPD * delta
	var rr: float = Vector2(_cpos.x, _cpos.z).length()
	if rr > 23.5:
		_cpos.x *= 23.5 / rr
		_cpos.z *= 23.5 / rr
	if _jump_pressed() and _ch <= 0.05:
		_cvy = JUMP_V * 0.85
	_cvy -= GRAV * delta
	_ch = maxf(0.0, _ch + _cvy * delta)
	if _ch <= 0.0:
		_cvy = 0.0
	if _avatar != null:
		_avatar.position = HALL_C + _cpos + Vector3(0, 0.5 + _ch + sin(_bob_t * 3.0) * 0.1, 0)
		_avatar.transform.basis = Basis(fwd.cross(Vector3.UP).normalized(), Vector3.UP, -fwd).orthonormalized()
	if _cam != null:
		var want: Vector3 = HALL_C + _cpos + Vector3(0, _ch + 6.5, 0) - fwd * 11.5
		_cam.position = _cam.position.lerp(want, clampf(delta * 5.0, 0.0, 1.0))
		_cam.look_at(HALL_C + _cpos + Vector3(0, _ch + 2.2, 0) + fwd * 3.0, Vector3.UP)
	var tt: float = Time.get_ticks_msec() / 1000.0
	for hf in _hall_flies:
		var n3: Node3D = hf["node"]
		var ha: float = tt * float(hf["spd"]) + float(hf["ph"])
		var hp := Vector3(cos(ha) * float(hf["r"]), float(hf["h"]) + sin(tt * 1.8 + float(hf["ph"])) * 0.6, sin(ha) * float(hf["r"]))
		var hv: Vector3 = (HALL_C + hp) - n3.position
		n3.position = HALL_C + hp
		if hv.length() > 0.01:
			n3.look_at(n3.position + hv, Vector3.UP)
		n3.scale = Vector3(1.0 + 0.28 * sin(tt * 14.0), 1.0, 1.0)
	var feet: Vector3 = HALL_C + _cpos + Vector3(0, 0.5, 0)
	for b in _bells:
		b["cool"] = maxf(0.0, float(b["cool"]) - delta)
		if float(b["cool"]) <= 0.0 and (b["pos"] as Vector3).distance_to(feet) < 3.4:
			b["cool"] = 0.5
			_chime(float(b["pitch"]))
			var bn: Label3D = b["node"]
			var tw2 := bn.create_tween()
			tw2.tween_property(bn, "scale", Vector3.ONE * 1.5, 0.08)
			tw2.tween_property(bn, "scale", Vector3.ONE, 0.2)
	_fount_cool = maxf(0.0, _fount_cool - delta)
	if _fount_cool <= 0.0 and feet.distance_to(HALL_C + Vector3(-14.0, 1.0, -2.0)) < 3.6:
		_fount_cool = 20.0
		_chime(1.35)
		if _main != null and _main.has_method("_sparkle_burst"):
			_main._sparkle_burst(HALL_C + Vector3(-14.0, 3.0, -2.0), Color(0.6, 0.9, 1.0))
		if _main != null and "pearl_count" in _main:
			_main.pearl_count += 2
			if _main.has_method("_update_hud"):
				_main._update_hud()
		if _main != null and _main.has_method("show_msg"):
			_main.show_msg("Mermaid Rosalina", "Your wish sparkles true! +2 pearls!", "win")
	# the doorway back out
	if _cpos.z > 21.5 and absf(_cpos.x) < 7.0:
		_exit_hall()

func _chime(pitch: float) -> void:
	if _main != null and "chime" in _main and _main.chime != null:
		_main.chime.pitch_scale = pitch
		_main.chime.play()

func _win() -> void:
	_state = "won"
	_won_t = 4.0
	_lbl_big.text = "⭐ YOU SAVED\nROSHAN GALAXY! ⭐"
	_lbl_hint.text = "+40 pearls for your treasure!"
	if _main != null and "pearl_count" in _main:
		_main.pearl_count += 40
		if _main.has_method("_write_save"):
			_main._write_save()
	_chime(1.0)

func _teardown(completed: bool) -> void:
	_state = "done"
	if _prev_env != null and "we_node" in _main and _main.we_node != null:
		_main.we_node.environment = _prev_env
	if _player_node != null and "cam" in _player_node and _player_node.cam != null:
		(_player_node.cam as Camera3D).make_current()
	if _finish_cb.is_valid():
		_finish_cb.call(completed)
	queue_free()
