extends SceneTree
# Spoken-spell probe (MIC_SPELLS.md). There is no microphone in CI, so this
# drives scripts/mic_input.gd through its test seam: synthetic utterances are
# pushed into the SAME endpoint-to-verdict path the live capture uses
# (resample -> DTW -> accept/reject), so the recogniser itself is under test,
# not a stub of it.
#
# Two synthetic "words" stand in for the real ones and are built to mirror why
# FREEZE and FIREBALL are separable in the first place: word A is one short
# fricative-vowel-fricative sweep, word B is three humps over twice the
# duration. If the matcher ever collapses to "loudest band wins", B stops
# reading as B and this probe goes red.
#
# The negative half matters as much as the positive half (probe_passive's
# rule): silence, a too-short blip and an unrelated noise pattern must all
# resolve to "no spell cast", and a switched-off toggle must capture nothing.

var main: ReefMain
var mic: MicInput
var bad := 0

func _init() -> void:
	seed(20260802)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	mic = main._mic_ref()
	_runtime_audio_repair_case()
	_teaching_case()
	_recognition_case()
	_rejection_case()
	_persistence_case()
	_toggle_case()
	await _arena_case()
	print("MIC|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()


func _runtime_audio_repair_case() -> void:
	var mic_idx: int = AudioServer.get_bus_index("Mic")
	if mic_idx < 0:
		AudioServer.add_bus()
		mic_idx = AudioServer.bus_count - 1
		AudioServer.set_bus_name(mic_idx, "Mic")
	while AudioServer.get_bus_effect_count(mic_idx) > 0:
		AudioServer.remove_bus_effect(
			mic_idx, AudioServer.get_bus_effect_count(mic_idx) - 1)
	var non_analyzer: AudioEffectCompressor = AudioEffectCompressor.new()
	AudioServer.add_bus_effect(mic_idx, non_analyzer)
	var analyzer: AudioEffectSpectrumAnalyzer = AudioEffectSpectrumAnalyzer.new()
	AudioServer.add_bus_effect(mic_idx, analyzer)
	AudioServer.set_bus_volume_db(mic_idx, -12.0)
	AudioServer.set_bus_mute(mic_idx, true)
	AudioServer.set_bus_send(mic_idx, "SFX")
	mic._bus_idx = -1
	mic._ensure_bus()
	var repaired_idx: int = AudioServer.get_bus_index("Mic")
	var analyzer_count: int = 0
	var discovered_idx: int = -1
	for effect_idx in range(AudioServer.get_bus_effect_count(repaired_idx)):
		var effect: AudioEffect = AudioServer.get_bus_effect(repaired_idx, effect_idx)
		if effect is AudioEffectSpectrumAnalyzer:
			analyzer_count += 1
			discovered_idx = effect_idx
	_ck("runtime Mic repair restores safe routing", repaired_idx >= 0 \
		and is_equal_approx(AudioServer.get_bus_volume_db(repaired_idx), -80.0) \
		and not AudioServer.is_bus_mute(repaired_idx) \
		and AudioServer.get_bus_send(repaired_idx) == "Master")
	_ck("runtime Mic repair finds analyzer after non-analyzer effect", \
		analyzer_count == 1 and mic._analyzer_idx == discovered_idx \
		and mic._analyzer_idx > 0)
	_ck("runtime Mic repair does not add a duplicate analyzer", \
		AudioServer.get_bus_effect_count(repaired_idx) == 2)


func _ck(label: String, ok: bool) -> void:
	print("MIC|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1


# ===================== SYNTHETIC SPEECH =====================

# One feature frame: a tent centred on `center` in mel-band space, which is
# what a formant looks like once magnitudes are logged and mean-removed.
func _frame(center: float, width: float, jitter: float) -> PackedFloat32Array:
	var f := PackedFloat32Array()
	f.resize(MicInput.BANDS)
	for b in range(MicInput.BANDS):
		f[b] = -absf(float(b) - center) / width + randf_range(-jitter, jitter)
	MicInput._normalise_frame(f)
	return f


# A word is a path through band space. Word A sweeps high -> low -> high in one
# gesture; word B walks three humps. `jitter` is the only difference between an
# enrollment sample and a later query.
func _word_a(frames: int, jitter: float) -> Array:
	var out: Array = []
	for i in range(frames):
		var t: float = float(i) / float(maxi(frames - 1, 1))
		var center: float = 15.0 - 9.0 * sin(t * PI)
		out.append(_frame(center, 4.0, jitter))
	return out


func _word_b(frames: int, jitter: float) -> Array:
	var out: Array = []
	for i in range(frames):
		var t: float = float(i) / float(maxi(frames - 1, 1))
		var center: float = 9.0 + 5.0 * sin(t * PI * 3.0) - 3.0 * t
		out.append(_frame(center, 3.4, jitter))
	return out


# The same word, delivered differently: formants shifted `shift` bands and the
# whole mouth a bit more open or closed (`wscale`).
func _drift(is_a: bool, frames: int, shift: float, wscale: float) -> Array:
	var out: Array = []
	for i in range(frames):
		var t: float = float(i) / float(maxi(frames - 1, 1))
		var center := 0.0
		var width := 0.0
		if is_a:
			center = 15.0 - 9.0 * sin(t * PI)
			width = 4.0
		else:
			center = 9.0 + 5.0 * sin(t * PI * 3.0) - 3.0 * t
			width = 3.4
		out.append(_frame(center + shift, width * wscale, 0.35))
	return out


func _noise_word(frames: int) -> Array:
	var out: Array = []
	for i in range(frames):
		out.append(_frame(randf_range(2.0, 17.0), 9.0, 0.9))
	return out


func _enroll(word: String, maker: Callable, frames: int, dur: float) -> void:
	mic.begin_enroll(word)
	for i in range(MicInput.TEMPLATES_PER_WORD):
		# each sample is a slightly different performance of the same word
		var n: int = frames + (i % 3) - 1
		mic.test_utterance(maker.call(n, 0.05), dur * (0.92 + 0.04 * float(i % 3)))


# ===================== CASES =====================

func _teaching_case() -> void:
	mic.test_clear_templates()
	main.mic_state = "test"
	_ck("nothing is castable before the spells are taught",
		mic.classify(_flatten(_word_a(18, 0.0)), 0.4) == "" and not mic.all_words_taught())
	_enroll("ice", _word_a, 18, 0.40)
	_ck("teaching ICE banks five templates", mic.has_templates("ice") and not mic.all_words_taught())
	_enroll("fire", _word_b, 34, 0.82)
	_ck("teaching both spells completes enrollment", mic.all_words_taught())


func _recognition_case() -> void:
	# Jitter 0.60 is deliberately well above the 0.05 the templates were taught
	# at: a recogniser that only matches its own enrollment audio is worthless.
	var heard_ice := 0
	var heard_fire := 0
	for i in range(6):
		mic.test_utterance(_word_a(17 + i % 3, 0.60), 0.40)
		if mic.poll_word() == "ice":
			heard_ice += 1
		mic.test_utterance(_word_b(33 + i % 3, 0.60), 0.82)
		if mic.poll_word() == "fire":
			heard_fire += 1
	_ck("a spoken ICE is recognised (%d/6)" % heard_ice, heard_ice >= 5)
	_ck("a spoken FIRE is recognised (%d/6)" % heard_fire, heard_fire >= 5)
	# The realistic hard case: the same word said a bit differently — shifted
	# formants, a wider or narrower delivery, a different pace. A four-year-old
	# never says a word the same way twice.
	var drifted := 0
	var attempts := 0
	for shift: float in [1.0, -1.0, 1.5, -1.5]:
		attempts += 2
		mic.test_utterance(_drift(true, 17, shift, 1.15 if shift > 0.0 else 0.9), 0.40)
		if mic.poll_word() == "ice":
			drifted += 1
		mic.test_utterance(_drift(false, 33, shift, 1.15 if shift > 0.0 else 0.9), 0.82)
		if mic.poll_word() == "fire":
			drifted += 1
	_ck("a sloppier delivery of the same word still lands (%d/%d)" % [drifted, attempts], drifted >= attempts - 1)
	# The whole point of a time x frequency template: the two words must not be
	# interchangeable. A single confusion here is a real regression.
	var confusions := 0
	for i in range(6):
		mic.test_utterance(_word_a(17 + i % 3, 0.60), 0.40)
		if mic.poll_word() == "fire":
			confusions += 1
		mic.test_utterance(_word_b(33 + i % 3, 0.60), 0.82)
		if mic.poll_word() == "ice":
			confusions += 1
	_ck("the two spells are never confused for each other", confusions == 0)


func _rejection_case() -> void:
	var spurious := 0
	for i in range(8):
		mic.test_utterance(_noise_word(20 + i), 0.5)
		if mic.poll_word() != "":
			spurious += 1
	_ck("room noise casts no spell (%d/8 leaked)" % spurious, spurious == 0)
	# Silence and a cough are both shorter than any real word.
	mic.test_utterance([], 0.0)
	_ck("silence casts no spell", mic.poll_word() == "")
	mic.test_utterance(_word_a(3, 0.0), 0.06)
	_ck("a blip too short to be a word casts no spell", mic.poll_word() == "")
	# A word said halfway between the two must resolve to nothing rather than
	# guessing: the accept margin, not the accept distance, is what guards this.
	var blended: Array = []
	for i in range(24):
		var t: float = float(i) / 23.0
		blended.append(_frame(12.0 - 4.0 * sin(t * PI * 2.0), 5.0, 0.2))
	mic.test_utterance(blended, 0.6)
	var verdict: String = mic.poll_word()
	_ck("an ambiguous sound stays silent instead of guessing (%s)" % ["<silent>" if verdict == "" else verdict], verdict == "")


func _persistence_case() -> void:
	mic.save_templates()
	_ck("templates are stored outside reef_save.json",
		FileAccess.file_exists(MicInput.TEMPLATE_PATH) and not main.save_data.has("mic_templates"))
	# A fresh MicInput must reload them from disk and still recognise.
	var reloaded: MicInput = MicInput.new(main)
	reloaded.test_utterance(_word_b(34, 0.30), 0.82)
	_ck("a relaunch reloads the taught spells", reloaded.poll_word() == "fire")
	# Corrupt templates must degrade to "no spells", never to a crash.
	var f: FileAccess = FileAccess.open(MicInput.TEMPLATE_PATH, FileAccess.WRITE)
	f.store_string("{ not json at all")
	f.close()
	var broken: MicInput = MicInput.new(main)
	broken.test_utterance(_word_a(18, 0.1), 0.40)
	_ck("a corrupt template file degrades to silence, not a crash",
		broken.poll_word() == "" and not broken.all_words_taught())
	mic.save_templates()


func _toggle_case() -> void:
	var before: bool = main.mic_on
	main.mic_on = false
	main.mic_state = "idle"
	mic.arm()
	_ck("the toggle off refuses to arm the microphone", main.mic_state == "off")
	mic.tick(0.016)
	_ck("a disarmed microphone captures nothing", mic.poll_word() == "")
	main.mic_on = true
	main._write_save()
	_ck("the toggle persists to the save document", main.save_data.get("mic", null) == true)
	main.mic_on = false
	main._write_save()
	var raw: Variant = JSON.parse_string(FileAccess.get_file_as_string(main.SAVE_PATH))
	_ck("the save document round-trips the toggle off",
		typeof(raw) == TYPE_DICTIONARY and (raw as Dictionary).get("mic", null) == false)
	main.mic_on = before
	main._write_save()


func _arena_case() -> void:
	# The arena must never make the microphone a requirement: with mic_on true
	# but headless (no device), the battle still plays entirely on buttons.
	main.mic_on = true
	main.game = "galaxy"
	main._start_combat("ice")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("the ice arena builds with spoken spells enabled", arena != null and arena.enemies.size() == 8)
	_ck("no device means no spoken-spell promise is shown", not arena.mic_live)
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	for i in range(20):
		await process_frame
	_ck("spoken spells cannot win a battle passively",
		arena.state == "play" and not main.combat_ice_done)
	# A word arriving while mic_live is false must be ignored outright.
	main.mic_state = "test"
	arena.mic_live = false
	main.mic_sys._pending = "ice"
	_ck("a stray word is dropped when the arena is not listening", arena._mic_power() == "")
	# ...and when it IS listening, the spoken word casts the arena's power.
	arena.mic_live = true
	main.mic_sys._pending = "ice"
	_ck("a spoken ICE casts ice in the ice arena", arena._mic_power() == "ice")
	main.mic_sys._pending = "fire"
	_ck("a spoken FIRE is inert in the ice arena", arena._mic_power() == "")
	# cancel(true) so _end_combat runs and main lets go of the arena — a
	# cancel(false) here would leave main.combat_game pointing at a freed node.
	arena.cancel(true)
	await process_frame
	_ck("leaving the arena closes the capture device",
		main.mic_state != "listening" and main.combat_game == null)


func _flatten(frames: Array) -> PackedFloat32Array:
	# the same resample the live path performs, so classify() can be called
	# directly with a synthetic word
	var probe: MicInput = MicInput.new(main)
	return probe._resample(frames)
