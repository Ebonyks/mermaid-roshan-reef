class_name FairyRestorationPrototype
extends Control
## Isolated Chapter 3 review scene. Never reads or writes reef_save.json.
## All work goes through live one-finger input, arrival and local contact.

const SAVE_PATH := "user://fairy_restoration_prototype.json"
const ALL := 7
const SIZE := Vector2(1280, 720)
const TREE_POINTS: Array[Vector2] = [Vector2(240, 245), Vector2(390, 200), Vector2(415, 370)]
const FRUIT_POINTS: Array[Vector2] = [Vector2(245, 275), Vector2(400, 245), Vector2(405, 395)]
const CHEF_POINTS: Array[Vector2] = [Vector2(740, 450), Vector2(885, 450), Vector2(1030, 450)]
const FRIEND_POINTS: Array[Vector2] = [Vector2(720, 255), Vector2(895, 200), Vector2(1070, 275)]
const FLOWER_POINTS: Array[Vector2] = [Vector2(300, 255), Vector2(640, 210), Vector2(980, 255)]
const ROOT_POINT := Vector2(340, 535)
const APPLE := "res://assets/props/story/fruit_apple.png"
const TREE := "res://assets/mg/tree.png"
const LEAF := "res://assets/fairy/sprites/boss_leaf.png"
const TABLE := "res://assets/flats/castle/dream_house/dining_table.png"
const BUTTERFLY := "res://assets/props/gen2/butterfly1.png"
const THORN := "res://assets/fairy/sprites/danger_thorn_halo.png"
const POINTER := "res://assets/castle/training/ghost_hand.png"
const STAR := "res://assets/mg/star.png"
const FARMER := "res://assets/opera/worlds/actors/animation/roshan_farmer_sheet_a.png"
const CHEF := "res://assets/opera/worlds/actors/animation/roshan_chef_sheet_a.png"
const FAIRY := "res://assets/characters/skins/fairy_mermaid.png"
const WINGS := "res://assets/characters/skins/fairy_wing_card.png"
const DOOR := "res://assets/flats/castle/fairy_conservatory/moonflower_door_open.png"
const GLOW := "res://assets/flats/castle/main_hall_2screen/castle_sconce_glow_reuse.png"

@export var persist := true
var progress: Dictionary = {"cleared": 0, "water": 0.0, "picked": 0, "cut": 0, "fed": 0, "bloom": 0, "returned": false}
var location := "castle"
var suspended := false
var cue_history: Array[String] = []
var _world: Node2D
var _scene: Node2D
var _actor: Sprite2D
var _wings: Sprite2D
var _hand: Sprite2D
var _magic: Sprite2D
var _title: Label
var _caption: Label
var _status: Label
var _effects: Control
var _flower_cards: Array[Sprite2D] = []
var _music: AudioStreamPlayer
var _voice: AudioStreamPlayer
var _cache: Dictionary = {}
var _owner := -2
var _last_point := Vector2.ZERO
var _stroke_start := Vector2.ZERO
var _action := ""
var _index := -1
var _target := Vector2.ZERO
var _approach := Vector2.ZERO
var _arrived := false
var _action_time := 0.0
var _clock := 0.0
var _shot_clock := 0.0
var _aim := Vector2(640, 520)
var _shot_tip := Vector2.ZERO
var _shot_visible := 0.0
var _pointer_base := Vector2.ZERO
var _roshan_position := Vector2(555, 535)

func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	if persist:
		load_checkpoint()
	_world = Node2D.new()
	add_child(_world)
	_music = AudioStreamPlayer.new()
	_music.stream = load("res://assets/audio/music/picture_garden.ogg") as AudioStream
	_music.volume_db = -20.0
	add_child(_music)
	_music.play()
	_voice = AudioStreamPlayer.new()
	_voice.volume_db = -4.0
	add_child(_voice)
	resized.connect(_layout)
	_layout()
	_rebuild()

func _layout() -> void:
	var factor: float = minf(size.x / SIZE.x, size.y / SIZE.y)
	_world.scale = Vector2.ONE * factor
	_world.position = (size - SIZE * factor) * 0.5

func phase() -> String:
	if int(progress.cleared) != ALL: return "arborist"
	if float(progress.water) < 1.0: return "water"
	if int(progress.picked) != ALL: return "harvest"
	if int(progress.cut) != ALL: return "chef"
	if int(progress.fed) != ALL: return "picnic"
	if int(progress.bloom) != ALL: return "shooter"
	return "complete"

func _texture(path: String) -> Texture2D:
	if not _cache.has(path): _cache[path] = load(path) as Texture2D
	return _cache[path] as Texture2D

func _sprite(path: String, point: Vector2, bounds: Vector2, parent: Node = null) -> Sprite2D:
	var card := Sprite2D.new()
	card.texture = _texture(path)
	card.position = point
	var texture_size: Vector2 = card.texture.get_size()
	card.scale = Vector2.ONE * minf(bounds.x / texture_size.x, bounds.y / texture_size.y)
	(parent if parent != null else _scene).add_child(card)
	return card

func _label(text: String, point: Vector2, bounds: Vector2, font_size: int = 24) -> Label:
	var label := Label.new()
	label.text = text
	label.position = point
	label.size = bounds
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", Color("34315d"))
	_scene.add_child(label)
	return label

func _panel(point: Vector2, bounds: Vector2) -> void:
	var panel := Panel.new()
	panel.position = point
	panel.size = bounds
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.bg_color = Color(1.0, 0.96, 0.85, 0.94)
	style.corner_radius_top_left = 24
	style.corner_radius_top_right = 24
	style.corner_radius_bottom_left = 24
	style.corner_radius_bottom_right = 24
	panel.add_theme_stylebox_override("panel", style)
	_scene.add_child(panel)

func _rebuild() -> void:
	if location == "garden" and is_instance_valid(_actor): _roshan_position = _actor.position
	_cancel_input()
	if is_instance_valid(_scene):
		_world.remove_child(_scene)
		_scene.queue_free()
	_scene = Node2D.new()
	_world.add_child(_scene)
	_flower_cards.clear()
	if location == "castle":
		_build_castle()
	else:
		_build_garden()
	_panel(Vector2(145, 18), Vector2(990, 80))
	_title = _label("FAERIE GARDEN", Vector2(190, 22), Vector2(900, 38), 28)
	_status = _label(_status_text(), Vector2(190, 60), Vector2(900, 28), 18)
	_panel(Vector2(160, 624), Vector2(960, 72))
	_caption = _label("", Vector2(182, 636), Vector2(916, 48), 23)
	_panel(Vector2(20, 6), Vector2(112, 112))
	_label("←", Vector2(20, 6), Vector2(112, 112), 40)
	_hand = _sprite(POINTER, Vector2.ZERO, Vector2(88, 88))
	_hand.z_index = 30
	_effects = Control.new()
	_effects.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_effects.z_index = 20
	_effects.draw.connect(_draw_effects)
	_scene.add_child(_effects)
	_set_cue()
	_effects.queue_redraw()

func _background(fairy: bool) -> void:
	for row: int in range(2):
		for column: int in range(4 if fairy else 2):
			var path: String
			var tile_size: Vector2
			var native: Vector2
			if fairy:
				path = "res://assets/flats/fairy_conservatory_handoff/background/handoff_background_r%d_c%d.png" % [row, column]
				tile_size = Vector2(910, 1024)
				native = Vector2(3640, 2048)
			else:
				path = "res://assets/flats/castle/main_hall_2screen/tiles/main_hall_room_led_r%d_c%d.png" % [row, column + 2]
				tile_size = Vector2(836, 470)
				native = Vector2(1672, 941)
			var card := _sprite(path, Vector2.ZERO, SIZE)
			card.centered = false
			card.scale = SIZE / native
			card.position = Vector2(column, row) * tile_size * card.scale

func _build_castle() -> void:
	_background(false)
	_sprite(DOOR, Vector2(635, 355), Vector2(390, 430))
	if bool(progress.returned):
		for point: Vector2 in [Vector2(230, 295), Vector2(1070, 295)]:
			_sprite(GLOW, point, Vector2(150, 170))
	_sprite("res://assets/characters/roshan_25d/roshan_base.png", Vector2(425, 485), Vector2(180, 230))
	_pointer_base = Vector2(630, 425)

func _build_garden() -> void:
	_background(true)
	var stage: String = phase()
	for point: Vector2 in [Vector2(325, 560), Vector2(890, 565)]:
		var pad := _sprite(LEAF, point, Vector2(550, 430))
		pad.rotation = PI * 0.5
	_sprite("res://assets/fairy/sprites/ornament_lily_cluster.png", Vector2(115, 560), Vector2(250, 200))
	if stage not in ["shooter", "complete"]:
		_sprite(TREE, Vector2(335, 342), Vector2(330, 470))
		_sprite(TABLE, Vector2(885, 505), Vector2(440, 260))
		for index: int in range(3):
			if not _has("cleared", index):
				_sprite(THORN, TREE_POINTS[index], Vector2(120, 120))
			if float(progress.water) >= 1.0 and not _has("picked", index):
				_sprite(APPLE, FRUIT_POINTS[index], Vector2(75, 90))
			var friend := _sprite(BUTTERFLY, FRIEND_POINTS[index], Vector2(125, 105))
			friend.set_meta("fed", _has("fed", index))
			if _has("picked", index) and not _has("fed", index):
				if _has("cut", index):
					_split_apple(CHEF_POINTS[index])
				else:
					_sprite(APPLE, CHEF_POINTS[index], Vector2(100, 110))
			if _has("fed", index):
				_sprite(STAR, FRIEND_POINTS[index] + Vector2(0, 80), Vector2(54, 54))
	else:
		for index: int in range(3):
			var form: String = "bloom" if _has("bloom", index) else "bud"
			_flower_cards.append(_sprite("res://assets/fairy/sprites/boss_%s.png" % form, FLOWER_POINTS[index], Vector2(210, 210)))
			_sprite(BUTTERFLY, Vector2(FLOWER_POINTS[index].x, maxf(145, FLOWER_POINTS[index].y - 95)), Vector2(96, 78))
		_sprite("res://assets/fairy/sprites/bug_moth.png", Vector2(470, 360), Vector2(90, 90))
		_sprite("res://assets/fairy/sprites/bug_moth.png", Vector2(810, 360), Vector2(90, 90))
	_wings = _sprite(WINGS, _roshan_position, Vector2(205, 150))
	_actor = _sprite(FARMER, _roshan_position, Vector2(1024, 1024))
	_actor.hframes = 4
	_actor.vframes = 4
	_actor.scale = Vector2.ONE * 0.9
	_actor.z_index = 10
	_pose(0)
	if stage == "chef" or stage == "picnic": _actor.texture = _texture(CHEF)
	if stage in ["shooter", "complete"]:
		_actor.texture = _texture(FAIRY)
		_actor.hframes = 1
		_actor.vframes = 1
		_actor.scale = Vector2.ONE * (195.0 / _actor.texture.get_height())
		_wings.visible = false
		_actor.position = _aim
	_magic = _sprite(STAR, Vector2.ZERO, Vector2(38, 38), _actor)
	_magic.position = Vector2(-77, -20)
	_magic.visible = false
	_pointer_base = _next_target() + Vector2(0, -72)
	if stage == "complete": _sprite(STAR, Vector2(640, 525), Vector2(95, 95))

func _split_apple(point: Vector2) -> void:
	for side: int in range(2):
		var half := _sprite(APPLE, point + Vector2(-38 if side == 0 else 38, 0), Vector2(100, 110))
		half.region_enabled = true
		var native: Vector2 = half.texture.get_size()
		half.region_rect = Rect2(Vector2(native.x * 0.5 * side, 0), Vector2(native.x * 0.5, native.y))

func _pose(frame: int) -> void:
	if is_instance_valid(_actor) and _actor.hframes == 4: _actor.frame = frame

func _has(key: String, index: int) -> bool:
	return (int(progress[key]) & (1 << index)) != 0

func _first_missing(key: String) -> int:
	for index: int in range(3):
		if not _has(key, index): return index
	return 0

func _next_target() -> Vector2:
	match phase():
		"arborist": return TREE_POINTS[_first_missing("cleared")]
		"water": return ROOT_POINT
		"harvest": return FRUIT_POINTS[_first_missing("picked")]
		"chef": return CHEF_POINTS[_first_missing("cut")]
		"picnic": return FRIEND_POINTS[_first_missing("fed")]
		"shooter": return FLOWER_POINTS[_first_missing("bloom")]
	return Vector2(640, 525)

func _status_text() -> String:
	if location == "castle": return "Castle magic · faerie half restored" if bool(progress.returned) else "The candle is gone · help the faerie garden"
	var names: Dictionary = {"arborist": "Arborist · untangle the sick tree", "water": "Arborist · water its thirsty roots", "harvest": "Harvest · fruit for butterfly snacks", "chef": "Chef · slice the fruit", "picnic": "Host · feed the butterflies", "shooter": "Faerie flight · help the flowers bloom", "complete": "Faerie magic restored · carry it home"}
	return String(names[phase()])

func _set_cue() -> void:
	if location == "castle":
		_say("enter" if not bool(progress.returned) else "returned", "The candle is gone. Let's help the faerie garden!" if not bool(progress.returned) else "The faerie magic is home! You can visit your butterfly friends.")
		return
	var cues: Dictionary = {"arborist": "Tap the tangled branches. Let's help our tree!", "water": "Rub across the thirsty roots to water our tree.", "harvest": "Our tree is well! Pick three apples for the butterflies.", "chef": "Swipe across each apple to make little butterfly snacks.", "picnic": "Tap each butterfly to share its snack.", "shooter": "Hold and glide under the flowers. Your sparkles help them bloom!", "complete": "Happy butterflies helped the flowers bloom! Tap the magic to take it home."}
	_say(phase(), String(cues[phase()]))

func _say(key: String, text: String) -> void:
	# Additive, synthetic Roshan cues use the established Kokoro voice settings.
	# Protected recordings remain byte-identical; listening acceptance is open.
	_caption.text = text
	cue_history.append(key + ": " + text)
	print("FAIRYCUE|", key, "|", text)
	_voice.stop()
	_music.volume_db = -20.0
	var path: String = "res://assets/prototypes/fairy_restoration/voices/%s.ogg" % key
	if ResourceLoader.exists(path):
		_voice.stream = load(path) as AudioStream
		_music.volume_db = -28.0
		_voice.play()

func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		back_to_castle()
		get_viewport().set_input_as_handled()
		return
	if suspended: return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed: _press(_logical(touch.position), touch.index)
		elif touch.index == _owner: _release()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == _owner: _drag(_logical(drag.position))
	elif event is InputEventMouseButton and _owner < 0:
		var click := event as InputEventMouseButton
		if click.button_index == MOUSE_BUTTON_LEFT:
			if click.pressed: _press(_logical(click.position), -1)
			elif _owner == -1: _release()
	elif event is InputEventMouseMotion and _owner == -1:
		_drag(_logical((event as InputEventMouseMotion).position))

func _logical(point: Vector2) -> Vector2:
	return (point - _world.position) / _world.scale

func _press(point: Vector2, owner: int) -> void:
	if _owner != -2: return
	_owner = owner
	_last_point = point
	_stroke_start = point
	if Rect2(20, 6, 112, 112).has_point(point):
		back_to_castle()
		return
	if location == "castle":
		if Rect2(460, 160, 350, 420).has_point(point):
			location = "garden"
			_rebuild()
		return
	if phase() == "complete":
		if point.distance_to(Vector2(640, 525)) < 120:
			progress.returned = true
			save_checkpoint()
			back_to_castle()
		return
	if phase() == "shooter":
		if point.y > 390 and point.y < 620:
			_action = "shoot"
			_aim = Vector2(clampf(point.x, 130, 1150), 530)
		return
	var points: Array[Vector2] = []
	var key := ""
	match phase():
		"arborist": points = TREE_POINTS; key = "cleared"
		"water": points = [ROOT_POINT]; key = "water"
		"harvest": points = FRUIT_POINTS; key = "picked"
		"chef": points = CHEF_POINTS; key = "cut"
		"picnic": points = FRIEND_POINTS; key = "fed"
	for index: int in range(points.size()):
		if key != "water" and _has(key, index): continue
		if point.distance_to(points[index]) > 68: continue
		_action = key
		_index = index
		_target = points[index]
		_approach = _target + Vector2(85, 20)
		_arrived = false
		_action_time = 0.0
		_pose(4)
		break

func _drag(point: Vector2) -> void:
	if _action == "shoot": _aim.x = clampf(point.x, 130, 1150)
	if not _arrived:
		_last_point = point
		return
	if _action == "water" and point.distance_to(ROOT_POINT) < 95 and _last_point.distance_to(ROOT_POINT) < 95:
		var distance: float = minf(point.distance_to(_last_point), 40)
		progress.water = minf(1.0, float(progress.water) + distance / 320.0)
		_magic.visible = true
		_effects.queue_redraw()
		if float(progress.water) >= 1.0: _commit()
	elif _action == "cut" and absf(point.y - _target.y) < 70:
		var crosses: bool = (_stroke_start.x < _target.x - 28 and point.x > _target.x + 28) or (_stroke_start.x > _target.x + 28 and point.x < _target.x - 28)
		if crosses and absf(_stroke_start.y - _target.y) < 70: _commit()
	_last_point = point

func _release() -> void:
	_owner = -2
	# Selected tap work completes after local arrival. Gestures never finish
	# from arrival or elapsed time; shooter stops immediately on release.
	if _action in ["water", "cut", "shoot"]: _cancel_input()
	save_checkpoint()

func _cancel_input() -> void:
	_owner = -2
	_action = ""
	_index = -1
	_arrived = false
	_action_time = 0.0
	_shot_clock = 0.0
	_shot_visible = 0.0
	if is_instance_valid(_magic): _magic.visible = false

func _process(delta: float) -> void:
	if suspended or not is_instance_valid(_scene): return
	_clock += delta
	if is_instance_valid(_hand): _hand.position = _pointer_base + Vector2(0, sin(_clock * 3.0) * 7)
	if _voice.playing: _music.volume_db = -28.0
	else: _music.volume_db = -20.0
	if location != "garden": return
	if phase() in ["water", "chef"]: _effects.queue_redraw()
	if phase() == "complete":
		_effects.queue_redraw()
		return
	if _action == "shoot":
		_actor.position = _actor.position.move_toward(_aim, delta * 700)
		_shot_clock += delta
		_shot_visible = maxf(0.0, _shot_visible - delta)
		if _shot_clock >= 0.7:
			_shot_clock = 0.0
			_shot_tip = Vector2(_actor.position.x, 160)
			for moth_x: float in [470.0, 810.0]:
				if absf(_actor.position.x - moth_x) < 50.0: _shot_tip.y = 360.0
			_shot_visible = 0.22
			for index: int in range(3):
				if not _has("bloom", index) and absf(_actor.position.x - FLOWER_POINTS[index].x) < 85:
					progress.bloom = int(progress.bloom) | (1 << index)
					_flower_cards[index].texture = _texture("res://assets/fairy/sprites/boss_bloom.png")
					save_checkpoint()
					_pointer_base = _next_target() + Vector2(0, -72)
					if int(progress.bloom) == ALL: _rebuild()
					break
		_effects.queue_redraw()
		return
	if _action.is_empty(): return
	if not _arrived:
		_actor.position = _actor.position.move_toward(_approach, delta * 520)
		_wings.position = _actor.position
		if _actor.position.distance_to(_approach) <= 2:
			_arrived = true
			_pose(8 if _action != "water" else 9)
			_magic.visible = true
	else:
		_action_time += delta
		if _action in ["cleared", "picked", "fed"] and _action_time >= 0.55: _commit()

func _commit() -> void:
	if _action == "water":
		progress.water = 1.0
	elif _action in ["cleared", "picked", "cut", "fed", "bloom"] and _index >= 0:
		progress[_action] = int(progress[_action]) | (1 << _index)
	else:
		return
	save_checkpoint()
	_rebuild()

func back_to_castle() -> void:
	_cancel_input()
	save_checkpoint()
	location = "castle"
	_rebuild()

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		suspended = true
		_cancel_input()
		if is_instance_valid(_voice): _voice.stop()
		if is_instance_valid(_music): _music.stream_paused = true
		save_checkpoint()
	elif what == NOTIFICATION_APPLICATION_FOCUS_IN:
		suspended = false
		if is_instance_valid(_music): _music.stream_paused = false

func _exit_tree() -> void:
	_cancel_input()
	save_checkpoint()
	if is_instance_valid(_voice): _voice.stop()
	if is_instance_valid(_music): _music.stop()

func save_checkpoint() -> void:
	if not persist: return
	var temporary: String = SAVE_PATH + ".tmp"
	var file := FileAccess.open(temporary, FileAccess.WRITE)
	if file == null:
		push_warning("Prototype checkpoint write unavailable; progress remains in memory")
		return
	file.store_string(JSON.stringify(progress))
	file.close()
	if FileAccess.file_exists(SAVE_PATH):
		var previous := JSON.new()
		if previous.parse(FileAccess.get_file_as_string(SAVE_PATH)) == OK and previous.data is Dictionary:
			DirAccess.copy_absolute(SAVE_PATH, SAVE_PATH + ".bak")
	var error: Error = DirAccess.rename_absolute(temporary, SAVE_PATH)
	if error != OK: push_warning("Prototype checkpoint replace failed: %s" % error)

func load_checkpoint() -> void:
	for path: String in [SAVE_PATH, SAVE_PATH + ".bak"]:
		if not FileAccess.file_exists(path): continue
		var parser := JSON.new()
		if parser.parse(FileAccess.get_file_as_string(path)) != OK: continue
		var parsed: Variant = parser.data
		if parsed is not Dictionary: continue
		var loaded: Dictionary = parsed as Dictionary
		progress.merge(loaded, true)
		for key: String in ["cleared", "picked", "cut", "fed", "bloom"]:
			progress[key] = int(progress[key]) & ALL if progress[key] is int or progress[key] is float else 0
		progress.water = clampf(float(progress.water), 0.0, 1.0) if progress.water is float or progress.water is int else 0.0
		progress.returned = progress.returned == true
		# Future/malformed state cannot bypass prerequisites. Preserve other keys.
		if int(progress.cleared) != ALL: progress.water = 0.0
		if float(progress.water) < 1.0: progress.picked = 0
		progress.cut = int(progress.cut) & int(progress.picked)
		progress.fed = int(progress.fed) & int(progress.cut)
		if int(progress.fed) != ALL: progress.bloom = 0
		if int(progress.bloom) != ALL: progress.returned = false
		return

func _draw_effects() -> void:
	if location != "garden" or not is_instance_valid(_world): return
	if phase() == "water":
		_effects.draw_circle(ROOT_POINT, 58, Color(0.25, 0.7, 1.0, 0.3))
		_effects.draw_arc(ROOT_POINT, 58, -PI * 0.5, -PI * 0.5 + TAU * float(progress.water), 30, Color("a1ffeb"), 9, true)
		var wiggle: float = sin(_clock * 2.4) * 40.0
		_effects.draw_line(ROOT_POINT + Vector2(-42, 0), ROOT_POINT + Vector2(42, 0), Color("a1ffeb"), 6, true)
		_effects.draw_circle(ROOT_POINT + Vector2(wiggle, 0), 12, Color("fff2ab"))
	if phase() == "chef":
		var point: Vector2 = CHEF_POINTS[_first_missing("cut")]
		_effects.draw_line(point + Vector2(-52, 0), point + Vector2(52, 0), Color("fff2ab"), 5, true)
		_effects.draw_circle(point + Vector2(sin(_clock * 2.4) * 44, 0), 9, Color("a1ffeb"))
	if _shot_visible > 0:
		_effects.draw_line(_actor.position + Vector2(0, -80), _shot_tip, Color("fff2ab"), 9, true)
		_effects.draw_circle(_shot_tip, 15, Color("ffffff"))
	if phase() == "complete":
		_effects.draw_circle(Vector2(640, 525), 70, Color(1, 0.85, 0.6, 0.7))
		_effects.draw_arc(Vector2(640, 525), 85, 0, TAU, 50, Color("ddbbff"), 8, true)
