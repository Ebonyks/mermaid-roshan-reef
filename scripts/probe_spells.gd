extends SceneTree
# MAGIC WORDS probe: the shouted-spell wing (scripts/voice_spells.gd) end to end
# without a microphone. Synthesised PCM is injected exactly where the mic's
# samples would arrive, so the loudness gate, the duration gate, the word-shape
# matcher, the cast routing and the arena's frost cone are all under test.
#
# The three things this must prove:
#   1. silence casts NOTHING (the passive-probe rule, with the mic switched on)
#   2. the shape matcher really discriminates — with forgiveness OFF, a
#      "freeze"-shaped shout casts and a flat vowel shout does not
#   3. the cone is a cone: enemies in front freeze, enemies behind do not

var main: ReefMain
var sp: VoiceSpells
var bad := 0

func _init() -> void:
	seed(20260725)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	sp = main._spells_ref()
	sp.enable_for_test()
	_ck("magic words switch on", main.spells_on and main.spell_hud != null)
	_ck("switching on does not silently rewrite the saved answer", not main.spells_pref)
	_settle()
	_listening_cases()
	_shape_cases()
	await _cone_cases()
	print("SPELLS|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	quit()

func _ck(label: String, ok: bool) -> void:
	print("SPELLS|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

# ===================== synthetic audio =====================

func _rate() -> float:
	return sp._mix_rate

func _frames(sec: float) -> int:
	return int(_rate() * sec)

func _quiet(sec: float) -> PackedVector2Array:
	# room tone: audible to the floor tracker, nowhere near the shout gate
	var out := PackedVector2Array()
	for i in range(_frames(sec)):
		var v: float = randf_range(-0.0008, 0.0008)
		out.append(Vector2(v, v))
	return out

func _hiss(sec: float, amp: float) -> PackedVector2Array:
	# a fricative (/f/, /z/): broadband noise, most of it above 1800 Hz
	var out := PackedVector2Array()
	for i in range(_frames(sec)):
		var v: float = randf_range(-amp, amp)
		out.append(Vector2(v, v))
	return out

func _vowel(sec: float, amp: float) -> PackedVector2Array:
	# a voiced vowel: a low pitch plus one formant plus a little breath
	var out := PackedVector2Array()
	var n: int = _frames(sec)
	for i in range(n):
		var t: float = float(i) / _rate()
		var v: float = sin(TAU * 300.0 * t) + 0.55 * sin(TAU * 950.0 * t) + randf_range(-0.10, 0.10)
		v *= amp * 0.62
		out.append(Vector2(v, v))
	return out

func _cat(parts: Array) -> PackedVector2Array:
	var out := PackedVector2Array()
	for p: PackedVector2Array in parts:
		out.append_array(p)
	return out

func _freeze_word(amp: float = 0.62) -> PackedVector2Array:
	# "FREEZE" — /fr/ hiss, /iː/ vowel, /z/ buzz, then the silence that ends it
	return _cat([_hiss(0.13, amp * 0.55), _vowel(0.30, amp), _hiss(0.16, amp * 0.6), _quiet(0.30)])

func _flat_shout(amp: float = 0.62) -> PackedVector2Array:
	# "AAAAH" — just as loud, just as long, no fricative edges at all
	return _cat([_vowel(0.55, amp), _quiet(0.30)])

func _plosive_word(amp: float = 0.62) -> PackedVector2Array:
	# "GO!" — a hard onset then a vowel. Hisses at the START only, which is the
	# false positive that an averaged edge test waved through.
	return _cat([_hiss(0.03, amp * 0.5), _vowel(0.28, amp), _quiet(0.30)])

func _mumbled_freeze(amp: float = 0.62) -> PackedVector2Array:
	# the same word from a 4yo across the room: both fricatives much weaker
	return _cat([_hiss(0.10, amp * 0.35), _vowel(0.34, amp), _hiss(0.11, amp * 0.30), _quiet(0.30)])

func _drive(pcm: PackedVector2Array) -> void:
	# one tick consumes up to eight hops, so advance the clock by exactly that
	# much audio — otherwise the retrigger lockout never expires in probe time
	var dt: float = float(sp._hop_samples * 8) / sp._mix_rate
	sp.feed_test_samples(pcm)
	for i in range(400):
		sp.tick(dt)
		if sp._test_queue.is_empty():
			break
	sp.tick(dt)

func _settle() -> void:
	# let the noise-floor tracker learn a quiet room before anything is shouted
	_drive(_quiet(1.2))

# ===================== cases =====================

func _listening_cases() -> void:
	var before: int = main.spell_casts
	_drive(_quiet(2.0))
	_ck("silence casts nothing", main.spell_casts == before)
	_drive(_cat([_hiss(0.06, 0.7), _quiet(0.30)]))
	_ck("a loud short blip is not a word", main.spell_casts == before)
	_drive(_cat([_vowel(3.4, 0.6), _quiet(0.40)]))
	# a held roar closes at MAX_WORD_SEC and is scored like any other utterance,
	# but one long noise must never machine-gun the spell
	_ck("a long roar casts exactly once", main.spell_casts == before + 1)

func _shape_cases() -> void:
	# forgiveness OFF isolates the matcher: only the word's SHAPE can cast now
	main.spells_forgiving = false
	_settle()
	var before: int = main.spell_casts
	_drive(_freeze_word())
	_ck("a freeze-shaped shout casts freeze", main.spell_casts == before + 1 and main.spell_last_word == "freeze")
	_settle()
	var soft: int = main.spell_casts
	_drive(_mumbled_freeze())
	_ck("a mumbled freeze from across the room still casts", main.spell_casts == soft + 1)
	_settle()
	var mid: int = main.spell_casts
	_drive(_flat_shout())
	_ck("a flat vowel shout is not the word freeze", main.spell_casts == mid)
	_settle()
	_drive(_plosive_word())
	_ck("a hard-onset word like GO is not freeze either", main.spell_casts == mid)
	# forgiveness back ON is the shipping setting: she knows one magic word, so
	# a loud word-length shout casts it even when the shape score misses
	main.spells_forgiving = true
	_settle()
	var kind_before: int = main.spell_casts
	_drive(_flat_shout())
	_ck("forgiving mode still casts for a 4yo's FEEEZ", main.spell_casts == kind_before + 1)

func _cone_cases() -> void:
	main.game = "galaxy"
	main._start_combat("ice")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("ice arena is live for the spell", arena != null and arena.enemies.size() == 8)
	arena.player_pos = CombatArena.CENTER + Vector3(0, 1.1, 0)
	arena.player_yaw = 0.0   # facing +Z
	var front: Dictionary = arena.enemies[0]
	var behind: Dictionary = arena.enemies[1]
	var far_ahead: Dictionary = arena.enemies[2]
	var wide: Dictionary = arena.enemies[3]
	front["pos"] = arena.player_pos + Vector3(0, 0, 9.0)
	behind["pos"] = arena.player_pos + Vector3(0, 0, -9.0)
	far_ahead["pos"] = arena.player_pos + Vector3(0, 0, 22.0)
	wide["pos"] = arena.player_pos + Vector3(9.0, 0, 2.0)   # ~77 deg off her nose
	for e: Dictionary in [front, behind, far_ahead, wide]:
		e["state"] = "active"
	var cast_ok: bool = arena.cast_freeze()
	_ck("the spell fires in the arena", cast_ok)
	_ck("an enemy in front of her freezes", String(front["state"]) == "frozen")
	_ck("an enemy behind her does not", String(behind["state"]) == "active")
	_ck("an enemy past the cone's reach does not", String(far_ahead["state"]) == "active")
	_ck("an enemy off to the side does not", String(wide["state"]) == "active")
	_ck("the spell then has to recharge", not arena.cast_freeze())
	# the shout itself must reach the arena, not just the direct call
	var reroute: Dictionary = arena.enemies[4]
	reroute["pos"] = arena.player_pos + Vector3(0, 0, 7.0)
	reroute["state"] = "active"
	arena.spell_cool = 0.0
	_settle()
	_drive(_freeze_word())
	_ck("a shout routes into the live arena", String(reroute["state"]) == "frozen")
	# with the mic open and nothing said, the battle still cannot be won
	var quiet_frozen := 0
	arena.spell_cool = 0.0
	_drive(_quiet(2.0))
	for e: Dictionary in arena.enemies:
		if String(e["state"]) == "active":
			quiet_frozen += 1
	_ck("an open microphone alone freezes nobody", quiet_frozen >= 3 and arena.state == "play")
	arena.cancel()
	# the boss arena: the frost cone reaches the dragon-turtle the same way.
	# Retarget the source world before pumping frames — cancel() hands control
	# straight back to combat_from on the same call.
	main.game = "level2"
	main.g["t"] = 0.0
	await process_frame
	await process_frame
	main._start_combat("fire")
	await process_frame
	var boss_arena: CombatArena = main.combat_game
	_ck("boss arena is live for the spell", boss_arena != null and not boss_arena.boss.is_empty())
	boss_arena.player_pos = (boss_arena.boss["pos"] as Vector3) + Vector3(0, 1.1, -12.0)
	boss_arena.player_yaw = 0.0
	boss_arena.boss["phase"] = "shell"
	var hp_before: int = int(boss_arena.boss["hp"])
	boss_arena.spell_cool = 0.0
	_ck("freezing the spinning shell is allowed", boss_arena.cast_freeze())
	_ck("the shell still shrugs the hit off", int(boss_arena.boss["hp"]) == hp_before)
	boss_arena.boss["phase"] = "peek"
	boss_arena.spell_cool = 0.0
	_ck("the spell fires again once recharged", boss_arena.cast_freeze())
	_ck("frost reaches the peeking dragon-turtle", int(boss_arena.boss["hp"]) < hp_before)
	# and it misses cleanly when she is facing the wrong way
	var hp_now: int = int(boss_arena.boss["hp"])
	boss_arena.player_yaw = PI
	boss_arena.spell_cool = 0.0
	_ck("facing away, the cone fires but misses", boss_arena.cast_freeze() and int(boss_arena.boss["hp"]) == hp_now)
	boss_arena.cancel()
	await process_frame
	await process_frame
	_ck("no fail state: nothing was lost by missing", main.game == "level2")
