extends Control
## Optional Opera practice game. All swim and color state belongs to this overlay.

signal close_requested

const ROUTE_ID := "opera_bubble_duel"
const POOL := preload("res://assets/flats/castle/interactions_v4/backgrounds/room_mermaid_pool_background.png")
const BUBBLES := preload("res://assets/opera/bubble_duel_v2/bubble.png")
const BUBBLE_REGION := Rect2(0, 0, 256, 256)
const ITEMS := preload("res://assets/opera/bubble_duel_v2/items.png")
const Shop := preload("res://scripts/bubble_duel_inventory.gd")
const ROSHAN := preload("res://assets/characters/roshan_25d/roshan_base.png")
const SWIM := preload("res://assets/characters/roshan_25d/roshan_swim_front.png")
const OTTER := preload("res://assets/opera/bubble_duel_v2/marlo_swim.png")
const PEARL := preload("res://assets/opera/worlds/teacher/pearl_uncounted.png")
const POP := preload("res://assets/sprites/fx_water/fx_water_bubble_burst_atlas.png")
const HAND := preload("res://assets/castle/training/ghost_hand.png")
const START := Vector2(350, 380)
const ARENA := Rect2(116, 208, 1048, 390)
const PLAYER_SIZE := 154.0
const FIN_Y := 49.0
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
var rival_survivor_side := 0
var player_bubbles := 2
var score := 0
var tint_index := 0
var pop_time := 0.0
var pop_at := Vector2.ZERO
var shop_page := 0
var gear := "classic"
var base_art: Texture2D = ROSHAN
var swim_art: Texture2D = SWIM
var power_button: Button
var wallet: Label
var glow := 100.0
var power_time := 0.0
var rival_offset := Vector2.ZERO
var projectiles: Array[Dictionary] = []
var pickup_cooldowns: Array[float] = [0.0, 0.0]
var return_cooldown := 0.0
var round_rewarded := false
var item_icons: Array[AtlasTexture] = []
var portraits: Dictionary = {}
var title_style: StyleBoxFlat
var glow_bar: ProgressBar
var rival_time := 0.0
var rival_glow := 100.0
var rival_pull_target := Vector2.ZERO


func setup(owner_main: ReefMain) -> void:
	main = owner_main
	name = "OperaBubbleDuel"
	size = StorybookUI.CANVAS_SIZE
	tint_index = Shop.color(main)
	gear = Shop.equipped(main)
	_bind_outfit()
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 70
	add_to_group(LivingWorldDirector.QUIET_GROUP)
	for index: int in range(8):
		var icon := AtlasTexture.new()
		icon.atlas = ITEMS
		icon.region = Rect2((index % 4) * 256, (index / 4) * 256, 256, 256)
		icon.filter_clip = true
		item_icons.append(icon)
	title_style = _title_panel()
	bubble = AtlasTexture.new()
	bubble.atlas = BUBBLES
	bubble.region = BUBBLE_REGION
	bubble.filter_clip = true
	heading = _label(Vector2(150, 32), 46)
	hint = _label(Vector2(150, 94), 27)
	wallet = _label(Vector2(940, 138), 27)
	wallet.size = Vector2(270, 42)
	wallet.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	power_button = Button.new()
	power_button.position = Vector2(18, 556)
	power_button.size = Vector2(124, 124)
	StorybookUI.style_picture_button(power_button)
	power_button.pressed.connect(_activate_power)
	power_button.hide()
	add_child(power_button)
	glow_bar = ProgressBar.new()
	glow_bar.position = Vector2(19, 686)
	glow_bar.size = Vector2(122, 16)
	glow_bar.show_percentage = false
	var glow_fill := StyleBoxFlat.new()
	glow_fill.bg_color = Color(0.45, 0.95, 0.80)
	glow_fill.set_corner_radius_all(7)
	glow_bar.add_theme_stylebox_override("fill", glow_fill)
	var glow_back := StyleBoxFlat.new()
	glow_back.bg_color = Color(0.12, 0.16, 0.30)
	glow_back.set_corner_radius_all(7)
	glow_bar.add_theme_stylebox_override("background", glow_back)
	glow_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	glow_bar.hide()
	add_child(glow_bar)
	menu = Control.new()
	menu.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(menu)
	_show_hub()


func _ready() -> void:
	_fit_view()
	get_viewport().size_changed.connect(_fit_view)


func _label(at: Vector2, font_size: int) -> Label:
	var label := Label.new()
	label.position = at
	label.size = Vector2(980, 58)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_hud_label(label, font_size)
	label.add_theme_color_override("font_color", Color(1.0, 0.98, 0.90))
	label.add_theme_color_override("font_outline_color", Color(0.12, 0.10, 0.30))
	label.add_theme_constant_override("outline_size", 4)
	add_child(label)
	return label


func _clear_menu() -> void:
	for child: Node in menu.get_children():
		menu.remove_child(child)
		child.queue_free()


func _card(title: String, art: Texture2D, at: Vector2, action: Callable,
		tint: Color = Color.WHITE, dimensions: Vector2 = Vector2(208, 176)) -> Button:
	var button := Button.new()
	button.position = at
	button.size = dimensions
	button.tooltip_text = title
	StorybookUI.style_picture_button(button)
	button.pressed.connect(action)
	menu.add_child(button)
	var picture := TextureRect.new()
	var multiline := title.contains("\n")
	var picture_size := minf(dimensions.x - 40, dimensions.y - (104 if multiline else 66))
	picture.position = Vector2((dimensions.x - picture_size) * 0.5, 8)
	picture.size = Vector2.ONE * picture_size
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	picture.texture = art
	picture.modulate = tint
	button.add_child(picture)
	var caption := Label.new()
	caption.text = title
	caption.position = Vector2(6, dimensions.y - (92 if multiline else 62))
	caption.size = Vector2(dimensions.x - 12, 88 if multiline else 58)
	caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	caption.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(caption, 20)
	button.add_child(caption)
	return button


func _show_hub() -> void:
	_reset_input()
	_clear_menu()
	mode = Mode.HUB
	heading.text = "Bubble Duel"
	hint.text = "Choose a place to play"
	power_button.hide()
	glow_bar.hide()
	_update_wallet()
	var otter := AtlasTexture.new()
	otter.atlas = OTTER
	otter.region = Rect2(0, 0, 256, 256)
	_card("Bubble Duel", otter, Vector2(194, 278), _begin.bind(Mode.DUEL))
	_card("Practice Lagoon", bubble, Vector2(422, 278), _begin.bind(Mode.PRACTICE))
	_card("Current Ride", PEARL, Vector2(650, 278), _begin.bind(Mode.CURRENT))
	_card("Shell Shop", _icon(1), Vector2(878, 278), _show_shop)
	queue_redraw()


func _show_shop() -> void:
	_reset_input()
	_clear_menu()
	mode = Mode.SHOP
	power_button.hide()
	glow_bar.hide()
	heading.text = "Pearl & Shell Shop"
	hint.text = "Choose your bubbles or a magical outfit"
	var data := Shop.state(main)
	for index: int in range(COLORS.size()):
		var owned: bool = index in data["colors"]
		var color_name: String = ["Aqua", "Rose", "Gold", "Mint", "Lilac"][index]
		var price: String = "✓" if tint_index == index else ("Owned" if owned else str(Shop.COLOR_PRICES[index]) + " pearls")
		_card(color_name + "  " + price, bubble, Vector2(164 + index * 194, 190),
			_select_color.bind(index), COLORS[index], Vector2(178, 150))
	var title := Label.new()
	title.position = Vector2(182, 356)
	title.size = Vector2(900, 46)
	title.text = "Power outfits"
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_hud_label(title, 29)
	title.add_theme_color_override("font_color", Color(1.0, 0.98, 0.90))
	title.add_theme_color_override("font_outline_color", Color(0.12, 0.10, 0.30))
	title.add_theme_constant_override("outline_size", 4)
	menu.add_child(title)
	for slot: int in range(4):
		var index := shop_page * 4 + slot
		var item: Dictionary = Shop.ITEMS[index]
		var id := String(item["id"])
		var equipped: bool = id == gear
		var price: String = "Wearing" if equipped else ("Owned" if id in data["owned"] else str(item["price"]) + " pearls")
		var portrait := _outfit_texture(ROSHAN.resource_path, id)
		var card := _card(String(item["name"]) + "\n" + price, portrait,
			Vector2(160 + slot * 226, 410), _choose_gear.bind(id), Color.WHITE, Vector2(210, 226))
		card.set_meta("gear_id", id)
		if int(item["icon"]) >= 0:
			var prop := TextureRect.new()
			prop.position = Vector2(142, 78)
			prop.size = Vector2(62, 62)
			prop.texture = _icon(int(item["icon"]))
			prop.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			prop.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			prop.mouse_filter = Control.MOUSE_FILTER_IGNORE
			card.add_child(prop)
	var next := Button.new()
	next.position = Vector2(1092, 451)
	next.size = Vector2(118, 118)
	StorybookUI.style_navigation_button(next, "→" if shop_page == 0 else "←", "More outfits")
	next.pressed.connect(_turn_shop_page)
	menu.add_child(next)
	_update_wallet()
	queue_redraw()


func _select_color(index: int) -> void:
	var bought := Shop.choose_color(main, index)
	if bought:
		tint_index = Shop.color(main)
	_show_shop()
	hint.text = "Your bubbles are ready!" if bought else "Keep finding pearls for this color"


func _begin(next: Mode) -> void:
	_reset_input()
	_clear_menu()
	mode = next
	swimmer = START
	direction = 1.0
	rival = Vector2(856, 515)
	rival_bubbles = 2
	rival_survivor_side = 0
	player_bubbles = 2
	score = 0
	elapsed = 0.0
	active_time = 0.0
	pop_time = 0.0
	heading.text = "Current Ride" if mode == Mode.CURRENT else (
		"Practice Lagoon" if mode == Mode.PRACTICE else "Bubble Duel")
	hint.text = "Touch a pearl to swim to it" if mode == Mode.CURRENT else (
		"Touch a glowing bubble to kick up and pop it")
	glow = 100.0
	power_time = 0.0
	rival_offset = Vector2.ZERO
	rival_pull_target = Vector2.ZERO
	rival_time = 0.0
	rival_glow = 100.0
	projectiles.clear()
	pickup_cooldowns = [0.0, 0.0]
	return_cooldown = 0.0
	round_rewarded = false
	power_button.visible = gear != "classic" and (mode == Mode.DUEL or gear not in ["kelp", "lullaby", "squid"])
	glow_bar.visible = power_button.visible
	_refresh_power()
	main._say("roshan", "idle2")
	_update_wallet()
	queue_redraw()


func go_back() -> void:
	if mode == Mode.HUB:
		close_requested.emit()
	else:
		main.clear_dialogue()
		_show_hub()
		# The global Back controller pops the route before invoking this callback.
		main._navigation_push(ROUTE_ID, self, go_back)


func shutdown() -> void:
	projectiles.clear()
	power_time = 0.0
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
		projectiles.clear()
		power_time = 0.0


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
			else:
				_assist_released_drag()
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
			else:
				_assist_released_drag()
		accept_event()
	elif event is InputEventMouseMotion and mouse_held \
			and event.position.distance_to(press_at) > 18.0:
		_steer(event.position)
		accept_event()


func _kick(at: Vector2) -> void:
	if player_bubbles == 0 or return_cooldown > 0.0:
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


func _assist_released_drag() -> void:
	if not armed or not climbing or assisted_slot >= 0 or mode == Mode.CURRENT:
		return
	if aim.distance_to(press_at) <= 18.0:
		return
	var projected_fin_x := aim.x - direction * FIN_X
	var closest := 54.0
	for slot: int in range(rival_bubbles):
		var target := _target(slot)
		var offset := absf(projected_fin_x - target.x)
		if _target_is_visible(slot) and aim.y <= target.y - 87.0 and offset < closest:
			closest = offset
			assisted_slot = slot


func _target(slot: int) -> Vector2:
	if mode == Mode.DUEL:
		var side := rival_survivor_side if rival_bubbles == 1 else slot
		return rival + Vector2(-37.0 if side == 1 else 37.0, -95.0)
	if mode == Mode.CURRENT:
		return Vector2(1190.0 - fposmod(active_time * 91.0 + slot * 290.0, 1030.0),
			320.0 + 75.0 * sin(active_time * 0.7 + float(slot) * 2.1))
	return Vector2(680.0 + float(slot) * 220.0, 365.0 + float(slot) * 86.0)


func _process(delta: float) -> void:
	if mode in [Mode.HUB, Mode.SHOP]:
		return
	elapsed += delta
	pop_time = maxf(0.0, pop_time - delta)
	return_cooldown = maxf(0.0, return_cooldown - delta)
	for slot: int in range(pickup_cooldowns.size()):
		pickup_cooldowns[slot] = maxf(0.0, pickup_cooldowns[slot] - delta)
	var remaining := minf(delta, 0.1)
	while (armed or not projectiles.is_empty()) and mode != Mode.CELEBRATE and remaining > 0.00001:
		var step := minf(remaining, 1.0 / 60.0)
		if armed:
			_tick_swim(step)
		else:
			_tick_projectiles(step)
		remaining -= step
	_refresh_power()
	queue_redraw()


func _tick_swim(delta: float) -> void:
	active_time += delta
	if player_bubbles > 0:
		glow = minf(100.0, glow + 22.0 * delta)
	rival_glow = minf(100.0, rival_glow + 22.0 * delta)
	power_time = maxf(0.0, power_time - delta)
	_tick_projectiles(delta)
	var previous_rival := rival
	if mode == Mode.DUEL:
		# Marlo moves during a swim. Keep him low enough to read both tethers.
		var pace := 0.35 if gear == "lullaby" and power_time > 0.0 else 1.0
		var pull := rival_pull_target if gear == "kelp" and power_time > 0.0 else Vector2.ZERO
		rival_offset = rival_offset.move_toward(pull, delta * 240.0)
		if not (gear == "squid" and power_time > 0.0):
			rival_time += delta * pace
			var phase := rival_time
			rival = Vector2(856.0 + 105.0 * sin(phase * 1.1),
				515.0 + 38.0 * sin(phase * 1.7)) + rival_offset
	var previous := swimmer
	if climbing:
		if assisted_slot >= 0:
			var target := _target(assisted_slot)
			aim = target if mode == Mode.CURRENT else target + Vector2(direction * FIN_X, -122)
		var swim_speed := 1000.0 if gear == "swiftconch" and power_time > 0.0 else 550.0
		swimmer = swimmer.move_toward(aim, swim_speed * delta)
		if swimmer.is_equal_approx(aim) and touch_id < 0 and not mouse_held:
			climbing = false
	else:
		var gravity := 560.0 if player_bubbles > 0 else 780.0
		if gear == "moonpearl" and power_time > 0.0 and glow > 0.0:
			gravity = 0.0
			velocity_y = move_toward(velocity_y, 0.0, 1100.0 * delta)
			glow = maxf(0.0, glow - 60.0 * delta)
		if gear == "tidewing" and velocity_y > 170.0 and power_time <= 0.0 and player_bubbles > 0 and assisted_slot < 0 and swimmer.y > 500.0:
			velocity_y = -90.0
			power_time = 0.7
		velocity_y = minf(365.0, velocity_y + gravity * delta)
		swimmer.y += velocity_y * delta
		if assisted_slot >= 0 and mode != Mode.CURRENT:
			var landing_x := _target(assisted_slot).x + direction * FIN_X
			swimmer.x = move_toward(swimmer.x, landing_x, 165.0 * delta)
	if mode == Mode.CURRENT:
		for slot: int in range(rival_bubbles):
			if _target_is_visible(slot) and swimmer.distance_to(_target(slot)) < 37.0:
				_pop_target(slot)
				return
	elif swimmer.y > previous.y and not climbing and player_bubbles > 0:
		var fin := swimmer + Vector2(-direction * FIN_X, FIN_Y)
		var previous_fin_y := previous.y + FIN_Y
		for slot: int in range(rival_bubbles - 1, -1, -1):
			var target := _target(slot)
			var old_target := target
			if mode == Mode.DUEL:
				old_target += previous_rival - rival
			var relative_from := Vector2(fin.x - (swimmer.x - previous.x), previous_fin_y) - old_target
			var relative_to := fin - target
			if not _target_is_visible(slot) or relative_from.y >= 0.0 or relative_to.y <= relative_from.y:
				continue
			var nearest := Geometry2D.get_closest_point_to_segment(Vector2.ZERO, relative_from, relative_to)
			if nearest.length_squared() <= TARGET_RADIUS * TARGET_RADIUS:
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
		return_cooldown = 0.6
		player_bubbles = 2
		_reset_input()


func _target_is_visible(slot: int) -> bool:
	if mode in [Mode.PRACTICE, Mode.CURRENT]:
		return pickup_cooldowns[slot] <= 0.0
	return true


func _pop_target(slot: int) -> void:
	if not _target_is_visible(slot):
		return
	_show_pop(_target(slot))
	score += 1
	assisted_slot = -1
	velocity_y = -150.0
	if mode in [Mode.CURRENT, Mode.PRACTICE]:
		pickup_cooldowns[slot] = 0.9
		Shop.reward(main, 1)
		_reset_input()
		hint.text = ("Pearls found  " if mode == Mode.CURRENT else "Bubbles popped  ") + str(score)
	else:
		rival_bubbles -= 1
		if rival_bubbles == 1:
			rival_survivor_side = 1 - slot
		if rival_bubbles == 0:
			_reset_input()
			mode = Mode.CELEBRATE
			if not round_rewarded:
				round_rewarded = true
				var data := Shop.state(main)
				var wins := int(data.get("wins", 0))
				var prize := mini(60, 10 + wins / 2)
				Shop.reward(main, prize, true)
				hint.text = "Both bubbles popped!  +" + str(prize) + " pearls"
			main._say("roshan", "tutorial_power_pop")
			power_button.hide()
			glow_bar.hide()
			var replay := Button.new()
			replay.position = Vector2(552, 230)
			StorybookUI.style_navigation_button(replay, "↻", "Play again")
			replay.size = Vector2(176, 176)
			replay.add_theme_font_size_override("font_size", 72)
			replay.pressed.connect(_begin.bind(Mode.DUEL))
			menu.add_child(replay)
	_update_wallet()


func _show_pop(at: Vector2) -> void:
	pop_at = at
	pop_time = 0.32
	main._audio_ref().pop(1)


func _player_bubble(slot: int) -> Vector2:
	return swimmer + Vector2(-34.0 if slot == 1 else 34.0, -103.0)


func _draw() -> void:
	var view := get_viewport_rect().size
	var offset := position / scale.x
	var canvas := Rect2(-offset, view / scale.x)
	var native := POOL.get_size()
	var aspect := canvas.size.x / canvas.size.y
	var source := Rect2(Vector2.ZERO, native)
	if aspect >= native.x / native.y:
		var crop_height := native.x / aspect
		source = Rect2(0, (native.y - crop_height) * 0.5, native.x, crop_height)
	else:
		var crop_width := native.y * aspect
		source = Rect2((native.x - crop_width) * 0.5, 0, crop_width, native.y)
	draw_texture_rect_region(POOL, canvas, source)
	draw_rect(canvas, Color(0.05, 0.20, 0.30, 0.11))
	draw_style_box(title_style, Rect2(170, 12, 940, 125))
	if mode in [Mode.HUB, Mode.SHOP]:
		return
	if mode in [Mode.DUEL, Mode.CELEBRATE]:
		for slot: int in range(rival_bubbles):
			_draw_bubble(_target(slot), rival, Color(1.0, 0.74, 0.53))
		_draw_cell(OTTER, int(active_time * 5.0) % 4, 2, rival, 185.0)
	else:
		for slot: int in range(rival_bubbles):
			if not _target_is_visible(slot):
				continue
			if mode == Mode.CURRENT:
				draw_texture_rect(PEARL, Rect2(_target(slot) - Vector2(35, 35), Vector2(70, 70)), false)
			else:
				draw_texture_rect(bubble, Rect2(_target(slot) - Vector2(34, 34), Vector2(68, 68)), false, Color(1.0, 0.80, 0.55))
	for slot: int in range(player_bubbles):
		_draw_bubble(_player_bubble(slot), swimmer, COLORS[tint_index])
	var frame := int(active_time * 15.0) % 16
	var shift := Vector2.ZERO
	if climbing:
		shift = (Vector2(128, 128) - RoshanSpriteAnchors.anchor("swim_front", frame)) * PLAYER_SIZE / 256.0
	draw_set_transform(swimmer, 0.0, Vector2(direction, 1.0))
	var body := Rect2(-Vector2.ONE * PLAYER_SIZE * 0.5 + shift, Vector2.ONE * PLAYER_SIZE)
	if climbing:
		draw_texture_rect_region(swim_art, body, _cell(frame, 4))
	else:
		draw_texture_rect(base_art, body, false)
	draw_set_transform(Vector2.ZERO)
	for shot: Dictionary in projectiles:
		draw_texture_rect(_icon(3), Rect2((shot["position"] as Vector2) - Vector2(26, 26), Vector2(52, 52)), false)
	if mode == Mode.DUEL and power_time > 0.0 and gear in ["kelp", "lullaby", "squid"]:
		var accent := _icon(int(Shop.item(gear)["icon"]))
		draw_texture_rect(accent, Rect2(rival + Vector2(-45, -155), Vector2(90, 90)), false, Color(1, 1, 1, 0.75))
	if pop_time > 0.0:
		var progress := (0.32 - pop_time) / 0.32
		var span := 84.0 + progress * 55.0
		var tint := Color(1, 1, 1, 1.0 - progress)
		draw_texture_rect(_icon(7), Rect2(pop_at - Vector2.ONE * span * 0.5, Vector2.ONE * span), false, tint)
		_draw_cell(POP, mini(7, int((0.32 - pop_time) * 25.0)), 4, pop_at, 155.0)
	if score == 0 and not armed and mode != Mode.CELEBRATE:
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
func _fit_view() -> void:
	var view := get_viewport_rect().size
	var factor := minf(view.x / 1280.0, view.y / 720.0)
	scale = Vector2.ONE * factor
	position = (view - size * factor) * 0.5


func _title_panel() -> StyleBoxFlat:
	var panel := StyleBoxFlat.new()
	panel.bg_color = Color(0.10, 0.16, 0.32, 0.75)
	panel.set_corner_radius_all(24)
	return panel


func _icon(index: int) -> Texture2D:
	return item_icons[index]


func _outfit_texture(source: String, id: String) -> Texture2D:
	if source == ROSHAN.resource_path and portraits.has(id):
		return portraits[id] as Texture2D
	var outfit := String(Shop.item(id)["outfit"])
	if outfit in ["star", "blossom", "winter", "magician"]:
		var spec := FashionSkinEngine.family(source)
		var parts := {"head": "head_" + outfit + "_v1", "body": "body_" + outfit + "_v1", "tail": "tail_original"}
		var path := FashionParts.composed_path(main, spec, source, "", parts)
		var art := load(path) as Texture2D
		if source == ROSHAN.resource_path:
			portraits[id] = art
		return art
	var art := load(FashionOutfitRenderer.path(main, source, outfit)) as Texture2D
	if source == ROSHAN.resource_path:
		portraits[id] = art
	return art


func _bind_outfit() -> void:
	base_art = _outfit_texture(ROSHAN.resource_path, gear)
	swim_art = _outfit_texture(SWIM.resource_path, gear)


func _choose_gear(id: String) -> void:
	var bought := Shop.choose_item(main, id)
	if bought:
		gear = Shop.equipped(main)
		_bind_outfit()
	_show_shop()
	hint.text = String(Shop.item(id)["help"]) if bought else "Find more pearls for this outfit"
	if bought:
		main._say("roshan", "win")
	else:
		main._say("roshan", "craft_need_pearls")


func _turn_shop_page() -> void:
	shop_page = 1 - shop_page
	_show_shop()


func _update_wallet() -> void:
	if wallet != null:
		wallet.text = str(Shop.state(main)["pearls"]) + " pearls"


func _refresh_power() -> void:
	glow_bar.value = glow
	var entry := Shop.item(gear)
	power_button.disabled = gear in ["classic", "tidewing"] or glow < float(entry["use"]) \
		or (gear == "rainbow" and not projectiles.is_empty())
	power_button.icon = _icon(int(entry["icon"])) if int(entry["icon"]) >= 0 else null
	power_button.expand_icon = true
	power_button.add_theme_constant_override("icon_max_width", 90)
	power_button.tooltip_text = String(entry["help"])
	power_button.modulate.a = 1.0 if not power_button.disabled else 0.55


func _activate_power() -> void:
	if mode not in [Mode.DUEL, Mode.PRACTICE, Mode.CURRENT] or player_bubbles == 0:
		return
	if gear in ["kelp", "lullaby", "squid"] and mode != Mode.DUEL:
		return
	var entry := Shop.item(gear)
	if gear in ["classic", "tidewing"] or glow < float(entry["use"]) \
			or (gear == "rainbow" and not projectiles.is_empty()):
		return
	main._say("roshan", "op_magician_work")
	glow -= float(entry["use"])
	armed = true
	power_time = 1.0
	match gear:
		"moonpearl":
			power_time = 1.5
		"swiftconch":
			power_time = 0.45
			aim.x = clampf(swimmer.x + direction * 220.0, ARENA.position.x, ARENA.end.x)
			aim.y = maxf(ARENA.position.y, swimmer.y - 30.0)
			climbing = true
		"rainbow":
			projectiles.append({"position": swimmer + Vector2(direction * 30, -30), "life": 2.5})
		"kelp":
			rival_pull_target = (swimmer - rival).normalized() * 90.0
			power_time = 1.2
		"lullaby":
			rival_glow = 0.0
			power_time = 2.0
		"squid":
			power_time = 1.33
	_refresh_power()
	queue_redraw()


func _tick_projectiles(delta: float) -> void:
	for index: int in range(projectiles.size() - 1, -1, -1):
		var shot: Dictionary = projectiles[index]
		shot["life"] = float(shot["life"]) - delta
		var from: Vector2 = shot["position"]
		var goal := _target(0)
		var next := from.move_toward(goal, 540.0 * delta)
		shot["position"] = next
		var nearest := Geometry2D.get_closest_point_to_segment(goal, from, next)
		if _target_is_visible(0) and nearest.distance_to(goal) <= TARGET_RADIUS:
			projectiles.remove_at(index)
			_pop_target(0)
		elif float(shot["life"]) <= 0.0:
			projectiles.remove_at(index)
