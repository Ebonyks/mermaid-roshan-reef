class_name OperaHouse
extends Node
# The Pearl Opera House (Peach Showtime model): an explorable THREE-floor
# theatre lobby. Twelve careers are twelve marquee doors, four per floor —
# Roshan swims the hall, walks into a door, transforms, and plays that one
# show. Bosses do NOT use doors (owner 2026-07-21): when a floor's four shows
# are starred, the centre of that floor's stage lights up and swimming onto
# the glowing medallion starts the boss. Floor 3's medallion is the fifteenth
# and final act — the Midnight Maestro's grand finale. Bubble lifts cycle
# ground → balcony → top gallery → ground. OperaAct owns every performance;
# this class owns the lobby world, door/medallion flow, star checkpoints
# (m.opera_stars bitmask) and safe exits.

const ACTS := [
	# ---------- FLOOR 1: the Lagoon Lights Stage ----------
	{"name": "The Great Cake Show", "career": "Pastry Chef", "costume": "chef", "emoji": "🍰", "story": 1, "type": "show",
		"kind": "order", "props": "cake", "order": [0, 2, 1, 0, 2], "finale": "stir", "decorate": 3, "imps": 6, "shell": true,
		"voice": "Chef hat on! Look at the recipe over the bowl — bring the cake layers up in that same order, give it a big stir, then pop the toppings on!",
		"win_line": "The show cake is PERFECT! Everybody wants a slice!",
		"floor_col": Color(0.72, 0.5, 0.62), "trim": Color(1.0, 0.78, 0.86), "curtain": Color(0.85, 0.3, 0.4)},
	{"name": "The Missing Tiara", "career": "Detective", "costume": "detective", "emoji": "🔍", "story": 1, "type": "show",
		"kind": "sleuth", "props_n": 6, "clues": 3, "imps": 6, "shell": true,
		"voice": "Detective Roshan is on the case! Three clues hide inside the big boxes — PEEK in each one, and watch out for silly fish!",
		"win_line": "Case closed! The tiara was in the treasure box all along!",
		"floor_col": Color(0.42, 0.46, 0.62), "trim": Color(0.72, 0.85, 1.0), "curtain": Color(0.3, 0.35, 0.6)},
	{"name": "The Dance Recital", "career": "Ballerina", "costume": "ballerina", "emoji": "🩰", "story": 1, "type": "show",
		"kind": "echo", "pads": 4, "rounds": [3, 4, 5], "pitch": 0.6,
		"voice": "Ballerina twirl! Watch the glowing dance tiles twinkle, then dance the same steps!",
		"win_line": "What a beautiful dance! The whole reef is clapping!",
		"floor_col": Color(0.62, 0.45, 0.72), "trim": Color(1.0, 0.72, 0.86), "curtain": Color(0.55, 0.3, 0.62)},
	{"name": "The Candy Parade", "career": "Candy Maker", "costume": "candymaker", "emoji": "🍬", "story": 1, "type": "show",
		"kind": "press", "candies": 7,
		"voice": "Candy Maker Roshan! Watch the golden star slide — tap PRESS when it's in the green middle to stamp a smiley candy!",
		"win_line": "Seven smiley candies! The sweetest show the reef has ever tasted!",
		"floor_col": Color(0.78, 0.5, 0.58), "trim": Color(1.0, 0.75, 0.82), "curtain": Color(0.82, 0.35, 0.5)},
	{"name": "The Curtain Dragon", "career": "Curtain Dragon", "costume": "", "emoji": "🐉", "story": 1, "type": "boss",
		"kind": "boss", "boss_hp": 9, "peek_time": 5.0, "hide_time": 3.5,
		"voice": "A grumbly dragon is hiding in the curtains! Be brave — tap SPARKLE when he peeks out!",
		"win_line": "The dragon isn't grumbly anymore — he just wanted to be in the show!",
		"floor_col": Color(0.45, 0.3, 0.4), "trim": Color(1.0, 0.65, 0.4), "curtain": Color(0.62, 0.2, 0.28)},
	# ---------- FLOOR 2: the Starlight Balcony ----------
	{"name": "The Plushy Checkup", "career": "Doctor", "costume": "doctor", "emoji": "🩺", "story": 2, "type": "show",
		"kind": "doctor", "imps": 6, "shell": true,
		"voice": "Doctor Roshan is here! The plushy starfish has boo-boos — follow the golden sparkle: listen with the stethoscope, take the temperature, kiss the ouchies better, then the bandage!",
		"win_line": "All better! The plushy starfish feels brand new — best doctor in the sea!",
		"floor_col": Color(0.75, 0.82, 0.9), "trim": Color(0.7, 0.95, 1.0), "curtain": Color(0.4, 0.55, 0.75)},
	{"name": "The Piggy Picnic", "career": "Farmer", "costume": "farmer", "emoji": "🐷", "story": 2, "type": "show",
		"kind": "scroll", "piggies": 9,
		"voice": "Farmer Roshan! The meadow is sliding by and the piggies are SO hungry — tap TOSS when a piggy is close to throw it a yummy veggie!",
		"win_line": "Nine happy piggies with full tummies! Best picnic the farm has ever had!",
		"floor_col": Color(0.55, 0.75, 0.5), "trim": Color(0.95, 0.9, 0.55), "curtain": Color(0.4, 0.6, 0.35)},
	{"name": "The Championship Bout", "career": "Boxer", "costume": "boxer", "emoji": "🥊", "story": 2, "type": "show",
		"kind": "box", "rounds": [3, 4, 5],
		"voice": "Boxer Roshan, into the ring! Bop the mischief imps with PUNCH — three rounds to win the championship belt!",
		"win_line": "And the winner is... ROSHAN! The sparkly championship belt is hers!",
		"floor_col": Color(0.55, 0.32, 0.3), "trim": Color(1.0, 0.82, 0.45), "curtain": Color(0.72, 0.2, 0.24)},
	{"name": "The Magic Hat Trick", "career": "Magician", "costume": "magician", "emoji": "🎩", "story": 2, "type": "show",
		"kind": "shuffle", "rounds": 4, "imps": 5, "shell": true,
		"voice": "Abracadabra! Watch the bunny-fish hop under a hat, keep your eyes on it, then pick the right one!",
		"win_line": "Magic! The bunny-fish says you have the sharpest eyes in the sea!",
		"floor_col": Color(0.36, 0.3, 0.55), "trim": Color(0.85, 0.7, 1.0), "curtain": Color(0.4, 0.22, 0.6)},
	{"name": "The Shadow Phantom", "career": "Shadow Phantom", "costume": "", "emoji": "🌙", "story": 2, "type": "boss",
		"kind": "boss", "dual": true, "boss_hp": 7, "peek_time": 5.0, "hide_time": 3.4,
		"voice": "A shy shadow is hiding on the stage! Light the twinkling lantern with SHINE, then tap SPARKLE when he peeks!",
		"win_line": "The shadow was a lonely little phantom — now he's the star of the curtain call!",
		"floor_col": Color(0.24, 0.22, 0.42), "trim": Color(0.95, 0.9, 0.6), "curtain": Color(0.16, 0.14, 0.34)},
	# ---------- FLOOR 3: the Grand Gallery ----------
	{"name": "Paint the Sunrise", "career": "Painter", "costume": "painter", "emoji": "🎨", "story": 3, "type": "show",
		"kind": "order", "props": "paint", "order": [2, 0, 1, 2], "flow": "carry_paint", "decorate": 3, "decorate_theme": "splatter", "imps": 5, "shell": true,
		"voice": "Painter Roshan! Dip your brush in the pot the picture shows, swipe the big canvas, then SPLAT some sparkle paint to finish!",
		"win_line": "The sunrise backdrop is finished! It's a masterpiece!",
		"floor_col": Color(0.65, 0.5, 0.42), "trim": Color(1.0, 0.82, 0.55), "curtain": Color(0.75, 0.42, 0.3)},
	{"name": "The Bubble Rocket", "career": "Astronaut Engineer", "costume": "astronaut", "emoji": "🚀", "story": 3, "type": "show",
		"kind": "fix", "imps": 6, "shell": true,
		"voice": "Astronaut Engineer Roshan! The bubble rocket's pipes are broken — carry each piece to the gap with the same picture, then spin the valve!",
		"win_line": "The bubbles reached the rocket! Three, two, one — TWINKLE-OFF!",
		"floor_col": Color(0.3, 0.34, 0.55), "trim": Color(0.7, 0.9, 1.0), "curtain": Color(0.22, 0.26, 0.5)},
	{"name": "The Opera Grand Prix", "career": "Racecar Driver", "costume": "racer", "emoji": "🏎", "story": 3, "type": "show",
		"kind": "race",
		"voice": "Racecar Driver Roshan! One special lap of the Opera Grand Prix — steer, grab the zoom strips, and tap TURBO to fly!",
		"win_line": "What a race! The whole audience is waving checkered flags!",
		"floor_col": Color(0.4, 0.4, 0.48), "trim": Color(1.0, 0.95, 0.95), "curtain": Color(0.85, 0.25, 0.3)},
	{"name": "The Starlight Concert", "career": "Pop Star", "costume": "popstar", "emoji": "🎤", "story": 3, "type": "show",
		"kind": "dance",
		"voice": "Pop Star Roshan! Tap the sparkling microphone, then dance the floating arrows to make rainbow magic!",
		"win_line": "The crowd is singing along! Pop Star Roshan, the reef's biggest star!",
		"floor_col": Color(0.5, 0.3, 0.6), "trim": Color(1.0, 0.7, 0.95), "curtain": Color(0.45, 0.2, 0.55)},
	{"name": "The Grand Finale", "career": "Midnight Maestro", "costume": "", "emoji": "🎼", "story": 3, "type": "boss",
		"kind": "boss", "finale": true, "boss_hp": 9, "peek_time": 5.0, "hide_time": 3.2,
		"voice": "The Midnight Maestro wants to steal the whole show! Use everything you've learned — SHINE the lanterns and SPARKLE when he peeks!",
		"win_line": "The Maestro just wanted to conduct the grand finale — now the whole opera sings together!",
		"floor_col": Color(0.16, 0.14, 0.3), "trim": Color(1.0, 0.88, 0.45), "curtain": Color(0.1, 0.09, 0.24)},
]

const L := Vector3(0.0, -2650.0, 0.0)   # lobby centre — 50 under the act stage, no overlap
const MOVE_SPEED := 13.0
const FLOOR_YS := [0.0, 13.0, 26.0]     # ground, Starlight Balcony, Grand Gallery
const ALL_STARS := (1 << 15) - 1

var m: ReefMain
var finish_cb: Callable
var state := "lobby"                    # lobby | leaving | done
var act: OperaAct = null
var act_index := -1
var doors: Array[Dictionary] = []
var boss_spots: Array[Dictionary] = []
var lifts: Array[Dictionary] = []
var lobby_root: Node3D = null
var lobby_pos := Vector3.ZERO
var lobby_y := 0.0                      # one of FLOOR_YS (tweened by the lifts)
var lift_busy := false
var avatar: Sprite3D = null
var cam: Camera3D = null
var hud: CanvasLayer = null
var star_label: Label = null
var pointer: Node3D = null
var prev_env: Environment = null
var elapsed := 0.0
var hint_t := 0.0
var materials := {}

func start(main: ReefMain, _checkpoint: int, done_cb: Callable) -> void:
	m = main
	finish_cb = done_cb
	lobby_pos = L + Vector3(0, 1.1, 16.0)
	lobby_y = 0.0
	_build_environment()
	_build_lobby()
	_build_doors()
	_build_boss_spots()
	_build_lifts()
	_build_avatar()
	_build_camera()
	_build_hud()
	_update_stars()
	m._sparkle_burst(lobby_pos + Vector3(0, 2.5, 0), Color(1.0, 0.85, 1.0))
	m.show_msg("Roshan", "Welcome to the Pearl Opera House! Every door is a different show — walk right in when one twinkles at you!", "talk")

# ---------------- primitive helpers (mirrors OperaAct's toy-set style) ----------------

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
	var target: Node3D = lobby_root if parent == null else parent
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

func _lobby_prop(fname: String, pos: Vector3, yaw: float = 0.0, prop_scale: float = 1.0) -> Node3D:
	# authored opera GLBs (tools/build_opera_house_art.py); callers keep their
	# primitive builders as the fallback whenever a file is missing
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
	prop.scale = Vector3.ONE * prop_scale
	lobby_root.add_child(prop)
	return prop

func _label(text: String, pos: Vector3, size: int, col: Color, parent: Node3D = null) -> Label3D:
	var lb := Label3D.new()
	lb.text = text
	lb.font_size = size
	lb.pixel_size = 0.03
	lb.outline_size = 10
	lb.modulate = col
	lb.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lb.position = pos
	var target: Node3D = lobby_root if parent == null else parent
	target.add_child(lb)
	return lb

# ---------------- the lobby world ----------------

func _build_environment() -> void:
	prev_env = m.we_node.environment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.05, 0.035, 0.10)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1.0, 0.9, 0.82)
	env.ambient_light_energy = 1.05
	env.glow_enabled = true
	env.glow_intensity = 0.5
	env.glow_bloom = 0.08
	m._speedy_glow_clamp(env)
	m.we_node.environment = env

func _build_lobby() -> void:
	lobby_root = Node3D.new()
	lobby_root.name = "OperaLobby"
	add_child(lobby_root)
	var sun := DirectionalLight3D.new()
	sun.light_color = Color(1.0, 0.92, 0.8)
	sun.light_energy = 1.0
	sun.shadow_enabled = m.quality != "speedy"
	sun.rotation_degrees = Vector3(-52, -24, 0)
	lobby_root.add_child(sun)
	var plum := Color(0.34, 0.24, 0.4)
	var gold := Color(1.0, 0.84, 0.5)
	var crimson := Color(0.66, 0.16, 0.24)
	var wallc := Color(0.5, 0.2, 0.28)
	# grand floor, red carpet runner + gold edging
	_box(L + Vector3(0, -0.3, 0), Vector3(78, 1.2, 46), plum)
	_box(L + Vector3(0, 0.32, 2.0), Vector3(11, 0.14, 40), crimson)
	for cx in [-5.9, 5.9]:
		_box(L + Vector3(cx, 0.36, 2.0), Vector3(0.7, 0.16, 40), gold, 0.2)
	# walls + ceiling (three storeys of soft theatre red)
	_box(L + Vector3(0, 23.0, -22.6), Vector3(78, 47, 1.2), wallc)
	_box(L + Vector3(-38.6, 23.0, 0), Vector3(1.2, 47, 46), wallc)
	_box(L + Vector3(38.6, 23.0, 0), Vector3(1.2, 47, 46), wallc)
	# the front stays OPEN like a dollhouse diorama — the follow camera watches
	# the lobby from the auditorium side over a low gold balustrade
	_box(L + Vector3(0, 1.2, 22.3), Vector3(78, 2.4, 0.8), wallc)
	_box(L + Vector3(0, 2.6, 22.3), Vector3(78, 0.5, 0.6), gold, 0.15)
	_box(L + Vector3(0, 46.6, 0), Vector3(78, 1.2, 46), Color(0.28, 0.18, 0.32))
	for wx in [-38.0, 38.0]:
		_box(L + Vector3(wx, 5.4, 0), Vector3(0.5, 0.7, 46), gold, 0.15)
	_box(L + Vector3(0, 5.4, -22.0), Vector3(78, 0.7, 0.5), gold, 0.15)
	# the two upper storeys: back mezzanines with gold railings + lift landings
	for fi in range(1, FLOOR_YS.size()):
		var fy := float(FLOOR_YS[fi])
		_box(L + Vector3(0, fy - 0.25, -17.0), Vector3(78, 0.5, 10.4), Color(0.42, 0.3, 0.46))
		for lx in [-33.0, 33.0]:
			_box(L + Vector3(lx, fy - 0.25, -9.0), Vector3(8.5, 0.5, 6.4), Color(0.42, 0.3, 0.46))
		var railing_glb := ResourceLoader.exists("res://assets/art35/opera/opera_railing.glb")
		if railing_glb:
			for ri in range(12):
				_lobby_prop("opera_railing.glb", L + Vector3(-33.0 + float(ri) * 6.0, fy, -11.9))
		else:
			for ri in range(13):
				var rx := -36.0 + float(ri) * 6.0
				_box(L + Vector3(rx, fy + 1.5, -11.9), Vector3(0.35, 3.0, 0.35), gold, 0.1)
			_box(L + Vector3(0, fy + 3.1, -11.9), Vector3(78, 0.5, 0.45), gold, 0.2)
	# chandeliers over the open hall (authored GLB with primitive fallback)
	for cx2 in [-18.0, 18.0]:
		if _lobby_prop("opera_chandelier.glb", L + Vector3(cx2, 35.2, 8.0)) == null:
			var ring := TorusMesh.new()
			ring.inner_radius = 1.7
			ring.outer_radius = 2.3
			_mesh(ring, L + Vector3(cx2, 36.0, 8.0), gold, 0.3)
			_sphere(L + Vector3(cx2, 35.2, 8.0), 1.0, Color(1.0, 0.95, 0.75), 1.0)
	# the THEATRE'S GRAND STAGE fronts the ground floor (owner 2026-07-21):
	# a proscenium arch and swagged curtains frame the centre-stage medallion
	# zone, and the footlit apron marks where the big shows take the boards
	_lobby_prop("opera_arch.glb", L + Vector3(0, 0, -19.5))
	_lobby_prop("opera_curtain.glb", L + Vector3(-8.6, 0, -20.6))
	_lobby_prop("opera_curtain.glb", L + Vector3(8.6, 0, -20.6), 180.0)
	_lobby_prop("opera_stage_apron.glb", L + Vector3(0, 0, -10.2))
	# the theatre crest over the top gallery
	_label("🎭", L + Vector3(0, 41.5, -21.4), 120, Color(1.0, 0.92, 0.7))
	_label("★", L + Vector3(0, 37.0, -21.4), 64, Color(1.0, 0.88, 0.45))
	# foyer greenery + poster cards from the converted flat library: coral
	# planters along the side walls, flower cards by the benches (Codex guide)
	var foyer_cards: Array = [
		["gen2/coral1_Image_0_flat", Vector3(-35.0, 2.6, 16.0), 2.2],
		["gen2/coral3_Image_0_flat", Vector3(35.0, 2.6, 16.0), 2.2],
		["gen2/coral5_Image_0_flat", Vector3(-35.0, 2.6, 6.0), 2.0],
		["gen2/coral2_Image_0_flat", Vector3(35.0, 2.6, 6.0), 2.0],
		["mg/flower2", Vector3(-27.5, 2.2, 16.5), 1.6],
		["mg/flower3", Vector3(27.5, 2.2, 16.5), 1.6],
		["mg/star", Vector3(0.0, 5.2, 21.8), 2.0],
	]
	for fc: Array in foyer_cards:
		var cpath := "res://assets/art35/cards/" + String(fc[0]) + ".glb"
		if ResourceLoader.exists(cpath):
			var cpacked := load(cpath) as PackedScene
			if cpacked != null:
				var cprop := cpacked.instantiate() as Node3D
				if cprop != null:
					cprop.position = L + (fc[1] as Vector3)
					cprop.rotation_degrees = Vector3(90.0, 0.0, 0.0)
					cprop.scale = Vector3.ONE * float(fc[2])
					lobby_root.add_child(cprop)
	# padded audience benches by the entrance (pure set dressing)
	for bz in [14.0, 18.5]:
		for bx in [-22.0, 22.0]:
			if _lobby_prop("opera_bench.glb", L + Vector3(bx, 0.6, bz)) == null:
				_box(L + Vector3(bx, 1.1, bz), Vector3(10, 1.0, 2.6), crimson)
				_box(L + Vector3(bx, 2.0, bz + 1.0), Vector3(10, 1.4, 0.6), Color(0.5, 0.13, 0.2))

func _build_doors() -> void:
	# four career doors per floor: ground shows line the side walls, the two
	# gallery floors line their upper back walls. Bosses have no doors — see
	# _build_boss_spots for the centre-stage medallions.
	var spots: Array = [
		{"i": 0, "base": Vector3(-37.2, 0, -2), "face": Vector3(1, 0, 0)},      # chef
		{"i": 1, "base": Vector3(-37.2, 0, 12), "face": Vector3(1, 0, 0)},      # detective
		{"i": 2, "base": Vector3(37.2, 0, -2), "face": Vector3(-1, 0, 0)},      # ballerina
		{"i": 3, "base": Vector3(37.2, 0, 12), "face": Vector3(-1, 0, 0)},      # candy maker
		{"i": 5, "base": Vector3(-27, 13.0, -21.4), "face": Vector3(0, 0, 1)},  # doctor
		{"i": 6, "base": Vector3(-9, 13.0, -21.4), "face": Vector3(0, 0, 1)},   # farmer
		{"i": 7, "base": Vector3(9, 13.0, -21.4), "face": Vector3(0, 0, 1)},    # opera star
		{"i": 8, "base": Vector3(27, 13.0, -21.4), "face": Vector3(0, 0, 1)},   # magician
		{"i": 10, "base": Vector3(-27, 26.0, -21.4), "face": Vector3(0, 0, 1)}, # painter
		{"i": 11, "base": Vector3(-9, 26.0, -21.4), "face": Vector3(0, 0, 1)},  # astronaut
		{"i": 12, "base": Vector3(9, 26.0, -21.4), "face": Vector3(0, 0, 1)},   # racecar
		{"i": 13, "base": Vector3(27, 26.0, -21.4), "face": Vector3(0, 0, 1)},  # pop star
	]
	for spot: Dictionary in spots:
		var i := int(spot["i"])
		var cfg: Dictionary = ACTS[i]
		var base: Vector3 = L + (spot["base"] as Vector3)
		var face: Vector3 = spot["face"]
		var root := Node3D.new()
		root.position = base
		root.rotation.y = atan2(face.x, face.z)
		lobby_root.add_child(root)
		var trim: Color = Color(cfg.get("trim", Color(1.0, 0.85, 0.55)))
		var curtain: Color = Color(cfg.get("curtain", Color(0.78, 0.24, 0.34)))
		var door_glb := _lobby_prop("opera_door.glb", base, rad_to_deg(atan2(face.x, face.z)))
		if door_glb == null:
			_box(Vector3(0, 4.6, -0.35), Vector3(5.4, 9.2, 0.5), Color(0.16, 0.1, 0.2), 0.0, root)
			_box(Vector3(0, 4.3, -0.05), Vector3(4.5, 8.4, 0.3), curtain, 0.06, root)
			for px in [-2.65, 2.65]:
				_box(Vector3(px, 4.8, 0.1), Vector3(0.75, 9.6, 0.75), trim, 0.14, root)
			_box(Vector3(0, 9.7, 0.1), Vector3(6.1, 0.85, 0.85), trim, 0.14, root)
		_label(String(cfg.get("emoji", "★")), Vector3(0, 11.2, 0.4), 40, Color(1, 1, 1), root)
		var veil := _box(Vector3(0, 3.6, 0.5), Vector3(3.7, 6.6, 0.2), Color(1.0, 0.78, 0.5), 0.5, root)
		var vmat := veil.material_override as StandardMaterial3D
		vmat = vmat.duplicate() as StandardMaterial3D
		vmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		vmat.albedo_color = Color(1.0, 0.78, 0.5, 0.34)
		veil.material_override = vmat
		var star := _label("★", Vector3(0, 13.0, 0.5), 58, Color(1.0, 0.88, 0.4), root)
		star.visible = false
		doors.append({"i": i, "cfg": cfg, "root": root, "veil": veil, "star": star,
			"pos": base + face * 1.8 + Vector3(0, 1.1, 0), "front": base + face * 5.2 + Vector3(0, 1.1, 0),
			"armed": true, "cool": 0.0, "hint_cool": 0.0})

func _build_boss_spots() -> void:
	# one centre-stage medallion per floor: dim until the floor's four shows
	# are starred, then it glows gold and swimming onto it starts the boss
	# the ground medallion sits ON the grand stage boards, framed by the
	# proscenium — shows belong on the stage (owner 2026-07-21)
	var layout: Array = [
		{"story": 1, "i": 4, "pos": Vector3(0, 0, -16)},
		{"story": 2, "i": 9, "pos": Vector3(0, 13.0, -17)},
		{"story": 3, "i": 14, "pos": Vector3(0, 26.0, -17)},
	]
	for entry: Dictionary in layout:
		var i := int(entry["i"])
		var cfg: Dictionary = ACTS[i]
		var pos: Vector3 = L + (entry["pos"] as Vector3)
		var medallion_glb := _lobby_prop("opera_medallion.glb", pos)
		# the glow disc floats just over the authored relief so the lit/unlit
		# state stays readable without z-fighting the gold star inlay
		var disc_y := 0.72 if medallion_glb != null else 0.25
		var disc := _cyl(pos + Vector3(0, disc_y, 0), 3.4, 0.5, Color(0.3, 0.22, 0.38), 0.05)
		disc.material_override = (disc.material_override as StandardMaterial3D).duplicate() as StandardMaterial3D
		var ring := TorusMesh.new()
		ring.inner_radius = 3.3
		ring.outer_radius = 3.8
		var halo := _mesh(ring, pos + Vector3(0, 0.35, 0), Color(1.0, 0.85, 0.45), 0.4)
		halo.material_override = (halo.material_override as StandardMaterial3D).duplicate() as StandardMaterial3D
		var crest := _label(String(cfg.get("emoji", "★")), pos + Vector3(0, 3.4, 0), 44, Color(1, 1, 1))
		var star := _label("★", pos + Vector3(0, 5.4, 0), 58, Color(1.0, 0.88, 0.4))
		star.visible = false
		boss_spots.append({"i": i, "cfg": cfg, "story": int(entry["story"]), "pos": pos + Vector3(0, 1.1, 0),
			"disc": disc, "halo": halo, "crest": crest, "star": star,
			"armed": true, "cool": 0.0, "hint_cool": 0.0})

func _build_lifts() -> void:
	# glowing bubble columns at the mezzanine landings: swim in to ride up one
	# floor (the top gallery ride loops gently back to the ground floor)
	for lx in [-33.0, 33.0]:
		var pos := L + Vector3(lx, 0, -9.0)
		if _lobby_prop("opera_lift.glb", pos) == null:
			var col := _cyl(pos + Vector3(0, 13.5, 0), 2.7, 30.0, Color(0.6, 0.9, 1.0), 0.35)
			var cmat := col.material_override as StandardMaterial3D
			cmat = cmat.duplicate() as StandardMaterial3D
			cmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			cmat.albedo_color = Color(0.6, 0.9, 1.0, 0.22)
			col.material_override = cmat
		for b in range(5):
			_sphere(pos + Vector3(randf_range(-1.4, 1.4), 2.0 + float(b) * 5.5, randf_range(-1.4, 1.4)), 0.4, Color(0.8, 0.97, 1.0), 0.7)
		_label("✨", pos + Vector3(0, 5.0, 1.8), 34, Color(0.85, 0.98, 1.0))
		lifts.append({"pos": pos, "armed": true})

func _build_avatar() -> void:
	avatar = Sprite3D.new()
	var tex := load("res://assets/characters/roshan_sprite.png") as Texture2D
	avatar.texture = tex
	avatar.pixel_size = 6.2 / maxf(float(tex.get_height()), 1.0) if tex != null else 0.01
	avatar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	avatar.position = lobby_pos
	lobby_root.add_child(avatar)
	# the golden usher-sparkle that points to the next open show
	pointer = Node3D.new()
	lobby_root.add_child(pointer)
	_sphere(Vector3.ZERO, 0.5, Color(1.0, 0.9, 0.4), 1.2, pointer)
	_label("★", Vector3(0, 1.0, 0), 30, Color(1.0, 0.9, 0.45), pointer)

func _build_camera() -> void:
	cam = Camera3D.new()
	cam.fov = 58.0
	cam.position = lobby_pos + Vector3(0, 16.0, 21.0)
	add_child(cam)
	cam.look_at(lobby_pos + Vector3(0, 2.0, 0), Vector3.UP)
	cam.make_current()

func _build_hud() -> void:
	hud = CanvasLayer.new()
	hud.layer = 16
	add_child(hud)
	var strip := Panel.new()
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.03, 0.1, 0.9)
	style.border_color = Color(1.0, 0.82, 0.5)
	style.set_border_width_all(3)
	style.set_corner_radius_all(20)
	strip.add_theme_stylebox_override("panel", style)
	strip.position = Vector2(30, 620)
	strip.size = Vector2(240, 80)
	strip.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hud.add_child(strip)
	star_label = Label.new()
	star_label.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	star_label.add_theme_font_size_override("font_size", 34)
	star_label.add_theme_color_override("font_outline_color", Color(0.02, 0.02, 0.08))
	star_label.add_theme_constant_override("outline_size", 7)
	star_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	star_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	star_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	strip.add_child(star_label)
	var home := Button.new()
	home.text = "⌂"
	home.position = Vector2(1138, 24)
	home.size = Vector2(112, 100)
	home.add_theme_font_size_override("font_size", 58)
	var home_style := StyleBoxFlat.new()
	home_style.bg_color = Color(0.2, 0.18, 0.38, 0.94)
	home_style.border_color = Color(1.0, 0.86, 0.5)
	home_style.set_border_width_all(4)
	home_style.set_corner_radius_all(28)
	home.add_theme_stylebox_override("normal", home_style)
	home.add_theme_stylebox_override("hover", home_style)
	home.add_theme_stylebox_override("pressed", home_style)
	home.pressed.connect(_leave_early)
	hud.add_child(home)

# ---------------- stars, medallions and the celebration ----------------

func _star_count() -> int:
	var stars := 0
	for i in range(ACTS.size()):
		if m.opera_stars & (1 << i):
			stars += 1
	return stars

func _floor_shows_starred(story: int) -> bool:
	for cfg_i in range(ACTS.size()):
		var cfg: Dictionary = ACTS[cfg_i]
		if int(cfg.get("story", 1)) == story and String(cfg.get("type", "show")) == "show":
			if (m.opera_stars & (1 << cfg_i)) == 0:
				return false
	return true

func _spot_lit(spot: Dictionary) -> bool:
	return _floor_shows_starred(int(spot["story"]))

func _update_stars() -> void:
	for door in doors:
		(door["star"] as Label3D).visible = (m.opera_stars & (1 << int(door["i"]))) != 0
	for spot in boss_spots:
		var lit := _spot_lit(spot)
		var starred: bool = (m.opera_stars & (1 << int(spot["i"]))) != 0
		(spot["star"] as Label3D).visible = starred
		(spot["crest"] as Label3D).visible = lit
		var dmat := (spot["disc"] as MeshInstance3D).material_override as StandardMaterial3D
		var hmat := (spot["halo"] as MeshInstance3D).material_override as StandardMaterial3D
		if lit:
			dmat.albedo_color = Color(1.0, 0.85, 0.45)
			dmat.emission_enabled = true
			dmat.emission = Color(1.0, 0.85, 0.45)
			dmat.emission_energy_multiplier = 0.7
			hmat.emission_energy_multiplier = 0.9
		else:
			dmat.albedo_color = Color(0.3, 0.22, 0.38)
			dmat.emission_energy_multiplier = 0.0
			hmat.emission_energy_multiplier = 0.12
	if star_label != null:
		star_label.text = "★ %d / %d" % [_star_count(), ACTS.size()]

# ---------------- door + medallion + lift flow ----------------

func _start_act(i: int) -> void:
	act_index = i
	var cfg: Dictionary = (ACTS[i] as Dictionary).duplicate()
	cfg["act_tag"] = String(cfg["name"]) + "  "
	lobby_root.visible = false
	act = OperaAct.new()
	add_child(act)
	act.start(m, cfg, Callable(self, "_act_won"))

func _enter_door(door: Dictionary) -> void:
	var cfg: Dictionary = door["cfg"]
	# the Showtime transformation moment at the threshold
	m._sparkle_burst((door["pos"] as Vector3) + Vector3(0, 2.5, 0), Color(1.0, 0.85, 1.0))
	m._sparkle_burst((door["pos"] as Vector3) + Vector3(0, 0.8, 0), Color(0.72, 0.95, 1.0))
	m.show_msg("Roshan", "%s! Costume time — %s Roshan!" % [String(cfg["name"]), String(cfg["career"])], "talk")
	_start_act(int(door["i"]))

func _enter_spot(spot: Dictionary) -> void:
	var cfg: Dictionary = spot["cfg"]
	m._sparkle_burst((spot["pos"] as Vector3) + Vector3(0, 2.5, 0), Color(1.0, 0.88, 0.5))
	m._sparkle_burst((spot["pos"] as Vector3) + Vector3(0, 0.8, 0), Color(1.0, 0.7, 0.4))
	m.show_msg("Roshan", "The centre stage is glowing — %s! The BIG show is starting!" % String(cfg["name"]), "talk")
	_start_act(int(spot["i"]))

func _act_won() -> void:
	var finished := act_index
	act = null
	act_index = -1
	var first_time: bool = (m.opera_stars & (1 << finished)) == 0
	m.opera_stars |= 1 << finished
	m.pearl_count += 3 if first_time else 1
	m.opera_progress = _star_count()
	if m.opera_stars == ALL_STARS and not m.opera_done:
		m.opera_done = true
		m.pearl_count += 50
		m.award_sticker("showtime")
	m._write_save()
	m._update_hud()
	_return_to_lobby(finished)

func _return_to_lobby(finished: int) -> void:
	lobby_root.visible = true
	var back := lobby_pos
	var back_y := lobby_y
	for door in doors:
		if int(door["i"]) == finished:
			back = door["front"] as Vector3
			door["armed"] = false
			door["cool"] = 3.0
	for spot in boss_spots:
		if int(spot["i"]) == finished:
			back = (spot["pos"] as Vector3) + Vector3(0, 0, 6.0)
			spot["armed"] = false
			spot["cool"] = 3.0
	lobby_pos = back
	back_y = 0.0
	for fy in FLOOR_YS:
		if absf((back.y - 1.1) - (L.y + float(fy))) < 3.0:
			back_y = float(fy)
	lobby_y = back_y
	if cam != null:
		cam.make_current()
	_update_stars()
	if m.opera_stars == ALL_STARS:
		m.show_msg("Roshan", "Every show and every big finale — all three floors! Take a bow, Opera Star Roshan!", "win")
		for i in range(10):
			m._sparkle_burst(L + Vector3(randf_range(-30.0, 30.0), randf_range(3.0, 40.0), randf_range(-18.0, 18.0)), Color.from_hsv(randf(), 0.5, 1.0))
	else:
		m.show_msg("Roshan", "A gold star for that show! Pick the next door whenever you're ready!", "win")

func _tick_doors(delta: float) -> void:
	for door in doors:
		door["cool"] = maxf(0.0, float(door["cool"]) - delta)
		var dist: float = (door["pos"] as Vector3).distance_to(lobby_pos)
		if dist > 6.5:
			door["armed"] = true
			continue
		if dist < 3.4 and bool(door["armed"]) and float(door["cool"]) <= 0.0:
			door["armed"] = false
			door["cool"] = 5.0
			_enter_door(door)
			return
	for spot in boss_spots:
		spot["cool"] = maxf(0.0, float(spot["cool"]) - delta)
		spot["hint_cool"] = maxf(0.0, float(spot["hint_cool"]) - delta)
		var sdist: float = (spot["pos"] as Vector3).distance_to(lobby_pos)
		if sdist > 6.5:
			spot["armed"] = true
			continue
		if sdist < 3.5 and bool(spot["armed"]) and float(spot["cool"]) <= 0.0:
			if not _spot_lit(spot):
				spot["armed"] = false
				spot["cool"] = 4.0
				if float(spot["hint_cool"]) <= 0.0:
					spot["hint_cool"] = 8.0
					m.show_msg("Roshan", "The centre stage lights up when this floor's four shows have stars! Follow the golden sparkle!", "hint")
				continue
			spot["armed"] = false
			spot["cool"] = 5.0
			_enter_spot(spot)
			return

func _tick_lifts(_delta: float) -> void:
	for lift in lifts:
		var lp: Vector3 = lift["pos"]
		var flat := Vector2(lobby_pos.x - lp.x, lobby_pos.z - lp.z).length()
		if flat > 6.0:
			lift["armed"] = true
			continue
		if lift_busy or not bool(lift["armed"]) or flat > 2.9:
			continue
		lift["armed"] = false
		lift_busy = true
		# ride up one floor; from the top gallery the bubbles loop gently home
		var fi := 0
		for k in range(FLOOR_YS.size()):
			if absf(lobby_y - float(FLOOR_YS[k])) < 3.0:
				fi = k
		var to_y := float(FLOOR_YS[(fi + 1) % FLOOR_YS.size()])
		m._sparkle_burst(lobby_pos + Vector3(0, 2.0, 0), Color(0.7, 0.95, 1.0))
		var tw := create_tween()
		tw.tween_property(self, "lobby_y", to_y, 1.9 if to_y < lobby_y else 1.4).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
		tw.tween_callback(_lift_done)

func _lift_done() -> void:
	lift_busy = false
	m._sparkle_burst(lobby_pos + Vector3(0, 2.0, 0), Color(0.7, 0.95, 1.0))

func _pointer_target() -> Vector3:
	# nearest un-starred show door on this floor; a lit, un-starred medallion
	# outranks doors (the floor finale is the natural next beat); if this floor
	# is finished the sparkle waits at a bubble lift
	var best := Vector3.INF
	var best_d := 1e9
	for door in doors:
		if (m.opera_stars & (1 << int(door["i"]))) != 0:
			continue
		var dpos: Vector3 = door["pos"]
		if absf((dpos.y - 1.1) - (L.y + lobby_y)) > 3.0:
			continue
		var d := dpos.distance_to(lobby_pos)
		if d < best_d:
			best_d = d
			best = dpos
	for spot in boss_spots:
		if (m.opera_stars & (1 << int(spot["i"]))) != 0 or not _spot_lit(spot):
			continue
		var spos: Vector3 = spot["pos"]
		if absf((spos.y - 1.1) - (L.y + lobby_y)) > 3.0:
			continue
		return spos
	if best != Vector3.INF:
		return best
	if m.opera_stars == ALL_STARS:
		return Vector3.INF
	return (lifts[0]["pos"] as Vector3) + Vector3(0, lobby_y + 1.5, 0) if lifts.size() > 0 else Vector3.INF

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

func _process(delta: float) -> void:
	if m == null or state != "lobby" or act != null:
		return
	elapsed += delta
	if not lift_busy:
		var move := _move_input()
		lobby_pos += Vector3(move.x, 0, move.y) * MOVE_SPEED * delta
	# stay inside the hall; each mezzanine is the back deck plus its two lift
	# landings at the front corners
	lobby_pos.x = clampf(lobby_pos.x, L.x - 36.0, L.x + 36.0)
	if lobby_y > 6.0 and not lift_busy:
		var zmax := (L.z - 13.2) if absf(lobby_pos.x - L.x) < 28.5 else (L.z - 6.2)
		lobby_pos.z = clampf(lobby_pos.z, L.z - 20.5, zmax)
	else:
		lobby_pos.z = clampf(lobby_pos.z, L.z - 20.5, L.z + 20.5)
	lobby_pos.y = L.y + lobby_y + 1.1
	avatar.position = lobby_pos + Vector3(0, sin(elapsed * 4.0) * 0.12, 0)
	if cam != null:
		var want := lobby_pos + Vector3(0, 16.0, 21.0)
		cam.position = cam.position.lerp(want, minf(1.0, delta * 5.0))
		cam.look_at(lobby_pos + Vector3(0, 2.0, 0), Vector3.UP)
	_tick_lifts(delta)
	_tick_doors(delta)
	if pointer != null:
		var target := _pointer_target()
		pointer.visible = target != Vector3.INF
		if pointer.visible:
			# lobby_root sits at the origin, so child positions are world positions
			pointer.position = target + Vector3(0, 3.4 + sin(elapsed * 3.0) * 0.4, 0)
	# a gentle repeating voice hint while nothing is starred yet
	hint_t += delta
	if hint_t > 24.0 and m.opera_stars == 0:
		hint_t = 0.0
		m.show_msg("Roshan", "Pick any twinkling door and walk right in — the show will teach you everything!", "hint")

# ---------------- exits ----------------

func _leave_early() -> void:
	if state != "lobby":
		return
	state = "leaving"
	if act != null:
		# a show in mid-performance keeps its star for next time only if it
		# already took its bow; cancel() handles both paths kindly
		act.cancel()
		act = null
	var completed: bool = m.opera_done
	m.show_msg("Roshan", "The whole opera sparkles!" if completed else "The Opera House will keep every star safe — come back for the next show!", "win" if completed else "home")
	_finish(completed)

func _finish(completed: bool) -> void:
	if state == "done":
		return
	state = "done"
	if prev_env != null:
		m.we_node.environment = prev_env
	if finish_cb.is_valid():
		finish_cb.call(completed)
	queue_free()

func action_label() -> String:
	if act != null:
		return act.action_label()
	return "SWIM"
