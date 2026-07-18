class_name ReefDistricts
extends RefCounted

# Authored composition for the open undersea world. Gameplay state remains on
# ReefMain; this satellite only chooses terrain shapes, scenery and dressing.

const GROVES := [
	{"p": Vector2(45, 27), "kind": "pearl"},
	{"p": Vector2(30, 52), "kind": "pearl"},
	{"p": Vector2(-28, 128), "kind": "kelp"},
	{"p": Vector2(-55, 165), "kind": "kelp"},
	{"p": Vector2(-12, 194), "kind": "kelp"},
	{"p": Vector2(-130, 110), "kind": "wreck"},
	{"p": Vector2(-160, 135), "kind": "wreck"},
	{"p": Vector2(-185, 155), "kind": "wreck"},
	{"p": Vector2(-130, 8), "kind": "moon"},
	{"p": Vector2(-178, -7), "kind": "moon"},
	{"p": Vector2(-25, -125), "kind": "rainbow"},
	{"p": Vector2(-48, -180), "kind": "rainbow"},
	{"p": Vector2(95, -78), "kind": "ice"},
	{"p": Vector2(150, -125), "kind": "ice"},
]

const REGION_CENTERS := {
	"pearl": Vector2(35, 30),
	"kelp": Vector2(-35, 165),
	"wreck": Vector2(-160, 135),
	"moon": Vector2(-165, 5),
	"rainbow": Vector2(-40, -165),
	"ice": Vector2(140, -115),
}

# Friend order matches ReefMain.FRIEND_DEFS. Friends sit at readable gateways;
# the dense scenic body of each district begins farther out behind them.
const FRIEND_POSITIONS := [
	Vector2(45, 32),
	Vector2(-22, 88),
	Vector2(-72, 8),
	Vector2(-26, -76),
	Vector2(70, -58),
]

const REGIONAL_SCENES := {
	"wreck_shoulders": "res://assets/reef_regions/wreck_ravine_shoulders.glb",
	"kelp_arch": "res://assets/reef_regions/kelp_cathedral_arch.glb",
	"kelp_lanterns": "res://assets/reef_regions/kelp_lantern_cluster.glb",
	"moon_arch": "res://assets/reef_regions/moon_shell_arch.glb",
	"moon_totem": "res://assets/reef_regions/moon_pearl_totem.glb",
	"ice_crystals": "res://assets/reef_regions/ice_crystal_cluster.glb",
	"ice_current": "res://assets/reef_regions/ice_current_fan.glb",
}

# The audit vocabulary for each district. Every region has at least three
# object families with a role beyond recolouring the same coral or rock.
const REGION_SIGNATURES := {
	"pearl": ["shell gardens", "barrel sponges", "pearl-shop ship"],
	"kelp": ["living kelp threshold", "hanging lantern pods", "tall kelp aisles"],
	"wreck": ["broken ship", "treasure debris", "ravine shoulders"],
	"moon": ["eroded shell arch", "pearl shell nest", "anemone bowl"],
	"rainbow": ["race gateway", "coral bouquets", "starfish flats"],
	"ice": ["brinicle hummocks", "frozen current sheets", "penguin floe"],
}

var m: ReefMain
var _scatter_rng := RandomNumberGenerator.new()

func _init(reef_main: ReefMain) -> void:
	m = reef_main
	_scatter_rng.seed = 0x52454546

static func _soft_disc(p: Vector2, center: Vector2, radius: float) -> float:
	var t: float = clampf(1.0 - p.distance_to(center) / radius, 0.0, 1.0)
	return t * t * (3.0 - 2.0 * t)

static func _segment_mask(p: Vector2, a: Vector2, b: Vector2, width: float) -> float:
	var ab: Vector2 = b - a
	var den: float = maxf(ab.length_squared(), 0.001)
	var t: float = clampf((p - a).dot(ab) / den, 0.0, 1.0)
	return _soft_disc(p, a.lerp(b, t), width)

static func shape_terrain(x: float, z: float, base_h: float) -> float:
	var p := Vector2(x, z)
	var h := base_h
	# A calm, readable hub and an open racing flat interrupt the noisy FBM.
	h = lerpf(h, -1.5, _soft_disc(p, Vector2.ZERO, 48.0) * 0.72)
	# Faron's nursery gateway is deliberately flat and free of the Moon bowl.
	h = lerpf(h, -2.0, _soft_disc(p, FRIEND_POSITIONS[2], 30.0) * 0.88)
	h = lerpf(h, -3.0, _soft_disc(p, Vector2(-5, -95), 42.0) * 0.72)
	h = lerpf(h, -4.0, _soft_disc(p, REGION_CENTERS["rainbow"], 52.0) * 0.58)
	# The wreck sits in a real diagonal ravine with raised shoulders.
	var trench: float = _segment_mask(p, Vector2(-190, 160), Vector2(-110, 95), 23.0)
	var shoulders: float = _segment_mask(p, Vector2(-190, 160), Vector2(-110, 95), 46.0) - trench
	h -= trench * 12.0
	h += maxf(shoulders, 0.0) * 9.0
	# A quiet bowl and broken ring give the moon grotto enclosure.
	var moon_inner: float = _soft_disc(p, REGION_CENTERS["moon"], 38.0)
	var moon_outer: float = _soft_disc(p, REGION_CENTERS["moon"], 66.0)
	h -= moon_inner * 8.0
	h += maxf(moon_outer - moon_inner, 0.0) * 17.0
	# Long ridges behind the kelp district make its vertical skyline legible.
	h += _segment_mask(p, Vector2(-78, 145), Vector2(-82, 220), 22.0) * 12.0
	h += _segment_mask(p, Vector2(12, 145), Vector2(5, 215), 19.0) * 9.0
	return h

static func region_at(p: Vector2) -> String:
	if p.length() < 55.0:
		return "pearl"
	var best := "pearl"
	var best_d := INF
	for key: String in REGION_CENTERS:
		var d: float = p.distance_squared_to(REGION_CENTERS[key])
		if d < best_d:
			best_d = d
			best = key
	return best

static func friend_position(index: int) -> Vector2:
	return FRIEND_POSITIONS[clampi(index, 0, FRIEND_POSITIONS.size() - 1)]

static func minimum_center_separation() -> float:
	var keys: Array = REGION_CENTERS.keys()
	var best: float = INF
	for i in range(keys.size()):
		for j in range(i + 1, keys.size()):
			var center_a: Vector2 = REGION_CENTERS[keys[i]]
			var center_b: Vector2 = REGION_CENTERS[keys[j]]
			best = minf(best, center_a.distance_to(center_b))
	return best

func seed_cluster_centers() -> void:
	m.cluster_centers.clear()
	for entry: Dictionary in GROVES:
		var p: Vector2 = entry["p"]
		m.cluster_centers.append(Vector3(p.x, m.seabed_y(p.x, p.y), p.y))

func grove_kind(index: int) -> String:
	return String((GROVES[index] as Dictionary)["kind"])

static func habitat_point_allowed(habitat: String, p: Vector2) -> bool:
	# Scatter is bounded to the playable seabed and kept away from the calm hub,
	# friend gateways and the rainbow portal's approach lane.
	if p.length() < 28.0 or p.length() > 252.0:
		return false
	for friend_pos: Vector2 in FRIEND_POSITIONS:
		if p.distance_to(friend_pos) < 12.0:
			return false
	if p.distance_to(Vector2(-5.0, -95.0)) < 18.0:
		return false
	var region: String = region_at(p)
	match habitat:
		"kelp", "anemone", "pearl", "wreck", "moon", "rainbow", "ice":
			var expected: String = "moon" if habitat == "anemone" else habitat
			return region == expected
		"starfish":
			return region == "pearl" or region == "rainbow"
		"urchin":
			return region == "wreck" or region == "moon"
		_:
			return true

func scatter_point(habitat: String) -> Vector3:
	var choices: Array[Vector2] = []
	match habitat:
		"kelp":
			choices = [Vector2(-28, 145), Vector2(-55, 178), Vector2(-10, 202)]
		"anemone":
			choices = [Vector2(-142, 5), Vector2(-185, 8)]
		"starfish":
			choices = [Vector2(35, 34), Vector2(-22, -138), Vector2(-52, -182)]
		"urchin":
			choices = [Vector2(-142, 118), Vector2(-178, 150), Vector2(-174, 0)]
		_:
			choices = [Vector2(38, 38), Vector2(-35, 165), Vector2(-160, 135), Vector2(-165, 5), Vector2(-40, -165), Vector2(140, -115)]
	var p: Vector2 = choices[0]
	for fallback: Vector2 in choices:
		if habitat_point_allowed(habitat, fallback):
			p = fallback
			break
	for attempt in range(24):
		var center: Vector2 = choices[_scatter_rng.randi_range(0, choices.size() - 1)]
		var ang: float = _scatter_rng.randf_range(0.0, TAU)
		var radius: float = sqrt(_scatter_rng.randf()) * (28.0 if habitat != "kelp" else 36.0)
		var candidate: Vector2 = center + Vector2(cos(ang), sin(ang)) * radius
		if habitat_point_allowed(habitat, candidate):
			p = candidate
			break
	return Vector3(p.x, m.seabed_y(p.x, p.y), p.y)

func build_macro_structures() -> void:
	# Pearl Garden and Rainbow Flats intentionally have no generic macro rocks:
	# they are the two broad, low breathing spaces in the world rhythm.
	# Kelp begins with one unmistakable living threshold, then grows outward.
	_regional_prop("kelp_arch", Vector2(-28, 130), 28.0, 0.0, false)
	_regional_prop("kelp_lanterns", Vector2(-52, 165), 9.0, -0.35, false)
	_regional_prop("kelp_lanterns", Vector2(-12, 198), 7.0, 0.5, false)
	# Wreck Ravine: two dedicated organic ridges frame the diagonal trench.
	_regional_prop("wreck_shoulders", Vector2(-150, 128), 34.0, 2.35, false)
	_regional_prop("wreck_shoulders", Vector2(-177, 157), 29.0, -0.7, false)
	# Moon-shell Grotto: its hero arch and pearl cairns use their own vocabulary,
	# with the terrain bowl acting as quiet enclosure rather than generic blocks.
	_regional_prop("moon_arch", Vector2(-125, 6), 36.0, 1.55, false)
	_regional_prop("moon_totem", Vector2(-175, -12), 10.0, 0.7, false)
	# Ice Current: its two unique families support the floe/shop silhouette.
	_regional_prop("ice_current", Vector2(98, -82), 15.0, -0.15, false)
	_regional_prop("ice_crystals", Vector2(155, -135), 14.0, 0.55, true)

func _regional_prop(kind: String, xz: Vector2, target: float, yrot: float, solid: bool) -> Node3D:
	var path: String = REGIONAL_SCENES[kind]
	if not ResourceLoader.exists(path):
		return null
	var packed: PackedScene = load(path)
	if packed == null:
		return null
	var wrap := Node3D.new()
	wrap.name = "Reef_region_%s" % kind
	var model: Node3D = packed.instantiate()
	m._fit_prop(model, target) # toonifies embedded matte region materials
	wrap.add_child(model)
	wrap.position = Vector3(xz.x, m.seabed_y(xz.x, xz.y), xz.y)
	wrap.rotation.y = yrot
	m.add_child(wrap)
	m.flora_nodes.append(wrap)
	if solid:
		m._register_solid(wrap, 0.68, 1.0)
	return wrap

func build_groves() -> void:
	seed_cluster_centers()
	var rng := RandomNumberGenerator.new()
	rng.seed = 0x47524F56
	for i in range(GROVES.size()):
		var entry: Dictionary = GROVES[i]
		var p: Vector2 = entry["p"]
		var kind: String = entry["kind"]
		var rocks: int = {"pearl": 0, "kelp": 1, "wreck": 2, "moon": 1, "rainbow": 0, "ice": 1}[kind]
		for k in range(rocks):
			var rp: Vector2 = _around(rng, p, 4.0, 13.0)
			var target: float = rng.randf_range(6.0, 12.0) if kind != "wreck" else rng.randf_range(9.0, 16.0)
			var rock_name: String = "rock_largea" if target > 12.0 else "rock%d" % rng.randi_range(1, 5)
			var rock: Node3D = m._gen2_prop(rock_name, Vector3(rp.x, m.seabed_y(rp.x, rp.y), rp.y), target, rng.randf_range(0.0, TAU), 0.18)
			if rock != null:
				m.flora_nodes.append(rock)
				if target >= 9.0:
					m._register_solid(rock)
		# Only one subtle magical marker per district, not one per grove.
		if i in [0, 2, 6, 9, 10, 12]:
			var col: Color = _district_accent(kind)
			m._fairy_light(Vector3(p.x, m.seabed_y(p.x, p.y) + 6.0, p.y), col, false)

func build_flora() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 0x464C4F52
	for i in range(GROVES.size()):
		var entry: Dictionary = GROVES[i]
		var p: Vector2 = entry["p"]
		var kind: String = entry["kind"]
		match kind:
			"pearl":
				_place_family(rng, kind, p, ["fanshell", "smallfanshell", "spiralshell"], 5, 2.2, 4.8, 3.0, 12.0)
				_place_family(rng, kind, p, ["sponge_barrel"], 1, 2.8, 4.0, 4.0, 9.0)
				_place_family(rng, kind, p, ["coral5", "coral2"], 2, 3.2, 5.2, 5.0, 12.0)
			"kelp":
				for k in range(8):
					var kp: Vector2 = p
					for attempt in range(8):
						var kelp_candidate: Vector2 = _around(rng, p, 4.0, 18.0)
						if habitat_point_allowed(kind, kelp_candidate):
							kp = kelp_candidate
							break
					m._gen2_seagrass(Vector3(kp.x, m.seabed_y(kp.x, kp.y), kp.y), rng.randf_range(5.0, 9.0))
				_place_family(rng, kind, p, ["coral5", "sponge_tubes"], 2, 3.0, 5.5, 5.0, 14.0)
			"wreck":
				_place_family(rng, kind, p, ["urchin_story"], 4, 1.8, 3.4, 5.0, 16.0)
				_place_family(rng, kind, p, ["sponge_barrel", "sponge_tubes"], 1, 2.5, 4.2, 6.0, 14.0)
			"moon":
				_place_family(rng, kind, p, ["anemone_story"], 5, 3.8, 7.5, 4.0, 16.0)
				_place_family(rng, kind, p, ["spiralshell", "fanshell", "coral3"], 3, 2.4, 5.0, 4.0, 13.0)
			"rainbow":
				_place_family(rng, kind, p, ["coral", "coral1", "coral4", "coral6"], 5, 2.8, 5.8, 5.0, 16.0)
				_place_family(rng, kind, p, ["starfish"], 2, 1.8, 2.8, 4.0, 12.0)
			"ice":
				_place_family(rng, kind, p, ["sponge_tubes", "sponge_barrel"], 3, 2.8, 5.2, 5.0, 16.0)
				_place_family(rng, kind, p, ["smallfanshell", "coral5"], 2, 2.0, 4.2, 5.0, 13.0)
	build_scattered_boulders(rng)

func build_scattered_boulders(rng: RandomNumberGenerator) -> void:
	for i in range(24):
		var ang: float = rng.randf_range(0.0, TAU)
		var radius: float = rng.randf_range(185.0, 245.0)
		var p := Vector2(cos(ang), sin(ang)) * radius
		var target: float = rng.randf_range(6.0, 14.0)
		var name: String = "rock_largea" if i % 4 == 0 else "rock%d" % rng.randi_range(1, 5)
		var rock: Node3D = m._gen2_prop(name, Vector3(p.x, m.seabed_y(p.x, p.y), p.y), target, rng.randf_range(0.0, TAU), 0.2)
		if rock != null:
			m.flora_nodes.append(rock)
			if target >= 9.0:
				m._register_solid(rock)

func _place_family(rng: RandomNumberGenerator, habitat: String, center: Vector2, names: Array, count: int, min_size: float, max_size: float, min_radius: float, max_radius: float) -> void:
	for i in range(count):
		var p: Vector2 = center
		for attempt in range(8):
			var candidate: Vector2 = _around(rng, center, min_radius, max_radius)
			if habitat_point_allowed(habitat, candidate):
				p = candidate
				break
		if not habitat_point_allowed(habitat, p):
			continue
		var name: String = String(names[rng.randi_range(0, names.size() - 1)])
		var node: Node3D = m._gen2_prop(name, Vector3(p.x, m.seabed_y(p.x, p.y), p.y), rng.randf_range(min_size, max_size), rng.randf_range(0.0, TAU), 0.1)
		if node != null:
			m.flora_nodes.append(node)

static func _around(rng: RandomNumberGenerator, center: Vector2, min_radius: float, max_radius: float) -> Vector2:
	var ang: float = rng.randf_range(0.0, TAU)
	var radius: float = rng.randf_range(min_radius, max_radius)
	return center + Vector2(cos(ang), sin(ang)) * radius

static func _district_accent(kind: String) -> Color:
	match kind:
		"pearl": return Color(0.86, 0.74, 0.78)
		"kelp": return Color(0.48, 0.72, 0.58)
		"wreck": return Color(0.58, 0.54, 0.68)
		"moon": return Color(0.72, 0.58, 0.82)
		"rainbow": return Color(0.88, 0.67, 0.50)
		"ice": return Color(0.58, 0.74, 0.86)
	return Color(0.65, 0.72, 0.75)
