class_name HitEngine
extends RefCounted
# The shared enemies-get-hit pipeline. An encounter (CombatArena today;
# StuffieBattle, BrawlGame, OperaAct by later migration) keeps its enemy
# dictionaries exactly as before and lends them to this engine, which adds one
# uniform interface on top:
#   tap_pick(screen_pos)        -> which enemy a screen tap landed on
#   hit(enemy, damage, source)  -> the single entry point for ALL damage
#   play_death(enemy, style)    -> the dying-animation library + disposal
# The source string is the open seam for future damage kinds — projectiles
# feed "shot_ice"/"shot_fire" today; COMBO_SYSTEM.md verbs ("mash", "slice")
# and anything later funnel through the same hit() call.
# Picking is screen-space unprojection (InteractionDirector's technique):
# no collision shapes, no raycasts, nothing for Jolt to simulate.
# No fail states enter through here: the engine only ever acts on enemies.

const SCREEN_HIT_RADIUS := 110.0
const AIM_HEIGHT := 2.2
const CHAIN_T := 2.0                     # rolling hit-combo window (COMBO_SYSTEM)
# SUPER burst radius. Owner 2026-08-04 ("it feels too easy"): 10.0 covered most
# of a brawler segment, so every fourth tap wiped the screen. A SUPER is now a
# LOCAL burst around the struck enemy — a reward, not a wave-clear.
const SUPER_R := 6.5
const HITSTOP := [0.04, 0.06, 0.09]      # target-freeze seconds at chain 0/1-2/3
# THE DAMAGE GRAMMAR (owner decision 2026-08-01) — canon for every encounter:
#   tap = 1 · slice/slash = 2 · hold (charge) = STAGED 2/3/5 totals · mash =
#   taps at 1. Enemy HP tiers: dust bunny 1 · basic imp 3 · advanced/captain
#   4+ · bosses phase-ruled. A surviving enemy plays the HARM animation; at 0
#   it is eliminated. The 1-2-3 tap combo therefore knocks out exactly a
#   basic imp (3 × 1) and never an advanced enemy. Partner Big Taps = tap + 1.
const VERB_DAMAGE := {"tap": 1, "mash": 1, "slice": 2, "hold": 5}   # hold = stage-3 total

# ---- the three-stage charge attack (owner 2026-08-01) -----------------------
# Press-and-HOLD on an enemy. The press already landed its tap (1 damage,
# press-fire), so the charge stages complete the owner's totals of 2/3/5:
# release at stage 1/2 adds +1/+2, stage 3 fires ITSELF for +4 — hold-until-
# full, never release timing. A translucent ring grows around the enemy and
# snaps color per stage (lavender → gold → pink) with a rising chime + tick.
# The ring is cosmetic; damage is one hit() on release. A finger must be
# down the whole time — begin/release come only from the touch layer, so a
# zero-input run can never charge (probe_passive).
# DIFFICULTY PASS (owner 2026-08-04, "it feels too easy"): the old ladder was
# 2/3/5 at 0.55/1.00/1.45s, which made HOLDING strictly better than playing —
# a 1.00s hold felled a 3-hp imp with ONE finger action while three taps cost
# ~1.2s and three actions. The charge was the laziest verb AND the strongest.
# Now the top of the ladder is 4 damage at 1.75s (2.3 dmg/s) — below a child's
# sustained tapping (~2.5 taps/s), so tapping is the fastest way to fight and
# the charge is what you spend when one BIG hit is worth the wait.
const CHARGE_GRACE := 0.12                   # held this long → the ring appears
const CHARGE_STAGE_T := [0.50, 1.10, 1.75]   # stage completions, from press
const CHARGE_RELEASE_DAMAGE := [0, 1, 2, 3]  # extra damage by stage reached
const CHARGE_COLORS := [Color(0.72, 0.60, 0.95, 0.45), Color(1.0, 0.85, 0.35, 0.52), Color(1.0, 0.45, 0.75, 0.60)]
const CHARGE_CHIME := [0.9, 1.12, 1.35]      # the fanfare ladder, one note per stage
const CHARGE_RING_MIN := 0.9
const CHARGE_RING_MAX := 2.7
const CHARGE_PIP_H := 1.75                   # stage pips ride this far above aim
# (1.35 collided with the hp-lamp row at aim_h+1.05 — radii 0.17+0.13 meant
# the two rows touched whenever a charge ran on a damaged enemy; alpha audit
# 2026-08-05 opened the gap to 0.7 so both read as separate readouts)
const CHARGE_PIP_GAP := 0.5

# ---- the SLICE / slash (owner 2026-08-04) -----------------------------------
# The horizontal swipe (owner-approved 2026-07-25) was never implemented — only
# its damage-table row existed. It is built here BOUNDED, because the obvious
# version (cut everything the finger crosses) clears a wave in one gesture:
#   NARROW BAND   the blade cuts a band SLASH_BAND px either side of the swipe
#                 line and nothing else. The ribbon that draws is exactly that
#                 band, so what she sees is precisely what she cut.
#   FIXED LENGTH  the blade is SLASH_MAX_LEN px long. Dragging further does not
#                 cut further — the ribbon visibly stops at the blade's end, so
#                 a screen-wide sweep is no better than a well-aimed one.
#   TARGET CAP    at most SLASH_MAX_TARGETS enemies per swipe, nearest-first
#                 along the blade. A packed crowd cannot be one-shotted.
#   COOLDOWN      SLASH_COOL between swipes. A spent blade draws grey and
#                 fizzles (a kind sound, never a buzzer) so the rest is visible.
# Damage stays 2 — it is the reward for an aimed, committed gesture, and two
# slices still do not fell a 4-hp advanced enemy on their own.
const SLASH_MIN_LEN := 90.0        # px of travel before a drag counts as a swipe
const SLASH_MAX_LEN := 420.0       # px: the blade's reach, hard-capped
const SLASH_BAND := 54.0           # px half-height of the cutting band
const SLASH_MAX_TARGETS := 2
const SLASH_COOL := 0.9
const SLASH_RIBBON_T := 0.28       # seconds the ribbon lingers

var m: ReefMain
# ENEMY PRIORITY RULE (owner decision 2026-07-28): enemies always sit in
# front of every other tappable thing on stage — a tap that lands on an
# enemy overlapping a prop/friend/interactable hits the enemy, full stop.
# Engines listed in main.hit_engines get first refusal on every world tap,
# before InteractionDirector picks anything. Level design opts a specific
# encounter out by setting tap_priority = false.
var tap_priority := true
var targets: Array = []            # the encounter's enemy dicts (shared reference)
var fx_root: Node3D = null         # parent for transient death-FX nodes
var camera: Camera3D = null        # picking lens (the encounter's own camera)
var on_hit: Callable = Callable()       # func(enemy, damage: int, source: String)
var on_defeated: Callable = Callable()  # func(enemy) — fires as a death begins
var hittable_states: Array = ["active"]
var materials: Dictionary = {}
# ---- the 1-2-3 hit combo (combat wing 2026-08) ------------------------------
# Every hit LANDED by the child's own verbs within the rolling window chains
# 1→2→3 — so tap-tap-tap on a basic imp (3 hp) is the combo AND the knockout.
# Chain 3 arms the NEXT hit as a SUPER. Per-encounter because the engine is.
# Partner supers never call note_hit — the combo is hers alone.
var chain := 0
var chain_t := 0.0
var super_armed := false
var big_taps := 0                  # PartnerAssist grant: +1 damage taps, jumbo feel
var chain_pips: Label = null       # engine-owned ⭐ pips, built on first pop
var pips_layer: CanvasLayer = null
var charge_enemy: Dictionary = {}
var charge_t := 0.0
var charge_stage := 0
var charge_ring: MeshInstance3D = null
var charge_pips: Node3D = null     # the three stage lamps above the target
var slash_cool := 0.0              # blade rest; a swipe inside it only fizzles
var ribbon: Line2D = null          # the band she cut, drawn at its true width

func _init(main: ReefMain) -> void:
	m = main

# Called once per frame by the hosting encounter: the chain window decays
# here (a lapsed chain fades silently) and a live charge grows its ring.
func tick(delta: float) -> void:
	_charge_tick(delta)
	slash_cool = maxf(0.0, slash_cool - delta)
	if chain_t <= 0.0:
		return
	chain_t = maxf(0.0, chain_t - delta)
	if chain_t <= 0.0:
		chain = 0
		super_armed = false
		_fade_pips()

# The touch layer starts a charge the moment a press-fired tap leaves its
# enemy alive, and releases it when that finger lifts.
func begin_charge(enemy: Dictionary) -> void:
	if not hittable(enemy):
		return
	_end_charge(false)
	charge_enemy = enemy
	charge_t = 0.0
	charge_stage = 0

func release_charge() -> void:
	if charge_enemy.is_empty():
		return
	var enemy: Dictionary = charge_enemy
	var stage: int = charge_stage
	_end_charge(stage > 0)
	if stage > 0 and hittable(enemy):
		hit(enemy, int(CHARGE_RELEASE_DAMAGE[mini(stage, 3)]), "hold")

func _charge_tick(delta: float) -> void:
	if charge_enemy.is_empty():
		return
	if not hittable(charge_enemy):
		_end_charge(false)
		return
	charge_t += delta
	var node: Node3D = charge_enemy["node"]
	if charge_t >= CHARGE_GRACE and charge_ring == null:
		_build_charge_ring(node)
	var stage: int = 0
	for i in range(CHARGE_STAGE_T.size()):
		if charge_t >= float(CHARGE_STAGE_T[i]):
			stage = i + 1
	if charge_pips == null:
		_build_charge_pips(node)
	if stage > charge_stage:
		charge_stage = stage
		_style_charge_ring()
		_light_charge_pip(stage)
		if m.chime != null:
			m.chime.pitch_scale = float(CHARGE_CHIME[stage - 1])
			m.chime.play()
		Juice.haptic(15)
	if charge_ring != null and is_instance_valid(charge_ring):
		var grow: float = clampf(charge_t / float(CHARGE_STAGE_T[2]), 0.0, 1.0)
		var radius: float = lerpf(CHARGE_RING_MIN, CHARGE_RING_MAX, grow)
		charge_ring.scale = Vector3(radius, 1.0, radius)
		charge_ring.global_position = node.global_position + Vector3(0, 0.15, 0)
	# THE WORKING-INDICATOR (owner 2026-08-04): the pip row is alive the whole
	# hold, not just at the stage snaps — the NEXT pip swells steadily toward
	# its moment, so a held finger always has something visibly filling. Nothing
	# here is countable-by-reading; it is three lamps and a growing one.
	if charge_pips != null and is_instance_valid(charge_pips):
		charge_pips.global_position = aim_point(charge_enemy) + Vector3(0, CHARGE_PIP_H, 0)
		var next_i: int = mini(charge_stage, CHARGE_STAGE_T.size() - 1)
		if charge_stage < CHARGE_STAGE_T.size():
			var from_t: float = 0.0 if charge_stage == 0 else float(CHARGE_STAGE_T[charge_stage - 1])
			var span: float = maxf(float(CHARGE_STAGE_T[next_i]) - from_t, 0.001)
			var fill: float = clampf((charge_t - from_t) / span, 0.0, 1.0)
			var pip: Node3D = charge_pips.get_child(next_i) as Node3D
			if pip != null:
				pip.scale = Vector3.ONE * lerpf(0.42, 1.0, fill)
	if charge_stage >= 3:
		release_charge()   # full charge fires itself — anticipation, not timing

# Three lamps over the target's head: dim = not yet, bright = banked. The one
# in progress swells (see _charge_tick), so "it is working" is legible from the
# first tenth of a second — the old ring alone waited 0.30s and read as a
# puddle on the floor in the 2.5D promenade.
func _build_charge_pips(node: Node3D) -> void:
	var parent: Node3D = fx_root
	if parent == null:
		parent = node.get_parent() as Node3D
	if parent == null:
		return
	charge_pips = Node3D.new()
	parent.add_child(charge_pips)
	charge_pips.global_position = aim_point(charge_enemy) + Vector3(0, CHARGE_PIP_H, 0)
	var span: float = float(CHARGE_STAGE_T.size() - 1) * CHARGE_PIP_GAP
	for i in range(CHARGE_STAGE_T.size()):
		var lamp: MeshInstance3D = _sphere(charge_pips,
			Vector3(-span * 0.5 + float(i) * CHARGE_PIP_GAP, 0.0, 0.0),
			0.17, Color(0.85, 0.88, 1.0), 0.0)
		lamp.scale = Vector3.ONE * 0.42

func _light_charge_pip(stage: int) -> void:
	if charge_pips == null or not is_instance_valid(charge_pips):
		return
	var lamp: MeshInstance3D = charge_pips.get_child(stage - 1) as MeshInstance3D
	if lamp == null:
		return
	lamp.material_override = _mat(CHARGE_COLORS[clampi(stage - 1, 0, CHARGE_COLORS.size() - 1)], 1.6)
	var tw: Tween = lamp.create_tween()
	tw.tween_property(lamp, "scale", Vector3.ONE * 1.5, 0.09).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(lamp, "scale", Vector3.ONE, 0.14).set_trans(Tween.TRANS_QUAD)

func _build_charge_ring(node: Node3D) -> void:
	var torus := TorusMesh.new()
	torus.inner_radius = 0.82
	torus.outer_radius = 1.0
	torus.rings = 24
	torus.ring_segments = 10
	charge_ring = MeshInstance3D.new()
	charge_ring.mesh = torus
	var parent: Node3D = fx_root
	if parent == null:
		parent = node.get_parent() as Node3D
	if parent == null:
		charge_ring = null
		return
	parent.add_child(charge_ring)
	charge_ring.global_position = node.global_position + Vector3(0, 0.15, 0)
	m._audio_ref().sfx("combat_charge_ring", 1.0, -10.0)
	_style_charge_ring()

func _style_charge_ring() -> void:
	if charge_ring == null or not is_instance_valid(charge_ring):
		return
	var col: Color = CHARGE_COLORS[clampi(charge_stage - 1, 0, CHARGE_COLORS.size() - 1)]
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.albedo_color = col
	mat.emission_enabled = true
	mat.emission = Color(col.r, col.g, col.b)
	mat.emission_energy_multiplier = 0.6
	charge_ring.material_override = mat

func _end_charge(fired: bool) -> void:
	charge_enemy = {}
	charge_t = 0.0
	charge_stage = 0
	if charge_pips != null and is_instance_valid(charge_pips):
		var lamps: Node3D = charge_pips
		var pip_tw: Tween = lamps.create_tween()
		pip_tw.tween_property(lamps, "scale", Vector3.ONE * 0.01, 0.14).set_ease(Tween.EASE_IN)
		pip_tw.tween_callback(lamps.queue_free)
	charge_pips = null
	if charge_ring == null or not is_instance_valid(charge_ring):
		charge_ring = null
		return
	var ring: MeshInstance3D = charge_ring
	charge_ring = null
	var tw: Tween = ring.create_tween()
	if fired:
		tw.tween_property(ring, "scale", ring.scale * 1.5, 0.18).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.parallel().tween_property(ring, "transparency", 1.0, 0.18)
	else:
		tw.tween_property(ring, "transparency", 1.0, 0.15)
	tw.tween_callback(ring.queue_free)

# A hit landed by the child's own verb. The default hp path calls this
# itself; on_hit encounters call it from their response. Returns the new
# chain level; level 3 arms the SUPER.
func note_hit(pos: Vector3) -> int:
	chain = mini(chain + 1, 3)
	chain_t = CHAIN_T
	if chain >= 3:
		super_armed = true
		m._sparkle_burst(pos + Vector3(0, 2.5, 0), Color(1.0, 0.95, 0.6))
	m._audio_ref().pop(chain)
	Juice.haptic(20)
	_show_pips()
	return chain

# The hit AFTER chain 3 is the SUPER: encounters ask-and-consume, then run
# their own response (the default path bursts nearby fodder itself). The
# chain resets bright — pop tops the ladder, hand buzzes, camera nudges.
func consume_super() -> bool:
	if not super_armed:
		return false
	super_armed = false
	chain = 0
	chain_t = 0.0
	m._audio_ref().pop(4)
	Juice.haptic(40)
	Juice.shake(camera if camera != null and is_instance_valid(camera) else m.get_viewport().get_camera_3d())
	_fade_pips()
	return true

# The engine's own screen overlay, shared by the chain pips and the ribbon.
func _ensure_pips_layer() -> void:
	if pips_layer != null and is_instance_valid(pips_layer):
		return
	pips_layer = CanvasLayer.new()
	pips_layer.layer = 14
	m.add_child(pips_layer)

func _show_pips() -> void:
	_ensure_pips_layer()
	if chain_pips == null:
		chain_pips = Label.new()
		StorybookUI.style_hud_label(chain_pips, 46)
		chain_pips.position = Vector2(m.get_viewport().get_visible_rect().size.x * 0.5 - 80.0, 148.0)
		pips_layer.add_child(chain_pips)
	chain_pips.text = "⭐".repeat(chain)
	chain_pips.modulate = Color(1, 1, 1, 1)
	chain_pips.scale = Vector2(1.25, 1.25)
	var tw: Tween = chain_pips.create_tween()
	tw.tween_property(chain_pips, "scale", Vector2.ONE, 0.15)

func _fade_pips() -> void:
	if chain_pips == null:
		return
	var tw: Tween = chain_pips.create_tween()
	tw.tween_property(chain_pips, "modulate:a", 0.0, 0.6)

# Encounters call this on every teardown path (beside their
# main.hit_engines.erase) so the pips HUD never outlives its battle.
func teardown() -> void:
	if pips_layer != null and is_instance_valid(pips_layer):
		pips_layer.queue_free()
	pips_layer = null
	chain_pips = null
	ribbon = null
	if charge_ring != null and is_instance_valid(charge_ring):
		charge_ring.queue_free()
	charge_ring = null
	if charge_pips != null and is_instance_valid(charge_pips):
		charge_pips.queue_free()
	charge_pips = null
	charge_enemy = {}
	slash_cool = 0.0

func hittable(enemy: Dictionary) -> bool:
	if enemy.is_empty():
		return false
	var node_value: Variant = enemy.get("node")
	if node_value == null or not is_instance_valid(node_value):
		return false
	return String(enemy.get("state", "active")) in hittable_states

func aim_point(enemy: Dictionary) -> Vector3:
	var node: Node3D = enemy["node"]
	return node.global_position + Vector3(0, float(enemy.get("aim_h", AIM_HEIGHT)), 0)

# Which enemy does a screen tap land on? Nearest hittable target whose
# projected aim point sits within its screen radius, depth as tiebreaker.
func tap_pick(screen_pos: Vector2) -> Dictionary:
	var lens: Camera3D = camera
	if lens == null or not is_instance_valid(lens):
		lens = m.get_viewport().get_camera_3d()
	if lens == null:
		return {}
	var best: Dictionary = {}
	var best_score := INF
	for enemy_value: Variant in targets:
		var enemy: Dictionary = enemy_value as Dictionary
		if not hittable(enemy):
			continue
		var pos: Vector3 = aim_point(enemy)
		if lens.is_position_behind(pos):
			continue
		var projected: Vector2 = lens.unproject_position(pos)
		var screen_distance: float = projected.distance_to(screen_pos)
		if screen_distance > float(enemy.get("screen_radius", SCREEN_HIT_RADIUS)):
			continue
		var score: float = screen_distance + lens.global_position.distance_to(pos) * 0.015
		if score < best_score:
			best_score = score
			best = enemy
	return best

# ---- the SLICE -------------------------------------------------------------
# A world drag that travelled far enough becomes a swipe of the blade. Returns
# how many enemies it cut. The blade is clamped to SLASH_MAX_LEN, cuts only
# inside SLASH_BAND of the line, takes at most SLASH_MAX_TARGETS nearest-first
# along its length, and then rests. Every one of those limits is drawn.
func slash(from: Vector2, to: Vector2) -> int:
	var span: Vector2 = to - from
	var travel: float = span.length()
	if travel < SLASH_MIN_LEN:
		return 0
	# the blade has a fixed reach: a longer finger-drag simply overshoots it
	var tip: Vector2 = from + span.normalized() * minf(travel, SLASH_MAX_LEN)
	if slash_cool > 0.0:
		_draw_ribbon(from, tip, true)      # spent blade: grey, and it fizzles
		m._audio_ref().sfx("combat_fizzle", 1.0, -6.0)
		return 0
	var lens: Camera3D = camera
	if lens == null or not is_instance_valid(lens):
		lens = m.get_viewport().get_camera_3d()
	if lens == null:
		return 0
	var blade: Vector2 = tip - from
	var blade_len: float = maxf(blade.length(), 0.001)
	var found: Array = []
	for enemy_value: Variant in targets:
		var enemy: Dictionary = enemy_value as Dictionary
		if not hittable(enemy):
			continue
		var pos: Vector3 = aim_point(enemy)
		if lens.is_position_behind(pos):
			continue
		var projected: Vector2 = lens.unproject_position(pos)
		# how far along the blade the enemy sits, and how far off its line
		var along: float = (projected - from).dot(blade) / blade_len
		if along < 0.0 or along > blade_len:
			continue
		var off: float = (projected - (from + blade.normalized() * along)).length()
		if off > SLASH_BAND:
			continue
		found.append({"enemy": enemy, "along": along})
	found.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		return float(a["along"]) < float(b["along"]))
	_draw_ribbon(from, tip, false)
	var cut := 0
	for record_value: Variant in found:
		if cut >= SLASH_MAX_TARGETS:
			break
		var enemy: Dictionary = (record_value as Dictionary)["enemy"] as Dictionary
		if hit(enemy, int(VERB_DAMAGE.get("slice", 2)), "slice"):
			cut += 1
	slash_cool = SLASH_COOL
	if cut > 0:
		Juice.haptic(28)
	else:
		# an honest miss still costs the blade its rest, but it is never a
		# scolding: the ribbon flew, a soft chime, and she may swipe again soon
		m._audio_ref().sfx("combat_fizzle", 1.12, -8.0)
	return cut

# The ribbon IS the hitbox: half-width SLASH_BAND, length the clamped blade.
# Drawing anything wider would be a lie about what the swipe can reach.
func _draw_ribbon(from: Vector2, to: Vector2, spent: bool) -> void:
	_ensure_pips_layer()
	if ribbon != null and is_instance_valid(ribbon):
		ribbon.queue_free()
	ribbon = Line2D.new()
	ribbon.width = SLASH_BAND * 2.0
	ribbon.begin_cap_mode = Line2D.LINE_CAP_ROUND
	ribbon.end_cap_mode = Line2D.LINE_CAP_ROUND
	ribbon.default_color = Color(0.72, 0.74, 0.80, 0.30) if spent else Color(1.0, 0.93, 0.66, 0.55)
	ribbon.points = PackedVector2Array([from, to])
	pips_layer.add_child(ribbon)
	var blade: Line2D = ribbon
	var tw: Tween = blade.create_tween()
	tw.tween_property(blade, "modulate:a", 0.0, SLASH_RIBBON_T)
	tw.tween_callback(blade.queue_free)

# A drag cancels a held charge: one finger, one verb. Without this the charge
# keeps growing under a swipe and auto-fires mid-gesture.
func cancel_charge_for_drag() -> void:
	if not charge_enemy.is_empty():
		_end_charge(false)

# Convenience: resolve a tap into a hit. Returns true when it landed.
func tap(screen_pos: Vector2) -> bool:
	var enemy: Dictionary = tap_pick(screen_pos)
	if enemy.is_empty():
		return false
	return hit(enemy, 1, "tap")

# The one damage entry point. Every damage source — taps, projectiles,
# future combo verbs — lands here. When the encounter sets on_hit it owns
# the response (freeze, phase logic, befriending); otherwise the default
# hp pipeline runs the enemy's death style when hp reaches zero.
func hit(enemy: Dictionary, damage: int = 1, source: String = "tap") -> bool:
	if not hittable(enemy):
		return false
	var node: Node3D = enemy["node"]
	# partner-granted Big Taps ride the child's own verb: +1 damage, big feel
	var big: bool = false
	if big_taps > 0 and source == "tap":
		big_taps -= 1
		damage += 1   # partner Big Tap: tap rides as 2 (the damage grammar)
		big = true
	# the universal feel stack — every hit deforms, blinks (sprite targets),
	# and briefly freezes the target. Cosmetic only; state stays instant.
	Juice.squash(node, big)
	Juice.flash(node)
	enemy["hitstop"] = HITSTOP[clampi(chain, 0, HITSTOP.size() - 1)]
	if not enemy.has("hp_max"):
		enemy["hp_max"] = int(enemy.get("hp", 1))
	if on_hit.is_valid():
		on_hit.call(enemy, damage, source)
		show_hp_pips(enemy)
		return true
	# default hp pipeline: the hit after an armed combo strikes hard (+2 —
	# a SUPER tap knocks out a basic imp outright), every landed hit chains,
	# and the target either plays the HARM animation or is eliminated.
	var super_now: bool = consume_super()
	if super_now:
		damage += 2
	note_hit(node.global_position)
	enemy["hp"] = maxi(0, int(enemy.get("hp", 1)) - damage)
	show_hp_pips(enemy)
	if int(enemy["hp"]) > 0:
		play_harm(enemy)
	else:
		play_death(enemy)
	if super_now:
		_super_burst(node.global_position, enemy)
	return true

# COMBAT EFFICACY, MADE VISIBLE (owner 2026-08-04). A 3-hp imp used to eat two
# taps with nothing but a wobble to show for them, which reads to a four-year-
# old as "my tapping does nothing" — the same feeling as "too easy" from the
# other side. Now every damaged enemy wears a little row of lamps: one per
# hit-point, snuffed out as they go. No numerals, no reading, and it says both
# "that worked" and "he is nearly done". One-pop fodder gets none — for them
# the pop IS the readout. The row rides above the aim point and follows.
func show_hp_pips(enemy: Dictionary) -> void:
	var max_hp: int = int(enemy.get("hp_max", 0))
	if max_hp <= 1:
		return
	var node_value: Variant = enemy.get("node")
	if node_value == null or not is_instance_valid(node_value):
		return
	var node: Node3D = node_value
	var row_value: Variant = enemy.get("hp_row")
	var row: Node3D = row_value as Node3D if row_value != null and is_instance_valid(row_value) else null
	if row == null:
		row = Node3D.new()
		node.add_child(row)
		row.position = Vector3(0, float(enemy.get("aim_h", AIM_HEIGHT)) + 1.05, 0)
		var span: float = float(max_hp - 1) * 0.34
		for i in range(max_hp):
			_sphere(row, Vector3(-span * 0.5 + float(i) * 0.34, 0.0, 0.0),
				0.13, Color(0.55, 0.95, 0.68), 1.1)
		enemy["hp_row"] = row
	var left: int = clampi(int(enemy.get("hp", 0)), 0, max_hp)
	for i in range(row.get_child_count()):
		var lamp: MeshInstance3D = row.get_child(i) as MeshInstance3D
		if lamp == null:
			continue
		if i < left:
			continue
		if lamp.scale.x > 0.2:
			lamp.material_override = _mat(Color(0.36, 0.33, 0.42), 0.0)
			var out: Tween = lamp.create_tween()
			out.tween_property(lamp, "scale", Vector3.ONE * 1.35, 0.06).set_ease(Tween.EASE_OUT)
			out.tween_property(lamp, "scale", Vector3.ONE * 0.18, 0.16).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
	if left <= 0:
		var gone: Tween = row.create_tween()
		gone.tween_property(row, "scale", Vector3.ONE * 0.01, 0.16).set_ease(Tween.EASE_IN)
		gone.tween_callback(row.queue_free)
		enemy.erase("hp_row")

# THE HARM ANIMATION (owner 2026-08-01): a surviving enemy visibly takes the
# hit — recoil wobble on the art child + hurt sparkle. Never grim, never a
# fail state; the feel stack (squash/flash/hitstop) already fired in hit().
func play_harm(enemy: Dictionary) -> void:
	var node_value: Variant = enemy.get("node")
	if node_value == null or not is_instance_valid(node_value):
		return
	var node: Node3D = node_value
	var target: Node3D = node
	for child in node.get_children():
		if child is Node3D:
			target = child as Node3D
			break
	var base_x: float = target.position.x
	var tw: Tween = target.create_tween()
	tw.tween_property(target, "position:x", base_x + 0.32, 0.05).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(target, "position:x", base_x - 0.22, 0.07).set_trans(Tween.TRANS_QUAD)
	tw.tween_property(target, "position:x", base_x, 0.09).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	m._audio_ref().sfx("combat_bonk")   # the rubbery "took it!" under the pop
	m._sparkle_burst(node.global_position + Vector3(0, 2.0, 0), Color(1.0, 0.85, 0.55))

# The default-path SUPER: everything near the struck enemy takes 1 damage —
# harmed or eliminated by its own hp, never a guaranteed wipe of advanced
# enemies. on_hit encounters own their super response via consume_super().
func _super_burst(center: Vector3, struck: Dictionary) -> void:
	m._sparkle_burst(center + Vector3(0, 2.5, 0), Color(1.0, 0.95, 0.6))
	for enemy_value: Variant in targets.duplicate():
		var enemy: Dictionary = enemy_value as Dictionary
		if enemy == struck or not hittable(enemy):
			continue
		var node: Node3D = enemy["node"]
		if node.global_position.distance_to(center) > SUPER_R:
			continue
		enemy["hp"] = maxi(0, int(enemy.get("hp", 1)) - 1)
		if int(enemy["hp"]) > 0:
			play_harm(enemy)
		else:
			play_death(enemy)
	m._audio_ref()._fanfare()

# ---- the dying-animation library -------------------------------------------
# Styles are cosmetic transitions; the enemy's dict state flips immediately so
# game logic (win checks, HUD counts) never waits on a tween. Disposal per
# style: "hide" keeps the node for reuse, "free" removes it, "keep" leaves it.
func play_death(enemy: Dictionary, style: String = "", cfg: Dictionary = {}) -> void:
	var node_value: Variant = enemy.get("node")
	if node_value == null or not is_instance_valid(node_value):
		return
	var node: Node3D = node_value
	var chosen: String = style if style != "" else String(enemy.get("death", "pop"))
	enemy["state"] = String(cfg.get("end_state", "popped"))
	# every elimination gets its airy poof under the style's visuals
	m._audio_ref().sfx("combat_poof", 0.9 if chosen == "flop" else 1.0)
	if on_defeated.is_valid():
		on_defeated.call(enemy)
	match chosen:
		"pop":
			_death_pop(enemy, node, cfg)
		"flop":
			_death_flop(enemy, node, cfg)
		_:
			_death_shrink(enemy, node, cfg)

# The popcorn burst: the arena's beloved imp finale, engine-owned so every
# encounter can serve it. Matches CombatArena's original tween exactly.
func _death_pop(enemy: Dictionary, node: Node3D, cfg: Dictionary) -> void:
	var pos: Vector3 = enemy.get("pos", node.position)
	node.visible = false
	var parent: Node3D = fx_root
	if parent == null:
		parent = node.get_parent() as Node3D
	var corn_count: int = int(cfg.get("count", 7))
	var art_theme: String = String(cfg.get("art_theme", ""))
	for i in range(corn_count):
		var a: float = float(i) * TAU / float(corn_count)
		var corn: Node3D
		if art_theme == "ember":
			corn = DungeonArt.spawn("completion_spark", parent,
				pos + Vector3(cos(a) * 1.2, 1.0 + float(i % 3), sin(a) * 1.2), art_theme)
			corn.scale = Vector3.ONE * 0.34
		else:
			corn = _sphere(parent, pos + Vector3(cos(a) * 1.2, 1.0 + float(i % 3), sin(a) * 1.2), 0.42, Color(1.0, 0.92, 0.62), 0.25)
		var tw: Tween = corn.create_tween()
		tw.tween_property(corn, "position", corn.position + Vector3(cos(a) * 3.0, 3.0 + randf() * 2.0, sin(a) * 3.0), 0.55).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(corn, "scale", Vector3.ZERO, 0.35).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
		tw.tween_callback(corn.queue_free)
	m._sparkle_burst(pos + Vector3(0, 2.0, 0), Color(1.0, 0.85, 0.45))
	_dispose(node, String(cfg.get("dispose", "hide")))

# The brawler's shrink-away, generalized.
func _death_shrink(_enemy: Dictionary, node: Node3D, cfg: Dictionary) -> void:
	var col: Color = cfg.get("color", Color(1.0, 0.75, 0.9))
	m._sparkle_burst(node.global_position + Vector3(0, 2.0, 0), col)
	var tw: Tween = node.create_tween()
	tw.tween_property(node, "scale", Vector3.ONE * 0.01, 0.3).set_ease(Tween.EASE_IN)
	_finish_tween(tw, node, String(cfg.get("dispose", "free")))

# The comic keel-over: a little hop, tip sideways like a landed fish (the
# player's "flop" verb in node form), then shrink out. Never grim.
func _death_flop(_enemy: Dictionary, node: Node3D, cfg: Dictionary) -> void:
	var col: Color = cfg.get("color", Color(1.0, 0.85, 0.55))
	m._sparkle_burst(node.global_position + Vector3(0, 2.0, 0), col)
	var tw: Tween = node.create_tween()
	tw.tween_property(node, "position:y", node.position.y + 1.1, 0.18).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.parallel().tween_property(node, "rotation:z", PI * 0.55, 0.42).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(node, "position:y", node.position.y + 0.2, 0.2).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw.tween_interval(0.25)
	tw.tween_property(node, "scale", Vector3.ONE * 0.01, 0.3).set_ease(Tween.EASE_IN)
	_finish_tween(tw, node, String(cfg.get("dispose", "free")))

func _finish_tween(tw: Tween, node: Node3D, dispose: String) -> void:
	match dispose:
		"free":
			tw.tween_callback(node.queue_free)
		"hide":
			tw.tween_callback(func() -> void: node.visible = false)
		_:
			pass

func _dispose(node: Node3D, dispose: String) -> void:
	match dispose:
		"free":
			node.queue_free()
		"hide":
			node.visible = false
		_:
			pass

func _mat(col: Color, emission: float = 0.0) -> StandardMaterial3D:
	var key := "%s:%.2f" % [col.to_html(true), emission]
	if materials.has(key):
		return materials[key]
	var mat := StandardMaterial3D.new()
	mat.albedo_color = col
	mat.roughness = 0.62
	if emission > 0.0:
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = emission
	materials[key] = mat
	return mat

func _sphere(parent: Node3D, pos: Vector3, radius: float, col: Color, emission: float = 0.0) -> MeshInstance3D:
	var shape := SphereMesh.new()
	shape.radius = radius
	shape.height = radius * 2.0
	shape.radial_segments = 12
	shape.rings = 6
	var node := MeshInstance3D.new()
	node.mesh = shape
	node.position = pos
	node.material_override = _mat(col, emission)
	parent.add_child(node)
	return node
