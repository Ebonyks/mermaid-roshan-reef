class_name BrawlGame
extends RefCounted
# Phase 8: the TOY CASTLE brawler — a Castle-Crashers-style walk-the-plane
# co-op on the SideScrollStage engine's brawl mode. Mischief imps have taken
# over Huluu's toy castle; Roshan walks the courtyard plane (x + depth) and
# POPS them with the one tap button, gates sliding the stage forward wave by
# wave. HULUU IS PLAYER 2: an illustrated-cutout hero who fights alongside —
# AI-driven solo, a second gamepad takes her over live.
# No fail: imps bump and giggle, never hurt. Agency rule (Phase 6): Huluu —
# human OR AI — only ever STUNS imps; ONLY Roshan's tap pops them, so a
# zero-input run can never win even with an AI partner on the field.
# All state stays on main (m.*); received by reference.

const SEG_W := 34.0                  # one courtyard segment per wave
const X0 := -17.0                    # left edge of segment 0 (stage-local)
const HALF_D := 7.0                  # walkable depth band (±z)
const WAVES := [3, 4, 5]             # imps per segment
const IMP_SPEED := 7.0
const HULUU_SPEED := 20.0
const STUN_T := 3.0                  # Huluu's stun duration
const STUN_R := 5.0                  # Huluu's stun reach
# Roshan's base pop reach (mercy grows it). Owner 2026-08-04, "it feels too
# easy": 6.0 base rising to 10.0 under mercy covered most of a 34-wide, 14-deep
# segment, so a bop landed on the nearest imp wherever she stood — the fight
# played itself. 4.5 rising to 7.5 asks her to actually close the distance,
# which is the "more active style" the pass is for, while mercy still rescues a
# child who is struggling (and the recover-pose bonus still forgives a lunge).
const BOP_R := 4.5
const BOP_R_MERCY := 3.0             # added at full mercy, not before
const CHAIN_T := 2.0                 # pop-chain rolling window (COMBO_SYSTEM.md)
const SUPER_R := 6.5                 # SUPER POP burst radius once chain 3 arms it
const BANNERS := [Color(1.0, 0.72, 0.82), Color(0.62, 0.90, 0.78), Color(0.78, 0.72, 0.98), Color(1.0, 0.87, 0.55)]

var m: ReefMain
var stage: SideScrollStage

func _init(main: ReefMain) -> void:
	m = main
	stage = SideScrollStage.new(main)

func build(fr: Dictionary, _origin: Vector3) -> void:
	m.g["seg"] = 0
	m.g["bops"] = 0
	m.g["chain"] = 0
	m.g["chain_t"] = 0.0
	m.g["wave_t"] = 0.0
	m.g["enemies"] = []
	m.g["gates"] = []
	m.g["timer"] = -1.0
	m.g["imp_brain"] = null      # a fresh crew brain is built per wave
	m.g["imp_warned"] = false
	m.g["brawl_reach_ring"] = null   # rebuilt on the fresh stage root
	_stage_open()
	stage.set_bounds(X0, X0 + SEG_W)
	m.show_msg("Huluu", "Mischief imps are in Huluu's toy castle! Tap to POP them — Huluu helps!", "greet")

func _tick_brawl(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var r := stage.root()
	if r == null:
		return
	var s: Dictionary = stage.brawl_tick(delta)
	stage.props_tick(delta)   # blocks: wake shove + swell tide + sleep contract
	m.g["wave_t"] = float(m.g.get("wave_t", 0.0)) + delta
	# pop-chain window: a lapsed chain just fades — no sound, no sting
	m.g["chain_t"] = maxf(0.0, float(m.g.get("chain_t", 0.0)) - delta)
	if float(m.g["chain_t"]) <= 0.0:
		m.g["chain"] = 0
	var enemies: Array = m.g["enemies"]
	var seg: int = int(m.g["seg"])
	if enemies.is_empty() and seg < WAVES.size():
		_spawn_wave(seg)
		enemies = m.g["enemies"]
	# mercy: a long wave slows the imps and grows Roshan's pop reach
	var mercy: float = clampf((float(m.g["wave_t"]) - 45.0) / 60.0, 0.0, 1.0)
	var imp_spd: float = IMP_SPEED * (1.0 - 0.45 * mercy)
	var bop_r: float = BOP_R + BOP_R_MERCY * mercy
	_update_reach_ring(r, s, bop_r, enemies)
	# Huluu (player 2): chase the nearest un-stunned imp, stun on contact.
	# Her taps (human) and her AI both STUN only — pops are Roshan's alone.
	var p2_want_x: float = float(s["px"]) - 4.0
	var p2_want_z: float = float(s["pz"])
	var p2_target: Dictionary = _nearest_imp(float(m.g.get("ss_p2x", 0.0)), float(m.g.get("ss_p2z", 0.0)), true)
	if not p2_target.is_empty():
		var tn: Node3D = p2_target["node"]
		p2_want_x = tn.position.x
		p2_want_z = tn.position.z
	var p2: Dictionary = stage.companion_tick(delta, p2_want_x, p2_want_z, HULUU_SPEED)
	m.g["p2_cd"] = maxf(0.0, float(m.g.get("p2_cd", 0.0)) - delta)
	var p2_stun_now: bool = bool(p2["tap"]) or (not bool(p2["human"]) and float(m.g["p2_cd"]) <= 0.0)
	if p2_stun_now and not p2_target.is_empty():
		var tn2: Node3D = p2_target["node"]
		if Vector2(tn2.position.x - float(p2["x"]), tn2.position.z - float(p2["z"])).length() < STUN_R:
			p2_target["stun"] = STUN_T
			m.g["p2_cd"] = 2.4
			var stunned_mind: Dictionary = p2_target.get("ai", {})
			var stun_brain: ImpAI = m.g.get("imp_brain", null) as ImpAI
			if stun_brain != null and not stunned_mind.is_empty():
				# a stunned imp stops deciding — Huluu buys Roshan the beat
				stun_brain.on_stun(stunned_mind, STUN_T)
			m._sparkle_burst(tn2.global_position + Vector3(0, 2.5, 0), Color(0.75, 0.85, 1.0))
	# imps: the shared crew brain (scripts/imp_ai.gd) decides who closes in,
	# who telegraphs a lunge and who hangs back once the wave thins. They
	# still only ever bump — a landed lunge is a giggle, never a hurt.
	var brain: ImpAI = m.g.get("imp_brain", null) as ImpAI
	var hero := Vector2(float(s["px"]), float(s["pz"]))
	if brain != null:
		brain.tune["speed"] = imp_spd
		var minds: Array = []
		for e in enemies:
			var en: Node3D = e["node"]
			if not is_instance_valid(en):
				continue
			e["stun"] = maxf(0.0, float(e.get("stun", 0.0)) - delta)
			e["bump_cd"] = maxf(0.0, float(e.get("bump_cd", 0.0)) - delta)
			var mind: Dictionary = e.get("ai", {})
			if mind.is_empty():
				continue
			mind["pos"] = Vector2(en.position.x, en.position.z)
			mind["alive"] = true
			minds.append(mind)
		brain.tick(delta, minds, hero)
		_brawl_brain_events(brain, r, hero)
		var lo: float = X0 + 1.5
		var hi: float = X0 + float(seg + 1) * SEG_W - 1.5
		for e in enemies:
			var en2: Node3D = e["node"]
			if not is_instance_valid(en2):
				continue
			var mind2: Dictionary = e.get("ai", {})
			if mind2.is_empty():
				continue
			var want: Vector2 = mind2.get("pos", Vector2(en2.position.x, en2.position.z))
			# the courtyard is the truth: imps stay inside the open segment
			var px: float = clampf(want.x, lo, hi)
			var pz: float = clampf(want.y, -HALF_D + 1.0, HALF_D - 1.0)
			mind2["pos"] = Vector2(px, pz)
			en2.position.x = px
			en2.position.z = pz
			_pose_imp(e, en2, String(mind2.get("pose", "prowl")), float(mind2.get("t", 0.0)), hero)
	# Roshan's BOP — the deliberate verb; only a fresh tap lands it. Every
	# landed bop chains 1→2→3 (one full combo fells a basic 3-hp imp); the
	# armed bop after chain 3 is the SUPER POP: +2 damage plus a 1-damage
	# splash near the hit. Only her taps chain — Huluu's stuns never count
	# (Phase-6 agency rule).
	if bool(s["tap"]):
		var hit: Dictionary = _nearest_imp(float(s["px"]), float(s["pz"]), false)
		var landed := false
		if not hit.is_empty():
			var hn: Node3D = hit["node"]
			# a lunging imp caught in its recovery is a bigger, kinder target
			var pop_r: float = bop_r * (1.4 if String(hit.get("pose", "")) == "recover" else 1.0)
			if Vector2(hn.position.x - float(s["px"]), hn.position.z - float(s["pz"])).length() < pop_r:
				landed = true
				var hit_mind: Dictionary = hit.get("ai", {})
				if brain != null and not hit_mind.is_empty():
					brain.on_hit(hit_mind, true)
				var super_pop: bool = int(m.g.get("chain", 0)) >= 3
				var dmg := 1
				if super_pop:
					m.g["chain"] = 0
					dmg = 3
					m._sparkle_burst(hn.global_position + Vector3(0, 3.5, 0), Color(1.0, 0.95, 0.6))
					m._say("huluu", "hero", 4.0)
				else:
					m.g["chain"] = int(m.g["chain"]) + 1
					if int(m.g["chain"]) == 3:
						m._say("huluu", "talk", 4.0)   # cheer: next bop is SUPER
				m.g["chain_t"] = CHAIN_T
				_damage_imp(hit, dmg)
				if super_pop:
					for e in enemies.duplicate():
						var en3: Node3D = e["node"]
						if e == hit or not is_instance_valid(en3):
							continue
						if Vector2(en3.position.x - hn.position.x, en3.position.z - hn.position.z).length() < SUPER_R:
							_damage_imp(e, 1)
				if m.voice != null:
					# pitch climbs with the chain; the SUPER POP tops the ramp
					if super_pop:
						m.voice.pitch_scale = 1.4
					else:
						m.voice.pitch_scale = 1.0 + 0.15 * float(maxi(int(m.g["chain"]) - 1, 0))
					m.voice.play()
		if brain != null:
			# a miss tells the crew she needs a slower fight; a hit tells it
			# she is ready for a bolder one
			brain.on_player_swing(landed)
	# wave cleared → the gate sparkles open and the courtyard slides forward
	if enemies.is_empty() and seg < WAVES.size():
		m.g["seg"] = seg + 1
		m.g["wave_t"] = 0.0
		if seg < WAVES.size() - 1:
			_open_gate(seg)
			# extend the right wall; the cleared courtyard stays walkable so
			# nobody ever gets snapped forward when a gate opens
			stage.set_bounds(X0, X0 + float(seg + 2) * SEG_W)
			m.show_msg("Huluu", "This way! More imps ahead! ➜", "talk")
		else:
			m.pearl_count += 3   # portal payout, same size as the treasure chest
			m._say("huluu", "hero", 0.0)
			m._end_game(true, fr, "You and Huluu saved the toy castle! Hero high-five!")
			return
	var imps_total := 0
	for wv in WAVES:
		imps_total += int(wv)
	var stars: String = "⭐".repeat(mini(int(m.g.get("chain", 0)), 3))
	m.hud_game.text = "POP the mischief imps!  " + m._pips(int(m.g["bops"]), imps_total, "🎈") + ("  " + stars if stars != "" else "")

func stage_close() -> void:
	stage.close()

# Harm-or-eliminate (damage grammar, owner 2026-08-01): a surviving imp
# flinches with a giggle-wobble; an emptied one pops away toward the wave.
# HER REACH, MADE VISIBLE (owner 2026-08-04). The pop reach shrank in the
# difficulty pass so she has to close the distance — but a reach she cannot see
# is just "my tapping stopped working". A soft ring on the floor shows exactly
# how far the bop carries, and it BRIGHTENS whenever an imp is standing inside
# it: the whole efficacy readout is "is my ring lit?", which needs no reading.
# It also grows on its own as mercy widens the reach, so the game visibly
# helping her is something she can watch happen.
func _update_reach_ring(r: Node3D, s: Dictionary, bop_r: float, enemies: Array) -> void:
	var ring: MeshInstance3D = m.g.get("brawl_reach_ring", null) as MeshInstance3D
	if ring == null or not is_instance_valid(ring):
		var torus := TorusMesh.new()
		torus.inner_radius = 0.93
		torus.outer_radius = 1.0
		torus.rings = 32
		torus.ring_segments = 8
		ring = MeshInstance3D.new()
		ring.mesh = torus
		var mat := StandardMaterial3D.new()
		mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		mat.emission_enabled = true
		ring.material_override = mat
		r.add_child(ring)
		m.g["brawl_reach_ring"] = ring
	ring.position = Vector3(float(s["px"]), 0.06, float(s["pz"]))
	ring.scale = Vector3(bop_r, 1.0, bop_r)
	var in_reach := false
	for e in enemies:
		var en: Node3D = e["node"]
		if not is_instance_valid(en):
			continue
		if Vector2(en.position.x - float(s["px"]), en.position.z - float(s["pz"])).length() < bop_r:
			in_reach = true
			break
	var mat_ref: StandardMaterial3D = ring.material_override as StandardMaterial3D
	if mat_ref == null:
		return
	# lit = something is poppable right now; resting = walk closer
	var col: Color = Color(1.0, 0.82, 0.42, 0.55) if in_reach else Color(0.72, 0.84, 1.0, 0.22)
	mat_ref.albedo_color = col
	mat_ref.emission = Color(col.r, col.g, col.b)
	mat_ref.emission_energy_multiplier = 0.9 if in_reach else 0.25

func _damage_imp(e: Dictionary, dmg: int) -> void:
	var en: Node3D = e["node"]
	if not is_instance_valid(en):
		return
	e["hp"] = maxi(0, int(e.get("hp", 3)) - dmg)
	if int(e["hp"]) > 0:
		m._sparkle_burst(en.global_position + Vector3(0, 2.0, 0), Color(1.0, 0.85, 0.55))
		var tw := en.create_tween()
		tw.tween_property(en, "rotation:z", 0.22, 0.07).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.tween_property(en, "rotation:z", -0.16, 0.09).set_trans(Tween.TRANS_QUAD)
		tw.tween_property(en, "rotation:z", 0.0, 0.1).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		return
	(m.g["enemies"] as Array).erase(e)
	m.g["bops"] = int(m.g["bops"]) + 1
	m._sparkle_burst(en.global_position + Vector3(0, 2.0, 0), Color(1.0, 0.75, 0.9))
	var tw2 := en.create_tween()
	tw2.tween_property(en, "scale", Vector3.ONE * 0.01, 0.3).set_ease(Tween.EASE_IN)
	tw2.tween_callback(en.queue_free)

func _nearest_imp(x: float, z: float, skip_stunned: bool) -> Dictionary:
	var best: Dictionary = {}
	var best_d := 1e9
	var enemies: Array = m.g.get("enemies", [])
	for e in enemies:
		var en: Node3D = e["node"]
		if not is_instance_valid(en):
			continue
		if skip_stunned and float(e.get("stun", 0.0)) > 0.0:
			continue
		var d: float = Vector2(en.position.x - x, en.position.z - z).length()
		if d < best_d:
			best_d = d
			best = e
	return best

## Toy-castle tuning for the shared imp brain — metres on the courtyard
## plane. Slower and shorter-ranged than the opera stage because the camera
## sits close and Roshan is walking, not standing on a mark.
const BRAWL_BRAIN_TUNE := {
	"strike_range": 11.0,
	"stand_off": 4.8,        # inside Roshan's pop reach: circling imps stay
	                         # tappable, they never hover out of her reach
	"contact": 3.0,
	"speed": IMP_SPEED,
	"charge_speed": 19.0,
	"flee_speed": 10.0,
	"windup": 0.95,
	"charge_time": 0.4,
	"slash_time": 0.26,
	"recover": 1.2,
	"stagger": 0.5,
	"guard_time": 0.8,
	"taunt_time": 0.9,
	"flee_time": 1.0,
	"cool_min": 2.6,
	"cool_max": 5.2,
	"max_attackers": 2,
}


func _spawn_wave(seg: int) -> void:
	var r := stage.root()
	var left: float = X0 + float(seg) * SEG_W
	# one brain per wave, seeded by the segment so the courtyard fights the
	# same way every run — the crew is scripted by decisions, not by luck
	var brain := ImpAI.new(BRAWL_BRAIN_TUNE, 918273 + seg * 613)
	brain.begin_crew(int(WAVES[seg]))
	m.g["imp_brain"] = brain
	m.g["imp_warned"] = bool(m.g.get("imp_warned", false))
	for i in range(int(WAVES[seg])):
		var imp := DungeonArt.spawn("imp", r,
			Vector3(left + SEG_W * 0.45 + randf() * SEG_W * 0.45,
				0.4, randf_range(-HALF_D + 1.0, HALF_D - 1.0)))
		imp.scale = Vector3.ONE * 1.6
		var mind: Dictionary = brain.spawn_mind(i, false)
		mind["pos"] = Vector2(imp.position.x, imp.position.z)
		(m.g["enemies"] as Array).append({
			"node": imp, "stun": 0.0, "bump_cd": 0.0, "ai": mind, "pose": "prowl",
			"hp": 3,   # basic imp = 3 hp (damage grammar, owner 2026-08-01)
		})


## One imp, one pose. The toy imps carry no animation clips, so every pose
## is played on the transform: a crouch before a lunge, a stretched dash, a
## swipe that rolls through, a slumped recovery that begs to be popped.
## (Art states are coming — CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md.)
func _pose_imp(e: Dictionary, en: Node3D, pose: String, t: float, hero: Vector2) -> void:
	e["pose"] = pose
	var clock: float = float(m.g.get("t", 0.0))
	var base := 1.6
	var hop: float = absf(sin(clock * 4.0 + en.position.x)) * 0.8
	var squash := Vector3(1.0, 1.0, 1.0)
	var tilt := 0.0
	match pose:
		"windup":
			hop = 0.0
			squash = Vector3(1.22, 0.74, 1.22)     # coil
			tilt = -0.22
		"charge":
			hop = 0.55
			squash = Vector3(0.86, 1.2, 0.86)      # stretched dash
			tilt = 0.35
		"slash":
			hop = 0.35
			squash = Vector3(1.14, 0.94, 1.14)
			tilt = lerpf(-0.6, 0.6, clampf(t / 0.26, 0.0, 1.0))
		"recover":
			hop = 0.0
			squash = Vector3(1.16, 0.82, 1.16)     # slumped: pop me
			tilt = -0.3
		"stagger":
			en.rotation.y += 0.12                  # dizzy spin
			hop = 0.15
			squash = Vector3(1.1, 0.9, 1.1)
		"taunt", "rally":
			hop = absf(sin(clock * 9.0)) * 1.5
			squash = Vector3(0.94, 1.1, 0.94)
		"flee":
			hop = absf(sin(clock * 10.0 + en.position.x)) * 1.1
			tilt = -0.2
	en.position.y = 0.4 + hop
	en.scale = Vector3(base * squash.x, base * squash.y, base * squash.z)
	en.rotation.z = tilt
	if pose != "stagger":
		var look := Vector2(hero.x - en.position.x, hero.y - en.position.z)
		if pose == "flee":
			look = -look
		if look.length() > 0.05:
			en.rotation.y = atan2(look.x, look.y)


func _brawl_brain_events(brain: ImpAI, r: Node3D, hero: Vector2) -> void:
	for ev: Dictionary in brain.drain_events():
		var at: Vector2 = ev.get("pos", Vector2.ZERO)
		var world_at: Vector3 = r.to_global(Vector3(at.x, 2.2, at.y))
		match String(ev.get("kind", "")):
			"telegraph":
				# gold flash + one spoken warning per castle run: a wind-up
				# is a thing to react to, never a thing to read
				m._sparkle_burst(world_at + Vector3(0, 1.4, 0), Color(1.0, 0.82, 0.3))
				if not bool(m.g.get("imp_warned", false)):
					m.g["imp_warned"] = true
					m.show_msg("Huluu", "Look out — that imp is winding up! POP it quick!", "talk")
			"charge":
				m._sparkle_burst(world_at, Color(1.0, 0.72, 0.45))
			"contact":
				_brawl_bump(int(ev.get("index", -1)), world_at, hero)
			"whiff":
				m._sparkle_burst(world_at, Color(0.92, 0.95, 1.0))
			"taunt":
				m._sparkle_burst(world_at + Vector3(0, 1.0, 0), Color(1.0, 0.7, 0.88))
			"rally":
				m._sparkle_burst(world_at + Vector3(0, 1.6, 0), Color(1.0, 0.85, 0.4))


func _brawl_bump(index: int, world_at: Vector3, hero: Vector2) -> void:
	# the giggly bump, unchanged in spirit: the imp shoves, bounces off and
	# loses ground. Nothing is taken from anybody.
	var enemies: Array = m.g.get("enemies", [])
	for e in enemies:
		var mind: Dictionary = e.get("ai", {})
		if mind.is_empty() or int(mind.get("index", -1)) != index:
			continue
		if float(e.get("bump_cd", 0.0)) > 0.0:
			return
		e["bump_cd"] = 1.4
		var here: Vector2 = mind.get("pos", hero)
		var away: Vector2 = here - hero
		if away.length() < 0.01:
			away = Vector2(1.0, 0.0)
		var shoved: Vector2 = here + away.normalized() * 2.5
		mind["pos"] = shoved
		var en: Node3D = e["node"]
		if is_instance_valid(en):
			en.position.x = shoved.x
			en.position.z = shoved.y
		break
	m._sparkle_burst(world_at, Color(1.0, 0.85, 0.55))

# ---- the toy castle courtyard ----------------------------------------------
func _stage_open() -> void:
	stage.open({
		"origin": m.ARENA_POS + Vector3(0, 2.5, 0),
		"half_w": X0 + SEG_W * float(WAVES.size()),
		"half_d": HALF_D,
		"hover": 3.0,
		"bob_amp": 0.5,
		"steer_speed": 24.8,
		"cam_h": 13.5,
		"cam_dist": 24.0,
		"look_h": 6.5,
		"cam_follow": 0.85,
		"swell": 0.6,   # the courtyard sits in the reef: a gentle shared tide
	})
	# Toy blocks strewn around Huluu's courtyard — the FIRST live prop fleet
	# (the engine shipped 2026-07-27 with zero consumers). Waterlogged per
	# the swell pairing rule so the tide can rock them; pastel banner tints
	# ARE the toy-block look until Codex standee art lands (a flat pastel
	# rectangle reads as a toy block by design). Garnish only, never logic.
	stage.props_arena()
	for i in range(6):
		stage.prop("", Vector2(1.6, 1.6), X0 + 4.0 + float(i) * 5.2,
			(-1.0 if i % 2 == 0 else 1.0) * (HALF_D - 1.5), {
				"color": BANNERS[i % BANNERS.size()],
				"drop": 0.8 + float(i % 3) * 0.6,
				"gravity_scale": 0.35, "damp": 1.0,
			})
	m._play_music("race")   # the energetic track until the castle gets its own
	var r := stage.root()
	var total_w: float = SEG_W * float(WAVES.size())
	# castle wall along the back of the plane, pastel stone + crenellations
	var wall := MeshInstance3D.new()
	var wm := BoxMesh.new()
	wm.size = Vector3(total_w + 22.0, 12.0, 3.0)
	wall.mesh = wm
	wall.position = Vector3(X0 + total_w * 0.5, 6.0, -HALF_D - 5.5)
	wall.material_override = m._soft_mat(Color(0.86, 0.80, 0.88), 0.08)
	r.add_child(wall)
	for c in range(int(total_w / 7.0)):
		var cren := MeshInstance3D.new()
		var cm := BoxMesh.new()
		cm.size = Vector3(3.0, 2.4, 3.0)
		cren.mesh = cm
		cren.position = Vector3(X0 - 8.0 + float(c) * 7.0, 13.2, -HALF_D - 5.5)
		cren.material_override = m._soft_mat(Color(0.80, 0.73, 0.84), 0.08)
		r.add_child(cren)
	# towers with candy-cone roofs at the ends, banners along the wall
	for tx in [X0 - 9.0, X0 + total_w + 9.0]:
		var tower := MeshInstance3D.new()
		var tm := CylinderMesh.new()
		tm.top_radius = 4.2
		tm.bottom_radius = 4.8
		tm.height = 18.0
		tower.mesh = tm
		tower.position = Vector3(float(tx), 9.0, -HALF_D - 5.5)
		tower.material_override = m._soft_mat(Color(0.86, 0.80, 0.88), 0.08)
		r.add_child(tower)
		var roof := MeshInstance3D.new()
		var rm := CylinderMesh.new()
		rm.top_radius = 0.1
		rm.bottom_radius = 5.2
		rm.height = 6.5
		roof.mesh = rm
		roof.position = Vector3(float(tx), 21.2, -HALF_D - 5.5)
		roof.material_override = m._soft_mat(Color(0.78, 0.55, 0.75), 0.14)
		r.add_child(roof)
	for b in range(int(total_w / 12.0)):
		var ban := MeshInstance3D.new()
		var bqm := QuadMesh.new()
		bqm.size = Vector2(2.6, 4.2)
		ban.mesh = bqm
		ban.position = Vector3(X0 + 4.0 + float(b) * 12.0, 8.5, -HALF_D - 3.9)
		ban.material_override = m._soft_mat(BANNERS[b % BANNERS.size()], 0.2)
		r.add_child(ban)
	# gates between segments: chunky pastel portcullis bars that lift open
	for gx in range(WAVES.size() - 1):
		var gate := Node3D.new()
		gate.position = Vector3(X0 + float(gx + 1) * SEG_W, 0.0, 0.0)
		for bar in range(5):
			var bm2 := MeshInstance3D.new()
			var brm := BoxMesh.new()
			brm.size = Vector3(0.9, 11.0, 0.9)
			bm2.mesh = brm
			bm2.position = Vector3(0, 5.5, -HALF_D + 0.8 + float(bar) * 3.1)
			bm2.material_override = m._soft_mat(Color(0.94, 0.83, 0.55), 0.16)
			gate.add_child(bm2)
		r.add_child(gate)
		(m.g["gates"] as Array).append(gate)
	# HULUU, player 2: the stuffie herself as an illustrated-cutout hero
	stage.companion_open("res://assets/characters/friends/huluu.png", 5.5,
		Vector3(-6.0, 0, 3.0))

func _open_gate(seg: int) -> void:
	var gates: Array = m.g["gates"]
	if seg >= gates.size():
		return
	var gate: Node3D = gates[seg]
	if gate == null or not is_instance_valid(gate):
		return
	m._sparkle_burst(gate.global_position + Vector3(0, 5.0, 0), Color(1.0, 0.9, 0.5))
	var tw := gate.create_tween()
	tw.tween_property(gate, "position:y", 12.5, 0.9).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
