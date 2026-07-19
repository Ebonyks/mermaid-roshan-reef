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


func _speaker_key(who: String) -> String:
	var w := who.to_lower()
	if "rosalina" in w: return "rosalina"
	if "roshan" in w: return "roshan"
	if "huluu" in w: return "huluu"
	if "evie" in w or "lamb" in w: return "evie"
	if "harper" in w or "fiona" in w: return "harper"
	if "faron" in w: return "faron"
	if "gabby" in w: return "gabby"
	if "chuck" in w: return "chuck"
	if "wacky" in w: return "wacky"
	if "shop" in w: return "shop"
	if "sparkle" in w or "eagle" in w: return "sparkle"
	if "mewsha" in w or "kitty" in w: return "mewsha"
	if "everyone" in w: return "everyone"
	return "roshan"


func show_msg(who: String, txt: String, vo: String = "talk") -> void:
	m.hud_msg.text = txt
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
	m.chime.pitch_scale = 0.9
	m.chime.play()
	m.get_tree().create_timer(0.16).timeout.connect(func():
		if m.chime != null:
			m.chime.pitch_scale = 1.12
			m.chime.play())
	m.get_tree().create_timer(0.34).timeout.connect(func():
		if m.chime != null:
			m.chime.pitch_scale = 1.35
			m.chime.play())


func _set_ambience(track: String) -> void:
	# a quiet world bed under the music: underwater in the reef, breeze +
	# birds in the lagoon, airy room tone in the castle. Ducks -6dB under voices.
	if m.ambience == null:
		m.ambience = AudioStreamPlayer.new()
		m.ambience.bus = "Ambience"
		m.add_child(m.ambience)
	var amb := ""
	match track:
		"world", "finale":
			amb = "res://assets/audio/ambience_reef.ogg"
		"level2", "castle_open":
			amb = "res://assets/audio/ambience_lagoon.ogg"
		"hall", "home":
			amb = "res://assets/audio/ambience_hall.ogg"
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
	if m.ambience == null or not m.ambience.playing:
		return
	var talking := false
	for vp in m.voice_pool:
		if (vp as AudioStreamPlayer).playing:
			talking = true
			break
	var want: float = -16.0 if talking else -10.0
	m.ambience.volume_db = lerpf(m.ambience.volume_db, want, minf(1.0, delta * 6.0))


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
	if n is Button:
		(n as Button).pressed.connect(m._ui_tap)


func _play_music(track: String) -> void:
	m.cur_track = track
	# night flips the reef to its dreamier track (Prairie Nights)
	var fname := track
	if track == "world" and m.is_night and ResourceLoader.exists("res://assets/audio/music/world_night.ogg"):
		fname = "world_night"
	_set_ambience(track)
	var mpath := "res://assets/audio/music/" + fname + ".ogg"
	if not ResourceLoader.exists(mpath):
		return   # no track for this kind (e.g. transient arena setup) — keep current music
	var st: AudioStream = load(mpath)
	if st is AudioStreamOggVorbis:
		(st as AudioStreamOggVorbis).loop = true
	m.music.stream = st
	m.music.volume_db = -8.0 if m.music_on else -60.0
	m.music.play()
