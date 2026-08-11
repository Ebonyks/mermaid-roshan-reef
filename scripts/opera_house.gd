class_name OperaHouse
extends Node
## Shipping builds use a direct touch-first Canvas lobby. The retired 3D
## navigation lobby remains headless-only for its detailed regression probe.

const Lobby2D := preload("res://scripts/opera_lobby_2d.gd")
# The Pearl Opera House (Peach Showtime model): an explorable THREE-floor
# theatre lobby. Thirteen careers are marquee doors: four on each of the first
# two floors and five on the Grand Gallery. Nursery Nurse is displayed as job
# 12, before Pop Star, while its appended save bit keeps old stars compatible.
# Roshan swims the hall, walks into a door, transforms, and plays that one
# show. Bosses do NOT use doors (owner 2026-07-21): when a floor's shows are
# starred, the centre of that floor's stage lights up and swimming onto the
# glowing medallion starts the boss. Bubble lifts cycle
# ground → balcony → top gallery → ground. OperaAct owns every performance;
# this class owns the lobby world, door/medallion flow, star checkpoints
# (m.opera_stars bitmask) and safe exits.

const ACTS := [
	# ---------- FLOOR 1: the Lagoon Lights Stage ----------
	{"name": "The Castle Bake-Off", "career": "Pastry Chef", "costume": "chef", "emoji": "🍰", "story": 1, "type": "show",
		"kind": "order", "music": "opera_chef", "props": "cake", "order": [0, 2, 1, 0, 2], "finale": "stir", "decorate": 4, "imps": 6, "shell": true,
		"rescue": "farmers", "gift": "carrots", "uses": "carrots",
		"voice": "Chef hat on! You and the pastry imp each have a kitchen. Sift, pour, stir, bake, pipe and decorate the brightest celebration cake for the crowd!",
		"win_line": "Roshan's celebration cake wins the Castle Bake-Off!",
		"floor_col": Color(0.72, 0.5, 0.62), "trim": Color(1.0, 0.78, 0.86), "curtain": Color(0.85, 0.3, 0.4)},
	{"name": "The Two-Detective Mystery", "career": "Detective", "costume": "detective", "emoji": "🔍", "story": 1, "type": "show",
		"kind": "sleuth", "music": "opera_detective", "props_n": 12, "clues": 5, "imps": 6, "shell": true,
		"rescue": "stagehands", "gift": "lanterns", "uses": "lanterns",
		"voice": "Detective Roshan and the detective imp are solving the SAME case! Find five clues before the timer; if the imp gets there first, watch the answer and race the remembered mystery again!",
		"win_line": "Case closed! Roshan solved the Two-Detective Mystery!",
		"floor_col": Color(0.42, 0.46, 0.62), "trim": Color(0.72, 0.85, 1.0), "curtain": Color(0.3, 0.35, 0.6)},
	{"name": "The Mermaid Pearl Ballet Party", "career": "Ballerina", "costume": "ballerina", "emoji": "🩰", "story": 1, "type": "show",
		"kind": "echo", "music": "opera_ballerina", "pads": 3, "rounds": [2, 3, 3], "pitch": 0.6,
		"silence_entry_voice": true,
		"rescue": "dancers", "gift": "ribbons", "rescue_imps": 4,
		"voice": "Mermaid ballet party! Hold pearl poses, guide the glowing ribbon, and finish with one beautiful grand twirl!",
		"win_line": "Roshan's pearl-ribbon ballet ends with a beautiful grand twirl!",
		"floor_col": Color(0.62, 0.45, 0.72), "trim": Color(1.0, 0.72, 0.86), "curtain": Color(0.55, 0.3, 0.62)},
	{"name": "The Candy Workshop Cup", "career": "Candy Maker", "costume": "candymaker", "emoji": "🍬", "story": 1, "type": "show",
		"kind": "press", "music": "opera_candymaker", "candies": 9,
		"rescue": "sweet-shop mice", "gift": "sugar", "rescue_imps": 4,
		"voice": "Candy Maker Roshan! Mix, sort, wrap and load your parade candies while the candy imp runs the rival workshop!",
		"win_line": "Roshan's smiling sweets win the Candy Workshop Cup!",
		"floor_col": Color(0.78, 0.5, 0.58), "trim": Color(1.0, 0.75, 0.82), "curtain": Color(0.82, 0.35, 0.5)},
	{"name": "The Curtain Dragon", "career": "Curtain Dragon", "costume": "", "emoji": "🐉", "story": 1, "type": "boss",
		"kind": "boss", "music": "opera_boss_dragon", "boss_hp": 15, "peek_time": 5.0, "hide_time": 5.0,
		"voice": "A grumbly dragon is hiding in the curtains! Be brave — tap SPARKLE when he peeks out!",
		"win_line": "The dragon isn't grumbly anymore — he just wanted to be in the show!",
		"floor_col": Color(0.45, 0.3, 0.4), "trim": Color(1.0, 0.65, 0.4), "curtain": Color(0.62, 0.2, 0.28)},
	# ---------- FLOOR 2: the Starlight Balcony ----------
	{"name": "The Stuffie Surgeon Relay", "career": "Stuffie Surgeon", "costume": "doctor", "emoji": "🩺", "story": 2, "type": "show",
		"kind": "doctor", "music": "opera_doctor", "imps": 6, "shell": true, "patients": 4,
		"voice": "Stuffie Surgeon Roshan and the surgeon imp each have a plushy-care station. Find each ouch, check the X-ray and wrap every soft cast with care!",
		"win_line": "Every stuffie is wiggling again — Roshan wins the surgeon relay!",
		"floor_col": Color(0.75, 0.82, 0.9), "trim": Color(0.7, 0.95, 1.0), "curtain": Color(0.4, 0.55, 0.75)},
	{"name": "The Piggy Picnic Challenge", "career": "Farmer", "costume": "farmer", "emoji": "🐷", "story": 2, "type": "show",
		"kind": "scroll", "music": "opera_farmer", "piggies": 12,
		"rescue": "farmers", "gift": "carrots", "rescue_imps": 5,
		"voice": "Farmer Roshan! Plant, feed and guide your piggies while the farmer imp tends the next meadow lane. Make the happiest herd!",
		"win_line": "Roshan's happy herd wins the Piggy Picnic Challenge!",
		"floor_col": Color(0.55, 0.75, 0.5), "trim": Color(0.95, 0.9, 0.55), "curtain": Color(0.4, 0.6, 0.35)},
	{"name": "The Friendly Championship Bout", "career": "Boxer", "costume": "boxer", "emoji": "🥊", "story": 2, "type": "show",
		"kind": "box", "music": "opera_boxer", "rounds": [4, 5, 6], "warmup": 5,
		"rescue": "the ring crew", "gift": "gloves", "rescue_imps": 4,
		"voice": "Boxer Roshan, into the ring! Warm up, then fight one padded boxer imp for three friendly rounds. Punch on the beat and duck the counter-glove!",
		"win_line": "And the winner of the friendly championship is... ROSHAN!",
		"floor_col": Color(0.55, 0.32, 0.3), "trim": Color(1.0, 0.82, 0.45), "curtain": Color(0.72, 0.2, 0.24)},
	{"name": "The Grand Illusion Duel", "career": "Magician", "costume": "magician", "emoji": "🎩", "story": 2, "type": "show",
		"kind": "shuffle", "music": "opera_magician", "rounds": 6, "imps": 5, "shell": true,
		"rescue": "usher crabs", "gift": "silk scarves", "uses": "silk scarves",
		"voice": "Abracadabra! Face the magician imp in a whole illusion duel: hide and track the bunny-fish, melt the rope, open the cabinet and charge the giant star portal!",
		"win_line": "Roshan's star portal wins the Grand Illusion Duel!",
		"floor_col": Color(0.36, 0.3, 0.55), "trim": Color(0.85, 0.7, 1.0), "curtain": Color(0.4, 0.22, 0.6)},
	{"name": "The Shadow Phantom", "career": "Shadow Phantom", "costume": "", "emoji": "🌙", "story": 2, "type": "boss",
		"kind": "boss", "music": "opera_boss_phantom", "dual": true, "boss_hp": 12, "lanterns": 5, "peek_time": 5.0, "hide_time": 4.0,
		"voice": "A shy shadow is hiding on the stage! Light the twinkling lantern with SHINE, then tap SPARKLE when he peeks!",
		"win_line": "The shadow was a lonely little phantom — now he's the star of the curtain call!",
		"floor_col": Color(0.24, 0.22, 0.42), "trim": Color(0.95, 0.9, 0.6), "curtain": Color(0.16, 0.14, 0.34)},
	# ---------- FLOOR 3: the Grand Gallery ----------
	{"name": "The Sunrise Paint-Off", "career": "Painter", "costume": "painter", "emoji": "🎨", "story": 3, "type": "show",
		"kind": "paint", "music": "opera_painter", "props": "paint", "order": [2, 0, 1, 2, 0], "flow": "carry_paint", "decorate": 5, "decorate_theme": "splatter", "imps": 5, "shell": true,
		"rescue": "painter", "gift": "paints", "uses": "paints",
		"voice": "Painter Roshan! You and the painter imp have matching easels. Trace, fill and paint your sunrise before the gallery reveal!",
		"win_line": "Roshan's sunrise wins the paint-off and hangs in the gallery!",
		"floor_col": Color(0.65, 0.5, 0.42), "trim": Color(1.0, 0.82, 0.55), "curtain": Color(0.75, 0.42, 0.3)},
	{"name": "The Rocket Repair Race", "career": "Astronaut Engineer", "costume": "astronaut", "emoji": "🚀", "story": 3, "type": "show",
		"kind": "fix", "music": "opera_astronaut", "imps": 6, "shell": true,
		"rescue": "bubble engineers", "gift": "spare pipes", "uses": "spare pipes",
		"voice": "Astronaut Engineer Roshan! Route your bubble pipes while the astronaut imp repairs the rival launch lane, then spin the valve and launch first!",
		"win_line": "Roshan routes the bubbles and wins the Rocket Repair Race!",
		"floor_col": Color(0.3, 0.34, 0.55), "trim": Color(0.7, 0.9, 1.0), "curtain": Color(0.22, 0.26, 0.5)},
	{"name": "The Opera Grand Prix", "career": "Racecar Driver", "costume": "racer", "emoji": "🏎", "story": 3, "type": "show",
		"kind": "race", "music": "opera_racer", "laps": 2,
		"rescue": "pit crew", "gift": "spare wheels", "rescue_imps": 4,
		"voice": "Racecar Driver Roshan! TWO laps against the helmeted rival imp — steer, grab the zoom strips and tap TURBO to fly!",
		"win_line": "Roshan takes the Opera Grand Prix as the audience waves checkered flags!",
		"floor_col": Color(0.4, 0.4, 0.48), "trim": Color(1.0, 0.95, 0.95), "curtain": Color(0.85, 0.25, 0.3)},
	{"name": "The Starlight Sound-Off", "career": "Pop Star", "costume": "popstar", "emoji": "🎤", "story": 3, "type": "show",
		"kind": "dance", "music": "opera_popstar", "rescue": "the band", "gift": "instruments", "rescue_imps": 4,
		"voice": "Pop Star Roshan! The pop-star imp has the other microphone. Dance the floating arrows and lift the crowd higher with every rainbow phrase!",
		"win_line": "Roshan wins the Starlight Sound-Off and the crowd sings along!",
		"floor_col": Color(0.5, 0.3, 0.6), "trim": Color(1.0, 0.7, 0.95), "curtain": Color(0.45, 0.2, 0.55)},
	{"name": "The Grand Finale", "career": "Midnight Maestro", "costume": "", "emoji": "🎼", "story": 3, "type": "boss",
		"kind": "boss", "music": "opera_boss_maestro", "finale": true, "boss_hp": 15, "peek_time": 5.0, "hide_time": 3.2,
		"voice": "The Midnight Maestro wants to steal the whole show! Use everything you've learned — SHINE the lanterns and SPARKLE when he peeks!",
		"win_line": "The Maestro just wanted to conduct the grand finale — now the whole opera sings together!",
		"floor_col": Color(0.16, 0.14, 0.3), "trim": Color(1.0, 0.88, 0.45), "curtain": Color(0.1, 0.09, 0.24)},
	{"name": "The Moonbeam Nursery", "career": "Nursery Nurse", "costume": "nursery", "emoji": "🍼", "story": 3, "type": "show",
		"kind": "nursery", "music": "opera_nursery",
		"voice": "Nursery Nurse Roshan! Work with Nurse Faron to catch the babies, feed them, burp them and tuck every little one into bed!",
		"win_line": "Roshan and Faron tucked every cozy baby into the Moonbeam Nursery!",
		"floor_col": Color(0.45, 0.68, 0.66), "trim": Color(1.0, 0.82, 0.70), "curtain": Color(0.48, 0.38, 0.68)},
]

const L := Vector3(0.0, -2650.0, 0.0)   # lobby centre — 50 under the act stage, no overlap
const MOVE_SPEED := 13.0
const FLOOR_YS := [0.0, 13.0, 26.0]     # ground, Starlight Balcony, Grand Gallery
const ALL_STARS := (1 << 16) - 1
const ROSHAN_SPRITE_LOOP := preload("res://scripts/roshan_sprite_loop.gd")

var m: ReefMain
var finish_cb: Callable
var state := "lobby"                    # lobby | leaving | done
var act: OperaAct = null
var act_index := -1
var doors: Array[Dictionary] = []
var boss_spots: Array[Dictionary] = []
var lifts: Array[Dictionary] = []
var gates: Array[Dictionary] = []
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
var use_lobby_2d := false
var lobby_2d: OperaLobby2D = null
var touch_was_visible := true
var previous_music := ""

func start(main: ReefMain, checkpoint: int, done_cb: Callable) -> void:
	m = main
	finish_cb = done_cb
	previous_music = m.cur_track
	m._play_music("opera_lobby")
	use_lobby_2d = (
		DisplayServer.get_name() != "headless"
		or OS.get_environment("OPERA_FORCE_2D_LOBBY") == "1"
	)
	if use_lobby_2d:
		_start_lobby_2d(checkpoint)
		return
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

func _start_lobby_2d(_checkpoint: int) -> void:
	if m.touch_ui != null:
		touch_was_visible = m.touch_ui.visible
		m.touch_ui.visible = false
	var start_floor := 0
	if _floor_unlocked(3):
		start_floor = 2
	elif _floor_unlocked(2):
		start_floor = 1
	lobby_2d = Lobby2D.new() as OperaLobby2D
	add_child(lobby_2d)
	lobby_2d.setup(
		m,
		ACTS,
		m.opera_stars,
		start_floor,
		Callable(self, "_start_act"),
		Callable(self, "_lobby_locked_hint"),
		Callable(self, "_leave_early")
	)
	m.show_msg("Roshan", "Welcome to the Pearl Opera! Tap a picture to choose our next show!", "talk")

func _lobby_locked_hint(story: int) -> void:
	if story <= 1 or _floor_shows_starred(story):
		m.show_msg("Roshan", "The big floor finale is ready! Tap the glowing finale card!", "hint")
	else:
		var show_count := 5 if story == 3 else 4
		m.show_msg("Roshan", "Win the %d picture shows on this floor, then the big finale lights up!" % show_count, "hint")

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
	# Four career doors occupy each lower floor; the Grand Gallery has five.
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
		{"i": 15, "base": Vector3(37.2, 26.0, -8), "face": Vector3(-1, 0, 0)},  # nursery nurse (job 12)
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
	# one centre-stage medallion per floor: dim until all that floor's shows
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
		# the shell-clasp gate guards each landing (handoff): closed leaves and
		# three dark pearl sockets at first entry; it swings open — leaves fold
		# clear of the lane — once the upstairs floor wakes
		var gate_glb := _lobby_prop("opera_shell_gate.glb", pos + Vector3(0, 0, 3.6))
		var pearls: Array = []
		for pi in range(3):
			var pearl := _sphere(pos + Vector3(-1.1 + float(pi) * 1.1, 5.75, 3.6), 0.26, Color(0.25, 0.2, 0.35), 0.05)
			pearl.material_override = (pearl.material_override as StandardMaterial3D).duplicate() as StandardMaterial3D
			pearls.append(pearl)
		gates.append({"glb": gate_glb, "pearls": pearls, "pos": pos + Vector3(0, 0, 3.6), "open": false})

func _build_avatar() -> void:
	avatar = Sprite3D.new()
	avatar.pixel_size = 6.2 / 256.0
	avatar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	avatar.position = lobby_pos
	lobby_root.add_child(avatar)
	var animator := ROSHAN_SPRITE_LOOP.new()
	avatar.add_child(animator)
	animator.setup_sprite_3d(avatar, false, avatar)
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
	var strip := StorybookUI.add_hud_panel(hud, Rect2(18, 18, 240, 96), StorybookUI.GOLD, Color(1.0, 0.97, 0.86, 0.96), 30)
	strip.name = "OperaProgressCard"
	star_label = Label.new()
	star_label.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	StorybookUI.style_hud_label(star_label, 34)
	star_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	star_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	star_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	strip.add_child(star_label)
	var home := Button.new()
	home.name = "OperaBackButton"
	StorybookUI.style_back_button(home, "Save stars and leave")
	home.position = Vector2(1138, 24)
	home.pressed.connect(_leave_early)
	hud.add_child(home)

# ---------------- stars, medallions and the celebration ----------------

func _star_count() -> int:
	var stars := 0
	for i in range(ACTS.size()):
		if m.opera_stars & (1 << i):
			stars += 1
	return stars

func _floor_unlocked(story: int) -> bool:
	# handoff contract (CLAUDE_OPERA_HOUSE_3D_CONTINUATION_2026-07-21): the
	# ground floor is always open; each upper floor opens when the floor
	# below's BOSS star is earned. Gates, portals, pointer and lifts all
	# consume this one helper.
	if story <= 1:
		return true
	var prior_boss := 4 if story == 2 else 9
	return (m.opera_stars & (1 << prior_boss)) != 0

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
	if use_lobby_2d:
		if lobby_2d != null and is_instance_valid(lobby_2d):
			lobby_2d.refresh(m.opera_stars)
		return
	for door in doors:
		(door["star"] as Label3D).visible = (m.opera_stars & (1 << int(door["i"]))) != 0
		# portals on a locked floor keep their curtains closed and dim
		var unlocked := _floor_unlocked(int((door["cfg"] as Dictionary).get("story", 1)))
		var veil := door["veil"] as MeshInstance3D
		var dvmat := veil.material_override as StandardMaterial3D
		dvmat.albedo_color = Color(1.0, 0.78, 0.5, 0.34) if unlocked else Color(0.5, 0.5, 0.58, 0.14)
		dvmat.emission = Color(1.0, 0.78, 0.5) if unlocked else Color(0.25, 0.25, 0.3)
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
	# shell-clasp gates: pearls light and leaves fold aside once the balcony
	# floor wakes (both landings share the story-2 unlock as the first gate)
	for gate in gates:
		var open := _floor_unlocked(2)
		for pearl_n in (gate["pearls"] as Array):
			var pmat := (pearl_n as MeshInstance3D).material_override as StandardMaterial3D
			pmat.albedo_color = Color(1.0, 0.88, 0.5) if open else Color(0.25, 0.2, 0.35)
			pmat.emission_enabled = open
			if open:
				pmat.emission = Color(1.0, 0.88, 0.5)
				pmat.emission_energy_multiplier = 0.8
		if open and not bool(gate["open"]) and gate["glb"] != null:
			gate["open"] = true
			var glb := gate["glb"] as Node3D
			for leaf in glb.find_children("*", "Node3D", true, false):
				var ln := String((leaf as Node).name)
				if ln.begins_with("leaf_l") or ln.begins_with("leaf_r"):
					var slide := -2.9 if ln.begins_with("leaf_l") else 2.9
					var lt := (leaf as Node3D).create_tween()
					lt.tween_property(leaf, "position:x", (leaf as Node3D).position.x + slide, 0.9).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
	if star_label != null:
		star_label.text = "★ %d / %d" % [_star_count(), ACTS.size()]

# ---------------- door + medallion + lift flow ----------------

func _start_act(i: int) -> void:
	act_index = i
	var cfg: Dictionary = (ACTS[i] as Dictionary).duplicate()
	cfg["act_tag"] = String(cfg["name"]) + "  "
	if bool(cfg.get("silence_entry_voice", false)):
		# A quick lobby tap can arrive while its generic welcome clip is still
		# playing. Clear that pool before the exact ballet teaching line begins.
		for voice_player: AudioStreamPlayer in m.voice_pool:
			voice_player.stop()
		if m.voice != null:
			m.voice.stop()
	if use_lobby_2d:
		if lobby_2d != null and is_instance_valid(lobby_2d):
			lobby_2d.hide_lobby()
		if m.touch_ui != null:
			m.touch_ui.visible = touch_was_visible
	else:
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
	if m.cur_track != "opera_lobby":
		m._play_music("opera_lobby")
	if use_lobby_2d:
		if m.touch_ui != null:
			m.touch_ui.visible = false
		var finished_story := int((ACTS[finished] as Dictionary).get("story", 1))
		var return_floor := finished_story - 1
		if finished == 4 or finished == 9:
			return_floor = mini(2, finished_story)
		if lobby_2d != null and is_instance_valid(lobby_2d):
			lobby_2d.show_lobby(return_floor, m.opera_stars)
		if (finished == 4 or finished == 9) and m.opera_stars != ALL_STARS:
			m.show_msg("Roshan", "The next floor just lit up! Tap its bright number at the top!", "win")
		elif m.opera_stars == ALL_STARS:
			m.show_msg("Roshan", "Every show and every big finale! Take a bow, Opera Star Roshan!", "win")
		else:
			m.show_msg("Roshan", "A gold star for that show! Tap the next sparkling picture!", "win")
		return
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
	# a floor-boss star wakes the next storey (handoff): burst + invitation
	if (finished == 4 or finished == 9) and m.opera_stars != ALL_STARS:
		for lift in lifts:
			m._sparkle_burst((lift["pos"] as Vector3) + Vector3(0, 4.0, 0), Color(0.7, 0.95, 1.0))
		m.show_msg("Roshan", "The whole next floor just woke up! Ride the sparkling bubbles!", "win")
		return
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
			if not _floor_unlocked(int((door["cfg"] as Dictionary).get("story", 1))):
				if float(door["hint_cool"]) <= 0.0:
					door["hint_cool"] = 8.0
					m.show_msg("Roshan", "This floor wakes up after the big show downstairs! Follow the golden sparkle!", "hint")
				continue
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
					m.show_msg("Roshan", "The centre stage lights up when every show on this floor has a star! Follow the golden sparkle!", "hint")
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
		# ride up one floor; from the top gallery the bubbles loop gently home.
		# A lift stays DORMANT toward locked floors (handoff): the cycle skips
		# to the next unlocked destination, and if none exists the bubbles
		# just shimmer with a kindly hint.
		var fi := 0
		for k in range(FLOOR_YS.size()):
			if absf(lobby_y - float(FLOOR_YS[k])) < 3.0:
				fi = k
		var to_fi := (fi + 1) % FLOOR_YS.size()
		while to_fi != fi and not _floor_unlocked(to_fi + 1):
			to_fi = (to_fi + 1) % FLOOR_YS.size()
		if to_fi == fi:
			lift["hint_cool"] = maxf(0.0, float(lift.get("hint_cool", 0.0)))
			if float(lift["hint_cool"]) <= 0.0:
				lift["hint_cool"] = 10.0
				m._sparkle_burst(lp + Vector3(0, 3.0, 0), Color(0.7, 0.9, 1.0))
				# pulse the three pearl sockets on the nearest gate (handoff)
				for gate in gates:
					if (gate["pos"] as Vector3).distance_to(lp) < 8.0:
						for pearl_n in (gate["pearls"] as Array):
							m._sparkle_burst((pearl_n as MeshInstance3D).position + Vector3(0, 0.8, 0), Color(1.0, 0.88, 0.5))
				m.show_msg("Roshan", "The bubbles are still sleepy! Win the big centre-stage show first!", "hint")
			continue
		lift_busy = true
		var to_y := float(FLOOR_YS[to_fi])
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
	if use_lobby_2d:
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
	if use_lobby_2d:
		if lobby_2d != null and is_instance_valid(lobby_2d):
			lobby_2d.close()
			lobby_2d = null
		if m.touch_ui != null:
			m.touch_ui.visible = touch_was_visible
	if prev_env != null:
		m.we_node.environment = prev_env
	if previous_music != "":
		m._play_music(previous_music)
	previous_music = ""
	if finish_cb.is_valid():
		finish_cb.call(completed)
	queue_free()

func action_label() -> String:
	if act != null:
		return act.action_label()
	return "PICK A SHOW" if use_lobby_2d else "SWIM"
