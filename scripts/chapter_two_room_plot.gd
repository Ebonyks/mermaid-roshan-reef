class_name ChapterTwoRoomPlot
extends Control

## Plot-only Castle-room affordances for Chapter 2.
##
## CastleRooms25D's painted book and stuffie-nook hotspots own their plot
## actions. The party table adds only a transparent touch surface over its
## visible world art; this layer never creates a floating ability button.
const IGNITION_HOLD_SECONDS := 2.4
const SCOUT_HOLD_SECONDS := 1.8
const KING_APPROACH_SECONDS := 1.35

var m: ReefMain
var room_id := ""
var plot_action := ""
var party_touch_surface: Control = null
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
	set_meta("direct_world_plot_surface", true)
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
	if plot_action == ChapterTwoDirector.ACTION_START_BIRTHDAY_PARTY:
		_build_party_touch_surface()
	if announce:
		_announce_plot_action()


func _clear_surface() -> void:
	set_process(false)
	party_sequence_elapsed = 0.0
	king_entry_started = false
	for child: Node in get_children():
		remove_child(child)
		child.queue_free()
	party_touch_surface = null
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


func _build_party_touch_surface() -> void:
	party_touch_surface = Control.new()
	party_touch_surface.name = "ChapterTwoPartyTableTouch"
	party_touch_surface.position = Vector2(285.0, 352.0)
	party_touch_surface.size = Vector2(710.0, 238.0)
	party_touch_surface.mouse_filter = Control.MOUSE_FILTER_STOP
	party_touch_surface.z_index = 5
	party_touch_surface.set_meta("direct_world_art_hotspot", true)
	party_touch_surface.set_meta("plot_action", plot_action)
	party_touch_surface.gui_input.connect(_on_party_table_input)
	add_child(party_touch_surface)


func _on_party_table_input(event: InputEvent) -> void:
	var pressed := event is InputEventScreenTouch \
		and (event as InputEventScreenTouch).pressed
	pressed = pressed or (event is InputEventMouseButton \
		and (event as InputEventMouseButton).pressed \
		and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT)
	if not pressed:
		return
	party_touch_surface.accept_event()
	_activate()


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
