class_name FairyGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# fairyshoot minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

# ===================== FAIRY POND — OVERHEAD SCROLLING BULLET HELL =====================
# A gentle top-down scrolling shooter sized for a 4-year-old: the camera hangs
# straight above a long pond "track" that glides beneath Roshan (in her fairy
# form) like a classic overhead shmup. She drifts up the screen on her own; the
# stick only slides her around the screen window — no jump, no turning, no depth.
# Shadow bugs wait along the track and lob big slow shadow sparks to dodge, and
# scary-but-toylike shadow monsters (jellies, urchins, eels) prowl the lane; her
# wand zaps straight up the screen all by itself. SPACE / the big button pops a
# sparkle shield that clears the sparks around her. The Fairy Flower boss waits
# at the end of the track.
const FS_LEN := 280.0          # track length (forward, +Z = up the screen)
const FS_FWD := 19.0           # auto-scroll speed (~15 s of cruise to the boss)
const FS_PLANE := 3.0          # everything gameplay lives at this height (flat = 2D)
const FS_CAM_H := 58.0         # overhead camera height
const FS_LOOK := 6.0           # camera looks a touch ahead, shmup-style
const FS_MOVE := 19.0          # direct steer speed (no momentum)
const FS_BX := 20.0            # half movement bound, across the screen
const FS_BZB := 12.0           # movement bound, down the screen (hanging back)
const FS_BZF := 14.0           # movement bound, up the screen (pushing ahead)
const FS_BOLT := 55.0          # wand bolt speed
const FS_BOLT_FLY := 46.0      # bolt lifetime distance (a bit past the screen top)
const FS_FIRE_CD := 0.25
const FS_HIT_R := 3.4          # forgiving bolt-vs-bug radius
const FS_BUG_R := 2.2
const FS_NBUGS := 10           # shadow bugs waiting along the track
const FS_BUG_WAKE := 36.0      # bugs this far up the screen start lobbing sparks
const FS_HEARTS := 3
const FS_ORB_SPD := 6.5        # shadow spark speed (slow enough to see coming)
const FS_HAZ_R := 3.2          # shadow-monster touch radius (jelly / urchin)
const FS_ORB_R := 2.6          # spark-vs-Roshan touch radius
const FS_ORB_CD_MIN := 3.0     # each awake bug lobs a spark every 3-5 s
const FS_ORB_CD_MAX := 5.0
const FS_ORB_MAX := 6          # never more sparks than this on screen
const FS_HURT_T := 1.6         # sparkle-blink safety time after a bump
const FS_NOVA_CD := 3.0        # sparkle-shield cooldown
const FS_NOVA_R := 11.0        # sparkle-shield clear radius
# ---- final boss: the Fairy Flower at the end of the track ----
const FS_BOSS_AHEAD := 24.0        # boss sits near the top of the frozen screen
const FS_BOSS_HIT_R := 5.5         # generous hitboxes
const FS_LEAVES := 6               # outer leaf shield
const FS_LEAF_HP := 1              # one blast per leaf
const FS_LEAF_T := 20.0            # seconds to blast the leaves away
const FS_LEAF_RING := 9.5          # leaf wreath radius (spins slowly around the bud)
const FS_BUD_HP := 10
const FS_BUD_T := 20.0             # seconds to bloom the flower open
const FS_BLOOM_T := 3.0
const FS_RING_CD := 4.5            # the flower puffs a slow ring of sparks
const FS_RING_N := 6
const FS_LEAF_SCALE := 6.5
const FS_BUG_ART_SCALE := 7.0
const FS_BACKGROUND_ART := [
	"res://assets/fairy/pond_dawn.png",
	"res://assets/fairy/pond_twilight.png",
	"res://assets/fairy/pond_boss_clearing.png",
]
const FS_BUG_ART := [
	"res://assets/fairy/models/bug_jewel.glb",
	"res://assets/fairy/models/bug_moth.glb",
	"res://assets/fairy/models/bug_firefly.glb",
]
const FS_BOSS_ART := {
	"seed": "res://assets/fairy/models/boss_seed.glb",
	"sprout": "res://assets/fairy/models/boss_sprout.glb",
	"bud": "res://assets/fairy/models/boss_bud.glb",
	"opening": "res://assets/fairy/models/boss_opening.glb",
	"bloom": "res://assets/fairy/models/boss_bloom.glb",
}
const FS_BOSS_STAGE_SCALE := {
	"seed": 7.0,
	"sprout": 9.0,
	"bud": 12.0,
	"opening": 15.5,
	"bloom": 20.0,
}
const FS_BOSS_LEAF_ART := "res://assets/fairy/models/boss_leaf.glb"

func _fairy_art_item(path: String, pos: Vector3, scl: float, yrot: float = 0.0) -> Node3D:
	var ps: PackedScene = m._fairy_art_cache.get(path, null)
	if ps == null:
		if not ResourceLoader.exists(path):
			return null
		ps = load(path)
		m._fairy_art_cache[path] = ps
	if ps == null:
		return null
	var item: Node3D = ps.instantiate()
	item.position = pos
	item.scale = Vector3.ONE * scl
	item.rotation.y = yrot
	m.add_child(item)
	m.game_nodes.append(item)
	return item

func _fairy_background_panel(origin: Vector3, texture_path: String, z_center: float, depth: float) -> void:
	if not ResourceLoader.exists(texture_path):
		return
	var texture: Texture2D = load(texture_path)
	if texture == null:
		return
	var panel := MeshInstance3D.new()
	var plane := PlaneMesh.new()
	plane.size = Vector2(90.0, depth)
	panel.mesh = plane
	var material := StandardMaterial3D.new()
	material.albedo_texture = texture
	material.roughness = 1.0
	material.metallic = 0.0
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	panel.material_override = material
	panel.position = origin + Vector3(0, 0.06, z_center)
	m.add_child(panel)
	m.game_nodes.append(panel)

func _fairy_set_boss_stage(stage: String) -> Node3D:
	var current: Node3D = m.g.get("boss_art")
	if String(m.g.get("boss_stage", "")) == stage and current != null and is_instance_valid(current):
		return current
	if current != null and is_instance_valid(current):
		current.queue_free()
	var path: String = String(FS_BOSS_ART.get(stage, ""))
	var scale_value: float = float(FS_BOSS_STAGE_SCALE.get(stage, 8.0))
	var center: Vector3 = m.g.get("boss_center", m.ARENA_POS)
	var art: Node3D = _fairy_art_item(path, center + Vector3(0, 0.18, 0), scale_value)
	m.g["boss_art"] = art
	m.g["boss_stage"] = stage
	m.g["bud"] = art   # compatibility for probes and cleanup paths that still name the focal node "bud"
	return art

func _build_fairyshoot(origin: Vector3) -> void:
	# Roshan wears her fairy form for this game only
	m.player.set_skin("fairy", m.FAIRY_SKIN_PATH)
	if m.chime != null:
		m.chime.volume_db = -13.0   # the wand fires a lot — keep its chime soft (restored in _end_game)
	m.g["fz"] = 0.0; m.g["ox"] = 0.0; m.g["oz"] = 0.0
	m.g["hits"] = 0; m.g["fire_cd"] = 0.0
	m.g["hearts"] = FS_HEARTS; m.g["hurt_t"] = 0.0; m.g["nova_cd"] = 0.0
	m.g["player_acted"] = false; m.g["awaiting_cheer"] = false
	m.g["fairy_wait_release"] = false
	m.g["targets"] = []; m.g["bolts"] = []; m.g["orbs"] = []; m.g["fireflies"] = []; m.g["rings"] = []
	m.g["hazards"] = []
	m.g["phase"] = "fly"; m.g["leaves"] = []; m.g["bud"] = null; m.g["petals"] = []
	m.g["boss_art"] = null; m.g["boss_stage"] = ""
	# ---- three authored overhead pond plates replace the metallic box, stock
	# banks, and primitive lily/reed dressing. Their quiet center preserves the
	# one-finger flight lane while the edge art changes from dawn to twilight to
	# the circular boss clearing. ----
	for bg_index in range(FS_BACKGROUND_ART.size()):
		_fairy_background_panel(origin, String(FS_BACKGROUND_ART[bg_index]), 50.0 + float(bg_index) * 120.0, 120.0)
	# Modeled flower arches keep the fly-through goals readable over the
	# purpose-built Fairy Pond V2 background plates.
	for k in range(6):
		var z2: float = 40.0 + float(k) * 40.0
		var rx: float = randf() * 16.0 - 8.0
		var ring: Node3D = m._art35_prop("res://assets/art35/arena/fairy_flower_gate.glb", origin + Vector3(rx, 0.8, z2), 1.05)
		(m.g["rings"] as Array).append({"node": ring, "x": rx, "z": z2, "done": false})
	# ---- drifting fireflies, low over the water (below the flight plane) ----
	for i in range(24):
		var ff := MeshInstance3D.new()
		var fm := SphereMesh.new(); fm.radius = 0.3; fm.height = 0.6
		ff.mesh = fm
		ff.material_override = m._soft_mat(Color(1.0, 0.95, 0.6), 3.0)
		ff.position = origin + Vector3(randf() * 68.0 - 34.0, 1.6, 15.0 + randf() * (FS_LEN + 20.0))
		m.add_child(ff); m.game_nodes.append(ff)
		(m.g["fireflies"] as Array).append({"node": ff, "ph": randf() * TAU, "base": ff.position})
	# ---- shadow bugs waiting along the track ----
	for k in range(FS_NBUGS):
		var z3: float = 70.0 + float(k) / float(FS_NBUGS) * (FS_LEN - 100.0) + randf() * 12.0
		var bx: float = (randf() * 2.0 - 1.0) * (FS_BX - 2.0)
		var bpos: Vector3 = origin + Vector3(bx, FS_PLANE, z3)
		var bug_path: String = String(FS_BUG_ART[k % FS_BUG_ART.size()])
		var bug: Node3D = _fairy_art_item(bug_path, bpos, FS_BUG_ART_SCALE, randf() * TAU)
		if bug == null:
			bug = Node3D.new()
			var fallback := MeshInstance3D.new()
			var sm := SphereMesh.new(); sm.radius = FS_BUG_R; sm.height = FS_BUG_R * 2.0
			fallback.mesh = sm
			fallback.material_override = m._soft_mat(Color(0.35, 0.12, 0.5), 0.8)
			bug.add_child(fallback)
			bug.position = bpos
			m.add_child(bug); m.game_nodes.append(bug)
		(m.g["targets"] as Array).append({"node": bug, "base": bpos, "alive": true,
				"ph": randf() * TAU, "orb_cd": 1.0 + randf() * 2.0})
	# ---- scary-but-toylike shadow monsters lurking along the track ----
	_fairy_build_hazards(origin)
	# ---- wand aim guide floating up-screen of Roshan ----
	var ret := MeshInstance3D.new()
	var rt := TorusMesh.new(); rt.inner_radius = 1.1; rt.outer_radius = 1.5; rt.rings = 16; rt.ring_segments = 8
	ret.mesh = rt
	ret.material_override = m._soft_mat(Color(1.0, 0.9, 0.4), 2.5)
	m.add_child(ret); m.game_nodes.append(ret)
	m.g["reticle"] = ret
	# ---- Roshan at the start of the track; camera snaps straight overhead ----
	m.player.position = origin + Vector3(0, FS_PLANE, 0)
	m.player.vel = Vector3.ZERO
	if m.player.cam != null and m.player.cam.is_inside_tree():
		m.player.cam.position = origin + Vector3(0, FS_CAM_H, FS_LOOK)
		m.player.cam.look_at(origin + Vector3(0, 0, FS_LOOK), Vector3(0, 0, 1))

func _fairy_eye(parent: Node3D, off: Vector3) -> void:
	# a glowing monster eye — reads clearly from straight above
	var eye := MeshInstance3D.new()
	var em := SphereMesh.new(); em.radius = 0.38; em.height = 0.76
	eye.mesh = em
	eye.material_override = m._soft_mat(Color(1.0, 0.55, 0.2), 2.6)
	eye.position = off
	parent.add_child(eye)

func _fairy_build_hazards(origin: Vector3) -> void:
	# scary-but-toylike shadow monsters to steer around — the wand can't zap
	# them, so the only answer is to fly around them (all one heart on touch)
	var shadow := m._soft_mat(Color(0.16, 0.08, 0.26), 0.35)
	# shadow jellyfish that drift loops around their spot
	for k in range(4):
		var jz: float = 55.0 + float(k) * ((FS_LEN - 110.0) / 3.0)
		var jelly_pos: Vector3 = origin + Vector3((randf() * 2.0 - 1.0) * (FS_BX - 4.0), FS_PLANE, jz)
		var jelly: Node3D = m._art35_prop("res://assets/art35/arena/fairy_shadow_jellyfish.glb", jelly_pos, 1.32, randf() * TAU)
		if jelly == null:
			continue
		(m.g["hazards"] as Array).append({"node": jelly, "kind": "jelly", "base": jelly.position, "ph": randf() * TAU})
	# spiky shadow urchins that spin in place
	for k in range(3):
		var uz: float = 75.0 + float(k) * ((FS_LEN - 150.0) / 2.0)
		var upos := origin + Vector3((randf() * 2.0 - 1.0) * (FS_BX - 6.0), FS_PLANE - 1.4, uz)
		var urch: Node3D = m._gen2_prop("urchin_story", upos, 5.2, randf() * TAU, 0.0)
		if urch == null:
			urch = Node3D.new()
			var core := MeshInstance3D.new()
			var cm2 := SphereMesh.new(); cm2.radius = 1.9; cm2.height = 3.8
			core.mesh = cm2; core.material_override = shadow
			urch.add_child(core)
			for s in range(8):
				var sa: float = float(s) / 8.0 * TAU
				var spike := MeshInstance3D.new()
				var spm2 := CylinderMesh.new(); spm2.top_radius = 0.0; spm2.bottom_radius = 0.5; spm2.height = 2.4
				spike.mesh = spm2; spike.material_override = m._soft_mat(Color(0.8, 0.3, 1.0), 1.2)
				spike.position = Vector3(cos(sa) * 2.6, 0, sin(sa) * 2.6)
				spike.rotation = Vector3(0, -sa, -PI / 2.0)
				urch.add_child(spike)
			urch.position = upos
			m.add_child(urch)
		m.game_nodes.append(urch)
		(m.g["hazards"] as Array).append({"node": urch, "kind": "urchin", "base": urch.position, "ph": randf() * TAU})
	# shadow eels sweeping side to side across the lane — time the gap!
	for k in range(2):
		var ez: float = FS_LEN * (0.4 if k == 0 else 0.75)
		var eel_pos: Vector3 = origin + Vector3(0, FS_PLANE, ez)
		var eel: Node3D = m._art35_prop("res://assets/art35/arena/fairy_shadow_eel.glb", eel_pos, 1.25, PI * 0.5)
		if eel == null:
			continue
		(m.g["hazards"] as Array).append({"node": eel, "kind": "eel", "base": eel.position, "ph": float(k) * PI})

func _fairy_spawn_orb(from: Vector3, dirv: Vector3) -> void:
	# a slow glowing shadow spark — the "bullet" of this bullet hell
	var orb := MeshInstance3D.new()
	var om := SphereMesh.new(); om.radius = 1.2; om.height = 2.4
	orb.mesh = om
	var omat := StandardMaterial3D.new()
	omat.albedo_color = Color(0.2, 0.06, 0.28)
	omat.emission_enabled = true; omat.emission = Color(0.7, 0.3, 1.0); omat.emission_energy_multiplier = 2.2
	orb.material_override = omat
	orb.position = from
	m.add_child(orb); m.game_nodes.append(orb)
	(m.g["orbs"] as Array).append({"node": orb, "dir": dirv})

func _fairy_clear_orbs() -> void:
	for od in m.g["orbs"]:
		if is_instance_valid(od["node"]):
			(od["node"] as Node3D).queue_free()
	(m.g["orbs"] as Array).clear()

func _fairy_start_boss(origin: Vector3) -> void:
	# The scroll freezes and the authored Fairy Flower fills the top of the screen.
	var center: Vector3 = origin + Vector3(0, FS_PLANE, float(m.g["fz"]) + FS_BOSS_AHEAD)
	m.g["boss_center"] = center
	m.g["phase"] = "boss_leaves"
	# retry kindness: each earlier fail stretches both boss timers by 6s (max +12)
	m.g["phase_t"] = FS_LEAF_T + 6.0 * float(mini(m.fs_fails, 2))
	m.g["ring_cd"] = FS_RING_CD
	_fairy_clear_orbs()   # a clean entrance for the flower
	# Begin with the small cracked seed; matched reliefs replace it as it grows.
	_fairy_set_boss_stage("seed")
	m.g["bud_hp"] = FS_BUD_HP
	# Six matching authored leaves orbit slowly so one stays lined up with the wand.
	m.g["leaves"] = []
	for k in range(FS_LEAVES):
		var a: float = float(k) / float(FS_LEAVES) * TAU
		var lp: Vector3 = center + Vector3(cos(a) * FS_LEAF_RING, -1.0, sin(a) * FS_LEAF_RING)
		var leaf: Node3D = _fairy_art_item(FS_BOSS_LEAF_ART, lp, FS_LEAF_SCALE, PI / 2.0 - a)
		if leaf == null:
			var lm := MeshInstance3D.new()
			var pm := PrismMesh.new(); pm.size = Vector3(5.0, 9.0, 2.0)
			lm.mesh = pm; lm.material_override = m._soft_mat(Color(0.35, 0.75, 0.4), 0.4)
			lm.position = lp; m.add_child(lm); m.game_nodes.append(lm); leaf = lm
		(m.g["leaves"] as Array).append({"node": leaf, "hp": FS_LEAF_HP, "ang": a})
	m.show_msg(fr_name_safe(), "The Fairy Flower! Blast the leaves out of the way!")

func fr_name_safe() -> String:
	return String((m.g.get("fr", {}) as Dictionary).get("fname", "Fairy Pond"))

func _fairy_bloom_start() -> void:
	m.g["phase"] = "boss_bloom"
	m.g["bloom_t"] = FS_BLOOM_T
	_fairy_clear_orbs()   # nothing to dodge during the celebration
	m.g["petals"] = []
	# One coherent full-blossom model grows outward for the celebration.
	var bloom: Node3D = _fairy_set_boss_stage("bloom")
	if bloom != null:
		bloom.scale = Vector3.ONE * (float(FS_BOSS_STAGE_SCALE["bloom"]) * 0.72)

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	_build_fairyshoot(origin)
	m._play_music("melody")   # dreamy track
	m.show_msg(fr["fname"], "Fly up the fairy pond! Dodge the sparks and the shadow monsters — your wand zaps ahead all by itself! SPACE / TAP makes a sparkle shield!")

func _tick_fairyshoot(delta: float, fr: Dictionary, _ppos: Vector3) -> void:
	var origin: Vector3 = m.ARENA_POS
	var phase: String = String(m.g.get("phase", "fly"))
	var tt: float = float(m.g["t"])
	# ---- the track scrolls on its own; the stick only slides Roshan around ----
	if phase == "fly":
		m.g["fz"] = float(m.g["fz"]) + FS_FWD * delta
	var fz: float = m.g["fz"]
	var inx := 0.0
	var iny := 0.0
	if Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A):
		inx -= 1.0
	if Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D):
		inx += 1.0
	if Input.is_physical_key_pressed(KEY_UP) or Input.is_physical_key_pressed(KEY_W):
		iny += 1.0
	if Input.is_physical_key_pressed(KEY_DOWN) or Input.is_physical_key_pressed(KEY_S):
		iny -= 1.0
	var jx: float = m.joy_axis(JOY_AXIS_LEFT_X)
	var jy: float = m.joy_axis(JOY_AXIS_LEFT_Y)
	if absf(jx) > 0.2: inx += jx
	if absf(jy) > 0.2: iny -= jy
	if m.touch_ui != null:
		if absf(m.touch_ui.stick_vec.x) > 0.15: inx += m.touch_ui.stick_vec.x
		if absf(m.touch_ui.stick_vec.y) > 0.15: iny -= m.touch_ui.stick_vec.y
	if absf(inx) > 0.15 or absf(iny) > 0.15:
		m.g["player_acted"] = true
	# x negated so 'right' reads screen-right under the overhead camera
	var ox: float = clampf(float(m.g["ox"]) - clampf(inx, -1.0, 1.0) * FS_MOVE * delta, -FS_BX, FS_BX)
	var oz: float = clampf(float(m.g["oz"]) + clampf(iny, -1.0, 1.0) * FS_MOVE * delta, -FS_BZB, FS_BZF)
	m.g["ox"] = ox; m.g["oz"] = oz
	var pos: Vector3 = origin + Vector3(ox, FS_PLANE, fz + oz)
	m.player.position = pos
	m.player.vel = Vector3.ZERO
	# ---- fixed overhead camera glides up the track: reads like a scrolling 2D map ----
	if m.player.cam != null and m.player.cam.is_inside_tree():
		var focus: Vector3 = origin + Vector3(ox * 0.15, 0, fz + FS_LOOK)
		m.player.cam.position = m.player.cam.position.lerp(focus + Vector3(0, FS_CAM_H, 0), 1.0 - pow(0.002, delta))
		m.player.cam.look_at(focus, Vector3(0, 0, 1))
	# ---- sparkle-blink safety time after a bump ----
	m.g["hurt_t"] = maxf(0.0, float(m.g["hurt_t"]) - delta)
	m.player.visible = float(m.g["hurt_t"]) <= 0.0 or fmod(tt, 0.24) > 0.09
	# ---- sparkle shield: one big friendly button clears nearby sparks ----
	m.g["nova_cd"] = maxf(0.0, float(m.g["nova_cd"]) - delta)
	var nova_pressed: bool = Input.is_physical_key_pressed(KEY_SPACE) or Input.is_joy_button_pressed(0, JOY_BUTTON_A)
	if m.touch_ui != null and m.touch_ui.action_down:
		nova_pressed = true
	if bool(m.g.get("fairy_wait_release", false)):
		if not nova_pressed:
			m.g["fairy_wait_release"] = false
		nova_pressed = false
	if nova_pressed:
		m.g["player_acted"] = true
	# one-finger auto-assist: steering leaves no thumb for the shield button,
	# so when a shadow spark drifts close the shield pulses ITSELF (the manual
	# press above still works). Defensive only — the auto path never sets
	# player_acted, so a zero-input player still cannot progress
	# (probe_passive fairy agency: bloom waits for a real verb).
	if not nova_pressed and float(m.g["nova_cd"]) <= 0.0:
		for od_a in (m.g["orbs"] as Array):
			var on_a: Node3D = od_a["node"]
			if is_instance_valid(on_a) and on_a.position.distance_to(pos) < FS_NOVA_R * 0.8:
				nova_pressed = true
				break
	if nova_pressed and float(m.g["nova_cd"]) <= 0.0:
		m.g["nova_cd"] = FS_NOVA_CD
		for k in range(6):
			var na: float = float(k) / 6.0 * TAU
			m._sparkle_burst(pos + Vector3(cos(na) * 4.0, 0.5, sin(na) * 4.0), Color(0.7, 0.95, 1.0))
		var orbs0: Array = m.g["orbs"]
		for oi0 in range(orbs0.size() - 1, -1, -1):
			var od0: Dictionary = orbs0[oi0]
			var on0: Node3D = od0["node"]
			if not is_instance_valid(on0):
				orbs0.remove_at(oi0); continue
			if on0.position.distance_to(pos) < FS_NOVA_R:
				m._sparkle_burst(on0.position, Color(0.85, 0.7, 1.0))
				on0.queue_free(); orbs0.remove_at(oi0)
		if m.chime != null:
			m.chime.pitch_scale = 1.6; m.chime.play()
	# ---- fairy rings sparkle as Roshan flies over them ----
	for rd in m.g["rings"]:
		if not rd["done"] and is_instance_valid(rd["node"]):
			if absf(pos.x - (origin.x + float(rd["x"]))) < 4.5 and absf(pos.z - (origin.z + float(rd["z"]))) < 3.0:
				rd["done"] = true
				m._sparkle_burst(pos, Color(1.0, 0.95, 0.6))
				if m.chime != null:
					m.chime.pitch_scale = 1.5; m.chime.play()
	# ---- shadow bugs bob in place; the ones on screen lob slow sparks ----
	for td in m.g["targets"]:
		if not td["alive"] or not is_instance_valid(td["node"]):
			continue
		var b0: Vector3 = td["base"]
		var bp: Vector3 = b0 + Vector3(sin(tt * 0.8 + float(td["ph"])) * 3.0, sin(tt * 2.0 + float(td["ph"])) * 0.5, 0)
		(td["node"] as Node3D).position = bp
		var ahead: float = bp.z - pos.z
		if ahead > -4.0 and ahead < FS_BUG_WAKE:
			td["orb_cd"] = float(td["orb_cd"]) - delta
			if float(td["orb_cd"]) <= 0.0 and (m.g["orbs"] as Array).size() < FS_ORB_MAX:
				td["orb_cd"] = FS_ORB_CD_MIN + randf() * (FS_ORB_CD_MAX - FS_ORB_CD_MIN)
				var dirv := Vector3(pos.x - bp.x, 0, pos.z - bp.z)
				if dirv.length() > 0.5:
					_fairy_spawn_orb(Vector3(bp.x, origin.y + FS_PLANE, bp.z), dirv.normalized())
	# ---- sparks drift; touching one uses sparkle energy, which refills with
	# extra safety time instead of ending the game ----
	var orbs: Array = m.g["orbs"]
	for oi in range(orbs.size() - 1, -1, -1):
		var od: Dictionary = orbs[oi]
		var on: Node3D = od["node"]
		if not is_instance_valid(on):
			orbs.remove_at(oi); continue
		on.position += (od["dir"] as Vector3) * FS_ORB_SPD * delta
		on.scale = Vector3.ONE * (1.0 + sin(tt * 6.0) * 0.12)
		if on.position.z < pos.z - 14.0 or on.position.z > pos.z + 52.0 or absf(on.position.x - origin.x) > 46.0:
			on.queue_free(); orbs.remove_at(oi); continue
		if float(m.g["hurt_t"]) <= 0.0 and on.position.distance_to(pos) < FS_ORB_R:
			on.queue_free(); orbs.remove_at(oi)
			m.g["hearts"] = int(m.g["hearts"]) - 1
			m.g["hurt_t"] = FS_HURT_T
			m._sparkle_burst(pos, Color(0.7, 0.4, 1.0))
			if m.chime != null:
				m.chime.pitch_scale = 0.7; m.chime.play()
			if int(m.g["hearts"]) <= 0:
				m.fs_fails += 1
				m.g["hearts"] = FS_HEARTS
				m.g["hurt_t"] = FS_HURT_T * 2.0
				m.player.visible = true
				m.show_msg(fr["fname"], "Sparkle shield! Your fairy light is full again — keep flying!", "encourage")
	# ---- shadow monsters prowl the track: jellies drift, urchins spin,
	# eels sweep the whole lane — the wand can't zap them, only flying
	# around them works (one heart on touch, same sparkle-blink mercy) ----
	for hd in m.g["hazards"]:
		var hn: Node3D = hd["node"]
		if not is_instance_valid(hn):
			continue
		var hkind: String = hd["kind"]
		var hb: Vector3 = hd["base"]
		var hph: float = hd["ph"]
		var hhit := false
		if hkind == "jelly":
			hn.position = hb + Vector3(sin(tt * 0.7 + hph) * 4.0, 0, sin(tt * 0.9 + hph) * 3.0)
			hn.scale = Vector3.ONE * (1.0 + sin(tt * 3.0 + hph) * 0.1)
			hhit = hn.position.distance_to(pos) < FS_HAZ_R
		elif hkind == "urchin":
			hn.rotation.y = tt * 1.1 + hph
			hhit = hn.position.distance_to(pos) < FS_HAZ_R
		else:   # eel: long body, box-ish touch check across the lane
			hn.position = hb + Vector3(sin(tt * 0.5 + hph) * (FS_BX - 6.0), 0, 0)
			hhit = absf(pos.z - hn.position.z) < 2.6 and absf(pos.x - hn.position.x) < 7.6
		if hhit and float(m.g["hurt_t"]) <= 0.0:
			m.g["hearts"] = int(m.g["hearts"]) - 1
			m.g["hurt_t"] = FS_HURT_T
			m._sparkle_burst(pos, Color(0.7, 0.4, 1.0))
			if m.chime != null:
				m.chime.pitch_scale = 0.7; m.chime.play()
			if int(m.g["hearts"]) <= 0:
				m.fs_fails += 1
				m.g["hearts"] = FS_HEARTS
				m.g["hurt_t"] = FS_HURT_T * 2.0
				m.player.visible = true
				m.show_msg(fr["fname"], "Sparkle shield! Your fairy light is full again — keep flying!", "encourage")
	# ---- wand aim guide floats up-screen of Roshan ----
	if m.g.has("reticle") and is_instance_valid(m.g["reticle"]):
		var ret := m.g["reticle"] as Node3D
		ret.visible = phase != "boss_bloom"
		ret.position = pos + Vector3(0, 1.5, 12.0)
	# ---- firing (auto-shooter: bolts zap straight up the screen; you just line up) ----
	m.g["fire_cd"] = maxf(0.0, float(m.g["fire_cd"]) - delta)
	if phase != "boss_bloom" and float(m.g["fire_cd"]) <= 0.0:
		m.g["fire_cd"] = FS_FIRE_CD
		var bolt := MeshInstance3D.new()
		var bsm := SphereMesh.new(); bsm.radius = 0.6; bsm.height = 1.2
		bolt.mesh = bsm
		bolt.material_override = m._soft_mat(Color(0.6, 1.0, 0.9), 3.0)
		bolt.position = pos + Vector3(0, 0, 2.0)
		m.add_child(bolt); m.game_nodes.append(bolt)
		(m.g["bolts"] as Array).append({"node": bolt, "fly": 0.0})
		if m.chime != null:
			m.chime.pitch_scale = 1.8; m.chime.play()
	# ---- advance bolts, check hits ----
	var bolts: Array = m.g["bolts"]
	for bi in range(bolts.size() - 1, -1, -1):
		var bd: Dictionary = bolts[bi]
		var bn: Node3D = bd["node"]
		if not is_instance_valid(bn):
			bolts.remove_at(bi); continue
		bn.position.z += FS_BOLT * delta
		bd["fly"] = float(bd["fly"]) + FS_BOLT * delta
		var dead: bool = float(bd["fly"]) > FS_BOLT_FLY
		for td in m.g["targets"]:
			if not td["alive"] or not is_instance_valid(td["node"]):
				continue
			if bn.position.distance_to((td["node"] as Node3D).position) < FS_HIT_R:
				td["alive"] = false
				m.g["hits"] = int(m.g["hits"]) + 1
				var tn: Node = td["node"]
				m._sparkle_burst((tn as Node3D).position, Color(1.0, 0.5, 0.7))
				if is_instance_valid(tn): tn.queue_free()
				if m.chime != null:
					m.chime.pitch_scale = 1.2; m.chime.play()
				dead = true
				break
		# boss: leaf shield
		if not dead and phase == "boss_leaves":
			for lf in m.g["leaves"]:
				if int(lf["hp"]) <= 0 or not is_instance_valid(lf["node"]):
					continue
				if bn.position.distance_to((lf["node"] as Node3D).position) < FS_BOSS_HIT_R:
					lf["hp"] = int(lf["hp"]) - 1
					m._sparkle_burst((lf["node"] as Node3D).position, Color(0.5, 1.0, 0.5))
					if int(lf["hp"]) <= 0:
						(lf["node"] as Node3D).queue_free()
						if m.chime != null: m.chime.pitch_scale = 1.4; m.chime.play()
					dead = true
					break
		# boss: flower bud
		if not dead and phase == "boss_bud" and m.g.get("bud") != null and is_instance_valid(m.g["bud"]):
			var center1: Vector3 = m.g["boss_center"]
			if bn.position.distance_to(center1) < FS_BOSS_HIT_R + 1.0:
				m.g["bud_hp"] = int(m.g["bud_hp"]) - 1
				m._sparkle_burst(center1 + Vector3(randf() * 4 - 2, 0.5, randf() * 4 - 2), Color(1.0, 0.7, 0.85))
				if m.chime != null: m.chime.pitch_scale = 1.1 + 0.02 * float(FS_BUD_HP - int(m.g["bud_hp"])); m.chime.play()
				dead = true
		if dead:
			bn.queue_free(); bolts.remove_at(bi)
	# ---- firefly idle drift ----
	for ffd in m.g["fireflies"]:
		if is_instance_valid(ffd["node"]):
			var b: Vector3 = ffd["base"]
			(ffd["node"] as Node3D).position = b + Vector3(sin(tt * 1.3 + float(ffd["ph"])) * 2.0, 0, cos(tt * 1.1 + float(ffd["ph"])) * 1.5)
	# ---- phase logic ----
	var hearts_str: String = "💗".repeat(maxi(0, int(m.g["hearts"])))
	if phase == "fly":
		m.hud_game.text = "Fairy Pond!  Shadow bugs zapped: %d / %d   %s" % [int(m.g["hits"]), FS_NBUGS, hearts_str]
		if fz >= FS_LEN:
			_fairy_start_boss(origin)
		return
	# ---- the flower puffs slow rings of sparks to weave through ----
	if phase != "boss_bloom":
		m.g["ring_cd"] = float(m.g.get("ring_cd", FS_RING_CD)) - delta
		if float(m.g["ring_cd"]) <= 0.0:
			m.g["ring_cd"] = FS_RING_CD
			var center2: Vector3 = m.g["boss_center"]
			for k in range(FS_RING_N):
				var ra: float = float(k) / float(FS_RING_N) * TAU + tt * 0.3
				_fairy_spawn_orb(center2 + Vector3(cos(ra) * (FS_LEAF_RING + 2.0), 0, sin(ra) * (FS_LEAF_RING + 2.0)), Vector3(cos(ra), 0, sin(ra)))
	m.g["phase_t"] = float(m.g.get("phase_t", 0.0)) - delta
	var pt: float = maxf(0.0, float(m.g["phase_t"]))
	if phase == "boss_leaves":
		var left := 0
		# Spin the custom leaf wreath slowly and rustle the survivors.
		var center3: Vector3 = m.g["boss_center"]
		for lf in m.g["leaves"]:
			if int(lf["hp"]) > 0:
				left += 1
				if is_instance_valid(lf["node"]):
					lf["ang"] = float(lf["ang"]) + delta * 0.3
					(lf["node"] as Node3D).position = center3 + Vector3(cos(float(lf["ang"])) * FS_LEAF_RING, -1.0, sin(float(lf["ang"])) * FS_LEAF_RING)
					(lf["node"] as Node3D).scale = Vector3.ONE * (FS_LEAF_SCALE * (1.0 + sin(tt * 4.0 + float(lf["ang"])) * 0.06))
		var seed_art: Node3D = m.g.get("boss_art")
		if seed_art != null and is_instance_valid(seed_art):
			seed_art.scale = Vector3.ONE * (float(FS_BOSS_STAGE_SCALE["seed"]) * (1.0 + sin(tt * 2.0) * 0.035))
		m.hud_game.text = "Blast the leaves away!   leaves left: %d   %s" % [left, hearts_str]
		if left <= 0:
			m.g["phase"] = "boss_bud"
			m.g["phase_t"] = FS_BUD_T + 6.0 * float(mini(m.fs_fails, 2))
			_fairy_set_boss_stage("sprout")
			m.show_msg(fr_name_safe(), "The flower! Keep blasting to make it grow and bloom!")
		elif pt <= 0.0:
			m.fs_fails += 1
			m.g["phase_t"] = FS_LEAF_T + 6.0 * float(mini(m.fs_fails, 2))
			m.g["hearts"] = FS_HEARTS
			m.g["ring_cd"] = FS_RING_CD * 2.0
			_fairy_clear_orbs()
			m.player.visible = true
			m.show_msg(fr["fname"], "The fairy light made more time! Keep lining up with the leaves!", "encourage")
		return
	if phase == "boss_bud":
		var hp: int = int(m.g["bud_hp"])
		var growth_stage := "sprout"
		if hp <= 7:
			growth_stage = "bud"
		if hp <= 3:
			growth_stage = "opening"
		_fairy_set_boss_stage(growth_stage)
		var bud: Node3D = m.g.get("bud")
		if bud != null and is_instance_valid(bud):
			var stage_scale: float = float(FS_BOSS_STAGE_SCALE[growth_stage])
			var pulse: float = 1.0 + sin(tt * 8.0) * 0.05
			bud.scale = Vector3.ONE * (stage_scale * pulse)
		m.hud_game.text = "Open the flower!   %d hits left   %s" % [maxi(0, hp), hearts_str]
		if hp <= 0:
			_fairy_bloom_start()
			m.show_msg(fr_name_safe(), "It's blooming! 🌸")
		elif pt <= 0.0:
			m.fs_fails += 1
			m.g["phase_t"] = FS_BUD_T + 6.0 * float(mini(m.fs_fails, 2))
			m.g["hearts"] = FS_HEARTS
			m.g["ring_cd"] = FS_RING_CD * 2.0
			_fairy_clear_orbs()
			m.player.visible = true
			m.show_msg(fr["fname"], "The fairy light made more time! Keep growing the flower!", "encourage")
		return
	if phase == "boss_bloom":
		m.g["bloom_t"] = float(m.g.get("bloom_t", 0.0)) - delta
		var f: float = clampf(1.0 - float(m.g["bloom_t"]) / FS_BLOOM_T, 0.0, 1.0)
		var center: Vector3 = m.g["boss_center"]
		var bloom_art: Node3D = m.g.get("boss_art")
		if bloom_art != null and is_instance_valid(bloom_art):
			var bloom_scale: float = float(FS_BOSS_STAGE_SCALE["bloom"])
			bloom_art.scale = Vector3.ONE * (bloom_scale * lerpf(0.72, 1.0, f))
		if fmod(tt, 0.18) < delta:
			m._sparkle_burst(center + Vector3(randf() * 16 - 8, 1.0, randf() * 16 - 8), Color.from_hsv(randf(), 0.4, 1.0))
		if float(m.g["bloom_t"]) <= 0.0:
			if not bool(m.g.get("player_acted", false)):
				m.g["bloom_t"] = 0.0
				if not bool(m.g.get("awaiting_cheer", false)):
					m.g["awaiting_cheer"] = true
					m.show_msg(fr["fname"], "Tap the sparkle or steer to cheer the flower awake!", "hint")
				return
			m.player.visible = true
			m.award_sticker("flower")
			# _end_game's medal hook reads m.fs_fails for the ranking, so the
			# retry-kindness counter resets AFTER the win is reported
			m._end_game(true, fr, "The Fairy Flower blossomed! You did it!")
			m.fs_fails = 0
		return
