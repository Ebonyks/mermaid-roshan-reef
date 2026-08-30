class_name DustBossGame
extends RefCounted
# THE DUST BUNNY BOSS — "Grand Puff", the biggest dust bunny in the Pearl
# Castle attic. See DUST_BUNNY_BOSS_2026-08-02.md for the character sheet and
# the AI contract this file implements.
#
# ART IS A PLACEHOLDER (owner note 2026-08-02). BOSS_TEX currently points at
# dust_bunny_curl_ears.png, which is a REGULAR member of the dirty-castle
# dust-bunny cast, not a boss. An exhaustive search of the art database — all
# branches, the source cast atlas, both cinematics, art_library/ART_INVENTORY
# and gen2/generated — found no boss-scale dust bunny anywhere, so the boss
# art has to be made: CODEX_BOSS_ART_HANDOFF_2026-08-02.md §1 orders it as a
# six-cell mood atlas. Until it lands the cast card stands in, blown up to
# boss scale, exactly as the project does for every character whose art has
# not arrived yet. Swap BOSS_TEX and drop BOSS_H back when the real art is in.
#
# The one idea of the fight (owner direction 2026-08-02): Grand Puff is NOT
# hittable whenever you like. He is a ball of dust — taps bounce off him with
# a giggle and a poof, always harmlessly. He is open ONLY while he is IN THE
# AIR and the star over his head is FLASHING. Watch, wait, tap on the flash.
# Three landed hits end the fight, and each one changes who he is:
#   hit 1 → DIZZY  (he wobbles, slows down, his next window is longer)
#   hit 2 → ANGRY  (he puffs up and moves at a much faster pace)
#   hit 3 → FRIENDS (he deflates into a cuddly little puff — nobody loses)
#
# The arena is the shared OctagonStage (scripts/games/octagon_stage.gd): one
# convex ring, a camera that never pans, so the boss can never leave the
# screen and a dragged finger always makes progress.
#
# No fail state: he bumps, but never hurts. Contact gives Roshan a readable
# shove and boing before she recovers immediately; it never removes progress.
# Five windows missed IN A ROW switch the fight to its slower assist pace:
# longer tells/windows, wider reach and one helping tap. A completed round
# resets the streak but keeps the earned pace for the rest of the encounter;
# a slower child never has to prove the same limitation three times. The
# opening feel stays lively for a child who is keeping up. Satellite rules per
# CLAUDE.md: logic only, `main` by reference, all state on m.g ("db_*" keys,
# reclaimed with the rest of the game scratch).

# THE DAMAGE CORE IS DustBunnyBossSprite (scripts/dust_bunny_boss_sprite.gd),
# the approved four-frame animation kit that arrived with Grand Puff's art.
# It owns the owner's 2026-07-29 contract — three rounds of THREE QUICK TAPS,
# a 0.75s window (0.65s in the final round), 1.25x action speed once two rounds
# are down — plus the flinch chain and the implosion. This file owns everything
# around it: the arena, the travel, the showing, the mercy ramp, the medal, the
# framing and the ending. See BOSS_CONVERGENCE_DECISION_2026-08-02.md.
const HP := DustBunnyBossSprite.TOTAL_DAMAGE_ROUNDS      # three damage rounds
const TAPS_PER_ROUND := DustBunnyBossSprite.REQUIRED_TAPS # three taps per window

# Window pacing: the WINDOW length now comes from the animation kit (0.75s,
# 0.65s final). What this file still owns is the SPACING — how long he prowls
# between windows, and the assist pace that starts after five consecutive
# missed windows, so the opening challenge stays intact but cannot become a
# motor-speed wall.
const SHOW_T := 6.4            # the showing: he is revealed before he fights
const WINDUP_T := 0.7          # squash-and-glimmer telegraph before the leap
const STRUCK_T := 1.8          # the hit reaction (spin, burst, hearts)
const DIZZY_T := 3.2           # extra stagger after hit 1 — a free breather
const ANGRY_T := 2.1           # the puff-up after hit 2
const PHASE_BEAT_T := 2.8      # authored pause before the next lively phase
const CELEBRATION_BEAT_T := 1.8 # sparkle/voice beat after each landed round
const WIN_T := 3.4             # befriending beat before the win banner
const POSITIVE_PACING_FLOOR := 38.0 # quick completions still get a warm ending

const LEAP_UP := 0.34          # seconds of rise at the top of a leap
const LEAP_H := 7.6            # hover height while he laughs, exposed
const REACH := 12.0            # base tap reach during a window (ring units)
const HOP_H := 2.4             # prowl hop arc height
const BOSS_H := 17.0           # on-screen height of the animated CARD. The
                               # authored frames carry dust plumes and padding,
                               # so the bunny inside reads at roughly 0.6 of
                               # this — about 10 units against Roshan's ~7,
                               # which is the size difference a boss needs.
                               # The stage re-solves its framing from this.
const RADIUS := 26.0           # the ring's circumradius (apothem ≈ 24.0)
const BOSS_INSET := 4.5        # how far inside the wall the boss may land

const MERCY_TRIGGER_STREAK := 5 # keep the lively opening for five real tries
const MERCY_WINDOW_PER_TIER := 5.5 # final window: 0.65s -> 6.15s at tier one
const MERCY_WINDOW_MAX := 6.0      # admits a measured four-second reaction
const MERCY_REACH_PER_TIER := 4.0
const MERCY_REACH_MAX := 6.0
const MERCY_SLOW_PER_TIER := 0.30 # angry travel drops near the opening pace
const MERCY_SLOW_MAX := 0.45
const MERCY_WINDUP_PER_TIER := 0.55 # more time to read squash -> gold star
const MERCY_WINDUP_MAX := 0.9
const PREASSIST_TRIGGER_STREAK := 2 # gentle help on attempt three after two misses
const PREASSIST_PROWL_CUT := 1.6    # bounded post-miss pacing, never a rush
const PREASSIST_PROWL_MAX := 3.2
const PREASSIST_PROWL_MIN := 0.9
const PREASSIST_WINDOW_PER_TIER := 4.0 # tier-one aid covers a slow first reaction
const PREASSIST_WINDOW_MAX := 4.0
const PREASSIST_LANDING_RADIUS := 2.0 # bias the leap toward rooted/wandering play
const PREASSIST_LANDING_MIN := 0.85
const PREASSIST_REACH := 1.25       # extra reach only after two misses
const FEEDBACK_COOLDOWN := 2.6       # one clear cue, then a quiet learning pause
const CLOSER_FEEDBACK_COOLDOWN := 2.8
const BUMP_COOLDOWN_BASE := 4.0      # first boing stays immediate; repeats space out
const BUMP_COOLDOWN_MISSED := 6.0    # soften repeated bumps in a long miss run
const BUMP_PUSH := 4.0          # visible cause/effect, never damage or lost work
const PLAYER_INSET := 2.6       # matches the OctagonStage walkable inset

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

# Who he is at 0, 1 and 2 landed hits. "hop_speed" is the pace the owner
# note is about: dizzy is slower than puffy, angry is much faster than both.
# Who he is after 0, 1 and 2 completed rounds. The animation kit escalates the
# ACTION (1.25x and a shorter window in the final round); these rows escalate
# the TRAVEL — dizzy is slower than his opening pace, angry is much faster.
const PHASES: Array[Dictionary] = [
	{"name": "puffy", "hop_speed": 10.0, "hop_gap": 0.78, "prowl_t": 3.4,
		"chase": 0.30, "puff": 1.0},
	{"name": "dizzy", "hop_speed": 6.4, "hop_gap": 1.15, "prowl_t": 4.0,
		"chase": 0.15, "puff": 0.96},
	{"name": "angry", "hop_speed": 16.5, "hop_gap": 0.46, "prowl_t": 2.4,
		"chase": 0.65, "puff": 1.12},
]

var m: ReefMain
var stage: OctagonStage

func _init(main: ReefMain) -> void:
	m = main
	stage = OctagonStage.new(main)

# ---- lifecycle -------------------------------------------------------------
func build(fr: Dictionary, _origin: Vector3) -> void:
	m.g["db_hits"] = 0
	m.g["db_miss"] = 0
	m.g["db_miss_streak"] = 0
	m.g["db_mercy_tier"] = 0
	m.g["db_bumps"] = 0
	m.g["db_shield_taps"] = 0
	m.g["db_shield_feedbacks"] = 0
	m.g["db_closer_taps"] = 0
	m.g["db_closer_feedbacks"] = 0
	m.g["db_helper_taps_total"] = 0
	m.g["db_feedback_cd"] = 0.0
	m.g["db_closer_cd"] = 0.0
	m.g["db_bump_cd"] = 0.0
	m.g["db_window_hit"] = 0
	m.g["db_win_len"] = 0.0
	m.g["db_x"] = 0.0
	m.g["db_z"] = -12.0
	m.g["db_y"] = 0.0
	m.g["db_from"] = Vector2(0.0, -12.0)
	m.g["db_to"] = Vector2(0.0, -12.0)
	m.g["db_hop_t"] = 0.0
	m.g["db_spin"] = 0.0
	m.g["db_flash"] = 0.0
	m.g["db_active_t"] = 0.0
	_stage_open()
	_build_boss()
	_enter_state("showing")
	# ONE trigger per beat: show_msg already fires _say(speaker, vo) itself
	# (audio_director.gd), so a paired _say() would speak twice the moment real
	# clips exist. The event name IS the vo argument.
	m.show_msg(String(fr.get("fname", "Dusty Attic")),
		"The GREAT dust bunny wakes up! He is too puffy to bonk...", "dustboss_show")

func action_label() -> String:
	# the only verb in this fight is a bonk; the shared reef button otherwise
	# reads "JUMP" with an up-arrow for the whole encounter
	return "BONK!" if String(m.g.get("db_state", "")) == "vuln" else "WAIT"

func stage_close() -> void:
	stage.close()

func tick(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var r := stage.root()
	if r == null:
		return
	# the real one-finger read: walk the ring, tap = THE button. Damage can
	# only ever come from a fresh tap edge here, so a zero-input run cannot
	# scratch him (probe_passive).
	var s: Dictionary = stage.tick(delta)
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
		"showing":
			_tick_showing(st, fr, tapped)
		"prowl":
			_tick_prowl(delta, st, s, tapped)
		"windup":
			_tick_windup(delta, st, tapped)
		"vuln":
			_tick_vuln(delta, st, s, tapped, fr)
		"struck":
			_tick_struck(delta, st, fr, tapped)
		"friends":
			_tick_friends(st, fr, tapped)
	if m.g.is_empty():
		return                      # the win banner fired and wiped the scratch
	_place_boss(delta)
	_update_hud()

# ---- the state machine -----------------------------------------------------
func _enter_state(next_state: String) -> void:
	m.g["db_state"] = next_state
	m.g["db_st"] = 0.0

func phase() -> int:
	# 0 puffy → 1 dizzy → 2 angry; clamped so the winning hit reads as angry
	return clampi(int(m.g.get("db_hits", 0)), 0, PHASES.size() - 1)

func phase_cfg() -> Dictionary:
	return PHASES[phase()]

func miss_streak() -> int:
	return int(m.g.get("db_miss_streak", 0))

func mercy_tier() -> int:
	# Tier one begins on miss five, tier two on miss ten. Using a discrete tier
	# makes the change legible and keeps attempts one through four identical.
	# Once earned it stays for this encounter, avoiding fast/slow oscillation
	# after an assisted success.
	return maxi(int(m.g.get("db_mercy_tier", 0)),
		miss_streak() / MERCY_TRIGGER_STREAK)

func preassist_tier() -> int:
	# This is deliberately separate from mercy_tier(): two misses means the
	# third attempt is the first gentle assist, while miss five still owns the
	# exact strong assist (long window, wide reach and free tap). The gentle
	# tiers only trim dead travel and make the landing easier to read.
	return clampi(miss_streak() - PREASSIST_TRIGGER_STREAK + 1, 0, 2)

func window_len() -> float:
	# the vulnerability window: the kit's own number (0.75s, 0.65s in the final
	# round) plus the assist tier this file owns
	var base: float = DustBunnyBossSprite.VULNERABILITY_WINDOW
	var kit: DustBunnyBossSprite = m.g.get("db_kit") as DustBunnyBossSprite
	if kit != null and is_instance_valid(kit):
		base = kit.current_vulnerability_window()
	var gentle: float = minf(
		PREASSIST_WINDOW_PER_TIER * float(preassist_tier()), PREASSIST_WINDOW_MAX)
	return base + gentle + minf(MERCY_WINDOW_PER_TIER * float(mercy_tier()), MERCY_WINDOW_MAX)

func reach() -> float:
	var gentle: float = PREASSIST_REACH * float(preassist_tier())
	return REACH + gentle + minf(MERCY_REACH_PER_TIER * float(mercy_tier()), MERCY_REACH_MAX)

func hop_speed() -> float:
	var base: float = float(phase_cfg()["hop_speed"])
	return base * (1.0 - minf(MERCY_SLOW_PER_TIER * float(mercy_tier()), MERCY_SLOW_MAX))

func windup_len() -> float:
	return WINDUP_T + minf(
		MERCY_WINDUP_PER_TIER * float(mercy_tier()), MERCY_WINDUP_MAX)

func prowl_len() -> float:
	var base: float = float(phase_cfg()["prowl_t"])
	var cut: float = minf(PREASSIST_PROWL_CUT * float(preassist_tier()),
		PREASSIST_PROWL_MAX)
	return maxf(PREASSIST_PROWL_MIN, base - cut)

func landing_radius() -> float:
	var tier: int = preassist_tier()
	if tier <= 0:
		return 4.0
	return maxf(PREASSIST_LANDING_MIN,
		PREASSIST_LANDING_RADIUS - 0.55 * float(tier - 1)
		- 0.35 * float(mercy_tier()))

func bump_cooldown() -> float:
	return BUMP_COOLDOWN_MISSED if miss_streak() >= PREASSIST_TRIGGER_STREAK else BUMP_COOLDOWN_BASE

func phase_beat_len(rounds: int) -> float:
	return PHASE_BEAT_T if rounds > 0 and rounds < HP else 0.0

func celebration_beat_len(rounds: int) -> float:
	return CELEBRATION_BEAT_T if rounds > 0 and rounds < HP else 0.0

# THE SHOWING — he is revealed before he is ever fought: he swells up out of
# his dust nest, takes one big parade hop, and demonstrates the tell (the star
# flashes) while the voice line and the pointer explain it. Taps do nothing
# here on purpose; the child is being taught, not tested.
func _tick_showing(st: float, fr: Dictionary, tapped: bool) -> void:
	if tapped:
		_answer_only()
	var grow: float = clampf(st / 1.6, 0.0, 1.0)
	m.g["db_show_grow"] = grow
	m.g["db_y"] = sin(clampf((st - 1.8) / 1.4, 0.0, 1.0) * PI) * 5.4
	# the demo flash: exactly what she has to wait for in the real fight
	var demo: bool = st > 3.2 and st < 5.2
	m.g["db_flash"] = 1.0 if demo else 0.0
	if demo and not bool(m.g.get("db_show_told", false)):
		m.g["db_show_told"] = true
		m.show_msg(String(fr.get("fname", "Dusty Attic")),
			"When he JUMPS and his star FLASHES — TAP him!", "dustboss_tell")
	if st >= SHOW_T:
		m.g["db_flash"] = 0.0
		_enter_state("prowl")
		_pick_hop(true)

# PROWL — bouncing around the ring, shielded. Taps bounce off with a poof;
# after three bounced taps he giggles the tell back at her.
func _tick_prowl(delta: float, st: float, s: Dictionary, tapped: bool) -> void:
	_hop_move(delta, s)
	if tapped:
		_bounce_off()
	if st >= prowl_len():
		_enter_state("windup")

# WIND-UP — the telegraph: he squashes down and the star starts to glimmer.
func _tick_windup(delta: float, st: float, tapped: bool) -> void:
	m.g["db_y"] = maxf(0.0, float(m.g.get("db_y", 0.0)) - delta * 8.0)
	var tell_len: float = windup_len()
	m.g["db_flash"] = clampf(st / tell_len, 0.0, 1.0) * 0.45   # a glimmer, not the flash
	if tapped:
		_bounce_off()
	if st >= tell_len:
		# he leaps toward Roshan so the skill is TIMING, not aim
		var here: Vector2 = stage.player_local()
		m.g["db_from"] = Vector2(float(m.g["db_x"]), float(m.g["db_z"]))
		m.g["db_to"] = stage.clamp_point(
			here + Vector2(randf_range(-landing_radius(), landing_radius()),
			randf_range(-landing_radius(), landing_radius())), BOSS_INSET)
		m.g["db_window_hit"] = 0
		m.g["db_win_len"] = window_len()
		m.g["db_taps_this_round"] = 0
		m.g["db_mercy_topped"] = false
		# the laugh is the tell: the kit opens vulnerability itself on frame 2
		# and starts its own 0.75s (0.65s final) clock
		var k: DustBunnyBossSprite = kit()
		if k != null and is_instance_valid(k):
			k.play_vulnerable_laugh()
		_enter_state("vuln")
		m._say("roshan", "dustboss_leap", 3.0)

# THE VULNERABILITY WINDOW — airborne, star flashing, open to exactly
# HITS_PER_WINDOW damage. Nothing else in the fight can hurt him.
func _tick_vuln(delta: float, st: float, s: Dictionary, tapped: bool, fr: Dictionary) -> void:
	var k: DustBunnyBossSprite = kit()
	var win: float = float(m.g.get("db_win_len", 0.75))
	# rise fast, hover while he laughs, settle on the last beat
	var up: float = clampf(st / LEAP_UP, 0.0, 1.0)
	var hang: float = maxf(0.6, win + 0.6)
	var down: float = clampf((st - (hang - 0.3)) / 0.3, 0.0, 1.0)
	m.g["db_y"] = LEAP_H * up * (1.0 - down) + sin(st * 3.4) * 0.5 * up * (1.0 - down)
	var glide: float = clampf(st / maxf(0.4, hang * 0.6), 0.0, 1.0)
	var from: Vector2 = m.g["db_from"]
	var to: Vector2 = m.g["db_to"]
	var here: Vector2 = from.lerp(to, glide)
	m.g["db_x"] = here.x
	m.g["db_z"] = here.y
	if k == null or not is_instance_valid(k):
		return
	var open_now: bool = k.vulnerable
	m.g["db_flash"] = 1.0 if open_now else 0.0
	# THE ASSIST PACE, applied to the kit's own clock exactly once per window.
	# Gentle time starts on attempt three (after two misses); strong mercy still
	# switches on after five consecutive misses. The shared guard prevents either
	# bonus from being applied twice when the kit's open signal spans frames.
	if open_now and not bool(m.g.get("db_mercy_topped", false)):
		m.g["db_mercy_topped"] = true
		var gentle_bonus: float = minf(
			PREASSIST_WINDOW_PER_TIER * float(preassist_tier()), PREASSIST_WINDOW_MAX)
		var mercy_bonus: float = minf(
			MERCY_WINDOW_PER_TIER * float(mercy_tier()), MERCY_WINDOW_MAX)
		var bonus: float = gentle_bonus + mercy_bonus
		if bonus > 0.0:
			k.vulnerability_time_left += bonus
		# A merely doubled short window is not enough for the slowest hand. The
		# measured slowpoke control reacts at ~4s, so tier one stays open beyond
		# that measured delay. The assist also GIVES
		# her taps: tier one lands the first one (tier two lands the second), so
		# the window she finally reads still needs her real input but not a fast
		# three-tap burst.
		for _free in range(_free_taps()):
			# The telemetry is authoritative: count only a helper insertion the kit
			# actually accepts. Compare its progress because the kit API may be void
			# in a compatible implementation even when it accepts the tap.
			var accepted_before: int = k.accepted_taps
			k.register_vulnerable_tap()
			var accepted_after: int = k.accepted_taps
			if accepted_after > accepted_before:
				m.g["db_helper_taps_total"] = int(
					m.g.get("db_helper_taps_total", 0)) + accepted_after - accepted_before

	if tapped:
		if open_now:
			var d: float = Vector2(here.x - float(s["px"]), here.y - float(s["pz"])).length()
			if d <= reach():
				# THE VERB: one of the three quick taps this window wants
				k.register_vulnerable_tap()
			else:
				_closer_feedback()
		else:
			_bounce_off()
	# the window closed. Either three taps landed (the kit fired
	# damage_cycle_completed and moved us on) or it expired — which is not a
	# failure, it is the mercy ramp.
	if String(m.g.get("db_state", "")) != "vuln":
		return
	if not open_now and st > LEAP_UP + 0.35:
		m.g["db_miss"] = int(m.g.get("db_miss", 0)) + 1
		m.g["db_miss_streak"] = miss_streak() + 1
		m.g["db_mercy_tier"] = mercy_tier()
		m.g["db_flash"] = 0.0
		m.g["db_y"] = 0.0
		_enter_state("prowl")
		_pick_hop(true)
		var streak: int = miss_streak()
		if streak == 1 or streak == PREASSIST_TRIGGER_STREAK \
				or streak == MERCY_TRIGGER_STREAK:
			var reminder: String = (
				"Grand Puff slowed down! Take your time — wait for the BIG GOLD STAR!"
				if streak == MERCY_TRIGGER_STREAK
				else "He is coming closer now — wait for the BIG GOLD STAR!"
				if streak == PREASSIST_TRIGGER_STREAK
				else "So close! Wait for the next FLASH and tap FAST — three times!"
			)
			m.show_msg(String(fr.get("fname", "Dusty Attic")),
				reminder, "dustboss_again")

func _free_taps() -> int:
	# Gentle aid changes timing, reach and landing only. Strong mercy begins
	# exactly after miss five and gives one tap; the result stays below a full
	# round so zero-input play can never complete the encounter.
	return mini(mercy_tier(), TAPS_PER_ROUND - 1)

# THE HIT REACTION — one per landed hit, and where he becomes someone new.
func _tick_struck(delta: float, st: float, fr: Dictionary, tapped: bool) -> void:
	if tapped:
		_answer_only()
	var rounds: int = int(m.g.get("db_hits", 0))
	m.g["db_spin"] = float(m.g.get("db_spin", 0.0)) + 9.0 * delta
	m.g["db_y"] = maxf(0.0, float(m.g.get("db_y", 0.0)) - delta * 22.0)
	m.g["db_flash"] = 0.0
	# the kit is playing flinch_3 -> angry; this hold is the breather the child
	# gets to see what she did before he is moving again
	var hold: float = STRUCK_T + (DIZZY_T if rounds == 1 else (ANGRY_T if rounds == 2 else 0.0)) \
		+ phase_beat_len(rounds) + celebration_beat_len(rounds)
	if rounds >= HP:
		return                     # the friends beat owns the ending
	if st >= hold:
		m.g["db_spin"] = 0.0
		_enter_state("prowl")
		_pick_hop(true)

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
		m.pearl_count += 3
		m._fanfare()
		m._end_game(true, fr,
			"The Great Dust Bunny is your friend now! He gave the castle's shine back!")

# ---- the verbs -------------------------------------------------------------
func _land_hit(fr: Dictionary) -> void:
	var hits: int = int(m.g.get("db_hits", 0)) + 1
	m.g["db_hits"] = hits
	m.g["db_miss_streak"] = 0
	m.g["db_shield_taps"] = 0
	var boss: Node3D = m.g.get("db_boss") as Node3D
	if boss != null and is_instance_valid(boss):
		m._sparkle_burst(boss.global_position + Vector3(0, BOSS_H * 0.5, 0),
			Color(0.86, 0.78, 1.0))
	# (no bare m.voice.play() here — show_msg below already speaks this beat,
	# and a third trigger on the same frame just restarts the same player)
	# a real recoil: the bonk shoves him back across the ring
	var knock: Vector2 = Vector2(float(m.g["db_x"]), float(m.g["db_z"])) \
		- stage.player_local()
	if knock.length() < 0.5:
		knock = Vector2(1.0, 0.0)
	var landed: Vector2 = stage.clamp_point(
		Vector2(float(m.g["db_x"]), float(m.g["db_z"])) + knock.normalized() * 6.0, BOSS_INSET)
	m.g["db_x"] = landed.x
	m.g["db_z"] = landed.y
	if hits >= HP:
		_enter_state("friends")
		m.show_msg(String(fr.get("fname", "Dusty Attic")),
			"POOF! The great dust bunny bursts into stars!", "dustboss_win")
		if m.player != null:
			m.player.play_verb("cheer")
		return
	_enter_state("struck")
	if hits == 1:
		m.show_msg(String(fr.get("fname", "Dusty Attic")),
			"BONK! He is all DIZZY — his ears are spinning!", "dustboss_dizzy")
	else:
		m.show_msg(String(fr.get("fname", "Dusty Attic")), "BONK! Two down!", "dustboss_hit")

func on_world_tap(screen_pos: Vector2) -> void:
	# HYBRID TOUCH: the finger lands ON the boss instead of on the action
	# button. Same verb, and MORE generous — a tap that visibly lands on his
	# card counts as in-reach however far away she is standing.
	if not m.g.has("db_state") or m.game != "dustboss":
		return
	var k: DustBunnyBossSprite = kit()
	var on_him: bool = _screen_hit(screen_pos)
	if k != null and is_instance_valid(k) and k.vulnerable \
			and String(m.g.get("db_state", "")) == "vuln":
		var here := Vector2(float(m.g["db_x"]), float(m.g["db_z"]))
		var d: float = (here - stage.player_local()).length()
		if on_him or d <= reach():
			k.register_vulnerable_tap()
			return
		_closer_feedback()
		return
	var st_now: String = String(m.g.get("db_state", ""))
	if st_now == "showing" or st_now == "struck" or st_now == "friends":
		_answer_only()   # same answer as the button — see D4
		return
	_bounce_off()

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
	return screen_pos.distance_to(centre) <= half

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
	if live == "prowl" or live == "windup" or live == "vuln":
		m.g["db_wasted"] = int(m.g.get("db_wasted", 0)) + 1
	if float(m.g.get("db_feedback_cd", 0.0)) <= 0.0:
		m.g["db_feedback_cd"] = FEEDBACK_COOLDOWN
		m.g["db_shield_feedbacks"] = int(m.g.get("db_shield_feedbacks", 0)) + 1
		m.show_msg("Roshan", "WAIT — dim star means no bonk. BIG GOLD STAR means TAP!",
			"dustboss_tell")

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
	m.show_msg("Roshan", "Come closer! Get under him, then tap the FLASH!",
		"dustboss_closer")

# ---- prowl motion ----------------------------------------------------------
func _pick_hop(reset: bool) -> void:
	var cfg: Dictionary = phase_cfg()
	var here := Vector2(float(m.g.get("db_x", 0.0)), float(m.g.get("db_z", 0.0)))
	var ang: float = randf() * TAU
	var rad: float = sqrt(randf()) * (RADIUS - BOSS_INSET)
	var want := Vector2(cos(ang) * rad, sin(ang) * rad)
	# part of the time he bounces AT her — playful, and the bump is harmless
	if randf() < float(cfg["chase"]):
		want = stage.player_local()
	var step: float = hop_speed() * float(cfg["hop_gap"])
	var dv: Vector2 = want - here
	if dv.length() > step:
		dv = dv.normalized() * step
	m.g["db_from"] = here
	m.g["db_to"] = stage.clamp_point(here + dv, BOSS_INSET)
	if reset:
		m.g["db_hop_t"] = 0.0

func _hop_move(delta: float, s: Dictionary) -> void:
	var cfg: Dictionary = phase_cfg()
	var gap: float = float(cfg["hop_gap"])
	var t: float = float(m.g.get("db_hop_t", 0.0)) + delta
	if t >= gap:
		t = 0.0
		var to_v: Vector2 = m.g["db_to"]
		m.g["db_x"] = to_v.x
		m.g["db_z"] = to_v.y
		_pick_hop(false)
		# one authored jump per hop — anticipation, lift-off, peak, landing ring
		var k: DustBunnyBossSprite = kit()
		if k != null and is_instance_valid(k):
			var from_v: Vector2 = m.g["db_from"]
			var to_v2: Vector2 = m.g["db_to"]
			k.play_jump(1.0 if to_v2.x >= from_v.x else -1.0)
	m.g["db_hop_t"] = t
	var u: float = clampf(t / gap, 0.0, 1.0)
	var from: Vector2 = m.g["db_from"]
	var to: Vector2 = m.g["db_to"]
	var here: Vector2 = from.lerp(to, u)
	m.g["db_x"] = here.x
	m.g["db_z"] = here.y
	m.g["db_y"] = sin(u * PI) * HOP_H
	# The giggly bump has an obvious physical answer, but no health/progress
	# cost and no control lock. Roshan can steer back immediately.
	if Vector2(here.x - float(s["px"]), here.y - float(s["pz"])).length() < 3.2 \
			and float(m.g.get("db_bump_cd", 0.0)) <= 0.0:
		m.g["db_bump_cd"] = bump_cooldown()
		_bump_player(here)
	m.g["db_bump_cd"] = maxf(0.0, float(m.g.get("db_bump_cd", 0.0)) - delta)

func _bump_player(from: Vector2) -> void:
	var here: Vector2 = stage.player_local()
	var away: Vector2 = here - from
	if away.length() < 0.1:
		var travel: Vector2 = (m.g.get("db_to", Vector2.ZERO) as Vector2) \
			- (m.g.get("db_from", Vector2.ZERO) as Vector2)
		away = -travel if travel.length() >= 0.1 else Vector2.DOWN
	var pushed: Vector2 = stage.clamp_point(
		here + away.normalized() * BUMP_PUSH, PLAYER_INSET)
	if m.player != null:
		# Apply the already-computed local displacement directly. Keeping this
		# in component form avoids adding any new 3D API debt while the existing
		# boss arena is migrated to the project's final 2D medium.
		m.player.global_position.x += pushed.x - here.x
		m.player.global_position.z += pushed.y - here.y
		m.player.vel.x = 0.0
		m.player.vel.z = 0.0
		m.player.play_verb("boing")
	m.g["db_bumps"] = int(m.g.get("db_bumps", 0)) + 1
	m._sparkle_burst(m.player.global_position + Vector3(0, 2.4, 0),
		Color(1.0, 0.88, 0.62))
	m._say("roshan", "bump", 2.5)

# ---- the beat map ----------------------------------------------------------
func pose_for_state() -> String:
	# which authored ANIMATION belongs to this beat. The kit plays them; this
	# is the map, kept public so the probe can assert it without reaching into
	# the tick. (Names are DustBunnyBossSprite animation names.)
	var st: String = String(m.g.get("db_state", ""))
	var rounds: int = int(m.g.get("db_hits", 0))
	match st:
		"prowl", "windup":
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
	var shadow: MeshInstance3D = m.g.get("db_shadow") as MeshInstance3D
	if shadow != null and is_instance_valid(shadow):
		var lift: float = clampf(float(m.g.get("db_y", 0.0)) / LEAP_H, 0.0, 1.0)
		shadow.position = Vector3(float(m.g.get("db_x", 0.0)), 0.14,
			float(m.g.get("db_z", 0.0)))
		shadow.scale = Vector3.ONE * (1.0 - 0.5 * lift) * maxf(0.02, puff)
		var sm: StandardMaterial3D = shadow.material_override as StandardMaterial3D
		if sm != null:
			sm.albedo_color = Color(0.16, 0.28, 0.45, 0.30 - 0.18 * lift)
	var glow: MeshInstance3D = m.g.get("db_glow") as MeshInstance3D
	if glow != null and is_instance_valid(glow):
		glow.visible = flash >= 0.99
		glow.position.y = BOSS_H * puff * 0.5
	var hand: Label3D = m.g.get("db_hand") as Label3D
	if hand != null and is_instance_valid(hand):
		# the non-reader pointer: a finger over his head only while he is open
		hand.visible = flash >= 0.99
		hand.position.y = BOSS_H * puff + 3.6 + sin(float(m.g.get("db_st", 0.0)) * 7.0) * 0.4

func _update_hud() -> void:
	var hits: int = int(m.g.get("db_hits", 0))
	var open: bool = String(m.g.get("db_state", "")) == "vuln"
	var lead: String = "⭐ TAP NOW!" if open else "Watch his star…"
	m.hud_game.text = lead + "   " + m._pips(hits, HP, "💜")

# ---- the attic in the round ------------------------------------------------
func _stage_open() -> void:
	stage.open({
		"origin": m.ARENA_POS + Vector3(0, 2.5, 0),
		"radius": RADIUS,
		"inset": 2.6,
		"wall_h": 5.4,
		"hover": 3.0,
		"bob_amp": 0.45,
		"speed": 24.0,
		# the frame must hold the whole ring AND the top of a leap plus the
		# star above his head — it follows BOSS_H, so re-scaling the boss
		# re-solves the camera instead of cropping him
		"headroom": LEAP_H + BOSS_H + 3.5,
		"start": Vector2(0.0, 14.0),
		"floor_col": Color(0.82, 0.74, 0.68),      # attic boards
		"trim_col": Color(0.78, 0.72, 0.88),       # lavender panelling
		"post_col": Color(0.94, 0.90, 0.99),
		"post_glow": Color(1.0, 0.88, 0.70),
	})
	m._play_music("race")
	var r := stage.root()
	if r == null:
		return
	# forgotten pearl crates stacked against the wall panels, and low dust
	# mounds banked in the corners: the room the dust came from
	for i in range(8):
		var ang: float = float(i) * PI / 4.0
		var apo: float = OctagonStage.apothem(RADIUS)
		if i % 2 == 0:
			var crate := MeshInstance3D.new()
			var cm := BoxMesh.new()
			cm.size = Vector3(5.2, 4.0, 3.4)
			crate.mesh = cm
			crate.position = Vector3(cos(ang) * (apo - 2.0), 2.0, sin(ang) * (apo - 2.0))
			crate.rotation.y = -ang
			crate.material_override = m._soft_mat(Color(0.86, 0.78, 0.70), 0.05)
			crate.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			r.add_child(crate)
		else:
			var mound := MeshInstance3D.new()
			var mm := SphereMesh.new()
			mm.radius = 3.6
			mm.height = 3.0
			mound.mesh = mm
			mound.position = Vector3(cos(ang) * (apo - 1.6), 0.5, sin(ang) * (apo - 1.6))
			mound.material_override = m._soft_mat(Color(0.80, 0.76, 0.92), 0.08)
			mound.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			r.add_child(mound)
	# his nest in the middle of the ring: he rises out of this in the showing
	var nest := MeshInstance3D.new()
	var nm := SphereMesh.new()
	nm.radius = 6.0
	nm.height = 4.4
	nest.mesh = nm
	nest.position = Vector3(0.0, 0.3, -12.0)
	nest.material_override = m._soft_mat(Color(0.80, 0.76, 0.92), 0.10)
	nest.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	r.add_child(nest)

func _build_boss() -> void:
	var r := stage.root()
	if r == null:
		return
	var boss := Node3D.new()
	boss.position = Vector3(float(m.g["db_x"]), 0.0, float(m.g["db_z"]))
	r.add_child(boss)
	m.g["db_boss"] = boss
	# THE ANIMATED BOSS. DustBunnyBossSprite owns the four-frame sheets, the
	# three-tap window, the flinch chain and the implosion; this file positions
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
	# the ground shadow stays on the deck so a leap reads as a leap
	var shadow := stage.contact_shadow(BOSS_H * 0.62)
	r.add_child(shadow)
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
	var hand := Label3D.new()
	hand.text = "👆"
	hand.font_size = 128
	hand.pixel_size = 0.03
	hand.outline_size = 18
	hand.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	hand.modulate = Color(1.0, 0.92, 0.5)
	hand.position = Vector3(0, BOSS_H + 3.6, 0)
	hand.visible = false
	boss.add_child(hand)
	m.g["db_hand"] = hand

func kit() -> DustBunnyBossSprite:
	return m.g.get("db_kit") as DustBunnyBossSprite

# ---- what the animation kit tells us ---------------------------------------
func _on_round_done() -> void:
	# one of the three damage rounds is down: three taps landed inside a window
	var rounds: int = int(m.g.get("db_hits", 0)) + 1
	m.g["db_hits"] = rounds
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
		m.show_msg(String(fr.get("fname", "Dusty Attic")),
			"POOF! The great dust bunny bursts into stars!", "dustboss_win")
		if m.player != null:
			m.player.play_verb("cheer")
		return
	_enter_state("struck")
	if rounds == 1:
		m.show_msg(String(fr.get("fname", "Dusty Attic")),
			"BONK BONK BONK! He is all DIZZY — his ears are spinning!", "dustboss_dizzy")
	else:
		m.show_msg(String(fr.get("fname", "Dusty Attic")), "BONK! Two down!", "dustboss_hit")

func _on_final_round(_speed: float) -> void:
	var fr: Dictionary = m.g.get("fr", {})
	m.show_msg(String(fr.get("fname", "Dusty Attic")),
		"He is CROSS now — he is much faster! Keep watching the star!", "dustboss_angry")

func _on_imploded() -> void:
	m.g["db_imploded"] = true

func _on_tap_progress(accepted: int, _required: int) -> void:
	m.g["db_taps_this_round"] = accepted

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
