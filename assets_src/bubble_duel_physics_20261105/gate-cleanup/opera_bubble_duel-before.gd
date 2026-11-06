class_name BubbleDuelOverlay
extends Control
## Elevator reef arcade. Shared fixed-step motion for solo, cooperative and versus play.

signal close_requested

const ROUTE_ID := "opera_bubble_duel"
const POOL := preload("res://assets/flats/castle/interactions_v4/backgrounds/room_mermaid_pool_background.png")
const BUBBLES := preload("res://assets/opera/bubble_duel_v2/bubble.png")
const BUBBLE_REGION := Rect2(0, 0, 256, 256)
const ITEMS := preload("res://assets/opera/bubble_duel_v2/items.png")
const Shop := preload("res://scripts/bubble_duel_inventory.gd")
const ROSHAN := preload("res://assets/characters/roshan_25d/roshan_base.png")
const PEARL := preload("res://assets/opera/worlds/teacher/pearl_uncounted.png")
const POP := preload("res://assets/sprites/fx_water/fx_water_bubble_burst_atlas.png")
const HAND := preload("res://assets/castle/training/ghost_hand.png")
const COLORS: Array[Color] = [
	Color(0.70, 0.95, 1.0), Color(1.0, 0.74, 0.86), Color(1.0, 0.91, 0.64),
	Color(0.74, 1.0, 0.81), Color(0.85, 0.76, 1.0),
]

enum Mode { HUB, DUEL, PRACTICE, CURRENT, SHOP, CELEBRATE, SETUP, PICKER, VERSUS }

const Cast := preload("res://scripts/bubble_duel_cast.gd")
const Duo := preload("res://scripts/bubble_duel_two_player.gd")
const Preview := preload("res://scripts/bubble_duel_preview.gd")

var appearance: BubbleDuelCast
var duo: BubbleDuelTwoPlayer
var world := BubbleDuelArena.new()
var geometry: BubbleDuelGeometry
var board: BubbleDuelView
var fixed_time: float = 0.0
var cooperative: bool = false
var campaign_stage: int = 0
var bonus_items: Array[Dictionary] = []
var bonus_rng := RandomNumberGenerator.new()
var fighters: Array[BubbleDuelFighter]:
	get: return world.fighters
var duo_touch_owners: Dictionary = {}
var duo_keys: Dictionary = {}
var duo_pops: Array[Dictionary] = []
var power_effects: Array[Dictionary] = []
var duo_guides: Array[TextureRect] = []
var local_two_player := false
var setup_two_player := false
var selected_player := 0
var picker_kind := "character"
var picker_page := 0
var shop_player := 0
var shop_from_setup := false
var second_power_button: Button
var second_glow_bar: ProgressBar
var main: ReefMain
var mode := Mode.HUB
var menu: Control
var status_label: Label
var heading: Label
var hint: Label
var bubble: AtlasTexture
var elapsed := 0.0
var active_time := 0.0
var score := 0
var tint_index := 0
var shop_page := 0
var gear := "classic"
var power_button: Button
var wallet: Label
var round_rewarded := false
var item_icons: Array[AtlasTexture] = []
var title_style: StyleBoxFlat
var glow_bar: ProgressBar


func setup(owner_main: ReefMain) -> void:
	main = owner_main
	for index: int in range(12):
		power_effects.append({"life": 0.0, "actor": 0, "target": -1, "gear": "classic"})
	appearance = Cast.new(main)
	geometry = BubbleDuelGeometry.new(appearance)
	board = BubbleDuelView.new()
	board.host = self
	board.position = Vector2(220, 0)
	board.size = Vector2(840, 720)
	board.clip_contents = true
	board.mouse_filter = Control.MOUSE_FILTER_IGNORE
	board.hide()
	add_child(board)
	duo = Duo.new(self)
	name = "OperaBubbleDuel"
	size = StorybookUI.CANVAS_SIZE
	tint_index = Shop.color(main)
	gear = Shop.equipped(main)
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
	power_button.position = Vector2(48, 292)
	power_button.size = Vector2(124, 124)
	StorybookUI.style_picture_button(power_button)
	power_button.button_down.connect(_activate_power)
	power_button.button_up.connect(func() -> void: world.queue_power(0, false, false))
	power_button.hide()
	add_child(power_button)
	glow_bar = ProgressBar.new()
	glow_bar.position = Vector2(49, 424)
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
	second_power_button = Button.new()
	second_power_button.position = Vector2(1108, 292)
	second_power_button.size = Vector2(124, 124)
	StorybookUI.style_picture_button(second_power_button)
	second_power_button.button_down.connect(func() -> void: duo.activate(1))
	second_power_button.button_up.connect(func() -> void: world.queue_power(1, false, false))
	second_power_button.hide()
	add_child(second_power_button)
	second_glow_bar = glow_bar.duplicate() as ProgressBar
	second_glow_bar.position.x = 1109
	second_glow_bar.hide()
	add_child(second_glow_bar)
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
	duo_guides.clear()
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
	local_two_player = false
	shop_player = 0
	shop_from_setup = false
	heading.text = "Bubble Duel"
	hint.text = "Choose a place to play"
	power_button.hide()
	glow_bar.hide()
	_update_wallet()
	var friend: Texture2D = appearance.texture(Shop.profile(main, 1), false)
	var duel_card := _card("Bubble Duel", friend, Vector2(194, 278), _show_setup.bind(false))
	(duel_card.get_child(0) as TextureRect).hide()
	_preview(duel_card, _solo_rival_profile(), Rect2(32, 3, 144, 112))
	_card("Practice Lagoon", bubble, Vector2(422, 278), _begin.bind(Mode.PRACTICE))
	_card("Current Ride", PEARL, Vector2(650, 278), _begin.bind(Mode.CURRENT))
	_card("Shell Shop", _icon(1), Vector2(878, 278), _show_shop)
	var two := _card("Two friends", ROSHAN, Vector2(490, 482), _show_setup.bind(true), Color.WHITE, Vector2(300, 165))
	(two.get_child(0) as TextureRect).hide()
	_preview(two, Shop.profile(main, 0), Rect2(17, 0, 118, 112))
	_preview(two, Shop.profile(main, 1), Rect2(164, 0, 118, 112), -1.0)
	queue_redraw()


func _show_shop() -> void:
	_reset_input()
	_clear_menu()
	mode = Mode.SHOP
	power_button.hide()
	glow_bar.hide()
	heading.text = "Pearl & Shell Shop"
	hint.text = "Player %d: choose bubbles and worn power items" % (shop_player + 1)
	var data := Shop.state(main)
	for index: int in range(COLORS.size()):
		var owned: bool = index in data["colors"]
		var color_name: String = ["Aqua", "Rose", "Gold", "Mint", "Lilac"][index]
		var price: String = "✓" if Shop.color(main, shop_player) == index else ("Owned" if owned else str(Shop.COLOR_PRICES[index]) + " pearls")
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
		var equipped: bool = id == Shop.equipped(main, shop_player)
		var price: String = "Wearing" if equipped else ("Owned" if id in data["owned"] else str(item["price"]) + " pearls")
		var portrait: Texture2D = ROSHAN
		var card := _card(String(item["name"]) + "\n" + price, portrait,
			Vector2(160 + slot * 226, 410), _choose_gear.bind(id), Color.WHITE, Vector2(210, 226))
		card.set_meta("gear_id", id)
		(card.get_child(0) as TextureRect).hide()
		var worn := Shop.profile(main, shop_player)
		worn["gear"] = id
		worn["look"] = "set:" + id
		_preview(card, worn, Rect2(16, 1, 172, 135))
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
	var bought := Shop.choose_color(main, index, shop_player)
	if bought:
		tint_index = Shop.color(main)
	_show_shop()
	hint.text = "Your bubbles are ready!" if bought else "Keep finding pearls for this color"


func _begin(next: Mode) -> void:
	local_two_player = false
	cooperative = false
	_start_bout(next)


func _start_bout(next: Mode) -> void:
	_reset_input()
	_clear_menu()
	mode = next
	heading.hide()
	hint.hide()
	elapsed = 0.0
	active_time = 0.0
	fixed_time = 0.0
	score = 0
	round_rewarded = false
	duo_pops.clear()
	for effect: Dictionary in power_effects: effect["life"] = 0.0
	bonus_items.clear()
	bonus_rng.seed = 1709 + int(Shop.state(main).get("wins", 0))
	var data: Dictionary = Shop.state(main)
	var campaign: Dictionary = Shop.campaign(main)
	campaign_stage = int(campaign["stage"])
	var environment: int = campaign_stage % 4 if next in [Mode.DUEL, Mode.VERSUS] else int(data.get("wins", 0)) % 4
	world.reset(environment, 4001 + campaign_stage * 193 + int(data.get("wins", 0)))
	world.prepare_geometry = geometry.apply
	if next != Mode.CURRENT: world.round_limit = 2700
	world.add_human(Shop.profile(main, 0), 0, 0, 4, next != Mode.VERSUS or cooperative)
	if local_two_player:
		world.add_human(Shop.profile(main, 1), 1, 0 if cooperative else 1, 4, cooperative)
	if next == Mode.DUEL or cooperative or next == Mode.PRACTICE:
		var enemies: int = 1 + mini(2, campaign_stage / 4) if next != Mode.PRACTICE else 3
		for index: int in range(enemies):
			var profile: Dictionary = _solo_rival_profile() if index == 0 else {
				"character": Cast.PEOPLE[(campaign_stage + index + 1) % Cast.PEOPLE.size()],
				"look": "set:classic", "color": (index + 2) % 5, "gear": "classic"}
			if campaign_stage >= 8 and next != Mode.PRACTICE:
				profile["gear"] = ["swiftconch", "rainbow", "kelp", "lullaby", "squid"][(campaign_stage + index) % 5]
			var level: int = 1 + campaign_stage * 5 + index * 6
			world.add_cpu(profile, minf(95, 25 + level * 0.65),
				minf(100, 30 + level * 0.65), level, 1, 1 if next != Mode.PRACTICE else 0)
		if next != Mode.PRACTICE:
			_restore_checkpoint(campaign)
	if next == Mode.CURRENT:
		var player: BubbleDuelFighter = world.human(0)
		player.position = Vector2(120, 150)
		player.previous = player.position
		player.velocity = Vector2.ZERO
		world.drift = 0.0
		for index: int in range(64):
			bonus_items.append({"active": false, "kind": "pearl", "position": Vector2.ZERO, "phase": 0.0})
	for fighter: BubbleDuelFighter in world.fighters:
		geometry.apply(fighter, 0)
		fighter.previous_fin = world._fin(fighter)
	board.show()
	_build_pads()
	_refresh_power()
	_update_wallet()
	main._say("roshan", "idle2")
	queue_redraw()


func _build_pads() -> void:
	for player: int in range(2 if local_two_player else 1):
		var pad := Button.new()
		pad.position = Duo.PADS[player].position
		pad.size = Duo.PADS[player].size
		pad.mouse_filter = Control.MOUSE_FILTER_IGNORE
		StorybookUI.style_picture_button(pad)
		pad.text = "←  ↑  →"
		pad.add_theme_font_size_override("font_size", 30)
		menu.add_child(pad)
		var guide := TextureRect.new()
		guide.texture = HAND
		guide.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		guide.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		guide.size = Vector2(62, 62)
		guide.position = Vector2(58, 58)
		guide.mouse_filter = Control.MOUSE_FILTER_IGNORE
		pad.add_child(guide)
		duo_guides.append(guide)
	status_label = _label(Vector2(4, 220), 24)
	status_label.name = "BoutStatus"
	status_label.size = Vector2(208, 64)
	status_label.text = "Reef %d / 16" % (campaign_stage + 1) if mode == Mode.DUEL or cooperative else ("Current Ride" if mode == Mode.CURRENT else "Tap to flap")
	remove_child(status_label)
	menu.add_child(status_label)


func resume_play() -> void:
	world.paused = false


func _restore_checkpoint(campaign: Dictionary) -> void:
	var checkpoint: Dictionary = campaign.get("checkpoint", {})
	if int(checkpoint.get("stage", -1)) != campaign_stage: return
	var enemies: Variant = checkpoint.get("enemies", [])
	if not enemies is Array: return
	var index: int = 0
	for fighter: BubbleDuelFighter in world.fighters:
		if fighter.human >= 0: continue
		if index < enemies.size() and enemies[index] is Dictionary:
			var saved: Dictionary = enemies[index]
			fighter.spares = clampi(int(saved.get("spares", fighter.spares)), 0, 4)
			fighter.bubbles = clampi(int(saved.get("bubbles", 2)), 0, 2)
			fighter.survivor_side = -1 if int(saved.get("side", 1)) < 0 else 1
			fighter.lost = bool(saved.get("lost", false))
			fighter.invincible = 50
		index += 1


func _checkpoint(pearls: int = 0, complete: bool = false) -> void:
	if mode == Mode.CURRENT:
		Shop.record_ride(main, score)
		return
	if mode not in [Mode.DUEL, Mode.VERSUS] or (mode == Mode.VERSUS and not cooperative): return
	var enemies: Array[Dictionary] = []
	for fighter: BubbleDuelFighter in world.fighters:
		if fighter.human < 0:
			enemies.append({"bubbles": fighter.bubbles, "spares": fighter.spares,
				"lost": fighter.lost, "side": fighter.survivor_side})
	Shop.checkpoint(main, campaign_stage, {"stage": campaign_stage, "enemies": enemies}, pearls, complete)



func go_back() -> void:
	_checkpoint()
	if mode == Mode.PICKER or (mode == Mode.SHOP and shop_from_setup):
		_show_setup(setup_two_player)
		main._navigation_push(ROUTE_ID, self, go_back)
	elif mode == Mode.HUB:
		close_requested.emit()
	else:
		main.clear_dialogue()
		_show_hub()
		# The global Back controller pops the route before invoking this callback.
		main._navigation_push(ROUTE_ID, self, go_back)


func shutdown() -> void:
	_checkpoint()
	remove_from_group(LivingWorldDirector.QUIET_GROUP)
	_reset_input()
	hide()
	set_process(false)
	main.clear_dialogue()


func _reset_input() -> void:
	if duo != null: duo.flush()
	if world != null: world.paused = true
	if second_power_button != null:
		second_power_button.hide()
		second_glow_bar.hide()
	if board != null: board.hide()
	if heading != null: heading.show()
	if hint != null: hint.show()



func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT or what == NOTIFICATION_APPLICATION_PAUSED or what == NOTIFICATION_PAUSED:
		if world != null:
			_checkpoint()
			if duo != null: duo.flush()
			world.paused = true
			fixed_time = 0.0



func _gui_input(event: InputEvent) -> void:
	if mode in [Mode.DUEL, Mode.PRACTICE, Mode.CURRENT, Mode.VERSUS] and duo.input(event):
		accept_event()



func _target(slot: int) -> Vector2:
	for fighter: BubbleDuelFighter in world.fighters:
		if fighter.human < 0 and not fighter.lost:
			return Vector2(220, 72) + world.bubble_position(fighter, -1 if slot == 0 else 1) * 2.1
	return Vector2.ZERO



func _process(delta: float) -> void:
	if mode not in [Mode.DUEL, Mode.PRACTICE, Mode.CURRENT, Mode.VERSUS, Mode.CELEBRATE]: return
	elapsed += delta
	if not world.paused:
		for effect: Dictionary in power_effects: effect["life"] = maxf(0.0, float(effect["life"]) - delta)
	for index: int in range(duo_pops.size() - 1, -1, -1):
		duo_pops[index]["time"] = float(duo_pops[index]["time"]) - delta
		if float(duo_pops[index]["time"]) <= 0.0: duo_pops.remove_at(index)
	if mode != Mode.CELEBRATE and not world.paused:
		# Bound catch-up after a suspended frame; do not turn a pause into a burst.
		fixed_time += minf(delta, 0.1)
		while fixed_time >= 1.0 / 30.0 and mode != Mode.CELEBRATE:
			world.step()
			if world.started:
				active_time += 1.0 / 30.0
				_consume_events()
				if mode == Mode.CURRENT: _tick_bonus()
				if world.finished: _finish_bout()
			fixed_time -= 1.0 / 30.0
	board.blend = clampf(fixed_time * 30.0, 0.0, 1.0)
	board.queue_redraw()
	if is_instance_valid(status_label):
		status_label.text = ("Reef %d / 16" % (campaign_stage + 1) if mode == Mode.DUEL or cooperative else ("Current Ride" if mode == Mode.CURRENT else ("Practice Lagoon" if mode == Mode.PRACTICE else "Bubble Duel"))) + "\n○  " + str(score)
	_refresh_power()
	queue_redraw()


func _consume_events() -> void:
	var reward: int = 0
	var changed: bool = false
	for index: int in range(world.event_count):
		var event: Dictionary = world.events[index]
		match String(event["kind"]):
			"pop":
				duo_pops.append({"position": event["position"], "time": 0.32})
				main._audio_ref().pop(1)
				var target: BubbleDuelFighter = world.fighters[int(event["actor"])]
				if target.human < 0:
					score += 1
					reward += 1
				changed = true
			"rescue":
				changed = true
			"power":
				var actor: BubbleDuelFighter = world.fighters[int(event["actor"])]
				var target: BubbleDuelFighter = BubbleDuelBrain.opponent(actor, world.fighters)
				for effect: Dictionary in power_effects:
					if float(effect["life"]) <= 0.0:
						effect["life"] = 1.0
						effect["actor"] = actor.slot
						effect["target"] = target.slot if target != null else -1
						effect["gear"] = actor.gear
						break
				main._audio_ref().pop(1)
			"bonk", "bump":
				main._audio_ref().pop(0)
	if changed:
		if mode == Mode.DUEL or cooperative: _checkpoint(reward)
		elif reward > 0 and mode == Mode.PRACTICE: Shop.reward(main, reward)


func _finish_bout() -> void:
	if round_rewarded: return
	round_rewarded = true
	var was: Mode = mode
	if was == Mode.CURRENT: Shop.record_ride(main, score)
	if was == Mode.DUEL or cooperative:
		_checkpoint(0 if world.timed_draw else 12 + campaign_stage * 2, not world.timed_draw)
	elif was == Mode.PRACTICE and not world.timed_draw:
		Shop.reward(main, 6, true)
	elif world.pops > 0:
		Shop.reward(main, 10, true)
	mode = Mode.CELEBRATE
	duo.flush()
	_clear_menu()
	power_button.hide()
	second_power_button.hide()
	glow_bar.hide()
	second_glow_bar.hide()
	heading.show()
	hint.show()
	heading.text = "Take a breath!" if world.timed_draw else "A shared splash!"
	hint.text = ("Progress saved · continue when ready" if world.timed_draw else "Next reef challenge!") if was == Mode.DUEL or cooperative else ("A friendly draw · play again" if world.timed_draw else "Play another round")
	main._say("roshan", "idle2" if world.timed_draw else "tutorial_power_pop")
	var replay := Button.new()
	replay.position = Vector2(552, 274)
	replay.size = Vector2(176, 176)
	StorybookUI.style_navigation_button(replay, "→" if was == Mode.DUEL or cooperative else "↻", "Next challenge")
	replay.add_theme_font_size_override("font_size", 72)
	if cooperative: replay.pressed.connect(_begin_coop)
	elif was == Mode.VERSUS: replay.pressed.connect(_begin_versus)
	else: replay.pressed.connect(_begin.bind(was))
	menu.add_child(replay)
	_update_wallet()


func _tick_bonus() -> void:
	var player: BubbleDuelFighter = world.human(0)
	player.position.x = clampf(player.position.x, 20, 380)
	var speed: float = minf(5, 2.0 + float(world.frame) / 1800.0)
	if world.frame % 25 == 0 and bonus_rng.randf() < 0.7:
		_bonus_spawn("pearl", Vector2(420, bonus_rng.randf_range(40, 250)))
	if world.frame % 70 == 0:
		var y: float = bonus_rng.randf_range(50, 250)
		for index: int in range(bonus_rng.randi_range(1, 3)):
			_bonus_spawn("ink", Vector2(420 + index * 22, y + sin(float(index)) * 8))
	var body := Rect2(player.position + player.body_box.position, player.body_box.size)
	for item: Dictionary in bonus_items:
		if not bool(item["active"]): continue
		var at: Vector2 = item["position"]
		at.x -= speed * (1.2 if item["kind"] == "ink" else 1.0)
		item["phase"] = float(item["phase"]) + 0.1
		if item["kind"] == "ink": at.y += sin(float(item["phase"])) * 0.6
		item["position"] = at
		if at.x < -30:
			item["active"] = false
			continue
		var hit: bool = body.intersects(Rect2(at - Vector2(9, 9), Vector2(18, 18)))
		for side: int in world.SIDES:
			if world._side_exists(player, side) and world.bubble_position(player, side).distance_to(at) < world.bubble_radius(player) + 9.0:
				hit = true
		if not hit: continue
		if item["kind"] == "pearl":
			score += 1
			Shop.reward(main, 1)
			main._audio_ref().pop(1)
			item["active"] = false
		elif player.invincible == 0:
			player.bubbles = maxi(0, player.bubbles - 1)
			player.invincible = 40
			if player.bubbles == 0: world.motion.rescue(player)
			item["active"] = false
	if active_time >= 90.0:
		world.finished = true
		world.winner = 0


func _bonus_spawn(kind: String, at: Vector2) -> void:
	for item: Dictionary in bonus_items:
		if not bool(item["active"]):
			item["kind"] = kind
			item["position"] = at
			item["phase"] = bonus_rng.randf_range(0, 6)
			item["active"] = true
			return



func _draw() -> void:
	var view: Vector2 = get_viewport_rect().size
	var offset: Vector2 = position / scale.x
	var canvas := Rect2(-offset, view / scale.x)
	var native: Vector2 = POOL.get_size()
	var aspect: float = canvas.size.x / canvas.size.y
	var source := Rect2(Vector2.ZERO, native)
	if aspect >= native.x / native.y:
		var crop_height: float = native.x / aspect
		source = Rect2(0, (native.y - crop_height) * 0.5, native.x, crop_height)
	else:
		var crop_width: float = native.y * aspect
		source = Rect2((native.x - crop_width) * 0.5, 0, crop_width, native.y)
	draw_texture_rect_region(POOL, canvas, source)
	draw_rect(canvas, Color(0.05, 0.20, 0.30, 0.11))
	if mode in [Mode.HUB, Mode.SHOP, Mode.SETUP, Mode.PICKER, Mode.CELEBRATE]:
		draw_style_box(title_style, Rect2(170, 12, 940, 125))
	if mode not in [Mode.DUEL, Mode.PRACTICE, Mode.CURRENT, Mode.VERSUS]: return
	for player: int in range(2 if local_two_player else 1):
		var fighter: BubbleDuelFighter = world.human(player)
		if fighter == null: continue
		var x: float = 28.0 if player == 0 else 1088.0
		for stock: int in range(mini(5, fighter.spares + 1)):
			draw_texture_rect(PEARL, Rect2(x + (stock % 3) * 40, 148 + (stock / 3) * 42, 34, 34), false)
		if world.round_limit > 0 or mode == Mode.CURRENT:
			var remaining: float = 1.0 - (active_time / 90.0 if mode == Mode.CURRENT else float(world.frame) / float(world.round_limit))
			draw_arc(Vector2(110 if player == 0 else 1170, 460), 17, -PI / 2, -PI / 2 + TAU * remaining, 30, Color(1, 0.88, 0.5), 5, true)
		if fighter.unlimited_rescues:
			draw_arc(Vector2(x + 160, 166), 12, 0, TAU, 20, Color(0.7, 1, 0.9), 3, true)



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


func _choose_gear(id: String) -> void:
	var bought := Shop.choose_item(main, id, shop_player)
	if bought:
		gear = Shop.equipped(main)
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
		wallet.visible = mode in [Mode.HUB, Mode.SHOP, Mode.SETUP, Mode.PICKER]


func _refresh_power() -> void:
	wallet.visible = mode in [Mode.HUB, Mode.SHOP, Mode.SETUP, Mode.PICKER]
	for player: int in range(2):
		var button: Button = power_button if player == 0 else second_power_button
		var bar: ProgressBar = glow_bar if player == 0 else second_glow_bar
		var fighter: BubbleDuelFighter = world.human(player)
		var playing: bool = mode in [Mode.DUEL, Mode.PRACTICE, Mode.CURRENT, Mode.VERSUS] and fighter != null
		button.visible = playing and fighter.gear != "classic"
		bar.visible = button.visible
		if not playing: continue
		var entry: Dictionary = Shop.item(fighter.gear)
		bar.value = fighter.charge
		button.disabled = fighter.lost or fighter.bubbles <= 0 or fighter.held > 0 or fighter.gear == "tidewing" or fighter.charge < float(entry["use"])
		button.icon = _icon(int(entry["icon"])) if int(entry["icon"]) >= 0 else null
		button.expand_icon = true
		button.add_theme_constant_override("icon_max_width", 90)
		button.tooltip_text = String(entry["help"])
		button.modulate.a = 0.55 if button.disabled else 1.0
		if player < duo_guides.size():
			duo_guides[player].visible = not world.started or world.paused



func _activate_power() -> void:
	if mode in [Mode.DUEL, Mode.PRACTICE, Mode.CURRENT, Mode.VERSUS]:
		duo.activate(0)



func _input(event: InputEvent) -> void:
	if mode in [Mode.DUEL, Mode.PRACTICE, Mode.CURRENT, Mode.VERSUS] and event is InputEventKey and duo.input(event):
		get_viewport().set_input_as_handled()



func _solo_rival_profile() -> Dictionary:
	var chosen := Shop.profile(main, 1)
	# Computer bouts use a plain loadout; the second human's saved gear is untouched.
	chosen["gear"] = "classic"
	return chosen


func _preview(parent: Control, profile: Dictionary, rect: Rect2, facing: float = 1.0) -> Control:
	var picture := Preview.new()
	picture.appearance = appearance
	picture.profile = profile.duplicate(true)
	picture.position = rect.position
	picture.size = rect.size
	picture.facing = facing
	parent.add_child(picture)
	return picture


func _show_setup(two_players: bool) -> void:
	_reset_input()
	_clear_menu()
	mode = Mode.SETUP
	local_two_player = false
	setup_two_player = two_players
	power_button.hide()
	glow_bar.hide()
	heading.text = "Two friends" if two_players else "Friendly Bubble Duel"
	hint.text = "Choose each friend, clothes and power item"
	for player: int in range(2):
		var chosen := Shop.profile(main, player)
		if player == 1 and not two_players:
			chosen = _solo_rival_profile()
		var title := ("Player %d" % (player + 1)) if two_players or player == 0 else "Computer friend"
		var card := _card(title + " · " + String(Cast.character(chosen["character"])["name"]), ROSHAN,
			Vector2(150 + player * 620, 178), _open_picker.bind(player, "character"), Color.WHITE, Vector2(360, 284))
		(card.get_child(0) as TextureRect).hide()
		_preview(card, chosen, Rect2(63, 0, 235, 220), 1.0 if player == 0 else -1.0)
		var ribbon: Texture2D = preload("res://assets/fashion/skin_engine_v2/garments/party.png")
		_card("Clothes", ribbon, Vector2(165 + player * 620, 475), _open_picker.bind(player, "look"), Color.WHITE, Vector2(158, 138))
		if two_players or player == 0:
			var icon := int(Shop.item(String(chosen["gear"]))["icon"])
			_card("Items & bubbles", bubble if icon < 0 else _icon(icon), Vector2(340 + player * 620, 475), _open_player_shop.bind(player), Color.WHITE, Vector2(158, 138))
	var play := Button.new()
	play.position = Vector2(552, 494)
	play.size = Vector2(176, 176)
	StorybookUI.style_navigation_button(play, "▶", "Play together" if two_players else "Play")
	play.add_theme_font_size_override("font_size", 64)
	if two_players:
		_card("Together vs friends", PEARL, Vector2(552, 290), _begin_coop, Color.WHITE, Vector2(176, 176))
	play.pressed.connect(_begin_versus if two_players else _begin.bind(Mode.DUEL))
	menu.add_child(play)
	_update_wallet()
	queue_redraw()


func _open_player_shop(player: int) -> void:
	shop_player = player
	shop_from_setup = true
	_show_shop()


func _open_picker(player: int, kind: String) -> void:
	selected_player = player
	picker_kind = kind
	picker_page = 0
	_show_picker()


func _show_picker() -> void:
	_reset_input()
	_clear_menu()
	mode = Mode.PICKER
	power_button.hide()
	glow_bar.hide()
	heading.text = "Player %d · %s" % [selected_player + 1, "Friends" if picker_kind == "character" else "Clothes"]
	hint.text = "Choose a picture"
	var chosen := Shop.profile(main, selected_player)
	var choices: Array[Dictionary] = Cast.ROSTER if picker_kind == "character" else Shop.looks(main, String(chosen["character"]))
	var pages := maxi(1, ceili(float(choices.size()) / 6.0))
	picker_page = clampi(picker_page, 0, pages - 1)
	for slot: int in range(6):
		var index := picker_page * 6 + slot
		if index >= choices.size(): break
		var entry: Dictionary = choices[index]
		var preview := chosen.duplicate(true)
		if picker_kind == "character":
			preview["character"] = entry["id"]
			if not Shop.look_available(main, String(entry["id"]), String(preview["look"])):
				preview["look"] = "set:classic"
		else:
			preview["look"] = entry["id"]
		var card := _card(String(entry["name"]), ROSHAN, Vector2(170 + (slot % 3) * 330, 174 + (slot / 3) * 211),
			_pick.bind(String(entry["id"])), Color.WHITE, Vector2(280, 198))
		(card.get_child(0) as TextureRect).hide()
		_preview(card, preview, Rect2(67, 0, 146, 142))
		card.set_meta("choice_id", entry["id"])
		if picker_kind == "character":
			card.disabled = entry["id"] not in Shop.state(main)["cast_unlocked"]
	if pages > 1:
		var previous := Button.new()
		previous.position = Vector2(180, 604)
		StorybookUI.style_navigation_button(previous, "←", "Previous clothes")
		previous.pressed.connect(_turn_picker.bind(-1))
		previous.disabled = picker_page == 0
		menu.add_child(previous)
		var next := Button.new()
		next.position = Vector2(992, 604)
		StorybookUI.style_navigation_button(next, "→", "More clothes")
		next.pressed.connect(_turn_picker.bind(1))
		next.disabled = picker_page == pages - 1
		menu.add_child(next)
	var back := Button.new()
	back.position = Vector2(584, 604)
	back.size = Vector2(112, 112)
	StorybookUI.style_navigation_button(back, "✓", "Ready")
	back.pressed.connect(_show_setup.bind(setup_two_player))
	menu.add_child(back)
	queue_redraw()


func _turn_picker(offset: int) -> void:
	picker_page += offset
	_show_picker()


func _pick(id: String) -> void:
	var selected := Shop.choose_character(main, id, selected_player) if picker_kind == "character" else Shop.choose_look(main, id, selected_player)
	if selected:
		main._audio_ref().pop(1)
		_show_setup(setup_two_player)


func _begin_versus() -> void:
	local_two_player = true
	cooperative = false
	_start_bout(Mode.VERSUS)


func _begin_coop() -> void:
	local_two_player = true
	cooperative = true
	_start_bout(Mode.VERSUS)



