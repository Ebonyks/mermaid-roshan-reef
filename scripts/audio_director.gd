class_name AudioDirector
extends RefCounted
# Phase 7.5: mechanical extraction of the audio pipeline from main.gd —
# music track switching (night-aware), the ambience bed + voice ducking,
# the global UI tap hook and the _say/show_msg voice pipeline. All state
# (players, pools, cur_track) stays on main; received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _say(speaker: String, event: String = "", min_gap: float = 0.0) -> void:
	var key := speaker + "_" + event
	if min_gap > 0.0:
		var now := Time.get_ticks_msec() / 1000.0
		if now - float(m.said_cool.get(key, -99.0)) < min_gap:
			return
		m.said_cool[key] = now
	# prefer a real recorded clip for this exact line, then any line for the speaker
	var stream: AudioStream = null
	var p1 := "res://assets/audio/voices/" + key + ".ogg"
	var p2 := "res://assets/audio/voices/" + speaker + ".ogg"
	if ResourceLoader.exists(p1):
		stream = load(p1)
	elif ResourceLoader.exists(p2):
		stream = load(p2)
	if stream != null:
		# Different semantic keys can resolve to the same family fallback clip
		# (for example harper_talk and harper_hint -> harper.ogg). Never start an
		# identical recording on a second pool player while the first is audible.
		for voice_player_value: Variant in m.voice_pool:
			var active_player := voice_player_value as AudioStreamPlayer
			if active_player != null and active_player.playing \
					and active_player.stream == stream:
				return
	var ap: AudioStreamPlayer = m.voice_pool[m.voice_i % m.voice_pool.size()]
	m.voice_i += 1
	if stream != null:
		ap.stream = stream
		ap.pitch_scale = 1.0
		ap.play()
	elif m.voice != null:
		# graceful fallback until real clips are dropped in: the recorded "yay",
		# pitched to give each character a recognisably different timbre
		m.voice.pitch_scale = float(m.VOICE_PITCH.get(speaker, 1.0))
		m.voice.play()


# ===================== STORY DIALOGUE =====================
# Sequenced spoken exchanges: two or more characters trading lines while the
# game keeps running. There is ONE caption slot, so a burst of show_msg calls
# overwrites itself; story lines queue here instead and advance on a TIMER —
# never on audio-finished, because headless probe runs have no audio device.
# Any touch skips to the next line, so neither an impatient child nor a probe
# pump is ever blocked. Queue state lives on ReefMain per the satellite rule.

func say_sequence(lines: Array, opening_hold: float = 0.0) -> void:
	if lines.is_empty():
		return
	m.dialogue_queue = lines.duplicate(true)
	m.dialogue_t = opening_hold
	m.dialogue_active = true
	if opening_hold <= 0.0:
		_advance_dialogue()


func _stop_active_speech() -> void:
	# Dialogue owns one audible voice at a time. Stop both exact-line players
	# and the generic fallback before a line changes or its location tears down.
	for voice_player_value: Variant in m.voice_pool:
		var voice_player: AudioStreamPlayer = voice_player_value as AudioStreamPlayer
		if voice_player != null:
			voice_player.stop()
	if m.voice != null:
		m.voice.stop()


func _advance_dialogue() -> void:
	_stop_active_speech()
	if m.dialogue_queue.is_empty():
		m.dialogue_active = false
		m.dialogue_t = 0.0
		return
	var line: Dictionary = m.dialogue_queue.pop_front()
	show_msg(
		String(line.get("who", "Roshan")),
		String(line.get("text", "")),
		String(line.get("vo", "talk"))
	)
	m.dialogue_t = maxf(0.8, float(line.get("hold", 3.2)))


## A touch consumed a story line? (callers use this to swallow the tap)
func skip_dialogue() -> bool:
	if not m.dialogue_active:
		return false
	_advance_dialogue()
	return true


func tick_dialogue(delta: float) -> void:
	if not m.dialogue_active:
		return
	m.dialogue_t -= delta
	if m.dialogue_t <= 0.0:
		_advance_dialogue()


func clear_dialogue() -> void:
	_stop_active_speech()
	m.dialogue_queue = []
	m.dialogue_t = 0.0
	m.dialogue_active = false


func _speaker_key(who: String) -> String:
	var w := who.to_lower()
	if "rosalina" in w: return "rosalina"
	if "roshan" in w: return "roshan"
	if "rumi" in w: return "rumi"
	if "huluu" in w: return "huluu"
	if "evie" in w or "lamb" in w: return "evie"
	if "harper" in w or "fiona" in w: return "harper"
	if "faron" in w: return "faron"
	if "daddy" in w: return "daddy"
	if "chuck" in w: return "chuck"
	if "wacky" in w: return "wacky"
	if "shop" in w: return "shop"
	if "sparkle" in w or "eagle" in w: return "sparkle"
	if "mewsha" in w or "kitty" in w: return "mewsha"
	if "everyone" in w: return "everyone"
	if "maestro" in w: return "maestro"
	if "kareem" in w: return "shop"
	if "imp" in w: return "imp"
	return "roshan"


func show_msg(who: String, txt: String, vo: String = "talk") -> void:
	# owner 2026-08-04: opera career worlds are full-screen art with no text.
	# The spoken line IS the message there; the caption strip stays empty.
	# ALPHA MERCY (2026-08-05): that rule assumed every line had a recording.
	# 14 career vo keys have none (all of detective's dialogue among them) —
	# with the caption ALSO hidden the instruction collapsed to a pitched
	# "yay" and the child was left with nothing. When the exact clip is
	# missing the caption comes back, so the grown-up sitting beside her can
	# read the line aloud. The moment a recording lands, the text hides again.
	if m.game == "opera":
		var speaker := _speaker_key(who)
		# "talk" is a generic acknowledgement, not an exact recording of an
		# arbitrary lobby/boss sentence. Never hide a supplied instruction just
		# because that one generic clip exists.
		var has_exact := vo != "talk" and ResourceLoader.exists(
			"res://assets/audio/voices/" + speaker + "_" + vo + ".ogg")
		m.hud_msg.visible = false
		if has_exact:
			# The main HUD loop derives visibility from text every frame. Clear both
			# fields so an earlier reading-aid caption cannot reappear underneath
			# this exact recording on the following frame.
			m.hud_msg.text = ""
			m.msg_timer = 0.0
		elif txt != "":
			m.hud_msg.text = txt
			m.hud_msg.visible = true
			m.msg_timer = 5.0
		if who != "":
			_say(speaker, vo, 0.5)
		return
	m.hud_msg.text = txt
	m.hud_msg.visible = txt != ""
	m.msg_timer = 5.0
	if who != "":
		_say(_speaker_key(who), vo, 0.5)
	# (speaker name + portrait intentionally omitted — just the message text)

# ===================== 3.0 PLATFORM & FLOW =====================


func _fanfare() -> void:
	# ta-da! three rising chimes. (Speaker voice lines are tried first via
	# show_msg's "win" event — drop recordings into
	# assets/audio/voices/<speaker>_win.ogg and they play automatically.)
	if m.chime == null:
		return
	var chime: AudioStreamPlayer = m.chime
	var chime_ref: WeakRef = weakref(chime)
	chime.pitch_scale = 0.9
	chime.play()
	m.get_tree().create_timer(0.16).timeout.connect(
		_play_fanfare_step.bind(chime_ref, 1.12))
	m.get_tree().create_timer(0.34).timeout.connect(
		_play_fanfare_step.bind(chime_ref, 1.35))


func _play_fanfare_step(chime_ref: WeakRef, pitch: float) -> void:
	var chime: AudioStreamPlayer = chime_ref.get_ref() as AudioStreamPlayer
	if chime == null or not is_instance_valid(chime):
		return
	chime.pitch_scale = pitch
	chime.play()


func _set_ambience(track: String) -> void:
	# a quiet world bed under the music: underwater in the reef, breeze +
	# birds in the lagoon, airy room tone in the castle. Ducks -6dB under voices.
	if m.ambience == null:
		m.ambience = AudioStreamPlayer.new()
		m.ambience.bus = "Ambience"
		m.add_child(m.ambience)
	var amb := ""
	if track in ["world", "finale"]:
		amb = "res://assets/audio/ambience_reef.ogg"
	elif track in ["level2", "castle_open", "northern", "galaxy", "ember",
			"dungeon_ice", "dungeon_ember", "combat_ice"] \
			or track.begins_with("picture_"):
		amb = "res://assets/audio/ambience_lagoon.ogg"
	elif track in ["hall", "home", "combat_tutorial", "combat_fire"] \
			or track.begins_with("castle_") \
			or track.begins_with("opera_"):
		# The Castle rooms and Opera are musical subspaces of the same pearl
		# interior. Their bespoke score must not accidentally silence the airy
		# room tone that used to ride beneath the shared hall cue.
		amb = "res://assets/audio/ambience_hall.ogg"
	elif track == "stuffie_battle":
		# Companion sparring can start from the reef, lagoon, or Castle. Keep
		# the source area's bed beneath its portable play-session cue.
		return
	if amb == "" or not ResourceLoader.exists(amb):
		m.ambience.stop()
		return
	var st2: AudioStream = load(amb)
	if st2 is AudioStreamOggVorbis:
		(st2 as AudioStreamOggVorbis).loop = true
	if m.ambience.stream != st2 or not m.ambience.playing:
		m.ambience.stream = st2
		m.ambience.volume_db = -10.0
		m.ambience.play()


func _tick_ambience_duck(delta: float) -> void:
	var talking := false
	for vp in m.voice_pool:
		if (vp as AudioStreamPlayer).playing:
			talking = true
			break
	# family voices also duck the music: lerp toward base (-8) plus a duck
	# offset. Re-anchoring on the -8 base means _play_music resetting
	# volume_db to -8 on a track change never fights the duck — the next
	# frame simply lerps from wherever the volume is. Skipped entirely when
	# music is muted (-60) so the duck can't drag a muted track audible.
	if m.music != null and m.music.playing and m.music_on:
		var mwant: float = -8.0 + (-6.0 if talking else 0.0)
		m.music.volume_db = lerpf(m.music.volume_db, mwant, minf(1.0, delta * 6.0))
	if m.ambience == null or not m.ambience.playing:
		return
	var want: float = -16.0 if talking else -10.0
	m.ambience.volume_db = lerpf(m.ambience.volume_db, want, minf(1.0, delta * 6.0))

# Combat pop with the chain pitch ladder (COMBO_SYSTEM): chain 1/2/3 climb
# a step each, 4 is the SUPER top. A dedicated player so combo pitch never
# fights the global button-tap hook. Combat has its own pop voice
# (synthesized pack, tools/gen_combat_sfx.py); ui_tap remains the fallback
# so a missing pack degrades to the old sound, never to silence.
const POP_PITCH: Array[float] = [1.0, 1.15, 1.3, 1.4]
const SFX_ROOT := "res://assets/audio/sfx/"


func pop(level: int) -> void:
	if m._pop_player == null:
		m._pop_player = AudioStreamPlayer.new()
		m._pop_player.bus = "UI"
		var pop_path: String = SFX_ROOT + "combat_pop.wav"
		if ResourceLoader.exists(pop_path):
			m._pop_player.stream = load(pop_path)
		else:
			m._pop_player.stream = load("res://assets/audio/ui_tap.ogg")
		m._pop_player.volume_db = -6.0
		m._pop_player.process_mode = Node.PROCESS_MODE_ALWAYS
		m.add_child(m._pop_player)
	m._pop_player.pitch_scale = POP_PITCH[clampi(level - 1, 0, POP_PITCH.size() - 1)]
	m._pop_player.play()


# The combat reaction voice: bonks, poofs, tinkles, fizzles. A tiny
# rotating pool so rapid hits never cut each other off; every call degrades
# to silence gracefully when a file is absent, so owner-recorded
# replacements can drop in at the same paths any time.
func sfx(name: String, pitch: float = 1.0, volume_db: float = -6.0) -> void:
	var path: String = SFX_ROOT + name + ".wav"
	if not ResourceLoader.exists(path):
		return
	if m._sfx_pool.is_empty():
		for _i in range(4):
			var ap := AudioStreamPlayer.new()
			ap.bus = "SFX"
			ap.process_mode = Node.PROCESS_MODE_ALWAYS
			m.add_child(ap)
			m._sfx_pool.append(ap)
	var player: AudioStreamPlayer = m._sfx_pool[m._sfx_i % m._sfx_pool.size()]
	m._sfx_i += 1
	if player.stream == null or player.stream.resource_path != path:
		player.stream = load(path)
	player.pitch_scale = pitch
	player.volume_db = volume_db
	player.play()


func _ui_tap() -> void:
	if m._tap_player == null:
		m._tap_player = AudioStreamPlayer.new()
		m._tap_player.bus = "UI"
		m._tap_player.stream = load("res://assets/audio/ui_tap.ogg")
		m._tap_player.volume_db = -8.0
		m._tap_player.process_mode = Node.PROCESS_MODE_ALWAYS
		m.add_child(m._tap_player)
	m._tap_player.play()


func _hook_button_taps(n: Node) -> void:
	# every Button anywhere in the game gets the soft bubble tap — one global
	# hook on node_added instead of wiring hundreds of creation sites
	if n is Button and not bool(n.get_meta("uses_own_sfx", false)):
		(n as Button).pressed.connect(m._ui_tap)


func _play_music(track: String, loop: bool = true) -> void:
	# night flips the reef to its dreamier track (Prairie Nights)
	var fname := track
	if track == "world" and m.is_night and ResourceLoader.exists("res://assets/audio/music/world_night.ogg"):
		fname = "world_night"
	var mpath := "res://assets/audio/music/" + fname + ".ogg"
	if not ResourceLoader.exists(mpath):
		return   # no track for this kind (e.g. transient arena setup) — keep current music
	if m.cur_track == track and m.music != null and m.music.playing \
			and m.music.stream != null \
			and m.music.stream.resource_path == mpath:
		_set_ambience(track)
		return
	# cur_track describes what can actually be restored. Setting it before the
	# existence check made a missing transient cue poison nested return paths
	# even though the audible stream correctly kept playing.
	m.cur_track = track
	_set_ambience(track)
	var st: AudioStream = load(mpath)
	if st is AudioStreamOggVorbis:
		# loop=false for one-shot stingers (finale, castle_open) so a short
		# fanfare doesn't wrap around; their call sites restore ongoing music
		(st as AudioStreamOggVorbis).loop = loop
	m.music.stream = st
	m.music.volume_db = -8.0 if m.music_on else -60.0
	m.music.play()
