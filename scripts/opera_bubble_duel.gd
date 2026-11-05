extends Control
## Optional Opera practice game. All swim and color state belongs to this overlay.

signal close_requested

const ROUTE_ID := "opera_bubble_duel"
const POOL := preload("res://assets/flats/castle/interactions_v4/backgrounds/room_mermaid_pool_background.png")
const BUBBLES := preload("res://assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png")
const BUBBLE_REGION := Rect2(69, 300, 144, 145)
const ROSHAN := preload("res://assets/characters/roshan_25d/roshan_base.png")
const SWIM := preload("res://assets/characters/roshan_25d/roshan_swim_front.png")
const OTTER := preload("res://assets/sprites/sky_lagoon/animals/otter_idle_atlas.png")
const PEARL := preload("res://assets/opera/worlds/teacher/pearl_uncounted.png")
const SHELL := preload("res://assets/ui/pearl_full.png")
const POP := preload("res://assets/sprites/fx_water/fx_water_bubble_burst_atlas.png")
const HAND := preload("res://assets/castle/training/ghost_hand.png")
const START := Vector2(350, 380)
const ARENA := Rect2(116, 208, 1048, 390)
const PLAYER_SIZE := 154.0
const FIN_Y := 61.0
const FIN_X := 31.0
const TARGET_RADIUS := 33.0
const COLORS: Array[Color] = [
	Color(0.70, 0.95, 1.0), Color(1.0, 0.74, 0.86), Color(1.0, 0.91, 0.64),
	Color(0.74, 1.0, 0.81), Color(0.85, 0.76, 1.0),
]

enum Mode { HUB, DUEL, PRACTICE, CURRENT, SHOP, CELEBRATE }

var main: ReefMain
var mode := Mode.HUB
var menu: Control
var heading: Label
var hint: Label
var bubble: AtlasTexture
var swimmer := START
var rival := Vector2(856, 515)
var aim := START
var press_at := Vector2.ZERO
var velocity_y := 0.0
var direction := 1.0
var touch_id := -1
var mouse_held := false
var armed := false
var climbing := false
var assisted_slot := -1
var elapsed := 0.0
var active_time := 0.0
var rival_bubbles := 2
var player_bubbles := 2
var score := 0
var tint_index := 0
var pop_time := 0.0
var pop_at := Vector2.ZERO


func setup(owner_main: ReefMain) -> void:
	main = owner_main
	name = "OperaBubbleDuel"
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 70
	add_to_group(LivingWorldDirector.QUIET_GROUP)
	bubble = AtlasTexture.new()
	bubble.atlas = BUBBLES
	bubble.region = BUBBLE_REGION
	bubble.filter_clip = true
	heading = _label(Vector2(150, 32), 46)
	hint = _label(Vector2(150, 94), 27)
	menu = Control.new()
	menu.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(menu)
	_show_hub()


func _label(at: Vector2, font_size: int) -> Label:
	var label := Label.new()
	label.position = at
	label.size = Vector2(980, 58)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_hud_label(label, font_size)
	add_child(label)
	return label


func _clear_menu() -> void:
	for child: Node in menu.get_children():
		menu.remove_child(child)
		child.queue_free()


func _card(title: String, art: Texture2D, at: Vector2, action: Callable,
		tint: Color = Color.WHITE) -> void:
	var button := Button.new()
	button.position = at
	button.size = Vector2(208, 176)
	button.tooltip_text = title
	StorybookUI.style_picture_button(button)
	button.pressed.connect(action)
	menu.add_child(button)
	var picture := TextureRect.new()
	picture.position = Vector2(46, 10)
	picture.size = Vector2(116, 116)
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	picture.texture = art
	picture.modulate = tint
	button.add_child(picture)
	var caption := Label.new()
	caption.text = title
	caption.position = Vector2(0, 126)
	caption.size = Vector2(208, 42)
	caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(caption, 23)
	button.add_child(caption)


func _show_hub() -> void:
	_reset_input()
	_clear_menu()
	mode = Mode.HUB
	heading.text = "Bubble Duel"
	hint.text = "Choose a place to play"
	var otter := AtlasTexture.new()
	otter.atlas = OTTER
	otter.region = Rect2(0, 0, 256, 256)
	_card("Bubble Duel", otter, Vector2(194, 278), _begin.bind(Mode.DUEL))
	_card("Practice Lagoon", bubble, Vector2(422, 278), _begin.bind(Mode.PRACTICE))
	_card("Current Ride", PEARL, Vector2(650, 278), _begin.bind(Mode.CURRENT))
	_card("Shell Shop", SHELL, Vector2(878, 278), _show_shop)
	queue_redraw()


func _show_shop() -> void:
	_clear_menu()
	mode = Mode.SHOP
	heading.text = "Shell Shop"
	hint.text = "Choose a bubble color"
	for index: int in range(COLORS.size()):
		var name_text: String = ["Aqua", "Rose", "Gold", "Mint", "Lilac"][index]
		if tint_index == index:
			name_text += "  ✓"
		_card(name_text, bubble, Vector2(86 + 225 * index, 278),
			_select_color.bind(index), COLORS[index])
	queue_redraw()


func _select_color(index: int) -> void:
	tint_index = index
	_show_shop()


func _begin(next: Mode) -> void:
	_reset_input()
	_clear_menu()
	mode = next
	swimmer = START
	direction = 1.0
	rival = Vector2(856, 515)
	rival_bubbles = 2
	player_bubbles = 2
	score = 0
	elapsed = 0.0
	active_time = 0.0
	pop_time = 0.0
	heading.text = "Current Ride" if mode == Mode.CURRENT else (
		"Practice Lagoon" if mode == Mode.PRACTICE else "Bubble Duel")
	hint.text = "Touch a pearl to swim to it" if mode == Mode.CURRENT else (
		"Touch a glowing bubble to kick up and pop it")
	main._say("roshan", "idle2")


func go_back() -> void:
	if mode == Mode.HUB:
		close_requested.emit()
	else:
		main.clear_dialogue()
		_show_hub()
		# The global Back controller pops the route before invoking this callback.
		main._navigation_push(ROUTE_ID, self, go_back)


func shutdown() -> void:
	remove_from_group(LivingWorldDirector.QUIET_GROUP)
	_reset_input()
	hide()
	set_process(false)
	main.clear_dialogue()


func _reset_input() -> void:
	touch_id = -1
	mouse_held = false
	armed = false
	climbing = false
	assisted_slot = -1
	velocity_y = 0.0


func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT or what == NOTIFICATION_APPLICATION_PAUSED \
			or what == NOTIFICATION_PAUSED:
		_reset_input()


func _gui_input(event: InputEvent) -> void:
	if mode != Mode.DUEL and mode != Mode.PRACTICE and mode != Mode.CURRENT:
		return
	if event is InputEventScreenTouch:
		if event.pressed and touch_id < 0 and not mouse_held:
			touch_id = event.index
			_kick(event.position)
		elif not event.pressed and touch_id == event.index:
			touch_id = -1
			if event.canceled:
				_reset_input()
		accept_event()
	elif event is InputEventScreenDrag:
		if touch_id == event.index and event.position.distance_to(press_at) > 18.0:
			_steer(event.position)
		accept_event()
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if touch_id < 0:
			mouse_held = event.pressed
			if mouse_held:
				_kick(event.position)
		accept_event()
	elif event is InputEventMouseMotion and mouse_held \
			and event.position.distance_to(press_at) > 18.0:
		_steer(event.position)
		accept_event()


func _kick(at: Vector2) -> void:
	if player_bubbles == 0:
		return
	press_at = at
	armed = true
	climbing = true
	_steer(at)
	var closest := 63.0
	for slot: int in range(rival_bubbles):
		var target := _target(slot)
		var distance := at.distance_to(target)
		if _target_is_visible(slot) and distance < closest:
			closest = distance
			assisted_slot = slot
			direction = 1.0 if target.x >= swimmer.x else -1.0


func _steer(at: Vector2) -> void:
	assisted_slot = -1
	var next := at.clamp(ARENA.position, ARENA.end)
	if absf(next.x - swimmer.x) > 8.0:
		direction = 1.0 if next.x > swimmer.x else -1.0
	aim = next
	climbing = true
	velocity_y = 0.0


func _target(slot: int) -> Vector2:
	if mode == Mode.DUEL:
		return rival + Vector2(-37.0 if slot == 1 else 37.0, -95.0)
	if mode == Mode.CURRENT:
		return Vector2(1190.0 - fposmod(active_time * 91.0 + slot * 290.0, 1030.0),
			320.0 + 75.0 * sin(float(score + slot) * 2.1))
	return Vector2(680.0 + float(slot) * 220.0, 365.0 + float(slot) * 86.0)


func _process(delta: float) -> void:
	if mode == Mode.CELEBRATE:
		if pop_time > 0.0:
			pop_time = maxf(0.0, pop_time - delta)
			queue_redraw()
		return
	if mode != Mode.DUEL and mode != Mode.PRACTICE and mode != Mode.CURRENT:
		return
	elapsed += delta
	pop_time = maxf(0.0, pop_time - delta)
	if armed:
		var step := minf(delta, 1.0 / 30.0)
		_tick_swim(step)
	queue_redraw()


func _tick_swim(delta: float) -> void:
	active_time += delta
	var previous_rival := rival
	if mode == Mode.DUEL:
		# Marlo moves during a swim. Keep him low enough to read both tethers.
		rival.x = 820.0 + 105.0 * sin(active_time * 1.1)
		rival.y = 495.0 + 38.0 * sin(active_time * 1.7)
	var previous := swimmer
	if climbing:
		if assisted_slot >= 0:
			var target := _target(assisted_slot)
			aim = target if mode == Mode.CURRENT else target + Vector2(direction * FIN_X, -122)
		swimmer = swimmer.move_toward(aim, 440.0 * delta)
		if swimmer.is_equal_approx(aim) and touch_id < 0 and not mouse_held:
			climbing = false
	else:
		velocity_y = minf(325.0, velocity_y + (470.0 if player_bubbles > 0 else 690.0) * delta)
		swimmer.y += velocity_y * delta
		if assisted_slot >= 0 and mode != Mode.CURRENT:
			var landing_x := _target(assisted_slot).x + direction * FIN_X
			swimmer.x = move_toward(swimmer.x, landing_x, 190.0 * delta)
	if mode == Mode.CURRENT:
		for slot: int in range(rival_bubbles):
			if swimmer.distance_to(_target(slot)) < 37.0:
				_pop_target(slot)
				return
	elif swimmer.y > previous.y and not climbing and player_bubbles > 0:
		var fin := swimmer + Vector2(-direction * FIN_X, FIN_Y)
		var previous_fin_y := previous.y + FIN_Y
		for slot: int in range(rival_bubbles - 1, -1, -1):
			var target := _target(slot)
			var top := target.y - TARGET_RADIUS * 0.8
			if _target_is_visible(slot) and previous_fin_y <= top and fin.y >= top \
					and absf(fin.x - target.x) < TARGET_RADIUS + 16.0:
				_pop_target(slot)
				return
	if mode == Mode.DUEL and player_bubbles > 0 and rival.y > previous_rival.y:
		var tether := _player_bubble(player_bubbles - 1)
		if tether.distance_to(rival + Vector2(-34, 15)) < 35.0:
			player_bubbles -= 1
			_show_pop(tether)
			if player_bubbles == 0:
				climbing = false
				assisted_slot = -1
	if swimmer.y > ARENA.end.y:
		swimmer = Vector2(swimmer.x, START.y)
		player_bubbles = 2
		_reset_input()


func _target_is_visible(slot: int) -> bool:
	return mode != Mode.PRACTICE or pop_time <= 0.0 or pop_at != _target(slot)


func _pop_target(slot: int) -> void:
	_show_pop(_target(slot))
	score += 1
	assisted_slot = -1
	velocity_y = -155.0
	if mode == Mode.CURRENT:
		_reset_input()
		hint.text = "Pearls found  %d" % score
	elif mode == Mode.PRACTICE:
		_reset_input()
		hint.text = "Bubbles popped  %d" % score
	else:
		rival_bubbles -= 1
		if rival_bubbles == 0:
			_reset_input()
			mode = Mode.CELEBRATE
			hint.text = "You popped both bubbles!"
			main._say("roshan", "tutorial_power_pop")
			_card("Play again", bubble, Vector2(536, 229), _begin.bind(Mode.DUEL))


func _show_pop(at: Vector2) -> void:
	pop_at = at
	pop_time = 0.32
	main._audio_ref().pop(1)


func _player_bubble(slot: int) -> Vector2:
	return swimmer + Vector2(-34.0 if slot == 1 else 34.0, -103.0)


func _draw() -> void:
	draw_texture_rect(POOL, Rect2(Vector2.ZERO, size), false)
	draw_rect(Rect2(Vector2.ZERO, size), Color(0.04, 0.18, 0.30, 0.25))
	if mode == Mode.HUB or mode == Mode.SHOP:
		return
	if mode == Mode.DUEL or mode == Mode.CELEBRATE:
		for slot: int in range(rival_bubbles):
			_draw_bubble(_target(slot), rival, COLORS[2])
		_draw_cell(OTTER, int(active_time * 4.0) % 4, 2, rival, 170.0)
	else:
		for slot: int in range(rival_bubbles):
			if mode == Mode.CURRENT:
				draw_texture_rect(PEARL, Rect2(_target(slot) - Vector2(35, 35), Vector2(70, 70)), false)
			elif _target_is_visible(slot):
				draw_texture_rect(bubble, Rect2(_target(slot) - Vector2(34, 34), Vector2(68, 68)), false, COLORS[2])
	for slot: int in range(player_bubbles):
		_draw_bubble(_player_bubble(slot), swimmer, COLORS[tint_index])
	var body := Rect2(-Vector2.ONE * PLAYER_SIZE * 0.5, Vector2.ONE * PLAYER_SIZE)
	draw_set_transform(swimmer, 0.0, Vector2(direction, 1.0))
	if climbing:
		var frame := int(active_time * 15.0) % 16
		draw_texture_rect_region(SWIM, body, _cell(frame, 4))
	else:
		draw_texture_rect(ROSHAN, body, false)
	draw_set_transform(Vector2.ZERO)
	if pop_time > 0.0:
		_draw_cell(POP, mini(7, int((0.32 - pop_time) * 25.0)), 4, pop_at, 112.0)
	if score == 0 and not armed:
		var guide := _target(0) + Vector2(-36, -99 + sin(elapsed * 5.0) * 7.0)
		draw_texture_rect(HAND, Rect2(guide, Vector2(76, 76)), false)


func _draw_bubble(at: Vector2, waist: Vector2, tint: Color) -> void:
	draw_line(at + Vector2(0, 26), waist, Color(0.22, 0.39, 0.26), 3.0, true)
	draw_texture_rect(bubble, Rect2(at - Vector2(34, 34), Vector2(68, 68)), false, tint)


func _draw_cell(atlas: Texture2D, frame: int, columns: int, center: Vector2,
		length: float) -> void:
	var span := Vector2.ONE * length
	draw_texture_rect_region(atlas, Rect2(center - span * 0.5, span), _cell(frame, columns))


func _cell(frame: int, columns: int) -> Rect2:
	return Rect2((frame % columns) * 256, floori(float(frame) / float(columns)) * 256, 256, 256)
