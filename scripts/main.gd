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
var hud_layer: CanvasLayer = null
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
var crafted_fish_spawned := 0      # how many custom_fish entries are already swimming
var craft_layer: CanvasLayer = null
var craft_body := Color(0.4, 0.7, 1.0)
var craft_fins := Color(1.0, 0.6, 0.2)
var craft_fishbox: Control = null
var craft_kind := "fish"
var craft_unlocks := {}            # one-time pearl unlocks for craft creatures ("cat", "bird")
var craft_status: Label = null     # in-studio feedback (HUD messages sit behind the overlay)
var craft_pearl_lbl: Label = null
var custom_friends: Array = []
# accent layers are DISTINCT zone masks (kitty: horn + chest tuft; birdie:
# crest + wings) painted from the body art — the old cat/bird "accent" reused
# the whole body at 50% alpha, so the two colors just mixed into grey
const CREATURE_LAYERS := {"fish": ["fish_fins", "fish_body", "fish_line"], "cat": ["cat_accent", "cat_body", "cat_line"], "bird": ["bird_accent", "bird_body", "bird_line"]}
var l2_open := false
# Phase 1: star progress survives slide/picture round-trips (the rebuild used
# to wipe it); reset ONLY on a fresh entry from the ocean portal
var l2_star_progress: Array = [false, false, false]
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
var arena_zones: Array = []   # y-banded floor/ceil overrides (castle stories)
var fade_walls: Array = []   # interior walls that fade out when they block the camera
var mg_cool := 0.0
var mg2d_layer: CanvasLayer
var mg2d_root: Control
var mg2d_stage: Control
var mg_kind := ""
# Rainbow Road kart racer (scripts/kart.gd)
var kart_portal_pos := Vector3.ZERO
var kart_cool := 0.0
var kart_game: Node = null
var kart_ground := "terrain"    # which variant the current race is ("float" = rainbow gateway)
var galaxy_game: Node = null    # Level 3 — Butterfly World (scripts/galaxy.gd)
var galaxy_unlocked := false
var fairy_skin_unlocked := false   # Butterfly World prize: the Fairy Roshan look
var bwd_done := false              # the 7 butterflies are home FOREVER (owner: never repeat the quest)

# ---- STICKER BOOK: in-game achievements, tuned for a 4yo (no gamerscore,
# ---- just a book of shiny stickers). Deliberately rewards the side content
# ---- that gates nothing: the penguin, the beans, the hug, the secret cave...
const STICKER_DEFS := [
	{"id": "penguin", "emoji": "🐧", "label": "Penguin Pal", "hint": "Catch the baby penguin on the big slide!"},
	{"id": "beans", "emoji": "💨", "label": "Toot Toot!", "hint": "Eat the magic beans from the Pearl Shop!"},
	{"id": "sleepy", "emoji": "💤", "label": "Sleepyhead", "hint": "Take a nap in the castle bed!"},
	{"id": "hug", "emoji": "❤", "label": "Biggest Hug", "hint": "Find Daddy's secret hug in the castle!"},
	{"id": "artist", "emoji": "🎨", "label": "Little Artist", "hint": "Craft a fishy, a kitty AND a birdie!"},
	{"id": "bells", "emoji": "🔔", "label": "Bell Singer", "hint": "Sing the whole bell song!"},
	{"id": "treasure", "emoji": "💎", "label": "Treasure Hunter", "hint": "Find the Secret Cave treasure!"},
	{"id": "snowman", "emoji": "⛄", "label": "Snow Roller", "hint": "Roll up a whole snowman!"},
	{"id": "racer", "emoji": "🏁", "label": "Rainbow Racer", "hint": "Win the race in 1st place!"},
	{"id": "throne", "emoji": "👑", "label": "Star Princess", "hint": "Sit on the Moon Throne!"},
	{"id": "fruit", "emoji": "🍎", "label": "Butterfly Feast", "hint": "Call the swarm to a fruit tray!"},
	{"id": "butterfly", "emoji": "🦋", "label": "Butterfly Hero", "hint": "Save the Butterfly World!"},
	{"id": "flower", "emoji": "🌸", "label": "Flower Bloomer", "hint": "Bloom the giant flower!"},
	{"id": "carrot", "emoji": "🥕", "label": "Snowman Snack", "hint": "Chase the runaway snowman... and EAT him!"},
	{"id": "shopper", "emoji": "💰", "label": "Big Shopper", "hint": "Buy every treasure in the Pearl Shop!"},
	{"id": "superstar", "emoji": "⭐", "label": "SUPER STAR", "hint": "Collect every sticker and every trophy!"},
]
var stickers := {}                 # id -> true (plus hidden "_" progress keys)
var stickers_layer: CanvasLayer = null

func _sticker_def(id: String) -> Dictionary:
	for d in STICKER_DEFS:
		if String(d["id"]) == id:
			return d
	return STICKER_DEFS[0]

func award_sticker(id: String) -> void:
	if bool(stickers.get(id, false)):
		return
	stickers[id] = true
	_write_save()
	var d := _sticker_def(id)
	_sticker_toast("%s  New sticker:  %s!" % [String(d["emoji"]), String(d["label"])])
	_fanfare()
	if player != null:
		_sparkle_burst(player.position + Vector3(0, 2.5, 0), Color(1.0, 0.9, 0.4))
	_check_superstar()

func _sticker_toast(txt: String) -> void:
	var cl4 := CanvasLayer.new()
	cl4.layer = 23
	add_child(cl4)
	var t := Label.new()
	t.text = txt
	t.add_theme_font_size_override("font_size", 44)
	t.add_theme_color_override("font_color", Color(1.0, 0.93, 0.55))
	t.add_theme_color_override("font_outline_color", Color(0.15, 0.08, 0.25))
	t.add_theme_constant_override("outline_size", 12)
	t.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	t.offset_top = -70.0
	cl4.add_child(t)
	var tw := t.create_tween()
	tw.tween_property(t, "offset_top", 120.0, 0.45).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_interval(2.6)
	tw.tween_property(t, "offset_top", -70.0, 0.4).set_ease(Tween.EASE_IN)
	tw.tween_callback(cl4.queue_free)

func _check_superstar() -> void:
	if bool(stickers.get("superstar", false)):
		return
	for d in STICKER_DEFS:
		var sid := String(d["id"])
		if sid != "superstar" and not bool(stickers.get(sid, false)):
			return
	if trophies < 5 or not level2_done_once or not fairy_skin_unlocked:
		return
	stickers["superstar"] = true
	_write_save()
	_begin_100_celebration()

func _begin_100_celebration() -> void:
	# 100%! The whole reef celebrates — fireworks, confetti, everyone cheering
	pose_t = 5.0
	_say("everyone", "")
	_fanfare()
	var cl5 := CanvasLayer.new()
	cl5.layer = 23
	add_child(cl5)
	var big := Label.new()
	big.text = "⭐ 100%! ⭐\nSUPER STAR ROSHAN!"
	big.add_theme_font_size_override("font_size", 96)
	big.add_theme_color_override("font_color", Color(1.0, 0.95, 0.6))
	big.add_theme_color_override("font_outline_color", Color(0.2, 0.08, 0.3))
	big.add_theme_constant_override("outline_size", 18)
	big.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	big.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	big.offset_top = 90.0
	cl5.add_child(big)
	for ci in range(70):
		var conf := ColorRect.new()
		conf.color = Color.from_hsv(randf(), 0.75, 1.0)
		conf.size = Vector2(18, 18)
		conf.position = Vector2(randf() * 1280.0, -40.0 - randf() * 500.0)
		conf.rotation = randf() * TAU
		cl5.add_child(conf)
		var ct := conf.create_tween()
		ct.tween_property(conf, "position:y", 800.0, 2.2 + randf() * 1.6).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	for fi in range(10):
		get_tree().create_timer(0.2 + 0.42 * float(fi)).timeout.connect(func():
			if player != null:
				_sparkle_burst(player.position + Vector3(randf_range(-8.0, 8.0), 3.0 + randf() * 7.0, randf_range(-8.0, 8.0)), Color.from_hsv(randf(), 0.6, 1.0)))
	get_tree().create_timer(5.4).timeout.connect(cl5.queue_free)    # set the first time the rainbow race soars into Level 3
var bw_portal_pos := Vector3.ZERO   # direct Butterfly World portal in the courtyard
var bw_cool := 0.0
var cel_post: Node = null   # fullscreen cel post-process quad (Forward+)
var kart_legA := Vector3.ZERO   # rainbow leg in world 2 -> forward race
var kart_legB := Vector3.ZERO   # rainbow leg in world 2 -> reversed race
var kart_from := ""             # which world launched the race ("" reef / "level2")
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
var caustics_plane: MeshInstance3D = null   # animated light dapples on the reef floor
var plankton_node: GPUParticles3D
var pause_layer: CanvasLayer
var pause_panel: Control
var pause_resume_btn: Button = null
var fps_lbl: Label = null
# bedtime: swim onto the castle bed -> tuck-in cutscene that flips day <-> night
var sleep_t := -1.0
var sleep_cool := 0.0
var sleep_layer: CanvasLayer = null
var sleep_overlay: ColorRect = null
var sleep_flip_done := false
var night_nodes: Array = []   # moon/beams/jellies — toggled when time flips at runtime
var quality_btn: Button
var music_btn: Button
var guide_fish: Sprite3D
var finale_done := false
var finale_t := -1.0
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
	{"id": "classic", "label": "Roshan", "preview": "res://assets/characters/roshan_sprite.png", "sprite": ""},
	{"id": "fairy", "label": "Fairy Mermaid", "preview": "res://assets/characters/skins/fairy_mermaid.png", "sprite": ""},
	{"id": "huluu", "label": "Princess Huluu", "preview": "res://assets/characters/friends/huluu.png", "sprite": "res://assets/characters/friends/huluu.png"},
	{"id": "pearl", "label": "Pearl Princess", "preview": "res://assets/characters/roshan_sprite.png", "sprite": ""}]
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
var fairy_pending := false      # a galaxy fountain touch queues the fairy flight
var fairy_from_galaxy := false  # so the fairy game returns to the Butterfly World
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
# THE PEARL SINK: with the Sticker Book driving completion, pearls become the
# treasure-shopping currency — real things to save up for instead of a number
# that only ever grows. Beans stay cheap; the rest are permanent treasures.
const SHOP_ITEMS := [
	{"id": "beans", "label": "Can of Beans", "price": 2},
	{"id": "tail", "label": "Rainbow Trail", "price": 60},
	{"id": "tiara", "label": "Pearl Tiara", "price": 120},
	{"id": "pearlskin", "label": "Pearl Princess", "price": 250}]
var shop_owned := {}   # permanent Pearl Shop treasures (persisted)
var flora_nodes: Array = []
var first_session := true
var chime: AudioStreamPlayer
var buy_sound: AudioStreamPlayer
var beans_sfx: AudioStreamPlayer   # banjo toot-loop: a SOUND EFFECT, not music (plays with music off)
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

# ---- gamepad input that works even for pads Godot has no SDL mapping for ----
# SDL mappings for the 8BitDo Lite family (Windows D-input, Linux, macOS,
# Android Bluetooth) — these pads otherwise show up unmapped and go dead.
const EXTRA_JOY_MAPPINGS := [
	"03000000c82d00001251000000000000,8BitDo Lite 2,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b6,leftstick:b13,lefttrigger:b8,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:b9,rightx:a3,righty:a4,start:b11,x:b4,y:b3,platform:Windows,",
	"03000000c82d00001251000011010000,8BitDo Lite 2,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b6,leftstick:b13,lefttrigger:a5,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:a4,rightx:a2,righty:a3,start:b11,x:b4,y:b3,platform:Linux,",
	"05000000c82d00001251000000010000,8BitDo Lite 2,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b6,leftstick:b13,lefttrigger:a5,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:a4,rightx:a2,righty:a3,start:b11,x:b4,y:b3,platform:Linux,",
	"03000000c82d00001251000000010000,8BitDo Lite 2,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b6,leftstick:b13,lefttrigger:a5,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:a4,rightx:a2,righty:a3,start:b11,x:b4,y:b3,platform:Mac OS X,",
	"30643332373663313263316637356631,8BitDo Lite 2,a:b1,b:b0,back:b15,dpdown:b12,dpleft:b13,dpright:b14,dpup:b11,guide:b5,leftshoulder:b9,leftstick:b7,lefttrigger:b17,leftx:a0,lefty:a1,rightshoulder:b10,rightstick:b8,righttrigger:b18,rightx:a2,righty:a3,start:b6,x:b3,y:b2,platform:Android,",
	"38426974446f204c6974652032000000,8BitDo Lite 2,a:b1,b:b0,back:b15,dpdown:b12,dpleft:b13,dpright:b14,dpup:b11,guide:b5,leftshoulder:b9,leftstick:b7,lefttrigger:b17,leftx:a0,lefty:a1,rightshoulder:b10,rightstick:b8,righttrigger:b18,rightx:a2,righty:a3,start:b6,x:b3,y:b2,platform:Android,",
	"62656331626461363634633735353032,8BitDo Lite 2,a:b1,b:b0,back:b15,dpdown:b12,dpleft:b13,dpright:b14,dpup:b11,guide:b5,leftshoulder:b9,leftstick:b7,lefttrigger:b17,leftx:a0,lefty:a1,rightshoulder:b10,rightstick:b8,righttrigger:b18,rightx:a2,righty:a3,start:b6,x:b3,y:b2,platform:Android,",
	"38426974446f2038426974446f204c69,8BitDo Lite,a:b1,b:b0,back:b15,dpdown:b12,dpleft:b13,dpright:b14,dpup:b11,guide:b5,leftshoulder:b9,leftstick:b7,lefttrigger:b17,leftx:a0,lefty:a1,rightshoulder:b10,rightstick:b8,righttrigger:b18,rightx:a2,righty:a3,start:b6,x:b3,y:b2,platform:Android,",
	"03000000c82d00001151000000000000,8BitDo Lite SE,a:b1,b:b0,back:b10,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,dpup:h0.1,guide:b12,leftshoulder:b6,leftstick:b13,lefttrigger:b8,leftx:a0,lefty:a1,rightshoulder:b7,rightstick:b14,righttrigger:b9,rightx:a3,righty:a4,start:b11,x:b4,y:b3,platform:Windows,",
]

var joy_ev_axis := {}      # raw axis index -> latest value (event-driven fallback)
var joy_ev_btn := {}       # raw button index -> pressed
var joy_has_unmapped := false   # any connected pad Godot has NO mapping for?

func _refresh_joy_mapped() -> void:
	joy_has_unmapped = false
	for dev: int in Input.get_connected_joypads():
		if not Input.is_joy_known(dev):
			joy_has_unmapped = true

func _input(ev: InputEvent) -> void:
	# record raw joypad events: unmapped pads never show up through the polled
	# Input.get_joy_axis / is_joy_button_pressed API, but they DO send events
	if ev is InputEventJoypadMotion:
		var jm := ev as InputEventJoypadMotion
		# hard deadzone on write: sticks only send events on CHANGE, so a small
		# resting drift value would otherwise stick around forever
		joy_ev_axis[int(jm.axis)] = jm.axis_value if absf(jm.axis_value) > 0.18 else 0.0
	elif ev is InputEventJoypadButton:
		var jb := ev as InputEventJoypadButton
		joy_ev_btn[int(jb.button_index)] = jb.pressed

func joy_axis(axis: int) -> float:
	# read from EVERY connected pad, not just device 0 — Bluetooth and 2.4GHz
	# dongles don't always enumerate as the first joypad
	var v := 0.0
	for dev: int in Input.get_connected_joypads():
		var a: float = Input.get_joy_axis(dev, axis)
		if absf(a) > absf(v):
			v = a
	# raw-event fallback ONLY while an unmapped pad is connected (axes 0/1 left
	# stick, 2/3 right stick on nearly every controller). For mapped pads the
	# polled API is authoritative — mixing in raw events risks stale values.
	if joy_has_unmapped:
		var raw: float = float(joy_ev_axis.get(int(axis), 0.0))
		if absf(raw) > absf(v):
			v = raw
	return v

func joy_pressed(btn: int) -> bool:
	for dev: int in Input.get_connected_joypads():
		if Input.is_joy_button_pressed(dev, btn):
			return true
	if joy_has_unmapped:
		if bool(joy_ev_btn.get(int(btn), false)):
			return true
		# unmapped-pad fallback: ANY face button (raw 0..3) counts as jump/action
		if btn == JOY_BUTTON_A or btn == JOY_BUTTON_B:
			for bi in range(4):
				if bool(joy_ev_btn.get(bi, false)):
					return true
	return false

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
	for jmap in EXTRA_JOY_MAPPINGS:
		Input.add_joy_mapping(String(jmap), true)
	Input.joy_connection_changed.connect(func(_dev: int, _conn: bool):
		joy_ev_axis.clear()   # never let a departed pad leave phantom input behind
		joy_ev_btn.clear()
		_refresh_joy_mapped())
	_refresh_joy_mapped()
	_build_environment()
	_build_terrain()
	_build_water()
	_build_garden()
	_build_meadows()
	_build_aquatic_flora()
	_build_aquatic_creatures()
	_build_wreck()
	_build_events()
	_build_pearls()
	_build_friends()
	_build_kart_portal()
	_build_player()
	_build_hud()
	_apply_cel_shading()
	_build_page_frame()
	get_tree().node_added.connect(_hook_button_taps)
	voice = AudioStreamPlayer.new()
	voice.stream = load("res://assets/audio/voice_yay.mp3")
	add_child(voice)
	chime = AudioStreamPlayer.new()
	chime.stream = load("res://assets/audio/chime.ogg")
	chime.volume_db = -4.0
	add_child(chime)
	buy_sound = AudioStreamPlayer.new()
	buy_sound.stream = load("res://assets/audio/buy.ogg")
	beans_sfx = AudioStreamPlayer.new()
	var banjo_st: AudioStream = load("res://assets/audio/music/banjo.ogg")
	if banjo_st is AudioStreamOggVorbis:
		(banjo_st as AudioStreamOggVorbis).loop = true
	beans_sfx.stream = banjo_st
	beans_sfx.volume_db = -7.0
	add_child(beans_sfx)
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
	_spawn_crafted_fish()   # save loads after the reef builds; spawn her fish now

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

func _unhandled_input(ev: InputEvent) -> void:
	# gamepad/keyboard advance for the storybook intro (taps and clicks land on
	# the invisible full-screen button; this covers A/B/Start, Space and Enter)
	if not intro_active:
		return
	var advance := false
	if ev is InputEventJoypadButton and (ev as InputEventJoypadButton).pressed:
		var bi: int = (ev as InputEventJoypadButton).button_index
		advance = bi == JOY_BUTTON_A or bi == JOY_BUTTON_B or bi == JOY_BUTTON_START
	elif ev is InputEventKey and (ev as InputEventKey).pressed and not (ev as InputEventKey).echo:
		var kc: int = (ev as InputEventKey).physical_keycode
		advance = kc == KEY_SPACE or kc == KEY_ENTER
	if advance:
		_intro_next()

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
		# night is MYSTICAL, not murky: strong blue moonlight so everything still
		# reads clearly, plus the bioluminescent dressing from _build_night_ocean
		if sky != null:
			sky.sky_top_color = Color(0.07, 0.17, 0.32)
			sky.sky_horizon_color = Color(0.03, 0.09, 0.19)
			sky.ground_bottom_color = Color(0.02, 0.04, 0.10)
			sky.ground_horizon_color = Color(0.03, 0.08, 0.15)
			sky.energy_multiplier = 0.52
		world_env.ambient_light_color = Color(0.30, 0.46, 0.64)
		world_env.ambient_light_energy = 0.85
		world_env.fog_light_color = Color(0.06, 0.16, 0.27)
		world_env.glow_intensity = 1.0   # bioluminescence reads stronger in the dark
		if sun_light != null:
			sun_light.light_color = Color(0.5, 0.66, 0.95)
			sun_light.light_energy = 0.46
		_build_night_ocean()
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
		world_env.glow_intensity = 0.75
		if sun_light != null:
			sun_light.light_color = Color(0.55, 0.80, 0.98)
			sun_light.light_energy = 0.55

var night_built := false

func _set_night(n: bool) -> void:
	# runtime day/night flip (used by the castle bed). The reef env + sun update
	# immediately; the night dressing is built once and shown/hidden after that.
	is_night = n
	_apply_time_of_day()   # builds the night dressing on first nightfall
	for nn in night_nodes:
		if is_instance_valid(nn):
			(nn as Node3D).visible = n
	if plankton_node != null:
		var pq := plankton_node.draw_pass_1 as QuadMesh
		if pq != null and pq.material is StandardMaterial3D:
			(pq.material as StandardMaterial3D).albedo_color = Color(0.62, 1.0, 0.95, 0.8) if n else Color(0.85, 0.97, 1.0, 0.5)

func _build_night_ocean() -> void:
	# mystical bioluminescent night dressing: a moon seen through the water,
	# shimmering moonbeam shafts, glowing drift-jellyfish, brighter plankton.
	# built once; _set_night() shows/hides it when the castle bed flips time
	if night_built:
		return
	night_built = true
	# ---- the moon, far overhead beyond the water surface ----
	var moon := MeshInstance3D.new()
	var msp := SphereMesh.new()
	msp.radius = 11.0
	msp.height = 22.0
	moon.mesh = msp
	var mm := StandardMaterial3D.new()
	mm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mm.albedo_color = Color(0.92, 0.96, 1.0)
	mm.emission_enabled = true
	mm.emission = Color(0.85, 0.92, 1.0)
	mm.emission_energy_multiplier = 2.2
	moon.material_override = mm
	moon.position = Vector3(110, 145, -150)
	add_child(moon)
	night_nodes.append(moon)
	night_nodes.append(_halo(moon.position, Color(0.75, 0.88, 1.0), 46.0))
	# ---- shimmering moonbeams reaching down to the reef floor ----
	var bsh := Shader.new()
	bsh.code = """shader_type spatial;
render_mode blend_add, unshaded, cull_disabled, depth_draw_never;
void fragment(){
	float sway = sin(TIME * 0.5 + UV.x * 12.0) * 0.5 + 0.5;
	float fade = smoothstep(0.0, 0.3, UV.y) * smoothstep(1.0, 0.55, UV.y);
	vec3 c = vec3(0.45, 0.75, 1.0);
	ALBEDO = c * fade * (0.10 + sway * 0.08);
	ALPHA = fade * 0.16;
}"""
	var bmat := ShaderMaterial.new()
	bmat.shader = bsh
	for bp: Vector3 in [Vector3(70, 0, -50), Vector3(-95, 0, 60), Vector3(25, 0, 115)]:
		var beam := MeshInstance3D.new()
		var bc := CylinderMesh.new()
		bc.top_radius = 4.5
		bc.bottom_radius = 8.5
		bc.height = WATER_TOP + 14.0
		bc.radial_segments = 10
		beam.mesh = bc
		beam.material_override = bmat
		beam.position = Vector3(bp.x, (WATER_TOP + 14.0) * 0.5 - 7.0, bp.z)
		add_child(beam)
		night_nodes.append(beam)
	# ---- glowing drift-jellyfish, each casting soft bioluminescent light ----
	# read the SAVED quality directly: _apply_time_of_day runs a moment before
	# _apply_quality, so the `quality` var still holds its default here
	var q: String = String(save_data.get("quality", "speedy" if OS.has_feature("mobile") else "sparkly"))
	var jcols := [Color(0.5, 0.95, 1.0), Color(1.0, 0.6, 0.9), Color(0.7, 0.6, 1.0), Color(0.5, 1.0, 0.8)]
	for i in range(8):
		var jc: Color = jcols[i % jcols.size()]
		var jelly := Node3D.new()
		var bell := MeshInstance3D.new()
		var bsp := SphereMesh.new()
		bsp.radius = 1.7
		bsp.height = 2.6
		bell.mesh = bsp
		var jm := StandardMaterial3D.new()
		jm.albedo_color = Color(jc.r, jc.g, jc.b, 0.65)
		jm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		jm.emission_enabled = true
		jm.emission = jc
		jm.emission_energy_multiplier = 1.5
		jm.cull_mode = BaseMaterial3D.CULL_DISABLED
		bell.material_override = jm
		jelly.add_child(bell)
		for tn in range(4):
			var tent := MeshInstance3D.new()
			var tc := CylinderMesh.new()
			tc.top_radius = 0.09
			tc.bottom_radius = 0.03
			tc.height = 3.4
			tc.radial_segments = 5
			tent.mesh = tc
			var tmat := StandardMaterial3D.new()
			tmat.albedo_color = Color(jc.r, jc.g, jc.b, 0.5)
			tmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			tmat.emission_enabled = true
			tmat.emission = jc
			tmat.emission_energy_multiplier = 0.8
			tent.material_override = tmat
			var ta: float = float(tn) / 4.0 * TAU
			tent.position = Vector3(cos(ta) * 0.8, -2.1, sin(ta) * 0.8)
			jelly.add_child(tent)
		var jl := OmniLight3D.new()
		jl.light_color = jc
		jl.light_energy = 1.1
		jl.omni_range = 15.0
		jl.visible = (q != "speedy") or (i % 2 == 0)
		jelly.add_child(jl)
		add_child(jelly)
		night_nodes.append(jelly)
		aquatic_movers.append({"node": jelly, "rad": 40.0 + randf() * 140.0, "spd": 0.05 + randf() * 0.06, "y": 16.0 + randf() * 26.0, "ph": randf() * TAU})
	# ---- the plankton field glows brighter on mystical nights ----
	if plankton_node != null:
		var pq := plankton_node.draw_pass_1 as QuadMesh
		if pq != null and pq.material is StandardMaterial3D:
			(pq.material as StandardMaterial3D).albedo_color = Color(0.62, 1.0, 0.95, 0.8)

func _grade(env: Environment) -> void:
	# cheap cinematic grade — ACES filmic tonemapping (works on the mobile renderer, ~free)
	env.tonemap_mode = Environment.TONE_MAPPER_ACES
	env.tonemap_exposure = 1.15
	env.tonemap_white = 1.2

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
	env.glow_enabled = true
	env.glow_intensity = 0.75
	env.glow_bloom = 0.14
	env.glow_hdr_threshold = 1.0
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
	sun.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_2_SPLITS
	sun.directional_shadow_max_distance = 90.0
	add_child(sun)
	sun_light = sun
	music.process_mode = Node.PROCESS_MODE_ALWAYS
	_build_god_rays()
	_build_caustics()

func _build_caustics() -> void:
	# animated underwater light dapples that follow Roshan along the reef floor (cheap, additive)
	var sh := Shader.new()
	sh.code = "shader_type spatial;\n" + \
		"render_mode unshaded, blend_add, cull_disabled, depth_draw_never, shadows_disabled;\n" + \
		"void fragment(){\n" + \
		"  vec2 uv = UV * 7.0;\n" + \
		"  float t = TIME * 0.4;\n" + \
		"  vec2 a = uv + vec2(sin(t + uv.y*2.0), cos(t*0.9 + uv.x*2.0)) * 0.22;\n" + \
		"  float c1 = sin(a.x*3.0 + t) * sin(a.y*3.0 - t*0.7);\n" + \
		"  float c2 = sin(a.x*4.7 - t*1.1) * sin(a.y*5.3 + t*0.5);\n" + \
		"  float c = pow(max(c1,0.0), 6.0) + pow(max(c2,0.0), 8.0);\n" + \
		"  ALBEDO = vec3(0.45, 0.8, 1.0) * c * 1.3;\n" + \
		"}"
	var pm := PlaneMesh.new()
	pm.size = Vector2(130.0, 130.0)
	var mi := MeshInstance3D.new()
	mi.mesh = pm
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mi.material_override = mat
	mi.visible = false
	add_child(mi)
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	caustics_plane = mi

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
	mat.albedo_texture = load("res://assets/terrain/up_sand_col.jpg")
	mat.normal_enabled = true
	mat.normal_texture = load("res://assets/terrain/up_sand_nrm.jpg")
	mat.roughness_texture = load("res://assets/terrain/up_sand_rgh.jpg")
	mat.uv1_triplanar = true
	mat.uv1_scale = Vector3(0.12, 0.12, 0.12)
	mat.albedo_color = Color(0.35, 0.55, 0.58)
	mi.material_override = mat
	add_child(mi)
	_add_caustics(mesh)
	_add_plankton()

func _add_caustics(terrain_mesh: Mesh) -> void:
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode blend_add, unshaded, depth_draw_never;
uniform sampler2D caustic;
void fragment(){
	vec3 wp = (INV_VIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;
	vec2 uv = wp.xz * 0.022 + vec2(TIME * 0.010, -TIME * 0.007);
	vec2 uv2 = wp.xz * 0.015 - vec2(TIME * 0.006, TIME * 0.009);
	float c = texture(caustic, uv).r * 0.55 + texture(caustic, uv2).r * 0.45;
	c = smoothstep(0.35, 0.95, c);
	ALBEDO = c * vec3(0.55, 0.78, 0.82) * 0.085;
}"""
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("caustic", load("res://assets/terrain/caustics.png"))
	var mi := MeshInstance3D.new()
	mi.mesh = terrain_mesh
	mi.material_override = m
	mi.position.y = 0.15
	add_child(mi)
func _add_plankton() -> void:
	var parts := GPUParticles3D.new()
	parts.amount = 320
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
	parts.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
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

func _toon_water_mat(deep: Color, shallow: Color, alpha: float, wobble_h: float, rip_scale: float) -> ShaderMaterial:
	# Phase 5: the one storybook water material (CC0 "Toon Water" base — see
	# ASSET_LICENSES.md). Depth-fade + shoreline foam on capable tiers; the
	# Speedy tier (and headless CI) runs it with zero depth-texture reads.
	var m := ShaderMaterial.new()
	m.shader = load("res://assets/shaders/toon_water.gdshader")
	m.set_shader_parameter("deep_color", deep)
	m.set_shader_parameter("shallow_color", shallow)
	m.set_shader_parameter("alpha_base", alpha)
	m.set_shader_parameter("wobble_height", wobble_h)
	m.set_shader_parameter("ripple_scale", rip_scale)
	m.set_shader_parameter("ripple", load("res://assets/terrain/up_water_nrm.jpg"))
	m.set_shader_parameter("caustics", load("res://assets/terrain/caustics.png"))
	m.set_shader_parameter("use_depth", quality != "speedy" and DisplayServer.get_name() != "headless")
	return m

func _build_water() -> void:
	var pm := PlaneMesh.new()
	pm.size = Vector2(WORLD_R * 2.6, WORLD_R * 2.6)
	pm.subdivide_width = 56
	pm.subdivide_depth = 56
	var mi := MeshInstance3D.new()
	mi.mesh = pm
	mi.position.y = WATER_TOP
	# Phase 5: the shared toon water (big soft ocean swell, extra sparkle —
	# this sheet is mostly seen from below, so it keeps a higher glow)
	var mat := _toon_water_mat(Color(0.14, 0.46, 0.66), Color(0.42, 0.78, 0.86), 0.52, 0.9, 0.012)
	mat.set_shader_parameter("sparkle", 0.6)
	mat.set_shader_parameter("wobble_speed", 0.9)
	mi.material_override = mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(mi)
	water_node = mi
	# experimental: real FFT ocean surface on top (GPU compute) — only on a real
	# device, never headless; the plane above stays as a guaranteed fallback

var water_node: MeshInstance3D
var water_y0 := 0.0
var rock_pbr: StandardMaterial3D
var wood_overlay: StandardMaterial3D

func _texture_mats() -> void:
	rock_pbr = StandardMaterial3D.new()
	rock_pbr.albedo_texture = load("res://assets/terrain/up_cliff_col.jpg")
	rock_pbr.albedo_color = Color(0.6, 0.66, 0.72)
	rock_pbr.normal_enabled = true
	rock_pbr.normal_texture = load("res://assets/terrain/up_cliff_nrm.jpg")
	rock_pbr.roughness_texture = load("res://assets/terrain/up_cliff_rgh.jpg")
	rock_pbr.uv1_triplanar = true
	rock_pbr.uv1_scale = Vector3(1.6, 1.6, 1.6)
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
	_toonify(inst)
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
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.position = pos
	add_child(mi)
	return mi

func _fairy_light(pos: Vector3, col: Color, hero: bool = false) -> void:
	if hero:
		var l := OmniLight3D.new()
		l.light_color = col
		l.light_energy = 1.8
		l.omni_range = 14.0
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

func _local_aabbs(n: Node, xf: Transform3D, acc: Array) -> void:
	if n is Node3D:
		xf = xf * (n as Node3D).transform
	if n is VisualInstance3D:
		acc.append(xf * (n as VisualInstance3D).get_aabb())
	for c in n.get_children():
		_local_aabbs(c, xf, acc)

func _fit_prop(model: Node3D, target_long: float) -> float:
	# scale a GLB prop so its longest HORIZONTAL footprint == target_long,
	# recentre it on the origin and seat its base at y=0 (works before add_child,
	# and survives far-off-origin models like the Poly throne). Returns height.
	_toonify(model)
	var acc: Array = []
	_local_aabbs(model, Transform3D.IDENTITY, acc)
	if acc.is_empty():
		return 0.0
	var bb: AABB = acc[0]
	for i in range(1, acc.size()):
		bb = bb.merge(acc[i])
	var longest: float = maxf(maxf(bb.size.x, bb.size.z), 0.001)
	var sc: float = target_long / longest
	model.scale = Vector3.ONE * sc
	var c: Vector3 = bb.position + bb.size * 0.5
	model.position = Vector3(-c.x * sc, -bb.position.y * sc, -c.z * sc)
	return bb.size.y * sc

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
	# tex (e.g. "castle") swaps the flat plaster for a real PBR stone material.
	var node := _l2_box(center, size, col)
	if tex != "":
		node.material_override = _up_mat(tex, 0.045, col)
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
		m.albedo_texture = load("res://assets/terrain/up_cliff_col.jpg")
		m.albedo_color = Color(0.66, 0.7, 0.74)
		m.normal_enabled = true
		m.normal_texture = load("res://assets/terrain/up_cliff_nrm.jpg")
		m.roughness_texture = load("res://assets/terrain/up_cliff_rgh.jpg")
		m.uv1_scale = Vector3(1.4, 1.4, 1.4)
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
	_toonify(inst)
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
		# GEN2 pilot: a family-style coral crowns the middle of every grove
		# (prominent placement per the owner's curation note)
		var gcoral := _gen2_prop("coral3", Vector3(c.x, seabed_y(c.x, c.z), c.z), 8.5, randf() * TAU, 0.08)
		if gcoral != null:
			flora_nodes.append(gcoral)
		# coral bouquet
		for k in range(4 + randi() % 4):
			var ca := randf() * TAU
			var cr := 2.0 + randf() * 9.0
			var cx := c.x + cos(ca) * cr
			var cz := c.z + sin(ca) * cr
			_place_aq(corals[randi() % corals.size()], Vector3(cx, seabed_y(cx, cz), cz), 1.6 + randf() * 2.2, false)
		# swaying seaweed — GEN2 crossed-quad sprite when present (denser, cheaper,
		# reads storybook); old GLB pack stays the strangler-fig fallback
		for k in range(3 + randi() % 3):
			var wa := randf() * TAU
			var wr := 3.0 + randf() * 10.0
			var wx := c.x + cos(wa) * wr
			var wz := c.z + sin(wa) * wr
			var sg := _gen2_seagrass(Vector3(wx, seabed_y(wx, wz), wz), 2.6 + randf() * 2.4)
			if sg == null:
				_place_aq(weeds[randi() % weeds.size()], Vector3(wx, seabed_y(wx, wz), wz), 1.8 + randf() * 2.0, true)
		# shells nestled in
		for k in range(2):
			var sa := randf() * TAU
			var sx := c.x + cos(sa) * (2.0 + randf() * 6.0)
			var sz := c.z + sin(sa) * (2.0 + randf() * 6.0)
			_place_aq(shells[randi() % shells.size()], Vector3(sx, seabed_y(sx, sz) + 0.3, sz), 1.2 + randf() * 1.5, false)
	# scattered boulders across the open seabed — the bigger ones are SOLID like
	# the grove rocks (they used to be swim-through, which read as a glitch)
	for i in range(70):
		var a := randf() * TAU
		var r := 25.0 + randf() * (WORLD_R * 0.85 - 25.0)
		var x := cos(a) * r
		var z := sin(a) * r
		var bscl: float = 2.0 + randf() * 4.0
		# GEN2 pilot: every other big boulder is the family-style rock
		# (audit KEEP nature_rock_largea/v1, owner-approved exemplar)
		if bscl >= 2.2 and i % 2 == 0:
			var grock := _gen2_prop("rock_largea", Vector3(x, seabed_y(x, z), z), bscl * 1.9, randf() * TAU, 0.25)
			if grock != null:
				flora_nodes.append(grock)
				_register_solid(grock)
				continue
		var brock := _place_aq(rocks[randi() % rocks.size()], Vector3(x, seabed_y(x, z), z), bscl, false)
		if bscl >= 2.2:   # audit #8: half the boulders were swim-through — inconsistent, read as a glitch
			_register_solid(brock)

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
	_spawn_crafted_fish()

func _spawn_crafted_fish() -> void:
	# spawn any custom_fish entries not yet in the water. Idempotent via the
	# counter: runs at world build, after _load_save() (the save loads AFTER
	# the reef builds, so spawning only at build time made every crafted fish
	# vanish on the next launch), and on each new craft.
	while crafted_fish_spawned < custom_fish.size():
		var cf: Variant = custom_fish[crafted_fish_spawned]
		crafted_fish_spawned += 1
		if not (cf is Array) or (cf as Array).size() < 6:
			continue
		var cfn := _make_creature_node("fish", Color(cf[0], cf[1], cf[2]), Color(cf[3], cf[4], cf[5]))
		add_child(cfn)
		flora_nodes.append(cfn)
		aquatic_movers.append({"node": cfn, "rad": 30.0 + randf() * 130.0, "spd": 0.10 + randf() * 0.12, "y": 8.0 + randf() * 26.0, "ph": randf() * TAU, "crafted": true})

func _tick_aquatic(delta: float) -> void:
	var t: float = Time.get_ticks_msec() / 1000.0
	for mv in aquatic_movers:
		var node: Node3D = mv["node"]
		var ang: float = t * float(mv["spd"]) + float(mv["ph"])
		var rad: float = float(mv["rad"])
		var pos := Vector3(cos(ang) * rad, float(mv["y"]) + sin(t * 0.3 + float(mv["ph"])) * 3.0, sin(ang) * rad)
		node.position = pos
		node.rotation.y = -ang + PI * 0.5
		# a fish SHE made recognises her: heart puff + chirp when she swims by
		if bool(mv.get("crafted", false)) and game == "":
			mv["greet_cool"] = maxf(0.0, float(mv.get("greet_cool", 0.0)) - delta)
			if float(mv["greet_cool"]) <= 0.0 and node.position.distance_to(player.position) < 6.0:
				mv["greet_cool"] = 9.0
				_greet_heart(node.position + Vector3(0, 2.2, 0))

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
	sph.radius = 1.3
	sph.height = 2.6
	mi.mesh = sph
	mi.material_override = pearl_mat
	mi.position = pearl_slots[slot]
	mi.set_meta("slot", slot)
	add_child(mi)
	var l := OmniLight3D.new()
	l.light_color = Color(1.0, 0.8, 1.0)
	l.light_energy = 0.9
	l.omni_range = 7.0
	l.visible = (quality != "speedy") or (slot % 2 == 0)
	l.position = mi.position
	add_child(l)
	pearl_lights.append(l)
	mi.set_meta("light", l)
	mi.set_meta("halo", _halo(mi.position, Color(1.0, 0.75, 0.95), 6.5))
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

func _cutout_tex(name: String) -> Texture2D:
	# STORYBOOK: in-world character cutouts use the die-cut STICKER bake
	# (white vinyl rim + soft navy drop shadow, assets/characters/stickers/,
	# generated from the sacred originals which stay untouched). UI portraits
	# and wardrobe previews keep the clean originals.
	var p := "res://assets/characters/stickers/" + name + ".png"
	if ResourceLoader.exists(p):
		return load(p)
	return load("res://assets/characters/friends/" + name + ".png")

func _build_friends() -> void:
	for i in range(FRIEND_DEFS.size()):
		var fd: Dictionary = FRIEND_DEFS[i]
		var a: float = float(i) / float(FRIEND_DEFS.size()) * TAU + 0.6
		var r: float = 55.0 + float(i % 3) * 30.0
		var x: float = cos(a) * r
		var z: float = sin(a) * r
		var spr := Sprite3D.new()
		spr.texture = _cutout_tex(String(fd["tex"]))
		spr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		spr.pixel_size = 0.016
		spr.position = Vector3(x, seabed_y(x, z) + 6.5, z)
		add_child(spr)
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

func _build_kart_portal() -> void:
	# the Ocean Race gate: a rainbow ring standing just above the REAL seabed near
	# spawn — the race track is built over this world's actual ocean floor
	# open sand flat south of the reef — it used to sit 5 units from Evie's
	# meadow, which crowded her hide-and-seek spot with a race gate
	var pos := Vector3(-5.0, seabed_y(-5.0, -95.0) + 9.0, -95.0)
	kart_portal_pos = pos
	var ring := MeshInstance3D.new()
	var tm := TorusMesh.new()
	tm.inner_radius = 7.0; tm.outer_radius = 9.0; tm.rings = 32; tm.ring_segments = 16
	ring.mesh = tm
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode cull_disabled, unshaded;\nvoid fragment(){ float b=fract(UV.x*6.0); vec3 c; if(b<0.16)c=vec3(0.95,0.2,0.35);else if(b<0.33)c=vec3(1.0,0.6,0.2);else if(b<0.5)c=vec3(1.0,0.92,0.3);else if(b<0.66)c=vec3(0.3,0.85,0.45);else if(b<0.83)c=vec3(0.3,0.6,1.0);else c=vec3(0.65,0.4,0.95); ALBEDO=c; EMISSION=c*(0.6+0.4*sin(TIME*3.0)); }"
	var m := ShaderMaterial.new(); m.shader = sh
	ring.material_override = m
	ring.position = pos
	add_child(ring)
	var lab := Label3D.new()
	lab.text = "Ocean Race!\nSwim in to RACE!"
	lab.font_size = 80; lab.outline_size = 16
	lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lab.position = pos + Vector3(0, 11.0, 0)
	add_child(lab)
	var gl := OmniLight3D.new()
	gl.light_color = Color(1.0, 0.7, 1.0); gl.light_energy = 3.0; gl.omni_range = 30.0
	gl.position = pos
	add_child(gl)
	var tw := ring.create_tween().set_loops()
	tw.tween_property(ring, "rotation:y", TAU, 6.0).from(0.0)

func _kart_gateway(pos: Vector3, label: String, col: Color) -> void:
	# a clear, glowing race portal at a rainbow leg
	var ring := MeshInstance3D.new()
	var tm := TorusMesh.new()
	tm.inner_radius = 5.0; tm.outer_radius = 6.5; tm.rings = 24; tm.ring_segments = 12
	ring.mesh = tm
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nrender_mode cull_disabled, unshaded;\nvoid fragment(){ float b=fract(UV.x*6.0); vec3 c; if(b<0.16)c=vec3(0.95,0.2,0.35);else if(b<0.33)c=vec3(1.0,0.6,0.2);else if(b<0.5)c=vec3(1.0,0.92,0.3);else if(b<0.66)c=vec3(0.3,0.85,0.45);else if(b<0.83)c=vec3(0.3,0.6,1.0);else c=vec3(0.65,0.4,0.95); ALBEDO=c; EMISSION=c*(0.6+0.4*sin(TIME*3.0)); }"
	var m := ShaderMaterial.new(); m.shader = sh
	ring.material_override = m
	ring.position = pos
	add_child(ring); game_nodes.append(ring)
	var lab := Label3D.new()
	lab.text = label; lab.font_size = 64; lab.outline_size = 14
	lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lab.modulate = col
	lab.position = pos + Vector3(0, 8.0, 0)
	add_child(lab); game_nodes.append(lab)
	var gl := OmniLight3D.new()
	gl.light_color = col; gl.light_energy = 3.0; gl.omni_range = 22.0
	gl.position = pos
	add_child(gl); game_nodes.append(gl)
	var tw := ring.create_tween().set_loops()
	tw.tween_property(ring, "rotation:y", TAU, 6.0).from(0.0)

func _start_kart_game(reversed: bool = false, ground: String = "terrain") -> void:
	if hud_layer != null:
		hud_layer.visible = false   # the race draws its own HUD — no overlap
	kart_from = game
	kart_ground = ground
	game = "kart"
	hud_game.text = ""
	kart_game = KartGame.new()
	add_child(kart_game)
	if ground == "float":
		# Level-2 rainbow legs run the classic floating Rainbow Road version
		(kart_game as KartGame).configure({"theme": "rainbow", "ground": "float"})
	player.visible = false   # audit: the real mermaid mesh was left frozen in-frame
	(kart_game as KartGame).start(self, Callable(self, "_end_kart_game"), reversed)

func _end_kart_game(place: int) -> void:
	player.visible = true
	if place == 1:
		award_sticker("racer")
	if hud_layer != null:
		hud_layer.visible = true
	kart_game = null
	kart_cool = 6.0
	var suf: String = ["st", "nd", "rd", "th", "th", "th", "th", "th"][clampi(place - 1, 0, 7)]
	if kart_ground == "float":
		# LEVEL 3: the rainbow road doesn't end — it soars on into Roshan Galaxy
		show_msg("Rainbow Road", "The rainbow road soars on and on... to ROSHAN GALAXY!")
		call_deferred("_start_galaxy")
		return
	var msg := "Ocean Race champion — 1st place!" if place == 1 else "Great racing — you came %d%s!" % [place, suf]
	show_msg("Ocean Race", msg)
	if kart_from == "level2":
		kart_from = ""
		game = ""
		call_deferred("_enter_level2", true)   # rebuild the courtyard cleanly
		return
	kart_from = ""
	game = ""
	_update_hud()

func _start_galaxy() -> void:
	if hud_layer != null:
		hud_layer.visible = false   # the galaxy draws its own HUD — no overlap
	if not galaxy_unlocked:
		galaxy_unlocked = true
		_write_save()
	game = "galaxy"
	hud_game.text = ""
	player.visible = false   # the galaxy has its own avatar
	galaxy_game = GalaxyLevel.new()
	add_child(galaxy_game)
	(galaxy_game as GalaxyLevel).start(self, Callable(self, "_end_galaxy"))

func _end_galaxy(completed: bool) -> void:
	player.visible = true
	if hud_layer != null:
		hud_layer.visible = true
	galaxy_game = null
	game = ""
	if fairy_pending:
		fairy_pending = false
		fairy_from_galaxy = true
		call_deferred("_start_game", fairy_fr)   # straight into the fairy flight
		return
	if completed:
		award_sticker("butterfly")
		show_msg("Mermaid Rosalina", "You saved the Butterfly World! FAIRY ROSHAN is waiting in the castle wardrobe! 🦋", "win")
	else:
		show_msg("Butterfly World", "Home again! The butterflies will wait for your return...")
	_update_hud()
	if kart_from == "level2":
		kart_from = ""
		call_deferred("_enter_level2", true)
		return
	kart_from = ""

const CEL_SHADING := true   # Wind Waker cel post-process (Forward+). Flip false to disable.

func _apply_cel_shading() -> void:
	# Forward+ screen-space cel: one fullscreen quad posterizes the frame into flat
	# toon bands + draws depth-edge ink lines. Brightness-preserving (it rounds colours,
	# it does NOT darken) — the proper fix vs the earlier per-object/lighting approach.
	if not CEL_SHADING:
		return
	var rm := String(ProjectSettings.get_setting_with_override("rendering/renderer/rendering_method"))
	if rm != "forward_plus":
		return   # cel post needs the Forward+ depth buffer; the unified renderer is Mobile (owner 2026-07-11)
	if DisplayServer.get_name() == "headless":
		return   # the dummy renderer can't compile it (probe-log noise otherwise)
	var quad := MeshInstance3D.new()
	var qm := QuadMesh.new()
	qm.size = Vector2(1, 1)
	quad.mesh = qm
	var mat := ShaderMaterial.new()
	mat.shader = load("res://assets/shaders/cel_post.gdshader")
	mat.render_priority = 120          # draw after the scene so it post-processes the frame
	quad.material_override = mat
	quad.extra_cull_margin = 16384.0   # never frustum-cull the fullscreen quad
	add_child(quad)
	cel_post = quad

func _cel_replace(root: Node, outline: ShaderMaterial) -> void:
	for mi in _all_meshes(root):
		var mesh: Mesh = mi.mesh
		if mesh == null:
			continue
		for si in range(mesh.get_surface_count()):
			var m: Material = mi.get_active_material(si)
			if m is BaseMaterial3D:
				var bm := m as BaseMaterial3D
				var cm := ShaderMaterial.new()
				cm.shader = load("res://assets/shaders/cel.gdshader")
				if bm.albedo_texture != null:
					cm.set_shader_parameter("albedo_tex", bm.albedo_texture)
				cm.set_shader_parameter("tint", bm.albedo_color)
				cm.next_pass = outline
				mi.set_surface_override_material(si, cm)

func _cel_outline(root: Node, outline: ShaderMaterial) -> void:
	# additive ink outline only — never changes a material's type (cast-safe)
	for mi in _all_meshes(root):
		var mesh: Mesh = mi.mesh
		if mesh == null:
			continue
		for si in range(mesh.get_surface_count()):
			var m: Material = mi.get_active_material(si)
			if m is BaseMaterial3D and m.next_pass == null:
				m.next_pass = outline

func _all_meshes(root: Node) -> Array:
	var out: Array = []
	var stack: Array = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is MeshInstance3D:
			out.append(n)
		for c in n.get_children():
			stack.append(c)
	return out

func _build_player() -> void:
	player = preload("res://scripts/player.gd").new()
	add_child(player)

func _build_hud() -> void:
	var cl := CanvasLayer.new()
	add_child(cl)
	hud_layer = cl
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
const VOICE_PITCH := {"roshan": 1.18, "huluu": 1.05, "evie": 1.28, "harper": 1.12, "faron": 1.0, "gabby": 1.22, "wacky": 0.7, "chuck": 1.0, "shop": 0.85, "sparkle": 1.35, "rosalina": 1.15, "everyone": 1.1}

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
	"rosalina": "res://assets/characters/skins/fairy_mermaid.png",
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
		# sits ABOVE the hud_msg dialogue line (y630+) — audit: they overlapped
		panel.position = Vector2(24, 370)
		panel.size = Vector2(190, 230)
		speech_layer.add_child(panel)
		speech_portrait = TextureRect.new()
		speech_portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		speech_portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
		speech_portrait.position = Vector2(34, 378)
		speech_portrait.size = Vector2(170, 214)
		speech_layer.add_child(speech_portrait)
		panel.name = "bubble"
	var key := _speaker_key(who)
	var path := String(SPEAKER_PORTRAIT.get(key, SPEAKER_PORTRAIT["roshan"]))
	if ResourceLoader.exists(path):
		speech_portrait.texture = load(path)
	speech_layer.visible = true
	speech_t = 4.0

# Phase 7.5: the audio pipeline lives in scripts/audio_director.gd
# (state stays here; AudioDirector receives main by reference)
var _audio_dir: AudioDirector = null

func _audio_ref() -> AudioDirector:
	if _audio_dir == null:
		_audio_dir = AudioDirector.new(self)
	return _audio_dir

func _say(speaker: String, event: String = "", min_gap: float = 0.0) -> void:
	_audio_ref()._say(speaker, event, min_gap)

func _speaker_key(who: String) -> String:
	return _audio_ref()._speaker_key(who)

func show_msg(who: String, txt: String, vo: String = "talk") -> void:
	_audio_ref().show_msg(who, txt, vo)

func _fanfare() -> void:
	_audio_ref()._fanfare()

func _set_ambience(track: String) -> void:
	_audio_ref()._set_ambience(track)

func _tick_ambience_duck(delta: float) -> void:
	_audio_ref()._tick_ambience_duck(delta)

func _ui_tap() -> void:
	_audio_ref()._ui_tap()

func _hook_button_taps(n: Node) -> void:
	_audio_ref()._hook_button_taps(n)

func _play_music(track: String) -> void:
	_audio_ref()._play_music(track)

func _apply_quality(q: String) -> void:
	quality = q
	var speedy: bool = q == "speedy"
	if sun_light != null:
		sun_light.shadow_enabled = not speedy
	if world_env != null:
		world_env.glow_bloom = 0.0 if speedy else 0.25
		world_env.glow_intensity = 0.7 if speedy else 0.95
	for i in range(pearl_lights.size()):
		var l: OmniLight3D = pearl_lights[i]
		if is_instance_valid(l):
			l.visible = (not speedy) or (i % 2 == 0)
	if plankton_node != null:
		plankton_node.amount_ratio = 0.45 if speedy else 1.0
	for gr in god_rays:
		if is_instance_valid(gr.get("node")):
			(gr["node"] as Node3D).visible = not speedy
	var vp := get_viewport()
	if vp != null:
		vp.scaling_3d_scale = 0.8 if speedy else 1.0
	for fn in flora_nodes:
		if is_instance_valid(fn):
			_set_vis_range(fn, 150.0 if speedy else 0.0)
	if quality_btn != null:
		quality_btn.text = "Graphics: Speedy" if speedy else "Graphics: Sparkly"
	# Phase 5: live-retune the reef water when the tier flips (arena water is
	# rebuilt on entry and picks the tier up itself)
	if water_node != null and water_node.material_override is ShaderMaterial:
		var wm := water_node.material_override as ShaderMaterial
		wm.set_shader_parameter("use_depth", (not speedy) and DisplayServer.get_name() != "headless")

func _set_vis_range(n: Node, dist: float) -> void:
	if n is GeometryInstance3D:
		(n as GeometryInstance3D).visibility_range_end = dist
		(n as GeometryInstance3D).visibility_range_end_margin = 12.0 if dist > 0.0 else 0.0
		(n as GeometryInstance3D).visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF if dist > 0.0 else GeometryInstance3D.VISIBILITY_RANGE_FADE_DISABLED
	for c in n.get_children():
		_set_vis_range(c, dist)

# Phase 7.1: save/load logic lives in scripts/save_state.gd (state stays
# here on main; SaveState receives main by reference and only owns logic)
var _save_state: SaveState = null

func _load_save() -> void:
	if _save_state == null:
		_save_state = SaveState.new(self)
	_save_state.load_save()

func _write_save() -> void:
	if _save_state == null:
		_save_state = SaveState.new(self)
	_save_state.write_save()

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
	pause_panel.position = Vector2(-230, -270)
	pause_panel.size = Vector2(460, 540)   # tall enough for the Sticker Book row
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
	fps_lbl = Label.new()
	fps_lbl.add_theme_font_size_override("font_size", 20)
	fps_lbl.add_theme_color_override("font_color", Color(0.7, 0.85, 1.0))
	fps_lbl.position = Vector2(16, 516)
	pause_panel.add_child(fps_lbl)
	var resume := _pause_btn(vb, "Keep Swimming!")
	var stick_btn := _pause_btn(vb, "⭐ Sticker Book")
	stick_btn.pressed.connect(func():
		toggle_pause()
		_open_stickers())
	resume.pressed.connect(toggle_pause)
	pause_resume_btn = resume
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
	# gamepad menu navigation: focus the first button so D-pad + A work
	if p and pause_resume_btn != null:
		pause_resume_btn.grab_focus()
	elif not p:
		var fo := get_viewport().gui_get_focus_owner()
		if fo != null:
			fo.release_focus()

# Phase 7.4: one file per minigame under scripts/games/ (state stays on
# main; each game class receives main by reference)
var _games := {}

func _game_obj(key: String, cls: Variant) -> Variant:
	if not _games.has(key):
		_games[key] = cls.new(self)
	return _games[key]

func _tick_fetch(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_game_obj("fetch", FetchGame)._tick_fetch(delta, fr, ppos)

func _tick_dolls(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_game_obj("dolls", DollsGame)._tick_dolls(delta, fr, ppos)

func _dolls2d_open(fr: Dictionary) -> void:
	_game_obj("dolls", DollsGame)._dolls2d_open(fr)

func _dolls2d_close() -> void:
	_game_obj("dolls", DollsGame)._dolls2d_close()

func _seek_hide() -> void:
	_game_obj("seek", SeekGame)._seek_hide()

func _tick_course(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_game_obj("race", SlideRaceGame)._tick_course(delta, fr, ppos)

func _tick_shop(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_game_obj("shop", ShopGame)._tick_shop(delta, fr, ppos)

func _shop_buy(id: String) -> void:
	_game_obj("shop", ShopGame)._shop_buy(id)

func _check_shopper() -> void:
	_game_obj("shop", ShopGame)._check_shopper()

func _tick_melody(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_game_obj("melody", MelodyGame)._tick_melody(delta, fr, ppos)

func _tick_fairyshoot(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	_game_obj("fairyshoot", FairyGame)._tick_fairyshoot(delta, fr, _ppos)

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
		portal_node.position.y = seabed_y(portal_node.position.x, portal_node.position.z) + 4.0 + sin(portal_t * 1.2) * 0.6
		portal_ready = true
		portal_cool = maxf(0.0, portal_cool - delta)
		var pdist: float = portal_node.position.distance_to(ppos)
		if pdist > 13.0:
			portal_armed = true
		if portal_ready and portal_armed and portal_cool <= 0.0 and game == "" and finale_t < 0.0 and pdist < 8.0:
			portal_armed = false
			l2_star_progress = [false, false, false]   # fresh visit, fresh stars
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
	lbl.text = "A RAINBOW PORTAL!\nSwim in!"
	lbl.font_size = 80
	lbl.outline_size = 18
	lbl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lbl.position.y = 9.0
	hub.add_child(lbl)
	# the Butterfly Gate stands over the portal — swim through the wings
	var bgate := _butterfly_gate(3.6)
	bgate.position = Vector3(0, 7.0, 0)
	hub.add_child(bgate)
	# a rainbow light beam rises from the portal to the surface — the landmark that
	# calls the player DOWN to the ocean floor from anywhere in the reef
	var beam := MeshInstance3D.new()
	beam.name = "Beam"
	var bc := CylinderMesh.new()
	bc.top_radius = 2.2
	bc.bottom_radius = 4.5
	bc.height = WATER_TOP + 20.0
	bc.radial_segments = 12
	beam.mesh = bc
	var bsh := Shader.new()
	bsh.code = """shader_type spatial;
render_mode blend_add, unshaded, cull_disabled, depth_draw_never;
void fragment(){
	float hue = fract(UV.x + TIME * 0.08);
	vec3 c = clamp(abs(fract(hue + vec3(0.0, 0.666, 0.333)) * 6.0 - 3.0) - 1.0, 0.0, 1.0);
	float fade = smoothstep(0.0, 0.25, UV.y) * smoothstep(1.0, 0.6, UV.y);
	ALBEDO = c * fade * 0.35;
	ALPHA = fade * 0.30;
}"""
	var bmat2 := ShaderMaterial.new()
	bmat2.shader = bsh
	beam.material_override = bmat2
	beam.position.y = (WATER_TOP + 20.0) * 0.5
	hub.add_child(beam)
	# the portal opens ON THE OCEAN FLOOR — the doorway to the Sky Lagoon
	hub.position = Vector3(0, seabed_y(0.0, 0.0) + 4.0, 0)
	add_child(hub)
	portal_node = hub
	show_msg("Roshan", "Wow! A RAINBOW PORTAL is opening deep on the ocean floor! Dive down and swim in!")

func _enter_level2(from_castle: bool = false) -> void:
	game = "level2"
	g = {"t": 0.0}
	arena_solids.clear()
	arena_zones.clear()
	fade_walls.clear()
	lagoon_floor = true   # the courtyard floor follows the rolling-hill terrain
	_play_music("level2")
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
	# Phase 5: a real painted-looking sky — 2K CC0 Poly Haven panoramas
	# (Qwantani pure-sky day + its dusk sister for the bedtime flip). The
	# procedural gradient stays as the fallback if the HDRs ever go missing.
	var pano_path := "res://assets/sky/lagoon_dusk_2k.hdr" if is_night else "res://assets/sky/lagoon_day_2k.hdr"
	if ResourceLoader.exists(pano_path):
		var pano := PanoramaSkyMaterial.new()
		pano.panorama = load(pano_path)
		pano.energy_multiplier = 0.6 if is_night else 1.0   # night stays dim + cosy
		sky.sky_material = pano
	else:
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
	arena_env.glow_enabled = true
	arena_env.glow_intensity = 0.5
	arena_env.glow_bloom = 0.1
	_grade(arena_env)
	we_node.environment = arena_env
	_build_pearl_castle(LEVEL2_POS)
	if is_night:
		_build_lagoon_night(LEVEL2_POS)
	# (Phase 3 fix: a stale _play_music("finale") here overrode the "level2"
	# track selected at the top of this function — the lagoon music never played)
	if from_castle:
		# castle is already won: open the door, hide the collected stars, spawn at the entrance facing the courtyard
		for sd in l2_stars:
			sd["got"] = true
			var sn: Node3D = sd["node"]
			if is_instance_valid(sn):
				sn.visible = false
		l2_open = true
		if g.has("door_solid"):
			arena_solids.erase(g["door_solid"])   # the door is open — no invisible barrier
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

func _build_page_frame() -> void:
	# STORYBOOK DIORAMA FRAMING (fork): every book page has a delicate dotted
	# border and pastel bubble clusters in the corners — the game view gets the
	# same, so play always feels like being INSIDE a page of her book
	var fl := CanvasLayer.new()
	fl.layer = 2
	add_child(fl)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	fl.add_child(root)
	var dot_col := Color(0.35, 0.48, 0.72, 0.30)
	for i in range(46):   # dotted frame: top + bottom edges
		var f2: float = float(i) / 46.0
		for edge in range(2):
			var d1 := ColorRect.new()
			d1.color = dot_col
			d1.mouse_filter = Control.MOUSE_FILTER_IGNORE
			d1.set_anchors_preset(Control.PRESET_TOP_WIDE if edge == 0 else Control.PRESET_BOTTOM_WIDE)
			d1.anchor_left = f2
			d1.anchor_right = f2
			d1.offset_left = 0.0
			d1.offset_right = 5.0
			d1.offset_top = 10.0 if edge == 0 else -15.0
			d1.offset_bottom = d1.offset_top + 5.0
			root.add_child(d1)
	for i in range(24):   # left + right edges
		var f3: float = float(i + 1) / 25.0
		for edge in range(2):
			var d2 := ColorRect.new()
			d2.color = dot_col
			d2.mouse_filter = Control.MOUSE_FILTER_IGNORE
			d2.set_anchors_preset(Control.PRESET_CENTER_LEFT if edge == 0 else Control.PRESET_CENTER_RIGHT)
			d2.anchor_top = f3
			d2.anchor_bottom = f3
			d2.offset_left = 10.0 if edge == 0 else -15.0
			d2.offset_right = d2.offset_left + 5.0
			d2.offset_top = 0.0
			d2.offset_bottom = 5.0
			root.add_child(d2)
	# pastel bubble clusters in two corners (like the book's coral vignettes)
	for ci in range(2):
		var bottom_left: bool = ci == 0
		for bi in range(3):
			var bub := Panel.new()
			var r: float = 26.0 - float(bi) * 7.0
			var sb := StyleBoxFlat.new()
			sb.bg_color = [Color(0.6, 0.85, 0.9, 0.16), Color(0.95, 0.7, 0.8, 0.14), Color(0.75, 0.7, 0.95, 0.15)][bi]
			sb.set_corner_radius_all(int(r))
			bub.add_theme_stylebox_override("panel", sb)
			bub.mouse_filter = Control.MOUSE_FILTER_IGNORE
			bub.set_anchors_preset(Control.PRESET_BOTTOM_LEFT if bottom_left else Control.PRESET_TOP_RIGHT)
			var bx: float = 20.0 + float(bi) * 40.0
			var by: float = 34.0 + float(bi) * 26.0
			bub.offset_left = bx if bottom_left else -bx - r * 2.0
			bub.offset_right = bub.offset_left + r * 2.0
			bub.offset_top = (-by - r * 2.0) if bottom_left else by
			bub.offset_bottom = bub.offset_top + r * 2.0
			root.add_child(bub)

func _butterfly_gate(scl: float) -> Node3D:
	# the BUTTERFLY GATE (Blender-built: wing-flanked pearl ring) + a swirling
	# rainbow film inside — the game's signature doorway between worlds
	var root := Node3D.new()
	if ResourceLoader.exists("res://assets/portal/butterfly_gate.glb"):
		var gg: Node3D = (load("res://assets/portal/butterfly_gate.glb") as PackedScene).instantiate()
		root.add_child(gg)
	var swirl := MeshInstance3D.new()
	var qm := QuadMesh.new()
	qm.size = Vector2(1.84, 1.84)
	swirl.mesh = qm
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode blend_add, unshaded, cull_disabled, depth_draw_never;
void fragment(){
	vec2 c = UV - vec2(0.5);
	float r = length(c) * 2.0;
	float hue = fract(r * 0.7 - TIME * 0.14 + atan(c.y, c.x) / 6.2831);
	float b6 = hue * 6.0;
	vec3 col = clamp(vec3(abs(b6 - 3.0) - 1.0, 2.0 - abs(b6 - 2.0), 2.0 - abs(b6 - 4.0)), 0.0, 1.0);
	ALBEDO = col * (1.0 - smoothstep(0.82, 1.0, r)) * 0.75;
}"""
	var sm := ShaderMaterial.new()
	sm.shader = sh
	swirl.material_override = sm
	root.add_child(swirl)
	root.scale = Vector3.ONE * scl
	return root

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

# Phase 7.3: the Sky Lagoon lives in scripts/arena/sky_lagoon.gd
# (state stays here; SkyLagoon receives main by reference)
var _sky_lagoon: SkyLagoon = null

func _lagoon_ref() -> SkyLagoon:
	if _sky_lagoon == null:
		_sky_lagoon = SkyLagoon.new(self)
	return _sky_lagoon

func _build_pearl_castle(o: Vector3) -> void:
	_lagoon_ref()._build_pearl_castle(o)

func _build_lagoon_terrain(o: Vector3) -> void:
	_lagoon_ref()._build_lagoon_terrain(o)

func _build_lagoon_night(o: Vector3) -> void:
	_lagoon_ref()._build_lagoon_night(o)

func _build_fairy_pond(o: Vector3) -> void:
	_lagoon_ref()._build_fairy_pond(o)

func _tick_level2(delta: float, ppos: Vector3) -> void:
	_lagoon_ref()._tick_level2(delta, ppos)

func _l2_tower(pos: Vector3, sc: float = 1.0) -> void:
	_lagoon_ref()._l2_tower(pos, sc)

func _seg_dist(p: Vector2, a: Vector2, b: Vector2) -> float:
	return _lagoon_ref()._seg_dist(p, a, b)

func _lagoon_river_dip(lx: float, lz: float) -> float:
	return _lagoon_ref()._lagoon_river_dip(lx, lz)

func _lagoon_moat_dip(lx: float, lz: float) -> float:
	return _lagoon_ref()._lagoon_moat_dip(lx, lz)

func _lagoon_bump(lx: float, lz: float, cx: float, cz: float, rad: float, amp: float) -> float:
	return _lagoon_ref()._lagoon_bump(lx, lz, cx, cz, rad, amp)

func _lagoon_local(lx: float, lz: float) -> float:
	return _lagoon_ref()._lagoon_local(lx, lz)

func _terr_v(st: SurfaceTool, lx: float, lz: float, y: float) -> void:
	_lagoon_ref()._terr_v(st, lx, lz, y)

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

var _kit_cache := {}

func _kit(name: String, pos: Vector3, target: float, yrot: float = 0.0) -> Node3D:
	# instantiate a CC0 kit piece (assets/kits/<name>.glb), restyle it for the
	# storybook look (_fit_prop calls _toonify), fit its footprint to `target`
	# units and seat its base at pos. Collision stays the caller's job — solids
	# are hand-placed so gameplay clearances remain explicit.
	var ps: PackedScene = _kit_cache.get(name, null)
	if ps == null:
		var path := "res://assets/kits/" + name + ".glb"
		if not ResourceLoader.exists(path):
			return null
		ps = load(path)
		_kit_cache[name] = ps
	if ps == null:
		return null
	var wrap := Node3D.new()
	var inst: Node3D = ps.instantiate()
	_fit_prop(inst, target)
	wrap.add_child(inst)
	wrap.position = pos
	wrap.rotation.y = yrot
	add_child(wrap)
	game_nodes.append(wrap)
	return wrap

var _gen2_cache := {}
const GEN2_CEL := true   # banded cel light + navy ink outline on GEN2 props. Flip false to revert.
var _gen2_outline: ShaderMaterial = null

var _seagrass_mats: Array = []   # a few shared sway materials (phase variety)

func _gen2_seagrass(pos: Vector3, size: float) -> Node3D:
	# GEN2 sea grass: the family-style seaweed sprite on two crossed quads with
	# a vertex-sine sway (assets/shaders/seagrass_sway.gdshader). Returns null
	# if the sprite is missing so callers can fall back to the old GLB pack.
	if not ResourceLoader.exists("res://assets/props/gen2/seagrass.png"):
		return null
	if _seagrass_mats.is_empty():
		for i in range(4):
			var sm := ShaderMaterial.new()
			sm.shader = load("res://assets/shaders/seagrass_sway.gdshader")
			sm.set_shader_parameter("tex", load("res://assets/props/gen2/seagrass.png"))
			sm.set_shader_parameter("phase", float(i) * 1.7)
			sm.set_shader_parameter("sway_amount", 0.22 + 0.07 * float(i))
			_seagrass_mats.append(sm)
	var wrap := Node3D.new()
	var qm := QuadMesh.new()
	qm.size = Vector2(size, size * 0.82)   # sprite aspect 892x735
	for q in range(2):
		var mi := MeshInstance3D.new()
		mi.mesh = qm
		mi.material_override = _seagrass_mats[randi() % _seagrass_mats.size()]
		mi.rotation.y = PI * 0.5 * float(q) + randf() * 0.4
		mi.position.y = size * 0.82 * 0.5 - 0.15   # seat the base just in the sand
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		wrap.add_child(mi)
	wrap.position = pos
	add_child(wrap)
	flora_nodes.append(wrap)
	return wrap

func _gen2_outline_mat() -> ShaderMaterial:
	if _gen2_outline == null:
		_gen2_outline = ShaderMaterial.new()
		_gen2_outline.shader = load("res://assets/shaders/outline.gdshader")
		# navy/purple ink per the art direction (not black)
		_gen2_outline.set_shader_parameter("line_color", Color(0.16, 0.12, 0.3))
	return _gen2_outline

func _gen2_prop(name: String, pos: Vector3, target: float, yrot: float = 0.0, sink: float = 0.0) -> Node3D:
	# GEN2 pipeline prop (assets/props/gen2/<name>.glb): art generated in the
	# family storybook style, audited, converted to 3D (Meshy) and shrunk for
	# the phone (tools/shrink_glb.py). Same contract as _kit: fits footprint
	# to `target`, seats base at pos; collisions and node-list registration
	# (game_nodes/flora_nodes) stay the caller's job.
	var ps: PackedScene = _gen2_cache.get(name, null)
	if ps == null:
		var path := "res://assets/props/gen2/" + name + ".glb"
		if not ResourceLoader.exists(path):
			return null
		ps = load(path)
		_gen2_cache[name] = ps
	if ps == null:
		return null
	var wrap := Node3D.new()
	var inst: Node3D = ps.instantiate()
	var h: float = _fit_prop(inst, target)
	if GEN2_CEL:
		# WW toon-bake 2/2: flat posterized albedo (shrink pass) + banded cel
		# light + inverted-hull navy outline. GEN2 props only — bounded, one
		# const to revert, per CEL_SHADING.md's incremental wiring plan.
		_cel_replace(inst, _gen2_outline_mat())
	wrap.add_child(inst)
	# sink settles the prop into the ground by a fraction of its height —
	# Meshy meshes have smooth rounded bases that only kiss the terrain at one
	# tangent point and read as floating on any slope (playtest 2026-07-10)
	wrap.position = pos - Vector3(0.0, h * sink, 0.0)
	wrap.rotation.y = yrot
	add_child(wrap)
	return wrap

func _pastel(c: Color) -> Color:
	# the book palette: colours drift toward airy pastel (lifted, softened)
	# while keeping their hue identity — rainbow saturation stays on CHARACTERS
	var h := c.h
	var s: float = minf(c.s * 0.82, 0.62)
	var v: float = clampf(c.v * 0.9 + 0.16, 0.0, 1.0)
	return Color.from_hsv(h, s, v, c.a)

func _dress_nature(node: Node) -> void:
	# STORYBOOK FORK: flat pastel toon materials — no realistic texture detail
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
				nm.albedo_color = _pastel(col)
				nm.roughness = 1.0
				nm.metallic_specular = 0.1
				mi.set_surface_override_material(si, nm)
	for c in node.get_children():
		_dress_nature(c)

func _toonify(node: Node) -> void:
	# restyle any imported CC0 prop for the storybook look: strip realistic
	# maps, flatten speculars, pastel-shift the albedo. Character art (Sprite3D
	# cutouts) is untouched — cutouts stay unshaded and visually dominant.
	if node is MeshInstance3D:
		var mi := node as MeshInstance3D
		if mi.material_override is StandardMaterial3D:
			var mo := mi.material_override as StandardMaterial3D
			mo.normal_enabled = false
			mo.roughness = 1.0
			mo.metallic = 0.0
			mo.albedo_color = _pastel(mo.albedo_color)
		elif mi.mesh != null:
			for si in range(mi.mesh.get_surface_count()):
				var sm0: Material = mi.get_surface_override_material(si)
				if sm0 == null:
					sm0 = mi.mesh.surface_get_material(si)
				if sm0 is StandardMaterial3D:
					var m2 := (sm0 as StandardMaterial3D).duplicate() as StandardMaterial3D
					m2.normal_enabled = false
					m2.roughness = 1.0
					m2.metallic = 0.0
					m2.metallic_specular = 0.1
					m2.albedo_color = _pastel(m2.albedo_color)
					mi.set_surface_override_material(si, m2)
	for c in node.get_children():
		_toonify(c)

# ===================== SKY LAGOON HEIGHTFIELD TERRAIN =====================
# Real rolling hills (solid land Roshan rests on) + rivers carved as genuine
# valleys she swims down into. The player floor follows lagoon_h() in the courtyard.
const LAGOON_RIVERS := [
	[Vector2(-210, -40), Vector2(-150, 30), Vector2(-90, 100), Vector2(-30, 170)],
	[Vector2(205, -30), Vector2(150, 40), Vector2(95, 110), Vector2(45, 180)]]
const LAGOON_RIVER_W := 17.0
const LAGOON_RIVER_DEPTH := 12.0   # was 18: that carved bare-walled canyons that no water sheet could ever look right in
# Castle moat: a ring channel carved around the keep, with a hidden door at its floor.
const MOAT_CX := 0.0
const MOAT_CZ := -120.0      # local (relative to LEVEL2_POS); matches the castle base
const MOAT_INNER := 46.0     # clears the keep + the four corner towers
const MOAT_OUTER := 64.0
const MOAT_DEPTH := 16.0
# Dream-Star platform spots (local to LEVEL2_POS) — shared by the builder and lagoon_walk_h
const L2_STAR_SPOTS: Array = [Vector3(-22, 5, 95), Vector3(24, 5, 20), Vector3(-20, 5, -55)]

func lagoon_h(x: float, z: float) -> float:
	return LEVEL2_POS.y + _lagoon_local(x - LEVEL2_POS.x, z - LEVEL2_POS.z)

func lagoon_walk_h(x: float, z: float) -> float:
	# The surface the PLAYER stands on in the Sky Lagoon: the terrain, plus the
	# wooden bridge deck and the Dream-Star platforms, so Roshan crosses the moat
	# on the bridge instead of sinking through it. Off the bridge the moat is
	# still an open, divable trench (that's how you find the secret hatch).
	var lx: float = x - LEVEL2_POS.x
	var lz: float = z - LEVEL2_POS.z
	var h: float = _lagoon_local(lx, lz)
	if absf(lx) <= 6.5 and lz >= -110.0 and lz <= -50.0:
		h = maxf(h, 3.0)   # bridge deck top: c+(0,2.6,40), 0.8 thick, 13 wide, 60 long
	for sp: Vector3 in L2_STAR_SPOTS:
		if absf(lx - sp.x) <= 6.0 and absf(lz - sp.z) <= 6.0:
			h = maxf(h, 2.2)   # star platform top (12 x 1.4 x 12 box at spot - 3.5)
	return LEVEL2_POS.y + h

# Phase 7.4b: the 2D picture games live in scripts/games/picture_games.gd
func _pics_ref() -> PictureGames:
	return _game_obj("pics", PictureGames)

func _mg2d_open(kind: String) -> void:
	_pics_ref()._mg2d_open(kind)

func _mg2d_close() -> void:
	_pics_ref()._mg2d_close()

func _mg_tick_snow_chase(delta: float) -> void:
	_pics_ref()._mg_tick_snow_chase(delta)

func _mg2d_win(msg: String) -> void:
	_pics_ref()._mg2d_win(msg)

func _mg_snow_ball_size(ball: Panel, r: float, center: Vector2) -> void:
	_pics_ref()._mg_snow_ball_size(ball, r, center)

func _mg_snow_ball_done() -> void:
	_pics_ref()._mg_snow_ball_done()

const SNOW_ROLL_C := Vector2(420, 500)   # where the growing snowball sits

func _tick_mg2d(delta: float) -> void:
	if mg_kind == "":
		return
	mg["t"] = float(mg["t"]) + delta
	# ---- controller support for the tap overlays: A presses the next available
	# ---- button, B closes the game — pad-only setups are never stuck
	if not bool(mg.get("won", false)):
		var apress: bool = joy_pressed(JOY_BUTTON_A)
		if apress and not bool(mg.get("joyA", false)) and not pad_cursor_active:
			# blind quick-press (first available button) only while the star
			# cursor is asleep — once it wakes, A clicks AT the cursor instead
			for b in (mg.get("btns", []) as Array):
				if b is Button and is_instance_valid(b) and (b as Button).visible and not (b as Button).disabled:
					(b as Button).pressed.emit()
					break
		mg["joyA"] = apress
		var bpress: bool = joy_pressed(JOY_BUTTON_B)
		if bpress and not bool(mg.get("joyB", false)) and float(mg["t"]) > 0.6:
			_mg2d_close()
			return
		mg["joyB"] = bpress
	if mg_kind == "snowman" and String(mg.get("phase", "")) in ["chase", "carrot"]:
		_mg_tick_snow_chase(delta)
	if mg_kind == "snowman" and String(mg.get("phase", "")) == "roll" and mg.has("roll_ball"):
		var t2: float = float(mg["t"])
		# flashing banner: pulse alpha + a little breathe
		var fl: Label = mg.get("flash")
		if fl != null and is_instance_valid(fl):
			fl.modulate = Color(1, 1, 1, 0.5 + 0.5 * (0.5 + 0.5 * sin(t2 * 7.0)))
			fl.scale = Vector2.ONE * (1.0 + 0.05 * sin(t2 * 7.0))
		# read a rotation angle: analog stick spun in circles, or a finger/mouse
		# drawing circles around the snowball
		var ang_ok := false
		var ang := 0.0
		var jv := Vector2(joy_axis(JOY_AXIS_LEFT_X), joy_axis(JOY_AXIS_LEFT_Y))
		if jv.length() > 0.35:   # little thumbs: was 0.45, half-pushed circles count too
			ang = jv.angle()
			ang_ok = true
		elif Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and mg2d_stage != null:
			var mp: Vector2 = mg2d_stage.get_local_mouse_position()
			var off: Vector2 = mp - SNOW_ROLL_C
			if off.length() > 30.0 and off.length() < 460.0:
				ang = off.angle()
				ang_ok = true
		if ang_ok:
			if mg.get("prev_ang") != null:
				var dphi: float = wrapf(ang - float(mg["prev_ang"]), -PI, PI)
				dphi = clampf(dphi, -0.32, 0.32)   # ignore teleport-y jumps
				mg["rot_acc"] = float(mg["rot_acc"]) + absf(dphi)
			mg["prev_ang"] = ang
		else:
			mg["prev_ang"] = null
		# grow the snowball with the accumulated rotation
		var prog: float = clampf(float(mg["rot_acc"]) / float(mg["rot_need"]), 0.0, 1.0)
		var r: float = lerpf(26.0, float(mg["final_r"]), prog)
		_mg_snow_ball_size(mg["roll_ball"], r, SNOW_ROLL_C)
		# struggle helper: the circle gesture is the one real motor skill in the
		# 2D games — if no progress for 8s, the spin arrow doubles in size and
		# Roshan chirps encouragement so a stuck kid gets a nudge, not a wall
		var stall: float = float(mg.get("stall", 0.0))
		if float(mg["rot_acc"]) > float(mg.get("stall_acc", 0.0)) + 0.3:
			mg["stall_acc"] = mg["rot_acc"]
			stall = 0.0
		else:
			stall += delta
		var assist: bool = stall > 8.0
		if assist and stall - delta <= 8.0 and voice != null:
			voice.pitch_scale = 1.3
			voice.play()
		mg["stall"] = stall
		# crunchy tick every half circle so the rolling feels alive
		if int(float(mg["rot_acc"]) / PI) > int(float(mg["rot_prev"]) / PI) and chime != null:
			chime.pitch_scale = 0.8 + prog * 0.35
			chime.play()
		mg["rot_prev"] = mg["rot_acc"]
		# hint arrow orbits the growing ball
		var ar: Label = mg.get("hint_arrow")
		if ar != null and is_instance_valid(ar):
			var oa: float = t2 * 2.6
			ar.position = SNOW_ROLL_C + Vector2(cos(oa), sin(oa)) * (r + 58.0) - Vector2(28, 46)
			ar.rotation = oa + PI * 0.5
			ar.scale = ar.scale.lerp(Vector2.ONE * (2.0 if assist else 1.0), delta * 5.0)
		if prog >= 1.0:
			_mg_snow_ball_done()
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
	if g.has("door_solid"):
		arena_solids.erase(g["door_solid"])   # the open doorway is passable again
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

func _enter_castle_interior(from_back: bool = false) -> void:
	_play_music("hall")
	g["l2_fish"] = []
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	arena_solids.clear()
	arena_zones.clear()
	fade_walls.clear()
	lagoon_floor = false   # the castle hall is flat indoor ground
	g["phase"] = "hall"
	arena_center = CASTLE_POS
	arena_dome = 90.0   # covers the bedroom, the new top chambers and the undercroft
	arena_ceil = 31.0   # keep Roshan below every interior ceiling (lowest sits at +32) instead of clipping through
	# warm indoor castle light
	var ie := Environment.new()
	ie.background_mode = Environment.BG_COLOR
	ie.background_color = Color(0.12, 0.10, 0.16)
	ie.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	ie.ambient_light_color = Color(0.9, 0.82, 0.7)
	ie.ambient_light_energy = 0.8
	ie.glow_enabled = true
	ie.glow_intensity = 0.6
	ie.glow_bloom = 0.12
	ie.fog_enabled = true
	ie.fog_light_color = Color(0.5, 0.42, 0.45)
	ie.fog_density = 0.006
	arena_env = ie
	_grade(ie)
	we_node.environment = ie
	_build_castle_hall(CASTLE_POS)
	player.cam_back = 10.0   # pull the chase camera in so it does not clip the hall / back-room walls (diorama lens: 6.5 * ~1.55)
	player.cam_high = 4.2
	if from_back:
		# the moat hatch is a SECRET back door: surface inside the treasure room
		# behind the throne, where Daddy mermaid is waiting
		player.position = CASTLE_POS + Vector3(4, 6, -44)
		player.yaw = PI
		player.vel = Vector3.ZERO
		g["secret_armed"] = false   # don't fire the treasure-chest surprise on arrival
		show_msg("Daddy", "Pssst... you found my secret door, Roshan! Welcome to the treasure room - Huluu is out on her throne!", "greet")
	else:
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

# Phase 7.2: the Grand Hall lives in scripts/arena/castle_hall.gd
# (state stays here; CastleHall receives main by reference)
var _castle_hall: CastleHall = null

func _hall_ref() -> CastleHall:
	if _castle_hall == null:
		_castle_hall = CastleHall.new(self)
	return _castle_hall

func _build_castle_hall(o: Vector3) -> void:
	_hall_ref().build(o)
	_hall_ref().build_expansion(o)

func _tick_castle_hall(delta: float, ppos: Vector3) -> void:
	_hall_ref().tick(delta, ppos)

func _build_castle_music_room(o: Vector3) -> void:
	_hall_ref().build_music_room(o)

func _build_castle_bedroom(o: Vector3) -> void:
	_hall_ref().build_bedroom(o)

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

func _find_skel(n: Node) -> Skeleton3D:
	if n is Skeleton3D:
		return n
	for c in n.get_children():
		var r := _find_skel(c)
		if r != null:
			return r
	return null

func _ring_bell(bd: Dictionary) -> void:
	(bd["player"] as AudioStreamPlayer).play()
	var bn: Node3D = bd["node"]
	var base_y: float = float(bd.get("base_y", 5.0))
	if bd.get("tw") != null and (bd["tw"] as Tween).is_valid():
		(bd["tw"] as Tween).kill()
	bn.position.y = base_y
	var bbtw: Tween = bn.create_tween()
	bbtw.tween_property(bn, "position:y", base_y - 1.6, 0.06)
	bbtw.tween_property(bn, "position:y", base_y, 0.16)
	bd["tw"] = bbtw
	_sparkle_burst(bn.position + Vector3(0, 4, 0), (bn.material_override as StandardMaterial3D).albedo_color)

func _tick_bellgame(bg2: Dictionary, delta: float, ppos: Vector3) -> void:
	if bg2.is_empty():
		return
	bg2["cool"] = maxf(0.0, float(bg2["cool"]) - delta)
	var st := String(bg2["state"])
	if st == "idle":
		if float(bg2["cool"]) <= 0.0 and g.has("song_star") and (g["song_star"] as Vector3).distance_to(ppos) < 5.0:
			bg2["round"] = 0
			show_msg("Music Room", "The bells want to sing you a song! Listen... then copy it!")
			_bellgame_new_round(bg2)
	elif st == "play":
		bg2["t"] = float(bg2["t"]) - delta
		if float(bg2["t"]) <= 0.0:
			var seq: Array = bg2["seq"]
			var i: int = int(bg2["i"])
			if i < seq.size():
				_ring_bell((g["bells"] as Array)[int(seq[i])])
				bg2["i"] = i + 1
				bg2["t"] = 0.75
			else:
				bg2["state"] = "echo"
				bg2["i"] = 0
				show_msg("Music Room", "Your turn! Ring the bells in the same order!")

func _bellgame_new_round(bg2: Dictionary) -> void:
	bg2["round"] = int(bg2["round"]) + 1
	var seq: Array = []
	var prev := -1
	for i in range(int(bg2["round"]) + 1):
		# no note twice in a row — the echo is edge-triggered (leave + re-enter
		# the same bell would stump a little player)
		var pick := randi() % 7
		while pick == prev:
			pick = randi() % 7
		seq.append(pick)
		prev = pick
	bg2["seq"] = seq
	bg2["state"] = "play"
	bg2["i"] = 0
	bg2["t"] = 1.1

func _bellgame_echo(bg2: Dictionary, bell_idx: int) -> void:
	var seq: Array = bg2["seq"]
	var i: int = int(bg2["i"])
	if i >= seq.size():
		return
	if bell_idx == int(seq[i]):
		bg2["i"] = i + 1
		if int(bg2["i"]) >= seq.size():
			if int(bg2["round"]) >= 3:
				bg2["state"] = "idle"
				bg2["cool"] = 30.0
				pearl_count += 2
				_write_save()
				_update_hud()
				_reward()
				award_sticker("bells")
				show_msg("Music Room", "You played the WHOLE bell song! +2 rainbow pearls!", "win")
			else:
				if chime != null:
					chime.pitch_scale = 1.4
					chime.play()
				show_msg("Music Room", "Beautiful! Now a longer one — listen!")
				_bellgame_new_round(bg2)
	else:
		if chime != null:
			chime.pitch_scale = 0.5
			chime.play()
		show_msg("Music Room", "Almost! Listen to the song one more time...", "oops")
		bg2["state"] = "play"
		bg2["i"] = 0
		bg2["t"] = 1.2

func _begin_sleep() -> void:
	# tuck-in cutscene: Roshan snuggles onto the bed, Zzz's float up, the screen
	# fades, day flips to night (or night to day), and she wakes refreshed
	award_sticker("sleepy")
	_play_music("home")   # A Place I Call Home — the tuck-in lullaby
	sleep_t = 0.0
	sleep_flip_done = false
	var bp: Vector3 = g["bed_pos"]
	player.position = bp + Vector3(0, 1.0, 0.4)
	player.vel = Vector3.ZERO
	player.rotation_degrees = Vector3(-64, 180, 0)   # reclined on the pillow
	if chime != null:
		chime.pitch_scale = 0.9
		chime.play()
	hud_game.text = ""
	show_msg("Roshan", "Time for a cosy little sleep... zZz")

func _sleep_z() -> void:
	var z := Label3D.new()
	z.text = "z"
	z.font_size = 90 + randi() % 60
	z.outline_size = 14
	z.modulate = Color(0.75, 0.85, 1.0)
	z.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	var bp: Vector3 = g["bed_pos"]
	z.position = bp + Vector3(randf() * 2.0 - 1.0, 2.5, randf() * 2.0 - 1.0)
	add_child(z)
	var tw := z.create_tween()
	tw.tween_property(z, "position:y", z.position.y + 5.0, 1.6)
	tw.parallel().tween_property(z, "modulate:a", 0.0, 1.6)
	tw.tween_callback(z.queue_free)

func _tick_sleep(delta: float) -> void:
	sleep_t += delta
	# slow breathing bob while she drifts off
	if player != null and g.has("bed_pos"):
		player.position.y = float((g["bed_pos"] as Vector3).y) + 1.0 + sin(sleep_t * 1.5) * 0.12
	if fmod(sleep_t, 0.8) < delta and sleep_t < 3.2:
		_sleep_z()
		if chime != null and sleep_t > 0.5:
			chime.pitch_scale = 0.85 - sleep_t * 0.06   # descending lullaby notes
			chime.play()
	if sleep_t >= 2.4 and sleep_layer == null:
		# dream-fade to deep sleepy indigo
		sleep_layer = CanvasLayer.new()
		sleep_layer.layer = 24
		add_child(sleep_layer)
		sleep_overlay = ColorRect.new()
		sleep_overlay.color = Color(0.03, 0.02, 0.10, 0.0)
		sleep_overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
		sleep_layer.add_child(sleep_overlay)
		var tw := sleep_overlay.create_tween()
		tw.tween_property(sleep_overlay, "color:a", 1.0, 0.9)
	if sleep_t >= 3.6 and not sleep_flip_done:
		sleep_flip_done = true
		_set_night(not is_night)   # the whole ocean changes while she dreams
	if sleep_t >= 4.6 and sleep_overlay != null and sleep_overlay.color.a >= 0.99:
		var tw2 := sleep_overlay.create_tween()
		tw2.tween_property(sleep_overlay, "color:a", 0.0, 1.0)
		sleep_overlay.color.a = 0.98   # nudge below the gate so this runs once
	if sleep_t >= 6.0:
		_end_sleep()

func _end_sleep() -> void:
	sleep_t = -1.0
	sleep_cool = 18.0
	_play_music("hall")   # lullaby over — back to the castle theme
	if sleep_layer != null and is_instance_valid(sleep_layer):
		sleep_layer.queue_free()
	sleep_layer = null
	sleep_overlay = null
	if player != null:
		player.rotation_degrees = Vector3.ZERO
		if g.has("bed_pos"):
			player.position = (g["bed_pos"] as Vector3) + Vector3(-5.0, 1.0, 3.0)
		player.vel = Vector3.ZERO
	_sparkle_burst(player.position + Vector3(0, 2, 0), Color(0.8, 0.9, 1.0))
	if is_night:
		show_msg("Roshan", "What a lovely nap! It's NIGHT now - the ocean is full of moonbeams and glowing jellyfish!", "win")
	else:
		show_msg("Roshan", "Good morning! The sun is shining over the reef again!", "win")

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
	player.cam_back = 25.0   # diorama lens default
	player.cam_high = 6.5
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	_enter_level2(true)

func _play_hug_cutscene() -> void:
	award_sticker("hug")
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
	daddy.texture = _cutout_tex("daddy")
	daddy.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	daddy.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	daddy.size = Vector2(vp.y * 0.62, vp.y * 0.9)
	daddy.position = Vector2(-daddy.size.x, vp.y * 0.1)
	root.add_child(daddy)
	# Roshan slides in from the right
	var rosh := TextureRect.new()
	rosh.texture = load(skin_sprite_path())
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

func _make_creature_node(kind: String, body: Color, accent: Color) -> Node3D:
	var ln: Array = CREATURE_LAYERS.get(kind, CREATURE_LAYERS["fish"])
	var root := Node3D.new()
	var acca := 1.0   # accents are separate zones now — draw them pure, no blending
	var lb := Sprite3D.new()
	lb.texture = load("res://assets/mg/" + String(ln[1]) + ".png"); lb.modulate = body
	lb.billboard = BaseMaterial3D.BILLBOARD_ENABLED; lb.pixel_size = 0.02; lb.render_priority = 0
	root.add_child(lb)
	var la := Sprite3D.new()
	la.texture = load("res://assets/mg/" + String(ln[0]) + ".png"); la.modulate = Color(accent.r, accent.g, accent.b, acca)
	la.billboard = BaseMaterial3D.BILLBOARD_ENABLED; la.pixel_size = 0.02; la.render_priority = 1
	la.set_meta("rb", false)
	root.add_child(la)
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
	var acca := 1.0
	var order := [String(ln[1]), String(ln[0]), String(ln[2])]
	var roles := ["body", "accent", "line"]
	var cols := [craft_body, Color(craft_fins.r, craft_fins.g, craft_fins.b, acca), Color(1, 1, 1)]
	for i in range(3): 
		var tr := TextureRect.new(); tr.texture = load("res://assets/mg/" + order[i] + ".png")
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE; tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		tr.size = craft_fishbox.size; tr.modulate = cols[i]; tr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		tr.set_meta("role", roles[i]); craft_fishbox.add_child(tr)

func _open_craft_studio() -> void:
	if craft_layer != null:
		return
	craft_kind = "fish"
	craft_body = Color(0.4, 0.7, 1.0)
	craft_fins = Color(1.0, 0.6, 0.2)
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
	title.add_to_group("craft_top")   # hidden when the farewell banner appears
	# creature-type buttons — Kitty and Birdie are one-time rainbow-pearl unlocks
	var kinds := [["fish", "Fishy", 0], ["cat", "Kitty", 5], ["bird", "Birdie", 8]]
	for ki in range(kinds.size()):
		var kk: String = String(kinds[ki][0])
		var knm: String = String(kinds[ki][1])
		var kpr: int = int(kinds[ki][2])
		var locked: bool = kpr > 0 and not bool(craft_unlocks.get(kk, false))
		var kb := Button.new(); kb.text = knm; kb.add_theme_font_size_override("font_size", 36)
		kb.position = Vector2(760.0 + float(ki) * 165.0, 14.0); kb.custom_minimum_size = Vector2(155, 64)
		var ksb := StyleBoxFlat.new(); ksb.bg_color = Color(0.32, 0.34, 0.48) if locked else Color(0.4, 0.45, 0.7); ksb.set_corner_radius_all(18)
		kb.add_theme_stylebox_override("normal", ksb); kb.add_theme_stylebox_override("hover", ksb); kb.add_theme_stylebox_override("pressed", ksb)
		kb.set_meta("style", ksb)
		if locked:
			kb.modulate = Color(0.78, 0.78, 0.85)
			var tag := Label.new(); tag.text = "%d pearls" % kpr
			tag.add_theme_font_size_override("font_size", 24)
			tag.add_theme_color_override("font_color", Color(1.0, 0.82, 1.0))
			tag.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); tag.add_theme_constant_override("outline_size", 6)
			tag.position = Vector2(kb.position.x + 28.0, 80.0)
			stage.add_child(tag)
			tag.add_to_group("craft_top")
			kb.set_meta("price_tag", tag)
		kb.pressed.connect(func(): _craft_pick_kind(kk, knm, kpr, kb))
		stage.add_child(kb)
		kb.add_to_group("craft_top")
	# pearl purse + feedback line (the normal HUD sits behind this overlay)
	craft_pearl_lbl = Label.new(); craft_pearl_lbl.text = "Rainbow pearls: %d" % pearl_count
	craft_pearl_lbl.add_theme_font_size_override("font_size", 28)
	craft_pearl_lbl.add_theme_color_override("font_color", Color(1.0, 0.85, 1.0))
	craft_pearl_lbl.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); craft_pearl_lbl.add_theme_constant_override("outline_size", 8)
	craft_pearl_lbl.position = Vector2(64, 86); stage.add_child(craft_pearl_lbl)
	craft_status = Label.new()
	craft_status.add_theme_font_size_override("font_size", 30)
	craft_status.add_theme_color_override("font_outline_color", Color(0.05, 0.05, 0.15)); craft_status.add_theme_constant_override("outline_size", 8)
	craft_status.position = Vector2(40, 240); craft_status.custom_minimum_size = Vector2(370, 200)
	craft_status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	stage.add_child(craft_status)
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
	var done := Button.new(); done.text = "  Done!  "; done.add_theme_font_size_override("font_size", 46)
	done.position = Vector2(1050, 330); done.custom_minimum_size = Vector2(190, 130)
	var dsb := StyleBoxFlat.new(); dsb.bg_color = Color(0.3, 0.8, 0.4); dsb.set_corner_radius_all(30)
	done.add_theme_stylebox_override("normal", dsb); done.add_theme_stylebox_override("hover", dsb); done.add_theme_stylebox_override("pressed", dsb)
	done.pressed.connect(_craft_done); stage.add_child(done)

func _craft_pick_kind(kk: String, knm: String, price: int, kb: Button) -> void:
	if price > 0 and not bool(craft_unlocks.get(kk, false)):
		if pearl_count < price:
			if craft_status != null and is_instance_valid(craft_status):
				craft_status.text = "%s costs %d rainbow pearls. You have %d - the reef is full of them!" % [knm, price, pearl_count]
			if chime != null:
				chime.pitch_scale = 0.7
				chime.play()
			return
		pearl_count -= price
		craft_unlocks[kk] = true
		_write_save()
		_update_hud()
		if chime != null:
			chime.pitch_scale = 1.5
			chime.play()
		kb.modulate = Color(1, 1, 1)
		var sb: StyleBoxFlat = kb.get_meta("style", null)
		if sb != null:
			sb.bg_color = Color(0.4, 0.45, 0.7)
		var tag: Label = kb.get_meta("price_tag", null)
		if tag != null and is_instance_valid(tag):
			tag.queue_free()
		if craft_pearl_lbl != null and is_instance_valid(craft_pearl_lbl):
			craft_pearl_lbl.text = "Rainbow pearls: %d" % pearl_count
		if craft_status != null and is_instance_valid(craft_status):
			craft_status.text = "%s unlocked forever! Yay!" % knm
	craft_kind = kk
	_craft_build_preview()

func _craft_set(part: String, col: Color) -> void:
	if part == "body": craft_body = col
	else: craft_fins = col
	if craft_fishbox != null:
		for c in craft_fishbox.get_children():
			if c is TextureRect:
				var role: String = (c as TextureRect).get_meta("role", "")
				if part == "body" and role == "body": (c as TextureRect).modulate = col
				if part == "accent" and role == "accent":
					(c as TextureRect).modulate = Color(col.r, col.g, col.b, 1.0)

func _craft_done() -> void:
	if craft_layer == null or bool(get_meta("craft_closing", false)):
		return   # reentry guard: double-click / double-A must not craft twice
	set_meta("craft_closing", true)
	stickers["_c_" + craft_kind] = true   # hidden progress toward Little Artist
	if bool(stickers.get("_c_fish", false)) and bool(stickers.get("_c_cat", false)) and bool(stickers.get("_c_bird", false)):
		award_sticker("artist")
	var fishy: bool = craft_kind == "fish"
	var msgtxt: String
	if fishy:
		custom_fish.append([craft_body.r, craft_body.g, craft_body.b, craft_fins.r, craft_fins.g, craft_fins.b])
		_spawn_crafted_fish()   # same spawn path as build/load keeps the counter honest
		msgtxt = "Swim away, little fish! Find me in the ocean!"
	else:
		custom_friends.append([craft_kind, craft_body.r, craft_body.g, craft_body.b, craft_fins.r, craft_fins.g, craft_fins.b])
		msgtxt = "Off to the courtyard! Find me when you visit!"
	_write_save()
	if chime != null:
		chime.pitch_scale = 1.3; chime.play()
	for tn in get_tree().get_nodes_in_group("craft_top"):
		if tn is CanvasItem:
			(tn as CanvasItem).visible = false   # audit: banner overlapped title/buttons
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
	set_meta("craft_closing", false)
	if craft_layer != null and is_instance_valid(craft_layer):
		craft_layer.queue_free()
	craft_status = null
	craft_pearl_lbl = null
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
	wd["stage"] = stage
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
		var eid := String(entry["id"])
		var locked: bool = (eid.begins_with("fairy") and not fairy_skin_unlocked) or (eid == "pearl" and not bool(shop_owned.get("pearlskin", false)))
		var box: StyleBoxFlat = entry["box"]
		box.bg_color = Color(0.28, 0.28, 0.38) if locked else (Color(0.3, 0.75, 0.42) if sel else Color(0.4, 0.42, 0.6))
		box.set_border_width_all(6 if sel else 0)
		box.border_color = Color(0.2, 1.0, 0.4)
		var bt: Button = entry["btn"]
		bt.text = "🔒 " + String(_skin_def(eid)["label"]) if locked else ("✔ " if sel else "    ") + String(_skin_def(eid)["label"])
		bt.modulate = Color(0.75, 0.75, 0.8) if locked else Color.WHITE

func _wardrobe_pick(id: String) -> void:
	if id.begins_with("fairy") and not fairy_skin_unlocked:
		# the Butterfly World prize — tease it, don't grant it
		if chime != null:
			chime.pitch_scale = 0.5
			chime.play()
		_wardrobe_toast("🦋 Save the Butterfly World to unlock Fairy Roshan!")
		return
	if id == "pearl" and not bool(shop_owned.get("pearlskin", false)):
		if chime != null:
			chime.pitch_scale = 0.5
			chime.play()
		_wardrobe_toast("🦪 Pearl Princess is waiting at the Pearl Shop — 250 pearls!")
		return
	skin_id = id
	_apply_skin()
	_wardrobe_refresh()
	if chime != null:
		chime.pitch_scale = 1.3; chime.play()
	# magic-moment: trying on a look showers Roshan in a sparkle swirl + twirl
	_sparkle_burst(player.position + Vector3(0, 2.0, 0), Color(1.0, 0.85, 1.0))
	_sparkle_burst(player.position + Vector3(0, 0.5, 0), Color(0.7, 0.95, 1.0))
	player.play_verb("twirl")   # R2-C: she shows off the new look

func _open_stickers() -> void:
	if stickers_layer != null:
		return
	stickers_layer = CanvasLayer.new(); stickers_layer.layer = 18; add_child(stickers_layer)
	var root := Control.new(); root.set_anchors_preset(Control.PRESET_FULL_RECT); stickers_layer.add_child(root)
	var vp: Vector2 = get_viewport().get_visible_rect().size
	var bg := ColorRect.new(); bg.color = Color(0.10, 0.07, 0.17, 0.96); bg.set_anchors_preset(Control.PRESET_FULL_RECT); root.add_child(bg)
	var stage := Control.new(); stage.size = Vector2(1280, 720)
	var sc: float = minf(vp.x / 1280.0, vp.y / 720.0)
	stage.scale = Vector2(sc, sc); stage.position = (vp - Vector2(1280, 720) * sc) * 0.5
	root.add_child(stage)
	var got := 0
	for d in STICKER_DEFS:
		if bool(stickers.get(String(d["id"]), false)):
			got += 1
	var title := Label.new(); title.text = "⭐ My Sticker Book!   %d / %d" % [got, STICKER_DEFS.size()]
	title.add_theme_font_size_override("font_size", 52)
	title.add_theme_color_override("font_color", Color(1.0, 0.93, 0.6))
	title.add_theme_color_override("font_outline_color", Color(0.08, 0.05, 0.15)); title.add_theme_constant_override("outline_size", 10)
	title.position = Vector2(60, 16); stage.add_child(title)
	for si in range(STICKER_DEFS.size()):
		var d2: Dictionary = STICKER_DEFS[si]
		var earned: bool = bool(stickers.get(String(d2["id"]), false))
		var cell := Panel.new()
		cell.position = Vector2(46.0 + float(si % 6) * 199.0, 104.0 + float(si / 6) * 194.0)
		cell.size = Vector2(184, 178)
		var csb := StyleBoxFlat.new()
		csb.bg_color = Color(0.32, 0.28, 0.5, 0.95) if earned else Color(0.2, 0.19, 0.28, 0.9)
		csb.set_corner_radius_all(22)
		csb.set_border_width_all(4)
		csb.border_color = Color(1.0, 0.85, 0.4) if earned else Color(0.35, 0.35, 0.45)
		cell.add_theme_stylebox_override("panel", csb)
		stage.add_child(cell)
		var em := Label.new()
		em.text = String(d2["emoji"]) if earned else "?"
		em.add_theme_font_size_override("font_size", 64)
		em.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
		em.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		em.offset_top = 8.0
		em.modulate = Color.WHITE if earned else Color(0.55, 0.55, 0.65)
		cell.add_child(em)
		var nm := Label.new()
		nm.text = String(d2["label"]) if earned else String(d2["hint"])
		nm.add_theme_font_size_override("font_size", 20 if earned else 15)
		nm.add_theme_color_override("font_color", Color(1.0, 0.95, 0.8) if earned else Color(0.7, 0.7, 0.78))
		nm.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		nm.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		nm.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
		nm.offset_top = -72.0
		nm.offset_left = 8.0
		nm.offset_right = -8.0
		cell.add_child(nm)
	var xb := Button.new(); xb.text = "✕"
	xb.add_theme_font_size_override("font_size", 42)
	xb.position = Vector2(1186, 14); xb.custom_minimum_size = Vector2(76, 76)
	xb.pressed.connect(_close_stickers)
	stage.add_child(xb)

func _close_stickers() -> void:
	if stickers_layer != null and is_instance_valid(stickers_layer):
		stickers_layer.queue_free()
	stickers_layer = null

func _wardrobe_toast(txt: String) -> void:
	if not wd.has("stage"):
		return
	var t := Label.new()
	t.text = txt
	t.add_theme_font_size_override("font_size", 34)
	t.add_theme_color_override("font_color", Color(1.0, 0.85, 0.5))
	t.add_theme_color_override("font_outline_color", Color(0.08, 0.05, 0.15))
	t.add_theme_constant_override("outline_size", 10)
	t.position = Vector2(110, 682)
	(wd["stage"] as Control).add_child(t)
	var tw := t.create_tween()
	tw.tween_interval(2.2)
	tw.tween_property(t, "modulate:a", 0.0, 0.6)
	tw.tween_callback(t.queue_free)

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
	player.cam_back = 25.0   # diorama lens default
	player.cam_high = 6.5
	game = ""
	g = {}
	hud_game.text = ""
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	arena_solids.clear()
	arena_zones.clear()
	fade_walls.clear()
	we_node.environment = world_env
	arena_center = ARENA_POS
	arena_dome = 48.0
	arena_ceil = 42.0
	portal_cool = 8.0
	portal_armed = false
	if portal_node != null and is_instance_valid(portal_node):
		# beside the seabed portal, resting on the ocean floor (never below it)
		player.position = portal_node.position + Vector3(22, 0, 22)
		player.position.y = seabed_y(player.position.x, player.position.z) + 6.0
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
	arena_zones.clear()
	fade_walls.clear()
	we_node.environment = world_env
	arena_center = ARENA_POS
	arena_dome = 48.0
	arena_ceil = 42.0
	portal_cool = 6.0
	portal_armed = false
	# beside the portal but clearly off it, resting on the ocean floor
	if portal_node != null and is_instance_valid(portal_node):
		player.position = portal_node.position + Vector3(22, 0, 22)
		player.position.y = seabed_y(player.position.x, player.position.z) + 6.0
	else:
		player.position = return_pos
	player.vel = Vector3.ZERO
	_play_music("world")
	show_msg("Princess Huluu", "You made it to my Pearl Castle, Roshan! You are the Queen of the Reef now!", "win")

func _beans_go() -> void:
	award_sticker("beans")
	beans_t = 40.0   # long enough to swim from the Pearl Shop to the Penguin Slide
	speed_mult = 2.0
	fart_t = 0.7
	if beans_sfx != null and not beans_sfx.playing:
		beans_sfx.play()
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
	beans_t -= delta
	if beans_t <= 0.0:
		beans_t = -1.0
		speed_mult = 1.0
		show_msg("", "Phew! The beans wore off.")
		if g_beans_bubbles != null and is_instance_valid(g_beans_bubbles):
			g_beans_bubbles.queue_free()
		g_beans_bubbles = null
		if beans_sfx != null:
			beans_sfx.stop()

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
	# NON-READER WAYFINDING (audit: every "where do I go?" cue was text-only).
	# The friend pillars now narrate progress: finished friends dim right down,
	# waiting friends stay soft, and the NEAREST quest friend pulses bright.
	var tt2: float = Time.get_ticks_msec() / 1000.0
	for f in friends:
		var pil: MeshInstance3D = f.get("pillar")
		if pil == null or not is_instance_valid(pil):
			continue
		var pmat2 := pil.material_override as StandardMaterial3D
		if pmat2 == null:
			continue
		if bool(f["won"]):
			pmat2.albedo_color.a = 0.03
		elif have and (f["node"] as Sprite3D).position == target:
			pmat2.albedo_color.a = 0.22 + 0.12 * (0.5 + 0.5 * sin(tt2 * 2.4))
		else:
			pmat2.albedo_color.a = 0.10
	if not have or best <= 16.0:
		return
	var dir2: Vector3 = (target - player.position).normalized()
	# gentle helping current: if the child is swimming roughly toward the goal, carry them
	var pv: Vector3 = player.vel
	if best > 25.0 and pv.length() > 4.0 and pv.normalized().dot(dir2) > 0.45:
		player.position += dir2 * 5.5 * delta
	# breadcrumb sparkles: when the goal is far, a short trail of gold twinkles
	# points the way every couple of seconds — follow the sparkles!
	var gt: float = float(get_meta("guide_t", 0.0)) - delta
	if best > 35.0 and gt <= 0.0:
		gt = 2.2
		for k: float in [8.0, 16.0]:
			_sparkle_burst(player.position + dir2 * k + Vector3(0, 1.5, 0), Color(1.0, 0.95, 0.6))
	set_meta("guide_t", gt)

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
	# (the old friends-circling-Roshan swarm is gone — the celebration now points
	# the player at the rainbow portal opening on the ocean floor)
	finale_done = true
	finale_t = 0.0
	_write_save()
	_play_music("finale")
	show_msg("Everyone", "Roshan did it! Hooray! Deep below, a RAINBOW PORTAL is beginning to open on the ocean floor!")

func _tick_finale(delta: float) -> void:
	if finale_t < 0.0:
		return
	finale_t += delta
	# fireworks of sparkles around Roshan, and at the portal once it exists
	if fmod(finale_t, 0.9) < delta:
		_sparkle_burst(player.position + Vector3(randf() * 8.0 - 4.0, 4.0, randf() * 8.0 - 4.0), Color.from_hsv(randf(), 0.6, 1.0))
		if portal_node != null and is_instance_valid(portal_node):
			_sparkle_burst(portal_node.position + Vector3(randf() * 6.0 - 3.0, 5.0, randf() * 6.0 - 3.0), Color.from_hsv(randf(), 0.5, 1.0))
	if finale_t > 10.0:
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
	_dolls2d_close()
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	arena_solids.clear()
	arena_zones.clear()
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
		"slide":      return "He's too speedy without magic beans! Toot toot!" if String(g.get("mode", "fish")) == "chase" else "So close! Catch more fish next time!"
		_:            return "So close! Swim back and try again!"

var pose_t := -1.0        # >=0: trophy curtain-call — player holds a happy pose
var night_star_t := 4.0   # countdown to the next shooting star over the night lagoon

var _shadow_disc: MeshInstance3D = null

func _tick_contact_shadow() -> void:
	# storybook readability: a soft aqua contact blob under Roshan grounds the
	# cutout against the diorama (book pages do the same with painted shadows)
	if _shadow_disc == null:
		_shadow_disc = MeshInstance3D.new()
		var qm := QuadMesh.new()
		qm.size = Vector2(4.4, 4.4)
		_shadow_disc.mesh = qm
		_shadow_disc.rotation_degrees.x = -90.0
		var m := StandardMaterial3D.new()
		m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		m.albedo_color = Color(0.16, 0.28, 0.45, 0.30)
		var g2 := Gradient.new()
		g2.set_color(0, Color(1, 1, 1, 1))
		g2.set_color(1, Color(1, 1, 1, 0))
		var gt2 := GradientTexture2D.new()
		gt2.gradient = g2
		gt2.fill = GradientTexture2D.FILL_RADIAL
		gt2.fill_from = Vector2(0.5, 0.5)
		gt2.fill_to = Vector2(0.5, 0.0)
		m.albedo_texture = gt2
		_shadow_disc.material_override = m
		add_child(_shadow_disc)
	var fy: float
	if game == "" and player != null:
		fy = seabed_y(player.position.x, player.position.z)
	elif game == "level2" and String(g.get("phase", "court")) != "hall" and player != null:
		fy = lagoon_walk_h(player.position.x - LEVEL2_POS.x, player.position.z - LEVEL2_POS.z) + LEVEL2_POS.y
	else:
		_shadow_disc.visible = false
		return
	var hgt: float = maxf(0.5, player.position.y - fy)
	_shadow_disc.visible = hgt < 26.0
	_shadow_disc.position = Vector3(player.position.x, fy + 0.25, player.position.z)
	_shadow_disc.scale = Vector3.ONE * clampf(1.25 - hgt * 0.028, 0.35, 1.2)
	(_shadow_disc.material_override as StandardMaterial3D).albedo_color.a = clampf(0.34 - hgt * 0.009, 0.06, 0.34)

func _reward(pose: bool = true) -> void:
	# RewardDirector: EVERY win in the game funnels through the same pattern —
	# rainbow sparkle, rising chimes, a short celebration pause, sticker/photo
	_fanfare()
	if pose:
		_celebrate_pose()

func _celebrate_pose() -> void:
	# the curtain call: 2 seconds of confetti + a trophy stamp + a sparkle ring
	# while Roshan holds her pose — every first-time trophy earns one
	pose_t = 2.2
	var cl3 := CanvasLayer.new()
	cl3.layer = 22
	add_child(cl3)
	var big := Label.new()
	big.text = "🏆 ⭐ 🏆"
	big.add_theme_font_size_override("font_size", 110)
	big.add_theme_constant_override("outline_size", 16)
	big.add_theme_color_override("font_outline_color", Color(0.2, 0.1, 0.3))
	big.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	big.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	big.offset_top = 50.0
	cl3.add_child(big)
	for ci in range(36):
		var conf := ColorRect.new()
		conf.color = Color.from_hsv(randf(), 0.7, 1.0)
		conf.size = Vector2(16, 16)
		conf.position = Vector2(randf() * 1280.0, -30.0 - randf() * 200.0)
		conf.rotation = randf() * TAU
		cl3.add_child(conf)
		var ct := conf.create_tween()
		ct.tween_property(conf, "position:y", 780.0, 1.6 + randf() * 0.8).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	for si in range(8):
		var sa: float = TAU * float(si) / 8.0
		_sparkle_burst(player.position + Vector3(cos(sa) * 2.5, 1.0 + float(si % 3), sin(sa) * 2.5), Color.from_hsv(float(si) / 8.0, 0.5, 1.0))
	get_tree().create_timer(2.4).timeout.connect(cl3.queue_free)

func _greet_heart(pos: Vector3) -> void:
	# a crafted friend says hello: floating heart + sparkle + happy chirp
	var h := Label3D.new()
	h.text = "❤"
	h.font_size = 140
	h.pixel_size = 0.02
	h.outline_size = 14
	h.modulate = Color(1.0, 0.45, 0.65)
	h.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	h.position = pos
	add_child(h)
	var tw := h.create_tween()
	tw.tween_property(h, "position:y", pos.y + 3.5, 1.1)
	tw.parallel().tween_property(h, "modulate:a", 0.0, 1.1)
	tw.tween_callback(h.queue_free)
	_sparkle_burst(pos, Color(1.0, 0.6, 0.8))
	if voice != null:
		voice.pitch_scale = 1.3 + randf() * 0.2
		voice.play()

func _spawn_shooting_star(ppos: Vector3) -> void:
	# night magic over the lagoon: a bright streak arcs across the sky
	var star := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = Vector3(0.4, 0.4, 9.0)
	star.mesh = bm
	var m := StandardMaterial3D.new()
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	m.albedo_color = Color(0.9, 0.95, 1.0, 0.9)
	star.material_override = m
	var start: Vector3 = ppos + Vector3(randf_range(-130.0, 130.0), 75.0 + randf() * 45.0, randf_range(-130.0, 130.0))
	var dirv := Vector3(randf_range(-1.0, 1.0), -0.35, randf_range(-1.0, 1.0)).normalized()
	add_child(star)
	star.position = start
	star.look_at(start + dirv, Vector3.UP)
	var tw := star.create_tween()
	tw.tween_property(star, "position", start + dirv * 130.0, 1.3)
	tw.parallel().tween_property(m, "albedo_color:a", 0.0, 1.3)
	tw.tween_callback(star.queue_free)

func _end_game(win: bool, fr: Dictionary, txt: String, vo: String = "talk") -> void:
	if chime != null:
		chime.volume_db = -4.0   # restore default chime volume (the fairy game lowers it)
	_leave_arena()
	if win and not fr["won"]:
		fr["won"] = true
		trophies += 1
		_add_won_star(fr)
		_reward()
		if player != null:
			player.play_verb("cheer")   # R2-C: arms up for the trophy curtain call
	fr["cool"] = 5.0
	if String(fr["fname"]) == "Secret Cave":
		treasure_cool = 14.0
	elif String(fr["fname"]) == "Pearl Shop":
		shop_cool = 16.0
	elif String(fr["fname"]) == "Fairy Pond":
		# quick retry after a boss fail — a 12s wait outside the pond was pure
		# friction for a kid who wants straight back in
		fairy_cool = 12.0 if win else 5.0
		_apply_skin()   # restore Roshan's normal look after the fairy flight
	_respawn_pearls()
	show_msg(fr["fname"], txt, "win" if win else vo)
	_update_hud()
	_clear_game()
	_write_save()
	if String(fr.get("fname", "")) == "Fairy Pond" and fairy_from_galaxy:
		fairy_from_galaxy = false
		call_deferred("_start_galaxy")   # back to the Butterfly World
		return
	if String(fr.get("fname", "")) == "Rainbow Slide" or String(fr.get("fname", "")) == "Fairy Pond":
		# return to the courtyard; only restore the OPEN castle if it was already
		# open — the slide is playable before the stars, and used to force the
		# door open (skipping the whole Dream-Star quest)
		call_deferred("_enter_level2", l2_open)
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
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
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
	m.uv1_scale = Vector3(0.18, 0.18, 0.18)
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
	# collision audit #4: the cabin walls were swim-through
	_wall_solid(Vector3(origin.x, f + 9.0, origin.z - 13.0), Vector3(34, 19, 1.2), 0.5)
	_wall_solid(Vector3(origin.x - 16.0, f + 9.0, origin.z + 2.0), Vector3(1.2, 19, 30), 0.5)
	_wall_solid(Vector3(origin.x + 16.0, f + 9.0, origin.z + 2.0), Vector3(1.2, 19, 30), 0.5)
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
	var slots := [-6.5, -2.2, 2.2, 6.5]
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
		elif iid == "pearlskin":
			# the grand prize: a giant shimmering pearl
			var bigp := MeshInstance3D.new()
			var pm3 := SphereMesh.new()
			pm3.radius = 1.0
			pm3.height = 2.0
			bigp.mesh = pm3
			var pmm := StandardMaterial3D.new()
			pmm.albedo_color = Color(1.0, 0.96, 1.0)
			pmm.metallic = 0.55
			pmm.roughness = 0.15
			pmm.emission_enabled = true
			pmm.emission = Color(1.0, 0.85, 0.95)
			pmm.emission_energy_multiplier = 0.9
			bigp.material_override = pmm
			inode = bigp
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
		if iid != "beans" and bool(shop_owned.get(iid, false)):
			inode.visible = false
			tag.text = "%s\n(yours!)" % String(it["label"])
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

func _start_game(fr: Dictionary) -> void:
	game = String(fr["game"])
	g = {"fr": fr, "t": 0.0, "timer": 30.0}
	_enter_arena(game)
	var origin: Vector3 = ARENA_POS
	if game == "fetch":
		_game_obj("fetch", FetchGame).build(fr, origin)
	elif game == "dolls":
		_game_obj("dolls", DollsGame).build(fr, origin)
	elif game == "seek":
		_game_obj("seek", SeekGame).build(fr, origin)
	elif game == "race":
		_game_obj("race", SlideRaceGame).build(fr, origin)
	elif game == "shop":
		_game_obj("shop", ShopGame).build(fr, origin)
	elif game == "treasure":
		_game_obj("treasure", TreasureGame).build(fr, origin)
	elif game == "melody":
		_game_obj("melody", MelodyGame).build(fr, origin)
	elif game == "slide":
		_game_obj("race", SlideRaceGame).build_slide(fr, origin)
	elif game == "fairyshoot":
		_game_obj("fairyshoot", FairyGame).build(fr, origin)
# ===================== PENGUIN ICE SLIDE =====================
# A short N64-style downhill chute. Roshan slides on momentum (gravity along the
# slope); the player only steers left/right. 5 fish to grab, ~12 seconds.

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

func _slide_pos(s: float) -> Vector3:
	# R1: Catmull-Rom position at arc-length s. The MOTION/CAMERA path is
	# C1-smooth; the plank visuals still sit on the raw polyline (they look
	# fine and the rider floats SLIDE_RIDE above them).
	var path: Array = g["path"]
	var cum: Array = g["cum"]
	var total: float = g["total"]
	s = clampf(s, 0.0, total)
	var i := 0
	while i < cum.size() - 2 and float(cum[i + 1]) < s:
		i += 1
	var seg_len: float = float(cum[i + 1]) - float(cum[i])
	var f: float = 0.0 if seg_len < 0.001 else (s - float(cum[i])) / seg_len
	var p0: Vector3 = path[maxi(i - 1, 0)]
	var p1: Vector3 = path[i]
	var p2: Vector3 = path[mini(i + 1, path.size() - 1)]
	var p3: Vector3 = path[mini(i + 2, path.size() - 1)]
	var f2: float = f * f
	var f3: float = f2 * f
	return ((p1 * 2.0) + (p2 - p0) * f + (p0 * 2.0 - p1 * 5.0 + p2 * 4.0 - p3) * f2 + (p1 * 3.0 - p0 - p2 * 3.0 + p3) * f3) * 0.5

func _slide_sample(s: float) -> Array:
	# returns [pos, tangent, right] at arc-length s along the chute.
	# R1: tangent by central difference of the spline (ds=1.5m), never from
	# segment indices - heading is continuous, no more per-joint yaw snaps.
	var pos := _slide_pos(s)
	var fwd: Vector3 = _slide_pos(s + 1.5) - _slide_pos(s - 1.5)
	var fwd_n: Vector3 = fwd.normalized() if fwd.length() > 0.001 else Vector3.FORWARD
	var right: Vector3 = Vector3.UP.cross(fwd_n)
	if right.length() < 0.001:
		right = Vector3.RIGHT
	return [pos, fwd_n, right.normalized()]

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
	var jx: float = joy_axis(JOY_AXIS_LEFT_X)
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
		# ===== RACE THE BABY PENGUIN — the BEAN PUZZLE =====
		# Without magic beans he is simply too fast: his lead never shrinks into catch
		# range and he crosses the finish first. EAT BEANS (Pearl Shop) and Roshan gets
		# the super-speed to reel him in — that's the puzzle.
		var p: float = s / total
		var beany: bool = beans_t >= 0.0 or bool(g.get("beany", false))
		g["beany"] = beany   # latch: beans active at any point during the ride count
		var gap: float
		if beany:
			gap = maxf(0.0, SLIDE_LEAD * (1.0 - p * 1.45))   # bean power: reel him in!
		else:
			# he TIRES near the bottom — sim: pure "beans or nothing" meant a
			# guaranteed first-run fail behind a text hint a 4yo can't read.
			# Unbeaned he's still catchable in the last stretch (p>~0.83);
			# beans catch him WAY earlier and stay the fun way to win.
			gap = SLIDE_LEAD * maxf(0.02, 1.0 - p * 0.5 - maxf(0.0, p - 0.7) * 1.4)
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
			award_sticker("penguin")
			_sparkle_burst(pbpos + Vector3(0, 1.5, 0), Color(1.0, 0.9, 0.4))
			if chime != null:
				chime.pitch_scale = 1.5; chime.play()
			_end_game(true, fr, "You caught the baby penguin! Hee hee, great race!")
			return
		if beany:
			hud_game.text = "BEAN POWER! Catch him!   ← →" if p > 0.3 else "Beans! Toot toot! GO GO GO!"
		elif p > 0.72:
			hud_game.text = "He's getting TIRED! Catch him! ← →"
		else:
			hud_game.text = "Catch the baby penguin! ...he's SO fast!"
		if float(g["s"]) >= total - 0.5:
			_end_game(false, fr, "He crossed the finish first — he's just too speedy! Hmm... maybe magic BEANS from the Pearl Shop would give me a super boost! Toot toot!", "fail")
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
const FS_BOSS_Z := FS_LEN + 64.0   # the GIANT boss needs distance to fit in view
const FS_BOSS_HIT_R := 16.0        # giant boss, giant hitboxes
const FS_LEAVES := 6               # outer leaf shield
const FS_LEAF_HP := 1              # one blast per leaf
const FS_LEAF_T := 18.0            # seconds to blast the leaves away
var fs_fails := 0                  # boss attempts lost -> retry kindness (+6s each, max +12)
const FS_LEAF_RING_X := 26.0       # the leaf wreath is a wide ellipse now (giant boss)
const FS_LEAF_RING_Y := 13.0       # ...but stays vertically reachable by the bolt aim
const FS_BUD_HP := 10
const FS_BUD_T := 18.0             # seconds to bloom the flower open
const FS_BLOOM_T := 6.5            # savour the giant bloom — the old 3s ending was blink-and-confusing
const FS_LEAF_SCALE := 17.0        # real Kenney bush models (CC0), giant
const FS_BUD_SCALE := 55.0         # the flower TOWERS (was 9 — it read as a shrub)
const FS_FLOWER := "flower_purpleA"  # ONE flower for the whole boss (grows, then blooms)

func _build_fairyshoot(origin: Vector3) -> void:
	# Roshan wears her fairy form for this game only
	if chime != null:
		chime.volume_db = -13.0   # the fairy game fires a lot — keep its chime soft (restored in _end_game)
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
	# retry kindness: each earlier fail stretches both boss timers by 6s (max
	# +12) so a determined kid always blooms the flower on attempt 2-3
	g["phase_t"] = FS_LEAF_T + 6.0 * float(mini(fs_fails, 2))
	# leafy stalk base (a big bush model)
	if _nature("plant_bushLargeTriangle", center + Vector3(0, -52.0, 1.0), 34.0, 0.0) == null:
		var stalk := _course_box(center + Vector3(0, -40.0, 0), Vector3(10, 70, 10), Color(0.3, 0.65, 0.35))
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
		var lp: Vector3 = center + Vector3(cos(a) * FS_LEAF_RING_X, sin(a) * FS_LEAF_RING_Y, -1.0)
		var leaf := _nature(leafkinds[k % leafkinds.size()], lp, FS_LEAF_SCALE, randf() * TAU)
		if leaf == null:
			var lm := MeshInstance3D.new()
			var pm := PrismMesh.new(); pm.size = Vector3(5.0, 9.0, 2.0)
			lm.mesh = pm; lm.material_override = _soft_mat(Color(0.35, 0.75, 0.4), 0.4)
			lm.position = lp; add_child(lm); game_nodes.append(lm); leaf = lm
		(g["leaves"] as Array).append({"node": leaf, "hp": FS_LEAF_HP, "ang": a, "base": lp})
	var bl := OmniLight3D.new()
	bl.light_color = Color(1.0, 0.7, 0.85); bl.light_energy = 4.0; bl.omni_range = 130.0
	bl.position = center; add_child(bl); game_nodes.append(bl)
	g["boss_light"] = bl
	show_msg(fr_name_safe(), "THE GIANT FAIRY FLOWER fills the sky! Blast the leaves out of the way!")

func fr_name_safe() -> String:
	return String((g.get("fr", {}) as Dictionary).get("fname", "Fairy Pond"))

func _fairy_bloom_start() -> void:
	award_sticker("flower")
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

func _build_slide_portal() -> void:
	# a penguin on a floating ice floe in the reef — swim up to it to start the slide
	slide_portal_pos = Vector3(48.0, WATER_TOP - 26.0, -42.0)   # nav audit: was (80,-20,-70) = 106m swim; now ~64m on an open lane
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
			_cyl_solid(gp + Vector3(0, 3.0, 0), 0.9, 3.0, 0.5)   # trunks solid; hide-bushes stay soft
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
		_game_obj("seek", SeekGame).tick(delta, fr, ppos)
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

var dolls_layer: CanvasLayer
var dolls_root: Control
var dolls_catcher: TextureRect
var dolls_score_lbl: Label

func skin_sprite_path() -> String:
	# the flat art matching the wardrobe skin — used by the kart driver,
	# the 2D minigame mermaid and the dolls catcher so the chosen look
	# follows Roshan into every game, not just the ocean
	if skin_id == "huluu":
		return "res://assets/characters/friends/huluu.png"
	if skin_id == "fairy":
		return "res://assets/characters/skins/fairy_mermaid.png"
	return "res://assets/characters/roshan_sprite.png"   # classic + pearl (classic art)

var _pad_prev_a := false
var _pad_prev_b := false
var _overlay_age := 0.0

# ---- PAD CURSOR: a golden star pointer, so a controller can click ANY button
# ---- in the pointer-driven overlays (craft swatches, wardrobe outfits, 2D
# ---- minigames). Wakes on the first stick push while an overlay is open.
var pad_cursor_layer: CanvasLayer = null
var pad_cursor_node: Label = null
var pad_cursor_pos := Vector2(640, 360)
var pad_cursor_active := false
var _pc_prev_a := false

func _overlay_root_for_cursor() -> Node:
	if craft_layer != null and is_instance_valid(craft_layer):
		return craft_layer
	if wardrobe_layer != null and is_instance_valid(wardrobe_layer):
		return wardrobe_layer
	if stickers_layer != null and is_instance_valid(stickers_layer):
		return stickers_layer
	if mg_kind != "" and mg2d_layer != null and mg2d_layer.visible:
		return mg2d_layer
	return null

func _tick_pad_cursor(delta: float) -> void:
	var root: Node = _overlay_root_for_cursor()
	var a: bool = joy_pressed(JOY_BUTTON_A)
	if root == null:
		pad_cursor_active = false
		if pad_cursor_layer != null:
			pad_cursor_layer.visible = false
		_pc_prev_a = a
		return
	var v := Vector2(joy_axis(JOY_AXIS_LEFT_X), joy_axis(JOY_AXIS_LEFT_Y))
	v += Vector2(joy_axis(JOY_AXIS_RIGHT_X), joy_axis(JOY_AXIS_RIGHT_Y))
	if v.length() < 0.2:
		v = Vector2.ZERO
	if not pad_cursor_active:
		if v == Vector2.ZERO:
			_pc_prev_a = a
			return
		pad_cursor_active = true
		pad_cursor_pos = get_viewport().get_visible_rect().size * 0.5
		if pad_cursor_layer == null:
			pad_cursor_layer = CanvasLayer.new()
			pad_cursor_layer.layer = 30
			add_child(pad_cursor_layer)
			pad_cursor_node = Label.new()
			pad_cursor_node.text = "✦"
			pad_cursor_node.add_theme_font_size_override("font_size", 58)
			pad_cursor_node.add_theme_color_override("font_color", Color(1.0, 0.85, 0.3))
			pad_cursor_node.add_theme_color_override("font_outline_color", Color(0.1, 0.05, 0.2))
			pad_cursor_node.add_theme_constant_override("outline_size", 12)
			pad_cursor_node.mouse_filter = Control.MOUSE_FILTER_IGNORE
			pad_cursor_layer.add_child(pad_cursor_node)
	pad_cursor_layer.visible = true
	var vr: Vector2 = get_viewport().get_visible_rect().size
	pad_cursor_pos = (pad_cursor_pos + v * 950.0 * delta).clamp(Vector2.ZERO, vr)
	pad_cursor_node.position = pad_cursor_pos - Vector2(20, 36)
	pad_cursor_node.scale = pad_cursor_node.scale.lerp(Vector2.ONE, minf(1.0, delta * 10.0))
	if a and not _pc_prev_a:
		# click whatever Button sits under the star (last hit in tree order = topmost)
		var hit: Button = null
		var stack: Array = [root]
		while not stack.is_empty():
			var n: Node = stack.pop_back()
			for c in n.get_children():
				stack.append(c)
			if n is Button and (n as Button).is_visible_in_tree() and not (n as Button).disabled:
				if (n as Button).get_global_rect().has_point(pad_cursor_pos):
					hit = n
		if hit != null:
			pad_cursor_node.scale = Vector2(1.5, 1.5)   # satisfying click pop
			hit.pressed.emit()
	_pc_prev_a = a

func _tick_overlay_pads(delta: float) -> void:
	# gamepad shortcuts for the pointer-driven overlays: A = Done, B = close.
	# Without these a controller-only setup could open the craft studio or the
	# wardrobe and never leave (no pointer, no exit).
	var a: bool = joy_pressed(JOY_BUTTON_A)
	var b: bool = joy_pressed(JOY_BUTTON_B)
	var overlay_open: bool = craft_layer != null or wardrobe_layer != null or stickers_layer != null
	_overlay_age = _overlay_age + delta if overlay_open else 0.0
	if _overlay_age > 0.6:   # grace so the A/B that was held while swimming in doesn't fire
		if craft_layer != null:
			if a and not _pad_prev_a and not pad_cursor_active:
				_craft_done()   # quick-finish only while the star cursor is asleep
			elif b and not _pad_prev_b:
				_close_craft()
		elif wardrobe_layer != null:
			if a and not _pad_prev_a and not pad_cursor_active:
				_wardrobe_done()
			elif b and not _pad_prev_b:
				_close_wardrobe()
		elif stickers_layer != null:
			if (b and not _pad_prev_b) or (a and not _pad_prev_a and not pad_cursor_active):
				_close_stickers()
	_pad_prev_a = a
	_pad_prev_b = b

var _wayfind_t := 0.0

func _tick_wayfinder(delta: float, ppos: Vector3) -> void:
	# MOBILE NAV AUDIT: a sparkle comet-trail from Roshan toward the current
	# best objective while she roams the open reef — the "pathfinding" a
	# non-reader can follow. Nearest un-won friend first; with all five won,
	# the Pearl Shop ship when she can afford something, else the penguin
	# floe. Throttled to 3 cheap bursts every 2.2s; silent inside games,
	# overlays, the intro and other worlds.
	if game != "" or mg_kind != "" or intro_active:
		return
	if _overlay_root_for_cursor() != null:
		return
	_wayfind_t -= delta
	if _wayfind_t > 0.0:
		return
	_wayfind_t = 2.2
	var target := Vector3.ZERO
	var best := 1e9
	for f in friends:
		if not bool(f["won"]):
			var p: Vector3 = (f["node"] as Node3D).position
			var d: float = p.distance_to(ppos)
			if d < best:
				best = d
				target = p
	if target == Vector3.ZERO:
		if pearl_count >= 60 and manta != null and is_instance_valid(manta):
			target = manta.position
		elif slide_portal_pos != Vector3.ZERO:
			target = slide_portal_pos
	if target == Vector3.ZERO or target.distance_to(ppos) < 22.0:
		return
	for k in range(3):
		var tt: float = 0.06 + 0.07 * float(k)
		_sparkle_burst(ppos.lerp(target, tt) + Vector3(0, 1.5, 0), Color(1.0, 0.95, 0.6))

func _process(delta: float) -> void:
	if msg_timer > 0.0:
		msg_timer -= delta
		if msg_timer <= 0.0:
			hud_msg.text = ""
	if pose_t >= 0.0:
		pose_t -= delta   # trophy curtain-call countdown (player frozen while >=0)
	_tick_contact_shadow()
	_tick_ambience_duck(delta)
	if player != null:
		_tick_wayfinder(delta, player.position)
	_tick_overlay_pads(delta)
	_tick_pad_cursor(delta)
	if fps_lbl != null and pause_panel != null and pause_panel.visible:
		fps_lbl.text = "FPS: %d   (%s)" % [Engine.get_frames_per_second(), quality]
	if speech_t > 0.0:
		speech_t -= delta
		if speech_t <= 0.0 and speech_layer != null:
			speech_layer.visible = false
	if player == null:
		return
	if intro_active:
		return
	var ppos: Vector3 = player.position
	if caustics_plane != null:
		if game == "" and not intro_active:
			caustics_plane.visible = true
			caustics_plane.position = Vector3(ppos.x, seabed_y(ppos.x, ppos.z) + 1.2, ppos.z)
		elif caustics_plane.visible:
			caustics_plane.visible = false
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
			if pearl_count % 25 == 0 and player != null:
				player.play_verb("giggle")   # R2-C: every 25th pearl is a little party
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
	elif game == "kart":
		pass   # the KartGame node ticks itself
	elif game == "galaxy":
		pass   # the GalaxyLevel node ticks itself
	elif game != "":
		_tick_game(delta)
	_tick_wall_fade(delta)
	_tick_life(delta)
	_tick_movers(delta)
	_tick_aquatic(delta)
	_tick_god_rays(delta)
	_tick_guide(delta)
	_tick_finale(delta)
	_tick_hints(delta)
	_tick_beans(delta)
	_tick_roshan_reactions(delta, ppos)
	shop_cool = maxf(0.0, shop_cool - delta)
	treasure_cool = maxf(0.0, treasure_cool - delta)
	slide_cool = maxf(0.0, slide_cool - delta)
	kart_cool = maxf(0.0, kart_cool - delta)
	if game == "" and finale_t < 0.0:
		if manta != null and shop_cool <= 0.0:
			if manta.position.distance_to(ppos) < 17.0:
				shop_cool = 16.0
				_start_game(shop_fr)
		if treasure_cool <= 0.0 and wreck_pos.distance_to(ppos) < 13.0:
			treasure_cool = 12.0
			_start_game(treasure_fr)
		if slide_cool <= 0.0 and slide_portal_pos != Vector3.ZERO and slide_portal_pos.distance_to(ppos) < 14.0:
			slide_cool = 14.0
			_start_game(slide_fr)
		if kart_cool <= 0.0 and kart_portal_pos != Vector3.ZERO:
			var kd: float = Vector2(kart_portal_pos.x - ppos.x, kart_portal_pos.z - ppos.z).length()
			if kd < 12.0 and absf(kart_portal_pos.y - ppos.y) < 14.0:
				_start_kart_game(false, "terrain")
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
void vertex(){
	float w = UV.y;
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	VERTEX.x += sin(TIME * 0.9 + wp.x * 0.28 + wp.z * 0.22) * 0.5 * w;
	VERTEX.z += cos(TIME * 0.7 + wp.x * 0.16) * 0.36 * w;
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
	// soft translucency so blades let light through, plus a faint tip glow
	BACKLIGHT = tip_col * (0.25 + t * 0.4);
	EMISSION = tip_col * (0.02 + t * t * 0.10);
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
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
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
		mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
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
	# nav audit: the shop ship was the game's remotest POI (150m ring). Pull it
	# to a 100m ring on the OPPOSITE heading from the wreck, same drift/beacon.
	var gsx: float = -wx * (100.0 / 150.0)
	var gsz: float = -wz * (100.0 / 150.0)
	var ghost := _spawn("ship-ghost", Vector3(gsx, WATER_TOP - 10.0, gsz), 7.0, 0.0)
	if ghost != null:
		ghost.set_meta("ghost", true)
		manta = ghost
		# PEARL SHOP ATTRACTION: the ship IS the shop, but three little lamps
		# didn't pull anyone in. A golden beacon pillar reaches down into the
		# reef (visible from anywhere underwater) + an unmissable sign.
		var spil := MeshInstance3D.new()
		var spm := CylinderMesh.new()
		spm.top_radius = 0.7
		spm.bottom_radius = 2.6
		spm.height = 46.0
		spm.radial_segments = 12
		var spmat := StandardMaterial3D.new()
		spmat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		spmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		spmat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		spmat.albedo_color = Color(1.0, 0.85, 0.4, 0.16)
		spmat.cull_mode = BaseMaterial3D.CULL_DISABLED
		spil.mesh = spm
		spil.material_override = spmat
		spil.position = ghost.position + Vector3(0, -24.0, 0)
		add_child(spil)
		var ssign := Label3D.new()
		ssign.text = "🫧 Pearl Shop! 🫧\nswim up to the ship!"
		ssign.font_size = 72
		ssign.outline_size = 16
		ssign.pixel_size = 0.03
		ssign.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		ssign.modulate = Color(1.0, 0.9, 0.55)
		ssign.position = ghost.position + Vector3(0, -6.5, 0)
		add_child(ssign)
		var sglow := OmniLight3D.new()
		sglow.light_color = Color(1.0, 0.82, 0.4)
		sglow.light_energy = 3.2
		sglow.omni_range = 42.0
		sglow.position = ghost.position + Vector3(0, -8.0, 0)
		add_child(sglow)
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
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		add_child(mi)
		god_rays.append({"node": mi, "base": mi.rotation.z, "ph": randf() * TAU})

func _tick_god_rays(delta: float) -> void:
	if Engine.get_process_frames() % 2 == 1:
		return   # cosmetic sway — half rate is invisible, half the cost
	var tt: float = Time.get_ticks_msec() / 1000.0
	for gr in god_rays:
		var n: MeshInstance3D = gr["node"]
		if is_instance_valid(n):
			n.rotation.z = float(gr["base"]) + sin(tt * 0.25 + float(gr["ph"])) * 0.06

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
var ambience: AudioStreamPlayer = null
var _tap_player: AudioStreamPlayer = null

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
	arena_zones.clear()
	fade_walls.clear()
	lagoon_floor = false
	arena_center = ARENA_POS
	arena_dome = 48.0
	arena_ceil = 42.0
	arena_env = Environment.new()
	arena_env.background_mode = Environment.BG_COLOR
	arena_env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	arena_env.glow_enabled = true
	arena_env.glow_intensity = 0.9
	if kind == "fetch":          # snowy backyard noon
		arena_env.background_color = Color(0.75, 0.88, 1.0)
		arena_env.ambient_light_color = Color(1, 1, 1)
		arena_env.ambient_light_energy = 1.2
		_arena_floor(Color(1.0, 1.02, 1.08), GTA + "up_snow_col.jpg", GTA + "up_snow_nrm.jpg", 0.06)
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
		_arena_floor(Color(0.55, 0.52, 0.56), GTA + "up_cliff_col.jpg", GTA + "up_cliff_nrm.jpg", 0.05)
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
		arena_env.glow_bloom = 0.15
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
		var down: bool = joy_pressed(int(btns[i]))
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
