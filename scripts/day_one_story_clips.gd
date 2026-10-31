class_name DayOneStoryClips
extends Control
## Day One story clips between gameplay scenes (owner decision 2026-09-23,
## DL-CIN-16). Each clip is a straight cut from the owner-selected 2026-09-20
## cut; the manifest is written by tools/build_day_one_story_clips.py. Clips
## never alter progression: a missing clip fails open to the existing scene.

signal finished(movie_id: String, status: String)

const MANIFEST_PATH: String = "res://assets/cinematics/day_one_story/story_clips.json"
const CLIP_ROOT: String = "res://assets/cinematics/day_one_story/"
const TIMEOUT_MARGIN_S: float = 8.0
const DOUBLE_TAP_MS: int = 450
const MAX_TAP_MS: int = 350
const TAP_MOTION_PX: float = 24.0
const DOUBLE_TAP_DISTANCE_PX: float = 80.0

## Headless probes stay deterministic unless a probe opts in to real playback.
static var headless_override: bool = false

var movie_id: String = ""
var player: VideoStreamPlayer = null
var _finished: bool = false
var _previous_paused: bool = false
var _pause_owned: bool = false
var _timeout: Timer = null
var _pointer_contacts: Dictionary = {}
var _tap_contact: int = -2
var _tap_origin: Vector2 = Vector2.ZERO
var _tap_started_ms: int = 0
var _tap_valid: bool = false
var _last_tap_ms: int = -1
var _last_tap_position: Vector2 = Vector2.ZERO
var _last_tap_was_mouse: bool = false
var _skip_input_suspended: bool = false

func _scene_tree() -> SceneTree:
	return Engine.get_main_loop() as SceneTree

static func enabled() -> bool:
	return DisplayServer.get_name() != "headless" or headless_override

static func clip_ids() -> Array[String]:
	var ids: Array[String] = []
	for key: Variant in _clips().keys():
		ids.append(String(key))
	return ids

static func path_for(id: String) -> String:
	var row: Variant = _clips().get(id, {})
	if not row is Dictionary:
		return ""
	var declared: String = String((row as Dictionary).get("path", ""))
	if not declared.begins_with(CLIP_ROOT) or declared.contains("..") \
			or not declared.ends_with(".ogv"):
		return ""
	return declared

static func seconds_for(id: String) -> float:
	var row: Variant = _clips().get(id, {})
	return float((row as Dictionary).get("seconds", 0.0)) if row is Dictionary else 0.0

static func available(id: String) -> bool:
	var path: String = path_for(id)
	return not path.is_empty() and ResourceLoader.exists(path)

static func _clips() -> Dictionary:
	var file: FileAccess = FileAccess.open(MANIFEST_PATH, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary:
		return {}
	var clips: Variant = (parsed as Dictionary).get("clips", {})
	return clips as Dictionary if clips is Dictionary else {}

func setup(id: String) -> bool:
	movie_id = id.strip_edges()
	if not enabled() or not available(movie_id):
		return false
	var resource: Resource = load(path_for(movie_id)) as Resource
	if not resource is VideoStream:
		return false
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	# Single taps stay on the movie. Two short taps skip on the second release;
	# the game-wide Back control remains available above this overlay.
	mouse_filter = Control.MOUSE_FILTER_STOP
	process_mode = Node.PROCESS_MODE_ALWAYS
	z_index = 70
	var black: ColorRect = ColorRect.new()
	black.color = Color.BLACK
	black.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	black.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(black)
	var aspect: AspectRatioContainer = AspectRatioContainer.new()
	aspect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	aspect.ratio = 16.0 / 9.0
	aspect.stretch_mode = AspectRatioContainer.STRETCH_FIT
	aspect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(aspect)
	player = VideoStreamPlayer.new()
	player.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	player.expand = true
	player.mouse_filter = Control.MOUSE_FILTER_IGNORE
	player.stream = resource as VideoStream
	player.finished.connect(_finish.bind("finished"), CONNECT_ONE_SHOT)
	aspect.add_child(player)
	_timeout = Timer.new()
	_timeout.one_shot = true
	_timeout.wait_time = maxf(seconds_for(movie_id), 1.0) + TIMEOUT_MARGIN_S
	_timeout.process_mode = Node.PROCESS_MODE_ALWAYS
	_timeout.timeout.connect(_finish.bind("timeout"), CONNECT_ONE_SHOT)
	add_child(_timeout)
	var tree: SceneTree = _scene_tree()
	if tree == null:
		return false
	_previous_paused = tree.paused
	tree.paused = true
	_pause_owned = true
	call_deferred("_start_playback")
	return true

func _start_playback() -> void:
	if not _finished and player != null and is_instance_valid(player):
		player.play()
		if _timeout != null:
			_timeout.start()

func _pointer_time_ms() -> int:
	return Time.get_ticks_msec()

func _input(event: InputEvent) -> void:
	if _finished or _skip_input_suspended or player == null:
		return
	# Android sends a mouse event for the same touch. Count that gesture once.
	if event.device == InputEvent.DEVICE_ID_EMULATION:
		return
	if event is InputEventScreenTouch:
		var touch: InputEventScreenTouch = event as InputEventScreenTouch
		if touch.canceled:
			_reset_skip_input()
		elif touch.pressed:
			_pointer_pressed(touch.index, touch.position)
		else:
			_pointer_released(touch.index, touch.position)
	elif event is InputEventScreenDrag:
		var drag: InputEventScreenDrag = event as InputEventScreenDrag
		_pointer_moved(drag.index, drag.position)
	elif event is InputEventMouseButton:
		var mouse: InputEventMouseButton = event as InputEventMouseButton
		if mouse.button_index == MOUSE_BUTTON_LEFT:
			if mouse.pressed:
				_pointer_pressed(-1, mouse.position)
			else:
				_pointer_released(-1, mouse.position)
	elif event is InputEventMouseMotion:
		_pointer_moved(-1, (event as InputEventMouseMotion).position)

func _pointer_pressed(contact: int, position: Vector2) -> void:
	_pointer_contacts[contact] = true
	if _pointer_contacts.size() != 1:
		_tap_valid = false
		_last_tap_ms = -1
		return
	_tap_contact = contact
	_tap_origin = position
	_tap_started_ms = _pointer_time_ms()
	_tap_valid = true

func _pointer_moved(contact: int, position: Vector2) -> void:
	if _tap_valid and contact == _tap_contact \
			and position.distance_to(_tap_origin) > TAP_MOTION_PX:
		_tap_valid = false
		_last_tap_ms = -1

func _pointer_released(contact: int, position: Vector2) -> void:
	var now: int = _pointer_time_ms()
	var valid: bool = _tap_valid and contact == _tap_contact \
		and _pointer_contacts.size() == 1 \
		and now - _tap_started_ms <= MAX_TAP_MS \
		and position.distance_to(_tap_origin) <= TAP_MOTION_PX
	_pointer_contacts.erase(contact)
	_tap_valid = false
	if not valid:
		_last_tap_ms = -1
		return
	var mouse: bool = contact == -1
	if _last_tap_ms >= 0 and now - _last_tap_ms <= DOUBLE_TAP_MS \
			and mouse == _last_tap_was_mouse \
			and position.distance_to(_last_tap_position) <= DOUBLE_TAP_DISTANCE_PX:
		# Consume the release before the finish callback restores gameplay.
		get_viewport().set_input_as_handled()
		skip()
		return
	_last_tap_ms = now
	_last_tap_position = position
	_last_tap_was_mouse = mouse

func _reset_skip_input() -> void:
	_pointer_contacts.clear()
	_tap_valid = false
	_last_tap_ms = -1

func _notification(what: int) -> void:
	# Hold the story while the app is away so none of it is missed.
	if player == null or not is_instance_valid(player) or _finished:
		return
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT \
			or what == NOTIFICATION_APPLICATION_PAUSED:
		_reset_skip_input()
		_skip_input_suspended = true
		player.paused = true
		if _timeout != null:
			_timeout.paused = true
	elif what == NOTIFICATION_APPLICATION_FOCUS_IN \
			or what == NOTIFICATION_APPLICATION_RESUMED:
		_reset_skip_input()
		_skip_input_suspended = false
		player.paused = false
		if _timeout != null:
			_timeout.paused = false

func skip() -> void:
	_finish("skipped")

func _exit_tree() -> void:
	_reset_skip_input()
	var tree: SceneTree = _scene_tree()
	if _pause_owned and tree != null:
		tree.paused = _previous_paused
		_pause_owned = false

func _finish(status: String) -> void:
	if _finished:
		return
	_finished = true
	_reset_skip_input()
	if player != null and is_instance_valid(player):
		player.stop()
	if _timeout != null and is_instance_valid(_timeout):
		_timeout.stop()
	var tree: SceneTree = _scene_tree()
	if _pause_owned and tree != null:
		tree.paused = _previous_paused
		_pause_owned = false
	finished.emit(movie_id, status)
	queue_free()
