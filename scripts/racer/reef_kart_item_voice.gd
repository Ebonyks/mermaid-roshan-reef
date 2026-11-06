extends AudioStreamPlayer
## Standalone PC speech lane. The embedded career uses its shared AudioDirector.
## One bounded FIFO for both players; no camera copy owns another voice player.

const ROOT := "res://assets/audio/objective_guides/guide_kart_"
const KINDS := ["zoom", "sparkle", "kelp", "pearls"]
var duel := false
var pending: Array[Dictionary] = []
var active: Dictionary = {}
var starts: Array[Dictionary] = []
var _mix_restore: Dictionary = {}

func _ready() -> void:
	if AudioServer.get_bus_index("Voice") >= 0:
		bus = "Voice"
	finished.connect(_next)

func award(slot: int, kind: String) -> void:
	if kind not in KINDS:
		return
	# A player can hold only one item; keep the latest waiting award per slot.
	for index in range(pending.size() - 1, -1, -1):
		if int(pending[index]["slot"]) == slot:
			pending.remove_at(index)
	pending.append({"slot": slot, "kind": kind})
	if not playing:
		_next()

func _next() -> void:
	if pending.is_empty():
		active.clear()
		_restore_mix()
		return
	active = pending.pop_front()
	var key := String(active["kind"])
	if duel and key == "sparkle":
		key = "sparkle_duel"
	stream = load(ROOT + key + ".ogg") as AudioStream
	if stream == null:
		clear()
		return
	for name: String in ["Music", "Ambience"]:
		var index := AudioServer.get_bus_index(name)
		if index < 0:
			continue
		if not _mix_restore.has(name):
			_mix_restore[name] = AudioServer.get_bus_volume_db(index)
		AudioServer.set_bus_volume_db(index, minf(float(_mix_restore[name]), -14.0 if name == "Music" else -16.0))
	starts.append(active.duplicate())
	if starts.size() > 16:
		starts.pop_front()
	play()

func skip() -> void:
	stop()
	_next()

func clear() -> void:
	stop()
	stream = null
	pending.clear()
	active.clear()
	_restore_mix()

func _restore_mix() -> void:
	for name: String in _mix_restore:
		var index := AudioServer.get_bus_index(name)
		if index >= 0 and AudioServer.get_bus_volume_db(index) > -60.0:
			AudioServer.set_bus_volume_db(index, float(_mix_restore[name]))
	_mix_restore.clear()

func _notification(what: int) -> void:
	if what in [NOTIFICATION_PAUSED, NOTIFICATION_APPLICATION_PAUSED,
			NOTIFICATION_APPLICATION_FOCUS_OUT, NOTIFICATION_EXIT_TREE]:
		clear()
