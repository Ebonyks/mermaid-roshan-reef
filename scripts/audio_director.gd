class_name AudioDirector
extends RefCounted
# Phase 7.5: mechanical extraction of the audio pipeline from main.gd —
# music track switching (night-aware), the ambience bed + voice ducking,
# the global UI tap hook and the _say/show_msg voice pipeline. All state
# (players, pools, cur_track) stays on main; received by reference.

var m: ReefMain
var _active_speaker := ""
var _day_one_context_catalog: Dictionary = {}
var _day_one_context_seen: Dictionary = {}
var _day_one_context_active_key := ""
var _active_required_key := ""
var _required_voice_queue: Array[Dictionary] = []
const FILLER_VOICE_DIR := "res://assets/audio/voices/filler_v1/"
const LEGACY_VOICE_DIR := "res://assets/audio/voices/"
const DAY_ONE_CONTEXT_CATALOG_SCRIPT: GDScript = preload(
	"res://scripts/day_one_contextual_voice_catalog.gd")
const RETIRED_OVERLAY_CONTEXT_CUES: Dictionary = {
	"day1_boss_dodge_prompt": true,
}

# These are the existing, manifest-backed semantic suffixes used by the Day
# One route.  Keep this list explicit: a required objective may never silently
# fall through to roshan_talk, roshan_win, or the retired yay fallback.
const DAY_ONE_REQUIRED_EVENTS: Dictionary = {
	"castle_home_day_one": true,
	"castle_door_resting": true,
	"day_one_jobs_resting": true,
	"day_one_rescue_bunnies": true,
	"day_one_finish_current": true,
	"day_one_room_clean": true,
	"day_one_new_door": true,
	"day_one_all_rooms_clean": true,
	"day_one_pool_ready": true,
	"bathroom_supplies_found": true,
	"bathroom_cleanup_start": true,
	"bathroom_basket_hint": true,
	"bathroom_sink_scrub": true,
	"bathroom_tub_drain": true,
	"bathroom_tub_brush": true,
	"bathroom_cleanup_done": true,
	"pool_surface_clean": true,
	"pool_waterfall_clean": true,
	"pool_seahorse_clean": true,
	"castle_playroom_rescue_start": true,
	"art_studio_hint": true,
	"art_studio_material_hint": true,
	"art_studio_scrub_hint": true,
	"dustboss_show": true,
	"dustboss_tell_opening": true,
	"dustboss_tell_shielded": true,
	"dustboss_again_miss": true,
	"dustboss_again_closer": true,
	"dustboss_again_mercy": true,
	"dustboss_dizzy_first": true,
	"dustboss_dizzy_round": true,
	"dustboss_angry": true,
	"dustboss_win": true,
	"day_two_begins": true,
}

func _init(main: ReefMain) -> void:
	m = main


func _load_day_one_context_catalog() -> Dictionary:
	if not _day_one_context_catalog.is_empty():
		return _day_one_context_catalog
	var runtime_catalog: RefCounted = DAY_ONE_CONTEXT_CATALOG_SCRIPT.new() as RefCounted
	if runtime_catalog == null or not runtime_catalog.has_method("catalog"):
		return {}
	var parsed: Variant = runtime_catalog.call("catalog")
	if parsed is Dictionary:
		_day_one_context_catalog = parsed as Dictionary
	return _day_one_context_catalog


func day_one_context_catalog() -> Dictionary:
	return _load_day_one_context_catalog().duplicate(true)


func _day_one_context_row(cue_id: String, variant: int) -> Dictionary:
	var catalog := _load_day_one_context_catalog()
	var rows: Variant = catalog.get("rows", [])
	if not rows is Array:
		return {}
	for row_value: Variant in rows:
		if not row_value is Dictionary:
			continue
		var row := row_value as Dictionary
		if String(row.get("cue_id", "")) != cue_id:
			continue
		var row_variant := int(row.get("variant", 0))
		if row_variant == variant:
			return row
		if not row.has("variant") and variant == 0:
			return row
	return {}


func _present_day_one_context_caption(caption: String, cue_id: String,
		missing: bool) -> void:
	if m.hud_msg == null:
		return
	m.hud_msg.text = caption
	m.hud_msg.visible = caption != ""
	m.msg_timer = 5.0
	m.hud_msg.set_meta("contextual_audio_missing", missing)
	m.hud_msg.set_meta("requested_contextual_voice_key", cue_id)


func _retain_day_one_context_caption(caption: String, cue_id: String) -> void:
	_present_day_one_context_caption(caption, cue_id, true)


## Play one exact, situation-owned Day One Roshan take.
##
## This is deliberately separate from _say(): a governed cue may never fall
## back to speaker/talk/win/yay. If its exact take is absent or still pending,
## the caption and any caller-owned pointer remain visible and this returns
## false. session_id and room_id provide replay policy without touching save
## state; callers can use a fresh session id when a video or room visit starts.
func say_day_one_context(cue_id: String, caption: String = "",
		room_id: String = "", session_id: String = "", variant: int = 0,
		allow_generic: bool = false) -> bool:
	if allow_generic or cue_id.strip_edges() == "":
		_retain_day_one_context_caption(caption, cue_id)
		return false
	# Mastered audio remains preserved for provenance, but retired cues that
	# name removed overlay controls must never become playable again.
	if bool(RETIRED_OVERLAY_CONTEXT_CUES.get(cue_id, false)):
		_retain_day_one_context_caption(caption, cue_id)
		return false
	var row := _day_one_context_row(cue_id, variant)
	if row.is_empty() or String(row.get("route", "")) == "":
		_retain_day_one_context_caption(caption, cue_id)
		return false
	var resolved_caption := caption if caption != "" else String(row.get("caption", ""))
	var policy := String(row.get("policy", "once_per_session"))
	var visit := session_id if session_id != "" else "runtime"
	var dedupe_key := visit + "|" + cue_id
	if policy == "once_per_room_visit":
		dedupe_key = visit + "|" + room_id + "|" + cue_id
	elif policy == "repeat_variant":
		dedupe_key = visit + "|" + room_id + "|" + cue_id + "|" + str(variant)
	if bool(_day_one_context_seen.get(dedupe_key, false)):
		return false
	var audio_path := String(row.get("audio_path", ""))
	var resource_path := "res://" + audio_path if not audio_path.begins_with("res://") \
		else audio_path
	if String(row.get("status", "")) != "READY" \
			or not ResourceLoader.exists(resource_path):
		_retain_day_one_context_caption(resolved_caption, cue_id)
		return false
	var stream := load(resource_path) as AudioStream
	if stream == null:
		_retain_day_one_context_caption(resolved_caption, cue_id)
		return false
	# A repeated signal for the currently audible exact cue is a no-op. A new
	# contextual cue owns the single voice lane and serially replaces the old
	# line, matching the existing non-governed dialogue contract.
	if _day_one_context_active_key == dedupe_key and _has_active_speech():
		return false
	_stop_active_speech()
	if m.voice_pool.is_empty():
		_retain_day_one_context_caption(resolved_caption, cue_id)
		return false
	var ap: AudioStreamPlayer = m.voice_pool[m.voice_i % m.voice_pool.size()]
	m.voice_i += 1
	ap.stream = stream
	ap.pitch_scale = 1.0
	ap.play()
	_active_speaker = "roshan"
	_day_one_context_active_key = dedupe_key
	_day_one_context_seen[dedupe_key] = true
	_present_day_one_context_caption(resolved_caption, cue_id, false)
	return true


## Clear the in-memory replay guard when a room or paired video tears down.
## This does not touch save state; a caller can reset one session or all local
## context history before starting a new audition.
func reset_day_one_context(session_id: String = "") -> void:
	if session_id == "":
		_day_one_context_seen.clear()
	else:
		for key: String in _day_one_context_seen.keys():
			if key.begins_with(session_id + "|"):
				_day_one_context_seen.erase(key)
	_day_one_context_active_key = ""


func _voice_path(speaker: String, event: String = "", allow_generic: bool = true) -> String:
	# Callers pass an event suffix. Accepting a mistakenly prefixed suffix here
	# keeps the resolver fail-safe while making the prefix ownership explicit.
	var event_suffix := event
	var speaker_prefix := speaker + "_"
	if event_suffix.begins_with(speaker_prefix):
		event_suffix = event_suffix.trim_prefix(speaker_prefix)
	var key := speaker + ("_" + event_suffix if event_suffix != "" else "")
	# Day One's persistent Rumi greeting deliberately stays in Roshan's voice
	# until an owner-approved Rumi identity recording exists. Reuse the approved
	# Roshan acknowledgement; never synthesize or pitch a new Rumi identity.
	if key == "roshan_day_one_rumi_hi":
		key = "roshan_talk"
	var protected_speaker := speaker in ["faron", "daddy", "chuck"]
	# Daddy's numbered family recordings remain protected and win through their
	# exact legacy keys. Synthetic filler is allowed only for a named Daddy event
	# that has no family recording; never use a generic synthetic Daddy fallback.
	var allow_exact_filler := not protected_speaker or speaker == "daddy"
	var candidates: Array[String] = []
	if allow_exact_filler:
		candidates.append(FILLER_VOICE_DIR + key + ".ogg")
	candidates.append(LEGACY_VOICE_DIR + key + ".ogg")
	if allow_generic and event_suffix != "":
		if not protected_speaker:
			candidates.append(FILLER_VOICE_DIR + speaker + ".ogg")
		candidates.append(LEGACY_VOICE_DIR + speaker + ".ogg")
	for path: String in candidates:
		if ResourceLoader.exists(path):
			return path
	return ""


func _is_required_day_one_event(event: String) -> bool:
	return bool(DAY_ONE_REQUIRED_EVENTS.get(event, false))

func _say(speaker: String, event: String = "", min_gap: float = 0.0) -> void:
	var event_suffix := event.trim_prefix(speaker + "_")
	var key := speaker + "_" + event_suffix
	if min_gap > 0.0:
		var now := Time.get_ticks_msec() / 1000.0
		if now - float(m.said_cool.get(key, -99.0)) < min_gap:
			return
		m.said_cool[key] = now
	# A required line owns the single objective voice channel. If another exact
	# objective arrives in the same frame, retain it in FIFO order; generic talk
	# and win are ignored until the required line has finished.
	var required := _is_required_day_one_event(event_suffix)
	if _flush_required_queue():
		return
	var exact_path := _voice_path(speaker, event_suffix, false)
	if required and exact_path == "":
		# Missing exact audio is an explicit pending gap, never a generic fallback.
		return
	if not required and _active_required_key != "" and _has_active_speech():
		return
	if required and _active_required_key != "" and _has_active_speech():
		if key != _active_required_key and _required_voice_queue.size() < 2:
			_required_voice_queue.append({"speaker": speaker, "event": event,
				"min_gap": min_gap})
		return
	# Prefer the machine-screened provisional filler for this exact line. Protected
	# recordings and legacy synthetic clips remain intact as fallback assets.
	var stream: AudioStream = null
	var path := exact_path if required else _voice_path(speaker, event_suffix)
	if path != "":
		stream = load(path)
	if stream != null:
		var protected_exact := speaker in ["faron", "daddy", "chuck"] \
			and path == LEGACY_VOICE_DIR + key + ".ogg"
		# Discovery/focus paths can request two semantic keys for the same
		# character within one frame. Let the first complete; never interrupt a
		# sentence with a second take from that same speaker. An exact protected
		# family cue remains authoritative and may replace a generic greeting.
		if _active_speaker == speaker and _has_active_speech() and not protected_exact:
			return
		# Different semantic keys can resolve to the same family fallback clip
		# when an exact take is unavailable. Never restart an
		# identical recording on a second pool player while the first is audible.
		for voice_player_value: Variant in m.voice_pool:
			var active_player := voice_player_value as AudioStreamPlayer
			if active_player != null and active_player.playing \
					and active_player.stream == stream:
				return
	# Spoken guidance is serial: a new semantic line replaces the prior voice
	# instead of producing two intelligible-but-cluttered speakers at once.
	_stop_active_speech()
	# Headless/state-only callers can construct ReefMain without its scene-owned
	# voice pool.  Voice is optional feedback; an empty pool must never turn a
	# valid gameplay action into a modulo-by-zero runtime error.
	if m.voice_pool.is_empty():
		if m.voice != null:
			m.voice.pitch_scale = float(m.VOICE_PITCH.get(speaker, 1.0))
			m.voice.play()
			_active_speaker = speaker
		return
	var ap: AudioStreamPlayer = m.voice_pool[m.voice_i % m.voice_pool.size()]
	m.voice_i += 1
	if stream != null:
		ap.stream = stream
		ap.pitch_scale = 1.0
		ap.play()
		_active_speaker = speaker
		_active_required_key = key if required else ""
	elif m.voice != null:
		# graceful fallback until real clips are dropped in: the recorded "yay",
		# pitched to give each character a recognisably different timbre
		m.voice.pitch_scale = float(m.VOICE_PITCH.get(speaker, 1.0))
		m.voice.play()
		_active_speaker = speaker


func play_companion_chirp(speaker: String = "sparkle") -> void:
	# Companion reactions are short, non-objective chirps. Keep them on an idle
	# pool player so the Roshan objective sentence remains intact.
	var path := _voice_path(speaker, "", false)
	if path == "":
		return
	var stream := load(path) as AudioStream
	if stream == null:
		return
	for voice_player_value: Variant in m.voice_pool:
		var voice_player := voice_player_value as AudioStreamPlayer
		if voice_player != null and not voice_player.playing:
			voice_player.stream = stream
			voice_player.pitch_scale = 1.0
			voice_player.play()
			return


func _flush_required_queue() -> bool:
	if _active_required_key == "" or _has_active_speech():
		return false
	_active_required_key = ""
	if _required_voice_queue.is_empty():
		return false
	var pending: Dictionary = _required_voice_queue.pop_front()
	_say(String(pending.get("speaker", "roshan")),
		String(pending.get("event", "")),
		float(pending.get("min_gap", 0.0)))
	return true


func tick_voice() -> void:
	_flush_required_queue()


func play_success_yay(pitch_scale: float = 1.0) -> void:
	# Success chirps share the same serialization contract as spoken guidance.
	# The stream is the new synthetic filler cue configured by ReefMain, never
	# the retired voice_yay.mp3 fallback.
	if _active_required_key != "" and _has_active_speech():
		return
	_stop_active_speech()
	if m.voice == null:
		return
	var path := FILLER_VOICE_DIR + "yay.ogg"
	if ResourceLoader.exists(path):
		m.voice.stream = load(path)
	m.voice.pitch_scale = pitch_scale
	m.voice.play()
	_active_speaker = "yay"


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
	_active_speaker = ""
	_day_one_context_active_key = ""
	_active_required_key = ""
	_required_voice_queue.clear()


func _has_active_speech() -> bool:
	for voice_player_value: Variant in m.voice_pool:
		var voice_player := voice_player_value as AudioStreamPlayer
		if voice_player != null and voice_player.playing:
			return true
	return m.voice != null and m.voice.playing


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


func show_msg(who: String, txt: String, vo: String = "talk",
		voice_min_gap: float = 0.5) -> void:
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
		var has_exact := vo != "talk" and _voice_path(speaker, vo, false) != ""
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
		m.hud_msg.set_meta("voice_recording_gap",
			not has_exact and txt != "")
		m.hud_msg.set_meta("requested_voice_key", vo)
		# A generic speaker clip or pitched yay cannot truthfully instruct a
		# nonreader. In Opera, play only the exact semantic recording; otherwise
		# leave the visual pointer and reading-aid caption present.
		if who != "" and has_exact:
			_say(speaker, vo, voice_min_gap)
		return
	m.hud_msg.text = txt
	m.hud_msg.visible = txt != ""
	m.msg_timer = 5.0
	if who != "":
		_say(_speaker_key(who), vo, voice_min_gap)
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
	# State-only probes may exercise a controller before its ReefMain owner is
	# mounted. AudioStreamPlayer.play() emits a noisy tree-membership error in
	# that case; a real mounted game still gets the same tap cue.
	if m == null or not m.is_inside_tree():
		return
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
