class_name ReefFlow
extends RefCounted
# E4 currents (ZELDA_GAMEPLAY_WORKORDER): authored flow fields in the reef —
# a two-segment stream ride across the north side and a geyser lift that
# pops her through the surface (pairs with the Gen-1 breach). Analytic:
# player._process queries accel_at() each frame; the bubble columns are the
# non-reader pointer. The geyser breathes ON 6s / OFF 4s so nothing — child
# or probe bot — can ever be pinned in the lift column.

const STREAMS := [
	{"a": Vector3(-40.0, 20.0, -35.0), "b": Vector3(20.0, 24.0, -70.0), "r": 7.0, "s": 30.0},
	{"a": Vector3(20.0, 24.0, -70.0), "b": Vector3(70.0, 30.0, -40.0), "r": 7.0, "s": 30.0},
]
const GEYSER := {"x": -52.0, "z": 8.0, "r": 5.5, "y1": 56.0, "s": 55.0}
const GEYSER_ON := 6.0
const GEYSER_CYCLE := 10.0

var m: ReefMain
var geyser_parts: CPUParticles3D = null

func _init(main: ReefMain) -> void:
	m = main
	for st in STREAMS:
		_bubbles(st["a"], st["b"], float(st["r"]), float(st["s"]))
	var gx: float = float(GEYSER["x"])
	var gz: float = float(GEYSER["z"])
	var base_y: float = ReefMain.seabed_y(gx, gz)
	geyser_parts = _bubbles(Vector3(gx, base_y + 1.0, gz),
		Vector3(gx, float(GEYSER["y1"]), gz), float(GEYSER["r"]) * 0.8, float(GEYSER["s"]))
	m._halo(Vector3(gx, base_y + 0.6, gz), Color(0.6, 0.95, 1.0), 10.0)

func geyser_on() -> bool:
	return fmod(Time.get_ticks_msec() / 1000.0, GEYSER_CYCLE) < GEYSER_ON

func tick(_delta: float, _ppos: Vector3) -> void:
	# the geyser breathes: bubbles only while the lift is blowing
	if geyser_parts != null:
		geyser_parts.emitting = geyser_on()

func accel_at(p: Vector3) -> Vector3:
	var acc := Vector3.ZERO
	for st in STREAMS:
		var a: Vector3 = st["a"]
		var ab: Vector3 = (st["b"] as Vector3) - a
		var t: float = clampf((p - a).dot(ab) / ab.length_squared(), 0.0, 1.0)
		var d: float = (p - (a + ab * t)).length()
		var r: float = float(st["r"])
		if d < r:
			acc += ab.normalized() * float(st["s"]) * (1.0 - d / r)
	if geyser_on():
		var gx: float = float(GEYSER["x"])
		var gz: float = float(GEYSER["z"])
		var gd: float = Vector2(p.x - gx, p.z - gz).length()
		var gr: float = float(GEYSER["r"])
		if gd < gr and p.y < float(GEYSER["y1"]):
			# lift plus a gentle centering pull so the ride holds together
			acc += Vector3((gx - p.x) * 0.6,
				float(GEYSER["s"]) * (1.0 - gd / gr), (gz - p.z) * 0.6)
	return acc

func _bubbles(a: Vector3, b: Vector3, r: float, spd: float) -> CPUParticles3D:
	var e := CPUParticles3D.new()
	var seg: Vector3 = b - a
	e.amount = 40
	e.lifetime = maxf(seg.length() / (spd * 0.5), 0.8)
	e.local_coords = false
	e.emission_shape = CPUParticles3D.EMISSION_SHAPE_SPHERE
	e.emission_sphere_radius = r * 0.7
	e.direction = seg.normalized()
	e.spread = 6.0
	e.gravity = Vector3.ZERO
	e.initial_velocity_min = spd * 0.4
	e.initial_velocity_max = spd * 0.55
	e.scale_amount_min = 0.14
	e.scale_amount_max = 0.4
	var sm := SphereMesh.new()
	sm.radius = 0.22
	sm.height = 0.44
	e.mesh = sm
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
	mat.albedo_color = Color(0.62, 0.9, 1.0, 0.5)
	e.material_override = mat
	e.position = a
	m.add_child(e)
	return e
