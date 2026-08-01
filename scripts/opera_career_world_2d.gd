class_name OperaCareerWorld2D
extends CanvasLayer
## The runtime 2D/2.5D Pearl Opera career world.
##
## Each career supplies artwork and a phase list, while this class owns the
## common living-world language: full-bleed environment painting, Mermaid
## Roshan and a dressed rival or care partner, one-finger job gestures,
## parallel/team progress, audience energy and a graded curtain call.

const GestureSurface := preload("res://scripts/opera_gesture_surface.gd")
const WorldBackdrop := preload("res://scripts/opera_world_backdrop_2d.gd")
const NurseryCatch := preload("res://scripts/opera_nursery_catch.gd")

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
	"nursery": "nursery",
	"popstar": "popstar",
}

const PHASES := {
	"chef": [
		{"name": "SIFT", "icon": "↔", "mode": "swipe", "goal": 2.4, "voice": "Scrub the sieve back and forth!"},
		{"name": "POUR", "icon": "●", "mode": "hold", "goal": 2.4, "voice": "Hold to pour the milk!"},
		{"name": "STIR", "icon": "↻", "mode": "circle", "goal": 1.8, "voice": "Draw big circles to stir!"},
		{"name": "BAKE", "icon": "★", "mode": "timing", "goal": 3.0, "voice": "Tap when the oven marker is green!"},
		{"name": "PIPE", "icon": "〰", "mode": "swipe", "goal": 2.6, "voice": "Swipe to pipe the frosting!"},
		{"name": "TOP", "icon": "●", "mode": "tap", "goal": 5.0, "voice": "Tap on the bright toppings!"},
	],
	"detective": [
		{"name": "LENS PRACTICE", "icon": "?", "mode": "choice", "goal": 3.0, "voice": "Practice moving the magnifier to three golden sparkles!"},
		{"name": "CLUES", "icon": "?", "mode": "choice", "goal": 5.0, "voice": "Find the glowing clue before the detective imp!"},
		{"name": "TRAIL", "icon": "→", "mode": "swipe", "goal": 2.4, "voice": "Swipe along the footprint trail!"},
		{"name": "BOARD", "icon": "◆", "mode": "choice", "goal": 4.0, "voice": "Match each clue to the glowing place!"},
		{"name": "NAME", "icon": "★", "mode": "choice", "goal": 1.0, "voice": "Tap the glowing mystery answer!"},
	],
	"ballerina": [
		{"name": "WATCH", "icon": "♪", "mode": "hold", "goal": 1.5, "voice": "Hold still and watch the glowing dance!"},
		{"name": "STEPS", "icon": "◆", "mode": "choice", "goal": 6.0, "voice": "Tap the glowing dance step!"},
		{"name": "RIBBON", "icon": "〰", "mode": "swipe", "goal": 2.6, "voice": "Trace the ribbon across the stage!"},
		{"name": "TWIRL", "icon": "↻", "mode": "circle", "goal": 2.2, "voice": "Draw circles for the final twirl!"},
	],
	"candymaker": [
		{"name": "SYRUP", "icon": "●", "mode": "hold", "goal": 2.0, "voice": "Hold the sparkling syrup bottle!"},
		{"name": "SORT", "icon": "◆", "mode": "choice", "goal": 7.0, "voice": "Tap the glowing candy chute!"},
		{"name": "WRAP", "icon": "↻", "mode": "circle", "goal": 1.8, "voice": "Twist the wrappers in circles!"},
		{"name": "PARADE", "icon": "★", "mode": "timing", "goal": 5.0, "voice": "Tap when the parade cart is in the green!"},
	],
	"doctor": [
		{"name": "WASH", "icon": "●", "mode": "hold", "goal": 2.0, "voice": "Hold to wash Stuffie Surgeon Roshan's hands!"},
		{"name": "FIND", "icon": "?", "mode": "choice", "goal": 3.0, "voice": "Find the plushy with the glowing ouch!"},
		{"name": "X-RAY", "icon": "◆", "mode": "choice", "goal": 3.0, "voice": "Tap the glowing cracked bone!"},
		{"name": "CAST", "icon": "↻", "mode": "circle", "goal": 2.6, "voice": "Draw circles to wrap the soft cast!"},
		{"name": "BANDAGE", "icon": "〰", "mode": "swipe", "goal": 2.0, "voice": "Swipe the stretchy bandage around!"},
	],
	"farmer": [
		{"name": "PLANT", "icon": "↓", "mode": "swipe", "goal": 2.6, "voice": "Swipe the seeds into the garden holes!"},
		{"name": "FEED", "icon": "★", "mode": "timing", "goal": 5.0, "voice": "Tap when the veggie reaches a piggy!"},
		{"name": "MUD HOPS", "icon": "↑", "mode": "swipe", "goal": 2.4, "voice": "Swipe up to hop over the mud!"},
		{"name": "BARN", "icon": "↔", "mode": "swipe", "goal": 3.0, "voice": "Sweep back and forth to guide the herd home!"},
	],
	"boxer": [
		{"name": "WARM UP", "icon": "●", "mode": "tap", "goal": 5.0, "voice": "Tap the bag to warm up both gloves!"},
		{"name": "ROUND 1", "icon": "★", "mode": "timing", "goal": 4.0, "voice": "Round one! Tap in the green to punch the padded gloves!"},
		{"name": "DUCK", "icon": "↓", "mode": "swipe", "goal": 1.5, "voice": "Swipe down to duck the imp's friendly counter!"},
		{"name": "ROUND 2", "icon": "★", "mode": "timing", "goal": 5.0, "voice": "Round two! Watch the bell and punch on the beat!"},
		{"name": "DUCK", "icon": "↓", "mode": "swipe", "goal": 1.5, "voice": "Swipe down, then pop back into guard!"},
		{"name": "ROUND 3", "icon": "★", "mode": "timing", "goal": 6.0, "voice": "Final round! Fill the crowd meter!"},
		{"name": "BELT", "icon": "★", "mode": "tap", "goal": 1.0, "voice": "Tap the championship belt for the winner!"},
	],
	"magician": [
		{"name": "VANISH", "icon": "●", "mode": "hold", "goal": 1.6, "voice": "Hold the wand to vanish the bunny-fish!"},
		{"name": "TRACK", "icon": "?", "mode": "choice", "goal": 6.0, "voice": "Follow the glowing hat through the shuffle!"},
		{"name": "ROPE", "icon": "〰", "mode": "swipe", "goal": 2.2, "voice": "Swipe the magic rope into one long ribbon!"},
		{"name": "CABINET", "icon": "★", "mode": "timing", "goal": 4.0, "voice": "Tap on the star flashes to open the cabinet!"},
		{"name": "STAR PORTAL", "icon": "✦", "mode": "hold", "goal": 2.8, "voice": "Hold the wand high and open the giant star portal!"},
	],
	"painter": [
		{"name": "SKETCH", "icon": "〰", "mode": "swipe", "goal": 2.6, "voice": "Trace the sunrise sketch!"},
		{"name": "FILL", "icon": "●", "mode": "hold", "goal": 2.1, "voice": "Hold to fill the glowing shape!"},
		{"name": "PAINT", "icon": "↔", "mode": "swipe", "goal": 3.2, "voice": "Race the painter imp across both canvases!"},
		{"name": "SPLATTER", "icon": "●", "mode": "tap", "goal": 5.0, "voice": "Tap five happy splatters!"},
		{"name": "GALLERY", "icon": "★", "mode": "tap", "goal": 1.0, "voice": "Tap Roshan's picture to hang it in the gallery!"},
	],
	"astronaut": [
		{"name": "PIPES", "icon": "◆", "mode": "choice", "goal": 6.0, "voice": "Tap the glowing pipe to route the bubbles!"},
		{"name": "PATCH", "icon": "●", "mode": "hold", "goal": 1.8, "voice": "Hold the patch over the sparkle leak!"},
		{"name": "VALVE", "icon": "↻", "mode": "circle", "goal": 2.4, "voice": "Draw circles to turn the launch valve!"},
		{"name": "LAUNCH", "icon": "↑", "mode": "hold", "goal": 2.6, "voice": "Hold for the countdown and launch first!"},
	],
	"racer": [
		{"name": "STEER", "icon": "↔", "mode": "swipe", "goal": 3.0, "voice": "Swipe to steer through the coral gates!"},
		{"name": "ZOOM", "icon": "★", "mode": "timing", "goal": 5.0, "voice": "Tap TURBO when the marker hits green!"},
		{"name": "LAP TWO", "icon": "↔", "mode": "swipe", "goal": 3.4, "voice": "Second lap! Swipe through the faster turns!"},
		{"name": "FINISH", "icon": "★", "mode": "timing", "goal": 3.0, "voice": "Hit the final zoom strips and cross the line!"},
	],
	"nursery": [
		{"name": "WASH HANDS", "icon": "●", "mode": "hold", "goal": 2.0, "voice": "Nursery Nurse Roshan! Hold the bubbly basin to wash your hands first!"},
		{"name": "CATCH BABIES", "icon": "↓", "mode": "catch", "goal": 5.0, "speaker": "Faron", "voice": "Slide the soft cradle under five falling babies! Pillows keep every miss safe."},
		{"name": "FEED", "icon": "♡", "mode": "hold", "goal": 4.2, "speaker": "Faron", "voice": "Hold the warm bottle while Roshan and Faron feed every baby!"},
		{"name": "BURP", "icon": "○", "mode": "timing", "goal": 3.0, "voice": "Tap in the green for three gentle burp-pats!"},
		{"name": "BEDTIME", "icon": "☾", "mode": "swipe", "goal": 3.0, "speaker": "Faron", "voice": "Swipe the blankets down and tuck every sleepy baby into bed!"},
	],
	"popstar": [
		{"name": "SOUND CHECK", "icon": "●", "mode": "hold", "goal": 1.4, "voice": "Hold the microphone for sound check!"},
		{"name": "DANCE", "icon": "◆", "mode": "choice", "goal": 7.0, "voice": "Tap the glowing dance arrow!"},
		{"name": "RHYTHM", "icon": "♪", "mode": "timing", "goal": 6.0, "voice": "Tap each rainbow note in the green!"},
		{"name": "ENCORE", "icon": "↻", "mode": "circle", "goal": 2.0, "voice": "Draw a big encore spin for the crowd!"},
	],
}

const FINALE_START := {
	"chef": 4,
	"detective": 1,
	"ballerina": 1,
	"candymaker": 3,
	"doctor": 3,
	"farmer": 2,
	"boxer": 1,
	"magician": 3,
	"painter": 2,
	"astronaut": 2,
	"racer": 2,
	"nursery": 1,
	"popstar": 2,
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

var root: Control
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
var nursery_catch: OperaNurseryCatch
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
	_full_rect(root)
	add_child(root)

	var backdrop := WorldBackdrop.new() as OperaWorldBackdrop2D
	backdrop.name = "CareerWorldBackdrop"
	_full_rect(backdrop)
	root.add_child(backdrop)
	backdrop.setup(career_id)

	var shade := ColorRect.new()
	shade.color = Color(0.025, 0.025, 0.11, 0.19)
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
	rival_name_label = _label("DRESSED IMP", 17, Color(0.82, 0.76, 1.0))
	rival_name_label.position = Vector2(784, 87)
	rival_name_label.size = Vector2(430, 28)
	top.add_child(rival_name_label)

	player_actor = _actor("res://assets/opera/worlds/actors/roshan_%s.png" % career_id)
	player_actor.position = Vector2(35, 150)
	player_actor.size = Vector2(420, 460)
	root.add_child(player_actor)
	var partner_path := "res://assets/opera/worlds/actors/rival_%s.png" % career_id
	if career_id == "nursery":
		partner_path = "res://assets/opera/worlds/actors/faron_nursery.png"
	rival_actor = _actor(partner_path)
	rival_actor.position = Vector2(825, 170)
	rival_actor.size = Vector2(410, 420)
	root.add_child(rival_actor)
	if career_id == "nursery":
		player_name_label.text = "NURSE ROSHAN"
		rival_name_label.text = "NURSE FARON"
	_set_finale_visible(false)

	var action_panel := ColorRect.new()
	action_panel.color = Color(0.025, 0.025, 0.11, 0.82)
	action_panel.position = Vector2(430, 160)
	action_panel.size = Vector2(420, 430)
	root.add_child(action_panel)
	phase_label = _label("", 32, Color(1.0, 0.92, 0.62))
	phase_label.position = Vector2(10, 8)
	phase_label.size = Vector2(400, 62)
	action_panel.add_child(phase_label)
	surface = GestureSurface.new()
	surface.position = Vector2(24, 78)
	surface.size = Vector2(372, 266)
	surface.gesture.connect(_on_gesture)
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
		if nursery_catch != null:
			nursery_catch.stop()
		active = false
		if win_callback.is_valid():
			win_callback.call()
		return
	if phase_index == _finale_start():
		competition.begin()
		_set_finale_visible(true)
	elif phase_index < _finale_start():
		_set_finale_visible(false)
	phase_progress = 0.0
	var phase := phases[phase_index] as Dictionary
	var accent := Color(competition.spec.get("accent", Color(1.0, 0.62, 0.8)))
	choice_target = (phase_index + int(competition.rival_step)) % 3
	var mode := String(phase.get("mode", "tap"))
	var is_nursery_catch := career_id == "nursery" and mode == "catch"
	surface.visible = not is_nursery_catch
	if nursery_catch != null:
		nursery_catch.visible = is_nursery_catch
		if is_nursery_catch:
			nursery_catch.start(int(ceilf(float(phase.get("goal", 5.0)))))
		else:
			nursery_catch.stop()
	if not is_nursery_catch:
		var visual_context := ""
		if career_id == "nursery":
			visual_context = String({
				"WASH HANDS": "nursery_wash",
				"FEED": "nursery_feed",
				"BURP": "nursery_burp",
				"BEDTIME": "nursery_bedtime",
			}.get(String(phase.get("name", "")), ""))
		surface.configure(mode, accent, choice_target, visual_context)
	phase_label.text = "%s   %s" % [String(phase.get("icon", "★")), String(phase.get("name", "PLAY"))]
	phase_fill.value = 0.0
	if m != null:
		m.show_msg(String(phase.get("speaker", "Roshan")), String(phase.get("voice", "Follow the golden sparkle!")), "hint")


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
	var phase := phases[phase_index] as Dictionary
	if String(phase.get("mode", "")) == "catch":
		return
	if quality < 0.5:
		competition.note_miss()
	else:
		competition.note_success(10)
	var gain := maxf(0.04, amount)
	phase_progress += gain
	var goal := maxf(0.1, float(phase.get("goal", 1.0)))
	phase_fill.value = clampf(phase_progress / goal, 0.0, 1.0) * 100.0
	_bounce_actor(player_actor, 14.0 if quality >= 0.5 else 7.0)
	if String(phase.get("mode", "")) == "choice" and quality >= 0.5:
		choice_target = (choice_target + 1 + phase_index) % 3
		surface.target_choice = choice_target
		surface.queue_redraw()
	if phase_progress >= goal:
		if career_id == "nursery":
			_bounce_actor(rival_actor, 9.0)
		phase_index += 1
		_show_phase()


func _on_nursery_baby_caught(quality: float) -> void:
	if not active or phase_index >= phases.size():
		return
	var phase := phases[phase_index] as Dictionary
	if career_id != "nursery" or String(phase.get("mode", "")) != "catch":
		return
	competition.note_success(18 if quality >= 0.5 else 8)
	phase_progress += 1.0
	var goal := maxf(1.0, float(phase.get("goal", 5.0)))
	phase_fill.value = clampf(phase_progress / goal, 0.0, 1.0) * 100.0
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
		m.show_msg("Rival Imp", "The imp found it! Watch the glowing answer, then solve the same mystery with the sparkle memory!", "talk")


func update_competition() -> void:
	if competition == null:
		return
	player_bar.value = competition.player_progress * 100.0
	rival_bar.value = competition.rival_progress * 100.0
	if competition.is_cooperative():
		score_label.text = "TEAM  ♡  %03d" % (competition.player_score + competition.rival_score)
	else:
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
	timing_phase = fmod(timing_phase + delta * 0.72, 2.0)
	var marker := timing_phase if timing_phase <= 1.0 else 2.0 - timing_phase
	surface.set_timing_position(marker)
	if active and phase_index < phases.size():
		var phase := phases[phase_index] as Dictionary
		if String(phase.get("mode", "")) == "hold" and surface.held:
			_on_gesture("hold", delta, 1.0)
	if reveal_t > 0.0:
		reveal_t -= delta
		surface.target_choice = int(floor(elapsed * 2.0)) % 3
		surface.queue_redraw()
		if reveal_t <= 0.0:
			guided = true
			phase_index = _finale_start()
			phase_progress = 0.0
			active = true
			competition.guided_retry()
			_show_phase()


func close() -> void:
	active = false
	if nursery_catch != null:
		nursery_catch.stop()
	queue_free()
