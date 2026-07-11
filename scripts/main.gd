extends Node3D
# Mermaid Roshan's Ocean World — Godot phase 2
# Undersea fairy garden (Kenney Nature Kit, CC0) + PBR seabed + rainbow pearls + 5 minigames.

const WATER_TOP := 58.0
const WORLD_R := 270.0
const PEARL_TOTAL := 10

var player: Node3D
var pearls: Array[Node3D] = []
var friends: Array = []
var pearl_count := 0
var trophies := 0
var hud_pearls: Label
var hud_stars: Label
var hud_msg: Label
var hud_game: Label
var msg_timer := 0.0
var voice: AudioStreamPlayer
var model_cache := {}
var cluster_centers: Array[Vector3] = []
var pulse_lights: Array = []        # dicts {light, base, phase}
var fish_schools: Array = []
var manta: Node3D
var manta_t := -20.0
var bloom_t := 25.0
var bloom_parts: GPUParticles3D

# ---------- minigame state ----------
var game := ""              # "", "fetch", "dolls", "seek", "race", "melody"
var g := {}                 # per-game scratch
var game_nodes: Array[Node3D] = []
var world_env: Environment
var arena_env: Environment
var we_node: WorldEnvironment
var music: AudioStreamPlayer
var return_pos := Vector3.ZERO
const ARENA_POS := Vector3(0, -600, 0)
const LEVEL2_POS := Vector3(0, -1300, 0)
const CASTLE_POS := Vector3(500, -1300, 0)
var arena_center := Vector3(0, -600, 0)
var arena_dome := 48.0
var arena_ceil := 42.0
var portal_node: Node3D
var portal_t := 0.0
var portal_ready := false
var portal_cool := 0.0
var portal_armed := false
var draining := false
var drain_t := 0.0
var level2_done_once := false
var l2_stars: Array = []
var l2_door: MeshInstance3D = null
var rainbow_slide_mode := false
var level2_finishing := false
var custom_fish: Array = []
var craft_layer: CanvasLayer = null
var craft_body := Color(0.4, 0.7, 1.0)
var craft_fins := Color(1.0, 0.6, 0.2)
var craft_fishbox: Control = null
var craft_kind := "fish"
var craft_body_rb := false
var craft_fins_rb := false
var custom_friends: Array = []
const CREATURE_LAYERS := {"fish": ["fish_fins", "fish_body", "fish_line"], "cat": ["cat_body", "cat_body", "cat_line"], "bird": ["bird_body", "bird_body", "bird_line"]}
var l2_open := false
var l2_cutscene_t := -1.0
var wall_pics: Array = []
# Soft-collision: vertical-cylinder colliders for big overworld structures
# (rock outcrops, shipwreck). Each entry: {x, z, r, y0, y1}. The player reads
# this list in player.gd and is pushed out of any cylinder it enters. Only
# consulted in the open-world state (game == ""); arenas use their own bounds.
var solids: Array = []
# Same idea for arena interiors (castle hall, levels). Rebuilt on every arena
# entry so colliders never leak between levels. Box entries are axis-aligned
# walls; cylinder entries are columns. Consulted by player.gd in the arena branch.
var arena_solids: Array = []
var fade_walls: Array = []   # interior walls that fade out when they block the camera
var mg_cool := 0.0
var mg2d_layer: CanvasLayer
var mg2d_root: Control
var mg2d_stage: Control
var mg_kind := ""
var mg := {}
var _nat_cache := {}

# ---- 3.0: platform / persistence / flow ----
const SAVE_PATH := "user://reef_save.json"
const GTA := "res://assets/terrain/"
var touch_ui: CanvasLayer
var quality := "sparkly"
var music_on := true
var save_data := {}
var plays := 0           # launch counter — alternates day/night across playthroughs
var is_night := false    # subtle day/night variation for both worlds
var lagoon_floor := false  # when true, the player's floor follows the Sky Lagoon heightfield
var pearl_lights: Array = []
var sun_light: DirectionalLight3D
var caustics_mat: ShaderMaterial = null   # terrain-conforming light dapples (day/night tuned)
var plankton_node: GPUParticles3D
# ---- WW motion language: one global wind drives streaks, water lines, seagrass
# sway and flags (via the wind_dir/wind_gust shader globals) so gusts roll
# coherently across the whole world instead of every prop looping on its own ----
var wind_t := 0.0
var wind_dir_v := Vector3(0.85, 0.0, 0.53)
var wind_gust_v := 0.6
var wind_streaks: Array = []   # pooled curl ribbons: {node, mat, age, life}
var streak_ctx := "none"       # "sea" | "sky" | "off" — restyled when it changes
var surf_rings: Array = []     # pooled expanding rings on the water underside
var ring_cool := 0.0
var flag_sh: Shader = null
var pause_layer: CanvasLayer
var pause_panel: Control
var quality_btn: Button
var music_btn: Button
var guide_fish: Sprite3D
var finale_done := false
var finale_t := -1.0
var finale_nodes: Array = []
var hint_idx := 0
var hint_t := 0.0
var anim_cull: Array = []
var cull_timer := 0.0
var wreck_pos := Vector3.ZERO
var shop_cool := 0.0
var treasure_cool := 0.0
# Cosmetics are full alternative skins (mutually exclusive), chosen at the bedroom wardrobe.
# "classic" is the default 3D Roshan; others swap her to a full-skin billboard.
# (The Fairy Mermaid is NOT a wardrobe skin — it is Roshan's look inside the Fairy Pond game.)
const SKINS := [
	{"id": "classic", "label": "Roshan", "preview": "res://assets/characters/roshan_sprite.png", "sprite": ""}]
const FAIRY_SKIN_PATH := "res://assets/characters/skins/fairy_mermaid.png"
var skin_id := "classic"
var wardrobe_layer: CanvasLayer = null
var wd: Dictionary = {}              # live references to dress-up UI controls
var treasure_fr := {"fname": "Secret Cave", "game": "treasure", "won": true, "cool": 0.0}
var shop_fr := {"fname": "Pearl Shop", "game": "shop", "won": true, "cool": 0.0}
var slide_fr := {"fname": "Penguin Slide", "game": "slide", "theme": "ice", "mode": "chase", "won": true, "cool": 0.0}
var slide_cool := 0.0
var slide_portal_pos := Vector3.ZERO
var slide_portal_penguin: Node3D = null
var fairy_fr := {"fname": "Fairy Pond", "game": "fairyshoot", "won": true, "cool": 0.0}
var fairy_pond_pos := Vector3.ZERO
var fairy_cool := 0.0
var shop_msg_cool := 0.0
var pearl_slots: Array = []
var pearl_mat: ShaderMaterial
var pearl_note := 0
const PENT := [0, 2, 4, 5, 7, 9, 11]   # C major diatonic scale
var speed_mult := 1.0
var beans_t := -1.0
var fart_t := 0.0
var cur_track := ""
var prev_track := ""
const SHOP_ITEMS := [
	{"id": "beans", "label": "Can of Beans", "price": 2}]
var flora_nodes: Array = []
var first_session := true
var chime: AudioStreamPlayer
var buy_sound: AudioStreamPlayer
var whale_node: Node3D
var voice_pool: Array = []
var voice_i := 0
var said_cool := {}
var roshan_spot_cool := 0.0
var idle_voice_t := 9.0
var intro_active := false
var intro_layer: CanvasLayer
var intro_idx := 0
var intro_art: TextureRect
var intro_art2: TextureRect
var intro_text: Label
const BTN_COLS := [Color(0.35, 0.95, 0.4), Color(1.0, 0.35, 0.35), Color(0.4, 0.55, 1.0), Color(1.0, 0.9, 0.35)]  # A B X Y
const BTN_OFFS := [Vector3(0, 0, 9), Vector3(9, 0, 0), Vector3(-9, 0, 0), Vector3(0, 0, -9)]                     # bottom right left top

const FRIEND_DEFS := [
	{"tex": "pearl_friend",  "fname": "Evie and Lamb-a'",      "msg": "You found us! Swim close again to play hide and seek!", "game": "seek"},
	{"tex": "two_friends",   "fname": "Harper and Fiona",      "msg": "Sisters Harper and Fiona! Come grab the fish down the rainbow slide!", "game": "slide", "theme": "rainbow", "mode": "fish"},
	{"tex": "mama_baby",     "fname": "Faron",                 "msg": "Faron and her dolls! Return to catch the sleepy dolls!", "game": "dolls"},
	{"tex": "gabby",         "fname": "Gabby",                 "msg": "Gabby! Come catch the rainbow on stage!", "game": "melody"},
	{"tex": "wacky_chuck",   "fname": "Wacky and Chuck",       "msg": "Wacky! And Chuck! Come back to play fetch!", "game": "fetch"},
]

static func hash2(x: float, y: float) -> float:
	var n: float = sin(x * 127.1 + y * 311.7) * 43758.5453
	return n - floorf(n)

static func vnoise(x: float, y: float) -> float:
	var xi: float = floorf(x)
	var yi: float = floorf(y)
	var xf: float = x - xi
	var yf: float = y - yi
	var u: float = xf * xf * (3.0 - 2.0 * xf)
	var v: float = yf * yf * (3.0 - 2.0 * yf)
	var a: float = hash2(xi, yi)
	var b: float = hash2(xi + 1.0, yi)
	var c: float = hash2(xi, yi + 1.0)
	var d: float = hash2(xi + 1.0, yi + 1.0)
	return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v

static func fbm(x: float, y: float) -> float:
	return vnoise(x, y) * 0.55 + vnoise(x * 2.3 + 5.0, y * 2.3 + 5.0) * 0.3 + vnoise(x * 5.1 + 9.0, y * 5.1 + 9.0) * 0.15

static func seabed_y(x: float, z: float) -> float:
	var h: float = fbm(x * 0.013, z * 0.013) * 26.0 - 6.0
	h += maxf(0.0, fbm(x * 0.05 + 30.0, z * 0.05 + 30.0) - 0.62) * 30.0
	var d := sqrt(x * x + z * z)
	if d > WORLD_R * 0.82:
		h += (d - WORLD_R * 0.82) * 0.55
	return h

func _ready() -> void:
	_build_environment()
	_build_terrain()
	_build_water()
	_build_wind_streaks()
	_build_surf_rings()
	_build_garden()
	_build_meadows()
	_build_aquatic_flora()
	_build_aquatic_creatures()
	_build_wreck()
	_build_events()
	_build_pearls()
	_build_friends()
	_build_player()
	_build_hud()
	voice = AudioStreamPlayer.new()
	voice.stream = load("res://assets/audio/voice_yay.mp3")
	add_child(voice)
	chime = AudioStreamPlayer.new()
	chime.stream = load("res://assets/audio/chime.ogg")
	chime.volume_db = -4.0
	add_child(chime)
	buy_sound = AudioStreamPlayer.new()
	buy_sound.stream = load("res://assets/audio/buy.ogg")
	add_child(buy_sound)
	for vp in range(4):
		var ap := AudioStreamPlayer.new()
		add_child(ap)
		voice_pool.append(ap)
	touch_ui = preload("res://scripts/touch_ui.gd").new()
	add_child(touch_ui)
	_build_guide()
	_build_slide_portal()
	_build_pause()
	_load_save()

const INTRO_PANELS := [
	{"title": "Princess Huluu", "art": ["huluu"], "vo": "intro1", "text": "Princess Huluu lives in a kingdom in the sky."},
	{"title": "The Storm", "art": ["huluu"], "vo": "intro2", "text": "A storm swept her down to the sea!"},
	{"title": "Best Friends", "art": ["roshan"], "vo": "intro3", "text": "Roshan says: I will help you, Huluu!"},
	{"title": "Go Home Together", "art": ["roshan", "huluu"], "vo": "intro4", "text": "Find the pearls. Open the sky river. Take Huluu home!"}]

func _build_intro() -> void:
	intro_active = true
	intro_idx = 0
	intro_layer = CanvasLayer.new()
	intro_layer.layer = 20
	intro_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	add_child(intro_layer)
	# tap-anywhere advance button (full screen, transparent)
	var tap := Button.new()
	tap.set_anchors_preset(Control.PRESET_FULL_RECT)
	tap.flat = true
	tap.focus_mode = Control.FOCUS_NONE
	var clear := StyleBoxEmpty.new()
	tap.add_theme_stylebox_override("normal", clear)
	tap.add_theme_stylebox_override("hover", clear)
	tap.add_theme_stylebox_override("pressed", clear)
	tap.pressed.connect(_intro_next)
	intro_layer.add_child(tap)
	# soft underwater backdrop
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.05, 0.13, 0.26)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	intro_layer.add_child(bg)
	var glowtop := ColorRect.new()
	glowtop.set_anchors_preset(Control.PRESET_TOP_WIDE)
	glowtop.custom_minimum_size = Vector2(0, 360)
	glowtop.size = Vector2(1280, 360)
	glowtop.color = Color(0.12, 0.30, 0.45, 0.6)
	glowtop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	intro_layer.add_child(glowtop)
	# two character slots
	intro_art = TextureRect.new()
	intro_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	intro_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
	intro_art.custom_minimum_size = Vector2(360, 560)
	intro_art.size = Vector2(360, 560)
	intro_art.position = Vector2(470, 70)
	intro_art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	intro_layer.add_child(intro_art)
	intro_art2 = TextureRect.new()
	intro_art2.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	intro_art2.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
	intro_art2.custom_minimum_size = Vector2(300, 470)
	intro_art2.size = Vector2(300, 470)
	intro_art2.position = Vector2(760, 150)
	intro_art2.mouse_filter = Control.MOUSE_FILTER_IGNORE
	intro_layer.add_child(intro_art2)
	# narration panel
	var panel := Panel.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = Color(0.04, 0.08, 0.2, 0.92)
	psb.set_corner_radius_all(24)
	psb.border_color = Color(1.0, 0.8, 0.5)
	psb.set_border_width_all(3)
	panel.add_theme_stylebox_override("panel", psb)
	panel.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	panel.position = Vector2(90, 540)
	panel.size = Vector2(1100, 150)
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	intro_layer.add_child(panel)
	intro_text = Label.new()
	intro_text.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	intro_text.offset_left = 30
	intro_text.offset_right = -30
	intro_text.add_theme_font_size_override("font_size", 30)
	intro_text.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.8))
	intro_text.add_theme_constant_override("outline_size", 8)
	intro_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	intro_text.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	intro_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	intro_text.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_child(intro_text)
	# "tap to continue" hint
	var hint := Label.new()
	hint.text = "tap to continue \u25b6"
	hint.add_theme_font_size_override("font_size", 22)
	hint.add_theme_color_override("font_color", Color(1.0, 0.9, 0.6))
	hint.position = Vector2(980, 700)
	hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	intro_layer.add_child(hint)
	_intro_show()

func _intro_tex(key: String) -> Texture2D:
	if key == "huluu":
		return load("res://assets/characters/friends/huluu.png")
	return load("res://assets/characters/roshan_sprite.png")

func _intro_show() -> void:
	var p: Dictionary = INTRO_PANELS[intro_idx]
	intro_text.text = String(p["text"])
	_say("roshan", String(p.get("vo", "")))
	var arts: Array = p["art"]
	intro_art.texture = _intro_tex(String(arts[0]))
	if arts.size() > 1:
		intro_art.position = Vector2(330, 70)
		intro_art2.texture = _intro_tex(String(arts[1]))
		intro_art2.visible = true
	else:
		intro_art.position = Vector2(470, 70)
		intro_art2.visible = false

func _intro_next() -> void:
	intro_idx += 1
	if intro_idx >= INTRO_PANELS.size():
		_skip_intro()
		if voice != null:
			voice.pitch_scale = 1.1
			voice.play()
		return
	if chime != null:
		chime.pitch_scale = 1.0
		chime.play()
	_intro_show()

func _skip_intro() -> void:
	intro_active = false
	if intro_layer != null and is_instance_valid(intro_layer):
		intro_layer.queue_free()
	intro_layer = null

func _tick_roshan_reactions(delta: float, ppos: Vector3) -> void:
	if game != "" or finale_t >= 0.0 or intro_active:
		return
	# idle chatter when she's been drifting calmly for a while
	if player != null and player.vel.length() < 5.0 and msg_timer <= 0.0:
		idle_voice_t -= delta
		if idle_voice_t <= 0.0:
			idle_voice_t = 16.0 + randf() * 10.0
			_say("roshan", ["idle1", "idle2", "idle3"][randi() % 3])
	else:
		idle_voice_t = maxf(idle_voice_t, 6.0)
	roshan_spot_cool = maxf(0.0, roshan_spot_cool - delta)
	if roshan_spot_cool > 0.0:
		return
	# the great whale
	if whale_node != null and is_instance_valid(whale_node) and whale_node.position.distance_to(ppos) < 34.0:
		roshan_spot_cool = 14.0
		_say("roshan", "whale", 12.0)
		show_msg("Roshan", "Wow! A GIANT whale! Hello, big friend!")
		return
	# the floating ghost ship on the water
	if manta != null and is_instance_valid(manta) and manta.position.distance_to(ppos) < 26.0:
		roshan_spot_cool = 14.0
		_say("roshan", "ship", 12.0)
		show_msg("Roshan", "A magic ship on the water! I wonder what is inside...")
		return
	# the sunken pirate ship
	if wreck_pos != Vector3.ZERO and wreck_pos.distance_to(ppos) < 24.0:
		roshan_spot_cool = 14.0
		_say("roshan", "wreck", 12.0)
		show_msg("Roshan", "Ooh, a sunken ship! Maybe there is treasure down there!")
		return

func _apply_time_of_day() -> void:
	# subtle day/night variation for the overworld reef (level2 handles its own in _enter_level2)
	if world_env == null:
		return
	var sky := world_env.sky.sky_material as ProceduralSkyMaterial
	if is_night:
		if sky != null:
			sky.sky_top_color = Color(0.05, 0.13, 0.24)
			sky.sky_horizon_color = Color(0.02, 0.06, 0.13)
			sky.ground_bottom_color = Color(0.01, 0.02, 0.06)
			sky.ground_horizon_color = Color(0.02, 0.05, 0.10)
			sky.energy_multiplier = 0.4
		world_env.ambient_light_color = Color(0.22, 0.36, 0.5)
		world_env.ambient_light_energy = 0.62
		world_env.fog_light_color = Color(0.04, 0.13, 0.22)
		world_env.glow_intensity = 1.0   # bioluminescence reads stronger in the dark
		if caustics_mat != null:          # thin blue moonlight dapples
			caustics_mat.set_shader_parameter("strength", 0.15)
			caustics_mat.set_shader_parameter("tint", Vector3(0.35, 0.55, 0.90))
		if sun_light != null:
			sun_light.light_color = Color(0.42, 0.56, 0.86)
			sun_light.light_energy = 0.3
	else:
		if sky != null:
			sky.sky_top_color = Color(0.16, 0.42, 0.55)
			sky.sky_horizon_color = Color(0.05, 0.17, 0.28)
			sky.ground_bottom_color = Color(0.02, 0.07, 0.13)
			sky.ground_horizon_color = Color(0.05, 0.15, 0.24)
			sky.energy_multiplier = 0.7
		world_env.ambient_light_color = Color(0.46, 0.66, 0.72)
		world_env.ambient_light_energy = 0.9
		world_env.fog_light_color = Color(0.10, 0.26, 0.34)
		world_env.glow_intensity = 0.95
		if caustics_mat != null:          # bright sun dapples
			caustics_mat.set_shader_parameter("strength", 0.30)
			caustics_mat.set_shader_parameter("tint", Vector3(0.50, 0.80, 0.90))
		if sun_light != null:
			sun_light.light_color = Color(0.55, 0.80, 0.98)
			sun_light.light_energy = 0.55

func _grade(env: Environment) -> void:
	# cheap cinematic grade — ACES filmic tonemapping (works on the mobile renderer, ~free)
	env.tonemap_mode = Environment.TONE_MAPPER_ACES
	env.tonemap_exposure = 1.15
	env.tonemap_white = 1.2

func _wind_waker_bloom(env: Environment, intensity: float = 0.95, bloom: float = 0.4, threshold: float = 0.9) -> void:
	# Wind Waker-style bloom: drop the HDR threshold below white so sunlit surfaces
	# (sand, sky, snow, highlights) bleed light — not just emissive materials — and
	# blend a wide + tight glow level pair for the soft dreamy halo. glow_bloom adds
	# the whole-frame haze that gives WW its light-soaked look.
	# threshold: ~0.82 for bright open-sky scenes; keep >= 0.9 in the emissive-heavy
	# underwater world or every glowing prop blows out to a white sheet.
	env.glow_enabled = true
	# SCREEN, not SOFTLIGHT: softlight preserves darks, so unlit props (seagrass
	# cones, rocks) get no bloom at all. Screen composites the blurred glow buffer
	# over the WHOLE frame — with glow_bloom feeding the unthresholded image into
	# that buffer, every object bleeds a soft halo. That's the universal WW wrap.
	env.glow_blend_mode = Environment.GLOW_BLEND_MODE_SCREEN
	env.glow_hdr_threshold = threshold
	env.glow_hdr_scale = 2.4
	env.glow_intensity = intensity
	env.glow_bloom = bloom
	for i in range(7):
		env.set_glow_level(i, 0.0)
	env.set_glow_level(0, 0.35)   # tight sparkle right at the highlight
	env.set_glow_level(2, 1.0)
	env.set_glow_level(4, 1.0)    # wide dreamy halo
	env.set_glow_level(6, 0.35)   # very wide faint wash

func _build_environment() -> void:
	var env := Environment.new()
	# gradient 'underwater sky' — light filtering from the surface above, deep blue below
	env.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var psky := ProceduralSkyMaterial.new()
	psky.sky_top_color = Color(0.16, 0.42, 0.55)
	psky.sky_horizon_color = Color(0.05, 0.17, 0.28)
	psky.sky_curve = 0.25
	psky.ground_bottom_color = Color(0.02, 0.07, 0.13)
	psky.ground_horizon_color = Color(0.05, 0.15, 0.24)
	psky.sun_angle_max = 30.0
	psky.energy_multiplier = 0.7
	sky.sky_material = psky
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	env.ambient_light_sky_contribution = 0.6
	env.ambient_light_color = Color(0.46, 0.66, 0.72)
	env.ambient_light_energy = 0.9
	env.fog_enabled = true
	env.fog_light_color = Color(0.10, 0.26, 0.34)
	env.fog_density = 0.0042
	env.fog_aerial_perspective = 0.75
	env.fog_sky_affect = 0.5
	_wind_waker_bloom(env, 0.95, 0.4, 0.92)   # reef is full of emissive props — bloom only true emitters
	env.adjustment_enabled = true
	env.adjustment_saturation = 1.12
	env.adjustment_contrast = 1.07
	env.adjustment_brightness = 1.02
	_grade(env)
	world_env = env
	we_node = WorldEnvironment.new()
	we_node.environment = env
	add_child(we_node)
	music = AudioStreamPlayer.new()
	add_child(music)
	_play_music("world")
	_build_bubble_columns()
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-55.0, 30.0, 0.0)
	sun.light_color = Color(0.55, 0.80, 0.98)
	sun.light_energy = 0.55
	sun.shadow_enabled = true
	add_child(sun)
	sun_light = sun
	music.process_mode = Node.PROCESS_MODE_ALWAYS
	_build_god_rays()
	# NOTE: the old player-following flat caustics plane is gone — it hovered at
	# one sampled height while the terrain rolled underneath, reading as a layer
	# of lights floating over the ground (and the bloom pass blew its HDR blobs
	# out to white). The terrain-conforming overlay in _add_caustics now carries
	# the dapple look, glued to the actual seabed geometry.

func _build_bubble_columns() -> void:
	for i in range(7):
		var a: float = randf() * TAU
		var r: float = 30.0 + randf() * (WORLD_R * 0.75)
		var bx: float = cos(a) * r
		var bz: float = sin(a) * r
		var by: float = seabed_y(bx, bz)
		var bub := GPUParticles3D.new()
		bub.amount = 22
		bub.lifetime = 5.0
		bub.preprocess = 3.0
		var pm := ParticleProcessMaterial.new()
		pm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_SPHERE
		pm.emission_sphere_radius = 1.2
		pm.gravity = Vector3(0, 6.0, 0)
		pm.initial_velocity_min = 2.0
		pm.initial_velocity_max = 4.0
		pm.scale_min = 0.15
		pm.scale_max = 0.5
		pm.damping_min = 0.5
		pm.damping_max = 1.0
		bub.process_material = pm
		var sm := SphereMesh.new()
		sm.radius = 0.5
		sm.height = 1.0
		sm.radial_segments = 6
		sm.rings = 4
		var bm := StandardMaterial3D.new()
		bm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		bm.albedo_color = Color(0.8, 0.95, 1.0, 0.35)
		bm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		bm.rim_enabled = true
		sm.material = bm
		bub.draw_pass_1 = sm
		bub.position = Vector3(bx, by + 1.0, bz)
		bub.visibility_aabb = AABB(Vector3(-3, 0, -3), Vector3(6, WATER_TOP, 6))
		add_child(bub)

func _build_terrain() -> void:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var seg := 110
	var size := WORLD_R * 2.3
	var c_sand := Color(0.30, 0.46, 0.46)
	var c_deep := Color(0.10, 0.28, 0.32)
	for j in range(seg):
		for i in range(seg):
			var p0 := _terra_pt(i, j, seg, size)
			var p1 := _terra_pt(i + 1, j, seg, size)
			var p2 := _terra_pt(i + 1, j + 1, seg, size)
			var p3 := _terra_pt(i, j + 1, seg, size)
			var mid_y: float = (p0.y + p2.y) * 0.5
			var t := clampf((mid_y + 6.0) / 30.0, 0.0, 1.0)
			t = roundf(t * 3.0) / 3.0
			var col := c_deep.lerp(c_sand, t)
			_emit_tri(st, p0, p1, p2, col)
			_emit_tri(st, p0, p2, p3, col)
	var mesh := st.commit()
	var mi := MeshInstance3D.new()
	mi.mesh = mesh
	var mat := StandardMaterial3D.new()
	mat.vertex_color_use_as_albedo = true
	mat.albedo_texture = load("res://assets/terrain/Ground054_2K_Color.jpg")   # smooth fine sand (the old up_sand read as cracked dry dirt)
	mat.normal_enabled = true
	mat.normal_texture = load("res://assets/terrain/Ground054_2K_NormalGL.jpg")
	mat.roughness_texture = load("res://assets/terrain/Ground054_2K_Roughness.jpg")
	mat.uv1_triplanar = true
	mat.uv1_world_triplanar = true
	mat.uv1_scale = Vector3(0.12, 0.12, 0.12)
	mat.albedo_color = Color(0.35, 0.55, 0.58)
	mi.material_override = mat
	add_child(mi)
	_add_caustics(mesh)
	_add_plankton()

func _add_caustics(terrain_mesh: Mesh) -> void:
	# light dapples glued to the actual seabed: the terrain mesh drawn a second
	# time with an additive caustic pass. Peak brightness stays well under the
	# bloom threshold so the dapples never blow out to white sheets.
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode blend_add, unshaded, depth_draw_never, shadows_disabled;
uniform sampler2D caustic;
uniform float strength = 0.30;
uniform vec3 tint = vec3(0.50, 0.80, 0.90);
void fragment(){
	vec3 wp = (INV_VIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;
	// two counter-scrolling layers + a slow swirl so the dapples wander like real light
	vec2 warp = vec2(sin(TIME * 0.35 + wp.z * 0.05), cos(TIME * 0.28 + wp.x * 0.045)) * 1.6;
	vec2 uv = (wp.xz + warp) * 0.022 + vec2(TIME * 0.010, -TIME * 0.007);
	vec2 uv2 = (wp.xz - warp) * 0.015 - vec2(TIME * 0.006, TIME * 0.009);
	float c = texture(caustic, uv).r * 0.55 + texture(caustic, uv2).r * 0.45;
	c = smoothstep(0.30, 0.95, c);
	ALBEDO = c * tint * strength;
}"""
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("caustic", load("res://assets/terrain/caustics.png"))
	caustics_mat = m
	var mi := MeshInstance3D.new()
	mi.mesh = terrain_mesh
	mi.material_override = m
	mi.position.y = 0.15
	add_child(mi)
func _add_plankton() -> void:
	var parts := GPUParticles3D.new()
	parts.amount = 600
	parts.lifetime = 12.0
	parts.preprocess = 12.0
	var pm := ParticleProcessMaterial.new()
	pm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
	pm.emission_box_extents = Vector3(WORLD_R, WATER_TOP * 0.5, WORLD_R)
	pm.gravity = Vector3(0, 0.15, 0)
	pm.initial_velocity_min = 0.1
	pm.initial_velocity_max = 0.5
	parts.process_material = pm
	var quad := QuadMesh.new()
	quad.size = Vector2(0.22, 0.22)
	var qm := StandardMaterial3D.new()
	qm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	qm.albedo_color = Color(0.85, 0.97, 1.0, 0.5)
	qm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	qm.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	quad.material = qm
	parts.draw_pass_1 = quad
	parts.position = Vector3(0, WATER_TOP * 0.5, 0)
	add_child(parts)
	plankton_node = parts

static func _terra_pt(i: int, j: int, seg: int, size: float) -> Vector3:
	var x: float = (float(i) / float(seg) - 0.5) * size
	var z: float = (float(j) / float(seg) - 0.5) * size
	return Vector3(x, seabed_y(x, z), z)

static func _emit_tri(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, col: Color) -> void:
	var n: Vector3 = (b - a).cross(c - a).normalized()
	if n.y < 0.0:
		n = -n
	for p in [a, b, c]:
		st.set_color(col)
		st.set_normal(n)
		st.add_vertex(p)

func _build_water() -> void:
	var pm := PlaneMesh.new()
	pm.size = Vector2(WORLD_R * 2.6, WORLD_R * 2.6)
	pm.subdivide_width = 56
	pm.subdivide_depth = 56
	var mi := MeshInstance3D.new()
	mi.mesh = pm
	mi.position.y = WATER_TOP
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode cull_disabled;
uniform sampler2D caus;
global uniform vec3 wind_dir;
global uniform float wind_gust;
varying vec2 wxz;
void vertex(){
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz;
	wxz = wp.xz;
	float gg = 0.6 + wind_gust * 0.8;
	VERTEX.y += (sin(TIME*0.9 + wp.x*0.055)*0.9 + cos(TIME*1.25 + wp.z*0.047 + wp.x*0.02)*0.7) * gg;
}
void fragment(){
	vec2 w = wxz;
	vec3 c1 = texture(caus, w*0.012 + vec2(TIME*0.014, TIME*0.008)).rgb;
	vec3 c2 = texture(caus, w*0.027 - vec2(TIME*0.011, -TIME*0.016)).rgb;
	float sparkle = c1.g * c2.g;
	// WW contour strokes: domain-warped bands drifting with the wind
	vec2 luv = w * 0.030 - wind_dir.xz * TIME * (0.35 + wind_gust * 0.75);
	vec2 q = luv + vec2(sin(luv.y * 1.7 + TIME * 0.35), cos(luv.x * 1.9 - TIME * 0.28)) * 0.55;
	float band = sin(q.x * 2.6) * sin(q.y * 2.2 + TIME * 0.4);
	float lines = smoothstep(0.55, 0.78, band) * (1.0 - smoothstep(0.78, 0.99, band));
	lines *= 0.55 + 0.45 * wind_gust;
	vec3 base = vec3(0.16, 0.52, 0.68);
	ALBEDO = base + sparkle * vec3(0.5, 0.85, 0.9) + lines * vec3(0.75, 0.95, 1.0);
	EMISSION = vec3(0.10, 0.32, 0.42) + sparkle * vec3(0.65, 0.95, 1.0) * 0.9 + lines * vec3(0.7, 0.95, 1.0) * 0.8;
	ALPHA = clamp(0.42 + sparkle * 0.25 + lines * 0.35, 0.0, 1.0);
}"""
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("caus", load("res://assets/terrain/caustics.png"))
	mi.material_override = mat
	add_child(mi)
	water_node = mi
	# experimental: real FFT ocean surface on top (GPU compute) — only on a real
	# device, never headless; the plane above stays as a guaranteed fallback
	if use_fft_ocean and not OS.has_feature("headless") and RenderingServer.get_rendering_device() != null:
		get_tree().create_timer(1.2).timeout.connect(_setup_fft_ocean)

var water_node: MeshInstance3D
var water_y0 := 0.0
var use_fft_ocean := false  # FFT surface overflows the per-instance shader-uniform buffer (material_storage.cpp:1794 flood) and is too heavy for the 3-4yo phone target; custom animated water plane is the shipped surface. Set true only for desktop experiments.
var fft_ocean = null
var fft_quad: Node3D = null
var fft_t := 0.0
func _setup_fft_ocean() -> void:
	if not use_fft_ocean or RenderingServer.get_rendering_device() == null:
		return
	var Ocean3D := load("res://addons/tessarakkt.oceanfft/components/Ocean3D.gd")
	var QuadTree3D := load("res://addons/tessarakkt.oceanfft/components/QuadTree3D.gd")
	var omat := load("res://addons/tessarakkt.oceanfft/Ocean.tres")
	if Ocean3D == null or QuadTree3D == null or omat == null:
		return
	# domain-warp noise for the wave detail
	var noise := FastNoiseLite.new()
	noise.noise_type = FastNoiseLite.TYPE_PERLIN
	var ntex := NoiseTexture2D.new()
	ntex.width = 1024
	ntex.height = 1024
	ntex.seamless = true
	ntex.noise = noise
	var ocean = Ocean3D.new()
	ocean.material = omat
	ocean.horizontal_dimension = 512
	ocean.time_scale = 1.1
	ocean.domain_warp_texture = ntex
	# keep it light for the phone target
	ocean.simulation_frameskip = 1
	if ocean.has_method("initialize_simulation"):
		ocean.initialize_simulation()
	fft_ocean = ocean
	var qt: Node3D = QuadTree3D.new()
	var lod_ranges: Array[float] = [250.0, 500.0, 1900.0, 3800.0, 7600.0, 15200.0, 30400.0]
	qt.set("ranges", lod_ranges)
	qt.set("lod_level", lod_ranges.size() - 1)
	qt.set("quad_size", 16384.0)
	qt.set("material", omat)
	qt.position.y = WATER_TOP
	add_child(qt)
	fft_quad = qt
	fft_t = 0.0

func _tick_fft_ocean(delta: float) -> void:
	if fft_ocean == null:
		return
	fft_t += delta
	if not bool(fft_ocean.get("initialized")):
		# give the GPU a few seconds; if it never inits, drop back to the plane
		if fft_t > 5.0:
			use_fft_ocean = false
			if fft_quad != null and is_instance_valid(fft_quad):
				fft_quad.queue_free()
			fft_quad = null
			fft_ocean = null
		return
	# FFT is live — hide the simple plane and run the wave sim
	if water_node != null and is_instance_valid(water_node):
		water_node.visible = false
	if fft_ocean.has_method("simulate"):
		fft_ocean.simulate(delta)

var rock_pbr: StandardMaterial3D
var wood_overlay: StandardMaterial3D

func _texture_mats() -> void:
	rock_pbr = StandardMaterial3D.new()
	rock_pbr.albedo_texture = load("res://assets/terrain/Rock061_2K_Color.jpg")
	rock_pbr.albedo_color = Color(0.62, 0.68, 0.76)
	rock_pbr.normal_enabled = true
	rock_pbr.normal_texture = load("res://assets/terrain/Rock061_2K_NormalGL.jpg")
	rock_pbr.roughness_texture = load("res://assets/terrain/Rock061_2K_Roughness.jpg")
	rock_pbr.uv1_triplanar = true
	rock_pbr.uv1_world_triplanar = true   # static rocks: same texel size no matter the node scale
	rock_pbr.uv1_scale = Vector3(0.3, 0.3, 0.3)
	wood_overlay = StandardMaterial3D.new()
	wood_overlay.albedo_texture = load("res://assets/terrain/up_wood_col.jpg")
	wood_overlay.albedo_color = Color(1.35, 1.3, 1.25)      # lift so MUL keeps base colors
	wood_overlay.normal_enabled = true
	wood_overlay.normal_texture = load("res://assets/terrain/up_wood_nrm.jpg")
	wood_overlay.uv1_triplanar = true
	wood_overlay.uv1_scale = Vector3(0.9, 0.9, 0.9)
	wood_overlay.blend_mode = BaseMaterial3D.BLEND_MODE_MUL
	wood_overlay.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED

func _apply_mat(node: Node, mat: Material, overlay: bool) -> void:
	if node is MeshInstance3D:
		if overlay:
			(node as MeshInstance3D).material_overlay = mat
		else:
			(node as MeshInstance3D).material_override = mat
	for c in node.get_children():
		_apply_mat(c, mat, overlay)

func _spawn(model: String, pos: Vector3, scl: float, yrot: float) -> Node3D:
	if rock_pbr == null:
		_texture_mats()
	if not model_cache.has(model):
		var base := "res://assets/ship/" if model.begins_with("ship") or model in ["chest", "barrel"] else "res://assets/kenney/"
		if not ResourceLoader.exists(base + model + ".glb"):
			model_cache[model] = null
		else:
			model_cache[model] = load(base + model + ".glb")
	var ps: PackedScene = model_cache[model]
	if ps == null:
		return null
	var inst: Node3D = ps.instantiate()
	inst.position = pos
	inst.scale = Vector3.ONE * scl
	inst.rotation.y = yrot
	if model.begins_with("cliff") or model.begins_with("rock"):
		_apply_mat(inst, rock_pbr, false)            # real rock PBR
	elif model.begins_with("ship") or model.begins_with("bridge") or model in ["barrel", "chest", "mast", "stump_round", "stump_roundDetailed", "stump_squareDetailed"]:
		_apply_mat(inst, wood_overlay, true)         # wood grain detail, keeps Kenney colors
	add_child(inst)
	return inst

func _halo(pos: Vector3, col: Color, size: float) -> MeshInstance3D:
	var gt := GradientTexture2D.new()
	gt.fill = GradientTexture2D.FILL_RADIAL
	gt.fill_from = Vector2(0.5, 0.5)
	gt.fill_to = Vector2(0.5, 0.0)
	var gr := Gradient.new()
	gr.set_color(0, Color(col.r, col.g, col.b, 0.55))
	gr.set_color(1, Color(col.r, col.g, col.b, 0.0))
	gt.gradient = gr
	var quad := QuadMesh.new()
	quad.size = Vector2(size, size)
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	m.albedo_texture = gt
	m.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	quad.material = m
	var mi := MeshInstance3D.new()
	mi.mesh = quad
	mi.position = pos
	add_child(mi)
	return mi

func _fairy_light(pos: Vector3, col: Color, hero: bool = false) -> void:
	if hero:
		var l := OmniLight3D.new()
		l.light_color = col
		l.light_energy = 1.8
		l.omni_range = 22.0
		l.position = pos
		add_child(l)
		pulse_lights.append({"light": l, "base": 1.8, "phase": randf() * TAU})
	var halo := _halo(pos, col, 7.0 + (6.0 if hero else 0.0))
	pulse_lights.append({"halo": halo, "base": halo.mesh.size.x if false else 7.0, "phase": randf() * TAU})
	var orb := MeshInstance3D.new()
	var sm := SphereMesh.new()
	sm.radius = 0.35
	sm.height = 0.7
	orb.mesh = sm
	var m := StandardMaterial3D.new()
	m.emission_enabled = true
	m.emission = col
	m.emission_energy_multiplier = 2.5
	orb.material_override = m
	orb.position = pos
	add_child(orb)

func _accumulate_aabb(n: Node, acc: Dictionary) -> void:
	# union of every visual child's AABB, in world space
	if n is VisualInstance3D and (n as VisualInstance3D).is_inside_tree():
		var vi := n as VisualInstance3D
		var ab: AABB = vi.global_transform * vi.get_aabb()
		acc["box"] = (acc["box"] as AABB).merge(ab) if acc.has("box") else ab
	for c in n.get_children():
		_accumulate_aabb(c, acc)

func _register_solid(node: Node3D, tight: float = 0.85, pad: float = 1.6) -> void:
	# approximate a spawned structure with a vertical-cylinder collider derived
	# from its world AABB. tight (<1) pulls the radius in from the box corners so
	# the bubble hugs the model; pad adds clearance for Roshan's body.
	if node == null:
		return
	var acc := {}
	_accumulate_aabb(node, acc)
	if not acc.has("box"):
		return
	var box: AABB = acc["box"]
	var center: Vector3 = box.position + box.size * 0.5
	var r: float = maxf(box.size.x, box.size.z) * 0.5 * tight + pad
	solids.append({
		"x": center.x, "z": center.z, "r": r,
		"y0": box.position.y - pad, "y1": box.position.y + box.size.y + pad,
	})

func _wall_solid(center: Vector3, size: Vector3, pad: float = 1.6) -> void:
	# axis-aligned box collider for an arena wall (player slides along the faces).
	# y range is gated so flat slabs (floors/ceilings) are NOT passed here — only
	# upright walls, columns and furniture the player should not swim through.
	arena_solids.append({
		"box": true,
		"cx": center.x, "cz": center.z,
		"hx": size.x * 0.5 + pad, "hz": size.z * 0.5 + pad,
		"y0": center.y - size.y * 0.5 - pad, "y1": center.y + size.y * 0.5 + pad,
	})

func _cyl_solid(center: Vector3, r: float, half_h: float, pad: float = 1.6) -> void:
	# vertical-cylinder collider for an arena column
	arena_solids.append({
		"box": false,
		"x": center.x, "z": center.z, "r": r + pad,
		"y0": center.y - half_h - pad, "y1": center.y + half_h + pad,
	})

func _iwall(center: Vector3, size: Vector3, col: Color, tex: String = "") -> MeshInstance3D:
	# an interior wall: visible box + solid collider + registered for camera cutaway fade.
	# Optional tex = an up_* PBR key (e.g. "marble") tinted by col; world triplanar keeps
	# the pattern continuous across wall segments and lintels.
	var node := _l2_box(center, size, col)
	if tex != "":
		node.material_override = _up_mat(tex, 0.07, col)
	_wall_solid(center, size)
	var base_a: float = 1.0
	if node.material_override is StandardMaterial3D:
		base_a = (node.material_override as StandardMaterial3D).albedo_color.a
	fade_walls.append({"node": node, "c": center, "h": size * 0.5, "base_a": base_a, "a": base_a})
	return node

func _build_garden() -> void:
	# marine coral groves: rock outcrops + giant anemone heads + kelp columns (Kenney garden retired)
	var fairy_cols := [Color(1.0, 0.55, 0.8), Color(0.5, 0.95, 1.0), Color(1.0, 0.85, 0.45), Color(0.75, 0.6, 1.0)]
	for ci in range(26):
		var a: float = float(ci) / 26.0 * TAU + hash2(ci, 7) * 1.5
		var r: float = 35.0 + hash2(ci, 3) * (WORLD_R * 0.85 - 35.0)
		var cx: float = cos(a) * r
		var cz: float = sin(a) * r
		cluster_centers.append(Vector3(cx, seabed_y(cx, cz), cz))
		# rocky reef heart
		for k in range(2 + randi() % 3):
			var ra: float = randf() * TAU
			var rx: float = cx + cos(ra) * (3.0 + randf() * 8.0)
			var rz: float = cz + sin(ra) * (3.0 + randf() * 8.0)
			var rname := "Rock" if randi() % 12 == 0 else "Rock%d" % (1 + randi() % 11)
			var rock := _place_aq(rname, Vector3(rx, seabed_y(rx, rz) + 0.2, rz), 2.0 + randf() * 2.6, false)
			if rock != null:
				rock.rotation_degrees = Vector3(randf() * 14.0, randf() * 360.0, randf() * 14.0)
				_register_solid(rock)
		# giant glowing anemone crowns on the rocks
		for k in range(3 + randi() % 3):
			var ga: float = randf() * TAU
			var gx: float = cx + cos(ga) * (2.0 + randf() * 9.0)
			var gz: float = cz + sin(ga) * (2.0 + randf() * 9.0)
			var an := MeshInstance3D.new()
			an.mesh = _anemone_mesh()
			an.material_override = _glow_tip_mat()
			var mm0 := an.material_override
			an.scale = Vector3.ONE * (2.4 + randf() * 2.4)
			an.position = Vector3(gx, seabed_y(gx, gz) + 1.6, gz)
			add_child(an)
		# fairy light hero every 6th grove
		_fairy_light(Vector3(cx, seabed_y(cx, cz) + 7.5 + randf() * 3.0, cz), fairy_cols[ci % fairy_cols.size()], ci % 6 == 0)
	# cave landmarks (rock PBR boxes arch)
	for li in range(2):
		var la: float = float(li) * PI + 0.9
		var lx: float = cos(la) * 110.0
		var lz: float = sin(la) * 110.0
		_fairy_light(Vector3(lx, seabed_y(lx, lz) + 5.0, lz), Color(0.6, 1.0, 0.9), true)

func _rainbow_mat() -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nvoid fragment(){\n\tfloat hue = fract(TIME * 0.12 + dot(NORMAL, VIEW) * 0.45);\n\tvec3 c = clamp(abs(fract(hue + vec3(0.0, 0.33, 0.67)) * 6.0 - 3.0) - 1.0, 0.0, 1.0);\n\tALBEDO = mix(vec3(0.95), c, 0.5);\n\tEMISSION = c * 0.8;\n\tROUGHNESS = 0.15;\n\tMETALLIC = 0.5;\n}"
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

var aquatic_movers: Array = []

const AQ_COLORS := {
	"Coral": Color(1.0, 0.45, 0.55), "Coral1": Color(1.0, 0.6, 0.35), "Coral2": Color(0.95, 0.4, 0.75),
	"Coral3": Color(0.7, 0.45, 1.0), "Coral4": Color(1.0, 0.75, 0.35), "Coral5": Color(0.4, 0.8, 1.0),
	"Coral6": Color(1.0, 0.5, 0.4),
	"SeaWeed": Color(0.25, 0.75, 0.45), "SeaWeed1": Color(0.3, 0.8, 0.5), "SeaWeed2": Color(0.2, 0.65, 0.5),
	"Rock": Color(0.45, 0.48, 0.52), "FanShell": Color(1.0, 0.85, 0.75), "SmallFanShell": Color(0.95, 0.8, 0.85),
	"SpiralShell": Color(0.9, 0.82, 0.7), "SandDollar": Color(0.85, 0.8, 0.7), "StarFish": Color(1.0, 0.55, 0.35),
	"Shark": Color(0.45, 0.55, 0.65), "Hammerhead": Color(0.5, 0.58, 0.62), "Whale": Color(0.25, 0.4, 0.55),
	"Dolphin": Color(0.55, 0.7, 0.8), "Turtle": Color(0.4, 0.65, 0.45), "StingRay": Color(0.55, 0.5, 0.6),
	"Squid": Color(0.9, 0.55, 0.6), "Octopus": Color(0.75, 0.4, 0.5), "Eel": Color(0.5, 0.6, 0.4),
	"ClownFish": Color(1.0, 0.5, 0.2), "Dory": Color(0.3, 0.5, 1.0), "Carp": Color(0.8, 0.6, 0.4),
	"Tuna": Color(0.5, 0.6, 0.75), "Crab": Color(0.9, 0.4, 0.3), "Lobster": Color(0.8, 0.3, 0.25),
	"Seal": Color(0.6, 0.55, 0.5), "Penguin": Color(0.3, 0.32, 0.38),
}

func _aq_mat(model: String) -> StandardMaterial3D:
	var key := model
	if model.begins_with("Rock"):
		key = "Rock"
	var cache_key := "aqmat_" + key
	if model_cache.has(cache_key):
		return model_cache[cache_key]
	var col: Color = AQ_COLORS.get(key, Color(0.7, 0.7, 0.75))
	var m := StandardMaterial3D.new()
	m.uv1_triplanar = true
	if key == "Rock":
		# true stone — upgraded CC0 rock face (shared with grove boulders & cavern)
		m.albedo_texture = load("res://assets/terrain/Rock061_2K_Color.jpg")
		m.albedo_color = Color(0.66, 0.7, 0.76)
		m.normal_enabled = true
		m.normal_texture = load("res://assets/terrain/Rock061_2K_NormalGL.jpg")
		m.roughness_texture = load("res://assets/terrain/Rock061_2K_Roughness.jpg")
		m.uv1_world_triplanar = true   # rocks are static; creature materials below stay object-space
		m.uv1_scale = Vector3(0.3, 0.3, 0.3)
	elif key.begins_with("SeaWeed"):
		# leafy — same treatment as the seagrass that reads well
		m.albedo_texture = load("res://assets/terrain/leaf.png")
		m.albedo_color = col * 1.2
		m.normal_enabled = true
		m.normal_texture = load("res://assets/terrain/scales_normal.png")
		m.normal_scale = 0.6
		m.uv1_scale = Vector3(1.8, 1.8, 1.8)
		m.roughness = 0.95
		m.emission_enabled = true
		m.emission = col * 0.25
		m.emission_energy_multiplier = 0.6
	elif key.begins_with("Coral") or key in ["FanShell", "SmallFanShell", "SpiralShell", "SandDollar", "StarFish"]:
		# living coral — polyp detail albedo + bump
		m.albedo_texture = load("res://assets/terrain/polyp.png")
		m.albedo_color = col
		m.normal_enabled = true
		m.normal_texture = load("res://assets/terrain/polyp_normal.png")
		m.normal_scale = 1.2
		m.uv1_scale = Vector3(2.2, 2.2, 2.2)
		m.roughness = 0.85
		m.emission_enabled = true
		m.emission = col * 0.22
		m.emission_energy_multiplier = 0.6
	else:
		# creatures — scaled hide, soft sheen, no washout
		m.albedo_color = col
		m.roughness = 0.65
		m.normal_enabled = true
		m.normal_texture = load("res://assets/terrain/scales_normal.png")
		m.normal_scale = 0.9
		m.uv1_scale = Vector3(2.5, 2.5, 2.5)
		m.rim_enabled = true
		m.rim = 0.25
		m.rim_tint = 0.6
		m.emission_enabled = true
		m.emission = col * 0.12
		m.emission_energy_multiplier = 0.4
	model_cache[cache_key] = m
	return m

func _paint_aq(node: Node, mat: StandardMaterial3D) -> void:
	if node is MeshInstance3D:
		(node as MeshInstance3D).material_override = mat
	for c in node.get_children():
		_paint_aq(c, mat)

func _aq(model: String) -> PackedScene:
	if not model_cache.has("aq_" + model):
		model_cache["aq_" + model] = load("res://assets/aquatic/" + model + ".glb")
	return model_cache["aq_" + model]

func _place_aq(model: String, pos: Vector3, scl: float, play_anim: bool) -> Node3D:
	var ps := _aq(model)
	if ps == null:
		return null
	var inst: Node3D = ps.instantiate()
	inst.position = pos
	inst.scale = Vector3.ONE * scl
	inst.rotation.y = randf() * TAU
	_paint_aq(inst, _aq_mat(model))
	add_child(inst)
	if not play_anim:
		flora_nodes.append(inst)
	if play_anim:
		var ap := _find_anim(inst)
		if ap != null:
			var clips := ap.get_animation_list()
			# prefer a swim/idle loop
			var pick := clips[0]
			for c in clips:
				if "Swim" in c or "Idle" in c:
					pick = c
					break
			var anim := ap.get_animation(pick)
			if anim != null:
				anim.loop_mode = Animation.LOOP_LINEAR
			ap.play(pick)
			ap.speed_scale = 0.6 + randf() * 0.5
			anim_cull.append({"ap": ap, "node": inst})
	return inst

func _find_anim(n: Node) -> AnimationPlayer:
	if n is AnimationPlayer:
		return n
	for c in n.get_children():
		var r := _find_anim(c)
		if r != null:
			return r
	return null

func _build_aquatic_flora() -> void:
	# real corals, seaweed, shells clustered on the reef groves; rocks scattered
	var corals := ["Coral", "Coral1", "Coral2", "Coral3", "Coral4", "Coral5", "Coral6"]
	var weeds := ["SeaWeed", "SeaWeed1", "SeaWeed2"]
	var shells := ["FanShell", "SmallFanShell", "SpiralShell", "SandDollar"]
	var rocks := ["Rock", "Rock1", "Rock2", "Rock3", "Rock4", "Rock5", "Rock6", "Rock7", "Rock8", "Rock9", "Rock10", "Rock11"]
	for c in cluster_centers:
		# coral bouquet
		for k in range(4 + randi() % 4):
			var ca := randf() * TAU
			var cr := 2.0 + randf() * 9.0
			var cx := c.x + cos(ca) * cr
			var cz := c.z + sin(ca) * cr
			_place_aq(corals[randi() % corals.size()], Vector3(cx, seabed_y(cx, cz), cz), 1.6 + randf() * 2.2, false)
		# swaying seaweed
		for k in range(3 + randi() % 3):
			var wa := randf() * TAU
			var wr := 3.0 + randf() * 10.0
			var wx := c.x + cos(wa) * wr
			var wz := c.z + sin(wa) * wr
			_place_aq(weeds[randi() % weeds.size()], Vector3(wx, seabed_y(wx, wz), wz), 1.8 + randf() * 2.0, true)
		# shells nestled in
		for k in range(2):
			var sa := randf() * TAU
			var sx := c.x + cos(sa) * (2.0 + randf() * 6.0)
			var sz := c.z + sin(sa) * (2.0 + randf() * 6.0)
			_place_aq(shells[randi() % shells.size()], Vector3(sx, seabed_y(sx, sz) + 0.3, sz), 1.2 + randf() * 1.5, false)
	# scattered boulders across the open seabed
	for i in range(70):
		var a := randf() * TAU
		var r := 25.0 + randf() * (WORLD_R * 0.85 - 25.0)
		var x := cos(a) * r
		var z := sin(a) * r
		_place_aq(rocks[randi() % rocks.size()], Vector3(x, seabed_y(x, z), z), 2.0 + randf() * 4.0, false)

func _build_aquatic_creatures() -> void:
	# hero animated creatures patrolling on circular paths
	var roster := [
		["Shark", 130.0, 0.05, 22.0, 4.0],
		["Hammerhead", 160.0, 0.045, 30.0, 4.0],
		["Whale", 200.0, 0.02, 40.0, 9.0],
		["Turtle", 55.0, 0.06, 9.0, 1.6],
		["Turtle", 90.0, 0.05, 13.0, 1.6],
		["StingRay", 75.0, 0.07, 7.0, 2.4],
		["StingRay", 110.0, 0.06, 16.0, 2.4],
		["Dolphin", 140.0, 0.08, 34.0, 2.6],
		["Squid", 60.0, 0.05, 18.0, 2.0],
	]
	for entry in roster:
		var inst := _place_aq(entry[0], Vector3.ZERO, entry[4], true)
		if inst == null:
			continue
		if String(entry[0]) == "Whale":
			whale_node = inst
		aquatic_movers.append({"node": inst, "rad": entry[1], "spd": entry[2], "y": entry[3], "ph": randf() * TAU})
	# bottom dwellers posed in the groves
	if cluster_centers.size() >= 4:
		var oc: Vector3 = cluster_centers[2]
		_place_aq("Octopus", Vector3(oc.x + 4.0, seabed_y(oc.x + 4.0, oc.z) + 0.4, oc.z), 2.2, true)
		var cc: Vector3 = cluster_centers[5]
		_place_aq("Crab", Vector3(cc.x, seabed_y(cc.x, cc.z) + 0.3, cc.z + 3.0), 2.0, true)
		var lc: Vector3 = cluster_centers[9]
		_place_aq("Lobster", Vector3(lc.x, seabed_y(lc.x, lc.z) + 0.3, lc.z - 3.0), 2.0, true)
	# small darting schools of the little fish
	var smallfish := ["ClownFish", "Dory", "Carp", "Tuna", "Eel"]
	for s in range(8):
		var inst := _place_aq(smallfish[s % smallfish.size()], Vector3.ZERO, 1.2 + randf() * 1.0, true)
		if inst == null:
			continue
		aquatic_movers.append({"node": inst, "rad": 40.0 + randf() * 150.0, "spd": 0.12 + randf() * 0.15, "y": 10.0 + randf() * 28.0, "ph": randf() * TAU})
	# player-crafted fish from the Crafting Studio (persist via save)
	for cf in custom_fish:
		if (cf as Array).size() < 6:
			continue
		var cfn := _make_creature_node("fish", Color(cf[0], cf[1], cf[2]), Color(cf[3], cf[4], cf[5]), (cf as Array).size() > 6 and int(cf[6]) == 1, (cf as Array).size() > 7 and int(cf[7]) == 1)
		add_child(cfn)
		flora_nodes.append(cfn)
		aquatic_movers.append({"node": cfn, "rad": 30.0 + randf() * 130.0, "spd": 0.10 + randf() * 0.12, "y": 8.0 + randf() * 26.0, "ph": randf() * TAU})

func _tick_aquatic(delta: float) -> void:
	var t: float = Time.get_ticks_msec() / 1000.0
	for mv in aquatic_movers:
		var node: Node3D = mv["node"]
		var ang: float = t * float(mv["spd"]) + float(mv["ph"])
		var rad: float = float(mv["rad"])
		var pos := Vector3(cos(ang) * rad, float(mv["y"]) + sin(t * 0.3 + float(mv["ph"])) * 3.0, sin(ang) * rad)
		node.position = pos
		node.rotation.y = -ang + PI * 0.5

func _build_pearls() -> void:
	pearl_mat = _rainbow_mat()
	for i in range(PEARL_TOTAL):
		# along the route between consecutive friends, light jitter
		var fi: int = i % FRIEND_DEFS.size()
		var fj: int = (fi + 1) % FRIEND_DEFS.size()
		var aa: float = float(fi) / float(FRIEND_DEFS.size()) * TAU + 0.6
		var ab: float = float(fj) / float(FRIEND_DEFS.size()) * TAU + 0.6
		var ra: float = 55.0 + float(fi % 3) * 30.0
		var rb: float = 55.0 + float(fj % 3) * 30.0
		var pa := Vector3(cos(aa) * ra, 0, sin(aa) * ra)
		var pb := Vector3(cos(ab) * rb, 0, sin(ab) * rb)
		var tmix: float = 0.35 if i < FRIEND_DEFS.size() else 0.65
		var pp: Vector3 = pa.lerp(pb, tmix)
		var x: float = pp.x + hash2(i, 5) * 10.0 - 5.0
		var z: float = pp.z + hash2(i, 11) * 10.0 - 5.0
		pearl_slots.append(Vector3(x, seabed_y(x, z) + 4.5 + hash2(i, 9) * 6.0, z))
		_spawn_pearl(i)

func _spawn_pearl(slot: int) -> void:
	var mi := MeshInstance3D.new()
	var sph := SphereMesh.new()
	sph.radius = 2.3
	sph.height = 4.6
	mi.mesh = sph
	mi.material_override = pearl_mat
	mi.position = pearl_slots[slot]
	mi.set_meta("slot", slot)
	add_child(mi)
	var l := OmniLight3D.new()
	l.light_color = Color(1.0, 0.8, 1.0)
	l.light_energy = 0.9
	l.omni_range = 10.0
	l.visible = (quality != "speedy") or (slot % 2 == 0)
	l.position = mi.position
	add_child(l)
	pearl_lights.append(l)
	mi.set_meta("light", l)
	mi.set_meta("halo", _halo(mi.position, Color(1.0, 0.75, 0.95), 10.0))
	pearls.append(mi)

func _respawn_pearls() -> void:
	var used := {}
	for p in pearls:
		used[int(p.get_meta("slot"))] = true
	var grew := false
	for i in range(PEARL_TOTAL):
		if not used.has(i):
			_spawn_pearl(i)
			grew = true
	if grew:
		show_msg("", "New rainbow pearls are shimmering in the reef!")

# --- TRIAL (2026-06-25): underwater integration for the 2D friend billboards ---
# Goal: stop the painterly sprites reading as flat stickers pasted on the 3D reef,
# WITHOUT converting them to 3D (their hand-painted likeness is the charm). We keep
# the Sprite3D (so all `as Sprite3D` / `.texture` call sites stay valid) and only
# swap its material for a shader that: billboards, feathers the cut-out edge, takes
# the scene's depth fog, and catches the caustic light + a rim — plus a soft contact
# shadow on the seabed so the friend sits *in* the water instead of floating on top.
# Fully reversible: delete _friend_underwater_fx + its call in _build_friends.
var _uw_sprite_shader: Shader = null
var _shadow_shader: Shader = null

func _friend_underwater_fx(spr: Sprite3D, ground_y: float) -> void:
	if _uw_sprite_shader == null:
		_uw_sprite_shader = Shader.new()
		_uw_sprite_shader.code = """shader_type spatial;
render_mode blend_mix, cull_disabled, depth_draw_opaque, shadows_disabled, specular_disabled;
uniform sampler2D tex : source_color, filter_linear_mipmap;
uniform sampler2D caustic : source_color;
uniform float glow = 0.8;          // self-illumination so the 'glowing friends' stay readable
uniform float caustic_amt = 0.5;   // strength of the reef-floor light dapples on the sprite
uniform float soft = 0.12;         // edge feather width (alpha units) -> kills the hard matte
void vertex() {
	// full billboard: face the camera, keeping the quad's built-in pixel size
	MODELVIEW_MATRIX = VIEW_MATRIX * mat4(
		INV_VIEW_MATRIX[0], INV_VIEW_MATRIX[1], INV_VIEW_MATRIX[2], MODEL_MATRIX[3]);
}
void fragment() {
	vec4 t = texture(tex, UV);
	float a = smoothstep(0.0, soft, t.a);   // soft feathered silhouette
	if (a < 0.01) { discard; }
	ALBEDO = t.rgb;
	ALPHA = a;
	EMISSION = t.rgb * glow;                 // keep brightness; scene fog still tints by depth
	// caustic dapples projected by world XZ (same look as the reef floor), masked to the body
	vec3 wp = (INV_VIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;
	vec2 cuv = wp.xz * 0.020 + vec2(TIME * 0.010, -TIME * 0.007);
	vec2 cuv2 = wp.xz * 0.014 - vec2(TIME * 0.006, TIME * 0.009);
	float c = texture(caustic, cuv).r * 0.55 + texture(caustic, cuv2).r * 0.45;
	c = smoothstep(0.4, 0.95, c);
	EMISSION += c * vec3(0.55, 0.78, 0.82) * caustic_amt;
	RIM = 0.7;          // soft rim so the edge catches the key light, not a sticker outline
	RIM_TINT = 0.3;
	ROUGHNESS = 0.9;
}"""
	var mat := ShaderMaterial.new()
	mat.shader = _uw_sprite_shader
	mat.set_shader_parameter("tex", spr.texture)
	mat.set_shader_parameter("caustic", load("res://assets/terrain/caustics.png"))
	spr.material_override = mat

	# soft contact shadow on the seabed beneath the friend
	if _shadow_shader == null:
		_shadow_shader = Shader.new()
		_shadow_shader.code = """shader_type spatial;
render_mode blend_mix, unshaded, cull_disabled, depth_draw_never, shadows_disabled;
uniform float strength = 0.34;
void fragment() {
	float r = length(UV - vec2(0.5)) * 2.0;     // 0 at centre -> 1 at edge
	ALBEDO = vec3(0.02, 0.05, 0.06);
	ALPHA = smoothstep(1.0, 0.0, r) * strength; // soft radial falloff
}"""
	var w: float = 5.0
	if spr.texture != null:
		w = float(spr.texture.get_size().x) * spr.pixel_size
	var shadow := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(w * 1.15, w * 1.15)
	shadow.mesh = pm
	var smat := ShaderMaterial.new()
	smat.shader = _shadow_shader
	shadow.material_override = smat
	shadow.position = Vector3(spr.position.x, ground_y + 0.12, spr.position.z)
	add_child(shadow)

func _build_friends() -> void:
	for i in range(FRIEND_DEFS.size()):
		var fd: Dictionary = FRIEND_DEFS[i]
		var a: float = float(i) / float(FRIEND_DEFS.size()) * TAU + 0.6
		var r: float = 55.0 + float(i % 3) * 30.0
		var x: float = cos(a) * r
		var z: float = sin(a) * r
		var spr := Sprite3D.new()
		spr.texture = load("res://assets/characters/friends/" + String(fd["tex"]) + ".png")
		spr.billboard = BaseMaterial3D.BILLBOARD_DISABLED   # billboard handled in the underwater shader
		spr.pixel_size = 0.016
		spr.position = Vector3(x, seabed_y(x, z) + 6.5, z)
		add_child(spr)
		_friend_underwater_fx(spr, seabed_y(x, z))   # TRIAL: light + ground the sprite into the 3D reef
		var bcols := [Color(1.0, 0.75, 0.35), Color(0.45, 0.9, 1.0), Color(1.0, 0.5, 0.75), Color(0.6, 1.0, 0.6), Color(0.8, 0.6, 1.0)]
		var bcol: Color = bcols[i % bcols.size()]
		var beacon := OmniLight3D.new()
		beacon.light_color = bcol
		beacon.light_energy = 2.4 + float(i % 3)
		beacon.omni_range = 20.0 + float(i % 3) * 6.0
		beacon.position = spr.position + Vector3(0, 8, 0)
		add_child(beacon)
		var pil := MeshInstance3D.new()
		var pm2 := CylinderMesh.new()
		pm2.top_radius = 0.3 + float(i % 3) * 0.25
		pm2.bottom_radius = 1.1 + float(i % 2) * 0.6
		pm2.height = WATER_TOP - spr.position.y
		pm2.radial_segments = 10
		var pmat := StandardMaterial3D.new()
		pmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		pmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		pmat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		pmat.albedo_color = Color(bcol.r, bcol.g, bcol.b, 0.10)
		pmat.cull_mode = BaseMaterial3D.CULL_DISABLED
		pil.mesh = pm2
		pil.material_override = pmat
		pil.position = Vector3(spr.position.x, spr.position.y + pm2.height * 0.5, spr.position.z)
		add_child(pil)
		var sparks: Array = []
		for sk in range(2):
			var orb := MeshInstance3D.new()
			var om := SphereMesh.new()
			om.radius = 0.28
			om.height = 0.56
			orb.mesh = om
			var omat := StandardMaterial3D.new()
			omat.emission_enabled = true
			omat.emission = bcol
			omat.emission_energy_multiplier = 3.0
			orb.material_override = omat
			add_child(orb)
			sparks.append(orb)
		friends.append({"node": spr, "fname": fd["fname"], "msg": fd["msg"], "game": fd["game"], "found": false, "won": false,
			"theme": fd.get("theme", "ice"), "mode": fd.get("mode", "fish"),
			"beacon": beacon, "pillar": pil, "sparks": sparks, "bcol": bcol, "cool": 0.0, "ph": randf() * TAU})

func _build_player() -> void:
	player = preload("res://scripts/player.gd").new()
	add_child(player)

func _build_hud() -> void:
	var cl := CanvasLayer.new()
	add_child(cl)
	hud_pearls = _mk_label(cl, Vector2(20, 14), 28)
	hud_stars = _mk_label(cl, Vector2(20, 52), 24)
	hud_game = _mk_label(cl, Vector2(20, 90), 24)
	hud_msg = _mk_label(cl, Vector2(20, 630), 30)
	hud_msg.text = "Find the glowing friends in the fairy garden!"
	_update_hud()

func _mk_label(cl: CanvasLayer, pos: Vector2, fsize: int) -> Label:
	var l := Label.new()
	l.position = pos
	l.add_theme_font_size_override("font_size", fsize)
	l.add_theme_color_override("font_outline_color", Color(0.02, 0.05, 0.14, 0.9))
	l.add_theme_constant_override("outline_size", 10)
	cl.add_child(l)
	return l

func _update_hud() -> void:
	hud_pearls.text = "Rainbow pearls: %d" % pearl_count
	var stars := 0
	for f in friends:
		if f["found"]:
			stars += 1
	hud_stars.text = "Friends: %d / 5   Trophies: %d / 5" % [stars, trophies]

# speaker key -> default pitch tint (so even the fallback clip differs per character)
const VOICE_PITCH := {"roshan": 1.18, "huluu": 1.05, "evie": 1.28, "harper": 1.12, "faron": 1.0, "gabby": 1.22, "wacky": 0.7, "chuck": 1.0, "shop": 0.85, "sparkle": 1.35, "everyone": 1.1}

var speech_layer: CanvasLayer
var speech_portrait: TextureRect
var speech_t := 0.0
const SPEAKER_PORTRAIT := {
	"roshan": "res://assets/characters/roshan_sprite.png",
	"huluu": "res://assets/characters/friends/huluu.png",
	"evie": "res://assets/characters/friends/mama_baby.png",
	"harper": "res://assets/characters/friends/two_friends.png",
	"faron": "res://assets/characters/friends/mama_baby.png",
	"gabby": "res://assets/characters/friends/gabby.png",
	"wacky": "res://assets/characters/friends/wacky_chuck.png",
	"chuck": "res://assets/characters/friends/wacky_chuck.png",
	"shop": "res://assets/characters/roshan_sprite.png",
	"sparkle": "res://assets/book/baby_eagle.png",
	"everyone": "res://assets/characters/roshan_sprite.png"}

func _flash_speaker_icon(who: String) -> void:
	if speech_layer == null:
		speech_layer = CanvasLayer.new()
		speech_layer.layer = 8
		add_child(speech_layer)
		var panel := Panel.new()
		var sb := StyleBoxFlat.new()
		sb.bg_color = Color(0.06, 0.1, 0.22, 0.85)
		sb.set_corner_radius_all(20)
		sb.border_color = Color(1.0, 0.85, 0.5)
		sb.set_border_width_all(3)
		panel.add_theme_stylebox_override("panel", sb)
		panel.position = Vector2(24, 470)
		panel.size = Vector2(190, 230)
		speech_layer.add_child(panel)
		speech_portrait = TextureRect.new()
		speech_portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		speech_portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
		speech_portrait.position = Vector2(34, 478)
		speech_portrait.size = Vector2(170, 214)
		speech_layer.add_child(speech_portrait)
		panel.name = "bubble"
	var key := _speaker_key(who)
	var path := String(SPEAKER_PORTRAIT.get(key, SPEAKER_PORTRAIT["roshan"]))
	if ResourceLoader.exists(path):
		speech_portrait.texture = load(path)
	speech_layer.visible = true
	speech_t = 4.0

func _say(speaker: String, event: String = "", min_gap: float = 0.0) -> void:
	var key := speaker + "_" + event
	if min_gap > 0.0:
		var now := Time.get_ticks_msec() / 1000.0
		if now - float(said_cool.get(key, -99.0)) < min_gap:
			return
		said_cool[key] = now
	# prefer a real recorded clip for this exact line, then any line for the speaker
	var stream: AudioStream = null
	var p1 := "res://assets/audio/voices/" + key + ".ogg"
	var p2 := "res://assets/audio/voices/" + speaker + ".ogg"
	if ResourceLoader.exists(p1):
		stream = load(p1)
	elif ResourceLoader.exists(p2):
		stream = load(p2)
	var ap: AudioStreamPlayer = voice_pool[voice_i % voice_pool.size()]
	voice_i += 1
	if stream != null:
		ap.stream = stream
		ap.pitch_scale = 1.0
		ap.play()
	elif voice != null:
		# graceful fallback until real clips are dropped in: the recorded "yay",
		# pitched to give each character a recognisably different timbre
		voice.pitch_scale = float(VOICE_PITCH.get(speaker, 1.0))
		voice.play()

func _speaker_key(who: String) -> String:
	var w := who.to_lower()
	if "roshan" in w: return "roshan"
	if "huluu" in w: return "huluu"
	if "evie" in w or "lamb" in w: return "evie"
	if "harper" in w or "fiona" in w: return "harper"
	if "faron" in w: return "faron"
	if "gabby" in w: return "gabby"
	if "chuck" in w: return "chuck"
	if "wacky" in w: return "wacky"
	if "shop" in w: return "shop"
	if "sparkle" in w or "eagle" in w: return "sparkle"
	if "everyone" in w: return "everyone"
	return "roshan"

func show_msg(who: String, txt: String, vo: String = "talk") -> void:
	hud_msg.text = txt
	msg_timer = 5.0
	if who != "":
		_say(_speaker_key(who), vo, 0.5)
	# (speaker name + portrait intentionally omitted — just the message text)

# ===================== 3.0 PLATFORM & FLOW =====================
func _apply_quality(q: String) -> void:
	quality = q
	var speedy: bool = q == "speedy"
	if sun_light != null:
		sun_light.shadow_enabled = not speedy
	if world_env != null:
		world_env.glow_bloom = 0.12 if speedy else 0.4
		world_env.glow_intensity = 0.75 if speedy else 0.95
	if player != null and "trail_enabled" in player:
		player.trail_enabled = not speedy   # the wake ribbon is the only per-frame CPU mesh rebuild
	streak_ctx = "none"   # force the streak pool to re-apply visibility for the new quality
	for i in range(pearl_lights.size()):
		var l: OmniLight3D = pearl_lights[i]
		if is_instance_valid(l):
			l.visible = (not speedy) or (i % 2 == 0)
	if plankton_node != null:
		plankton_node.amount_ratio = 0.45 if speedy else 1.0
	var vp := get_viewport()
	if vp != null:
		vp.scaling_3d_scale = 0.8 if speedy else 1.0
	for fn in flora_nodes:
		if is_instance_valid(fn):
			_set_vis_range(fn, 150.0 if speedy else 0.0)
	if quality_btn != null:
		quality_btn.text = "Graphics: Speedy" if speedy else "Graphics: Sparkly"

func _set_vis_range(n: Node, dist: float) -> void:
	if n is GeometryInstance3D:
		(n as GeometryInstance3D).visibility_range_end = dist
		(n as GeometryInstance3D).visibility_range_end_margin = 12.0 if dist > 0.0 else 0.0
		(n as GeometryInstance3D).visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF if dist > 0.0 else GeometryInstance3D.VISIBILITY_RANGE_FADE_DISABLED
	for c in n.get_children():
		_set_vis_range(c, dist)

func _load_save() -> void:
	if FileAccess.file_exists(SAVE_PATH):
		var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
		if f != null:
			var d: Variant = JSON.parse_string(f.get_as_text())
			if d is Dictionary:
				save_data = d
	finale_done = bool(save_data.get("finale", false))
	level2_done_once = bool(save_data.get("level2", false))
	plays = int(save_data.get("plays", 0)) + 1   # each launch flips day <-> night
	is_night = (plays % 2) == 0
	_apply_time_of_day()
	music_on = bool(save_data.get("music", true))
	var qdef: String = "speedy" if OS.has_feature("mobile") else "sparkly"
	_apply_quality(String(save_data.get("quality", qdef)))
	music.volume_db = -8.0 if music_on else -60.0
	if music_btn != null:
		music_btn.text = "Music: On" if music_on else "Music: Off"
	pearl_count = int(save_data.get("pearls", 0))
	custom_fish = save_data.get("custom_fish", [])
	custom_friends = save_data.get("custom_friends", [])
	skin_id = String(save_data.get("skin", "classic"))
	_apply_skin()
	var won_d: Dictionary = save_data.get("won", {})
	var found_d: Dictionary = save_data.get("found", {})
	for f2 in friends:
		var nm := String(f2["fname"])
		if bool(found_d.get(nm, false)):
			first_session = false
			f2["found"] = true
			(f2["beacon"] as OmniLight3D).light_energy = 1.0
			((f2["pillar"] as MeshInstance3D).material_override as StandardMaterial3D).albedo_color.a = 0.035
		if bool(won_d.get(nm, false)):
			f2["won"] = true
			trophies += 1
			_add_won_star(f2)
	_update_hud()

func _write_save() -> void:
	var won_d := {}
	var found_d := {}
	for f2 in friends:
		won_d[String(f2["fname"])] = bool(f2["won"])
		found_d[String(f2["fname"])] = bool(f2["found"])
	save_data = {"won": won_d, "found": found_d, "finale": finale_done, "music": music_on, "quality": quality, "pearls": pearl_count, "skin": skin_id, "level2": level2_done_once, "plays": plays, "custom_fish": custom_fish, "custom_friends": custom_friends}
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f != null:
		f.store_string(JSON.stringify(save_data))

func _add_won_star(fr: Dictionary) -> void:
	if fr.has("star"):
		return
	var st := Label3D.new()
	st.text = "\u2605"
	st.font_size = 240
	st.modulate = Color(1.0, 0.85, 0.2)
	st.outline_size = 24
	st.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	st.position = (fr["node"] as Sprite3D).position + Vector3(0, 7.5, 0)
	add_child(st)
	fr["star"] = st

func _build_pause() -> void:
	pause_layer = CanvasLayer.new()
	pause_layer.layer = 12
	pause_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	add_child(pause_layer)
	var gear := Button.new()
	gear.text = "| |"
	gear.add_theme_font_size_override("font_size", 26)
	gear.custom_minimum_size = Vector2(76, 76)
	var gsb := StyleBoxFlat.new()
	gsb.bg_color = Color(0.1, 0.15, 0.3, 0.55)
	gsb.set_corner_radius_all(38)
	gear.add_theme_stylebox_override("normal", gsb)
	gear.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	gear.position = Vector2(-96, 18)
	gear.pressed.connect(toggle_pause)
	pause_layer.add_child(gear)
	pause_panel = Panel.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = Color(0.07, 0.1, 0.24, 0.93)
	psb.set_corner_radius_all(28)
	pause_panel.add_theme_stylebox_override("panel", psb)
	pause_panel.custom_minimum_size = Vector2(460, 420)
	pause_panel.set_anchors_preset(Control.PRESET_CENTER)
	pause_panel.position = Vector2(-230, -210)
	pause_panel.size = Vector2(460, 420)
	pause_panel.visible = false
	pause_layer.add_child(pause_panel)
	var vb := VBoxContainer.new()
	vb.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	vb.offset_left = 36
	vb.offset_right = -36
	vb.offset_top = 30
	vb.offset_bottom = -30
	vb.add_theme_constant_override("separation", 22)
	pause_panel.add_child(vb)
	var resume := _pause_btn(vb, "Keep Swimming!")
	resume.pressed.connect(toggle_pause)
	quality_btn = _pause_btn(vb, "Graphics: Sparkly")
	quality_btn.pressed.connect(func():
		_apply_quality("speedy" if quality == "sparkly" else "sparkly")
		_write_save())
	music_btn = _pause_btn(vb, "Music: On")
	music_btn.pressed.connect(func():
		music_on = not music_on
		music.volume_db = -8.0 if music_on else -60.0
		music_btn.text = "Music: On" if music_on else "Music: Off"
		_write_save())

func _pause_btn(vb: VBoxContainer, txt: String) -> Button:
	var b := Button.new()
	b.text = txt
	b.add_theme_font_size_override("font_size", 30)
	b.custom_minimum_size = Vector2(0, 96)
	vb.add_child(b)
	return b

func toggle_pause() -> void:
	var p: bool = not get_tree().paused
	get_tree().paused = p
	pause_panel.visible = p

func _shop_buy(id: String) -> void:
	for it in SHOP_ITEMS:
		if String(it["id"]) != id or pearl_count < int(it["price"]):
			continue
		if id == "beans":
			if beans_t < 0.0:
				pearl_count -= int(it["price"])
				_update_hud()
				_write_save()
				if buy_sound != null:
					buy_sound.play()
				_beans_go()
				_sparkle_burst(player.position + Vector3(0, 1, 0), Color(0.6, 1.0, 0.4))
			return

func _near_ground(obj_pos: Vector3, ppos: Vector3, r: float, htol: float = 12.0) -> bool:
	return Vector2(obj_pos.x - ppos.x, obj_pos.z - ppos.z).length() < r and absf(obj_pos.y - ppos.y) < htol

func _skin_def(id: String) -> Dictionary:
	for s in SKINS:
		if String(s["id"]) == id:
			return s
	return SKINS[0]

func _apply_skin() -> void:
	# swap Roshan's whole appearance to the chosen skin (classic = 3D model)
	if player == null:
		return
	var s := _skin_def(skin_id)
	skin_id = String(s["id"])   # normalise any stale/removed skin id back to a valid one
	player.set_skin(skin_id, String(s["sprite"]))

func _all_pearls_done() -> bool:
	return pearls.is_empty()

func _check_level2_unlock(ppos: Vector3, delta: float) -> void:
	var stars := 0
	for f in friends:
		if f["found"]:
			stars += 1
	var ready: bool = trophies >= 5 and stars >= 5 and pearl_count >= PEARL_TOTAL
	if ready and portal_node == null:
		_raise_portal()
	if portal_node != null and is_instance_valid(portal_node):
		portal_t += delta
		portal_node.rotation.y += delta * 0.4
		var swirl: Node3D = portal_node.get_node_or_null("Swirl")
		if swirl != null:
			swirl.rotation.z += delta * 2.2
			swirl.scale = Vector3.ONE * (1.0 + sin(portal_t * 3.0) * 0.06)
		portal_node.position.y = (WATER_TOP - 9.0) + sin(portal_t * 1.2) * 0.6
		portal_ready = true
		portal_cool = maxf(0.0, portal_cool - delta)
		var pdist: float = portal_node.position.distance_to(ppos)
		if pdist > 13.0:
			portal_armed = true
		if portal_ready and portal_armed and portal_cool <= 0.0 and game == "" and finale_t < 0.0 and pdist < 8.0:
			portal_armed = false
			_enter_level2()

func _raise_portal() -> void:
	var hub := Node3D.new()
	hub.name = "Portal"
	# giant rainbow conch shell base (spiral of tinted torus rings)
	for i in range(6):
		var ring := MeshInstance3D.new()
		var tm := TorusMesh.new()
		tm.inner_radius = 3.4 - float(i) * 0.45
		tm.outer_radius = 4.0 - float(i) * 0.45
		ring.mesh = tm
		var rm := StandardMaterial3D.new()
		rm.albedo_color = Color.from_hsv(float(i) / 6.0, 0.55, 1.0)
		rm.roughness = 0.4
		rm.emission_enabled = true
		rm.emission = Color.from_hsv(float(i) / 6.0, 0.55, 1.0)
		rm.emission_energy_multiplier = 0.5
		ring.material_override = rm
		ring.position.y = float(i) * 1.5
		ring.rotation_degrees = Vector3(90, 0, float(i) * 18.0)
		hub.add_child(ring)
	# swirling rainbow vortex disc inside
	var swirl := MeshInstance3D.new()
	swirl.name = "Swirl"
	var sd := CylinderMesh.new()
	sd.top_radius = 3.0
	sd.bottom_radius = 3.0
	sd.height = 0.3
	swirl.mesh = sd
	swirl.rotation_degrees = Vector3(90, 0, 0)
	swirl.position.y = 4.5
	swirl.material_override = _rainbow_mat()
	hub.add_child(swirl)
	# beckoning light
	var pl := OmniLight3D.new()
	pl.light_color = Color(1.0, 0.9, 1.0)
	pl.light_energy = 3.0
	pl.omni_range = 28.0
	pl.position.y = 5.0
	hub.add_child(pl)
	var lbl := Label3D.new()
	lbl.text = "A magic river to the sky!\nSwim UP into it!"
	lbl.font_size = 80
	lbl.outline_size = 18
	lbl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lbl.position.y = 9.0
	hub.add_child(lbl)
	# a glowing river streams across the top of the stage and pours into the conch
	var river := MeshInstance3D.new()
	river.name = "River"
	var rp := PlaneMesh.new()
	rp.size = Vector2(40.0, 220.0)
	rp.subdivide_depth = 40
	river.mesh = rp
	var rsh := Shader.new()
	rsh.code = """shader_type spatial;
render_mode cull_disabled;
void vertex(){
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz;
	VERTEX.y += sin(TIME*1.6 + wp.z*0.20)*0.5 + cos(TIME*1.1 + wp.x*0.15)*0.35;
}
void fragment(){
	float flow = fract(UV.y*6.0 - TIME*0.35);
	float band = smoothstep(0.0,0.5,flow)*smoothstep(1.0,0.5,flow);
	vec3 base = vec3(0.25,0.62,0.85);
	ALBEDO = base + band*vec3(0.35,0.45,0.4);
	EMISSION = (base*0.4 + band*vec3(0.4,0.7,0.85))*0.8;
	ALPHA = 0.6;
}"""
	var rmat := ShaderMaterial.new()
	rmat.shader = rsh
	rmat.render_priority = 1
	var rmm := rmat
	river.material_override = rmm
	(river.material_override as ShaderMaterial).shader = rsh
	var rtrans := StandardMaterial3D.new()
	# river is translucent
	river.position = Vector3(0, 2.0, -90.0)
	river.rotation_degrees = Vector3(8, 0, 0)
	hub.add_child(river)
	hub.position = Vector3(0, WATER_TOP - 9.0, 0)
	add_child(hub)
	portal_node = hub
	show_msg("Roshan", "Wow! A magic river to the sky is opening up high above the reef!")

func _enter_level2(from_castle: bool = false) -> void:
	game = "level2"
	g = {"t": 0.0}
	arena_solids.clear()
	fade_walls.clear()
	lagoon_floor = true   # the courtyard floor follows the rolling-hill terrain
	return_pos = player.position
	arena_center = LEVEL2_POS
	arena_dome = 235.0
	arena_ceil = 120.0
	l2_stars = []
	l2_open = false
	g["phase"] = "court"
	arena_env = Environment.new()
	arena_env.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var psky := ProceduralSkyMaterial.new()
	if is_night:
		psky.sky_top_color = Color(0.06, 0.07, 0.22)
		psky.sky_horizon_color = Color(0.22, 0.20, 0.42)
		psky.ground_bottom_color = Color(0.10, 0.12, 0.26)
		psky.ground_horizon_color = Color(0.18, 0.18, 0.36)
	else:
		psky.sky_top_color = Color(0.35, 0.62, 0.95)
		psky.sky_horizon_color = Color(0.85, 0.92, 1.0)
		psky.ground_bottom_color = Color(0.7, 0.85, 0.95)
		psky.ground_horizon_color = Color(0.8, 0.9, 1.0)
	sky.sky_material = psky
	arena_env.sky = sky
	arena_env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	arena_env.ambient_light_energy = 0.7 if is_night else 1.0
	_wind_waker_bloom(arena_env, 0.85, 0.3, 1.0)   # open sky above the lagoon — bloom the sky/windows, not every sunlit wall (0.82 white-washed the whole castle)
	_grade(arena_env)
	we_node.environment = arena_env
	_build_pearl_castle(LEVEL2_POS)
	if is_night:
		_build_lagoon_night(LEVEL2_POS)
	_play_music("finale")
	if from_castle:
		# castle is already won: open the door, hide the collected stars, spawn at the entrance facing the courtyard
		for sd in l2_stars:
			sd["got"] = true
			var sn: Node3D = sd["node"]
			if is_instance_valid(sn):
				sn.visible = false
		l2_open = true
		if l2_door != null and is_instance_valid(l2_door):
			l2_door.position.y = float(g.get("door_closed_y", l2_door.position.y)) + 30.0
		if g.has("arch") and is_instance_valid(g["arch"]):
			(g["arch"] as Node3D).visible = true
		player.position = LEVEL2_POS + Vector3(0, 8, -58)
		player.yaw = 0.0
		player.vel = Vector3.ZERO
		show_msg("Roshan", "Out in the castle courtyard! Wheee!")
	else:
		player.position = LEVEL2_POS + Vector3(0, 8, 175)
		player.vel = Vector3.ZERO
		show_msg("Sky Lagoon", "You found Princess Huluu's SKY LAGOON! Follow the path and catch 3 Dream Stars to open the castle!")

func _up_mat(key: String, uvs: float = 0.1, tint: Color = Color(1, 1, 1)) -> StandardMaterial3D:
	# upgraded CC0 PBR material (color + OpenGL normal + roughness), triplanar-tiled
	var m := StandardMaterial3D.new()
	m.albedo_texture = load("res://assets/terrain/up_%s_col.jpg" % key)
	m.albedo_color = tint
	m.normal_enabled = true
	m.normal_texture = load("res://assets/terrain/up_%s_nrm.jpg" % key)
	m.normal_scale = 1.0
	m.roughness_texture = load("res://assets/terrain/up_%s_rgh.jpg" % key)
	m.uv1_triplanar = true
	# WORLD-space triplanar: adjacent boxes/panels sharing a material tile
	# continuously instead of each restarting the pattern at its own origin
	# (local-space triplanar was the source of the "spliced" seams on the castle).
	# Moving meshes (e.g. the castle door) must switch this back off.
	m.uv1_world_triplanar = true
	m.uv1_scale = Vector3(uvs, uvs, uvs)
	m.roughness = 1.0
	return m

func _l2_box(pos: Vector3, size: Vector3, col: Color, glow: float = 0.0) -> MeshInstance3D:
	var b := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	b.mesh = bm
	var m := StandardMaterial3D.new()
	m.albedo_color = col
	m.roughness = 0.7
	if glow > 0.0:
		m.emission_enabled = true
		m.emission = col
		m.emission_energy_multiplier = glow
	b.material_override = m
	b.position = pos
	add_child(b)
	game_nodes.append(b)
	return b

func _l2_tower(pos: Vector3, sc: float = 1.0) -> void:
	# fantasy turret: textured stone shaft, gold band, glowing window, conic roof, flag
	var shaft := MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.top_radius = 3.0 * sc
	cm.bottom_radius = 3.7 * sc
	cm.height = 26.0 * sc
	cm.radial_segments = 16
	shaft.mesh = cm
	shaft.material_override = _up_mat("marble", 0.07, Color(0.98, 0.9, 1.0))
	shaft.position = pos + Vector3(0, 13.0 * sc, 0)
	add_child(shaft)
	game_nodes.append(shaft)
	# decorative gold band near the top
	var band := MeshInstance3D.new()
	var bcm := CylinderMesh.new()
	bcm.top_radius = 3.85 * sc; bcm.bottom_radius = 3.85 * sc; bcm.height = 1.4 * sc; bcm.radial_segments = 16
	band.mesh = bcm
	var bm := StandardMaterial3D.new()
	bm.albedo_color = Color(0.95, 0.8, 0.4); bm.metallic = 0.8; bm.roughness = 0.3
	bm.emission_enabled = true; bm.emission = Color(0.9, 0.7, 0.3); bm.emission_energy_multiplier = 0.3
	band.material_override = bm
	band.position = pos + Vector3(0, 24.0 * sc, 0)
	add_child(band); game_nodes.append(band)
	# glowing arched window facing the courtyard
	var win := _l2_box(pos + Vector3(0, 16.0 * sc, 3.5 * sc), Vector3(1.8 * sc, 4.2 * sc, 0.5 * sc), Color(1.0, 0.85, 0.5))
	win.material_override.emission_enabled = true
	win.material_override.emission = Color(1.0, 0.8, 0.45)
	win.material_override.emission_energy_multiplier = 1.6
	# steeper conic roof
	var roof := MeshInstance3D.new()
	var rc := CylinderMesh.new()
	rc.top_radius = 0.0
	rc.bottom_radius = 5.0 * sc
	rc.height = 9.5 * sc
	rc.radial_segments = 16
	roof.mesh = rc
	roof.material_override = _up_mat("roof", 0.12, Color(1.0, 0.7, 0.7))   # clay roof tiles
	roof.position = pos + Vector3(0, 30.7 * sc, 0)
	add_child(roof)
	game_nodes.append(roof)
	# flagpole + flag
	_l2_box(pos + Vector3(0, 36.0 * sc, 0), Vector3(0.3 * sc, 8.0 * sc, 0.3 * sc), Color(0.35, 0.28, 0.2))
	var flag := MeshInstance3D.new()
	var fq := QuadMesh.new()
	fq.size = Vector2(3.0 * sc, 1.6 * sc)
	fq.subdivide_width = 10   # enough segments for the wave to bend through
	flag.mesh = fq
	var fm := ShaderMaterial.new()
	fm.shader = _flag_shader()
	fm.set_shader_parameter("col", Color.from_hsv(randf(), 0.6, 1.0))
	fm.set_shader_parameter("amp", 0.35 * sc)
	flag.material_override = fm
	flag.position = pos + Vector3(1.6 * sc, 38.0 * sc, 0)
	add_child(flag)
	game_nodes.append(flag)
func _nature(name: String, pos: Vector3, scl: float, yrot: float) -> Node3D:
	var ps: PackedScene = _nat_cache.get(name, null)
	if ps == null:
		var path := "res://assets/nature/" + name + ".glb"
		if not ResourceLoader.exists(path):
			return null
		ps = load(path)
		_nat_cache[name] = ps
	if ps == null:
		return null
	var inst: Node3D = ps.instantiate()
	inst.position = pos
	inst.scale = Vector3.ONE * scl
	inst.rotation.y = yrot
	add_child(inst)
	game_nodes.append(inst)
	_dress_nature(inst)
	return inst

func _dress_nature(node: Node) -> void:
	if node is MeshInstance3D:
		var mi := node as MeshInstance3D
		var mesh := mi.mesh
		if mesh != null:
			for si in range(mesh.get_surface_count()):
				var bm: Material = mesh.surface_get_material(si)
				var col := Color(0.5, 0.6, 0.4)
				if bm is StandardMaterial3D:
					col = (bm as StandardMaterial3D).albedo_color
				var nm := StandardMaterial3D.new()
				var greenish: bool = col.g >= col.r and col.g >= col.b
				nm.albedo_color = col
				nm.albedo_texture = load("res://assets/terrain/up_grass_col.jpg" if greenish else "res://assets/terrain/Rock061_2K_Color.jpg")
				nm.uv1_triplanar = true
				nm.uv1_world_triplanar = true
				nm.uv1_scale = Vector3(0.4, 0.4, 0.4) if greenish else Vector3(0.3, 0.3, 0.3)
				nm.roughness = 0.95
				mi.set_surface_override_material(si, nm)
	for c in node.get_children():
		_dress_nature(c)

# ===================== SKY LAGOON HEIGHTFIELD TERRAIN =====================
# Real rolling hills (solid land Roshan rests on) + rivers carved as genuine
# valleys she swims down into. The player floor follows lagoon_h() in the courtyard.
const LAGOON_RIVERS := [
	[Vector2(-210, -40), Vector2(-150, 30), Vector2(-90, 100), Vector2(-30, 170)],
	[Vector2(205, -30), Vector2(150, 40), Vector2(95, 110), Vector2(45, 180)]]
const LAGOON_RIVER_W := 17.0
const LAGOON_RIVER_DEPTH := 10.0

func _seg_dist(p: Vector2, a: Vector2, b: Vector2) -> float:
	var ab: Vector2 = b - a
	var l2: float = ab.length_squared()
	var t := 0.0
	if l2 > 0.0001:
		t = clampf((p - a).dot(ab) / l2, 0.0, 1.0)
	return p.distance_to(a + ab * t)

func _lagoon_river_dip(lx: float, lz: float) -> float:
	var p := Vector2(lx, lz)
	var best := 9999.0
	for rv in LAGOON_RIVERS:
		for i in range(rv.size() - 1):
			best = minf(best, _seg_dist(p, rv[i], rv[i + 1]))
	if best >= LAGOON_RIVER_W:
		return 0.0
	var t: float = best / LAGOON_RIVER_W
	return LAGOON_RIVER_DEPTH * (1.0 - t * t)   # parabolic channel, deepest at the centre

func _lagoon_bump(lx: float, lz: float, cx: float, cz: float, rad: float, amp: float) -> float:
	var d2: float = (lx - cx) * (lx - cx) + (lz - cz) * (lz - cz)
	var r2: float = rad * rad
	if d2 >= r2:
		return 0.0
	var f: float = 1.0 - d2 / r2
	return amp * f * f

func _lagoon_local(lx: float, lz: float) -> float:
	var r: float = sqrt(lx * lx + lz * lz)
	var h := 0.0
	# rolling hills (away from the central castle + path so gameplay stays clear)
	h += _lagoon_bump(lx, lz, -130.0, 20.0, 62.0, 20.0)
	h += _lagoon_bump(lx, lz, 128.0, -20.0, 64.0, 18.0)
	h += _lagoon_bump(lx, lz, -60.0, 168.0, 54.0, 15.0)
	h += _lagoon_bump(lx, lz, 100.0, 150.0, 54.0, 14.0)
	# rivers carve valleys
	h -= _lagoon_river_dip(lx, lz)
	# smoothly flatten the castle disc + the path corridor so they stay solid & level
	var m_disc: float = 1.0 - smoothstep(50.0, 72.0, r)
	var m_path := 0.0
	if lz > -95.0 and lz < 172.0:
		m_path = 1.0 - smoothstep(16.0, 28.0, absf(lx))
	h = lerpf(h, 0.0, maxf(m_disc, m_path))
	# island rim falls away at the edge
	if r > 205.0:
		h -= (r - 205.0) * 1.2
	return h

func lagoon_h(x: float, z: float) -> float:
	return LEVEL2_POS.y + _lagoon_local(x - LEVEL2_POS.x, z - LEVEL2_POS.z)

func _terr_v(st: SurfaceTool, lx: float, lz: float) -> void:
	st.set_uv(Vector2(lx, lz))
	st.add_vertex(Vector3(lx, _lagoon_local(lx, lz), lz))

func _build_lagoon_terrain(o: Vector3) -> void:
	# blended terrain material: lush grass on the hills/plains, muddy dirt down in the
	# river valleys (CC0 Poly Haven sets), with normal maps for real surface depth
	var tsh := Shader.new()
	tsh.code = "shader_type spatial;\n" + \
		"uniform sampler2D grass_t; uniform sampler2D grass_n; uniform sampler2D dirt_t; uniform sampler2D dirt_n;\n" + \
		"uniform float tile = 0.045; uniform float blo = -6.0; uniform float bhi = 2.5;\n" + \
		"varying float ly;\n" + \
		"void vertex(){ ly = VERTEX.y; }\n" + \
		"void fragment(){\n" + \
		"  vec2 uv = UV * tile;\n" + \
		"  float g = smoothstep(blo, bhi, ly);\n" + \
		"  ALBEDO = mix(texture(dirt_t, uv).rgb, texture(grass_t, uv).rgb, g);\n" + \
		"  NORMAL_MAP = mix(texture(dirt_n, uv).rgb, texture(grass_n, uv).rgb, g);\n" + \
		"  ROUGHNESS = 0.95;\n" + \
		"}"
	var gm := ShaderMaterial.new()
	gm.shader = tsh
	gm.set_shader_parameter("grass_t", load("res://assets/terrain/up_grass_col.jpg"))
	gm.set_shader_parameter("grass_n", load("res://assets/terrain/up_grass_nrm.jpg"))
	gm.set_shader_parameter("dirt_t", load("res://assets/terrain/up_dirt_col.jpg"))
	gm.set_shader_parameter("dirt_n", load("res://assets/terrain/up_dirt_nrm.jpg"))
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var N := 64
	var span := 245.0
	var step: float = span * 2.0 / float(N)
	for i in range(N):
		var x0: float = -span + float(i) * step
		var x1: float = x0 + step
		for j in range(N):
			var z0: float = -span + float(j) * step
			var z1: float = z0 + step
			var cx: float = (x0 + x1) * 0.5
			var cz: float = (z0 + z1) * 0.5
			if sqrt(cx * cx + cz * cz) > 245.0:
				continue
			# winding gives upward-facing normals
			_terr_v(st, x0, z0); _terr_v(st, x1, z1); _terr_v(st, x0, z1)
			_terr_v(st, x0, z0); _terr_v(st, x1, z0); _terr_v(st, x1, z1)
	st.generate_normals()
	st.generate_tangents()   # needed so the terrain normal maps light correctly
	var mi := MeshInstance3D.new()
	mi.mesh = st.commit()
	mi.material_override = gm
	mi.position = o
	add_child(mi)
	game_nodes.append(mi)
	# ---- river water sitting low in each carved valley, with fish ----
	g["l2_fish"] = []
	var fishkinds := ["ClownFish", "Dory", "Carp", "Tuna", "Eel"]
	var wsh := Shader.new()
	wsh.code = """shader_type spatial;
render_mode cull_disabled;
uniform sampler2D ripple;
global uniform float wind_gust;
void vertex(){ VERTEX.y += sin(TIME*1.4 + VERTEX.x*0.3)*0.25; }
void fragment(){
	// flow bands running down the channel
	float f = fract(UV.y*8.0 - TIME*0.3);
	float band = smoothstep(0.0,0.5,f)*smoothstep(1.0,0.5,f);
	// WW contour strokes drifting over the surface
	vec2 luv = vec2(UV.x * 2.0, UV.y * 14.0 - TIME * (0.25 + wind_gust * 0.35));
	vec2 q = luv + vec2(sin(luv.y*1.6 + TIME*0.4), cos(luv.x*2.3 - TIME*0.3))*0.4;
	float b2 = sin(q.x*3.0)*sin(q.y*2.4);
	float lines = smoothstep(0.55,0.8,b2)*(1.0-smoothstep(0.8,0.99,b2));
	// edge foam where the water meets the banks — analytic (distance from the
	// centreline; the channel shape is parabolic so the banks sit near |UV.x-0.5|*2 ~ 0.75)
	float edge = abs(UV.x - 0.5) * 2.0;
	float wob = sin(UV.y*60.0 + TIME*2.2)*0.03 + sin(UV.y*23.0 - TIME*1.3)*0.05;
	float foam = smoothstep(0.62 + wob, 0.92 + wob, edge);
	foam *= 0.75 + 0.25*sin(TIME*3.0 + UV.y*40.0);
	vec3 base=vec3(0.2,0.55,0.8);
	vec3 white=vec3(0.9,0.98,1.0);
	ALBEDO = base + band*vec3(0.3,0.4,0.4) + lines*white*0.55 + foam*white*0.8;
	EMISSION = base*0.3 + band*vec3(0.3,0.5,0.6)*0.6 + (lines*0.5 + foam*0.55)*white;
	vec2 ruv=UV*4.0+vec2(TIME*0.04,TIME*0.07);
	NORMAL_MAP=mix(texture(ripple,ruv).rgb, texture(ripple,ruv*1.7-TIME*0.03).rgb, 0.5);
	NORMAL_MAP_DEPTH=0.6; ROUGHNESS=0.08; METALLIC=0.4;
	ALPHA = clamp(0.82 + foam*0.18, 0.0, 1.0);
}"""
	var ripple_tex := load("res://assets/terrain/up_water_nrm.jpg")
	for rv in LAGOON_RIVERS:
		for i in range(rv.size() - 1):
			var a2: Vector2 = rv[i]
			var b2: Vector2 = rv[i + 1]
			var mid: Vector2 = (a2 + b2) * 0.5
			var leng: float = a2.distance_to(b2)
			var ryaw: float = atan2((b2 - a2).x, (b2 - a2).y)
			var water := MeshInstance3D.new()
			var rq := PlaneMesh.new(); rq.size = Vector2(LAGOON_RIVER_W * 2.0, leng); rq.subdivide_depth = 20
			water.mesh = rq
			var rmat := ShaderMaterial.new(); rmat.shader = wsh
			rmat.set_shader_parameter("ripple", ripple_tex)
			water.material_override = rmat
			# surface sits partway up the valley so the depth reads
			water.position = o + Vector3(mid.x, _lagoon_local(mid.x, mid.y) + LAGOON_RIVER_DEPTH * 0.55, mid.y)
			water.rotation = Vector3(0, ryaw, 0)
			add_child(water); game_nodes.append(water)
		# fish swimming down the channel
		var ra: Vector2 = rv[0]
		var rb: Vector2 = rv[rv.size() - 1]
		var rdir3: Vector3 = Vector3(rb.x - ra.x, 0, rb.y - ra.y).normalized()
		var rlen: float = ra.distance_to(rb)
		for fz in range(6):
			var fishinst := _place_aq(fishkinds[fz % fishkinds.size()], Vector3.ZERO, 1.0 + randf() * 0.6, true)
			if fishinst != null:
				game_nodes.append(fishinst)
				var fa := o + Vector3(ra.x, _lagoon_local(ra.x, ra.y) + 1.5, ra.y)
				(g["l2_fish"] as Array).append({"node": fishinst, "a": fa, "dir": rdir3, "len": rlen, "off": randf() * rlen, "spd": 4.0 + randf() * 4.0, "lane": randf() * 6.0 - 3.0})

func _build_pearl_castle(o: Vector3) -> void:
	wall_pics = []
	# ---------- warm daytime sun for the sky lagoon (soft shadows) ----------
	var sun2 := DirectionalLight3D.new()
	sun2.rotation_degrees = Vector3(-48.0, 35.0, 0.0)
	sun2.light_color = Color(0.6, 0.68, 0.95) if is_night else Color(1.0, 0.96, 0.86)
	sun2.light_energy = 0.5 if is_night else 1.15
	sun2.shadow_enabled = (quality != "speedy")
	sun2.light_specular = 0.3
	add_child(sun2)
	game_nodes.append(sun2)
	# ---------- rolling-hill grass terrain + carved river valleys (real -Y depth) ----------
	_build_lagoon_terrain(o)
	# ---------- rocky floating-island underside ----------
	var cliff := MeshInstance3D.new()
	var cc := CylinderMesh.new()
	cc.top_radius = 236.0
	cc.bottom_radius = 120.0
	cc.height = 54.0
	cc.radial_segments = 40
	cliff.mesh = cc
	cliff.material_override = _up_mat("cliff", 0.04, Color(0.8, 0.74, 0.68))   # rugged rock face
	cliff.position = o + Vector3(0, -29.0, 0)
	add_child(cliff)
	game_nodes.append(cliff)
	# ---------- grand path from the spawn to the castle ----------
	var path := MeshInstance3D.new()
	var pb := BoxMesh.new()
	pb.size = Vector3(18.0, 0.6, 270.0)
	path.mesh = pb
	path.material_override = _up_mat("cobble", 0.10)   # cobblestone path to the castle (0.035 made each cobble metres wide)
	path.position = o + Vector3(0, 2.4, 45.0)
	add_child(path)
	game_nodes.append(path)
	# lamp posts + banners (her book art) line the path
	var banners := ["p_seattle", "p_snowman", "p_garden", "p_trampoline", "p_slide", "p_xmas"]
	for li in range(6):
		var z := 150.0 - float(li) * 46.0
		for sgn in [-1.0, 1.0]:
			var post := _l2_box(o + Vector3(sgn * 13.0, 6.0, z), Vector3(1.0, 12.0, 1.0), Color(0.5, 0.36, 0.22))
			var lampbulb := MeshInstance3D.new()
			var lb := SphereMesh.new()
			lb.radius = 1.1
			lb.height = 2.2
			lampbulb.mesh = lb
			var lm := StandardMaterial3D.new()
			lm.emission_enabled = true
			lm.emission = Color(1.0, 0.85, 0.5)
			lm.emission_energy_multiplier = 3.0
			lampbulb.material_override = lm
			lampbulb.position = o + Vector3(sgn * 13.0, 12.5, z)
			add_child(lampbulb)
			game_nodes.append(lampbulb)
			var lo := OmniLight3D.new()
			lo.light_color = Color(1.0, 0.85, 0.55)
			lo.light_energy = 1.6
			lo.omni_range = 26.0
			lo.position = lampbulb.position
			add_child(lo)
			game_nodes.append(lo)
		# a hanging banner of her memories on the left posts
		_hang_portrait(o + Vector3(-13.0, 7.0, z) + Vector3(0.7, 0, 0), Vector3(0, 90, 0), banners[li])
	# ---------- decorate the meadow with CC0 nature (dense, grounded, clustered) ----------
	var trees := ["tree_palm", "tree_pineRoundF", "tree_default_fall", "tree_simple_fall", "tree_fat"]
	var flowers := ["flower_redA", "flower_yellowB", "flower_purpleA"]
	var seed := 3
	# tree CLUSTERS (little groves read as a real forest edge)
	for grove in range(14):
		seed = (seed * 1103515245 + 12345) & 0x7fffffff
		var ga: float = float(seed % 1000) / 1000.0 * TAU
		var grad: float = 60.0 + float((seed / 1000) % 1000) / 1000.0 * 165.0
		var gcx: float = cos(ga) * grad
		var gcz: float = sin(ga) * grad
		if absf(gcx) < 26.0 and gcz > -95.0 and gcz < 165.0:
			continue
		for t in range(3 + (seed / 3) % 4):
			seed = (seed * 1103515245 + 12345) & 0x7fffffff
			var ox: float = float(seed % 200) / 10.0 - 10.0
			var oz: float = float((seed / 200) % 200) / 10.0 - 10.0
			_nature(trees[(seed / 11) % trees.size()], o + Vector3(gcx + ox, _lagoon_local(gcx + ox, gcz + oz) - 0.5, gcz + oz), 9.0 + float(seed % 5), float(seed % 628) / 100.0)
	# undergrowth: bushes, mushrooms, grass tufts, flower clumps
	for k in range(90):
		seed = (seed * 1103515245 + 12345) & 0x7fffffff
		var ang: float = float(seed % 1000) / 1000.0 * TAU
		var rad: float = 26.0 + float((seed / 1000) % 1000) / 1000.0 * 200.0
		var px: float = cos(ang) * rad
		var pz: float = sin(ang) * rad
		if absf(px) < 13.0 and pz > -92.0 and pz < 168.0:
			continue
		var pick := (seed / 7) % 10
		var gp := Vector3(px, _lagoon_local(px, pz) - 0.2, pz)
		var yr := float(seed % 628) / 100.0
		if pick < 3:
			_nature("plant_bushLargeTriangle", o + gp, 6.0, yr)
		elif pick < 5:
			_nature("plant_bush", o + gp, 5.0, yr)
		elif pick < 6:
			_nature("mushroom_red", o + gp, 5.0, yr)
		elif pick < 7:
			_nature("mushroom_tanGroup", o + gp, 5.5, yr)
		elif pick < 8:
			_nature("grass_leafsLarge", o + gp, 5.0, yr)
		else:
			_nature(flowers[(seed / 17) % flowers.size()], o + gp, 6.0, yr)
	# a calm pond off to the side, ringed with cattails
	var pond := MeshInstance3D.new()
	var pondm := CylinderMesh.new()
	pondm.top_radius = 34.0
	pondm.bottom_radius = 34.0
	pondm.height = 0.6
	pond.mesh = pondm
	var pmm := StandardMaterial3D.new()
	pmm.albedo_color = Color(0.3, 0.62, 0.85, 0.82)
	pmm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	pmm.metallic = 0.6
	pmm.roughness = 0.08
	pmm.emission_enabled = true
	pmm.emission = Color(0.2, 0.45, 0.65)
	pmm.emission_energy_multiplier = 0.18
	pond.material_override = pmm
	pond.position = o + Vector3(-95, _lagoon_local(-95, 70) + 0.6, 70)
	add_child(pond)
	game_nodes.append(pond)
	for ct in range(14):
		var cta: float = float(ct) / 14.0 * TAU
		var cpx: float = -95 + cos(cta) * 36.0
		var cpz: float = 70 + sin(cta) * 36.0
		_nature("grass_leafsLarge", o + Vector3(cpx, _lagoon_local(cpx, cpz) - 0.3, cpz), 5.5, randf() * TAU)
	# (rivers + fish are built as real carved valleys in _build_lagoon_terrain above)
	# player-crafted FRIENDS from the Crafting Studio hang around the courtyard
	for fi in range(custom_friends.size()):
		var cf2: Array = custom_friends[fi]
		if cf2.size() < 7:
			continue
		var frn := _make_creature_node(String(cf2[0]), Color(cf2[1], cf2[2], cf2[3]), Color(cf2[4], cf2[5], cf2[6]), cf2.size() > 7 and int(cf2[7]) == 1, cf2.size() > 8 and int(cf2[8]) == 1)
		var fang: float = float(fi) * 1.3
		frn.position = o + Vector3(cos(fang) * (34.0 + float(fi % 5) * 11.0), 6.0, 70.0 + sin(fang) * 45.0)
		add_child(frn)
		game_nodes.append(frn)
	# a big rainbow arc over the meadow
	var rainbow := MeshInstance3D.new()
	var rt := TorusMesh.new()
	rt.inner_radius = 118.0
	rt.outer_radius = 130.0
	rt.rings = 48
	rt.ring_segments = 24
	rainbow.mesh = rt
	var rbsh := Shader.new()
	rbsh.code = "shader_type spatial;\nrender_mode cull_disabled, unshaded;\nvoid fragment(){\n\tfloat b = UV.y;\n\tvec3 c = vec3(0.0);\n\tif(b<0.16)c=vec3(0.9,0.2,0.3);else if(b<0.33)c=vec3(1.0,0.6,0.2);else if(b<0.5)c=vec3(1.0,0.9,0.3);else if(b<0.66)c=vec3(0.3,0.8,0.4);else if(b<0.83)c=vec3(0.3,0.6,1.0);else c=vec3(0.6,0.4,0.9);\n\tALBEDO=c;\n\tEMISSION=c*0.4;\n\tALPHA=0.6;\n}"
	var rbm := ShaderMaterial.new()
	rbm.shader = rbsh
	rainbow.material_override = rbm
	rainbow.position = o + Vector3(40, 0, -10)
	rainbow.rotation_degrees = Vector3(0, 0, 90)
	add_child(rainbow)
	game_nodes.append(rainbow)
	# (home portal removed — the way back to the ocean is now inside the castle / Level 3)
	# drifting butterflies for life
	var bfly := CPUParticles3D.new()
	bfly.amount = 26
	bfly.lifetime = 6.0
	bfly.emission_shape = CPUParticles3D.EMISSION_SHAPE_BOX
	bfly.emission_box_extents = Vector3(180, 14, 180)
	bfly.gravity = Vector3.ZERO
	bfly.initial_velocity_min = 2.0
	bfly.initial_velocity_max = 5.0
	bfly.angular_velocity_min = -90.0
	bfly.angular_velocity_max = 90.0
	bfly.scale_amount_min = 1.2
	bfly.scale_amount_max = 2.0
	var bq := QuadMesh.new()
	bq.size = Vector2(1.2, 1.2)
	bfly.mesh = bq
	var bmat := StandardMaterial3D.new()
	bmat.albedo_texture = load(GTA + "flower.png")
	bmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	bmat.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	bmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	bfly.material_override = bmat
	bfly.position = o + Vector3(0, 14, 30)
	add_child(bfly)
	game_nodes.append(bfly)
	# ---------- the castle (back of the island) ----------
	var c := o + Vector3(0, 0, -120.0)
	# (the moat was removed — rivers run through the meadow instead)
	# a long wooden bridge from the courtyard, ACROSS the moat, right up to the door
	var bridge := _l2_box(c + Vector3(0, 2.6, 40.0), Vector3(13.0, 0.8, 60.0), Color(0.62, 0.45, 0.28))
	bridge.material_override.roughness = 1.0
	# bridge railings + posts
	for bsgn in [-1.0, 1.0]:
		_l2_box(c + Vector3(bsgn * 6.2, 4.0, 40.0), Vector3(0.6, 2.2, 60.0), Color(0.5, 0.36, 0.22))
		for bp in range(7):
			_l2_box(c + Vector3(bsgn * 6.2, 4.2, 12.0 + float(bp) * 9.0), Vector3(1.0, 3.0, 1.0), Color(0.45, 0.32, 0.2))
	# keep + battlements
	# keep — a STONE shell with a real doorway opening, so the open door reveals a warm interior (not a white void)
	var _keep_parts := [
		_l2_box(c + Vector3(-18, 26, 12), Vector3(20, 52, 1.5), Color(0.88, 0.86, 0.92)),
		_l2_box(c + Vector3(18, 26, 12), Vector3(20, 52, 1.5), Color(0.88, 0.86, 0.92)),
		_l2_box(c + Vector3(0, 38, 12), Vector3(16, 28, 1.5), Color(0.88, 0.86, 0.92)),
		_l2_box(c + Vector3(0, 26, -28), Vector3(56, 52, 1.5), Color(0.82, 0.80, 0.87)),
		_l2_box(c + Vector3(-28, 26, -8), Vector3(1.5, 52, 40), Color(0.84, 0.82, 0.89)),
		_l2_box(c + Vector3(28, 26, -8), Vector3(1.5, 52, 40), Color(0.84, 0.82, 0.89)),
		_l2_box(c + Vector3(0, 52, -8), Vector3(56, 1.5, 40), Color(0.82, 0.80, 0.87))]
	for _kp in _keep_parts:
		_kp.material_override = _up_mat("marble", 0.07, Color(0.98, 0.9, 1.0))   # big pastel dressed-stone courses (the red-brick photo read as dark noise at any scale)
	# ---- warm interior foyer, visible through the doorway ----
	var _foyback := _l2_box(c + Vector3(0, 12, -2), Vector3(22, 24, 1.0), Color(0.9, 0.66, 0.45))
	_foyback.material_override = _up_mat("marble", 0.07, Color(1.0, 0.82, 0.62))   # same stone as the keep, warmed by the foyer light
	_l2_box(c + Vector3(0, 0.7, 5), Vector3(13, 0.4, 16), Color(0.72, 0.16, 0.22))      # red carpet leading in
	_l2_box(c + Vector3(-11, 12, 5), Vector3(1.0, 24, 14), Color(0.84, 0.82, 0.89))     # foyer left wall
	_l2_box(c + Vector3(11, 12, 5), Vector3(1.0, 24, 14), Color(0.84, 0.82, 0.89))      # foyer right wall
	_l2_box(c + Vector3(0, 24, 5), Vector3(22, 1.0, 14), Color(0.80, 0.78, 0.85))       # foyer ceiling
	var _foylight := OmniLight3D.new()
	_foylight.light_color = Color(1.0, 0.82, 0.5)
	_foylight.light_energy = 3.2
	_foylight.omni_range = 32.0
	_foylight.position = c + Vector3(0, 14, 6)
	add_child(_foylight); game_nodes.append(_foylight)
	_hang_portrait(c + Vector3(0, 13, -1.3), Vector3(0, 0, 0), "p_seattle")             # a glimpse of 'inside'''
	for bx in range(-4, 5):
		_l2_box(c + Vector3(float(bx) * 6.0, 53.0, -8.0), Vector3(3.5, 6.0, 40.0), Color(0.9, 0.88, 0.95))
	# four big towers
	_l2_tower(c + Vector3(-32.0, 2.0, 10.0), 1.9)
	_l2_tower(c + Vector3(32.0, 2.0, 10.0), 1.9)
	_l2_tower(c + Vector3(-32.0, 2.0, -28.0), 1.9)
	_l2_tower(c + Vector3(32.0, 2.0, -28.0), 1.9)
	# ---- the Mermaid Roshan stained glass — the grand centrepiece on the FRONT facade ----
	_glass_window(c + Vector3(0, 38.0, 12.3), Vector3(0, 0, 0), 30.0)
	# gold frame around the rose window
	for fxg in [-1.0, 1.0]:
		_l2_box(c + Vector3(fxg * 11.5, 38.0, 12.2), Vector3(1.2, 32.0, 1.0), Color(0.95, 0.8, 0.4), 0.3)
	_l2_box(c + Vector3(0, 54.0, 12.2), Vector3(24.0, 1.2, 1.0), Color(0.95, 0.8, 0.4), 0.3)
	_l2_box(c + Vector3(0, 22.0, 12.2), Vector3(24.0, 1.2, 1.0), Color(0.95, 0.8, 0.4), 0.3)
	# ---- crenellated battlements along the keep top ----
	for cz2 in [12.0, -28.0]:
		for cmx in range(-4, 5):
			var mr := _l2_box(c + Vector3(float(cmx) * 6.4, 53.5, cz2), Vector3(3.2, 5.0, 2.0), Color(0.9, 0.88, 0.95))
			mr.material_override = _up_mat("marble", 0.07, Color(0.98, 0.9, 1.0))
	for cmx2 in range(-3, 4):
		for csx in [-28.0, 28.0]:
			var mr2 := _l2_box(c + Vector3(csx, 53.5, -8.0 + float(cmx2) * 6.4), Vector3(2.0, 5.0, 3.2), Color(0.9, 0.88, 0.95))
			mr2.material_override = _up_mat("marble", 0.07, Color(0.98, 0.9, 1.0))
	# ---- royal banners flanking the door ----
	for bxs in [-1.0, 1.0]:
		var ban := MeshInstance3D.new()
		var banq := QuadMesh.new(); banq.size = Vector2(5.0, 18.0)
		ban.mesh = banq
		var banm := StandardMaterial3D.new()
		banm.albedo_color = Color(0.7, 0.18, 0.3) if bxs < 0.0 else Color(0.2, 0.35, 0.7)
		banm.emission_enabled = true; banm.emission = banm.albedo_color * 0.4
		banm.cull_mode = BaseMaterial3D.CULL_DISABLED; banm.roughness = 0.9
		ban.material_override = banm
		ban.position = c + Vector3(bxs * 9.5, 17.0, 12.6)
		add_child(ban); game_nodes.append(ban)
		# a little gold star crest on the banner
		var crest := Label3D.new()
		crest.text = "★"; crest.font_size = 110; crest.modulate = Color(1.0, 0.88, 0.4)
		crest.position = c + Vector3(bxs * 9.5, 19.0, 12.8)
		add_child(crest); game_nodes.append(crest)
	# big arched door (starts closed)
	var door := _l2_box(c + Vector3(0, 12.0, 12.4), Vector3(16.0, 24.0, 1.2), Color(0.62, 0.42, 0.26), 0.0)
	door.material_override = _up_mat("wood", 0.06, Color(0.85, 0.6, 0.4))   # weathered timber door
	door.material_override.uv1_world_triplanar = false   # the door slides open — keep its grain glued to the mesh, not the world
	l2_door = door
	g["door_closed_y"] = door.position.y
	g["entry"] = door.position
	# glowing archway frame (revealed when the door opens)
	var arch := _l2_box(c + Vector3(0, 12.0, 12.0), Vector3(17.0, 25.0, 0.4), Color(0.55, 0.9, 1.0), 0.0)
	arch.visible = false
	g["arch"] = arch
	var dl := Label3D.new()
	dl.text = "Princess Huluu\u2019s Castle"
	dl.font_size = 90
	dl.outline_size = 18
	dl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	dl.position = c + Vector3(0, 30.0, 14.0)
	add_child(dl)
	game_nodes.append(dl)
	# ---------- 3 Dream Stars: low + along the path, easy for a 4yo ----------
	var spots := [Vector3(-22, 5, 95), Vector3(24, 5, 20), Vector3(-20, 5, -55)]
	for idx in range(spots.size()):
		var sp: Vector3 = o + spots[idx]
		# a low, friendly platform with a soft ramp feel
		var plat := _l2_box(sp + Vector3(0, -3.5, 0), Vector3(12, 1.4, 12), Color(0.9, 0.82, 0.98), 0.1)
		_nature("flower_yellowB", sp + Vector3(-3, -2.6, -3), 4.0, 0.0)
		_nature("flower_redA", sp + Vector3(3, -2.6, 3), 4.0, 1.0)
		var star := Label3D.new()
		star.text = "\u2605"
		star.font_size = 340
		star.pixel_size = 0.05
		star.modulate = Color(1.0, 1.0, 1.0)
		star.outline_size = 34
		star.set_meta("rainbow", randf() * TAU)
		star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		star.position = sp + Vector3(0, 4.0, 0)
		add_child(star)
		game_nodes.append(star)
		var sl := OmniLight3D.new()
		sl.light_color = Color(1.0, 0.9, 0.5)
		sl.light_energy = 3.2
		sl.omni_range = 34.0
		star.add_child(sl)
		l2_stars.append({"node": star, "got": false})
	# ---------- clouds + rainbow accents ----------
	for cz in range(14):
		var cloud := MeshInstance3D.new()
		var cs := SphereMesh.new()
		cs.radius = 8.0 + randf() * 7.0
		cs.height = 10.0
		cloud.mesh = cs
		var cm2 := StandardMaterial3D.new()
		cm2.albedo_color = Color(1, 1, 1)
		cm2.roughness = 1.0
		cloud.material_override = cm2
		cloud.position = o + Vector3(randf() * 380.0 - 190.0, 55.0 + randf() * 40.0, randf() * 380.0 - 190.0)
		cloud.scale = Vector3(2.2, 0.7, 1.7)
		add_child(cloud)
		game_nodes.append(cloud)
	_build_fairy_pond(o)

func _build_lagoon_night(o: Vector3) -> void:
	# subtle night dressing for the Sky Lagoon: a moon + a scatter of twinkling stars
	var moon := MeshInstance3D.new()
	var ms := SphereMesh.new(); ms.radius = 16.0; ms.height = 32.0
	moon.mesh = ms
	moon.material_override = _soft_mat(Color(1.0, 0.97, 0.85), 2.2)
	moon.position = o + Vector3(-120.0, 130.0, -180.0)
	add_child(moon); game_nodes.append(moon)
	var ml := OmniLight3D.new()
	ml.light_color = Color(0.7, 0.78, 1.0); ml.light_energy = 1.2; ml.omni_range = 400.0
	ml.position = moon.position; add_child(ml); game_nodes.append(ml)
	var seed := 91
	for k in range(60):
		seed = (seed * 1103515245 + 12345) & 0x7fffffff
		var ang: float = float(seed % 1000) / 1000.0 * TAU
		var el: float = 0.3 + float((seed / 1000) % 1000) / 1000.0 * 0.6
		var dist := 260.0
		var star := MeshInstance3D.new()
		var ss := SphereMesh.new(); ss.radius = 0.7 + float(seed % 5) * 0.25; ss.height = ss.radius * 2.0
		star.mesh = ss
		star.material_override = _soft_mat(Color(1.0, 1.0, 0.92), 3.0)
		star.position = o + Vector3(cos(ang) * dist * cos(el), 60.0 + el * 150.0, sin(ang) * dist * cos(el))
		add_child(star); game_nodes.append(star)

func _build_fairy_pond(o: Vector3) -> void:
	# a glowing fairy pond off in the courtyard — swim into it (after the castle opens)
	# to fly the fairy on-rails shooter
	var c: Vector3 = o + Vector3(125.0, 0.0, 35.0)
	fairy_pond_pos = c + Vector3(0, 6.0, 0)
	var pond := MeshInstance3D.new()
	var cm := CylinderMesh.new(); cm.top_radius = 17.0; cm.bottom_radius = 17.0; cm.height = 1.0
	pond.mesh = cm
	var pmat := StandardMaterial3D.new()
	pmat.albedo_color = Color(0.4, 0.55, 0.95); pmat.metallic = 0.85; pmat.roughness = 0.07
	pmat.emission_enabled = true; pmat.emission = Color(0.5, 0.55, 1.0); pmat.emission_energy_multiplier = 0.6
	pond.material_override = pmat
	pond.position = c + Vector3(0, 2.6, 0)
	add_child(pond); game_nodes.append(pond)
	# a ring of glowing fairy flowers around it
	for k in range(10):
		var a: float = float(k) / 10.0 * TAU
		var fl := MeshInstance3D.new()
		var fm := SphereMesh.new(); fm.radius = 1.3; fm.height = 2.6
		fl.mesh = fm
		fl.material_override = _soft_mat(Color.from_hsv(float(k) / 10.0, 0.5, 1.0), 1.5)
		fl.position = c + Vector3(cos(a) * 17.0, 3.4, sin(a) * 17.0)
		add_child(fl); game_nodes.append(fl)
	var l := OmniLight3D.new()
	l.light_color = Color(0.7, 0.72, 1.0); l.light_energy = 2.6; l.omni_range = 32.0
	l.position = c + Vector3(0, 9, 0); add_child(l); game_nodes.append(l)
	var lab := Label3D.new()
	lab.text = "🧚 Fairy Pond — fly!"
	lab.font_size = 64; lab.pixel_size = 0.05; lab.outline_size = 14
	lab.modulate = Color(0.88, 0.82, 1.0); lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lab.position = c + Vector3(0, 13, 0); add_child(lab); game_nodes.append(lab)

func _tick_level2(delta: float, ppos: Vector3) -> void:
	if mg_kind != "":
		_tick_mg2d(delta)
		return
	if l2_cutscene_t >= 0.0:
		_tick_cutscene(delta)
		return
	if String(g.get("phase", "court")) == "hall":
		_tick_castle_hall(delta, ppos)
		return
	for fd in g.get("l2_fish", []):
		var fn2: Node3D = fd["node"]
		if not is_instance_valid(fn2):
			continue
		fd["off"] = fmod(float(fd["off"]) + float(fd["spd"]) * delta, float(fd["len"]))
		var base: Vector3 = (fd["a"] as Vector3) + (fd["dir"] as Vector3) * float(fd["off"])
		var side: Vector3 = (fd["dir"] as Vector3).cross(Vector3.UP).normalized()
		var fp: Vector3 = base + side * float(fd["lane"]) + Vector3(0, 3.2 + sin(float(g.get("t", 0.0)) * 3.0 + float(fd["off"])) * 0.4, 0)
		fn2.position = fp
		fn2.look_at(fp + (fd["dir"] as Vector3) * 2.0, Vector3.UP)
	var got := 0
	var nxt: Node3D = null
	for sd in l2_stars:
		if bool(sd["got"]):
			got += 1
			continue
		var star: Label3D = sd["node"]
		star.position.y += sin(float(g["t"]) * 2.0 + star.position.x) * 0.02
		star.rotate_y(delta * 1.6)
		star.scale = Vector3.ONE * (1.0 + sin(float(g["t"]) * 4.0) * 0.12)
		if nxt == null:
			nxt = star
		var d: float = star.position.distance_to(ppos)
		# gentle magnet so a 4yo who swims close gets pulled in
		if d < 32.0:
			player.position = player.position.lerp(star.position, minf(0.85, delta * 1.7 * (1.0 - d / 32.0)))
		if d < 14.0:
			sd["got"] = true
			got += 1
			_sparkle_burst(star.position, Color(1.0, 0.9, 0.4))
			if chime != null:
				chime.pitch_scale = 1.0 + float(got) * 0.12
				chime.play()
			if voice != null:
				voice.pitch_scale = 1.0 + randf() * 0.2
				voice.play()
			star.visible = false
			if star.get_child_count() > 0:
				star.get_child(0).queue_free()
			if got >= 3:
				_open_castle_door()
	if got >= 3 and not l2_open:
		_open_castle_door()
	# iridescent rainbow shimmer on the dream stars
	for sd2 in l2_stars:
		var stn: Label3D = sd2["node"]
		if is_instance_valid(stn) and stn.has_meta("rainbow"):
			var hue: float = fmod(float(g["t"]) * 0.4 + float(stn.get_meta("rainbow")), 1.0)
			stn.modulate = Color.from_hsv(hue, 0.55, 1.0)
	# fairy pond — fly the on-rails shooter (active once the castle is open)
	fairy_cool = maxf(0.0, fairy_cool - delta)
	if l2_open and fairy_cool <= 0.0 and fairy_pond_pos != Vector3.ZERO:
		if Vector2(fairy_pond_pos.x - ppos.x, fairy_pond_pos.z - ppos.z).length() < 13.0 and absf(fairy_pond_pos.y - ppos.y) < 16.0:
			fairy_cool = 12.0
			_start_game(fairy_fr)
			return
	# the rainbow gateway always takes you back to the ocean
	mg_cool = maxf(0.0, mg_cool - delta)
	if mg_cool <= 0.0 and mg_kind == "":
		for wp in wall_pics:
			var wpp: Vector3 = wp["pos"]
			if Vector2(wpp.x - ppos.x, wpp.z - ppos.z).length() < 7.0 and absf(wpp.y - ppos.y) < 9.0:
				if String(wp["art"]) == "p_slide":
					_l2_start_slide()
				else:
					_mg2d_open(String(PIC_GAME[String(wp["art"])]))
				return
	if not l2_open:
		hud_game.text = "Dream Stars: %d / 3  -  follow the arrow!  (or touch a picture to play!)" % got
	else:
		hud_game.text = "The castle is OPEN!  Swim to the glowing door!"
		# magnet toward the fixed doorway (the door itself slides up out of view)
		var entry: Vector3 = g.get("entry", l2_door.position)
		var dd: float = Vector2(entry.x - ppos.x, entry.z - ppos.z).length()
		if dd < 36.0:
			var pull: Vector3 = entry + Vector3(0, 2, 10)
			player.position = player.position.lerp(pull, minf(0.75, delta * 1.5 * (1.0 - dd / 36.0)))
		if dd < 20.0:
			_enter_castle_interior()

# ============ STAGE 2 MINIGAMES (2D tap overlays, launched from wall pictures) ============
func _mg2d_open(kind: String) -> void:
	if kind == "slide":
		_l2_start_slide()   # the rainbow slide is always the 3D play-place, never the old 2D screen
		return
	mg_kind = kind
	mg = {"t": 0.0, "btns": []}
	if mg2d_layer == null:
		mg2d_layer = CanvasLayer.new()
		mg2d_layer.layer = 7
		add_child(mg2d_layer)
	mg2d_root = Control.new()
	mg2d_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	mg2d_layer.add_child(mg2d_root)
	mg2d_layer.visible = true
	# clean themed gradient background (no busy book page behind the toys)
	var themes := {
		"snowman": [Color(0.50, 0.66, 0.86), Color(0.88, 0.94, 1.0)],
		"garden": [Color(0.45, 0.78, 0.95), Color(0.7, 0.92, 0.6)],
		"trampoline": [Color(0.45, 0.72, 1.0), Color(0.86, 0.95, 1.0)],
		"slide": [Color(0.55, 0.7, 1.0), Color(1.0, 0.85, 0.92)],
		"xmas": [Color(0.10, 0.18, 0.30), Color(0.25, 0.40, 0.48)]}
	var grad := Gradient.new()
	grad.set_color(0, themes[kind][0])
	grad.set_color(1, themes[kind][1])
	var gt := GradientTexture2D.new()
	gt.gradient = grad
	gt.fill_from = Vector2(0, 0)
	gt.fill_to = Vector2(0, 1)
	gt.width = 64
	gt.height = 64
	var bg := TextureRect.new()
	bg.texture = gt
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.stretch_mode = TextureRect.STRETCH_SCALE
	mg2d_root.add_child(bg)
	# responsive 1280x720 stage, scaled + centred to any screen (fixes landscape)
	mg2d_stage = Control.new()
	mg2d_stage.size = Vector2(1280, 720)
	var vp: Vector2 = get_viewport().get_visible_rect().size
	var sc: float = minf(vp.x / 1280.0, vp.y / 720.0)
	mg2d_stage.scale = Vector2(sc, sc)
	mg2d_stage.position = (vp - Vector2(1280, 720) * sc) * 0.5
	mg2d_root.add_child(mg2d_stage)
	mg["hud"] = _mg_label("", 40, Vector2(40, 26))
	if kind == "snowman": _mg_build_snowman()
	elif kind == "garden": _mg_build_garden()
	elif kind == "trampoline": _mg_build_trampoline()
	elif kind == "slide": _mg_build_slide()
	elif kind == "xmas": _mg_build_xmas()

func _mg_label(txt: String, size: int, pos: Vector2) -> Label:
	var l := Label.new()
	l.text = txt
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15, 0.95))
	l.add_theme_constant_override("outline_size", 12)
	l.position = pos
	mg2d_stage.add_child(l)
	return l

func _mg_circle(pos: Vector2, r: float, col: Color) -> Panel:
	var p := Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(int(r))
	sb.shadow_color = Color(0, 0, 0, 0.28)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 5)
	sb.border_color = col.darkened(0.22)              # soft rim for roundness
	sb.set_border_width_all(maxi(2, int(r * 0.05)))
	p.add_theme_stylebox_override("panel", sb)
	p.size = Vector2(r * 2.0, r * 2.0)
	p.position = pos - Vector2(r, r)
	mg2d_stage.add_child(p)
	# glossy highlight (upper-left) gives a 3D ball sheen
	var hl := Panel.new()
	var hsb := StyleBoxFlat.new()
	hsb.bg_color = Color(1, 1, 1, 0.38)
	hsb.set_corner_radius_all(int(r * 0.5))
	hl.add_theme_stylebox_override("panel", hsb)
	hl.size = Vector2(r * 0.85, r * 0.6)
	hl.position = Vector2(r * 0.32, r * 0.22)
	hl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	p.add_child(hl)
	return p

func _mg_sprite(path: String, pos: Vector2, sz: Vector2) -> TextureRect:
	var t := TextureRect.new()
	t.texture = load(path)
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	t.size = sz
	t.position = pos - sz * 0.5
	mg2d_stage.add_child(t)
	return t

func _mg_artbtn(path: String, pos: Vector2, sz: Vector2) -> Button:
	var b := Button.new()
	b.position = pos - sz * 0.5
	b.custom_minimum_size = sz
	b.size = sz
	b.flat = true
	var t := TextureRect.new()
	t.texture = load(path)
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	t.set_anchors_preset(Control.PRESET_FULL_RECT)
	t.mouse_filter = Control.MOUSE_FILTER_IGNORE
	b.add_child(t)
	mg2d_stage.add_child(b)
	(mg["btns"] as Array).append(b)
	return b

func _mg_roundbtn(pos: Vector2, r: float, col: Color, txt: String = "") -> Button:
	var b := Button.new()
	b.position = pos - Vector2(r, r)
	b.custom_minimum_size = Vector2(r * 2.0, r * 2.0)
	b.size = Vector2(r * 2.0, r * 2.0)
	b.text = txt
	b.add_theme_font_size_override("font_size", 44)
	var sb := StyleBoxFlat.new()
	sb.bg_color = col
	sb.set_corner_radius_all(int(r))
	b.add_theme_stylebox_override("normal", sb)
	var sb2: StyleBoxFlat = sb.duplicate()
	sb2.bg_color = col.lightened(0.3)
	b.add_theme_stylebox_override("pressed", sb2)
	b.add_theme_stylebox_override("hover", sb)
	mg2d_stage.add_child(b)
	(mg["btns"] as Array).append(b)
	return b

func _mg2d_win(msg: String) -> void:
	if bool(mg.get("won", false)):
		return
	mg["won"] = true
	show_msg("Roshan", msg, "win")
	for i in range(8):
		_sparkle_burst(player.position + Vector3(randf() * 8 - 4, randf() * 6, randf() * 8 - 4), Color.from_hsv(randf(), 0.6, 1.0))
	pearl_count += 2
	_update_hud()
	_write_save()
	# hide the buttons + show a celebratory banner over the FINISHED scene, hold ~1.6s, then close
	for b in (mg.get("btns", []) as Array):
		if is_instance_valid(b):
			b.disabled = true
			b.visible = false
	if mg2d_stage != null and is_instance_valid(mg2d_stage):
		var banner := _mg_label("\u2b50  Yay! You did it!  \u2b50", 76, Vector2(330, 26))
		banner.add_theme_color_override("font_color", Color(1.0, 0.95, 0.4))
		for ci in range(40):
			var conf := ColorRect.new()
			conf.color = Color.from_hsv(randf(), 0.7, 1.0)
			conf.size = Vector2(18, 18)
			conf.position = Vector2(randf() * 1280, -20.0 - randf() * 200.0)
			conf.rotation = randf() * TAU
			mg2d_stage.add_child(conf)
			var tw := create_tween()
			tw.tween_property(conf, "position:y", 760.0, 1.3 + randf() * 0.5).set_delay(randf() * 0.3)
	get_tree().create_timer(1.6).timeout.connect(_mg2d_close)

func _mg2d_close() -> void:
	if mg2d_root != null and is_instance_valid(mg2d_root):
		mg2d_root.queue_free()
	mg2d_root = null
	mg2d_stage = null
	if mg2d_layer != null:
		mg2d_layer.visible = false
	mg_kind = ""
	mg = {}
	mg_cool = 8.0

# ---- SNOWMAN: tap 3 snow piles to stack the snowman, then place the face ----
func _mg_build_snowman() -> void:
	mg["phase"] = "roll"
	mg["balls"] = 0
	mg["face"] = 0
	mg["pile_taps"] = [0, 0, 0]
	(mg["hud"] as Label).text = "Tap the snow piles to build a snowman!"
	# ground
	_mg_circle(Vector2(640, 980), 700.0, Color(0.95, 0.97, 1.0, 0.5))
	for i in range(3):
		var pile := _mg_roundbtn(Vector2(230 + float(i) * 250, 600), 95.0, Color(0.96, 0.98, 1.0))
		var idx := i
		pile.pressed.connect(func(): _mg_snow_tap(idx))
	mg["body"] = []   # stacked balls (centre)

func _mg_snow_tap(i: int) -> void:
	if mg_kind != "snowman" or String(mg["phase"]) != "roll":
		return
	var taps: Array = mg["pile_taps"]
	taps[i] = int(taps[i]) + 1
	if int(taps[i]) >= 1:
		(mg["btns"] as Array)[i].visible = false
		var b := int(mg["balls"]) + 1
		mg["balls"] = b
		var r := 150.0 - float(b) * 26.0
		var bc := Vector2(980, 560 - float(b - 1) * 175.0)
		var ball := _mg_circle(bc, r, Color(0.97, 0.99, 1.0))
		(mg["body"] as Array).append(ball)
		if b >= 3:
			mg["head_pos"] = bc
			_mg_snow_face_phase()

func _mg_snow_face_phase() -> void:
	mg["phase"] = "face"
	(mg["hud"] as Label).text = "Now give him a face! Tap the carrot and coal."
	var carrot := _mg_artbtn("res://assets/mg/carrot.png", Vector2(360, 600), Vector2(150, 110))
	carrot.pressed.connect(func(): _mg_snow_face("carrot", carrot))
	for i in range(2):
		var coal := _mg_artbtn("res://assets/mg/coal.png", Vector2(250 + float(i) * 220, 600), Vector2(90, 90))
		var idx := i
		coal.pressed.connect(func(): _mg_snow_face("coal" + str(idx), coal))

func _mg_snow_face(_part: String, b: Button) -> void:
	if mg_kind != "snowman" or String(mg["phase"]) != "face" or not b.visible:
		return
	b.visible = false
	var head: Vector2 = mg.get("head_pos", Vector2(980, 210))
	if _part == "carrot":
		_mg_sprite("res://assets/mg/carrot.png", head + Vector2(0, 14), Vector2(95, 60))
	elif _part == "coal0":
		_mg_sprite("res://assets/mg/coal.png", head + Vector2(-24, -18), Vector2(42, 42))
	else:
		_mg_sprite("res://assets/mg/coal.png", head + Vector2(24, -18), Vector2(42, 42))
	mg["face"] = int(mg["face"]) + 1
	if int(mg["face"]) >= 3:
		_mg2d_win("I built a snowman! Yay!")

# ---- GARDEN: tap sprouts to grow them into flowers ----
func _mg_build_garden() -> void:
	mg["grown"] = 0
	mg["stage"] = [0, 0, 0, 0, 0]
	mg["flowers"] = ["k_flower1", "flower", "flower2", "k_flower2", "flower3"]   # each plant ends as a DIFFERENT flower
	(mg["hud"] as Label).text = "Tap each seed to grow it: seed, then sprout, then a FLOWER!"
	_mg_sprite("res://assets/mg/sun.png", Vector2(120, 130), Vector2(180, 180))
	# a soft grassy mound across the bottom
	var mound := _mg_circle(Vector2(640, 1050), 760.0, Color(0.5, 0.78, 0.45))
	mound.size.y = 500.0
	mound.position = Vector2(-120, 640)
	# five clay pots, each starting as a SEED
	for i in range(5):
		var x := 180.0 + float(i) * 240.0
		var potm := _mg_circle(Vector2(x, 640), 64.0, Color(0.78, 0.42, 0.28))
		potm.size = Vector2(150, 100)
		potm.position = Vector2(x - 75, 600)
		var sp := _mg_artbtn("res://assets/mg/seed.png", Vector2(x, 600), Vector2(72, 72))
		sp.set_meta("hx", x)
		var idx := i
		sp.pressed.connect(func(): _mg_garden_tap(idx, sp))
	# Roshan watering, watching over the garden
	_mg_sprite("res://assets/characters/roshan_sprite.png", Vector2(1140, 360), Vector2(180, 230))
	_mg_sprite("res://assets/mg/wateringcan.png", Vector2(1010, 430), Vector2(150, 130))
	# a couple of drifting butterflies
	for bi in range(3):
		var bf := _mg_sprite("res://assets/mg/butterfly.png", Vector2(300 + float(bi) * 350, 220), Vector2(90, 90))
		bf.set_meta("bf", float(bi))

func _mg_garden_tap(i: int, b: Button) -> void:
	if mg_kind != "garden":
		return
	var st: Array = mg["stage"]
	if int(st[i]) >= 2:
		return
	st[i] = int(st[i]) + 1
	var x: float = b.get_meta("hx")
	_sparkle_burst(player.position + Vector3(0, 1, 0), Color(0.4, 0.7, 1.0))
	var tex := b.get_child(0) as TextureRect
	if int(st[i]) == 1:
		# seed -> seedling (same small sprout for every plant)
		tex.texture = load("res://assets/mg/k_sprout.png")
		b.size = Vector2(120, 150)
		b.custom_minimum_size = b.size
		b.position = Vector2(x, 540) - b.size * 0.5
	else:
		# seedling -> a distinct flower, with a happy pop
		tex.texture = load("res://assets/mg/" + String((mg["flowers"] as Array)[i]) + ".png")
		b.size = Vector2(175, 205)
		b.custom_minimum_size = b.size
		b.position = Vector2(x, 495) - b.size * 0.5
		b.pivot_offset = b.size * 0.5
		b.disabled = true
		var tw := create_tween()
		tw.tween_property(b, "scale", Vector2(1.2, 1.2), 0.12)
		tw.tween_property(b, "scale", Vector2(1.0, 1.0), 0.12)
		mg["grown"] = int(mg["grown"]) + 1
		if int(mg["grown"]) >= 5:
			_mg2d_win("Look at my beautiful flower garden!")

# ---- TRAMPOLINE: tap BOUNCE to jump up to the star ----
func _mg_build_trampoline() -> void:
	mg["bounces"] = 0
	mg["star_y"] = 90.0
	(mg["hud"] as Label).text = "Tap JUMP to bounce up and TOUCH the star!"
	mg["star"] = _mg_sprite("res://assets/mg/star.png", Vector2(640, 90), Vector2(140, 140))
	# trampoline (kept high enough that the JUMP button fits on the 1280x720 stage in landscape)
	var tramp := _mg_circle(Vector2(640, 520), 200.0, Color(0.25, 0.5, 0.85))
	tramp.size.y = 56.0
	tramp.position = Vector2(640 - 200, 492)
	mg["rest_y"] = 430.0
	mg["roshan"] = _mg_sprite("res://assets/characters/roshan_sprite.png", Vector2(640, 430), Vector2(150, 190))
	var b := _mg_roundbtn(Vector2(640, 648), 66.0, Color(0.3, 0.6, 1.0), "JUMP")
	b.pressed.connect(_mg_tramp_tap)

func _mg_tramp_tap() -> void:
	if mg_kind != "trampoline":
		return
	mg["bounces"] = int(mg["bounces"]) + 1
	var r: TextureRect = mg["roshan"]
	var rest_y: float = float(mg.get("rest_y", 430.0))
	var star_y: float = float(mg.get("star_y", 90.0))
	# each bounce reaches higher; Roshan only WINS when her sprite actually reaches the star
	var apex_center: float = rest_y - float(mg["bounces"]) * 85.0
	var sprite_top: float = apex_center - 95.0
	var reached: bool = sprite_top <= star_y + 35.0
	if reached:
		apex_center = star_y + 110.0   # land her right at the star
	var rest_top: float = rest_y - 95.0
	var tw := create_tween()
	tw.tween_property(r, "position:y", apex_center - 95.0, 0.25).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(r, "position:y", rest_top, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	if reached:
		tw.tween_callback(func(): _mg2d_win("Boing! I touched the star!"))

# ---- SLIDE: tap GO, ride the rainbow slide ----
func _mg_build_slide() -> void:
	mg["phase"] = "ready"
	(mg["hud"] as Label).text = "Tap GO for the rainbow slide!"
	# the rainbow slide bands (diagonal)
	var cols := [Color(0.9, 0.2, 0.3), Color(1.0, 0.6, 0.2), Color(1.0, 0.9, 0.3), Color(0.3, 0.8, 0.4), Color(0.3, 0.6, 1.0), Color(0.6, 0.4, 0.9)]
	for i in range(cols.size()):
		var band := ColorRect.new()
		band.color = cols[i]
		band.size = Vector2(1500, 60)
		band.position = Vector2(-100, 150 + float(i) * 58.0)
		band.rotation = 0.5
		mg2d_stage.add_child(band)
	mg["roshan"] = _mg_sprite("res://assets/characters/roshan_sprite.png", Vector2(160, 150), Vector2(140, 180))
	var b := _mg_roundbtn(Vector2(640, 650), 80.0, Color(1.0, 0.5, 0.7), "GO!")
	b.pressed.connect(_mg_slide_go)

func _mg_slide_go() -> void:
	if mg_kind != "slide" or String(mg["phase"]) != "ready":
		return
	mg["phase"] = "ride"
	mg["ride_t"] = 0.0
	(mg["btns"] as Array)[0].visible = false

# ---- XMAS: tap ornaments onto the tree, friendship flower on top ----
func _mg_build_xmas() -> void:
	mg["placed"] = 0
	(mg["hud"] as Label).text = "Tap the ornaments onto the tree!"
	_mg_sprite("res://assets/mg/xtree.png", Vector2(640, 430), Vector2(420, 560))
	mg["orn_spots"] = [Vector2(640, 300), Vector2(580, 400), Vector2(700, 400), Vector2(600, 520), Vector2(700, 520)]
	for i in range(5):
		var o := _mg_artbtn("res://assets/mg/orn" + str(i + 1) + ".png", Vector2(180 + float(i) * 150, 660), Vector2(110, 110))
		var idx := i
		o.pressed.connect(func(): _mg_xmas_tap(idx, o))
	var fl := _mg_artbtn("res://assets/book/friendship_flower.png", Vector2(1050, 660), Vector2(130, 130))
	fl.disabled = true
	fl.modulate = Color(0.5, 0.5, 0.5)
	fl.pressed.connect(_mg_xmas_flower)
	mg["flowerbtn"] = fl

func _mg_xmas_tap(i: int, b: Button) -> void:
	if mg_kind != "xmas" or not b.visible:
		return
	b.visible = false
	var spots: Array = mg["orn_spots"]
	_mg_sprite("res://assets/mg/orn" + str(i + 1) + ".png", spots[i], Vector2(70, 70))
	mg["placed"] = int(mg["placed"]) + 1
	if int(mg["placed"]) >= 5:
		(mg["flowerbtn"] as Button).disabled = false
		(mg["flowerbtn"] as Button).modulate = Color(1.3, 1.3, 1.0)

func _mg_xmas_flower() -> void:
	if mg_kind != "xmas" or int(mg["placed"]) < 5:
		return
	_mg_sprite("res://assets/book/friendship_flower.png", Vector2(640, 200), Vector2(140, 130))
	_mg2d_win("The friendship flower on top! It is beautiful!")

func _tick_mg2d(delta: float) -> void:
	if mg_kind == "":
		return
	mg["t"] = float(mg["t"]) + delta
	if mg_kind == "garden" and mg2d_stage != null:
		for c in mg2d_stage.get_children():
			if c is TextureRect and (c as TextureRect).has_meta("bf"):
				var ph: float = (c as TextureRect).get_meta("bf")
				c.position += Vector2(cos(float(mg["t"]) * 1.3 + ph) * 1.6, sin(float(mg["t"]) * 2.0 + ph) * 1.2)
	if mg_kind == "slide" and String(mg.get("phase", "")) == "ride":
		var rt := float(mg["ride_t"]) + delta
		mg["ride_t"] = rt
		var r: TextureRect = mg["roshan"]
		var p := clampf(rt / 3.0, 0.0, 1.0)
		r.position = Vector2(160 + p * 920.0, 150 + p * 560.0 + sin(rt * 6.0) * 24.0)
		r.rotation = 0.5 + sin(rt * 5.0) * 0.15
		if p >= 1.0:
			_mg2d_win("Wheee! Best slide ever!")

func _open_castle_door() -> void:
	if l2_open:
		return
	l2_open = true
	# ----- CUTSCENE: glorious door opening -----
	l2_cutscene_t = 5.0
	prev_track = cur_track
	_play_music("castle_open")
	show_msg("Princess Huluu", "You found all three stars! Behold... my castle opens!", "greet")
	var arch: Node3D = g.get("arch")
	if arch != null and is_instance_valid(arch):
		arch.visible = true
		var am: StandardMaterial3D = (arch as MeshInstance3D).material_override
		am.emission_enabled = true
		am.emission = Color(0.5, 0.9, 1.0)
		am.emission_energy_multiplier = 2.6
	# the great doors slide open after a beat
	var top_y: float = float(g.get("door_closed_y", l2_door.position.y)) + 30.0
	var tw := create_tween()
	tw.tween_interval(0.8)
	tw.tween_property(l2_door, "position:y", top_y, 1.6).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	# a ring of golden light blooms at the doorway
	var halo := _halo(l2_door.position + Vector3(0, 0, 2), Color(1.0, 0.9, 0.45), 30.0)
	game_nodes.append(halo)

func _tick_cutscene(delta: float) -> void:
	l2_cutscene_t -= delta
	# bursts of sparkles at the doorway through the whole cutscene
	if fmod(l2_cutscene_t, 0.35) < delta and l2_door != null:
		_sparkle_burst(l2_door.position + Vector3(randf() * 16 - 8, randf() * 10, 2), Color.from_hsv(randf(), 0.5, 1.0))
	# slowly swing the camera to admire the door
	if player != null:
		player.vel = Vector3.ZERO
		var look: Vector3 = (g.get("entry", l2_door.position) as Vector3)
		player.yaw = lerp_angle(player.yaw, atan2(look.x - player.position.x, look.z - player.position.z), 1.0 - pow(0.1, delta))
	if l2_cutscene_t <= 0.0:
		l2_cutscene_t = -1.0
		if cur_track == "castle_open":
			_play_music(prev_track if prev_track != "" else "finale")
		show_msg("Roshan", "Wow! Let's go inside!")

func _enter_castle_interior() -> void:
	g["l2_fish"] = []
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	arena_solids.clear()
	fade_walls.clear()
	lagoon_floor = false   # the castle hall is flat indoor ground
	g["phase"] = "hall"
	arena_center = CASTLE_POS
	arena_dome = 60.0
	arena_ceil = 31.0   # keep Roshan below every interior ceiling (lowest sits at +32) instead of clipping through
	# warm indoor castle light
	var ie := Environment.new()
	ie.background_mode = Environment.BG_COLOR
	ie.background_color = Color(0.12, 0.10, 0.16)
	ie.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	ie.ambient_light_color = Color(0.9, 0.82, 0.7)
	ie.ambient_light_energy = 0.8
	_wind_waker_bloom(ie, 0.6, 0.22, 1.05)   # threshold above 1.0: only true emitters bloom — pale lit walls stay crisp instead of smearing white
	ie.fog_enabled = true
	ie.fog_light_color = Color(0.5, 0.42, 0.45)
	ie.fog_density = 0.002   # 0.006 pink-hazed the whole hall and mushed the floor pattern into "spliced" blotches
	arena_env = ie
	_grade(ie)
	we_node.environment = ie
	_build_castle_hall(CASTLE_POS)
	player.cam_back = 6.5   # pull the chase camera in so it does not clip the hall / back-room walls
	player.cam_high = 4.2
	player.position = CASTLE_POS + Vector3(0, 6, 24)
	player.yaw = 0.0
	player.vel = Vector3.ZERO
	show_msg("Pearl Castle", "The Grand Hall! Princess Huluu is waiting up on the throne - climb the royal staircase!")

func _panel_glass(pos: Vector3, rot_deg: Vector3, w: float, h: float) -> void:
	# a stained-glass grid of glowing coloured panels (no mermaid)
	var cols := [Color(0.9, 0.3, 0.4), Color(0.3, 0.6, 1.0), Color(1.0, 0.85, 0.3), Color(0.4, 0.85, 0.5), Color(0.7, 0.4, 0.9), Color(1.0, 0.55, 0.3)]
	var root := Node3D.new()
	root.position = pos
	root.rotation_degrees = rot_deg
	add_child(root)
	game_nodes.append(root)
	var nx := 3
	var ny := 4
	for ix in range(nx):
		for iy in range(ny):
			var q := MeshInstance3D.new()
			var qm := QuadMesh.new()
			qm.size = Vector2(w / float(nx) * 0.9, h / float(ny) * 0.9)
			q.mesh = qm
			var mm := StandardMaterial3D.new()
			var cc: Color = cols[(ix + iy * nx) % cols.size()]
			mm.albedo_color = Color(cc.r, cc.g, cc.b, 0.72)
			mm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			mm.cull_mode = BaseMaterial3D.CULL_DISABLED
			mm.emission_enabled = true
			mm.emission = cc
			mm.emission_energy_multiplier = 0.85
			mm.roughness = 0.4
			q.material_override = mm
			q.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			q.position = Vector3((float(ix) - float(nx - 1) * 0.5) * w / float(nx), (float(iy) - float(ny - 1) * 0.5) * h / float(ny), 0)
			root.add_child(q)
	var bl := OmniLight3D.new()
	bl.light_color = Color(1.0, 0.95, 0.95)
	bl.light_energy = 2.0
	bl.omni_range = h * 2.0
	bl.position = pos
	bl.translate_object_local(Vector3(0, 0, -3.0))
	add_child(bl)
	game_nodes.append(bl)

func _glass_window(pos: Vector3, rot_deg: Vector3, height: float) -> void:
	var pane := MeshInstance3D.new()
	var q := QuadMesh.new()
	q.size = Vector2(height * 0.72, height)
	pane.mesh = q
	var m := StandardMaterial3D.new()
	var tex := load("res://assets/book/hall/glass_mermaid.png")
	m.albedo_texture = tex
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	m.emission_enabled = true
	m.emission_texture = tex
	m.emission_energy_multiplier = 0.9
	m.roughness = 0.5
	pane.material_override = m
	pane.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF   # the quad cast a huge round shadow blob onto the facade
	pane.position = pos
	pane.rotation_degrees = rot_deg
	add_child(pane)
	game_nodes.append(pane)
	# backlight so it glows like real stained glass
	var bl := OmniLight3D.new()
	bl.light_color = Color(1.0, 0.95, 0.9)
	bl.light_energy = 2.2
	bl.omni_range = height * 2.2
	bl.position = pos
	bl.translate_object_local(Vector3(0, 0, -3.0))
	add_child(bl)
	game_nodes.append(bl)

const PIC_GAME := {"p_snowman": "snowman", "p_garden": "garden", "p_trampoline": "trampoline", "p_slide": "slide", "p_xmas": "xmas"}
func _hang_portrait(pos: Vector3, rot_deg: Vector3, art: String) -> void:
	if PIC_GAME.has(art):
		wall_pics.append({"pos": pos, "art": art})
	var frame := MeshInstance3D.new()
	var fb := BoxMesh.new()
	fb.size = Vector3(9.5, 12.5, 0.6)
	frame.mesh = fb
	var fm := StandardMaterial3D.new()
	fm.albedo_color = Color(0.85, 0.68, 0.3)
	fm.metallic = 0.7
	fm.roughness = 0.35
	fm.emission_enabled = true
	fm.emission = Color(0.5, 0.4, 0.18)
	fm.emission_energy_multiplier = 0.25
	frame.material_override = fm
	frame.position = pos
	frame.rotation_degrees = rot_deg
	add_child(frame)
	game_nodes.append(frame)
	var pic := MeshInstance3D.new()
	var pq := QuadMesh.new()
	pq.size = Vector2(8.0, 11.0)
	pic.mesh = pq
	var pm := StandardMaterial3D.new()
	pm.albedo_texture = load("res://assets/book/hall/" + art + ".jpg")
	pm.roughness = 0.6
	pm.emission_enabled = true
	pm.emission_texture = pm.albedo_texture
	pm.emission_energy_multiplier = 0.35
	pic.material_override = pm
	pic.position = pos
	pic.rotation_degrees = rot_deg
	pic.translate_object_local(Vector3(0, 0, 0.4))
	add_child(pic)
	game_nodes.append(pic)
	# little picture light
	var pl := OmniLight3D.new()
	pl.light_color = Color(1.0, 0.92, 0.78)
	pl.light_energy = 1.0
	pl.omni_range = 11.0
	pl.position = pos
	pl.translate_object_local(Vector3(0, 4, 4))
	add_child(pl)
	game_nodes.append(pl)

func _build_castle_hall(o: Vector3) -> void:
	# polished marble floor
	var floor := MeshInstance3D.new()
	var fb := BoxMesh.new()
	fb.size = Vector3(70, 1.0, 80)
	floor.mesh = fb
	var fm := _up_mat("marble", 0.08, Color(0.95, 0.93, 0.98))   # polished marble hall floor (0.03 gave room-sized slabs that read as broken splicing)
	fm.metallic = 0.25
	fm.roughness = 0.22
	floor.material_override = fm
	floor.position = o + Vector3(0, 0, 6)
	add_child(floor)
	game_nodes.append(floor)
	# checker accent tiles
	for cxx in range(-3, 4):
		for czz in range(-3, 5):
			if (cxx + czz) % 2 == 0:
				continue
			var tile := _l2_box(o + Vector3(float(cxx) * 9.0, 0.55, 6.0 + float(czz) * 9.0), Vector3(8.6, 0.1, 8.6), Color(0.55, 0.5, 0.72))
			# lavender-tinted marble, same scale as the floor beneath: the old brown
			# flagstone photo under a purple tint made a muddy mismatched checker
			tile.material_override = _up_mat("marble", 0.08, Color(0.72, 0.66, 0.9))
	# plush red carpet runner from the entrance up to the stairs
	var runner := _l2_box(o + Vector3(0, 0.62, 14.0), Vector3(10.0, 0.15, 52.0), Color(0.72, 0.16, 0.22))
	runner.material_override.roughness = 1.0
	for trim in [-5.4, 5.4]:
		_l2_box(o + Vector3(trim, 0.66, 14.0), Vector3(0.7, 0.2, 52.0), Color(0.95, 0.8, 0.35), 0.15)
	# walls (each upright wall also registers a solid collider so Roshan can't swim through it)
	var wcol := Color(0.95, 0.92, 0.97)
	var scol := Color(0.93, 0.9, 0.95)
	# back wall, SEGMENTED to leave two real doorway openings at x=+-22 (the side archways)
	_iwall(o + Vector3(0, 18, -34), Vector3(35.0, 36, 1.5), wcol, "marble")      # center (behind throne/glass)
	_iwall(o + Vector3(-30.75, 18, -34), Vector3(8.5, 36, 1.5), wcol, "marble")  # left edge
	_iwall(o + Vector3(30.75, 18, -34), Vector3(8.5, 36, 1.5), wcol, "marble")   # right edge
	_iwall(o + Vector3(-22, 25.5, -34), Vector3(9.0, 21, 1.5), wcol, "marble")   # lintel over left arch
	_iwall(o + Vector3(22, 25.5, -34), Vector3(9.0, 21, 1.5), wcol, "marble")    # lintel over right arch
	# left side wall, SEGMENTED to leave a doorway at z=-16 into the new MUSIC ROOM
	_iwall(o + Vector3(-35, 18, 17.5), Vector3(1.5, 36, 57), scol, "marble")  # front segment (z +46..-11)
	_iwall(o + Vector3(-35, 18, -27.5), Vector3(1.5, 36, 13), scol, "marble") # back segment (z -21..-34)
	_iwall(o + Vector3(-35, 27, -16), Vector3(1.5, 18, 10), scol, "marble")   # lintel over the music-room door
	# right side wall, SEGMENTED to leave a doorway at z=-16 into the new BEDROOM
	_iwall(o + Vector3(35, 18, 27.5), Vector3(1.5, 36, 37), scol, "marble")  # front segment (z +46..+9)
	_iwall(o + Vector3(35, 18, -6.0), Vector3(1.5, 36, 10), scol, "marble")  # mid segment (z -1..-11)
	_iwall(o + Vector3(35, 18, -27.5), Vector3(1.5, 36, 13), scol, "marble") # back segment (z -21..-34)
	_iwall(o + Vector3(35, 27, -16), Vector3(1.5, 18, 10), scol, "marble")   # lintel over the bedroom door
	_iwall(o + Vector3(35, 27, 4), Vector3(1.5, 18, 10), scol, "marble")     # lintel over the craft-room door
	_l2_box(o + Vector3(0, 35, 6), Vector3(70, 1.5, 80), Color(0.85, 0.82, 0.9))      # ceiling (no collider; arena_ceil caps height)
	# regal stained-glass panels behind the throne (the Mermaid Roshan glass now lives
	# on the castle's FRONT exterior — this is a plain coloured rose window for Huluu)
	_panel_glass(o + Vector3(0, 23, -33.0), Vector3(0, 0, 0), 17.0, 24.0)
	# royal red-carpet staircase up to the throne dais
	for st in range(7):
		_l2_box(o + Vector3(0, 1.5 + float(st) * 2.0, -10.0 - float(st) * 2.2), Vector3(16.0 - float(st) * 0.6, 2.0, 3.0), Color(0.8, 0.25, 0.3))
	# throne dais
	_l2_box(o + Vector3(0, 15.0, -27.0), Vector3(14, 2.0, 6), Color(0.95, 0.85, 0.55), 0.2)
	var throne := _l2_box(o + Vector3(0, 18.5, -28.0), Vector3(5, 6, 2), Color(0.95, 0.8, 0.4), 0.3)
	throne.material_override.metallic = 0.7
	# Princess Huluu, ruler of the Pearl Castle, waiting on her throne
	var huluu := Sprite3D.new()
	huluu.texture = load("res://assets/characters/friends/huluu.png")
	huluu.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	huluu.pixel_size = 0.011
	huluu.position = o + Vector3(0, 21.0, -27.0)
	add_child(huluu)
	game_nodes.append(huluu)
	var hl := OmniLight3D.new()
	hl.light_color = Color(1.0, 0.9, 0.95)
	hl.light_energy = 1.4
	hl.omni_range = 16.0
	hl.position = o + Vector3(0, 22.0, -24.0)
	add_child(hl)
	game_nodes.append(hl)
	# ---------- columns line the hall ----------
	for cz in [-24.0, -8.0, 8.0, 24.0]:
		for cx in [-28.0, 28.0]:
			var col := MeshInstance3D.new()
			var colm := CylinderMesh.new()
			colm.top_radius = 2.2
			colm.bottom_radius = 2.6
			colm.height = 34.0
			col.mesh = colm
			col.material_override = _up_mat("marble", 0.07, Color(0.96, 0.93, 0.98))   # same dressed stone as the walls
			col.position = o + Vector3(cx, 17.0, cz)
			add_child(col)
			game_nodes.append(col)
			_cyl_solid(col.position, 2.6, 17.0)   # pillars are solid — Roshan slides around them
			# gold capital + base
			_l2_box(o + Vector3(cx, 33.6, cz), Vector3(6, 1.4, 6), Color(0.95, 0.8, 0.4), 0.2)
			_l2_box(o + Vector3(cx, 1.0, cz), Vector3(6, 2.0, 6), Color(0.9, 0.85, 0.7))
			# warm sconce glow at each column
			var sc := OmniLight3D.new()
			sc.light_color = Color(1.0, 0.78, 0.5)
			sc.light_energy = 1.7
			sc.omni_range = 24.0
			sc.position = o + Vector3(cx * 0.86, 20.0, cz)
			add_child(sc)
			game_nodes.append(sc)
			var flame := MeshInstance3D.new()
			var fl := SphereMesh.new()
			fl.radius = 0.7
			fl.height = 1.4
			flame.mesh = fl
			var flm := StandardMaterial3D.new()
			flm.emission_enabled = true
			flm.emission = Color(1.0, 0.7, 0.35)
			flm.emission_energy_multiplier = 4.0
			flame.material_override = flm
			flame.position = sc.position
			add_child(flame)
			game_nodes.append(flame)
	# ---------- tapestries between the columns ----------
	var tcols := [Color(0.7, 0.2, 0.3), Color(0.25, 0.4, 0.75), Color(0.45, 0.3, 0.65), Color(0.2, 0.55, 0.45)]
	for ti in range(4):
		for sgn in [-1.0, 1.0]:
			var tap := MeshInstance3D.new()
			var tq := QuadMesh.new()
			tq.size = Vector2(7.0, 16.0)
			tap.mesh = tq
			var tm2 := StandardMaterial3D.new()
			tm2.albedo_color = tcols[ti]
			tm2.roughness = 1.0
			tm2.cull_mode = BaseMaterial3D.CULL_DISABLED
			tm2.emission_enabled = true
			tm2.emission = tcols[ti] * 0.2
			tap.material_override = tm2
			tap.position = o + Vector3(sgn * 34.0, 20.0, -24.0 + float(ti) * 16.0)
			tap.rotation_degrees = Vector3(0, -90.0 * sgn, 0)
			add_child(tap)
			game_nodes.append(tap)
	# ---------- her memories framed along the hall walls ----------
	# (Roshan wall-art portraits removed from the Grand Hall — inconsistent with how the games work here)
	# ---------- potted plants flank the throne + entrance ----------
	for pp in [Vector3(-9, 1.0, -22), Vector3(9, 1.0, -22), Vector3(-7, 1.0, 36), Vector3(7, 1.0, 36)]:
		var pot := MeshInstance3D.new()
		var potm := CylinderMesh.new()
		potm.top_radius = 1.6
		potm.bottom_radius = 1.2
		potm.height = 2.4
		pot.mesh = potm
		var ptm := StandardMaterial3D.new()
		ptm.albedo_color = Color(0.7, 0.4, 0.3)
		ptm.roughness = 0.7
		pot.material_override = ptm
		pot.position = o + pp + Vector3(0, 0.5, 0)
		add_child(pot)
		game_nodes.append(pot)
		_nature("plant_bushLargeTriangle", o + pp + Vector3(0, 1.6, 0), 3.0, randf() * TAU)
	# ---------- hanging chandeliers (mesh + light) ----------
	for chz in [-12.0, 10.0]:
		var ch := MeshInstance3D.new()
		var cht := TorusMesh.new()
		cht.inner_radius = 2.4
		cht.outer_radius = 3.2
		ch.mesh = cht
		var chm := StandardMaterial3D.new()
		chm.albedo_color = Color(0.95, 0.8, 0.4)
		chm.metallic = 0.8
		chm.roughness = 0.3
		chm.emission_enabled = true
		chm.emission = Color(1.0, 0.8, 0.4)
		chm.emission_energy_multiplier = 0.8
		ch.material_override = chm
		ch.position = o + Vector3(0, 30.0, chz)
		add_child(ch)
		game_nodes.append(ch)
		var chl := OmniLight3D.new()
		chl.light_color = Color(1.0, 0.85, 0.55)
		chl.light_energy = 2.2
		chl.omni_range = 30.0
		chl.position = o + Vector3(0, 28.0, chz)
		add_child(chl)
		game_nodes.append(chl)
	# OPEN back doorways (dark archways) flanking the throne
	for dx in [-22.0, 22.0]:
		_l2_box(o + Vector3(dx - 5.0, 8, -33.2), Vector3(1.2, 16, 1.2), Color(0.8, 0.7, 0.5), 0.1)  # gold frame posts
		_l2_box(o + Vector3(dx + 5.0, 8, -33.2), Vector3(1.2, 16, 1.2), Color(0.8, 0.7, 0.5), 0.1)
		_l2_box(o + Vector3(dx, 15.5, -33.2), Vector3(11, 1.2, 1.2), Color(0.8, 0.7, 0.5), 0.1)
	# ---------- REAL BACK ROOM behind the throne (entered through the two side archways) ----------
	var br := o + Vector3(0, 0, -46.0)   # back-room center
	var brfloor := _l2_box(br + Vector3(0, 0.4, 0), Vector3(52, 1.0, 22), Color(0.86, 0.82, 0.92))   # floor
	brfloor.material_override = _up_mat("marble", 0.08, Color(0.9, 0.86, 0.95))   # same stone family as the hall floor
	_l2_box(br + Vector3(0, 33.0, 0), Vector3(52, 1.5, 22), Color(0.82, 0.79, 0.88))           # ceiling
	_iwall(br + Vector3(0, 16, -10.5), Vector3(52, 34, 1.5), Color(0.93, 0.9, 0.95), "marble")          # back wall
	_iwall(br + Vector3(-25.5, 16, 0), Vector3(1.5, 34, 22), Color(0.93, 0.9, 0.95), "marble")          # left wall
	_iwall(br + Vector3(25.5, 16, 0), Vector3(1.5, 34, 22), Color(0.93, 0.9, 0.95), "marble")           # right wall
	# warm light + a soft red runner inside
	var brl := OmniLight3D.new(); brl.light_color = Color(1.0, 0.85, 0.6); brl.light_energy = 2.0; brl.omni_range = 34.0
	brl.position = br + Vector3(0, 20, 0); add_child(brl); game_nodes.append(brl)
	_l2_box(br + Vector3(0, 1.0, 2.0), Vector3(10, 0.2, 26), Color(0.72, 0.16, 0.22))          # carpet from arch to treasure
	# a glowing royal treasure chest = the bonus trigger
	var chest := _l2_box(br + Vector3(0, 3.0, -1.0), Vector3(7, 5, 4.5), Color(0.95, 0.78, 0.35), 0.6)
	chest.material_override.metallic = 0.6
	_l2_box(br + Vector3(0, 6.0, -1.0), Vector3(7.4, 1.4, 5.0), Color(0.8, 0.62, 0.25), 0.5)   # lid rim
	g["secret_door"] = chest.position
	var sl2 := OmniLight3D.new(); sl2.light_color = Color(0.6, 0.95, 1.0); sl2.light_energy = 2.2; sl2.omni_range = 16.0
	sl2.position = chest.position + Vector3(0, 4, 0); add_child(sl2); game_nodes.append(sl2)
	# Daddy mermaid lives in the secret room (his real recorded voice greets Roshan)
	var daddy := Sprite3D.new()
	daddy.texture = load("res://assets/characters/friends/daddy.png")
	daddy.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	daddy.pixel_size = 0.0066
	daddy.position = br + Vector3(10, 8, -3)
	add_child(daddy); game_nodes.append(daddy)
	var dlt := OmniLight3D.new(); dlt.light_color = Color(1.0, 0.9, 0.8); dlt.light_energy = 1.8; dlt.omni_range = 22.0
	dlt.position = daddy.position + Vector3(0, 2, 5); add_child(dlt); game_nodes.append(dlt)
	var sl := OmniLight3D.new()
	sl.light_color = Color(0.5, 0.9, 1.0)
	sl.light_energy = 1.5
	sl.omni_range = 14.0
	sl.position = o + Vector3(-22, 7, -33.0)   # invite glow at the left archway
	add_child(sl)
	game_nodes.append(sl)
	var sl3 := OmniLight3D.new()
	sl3.light_color = Color(0.5, 0.9, 1.0)
	sl3.light_energy = 1.5
	sl3.omni_range = 14.0
	sl3.position = o + Vector3(22, 7, -33.0)   # invite glow at the right archway
	add_child(sl3)
	game_nodes.append(sl3)
	var slab := Label3D.new()
	slab.text = "\u2728 Daddy Mermaid \u2728"
	slab.font_size = 40
	slab.pixel_size = 0.02
	slab.outline_size = 10
	slab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	slab.position = g["secret_door"] + Vector3(0, 7.0, 0)
	add_child(slab)
	game_nodes.append(slab)
	# just TWO framed memories on the side walls (fewer pictures)
	# (the swim-through xylophone now lives in the dedicated MUSIC ROOM off the left wall \u2014 see _build_castle_music_room)
	# (the crafting easel now lives in the dedicated CRAFT ROOM off the right wall — see _build_castle_craft_room)
	# hanging chandeliers
	for cz in [-14.0, 8.0]:
		var ch := OmniLight3D.new()
		ch.light_color = Color(1.0, 0.8, 0.5)
		ch.light_energy = 2.0
		ch.omni_range = 26.0
		ch.position = o + Vector3(0, 26, cz)
		add_child(ch)
		game_nodes.append(ch)
		var bulb := MeshInstance3D.new()
		var bs := SphereMesh.new()
		bs.radius = 0.8
		bs.height = 1.6
		bulb.mesh = bs
		var bm := StandardMaterial3D.new()
		bm.emission_enabled = true
		bm.emission = Color(1.0, 0.85, 0.5)
		bm.emission_energy_multiplier = 3.0
		bulb.material_override = bm
		bulb.position = ch.position
		add_child(bulb)
		game_nodes.append(bulb)
	# the crown Star atop the throne — the goal
	var crown := Label3D.new()
	crown.text = "\u2605"
	crown.font_size = 340
	crown.modulate = Color(1.0, 0.9, 0.3)
	crown.outline_size = 34
	crown.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	crown.position = o + Vector3(0, 24.0, -28.0)
	add_child(crown)
	game_nodes.append(crown)
	l2_stars = [{"node": crown, "got": false}]
	# EXIT door at the entrance — swim into it to go back to the ocean
	var exit := MeshInstance3D.new()
	var et := TorusMesh.new()
	et.inner_radius = 3.4
	et.outer_radius = 4.6
	exit.mesh = et
	exit.material_override = _rainbow_mat()
	exit.position = o + Vector3(0, 5.0, 44.0)
	add_child(exit)
	game_nodes.append(exit)
	var exl := OmniLight3D.new()
	exl.light_color = Color(0.6, 0.9, 1.0)
	exl.light_energy = 2.0
	exl.omni_range = 18.0
	exl.position = exit.position
	add_child(exl)
	game_nodes.append(exl)
	var exlab := Label3D.new()
	exlab.text = "\u2190 leave the castle"
	exlab.font_size = 60
	exlab.pixel_size = 0.03
	exlab.outline_size = 12
	exlab.modulate = Color(0.7, 0.95, 1.0)
	exlab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	exlab.position = exit.position + Vector3(0, 6.5, 0)
	add_child(exlab)
	game_nodes.append(exlab)
	g["hall_exit"] = exit.position
	# (no ocean ring here — reaching Princess Huluu / the Crown Star at the throne is the link back to the ocean)
	# a cosy royal bedroom opens off the right-hand wall (doorway at z=-16)
	_build_castle_bedroom(o)
	# ...and a music room opens off the left-hand wall (doorway at z=-16)
	_build_castle_music_room(o)
	_build_castle_craft_room(o)

func _build_castle_music_room(o: Vector3) -> void:
	# Roomy music hall off the LEFT wall (doorway x=-35, z=-16).
	# Footprint x:-52..-35 (width 17), z:-24..+14 (depth 38) — a long room so the
	# xylophone has space. Interior corners stay inside the dome (r<58).
	var mo: Vector3 = o + Vector3(-43.5, 0, -5)           # room centre
	var wall := Color(0.86, 0.88, 0.98)                  # cool lilac plaster
	# floor + ceiling (no colliders — floor clamp / arena_ceil handle vertical)
	var mfloor := _l2_box(mo + Vector3(0, 0.4, 0), Vector3(19, 1.0, 40), Color(0.5, 0.45, 0.7))
	mfloor.material_override = _up_mat("wood", 0.1, Color(0.62, 0.56, 0.85))   # violet-stained boards
	_l2_box(mo + Vector3(0, 33.0, 0), Vector3(19, 1.5, 40), Color(0.8, 0.82, 0.92))
	# enclosing walls (the right/hall side is the segmented hall wall already built)
	_iwall(mo + Vector3(-9.25, 16, 0), Vector3(1.5, 34, 40), wall)       # far wall (x=-52.75)
	_iwall(mo + Vector3(0, 16, -19.75), Vector3(19, 34, 1.5), wall)      # back wall (z=-24.75)
	_iwall(mo + Vector3(0, 16, 19.75), Vector3(19, 34, 1.5), wall)       # front wall (z=+14.75)
	# gold doorway frame around the opening in the hall wall
	for dz in [-21.0, -11.0]:
		_l2_box(o + Vector3(-35, 8, dz), Vector3(1.2, 16, 1.2), Color(0.85, 0.72, 0.45), 0.15)
	# soft rug by the entrance
	var rug := _l2_box(mo + Vector3(3.0, 0.95, -11.0), Vector3(9, 0.1, 8), Color(0.35, 0.3, 0.6))
	rug.material_override.roughness = 1.0
	# ---------- the swim-through xylophone (a free-play music toy) ----------
	# bells run in a spaced row down the length of the room (no overlap)
	var bellcols := [Color(1, 0.3, 0.3), Color(1, 0.6, 0.2), Color(1, 0.9, 0.3), Color(0.3, 0.85, 0.4), Color(0.3, 0.6, 1.0), Color(0.5, 0.4, 0.9), Color(0.95, 0.4, 0.8)]
	var bellpitch := [0.8, 0.9, 1.0, 1.2, 1.35, 1.5, 1.8]
	g["bells"] = []
	for bi in range(7):
		var bell := MeshInstance3D.new()
		var bm := BoxMesh.new()
		bm.size = Vector3(2.6, 9.0 - float(bi) * 0.5, 2.6)
		bell.mesh = bm
		var bmat := StandardMaterial3D.new()
		bmat.albedo_color = bellcols[bi]
		bmat.emission_enabled = true
		bmat.emission = bellcols[bi]
		bmat.emission_energy_multiplier = 0.7
		bmat.metallic = 0.4
		bmat.roughness = 0.3
		bell.material_override = bmat
		bell.position = mo + Vector3(0.0, 5.0, -13.5 + float(bi) * 4.5)   # spaced 4.5 along z
		add_child(bell)
		game_nodes.append(bell)
		var bp := AudioStreamPlayer.new()
		bp.stream = load("res://assets/audio/chime.ogg")
		bp.pitch_scale = bellpitch[bi]
		bp.volume_db = -1.0
		bell.add_child(bp)   # parent to the bell so it frees with the room (game_nodes is Array[Node3D])
		(g["bells"] as Array).append({"node": bell, "player": bp, "cool": 0.0, "base_y": bell.position.y, "tw": null})
	# two warm fill lights down the length
	for lz in [-12.0, 10.0]:
		var ml := OmniLight3D.new()
		ml.light_color = Color(0.85, 0.85, 1.0); ml.light_energy = 1.7; ml.omni_range = 28.0
		ml.position = mo + Vector3(0, 22, lz); add_child(ml); game_nodes.append(ml)
	# glowing windows on the far wall
	for wz in [-10.0, 10.0]:
		var win := _l2_box(mo + Vector3(-9.1, 20, wz), Vector3(0.4, 7, 6), Color(0.7, 0.8, 1.0), 0.8)
		win.material_override.emission_energy_multiplier = 1.2
	# sign over the doorway
	var msign := Label3D.new()
	msign.text = "♪ Music Room ♪"
	msign.font_size = 56; msign.pixel_size = 0.028; msign.outline_size = 12
	msign.modulate = Color(0.85, 0.9, 1.0); msign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	msign.position = o + Vector3(-35, 20.0, -16); add_child(msign); game_nodes.append(msign)
	# cool invite glow at the doorway
	var il := OmniLight3D.new()
	il.light_color = Color(0.6, 0.7, 1.0); il.light_energy = 1.6; il.omni_range = 14.0
	il.position = o + Vector3(-34, 7, -16); add_child(il); game_nodes.append(il)

func _build_castle_craft_room(o: Vector3) -> void:
	# Craft room off the RIGHT hall wall, doorway at z -1..+9 (the easel keeps its old z~2 spot, just deeper).
	# Footprint x:35..52.75, z:-4.75..12.75 — inside the dome (far corner r≈54.5 < 60).
	var co: Vector3 = o + Vector3(44, 0, 4)              # room centre
	var wall := Color(0.93, 0.95, 0.9)                   # soft mint plaster
	var cfloor := _l2_box(co + Vector3(0, 0.4, 0), Vector3(18, 1.0, 18), Color(0.82, 0.74, 0.6))
	cfloor.material_override = _up_mat("wood", 0.1, Color(0.95, 0.85, 0.68))   # honey studio boards
	_l2_box(co + Vector3(0, 33.0, 0), Vector3(18, 1.5, 18), Color(0.88, 0.9, 0.86))
	# enclosing walls (the left/hall side is the segmented hall wall already built)
	_iwall(co + Vector3(8.75, 16, 0), Vector3(1.5, 34, 18), wall)        # far wall (x=52.75)
	_iwall(co + Vector3(0, 16, -8.75), Vector3(18, 34, 1.5), wall)       # back wall (z=-4.75)
	_iwall(co + Vector3(0, 16, 8.75), Vector3(18, 34, 1.5), wall)        # front wall (z=12.75)
	# gold doorway frame around the opening in the hall wall
	for dz in [-1.0, 9.0]:
		_l2_box(o + Vector3(35, 8, dz), Vector3(1.2, 16, 1.2), Color(0.85, 0.72, 0.45), 0.15)
	# paint-splat rug by the entrance
	var rug := _l2_box(co + Vector3(-4.0, 0.95, 0.0), Vector3(8, 0.1, 7), Color(0.95, 0.72, 0.35))
	rug.material_override.roughness = 1.0
	# ---------- the easel, against the far wall ----------
	var easel := _l2_box(co + Vector3(6.5, 7.0, 0.0), Vector3(0.6, 11.0, 8.0), Color(0.55, 0.4, 0.26))
	_mg_noop_ref(easel)
	var canvas := _l2_box(co + Vector3(5.9, 9.0, 0.0), Vector3(0.4, 7.0, 6.0), Color(0.97, 0.96, 0.92), 0.1)
	_mg_noop_ref(canvas)
	var craft_fish_icon := Sprite3D.new()
	craft_fish_icon.texture = load("res://assets/mg/fish_line.png")
	craft_fish_icon.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	craft_fish_icon.pixel_size = 0.012
	craft_fish_icon.position = co + Vector3(5.4, 9.0, 0.0)
	add_child(craft_fish_icon); game_nodes.append(craft_fish_icon)
	# paint pots along the back wall for set dressing
	var potcols := [Color(0.92, 0.3, 0.3), Color(1.0, 0.8, 0.25), Color(0.35, 0.75, 0.4), Color(0.35, 0.6, 0.95), Color(0.7, 0.4, 0.9)]
	for pi in range(potcols.size()):
		var pot := _l2_box(co + Vector3(-6.0 + float(pi) * 3.0, 1.6, -7.0), Vector3(1.6, 2.2, 1.6), Color(0.85, 0.82, 0.78))
		_mg_noop_ref(pot)
		var paint := _l2_box(co + Vector3(-6.0 + float(pi) * 3.0, 2.9, -7.0), Vector3(1.3, 0.4, 1.3), potcols[pi], 0.4)
		_mg_noop_ref(paint)
	# sign over the doorway (visible from the hall)
	var csign := Label3D.new()
	csign.text = "\U0001f3a8 Crafting Room"
	csign.font_size = 56; csign.pixel_size = 0.028; csign.outline_size = 12
	csign.modulate = Color(0.95, 0.9, 1.0); csign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	csign.position = o + Vector3(35, 20.0, 4)
	add_child(csign); game_nodes.append(csign)
	# warm invite glow at the doorway + fill light inside
	var il := OmniLight3D.new()
	il.light_color = Color(1.0, 0.9, 0.7); il.light_energy = 1.5; il.omni_range = 14.0
	il.position = o + Vector3(35, 7, 4); add_child(il); game_nodes.append(il)
	var fl := OmniLight3D.new()
	fl.light_color = Color(1.0, 0.95, 0.85); fl.light_energy = 1.8; fl.omni_range = 26.0
	fl.position = co + Vector3(0, 22, 0); add_child(fl); game_nodes.append(fl)
	g["craft_easel"] = co + Vector3(4.5, 7.0, 0.0)

func _build_castle_bedroom(o: Vector3) -> void:
	# Cosy single-bed room reached through the right-wall doorway (x=35, z=-16).
	# Footprint x:35..52.75, z:-24.75..-7.25 — entirely inside the dome (r<60).
	var bo: Vector3 = o + Vector3(44, 0, -16)            # room centre
	var wall := Color(0.96, 0.9, 0.86)                   # warm rosy plaster
	# floor + ceiling (no colliders — handled by the floor clamp / arena_ceil)
	var bfloor := _l2_box(bo + Vector3(0, 0.4, 0), Vector3(18, 1.0, 18), Color(0.78, 0.6, 0.5))
	bfloor.material_override = _up_mat("wood", 0.1, Color(0.92, 0.72, 0.58))   # warm rosy boards
	_l2_box(bo + Vector3(0, 33.0, 0), Vector3(18, 1.5, 18), Color(0.9, 0.84, 0.82))
	# enclosing walls (the left/hall side is the segmented hall wall already built)
	_iwall(bo + Vector3(8.75, 16, 0), Vector3(1.5, 34, 18), wall)        # far wall (x=52.75)
	_iwall(bo + Vector3(0, 16, -8.75), Vector3(18, 34, 1.5), wall)       # back wall (z=-24.75)
	_iwall(bo + Vector3(0, 16, 8.75), Vector3(18, 34, 1.5), wall)        # front wall (z=-7.25)
	# gold doorway frame around the opening in the hall wall
	for dz in [-21.0, -11.0]:
		_l2_box(o + Vector3(35, 8, dz), Vector3(1.2, 16, 1.2), Color(0.85, 0.72, 0.45), 0.15)
	# ---------- the single bed (head against the back wall) ----------
	var bx := 4.0      # bed centre offset toward the far wall
	var bcx: float = bo.x + bx
	var frame := _l2_box(Vector3(bcx, o.y + 2.0, bo.z), Vector3(6, 2.5, 10), Color(0.5, 0.32, 0.2))   # wooden frame
	frame.material_override.roughness = 0.8
	_l2_box(Vector3(bcx, o.y + 3.7, bo.z), Vector3(5, 1.2, 9), Color(0.98, 0.97, 1.0))                # mattress
	_l2_box(Vector3(bcx, o.y + 4.4, bo.z + 1.5), Vector3(5.2, 0.5, 5.5), Color(0.45, 0.62, 0.92))     # folded blanket
	_l2_box(Vector3(bcx, o.y + 4.6, bo.z - 3.4), Vector3(4.2, 0.9, 2.2), Color(1.0, 1.0, 1.0))        # pillow
	var headboard := _l2_box(Vector3(bcx, o.y + 5.5, bo.z - 4.7), Vector3(6, 6, 0.9), Color(0.45, 0.28, 0.17))
	headboard.material_override.roughness = 0.7
	# bed collider: low (player can swim over it) but blocks at floor level
	_wall_solid(Vector3(bcx, o.y + 2.0, bo.z), Vector3(6, 2.5, 10))
	# ---------- bedside table + glowing lamp ----------
	var table := _l2_box(Vector3(bo.x - 4.5, o.y + 1.8, bo.z - 5.5), Vector3(2.4, 3.2, 2.4), Color(0.5, 0.32, 0.2))
	table.material_override.roughness = 0.8
	var lampbulb := MeshInstance3D.new()
	var ls := SphereMesh.new(); ls.radius = 0.7; ls.height = 1.4
	lampbulb.mesh = ls
	var lmat := StandardMaterial3D.new()
	lmat.emission_enabled = true; lmat.emission = Color(1.0, 0.82, 0.5); lmat.emission_energy_multiplier = 3.0
	lampbulb.material_override = lmat
	lampbulb.position = Vector3(bo.x - 4.5, o.y + 4.6, bo.z - 5.5)
	add_child(lampbulb); game_nodes.append(lampbulb)
	var lamp := OmniLight3D.new()
	lamp.light_color = Color(1.0, 0.82, 0.55); lamp.light_energy = 2.0; lamp.omni_range = 18.0
	lamp.position = lampbulb.position; add_child(lamp); game_nodes.append(lamp)
	# soft rug by the doorway
	var rug := _l2_box(bo + Vector3(-4.0, 0.95, 2.0), Vector3(8, 0.1, 7), Color(0.7, 0.3, 0.4))
	rug.material_override.roughness = 1.0
	# ---------- DRESS-UP VANITY: a wardrobe + mirror (swim up to pick your outfit) ----------
	var vpos: Vector3 = bo + Vector3(-3.5, 0, 7.0)        # against the front wall, facing the room
	var wardrobe := _l2_box(vpos + Vector3(0, 7.0, 1.0), Vector3(7, 14, 1.6), Color(0.55, 0.34, 0.22))
	wardrobe.material_override.roughness = 0.8
	var mirror := _l2_box(vpos + Vector3(0, 7.5, 0.1), Vector3(4.5, 9.0, 0.2), Color(0.7, 0.92, 1.0), 0.6)  # glowing mirror glass
	mirror.material_override.metallic = 0.9
	mirror.material_override.roughness = 0.05
	for fx in [-2.6, 2.6]:                                 # gold mirror frame posts
		_l2_box(vpos + Vector3(fx, 7.5, 0.2), Vector3(0.6, 9.5, 0.5), Color(0.95, 0.8, 0.4), 0.2)
	_l2_box(vpos + Vector3(0, 12.4, 0.2), Vector3(5.7, 0.6, 0.5), Color(0.95, 0.8, 0.4), 0.2)   # frame top
	_wall_solid(vpos + Vector3(0, 7.0, 1.0), Vector3(7, 14, 1.6))   # the wardrobe is solid
	var vsign := Label3D.new()
	vsign.text = "\U0001f457 Dress Up!"
	vsign.font_size = 48; vsign.pixel_size = 0.028; vsign.outline_size = 12
	vsign.modulate = Color(1.0, 0.8, 0.95); vsign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	vsign.position = vpos + Vector3(0, 13.6, 0); add_child(vsign); game_nodes.append(vsign)
	var vl := OmniLight3D.new()
	vl.light_color = Color(1.0, 0.85, 0.95); vl.light_energy = 1.6; vl.omni_range = 14.0
	vl.position = vpos + Vector3(0, 8, -2); add_child(vl); game_nodes.append(vl)
	g["wardrobe"] = vpos + Vector3(0, 6, -2)
	# fill light so the room reads warm
	var bl := OmniLight3D.new()
	bl.light_color = Color(1.0, 0.88, 0.78); bl.light_energy = 1.8; bl.omni_range = 30.0
	bl.position = bo + Vector3(0, 22, 0); add_child(bl); game_nodes.append(bl)
	# little glowing window on the far wall for ambiance
	var win := _l2_box(bo + Vector3(8.1, 20, 0), Vector3(0.4, 7, 6), Color(0.6, 0.85, 1.0), 0.8)
	win.material_override.emission_energy_multiplier = 1.2
	# label over the doorway
	var blab := Label3D.new()
	blab.text = "\U0001f6cf️ Bedroom"
	blab.font_size = 56; blab.pixel_size = 0.03; blab.outline_size = 12
	blab.modulate = Color(1.0, 0.9, 0.85)
	blab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	blab.position = o + Vector3(35, 20.0, -16)
	add_child(blab); game_nodes.append(blab)
	# warm invite glow at the doorway
	var il := OmniLight3D.new()
	il.light_color = Color(1.0, 0.8, 0.6); il.light_energy = 1.6; il.omni_range = 14.0
	il.position = o + Vector3(34, 7, -16); add_child(il); game_nodes.append(il)

func _seg_box(p0: Vector3, p1: Vector3, c: Vector3, h: Vector3) -> bool:
	# does the segment p0->p1 pass through the axis-aligned box (center c, half-extents h)?
	var d: Vector3 = p1 - p0
	var tmin := 0.0
	var tmax := 1.0
	for ax in range(3):
		var dd: float = d[ax]
		var lo: float = c[ax] - h[ax]
		var hi: float = c[ax] + h[ax]
		if absf(dd) < 0.00001:
			if p0[ax] < lo or p0[ax] > hi:
				return false
		else:
			var t1: float = (lo - p0[ax]) / dd
			var t2: float = (hi - p0[ax]) / dd
			if t1 > t2:
				var tmp := t1; t1 = t2; t2 = tmp
			tmin = maxf(tmin, t1)
			tmax = minf(tmax, t2)
			if tmin > tmax:
				return false
	return true

func _tick_wall_fade(delta: float) -> void:
	# cut away any interior wall that sits between the chase camera and Roshan
	if fade_walls.is_empty() or player == null or player.cam == null or not player.cam.is_inside_tree():
		return
	var cam_p: Vector3 = player.cam.global_position
	var pl_p: Vector3 = player.position + Vector3(0, 1.2, 0)
	var margin := Vector3(1.0, 1.0, 1.0)
	for w in fade_walls:
		if not is_instance_valid(w["node"]):   # check BEFORE the typed assign below
			continue
		var node: MeshInstance3D = w["node"]
		if not (node.material_override is StandardMaterial3D):
			continue
		var base_a: float = w["base_a"]
		var occ: bool = _seg_box(cam_p, pl_p, w["c"], (w["h"] as Vector3) + margin)
		var target: float = (base_a * 0.16) if occ else base_a
		var a: float = lerpf(float(w["a"]), target, 1.0 - pow(0.0015, delta))
		w["a"] = a
		var mat: StandardMaterial3D = node.material_override
		if a < base_a - 0.02:
			mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			mat.albedo_color.a = a
		else:
			mat.transparency = BaseMaterial3D.TRANSPARENCY_DISABLED
			mat.albedo_color.a = base_a

func _tick_castle_hall(delta: float, ppos: Vector3) -> void:
	if wardrobe_layer != null:
		return   # dressing up — pause all hall triggers
	hud_game.text = "Swim up the stairs to Princess Huluu and the Crown Star!"
	# leave the castle from the entrance
	if g.has("hall_exit") and float(g["t"]) > 2.5:
		var hx: Vector3 = g["hall_exit"]
		if hx.distance_to(ppos) > 14.0:
			g["hall_exit_armed"] = true
		if bool(g.get("hall_exit_armed", false)) and hx.distance_to(ppos) < 6.0:
			_return_to_courtyard()
			return
	# crafting studio: swim up to the easel to color a fish
	if g.has("craft_easel") and craft_layer == null and mg_cool <= 0.0 and mg_kind == "":
		var ce: Vector3 = g["craft_easel"]
		if ce.distance_to(ppos) < 7.0:
			_open_craft_studio()
			return
	# dress-up vanity: swim up to the bedroom wardrobe to pick your outfit
	if g.has("wardrobe") and wardrobe_layer == null and craft_layer == null and mg_cool <= 0.0 and mg_kind == "":
		var wp: Vector3 = g["wardrobe"]
		if wp.distance_to(ppos) < 7.0:
			_open_wardrobe()
			return
	# music room: swim near a bell to play its note. Short cooldown so rapid
	# passes re-trigger almost instantly; the prior bob tween is killed and the
	# bell reset to base each strike so overlapping hits stay snappy, not jittery.
	for bd in g.get("bells", []):
		bd["cool"] = maxf(0.0, float(bd["cool"]) - delta)
		var bn: Node3D = bd["node"]
		if not is_instance_valid(bn):
			continue
		if bn.position.distance_to(ppos) < 5.0 and float(bd["cool"]) <= 0.0:
			bd["cool"] = 0.12
			(bd["player"] as AudioStreamPlayer).play()
			var base_y: float = float(bd.get("base_y", 5.0))
			if bd.get("tw") != null and (bd["tw"] as Tween).is_valid():
				(bd["tw"] as Tween).kill()
			bn.position.y = base_y
			var bbtw: Tween = bn.create_tween()
			bbtw.tween_property(bn, "position:y", base_y - 1.6, 0.06)
			bbtw.tween_property(bn, "position:y", base_y, 0.16)
			bd["tw"] = bbtw
			_sparkle_burst(bn.position + Vector3(0, 4, 0), (bn.material_override as StandardMaterial3D).albedo_color)
	# secret easter-egg chest behind the throne -> ONE consistent bonus game.
	# Fires once when you reach it; will not fire again until you swim away and come back
	# (so it never spins randomly through games while you linger nearby).
	if g.has("secret_door") and mg_cool <= 0.0 and mg_kind == "":
		var sd: Vector3 = g["secret_door"]
		var near: bool = sd.distance_to(ppos) < 14.0
		if not near:
			g["secret_armed"] = true
		elif bool(g.get("secret_armed", true)):
			g["secret_armed"] = false
			_play_hug_cutscene()
			return
	mg_cool = maxf(0.0, mg_cool - delta)
	# Princess Huluu greets Roshan as she gets near the throne
	var hpos: Vector3 = CASTLE_POS + Vector3(0, 21.0, -27.0)
	if not bool(g.get("huluu_greeted", false)) and hpos.distance_to(ppos) < 26.0:
		g["huluu_greeted"] = true
		show_msg("Princess Huluu", "Thank you, Mermaid Roshan, you did a great job! This is now your castle!", "win")
	var crown: Label3D = l2_stars[0]["node"]
	crown.rotate_y(delta * 1.4)
	crown.position.y += sin(float(g["t"]) * 2.0) * 0.02
	# GENTLE STAIR HELPER (not a black hole): only a soft updraft when the player is in
	# FRONT of the throne and below the crown. No far-reaching horizontal pull, so the
	# back room behind the throne stays reachable. Finishing requires actually touching the crown.
	var d: float = crown.position.distance_to(ppos)
	var in_front: bool = ppos.z > crown.position.z + 3.0
	if in_front and d < 16.0 and ppos.y < crown.position.y - 1.0:
		player.position = player.position.lerp(crown.position, minf(0.16, delta * 0.5))
		player.vel.y = maxf(player.vel.y, 0.0)
	if d < 5.0:
		_finish_level2()

func _l2_start_slide() -> void:
	# the rainbow slide is the 3D play place (same world as Harper's game), returning to the courtyard when done
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	l2_stars = []
	var fr := {"fname": "Rainbow Slide", "won": true, "game": "race", "cool": 0.0}
	rainbow_slide_mode = true
	_start_game(fr)
	rainbow_slide_mode = false
	# a brighter rainbow-dream sky in place of the sunset
	if arena_env != null:
		arena_env.background_color = Color(0.62, 0.80, 1.0)
		arena_env.ambient_light_color = Color(1.0, 0.95, 1.0)
		arena_env.ambient_light_energy = 1.2
	# flashing colored disco lights ringing the play place (this is the RAINBOW slide!)
	var rbc := [Color(1, 0.2, 0.2), Color(1, 0.6, 0.1), Color(1, 0.9, 0.2), Color(0.2, 0.9, 0.3), Color(0.2, 0.5, 1.0), Color(0.6, 0.3, 0.9)]
	for li in range(8):
		var fl := OmniLight3D.new()
		fl.light_energy = 4.0
		fl.omni_range = 34.0
		var ang: float = float(li) / 8.0 * TAU
		fl.position = ARENA_POS + Vector3(cos(ang) * 17.0, 5.0 + float(li % 4) * 8.0, sin(ang) * 17.0)
		fl.light_color = rbc[li % rbc.size()]
		add_child(fl)
		game_nodes.append(fl)
		var tw := fl.create_tween().set_loops()
		for ci in range(rbc.size()):
			tw.tween_property(fl, "light_color", rbc[(li + ci + 1) % rbc.size()], 0.3)
	# a couple of rainbow arches over the climb
	for ai in range(2):
		var arc := MeshInstance3D.new()
		var at := TorusMesh.new(); at.inner_radius = 16.0 + float(ai) * 6.0; at.outer_radius = 18.0 + float(ai) * 6.0
		at.rings = 32; at.ring_segments = 16
		arc.mesh = at
		var ash := Shader.new()
		ash.code = "shader_type spatial;\nrender_mode cull_disabled, unshaded;\nvoid fragment(){ float b=UV.y; vec3 c; if(b<0.16)c=vec3(0.9,0.2,0.3);else if(b<0.33)c=vec3(1.0,0.6,0.2);else if(b<0.5)c=vec3(1.0,0.9,0.3);else if(b<0.66)c=vec3(0.3,0.8,0.4);else if(b<0.83)c=vec3(0.3,0.6,1.0);else c=vec3(0.6,0.4,0.9); ALBEDO=c; EMISSION=c*0.5; }"
		var am := ShaderMaterial.new(); am.shader = ash
		arc.material_override = am
		arc.position = ARENA_POS + Vector3(0, 24.0 + float(ai) * 6.0, 0)
		arc.rotation_degrees = Vector3(0, 0, 90)
		add_child(arc)
		game_nodes.append(arc)

func _return_to_courtyard() -> void:
	# step OUT of the castle into its own courtyard (Sky Lagoon) — not all the way back to the ocean
	player.cam_back = 16.0
	player.cam_high = 6.5
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	_enter_level2(true)

func _play_hug_cutscene() -> void:
	var cl := CanvasLayer.new()
	cl.layer = 20
	add_child(cl)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	cl.add_child(root)
	var vp: Vector2 = get_viewport().get_visible_rect().size
	var bg := ColorRect.new()
	bg.color = Color(0.06, 0.03, 0.14, 0.0)
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.add_child(bg)
	var tb := create_tween()
	tb.tween_property(bg, "color", Color(0.06, 0.03, 0.14, 0.5), 0.4)
	# Daddy slides in from the left
	var daddy := TextureRect.new()
	daddy.texture = load("res://assets/characters/friends/daddy.png")
	daddy.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	daddy.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	daddy.size = Vector2(vp.y * 0.62, vp.y * 0.9)
	daddy.position = Vector2(-daddy.size.x, vp.y * 0.1)
	root.add_child(daddy)
	# Roshan slides in from the right
	var rosh := TextureRect.new()
	rosh.texture = load("res://assets/characters/roshan_sprite.png")
	rosh.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	rosh.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	rosh.size = Vector2(vp.y * 0.5, vp.y * 0.7)
	rosh.position = Vector2(vp.x, vp.y * 0.28)
	root.add_child(rosh)
	var lbl := Label.new()
	lbl.text = "\u2764  I love you, Roshan!  \u2764"
	lbl.add_theme_font_size_override("font_size", int(vp.y * 0.07))
	lbl.add_theme_color_override("font_color", Color(1, 1, 1))
	lbl.add_theme_color_override("font_outline_color", Color(0.6, 0.1, 0.3))
	lbl.add_theme_constant_override("outline_size", 12)
	lbl.position = Vector2(vp.x * 0.22, vp.y * 0.06)
	lbl.modulate.a = 0.0
	root.add_child(lbl)
	var dp := AudioStreamPlayer.new()
	dp.stream = load("res://assets/audio/voices/daddy1.ogg")
	dp.volume_db = 4.0
	root.add_child(dp)
	dp.play()
	var tw := create_tween().set_parallel(true)
	tw.tween_property(daddy, "position:x", vp.x * 0.5 - daddy.size.x * 0.64, 0.6).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(rosh, "position:x", vp.x * 0.5 - rosh.size.x * 0.36, 0.6).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(lbl, "modulate:a", 1.0, 0.5).set_delay(0.5)
	for hi in range(16):
		var h := Label.new()
		h.text = "\u2764"
		h.add_theme_font_size_override("font_size", int(vp.y * 0.05 * (0.6 + randf())))
		h.add_theme_color_override("font_color", Color.from_hsv(0.94 + randf() * 0.12, 0.55, 1.0))
		h.position = Vector2(vp.x * 0.5 + randf() * vp.x * 0.34 - vp.x * 0.17, vp.y * 0.62)
		root.add_child(h)
		var ht := create_tween().set_parallel(true)
		ht.tween_property(h, "position:y", vp.y * 0.08, 1.7 + randf()).set_delay(0.5 + randf() * 0.6)
		ht.tween_property(h, "modulate:a", 0.0, 1.6).set_delay(0.9)
	get_tree().create_timer(2.7).timeout.connect(func():
		var fo := root.create_tween()
		fo.tween_property(root, "modulate:a", 0.0, 0.45)
		fo.finished.connect(cl.queue_free))


func _mg_noop_ref(_n: Node) -> void:
	pass

func _layer_fx(nd: Object, role: String, col: Color, rb: bool, kind: String) -> void:
	# kill any prior fx tween on this layer
	var old: Variant = nd.get_meta("fxtw") if nd.has_meta("fxtw") else null
	if old is Tween and (old as Tween).is_valid():
		(old as Tween).kill()
	var base_a: float = 1.0
	if role == "accent":
		base_a = 1.0 if kind == "fish" else 0.5
	if rb:
		# RAINBOW: loop the layer through the hue wheel
		var tw: Tween = (nd as Node).create_tween().set_loops()
		for hi in range(6):
			var hc := Color.from_hsv(float(hi) / 6.0, 0.75, 1.0, base_a)
			tw.tween_property(nd, "modulate", hc, 0.4)
		nd.set_meta("fxtw", tw)
	elif role == "accent":
		# GLITTER: Color 2 shimmers between the color and a bright sparkle of itself
		var c0 := Color(col.r, col.g, col.b, base_a)
		var c1 := Color(minf(col.r * 1.6 + 0.15, 1.0), minf(col.g * 1.6 + 0.15, 1.0), minf(col.b * 1.6 + 0.15, 1.0), minf(base_a + 0.18, 1.0))
		nd.set("modulate", c0)
		var tw2: Tween = (nd as Node).create_tween().set_loops()
		tw2.tween_property(nd, "modulate", c1, 0.35).set_trans(Tween.TRANS_SINE)
		tw2.tween_property(nd, "modulate", c0, 0.45).set_trans(Tween.TRANS_SINE)
		nd.set_meta("fxtw", tw2)
	else:
		nd.set("modulate", Color(col.r, col.g, col.b, base_a))

func _make_creature_node(kind: String, body: Color, accent: Color, body_rb: bool = false, acc_rb: bool = false) -> Node3D:
	var ln: Array = CREATURE_LAYERS.get(kind, CREATURE_LAYERS["fish"])
	var root := Node3D.new()
	var lb := Sprite3D.new()
	lb.texture = load("res://assets/mg/" + String(ln[1]) + ".png")
	lb.billboard = BaseMaterial3D.BILLBOARD_ENABLED; lb.pixel_size = 0.02; lb.render_priority = 0
	root.add_child(lb)
	_layer_fx(lb, "body", body, body_rb, kind)
	var la := Sprite3D.new()
	la.texture = load("res://assets/mg/" + String(ln[0]) + ".png")
	la.billboard = BaseMaterial3D.BILLBOARD_ENABLED; la.pixel_size = 0.02; la.render_priority = 1
	root.add_child(la)
	_layer_fx(la, "accent", accent, acc_rb, kind)
	var ll := Sprite3D.new()
	ll.texture = load("res://assets/mg/" + String(ln[2]) + ".png")
	ll.billboard = BaseMaterial3D.BILLBOARD_ENABLED; ll.pixel_size = 0.02; ll.render_priority = 2
	root.add_child(ll)
	return root

func _craft_build_preview() -> void:
	if craft_fishbox == null:
		return
	for c in craft_fishbox.get_children():
		c.queue_free()
	var ln: Array = CREATURE_LAYERS.get(craft_kind, CREATURE_LAYERS["fish"])
	var acca: float = 1.0 if craft_kind == "fish" else 0.5
	var order := [String(ln[1]), String(ln[0]), String(ln[2])]
	var roles := ["body", "accent", "line"]
	var cols := [craft_body, Color(craft_fins.r, craft_fins.g, craft_fins.b, acca), Color(1, 1, 1)]
	var rbs := [craft_body_rb, craft_fins_rb, false]
	for i in range(3):
		var tr := TextureRect.new(); tr.texture = load("res://assets/mg/" + order[i] + ".png")
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE; tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		tr.size = craft_fishbox.size; tr.modulate = cols[i]; tr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		tr.set_meta("role", roles[i]); craft_fishbox.add_child(tr)
		if roles[i] != "line":
			_layer_fx(tr, roles[i], cols[i], rbs[i], craft_kind)

func _open_craft_studio() -> void:
	if craft_layer != null:
		return
	craft_kind = "fish"
	craft_body = Color(0.4, 0.7, 1.0)
	craft_fins = Color(1.0, 0.6, 0.2)
	craft_body_rb = false
	craft_fins_rb = false
	craft_layer = CanvasLayer.new(); craft_layer.layer = 18; add_child(craft_layer)
	var root := Control.new(); root.set_anchors_preset(Control.PRESET_FULL_RECT); craft_layer.add_child(root)
	var vp: Vector2 = get_viewport().get_visible_rect().size
	var bg := ColorRect.new(); bg.color = Color(0.10, 0.13, 0.22, 0.95); bg.set_anchors_preset(Control.PRESET_FULL_RECT); root.add_child(bg)
	var stage := Control.new(); stage.size = Vector2(1280, 720)
	var sc: float = minf(vp.x / 1280.0, vp.y / 720.0)
	stage.scale = Vector2(sc, sc); stage.position = (vp - Vector2(1280, 720) * sc) * 0.5
	root.add_child(stage)
	var title := Label.new(); title.text = "Color your friend!"
	title.add_theme_font_size_override("font_size", 52)
	title.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); title.add_theme_constant_override("outline_size", 10)
	title.position = Vector2(60, 16); stage.add_child(title)
	# creature-type buttons
	var kinds := [["fish", "Fishy"], ["cat", "Kitty"], ["bird", "Birdie"]]
	for ki in range(kinds.size()):
		var kb := Button.new(); kb.text = String(kinds[ki][1]); kb.add_theme_font_size_override("font_size", 36)
		kb.position = Vector2(760.0 + float(ki) * 165.0, 14.0); kb.custom_minimum_size = Vector2(155, 64)
		var ksb := StyleBoxFlat.new(); ksb.bg_color = Color(0.4, 0.45, 0.7); ksb.set_corner_radius_all(18)
		kb.add_theme_stylebox_override("normal", ksb); kb.add_theme_stylebox_override("hover", ksb); kb.add_theme_stylebox_override("pressed", ksb)
		var kk: String = String(kinds[ki][0])
		kb.pressed.connect(func(): craft_kind = kk; _craft_build_preview())
		stage.add_child(kb)
	craft_fishbox = Control.new(); craft_fishbox.size = Vector2(400, 400); craft_fishbox.position = Vector2(440, 72); stage.add_child(craft_fishbox)
	_craft_build_preview()
	var pal := [Color(0.92, 0.26, 0.3), Color(1, 0.6, 0.2), Color(1, 0.85, 0.25), Color(0.35, 0.8, 0.4), Color(0.3, 0.8, 0.9), Color(0.3, 0.55, 1.0), Color(0.6, 0.4, 0.9), Color(0.95, 0.5, 0.8)]
	for row in range(2):
		var part := "body" if row == 0 else "accent"
		for ci in range(pal.size()):
			var sw := Button.new(); sw.custom_minimum_size = Vector2(90, 90); sw.size = Vector2(90, 90)
			sw.position = Vector2(300.0 + float(ci) * 100.0, 492.0 + float(row) * 108.0)
			var sb := StyleBoxFlat.new(); sb.bg_color = pal[ci]; sb.set_corner_radius_all(20); sb.set_border_width_all(4); sb.border_color = Color(1, 1, 1, 0.7)
			sw.add_theme_stylebox_override("normal", sb); sw.add_theme_stylebox_override("hover", sb); sw.add_theme_stylebox_override("pressed", sb)
			var col: Color = pal[ci]; var pp: String = part
			sw.pressed.connect(func(): _craft_set(pp, col))
			stage.add_child(sw)
		# 9th swatch: RAINBOW (the whole layer cycles through every color)
		var rbw := Button.new(); rbw.custom_minimum_size = Vector2(90, 90); rbw.size = Vector2(90, 90)
		rbw.position = Vector2(300.0 + float(pal.size()) * 100.0 - 1400.0 * 0.0, 492.0 + float(row) * 108.0)
		rbw.position.x = 300.0 - 100.0   # place it BEFORE the solid colors so it fits the row
		rbw.flat = true
		var rimg := TextureRect.new(); rimg.texture = load("res://assets/mg/rainbow_swatch.png")
		rimg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE; rimg.stretch_mode = TextureRect.STRETCH_SCALE
		rimg.set_anchors_preset(Control.PRESET_FULL_RECT); rimg.mouse_filter = Control.MOUSE_FILTER_IGNORE
		rbw.add_child(rimg)
		var pp2: String = part
		rbw.pressed.connect(func(): _craft_set(pp2, Color(1, 1, 1), true))
		stage.add_child(rbw)
	var done := Button.new(); done.text = "  Done!  "; done.add_theme_font_size_override("font_size", 46)
	done.position = Vector2(1050, 330); done.custom_minimum_size = Vector2(190, 130)
	var dsb := StyleBoxFlat.new(); dsb.bg_color = Color(0.3, 0.8, 0.4); dsb.set_corner_radius_all(30)
	done.add_theme_stylebox_override("normal", dsb); done.add_theme_stylebox_override("hover", dsb); done.add_theme_stylebox_override("pressed", dsb)
	done.pressed.connect(_craft_done); stage.add_child(done)

func _craft_set(part: String, col: Color, rb: bool = false) -> void:
	if part == "body":
		craft_body = col
		craft_body_rb = rb
	else:
		craft_fins = col
		craft_fins_rb = rb
	if craft_fishbox != null:
		for c in craft_fishbox.get_children():
			if c is TextureRect:
				var role: String = (c as TextureRect).get_meta("role", "")
				if part == role:
					_layer_fx(c, role, col, rb, craft_kind)

func _craft_done() -> void:
	if craft_layer == null:
		return
	var fishy: bool = craft_kind == "fish"
	var msgtxt: String
	if fishy:
		custom_fish.append([craft_body.r, craft_body.g, craft_body.b, craft_fins.r, craft_fins.g, craft_fins.b, 1 if craft_body_rb else 0, 1 if craft_fins_rb else 0])
		var newfish := _make_creature_node("fish", craft_body, craft_fins, craft_body_rb, craft_fins_rb)
		add_child(newfish); flora_nodes.append(newfish)
		aquatic_movers.append({"node": newfish, "rad": 30.0 + randf() * 130.0, "spd": 0.10 + randf() * 0.12, "y": 8.0 + randf() * 26.0, "ph": randf() * TAU})
		msgtxt = "Swim away, little fish! Find me in the ocean!"
	else:
		custom_friends.append([craft_kind, craft_body.r, craft_body.g, craft_body.b, craft_fins.r, craft_fins.g, craft_fins.b, 1 if craft_body_rb else 0, 1 if craft_fins_rb else 0])
		msgtxt = "Off to the courtyard! Find me when you visit!"
	_write_save()
	if chime != null:
		chime.pitch_scale = 1.3; chime.play()
	if craft_fishbox != null:
		var box := craft_fishbox
		var msg := Label.new(); msg.text = msgtxt
		msg.add_theme_font_size_override("font_size", 46); msg.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); msg.add_theme_constant_override("outline_size", 10)
		msg.position = Vector2(180, 18); box.get_parent().add_child(msg)
		box.pivot_offset = box.size * 0.5
		var tw := box.create_tween()
		tw.tween_property(box, "scale", Vector2(1.25, 1.25), 0.4).set_trans(Tween.TRANS_BACK)
		tw.tween_interval(0.5)
		tw.parallel().tween_property(box, "position:x", 1500.0, 1.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		tw.parallel().tween_property(box, "scale", Vector2(0.5, 0.5), 1.0)
	get_tree().create_timer(2.6).timeout.connect(_close_craft)

func _close_craft() -> void:
	if craft_layer != null and is_instance_valid(craft_layer):
		craft_layer.queue_free()
	craft_layer = null
	craft_fishbox = null
	mg_cool = 10.0

# ---------------- DRESS-UP WARDROBE (full-skin picker) ----------------
func _open_wardrobe() -> void:
	if wardrobe_layer != null:
		return
	wardrobe_layer = CanvasLayer.new(); wardrobe_layer.layer = 18; add_child(wardrobe_layer)
	var root := Control.new(); root.set_anchors_preset(Control.PRESET_FULL_RECT); wardrobe_layer.add_child(root)
	var vp: Vector2 = get_viewport().get_visible_rect().size
	var bg := ColorRect.new(); bg.color = Color(0.13, 0.09, 0.18, 0.96); bg.set_anchors_preset(Control.PRESET_FULL_RECT); root.add_child(bg)
	var stage := Control.new(); stage.size = Vector2(1280, 720)
	var sc: float = minf(vp.x / 1280.0, vp.y / 720.0)
	stage.scale = Vector2(sc, sc); stage.position = (vp - Vector2(1280, 720) * sc) * 0.5
	root.add_child(stage)
	var title := Label.new(); title.text = "Pick your look!"
	title.add_theme_font_size_override("font_size", 56)
	title.add_theme_color_override("font_color", Color(1.0, 0.92, 0.98))
	title.add_theme_color_override("font_outline_color", Color(0.08, 0.05, 0.15)); title.add_theme_constant_override("outline_size", 10)
	title.position = Vector2(60, 18); stage.add_child(title)
	# ---- preview of the selected skin ----
	var frame := Panel.new(); frame.position = Vector2(110, 110); frame.size = Vector2(470, 560)
	var fsb := StyleBoxFlat.new(); fsb.bg_color = Color(0.22, 0.26, 0.42); fsb.set_corner_radius_all(28)
	fsb.set_border_width_all(8); fsb.border_color = Color(0.95, 0.8, 0.45)
	frame.add_theme_stylebox_override("panel", fsb); stage.add_child(frame)
	var preview := TextureRect.new()
	preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	preview.position = Vector2(125, 125); preview.size = Vector2(440, 530)
	stage.add_child(preview)
	wd["preview"] = preview
	# ---- one button per skin (mutually exclusive) ----
	wd["btns"] = []
	for si in range(SKINS.size()):
		var entry: Dictionary = SKINS[si]
		var id: String = String(entry["id"])
		var b := Button.new(); b.add_theme_font_size_override("font_size", 40)
		b.position = Vector2(640, 130.0 + float(si) * 110.0); b.custom_minimum_size = Vector2(450, 92)
		var sb := StyleBoxFlat.new(); sb.set_corner_radius_all(20)
		b.add_theme_stylebox_override("normal", sb); b.add_theme_stylebox_override("hover", sb); b.add_theme_stylebox_override("pressed", sb)
		b.pressed.connect(func(): _wardrobe_pick(id))
		stage.add_child(b)
		(wd["btns"] as Array).append({"btn": b, "box": sb, "id": id})
	# ---- Done ----
	var done := Button.new(); done.text = "  Done!  "; done.add_theme_font_size_override("font_size", 46)
	done.position = Vector2(740, 560); done.custom_minimum_size = Vector2(220, 120)
	var dsb := StyleBoxFlat.new(); dsb.bg_color = Color(0.3, 0.8, 0.45); dsb.set_corner_radius_all(30)
	done.add_theme_stylebox_override("normal", dsb); done.add_theme_stylebox_override("hover", dsb); done.add_theme_stylebox_override("pressed", dsb)
	done.pressed.connect(_wardrobe_done); stage.add_child(done)
	_wardrobe_refresh()

func _wardrobe_refresh() -> void:
	if wardrobe_layer == null:
		return
	if wd.has("preview"):
		(wd["preview"] as TextureRect).texture = load(String(_skin_def(skin_id)["preview"]))
	for entry in wd.get("btns", []):
		var sel: bool = String(entry["id"]) == skin_id
		var box: StyleBoxFlat = entry["box"]
		box.bg_color = Color(0.3, 0.75, 0.42) if sel else Color(0.4, 0.42, 0.6)
		box.set_border_width_all(6 if sel else 0)
		box.border_color = Color(0.2, 1.0, 0.4)
		(entry["btn"] as Button).text = ("✔ " if sel else "    ") + String(_skin_def(String(entry["id"]))["label"])

func _wardrobe_pick(id: String) -> void:
	skin_id = id
	_apply_skin()
	_wardrobe_refresh()
	if chime != null:
		chime.pitch_scale = 1.3; chime.play()

func _wardrobe_done() -> void:
	_write_save()
	if voice != null:
		voice.pitch_scale = 1.15; voice.play()
	_close_wardrobe()

func _close_wardrobe() -> void:
	if wardrobe_layer != null and is_instance_valid(wardrobe_layer):
		wardrobe_layer.queue_free()
	wardrobe_layer = null
	wd = {}
	mg_cool = 8.0

func _exit_level2() -> void:
	player.cam_back = 16.0
	player.cam_high = 6.5
	game = ""
	g = {}
	hud_game.text = ""
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	arena_solids.clear()
	fade_walls.clear()
	we_node.environment = world_env
	arena_center = ARENA_POS
	arena_dome = 48.0
	arena_ceil = 42.0
	portal_cool = 8.0
	portal_armed = false
	if portal_node != null and is_instance_valid(portal_node):
		player.position = portal_node.position + Vector3(22, -6, 22)
	else:
		player.position = return_pos
	player.vel = Vector3.ZERO
	_play_music("world")
	show_msg("Roshan", "Back to the ocean! Wheee!")

func _finish_level2() -> void:
	_do_finish_level2()

func _do_finish_level2() -> void:
	level2_finishing = false
	for i in range(10):
		_sparkle_burst(player.position + Vector3(randf() * 12 - 6, randf() * 8, randf() * 12 - 6), Color.from_hsv(randf(), 0.6, 1.0))
	level2_done_once = true
	_write_save()
	if voice != null:
		voice.pitch_scale = 1.15
		voice.play()
	game = ""
	g = {}
	hud_game.text = ""
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	arena_solids.clear()
	fade_walls.clear()
	we_node.environment = world_env
	arena_center = ARENA_POS
	arena_dome = 48.0
	arena_ceil = 42.0
	portal_cool = 6.0
	portal_armed = false
	# surface near the portal but clearly off it, facing away
	if portal_node != null and is_instance_valid(portal_node):
		player.position = portal_node.position + Vector3(22, -4, 22)
	else:
		player.position = return_pos
	player.vel = Vector3.ZERO
	_play_music("world")
	show_msg("Princess Huluu", "You made it to my Pearl Castle, Roshan! You are the Queen of the Reef now!", "win")

func _beans_go() -> void:
	beans_t = 12.0
	speed_mult = 2.0
	fart_t = 0.7
	prev_track = cur_track if cur_track != "banjo" else "world"
	_play_music("banjo")
	_say("roshan", "beans")
	show_msg("Roshan", "Yummy, beans! ...toot!")
	_beans_bubbles()

func _beans_bubbles() -> void:
	if player == null:
		return
	var bp := CPUParticles3D.new()
	bp.one_shot = false
	bp.emitting = true
	bp.amount = 40
	bp.lifetime = 1.6
	bp.local_coords = false
	bp.direction = Vector3(0, 1, -1)
	bp.spread = 60.0
	bp.gravity = Vector3(0, 5.0, 0)
	bp.initial_velocity_min = 2.0
	bp.initial_velocity_max = 6.0
	bp.scale_amount_min = 0.15
	bp.scale_amount_max = 0.5
	var sm := SphereMesh.new()
	sm.radius = 0.5
	sm.height = 1.0
	bp.mesh = sm
	var bm := StandardMaterial3D.new()
	bm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	bm.albedo_color = Color(0.8, 0.95, 1.0, 0.4)
	bm.emission_enabled = true
	bm.emission = Color(0.6, 0.85, 1.0)
	bm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	bp.material_override = bm
	bp.position = Vector3(0, -0.5, -0.5)
	player.add_child(bp)
	g_beans_bubbles = bp

var g_beans_bubbles: CPUParticles3D
func _tick_beans(delta: float) -> void:
	if beans_t < 0.0:
		return
	# keep banjo playing through any arena transition while beans are active
	if cur_track != "banjo":
		_play_music("banjo")
	beans_t -= delta
	if beans_t <= 0.0:
		beans_t = -1.0
		speed_mult = 1.0
		show_msg("", "Phew! The beans wore off.")
		if g_beans_bubbles != null and is_instance_valid(g_beans_bubbles):
			g_beans_bubbles.queue_free()
		g_beans_bubbles = null
		if cur_track == "banjo":
			_play_music(prev_track if prev_track != "" else "world")

func _build_guide() -> void:
	# no guide character; wayfinding = beacon pillars + a silent helping current
	guide_fish = null

func _tick_guide(delta: float) -> void:
	if player == null:
		return
	if game != "" or finale_t >= 0.0:
		return
	var target := Vector3.ZERO
	var best := 1.0e9
	var have := false
	for f in friends:
		if not bool(f["won"]):
			var d: float = (f["node"] as Sprite3D).position.distance_to(player.position)
			if d < best:
				best = d
				target = (f["node"] as Sprite3D).position
				have = true
	if not have:
		for p in pearls:
			var d2: float = p.position.distance_to(player.position)
			if d2 < best:
				best = d2
				target = p.position
				have = true
	if not have or best <= 16.0:
		return
	var dir2: Vector3 = (target - player.position).normalized()
	# gentle helping current: if the child is swimming roughly toward the goal, carry them
	var pv: Vector3 = player.vel
	if best > 25.0 and pv.length() > 4.0 and pv.normalized().dot(dir2) > 0.45:
		player.position += dir2 * 5.5 * delta

func _sparkle_burst(pos: Vector3, col: Color) -> void:
	var cp := CPUParticles3D.new()
	cp.one_shot = true
	cp.emitting = true
	cp.amount = 36
	cp.lifetime = 1.1
	cp.explosiveness = 1.0
	cp.direction = Vector3.UP
	cp.spread = 180.0
	cp.initial_velocity_min = 3.0
	cp.initial_velocity_max = 7.5
	cp.gravity = Vector3(0, -1.2, 0)
	cp.scale_amount_min = 0.10
	cp.scale_amount_max = 0.26
	var bm := BoxMesh.new()
	bm.size = Vector3(0.3, 0.3, 0.3)
	cp.mesh = bm
	var pm := StandardMaterial3D.new()
	pm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	pm.albedo_color = col
	cp.material_override = pm
	cp.position = pos
	add_child(cp)
	var tw := create_tween()
	tw.tween_interval(1.6)
	tw.tween_callback(cp.queue_free)

func _begin_finale() -> void:
	finale_done = true
	finale_t = 0.0
	_write_save()
	_play_music("finale")
	show_msg("Everyone", "Roshan did it! ALL the friends cheer! Hooray!")
	for i in range(friends.size()):
		var src: Sprite3D = friends[i]["node"]
		var cl3 := Sprite3D.new()
		cl3.texture = src.texture
		cl3.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		cl3.pixel_size = 0.016
		cl3.position = player.position
		add_child(cl3)
		finale_nodes.append(cl3)

func _tick_finale(delta: float) -> void:
	if finale_t < 0.0:
		return
	finale_t += delta
	for i in range(finale_nodes.size()):
		var n3: Sprite3D = finale_nodes[i]
		if not is_instance_valid(n3):
			continue
		var aa: float = finale_t * 0.55 + float(i) / 5.0 * TAU
		var goal: Vector3 = player.position + Vector3(cos(aa) * 7.0, 1.6 + sin(finale_t * 2.0 + float(i)) * 1.1, sin(aa) * 7.0)
		n3.position = n3.position.lerp(goal, 1.0 - pow(0.02, delta))
	if fmod(finale_t, 1.4) < delta:
		_sparkle_burst(player.position + Vector3(randf() * 8.0 - 4.0, 4.0, randf() * 8.0 - 4.0), Color.from_hsv(randf(), 0.6, 1.0))
	if finale_t > 28.0:
		for n4 in finale_nodes:
			if is_instance_valid(n4):
				n4.queue_free()
		finale_nodes.clear()
		finale_t = -1.0
		_play_music("world")

const HINTS := [
	"Move with the stick - or the arrow keys!",
	"Press the big button to swim up!",
	"Swim to the glowing light pillars to find friends!"]

func _tick_hints(delta: float) -> void:
	if not first_session or game != "" or hint_idx >= HINTS.size():
		return
	hint_t += delta
	if hint_t > 2.0 + float(hint_idx) * 8.0:
		show_msg("Roshan", HINTS[hint_idx])
		hint_idx += 1

# ===================== MINIGAMES =====================
func _clear_game() -> void:
	if melody_ui != null:
		melody_ui.visible = false
	_dolls2d_close()
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	arena_solids.clear()
	fade_walls.clear()
	game = ""
	g = {}
	hud_game.text = ""

func _fail_line() -> String:
	# in-character failure lines, by game (the on-screen text; the matching
	# character voice plays via show_msg's "fail" event — drop <speaker>_fail.ogg
	# into assets/audio/voices to use a real recorded clip)
	match game:
		"fetch":      return "Aww... now Chuck is all wet!"
		"dolls":      return "Oh no, the babies!"
		"seek":       return "Where did Lamb-a' go?"
		"melody":     return "Oh no, the colors!"
		"treasure":   return "Aww, the treasure slipped back into the dark!"
		"shop":       return "Come back when you've found more pearls!"
		"fairyshoot": return "Oh no, the shadow bugs got away!"
		"slide":      return "Aww, the baby penguin slid away! Race again?" if String(g.get("mode", "fish")) == "chase" else "So close! Catch more fish next time!"
		_:            return "So close! Swim back and try again!"

func _end_game(win: bool, fr: Dictionary, txt: String, vo: String = "talk") -> void:
	_leave_arena()
	if win and not fr["won"]:
		fr["won"] = true
		trophies += 1
		_add_won_star(fr)
		if voice != null:
			voice.pitch_scale = 1.1
			voice.play()
	fr["cool"] = 5.0
	if String(fr["fname"]) == "Secret Cave":
		treasure_cool = 14.0
	elif String(fr["fname"]) == "Pearl Shop":
		shop_cool = 16.0
	elif String(fr["fname"]) == "Fairy Pond":
		fairy_cool = 12.0
		_apply_skin()   # restore Roshan's normal look after the fairy flight
	_respawn_pearls()
	show_msg(fr["fname"], txt, vo)
	_update_hud()
	_clear_game()
	_write_save()
	if String(fr.get("fname", "")) == "Rainbow Slide" or String(fr.get("fname", "")) == "Fairy Pond":
		call_deferred("_enter_level2", true)   # return to the castle courtyard
		return
	if trophies >= 5 and not finale_done:
		call_deferred("_begin_finale")

func _game_ball(col: Color, radius: float) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var sph := SphereMesh.new()
	sph.radius = radius
	sph.height = radius * 2.0
	mi.mesh = sph
	var m := StandardMaterial3D.new()
	if col == Color(1.0, 0.4, 0.25):
		m.albedo_texture = load("res://assets/terrain/beachball.png")
		m.albedo_color = Color(1, 1, 1)
		m.roughness = 0.35
		m.emission_enabled = true
		m.emission = Color(0.6, 0.5, 0.45)
		m.emission_energy_multiplier = 0.25
	else:
		m.albedo_color = col
		m.emission_enabled = true
		m.emission = col * 0.5
	mi.material_override = m
	add_child(mi)
	game_nodes.append(mi)
	return mi

func _soft_mat(col: Color, glow: float = 0.12) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = col
	m.roughness = 0.55
	m.emission_enabled = true
	m.emission = col * glow
	return m

func _check_star(pos: Vector3) -> MeshInstance3D:
	var st := MeshInstance3D.new()
	var tor := TorusMesh.new()
	tor.inner_radius = 1.7
	tor.outer_radius = 2.3
	st.mesh = tor
	var m := StandardMaterial3D.new()
	m.albedo_color = Color(1.0, 0.88, 0.35)
	m.emission_enabled = true
	m.emission = Color(1.0, 0.85, 0.4)
	m.emission_energy_multiplier = 1.6
	st.material_override = m
	st.position = pos
	add_child(st)
	game_nodes.append(st)
	var l := OmniLight3D.new()
	l.light_color = Color(1.0, 0.9, 0.6)
	l.light_energy = 1.3
	l.omni_range = 9.0
	st.add_child(l)
	return st

func _course_box(pos: Vector3, size: Vector3, col: Color, rotdeg: Vector3 = Vector3.ZERO) -> MeshInstance3D:
	var b := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	b.mesh = bm
	b.material_override = _soft_mat(col)
	b.position = pos
	b.rotation_degrees = rotdeg
	add_child(b)
	game_nodes.append(b)
	return b

func _build_chain_curtain(bar_from: Vector3, bar_to: Vector3, n_chains: int) -> void:
	# soft-play "finger" curtain: swinging rod chains with simple spring physics
	_course_box((bar_from + bar_to) * 0.5, Vector3(maxf((bar_to - bar_from).length(), 0.6), 0.6, 0.6), Color(0.9, 0.4, 0.7), Vector3(0, rad_to_deg(atan2((bar_to - bar_from).z, (bar_to - bar_from).x)) * -1.0, 0))
	var fingers := [Color(1.0, 0.45, 0.45), Color(1.0, 0.85, 0.3), Color(0.4, 0.9, 0.6), Color(0.45, 0.6, 1.0), Color(0.8, 0.5, 1.0)]
	for i in range(n_chains):
		var t: float = float(i) / float(n_chains - 1)
		var base: Vector3 = bar_from.lerp(bar_to, t)
		var segs: Array = []
		for k in range(5):
			var cap := MeshInstance3D.new()
			var cm := CapsuleMesh.new()
			cm.radius = 0.26
			cm.height = 1.05
			cap.mesh = cm
			cap.material_override = _soft_mat(fingers[(i + k) % fingers.size()], 0.25)
			add_child(cap)
			game_nodes.append(cap)
			segs.append(cap)
		(g["chains"] as Array).append({"base": base, "ang": Vector2(randf() * 0.1, randf() * 0.1), "vel": Vector2.ZERO, "segs": segs})

func _add_check(pos: Vector3, kind: String) -> void:
	var node := _check_star(pos)
	(g["checks"] as Array).append({"node": node, "hit": false, "kind": kind})

func _build_playplace(origin: Vector3, fr: Dictionary) -> void:
	var gy: float = ARENA_POS.y
	var pads := [Color(1.0, 0.5, 0.6), Color(1.0, 0.85, 0.35), Color(0.4, 0.85, 0.95), Color(0.7, 0.55, 1.0)]
	if rainbow_slide_mode:
		pads = [Color(1.0, 0.25, 0.3), Color(1.0, 0.6, 0.15), Color(1.0, 0.9, 0.25), Color(0.3, 0.85, 0.4), Color(0.3, 0.55, 1.0), Color(0.6, 0.35, 0.9)]
	# spiral story platforms (3 stories)
	for i in range(9):
		var aa: float = float(i) * 0.75
		var rr: float = 14.0 - float(i) * 0.8
		var pp := Vector3(origin.x + cos(aa) * rr, gy + 2.0 + float(i) * 3.0, origin.z + sin(aa) * rr)
		_course_box(pp, Vector3(5.5, 0.8, 4.2), pads[i % pads.size()])
	# story rims (visual floors)
	for st in range(3):
		var rim := MeshInstance3D.new()
		var tm := TorusMesh.new()
		tm.inner_radius = 16.5
		tm.outer_radius = 17.3
		rim.mesh = tm
		rim.material_override = _soft_mat(pads[st % pads.size()], 0.3)
		rim.position = Vector3(origin.x, gy + 10.0 + float(st) * 9.0, origin.z)
		add_child(rim)
		game_nodes.append(rim)
	# ball pit (colorful balls in a ring pool)
	var pit := Vector3(origin.x + 14.0, gy + 0.8, origin.z)
	var wall := MeshInstance3D.new()
	var wt := TorusMesh.new()
	wt.inner_radius = 5.4
	wt.outer_radius = 6.6
	wall.mesh = wt
	wall.material_override = _soft_mat(Color(0.45, 0.6, 1.0), 0.2)
	wall.position = pit
	add_child(wall)
	game_nodes.append(wall)
	var mmi := MultiMeshInstance3D.new()
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = true
	var bms := SphereMesh.new()
	bms.radius = 0.55
	bms.height = 1.1
	var bmat := StandardMaterial3D.new()
	bmat.vertex_color_use_as_albedo = true
	bmat.roughness = 0.4
	bms.material = bmat
	mm.mesh = bms
	mm.instance_count = 90
	for bi in range(90):
		var ba: float = randf() * TAU
		var br: float = sqrt(randf()) * 4.8
		var bp := Vector3(pit.x + cos(ba) * br, gy + 0.7 + randf() * 1.6, pit.z + sin(ba) * br)
		mm.set_instance_transform(bi, Transform3D(Basis(), bp))
		mm.set_instance_color(bi, pads[bi % pads.size()])
	mmi.multimesh = mm
	add_child(mmi)
	game_nodes.append(mmi)
	# trampoline
	var tramp := Vector3(origin.x - 13.0, gy + 1.2, origin.z + 8.0)
	_course_box(tramp, Vector3(4.6, 0.7, 4.6), Color(0.25, 0.45, 0.95))
	_course_box(tramp + Vector3(0, -0.8, 0), Vector3(3.6, 0.9, 3.6), Color(0.15, 0.2, 0.4))
	g["tramp_pos"] = tramp
	# finger curtains (2 passages)
	_build_chain_curtain(Vector3(origin.x - 5.0, gy + 17.5, origin.z - 11.0), Vector3(origin.x + 5.0, gy + 17.5, origin.z - 11.0), 7)
	_build_chain_curtain(Vector3(origin.x + 4.0, gy + 27.5, origin.z + 3.0), Vector3(origin.x + 4.0, gy + 27.5, origin.z + 13.0), 7)
	# moving ring obstacle (story 2)
	var mv := MeshInstance3D.new()
	var mt := TorusMesh.new()
	mt.inner_radius = 2.6
	mt.outer_radius = 3.4
	mv.mesh = mt
	mv.material_override = _soft_mat(Color(0.5, 1.0, 0.6), 0.6)
	mv.rotation_degrees = Vector3(90, 0, 0)
	mv.position = Vector3(origin.x - 6.0, gy + 19.0, origin.z + 6.0)
	add_child(mv)
	game_nodes.append(mv)
	g["mover_node"] = mv
	g["mover_base"] = mv.position
	# THE BIG SLIDE: yellow chute from the top to the ground
	var path: Array = [
		Vector3(origin.x, gy + 29.0, origin.z),
		Vector3(origin.x + 6.0, gy + 25.5, origin.z + 4.0),
		Vector3(origin.x + 11.0, gy + 21.0, origin.z + 8.0),
		Vector3(origin.x + 14.5, gy + 15.5, origin.z + 12.0),
		Vector3(origin.x + 16.0, gy + 10.0, origin.z + 16.5),
		Vector3(origin.x + 15.0, gy + 5.0, origin.z + 21.0),
		Vector3(origin.x + 12.5, gy + 2.8, origin.z + 25.0)]
	g["slide_path"] = path
	for i in range(path.size() - 1):
		var a2: Vector3 = path[i]
		var b2: Vector3 = path[i + 1]
		var mid: Vector3 = (a2 + b2) * 0.5
		var seg := MeshInstance3D.new()
		var sb := BoxMesh.new()
		sb.size = Vector3(3.4, 0.5, a2.distance_to(b2) + 0.7)
		seg.mesh = sb
		seg.material_override = _soft_mat(Color(1.0, 0.8, 0.2), 0.25)
		add_child(seg)
		seg.look_at_from_position(mid, b2, Vector3.UP)
		game_nodes.append(seg)
		for sgn in [-1.0, 1.0]:
			var rail := MeshInstance3D.new()
			var rb := BoxMesh.new()
			rb.size = Vector3(0.4, 1.0, a2.distance_to(b2) + 0.7)
			rail.mesh = rb
			rail.material_override = _soft_mat(Color(1.0, 0.55, 0.25), 0.2)
			add_child(rail)
			rail.look_at_from_position(mid, b2, Vector3.UP)
			rail.translate_object_local(Vector3(sgn * 1.7, 0.5, 0))
			game_nodes.append(rail)
	# friend cheering at the slide top (only when this game has a friend sprite — the Rainbow Slide has none)
	var cheer_node = fr.get("node")
	if cheer_node != null and is_instance_valid(cheer_node) and cheer_node is Sprite3D:
		var sis := Sprite3D.new()
		sis.texture = (cheer_node as Sprite3D).texture
		sis.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		sis.pixel_size = 0.013
		sis.position = path[0] + Vector3(-3.0, 3.0, -2.0)
		add_child(sis)
		game_nodes.append(sis)
	# checkpoints: ballpit -> trampoline -> curtain 1 -> moving ring -> curtain 2 -> slide
	_add_check(pit + Vector3(0, 1.6, 0), "ball")
	_add_check(g["tramp_pos"] + Vector3(0, 1.8, 0), "tramp")
	_add_check(Vector3(origin.x, gy + 14.6, origin.z - 11.0), "curtain")
	_add_check(mv.position, "mover")
	_add_check(Vector3(origin.x + 4.0, gy + 24.6, origin.z + 8.0), "curtain")
	_add_check(path[0], "slide")

func _build_cavern(origin: Vector3) -> void:
	var gy: float = ARENA_POS.y
	var pts := [
		Vector3(origin.x, gy + 8.0, origin.z + 14.0),
		Vector3(origin.x - 10.0, gy + 6.0, origin.z + 4.0),
		Vector3(origin.x - 6.0, gy + 4.2, origin.z - 8.0),
		Vector3(origin.x + 6.0, gy + 3.4, origin.z - 12.0),
		Vector3(origin.x + 12.0, gy + 3.0, origin.z - 2.0)]
	# rock tunnels around each passage
	for i in range(pts.size() - 1):
		var a2: Vector3 = pts[i]
		var b2: Vector3 = pts[i + 1]
		var mid: Vector3 = (a2 + b2) * 0.5
		var dirv: Vector3 = (b2 - a2).normalized()
		var side: Vector3 = dirv.cross(Vector3.UP).normalized()
		var up2: Vector3 = side.cross(dirv).normalized()
		for k in range(7):
			var ra: float = float(k) / 7.0 * TAU
			var rp: Vector3 = mid + (side * cos(ra) + up2 * sin(ra)) * 5.2
			var rk := _place_aq("Rock%d" % (1 + (k + i) % 11), rp, 1.5 + randf() * 1.2, false)
			if rk != null:
				game_nodes.append(rk)
	# glowing anemones light the way
	for p2 in pts:
		var an := MeshInstance3D.new()
		an.mesh = _anemone_mesh()
		an.material_override = _glow_tip_mat()
		an.scale = Vector3.ONE * 1.8
		an.position = p2 + Vector3(1.5, -2.0, 1.0)
		add_child(an)
		game_nodes.append(an)
	# treasure chest at the bottom, bathed in gold light
	var chest := _spawn("chest", pts[pts.size() - 1] + Vector3(0, -2.4, 0), 5.0, 0.9)
	if chest != null:
		game_nodes.append(chest)
	var gl := OmniLight3D.new()
	gl.light_color = Color(1.0, 0.85, 0.4)
	gl.light_energy = 2.2
	gl.omni_range = 14.0
	gl.position = pts[pts.size() - 1]
	add_child(gl)
	game_nodes.append(gl)
	# ---- treasure-cave dressing: glowing crystals, gems, gold coins, pearls ----
	var gem_cols := [Color(1.0, 0.3, 0.45), Color(0.4, 0.7, 1.0), Color(0.5, 1.0, 0.65), Color(1.0, 0.85, 0.35), Color(0.8, 0.45, 1.0)]
	var seed2 := 7
	for k in range(28):
		seed2 = (seed2 * 1103515245 + 12345) & 0x7fffffff
		var pa: Vector3 = pts[(seed2 / 31) % pts.size()]
		var off := Vector3(float(seed2 % 100) / 100.0 * 9.0 - 4.5, -2.2 - float((seed2 / 100) % 100) / 100.0 * 1.6, float((seed2 / 7) % 100) / 100.0 * 9.0 - 4.5)
		var spot: Vector3 = pa + off
		var kind := (seed2 / 13) % 4
		if kind == 0:                      # glowing crystal cluster
			var cr := MeshInstance3D.new()
			var pm := PrismMesh.new(); pm.size = Vector3(1.3, 3.5 + randf() * 2.5, 1.3)
			cr.mesh = pm
			cr.material_override = _soft_mat(gem_cols[(seed2 / 3) % gem_cols.size()], 1.7)
			cr.position = spot; cr.rotation = Vector3(randf() * 0.3, randf() * TAU, randf() * 0.3)
			add_child(cr); game_nodes.append(cr)
		elif kind == 1:                    # bright gem
			var gem := MeshInstance3D.new()
			var sp := SphereMesh.new(); sp.radius = 0.55; sp.height = 1.1
			gem.mesh = sp
			gem.material_override = _soft_mat(gem_cols[(seed2 / 5) % gem_cols.size()], 2.6)
			gem.position = spot + Vector3(0, 1.0, 0)
			add_child(gem); game_nodes.append(gem)
		elif kind == 2:                    # stack of gold coins
			for c in range(3):
				var coin := MeshInstance3D.new()
				var cyl := CylinderMesh.new(); cyl.top_radius = 0.5; cyl.bottom_radius = 0.5; cyl.height = 0.12
				coin.mesh = cyl
				var cmat := StandardMaterial3D.new()
				cmat.albedo_color = Color(1.0, 0.82, 0.3); cmat.metallic = 0.9; cmat.roughness = 0.25
				cmat.emission_enabled = true; cmat.emission = Color(0.8, 0.6, 0.2); cmat.emission_energy_multiplier = 0.4
				coin.material_override = cmat
				coin.position = spot + Vector3(0, 0.2 + float(c) * 0.13, 0)
				add_child(coin); game_nodes.append(coin)
		else:                              # glowing pearl
			var pl := MeshInstance3D.new()
			var ps := SphereMesh.new(); ps.radius = 0.6; ps.height = 1.2
			pl.mesh = ps
			pl.material_override = _soft_mat(Color(1.0, 0.92, 0.97), 1.1)
			pl.position = spot + Vector3(0, 0.6, 0)
			add_child(pl); game_nodes.append(pl)
	for i in range(pts.size()):
		_add_check(pts[i], "chest" if i == pts.size() - 1 else "way")

func _plank_box(pos: Vector3, size: Vector3, alpha: float = 1.0) -> void:
	var b := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	b.mesh = bm
	var m := StandardMaterial3D.new()
	m.albedo_texture = load("res://assets/terrain/up_wood_col.jpg")
	m.albedo_color = Color(0.85, 0.72, 0.55, alpha)
	m.normal_enabled = true
	m.normal_texture = load("res://assets/terrain/up_wood_nrm.jpg")
	m.roughness_texture = load("res://assets/terrain/up_wood_rgh.jpg")
	m.uv1_triplanar = true
	m.uv1_world_triplanar = true
	m.uv1_scale = Vector3(0.15, 0.15, 0.15)
	m.roughness = 0.9
	if alpha < 1.0:
		m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		m.cull_mode = BaseMaterial3D.CULL_DISABLED
	b.material_override = m
	b.position = pos
	add_child(b)
	game_nodes.append(b)

func _build_shop_cabin(origin: Vector3) -> void:
	var f: float = ARENA_POS.y + 2.0
	# open-fronted cabin diorama: solid back, see-through sides, no front wall/ceiling
	# (so the chase camera never clips into a solid wall)
	_plank_box(Vector3(origin.x, f + 9.0, origin.z - 13.0), Vector3(34, 19, 1.2))
	_plank_box(Vector3(origin.x - 16.0, f + 9.0, origin.z + 2.0), Vector3(1.2, 19, 30), 0.35)
	_plank_box(Vector3(origin.x + 16.0, f + 9.0, origin.z + 2.0), Vector3(1.2, 19, 30), 0.35)
	# slim top beam instead of a full ceiling
	_plank_box(Vector3(origin.x, f + 18.0, origin.z - 13.0), Vector3(34, 1.2, 4), 0.5)
	# counter with a cloth
	var counter := _course_box(Vector3(origin.x, f + 1.3, origin.z - 5.0), Vector3(12.0, 2.6, 4.6), Color(0.35, 0.55, 0.3))
	counter.material_override.roughness = 1.0
	# warm hanging lanterns
	for lx in [-7.0, 7.0]:
		var lamp := OmniLight3D.new()
		lamp.light_color = Color(1.0, 0.78, 0.45)
		lamp.light_energy = 2.4
		lamp.omni_range = 22.0
		lamp.position = Vector3(origin.x + lx, f + 12.0, origin.z - 2.0)
		add_child(lamp)
		game_nodes.append(lamp)
		var bulb := MeshInstance3D.new()
		var bm3 := SphereMesh.new()
		bm3.radius = 0.3
		bm3.height = 0.6
		bulb.mesh = bm3
		var bmat3 := StandardMaterial3D.new()
		bmat3.emission_enabled = true
		bmat3.emission = Color(1.0, 0.8, 0.45)
		bmat3.emission_energy_multiplier = 3.5
		bulb.material_override = bmat3
		bulb.position = lamp.position
		add_child(bulb)
		game_nodes.append(bulb)
		var cord := _course_box(lamp.position + Vector3(0, 3.0, 0), Vector3(0.12, 6.0, 0.12), Color(0.25, 0.18, 0.1))
		cord.material_override.emission_enabled = false
	# hanging kelp bunches like dried herbs
	for hk in range(5):
		var bunch := MeshInstance3D.new()
		bunch.mesh = _cross_blade(0.5, 2.2)
		bunch.material_override = _sway_grass_mat(Color(0.2, 0.25, 0.1), Color(0.45, 0.5, 0.2))
		bunch.position = Vector3(origin.x - 10.0 + float(hk) * 5.0, f + 15.5, origin.z - 9.0)
		bunch.rotation_degrees = Vector3(180, randf() * 360.0, 0)
		add_child(bunch)
		game_nodes.append(bunch)
	# barrels in the corners
	var b1 := _spawn("barrel", Vector3(origin.x - 13.0, f, origin.z + 12.0), 3.2, 0.4)
	if b1 != null:
		game_nodes.append(b1)
	var b2 := _spawn("barrel", Vector3(origin.x + 13.0, f, origin.z - 9.0), 3.2, 1.1)
	if b2 != null:
		game_nodes.append(b2)
	# Kareem is the living shopkeeper, a billboard sprite sitting beside his goods
	var kareem := Sprite3D.new()
	kareem.texture = load("res://assets/characters/friends/kareem.png")
	kareem.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	kareem.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	kareem.pixel_size = 0.02
	kareem.position = Vector3(origin.x + 9.5, f + 5.5, origin.z - 6.0)
	add_child(kareem)
	game_nodes.append(kareem)
	var kspot := OmniLight3D.new()
	kspot.light_color = Color(1.0, 0.92, 0.8)
	kspot.light_energy = 1.6
	kspot.omni_range = 16.0
	kspot.position = kareem.position + Vector3(0, 3, 3)
	add_child(kspot)
	game_nodes.append(kspot)
	var klbl := Label3D.new()
	klbl.text = "Kareem's Shop"
	klbl.font_size = 60
	klbl.pixel_size = 0.02
	klbl.outline_size = 12
	klbl.modulate = Color(1.0, 0.9, 0.6)
	klbl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	klbl.position = Vector3(origin.x, f + 14.0, origin.z - 9.0)
	add_child(klbl)
	game_nodes.append(klbl)
	# wares on the counter
	g["items"] = []
	var slots := [-4.0, 0.0, 4.0]
	for ii in range(SHOP_ITEMS.size()):
		var it: Dictionary = SHOP_ITEMS[ii]
		var iid := String(it["id"])
		var ipos := Vector3(origin.x + slots[ii], f + 2.2, origin.z - 4.6)
		var inode: Node3D
		if iid == "tiara":
			var crown := MeshInstance3D.new()
			var tm := TorusMesh.new()
			tm.inner_radius = 0.55
			tm.outer_radius = 0.85
			crown.mesh = tm
			var cm := StandardMaterial3D.new()
			cm.albedo_color = Color(1.0, 0.85, 0.35)
			cm.metallic = 0.8
			cm.roughness = 0.25
			cm.emission_enabled = true
			cm.emission = Color(1.0, 0.8, 0.3)
			cm.emission_energy_multiplier = 1.6
			crown.material_override = cm
			inode = crown
		elif iid == "tail":
			var orb := MeshInstance3D.new()
			var om2 := SphereMesh.new()
			om2.radius = 0.7
			om2.height = 1.4
			orb.mesh = om2
			orb.material_override = _rainbow_mat()
			inode = orb
		else:
			# the legendary Can of Beans
			var can := MeshInstance3D.new()
			var cyl := CylinderMesh.new()
			cyl.top_radius = 0.45
			cyl.bottom_radius = 0.45
			cyl.height = 1.1
			can.mesh = cyl
			var tin := StandardMaterial3D.new()
			tin.albedo_color = Color(0.75, 0.78, 0.8)
			tin.metallic = 0.9
			tin.roughness = 0.3
			can.material_override = tin
			var lbl := MeshInstance3D.new()
			var lcyl := CylinderMesh.new()
			lcyl.top_radius = 0.47
			lcyl.bottom_radius = 0.47
			lcyl.height = 0.6
			lbl.mesh = lcyl
			var lm2 := StandardMaterial3D.new()
			lm2.albedo_color = Color(0.85, 0.3, 0.2)
			lm2.roughness = 0.8
			lbl.material_override = lm2
			can.add_child(lbl)
			inode = can
		inode.position = ipos
		add_child(inode)
		game_nodes.append(inode)
		var tag := Label3D.new()
		tag.text = "%s\n%d pearls" % [String(it["label"]), int(it["price"])]
		tag.font_size = 64
		tag.modulate = Color(1.0, 0.95, 0.8)
		tag.outline_size = 14
		tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		tag.position = ipos + Vector3(0, 1.7, 0)
		add_child(tag)
		game_nodes.append(tag)
		(g["items"] as Array).append({"id": iid, "node": inode, "tag": tag, "price": int(it["price"]), "base": ipos})
	# glowing exit door
	var door := MeshInstance3D.new()
	var dt := TorusMesh.new()
	dt.inner_radius = 2.4
	dt.outer_radius = 3.1
	door.mesh = dt
	door.rotation_degrees = Vector3(90, 0, 0)
	var dm := StandardMaterial3D.new()
	dm.albedo_color = Color(0.5, 0.9, 1.0)
	dm.emission_enabled = true
	dm.emission = Color(0.4, 0.85, 1.0)
	dm.emission_energy_multiplier = 1.8
	door.material_override = dm
	door.position = Vector3(origin.x - 12.0, f + 4.0, origin.z + 14.5)
	add_child(door)
	game_nodes.append(door)
	g["exit"] = door
	var dl := Label3D.new()
	dl.text = "\u2190 swim out to leave"
	dl.font_size = 56
	dl.outline_size = 12
	dl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	dl.position = door.position + Vector3(0, 3.6, 0)
	add_child(dl)
	game_nodes.append(dl)

func _tick_shop(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	hud_game.text = "Pearls: %d - swim to a treasure to buy it!" % pearl_count
	shop_msg_cool = maxf(0.0, shop_msg_cool - delta)
	for it in g.get("items", []):
		var inode: Node3D = it["node"]
		if not inode.visible:
			continue
		inode.position.y = (it["base"] as Vector3).y + sin(float(g["t"]) * 2.0 + (it["base"] as Vector3).x) * 0.25
		inode.rotate_y(delta * 1.2)
		if _near_ground(it["base"], ppos, 5.0, 14.0):
			var iid := String(it["id"])
			var price: int = int(it["price"])
			if iid == "beans":
				if beans_t >= 0.0:
					pass
				elif pearl_count >= price:
					_shop_buy(iid)
					show_msg("Pearl Shop", "Beans! Hold on to your tail!")
				elif shop_msg_cool <= 0.0:
					shop_msg_cool = 2.5
					show_msg("Pearl Shop", "Beans cost %d pearls - the reef is full of them!" % price)
			elif pearl_count >= price:
				_shop_buy(iid)
				inode.visible = false
				(it["tag"] as Label3D).text = String(it["tag"].text.split("\n")[0]) + "\n(yours!)"
				show_msg("Pearl Shop", "It looks WONDERFUL on you!")
			elif shop_msg_cool <= 0.0:
				shop_msg_cool = 2.5
				show_msg("Pearl Shop", "You need %d pearls for that - the reef is full of them!" % price)
	var door: MeshInstance3D = g["exit"]
	door.scale = Vector3.ONE * (1.0 + sin(float(g["t"]) * 3.0) * 0.08)
	# leave the shop by simply swimming OUT of the room (open front / sides)
	var rel: Vector3 = ppos - ARENA_POS
	if float(g["t"]) > 1.5 and (rel.z > 20.0 or rel.z < -16.0 or absf(rel.x) > 19.0):
		_end_game(true, fr, "Bye-bye! Come back soon!")

func _tick_chains(delta: float, ppos: Vector3) -> void:
	for ch in g.get("chains", []):
		var base: Vector3 = ch["base"]
		var ang: Vector2 = ch["ang"]
		var vel: Vector2 = ch["vel"]
		vel += (-ang * 7.0 - vel * 1.8) * delta
		# the player brushes the fingers aside
		var mid: Vector3 = base + Vector3(ang.x, -1.0, ang.y).normalized() * 2.4
		var dd: float = mid.distance_to(ppos)
		if dd < 2.6:
			var push := Vector2(mid.x - ppos.x, mid.z - ppos.z)
			if push.length() > 0.01:
				vel += push.normalized() * (2.6 - dd) * 14.0 * delta
		ang += vel * delta
		if ang.length() > 1.0:
			ang = ang.normalized()
		ch["ang"] = ang
		ch["vel"] = vel
		var dirv: Vector3 = Vector3(ang.x, -1.0, ang.y).normalized()
		var segs: Array = ch["segs"]
		for k in range(segs.size()):
			var seg: MeshInstance3D = segs[k]
			seg.position = base + dirv * (0.6 + float(k) * 0.98)
			seg.quaternion = Quaternion(Vector3.DOWN, dirv)

func _tick_course(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_tick_chains(delta, ppos)
	if g.has("mover_node"):
		var mvn: MeshInstance3D = g["mover_node"]
		mvn.position = (g["mover_base"] as Vector3) + Vector3(sin(float(g["t"]) * 0.9) * 6.0, 0, 0)
	# slide ride
	if String(g.get("phase", "")) == "slide":
		var path: Array = g["slide_path"]
		var st: float = float(g.get("slide_t", 0.0)) + delta * 13.0
		g["slide_t"] = st
		var total := 0.0
		for i in range(path.size() - 1):
			var seg_len: float = (path[i] as Vector3).distance_to(path[i + 1])
			if st <= total + seg_len:
				player.position = (path[i] as Vector3).lerp(path[i + 1], (st - total) / seg_len)
				player.vel = Vector3.ZERO
				hud_game.text = "WHEEEEE!"
				return
			total += seg_len
		_sparkle_burst(player.position, Color(0.5, 0.85, 1.0))
		if chime != null:
			chime.play()
		_end_game(true, fr, "What a SLIDE! Best play place ever!" if game == "race" else "")
		return
	var checks: Array = g.get("checks", [])
	var done := 0
	var nxt: Dictionary = {}
	for c in checks:
		if c["hit"]:
			done += 1
		elif nxt.is_empty():
			nxt = c
	hud_game.text = ("Climb the play place! Sparkles: %d / %d" if game == "race" else "Dive the caverns! Sparkles: %d / %d") % [done, checks.size()]
	if nxt.is_empty():
		return
	var node: MeshInstance3D = nxt["node"]
	node.scale = Vector3.ONE * (1.0 + sin(float(g["t"]) * 5.0) * 0.15)
	node.rotate_y(delta * 1.5)
	var dd2: float = node.position.distance_to(ppos)
	# strong, far-reaching magnet carries a 4yo up the play-place automatically
	if dd2 < 34.0:
		player.position = player.position.lerp(node.position, minf(0.92, delta * 2.6 * (1.0 - dd2 / 34.0)))
		player.vel.y = maxf(player.vel.y, 0.0)
	if dd2 < 7.5:
		nxt["hit"] = true
		_sparkle_burst(node.position, Color(1.0, 0.9, 0.5))
		if chime != null:
			chime.pitch_scale = 1.0 + float(done) * 0.08
			chime.play()
		var kind := String(nxt["kind"])
		if kind == "tramp":
			player.vel.y = 26.0
			show_msg(fr["fname"], "BOING! Up you go!")
		elif kind == "slide":
			g["phase"] = "slide"
			g["slide_t"] = 0.0
		elif kind == "chest":
			pearl_count += 3
			_update_hud()
			_write_save()
			_sparkle_burst(node.position, Color(1.0, 0.85, 0.3))
			_end_game(true, fr, "TREASURE! +3 rainbow pearls for the Pearl Shop!")
		else:
			node.visible = false

func _start_game(fr: Dictionary) -> void:
	game = String(fr["game"])
	g = {"fr": fr, "t": 0.0, "timer": 30.0}
	_enter_arena(game)
	var origin: Vector3 = ARENA_POS
	if game == "fetch":
		g["phase"] = "aim"
		g["round"] = 0
		g["miss"] = 0
		g["timer"] = -1.0
		g["ball"] = _game_ball(Color(1.0, 0.4, 0.25), 0.8)
		# ----- a real 3D winter Lake Michigan scene -----
		# snowy play field (the LEFT side, where Roshan and Chuck are)
		var snow := MeshInstance3D.new()
		var snm := BoxMesh.new()
		snm.size = Vector3(70.0, 1.0, 170.0)
		snow.mesh = snm
		var snmat := StandardMaterial3D.new()
		snmat.albedo_color = Color(0.96, 0.98, 1.0)
		snmat.roughness = 0.85
		snow.material_override = snmat
		snow.position = origin + Vector3(-27.0, 0.0, 0.0)
		add_child(snow)
		game_nodes.append(snow)
		# the VAST icy lake — stretches the whole length on the right, out to the horizon
		var lake := MeshInstance3D.new()
		var lb := BoxMesh.new()
		lb.size = Vector3(220.0, 0.6, 320.0)
		lake.mesh = lb
		var lm := StandardMaterial3D.new()
		lm.albedo_color = Color(0.45, 0.66, 0.82)
		lm.metallic = 0.85
		lm.roughness = 0.06
		lm.emission_enabled = true
		lm.emission = Color(0.3, 0.55, 0.72)
		lm.emission_energy_multiplier = 0.2
		lake.material_override = lm
		lake.position = origin + Vector3(118.0, 0.3, 0.0)
		add_child(lake)
		game_nodes.append(lake)
		# snowdrift shoreline ridge along the waterline (the whole length)
		_course_box(origin + Vector3(8.2, 0.7, 0.0), Vector3(2.0, 1.4, 170.0), Color(0.99, 1.0, 1.0))
		# drifting ice floes far out on the lake
		for fl in range(8):
			var floe := MeshInstance3D.new()
			var fm := CylinderMesh.new()
			fm.top_radius = 2.0 + randf() * 3.0
			fm.bottom_radius = fm.top_radius + 0.3
			fm.height = 0.5
			floe.mesh = fm
			floe.material_override = _soft_mat(Color(0.95, 0.98, 1.0), 0.1)
			floe.position = origin + Vector3(18.0 + randf() * 90.0, 0.8, -75.0 + randf() * 150.0)
			add_child(floe)
			game_nodes.append(floe)
		# snowy pine forest + hills along the far shore and behind
		for tz in range(16):
			var tang := float(tz) / 16.0
			var tx: float = -52.0 + randf() * 14.0
			var tzz: float = -80.0 + tang * 160.0
			# snowy hill
			if tz % 3 == 0:
				var hill := MeshInstance3D.new()
				var hs := SphereMesh.new()
				hs.radius = 12.0 + randf() * 8.0
				hill.mesh = hs
				hill.material_override = snmat
				hill.position = origin + Vector3(tx - 8.0, -2.0, tzz)
				hill.scale.y = 0.45
				add_child(hill)
				game_nodes.append(hill)
			# snowy pine (green cone capped with snow)
			var pine := MeshInstance3D.new()
			var pc := CylinderMesh.new()
			pc.top_radius = 0.0
			pc.bottom_radius = 3.0 + randf() * 1.5
			pc.height = 9.0 + randf() * 4.0
			pine.mesh = pc
			var pmat := StandardMaterial3D.new()
			pmat.albedo_color = Color(0.25, 0.42, 0.32)
			pine.material_override = pmat
			pine.position = origin + Vector3(tx, pc.height * 0.5, tzz)
			add_child(pine)
			game_nodes.append(pine)
			var cap := MeshInstance3D.new()
			var cc := CylinderMesh.new()
			cc.top_radius = 0.0
			cc.bottom_radius = pc.bottom_radius * 0.7
			cc.height = pc.height * 0.45
			cap.mesh = cc
			cap.material_override = snmat
			cap.position = pine.position + Vector3(0, pc.height * 0.32, 0)
			add_child(cap)
			game_nodes.append(cap)
		# gently falling snow over the scene
		var snowfall := GPUParticles3D.new()
		snowfall.amount = 120
		snowfall.lifetime = 6.0
		snowfall.preprocess = 4.0
		var spm := ParticleProcessMaterial.new()
		spm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
		spm.emission_box_extents = Vector3(60, 1, 80)
		spm.gravity = Vector3(1.0, -4.0, 0)
		spm.initial_velocity_min = 0.5
		spm.initial_velocity_max = 1.5
		spm.scale_min = 0.1
		spm.scale_max = 0.3
		snowfall.process_material = spm
		var sflake := SphereMesh.new()
		sflake.radius = 0.5
		sflake.height = 1.0
		sflake.radial_segments = 5
		sflake.rings = 3
		var sfm := StandardMaterial3D.new()
		sfm.albedo_color = Color(1, 1, 1)
		sfm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		sflake.material = sfm
		snowfall.draw_pass_1 = sflake
		snowfall.position = origin + Vector3(-10, 30, 0)
		add_child(snowfall)
		game_nodes.append(snowfall)
		# ---- explorable detail: snowy boulders, a wooden dock, a cleared shore path ----
		var rockmat := StandardMaterial3D.new()
		rockmat.albedo_texture = load("res://assets/terrain/Rock061_2K_Color.jpg")
		rockmat.albedo_color = Color(0.78, 0.8, 0.86)
		rockmat.normal_enabled = true
		rockmat.normal_texture = load("res://assets/terrain/Rock061_2K_NormalGL.jpg")
		rockmat.uv1_triplanar = true
		rockmat.uv1_world_triplanar = true
		rockmat.uv1_scale = Vector3(0.3, 0.3, 0.3)
		rockmat.roughness = 0.95
		var rsd := 7
		for ri in range(10):
			rsd = (rsd * 1103515245 + 12345) & 0x7fffffff
			var rx: float = -52.0 + float(rsd % 50)
			var rz: float = -75.0 + float((rsd / 50) % 150)
			var rsz: float = 1.4 + float(rsd % 3)
			var rk := MeshInstance3D.new()
			var rm := SphereMesh.new(); rm.radius = rsz; rm.height = rsz * 1.5
			rk.mesh = rm
			rk.material_override = rockmat
			rk.position = origin + Vector3(rx, rsz * 0.35, rz)
			rk.scale.y = 0.7
			add_child(rk); game_nodes.append(rk)
			var rcap := MeshInstance3D.new()
			var rcm := SphereMesh.new(); rcm.radius = rsz * 0.85; rcm.height = rsz * 0.9
			rcap.mesh = rcm; rcap.material_override = snmat
			rcap.position = rk.position + Vector3(0, rsz * 0.32, 0); rcap.scale.y = 0.4
			add_child(rcap); game_nodes.append(rcap)
		# a wooden dock reaching out over the ice (somewhere to explore)
		var dmat := StandardMaterial3D.new()
		dmat.albedo_texture = load("res://assets/terrain/up_wood_col.jpg")
		dmat.normal_enabled = true
		dmat.normal_texture = load("res://assets/terrain/up_wood_nrm.jpg")
		dmat.uv1_triplanar = true; dmat.uv1_world_triplanar = true; dmat.uv1_scale = Vector3(0.15, 0.15, 0.15); dmat.roughness = 0.9
		var dock := _course_box(origin + Vector3(17.0, 1.1, 0.0), Vector3(30.0, 0.5, 6.0), Color(0.6, 0.44, 0.28))
		dock.material_override = dmat
		for dp in range(6):
			_course_box(origin + Vector3(4.0 + float(dp) * 6.0, 0.0, 3.2), Vector3(0.8, 2.2, 0.8), Color(0.4, 0.3, 0.2))
			_course_box(origin + Vector3(4.0 + float(dp) * 6.0, 0.0, -3.2), Vector3(0.8, 2.2, 0.8), Color(0.4, 0.3, 0.2))
		# a cleared path along the snowy shore
		var pth := _course_box(origin + Vector3(-27.0, 0.56, 0.0), Vector3(9.0, 0.1, 150.0), Color(0.82, 0.86, 0.92))
		pth.material_override.roughness = 1.0
		# Chuck waits on the snow - rigged 3D poodle (clips authored in tools/animate_chuck.py)
		var chuck_root := Node3D.new()
		chuck_root.position = origin + Vector3(-8, 0.5, -4)
		add_child(chuck_root)
		game_nodes.append(chuck_root)
		var pood: Node3D = (load("res://assets/characters/chuck_poodle_rigged.glb") as PackedScene).instantiate()
		pood.scale = Vector3.ONE * 1.5
		pood.position.y = 0.95 * 1.5
		chuck_root.add_child(pood)
		var chuck_ap: AnimationPlayer = pood.find_child("AnimationPlayer", true, false)
		for an in ["sit_idle", "sit_excited", "run", "wag"]:
			if chuck_ap.has_animation(an):
				chuck_ap.get_animation(an).loop_mode = Animation.LOOP_LINEAR
		g["chuck"] = chuck_root
		g["chuck_ap"] = chuck_ap
		g["home"] = chuck_root.position
		# aim arrow Roshan points while holding the ball
		var arrow := MeshInstance3D.new()
		var ab := PrismMesh.new()
		ab.size = Vector3(1.6, 2.6, 0.5)
		arrow.mesh = ab
		arrow.material_override = _soft_mat(Color(0.4, 1.0, 0.5), 0.9)
		add_child(arrow)
		game_nodes.append(arrow)
		g["arrow"] = arrow
		show_msg(fr["fname"], "Throw the ball for Chuck - but NOT into the lake! Press when the arrow is GREEN!")
	elif game == "dolls":
		g["spawned"] = 0
		g["caught"] = 0
		g["resolved"] = 0
		g["next"] = 0.6
		g["dolls"] = []
		g["timer"] = -1.0
		_dolls2d_open(fr)
		show_msg(fr["fname"], "Catch 3 sleepy dolls in your arms!")
	elif game == "seek":
		g["found"] = 0
		g["timer"] = 20.0
		g["bushes"] = []
		for i in range(4):
			var bush := MeshInstance3D.new()
			var bm3 := SphereMesh.new()
			bm3.radius = 2.4
			bm3.height = 3.4
			bush.mesh = bm3
			var bmat3 := StandardMaterial3D.new()
			bmat3.albedo_color = BTN_COLS[i] * 0.55 + Color(0.25, 0.45, 0.25)
			bmat3.albedo_texture = load("res://assets/terrain/up_grass_col.jpg")
			bmat3.uv1_triplanar = true
			bmat3.uv1_scale = Vector3(3.0, 3.0, 3.0)
			bmat3.normal_enabled = true
			bmat3.normal_texture = load("res://assets/terrain/scales_normal.png")
			bmat3.normal_scale = 1.0
			bmat3.roughness = 1.0
			bmat3.emission_enabled = true
			bmat3.emission = BTN_COLS[i] * 0.3
			bmat3.emission_energy_multiplier = 0.7
			bush.material_override = bmat3
			bush.position = origin + BTN_OFFS[i] + Vector3(0, 2.2, 0)
			add_child(bush)
			game_nodes.append(bush)
			(g["bushes"] as Array).append(bush)
		var lamb_ps: PackedScene = load("res://assets/characters/lamb.glb")
		var lamb: Node3D
		if lamb_ps != null:
			lamb = lamb_ps.instantiate()
			lamb.scale = Vector3.ONE * 2.6
			add_child(lamb)
			game_nodes.append(lamb)
		else:
			lamb = _game_ball(Color(1.0, 0.99, 0.95), 1.2)
		g["lamb"] = lamb
		_decorate_lamb_meadow(origin)
		_seek_hide()
		_melody_buttons_show(false)
		show_msg(fr["fname"], "Lamb-a' is playing in the meadow! Find her behind a wiggly bush!")
	elif game == "race":
		g["timer"] = 999.0
		g["checks"] = []
		g["chains"] = []
		_build_playplace(origin, fr)
		show_msg(fr["fname"], "Welcome to the play place! Touch the sparkles all the way up to the BIG slide!")
	elif game == "shop":
		g["timer"] = 999.0
		_build_shop_cabin(origin)
		player.position = origin + Vector3(0, 4, 9)
		player.vel = Vector3.ZERO
		player.yaw = PI
		show_msg("Pearl Shop", "Welcome aboard! Swim up to a treasure on the counter to buy it!")
	elif game == "treasure":
		g["timer"] = 999.0
		g["checks"] = []
		g["chains"] = []
		_build_cavern(origin)
		show_msg(fr["fname"], "Shhh... secret caverns! Follow the sparkles down to the treasure!")
	elif game == "melody":
		g["caught"] = 0
		g["orbs"] = []
		# the whole Gabby concert page is the stage backdrop
		var bd := MeshInstance3D.new()
		var qm := QuadMesh.new()
		qm.size = Vector2(46.0, 41.8)
		bd.mesh = qm
		var bdm := StandardMaterial3D.new()
		bdm.albedo_texture = load("res://assets/book/gabby_stage.jpg")
		bdm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		bd.material_override = bdm
		bd.position = origin + Vector3(0, 19.0, -15.0)
		add_child(bd)
		game_nodes.append(bd)
		# ---- 3D concert stage set dressing (rich, themed — like the fetch/seek worlds) ----
		var stage_f: float = ARENA_POS.y + 0.6
		var rcols := [Color(1.0, 0.2, 0.2), Color(1.0, 0.55, 0.15), Color(1.0, 0.9, 0.2), Color(0.25, 0.9, 0.3), Color(0.2, 0.55, 1.0), Color(0.35, 0.25, 0.9), Color(0.7, 0.3, 0.9)]
		# raised stage platform with a glowing edge
		var plat := _course_box(origin + Vector3(0, stage_f + 0.8, -8.0), Vector3(40, 1.6, 26), Color(0.18, 0.12, 0.28))
		plat.material_override.metallic = 0.4; plat.material_override.roughness = 0.3
		var edge := _course_box(origin + Vector3(0, stage_f + 1.7, -8.0), Vector3(41, 0.4, 27), Color(1.0, 0.3, 0.7))
		edge.material_override = _soft_mat(Color(1.0, 0.3, 0.7), 1.6)
		# big speaker stacks flanking the stage
		for sx in [-17.0, 17.0]:
			for sy in range(3):
				var spk := _course_box(origin + Vector3(sx, stage_f + 3.0 + float(sy) * 5.0, -12.0), Vector3(7, 4.6, 6), Color(0.08, 0.08, 0.1))
				spk.material_override.roughness = 0.8
				var cone := MeshInstance3D.new()
				var cmh := CylinderMesh.new(); cmh.top_radius = 2.2; cmh.bottom_radius = 0.6; cmh.height = 0.8
				cone.mesh = cmh
				cone.material_override = _soft_mat(Color(0.3, 0.3, 0.35), 0.1)
				cone.rotation_degrees = Vector3(90, 0, 0)
				cone.position = origin + Vector3(sx, stage_f + 3.0 + float(sy) * 5.0, -8.9)
				add_child(cone); game_nodes.append(cone)
		# overhead lighting truss with colored spotlights + beams
		var truss := _course_box(origin + Vector3(0, stage_f + 24.0, -10.0), Vector3(44, 1.0, 1.0), Color(0.2, 0.2, 0.22))
		truss.material_override.metallic = 0.6
		for li in range(5):
			var lx2: float = -18.0 + float(li) * 9.0
			var lc: Color = rcols[li % rcols.size()]
			var sl := OmniLight3D.new()
			sl.light_color = lc; sl.light_energy = 2.6; sl.omni_range = 26.0
			sl.position = origin + Vector3(lx2, stage_f + 22.0, -8.0)
			add_child(sl); game_nodes.append(sl)
			var beam := MeshInstance3D.new()
			var bcone := CylinderMesh.new(); bcone.top_radius = 0.4; bcone.bottom_radius = 5.0; bcone.height = 22.0
			beam.mesh = bcone
			var bmm := StandardMaterial3D.new()
			bmm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			bmm.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
			bmm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			bmm.albedo_color = Color(lc.r, lc.g, lc.b, 0.14)
			beam.material_override = bmm
			beam.position = origin + Vector3(lx2, stage_f + 12.0, -9.0)
			add_child(beam); game_nodes.append(beam)
		# floating music notes drifting over the crowd
		for ni in range(10):
			var note := Label3D.new()
			note.text = ["♪", "♫", "♩", "♬"][ni % 4]
			note.font_size = 120; note.modulate = rcols[ni % rcols.size()]
			note.outline_size = 10; note.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			note.position = origin + Vector3(randf() * 36.0 - 18.0, stage_f + 6.0 + randf() * 14.0, 2.0 + randf() * 12.0)
			add_child(note); game_nodes.append(note)
		var rainbow := rcols
		for i in range(7):
			var orb := MeshInstance3D.new()
			var sph := SphereMesh.new()
			sph.radius = 1.25
			sph.height = 2.5
			orb.mesh = sph
			var om := StandardMaterial3D.new()
			om.albedo_color = rainbow[i]
			om.emission_enabled = true
			om.emission = rainbow[i]
			om.emission_energy_multiplier = 1.5
			orb.material_override = om
			orb.position = origin + Vector3(-12.0 + float(i) * 4.0, 5.0 + fmod(float(i) * 2.7, 8.0), -6.0 + fmod(float(i) * 3.3, 12.0))
			add_child(orb)
			game_nodes.append(orb)
			var ov := Vector3(sin(float(i) * 2.1), sin(float(i) * 1.3) * 0.6, cos(float(i) * 1.7)).normalized() * (6.0 + float(i % 3) * 2.0)
			(g["orbs"] as Array).append({"node": orb, "vel": ov, "caught": false})
		show_msg(fr["fname"], "Catch all 7 colors of the rainbow! Swim into the bouncing orbs!")
	elif game == "slide":
		g["timer"] = -1.0   # no countdown — reaching the bottom ends it (~12s run)
		var theme: String = String(fr.get("theme", "ice"))
		var mode: String = String(fr.get("mode", "fish"))
		g["mode"] = mode
		_build_slide(origin, theme, mode)
		_play_music("fetch")   # reuse the snowy track
		if theme == "rainbow":
			arena_env.background_color = Color(0.72, 0.86, 1.0)
			arena_env.ambient_light_color = Color(1.0, 0.97, 1.0)
			arena_env.ambient_light_energy = 1.35
		if mode == "chase":
			show_msg(fr["fname"], "Race the baby penguin! Catch him before the bottom of the slide!")
		else:
			show_msg(fr["fname"], "Whooosh down the ice! Lean LEFT and RIGHT to grab all 5 fish!")
	elif game == "fairyshoot":
		g["timer"] = -1.0
		_build_fairyshoot(origin)
		_play_music("melody")   # dreamy track
		show_msg(fr["fname"], "Fly the fairy! Move to dodge, hold SPACE / TAP to zap the shadow bugs!")

# ===================== PENGUIN ICE SLIDE =====================
# A short N64-style downhill chute. Roshan slides on momentum (gravity along the
# slope); the player only steers left/right. 5 fish to grab, ~12 seconds.
const SLIDE_WIDTH := 18.0          # chute interior width
const SLIDE_GRAV := 44.0           # along-slope gravity pull
const SLIDE_FRICT := 0.32          # speed-proportional drag (sets terminal speed)
const SLIDE_VMAX := 26.0
const SLIDE_VMIN := 13.0           # keeps the flat finish from crawling
const SLIDE_STEER := 38.0          # lateral acceleration from steering
const SLIDE_RIDE := 2.2            # how far above the chute surface Roshan rides
const SLIDE_LEAD := 22.0           # baby penguin's head start (shrinks to 0 at the bottom)

func _ice_mat(col: Color, glow: float = 0.18) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = col
	m.metallic = 0.25
	m.roughness = 0.12
	m.emission_enabled = true
	m.emission = col * glow
	return m

func _slide_plank(a: Vector3, b: Vector3, width: float, mat: StandardMaterial3D, thick: float = 0.8) -> void:
	var mid: Vector3 = (a + b) * 0.5
	var dir: Vector3 = b - a
	var seg: float = dir.length()
	if seg < 0.001:
		return
	var fwd: Vector3 = dir / seg
	var right: Vector3 = Vector3.UP.cross(fwd)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	right = right.normalized()
	var up2: Vector3 = fwd.cross(right).normalized()
	var mi := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = Vector3(width, thick, seg)
	mi.mesh = bm
	mi.material_override = mat
	mi.transform = Transform3D(Basis(right, up2, fwd), mid)
	add_child(mi)
	game_nodes.append(mi)

func _aq_game(model: String, pos: Vector3, scl: float) -> Node3D:
	# spawn an aquatic model as a GAME object (freed with the arena, no flora_nodes leak)
	var ps := _aq(model)
	if ps == null:
		return null
	var inst: Node3D = ps.instantiate()
	inst.position = pos
	inst.scale = Vector3.ONE * scl
	_paint_aq(inst, _aq_mat(model))
	add_child(inst)
	game_nodes.append(inst)
	return inst

func _build_slide(origin: Vector3, theme: String = "ice", mode: String = "fish") -> void:
	# ---- centerline: an S-curve that descends, then flattens out at the bottom ----
	var path: Array = []
	var N := 26
	for i in range(N + 1):
		var t: float = float(i) / float(N)
		var z: float = lerp(-110.0, 120.0, t)
		var x: float = sin(t * TAU * 0.85) * 24.0
		# steep at the top (quick whoosh), easing flat near the bottom for a gentle finish
		var y: float = 2.0 + 48.0 * pow(1.0 - t, 1.2)
		path.append(origin + Vector3(x, y, z))
	g["path"] = path
	# precompute cumulative arc length
	var cum: Array = [0.0]
	var total := 0.0
	for i in range(path.size() - 1):
		total += (path[i + 1] - path[i]).length()
		cum.append(total)
	g["cum"] = cum
	g["total"] = total
	g["s"] = 0.0
	g["v"] = SLIDE_VMIN
	g["x"] = 0.0
	g["vx"] = 0.0
	g["got"] = 0
	g["caught"] = false
	# ---- build the chute: themed floor planks + glowing side rails ----
	var rainbow := [Color(1, 0.45, 0.5), Color(1, 0.7, 0.4), Color(1, 0.95, 0.45), Color(0.5, 0.9, 0.55), Color(0.45, 0.8, 1.0), Color(0.6, 0.55, 1.0), Color(0.9, 0.55, 0.95)]
	var rail := _ice_mat(Color(0.55, 0.8, 1.0), 0.5) if theme == "ice" else _ice_mat(Color(1.0, 0.9, 0.5), 0.6)
	for i in range(path.size() - 1):
		var a: Vector3 = path[i]
		var b: Vector3 = path[i + 1]
		var pmat: StandardMaterial3D = _ice_mat(rainbow[i % rainbow.size()], 0.35) if theme == "rainbow" else _ice_mat(Color(0.72, 0.9, 1.0))
		_slide_plank(a, b, SLIDE_WIDTH, pmat)
		# side rails sit on the chute edges
		var smp := _slide_dir(i)
		var rt: Vector3 = smp[1]
		_slide_plank(a + rt * (SLIDE_WIDTH * 0.5), b + rt * (SLIDE_WIDTH * 0.5), 1.4, rail, 4.0)
		_slide_plank(a - rt * (SLIDE_WIDTH * 0.5), b - rt * (SLIDE_WIDTH * 0.5), 1.4, rail, 4.0)
	# ---- penguins cheering on the banks ----
	for k in range(6):
		var tt: float = 0.12 + 0.72 * float(k) / 5.0
		var ps := _slide_sample(tt * total)
		var side: float = -1.0 if k % 2 == 0 else 1.0
		var peng := _aq_game("Penguin", ps[0] + ps[2] * (side * (SLIDE_WIDTH * 0.5 + 4.0)) + Vector3(0, 2.0, 0), 3.0)
		if peng != null:
			peng.rotation.y = atan2(-ps[1].x, -ps[1].z) + (0.4 if side > 0.0 else -0.4)
	g["fish"] = []
	if mode == "chase":
		# ---- the baby penguin you race + catch (positioned each frame in _tick_slide) ----
		var baby := _aq_game("Penguin", _slide_sample(40.0)[0] + Vector3(0, SLIDE_RIDE, 0), 2.2)
		g["peng_node"] = baby
		g["peng_x"] = 0.0
	else:
		# ---- 5 fish collectables, spaced along the run, alternating sides ----
		var spots := [0.16, 0.34, 0.52, 0.70, 0.86]
		var sides := [-1.0, 1.0, -0.4, 1.0, -1.0]
		for k in range(spots.size()):
			var samp := _slide_sample(float(spots[k]) * total)
			var fpos: Vector3 = samp[0] + samp[2] * (sides[k] * SLIDE_WIDTH * 0.32) + Vector3(0, SLIDE_RIDE + 1.6, 0)
			var fish := _aq_game("ClownFish", fpos, 3.0)
			if fish == null:
				fish = _check_star(fpos)   # fallback if the model is missing
			var halo := _halo(fpos, Color(1.0, 0.85, 0.4), 6.0)
			game_nodes.append(halo)
			(g["fish"] as Array).append({"node": fish, "halo": halo, "pos": fpos, "got": false})
		# ---- a big ball rolling behind, for the "chase" feel (decor only) ----
		var ball := MeshInstance3D.new()
		var bs := SphereMesh.new(); bs.radius = 7.0; bs.height = 14.0
		ball.mesh = bs
		ball.material_override = _ice_mat(Color(1.0, 0.85, 0.4), 0.5) if theme == "rainbow" else _ice_mat(Color(0.97, 0.99, 1.0), 0.05)
		add_child(ball); game_nodes.append(ball)
		g["ball"] = ball
	# ---- finish banner at the bottom ----
	var fin := _slide_sample(total)
	var banner := _course_box(fin[0] + Vector3(0, 9.0, 0), Vector3(SLIDE_WIDTH + 6.0, 1.6, 1.0), Color(1.0, 0.85, 0.35))
	banner.material_override = _ice_mat(Color(1.0, 0.85, 0.35), 0.6)
	for sx in [-1.0, 1.0]:
		_course_box(fin[0] + Vector3(sx * (SLIDE_WIDTH * 0.5 + 3.0), 4.5, 0), Vector3(1.2, 9.0, 1.2), Color(1.0, 0.8, 0.4))
	# ---- place Roshan at the top, facing down the chute ----
	var top := _slide_sample(0.0)
	player.position = top[0] + Vector3(0, SLIDE_RIDE, 0)
	player.vel = Vector3.ZERO
	player.yaw = atan2(top[1].x, top[1].z)

func _slide_dir(i: int) -> Array:
	# tangent + horizontal-right for segment i of the path
	var path: Array = g["path"]
	var j: int = clampi(i, 0, path.size() - 2)
	var fwd: Vector3 = (path[j + 1] - path[j]).normalized()
	var right: Vector3 = Vector3.UP.cross(fwd)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	return [fwd, right.normalized()]

func _slide_sample(s: float) -> Array:
	# returns [pos, tangent, right] at arc-length s along the chute
	var path: Array = g["path"]
	var cum: Array = g["cum"]
	var total: float = g["total"]
	s = clampf(s, 0.0, total)
	var i := 0
	while i < cum.size() - 2 and float(cum[i + 1]) < s:
		i += 1
	var seg_len: float = float(cum[i + 1]) - float(cum[i])
	var f: float = 0.0 if seg_len < 0.001 else (s - float(cum[i])) / seg_len
	var pos: Vector3 = (path[i] as Vector3).lerp(path[i + 1], f)
	var d: Array = _slide_dir(i)
	return [pos, d[0], d[1]]

func _tick_slide(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var total: float = g["total"]
	var s: float = g["s"]
	var samp := _slide_sample(s)
	var tangent: Vector3 = samp[1]
	var right: Vector3 = samp[2]
	# --- steering input (left/right only) ---
	var steer := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		steer -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		steer += 1.0
	var jx: float = Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
	if absf(jx) > 0.2:
		steer += jx
	if touch_ui != null and absf(touch_ui.stick_vec.x) > 0.15:
		steer += touch_ui.stick_vec.x
	steer = clampf(steer, -1.0, 1.0)
	# --- along-slope physics: gravity pulls down the gradient, drag caps speed ---
	var v: float = g["v"]
	var grade: float = -tangent.y          # >0 going downhill
	v += (SLIDE_GRAV * grade - SLIDE_FRICT * v) * delta
	v = clampf(v, SLIDE_VMIN, SLIDE_VMAX)
	g["v"] = v
	g["s"] = s + v * delta
	# --- lateral steering with damping + soft walls ---
	# (negated: the chase-cam looks down +tangent, so the chute's "right" vector
	#  is screen-left — flip so pressing right steers screen-right)
	var vx: float = g["vx"]
	vx -= steer * SLIDE_STEER * delta
	vx *= pow(0.02, delta)
	var x: float = float(g["x"]) + vx * delta
	var lim: float = SLIDE_WIDTH * 0.5 - 2.0
	if absf(x) > lim:
		x = clampf(x, -lim, lim)
		vx *= -0.3                         # gentle bounce off the ice banks
	g["x"] = x
	g["vx"] = vx
	# --- place + orient Roshan ---
	var pos: Vector3 = samp[0] + right * x + Vector3(0, SLIDE_RIDE, 0)
	player.position = pos
	player.yaw = atan2(tangent.x, tangent.z)
	player.rotation = Vector3(-0.35, player.yaw + PI, -clampf(vx * 0.02, -0.5, 0.5))
	# --- chase camera, locked behind and above ---
	if player.cam != null and player.cam.is_inside_tree():
		var cam_target: Vector3 = pos - tangent * 15.0 + Vector3(0, 7.0, 0)
		player.cam.position = player.cam.position.lerp(cam_target, 1.0 - pow(0.0008, delta))
		player.cam.look_at(pos + tangent * 6.0 + Vector3(0, 1.0, 0))
	if String(g.get("mode", "fish")) == "chase":
		# ===== RACE THE BABY PENGUIN =====
		# He leads far ahead, then "tires" so he's catchable for the final ~5 seconds.
		var p: float = s / total
		# the baby penguin keeps a head start that shrinks STEADILY the whole way down,
		# so Roshan is always gaining on him (no stall) — he comes into catch range for
		# roughly the last 5 seconds, where you must corner him to win.
		var gap: float = SLIDE_LEAD * (1.0 - p)
		var peng_s: float = minf(s + gap, total)
		# he FLEES sideways away from Roshan (slower than she can steer), pinned by the
		# chute walls — so a passive player never catches him; you must corner him.
		var px: float = float(g.get("peng_x", 0.0))
		var flee_dir: float = signf(px - x)
		if flee_dir == 0.0:
			flee_dir = 1.0 if sin(float(g["t"]) * 1.3) >= 0.0 else -1.0
		px += flee_dir * 7.5 * delta
		px += sin(float(g["t"]) * 2.5) * 1.2 * delta            # lively wander
		px = clampf(px, -lim, lim)
		g["peng_x"] = px
		var psamp := _slide_sample(peng_s)
		var pbpos: Vector3 = psamp[0] + psamp[2] * px + Vector3(0, SLIDE_RIDE, 0)
		var pnode = g.get("peng_node")
		if pnode != null and is_instance_valid(pnode):
			(pnode as Node3D).position = pbpos
			var wob: float = sin(float(g["t"]) * 9.0) * 0.18      # waddle
			(pnode as Node3D).rotation = Vector3(0, atan2(psamp[1].x, psamp[1].z) + PI, wob)
		# catch when you've cornered him during the window
		if not bool(g.get("caught", false)) and gap < 9.0 and absf(x - px) < 4.5:
			g["caught"] = true
			_sparkle_burst(pbpos + Vector3(0, 1.5, 0), Color(1.0, 0.9, 0.4))
			if chime != null:
				chime.pitch_scale = 1.5; chime.play()
			_end_game(true, fr, "You caught the baby penguin! Hee hee, great race!")
			return
		hud_game.text = "Catch the baby penguin!" if p < 0.58 else "NOW!  Catch him!   ← →"
		if float(g["s"]) >= total - 0.5:
			_end_game(false, fr, "Aww, the baby penguin slid away! Race again?", "fail")
			return
	else:
		# ===== COLLECT THE FISH =====
		# rolling chase snowball behind (decor)
		if g.has("ball") and is_instance_valid(g["ball"]):
			var bsamp := _slide_sample(maxf(0.0, s - 26.0))
			(g["ball"] as Node3D).position = bsamp[0] + Vector3(0, 5.0, 0)
			(g["ball"] as Node3D).rotate_x(delta * 3.0)
		for fd in g.get("fish", []):
			if fd["got"]:
				continue
			if (fd["pos"] as Vector3).distance_to(pos) < 4.2:
				fd["got"] = true
				g["got"] = int(g["got"]) + 1
				var fn: Node = fd["node"]
				if is_instance_valid(fn):
					fn.queue_free()
				var fh: Node = fd["halo"]
				if is_instance_valid(fh):
					fh.queue_free()
				_sparkle_burst(pos + Vector3(0, 1.5, 0), Color(1.0, 0.85, 0.4))
				if chime != null:
					chime.pitch_scale = 1.0 + 0.12 * float(g["got"])
					chime.play()
		hud_game.text = "Slide!  Fish: %d / 5" % int(g["got"])
		if float(g["s"]) >= total - 0.5:
			var got: int = int(g["got"])
			var msg := "WHEEE! You grabbed every fish! Best slider ever!" if got >= 5 else "What a ride! You caught %d fish!" % got
			_end_game(true, fr, msg)

# ===================== FAIRY POND — ON-RAILS SHOOTER =====================
# A tribute to the N64 space-fox rail shooter: Roshan flies as the fairy through a
# dreamy pond corridor, dodging with free 2D movement and zapping shadow bugs.
const FS_LEN := 520.0          # corridor length (forward, +Z)
const FS_FWD := 30.0           # auto-forward speed (gentler for little ones)
const FS_MOVE := 34.0          # lateral / vertical steering speed
const FS_BX := 20.0            # half movement bound (x)
const FS_BY := 10.0            # half movement bound (y)
const FS_BASE_Y := 13.0        # flight height above the pond
const FS_BOLT := 150.0         # laser bolt speed
const FS_FIRE_CD := 0.14
const FS_HIT_R := 7.0          # big, forgiving bolt-vs-bug radius
const FS_BUG_R := 3.2          # bigger shadow bugs (easier to see + hit)
const FS_NBUGS := 12
# ---- final boss: the Fairy Flower (auto-shooter, gentle difficulty) ----
const FS_BOSS_Z := FS_LEN + 34.0   # boss sits just past the end of the run
const FS_BOSS_HIT_R := 8.5         # generous hitboxes
const FS_LEAVES := 6               # outer leaf shield
const FS_LEAF_HP := 1              # one blast per leaf
const FS_LEAF_T := 18.0            # seconds to blast the leaves away
const FS_LEAF_RING := 7.5          # leaf ring radius (just beyond bolt reach -> light aiming)
const FS_BUD_HP := 10
const FS_BUD_T := 18.0             # seconds to bloom the flower open
const FS_BLOOM_T := 3.0
const FS_LEAF_SCALE := 6.5         # real Kenney bush models (CC0)
const FS_BUD_SCALE := 9.0
const FS_FLOWER := "flower_purpleA"  # ONE flower for the whole boss (grows, then blooms)

func _build_fairyshoot(origin: Vector3) -> void:
	# Roshan wears her fairy form for this game only
	player.set_skin("fairy", FAIRY_SKIN_PATH)
	g["fz"] = 0.0; g["ox"] = 0.0; g["oy"] = 0.0
	g["hits"] = 0; g["fire_cd"] = 0.0
	g["targets"] = []; g["bolts"] = []; g["fireflies"] = []
	g["phase"] = "fly"; g["leaves"] = []; g["bud"] = null; g["petals"] = []
	# ---- the dreamy pond below ----
	var pond := MeshInstance3D.new()
	var pm := BoxMesh.new(); pm.size = Vector3(90.0, 1.0, FS_LEN + 160.0)
	pond.mesh = pm
	var pmat := StandardMaterial3D.new()
	pmat.albedo_color = Color(0.2, 0.35, 0.55)
	pmat.metallic = 0.7; pmat.roughness = 0.1
	pmat.emission_enabled = true; pmat.emission = Color(0.15, 0.3, 0.5); pmat.emission_energy_multiplier = 0.25
	pond.material_override = pmat
	pond.position = origin + Vector3(0, 0.0, FS_LEN * 0.5)
	add_child(pond); game_nodes.append(pond)
	# ---- lily pads + glowing reeds on the banks ----
	for i in range(18):
		var z: float = 20.0 + randf() * FS_LEN
		var side: float = -1.0 if i % 2 == 0 else 1.0
		var pad := MeshInstance3D.new()
		var cm := CylinderMesh.new(); cm.top_radius = 2.5 + randf() * 2.0; cm.bottom_radius = cm.top_radius; cm.height = 0.3
		pad.mesh = cm
		pad.material_override = _soft_mat(Color(0.3, 0.7, 0.4), 0.2)
		pad.position = origin + Vector3(side * (12.0 + randf() * 26.0), 0.8, z)
		add_child(pad); game_nodes.append(pad)
		if i % 3 == 0:   # a glowing flower on some pads
			var fl := MeshInstance3D.new()
			var fs := SphereMesh.new(); fs.radius = 1.0; fs.height = 2.0
			fl.mesh = fs
			fl.material_override = _soft_mat(Color(1.0, 0.6, 0.85), 1.4)
			fl.position = pad.position + Vector3(0, 1.0, 0)
			add_child(fl); game_nodes.append(fl)
	# ---- glowing fairy-ring gates to fly through (decor homage) ----
	for k in range(6):
		var z2: float = 70.0 + float(k) * 78.0
		var ring := MeshInstance3D.new()
		var tor := TorusMesh.new(); tor.inner_radius = 13.5; tor.outer_radius = 15.0; tor.rings = 24; tor.ring_segments = 12
		ring.mesh = tor
		var rcol := Color.from_hsv(fmod(float(k) * 0.16, 1.0), 0.5, 1.0)
		ring.material_override = _soft_mat(rcol, 1.6)
		ring.position = origin + Vector3(0, FS_BASE_Y, z2)
		ring.rotation_degrees = Vector3(90, 0, 0)   # stand the ring up so its opening faces the player to fly through
		add_child(ring); game_nodes.append(ring)
	# ---- drifting fireflies ----
	for i in range(24):
		var ff := MeshInstance3D.new()
		var fm := SphereMesh.new(); fm.radius = 0.3; fm.height = 0.6
		ff.mesh = fm
		ff.material_override = _soft_mat(Color(1.0, 0.95, 0.6), 3.0)
		ff.position = origin + Vector3(randf() * 60.0 - 30.0, 4.0 + randf() * 22.0, 20.0 + randf() * FS_LEN)
		add_child(ff); game_nodes.append(ff)
		(g["fireflies"] as Array).append({"node": ff, "ph": randf() * TAU, "base": ff.position})
	# ---- shadow bugs to zap ----
	for k in range(FS_NBUGS):
		var z3: float = 80.0 + float(k) / float(FS_NBUGS) * (FS_LEN - 120.0) + randf() * 18.0
		var bx: float = (randf() * 2.0 - 1.0) * (FS_BX - 3.0)
		var by: float = (randf() * 2.0 - 1.0) * (FS_BY - 2.0)
		var bug := MeshInstance3D.new()
		var sm := SphereMesh.new(); sm.radius = FS_BUG_R; sm.height = FS_BUG_R * 2.0
		bug.mesh = sm
		var bmat := StandardMaterial3D.new()
		bmat.albedo_color = Color(0.22, 0.05, 0.3)
		bmat.emission_enabled = true; bmat.emission = Color(0.85, 0.2, 0.55); bmat.emission_energy_multiplier = 1.5
		bug.material_override = bmat
		var bpos: Vector3 = origin + Vector3(bx, FS_BASE_Y + by, z3)
		bug.position = bpos
		add_child(bug); game_nodes.append(bug)
		(g["targets"] as Array).append({"node": bug, "pos": bpos, "alive": true, "ph": randf() * TAU})
	# ---- aiming reticle ----
	var ret := MeshInstance3D.new()
	var rt := TorusMesh.new(); rt.inner_radius = 1.1; rt.outer_radius = 1.5; rt.rings = 16; rt.ring_segments = 8
	ret.mesh = rt
	ret.material_override = _soft_mat(Color(1.0, 0.9, 0.4), 2.5)
	add_child(ret); game_nodes.append(ret)
	g["reticle"] = ret
	# ---- place Roshan at the corridor start ----
	player.position = origin + Vector3(0, FS_BASE_Y, 0)
	player.vel = Vector3.ZERO

func _fairy_start_boss(origin: Vector3) -> void:
	# Built from real CC0 Kenney flora models (assets/nature) — minimal custom geometry.
	var center: Vector3 = origin + Vector3(0, FS_BASE_Y, FS_BOSS_Z)
	g["boss_center"] = center
	g["phase"] = "boss_leaves"
	g["phase_t"] = FS_LEAF_T
	# leafy stalk base (a big bush model)
	if _nature("plant_bushLargeTriangle", center + Vector3(0, -15.0, 1.0), 11.0, 0.0) == null:
		var stalk := _course_box(center + Vector3(0, -15.0, 0), Vector3(4, 26, 4), Color(0.3, 0.65, 0.35))
		_mg_noop_ref(stalk)
	# the flower at the core — ONE flower (FS_FLOWER), small/tight until the leaves fall,
	# then it grows bigger with every hit before blooming
	var bud := _nature(FS_FLOWER, center + Vector3(0, -4.0, 0), FS_BUD_SCALE * 0.4, 0.0)
	if bud == null:
		var bm := MeshInstance3D.new()
		var bsm := SphereMesh.new(); bsm.radius = 4.5; bsm.height = 9.0
		bm.mesh = bsm; bm.material_override = _soft_mat(Color(0.85, 0.45, 0.7), 0.5)
		bm.position = center; bm.scale = Vector3.ONE * (FS_BUD_SCALE * 0.4)
		add_child(bm); game_nodes.append(bm); bud = bm
	g["bud"] = bud
	g["bud_hp"] = FS_BUD_HP
	# leaf shield: a wreath of real leafy bushes, ringed just beyond the bolt reach
	# so a little light steering is needed
	g["leaves"] = []
	var leafkinds := ["plant_bushLargeTriangle", "grass_leafsLarge", "plant_bush"]
	for k in range(FS_LEAVES):
		var a: float = float(k) / float(FS_LEAVES) * TAU
		var lp: Vector3 = center + Vector3(cos(a) * FS_LEAF_RING, sin(a) * FS_LEAF_RING, -1.0)
		var leaf := _nature(leafkinds[k % leafkinds.size()], lp, FS_LEAF_SCALE, randf() * TAU)
		if leaf == null:
			var lm := MeshInstance3D.new()
			var pm := PrismMesh.new(); pm.size = Vector3(5.0, 9.0, 2.0)
			lm.mesh = pm; lm.material_override = _soft_mat(Color(0.35, 0.75, 0.4), 0.4)
			lm.position = lp; add_child(lm); game_nodes.append(lm); leaf = lm
		(g["leaves"] as Array).append({"node": leaf, "hp": FS_LEAF_HP, "ang": a, "base": lp})
	var bl := OmniLight3D.new()
	bl.light_color = Color(1.0, 0.7, 0.85); bl.light_energy = 2.6; bl.omni_range = 44.0
	bl.position = center; add_child(bl); game_nodes.append(bl)
	g["boss_light"] = bl
	show_msg(fr_name_safe(), "The Fairy Flower! Blast the leaves out of the way!")

func fr_name_safe() -> String:
	return String((g.get("fr", {}) as Dictionary).get("fname", "Fairy Pond"))

func _fairy_bloom_start() -> void:
	g["phase"] = "boss_bloom"
	g["bloom_t"] = FS_BLOOM_T
	var center: Vector3 = g["boss_center"]
	g["petals"] = []
	# the blossom is a ring of the SAME flower opening outward (one coherent flower)
	for k in range(8):
		var a: float = float(k) / 8.0 * TAU
		var petal := _nature(FS_FLOWER, center, 0.5, a)
		if petal == null:
			var pm := MeshInstance3D.new()
			var sp := SphereMesh.new(); sp.radius = 2.4; sp.height = 4.8
			pm.mesh = sp; pm.material_override = _soft_mat(Color(1.0, 0.6, 0.8), 1.2)
			pm.position = center; add_child(pm); game_nodes.append(pm); petal = pm
		(g["petals"] as Array).append({"node": petal, "ang": a})

func _tick_fairyshoot(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var origin: Vector3 = ARENA_POS
	var phase: String = String(g.get("phase", "fly"))
	if phase == "fly":
		g["fz"] = float(g["fz"]) + FS_FWD * delta
	var fz: float = g["fz"]
	# ---- steering input (free 2D), x negated so 'right' reads screen-right ----
	var inx := 0.0
	var iny := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		inx -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		inx += 1.0
	if Input.is_physical_key_pressed(KEY_UP) or Input.is_physical_key_pressed(KEY_W):
		iny += 1.0
	if Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S):
		iny -= 1.0
	var jx: float = Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
	var jy: float = Input.get_joy_axis(0, JOY_AXIS_LEFT_Y)
	if absf(jx) > 0.2: inx += jx
	if absf(jy) > 0.2: iny -= jy
	if touch_ui != null:
		if absf(touch_ui.stick_vec.x) > 0.15: inx += touch_ui.stick_vec.x
		if absf(touch_ui.stick_vec.y) > 0.15: iny -= touch_ui.stick_vec.y
	var ox: float = clampf(float(g["ox"]) - inx * FS_MOVE * delta, -FS_BX, FS_BX)
	var oy: float = clampf(float(g["oy"]) + iny * FS_MOVE * delta, -FS_BY, FS_BY)
	g["ox"] = ox; g["oy"] = oy
	var pos: Vector3 = origin + Vector3(ox, FS_BASE_Y + oy, fz)
	player.position = pos
	# ---- chase camera, locked behind ----
	if player.cam != null and player.cam.is_inside_tree():
		var campos := Vector3(origin.x + ox * 0.4, origin.y + FS_BASE_Y + 5.0 + oy * 0.3, pos.z - 16.0)
		player.cam.position = player.cam.position.lerp(campos, 1.0 - pow(0.0006, delta))
		player.cam.look_at(pos + Vector3(0, 0.5, 26.0))
	# ---- reticle ahead of the player ----
	if g.has("reticle") and is_instance_valid(g["reticle"]):
		(g["reticle"] as Node3D).position = pos + Vector3(0, 0, 34.0)
	# ---- firing (auto-shooter: bolts fire on their own; you just aim by moving) ----
	g["fire_cd"] = maxf(0.0, float(g["fire_cd"]) - delta)
	if float(g["fire_cd"]) <= 0.0:
		g["fire_cd"] = FS_FIRE_CD
		var bolt := MeshInstance3D.new()
		var bsm := SphereMesh.new(); bsm.radius = 0.6; bsm.height = 1.2
		bolt.mesh = bsm
		bolt.material_override = _soft_mat(Color(0.6, 1.0, 0.9), 3.0)
		bolt.position = pos + Vector3(0, 0, 3.0)
		add_child(bolt); game_nodes.append(bolt)
		(g["bolts"] as Array).append({"node": bolt})
		if chime != null:
			chime.pitch_scale = 1.8; chime.play()
	# ---- advance bolts, check hits ----
	var bolts: Array = g["bolts"]
	for bi in range(bolts.size() - 1, -1, -1):
		var bd: Dictionary = bolts[bi]
		var bn: Node3D = bd["node"]
		if not is_instance_valid(bn):
			bolts.remove_at(bi); continue
		bn.position.z += FS_BOLT * delta
		var dead := bn.position.z > pos.z + 280.0
		for td in g["targets"]:
			if not td["alive"]:
				continue
			if bn.position.distance_to(td["node"].position) < FS_HIT_R:
				td["alive"] = false
				g["hits"] = int(g["hits"]) + 1
				var tn: Node = td["node"]
				_sparkle_burst((tn as Node3D).position, Color(1.0, 0.5, 0.7))
				if is_instance_valid(tn): tn.queue_free()
				if chime != null:
					chime.pitch_scale = 1.2; chime.play()
				dead = true
				break
		# boss: leaf shield
		if not dead and phase == "boss_leaves":
			for lf in g["leaves"]:
				if int(lf["hp"]) <= 0 or not is_instance_valid(lf["node"]):
					continue
				if bn.position.distance_to((lf["node"] as Node3D).position) < FS_BOSS_HIT_R:
					lf["hp"] = int(lf["hp"]) - 1
					_sparkle_burst((lf["node"] as Node3D).position, Color(0.5, 1.0, 0.5))
					if int(lf["hp"]) <= 0:
						(lf["node"] as Node3D).queue_free()
						if chime != null: chime.pitch_scale = 1.4; chime.play()
					dead = true
					break
		# boss: flower bud
		if not dead and phase == "boss_bud" and g.get("bud") != null and is_instance_valid(g["bud"]):
			if bn.position.distance_to((g["bud"] as Node3D).position) < FS_BOSS_HIT_R + 1.0:
				g["bud_hp"] = int(g["bud_hp"]) - 1
				_sparkle_burst((g["bud"] as Node3D).position + Vector3(randf() * 4 - 2, randf() * 4 - 2, 0), Color(1.0, 0.7, 0.85))
				if chime != null: chime.pitch_scale = 1.1 + 0.02 * float(FS_BUD_HP - int(g["bud_hp"])); chime.play()
				dead = true
		if dead:
			bn.queue_free(); bolts.remove_at(bi)
	# ---- bug + firefly idle motion ----
	var tt: float = float(g["t"])
	for td in g["targets"]:
		if td["alive"] and is_instance_valid(td["node"]):
			(td["node"] as Node3D).position.y = (td["pos"] as Vector3).y + sin(tt * 2.0 + float(td["ph"])) * 0.8
	for ff in g["fireflies"]:
		if is_instance_valid(ff["node"]):
			var b: Vector3 = ff["base"]
			(ff["node"] as Node3D).position = b + Vector3(sin(tt * 1.3 + float(ff["ph"])) * 2.0, cos(tt * 1.1 + float(ff["ph"])) * 1.5, 0)
	# ---- phase logic ----
	if phase == "fly":
		hud_game.text = "Fairy Pond!  Shadow bugs zapped: %d / %d" % [int(g["hits"]), FS_NBUGS]
		if fz >= FS_LEN:
			_fairy_start_boss(origin)
		return
	g["phase_t"] = float(g.get("phase_t", 0.0)) - delta
	var pt: float = maxf(0.0, float(g["phase_t"]))
	if phase == "boss_leaves":
		var left := 0
		for lf in g["leaves"]:
			if int(lf["hp"]) > 0:
				left += 1
			elif is_instance_valid(lf.get("node")):
				pass
		# rustle surviving leaves (gentle scale pulse — keeps the GLB bushes upright)
		for lf in g["leaves"]:
			if int(lf["hp"]) > 0 and is_instance_valid(lf["node"]):
				(lf["node"] as Node3D).scale = Vector3.ONE * (FS_LEAF_SCALE * (1.0 + sin(tt * 4.0 + float(lf["ang"])) * 0.06))
		hud_game.text = "Blast the leaves away!   leaves left: %d   ⏱ %d" % [left, int(ceil(pt))]
		if left <= 0:
			g["phase"] = "boss_bud"
			g["phase_t"] = FS_BUD_T
			if g.get("bud") != null and is_instance_valid(g["bud"]):
				(g["bud"] as Node3D).scale = Vector3.ONE * (FS_BUD_SCALE * 0.5)
			show_msg(fr_name_safe(), "The flower! Keep blasting to make it grow and bloom!")
		elif pt <= 0.0:
			_end_game(false, fr, "Oh no — the flower stayed shut! Fly back and try again!", "fail")
		return
	if phase == "boss_bud":
		var hp: int = int(g["bud_hp"])
		var bud: Node3D = g.get("bud")
		if bud != null and is_instance_valid(bud):
			# the flower GROWS bigger with every hit (0.5x -> 1.4x), plus a gentle pulse
			var grown: float = lerpf(0.5, 1.4, clampf(1.0 - float(hp) / float(FS_BUD_HP), 0.0, 1.0))
			var pulse: float = 1.0 + sin(tt * 8.0) * 0.05
			bud.scale = Vector3.ONE * (FS_BUD_SCALE * grown * pulse)
		hud_game.text = "Open the flower!   %d hits left   ⏱ %d" % [maxi(0, hp), int(ceil(pt))]
		if hp <= 0:
			_fairy_bloom_start()
			show_msg(fr_name_safe(), "It's blooming! 🌸")
		elif pt <= 0.0:
			_end_game(false, fr, "Oh no — the flower stayed shut! Fly back and try again!", "fail")
		return
	if phase == "boss_bloom":
		g["bloom_t"] = float(g.get("bloom_t", 0.0)) - delta
		var f: float = clampf(1.0 - float(g["bloom_t"]) / FS_BLOOM_T, 0.0, 1.0)
		var center: Vector3 = g["boss_center"]
		if g.get("bud") != null and is_instance_valid(g["bud"]):
			(g["bud"] as Node3D).scale = Vector3.ONE * (FS_BUD_SCALE * (1.0 - f * 0.55))
		for pd in g.get("petals", []):
			if is_instance_valid(pd["node"]):
				var a: float = pd["ang"]
				var r: float = 3.0 + f * 9.0
				(pd["node"] as Node3D).position = center + Vector3(cos(a) * r, sin(a) * r, 0)
				(pd["node"] as Node3D).scale = Vector3.ONE * (1.0 + f * 6.0)
		if fmod(tt, 0.18) < delta:
			_sparkle_burst(center + Vector3(randf() * 16 - 8, randf() * 16 - 8, 0), Color.from_hsv(randf(), 0.4, 1.0))
		if float(g["bloom_t"]) <= 0.0:
			_end_game(true, fr, "The Fairy Flower blossomed! You did it!")
		return

func _build_slide_portal() -> void:
	# a penguin on a floating ice floe in the reef — swim up to it to start the slide
	slide_portal_pos = Vector3(80.0, WATER_TOP - 20.0, -70.0)
	var floe := MeshInstance3D.new()
	var fm := CylinderMesh.new(); fm.top_radius = 11.0; fm.bottom_radius = 8.5; fm.height = 3.0
	floe.mesh = fm
	floe.material_override = _ice_mat(Color(0.86, 0.95, 1.0), 0.08)
	floe.position = slide_portal_pos + Vector3(0, -2.0, 0)
	add_child(floe)
	var peng := _place_aq("Penguin", slide_portal_pos + Vector3(0, 1.4, 0), 4.2, false)
	if peng != null:
		slide_portal_penguin = peng
	_halo(slide_portal_pos + Vector3(0, 3, 0), Color(0.6, 0.9, 1.0), 15.0)
	var l := OmniLight3D.new()
	l.light_color = Color(0.7, 0.9, 1.0); l.light_energy = 2.2; l.omni_range = 24.0
	l.position = slide_portal_pos + Vector3(0, 6, 0); add_child(l)
	var lab := Label3D.new()
	lab.text = "🐧 Penguin Slide!"
	lab.font_size = 64; lab.pixel_size = 0.04; lab.outline_size = 14
	lab.modulate = Color(0.75, 0.95, 1.0); lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lab.position = slide_portal_pos + Vector3(0, 9, 0); add_child(lab)

func _decorate_lamb_meadow(origin: Vector3) -> void:
	# a soft rolling green meadow for Lamb-a' to play in
	var hill := MeshInstance3D.new()
	var hs := SphereMesh.new()
	hs.radius = 60.0
	hs.height = 120.0
	hill.mesh = hs
	var hm := StandardMaterial3D.new()
	hm.albedo_texture = load("res://assets/terrain/up_grass_col.jpg")
	hm.albedo_color = Color(0.92, 1.0, 0.9)
	hm.normal_enabled = true
	hm.normal_texture = load("res://assets/terrain/up_grass_nrm.jpg")
	hm.uv1_triplanar = true
	hm.uv1_world_triplanar = true
	hm.uv1_scale = Vector3(0.05, 0.05, 0.05)
	hm.roughness = 1.0
	hill.material_override = hm
	hill.position = origin + Vector3(0, -56.0, 0)
	add_child(hill)
	game_nodes.append(hill)
	# scattered living things around the play circle (kept clear of the bushes)
	var trees := ["tree_palm", "tree_pineRoundF", "tree_default_fall", "tree_simple_fall", "tree_fat"]
	var flowers := ["flower_redA", "flower_yellowB", "flower_purpleA"]
	var seed := 11
	for k in range(40):
		seed = (seed * 1103515245 + 12345) & 0x7fffffff
		var ang: float = float(seed % 1000) / 1000.0 * TAU
		var rad: float = 16.0 + float((seed / 1000) % 1000) / 1000.0 * 26.0
		var gp := origin + Vector3(cos(ang) * rad, 1.0, sin(ang) * rad)
		var pick := (seed / 7) % 10
		var yr := float(seed % 628) / 100.0
		if pick < 3:
			_nature(trees[(seed / 13) % trees.size()], gp, 4.5 + float(seed % 3), yr)
		elif pick < 5:
			_nature("plant_bushLargeTriangle", gp, 4.0, yr)
		elif pick < 6:
			_nature("mushroom_red", gp, 4.0, yr)
		elif pick < 7:
			_nature("mushroom_tanGroup", gp, 4.5, yr)
		elif pick < 8:
			_nature("grass_leafsLarge", gp, 3.5, yr)
		else:
			_nature(flowers[(seed / 17) % flowers.size()], gp, 4.5, yr)
	# a couple of fluffy clouds + a warm sun glow
	for c in range(5):
		var cl := MeshInstance3D.new()
		var cs := SphereMesh.new()
		cs.radius = 5.0 + randf() * 4.0
		cs.height = 7.0
		cl.mesh = cs
		var cmat := StandardMaterial3D.new()
		cmat.albedo_color = Color(1, 1, 1)
		cmat.roughness = 1.0
		cl.material_override = cmat
		cl.position = origin + Vector3(randf() * 70.0 - 35.0, 28.0 + randf() * 10.0, randf() * 70.0 - 35.0)
		cl.scale = Vector3(1.8, 0.6, 1.4)
		add_child(cl)
		game_nodes.append(cl)
	var sun := OmniLight3D.new()
	sun.light_color = Color(1.0, 0.95, 0.8)
	sun.light_energy = 1.6
	sun.omni_range = 70.0
	sun.position = origin + Vector3(18, 30, 12)
	add_child(sun)
	game_nodes.append(sun)

func _seek_hide() -> void:
	g["which"] = randi() % 4
	var bush: MeshInstance3D = (g["bushes"] as Array)[int(g["which"])]
	(g["lamb"] as Node3D).position = bush.position + Vector3(0, 0.5, -2.2)
	(g["lamb"] as Node3D).rotation.y = 0.0
	var tw := create_tween().set_loops(8)
	tw.tween_property(bush, "scale", Vector3(1.35, 0.75, 1.35), 0.16)
	tw.tween_property(bush, "scale", Vector3.ONE, 0.16)

var melody_ui: Control
var melody_btns: Array = []
var melody_pressed := -1

func _melody_buttons_show(on: bool) -> void:
	if melody_ui == null:
		melody_ui = Control.new()
		melody_ui.set_anchors_preset(Control.PRESET_FULL_RECT)
		var cl2 := CanvasLayer.new()
		cl2.layer = 5
		add_child(cl2)
		cl2.add_child(melody_ui)
		var center := Vector2(1100, 540)
		var offs := [Vector2(0, 105), Vector2(105, 0), Vector2(-105, 0), Vector2(0, -105)]   # A B X Y diamond
		var labels := ["A", "B", "X", "Y"]
		for i in range(4):
			var b := Button.new()
			b.text = labels[i]
			b.custom_minimum_size = Vector2(110, 110)
			b.position = center + offs[i] - Vector2(55, 55)
			b.add_theme_font_size_override("font_size", 40)
			var sb := StyleBoxFlat.new()
			sb.bg_color = BTN_COLS[i] * 0.8
			sb.corner_radius_top_left = 55
			sb.corner_radius_top_right = 55
			sb.corner_radius_bottom_left = 55
			sb.corner_radius_bottom_right = 55
			b.add_theme_stylebox_override("normal", sb)
			var idx := i
			b.pressed.connect(func(): melody_pressed = idx)
			melody_ui.add_child(b)
			melody_btns.append(b)
	melody_ui.visible = on
	melody_pressed = -1

func _tick_game(delta: float) -> void:
	var fr: Dictionary = g["fr"]
	g["t"] = float(g["t"]) + delta
	if float(g["timer"]) > 0.0:
		g["timer"] = float(g["timer"]) - delta
		if float(g["timer"]) <= 0.0:
			_end_game(false, fr, _fail_line(), "fail")
			return
	var ppos: Vector3 = player.position
	if game == "fetch":
		_tick_fetch(delta, fr, ppos)
	elif game == "dolls":
		_tick_dolls(delta, fr, ppos)
	elif game == "seek":
		hud_game.text = "Find Lamb-a'! %d / 4   %ds" % [int(g["found"]), int(g["timer"])]
		var which: int = int(g.get("which", 0))
		var bush: MeshInstance3D = (g["bushes"] as Array)[which]
		var hit: bool = _btn_pressed() == which or melody_pressed == which or bush.position.distance_to(ppos) < 4.0
		melody_pressed = -1
		if hit:
			g["found"] = int(g["found"]) + 1
			var lamb2: Node3D = g["lamb"]
			lamb2.position = bush.position + Vector3(0, 4.8, 0)
			var twl := create_tween()
			twl.tween_property(lamb2, "scale", Vector3.ONE * 3.4, 0.2)
			twl.tween_property(lamb2, "scale", Vector3.ONE * 2.6, 0.3)
			if voice != null:
				voice.pitch_scale = 1.0 + randf() * 0.3
				voice.play()
			if int(g["found"]) >= 4:
				_end_game(true, fr, "You found Lamb-a' every time! Best seeker ever!")
				return
			_seek_hide()
	elif game == "race" or game == "treasure":
		_tick_course(delta, fr, ppos)
	elif game == "shop":
		_tick_shop(delta, fr, ppos)
	elif game == "melody":
		_tick_melody(delta, fr, ppos)
	elif game == "slide":
		_tick_slide(delta, fr, ppos)
	elif game == "fairyshoot":
		_tick_fairyshoot(delta, fr, ppos)

func _chuck_play(anim: String, blend: float = 0.25) -> void:
	var ap: AnimationPlayer = g["chuck_ap"]
	if ap != null and ap.has_animation(anim) and ap.current_animation != anim:
		ap.play(anim, blend)

func _tick_fetch(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	var ball: MeshInstance3D = g["ball"]
	var chuck: Node3D = g["chuck"]
	if String(g["phase"]) == "aim" or String(g["phase"]) == "fly":
		# Chuck SITS on the snow, watching Roshan (the ball, once it flies)
		var watch: Vector3 = (ball.position if String(g["phase"]) == "fly" else ppos) - chuck.position
		if Vector2(watch.x, watch.z).length() > 0.1:
			chuck.rotation.y = atan2(watch.x, watch.z)
		_chuck_play("sit_excited" if String(g["phase"]) == "fly" else "sit_idle", 0.35)
	if String(g["phase"]) == "aim":
		hud_game.text = "Throw %d / 2   (oops: %d / 2)" % [int(g["round"]) + 1, int(g["miss"])]
		# Roshan HOLDS the ball
		var fdir := Vector3(sin(player.yaw + PI), 0, cos(player.yaw + PI))
		ball.position = ppos + fdir * 1.3 + Vector3(0, -0.2, 0)
		# sweeping aim
		var sw: float = sin(float(g["t"]) * 1.5) * 1.25
		var dirv := Vector3(sin(sw), 0, -cos(sw))
		g["aim_dir"] = dirv
		var arrow: MeshInstance3D = g["arrow"]
		arrow.position = ppos + dirv * 3.2
		arrow.look_at(ppos + dirv * 9.0, Vector3.UP)
		arrow.rotation.x = -PI * 0.5
		var landing: Vector3 = ppos + dirv * 14.0
		var wet: bool = landing.x - ARENA_POS.x > 8.2
		(arrow.material_override as StandardMaterial3D).albedo_color = Color(1.0, 0.3, 0.3) if wet else Color(0.4, 1.0, 0.5)
		(arrow.material_override as StandardMaterial3D).emission = (Color(1.0, 0.25, 0.25) if wet else Color(0.3, 1.0, 0.45)) * 0.9
		var pressed: bool = Input.is_physical_key_pressed(KEY_SPACE) or Input.is_joy_button_pressed(0, JOY_BUTTON_A) or Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) or (touch_ui != null and touch_ui.action_down)
		if pressed and float(g.get("press_cool", 0.0)) <= 0.0:
			g["press_cool"] = 1.0
			g["vel"] = dirv * 11.5 + Vector3(0, 6.5, 0)
			g["phase"] = "fly"
			arrow.visible = false
			if voice != null:
				voice.pitch_scale = 1.1
				voice.play()
		g["press_cool"] = maxf(0.0, float(g.get("press_cool", 0.0)) - delta)
	elif String(g["phase"]) == "fly":
		hud_game.text = "Wheee!"
		var v: Vector3 = g["vel"]
		v.y -= 9.5 * delta
		g["vel"] = v
		ball.position += v * delta
		if ball.position.y <= ARENA_POS.y + 0.9:
			ball.position.y = ARENA_POS.y + 0.9
			if ball.position.x - ARENA_POS.x > 8.2:
				# SPLASH - into the lake!
				g["miss"] = int(g["miss"]) + 1
				_sparkle_burst(ball.position, Color(0.4, 0.7, 1.0))
				var bz := AudioStreamPlayer.new()
				bz.stream = load("res://assets/audio/buzz.ogg")
				add_child(bz)
				bz.play()
				bz.finished.connect(bz.queue_free)
				if int(g["miss"]) >= 2:
					_end_game(false, fr, "Aww... now Chuck is all wet!", "fail")
					return
				show_msg(fr["fname"], "SPLASH! Chuck can't swim out there! One more try...")
				g["phase"] = "aim"
				(g["arrow"] as MeshInstance3D).visible = true
			else:
				g["phase"] = "fetch"
	elif String(g["phase"]) == "pickup":
		# nose down to grab the ball, then turn for home
		hud_game.text = "Chuck is on it!"
		g["pickup_t"] = float(g.get("pickup_t", 0.8)) - delta
		if float(g["pickup_t"]) <= 0.35:
			var mouth := Vector3(sin(chuck.rotation.y), 0, cos(chuck.rotation.y))
			ball.position = chuck.position + mouth * 1.4 + Vector3(0, 1.0, 0)
		if float(g["pickup_t"]) <= 0.0:
			g["phase"] = "return"
			_chuck_play("run")
	else:
		var target: Vector3 = ball.position
		if String(g["phase"]) == "return":
			target = ppos
		var d: Vector3 = target - chuck.position
		d.y = 0.0
		hud_game.text = "Chuck is on it!"
		if d.length() > 2.0:
			chuck.position += d.normalized() * minf(40.0 * delta, d.length())
			chuck.rotation.y = atan2(d.x, d.z)
			_chuck_play("run")
			if String(g["phase"]) == "return":
				var mouth := Vector3(sin(chuck.rotation.y), 0, cos(chuck.rotation.y))
				ball.position = chuck.position + mouth * 1.4 + Vector3(0, 1.0, 0)
		elif String(g["phase"]) == "fetch":
			g["phase"] = "pickup"
			g["pickup_t"] = 0.8
			_chuck_play("pickup", 0.15)
		else:
			g["round"] = int(g["round"]) + 1
			_chuck_play("wag", 0.2)
			if int(g["round"]) >= 2:
				_say("chuck", "bark")
				_end_game(true, fr, "Chuck loves to fetch! What a good boy!")
			else:
				g["phase"] = "aim"
				(g["arrow"] as MeshInstance3D).visible = true
var dolls_layer: CanvasLayer
var dolls_root: Control
var dolls_catcher: TextureRect

func _dolls2d_open(fr: Dictionary) -> void:
	if dolls_layer == null:
		dolls_layer = CanvasLayer.new()
		dolls_layer.layer = 6
		add_child(dolls_layer)
	dolls_root = Control.new()
	dolls_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	dolls_layer.add_child(dolls_root)
	var bg := TextureRect.new()
	bg.texture = load("res://assets/book/nursery_bg.jpg")
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	dolls_root.add_child(bg)
	var tint := ColorRect.new()
	tint.color = Color(0.08, 0.05, 0.2, 0.25)
	tint.set_anchors_preset(Control.PRESET_FULL_RECT)
	dolls_root.add_child(tint)
	var faron := TextureRect.new()
	faron.texture = (fr["node"] as Sprite3D).texture
	faron.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	faron.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
	faron.custom_minimum_size = Vector2(170, 200)
	faron.size = Vector2(170, 200)
	faron.position = Vector2(40, 60)
	dolls_root.add_child(faron)
	dolls_catcher = TextureRect.new()
	dolls_catcher.texture = load("res://assets/characters/roshan_sprite.png")
	dolls_catcher.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	dolls_catcher.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
	dolls_catcher.custom_minimum_size = Vector2(130, 165)
	dolls_catcher.size = Vector2(130, 165)
	dolls_catcher.position = Vector2(580, 530)
	dolls_root.add_child(dolls_catcher)

func _dolls2d_close() -> void:
	if dolls_root != null and is_instance_valid(dolls_root):
		dolls_root.queue_free()
	dolls_root = null
	dolls_catcher = null

func _tick_dolls(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	if dolls_root == null:
		return
	# move the 2D catcher: stick / arrows / mouse-touch x
	var mx := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		mx -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		mx += 1.0
	var jx: float = Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
	if absf(jx) > 0.2:
		mx += jx
	if touch_ui != null and absf((touch_ui.stick_vec as Vector2).x) > 0.15:
		mx += (touch_ui.stick_vec as Vector2).x
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		var target_x: float = dolls_root.get_global_mouse_position().x - 60.0
		dolls_catcher.position.x = lerpf(dolls_catcher.position.x, target_x, 0.2)
	dolls_catcher.position.x = clampf(dolls_catcher.position.x + mx * 620.0 * delta, 0.0, 1160.0)
	g["next"] = float(g["next"]) - delta
	if float(g["next"]) <= 0.0 and int(g["spawned"]) < 5:
		g["spawned"] = int(g["spawned"]) + 1
		g["next"] = 1.2
		var doll := ColorRect.new()
		doll.color = Color(0, 0, 0, 0)
		doll.size = Vector2(96, 86)
		doll.position = Vector2(80.0 + randf() * 1100.0, -100.0)
		var dtex := TextureRect.new()
		dtex.texture = load(["res://assets/book/baby_doll.png", "res://assets/book/baby_doll2.png", "res://assets/book/baby_doll3.png"][int(g["spawned"]) % 3])
		dtex.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		dtex.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		dtex.set_anchors_preset(Control.PRESET_FULL_RECT)
		doll.add_child(dtex)
		dolls_root.add_child(doll)
		(g["dolls"] as Array).append(doll)
	var dolls: Array = g["dolls"]
	for i in range(dolls.size() - 1, -1, -1):
		var doll: ColorRect = dolls[i]
		doll.position.y += 190.0 * delta
		doll.position.x += sin(float(g["t"]) * 1.6 + float(i) * 2.0) * 60.0 * delta
		doll.rotation = sin(float(g["t"]) * 2.0 + float(i)) * 0.25
		var caught: bool = doll.position.y > 490.0 and absf(doll.position.x + 48.0 - (dolls_catcher.position.x + 65.0)) < 115.0
		if caught:
			g["caught"] = int(g["caught"]) + 1
			g["resolved"] = int(g["resolved"]) + 1
			doll.queue_free()
			dolls.remove_at(i)
			if voice != null:
				voice.pitch_scale = 1.0 + randf() * 0.25
				voice.play()
		elif doll.position.y > 700.0:
			g["resolved"] = int(g["resolved"]) + 1
			doll.queue_free()
			dolls.remove_at(i)
	hud_game.text = "Sleepy dolls caught: %d (catch 3 to win!)" % int(g["caught"])
	if int(g["resolved"]) >= 5 and dolls.is_empty():
		_dolls2d_close()
		if int(g["caught"]) >= 3:
			_end_game(true, fr, "You tucked in %d dolls! All cozy now." % int(g["caught"]))
		else:
			_end_game(false, fr, "Oh no, the babies!", "fail")

func _tick_melody(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	var caught: int = int(g["caught"])
	hud_game.text = "Rainbow colors: %d / 7" % caught
	for ob in g["orbs"]:
		if bool(ob["caught"]):
			continue
		var node: MeshInstance3D = ob["node"]
		var v: Vector3 = ob["vel"]
		node.position += v * delta
		var rel: Vector3 = node.position - ARENA_POS
		if absf(rel.x) > 16.0:
			v.x = -v.x
			node.position.x = ARENA_POS.x + clampf(rel.x, -16.0, 16.0)
		if rel.y < 2.6 or rel.y > 17.0:
			v.y = -v.y
			node.position.y = ARENA_POS.y + clampf(rel.y, 2.6, 17.0)
		if absf(rel.z) > 12.0:
			v.z = -v.z
			node.position.z = ARENA_POS.z + clampf(rel.z, -12.0, 12.0)
		ob["vel"] = v
		node.scale = Vector3.ONE * (1.0 + sin(float(g["t"]) * 6.0 + node.position.x) * 0.10)
		if absf(node.position.x - ppos.x) < 14.0 and absf(node.position.y - ppos.y) < 7.0 and absf(node.position.z - ppos.z) < 14.0:
			ob["caught"] = true
			node.visible = false
			caught += 1
			g["caught"] = caught
			_sparkle_burst(node.position, (node.material_override as StandardMaterial3D).albedo_color)
			if chime != null:
				chime.pitch_scale = 0.9 + float(caught) * 0.07
				chime.play()
			if voice != null and caught % 2 == 0:
				voice.pitch_scale = 1.0 + randf() * 0.25
				voice.play()
			if caught >= 7:
				_end_game(true, fr, "You caught the WHOLE rainbow! Gabby and her friends cheer!")
				return
func _process(delta: float) -> void:
	if msg_timer > 0.0:
		msg_timer -= delta
		if msg_timer <= 0.0:
			hud_msg.text = ""
	if speech_t > 0.0:
		speech_t -= delta
		if speech_t <= 0.0 and speech_layer != null:
			speech_layer.visible = false
	if player == null:
		return
	if intro_active:
		return
	var ppos: Vector3 = player.position
	for i in range(pearls.size() - 1, -1, -1):
		var p := pearls[i]
		p.rotate_y(delta * 0.7)
		p.position.y += sin(Time.get_ticks_msec() / 700.0 + float(i)) * 0.006
		if p.position.distance_to(ppos) < 6.0:
			var l: OmniLight3D = p.get_meta("light")
			if is_instance_valid(l):
				l.queue_free()
			var h: MeshInstance3D = p.get_meta("halo")
			if is_instance_valid(h):
				h.queue_free()
			p.queue_free()
			pearls.remove_at(i)
			pearl_count += 1
			_sparkle_burst(p.position, Color(1.0, 0.8, 1.0))
			if chime != null:
				var step: int = pearl_note % 21
				var deg: int = step % 7
				var octv: int = step / 7
				chime.pitch_scale = 0.75 * pow(2.0, float(PENT[deg] + 12 * octv) / 12.0)
				chime.play()
				pearl_note += 1
			_say("roshan", ["pearl", "pearl2", "pearl3"][pearl_note % 3])
			_update_hud()
			_write_save()
	var tt: float = Time.get_ticks_msec() / 1000.0
	for f in friends:
		var node: Sprite3D = f["node"]
		var sparks: Array = f["sparks"]
		for si in range(sparks.size()):
			var orb: MeshInstance3D = sparks[si]
			var oa: float = tt * (0.9 + 0.3 * float(si)) + float(f["ph"]) + PI * float(si)
			orb.position = node.position + Vector3(cos(oa) * 3.2, 4.5 + sin(tt * 1.7 + float(si)) * 1.4, sin(oa) * 3.2)
		var pl: MeshInstance3D = f["pillar"]
		pl.scale.x = 1.0 + 0.18 * sin(tt * 1.3 + float(f["ph"]))
		pl.scale.z = pl.scale.x
		f["cool"] = maxf(0.0, float(f["cool"]) - delta)
		var dd: float = node.position.distance_to(ppos)
		if not f["found"] and dd < 9.0:
			f["found"] = true
			(f["beacon"] as OmniLight3D).light_energy = 1.0
			var pmat2: StandardMaterial3D = (f["pillar"] as MeshInstance3D).material_override
			pmat2.albedo_color.a = 0.035
			f["cool"] = 2.5
			show_msg(f["fname"], f["msg"])
			_update_hud()
			_write_save()
		elif f["found"] and game == "" and dd < 10.0:
			if float(f["cool"]) > 0.0:
				hud_game.text = "%s: game starting in %d..." % [f["fname"], int(ceilf(float(f["cool"])))]
			elif dd < 8.0:
				hud_game.text = ""
				_start_game(f)
	if game == "level2":
		g["t"] = float(g["t"]) + delta
		_tick_level2(delta, ppos)
	elif game != "":
		_tick_game(delta)
	_tick_wall_fade(delta)
	_tick_life(delta)
	_tick_movers(delta)
	_tick_aquatic(delta)
	_tick_fft_ocean(delta)
	_tick_wind(delta)
	_tick_wind_streaks(delta)
	_tick_surf_rings(delta, ppos)
	_tick_god_rays(delta)
	_tick_guide(delta)
	_tick_finale(delta)
	_tick_hints(delta)
	_tick_beans(delta)
	_tick_roshan_reactions(delta, ppos)
	shop_cool = maxf(0.0, shop_cool - delta)
	treasure_cool = maxf(0.0, treasure_cool - delta)
	slide_cool = maxf(0.0, slide_cool - delta)
	if game == "" and finale_t < 0.0:
		if manta != null and shop_cool <= 0.0:
			if manta.position.distance_to(ppos) < 17.0:
				shop_cool = 16.0
				_start_game(shop_fr)
		if treasure_cool <= 0.0 and wreck_pos.distance_to(ppos) < 13.0:
			treasure_cool = 12.0
			_start_game(treasure_fr)
		if slide_cool <= 0.0 and slide_portal_pos != Vector3.ZERO and slide_portal_pos.distance_to(ppos) < 12.0:
			slide_cool = 14.0
			_start_game(slide_fr)
		_check_level2_unlock(ppos, delta)
	cull_timer -= delta
	if cull_timer <= 0.0:
		cull_timer = 0.7
		var lim: float = 95.0 if quality == "speedy" else 160.0
		for i3 in range(anim_cull.size() - 1, -1, -1):
			var ac: Dictionary = anim_cull[i3]
			if not is_instance_valid(ac["node"]) or not is_instance_valid(ac["ap"]):
				anim_cull.remove_at(i3)
				continue
			var nd: Node3D = ac["node"]
			var ap2: AnimationPlayer = ac["ap"]
			var near: bool = nd.position.distance_to(ppos) < lim
			if near and not ap2.is_playing():
				ap2.play()
			elif not near and ap2.is_playing():
				ap2.pause()
	if touch_ui != null:
		var act_lbl := "JUMP"
		if game == "fetch" and String(g.get("phase", "")) == "aim":
			act_lbl = "THROW"
		elif game == "fairyshoot":
			act_lbl = "FIRE"
		touch_ui.set_action_label(act_lbl)

# ===================== BIOLUMINESCENT LIFE =====================
func _sway_grass_mat(base: Color, tip: Color) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode cull_disabled, depth_prepass_alpha;
uniform vec3 base_col;
uniform vec3 tip_col;
uniform sampler2D leaf;
global uniform vec3 wind_dir;
global uniform float wind_gust;
void vertex(){
	float w = UV.y;
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	// gusts ROLL across the meadow: phase offset along the wind direction, and
	// the blades lean downwind on top of their own sway
	float gg = 0.4 + wind_gust * 1.2;
	float ph = TIME * (0.9 + wind_gust * 0.7) - dot(wp.xz, wind_dir.xz) * 0.14;
	VERTEX.x += (sin(ph + wp.x * 0.28 + wp.z * 0.22) * 0.5 * gg + wind_dir.x * wind_gust * 0.5) * w;
	VERTEX.z += (cos(ph * 0.78 + wp.x * 0.16) * 0.36 * gg + wind_dir.z * wind_gust * 0.5) * w;
}
void fragment(){
	vec4 lf = texture(leaf, vec2(UV.x, 1.0 - UV.y));
	if (lf.a < 0.4) { discard; }
	float t = UV.y;
	vec3 col = mix(base_col, tip_col, t * t);
	col *= (0.7 + lf.g * 0.45);
	ALBEDO = col;
	ROUGHNESS = 0.8;
	SPECULAR = 0.15;
	// soft translucency so blades let light through, plus a tip glow strong
	// enough to feed the bloom pass (dark blades otherwise never bloom)
	BACKLIGHT = tip_col * (0.25 + t * 0.4);
	EMISSION = tip_col * (0.05 + t * t * 0.22);
}"""
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("base_col", Vector3(base.r, base.g, base.b))
	m.set_shader_parameter("tip_col", Vector3(tip.r, tip.g, tip.b))
	m.set_shader_parameter("leaf", load("res://assets/terrain/leaf.png"))
	return m
func _glow_dot_mat() -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = """shader_type spatial;
void fragment(){
	ALBEDO = COLOR.rgb * 0.6;
	ROUGHNESS = 0.6;
	EMISSION = COLOR.rgb * 0.85;
}"""
	var m := ShaderMaterial.new()
	m.shader = sh
	return m
func _scatter_field(count: int, mesh: Mesh, mat: Material, y_off: float, use_color: bool, cols: Array, upright: bool = false) -> void:
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = use_color
	mm.mesh = mesh
	mm.instance_count = count
	for i in range(count):
		var pos := Vector3.ZERO
		if i % 10 < 6 and cluster_centers.size() > 0:
			var c: Vector3 = cluster_centers[randi() % cluster_centers.size()]
			var aa: float = randf() * TAU
			var rr: float = 4.0 + randf() * 22.0
			pos = Vector3(c.x + cos(aa) * rr, 0, c.z + sin(aa) * rr)
		else:
			var aa2: float = randf() * TAU
			var rr2: float = 25.0 + randf() * (WORLD_R * 0.9 - 25.0)
			pos = Vector3(cos(aa2) * rr2, 0, sin(aa2) * rr2)
		pos.y = seabed_y(pos.x, pos.z) + y_off
		var sc: float = 0.55 + randf() * 1.9
		var bas := Basis(Vector3.UP, randf() * TAU).scaled(Vector3(sc, sc * (0.8 + randf() * 0.8), sc))
		if upright:
			bas = Basis(Vector3.UP, randf() * TAU) * Basis(Vector3.RIGHT, PI * 0.5).scaled(Vector3(sc, sc, sc))
		var tr := Transform3D(bas, pos)
		mm.set_instance_transform(i, tr)
		if use_color:
			mm.set_instance_color(i, cols[randi() % cols.size()])
	var mmi := MultiMeshInstance3D.new()
	mmi.multimesh = mm
	mmi.material_override = mat
	add_child(mmi)

func _build_meadows() -> void:
	# seagrass meadow — crossed swaying blades
	_scatter_field(2100, _cross_blade(0.9, 3.8), _sway_grass_mat(Color(0.09, 0.30, 0.26), Color(0.40, 0.78, 0.62)), 0.0, false, [])
	# tall kelp ribbons (muted teal, not electric)
	_scatter_field(520, _cross_blade(1.6, 11.0), _sway_grass_mat(Color(0.08, 0.22, 0.26), Color(0.34, 0.55, 0.64)), 0.0, false, [])
	# real sea-floor life: anemones, starfish, urchins — soft jewel tones
	_scatter_field(360, _anemone_mesh(), _glow_tip_mat(), 0.1, true,
		[Color(0.95, 0.55, 0.72), Color(0.55, 0.82, 0.92), Color(0.78, 0.62, 0.95), Color(0.55, 0.92, 0.80)])
	_scatter_field(240, _starfish_mesh(), _glow_tip_mat("res://assets/terrain/star_detail.png"), 0.15, true,
		[Color(0.98, 0.66, 0.52), Color(0.95, 0.58, 0.62), Color(0.98, 0.78, 0.52), Color(0.85, 0.66, 0.92)])
	_scatter_field(200, _urchin_mesh(), _glow_tip_mat(), 0.3, true,
		[Color(0.6, 0.5, 0.78), Color(0.5, 0.62, 0.85), Color(0.82, 0.55, 0.68)])

func _fish_mat() -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nuniform sampler2D scales;\nvoid fragment(){\n\tfloat sc = texture(scales, UV * vec2(3.0, 1.5)).r;\n\tfloat belly = smoothstep(-0.3, 0.4, NORMAL.y);\n\tvec3 body = mix(COLOR.rgb * 0.10, COLOR.rgb * 0.45 + vec3(0.25), belly) * (0.7 + sc * 0.6);\n\tfloat rim = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 2.5);\n\tfloat band = step(0.8, fract(UV.x * 3.0)) ;\n\tALBEDO = body;\n\tEMISSION = COLOR.rgb * (band * 1.2 + rim * 1.6 + sc * 0.15);\n\tROUGHNESS = 0.35;\n}"
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("scales", load("res://assets/terrain/scales.png"))
	return m

func _build_fish() -> void:
	var cols := [Color(0.3, 0.95, 1.0), Color(1.0, 0.6, 0.85), Color(0.6, 1.0, 0.5), Color(1.0, 0.85, 0.4), Color(0.7, 0.55, 1.0), Color(0.4, 0.8, 1.0)]
	var body := _fish_mesh(1.0)
	var fmat := _fish_mat()
	for s2 in range(6):
		var col: Color = cols[s2]
		var aa: float = randf() * TAU
		var rr: float = 50.0 + randf() * 160.0
		var school := {"cx": cos(aa) * rr, "cz": sin(aa) * rr, "cy": 12.0 + randf() * 22.0,
			"rad": 12.0 + randf() * 14.0, "spd": 0.2 + randf() * 0.3, "ph": randf() * TAU, "fish": []}
		var mm := MultiMesh.new()
		mm.transform_format = MultiMesh.TRANSFORM_3D
		mm.use_colors = true
		mm.mesh = body
		mm.instance_count = 14
		for i in range(14):
			mm.set_instance_color(i, col)
		var mmi := MultiMeshInstance3D.new()
		mmi.multimesh = mm
		mmi.material_override = fmat
		add_child(mmi)
		school["mm"] = mm
		var halo := _halo(Vector3.ZERO, col, 12.0)
		school["light"] = halo
		fish_schools.append(school)

func _build_wreck() -> void:
	var wx: float = cos(2.4) * 150.0
	var wz: float = sin(2.4) * 150.0
	var wy: float = seabed_y(wx, wz)
	wreck_pos = Vector3(wx, wy + 4.0, wz)
	var ship := _spawn("ship-wreck", Vector3(wx, wy - 0.5, wz), 9.0, 2.4)
	if ship != null:
		ship.rotation_degrees.z = 14.0
		# NOTE: no collider on the wreck — swimming within 13u of it launches the
		# treasure-dive minigame (see _build_events / treasure trigger). A solid
		# bubble here would either block that trigger or, given the long hull,
		# fit it badly. The wreck is an entrance, not a wall.
	_spawn("chest", Vector3(wx + 10.0, seabed_y(wx + 10.0, wz + 4.0), wz + 4.0), 4.0, 1.0)
	_spawn("barrel", Vector3(wx - 8.0, seabed_y(wx - 8.0, wz - 5.0), wz - 5.0), 4.0, 0.4)
	_fairy_light(Vector3(wx, wy + 9.0, wz), Color(0.4, 1.0, 0.8), true)
	_fairy_light(Vector3(wx + 10.0, seabed_y(wx + 10.0, wz + 4.0) + 3.0, wz + 4.0), Color(1.0, 0.85, 0.4), true)
	# ghost ship drifting high above — the mystery
	var ghost := _spawn("ship-ghost", Vector3(-wx, WATER_TOP - 10.0, -wz), 7.0, 0.0)
	if ghost != null:
		ghost.set_meta("ghost", true)
		manta = ghost
		for li2 in range(3):
			var lamp := OmniLight3D.new()
			lamp.light_color = Color(1.0, 0.78, 0.42)
			lamp.light_energy = 2.2
			lamp.omni_range = 34.0
			lamp.position = Vector3(-0.9 + float(li2) * 0.9, 1.2, 0.35 - float(li2) * 0.3)
			ghost.add_child(lamp)
			var bulb := MeshInstance3D.new()
			var bm2 := SphereMesh.new()
			bm2.radius = 0.12
			bm2.height = 0.24
			bulb.mesh = bm2
			var bmat := StandardMaterial3D.new()
			bmat.emission_enabled = true
			bmat.emission = Color(1.0, 0.8, 0.45)
			bmat.emission_energy_multiplier = 4.0
			bulb.material_override = bmat
			bulb.position = lamp.position
			ghost.add_child(bulb)
			pulse_lights.append({"light": lamp, "base": 2.2, "phase": randf() * TAU})

func _build_events() -> void:
	bloom_parts = GPUParticles3D.new()
	bloom_parts.amount = 220
	bloom_parts.lifetime = 2.6
	bloom_parts.one_shot = true
	bloom_parts.explosiveness = 0.9
	bloom_parts.emitting = false
	var pm := ParticleProcessMaterial.new()
	pm.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_SPHERE
	pm.emission_sphere_radius = 4.0
	pm.gravity = Vector3(0, 2.5, 0)
	pm.initial_velocity_min = 2.0
	pm.initial_velocity_max = 6.0
	bloom_parts.process_material = pm
	var quad := QuadMesh.new()
	quad.size = Vector2(0.4, 0.4)
	var qm := StandardMaterial3D.new()
	qm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	qm.albedo_color = Color(0.7, 1.0, 0.9)
	qm.emission_enabled = true
	qm.emission = Color(0.5, 1.0, 0.8)
	qm.emission_energy_multiplier = 2.0
	qm.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
	quad.material = qm
	bloom_parts.draw_pass_1 = quad
	add_child(bloom_parts)

func _tick_life(delta: float) -> void:
	var t: float = Time.get_ticks_msec() / 1000.0
	for pl in pulse_lights:
		var k: float = 0.65 + 0.45 * sin(t * 1.6 + float(pl["phase"]))
		if pl.has("light"):
			(pl["light"] as OmniLight3D).light_energy = float(pl["base"]) * k
		elif pl.has("halo"):
			(pl["halo"] as MeshInstance3D).scale = Vector3.ONE * (0.8 + 0.3 * k)
	for sc in fish_schools:
		var ang: float = t * float(sc["spd"]) + float(sc["ph"])
		var cx: float = float(sc["cx"]) + cos(ang) * float(sc["rad"])
		var cz: float = float(sc["cz"]) + sin(ang) * float(sc["rad"])
		var cy: float = float(sc["cy"]) + sin(t * 0.7 + float(sc["ph"])) * 2.5
		var mm: MultiMesh = sc["mm"]
		var heading := Basis(Vector3.UP, -ang + PI * 0.5)
		for i in range(14):
			var off := Vector3(sin(t * 2.0 + float(i) * 1.7) * 2.6, sin(t * 2.6 + float(i)) * 1.2 + float(i % 3 - 1) * 1.1, cos(t * 1.8 + float(i) * 2.1) * 2.6)
			mm.set_instance_transform(i, Transform3D(heading, Vector3(cx, cy, cz) + off))
		(sc["light"] as MeshInstance3D).position = Vector3(cx, cy, cz)
	# ghost ship slow drift + bob
	if manta != null:
		manta.position.x += sin(t * 0.05) * 0.02
		manta.position.y = WATER_TOP - 10.0 + sin(t * 0.4) * 1.5
		manta.rotation.y += delta * 0.03
	# sparkle bloom event
	bloom_t -= delta
	if bloom_t <= 0.0 and cluster_centers.size() > 0:
		bloom_t = 35.0 + randf() * 30.0
		var c: Vector3 = cluster_centers[randi() % cluster_centers.size()]
		bloom_parts.position = c + Vector3(0, 4, 0)
		bloom_parts.restart()
		bloom_parts.emitting = true

# ===================== ADVANCED CHEAP LIGHT + REAL CREATURES =====================
func _cross_blade(w: float, h: float) -> ArrayMesh:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for rot in [0.0, PI * 0.5]:
		var bas := Basis(Vector3.UP, rot)
		var p00 := bas * Vector3(-w * 0.5, 0, 0)
		var p10 := bas * Vector3(w * 0.5, 0, 0)
		var p01 := bas * Vector3(-w * 0.15, h, 0)
		var p11 := bas * Vector3(w * 0.15, h, 0)
		st.set_uv(Vector2(0, 0)); st.add_vertex(p00)
		st.set_uv(Vector2(1, 0)); st.add_vertex(p10)
		st.set_uv(Vector2(1, 1)); st.add_vertex(p11)
		st.set_uv(Vector2(0, 0)); st.add_vertex(p00)
		st.set_uv(Vector2(1, 1)); st.add_vertex(p11)
		st.set_uv(Vector2(0, 1)); st.add_vertex(p01)
	st.generate_normals()
	return st.commit()

func _glow_tip_mat(detail: String = "res://assets/terrain/polyp.png") -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode cull_disabled;
uniform sampler2D det;
void fragment(){
	float t = UV.y;
	vec3 d = texture(det, VERTEX.xz * 0.55 + VERTEX.yy * 0.21).rgb;
	float dl = 0.7 + d.g * 0.6;
	ALBEDO = COLOR.rgb * dl;
	ROUGHNESS = 0.65;
	SPECULAR = 0.3;
	// gentle glow concentrated at the tips, much softer than before
	EMISSION = COLOR.rgb * (0.08 + (1.0 - t) * (1.0 - t) * 0.45) * (0.7 + d.g * 0.5);
}"""
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("det", load(detail))
	return m
func _fish_mesh(s2: float) -> ArrayMesh:
	# stylized fish: flattened body + tail fin, nose at +X
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var nose := Vector3(0.7, 0, 0) * s2
	var top := Vector3(0.0, 0.28, 0) * s2
	var bot := Vector3(0.0, -0.24, 0) * s2
	var l := Vector3(0.0, 0, 0.10) * s2
	var r := Vector3(0.0, 0, -0.10) * s2
	var rear := Vector3(-0.55, 0, 0) * s2
	var t_up := Vector3(-0.95, 0.3, 0) * s2
	var t_dn := Vector3(-0.95, -0.3, 0) * s2
	var quads := [
		[nose, top, l], [nose, l, bot], [nose, bot, r], [nose, r, top],
		[rear, l, top], [rear, bot, l], [rear, r, bot], [rear, top, r],
		[rear, t_up, t_dn], [rear, t_dn, t_up],
	]
	for tri in quads:
		var uvv: float = 0.5
		for p in tri:
			st.set_uv(Vector2(clampf((p.x / s2 + 0.95) / 1.65, 0.0, 1.0), uvv))
			st.add_vertex(p)
	st.generate_normals()
	return st.commit()

func _creature_mat() -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode cull_disabled;\nuniform sampler2D scales;\nvoid fragment(){\n\tfloat sc = texture(scales, UV * vec2(6.0, 3.0)).r;\n\tfloat belly = smoothstep(-0.4, 0.5, NORMAL.y);\n\tALBEDO = (vec3(0.03, 0.07, 0.11) + COLOR.rgb * 0.12 * belly) * (0.7 + sc * 0.5);\n\tfloat rim = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 2.2);\n\tvec2 cell = fract(UV * vec2(10.0, 5.0)) - 0.5;\n\tfloat rnd = fract(sin(dot(floor(UV * vec2(10.0, 5.0)), vec2(12.98, 78.23))) * 43758.54);\n\tfloat spots = smoothstep(0.28, 0.16, length(cell)) * step(0.5, rnd);\n\tEMISSION = COLOR.rgb * (spots * 1.8 + rim * 1.2 + 0.06) + vec3(0.1, 0.3, 0.4) * rim;\n}"
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("scales", load("res://assets/terrain/scales.png"))
	return m

func _flap_mat(col: Color) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode cull_disabled;\nuniform vec3 tint;\nvoid vertex(){\n\tfloat wing = abs(VERTEX.z);\n\tVERTEX.y += sin(TIME * 2.2 + wing * 0.8) * wing * 0.35;\n}\nvoid fragment(){\n\tfloat belly = smoothstep(-0.5, 0.5, NORMAL.y);\n\tALBEDO = mix(vec3(0.02, 0.04, 0.08), tint * 0.30 + vec3(0.18), belly);\n\tvec2 cell = fract(UV * vec2(9.0, 16.0)) - 0.5;\n\tfloat rnd = fract(sin(dot(floor(UV * vec2(9.0, 16.0)), vec2(12.98, 78.23))) * 43758.54);\n\tfloat dot_m = smoothstep(0.30, 0.18, length(cell)) * step(0.55, rnd);\n\tfloat rim = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 2.2);\n\tEMISSION = tint * (dot_m * 1.8 + rim * 1.1 + 0.05);\n}"
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("tint", Vector3(col.r, col.g, col.b))
	return m

func _manta_mesh() -> ArrayMesh:
	# smooth winged diamond: 6 chord strips per wing + tail dart
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var rows := 6
	var prev_front := Vector3(2.0, 0, 0)
	var prev_back := Vector3(-2.2, 0, 0)
	for k in range(1, rows + 1):
		var f: float = float(k) / float(rows)
		var span: float = 4.4 * sin(f * PI * 0.5)
		var chord_f: float = 2.0 * (1.0 - f * 0.85)
		var chord_b: float = -2.2 * (1.0 - f * 0.9)
		var lift: float = -0.25 * f * f
		for side in [1.0, -1.0]:
			var z0: float = span * (float(k - 1) / float(rows)) / max(f, 0.001) * f * side
			var cf0 := prev_front
			var cb0 := prev_back
			var cf1 := Vector3(chord_f, lift, span * side)
			var cb1 := Vector3(chord_b, lift, span * side)
			for tri in [[cf0, cf1, cb1], [cf0, cb1, cb0]]:
				var order: Array = tri if side > 0.0 else [tri[0], tri[2], tri[1]]
				for p in order:
					st.set_uv(Vector2((p.x + 2.2) / 4.2, (p.z + 4.4) / 8.8))
					st.add_vertex(p)
		prev_front = Vector3(chord_f, lift, 0)
		prev_back = Vector3(chord_b, lift, 0)
	# tail dart
	for tri in [[Vector3(-2.0, 0, 0), Vector3(-4.4, 0.1, 0.18), Vector3(-4.4, 0.1, -0.18)]]:
		for p in tri:
			st.set_uv(Vector2(0.0, 0.5))
			st.add_vertex(p)
	st.generate_normals()
	return st.commit()

var movers: Array = []
func _build_megafauna() -> void:
	# 3 glowing mantas
	var mmesh := _manta_mesh()
	for i in range(3):
		var m := MeshInstance3D.new()
		m.mesh = mmesh
		m.material_override = _flap_mat([Color(0.4, 0.9, 1.0), Color(0.9, 0.6, 1.0), Color(0.5, 1.0, 0.7)][i])
		m.scale = Vector3.ONE * (2.2 + float(i) * 0.6)
		add_child(m)
		movers.append({"node": m, "kind": "manta", "rad": 90.0 + float(i) * 45.0, "spd": 0.06 + randf() * 0.04,
			"ph": randf() * TAU, "y": 24.0 + float(i) * 8.0})
	# 1 great glowing whale
	var w := MeshInstance3D.new()
	w.mesh = _fish_mesh(14.0)
	w.material_override = _creature_mat()
	var mmw := MultiMesh.new()
	add_child(w)
	movers.append({"node": w, "kind": "whale", "rad": 200.0, "spd": 0.018, "ph": 0.0, "y": 38.0})
	# 2 sea turtles cruising low
	for i in range(2):
		var tm := MeshInstance3D.new()
		tm.mesh = _manta_mesh()
		tm.material_override = _flap_mat(Color(0.55, 1.0, 0.45))
		tm.scale = Vector3.ONE * 1.1
		add_child(tm)
		movers.append({"node": tm, "kind": "turtle", "rad": 60.0 + float(i) * 70.0, "spd": 0.05,
			"ph": PI * float(i), "y": 10.0 + float(i) * 5.0})

var god_rays: Array = []
func _build_god_rays() -> void:
	var rsh := Shader.new()
	rsh.code = "shader_type spatial;\nrender_mode cull_disabled, unshaded, blend_add, depth_draw_never;\nuniform vec4 tint : source_color;\nvoid fragment(){\n\tfloat across = 1.0 - abs(UV.x - 0.5) * 2.0;\n\tfloat down = smoothstep(0.0, 0.35, UV.y) * (1.0 - UV.y * 0.5);\n\tALBEDO = tint.rgb;\n\tALPHA = tint.a * pow(across, 1.8) * down;\n}"
	for i in range(18):
		var a: float = float(i) / 18.0 * TAU + randf() * 0.5
		var r: float = 30.0 + randf() * (WORLD_R * 0.85)
		var quad := QuadMesh.new()
		quad.size = Vector2(7.0 + randf() * 10.0, WATER_TOP + 30.0)
		var m := ShaderMaterial.new()
		m.shader = rsh
		m.set_shader_parameter("tint", Color(0.55, 0.88, 1.0, 0.06 + randf() * 0.05))
		var mi := MeshInstance3D.new()
		mi.mesh = quad
		mi.material_override = m
		mi.position = Vector3(cos(a) * r, (WATER_TOP + 30.0) * 0.45, sin(a) * r)
		mi.rotation_degrees = Vector3(0, randf() * 180.0, 6.0 + randf() * 8.0)
		add_child(mi)
		god_rays.append({"node": mi, "base": mi.rotation.z, "ph": randf() * TAU})

func _tick_god_rays(delta: float) -> void:
	var tt: float = Time.get_ticks_msec() / 1000.0
	for gr in god_rays:
		var n: MeshInstance3D = gr["node"]
		if is_instance_valid(n):
			n.rotation.z = float(gr["base"]) + sin(tt * 0.25 + float(gr["ph"])) * (0.03 + 0.06 * wind_gust_v)

# ===================== WW MOTION LANGUAGE: WIND / STREAKS / RINGS =====================
func _tick_wind(delta: float) -> void:
	wind_t += delta
	# slowly wandering direction + two beating sines so gusts swell and die
	var wyaw: float = 0.55 + sin(wind_t * 0.023) * 1.1 + sin(wind_t * 0.011 + 2.0) * 0.5
	wind_dir_v = Vector3(sin(wyaw), 0.0, cos(wyaw))
	wind_gust_v = clampf(0.55 + 0.30 * sin(wind_t * 0.34) + 0.18 * sin(wind_t * 0.9 + 1.7), 0.08, 1.0)
	RenderingServer.global_shader_parameter_set("wind_dir", wind_dir_v)
	RenderingServer.global_shader_parameter_set("wind_gust", wind_gust_v)

func _flag_shader() -> Shader:
	# turret flags ripple with the global gust — pinned at the pole (UV.x = 0)
	if flag_sh == null:
		flag_sh = Shader.new()
		flag_sh.code = """shader_type spatial;
render_mode cull_disabled;
uniform vec4 col : source_color;
uniform float amp = 0.3;
global uniform float wind_gust;
void vertex(){
	float t = UV.x;
	float gg = 0.35 + wind_gust * 0.9;
	VERTEX.z += sin(TIME * (5.0 + wind_gust * 5.0) - t * 7.0) * amp * t * gg;
	VERTEX.y += sin(TIME * (3.4 + wind_gust * 3.2) - t * 5.0 + 1.3) * amp * 0.35 * t * gg;
}
void fragment(){
	ALBEDO = col.rgb;
	EMISSION = col.rgb * 0.4;
	ROUGHNESS = 0.9;
}"""
	return flag_sh

func _streak_mesh(leng: float, curl: float, wdt: float) -> ArrayMesh:
	# corkscrew ribbon with UV.x running along its length — the dash shader travels down it
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLE_STRIP)
	var segs := 36
	for i in range(segs + 1):
		var t: float = float(i) / float(segs)
		var th: float = t * TAU * 1.6
		var r: float = curl * sin(PI * t)
		var p := Vector3(t * leng, sin(th) * r, cos(th) * r * 0.6)
		var side := Vector3(0.0, cos(th), -sin(th)).normalized() * wdt * (0.5 + 0.5 * sin(PI * t))
		st.set_uv(Vector2(t, 0.0))
		st.add_vertex(p + side)
		st.set_uv(Vector2(t, 1.0))
		st.add_vertex(p - side)
	return st.commit()

func _build_wind_streaks() -> void:
	# pooled WW gust curls: slow cyan current lines underwater, white wind gusts
	# in the Sky Lagoon. The pool lives forever; _tick_wind_streaks restyles it
	# whenever the context (sea / sky / off) changes.
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode unshaded, blend_add, cull_disabled, depth_draw_never, shadows_disabled;
uniform vec4 tint : source_color;
uniform float ph = 0.0;
uniform float spd = 0.3;
global uniform float wind_gust;
void fragment(){
	float cyc = fract(TIME * spd + ph) * 1.9 - 0.45;   // dash sweeps past both ends, then rests
	float dash = smoothstep(cyc - 0.42, cyc - 0.03, UV.x) * (1.0 - smoothstep(cyc - 0.03, cyc + 0.02, UV.x));
	float across = 1.0 - abs(UV.y - 0.5) * 2.0;
	float ends = smoothstep(0.0, 0.10, UV.x) * (1.0 - smoothstep(0.90, 1.0, UV.x));
	ALBEDO = tint.rgb;
	ALPHA = tint.a * dash * pow(across, 1.4) * ends * (0.35 + 0.65 * wind_gust);
}"""
	for i in range(10):
		var mi := MeshInstance3D.new()
		mi.mesh = _streak_mesh(24.0 + randf() * 14.0, 2.2 + randf() * 1.6, 0.32 + randf() * 0.2)
		var m := ShaderMaterial.new()
		m.shader = sh
		m.set_shader_parameter("ph", randf())
		m.set_shader_parameter("spd", 0.22 + randf() * 0.16)
		mi.material_override = m
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.visible = false
		add_child(mi)
		wind_streaks.append({"node": mi, "mat": m, "age": randf() * 8.0, "life": 7.0 + randf() * 5.0})

func _tick_wind_streaks(delta: float) -> void:
	var ctx := "off"
	if game == "":
		ctx = "sea"
	elif game == "level2" and String(g.get("phase", "")) != "hall":
		ctx = "sky"   # outdoors in the Sky Lagoon (not inside the castle hall)
	if ctx != streak_ctx:
		streak_ctx = ctx
		for i in range(wind_streaks.size()):
			var s: Dictionary = wind_streaks[i]
			var mi: MeshInstance3D = s["node"]
			mi.visible = ctx != "off" and (quality != "speedy" or i % 2 == 0)
			var m: ShaderMaterial = s["mat"]
			if ctx == "sea":
				m.set_shader_parameter("tint", Color(0.55, 0.85, 1.0, 0.30))
			else:
				m.set_shader_parameter("tint", Color(1.0, 1.0, 1.0, 0.42))
			_respawn_streak(s, true)
	if ctx == "off":
		return
	var spd: float = (2.5 + wind_gust_v * 5.0) if ctx == "sea" else (7.0 + wind_gust_v * 11.0)
	for s in wind_streaks:
		var mi: MeshInstance3D = s["node"]
		if not mi.visible:
			continue
		s["age"] = float(s["age"]) + delta
		mi.position += wind_dir_v * spd * delta
		if float(s["age"]) > float(s["life"]) or mi.position.distance_to(player.position) > 95.0:
			_respawn_streak(s, false)

func _respawn_streak(s: Dictionary, scatter: bool) -> void:
	var mi: MeshInstance3D = s["node"]
	s["age"] = 0.0
	s["life"] = 7.0 + randf() * 5.0
	var back: float = -55.0 + (randf() * 90.0 if scatter else randf() * 20.0)
	var perp := Vector3(-wind_dir_v.z, 0.0, wind_dir_v.x)
	var base: Vector3 = player.position + wind_dir_v * back + perp * (randf() * 70.0 - 35.0)
	if streak_ctx == "sky":
		base.y = lagoon_h(base.x, base.z) + 5.0 + randf() * 22.0
	else:
		base.y = clampf(8.0 + randf() * (WATER_TOP - 20.0), 6.0, WATER_TOP - 6.0)
	mi.position = base
	# the mesh extends along +X; yaw it so +X points down the wind
	mi.rotation = Vector3(0.0, atan2(-wind_dir_v.z, wind_dir_v.x), randf() * 0.6 - 0.3)

func _build_surf_rings() -> void:
	# pooled expanding rings on the underside of the water ceiling (WW telegraphs
	# every surface interaction with one of these)
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode unshaded, blend_add, cull_disabled, depth_draw_never, shadows_disabled;
uniform float prog = 1.0;
uniform vec4 tint : source_color;
void fragment(){
	float r = length(UV - 0.5) * 2.0;
	float ring = smoothstep(prog - 0.22, prog - 0.02, r) * (1.0 - smoothstep(prog - 0.02, prog + 0.03, r));
	ALBEDO = tint.rgb;
	ALPHA = tint.a * ring * (1.0 - prog);
}"""
	for i in range(6):
		var q := QuadMesh.new()
		q.size = Vector2(1.0, 1.0)
		var mi := MeshInstance3D.new()
		mi.mesh = q
		var m := ShaderMaterial.new()
		m.shader = sh
		m.set_shader_parameter("tint", Color(0.85, 0.97, 1.0, 0.85))
		m.set_shader_parameter("prog", 1.0)
		mi.material_override = m
		mi.rotation_degrees = Vector3(-90, 0, 0)   # lie flat on the surface
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.visible = false
		add_child(mi)
		surf_rings.append({"node": mi, "mat": m, "t": 1.0})

func _spawn_surf_ring(pos: Vector3, size: float) -> void:
	for s in surf_rings:
		if float(s["t"]) >= 1.0:
			s["t"] = 0.0
			var mi: MeshInstance3D = s["node"]
			mi.scale = Vector3.ONE * size
			mi.position = pos
			mi.visible = true
			return

func _tick_surf_rings(delta: float, ppos: Vector3) -> void:
	ring_cool -= delta
	if game == "" and ppos.y > WATER_TOP - 7.0 and ring_cool <= 0.0:
		var pv: Vector3 = player.vel
		if Vector3(pv.x, 0, pv.z).length() > 4.0 or pv.y > 6.0:
			ring_cool = 0.38
			_spawn_surf_ring(Vector3(ppos.x, WATER_TOP - 0.25, ppos.z), 9.0 + randf() * 4.0)
	for s in surf_rings:
		if float(s["t"]) < 1.0:
			s["t"] = minf(float(s["t"]) + delta / 1.25, 1.0)
			(s["mat"] as ShaderMaterial).set_shader_parameter("prog", float(s["t"]))
			if float(s["t"]) >= 1.0:
				(s["node"] as MeshInstance3D).visible = false

func on_player_jump(pos: Vector3) -> void:
	# WW-style splash telegraph: ring + sparkles when she leaps near the surface
	if game == "" and pos.y > WATER_TOP - 12.0:
		_spawn_surf_ring(Vector3(pos.x, WATER_TOP - 0.25, pos.z), 16.0)
		_sparkle_burst(Vector3(pos.x, minf(pos.y + 2.0, WATER_TOP - 1.0), pos.z), Color(0.75, 0.95, 1.0))

func _tick_movers(delta: float) -> void:
	var t: float = Time.get_ticks_msec() / 1000.0
	for mv in movers:
		var node: Node3D = mv["node"]
		var ang: float = t * float(mv["spd"]) + float(mv["ph"])
		var rad: float = float(mv["rad"])
		var pos := Vector3(cos(ang) * rad, float(mv["y"]) + sin(t * 0.3 + float(mv["ph"])) * 3.0, sin(ang) * rad)
		node.position = pos
		node.rotation.y = -ang
		if String(mv["kind"]) == "whale":
			node.rotation.z = sin(t * 0.5) * 0.06

# ===================== CUTAWAY ARENAS =====================
func _play_music(track: String) -> void:
	cur_track = track
	var mpath := "res://assets/audio/music/" + track + ".ogg"
	if not ResourceLoader.exists(mpath):
		return   # no track for this kind (e.g. transient arena setup) — keep current music
	var st: AudioStream = load(mpath)
	if st is AudioStreamOggVorbis:
		(st as AudioStreamOggVorbis).loop = true
	music.stream = st
	music.volume_db = -8.0 if music_on else -60.0
	music.play()

func _arena_floor(col: Color, tex: String = "", nrm: String = "", uvs: float = 0.06) -> void:
	var disc := CylinderMesh.new()
	disc.top_radius = 55.0
	disc.bottom_radius = 55.0
	disc.height = 1.0
	var mi := MeshInstance3D.new()
	mi.mesh = disc
	var m := StandardMaterial3D.new()
	m.albedo_color = col
	if tex != "":
		m.albedo_texture = load(tex)
		m.uv1_triplanar = true
		m.uv1_world_triplanar = true
		m.uv1_scale = Vector3(uvs, uvs, uvs)
		m.roughness = 0.95
	if nrm != "":
		m.normal_enabled = true
		m.normal_texture = load(nrm)
		m.normal_scale = 0.8
	mi.material_override = m
	mi.position = ARENA_POS + Vector3(0, -0.5, 0)
	add_child(mi)
	game_nodes.append(mi)

func _enter_arena(kind: String) -> void:
	return_pos = player.position
	arena_solids.clear()
	fade_walls.clear()
	lagoon_floor = false
	arena_center = ARENA_POS
	arena_dome = 48.0
	arena_ceil = 42.0
	arena_env = Environment.new()
	arena_env.background_mode = Environment.BG_COLOR
	arena_env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	_wind_waker_bloom(arena_env, 0.9, 0.35, 1.02)   # bloom emitters only — 0.85 white-washed bright floors (snow!)
	if kind == "fetch":          # snowy backyard noon
		arena_env.background_color = Color(0.75, 0.88, 1.0)
		arena_env.ambient_light_color = Color(0.94, 0.96, 1.0)
		arena_env.ambient_light_energy = 0.65   # snow bounces plenty; higher ambient + the world sun pushed the floor past ACES white
		arena_env.glow_bloom = 0.05             # near-zero whole-frame haze: on an already-white scene the WW haze clips everything
		_arena_floor(Color(0.74, 0.77, 0.84), GTA + "up_snowsoft_col.jpg", GTA + "up_snow_nrm.jpg", 0.06)   # fresh snow; tint keeps it under ACES clip so the surface stays readable
	elif kind == "dolls":        # starry dream nursery
		arena_env.background_color = Color(0.10, 0.06, 0.22)
		arena_env.ambient_light_color = Color(0.7, 0.6, 1.0)
		arena_env.ambient_light_energy = 0.7
		_arena_floor(Color(0.85, 0.78, 0.72), GTA + "up_wood_col.jpg", GTA + "up_wood_nrm.jpg", 0.06)
	elif kind == "seek":         # sunny meadow
		arena_env.background_color = Color(0.55, 0.85, 1.0)
		arena_env.ambient_light_color = Color(1, 1, 0.95)
		arena_env.ambient_light_energy = 1.2
		_arena_floor(Color(0.95, 1.0, 0.92), GTA + "up_grass_col.jpg", GTA + "up_grass_nrm.jpg", 0.06)
	elif kind == "race":         # sunset sky
		arena_env.background_color = Color(1.0, 0.62, 0.38)
		arena_env.ambient_light_color = Color(1.0, 0.8, 0.65)
		arena_env.ambient_light_energy = 1.1
		_arena_floor(Color(1.05, 0.82, 0.62), GTA + "up_dirt_col.jpg", GTA + "up_dirt_nrm.jpg", 0.05)
	elif kind == "shop":         # warm wooden ship cabin
		arena_env.background_color = Color(0.06, 0.045, 0.025)
		arena_env.ambient_light_color = Color(1.0, 0.85, 0.6)
		arena_env.ambient_light_energy = 0.9
		arena_env.glow_intensity = 0.8
		_arena_floor(Color(0.9, 0.8, 0.65), GTA + "up_wood_col.jpg", GTA + "up_wood_nrm.jpg", 0.06)
	elif kind == "treasure":     # deep dark cavern
		arena_env.background_color = Color(0.012, 0.035, 0.06)
		arena_env.ambient_light_color = Color(0.35, 0.55, 0.75)
		arena_env.ambient_light_energy = 0.55
		arena_env.glow_intensity = 1.15
		_arena_floor(Color(0.55, 0.54, 0.6), GTA + "Rock061_2K_Color.jpg", GTA + "Rock061_2K_NormalGL.jpg", 0.08)
	elif kind == "slide":        # bright icy sky — the chute builds its own geometry (no flat floor)
		arena_env.background_color = Color(0.62, 0.82, 1.0)
		arena_env.ambient_light_color = Color(0.95, 0.98, 1.0)
		arena_env.ambient_light_energy = 1.25
		arena_env.glow_intensity = 0.7
	elif kind == "fairyshoot":   # dreamy twilight fairy pond — the corridor builds its own geometry
		arena_env.background_color = Color(0.16, 0.10, 0.30)
		arena_env.ambient_light_color = Color(0.7, 0.65, 1.0)
		arena_env.ambient_light_energy = 0.9
		arena_env.glow_intensity = 1.2
		arena_env.glow_bloom = 0.5   # extra-dreamy fairy pond
	else:                        # concert stage night
		arena_env.background_color = Color(0.06, 0.03, 0.12)
		arena_env.ambient_light_color = Color(0.8, 0.6, 1.0)
		arena_env.ambient_light_energy = 0.85
		_arena_floor(Color(0.62, 0.5, 0.72), GTA + "up_wood_col.jpg", GTA + "up_wood_nrm.jpg", 0.06)
	_grade(arena_env)
	we_node.environment = arena_env
	player.position = ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	_play_music(kind)

func _leave_arena() -> void:
	we_node.environment = world_env
	player.position = return_pos
	player.vel = Vector3.ZERO
	_play_music("world")

func _btn_pressed() -> int:
	# returns 0..3 for A/B/X/Y edge press, else -1
	var btns := [JOY_BUTTON_A, JOY_BUTTON_B, JOY_BUTTON_X, JOY_BUTTON_Y]
	for i in range(4):
		var down: bool = Input.is_joy_button_pressed(0, btns[i])
		var key: String = "btn%d" % i
		if down and not bool(g.get(key, false)):
			g[key] = true
			return i
		if not down:
			g[key] = false
	return -1

# ===================== SEA CREATURE MESHES =====================
func _anemone_mesh() -> ArrayMesh:
	# ring of 9 tentacles curving outward, UV.y along tentacle for tip glow
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for k in range(9):
		var a: float = float(k) / 9.0 * TAU
		var out := Vector3(cos(a), 0, sin(a))
		var side := Vector3(-sin(a), 0, cos(a)) * 0.10
		var segs := 3
		var prev_a := out * 0.25 - side
		var prev_b := out * 0.25 + side
		var prev_v := 0.0
		for s2 in range(1, segs + 1):
			var f: float = float(s2) / float(segs)
			var p := out * (0.25 + f * 0.9) + Vector3(0, 1.5 * f - 0.55 * f * f, 0)
			var w: float = 0.10 * (1.0 - f * 0.8)
			var na := p - side.normalized() * w
			var nb := p + side.normalized() * w
			for tri in [[prev_a, prev_b, nb], [prev_a, nb, na]]:
				for q in tri:
					var vv: float = prev_v if (q == prev_a or q == prev_b) else f
					st.set_uv(Vector2(0.5, 1.0 - vv))
					st.add_vertex(q)
			prev_a = na
			prev_b = nb
			prev_v = f
	st.generate_normals()
	return st.commit()

func _starfish_mesh() -> ArrayMesh:
	# flat 5-armed star resting on the sand
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var c := Vector3(0, 0.12, 0)
	for k in range(5):
		var a: float = float(k) / 5.0 * TAU
		var a2: float = a + TAU / 10.0
		var tip := Vector3(cos(a), 0.02, sin(a)) * 1.5
		var v1 := Vector3(cos(a - 0.45), 0.06, sin(a - 0.45)) * 0.5
		var v2 := Vector3(cos(a + 0.45), 0.06, sin(a + 0.45)) * 0.5
		for tri in [[c, v1, tip], [c, tip, v2]]:
			for q in tri:
				var d2: float = Vector2(q.x, q.z).length() / 1.5
				st.set_uv(Vector2(0.5, 1.0 - d2))
				st.add_vertex(q)
	st.generate_normals()
	return st.commit()

func _urchin_mesh() -> ArrayMesh:
	# spiky ball: low dome + 14 needle spikes
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var dome := 8
	for k in range(dome):
		var a: float = float(k) / float(dome) * TAU
		var b: float = float(k + 1) / float(dome) * TAU
		var p1 := Vector3(cos(a), 0, sin(a)) * 0.45
		var p2 := Vector3(cos(b), 0, sin(b)) * 0.45
		var top := Vector3(0, 0.5, 0)
		for q in [p1, p2, top]:
			st.set_uv(Vector2(0.5, 1.0))
			st.add_vertex(q)
	for k in range(14):
		var ya: float = randf() * TAU
		var pitch: float = 0.25 + randf() * 1.0
		var dirv := Vector3(cos(ya) * cos(pitch), sin(pitch), sin(ya) * cos(pitch))
		var base := dirv * 0.35
		var tip := dirv * (1.0 + randf() * 0.4)
		var sidev := dirv.cross(Vector3.UP).normalized() * 0.05
		if sidev.length() < 0.01:
			sidev = Vector3(0.05, 0, 0)
		for tri in [[base - sidev, base + sidev, tip]]:
			for i2 in range(3):
				var q: Vector3 = tri[i2]
				st.set_uv(Vector2(0.5, 1.0 if i2 < 2 else 0.0))
				st.add_vertex(q)
	st.generate_normals()
	return st.commit()
