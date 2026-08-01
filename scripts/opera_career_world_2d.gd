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
		{"name": "PEEK", "icon": "?", "mode": "hold", "goal": 5.0, "vo": "op_detective_peek", "voice": "Hold the magnifier over the glowing clue!"},
		{"name": "TRAIL", "icon": "→", "mode": "swipe", "goal": 7.5, "vo": "op_detective_trail", "voice": "Swipe along the footprint trail!"},
		{"name": "CLUES", "icon": "●", "mode": "tap", "goal": 8.0, "vo": "op_detective_clues", "voice": "Tap every glowing clue you find!"},
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
var bop_puff_texture: Texture2D = null

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
	player_actor.position = Vector2(35, 150)
	player_actor.size = Vector2(420, 460)
	root.add_child(player_actor)
	rival_actor = _actor("res://assets/opera/worlds/actors/rival_%s.png" % career_id)
	rival_actor.position = Vector2(825, 170)
	rival_actor.size = Vector2(410, 420)
	root.add_child(rival_actor)
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
	action_panel.color = Color(0.025, 0.025, 0.11, 0.62)
	action_panel.position = Vector2(430, 160)
	action_panel.size = Vector2(420, 430)
	action_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(action_panel)
	phase_label = _label("", 32, Color(1.0, 0.92, 0.62))
	phase_label.position = Vector2(10, 8)
	phase_label.size = Vector2(400, 62)
	action_panel.add_child(phase_label)
	surface = GestureSurface.new()
	surface.position = Vector2(24, 78)
	surface.size = Vector2(372, 266)
	surface.gesture.connect(_on_gesture)
	# The scuffle crews wear the career's special imp costume (the accepted
	# costume-sheet slices). Basic placeholder imps are only the fallback.
	if rival_actor != null and rival_actor.texture != null:
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
	phase_fill = ProgressBar.new()
	phase_fill.position = Vector2(24, 362)
	phase_fill.size = Vector2(372, 40)
	phase_fill.show_percentage = false
	phase_fill.mouse_filter = Control.MOUSE_FILTER_IGNORE
	action_panel.add_child(phase_fill)

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
	var is_bop := String(phase.get("mode", "tap")) == "bop"
	var accent := Color(competition.spec.get("accent", Color(1.0, 0.62, 0.8)))
	choice_target = (phase_index + int(competition.rival_step)) % 3
	_apply_panel_layout(is_bop)
	surface.configure(String(phase.get("mode", "tap")), accent, choice_target)
	match String(phase.get("dir", "")):
		"down":
			surface.swipe_dir = Vector2.DOWN
		"up":
			surface.swipe_dir = Vector2.UP
	if is_bop:
		bop_time = 0.0
		surface.set_bop_targets(_build_bop_targets(phase.get("combat", {}) as Dictionary))
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
		m.show_msg("Roshan", String(phase.get("voice", "Follow the golden sparkle!")), String(phase.get("vo", "hint")))


func _apply_panel_layout(wide: bool) -> void:
	if action_panel == null:
		return
	if wide:
		action_panel.position = Vector2(140, 150)
		action_panel.size = Vector2(1000, 446)
		phase_label.size = Vector2(980, 54)
		surface.position = Vector2(24, 66)
		surface.size = Vector2(952, 334)
		phase_fill.position = Vector2(24, 408)
		phase_fill.size = Vector2(952, 28)
	else:
		action_panel.position = Vector2(430, 160)
		action_panel.size = Vector2(420, 430)
		phase_label.size = Vector2(400, 62)
		surface.position = Vector2(24, 78)
		surface.size = Vector2(372, 266)
		phase_fill.position = Vector2(24, 362)
		phase_fill.size = Vector2(372, 40)


func _build_bop_targets(combat: Dictionary) -> Array:
	var targets: Array = []
	var count := maxi(1, int(combat.get("count", 3)))
	var w := surface.size.x
	var columns := maxi(1, ceili(float(count) / 2.0))
	var spacing := (w - 220.0) / maxf(1.0, float(columns - 1))
	for index in range(count):
		# deterministic two-row lattice — guaranteed spacing even at full
		# bob sway, and no RNG so probes and replays are stable
		var home := Vector2(
			110.0 + float(index / 2) * spacing + float(index % 2) * 40.0
				+ fmod(float(career_id.length()) * 29.0, 36.0),
			96.0 + float(index % 2) * 130.0
		)
		targets.append({
			"home": home, "pos": home, "r": 46.0,
			"hp": 1, "captain": false, "popped": false, "seed": index,
		})
	# the captain waits in the wings and jumps in once the crew is cleared
	captain_pending = bool(combat.get("captain", false))
	return targets


func _spawn_bop_captain() -> void:
	captain_pending = false
	var w := surface.size.x
	var h := surface.size.y
	var home := Vector2(w * 0.5, h * 0.45)
	surface.bop_targets.append({
		"home": home, "pos": home, "r": 62.0,
		"hp": 2, "captain": true, "popped": false, "seed": surface.bop_targets.size(),
	})
	surface.queue_redraw()
	if m != null:
		m.show_msg("Imp Captain", "Hee hee! You'll have to bop ME twice!", "op_captain")


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
	if rival_actor != null:
		rival_actor.visible = show_finale
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
	idle_t = 0.0
	surface.note_input()
	if quality < 0.5:
		competition.note_miss()
	else:
		competition.note_success(10)
	var gain := maxf(0.04, amount)
	phase_progress += gain
	var goal := maxf(0.1, float(phase.get("goal", 1.0)))
	phase_fill.value = clampf(phase_progress / goal, 0.0, 1.0) * 100.0
	_bounce_actor(player_actor, 14.0 if quality >= 0.5 else 7.0)
	if mode == "choice":
		if quality >= 0.5:
			# never rotate by a multiple of three — that froze the target
			choice_target = (choice_target + 1 + (phase_index % 2)) % 3
			surface.target_choice = choice_target
		surface.reflash_choice()
	elif mode == "bop":
		if quality >= 0.5:
			_bop_burst(surface.last_bop_pos)
			if captain_pending and surface.bop_remaining() <= 2 and phase_progress < goal:
				_spawn_bop_captain()
		# the captain can never be mashed past: his two bops are reserved.
		# (probe pumps arrive with amount 100 and skip the reserve)
		if amount < 5.0 and (captain_pending or _live_captain_hp() > 0):
			var reserve := 2.0 if captain_pending else float(_live_captain_hp())
			phase_progress = minf(phase_progress, goal - reserve)
	if phase_progress >= goal:
		phase_index += 1
		_show_phase()


func _live_captain_hp() -> int:
	for target: Dictionary in surface.bop_targets:
		if bool(target.get("captain", false)) and not bool(target.get("popped", false)):
			return maxi(0, int(target.get("hp", 0)))
	return 0


func _bop_burst(at: Vector2) -> void:
	if action_panel == null:
		return
	var origin := action_panel.position + surface.position + at
	if bop_puff_texture != null:
		# the accepted boxer bubble-puff impact card is the shared hit effect
		var puff := TextureRect.new()
		puff.texture = bop_puff_texture
		puff.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		puff.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		puff.mouse_filter = Control.MOUSE_FILTER_IGNORE
		puff.position = origin - Vector2(30, 30)
		puff.size = Vector2(60, 60)
		puff.pivot_offset = Vector2(30, 30)
		root.add_child(puff)
		var pop := puff.create_tween()
		pop.tween_property(puff, "scale", Vector2(2.2, 2.2), 0.3).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		pop.parallel().tween_property(puff, "modulate:a", 0.0, 0.34)
		pop.tween_callback(puff.queue_free)
	for index in range(6):
		var bit := ColorRect.new()
		bit.color = Color.from_hsv(0.72 + float(index) * 0.04, 0.4, 1.0)
		bit.position = origin
		bit.size = Vector2(9, 9)
		bit.mouse_filter = Control.MOUSE_FILTER_IGNORE
		root.add_child(bit)
		var jump := Vector2(cos(float(index) * TAU / 6.0), sin(float(index) * TAU / 6.0)) * 64.0
		var tween := bit.create_tween()
		tween.tween_property(bit, "position", origin + jump, 0.34).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tween.parallel().tween_property(bit, "modulate:a", 0.0, 0.34)
		tween.tween_callback(bit.queue_free)


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
	title_label.text = "%s — ROSHAN WINS!" % String(result.get("cheer", "BIG CHEERS"))
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


func _process(delta: float) -> void:
	elapsed += delta
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
	timing_phase = fmod(timing_phase + delta * minf(0.92, 0.72 + 0.03 * float(phase_index)), 2.0)
	var marker := timing_phase if timing_phase <= 1.0 else 2.0 - timing_phase
	surface.set_timing_position(marker)
	if active and phase_index < phases.size():
		var phase := phases[phase_index] as Dictionary
		var mode := String(phase.get("mode", ""))
		if mode == "hold" and surface.held and phase_gap <= 0.0:
			_on_gesture("hold", delta, 1.0)
		elif mode == "bop":
			bop_time += delta
			for target: Dictionary in surface.bop_targets:
				var seed := float(target.get("seed", 0))
				var sway := 20.0 if bool(target.get("captain", false)) else 28.0
				target["pos"] = (target.get("home", Vector2.ZERO) as Vector2) + Vector2(
					sin(bop_time * 1.3 + seed * 2.1) * sway,
					sin(bop_time * 2.2 + seed * 1.7) * sway * 0.65
				)
			surface.queue_redraw()
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
