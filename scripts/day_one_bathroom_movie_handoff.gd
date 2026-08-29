class_name DayOneBathroomMovieHandoff
extends Control
## Optional two-phase movie seam for the Day One bathroom rescue.
##
## The entry movie plays over the already-built dirty bathroom before the
## basket lesson. The cleanup movie plays over the final clean room before the
## pool route appears. Neither movie is delivered by this change: an absent or
## invalid stream fails open to the matching playable room state. A real stream
## commits its phase-specific once-only marker before playback.

signal handoff_finished(phase: String, status: String)

const PHASE_ENTRY: String = "entry"
const PHASE_CLEANUP: String = "cleanup"
const DEFAULT_ENTRY_MOVIE_PATH: String = \
	"res://assets/cinematics/day_one_bathroom_entry.ogv"
const DEFAULT_CLEANUP_MOVIE_PATH: String = \
	"res://assets/cinematics/day_one_bathroom_cleaned.ogv"
const ENTRY_SAVE_KEY: String = "day_one_bathroom_entry_movie_handoff_done"
const CLEANUP_SAVE_KEY: String = "day_one_bathroom_end_movie_handoff_done"
# Compatibility aliases for callers and save files built against the original
# single completion-movie seam.
const DEFAULT_MOVIE_PATH: String = DEFAULT_CLEANUP_MOVIE_PATH
const HANDOFF_SAVE_KEY: String = CLEANUP_SAVE_KEY

var m: ReefMain = null
var phase: String = PHASE_CLEANUP
var movie_path: String = DEFAULT_CLEANUP_MOVIE_PATH
var playback_count: int = 0
var fallback_count: int = 0
var _handoff_done: bool = false
var _last_status: String = "not_started"
var _player: VideoStreamPlayer = null
var _save_writer: Callable = Callable()


static func normalise_phase(phase_value: String) -> String:
	return PHASE_ENTRY if phase_value.strip_edges().to_lower() == PHASE_ENTRY \
		else PHASE_CLEANUP


static func default_movie_path(phase_value: String) -> String:
	return DEFAULT_ENTRY_MOVIE_PATH \
		if normalise_phase(phase_value) == PHASE_ENTRY \
		else DEFAULT_CLEANUP_MOVIE_PATH


static func save_key_for_phase(phase_value: String) -> String:
	return ENTRY_SAVE_KEY if normalise_phase(phase_value) == PHASE_ENTRY \
		else CLEANUP_SAVE_KEY


static func normalise_movie_path(path_override: String,
		phase_value: String = PHASE_CLEANUP) -> String:
	var candidate: String = path_override.strip_edges()
	return default_movie_path(phase_value) if candidate.is_empty() else candidate


static func is_movie_candidate_path(path_value: String) -> bool:
	var candidate: String = path_value.strip_edges().to_lower()
	return candidate.ends_with(".ogv")


func setup(main: ReefMain, phase_value: String = PHASE_CLEANUP,
		path_override: String = "") -> void:
	m = main
	phase = normalise_phase(phase_value)
	movie_path = normalise_movie_path(path_override, phase)
	name = "DayOneBathroom%sMovieHandoff" % phase.capitalize()
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	focus_mode = Control.FOCUS_NONE
	z_index = 60
	visible = false


## Tests may inject a deterministic writer. Runtime callers leave this unset,
## which uses ReefMain's transactional _write_save() path.
func set_save_writer(writer: Callable) -> void:
	_save_writer = writer


func start() -> Dictionary:
	return start_before_cleanup() if phase == PHASE_ENTRY \
		else start_after_completion()


## Entry is valid only while Day One still owns the unfinished bathroom. A
## present movie receives a save-before-play marker; an absent movie does not
## poison future saves before the authored cinematic is installed.
func start_before_cleanup() -> Dictionary:
	if m == null or not m.day_one_is_active():
		return _result("not_ready", false)
	var director: DayOneDirector = m._day_one_ref()
	if director.current_room_id != "bathroom" \
			or director.is_room_completed("bathroom"):
		return _result("wrong_state", false)
	return _start_validated()


## Called only after day_one_complete_bathroom_scene() returns true. Completion
## has already been committed before this seam is entered.
func start_after_completion() -> Dictionary:
	if m == null:
		return _result("not_ready", false)
	if not m._day_one_ref().is_room_completed("bathroom"):
		return _result("not_completed", false)
	return _start_validated()


func stop() -> void:
	if _player != null and is_instance_valid(_player):
		_player.stop()
		_player.queue_free()
	_player = null
	visible = false
	if _last_status == "playing":
		_last_status = "finished"
		handoff_finished.emit(phase, _last_status)


func audit_snapshot() -> Dictionary:
	return {
		"phase": phase,
		"movie_path": movie_path,
		"movie_candidate_path": is_movie_candidate_path(movie_path),
		"save_key": save_key_for_phase(phase),
		"handoff_done": _handoff_done,
		"last_status": _last_status,
		"playback_count": playback_count,
		"fallback_count": fallback_count,
		"player_active": _player != null and is_instance_valid(_player),
		"modal_input_blocker": mouse_filter == Control.MOUSE_FILTER_STOP,
		"full_frame_overlay": anchors_preset == Control.PRESET_FULL_RECT,
		"seamless_dirty_scene_cut": phase == PHASE_ENTRY,
		"seamless_clean_scene_cut": phase == PHASE_CLEANUP,
		"canvas_only": _all_canvas_children(self),
	}


func _start_validated() -> Dictionary:
	if _handoff_done or bool(m.save_data.get(save_key_for_phase(phase), false)):
		_handoff_done = true
		return _result("already_done", true)
	var stream: VideoStream = _load_movie_stream()
	if stream == null:
		# This instance will not retry every frame. The absence is deliberately
		# not serialized, allowing an authored movie added to a later build to
		# remain eligible for a Day One save that never actually played it.
		_handoff_done = true
		fallback_count += 1
		return _result("fallback", true)
	# A failed earlier write leaves main dirty. Retry it before adding the
	# phase-specific once-only marker, then refuse playback if it still fails.
	if m.save_dirty and not _flush_save():
		return _result("save_pending", false)
	var save_key: String = save_key_for_phase(phase)
	var previous_marker: Variant = m.save_data.get(save_key, null)
	m.save_data[save_key] = true
	if not _flush_save():
		if previous_marker == null:
			m.save_data.erase(save_key)
		else:
			m.save_data[save_key] = previous_marker
		return _result("save_pending", false)
	_handoff_done = true
	_play(stream)
	return _result("playing", true)


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
	_player.name = "DayOneBathroom%sMovie" % phase.capitalize()
	_player.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_player.mouse_filter = Control.MOUSE_FILTER_STOP
	_player.expand = true
	_player.stream = stream
	_player.finished.connect(stop, CONNECT_ONE_SHOT)
	add_child(_player)
	_player.play()
	playback_count += 1
	_last_status = "playing"


func _result(status: String, completion_committed: bool) -> Dictionary:
	_last_status = status
	return {
		"phase": phase,
		"status": status,
		"completion_committed": completion_committed,
		"movie_path": movie_path,
		"save_key": save_key_for_phase(phase),
		"playback_count": playback_count,
		"fallback_count": fallback_count,
	}


func _all_canvas_children(node: Node) -> bool:
	for child: Node in node.get_children():
		if not child is CanvasItem or not _all_canvas_children(child):
			return false
	return true
