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
# BOOM-OVER (NAVIGATION_AUDIT_2026-07-25 C2): before shortening the boom into
# Roshan's back, try lifting the lens over the obstacle. Most things behind
# her are waist-high furniture or a wall with open air above it, and looking
# down over the top keeps her whole body on screen. Only when no lift clears
# does the boom shorten — which is what used to happen on every heading in a
# 13-unit basement room, blinking her out of the frame at the same time.
const LIFTS: Array[float] = [4.0, 9.0]


# ---- venue profiles (NAVIGATION_AUDIT_2026-07-25 P0) ----
# The ONE definition of the chase lens per venue: boot value and every restore
# site read these, so the framing can no longer drift the way cam_high did
# (player.gd booted at 9.0 while three separate restores hand-typed 6.5, so the
# outdoor lens permanently dropped after the first castle visit).
#
# INTERIOR is 18/8, not the old hand-tuned 10/4.2. At the 38 deg diorama lens a
# 10-unit boom frames the 7.03u Roshan inside a 7.1u window - she filled 99% of
# the screen height indoors against 39% outdoors. That hand-tune existed only to
# stop wall clipping, which resolve() below has done analytically since the
# 2026-07-19 camera audit; 18/8 puts her back at ~55% and lets the resolver do
# its job. far is per-venue: the reef backdrop ring sits at r=340 (so ~610u
# across the world) and the northern strip spans its 430 dome twice, hence 1200
# outdoors; an enclosed castle needs nothing past its own 90u dome.
const OUTDOOR := {"back": 25.0, "high": 9.0, "fov": 38.0, "near": 0.3, "far": 1200.0}
const INTERIOR := {"back": 18.0, "high": 8.0, "fov": 38.0, "near": 0.3, "far": 500.0}


static func resolve(m: Node, focus: Vector3, want: Vector3) -> Vector3:
	# Clamp the boom focus->want so the camera stays out of walls, above the
	# ground and below interior ceilings. Cheap: one pass over arena_solids
	# plus two or three height-oracle samples.
	var boom: Vector3 = want - focus
	var length: float = boom.length()
	if length < 0.001:
		return want
	var t: float = boom_hit_t(m, focus, want)
	if t < 1.0:
		# BOOM-OVER before BOOM-IN: keep the full boom length and raise the lens
		# instead, if any lift in LIFTS clears the obstruction outright.
		# Capped by the ceiling of the band the ideal spot sits in — interior
		# roofs are not solids, so without this the lens would happily rise
		# through the floor of the room above and film its underside.
		var lift_cap: float = ceil_y(m, want) - want.y
		for lift in LIFTS:
			if lift > lift_cap:
				break
			var raised: Vector3 = want + Vector3(0.0, lift, 0.0)
			if boom_hit_t(m, focus, raised) >= 1.0:
				want = raised
				boom = want - focus
				length = boom.length()
				t = 1.0
				break
	var keep: float = length
	if t < 1.0:
		# when Roshan is cornered against a solid (t near 0) the boom
		# collapses toward her rather than ever placing the lens in the wall;
		# MIN_BOOM overshoot stays inside the solid's pad, never its mesh
		keep = clampf(t * length - SKIN, MIN_BOOM, length)
	var pos: Vector3 = focus + boom * (keep / length)
	# ceiling first, ground last: a zone stack can legitimately put the ceiling
	# right on top of the floor (zone_bounds collapses inversions rather than
	# pinning), and the lens must never end up buried under the floor.
	var cy: float = ceil_y(m, pos)
	if pos.y > cy:
		pos.y = cy
	# ground: sample under the camera AND mid-boom, so a ridge rising between
	# Roshan and the lens lifts the camera over it instead of burying it
	var gy: float = ground_y(m, pos)
	var mid: Vector3 = focus.lerp(pos, 0.55)
	gy = maxf(gy, ground_y(m, Vector3(mid.x, pos.y, mid.z)))
	if pos.y < gy:
		pos.y = gy
	return pos


static func boom_hit_t(m: Node, focus: Vector3, want: Vector3) -> float:
	# Fraction t in [0..1] along focus->want where the segment first enters an
	# arena solid; 1.0 when clear, 0.0 when the segment STARTS inside one.
	#
	# PAD RULE (castle-stairs bug, 2026-07-21): every solid is stored inflated
	# by its body-clearance pad — 1.6u of empty AIR around the real mesh. When
	# Roshan STANDS ON a solid (under-stair blocks, furniture, platforms) the
	# focus point sits inside that pad ring, and collapsing the boom there
	# glues the lens inside her body for the whole stair climb. So: a focus
	# inside the PADDED solid but outside its CORE re-tests entry against the
	# core — the lens may cross pad air but still never enters mesh. A focus
	# inside the CORE itself still collapses (the door-arch lesson: a plain
	# "ignore this solid" exemption lets the lens glide through real geometry).
	if not ("arena_solids" in m):
		return 1.0
	var t: float = 1.0
	var d: Vector3 = want - focus
	for s in m.arena_solids:
		var st: float
		var pad: float = float(s.get("pad", 0.0))
		if s.box:
			st = _seg_box_t(focus, d, s, 0.0)
			if st <= 0.0 and pad > 0.0:
				st = _seg_box_t(focus, d, s, pad)
		else:
			st = _seg_cyl_t(focus, d, s, 0.0)
			if st <= 0.0 and pad > 0.0:
				st = _seg_cyl_t(focus, d, s, pad)
		t = minf(t, st)
	return t


static func _seg_box_t(p: Vector3, d: Vector3, s: Dictionary, shrink: float = 0.0) -> float:
	# slab test against the AABB {cx±hx, y0..y1, cz±hz}: entry fraction,
	# 0.0 when starting inside, 1.0 on a miss. shrink deflates the box on all
	# sides (used to test a solid's CORE inside its stored pad inflation).
	var mins: Array = [float(s.cx) - float(s.hx) + shrink, float(s.y0) + shrink, float(s.cz) - float(s.hz) + shrink]
	var maxs: Array = [float(s.cx) + float(s.hx) - shrink, float(s.y1) - shrink, float(s.cz) + float(s.hz) - shrink]
	if float(mins[0]) >= float(maxs[0]) or float(mins[1]) >= float(maxs[1]) or float(mins[2]) >= float(maxs[2]):
		return 1.0   # pad bigger than the solid: no core to hit
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


static func _seg_cyl_t(p: Vector3, d: Vector3, s: Dictionary, shrink: float = 0.0) -> float:
	# vertical finite cylinder: side-surface roots in xz PLUS the flat caps
	# (a boom rising into an arch crown or fountain basin enters via a cap).
	# shrink deflates radius and caps (core-vs-pad test, see boom_hit_t).
	var ox: float = p.x - float(s.x)
	var oz: float = p.z - float(s.z)
	var r: float = float(s.r) - shrink
	var y0: float = float(s.y0) + shrink
	var y1: float = float(s.y1) - shrink
	if r <= 0.0 or y0 >= y1:
		return 1.0   # pad bigger than the solid: no core to hit
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


static func zone_bounds(m: Node, p: Vector3, base_floor: float, base_ceil: float) -> Vector2:
	# THE resolution of the y-banded m.arena_zones table, in world y.
	#
	# NAVIGATION_AUDIT_2026-07-25 C4: player.gd and this file each had their own
	# copy and they did not agree. The body applied zones IN ORDER (later entries
	# override earlier ones); the lens took maxf of every floor and minf of every
	# ceiling. The castle table has 17 deliberately overlapping entries, so
	# wherever two overlapped and the later one was not the highest, the camera
	# and the heroine stood on different floors. One function, the BODY's
	# semantics, both callers.
	var flr: float = base_floor
	var ceil_v: float = base_ceil
	if not ("arena_zones" in m):
		return Vector2(flr, ceil_v)
	var ap: Vector3 = m.arena_center
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
			flr = ap.y + float(zz["floor"])
		if zz.has("ramp"):
			# sloped stair floor: [axis (0=x, 2=z), p0, floor0, p1, floor1]
			var rp: Array = zz["ramp"]
			var pv: float = lx if int(rp[0]) == 0 else lz
			var rt: float = clampf((pv - float(rp[1])) / (float(rp[3]) - float(rp[1])), 0.0, 1.0)
			flr = ap.y + lerpf(float(rp[2]), float(rp[4]), rt)
		if zz.has("ceil"):
			ceil_v = ap.y + float(zz["ceil"])
	# NEVER PIN. Where an overlap leaves the floor above the ceiling (the
	# undercroft shaft mouth does this for about half a unit of z), the old code
	# clamped her UP to the floor and straight back DOWN to the ceiling with
	# vel.y forced to zero every frame - a sticky step you had to wriggle out of.
	# The floor wins: she stands on something, she is never trapped under it.
	if ceil_v < flr:
		ceil_v = flr
	return Vector2(flr, ceil_v)


static func ground_y(m: Node, p: Vector3) -> float:
	# Lowest y the camera may occupy at (p.x, p.z) — same zone resolution the
	# body uses, plus the lens's own floor clearance.
	if String(m.game) == "":
		return m.seabed_y(p.x, p.z) + FLOOR_OFF
	var ap: Vector3 = m.arena_center
	var base: float = ap.y + 1.5 - FLOOR_OFF
	if "lagoon_floor" in m and m.lagoon_floor:
		base = m.lagoon_walk_h(p.x, p.z)
	elif "northern_floor" in m and m.northern_floor:
		base = m.northern_walk_h(p.x, p.z)
	return zone_bounds(m, p, base, 1e9).x + FLOOR_OFF


static func ceil_y(m: Node, p: Vector3) -> float:
	# Highest y the camera may occupy — interior roofs are NOT solids (only
	# upright walls are), but every real interior already registers a "ceil"
	# zone for the player; the camera honours the same bands.
	# NOTE the base is 1e9, never m.arena_ceil: that one is a BODY clamp (it
	# keeps Roshan under the lowest interior ceiling, 31 in the castle) and would
	# bury the lens the moment she stepped onto the balcony deck at y 33.4.
	if String(m.game) == "":
		return 1e9
	return zone_bounds(m, p, -1e9, 1e9).y - CEIL_OFF
