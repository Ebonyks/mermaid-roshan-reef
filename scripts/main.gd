class_name ReefMain
extends Node3D

const StoryArtFactory = preload("res://scripts/story_art.gd")
const LandmarkArtFactory = preload("res://scripts/landmark_art.gd")
const CollectionSystemLogic = preload("res://scripts/collection_system.gd")
const InteractionAffordanceLogic = preload("res://scripts/interaction_affordance.gd")
const InteractionDirectorLogic = preload("res://scripts/interaction_director.gd")
const TapMoveDirectorLogic = preload("res://scripts/tap_move_director.gd")
const LivingWorldLogic = preload("res://scripts/living_world.gd")
const BootSplashOverlayLogic = preload("res://scripts/boot_splash_overlay.gd")
const StartMenuLogic = preload("res://scripts/start_menu.gd")
const AttackCustomizerLogic = preload("res://scripts/attack_customizer.gd")
const DayOneArtStudioLogic = preload("res://scripts/day_one_art_studio.gd")
const DayOneBathroomCleanupLogic = preload(
	"res://scripts/games/day_one_bathroom_cleanup.gd")
const DayOneBathroomMovieHandoffLogic = preload(
	"res://scripts/day_one_bathroom_movie_handoff.gd")
const DAY_ONE_POOL_ROUTE_PREVIEW_TEXTURE := \
	"res://assets/flats/castle/rooms/room_mermaid_pool.png"
# Mermaid Roshan's Ocean World — Godot phase 2
# Undersea fairy garden (Kenney Nature Kit, CC0) + PBR seabed + rainbow pearls + 5 minigames.

const WATER_TOP := 58.0
const WORLD_R := 270.0
const PEARL_TOTAL := 10
# Sky Lagoon is a full-screen Canvas stage. Keep its complete stack explicit so
# the opaque world can never cover the child-facing HUD or steal camera/input
# authority from the layers above it. The promenade and living-world director
# share these values; speech, touch, pause and fade retain their existing 8/9/
# 12/30 homes.
const SKY_LAGOON_STAGE_CANVAS_LAYER := -1
const SKY_LAGOON_HUD_CANVAS_LAYER := 0
const SKY_LAGOON_LIVING_CANVAS_LAYER := 6
# Phone builds now open at the authored gatehouse before Pearl Castle. Headless
# probes keep the legacy ocean bootstrap unless they explicitly enter the hub,
# so the existing trusted activity probes remain deterministic while the new
# kingdom probe covers the launch route directly.
const START_AT_CASTLE_GATE := true
const MELODY_LEGACY_TOUCH_SOURCE := &"legacy_world_touch"
const MELODY_CONTEXT_FOCUS := &"focus"
const MELODY_CONTEXT_APPLICATION := &"application"
const MELODY_CONTEXT_CLOSE := &"window_close"
const SLIDE_CANVAS_LEGACY_TOUCH_SOURCE := &"slide_canvas_legacy_world_touch"
const SLIDE_CANVAS_CONTEXT_FOCUS := &"focus"
const SLIDE_CANVAS_CONTEXT_APPLICATION := &"application"
const SLIDE_CANVAS_CONTEXT_CLOSE := &"window_close"
const SLIDE_CANVAS_RETURN_KEYS: Array[Key] = [
	KEY_W, KEY_A, KEY_S, KEY_D,
	KEY_UP, KEY_LEFT, KEY_DOWN, KEY_RIGHT,
	KEY_SPACE, KEY_ENTER, KEY_KP_ENTER,
]
const SLIDE_CANVAS_RETURN_PAD_BUTTONS: Array[JoyButton] = [
	JOY_BUTTON_A, JOY_BUTTON_B, JOY_BUTTON_X, JOY_BUTTON_Y,
	JOY_BUTTON_DPAD_UP, JOY_BUTTON_DPAD_DOWN,
	JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT,
]

var player: Node3D
var pearls: Array[Node3D] = []
var friends: Array = []
var pearl_count := 0
var pearls_ever := 0              # highest pearl balance ever held; preserves the original 10-pearl gate after spending
var portal_unlocked := false
var trophies := 0
var medals := {}                  # game id -> best tier ever (1 bronze / 2 silver / 3 gold); persisted, upgrade-only (MedalSystem owns logic)
var hud_layer: CanvasLayer = null
var hud_pearls: Label
var hud_stars: Label
var hud_msg: Label
var hud_game: Label
var obj_card: Panel = null         # top-center picture-first objective card
var obj_icon: TextureRect = null   # friend portrait pictogram
var obj_icon_lbl: Label = null     # emoji pictogram for portal/star goals
var obj_key := ""                  # current objective identity; card pulses once on change
var obj_seen_t := 0.0              # seconds on the same target; card calms after comprehension
var msg_timer := 0.0
# ---- STORY DIALOGUE (AudioDirector owns the logic; state lives here) ----
var dialogue_queue: Array = []     # [{who, text, vo, hold}] spoken in order
var dialogue_t := 0.0              # seconds left on the line being spoken
var dialogue_active := false       # true while a story sequence is playing
var fade_rect: ColorRect = null   # full-screen black cover (layer 30) — see _fade_cut
var fade_tween: Tween = null      # active reveal tween; killed on every new cut
# ---- CRITTER BOOK: mutable state stays on ReefMain; CollectionSystem owns logic ----
var critter_collection := {}              # species id -> true; persisted in reef_save.json
var collection_nodes: Array = []          # runtime rows for the active world
var collection_root: Node3D = null
var collection_habitat := ""              # "ocean" | "lagoon" | ""
var collection_nearby_id := ""
var collection_action_prev := false
var collection_hint_shown := false
var collection_layer: CanvasLayer = null
var collection_stage: Control = null
var collection_button_layer: CanvasLayer = null
var collection_button: Button = null
var collection_category := "fish"
var voice: AudioStreamPlayer
var model_cache := {}
var _toon_mats := {}   # source material -> shared pastel override (see _toonify)
var _nature_mats: Dictionary = {}   # pastel rgba32 -> shared flat material (see _dress_nature)
var cluster_centers: Array[Vector3] = []
var pulse_lights: Array = []        # dicts {light, base, phase}
var fish_schools: Array = []
var _reef_districts: ReefDistricts = null
# ---- LIVING WORLD: mutable runtime state stays on ReefMain; the extracted
# ---- director only resolves stages and drives one reusable 2D CanvasItem.
var _living_world: LivingWorldDirector = null
var _fx_water: FxWater = null
var fxw_cards: Array = []       # live water-FX cards (fx_water.gd satellite)
var fxw_lines: Array = []       # drifting foam waterlines (same satellite)
var fxw_total := 0              # cards ever spawned — probe_passive's counter
var fxw_cool: Dictionary = {}   # per-emitter proc cooldowns
var living_specs: Dictionary = {}
var living_layer: CanvasLayer = null
var living_canvas: LivingWorldCanvas = null
var living_stage_id := ""
var living_probe_stage_override := ""
var living_time := 0.0
var living_idle_time := 0.0
var living_cooldown := 0.0
var living_event_time := -1.0
var living_event_count := 0
var living_generation := 0
var manta: Node3D   # stays null: the ghost-ship pearl shop went with the wreck; all uses are null-guarded
var manta_t := -20.0
var bloom_t := 25.0
var bloom_parts: GPUParticles3D

# ---------- minigame state ----------
var game := ""              # "", "fetch", "dolls", "seek", "race", "melody"
var g := {}                 # per-game scratch
var game_nodes: Array[Node3D] = []
var _melody_held_sources: Dictionary = {}
var _melody_input_context_losses: Dictionary = {}
var _slide_canvas_held_sources: Dictionary = {}
var _slide_canvas_input_context_losses: Dictionary = {}
var _slide_canvas_overlay_axis_wait_neutral := false
var _slide_canvas_overlay_poll_neutral_frames := 0
var _slide_canvas_return_guard_armed := false
var _slide_canvas_return_held_sources: Dictionary = {}
var _slide_canvas_return_neutral_frames := 0
var _slide_canvas_return_fade_clear := false
var _slide_canvas_return_retire_pending := false
var fs_fails := 0                  # boss attempts lost -> retry kindness (+6s each, max +12)
var _fairy_art_cache: Dictionary = {}
var world_env: Environment
var arena_env: Environment
var we_node: WorldEnvironment
var music: AudioStreamPlayer
var dance_engine: CanvasLayer = null
var return_pos := Vector3.ZERO
# The world a minigame was launched FROM, captured beside return_pos so the
# exit restores where she actually came from instead of assuming the reef.
# Null/"" mean "nothing captured yet" and fall back to the old reef values.
var return_env: Environment = null
var return_track := ""
const ARENA_POS := Vector3(0, -600, 0)
const LEVEL2_POS := Vector3(0, -1300, 0)
const CASTLE_POS := Vector3(500, -1300, 0)
const NORTHERN_POS := Vector3(0, -2200, 0)
var arena_center := Vector3(0, -600, 0)
var arena_dome := 48.0
var arena_ceil := 42.0
var portal_node: Node3D
var portal_t := 0.0
var portal_ready := false
var portal_cool := 0.0
var portal_armed := false
var ocean_kingdom := ReefDistricts.KINGDOM_CARIBBEAN
var ocean_routes_enabled := false
var ocean_return_gate_armed := false
var ocean_return_gate_cool := 0.0
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
var craft_part := "body"              # one active palette row: body / accent / third
var craft_body_rb := false           # rainbow-cycle toggle for the body layer (ww craft fx)
var craft_fins_rb := false           # rainbow-cycle toggle for the accent layer
var craft_c3 := Color(0, 0, 0, 0)    # third zone colour; alpha 0 = the kind's book-art default
var craft_unlocks := {}            # one-time pearl unlocks for craft creatures ("cat", "bird")
var craft_status: Label = null     # in-studio feedback (HUD messages sit behind the overlay)
var craft_pearl_lbl: Label = null
var custom_friends: Array = []
# ---- CASTLE LOGO TABLE: the paint-table activity owns layout only; the
# chosen emblem lives here and is saved as two stable ids.
var castle_logo_layer: CanvasLayer = null
var castle_logo_preview: Control = null
var castle_logo_room_display: Control = null
var castle_logo_color := "rainbow"
var castle_logo_symbol := "rainbow"
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
var toy_play := {}                # active playground play-moment (drives the player)
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
var kart_ocean_portal_armed := true   # Roshan must leave the gate before it can fire again
var kart_float_portals_armed := true  # shared latch for the two Sky Lagoon rainbow legs
var galaxy_gateway_armed := true      # direct Butterfly World gate uses the same rule
var kart_completion_committed := false
var kart_prev_track := ""
var galaxy_game: Node = null    # Level 3 — Butterfly World (scripts/galaxy.gd)
var galaxy_unlocked := false
var fairy_skin_unlocked := false   # Butterfly World prize: the Fairy Roshan look
var bwd_done := false              # the 7 butterflies are home FOREVER (owner: never repeat the quest)
var galaxy_from := ""              # world to restore after Butterfly World ("" ocean / "level2")
var galaxy_return_set := false     # stays set across the optional fairy-flight round trip
var galaxy_return_pos := Vector3.ZERO
var galaxy_level2_open := false
# Runtime-only Canvas route checkpoint shared by every off-lagoon trip. The
# generic spatial return positions below remain for older/non-promenade callers.
var lagoon_trip_return_master_x := -1.0
var combat_ice_done := false       # Butterfly Castle ice-berry encounter completed
var combat_fire_done := false      # Pearl Castle basement pepper encounter completed
var combat_tutorial_done := false  # the Royal Hall sparring class, finished once
## Player-selected attack presentation. These are deliberately small, stable
## values so every combat mode can read the same profile without owning save
## state or introducing another rendering path.
var attack_color: Color = Color(0.2705882353, 0.8588235294, 0.9215686275, 1.0)
var attack_effect: String = "bubbles"
var combat_game: CombatArena = null
var combat_tutorial_game: CombatTutorial = null
var combat_from := ""
var combat_prev_track := ""
# ---- STUFFED-FRIEND COMPANION (Pokemon-style wing): mutable state stays here;
# ---- CompanionSystem (scripts/companion.gd) owns the logic, StuffieBattle
# ---- (scripts/stuffie_battle.gd) owns the sparring arena ----
var companion_id := ""                    # chosen stuffie ("" until picked at the Royal Hall welcome)
var companion_colors: Array = []          # [body, accent, third] html colours from the picker
var fish_tokens := 0                      # LEGACY sparkle-fish count — kept for save compat; migrated into care_points on load
var stuffie_wins := {}                    # sparring-den ladder progress (round tag -> true)
var companion_node: Node3D = null         # the follower in the open reef (never saved)
var companion_gift: Node3D = null         # Huluu's gift box beside the Crown Star
var companion_room: Node3D = null         # the Stuffie Studio on the castle's Dreaming Floor
var companion_room_rows: Array = []       # shelf rows {id, node, marker, heart}
var companion_room_action_prev := false
var castle_room_layer: CanvasLayer = null
var castle_room_stage: Control = null
var castle_room_world_root: Node2D = null
var castle_room_background: Sprite2D = null
var castle_room_background_tiles: Array[Sprite2D] = []
var castle_room_detail_tiles: Array[Sprite2D] = []
var castle_room_mid_layer: Node2D = null
var castle_room_front_layer: Node2D = null
var castle_room_item_visual_layer: Node2D = null
var castle_room_item_effect_layer: Node2D = null
var castle_room_item_hotspot_layer: Control = null
var castle_room_door_hotspot_layer: Control = null
var castle_room_link_layer: Control = null
var castle_room_door_hotspots: Array[Dictionary] = []
var castle_room_item_sprites: Dictionary = {}
var castle_room_fixture_manifest: Dictionary = {}
var castle_room_fixture_rigs: Dictionary = {}
var castle_room_fixture_physics: Array[Node2D] = []
var castle_room_light_states: Dictionary = {}
var castle_room_prop_sfx: AudioStreamPlayer = null
var castle_room_player_sprite: Sprite2D = null
var castle_room_player_shadow: Sprite2D = null
var castle_room_action_button: Button = null
var castle_room_back_button: Button = null
var castle_room_buttons: Dictionary = {}
var castle_room_menu_panel: Control = null
var castle_room_menu_buttons: Dictionary = {}
var castle_room_menu_open := false
var castle_room_id := "main_hall"
const DAY_ONE_CASTLE_ROOM_IDS: Dictionary = {
	"bubble_bath": "bathroom",
	"mermaid_pool": "pool",
	"playroom": "stuffie",
	"craft_room": "art",
}
var day_one_active: bool = true
var day_one_current_room_id: String = "bathroom"
var day_one_completed_rooms: Dictionary = {}
var day_one_cleaned_rooms: Dictionary = {}
var day_one_arrival_plane_media_seen: bool = false
var day_one_dirty_castle_discovered: bool = false
var day_one_grok_video_2_seen: bool = false
var day_one_boss_door_glow: bool = false
var day_one_giant_dust_bunny_boss_triggered: bool = false
var day_one_bathroom_cleanup_step: int = 0
var day_one_bathroom_supply_hunt_step: int = 0
var day_one_bathroom_tools_authorized: bool = false
var day_one_pool_cleanup_step: int = 0
var day_one_pool_rumi_met: bool = false
var day_one_pool_skimmer_mask: int = 0
var day_one_pool_waterfall_mask: int = 0
var day_one_pool_seahorse_tugs: int = 0
var day_one_art_collected_materials: Dictionary = {}
var day_one_art_cleaned_grime: Dictionary = {}
var day_one_art_desk_unlocked: bool = false
var day_one_art_customization_completed: bool = false
var day_one_event_seen: Dictionary = {}
var day_one_event_history: Array[Dictionary] = []
var _day_one_director: DayOneDirector = null
var _day_one_bathroom_cleanup: DayOneBathroomCleanup = null
var _day_one_bathroom_movie_handoff: DayOneBathroomMovieHandoff = null
var _day_one_bathroom_movie_handoff_pending: bool = false
var _day_one_pool_route_button: Button = null
var _day_one_bathroom_controls_suspended: bool = false
var _day_one_bathroom_control_state: Array[Dictionary] = []
var _day_one_bathroom_menu_was_open: bool = false
var _attack_customizer: AttackCustomizer = null
var _attack_customizer_layer: CanvasLayer = null
var _day_one_art_studio: DayOneArtStudio = null
var day_one_castle_dressing: DayOneCastleDressing = null
var castle_royal_hall_mist_cards: Array[Sprite2D] = []
var castle_royal_hall_mist_time := 0.0
var castle_royal_hall_mist_flutter_time := 0.0
var castle_royal_hall_feedback_cool := 0.0
# Runtime generations prevent a delayed doorway arrival or stale event owner
# from consuming a newer Royal Hall event after navigation or re-arming.
var castle_royal_hall_arrival_generation := 0
var castle_royal_hall_arrival_pending := false
# Runtime-only event hook. Concrete story/boss controllers own persistence and
# re-arm this doorway from their saved progression flags; Callables never enter
# reef_save.json.
var castle_royal_hall_event_id := ""
var castle_royal_hall_event_entry: Callable = Callable()
var castle_royal_hall_event_generation := 0
var companion_zone := ""                  # last game context; a flip snaps the follower to her side
var companion_den: Node3D = null          # the sparkle-ring battle entrance in the reef
# ---- Tamagotchi care (owner 2026-07-20: replaces the sparkle-fish tokens) ----
var care_points := 0                      # fulfilled wants; THE growth track (persisted)
var companion_want := ""                  # active want id ("" = content)
var companion_want_bubble: Label3D = null # the emoji thought bubble over the stuffie
var companion_want_cool := 25.0           # first ask lands soon after adoption
var companion_care_t := -1.0              # >0 while a care moment animation plays
var companion_care_action_prev := false
var companion_resting := false            # retired save flag; always normalized false (compatibility only)
var companion_bruises := 0                # battle boo-boos awaiting care (persisted)
var companion_want_queue: Array = []      # queued wants (post-battle hug + bath)
var companion_rest_timer := -1.0          # >0 while injured: time until the next gentle reminder
var companion_layer: CanvasLayer = null   # picker overlay
var companion_stage: Control = null
var companion_care_layer: CanvasLayer = null # Tamagotchi care overlay
var companion_care_stage: Control = null
var companion_menu_button: Button = null  # inset upper-right HUD launcher
var companion_pick_id := ""               # picker working state
var companion_pick_colors: Array = []
var companion_pick_slot := 0               # one large active paint row at a time
var companion_pick_mode := "adopt"         # adopt / swap at chest / studio repaint
var companion_cool := 0.0                 # cheer cooldown
var companion_cheer_t := -1.0
var companion_guide_cool := 20.0          # "this way!" helper dash cooldown
var companion_greeted := false            # one-time hello per session
var companion_den_said := false           # one-time den intro per session
var companion_action_prev := false
var companion_p2 := false                 # true while a pad holds R1 — P2 steers the stuffie
var stuffie_game: StuffieBattle = null
var stuffie_from := ""
var stuffie_prev_track := ""
var stuffie_cool := 0.0
var dungeon_game: DungeonLevel = null
var dungeon_prev_track := ""
var dungeon_progress := 0          # cleared rooms, 0..10; next visit resumes here
var dungeon_done := false
var ember_game: Node = null        # the Ember Fortress (scripts/ember_fortress.gd)
var ember_found := false           # Roshan has used the dark gate at the rainbow junction
var ember_progress := 0            # fortress-dungeon checkpoint, 0..6; resumes here
var ember_done := false            # the six-room fortress dungeon is solved
var ember_from := ""               # world to restore after the Ember Fortress ("" ocean / "level2")
var ember_return_set := false
var ember_return_pos := Vector3.ZERO
var ember_level2_open := false
var ember_portal_pos := Vector3.ZERO   # the dark gateway at the rainbow junction
var ember_gateway_armed := true        # same leave-before-refire latch as the galaxy gate
var kart_float_dest := "galaxy"    # where the floating rainbow race lands ("galaxy" | "ember")
var opera_game: OperaHouse = null
var opera_pending_act_index := -1
var opera_active_act_index := -1
var opera_return_room := ""
var opera_hud_was_visible := true
var opera_hud_previous_layer := 0
var opera_hud_game_was_visible := false
var opera_obj_was_visible := false
var opera_player_was_visible := true
var opera_progress := 0            # cleared live Opera careers, 0..13
var opera_stars := 0               # stable 16-bit mask; retired bits stay preserved
var opera_done := false
# The rhythm (owner 2026-07-25): every shelled act opens with a RESCUE — imps
# have someone caged backstage — and the freed friends hand Roshan a GIFT that
# the act then cooks, paints or plays with. Gifts persist, so the carrots the
# farmers give her on Floor 1 are still in the larder for later shows.
var opera_pantry: Dictionary = {}

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
	{"id": "racer", "emoji": "🏁", "label": "Rainbow Racer", "hint": "Finish a rainbow race!"},
	{"id": "throne", "emoji": "👑", "label": "Star Princess", "hint": "Sit on the Moon Throne!"},
	{"id": "fruit", "emoji": "🍎", "label": "Butterfly Feast", "hint": "Call the swarm to a fruit tray!"},
	{"id": "butterfly", "emoji": "🦋", "label": "Butterfly Hero", "hint": "Save the Butterfly World!"},
	{"id": "flower", "emoji": "🌸", "label": "Flower Bloomer", "hint": "Bloom the giant flower!"},
	{"id": "carrot", "emoji": "🥕", "label": "Snowman Snack", "hint": "Chase the runaway snowman... and EAT him!"},
	{"id": "shopper", "emoji": "💰", "label": "Big Shopper", "hint": "Buy every treasure in the Pearl Shop!"},
	{"id": "showtime", "emoji": "🎭", "label": "Showtime Star", "hint": "Perform every show in the Opera House!"},
	{"id": "volcano", "emoji": "🌋", "label": "Fortress Hero", "hint": "Solve the Ember Fortress dungeon!"},
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
	_say("roshan", "win", 0.5)   # cheer with the toast — the fanfare alone felt silent
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
const TOUCH_MODE_HYBRID := "hybrid"
const TOUCH_MODE_CLASSIC := "classic"
var touch_mode := TOUCH_MODE_HYBRID
var touch_mode_btn: Button = null
var touch_control_blocks: Dictionary = {}
# Mutable touch experiment state stays on ReefMain. The two RefCounted
# directors receive this node and own behavior only, matching the extraction
# rules used by the arena/minigame satellites.
var touch_interactables: Array = []
# Active HitEngine instances (encounters register in start, unregister on
# teardown). Enemy priority rule: these get first refusal on every world
# tap, ahead of touch_interactables — see _on_touch_world.
var hit_engines: Array = []
# castle-local chain engine (combat wing 2026-08): deliberately NEVER in
# hit_engines — the castle owns its own touch path; this instance supplies
# the pop-chain, pips and feel to the dust-bunny pops there.
var castle_dust_he: HitEngine = null
# Daddy Mermaid's castle partner bubble (combat wing): staged in by the
# child's first bunny pop each visit, torn down with the castle.
var castle_partner: PartnerAssist = null
var touch_focus_id := ""
var touch_focus_ready := false
var touch_registry_t := 0.0
var touch_discovery_ring: MeshInstance3D = null
var touch_focus_ring: MeshInstance3D = null
var touch_auto_active := false
var touch_auto_target := Vector3.ZERO
var touch_auto_waypoint := Vector3.ZERO
var touch_auto_interactable := ""
var touch_auto_activation_radius := 5.0
var touch_auto_last_distance := 0.0
var touch_auto_stall_t := 0.0
var touch_auto_recoveries := 0
var _interaction_director: InteractionDirector = null
var _tap_move_director: TapMoveDirector = null
var quality := "sparkly"
var music_on := true
# Spoken spells (prototype 2026-08-02, see MIC_SPELLS.md). DEFAULT-ON is an
# owner decision: MIC_DEFAULT_ON is the ONE flip point — set it to false and
# the toggle, the save default and a fresh install all ship the feature dark.
# On-by-default is only safe because the microphone device is opened lazily on
# the first battle (never at boot), a denied RECORD_AUDIO permission silently
# disables the feature forever, and the ICE/FIRE buttons are always live.
const MIC_DEFAULT_ON := true
var mic_on := MIC_DEFAULT_ON
var mic_state := "idle"        # idle | asking | listening | enroll | test | off
var mic_last_word := ""        # debug/HUD readout of the last accepted spell
var mic_last_dist := -1.0      # ...and its DTW distance, for calibration
var mic_enroll_left := 0
var mic_permission_denied := false
var mic_teach_layer: CanvasLayer = null
var mic_btn: Button
var save_data := {}
var save_generation := 0   # monotonically orders primary/.tmp/.bak snapshots
var has_saved_game := false
var save_dirty := false    # main retains failed-write responsibility after a minigame frees
var save_retry_t := 0.0
var save_pending := false  # debounced write queued by the hot sites (pearl pickup, friend discovery)
var save_pending_t := 0.0
var plays := 0           # launch counter — alternates day/night across playthroughs
var is_night := false    # subtle day/night variation for both worlds
var lagoon_floor := false  # when true, the player's floor follows the Sky Lagoon heightfield
var northern_floor := false  # the world beyond the Alpine cave has its own terrain heightfield
var pearl_lights: Array = []
var sun_light: DirectionalLight3D
var caustics_plane: MeshInstance3D = null   # animated light dapples on the reef floor
var caustics_mat: ShaderMaterial = null      # terrain-conforming dapple overlay (day/night tuned)
var caustics_enabled := true                # developer mode can switch the caustic layer off
var dev_mode: Node = null                   # in-game developer "look lab" (scripts/dev_mode.gd)
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
var pause_dim: ColorRect = null      # full-screen cool dim under the pause panel
var pause_gear_btn: Button = null    # top-right pause button (128 hit / 112 visual)
var pause_grid: GridContainer = null # secondary icon tiles (probe-checked sizes)
var pause_resume_btn: Button = null
var pause_leave_btn: Button = null
var fps_lbl: Label = null
# bedtime: swim onto the castle bed -> tuck-in cutscene that flips day <-> night
var sleep_t := -1.0
var sleep_cool := 0.0
var sleep_layer: CanvasLayer = null
var sleep_overlay: ColorRect = null
var sleep_flip_done := false
var hug_layer: CanvasLayer = null
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
var wreck_pos := Vector3.ZERO   # stays ZERO: the 3D wreck was deleted 2026-07-28 (redesigned); guards below and companion.gd no-op on ZERO
var shop_cool := 0.0
var treasure_cool := 0.0
# Cosmetics are full alternative skins (mutually exclusive), chosen at the bedroom wardrobe.
# "classic" is the animated 2.5D Roshan; other looks keep their existing paths.
# (The Fairy Mermaid is NOT a wardrobe skin — it is Roshan's look inside the Fairy Pond game.)
const SKINS := [
	{"id": "classic", "label": "Roshan", "preview": "res://assets/characters/roshan_25d/roshan_base.png", "sprite": ""},
	{"id": "fairy", "label": "Fairy Mermaid", "preview": "res://assets/characters/skins/fairy_mermaid.png", "sprite": "res://assets/characters/skins/fairy_mermaid.png"},
	{"id": "huluu", "label": "Princess Huluu", "preview": "res://assets/characters/friends/huluu.png", "sprite": "res://assets/characters/friends/huluu.png"}]
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
var peng_wave_cool := 0.0   # portal penguin's interactive cheer cooldown
var peng_pal: Node3D = null          # the caught baby penguin — follows Roshan in the reef
var peng_pal_cool := 0.0             # pal's cheer/giggle cooldown
var peng_pal_cheer_t := -1.0         # while >0 the cheer clip owns the pal
var peng_pal_greeted := false        # one-time "I'm coming too!" message per session
var peng_giggle: AudioStreamPlayer = null   # the baby's squeaky giggle
var brawl_fr := {"fname": "Toy Castle", "game": "brawl", "won": true, "cool": 0.0}
var brawl_portal_pos := Vector3.ZERO
var brawl_cool := 0.0
# the great dust bunny's attic (scripts/games/dust_boss.gd) — a boss with one
# rule: he is only open while airborne with his star flashing
var dust_boss_fr := {"fname": "Dusty Attic", "game": "dustboss", "won": true, "cool": 0.0}
var dust_boss_portal_pos := Vector3.ZERO
var dust_boss_cool := 0.0
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
# that only ever grows. The early procedural cosmetics (Rainbow Trail / Pearl
# Tiara / Pearl Princess) were retired 2026-07-13 — low-res primitives that
# never sat right on the V2+ bodies; any new treasure must be a hard-generated
# asset that actually fits her. Old saves keep their "owned" flags harmlessly.
const SHOP_ITEMS := [
	{"id": "beans", "label": "Can of Beans", "price": 2},
	{"id": "tail", "label": "Rainbow Trail", "price": 60},
	{"id": "tiara", "label": "Pearl Tiara", "price": 120},
	{"id": "pearlskin", "label": "Pearl Princess", "price": 250}]
var shop_owned := {}   # permanent Pearl Shop treasures (persisted)
# THE ANIMAL TANKS: these reef friends start out in glass tanks on the
# cabin's back wall. Buying one sets it free into the reef forever - her
# pearls turn into living neighbours, not just a bigger number. Patrol
# rows are [radius, speed, y, scale], copied verbatim from the old
# _build_aquatic_creatures roster so a released animal swims exactly the
# route it always did; "babies" restores that species' school slots.
const ANIMAL_SHOP := [
	{"id": "stingray", "model": "StingRay", "label": "Sting Ray", "price": 20, "babies": 2,
		"patrols": [[75.0, 0.07, 7.0, 2.4], [110.0, 0.06, 16.0, 2.4]]},
	{"id": "turtle", "model": "Turtle", "label": "Sea Turtle", "price": 25, "babies": 2,
		"patrols": [[55.0, 0.06, 9.0, 1.6], [90.0, 0.05, 13.0, 1.6]]},
	{"id": "squid", "model": "Squid", "label": "Squid", "price": 30, "babies": 1,
		"patrols": [[60.0, 0.05, 18.0, 2.0]]},
	{"id": "dolphin", "model": "Dolphin", "label": "Dolphin", "price": 40, "babies": 0,
		"patrols": [[140.0, 0.08, 34.0, 2.6]]}]
var animals_owned := {}    # tank friends released into the reef (persisted)
var animals_spawned := {}  # runtime: released species already swimming this session
var flora_nodes: Array = []
var first_session := true
var start_menu_active := false
var start_menu_layer: CanvasLayer = null
var chime: AudioStreamPlayer
var buy_sound: AudioStreamPlayer
var beans_sfx: AudioStreamPlayer   # banjo toot-loop: a SOUND EFFECT, not music (plays with music off)
var hop_sfx: AudioStreamPlayer     # soft cartoon boing per on-land hop touchdown
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

const FRIEND_DEFS := [
	{"tex": "pearl_friend",  "fname": "Evie and Lamb-a'",      "msg": "You found us! Swim close again to play hide and seek!", "game": "seek"},
	{"tex": "two_friends",   "fname": "Harper and Fiona",      "msg": "Sisters Harper and Fiona! Come grab the fish down the rainbow slide!", "game": "slide", "theme": "rainbow", "mode": "fish"},
	{"tex": "mama_baby",     "fname": "Faron",                 "msg": "Faron and her dolls! Return to catch the sleepy dolls!", "game": "dolls",
		"discover_radius": 12.0, "linger_radius": 13.0, "start_radius": 10.0},
	{"tex": "daddy",         "fname": "Daddy Mermaid",         "msg": "Daddy Mermaid! Come catch the rainbow on stage!", "game": "melody"},
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
	# OS focus/background notifications are independently nested. Never let
	# delayed platform traffic rebuild Melody's entry-source census, and never
	# route a live Melody stage until every loss reason and its first-active-tick
	# restoration guard have cleared.
	if _slide_canvas_fish_route_active() or _slide_canvas_return_guard_active():
		_observe_slide_canvas_return_source(ev)
	if _slide_canvas_return_guard_active() \
			and _slide_canvas_return_physical_event(ev):
		# The return fade is still opaque or the pre-return physical levels have
		# not established a trustworthy neutral boundary. Observe terminal levels
		# above, then consume the whole gameplay vocabulary before Reef systems or
		# a focused Control can turn a held source into a fresh action.
		get_viewport().set_input_as_handled()
		return
	var melody_context_blocked: bool = _melody_input_context_blocks_input()
	var slide_canvas_context_blocked: bool = _slide_canvas_input_context_blocks_input()
	var slide_canvas_source: StringName = _slide_canvas_source_token(ev)
	var slide_canvas_source_was_held: bool = not slide_canvas_source.is_empty() \
		and _slide_canvas_held_sources.has(slide_canvas_source)
	if not melody_context_blocked:
		_track_melody_source_state(ev)
	if not slide_canvas_context_blocked:
		_track_slide_canvas_source_state(ev)
	if game == "melody" and melody_context_blocked:
		# Fail closed before TouchUI or a focused Pause Control can interpret stale
		# queued actions. TouchUI repeats this sink while Main is SceneTree-paused.
		get_viewport().set_input_as_handled()
		return
	if _slide_canvas_fish_route_active() and slide_canvas_context_blocked:
		# The fish slide has the same source-free restoration boundary. Consume
		# delayed platform traffic before it can steer or activate a Pause control.
		get_viewport().set_input_as_handled()
		return
	if _slide_canvas_fish_route_active() \
			and _slide_canvas_overlay_axis_wait_neutral:
		# The controller guard has retired, but polled overlay sources still need
		# two trustworthy neutral samples. Record their raw level only; consume the
		# event before a focused GUI Button can reinterpret held A/B as ui_accept.
		_record_slide_canvas_poll_level(ev)
		get_viewport().set_input_as_handled()
		return
	# Story exchanges advance on the next deliberate press and consume that
	# press, so skipping a witness line never also scores the task underneath.
	var dialogue_press := false
	if ev is InputEventScreenTouch:
		dialogue_press = (ev as InputEventScreenTouch).pressed
	elif ev is InputEventMouseButton:
		var mouse_event := ev as InputEventMouseButton
		dialogue_press = mouse_event.pressed and mouse_event.button_index == MOUSE_BUTTON_LEFT \
			and mouse_event.device != InputEvent.DEVICE_ID_EMULATION
	elif ev is InputEventJoypadButton:
		dialogue_press = (ev as InputEventJoypadButton).pressed
	elif ev is InputEventKey:
		var key_event := ev as InputEventKey
		dialogue_press = key_event.pressed and not key_event.echo
	if game == "opera" and dialogue_press and skip_dialogue():
		get_viewport().set_input_as_handled()
		return
	if _route_slide_canvas_input(ev, slide_canvas_source_was_held):
		# A claimed Canvas steer never reaches the hidden Reef activity census or
		# seeds its raw-pad fallback state. A terminal axis/d-pad event may be the
		# release of a level first observed by an overlay, so mirror only that neutral
		# value to prevent a stale cursor on the next overlay opening.
		if _slide_canvas_source_release(ev):
			_record_slide_canvas_poll_level(ev)
		get_viewport().set_input_as_handled()
		return
	if not _slide_canvas_fish_route_active():
		# The opaque ride suspends the hidden Reef's living-world clock. Unclaimed
		# controller traffic may still update the legacy raw-pad fallback below,
		# but it must not cancel or cool down a passive Reef event behind the stage.
		_living_world_ref().note_input(ev)
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
	if _route_melody_input(ev):
		get_viewport().set_input_as_handled()
		return

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
	# GEN3 geography (owner 2026-07-13: "very same-y... larger hills, more
	# geography"). Three scales shape the reef: the original rolling detail
	# and sparse bumps, plus a broad LANDMARK SWELL — real hills and basins
	# a swimmer can navigate by — faded near the spawn plaza so the castle
	# approach stays open. Interior height is capped well under WATER_TOP
	# (and under the fixed-height ice floe/ship); past the rim the floor
	# climbs steep scalloped CLIFF BAYS instead of the old smooth cone.
	var h: float = fbm(x * 0.013, z * 0.013) * 26.0 - 6.0
	h += maxf(0.0, fbm(x * 0.05 + 30.0, z * 0.05 + 30.0) - 0.62) * 30.0
	var d := sqrt(x * x + z * z)
	var swell: float = (fbm(x * 0.0045 + 7.0, z * 0.0045 - 11.0) * 2.0 - 1.0) * 24.0
	h += swell * clampf((d - 34.0) / 56.0, 0.0, 1.0)
	h = minf(h, 24.0)
	if d > WORLD_R * 0.82:
		var rim: float = d - WORLD_R * 0.82
		# capped so the cliff ring CRESTS and the painted seamount backdrop
		# shows above it (uncapped, the mesh corners towered over the ring)
		h += minf(rim * 0.85 + sin(atan2(z, x) * 9.0 + rim * 0.06) * minf(rim * 0.25, 7.0), 84.0)
	return ReefDistricts.shape_terrain(x, z, h)

func _district_ref() -> ReefDistricts:
	if _reef_districts == null:
		_reef_districts = ReefDistricts.new(self)
	return _reef_districts

func _living_world_ref() -> LivingWorldDirector:
	if _living_world == null:
		_living_world = LivingWorldLogic.new(self)
	return _living_world

func _fx_water_ref() -> FxWater:
	if _fx_water == null:
		_fx_water = FxWater.new(self)
	return _fx_water

func fx_splash(pos: Vector3, energy: float, emitter: String = "", cfg: Dictionary = {}) -> void:
	# the shared water-FX proc point (WATER_PHYSICS_EVALUATION_2026-08-02.md):
	# every water system calls this on a discrete crossing event — never from
	# an ambient channel — so the whole game splashes in one vocabulary
	_fx_water_ref().splash(pos, energy, emitter, cfg)

func _ready() -> void:
	BootSplashOverlayLogic.show(self)
	for jmap in EXTRA_JOY_MAPPINGS:
		Input.add_joy_mapping(String(jmap), true)
	Input.joy_connection_changed.connect(func(_dev: int, _conn: bool):
		joy_ev_axis.clear()   # never let a departed pad leave phantom input behind
		joy_ev_btn.clear()
		if not _conn:
			_forget_melody_pad_device(_dev)
			_forget_slide_canvas_pad_device(_dev)
		_refresh_joy_mapped())
	_refresh_joy_mapped()
	_build_environment()
	_build_terrain()
	_build_water()
	_build_wind_streaks()
	_build_surf_rings()
	_build_garden()
	_build_meadows()
	_build_aquatic_flora()
	_build_aquatic_creatures()
	_build_events()
	_build_pearls()
	_build_friends()
	_build_kart_portal()
	_build_player()
	_build_hud()
	_build_fade_cover()
	_living_world_ref().setup()
	_apply_cel_shading()
	# (the storybook page frame — dotted border + corner bubbles — was removed
	# here, owner request 2026-07-21: the screen was getting too busy)
	get_tree().node_added.connect(_hook_button_taps)
	voice = AudioStreamPlayer.new()
	voice.stream = load("res://assets/audio/voice_yay.mp3")
	voice.bus = "Voice"
	add_child(voice)
	chime = AudioStreamPlayer.new()
	chime.stream = load("res://assets/audio/chime.ogg")
	chime.bus = "SFX"
	chime.volume_db = -4.0
	add_child(chime)
	hop_sfx = AudioStreamPlayer.new()
	hop_sfx.stream = load("res://assets/audio/hop_boing.ogg")
	hop_sfx.bus = "SFX"
	hop_sfx.volume_db = -12.0   # a scoot is many hops — keep the boing well under the chime
	add_child(hop_sfx)
	peng_giggle = AudioStreamPlayer.new()
	peng_giggle.stream = load("res://assets/audio/penguin_giggle.ogg")
	peng_giggle.bus = "SFX"
	peng_giggle.volume_db = -3.0
	add_child(peng_giggle)
	buy_sound = AudioStreamPlayer.new()
	buy_sound.stream = load("res://assets/audio/buy.ogg")
	buy_sound.bus = "SFX"
	beans_sfx = AudioStreamPlayer.new()
	beans_sfx.bus = "SFX"
	var banjo_st: AudioStream = load("res://assets/audio/music/banjo.ogg")
	if banjo_st is AudioStreamOggVorbis:
		(banjo_st as AudioStreamOggVorbis).loop = true
	beans_sfx.stream = banjo_st
	beans_sfx.volume_db = -7.0
	add_child(beans_sfx)
	add_child(buy_sound)
	for vp in range(4):
		var ap := AudioStreamPlayer.new()
		ap.bus = "Voice"
		add_child(ap)
		voice_pool.append(ap)
	touch_ui = preload("res://scripts/touch_ui.gd").new()
	add_child(touch_ui)
	if OS.has_feature("editor") or "--dev-mode" in OS.get_cmdline_user_args():
		dev_mode = preload("res://scripts/dev_mode.gd").new()
		add_child(dev_mode)
	_build_guide()
	_build_slide_portal()
	_build_brawl_portal()
	dust_boss_portal_pos = _game_obj("dustboss", DustBossGame).build_portal()
	_build_pause()
	_load_save()
	_init_touch_experiment()
	# Display builds defer the authored gatehouse entry until the start menu
	# knows whether this is a direct Continue or a fresh Day 1 adventure.
	# Headless probes retain their established self-directed bootstrap.
	_collection_ref().build()
	if DisplayServer.get_name() == "headless":
		if first_session:
			_build_intro()
	else:
		_build_start_menu()
	_spawn_crafted_fish()   # save loads after the reef builds; spawn her fish now
	_spawn_shop_animals()   # same ordering trap: released tank friends spawn now
	_warm_shaders()         # precompile the hot runtime shaders behind the intro

func _warm_shaders() -> void:
	# Pipeline pre-warm: the runtime ShaderMaterials that first draw MID-PLAY
	# (the trophy beach ball, the first cel/coral_flow toonified prop, the
	# first sparkle burst) each hitch the phone on their first frame while the
	# driver compiles them. Draw each once now, far below the world, while the
	# intro/first seconds cover the cost. extra_cull_margin keeps the draws
	# from being frustum-culled (a culled draw compiles nothing); no fragment
	# ever lands on screen. Display builds only — the headless dummy renderer
	# compiles nothing and probes must not carry the extra nodes.
	if DisplayServer.get_name() == "headless":
		return
	var rig := Node3D.new()
	rig.position = Vector3(0.0, -5000.0, 0.0)
	add_child(rig)
	var mats: Array[Material] = []
	mats.append(_ball_panel_mat())   # shares the cached Shader _game_ball uses
	var cel := ShaderMaterial.new()  # _cel_replace's default pair: cel + ink outline next_pass
	cel.shader = load("res://assets/shaders/cel.gdshader")
	cel.set_shader_parameter("tint", Color(1.0, 1.0, 1.0))
	cel.next_pass = _gen2_outline_mat()
	mats.append(cel)
	var flow := ShaderMaterial.new() # the swaying-coral variant (see _cel_replace)
	flow.shader = load("res://assets/shaders/coral_flow.gdshader")
	flow.set_shader_parameter("phase", 0.0)
	flow.set_shader_parameter("aabb_y0", -0.6)
	flow.set_shader_parameter("aabb_h", 1.2)
	flow.next_pass = _gen2_outline_mat()
	mats.append(flow)
	for mat in mats:
		var mi := MeshInstance3D.new()
		var sph := SphereMesh.new()
		sph.radius = 0.5
		sph.height = 1.0
		sph.radial_segments = 8
		sph.rings = 4
		mi.mesh = sph
		mi.material_override = mat
		mi.extra_cull_margin = 16384.0
		rig.add_child(mi)
	# the trophy sparkle burst: CPUParticles draws are their own pipeline
	# variant, so warm one with _sparkle_burst's exact material recipe
	var cp := CPUParticles3D.new()
	cp.amount = 4
	cp.lifetime = 1.1
	cp.emitting = true
	var bm := BoxMesh.new()
	bm.size = Vector3(0.3, 0.3, 0.3)
	cp.mesh = bm
	var pm := StandardMaterial3D.new()
	pm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	pm.albedo_color = Color(1.0, 0.9, 0.7)
	cp.material_override = pm
	cp.extra_cull_margin = 16384.0
	rig.add_child(cp)
	# a handful of frames is enough for the driver to finish; then vanish
	get_tree().create_timer(0.5).timeout.connect(rig.queue_free)

# the storybook intro overlay lives in scripts/intro_overlay.gd
# (state stays here; IntroOverlay receives main by reference)
var _start_menu: StartMenu = null
var _intro_overlay: IntroOverlay = null

func _start_menu_ref() -> StartMenu:
	if _start_menu == null:
		_start_menu = StartMenuLogic.new(self)
	return _start_menu

func _build_start_menu() -> void:
	_start_menu_ref().build()

func _intro_ref() -> IntroOverlay:
	if _intro_overlay == null:
		_intro_overlay = IntroOverlay.new(self)
	return _intro_overlay

func _build_intro() -> void:
	_intro_ref()._build_intro()

func _intro_next() -> void:
	_intro_ref()._intro_next()

func _skip_intro() -> void:
	_intro_ref()._skip_intro()

func _unhandled_input(ev: InputEvent) -> void:
	# gamepad/keyboard advance for the storybook intro (taps and clicks land on
	# the invisible full-screen button; this covers A/B/Start, Space and Enter)
	if start_menu_active or not intro_active:
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
		show_msg("Roshan", "Wow! A GIANT whale! Hello, big friend!", "whale")
		return
	# the floating ghost ship on the water
	if manta != null and is_instance_valid(manta) and manta.position.distance_to(ppos) < 26.0:
		roshan_spot_cool = 14.0
		show_msg("Roshan", "A magic ship on the water! I wonder what is inside...", "ship")
		return
	# the sunken pirate ship
	if wreck_pos != Vector3.ZERO and wreck_pos.distance_to(ppos) < 24.0:
		roshan_spot_cool = 14.0
		show_msg("Roshan", "Ooh, a sunken ship! Maybe there is treasure down there!", "wreck")
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
		world_env.glow_intensity = _world_glow_target()
		if caustics_mat != null:          # bright sun dapples
			caustics_mat.set_shader_parameter("strength", 0.30)
			caustics_mat.set_shader_parameter("tint", Vector3(0.50, 0.80, 0.90))
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
		var jelly: Node3D = _gen2_creature("jellyfish", Vector3.ZERO, 5.4 + float(i % 3) * 0.7)
		if jelly == null:
			continue
		var jl := OmniLight3D.new()
		jl.light_color = jc
		jl.light_energy = 1.1
		jl.omni_range = 15.0
		jl.visible = (q != "speedy") or (i % 2 == 0)
		jelly.add_child(jl)
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

func _apply_scene_grade(env: Environment, profile: String) -> void:
	# Bright arenas used to stack the reef grade with near-white albedo and hot
	# ambient light. Named profiles keep those independently-built worlds inside
	# one contrast envelope while preserving the reef's established treatment.
	#
	# GRADE RULE for the 2.5D worlds (LIGHTING_2P5D_AUDIT_2026-08-02 §E1): every
	# profile that shows painted flats directly is showing FINISHED art through
	# an unshaded card. Its job is to be nearly transparent — match the panel,
	# protect both ends of the value range, and leave the look to the painting.
	# So: white_point >= ~1.55 (ACES below that puts painted highlights over the
	# knee and clips single channels, which reads as a hue shift, not as
	# overexposure), and post `contrast` <= ~1.05 (contrast pivots on 0.5 and
	# attacks the top and bottom of the range at once). tools/check_grade_headroom.py
	# gates this against the real art. The reef default and "ember" are exempt:
	# the reef is 3D meshes rather than flats, and Ember's harder grade is a
	# deliberate art decision (dark basalt must stay dark).
	_grade(env)
	var full_exposure: float = 1.15
	var speedy_exposure: float = 1.05
	var white_point: float = 1.2
	var saturation: float = 1.0
	var contrast: float = 1.0
	var brightness: float = 1.0
	var full_ambient_cap: float = env.ambient_light_energy
	var speedy_ambient_cap: float = env.ambient_light_energy
	match profile:
		"sky_lagoon":
			# The Lagoon has its own daylight and a largely pearl/snow palette.
			# Keep enough headroom for those pale surfaces to retain their painted
			# value steps instead of clipping into one white mass on Mobile.
			# 2026-08-02: the high white point already protected the highlights
			# (0.2% -> 0.05% clipped), but contrast 1.16 with brightness < 1.0
			# crushed 8.5% of the panorama's shadows to solid black. The painted
			# flats carry their own contrast; post-contrast only attacks the ends.
			full_exposure = 0.72
			speedy_exposure = 0.66
			white_point = 1.55
			saturation = 1.10
			contrast = 1.04
			brightness = 1.0
			full_ambient_cap = 0.46
			speedy_ambient_cap = 0.42
		"bright_pastel":
			full_exposure = 0.88
			speedy_exposure = 0.78
			white_point = 1.62
			saturation = 1.04
			contrast = 1.03
			brightness = 0.97
			full_ambient_cap = 0.75
			speedy_ambient_cap = 0.68
		"warm_pastel":
			full_exposure = 0.92
			speedy_exposure = 0.82
			white_point = 1.62
			saturation = 1.06
			contrast = 1.03
			brightness = 0.97
			full_ambient_cap = 0.82
			speedy_ambient_cap = 0.74
		"galaxy":
			full_exposure = 0.92
			speedy_exposure = 0.82
			white_point = 1.58
			saturation = 1.04
			contrast = 1.04
			brightness = 0.97
			full_ambient_cap = 0.82
			speedy_ambient_cap = 0.72
		"ember":
			# The Ember Fortress: dark stone must STAY dark on Mobile while
			# the lava emission blooms — deeper exposure, harder contrast,
			# and a low ambient cap so the night-black basalt keeps its dread.
			full_exposure = 0.85
			speedy_exposure = 0.76
			white_point = 1.4
			saturation = 1.04
			contrast = 1.18
			brightness = 0.92
			full_ambient_cap = 0.55
			speedy_ambient_cap = 0.48
		_:
			pass
	env.tonemap_white = white_point
	env.adjustment_enabled = true
	env.adjustment_saturation = saturation
	env.adjustment_contrast = contrast
	env.adjustment_brightness = brightness
	var full_ambient: float = minf(env.ambient_light_energy, full_ambient_cap)
	env.set_meta("scene_grade_profile", profile)
	env.set_meta("scene_grade_exposure", Vector2(full_exposure, speedy_exposure))
	env.set_meta("scene_grade_ambient", Vector2(full_ambient, minf(full_ambient, speedy_ambient_cap)))
	_refresh_scene_grade(env)

func _refresh_scene_grade(env: Environment) -> void:
	if not env.has_meta("scene_grade_exposure") or not env.has_meta("scene_grade_ambient"):
		return
	var exposures: Vector2 = env.get_meta("scene_grade_exposure")
	var ambients: Vector2 = env.get_meta("scene_grade_ambient")
	var speedy: bool = quality == "speedy"
	env.tonemap_exposure = exposures.y if speedy else exposures.x
	env.ambient_light_energy = ambients.y if speedy else ambients.x

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
	_speedy_glow_clamp(env)

func _speedy_glow_clamp(env: Environment) -> void:
	# speedy quality = calmer bloom EVERYWHERE, not just the reef. Remembers the
	# full-quality pair in meta first so _apply_quality can restore it live when
	# the player toggles back to sparkly mid-scene.
	env.set_meta("ww_full", Vector2(env.glow_intensity, env.glow_bloom))
	if quality == "speedy":
		env.glow_intensity = minf(env.glow_intensity, 0.75)
		env.glow_bloom = minf(env.glow_bloom, 0.12)

func _world_glow_target() -> float:
	# ONE place decides the reef glow intensity so day/night and the quality
	# toggle can't fight over it (last-writer-wins bugs)
	var gi: float = 0.82 if is_night else 0.68   # landmarks glow; the whole reef no longer does
	return minf(gi, 0.75) if quality == "speedy" else gi

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
	_wind_waker_bloom(env, 0.68, 0.22, 0.96)   # selective magic, not a white wash over ordinary scenery
	env.adjustment_enabled = true
	env.adjustment_saturation = 0.98
	env.adjustment_contrast = 1.03
	env.adjustment_brightness = 0.96
	_grade(env)
	world_env = env
	we_node = WorldEnvironment.new()
	we_node.environment = env
	add_child(we_node)
	music = AudioStreamPlayer.new()
	music.bus = "Music"
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
	# GEN3 terrain shader: triplanar compact up_sand map on the flats (the prior
	# painted sheet read as cracked dirt), blending to the new painted
	# CLIFF-WALL sheet on steep slopes, so the hills and the scalloped rim
	# bays have real wall detail (owner 2026-07-13: "walls have no details").
	# Vertex colours keep the storybook depth banding exactly as before.
	var mat := ShaderMaterial.new()
	var tsh := Shader.new()
	tsh.code = """shader_type spatial;
uniform sampler2D sand_tex : source_color, repeat_enable, filter_linear_mipmap;
uniform sampler2D cliff_tex : source_color, repeat_enable, filter_linear_mipmap;
uniform vec3 sand_tint = vec3(0.55, 0.72, 0.74);
uniform vec3 cliff_tint = vec3(0.95, 0.98, 1.12);
varying vec3 wpos;
varying vec3 vcol;
void vertex(){
	wpos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	vcol = COLOR.rgb;
}
vec3 tri(sampler2D t, vec3 p, vec3 n, float s){
	vec3 w = abs(n);
	w /= (w.x + w.y + w.z);
	return texture(t, p.yz * s).rgb * w.x + texture(t, p.xz * s).rgb * w.y + texture(t, p.xy * s).rgb * w.z;
}
float district(vec2 p, vec2 c, float r){
	return 1.0 - smoothstep(r * 0.45, r, distance(p, c));
}
void fragment(){
	vec3 n = normalize(mat3(INV_VIEW_MATRIX) * NORMAL);
	vec3 sand = tri(sand_tex, wpos, n, 0.06) * sand_tint * vcol;
	vec3 cliff = tri(cliff_tex, wpos, n, 0.028) * cliff_tint * mix(vcol, vec3(1.0), 0.45);
	float steep = smoothstep(0.35, 0.62, 1.0 - n.y);
	vec3 zone = vec3(0.94, 0.96, 0.96);
	zone = mix(zone, vec3(0.92, 1.00, 0.88), district(wpos.xz, vec2(-35.0, 165.0), 70.0));
	zone = mix(zone, vec3(0.78, 0.76, 0.92), district(wpos.xz, vec2(-160.0, 135.0), 68.0));
	zone = mix(zone, vec3(0.96, 0.80, 1.06), district(wpos.xz, vec2(-165.0, 5.0), 62.0));
	zone = mix(zone, vec3(1.08, 0.89, 0.72), district(wpos.xz, vec2(-40.0, -165.0), 70.0));
	zone = mix(zone, vec3(0.80, 0.94, 1.08), district(wpos.xz, vec2(140.0, -115.0), 70.0));
	zone = mix(zone, vec3(1.02, 0.94, 0.86), district(wpos.xz, vec2(35.0, 30.0), 50.0));
	ALBEDO = mix(sand, cliff, steep) * zone;
	ROUGHNESS = 0.95;
	SPECULAR = 0.05;
}"""
	mat.shader = tsh
	mat.set_shader_parameter("sand_tex", load("res://assets/terrain/up_sand_col.jpg"))
	var cliff_path := "res://assets/terrain/up_cliffwall_col.jpg"
	if not ResourceLoader.exists(cliff_path):
		cliff_path = "res://assets/terrain/up_cliff_col.jpg"   # strangler-fig fallback
	mat.set_shader_parameter("cliff_tex", load(cliff_path))
	mi.material_override = mat
	add_child(mi)
	_add_caustics(mesh)
	_add_plankton()
	_build_backdrop()
	_build_landmark_hills()

func _build_backdrop() -> void:
	# GEN3: painted seamount silhouettes ring the world beyond the rim — the
	# empty gradient horizon finally has geography (nano-banana panorama;
	# mirror-wrapped in the shader so the loop can never seam)
	if not ResourceLoader.exists("res://assets/terrain/backdrop_seamounts.jpg"):
		return
	var ring := MeshInstance3D.new()
	var cyl := CylinderMesh.new()
	cyl.top_radius = WORLD_R + 70.0
	cyl.bottom_radius = WORLD_R + 70.0
	cyl.height = 150.0
	cyl.radial_segments = 48
	cyl.rings = 1
	cyl.cap_top = false
	cyl.cap_bottom = false
	ring.mesh = cyl
	var bsh := Shader.new()
	bsh.code = """shader_type spatial;
render_mode unshaded, cull_front, shadows_disabled;
uniform sampler2D pano : source_color, repeat_enable, filter_linear_mipmap;
uniform vec3 fog_col = vec3(0.13, 0.38, 0.48);
void fragment(){
	float u = 1.0 - abs(fract(UV.x * 1.5) * 2.0 - 1.0);
	vec3 col = texture(pano, vec2(u, UV.y)).rgb;
	float fade = smoothstep(0.45, 0.02, UV.y);
	ALBEDO = mix(col, fog_col, fade * 0.92);
}"""
	var bm := ShaderMaterial.new()
	bm.shader = bsh
	bm.set_shader_parameter("pano", load("res://assets/terrain/backdrop_seamounts.jpg"))
	ring.material_override = bm
	ring.position = Vector3(0, 38.0, 0)
	ring.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(ring)

func _build_landmark_hills() -> void:
	_district_ref().build_macro_structures()

func _add_caustics(terrain_mesh: Mesh) -> void:
	# light dapples glued to the actual seabed: the terrain mesh drawn a second
	# time with an additive caustic pass. Peak brightness stays well under the
	# bloom threshold so the dapples never blow out to white sheets.
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode blend_add, unshaded, depth_draw_never, shadows_disabled;
uniform sampler2D caustic;
uniform float strength = 0.18;
uniform vec3 tint = vec3(0.42, 0.66, 0.72);
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
	rock_pbr.albedo_color = Color(0.62, 0.68, 0.76)
	rock_pbr.normal_enabled = true
	rock_pbr.normal_texture = load("res://assets/terrain/up_cliff_nrm.jpg")
	rock_pbr.roughness_texture = load("res://assets/terrain/up_cliff_rgh.jpg")
	rock_pbr.uv1_triplanar = true
	rock_pbr.uv1_world_triplanar = true   # static rocks: same texel size no matter the node scale
	rock_pbr.uv1_scale = Vector3(0.3, 0.3, 0.3)
	wood_overlay = StandardMaterial3D.new()
	wood_overlay.albedo_texture = load("res://assets/terrain/up_shipwood_col.png")
	wood_overlay.albedo_color = Color(1.2, 1.16, 1.2)      # lift so MUL keeps base colors
	wood_overlay.normal_enabled = false
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
		"pad": pad,   # CameraKit: the pad ring is body-clearance AIR, not mesh
	})

func _cyl_solid(center: Vector3, r: float, half_h: float, pad: float = 1.6) -> void:
	# vertical-cylinder collider for an arena column
	arena_solids.append({
		"box": false,
		"x": center.x, "z": center.z, "r": r + pad,
		"y0": center.y - half_h - pad, "y1": center.y + half_h + pad,
		"pad": pad,   # CameraKit: the pad ring is body-clearance AIR, not mesh
	})

func _iwall(center: Vector3, size: Vector3, col: Color, tex: String = "") -> MeshInstance3D:
	# an interior wall: visible box + solid collider + registered for camera cutaway fade.
	# tex (e.g. "castle") swaps the flat plaster for a real PBR stone material.
	var node := _l2_box(center, size, col)
	if tex == "castle":
		node.material_override = _castle_mat("wall", 0.065, col)
	elif tex != "":
		node.material_override = _up_mat(tex, 0.045, col)
	_wall_solid(center, size)
	var base_a: float = 1.0
	if node.material_override is StandardMaterial3D:
		base_a = (node.material_override as StandardMaterial3D).albedo_color.a
	fade_walls.append({"node": node, "c": center, "h": size * 0.5, "base_a": base_a, "a": base_a})
	return node

func _build_garden() -> void:
	_district_ref().build_groves()

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
		m.albedo_color = Color(0.66, 0.7, 0.76)
		m.normal_enabled = true
		m.normal_texture = load("res://assets/terrain/up_cliff_nrm.jpg")
		m.roughness_texture = load("res://assets/terrain/up_cliff_rgh.jpg")
		m.uv1_world_triplanar = true   # rocks are static; creature materials below stay object-space
		m.uv1_scale = Vector3(0.3, 0.3, 0.3)
	elif key.begins_with("SeaWeed"):
		# Legacy solid-mesh fallback stays matte; the illustrated alpha leaf is for cards.
		m.albedo_color = col * 1.2
		m.roughness = 0.95
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
		m.emission_energy_multiplier = 0.28
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
	# Legacy model packs were retired with the 2D migration. Unknown species
	# already have a null-safe fallback at the call site.
	model_cache["aq_" + model] = null
	return null

# MR2.0: pack name -> painted GEN2 prop. Every mapped piece spawns the
# family-style Meshy model (footprint-fit, cel+outline, settled); the pack
	# Missing converted art is handled by the null-safe caller fallback.
# 2nd audit (owner 2026-07-11): baked-in faces are CHARM, not flaws - the
# dealbreakers are invented characters (F9/F10), inconsistency, and concept
# enmeshment (F8). coral1 is the face coral Roshan chose herself; fanshell
# and spiralshell restored likewise. smallfanshell keeps its regen (F10).
# swimming creatures: statics brought alive by creature_sway.gdshader
# (tail-weighted body wave; facing measured equal to the pack: -Y, offset 0)
const CREATURE_GEN2 := {"ClownFish": "clownfish", "Turtle": "turtle", "Dolphin": "dolphin",
	"Shark": "shark", "Hammerhead": "hammerhead", "Whale": "whale", "StingRay": "stingray",
	"Squid": "squid", "Penguin": "penguin", "Octopus": "octopus", "Lobster": "lobster", "Crab": "crab"}
# per-species SWIM profile: [mode, speed, amount] for creature_sway.gdshader
# (0 tail-wave, 1 wing undulation, 2 jelly pulse, 3 waddle rock)
const CREATURE_SWAY := {"clownfish": [0, 4.2, 0.14], "dolphin": [0, 3.2, 0.11], "turtle": [0, 2.2, 0.08],
	"shark": [0, 3.6, 0.12], "hammerhead": [0, 3.4, 0.12], "whale": [1, 1.6, 0.08],
	"stingray": [1, 2.6, 0.15], "squid": [2, 2.8, 0.12], "octopus": [2, 2.2, 0.13],
	"jellyfish": [2, 1.8, 0.10], "shrimp": [3, 3.0, 0.04],
	"penguin": [3, 3.0, 0.03], "lobster": [3, 2.4, 0.06], "crab": [3, 2.6, 0.06],   # penguin: rigged clips carry the motion now
	"craft_kitty": [3, 2.0, 0.05], "craft_birdie": [3, 2.8, 0.07]}   # HER craft creatures: gentle waddle idle

# The three former 3/5 creatures keep their proven anatomy and animation, but
# receive stronger story-palette separation instead of another model lottery.
const CREATURE_REPAINT_3 := {
	"dolphin": [Color(0.30, 0.72, 0.86), Color(0.78, 0.94, 0.94)],
	"whale": [Color(0.48, 0.45, 0.72), Color(0.74, 0.90, 0.96)],
}

const AQ_GEN2 := {"Coral": "coral", "Coral1": "coral1", "Coral2": "coral2", "Coral3": "coral3", "Coral4": "coral4", "Coral5": "coral5", "Coral6": "coral6",
	"Rock": "rock", "Rock1": "rock1", "Rock2": "rock2", "Rock3": "rock3", "Rock4": "rock4", "Rock5": "rock5",
	"Rock6": "rock", "Rock7": "rock1", "Rock8": "rock2", "Rock9": "rock3", "Rock10": "rock4", "Rock11": "rock5",
	"FanShell": "fanshell", "SmallFanShell": "smallfanshell", "SpiralShell": "spiralshell", "SandDollar": "sanddollar", "StarFish": "starfish"}

func _place_aq(model: String, pos: Vector3, scl: float, play_anim: bool) -> Node3D:
	if AQ_GEN2.has(model):
		var sink: float = 0.25 if model.begins_with("Rock") else 0.1
		var gn := _gen2_prop(String(AQ_GEN2[model]), pos, scl * 2.2, randf() * TAU, sink)
		if gn != null:
			if not play_anim:
				flora_nodes.append(gn)
			return gn
	if CREATURE_GEN2.has(model):
		# NPCs too (play_anim=false, e.g. the slide penguin): the sway shader
		# gives statics their idle, so the old pack model is never needed
		var cw := _gen2_creature(String(CREATURE_GEN2[model]), pos, scl * 2.0)
		if cw != null:
			if not play_anim:
				flora_nodes.append(cw)
			return cw
		# Retired model resources deliberately have no runtime fallback. Keep
		# released shop friends visible with the existing layered card.
		var card := _make_creature_node("fish", AQ_COLORS.get(model, Color(0.4, 0.75, 0.7)),
			AQ_COLORS.get(model, Color(0.4, 0.75, 0.7)).lightened(0.2))
		if card != null:
			card.position = pos
			card.scale *= scl
			add_child(card)
			if not play_anim:
				flora_nodes.append(card)
			return card
	var ps := _aq(model)
	if ps == null:
		return null
	var inst: Node3D = ps.instantiate()
	inst.position = pos
	inst.scale = Vector3.ONE * scl
	inst.rotation.y = randf() * TAU
	_paint_aq(inst, _aq_mat(model))
	_toonify(inst)
	if model.begins_with("Rock"):
		# painted reef stone (fallback path) - bigger strokes, richer tint so
		# the cliff sheet reads instead of washing white (owner 2026-07-11)
		_toon_tile(inst, "cliff", 0.055, Color(0.82, 0.8, 0.95))
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

func _play_clip(node: Node3D, clip: String, speed: float = 1.0) -> void:
	# rigged GEN2 clip playback — a no-op for unrigged creatures, so callers
	# can request clips unconditionally. The AnimationPlayer is cached on the
	# node (the slide tick calls this every frame); clips loop + cross-blend.
	if node == null or not is_instance_valid(node):
		return
	if node.has_meta("no_clips"):
		return
	var ap: AnimationPlayer = node.get_meta("clip_ap") if node.has_meta("clip_ap") else null
	if ap == null:
		ap = _find_anim(node)
		if ap == null:
			node.set_meta("no_clips", true)
			return
		node.set_meta("clip_ap", ap)
	if not is_instance_valid(ap) or not ap.has_animation(clip):
		return
	if ap.current_animation != clip:
		ap.get_animation(clip).loop_mode = Animation.LOOP_LINEAR
		ap.play(clip, 0.25)
	ap.speed_scale = speed

func _build_aquatic_flora() -> void:
	_district_ref().build_flora()

func _build_aquatic_creatures() -> void:
	# hero animated creatures patrolling on circular paths. The turtles,
	# rays, dolphin and squid moved into the Pearl Shop's wall tanks
	# (ANIMAL_SHOP): they only join the reef once she buys them free, so
	# their patrol rows live there now and spawn via _spawn_shop_animals().
	var roster: Array[Dictionary] = [
		{"model": "Shark", "center": Vector2(35.0, 30.0), "rad": 62.0,
			"spd": 0.05, "y": 22.0, "size": 4.0, "kingdom": ReefDistricts.KINGDOM_CARIBBEAN},
		{"model": "Hammerhead", "center": Vector2(-40.0, -165.0), "rad": 48.0,
			"spd": 0.045, "y": 30.0, "size": 4.0, "kingdom": ReefDistricts.KINGDOM_CARIBBEAN},
		{"model": "Whale", "center": Vector2(140.0, -115.0), "rad": 42.0,
			"spd": 0.02, "y": 38.0, "size": 9.0, "kingdom": ReefDistricts.KINGDOM_NORWEGIAN},
	]
	for entry: Dictionary in roster:
		var model_name: String = String(entry["model"])
		var inst := _place_aq(model_name, Vector3.ZERO, float(entry["size"]), true)
		if inst == null:
			continue
		if model_name == "Whale":
			whale_node = inst
		var center: Vector2 = entry["center"]
		aquatic_movers.append({"node": inst, "rad": entry["rad"], "spd": entry["spd"], "y": entry["y"],
			"cx": center.x, "cz": center.y, "kingdom": entry["kingdom"],
			"ph": randf() * TAU, "clearance": float(entry["size"]) + 1.5})
	# bottom dwellers posed in the groves
	if cluster_centers.size() >= 4:
		var oc: Vector3 = cluster_centers[2]
		_place_aq("Octopus", Vector3(oc.x + 4.0, seabed_y(oc.x + 4.0, oc.z) + 0.4, oc.z), 2.2, true)
		var cc: Vector3 = cluster_centers[5]
		_place_aq("Crab", Vector3(cc.x, seabed_y(cc.x, cc.z) + 0.3, cc.z + 3.0), 2.0, true)
		var lc: Vector3 = cluster_centers[9]
		_place_aq("Lobster", Vector3(lc.x, seabed_y(lc.x, lc.z) + 0.3, lc.z - 3.0), 2.0, true)
	# small darting schools — babies of HER creatures (the old Dory/Carp/Tuna/Eel
	# pack fish were the last un-upgraded swimmers; playtest 2026-07-11).
	# Only the clownfish schools are free from the start: the turtle/ray/
	# squid babies arrive with their species when a tank friend is bought
	# (the "babies" count on ANIMAL_SHOP keeps the old totals intact).
	for s in range(3):
		var inst := _place_aq("ClownFish", Vector3.ZERO, 1.2 + randf() * 1.0, true)
		if inst == null:
			continue
		aquatic_movers.append({"node": inst, "rad": 40.0 + randf() * 150.0,
			"spd": 0.12 + randf() * 0.15, "y": 10.0 + randf() * 28.0,
			"ph": randf() * TAU, "clearance": 2.0})
	# player-crafted fish from the Crafting Studio (persist via save)
	_spawn_crafted_fish()
	# reef friends already bought free from the shop tanks (persist via save)
	_spawn_shop_animals()

func _spawn_crafted_fish() -> void:
	# spawn any custom_fish entries not yet in the water. Idempotent via the
	# counter: runs at world build, after _load_save() (the save loads AFTER
	# the reef builds, so spawning only at build time made every crafted fish
	# vanish on the next launch), and on each new craft.
	# Live spawns cap at the NEWEST 30 entries (skip ahead to the tail) so a
	# big collection cannot flood the reef with movers. The saved custom_fish
	# array itself is uncapped by design — her crafted fish data is sacred and
	# is never truncated or reordered here.
	crafted_fish_spawned = maxi(crafted_fish_spawned, custom_fish.size() - 30)
	while crafted_fish_spawned < custom_fish.size():
		var cf: Variant = custom_fish[crafted_fish_spawned]
		crafted_fish_spawned += 1
		if not (cf is Array) or (cf as Array).size() < 6:
			continue
		var cfn := _make_creature_node("fish", Color(cf[0], cf[1], cf[2]), Color(cf[3], cf[4], cf[5]), (cf as Array).size() > 6 and int(cf[6]) == 1, (cf as Array).size() > 7 and int(cf[7]) == 1)
		add_child(cfn)
		flora_nodes.append(cfn)
		aquatic_movers.append({"node": cfn, "rad": 30.0 + randf() * 130.0,
			"spd": 0.10 + randf() * 0.12, "y": 8.0 + randf() * 26.0,
			"ph": randf() * TAU, "crafted": true, "clearance": 2.0})

func _spawn_shop_animals() -> void:
	# put every OWNED tank species in the water: its old patrol rows plus its
	# school babies. Idempotent via animals_spawned, same shape as
	# _spawn_crafted_fish: runs at world build, after _load_save() (the save
	# loads AFTER the reef builds), and right when a tank friend is bought so
	# it is already swimming when she leaves the shop.
	for it in ANIMAL_SHOP:
		var sp := String(it["id"])
		if not bool(animals_owned.get(sp, false)) or bool(animals_spawned.get(sp, false)):
			continue
		animals_spawned[sp] = true
		for pat in (it["patrols"] as Array):
			var inst := _place_aq(String(it["model"]), Vector3.ZERO, float(pat[3]), true)
			if inst == null:
				continue
			var mover := {"node": inst, "rad": float(pat[0]), "spd": float(pat[1]),
				"y": float(pat[2]), "ph": randf() * TAU, "shop_pet": sp,
				"clearance": maxf(2.0, float(pat[3]) * 0.55)}
			if sp == "turtle":
				# the freed turtle keeps its tank skeleton: flippers stroke
				# out in the open reef too, so the purchase payoff is visible
				var rig := _rig_turtle(inst, 3.0)
				if not rig.is_empty():
					mover["rig"] = rig
					_set_sway(inst, 0.03)
			aquatic_movers.append(mover)
		for b in range(int(it["babies"])):
			var binst := _place_aq(String(it["model"]), Vector3.ZERO, 1.2 + randf() * 1.0, true)
			if binst == null:
				continue
			var bmover := {"node": binst, "rad": 40.0 + randf() * 150.0,
				"spd": 0.12 + randf() * 0.15, "y": 10.0 + randf() * 28.0,
				"ph": randf() * TAU, "shop_pet": sp, "clearance": 2.0}
			if sp == "turtle":
				var brig := _rig_turtle(binst, 3.6)
				if not brig.is_empty():
					bmover["rig"] = brig
					_set_sway(binst, 0.03)
			aquatic_movers.append(bmover)

var _turtle_rig_mesh: ArrayMesh = null   # cage-skinned turtle mesh, built once, shared
var _turtle_rig_skin: Skin = null

func _rig_turtle(pet: Node3D, speed: float) -> Dictionary:
	# THE TURTLE RIG: a real Skeleton3D over the (unrigged) Meshy turtle so
	# the flippers FLAP from the shoulder instead of shearing with the body
	# wave. Skin weights come from a MOTION CAGE - anatomical regions measured
	# from the turtle mesh's vertex slices (mesh space, +Z = head):
	#   head/neck tube  z > 0.42, |x| < 0.30
	#   front flippers  blades |x| 0.55..0.93, z -0.44..+0.30, shoulder ~0.48
	#   rear paddles    |x| 0.28..0.55, z -0.95..-0.55
	#   shell           everything else (rigid root)
	# Each vertex blends its limb bone with the shell root on a smoothstep
	# falloff through the cage boundary, so joints bend without cracks. The
	# skinned ArrayMesh + Skin are built once and shared by every instance;
	# only the (7-bone) skeleton is per-turtle.
	if pet == null or not is_instance_valid(pet):
		return {}
	var mi: MeshInstance3D = null
	for m2 in _all_meshes(pet):
		mi = m2
		break
	if mi == null or mi.mesh == null or mi.mesh.get_surface_count() != 1:
		return {}
	if _turtle_rig_mesh == null:
		var arrays: Array = mi.mesh.surface_get_arrays(0)
		var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
		var bones := PackedInt32Array()
		bones.resize(verts.size() * 4)
		var wts := PackedFloat32Array()
		wts.resize(verts.size() * 4)
		for i in range(verts.size()):
			var v: Vector3 = verts[i]
			var bi: int = i * 4
			var ax: float = absf(v.x)
			var limb: int = 0
			var w: float = 0.0
			if v.z > -0.50 and v.z < 0.34 and v.y < 0.22:
				w = smoothstep(0.45, 0.62, ax)          # through the shoulder
				limb = 3 if v.x > 0.0 else 4
			elif v.z <= -0.50 and v.y < 0.24:
				w = smoothstep(0.24, 0.36, ax) * smoothstep(0.50, 0.62, -v.z)
				limb = 5 if v.x > 0.0 else 6
			if w > 0.0:
				bones[bi] = limb
				wts[bi] = w
				bones[bi + 1] = 0
				wts[bi + 1] = 1.0 - w
			elif v.z > 0.36 and ax < 0.38:
				var wn: float = smoothstep(0.36, 0.52, v.z)  # into the neck
				var wh: float = smoothstep(0.55, 0.72, v.z)  # on to the head
				bones[bi] = 1
				wts[bi] = wn * (1.0 - wh)
				bones[bi + 1] = 2
				wts[bi + 1] = wn * wh
				bones[bi + 2] = 0
				wts[bi + 2] = 1.0 - wn
			else:
				bones[bi] = 0
				wts[bi] = 1.0
		arrays[Mesh.ARRAY_BONES] = bones
		arrays[Mesh.ARRAY_WEIGHTS] = wts
		var am := ArrayMesh.new()
		am.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
		_turtle_rig_mesh = am
	# bone rests: hinge points sit where each limb meets the body
	var origins: Array = [Vector3.ZERO, Vector3(0.0, -0.02, 0.40), Vector3(0.0, 0.0, 0.62),
		Vector3(0.48, -0.15, -0.05), Vector3(-0.48, -0.15, -0.05),
		Vector3(0.30, -0.12, -0.58), Vector3(-0.30, -0.12, -0.58)]
	var parents: Array = [-1, 0, 1, 0, 0, 0, 0]
	var skel := Skeleton3D.new()
	for bn in ["shell", "neck", "head", "fin_p", "fin_n", "rear_p", "rear_n"]:
		skel.add_bone(bn)
	for i in range(7):
		if int(parents[i]) >= 0:
			skel.set_bone_parent(i, int(parents[i]))
		var local: Vector3 = origins[i]
		if int(parents[i]) >= 0:
			local = (origins[i] as Vector3) - (origins[int(parents[i])] as Vector3)
		skel.set_bone_rest(i, Transform3D(Basis.IDENTITY, local))
	if _turtle_rig_skin == null:
		var sk := Skin.new()
		for i in range(7):
			sk.add_bind(i, Transform3D(Basis.IDENTITY, -(origins[i] as Vector3)))
		_turtle_rig_skin = sk
	# swap in the skinned mesh; the skeleton lives INSIDE the mesh instance so
	# skeleton space == mesh space no matter how the wrap is fitted/rotated
	var ov: Material = mi.get_surface_override_material(0)
	mi.mesh = _turtle_rig_mesh
	if ov != null:
		mi.set_surface_override_material(0, ov)
	mi.skin = _turtle_rig_skin
	mi.add_child(skel)
	mi.skeleton = mi.get_path_to(skel)
	skel.reset_bone_poses()
	return {"skel": skel, "ph": randf() * TAU, "speed": speed}

func _turtle_idle(rig: Dictionary, t: float) -> void:
	# the flap cycle: slow recovery lift, quick power pull (second harmonic
	# sharpens the downbeat), flippers feathering through the stroke like a
	# slow-motion wingbeat; rear paddles rudder on the half-beat; the neck
	# looks around on its own slower clock so she reads as curious, not
	# mechanical. Bones rotate in mesh space: +Z forward, fins along +/-X.
	var skel: Skeleton3D = rig.get("skel", null)
	if skel == null or not is_instance_valid(skel):
		return
	var ph: float = t * float(rig["speed"]) + float(rig["ph"])
	var flap: float = sin(ph) * 0.42 + sin(ph * 2.0 + 0.9) * 0.13
	var feather: float = sin(ph - 1.1) * 0.22
	skel.set_bone_pose_rotation(3, Quaternion(Vector3(0, 0, 1), flap) * Quaternion(Vector3(1, 0, 0), feather))
	skel.set_bone_pose_rotation(4, Quaternion(Vector3(0, 0, 1), -flap) * Quaternion(Vector3(1, 0, 0), -feather))
	skel.set_bone_pose_rotation(5, Quaternion(Vector3(1, 0, 0), sin(ph * 0.5 + 2.0) * 0.16))
	skel.set_bone_pose_rotation(6, Quaternion(Vector3(1, 0, 0), sin(ph * 0.5 + 2.6) * 0.16))
	var yaw: float = sin(t * 0.31 + float(rig["ph"])) * 0.30
	var pitch: float = sin(t * 0.21 + float(rig["ph"]) * 1.7) * 0.10
	skel.set_bone_pose_rotation(1, Quaternion(Vector3(0, 1, 0), yaw) * Quaternion(Vector3(1, 0, 0), pitch))
	skel.set_bone_pose_rotation(2, Quaternion(Vector3(0, 1, 0), yaw * 0.6) * Quaternion(Vector3(1, 0, 0), pitch * 0.7))
	skel.set_bone_pose_rotation(0, Quaternion(Vector3(1, 0, 0), sin(ph - 1.4) * 0.05))

func _set_sway(pet: Node3D, amount: float) -> void:
	# retune the sway shader on one instance (materials are per-surface
	# copies, so this never bleeds to other creatures). The rigged turtle
	# drops to near-zero so the skeleton owns the motion; the other tank
	# friends get a close-up boost so their idle reads through the glass.
	if pet == null or not is_instance_valid(pet):
		return
	for mi in _all_meshes(pet):
		if mi.mesh == null:
			continue
		for si in range(mi.mesh.get_surface_count()):
			var mat: Material = mi.get_surface_override_material(si)
			if mat is ShaderMaterial:
				(mat as ShaderMaterial).set_shader_parameter("sway_amount", amount)

func _aquatic_patrol_height(x: float, z: float, desired_y: float, clearance: float = 3.0) -> float:
	# Patrol circles cross terrain of very different heights. Keep each creature
	# above the local seabed while retaining a safe margin below the water surface.
	var ceiling: float = WATER_TOP - 3.0
	var floor: float = minf(seabed_y(x, z) + clearance, ceiling)
	return clampf(desired_y, floor, ceiling)


func _tick_aquatic(delta: float) -> void:
	# NOTE: this keeps running inside the cutaway arenas/lagoon/castle — the
	# reef creatures are never hidden there (the cutaways just sit hundreds of
	# units below at ARENA_POS/LEVEL2_POS), so their patrols stay live. Only
	# kart suspends the whole reef tick block upstream in _process.
	var t: float = Time.get_ticks_msec() / 1000.0
	var ceiling: float = WATER_TOP - 3.0
	var frame: int = Engine.get_process_frames()
	var idx: int = -1
	for mv in aquatic_movers:
		idx += 1
		var node: Node3D = mv["node"]
		var ang: float = t * float(mv["spd"]) + float(mv["ph"])
		var rad: float = float(mv["rad"])
		var px: float = float(mv.get("cx", 0.0)) + cos(ang) * rad
		var pz: float = float(mv.get("cz", 0.0)) + sin(ang) * rad
		var desired_y: float = float(mv["y"]) + sin(t * 0.3 + float(mv["ph"])) * 3.0
		# perf (Helio G88): seabed_y costs ~12 sin/sqrt per call — too hot for
		# every mover every frame. Cache each mover's clamp floor ("_cy") and
		# refresh it every 8th frame, staggered by loop index so the movers
		# don't all recompute on the same frame. Movement itself stays
		# per-frame smooth — only the terrain floor under the bob is cadenced.
		if not mv.has("_cy") or (frame + idx) % 8 == 0:
			mv["_cy"] = minf(seabed_y(px, pz) + float(mv.get("clearance", 3.0)), ceiling)
		var pos := Vector3(px, clampf(desired_y, float(mv["_cy"]), ceiling), pz)
		node.position = pos
		node.rotation.y = -ang + PI * 0.5
		if mv.has("rig"):
			_turtle_idle(mv["rig"], t)
		# a fish SHE made recognises her: heart puff + chirp when she swims by
		if bool(mv.get("crafted", false)) and game == "":
			mv["greet_cool"] = maxf(0.0, float(mv.get("greet_cool", 0.0)) - delta)
			if float(mv["greet_cool"]) <= 0.0 and node.position.distance_to(player.position) < 6.0:
				mv["greet_cool"] = 9.0
				_greet_heart(node.position + Vector3(0, 2.2, 0))
		elif game == "":
			# EVERY sea friend says hello now: excited wiggle + squash-bounce
			# + sparkle when Roshan swims close (free swim only, cooled down)
			mv["greet_cool"] = maxf(0.0, float(mv.get("greet_cool", 0.0)) - delta)
			if float(mv["greet_cool"]) <= 0.0 and node.position.distance_to(player.position) < 7.5:
				mv["greet_cool"] = 14.0
				_creature_greet(node)

func _tick_peng_pal(delta: float) -> void:
	# THE BABY PENGUIN PAL: once Roshan catches him on the big slide (the
	# "penguin" sticker), he becomes a little secondary character who tags
	# along behind her in the open reef — paddling hard when he falls behind,
	# waddle-bobbing at her side, and cheering with a giggle when she stops.
	if not bool(stickers.get("penguin", false)):
		return
	if peng_pal == null or not is_instance_valid(peng_pal):
		if game != "":
			return   # spawn him in the open water, never inside an arena
		var fwd0 := Vector3(sin(player.yaw), 0, cos(player.yaw))
		peng_pal = _gen2_creature("penguin", player.position - fwd0 * 5.0 + Vector3(1.5, 1.0, 0), 2.4)
		if peng_pal == null:
			return
		_sparkle_burst(peng_pal.position + Vector3(0, 1.5, 0), Color(0.7, 0.9, 1.0))
		if peng_giggle != null:
			peng_giggle.pitch_scale = 1.05
			peng_giggle.play()
		if not peng_pal_greeted:
			peng_pal_greeted = true
			show_msg("Baby Penguin", "Wait for meee! I'm coming too! Toot toot!")
	# hide him during minigames/castle so he never photobombs an arena
	peng_pal.visible = game == ""
	if game != "":
		return
	var t: float = Time.get_ticks_msec() / 1000.0
	var fwd := Vector3(sin(player.yaw), 0, cos(player.yaw))
	var want: Vector3 = player.position - fwd * 4.5 + Vector3(0, 0.8, 0)
	want += Vector3(sin(t * 0.7) * 0.8, sin(t * 1.1) * 0.5, cos(t * 0.9) * 0.8)   # lively drift
	var to_want: Vector3 = want - peng_pal.position
	var d: float = to_want.length()
	if d > 70.0:
		peng_pal.position = want   # she warped across the reef — pop him back to her side
	elif d > 0.05:
		# swims harder the further he lags, so he rubber-bands but never magnets
		var spd: float = clampf(d * 1.8, 2.5, 20.0)
		peng_pal.position += to_want.limit_length(spd * delta)
	# keep the little guy out of the sand
	peng_pal.position.y = maxf(peng_pal.position.y, seabed_y(peng_pal.position.x, peng_pal.position.z) + 1.4)
	# face where he's headed (gen2 face = local -X), or Roshan when idling
	var face: Vector3 = to_want if d > 1.6 else (player.position - peng_pal.position)
	if Vector2(face.x, face.z).length() > 0.3:
		peng_pal.rotation.y = lerp_angle(peng_pal.rotation.y, atan2(face.z, -face.x), 1.0 - pow(0.03, delta))
	peng_pal_cool -= delta
	peng_pal_cheer_t -= delta
	if peng_pal_cool <= 0.0 and d < 6.5 and player.vel.length() < 3.0:
		peng_pal_cool = 16.0
		peng_pal_cheer_t = 1.4
		_greet_heart(peng_pal.position + Vector3(0, 2.4, 0))
		if peng_giggle != null:
			peng_giggle.pitch_scale = 0.95 + randf() * 0.2
			peng_giggle.play()
	if peng_pal_cheer_t > 0.0:
		_play_clip(peng_pal, "cheer", 1.0)
	else:
		_play_clip(peng_pal, "sprint" if d > 9.0 else "waddle", 1.4 if d > 9.0 else 0.9)

func _build_pearls() -> void:
	pearl_mat = _rainbow_mat()
	for i in range(PEARL_TOTAL):
		# along the route between consecutive friends, light jitter
		var fi: int = i % FRIEND_DEFS.size()
		var fj: int = (fi + 1) % FRIEND_DEFS.size()
		var fpa: Vector2 = ReefDistricts.friend_position(fi)
		var fpb: Vector2 = ReefDistricts.friend_position(fj)
		var pa := Vector3(fpa.x, 0, fpa.y)
		var pb := Vector3(fpb.x, 0, fpb.y)
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
	if grew and msg_timer <= 4.0:
		# show_msg sets msg_timer = 5.0, so > 4.0 means another banner went up
		# less than a second ago (the _end_game win message) — never fight it;
		# the respawned pearls announce themselves by shimmering anyway
		show_msg("", "New rainbow pearls are shimmering in the ocean!")

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
		var fp: Vector2 = ReefDistricts.friend_position(i)
		var x: float = fp.x
		var z: float = fp.y
		# 3D migration (owner 2026-07-19): prefer a gen2 model when one has
		# landed for this character; the sprite cutout remains the fallback.
		var tex_name := String(fd["tex"])
		var cut := Sprite3D.new()
		cut.texture = _cutout_tex(tex_name)
		cut.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		cut.pixel_size = 0.016
		cut.position = Vector3(x, seabed_y(x, z) + 6.5, z)
		add_child(cut)
		var spr: Node3D = cut
		var bcols := [Color(1.0, 0.75, 0.35), Color(0.45, 0.9, 1.0), Color(1.0, 0.5, 0.75), Color(0.6, 1.0, 0.6), Color(0.8, 0.6, 1.0)]
		var bcol: Color = bcols[i % bcols.size()]
		var beacon := OmniLight3D.new()
		beacon.light_color = bcol
		beacon.light_energy = 0.7
		beacon.omni_range = 15.0
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
		pmat.albedo_color = Color(bcol.r, bcol.g, bcol.b, 0.09)
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
			omat.emission_energy_multiplier = 1.2
			orb.material_override = omat
			add_child(orb)
			sparks.append(orb)
		friends.append({"node": spr, "fname": fd["fname"], "tex": tex_name, "msg": fd["msg"], "game": fd["game"], "found": false, "won": false,
			"theme": fd.get("theme", "ice"), "mode": fd.get("mode", "fish"),
			"discover_radius": fd.get("discover_radius", 9.0), "linger_radius": fd.get("linger_radius", 10.0),
			"start_radius": fd.get("start_radius", 8.0),
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

func _kart_gateway(pos: Vector3, label: String, col: Color, show_ring: bool = true) -> void:
	# a clear, glowing race portal at a rainbow leg
	if show_ring:
		var ring := MeshInstance3D.new()
		var tm := TorusMesh.new()
		tm.inner_radius = 5.0; tm.outer_radius = 6.5; tm.rings = 24; tm.ring_segments = 12
		ring.mesh = tm
		var sh := Shader.new()
		sh.code = "shader_type spatial;\nrender_mode cull_disabled, unshaded;\nvoid fragment(){ float b=fract(UV.x*6.0); vec3 c; if(b<0.16)c=vec3(0.95,0.2,0.35);else if(b<0.33)c=vec3(1.0,0.6,0.2);else if(b<0.5)c=vec3(1.0,0.92,0.3);else if(b<0.66)c=vec3(0.3,0.85,0.45);else if(b<0.83)c=vec3(0.3,0.6,1.0);else c=vec3(0.65,0.4,0.95); ALBEDO=c; EMISSION=c*(0.6+0.4*sin(TIME*3.0)); }"
		var ring_mat := ShaderMaterial.new(); ring_mat.shader = sh
		ring.material_override = ring_mat
		ring.position = pos
		add_child(ring); game_nodes.append(ring)
		var tw := ring.create_tween().set_loops()
		tw.tween_property(ring, "rotation:y", TAU, 6.0).from(0.0)
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

func _start_kart_game(reversed: bool = false, ground: String = "terrain") -> void:
	_fade_cut(_start_kart_game_now.bind(reversed, ground))

func _capture_lagoon_trip_return() -> void:
	if game != "level2" or String(g.get("phase", "")) != "promenade":
		return
	var promenade: SkyLagoonPromenade = _lagoon_promenade_ref()
	lagoon_trip_return_master_x = promenade.master_route_x()
	# External games own their own stage and input. Release the lagoon Canvas
	# only after its canonical route coordinate has been captured.
	_prepare_touch_transition()
	promenade.teardown()

func _start_kart_game_now(reversed: bool = false, ground: String = "terrain") -> void:
	_capture_lagoon_trip_return()
	if hud_layer != null:
		hud_layer.visible = false   # the race draws its own HUD — no overlap
	kart_from = game
	kart_ground = ground
	kart_completion_committed = false
	if ground == "float":
		kart_float_portals_armed = false
	else:
		kart_ocean_portal_armed = false
	kart_prev_track = cur_track
	_play_music("race")
	game = "kart"
	hud_game.text = ""
	kart_game = KartGame.new()
	add_child(kart_game)
	if ground == "float":
		# Level-2 rainbow legs run the classic floating Rainbow Road version
		(kart_game as KartGame).configure({"theme": "rainbow", "ground": "float"})
	player.visible = false   # audit: the real mermaid mesh was left frozen in-frame
	(kart_game as KartGame).start(self, Callable(self, "_end_kart_game"), reversed)

func _kart_completion_committed(place: int) -> void:
	# KartGame calls this immediately after its pearl payout/save and before the
	# podium. Keep the teardown callback as a fallback for older/test controllers.
	if place <= 0 or kart_completion_committed:
		return
	kart_completion_committed = true
	_medal_ref().award_stats("kart", {"place": place})
	var unlocked_galaxy := false
	if kart_ground == "float" and not galaxy_unlocked:
		galaxy_unlocked = true
		unlocked_galaxy = true
	# Every completed race is a success for a preschooler. Set Galaxy first so
	# award_sticker's immediate save commits both rewards in the same snapshot.
	if not bool(stickers.get("racer", false)):
		award_sticker("racer")
	elif unlocked_galaxy:
		_write_save()

func _restore_kart_music() -> void:
	var restore_track := kart_prev_track
	if restore_track == "":
		restore_track = "level2" if kart_from == "level2" else "world"
	kart_prev_track = ""
	_play_music(restore_track)

func _end_kart_game(place: int) -> void:
	if place > 0:
		_kart_completion_committed(place)
	_restore_kart_music()
	player.visible = true
	if place < 0:
		# ✕ quit from the race HUD: no completion reward, podium, or galaxy. The mermaid
		# node never moves during a race, so restoring the pre-race mode
		# respawns her exactly where she swam into the portal. The source portal's
		# armed latch stays false until she deliberately leaves its trigger.
		kart_float_dest = "galaxy"   # a quit road leads nowhere new
		if hud_layer != null:
			hud_layer.visible = true
		kart_game = null
		kart_cool = 6.0
		var quit_world: String = kart_from
		var rebuild_lagoon: bool = quit_world == "level2" and lagoon_trip_return_master_x >= 0.0
		var saved_level2_open: bool = l2_open
		var saved_level2_pos = player.position
		game = quit_world
		kart_from = ""
		if rebuild_lagoon:
			game = ""
			call_deferred("_restore_level2_after_trip", saved_level2_open, saved_level2_pos)
			return
		_update_hud()
		return
	if hud_layer != null:
		hud_layer.visible = true
	kart_game = null
	kart_cool = 6.0
	var suf: String = ["st", "nd", "rd", "th", "th", "th", "th", "th"][clampi(place - 1, 0, 7)]
	if kart_ground == "float":
		# THE RAINBOW JUNCTION: the floating road doesn't end at the finish
		# line. Entered through a rainbow leg it soars UP into Roshan Galaxy;
		# entered through the dark ember gate it dives DOWN to the fortress.
		if kart_float_dest == "ember":
			kart_float_dest = "galaxy"
			show_msg("Rainbow Road", "The rainbow road dives DOWN and DOWN... to the EMBER FORTRESS!")
			call_deferred("_start_ember")
			return
		show_msg("Rainbow Road", "The rainbow road soars on and on... to ROSHAN GALAXY!")
		call_deferred("_start_galaxy")
		return
	var msg := "Ocean Race champion — 1st place!" if place == 1 else "Great racing — you came %d%s!" % [place, suf]
	show_msg("Ocean Race", msg)
	if kart_from == "level2":
		var saved_level2_open: bool = l2_open
		var saved_level2_pos = player.position
		kart_from = ""
		game = ""
		call_deferred("_restore_level2_after_trip", saved_level2_open, saved_level2_pos)
		return
	kart_from = ""
	game = ""
	_update_hud()

func _start_galaxy() -> void:
	_fade_cut(_start_galaxy_now)

func _start_galaxy_now() -> void:
	# A direct courtyard portal and the Rainbow Road both reach this function.
	# Remember the actual world underneath once, and keep it through the optional
	# fairy-flight detour so Butterfly World always returns symmetrically.
	if not galaxy_return_set:
		_capture_lagoon_trip_return()
		galaxy_from = kart_from if game == "kart" else game
		galaxy_return_pos = player.position
		galaxy_level2_open = l2_open
		galaxy_return_set = true
		if game == "kart":
			kart_from = ""
	if hud_layer != null:
		hud_layer.visible = false   # the galaxy draws its own HUD — no overlap
	if not galaxy_unlocked:
		galaxy_unlocked = true
		_write_save()
	game = "galaxy"
	_play_music("galaxy")
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
	var return_world: String = galaxy_from
	var return_level2_open: bool = galaxy_level2_open or level2_done_once
	var saved_return_pos: Vector3 = galaxy_return_pos
	galaxy_from = ""
	galaxy_return_set = false
	galaxy_return_pos = Vector3.ZERO
	galaxy_level2_open = false
	if return_world == "level2":
		call_deferred("_restore_level2_after_trip", return_level2_open, saved_return_pos)
		return
	kart_from = ""
	# Defensive ocean restoration for direct/debug entries. GalaxyLevel restores
	# its previous environment, but these assignments also repair an older hybrid
	# state left by a portal that forgot where it came from.
	player.position = saved_return_pos
	player.vel = Vector3.ZERO
	we_node.environment = world_env
	_play_music("world")

func _restore_level2_after_trip(was_open: bool, saved_position: Vector3) -> void:
	# _fade_cut invokes its rebuild callback synchronously, so the promenade and
	# its Canvas route controller exist again when _enter_level2 returns. Restore
	# the canonical master coordinate after that build; keep the spatial write as
	# compatibility for legacy callers and the generic hidden player node.
	var saved_master_x: float = lagoon_trip_return_master_x
	lagoon_trip_return_master_x = -1.0
	_enter_level2(was_open)
	player.position = saved_position
	player.vel = Vector3.ZERO
	if saved_master_x >= 0.0:
		_lagoon_promenade_ref().set_master_route_x(saved_master_x)
	bw_cool = maxf(bw_cool, 3.0)
	kart_cool = maxf(kart_cool, 3.0)

func _start_combat(battle_kind: String) -> void:
	if combat_game != null or battle_kind not in ["ice", "fire"]:
		return
	_prepare_touch_transition()
	combat_from = game
	combat_prev_track = cur_track
	_play_music("combat_" + battle_kind)
	game = "combat"
	_populate_touch_interactables()
	if hud_layer != null:
		hud_layer.visible = false
	player.visible = false
	if combat_from == "galaxy" and galaxy_game != null:
		var galaxy_level := galaxy_game as GalaxyLevel
		galaxy_level.visible = false
		galaxy_level.process_mode = Node.PROCESS_MODE_DISABLED
	combat_game = CombatArena.new()
	add_child(combat_game)
	combat_game.start(self, battle_kind, Callable(self, "_end_combat"))

func _end_combat(battle_kind: String) -> void:
	combat_game = null
	var completed: bool = battle_kind in ["ice", "fire"]
	if battle_kind == "ice":
		combat_ice_done = true
		pearl_count += 12
	elif battle_kind == "fire":
		combat_fire_done = true
		pearl_count += 20
	if completed:
		_write_save()
		_update_hud()
	game = combat_from
	_populate_touch_interactables()
	if combat_from == "galaxy" and galaxy_game != null:
		var galaxy_level := galaxy_game as GalaxyLevel
		galaxy_level.visible = true
		galaxy_level.process_mode = Node.PROCESS_MODE_INHERIT
		galaxy_level.resume_from_combat(completed)
	else:
		player.visible = true
		if player.cam != null:
			player.cam.make_current()
		if hud_layer != null:
			hud_layer.visible = true
		if game == "level2" and g.has("toilet"):
			var toilet_pos: Vector3 = (g["toilet"] as Dictionary)["pos"]
			player.position = toilet_pos + Vector3(5.5, 1.0, 0)
			player.vel = Vector3.ZERO
		player.snap_cam()   # resume the chase lens in place, no cross-world swoop
	_play_music(combat_prev_track if combat_prev_track != "" else "world")
	combat_prev_track = ""
	combat_from = ""

func _start_stuffie_battle() -> void:
	# the sparring-den ladder: one round per visit; once all three are won the
	# den keeps serving rounds in rotation (replayable, no dead end)
	if stuffie_game != null or companion_id == "":
		return
	# The battle swaps the mode with no fade, so stale focus/assisted travel
	# must not survive into (or past) it.
	_prepare_touch_transition()
	var ladder_index := 0
	for i in range(StuffieBattle.LADDER.size()):
		if not bool(stuffie_wins.get(String(StuffieBattle.LADDER[i]["tag"]), false)):
			ladder_index = i
			break
		ladder_index = (int(stuffie_wins.get("_replays", 0)) + i + 1) % StuffieBattle.LADDER.size()
	stuffie_from = game
	stuffie_prev_track = cur_track
	_play_music("stuffie_battle")
	game = "stuffie"
	if hud_layer != null:
		hud_layer.visible = false
	player.visible = false
	if companion_node != null and is_instance_valid(companion_node):
		companion_node.visible = false
	stuffie_game = StuffieBattle.new()
	add_child(stuffie_game)
	stuffie_game.start(self, ladder_index, Callable(self, "_end_stuffie_battle"))

func _end_stuffie_battle(round_tag: String) -> void:
	stuffie_game = null
	if round_tag != "":
		if bool(stuffie_wins.get(round_tag, false)):
			stuffie_wins["_replays"] = int(stuffie_wins.get("_replays", 0)) + 1
		stuffie_wins[round_tag] = true
		# CAPTURE (owner 2026-07-20): befriending a boss stuffie takes it HOME —
		# it moves onto its Stuffie Studio shelf and becomes a carryable companion
		for cfg in StuffieBattle.LADDER:
			if String(cfg["tag"]) != round_tag or not cfg.has("award"):
				continue
			var friend_key := "friend_" + String(cfg["award"])
			if not bool(stuffie_wins.get(friend_key, false)):
				stuffie_wins[friend_key] = true
				show_msg(String(cfg.get("award_name", "Your new friend")),
					"I'm coming HOME with you! Find me on my shelf in the castle's Stuffie Studio!", "win")
		pearl_count += 8
		_reward(false)
		_write_save()
		_update_hud()
	game = stuffie_from
	stuffie_from = ""
	_play_music(stuffie_prev_track if stuffie_prev_track != "" else "world")
	stuffie_prev_track = ""
	stuffie_cool = 12.0
	player.visible = true
	if player.cam != null:
		player.cam.make_current()
		player.snap_cam()   # resume the chase lens in place, no cross-world swoop
	if hud_layer != null:
		hud_layer.visible = true
	# Post-battle care is a patient hug + bath invitation. Boo-boos wait until
	# the child is ready; the reminder clock never removes or blocks the friend.
	_companion_ref().after_battle()

func _start_dungeon() -> void:
	_fade_cut(_start_dungeon_now)

func _start_dungeon_now() -> void:
	# The dungeon introduces its elemental actions in context. Requiring the two
	# optional overworld encounters here made a fresh save impossible to progress.
	if dungeon_game != null:
		return
	dungeon_prev_track = cur_track
	_play_music("dungeon_ice")
	game = "dungeon"
	if hud_layer != null:
		hud_layer.visible = false
	player.visible = false
	dungeon_game = DungeonLevel.new()
	add_child(dungeon_game)
	dungeon_game.start(self, dungeon_progress, Callable(self, "_end_dungeon"))

func _end_dungeon(completed: bool) -> void:
	dungeon_game = null
	game = "level2"
	player.visible = true
	if player.cam != null:
		player.cam.make_current()
	if hud_layer != null:
		hud_layer.visible = true
	if g.has("dungeon_gate"):
		var gate: Dictionary = g["dungeon_gate"]
		player.position = (gate["pos"] as Vector3) + Vector3(6.5, 0, 0)
		player.vel = Vector3.ZERO
		gate["armed"] = false
	player.snap_cam()   # resume the chase lens in place, no cross-world swoop
	_play_music(dungeon_prev_track if dungeon_prev_track != "" else "northern")
	dungeon_prev_track = ""
	show_msg("Roshan", "Ten-room dungeon complete!" if completed else "Checkpoint safe — come back whenever you want!", "win" if completed else "home")

func _ember_open() -> bool:
	# The Ember Fortress is a LATER world to discover: in normal play its dark
	# gateway only appears at the rainbow junction once the Butterfly World has
	# been saved (or after any visit). Dev-mode builds keep it always open.
	return ember_found or ember_done or bwd_done or dev_mode != null

func _start_ember() -> void:
	# Reached through the rainbow junction's dark gate (via the float race) —
	# same return-symmetry bookkeeping as the Butterfly World.
	if not ember_return_set:
		_capture_lagoon_trip_return()
		ember_from = kart_from if game == "kart" else game
		ember_return_pos = player.position
		ember_level2_open = l2_open
		ember_return_set = true
		if game == "kart":
			kart_from = ""
	if hud_layer != null:
		hud_layer.visible = false   # the fortress draws its own HUD — no overlap
	if not ember_found:
		ember_found = true
		_write_save()
	game = "ember"
	hud_game.text = ""
	player.visible = false   # the fortress has its own avatar
	_play_music("ember")
	ember_game = EmberFortressLevel.new()
	add_child(ember_game)
	(ember_game as EmberFortressLevel).start(self, Callable(self, "_end_ember"))

func _end_ember(_completed: bool) -> void:
	player.visible = true
	if hud_layer != null:
		hud_layer.visible = true
	ember_game = null
	game = ""
	if ember_done:
		show_msg("Ember King", "Come back and play in my fortress any time, little hero!", "win")
	else:
		show_msg("Ember Fortress", "Home again! The Ember King will keep his lanterns warm for you...")
	_update_hud()
	var return_world: String = ember_from
	var return_level2_open: bool = ember_level2_open or level2_done_once
	var saved_return_pos: Vector3 = ember_return_pos
	ember_from = ""
	ember_return_set = false
	ember_return_pos = Vector3.ZERO
	ember_level2_open = false
	if return_world == "level2":
		call_deferred("_restore_level2_after_trip", return_level2_open, saved_return_pos)
		return
	kart_from = ""
	# defensive ocean restoration, mirroring _end_galaxy's repair path
	player.position = saved_return_pos
	player.vel = Vector3.ZERO
	we_node.environment = world_env
	_play_music("world")

func _start_ember_dungeon() -> void:
	# The Great Gate inside the Ember Fortress. Same rule as the castle
	# dungeon: the rooms teach everything they need — no prerequisites beyond
	# the five lanterns that opened the gate.
	if dungeon_game != null or ember_game == null:
		return
	dungeon_prev_track = cur_track
	_play_music("dungeon_ember")
	game = "emberdun"
	var ember_level := ember_game as EmberFortressLevel
	ember_level.visible = false
	ember_level.process_mode = Node.PROCESS_MODE_DISABLED
	dungeon_game = DungeonLevel.new()
	add_child(dungeon_game)
	dungeon_game.start(self, ember_progress, Callable(self, "_end_ember_dungeon"),
		EmberFortressLevel.ROOMS, "ember_progress", "ember_done", EmberFortressLevel.FLAVOR)

func _end_ember_dungeon(completed: bool) -> void:
	dungeon_game = null
	game = "ember"
	_play_music(dungeon_prev_track if dungeon_prev_track != "" else "ember")
	dungeon_prev_track = ""
	if completed:
		award_sticker("volcano")
	if ember_game != null:
		var ember_level := ember_game as EmberFortressLevel
		ember_level.visible = true
		ember_level.process_mode = Node.PROCESS_MODE_INHERIT
		ember_level.resume_from_dungeon(completed)

func _start_opera() -> void:
	if not day_one_opera_enabled():
		show_msg("Daddy Mermaid",
			"The Opera House is resting. Today we clean the castle together!",
			"hint")
		return
	# The stage star opens the recovered three-floor Pearl Opera House venue.
	# CastleRooms25D historically suspends before calling this method, so undo
	# that cover immediately; otherwise the venue would open behind the room.
	if _castle_rooms_ref().is_open() and castle_room_id != "" \
			and (castle_room_layer == null or not castle_room_layer.visible):
		_castle_rooms_ref().resume(castle_room_id)
	if _castle_career_routes_ref().open_opera_venue():
		show_msg("Pearl Opera House",
			"The grand foyer is open! Ride a bubble lift and swim into a glowing show door!",
			"home")


func _start_opera_from_room(act_index: int, room_id: String) -> void:
	if not day_one_opera_enabled():
		opera_pending_act_index = -1
		opera_return_room = ""
		show_msg("Daddy Mermaid",
			"The castle jobs are locked until our cleaning adventure is done!",
			"hint")
		return
	if opera_game != null or opera_pending_act_index >= 0:
		return
	# The route owner is authoritative too: a matching tuple cannot be used as
	# a programmatic backdoor while another world, Castle room, or transition is
	# active. Clear all transient route state before rejecting it.
	var castle_rooms := _castle_rooms_ref()
	var castle_visible := castle_room_layer != null \
		and is_instance_valid(castle_room_layer) and castle_room_layer.visible
	var current_castle_route := game == "level2" \
		and String(g.get("phase", "")) == "hall" \
		and castle_rooms.is_open() and castle_visible \
		and castle_room_id == room_id
	if not current_castle_route \
			or not CastleCareerRoutes.route_matches(room_id, act_index):
		opera_pending_act_index = -1
		opera_return_room = ""
		return
	opera_pending_act_index = act_index
	opera_return_room = room_id
	castle_rooms.suspend()
	_fade_cut(_start_opera_now)

func _start_opera_now() -> void:
	if not day_one_opera_enabled():
		var blocked_return_room: String = opera_return_room
		opera_pending_act_index = -1
		opera_return_room = ""
		if blocked_return_room != "" and _castle_rooms_ref().is_open():
			_castle_rooms_ref().resume(blocked_return_room)
		return
	# Every career is launched from its one owner-approved Castle-room picture.
	# There is deliberately no no-argument picker or hidden all-career backdoor.
	var act_index := opera_pending_act_index
	var return_room := opera_return_room
	var castle_rooms := _castle_rooms_ref()
	var route_still_owned := game == "level2" \
		and String(g.get("phase", "")) == "hall" \
		and castle_rooms.is_open() and castle_room_id == return_room \
		and CastleCareerRoutes.route_matches(return_room, act_index)
	if opera_game != null or not route_still_owned:
		opera_pending_act_index = -1
		opera_return_room = ""
		if return_room != "" and castle_rooms.is_open():
			castle_rooms.resume(return_room)
		return
	opera_pending_act_index = -1
	game = "opera"
	if hud_layer != null:
		opera_hud_was_visible = hud_layer.visible
		opera_hud_previous_layer = hud_layer.layer
		opera_hud_game_was_visible = hud_game != null and hud_game.visible
		opera_obj_was_visible = obj_card != null and obj_card.visible
		hud_layer.layer = 12
		hud_layer.visible = true
		if hud_game != null:
			hud_game.visible = false
		if obj_card != null:
			obj_card.visible = false
	if hud_msg != null:
		hud_msg.text = ""
		hud_msg.visible = false
	opera_player_was_visible = player != null and player.visible
	if player != null:
		player.visible = false
	_sync_pause_surface_layer()
	var next_house := OperaHouse.new()
	add_child(next_house)
	if not next_house.start(
			self, act_index, Callable(self, "_end_opera")):
		next_house.queue_free()
		opera_active_act_index = -1
		opera_return_room = ""
		_restore_opera_route_state(return_room)
		show_msg("Roshan",
			"That career picture is resting. We are safely back in the room!",
			"hint")
		return
	opera_active_act_index = act_index
	opera_game = next_house

func _end_opera(completed: bool) -> void:
	opera_game = null
	var return_room := opera_return_room
	var finished_act := opera_active_act_index
	opera_active_act_index = -1
	opera_return_room = ""
	_restore_opera_route_state(return_room)
	var career_name := "career"
	if OperaHouse.is_live_act_index(finished_act):
		career_name = String((OperaHouse.ACTS[finished_act] as Dictionary).get(
			"career", "career"))
	show_msg(
		"Roshan",
		("%s star saved! Back to our room!" % career_name)
			if completed else "Back to the room - every career star is safe!",
		"win" if completed else "home")


func _restore_opera_route_state(return_room: String) -> void:
	game = "level2"
	if player != null:
		player.visible = opera_player_was_visible
		if player.cam != null:
			player.cam.make_current()
	if hud_layer != null:
		hud_layer.layer = opera_hud_previous_layer
		hud_layer.visible = opera_hud_was_visible
		if hud_game != null:
			hud_game.visible = opera_hud_game_was_visible
		if obj_card != null:
			obj_card.visible = opera_obj_was_visible
	if player != null:
		player.snap_cam()   # resume the chase lens in place, no cross-world swoop
	if String(g.get("phase", "")) == "hall" and return_room != "":
		_castle_rooms_ref().resume(return_room)
		_castle_career_routes_ref().sync()
	_sync_pause_surface_layer()

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

func _cel_replace(root: Node, outline: ShaderMaterial, shader_path: String = "res://assets/shaders/cel.gdshader") -> void:
	var ph := randf() * TAU
	for mi in _all_meshes(root):
		var mesh: Mesh = mi.mesh
		if mesh == null:
			continue
		for si in range(mesh.get_surface_count()):
			var m: Material = mi.get_active_material(si)
			if m is BaseMaterial3D:
				var bm := m as BaseMaterial3D
				var cm := ShaderMaterial.new()
				cm.shader = load(shader_path)
				if bm.albedo_texture != null:
					cm.set_shader_parameter("albedo_tex", bm.albedo_texture)
				cm.set_shader_parameter("tint", bm.albedo_color)
				if shader_path.contains("coral_flow"):
					cm.set_shader_parameter("phase", ph)
					# height-normalize the flow gate: roots still, crowns sway
					var bb: AABB = mesh.get_aabb()
					cm.set_shader_parameter("aabb_y0", bb.position.y)
					cm.set_shader_parameter("aabb_h", bb.size.y)
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

func _all_meshes(root: Node) -> Array[MeshInstance3D]:
	var out: Array[MeshInstance3D] = []
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
	# Spawn ownership belongs to world topology, not the controller. This keeps
	# old headless/ocean flows byte-for-position compatible and lets display
	# builds immediately move to the castle gatehouse after save restoration.
	player.position = Vector3(0.0, 26.0, 0.0)
	player.vel = Vector3.ZERO
	player.snap_cam()

func _build_hud() -> void:
	var cl := CanvasLayer.new()
	cl.layer = SKY_LAGOON_HUD_CANVAS_LAYER
	add_child(cl)
	hud_layer = cl
	var status_panel := Panel.new()
	status_panel.name = "HudStatusTray"
	status_panel.position = Vector2(16, 14)
	status_panel.size = Vector2(280, 146)
	status_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	status_panel.add_theme_stylebox_override("panel", StorybookUI.panel_style(StorybookUI.LAVENDER, Color(0.93, 0.97, 1.0, 0.94), 44, 4))
	# The July 23 owner declutter removed persistent scorekeeping from free roam.
	# Keep these nodes as hidden compatibility surfaces for probes/save refreshes.
	status_panel.visible = false
	cl.add_child(status_panel)
	hud_pearls = _mk_label(cl, Vector2(42, 24), 30)
	hud_pearls.size = Vector2(220, 42)
	hud_pearls.visible = false
	hud_stars = _mk_label(cl, Vector2(42, 65), 22)
	hud_stars.visible = false
	# three lines (stars / crowns+critters / medal tally) inside the 146-tall tray
	hud_stars.size = Vector2(230, 112)
	hud_game = _mk_label(cl, Vector2(430, 20), 23)
	hud_game.name = "HudPictureObjective"
	hud_game.size = Vector2(420, 112)
	hud_game.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hud_game.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	hud_game.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	hud_game.add_theme_stylebox_override("normal", StorybookUI.panel_style(StorybookUI.GOLD, Color(0.94, 0.97, 1.0, 0.94), 30, 4))
	hud_game.set_meta("picture_objective", true)
	hud_game.visible = false
	hud_msg = _mk_label(cl, Vector2(230, 590), 24)
	hud_msg.name = "HudVoiceCaption"
	hud_msg.size = Vector2(820, 112)
	hud_msg.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hud_msg.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	hud_msg.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	hud_msg.add_theme_stylebox_override("normal", StorybookUI.panel_style(StorybookUI.LAVENDER, Color(0.91, 0.94, 1.0, 0.94), 30, 4))
	hud_msg.text = ""
	_build_obj_card(cl)
	_update_hud()

func _build_obj_card(cl: CanvasLayer) -> void:
	# Picture-first objective card: a big pictogram of WHO/what to find plus the
	# sparkle-current echo. Reading it is never required — narration and the
	# in-world helping current carry the same information.
	obj_card = StorybookUI.add_hud_panel(cl, Rect2(528, 12, 224, 150), StorybookUI.MINT, Color(0.93, 0.98, 1.0, 0.96), 30)
	obj_card.name = "HudPictureTargetCard"
	obj_card.visible = false
	obj_icon = TextureRect.new()
	obj_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	obj_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	obj_icon.position = Vector2(62, 6)
	obj_icon.size = Vector2(100, 104)
	obj_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	obj_card.add_child(obj_icon)
	obj_icon_lbl = Label.new()
	StorybookUI.style_hud_label(obj_icon_lbl, 72)
	obj_icon_lbl.position = Vector2(0, 2)
	obj_icon_lbl.size = Vector2(224, 108)
	obj_icon_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	obj_icon_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	obj_icon_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	obj_card.add_child(obj_icon_lbl)
	var hint := Label.new()
	hint.text = "✨ ✨ ✨"
	StorybookUI.style_hud_label(hint, 24, StorybookUI.GOLD, 3)
	hint.position = Vector2(0, 112)
	hint.size = Vector2(224, 34)
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	obj_card.add_child(hint)

func _set_objective(key: String, tex: Texture2D, emoji: String) -> void:
	if obj_card == null:
		return
	if key == "":
		obj_card.visible = false
		obj_key = ""
		return
	if key == obj_key:
		# Teach a changed picture briefly, then return the scenery to the child.
		obj_seen_t += get_process_delta_time()
		if obj_seen_t > 3.5:
			obj_card.visible = false
		return
	obj_key = key
	obj_seen_t = 0.0
	obj_card.visible = true
	obj_card.modulate.a = 1.0
	obj_icon.texture = tex
	obj_icon.visible = tex != null
	obj_icon_lbl.text = emoji
	obj_icon_lbl.visible = tex == null
	# one pulse when the target changes, then settle (handoff card contract)
	obj_card.pivot_offset = obj_card.size * 0.5
	var tw := create_tween()
	tw.tween_property(obj_card, "scale", Vector2(1.12, 1.12), 0.18)
	tw.tween_property(obj_card, "scale", Vector2.ONE, 0.22)

func _build_fade_cover() -> void:
	# layer 30: above the HUD, pause menu and touch UI — a plain black cover
	# that hides the single-frame stall of every heavy world rebuild (_fade_cut)
	var cl := CanvasLayer.new()
	cl.layer = 30
	add_child(cl)
	fade_rect = ColorRect.new()
	fade_rect.color = Color.BLACK
	fade_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	fade_rect.modulate.a = 0.0
	cl.add_child(fade_rect)
	fade_rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

func _fade_cut(cb: Callable) -> void:
	# Visual cover for a synchronous heavy world rebuild. PROBE SAFETY: the
	# rebuild must happen in THIS call chain — probes call these entry points
	# and assert state a frame or two later, so cb is never tween-deferred.
	# Snap the cover to full black, run the build under it in the same frame,
	# then tween only the reveal. State timing is byte-identical to before.
	_prepare_touch_transition()
	if fade_rect == null:
		cb.call()
		_finish_touch_transition()
		return
	fade_rect.mouse_filter = Control.MOUSE_FILTER_STOP
	fade_rect.modulate.a = 1.0
	cb.call()
	_populate_touch_interactables()
	if fade_tween != null and fade_tween.is_valid():
		fade_tween.kill()
	fade_tween = create_tween()
	fade_tween.tween_property(fade_rect, "modulate:a", 0.0, 0.25)
	fade_tween.tween_callback(_finish_touch_transition)

func _mk_label(cl: CanvasLayer, pos: Vector2, fsize: int) -> Label:
	var l := Label.new()
	l.position = pos
	StorybookUI.style_label(l, fsize, StorybookUI.INK, 3)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cl.add_child(l)
	return l

# Non-reader progress pips: filled thematic emoji up to `filled`, then "·"
# placeholders up to `total` — a 4yo can compare lengths, not numerals.
func _pips(filled: int, total: int, emoji: String) -> String:
	var f := clampi(filled, 0, total)
	return emoji.repeat(f) + "·".repeat(total - f)

func _update_hud() -> void:
	hud_pearls.text = "◉  %d" % pearl_count
	var stars := 0
	for f in friends:
		if f["found"]:
			stars += 1
	var critters := 0
	for caught_value: Variant in critter_collection.values():
		if bool(caught_value):
			critters += 1
	# critters stay numeric on purpose: 18 pips would wrap the HUD line
	hud_stars.text = "★  %s\n♛  %s    ◇  %d / 18" % [_pips(stars, 5, "●"), _pips(trophies, 5, "●"), critters] + _medal_ref().hud_suffix()

# speaker key -> default pitch tint (so even the fallback clip differs per character)
const VOICE_PITCH := {"roshan": 1.18, "huluu": 1.05, "evie": 1.28, "harper": 1.12, "faron": 1.0, "daddy": 0.9, "wacky": 0.7, "chuck": 1.0, "shop": 0.85, "sparkle": 1.35, "mewsha": 1.3, "rosalina": 1.15, "rumi": 1.24, "everyone": 1.1}

var speech_layer: CanvasLayer
var speech_portrait: TextureRect
var speech_t := 0.0
const SPEAKER_PORTRAIT := {
	"roshan": "res://assets/characters/roshan_25d/roshan_base.png",
	"huluu": "res://assets/characters/friends/huluu.png",
	"evie": "res://assets/minigames/seek/evie_portrait.png",
	"harper": "res://assets/characters/friends/two_friends.png",
	"faron": "res://assets/characters/friends/mama_baby.png",
	"daddy": "res://assets/characters/friends/daddy.webp",
	"wacky": "res://assets/characters/friends/wacky_chuck.png",
	"chuck": "res://assets/characters/friends/wacky_chuck.png",
	"shop": "res://assets/characters/roshan_25d/roshan_base.png",
	"sparkle": "res://assets/book/baby_eagle.png",
	"rosalina": "res://assets/characters/skins/fairy_mermaid.png",
	"everyone": "res://assets/characters/roshan_25d/roshan_base.png"}

func _flash_speaker_icon(who: String) -> void:
	if speech_layer == null:
		speech_layer = CanvasLayer.new()
		speech_layer.layer = 8
		add_child(speech_layer)
		var panel := StorybookUI.add_hud_panel(speech_layer, Rect2(24, 228, 190, 208), StorybookUI.GOLD, Color(0.94, 0.97, 1.0, 0.94), 30)
		panel.name = "HudSpeakerPortraitCard"
		# Codex UI handoff: between the status tray (ends y188-224) and the
		# resting joystick corner (starts y~440) — portraits never enter
		# touch corner zones
		speech_portrait = TextureRect.new()
		speech_portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		speech_portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
		speech_portrait.position = Vector2(34, 236)
		speech_portrait.size = Vector2(170, 192)
		speech_layer.add_child(speech_portrait)
	var key := _speaker_key(who)
	var path := String(SPEAKER_PORTRAIT.get(key, SPEAKER_PORTRAIT["roshan"]))
	if ResourceLoader.exists(path):
		speech_portrait.texture = load(path)
	speech_layer.visible = true
	speech_t = 4.0

# Phase 7.5: the audio pipeline lives in scripts/audio_director.gd
# (state stays here; AudioDirector receives main by reference)
var _audio_dir: AudioDirector = null

# Phase 7 satellite: spoken-spell recognition (scripts/mic_input.gd). Built on
# first use so a launch that never enters combat never touches the audio input.
var mic_sys: MicInput = null

func _mic_ref() -> MicInput:
	if mic_sys == null:
		mic_sys = MicInput.new(self)
	return mic_sys

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

func say_sequence(lines: Array, opening_hold: float = 0.0) -> void:
	_audio_ref().say_sequence(lines, opening_hold)

func skip_dialogue() -> bool:
	return _audio_ref().skip_dialogue()

func clear_dialogue() -> void:
	_audio_ref().clear_dialogue()

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

func _play_music(track: String, loop: bool = true) -> void:
	_audio_ref()._play_music(track, loop)

func _apply_quality(q: String) -> void:
	quality = q
	var speedy: bool = q == "speedy"
	if sun_light != null:
		sun_light.shadow_enabled = not speedy
	if world_env != null:
		world_env.glow_bloom = 0.12 if speedy else 0.4
		world_env.glow_intensity = _world_glow_target()
	# keep the ACTIVE cutaway environment (lagoon / castle / arena) in step too —
	# restore its remembered full-quality bloom or clamp it, live
	if arena_env != null and we_node != null and we_node.environment == arena_env and arena_env.has_meta("ww_full"):
		var fv: Vector2 = arena_env.get_meta("ww_full")
		arena_env.glow_intensity = minf(fv.x, 0.75) if speedy else fv.x
		arena_env.glow_bloom = minf(fv.y, 0.12) if speedy else fv.y
		_refresh_scene_grade(arena_env)
	_sync_castle_lights()
	if player != null and "trail_enabled" in player:
		player.trail_enabled = not speedy   # the wake ribbon is the only per-frame CPU mesh rebuild
	streak_ctx = "none"   # force the streak pool to re-apply visibility for the new quality
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
		quality_btn.text = "≋   SPEEDY" if speedy else "✦   SPARKLY"
		quality_btn.set_meta("toggle_on", not speedy)
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
var carry_sys: CarrySystem = null

func _carry_ref() -> CarrySystem:
	if carry_sys == null:
		carry_sys = CarrySystem.new(self)
	return carry_sys

var flow_sys: ReefFlow = null

func _flow_ref() -> ReefFlow:
	if flow_sys == null:
		flow_sys = ReefFlow.new(self)
	return flow_sys

var grotto_sys: GrottoPuzzle = null

func _grotto_ref() -> GrottoPuzzle:
	if grotto_sys == null:
		grotto_sys = GrottoPuzzle.new(self)
	return grotto_sys

var _save_state: SaveState = null
var _collection_system: CollectionSystem = null

func _collection_ref() -> CollectionSystem:
	if _collection_system == null:
		_collection_system = CollectionSystemLogic.new(self)
	return _collection_system

# ---- the stuffed-friend companion wing lives in scripts/companion.gd
# ---- (state stays here; CompanionSystem receives main by reference)
var _companion_system: CompanionSystem = null

func _companion_ref() -> CompanionSystem:
	if _companion_system == null:
		_companion_system = CompanionSystem.new(self)
	return _companion_system

# bronze/silver/gold rankings live in scripts/medal_system.gd
# (state stays here on m.medals; MedalSystem receives main by reference)
var _medal_system: MedalSystem = null

func _medal_ref() -> MedalSystem:
	if _medal_system == null:
		_medal_system = MedalSystem.new(self)
	return _medal_system

func _load_save() -> void:
	if _save_state == null:
		_save_state = SaveState.new(self)
	_save_state.load_save()

func _write_save() -> bool:
	if _save_state == null:
		_save_state = SaveState.new(self)
	var saved: bool = _save_state.write_save()
	# every immediate write also satisfies any debounced request — milestone
	# sites (_end_game etc.) are natural flush points, never double writes
	save_pending = false
	save_pending_t = 0.0
	save_dirty = not saved
	save_retry_t = 1.5 if save_dirty else 0.0
	return saved

func _start_new_game() -> bool:
	if _save_state == null:
		_save_state = SaveState.new(self)
	return _save_state.start_new_game()

func _launch_from_start_menu(start_day_one: bool) -> void:
	# The launch choice owns the Day 1 boundary. Continue is deliberately a
	# direct game entry, even when an older save predates the Day 1 fields;
	# New Game keeps the fresh-save defaults and fires the authored arrival.
	_prepare_start_menu_launch(start_day_one)
	if START_AT_CASTLE_GATE:
		_enter_level2_now(false, false, true)

func _prepare_start_menu_launch(start_day_one: bool) -> void:
	first_session = false
	# Initialize the director before selecting the mode: its constructor
	# normalizes default Day 1 state and must not overwrite a Continue choice.
	var director: DayOneDirector = _day_one_ref()
	director.day_one_active = start_day_one
	if not start_day_one:
		_day_one_clear_castle_dressing()

func _queue_save() -> void:
	# debounce for the per-frame hot sites (pearl pickup, friend discovery):
	# one write ~1.5s after the last event instead of a synchronous multi-file
	# write per pearl. Milestones keep calling _write_save() directly.
	save_pending = true
	save_pending_t = 1.5


func _melody_input_context_lost() -> bool:
	return not _melody_input_context_losses.is_empty()


func _melody_input_context_blocks_input() -> bool:
	if _melody_input_context_lost():
		return true
	if game != "melody":
		return false
	return (_game_obj("melody", MelodyGame) as MelodyGame).input_context_blocks_input()


func _lose_melody_input_context(reason: StringName) -> void:
	if reason.is_empty() or _melody_input_context_losses.has(reason):
		return
	# Clear once on the active -> lost boundary. Further nested loss reasons must
	# not mutate the census at all; lost-context input is blocked at its writers.
	if _melody_input_context_losses.is_empty():
		_melody_held_sources.clear()
	_melody_input_context_losses[reason] = true
	if game == "melody":
		(_game_obj("melody", MelodyGame) as MelodyGame).on_input_context_lost(
			reason)


func _restore_melody_input_context(reason: StringName) -> void:
	if reason.is_empty() or not _melody_input_context_losses.has(reason):
		return
	_melody_input_context_losses.erase(reason)
	if game == "melody":
		(_game_obj("melody", MelodyGame) as MelodyGame).on_input_context_restored(
			reason)
	if _melody_input_context_losses.is_empty():
		# A platform may deliver stale terminal events around the restoration edge.
		# Re-establish the empty census before the first active post-restore tick.
		_melody_held_sources.clear()


func _slide_canvas_fish_route_active() -> bool:
	# Route scope is deliberately exact. Penguin Slide remains the legacy chase,
	# and game="race" remains the shared 3D play-place course.
	return game == "slide" and String(g.get("mode", "")) == "fish"


func _slide_canvas_return_guard_active() -> bool:
	return _slide_canvas_return_guard_armed


func _slide_canvas_return_fade_is_clear() -> bool:
	return fade_rect == null or (fade_rect.modulate.a <= 0.02 \
		and fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE)


func _slide_canvas_return_guard_snapshot() -> Dictionary:
	return {
		"active": _slide_canvas_return_guard_armed,
		"fade_clear": _slide_canvas_return_fade_is_clear(),
		"neutral_frames": _slide_canvas_return_neutral_frames,
		"held_sources": _slide_canvas_return_held_sources.size(),
		"context_lost": _slide_canvas_input_context_lost(),
		"physical_neutral": _slide_canvas_return_sources_neutral(),
		"control_blocked": touch_control_blocks.has("slide_canvas_return"),
		"retire_pending": _slide_canvas_return_retire_pending,
	}


func _slide_canvas_return_physical_event(ev: InputEvent) -> bool:
	return ev is InputEventScreenTouch or ev is InputEventScreenDrag \
		or ev is InputEventMouseButton or ev is InputEventMouseMotion \
		or ev is InputEventKey or ev is InputEventJoypadButton \
		or ev is InputEventJoypadMotion or ev is InputEventAction


func _slide_canvas_return_source_token(ev: InputEvent) -> StringName:
	# This deliberately has a broader vocabulary than the live slide source
	# router. Never feed these tokens to arm_entry_sources(): the Canvas runtime
	# owns only left/right steering and cannot retire A/B, vertical or look axes.
	if ev is InputEventScreenTouch:
		var touch := ev as InputEventScreenTouch
		return StringName("return:touch:%d:%d" % [touch.device, touch.index])
	if ev is InputEventScreenDrag:
		var drag := ev as InputEventScreenDrag
		return StringName("return:touch:%d:%d" % [drag.device, drag.index])
	if ev is InputEventMouseButton:
		var mouse_button := ev as InputEventMouseButton
		if mouse_button.device != InputEvent.DEVICE_ID_EMULATION \
				and mouse_button.button_index in [MOUSE_BUTTON_LEFT,
				MOUSE_BUTTON_RIGHT]:
			return StringName("return:mouse:%d:%d" % [mouse_button.device,
				mouse_button.button_index])
	if ev is InputEventMouseMotion:
		var mouse_motion := ev as InputEventMouseMotion
		if mouse_motion.device != InputEvent.DEVICE_ID_EMULATION:
			if (mouse_motion.button_mask & MOUSE_BUTTON_MASK_LEFT) != 0:
				return StringName("return:mouse:%d:%d" % [mouse_motion.device,
					MOUSE_BUTTON_LEFT])
			if (mouse_motion.button_mask & MOUSE_BUTTON_MASK_RIGHT) != 0:
				return StringName("return:mouse:%d:%d" % [mouse_motion.device,
					MOUSE_BUTTON_RIGHT])
	if ev is InputEventKey:
		var key := ev as InputEventKey
		var key_code: int = int(key.physical_keycode)
		if key_code == 0:
			key_code = int(key.keycode)
		if key_code in SLIDE_CANVAS_RETURN_KEYS:
			return StringName("return:key:%d:%d" % [key.device, key_code])
	if ev is InputEventJoypadButton:
		var button := ev as InputEventJoypadButton
		if button.button_index in SLIDE_CANVAS_RETURN_PAD_BUTTONS:
			return StringName("return:pad:%d:button:%d" % [button.device,
				button.button_index])
	if ev is InputEventJoypadMotion:
		var motion := ev as InputEventJoypadMotion
		if motion.axis in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y,
				JOY_AXIS_RIGHT_X, JOY_AXIS_RIGHT_Y]:
			return StringName("return:pad:%d:axis:%d" % [motion.device,
				motion.axis])
	return &""


func _observe_slide_canvas_return_source(ev: InputEvent) -> void:
	# During a context loss there is no trustworthy terminal stream. The loss
	# hook clears this census; post-restore physical polling establishes the new
	# baseline without reviving delayed events as owners.
	if _slide_canvas_input_context_lost():
		return
	var source_token: StringName = _slide_canvas_return_source_token(ev)
	if not source_token.is_empty():
		var pressed := false
		var released := false
		if ev is InputEventScreenTouch:
			pressed = (ev as InputEventScreenTouch).pressed
			released = not pressed
		elif ev is InputEventScreenDrag or ev is InputEventMouseMotion:
			pressed = true
		elif ev is InputEventMouseButton:
			pressed = (ev as InputEventMouseButton).pressed
			released = not pressed
		elif ev is InputEventKey:
			var key := ev as InputEventKey
			pressed = key.pressed and not key.echo
			released = not key.pressed
		elif ev is InputEventJoypadButton:
			pressed = (ev as InputEventJoypadButton).pressed
			released = not pressed
		elif ev is InputEventJoypadMotion:
			pressed = absf((ev as InputEventJoypadMotion).axis_value) > 0.18
			released = not pressed
		if pressed:
			_slide_canvas_return_held_sources[source_token] = true
		elif released:
			_slide_canvas_return_held_sources.erase(source_token)
	if _slide_canvas_return_guard_armed:
		# Guard traffic returns before the ordinary Melody census tracker. Retire
		# only the exact terminal token here so a source held through the fish
		# stage cannot poison a later Melody entry; never route or cancel a live
		# Melody controller from this post-Canvas boundary.
		if _melody_source_release(ev):
			var melody_source: StringName = _melody_source_token(ev)
			if not melody_source.is_empty():
				_melody_held_sources.erase(melody_source)
		var live_source: StringName = _slide_canvas_source_token(ev)
		if not live_source.is_empty():
			if _slide_canvas_source_press(ev):
				_slide_canvas_held_sources[live_source] = true
			elif _slide_canvas_source_release(ev):
				_slide_canvas_held_sources.erase(live_source)
		# Main consumes guard traffic before the ordinary raw fallback recorder.
		# Mirror only pad levels here so an unmapped controller cannot disappear
		# from the neutral oracle while its physical source remains held.
		_record_slide_canvas_poll_level(ev)
		_slide_canvas_return_neutral_frames = 0
		_slide_canvas_return_retire_pending = false


func _arm_slide_canvas_return_guard() -> void:
	_slide_canvas_return_guard_armed = true
	_slide_canvas_return_neutral_frames = 0
	_slide_canvas_return_fade_clear = false
	_slide_canvas_return_retire_pending = false
	# The live router's touch/mouse-left/steering census is intentionally left
	# intact. The return oracle checks it separately from this broader census.
	_set_world_controls_enabled(false, "slide_canvas_return")
	if player != null:
		player.vel *= 0.0


func _slide_canvas_return_sources_neutral() -> bool:
	if not _slide_canvas_return_held_sources.is_empty() \
			or not _slide_canvas_held_sources.is_empty():
		return false
	for key_code: Key in SLIDE_CANVAS_RETURN_KEYS:
		if Input.is_physical_key_pressed(key_code):
			return false
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) \
			or Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
		return false
	for button: JoyButton in SLIDE_CANVAS_RETURN_PAD_BUTTONS:
		if joy_pressed(button):
			return false
	for axis: JoyAxis in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y,
			JOY_AXIS_RIGHT_X, JOY_AXIS_RIGHT_Y]:
		if absf(joy_axis(axis)) > 0.18:
			return false
	if touch_ui != null:
		if (touch_ui.stick_vec as Vector2).length() > 0.05 \
				or bool(touch_ui.action_down) or bool(touch_ui.action_just) \
				or not (touch_ui.touch_owners as Dictionary).is_empty() \
				or bool(touch_ui.drag_active):
			return false
	return true


func _finish_slide_canvas_return_guard() -> void:
	# Retirement is deferred until every Node has finished this process frame, so
	# Player cannot observe a cleared guard on the second neutral quarantine frame.
	# A terminal event or context loss may arrive after scheduling; fail closed and
	# require two new trustworthy polls instead of honoring a stale callback.
	if not _slide_canvas_return_retire_pending:
		return
	if not _slide_canvas_return_guard_armed \
			or _slide_canvas_input_context_lost() \
			or not _slide_canvas_return_fade_is_clear() \
			or not _slide_canvas_return_sources_neutral() \
			or _slide_canvas_return_neutral_frames < 2:
		_slide_canvas_return_retire_pending = false
		_slide_canvas_return_neutral_frames = 0
		return
	_slide_canvas_return_retire_pending = false
	_slide_canvas_return_guard_armed = false
	_slide_canvas_return_neutral_frames = 0
	_slide_canvas_return_fade_clear = true
	_slide_canvas_return_held_sources.clear()
	_slide_canvas_held_sources.clear()
	joy_ev_axis.clear()
	joy_ev_btn.clear()
	_pad_prev_a = false
	_pad_prev_b = false
	_pc_prev_a = false
	pad_cursor_active = false
	if pad_cursor_layer != null:
		pad_cursor_layer.visible = false
	if touch_ui != null:
		touch_ui.cancel_all_touches()
		touch_ui.consume_action()
	if player != null:
		player.vel *= 0.0
	_set_world_controls_enabled(true, "slide_canvas_return")


func _tick_slide_canvas_return_guard() -> void:
	if not _slide_canvas_return_guard_armed:
		return
	if player != null:
		player.vel *= 0.0
	_slide_canvas_return_fade_clear = _slide_canvas_return_fade_is_clear()
	if _slide_canvas_input_context_lost() or not _slide_canvas_return_fade_clear \
			or not _slide_canvas_return_sources_neutral():
		_slide_canvas_return_neutral_frames = 0
		_slide_canvas_return_retire_pending = false
		return
	if _slide_canvas_return_retire_pending:
		return
	# Two trustworthy focused process polls cover delayed mapped-state republish.
	_slide_canvas_return_neutral_frames += 1
	if _slide_canvas_return_neutral_frames >= 2:
		_slide_canvas_return_retire_pending = true
		call_deferred("_finish_slide_canvas_return_guard")


func active_viewport_camera() -> Camera3D:
	# One typed public boundary keeps Canvas probes and lifecycle code honest
	# without duplicating the renderer's lowercase spatial API throughout probes.
	return get_viewport().get_camera_3d()


func _slide_canvas_input_context_lost() -> bool:
	return not _slide_canvas_input_context_losses.is_empty()


func _slide_canvas_poll_restore_waiting() -> bool:
	return _slide_canvas_fish_route_active() \
		and _slide_canvas_overlay_axis_wait_neutral


func _record_slide_canvas_poll_level(ev: InputEvent) -> void:
	# TouchUI can run while Main is SceneTree-paused and can reach this same
	# narrow seam first. Replaying a level is idempotent and never routes gameplay.
	if ev is InputEventJoypadMotion:
		var motion := ev as InputEventJoypadMotion
		joy_ev_axis[int(motion.axis)] = motion.axis_value \
			if absf(motion.axis_value) > 0.18 else 0.0
	elif ev is InputEventJoypadButton:
		var button := ev as InputEventJoypadButton
		joy_ev_btn[int(button.button_index)] = button.pressed


func _slide_canvas_input_context_blocks_input() -> bool:
	if _slide_canvas_input_context_lost():
		return true
	if not _slide_canvas_fish_route_active():
		return false
	return (_game_obj("race", SlideRaceGame) as SlideRaceGame).input_context_blocks_input()


func _lose_slide_canvas_input_context(reason: StringName) -> void:
	if reason.is_empty() or _slide_canvas_input_context_losses.has(reason):
		return
	# Focus-out and app-paused can arrive in either order. Clear the process-wide
	# census once on the first loss, then leave it untouched until every reason is
	# restored; missing releases are not valid input owners after that boundary.
	if _slide_canvas_input_context_losses.is_empty():
		_slide_canvas_held_sources.clear()
		_slide_canvas_return_held_sources.clear()
	_slide_canvas_input_context_losses[reason] = true
	_slide_canvas_return_neutral_frames = 0
	_slide_canvas_return_retire_pending = false
	if _slide_canvas_fish_route_active() or _slide_canvas_return_guard_active():
		# A polled stick has no terminal event while the app is absent. Forget raw
		# fallback levels and require mapped axes to return neutral before the
		# overlay star cursor can wake again after restoration.
		joy_ev_axis.clear()
		joy_ev_btn.clear()
	if _slide_canvas_fish_route_active():
		_slide_canvas_overlay_axis_wait_neutral = true
		_slide_canvas_overlay_poll_neutral_frames = 0
		(_game_obj("race", SlideRaceGame) as SlideRaceGame).on_input_context_lost(
			reason)


func _restore_slide_canvas_input_context(reason: StringName) -> void:
	if reason.is_empty() or not _slide_canvas_input_context_losses.has(reason):
		return
	_slide_canvas_input_context_losses.erase(reason)
	if _slide_canvas_return_guard_active():
		_slide_canvas_return_neutral_frames = 0
	if _slide_canvas_fish_route_active():
		(_game_obj("race", SlideRaceGame) as SlideRaceGame).on_input_context_restored(
			reason)
	if _slide_canvas_input_context_losses.is_empty():
		# The runtime retains a source-free one-tick guard. Keep the entry census
		# empty across the same restoration edge so delayed releases cannot seed it.
		_slide_canvas_held_sources.clear()


func _notification(what: int) -> void:
	match what:
		NOTIFICATION_APPLICATION_FOCUS_OUT:
			_lose_melody_input_context(MELODY_CONTEXT_FOCUS)
			_lose_slide_canvas_input_context(SLIDE_CANVAS_CONTEXT_FOCUS)
		NOTIFICATION_APPLICATION_PAUSED:
			_lose_melody_input_context(MELODY_CONTEXT_APPLICATION)
			_lose_slide_canvas_input_context(SLIDE_CANVAS_CONTEXT_APPLICATION)
		NOTIFICATION_APPLICATION_RESUMED:
			_restore_melody_input_context(MELODY_CONTEXT_APPLICATION)
			_restore_slide_canvas_input_context(SLIDE_CANVAS_CONTEXT_APPLICATION)
		NOTIFICATION_APPLICATION_FOCUS_IN:
			_restore_melody_input_context(MELODY_CONTEXT_FOCUS)
			_restore_slide_canvas_input_context(SLIDE_CANVAS_CONTEXT_FOCUS)
		NOTIFICATION_WM_CLOSE_REQUEST:
			_lose_melody_input_context(MELODY_CONTEXT_CLOSE)
			_lose_slide_canvas_input_context(SLIDE_CANVAS_CONTEXT_CLOSE)
	if what == NOTIFICATION_APPLICATION_PAUSED or what == NOTIFICATION_WM_CLOSE_REQUEST:
		# flush BOTH a failed write awaiting retry and a debounced pending
		# write — going to the background must never drop queued progress
		if save_dirty or save_pending:
			_write_save()

func _add_won_star(fr: Dictionary) -> void:
	if fr.has("star"):
		return
	var st := Label3D.new()
	st.text = "\u2605"
	st.font_size = 240
	st.modulate = Color(1.0, 0.85, 0.2)
	st.outline_size = 24
	st.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	st.position = (fr["node"] as Node3D).position + Vector3(0, 7.5, 0)
	add_child(st)
	fr["star"] = st

# the pause menu overlay lives in scripts/pause_menu.gd
# (state stays here; PauseMenu receives main by reference)
var _pause_menu: PauseMenu = null

func _pause_ref() -> PauseMenu:
	if _pause_menu == null:
		_pause_menu = PauseMenu.new(self)
	return _pause_menu

func _build_pause() -> void:
	_pause_ref()._build_pause()

func toggle_pause() -> void:
	if touch_ui != null:
		touch_ui.cancel_all_touches()
	_pause_ref().toggle_pause()


func _sync_pause_surface_layer() -> void:
	# The shipped Castle owns opaque CanvasLayer 14. Keep the phone's pause
	# affordance above its layer-15 ambient accents. During Opera it sits above
	# the layer-10 career, layer-11 ambient accents and layer-12 caption HUD.
	# An opened pause sheet still owns layer 29 beneath the layer-30 fade.
	if pause_layer == null or get_tree().paused:
		return
	var castle_front := castle_room_layer != null \
		and is_instance_valid(castle_room_layer) and castle_room_layer.visible
	if castle_front:
		pause_layer.layer = 16
	elif game == "opera":
		pause_layer.layer = 13
	else:
		pause_layer.layer = 12

# ===================== REVERSIBLE TOUCH-CENTRIC EXPERIMENT =====================

func _init_touch_experiment() -> void:
	# Trusted legacy probes exercise the preserved Classic contract while the
	# dedicated touch probes exercise Hybrid. These test-only flags never write
	# the preference and are not used by Android/desktop game launches.
	var user_args: PackedStringArray = OS.get_cmdline_user_args()
	if "--classic-touch-test" in user_args:
		_set_touch_mode(TOUCH_MODE_CLASSIC, false)
	elif "--hybrid-touch-test" in user_args:
		_set_touch_mode(TOUCH_MODE_HYBRID, false)
	if touch_ui != null:
		touch_ui.set_mode(touch_mode)
		if not touch_ui.world_touched.is_connected(_on_touch_world):
			touch_ui.world_touched.connect(_on_touch_world)
		if not touch_ui.manual_move_started.is_connected(_on_touch_manual_move):
			touch_ui.manual_move_started.connect(_on_touch_manual_move)
		touch_ui.world_press_probe = Callable(self, "_on_world_press")
		touch_ui.world_press_release = Callable(self, "_on_world_press_release")
		touch_ui.world_press_drag = Callable(self, "_on_world_press_drag")
		touch_ui.world_drag_end = Callable(self, "_on_world_drag_end")
		touch_ui.world_press_cancel = Callable(self, "_on_world_press_cancel")
	_interaction_ref()
	_populate_touch_interactables()

func _interaction_ref() -> InteractionDirector:
	if _interaction_director == null:
		_interaction_director = InteractionDirectorLogic.new(self)
	return _interaction_director

func _tap_move_ref() -> TapMoveDirector:
	if _tap_move_director == null:
		_tap_move_director = TapMoveDirectorLogic.new(self)
	return _tap_move_director

func touch_uses_explicit_interactions() -> bool:
	return touch_mode == TOUCH_MODE_HYBRID and touch_ui != null and touch_ui.wants_touch()

func _set_touch_mode(next_mode: String, persist: bool = true) -> void:
	touch_mode = TOUCH_MODE_CLASSIC if next_mode == TOUCH_MODE_CLASSIC else TOUCH_MODE_HYBRID
	touch_auto_active = false
	touch_focus_id = ""
	touch_focus_ready = false
	if touch_discovery_ring != null:
		touch_discovery_ring.visible = false
	if touch_focus_ring != null:
		touch_focus_ring.visible = false
	if touch_ui != null:
		touch_ui.set_mode(touch_mode)
	if touch_mode_btn != null:
		touch_mode_btn.text = _touch_mode_label()
	if persist:
		_write_save()

func _touch_mode_label() -> String:
	return "🖐\nHybrid Touch" if touch_mode == TOUCH_MODE_HYBRID else "↔\nClassic Touch"

# The world-tap gates shared by the release path and the press-fire probe:
# a tap may reach the stage only when no overlay or mode owns the screen.
func _world_tap_gated() -> bool:
	if intro_active or get_tree().paused or mg_kind != "":
		return true
	if fade_rect != null and fade_rect.modulate.a > 0.02:
		return true
	if touch_ui != null and not touch_ui.world_controls_enabled:
		return true
	if wardrobe_layer != null or craft_layer != null \
			or castle_logo_layer != null or collection_layer != null:
		return true
	return false

func _melody_input_gated() -> bool:
	# Melody deliberately disables the legacy swim controls while its opaque
	# Canvas is open, so its own input gate mirrors the shared overlay/fade rules
	# without treating that one intentional control block as an input failure.
	if intro_active or get_tree().paused or mg_kind != "":
		return true
	if fade_rect != null and fade_rect.modulate.a > 0.02:
		return true
	return false

func _melody_overlay_owns_input() -> bool:
	# Full-screen books/studios sit above Melody's layer and retain their normal
	# GUI input.  Melody still receives a neutral cancellation/release so the
	# note underneath can never score while an overlay is open.
	return game == "melody" and (wardrobe_layer != null or craft_layer != null \
		or castle_logo_layer != null or stickers_layer != null \
		or collection_layer != null or companion_layer != null \
		or companion_care_layer != null or mic_teach_layer != null)

func _melody_source_token(ev: InputEvent) -> StringName:
	if ev is InputEventScreenTouch:
		var touch := ev as InputEventScreenTouch
		return StringName("touch:%d:%d" % [touch.device, touch.index])
	if ev is InputEventScreenDrag:
		var drag := ev as InputEventScreenDrag
		return StringName("touch:%d:%d" % [drag.device, drag.index])
	if ev is InputEventMouseButton:
		var mouse_button := ev as InputEventMouseButton
		if mouse_button.device != InputEvent.DEVICE_ID_EMULATION \
				and mouse_button.button_index == MOUSE_BUTTON_LEFT:
			return StringName("mouse:%d:left" % mouse_button.device)
	if ev is InputEventMouseMotion:
		var mouse_motion := ev as InputEventMouseMotion
		if mouse_motion.device != InputEvent.DEVICE_ID_EMULATION \
				and (mouse_motion.button_mask & MOUSE_BUTTON_MASK_LEFT) != 0:
			return StringName("mouse:%d:left" % mouse_motion.device)
	if ev is InputEventKey:
		var key := ev as InputEventKey
		if key.physical_keycode in [KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
			return StringName("key:%d:%d" % [key.device, key.physical_keycode])
	if ev is InputEventJoypadButton:
		var button := ev as InputEventJoypadButton
		if button.button_index in [JOY_BUTTON_A, JOY_BUTTON_B,
				JOY_BUTTON_X, JOY_BUTTON_Y]:
			return StringName("pad:%d:%d" % [button.device, button.button_index])
	return &""

func _melody_source_press(ev: InputEvent) -> bool:
	if ev is InputEventScreenTouch:
		return (ev as InputEventScreenTouch).pressed
	if ev is InputEventMouseButton:
		return (ev as InputEventMouseButton).pressed
	if ev is InputEventKey:
		var key := ev as InputEventKey
		return key.pressed and not key.echo
	if ev is InputEventJoypadButton:
		return (ev as InputEventJoypadButton).pressed
	return false

func _melody_source_release(ev: InputEvent) -> bool:
	if ev is InputEventScreenTouch:
		return not (ev as InputEventScreenTouch).pressed
	if ev is InputEventMouseButton:
		return not (ev as InputEventMouseButton).pressed
	if ev is InputEventKey:
		return not (ev as InputEventKey).pressed
	if ev is InputEventJoypadButton:
		return not (ev as InputEventJoypadButton).pressed
	return false

func _track_melody_source_state(ev: InputEvent) -> void:
	if _melody_input_context_blocks_input():
		return
	var source_token := _melody_source_token(ev)
	if source_token.is_empty():
		return
	if _melody_source_press(ev):
		_melody_held_sources[source_token] = true
	elif _melody_source_release(ev):
		_melody_held_sources.erase(source_token)


func _retire_paused_melody_release(ev: InputEvent) -> void:
	# Main itself is pausable, so TouchUI's always-processing relay calls this
	# for recognized terminal events. Retire the process-wide entry census in
	# every activity. Only a live Melody stage also needs its cancel-before-exact-
	# release contract; neither path claims the event from the visible Pause GUI.
	if _melody_input_context_lost() \
			or not _melody_source_release(ev) \
			or _melody_source_token(ev).is_empty():
		return
	_track_melody_source_state(ev)
	if game == "melody":
		_release_melody_source_event(ev,
			_game_obj("melody", MelodyGame) as MelodyGame)


func _retire_touch_ui_consumed_entry_release(ev: InputEvent) -> void:
	# Hybrid stick/action releases are consumed by TouchUI's early _input path.
	# Main sees the matching press before TouchUI claims the control in
	# _unhandled_input, so retire both process-wide pre-entry censuses here before
	# TouchUI marks the terminal handled. Opaque games disable world controls and
	# therefore never reach this seam; their live controller routing is unchanged.
	if _melody_source_release(ev):
		var melody_source: StringName = _melody_source_token(ev)
		if not melody_source.is_empty():
			_melody_held_sources.erase(melody_source)
	if _slide_canvas_source_release(ev):
		var slide_source: StringName = _slide_canvas_source_token(ev)
		if not slide_source.is_empty():
			_slide_canvas_held_sources.erase(slide_source)


func _forget_melody_pad_device(device: int) -> void:
	if _melody_input_context_blocks_input():
		return
	var source_prefix := "pad:%d:" % device
	for source_value: Variant in _melody_held_sources.keys():
		var source_token := StringName(String(source_value))
		if String(source_token).begins_with(source_prefix):
			_melody_held_sources.erase(source_token)
	if game == "melody":
		var melody: MelodyGame = _game_obj("melody", MelodyGame) as MelodyGame
		melody.forget_sources_with_prefix(source_prefix)

func _release_melody_source_event(ev: InputEvent,
		melody: MelodyGame) -> bool:
	if not _melody_source_release(ev):
		return false
	var source_token := _melody_source_token(ev)
	if source_token.is_empty():
		return false
	# An overlay/fade may have appeared between press and release. Transfer any
	# armed press into the neutral blocked set before forwarding the exact lift,
	# otherwise that release could score behind the new owner.
	melody.cancel_input()
	if String(source_token).begins_with("touch:") \
			or String(source_token).begins_with("mouse:"):
		melody.handle_touch_release(source_token)
	else:
		melody.handle_action_release(source_token)
	return true

func _release_melody_input_under_overlay(ev: InputEvent,
		melody: MelodyGame) -> void:
	if _release_melody_source_event(ev, melody):
		return
	var source_token := _melody_source_token(ev)
	if _melody_source_press(ev) and not source_token.is_empty():
		melody.cancel_input(source_token)
	else:
		melody.cancel_input()

func _melody_pause_zone_hit(screen_pos: Vector2) -> bool:
	if touch_ui == null or not touch_ui.has_method("pause_zone"):
		return false
	var pause_rect: Rect2 = touch_ui.call("pause_zone") as Rect2
	return pause_rect.has_point(screen_pos)

func _route_melody_input(ev: InputEvent) -> bool:
	# Melody is an opaque Canvas activity. Read its pointer before the legacy
	# touch router can reinterpret Classic touches as swimming or reserve parts
	# of the painted stage as a virtual stick/action bay. The pause corner stays
	# owned by TouchUI, which cancels this controller before raising the sheet.
	if game != "melody":
		return false
	if _melody_input_context_blocks_input():
		return false
	var melody: MelodyGame = _game_obj("melody", MelodyGame) as MelodyGame
	if get_tree().paused:
		# The Pause sheet still owns and receives its controls, but an original
		# note source may lift while the tree is paused. Forward only exact neutral
		# releases so that source cannot leave the activity permanently latched.
		# Main._input is itself paused, so TouchUI normally reaches the narrow helper
		# directly. Keep this branch for any other always-processing caller.
		_retire_paused_melody_release(ev)
		return false
	if _melody_overlay_owns_input():
		# Do not mark this event handled: the visible higher-layer GUI owns it.
		# Releases still clear Melody's neutral latch without ever scoring.
		_release_melody_input_under_overlay(ev, melody)
		return false
	if ev is InputEventScreenTouch:
		var touch := ev as InputEventScreenTouch
		var touch_source := _melody_source_token(touch)
		# A release is always neutral-safe, including during a fade.  Cancelling
		# both halves used to leave the fresh-input latch armed forever after a
		# quick tap wholly inside the entry transition.
		if not touch.pressed:
			if _melody_input_gated():
				melody.cancel_input()
				melody.handle_touch_release(touch_source)
			elif touch.canceled:
				melody.handle_touch_cancel(touch_source)
			else:
				melody.handle_touch_release(touch_source)
			return true
		if touch.pressed and _melody_pause_zone_hit(touch.position):
			return false
		if _melody_input_gated():
			melody.cancel_input(touch_source)
			return true
		melody.handle_touch_press(touch.position, touch_source)
		return true
	if ev is InputEventScreenDrag:
		var drag := ev as InputEventScreenDrag
		var drag_source := _melody_source_token(drag)
		if _melody_input_gated():
			melody.cancel_input()
			return true
		melody.handle_touch_drag(drag.position, drag_source)
		return true
	if ev is InputEventMouseButton:
		var mouse_button := ev as InputEventMouseButton
		if mouse_button.device == InputEvent.DEVICE_ID_EMULATION \
				or mouse_button.button_index != MOUSE_BUTTON_LEFT:
			return false
		var mouse_source := _melody_source_token(mouse_button)
		if not mouse_button.pressed:
			if _melody_input_gated():
				melody.cancel_input()
				melody.handle_touch_release(mouse_source)
			elif mouse_button.canceled:
				melody.handle_touch_cancel(mouse_source)
			else:
				melody.handle_touch_release(mouse_source)
			return true
		if mouse_button.pressed and _melody_pause_zone_hit(mouse_button.position):
			return false
		if _melody_input_gated():
			melody.cancel_input(mouse_source)
			return true
		melody.handle_touch_press(mouse_button.position, mouse_source)
		return true
	if ev is InputEventMouseMotion:
		var mouse_motion := ev as InputEventMouseMotion
		if mouse_motion.device == InputEvent.DEVICE_ID_EMULATION \
				or (mouse_motion.button_mask & MOUSE_BUTTON_MASK_LEFT) == 0:
			return false
		var mouse_drag_source := _melody_source_token(mouse_motion)
		if _melody_input_gated():
			melody.cancel_input()
			return true
		melody.handle_touch_drag(mouse_motion.position, mouse_drag_source)
		return true
	if ev is InputEventKey:
		var key := ev as InputEventKey
		if key.physical_keycode not in [KEY_SPACE, KEY_ENTER, KEY_KP_ENTER]:
			return false
		var key_source := _melody_source_token(key)
		if _melody_input_gated():
			if key.pressed:
				if not key.echo:
					melody.cancel_input(key_source)
			else:
				melody.cancel_input()
				melody.handle_action_release(key_source)
			return true
		if key.pressed:
			if not key.echo:
				melody.handle_action_press(key_source)
		else:
			melody.handle_action_release(key_source)
		return true
	if ev is InputEventJoypadButton:
		var button := ev as InputEventJoypadButton
		if button.button_index not in [JOY_BUTTON_A, JOY_BUTTON_B, JOY_BUTTON_X, JOY_BUTTON_Y]:
			return false
		var pad_source := _melody_source_token(button)
		if _melody_input_gated():
			if button.pressed:
				melody.cancel_input(pad_source)
			else:
				melody.cancel_input()
				melody.handle_action_release(pad_source)
			return true
		if button.pressed:
			melody.handle_action_press(pad_source)
		else:
			melody.handle_action_release(pad_source)
		return true
	return false


func _slide_canvas_input_gated() -> bool:
	# The fish Canvas intentionally disables the legacy swim controls. Its own
	# route therefore mirrors shared overlay/fade gates without interpreting the
	# dedicated slide_canvas control block as a gameplay failure.
	if intro_active or get_tree().paused or mg_kind != "":
		return true
	if fade_rect != null and (fade_rect.modulate.a > 0.02 \
			or fade_rect.mouse_filter != Control.MOUSE_FILTER_IGNORE):
		return true
	return false


func _slide_canvas_overlay_owns_input() -> bool:
	return _slide_canvas_fish_route_active() and (wardrobe_layer != null \
		or craft_layer != null or castle_logo_layer != null \
		or stickers_layer != null or collection_layer != null \
		or companion_layer != null or companion_care_layer != null \
		or mic_teach_layer != null \
		or (dev_mode != null and bool(dev_mode.get("open"))))


func _slide_canvas_source_token(ev: InputEvent) -> StringName:
	if ev is InputEventScreenTouch:
		var touch := ev as InputEventScreenTouch
		return StringName("touch:%d:%d" % [touch.device, touch.index])
	if ev is InputEventScreenDrag:
		var drag := ev as InputEventScreenDrag
		return StringName("touch:%d:%d" % [drag.device, drag.index])
	if ev is InputEventMouseButton:
		var mouse_button := ev as InputEventMouseButton
		if mouse_button.device != InputEvent.DEVICE_ID_EMULATION \
				and mouse_button.button_index == MOUSE_BUTTON_LEFT:
			return StringName("mouse:%d:left" % mouse_button.device)
	if ev is InputEventMouseMotion:
		var mouse_motion := ev as InputEventMouseMotion
		if mouse_motion.device != InputEvent.DEVICE_ID_EMULATION \
				and (mouse_motion.button_mask & MOUSE_BUTTON_MASK_LEFT) != 0:
			return StringName("mouse:%d:left" % mouse_motion.device)
	if ev is InputEventKey:
		var key := ev as InputEventKey
		var key_code: int = int(key.physical_keycode)
		if key_code == 0:
			key_code = int(key.keycode)
		if key_code in [KEY_LEFT, KEY_A, KEY_RIGHT, KEY_D]:
			return StringName("key:%d:%d" % [key.device, key_code])
	if ev is InputEventJoypadButton:
		var button := ev as InputEventJoypadButton
		if button.button_index in [JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT]:
			return StringName("pad:%d:%d" % [button.device, button.button_index])
	if ev is InputEventJoypadMotion:
		var motion := ev as InputEventJoypadMotion
		if motion.axis == JOY_AXIS_LEFT_X:
			return StringName("pad:%d:axis:%d" % [motion.device, motion.axis])
	return &""


func _slide_canvas_source_press(ev: InputEvent) -> bool:
	if ev is InputEventScreenTouch:
		return (ev as InputEventScreenTouch).pressed
	if ev is InputEventMouseButton:
		return (ev as InputEventMouseButton).pressed
	if ev is InputEventKey:
		var key := ev as InputEventKey
		return key.pressed and not key.echo
	if ev is InputEventJoypadButton:
		return (ev as InputEventJoypadButton).pressed
	if ev is InputEventJoypadMotion:
		return absf((ev as InputEventJoypadMotion).axis_value) > 0.18
	return false


func _slide_canvas_source_release(ev: InputEvent) -> bool:
	if ev is InputEventScreenTouch:
		return not (ev as InputEventScreenTouch).pressed
	if ev is InputEventMouseButton:
		return not (ev as InputEventMouseButton).pressed
	if ev is InputEventKey:
		return not (ev as InputEventKey).pressed
	if ev is InputEventJoypadButton:
		return not (ev as InputEventJoypadButton).pressed
	if ev is InputEventJoypadMotion:
		return absf((ev as InputEventJoypadMotion).axis_value) <= 0.18
	return false


func _track_slide_canvas_source_state(ev: InputEvent) -> void:
	if _slide_canvas_input_context_blocks_input():
		return
	var source_token := _slide_canvas_source_token(ev)
	if source_token.is_empty():
		return
	if _slide_canvas_source_press(ev):
		_slide_canvas_held_sources[source_token] = true
	elif _slide_canvas_source_release(ev):
		_slide_canvas_held_sources.erase(source_token)


func _retire_paused_slide_canvas_release(ev: InputEvent) -> void:
	# TouchUI remains always-processing while Main is paused. It forwards only
	# terminal events here, without claiming them from the visible Pause sheet.
	if _slide_canvas_input_context_lost() \
			or not _slide_canvas_source_release(ev) \
			or _slide_canvas_source_token(ev).is_empty():
		return
	_track_slide_canvas_source_state(ev)
	if _slide_canvas_fish_route_active():
		_release_slide_canvas_source_event(ev,
			_game_obj("race", SlideRaceGame) as SlideRaceGame)


func _retire_paused_slide_canvas_restore_boundary() -> void:
	# Main does not process while SceneTree.paused; TouchUI does. After every OS
	# loss reason clears, let that ALWAYS relay spend the controller's source-free
	# boundary and two neutral poll frames without advancing g.t or routing a GUI
	# action. Ordinary Pause (no OS loss/restore guard) remains untouched.
	if not _slide_canvas_fish_route_active():
		return
	var slide := _game_obj("race", SlideRaceGame) as SlideRaceGame
	slide.refresh_canvas_layout()
	if _slide_canvas_input_context_lost():
		return
	if slide.input_context_blocks_input():
		slide.retire_input_context_restore_guard()
	if _slide_canvas_overlay_axis_wait_neutral:
		_neutralize_slide_canvas_overlay_poll()


func _forget_slide_canvas_pad_device(device: int) -> void:
	var return_source_prefix := "return:pad:%d:" % device
	for return_source_value: Variant in _slide_canvas_return_held_sources.keys():
		var return_source_token := StringName(String(return_source_value))
		if String(return_source_token).begins_with(return_source_prefix):
			_slide_canvas_return_held_sources.erase(return_source_token)
	if _slide_canvas_return_guard_active():
		_slide_canvas_return_neutral_frames = 0
	if _slide_canvas_input_context_blocks_input():
		return
	var source_prefix := "pad:%d:" % device
	for source_value: Variant in _slide_canvas_held_sources.keys():
		var source_token := StringName(String(source_value))
		if String(source_token).begins_with(source_prefix):
			_slide_canvas_held_sources.erase(source_token)
	if _slide_canvas_fish_route_active():
		(_game_obj("race", SlideRaceGame) as SlideRaceGame).forget_sources_with_prefix(
			source_prefix)


func _release_slide_canvas_source_event(ev: InputEvent,
		slide: SlideRaceGame) -> bool:
	if not _slide_canvas_source_release(ev):
		return false
	var source_token := _slide_canvas_source_token(ev)
	if source_token.is_empty():
		return false
	# A fade/overlay can appear between press and lift. Neutralize the current
	# owner first, then forward only this concrete terminal source.
	slide.cancel_input()
	if ev is InputEventScreenTouch or ev is InputEventMouseButton:
		slide.handle_touch_release(source_token)
	else:
		slide.handle_steer_release(source_token)
	return true


func _release_slide_canvas_input_under_overlay(ev: InputEvent,
		slide: SlideRaceGame) -> void:
	if _release_slide_canvas_source_event(ev, slide):
		return
	var source_token := _slide_canvas_source_token(ev)
	if _slide_canvas_source_press(ev) and not source_token.is_empty():
		slide.cancel_input(source_token)
	else:
		slide.cancel_input()


func _slide_canvas_pause_zone_hit(screen_pos: Vector2) -> bool:
	if touch_ui == null or not touch_ui.has_method("pause_zone"):
		return false
	var pause_rect: Rect2 = touch_ui.call("pause_zone") as Rect2
	return pause_rect.has_point(screen_pos)


func _route_slide_canvas_input(ev: InputEvent,
		source_was_held: bool = false) -> bool:
	# The opaque fish slide owns the entire pointer surface before TouchUI can
	# reinterpret it as swimming. Only the visible Pause corner and higher-layer
	# overlays retain their normal GUI route.
	if not _slide_canvas_fish_route_active():
		return false
	if _slide_canvas_input_context_blocks_input():
		return false
	var slide: SlideRaceGame = _game_obj("race", SlideRaceGame) as SlideRaceGame
	if get_tree().paused:
		_retire_paused_slide_canvas_release(ev)
		return false
	if _slide_canvas_overlay_owns_input():
		_release_slide_canvas_input_under_overlay(ev, slide)
		return false
	if ev is InputEventScreenTouch:
		var touch := ev as InputEventScreenTouch
		var touch_source := _slide_canvas_source_token(touch)
		if not touch.pressed:
			if _slide_canvas_input_gated():
				slide.cancel_input()
				slide.handle_touch_release(touch_source)
			elif touch.canceled:
				slide.handle_touch_cancel(touch_source)
			else:
				slide.handle_touch_release(touch_source)
			return true
		if _slide_canvas_pause_zone_hit(touch.position):
			return false
		if _slide_canvas_input_gated():
			slide.cancel_input(touch_source)
			return true
		slide.handle_touch_press(touch.position, touch_source)
		return true
	if ev is InputEventScreenDrag:
		var drag := ev as InputEventScreenDrag
		var drag_source := _slide_canvas_source_token(drag)
		if _slide_canvas_input_gated():
			slide.cancel_input()
			return true
		slide.handle_touch_drag(drag.position, drag_source)
		return true
	if ev is InputEventMouseButton:
		var mouse_button := ev as InputEventMouseButton
		if mouse_button.device == InputEvent.DEVICE_ID_EMULATION \
				or mouse_button.button_index != MOUSE_BUTTON_LEFT:
			return false
		var mouse_source := _slide_canvas_source_token(mouse_button)
		if not mouse_button.pressed:
			if _slide_canvas_input_gated():
				slide.cancel_input()
				slide.handle_touch_release(mouse_source)
			elif mouse_button.canceled:
				slide.handle_touch_cancel(mouse_source)
			else:
				slide.handle_touch_release(mouse_source)
			return true
		if _slide_canvas_pause_zone_hit(mouse_button.position):
			return false
		if _slide_canvas_input_gated():
			slide.cancel_input(mouse_source)
			return true
		slide.handle_touch_press(mouse_button.position, mouse_source)
		return true
	if ev is InputEventMouseMotion:
		var mouse_motion := ev as InputEventMouseMotion
		if mouse_motion.device == InputEvent.DEVICE_ID_EMULATION \
				or (mouse_motion.button_mask & MOUSE_BUTTON_MASK_LEFT) == 0:
			return false
		var mouse_drag_source := _slide_canvas_source_token(mouse_motion)
		if _slide_canvas_input_gated():
			slide.cancel_input()
			return true
		slide.handle_touch_drag(mouse_motion.position, mouse_drag_source)
		return true
	if ev is InputEventKey:
		var key := ev as InputEventKey
		var key_code: int = int(key.physical_keycode)
		if key_code == 0:
			key_code = int(key.keycode)
		if key_code not in [KEY_LEFT, KEY_A, KEY_RIGHT, KEY_D]:
			return false
		var key_source := _slide_canvas_source_token(key)
		var key_axis: float = -1.0 if key_code in [KEY_LEFT, KEY_A] else 1.0
		if _slide_canvas_input_gated():
			if key.pressed:
				if not key.echo:
					slide.cancel_input(key_source)
			else:
				slide.cancel_input()
				slide.handle_steer_release(key_source)
			return true
		if key.pressed:
			if not key.echo:
				slide.handle_steer_press(key_axis, key_source)
		else:
			slide.handle_steer_release(key_source)
		return true
	if ev is InputEventJoypadButton:
		var button := ev as InputEventJoypadButton
		if button.button_index not in [JOY_BUTTON_DPAD_LEFT, JOY_BUTTON_DPAD_RIGHT]:
			return false
		var pad_source := _slide_canvas_source_token(button)
		var pad_axis := -1.0 if button.button_index == JOY_BUTTON_DPAD_LEFT else 1.0
		if _slide_canvas_input_gated():
			if button.pressed:
				slide.cancel_input(pad_source)
			else:
				slide.cancel_input()
				slide.handle_steer_release(pad_source)
			return true
		if button.pressed:
			slide.handle_steer_press(pad_axis, pad_source)
		else:
			slide.handle_steer_release(pad_source)
		return true
	if ev is InputEventJoypadMotion:
		var motion := ev as InputEventJoypadMotion
		if motion.axis != JOY_AXIS_LEFT_X:
			return false
		var axis_source := _slide_canvas_source_token(motion)
		var steer_axis: float = clampf(motion.axis_value, -1.0, 1.0)
		if absf(steer_axis) <= 0.18:
			if _slide_canvas_input_gated():
				slide.cancel_input()
			slide.handle_steer_release(axis_source)
			return true
		if _slide_canvas_input_gated():
			slide.cancel_input(axis_source)
			return true
		if source_was_held:
			slide.handle_steer_motion(steer_axis, axis_source)
		else:
			slide.handle_steer_press(steer_axis, axis_source)
		return true
	return false

# ENEMY PRIORITY RULE, press half (combat wing 2026-08): hit engines get the
# finger-DOWN so a pop lands the instant the finger does — never after the
# release half of a grabby preschool tap. Returning true tells the router to
# suppress the release-side world_touched for this touch.
func _on_world_press(screen_pos: Vector2) -> bool:
	_living_world_ref().note_activity()
	if game == "melody":
		if _melody_input_gated():
			(_game_obj("melody", MelodyGame) as MelodyGame).cancel_input(
				MELODY_LEGACY_TOUCH_SOURCE)
			return false
		(_game_obj("melody", MelodyGame) as MelodyGame).handle_touch_press(
			screen_pos, MELODY_LEGACY_TOUCH_SOURCE)
		return true   # the opaque stage owns misses too; never leak into Reef travel
	if _slide_canvas_fish_route_active():
		var slide: SlideRaceGame = _game_obj("race", SlideRaceGame) as SlideRaceGame
		if _slide_canvas_input_gated():
			slide.cancel_input(SLIDE_CANVAS_LEGACY_TOUCH_SOURCE)
			return false
		slide.handle_touch_press(screen_pos, SLIDE_CANVAS_LEGACY_TOUCH_SOURCE)
		return true
	if _world_tap_gated():
		return false
	if game == "level2" and String(g.get("phase", "")) == "promenade":
		return false
	for engine_value: Variant in hit_engines:
		var engine: HitEngine = engine_value as HitEngine
		if engine == null or not engine.tap_priority:
			continue
		var enemy: Dictionary = engine.tap_pick(screen_pos)
		if not enemy.is_empty():
			engine.hit(enemy, 1, "tap")
			# a surviving enemy invites the three-stage CHARGE: keep holding
			# and a ring grows around it; the lift (or stage 3) delivers
			engine.begin_charge(enemy)
			return true
	return false

# The finger that press-fired has lifted: any held charge releases now.
func _on_world_press_release() -> void:
	if game == "melody":
		(_game_obj("melody", MelodyGame) as MelodyGame).handle_touch_release(
			MELODY_LEGACY_TOUCH_SOURCE)
		return
	if _slide_canvas_fish_route_active():
		(_game_obj("race", SlideRaceGame) as SlideRaceGame).handle_touch_release(
			SLIDE_CANVAS_LEGACY_TOUCH_SOURCE)
		return
	for engine_value: Variant in hit_engines:
		var engine: HitEngine = engine_value as HitEngine
		if engine != null:
			engine.release_charge()
	if castle_dust_he != null:
		castle_dust_he.release_charge()

# Every hit engine currently on stage, battle engines first.
func _live_hit_engines() -> Array:
	var live: Array = []
	for engine_value: Variant in hit_engines:
		var engine: HitEngine = engine_value as HitEngine
		if engine != null:
			live.append(engine)
	if castle_dust_he != null:
		live.append(castle_dust_he)
	return live

# The press-firing finger started travelling: it is a SLICE now, not a charge.
func _on_world_press_drag() -> void:
	if game == "melody":
		# TouchUI's compatibility callback has no coordinate. Cancel rather than
		# guessing a target; the raw Canvas route above supplies real drag points.
		(_game_obj("melody", MelodyGame) as MelodyGame).cancel_input(
			MELODY_LEGACY_TOUCH_SOURCE)
		return
	if _slide_canvas_fish_route_active():
		# The raw Canvas route carries the true drag coordinate; this legacy seam
		# cannot, so it may only neutralize its own fallback owner.
		(_game_obj("race", SlideRaceGame) as SlideRaceGame).cancel_input(
			SLIDE_CANVAS_LEGACY_TOUCH_SOURCE)
		return
	if game == "level2" and String(g.get("phase", "")) == "promenade":
		return
	for engine_value: Variant in _live_hit_engines():
		(engine_value as HitEngine).cancel_charge_for_drag()

# Focus loss / pause / touch-state reset: any held charge is thrown away
# WITHOUT firing — opening the pause menu must never land a hit.
func _on_world_press_cancel() -> void:
	_cancel_lagoon_navigation()
	if game == "melody":
		(_game_obj("melody", MelodyGame) as MelodyGame).cancel_input()
		return
	if _slide_canvas_fish_route_active():
		(_game_obj("race", SlideRaceGame) as SlideRaceGame).cancel_input()
		return
	for engine_value: Variant in _live_hit_engines():
		(engine_value as HitEngine).cancel_charge_for_drag()

# A world touch that travelled — offer it to the blades. A drag that reaches no
# enemy simply cuts nothing; it never stole a tap, because a moved world touch
# has never emitted world_touched.
func _on_world_drag_end(from: Vector2, to: Vector2) -> void:
	if game == "melody":
		(_game_obj("melody", MelodyGame) as MelodyGame).cancel_input(
			MELODY_LEGACY_TOUCH_SOURCE)
		return
	if _slide_canvas_fish_route_active():
		(_game_obj("race", SlideRaceGame) as SlideRaceGame).cancel_input(
			SLIDE_CANVAS_LEGACY_TOUCH_SOURCE)
		return
	if _world_tap_gated():
		return
	if game == "level2" and String(g.get("phase", "")) == "promenade":
		_lagoon_promenade_ref().handle_drag(from, to)
		return
	for engine_value: Variant in _live_hit_engines():
		var engine: HitEngine = engine_value as HitEngine
		if not engine.tap_priority:
			continue   # a suspended castle's engine must not catch swipes
		if engine.slash(from, to) > 0:
			return

func _on_touch_world(screen_pos: Vector2) -> void:
	_living_world_ref().note_activity()
	if game == "melody":
		if _melody_input_gated():
			(_game_obj("melody", MelodyGame) as MelodyGame).cancel_input()
			return
		# Release-side compatibility for callers which emit only world_touched.
		var melody: MelodyGame = _game_obj("melody", MelodyGame) as MelodyGame
		melody.handle_touch_press(screen_pos, MELODY_LEGACY_TOUCH_SOURCE)
		melody.handle_touch_release(MELODY_LEGACY_TOUCH_SOURCE)
		return
	if _slide_canvas_fish_route_active():
		if _slide_canvas_input_gated():
			(_game_obj("race", SlideRaceGame) as SlideRaceGame).cancel_input()
			return
		# Release-side compatibility for non-raw callers. The ordinary app route is
		# claimed earlier in _input and never reaches this fallback.
		var slide: SlideRaceGame = _game_obj("race", SlideRaceGame) as SlideRaceGame
		slide.handle_touch_press(screen_pos, SLIDE_CANVAS_LEGACY_TOUCH_SOURCE)
		slide.handle_touch_release(SLIDE_CANVAS_LEGACY_TOUCH_SOURCE)
		return
	if _world_tap_gated():
		return
	if game == "level2" and String(g.get("phase", "")) == "promenade":
		_lagoon_promenade_ref().handle_touch(screen_pos)
		return
	# ENEMY PRIORITY RULE: enemies are always in the forefront of the stage.
	# Every active hit engine gets first refusal on the tap — an enemy
	# overlapping any prop/friend/interactable takes the touch, and only a
	# tap that hits no enemy falls through to the interaction director.
	# (Level design opts an encounter out via HitEngine.tap_priority.)
	for engine_value: Variant in hit_engines:
		var engine: HitEngine = engine_value as HitEngine
		if engine == null or not engine.tap_priority:
			continue
		var enemy: Dictionary = engine.tap_pick(screen_pos)
		if not enemy.is_empty():
			engine.hit(enemy, 1, "tap")
			return
	var arena: CombatArena = _combat_arena_ref()
	if arena != null:
		arena.on_world_tap(screen_pos)
		return
	if game == "dustboss":
		# The boss is an ENEMY and obeys the same forefront rule: in Hybrid
		# touch the finger goes ON him, and that must be the bonk. Without this
		# the most natural thing a 4-year-old can do — tap the big fluffy
		# thing — fell through to tap-to-move and did nothing at all
		# (2026-08-02 boss stress test).
		_game_obj("dustboss", DustBossGame).on_world_tap(screen_pos)
		return
	_interaction_ref().on_world_touch(screen_pos)

# The live hit-engine client, if a battle is running: a standalone arena
# (overworld/galaxy encounters) or the arena inside either dungeon.
func _combat_arena_ref() -> CombatArena:
	if combat_game != null:
		return combat_game
	if dungeon_game != null:
		return dungeon_game.arena
	return null

func _on_touch_manual_move() -> void:
	_living_world_ref().note_activity()
	if game == "melody":
		(_game_obj("melody", MelodyGame) as MelodyGame).cancel_input()
		return
	if _slide_canvas_fish_route_active():
		(_game_obj("race", SlideRaceGame) as SlideRaceGame).cancel_input()
		return
	_cancel_lagoon_navigation()
	_tap_move_ref().cancel("manual")

func _cancel_lagoon_navigation() -> void:
	if game == "level2" and String(g.get("phase", "")) == "promenade":
		_lagoon_promenade_ref().cancel_navigation()

func _set_world_controls_enabled(enabled: bool, reason: String = "overlay") -> void:
	if enabled:
		touch_control_blocks.erase(reason)
	else:
		touch_control_blocks[reason] = true
	var controls_enabled: bool = touch_control_blocks.is_empty()
	if touch_ui != null:
		touch_ui.set_world_controls_enabled(controls_enabled)
	if not controls_enabled:
		_cancel_lagoon_navigation()
		_tap_move_ref().cancel("overlay")
		_interaction_ref().clear_focus()
		touch_interactables.clear()
	else:
		_populate_touch_interactables()

func _prepare_touch_transition() -> void:
	if touch_ui != null:
		touch_ui.cancel_all_touches()
	_cancel_lagoon_navigation()
	_tap_move_ref().cancel("transition")
	_interaction_ref().clear_focus()
	touch_interactables.clear()

func _finish_touch_transition() -> void:
	if fade_rect != null:
		fade_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_populate_touch_interactables()

func _touch_interaction_ready(interactable_id: String) -> void:
	_interaction_ref().mark_ready(interactable_id)

func touch_auto_direction() -> Vector3:
	if not touch_uses_explicit_interactions() \
			or (game == "level2" and String(g.get("phase", "")) == "promenade"):
		return Vector3.ZERO
	return _tap_move_ref().desired_direction()

func touch_auto_vertical() -> float:
	if not touch_uses_explicit_interactions() \
			or (game == "level2" and String(g.get("phase", "")) == "promenade"):
		return 0.0
	return _tap_move_ref().desired_vertical()

func _touch_add_item(id: String, label: String, pos: Vector3,
		node: Node3D = null, activation_radius: float = 6.0,
		discover_radius: float = 32.0, verb: String = "PLAY",
		payload: Variant = null, enabled: bool = true,
		affordance_kind: String = InteractionAffordanceLogic.INTERACTION) -> void:
	touch_interactables.append({
		"id": id,
		"label": label,
		"pos": pos,
		"node": node,
		"activation_radius": activation_radius,
		"discover_radius": discover_radius,
		"verb": verb,
		"payload": payload,
		"enabled": enabled,
		"affordance_kind": InteractionAffordanceLogic.normalize(affordance_kind),
	})

func _populate_touch_interactables() -> void:
	touch_interactables.clear()
	if not touch_uses_explicit_interactions() or player == null:
		return
	if game == "":
		for friend_index in range(friends.size()):
			var friend: Dictionary = friends[friend_index]
			var friend_node: Node3D = friend.get("node") as Node3D
			if not is_instance_valid(friend_node):
				continue
			var friend_affordance: String = InteractionAffordanceLogic.PLOT \
				if not bool(friend.get("won", false)) \
				else InteractionAffordanceLogic.INTERACTION
			_touch_add_item(
				"friend:%d" % friend_index,
				String(friend.get("fname", "Friend")),
				friend_node.position,
				friend_node,
				maxf(6.0, float(friend.get("start_radius", 8.0))),
				maxf(30.0, float(friend.get("linger_radius", 10.0)) * 3.0),
				"PLAY",
				friend_index,
				true, friend_affordance)
		if manta != null and is_instance_valid(manta):
			_touch_add_item("reef:shop", "Pearl Shop", manta.position, manta, 17.0, 38.0, "SHOP")
		if wreck_pos != Vector3.ZERO:
			_touch_add_item("reef:treasure", "Secret Cave", wreck_pos, null, 13.0, 34.0, "OPEN")
		if slide_portal_pos != Vector3.ZERO:
			_touch_add_item("reef:slide", "Penguin Slide", slide_portal_pos, slide_portal_penguin, 14.0, 38.0, "SLIDE")
		if brawl_portal_pos != Vector3.ZERO:
			_touch_add_item("reef:brawl", "Toy Castle", brawl_portal_pos, null, 13.0, 36.0, "PLAY")
		if dust_boss_portal_pos != Vector3.ZERO:
			_touch_add_item("reef:dustboss", "Dusty Attic", dust_boss_portal_pos, null, 13.0, 36.0, "PLAY")
		if kart_portal_pos != Vector3.ZERO:
			_touch_add_item("reef:kart", "Ocean Race", kart_portal_pos, null, 12.0, 42.0, "RACE")
		if companion_den != null and is_instance_valid(companion_den) \
				and companion_id != "" \
				and stuffie_game == null and stuffie_cool <= 0.0:
			# 9.0 matches companion.gd DEN_RADIUS (the Classic walk-in ring)
			_touch_add_item("reef:den", "Sparring Den", companion_den.position,
				companion_den, 9.0, 30.0, "PLAY")
		if portal_node != null and is_instance_valid(portal_node):
			var lagoon_affordance: String = InteractionAffordanceLogic.PLOT \
				if not level2_done_once else InteractionAffordanceLogic.INTERACTION
			_touch_add_item("reef:lagoon", "Rainbow Portal", portal_node.position,
				portal_node, 9.0, 42.0, "ENTER", null, true, lagoon_affordance)
		if ocean_routes_enabled:
			var kingdom: String = ReefDistricts.kingdom_at(Vector2(player.position.x, player.position.z))
			var gate_xz: Vector2 = ReefDistricts.kingdom_return_gate(kingdom)
			var gate_pos := Vector3(gate_xz.x, seabed_y(gate_xz.x, gate_xz.y) + 6.0, gate_xz.y)
			var return_affordance: String = InteractionAffordanceLogic.PLOT \
				if _all_friends_won() else InteractionAffordanceLogic.INTERACTION
			_touch_add_item("reef:return", "Castle Gate", gate_pos, null,
				10.0, 42.0, "ENTER", kingdom, true, return_affordance)
		return
	if game == "north":
		var north_return: Vector3 = g.get("north_return_pos", Vector3.ZERO)
		if north_return != Vector3.ZERO:
			_touch_add_item("north:return", "Magic Cave Home", north_return, null, 9.0, 42.0, "ENTER")
		return
	if game != "level2":
		return
	if String(g.get("phase", "")) == "promenade":
		return
	if String(g.get("phase", "court")) == "hall":
		# The castle room stage owns every interior touch target. Never rebuild
		# the retired free-roaming hall's world-space interaction list behind it.
		return
	else:
		_populate_courtyard_touch_interactables()

func _populate_courtyard_touch_interactables() -> void:
	var kingdom_gates: Array = g.get("ocean_kingdom_gates", [])
	for gate_index in range(kingdom_gates.size()):
		var gate: Dictionary = kingdom_gates[gate_index]
		_touch_add_item(
			"court:ocean:%d" % gate_index,
			"Ocean Kingdom",
			gate.get("pos", Vector3.ZERO),
			gate.get("rune") as Node3D,
			9.0, 40.0, "ENTER", gate_index, true,
			InteractionAffordanceLogic.PLOT)
	if g.has("northern_portal_pos"):
		_touch_add_item("court:north", "Magic Cave", g["northern_portal_pos"],
			g.get("northern_portal_rune") as Node3D, 8.0, 38.0, "ENTER")
	if galaxy_unlocked and bw_portal_pos != Vector3.ZERO:
		_touch_add_item("court:galaxy", "Butterfly World", bw_portal_pos, null, 9.0, 38.0, "ENTER")
	if ember_portal_pos != Vector3.ZERO:
		_touch_add_item("court:ember", "Ember Fortress", ember_portal_pos, null, 10.0, 38.0, "ENTER")
	if kart_legA != Vector3.ZERO:
		_touch_add_item("court:kart_a", "Rainbow Race", kart_legA, null, 14.0, 42.0, "RACE")
		_touch_add_item("court:kart_b", "Reverse Rainbow Race", kart_legB, null, 14.0, 42.0, "RACE")
	for star_index in range(l2_stars.size()):
		var star_data: Dictionary = l2_stars[star_index]
		if bool(star_data.get("got", false)):
			continue
		var star_node: Node3D = star_data.get("node") as Node3D
		if is_instance_valid(star_node):
			_touch_add_item("court:star:%d" % star_index, "Dream Star", star_node.position,
				star_node, 14.0, 50.0, "GET", star_index, true,
				InteractionAffordanceLogic.PLOT)
	if l2_open:
		for picture_index in range(wall_pics.size()):
			var picture: Dictionary = wall_pics[picture_index]
			_touch_add_item("court:picture:%d" % picture_index, "Picture Game",
				picture.get("pos", Vector3.ZERO), picture.get("node") as Node3D,
				5.0, 24.0, "PLAY", picture_index)
	if g.has("back_entry"):
		_touch_add_item("court:back_entry", "Secret Castle Door", g["back_entry"], null, 9.0, 30.0, "ENTER")
	if l2_open and g.has("entry"):
		# Never track the l2_door NODE here: the slab slides ~30 units up into
		# the sky when the castle opens, dragging the ring/pick/approach with
		# it — a front-door tap then misses entirely (and could pick the SECRET
		# back hatch through the walls instead). Anchor the target on the
		# doorway itself at walk height, where the child actually taps.
		var castle_entry: Vector3 = g["entry"]
		if lagoon_floor:
			castle_entry.y = lagoon_walk_h(castle_entry.x, castle_entry.z) + 2.0
		_touch_add_item("court:castle", "Pearl Castle", castle_entry, null,
			20.0, 52.0, "ENTER", null, true,
			InteractionAffordanceLogic.PLOT)

func _activate_touch_interactable(id: String, payload: Variant = null) -> void:
	if not touch_uses_explicit_interactions():
		return
	if touch_ui != null:
		# Consume the activating button without stealing a simultaneously held
		# left-stick finger. Fade-backed activities clear every owner below.
		touch_ui.consume_action()
	if id.begins_with("friend:"):
		var friend_index: int = int(payload)
		if friend_index >= 0 and friend_index < friends.size():
			var friend: Dictionary = friends[friend_index]
			friend["cool"] = 0.0
			_start_game(friend)
		return
	match id:
		"reef:shop":
			shop_cool = 16.0
			_start_game(shop_fr)
		"reef:treasure":
			treasure_cool = 12.0
			_start_game(treasure_fr)
		"reef:slide":
			slide_cool = 14.0
			_start_game(slide_fr)
		"reef:brawl":
			brawl_cool = 14.0
			_start_game(brawl_fr)
		"reef:dustboss":
			dust_boss_cool = 14.0
			_start_game(dust_boss_fr)
		"reef:kart":
			_start_kart_game(false, "terrain")
		"reef:den":
			stuffie_cool = 14.0
			_start_stuffie_battle()
		"reef:lagoon":
			_enter_level2(level2_done_once)
		"reef:return":
			ocean_kingdom = String(payload)
			_enter_level2(false, false, true)
		"court:north":
			_enter_northern_kingdom()
		"north:return":
			_enter_level2(false, true)
		"court:galaxy":
			kart_from = "level2"
			_start_galaxy()
		"court:ember":
			kart_float_dest = "ember"
			_start_kart_game(false, "float")
		"court:kart_a":
			_start_kart_game(false, "float")
		"court:kart_b":
			_start_kart_game(true, "float")
		"court:back_entry":
			_enter_castle_interior(true)
		"court:castle":
			_enter_castle_interior()
		_:
			if id.begins_with("court:ocean:"):
				var gate_index: int = int(payload)
				var gates: Array = g.get("ocean_kingdom_gates", [])
				if gate_index >= 0 and gate_index < gates.size():
					var gate: Dictionary = gates[gate_index]
					_enter_ocean_kingdom(String(gate["kingdom"]))
			elif id.begins_with("court:picture:"):
				_touch_open_picture(int(payload))
			elif id.begins_with("court:star:"):
				# Arrival collection remains the familiar forgiving proximity
				# reward; the tap supplies navigation, not a second requirement.
				pass

func _touch_open_picture(picture_index: int) -> void:
	if picture_index < 0 or picture_index >= wall_pics.size():
		return
	var picture: Dictionary = wall_pics[picture_index]
	var art_key: String = String(picture.get("art", ""))
	if art_key == "p_slide":
		_l2_start_slide()
	elif PIC_GAME.has(art_key):
		_mg2d_open(String(PIC_GAME[art_key]))

func _leave_current_activity() -> void:
	_pause_ref()._leave_current_activity()


func _open_dance_demo() -> void:
	if dance_engine == null or not is_instance_valid(dance_engine):
		dance_engine = preload("res://scripts/games/dance_engine.gd").new(self)
		add_child(dance_engine)
	(dance_engine as DanceEngine).open_demo()

# Phase 7.4: one file per minigame under scripts/games/ (state stays on
# main; each game class receives main by reference)
var _games := {}

func _game_obj(key: String, cls: Variant) -> Variant:
	if not _games.has(key):
		_games[key] = cls.new(self)
	return _games[key]

func _tick_fetch(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_game_obj("fetch", FetchGame)._tick_fetch(delta, fr, ppos)

func _tick_dolls(delta: float, fr: Dictionary) -> void:
	_game_obj("dolls", DollsGame)._tick_dolls(delta, fr)

func _tick_brawl(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_game_obj("brawl", BrawlGame)._tick_brawl(delta, fr, ppos)

func _seek_hide() -> void:
	_game_obj("seek", SeekGame)._seek_hide()

func _tick_course(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_game_obj("race", SlideRaceGame)._tick_course(delta, fr, ppos)

func _tick_shop(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	_game_obj("shop", ShopGame)._tick_shop(delta, fr, ppos)

func _shop_buy(id: String) -> void:
	_game_obj("shop", ShopGame)._shop_buy(id)

func _tank_buy(id: String) -> void:
	_game_obj("shop", ShopGame)._tank_buy(id)

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
	# swap Roshan's whole appearance to the chosen skin (classic = 2.5D atlas)
	if player == null:
		return
	var s := _skin_def(skin_id)
	skin_id = String(s["id"])   # normalise any stale/removed skin id back to a valid one
	player.set_skin(skin_id, String(s["sprite"]))
	if _castle_rooms_25d != null and _castle_rooms_25d.is_open():
		_castle_rooms_25d.refresh_player_skin()

func _all_pearls_done() -> bool:
	return pearls.is_empty()

func _check_level2_unlock(ppos: Vector3, delta: float) -> void:
	var stars := 0
	for f in friends:
		if f["found"]:
			stars += 1
	# The original gate required a ten-pearl wallet. Remember the highest balance
	# so buying a toy later can never close a story doorway that already opened.
	pearls_ever = maxi(pearls_ever, pearl_count)
	# Story progress is a permanent milestone, never a test of the current wallet.
	if not portal_unlocked and trophies >= 5 and stars >= 5 and pearls_ever >= PEARL_TOTAL:
		portal_unlocked = true
		_write_save()
	var ready: bool = portal_unlocked or level2_done_once
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
		if not touch_uses_explicit_interactions() and portal_ready and portal_armed and portal_cool <= 0.0 and game == "" and finale_t < 0.0 and pdist < 8.0:
			portal_armed = false
			if level2_done_once:
				l2_star_progress = [true, true, true]
				_enter_level2(true)
			else:
				for i in range(l2_star_progress.size()):
					l2_star_progress[i] = bool(stickers.get("_l2_star_%d" % i, l2_star_progress[i]))
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

func _enter_level2(from_castle: bool = false, from_north: bool = false,
	at_ocean_gate_hub: bool = false) -> void:
	# covers every entry: the ocean portal, the _end_game/pause deferred
	# returns and _restore_level2_after_trip (call_deferred callers unchanged)
	_fade_cut(_enter_level2_now.bind(from_castle, from_north, at_ocean_gate_hub))

func _enter_level2_now(from_castle: bool = false, from_north: bool = false,
	at_ocean_gate_hub: bool = false) -> void:
	game = "level2"
	# The reef sun is a persistent world node. Sky Lagoon supplies its own sun;
	# stacking both erased nearly all color from pearl, snow, and pastel props.
	if sun_light != null:
		sun_light.visible = false
	# A completed castle is a permanent playground. Never rebuild its three-star
	# lock on a later visit, even when an older caller omits from_castle.
	if level2_done_once:
		l2_star_progress = [true, true, true]
	else:
		for i in range(l2_star_progress.size()):
			l2_star_progress[i] = bool(stickers.get("_l2_star_%d" % i, l2_star_progress[i]))
	# free whatever level nodes are still alive BEFORE rebuilding: the rainbow-
	# road/galaxy return path re-entered here without tearing the lagoon down
	# first, stacking a second terrain+castle+playground exactly on top of the
	# live one (coplanar z-fighting shimmer over the whole level). Same idiom
	# as _enter_castle_interior; the callers that already pre-free stay no-ops.
	if String(g.get("phase", "")) == "promenade" and _sky_lagoon_promenade != null:
		_sky_lagoon_promenade.teardown()
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	g = {"t": 0.0}
	arena_solids.clear()
	arena_zones.clear()
	fade_walls.clear()
	lagoon_floor = true   # the courtyard floor follows the rolling-hill terrain
	northern_floor = false
	_play_music("level2")
	return_pos = player.position
	# The Canvas promenade owns its visible Roshan, Camera2D and route state.
	# Preserve the generic player only as a hidden return-position compatibility
	# object; neither its renderer nor its compatibility camera may remain authoritative.
	player.vel = player.vel * 0.0
	player.visible = false
	if player.cam != null and player.cam.is_inside_tree():
		player.cam.clear_current(false)
	arena_center = LEVEL2_POS
	arena_dome = 235.0
	arena_ceil = 120.0
	l2_stars = []
	l2_open = false
	g["phase"] = "court"
	g["ocean_gate_hub"] = at_ocean_gate_hub
	# No spatial fallback sits behind the Canvas product. A missing Canvas layer
	# must fail visibly instead of silently revealing the retired 3D sky grade.
	arena_env = null
	we_node.environment = null
	if String(g.get("phase", "")) == "court":
		_lagoon_promenade_ref().build(from_castle, from_north, at_ocean_gate_hub)
		_day_one_begin_arrival()
		l2_open = from_castle or level2_done_once
		# A prior world's assisted route, focus ring, objective or spatial
		# critter must not survive underneath the Canvas product. These generic
		# directors remain available elsewhere but have no active Sky authority.
		_tap_move_ref().cancel("sky_canvas_entry")
		_interaction_ref().clear_focus()
		touch_interactables.clear()
		_set_objective("", null, "")
		_collection_ref().tick(0.0, player.position)
		return
	_build_pearl_castle(LEVEL2_POS)
	if is_night:
		_build_lagoon_night(LEVEL2_POS)
	# (Phase 3 fix: a stale _play_music("finale") here overrode the "level2"
	# track selected at the top of this function — the lagoon music never played)
	if from_north:
		# Return at the cave mouth, facing the snowy village. The star is disarmed
		# until Roshan swims away, preventing a bounce loop.
		var north_gate: Vector3 = g.get("northern_portal_pos",
			LEVEL2_POS + Vector3(-128.0, 52.0, -165.0))
		player.position = g.get("alpine_cave_entrance", north_gate + Vector3(20.0, 0.0, 0.0))
		player.position.y = lagoon_walk_h(player.position.x, player.position.z) + 2.0
		player.yaw = PI * 0.5
		player.vel = Vector3.ZERO
		g["northern_portal_armed"] = false
		show_msg("Roshan", "Back through the magic cave star!", "pearl2")
	elif from_castle:
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
		if at_ocean_gate_hub:
			show_msg("Roshan", "Two ocean kingdoms! The sunny shell leads to the Caribbean. The blue ice gate leads to Norway!", "intro")
		else:
			show_msg("Princess Huluu", "Follow the sparkle trail! Find 3 Dream Stars!", "intro")
	player.snap_cam()   # never lerp the lens across the world gap (CAMERA_AUDIT P0)

func _enter_northern_kingdom() -> void:
	_fade_cut(_enter_northern_kingdom_now)

func _enter_northern_kingdom_now() -> void:
	if String(g.get("phase", "")) == "promenade" \
			and _sky_lagoon_promenade != null:
		_sky_lagoon_promenade.teardown()
	player.visible = true
	if player.cam != null and player.cam.is_inside_tree():
		player.cam.make_current()
	game = "north"
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	g = {"t": 0.0, "phase": "north"}
	arena_solids.clear()
	arena_zones.clear()
	fade_walls.clear()
	lagoon_floor = false
	northern_floor = true
	_play_music("northern")
	arena_center = NORTHERN_POS
	arena_dome = 430.0   # the redesigned kingdom is a LONG strip, not a disc
	# Low sky: Roshan can hop over the canopy but not helicopter above the
	# whole stage — the interesting layer is the ground, and the mist hides
	# nothing worth seeing from up high anyway.
	arena_ceil = 54.0
	_northern_ref().build(NORTHERN_POS)
	var spawn_y: float = northern_walk_h(NORTHERN_POS.x, NORTHERN_POS.z + 332.0)
	player.position = Vector3(NORTHERN_POS.x, spawn_y + 2.0, NORTHERN_POS.z + 332.0)
	player.yaw = PI
	player.vel = Vector3.ZERO
	player.snap_cam()   # never lerp the lens across the world gap (CAMERA_AUDIT P0)
	show_msg("Roshan", "A magical forest! The glowing lights lead to the fjord castle!", "pearl")

func _butterfly_gate(scl: float) -> Node3D:
	return LandmarkArtFactory.create_butterfly_gate(scl)

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
	# WORLD-space triplanar: adjacent boxes/panels sharing a sheet tile continuously
	# instead of each segment restarting the pattern at its own origin (this was the
	# castle "texture splicing"). Moving meshes (the keep door) must switch this off.
	m.uv1_world_triplanar = true
	m.uv1_scale = Vector3(uvs, uvs, uvs)
	m.roughness = 1.0
	return m

func _castle_mat(role: String, uvs: float = 0.1, tint: Color = Color(1, 1, 1), roughness_override: float = -1.0) -> StandardMaterial3D:
	# Castle-only painted materials. The legacy up_* normal maps are identical
	# neutral placeholders and their roughness sheets do not match the painted
	# albedos. Sampling those through triplanar projection cost the Mali three
	# times per map while adding false/no surface detail, so this family keeps
	# one color texture plus an honest scalar roughness per material role.
	var tex_path: String = "res://assets/terrain/up_castle_col.jpg"
	var role_roughness: float = 0.86
	match role:
		"floor":
			tex_path = "res://assets/terrain/castle_floor_col.jpg"
			role_roughness = 0.62
		"carpet":
			tex_path = "res://assets/terrain/castle_carpet_col.jpg"
			role_roughness = 0.95
		"door":
			tex_path = "res://assets/terrain/up_door_col.jpg"
			role_roughness = 0.78
		"roof":
			tex_path = "res://assets/terrain/up_roof_col.jpg"
			role_roughness = 0.82
		"wood":
			tex_path = "res://assets/terrain/up_wood_col.jpg"
			role_roughness = 0.78
		"cobble":
			tex_path = "res://assets/terrain/up_cobble_col.jpg"
			role_roughness = 0.90
		"kitchen_floor":
			tex_path = "res://assets/terrain/kitchen_floor_col.jpg"
			role_roughness = 0.72
		"kitchen_wood":
			tex_path = "res://assets/terrain/kitchen_wood_col.jpg"
			role_roughness = 0.80
		"kitchen_counter":
			tex_path = "res://assets/terrain/kitchen_counter_col.jpg"
			role_roughness = 0.58
		"bathroom_tile":
			tex_path = "res://assets/terrain/bathroom_tile_col.jpg"
			role_roughness = 0.68
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = load(tex_path)
	mat.albedo_color = tint
	mat.uv1_triplanar = true
	mat.uv1_world_triplanar = true
	mat.uv1_scale = Vector3(uvs, uvs, uvs)
	mat.roughness = roughness_override if roughness_override >= 0.0 else role_roughness
	mat.metallic = 0.0
	return mat

func _register_castle_light(light: Light3D, speedy_visible: bool = false, night_only: bool = false, quality_shadows: bool = false) -> void:
	# One quality-aware registry serves the outdoor keep and the rebuilt hall.
	# Both scenes reset g before building, so stale freed lights never accumulate.
	var detail_lights: Array = g.get("castle_detail_lights", [])
	detail_lights.append({"light": light, "speedy": speedy_visible, "night_only": night_only, "quality_shadows": quality_shadows})
	g["castle_detail_lights"] = detail_lights
	var show_now: bool = (quality != "speedy" or speedy_visible) and (not night_only or is_night)
	light.visible = show_now
	if quality_shadows:
		light.shadow_enabled = quality != "speedy"

func _sync_castle_lights() -> void:
	var speedy: bool = quality == "speedy"
	var detail_lights: Array = g.get("castle_detail_lights", [])
	for value in detail_lights:
		var item: Dictionary = value
		var light: Light3D = item.get("light") as Light3D
		if not is_instance_valid(light):
			continue
		var show_now: bool = (not speedy or bool(item.get("speedy", false))) and (not bool(item.get("night_only", false)) or is_night)
		light.visible = show_now
		if bool(item.get("quality_shadows", false)):
			light.shadow_enabled = not speedy

func _l2_box(pos: Vector3, size: Vector3, col: Color, glow: float = 0.0) -> MeshInstance3D:
	var b := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	b.mesh = bm
	# All Level 2 blockwork shares the castle albedo, but avoids the legacy
	# placeholder normal and mismatched roughness sheets audited in this pass.
	var m := _castle_mat("wall", 0.12, col.lightened(0.12))
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
var _sky_lagoon_promenade: SkyLagoonPromenade = null

func _lagoon_ref() -> SkyLagoon:
	if _sky_lagoon == null:
		_sky_lagoon = SkyLagoon.new(self)
	return _sky_lagoon

func _lagoon_promenade_ref() -> SkyLagoonPromenade:
	if _sky_lagoon_promenade == null:
		_sky_lagoon_promenade = SkyLagoonPromenade.new(self)
	return _sky_lagoon_promenade

# The northern kingdom beyond the Alpine cave star is loaded separately so its
# forest, town, and castle never share the mobile render budget with the lagoon.
# State stays here on main; the satellite only builds and ticks it.
var _northern_kingdom: NorthernKingdom = null

func _northern_ref() -> NorthernKingdom:
	if _northern_kingdom == null:
		_northern_kingdom = NorthernKingdom.new(self)
	return _northern_kingdom

func northern_walk_h(x: float, z: float) -> float:
	return _northern_ref().walk_h(x, z)

func _tick_northern(delta: float, ppos: Vector3) -> void:
	_northern_ref().tick(delta, ppos)

# The courtyard train (Sky Lagoon ride) lives in scripts/arena/courtyard_train.gd
# (state stays here in g["train"] / g["toys"]; the satellite receives main by reference)
var _train_obj: CourtyardTrain = null

func _train_ref() -> CourtyardTrain:
	if _train_obj == null:
		_train_obj = CourtyardTrain.new(self)
	return _train_obj

func _build_pearl_castle(o: Vector3) -> void:
	_lagoon_ref()._build_pearl_castle(o)

func _build_lagoon_terrain(o: Vector3) -> void:
	_lagoon_ref()._build_lagoon_terrain(o)

func _build_lagoon_night(o: Vector3) -> void:
	_lagoon_ref()._build_lagoon_night(o)

func _build_fairy_pond(o: Vector3) -> void:
	_lagoon_ref()._build_fairy_pond(o)

func _tick_level2(delta: float, ppos: Vector3) -> void:
	if String(g.get("phase", "")) == "promenade":
		_lagoon_promenade_ref().tick(delta)
		return
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

# courtyard trees: pack name -> painted GEN2 sculpt (strangler-fig fallback)
const NATURE_GEN2 := {"tree_palm": "tree_palm", "tree_default_fall": "tree_fall",
	"tree_simple_fall": "tree_fall2", "tree_fat": "tree_fat", "tree_pineRoundF": "tree_pineroundf"}

func _wind_sway(node: Node3D) -> void:
	# simple living-world animation: a slow base-pinned lean, random phase
	# per tree (gen2 wraps pivot at the base, so this reads as wind not tilt)
	var amp: float = 0.018 + randf() * 0.014
	var dur: float = 1.7 + randf() * 0.9
	# on the tree, not on main: a looping tween on main whose target is freed
	# degenerates into a zero-duration loop and errors every frame forever
	var tw := node.create_tween().set_loops()
	tw.tween_property(node, "rotation:z", amp, dur).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(node, "rotation:z", -amp, dur * 2.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(node, "rotation:z", 0.0, dur).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)

func _nature(name: String, pos: Vector3, scl: float, yrot: float) -> Node3D:
	if NATURE_GEN2.has(name):
		var gn := _gen2_prop(String(NATURE_GEN2[name]), pos, scl, yrot, 0.06)
		if gn != null:
			game_nodes.append(gn)
			_wind_sway(gn)
			return gn
	var story_plant: Node3D = StoryArtFactory.plant(name, scl)
	if story_plant != null:
		story_plant.position = pos
		story_plant.rotation.y = yrot
		add_child(story_plant)
		game_nodes.append(story_plant)
		_wind_sway(story_plant)
		return story_plant
	return null

var _kit_cache := {}

func _toon_tile(node: Node, key: String, uvs: float, tint: Color = Color(1, 1, 1)) -> void:
	# NANO-BANANA TILE WRAP (owner 2026-07-11): dress an EXISTING model in a
	# painted GEN2 tile. Triplanar ignores the mesh's own UVs, so any object
	# already in the game can wear the new art - no new geometry, no Meshy.
	if node is MeshInstance3D:
		var mi := node as MeshInstance3D
		if mi.mesh != null:
			# One shared material per tile config, cached on main — same
			# teardown rationale as _toonify's cache: a node-owned material
			# is freed before its instance and the headless dummy renderer
			# errors on the stale RID during the dirty-instance flush.
			var ck := "%s|%s|%s" % [key, uvs, tint]
			var tm: StandardMaterial3D = _toon_mats.get(ck)
			if tm == null:
				tm = StandardMaterial3D.new()
				tm.albedo_texture = load("res://assets/terrain/up_%s_col.jpg" % key)
				tm.albedo_color = _pastel(tint)
				tm.uv1_triplanar = true
				tm.uv1_scale = Vector3(uvs, uvs, uvs)
				tm.roughness = 1.0
				tm.metallic = 0.0
				tm.metallic_specular = 0.1
				_toon_mats[ck] = tm
			for si in range(mi.mesh.get_surface_count()):
				mi.set_surface_override_material(si, tm)
	for c in node.get_children():
		_toon_tile(c, key, uvs, tint)

# playground: kit path -> painted GEN2 sculpt + its ambient toy animation
const KIT_GEN2 := {"play/slide_A": "play_slide", "play/swing_A_large": "play_swing",
	"play/merry_go_round": "play_merry", "play/seesaw_large": "play_seesaw",
	"play/sandbox_round_decorated": "play_sandbox", "play/spring_horse_A": "play_horse"}

func _toy_anim(node: Node3D, name: String) -> void:
	# simple always-alive toy motion (cosmetic; solids stay where they were)
	if name.contains("merry"):
		# the ambient spin IS the ride drive — _tick_toys reads rotation.y to
		# seat Roshan on the deck, so this never pauses. 7s/turn reads clearly
		# as spinning from across the meadow (11s looked parked at a glance).
		# All three toy tweens live on the toy node (not main) so they die
		# with it instead of error-looping empty after a zone rebuild.
		var tw := node.create_tween().set_loops()
		tw.tween_property(node, "rotation:y", node.rotation.y + TAU, 7.0)
	elif name.contains("horse"):
		var tw2 := node.create_tween().set_loops()
		tw2.tween_property(node, "rotation:x", 0.07, 0.9).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		tw2.tween_property(node, "rotation:x", -0.05, 0.9).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		node.set_meta("toy_tw", tw2)   # paused while Roshan rides — she drives the rock herself
	elif name.contains("seesaw"):
		var tw3 := node.create_tween().set_loops()
		tw3.tween_property(node, "rotation:z", 0.055, 2.4).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		tw3.tween_property(node, "rotation:z", -0.055, 2.4).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		node.set_meta("toy_tw", tw3)   # paused while Roshan bounces the open seat
	elif name.contains("swing"):
		# the sculpt is fused (no seat nodes), so the empty seats pendulum at
		# the vertex stage: swap the cel shader for the swing_sway variant and
		# feed it each mesh's local AABB — pivot at the top bar, middle span
		# only (legs + ground rails stay rigid). See swing_sway.gdshader.
		var sway_sh: Shader = load("res://assets/shaders/swing_sway.gdshader")
		for mi in _all_meshes(node):
			if mi.mesh == null:
				continue
			var bb: AABB = mi.mesh.get_aabb()
			for si in range(mi.mesh.get_surface_count()):
				var sm: Material = mi.get_active_material(si)
				if sm is ShaderMaterial:
					var swm := sm as ShaderMaterial
					swm.shader = sway_sh
					swm.set_shader_parameter("bar_y", bb.position.y + bb.size.y * 0.92)
					swm.set_shader_parameter("y_min", bb.position.y + bb.size.y * 0.12)
					swm.set_shader_parameter("x_max", bb.size.x * 0.30)

func _kit(name: String, pos: Vector3, target: float, yrot: float = 0.0) -> Node3D:
	# instantiate a CC0 kit piece, restyle it for the
	# storybook look (_fit_prop calls _toonify), fit its footprint to `target`
	# units and seat its base at pos. Collision stays the caller's job — solids
	# are hand-placed so gameplay clearances remain explicit.
	if KIT_GEN2.has(name):
		var kg := _gen2_prop(String(KIT_GEN2[name]), pos, target, yrot, 0.04)
		if kg != null:
			game_nodes.append(kg)
			_toy_anim(kg, name)
			return kg
	return null

var _gen2_cache := {}
var _gen2_mesh_cache := {}
const GEN2_CEL := true   # banded cel light + navy ink outline on GEN2 props. Flip false to revert.
var _gen2_outline: ShaderMaterial = null

# crossed-quad sea flora sprites: [name, height/width aspect, width factor]
const SEAGRASS_SPRITES := [["seagrass", 0.82, 1.0], ["grasstuft", 0.82, 0.75], ["kelp", 2.63, 0.55]]
var _seagrass_mats := {}   # sprite name -> 4 phase-varied sway materials

# A RIGGED family creature: same Meshy mesh as _gen2_creature but skinned to a
# 20-bone quadruped (tools/build_chuck_rig.py + animate_kitty.py) with real
# idle/walk/run/happy clips — legs actually cycle and paws plant, instead of a
# static mesh sliding. Recolour still rides the sway shader (sway_amount 0 so it
# never fights the skeleton; paint_body/fin map HER colours by luma). The
# returned wrap carries meta "ap" = the AnimationPlayer for the behaviour FSM.
func _gen2_creature_rigged(gname: String, target: float, body: Color, accent: Color, third: Color = Color(1, 1, 1)) -> Node3D:
	var ps: PackedScene = _gen2_cache.get(gname, null)
	if ps == null:
		var path := ""
		if not ResourceLoader.exists(path):
			return null
		ps = load(path)
		_gen2_cache[gname] = ps
	if ps == null:
		return null
	var wrap := Node3D.new()
	var inst: Node3D = ps.instantiate()
	_fit_prop(inst, target)          # fit footprint + seat base at y=0 (materials re-swapped below)
	inst.rotation.y = -PI * 0.5      # face local -X (mover/FSM convention; memory gen2-creature-facing)
	var swaysh: Shader = load("res://assets/shaders/creature_sway.gdshader")
	for mi in _all_meshes(inst):
		var mesh: Mesh = mi.mesh
		if mesh == null:
			continue
		for si in range(mesh.get_surface_count()):
			var src: Material = mi.get_active_material(si)
			var alb: Texture2D = null
			if src is StandardMaterial3D:
				alb = (src as StandardMaterial3D).albedo_texture
			var sm := ShaderMaterial.new()
			sm.shader = swaysh
			if alb != null:
				sm.set_shader_parameter("albedo_tex", alb)
			sm.set_shader_parameter("sway_amount", 0.0)   # the skeleton animates; no vertex sway
			sm.set_shader_parameter("paint_mix", 1.0)
			sm.set_shader_parameter("paint_body", body)
			sm.set_shader_parameter("paint_fin", accent)
			sm.set_shader_parameter("paint_third", third)
			# zone mask (baked from geometry) paints the BOOK-ART pattern:
			# body / accent / third-colour regions; black = fixed features
			var mpath := "res://assets/props/gen2/" + gname.replace("_rigged", "_mask") + ".png"
			if ResourceLoader.exists(mpath):
				sm.set_shader_parameter("zone_mask", load(mpath))
				sm.set_shader_parameter("use_zones", 1)
			mi.set_surface_override_material(si, sm)
	var ap: AnimationPlayer = inst.find_child("AnimationPlayer", true, false)
	if ap != null:
		for an in ap.get_animation_list():
			ap.get_animation(an).loop_mode = Animation.LOOP_LINEAR
		ap.play("idle")
		wrap.set_meta("ap", ap)
	wrap.add_child(inst)
	wrap.set_meta("gen2", true)
	return wrap

func _gen2_creature(gname: String, pos: Vector3, target: float) -> Node3D:
	# a family-style Meshy animal: loaded/fit like a prop, then every surface
	# swaps to the sway shader (tail-weighted swim wave + toon response, ink
	# outline as next_pass). Movers drive position/heading exactly as they
	# drove the pack creatures - facing offset measured to be zero.
	var wrap := _gen2_prop(gname, pos, target, 0.0, 0.0)
	if wrap == null:
		return null
	# Meshy creatures face -Y in the Blender frame, but the mover math steers
	# a -X face (measured against the pack turtle; playtest 2026-07-11: "ray
	# swims sideways, so does turtle"). Quarter-turn the inner instance and
	# swing its centering offset with it; mesh-local axes are untouched, so
	# the sway shader's tail weighting stays valid.
	var inner: Node3D = wrap.get_child(0)
	inner.rotation.y = -PI * 0.5
	var off: Vector3 = inner.position
	inner.position = Vector3(-off.z, off.y, off.x)
	var ph := randf() * TAU
	var prof: Array = CREATURE_SWAY.get(gname, [0, 4.2, 0.09])
	for mi in _all_meshes(wrap):
		var mesh: Mesh = mi.mesh
		if mesh == null:
			continue
		for si in range(mesh.get_surface_count()):
			var src0: Material = mi.get_active_material(si)
			var sm := ShaderMaterial.new()
			sm.shader = load("res://assets/shaders/creature_sway.gdshader")
			# _gen2_prop's cel pass already swapped the surface to a
			# ShaderMaterial, so the painted albedo must be read back from
			# either material type (BaseMaterial3D-only left every creature
			# hint_default_white: ghost animals, playtest 2026-07-11)
			var tex0: Texture2D = null
			if src0 is BaseMaterial3D:
				tex0 = (src0 as BaseMaterial3D).albedo_texture
			elif src0 is ShaderMaterial:
				tex0 = (src0 as ShaderMaterial).get_shader_parameter("albedo_tex")
			if tex0 != null:
				sm.set_shader_parameter("albedo_tex", tex0)
			# Blender-authored replacements use flat material colors instead of
			# baked albedo maps. Preserve that tint when the swim shader takes over.
			var source_tint := Color.WHITE
			if src0 is BaseMaterial3D:
				source_tint = (src0 as BaseMaterial3D).albedo_color
			elif src0 is ShaderMaterial:
				var tint_value: Variant = (src0 as ShaderMaterial).get_shader_parameter("tint")
				if tint_value is Color:
					source_tint = tint_value as Color
			sm.set_shader_parameter("tint", source_tint)
			sm.set_shader_parameter("phase", ph)
			sm.set_shader_parameter("sway_mode", int(prof[0]))
			sm.set_shader_parameter("sway_speed", float(prof[1]))
			sm.set_shader_parameter("sway_amount", float(prof[2]))
			sm.set_shader_parameter("paint_contrast", 1.18 if gname in ["dolphin", "whale", "penguin"] else 1.0)
			if CREATURE_REPAINT_3.has(gname):
				var repaint: Array = CREATURE_REPAINT_3[gname]
				sm.set_shader_parameter("paint_mix", 0.72)
				sm.set_shader_parameter("paint_body", repaint[0])
				sm.set_shader_parameter("paint_fin", repaint[1])
			sm.next_pass = _gen2_outline_mat()
			mi.set_surface_override_material(si, sm)
	if gname == "penguin":
		_attach_penguin_beak(wrap)   # AFTER the material pass so the beak keeps its own paint
	return wrap

func _attach_penguin_beak(wrap: Node3D) -> void:
	# the Meshy penguin sculpt has NO beak — just a smooth face with eyes
	# (owner report 2026-07-13). Graft a small orange cone onto the rig's
	# head bone so it rides every clip. Placement tuned via
	# scripts/probe_penguin_beak.gd (bone frame != Blender frame — don't
	# eyeball it, probe it).
	var skels := wrap.find_children("*", "Skeleton3D", true, false)
	if skels.is_empty():
		return
	var att := BoneAttachment3D.new()
	(skels[0] as Skeleton3D).add_child(att)
	att.bone_name = "head"
	var beak := MeshInstance3D.new()
	var cone := CylinderMesh.new()
	cone.top_radius = 0.0
	cone.bottom_radius = 0.07
	cone.height = 0.18
	cone.radial_segments = 24
	beak.mesh = cone
	var bm := StandardMaterial3D.new()
	bm.albedo_color = Color(1.0, 0.66, 0.12)   # matches his feet
	bm.roughness = 0.9
	bm.next_pass = _gen2_outline_mat()
	beak.material_override = bm
	att.add_child(beak)
	beak.position = Vector3(0, 0.50, 0.14)
	beak.rotation = Vector3(-0.32, 0, 0)

func _gen2_seagrass(pos: Vector3, size: float) -> Node3D:
	# Converted 2D cards replace the crossed cards that dominated nearby cameras.
	var variant: int = randi() % 2
	var family: String = "kelp" if randf() > 0.82 else "seagrass"
	var path := ""
	if not ResourceLoader.exists(path):
		return null
	var packed: PackedScene = load(path)
	if packed == null:
		return null
	var wrap := Node3D.new()
	var inst: Node3D = packed.instantiate()
	_fit_prop(inst, size * (0.62 if family == "kelp" else 0.46))
	wrap.add_child(inst)
	wrap.position = pos
	wrap.rotation.y = randf() * TAU
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

func _gen2_static_mesh(name: String) -> Mesh:
	# MultiMesh scenery has no remaining model source in the 2D build.
	var cached: Mesh = _gen2_mesh_cache.get(name, null)
	if cached != null:
		return cached
	var path := ""
	if not ResourceLoader.exists(path):
		return null
	var ps: PackedScene = load(path)
	if ps == null:
		return null
	var inst: Node3D = ps.instantiate()
	var meshes := _all_meshes(inst)
	if meshes.is_empty():
		inst.free()
		return null
	var result: Mesh = (meshes[0] as MeshInstance3D).mesh
	_gen2_mesh_cache[name] = result
	inst.free()
	return result

func _art35_static_mesh(path: String) -> Mesh:
	var cached: Mesh = _gen2_mesh_cache.get(path, null)
	if cached != null:
		return cached
	if not ResourceLoader.exists(path):
		return null
	var packed: PackedScene = load(path)
	if packed == null:
		return null
	var inst: Node3D = packed.instantiate()
	var meshes := _all_meshes(inst)
	if meshes.is_empty():
		inst.free()
		return null
	var result: Mesh = (meshes[0] as MeshInstance3D).mesh
	_gen2_mesh_cache[path] = result
	inst.free()
	return result

func _art35_prop(path: String, pos: Vector3, scl: float = 1.0, yaw: float = 0.0) -> Node3D:
	# Authored multi-part props must stay as scene trees; taking only the first
	# mesh would drop their outlines, petals, legs, books, or snow layers.
	if not ResourceLoader.exists(path):
		return null
	var packed: PackedScene = load(path) as PackedScene
	if packed == null:
		return null
	var prop: Node3D = packed.instantiate() as Node3D
	if prop == null:
		return null
	prop.position = pos
	prop.scale = Vector3.ONE * scl
	prop.rotation.y = yaw
	_cel_replace(prop, _gen2_outline_mat())
	add_child(prop)
	game_nodes.append(prop)
	return prop

func _gen2_prop(name: String, pos: Vector3, target: float, yrot: float = 0.0, sink: float = 0.0) -> Node3D:
	# GEN2 pipeline prop: art generated in the family storybook style and
	# converted to 2D before shipping.
	# the phone (tools/shrink_glb.py). Same contract as _kit: fits footprint
	# to `target`, seats base at pos; collisions and node-list registration
	# (game_nodes/flora_nodes) stay the caller's job.
	# Carryable reef props retain approved 2D art after the retired model pack
	# was removed. CarrySystem owns these nodes, so do not register them in
	# game_nodes: Canvas minigames clear that list as part of their lifecycle.
	if name == "starfish":
		var star := LandmarkArtFactory.create_star(2.4, Color(1.0, 0.76, 0.24))
		star.position = pos
		star.rotation.y = yrot
		star.scale *= target / 2.4
		add_child(star)
		return star
	if name == "spiralshell":
		var shell := StoryArtFactory.ground_card("res://assets/props/gen2/spiralshell_Image_0_flat.png", target)
		shell.position = pos
		shell.rotation.y = yrot
		add_child(shell)
		return shell
	var ps: PackedScene = _gen2_cache.get(name, null)
	if ps == null:
		var path := ""
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
		# Corals get the two-layer FLOW variant: green growth sways with the
		# ocean, rocky bodies stay rigid (greenness-gated in the shader).
		if name.begins_with("coral"):
			_cel_replace(inst, _gen2_outline_mat(), "res://assets/shaders/coral_flow.gdshader")
		else:
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
				# perf (Mali-G52): identical pastel colors share ONE material.
				# A fresh StandardMaterial3D per surface per instance made
				# every nature prop its own draw-state (hundreds of unique
				# RIDs in the lagoon, defeating batching, re-allocated on
				# every arena entry). All other params are constants, so the
				# final pastel color is the whole visual identity of the mat.
				var pc: Color = _pastel(col)
				var key: int = pc.to_rgba32()
				var nm: StandardMaterial3D = _nature_mats.get(key)
				if nm == null:
					nm = StandardMaterial3D.new()
					nm.albedo_color = pc
					nm.roughness = 1.0
					nm.metallic_specular = 0.1
					_nature_mats[key] = nm
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
					# One shared override per source material, cached on main.
					# A per-node duplicate's only ref is the node itself, and
					# node teardown frees the material RID before the instance
					# RID — the headless dummy renderer then enumerates the
					# stale RID and spams "Parameter material is null" (probe
					# audit). The cache keeps the override alive past the node.
					var m2: StandardMaterial3D = _toon_mats.get(sm0)
					if m2 == null:
						m2 = (sm0 as StandardMaterial3D).duplicate() as StandardMaterial3D
						m2.normal_enabled = false
						m2.roughness = 1.0
						m2.metallic = 0.0
						m2.metallic_specular = 0.1
						m2.albedo_color = _pastel(m2.albedo_color)
						_toon_mats[sm0] = m2
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
const LAGOON_RIVER_DEPTH := 15.5   # deeper bed, unchanged waterline: enough room for Roshan to swim at every capped rapid
const LAGOON_RIVER_MIN_DEPTH := 4.3
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

func water_surface_y(x: float, z: float) -> float:
	# Local waterline for the player: below this height she is in water (swim
	# rules + swim animation), above it she is on land / in air. 1e18 means
	# water everywhere (underwater arenas keep their behavior); -1e18 means
	# bone dry. Mirrors ReefPhysics.World.water_y so a later physics pass can
	# feed the same oracle straight into the LAND medium.
	if game == "":
		return WATER_TOP
	if lagoon_floor:
		# dry meadow, except down inside the carved river / moat channels,
		# whose surfaces sit a couple of units under the bank rim
		var lx: float = x - LEVEL2_POS.x
		var lz: float = z - LEVEL2_POS.z
		var dip: float = _lagoon_river_dip(lx, lz) + _lagoon_moat_dip(lx, lz)
		if dip <= 2.0:
			return -1e18
		return lagoon_h(x, z) + dip - 2.0
	if northern_floor:
		return NORTHERN_POS.y - 4.8   # the fjord sheets (see _build_fjords)
	if game == "level2" and String(g.get("phase", "")) == "hall":
		return -1e18   # castle interior: dry floors throughout
	return 1e18

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
		var stick_intent := false
		var jv := Vector2(joy_axis(JOY_AXIS_LEFT_X), joy_axis(JOY_AXIS_LEFT_Y))
		if jv.length() > 0.35:   # little thumbs: was 0.45, half-pushed circles count too
			ang = jv.angle()
			ang_ok = true
			stick_intent = true
		elif touch_ui != null and (touch_ui.stick_vec as Vector2).length() > 0.35:
			# The Android virtual stick is the primary control on the target device.
			# Treat circling it exactly like circling a physical stick.
			ang = (touch_ui.stick_vec as Vector2).angle()
			ang_ok = true
			stick_intent = true
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
		var assist: bool = bool(mg.get("motor_assist", false))
		if not assist and stall > 8.0 and stick_intent:
			# A held direction is a deliberate motor alternative after the child has
			# tried for eight seconds. Zero input still makes zero progress.
			assist = true
			mg["motor_assist"] = true
			if voice != null:
				voice.pitch_scale = 1.3
				voice.play()
		if assist and stick_intent:
			mg["rot_acc"] = float(mg["rot_acc"]) + delta * 2.4
		mg["stall"] = stall
		prog = clampf(float(mg["rot_acc"]) / float(mg["rot_need"]), 0.0, 1.0)
		r = lerpf(26.0, float(mg["final_r"]), prog)
		_mg_snow_ball_size(mg["roll_ball"], r, SNOW_ROLL_C)
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
	_play_music("castle_open", false)   # one-shot stinger (6.2s); _tick_cutscene restores prev_track at 5s
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
	_fade_cut(_enter_castle_interior_now.bind(from_back))

func _enter_castle_interior_now(from_back: bool = false) -> void:
	player.visible = true
	_play_music("hall")
	if String(g.get("phase", "")) == "promenade" and _sky_lagoon_promenade != null:
		_sky_lagoon_promenade.teardown()
	g["l2_fish"] = []
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	arena_solids.clear()
	arena_zones.clear()
	fade_walls.clear()
	lagoon_floor = false
	g["phase"] = "hall"
	arena_center = CASTLE_POS
	# The castle interior is exclusively the sprite-card room stage. Keep a
	# harmless hidden player anchor for save/return continuity, but do not
	# construct an Environment, meshes, colliders, lights, or the retired hall.
	arena_dome = 24.0
	arena_ceil = 12.0
	player.position = CASTLE_POS + Vector3(0, 6, 24)
	player.yaw = 0.0
	player.vel = Vector3.ZERO
	var castle_rooms: CastleRooms25D = _castle_rooms_ref()
	castle_rooms.open("main_hall")
	_day_one_discover_dirty_castle()
	var entry_hint := \
		"Follow the one golden rainbow door! Foggy doors are resting until it is their turn." \
		if day_one_is_active() \
		else "Touch a picture door or the shell elevator to visit a room!"
	show_msg("Pearl Castle",
		entry_hint if not from_back
		else "The secret shell door opens into the Main Hall!",
		"home")
	_say("roshan", "talk", 0.5)

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
	_register_castle_light(bl, false)

func _glass_window(pos: Vector3, rot_deg: Vector3, height: float) -> void:
	var pane := MeshInstance3D.new()
	var q := QuadMesh.new()
	# Crop to the actual pointed pane inside the protected source. The source has
	# a baked checkerboard/signature around that pane; a UV silhouette removes it
	# at render time without altering, recompressing, or replacing the image.
	q.size = Vector2(height * 0.61, height)
	pane.mesh = q
	var glass_shader := Shader.new()
	glass_shader.code = "shader_type spatial;\nrender_mode unshaded, cull_disabled;\nuniform sampler2D glass_tex : source_color, filter_linear_mipmap;\nvoid fragment(){\n\tfloat roof_half = mix(0.015, 0.50, clamp(UV.y / 0.16, 0.0, 1.0));\n\tif (abs(UV.x - 0.5) > roof_half) discard;\n\tvec2 src_uv = vec2(mix(0.105, 0.895, UV.x), mix(0.035, 0.965, UV.y));\n\tvec3 c = texture(glass_tex, src_uv).rgb;\n\tALBEDO = c;\n\tEMISSION = c * 0.22;\n}"
	var glass_mat := ShaderMaterial.new()
	glass_mat.shader = glass_shader
	glass_mat.set_shader_parameter("glass_tex", load("res://assets/book/hall/glass_mermaid.png"))
	pane.material_override = glass_mat
	pane.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF   # the quad cast a huge round shadow blob onto the facade
	pane.position = pos
	pane.rotation_degrees = rot_deg
	add_child(pane)
	game_nodes.append(pane)

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

var _light_rig: LightRig = null

func light_rig() -> LightRig:
	# The one place that decides what colour a painted card is multiplied by
	# (LIGHTING_2P5D_AUDIT_2026-08-02 §E2). Painted flats are drawn unshaded,
	# so modulate is the only per-card lever the engine has; this keeps every
	# zone's depth ramp, night wash and accent classes in one table instead of
	# re-invented inline per satellite. Lazily built, so a headless probe that
	# never opens a painted zone never pays for it.
	if _light_rig == null:
		_light_rig = LightRig.new(self)
	return _light_rig

var _castle_rooms_25d: CastleRooms25D = null
var _castle_career_routes: CastleCareerRoutes = null

func _day_one_ref() -> DayOneDirector:
	if _day_one_director == null:
		_day_one_director = DayOneDirector.new(self)
		_day_one_director.hook_event.connect(_on_day_one_hook_event)
	return _day_one_director


## The attack customizer is intentionally loaded lazily. This keeps the main
## boot path independent of the optional art-room overlay while still giving
## every combat mode one owner-facing entry point.
func _attack_customizer_ref() -> AttackCustomizer:
	if _attack_customizer != null and is_instance_valid(_attack_customizer):
		return _attack_customizer
	if _attack_customizer_layer == null or not is_instance_valid(_attack_customizer_layer):
		_attack_customizer_layer = CanvasLayer.new()
		_attack_customizer_layer.name = "AttackCustomizerLayer"
		# Castle rooms own opaque layer 14 and their controls reach layer 16.
		# This modal must remain above both while it owns the child's touch.
		_attack_customizer_layer.layer = 18
		add_child(_attack_customizer_layer)
	_attack_customizer = AttackCustomizerLogic.new() as AttackCustomizer
	_attack_customizer_layer.add_child(_attack_customizer)
	_attack_customizer.attach(self)
	return _attack_customizer


func _open_attack_customizer(on_confirm: Callable = Callable()) -> bool:
	var customizer: AttackCustomizer = _attack_customizer_ref()
	if customizer == null or not customizer.has_method("open"):
		return false
	var result: Variant = customizer.call("open", on_confirm)
	return bool(result) if result is bool else true


func _close_attack_customizer() -> void:
	if _attack_customizer != null and is_instance_valid(_attack_customizer) \
			and _attack_customizer.has_method("close"):
		_attack_customizer.call("close")


func set_attack_profile(next_color: Color, next_effect: String) -> bool:
	var effect: String = next_effect.strip_edges().to_lower()
	if effect not in ["bubbles", "splashes"]:
		effect = "bubbles"
	attack_color = Color(
		clampf(next_color.r, 0.0, 1.0),
		clampf(next_color.g, 0.0, 1.0),
		clampf(next_color.b, 0.0, 1.0),
		clampf(next_color.a, 0.0, 1.0))
	attack_effect = effect
	_queue_save()
	return true


func _open_day_one_art_studio() -> bool:
	if castle_room_stage == null or castle_room_id != "craft_room" \
			or not day_one_is_active() \
			or _day_one_ref().is_room_completed("art"):
		return false
	if _day_one_art_studio != null and is_instance_valid(_day_one_art_studio):
		_day_one_art_studio.refresh_from_state()
		return true
	_day_one_art_studio = DayOneArtStudioLogic.new() as DayOneArtStudio
	castle_room_stage.add_child(_day_one_art_studio)
	_day_one_art_studio.setup(self)
	if castle_room_action_button != null:
		castle_room_action_button.visible = false
	return true


func _close_day_one_art_studio() -> void:
	if _day_one_art_studio != null and is_instance_valid(_day_one_art_studio):
		_day_one_art_studio.teardown()
	_day_one_art_studio = null


func day_one_is_active() -> bool:
	return _day_one_ref().day_one_active

func day_one_jobs_locked() -> bool:
	return day_one_is_active() and _day_one_ref().jobs_are_globally_locked()

func day_one_opera_enabled() -> bool:
	return not day_one_is_active() or _day_one_ref().can_start_opera()

func day_one_boss_door_ready() -> bool:
	var director: DayOneDirector = _day_one_ref()
	return day_one_is_active() and director.boss_door_glow \
		and not director.giant_dust_bunny_boss_triggered

func day_one_castle_room_is_clean(castle_room: String) -> bool:
	var logical_room: String = String(DAY_ONE_CASTLE_ROOM_IDS.get(
		castle_room, ""))
	return logical_room != "" \
		and _day_one_ref().is_dust_bunny_cleaned(logical_room)

func day_one_can_enter_castle_room(castle_room: String) -> bool:
	if not day_one_is_active() or castle_room == "main_hall":
		return true
	var logical_room: String = String(DAY_ONE_CASTLE_ROOM_IDS.get(
		castle_room, ""))
	return logical_room != "" and _day_one_ref().can_enter_room(logical_room)

func day_one_try_enter_castle_room(castle_room: String) -> bool:
	if day_one_can_enter_castle_room(castle_room):
		return true
	show_msg("Daddy Mermaid",
		"That door is resting. Follow the glowing picture door together!",
		"hint")
	_say("roshan", "talk", 0.8)
	return false

func day_one_activate_castle_room(castle_room: String) -> bool:
	if not day_one_is_active():
		return false
	var logical_room: String = String(DAY_ONE_CASTLE_ROOM_IDS.get(
		castle_room, ""))
	if logical_room == "":
		show_msg("Daddy Mermaid",
			"The castle jobs are resting today. First, let's clean together!",
			"hint")
		_say("roshan", "talk", 0.8)
		return true
	var director: DayOneDirector = _day_one_ref()
	if director.is_room_completed(logical_room):
		show_msg("Roshan", "This room is sparkly clean!", "win")
		_say("roshan", "talk", 0.6)
		return true
	if logical_room == "bathroom":
		_sync_day_one_bathroom_cleanup()
		return true
	if logical_room == "pool":
		_castle_rooms_ref().start_day_one_pool_cleanup()
		return true
	if logical_room == "stuffie":
		if not bool(stuffie_wins.get("rescued_eagle", false)):
			show_msg("Baby Eagle",
				"Bump both dust bunnies away first! I know you can do it!",
				"talk")
			_say("roshan", "talk", 0.8)
		else:
			day_one_complete_stuffie_rescue()
		return true
	if logical_room == "art":
		if director.art_customization_completed:
			day_one_complete_art_scene()
		else:
			_open_day_one_art_studio()
		return true
	if not director.complete_placeholder(logical_room):
		show_msg("Daddy Mermaid",
			"Let's finish the glowing room before opening another door!",
			"hint")
		_say("roshan", "talk", 0.8)
		return true
	_castle_rooms_ref().apply_day_one_cleanup(castle_room)
	_day_one_sync_castle_dressing()
	_write_save()
	if director.boss_door_glow:
		_day_one_arm_boss_door()
		show_msg("Roshan",
			"All four rooms are clean! The big back door is glowing!",
			"win")
	else:
		show_msg("Roshan",
			"Dust bunnies cleaned up! A new picture door is glowing!",
			"win")
	_say("roshan", "talk", 0.8)
	return true

func day_one_record_bathroom_cleanup_step(step: int) -> void:
	if not day_one_is_active():
		return
	day_one_bathroom_cleanup_step = clampi(maxi(
		day_one_bathroom_cleanup_step, step), 0, 3)
	_queue_save()

func day_one_record_bathroom_supply_step(step: int) -> void:
	if not day_one_is_active():
		return
	day_one_bathroom_supply_hunt_step = clampi(maxi(
		day_one_bathroom_supply_hunt_step, step), 0, 2)
	if day_one_bathroom_supply_hunt_step >= 2:
		day_one_bathroom_tools_authorized = true
	_queue_save()


## The basket is the single authorization point for the two cleaning tools.
## The old hunt-step key is advanced for save compatibility; new callers can
## use this idempotent seam without reviving a cabinet hunt.
func day_one_authorize_bathroom_tools() -> bool:
	if not day_one_is_active() \
			or _day_one_ref().current_room_id != "bathroom" \
			or _day_one_ref().is_room_completed("bathroom"):
		return false
	if day_one_bathroom_tools_authorized:
		return true
	day_one_bathroom_tools_authorized = true
	day_one_bathroom_supply_hunt_step = 2
	_write_save()
	return true

func day_one_complete_bathroom_scene() -> bool:
	if not day_one_is_active():
		return false
	var director: DayOneDirector = _day_one_ref()
	if director.is_room_completed("bathroom"):
		return false
	# The pool unlock is downstream of both the ordered supply hunt and the two
	# live cleaning gestures. A stale or partial save must never skip either.
	if not day_one_bathroom_tools_authorized \
			or day_one_bathroom_supply_hunt_step < 2 \
			or day_one_bathroom_cleanup_step < 2:
		return false
	if not director.complete_tutorial("bathroom"):
		return false
	day_one_bathroom_cleanup_step = 3
	day_one_bathroom_supply_hunt_step = 2
	_castle_rooms_ref().apply_day_one_cleanup("bubble_bath")
	_day_one_sync_castle_dressing()
	_write_save()
	_start_day_one_bathroom_movie_handoff()
	_show_day_one_pool_route()
	return true


func day_one_record_art_cleanup(kind: String, item_id: String) -> bool:
	if not day_one_is_active() or _day_one_ref().current_room_id != "art":
		return false
	var changed: bool = _day_one_ref().record_art_cleanup(kind, item_id)
	if changed:
		_queue_save()
	return changed


func day_one_complete_art_customization() -> bool:
	if not day_one_is_active() or _day_one_ref().current_room_id != "art":
		return false
	var changed: bool = _day_one_ref().complete_art_customization()
	if changed:
		_write_save()
	return changed


func day_one_complete_art_scene() -> bool:
	if not day_one_is_active():
		return false
	var director: DayOneDirector = _day_one_ref()
	if not director.complete_art_studio():
		return false
	_close_day_one_art_studio()
	_castle_rooms_ref().apply_day_one_cleanup("craft_room")
	_day_one_sync_castle_dressing()
	_write_save()
	return true


func day_one_record_pool_cleanup_step(step: int) -> void:
	if not day_one_is_active():
		return
	day_one_pool_cleanup_step = clampi(maxi(
		day_one_pool_cleanup_step, step), 0, 4)
	_queue_save()


func day_one_record_pool_activity_progress(
		skimmer_mask: int, waterfall_mask: int, seahorse_tugs: int) -> void:
	if not day_one_is_active():
		return
	day_one_pool_skimmer_mask |= skimmer_mask & 0x3F
	day_one_pool_waterfall_mask |= waterfall_mask & 0x07
	day_one_pool_seahorse_tugs = clampi(maxi(
		day_one_pool_seahorse_tugs, seahorse_tugs), 0, 8)
	_queue_save()

func day_one_complete_pool_scene() -> bool:
	if not day_one_is_active():
		return false
	var director: DayOneDirector = _day_one_ref()
	if director.is_room_completed("pool"):
		return false
	day_one_pool_cleanup_step = 4
	day_one_pool_rumi_met = true
	day_one_pool_skimmer_mask = 0x3F
	day_one_pool_waterfall_mask = 0x07
	day_one_pool_seahorse_tugs = 8
	if not director.complete_activity("pool", "pool_activity"):
		return false
	_castle_rooms_ref().apply_day_one_cleanup("mermaid_pool")
	_day_one_sync_castle_dressing()
	_write_save()
	return true

func day_one_complete_stuffie_rescue() -> bool:
	if not day_one_is_active() \
			or not bool(stuffie_wins.get("rescued_eagle", false)):
		return false
	var director: DayOneDirector = _day_one_ref()
	if director.is_room_completed("stuffie") \
			or not director.complete_activity("stuffie", "stuffie_activity"):
		return false
	_castle_rooms_ref().apply_day_one_cleanup("playroom")
	_day_one_sync_castle_dressing()
	_write_save()
	return true

func _day_one_begin_arrival() -> void:
	if day_one_is_active():
		_day_one_ref().trigger_arrival_plane_media()

func _day_one_discover_dirty_castle() -> void:
	if not day_one_is_active():
		return
	_day_one_ref().discover_dirty_castle()
	_day_one_attach_castle_dressing()
	_day_one_arm_boss_door()

func _day_one_attach_castle_dressing() -> void:
	if not day_one_is_active() or castle_room_stage == null:
		return
	if day_one_castle_dressing == null \
			or not is_instance_valid(day_one_castle_dressing):
		day_one_castle_dressing = DayOneCastleDressing.create_dressing(
			castle_room_stage)
		day_one_castle_dressing.name = "DayOneDirtyCastleDressing"
		day_one_castle_dressing.z_index = 20
	_day_one_sync_castle_dressing()

func _day_one_sync_castle_dressing() -> void:
	_sync_day_one_art_studio()
	if day_one_castle_dressing == null \
			or not is_instance_valid(day_one_castle_dressing):
		return
	var director: DayOneDirector = _day_one_ref()
	var room_dirty: Dictionary = {}
	var door_unlocked: Dictionary = {}
	for castle_room_value: Variant in DAY_ONE_CASTLE_ROOM_IDS.keys():
		var castle_room: String = String(castle_room_value)
		var logical_room: String = String(DAY_ONE_CASTLE_ROOM_IDS[castle_room])
		room_dirty[castle_room] = not director.is_dust_bunny_cleaned(logical_room)
		door_unlocked[castle_room] = director.can_enter_room(logical_room)
	day_one_castle_dressing.update_dressing(0.0, {
		"room_dirty": room_dirty,
		"door_unlocked": door_unlocked,
		"boss_back_door_active": director.boss_door_glow,
		"visible_room_id": castle_room_id,
	})
	if _castle_rooms_25d != null and _castle_rooms_25d.is_open():
		_castle_rooms_25d.refresh_door_states()


func _sync_day_one_bathroom_cleanup() -> void:
	var should_show: bool = day_one_is_active() \
			and castle_room_stage != null \
			and castle_room_id == "bubble_bath" \
			and not day_one_castle_room_is_clean("bubble_bath")
	var bathroom_route_owned: bool = day_one_is_active() \
			and castle_room_stage != null \
			and castle_room_id == "bubble_bath" \
			and _day_one_ref().is_room_completed("bathroom")
	if not should_show:
		_clear_day_one_bathroom_cleanup()
		if castle_room_id != "bubble_bath":
			_clear_day_one_pool_route()
		if bathroom_route_owned:
			_suspend_day_one_bathroom_controls()
		else:
			_restore_day_one_bathroom_controls()
		return
	_suspend_day_one_bathroom_controls()
	if _day_one_bathroom_cleanup != null \
			and is_instance_valid(_day_one_bathroom_cleanup):
		if castle_room_action_button != null:
			castle_room_action_button.visible = false
		return
	_day_one_bathroom_cleanup = DayOneBathroomCleanupLogic.new() \
		as DayOneBathroomCleanup
	castle_room_stage.add_child(_day_one_bathroom_cleanup)
	_day_one_bathroom_cleanup.cleanup_step_completed.connect(
		_on_day_one_bathroom_cleanup_step)
	_day_one_bathroom_cleanup.supply_hunt_completed.connect(
		_on_day_one_bathroom_supply_hunt_completed)
	_day_one_bathroom_cleanup.finale_started.connect(
		_on_day_one_bathroom_finale_started)
	_day_one_bathroom_cleanup.cleanup_completed.connect(
		_on_day_one_bathroom_cleanup_completed)
	_day_one_bathroom_cleanup.setup(self)
	# The bespoke rescue owns the visible dirt and its one active touch target.
	# Hide generic Day One dressing so the first lesson stays visually simple.
	if day_one_castle_dressing != null \
			and is_instance_valid(day_one_castle_dressing):
		day_one_castle_dressing.set_visible_room("main_hall")
	_castle_rooms_ref()._position_player_at_foot(Vector2(790.0, 630.0), false)
	if castle_room_action_button != null:
		castle_room_action_button.visible = false


func _clear_day_one_bathroom_cleanup() -> void:
	if _day_one_bathroom_cleanup != null \
			and is_instance_valid(_day_one_bathroom_cleanup):
		_day_one_bathroom_cleanup.teardown()
	_day_one_bathroom_cleanup = null


func _on_day_one_bathroom_cleanup_step(step: int, cleanup_id: String) -> void:
	day_one_record_bathroom_cleanup_step(step)
	g["day_one_bathroom_last_cleanup"] = cleanup_id


func _on_day_one_bathroom_supply_hunt_completed() -> void:
	# This is only the handoff to the sink/tub gestures. Room completion and
	# pool unlock still require day_one_complete_bathroom_scene().
	if _day_one_bathroom_cleanup != null \
			and is_instance_valid(_day_one_bathroom_cleanup):
		_day_one_bathroom_cleanup.begin_cleaning_handoff()
	g["day_one_bathroom_supply_hunt_complete"] = true


func _on_day_one_bathroom_finale_started() -> void:
	# The bespoke rescue owns fixture-associated sparkle sprites. Do not add the
	# Castle-wide center-floor burst here: it obscures the clean sink/tub result.
	pass


func _on_day_one_bathroom_cleanup_completed() -> void:
	if not day_one_complete_bathroom_scene():
		return
	_clear_day_one_bathroom_cleanup()
	_day_one_sync_castle_dressing()


func _sync_day_one_art_studio() -> void:
	var should_show: bool = day_one_is_active() \
		and castle_room_stage != null \
		and castle_room_id == "craft_room" \
		and not _day_one_ref().is_room_completed("art")
	if should_show:
		_open_day_one_art_studio()
	else:
		_close_day_one_art_studio()


func _day_one_clear_castle_dressing() -> void:
	_clear_day_one_bathroom_cleanup()
	_clear_day_one_bathroom_movie_handoff()
	_day_one_bathroom_movie_handoff_pending = false
	_clear_day_one_pool_route()
	_restore_day_one_bathroom_controls()
	_close_day_one_art_studio()
	if day_one_castle_dressing != null \
			and is_instance_valid(day_one_castle_dressing):
		day_one_castle_dressing.teardown()
	day_one_castle_dressing = null


func _clear_day_one_bathroom_movie_handoff() -> void:
	if _day_one_bathroom_movie_handoff != null \
			and is_instance_valid(_day_one_bathroom_movie_handoff):
		_day_one_bathroom_movie_handoff.stop()
		_day_one_bathroom_movie_handoff.queue_free()
	_day_one_bathroom_movie_handoff = null
	_day_one_bathroom_movie_handoff_pending = false


func _start_day_one_bathroom_movie_handoff() -> void:
	if not day_one_is_active() or _day_one_bathroom_movie_handoff != null \
			or castle_room_stage == null:
		return
	_day_one_bathroom_movie_handoff_pending = false
	_suspend_day_one_bathroom_controls()
	_day_one_bathroom_movie_handoff = DayOneBathroomMovieHandoffLogic.new() \
		as DayOneBathroomMovieHandoff
	castle_room_stage.add_child(_day_one_bathroom_movie_handoff)
	_day_one_bathroom_movie_handoff.setup(self)
	var handoff: Dictionary = \
		_day_one_bathroom_movie_handoff.start_after_completion()
	var status: String = String(handoff.get("status", ""))
	if status == "save_pending":
		_day_one_bathroom_movie_handoff_pending = true
	elif status == "fallback":
		_day_one_bathroom_movie_handoff.stop()
		_day_one_bathroom_movie_handoff.queue_free()
		_day_one_bathroom_movie_handoff = null


func _show_day_one_pool_route() -> void:
	if not day_one_is_active() or castle_room_stage == null \
			or not _day_one_ref().can_enter_room("pool"):
		return
	if _day_one_bathroom_movie_handoff_pending \
			or _day_one_bathroom_movie_is_playing():
		return
	# The pool picture is still a Day One bathroom-owned presentation. Keep the
	# generic action/elevator controls out of its touch area until the picture is
	# consumed and show_room() transfers ownership to the next room.
	_suspend_day_one_bathroom_controls()
	if _day_one_pool_route_button != null \
			and is_instance_valid(_day_one_pool_route_button):
		_day_one_pool_route_button.visible = true
		return
	_day_one_pool_route_button = Button.new()
	_day_one_pool_route_button.name = "DayOnePoolRoute"
	_day_one_pool_route_button.text = ""
	_day_one_pool_route_button.tooltip_text = "Sparkle Pool"
	_day_one_pool_route_button.position = Vector2(1035.0, 455.0)
	_day_one_pool_route_button.size = Vector2(205.0, 190.0)
	_day_one_pool_route_button.z_index = 44
	_day_one_pool_route_button.flat = true
	_day_one_pool_route_button.focus_mode = Control.FOCUS_NONE
	_day_one_pool_route_button.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_day_one_pool_route_button.set_meta("day_one_route_target", "mermaid_pool")
	_day_one_pool_route_button.set_meta("real_navigation_control", true)
	_day_one_pool_route_button.set_meta("route_preview_kind",
		"actual_pool_room")
	_day_one_pool_route_button.set_meta("route_preview_asset",
		DAY_ONE_POOL_ROUTE_PREVIEW_TEXTURE)
	_day_one_pool_route_button.pressed.connect(_open_day_one_pool_route)
	var empty_style := StyleBoxEmpty.new()
	_day_one_pool_route_button.add_theme_stylebox_override("normal", empty_style)
	_day_one_pool_route_button.add_theme_stylebox_override("hover", empty_style)
	_day_one_pool_route_button.add_theme_stylebox_override("pressed", empty_style)
	_day_one_pool_route_button.add_theme_stylebox_override("focus", empty_style)
	var pool_picture := Sprite2D.new()
	pool_picture.name = "ApprovedPoolRoomPreview"
	pool_picture.texture = load(DAY_ONE_POOL_ROUTE_PREVIEW_TEXTURE) as Texture2D
	# Keep the complete 16:9 room visible inside the transparent route target.
	# Sprite2D avoids TextureRect's live stretch/crop interaction on the Canvas.
	pool_picture.centered = true
	pool_picture.position = Vector2(102.5, 95.0)
	pool_picture.scale = Vector2.ONE * 0.18
	pool_picture.region_enabled = false
	pool_picture.set_meta("approved_pool_room_preview", true)
	pool_picture.set_meta("actual_destination_room", "mermaid_pool")
	pool_picture.set_meta("uniform_preview_scale", 0.18)
	_day_one_pool_route_button.add_child(pool_picture)
	var hand := Sprite2D.new()
	hand.name = "PoolRouteGhostHand"
	hand.texture = load("res://assets/castle/training/ghost_hand.png") as Texture2D
	hand.position = Vector2(168.0, 12.0)
	hand.scale = Vector2.ONE * 0.13
	hand.z_index = 1
	hand.set_meta("visual_pointer", true)
	_day_one_pool_route_button.add_child(hand)
	var pointer_tween: Tween = hand.create_tween().set_loops()
	pointer_tween.tween_property(hand, "position:y", 26.0, 0.42) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	pointer_tween.tween_property(hand, "position:y", 12.0, 0.42) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	castle_room_stage.add_child(_day_one_pool_route_button)
	show_msg("Roshan", "The sparkle pool is ready! Tap the pool picture!", "win")
	_say("roshan", "talk", 0.8)


func _sync_day_one_pool_route() -> void:
	var bathroom_rescue_active: bool = day_one_is_active() \
			and castle_room_stage != null \
			and castle_room_id == "bubble_bath" \
			and not _day_one_ref().is_room_completed("bathroom")
	if not day_one_is_active() or castle_room_stage == null \
			or castle_room_id != "bubble_bath" \
			or not _day_one_ref().is_room_completed("bathroom"):
		_clear_day_one_pool_route()
		if castle_room_id != "bubble_bath":
			_clear_day_one_bathroom_movie_handoff()
		if bathroom_rescue_active:
			_suspend_day_one_bathroom_controls()
		else:
			_restore_day_one_bathroom_controls()
		return
	if _day_one_bathroom_movie_handoff_pending \
			and not save_dirty and not save_pending \
			and _day_one_bathroom_movie_handoff != null \
			and is_instance_valid(_day_one_bathroom_movie_handoff):
		var handoff: Dictionary = \
			_day_one_bathroom_movie_handoff.start_after_completion()
		var status: String = String(handoff.get("status", ""))
		if status != "save_pending":
			_day_one_bathroom_movie_handoff_pending = false
			if status == "fallback":
				_day_one_bathroom_movie_handoff.stop()
				_day_one_bathroom_movie_handoff.queue_free()
				_day_one_bathroom_movie_handoff = null
	if _day_one_bathroom_movie_handoff_pending \
			or _day_one_bathroom_movie_is_playing():
		_suspend_day_one_bathroom_controls()
		return
	_suspend_day_one_bathroom_controls()
	_show_day_one_pool_route()


func _day_one_bathroom_movie_is_playing() -> bool:
	if _day_one_bathroom_movie_handoff == null \
			or not is_instance_valid(_day_one_bathroom_movie_handoff):
		return false
	return bool(_day_one_bathroom_movie_handoff.audit_snapshot().get(
		"player_active", false))


func _day_one_bathroom_navigation_controls() -> Array[Control]:
	var controls: Array[Control] = []
	var candidates: Array[Node] = [
		castle_room_action_button,
		castle_room_back_button,
		castle_room_stage.get_node_or_null("ElevatorButton") \
			if castle_room_stage != null else null,
		castle_room_stage.get_node_or_null("ElevatorPointer") \
			if castle_room_stage != null else null,
		castle_room_menu_panel,
	]
	for candidate: Node in candidates:
		var control: Control = candidate as Control
		if control != null and is_instance_valid(control) \
				and not controls.has(control):
			controls.append(control)
	return controls


func _suspend_day_one_bathroom_controls() -> void:
	var controls: Array[Control] = _day_one_bathroom_navigation_controls()
	if not _day_one_bathroom_controls_suspended:
		_day_one_bathroom_control_state.clear()
		_day_one_bathroom_menu_was_open = castle_room_menu_open
		for control: Control in controls:
			var button: BaseButton = control as BaseButton
			_day_one_bathroom_control_state.append({
				"control": control,
				"visible": control.visible,
				"mouse_filter": control.mouse_filter,
				"disabled": button.disabled if button != null else false,
			})
		_day_one_bathroom_controls_suspended = true
	for control: Control in controls:
		control.visible = false
		control.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var button: BaseButton = control as BaseButton
		if button != null:
			button.disabled = true
	castle_room_menu_open = false
	_set_world_controls_enabled(false, "day_one_bathroom_lifecycle")


func _restore_day_one_bathroom_controls() -> void:
	if not _day_one_bathroom_controls_suspended:
		return
	for state: Dictionary in _day_one_bathroom_control_state:
		var control: Control = state.get("control") as Control
		if control == null or not is_instance_valid(control):
			continue
		control.visible = bool(state.get("visible", true))
		control.mouse_filter = int(state.get("mouse_filter",
			Control.MOUSE_FILTER_STOP))
		var button: BaseButton = control as BaseButton
		if button != null:
			button.disabled = bool(state.get("disabled", false))
	_day_one_bathroom_control_state.clear()
	_day_one_bathroom_controls_suspended = false
	castle_room_menu_open = _day_one_bathroom_menu_was_open
	_set_world_controls_enabled(true, "day_one_bathroom_lifecycle")


func _clear_day_one_pool_route() -> void:
	if _day_one_pool_route_button != null \
			and is_instance_valid(_day_one_pool_route_button):
		_day_one_pool_route_button.queue_free()
	_day_one_pool_route_button = null


func _open_day_one_pool_route() -> void:
	if not day_one_is_active() or not _day_one_ref().can_enter_room("pool"):
		return
	_clear_day_one_pool_route()
	if _castle_rooms_ref().is_open():
		_castle_rooms_ref().show_room("mermaid_pool", true)

func _day_one_arm_boss_door() -> void:
	var director: DayOneDirector = _day_one_ref()
	if not day_one_is_active() or not director.boss_door_glow \
			or director.giant_dust_bunny_boss_triggered:
		return
	_castle_rooms_ref().arm_royal_hall_event(
		"day_one_giant_dust_bunny", _day_one_trigger_boss)

func _day_one_trigger_boss() -> void:
	_day_one_ref().trigger_giant_dust_bunny_boss()

func _on_day_one_hook_event(event_name: String, payload: Dictionary) -> void:
	g["day_one_last_event"] = event_name
	match event_name:
		DayOneDirector.EVENT_ARRIVAL_PLANE_MEDIA:
			# The Grok render is a handoff contract, not an imported runtime asset.
			# Keep the request explicit while the existing pearl-plane animation is
			# the safe in-engine fallback.
			g["day_one_media_request"] = "grok_opening_flight"
		DayOneDirector.EVENT_DIRTY_CASTLE_DISCOVERY:
			g["day_one_castle_dirty"] = true
		DayOneDirector.EVENT_GROK_VIDEO_2:
			g["day_one_media_request"] = "grok_dirty_castle_video_2"
			show_msg("Roshan",
				"Dust bunnies! This castle needs our help!", "talk")
		DayOneDirector.EVENT_DUST_BUNNY_CLEANUP:
			g["day_one_cleaned_room"] = String(payload.get("room_id", ""))
		DayOneDirector.EVENT_ART_DESK_UNLOCKED:
			g["day_one_art_desk_unlocked"] = true
		DayOneDirector.EVENT_ART_CUSTOMIZATION_COMPLETED:
			g["day_one_art_customization_completed"] = true
		DayOneDirector.EVENT_BOSS_DOOR_GLOW:
			_day_one_arm_boss_door()
		DayOneDirector.EVENT_GIANT_DUST_BUNNY_BOSS:
			_write_save()
			if _castle_rooms_25d != null and _castle_rooms_25d.is_open():
				_castle_rooms_25d.close()
			_start_game(dust_boss_fr)
	_queue_save()

func _castle_rooms_ref() -> CastleRooms25D:
	if _castle_rooms_25d == null:
		_castle_rooms_25d = CastleRooms25D.new(self)
	return _castle_rooms_25d

func _castle_career_routes_ref() -> CastleCareerRoutes:
	if _castle_career_routes == null:
		_castle_career_routes = CastleCareerRoutes.new(self)
	return _castle_career_routes

func _castle_room_music_track(room_id: String) -> String:
	# CastleRooms25D is protected by a hash-backed visual approval ledger, so
	# its soundtrack follows the room-state naming contract from this owner.
	return "hall" if room_id == "main_hall" else "castle_" + room_id

func _sync_castle_room_music() -> void:
	# Suspended Castle cutaways hide the layer; picture games set mg_kind. Both
	# own their temporary cue and must be allowed to restore it before the live
	# room resumes soundtrack ownership.
	if castle_room_layer == null or not is_instance_valid(castle_room_layer) \
			or not castle_room_layer.visible or mg_kind != "":
		return
	var room_track: String = _castle_room_music_track(castle_room_id)
	if cur_track != room_track:
		_play_music(room_track)

func _tick_castle_rooms(delta: float) -> void:
	# Phase "hall" now means the sprite-card castle exclusively. If an
	# activity teardown returned without resuming its overlay, restore it here
	# instead of falling back to the retired free-roaming 3D hall.
	if not _castle_rooms_ref().is_open():
		_castle_rooms_ref().open("main_hall")
	_sync_castle_room_music()
	_castle_rooms_ref().tick(delta)
	_sync_day_one_bathroom_cleanup()
	_sync_day_one_pool_route()
	_castle_career_routes_ref().sync()

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
	# art pass 3.5 made the bars GLB props — the root Node3D has no
	# material_override, so the burst color comes from the bell dict
	_sparkle_burst(bn.position + Vector3(0, 4, 0), Color(bd.get("color", Color(1.0, 0.9, 0.55))))

func _tick_bellgame(bg2: Dictionary, delta: float, ppos: Vector3) -> void:
	if bg2.is_empty():
		return
	bg2["cool"] = maxf(0.0, float(bg2["cool"]) - delta)
	var st := String(bg2["state"])
	if st == "idle":
		if not touch_uses_explicit_interactions() and float(bg2["cool"]) <= 0.0 and g.has("song_star") and (g["song_star"] as Vector3).distance_to(ppos) < 5.0:
			_start_bellgame(bg2)
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
				_populate_touch_interactables()

func _start_bellgame(bg2: Dictionary) -> void:
	if bg2.is_empty() or String(bg2.get("state", "")) != "idle" or float(bg2.get("cool", 0.0)) > 0.0:
		return
	bg2["round"] = 0
	bg2["oops"] = 0
	show_msg("Music Room", "The bells want to sing you a song! Listen... then copy it!")
	_bellgame_new_round(bg2)

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
	_populate_touch_interactables()

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
				_medal_ref().award_stats("bells", {"oops": int(bg2.get("oops", 0))})
				show_msg("Music Room", "You played the WHOLE bell song! +2 rainbow pearls!", "win")
				_populate_touch_interactables()
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
		bg2["oops"] = int(bg2.get("oops", 0)) + 1
		bg2["state"] = "play"
		bg2["i"] = 0
		bg2["t"] = 1.2
		_populate_touch_interactables()

func _begin_sleep() -> void:
	# tuck-in cutscene: Roshan snuggles onto the bed, Zzz's float up, the screen
	# fades, day flips to night (or night to day), and she wakes refreshed
	if sleep_t >= 0.0:
		return
	_set_world_controls_enabled(false, "sleep")
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
		show_msg("Roshan", "Good morning! The sun is shining over the ocean again!", "win")
	_set_world_controls_enabled(true, "sleep")

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
		arena_env.background_color = Color(0.48, 0.70, 0.90)
		arena_env.ambient_light_color = Color(0.88, 0.90, 1.0)
		arena_env.ambient_light_energy = 0.62
		_apply_scene_grade(arena_env, "bright_pastel")
	# flashing colored disco lights ringing the play place (this is the RAINBOW slide!)
	var rbc := [Color(1, 0.2, 0.2), Color(1, 0.6, 0.1), Color(1, 0.9, 0.2), Color(0.2, 0.9, 0.3), Color(0.2, 0.5, 1.0), Color(0.6, 0.3, 0.9)]
	for li in range(8):
		var fl := OmniLight3D.new()
		fl.light_energy = 1.25 if quality == "speedy" else 2.0
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
	if _castle_rooms_25d != null and _castle_rooms_25d.is_open():
		_castle_rooms_25d.close()
	player.cam_back = 25.0   # diorama lens default
	player.cam_high = 6.5
	for n in game_nodes:
		if is_instance_valid(n):
			n.queue_free()
	game_nodes.clear()
	_enter_level2(true)

func _play_hug_cutscene() -> void:
	if hug_layer != null:
		return
	_set_world_controls_enabled(false, "hug")
	award_sticker("hug")
	var cl := CanvasLayer.new()
	cl.layer = 20
	add_child(cl)
	hug_layer = cl
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
	dp.stream = load("res://assets/audio/voices/" + ["daddy1", "daddy2", "daddy3"][randi() % 3] + ".ogg")
	dp.bus = "Voice"
	dp.volume_db = 1.5   # was +4: headroom — the hot daddy clip clipped on small phone speakers
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
		if not is_instance_valid(root):
			return
		var fo := root.create_tween()
		fo.tween_property(root, "modulate:a", 0.0, 0.45)
		fo.finished.connect(_end_hug_cutscene))

func _end_hug_cutscene() -> void:
	if hug_layer != null and is_instance_valid(hug_layer):
		hug_layer.queue_free()
	hug_layer = null
	_set_world_controls_enabled(true, "hug")


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

# each craft-studio creature -> its family Meshy mesh + footprint target. All
# three of HER creations are real 3D friends now, recolored in her chosen
# colors by the sway shader (paint_body/paint_fin). Billboards are fallback.
const CRAFT_GEN2 := {"fish": ["clownfish", 1.7], "cat": ["craft_kitty", 3.2], "bird": ["craft_birdie", 2.6]}
# creatures with a real skeleton + gait clips take priority over the static sway
# mesh (kitty -> Chuck's quadruped cage; birdie -> its own standing-bird rig,
# tools/rig_birdie.py). name -> [rigged glb, footprint]
# name -> [rigged glb, footprint, default third colour (the book-art tone:
# kitty's white muzzle+chest bib, birdie's sunny belly)]
const CRAFT_RIGGED := {"cat": ["craft_kitty_rigged", 3.2, Color(0.97, 0.96, 0.93)],
	"bird": ["craft_birdie_rigged", 2.6, Color(1.0, 0.9, 0.45)]}

func _make_creature_node(kind: String, body: Color, accent: Color, body_rb: bool = false, acc_rb: bool = false, third: Color = Color(0, 0, 0, 0)) -> Node3D:
	if CRAFT_RIGGED.has(kind):
		var rspec: Array = CRAFT_RIGGED[kind]
		var c3: Color = third if third.a > 0.0 else (rspec[2] as Color)
		var rn := _gen2_creature_rigged(String(rspec[0]), float(rspec[1]), body, accent, c3)
		if rn != null:
			if body_rb or acc_rb:
				rn.tree_entered.connect(_start_gen2_rainbow.bind(rn, body_rb, acc_rb), CONNECT_ONE_SHOT)
			return rn
	if CRAFT_GEN2.has(kind):
		var spec: Array = CRAFT_GEN2[kind]
		var pf := _gen2_creature(String(spec[0]), Vector3.ZERO, float(spec[1]))
		if pf != null:
			remove_child(pf)   # _gen2_prop parents to main; callers re-parent
			for mi in _all_meshes(pf):
				var mesh: Mesh = mi.mesh
				if mesh == null:
					continue
				for si in range(mesh.get_surface_count()):
					var sm2: Material = mi.get_surface_override_material(si)
					if sm2 is ShaderMaterial:
						(sm2 as ShaderMaterial).set_shader_parameter("paint_mix", 1.0)
						(sm2 as ShaderMaterial).set_shader_parameter("paint_body", body)
						(sm2 as ShaderMaterial).set_shader_parameter("paint_fin", accent)
			pf.set_meta("gen2", true)   # base at origin (billboards are center-origin)
			if body_rb or acc_rb:
				pf.tree_entered.connect(_start_gen2_rainbow.bind(pf, body_rb, acc_rb), CONNECT_ONE_SHOT)
			return pf
	var ln: Array = CREATURE_LAYERS.get(kind, CREATURE_LAYERS["fish"])
	var root := Node3D.new()
	# inner pivot so the idle animation never fights whoever owns root position
	var anim := Node3D.new()
	root.add_child(anim)
	var lb := Sprite3D.new()
	lb.texture = load("res://assets/mg/" + String(ln[1]) + ".png")
	lb.billboard = BaseMaterial3D.BILLBOARD_ENABLED; lb.pixel_size = 0.02; lb.render_priority = 0
	anim.add_child(lb)
	var la := Sprite3D.new()
	la.texture = load("res://assets/mg/" + String(ln[0]) + ".png")
	la.billboard = BaseMaterial3D.BILLBOARD_ENABLED; la.pixel_size = 0.02; la.render_priority = 1
	anim.add_child(la)
	var ll := Sprite3D.new()
	ll.texture = load("res://assets/mg/" + String(ln[2]) + ".png")
	ll.billboard = BaseMaterial3D.BILLBOARD_ENABLED; ll.pixel_size = 0.02; ll.render_priority = 2
	anim.add_child(ll)
	# colors + idle tweens can only start inside the tree, hence the deferred
	# hook (create_tween() errors outside it; this also restores the craft
	# tints the billboard fallback would otherwise render pure white)
	root.tree_entered.connect(_creature_spawned.bind(lb, la, anim, body, accent, body_rb, acc_rb, kind), CONNECT_ONE_SHOT)
	return root

func _start_gen2_rainbow(root: Node3D, body_rb: bool, acc_rb: bool) -> void:
	for mi in _all_meshes(root):
		var mesh: Mesh = mi.mesh
		if mesh == null:
			continue
		for si in range(mesh.get_surface_count()):
			var material: Material = mi.get_surface_override_material(si)
			if not material is ShaderMaterial:
				continue
			var shader_material := material as ShaderMaterial
			if body_rb:
				_loop_paint_rainbow(root, shader_material, "paint_body")
			if acc_rb:
				_loop_paint_rainbow(root, shader_material, "paint_fin")

func _loop_paint_rainbow(owner: Node3D, material: ShaderMaterial, parameter: String) -> void:
	var tw: Tween = owner.create_tween().set_loops()
	for hi in range(7):
		var c0 := Color.from_hsv(float(hi) / 7.0, 0.75, 1.0)
		var c1 := Color.from_hsv(float(hi + 1) / 7.0, 0.75, 1.0)
		tw.tween_method(_set_paint_colour.bind(material, parameter), c0, c1, 0.4)

func _set_paint_colour(colour: Color, material: ShaderMaterial, parameter: String) -> void:
	material.set_shader_parameter(parameter, colour)

func _creature_spawned(lb: Sprite3D, la: Sprite3D, anim: Node3D, body: Color, accent: Color, body_rb: bool, acc_rb: bool, kind: String) -> void:
	_layer_fx(lb, "body", body, body_rb, kind)
	_layer_fx(la, "accent", accent, acc_rb, kind)
	_animate_billboard_creature(anim, la, kind)

func _animate_billboard_creature(anim: Node3D, accent: Sprite3D, kind: String) -> void:
	# idle life for the billboard craft creatures (kitty + birdie in the
	# courtyard; fish only as the strangler-fig fallback). Billboards ignore
	# rotation, so only scale, sprite offset and height read on screen.
	if kind == "cat":
		# soft breathing + a happy little hop every few seconds
		var tw: Tween = anim.create_tween().set_loops()
		tw.tween_property(anim, "scale", Vector3(1.02, 0.975, 1.0), 1.1).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		tw.tween_property(anim, "scale", Vector3(0.985, 1.02, 1.0), 1.1).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		var th: Tween = anim.create_tween().set_loops()
		th.tween_interval(2.2 + randf() * 2.6)
		th.tween_property(anim, "position:y", 1.4, 0.26).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		th.tween_property(anim, "position:y", 0.0, 0.34).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	elif kind == "bird":
		# hovering flit with a quick wing-beat bounce
		var th2: Tween = anim.create_tween().set_loops()
		th2.tween_property(anim, "position:y", 1.2, 1.05).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		th2.tween_property(anim, "position:y", -0.2, 1.05).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		var tf: Tween = anim.create_tween().set_loops()
		tf.tween_property(anim, "scale:y", 0.94, 0.15).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		tf.tween_property(anim, "scale:y", 1.0, 0.15).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	else:
		# fish fallback: swim-kick squash-stretch + fin-layer flutter
		var tw2: Tween = anim.create_tween().set_loops()
		tw2.tween_property(anim, "scale", Vector3(0.93, 1.06, 1.0), 0.45).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		tw2.tween_property(anim, "scale", Vector3(1.06, 0.95, 1.0), 0.45).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		var tf2: Tween = accent.create_tween().set_loops()
		tf2.tween_property(accent, "offset", Vector2(-10.0, 6.0), 0.24).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		tf2.tween_property(accent, "offset", Vector2(6.0, -4.0), 0.24).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)

# the craft studio overlay lives in scripts/craft_studio.gd
# (state stays here; CraftStudio receives main by reference)
var _craft_studio: CraftStudio = null

func _craft_ref() -> CraftStudio:
	if _craft_studio == null:
		_craft_studio = CraftStudio.new(self)
	return _craft_studio

func _open_craft_studio() -> void:
	_craft_ref()._open_craft_studio()

func _craft_done() -> void:
	_craft_ref()._craft_done()

func _close_craft() -> void:
	_craft_ref()._close_craft()

# the castle-logo maker lives on the Craft Room paint table
var _castle_logo_studio: CastleLogoStudio = null

func _castle_logo_ref() -> CastleLogoStudio:
	if _castle_logo_studio == null:
		_castle_logo_studio = CastleLogoStudio.new(self)
	return _castle_logo_studio

func _open_castle_logo() -> void:
	_castle_logo_ref().open()

func _finish_castle_logo() -> void:
	_castle_logo_ref().finish()

func _close_castle_logo() -> void:
	_castle_logo_ref().close(false)

# the wardrobe + sticker book overlays live in scripts/wardrobe_ui.gd
# (state stays here; WardrobeUI receives main by reference)
var _wardrobe_ui: WardrobeUI = null

func _wardrobe_ref() -> WardrobeUI:
	if _wardrobe_ui == null:
		_wardrobe_ui = WardrobeUI.new(self)
	return _wardrobe_ui

func _open_wardrobe() -> void:
	_wardrobe_ref()._open_wardrobe()

func _wardrobe_done() -> void:
	_wardrobe_ref()._wardrobe_done()

func _close_wardrobe() -> void:
	_wardrobe_ref()._close_wardrobe()

func _open_stickers() -> void:
	_wardrobe_ref()._open_stickers()

func _close_stickers() -> void:
	_wardrobe_ref()._close_stickers()

func _exit_level2() -> void:
	_fade_cut(_exit_level2_now)

func _enter_ocean_kingdom(kingdom: String) -> void:
	if kingdom != ReefDistricts.KINGDOM_CARIBBEAN and kingdom != ReefDistricts.KINGDOM_NORWEGIAN:
		kingdom = ReefDistricts.KINGDOM_CARIBBEAN
	_fade_cut(_exit_level2_now.bind(kingdom))

func _exit_level2_now(target_kingdom: String = "") -> void:
	if _castle_rooms_25d != null and _castle_rooms_25d.is_open():
		_castle_rooms_25d.close()
	player.visible = true
	if player.cam != null and player.cam.is_inside_tree():
		player.cam.make_current()
	if sleep_t >= 0.0:
		# Leaving mid-tuck-in (pause -> Leave): _tick_sleep only runs in the
		# hall, so nothing would ever release the "sleep" input block or the
		# indigo dream overlay — every touch control stays dead until an app
		# restart. Unwind the cutscene before tearing the world down.
		sleep_t = -1.0
		sleep_cool = 6.0
		sleep_flip_done = false
		if sleep_layer != null and is_instance_valid(sleep_layer):
			sleep_layer.queue_free()
		sleep_layer = null
		sleep_overlay = null
		if player != null:
			player.rotation_degrees = Vector3.ZERO
		_set_world_controls_enabled(true, "sleep")
	player.cam_back = 25.0   # diorama lens default
	player.cam_high = 6.5
	_tap_move_ref().cancel("sky_canvas_exit")
	_interaction_ref().clear_focus()
	touch_interactables.clear()
	lagoon_trip_return_master_x = -1.0
	game = ""
	if String(g.get("phase", "")) == "promenade" and _sky_lagoon_promenade != null:
		_sky_lagoon_promenade.teardown()
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
	if sun_light != null:
		sun_light.visible = true
	arena_center = ARENA_POS
	arena_dome = 48.0
	arena_ceil = 42.0
	portal_cool = 8.0
	portal_armed = false
	if target_kingdom != "":
		ocean_kingdom = target_kingdom
		ocean_routes_enabled = true
		var entry_xz: Vector2 = ReefDistricts.kingdom_entry_point(ocean_kingdom)
		var destination_xz: Vector2 = ReefDistricts.kingdom_destination_center(ocean_kingdom)
		player.position = Vector3(entry_xz.x,
			seabed_y(entry_xz.x, entry_xz.y) + 6.0, entry_xz.y)
		var into_kingdom: Vector2 = destination_xz - entry_xz
		player.yaw = atan2(into_kingdom.x, into_kingdom.y)
		ocean_return_gate_armed = false
		ocean_return_gate_cool = 2.5
	elif portal_node != null and is_instance_valid(portal_node):
		# beside the seabed portal, resting on the ocean floor (never below it)
		player.position = portal_node.position + Vector3(22, 0, 22)
		player.position.y = seabed_y(player.position.x, player.position.z) + 6.0
	else:
		player.position = return_pos
	player.vel = Vector3.ZERO
	player.snap_cam()   # never lerp the lens across the world gap (CAMERA_AUDIT P0)
	_play_music("world")
	if target_kingdom == ReefDistricts.KINGDOM_NORWEGIAN:
		show_msg("Roshan", "The icy waters of Norway! Follow the blue currents through the kelp and fjord!", "pearl2")
	elif target_kingdom == ReefDistricts.KINGDOM_CARIBBEAN:
		show_msg("Roshan", "The sunny Caribbean! Follow the warm shells and rainbow coral!", "pearl")
	else:
		show_msg("Roshan", "Back in the Reef! I love swimming!", "idle2")

func _finish_level2() -> void:
	_do_finish_level2()

func _do_finish_level2() -> void:
	level2_finishing = false
	player.cam_back = 25.0   # restore the outdoor diorama lens (tightened for the hall)
	player.cam_high = 6.5
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
	if sun_light != null:
		sun_light.visible = true
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
	player.snap_cam()   # never lerp the lens across the world gap (CAMERA_AUDIT P0)
	_play_music("world")
	show_msg("Princess Huluu", "You made it to my Pearl Castle, Roshan! You are the Queen of the Castle now!", "win")

func _beans_go() -> void:
	award_sticker("beans")
	beans_t = 40.0   # long enough to swim from the Pearl Shop to the Penguin Slide
	speed_mult = 2.0
	fart_t = 0.7
	if beans_sfx != null and not beans_sfx.playing:
		beans_sfx.play()
	show_msg("Roshan", "Yummy, beans! ...toot!", "beans")
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
			var d: float = (f["node"] as Node3D).position.distance_to(player.position)
			if d < best:
				best = d
				target = (f["node"] as Node3D).position
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
		var beacon: OmniLight3D = f.get("beacon") as OmniLight3D
		if bool(f["won"]):
			pmat2.albedo_color.a = 0.012
			if beacon != null:
				beacon.light_energy = 0.25
		elif have and (f["node"] as Node3D).position == target:
			pmat2.albedo_color.a = 0.12 + 0.07 * (0.5 + 0.5 * sin(tt2 * 2.4))
			if beacon != null:
				beacon.light_energy = 1.5 + 0.35 * sin(tt2 * 2.4)
		else:
			# idle floor 0.09: actually visible on a phone in daylight, yet the
			# nearest-friend pulse (0.12-0.19) still reads clearly brighter
			pmat2.albedo_color.a = 0.09
			if beacon != null:
				beacon.light_energy = 0.55
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
	_play_music("finale", false)   # one-shot fanfare (42s); _tick_finale brings "world" back at 10s
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
	var closing_melody: bool = game == "melody"
	var closing_slide_canvas: bool = _slide_canvas_fish_route_active()
	var slide_canvas_player_was_visible: bool = bool(
		g.get("slide_canvas_player_was_visible", true))
	var slide_canvas_collection_was_visible: bool = bool(
		g.get("slide_canvas_collection_was_visible", false))
	var slide_canvas_living_was_visible: bool = bool(
		g.get("slide_canvas_living_was_visible", false))
	var slide_canvas_return_camera: Variant = g.get(
		"slide_canvas_return_camera", null)
	var slide_canvas_camera_was_current: bool = bool(
		g.get("slide_canvas_camera_was_current", false))
	var slide_canvas_player_cam_transform: Variant = g.get(
		"slide_canvas_player_cam_transform", null)
	var slide_canvas_player_cam_fov: float = float(
		g.get("slide_canvas_player_cam_fov", 0.0))
	var slide_canvas_player_cam_orbit: float = float(
		g.get("slide_canvas_player_cam_orbit", 0.0))
	var slide_canvas_player_cam_pitch: float = float(
		g.get("slide_canvas_player_cam_pitch", 0.0))
	_game_obj("dolls", DollsGame).stage_close()
	_game_obj("seek", SeekGame).stage_close()
	_game_obj("brawl", BrawlGame).stage_close()
	_game_obj("melody", MelodyGame).stage_close()
	if closing_slide_canvas:
		# Arm while the exact route and its complete held-source census still exist.
		# This distinct return block survives game/g reset and the reveal tween.
		_arm_slide_canvas_return_guard()
		# The Canvas layer must be gone synchronously while its g-backed controller
		# state still exists. No queued frame may survive into the return world.
		(_game_obj("race", SlideRaceGame) as SlideRaceGame).stage_close()
		# Preserve raw fallback levels until the return guard observes their actual
		# terminal neutral boundary; it clears them only when the guard retires.
		_slide_canvas_overlay_axis_wait_neutral = false
		_slide_canvas_overlay_poll_neutral_frames = 0
		# Restore the exact lens the child was looking through. This route never
		# teleports the Reef player, so the generic snap_cam watchdog would be a
		# visible and unnecessary orbit/pitch jump on the first returned frame.
		if player != null and player.cam != null:
			if slide_canvas_player_cam_transform != null:
				player.cam.transform = slide_canvas_player_cam_transform
			if slide_canvas_player_cam_fov > 0.0:
				player.cam.fov = slide_canvas_player_cam_fov
			player.cam_orbit = slide_canvas_player_cam_orbit
			player.cam_pitch_off = slide_canvas_player_cam_pitch
		if slide_canvas_camera_was_current \
				and slide_canvas_return_camera is Node \
				and is_instance_valid(slide_canvas_return_camera) \
				and (slide_canvas_return_camera as Node).is_inside_tree():
			(slide_canvas_return_camera as Node).call(&"make_current")
	_game_obj("dustboss", DustBossGame).stage_close()
	# safety net (alpha audit 2026-08-05): any tween a minigame stashed in g
	# dies WITH the game — a looping tween that outlives its freed target
	# degenerates to a zero-duration loop and errors every frame forever
	for v in g.values():
		if v is Tween and (v as Tween).is_valid():
			(v as Tween).kill()
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
	if closing_melody:
		_set_world_controls_enabled(true, "melody")
	if closing_slide_canvas:
		if player != null:
			player.visible = slide_canvas_player_was_visible
		if collection_button_layer != null:
			collection_button_layer.visible = slide_canvas_collection_was_visible
		if living_layer != null:
			living_layer.visible = slide_canvas_living_was_visible
		_set_world_controls_enabled(true, "slide_canvas")

func _fail_line() -> String:
	# in-character failure lines, by game (the on-screen text; the matching
	# character voice plays via show_msg's "fail" event — drop <speaker>_fail.ogg
	# into assets/audio/voices to use a real recorded clip)
	match game:
		"fetch":      return "Aww... now Chuck is all wet!"
		"dolls":      return "Oh no, the babies!"
		"brawl":      return "The imps are extra giggly today! Huluu says come back soon!"
		"dustboss":   return "The great dust bunny puffed away — he'll bounce back for another game!"
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
	# Sky owns a Canvas contact shadow for its visible actor. Do not construct or
	# expose the generic spatial disc behind that opaque stage.
	if game == "melody" or _slide_canvas_fish_route_active() \
			or _slide_canvas_return_guard_active() \
			or (game == "level2" and String(g.get("phase", "")) == "promenade"):
		if _shadow_disc != null:
			_shadow_disc.visible = false
		return
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
	var celebration_card := StorybookUI.add_hud_panel(cl3, Rect2(350, 40, 580, 170), StorybookUI.GOLD, Color(1.0, 0.97, 0.88, 0.96), 48)
	celebration_card.name = "TrophyCelebrationCard"
	var big := Label.new()
	big.text = "🏆 ⭐ 🏆"
	StorybookUI.style_hud_label(big, 110, StorybookUI.GOLD, 12)
	big.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	big.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	big.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	celebration_card.add_child(big)
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

func _creature_greet(node: Node3D) -> void:
	# the interaction beat: the creature gets EXCITED for ~1.5s - its sway
	# shader speeds up (excite uniform), it does a squash-and-stretch bounce
	# (movers own position, so the bounce lives in scale), plus sparkles and
	# a happy chirp. Works on any mover; pack survivors just skip the shader.
	for mi in _all_meshes(node):
		if mi.mesh == null:
			continue
		for si in range(mi.mesh.get_surface_count()):
			var m0: Material = mi.get_surface_override_material(si)
			if m0 is ShaderMaterial and (m0 as ShaderMaterial).shader != null:
				var sm := m0 as ShaderMaterial
				var tw0 := create_tween()
				tw0.tween_method(func(v: float): sm.set_shader_parameter("excite", v), 0.0, 1.0, 0.25)
				tw0.tween_interval(0.9)
				tw0.tween_method(func(v: float): sm.set_shader_parameter("excite", v), 1.0, 0.0, 0.4)
	var base_scale: Vector3 = node.scale
	var tw := create_tween()
	tw.tween_property(node, "scale", base_scale * Vector3(1.08, 1.2, 1.08), 0.2).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(node, "scale", base_scale, 0.55).set_trans(Tween.TRANS_ELASTIC).set_ease(Tween.EASE_OUT)
	_sparkle_burst(node.position + Vector3(0, 1.6, 0), Color(0.8, 0.95, 1.0))
	if voice != null:
		voice.pitch_scale = 1.35 + randf() * 0.3
		voice.play()

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
	if win:
		# ranked BEFORE _clear_game wipes g — every completion earns at least
		# bronze; MedalSystem persists only upgrades (shop is unranked: no-op)
		_medal_ref().award_from_end_game(game, g)
	if win and not fr["won"]:
		fr["won"] = true
		trophies += 1
		_add_won_star(fr)
		_reward()
		if player != null:
			player.play_verb("cheer")   # R2-C: arms up for the trophy curtain call
	fr["cool"] = 5.0
	# Short re-entry cooldowns: "again!" should take seconds, not sixteen.
	# They only need to outlast the return teleport so the portal doesn't
	# swallow her on the same frame — lingering by choice restarting the game
	# is the feature (starting is a greeting, not a win; probe_passive keeps
	# zero-input play unwinnable regardless of how often a game re-opens).
	if String(fr["fname"]) == "Secret Cave":
		treasure_cool = 4.0
	elif String(fr["fname"]) == "Pearl Shop":
		shop_cool = 4.0
	elif String(fr["fname"]) == "Penguin Slide":
		slide_cool = 3.0
	elif String(fr["fname"]) == "Toy Castle":
		brawl_cool = 3.0
	elif String(fr["fname"]) == "Dusty Attic":
		dust_boss_cool = 3.0
	elif String(fr["fname"]) == "Fairy Pond":
		fairy_cool = 3.0
		_apply_skin()   # restore Roshan's normal look after the fairy flight
	show_msg(fr["fname"], txt, "win" if win else vo)
	_respawn_pearls()   # after the banner: its freshness guard yields to the win message
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
	var m: Material
	if col == Color(1.0, 0.4, 0.25):
		m = _ball_panel_mat()
	else:
		var soft := StandardMaterial3D.new()
		soft.albedo_color = col
		soft.roughness = 0.78
		soft.emission_enabled = true
		soft.emission = col * 0.25
		soft.emission_energy_multiplier = 0.35
		m = soft
	mi.material_override = m
	add_child(mi)
	game_nodes.append(mi)
	return mi

var _ball_panel_shader: Shader = null

func _ball_panel_mat() -> ShaderMaterial:
	# the six-panel beach-ball shader (shared Shader resource: one pipeline
	# compile ever, pre-warmed by _warm_shaders behind the intro)
	if _ball_panel_shader == null:
		_ball_panel_shader = Shader.new()
		_ball_panel_shader.code = """shader_type spatial;
render_mode diffuse_burley, specular_schlick_ggx;
void fragment() {
	float angle = UV.x;
	float panel = floor(fract(angle) * 6.0);
	vec3 coral = vec3(0.98, 0.38, 0.40);
	vec3 aqua = vec3(0.25, 0.78, 0.78);
	vec3 shell = vec3(1.0, 0.88, 0.68);
	vec3 lavender = vec3(0.62, 0.49, 0.82);
	vec3 gold = vec3(1.0, 0.70, 0.24);
	vec3 color = panel < 1.0 ? coral : (panel < 2.0 ? aqua : (panel < 3.0 ? shell : (panel < 4.0 ? lavender : (panel < 5.0 ? gold : aqua))));
	float panel_uv = fract(angle * 6.0);
	float edge = min(panel_uv, 1.0 - panel_uv);
	float seam = 1.0 - smoothstep(0.008, 0.025, edge);
	ALBEDO = mix(color, vec3(0.16, 0.12, 0.28), seam * 0.55);
	ROUGHNESS = 0.82;
	SPECULAR = 0.12;
}"""
	var shader_mat := ShaderMaterial.new()
	shader_mat.shader = _ball_panel_shader
	return shader_mat

func _soft_mat(col: Color, glow: float = 0.12) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = col
	m.roughness = 0.55
	m.emission_enabled = true
	m.emission = col * glow
	return m

func _check_star(pos: Vector3) -> Node3D:
	var st: Node3D = LandmarkArtFactory.create_star(2.4, Color(1.0, 0.76, 0.24))
	st.position = pos
	add_child(st)
	game_nodes.append(st)
	return st

func _course_box(pos: Vector3, size: Vector3, col: Color, rotdeg: Vector3 = Vector3.ZERO) -> MeshInstance3D:
	var b := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	b.mesh = bm
	b.material_override = _up_mat("fabric", 0.18, col.lightened(0.12))
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
	_fade_cut(_start_game_now.bind(fr))

func _start_game_now(fr: Dictionary) -> void:
	game = String(fr["game"])
	g = {"fr": fr, "t": 0.0, "timer": -1.0}
	if game == "slide":
		# _enter_arena must know the exact route before it decides whether to build
		# and teleport into a spatial arena. Penguin chase remains mode="chase".
		g["mode"] = String(fr.get("mode", "fish"))
	_enter_arena(game)
	if game == "melody":
		# Its full-screen notes own the complete touch surface; hide the legacy
		# swim stick/action bay while retaining the separately-owned pause corner.
		_set_world_controls_enabled(false, "melody")
	var origin: Vector3 = ARENA_POS
	if game == "fetch":
		_game_obj("fetch", FetchGame).build(fr, origin)
	elif game == "dolls":
		_game_obj("dolls", DollsGame).build(fr)
	elif game == "brawl":
		_game_obj("brawl", BrawlGame).build(fr, origin)
	elif game == "dustboss":
		_game_obj("dustboss", DustBossGame).build(fr, origin)
	elif game == "seek":
		_game_obj("seek", SeekGame).build(fr)
	elif game == "race":
		_game_obj("race", SlideRaceGame).build(fr, origin)
	elif game == "shop":
		_game_obj("shop", ShopGame).build(fr, origin)
	elif game == "treasure":
		_game_obj("treasure", TreasureGame).build(fr, origin)
	elif game == "melody":
		var melody: MelodyGame = _game_obj("melody", MelodyGame) as MelodyGame
		melody.build(fr, origin)
		for reason_value: Variant in _melody_input_context_losses.keys():
			melody.on_input_context_lost(StringName(String(reason_value)))
		melody.arm_entry_sources(_melody_held_sources.keys())
	elif game == "slide":
		var slide: SlideRaceGame = _game_obj("race", SlideRaceGame) as SlideRaceGame
		var slide_canvas_route: bool = _slide_canvas_fish_route_active()
		if slide_canvas_route:
			# Clear the legacy router before build. Its cancellation callback is safe
			# against the closed controller; build then establishes the authoritative
			# fresh startup latch which remains intact through the reveal fade.
			joy_ev_axis.clear()
			joy_ev_btn.clear()
			_slide_canvas_overlay_axis_wait_neutral = false
			_slide_canvas_overlay_poll_neutral_frames = 0
			var slide_canvas_return_camera := active_viewport_camera()
			g["slide_canvas_return_camera"] = slide_canvas_return_camera
			g["slide_canvas_camera_was_current"] = \
				slide_canvas_return_camera != null
			if player != null and player.cam != null:
				g["slide_canvas_player_cam_transform"] = player.cam.transform
				g["slide_canvas_player_cam_fov"] = player.cam.fov
				g["slide_canvas_player_cam_orbit"] = player.cam_orbit
				g["slide_canvas_player_cam_pitch"] = player.cam_pitch_off
			if slide_canvas_return_camera != null:
				slide_canvas_return_camera.clear_current(false)
			if collection_button_layer != null:
				g["slide_canvas_collection_was_visible"] = \
					collection_button_layer.visible
				collection_button_layer.visible = false
			if living_layer != null:
				g["slide_canvas_living_was_visible"] = living_layer.visible
				living_layer.visible = false
			_set_world_controls_enabled(false, "slide_canvas")
			if player != null:
				g["slide_canvas_player_was_visible"] = player.visible
		slide.build_slide(fr, origin)
		if slide_canvas_route:
			# The fade still covers the fresh layer. Hide the spatial actor and seed
			# every concrete source which was physically down before entry.
			if player != null:
				player.visible = false
				player.vel *= 0.0
			for reason_value: Variant in _slide_canvas_input_context_losses.keys():
				slide.on_input_context_lost(StringName(String(reason_value)))
			slide.arm_entry_sources(_slide_canvas_held_sources.keys())
	elif game == "fairyshoot":
		_game_obj("fairyshoot", FairyGame).build(fr, origin)

func _ice_mat(col: Color, glow: float = 0.18, tex: String = "") -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = col
	m.metallic = 0.25
	m.roughness = 0.12
	m.emission_enabled = true
	m.emission = col * glow
	if tex != "":
		# painted GEN2 sheet (nano-banana suite) over the glow base - used
		# for the snow surfaces so they read as HER art, not flat white
		m.albedo_texture = load("res://assets/terrain/up_%s_col.jpg" % tex)
		m.uv1_triplanar = true
		m.uv1_scale = Vector3(0.14, 0.14, 0.14)
		m.metallic = 0.05
		m.roughness = 0.7
	return m

func _build_slide_portal() -> void:
	# a penguin on a floating ice floe in the reef — swim up to it to start the slide
	slide_portal_pos = Vector3(48.0, WATER_TOP + 0.5, -42.0)
	var floe := MeshInstance3D.new()
	var fm := CylinderMesh.new(); fm.top_radius = 11.0; fm.bottom_radius = 8.5; fm.height = 3.0
	floe.mesh = fm
	floe.material_override = _ice_mat(Color(0.95, 1.0, 1.05), 0.08, "snow")
	floe.position = slide_portal_pos + Vector3(0, -2.0, 0)
	add_child(floe)
	var peng := _place_aq("Penguin", slide_portal_pos + Vector3(0, 1.4, 0), 4.2, false)
	if peng != null:
		# face the reef center (gen2 -X face) so Roshan meets his face, not his back
		peng.rotation.y = atan2(-slide_portal_pos.z, slide_portal_pos.x)
		_play_clip(peng, "idle")
	if peng != null:
		slide_portal_penguin = peng

func _build_brawl_portal() -> void:
	# Princess Huluu waits by her toy castle on the seabed — swim up to start
	# the two-hero TOY CASTLE brawler (scripts/games/brawl.gd)
	var bx := -98.0
	var bz := 72.0
	brawl_portal_pos = Vector3(bx, seabed_y(bx, bz) + 4.0, bz)
	var castle := Node3D.new()
	castle.position = brawl_portal_pos + Vector3(0, -3.2, -5.0)
	add_child(castle)
	var keep := MeshInstance3D.new()
	var km := BoxMesh.new()
	km.size = Vector3(7.0, 6.0, 5.0)
	keep.mesh = km
	keep.position = Vector3(0, 3.0, 0)
	keep.material_override = _soft_mat(Color(0.86, 0.80, 0.88), 0.10)
	castle.add_child(keep)
	for tx in [-4.2, 4.2]:
		var tower := MeshInstance3D.new()
		var tm := CylinderMesh.new()
		tm.top_radius = 1.5
		tm.bottom_radius = 1.7
		tm.height = 8.0
		tower.mesh = tm
		tower.position = Vector3(float(tx), 4.0, 0)
		tower.material_override = _soft_mat(Color(0.86, 0.80, 0.88), 0.10)
		castle.add_child(tower)
		var roof := MeshInstance3D.new()
		var rm := CylinderMesh.new()
		rm.top_radius = 0.05
		rm.bottom_radius = 1.9
		rm.height = 2.6
		roof.mesh = rm
		roof.position = Vector3(float(tx), 9.2, 0)
		roof.material_override = _soft_mat(Color(0.78, 0.55, 0.75), 0.16)
		castle.add_child(roof)
	var hu := Sprite3D.new()
	hu.texture = load("res://assets/characters/friends/huluu.png")
	hu.pixel_size = 5.5 / maxf(1.0, float(hu.texture.get_height()))
	hu.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	hu.shaded = false
	hu.position = brawl_portal_pos + Vector3(3.2, 0.4, 3.0)
	add_child(hu)
	_halo(brawl_portal_pos + Vector3(0, 0.6, 0), Color(1.0, 0.8, 0.95), 10.0)
	_halo(slide_portal_pos + Vector3(0, 3, 0), Color(0.6, 0.9, 1.0), 15.0)
	var l := OmniLight3D.new()
	l.light_color = Color(0.7, 0.9, 1.0); l.light_energy = 2.2; l.omni_range = 24.0
	l.position = slide_portal_pos + Vector3(0, 6, 0); add_child(l)
	var lab := Label3D.new()
	lab.text = "🐧 Penguin Slide!"
	lab.font_size = 64; lab.pixel_size = 0.04; lab.outline_size = 14
	lab.modulate = Color(0.75, 0.95, 1.0); lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	lab.position = slide_portal_pos + Vector3(0, 9, 0); add_child(lab)

func _tick_game(delta: float) -> void:
	var fr: Dictionary = g["fr"]
	g["t"] = float(g["t"]) + delta
	if float(g["timer"]) > 0.0:
		g["timer"] = float(g["timer"]) - delta
		if float(g["timer"]) <= 0.0:
			g["timer"] = -1.0
			show_msg(String(fr.get("fname", "Roshan")), "Take your time — keep playing when you're ready!", "hint")
	var ppos: Vector3 = player.position
	if game == "fetch":
		_tick_fetch(delta, fr, ppos)
	elif game == "dolls":
		_tick_dolls(delta, fr)
	elif game == "brawl":
		_tick_brawl(delta, fr, ppos)
	elif game == "dustboss":
		_game_obj("dustboss", DustBossGame).tick(delta, fr, ppos)
	elif game == "seek":
		_game_obj("seek", SeekGame).tick(delta, fr)
	elif game == "race" or game == "treasure":
		_tick_course(delta, fr, ppos)
	elif game == "shop":
		_tick_shop(delta, fr, ppos)
	elif game == "melody":
		_tick_melody(delta, fr, ppos)
	elif game == "slide":
		_game_obj("race", SlideRaceGame)._tick_slide(delta, fr, ppos)
	elif game == "fairyshoot":
		_tick_fairyshoot(delta, fr, ppos)

func skin_sprite_path() -> String:
	# the flat art matching the wardrobe skin — used by the kart driver and
	# the 2D minigame mermaid so the chosen look follows Roshan into every
	# game, not just the ocean (the Dolls Canvas catcher uses this path too)
	if skin_id == "huluu":
		return "res://assets/characters/friends/huluu.png"
	if skin_id == "fairy":
		return "res://assets/characters/skins/fairy_mermaid.png"
	return "res://assets/characters/roshan_25d/roshan_base.png"   # classic

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
	if castle_logo_layer != null and is_instance_valid(castle_logo_layer):
		return castle_logo_layer
	if craft_layer != null and is_instance_valid(craft_layer):
		return craft_layer
	if wardrobe_layer != null and is_instance_valid(wardrobe_layer):
		return wardrobe_layer
	if stickers_layer != null and is_instance_valid(stickers_layer):
		return stickers_layer
	if collection_layer != null and is_instance_valid(collection_layer):
		return collection_layer
	if companion_care_layer != null and is_instance_valid(companion_care_layer):
		return companion_care_layer
	if companion_layer != null and is_instance_valid(companion_layer):
		return companion_layer
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


func _neutralize_slide_canvas_overlay_poll() -> void:
	# Input events are quarantined while the app is unfocused/backgrounded and
	# through the source-free restore boundary. Polling must obey the same rule:
	# sample current button levels as the new baseline, never synthesize an edge,
	# and retire the old star cursor until a deliberate post-restore stick move.
	_pad_prev_a = joy_pressed(JOY_BUTTON_A)
	_pad_prev_b = joy_pressed(JOY_BUTTON_B)
	_pc_prev_a = _pad_prev_a
	pad_cursor_active = false
	if pad_cursor_layer != null:
		pad_cursor_layer.visible = false
	if not _slide_canvas_overlay_axis_wait_neutral:
		return
	var all_poll_sources_neutral: bool = not _pad_prev_a and not _pad_prev_b \
		and not joy_pressed(JOY_BUTTON_DPAD_LEFT) \
		and not joy_pressed(JOY_BUTTON_DPAD_RIGHT) \
		and not joy_pressed(JOY_BUTTON_DPAD_UP) \
		and not joy_pressed(JOY_BUTTON_DPAD_DOWN) \
		and absf(joy_axis(JOY_AXIS_LEFT_X)) <= 0.18 \
		and absf(joy_axis(JOY_AXIS_LEFT_Y)) <= 0.18 \
		and absf(joy_axis(JOY_AXIS_RIGHT_X)) <= 0.18 \
		and absf(joy_axis(JOY_AXIS_RIGHT_Y)) <= 0.18
	if _slide_canvas_input_context_lost() \
			or _slide_canvas_input_context_blocks_input() \
			or not all_poll_sources_neutral:
		_slide_canvas_overlay_poll_neutral_frames = 0
		return
	# Require two trustworthy post-guard neutral polls. Some mobile backends
	# publish a stale zero for one frame before their mapped pad state refreshes.
	_slide_canvas_overlay_poll_neutral_frames += 1
	if _slide_canvas_overlay_poll_neutral_frames >= 2:
		_slide_canvas_overlay_axis_wait_neutral = false
		_slide_canvas_overlay_poll_neutral_frames = 0

func _tick_overlay_pads(delta: float) -> void:
	# gamepad shortcuts for the pointer-driven overlays: A = Done, B = close.
	# Without these a controller-only setup could open the craft studio or the
	# wardrobe and never leave (no pointer, no exit).
	var a: bool = joy_pressed(JOY_BUTTON_A)
	var b: bool = joy_pressed(JOY_BUTTON_B)
	var overlay_open: bool = castle_logo_layer != null or craft_layer != null \
		or wardrobe_layer != null or stickers_layer != null \
		or collection_layer != null or companion_layer != null \
		or companion_care_layer != null
	_overlay_age = _overlay_age + delta if overlay_open else 0.0
	if _overlay_age > 0.6:   # grace so the A/B that was held while swimming in doesn't fire
		if castle_logo_layer != null:
			if a and not _pad_prev_a and not pad_cursor_active:
				_finish_castle_logo()
			elif b and not _pad_prev_b:
				_close_castle_logo()
		elif craft_layer != null:
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
		elif collection_layer != null:
			if (b and not _pad_prev_b) or (a and not _pad_prev_a and not pad_cursor_active):
				_collection_ref().close_book()
		elif companion_care_layer != null:
			if b and not _pad_prev_b:
				_companion_ref().close_care_menu()
		elif companion_layer != null:
			if b and not _pad_prev_b:
				_companion_ref().close_picker()
	_pad_prev_a = a
	_pad_prev_b = b

var _wayfind_t := 0.0

func _tick_wayfinder(delta: float, ppos: Vector3) -> void:
	# MOBILE NAV AUDIT: a sparkle comet-trail from Roshan toward the current
	# best objective — the "pathfinding" a non-reader can follow. In the reef
	# this is the nearest friend/shop/slide goal; in the Sky Lagoon it is the
	# next Dream Star, then the open castle door. Throttled to 3 cheap bursts
	# every 2.2s and silent during overlays, minigames and castle interiors.
	var level2_court: bool = (game == "level2"
		and String(g.get("phase", "court")) == "court")
	if (game != "" and not level2_court) or mg_kind != "" or intro_active:
		_set_objective("", null, "")
		return
	if _overlay_root_for_cursor() != null:
		_set_objective("", null, "")
		return
	_wayfind_t -= delta
	if _wayfind_t > 0.0:
		return
	_wayfind_t = 2.2
	var target := Vector3.ZERO
	# the objective card mirrors the sparkle current as a picture: portrait for
	# a friend, emoji pictogram for portals/stars (Codex UI handoff)
	var okey := ""
	var otex: Texture2D = null
	var oemj := ""
	if level2_court:
		if bool(g.get("ocean_gate_hub", false)):
			var gates: Array = g.get("ocean_kingdom_gates", [])
			var nearest_gate_distance: float = INF
			for gate_value: Variant in gates:
				var gate: Dictionary = gate_value as Dictionary
				var gate_pos: Vector3 = gate.get("pos", Vector3.ZERO)
				var gate_distance: float = gate_pos.distance_to(ppos)
				if gate_distance < nearest_gate_distance:
					nearest_gate_distance = gate_distance
					target = gate_pos
		for sd in l2_stars:
			if target != Vector3.ZERO:
				break
			if not bool(sd["got"]):
				var star: Node3D = sd["node"]
				if is_instance_valid(star):
					target = star.position
					okey = "l2star"
					oemj = "⭐"
				break
		if target == Vector3.ZERO and l2_open and l2_door != null and is_instance_valid(l2_door):
			target = g.get("entry", l2_door.position)
			okey = "l2door"
			oemj = "🏰"
	else:
		var best := 1e9
		for f in friends:
			if not bool(f["won"]):
				var p: Vector3 = (f["node"] as Node3D).position
				var d: float = p.distance_to(ppos)
				if d < best:
					best = d
					target = p
					okey = "friend:" + String(f["fname"])
					var tn: String = String(f.get("tex", ""))
					otex = _cutout_tex(tn) if tn != "" else null
					oemj = "⭐"
		if target == Vector3.ZERO:
			if pearl_count >= 60 and manta != null and is_instance_valid(manta):
				target = manta.position
				okey = "manta"
				oemj = "🌟"
			elif _all_friends_won():
				var return_xz: Vector2 = ReefDistricts.kingdom_return_gate(
					ReefDistricts.kingdom_at(Vector2(ppos.x, ppos.z)))
				target = Vector3(return_xz.x,
					seabed_y(return_xz.x, return_xz.y) + 6.0, return_xz.y)
			elif slide_portal_pos != Vector3.ZERO:
				target = slide_portal_pos
				okey = "slide"
				oemj = "🐧"
	if target == Vector3.ZERO or target.distance_to(ppos) < 22.0:
		_set_objective("", null, "")
		return
	_set_objective(okey, otex, oemj)
	for k in range(3):
		var tt: float = 0.06 + 0.07 * float(k)
		_sparkle_burst(ppos.lerp(target, tt) + Vector3(0, 1.5, 0), Color(1.0, 0.95, 0.6))

func _all_friends_won() -> bool:
	for friend_value: Variant in friends:
		var friend: Dictionary = friend_value as Dictionary
		if not bool(friend.get("won", false)):
			return false
	return not friends.is_empty()

func _tick_ocean_return_gate(delta: float, ppos: Vector3) -> bool:
	# Both ecosystems reuse an authored landmark as their doorway back to the
	# castle gatehouse. Leave/re-enter hysteresis prevents arrival bounce.
	# Legacy headless probes stay on their historical routes until they
	# explicitly choose a kingdom through the new hub.
	if not ocean_routes_enabled:
		return false
	ocean_return_gate_cool = maxf(0.0, ocean_return_gate_cool - delta)
	var local_kingdom: String = ReefDistricts.kingdom_at(Vector2(ppos.x, ppos.z))
	var gate_xz: Vector2 = ReefDistricts.kingdom_return_gate(local_kingdom)
	var gate_pos := Vector3(gate_xz.x, seabed_y(gate_xz.x, gate_xz.y) + 6.0, gate_xz.y)
	var distance: float = gate_pos.distance_to(ppos)
	if not ocean_return_gate_armed:
		if distance > 17.0:
			ocean_return_gate_armed = true
		return false
	if not touch_uses_explicit_interactions() and ocean_return_gate_cool <= 0.0 and distance < 10.0:
		ocean_return_gate_armed = false
		ocean_kingdom = local_kingdom
		_enter_level2(false, false, true)
		return true
	return false

func _process(delta: float) -> void:
	_sync_pause_surface_layer()
	var slide_canvas_active: bool = _slide_canvas_fish_route_active()
	var slide_canvas_return_was_active: bool = _slide_canvas_return_guard_active()
	if slide_canvas_return_was_active:
		_tick_slide_canvas_return_guard()
	if not slide_canvas_active and not slide_canvas_return_was_active:
		_living_world_ref().tick(delta)
		if _fx_water != null:
			_fx_water.tick(delta)   # cutaways keep water FX; opaque fish Canvas suspends them
	# camera watchdog (CAMERA_AUDIT_2026_07 P0): if a torn-down mode freed the
	# current camera without restoring one (kart/galaxy teardown guards,
	# cancel(false) paths), fall back to Roshan instead of a black screen
	var vp_cam := active_viewport_camera()
	var sky_canvas_active: bool = game == "level2" \
		and String(g.get("phase", "")) == "promenade"
	var melody_canvas_active: bool = game == "melody"
	var opaque_canvas_active: bool = sky_canvas_active or melody_canvas_active \
		or slide_canvas_active
	# Player creates its compatibility camera deferred during boot. Direct phone
	# entry can therefore reach Sky before that compatibility camera joins the tree; disarm
	# the late arrival as well as the synchronous entry path above.
	if slide_canvas_active and vp_cam != null and vp_cam.is_inside_tree():
		# Clear whichever camera actually owned the Viewport, not merely the
		# compatibility player camera. Exact ownership is restored on teardown.
		vp_cam.clear_current(false)
	elif opaque_canvas_active and player != null and player.cam != null \
			and player.cam.is_inside_tree() and player.cam.current:
		player.cam.clear_current(false)
	elif not opaque_canvas_active and vp_cam == null \
			and player != null and player.cam != null and player.cam.is_inside_tree():
		player.snap_cam()
		player.cam.make_current()
	if save_dirty:
		save_retry_t -= delta
		if save_retry_t <= 0.0:
			_write_save()
	elif save_pending:
		save_pending_t -= delta
		if save_pending_t <= 0.0:
			_write_save()
	_audio_ref().tick_dialogue(delta)
	if msg_timer > 0.0:
		msg_timer -= delta
		if msg_timer <= 0.0:
			hud_msg.text = ""
	if hud_msg != null:
		hud_msg.visible = hud_msg.text != ""
	if hud_game != null:
		# Activity-specific picture HUDs own their own surfaces; this legacy
		# free-roam sentence card is intentionally never persistent.
		hud_game.visible = false
	if pose_t >= 0.0:
		pose_t -= delta   # trophy curtain-call countdown (player frozen while >=0)
	_tick_contact_shadow()
	_tick_ambience_duck(delta)
	if mic_sys != null:
		mic_sys.tick(delta)   # no-op unless a battle armed the microphone
	if player != null and not opaque_canvas_active \
			and not slide_canvas_return_was_active:
		_tick_wayfinder(delta, player.position)
	if slide_canvas_return_was_active:
		_neutralize_slide_canvas_overlay_poll()
	elif slide_canvas_active and (_slide_canvas_input_context_blocks_input() \
			or _slide_canvas_overlay_axis_wait_neutral):
		_neutralize_slide_canvas_overlay_poll()
	else:
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
	if slide_canvas_return_was_active:
		# Even the second neutral sample is a quarantine frame. The controls block
		# may retire above, but the returned world cannot consume a level until a
		# genuinely fresh event arrives on a later frame.
		if caustics_plane != null and caustics_plane.visible:
			caustics_plane.visible = false
		return
	var ppos: Vector3 = player.position
	if melody_canvas_active:
		# Melody owns the complete visible and interactive world. Preserve the
		# shared save/audio/pause work above, tick its controller exactly once,
		# and suspend every hidden spatial system until synchronous teardown.
		if caustics_plane != null and caustics_plane.visible:
			caustics_plane.visible = false
		if touch_ui != null:
			touch_ui.set_action_label("PLAY")
		# Some platforms continue producing frames between focus-out/paused and
		# resumed/focus-in. Those frames are not gameplay time and cannot advance
		# Melody's medal clock, motion, neutral guard, or controller state.
		if _melody_input_context_lost():
			return
		_tick_game(delta)
		return
	if slide_canvas_active:
		# Harper and Fiona's fish slide is a complete Canvas world. Keep the shared
		# save/audio/pause seams above, but suspend every hidden Reef system and
		# tick its controller exactly once through _tick_game (after g.t advances).
		var slide_canvas := _game_obj("race", SlideRaceGame) as SlideRaceGame
		slide_canvas.refresh_canvas_layout()
		if caustics_plane != null and caustics_plane.visible:
			caustics_plane.visible = false
		if _slide_canvas_input_context_lost():
			return
		if _slide_canvas_overlay_axis_wait_neutral:
			# Restore the controller's source-free boundary without advancing g.t,
			# then keep the ride frozen until two trustworthy neutral polls retire
			# every held overlay/gamepad source.
			slide_canvas.retire_input_context_restore_guard()
			return
		# Sticker Book and the other full-screen overlays resume SceneTree so their
		# own UI can animate. They must nevertheless freeze the ride itself: a
		# previously latched steer may never finish or award the game behind them.
		if _slide_canvas_overlay_owns_input():
			# Context restoration normally spends one source-free controller tick.
			# An overlay suppresses that tick, so retire only the guard here without
			# advancing g.t/progress; otherwise its own visible Back button deadlocks.
			slide_canvas.retire_input_context_restore_guard()
			return
		_tick_game(delta)
		return
	if sky_canvas_active:
		# The opaque Canvas promenade is a complete world slice. Its controller
		# is the sole movement, camera, interaction, collection and proximity
		# owner; the hidden player is only a legacy return coordinate.
		if caustics_plane != null and caustics_plane.visible:
			caustics_plane.visible = false
		g["t"] = float(g.get("t", 0.0)) + delta
		_lagoon_promenade_ref().tick(delta)
		if touch_ui != null:
			touch_ui.set_action_label(_lagoon_promenade_ref().action_label())
		return
	if touch_uses_explicit_interactions():
		_tap_move_ref().tick(delta)
		_interaction_ref().tick(delta, ppos)
	_collection_ref().tick(delta, ppos)
	if caustics_plane != null:
		if game == "" and not intro_active and caustics_enabled:
			caustics_plane.visible = true
			caustics_plane.position = Vector3(ppos.x, seabed_y(ppos.x, ppos.z) + 1.2, ppos.z)
		elif caustics_plane.visible:
			caustics_plane.visible = false
	# KartGame owns the visible scene and input while racing. Keep the small
	# global timer/audio work above, but suspend hidden reef collectibles,
	# characters, foliage, movers and culling instead of paying for two worlds.
	if game == "kart":
		if touch_ui != null and kart_game != null and kart_game.has_method("action_label"):
			touch_ui.set_action_label(String(kart_game.action_label()))
		return
	if game == "":
		if _tick_ocean_return_gate(delta, ppos):
			return
		_carry_ref().tick(delta, ppos)   # starfish scoop/toss + singing shells
		_flow_ref().tick(delta, ppos)    # stream/geyser currents (accel read by player)
		_grotto_ref().tick(delta, ppos)  # push-block grotto
	for i in range(pearls.size() - 1, -1, -1):
		var p := pearls[i]
		p.rotate_y(delta * 0.7)
		p.position.y += sin(Time.get_ticks_msec() / 700.0 + float(i)) * 0.006
		if p.position.distance_to(ppos) < 6.0:
			var l: OmniLight3D = p.get_meta("light")
			if is_instance_valid(l):
				l.queue_free()
			pearl_lights.erase(l)   # keep the quality-toggle list free of dead refs
			var h: MeshInstance3D = p.get_meta("halo")
			if is_instance_valid(h):
				h.queue_free()
			p.queue_free()
			pearls.remove_at(i)
			pearl_count += 1
			if pearl_count % 25 == 0 and player != null:
				player.play_verb("giggle")   # R2-C: every 25th pearl is a little party
			elif player != null and String(player.verb) == "":
				player.play_verb("collect")   # quick two-hand scoop on every pearl
			_sparkle_burst(p.position, Color(1.0, 0.8, 1.0))
			if chime != null:
				var step: int = pearl_note % 21
				var deg: int = step % 7
				var octv: int = step / 7
				chime.pitch_scale = 0.75 * pow(2.0, float(PENT[deg] + 12 * octv) / 12.0)
				chime.play()
				pearl_note += 1
			# ~6s min-gap shared across all three pearl lines. _say's own gap is
			# keyed per speaker_event, so the rotating pick would sidestep it and
			# chatter on every pearl of a string.
			var vnow := Time.get_ticks_msec() / 1000.0
			if vnow - float(said_cool.get("roshan_pearl_any", -99.0)) >= 6.0:
				said_cool["roshan_pearl_any"] = vnow
				_say("roshan", ["pearl", "pearl2", "pearl3"][pearl_note % 3])
			_update_hud()
			_queue_save()   # hot path: debounced, flushed by _process/pause/close
	var tt: float = Time.get_ticks_msec() / 1000.0
	for f in friends:
		var node: Node3D = f["node"]
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
		var discover_radius: float = float(f.get("discover_radius", 9.0))
		var linger_radius: float = float(f.get("linger_radius", 10.0))
		var start_radius: float = float(f.get("start_radius", 8.0))
		if not f["found"] and dd < discover_radius:
			f["found"] = true
			(f["beacon"] as OmniLight3D).light_energy = 1.0
			var pmat2: StandardMaterial3D = (f["pillar"] as MeshInstance3D).material_override
			pmat2.albedo_color.a = 0.09
			f["cool"] = 2.5
			show_msg(f["fname"], f["msg"])
			_update_hud()
			_queue_save()   # hot path: debounced, flushed by _process/pause/close
		elif f["found"] and game == "" and dd < linger_radius:
			if touch_uses_explicit_interactions():
				hud_game.text = "Tap the glowing friend to play!"
			elif float(f["cool"]) > 0.0:
				hud_game.text = "%s: game starting in %d..." % [f["fname"], int(ceilf(float(f["cool"])))]
			elif dd < start_radius:
				hud_game.text = ""
				_start_game(f)
	if game == "level2":
		g["t"] = float(g["t"]) + delta
		_tick_level2(delta, ppos)
	elif game == "north":
		_tick_northern(delta, ppos)
	elif game == "kart":
		pass   # the KartGame node ticks itself
	elif game == "galaxy":
		pass   # the GalaxyLevel node ticks itself
	elif game == "ember":
		pass   # the EmberFortressLevel node ticks itself
	elif game == "combat":
		pass   # the CombatArena node owns movement, camera and encounter logic
	elif game == "stuffie":
		pass   # the StuffieBattle node owns the creature, camera and dodge QTE
	elif game == "dungeon" or game == "emberdun":
		pass   # DungeonLevel sequences the battles and visual puzzles
	elif game == "opera":
		pass   # OperaHouse sequences the thirteen Canvas career shows
	elif game == "kitchen_cooking":
		pass   # The fridge portal's OperaAct owns the cooking gesture chain
	elif game != "":
		_tick_game(delta)
	_tick_wall_fade(delta)
	_tick_foliage_push(ppos)
	_tick_life(delta)
	_tick_movers(delta)
	_tick_aquatic(delta)
	_tick_peng_pal(delta)
	_companion_ref().tick(delta)
	_tick_god_rays(delta)
	_tick_guide(delta)
	_tick_finale(delta)
	_tick_hints(delta)
	_tick_beans(delta)
	_tick_roshan_reactions(delta, ppos)
	shop_cool = maxf(0.0, shop_cool - delta)
	treasure_cool = maxf(0.0, treasure_cool - delta)
	slide_cool = maxf(0.0, slide_cool - delta)
	brawl_cool = maxf(0.0, brawl_cool - delta)
	dust_boss_cool = maxf(0.0, dust_boss_cool - delta)
	kart_cool = maxf(0.0, kart_cool - delta)
	if game == "" and finale_t < 0.0 and not touch_uses_explicit_interactions():
		if manta != null and shop_cool <= 0.0:
			if manta.position.distance_to(ppos) < 17.0:
				shop_cool = 16.0
				_start_game(shop_fr)
		if treasure_cool <= 0.0 and wreck_pos != Vector3.ZERO \
				and wreck_pos.distance_to(ppos) < 13.0:
			# ZERO guard required: with the wreck deleted (2026-07-28) an
			# unguarded distance check put this trigger at the world origin
			treasure_cool = 12.0
			_start_game(treasure_fr)
		# the portal penguin is INTERACTIVE: he cheers when Roshan swims near,
		# before the game-start radius fires (rigged clip + chirp, cooled down)
		if slide_portal_penguin != null and is_instance_valid(slide_portal_penguin):
			peng_wave_cool -= delta
			var pd: float = slide_portal_pos.distance_to(ppos)
			if peng_wave_cool <= 0.0 and pd < 24.0 and pd > 13.0:
				peng_wave_cool = 12.0
				_play_clip(slide_portal_penguin, "cheer", 1.1)
				_sparkle_burst(slide_portal_penguin.position + Vector3(0, 3.0, 0), Color(0.7, 0.9, 1.0))
				if peng_giggle != null:
					peng_giggle.pitch_scale = 0.9 + randf() * 0.15
					peng_giggle.play()
			elif pd > 30.0:
				_play_clip(slide_portal_penguin, "idle")
		if slide_cool <= 0.0 and slide_portal_pos != Vector3.ZERO and slide_portal_pos.distance_to(ppos) < 14.0:
			slide_cool = 14.0
			_start_game(slide_fr)
		if brawl_cool <= 0.0 and brawl_portal_pos != Vector3.ZERO and brawl_portal_pos.distance_to(ppos) < 13.0:
			brawl_cool = 14.0
			_start_game(brawl_fr)
		if dust_boss_cool <= 0.0 and dust_boss_portal_pos != Vector3.ZERO \
				and dust_boss_portal_pos.distance_to(ppos) < 13.0:
			dust_boss_cool = 14.0
			_start_game(dust_boss_fr)
		if kart_portal_pos != Vector3.ZERO:
			var kd: float = Vector2(kart_portal_pos.x - ppos.x, kart_portal_pos.z - ppos.z).length()
			var ky: float = absf(kart_portal_pos.y - ppos.y)
			if not kart_ocean_portal_armed:
				# Hysteresis keeps boundary bobbing from re-arming the gate under Roshan.
				if kd > 16.0 or ky > 18.0:
					kart_ocean_portal_armed = true
			elif kart_cool <= 0.0 and kd < 12.0 and ky < 14.0:
				_start_kart_game(false, "terrain")
	if game == "" and finale_t < 0.0:
		# Hybrid replaces only the proximity transition. Story progression and
		# the portal's visual raise/animation must keep ticking in both modes.
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
		if game == "level2" and String(g.get("phase", "")) == "promenade":
			act_lbl = _lagoon_promenade_ref().action_label()
		elif touch_uses_explicit_interactions() and touch_focus_ready:
			for touch_item_value: Variant in touch_interactables:
				var touch_item: Dictionary = touch_item_value as Dictionary
				if String(touch_item.get("id", "")) == touch_focus_id:
					act_lbl = String(touch_item.get("verb", "GO"))
					break
		elif _collection_ref().has_nearby():
			act_lbl = "CATCH!"
		elif game == "fetch" and String(g.get("phase", "")) == "aim":
			act_lbl = "THROW"
		elif game == "shop":
			act_lbl = "BUY"
		elif game == "fairyshoot":
			act_lbl = "SPARKLE"
		elif game == "kart" and kart_game != null and kart_game.has_method("action_label"):
			act_lbl = String(kart_game.action_label())   # GO! on the pick screens, TURBO in the race
		elif game == "combat" and combat_game != null:
			act_lbl = "ICE" if combat_game.kind == "ice" else "FIRE"
		elif game == "dustboss":
			act_lbl = String(_game_obj("dustboss", DustBossGame).action_label())
		elif game == "stuffie" and stuffie_game != null:
			act_lbl = stuffie_game.action_label()   # PECK / CLAW
		elif (game == "dungeon" or game == "emberdun") and dungeon_game != null:
			act_lbl = dungeon_game.action_label()
		elif game == "opera" and opera_game != null:
			act_lbl = opera_game.action_label()
		elif game == "kitchen_cooking":
			act_lbl = _castle_rooms_ref().kitchen_action_label()
		touch_ui.set_action_label(act_lbl)

# ===================== BIOLUMINESCENT LIFE =====================
# ============== PHYSICS LAB (dev-mode experiment — cleanse later) ==============
# Two engine experiments for the Lenovo M11 (Helio G88 / Mali-G52) grading run,
# both triggerable from Developer Mode:
#  1. foliage_push_enabled — GPU foliage interaction: Roshan's position/speed
#     feed the (memoized) sway shaders once per frame; blades part around her.
#  2. Jolt props — real RigidBody3D barrels/balls (Jolt engine, see
#     project.godot [physics]) spawned near Roshan, shoved by her swim wake.
var foliage_push_enabled := true
var _sway_mat_cache := {}     # one sway material per color pair (also a perf win)
var jolt_props: Array = []

func _tick_foliage_push(ppos: Vector3) -> void:
	if _sway_mat_cache.is_empty():
		return
	var amt: float = 0.0
	if foliage_push_enabled and player != null:
		amt = clampf(0.25 + (player.vel as Vector3).length() * 0.04, 0.25, 1.1)
	for m in _sway_mat_cache.values():
		(m as ShaderMaterial).set_shader_parameter("push_pos", ppos)
		(m as ShaderMaterial).set_shader_parameter("push_amt", amt)

func _physlab_spawn() -> void:
	# 6 barrels + 6 balls in a ring around Roshan, resting on an invisible
	# static disc at seabed height (the reef floor is analytic, not a body)
	_physlab_clear()
	if player == null:
		return
	var c: Vector3 = player.position
	var floor_y: float = seabed_y(c.x, c.z)
	var sb := _jolt_static_box(Vector3(c.x, floor_y - 0.5, c.z), Vector3(60, 1, 60))
	sb.set_meta("physlab", true)
	jolt_props.append(sb)
	for i in range(12):
		var a: float = float(i) / 12.0 * TAU
		var pos := Vector3(c.x + cos(a) * 6.0, floor_y + 3.0 + float(i % 3), c.z + sin(a) * 6.0)
		if i % 2 == 0:
			jolt_props.append(_jolt_barrel(pos))
		else:
			jolt_props.append(_jolt_ball(pos, 0.9, Color.from_hsv(float(i) / 12.0, 0.6, 1.0), 0.35, 1.4))

func _physlab_clear() -> void:
	for p in jolt_props:
		if is_instance_valid(p):
			p.queue_free()
	jolt_props.clear()

func _physlab_standees() -> void:
	# Physical standees (2.5D redesign prototype, charter 2026-07-27): the
	# E2 prop() primitive spawned in the free-swim world — sprite cutouts
	# riding Jolt bodies, shoved by the same swim-wake coupling as the
	# barrels above. Dev-gated preview of the promenade prop fleet; the
	# waterlogged gravity/damp match the barrel feel in the reef.
	_physlab_clear()
	if player == null:
		return
	var c: Vector3 = player.position
	var floor_y: float = seabed_y(c.x, c.z)
	var sb := _jolt_static_box(Vector3(c.x, floor_y - 0.5, c.z), Vector3(60, 1, 60))
	sb.set_meta("physlab", true)
	jolt_props.append(sb)
	var e2 := SideScrollStage.new(self)
	for i in range(6):
		var a: float = float(i) / 6.0 * TAU
		var col := Color.from_hsv(float(i) / 6.0, 0.35, 1.0)
		var p := e2.prop("", Vector2(2.4, 3.2),
			c.x + cos(a) * 5.0, c.z + sin(a) * 5.0, {
				"parent": self, "register": false, "floor_y": floor_y,
				"drop": 2.0 + float(i) * 0.5, "color": col,
				"tumble": i % 2 == 0, "gravity_scale": 0.35, "damp": 1.2,
			})
		if p != null:
			jolt_props.append(p)

func _physics_process(delta: float) -> void:
	if _slide_canvas_fish_route_active() or _slide_canvas_return_guard_active():
		return
	if _castle_rooms_25d != null and _castle_rooms_25d.is_open():
		_castle_rooms_25d.physics_tick(delta)
	if game == "melody" \
			or (game == "level2" and String(g.get("phase", "")) == "promenade"):
		return
	# Roshan -> Jolt coupling: firm contact push + softer swim-wake drag,
	# at the physics tick so it is frame-rate independent.
	if player == null or jolt_props.is_empty():
		return
	var ppos: Vector3 = player.position
	var pvel: Vector3 = player.vel
	for p in jolt_props:
		var b := p as RigidBody3D
		if b == null or not is_instance_valid(b):
			continue
		var d: Vector3 = b.position - ppos
		var dist: float = d.length()
		if dist > 7.0 or dist < 0.001:
			continue
		var flat := Vector3(d.x, d.y * 0.25, d.z)
		if flat.length() < 0.001:
			flat = Vector3(pvel.x, 0, pvel.z)
		var dirf: Vector3 = flat.normalized()
		var imp: Vector3 = dirf * (maxf(0.0, 4.5 - dist) * 22.0)
		imp += pvel * (maxf(0.0, 1.0 - dist / 7.0) * 0.9)
		if imp.length_squared() > 0.0001:
			b.apply_central_impulse(imp * delta * b.mass)

func _jolt_barrel(pos: Vector3) -> RigidBody3D:
	var prop := RigidBody3D.new()
	prop.collision_layer = 2
	prop.collision_mask = 1 | 2
	prop.mass = 2.0
	prop.gravity_scale = 0.30       # water-logged: sinks slowly, easy to shove
	prop.linear_damp = 1.6
	prop.angular_damp = 1.2
	var shp := CollisionShape3D.new()
	var cy := CylinderShape3D.new()
	cy.radius = 1.0
	cy.height = 2.4
	shp.shape = cy
	prop.add_child(shp)
	prop.position = pos
	add_child(prop)
	return prop

func _jolt_ball(pos: Vector3, r: float, col: Color, gscale: float, damp: float) -> RigidBody3D:
	var b := RigidBody3D.new()
	b.collision_layer = 2
	b.collision_mask = 1 | 2
	b.mass = 1.0
	b.gravity_scale = gscale
	b.linear_damp = damp
	b.angular_damp = damp * 0.5
	var cs := CollisionShape3D.new()
	var sh := SphereShape3D.new()
	sh.radius = r
	cs.shape = sh
	b.add_child(cs)
	var mi := MeshInstance3D.new()
	var sm := SphereMesh.new()
	sm.radius = r
	sm.height = r * 2.0
	mi.mesh = sm
	mi.material_override = _soft_mat(col, 0.3)
	b.add_child(mi)
	b.position = pos
	add_child(b)
	return b

func _jolt_static_box(center: Vector3, size: Vector3) -> StaticBody3D:
	var sb := StaticBody3D.new()
	sb.collision_layer = 1
	sb.collision_mask = 0
	var cs := CollisionShape3D.new()
	var bx := BoxShape3D.new()
	bx.size = size
	cs.shape = bx
	sb.add_child(cs)
	sb.position = center
	add_child(sb)
	return sb
# ============ END PHYSICS LAB ==============

func _sway_grass_mat(base: Color, tip: Color) -> ShaderMaterial:
	var key := "%s|%s" % [base.to_html(), tip.to_html()]
	if _sway_mat_cache.has(key):
		return _sway_mat_cache[key]
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode cull_disabled, depth_prepass_alpha;
uniform vec3 base_col;
uniform vec3 tip_col;
uniform sampler2D leaf;
global uniform vec3 wind_dir;
global uniform float wind_gust;
uniform vec3 push_pos;          // Roshan's position (fed per frame)
uniform float push_amt = 0.0;   // bend strength, scaled by her speed
void vertex(){
	float w = UV.y;
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	// gusts ROLL across the meadow: phase offset along the wind direction, and
	// the blades lean downwind on top of their own sway
	float gg = 0.4 + wind_gust * 1.2;
	float ph = TIME * (0.9 + wind_gust * 0.7) - dot(wp.xz, wind_dir.xz) * 0.14;
	VERTEX.x += (sin(ph + wp.x * 0.28 + wp.z * 0.22) * 0.5 * gg + wind_dir.x * wind_gust * 0.5) * w;
	VERTEX.z += (cos(ph * 0.78 + wp.x * 0.16) * 0.36 * gg + wind_dir.z * wind_gust * 0.5) * w;
	// PHYSICS LAB: blades bend away from Roshan, harder the faster she moves
	vec2 away = wp.xz - push_pos.xz;
	float pdist = length(away);
	float ring = 1.0 - smoothstep(0.0, 4.5, pdist);
	float band = 1.0 - smoothstep(2.0, 8.0, abs(wp.y - push_pos.y));
	float bend = ring * band * push_amt * w;
	if (bend > 0.001 && pdist > 0.001) {
		vec3 off_ws = vec3(away.x / pdist, -0.35, away.y / pdist);
		vec3 off_ms = normalize((vec4(off_ws, 0.0) * MODEL_MATRIX).xyz);
		VERTEX += off_ms * bend * 1.5;
	}
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
	_sway_mat_cache[key] = m
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
func _scatter_field(count: int, mesh: Mesh, mat: Material, y_off: float, use_color: bool, cols: Array, upright: bool = false, habitat: String = "mixed") -> void:
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.use_colors = use_color
	mm.mesh = mesh
	mm.instance_count = count
	for i in range(count):
		var pos: Vector3 = _district_ref().scatter_point(habitat)
		pos.y += y_off
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
	flora_nodes.append(mmi)   # Speedy tier applies its 150u range to mass fields too

func _build_meadows() -> void:
	# The 2D build uses the procedural flora fallback below. Converted model
	# scenery is intentionally absent so this path stays mobile-safe.
	# anemones + urchins stay procedural for now (no painted source art yet —
	# see TEXTURE_SOURCE_AUDIT.md), soft jewel tones
	var anemone_mesh := _gen2_static_mesh("anemone_story")
	if anemone_mesh != null:
		_scatter_field(100, anemone_mesh, null, 0.1, false, [], false, "anemone")
	else:
		_scatter_field(100, _anemone_mesh(), _glow_tip_mat(), 0.1, true,
			[Color(0.95, 0.55, 0.72), Color(0.55, 0.82, 0.92), Color(0.78, 0.62, 0.95), Color(0.55, 0.92, 0.80)], false, "anemone")
	# HER starfish: flat painted decals resting on the sand (rendered from the
	# gen2 starfish model — the procedural white stars read as paper cutouts)
	var sf := PlaneMesh.new()
	sf.size = Vector2(2.1, 2.1)
	var sfm := StandardMaterial3D.new()
	sfm.albedo_texture = load("res://assets/props/gen2/starfish_decal.png")
	sfm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
	sfm.alpha_scissor_threshold = 0.5
	sfm.roughness = 1.0
	sfm.emission_enabled = true
	sfm.emission = Color(0.45, 0.32, 0.3)
	sfm.emission_energy_multiplier = 0.25
	_scatter_field(140, sf, sfm, 0.12, false, [], false, "starfish")
	var urchin_mesh := _gen2_static_mesh("urchin_story")
	if urchin_mesh != null:
		_scatter_field(60, urchin_mesh, null, 0.15, false, [], false, "urchin")
	else:
		_scatter_field(60, _urchin_mesh(), _glow_tip_mat(), 0.3, true,
			[Color(0.6, 0.5, 0.78), Color(0.5, 0.62, 0.85), Color(0.82, 0.55, 0.68)], false, "urchin")

func _sway_sprite_mat(sprite_path: String) -> ShaderMaterial:
	# gen2 painted blade: same wind-driven sway as the old procedural grass,
	# but the sprite's own art is the colour (alpha-cut, soft tip glow)
	var sh := Shader.new()
	sh.code = """shader_type spatial;
render_mode cull_disabled, depth_prepass_alpha;
uniform sampler2D leaf : source_color, filter_linear_mipmap;
global uniform vec3 wind_dir;
global uniform float wind_gust;
void vertex(){
	float w = UV.y;
	vec3 wp = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	float gg = 0.4 + wind_gust * 1.2;
	float ph = TIME * (0.9 + wind_gust * 0.7) - dot(wp.xz, wind_dir.xz) * 0.14;
	VERTEX.x += (sin(ph + wp.x * 0.28 + wp.z * 0.22) * 0.5 * gg + wind_dir.x * wind_gust * 0.5) * w;
	VERTEX.z += (cos(ph * 0.78 + wp.x * 0.16) * 0.36 * gg + wind_dir.z * wind_gust * 0.5) * w;
}
void fragment(){
	vec4 lf = texture(leaf, vec2(UV.x, 1.0 - UV.y));
	if (lf.a < 0.5) { discard; }
	ALBEDO = lf.rgb;
	ROUGHNESS = 0.85;
	SPECULAR = 0.1;
	BACKLIGHT = lf.rgb * (0.2 + UV.y * 0.3);
	EMISSION = lf.rgb * (0.02 + UV.y * UV.y * 0.06);
}"""
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("leaf", load(sprite_path))
	return m

func _fish_mat() -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nuniform sampler2D scales;\nvoid fragment(){\n\tfloat sc = texture(scales, UV * vec2(3.0, 1.5)).r;\n\tfloat belly = smoothstep(-0.3, 0.4, NORMAL.y);\n\tvec3 body = mix(COLOR.rgb * 0.10, COLOR.rgb * 0.45 + vec3(0.25), belly) * (0.7 + sc * 0.6);\n\tfloat rim = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 2.5);\n\tfloat band = step(0.8, fract(UV.x * 3.0)) ;\n\tALBEDO = body;\n\tEMISSION = COLOR.rgb * (band * 1.2 + rim * 1.6 + sc * 0.15);\n\tROUGHNESS = 0.35;\n}"
	var m := ShaderMaterial.new()
	m.shader = sh
	m.set_shader_parameter("scales", load("res://assets/terrain/scales.png"))
	return m

func _build_fish() -> void:
	var cols := [Color(0.3, 0.95, 1.0), Color(1.0, 0.6, 0.85), Color(0.6, 1.0, 0.5), Color(1.0, 0.85, 0.4), Color(0.7, 0.55, 1.0), Color(0.4, 0.8, 1.0)]
	# ambient schools are HER clownfish now: painted side-view sprites on
	# quads (rendered from the gen2 model), softly tinted per school. The
	# quad's local X is the travel axis, so the painted head leads.
	var body := QuadMesh.new()
	body.size = Vector2(2.0, 1.5)
	var fmat := StandardMaterial3D.new()
	fmat.albedo_texture = load("res://assets/props/gen2/clownfish_side.png")
	fmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
	fmat.alpha_scissor_threshold = 0.5
	fmat.cull_mode = BaseMaterial3D.CULL_DISABLED
	fmat.vertex_color_use_as_albedo = true
	fmat.roughness = 0.9
	fmat.emission_enabled = true
	fmat.emission = Color(0.25, 0.22, 0.2)
	fmat.emission_energy_multiplier = 0.5
	for s2 in range(6):
		var col: Color = cols[s2]
		var school_center: Vector3 = _district_ref().scatter_point(ReefDistricts.KINGDOM_CARIBBEAN)
		var school := {"cx": school_center.x, "cz": school_center.z, "cy": 12.0 + randf() * 22.0,
			"rad": 12.0 + randf() * 14.0, "spd": 0.2 + randf() * 0.3, "ph": randf() * TAU, "fish": []}
		var mm := MultiMesh.new()
		mm.transform_format = MultiMesh.TRANSFORM_3D
		mm.use_colors = true
		mm.mesh = body
		mm.instance_count = 14
		for i in range(14):
			# soft tint only: the sprite is already painted art, a full-
			# saturation multiply would muddy it (school identity stays on the halo)
			mm.set_instance_color(i, Color(1, 1, 1).lerp(col, 0.35))
		var mmi := MultiMeshInstance3D.new()
		mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mmi.multimesh = mm
		mmi.material_override = fmat
		add_child(mmi)
		flora_nodes.append(mmi)
		school["mm"] = mm
		var halo := _halo(Vector3.ZERO, col, 12.0)
		school["light"] = halo
		fish_schools.append(school)

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
	# Three storybook stingrays; the procedural ribbon remains missing-file fallback.
	var mmesh := _manta_mesh()
	for i in range(3):
		var m: Node3D = _gen2_creature("stingray", Vector3.ZERO, 5.0 + float(i) * 1.2)
		if m == null:
			var old_m := MeshInstance3D.new()
			old_m.mesh = mmesh
			old_m.material_override = _flap_mat([Color(0.4, 0.9, 1.0), Color(0.9, 0.6, 1.0), Color(0.5, 1.0, 0.7)][i])
			old_m.scale = Vector3.ONE * (2.2 + float(i) * 0.6)
			add_child(old_m)
			m = old_m
		movers.append({"node": m, "kind": "manta", "rad": 90.0 + float(i) * 45.0, "spd": 0.06 + randf() * 0.04,
			"ph": randf() * TAU, "y": 24.0 + float(i) * 8.0})
	# One great storybook fish with paired fins and horizontal flukes.
	var w: Node3D = _gen2_prop("giant_fish_story", Vector3.ZERO, 28.0, 0.0, 0.0)
	if w != null:
		var wap := _find_anim(w)
		if wap != null:
			var clips := wap.get_animation_list()
			if not clips.is_empty():
				var clip: StringName = clips[0]
				wap.get_animation(clip).loop_mode = Animation.LOOP_LINEAR
				wap.play(clip)
				wap.speed_scale = 0.65
	else:
		var old_w := MeshInstance3D.new()
		old_w.mesh = _fish_mesh(14.0)
		old_w.material_override = _creature_mat()
		add_child(old_w)
		w = old_w
	movers.append({"node": w, "kind": "whale", "rad": 200.0, "spd": 0.018, "ph": 0.0, "y": 38.0})
	# 2 sea turtles cruising low
	for i in range(2):
		var tm: Node3D = _gen2_creature("turtle", Vector3.ZERO, 5.2 + float(i) * 0.8)
		if tm == null:
			var old_tm := MeshInstance3D.new()
			old_tm.mesh = _manta_mesh()
			old_tm.material_override = _flap_mat(Color(0.55, 1.0, 0.45))
			old_tm.scale = Vector3.ONE * 1.1
			add_child(old_tm)
			tm = old_tm
		movers.append({"node": tm, "kind": "turtle", "rad": 60.0 + float(i) * 70.0, "spd": 0.05,
			"ph": PI * float(i), "y": 10.0 + float(i) * 5.0})

var god_rays: Array = []
func _build_god_rays() -> void:
	var rsh := Shader.new()
	rsh.code = "shader_type spatial;\nrender_mode cull_disabled, unshaded, blend_mix, depth_draw_never, shadows_disabled;\nuniform vec4 tint : source_color;\nvoid fragment(){\n\tfloat across = 1.0 - abs(UV.x - 0.5) * 2.0;\n\tfloat down = smoothstep(0.0, 0.28, UV.y) * smoothstep(1.0, 0.52, UV.y);\n\tALBEDO = tint.rgb;\n\tALPHA = tint.a * pow(max(across, 0.0), 2.4) * down;\n}"
	# Seven faint distant shafts are enough to imply filtered surface light.
	# The former 18 full-height quads overlapped into opaque blue walls on Mobile.
	var ray_count := 7
	for i in range(ray_count):
		var a: float = float(i) / float(ray_count) * TAU + randf() * 0.35
		var r: float = 72.0 + randf() * (WORLD_R * 0.58)
		var quad := QuadMesh.new()
		quad.size = Vector2(4.0 + randf() * 4.0, WATER_TOP + 16.0)
		var m := ShaderMaterial.new()
		m.shader = rsh
		m.set_shader_parameter("tint", Color(0.62, 0.90, 1.0, 0.018 + randf() * 0.012))
		var mi := MeshInstance3D.new()
		mi.mesh = quad
		mi.material_override = m
		mi.position = Vector3(cos(a) * r, (WATER_TOP + 16.0) * 0.45, sin(a) * r)
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

func on_player_jump(pos: Vector3, crossed: bool = false) -> void:
	# WW-style splash telegraph: ring + sparkles when she leaps near the surface
	if game == "" and pos.y > WATER_TOP - 12.0:
		_spawn_surf_ring(Vector3(pos.x, WATER_TOP - 0.25, pos.z), 16.0)
		_sparkle_burst(Vector3(pos.x, minf(pos.y + 2.0, WATER_TOP - 1.0), pos.z), Color(0.75, 0.95, 1.0))
		if crossed and player != null:
			# a REAL surface crossing (breach out or plunge back in) gets the
			# shared splash card, sized by how hard she crossed — kicks that
			# never break the surface keep the telegraph ring only
			fx_splash(Vector3(pos.x, WATER_TOP - 0.2, pos.z),
				absf((player.vel as Vector3).y), "roshan_surface")

func on_player_wet_change(pos: Vector3, entering: bool, speed: float) -> void:
	# Arena wet/dry oracle flip (lagoon rivers and moat, northern fjords):
	# the formerly SILENT water boundaries speak the shared vocabulary too.
	var s: float = water_surface_y(pos.x, pos.z)
	var at := Vector3(pos.x, pos.y + 0.4, pos.z)
	if absf(s) < 1e17:
		at.y = s + 0.05
	fx_splash(at, speed * 0.55, "roshan_wetline")
	if entering:
		_sparkle_burst(at + Vector3(0, 0.8, 0), Color(0.75, 0.95, 1.0))

func on_player_hop_land() -> void:
	# soft cartoon boing per on-land hop touchdown, pitch-wobbled so a scoot
	# across the meadow reads as boing-boing-boing instead of a metronome
	if hop_sfx != null:
		hop_sfx.pitch_scale = 0.9 + randf() * 0.25
		hop_sfx.play()

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
@warning_ignore("unused_private_class_variable")   # written/read by AudioDirector via m.
var _tap_player: AudioStreamPlayer = null
@warning_ignore("unused_private_class_variable")   # written/read by AudioDirector via m.
var _pop_player: AudioStreamPlayer = null
@warning_ignore("unused_private_class_variable")   # written/read by AudioDirector via m.
var _sfx_pool: Array = []
@warning_ignore("unused_private_class_variable")   # written/read by AudioDirector via m.
var _sfx_i := 0

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
	# Capture the whole return context, not just the spot. Today every caller
	# launches from the reef, so these hold world_env/"world" and the exit is
	# byte-for-byte what it always did; once the reef is gone they are what
	# lets a game hand her back to the promenade or the castle she came from.
	return_env = we_node.environment
	return_track = cur_track
	# Opaque true-Canvas activities preserve the shared return/music lifecycle,
	# but never construct or teleport into a hidden arena beneath their pixels.
	if kind == "dolls" or kind == "seek" or kind == "melody" \
			or (kind == "slide" and String(g.get("mode", "")) == "fish"):
		_play_music(kind)
		return
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
	var grade_profile: String = ""
	_wind_waker_bloom(arena_env, 0.9, 0.35, 1.02)   # bloom emitters only — 0.85 white-washed bright floors (snow!)
	if kind == "fetch":          # snowy backyard noon
		grade_profile = "bright_pastel"
		arena_env.background_color = Color(0.62, 0.80, 0.94)
		arena_env.ambient_light_color = Color(0.88, 0.92, 1.0)
		arena_env.ambient_light_energy = 0.58   # snow bounces plenty; higher ambient + the world sun pushed the floor past ACES white
		arena_env.glow_bloom = 0.05             # near-zero whole-frame haze: on an already-white scene the WW haze clips everything
		_arena_floor(Color(0.68, 0.74, 0.82), GTA + "up_snowsoft_col.jpg", GTA + "up_snow_nrm.jpg", 0.06)   # fresh snow; tint keeps it under ACES clip so the surface stays readable
	elif kind == "brawl":        # toy castle courtyard, warm afternoon
		grade_profile = "warm_pastel"
		arena_env.background_color = Color(0.62, 0.72, 0.92)
		arena_env.ambient_light_color = Color(0.96, 0.88, 0.78)
		arena_env.ambient_light_energy = 0.62
		arena_env.glow_bloom = 0.06
		_arena_floor(Color(0.84, 0.76, 0.68), GTA + "up_cliff_col.jpg", GTA + "up_cliff_nrm.jpg", 0.07)
	elif kind == "dustboss":     # the castle attic: lavender dusk through one round window
		grade_profile = "warm_pastel"
		arena_env.background_color = Color(0.30, 0.24, 0.42)
		arena_env.ambient_light_color = Color(0.86, 0.80, 0.98)
		arena_env.ambient_light_energy = 0.60
		arena_env.glow_bloom = 0.07
		_arena_floor(Color(0.80, 0.72, 0.66), GTA + "up_wood_col.jpg", GTA + "up_wood_nrm.jpg", 0.06)
	elif kind == "seek":         # sunny meadow
		grade_profile = "bright_pastel"
		arena_env.background_color = Color(0.30, 0.58, 0.78)
		arena_env.ambient_light_color = Color(0.76, 0.86, 0.78)
		arena_env.ambient_light_energy = 0.52
		arena_env.glow_intensity = 0.54
		arena_env.glow_bloom = 0.04
		_arena_floor(Color(0.56, 0.70, 0.50), GTA + "up_grass_col.jpg", GTA + "up_grass_nrm.jpg", 0.06)
	elif kind == "race":         # sunset sky
		grade_profile = "warm_pastel"
		arena_env.background_color = Color(0.82, 0.42, 0.30)
		arena_env.ambient_light_color = Color(0.94, 0.72, 0.62)
		arena_env.ambient_light_energy = 0.74
		_arena_floor(Color(0.72, 0.50, 0.40), GTA + "up_dirt_col.jpg", GTA + "up_dirt_nrm.jpg", 0.05)
	elif kind == "shop":         # warm wooden ship cabin
		arena_env.background_color = Color(0.06, 0.045, 0.025)
		arena_env.ambient_light_color = Color(1.0, 0.85, 0.6)
		arena_env.ambient_light_energy = 0.52
		arena_env.glow_intensity = 0.46
		arena_env.glow_bloom = 0.08
		_arena_floor(Color(0.9, 0.8, 0.65), GTA + "up_wood_col.jpg", GTA + "up_wood_nrm.jpg", 0.06)
	elif kind == "treasure":     # deep dark cavern
		arena_env.background_color = Color(0.025, 0.075, 0.12)
		arena_env.ambient_light_color = Color(0.42, 0.62, 0.82)
		arena_env.ambient_light_energy = 0.64
		arena_env.glow_intensity = 0.72
		arena_env.glow_bloom = 0.12
		_arena_floor(Color(0.55, 0.54, 0.6), GTA + "up_cliff_col.jpg", GTA + "up_cliff_nrm.jpg", 0.08)
	elif kind == "slide":        # bright icy sky — the chute builds its own geometry (no flat floor)
		grade_profile = "bright_pastel"
		# same anti-white-wash recipe as the snowy "fetch" yard: on an
		# already-white ice scene the WW screen-blend haze + hot ambient
		# clips the whole frame past ACES white (fully blown out on the
		# Android framebuffer, owner report 2026-07-13)
		arena_env.background_color = Color(0.48, 0.70, 0.90)
		arena_env.ambient_light_color = Color(0.86, 0.92, 1.0)
		arena_env.ambient_light_energy = 0.58
		arena_env.glow_bloom = 0.05
	elif kind == "fairyshoot":   # dreamy twilight fairy pond — the top-down pond builds its own geometry
		arena_env.background_color = Color(0.16, 0.10, 0.30)
		arena_env.ambient_light_color = Color(0.7, 0.65, 1.0)
		arena_env.ambient_light_energy = 0.58
		arena_env.glow_intensity = 0.52
		arena_env.glow_bloom = 0.08
	elif kind == "melody":      # Daddy Mermaid's enclosed underwater rainbow theater
		arena_env.background_color = Color(0.035, 0.09, 0.16)
		arena_env.ambient_light_color = Color(0.48, 0.78, 0.88)
		arena_env.ambient_light_energy = 0.68
		arena_env.glow_intensity = 0.72
		arena_env.glow_bloom = 0.12
		_arena_floor(Color(0.22, 0.42, 0.50), GTA + "up_wood_col.jpg", GTA + "up_wood_nrm.jpg", 0.06)
	else:
		arena_env.background_color = Color(0.06, 0.03, 0.12)
		arena_env.ambient_light_color = Color(0.8, 0.6, 1.0)
		arena_env.ambient_light_energy = 0.85
		_arena_floor(Color(0.62, 0.5, 0.72), GTA + "up_wood_col.jpg", GTA + "up_wood_nrm.jpg", 0.06)
	_speedy_glow_clamp(arena_env)   # re-run after the per-theme overrides so they respect speedy too
	if grade_profile.is_empty():
		_grade(arena_env)
	else:
		_apply_scene_grade(arena_env, grade_profile)
	we_node.environment = arena_env
	player.position = ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	# drop any leftover swim banking/pitch tilt: slide/fairyshoot early-return
	# in player._process, so a mid-turn lean would otherwise freeze on her
	player.rotation.x = 0.0
	player.rotation.z = 0.0
	_play_music(kind)

func _leave_arena() -> void:
	# covers both callers of the arena→reef cut: _end_game and the pause
	# menu's Leave Activity (pause_menu.gd)
	_fade_cut(_leave_arena_now)

func _leave_arena_now() -> void:
	# Hand her back to the world she came from. The fallbacks keep every
	# pre-existing caller (and any save restored mid-activity) behaving exactly
	# as before rather than dropping her into a null environment.
	we_node.environment = return_env if return_env != null else world_env
	player.position = return_pos
	player.vel = Vector3.ZERO
	_play_music(return_track if return_track != "" else "world")

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
