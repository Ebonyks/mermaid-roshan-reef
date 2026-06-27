extends Node3D
class_name KartGame
# ============================================================================
# Rainbow Road kart racer (N64-Rainbow-Road inspired) — Mermaid Roshan's rainbow
# go-kart vs. Faron, Harper, Fiona, Gabby, Kareem, Lamb-a' and Chuck.
#
# Self-contained: builds its own neon rainbow track high in the sky, its own
# karts, camera, starfield environment and HUD, runs its own physics/AI in
# _process, and calls a finish callback back into main.gd. Nothing here touches
# the reef, so it can't break the overworld.
#
# Karts drive on an ARC-LENGTH spline: each kart has a distance `s` along the
# loop + a lateral offset `lat`. Steering moves `lat`, accelerator/brake move
# `s`. This is robust (no physics collisions to misbehave) and gives a proper
# Mario-Kart feel with constant-speed AI and a hidden shortcut.
#
# Launch:   var k := KartGame.new(); main.add_child(k); k.start(main, on_finish)
# Finish:   calls on_finish.call(placement:int)  (1 = first place)
# ============================================================================

const LAPS := 2
const LAP_TARGET_SEC := 30.0      # tunes total race into the ~45-60s window (more zips = more boost)
const ROAD_HALF := 11.0           # half-width of the rainbow ribbon
const COLLIDE_R := 4.5            # kart-vs-kart bump radius
const WALL_SLOW := 0.82           # speed kept when you scrape a wall (bouncy + slows you)
const SAMPLES := 260              # spline samples for the arc-length table
const ORIGIN := Vector3(0.0, 4000.0, 0.0)   # far above the reef so nothing else is in frame

# control points of the looping rainbow road (relative to ORIGIN); gentle ups/downs
const CTRL := [
	Vector3(0, 0, 150),
	Vector3(70, 6, 132),
	Vector3(122, 18, 72),      # climb to a crest
	Vector3(142, 16, -8),
	Vector3(112, 4, -78),      # swoop down
	Vector3(64, -8, -120),     # dip into a valley
	Vector3(-8, -6, -150),
	Vector3(-84, 8, -118),
	Vector3(-138, 22, -48),    # the big hill
	Vector3(-122, 14, 26),
	Vector3(-70, 0, 92),
	Vector3(-30, 12, 132),     # rolling rise back to the line
]
# the slightly-hidden shortcut: a side gate on the inside of the far bend that
# warps the player across the long loop (only the player can take it).
const SHORTCUT_FROM_U := 0.34
const SHORTCUT_TO_U := 0.50

# boosts: zoom strips on the road + collectible items (kept mild so the race stays ~45-60s)
const BOOST_MUL := 0.5          # +50% top speed while boosting
const STRIP_BOOST := 0.7        # seconds of boost from a zoom strip
const SHELL_BOOST := 1.1        # mermaid spiral-shell pickup
const STAR_BOOST := 1.7         # star pickup (bigger, longer)
# zoom strips: u-fraction along the loop, lateral offset, arc length, half-width
const STRIPS := [
	{"u": 0.08, "lat": 0.0, "len": 16.0, "hw": 7.0},
	{"u": 0.20, "lat": 5.0, "len": 14.0, "hw": 7.0},
	{"u": 0.34, "lat": -5.0, "len": 14.0, "hw": 7.0},
	{"u": 0.50, "lat": 0.0, "len": 16.0, "hw": 7.0},
	{"u": 0.62, "lat": -4.0, "len": 16.0, "hw": 7.0},
	{"u": 0.78, "lat": 4.0, "len": 14.0, "hw": 7.0},
	{"u": 0.92, "lat": 0.0, "len": 16.0, "hw": 7.0},
]
# pickups: u-fraction, lateral offset, kind ("shell" | "star")
const PICKUPS := [
	{"u": 0.22, "lat": -5.0, "kind": "shell"},
	{"u": 0.45, "lat": 5.0, "kind": "star"},
	{"u": 0.72, "lat": 0.0, "kind": "shell"},
	{"u": 0.93, "lat": -3.0, "kind": "star"},
]
const SHELL_GLB := "res://assets/aquatic/SpiralShell.glb"

# racer roster: name, kart colour, driver sprite (falls back to a coloured head)
const RACERS := [
	{"name": "Roshan", "col": Color(1.0, 0.4, 0.8), "sprite": "res://assets/characters/roshan_sprite.png", "player": true},
	{"name": "Faron", "col": Color(0.45, 0.85, 1.0), "sprite": "res://assets/characters/friends/mama_baby.png"},
	{"name": "Harper", "col": Color(1.0, 0.55, 0.3), "sprite": "res://assets/characters/friends/two_friends.png"},
	{"name": "Fiona", "col": Color(1.0, 0.8, 0.35), "sprite": "res://assets/characters/friends/two_friends.png"},
	{"name": "Gabby", "col": Color(0.6, 0.4, 1.0), "sprite": "res://assets/characters/friends/gabby.png"},
	{"name": "Kareem", "col": Color(0.35, 0.9, 0.5), "sprite": "res://assets/characters/friends/kareem.png"},
	{"name": "Lamb-a'", "col": Color(0.95, 0.95, 1.0), "sprite": "res://assets/characters/friends/pearl_friend.png"},
	{"name": "Chuck", "col": Color(0.5, 0.55, 0.6), "sprite": "res://assets/characters/friends/wacky_chuck.png"},
]

var _main: Node = null
var _player_node: Node3D = null
var _finish_cb: Callable
var _cam: Camera3D = null
var _prev_env: Environment = null
var _hud: CanvasLayer = null
var _lbl_place: Label = null
var _lbl_lap: Label = null
var _lbl_big: Label = null

var _lut: PackedVector3Array = []   # sampled centreline points (world)
var _cum: PackedFloat32Array = []   # cumulative arc length at each sample
var _len := 0.0                     # total loop length
var _vmax := 40.0

var _karts: Array = []              # each: {node, name, is_player, s, lat, speed, ai, boost}
var _pl = null                      # the player's kart dict
var _strip_data: Array = []         # {s, lat, len, hw}
var _pickups_live: Array = []       # {node, s, lat, kind, cool}
var _state := "countdown"           # countdown -> race -> done
var _clock := 0.0
var _race_t := 0.0
var _shortcut_used_lap := -1
var _rev := false                   # reversed track (entered via the rainbow's other half)

# ---------------------------------------------------------------- spline maths
func _catmull(p0: Vector3, p1: Vector3, p2: Vector3, p3: Vector3, t: float) -> Vector3:
	var t2 := t * t
	var t3 := t2 * t
	return 0.5 * ((2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2 + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3)

func _spline_u(u: float) -> Vector3:
	var n := CTRL.size()
	var f: float = fposmod(u, 1.0) * float(n)
	var i: int = int(floor(f))
	var t: float = f - float(i)
	var p0: Vector3 = CTRL[(i - 1 + n) % n]
	var p1: Vector3 = CTRL[i % n]
	var p2: Vector3 = CTRL[(i + 1) % n]
	var p3: Vector3 = CTRL[(i + 2) % n]
	return ORIGIN + _catmull(p0, p1, p2, p3, t)

func _build_lut() -> void:
	_lut = PackedVector3Array()
	_cum = PackedFloat32Array()
	var prev := _spline_u(0.0)
	var d := 0.0
	for i in range(SAMPLES + 1):
		var u := float(i) / float(SAMPLES)
		var p := _spline_u(u)
		if i > 0:
			d += prev.distance_to(p)
		_lut.append(p)
		_cum.append(d)
		prev = p
	_len = d
	_vmax = _len / LAP_TARGET_SEC

func _pos_at(s: float) -> Vector3:
	var ss := fposmod(s, _len)
	# linear search the cumulative table (SAMPLES small; fine per-frame for 8 karts)
	var i := 0
	while i < SAMPLES and _cum[i + 1] < ss:
		i += 1
	var seg: float = _cum[i + 1] - _cum[i]
	var t: float = 0.0 if seg <= 0.0001 else (ss - _cum[i]) / seg
	return _lut[i].lerp(_lut[i + 1], t)

func _tangent_at(s: float) -> Vector3:
	var a := _pos_at(s)
	var b := _pos_at(s + 2.0)
	var dir := b - a
	if dir.length() < 0.001:
		return Vector3.FORWARD
	return dir.normalized()

func _width_at(s: float) -> float:
	# road half-width varies along the loop -> narrow & wide sections
	var u := fposmod(s, _len) / _len
	return ROAD_HALF * (1.0 + 0.32 * sin(u * TAU * 2.0))

func _bank_at(s: float) -> float:
	# roll the road into turns, proportional to how fast the heading turns
	var t0 := _tangent_at(s)
	var t1 := _tangent_at(s + 6.0)
	return clampf(t0.cross(t1).y * 7.0, -0.45, 0.45)

func _frame_at(s: float, lat: float) -> Array:
	var fwd := _tangent_at(s)
	var flat_right := fwd.cross(Vector3.UP).normalized()
	var bank := _bank_at(s)
	var right := flat_right.rotated(fwd, bank)
	var up := Vector3.UP.rotated(fwd, bank)
	var pos := _pos_at(s) + right * lat
	return [pos, fwd, right, up]

func _eff(s: float) -> float:
	# map a kart's ever-increasing distance to a sampling point; mirror it when reversed
	var m := fposmod(s, _len)
	return (_len - m) if _rev else m

func _kart_frame(s: float, lat: float) -> Array:
	# kart placement/facing — honours reversed travel (track mesh itself is built forward)
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

# ---------------------------------------------------------------- build
func start(main: Node, finish_cb: Callable, reversed: bool = false) -> void:
	_main = main
	_finish_cb = finish_cb
	_rev = reversed
	if "player" in main and main.player != null:
		_player_node = main.player
	_build_lut()
	_build_sky()
	_build_track()
	_build_strips()
	_build_pickups()
	_build_karts()
	_build_camera()
	_build_hud()
	_state = "countdown"
	_clock = 3.999

func _build_sky() -> void:
	# swap the world environment to a starry Rainbow-Road void; restore on exit
	if "we_node" in _main and _main.we_node != null:
		_prev_env = _main.we_node.environment
		var e := Environment.new()
		e.background_mode = Environment.BG_COLOR
		e.background_color = Color(0.02, 0.01, 0.06)
		e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		e.ambient_light_color = Color(0.5, 0.5, 0.7)
		e.ambient_light_energy = 0.9
		e.glow_enabled = true
		e.glow_intensity = 0.5
		_main.we_node.environment = e
	# starfield: a big inverted sphere with a procedural star shader
	var sky := MeshInstance3D.new()
	var sm := SphereMesh.new(); sm.radius = 900.0; sm.height = 1800.0; sm.flip_faces = true
	sky.mesh = sm
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode unshaded, cull_front;
float h(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5); }
void fragment(){
	vec2 uv = UV * vec2(220.0, 120.0);
	vec2 c = floor(uv); vec2 f = fract(uv);
	float r = h(c);
	float star = step(0.992, r) * smoothstep(0.18, 0.0, length(f - 0.5));
	vec3 sky = mix(vec3(0.02,0.01,0.08), vec3(0.10,0.04,0.20), UV.y);
	ALBEDO = sky + vec3(star);
	EMISSION = vec3(star) * 1.5;
}"""
	var smat := ShaderMaterial.new(); smat.shader = sh
	sky.material_override = smat
	sky.position = ORIGIN
	add_child(sky)

func _build_track() -> void:
	# rainbow ribbon
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
		st.set_uv(Vector2(0.0, v)); st.add_vertex(l - ORIGIN)
		st.set_uv(Vector2(1.0, v)); st.add_vertex(r - ORIGIN)
	for i in range(SAMPLES):
		var a := i * 2
		st.add_index(a); st.add_index(a + 1); st.add_index(a + 3)
		st.add_index(a); st.add_index(a + 3); st.add_index(a + 2)
	var mesh := st.commit()
	var road := MeshInstance3D.new()
	road.mesh = mesh
	var rsh := Shader.new()
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
	ALBEDO = c;
	EMISSION = c * (0.5 + 0.4*sin(TIME*2.0 + UV.y*40.0));
	ROUGHNESS = 0.4;
}"""
	var rmat := ShaderMaterial.new(); rmat.shader = rsh
	road.material_override = rmat
	road.position = ORIGIN
	add_child(road)
	# glowing edge rails
	for sgn: float in [1.0, -1.0]:
		var rail := MeshInstance3D.new()
		var rst := SurfaceTool.new(); rst.begin(Mesh.PRIMITIVE_TRIANGLES)
		for i in range(SAMPLES + 1):
			var s: float = (_cum[i] if i < _cum.size() else _len)
			var fr := _frame_at(s, 0.0)
			var right: Vector3 = fr[2]
			var rup: Vector3 = fr[3]
			var edge: Vector3 = _pos_at(s) - ORIGIN + right * (_width_at(s) * sgn)
			rst.add_vertex(edge); rst.add_vertex(edge + rup * 1.8)
		for i in range(SAMPLES):
			var a := i * 2
			rst.add_index(a); rst.add_index(a + 1); rst.add_index(a + 3)
			rst.add_index(a); rst.add_index(a + 3); rst.add_index(a + 2)
		rail.mesh = rst.commit()
		var em := StandardMaterial3D.new()
		em.albedo_color = Color(1.0, 1.0, 1.0)
		em.emission_enabled = true; em.emission = Color(0.7, 0.9, 1.0); em.emission_energy_multiplier = 2.0
		em.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		em.cull_mode = BaseMaterial3D.CULL_DISABLED
		rail.material_override = em
		rail.position = ORIGIN
		add_child(rail)
	# ---- big START/FINISH line with a rainbow dome over it (so the end is obvious) ----
	var sf := _frame_at(0.0, 0.0)
	var c0: Vector3 = sf[0]
	var ffwd: Vector3 = sf[1]
	var fright: Vector3 = sf[2]
	# checkered line across the road
	var line := MeshInstance3D.new()
	var lpm := PlaneMesh.new(); lpm.size = Vector2(ROAD_HALF * 2.0, 4.0)
	line.mesh = lpm
	var lsh := Shader.new()
	lsh.code = """shader_type spatial;
render_mode unshaded, cull_disabled;
void fragment(){
	vec2 g = floor(UV * vec2(10.0, 2.0));
	float chk = mod(g.x + g.y, 2.0);
	ALBEDO = vec3(chk);
	EMISSION = vec3(chk) * 0.3;
}"""
	var lmat := ShaderMaterial.new(); lmat.shader = lsh
	line.material_override = lmat
	line.transform = Transform3D(Basis(fright, Vector3.UP, ffwd).orthonormalized(), c0 + Vector3(0, 0.2, 0))
	add_child(line)
	# tall posts at the road edges
	for psgn: float in [1.0, -1.0]:
		var post := MeshInstance3D.new()
		var pbm := BoxMesh.new(); pbm.size = Vector3(1.4, 15.0, 1.4)
		post.mesh = pbm
		var pmat := StandardMaterial3D.new()
		pmat.albedo_color = Color(1, 1, 1); pmat.emission_enabled = true
		pmat.emission = Color(1, 1, 1); pmat.emission_energy_multiplier = 0.3
		post.material_override = pmat
		post.position = c0 + fright * (ROAD_HALF * psgn) + Vector3(0, 7.5, 0)
		add_child(post)
	# rainbow dome arching over the line (you drive through it)
	var dome := MeshInstance3D.new()
	var dtm := TorusMesh.new()
	dtm.inner_radius = ROAD_HALF + 1.0; dtm.outer_radius = ROAD_HALF + 4.0
	dtm.rings = 40; dtm.ring_segments = 18
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
	var dmat := ShaderMaterial.new(); dmat.shader = dsh
	dome.material_override = dmat
	dome.transform = Transform3D(Basis(fright, ffwd, Vector3.UP).orthonormalized(), c0 + Vector3(0, 1.0, 0))
	add_child(dome)
	# FINISH banner text
	var flab := Label3D.new()
	flab.text = "★ FINISH ★"; flab.font_size = 120; flab.outline_size = 22
	flab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	flab.modulate = Color(1.0, 0.95, 0.4)
	flab.position = c0 + Vector3(0, ROAD_HALF + 8.0, 0)
	add_child(flab)
	# the hidden shortcut gate (a glowing ring, set off the racing line on the inside)
	var gate_fr := _frame_at(SHORTCUT_FROM_U * _len, 0.0)
	# placed near the inside edge (reachable: karts steer to ~0.86*ROAD_HALF) so it's
	# slightly hidden off the racing line but you CAN tuck into it
	var gate_pos: Vector3 = (gate_fr[0] as Vector3) + (gate_fr[2] as Vector3) * (ROAD_HALF * 0.78)
	var ring := MeshInstance3D.new()
	var tm := TorusMesh.new(); tm.inner_radius = 3.5; tm.outer_radius = 5.0
	ring.mesh = tm
	var gmat := StandardMaterial3D.new()
	gmat.albedo_color = Color(0.7, 1.0, 0.9); gmat.emission_enabled = true
	gmat.emission = Color(0.4, 1.0, 0.7); gmat.emission_energy_multiplier = 1.6
	gmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	ring.material_override = gmat
	ring.position = gate_pos + Vector3(0, 3.0, 0)
	ring.rotation = Vector3(deg_to_rad(90), 0, 0)
	ring.visible = not _rev   # shortcut only exists on the forward course
	add_child(ring)
	set_meta("gate_pos", gate_pos)
	# ---- floating scenery for variety (rainbow crystals beside the track) ----
	for si2 in range(7):
		var su: float = float(si2) / 7.0
		var pf := _frame_at(su * _len, 0.0)
		var sp: Vector3 = pf[0]
		var rgt: Vector3 = pf[2]
		var side: float = 1.0 if si2 % 2 == 0 else -1.0
		var deco := MeshInstance3D.new()
		var dmsh := BoxMesh.new(); dmsh.size = Vector3(7, 7, 7)
		deco.mesh = dmsh
		var dcm := StandardMaterial3D.new()
		dcm.albedo_color = Color.from_hsv(su, 0.55, 1.0)
		dcm.emission_enabled = true; dcm.emission = dcm.albedo_color; dcm.emission_energy_multiplier = 0.6
		deco.material_override = dcm
		deco.position = sp + rgt * ((ROAD_HALF + 16.0) * side) + Vector3(0, 4.0 + sin(su * TAU) * 8.0, 0)
		deco.rotation = Vector3(su * 6.0, su * 4.0, su * 2.0)
		add_child(deco)

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
	for sd in STRIPS:
		var s0: float = float(sd["u"]) * _len
		var fr := _frame_at(s0 + float(sd["len"]) * 0.5, float(sd["lat"]))
		var pos: Vector3 = fr[0]
		var fwd: Vector3 = fr[1]
		var pm := PlaneMesh.new(); pm.size = Vector2(float(sd["hw"]) * 2.0, float(sd["len"]))
		var mi := MeshInstance3D.new(); mi.mesh = pm
		var mat := ShaderMaterial.new(); mat.shader = sh
		mi.material_override = mat
		mi.position = pos + Vector3(0, 0.18, 0)
		mi.rotation = Vector3(0, atan2(fwd.x, fwd.z), 0)
		add_child(mi)
		_strip_data.append({"pos": pos + Vector3(0, 1.0, 0), "len": float(sd["len"])})

func _build_pickups() -> void:
	for pd in PICKUPS:
		var s0: float = float(pd["u"]) * _len
		var fr := _frame_at(s0, float(pd["lat"]))
		var pos: Vector3 = fr[0]
		var holder := Node3D.new()
		holder.position = pos + Vector3(0, 2.6, 0)
		if String(pd["kind"]) == "shell" and ResourceLoader.exists(SHELL_GLB):
			var sm: Node3D = (load(SHELL_GLB) as PackedScene).instantiate()
			sm.scale = Vector3.ONE * 2.4
			holder.add_child(sm)
			var gl := OmniLight3D.new(); gl.light_color = Color(1.0, 0.7, 0.95); gl.light_energy = 2.0; gl.omni_range = 9.0
			holder.add_child(gl)
		else:
			var lab := Label3D.new()
			lab.text = ("🐚" if String(pd["kind"]) == "shell" else "★")
			lab.font_size = 180; lab.pixel_size = 0.03
			lab.modulate = (Color(1.0, 0.7, 0.95) if String(pd["kind"]) == "shell" else Color(1.0, 0.9, 0.3))
			lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			holder.add_child(lab)
			var gl2 := OmniLight3D.new(); gl2.light_color = lab.modulate; gl2.light_energy = 2.4; gl2.omni_range = 10.0
			holder.add_child(gl2)
		add_child(holder)
		_pickups_live.append({"node": holder, "s": s0, "lat": float(pd["lat"]), "kind": String(pd["kind"]), "cool": 0.0})

func _kart_body(col: Color, sprite_path: String, racer_name: String) -> Node3D:
	var root := Node3D.new()
	# chassis
	var chassis := MeshInstance3D.new()
	var cm := BoxMesh.new(); cm.size = Vector3(3.0, 1.0, 4.4)
	chassis.mesh = cm
	var mat := StandardMaterial3D.new(); mat.albedo_color = col
	mat.metallic = 0.2; mat.roughness = 0.5
	mat.emission_enabled = true; mat.emission = col; mat.emission_energy_multiplier = 0.25
	chassis.material_override = mat
	chassis.position = Vector3(0, 1.0, 0)
	root.add_child(chassis)
	# wheels
	for wx: float in [-1.7, 1.7]:
		for wz: float in [-1.6, 1.6]:
			var w := MeshInstance3D.new()
			var wm := CylinderMesh.new(); wm.top_radius = 0.8; wm.bottom_radius = 0.8; wm.height = 0.6
			w.mesh = wm
			var wmt := StandardMaterial3D.new(); wmt.albedo_color = Color(0.08, 0.08, 0.1); wmt.roughness = 0.9
			w.material_override = wmt
			w.rotation = Vector3(0, 0, deg_to_rad(90))
			w.position = Vector3(wx, 0.6, wz)
			root.add_child(w)
	# driver: sprite billboard if available, else a coloured head
	var driver: Node3D
	if sprite_path != "" and ResourceLoader.exists(sprite_path):
		var spr := Sprite3D.new()
		spr.texture = load(sprite_path)
		spr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		spr.pixel_size = 0.0075
		spr.position = Vector3(0, 4.0, 0)
		driver = spr
	else:
		var head := MeshInstance3D.new()
		var hm := SphereMesh.new(); hm.radius = 1.2; hm.height = 2.4
		head.mesh = hm
		var hmt := StandardMaterial3D.new(); hmt.albedo_color = col.lightened(0.3)
		head.material_override = hmt
		head.position = Vector3(0, 3.2, 0)
		driver = head
	root.add_child(driver)
	# nameplate
	var nl := Label3D.new()
	nl.text = racer_name; nl.font_size = 70; nl.outline_size = 14
	nl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	nl.modulate = col.lightened(0.4)
	nl.position = Vector3(0, 6.2, 0)
	root.add_child(nl)
	# rainbow trail accent for Roshan
	if racer_name == "Roshan":
		var trail := OmniLight3D.new()
		trail.light_color = Color(1.0, 0.5, 0.9); trail.light_energy = 2.5; trail.omni_range = 14.0
		trail.position = Vector3(0, 2.0, 2.5)
		root.add_child(trail)
	return root

func _build_karts() -> void:
	var n := RACERS.size()
	for idx in range(n):
		var r: Dictionary = RACERS[idx]
		var node := _kart_body(r["col"], String(r.get("sprite", "")), String(r["name"]))
		add_child(node)
		# stagger the grid: spread back from the line, alternating lanes
		var start_s := -6.0 - float(idx) * 5.0
		var lane := (-1.0 if idx % 2 == 0 else 1.0) * ROAD_HALF * 0.45
		var is_p: bool = bool(r.get("player", false))
		var k := {
			"node": node, "name": String(r["name"]), "is_player": is_p,
			"s": start_s, "lat": lane, "speed": 0.0, "boost": 0.0,
			"ai_skill": 0.92 + 0.10 * (float(idx) / float(n)),   # spread of AI pace (rubber-banded too)
			"ai_phase": float(idx) * 1.3,
		}
		_karts.append(k)
		if is_p:
			_pl = k

func _build_camera() -> void:
	_cam = Camera3D.new()
	_cam.fov = 68.0
	add_child(_cam)
	_cam.make_current()

func _mk_label(parent: Control, pos: Vector2, size: int, col: Color = Color.WHITE) -> Label:
	var l := Label.new()
	l.position = pos
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", col)
	l.add_theme_color_override("font_outline_color", Color(0, 0, 0))
	l.add_theme_constant_override("outline_size", 8)
	parent.add_child(l)
	return l

func _build_hud() -> void:
	_hud = CanvasLayer.new(); _hud.layer = 18
	add_child(_hud)
	var root := Control.new(); root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_hud.add_child(root)
	_lbl_lap = _mk_label(root, Vector2(24, 18), 38, Color(1, 0.95, 0.6))
	_lbl_place = _mk_label(root, Vector2(24, 66), 48, Color(0.7, 1.0, 1.0))
	_lbl_big = _mk_label(root, Vector2(0, 0), 130, Color(1, 1, 1))
	_lbl_big.set_anchors_preset(Control.PRESET_CENTER)
	_lbl_big.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_lbl_big.position = Vector2(-220, -120); _lbl_big.size = Vector2(440, 240)
	var hint := _mk_label(root, Vector2(24, 0), 26, Color(0.9, 0.9, 1.0))
	hint.anchor_top = 1.0; hint.position = Vector2(24, -56)
	hint.text = "Hold UP / A to GO   •   DOWN to brake   •   LEFT/RIGHT to steer"

# ---------------------------------------------------------------- input
func _steer_accel() -> Array:
	var accel := 0.0
	var steer := 0.0
	if Input.is_physical_key_pressed(KEY_UP) or Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_SPACE):
		accel += 1.0
	if Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S):
		accel -= 1.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		steer -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		steer += 1.0
	if Input.is_joy_button_pressed(0, JOY_BUTTON_A):
		accel += 1.0
	var jx: float = Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
	if absf(jx) > 0.2:
		steer += jx
	# touch: virtual stick (y = accel/brake, x = steer) + action = accel
	if _main != null and "touch_ui" in _main and _main.touch_ui != null:
		var tv: Vector2 = _main.touch_ui.stick_vec
		if tv.y < -0.15:
			accel += -tv.y
		elif tv.y > 0.15:
			accel -= tv.y
		if absf(tv.x) > 0.15:
			steer += tv.x
		if _main.touch_ui.action_down:
			accel += 1.0
	return [clampf(accel, -1.0, 1.0), clampf(steer, -1.0, 1.0)]

# ---------------------------------------------------------------- per-frame
func _process(delta: float) -> void:
	if _state == "done":
		return
	_clock -= delta
	if _state == "countdown":
		var n := int(ceil(_clock))
		_lbl_big.text = ("GO!" if n <= 0 else str(n))
		if _clock <= 0.0:
			_state = "race"
			_lbl_big.text = ""
			_clock = 0.0
		_update_camera(delta)
		return

	_race_t += delta
	var ic := _steer_accel()
	var accel: float = ic[0]
	var steer: float = ic[1]

	for k in _karts:
		if k["is_player"]:
			_update_player(k, accel, steer, delta)
		else:
			_update_ai(k, delta)
		_place_kart(k)

	_check_strips()
	_check_pickups(delta)
	_check_shortcut()
	_resolve_collisions()
	_update_camera(delta)
	_update_hud()

	# player finished all laps (or a long safety timeout so it can never soft-lock)?
	if _pl != null and (float(_pl["s"]) >= _len * float(LAPS) or _race_t > 150.0):
		_finish()

func _update_player(k: Dictionary, accel: float, steer: float, delta: float) -> void:
	k["boost"] = maxf(0.0, float(k["boost"]) - delta)
	var bf: float = 1.0 + (BOOST_MUL if float(k["boost"]) > 0.0 else 0.0)
	var target: float = (_vmax * 1.06 * bf) if accel > 0.0 else (0.0 if accel < 0.0 else _vmax * 0.25)
	if accel < 0.0:
		target = -_vmax * 0.12   # brake/reverse a touch
	elif float(k["boost"]) > 0.0:
		target = _vmax * 1.1 * bf   # the boost carries you even off the gas
	var rate: float = 22.0 if accel >= 0.0 else 40.0
	if float(k["boost"]) > 0.0:
		rate = 60.0   # snap up to boost speed fast
	k["speed"] = move_toward(float(k["speed"]), target, rate * delta)
	k["s"] = float(k["s"]) + float(k["speed"]) * delta
	# steering scales a bit with speed so it feels grippy
	var grip: float = clampf(absf(float(k["speed"])) / _vmax, 0.15, 1.0)
	_apply_lat(k, float(k["lat"]) + steer * 16.0 * grip * delta)

func _update_ai(k: Dictionary, delta: float) -> void:
	# constant-ish pace with gentle rubber-banding toward the player + lane wander
	k["boost"] = maxf(0.0, float(k["boost"]) - delta)
	var bf: float = 1.0 + (BOOST_MUL if float(k["boost"]) > 0.0 else 0.0)
	var base: float = _vmax * float(k["ai_skill"]) * bf
	if _pl != null:
		var gap: float = float(_pl["s"]) - float(k["s"])
		base += clampf(gap * 0.045, -_vmax * 0.13, _vmax * 0.24)   # stronger catch-up / hold-back (tight pack)
	base += sin(_race_t * 0.8 + float(k["ai_phase"])) * _vmax * 0.04
	k["speed"] = move_toward(float(k["speed"]), maxf(base, 0.0), 18.0 * delta)
	k["s"] = float(k["s"]) + float(k["speed"]) * delta
	var want: float = sin(_race_t * 0.5 + float(k["ai_phase"])) * ROAD_HALF * 0.4
	_apply_lat(k, move_toward(float(k["lat"]), want, 6.0 * delta))

func _apply_lat(k: Dictionary, new_lat: float) -> void:
	# bouncy walls: if you'd cross the rail, clamp + rebound inward and lose a little speed
	var wall: float = _width_at(_eff(float(k["s"]))) - 1.6
	if absf(new_lat) > wall:
		new_lat = clampf(new_lat, -wall, wall) * 0.8   # bounce back off the wall
		k["speed"] = float(k["speed"]) * WALL_SLOW       # and scrub speed (balance)
	k["lat"] = new_lat

func _resolve_collisions() -> void:
	# gentle kart-vs-kart bumping: push apart laterally + bleed a little speed
	for i in range(_karts.size()):
		for j in range(i + 1, _karts.size()):
			var a: Dictionary = _karts[i]
			var b: Dictionary = _karts[j]
			var an: Node3D = a["node"]
			var bn: Node3D = b["node"]
			var d: float = an.position.distance_to(bn.position)
			if d < COLLIDE_R and d > 0.01:
				var sep: float = (COLLIDE_R - d) * 0.5
				var dir: float = 1.0 if float(a["lat"]) >= float(b["lat"]) else -1.0
				var wa: float = _width_at(_eff(float(a["s"]))) - 1.4
				var wb: float = _width_at(_eff(float(b["s"]))) - 1.4
				a["lat"] = clampf(float(a["lat"]) + dir * sep, -wa, wa)
				b["lat"] = clampf(float(b["lat"]) - dir * sep, -wb, wb)
				a["speed"] = float(a["speed"]) * 0.93
				b["speed"] = float(b["speed"]) * 0.93
				# nudge the kart that's ahead in s back a touch so they don't interpenetrate
				if float(a["s"]) > float(b["s"]):
					a["s"] = float(a["s"]) - sep * 0.25
				else:
					b["s"] = float(b["s"]) - sep * 0.25

func _place_kart(k: Dictionary) -> void:
	var fr := _kart_frame(float(k["s"]), float(k["lat"]))
	var pos: Vector3 = fr[0]
	var fwd: Vector3 = fr[1]
	var up: Vector3 = fr[3]
	var node: Node3D = k["node"]
	node.position = pos + up * 1.2
	if fwd.length() > 0.001:
		node.look_at(pos + fwd + up * 1.2, up)

func _check_strips() -> void:
	# any kart driving over a zoom strip gets a boost (proximity -> works either direction)
	for k in _karts:
		var kn: Node3D = k["node"]
		for sd in _strip_data:
			if kn.position.distance_to(sd["pos"]) < float(sd["len"]) * 0.6 + 3.0:
				if float(k["boost"]) < STRIP_BOOST:
					k["boost"] = STRIP_BOOST

func _check_pickups(delta: float) -> void:
	# only the player collects items (the player's advantage, like the shortcut)
	if _pl == null:
		return
	var pn: Node3D = _pl["node"]
	var t: float = Time.get_ticks_msec() / 1000.0
	for pu in _pickups_live:
		var node: Node3D = pu["node"]
		# spin + bob the live ones
		node.rotation.y = t * 1.6
		node.position.y = (_frame_at(float(pu["s"]), float(pu["lat"]))[0] as Vector3).y + 2.6 + sin(t * 2.0 + float(pu["s"])) * 0.5
		if float(pu["cool"]) > 0.0:
			pu["cool"] = float(pu["cool"]) - delta
			if float(pu["cool"]) <= 0.0:
				node.visible = true
			continue
		if node.position.distance_to(pn.position) < 6.5:
			var amt: float = STAR_BOOST if String(pu["kind"]) == "star" else SHELL_BOOST
			_pl["boost"] = maxf(float(_pl["boost"]), amt)
			node.visible = false
			pu["cool"] = 6.0
			if _main != null and _main.has_method("_sparkle_burst"):
				var col := Color(1.0, 0.9, 0.3) if String(pu["kind"]) == "star" else Color(1.0, 0.7, 0.95)
				_main._sparkle_burst(pn.position, col)

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
		# warp across the loop (stay within this lap's distance band)
		var base: float = float(lap) * _len
		_pl["s"] = base + SHORTCUT_TO_U * _len
		_pl["speed"] = _vmax * 1.15      # little boost out of the warp
		if _main != null and _main.has_method("_sparkle_burst"):
			_main._sparkle_burst(pn.position, Color(0.5, 1.0, 0.8))

func _update_camera(delta: float) -> void:
	if _cam == null or _pl == null:
		return
	var pn: Node3D = _pl["node"]
	var fr := _kart_frame(float(_pl["s"]), float(_pl["lat"]))
	var fwd: Vector3 = fr[1]
	var want: Vector3 = pn.position - fwd * 16.0 + Vector3(0, 8.0, 0)
	_cam.position = _cam.position.lerp(want, clampf(delta * 4.0, 0.0, 1.0))
	_cam.look_at(pn.position + fwd * 6.0 + Vector3(0, 2.0, 0), Vector3.UP)

func _placement() -> int:
	if _pl == null:
		return 1
	var ahead := 1
	for k in _karts:
		if not k["is_player"] and float(k["s"]) > float(_pl["s"]):
			ahead += 1
	return ahead

func _update_hud() -> void:
	if _pl == null:
		return
	var lap: int = clampi(int(float(_pl["s"]) / _len) + 1, 1, LAPS)
	_lbl_lap.text = ("Lap %d / %d  ↺ REVERSE" % [lap, LAPS]) if _rev else ("Lap %d / %d" % [lap, LAPS])
	var place := _placement()
	var suffix: String = ["st", "nd", "rd", "th", "th", "th", "th", "th"][clampi(place - 1, 0, 7)]
	_lbl_place.text = "%d%s" % [place, suffix]

func _finish() -> void:
	_state = "done"
	var place := _placement()
	_lbl_big.text = ("YOU WIN!" if place == 1 else "%d%s!" % [place, ["st","nd","rd","th","th","th","th","th"][clampi(place-1,0,7)]])
	# brief celebration, then hand back to main
	var tw := create_tween()
	tw.tween_interval(2.4)
	tw.tween_callback(func():
		if _prev_env != null and "we_node" in _main and _main.we_node != null:
			_main.we_node.environment = _prev_env
		if _player_node != null and "cam" in _player_node and _player_node.cam != null:
			(_player_node.cam as Camera3D).make_current()
		if _finish_cb.is_valid():
			_finish_cb.call(place)
		queue_free()
	)
