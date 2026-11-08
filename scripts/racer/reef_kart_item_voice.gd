extends AudioStreamPlayer
## Standalone PC speech lane. The embedded career uses its shared AudioDirector.
## One bounded FIFO for both players; no camera copy owns another voice player.

const ROOT := "res://assets/audio/objective_guides/guide_kart_"
const KINDS := ["zoom", "sparkle", "kelp", "pearls"]
const SHARED_SLOT := -1
const SEAT_PAN := [-0.65, 0.65]
var duel := false
var pending: Array[Dictionary] = []
var active: Dictionary = {}
var starts: Array[Dictionary] = []
var _mix_restore: Dictionary = {}
var _seat_bus: StringName
var _panner: AudioEffectPanner

func _ready() -> void:
	if AudioServer.get_bus_index("Voice") >= 0:
		bus = "Voice"
	if duel:
		# A private bus gives the shared speech queue stereo position while
		# retaining the existing Voice volume, mute, and mix controls.
		var voice_bus := bus
		var index := AudioServer.bus_count
		AudioServer.add_bus()
		_seat_bus = StringName("ReefKartVoice_%d" % get_instance_id())
		AudioServer.set_bus_name(index, _seat_bus)
		AudioServer.set_bus_send(index, voice_bus)
		_panner = AudioEffectPanner.new()
		AudioServer.add_bus_effect(index, _panner)
		bus = _seat_bus
	finished.connect(_next)

func award(slot: int, kind: String) -> void:
	if kind not in KINDS or slot < SHARED_SLOT or slot >= SEAT_PAN.size():
		return
	discard_pending(slot)
	pending.append({"slot": slot, "kind": kind})
	if not playing:
		_next()

func discard_pending(slot: int) -> void:
	# A player can hold only one item. A spent or replaced award is obsolete.
	for index in range(pending.size() - 1, -1, -1):
		if int(pending[index]["slot"]) == slot:
			pending.remove_at(index)

func _next() -> void:
	if pending.is_empty():
		active.clear()
		_restore_mix()
		return
	active = pending.pop_front()
	var slot := int(active["slot"])
	if _panner != null:
		var pan: float = 0.0 if slot == SHARED_SLOT else SEAT_PAN[slot]
		_panner.pan = pan
		# The panner boosts the near channel. Keep that channel at the
		# recorded voice level and leave the opposite channel audible.
		volume_db = -linear_to_db(1.0 + absf(pan))
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

func skip(slot: int) -> void:
	discard_pending(slot)
	if not active.is_empty() and int(active["slot"]) in [slot, SHARED_SLOT]:
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
	if what == NOTIFICATION_EXIT_TREE and _panner != null:
		var index := AudioServer.get_bus_index(_seat_bus)
		if index >= 0:
			bus = AudioServer.get_bus_send(index)
			AudioServer.remove_bus(index)
		_panner = null
