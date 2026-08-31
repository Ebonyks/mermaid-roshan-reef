class_name ChapterTwoRoomPlot
extends Control

## Plot-only Castle-room affordances for Chapter 2.
##
## This is deliberately separate from CastleRooms25D's ordinary prop action.
## A button exists only for the exact director-owned objective and room, then
## is removed as soon as the plot advances or the child leaves the room.

const MAGNIFIER_TEXTURE := "res://assets/opera/worlds/ui/magnifier.png"
const BALLERINA_TEXTURE := \
	"res://assets/opera/worlds/props/goal_ballerina.png"
const PARTY_TEXTURE := \
	"res://assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png"
const GHOST_HAND_TEXTURE := \
	"res://assets/castle/training/ghost_hand.png"
const IGNITION_HOLD_SECONDS := 2.4
const SCOUT_HOLD_SECONDS := 1.8
const KING_APPROACH_SECONDS := 1.35

var m: ReefMain
var room_id := ""
var plot_action := ""
var ability_button: Button = null
var candle: ChapterTwoRainbowCandle2D = null
var party_table: ChapterTwoPartyTable2D = null
var party_sequence_elapsed := 0.0
var king_entry_started := false


func setup(main: ReefMain) -> void:
	m = main
	name = "ChapterTwoRoomPlot"
	position = Vector2.ZERO
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 46
	set_meta("plot_only_ability_surface", true)
	set_process(false)


func sync(next_room_id: String, announce: bool = true) -> void:
	room_id = next_room_id
	_clear_surface()
	if m == null or not m._chapter_two_ref().active:
		return
	if m._chapter_two_ref().should_show_candle(room_id):
		_build_candle()
	if m._chapter_two_ref().should_show_party_table(room_id):
		_build_party_table()
		_arm_party_sequence()
	plot_action = m._chapter_two_ref().room_plot_action(room_id)
	if plot_action == "":
		return
	_build_ability_button()
	if announce:
		_announce_plot_action()


func _clear_surface() -> void:
	set_process(false)
	party_sequence_elapsed = 0.0
	king_entry_started = false
	for child: Node in get_children():
		remove_child(child)
		child.queue_free()
	ability_button = null
	candle = null
	party_table = null
	plot_action = ""


func _arm_party_sequence() -> void:
	if party_table == null or m == null:
		return
	var director := m._chapter_two_ref()
	if not director.party_started or director.ember_king_crashed:
		return
	party_sequence_elapsed = 0.0
	king_entry_started = false
	set_process(true)
	set_meta("party_sequence_lifecycle_owned", true)
	set_meta("party_sequence_phase", director.party_event_phase)


func _process(delta: float) -> void:
	if m == null or party_table == null or not is_instance_valid(party_table) \
			or not is_visible_in_tree() \
			or not m._chapter_two_live_castle_room("main_hall"):
		return
	var director := m._chapter_two_ref()
	if not director.party_started or director.ember_king_crashed:
		set_process(false)
		return
	party_sequence_elapsed += delta
	if director.party_event_phase == ChapterTwoDirector.PARTY_EVENT_IGNITION:
		if party_sequence_elapsed < IGNITION_HOLD_SECONDS:
			return
		party_sequence_elapsed = 0.0
		if director.record_ember_scout():
			party_table.refresh()
			party_table.play_scout_arrival()
			m._queue_save()
			set_meta("party_sequence_phase", director.party_event_phase)
		return
	if director.party_event_phase != ChapterTwoDirector.PARTY_EVENT_SCOUT_SEEN:
		return
	if not king_entry_started:
		if party_sequence_elapsed < SCOUT_HOLD_SECONDS:
			return
		party_sequence_elapsed = 0.0
		king_entry_started = true
		party_table.play_king_entrance()
		set_meta("party_sequence_visual_beat", "king_approach")
		return
	if party_sequence_elapsed < KING_APPROACH_SECONDS:
		return
	set_process(false)
	if director.trigger_ember_king_crash("main_hall"):
		party_table.complete_king_take()
		m._write_save()
		set_meta("party_sequence_phase", director.party_event_phase)
		set_meta("party_sequence_visual_beat", "lit_candle_departure")


func _build_candle() -> void:
	candle = ChapterTwoRainbowCandle2D.new()
	candle.setup(false)
	candle.position = Vector2(588.0, 200.0)
	candle.scale = Vector2.ONE * 0.70
	candle.z_index = 2
	candle.set_meta("hidden_place", "library_magic_book")
	candle.set_meta("chapter2_locked_unlit", true)
	add_child(candle)


func _build_party_table() -> void:
	party_table = ChapterTwoPartyTable2D.new()
	party_table.setup(m)
	party_table.set_meta("room_id", "main_hall")
	add_child(party_table)


func _build_ability_button() -> void:
	ability_button = Button.new()
	ability_button.name = "ChapterTwoPlotAbility"
	ability_button.text = ""
	ability_button.tooltip_text = _action_hint()
	ability_button.custom_minimum_size = StorybookUI.MIN_TOUCH
	ability_button.focus_mode = Control.FOCUS_ALL
	ability_button.z_index = 5
	ability_button.set_meta("plot_only", true)
	ability_button.set_meta("plot_action", plot_action)
	ability_button.set_meta("room_id", room_id)
	ability_button.set_meta("general_room_activation", false)
	if plot_action == ChapterTwoDirector.ACTION_DETECTIVE_SEARCH:
		ability_button.position = Vector2(468.0, 92.0)
		ability_button.size = Vector2(196.0, 196.0)
		_add_picture(MAGNIFIER_TEXTURE, Vector2(34.0, 25.0), Vector2(128.0, 128.0))
	elif plot_action == ChapterTwoDirector.ACTION_STUFFIE_BALLET:
		ability_button.position = Vector2(394.0, 92.0)
		ability_button.size = Vector2(214.0, 198.0)
		_add_picture(BALLERINA_TEXTURE, Vector2(38.0, 20.0), Vector2(138.0, 138.0))
	elif plot_action == ChapterTwoDirector.ACTION_START_BIRTHDAY_PARTY:
		ability_button.position = Vector2(1032.0, 424.0)
		ability_button.size = Vector2(196.0, 172.0)
		_add_picture(PARTY_TEXTURE, Vector2(22.0, 19.0), Vector2(152.0, 118.0))
	else:
		ability_button.queue_free()
		ability_button = null
		return
	_style_plot_button(ability_button)
	ability_button.pressed.connect(_activate)
	add_child(ability_button)
	_add_pointer()
	if ability_button.is_inside_tree():
		ability_button.grab_focus()


func _add_picture(path: String, picture_position: Vector2,
		picture_size: Vector2) -> void:
	var picture := TextureRect.new()
	picture.name = "SkillPicture"
	picture.position = picture_position
	picture.size = picture_size
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	picture.texture = load(path) as Texture2D
	picture.set_meta("visual_pointer", true)
	ability_button.add_child(picture)


func _add_pointer() -> void:
	var pointer := Sprite2D.new()
	pointer.name = "ChapterTwoPlotPointer"
	pointer.texture = load(GHOST_HAND_TEXTURE) as Texture2D
	var pointer_start := Vector2(ability_button.size.x - 24.0, 26.0)
	pointer.position = pointer_start
	pointer.scale = Vector2.ONE * 0.13
	pointer.set_meta("visual_pointer", true)
	pointer.set_meta("points_to_plot_prop", plot_action)
	ability_button.add_child(pointer)
	var tween := pointer.create_tween().set_loops()
	tween.tween_property(pointer, "position:y", pointer_start.y + 16.0, 0.46) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(pointer, "position:y", pointer_start.y, 0.46) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)


func _style_plot_button(button: Button) -> void:
	var normal := StorybookUI.panel_style(
		Color(0.32, 0.20, 0.52, 0.10), StorybookUI.GOLD, 52, 4)
	var hover := StorybookUI.panel_style(
		Color(0.46, 0.28, 0.66, 0.18), Color.WHITE, 52, 6)
	button.add_theme_stylebox_override("normal", normal)
	button.add_theme_stylebox_override("hover", hover)
	button.add_theme_stylebox_override("pressed", hover)
	button.add_theme_stylebox_override("focus", hover)


func _action_hint() -> String:
	match plot_action:
		ChapterTwoDirector.ACTION_DETECTIVE_SEARCH:
			return "Use Detective at the magic storybook"
		ChapterTwoDirector.ACTION_STUFFIE_BALLET:
			return "Lead the stuffies in their birthday ballet"
		ChapterTwoDirector.ACTION_START_BIRTHDAY_PARTY:
			return "Start Mermaid Roshan's birthday party"
	return "Party surprise"


func _announce_plot_action() -> void:
	match plot_action:
		ChapterTwoDirector.ACTION_DETECTIVE_SEARCH:
			m.show_msg("",
				"Detective sparkle! Search the magic storybook!", "hint")
		ChapterTwoDirector.ACTION_STUFFIE_BALLET:
			m.show_msg("",
				"Ballerina sparkle! The stuffies are ready to dance!", "hint")
		ChapterTwoDirector.ACTION_START_BIRTHDAY_PARTY:
			m.show_msg("",
				"Everything is ready! Tap the rainbow to start the party!", "hint")


func _activate() -> void:
	if m == null or plot_action == "":
		return
	m.chapter2_activate_room_plot(room_id, plot_action)
