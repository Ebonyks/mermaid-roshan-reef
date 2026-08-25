class_name CastleCareerRoutes
extends RefCounted
## Picture-first Castle-room entrances for the thirteen live Opera careers.
##
## Owner authority distributes the careers through themed Castle rooms. The
## historical Opera save slots remain sparse and stable; this surface only
## decides where each existing Canvas activity can be launched.

const CREST_ROOT := "res://assets/opera/worlds/ui/crests/"
const ACTOR_ROOT := "res://assets/opera/worlds/actors/"
const CARD_SIZE := Vector2(154.0, 154.0)
const CARD_GAP := 22.0
# Bottom-anchored so the full touch cards clear Roshan's face and walk lane;
# the eight-pixel floor inset keeps silhouettes readable without stealing the
# corner movement/elevator controls.
const CARD_Y := StorybookUI.CANVAS_SIZE.y - CARD_SIZE.y - 8.0

const ROOM_ACT_INDICES := {
	"kitchen": [0, 3],
	"opera_hall": [2, 13, 8],
	"library": [1],
	"craft_room": [10],
	"playroom": [5, 7],
	"bubble_bath": [15],
	"mermaid_pool": [11],
	"dining_room": [6],
	# The owner left Racer's final home as Movie Lounge OR Courtyard. Movie
	# Lounge is the bounded Castle-room choice: its big screen is a truthful
	# Grand Prix picture affordance and it avoids two legacy Courtyard races.
	"movie_lounge": [12],
}
const CAREER_CREST_FILES := {
	"chef": "opera_crest_chef.png",
	"detective": "opera_crest_detective.png",
	"ballerina": "opera_crest_ballerina.png",
	"candymaker": "opera_crest_candy.png",
	"doctor": "opera_crest_doctor.png",
	"farmer": "opera_crest_farmer.png",
	"boxer": "opera_crest_boxer.png",
	"magician": "opera_crest_magician.png",
	"painter": "opera_crest_painter.png",
	"astronaut": "opera_crest_engineer.png",
	"racer": "opera_crest_racer.png",
	"popstar": "opera_crest_singer.png",
	"nursery": "goal_nursery.png",
}

var m: ReefMain
var root: Control = null
var stage_owner: Control = null
var room_id := ""
var buttons: Array[Button] = []
var active_animator: OperaRoshanActor = null
var highlighted_act := -1
var opera_venue: OperaHouseVenue2D = null


func _init(main: ReefMain) -> void:
	m = main


static func act_indices_for_room(target_room: String) -> Array[int]:
	var result: Array[int] = []
	for value: Variant in (ROOM_ACT_INDICES.get(target_room, []) as Array):
		result.append(int(value))
	return result


static func room_for_act(act_index: int) -> String:
	for target_room: String in ROOM_ACT_INDICES:
		if (ROOM_ACT_INDICES[target_room] as Array).has(act_index):
			return target_room
	return ""


static func route_matches(target_room: String, act_index: int) -> bool:
	return room_for_act(act_index) == target_room \
		and OperaHouse.is_live_act_index(act_index)


static func routed_act_indices() -> Array[int]:
	var result: Array[int] = []
	for target_room: String in ROOM_ACT_INDICES:
		for act_index: int in act_indices_for_room(target_room):
			if not result.has(act_index):
				result.append(act_index)
	result.sort()
	return result


static func preferred_act_for_room(target_room: String, stars: int) -> int:
	var indices := act_indices_for_room(target_room)
	for act_index: int in indices:
		if (stars & (1 << act_index)) == 0:
			return act_index
	return indices[0] if not indices.is_empty() else -1


func sync() -> void:
	var stage := m.castle_room_stage as Control
	if stage == null or not is_instance_valid(stage):
		clear()
		return
	if root == null or not is_instance_valid(root) or stage_owner != stage:
		_attach(stage)
	if room_id != m.castle_room_id:
		room_id = m.castle_room_id
		_rebuild_room()
	var castle_visible := m.castle_room_layer != null \
		and is_instance_valid(m.castle_room_layer) \
		and m.castle_room_layer.visible
	root.visible = not m.day_one_jobs_locked() \
		and castle_visible and m.game == "level2" \
		and String(m.g.get("phase", "")) == "hall" \
		and m.mg_kind == "" and m.opera_game == null \
		and not m.castle_room_menu_open and not buttons.is_empty()
	if root.visible:
		_refresh_completion()


func clear() -> void:
	_stop_animator()
	buttons.clear()
	opera_venue = null
	room_id = ""
	stage_owner = null
	if root != null and is_instance_valid(root):
		root.queue_free()
	root = null


func button_for_act(act_index: int) -> Button:
	for button: Button in buttons:
		if int(button.get_meta("act_index", -1)) == act_index:
			return button
	return null


func guide_current_room() -> bool:
	if m.day_one_jobs_locked():
		return false
	sync()
	if room_id == "opera_hall" and opera_venue != null \
			and is_instance_valid(opera_venue) and opera_venue.is_open():
		return opera_venue.guide_current_floor()
	var act_index := preferred_act_for_room(room_id, m.opera_stars)
	var button := button_for_act(act_index)
	if button == null or not button.visible or button.disabled:
		return false
	_highlight(act_index)
	button.grab_focus()
	return true


func _attach(stage: Control) -> void:
	clear()
	stage_owner = stage
	root = Control.new()
	root.name = "CastleCareerRoutes"
	root.position = Vector2.ZERO
	root.size = StorybookUI.CANVAS_SIZE
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.z_index = 35
	root.set_meta("room_owned_career_routes", true)
	stage.add_child(root)
	active_animator = OperaRoshanActor.new()
	active_animator.name = "ActiveRoomCareerAnimator"
	root.add_child(active_animator)
	room_id = m.castle_room_id
	_rebuild_room()


func _rebuild_room() -> void:
	_stop_animator()
	buttons.clear()
	opera_venue = null
	if root == null or not is_instance_valid(root):
		return
	for child: Node in root.get_children():
		if child != active_animator:
			child.queue_free()
	if m.day_one_jobs_locked():
		return
	var indices := act_indices_for_room(room_id)
	if indices.is_empty():
		return
	if room_id == "opera_hall":
		opera_venue = OperaHouseVenue2D.new()
		opera_venue.setup(
			m, m.opera_stars, Callable(self, "_launch_opera_venue"))
		root.add_child(opera_venue)
		buttons = opera_venue.career_buttons()
		_refresh_completion()
		return
	var width := float(indices.size()) * CARD_SIZE.x \
		+ float(indices.size() - 1) * CARD_GAP
	var left := (StorybookUI.CANVAS_SIZE.x - width) * 0.5
	for slot: int in range(indices.size()):
		var act_index: int = indices[slot]
		var config: Dictionary = OperaHouse.ACTS[act_index]
		var costume := String(config.get("costume", ""))
		var button := Button.new()
		button.name = "RoomCareer_%02d" % act_index
		button.text = ""
		button.tooltip_text = "Play %s" % String(config.get("career", "career"))
		button.position = Vector2(
			left + float(slot) * (CARD_SIZE.x + CARD_GAP), CARD_Y)
		button.size = CARD_SIZE
		button.custom_minimum_size = StorybookUI.MIN_TOUCH
		button.clip_contents = false
		button.focus_mode = Control.FOCUS_ALL
		button.set_meta("act_index", act_index)
		button.set_meta("castle_room_id", room_id)
		button.set_meta("picture_first", true)
		button.set_meta("career_costume", costume)
		button.set_meta("screen_hit_size", button.size)
		button.set_meta("presentation", "room_picture_card")
		StorybookUI.style_picture_button(
			button, Color(0.94, 0.96, 1.0, 0.98), StorybookUI.GOLD, 42)
		button.pressed.connect(_launch.bind(room_id, act_index))
		button.focus_entered.connect(_highlight.bind(act_index))
		button.mouse_entered.connect(_highlight.bind(act_index))
		root.add_child(button)
		buttons.append(button)

		var actor := TextureRect.new()
		actor.name = "RoshanActor"
		actor.position = Vector2(21.0, 2.0)
		actor.size = Vector2(112.0, 112.0)
		actor.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		actor.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		actor.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var fallback_path := ACTOR_ROOT + "roshan_%s.png" % costume
		var fallback: Texture2D = load(fallback_path) as Texture2D \
			if ResourceLoader.exists(fallback_path) else null
		actor.texture = OperaRoshanActor.idle_frame(costume, fallback)
		button.add_child(actor)

		var crest := TextureRect.new()
		crest.name = "CareerCrest"
		crest.position = Vector2(52.0, 98.0)
		crest.size = Vector2(50.0, 50.0)
		crest.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		crest.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		crest.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var crest_file := String(CAREER_CREST_FILES.get(costume, ""))
		var crest_path := CREST_ROOT + crest_file
		if crest_file != "" and ResourceLoader.exists(crest_path):
			crest.texture = load(crest_path) as Texture2D
		button.add_child(crest)

		var pearl := Panel.new()
		pearl.name = "CareerPearl"
		pearl.position = Vector2(118.0, 6.0)
		pearl.size = Vector2(28.0, 28.0)
		pearl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		button.add_child(pearl)
	_refresh_completion()
	_highlight(preferred_act_for_room(room_id, m.opera_stars))

func _refresh_completion() -> void:
	for button: Button in buttons:
		var act_index := int(button.get_meta("act_index", -1))
		var complete := act_index >= 0 and (m.opera_stars & (1 << act_index)) != 0
		var pearl := button.get_node_or_null("CareerPearl") as Panel
		if pearl != null:
			pearl.set_meta("complete", complete)
			pearl.add_theme_stylebox_override("panel", StorybookUI.panel_style(
				StorybookUI.GOLD if complete else StorybookUI.LAVENDER,
				Color(1.0, 0.94, 0.58, 1.0) if complete \
				else Color(0.88, 0.90, 1.0, 0.96), 18, 3))


func _highlight(act_index: int) -> void:
	if highlighted_act == act_index or active_animator == null \
		or not is_instance_valid(active_animator):
		return
	_stop_animator()
	var button := button_for_act(act_index)
	if button == null:
		return
	if String(button.get_meta("presentation", "")) \
			== "historical_three_floor_portal":
		highlighted_act = act_index
		return
	var actor := button.get_node_or_null("RoshanActor") as TextureRect
	if actor == null:
		return
	highlighted_act = act_index
	active_animator.setup(
		actor, String(button.get_meta("career_costume", "")), actor.texture)


func _stop_animator() -> void:
	highlighted_act = -1
	if active_animator != null and is_instance_valid(active_animator):
		active_animator.stop()
		active_animator.setup(null, "", null)


func _launch(expected_room: String, act_index: int) -> void:
	if m.day_one_jobs_locked() \
		or m.castle_room_id != expected_room \
		or not route_matches(expected_room, act_index) \
		or m.opera_game != null:
		return
	m._start_opera_from_room(act_index, expected_room)


func open_opera_venue() -> bool:
	if m.day_one_jobs_locked() or m.castle_room_id != "opera_hall":
		return false
	sync()
	if opera_venue == null or not is_instance_valid(opera_venue):
		return false
	opera_venue.open(m.opera_stars)
	root.visible = true
	return true


func close_opera_venue() -> void:
	if opera_venue != null and is_instance_valid(opera_venue):
		opera_venue.close()


func _launch_opera_venue(act_index: int) -> void:
	_launch("opera_hall", act_index)
