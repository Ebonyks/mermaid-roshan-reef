class_name DayOneDraftMovies
extends Control
## Opt-in DaVinci/Grok review movies. Drafts never alter progression or claims.

signal finished(movie_id: String, status: String)

const ROOT: String = "res://assets_src/cinematics/day_one_davinci_draft_2026-09-04/exports/"
const MANIFEST_PATH: String = "res://assets_src/cinematics/day_one_davinci_draft_2026-09-04/runtime_manifest.json"
const MOVIE_IDS: Array[String] = [
	"D1-C00", "D1-C01", "D1-C02", "D1-C03", "D1-C04", "D1-C05", "D1-C06",
	"D1-C07", "D1-C08", "D1-C09", "D1-C10", "D1-C11", "D1-C12", "D1-C13",
]

var movie_id: String = ""
var player: VideoStreamPlayer = null
var skip_button: Button = null
var _finished: bool = false
var _previous_paused: bool = false
var _pause_owned: bool = false
var _timeout: Timer = null

func _scene_tree() -> SceneTree:
	return Engine.get_main_loop() as SceneTree

static func enabled() -> bool:
	var args: PackedStringArray = OS.get_cmdline_args()
	var user_args: PackedStringArray = OS.get_cmdline_user_args()
	return "--day-one-draft-movies" in args or "--day-one-draft-movies" in user_args

static func path_for(id: String) -> String:
	if id not in MOVIE_IDS:
		return ""
	var row: Dictionary = _manifest_row(id)
	var declared: String = String(row.get("path", "exports/%s.ogv" % id))
	if declared.is_empty() or declared.begins_with("/") \
			or declared.contains("..") or not declared.begins_with("exports/"):
		return ""
	return "res://assets_src/cinematics/day_one_davinci_draft_2026-09-04/" + declared

static func _manifest_row(id: String) -> Dictionary:
	var file: FileAccess = FileAccess.open(MANIFEST_PATH, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary:
		return {}
	var movies: Variant = (parsed as Dictionary).get("movies", {})
	if not movies is Dictionary:
		return {}
	var row: Variant = (movies as Dictionary).get(id, {})
	return row as Dictionary if row is Dictionary else {}

static func runtime_preview_eligible(id: String) -> bool:
	var row: Dictionary = _manifest_row(id)
	var path: String = path_for(id)
	return bool(row.get("runtime_preview_eligible", false)) \
		and not path.is_empty() and ResourceLoader.exists(path)

func setup(id: String) -> bool:
	movie_id = id.strip_edges().to_upper()
	if not enabled() or not runtime_preview_eligible(movie_id) \
			or path_for(movie_id).is_empty() \
			or not ResourceLoader.exists(path_for(movie_id)):
		return false
	var resource: Resource = load(path_for(movie_id)) as Resource
	if not resource is VideoStream:
		return false
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
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
	# Full-frame transparent tap target: review clips must always be escapable.
	skip_button = Button.new()
	skip_button.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	skip_button.flat = true
	skip_button.focus_mode = Control.FOCUS_NONE
	skip_button.mouse_default_cursor_shape = Control.CURSOR_ARROW
	skip_button.modulate.a = 0.01
	skip_button.process_mode = Node.PROCESS_MODE_ALWAYS
	skip_button.pressed.connect(skip)
	add_child(skip_button)
	_timeout = Timer.new()
	_timeout.one_shot = true
	_timeout.wait_time = 120.0
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
