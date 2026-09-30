class_name OperaTreeBookTest
extends Control
## One patient, three decisions, then deliberate treatment. No career/star writes.
signal checkpoint_changed(checkpoint: Dictionary)
signal close_requested

const ART := "res://assets/opera/tree_book_test/"
const SAVE_KEY := "arborist_tree_book_test"
const CAPTIONS: Array[String] = [
	"Which tree? Find the same tree.",
	"What is wrong? Find the orange spots.",
	"Orange spots need leaf spray. Find its bottle.",
	"Let's take the spray to our tree.",
	"Hold this leaf. Spray, spray!",
	"Our tree feels better!",
]
const CUES: Array[String] = ["tree", "leaf", "medicine", "carry", "spray", "done"]
const ORDERS := [[2, 0, 3, 1], [3, 2, 0, 1], [0, 1, 3, 2]]
const ANSWERS := [0, 1, 1]
const PATIENT_RECT := Rect2(900, 105, 310, 305)
const LEAF_RECT := Rect2(701, 118, 142, 142)
const BACK_RECT := Rect2(14, 14, 110, 110)
const REPLAY_RECT := Rect2(455, 539, 150, 120)
const SPRAY_SECONDS := 1.0
# Measured native-cell rectangles, normalized at runtime. The right-hand
# spray drops belong to cell 2; columns are deliberately not equal crops.
const POSE_RECTS := [
	Rect2(0, 0, 640, 606), Rect2(640, 0, 646, 606),
	Rect2(0, 610, 705, 613), Rect2(705, 610, 581, 613),
]
var m: ReefMain
var stage := 0
var treatment := 0.0
var idle_seconds := 0.0
var elapsed := 0.0
var approach := 0.0
var pointer_id := -99
var pressed_choice := -1
var press_position := Vector2.ZERO
var pointer_position := Vector2.ZERO
var wrong_slot := -1
var wrong_time := 0.0
var suspended := false
var suspension_reasons: Dictionary = {}
var closing := false
var textures: Dictionary = {}
var voice: AudioStreamPlayer
var font: Font
var instruction: Label
var hand: Texture2D
var help_level := 0

func setup(main: ReefMain, saved: Variant = {}) -> void:
	m = main
	restore_progress(saved)

func _ready() -> void:
	name = "OperaTreeBookTest"
	size = Vector2(1280, 720)
	mouse_filter = Control.MOUSE_FILTER_STOP
	clip_contents = true
	if m == null:
		set_anchors_preset(Control.PRESET_TOP_LEFT)
		get_viewport().size_changed.connect(_fit_standalone)
		_fit_standalone()
	z_index = 60
	for file: String in ["book.png", "roshan_book.png", "patient.png",
			"leaves_medicine.png", "spray_poses.png", "lagoon_tree_bigleaf_maple.png",
			"lagoon_tree_pacific_dogwood.png", "sky_lagoon_tree_sticker_tall_v1.png"]:
		textures[file] = load(ART + file) as Texture2D
	hand = load("res://assets/castle/training/ghost_hand.png") as Texture2D
	font = ThemeDB.fallback_font
	instruction = Label.new()
	instruction.position = Vector2(170, 25)
	instruction.size = Vector2(930, 80)
	instruction.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	instruction.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_label(instruction, 30, Color("#334b60"), 0)
	instruction.add_theme_color_override("font_color", Color("#334b60"))
	instruction.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(instruction)
	voice = AudioStreamPlayer.new()
	add_child(voice)
	if m == null:
		close_requested.connect(func() -> void: get_tree().quit())
	_announce()
	queue_redraw()

func _fit_standalone() -> void:
	var available := get_viewport_rect().size
	var factor := minf(available.x / 1280.0, available.y / 720.0)
	size = Vector2(1280,720)
	scale = Vector2.ONE * factor
	position = (available - size * factor) * 0.5

func progress_snapshot() -> Dictionary:
	return {"version": 1, "patient": "orange_spots", "stage": stage,
		"treatment": treatment}

func restore_progress(saved: Variant) -> void:
	stage = 0
	treatment = 0.0
	if saved is Dictionary and saved.get("version") == 1 \
			and saved.get("patient") == "orange_spots":
		var value: Variant = saved.get("stage", 0)
		if (value is int or value is float) and is_finite(float(value)) \
				and float(value) == floorf(float(value)) and int(value) in range(6):
			stage = int(value)
		var dose: Variant = saved.get("treatment", 0.0)
		if (dose is int or dose is float) and is_finite(float(dose)) and stage == 4:
			treatment = clampf(float(dose), 0.0, 0.95)
		if stage == 5:
			treatment = 1.0
	approach = 0.0
	idle_seconds = 0.0
	help_level = 0
	_cancel_pointer()
	if is_node_ready():
		_announce()
		queue_redraw()

func choice_rect(slot: int) -> Rect2:
	if stage == 2:
		return Rect2(728 + (slot % 2) * 250, 415 + (slot / 2) * 137, 225, 125)
	return Rect2(122 + (slot % 2) * 252, 198 + (slot / 2) * 197, 178, 180)

func answer_slot() -> int:
	if stage > 2:
		return -1
	return ORDERS[stage].find(ANSWERS[stage])

func _gui_input(event: InputEvent) -> void:
	if closing or suspended or not is_visible_in_tree():
		return
	if event is InputEventScreenTouch:
		if event.canceled:
			if pointer_id == event.index:
				_cancel_pointer()
			return
		_touch(event.index, event.pressed, event.position)
		accept_event()
	elif event is InputEventScreenDrag:
		if pointer_id == event.index:
			pointer_position = event.position
		accept_event()
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		# Godot emits emulated mouse events for touch; only one physical route owns it.
		if event.device != InputEvent.DEVICE_ID_EMULATION:
			_touch(-1, event.pressed, event.position)
		accept_event()
	elif event is InputEventMouseMotion and pointer_id == -1:
		pointer_position = event.position

func _touch(id: int, down: bool, point: Vector2) -> void:
	if down:
		if pointer_id != -99:
			return
		pointer_id = id
		press_position = point
		pointer_position = point
		pressed_choice = -1
		if stage < 3:
			for slot: int in range(4):
				if choice_rect(slot).has_point(point):
					pressed_choice = slot
		queue_redraw()
		return
	if pointer_id != id:
		return
	var slot := pressed_choice
	var origin := press_position
	_cancel_pointer()
	if point.distance_to(origin) > 42.0:
		return
	if m == null and BACK_RECT.has_point(origin) and BACK_RECT.has_point(point):
		shutdown()
		close_requested.emit()
		return
	if stage == 5 and REPLAY_RECT.has_point(origin) and REPLAY_RECT.has_point(point):
		restore_progress({})
		checkpoint_changed.emit(progress_snapshot())
		return
	if stage < 3 and slot >= 0 and choice_rect(slot).has_point(point):
		if ORDERS[stage][slot] == ANSWERS[stage]:
			_set_stage(stage + 1)
		else:
			wrong_slot = slot
			wrong_time = 0.6
			idle_seconds = maxf(idle_seconds, 5.0)
			_say("try_tree" if stage == 0 else "try_spots")

func _cancel_pointer() -> void:
	pointer_id = -99
	pressed_choice = -1
	press_position = Vector2(-1000, -1000)
	pointer_position = press_position

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		suspension_reasons["focus"] = true
	elif what == NOTIFICATION_APPLICATION_PAUSED:
		suspension_reasons["application"] = true
	elif what == NOTIFICATION_PAUSED:
		suspension_reasons["tree"] = true
	elif what == NOTIFICATION_APPLICATION_FOCUS_IN:
		suspension_reasons.erase("focus")
	elif what == NOTIFICATION_APPLICATION_RESUMED:
		suspension_reasons.erase("application")
	elif what == NOTIFICATION_UNPAUSED:
		suspension_reasons.erase("tree")
	elif what == NOTIFICATION_VISIBILITY_CHANGED and not is_visible_in_tree():
		_cancel_pointer()
	suspended = not suspension_reasons.is_empty()
	if suspended:
		_cancel_pointer()
	if voice != null:
		voice.stream_paused = suspended

func shutdown() -> void:
	if closing:
		return
	closing = true
	_cancel_pointer()
	set_process(false)
	checkpoint_changed.emit(progress_snapshot())
	if voice != null:
		voice.stop()
	if is_instance_valid(m):
		for player: AudioStreamPlayer in m.voice_pool:
			if player.stream != null and player.stream.resource_path.begins_with("res://assets/audio/arborist_tree_book/"):
				player.stop()

func _exit_tree() -> void:
	shutdown()

func _process(delta: float) -> void:
	advance(delta)

func advance(delta: float) -> void:
	if suspended or closing or not is_visible_in_tree():
		return
	elapsed += delta
	wrong_time = maxf(0.0, wrong_time - delta)
	if stage < 3 or stage == 4:
		idle_seconds += delta
		help_level = 2 if idle_seconds >= 10.0 else (1 if idle_seconds >= 5.0 else 0)
	if stage == 3:
		approach = minf(1.0, approach + delta / 1.1)
		if approach >= 1.0:
			_set_stage(4)
	elif stage == 4 and pointer_id != -99 \
			and LEAF_RECT.has_point(press_position) and LEAF_RECT.has_point(pointer_position):
		treatment = minf(1.0, treatment + minf(delta, 0.1) / SPRAY_SECONDS)
		checkpoint_changed.emit(progress_snapshot())
		if treatment >= 1.0:
			_set_stage(5)
	queue_redraw()

func _set_stage(next: int) -> void:
	stage = next
	idle_seconds = 0.0
	help_level = 0
	wrong_time = 0.0
	_cancel_pointer()
	checkpoint_changed.emit(progress_snapshot())
	_announce()
	queue_redraw()

func _announce() -> void:
	if instruction != null:
		instruction.text = CAPTIONS[stage]
	_say(CUES[stage])

func _say(cue: String) -> void:
	var path := "res://assets/audio/arborist_tree_book/roshan_arborist_tree_book_" + cue + ".ogg"
	if voice == null or not ResourceLoader.exists(path):
		return
	# The test owns its speech channel, so closing/repeating cancels obsolete cues.
	voice.stop()
	if m != null:
		m._audio_ref()._stop_active_speech()
		m._say("roshan", "arborist_tree_book_" + cue)
		return
	voice.stream = load(path) as AudioStream
	voice.play()

func _tex(file: String) -> Texture2D:
	return textures.get(file) as Texture2D

func _atlas(file: String, region: Rect2) -> Texture2D:
	var result := AtlasTexture.new()
	result.atlas = _tex(file)
	result.region = region
	result.filter_clip = true
	return result

func patient_texture(healthy: bool) -> Texture2D:
	return _atlas("patient.png", Rect2(512 if healthy else 0, 0, 512, 512))

func leaf_texture(index: int, medicine: bool = false) -> Texture2D:
	var regions := [
		Rect2(0, 0, 443, 444), Rect2(443, 0, 444, 430),
		Rect2(887, 0, 443, 444), Rect2(1330, 0, 444, 430),
	]
	if medicine:
		regions = [
			Rect2(0, 460, 492, 427), Rect2(500, 430, 387, 457),
			Rect2(895, 440, 440, 447), Rect2(1340, 440, 434, 447),
		]
	var region: Rect2 = regions[index]
	return _atlas("leaves_medicine.png", Rect2(region.position * (1024.0 / 1774.0),
		region.size * (1024.0 / 1774.0)))

func pose_texture(index: int) -> Texture2D:
	var region: Rect2 = POSE_RECTS[index]
	var factor := Vector2(1024.0/1286.0,974.0/1223.0)
	var texture := _atlas("spray_poses.png", Rect2(region.position * factor,
		region.size * factor)) as AtlasTexture
	texture.margin = Rect2(Vector2(58 if index == 3 else 0,0) * factor,
		(Vector2(720,615) - region.size) * factor)
	return texture

func _fit(texture: Texture2D, box: Rect2) -> void:
	if texture == null:
		return
	var factor := minf(box.size.x / texture.get_width(), box.size.y / texture.get_height())
	var dimensions := texture.get_size() * factor
	draw_texture_rect(texture, Rect2(box.get_center() - dimensions / 2, dimensions), false)

func _panel(rect: Rect2, color: Color, edge: Color, radius: int = 22) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.border_color = edge
	style.set_border_width_all(3)
	style.set_corner_radius_all(radius)
	draw_style_box(style, rect)

func _draw() -> void:
	if textures.is_empty():
		return
	draw_rect(Rect2(0, 0, 1280, 720), Color("#e5f2e8"))
	_panel(Rect2(690, 101, 558, 590), Color("#f5f3df"), Color("#adcdb8"), 40)
	draw_arc(Vector2(1090, 672), 450, PI, TAU, 60, Color("#d4e5ce"), 24, true)
	_fit(_tex("book.png"), Rect2(18, 120, 660, 568))
	if m == null:
		_panel(BACK_RECT, Color("#fff6de"), Color("#7d9b99"))
		draw_line(Vector2(92, 68), Vector2(44, 68), Color("#426878"), 8, true)
		draw_polyline(PackedVector2Array([Vector2(63,47),Vector2(42,68),Vector2(63,89)]),
			Color("#426878"),8,true)
	for step: int in range(3):
		draw_circle(Vector2(579+step*44, 112), 12, Color("#e4b664") if stage > step else Color("#bdccc0"))
	_fit(patient_texture(stage == 5), PATIENT_RECT)
	if stage < 5:
		draw_line(LEAF_RECT.get_center(),Vector2(1000,210),Color("#d6c6a0"),3,true)
		_panel(LEAF_RECT, Color("#fffdf0"), Color("#daaa68"), 64)
		_fit(leaf_texture(1), LEAF_RECT.grow(-12))
	if stage < 2:
		_fit(_tex("roshan_book.png"), Rect2(704, 359, 310, 330))
	if stage < 3:
		for slot: int in range(4):
			var rect := choice_rect(slot)
			if wrong_time > 0 and wrong_slot == slot:
				rect.position.x += sin(wrong_time*40.0)*8.0
			var target := slot == answer_slot()
			var edge := Color("#d7b55d") if target and help_level > 0 else Color("#a9bcb1")
			_panel(rect, Color("#fffbee"), edge, 20)
			if slot == pressed_choice:
				_panel(rect.grow(-4), Color("#e0efcf"), edge, 18)
			var value: int = ORDERS[stage][slot]
			if stage == 0:
				if value == 0:
					_fit(patient_texture(false), rect.grow(-9))
				else:
					_fit(_tex(["lagoon_tree_bigleaf_maple.png",
						"lagoon_tree_pacific_dogwood.png","sky_lagoon_tree_sticker_tall_v1.png"][value-1]),rect.grow(-12))
			else:
				_fit(leaf_texture(value,stage==2),rect.grow(-12))
			if target and help_level == 2:
				_fit(hand,Rect2(rect.end-Vector2(68,55+sin(elapsed*3)*9),Vector2(80,80)))
	if stage == 2:
		_fit(leaf_texture(1),Rect2(132,231,165,210))
		_fit(leaf_texture(1,true),Rect2(380,231,170,210))
		draw_line(Vector2(304,330),Vector2(360,330),Color("#da9d56"),7,true)
		draw_polyline(PackedVector2Array([Vector2(344,312),Vector2(362,330),Vector2(344,348)]),Color("#da9d56"),7,true)
		draw_string(font,Vector2(166,503),"Spots",HORIZONTAL_ALIGNMENT_LEFT,-1,28,Color("#4b6374"))
		draw_string(font,Vector2(411,503),"Spray",HORIZONTAL_ALIGNMENT_LEFT,-1,28,Color("#4b6374"))
	if stage >= 3:
		var pose := 0
		if stage == 4:
			pose = 2 if pointer_id != -99 and LEAF_RECT.has_point(pointer_position) else 1
		elif stage == 5:
			pose = 3
		var actor_x := lerpf(675,735,approach) if stage == 3 else 735.0
		var actor_y := lerpf(340,100,approach) if stage == 3 else 100.0
		_fit(pose_texture(pose),Rect2(actor_x,actor_y,350,350))
		if stage == 4:
			_fit(leaf_texture(1,true),Rect2(192,234,310,270))
			draw_arc(LEAF_RECT.get_center(),80,-PI/2,-PI/2+TAU*treatment,48,Color("#57bba3"),10,true)
			if help_level > 0:
				_fit(hand,Rect2(LEAF_RECT.position+Vector2(80,78+sin(elapsed*3)*10),Vector2(95,95)))
		elif stage == 3:
			_fit(leaf_texture(1,true),Rect2(192,234,310,270))
		else:
			_panel(Rect2(169,227,327,286),Color("#fff7d0"),Color("#e0bd69"),54)
			_fit(patient_texture(true),Rect2(194,244,275,250))
			_panel(REPLAY_RECT,Color("#e7f0d3"),Color("#819d8c"))
			draw_arc(REPLAY_RECT.get_center(),31,-PI*0.65,PI*0.88,32,Color("#527b73"),7,true)
			draw_circle(REPLAY_RECT.get_center()+Vector2(-27,15),9,Color("#527b73"))
