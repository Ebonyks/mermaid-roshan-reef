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
# No fail state: he bumps, he never hurts. Every window that closes unhit
# makes the NEXT window longer and Roshan's reach bigger (the mercy ramp), so
# the fight always ends in a win — the only variable is how many windows it
# takes. Satellite rules per CLAUDE.md: logic only, `main` by reference, all
# state on m.g ("db_*" keys, reclaimed with the rest of the game scratch).

const HP := 3                  # three landed hits — the whole health bar
const HITS_PER_WINDOW := 1     # one hit per airborne window; the rest sparkle

# Window pacing (owner direction): space the windows so three damage is the
# amount a small player actually places over a fight. One window is a
# comfortable tap (2.6s of flashing ≈ 150 frames), the prowl between windows
# is longer than the window itself, and a landed hit closes the window early.
const SHOW_T := 6.4            # the showing: he is revealed before he fights
const WINDUP_T := 0.7          # squash-and-glimmer telegraph before the leap
const STRUCK_T := 1.4          # the hit reaction (spin, burst, hearts)
const DIZZY_T := 2.6           # extra stagger after hit 1 — a free breather
const ANGRY_T := 1.5           # the puff-up after hit 2
const WIN_T := 2.6             # befriending beat before the win banner

const LEAP_UP := 0.34          # seconds of rise at the top of a leap
const LEAP_H := 7.6            # hover height while the star flashes
const REACH := 12.0            # base tap reach during a window (ring units)
const HOP_H := 2.4             # prowl hop arc height
const BOSS_H := 16.0           # placeholder scale: Roshan is ~7 units, and a
                               # boss must not read as one of the hall bunnies
                               # she already sweeps up. Drop to ~11.5 when the
                               # real boss art lands (it will carry its own mass)
const RADIUS := 26.0           # the ring's circumradius (apothem ≈ 24.0)
const BOSS_INSET := 4.5        # how far inside the wall the boss may land

const MERCY_WINDOW := 0.45     # +seconds of window per missed window
const MERCY_WINDOW_MAX := 2.2
const MERCY_REACH := 1.6       # +reach per missed window
const MERCY_REACH_MAX := 6.0
const MERCY_SLOW := 0.07       # he calms down when she keeps missing
const MERCY_SLOW_MAX := 0.40

# ---- the boss art contract -------------------------------------------------
# One cutout per BEAT, not one cutout for the whole fight. Codex delivered the
# sheets on 2026-08-02 (see BOSS_ART_INTEGRATION_2026-08-02.md for the cell
# map); each pose below is optional, and any file that is not present falls
# back to BOSS_FALLBACK_TEX, so the encounter runs identically whether none,
# some or all of the art has landed.
const BOSS_ART_DIR := "res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/boss/"
const BOSS_FALLBACK_TEX := "res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_curl_ears.png"
const BOSS_POSES := {
	"idle": "boss_idle.png",          # prowling, shielded, pleased with himself
	"windup": "boss_windup.png",      # squashed, ears back — he is about to spring
	"open": "boss_open.png",          # airborne, crest lit — THE window
	"struck": "boss_struck.png",      # the bonk: eyes wide, impact arrows
	"dizzy": "boss_dizzy.png",        # spiral eyes, one ear drooping
	"angry": "boss_angry.png",        # puffed, brows down, steam puffs
	"friends": "boss_friends.png",    # eyes closed, laughing, crest halo
}
# The tell is its own art too: a closed badge and an open badge that read as
# DIFFERENT OBJECTS, not one badge at two alphas.
const TELL_OPEN_TEX := BOSS_ART_DIR + "boss_tell_open.png"
const TELL_SHUT_TEX := BOSS_ART_DIR + "boss_tell_shielded.png"
const STAR_TEX := "res://assets/mg/star.png"   # fallback tell (generic reward star)

# Who he is at 0, 1 and 2 landed hits. "hop_speed" is the pace the owner
# note is about: dizzy is slower than puffy, angry is much faster than both.
const PHASES: Array[Dictionary] = [
	{"name": "puffy", "hop_speed": 10.0, "hop_gap": 0.78, "prowl_t": 3.4,
		"window_t": 2.6, "chase": 0.30, "tint": Color(1.0, 1.0, 1.0), "puff": 1.0},
	{"name": "dizzy", "hop_speed": 6.4, "hop_gap": 1.15, "prowl_t": 4.0,
		"window_t": 3.2, "chase": 0.15, "tint": Color(0.88, 0.93, 1.0), "puff": 0.96},
	{"name": "angry", "hop_speed": 16.5, "hop_gap": 0.46, "prowl_t": 2.4,
		"window_t": 2.1, "chase": 0.65, "tint": Color(1.0, 0.82, 0.78), "puff": 1.12},
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
	m.g["db_shield_taps"] = 0
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
	_stage_open()
	_build_boss()
	_enter_state("showing")
	m.show_msg(String(fr.get("fname", "Dusty Attic")),
		"The GREAT dust bunny wakes up! He is too puffy to bonk...")
	m._say("roshan", "dustboss_show", 2.0)

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
	m.g["db_st"] = float(m.g.get("db_st", 0.0)) + delta
	var st: float = float(m.g["db_st"])
	match String(m.g.get("db_state", "showing")):
		"showing":
			_tick_showing(st, fr)
		"prowl":
			_tick_prowl(delta, st, s, tapped)
		"windup":
			_tick_windup(delta, st, tapped)
		"vuln":
			_tick_vuln(delta, st, s, tapped, fr)
		"struck":
			_tick_struck(delta, st, fr)
		"friends":
			_tick_friends(st, fr)
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

func _mercy() -> int:
	return int(m.g.get("db_miss", 0))

func window_len() -> float:
	# the vulnerability window, mercy included — the number the whole fight is
	# tuned around, and the one a probe asserts grows after a missed window
	var base: float = float(phase_cfg()["window_t"])
	return base + minf(MERCY_WINDOW * float(_mercy()), MERCY_WINDOW_MAX)

func reach() -> float:
	return REACH + minf(MERCY_REACH * float(_mercy()), MERCY_REACH_MAX)

func hop_speed() -> float:
	var base: float = float(phase_cfg()["hop_speed"])
	return base * (1.0 - minf(MERCY_SLOW * float(_mercy()), MERCY_SLOW_MAX))

# THE SHOWING — he is revealed before he is ever fought: he swells up out of
# his dust nest, takes one big parade hop, and demonstrates the tell (the star
# flashes) while the voice line and the pointer explain it. Taps do nothing
# here on purpose; the child is being taught, not tested.
func _tick_showing(st: float, fr: Dictionary) -> void:
	var grow: float = clampf(st / 1.6, 0.0, 1.0)
	m.g["db_show_grow"] = grow
	m.g["db_y"] = sin(clampf((st - 1.8) / 1.4, 0.0, 1.0) * PI) * 5.4
	# the demo flash: exactly what she has to wait for in the real fight
	var demo: bool = st > 3.2 and st < 5.2
	m.g["db_flash"] = 1.0 if demo else 0.0
	if demo and not bool(m.g.get("db_show_told", false)):
		m.g["db_show_told"] = true
		m.show_msg(String(fr.get("fname", "Dusty Attic")),
			"When he JUMPS and his star FLASHES — TAP him!")
		m._say("roshan", "dustboss_tell", 2.0)
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
	if st >= float(phase_cfg()["prowl_t"]):
		_enter_state("windup")

# WIND-UP — the telegraph: he squashes down and the star starts to glimmer.
func _tick_windup(delta: float, st: float, tapped: bool) -> void:
	m.g["db_y"] = maxf(0.0, float(m.g.get("db_y", 0.0)) - delta * 8.0)
	m.g["db_flash"] = clampf(st / WINDUP_T, 0.0, 1.0) * 0.45   # a glimmer, not the flash
	if tapped:
		_bounce_off()
	if st >= WINDUP_T:
		# he leaps toward Roshan so the skill is TIMING, not aim
		var here: Vector2 = stage.player_local()
		m.g["db_from"] = Vector2(float(m.g["db_x"]), float(m.g["db_z"]))
		m.g["db_to"] = stage.clamp_point(
			here + Vector2(randf_range(-4.0, 4.0), randf_range(-4.0, 4.0)), BOSS_INSET)
		m.g["db_window_hit"] = 0
		m.g["db_win_len"] = window_len()
		_enter_state("vuln")
		m._say("roshan", "dustboss_leap", 3.0)

# THE VULNERABILITY WINDOW — airborne, star flashing, open to exactly
# HITS_PER_WINDOW damage. Nothing else in the fight can hurt him.
func _tick_vuln(delta: float, st: float, s: Dictionary, tapped: bool, fr: Dictionary) -> void:
	var win: float = float(m.g.get("db_win_len", 2.6))
	# rise fast, hover while flashing, settle on the last beat
	var up: float = clampf(st / LEAP_UP, 0.0, 1.0)
	var down: float = clampf((st - (win - 0.3)) / 0.3, 0.0, 1.0)
	m.g["db_y"] = LEAP_H * up * (1.0 - down) + sin(st * 3.4) * 0.5 * up * (1.0 - down)
	var glide: float = clampf(st / maxf(0.4, win * 0.6), 0.0, 1.0)
	var from: Vector2 = m.g["db_from"]
	var to: Vector2 = m.g["db_to"]
	var here: Vector2 = from.lerp(to, glide)
	m.g["db_x"] = here.x
	m.g["db_z"] = here.y
	m.g["db_flash"] = 1.0
	if tapped and int(m.g.get("db_window_hit", 0)) < HITS_PER_WINDOW:
		var d: float = Vector2(here.x - float(s["px"]), here.y - float(s["pz"])).length()
		if d <= reach():
			m.g["db_window_hit"] = int(m.g.get("db_window_hit", 0)) + 1
			_land_hit(fr)
			return
		# in range of the tell but not of him: sparkle where she reached, and
		# nudge her toward him rather than letting the tap read as broken
		m._sparkle_burst(m.player.global_position + Vector3(0, 3.0, 0), Color(1.0, 0.92, 0.62))
		m.show_msg("Roshan", "Closer! Get under him and tap!", "hint")
	elif tapped:
		_bounce_off()
	if st >= win:
		# the window closed unhit — that is not a failure, it is the mercy ramp
		m.g["db_miss"] = int(m.g.get("db_miss", 0)) + 1
		m.g["db_flash"] = 0.0
		m.g["db_y"] = 0.0
		_enter_state("prowl")
		_pick_hop(true)
		if int(m.g["db_miss"]) == 1 or int(m.g["db_miss"]) % 3 == 0:
			m.show_msg(String(fr.get("fname", "Dusty Attic")),
				"He landed! Wait for the next FLASH — you get as many tries as you like.")
			m._say("roshan", "dustboss_again", 4.0)

# THE HIT REACTION — one per landed hit, and where he becomes someone new.
func _tick_struck(delta: float, st: float, fr: Dictionary) -> void:
	var hits: int = int(m.g.get("db_hits", 0))
	m.g["db_spin"] = float(m.g.get("db_spin", 0.0)) + 9.0 * delta
	m.g["db_y"] = maxf(0.0, float(m.g.get("db_y", 0.0)) - delta * 22.0)
	m.g["db_flash"] = 0.0
	var hold: float = STRUCK_T + (DIZZY_T if hits == 1 else (ANGRY_T if hits == 2 else 0.0))
	if hits >= HP:
		return                     # the friends beat owns the ending
	if st >= hold:
		m.g["db_spin"] = 0.0
		if hits == 2:
			m.show_msg(String(fr.get("fname", "Dusty Attic")),
				"He is CROSS now — he is much faster! Keep watching the star!")
			m._say("roshan", "dustboss_angry", 3.0)
		_enter_state("prowl")
		_pick_hop(true)

# THE ENDING — nobody loses: he deflates into a small cuddly puff, gives back
# the castle's dust in a burst of stars, and the win banner fires.
func _tick_friends(st: float, fr: Dictionary) -> void:
	m.g["db_y"] = maxf(0.0, float(m.g.get("db_y", 0.0)) - 0.3)
	m.g["db_flash"] = 0.0
	if st >= WIN_T and not bool(m.g.get("db_done", false)):
		m.g["db_done"] = true
		m.pearl_count += 3
		m._end_game(true, fr,
			"The Great Dust Bunny is your friend now! He gave the castle's shine back!")

# ---- the verbs -------------------------------------------------------------
func _land_hit(fr: Dictionary) -> void:
	var hits: int = int(m.g.get("db_hits", 0)) + 1
	m.g["db_hits"] = hits
	m.g["db_shield_taps"] = 0
	var boss: Node3D = m.g.get("db_boss") as Node3D
	if boss != null and is_instance_valid(boss):
		m._sparkle_burst(boss.global_position + Vector3(0, BOSS_H * 0.5, 0),
			Color(0.86, 0.78, 1.0))
	if m.voice != null:
		m.voice.pitch_scale = 1.1 + randf() * 0.2
		m.voice.play()
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
			"POOF! The great dust bunny bursts into stars!")
		m._say("roshan", "dustboss_win", 0.0)
		if m.player != null:
			m.player.play_verb("cheer")
		return
	_enter_state("struck")
	if hits == 1:
		m.show_msg(String(fr.get("fname", "Dusty Attic")),
			"BONK! He is all DIZZY — his ears are spinning!")
		m._say("roshan", "dustboss_dizzy", 2.0)
	else:
		m.show_msg(String(fr.get("fname", "Dusty Attic")), "BONK! Two down!")
		m._say("roshan", "dustboss_hit", 2.0)

func on_world_tap(screen_pos: Vector2) -> void:
	# HYBRID TOUCH: the finger lands ON the boss instead of on the action
	# button. Same verb, and MORE generous — a tap that visibly lands on his
	# card counts as in-reach however far away she is standing, because "I
	# touched the thing I wanted to bonk" is the truest intent a small player
	# can express. It can never be less generous than the button.
	if not m.g.has("db_state") or m.game != "dustboss":
		return
	var fr: Dictionary = m.g.get("fr", {})
	var on_him: bool = _screen_hit(screen_pos)
	if String(m.g.get("db_state", "")) == "vuln" \
			and int(m.g.get("db_window_hit", 0)) < HITS_PER_WINDOW:
		var here := Vector2(float(m.g["db_x"]), float(m.g["db_z"]))
		var d: float = (here - stage.player_local()).length()
		if on_him or d <= reach():
			m.g["db_window_hit"] = int(m.g.get("db_window_hit", 0)) + 1
			_land_hit(fr)
			return
		m._sparkle_burst(m.player.global_position + Vector3(0, 3.0, 0), Color(1.0, 0.92, 0.62))
		m._say("roshan", "dustboss_closer", 3.0)
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

func _bounce_off() -> void:
	# a shielded tap: never a failure, never a penalty — a poof, a giggle, and
	# after three of them he giggles the tell back at her
	var boss: Node3D = m.g.get("db_boss") as Node3D
	if boss != null and is_instance_valid(boss):
		m._sparkle_burst(boss.global_position + Vector3(0, BOSS_H * 0.35, 0),
			Color(0.78, 0.74, 0.92))
	m.g["db_shield_taps"] = int(m.g.get("db_shield_taps", 0)) + 1
	if int(m.g["db_shield_taps"]) % 3 == 0:
		m.show_msg("Roshan", "Too puffy! Wait for him to JUMP and FLASH!", "hint")
		m._say("roshan", "dustboss_tell", 3.0)

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
	m.g["db_hop_t"] = t
	var u: float = clampf(t / gap, 0.0, 1.0)
	var from: Vector2 = m.g["db_from"]
	var to: Vector2 = m.g["db_to"]
	var here: Vector2 = from.lerp(to, u)
	m.g["db_x"] = here.x
	m.g["db_z"] = here.y
	m.g["db_y"] = sin(u * PI) * HOP_H
	# the giggly bump: he shoves nobody over and takes nothing away
	if Vector2(here.x - float(s["px"]), here.y - float(s["pz"])).length() < 3.2 \
			and float(m.g.get("db_bump_cd", 0.0)) <= 0.0:
		m.g["db_bump_cd"] = 1.6
		m._sparkle_burst(m.player.global_position + Vector3(0, 2.4, 0), Color(1.0, 0.88, 0.62))
		m._say("roshan", "bump", 2.5)
	m.g["db_bump_cd"] = maxf(0.0, float(m.g.get("db_bump_cd", 0.0)) - delta)

# ---- the pose system -------------------------------------------------------
func _pose_path(key: String) -> String:
	var file: String = String(BOSS_POSES.get(key, ""))
	if file != "":
		var full: String = BOSS_ART_DIR + file
		if ResourceLoader.exists(full):
			return full
	return BOSS_FALLBACK_TEX

func pose_for_state() -> String:
	# which drawing belongs to this beat. Public so the probe can assert the
	# map without reaching into the tick.
	var st: String = String(m.g.get("db_state", ""))
	var hits: int = int(m.g.get("db_hits", 0))
	match st:
		"windup":
			return "windup"
		"vuln":
			return "open"
		"struck":
			return "dizzy" if hits == 1 else "struck"
		"friends":
			return "friends"
	return "angry" if hits >= 2 else "idle"

func _apply_pose(body: Sprite3D, key: String) -> void:
	var path: String = _pose_path(key)
	if not ResourceLoader.exists(path):
		return
	var tex: Texture2D = load(path)
	if tex == null:
		return
	body.texture = tex
	# every pose is authored at its own height; normalise so the boss keeps
	# one physical size no matter which drawing is showing
	body.pixel_size = BOSS_H / maxf(1.0, float(tex.get_height()))
	m.g["db_pose"] = key

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
	# dizzy wobbles, angry throbs — the phase is legible without any words
	var body: Sprite3D = m.g.get("db_body") as Sprite3D
	if body != null and is_instance_valid(body):
		var want_pose: String = pose_for_state()
		if String(m.g.get("db_pose", "")) != want_pose:
			_apply_pose(body, want_pose)
		var wob: float = 0.0
		if String(m.g.get("db_state", "")) == "struck" and int(m.g.get("db_hits", 0)) == 1:
			wob = sin(float(m.g.get("db_st", 0.0)) * 11.0) * 0.22
		elif phase() == 1:
			wob = sin(float(m.g.get("db_st", 0.0)) * 3.0) * 0.06
		elif phase() == 2:
			puff *= 1.0 + sin(float(m.g.get("db_st", 0.0)) * 9.0) * 0.035
		body.rotation.z = lerpf(body.rotation.z, wob, 1.0 - pow(0.002, delta))
		body.scale = Vector3.ONE * maxf(0.02, puff)
		body.modulate = cfg["tint"] as Color
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
	# the cutout: unshaded, billboarded, never re-lit or redesigned
	var body := Sprite3D.new()
	_apply_pose(body, "idle")
	body.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	body.shaded = false
	body.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	body.position = Vector3(0, BOSS_H * 0.5, 0)
	boss.add_child(body)
	m.g["db_body"] = body
	# THE GROUND SHADOW STAYS ON THE DECK. Parented to the boss it would fly
	# with him and an airborne leap would read exactly like a ground hop —
	# the shadow shrinking away from his feet is what says "he is UP THERE"
	# (2026-08-02 stress test, visual pass).
	var shadow := stage.contact_shadow(BOSS_H * 0.62)
	r.add_child(shadow)
	m.g["db_shadow"] = shadow
	# THE ICON ON HIS HEAD — the whole fight is reading this one sprite
	var star := Sprite3D.new()
	_apply_tell(star, false)
	star.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	star.shaded = false
	star.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	star.position = Vector3(0, BOSS_H + 1.5, 0)
	star.modulate = Color(0.66, 0.62, 0.78, 0.42)
	boss.add_child(star)
	m.g["db_star"] = star
	var glow := stage.glow(Color(1.0, 0.92, 0.55), BOSS_H * 1.5)
	glow.position = Vector3(0, BOSS_H * 0.5, 0)
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
	var peek := Sprite3D.new()
	var peek_tex: String = _pose_path("idle")
	if ResourceLoader.exists(peek_tex):
		peek.texture = load(peek_tex)
		peek.pixel_size = 6.5 / maxf(1.0, float(peek.texture.get_height()))
	peek.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	peek.shaded = false
	peek.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	peek.position = pos + Vector3(2.6, 1.4, 2.4)
	m.add_child(peek)
	m._halo(pos + Vector3(0, 0.6, 0), Color(0.82, 0.76, 1.0), 10.0)
	return pos
