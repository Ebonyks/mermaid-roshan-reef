class_name OperaCareerWorld2D
extends CanvasLayer
## The runtime 2D/2.5D Pearl Opera career world.
##
## Each career supplies artwork and a phase list, while this class owns the
## common living-world language: full-bleed environment painting, Mermaid
## Roshan and a dressed rival on opposite sides, one-finger job gestures,
## parallel score/progress, audience energy and a graded curtain call.

const GestureSurface := preload("res://scripts/opera_gesture_surface.gd")
const WorldBackdrop := preload("res://scripts/opera_world_backdrop_2d.gd")
const NurseryCatch := preload("res://scripts/opera_nursery_catch.gd")
const StagePaths := preload("res://scripts/opera_stage_paths.gd")

const SLUGS := {
	"chef": "chef",
	"detective": "detective",
	"ballerina": "ballerina",
	"candymaker": "candymaker",
	"doctor": "doctor",
	"farmer": "farmer",
	"boxer": "boxer",
	"magician": "magician",
	"painter": "painter",
	"astronaut": "astronaut",
	"racer": "racer",
	"popstar": "popstar",
	"nursery": "nursery",
}

## Every career follows the same five-beat arc (OPERA_2D_REBUILD_2026-08-01.md):
## short imp scuffle -> learn the job -> do the job -> the imp captain steals
## the goal prop -> two-phase finale on the proscenium stage against the
## dressed rival. "bop" phases carry a "combat" dict; FINALE_START is always
## the first on-stage phase.
const PHASES := {
	"chef": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_chef_imps", "voice": "Mischief imps grabbed the spoons! Tap each imp to shoo them off!"},
		{"name": "POUR", "icon": "●", "mode": "hold", "goal": 5.0, "vo": "op_chef_pour", "voice": "Hold to pour the sparkling batter!"},
		{"name": "STIR", "icon": "↻", "mode": "circle", "goal": 4.0, "vo": "op_chef_stir", "voice": "Draw big circles to stir!"},
		{"name": "BAKE", "icon": "★", "mode": "timing", "goal": 6.0, "vo": "op_chef_bake", "voice": "Tap when the oven marker is green!"},
		{"name": "CAKE CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_chef_cake_chase", "voice": "The imp captain snatched the cake! Bop the crew to the stage door!"},
		{"name": "PIPE", "icon": "〰", "mode": "swipe", "goal": 7.0, "vo": "op_chef_pipe", "voice": "On stage! Swipe to pipe the frosting!"},
		{"name": "TOP", "icon": "●", "mode": "tap", "goal": 8.0, "vo": "op_chef_top", "voice": "Tap the bright toppings and win the cake back!"},
	],
	"detective": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_detective_imps", "voice": "Imps scattered the clue boxes! Tap each imp!"},
		{"name": "LENS", "icon": "?", "mode": "lens", "goal": 3.0, "vo": "op_detective_lens", "voice": "Drag the magic magnifying glass over the stage to find the glowing clues!"},
		{"name": "TRAIL", "icon": "→", "mode": "swipe", "goal": 7.5, "vo": "op_detective_trail", "voice": "Swipe along the footprint trail!"},
		{"name": "SEARCH", "icon": "★", "mode": "lens", "goal": 5.0, "vo": "op_detective_search", "voice": "Search the whole stage! Sweep your magnifying glass to find every hidden sparkle!"},
		{"name": "TIARA CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_detective_tiara_chase", "voice": "The imp captain ran off with the tiara case! Bop the lookouts!"},
		{"name": "MATCH", "icon": "◆", "mode": "choice", "goal": 5.0, "vo": "op_detective_match", "voice": "Match each clue to the glowing place!"},
		{"name": "NAME", "icon": "★", "mode": "timing", "goal": 2.0, "vo": "op_detective_name", "voice": "Tap when the spotlight shines on the answer!"},
	],
	"ballerina": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_ballerina_imps", "voice": "Imps are bouncing on the recital tiles! Tap them gently off!"},
		{"name": "WATCH", "icon": "♪", "mode": "hold", "goal": 4.0, "vo": "op_ballerina_watch", "voice": "Hold still and watch the glowing dance!"},
		{"name": "STEPS", "icon": "◆", "mode": "choice", "goal": 7.0, "vo": "op_ballerina_steps", "voice": "Tap the glowing dance step!"},
		{"name": "RIBBON", "icon": "〰", "mode": "swipe", "goal": 6.5, "vo": "op_ballerina_ribbon", "voice": "Trace the ribbon across the floor!"},
		{"name": "RIBBON CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_ballerina_ribbon_chase", "voice": "The imp captain tangled the ribbons! Twirl-bop the crew!"},
		{"name": "DUET", "icon": "★", "mode": "timing", "goal": 6.0, "vo": "op_ballerina_duet", "voice": "Step on the beat — tap in the green!"},
		{"name": "TWIRL", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_ballerina_twirl", "voice": "Draw circles for the grand twirl!"},
	],
	"candymaker": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_candymaker_imps", "voice": "Imps are juggling the gumdrops! Tap each imp!"},
		{"name": "SYRUP", "icon": "●", "mode": "hold", "goal": 4.5, "vo": "op_candymaker_syrup", "voice": "Hold the sparkling syrup bottle!"},
		{"name": "SORT", "icon": "◆", "mode": "choice", "goal": 7.0, "vo": "op_candymaker_sort", "voice": "Tap the glowing candy chute!"},
		{"name": "WRAP", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_candymaker_wrap", "voice": "Twist the wrappers in circles!"},
		{"name": "CANDY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_candymaker_candy_chase", "voice": "The imp captain rolled away the candy cart! Bop the crew!"},
		{"name": "PARADE", "icon": "★", "mode": "timing", "goal": 6.0, "vo": "op_candymaker_parade", "voice": "Tap when the parade cart is in the green!"},
		{"name": "SHARE", "icon": "●", "mode": "tap", "goal": 7.0, "vo": "op_candymaker_share", "voice": "Tap a candy for every friend in the crowd!"},
	],
	"doctor": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_doctor_imps", "voice": "Imps are hiding the bandages! Tap each imp!"},
		{"name": "WASH", "icon": "●", "mode": "hold", "goal": 4.5, "vo": "op_doctor_wash", "voice": "Hold to wash Doctor Roshan's hands!"},
		{"name": "FIND", "icon": "?", "mode": "choice", "goal": 6.0, "vo": "op_doctor_find", "voice": "Find the plushy with the glowing ouch!"},
		{"name": "X-RAY", "icon": "◆", "mode": "tap", "goal": 6.0, "vo": "op_doctor_x_ray", "voice": "Tap the glowing cracked bone!"},
		{"name": "PLUSHY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_doctor_plushy_chase", "voice": "The imp captain borrowed the plushy patient! Bop the crew to the stage!"},
		{"name": "CAST", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_doctor_cast", "voice": "Draw circles to wrap the soft cast!"},
		{"name": "BANDAGE", "icon": "〰", "mode": "swipe", "goal": 6.5, "vo": "op_doctor_bandage", "voice": "Swipe the stretchy bandage around!"},
	],
	"farmer": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_farmer_imps", "voice": "Imps are splashing in the mud! Tap each imp!"},
		{"name": "PLANT", "icon": "◆", "mode": "choice", "goal": 6.0, "vo": "op_farmer_plant", "voice": "Tap the glowing garden row and plant the seed!"},
		{"name": "FEED", "icon": "★", "mode": "timing", "goal": 6.0, "vo": "op_farmer_feed", "voice": "Tap when the veggie reaches a piggy!"},
		{"name": "MUD HOP", "icon": "●", "mode": "hold", "goal": 4.0, "vo": "op_farmer_mud_hop", "voice": "Hold to wind up... and make a big mud hop!"},
		{"name": "PIGGY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_farmer_piggy_chase", "voice": "The imp captain opened the piggy gate! Bop the crew!"},
		{"name": "HERD", "icon": "↔", "mode": "swipe", "goal": 7.0, "vo": "op_farmer_herd", "voice": "Sweep back and forth to guide the herd on stage!"},
		{"name": "PICNIC", "icon": "●", "mode": "tap", "goal": 7.0, "vo": "op_farmer_picnic", "voice": "Tap a snack for every happy piggy!"},
	],
	"boxer": [
		{"name": "SPAR", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_boxer_spar", "voice": "Friendly sparring! Bop each padded imp!"},
		{"name": "JAB", "icon": "★", "mode": "timing", "goal": 7.0, "vo": "op_boxer_jab", "voice": "Tap in the green to punch the padded gloves!"},
		{"name": "DUCK", "icon": "↓", "mode": "swipe", "goal": 4.0, "dir": "down", "vo": "op_boxer_duck", "voice": "Swipe down to duck the friendly counter!"},
		{"name": "BELL CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_boxer_bell_chase", "voice": "The imp captain grabbed the championship belt and rang the big bell! Win it back in the title match!"},
		{"name": "ROUND", "icon": "◆", "mode": "choice", "goal": 8.0, "vo": "op_boxer_round", "voice": "Punch the glowing pad — left, middle, right!"},
		{"name": "BELT", "icon": "★", "mode": "tap", "goal": 1.0, "vo": "op_boxer_belt", "voice": "Tap the championship belt for the winner!"},
	],
	"magician": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_magician_imps", "voice": "Imps popped out of the magic hats! Tap each imp!"},
		{"name": "VANISH", "icon": "●", "mode": "hold", "goal": 4.2, "vo": "op_magician_vanish", "voice": "Hold the wand to make Lamba vanish!"},
		{"name": "TRACK", "icon": "?", "mode": "choice", "goal": 6.0, "vo": "op_magician_track", "voice": "Follow the glowing hat through the shuffle!"},
		{"name": "ROPE", "icon": "〰", "mode": "swipe", "goal": 6.5, "vo": "op_magician_rope", "voice": "Swipe the magic rope into one long ribbon!"},
		{"name": "LAMBA CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_magician_bunny_chase", "voice": "The imp captain hid Lamba! Bop the crew to the stage!"},
		{"name": "CABINET", "icon": "★", "mode": "timing", "goal": 6.0, "vo": "op_magician_cabinet", "voice": "Tap on the star flashes to open the cabinet!"},
		{"name": "PORTAL", "icon": "↻", "mode": "circle", "goal": 4.0, "vo": "op_magician_portal", "voice": "Draw circles to open the giant star portal!"},
	],
	"painter": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_painter_imps", "voice": "Imps splashed the paint pots! Tap each imp!"},
		{"name": "SKETCH", "icon": "〰", "mode": "swipe", "goal": 6.5, "vo": "op_painter_sketch", "voice": "Trace the sunrise sketch!"},
		{"name": "FILL", "icon": "●", "mode": "hold", "goal": 4.5, "vo": "op_painter_fill", "voice": "Hold to fill the glowing shape!"},
		{"name": "SPLAT", "icon": "●", "mode": "tap", "goal": 7.0, "vo": "op_painter_splat", "voice": "Tap five happy splatters!"},
		{"name": "SUNRISE CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_painter_sunrise_chase", "voice": "The imp captain took the sunrise painting! Bop the crew!"},
		{"name": "STROKES", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_painter_strokes", "voice": "Paint grand circles for the crowd!"},
		{"name": "REVEAL", "icon": "★", "mode": "choice", "goal": 1.0, "vo": "op_painter_reveal", "voice": "Tap the glowing frame to hang the sunrise!"},
	],
	"astronaut": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_astronaut_imps", "voice": "Imps are floating around the rocket bay! Tap each imp!"},
		{"name": "PIPES", "icon": "◆", "mode": "choice", "goal": 6.0, "vo": "op_astronaut_pipes", "voice": "Tap the glowing pipe to route the bubbles!"},
		{"name": "PATCH", "icon": "●", "mode": "tap", "goal": 6.0, "vo": "op_astronaut_patch", "voice": "Tap the sparkle leaks to patch them!"},
		{"name": "VALVE", "icon": "↻", "mode": "circle", "goal": 3.6, "vo": "op_astronaut_valve", "voice": "Draw circles to turn the launch valve!"},
		{"name": "ROCKET CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_astronaut_rocket_chase", "voice": "The imp captain scooped up the little rocket and pressed the silly button! Bop the crew!"},
		{"name": "BOOST", "icon": "★", "mode": "timing", "goal": 6.0, "vo": "op_astronaut_boost", "voice": "Tap the boosters in the green!"},
		{"name": "LAUNCH", "icon": "●", "mode": "hold", "goal": 5.0, "vo": "op_astronaut_launch", "voice": "Hold through the countdown... and launch!"},
	],
	"racer": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_racer_imps", "voice": "Imps rolled tires onto the track! Tap each imp!"},
		{"name": "STEER", "icon": "↔", "mode": "swipe", "goal": 9.0, "vo": "op_racer_steer", "voice": "Swipe to steer through the coral gates!"},
		{"name": "TURBO", "icon": "★", "mode": "timing", "goal": 7.0, "vo": "op_racer_turbo", "voice": "Tap TURBO when the marker hits green!"},
		{"name": "TROPHY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_racer_trophy_chase", "voice": "The imp captain grabbed the shell trophy! Clear the track!"},
		{"name": "LAP TWO", "icon": "↻", "mode": "circle", "goal": 4.0, "vo": "op_racer_lap_two", "voice": "Loop the loop! Draw big racing circles!"},
		{"name": "FINISH", "icon": "●", "mode": "tap", "goal": 7.0, "vo": "op_racer_finish", "voice": "Tap the zoom strips and cross the line!"},
	],
	"nursery": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_nursery_imps", "voice": "Mischief imps are tickling the babies awake! Tap each imp!"},
		{"name": "WASH HANDS", "icon": "●", "mode": "hold", "goal": 3.6, "vo": "op_nursery_wash", "voice": "Nursery Nurse Roshan! Hold the bubbly basin to wash your hands first!"},
		{"name": "CATCH BABIES", "icon": "↓", "mode": "catch", "goal": 5.0, "speaker": "Faron", "vo": "op_nursery_catch", "voice": "Slide the soft cradle under five falling babies! Pillows keep every miss safe."},
		{"name": "FEED", "icon": "♡", "mode": "hold", "goal": 4.2, "speaker": "Faron", "vo": "op_nursery_feed", "voice": "Hold the warm bottle while Roshan and Faron feed every baby!"},
		{"name": "BABY CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_nursery_baby_chase", "voice": "The imp captain is playing peek-a-boo with the babies! Bop the crew to the stage!"},
		{"name": "BURP", "icon": "○", "mode": "timing", "goal": 4.0, "vo": "op_nursery_burp", "voice": "Tap in the green for gentle burp-pats!"},
		{"name": "BEDTIME", "icon": "☾", "mode": "swipe", "goal": 6.0, "speaker": "Faron", "vo": "op_nursery_bedtime", "voice": "Swipe the blankets down and tuck every sleepy baby into bed!"},
	],
	"popstar": [
		{"name": "IMPS!", "icon": "!", "mode": "bop", "goal": 5.0, "combat": {"count": 5}, "vo": "op_popstar_imps", "voice": "Imps are drumming on the speakers! Tap each imp!"},
		{"name": "SOUND CHECK", "icon": "●", "mode": "hold", "goal": 4.5, "vo": "op_popstar_sound_check", "voice": "Hold the microphone for sound check!"},
		{"name": "DANCE", "icon": "◆", "mode": "choice", "goal": 8.0, "vo": "op_popstar_dance", "voice": "Tap the glowing dance arrow!"},
		{"name": "MIC CHASE", "icon": "!", "mode": "bop", "goal": 10.0, "combat": {"count": 8, "captain": true}, "vo": "op_popstar_mic_chase", "voice": "The imp captain unplugged the microphone! Bop the mischief band!"},
		{"name": "RHYTHM", "icon": "♪", "mode": "timing", "goal": 7.0, "vo": "op_popstar_rhythm", "voice": "Tap each rainbow note in the green!"},
		{"name": "ENCORE", "icon": "↻", "mode": "circle", "goal": 4.2, "vo": "op_popstar_encore", "voice": "Draw a big encore spin for the crowd!"},
	],
}

const FINALE_START := {
	"chef": 5,
	"detective": 5,
	"ballerina": 5,
	"candymaker": 5,
	"doctor": 5,
	"farmer": 5,
	"boxer": 4,
	"magician": 5,
	"painter": 5,
	"astronaut": 5,
	"racer": 4,
	"popstar": 4,
	"nursery": 5,
}

## Career goal prop shown at the workbench until the imp captain steals it in
## beat four; celebrate() brings it back for the curtain call. Textures are
## codex flat-package cards matted by tools/prepare_opera_2d_props.py; a
## missing file simply hides the prop.
const GOAL_PROPS := {
	"chef": "goal_chef",
	"detective": "goal_detective",
	"ballerina": "goal_ballerina",
	"candymaker": "goal_candymaker",
	"doctor": "goal_doctor",
	"farmer": "goal_farmer",
	"boxer": "goal_boxer",
	"magician": "goal_magician",
	"painter": "goal_painter",
	"astronaut": "goal_astronaut",
	"racer": "goal_racer",
	"popstar": "goal_popstar",
	"nursery": "goal_nursery",
}
var m: ReefMain
var config: Dictionary = {}
var competition: OperaCompetition
var win_callback: Callable
var career_id := ""
var phases: Array = []
var phase_index := 0
var phase_progress := 0.0
var active := true
var guided := false
var reveal_t := 0.0
var elapsed := 0.0
var timing_phase := 0.0
var choice_target := 1

var phase_gap := 0.0
var bop_time := 0.0
var steal_index := -1
var captain_pending := false
var idle_t := 0.0
var score_cool := 0.0
var bop_puff_texture: Texture2D = null
var nursery_catch: OperaNurseryCatch = null
## Stage geography: the painted world's walkable route and task stations.
var stage_points := PackedVector2Array()
var station_list: Array[Dictionary] = []
var station_nodes: Array[Control] = []
var station_for_phase: Dictionary = {}
## Roaming stage combat (replaces the old panel scuffle).
var combat_layer: Control = null
var combat_fx: Control = null
var combat_imps: Array[Dictionary] = []
var combat_marks: Array[Dictionary] = []
var imp_idle_texture: Texture2D = null
var imp_bopped_texture: Texture2D = null
var imp_bow_texture: Texture2D = null
var captain_idle_texture: Texture2D = null
var captain_bopped_texture: Texture2D = null
var captain_bow_texture: Texture2D = null
var fx_telegraph_ring_texture: Texture2D = null
var fx_telegraph_bang_texture: Texture2D = null
var fx_slash_arc_texture: Texture2D = null
var fx_dust_puff_texture: Texture2D = null
var fx_stolen_sparkle_texture: Texture2D = null
var fx_dizzy_stars_texture: Texture2D = null
var swipe_stroke := 0
var combat_miss_cool := 0.0
var imp_state_cache: Dictionary = {}
## The shared mischief-imp brain (scripts/imp_ai.gd) drives the crew: who
## closes in, who telegraphs, who hangs back. All state stays here.
var imp_brain: ImpAI = null
var combat_warned := false
## Magnifier lens phases (detective's masked reveal over the whole stage).
var lens_layer: Control = null
var lens_pos := Vector2(640, 400)
var lens_clues := PackedVector2Array()
var lens_found: Array[bool] = []
var lens_dwell := 0.0
var lens_target := -1
var lens_demo := true
var task_frame_texture: Texture2D = null
var station_marker_texture: Texture2D = null
var magnifier_texture: Texture2D = null

var root: Control
var backdrop_node: OperaWorldBackdrop2D
var action_panel: ColorRect
var prop_rect: TextureRect
var player_actor: TextureRect
var rival_actor: TextureRect
var player_bar: ProgressBar
var rival_bar: ProgressBar
var title_label: Label
var phase_label: Label
var score_label: Label
var timer_label: Label
var player_name_label: Label
var rival_name_label: Label
var crowd_label: Label
var surface: OperaGestureSurface
var phase_fill: ProgressBar
var audience: Array[TextureRect] = []
var confetti: Array[ColorRect] = []


func setup(main: ReefMain, act_config: Dictionary, director: OperaCompetition, on_win: Callable) -> void:
	m = main
	config = act_config
	competition = director
	competition.pause()
	win_callback = on_win
	career_id = String(config.get("costume", "chef"))
	phases = (PHASES.get(career_id, []) as Array).duplicate(true)
	steal_index = -1
	for index in range(phases.size()):
		var phase := phases[index] as Dictionary
		if String(phase.get("mode", "")) == "bop" and bool((phase.get("combat", {}) as Dictionary).get("captain", false)):
			steal_index = index
	layer = 38
	_build_world()
	_show_phase()


func _full_rect(control: Control) -> void:
	control.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)


func _label(text: String, font_size: int, colour: Color = Color.WHITE) -> Label:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", colour)
	label.add_theme_color_override("font_shadow_color", Color(0.03, 0.02, 0.12, 0.92))
	label.add_theme_constant_override("shadow_offset_x", 3)
	label.add_theme_constant_override("shadow_offset_y", 3)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	return label


func _build_world() -> void:
	root = Control.new()
	root.name = "OperaCareerWorld2D"
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_full_rect(root)
	add_child(root)
	task_frame_texture = _load_if_exists("res://assets/opera/worlds/ui/task_card_frame.png")
	station_marker_texture = _load_if_exists("res://assets/opera/worlds/ui/station_marker.png")
	magnifier_texture = _load_if_exists("res://assets/opera/worlds/ui/magnifier.png")

	backdrop_node = WorldBackdrop.new() as OperaWorldBackdrop2D
	backdrop_node.name = "CareerWorldBackdrop"
	_full_rect(backdrop_node)
	root.add_child(backdrop_node)
	backdrop_node.setup(career_id)

	var shade := ColorRect.new()
	shade.color = Color(0.025, 0.025, 0.11, 0.10)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_full_rect(shade)
	root.add_child(shade)

	stage_points = StagePaths.path_points(career_id)
	station_list = StagePaths.stations(career_id)
	_assign_stations()
	_build_station_markers()

	var top := ColorRect.new()
	top.color = Color(0.025, 0.025, 0.11, 0.84)
	top.position = Vector2(18, 14)
	top.size = Vector2(1244, 124)
	top.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(top)

	title_label = _label(String(competition.spec.get("world", String(config.get("name", "CAREER CUP")))), 28, Color(1.0, 0.91, 0.55))
	title_label.position = Vector2(24, 8)
	title_label.size = Vector2(1196, 38)
	top.add_child(title_label)

	player_bar = ProgressBar.new()
	player_bar.position = Vector2(30, 58)
	player_bar.size = Vector2(430, 28)
	player_bar.show_percentage = false
	top.add_child(player_bar)
	rival_bar = ProgressBar.new()
	rival_bar.position = Vector2(784, 58)
	rival_bar.size = Vector2(430, 28)
	rival_bar.show_percentage = false
	top.add_child(rival_bar)
	score_label = _label("0  ★  0", 25)
	score_label.position = Vector2(470, 51)
	score_label.size = Vector2(304, 42)
	top.add_child(score_label)
	timer_label = _label("", 21, Color(0.72, 0.94, 1.0))
	timer_label.position = Vector2(490, 88)
	timer_label.size = Vector2(264, 30)
	top.add_child(timer_label)
	player_name_label = _label("MERMAID ROSHAN", 17, Color(1.0, 0.82, 0.94))
	player_name_label.position = Vector2(30, 87)
	player_name_label.size = Vector2(430, 28)
	top.add_child(player_name_label)
	rival_name_label = _label("%s IMP" % String(config.get("career", "RIVAL")).to_upper(), 17, Color(0.82, 0.76, 1.0))
	rival_name_label.position = Vector2(784, 87)
	rival_name_label.size = Vector2(430, 28)
	top.add_child(rival_name_label)

	player_actor = _actor("res://assets/opera/worlds/actors/roshan_%s.png" % career_id)
	player_actor.size = Vector2(250, 288)
	_place_on_stage(player_actor, StagePaths.point_along(stage_points, 0.08))
	root.add_child(player_actor)
	var partner_path := "res://assets/opera/worlds/actors/rival_%s.png" % career_id
	if career_id == "nursery":
		partner_path = "res://assets/opera/worlds/actors/faron_nursery.png"
	rival_actor = _actor(partner_path)
	rival_actor.size = Vector2(250, 270)
	_place_on_stage(rival_actor, StagePaths.point_along(stage_points, 0.92))
	root.add_child(rival_actor)
	if career_id == "nursery":
		player_name_label.text = "NURSE ROSHAN"
		rival_name_label.text = "NURSE FARON"
	_set_finale_visible(false)

	prop_rect = TextureRect.new()
	var prop_path := "res://assets/opera/worlds/props/%s.png" % String(GOAL_PROPS.get(career_id, ""))
	if ResourceLoader.exists(prop_path):
		prop_rect.texture = load(prop_path) as Texture2D
	prop_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	prop_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	prop_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	prop_rect.position = Vector2(890, 330)
	prop_rect.size = Vector2(280, 230)
	prop_rect.visible = false
	root.add_child(prop_rect)

	action_panel = ColorRect.new()
	# transparent host; the storybook card frame is drawn in _draw_task_card
	action_panel.color = Color(0, 0, 0, 0)
	action_panel.position = Vector2(430, 160)
	action_panel.size = Vector2(420, 430)
	action_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	action_panel.draw.connect(_draw_task_card)
	root.add_child(action_panel)
	phase_label = _label("", 30, Color("#382485"))
	phase_label.position = Vector2(10, 8)
	phase_label.size = Vector2(400, 62)
	action_panel.add_child(phase_label)
	surface = GestureSurface.new()
	surface.position = Vector2(24, 78)
	surface.size = Vector2(372, 266)
	surface.gesture.connect(_on_gesture)
	# The scuffle crews wear the career's special imp costume (the accepted
	# costume-sheet slices). Co-op careers keep the dedicated mischief-imp
	# sprites (the partner is not an imp); placeholders are the last fallback.
	if competition != null and competition.is_cooperative():
		if ResourceLoader.exists("res://assets/opera/worlds/actors/imp_mischief.png"):
			surface.bop_texture = load("res://assets/opera/worlds/actors/imp_mischief.png") as Texture2D
		if ResourceLoader.exists("res://assets/opera/worlds/actors/imp_captain.png"):
			surface.bop_captain_texture = load("res://assets/opera/worlds/actors/imp_captain.png") as Texture2D
	elif rival_actor != null and rival_actor.texture != null:
		surface.bop_texture = rival_actor.texture
		surface.bop_captain_texture = rival_actor.texture
	else:
		if ResourceLoader.exists("res://assets/opera/worlds/actors/imp_mischief.png"):
			surface.bop_texture = load("res://assets/opera/worlds/actors/imp_mischief.png") as Texture2D
		if ResourceLoader.exists("res://assets/opera/worlds/actors/imp_captain.png"):
			surface.bop_captain_texture = load("res://assets/opera/worlds/actors/imp_captain.png") as Texture2D
	if ResourceLoader.exists("res://assets/opera/worlds/props/fx_bop_puff.png"):
		bop_puff_texture = load("res://assets/opera/worlds/props/fx_bop_puff.png") as Texture2D
	action_panel.add_child(surface)
	if career_id == "nursery":
		nursery_catch = NurseryCatch.new() as OperaNurseryCatch
		nursery_catch.name = "NurseryCatchSurface"
		nursery_catch.position = Vector2(24, 78)
		nursery_catch.size = Vector2(372, 266)
		nursery_catch.visible = false
		nursery_catch.baby_caught.connect(_on_nursery_baby_caught)
		nursery_catch.baby_missed.connect(_on_nursery_baby_missed)
		action_panel.add_child(nursery_catch)
	phase_fill = ProgressBar.new()
	phase_fill.position = Vector2(24, 362)
	phase_fill.size = Vector2(372, 40)
	phase_fill.show_percentage = false
	phase_fill.mouse_filter = Control.MOUSE_FILTER_IGNORE
	action_panel.add_child(phase_fill)

	combat_layer = Control.new()
	combat_layer.name = "StageCombatLayer"
	_full_rect(combat_layer)
	combat_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	combat_layer.gui_input.connect(_combat_input)
	root.add_child(combat_layer)
	# telegraph rings, slash arcs and stolen-sparkle glints draw above the
	# crew but never take input — the imps themselves stay tappable
	combat_fx = Control.new()
	combat_fx.name = "StageCombatFX"
	_full_rect(combat_fx)
	combat_fx.mouse_filter = Control.MOUSE_FILTER_IGNORE
	combat_fx.draw.connect(_draw_combat_fx)
	root.add_child(combat_fx)
	imp_idle_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_mischief.png")
	imp_bopped_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_mischief_bopped.png")
	imp_bow_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_mischief_bow.png")
	captain_idle_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_captain.png")
	captain_bopped_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_captain_bopped.png")
	captain_bow_texture = _load_if_exists("res://assets/opera/worlds/actors/imp_captain_bow.png")
	fx_telegraph_ring_texture = _load_if_exists("res://assets/opera/worlds/props/fx_telegraph_ring.png")
	fx_telegraph_bang_texture = _load_if_exists("res://assets/opera/worlds/props/fx_telegraph_bang.png")
	fx_slash_arc_texture = _load_if_exists("res://assets/opera/worlds/props/fx_slash_arc.png")
	fx_dust_puff_texture = _load_if_exists("res://assets/opera/worlds/props/fx_dust_puff.png")
	fx_stolen_sparkle_texture = _load_if_exists("res://assets/opera/worlds/props/fx_stolen_sparkle.png")
	fx_dizzy_stars_texture = _load_if_exists("res://assets/opera/worlds/props/fx_dizzy_stars.png")
	if not competition.is_cooperative() and rival_actor != null and rival_actor.texture != null:
		# crews wear the career's special imp costume; the base-imp set keeps
		# the bopped state until per-costume state sprites land (codex handoff)
		imp_idle_texture = rival_actor.texture
		captain_idle_texture = rival_actor.texture

	lens_layer = Control.new()
	lens_layer.name = "MagnifierLensLayer"
	_full_rect(lens_layer)
	lens_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	lens_layer.visible = false
	lens_layer.gui_input.connect(_lens_input)
	lens_layer.draw.connect(_draw_lens_layer)
	root.add_child(lens_layer)

	crowd_label = _label("●  ●  ●  ●  ●", 30, Color(1.0, 0.84, 0.5))
	crowd_label.position = Vector2(430, 595)
	crowd_label.size = Vector2(420, 42)
	root.add_child(crowd_label)
	_build_audience()


func _actor(path: String) -> TextureRect:
	var actor := TextureRect.new()
	actor.texture = load(path) as Texture2D
	actor.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	actor.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	actor.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return actor


func _load_if_exists(path: String) -> Texture2D:
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


func _place_on_stage(actor: Control, feet: Vector2) -> void:
	# anchor a stage character by its feet with gentle painted-depth scaling
	var depth := clampf(0.62 + (feet.y / 720.0) * 0.55, 0.62, 1.1)
	actor.scale = Vector2(depth, depth)
	actor.position = feet - Vector2(actor.size.x * 0.5 * depth, actor.size.y * depth - 12.0)


func _assign_stations() -> void:
	# non-combat phases visit the painted stations left-to-right in order
	station_for_phase = {}
	if station_list.is_empty():
		return
	var station_index := 0
	for index in range(phases.size()):
		var mode := String((phases[index] as Dictionary).get("mode", ""))
		if mode == "bop":
			continue
		station_for_phase[index] = mini(station_index, station_list.size() - 1)
		station_index += 1


func _build_station_markers() -> void:
	for station: Dictionary in station_list:
		var marker := Control.new()
		marker.mouse_filter = Control.MOUSE_FILTER_IGNORE
		marker.position = station.get("pos", Vector2(640, 480)) as Vector2
		marker.draw.connect(_draw_station_marker.bind(marker))
		root.add_child(marker)
		station_nodes.append(marker)


func _draw_task_card() -> void:
	# the exact StorybookUI menu language (see the UI extraction report):
	# paper fill, violet drop shadow, PURPLE->PURPLE_DEEP contour, gold
	# title ribbon and corner pearls — a task card that matches the menus
	var card_size := action_panel.size
	var rect := Rect2(Vector2.ZERO, card_size)
	if task_frame_texture != null:
		action_panel.draw_rect(rect.grow(-20.0), Color("#e6f5ff"), true)
		action_panel.draw_texture_rect(task_frame_texture, rect, false)
		return
	var frame := StyleBoxFlat.new()
	frame.bg_color = Color("#e6f5ff")
	frame.set_border_width_all(5)
	frame.border_color = Color("#4b33a0")
	frame.set_corner_radius_all(44)
	frame.shadow_color = Color(0.19, 0.10, 0.48, 0.34)
	frame.shadow_size = 14
	frame.shadow_offset = Vector2(0, 8)
	frame.draw(action_panel.get_canvas_item(), rect)
	var ribbon := StyleBoxFlat.new()
	ribbon.bg_color = Color("#fff7db")
	ribbon.set_border_width_all(4)
	ribbon.border_color = Color("#ffc74d").lerp(Color("#382485"), 0.62)
	ribbon.set_corner_radius_all(32)
	ribbon.draw(action_panel.get_canvas_item(), Rect2(20.0, 14.0, card_size.x - 40.0, 56.0))
	for corner: Vector2 in [
		Vector2(26, 26), Vector2(card_size.x - 26.0, 26),
		Vector2(26, card_size.y - 26.0), Vector2(card_size.x - 26.0, card_size.y - 26.0),
	]:
		action_panel.draw_circle(corner, 9.0, Color("#382485"))
		action_panel.draw_circle(corner, 6.5, Color("#b3f7ff"))
		action_panel.draw_circle(corner + Vector2(-2, -2), 2.0, Color.WHITE)


func _draw_station_marker(marker: Control) -> void:
	var index := station_nodes.find(marker)
	var current := int(station_for_phase.get(phase_index, -1)) == index
	var pulse := (sin(elapsed * 4.2) + 1.0) * 0.5 if current else 0.0
	var base := Color(1.0, 0.86, 0.42, 0.55 + pulse * 0.35) if current else Color(1.0, 1.0, 1.0, 0.22)
	if station_marker_texture != null:
		var marker_size := Vector2(96.0, 192.0) * (1.0 + pulse * 0.06)
		var marker_rect := Rect2(Vector2(-marker_size.x * 0.5, -marker_size.y + 14.0), marker_size)
		marker.draw_texture_rect(station_marker_texture, marker_rect, false, base)
		return
	marker.draw_circle(Vector2.ZERO, 26.0 + pulse * 7.0, Color(base, base.a * 0.35))
	marker.draw_arc(Vector2.ZERO, 26.0 + pulse * 7.0, 0.0, TAU, 32, base, 5.0)
	if current:
		marker.draw_circle(Vector2.ZERO, 8.0, Color(1.0, 0.97, 0.85))


func _glide_roshan_to(feet: Vector2, duration: float = 1.3) -> void:
	var depth := clampf(0.62 + (feet.y / 720.0) * 0.55, 0.62, 1.1)
	var target := feet - Vector2(player_actor.size.x * 0.5 * depth, player_actor.size.y * depth - 12.0)
	player_actor.flip_h = target.x < player_actor.position.x
	var tween := player_actor.create_tween()
	tween.tween_property(player_actor, "position", target, duration).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.parallel().tween_property(player_actor, "scale", Vector2(depth, depth), duration)


func _build_audience() -> void:
	var portraits := [
		"res://assets/characters/friends/daddy.webp",
		"res://assets/characters/friends/huluu.png",
		"res://assets/characters/friends/mama_baby.png",
		"res://assets/characters/friends/flower_friend.png",
		"res://assets/characters/friends/wacky_chuck.png",
		"res://assets/characters/friends/two_friends.png",
	]
	for index in range(portraits.size()):
		var fan := _actor(String(portraits[index]))
		fan.position = Vector2(18.0 + float(index) * 207.0, 592.0)
		fan.size = Vector2(116, 126)
		fan.modulate = Color(1.0, 1.0, 1.0, 0.96)
		root.add_child(fan)
		audience.append(fan)


func _widget_template(phase: Dictionary) -> String:
	var mode := String(phase.get("mode", ""))
	var name := String(phase.get("name", ""))
	match mode:
		"timing":
			return "gauge" if career_id in ["chef", "astronaut", "racer"] else "track"
		"hold":
			if name in ["WASH", "WASH HANDS"]:
				return "basin"
			if name in ["POUR", "SYRUP", "FILL", "FEED"]:
				return "pour"
			return "charge"
		"circle":
			return "crank"
		"swipe":
			return "push" if name in ["HERD", "DUCK", "STEER", "BEDTIME"] else "trace"
		"tap":
			return "target"
		"choice":
			return "lanes"
		"catch":
			return "catch"
	return ""


func _show_phase() -> void:
	if phase_index >= phases.size():
		active = false
		if win_callback.is_valid():
			win_callback.call()
		return
	if phase_index == _finale_start():
		competition.begin()
		_set_finale_visible(true)
		# a longer sting as the proscenium curtain rises; any touch skips it
		phase_gap = 2.6
	elif phase_index < _finale_start():
		_set_finale_visible(false)
		if phase_index > 0:
			phase_gap = 1.0
	else:
		phase_gap = 1.0
	if backdrop_node != null:
		# the captain scuffle already happens at the stage door, so the
		# proscenium frames both the big battle and the finale contest
		var stage_from := steal_index if steal_index >= 0 else _finale_start()
		backdrop_node.set_stage(phase_index >= stage_from)
	phase_progress = 0.0
	idle_t = 0.0
	var phase := phases[phase_index] as Dictionary
	var mode_name := String(phase.get("mode", "tap"))
	var is_bop := mode_name == "bop"
	var is_lens := mode_name == "lens"
	var accent := Color(competition.spec.get("accent", Color(1.0, 0.62, 0.8)))
	choice_target = (phase_index + int(competition.rival_step)) % 3
	_apply_panel_layout(phase)
	if is_bop:
		_start_stage_combat(phase.get("combat", {}) as Dictionary)
	else:
		_clear_stage_combat()
		var station_index := int(station_for_phase.get(phase_index, -1))
		if station_index >= 0 and station_index < station_list.size():
			_glide_roshan_to(station_list[station_index].get("pos", Vector2(640, 480)) as Vector2)
	if is_lens:
		_start_lens_phase(phase)
	elif lens_layer != null:
		lens_layer.visible = false
		lens_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	for marker in station_nodes:
		marker.queue_redraw()
	var is_nursery_catch := career_id == "nursery" and mode_name == "catch"
	surface.visible = not is_nursery_catch
	if nursery_catch != null:
		nursery_catch.visible = is_nursery_catch
		if is_nursery_catch:
			nursery_catch.start(int(ceilf(float(phase.get("goal", 5.0)))))
		else:
			nursery_catch.stop()
	var template := _widget_template(phase)
	var context := "%s_%s" % [template, career_id] if not template.is_empty() else ""
	surface.configure(mode_name, accent, choice_target, context)
	surface.set_fill(0.0)
	match String(phase.get("dir", "")):
		"down":
			surface.swipe_dir = Vector2.DOWN
			surface.swipe_require_dir = true
		"up":
			surface.swipe_dir = Vector2.UP
			surface.swipe_require_dir = true
	if prop_rect != null:
		if phase_index == steal_index and prop_rect.visible:
			# the theft is a visible event: the captain hauls the prop away
			var flee := prop_rect.create_tween()
			flee.tween_property(prop_rect, "position", Vector2(1210.0, -180.0), 0.9).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
			flee.parallel().tween_property(prop_rect, "size", Vector2(140, 115), 0.9)
			flee.tween_callback(func() -> void:
				prop_rect.visible = false
				prop_rect.position = Vector2(890, 330)
				prop_rect.size = Vector2(280, 230))
		else:
			prop_rect.visible = prop_rect.texture != null and phase_index > 0 \
				and (steal_index < 0 or phase_index < steal_index)
	phase_label.text = "%s   %s" % [String(phase.get("icon", "★")), String(phase.get("name", "PLAY"))]
	phase_fill.value = 0.0
	if m != null:
		m.show_msg(String(phase.get("speaker", "Roshan")), String(phase.get("voice", "Follow the golden sparkle!")), String(phase.get("vo", "hint")))


func _apply_panel_layout(phase: Dictionary) -> void:
	if action_panel == null:
		return
	var mode := String(phase.get("mode", "tap"))
	if mode == "bop" or mode == "lens":
		# stage-wide beats play on the painting itself — no card at all
		action_panel.visible = false
		return
	action_panel.visible = true
	action_panel.position = _card_position_near_station()
	action_panel.size = Vector2(440, 384)
	phase_label.size = Vector2(420, 56)
	surface.position = Vector2(24, 70)
	surface.size = Vector2(392, 232)
	phase_fill.position = Vector2(24, 318)
	phase_fill.size = Vector2(392, 34)
	action_panel.queue_redraw()


func _card_position_near_station() -> Vector2:
	# dock the task card beside the phase's station, clamped on screen and
	# clear of the top HUD strip and the audience row
	var station_index := int(station_for_phase.get(phase_index, -1))
	var anchor := Vector2(640, 430)
	if station_index >= 0 and station_index < station_list.size():
		anchor = station_list[station_index].get("pos", anchor) as Vector2
	var pos := anchor + Vector2(60.0 if anchor.x < 640.0 else -500.0, -260.0)
	pos.x = clampf(pos.x, 24.0, 1280.0 - 464.0)
	pos.y = clampf(pos.y, 150.0, 720.0 - 384.0 - 130.0)
	return pos


## Screen-space tuning for the shared imp brain. The brain thinks in the
## caller's own units, so these are PIXELS on the 1280x720 stage: a crew
## that closes from ~a third of the stage away, telegraphs for most of a
## second, and lunges about two imp-widths.
const IMP_BRAIN_TUNE := {
	"strike_range": 300.0,
	"stand_off": 186.0,
	"contact": 104.0,
	"speed": 132.0,
	"charge_speed": 520.0,
	"flee_speed": 250.0,
	"windup": 0.95,
	"charge_time": 0.4,
	"slash_time": 0.28,
	"recover": 1.15,
	"stagger": 0.5,
	"guard_time": 0.8,
	"taunt_time": 0.85,
	"flee_time": 1.1,
	"cool_min": 2.4,
	"cool_max": 5.0,
	"max_attackers": 2,
	"captain_scale": 1.2,
}


func _start_stage_combat(combat: Dictionary) -> void:
	_clear_stage_combat()
	bop_time = 0.0
	swipe_stroke = 0
	combat_warned = false
	combat_layer.mouse_filter = Control.MOUSE_FILTER_STOP
	var count := maxi(1, int(combat.get("count", 3)))
	var captain_coming := bool(combat.get("captain", false))
	# one brain per scuffle; the seed is the career + beat so the crew makes
	# the SAME decisions on every run (probe-checkable, never luck)
	imp_brain = ImpAI.new(IMP_BRAIN_TUNE, career_id.hash() + phase_index * 7919)
	imp_brain.begin_crew(count + (1 if captain_coming else 0))
	for index in range(count):
		# deterministic spread along the painted route — no RNG
		var t := fmod(0.14 + float(index) * 0.83 / float(count) + float(career_id.length()) * 0.031, 0.9)
		_spawn_stage_imp(t, false, index)
	captain_pending = captain_coming
	# Roshan takes her mark so the crew has room to come at her from both
	# sides: mid-route for the first scuffle, the stage door for the chase
	_glide_roshan_to(StagePaths.point_along(stage_points, 0.78 if captain_coming else 0.42), 0.9)


func _spawn_stage_imp(path_t: float, captain: bool, seed_index: int) -> void:
	var node := TextureRect.new()
	node.texture = captain_idle_texture if captain else imp_idle_texture
	node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	node.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	node.mouse_filter = Control.MOUSE_FILTER_IGNORE
	node.size = Vector2(150, 150) if captain else Vector2(118, 118)
	node.pivot_offset = node.size * Vector2(0.5, 1.0)   # pivot at the feet
	combat_layer.add_child(node)
	var feet := StagePaths.point_along(stage_points, path_t)
	var imp := {
		"node": node, "t": path_t, "dir": 1.0 if seed_index % 2 == 0 else -1.0,
		"speed": (46.0 if captain else 60.0) + float(seed_index % 3) * 14.0,
		"hp": 2 if captain else 1, "captain": captain,
		"popped": false, "seed": seed_index, "stroke": -1,
		"feet": feet, "carrying": false, "pose": "prowl",
	}
	if imp_brain != null:
		var mind: Dictionary = imp_brain.spawn_mind(seed_index, captain)
		mind["pos"] = feet
		imp["ai"] = mind
	# place it once up front: a tap that arrives before the first tick must
	# still find the imp where it looks like it is
	_apply_imp_pose(imp, node, feet, "prowl", 1.0)
	combat_imps.append(imp)


func _clear_stage_combat() -> void:
	for imp: Dictionary in combat_imps:
		var node := imp.get("node") as TextureRect
		if node != null and is_instance_valid(node):
			node.queue_free()
	combat_imps = []
	combat_marks = []
	imp_brain = null
	captain_pending = false
	if combat_layer != null:
		combat_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if combat_fx != null:
		combat_fx.queue_redraw()


func _combat_remaining() -> int:
	var left := 0
	for imp: Dictionary in combat_imps:
		if not bool(imp.get("popped", false)):
			left += 1
	return left


func _spawn_stage_captain() -> void:
	captain_pending = false
	_spawn_stage_imp(0.5, true, combat_imps.size())
	if m != null:
		m.show_msg("Imp Captain", "Hee hee! You'll have to bop ME twice!", "op_captain")


func _combat_input(event: InputEvent) -> void:
	if not active or combat_imps.is_empty():
		return
	if event is InputEventMouseButton and (event as InputEventMouseButton).device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventMouseMotion and (event as InputEventMouseMotion).device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed:
		_combat_strike((event as InputEventScreenTouch).position, (event as InputEventScreenTouch).position)
		swipe_stroke += 1
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT and (event as InputEventMouseButton).pressed:
		_combat_strike((event as InputEventMouseButton).position, (event as InputEventMouseButton).position)
		swipe_stroke += 1
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		_combat_strike(drag.position - drag.relative, drag.position)
	elif event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		var motion := event as InputEventMouseMotion
		_combat_strike(motion.position - motion.relative, motion.position)


func _combat_strike(from: Vector2, to: Vector2) -> void:
	# taps and swipe sweeps both bop: an imp is hit when the stroke segment
	# passes within its friendly reach
	var hit_any := false
	for imp: Dictionary in combat_imps:
		if bool(imp.get("popped", false)) or int(imp.get("stroke", -1)) == swipe_stroke:
			continue
		var node := imp.get("node") as TextureRect
		if node == null or not is_instance_valid(node):
			continue
		var center: Vector2 = imp.get("center", node.position + node.size * 0.5)
		var reach: float = float(imp.get("reach", node.size.x * 0.62))
		# the counter window: an imp caught in its recovery is a bigger,
		# friendlier target than one still on its feet
		if String(imp.get("pose", "")) == "recover":
			reach *= 1.45
		if _segment_distance(from, to, center) <= reach:
			imp["stroke"] = swipe_stroke
			hit_any = true
			_hit_stage_imp(imp, center)
	if imp_brain != null:
		imp_brain.on_player_swing(hit_any)
	if not hit_any and from.distance_to(to) < 6.0:
		# a stray tap fizzles kindly; repeats inside the cooldown pay nothing
		_bop_burst_at(to, true)
		var pay := 0.0
		if combat_miss_cool <= 0.0:
			combat_miss_cool = 0.45
			pay = 0.05
		_register_bop(pay, 0.2)


func _segment_distance(a: Vector2, b: Vector2, point: Vector2) -> float:
	var ab := b - a
	var len_sq := ab.length_squared()
	if len_sq <= 0.0001:
		return a.distance_to(point)
	var t := clampf((point - a).dot(ab) / len_sq, 0.0, 1.0)
	return (a + ab * t).distance_to(point)


func _hit_stage_imp(imp: Dictionary, at: Vector2) -> void:
	var mind: Dictionary = imp.get("ai", {})
	var node := imp.get("node") as TextureRect
	if String(imp.get("pose", "")) == "guard" and not mind.is_empty() and imp_brain != null:
		# the captain's guard: a bop bounces off, breaks the block early and
		# leaves him open. It costs no health, but nothing is ever wasted —
		# the guard drops NOW instead of running its own clock out.
		mind["state"] = "recover"
		mind["pose"] = "recover"
		mind["t"] = 0.0
		combat_marks.append({"kind": "bump", "pos": at, "t": 0.0, "life": 0.4})
		_bop_burst_at(at, true)
		_register_bop(0.2, 1.0)
		return
	imp["hp"] = int(imp.get("hp", 1)) - 1
	var popped := int(imp["hp"]) <= 0
	if imp_brain != null and not mind.is_empty():
		imp_brain.on_hit(mind, popped)
	if popped:
		imp["popped"] = true
		if node != null and is_instance_valid(node):
			var bopped := _imp_texture(imp, "bopped")
			combat_marks.append({"kind": "dizzy", "pos": at, "t": 0.0, "life": 0.62})
			if bopped != null:
				node.texture = bopped
			var spin := node.create_tween()
			spin.tween_property(node, "rotation", 0.6, 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			spin.parallel().tween_property(node, "modulate:a", 0.0, 0.62)
			spin.tween_callback(node.queue_free)
	# (a survivor needs no squash tween: the brain puts it straight into the
	# stagger pose, which the pose renderer plays every frame)
	_bop_burst_at(at, false)
	var bonus := 0.0
	if popped and bool(imp.get("carrying", false)):
		# it swiped a sparkle off her earlier — bopping it wins the sparkle
		# back, so being bumped only ever ADDS something to chase
		imp["carrying"] = false
		bonus = 0.5
		combat_marks.append({"kind": "taunt", "pos": at, "t": 0.0, "life": 0.6})
		_bop_burst_at(at, false)
	# one gesture, bonus folded in: a pop that finishes the beat must not
	# spill its sparkle bonus into the next phase
	_register_bop(1.0 + bonus, 1.0)


func _register_bop(amount: float, quality: float) -> void:
	# feeds the shared phase pipeline exactly like a gesture-surface event
	_on_gesture("bop", amount, quality)


func _finale_start() -> int:
	return clampi(int(FINALE_START.get(career_id, phases.size() - 1)), 0, maxi(0, phases.size() - 1))


func in_competition_finale() -> bool:
	return phase_index >= _finale_start()


func competition_progress() -> float:
	if phases.is_empty() or phase_index < _finale_start():
		return 0.0
	if phase_index >= phases.size():
		return 1.0
	var phase := phases[phase_index] as Dictionary
	var local := clampf(phase_progress / maxf(0.1, float(phase.get("goal", 1.0))), 0.0, 1.0)
	var finale_size := maxi(1, phases.size() - _finale_start())
	return (float(phase_index - _finale_start()) + local) / float(finale_size)


func _set_finale_visible(show_finale: bool) -> void:
	var cooperative := competition != null and competition.is_cooperative()
	if rival_actor != null:
		rival_actor.visible = show_finale or cooperative
	if player_bar != null:
		player_bar.visible = show_finale
	if rival_bar != null:
		rival_bar.visible = show_finale
	if score_label != null:
		score_label.visible = show_finale
	if timer_label != null:
		timer_label.visible = show_finale and career_id == "detective"
	if player_name_label != null:
		player_name_label.visible = show_finale
	if rival_name_label != null:
		rival_name_label.visible = show_finale
	if title_label != null:
		title_label.text = String(competition.spec.get("world", String(config.get("name", "CAREER CUP")))) if show_finale else "%s MINIGAMES" % String(config.get("career", "CAREER")).to_upper()

func _on_gesture(_kind: String, amount: float, quality: float) -> void:
	if not active or reveal_t > 0.0 or phase_index >= phases.size():
		return
	if phase_gap > 0.0:
		# any touch skips the between-phase sparkle sting
		phase_gap = 0.0
		return
	var phase := phases[phase_index] as Dictionary
	var mode := String(phase.get("mode", ""))
	if mode == "catch" and amount < 5.0:
		return
	idle_t = 0.0
	surface.note_input()
	var continuous := mode == "hold" or mode == "swipe" or mode == "circle"
	if quality < 0.5:
		competition.note_miss()
	elif not continuous or score_cool <= 0.0:
		# continuous verbs award applause at most twice a second — a held
		# finger must not out-score the whole finale
		competition.note_success(10)
		if continuous:
			score_cool = 0.5
	var gain := amount if continuous else maxf(0.04, amount)
	phase_progress += gain
	var goal := maxf(0.1, float(phase.get("goal", 1.0)))
	var progress := clampf(phase_progress / goal, 0.0, 1.0)
	phase_fill.value = progress * 100.0
	surface.set_fill(progress)
	_bounce_actor(player_actor, 14.0 if quality >= 0.5 else 7.0)
	if mode == "choice":
		if quality >= 0.5:
			# never rotate by a multiple of three — that froze the target
			choice_target = (choice_target + 1 + (phase_index % 2)) % 3
			surface.target_choice = choice_target
			surface.queue_redraw()
		else:
			# the answer re-flashes as mercy for a WRONG pick only — a
			# correct pick must not reveal the next answer for free
			surface.reflash_choice()
	elif mode == "bop":
		if quality >= 0.5 and captain_pending and _combat_remaining() <= 2 and phase_progress < goal:
			_spawn_stage_captain()
		# the captain can never be mashed past: his two bops are reserved.
		# (probe pumps arrive with amount 100 and skip the reserve)
		if amount < 5.0 and (captain_pending or _live_captain_hp() > 0):
			var reserve := 2.0 if captain_pending else float(_live_captain_hp())
			phase_progress = minf(phase_progress, goal - reserve)
	if phase_progress >= goal:
		phase_index += 1
		_show_phase()


func _live_captain_hp() -> int:
	for imp: Dictionary in combat_imps:
		if bool(imp.get("captain", false)) and not bool(imp.get("popped", false)):
			return maxi(0, int(imp.get("hp", 0)))
	return 0


func _bop_burst_at(origin: Vector2, fizzle: bool) -> void:
	if bop_puff_texture != null and not fizzle:
		# the accepted boxer bubble-puff impact card is the shared hit effect
		var puff := TextureRect.new()
		puff.texture = bop_puff_texture
		puff.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		puff.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		puff.mouse_filter = Control.MOUSE_FILTER_IGNORE
		puff.position = origin - Vector2(34, 34)
		puff.size = Vector2(68, 68)
		puff.pivot_offset = Vector2(34, 34)
		root.add_child(puff)
		var pop := puff.create_tween()
		pop.tween_property(puff, "scale", Vector2(2.2, 2.2), 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		pop.parallel().tween_property(puff, "modulate:a", 0.0, 0.34)
		pop.tween_callback(puff.queue_free)
	var bits := 4 if fizzle else 6
	for index in range(bits):
		var bit := ColorRect.new()
		bit.color = Color.from_hsv(0.72 + float(index) * 0.04, 0.4, 1.0)
		bit.position = origin
		bit.size = Vector2(7, 7) if fizzle else Vector2(9, 9)
		bit.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(bit)
		var jump := Vector2(cos(float(index) * TAU / float(bits)), sin(float(index) * TAU / float(bits))) * (40.0 if fizzle else 64.0)
		var tween := bit.create_tween()
		tween.tween_property(bit, "position", origin + jump, 0.34).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tween.parallel().tween_property(bit, "modulate:a", 0.0, 0.34)
		tween.tween_callback(bit.queue_free)


func _on_nursery_baby_caught(quality: float) -> void:
	if not active or phase_index >= phases.size():
		return
	var phase := phases[phase_index] as Dictionary
	if career_id != "nursery" or String(phase.get("mode", "")) != "catch":
		return
	idle_t = 0.0
	competition.note_success(18 if quality >= 0.5 else 8)
	phase_progress += 1.0
	var goal := maxf(1.0, float(phase.get("goal", 5.0)))
	var progress := clampf(phase_progress / goal, 0.0, 1.0)
	phase_fill.value = progress * 100.0
	surface.set_fill(progress)
	_bounce_actor(player_actor, 14.0)
	_bounce_actor(rival_actor, 9.0)
	if phase_progress >= goal:
		phase_index += 1
		_show_phase()


func _on_nursery_baby_missed() -> void:
	if not active or phase_index >= phases.size():
		return
	var phase := phases[phase_index] as Dictionary
	if career_id != "nursery" or String(phase.get("mode", "")) != "catch":
		return
	_bounce_actor(rival_actor, 14.0)
	competition.note_miss()
	if m != null:
		m._say("faron", "miss", 3.0)


func _bounce_actor(actor: Control, height: float) -> void:
	var home_y := actor.position.y
	var tween := actor.create_tween()
	tween.tween_property(actor, "position:y", home_y - height, 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_property(actor, "position:y", home_y, 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)


func progress() -> float:
	if phases.is_empty():
		return 0.0
	if phase_index >= phases.size():
		return 1.0
	var phase := phases[phase_index] as Dictionary
	var local := clampf(phase_progress / maxf(0.1, float(phase.get("goal", 1.0))), 0.0, 1.0)
	return (float(phase_index) + local) / float(phases.size())


func rival_step() -> void:
	if rival_actor == null:
		return
	_bounce_actor(rival_actor, 10.0 + float(competition.rival_step) * 1.8)


func begin_guided_retry() -> void:
	if career_id != "detective" or reveal_t > 0.0:
		return
	active = false
	reveal_t = 3.6
	phase_label.text = "★   WATCH THE IMP'S ANSWER"
	surface.configure("choice", Color(1.0, 0.84, 0.28), choice_target)
	if m != null:
		m.show_msg("Rival Imp", "The imp found it! Watch the glowing answer, then solve the same mystery with the sparkle memory!", "op_retry")


func update_competition() -> void:
	if competition == null:
		return
	player_bar.value = competition.player_progress * 100.0
	rival_bar.value = competition.rival_progress * 100.0
	score_label.text = "%03d  ★  %03d" % [competition.player_score, competition.rival_score]
	var left := competition.time_left()
	timer_label.text = "⏳ %02d" % int(ceilf(left)) if left >= 0.0 else ""
	var energy := competition.audience_energy()
	crowd_label.text = "●  ●  ●" if energy < 0.36 else ("●  ●  ●  ●  ●" if energy < 0.72 else "★  ★  ★  ★  ★")


func celebrate(result: Dictionary) -> void:
	active = false
	var tier := int(result.get("tier", 1))
	title_label.text = (
		"THE BABIES ARE COZY!" if competition.is_cooperative()
		else "%s — ROSHAN WINS!" % String(result.get("cheer", "BIG CHEERS"))
	)
	if prop_rect != null and prop_rect.texture != null:
		# the stolen goal prop comes home for the curtain call
		prop_rect.position = Vector2(540, 250)
		prop_rect.size = Vector2(200, 170)
		prop_rect.visible = true
		var prop_home := prop_rect.position.y
		var prop_tween := prop_rect.create_tween().set_loops(3)
		prop_tween.tween_property(prop_rect, "position:y", prop_home - 26.0, 0.22).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		prop_tween.tween_property(prop_rect, "position:y", prop_home, 0.26).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
	crowd_label.text = "★  " + "★  ".repeat(tier * 2 + 1)
	for index in range(audience.size()):
		var fan := audience[index]
		var home_y := fan.position.y
		var tween := fan.create_tween().set_loops(tier + 1)
		tween.tween_property(fan, "position:y", home_y - 18.0 - float(tier) * 6.0, 0.13).set_delay(float(index) * 0.025)
		tween.tween_property(fan, "position:y", home_y, 0.16)
	_bounce_actor(player_actor, 34.0)
	var bow_y := rival_actor.position.y
	var bow := rival_actor.create_tween()
	bow.tween_property(rival_actor, "rotation", 0.15, 0.25)
	bow.tween_property(rival_actor, "rotation", 0.0, 0.25)
	bow.tween_property(rival_actor, "position:y", bow_y + 12.0, 0.2)
	bow.tween_property(rival_actor, "position:y", bow_y, 0.2)
	for index in range(24):
		var bit := ColorRect.new()
		bit.color = Color.from_hsv(float(index) / 24.0, 0.58, 1.0)
		bit.position = Vector2(30.0 + float((index * 97) % 1220), -30.0 - float((index * 31) % 160))
		bit.size = Vector2(10, 22)
		bit.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(bit)
		confetti.append(bit)
		var fall := bit.create_tween()
		fall.tween_property(bit, "position:y", 760.0, 1.8 + float(index % 5) * 0.17)


func _tick_stage_combat(delta: float) -> void:
	# The crew thinks as a crew (scripts/imp_ai.gd) — who closes in, who
	# telegraphs, who hangs back — and each imp is then drawn back onto the
	# painted walkway in whatever pose it decided on.
	var hero := _hero_feet()
	if imp_brain != null:
		var minds: Array = []
		for imp: Dictionary in combat_imps:
			if bool(imp.get("popped", false)):
				continue
			var mind: Dictionary = imp.get("ai", {})
			if mind.is_empty():
				continue
			# the mind keeps its own ring coordinate; the renderer only ever
			# corrects its x (below), so the ring cannot collapse frame by
			# frame into the flattened screen depth
			mind["alive"] = true
			minds.append(mind)
		imp_brain.tick(delta, minds, hero)
		_handle_brain_events()
	for imp: Dictionary in combat_imps:
		if bool(imp.get("popped", false)):
			continue
		var node := imp.get("node") as TextureRect
		if node == null or not is_instance_valid(node):
			continue
		var mind: Dictionary = imp.get("ai", {})
		var feet: Vector2 = imp.get("feet", hero)
		var pose := "prowl"
		var face := 1.0
		if mind.is_empty():
			# no mind (never in normal play): idle in place rather than
			# freeze the fight — an imp must always stay tappable
			feet = _stage_feet_at_x(feet.x)
		else:
			# the brain circles her on a ring; the stage is a promenade, so
			# the ring's "sideways" becomes walkway travel and its "toward
			# camera" becomes standing a little in front of or behind her
			var want: Vector2 = mind.get("pos", feet)
			var base := _stage_feet_at_x(want.x)
			var depth_off := clampf(want.y - hero.y, -190.0, 190.0) * 0.42
			feet = Vector2(base.x, base.y + depth_off)
			mind["pos"] = Vector2(base.x, want.y)   # the walkway owns x
			pose = String(mind.get("pose", "prowl"))
			face = float(mind.get("face", 1.0))
			imp["state_t"] = float(mind.get("t", 0.0))
		imp["feet"] = feet
		imp["pose"] = pose
		_apply_imp_pose(imp, node, feet, pose, face)
	_tick_combat_marks(delta)


func _hero_feet() -> Vector2:
	if player_actor == null:
		return StagePaths.point_along(stage_points, 0.5)
	var s: Vector2 = player_actor.scale
	return player_actor.position + Vector2(
		player_actor.size.x * 0.5 * s.x, player_actor.size.y * s.y - 12.0)


func _stage_feet_at_x(x: float) -> Vector2:
	# snap a brain-space position back onto the painted route: imps walk the
	# walkway the world was painted with, they never float over the scenery
	if stage_points.size() < 2:
		return Vector2(clampf(x, 80.0, 1200.0), 470.0)
	var first: Vector2 = stage_points[0]
	var last: Vector2 = stage_points[stage_points.size() - 1]
	var lo: float = minf(first.x, last.x) + 40.0
	var hi: float = maxf(first.x, last.x) - 40.0
	var cx: float = clampf(x, minf(lo, hi), maxf(lo, hi))
	for index in range(stage_points.size() - 1):
		var a: Vector2 = stage_points[index]
		var b: Vector2 = stage_points[index + 1]
		if absf(b.x - a.x) < 0.001:
			continue
		if cx >= minf(a.x, b.x) and cx <= maxf(a.x, b.x):
			var f: float = clampf((cx - a.x) / (b.x - a.x), 0.0, 1.0)
			return Vector2(cx, lerpf(a.y, b.y, f))
	return Vector2(cx, first.y if cx <= first.x else last.y)


## Pose -> what the imp actually looks like this frame. State art is used
## when it exists (see CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md); until it
## lands every pose is still readable through squash, tilt, lift and tint.
func _apply_imp_pose(imp: Dictionary, node: TextureRect, feet: Vector2,
		pose: String, face: float) -> void:
	var depth := clampf(0.62 + (feet.y / 720.0) * 0.55, 0.62, 1.1)
	var seed := float(imp.get("seed", 0))
	var t := float(imp.get("state_t", 0.0))
	var lift := 0.0
	var squash := Vector2.ONE
	var tilt := 0.0
	var tint := Color.WHITE
	match pose:
		"windup":
			# the crouch: held, obvious, and never shorter than MIN_WINDUP
			var hold: float = imp_brain.windup_time() if imp_brain != null else 0.9
			var k := clampf(t / maxf(0.2, hold), 0.0, 1.0)
			squash = Vector2(1.0 + 0.18 * k, 1.0 - 0.2 * k)
			tilt = -0.14 * k * face
			tint = Color(1.0, 0.9, 0.78).lerp(Color(1.0, 0.6, 0.52), k)
		"charge":
			squash = Vector2(1.14, 0.92)
			tilt = 0.24 * face
			lift = 12.0
		"slash":
			squash = Vector2(1.08, 1.02)
			tilt = lerpf(-0.55, 0.55, clampf(t / 0.28, 0.0, 1.0)) * face
			lift = 8.0
		"recover":
			# wide open: the counter window reads as an exhausted slump
			squash = Vector2(1.08, 0.88)
			tilt = -0.18 * face
			tint = Color(0.84, 0.9, 1.0)
		"guard":
			squash = Vector2(0.9, 1.08)
			tint = Color(0.78, 0.93, 1.0)
		"taunt", "rally":
			lift = absf(sin(t * 9.0)) * 18.0
			tilt = sin(t * 12.0) * 0.13
		"stagger":
			tilt = sin(t * 26.0) * 0.3
			lift = 5.0
		"flee":
			lift = absf(sin(bop_time * 9.5 + seed)) * 15.0
			tilt = -0.2 * face
		_:
			lift = sin(bop_time * 5.2 + seed * 1.7) * 9.0
	var texture := _imp_texture(imp, pose)
	if texture != null:
		node.texture = texture
	node.pivot_offset = node.size * Vector2(0.5, 1.0)
	node.scale = Vector2(depth * squash.x, depth * squash.y)
	node.rotation = tilt
	node.flip_h = face < 0.0
	node.modulate = tint
	node.position = feet - Vector2(node.size.x * 0.5, node.size.y) - Vector2(0.0, lift - 8.0)
	imp["center"] = feet - Vector2(0.0, node.size.y * node.scale.y * 0.5 + lift - 8.0)
	imp["reach"] = node.size.x * 0.62 * maxf(depth, 0.7)


## Pose -> state sprite, ALWAYS inside the same character's own sheet: an
## imp in a chef's hat must never borrow the bare imp's body for one frame.
## The chain is "the pose's own art, then its nearest cousin, then idle" —
## every missing file just falls through (see the codex handoff).
const POSE_STATES := {
	"windup": ["windup", "hop_a"],
	"charge": ["charge", "hop_b"],
	"slash": ["slash", "hop_b"],
	"recover": ["recover"],
	"guard": ["guard"],
	"taunt": ["taunt", "bow"],
	"rally": ["taunt", "bow"],
	"flee": ["flee", "hop_b"],
	"stagger": ["stagger"],
	"bopped": ["bopped"],
}


func _imp_family(captain: bool) -> String:
	# the crew wears the career costume in competitive acts, and the base
	# mischief-imp sheets in the cooperative ones
	if competition != null and not competition.is_cooperative() \
			and rival_actor != null and rival_actor.texture != null:
		return "rival_%s" % career_id
	return "imp_captain" if captain else "imp_mischief"


func _imp_texture(imp: Dictionary, pose: String) -> Texture2D:
	var captain := bool(imp.get("captain", false))
	var family := _imp_family(captain)
	var states: Array = POSE_STATES.get(pose, [])
	for state: String in states:
		var art := _state_texture("%s_%s" % [family, state])
		if art != null:
			return art
	if pose == "bopped":
		return captain_bopped_texture if captain else imp_bopped_texture
	if pose == "taunt" or pose == "rally":
		var bow := captain_bow_texture if captain else imp_bow_texture
		if bow != null and family.begins_with("imp_"):
			return bow
	return captain_idle_texture if captain else imp_idle_texture


func _state_texture(slug: String) -> Texture2D:
	if imp_state_cache.has(slug):
		return imp_state_cache[slug] as Texture2D
	var texture := _load_if_exists("res://assets/opera/worlds/actors/%s.png" % slug)
	imp_state_cache[slug] = texture
	return texture


func _handle_brain_events() -> void:
	for ev: Dictionary in imp_brain.drain_events():
		var kind := String(ev.get("kind", ""))
		var at: Vector2 = ev.get("pos", Vector2(640, 460))
		match kind:
			"telegraph":
				combat_marks.append({"kind": "ring", "pos": at, "t": 0.0,
					"life": maxf(0.3, imp_brain.windup_time())})
				if not combat_warned and m != null:
					# the first wind-up of the act gets its own voice line —
					# a new thing to react to is never text-only
					combat_warned = true
					m.show_msg("Roshan", "Watch out! That imp is winding up — bop it before it swipes!", "hint")
			"charge":
				combat_marks.append({"kind": "dust", "pos": at, "t": 0.0, "life": 0.4})
			"contact":
				_imp_contact(int(ev.get("index", -1)), at)
			"whiff":
				combat_marks.append({"kind": "arc", "pos": at, "t": 0.0, "life": 0.3})
			"taunt":
				combat_marks.append({"kind": "taunt", "pos": at, "t": 0.0, "life": 0.7})
			"rally":
				if m != null:
					m.show_msg("Imp Captain", "Crew! Back to me! Hee hee!", "op_captain")
			"flee":
				combat_marks.append({"kind": "dust", "pos": at, "t": 0.0, "life": 0.35})


## A slash landed. NO fail state and NO lost progress (CLAUDE.md): the imp
## bounces off Roshan's bubble shield and runs off with one of her sparkles
## — which turns that imp into a bonus target instead of a punishment.
func _imp_contact(index: int, at: Vector2) -> void:
	for imp: Dictionary in combat_imps:
		if int(imp.get("seed", -1)) != index or bool(imp.get("popped", false)):
			continue
		imp["carrying"] = true
		break
	combat_marks.append({"kind": "bump", "pos": at, "t": 0.0, "life": 0.5})
	_bop_burst_at(at, true)
	if player_actor != null:
		var home := player_actor.position
		var away := signf(home.x + player_actor.size.x * 0.5 - at.x)
		var shove := player_actor.create_tween()
		shove.tween_property(player_actor, "position",
			home + Vector2(away * 26.0, -8.0), 0.09).set_trans(Tween.TRANS_QUAD)
		shove.tween_property(player_actor, "position", home, 0.24).set_trans(Tween.TRANS_BOUNCE)


func _tick_combat_marks(delta: float) -> void:
	for index in range(combat_marks.size() - 1, -1, -1):
		var mark: Dictionary = combat_marks[index]
		mark["t"] = float(mark.get("t", 0.0)) + delta
		if float(mark["t"]) >= float(mark.get("life", 0.3)):
			combat_marks.remove_at(index)
	if combat_fx != null:
		combat_fx.queue_redraw()


func _draw_combat_fx() -> void:
	# the crew's intentions, drawn where a four-year-old is already looking:
	# a gold ring + "!" while an imp winds up, a swipe arc when it misses,
	# a stolen sparkle orbiting whoever bumped her
	for mark: Dictionary in combat_marks:
		var at: Vector2 = mark.get("pos", Vector2.ZERO)
		var life: float = maxf(0.05, float(mark.get("life", 0.3)))
		var k: float = clampf(float(mark.get("t", 0.0)) / life, 0.0, 1.0)
		match String(mark.get("kind", "")):
			"ring":
				var pulse := 1.0 - k
				var head := at - Vector2(0.0, 132.0)
				if fx_telegraph_ring_texture != null and fx_telegraph_bang_texture != null:
					var ring_size := Vector2.ONE * (92.0 + k * 68.0)
					combat_fx.draw_texture_rect(fx_telegraph_ring_texture,
						Rect2(at - ring_size * 0.5, ring_size), false,
						Color(1.0, 1.0, 1.0, 0.25 + pulse * 0.6))
					var bang_size := Vector2(32.0, 64.0)
					combat_fx.draw_texture_rect(fx_telegraph_bang_texture,
						Rect2(head - bang_size * 0.5, bang_size), false,
						Color(1.0, 1.0, 1.0, 0.55 + pulse * 0.45))
				else:
					combat_fx.draw_arc(at, 46.0 + k * 34.0, 0.0, TAU, 28,
						Color(1.0, 0.78, 0.28, 0.25 + pulse * 0.6), 6.0)
					combat_fx.draw_rect(Rect2(head - Vector2(6.0, 30.0), Vector2(12.0, 34.0)),
						Color(1.0, 0.85, 0.3, 0.55 + pulse * 0.45))
					combat_fx.draw_circle(head + Vector2(0.0, 14.0), 7.0,
						Color(1.0, 0.85, 0.3, 0.55 + pulse * 0.45))
			"arc":
				if fx_slash_arc_texture != null:
					var arc_size := Vector2(210.0, 105.0)
					combat_fx.draw_texture_rect(fx_slash_arc_texture,
						Rect2(at - Vector2(arc_size.x * 0.5, arc_size.y * 0.5 + 60.0), arc_size),
						false, Color(1.0, 1.0, 1.0, 0.55 * (1.0 - k)))
				else:
					combat_fx.draw_arc(at - Vector2(0.0, 60.0), 92.0, -0.9, 0.9, 20,
						Color(1.0, 1.0, 1.0, 0.55 * (1.0 - k)), 9.0)
			"dust":
				if fx_dust_puff_texture != null:
					var dust_size := Vector2.ONE * (96.0 + k * 44.0)
					combat_fx.draw_texture_rect(fx_dust_puff_texture,
						Rect2(at - dust_size * 0.5, dust_size), false,
						Color(1.0, 1.0, 1.0, 0.5 * (1.0 - k)))
				else:
					combat_fx.draw_circle(at, 18.0 + k * 26.0,
						Color(0.92, 0.88, 1.0, 0.32 * (1.0 - k)))
			"bump":
				combat_fx.draw_arc(at, 40.0 + k * 60.0, 0.0, TAU, 26,
					Color(0.62, 0.93, 1.0, 0.7 * (1.0 - k)), 7.0)
			"taunt":
				combat_fx.draw_circle(at - Vector2(0.0, 150.0 + k * 20.0), 9.0,
					Color(1.0, 0.72, 0.86, 0.75 * (1.0 - k)))
			"dizzy":
				if fx_dizzy_stars_texture != null:
					combat_fx.draw_set_transform(at - Vector2(0.0, 90.0), k * TAU * 1.5,
						Vector2.ONE * 0.46)
					combat_fx.draw_texture(fx_dizzy_stars_texture, Vector2(-128.0, -128.0),
						Color(1.0, 1.0, 1.0, 1.0 - k))
					combat_fx.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	for imp: Dictionary in combat_imps:
		if bool(imp.get("popped", false)) or not bool(imp.get("carrying", false)):
			continue
		var centre: Vector2 = imp.get("center", Vector2.ZERO)
		var spin: float = elapsed * 3.4 + float(imp.get("seed", 0))
		var star: Vector2 = centre + Vector2(cos(spin), sin(spin) * 0.5) * 54.0
		if fx_stolen_sparkle_texture != null:
			var sparkle_size := Vector2.ONE * 32.0
			combat_fx.draw_texture_rect(fx_stolen_sparkle_texture,
				Rect2(star - sparkle_size * 0.5, sparkle_size), false)
		else:
			combat_fx.draw_circle(star, 11.0, Color(1.0, 0.94, 0.55, 0.95))
			combat_fx.draw_circle(star, 5.0, Color.WHITE)


func _start_lens_phase(phase: Dictionary) -> void:
	lens_layer.visible = true
	lens_layer.mouse_filter = Control.MOUSE_FILTER_STOP
	lens_pos = Vector2(640, 420)
	lens_demo = true
	lens_dwell = 0.0
	lens_target = -1
	var spots := StagePaths.clue_spots(career_id)
	var goal := mini(int(ceilf(float(phase.get("goal", 5.0)))), spots.size())
	# rotate which painted details hide sparkles so the two lens phases differ
	var offset := phase_index * 3
	lens_clues = PackedVector2Array()
	lens_found = []
	for index in range(goal):
		lens_clues.append(spots[(index + offset) % spots.size()])
		lens_found.append(false)


func _lens_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and (event as InputEventMouseButton).device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventMouseMotion and (event as InputEventMouseMotion).device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed:
		lens_pos = (event as InputEventScreenTouch).position
		lens_demo = false
	elif event is InputEventScreenDrag:
		lens_pos = (event as InputEventScreenDrag).position
		lens_demo = false
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT and (event as InputEventMouseButton).pressed:
		lens_pos = (event as InputEventMouseButton).position
		lens_demo = false
	elif event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		lens_pos = (event as InputEventMouseMotion).position
		lens_demo = false
	lens_layer.queue_redraw()


func _tick_lens(delta: float) -> void:
	if lens_layer == null or not lens_layer.visible:
		return
	if lens_demo:
		# the ghost lens drifts along the stage until the child grabs it
		lens_pos = Vector2(
			640.0 + sin(elapsed * 0.9) * 420.0,
			410.0 + sin(elapsed * 1.7) * 130.0
		)
	var found_index := -1
	for index in range(lens_clues.size()):
		if not lens_found[index] and lens_pos.distance_to(lens_clues[index]) <= 96.0:
			found_index = index
			break
	if found_index != lens_target:
		lens_target = found_index
		lens_dwell = 0.0
	elif found_index >= 0 and not lens_demo:
		lens_dwell += delta
		if lens_dwell >= 0.45:
			lens_found[found_index] = true
			lens_target = -1
			lens_dwell = 0.0
			_bop_burst_at(lens_clues[found_index], false)
			_on_gesture("lens", 1.0, 1.0)
	lens_layer.queue_redraw()


func _draw_lens_layer() -> void:
	# sparkles hide in the painting and only glow under the magic lens
	for index in range(lens_clues.size()):
		var spot := lens_clues[index]
		if lens_found[index]:
			lens_layer.draw_circle(spot, 10.0, Color(1.0, 0.9, 0.5, 0.9))
			continue
		var d := lens_pos.distance_to(spot)
		if d <= 118.0:
			var reveal := clampf(1.0 - d / 118.0, 0.0, 1.0)
			var twinkle := 0.6 + (sin(elapsed * 6.0 + float(index)) + 1.0) * 0.2
			lens_layer.draw_circle(spot, 13.0 * reveal, Color(1.0, 0.95, 0.55, reveal * twinkle))
			lens_layer.draw_arc(spot, 19.0 * reveal, 0.0, TAU, 20, Color(1.0, 0.85, 0.3, reveal * 0.8), 3.0)
	# The raster prop is authored at 45 degrees with translucent aqua glass.
	if magnifier_texture != null:
		lens_layer.draw_texture_rect(
			magnifier_texture,
			Rect2(lens_pos - Vector2(128.0, 128.0), Vector2(256.0, 256.0)),
			false
		)
	else:
		lens_layer.draw_circle(lens_pos, 92.0, Color(0.75, 0.92, 1.0, 0.14))
		lens_layer.draw_arc(lens_pos, 92.0, 0.0, TAU, 48, Color("#c88b3c"), 9.0)
		lens_layer.draw_arc(lens_pos, 80.0, 0.0, TAU, 48, Color(1.0, 1.0, 1.0, 0.35), 3.0)
		var handle_dir := Vector2(0.72, 0.72)
		lens_layer.draw_line(lens_pos + handle_dir * 92.0, lens_pos + handle_dir * 158.0, Color("#8a5f3c"), 16.0)
	if lens_target >= 0:
		lens_layer.draw_arc(lens_pos, 100.0, -PI * 0.5, -PI * 0.5 + TAU * clampf(lens_dwell / 0.45, 0.0, 1.0), 40, Color(1.0, 0.9, 0.4), 6.0)


func _process(delta: float) -> void:
	elapsed += delta
	if score_cool > 0.0:
		score_cool = maxf(0.0, score_cool - delta)
	if combat_miss_cool > 0.0:
		combat_miss_cool = maxf(0.0, combat_miss_cool - delta)
	if phase_gap > 0.0:
		phase_gap = maxf(0.0, phase_gap - delta)
	if active and reveal_t <= 0.0 and phase_index < phases.size():
		# quiet children get the prompt again plus a fresh finger demo
		idle_t += delta
		if idle_t >= 9.0:
			idle_t = 0.0
			surface.restart_demo()
			if m != null:
				m.show_msg("Roshan", String((phases[phase_index] as Dictionary).get("voice", "Follow the golden sparkle!")), "hint")
	timing_phase = fmod(timing_phase + delta * minf(0.70, 0.55 + 0.02 * float(phase_index)), 2.0)
	var marker := timing_phase if timing_phase <= 1.0 else 2.0 - timing_phase
	surface.set_timing_position(marker)
	if active and phase_index < phases.size():
		var phase := phases[phase_index] as Dictionary
		var mode := String(phase.get("mode", ""))
		if mode == "hold" and surface.held and phase_gap <= 0.0:
			_on_gesture("hold", delta, 1.0)
		elif mode == "bop":
			bop_time += delta
			_tick_stage_combat(delta)
		elif mode == "lens":
			_tick_lens(delta)
	for marker_node in station_nodes:
		marker_node.queue_redraw()
	if reveal_t > 0.0:
		reveal_t -= delta
		# the reveal shows the ACTUAL answer, steady — recognition, not a light show
		surface.target_choice = choice_target
		surface.choice_flash = 0.6
		surface.queue_redraw()
		if reveal_t <= 0.0:
			guided = true
			phase_index = _finale_start()
			phase_progress = 0.0
			active = true
			competition.guided_retry()
			_show_phase()
			# the remembered clues give a visible head start on the rematch
			phase_progress = 2.0
			phase_fill.value = clampf(2.0 / maxf(0.1, float((phases[phase_index] as Dictionary).get("goal", 1.0))), 0.0, 1.0) * 100.0


func close() -> void:
	active = false
	queue_free()
