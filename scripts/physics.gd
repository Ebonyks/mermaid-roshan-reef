class_name ReefPhysics
extends RefCounted
# ============================================================================
# ReefPhysics — the game's unified physics engine.
#
# Everything that moves under simulated forces (Roshan, the fetch ball, the
# melody orbs, falling dolls, the 2D trampoline, fairy bolts, the finger
# chains, the penguin-slide sled) runs through this one module instead of the
# nine hand-rolled integrators it replaced.
#
# Design constraints (see PHYSICS_ENGINE.md):
#  * pure static module — no nodes, no autoload, no per-frame allocations
#  * fixed-substep semi-implicit Euler so 3-4yo-phone frame hitches and the
#    probes' Engine.time_scale=6 produce the same trajectories
#  * media (WATER / AIR / LAND), not weights: a body crossing the water
#    surface changes rules (gravity, drag, control), which is what makes land
#    feel like land and water feel like water
#  * the collision model is the game's existing analytic one — heightfield
#    floor oracle, dome/radius bounds, cylinder+box soft solids — not
#    Godot physics bodies (too heavy for the target phones)
# ============================================================================

const SUB_DT := 1.0 / 60.0     # fixed integration substep
const MAX_SUBSTEPS := 12       # cap for huge frames / time_scale 6 probes

enum { ST_SWIM, ST_AIR, ST_GROUND }


# ---------------------------------------------------------------------------
# Medium — the rules of motion for a volume (water, air, dream-land).
# ---------------------------------------------------------------------------
class Medium:
	extends RefCounted
	var gravity := 13.0     # downward accel, u/s^2
	var drag := 0.18        # velocity fraction retained per second (exp form)
	var control := 1.0      # thrust authority multiplier
	var buoyancy := 0.0     # upward accel inside the surface band, u/s^2
	var buoy_band := 0.0    # depth below the surface where buoyancy acts

	func _init(g := 13.0, dr := 0.18, ctl := 1.0, buoy := 0.0, band := 0.0) -> void:
		gravity = g
		drag = dr
		control = ctl
		buoyancy = buoy
		buoy_band = band


# Presets. WATER matches the original hand-tuned swim feel exactly; AIR gives
# crisp ballistic breach arcs; LAND is the Sky-Lagoon "dream float" — real
# enough gravity to keep Roshan on the grass, soft enough for a 4yo to hop
# rivers and still reach every dream star.
static func water_medium() -> Medium:
	return Medium.new(13.0, 0.18, 1.0, 34.0, 4.5)

static func air_medium() -> Medium:
	return Medium.new(30.0, 0.90, 0.15, 0.0, 0.0)

static func land_medium() -> Medium:
	return Medium.new(20.0, 0.15, 1.0, 0.0, 0.0)

static func free_medium(g := 0.0) -> Medium:
	# projectiles / orbs: optional gravity, no drag, no control
	return Medium.new(g, 1.0, 0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# World — the analytic collision environment a body moves through.
# ---------------------------------------------------------------------------
class World:
	extends RefCounted
	var floor_fn := Callable()      # (x, z) -> ground height; unset = flat floor_y
	var floor_y := -INF             # flat floor when floor_fn is unset
	var floor_pad := 0.0            # body rest height above the ground oracle
	var ceil_y := INF
	var water_y := INF              # below = water medium, above = air medium
	var center := Vector3.ZERO      # for radial bounds
	var bound_r := 0.0              # XZ radial clamp around center (0 = off)
	var solids: Array = []          # cylinder/box dicts (main.gd registry format)

	func ground_at(x: float, z: float) -> float:
		if floor_fn.is_valid():
			return float(floor_fn.call(x, z)) + floor_pad
		return floor_y + floor_pad


# ---------------------------------------------------------------------------
# Body — a point body with a radius, moved by step().
# ---------------------------------------------------------------------------
class Body:
	extends RefCounted
	var pos := Vector3.ZERO
	var vel := Vector3.ZERO
	var node: Node3D = null         # optional: synced after step()
	var water: Medium
	var air: Medium
	var bounce := 0.0               # restitution vs floor / box bounds
	var ground_friction := 8.0      # extra horizontal damp/s when grounded, idle
	var box := AABB()               # optional reflect region (melody orbs); zero = off
	var state := ST_SWIM
	var on_floor := false
	var splashed := 0               # +1 = entered water this step, -1 = left it

	func _init(m_water: Medium = null, m_air: Medium = null) -> void:
		water = m_water
		air = m_air
		if water == null and m_air != null:
			water = m_air
		if air == null and water != null:
			air = water

	func medium_at(y: float, surface_y: float) -> Medium:
		return water if y < surface_y else air


# ---------------------------------------------------------------------------
# The integrator.
#   thrust  — desired acceleration (u/s^2), already directed; scaled by the
#             active medium's control authority
#   world   — may be null for free-flying bodies (projectiles); the body's
#             own reflect box still applies
#   returns — the body, for chaining
# ---------------------------------------------------------------------------
static func step(body: Body, world: World, thrust: Vector3, dt: float) -> Body:
	body.splashed = 0
	var remaining := dt
	var steps := 0
	while remaining > 0.0 and steps < MAX_SUBSTEPS:
		var h: float = minf(remaining, SUB_DT)
		remaining -= h
		steps += 1
		_substep(body, world, thrust, h)
	if remaining > 0.0:
		# huge frame: finish in one final gulp rather than lose time
		_substep(body, world, thrust, remaining)
	if body.node != null and is_instance_valid(body.node):
		body.node.position = body.pos
	return body


static func _substep(body: Body, world: World, thrust: Vector3, h: float) -> void:
	var surface_y: float = world.water_y if world != null else INF
	var was_water: bool = body.pos.y < surface_y
	var med: Medium = body.medium_at(body.pos.y, surface_y)
	# forces
	body.vel += thrust * med.control * h
	body.vel.y -= med.gravity * h
	if was_water and med.buoy_band > 0.0:
		var depth: float = surface_y - body.pos.y
		if depth < med.buoy_band:
			# lift grows with submergence (like real displacement), making the
			# surface band a STABLE shelf: bodies bob at the waterline instead
			# of sliding off it. Deeper than the band there is no lift at all,
			# so diving and the classic idle sink are untouched.
			body.vel.y += med.buoyancy * (depth / med.buoy_band) * h
	# drag (exponential — frame-rate independent by construction)
	body.vel *= pow(med.drag, h)
	if body.state == ST_GROUND and thrust.x == 0.0 and thrust.z == 0.0:
		var f: float = pow(0.001, h * body.ground_friction / 8.0)
		body.vel.x *= f
		body.vel.z *= f
	# integrate
	body.pos += body.vel * h
	# splash detection (crossing the surface either way)
	var is_water: bool = body.pos.y < surface_y
	if is_water != was_water:
		body.splashed = 1 if is_water else -1
	# resolve the world (free bodies still honor their own reflect box)
	if world != null:
		collide(body, world)
	elif body.box.size != Vector3.ZERO:
		body.on_floor = false
		_reflect_box(body)
	# classify state — water wins: resting on the seabed is still swimming;
	# grounded (with its friction and hop rules) only exists out of water
	if is_water:
		body.state = ST_SWIM
	elif body.on_floor:
		body.state = ST_GROUND
	else:
		body.state = ST_AIR


# ---------------------------------------------------------------------------
# Collision: floor/ceiling, radial bound, optional reflect box, soft solids.
# Same analytic model the game has always used, in one place.
# ---------------------------------------------------------------------------
static func collide(body: Body, world: World) -> void:
	body.on_floor = false
	var gy: float = world.ground_at(body.pos.x, body.pos.z)
	if gy > -1e17 and body.pos.y < gy:
		body.pos.y = gy
		if body.bounce > 0.0 and body.vel.y < -1.0:
			body.vel.y = -body.vel.y * body.bounce
		else:
			body.vel.y = maxf(0.0, body.vel.y)
			body.on_floor = true
	if body.pos.y > world.ceil_y:
		body.pos.y = world.ceil_y
		body.vel.y = minf(0.0, body.vel.y)
	if world.bound_r > 0.0:
		var dx: float = body.pos.x - world.center.x
		var dz: float = body.pos.z - world.center.z
		var d: float = Vector2(dx, dz).length()
		if d > world.bound_r:
			body.pos.x = world.center.x + dx * world.bound_r / d
			body.pos.z = world.center.z + dz * world.bound_r / d
	if body.box.size != Vector3.ZERO:
		_reflect_box(body)
	if not world.solids.is_empty():
		collide_solids(body.pos, body.vel, world.solids, body)


static func _reflect_box(body: Body) -> void:
	var lo: Vector3 = body.box.position
	var hi: Vector3 = body.box.end
	for ax in range(3):
		if body.pos[ax] < lo[ax]:
			body.pos[ax] = lo[ax]
			body.vel[ax] = absf(body.vel[ax]) * maxf(body.bounce, 0.01)
		elif body.pos[ax] > hi[ax]:
			body.pos[ax] = hi[ax]
			body.vel[ax] = -absf(body.vel[ax]) * maxf(body.bounce, 0.01)


# Soft-collision against the solids registry (cylinders + boxes): eject the
# body and cancel inward velocity so it slides along the face. This is the
# exact model player.gd pioneered, shared by every body now.
static func collide_solids(pos: Vector3, vel: Vector3, solids: Array, out: Body) -> void:
	for s in solids:
		if pos.y < float(s.y0) or pos.y > float(s.y1):
			continue
		if bool(s.get("box", false)):
			var lx: float = pos.x - float(s.cx)
			var lz: float = pos.z - float(s.cz)
			var hx: float = float(s.hx)
			var hz: float = float(s.hz)
			if absf(lx) < hx and absf(lz) < hz:
				if hx - absf(lx) < hz - absf(lz):
					var sgx: float = signf(lx) if lx != 0.0 else 1.0
					pos.x = float(s.cx) + sgx * hx
					if vel.x * sgx < 0.0:
						vel.x = 0.0
				else:
					var sgz: float = signf(lz) if lz != 0.0 else 1.0
					pos.z = float(s.cz) + sgz * hz
					if vel.z * sgz < 0.0:
						vel.z = 0.0
		else:
			var dx: float = pos.x - float(s.x)
			var dz: float = pos.z - float(s.z)
			var dd: float = sqrt(dx * dx + dz * dz)
			var r: float = float(s.r)
			if dd < r and dd > 0.001:
				var nx: float = dx / dd
				var nz: float = dz / dd
				pos.x = float(s.x) + nx * r
				pos.z = float(s.z) + nz * r
				var vn: float = vel.x * nx + vel.z * nz
				if vn < 0.0:
					vel.x -= vn * nx
					vel.z -= vn * nz
	out.pos = pos
	out.vel = vel


# ===========================================================================
# 2D bodies — the CanvasLayer minigames (dolls, trampoline) share the same
# integrator idea in UI pixels. +y is DOWN in canvas space.
# ===========================================================================
class Body2D:
	extends RefCounted
	var pos := Vector2.ZERO
	var vel := Vector2.ZERO
	var gravity := 0.0          # px/s^2, downward (+y)
	var drag := 1.0             # per-second retention
	var terminal := 1e9         # max fall speed, px/s
	var floor_y := INF          # canvas floor (rest line)
	var bounce := 0.0
	var on_floor := false


static func step2d(b: Body2D, thrust: Vector2, dt: float) -> Body2D:
	var remaining := dt
	var steps := 0
	while remaining > 0.0 and steps < MAX_SUBSTEPS:
		var h: float = minf(remaining, SUB_DT)
		remaining -= h
		steps += 1
		b.vel += thrust * h
		b.vel.y = minf(b.vel.y + b.gravity * h, b.terminal)
		b.vel *= pow(b.drag, h)
		b.pos += b.vel * h
		b.on_floor = false
		if b.pos.y > b.floor_y:
			b.pos.y = b.floor_y
			if b.bounce > 0.0 and b.vel.y > 60.0:
				b.vel.y = -b.vel.y * b.bounce
			else:
				b.vel.y = 0.0
				b.on_floor = true
	return b


# Impulse that reaches exactly `height` px above the floor under `gravity`.
static func jump_for_height(height: float, gravity: float) -> float:
	return -sqrt(maxf(0.0, 2.0 * gravity * height))


# ===========================================================================
# Shared motion helpers — the game's recurring idioms, frame-rate correct.
# ===========================================================================

# Exponential smoothing factor: fraction of remaining distance covered in dt.
# `base` is the fraction REMAINING after 1 second (like pow(0.001, delta)).
static func smooth(base: float, dt: float) -> float:
	return 1.0 - pow(base, dt)


# Magnet-assist: pull `pos` toward `target` when within `radius`, stronger as
# it gets closer. `strength` matches the old lerp(delta*k*(1-d/R)) tuning but
# in the exponential (frame-rate independent) form.
static func magnet(pos: Vector3, target: Vector3, radius: float, strength: float, dt: float) -> Vector3:
	var d: float = pos.distance_to(target)
	if d >= radius or d <= 0.0001:
		return pos
	var f: float = 1.0 - exp(-strength * (1.0 - d / radius) * dt)
	return pos.lerp(target, minf(f, 0.95))


# Constant-speed seek on the ground plane (Chuck fetching the ball).
static func toward_xz(pos: Vector3, target: Vector3, speed: float, dt: float) -> Vector3:
	var d := target - pos
	d.y = 0.0
	var l := d.length()
	if l < 0.0001:
		return pos
	return pos + d / l * minf(speed * dt, l)


# Damped angular spring for hanging things (finger-curtain chains).
# state is a Dictionary with "ang": Vector2 and "vel": Vector2, mutated.
static func spring2(state: Dictionary, stiffness: float, damping: float, dt: float) -> void:
	var ang: Vector2 = state["ang"]
	var vel: Vector2 = state["vel"]
	vel += (-ang * stiffness - vel * damping) * dt
	ang += vel * dt
	if ang.length() > 1.0:
		ang = ang.normalized()
	state["ang"] = ang
	state["vel"] = vel


# Along-track sled physics (penguin slide): gravity component along the
# grade accelerates, linear friction caps speed.
static func track_speed(v: float, grade: float, grav: float, frict: float, vmin: float, vmax: float, dt: float) -> float:
	v += (grav * grade - frict * v) * dt
	return clampf(v, vmin, vmax)


# Lateral steering with exponential damping (slide / rail-shooter strafing).
static func lateral(vx: float, steer_accel: float, damp_base: float, dt: float) -> float:
	vx += steer_accel * dt
	return vx * pow(damp_base, dt)
