class_name MicInput
extends RefCounted
# Spoken spells (PROTOTYPE, 2026-08-02). Speaker-dependent DTW over a 20-band
# log-mel spectrogram: no ASR, no model file, no native binary, no network.
#
# Front end is free — Godot's own AudioEffectSpectrumAnalyzer already runs an
# FFT in C++ on the muted "Mic" bus, so this script only reads 20 mel-spaced
# magnitudes per frame. That is deliberately more than a two-band energy test:
# the stored template is a time x frequency shape, so it carries syllable
# count and formant movement. "Freeze" (one syllable, sibilant tail) and
# "fireball" (three syllables) separate easily even though both open on /f/.
#
# Speaker dependence is a FEATURE here, not a compromise: there is exactly one
# player, and the family already records her voice into assets/audio/voices/.
# Enrollment is five spoken samples per word, kept in user://mic_spells.json,
# never in reef_save.json.
#
# Phase 7 satellite rules: everything the rest of the game or the save file can
# observe lives on main (m.mic_on, m.mic_state, m.mic_last_word, ...). Only the
# DSP scratch and the enrolled templates are private here — the same division
# SaveState uses for its own file-handling mechanism.
#
# NO FAIL STATE: an unheard, rejected or ambiguous word does nothing at all.
# The ICE/FIRE buttons stay live the whole time and remain the primary control;
# the microphone is only ever an extra way to do what a tap already does.

const BANDS := 20               # mel filterbank width
const F_LO := 80.0
const F_HI := 8000.0
const NORM_FRAMES := 32         # every utterance is resampled to this length,
                                # so recognition is frame-rate independent
const DTW_BAND := 8             # Sakoe-Chiba radius, in normalised frames
const RAW_MIN_FRAMES := 6       # shorter than this is a cough, not a word
const RAW_MAX_FRAMES := 120     # hard cap; MAX_SECONDS normally ends it first
const MAX_SECONDS := 1.6
const MIN_SECONDS := 0.15
const PREROLL := 4              # frames kept before onset so /f/ is not clipped
const START_MARGIN_DB := 12.0   # above the rolling noise floor to open a word
const END_MARGIN_DB := 6.0      # ...and to close it again
const START_HOLD := 3
const END_HOLD := 15
const FLOOR_RISE := 0.08        # the floor climbs quickly (music starting up)
const FLOOR_FALL := 0.02        # ...and falls slowly, so it cannot chase a word
const SELF_AUDIO_TAIL := 0.25   # deaf for this long after our own voice lines
const TEMPLATES_PER_WORD := 5
const DUR_WEIGHT := 0.15        # duration is a weak extra cue after resampling
const TEMPLATE_PATH := "user://mic_spells.json"
const TEMPLATE_VERSION := 1
const MAX_PERMISSION_ASKS := 2  # never nag a four-year-old's phone
# The decision rule. ACCEPT_RATIO does the real work and ACCEPT_DIST is only a
# sanity ceiling — that split is measured, not guessed (tools/dtw_calib.py):
#
#   same word, clean ............ distance 0.06        ratio 0.16-0.18
#   same word, sloppy delivery .. distance 0.09-0.14   ratio 0.23-0.50
#   same word, very noisy ....... distance 0.21-0.26   ratio 0.47-0.55
#   ambiguous half-word ......... distance 0.28-0.30   ratio 0.65-0.67
#   room noise .................. distance 0.34-0.46   ratio 0.69-0.90
#
# Absolute distance does NOT separate those classes: room noise reaches down to
# 0.34 while a genuine but noisy word reaches up to 0.26, and both drift with
# loudness and room colour, so any ceiling that accepts the word also accepts
# some of the noise. The RATIO of best to runner-up does separate them and is
# scale-invariant: a real word is close to one template family and far from the
# other, while noise is equally far from both. So the ratio decides, and the
# ceiling only catches the degenerate case where a single word is enrolled and
# there is no runner-up to compare against.
const ACCEPT_DIST := 0.45
const ACCEPT_RATIO := 0.60
const WORDS: Array[String] = ["ice", "fire"]
const WORD_GLYPH := {"ice": "❄", "fire": "🔥"}
const WORD_PROMPT := {
	"ice": "Say  FREEZE!",
	"fire": "Say  FIREBALL!",
}

var m: ReefMain

# --- audio plumbing -----------------------------------------------------
var _bus_idx := -1
var _player: AudioStreamPlayer = null
var _analyzer: AudioEffectSpectrumAnalyzerInstance = null
var _edges := PackedFloat32Array()
var _ask_count := 0

# --- capture / endpointing ---------------------------------------------
var _frame := PackedFloat32Array()      # the current normalised feature vector
var _frame_db := -120.0
var _floor_db := -60.0
var _floor_seeded := false
var _hot := 0
var _cold := 0
var _speaking := false
var _self_audio_t := 0.0
var _raw: Array = []                    # Array[PackedFloat32Array] this word
var _raw_t := 0.0
var _preroll: Array = []                # Array[PackedFloat32Array] ring

# --- templates / matching ----------------------------------------------
var _templates := {}                    # word -> Array[Dictionary]
var _loaded := false
var _dtw_cost := PackedFloat32Array()
var _query := PackedFloat32Array()
var _pending := ""                      # one recognised word, waiting on poll

# --- enrollment ---------------------------------------------------------
var _enroll_word := ""
var _enroll_left := 0
var _teach_queue: Array[String] = []
var _teach_pips: Array = []
var _teach_glyph: Label = null
var _teach_prompt: Label = null


func _init(main: ReefMain) -> void:
	m = main
	_frame.resize(BANDS)
	_query.resize(NORM_FRAMES * BANDS)
	_dtw_cost.resize(NORM_FRAMES * NORM_FRAMES)
	_build_mel_edges()


# ===================== PUBLIC API =====================

# Called when an activity that understands spoken spells begins. This is the
# ONLY place the microphone device is opened — never at boot, so a child who
# never enters combat is never recorded and never sees a permission dialog.
func arm() -> void:
	if not m.mic_on or m.mic_permission_denied:
		m.mic_state = "off"
		return
	_load_templates()
	if _is_headless():
		m.mic_state = "test"     # probes push utterances in directly
		return
	if not _ensure_permission():
		return
	_ensure_bus()
	_ensure_player()
	if _player != null and not _player.playing:
		_player.play()
	_reset_capture()
	m.mic_state = "enroll" if _enroll_left > 0 else "listening"


# Closes the capture device. Called on every arena exit, so the audio HAL is
# only awake while a battle is actually running.
func disarm() -> void:
	if _player != null and _player.playing:
		_player.stop()
	_analyzer = null
	_reset_capture()
	_pending = ""
	if m.mic_state != "off":
		m.mic_state = "idle"


# Returns a recognised spell word once, then forgets it. "" means nothing was
# heard — which is the overwhelmingly common case and must stay harmless.
func poll_word() -> String:
	var word := _pending
	_pending = ""
	return word


func has_templates(word: String) -> bool:
	_load_templates()
	var list: Array = _templates.get(word, [])
	return list.size() >= 2


func all_words_taught() -> bool:
	for w: String in WORDS:
		if not has_templates(w):
			return false
	return true


func tick(delta: float) -> void:
	if m.mic_state == "off" or m.mic_state == "idle":
		return
	_self_audio_t = maxf(0.0, _self_audio_t - delta)
	if _game_audio_playing():
		_self_audio_t = SELF_AUDIO_TAIL
	if m.mic_state == "test":
		return                      # probe-driven; no device, no analyzer
	if not _read_frame():
		return
	_on_frame(delta)


# ===================== AUDIO PLUMBING =====================

func _is_headless() -> bool:
	return DisplayServer.get_name() == "headless" or OS.has_feature("headless")


func _ensure_permission() -> bool:
	if OS.get_name() != "Android":
		return true
	var granted: PackedStringArray = OS.get_granted_permissions()
	for perm: String in granted:
		if perm.ends_with("RECORD_AUDIO"):
			return true
	if _ask_count >= MAX_PERMISSION_ASKS:
		# Asked twice, still not granted. Stop asking forever and fall back to
		# the buttons in silence — a denied permission must never block a fight.
		m.mic_permission_denied = true
		m.mic_state = "off"
		return false
	_ask_count += 1
	OS.request_permission("RECORD_AUDIO")
	m.mic_state = "asking"       # the dialog is async; the next arm() re-checks
	return false


func _ensure_bus() -> void:
	if _bus_idx >= 0 and _bus_idx < AudioServer.bus_count and AudioServer.get_bus_name(_bus_idx) == "Mic":
		return
	var found: int = AudioServer.get_bus_index("Mic")
	if found < 0:
		found = AudioServer.bus_count
		AudioServer.add_bus(found)
		AudioServer.set_bus_name(found, "Mic")
		AudioServer.set_bus_send(found, "Master")
	_bus_idx = found
	# -80 dB, NOT mute: the analyzer is a bus effect and must still see the
	# signal, while nothing the microphone hears can ever reach the speaker.
	# (Playing the mic back into a phone speaker is an instant feedback howl.)
	AudioServer.set_bus_volume_db(_bus_idx, -80.0)
	if AudioServer.get_bus_effect_count(_bus_idx) == 0:
		var fx := AudioEffectSpectrumAnalyzer.new()
		fx.fft_size = AudioEffectSpectrumAnalyzer.FFT_SIZE_1024
		fx.buffer_length = 0.1
		AudioServer.add_bus_effect(_bus_idx, fx)
	_analyzer = null


func _ensure_player() -> void:
	if _player != null and is_instance_valid(_player):
		return
	_player = AudioStreamPlayer.new()
	_player.name = "MicCapture"
	_player.stream = AudioStreamMicrophone.new()
	_player.bus = "Mic"
	_player.process_mode = Node.PROCESS_MODE_ALWAYS
	m.add_child(_player)


func _build_mel_edges() -> void:
	_edges.resize(BANDS + 1)
	var lo: float = _hz_to_mel(F_LO)
	var hi: float = _hz_to_mel(F_HI)
	for i in range(BANDS + 1):
		_edges[i] = _mel_to_hz(lo + (hi - lo) * float(i) / float(BANDS))


func _hz_to_mel(f: float) -> float:
	return 2595.0 * log(1.0 + f / 700.0) / log(10.0)


func _mel_to_hz(mel: float) -> float:
	return 700.0 * (pow(10.0, mel / 2595.0) - 1.0)


func _game_audio_playing() -> bool:
	# Our own voice lines and chimes come straight back in through the phone
	# speaker. Stay deaf while they play so a fireball cannot re-cast itself.
	for vp: Variant in m.voice_pool:
		var ap: AudioStreamPlayer = vp as AudioStreamPlayer
		if ap != null and ap.playing:
			return true
	if m.chime != null and m.chime.playing:
		return true
	return false


# Reads one feature frame from the spectrum analyzer into _frame/_frame_db.
func _read_frame() -> bool:
	if _analyzer == null:
		if _bus_idx < 0:
			return false
		_analyzer = AudioServer.get_bus_effect_instance(_bus_idx, 0) as AudioEffectSpectrumAnalyzerInstance
		if _analyzer == null:
			return false          # the bus has not mixed yet; try again next tick
	var total := 0.0
	for b in range(BANDS):
		var mag: Vector2 = _analyzer.get_magnitude_for_frequency_range(
			_edges[b], _edges[b + 1], AudioEffectSpectrumAnalyzerInstance.MAGNITUDE_AVERAGE)
		var lin: float = (mag.x + mag.y) * 0.5
		total += lin
		_frame[b] = log(lin + 1e-7)
	_frame_db = 20.0 * log(total + 1e-7) / log(10.0)
	_normalise_frame(_frame)
	return true


# Per-frame mean removal: drops overall loudness and the fixed colouration of
# this phone's microphone and this room, leaving only spectral shape.
static func _normalise_frame(f: PackedFloat32Array) -> void:
	var mean := 0.0
	for b in range(f.size()):
		mean += f[b]
	mean /= float(f.size())
	for b in range(f.size()):
		f[b] = f[b] - mean


# ===================== ENDPOINTING =====================

func _reset_capture() -> void:
	_hot = 0
	_cold = 0
	_speaking = false
	_raw.clear()
	_raw_t = 0.0
	_preroll.clear()


func _on_frame(delta: float) -> void:
	if not _floor_seeded:
		_floor_db = _frame_db
		_floor_seeded = true
	if not _speaking:
		# Track the room: up fast, down slow. A slowly-rising floor cannot
		# chase a word, but background music starting is absorbed in ~1 s.
		var rate: float = FLOOR_RISE if _frame_db > _floor_db else FLOOR_FALL
		_floor_db = lerpf(_floor_db, _frame_db, rate)
		if _self_audio_t > 0.0:
			_hot = 0
			return
		var copy := PackedFloat32Array(_frame)
		_preroll.append(copy)
		while _preroll.size() > PREROLL:
			_preroll.pop_front()
		if _frame_db > _floor_db + START_MARGIN_DB:
			_hot += 1
			if _hot >= START_HOLD:
				_speaking = true
				_cold = 0
				_raw = _preroll.duplicate()
				_raw_t = float(_preroll.size()) * delta
				_preroll.clear()
		else:
			_hot = 0
		return
	_raw.append(PackedFloat32Array(_frame))
	_raw_t += delta
	if _frame_db < _floor_db + END_MARGIN_DB:
		_cold += 1
	else:
		_cold = 0
	if _cold >= END_HOLD or _raw_t >= MAX_SECONDS or _raw.size() >= RAW_MAX_FRAMES:
		var frames: Array = _raw
		var dur: float = _raw_t
		_reset_capture()
		_finish_utterance(frames, dur)


# Both the live capture path and the probes land here.
func _finish_utterance(frames: Array, dur: float) -> void:
	if frames.size() < RAW_MIN_FRAMES or dur < MIN_SECONDS:
		return
	var norm: PackedFloat32Array = _resample(frames)
	if _enroll_left > 0 and _enroll_word != "":
		_add_template(_enroll_word, norm, dur)
		return
	var word: String = classify(norm, dur)
	if word != "":
		_pending = word
		m.mic_last_word = word


# Linear resample of a variable-length utterance onto NORM_FRAMES. This is what
# makes recognition independent of frame rate: a word captured at 30 fps on the
# phone and the same word captured at 60 fps produce the same matrix.
func _resample(frames: Array) -> PackedFloat32Array:
	var out := PackedFloat32Array()
	out.resize(NORM_FRAMES * BANDS)
	var n: int = frames.size()
	for i in range(NORM_FRAMES):
		var pos: float = float(i) * float(n - 1) / float(NORM_FRAMES - 1)
		var i0: int = int(floor(pos))
		var i1: int = mini(i0 + 1, n - 1)
		var t: float = pos - float(i0)
		var a: PackedFloat32Array = frames[i0]
		var b: PackedFloat32Array = frames[i1]
		var off: int = i * BANDS
		for k in range(BANDS):
			out[off + k] = a[k] + (b[k] - a[k]) * t
	return out


# ===================== MATCHING =====================

# Public so the probes can score a synthetic utterance without a device.
func classify(norm: PackedFloat32Array, dur: float) -> String:
	_load_templates()
	var best_word := ""
	var best := INF
	var runner_up := INF
	for word: String in WORDS:
		var list: Array = _templates.get(word, [])
		var word_best := INF
		for entry: Variant in list:
			var tpl: Dictionary = entry as Dictionary
			var data: PackedFloat32Array = tpl.get("data", PackedFloat32Array())
			if data.size() != NORM_FRAMES * BANDS:
				continue
			var d: float = _dtw(norm, data)
			var tdur: float = float(tpl.get("dur", dur))
			if tdur > 0.0 and dur > 0.0:
				# Resampling threw duration away; put a little of it back, so
				# a three-syllable word cannot masquerade as a one-syllable one.
				d += DUR_WEIGHT * absf(log(dur / tdur))
			word_best = minf(word_best, d)
		if word_best < best:
			runner_up = best
			best = word_best
			best_word = word
		elif word_best < runner_up:
			runner_up = word_best
	m.mic_last_dist = best if best < INF else -1.0
	if best_word == "" or best > ACCEPT_DIST:
		return ""
	if runner_up < INF and best > ACCEPT_RATIO * runner_up:
		return ""      # too close to call — say nothing, the buttons still work
	return best_word


# Dynamic time warping with a Sakoe-Chiba band. Both sequences are NORM_FRAMES
# long, so this is a fixed ~550 banded cells x 20 dims — about 11k operations
# per template, a few hundred thousand per spoken word, and exactly zero
# between words. The cost matrix is allocated once in _init and reused.
func _dtw(a: PackedFloat32Array, b: PackedFloat32Array) -> float:
	var n := NORM_FRAMES
	_dtw_cost.fill(INF)
	for i in range(n):
		var lo: int = maxi(0, i - DTW_BAND)
		var hi: int = mini(n - 1, i + DTW_BAND)
		var row: int = i * n
		var prev_row: int = row - n
		for j in range(lo, hi + 1):
			var d: float = _local(a, i, b, j)
			if i == 0 and j == 0:
				_dtw_cost[row + j] = d
				continue
			var best := INF
			if i > 0:
				best = minf(best, _dtw_cost[prev_row + j])
				if j > 0:
					best = minf(best, _dtw_cost[prev_row + j - 1])
			if j > 0:
				best = minf(best, _dtw_cost[row + j - 1])
			_dtw_cost[row + j] = best + d
	var total: float = _dtw_cost[(n - 1) * n + (n - 1)]
	if total == INF:
		return INF
	return total / float(2 * n)


# L1 over the band vector — no sqrt, and the same discriminative power as L2
# on mean-removed log magnitudes.
func _local(a: PackedFloat32Array, ai: int, b: PackedFloat32Array, bi: int) -> float:
	var s := 0.0
	var oa: int = ai * BANDS
	var ob: int = bi * BANDS
	for k in range(BANDS):
		s += absf(a[oa + k] - b[ob + k])
	return s / float(BANDS)


# ===================== ENROLLMENT & PERSISTENCE =====================

func begin_enroll(word: String, count: int = TEMPLATES_PER_WORD) -> void:
	_load_templates()
	_enroll_word = word
	_enroll_left = count
	_templates[word] = []
	m.mic_state = "enroll" if m.mic_state != "test" else "test"
	_reset_capture()


func cancel_enroll() -> void:
	_enroll_word = ""
	_enroll_left = 0
	_teach_queue.clear()


func _add_template(word: String, norm: PackedFloat32Array, dur: float) -> void:
	var list: Array = _templates.get(word, [])
	list.append({"data": norm, "dur": dur})
	_templates[word] = list
	_enroll_left -= 1
	m.mic_enroll_left = _enroll_left
	_on_template_captured(word)
	if _enroll_left <= 0:
		_enroll_word = ""
		save_templates()
		_advance_teach()


func save_templates() -> void:
	var words := {}
	for word: String in WORDS:
		var list: Array = _templates.get(word, [])
		var out: Array = []
		for entry: Variant in list:
			var tpl: Dictionary = entry as Dictionary
			var data: PackedFloat32Array = tpl.get("data", PackedFloat32Array())
			var flat: Array = []
			flat.resize(data.size())
			for i in range(data.size()):
				flat[i] = snappedf(data[i], 0.001)
			out.append({"dur": snappedf(float(tpl.get("dur", 0.0)), 0.001), "data": flat})
		words[word] = out
	var f: FileAccess = FileAccess.open(TEMPLATE_PATH, FileAccess.WRITE)
	if f == null:
		push_warning("MicInput: could not write %s" % TEMPLATE_PATH)
		return
	f.store_string(JSON.stringify({"version": TEMPLATE_VERSION, "words": words}))
	f.close()


func _load_templates() -> void:
	if _loaded:
		return
	_loaded = true
	if not FileAccess.file_exists(TEMPLATE_PATH):
		return
	var f: FileAccess = FileAccess.open(TEMPLATE_PATH, FileAccess.READ)
	if f == null:
		return
	var text: String = f.get_as_text()
	f.close()
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("MicInput: %s is unreadable; spells must be taught again" % TEMPLATE_PATH)
		return
	var doc: Dictionary = parsed as Dictionary
	var words: Variant = doc.get("words", {})
	if typeof(words) != TYPE_DICTIONARY:
		return
	var words_d: Dictionary = words as Dictionary
	for word: String in WORDS:
		var raw: Variant = words_d.get(word, [])
		if typeof(raw) != TYPE_ARRAY:
			continue
		var list: Array = []
		for entry: Variant in (raw as Array):
			if typeof(entry) != TYPE_DICTIONARY:
				continue
			var tpl: Dictionary = entry as Dictionary
			var flat: Variant = tpl.get("data", [])
			if typeof(flat) != TYPE_ARRAY:
				continue
			var flat_a: Array = flat as Array
			if flat_a.size() != NORM_FRAMES * BANDS:
				continue
			var data := PackedFloat32Array()
			data.resize(flat_a.size())
			for i in range(flat_a.size()):
				data[i] = float(flat_a[i])
			list.append({"data": data, "dur": float(tpl.get("dur", 0.4))})
		_templates[word] = list


# Probe seam: install templates without a device or a file.
func test_install_template(word: String, norm: PackedFloat32Array, dur: float) -> void:
	_loaded = true
	var list: Array = _templates.get(word, [])
	list.append({"data": norm, "dur": dur})
	_templates[word] = list


# Probe seam: run a synthetic utterance through the real endpoint-to-verdict
# path (resample, enroll-or-classify) with no microphone in the picture.
func test_utterance(frames: Array, dur: float) -> void:
	_finish_utterance(frames, dur)


func test_clear_templates() -> void:
	_templates.clear()
	_loaded = true


# ===================== TEACH-THE-SPELL OVERLAY =====================
# Opened from the pause menu the first time the toggle is switched on. A
# non-reader gets a giant glyph, a recorded prompt and a row of pips that fill
# in as she speaks. SKIP is always available and always safe.

func open_teach() -> void:
	if _is_headless():
		return
	m._navigation_push("mic_teach", self, Callable(self, "close_teach"))
	_load_templates()
	_teach_queue = WORDS.duplicate()
	_build_teach_layer()
	m._set_world_controls_enabled(false, "mic_teach")
	_advance_teach()
	arm()


func close_teach(save: bool = true) -> void:
	m._navigation_remove("mic_teach")
	if save:
		save_templates()
	cancel_enroll()
	_teach_pips.clear()
	_teach_glyph = null
	_teach_prompt = null
	if m.mic_teach_layer != null and is_instance_valid(m.mic_teach_layer):
		m.mic_teach_layer.queue_free()
	m.mic_teach_layer = null
	m._set_world_controls_enabled(true, "mic_teach")
	disarm()
	m.mic_state = "idle"


func _advance_teach() -> void:
	if m.mic_teach_layer == null or not is_instance_valid(m.mic_teach_layer):
		return
	if _teach_queue.is_empty():
		m.show_msg("Roshan", "You know the magic words now! Say them in a battle!", "win")
		close_teach()
		return
	var word: String = _teach_queue.pop_front()
	begin_enroll(word)
	m.mic_enroll_left = _enroll_left
	if _teach_glyph != null:
		_teach_glyph.text = String(WORD_GLYPH.get(word, "✦"))
	if _teach_prompt != null:
		_teach_prompt.text = String(WORD_PROMPT.get(word, "Say the magic word!"))
	_rebuild_pips()
	m.show_msg("Roshan", String(WORD_PROMPT.get(word, "Say the magic word!")), "talk")


func _on_template_captured(_word: String) -> void:
	if m.chime != null:
		m.chime.pitch_scale = 1.2
		m.chime.play()
	_rebuild_pips()


func _rebuild_pips() -> void:
	var filled: int = TEMPLATES_PER_WORD - maxi(_enroll_left, 0)
	for i in range(_teach_pips.size()):
		var pip: Label = _teach_pips[i] as Label
		if pip != null:
			pip.text = "★" if i < filled else "☆"


func _build_teach_layer() -> void:
	if m.mic_teach_layer != null and is_instance_valid(m.mic_teach_layer):
		m.mic_teach_layer.queue_free()
	var layer := CanvasLayer.new()
	layer.name = "MicTeachLayer"
	layer.layer = 13
	m.add_child(layer)
	m.mic_teach_layer = layer
	var root := Control.new()
	root.name = "MicTeachOverlay"
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	layer.add_child(root)
	var dim: ColorRect = StorybookUI.add_dim(root)
	dim.mouse_filter = Control.MOUSE_FILTER_STOP
	var shell_rect := Rect2(290, 90, 700, 540)
	var shell: Panel = StorybookUI.add_panel(root, shell_rect, StorybookUI.PURPLE, Color(0.90, 0.96, 1.0, 0.99), 62)
	shell.name = "MicTeachShell"
	StorybookUI.adorn_panel(root, shell_rect, "MicTeach")

	_teach_glyph = Label.new()
	_teach_glyph.name = "MicTeachGlyph"
	StorybookUI.style_label(_teach_glyph, 150, StorybookUI.INK, 6)
	_teach_glyph.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_teach_glyph.position = Vector2(340, 130)
	_teach_glyph.custom_minimum_size = Vector2(600, 180)
	_teach_glyph.size = Vector2(600, 180)
	root.add_child(_teach_glyph)

	_teach_prompt = Label.new()
	_teach_prompt.name = "MicTeachPrompt"
	StorybookUI.style_label(_teach_prompt, 46, StorybookUI.INK, 4)
	_teach_prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_teach_prompt.position = Vector2(340, 330)
	_teach_prompt.custom_minimum_size = Vector2(600, 70)
	_teach_prompt.size = Vector2(600, 70)
	root.add_child(_teach_prompt)

	var pip_row := HBoxContainer.new()
	pip_row.name = "MicTeachPips"
	pip_row.position = Vector2(470, 410)
	pip_row.add_theme_constant_override("separation", 18)
	root.add_child(pip_row)
	_teach_pips.clear()
	for i in range(TEMPLATES_PER_WORD):
		var pip := Label.new()
		StorybookUI.style_label(pip, 54, StorybookUI.INK, 4)
		pip.text = "☆"
		pip_row.add_child(pip)
		_teach_pips.append(pip)

	var skip := Button.new()
	skip.name = "MicTeachSkipButton"
	skip.text = "✔   ALL DONE"
	skip.position = Vector2(440, 490)
	skip.custom_minimum_size = Vector2(400, 120)
	skip.size = Vector2(400, 120)
	StorybookUI.style_button(skip, "primary", 32, 34)
	skip.pressed.connect(func(): close_teach())
	root.add_child(skip)
