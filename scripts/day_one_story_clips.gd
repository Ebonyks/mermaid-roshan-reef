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

## Headless probes stay deterministic unless a probe opts in to real playback.
static var headless_override: bool = false

var movie_id: String = ""
var player: VideoStreamPlayer = null
var _finished: bool = false
var _previous_paused: bool = false
var _pause_owned: bool = false
var _timeout: Timer = null

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
	# Taps are swallowed so a stray touch can never skip the story; the
	# game-wide Back control is the one skip route (see ReefMain).
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

func _notification(what: int) -> void:
	# Hold the story while the app is away so none of it is missed.
	if player == null or not is_instance_valid(player) or _finished:
		return
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT \
			or what == NOTIFICATION_APPLICATION_PAUSED:
		player.paused = true
		if _timeout != null:
			_timeout.paused = true
	elif what == NOTIFICATION_APPLICATION_FOCUS_IN \
			or what == NOTIFICATION_APPLICATION_RESUMED:
		player.paused = false
		if _timeout != null:
			_timeout.paused = false

func skip() -> void:
	_finish("skipped")

func _exit_tree() -> void:
	var tree: SceneTree = _scene_tree()
	if _pause_owned and tree != null:
		tree.paused = _previous_paused
		_pause_owned = false

func _finish(status: String) -> void:
	if _finished:
		return
	_finished = true
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
