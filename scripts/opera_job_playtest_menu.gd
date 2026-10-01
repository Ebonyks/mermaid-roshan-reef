class_name OperaJobPlaytestMenu
extends Control
## Owner-requested temporary elevator launcher. Uses the shipping job engine;
## each run is fresh and opts out of durable story, checkpoint and reward writes.

const ENABLED := true
const ROUTE_ID := "opera_job_playtest"
const COLUMNS := 5
const CARD_SIZE := Vector2(224.0, 152.0)
const CARD_GAP := Vector2(14.0, 14.0)
const GRID_ORIGIN := Vector2(52.0, 182.0)

var m: ReefMain
var venue: OperaHouseVenue2D
var job_buttons: Array[Button] = []
var session_open := false
var running := false
var shutting_down := false


func setup(main: ReefMain, owner_venue: OperaHouseVenue2D) -> void:
	m = main
	venue = owner_venue
	name = "OperaJobPlaytestMenu"
	position = Vector2.ZERO
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 70
	hide()


func open() -> void:
	if not ENABLED or session_open or not _owns_venue():
		return
	if job_buttons.is_empty():
		_build_menu()
	session_open = true
	venue.accepting_input = false
	venue.refresh(m.opera_stars)
	if venue.guide_pointer != null:
		venue.guide_pointer.hide()
	m.clear_dialogue()
	m._set_world_controls_enabled(false, ROUTE_ID)
	m._navigation_push(ROUTE_ID, self, Callable(self, "close"))
	show()


func close() -> void:
	shutdown()
	if is_instance_valid(venue) and venue.visible:
		venue.accepting_input = true
		venue.refresh(m.opera_stars)


func shutdown() -> void:
	if not session_open or shutting_down:
		return
	shutting_down = true
	if running and m.opera_game != null:
		m.opera_game._leave_early()
	session_open = false
	running = false
	hide()
	m._navigation_remove(ROUTE_ID)
	m._set_world_controls_enabled(true, ROUTE_ID)
	shutting_down = false


func launch_job(act_index: int) -> bool:
	if not session_open or running or not visible or not _owns_venue() \
			or not OperaHouse.is_live_act_index(act_index):
		return false
	running = true
	hide()
	venue.hide()
	m._castle_rooms_ref().suspend()
	m.clear_dialogue()
	m.game = "opera"
	m.opera_return_room = "opera_hall"
	m.opera_active_act_index = act_index
	OperaRoutePresentation.suspend(m)
	var house := OperaHouse.new()
	m.add_child(house)
	m.opera_game = house
	if not house.start(m, act_index, Callable(self, "_job_finished"), {},
			{"reward_policy": "dev_playtest"}):
		m._navigation_remove("opera_act")
		house.queue_free()
		_job_finished(false)
		return false
	return true


func _job_finished(_completed: bool) -> void:
	m.clear_dialogue()
	m.opera_game = null
	m.opera_active_act_index = -1
	m.opera_return_room = ""
	m.opera_plot_context = ""
	running = false
	m._restore_opera_route_state("opera_hall")
	if shutting_down or not session_open or not is_instance_valid(venue):
		return
	venue.show()
	venue.accepting_input = false
	venue.refresh(m.opera_stars)
	show()
	m._navigation_push(ROUTE_ID, self, Callable(self, "close"))


func _owns_venue() -> bool:
	return m != null and is_instance_valid(venue) and venue.is_open() \
		and m.game == "level2" and m.castle_room_id == "opera_hall" \
		and m.castle_room_layer != null and m.castle_room_layer.visible \
		and m.opera_game == null and m.opera_pending_act_index < 0 \
		and venue.tree_book_test == null \
		and (m.fade_rect == null or m.fade_rect.modulate.a <= 0.02)


func _build_menu() -> void:
	var paper := ColorRect.new()
	paper.color = StorybookUI.PAPER
	paper.size = size
	paper.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(paper)
	var title := Label.new()
	title.text = "Job playtesting"
	title.position = Vector2(172.0, 28.0)
	title.size = Vector2(1010.0, 60.0)
	title.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(title, 44)
	add_child(title)
	var caption := Label.new()
	caption.text = "DEV MODE - Fresh runs. Saved progress and rewards stay safe."
	caption.position = Vector2(172.0, 94.0)
	caption.size = Vector2(1030.0, 66.0)
	caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	StorybookUI.style_label(caption, 26)
	add_child(caption)
	for slot: int in range(OperaHouse.LIVE_ACT_INDICES.size()):
		var act_index: int = OperaHouse.LIVE_ACT_INDICES[slot]
		var config: Dictionary = OperaHouse.ACTS[act_index]
		var costume := String(config.get("costume", ""))
		var button := Button.new()
		button.name = "PlaytestJob_%02d" % act_index
		button.position = GRID_ORIGIN + Vector2(
			float(slot % COLUMNS) * (CARD_SIZE.x + CARD_GAP.x),
			float(slot / COLUMNS) * (CARD_SIZE.y + CARD_GAP.y))
		button.size = CARD_SIZE
		button.text = ""
		button.tooltip_text = "%s - %s" % [String(config.get("career", "")),
			CastleCareerRoutes.room_for_act(act_index).replace("_", " ")]
		button.set_meta("act_index", act_index)
		StorybookUI.style_picture_button(button)
		button.pressed.connect(launch_job.bind(act_index))
		add_child(button)
		job_buttons.append(button)
		var picture := TextureRect.new()
		picture.name = "JobPicture"
		picture.position = Vector2(72.0, 8.0)
		picture.size = Vector2(80.0, 80.0)
		var file := String(CastleCareerRoutes.CAREER_CREST_FILES.get(costume, ""))
		var path := file if file.begins_with("res://") else CastleCareerRoutes.CREST_ROOT + file
		picture.texture = load(path) as Texture2D
		picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
		button.add_child(picture)
		var label := Label.new()
		label.text = String(config.get("career", ""))
		label.position = Vector2(8.0, 91.0)
		label.size = Vector2(208.0, 54.0)
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		StorybookUI.style_label(label, 28)
		button.add_child(label)
