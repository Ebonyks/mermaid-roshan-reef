class_name DustBossGame
extends RefCounted
# Grand Puff teaches one repeating rule: leave every painted danger shape,
# then tap the flashing head once. Damage costs time and mastery but never
# progress or life. Targets lock when their tell begins and never home.
const HP := DustBunnyBossSprite.TOTAL_DAMAGE_ROUNDS
const BossSplash2DLogic = preload("res://scripts/boss_splash_2d.gd")
const DustBossTelegraph2DLogic = preload("res://scripts/dust_boss_telegraph_2d.gd")
const ATTIC_BACKDROP = preload("res://assets/flats/castle/boss/dusty_attic_arena_2048.png")

const SHOW_T := 6.4            # the showing: he is revealed before he fights
const SHOW_SKIP_T := 5.2       # the demo flash must have played before skipping
const LANDED_ROUND_HOLD_T := 5.4 # one bounded, child-readable landed-round hold
const WIN_T := 3.4             # befriending beat before the win banner
const POSITIVE_PACING_FLOOR := 38.0 # quick completions still get a warm ending

const LEAP_H := 7.6            # existing contact-shadow scale reference
const HOP_H := 2.4
const BOSS_H := 17.0           # on-screen height of the animated CARD. The
                               # authored frames carry dust plumes and padding,
                               # so the bunny inside reads at roughly 0.6 of
                               # this — about 10 units against Roshan's ~7,
                               # which is the size difference a boss needs.
                               # The stage re-solves its framing from this.
const RADIUS := 26.0           # the ring's circumradius (apothem ≈ 24.0)
const BOSS_INSET := 4.5        # how far inside the wall the boss may land

const FEEDBACK_COOLDOWN := 2.6       # one clear cue, then a quiet learning pause
const CLOSER_FEEDBACK_COOLDOWN := 2.8
const BASE_WIN_PEARLS := 3
const PERFECT_BONUS_PEARLS := 2
const DAMAGE_RECOVERY_T: float = 1.05

# Grand Puff owns a deterministic 120 BPM adaptive cue. The rendered track's
# beat 16 is the unmistakable action downbeat. The actual vulnerable animation
# signal corrects to beat 16 so audio and the gold flash remain one event.
const MUSIC_SECONDS_PER_BEAT := 0.5
const MUSIC_ACTION_BEAT := 16.0
const MUSIC_ACTION_T := MUSIC_ACTION_BEAT * MUSIC_SECONDS_PER_BEAT
const MUSIC_SHOW_FLASH_T := 3.2
const MUSIC_OPEN_FRAME_T := 0.2
const MUSIC_SYNC_TOLERANCE := 0.08

const MASTERY_GOLD := 3
const MASTERY_SILVER := 2
const MASTERY_BRONZE := 1
const MASTERY_COLORS: Dictionary = {
	MASTERY_GOLD: Color(1.0, 0.78, 0.20),
	MASTERY_SILVER: Color(0.76, 0.86, 0.96),
	MASTERY_BRONZE: Color(0.83, 0.48, 0.28),
}

# ---- the boss art contract -------------------------------------------------
# One cutout per BEAT, not one cutout for the whole fight. Codex delivered the
# sheets on 2026-08-02 (see BOSS_ART_INTEGRATION_2026-08-02.md for the cell
# map); each pose below is optional, and any file that is not present falls
# back to BOSS_FALLBACK_TEX, so the encounter runs identically whether none,
# some or all of the art has landed.
const BOSS_ART_DIR := "res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/boss/"
# The tell is its own art too: a closed badge and an open badge that read as
# DIFFERENT OBJECTS, not one badge at two alphas.
const TELL_OPEN_TEX := BOSS_ART_DIR + "boss_tell_open.png"
const TELL_SHUT_TEX := BOSS_ART_DIR + "boss_tell_shielded.png"
const STAR_TEX := "res://assets/mg/star.png"   # fallback tell (generic reward star)

const PHASE_ART: Dictionary = {
	&"puffy": {"name": "puffy", "puff": 1.0},
	&"dizzy": {"name": "dizzy", "puff": 0.96},
	&"angry": {"name": "angry", "puff": 1.12},
}

var m: ReefMain
var stage: OctagonStage
var _day_one_voice_session: String = "boss_visit_0"
var attack_feedback: HitEngine = null
var encounter := BossEncounter2D.new()
var patterns: EncounterPatterns2D = null
var navigation := EncounterNavigation2D.new()
var _projection_size := Vector2.ZERO
var _caption_position := Vector2.ZERO
var _caption_size := Vector2.ZERO
var _caption_style: StyleBox = null
var _warning_points := PackedVector2Array()
var _safe_destination := Vector2.ZERO
var _telegraph_data: Dictionary = {}

func _init(main: ReefMain) -> void:
	m = main
	stage = OctagonStage.new(main)
	encounter.configure(EncounterProfile2D.grand_puff())
	patterns = encounter.patterns


func _say_day_one_context(cue_id: String, caption: String,
		variant: int = 0) -> void:
	m.say_day_one_context(cue_id, caption, "boss", _day_one_voice_session,
		variant, false)

# ---- lifecycle -------------------------------------------------------------
func build(fr: Dictionary, _origin: Vector3) -> void:
	var voice_visit: int = int(m.g.get("day_one_boss_voice_visit_count", 0)) + 1
	m.g["day_one_boss_voice_visit_count"] = voice_visit
	_day_one_voice_session = "boss_visit_%d" % voice_visit
	_ensure_attack_feedback()
	m.g["db_hits"] = 0
	m.g["db_miss"] = 0
	m.g["db_miss_streak"] = 0
	m.g["db_bumps"] = 0
	m.g["db_perfect_bonus"] = false
	m.g["db_shield_taps"] = 0
	m.g["db_shield_feedbacks"] = 0
	m.g["db_closer_taps"] = 0
	m.g["db_feedback_cd"] = 0.0
	m.g["db_closer_cd"] = 0.0
	m.g["db_taps_this_round"] = 0
	m.g["db_x"] = 0.0
	m.g["db_z"] = -12.0
	m.g["db_y"] = 0.0
	m.g["db_from"] = Vector2(0.0, -12.0)
	m.g["db_to"] = Vector2(0.0, -12.0)
	m.g["db_spin"] = 0.0
	m.g["db_flash"] = 0.0
	m.g["db_active_t"] = 0.0
	m.g["db_music_action_cues"] = 0
	m.g["db_music_seek_t"] = 0.0
	m.g["db_music_action_drift"] = 0.0
	m.g["db_damage_taken"] = 0
	m.g["db_avoids"] = 0
	m.g["db_dust_charge"] = 0
	m.g["db_opening_misses"] = 0
	m.g["db_attack_hit"] = false
	_stage_open()
	_build_mastery_ui()
	_build_boss()
	_restore_round_checkpoint()
	_enter_state("splash")
	_update_mastery_ui()
	_show_boss_splash(fr)


func _restore_round_checkpoint() -> void:
	var restored: int = clampi(int(m.save_data.get(
		"dustboss_pending_rounds", 0)), 0, HP)
	m.g["db_hits"] = restored
	m.g["db_damage_taken"] = maxi(0, int(m.save_data.get(
		"dustboss_pending_damage", 0)))
	m.g["db_bumps"] = int(m.g["db_damage_taken"])
	m.g["db_opening_misses"] = maxi(0, int(m.save_data.get(
		"dustboss_pending_misses", 0)))
	encounter.configure(EncounterProfile2D.grand_puff(), restored,
		int(m.g["db_damage_taken"]), int(m.g["db_opening_misses"]))
	patterns = encounter.patterns
	var k: DustBunnyBossSprite = kit()
	if k == null or not is_instance_valid(k):
		return
	k.damage_rounds_completed = restored
	k.boss_health_rounds_remaining = HP - restored
	k.final_round_active = restored >= HP - 1
	k.combat_speed_scale = DustBunnyBossSprite.FINAL_ROUND_SPEED_SCALE \
		if k.final_round_active else 1.0

func action_label() -> String:
	# the only verb in this fight is a bonk; the shared reef button otherwise
	# reads "JUMP" with an up-arrow for the whole encounter
	var k: DustBunnyBossSprite = kit()
	return "BONK!" if String(m.g.get("db_state", "")) == "vuln" \
		and k != null and is_instance_valid(k) and k.vulnerable else "WAIT"


func danger_geometry() -> Dictionary:
	if patterns == null:
		return {"active": false}
	var result: Dictionary = patterns.readout()
	result["active"] = String(m.g.get("db_state", "")) == "tell"
	result["safe_point"] = _safe_destination
	return result

func stage_close() -> void:
	navigation.cancel()
	if m.touch_ui != null:
		m.touch_ui.set_encounter_controls()
	if m.hud_msg != null and _caption_style != null:
		m.hud_msg.position = _caption_position
		m.hud_msg.size = _caption_size
		m.hud_msg.add_theme_stylebox_override("normal", _caption_style)
	var attic_layer: CanvasLayer = m.g.get("db_attic_layer") as CanvasLayer
	if attic_layer != null and is_instance_valid(attic_layer):
		attic_layer.visible = false
		attic_layer.queue_free()
	if m.player != null and m.player.classic_sprite != null \
			and m.g.has("db_player_draw_priority"):
		m.player.classic_sprite.render_priority = int(m.g["db_player_draw_priority"])
		m.player.classic_sprite.no_depth_test = bool(m.g["db_player_depth_override"])
		m.g.erase("db_player_draw_priority")
		m.g.erase("db_player_depth_override")
	var splash: BossSplash2D = m.g.get("db_splash") as BossSplash2D
	if splash != null and is_instance_valid(splash):
		splash.cancel()
	var mastery_layer: CanvasLayer = m.g.get("db_mastery_layer") as CanvasLayer
	if mastery_layer != null and is_instance_valid(mastery_layer):
		mastery_layer.visible = false
		mastery_layer.queue_free()
	stage.close()
	if attack_feedback != null:
		attack_feedback.teardown()
	attack_feedback = null
	m.g.erase("db_attack_feedback")

func _ensure_attack_feedback() -> HitEngine:
	if attack_feedback == null:
		attack_feedback = HitEngine.new(m)
		m.g["db_attack_feedback"] = attack_feedback
	return attack_feedback

func _show_attack_feedback() -> void:
	var feedback: HitEngine = _ensure_attack_feedback()
	var viewport: Viewport = m.get_viewport()
	var screen_pos := Vector2(640.0, 360.0)
	if viewport != null:
		screen_pos = viewport.get_visible_rect().get_center()
	var boss: Variant = m.g.get("db_boss")
	var cam: Variant = m.player.cam if m.player != null else null
	if boss != null and is_instance_valid(boss) and cam != null \
			and cam.is_inside_tree() and not cam.is_position_behind(boss.global_position):
		screen_pos = cam.unproject_position(boss.global_position)
	feedback.show_attack_feedback_2d(screen_pos)

static func mastery_tier_for_bumps(bumps: int) -> int:
	# Bumps are harmless and never gate completion. They only leave an inviting
	# replay target: one is still gold, two is silver, and three-plus is bronze.
	if bumps <= 1:
		return MASTERY_GOLD
	if bumps == 2:
		return MASTERY_SILVER
	return MASTERY_BRONZE

func mastery_tier() -> int:
	return mastery_tier_for_bumps(int(m.g.get("db_bumps", 0)))

func tick(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var r := stage.root()
	if r == null:
		return
	# the real one-finger read: walk the ring, tap = THE button. Damage can
	# only ever come from a fresh tap edge here, so a zero-input run cannot
	# scratch him (probe_passive).
	_update_projection()
	var s: Dictionary = stage.tick(delta, navigation)
	var tapped: bool = bool(s["tap"])
	m.g["db_feedback_cd"] = maxf(0.0,
		float(m.g.get("db_feedback_cd", 0.0)) - delta)
	m.g["db_closer_cd"] = maxf(0.0,
		float(m.g.get("db_closer_cd", 0.0)) - delta)
	if String(m.g.get("db_state", "showing")) != "showing":
		m.g["db_active_t"] = float(m.g.get("db_active_t", 0.0)) + delta
	m.g["db_st"] = float(m.g.get("db_st", 0.0)) + delta
	var st: float = float(m.g["db_st"])
	match String(m.g.get("db_state", "showing")):
		"splash":
			pass
		"showing":
			_tick_showing(st, fr, tapped)
		"tell":
			_tick_attack_tell(delta, tapped)
		"strike":
			_tick_attack_strike(st, tapped)
		"damage_recovery":
			_tick_damage_recovery(st, tapped)
		"vuln":
			_tick_counter_opening(delta, tapped)
		"struck":
			_tick_struck(delta, st, fr, tapped)
		"friends":
			_tick_friends(st, fr, tapped)
	if m.g.is_empty():
		return                      # the win banner fired and wiped the scratch
	_place_boss(delta)
	_update_hud()
	_update_mastery_ui()


func _show_boss_splash(fr: Dictionary) -> void:
	var splash := BossSplash2DLogic.new() as BossSplash2D
	if splash == null:
		_begin_showing(fr)
		return
	var badge: Texture2D = load(STAR_TEX) as Texture2D
	splash.configure(
		DustBunnyBossSprite.make_sprite_frames(),
		"GRAND PUFF",
		"THE GREAT DUST BUNNY",
		badge, ATTIC_BACKDROP)
	splash.finished.connect(_on_boss_splash_finished.bind(fr), CONNECT_ONE_SHOT)
	m.add_child(splash)
	m.g["db_splash"] = splash


func _on_boss_splash_finished(fr: Dictionary) -> void:
	if m.game != "dustboss" or m.g.is_empty():
		return
	m.g["db_splash"] = null
	if int(m.g.get("db_hits", 0)) >= HP:
		# All counters were earned before the interruption. Resume the ending,
		# not another attack; its normal save atomically grants and clears once.
		m.g["db_active_t"] = POSITIVE_PACING_FLOOR
		_enter_state("friends")
		var k: DustBunnyBossSprite = kit()
		if k != null and is_instance_valid(k):
			k.play_implode()
		return
	_begin_showing(fr)


func _begin_showing(fr: Dictionary) -> void:
	_enter_state("showing")
	_say_day_one_context("day1_boss_intro",
		"The giant dust bunny woke up! It is too fluffy. Sparkle taps will work!")

# ---- the state machine -----------------------------------------------------
func _enter_state(next_state: String) -> void:
	if m.hud_msg != null:
		m.hud_msg.text = ""
		m.msg_timer = 0.0
	m.g["db_state"] = next_state
	m.g["db_st"] = 0.0
	_sync_music_for_state(next_state)


func _music_ready() -> bool:
	return m.music != null and m.music.playing and m.cur_track == "dustboss" \
		and m.music.stream != null \
		and m.music.stream.resource_path == "res://assets/audio/music/dustboss.ogg"


func _music_seek(seconds: float) -> void:
	var target: float = maxf(0.0, seconds)
	m.g["db_music_seek_t"] = target
	if _music_ready():
		m.music.seek(target)


func _music_open_delay() -> float:
	var k: DustBunnyBossSprite = kit()
	var speed: float = 1.0
	if k != null and is_instance_valid(k):
		speed = maxf(0.01, k.combat_speed_scale)
	return MUSIC_OPEN_FRAME_T / speed


func _sync_music_for_state(next_state: String) -> void:
	match next_state:
		"showing":
			# The rehearsal flash receives the same downbeat as real play.
			_music_seek(MUSIC_ACTION_T - MUSIC_SHOW_FLASH_T)
		"tell":
			# Start far enough back in the quiet passage that the animation's
			# first open frame, not merely the state boundary, reaches beat 16.
			_music_seek(MUSIC_ACTION_T - patterns.tell_time \
				- _music_open_delay())


func _on_vulnerability_changed(is_open: bool) -> void:
	if not is_open:
		return
	m.g["db_music_action_cues"] = int(m.g.get("db_music_action_cues", 0)) + 1
	if not _music_ready():
		return
	var drift: float = absf(m.music.get_playback_position() - MUSIC_ACTION_T)
	m.g["db_music_action_drift"] = drift
	# The planned seek normally arrives within a frame. Correct larger decoder
	# or scheduling drift without double-triggering an already-landed downbeat.
	if drift > MUSIC_SYNC_TOLERANCE:
		_music_seek(MUSIC_ACTION_T)

func phase() -> int:
	# 0 puffy → 1 dizzy → 2 angry; clamped so the winning hit reads as angry
	return clampi(encounter.completed_rounds, 0, encounter.profile.phases.size() - 1)

func phase_cfg() -> Dictionary:
	return PHASE_ART.get(encounter.profile.phases[phase()].phase_id, PHASE_ART[&"puffy"])

func _begin_attack_tell() -> void:
	if patterns == null:
		return
	var boss_here := Vector2(float(m.g.get("db_x", 0.0)),
		float(m.g.get("db_z", 0.0)))
	encounter.begin_attack(stage.player_local(), boss_here, RADIUS)
	_prepare_telegraph_geometry()
	m.g["db_attack_hit"] = false
	_enter_state("tell")
	_say_day_one_context("day1_boss_dodge",
		"The big dust bunny is coming closer!")


func _tick_attack_tell(delta: float, tapped: bool) -> void:
	if tapped:
		_bounce_off()
	if patterns == null:
		return
	encounter.tick_tell(delta)
	m.g["db_flash"] = 0.18 + 0.22 * clampf(patterns.elapsed / maxf(patterns.tell_time, 0.01), 0.0, 1.0)
	if patterns.tell_finished():
		encounter.begin_strike()
		m.g["db_attack_hit"] = false
		m.g["db_impact_sampled"] = false
		var shape: String = String(patterns.geometry.get("shape", ""))
		var attack_from := Vector2(float(m.g.get("db_x", 0.0)),
			float(m.g.get("db_z", 0.0)))
		var attack_to: Vector2 = attack_from
		if shape == "circle":
			attack_to = patterns.geometry.get("center", Vector2.ZERO) as Vector2
		else:
			attack_from = patterns.geometry.get("from", attack_from) as Vector2
			attack_to = patterns.geometry.get("to", attack_from) as Vector2
		m.g["db_from"] = attack_from
		m.g["db_to"] = attack_to
		m.g["db_x"] = attack_from.x
		m.g["db_z"] = attack_from.y
		var k: DustBunnyBossSprite = kit()
		var strike_duration: float = 0.6
		if k != null and is_instance_valid(k):
			strike_duration = k.play_jump(1.0 if attack_to.x >= attack_from.x else -1.0)
		m.g["db_strike_duration"] = maxf(0.5, strike_duration)
		_enter_state("strike")


func _tick_attack_strike(st: float, tapped: bool) -> void:
	if tapped:
		_answer_only()
	var duration: float = maxf(0.5, float(m.g.get("db_strike_duration", 0.6)))
	var progress: float = clampf(st / duration, 0.0, 1.0)
	var attack_from: Vector2 = m.g.get("db_from", Vector2.ZERO) as Vector2
	var attack_to: Vector2 = m.g.get("db_to", Vector2.ZERO) as Vector2
	var boss_here: Vector2 = attack_from.lerp(attack_to, progress)
	m.g["db_x"] = boss_here.x
	m.g["db_z"] = boss_here.y
	m.g["db_y"] = sin(progress * PI) * HOP_H
	if st < duration:
		return
	m.g["db_y"] = 0.0
	var impact: BossEncounter2D.Impact = encounter.resolve_impact(
		stage.player_local(), boss_here, RADIUS)
	m.g["db_impact_sampled"] = true
	m.g["db_attack_hit"] = impact == BossEncounter2D.Impact.HIT
	if impact == BossEncounter2D.Impact.HIT:
		m.g["db_damage_taken"] = encounter.damage_taken
		m.save_data["dustboss_pending_damage"] = int(m.g["db_damage_taken"])
		m._write_save()
		m.g["db_dust_charge"] = 0
		m.g["db_bumps"] = int(m.g.get("db_bumps", 0)) + 1
		if m.player != null:
			m.player.play_verb("boing")
		_say_day_one_context("day1_boss_bump", "Grand Puff bounced away!")
		_enter_state("damage_recovery")
		return
	if impact == BossEncounter2D.Impact.IGNORED:
		return
	m.g["db_avoids"] = encounter.avoids
	m.g["db_dust_charge"] = int(m.g.get("db_dust_charge", 0)) + 1
	if impact == BossEncounter2D.Impact.NEXT_TELL:
		_prepare_telegraph_geometry()
		_enter_state("tell")
		_say_day_one_context("day1_boss_dodge",
			"The big dust bunny is coming closer!")
		return
	_begin_counter_opening()


func _tick_damage_recovery(st: float, tapped: bool) -> void:
	if tapped:
		_answer_only()
	m.g["db_flash"] = 0.0
	if st >= DAMAGE_RECOVERY_T:
		_begin_attack_tell()


func _counter_window() -> float:
	return encounter.counter_window()


func _begin_counter_opening() -> void:
	encounter.open_counter()
	var k: DustBunnyBossSprite = kit()
	if k != null and is_instance_valid(k):
		k.configure_counter_mode(_counter_window())
		k.play_vulnerable_laugh()
	m.g["db_flash"] = 0.0
	_enter_state("vuln")
	_say_day_one_context("day1_boss_wait_gold",
		"Wait for the gold star, then tap!")


func _tick_counter_opening(delta: float, tapped: bool) -> void:
	var k: DustBunnyBossSprite = kit()
	var open_now: bool = k != null and is_instance_valid(k) and k.vulnerable
	m.g["db_flash"] = 1.0 if open_now else 0.0
	if tapped and open_now:
		_accept_counter()
		return
	if not encounter.tick_counter(delta, open_now):
		return
	m.g["db_opening_misses"] = encounter.opening_misses
	m.save_data["dustboss_pending_misses"] = int(m.g["db_opening_misses"])
	m._write_save()
	m.g["db_miss"] = int(m.g.get("db_miss", 0)) + 1
	m.g["db_flash"] = 0.0
	if k != null and is_instance_valid(k):
		k.close_vulnerability()
	_begin_attack_tell()

# THE SHOWING — he is revealed before he is ever fought: he swells up out of
# his dust nest, takes one big parade hop, and demonstrates the tell (the star
# flashes) while the voice line and the pointer explain it. Taps do nothing
# here on purpose; the child is being taught, not tested.
func _tick_showing(st: float, fr: Dictionary, tapped: bool) -> void:
	if tapped:
		if st >= SHOW_SKIP_T:
			# A demo flash has already been shown. Let the child's tap move on,
			# while early taps remain a harmless teaching response.
			_begin_attack_tell()
			return
		_answer_only()
	var grow: float = clampf(st / 1.6, 0.0, 1.0)
	m.g["db_show_grow"] = grow
	m.g["db_y"] = sin(clampf((st - 1.8) / 1.4, 0.0, 1.0) * PI) * 5.4
	# the demo flash: exactly what she has to wait for in the real fight
	var demo: bool = st > MUSIC_SHOW_FLASH_T and st < SHOW_SKIP_T
	m.g["db_flash"] = 1.0 if demo else 0.0
	if demo and not bool(m.g.get("db_show_told", false)):
		m.g["db_show_told"] = true
		_say_day_one_context("day1_boss_wait_gold",
			"Wait for the gold star, then tap!")
	if st >= SHOW_T:
		m.g["db_flash"] = 0.0
		_begin_attack_tell()

# The landed counter plays the existing flinch sequence before another attack.
func _tick_struck(delta: float, st: float, fr: Dictionary, tapped: bool) -> void:
	if tapped:
		_answer_only()
	var rounds: int = int(m.g.get("db_hits", 0))
	m.g["db_spin"] = float(m.g.get("db_spin", 0.0)) + 9.0 * delta
	m.g["db_y"] = maxf(0.0, float(m.g.get("db_y", 0.0)) - delta * 22.0)
	m.g["db_flash"] = 0.0
	# the kit is playing flinch_3 -> angry; this hold is the breather the child
	# gets to see what she did before he is moving again
	var hold: float = LANDED_ROUND_HOLD_T
	if rounds >= HP:
		return                     # the friends beat owns the ending
	if st >= hold:
		m.g["db_spin"] = 0.0
		_begin_attack_tell()

# THE ENDING — nobody loses: he deflates into a small cuddly puff, gives back
# the castle's dust in a burst of stars, and the win banner fires.
func _tick_friends(st: float, fr: Dictionary, tapped: bool) -> void:
	if tapped:
		_answer_only()
	m.g["db_y"] = maxf(0.0, float(m.g.get("db_y", 0.0)) - 0.3)
	m.g["db_flash"] = 0.0
	# the kit plays the implosion off flinch_3 and reports when the last wisp
	# is gone; only then is the fight over
	var done: bool = bool(m.g.get("db_imploded", false))
	# db_active_t and this state's st both advance every tick. Gate the floor
	# against the authoritative encounter clock instead of subtracting it into
	# a second advancing hold (which made the remaining floor shrink twice fast).
	var floor_met: bool = float(m.g.get("db_active_t", 0.0)) >= POSITIVE_PACING_FLOOR
	var celebration_ready: bool = st >= WIN_T
	if ((done and floor_met and celebration_ready) \
			or (floor_met and st >= WIN_T + 2.0)) \
			and not bool(m.g.get("db_done", false)):
		m.g["db_done"] = true
		m.save_data["dustboss_pending_rounds"] = 0
		m.save_data["dustboss_pending_damage"] = 0
		m.save_data["dustboss_pending_misses"] = 0
		# The normal victory save commits this reset together with rewards.
		var bumps: int = int(m.g.get("db_bumps", 0))
		var tier: int = mastery_tier_for_bumps(bumps)
		var bonus: int = PERFECT_BONUS_PEARLS if bumps == 0 else 0
		m.g["db_mastery_tier"] = tier
		m.g["db_perfect_bonus"] = bonus > 0
		m.g["db_perfect_bonus_pearls"] = bonus
		m.pearl_count += BASE_WIN_PEARLS + bonus
		m._fanfare()
		m.day_one_complete_boss_and_begin_day_two()
		m._end_game(true, fr, _victory_message(bumps, tier))

func _victory_message(bumps: int, tier: int) -> String:
	if bumps == 0:
		return "PERFECT AVOIDANCE! Three gold stars and two bonus pearls — Grand Puff is your friend!"
	if tier == MASTERY_GOLD:
		return "Three gold stars! Grand Puff is your friend. Avoid every dust attack next time for the shining bonus!"
	if tier == MASTERY_SILVER:
		return "Two silver stars! Grand Puff is your friend. Dodge one more bump next time to light the gold star!"
	return "A bronze star! Grand Puff is your friend. Play again and dodge his hops to light more stars!"

# ---- the verbs -------------------------------------------------------------
func on_world_tap(screen_pos: Vector2) -> void:
	# HYBRID TOUCH: the finger lands ON the boss instead of on the action
	# button. Same verb, and MORE generous — a tap that visibly lands on his
	# card counts as in-reach however far away she is standing.
	if not m.g.has("db_state") or m.game != "dustboss" or m.get_tree().paused:
		return
	var k: DustBunnyBossSprite = kit()
	var on_him: bool = _screen_hit(screen_pos)
	if k != null and is_instance_valid(k) and k.vulnerable \
			and String(m.g.get("db_state", "")) == "vuln":
		if on_him:
			_accept_counter()
			return
	var st_now: String = String(m.g.get("db_state", ""))
	if st_now == "showing" or st_now == "struck" or st_now == "friends":
		_answer_only()   # same answer as the button — see D4
		return
	if on_him:
		_bounce_off()
		return
	var target: Vector2 = navigation.screen_to_floor(screen_pos)
	if String(m.g.get("db_state", "")) == "tell" \
			and screen_pos.distance_to(stage.project_floor_point(_safe_destination)) <= 58.0:
		target = _safe_destination
	navigation.move_to(stage.clamp_point(target, 2.6))

func _accept_counter() -> void:
	var k: DustBunnyBossSprite = kit()
	if k != null and encounter.try_counter(true, true, k.vulnerable):
		navigation.cancel()
		k.register_counter_tap()

func _screen_hit(screen_pos: Vector2) -> bool:
	# did the finger land on his card? (generous: the whole cutout plus a ring)
	var boss: Node3D = m.g.get("db_boss") as Node3D
	var cam: Camera3D = m.player.cam if m.player != null else null
	if boss == null or not is_instance_valid(boss) or cam == null or not cam.is_inside_tree():
		return false
	var mid: Vector3 = boss.global_position + Vector3(0, BOSS_H * 0.5, 0)
	if cam.is_position_behind(mid):
		return false
	var centre: Vector2 = cam.unproject_position(mid)
	var top: Vector2 = cam.unproject_position(boss.global_position + Vector3(0, BOSS_H, 0))
	var half: float = maxf(64.0, absf(centre.y - top.y) * 1.15)
	return screen_pos.distance_to(centre) <= half or screen_pos.distance_to(top) <= 56.0

func _answer_only() -> void:
	# A tap during the showing, the bonk reaction or the befriending must not
	# be silent AND must not scold. Before this, the button did nothing in
	# these three states while a screen tap ran the full shield answer — so the
	# same finger got two different answers depending on where it landed, and
	# "Too puffy! Wait for him to JUMP and FLASH!" could print over the
	# teaching line itself (2026-08-02 stress-test synthesis, D4).
	m._sparkle_burst(m.player.global_position + Vector3(0, 3.0, 0),
		Color(0.92, 0.88, 1.0))

func _bounce_off() -> void:
	# a shielded tap: never a failure, never a penalty — a poof, a giggle, and
	# after three of them he giggles the tell back at her
	var boss: Node3D = m.g.get("db_boss") as Node3D
	if boss != null and is_instance_valid(boss):
		m._sparkle_burst(boss.global_position + Vector3(0, BOSS_H * 0.35, 0),
			Color(0.78, 0.74, 0.92))
	m.g["db_shield_taps"] = int(m.g.get("db_shield_taps", 0)) + 1
	# the medal axis: taps thrown while he was shielded and the fight was
	# actually live. Never reset (db_shield_taps resets on every hit), and
	# never incremented during showing/struck/friends — the teaching beat and
	# the celebration must not cost her a tier.
	var live: String = String(m.g.get("db_state", ""))
	if live == "tell" or live == "strike" or live == "vuln":
		m.g["db_wasted"] = int(m.g.get("db_wasted", 0)) + 1
	if float(m.g.get("db_feedback_cd", 0.0)) <= 0.0:
		m.g["db_feedback_cd"] = FEEDBACK_COOLDOWN
		m.g["db_shield_feedbacks"] = int(m.g.get("db_shield_feedbacks", 0)) + 1
		_say_day_one_context("day1_boss_reminder_dim",
			"That star is dim. Wait for the big gold star!")

func _closer_feedback() -> void:
	# Every far tap still gets a bright positional sparkle, but voice/text is
	# rate-limited so mashing cannot drown out the one useful instruction.
	m.g["db_closer_taps"] = int(m.g.get("db_closer_taps", 0)) + 1
	if float(m.g.get("db_closer_cd", 0.0)) > 0.0:
		return
	m.g["db_closer_cd"] = CLOSER_FEEDBACK_COOLDOWN
	m.g["db_closer_feedbacks"] = int(m.g.get("db_closer_feedbacks", 0)) + 1
	m._sparkle_burst(m.player.global_position + Vector3(0, 3.0, 0),
		Color(1.0, 0.92, 0.62))
	_say_day_one_context("day1_boss_wait_gold",
		"Wait for the gold star, then tap!")

func pose_for_state() -> String:
	# which authored ANIMATION belongs to this beat. The kit plays them; this
	# is the map, kept public so the probe can assert it without reaching into
	# the tick. (Names are DustBunnyBossSprite animation names.)
	var st: String = String(m.g.get("db_state", ""))
	var rounds: int = int(m.g.get("db_hits", 0))
	match st:
		"tell", "strike", "damage_recovery":
			return "angry_jump_final" if rounds >= 2 else "jump"
		"vuln":
			return "laugh_vulnerable"
		"struck":
			return "flinch_3"
		"friends":
			return "implode"
	return "idle"

func _apply_tell(star: Sprite3D, open_now: bool) -> void:
	var want: String = TELL_OPEN_TEX if open_now else TELL_SHUT_TEX
	if not ResourceLoader.exists(want):
		want = STAR_TEX
	if not ResourceLoader.exists(want):
		return
	if String(m.g.get("db_tell_tex", "")) == want:
		return
	var tex: Texture2D = load(want)
	if tex == null:
		return
	star.texture = tex
	star.pixel_size = 4.2 / maxf(1.0, float(tex.get_height()))
	m.g["db_tell_tex"] = want

# ---- presentation ----------------------------------------------------------
func _place_boss(delta: float) -> void:
	var boss: Node3D = m.g.get("db_boss") as Node3D
	var r := stage.root()
	if boss == null or not is_instance_valid(boss) or r == null:
		return
	boss.position = Vector3(float(m.g.get("db_x", 0.0)),
		float(m.g.get("db_y", 0.0)), float(m.g.get("db_z", 0.0)))
	var cfg: Dictionary = phase_cfg()
	var grow: float = float(m.g.get("db_show_grow", 1.0))
	var puff: float = float(cfg["puff"]) * grow
	# the card is animated by the kit now — this file only carries it, and
	# still owns the ground shadow and the head badge
	var k: DustBunnyBossSprite = kit()
	if k != null and is_instance_valid(k):
		k.position.y = 0.0
	# THE TELL: the star over his head. Dim and small while he is shielded,
	# huge and strobing gold the instant he is open.
	var flash: float = float(m.g.get("db_flash", 0.0))
	var star: Sprite3D = m.g.get("db_star") as Sprite3D
	if star != null and is_instance_valid(star):
		_apply_tell(star, flash >= 0.99)
		var strobe: float = 0.5 + 0.5 * sin(float(m.g.get("db_st", 0.0)) * 22.0)
		star.position.y = BOSS_H * puff + 1.5
		star.position.x = 0.0
		if String(m.g.get("db_state", "")) == "struck" and int(m.g.get("db_hits", 0)) == 1:
			# seeing stars: the tell orbits his head while he is dizzy
			var orbit: float = float(m.g.get("db_spin", 0.0)) * 3.0
			star.position.x = cos(orbit) * 2.6
			star.position.y = BOSS_H * puff + 1.0 + sin(orbit) * 0.6
		if flash >= 0.99:
			star.modulate = Color(1.0, 0.92, 0.45, 0.55 + 0.45 * strobe)
			star.scale = Vector3.ONE * (1.35 + 0.35 * strobe)
		else:
			star.modulate = Color(0.66, 0.62, 0.78, 0.42 + 0.35 * flash)
			star.scale = Vector3.ONE * (0.85 + 0.3 * flash)
	var shadow: Sprite2D = m.g.get("db_shadow") as Sprite2D
	if shadow != null and is_instance_valid(shadow):
		var lift: float = clampf(float(m.g.get("db_y", 0.0)) / LEAP_H, 0.0, 1.0)
		var floor_point := Vector2(float(m.g.get("db_x", 0.0)), float(m.g.get("db_z", 0.0)))
		shadow.position = stage.project_floor_point(floor_point)
		var width: float = stage.project_floor_point(floor_point + Vector2(BOSS_H * 0.36, 0.0)).distance_to(shadow.position) * 2.0
		shadow.scale = Vector2.ONE * width / float(shadow.texture.get_width()) * (1.0 - 0.5 * lift) * maxf(0.02, puff)
		shadow.modulate.a = 0.65 - 0.35 * lift
	var glow: MeshInstance3D = m.g.get("db_glow") as MeshInstance3D
	if glow != null and is_instance_valid(glow):
		glow.visible = flash >= 0.99
		glow.position.y = BOSS_H * puff * 0.5
	var hand: EncounterGestureGuide2D = m.g.get("db_hand") as EncounterGestureGuide2D
	if hand != null and is_instance_valid(hand):
		# the non-reader pointer: a finger over his head only while he is open
		hand.visible = flash >= 0.99
		if star != null and m.player.cam != null:
			hand.anchor = m.player.cam.unproject_position(star.global_position)

func _update_hud() -> void:
	# The live head and three encounter puffs carry the lesson. Mastery belongs
	# to the earned result, not a second bright instruction during an attack.
	m.hud_game.visible = false

func _build_mastery_ui() -> void:
	var layer := CanvasLayer.new()
	layer.name = "DustBossMasteryLayer"
	layer.layer = 10
	m.add_child(layer)
	m.g["db_mastery_layer"] = layer
	var root := Control.new()
	root.name = "DustBossMasteryRoot"
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(root)
	var telegraph := DustBossTelegraph2DLogic.new() as DustBossTelegraph2D
	telegraph.configure_quality(m.quality)
	telegraph.draw_floor = false
	telegraph.name = "DustBossTelegraph"
	root.add_child(telegraph)
	m.g["db_telegraph"] = telegraph
	# The painted warning belongs on the floor behind the retained actors.
	# Keep the destination hand and progress above them on the HUD canvas.
	var floor_telegraph := DustBossTelegraph2DLogic.new() as DustBossTelegraph2D
	floor_telegraph.configure_quality(m.quality)
	floor_telegraph.draw_overlay = false
	floor_telegraph.name = "DustBossFloorWarning"
	(m.g["db_attic_layer"] as CanvasLayer).add_child(floor_telegraph)
	m.g["db_floor_telegraph"] = floor_telegraph

func _update_mastery_ui() -> void:
	var layer: CanvasLayer = m.g.get("db_mastery_layer") as CanvasLayer
	if layer == null or not is_instance_valid(layer):
		return
	layer.visible = String(m.g.get("db_state", "")) != "splash"
	_update_telegraph()

func _update_projection() -> void:
	var viewport_size: Vector2 = m.get_viewport().get_visible_rect().size
	if viewport_size == _projection_size:
		return
	_projection_size = viewport_size
	stage.fit_camera()
	var corners := PackedVector2Array()
	for point: Vector2 in [Vector2(-RADIUS, -RADIUS), Vector2(RADIUS, -RADIUS),
			Vector2(RADIUS, RADIUS), Vector2(-RADIUS, RADIUS)]:
		corners.append(stage.project_floor_point(point))
	navigation.set_projection(Rect2(-RADIUS, -RADIUS, RADIUS * 2.0, RADIUS * 2.0), corners)
	if m.hud_msg != null:
		m.hud_msg.position = Vector2(viewport_size.x * 0.20, viewport_size.y - 62.0)
		m.hud_msg.size = Vector2(viewport_size.x * 0.60, 50.0)
	_prepare_telegraph_geometry()

func _prepare_telegraph_geometry() -> void:
	_warning_points.clear()
	if patterns == null or patterns.geometry.is_empty():
		return
	var danger: Dictionary = patterns.geometry
	if String(danger.get("shape", "circle")) == "lane":
		var from: Vector2 = danger["from"]
		var to: Vector2 = danger["to"]
		var direction: Vector2 = (to - from).normalized()
		var side := Vector2(-direction.y, direction.x) * float(danger["half_width"])
		for point: Vector2 in [from + side, to + side, to - side, from - side]:
			_warning_points.append(stage.project_floor_point(point))
	else:
		var center: Vector2 = danger["center"]
		for index: int in range(32):
			var angle: float = TAU * float(index) / 32.0
			var point: Vector2 = center + Vector2(cos(angle), sin(angle)) * float(danger["radius"])
			_warning_points.append(stage.project_floor_point(point))
	# The destination must be a live ground target, outside the boss's head hit
	# region as well as its hazard. Search once per warning, never each frame.
	var safe: Vector2 = danger.get("safe_point", Vector2.ZERO) as Vector2
	if _screen_hit(stage.project_floor_point(safe)):
		var origin: Vector2 = stage.player_local()
		var best_distance: float = INF
		for distance: float in [10.0, 15.0, 20.0]:
			for index: int in range(16):
				var angle: float = TAU * float(index) / 16.0
				var candidate: Vector2 = stage.clamp_point(origin + Vector2(cos(angle), sin(angle)) * distance, 2.6)
				if not patterns.contains(candidate, 1.2) and not _screen_hit(stage.project_floor_point(candidate)):
					var travel: float = origin.distance_to(candidate)
					if travel < best_distance:
						best_distance = travel
						safe = candidate
			if best_distance < INF:
				break
	_safe_destination = safe

func _update_telegraph() -> void:
	var telegraph: DustBossTelegraph2D = m.g.get("db_telegraph") as DustBossTelegraph2D
	if telegraph == null or not is_instance_valid(telegraph):
		return
	var state: String = String(m.g.get("db_state", ""))
	var player_here: Vector2 = stage.player_local()
	var threatened: bool = patterns != null and patterns.contains(player_here)
	_telegraph_data["visible"] = state == "tell" or state == "strike"
	_telegraph_data["active"] = state == "strike"
	_telegraph_data["points"] = _warning_points
	_telegraph_data["progress"] = clampf(patterns.elapsed / maxf(patterns.tell_time, 0.01), 0.0, 1.0)
	_telegraph_data["safe_point"] = stage.project_floor_point(_safe_destination) if threatened else Vector2.ZERO
	_telegraph_data["safe_visible"] = threatened
	_telegraph_data["player_point"] = stage.project_floor_point(player_here)
	_telegraph_data["puffs"] = encounter.completed_rounds
	_telegraph_data["total"] = HP
	telegraph.set_telegraph(_telegraph_data)
	var floor_telegraph: DustBossTelegraph2D = m.g.get("db_floor_telegraph") as DustBossTelegraph2D
	if floor_telegraph != null and is_instance_valid(floor_telegraph):
		floor_telegraph.set_telegraph(_telegraph_data)

# ---- the attic in the round ------------------------------------------------
func _stage_open() -> void:
	if m.touch_ui != null:
		m.touch_ui.set_encounter_controls(on_world_tap, navigation.cancel)
	if m.hud_msg != null:
		_caption_position = m.hud_msg.position
		_caption_size = m.hud_msg.size
		_caption_style = m.hud_msg.get_theme_stylebox("normal")
		m.hud_msg.add_theme_stylebox_override("normal", StorybookUI.panel_style(
			StorybookUI.LAVENDER, Color(0.94, 0.96, 1.0, 0.88), 18, 2))
	_projection_size = Vector2.ZERO
	_build_attic_backdrop()
	stage.open({
		"canvas_backdrop": true,
		"origin": m.ARENA_POS + Vector3(0, 2.5, 0),
		"radius": RADIUS,
		"inset": 2.6,
		"wall_h": 1.2,
		"hover": 3.0,
		"bob_amp": 0.45,
		"speed": 24.0,
		# the frame must hold the whole ring AND the top of a leap plus the
		# star above his head — it follows BOSS_H, so re-scaling the boss
		# re-solves the camera instead of cropping him
		"headroom": HOP_H + BOSS_H + 3.5,
		"look_height_ratio": 0.35,
		"screen_top_margin": 0.10,
		"screen_bottom_margin": 0.10,
		"start": Vector2(0.0, 14.0),
		"floor_col": Color(0.82, 0.74, 0.68),      # attic boards
		"trim_col": Color(0.78, 0.72, 0.88),       # lavender panelling
		"post_col": Color(0.94, 0.90, 0.99),
		"post_glow": Color(1.0, 0.88, 0.70),
	})
	m._play_music("dustboss")
	# Preserve the existing cutout's pixels but keep Roshan readable when the
	# much larger boss lands directly in front of her. Restore on every exit.
	if m.player != null and m.player.classic_sprite != null:
		m.g["db_player_draw_priority"] = m.player.classic_sprite.render_priority
		m.g["db_player_depth_override"] = m.player.classic_sprite.no_depth_test
		m.player.classic_sprite.render_priority = 100
		m.player.classic_sprite.no_depth_test = true

func _build_attic_backdrop() -> void:
	# Presentation binding belongs to the encounter adapter, not main.
	m.arena_env.background_mode = 3 # Canvas background in the existing viewport.
	m.arena_env.background_canvas_max_layer = -20
	var layer := CanvasLayer.new()
	layer.name = "DustBossAtticCanvas"
	layer.layer = -20
	m.add_child(layer)
	var backdrop := TextureRect.new()
	backdrop.name = "DustBossAtticBackdrop"
	backdrop.texture = ATTIC_BACKDROP
	backdrop.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	backdrop.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	backdrop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	backdrop.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	backdrop.offset_left = -16.0
	backdrop.offset_top = -16.0
	backdrop.offset_right = 16.0
	backdrop.offset_bottom = 16.0
	layer.add_child(backdrop)
	m.g["db_attic_layer"] = layer

func _build_boss() -> void:
	var r := stage.root()
	if r == null:
		return
	var boss := Node3D.new()
	boss.position = Vector3(float(m.g["db_x"]), 0.0, float(m.g["db_z"]))
	r.add_child(boss)
	m.g["db_boss"] = boss
	# THE ANIMATED BOSS. DustBunnyBossSprite owns the four-frame sheets, the
	# counter window, the flinch chain and the implosion; this file positions
	# it, tells it when to jump and when to open, and answers its signals.
	var kit := DustBunnyBossSprite.new()
	kit.name = "GrandPuff"
	kit.scale = Vector3.ONE * (BOSS_H / maxf(0.01, DustBunnyBossSprite.DISPLAY_HEIGHT))
	boss.add_child(kit)
	m.g["db_kit"] = kit
	kit.damage_cycle_completed.connect(_on_round_done)
	kit.implosion_finished.connect(_on_imploded)
	kit.final_round_started.connect(_on_final_round)
	kit.tap_progress_changed.connect(_on_tap_progress)
	kit.vulnerability_changed.connect(_on_vulnerability_changed)
	# the ground shadow stays on the deck so a leap reads as a leap
	var shadow := Sprite2D.new()
	shadow.texture = preload("res://assets/flats/castle/rooms/room_actor_shadow.png")
	(m.g["db_attic_layer"] as CanvasLayer).add_child(shadow)
	m.g["db_shadow"] = shadow
	# THE ICON ON HIS HEAD — the art carries a glowing crest on the exposed
	# frame, and this badge repeats it above the card so the tell is readable
	# from across the ring on a phone.
	var star := Sprite3D.new()
	_apply_tell(star, false)
	star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	star.shaded = false
	star.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	star.position = Vector3(0, BOSS_H + 1.5, 0)
	star.modulate = Color(0.66, 0.62, 0.78, 0.42)
	boss.add_child(star)
	m.g["db_star"] = star
	# a small warm halo BEHIND him only. The authored open frame already
	# carries a glowing crest, so the old BOSS_H*1.5 bloom was washing the
	# character out instead of pointing at him.
	var glow := stage.glow(Color(1.0, 0.90, 0.60), BOSS_H * 0.62)
	glow.position = Vector3(0, BOSS_H * 0.42, -0.4)
	glow.visible = false
	boss.add_child(glow)
	m.g["db_glow"] = glow
	var hand := EncounterGestureGuide2D.new()
	hand.show_chip = false
	hand.configure_quality(m.quality)
	hand.visible = false
	(m.g["db_mastery_layer"] as CanvasLayer).add_child(hand)
	m.g["db_hand"] = hand

func kit() -> DustBunnyBossSprite:
	return m.g.get("db_kit") as DustBunnyBossSprite

# ---- what the animation kit tells us ---------------------------------------
func _on_round_done() -> void:
	# One clean avoidance and one intentional counter tap completed this round.
	var rounds: int = encounter.completed_rounds
	m.g["db_hits"] = rounds
	m.save_data["dustboss_pending_rounds"] = mini(rounds, HP)
	m.save_data["dustboss_pending_damage"] = int(m.g.get("db_damage_taken", 0))
	m._write_save()
	m.g["db_miss_streak"] = 0
	m.g["db_shield_taps"] = 0
	var boss: Node3D = m.g.get("db_boss") as Node3D
	if boss != null and is_instance_valid(boss):
		m._sparkle_burst(boss.global_position + Vector3(0, BOSS_H * 0.5, 0),
			Color(0.86, 0.78, 1.0))
	var fr: Dictionary = m.g.get("fr", {})
	if rounds >= HP:
		# the kit plays the implosion itself off flinch_3; wait for the signal
		_enter_state("friends")
		_say_day_one_context("day1_boss_defeated",
			"Grand Puff burst into sparkly stars!")
		if m.player != null:
			m.player.play_verb("cheer")
		return
	_enter_state("struck")
	if rounds == 1:
		_say_day_one_context("day1_boss_hit_first",
			"Boop! Grand Puff is dizzy!")
	else:
		_say_day_one_context("day1_boss_hit_second",
			"Bonk! Two dust puffs down!")

func _on_final_round(_speed: float) -> void:
	_say_day_one_context("day1_boss_enraged",
		"Grand Puff is speedy now! Keep watching the star!")

func _on_imploded() -> void:
	m.g["db_imploded"] = true

func _on_tap_progress(accepted: int, _required: int) -> void:
	m.g["db_taps_this_round"] = accepted
	if accepted > 0:
		_show_attack_feedback()

# ---- the reef doorway ------------------------------------------------------
func build_portal() -> Vector3:
	# A showing before the showing: the great dust bunny peeks out of an attic
	# door on the seabed, so he is a character she has MET before he is ever a
	# fight. Called once from main._build_world; the position it returns is the
	# portal state main owns.
	var bx := -74.0
	var bz := 96.0
	var pos := Vector3(bx, m.seabed_y(bx, bz) + 4.0, bz)
	var frame := Node3D.new()
	frame.position = pos + Vector3(0, -3.0, -4.5)
	m.add_child(frame)
	var arch := MeshInstance3D.new()
	var am := BoxMesh.new()
	am.size = Vector3(9.0, 9.5, 1.4)
	arch.mesh = am
	arch.position = Vector3(0, 4.8, 0)
	arch.material_override = m._soft_mat(Color(0.80, 0.74, 0.86), 0.08)
	frame.add_child(arch)
	var door := MeshInstance3D.new()
	var dm := BoxMesh.new()
	dm.size = Vector3(6.2, 7.4, 0.5)
	door.mesh = dm
	door.position = Vector3(0, 4.0, 0.9)
	door.material_override = m._soft_mat(Color(0.60, 0.50, 0.72), 0.16)
	frame.add_child(door)
	# he peeks out of the attic door in the reef, in his own art: the same
	# animation kit, parked on its idle frame, so she MEETS him before the fight
	var peek := DustBunnyBossSprite.new()
	peek.name = "GrandPuffPeek"
	peek.scale = Vector3.ONE * (6.5 / maxf(0.01, DustBunnyBossSprite.DISPLAY_HEIGHT))
	peek.position = pos + Vector3(2.6, -1.2, 2.4)
	m.add_child(peek)
	m._halo(pos + Vector3(0, 0.6, 0), Color(0.82, 0.76, 1.0), 10.0)
	return pos
