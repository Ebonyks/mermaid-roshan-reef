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
# answer. Props are rough primitive demos — authored art swaps in later.

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
var avatar: Sprite3D = null
var costume_root: Node3D = null
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
var stir_done := 0
var brush_loaded := -1
var brush_node: Node3D = null
var canvas_pos := Vector3.ZERO
var stripes: Array[Node3D] = []

# ---- "echo" engine ----
var echo_rounds: Array[int] = []
var echo_round := 0
var echo_seq: Array[int] = []
var echo_pos := 0
var echo_phase := "show"           # show | repeat
var echo_show_i := 0
var echo_show_t := 0.0
var last_pad := -1

# ---- "shuffle" engine ----
var hats: Array[Dictionary] = []
var bunny: Node3D = null
var bunny_at := 0
var shuffle_round := 0
var shuffle_phase := "watch"       # watch | pick
var shuffle_t := 0.0
var swap_plan: Array[Dictionary] = []

# ---- "fix" engine ----
var pieces: Array[Dictionary] = []
var slots: Array[Dictionary] = []
var fix_step := 0
var carried := -1
var fix_phase := "pipes"           # pipes | valve
var valve: Node3D = null
var rocket_window: MeshInstance3D = null

# ---- "press" engine ----
var press_x := 0.0                 # slider position, -1..1
var press_zone := 0.34             # sweet-spot half-width (generous, shrinks a little)
var press_busy := 0.0              # stamp animation lockout
var candies_done := 0
var candy_node: Node3D = null
var press_block: Node3D = null
var press_slider: Node3D = null
var press_zone_box: Node3D = null
var shelf_candies: Array[Node3D] = []

# ---- "doctor" engine ----
var doc_targets: Array[Dictionary] = []
var doc_step := 0
var patient: Node3D = null

# ---- "scroll" engine (2D farm overlay; piggy art is a pending art-wing pass) ----
const FARM_SPEED := 150.0
const FARM_WRAP := 3000.0
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
var peek_spots: Array[float] = [-12.0, 0.0, 12.0]   # the dragon roams the curtain
var peek_i := 0
var far_hint_cool := 0.0

# ---- shared: the rescue arrow ----
# The golden pointer is a RESCUE, not the answer: for guessing games it only
# appears after ~5s without progress (or right after a mistake), so the child
# gets a real "I did it myself!" moment before help arrives.
const RESCUE_DELAY := 5.0

func start(main: ReefMain, act_config: Dictionary, done_cb: Callable) -> void:
	m = main
	config = act_config
	finish_cb = done_cb
	kind = String(config.get("kind", "order"))
	reveal_one = bool(config.get("reveal_one", false))
	act_tag = String(config.get("act_tag", ""))
	player_pos = CENTER + Vector3(0, 1.1, 14.0)
	_build_environment()
	_build_theatre()
	_build_avatar()
	_build_camera()
	_build_hud()
	match kind:
		"order":
			_build_order()
		"echo":
			_build_echo()
		"shuffle":
			_build_shuffle()
		"fix":
			_build_fix()
		"press":
			_build_press()
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
	# the Showtime transformation moment: sparkles + the career announcement
	m._sparkle_burst(player_pos + Vector3(0, 2.5, 0), Color(1.0, 0.85, 1.0))
	m._sparkle_burst(player_pos + Vector3(0, 0.8, 0), Color(0.72, 0.95, 1.0))
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

func _build_theatre() -> void:
	var floor_col := Color(config.get("floor_col", Color(0.52, 0.4, 0.62)))
	var trim: Color = Color(config.get("trim", Color(1.0, 0.85, 0.55)))
	var curtain: Color = Color(config.get("curtain", Color(0.78, 0.24, 0.34)))
	# stage deck + front apron edge
	_box(CENTER + Vector3(0, -0.3, -2.0), Vector3(52, 1.2, 34), floor_col)
	_box(CENTER + Vector3(0, 0.15, 15.2), Vector3(52, 0.5, 1.6), trim, 0.2)
	# proscenium: two gold pillars + top beam
	_box(CENTER + Vector3(-23.0, 8.0, 12.0), Vector3(2.2, 17, 2.2), trim, 0.12)
	_box(CENTER + Vector3(23.0, 8.0, 12.0), Vector3(2.2, 17, 2.2), trim, 0.12)
	_box(CENTER + Vector3(0, 16.6, 12.0), Vector3(48.2, 2.6, 2.4), trim, 0.12)
	# back curtain + gathered side curtains
	_box(CENTER + Vector3(0, 7.5, -18.0), Vector3(46, 16, 1.4), curtain)
	_box(CENTER + Vector3(-21.0, 7.5, -3.0), Vector3(2.6, 16, 30), curtain.darkened(0.12))
	_box(CENTER + Vector3(21.0, 7.5, -3.0), Vector3(2.6, 16, 30), curtain.darkened(0.12))
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
	var guests: Array[String] = ["pearl_friend", "two_friends", "gabby", "wacky_chuck"]
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

func _build_avatar() -> void:
	avatar = Sprite3D.new()
	var tex := load("res://assets/characters/roshan_sprite.png") as Texture2D
	avatar.texture = tex
	avatar.pixel_size = 6.2 / maxf(float(tex.get_height()), 1.0) if tex != null else 0.01
	avatar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	avatar.position = player_pos
	add_child(avatar)
	_build_costume(String(config.get("costume", "")))

func _build_costume(costume: String) -> void:
	# Career costumes are oversized toy props floating at hat/waist height beside
	# the storybook cutout — the illustration itself is never redrawn or re-lit.
	costume_root = Node3D.new()
	costume_root.name = "Costume_" + costume
	add_child(costume_root)
	match costume:
		"chef":
			_cyl(Vector3(0, 3.6, 0), 0.85, 0.9, Color(0.98, 0.97, 0.94), 0.05, costume_root)
			_sphere(Vector3(0, 4.35, 0), 0.95, Color(1.0, 1.0, 0.98), 0.05, costume_root)
		"detective":
			_cyl(Vector3(0, 3.6, 0), 1.05, 0.5, Color(0.62, 0.45, 0.3), 0.0, costume_root)
			var lens := TorusMesh.new()
			lens.inner_radius = 0.34
			lens.outer_radius = 0.56
			_mesh(lens, Vector3(1.7, 1.6, 0), Color(1.0, 0.85, 0.4), 0.3, costume_root)
			_box(Vector3(2.25, 0.95, 0), Vector3(0.2, 0.9, 0.2), Color(0.5, 0.3, 0.2), 0.0, costume_root)
		"ballerina":
			var tutu := TorusMesh.new()
			tutu.inner_radius = 0.55
			tutu.outer_radius = 1.35
			_mesh(tutu, Vector3(0, 1.1, 0), Color(1.0, 0.72, 0.86), 0.15, costume_root)
		"knight":
			_cyl(Vector3(-1.8, 1.7, 0), 0.85, 0.3, Color(0.65, 0.78, 0.95), 0.25, costume_root)
			_sphere(Vector3(-1.8, 1.7, 0), 0.35, Color(1.0, 0.85, 0.4), 0.8, costume_root)
			_sphere(Vector3(0, 3.7, 0), 0.5, Color(1.0, 0.9, 0.4), 0.6, costume_root)
		"singer":
			var tiara := TorusMesh.new()
			tiara.inner_radius = 0.5
			tiara.outer_radius = 0.75
			_mesh(tiara, Vector3(0, 3.5, 0), Color(1.0, 0.87, 0.42), 0.5, costume_root)
			_sphere(Vector3(1.8, 2.6, 0), 0.32, Color(1.0, 0.95, 0.5), 0.9, costume_root)
			_box(Vector3(2.05, 3.25, 0), Vector3(0.14, 1.0, 0.14), Color(1.0, 0.95, 0.5), 0.9, costume_root)
		"magician":
			_cyl(Vector3(0, 3.9, 0), 0.8, 1.3, Color(0.36, 0.22, 0.55), 0.15, costume_root)
			_cyl(Vector3(0, 3.3, 0), 1.15, 0.22, Color(0.36, 0.22, 0.55), 0.15, costume_root)
			_box(Vector3(1.9, 1.6, 0), Vector3(0.16, 1.2, 0.16), Color(0.95, 0.95, 1.0), 0.4, costume_root)
		"painter":
			var beret := _cyl(Vector3(0.2, 3.55, 0), 1.0, 0.35, Color(0.32, 0.5, 0.85), 0.1, costume_root)
			beret.rotation_degrees = Vector3(0, 0, -12.0)
			_box(Vector3(1.8, 1.5, 0), Vector3(0.16, 1.1, 0.16), Color(0.6, 0.4, 0.25), 0.0, costume_root)
			_box(Vector3(1.8, 2.2, 0), Vector3(0.24, 0.3, 0.24), Color(1.0, 0.45, 0.6), 0.5, costume_root)
		"starcape":
			var cape := _box(Vector3(0, 1.9, -0.9), Vector3(2.4, 3.4, 0.18), Color(0.16, 0.14, 0.4), 0.1, costume_root)
			cape.rotation_degrees = Vector3(8.0, 0, 0)
			_sphere(Vector3(0, 3.8, 0), 0.45, Color(1.0, 0.9, 0.4), 0.8, costume_root)
		"astronaut":
			var collar := TorusMesh.new()
			collar.inner_radius = 0.75
			collar.outer_radius = 1.05
			_mesh(collar, Vector3(0, 2.9, 0), Color(0.85, 0.88, 0.95), 0.2, costume_root)
			_sphere(Vector3(0, 3.7, 0), 1.15, Color(0.92, 0.97, 1.0), 0.15, costume_root)
			_cyl(Vector3(-0.5, 1.6, -0.85), 0.35, 1.4, Color(0.75, 0.8, 0.9), 0.2, costume_root)
			_cyl(Vector3(0.5, 1.6, -0.85), 0.35, 1.4, Color(0.75, 0.8, 0.9), 0.2, costume_root)
		"candymaker":
			_cyl(Vector3(0, 3.4, 0), 0.9, 0.5, Color(1.0, 0.62, 0.7), 0.2, costume_root)
			_cyl(Vector3(0, 3.9, 0), 0.75, 0.5, Color(1.0, 0.95, 0.95), 0.2, costume_root)
			_cyl(Vector3(0, 4.4, 0), 0.6, 0.5, Color(1.0, 0.62, 0.7), 0.2, costume_root)
			_cyl(Vector3(1.9, 2.6, 0), 0.55, 0.2, Color(1.0, 0.5, 0.65), 0.6, costume_root)
			_box(Vector3(1.9, 1.6, 0), Vector3(0.14, 1.4, 0.14), Color(0.98, 0.95, 0.9), 0.1, costume_root)
		"doctor":
			var mirror := TorusMesh.new()
			mirror.inner_radius = 0.55
			mirror.outer_radius = 0.8
			_mesh(mirror, Vector3(0, 3.4, 0), Color(0.95, 0.97, 1.0), 0.2, costume_root)
			_sphere(Vector3(0, 3.75, 0.5), 0.3, Color(1.0, 0.9, 0.5), 0.8, costume_root)
			var scope := TorusMesh.new()
			scope.inner_radius = 0.6
			scope.outer_radius = 0.78
			_mesh(scope, Vector3(0, 2.5, 0.2), Color(0.35, 0.4, 0.55), 0.1, costume_root)
			_cyl(Vector3(0, 1.7, 0.55), 0.28, 0.14, Color(0.8, 0.85, 0.95), 0.4, costume_root)
		"racer":
			_sphere(Vector3(0, 3.7, 0), 0.95, Color(0.95, 0.35, 0.3), 0.2, costume_root)
			_box(Vector3(0, 3.6, 0.75), Vector3(1.3, 0.5, 0.3), Color(0.4, 0.75, 1.0), 0.4, costume_root)
			var wheel := TorusMesh.new()
			wheel.inner_radius = 0.55
			wheel.outer_radius = 0.85
			var wheel_mesh := _mesh(wheel, Vector3(1.8, 1.5, 0), Color(0.25, 0.25, 0.35), 0.1, costume_root)
			wheel_mesh.rotation_degrees = Vector3(90, 0, 0)
		"farmer":
			_cyl(Vector3(0, 3.35, 0), 1.5, 0.22, Color(0.93, 0.82, 0.5), 0.1, costume_root)
			_cyl(Vector3(0, 3.75, 0), 0.85, 0.7, Color(0.93, 0.82, 0.5), 0.1, costume_root)
			var carrot := CylinderMesh.new()
			carrot.top_radius = 0.05
			carrot.bottom_radius = 0.4
			carrot.height = 1.2
			var carrot_mesh := _mesh(carrot, Vector3(1.8, 1.7, 0), Color(1.0, 0.55, 0.2), 0.3, costume_root)
			carrot_mesh.rotation_degrees = Vector3(180, 0, 0)
			_sphere(Vector3(1.8, 2.45, 0), 0.3, Color(0.45, 0.8, 0.4), 0.2, costume_root)
		"popstar":
			_sphere(Vector3(-0.5, 3.0, 0.6), 0.4, Color(1.0, 0.85, 0.35), 0.7, costume_root)
			_sphere(Vector3(0.5, 3.0, 0.6), 0.4, Color(1.0, 0.85, 0.35), 0.7, costume_root)
			_box(Vector3(0, 3.0, 0.62), Vector3(0.5, 0.14, 0.14), Color(1.0, 0.85, 0.35), 0.7, costume_root)
			_box(Vector3(1.8, 1.7, 0), Vector3(0.16, 1.1, 0.16), Color(0.75, 0.78, 0.88), 0.2, costume_root)
			_sphere(Vector3(1.8, 2.5, 0), 0.42, Color(0.9, 0.5, 0.85), 0.6, costume_root)
	costume_root.position = player_pos

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

# ---------------- "order" engine (chef / detective / painter) ----------------

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
			_box(Vector3(0, 2.6, 0), Vector3(6.4, 4.6, 0.4), Color(0.96, 0.94, 0.88), 0.1, goal)
			_box(Vector3(0, 0.3, 0.6), Vector3(5.0, 0.6, 0.6), Color(0.55, 0.38, 0.24), 0.0, goal)
		_:
			var bowl := CylinderMesh.new()
			bowl.top_radius = 2.4
			bowl.bottom_radius = 1.5
			bowl.height = 1.6
			_mesh(bowl, Vector3(0, 0.8, 0), Color(0.85, 0.9, 1.0), 0.1, goal)
	# the picture recipe: small copies above the goal, left-to-right = the order
	if not reveal_one:
		for s in range(order_steps.size()):
			var ci := order_steps[s]
			_sphere(goal.position + Vector3(-3.2 + float(s) * 3.2, 5.8, 0), 0.8, cols[ci], 0.5)
	if order_flow == "carry_paint":
		canvas_pos = goal.position
		# three hidden stripes fill the canvas as Roshan swipes each color on
		for s2 in range(order_steps.size()):
			var stripe := _box(goal.position + Vector3(0, 1.2 + float(s2) * 1.4, 0.25), Vector3(5.8, 1.2, 0.2), cols[order_steps[s2]], 0.35)
			stripe.visible = false
			stripes.append(stripe)
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
			return [Color(1.0, 0.55, 0.3), Color(1.0, 0.85, 0.35), Color(0.6, 0.5, 0.95)]
		_:
			return [Color(0.65, 0.42, 0.25), Color(1.0, 0.62, 0.78), Color(0.98, 0.94, 0.85)]

func _order_prop(theme: String, i: int, col: Color, parent: Node3D) -> Node3D:
	var prop := Node3D.new()
	prop.name = "PadProp"
	prop.position = Vector3(0, 0.6, 0)
	parent.add_child(prop)
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
	if state != "play" or kind != "order" or order_phase != "steps" or step >= order_steps.size():
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
	if state != "play" or kind != "order" or order_phase != "stir":
		return
	stir_done += 1
	progress_t = 0.0
	var tw := goal.create_tween()
	tw.tween_property(goal, "rotation:y", goal.rotation.y + TAU * float(stir_done), 0.55).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	m._sparkle_burst(goal.position + Vector3(0, 3.0, 0), Color(1.0, 0.85, 0.6))
	if m.chime != null:
		m.chime.pitch_scale = 0.85 + 0.25 * float(stir_done)
		m.chime.play()
	if stir_done >= 3:
		var pop := goal.create_tween()
		pop.tween_property(goal, "scale", goal.scale * 1.25, 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		m._sparkle_burst(goal.position + Vector3(0, 4.5, 0), Color(1.0, 0.75, 0.9))
		_win()
	else:
		_update_hud()

func _paint_touch() -> void:
	# the painter swipe: a loaded brush near the canvas sweeps a stripe on
	if state != "play" or kind != "order" or order_flow != "carry_paint" or brush_loaded < 0:
		return
	var stripe := stripes[step]
	stripe.visible = true
	stripe.scale = Vector3(0.05, 1.0, 1.0)
	var tw := stripe.create_tween()
	tw.tween_property(stripe, "scale", Vector3.ONE, 0.6).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	brush_node.visible = false
	brush_loaded = -1
	m._sparkle_burst(canvas_pos + Vector3(0, 3.0, 1.0), Color(1.0, 0.9, 0.6))
	if m.chime != null:
		m.chime.pitch_scale = 0.95 + 0.18 * float(step)
		m.chime.play()
	step += 1
	progress_t = 0.0
	if step >= order_steps.size():
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
	_sphere(Vector3(0, 0, 0), 0.8, Color(0.95, 0.92, 1.0), 0.2, bunny)
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
			shuffle_phase = "wait"   # neutral while the reveal plays out
			var next := (bunny_at + 1) % 3
			var tw2 := create_tween()
			tw2.tween_interval(0.9)
			tw2.tween_callback(func() -> void: _shuffle_hide(next))
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
	_cyl(Vector3(0, 2.2, 0), 2.2, 4.4, Color(0.55, 0.85, 0.95), 0.15, tank)
	_sphere(Vector3(0, 5.0, 0), 1.4, Color(0.75, 0.95, 1.0), 0.3, tank)
	var rocket := Node3D.new()
	rocket.name = "StarRocket"
	rocket.position = CENTER + Vector3(14.0, 1.0, -12.0)
	add_child(rocket)
	_cyl(Vector3(0, 3.0, 0), 1.8, 6.0, Color(0.92, 0.9, 0.98), 0.1, rocket)
	var nose := CylinderMesh.new()
	nose.top_radius = 0.1
	nose.bottom_radius = 1.8
	nose.height = 2.6
	_mesh(nose, Vector3(0, 7.3, 0), Color(1.0, 0.55, 0.5), 0.2, rocket)
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
	if state != "play" or kind != "fix" or fix_phase != "valve":
		return
	var tw := valve.create_tween()
	tw.tween_property(valve, "rotation:z", TAU, 0.8).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
	# bubbles race down the finished pipe and light the rocket window
	for i in range(5):
		m._sparkle_burst(CENTER + Vector3(-14.0 + float(i) * 7.0, 4.0, -12.0), Color(0.7, 0.95, 1.0))
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
	var machine := Node3D.new()
	machine.name = "CandyPress"
	machine.position = CENTER + Vector3(0, 1.0, -10.0)
	add_child(machine)
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
		press_zone = maxf(0.22, 0.34 - 0.06 * float(candies_done))
		if press_zone_box != null:
			press_zone_box.scale.x = press_zone / 0.34
		if candies_done >= 3:
			_win()
		else:
			var tw3 := create_tween()
			tw3.tween_interval(0.8)
			tw3.tween_callback(_candy_next)
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
	_sphere(Vector3.ZERO, 1.6, Color(0.78, 0.66, 0.92), 0.1, patient)
	for i in range(5):
		var a := float(i) * TAU / 5.0 + 0.3
		_sphere(Vector3(cos(a) * 1.7, 0.2, sin(a) * 1.7), 0.62, Color(0.82, 0.7, 0.95), 0.1, patient)
	_sphere(Vector3(-0.45, 0.8, 1.15), 0.2, Color(0.12, 0.1, 0.25), 0.0, patient)
	_sphere(Vector3(0.45, 0.8, 1.15), 0.2, Color(0.12, 0.1, 0.25), 0.0, patient)
	# step 0: the stethoscope — listen to the plushy's little heart first
	var scope := Node3D.new()
	scope.name = "Stethoscope"
	scope.position = CENTER + Vector3(-9.0, 1.0, 4.0)
	add_child(scope)
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
	_cyl(Vector3(0, 0.2, 0), 1.2, 0.4, Color(0.8, 0.85, 0.92), 0.05, thermo)
	var stem := _box(Vector3(0, 1.4, 0), Vector3(0.3, 2.2, 0.3), Color(0.95, 0.97, 1.0), 0.3, thermo)
	stem.rotation_degrees = Vector3(0, 0, 18.0)
	_sphere(Vector3(-0.35, 0.55, 0), 0.34, Color(1.0, 0.35, 0.3), 0.5, thermo)
	doc_targets.append({"index": 1, "node": thermo, "pos": thermo.position, "kind": "thermo"})
	# steps 2-3: glowing boo-boos on the plush that become hearts when tended
	var boo_spots: Array[Vector3] = [Vector3(-1.1, 0.9, 0.8), Vector3(1.2, 0.5, 0.9)]
	for b in range(boo_spots.size()):
		var boo := _sphere(boo_spots[b], 0.4, Color(1.0, 0.3, 0.25), 0.9, patient)
		var heart := _sphere(boo_spots[b] + Vector3(0, 0.15, 0.1), 0.42, Color(1.0, 0.55, 0.75), 0.7, patient)
		heart.visible = false
		var reach := CENTER + Vector3(-2.0 + float(b) * 4.0, 1.0, 1.4)
		doc_targets.append({"index": 2 + b, "node": boo, "heart": heart, "pos": reach, "kind": "boo"})
	# step 4: the bandage roll, which wraps a soft white band around the plush
	var roll := Node3D.new()
	roll.name = "BandageRoll"
	roll.position = CENTER + Vector3(0.0, 1.0, 6.5)
	add_child(roll)
	var loop := TorusMesh.new()
	loop.inner_radius = 0.4
	loop.outer_radius = 0.9
	_mesh(loop, Vector3(0, 0.9, 0), Color(0.97, 0.97, 0.94), 0.15, roll)
	var band := _box(Vector3(0, 0.1, 0), Vector3(3.6, 0.5, 3.6), Color(0.98, 0.98, 0.95), 0.2, patient)
	band.visible = false
	doc_targets.append({"index": 4, "node": roll, "band": band, "pos": roll.position, "kind": "bandage"})

func _doctor_action(choice: int) -> void:
	if state != "play" or kind != "doctor" or doc_step >= doc_targets.size():
		return
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
		# magic-kiss finale: a fountain of hearts, then the plush pops up better
		for h in range(3):
			m._sparkle_burst(patient.position + Vector3(-1.5 + float(h) * 1.5, 2.5 + float(h) * 0.8, 1.0), Color(1.0, 0.6, 0.8))
		var hop := patient.create_tween()
		hop.tween_property(patient, "position:y", patient.position.y + 1.6, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		hop.tween_property(patient, "position:y", patient.position.y, 0.35).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
		_win()
	else:
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
	for i in range(5):
		var pig := Control.new()
		pig.position = Vector2(900.0 + float(i) * 520.0, 420.0)
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
			"x": 900.0 + float(i) * 520.0, "sx": 900.0 + float(i) * 520.0, "fed": false})

func _tick_farm(delta: float) -> void:
	farm_t += delta
	farm_toss_cool = maxf(0.0, farm_toss_cool - delta)
	if farm_roshan != null:
		farm_roshan.position.y = 330.0 + sin(elapsed * 3.2) * 14.0
	for pig in piggies:
		var sx: float = float(pig["x"]) - farm_t * FARM_SPEED
		while sx < -160.0:
			# unfed piggies trot back around; fed ones park happily off-screen
			if bool(pig["fed"]):
				break
			pig["x"] = float(pig["x"]) + FARM_WRAP
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
	var dual := bool(config.get("dual", false))
	var root := Node3D.new()
	root.name = "OperaBoss"
	root.position = CENTER + Vector3(0, 1.0, -14.0)
	add_child(root)
	if dual:
		var cone := CylinderMesh.new()
		cone.top_radius = 0.3
		cone.bottom_radius = 2.4
		cone.height = 5.2
		_mesh(cone, Vector3(0, 2.6, 0), Color(0.16, 0.13, 0.3), 0.1, root)
		_sphere(Vector3(0, 5.2, 0.8), 1.0, Color(0.94, 0.94, 1.0), 0.25, root)
		_sphere(Vector3(-0.4, 5.4, 1.55), 0.22, Color(0.1, 0.1, 0.25), 0.0, root)
		_sphere(Vector3(0.4, 5.4, 1.55), 0.22, Color(0.1, 0.1, 0.25), 0.0, root)
	else:
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
		"timer": float(config.get("hide_time", 2.2)), "attack": 1.6, "dual": dual}
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
	var caught := Vector3(lant_pos.x, 1.0, -12.0)
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
	if bool(boss.get("dual", false)):
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
			# whack-a-mole roam: the dragon pops from a DIFFERENT curtain spot
			# each time, so Roshan chases him along the stage
			peek_i = (peek_i + 1) % peek_spots.size()
			var new_home := Vector3(CENTER.x + peek_spots[peek_i], home.y, home.z)
			boss["home"] = new_home
			root.position = new_home + Vector3(0, -6.5, 0)
			boss["phase"] = "peek"
			boss["timer"] = float(config.get("peek_time", 4.5))
			boss["attack"] = 1.0
			m._sparkle_burst(new_home + Vector3(0, 5.0, 1.0), Color(0.6, 0.95, 0.7))
	elif phase == "peek":
		root.position = root.position.lerp(home, delta * 5.0)
		root.rotation.y = sin(elapsed * 1.6) * 0.2
		if float(boss["attack"]) <= 0.0:
			boss["attack"] = 2.0
			_spawn_puff(root.position + Vector3(0, 4.5, 1.5))
		if float(boss["timer"]) <= 0.0:
			if bool(boss.get("dual", false)):
				# no fail: the shy phantom just re-hides; the same lantern twinkles again
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
		"order":
			_order_action(choice)
		"shuffle":
			_shuffle_action(choice)

func _process(delta: float) -> void:
	if m == null or state == "done":
		return
	elapsed += delta
	progress_t += delta
	if state == "won":
		win_t -= delta
		if fmod(win_t, 0.35) < delta:
			m._sparkle_burst(CENTER + Vector3(randf_range(-12.0, 12.0), randf_range(1.0, 8.0), randf_range(-8.0, 10.0)), Color.from_hsv(randf(), 0.5, 1.0))
		if kind == "echo":
			# free-dance encore: during the applause every tile still lights up
			# under Roshan — a pure toy moment with no goal at all
			var move2 := _move_input()
			player_pos += Vector3(move2.x, 0, move2.y) * MOVE_SPEED * delta
			avatar.position = player_pos + Vector3(0, sin(elapsed * 4.0) * 0.12, 0)
			if costume_root != null:
				costume_root.position = avatar.position
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
	var flat := Vector2(player_pos.x - CENTER.x, player_pos.z - CENTER.z)
	if flat.length() > RADIUS - 2.0:
		flat = flat.normalized() * (RADIUS - 2.0)
		player_pos.x = CENTER.x + flat.x
		player_pos.z = CENTER.z + flat.y
	avatar.position = player_pos + Vector3(0, sin(elapsed * 4.0) * 0.12, 0)
	if costume_root != null:
		costume_root.position = avatar.position
	for i in range(audience.size()):
		audience[i].position.y = CENTER.y + 4.0 + sin(elapsed * 2.2 + float(i) * 1.4) * 0.18
	if _action_pressed():
		match kind:
			"order":
				if order_phase == "stir":
					if goal.position.distance_to(player_pos) < 5.5:
						_stir_action()
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
		"order":
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
				if canvas_pos.distance_to(player_pos) < 5.5:
					_paint_touch()
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
				if not near_any:
					last_pad = -1
				elif touched >= 0 and touched != last_pad:
					last_pad = touched
					_pad_touch(touched)
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

func _pointer_target() -> Vector3:
	match kind:
		"order":
			if order_phase == "stir":
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
	# that arrives after RESCUE_DELAY without progress (mistakes summon it)
	if kind == "order" and not order_hidden:
		show = show and progress_t > RESCUE_DELAY
	elif kind == "echo" and echo_phase == "repeat":
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
	match kind:
		"order":
			if order_phase == "stir":
				objective.text = tag + "🥄  STIR the big bowl!  %d / 3" % stir_done
			elif brush_loaded >= 0:
				objective.text = tag + "🖌  Swipe the canvas to paint!  %d / %d" % [step, order_steps.size()]
			else:
				objective.text = tag + "✨  Match the pictures!  %d / %d" % [step, order_steps.size()]
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
				objective.text = tag + "💨  Spin the big valve — tap USE!"
			elif carried >= 0:
				objective.text = tag + "🔧  Carry it to the glowing gap!  %d / %d" % [fix_step, slots.size()]
			else:
				objective.text = tag + "🔧  Grab the pipe piece under the arrow!  %d / %d" % [fix_step, slots.size()]
		"press":
			objective.text = tag + "🍬  PRESS when the star is in the green middle!  %d / 3" % candies_done
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
	if prev_env != null:
		m.we_node.environment = prev_env
	if finish_cb.is_valid():
		finish_cb.call()
	queue_free()

func cancel() -> void:
	if state == "done":
		return
	if state == "won":
		_finish()   # the applause was already earned; leaving skips only the delay
		return
	state = "done"
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
	match kind:
		"echo":
			return "DANCE"
		"press":
			return "PRESS"
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
