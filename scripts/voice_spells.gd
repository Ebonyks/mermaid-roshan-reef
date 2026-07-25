class_name VoiceSpells
extends RefCounted
# MAGIC WORDS — Roshan casts a spell when the child SHOUTS the word into the
# phone's microphone. First spell: FREEZE. A frost cone puffs out in front of
# her and every enemy caught inside it freezes solid.
#
# Satellite of main.gd (Phase 7 shape): receives `main` by reference, owns only
# logic. Player-visible / persisted state lives on main (m.spells_on,
# m.spell_hud, m.spell_mic, m.spell_capture, m.spell_casts, m.spell_last_word).
# The per-frame DSP scratch below is transient signal state, never game state —
# it is rebuilt from silence on every enable() and must not survive a reload.
#
# WHAT THE MATCHER ACTUALLY DOES (be honest about this — see SPELLS.md):
# Godot ships no speech recogniser and the game must work offline on a cheap
# phone, so this is NOT general speech-to-text. It is a shout detector plus a
# coarse word-SHAPE check:
#   1. loudness gate  — the utterance must be well above the room's noise floor
#                       and above an absolute "you actually shouted" level
#   2. duration gate  — long enough to be a word, short enough not to be a song
#   3. shape score    — "freeze" is fricative /f/ .. voiced vowel /iː/ ..
#                       buzzing /z/, i.e. HIGH-band energy at both ends with a
#                       LOW/MID vowel in the middle. That envelope is what gets
#                       scored, and it is what separates "freeze" from "go",
#                       "aaaah" or a clap.
# NO FAIL STATE (hard rule): in the default forgiving mode a loud, word-length
# shout still casts the one spell she knows even if the shape score misses —
# a 4yo's "FEEEZ!" must work. The shape score only decides WHICH spell once
# more than one exists. Nothing in the game is ever gated behind being heard:
# the ICE button always does the same job.

# ---------------- tuning ----------------
const HOP_SEC := 0.02          # one analysis frame per 20 ms
const BAND_LOW_HZ := 400.0     # below: vowel body / voice pitch
const BAND_HIGH_HZ := 1800.0   # above: fricative hiss (/f/, /s/, /z/)
const FLOOR_MIN_DB := -70.0
const FLOOR_MAX_DB := -24.0
const TRIGGER_MARGIN_DB := 14.0   # how far over the room floor counts as "loud"
const RELEASE_MARGIN_DB := 7.0    # hysteresis so a word's quiet middle survives
const SHOUT_MIN_DB := -30.0       # absolute floor: whispering never casts
const RELEASE_SEC := 0.16         # silence that ends an utterance
const MIN_WORD_SEC := 0.20
const MAX_WORD_SEC := 2.00
const RETRIGGER_SEC := 0.75       # lockout so one shout cannot cast twice
const MAX_FRAMES := 128           # 2.56 s of features — hard cap on scratch growth
const CAST_SCORE := 0.62          # shape score that counts as a confident match

# Spell book. Each profile is [onset, middle, tail] band-energy fractions
# (low, mid, high) — the coarse shape of the spoken word. Adding a second
# spell is a new entry here plus a cast handler; nothing else changes.
const SPELLS := {
	"freeze": {
		"icon": "❄",
		"profile": [
			Vector3(0.20, 0.35, 0.45),   # /fr/  — breathy hiss, quiet
			Vector3(0.38, 0.40, 0.22),   # /iː/  — voiced vowel, loud
			Vector3(0.22, 0.33, 0.45),   # /z/   — buzzing tail
		],
		# "freeze" starts and ends on fricatives: high-band energy at the EDGES
		# minus the middle is the single most telling feature of the word.
		"edge_hiss": 0.14,
	},
}

var m: ReefMain
var cast_handler: Callable = Callable()   # set by whatever owns the current scene

# ---- transient DSP scratch (see header) ----
var _bus_idx := -1
var _mix_rate := 44100.0
var _a_low := 0.0
var _a_high := 0.0
var _lp1 := 0.0
var _lp2 := 0.0
var _acc_n := 0
var _acc_low := 0.0
var _acc_mid := 0.0
var _acc_high := 0.0
var _hop_samples := 882
var _floor_db := -55.0
var _speaking := false
var _armed := true           # a new utterance needs a genuinely quiet frame first
var _quiet_t := 0.0
var _word_t := 0.0
var _peak_db := -99.0
var _lockout := 0.0
var _level := 0.0            # 0..1 smoothed loudness, drives the HUD ring
var _feat: Array[Vector4] = []   # per frame: (low, mid, high, rms_db)
var _test_queue: PackedVector2Array = PackedVector2Array()
var _test_mode := false

func _init(main: ReefMain) -> void:
	m = main
	_reset_dsp()

# ===================== availability & lifecycle =====================

func available() -> bool:
	# headless probes and any build without an audio input device: the whole
	# wing stays dark rather than erroring
	if _test_mode:
		return true
	if DisplayServer.get_name() == "headless":
		return false
	return AudioServer.get_input_device_list().size() > 0

func enable(announce: bool = true) -> bool:
	# announce=false is the boot restore of a saved preference: it must never
	# pop a permission dialog over the intro, and never re-teach a spell she
	# already knows. It just quietly re-opens a microphone she already allowed.
	if m.spells_on:
		return true
	if OS.get_name() == "Android" and not _has_record_permission():
		if not announce:
			return false
		OS.request_permission("RECORD_AUDIO")
		# Android answers the dialog asynchronously; the child taps the toggle
		# again once a grown-up has said yes. Never block, never error.
		m.show_msg("Roshan", "Say YES to let me hear you, then tap the magic words again!", "talk")
		return false
	if not _test_mode and not _open_mic():
		if announce:
			m.show_msg("Roshan", "I can't hear anything right now — the ICE button still works!", "talk")
		return false
	m.spells_on = true
	_reset_dsp()
	_build_hud()
	if announce:
		_teach()
	return true

func disable() -> void:
	m.spells_on = false
	_close_mic()
	_reset_dsp()
	if m.spell_hud != null:
		m.spell_hud.visible = false

func enable_for_test() -> void:
	# probe entry point: everything except the physical microphone
	_test_mode = true
	enable()

func _has_record_permission() -> bool:
	return "android.permission.RECORD_AUDIO" in OS.get_granted_permissions()

func _open_mic() -> bool:
	if not available():
		return false
	_bus_idx = AudioServer.get_bus_index("Mic")
	if _bus_idx < 0:
		AudioServer.add_bus()
		_bus_idx = AudioServer.bus_count - 1
		AudioServer.set_bus_name(_bus_idx, "Mic")
		AudioServer.set_bus_send(_bus_idx, "Master")
	# MUTED on purpose: the effect still sees the signal, but the phone never
	# plays the child's own voice back at her (that howls through the speaker).
	AudioServer.set_bus_mute(_bus_idx, true)
	AudioServer.set_bus_volume_db(_bus_idx, -80.0)
	var capture: AudioEffectCapture = null
	for i in range(AudioServer.get_bus_effect_count(_bus_idx)):
		var fx: AudioEffect = AudioServer.get_bus_effect(_bus_idx, i)
		if fx is AudioEffectCapture:
			capture = fx as AudioEffectCapture
			break
	if capture == null:
		capture = AudioEffectCapture.new()
		capture.buffer_length = 0.5
		AudioServer.add_bus_effect(_bus_idx, capture)
	m.spell_capture = capture
	if m.spell_mic == null:
		m.spell_mic = AudioStreamPlayer.new()
		m.spell_mic.name = "SpellMic"
		m.spell_mic.stream = AudioStreamMicrophone.new()
		m.spell_mic.bus = "Mic"
		m.spell_mic.process_mode = Node.PROCESS_MODE_ALWAYS
		m.add_child(m.spell_mic)
	m.spell_mic.play()
	return m.spell_mic.playing

func _close_mic() -> void:
	if m.spell_mic != null:
		m.spell_mic.stop()
	m.spell_capture = null

func _reset_dsp() -> void:
	_mix_rate = maxf(8000.0, AudioServer.get_mix_rate())
	_hop_samples = maxi(64, int(_mix_rate * HOP_SEC))
	_a_low = 1.0 - exp(-TAU * BAND_LOW_HZ / _mix_rate)
	_a_high = 1.0 - exp(-TAU * BAND_HIGH_HZ / _mix_rate)
	_lp1 = 0.0
	_lp2 = 0.0
	_acc_n = 0
	_acc_low = 0.0
	_acc_mid = 0.0
	_acc_high = 0.0
	_floor_db = -55.0
	_speaking = false
	_armed = true
	_quiet_t = 0.0
	_word_t = 0.0
	_peak_db = -99.0
	_level = 0.0
	_feat.clear()
	_test_queue = PackedVector2Array()

# ===================== per-frame =====================

func tick(delta: float) -> void:
	if not m.spells_on:
		return
	if _lockout > 0.0:
		_lockout = maxf(0.0, _lockout - delta)
	var chunk: PackedVector2Array = _pull()
	if chunk.size() > 0:
		_analyse(chunk)
	# an utterance that never falls quiet (a held shout, a passing lorry) still
	# has to end: MAX_WORD_SEC closes it and it is scored like any other
	if _speaking and _word_t >= MAX_WORD_SEC:
		_end_utterance()
	_level = maxf(0.0, _level - delta * 1.6)
	_update_hud()

func feed_test_samples(pcm: PackedVector2Array) -> void:
	# probe hook: inject synthesised audio exactly where the microphone's
	# samples would have arrived, so the whole gate/shape path is under test
	_test_queue.append_array(pcm)

func _pull() -> PackedVector2Array:
	if _test_queue.size() > 0:
		var take: int = mini(_test_queue.size(), _hop_samples * 8)
		var out: PackedVector2Array = _test_queue.slice(0, take)
		_test_queue = _test_queue.slice(take)
		return out
	if m.spell_capture == null:
		return PackedVector2Array()
	var avail: int = m.spell_capture.get_frames_available()
	if avail <= 0:
		return PackedVector2Array()
	# never drain more than ~8 hops in one frame: a hitch that piled up half a
	# second of audio must not spend that half second inside one _process
	return m.spell_capture.get_buffer(mini(avail, _hop_samples * 8))

func _analyse(chunk: PackedVector2Array) -> void:
	for i in range(chunk.size()):
		var s: Vector2 = chunk[i]
		var x: float = (s.x + s.y) * 0.5
		# two cascaded one-pole lowpasses split the signal into three coarse
		# bands without an FFT — cheap enough for the oldest phone in the house
		_lp1 += _a_low * (x - _lp1)
		_lp2 += _a_high * (x - _lp2)
		var lo: float = _lp1
		var mid: float = _lp2 - _lp1
		var hi: float = x - _lp2
		_acc_low += lo * lo
		_acc_mid += mid * mid
		_acc_high += hi * hi
		_acc_n += 1
		if _acc_n >= _hop_samples:
			_push_frame()

func _push_frame() -> void:
	var n: float = float(maxi(_acc_n, 1))
	var e_low: float = _acc_low / n
	var e_mid: float = _acc_mid / n
	var e_high: float = _acc_high / n
	var total: float = e_low + e_mid + e_high
	var db: float = linear_to_db(sqrt(maxf(total, 1e-12)))
	var inv: float = 1.0 / maxf(total, 1e-12)
	_acc_n = 0
	_acc_low = 0.0
	_acc_mid = 0.0
	_acc_high = 0.0
	_level = maxf(_level, clampf((db - SHOUT_MIN_DB - 12.0) / 24.0, 0.0, 1.0))
	if _speaking:
		_word_t += HOP_SEC
		_peak_db = maxf(_peak_db, db)
		if _feat.size() < MAX_FRAMES:
			_feat.append(Vector4(e_low * inv, e_mid * inv, e_high * inv, db))
		if _word_t >= MAX_WORD_SEC:
			_end_utterance()   # a held "FREEEEEZE" still counts — scored at the cap
		elif db < _floor_db + RELEASE_MARGIN_DB:
			_quiet_t += HOP_SEC
			if _quiet_t >= RELEASE_SEC:
				_end_utterance()
		else:
			_quiet_t = 0.0
		return
	# quiet: the room's noise floor follows fast downward, slowly upward, so a
	# noisy playroom raises the bar instead of casting spells by itself
	_floor_db = clampf(lerpf(_floor_db, db, 0.30 if db < _floor_db else 0.02), FLOOR_MIN_DB, FLOOR_MAX_DB)
	if db < _floor_db + RELEASE_MARGIN_DB:
		# the signal really dropped: the next loud onset is a NEW word. Without
		# this, one long scream (or a vacuum cleaner) re-triggers over and over
		# as soon as the lockout expires.
		_armed = true
	if _lockout > 0.0 or not _armed:
		return
	if db > _floor_db + TRIGGER_MARGIN_DB and db > SHOUT_MIN_DB:
		_speaking = true
		_word_t = HOP_SEC
		_quiet_t = 0.0
		_peak_db = db
		_feat.clear()
		_feat.append(Vector4(e_low * inv, e_mid * inv, e_high * inv, db))

func _end_utterance() -> void:
	# The release hold is silence, not speech. Room tone is broadband, so those
	# trailing frames read as a textbook fricative — leaving them in made every
	# vowel look like it ended on a /z/ and scored "aaaah" as high as "freeze".
	# Trim them off both the features and the measured word length.
	var tail: int = int(round(_quiet_t / HOP_SEC))
	var length: float = _word_t - _quiet_t
	var peak: float = _peak_db
	var feats: Array[Vector4] = []
	feats.assign(_feat.slice(0, maxi(3, _feat.size() - tail)))
	_speaking = false
	_armed = false   # re-arms only once the room actually falls quiet again
	_word_t = 0.0
	_quiet_t = 0.0
	_peak_db = -99.0
	_feat.clear()
	if length < MIN_WORD_SEC or length > MAX_WORD_SEC + HOP_SEC * 2.0:
		return          # a clap, a cough, or a whole sung verse — not a word
	if peak < SHOUT_MIN_DB:
		return          # "loudly" is part of the spell
	var best: Dictionary = best_match(feats)
	var word: String = String(best.get("word", ""))
	if word == "":
		return
	_lockout = RETRIGGER_SEC
	_route_cast(word, float(best.get("score", 0.0)), bool(best.get("matched", false)))

# ===================== word shape =====================

func best_match(feats: Array[Vector4]) -> Dictionary:
	# Scores the utterance against every spell in the book and returns the
	# winner. `matched` says whether the shape was actually recognised, or
	# whether forgiving mode is carrying a shout that only ALMOST fit.
	if feats.size() < 3:
		return {}
	var best_word := ""
	var best_score := -1.0
	for word: String in SPELLS.keys():
		var score: float = score_word(feats, word)
		if score > best_score:
			best_score = score
			best_word = word
	if best_score >= CAST_SCORE:
		return {"word": best_word, "score": best_score, "matched": true}
	if m.spells_forgiving and SPELLS.size() == 1:
		# She knows exactly one magic word. A loud, word-length shout IS that
		# word as far as a 4yo is concerned — never make her say it "properly".
		return {"word": best_word, "score": best_score, "matched": false}
	return {}

func score_word(feats: Array[Vector4], word: String) -> float:
	if not SPELLS.has(word) or feats.size() < 3:
		return 0.0
	var spell: Dictionary = SPELLS[word]
	var profile: Array = spell["profile"]
	var segs: Array[Vector3] = _segments(feats, profile.size())
	var fit := 0.0
	for i in range(segs.size()):
		var want: Vector3 = profile[i]
		var got: Vector3 = segs[i]
		# fractions sum to 1, so the L1 distance is at most 2 — map it to 0..1
		var l1: float = absf(got.x - want.x) + absf(got.y - want.y) + absf(got.z - want.z)
		fit += clampf(1.0 - l1 * 0.5, 0.0, 1.0)
	fit /= float(maxi(segs.size(), 1))
	# The discriminating feature: hiss at BOTH ends with a vowel in between.
	# It has to be the weaker end, not the average — averaging let "GO" through
	# on the strength of its plosive onset alone.
	var edge: float = minf(segs[0].z, segs[segs.size() - 1].z)
	var middle: float = segs[segs.size() / 2].z
	var hiss: float = clampf((edge - middle) / maxf(float(spell["edge_hiss"]), 0.01), 0.0, 1.0)
	return clampf(fit * 0.6 + hiss * 0.4, 0.0, 1.0)

func _segments(feats: Array[Vector4], count: int) -> Array[Vector3]:
	# average band fractions over `count` equal slices of the utterance
	var out: Array[Vector3] = []
	var n: int = feats.size()
	for s in range(count):
		var from: int = int(floor(float(s) * float(n) / float(count)))
		var to: int = maxi(from + 1, int(floor(float(s + 1) * float(n) / float(count))))
		var sum := Vector3.ZERO
		var taken := 0
		for i in range(from, mini(to, n)):
			var f: Vector4 = feats[i]
			sum += Vector3(f.x, f.y, f.z)
			taken += 1
		out.append(sum / float(maxi(taken, 1)))
	return out

# ===================== casting =====================

func _route_cast(word: String, score: float, matched: bool) -> void:
	m.spell_casts += 1
	m.spell_last_word = word
	# kept for tuning on a real phone: how well the shout actually fit the word,
	# and whether forgiving mode had to carry it
	m.spell_last_score = score
	m.spell_last_matched = matched
	_flash_hud()
	if cast_handler.is_valid():
		# whoever owns the current scene gets first refusal (the arena refuses
		# while the spell is recharging, and answers with its own hint)
		if bool(cast_handler.call(word)):
			return
	if word == "freeze" and is_instance_valid(m.combat_game):
		if m.combat_game.cast_freeze():
			return
		m.show_msg("Roshan", "My magic is still catching its breath — try the ICE button!", "talk")
		return
	_flourish(word)

func _flourish(word: String) -> void:
	# heard out in the open reef, where there is nothing to freeze: she still
	# gets the whole sparkle so the magic word is never "wrong", only unaimed
	if m.player == null:
		return
	var fwd: Vector3 = -m.player.global_transform.basis.z
	fwd.y = 0.0
	if fwd.length() < 0.01:
		fwd = Vector3.FORWARD
	fwd = fwd.normalized()
	var at: Vector3 = m.player.position + Vector3(0, 1.2, 0) + fwd * 4.0
	m._sparkle_burst(at, Color(0.62, 0.94, 1.0))
	# vo = the spell name: drop assets/audio/voices/roshan_freeze.ogg in and the
	# real family recording plays here automatically (see AudioDirector._say)
	m.show_msg("Roshan", "%s  FREEZE! Frosty sparkles everywhere!" % String(SPELLS[word]["icon"]), word)

func _teach() -> void:
	# hard rule: a new objective fires a voice line AND shows a visible pointer.
	# The pointer here is the pulsing snowflake bubble the HUD just switched on.
	m.show_msg("Roshan", "❄  Magic words are ON! Shout FREEZE and watch what happens!", "freeze")

# ===================== geometry =====================

static func in_cone(origin: Vector3, dir: Vector3, target: Vector3, length: float, half_deg: float, near: float = 2.5) -> bool:
	# flat (XZ) cone test: everything in the wedge in front of her, plus a
	# generous point-blank bubble so an enemy right on top of her always counts
	var to: Vector3 = target - origin
	to.y = 0.0
	var dist: float = to.length()
	if dist > length:
		return false
	if dist <= near:
		return true
	var fwd: Vector3 = Vector3(dir.x, 0.0, dir.z)
	if fwd.length() < 0.001:
		return false
	return fwd.normalized().dot(to / dist) >= cos(deg_to_rad(half_deg))

# ===================== HUD =====================

func _build_hud() -> void:
	if m.spell_hud != null:
		m.spell_hud.visible = true
		return
	var cl := CanvasLayer.new()
	cl.layer = 11   # over the world HUD, under the pause menu (12)
	cl.name = "SpellHud"
	m.add_child(cl)
	m.spell_hud = cl
	var bubble := Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0.09, 0.16, 0.34, 0.62)
	sb.border_color = Color(0.62, 0.94, 1.0, 0.85)
	sb.set_border_width_all(4)
	sb.set_corner_radius_all(46)
	bubble.add_theme_stylebox_override("panel", sb)
	bubble.position = Vector2(556, 12)
	bubble.size = Vector2(168, 92)
	bubble.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cl.add_child(bubble)
	m.spell_bubble = bubble
	var icon := Label.new()
	# icons, not words: the mouth says "shout", the snowflake says "freeze"
	icon.text = "🗣 ❄"
	icon.add_theme_font_size_override("font_size", 40)
	icon.add_theme_color_override("font_outline_color", Color(0.03, 0.06, 0.16))
	icon.add_theme_constant_override("outline_size", 7)
	icon.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	icon.offset_bottom = -18
	icon.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	icon.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	bubble.add_child(icon)
	var meter := ProgressBar.new()
	# a loudness worm: she can SEE the phone hearing her before any word lands
	meter.show_percentage = false
	meter.min_value = 0.0
	meter.max_value = 1.0
	meter.position = Vector2(22, 64)
	meter.size = Vector2(124, 14)
	meter.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var fill := StyleBoxFlat.new()
	fill.bg_color = Color(0.62, 0.94, 1.0, 0.95)
	fill.set_corner_radius_all(7)
	var bg := StyleBoxFlat.new()
	bg.bg_color = Color(0.05, 0.1, 0.22, 0.7)
	bg.set_corner_radius_all(7)
	meter.add_theme_stylebox_override("fill", fill)
	meter.add_theme_stylebox_override("background", bg)
	bubble.add_child(meter)
	m.spell_meter = meter

func _update_hud() -> void:
	if m.spell_meter != null:
		m.spell_meter.value = _level
	if m.spell_bubble != null:
		var pulse: float = 1.0 + _level * 0.12
		m.spell_bubble.pivot_offset = m.spell_bubble.size * 0.5
		m.spell_bubble.scale = Vector2(pulse, pulse)

func _flash_hud() -> void:
	if m.spell_bubble == null:
		return
	var ring := ColorRect.new()
	ring.color = Color(0.75, 0.97, 1.0, 0.55)
	ring.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ring.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	m.spell_bubble.add_child(ring)
	var tw: Tween = ring.create_tween()
	tw.tween_property(ring, "color:a", 0.0, 0.45)
	tw.tween_callback(ring.queue_free)
