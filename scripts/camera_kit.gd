class_name CameraKit
extends RefCounted
# Shared camera helpers — Phase 0 of CAMERA_AUDIT_2026_07.md.
#
# This world has (almost) no physics bodies: collision is ANALYTIC — the
# m.arena_solids box/cylinder dicts built by main._wall_solid plus the
# per-venue walk-height oracles (northern_walk_h / lagoon_walk_h / seabed_y)
# and the m.arena_zones floor/ramp/ceil bands. A SpringArm3D or physics ray
# would hit nothing, so the camera resolves occlusion against that same
# analytic data. Guarantee: a position returned by resolve() is never inside
# a registered solid, never under the walk floor, never above a zone ceiling.
#
# Contract for callers (player.gd chase cam):
#   var want := CameraKit.resolve(m, focus, target)   # ideal, non-clipping
#   var glide := cam.position.lerp(want, k)           # smooth toward it
#   cam.position = CameraKit.resolve(m, focus, glide) # snap IN instantly if
#                                                     # the glide would clip
# Shorten-instantly / relax-out-smoothly falls out of resolving twice.

const SKIN := 0.5      # keep the lens this far in front of a hit surface
const MIN_BOOM := 0.15 # cornered: pull nearly first-person rather than clip
const FLOOR_OFF := 1.2 # lens height above the walk floor / seabed
const CEIL_OFF := 1.0  # lens clearance under a zone ceiling


static func resolve(m: Node, focus: Vector3, want: Vector3) -> Vector3:
	# Clamp the boom focus->want so the camera stays out of walls, above the
	# ground and below interior ceilings. Cheap: one pass over arena_solids
	# plus two or three height-oracle samples.
	var boom: Vector3 = want - focus
	var length: float = boom.length()
	if length < 0.001:
		return want
	var t: float = boom_hit_t(m, focus, want)
	var keep: float = length
	if t < 1.0:
		# when Roshan is cornered against a solid (t near 0) the boom
		# collapses toward her rather than ever placing the lens in the wall;
		# MIN_BOOM overshoot stays inside the solid's pad, never its mesh
		keep = clampf(t * length - SKIN, MIN_BOOM, length)
	var pos: Vector3 = focus + boom * (keep / length)
	# ground: sample under the camera AND mid-boom, so a ridge rising between
	# Roshan and the lens lifts the camera over it instead of burying it
	var gy: float = ground_y(m, pos)
	var mid: Vector3 = focus.lerp(pos, 0.55)
	gy = maxf(gy, ground_y(m, Vector3(mid.x, pos.y, mid.z)))
	if pos.y < gy:
		pos.y = gy
	var cy: float = ceil_y(m, pos)
	if pos.y > cy:
		pos.y = cy
	return pos


static func boom_hit_t(m: Node, focus: Vector3, want: Vector3) -> float:
	# Fraction t in [0..1] along focus->want where the segment first enters an
	# arena solid; 1.0 when clear, 0.0 when the segment STARTS inside one
	# (Roshan pressed into a solid's pad ring — the boom collapses to her).
	if not ("arena_solids" in m):
		return 1.0
	var t: float = 1.0
	var d: Vector3 = want - focus
	for s in m.arena_solids:
		if s.box:
			t = minf(t, _seg_box_t(focus, d, s))
		else:
			t = minf(t, _seg_cyl_t(focus, d, s))
	return t


static func _seg_box_t(p: Vector3, d: Vector3, s: Dictionary) -> float:
	# slab test against the AABB {cx±hx, y0..y1, cz±hz}: entry fraction,
	# 0.0 when starting inside, 1.0 on a miss
	var mins: Array = [float(s.cx) - float(s.hx), float(s.y0), float(s.cz) - float(s.hz)]
	var maxs: Array = [float(s.cx) + float(s.hx), float(s.y1), float(s.cz) + float(s.hz)]
	var tmin: float = -1e9
	var tmax: float = 1e9
	for ax in range(3):
		var pa: float = p[ax]
		var da: float = d[ax]
		var lo: float = mins[ax]
		var hi: float = maxs[ax]
		if absf(da) < 0.0001:
			if pa < lo or pa > hi:
				return 1.0
			continue
		var t1: float = (lo - pa) / da
		var t2: float = (hi - pa) / da
		if t1 > t2:
			var tmp: float = t1
			t1 = t2
			t2 = tmp
		tmin = maxf(tmin, t1)
		tmax = minf(tmax, t2)
		if tmin > tmax:
			return 1.0
	if tmax <= 0.0 or tmin >= 1.0:
		return 1.0   # solid lies entirely behind or beyond the boom
	if tmin <= 0.0:
		return 0.0   # boom starts inside — collapse
	return tmin


static func _seg_cyl_t(p: Vector3, d: Vector3, s: Dictionary) -> float:
	# vertical finite cylinder: side-surface roots in xz PLUS the flat caps
	# (a boom rising into an arch crown or fountain basin enters via a cap).
	var ox: float = p.x - float(s.x)
	var oz: float = p.z - float(s.z)
	var r: float = float(s.r)
	var y0: float = float(s.y0)
	var y1: float = float(s.y1)
	var in_xz: bool = ox * ox + oz * oz < r * r
	if in_xz and p.y > y0 and p.y < y1:
		return 0.0   # boom starts inside — collapse
	var best: float = 1.0
	var a: float = d.x * d.x + d.z * d.z
	if a > 0.000001:
		var b: float = 2.0 * (ox * d.x + oz * d.z)
		var c: float = ox * ox + oz * oz - r * r
		var disc: float = b * b - 4.0 * a * c
		if disc >= 0.0:
			var t1: float = (-b - sqrt(disc)) / (2.0 * a)
			if t1 > 0.0 and t1 < best:
				var hit_y: float = p.y + d.y * t1
				if hit_y > y0 and hit_y < y1:
					best = t1
	if absf(d.y) > 0.0001:
		for yc in [y0, y1]:
			var tc: float = (yc - p.y) / d.y
			if tc > 0.0 and tc < best:
				var hx: float = ox + d.x * tc
				var hz: float = oz + d.z * tc
				if hx * hx + hz * hz < r * r:
					best = tc
	return best


static func ground_y(m: Node, p: Vector3) -> float:
	# Lowest y the camera may occupy at (p.x, p.z) — mirrors the player floor
	# logic (player.gd walk/zone block) so lens and heroine agree on the world.
	if String(m.game) == "":
		return m.seabed_y(p.x, p.z) + FLOOR_OFF
	var ap: Vector3 = m.arena_center
	var gy: float = ap.y + 1.5
	if "lagoon_floor" in m and m.lagoon_floor:
		gy = m.lagoon_walk_h(p.x, p.z) + FLOOR_OFF
	elif "northern_floor" in m and m.northern_floor:
		gy = m.northern_walk_h(p.x, p.z) + FLOOR_OFF
	if "arena_zones" in m:
		var lx: float = p.x - ap.x
		var lz: float = p.z - ap.z
		var ly: float = p.y - ap.y
		for zz in m.arena_zones:
			if not (zz["rect"] as Rect2).has_point(Vector2(lx, lz)):
				continue
			var band: Vector2 = zz.get("band", Vector2(-1e6, 1e6))
			if ly < band.x or ly > band.y:
				continue
			if zz.has("floor"):
				gy = maxf(gy, ap.y + float(zz["floor"]) + FLOOR_OFF)
			if zz.has("ramp"):
				var rp: Array = zz["ramp"]
				var pv: float = lx if int(rp[0]) == 0 else lz
				var rt: float = clampf((pv - float(rp[1])) / (float(rp[3]) - float(rp[1])), 0.0, 1.0)
				gy = maxf(gy, ap.y + lerpf(float(rp[2]), float(rp[4]), rt) + FLOOR_OFF)
	return gy


static func ceil_y(m: Node, p: Vector3) -> float:
	# Highest y the camera may occupy — interior roofs are NOT solids (only
	# upright walls are), but every real interior already registers a "ceil"
	# zone for the player; the camera honours the same bands.
	if String(m.game) == "" or not ("arena_zones" in m):
		return 1e9
	var ap: Vector3 = m.arena_center
	var cy: float = 1e9
	var lx: float = p.x - ap.x
	var lz: float = p.z - ap.z
	var ly: float = p.y - ap.y
	for zz in m.arena_zones:
		if not zz.has("ceil"):
			continue
		if not (zz["rect"] as Rect2).has_point(Vector2(lx, lz)):
			continue
		var band: Vector2 = zz.get("band", Vector2(-1e6, 1e6))
		if ly < band.x or ly > band.y:
			continue
		cy = minf(cy, ap.y + float(zz["ceil"]) - CEIL_OFF)
	return cy
