class_name ChapterTwoLawnFinale2D
extends Control

## Playable Canvas alpha. Static story blocking and gameplay cutouts are
## explicitly not accepted cinematic frames. The Grok/full-frame lane stays
## separate. Gameplay state belongs to ReefMain and its save owner.
const SIZE := Vector2(1280.0, 720.0)
const ORIGIN := Vector2(805.0, 535.0)
const PROJECTION := Vector2(11.0, 3.5)
const KEY := "chapter2_lawn_runtime"
const ROCKET_RECT := Rect2(480.0, 422.0, 140.0, 145.0)
# Heights use visible silhouettes, not transparent texture padding.
# Prince's approved standing height is exactly 80% of the King's.
const KING_VISIBLE_HEIGHT := 288.0
const KING_SCALE := KING_VISIBLE_HEIGHT / 797.0
const KING_SIZE := Vector2(747.0, 817.0) * KING_SCALE
const KING_RECT := Rect2(Vector2(960.0, 560.0 - 807.0 * KING_SCALE), KING_SIZE)
const BOSS_POINT := (Vector2(KING_RECT.position.x + KING_SIZE.x * 0.5, 560.0) - ORIGIN) / PROJECTION
const PRINCE_SIZE := Vector2(144.0, 301.0) * (KING_VISIBLE_HEIGHT * 0.8 / 301.0)
const PRINCE_RECT := Rect2(Vector2(848.0, 560.0 - PRINCE_SIZE.y), PRINCE_SIZE)
const ROSHAN_SIZE := Vector2(256.0, 256.0)
const ROSHAN_FOOT := Vector2(128.0, 229.0)
const CANDLE_RECT := Rect2(385.0, 272.0, 64.0, 90.0)
const CANDLE_WICK := Vector2(417.0, 293.0)
const CONTINUE_RECT := Rect2(1050.0, 592.0, 180.0, 106.0)
const BACK_RECT := Rect2(1150.0, 18.0, 112.0, 112.0)
const ROSHAN_HOME := Vector2(625.0, 331.0)
# The upper central brass button, above the blue porthole: source (256,168).
const IGNITION_POINT := ROCKET_RECT.position + Vector2(70.0, 48.4375)
const IGNITION_REACH_POSITION := IGNITION_POINT - Vector2(16.0, 77.0)
const ROSHAN_BASE := "res://assets/characters/roshan_25d/roshan_base.png"
const ROSHAN_REACH := "res://assets/characters/roshan_25d/roshan_gesture_b.png"
const ROSHAN_SWIM := "res://assets/characters/roshan_25d/roshan_swim_front.png"
const GUEST_FILES := ["wacky_chuck", "two_friends", "pearl_friend",
	"mama_baby", "kareem", "huluu", "flower_friend", "daddy"]
const VOICE_BEATS := ["ready", "lit", "arrive", "challenge", "protect", "safe", "theft", "leave", "hope"]
const DIALOGUE := [
	"Roshan: We made all of this together! Let's light our rainbow!",
	"Roshan: Look! Our rainbow candle is shining!",
	"Prince: You made that?  Roshan: All of us did. You can join us.",
	"King: That light belongs at a KING'S party. Show me how strong you are!",
	"Roshan: He's so big. But I can keep my friends safe.",
	"Roshan: You're safe!  Prince: She did it, Father!",
	"King: Enough games. I am taking the light!  Prince: That isn't fair!",
	"King: Come, son.  Prince: I'm sorry, Roshan.",
	"Roshan: You're all still here. We'll find our light together.",
]

var m: ReefMain
var battle: ChapterTwoEmberEncounter
var art: Dictionary = {}
var caption: Label
var foreground: Control
var pointer: TextureRect
var on_exit: Callable
var ignition_pose := AtlasTexture.new()

func setup(main: ReefMain, exit_callback: Callable) -> void:
	m = main
	battle = ChapterTwoEmberEncounter.new(m)
	on_exit = exit_callback
	name = "ChapterTwoSkyLagoonLawn"
	size = SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	clip_contents = true
	m.g[KEY] = {"elapsed": 0.0, "beat_elapsed": 0.0, "mode": "story",
		"mode_elapsed": 0.0, "player": Vector2(0.0, 12.0),
		"destination": Vector2(0.0, 12.0), "pointer_id": -1,
		"last_touch": -10.0, "feedback": "", "feedback_time": 0.0,
		"context_losses": {}, "ignition_source": -1}
	set_meta("true_2d_lawn", true)
	set_meta("cinematic_delivery_accepted", false)
	set_meta("character_identity_review", "king_v4_owner_confirmed_prince_recovered")
	set_meta("guest_portraits_unchanged", true)
	set_meta("stage_purpose", "happy_birthday_sky_lagoon")
	set_meta("playground_equipment_present", false)
	_build_art()
	_build_controls()
	if m.chapter2_lawn_beat == 4:
		_start_battle()
	_refresh_story()
	_say_beat()
	_fit()

func _state() -> Dictionary:
	return m.g[KEY] as Dictionary

func set_input_context(reason: StringName, lost: bool) -> void:
	if m == null or not m.g.has(KEY):
		return
	var losses: Dictionary = _state()["context_losses"]
	if lost:
		losses[reason] = true
		_state()["pointer_id"] = -1
		_state()["destination"] = _state()["player"]
		_cancel_ignition()
	else:
		losses.erase(reason)

func _input_context_lost() -> bool:
	return not (_state()["context_losses"] as Dictionary).is_empty()

func uses_global_navigation() -> bool:
	return m != null and is_instance_valid(m.global_navigation_button)

func _fit() -> void:
	var viewport_size := get_viewport_rect().size
	var factor := minf(viewport_size.x / SIZE.x, viewport_size.y / SIZE.y)
	scale = Vector2.ONE * factor
	position = (viewport_size - SIZE * factor) * 0.5

func _picture(id: String, path: String, rect: Rect2) -> TextureRect:
	var picture := TextureRect.new()
	picture.name = id
	picture.texture = load(path) as Texture2D
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.position = rect.position
	picture.size = rect.size
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(picture)
	art[id] = picture
	return picture

func _build_art() -> void:
	# The middle playable screen retains its full native 2048x2048 coverage.
	# All four existing tiles receive one identical whole-canvas transform.
	for row: int in range(2):
		for column: int in range(2):
			var tile := _picture("LawnTile%d%d" % [row, column],
				"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png"
				% [row, column + 2], Rect2(column * 640.0, row * 640.0 - 340.0, 640.0, 640.0))
			tile.stretch_mode = TextureRect.STRETCH_SCALE
			tile.show_behind_parent = true
	_picture("Banner", ChapterTwoPartyTable2D.BANNER_TEXTURE,
		Rect2(50.0, 118.0, 90.0, 145.0))
	for stamp_index: int in range(5):
		var stamp := TextureRect.new()
		stamp.name = "BirthdayStarStamp%d" % stamp_index
		stamp.texture = load("res://assets/flats/castle/logo_studio_v2/castle_banner_motif_star.png") as Texture2D
		stamp.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		stamp.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		stamp.size = Vector2(20.0, 20.0)
		stamp.position = Vector2(16.0 + float(stamp_index % 3) * 19.0,
			58.0 + float(stamp_index / 3) * 28.0)
		stamp.mouse_filter = Control.MOUSE_FILTER_IGNORE
		(art["Banner"] as Control).add_child(stamp)
	_picture("Table", ChapterTwoPartyTable2D.TABLE_TEXTURE,
		Rect2(240.0, 440.0, 360.0, 165.0))
	for index: int in range(GUEST_FILES.size()):
		var guest_positions := [Vector2(40, 350), Vector2(170, 325),
			Vector2(40, 505), Vector2(165, 500), Vector2(290, 550),
			Vector2(405, 560), Vector2(515, 545), Vector2(520, 280)]
		var guest_position: Vector2 = guest_positions[index]
		var guest := _picture("Guest_%s" % GUEST_FILES[index],
			"res://assets/characters/friends/%s.%s" % [GUEST_FILES[index],
				"webp" if GUEST_FILES[index] == "daddy" else "png"],
			Rect2(guest_position, Vector2(118.0, 140.0)))
		guest.set_meta("protected_source_unchanged", true)
		guest.z_index = 2 if index >= 4 else 0
		if GUEST_FILES[index] == "two_friends":
			_add_hat(guest, Vector2(26.0, 37.0), index, 0.65)
			_add_hat(guest, Vector2(56.0, 30.0), index + 1, 0.8)
		elif GUEST_FILES[index] == "pearl_friend":
			_add_hat(guest, Vector2(89.0, 27.0), index, 0.8)
		elif GUEST_FILES[index] == "mama_baby":
			_add_hat(guest, Vector2(44.0, 26.0), index)
			_add_hat(guest, Vector2(81.0, 63.0), index + 1, 0.55)
		else:
			_add_hat(guest, Vector2(59.0, -8.0 if index == 7 else 10.0), index)
	# Carry forward the actual Ballerina and Pop Star participants and objects,
	# using the same source art as OperaCareerWorld2D's Chapter 2 scenes.
	_picture("StuffieCat", "res://assets/book/doll_cat.png", Rect2(85.0, 620.0, 65.0, 68.0))
	_picture("StuffieBunny", "res://assets/book/doll_bunny.png", Rect2(158.0, 620.0, 60.0, 63.0))
	_picture("MusicBox", OperaBalletSurface.MUSIC_BOX_PATH, Rect2(205.0, 460.0, 70.0, 68.0))
	_picture("PartyMicrophone", "res://assets/opera/worlds/props/goal_popstar.png",
		Rect2(630.0, 440.0, 64.0, 75.0))
	var rumi := _picture("Rumi", "res://assets/characters/rumi/rumi_eight_pose_runtime.png",
		Rect2(590.0, 320.0, 100.0, 140.0))
	var rumi_frame := AtlasTexture.new()
	rumi_frame.atlas = rumi.texture
	rumi_frame.region = Rect2(0.0, 0.0, rumi.texture.get_width() / 4.0,
		rumi.texture.get_height() / 2.0)
	rumi.texture = rumi_frame
	_add_hat(rumi, Vector2(50.0, 20.0), 2, 0.65)
	_picture("Cake", ChapterTwoGiantCake2D.FINAL_CAKE_TEXTURE,
		Rect2(310.0, 320.0, 210.0, 235.0))
	_picture("Candle", ChapterTwoRainbowCandle2D.UNLIT_TEXTURE,
		CANDLE_RECT)
	_picture("Rocket", "res://assets/opera/worlds/props/goal_astronaut.png", ROCKET_RECT)
	_picture("King", "res://assets/chapter2/ember_alpha/king_v4_cutout.png", KING_RECT)
	var prince := _picture("Prince", "res://assets/chapter2/ember_alpha/prince_idle.png",
		PRINCE_RECT)
	var prince_frame := AtlasTexture.new()
	prince_frame.atlas = prince.texture
	prince_frame.region = Rect2(56.0, 75.0, 144.0, 301.0)
	prince.texture = prince_frame
	_picture("CarriedCandle", ChapterTwoRainbowCandle2D.LIT_TEXTURE,
		Rect2(953.0, 300.0, 64.0, 90.0))
	_picture("Roshan", ROSHAN_BASE, Rect2(ROSHAN_HOME, ROSHAN_SIZE))

func _add_hat(parent: Control, point: Vector2, colour_index: int,
		factor: float = 1.0) -> void:
	# A removable Canvas costume accessory, never an edit to a friend portrait.
	var hat := Polygon2D.new()
	hat.name = "PartyHat"
	hat.position = point
	hat.scale = Vector2.ONE * factor
	hat.polygon = PackedVector2Array([Vector2(-22, 8), Vector2(0, -38), Vector2(22, 8)])
	hat.color = [Color("f4b7d6"), Color("f7d77a"), Color("9bded4"),
		Color("c5a6f1")][colour_index % 4]
	parent.add_child(hat)
	var edge := Line2D.new()
	edge.points = PackedVector2Array([Vector2(-22, 8), Vector2(0, -38),
		Vector2(22, 8), Vector2(-22, 8)])
	edge.width = 3.0
	edge.default_color = Color("49375f")
	hat.add_child(edge)
	var stripe := Line2D.new()
	stripe.points = PackedVector2Array([Vector2(-12, -12), Vector2(12, -12)])
	stripe.width = 5.0
	stripe.default_color = Color("fff2c8")
	hat.add_child(stripe)

func _build_controls() -> void:
	var birthday_title := Label.new()
	birthday_title.text = "Happy Birthday, Roshan!"
	birthday_title.position = Vector2(175.0, 115.0)
	birthday_title.size = Vector2(750.0, 70.0)
	birthday_title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI._apply_typography(birthday_title, StorybookUI.ROLE_BODY, 42)
	add_child(birthday_title)
	caption = Label.new()
	caption.position = Vector2(30.0, 20.0)
	caption.size = Vector2(1080.0, 85.0)
	caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI._apply_typography(caption, StorybookUI.ROLE_BODY, 27)
	add_child(caption)
	foreground = Control.new()
	foreground.name = "BattleOpeningOverlay"
	foreground.size = SIZE
	foreground.z_index = 10
	foreground.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(foreground)
	foreground.draw.connect(_draw_foreground)
	pointer = _picture("GuideHand", "res://assets/castle/training/ghost_hand.png",
		Rect2(520.0, 500.0, 88.0, 88.0))
	pointer.z_index = 11

func _candle_texture(lit: bool) -> AtlasTexture:
	var texture := AtlasTexture.new()
	texture.atlas = load(ChapterTwoRainbowCandle2D.LIT_TEXTURE
		if lit else ChapterTwoRainbowCandle2D.UNLIT_TEXTURE) as Texture2D
	# One shared source rectangle keeps wax size and holder position invariant
	# when the flame appears. Only transparent side padding is excluded.
	texture.region = Rect2(344.0, 16.0, 332.0, 984.0)
	return texture

func _refresh_story() -> void:
	_refresh_earned_artifacts()
	var beat := m.chapter2_lawn_beat
	caption.text = DIALOGUE[clampi(beat, 0, DIALOGUE.size() - 1)]
	(art["Candle"] as TextureRect).texture = _candle_texture(m.chapter2_candle_lit)
	(art["CarriedCandle"] as TextureRect).texture = _candle_texture(true)
	(art["King"] as TextureRect).visible = beat >= 2 and beat <= 7
	(art["Prince"] as TextureRect).visible = beat >= 2 and beat <= 7
	(art["CarriedCandle"] as TextureRect).visible = beat in [6, 7]
	_state()["beat_elapsed"] = 0.0
	queue_redraw()
	if foreground != null:
		foreground.queue_redraw()

func _refresh_earned_artifacts() -> void:
	var represented: Array[String] = []
	for entry: Dictionary in ChapterTwoPartyPlan.LIVE_CAREERS:
		var act := int(entry["act_index"])
		var earned := (m.chapter2_party_piece_mask & (1 << act)) != 0
		for id: String in entry["lawn_nodes"]:
			var prop := art.get(id) as Control
			if prop == null:
				continue
			prop.visible = earned and (id != "Candle" or not m.chapter2_candle_taken)
			prop.set_meta("earned_in_castle_jobs", true)
			prop.set_meta("source_job_piece", String(entry["piece"]))
		if earned:
			represented.append(String(entry["piece"]))
	set_meta("earned_party_pieces", represented)
	# The first three jobs are physically combined in ONE cake with FIVE berries.
	# Do not resurrect raw berry baskets, corn, candy bags, clue chests or crowns.
	set_meta("cake_contains_job_outputs", ["strawberries", "birthday_cake", "candied_strawberries"])

func _say_beat() -> void:
	m._say("roshan", "chapter2_lawn_" + VOICE_BEATS[clampi(m.chapter2_lawn_beat, 0, 8)], 0.0)
	set_meta("scene_specific_voice_acceptance", false)
	set_meta("alpha_voice", "existing_synthetic_roshan_owner_listening_pending")

func _begin_ignition() -> void:
	if String(_state()["mode"]) != "story" or m.chapter2_lawn_beat != 0:
		return
	_mode("ignition_walk")
	_state()["ignition_source"] = int(_state()["pointer_id"])
	(art["Roshan"] as Control).z_index = 3
	set_meta("ignition_hand_contact", false)

func _cancel_ignition() -> void:
	if not String(_state()["mode"]).begins_with("ignition_"):
		return
	_mode("story")
	_state()["ignition_source"] = -1
	(art["Roshan"] as TextureRect).texture = load(ROSHAN_BASE) as Texture2D
	(art["Roshan"] as Control).z_index = 0
	set_meta("ignition_hand_contact", false)

func _ignition_pose(path: String, frame: int) -> void:
	ignition_pose.atlas = load(path) as Texture2D
	ignition_pose.region = Rect2(float(frame % 4) * 256.0, float(frame / 4) * 256.0, 256.0, 256.0)
	(art["Roshan"] as TextureRect).texture = ignition_pose

func _tick_ignition(delta: float) -> void:
	var actor := art["Roshan"] as TextureRect
	var state := _state()
	var step := minf(delta, 1.0 / 30.0)
	# One bounded gameplay step cannot teleport her or skip the authored reach.
	state["mode_elapsed"] = float(state["mode_elapsed"]) - delta + step
	var elapsed := float(state["mode_elapsed"])
	match String(state["mode"]):
		"ignition_walk", "ignition_return":
			var returning := String(state["mode"]) == "ignition_return"
			var target := ROSHAN_HOME if returning else IGNITION_REACH_POSITION
			actor.position = actor.position.move_toward(target, step * 140.0)
			_ignition_pose(ROSHAN_SWIM, int(elapsed * 12.0) % 16)
			if actor.position.distance_to(target) < 0.1:
				if returning:
					actor.texture = load(ROSHAN_BASE) as Texture2D
					actor.z_index = 0
					state["ignition_source"] = -1
					_mode("story")
				else:
					_mode("ignition_reach")
					_ignition_pose(ROSHAN_REACH, 12)
		"ignition_reach":
			_ignition_pose(ROSHAN_REACH, 12 + mini(int(elapsed / 0.25), 3))
			set_meta("ignition_hand_contact", elapsed >= 0.75)
			if elapsed >= 1.6:
				_advance_story()
				set_meta("ignition_hand_contact", false)
				_mode("ignition_return")

func _advance_story() -> void:
	if float(_state()["beat_elapsed"]) < (2.4 if m.chapter2_lawn_beat == 1 else 0.5):
		return
	var director := m._chapter_two_ref()
	match m.chapter2_lawn_beat:
		0:
			if not director.start_main_hall_party("sky_lagoon_lawn"):
				return
			m.chapter2_lawn_beat = 1
		1:
			director.record_ember_scout()
			m.chapter2_lawn_beat = 2
		2:
			m.chapter2_lawn_beat = 3
		3:
			m.chapter2_lawn_beat = 4
			_start_battle()
		5:
			if not director.trigger_ember_king_crash("sky_lagoon_lawn"):
				return
			m.chapter2_lawn_beat = 6
		6:
			m.chapter2_lawn_beat = 7
		7:
			m.chapter2_lawn_beat = 8
			m.chapter2_story_complete = true
		8:
			on_exit.call()
			return
		_:
			return
	_refresh_story()
	_say_beat()
	m._write_save()

func _start_battle() -> void:
	var current := battle.begin()
	if current.finished():
		m.chapter2_lawn_beat = 5
		_state()["mode"] = "story"
		return
	_begin_tell()

func _begin_tell() -> void:
	battle.engine().begin_attack(_state()["player"] as Vector2, BOSS_POINT, 26.0)
	_mode("tell")
	_state()["feedback"] = "Prince: Over here! Move out of the orange shape."
	m._say("roshan", "chapter2_lawn_dodge", 0.0)

func _mode(value: String) -> void:
	_state()["mode"] = value
	_state()["mode_elapsed"] = 0.0

func tick(delta: float) -> void:
	if m == null or m.game != "chapter2_lawn" or not m.g.has(KEY):
		return
	if _input_context_lost():
		return
	_fit()
	var state := _state()
	state["elapsed"] = float(state["elapsed"]) + delta
	state["beat_elapsed"] = float(state["beat_elapsed"]) + delta
	state["mode_elapsed"] = float(state["mode_elapsed"]) + delta
	if String(state["mode"]).begins_with("ignition_"):
		_tick_ignition(delta)
	if m.chapter2_lawn_beat == 4:
		_tick_battle(delta)
	pointer.visible = not String(state["mode"]).begins_with("ignition_")
	var hint := IGNITION_POINT if m.chapter2_lawn_beat == 0 else CONTINUE_RECT.get_center()
	if m.chapter2_lawn_beat == 4:
		var current := battle.engine()
		if current.state == BossEncounter2D.State.OPENING:
			hint = KING_RECT.get_center()
		else:
			hint = _screen(current.patterns.readout().get("safe_point", Vector2.ZERO) as Vector2)
	pointer.position = hint + Vector2(18.0, 8.0 + sin(float(state["elapsed"]) * 3.0) * 9.0)
	queue_redraw()
	if foreground != null:
		foreground.queue_redraw()

func _tick_battle(delta: float) -> void:
	var state := _state()
	var current := battle.engine()
	state["player"] = (state["player"] as Vector2).move_toward(
		state["destination"] as Vector2, delta * 24.0)
	var roshan := art["Roshan"] as TextureRect
	roshan.z_index = 3
	roshan.position = _screen(state["player"] as Vector2) - ROSHAN_FOOT
	caption.text = String(state["feedback"])
	var king := art["King"] as TextureRect
	king.position = KING_RECT.position
	if current.state == BossEncounter2D.State.TELL:
		king.position.y -= 6.0 * sin(minf(float(state["mode_elapsed"]), 1.0) * PI * 0.5)
	elif current.state == BossEncounter2D.State.STRIKE:
		king.position.y += 4.0

	match String(state["mode"]):
		"tell":
			if current.tick_tell(delta):
				current.begin_strike()
				_mode("strike")
		"strike":
			if float(state["mode_elapsed"]) < 0.35:
				return
			var impact := current.resolve_impact(state["player"] as Vector2, BOSS_POINT, 26.0)
			if impact == BossEncounter2D.Impact.NEXT_TELL:
				_mode("tell")
			elif impact == BossEncounter2D.Impact.COUNTER_READY:
				current.open_counter()
				_mode("opening")
				state["feedback"] = "Roshan: Now! Tap the King's glowing opening!"
				m._say("roshan", "chapter2_lawn_counter", 0.0)
			else:
				_mode("recover")
				state["feedback"] = "Prince: You're safe. Let's try again."
				m._say("roshan", "chapter2_lawn_retry", 0.0)
				battle.checkpoint_assistance()
				m._write_save()
		"opening":
			if current.tick_counter(delta, true):
				_mode("recover")
				state["feedback"] = "Roshan: Another chance!"
				battle.checkpoint_assistance()
				m._write_save()
		"recover":
			if float(state["mode_elapsed"]) >= 1.2:
				_begin_tell()
		"round":
			if float(state["mode_elapsed"]) >= 1.5:
				if battle.friends_are_safe():
					m.chapter2_lawn_beat = 5
					_mode("story")
					_refresh_story()
					_say_beat()
					m._write_save()
				else:
					_begin_tell()

func _screen(point: Vector2) -> Vector2:
	return ORIGIN + point * PROJECTION

func _destination(point: Vector2) -> void:
	if _input_context_lost():
		return
	var logical := (point - ORIGIN) / PROJECTION
	_state()["destination"] = logical.limit_length(20.5)

func _gui_input(event: InputEvent) -> void:
	if m == null or m.game != "chapter2_lawn":
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		_state()["last_touch"] = float(_state()["elapsed"])
		if touch.canceled:
			if touch.index == int(_state()["ignition_source"]):
				_cancel_ignition()
			_point_event(touch.position, false, touch.index)
			accept_event()
			return
		_point_event(touch.position, touch.pressed, touch.index)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if int(_state()["pointer_id"]) == drag.index and m.chapter2_lawn_beat == 4:
			_destination(drag.position)
		accept_event()
	elif event is InputEventMouseButton:
		var mouse := event as InputEventMouseButton
		if mouse.button_index == MOUSE_BUTTON_LEFT and float(_state()["elapsed"]) \
				- float(_state()["last_touch"]) > 1.0:
			_point_event(mouse.position, mouse.pressed, 1000)
		accept_event()
	elif event is InputEventMouseMotion:
		if int(_state()["pointer_id"]) == 1000 and m.chapter2_lawn_beat == 4:
			_destination((event as InputEventMouseMotion).position)
		accept_event()

func _point_event(point: Vector2, pressed: bool, id: int) -> void:
	if _input_context_lost():
		return
	if not pressed:
		if int(_state()["pointer_id"]) == id:
			_state()["pointer_id"] = -1
		return
	if int(_state()["pointer_id"]) != -1 or float(_state()["elapsed"]) < 0.4:
		return
	_state()["pointer_id"] = id
	if not uses_global_navigation() and BACK_RECT.has_point(point):
		on_exit.call()
		return
	if String(_state()["mode"]).begins_with("ignition_"):
		return
	if m.chapter2_lawn_beat != 4:
		if (ROCKET_RECT if m.chapter2_lawn_beat == 0 else CONTINUE_RECT).has_point(point):
			if m.chapter2_lawn_beat == 0:
				_begin_ignition()
			else:
				_advance_story()
		return
	var current := battle.engine()
	if current.state == BossEncounter2D.State.OPENING and KING_RECT.has_point(point):
		if battle.accept_counter(true, true, true):
			_mode("round")
			_state()["feedback"] = "Roshan: Our rainbow is getting stronger!"
			m._say("roshan", "chapter2_lawn_round", 0.0)
			m._write_save()
	else:
		_destination(point)

func _draw() -> void:
	if m == null or not m.g.has(KEY):
		return
	# The live game owns one shared Back. Only isolated view probes need a fallback.
	if not uses_global_navigation():
		draw_style_box(StorybookUI.panel_style(Color("503964"), Color("f8e9d4"), 30, 3), BACK_RECT)
		var origin := BACK_RECT.position
		draw_polyline(PackedVector2Array([origin + Vector2(71, 24),
			origin + Vector2(36, 49), origin + Vector2(71, 74)]), Color("503964"), 8.0, true)
	if m.chapter2_lawn_beat != 4 and m.chapter2_lawn_beat != 0:
		draw_style_box(StorybookUI.panel_style(Color("503964"), Color("f8e9d4"), 36, 3), CONTINUE_RECT)
		draw_polyline(PackedVector2Array([Vector2(1120, 620), Vector2(1162, 645), Vector2(1120, 670)]),
			Color("503964"), 9.0, true)
	for round_index: int in range(m.chapter2_protection_rounds):
		draw_arc(Vector2(343, 530), 260.0 + round_index * 10.0,
			PI, TAU, 64, [Color("f7d87c"), Color("a7e4da"), Color("d5b0f0")][round_index], 7.0, true)
	if m.chapter2_lawn_beat != 4:
		return
	var current := battle.engine()
	if current == null:
		return
	if current.state in [BossEncounter2D.State.TELL, BossEncounter2D.State.STRIKE]:
		var geometry := current.patterns.readout()
		var points := PackedVector2Array()
		var center: Vector2 = geometry.get("center", Vector2.ZERO)
		if String(geometry.get("kind", "")) == "landing_circle":
			for index: int in range(49):
				var angle := float(index) / 48.0 * TAU
				points.append(_screen(center + Vector2(cos(angle), sin(angle))
					* float(geometry.get("radius", 5.2))))
		else:
			var direction: Vector2 = geometry.get("direction", Vector2.RIGHT)
			var across := Vector2(-direction.y, direction.x)
			for corner: Vector2 in [Vector2(-1, -1), Vector2(1, -1), Vector2(1, 1), Vector2(-1, 1)]:
				points.append(_screen(center + direction * corner.x * float(geometry.get("half_length", 23.0))
					+ across * corner.y * float(geometry.get("half_width", 4.4))))
			points.append(points[0])
		draw_colored_polygon(points, Color(1.0, 0.39, 0.20, 0.34))
		draw_polyline(points, Color("f39550"), 6.0, true)
		var safe: Vector2 = geometry.get("safe_point", Vector2.ZERO)
		draw_circle(_screen(safe), 24.0, Color("d1f6e2"), false, 4.0, true)

func _draw_foreground() -> void:
	if m == null or not m.g.has(KEY):
		return
	if String(_state()["mode"]) == "ignition_reach":
		var elapsed := float(_state()["mode_elapsed"])
		if elapsed >= 0.75:
			foreground.draw_circle(IGNITION_POINT, 7.0, Color("fff0a5"), false, 3.0, true)
		if elapsed >= 1.0:
			var from := ROCKET_RECT.position + Vector2(70.0, 8.0)
			var to := CANDLE_WICK
			var progress := clampf((elapsed - 1.0) / 0.6, 0.0, 1.0)
			foreground.draw_circle(from.lerp(to, progress), 7.0, Color("fff0a5"))
	if m.chapter2_lawn_beat != 4:
		return
	var current := battle.engine()
	if current != null and current.state == BossEncounter2D.State.OPENING:
		# The opening must remain visible over the opaque character artwork.
		foreground.draw_arc(KING_RECT.get_center(), 110.0, 0.0, TAU, 64,
			Color("fff099"), 9.0, true)
		for spark: int in range(4):
			var angle := float(spark) * PI * 0.5
			foreground.draw_circle(KING_RECT.get_center() + Vector2(cos(angle), sin(angle)) * 110.0,
				8.0, Color("fff7ce"))

func teardown() -> void:
	if battle != null:
		battle.teardown()
	if m != null:
		m.g.erase(KEY)
	set_process(false)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	hide()
