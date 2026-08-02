class_name FxWater
extends RefCounted
# Shared water-FX vocabulary (WATER_PHYSICS_EVALUATION_2026-08-02.md): every
# water system procs the same small set of splash/ripple/bubble cards so a
# splash in the reef, a river crossing in the lagoon, the fetch lake and the
# promenade prop fleet all read as ONE game. Physics decides WHEN (discrete
# events: surface crossings, wet/dry flips, waterline hits); this module
# decides WHAT IT LOOKS LIKE. Ambient channels (the swell, sleeping-prop
# sway, toon-water shimmer) never proc a card — a card means something
# happened; probe_passive asserts zero cards under zero input.
#
# Visuals are two-track. When a Codex atlas exists
# (assets/sprites/fx_water/fx_water_<kind>_atlas.png, fixed-pivot grids per
# CODEX_WATER_FX_WORKORDER_2026-08-02.md) the card flipbooks it at the
# castle-interaction frame timings. Until that art lands, the card draws a
# styled procedural stand-in — expanding foam ring + soft burst + sparkles,
# the exact idiom of _spawn_surf_ring/_sparkle_burst, in the shared
# toon-water palette — so the placeholder already looks like Mermaid Roshan
# rather than dev art, and the Codex drop-in changes no call site.
#
# Phase 7 satellite: logic only, receives main by reference; the card list,
# counters and cooldowns are main member vars (NOT m.g — m.g is per-game
# scratch and resets on every _start_game, which would orphan live cards).

const CAP := 6                  # concurrent cards; oldest evicted (perf contract)
const COOL := 0.5               # per-emitter proc cooldown, seconds
const TIER_MEDIUM := 8.0        # crossing energy (u/s): below = small plink
const TIER_BREACH := 14.0       # at/above = the full breach burst
# the shared toon-water family (Phase 5 water mats, castle bubble atlases):
# every card draws only from these — this is the continuity contract
const COL_DEEP := Color(0.2, 0.55, 0.8)
const COL_LIGHT := Color(0.5, 0.82, 0.9)
const COL_FOAM := Color(0.85, 0.97, 1.0)

# kind -> [atlas hframes, vframes, frames used, seconds/frame, world size]
const KINDS := {
	"splash_small": [4, 2, 8, 0.08, 2.6],
	"splash_medium": [3, 3, 8, 0.10, 4.6],
	"splash_breach": [3, 3, 8, 0.11, 7.5],
	"ripple_ring": [4, 2, 8, 0.12, 5.0],
	"bubble_burst": [4, 2, 8, 0.10, 3.2],
}

var m: ReefMain
var _tex_cache := {}            # procedural gradient textures, one per shape

func _init(main: ReefMain) -> void:
	m = main

func splash(pos: Vector3, energy: float, emitter: String = "", cfg: Dictionary = {}) -> void:
	# The one proc point every water system calls: energy (speed of the
	# crossing, u/s) picks the tier so the same event always looks the same
	# size, and the per-emitter cooldown keeps a body bobbing at the
	# waterline reading as a bob, not a machine-gun splash.
	if float(m.fxw_cool.get(emitter, 0.0)) > 0.0:
		return
	m.fxw_cool[emitter] = COOL
	var kind := "splash_small"
	if energy >= TIER_BREACH:
		kind = "splash_breach"
	elif energy >= TIER_MEDIUM:
		kind = "splash_medium"
	card(kind, pos, cfg)
	if bool(cfg.get("ripple", true)):
		card("ripple_ring", pos, cfg)

func card(kind: String, pos: Vector3, cfg: Dictionary = {}) -> Node3D:
	# Spawn one effect card at a real world position/depth (so the depth
	# buffer sorts it against standees and Roshan like everything else in
	# the 2.5D world). Returns the holder node, or null on an unknown kind.
	if not KINDS.has(kind):
		return null
	var kd: Array = KINDS[kind]
	var parent: Node3D = cfg.get("parent", m)
	if parent == null or not is_instance_valid(parent):
		return null
	while m.fxw_cards.size() >= CAP:
		var old: Dictionary = m.fxw_cards.pop_front()
		var on: Node3D = old.get("node")
		if on != null and is_instance_valid(on):
			on.queue_free()
	var size: float = float(kd[4]) * float(cfg.get("scale", 1.0))
	var holder := Node3D.new()
	holder.position = pos
	parent.add_child(holder)
	var entry := {"node": holder, "kind": kind, "t": 0.0,
		"dur": float(kd[2]) * float(kd[3]), "frames": int(kd[2]),
		"size": size, "sprite": null, "ring": null, "ring_mat": null,
		"burst": null, "burst_mat": null}
	var atlas_path: String = "res://assets/sprites/fx_water/fx_water_" + kind + "_atlas.png"
	if ResourceLoader.exists(atlas_path):
		var spr := Sprite3D.new()
		var tex: Texture2D = load(atlas_path)
		spr.texture = tex
		spr.hframes = int(kd[0])
		spr.vframes = int(kd[1])
		spr.frame = 0
		spr.shaded = false
		spr.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		var fw: float = float(tex.get_width()) / float(kd[0])
		spr.pixel_size = size / maxf(fw, 1.0)
		if kind == "ripple_ring":
			spr.rotation_degrees.x = -90.0   # lies flat on the water surface
		else:
			spr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		holder.add_child(spr)
		entry["sprite"] = spr
	else:
		_placeholder(holder, entry, kind, size)
	m.fxw_cards.append(entry)
	m.fxw_total += 1
	if bool(cfg.get("sound", kind.begins_with("splash"))):
		_plink(kind)
	if kind == "splash_medium" or kind == "splash_breach":
		# thrown droplets: the game's existing sparkle idiom, water-tinted
		m._sparkle_burst(pos + Vector3(0, 1.2, 0), COL_LIGHT)
	return holder

func tick(delta: float) -> void:
	for k in m.fxw_cool.keys():
		m.fxw_cool[k] = maxf(0.0, float(m.fxw_cool[k]) - delta)
	if m.fxw_cards.is_empty():
		return
	var alive: Array = []
	for c_v in m.fxw_cards:
		var c: Dictionary = c_v
		var n: Node3D = c["node"]
		if n == null or not is_instance_valid(n):
			continue
		c["t"] = float(c["t"]) + delta
		var p: float = clampf(float(c["t"]) / float(c["dur"]), 0.0, 1.0)
		var spr: Sprite3D = c["sprite"]
		if spr != null and is_instance_valid(spr):
			spr.frame = mini(int(p * float(c["frames"])), int(c["frames"]) - 1)
		else:
			_placeholder_tick(c, p, delta)
		if float(c["t"]) >= float(c["dur"]):
			n.queue_free()
		else:
			alive.append(c)
	m.fxw_cards = alive

# ---- procedural stand-in (until the Codex atlases land) --------------------

func _placeholder(holder: Node3D, entry: Dictionary, kind: String, size: float) -> void:
	# foam ring lying on the surface — the _spawn_surf_ring silhouette
	var ring := MeshInstance3D.new()
	var rq := QuadMesh.new()
	rq.size = Vector2(1.0, 1.0)
	ring.mesh = rq
	ring.rotation_degrees.x = -90.0
	var rm := StandardMaterial3D.new()
	rm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	rm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	rm.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	rm.albedo_texture = _shape_tex("ring")
	rm.albedo_color = COL_FOAM
	ring.material_override = rm
	ring.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	holder.add_child(ring)
	entry["ring"] = ring
	entry["ring_mat"] = rm
	if kind != "ripple_ring":
		# soft foam burst above the ring — billboard, pops then fades
		var burst := MeshInstance3D.new()
		var bq := QuadMesh.new()
		bq.size = Vector2(1.0, 1.0)
		burst.mesh = bq
		var bm := StandardMaterial3D.new()
		bm.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		bm.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		bm.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		bm.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
		bm.albedo_texture = _shape_tex("burst")
		bm.albedo_color = COL_LIGHT if kind == "bubble_burst" else COL_FOAM
		burst.material_override = bm
		burst.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		burst.position = Vector3(0, size * 0.22, 0)
		holder.add_child(burst)
		entry["burst"] = burst
		entry["burst_mat"] = bm
	var s0: float = size * 0.3
	holder.scale = Vector3(s0, s0, s0)

func _placeholder_tick(c: Dictionary, p: float, delta: float) -> void:
	var size: float = float(c["size"])
	var ring: MeshInstance3D = c["ring"]
	if ring != null and is_instance_valid(ring):
		var rs: float = size * (0.3 + 1.15 * p)
		ring.scale = Vector3(rs, rs, rs)
		(c["ring_mat"] as StandardMaterial3D).albedo_color = Color(
			COL_FOAM.r, COL_FOAM.g, COL_FOAM.b, 0.85 * (1.0 - p))
	var burst: MeshInstance3D = c["burst"]
	if burst != null and is_instance_valid(burst):
		var bs: float = size * 0.62 * (0.4 + 0.9 * minf(p * 2.4, 1.0))
		burst.scale = Vector3(bs, bs, bs)
		var bcol: Color = (c["burst_mat"] as StandardMaterial3D).albedo_color
		bcol.a = 0.9 * pow(1.0 - p, 1.3)
		(c["burst_mat"] as StandardMaterial3D).albedo_color = bcol
		if String(c["kind"]) == "bubble_burst":
			burst.position.y += delta * 1.4   # bubbles drift up before they pop

func _shape_tex(shape: String) -> GradientTexture2D:
	if _tex_cache.has(shape):
		return _tex_cache[shape]
	var gt := GradientTexture2D.new()
	gt.width = 128
	gt.height = 128
	gt.fill = GradientTexture2D.FILL_RADIAL
	gt.fill_from = Vector2(0.5, 0.5)
	gt.fill_to = Vector2(0.5, 0.0)
	var gr := Gradient.new()
	if shape == "ring":
		# hollow foam ring: clear middle, bright rim, soft outside
		gr.offsets = PackedFloat32Array([0.0, 0.55, 0.74, 0.86, 1.0])
		gr.colors = PackedColorArray([
			Color(1, 1, 1, 0.0), Color(1, 1, 1, 0.0), Color(1, 1, 1, 0.9),
			Color(1, 1, 1, 0.35), Color(1, 1, 1, 0.0)])
	else:
		# soft foam puff: bright core fading out
		gr.offsets = PackedFloat32Array([0.0, 0.35, 1.0])
		gr.colors = PackedColorArray([
			Color(1, 1, 1, 0.95), Color(1, 1, 1, 0.5), Color(1, 1, 1, 0.0)])
	gt.gradient = gr
	_tex_cache[shape] = gt
	return gt

func _plink(kind: String) -> void:
	# every proc pairs with the castle bubble-water family — same coupling
	# the room atlases enforce; tier only changes the pitch
	var stream: AudioStream = load("res://assets/audio/castle/bubble_water.ogg")
	if stream == null:
		return
	var sp := AudioStreamPlayer.new()
	sp.stream = stream
	sp.volume_db = -8.0
	sp.pitch_scale = 1.35 if kind == "splash_small" else (0.85 if kind == "splash_breach" else 1.05)
	m.add_child(sp)
	sp.play()
	sp.finished.connect(sp.queue_free)
