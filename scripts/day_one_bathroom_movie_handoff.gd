class_name DayOneBathroomMovieHandoff
extends Control
## Optional end-movie seam for the Day One bathroom rescue.
##
## The movie is deliberately not part of this change. A future full-frame
## VideoStream can be installed at DEFAULT_MOVIE_PATH, or supplied through
## setup(). The final clean room remains underneath the player, so an absent
## or invalid movie is a harmless no-op rather than a new failure state.

const DEFAULT_MOVIE_PATH: String = \
	"res://assets/cinematics/day_one_bathroom_finale.webm"
const HANDOFF_SAVE_KEY: String = "day_one_bathroom_end_movie_handoff_done"

var m: ReefMain = null
var movie_path: String = DEFAULT_MOVIE_PATH
var playback_count: int = 0
var fallback_count: int = 0
var _handoff_done: bool = false
var _player: VideoStreamPlayer = null
var _save_writer: Callable = Callable()


static func normalise_movie_path(path_override: String) -> String:
	var candidate: String = path_override.strip_edges()
	return DEFAULT_MOVIE_PATH if candidate.is_empty() else candidate


static func is_movie_candidate_path(path_value: String) -> bool:
	var candidate: String = path_value.strip_edges().to_lower()
	return candidate.ends_with(".webm") or candidate.ends_with(".ogv") \
		or candidate.ends_with(".mp4")


func setup(main: ReefMain, path_override: String = "") -> void:
	m = main
	movie_path = normalise_movie_path(path_override)
	name = "DayOneBathroomMovieHandoff"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	focus_mode = Control.FOCUS_NONE
	visible = false


## Tests may inject a deterministic writer. Runtime callers leave this unset,
## which uses ReefMain's transactional _write_save() path.
func set_save_writer(writer: Callable) -> void:
	_save_writer = writer


## Called only after day_one_complete_bathroom_scene() returns true. The saved
## marker is committed before the player is created, making Continue a strict
## no-replay path even when the movie finishes after a scene transition.
func start_after_completion() -> Dictionary:
	if m == null:
		return _result("not_ready", false)
	if not m._day_one_ref().is_room_completed("bathroom"):
		return _result("not_completed", false)
	if _handoff_done or bool(m.save_data.get(HANDOFF_SAVE_KEY, false)):
		_handoff_done = true
		return _result("already_done", true)
	# A failed completion write leaves main dirty. Retry that transaction before
	# adding the once-only handoff marker, then refuse playback if it still fails.
	if m.save_dirty and not _flush_save():
		return _result("save_pending", false)
	var previous_marker: Variant = m.save_data.get(HANDOFF_SAVE_KEY, null)
	m.save_data[HANDOFF_SAVE_KEY] = true
	if not _flush_save():
		if previous_marker == null:
			m.save_data.erase(HANDOFF_SAVE_KEY)
		else:
			m.save_data[HANDOFF_SAVE_KEY] = previous_marker
		return _result("save_pending", false)
	_handoff_done = true
	var stream: VideoStream = _load_movie_stream()
	if stream == null:
		fallback_count += 1
		return _result("fallback", true)
	_play(stream)
	return _result("playing", true)


func stop() -> void:
	if _player != null and is_instance_valid(_player):
		_player.stop()
		_player.queue_free()
	_player = null
	visible = false


func audit_snapshot() -> Dictionary:
	return {
		"movie_path": movie_path,
		"movie_candidate_path": is_movie_candidate_path(movie_path),
		"handoff_done": _handoff_done,
		"playback_count": playback_count,
		"fallback_count": fallback_count,
		"player_active": _player != null and is_instance_valid(_player),
		"canvas_only": _all_canvas_children(self),
	}


func _flush_save() -> bool:
	if _save_writer.is_valid():
		return bool(_save_writer.call())
	return m._write_save()


func _load_movie_stream() -> VideoStream:
	if not is_movie_candidate_path(movie_path) \
		or not ResourceLoader.exists(movie_path):
		return null
	var resource: Resource = load(movie_path) as Resource
	return resource as VideoStream


func _play(stream: VideoStream) -> void:
	visible = true
	_player = VideoStreamPlayer.new()
	_player.name = "DayOneBathroomEndMovie"
	_player.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_player.mouse_filter = Control.MOUSE_FILTER_STOP
	_player.expand = true
	_player.stream = stream
	_player.finished.connect(_on_movie_finished, CONNECT_ONE_SHOT)
	add_child(_player)
	_player.play()
	playback_count += 1


func _on_movie_finished() -> void:
	stop()


func _result(status: String, completion_committed: bool) -> Dictionary:
	return {
		"status": status,
		"completion_committed": completion_committed,
		"movie_path": movie_path,
		"playback_count": playback_count,
		"fallback_count": fallback_count,
	}


func _all_canvas_children(node: Node) -> bool:
	for child: Node in node.get_children():
		if not child is CanvasItem or not _all_canvas_children(child):
			return false
	return true
