class_name DirtyCastleStage
extends RefCounted
# Day One is a genuine full-screen Control minigame, not a navigable world.
# Its one native 2K vector master and transparent cutouts are UI presentation;
# no Node3D, mesh, light, physics body, or passive helper can complete a target.

const ART := "res://assets/castle/dirty_cleanup_2d/"
const BACKGROUND := "res://assets/flats/dirty_castle/day_one_dirty_castle_2048x1024.svg"
const RUBS_PER_TARGET := 3
const ROOMS := [
	{
		"id": "grand_hall", "dirty": BACKGROUND,
		"clean": BACKGROUND,
		"tool": ART + "tools/tool_star_sponge.png",
		"voice": "The imp left a mess. Tap the glowing spot and make the hall sparkle!",
		"targets": [
			{"id": "hall_window", "art": ART + "targets/target_window_smudge.png", "rect": Rect2(110, 180, 260, 260)},
			{"id": "hall_floor", "art": ART + "targets/target_floor_scuff.png", "rect": Rect2(485, 390, 300, 250)},
			{"id": "hall_cobweb", "art": ART + "targets/target_cobweb.png", "rect": Rect2(900, 145, 250, 250)},
		],
	},
	{
		"id": "playroom", "dirty": BACKGROUND,
		"clean": BACKGROUND,
		"tool": ART + "tools/tool_sorting_basket.png",
		"voice": "One toy at a time. Tap the glowing toy and put it away!",
		"targets": [
			{"id": "play_puzzle", "art": ART + "targets/target_toy_blocks.png", "rect": Rect2(90, 390, 290, 260)},
			{"id": "play_dressup", "art": ART + "targets/target_buttons_beads.png", "rect": Rect2(475, 330, 300, 290)},
			{"id": "play_balls", "art": ART + "targets/target_cloud_cushions.png", "rect": Rect2(880, 360, 290, 270)},
		],
	},
	{
		"id": "library", "dirty": BACKGROUND,
		"clean": BACKGROUND,
		"tool": ART + "tools/tool_ribbon_duster.png",
		"voice": "The books need their homes. Tap the glow and tidy each pile!",
		"targets": [
			{"id": "library_books", "art": ART + "targets/target_tipped_books.png", "rect": Rect2(80, 375, 300, 270)},
			{"id": "library_cart", "art": ART + "targets/target_dusty_shelf.png", "rect": Rect2(470, 300, 320, 320)},
			{"id": "library_cushions", "art": ART + "targets/target_cobweb.png", "rect": Rect2(870, 365, 300, 275)},
		],
	},
	{
		"id": "kitchen", "dirty": BACKGROUND,
		"clean": BACKGROUND,
		"tool": ART + "tools/tool_shell_scrub_brush.png",
		"voice": "The stove is cool. Tap each glow and scrub the kitchen shiny!",
		"targets": [
			{"id": "kitchen_sink", "art": ART + "targets/target_sticky_spill.png", "rect": Rect2(70, 330, 310, 300)},
			{"id": "kitchen_flour", "art": ART + "targets/target_flour_spill.png", "rect": Rect2(465, 360, 320, 275)},
			{"id": "kitchen_stove", "art": ART + "targets/target_muddy_footprints.png", "rect": Rect2(875, 325, 300, 305)},
		],
	},
	{
		"id": "bubble_bath", "dirty": BACKGROUND,
		"clean": BACKGROUND,
		"tool": ART + "tools/tool_window_squeegee.png",
		"voice": "Sponge, wipe, and sort. Tap the glow to clean the Bubble Bath!",
		"targets": [
			{"id": "bath_mirror", "art": ART + "targets/target_cloudy_mirror.png", "rect": Rect2(80, 180, 300, 310)},
			{"id": "bath_ring", "art": ART + "targets/target_bath_soap_ring.png", "rect": Rect2(465, 345, 330, 285)},
			{"id": "bath_toys", "art": ART + "targets/target_leaf_trail.png", "rect": Rect2(875, 360, 300, 275)},
		],
	},
	{
		"id": "royal_loo", "dirty": BACKGROUND,
		"clean": BACKGROUND,
		"tool": ART + "tools/tool_star_sponge.png",
		"voice": "Only soap and clean water. Tap each glow and make it sparkle!",
		"targets": [
			{"id": "loo_ring", "art": ART + "targets/target_bath_soap_ring.png", "rect": Rect2(100, 320, 300, 310)},
			{"id": "loo_rolls", "art": ART + "targets/target_muddy_footprints.png", "rect": Rect2(480, 340, 300, 285)},
			{"id": "loo_splash", "art": ART + "targets/target_sticky_spill.png", "rect": Rect2(875, 375, 300, 250)},
		],
	},
	{
		"id": "undercroft", "dirty": BACKGROUND,
		"clean": BACKGROUND,
		"tool": ART + "tools/tool_shell_broom.png",
		"voice": "Last room. Tap the two glows and help the dust bunnies home!",
		"targets": [
			{"id": "under_storage", "art": ART + "targets/target_dust_bunnies.png", "rect": Rect2(240, 320, 330, 310)},
			{"id": "under_stairs", "art": ART + "targets/target_cobweb.png", "rect": Rect2(710, 270, 330, 340)},
		],
	},
]

var m: ReefMain
var layer: CanvasLayer = null
var stage: Control = null
var background: TextureRect = null
var target_root: Control = null
var tool_card: TextureRect = null
var progress_row: HBoxContainer = null
var continue_button: Button = null
var room_index := 0
var pulse_t := 0.0

func _init(main: ReefMain) -> void:
	m = main

func build() -> void:
	clear()
	m.player.visible = false
	m.player.vel = Vector3.ZERO
	m._set_world_controls_enabled(false, "dirty_castle")
	layer = CanvasLayer.new()
	layer.name = "DirtyCastle2DLayer"
	layer.layer = 6
	m.add_child(layer)
	m.dirty_castle_layer = layer
	layer.set_meta("presentation_kind", "full_screen_control_minigame")
	layer.set_meta("navigable_world", false)
	layer.set_meta("runtime_plate", BACKGROUND)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	layer.add_child(root)
	var ink := ColorRect.new()
	ink.set_anchors_preset(Control.PRESET_FULL_RECT)
	ink.color = Color(0.04, 0.03, 0.12)
	root.add_child(ink)
	stage = StorybookUI.add_stage(root, m.get_viewport().get_visible_rect().size)
	background = TextureRect.new()
	background.size = StorybookUI.CANVAS_SIZE
	background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(background)
	target_root = Control.new()
	target_root.size = StorybookUI.CANVAS_SIZE
	stage.add_child(target_root)
	progress_row = HBoxContainer.new()
	progress_row.position = Vector2(440, 18)
	progress_row.size = Vector2(400, 58)
	progress_row.add_theme_constant_override("separation", 10)
	stage.add_child(progress_row)
	tool_card = TextureRect.new()
	tool_card.position = Vector2(1135, 18)
	tool_card.size = Vector2(120, 120)
	tool_card.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	tool_card.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	tool_card.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(tool_card)
	var back := Button.new()
	back.name = "DirtyCastleBackButton"
	StorybookUI.style_back_button(back, "Back outside")
	back.position = Vector2(22, 580)
	back.pressed.connect(_leave_castle)
	stage.add_child(back)
	continue_button = Button.new()
	continue_button.name = "DirtyCastleNextRoomButton"
	StorybookUI.style_icon_button(continue_button, ">>", "gold",
		Vector2(164, 150), "Next room")
	continue_button.position = Vector2(1088, 548)
	continue_button.pressed.connect(_continue_to_next_room)
	stage.add_child(continue_button)
	room_index = _first_incomplete_room()
	if room_index >= ROOMS.size():
		_show_finale()
	else:
		_show_room(room_index)

func clear() -> void:
	if layer != null and is_instance_valid(layer):
		layer.queue_free()
	layer = null
	stage = null
	background = null
	target_root = null
	tool_card = null
	progress_row = null
	continue_button = null
	if m.dirty_castle_layer != null:
		m.dirty_castle_layer = null
	m._set_world_controls_enabled(true, "dirty_castle")
	if m.player != null:
		m.player.visible = true

func tick(delta: float) -> void:
	pulse_t += delta
	if target_root == null:
		return
	var active_id := current_target_id()
	for child: Node in target_root.get_children():
		if child is Button and String(child.get_meta("target_id", "")) == active_id:
			var ring: TextureRect = child.get_meta("ring") as TextureRect
			if ring != null and is_instance_valid(ring):
				var pulse: float = 1.0 + sin(pulse_t * 5.0) * 0.06
				ring.scale = Vector2.ONE * pulse

func _show_room(next_index: int) -> void:
	room_index = next_index
	_clear_targets()
	continue_button.visible = false
	var room: Dictionary = ROOMS[room_index]
	background.texture = load(BACKGROUND) as Texture2D
	background.modulate = Color(0.80, 0.78, 0.88)
	tool_card.texture = load(String(room["tool"])) as Texture2D
	var targets: Array = room["targets"]
	for target_value: Variant in targets:
		var target: Dictionary = target_value as Dictionary
		if not bool(m.clean_done.get(String(target["id"]), false)):
			_add_target(target)
	_refresh_progress()
	_refresh_pointer()
	if current_target_id() == "":
		_show_room_complete()
	else:
		m.show_msg("Princess Huluu", String(room["voice"]), "intro")

func _add_target(target: Dictionary) -> void:
	var rect: Rect2 = target["rect"]
	var button := Button.new()
	button.name = "CleanTarget_" + String(target["id"])
	button.position = rect.position
	button.size = rect.size
	button.focus_mode = Control.FOCUS_NONE
	button.set_meta("target_id", String(target["id"]))
	button.set_meta("rubs", 0)
	var empty := StyleBoxEmpty.new()
	for state: String in ["normal", "hover", "pressed", "disabled", "focus"]:
		button.add_theme_stylebox_override(state, empty)
	var ring := TextureRect.new()
	ring.texture = load(ART + "effects/fx_clean_ring.png") as Texture2D
	ring.position = Vector2(-18, -18)
	ring.size = rect.size + Vector2(36, 36)
	ring.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	ring.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	ring.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ring.pivot_offset = ring.size * 0.5
	button.add_child(ring)
	button.set_meta("ring", ring)
	var art := TextureRect.new()
	art.name = "TargetArt"
	art.texture = load(String(target["art"])) as Texture2D
	art.size = rect.size
	art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	button.add_child(art)
	button.pressed.connect(_rub_target.bind(String(target["id"])))
	target_root.add_child(button)

func _rub_target(target_id: String) -> void:
	if target_id != current_target_id():
		return
	var button := target_root.find_child("CleanTarget_" + target_id, false, false) as Button
	if button == null:
		return
	var rubs: int = int(button.get_meta("rubs", 0)) + 1
	button.set_meta("rubs", rubs)
	var art := button.get_node("TargetArt") as TextureRect
	if art != null:
		art.modulate.a = maxf(0.25, 1.0 - float(rubs) * 0.22)
		var pop: Tween = art.create_tween()
		pop.tween_property(art, "scale", Vector2.ONE * 1.08, 0.08)
		pop.tween_property(art, "scale", Vector2.ONE, 0.12)
	_feedback(button.get_rect())
	if m.chime != null:
		m.chime.pitch_scale = 0.9 + 0.12 * float(rubs)
		m.chime.play()
	if rubs < RUBS_PER_TARGET:
		return
	m.clean_done[target_id] = true
	m.save_data["clean_done"] = m.clean_done.duplicate(true)
	m._write_save()
	button.queue_free()
	_refresh_progress()
	if current_target_id() == "":
		_show_room_complete()
	else:
		_refresh_pointer()
		m.show_msg("Princess Huluu", "Sparkly! Now follow the next glowing ring!", "thanks")

func _feedback(rect: Rect2) -> void:
	var puff := TextureRect.new()
	puff.texture = load(ART + "effects/fx_soap_bubbles.png") as Texture2D
	puff.position = rect.position + rect.size * 0.5 - Vector2(75, 75)
	puff.size = Vector2(150, 150)
	puff.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	puff.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	puff.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(puff)
	var tween: Tween = puff.create_tween()
	tween.tween_property(puff, "position", puff.position + Vector2(0, -70), 0.55)
	tween.parallel().tween_property(puff, "modulate:a", 0.0, 0.55)
	tween.tween_callback(puff.queue_free)

func _refresh_pointer() -> void:
	if target_root == null:
		return
	var active_id := current_target_id()
	for child: Node in target_root.get_children():
		if child is Button:
			var active: bool = String(child.get_meta("target_id", "")) == active_id
			(child as Button).disabled = not active
			(child as Button).modulate = Color.WHITE if active else Color(0.65, 0.65, 0.78, 0.62)
			var ring: TextureRect = child.get_meta("ring") as TextureRect
			if ring != null:
				ring.visible = active

func _refresh_progress() -> void:
	if progress_row == null:
		return
	for child: Node in progress_row.get_children():
		child.queue_free()
	for room_value: Variant in ROOMS:
		var room: Dictionary = room_value as Dictionary
		var icon := TextureRect.new()
		icon.texture = load(ART + "progress/progress_three_pearls.png") as Texture2D
		icon.custom_minimum_size = Vector2(48, 48)
		icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		icon.modulate = Color.WHITE if _room_done(room) else Color(0.42, 0.44, 0.58, 0.55)
		progress_row.add_child(icon)

func _show_room_complete() -> void:
	var room: Dictionary = ROOMS[room_index]
	background.texture = load(BACKGROUND) as Texture2D
	background.modulate = Color.WHITE
	_clear_targets()
	_refresh_progress()
	m._fanfare()
	m.show_msg("Princess Huluu", "This room is clean! Tap the golden arrow for the next room!", "thanks")
	if room_index + 1 < ROOMS.size():
		continue_button.visible = true
	else:
		_show_finale()

func _continue_to_next_room() -> void:
	if room_index + 1 < ROOMS.size():
		_show_room(room_index + 1)
	else:
		_show_finale()

func _show_finale() -> void:
	_clear_targets()
	background.texture = load(BACKGROUND) as Texture2D
	background.modulate = Color.WHITE
	var badge := TextureRect.new()
	badge.name = "DirtyCastleAllCleanBadge"
	badge.texture = load(ART + "effects/fx_all_clean_badge.png") as Texture2D
	badge.position = Vector2(450, 110)
	badge.size = Vector2(380, 380)
	badge.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	badge.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
	target_root.add_child(badge)
	tool_card.visible = false
	continue_button.visible = false
	_refresh_progress()
	m._fanfare()
	m.show_msg("Princess Huluu", "The whole castle sparkles! You cleaned it piece by piece!", "win")

func _clear_targets() -> void:
	if target_root == null:
		return
	for child: Node in target_root.get_children():
		target_root.remove_child(child)
		child.queue_free()

func _first_incomplete_room() -> int:
	for index in range(ROOMS.size()):
		if not _room_done(ROOMS[index] as Dictionary):
			return index
	return ROOMS.size()

func _room_done(room: Dictionary) -> bool:
	for target_value: Variant in (room["targets"] as Array):
		var target: Dictionary = target_value as Dictionary
		if not bool(m.clean_done.get(String(target["id"]), false)):
			return false
	return true

func current_target_id() -> String:
	if room_index < 0 or room_index >= ROOMS.size():
		return ""
	var room: Dictionary = ROOMS[room_index]
	for target_value: Variant in (room["targets"] as Array):
		var target: Dictionary = target_value as Dictionary
		var target_id := String(target["id"])
		if not bool(m.clean_done.get(target_id, false)):
			return target_id
	return ""

func rub_active() -> void:
	var target_id := current_target_id()
	if target_id != "":
		_rub_target(target_id)

func targets_left() -> int:
	var left := 0
	for room_value: Variant in ROOMS:
		var room: Dictionary = room_value as Dictionary
		for target_value: Variant in (room["targets"] as Array):
			var target: Dictionary = target_value as Dictionary
			if not bool(m.clean_done.get(String(target["id"]), false)):
				left += 1
	return left

func _leave_castle() -> void:
	clear()
	m._enter_level2(true)
