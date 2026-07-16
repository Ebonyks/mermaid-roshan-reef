class_name ReefDistricts
extends RefCounted

# Authored composition for the open undersea world. Gameplay state remains on
# ReefMain; this satellite only chooses terrain shapes, scenery and dressing.

const GROVES := [
	{"p": Vector2(45, 27), "kind": "pearl"},
	{"p": Vector2(30, 52), "kind": "pearl"},
	{"p": Vector2(-24, 78), "kind": "kelp"},
	{"p": Vector2(-48, 108), "kind": "kelp"},
	{"p": Vector2(4, 125), "kind": "kelp"},
	{"p": Vector2(-8, 158), "kind": "kelp"},
	{"p": Vector2(-84, 78), "kind": "wreck"},
	{"p": Vector2(-126, 112), "kind": "wreck"},
	{"p": Vector2(-158, 82), "kind": "wreck"},
	{"p": Vector2(-88, 8), "kind": "moon"},
	{"p": Vector2(-124, -10), "kind": "moon"},
	{"p": Vector2(-151, 24), "kind": "moon"},
	{"p": Vector2(-50, -68), "kind": "rainbow"},
	{"p": Vector2(-14, -112), "kind": "rainbow"},
	{"p": Vector2(23, -128), "kind": "rainbow"},
	{"p": Vector2(52, -48), "kind": "ice"},
	{"p": Vector2(88, -76), "kind": "ice"},
	{"p": Vector2(118, -42), "kind": "ice"},
]

const REGION_CENTERS := {
	"pearl": Vector2(20, 25),
	"kelp": Vector2(-22, 116),
	"wreck": Vector2(-122, 100),
	"moon": Vector2(-124, 4),
	"rainbow": Vector2(-12, -105),
	"ice": Vector2(82, -60),
}

const STRUCTURE_SCENES := {
	"spire": "res://assets/nature/cliff_large_rock.glb",
	"block": "res://assets/nature/cliff_block_rock.glb",
	"cave": "res://assets/ship/cliff_cave_rock.glb",
}

const REGIONAL_SCENES := {
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
	"kelp": ["cathedral arches", "lantern pods", "tall kelp aisles"],
	"wreck": ["broken ship", "treasure debris", "ravine shoulders"],
	"moon": ["shell arch", "pearl totems", "anemone bowls"],
	"rainbow": ["race gateway", "coral bouquets", "starfish flats"],
	"ice": ["crystal clusters", "current fins", "penguin floe"],
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
	h = lerpf(h, -3.0, _soft_disc(p, REGION_CENTERS["rainbow"], 55.0) * 0.68)
	# The wreck sits in a real diagonal ravine with raised shoulders.
	var trench: float = _segment_mask(p, Vector2(-174, 148), Vector2(-72, 62), 25.0)
	var shoulders: float = _segment_mask(p, Vector2(-174, 148), Vector2(-72, 62), 48.0) - trench
	h -= trench * 12.0
	h += maxf(shoulders, 0.0) * 9.0
	# A quiet bowl and broken ring give the moon grotto enclosure.
	var moon_inner: float = _soft_disc(p, REGION_CENTERS["moon"], 45.0)
	var moon_outer: float = _soft_disc(p, REGION_CENTERS["moon"], 72.0)
	h -= moon_inner * 8.0
	h += maxf(moon_outer - moon_inner, 0.0) * 17.0
	# Long ridges behind the kelp district make its vertical skyline legible.
	h += _segment_mask(p, Vector2(-68, 98), Vector2(-50, 170), 24.0) * 12.0
	h += _segment_mask(p, Vector2(22, 92), Vector2(16, 170), 20.0) * 9.0
	return h

static func region_at(p: Vector2) -> String:
	if p.length() < 50.0:
		return "pearl"
	var best := "pearl"
	var best_d := INF
	for key: String in REGION_CENTERS:
		var d: float = p.distance_squared_to(REGION_CENTERS[key])
		if d < best_d:
			best_d = d
			best = key
	return best

func seed_cluster_centers() -> void:
	m.cluster_centers.clear()
	for entry: Dictionary in GROVES:
		var p: Vector2 = entry["p"]
		m.cluster_centers.append(Vector3(p.x, m.seabed_y(p.x, p.y), p.y))

func grove_kind(index: int) -> String:
	return String((GROVES[index] as Dictionary)["kind"])

func scatter_point(habitat: String) -> Vector3:
	var choices: Array[Vector2] = []
	match habitat:
		"kelp":
			choices = [Vector2(-24, 90), Vector2(-44, 126), Vector2(5, 140)]
		"anemone":
			choices = [Vector2(-104, 5), Vector2(-142, 18), Vector2(36, 35)]
		"starfish":
			choices = [Vector2(18, 24), Vector2(-15, -92), Vector2(20, -125)]
		"urchin":
			choices = [Vector2(-116, 96), Vector2(-146, 78), Vector2(-128, -2)]
		_:
			choices = [Vector2(36, 38), Vector2(-25, 105), Vector2(-120, 102), Vector2(-125, 4), Vector2(-8, -104), Vector2(83, -62)]
	var center: Vector2 = choices[_scatter_rng.randi_range(0, choices.size() - 1)]
	var ang: float = _scatter_rng.randf_range(0.0, TAU)
	var radius: float = sqrt(_scatter_rng.randf()) * (38.0 if habitat != "kelp" else 46.0)
	# A small minority bridges districts; the hub itself stays calm and open.
	if _scatter_rng.randf() < 0.16:
		ang = _scatter_rng.randf_range(0.0, TAU)
		radius = _scatter_rng.randf_range(75.0, 220.0)
		center = Vector2.ZERO
	var p: Vector2 = center + Vector2(cos(ang), sin(ang)) * radius
	if p.length() < 28.0:
		p = p.normalized() * 28.0 if p.length() > 0.1 else Vector2(28.0, 0.0)
	return Vector3(p.x, m.seabed_y(p.x, p.y), p.y)

func build_macro_structures() -> void:
	# Pearl Garden: low framing stones leave the centre broad and readable.
	_structure("block", Vector2(-38, 20), 25.0, 0.4, Color(0.58, 0.63, 0.69), false)
	_structure("block", Vector2(36, -17), 22.0, -0.8, Color(0.64, 0.61, 0.72), false)
	# Kelp Cathedral: paired ribs create a destination-scale aisle.
	for row in range(3):
		var z: float = 86.0 + float(row) * 34.0
		_structure("spire", Vector2(-58, z), 38.0 + float(row) * 5.0, 0.25, Color(0.28, 0.43, 0.43))
		_structure("spire", Vector2(18, z + 5.0), 34.0 + float(row) * 4.0, -0.4, Color(0.30, 0.46, 0.44))
	# Two enormous living ribs create an actual cathedral sequence; lantern
	# clusters punctuate it without repeating at every grove.
	_regional_prop("kelp_arch", Vector2(-20, 105), 30.0, 0.0, false)
	_regional_prop("kelp_arch", Vector2(-18, 145), 34.0, 0.08, false)
	_regional_prop("kelp_lanterns", Vector2(-47, 92), 9.0, -0.35, false)
	_regional_prop("kelp_lanterns", Vector2(5, 126), 10.0, 0.5, false)
	_regional_prop("kelp_lanterns", Vector2(-45, 158), 8.0, -0.8, false)
	# Wreck Ravine: two irregular shoulders frame the diagonal trench.
	var wreck_left := [Vector2(-157, 126), Vector2(-132, 108), Vector2(-105, 85)]
	var wreck_right := [Vector2(-139, 149), Vector2(-110, 128), Vector2(-82, 101)]
	for i in range(wreck_left.size()):
		_structure("block", wreck_left[i], 34.0 + float(i) * 5.0, 2.35, Color(0.42, 0.43, 0.55))
		_structure("spire", wreck_right[i], 31.0 + float(i) * 4.0, -0.7, Color(0.36, 0.40, 0.52))
	# Moon-shell Grotto: its hero arch and pearl cairns use their own vocabulary,
	# with asymmetric rock masses acting as quiet enclosure rather than identity.
	_regional_prop("moon_arch", Vector2(-126, 2), 42.0, 1.55, false)
	_regional_prop("moon_totem", Vector2(-101, -24), 9.0, -0.4, false)
	_regional_prop("moon_totem", Vector2(-151, 23), 11.0, 0.7, false)
	_regional_prop("moon_totem", Vector2(-105, 33), 7.0, 1.2, false)
	_structure("spire", Vector2(-162, -18), 38.0, 0.2, Color(0.48, 0.44, 0.59))
	_structure("block", Vector2(-91, 30), 32.0, -0.5, Color(0.59, 0.50, 0.66))
	# Rainbow Flats: low warm banks preserve long, open race lanes.
	_structure("block", Vector2(-58, -112), 26.0, 0.8, Color(0.64, 0.55, 0.48), false)
	_structure("block", Vector2(38, -104), 24.0, -0.7, Color(0.66, 0.57, 0.51), false)
	# Ice Current: sparse blue-grey pillars support the floe/shop silhouette.
	_structure("spire", Vector2(96, -103), 39.0, -0.25, Color(0.47, 0.58, 0.69))
	_structure("block", Vector2(128, -47), 31.0, 0.55, Color(0.50, 0.61, 0.71))
	_structure("spire", Vector2(82, -25), 29.0, 0.2, Color(0.45, 0.55, 0.67), false)
	_regional_prop("ice_crystals", Vector2(72, -91), 15.0, -0.3, true)
	_regional_prop("ice_crystals", Vector2(117, -68), 11.0, 0.55, true)
	_regional_prop("ice_current", Vector2(51, -51), 14.0, -0.15, false)
	_regional_prop("ice_current", Vector2(101, -28), 12.0, 0.7, false)

func _structure(kind: String, xz: Vector2, target: float, yrot: float, tint: Color, solid: bool = true) -> Node3D:
	var path: String = STRUCTURE_SCENES[kind]
	if not ResourceLoader.exists(path):
		return null
	var packed: PackedScene = load(path)
	if packed == null:
		return null
	var wrap := Node3D.new()
	wrap.name = "Reef_%s" % kind
	var model: Node3D = packed.instantiate()
	m._fit_prop(model, target)
	m._toon_tile(model, "cliff", 0.045, tint)
	wrap.add_child(model)
	wrap.position = Vector3(xz.x, m.seabed_y(xz.x, xz.y) - 1.2, xz.y)
	wrap.rotation.y = yrot
	m.add_child(wrap)
	m.flora_nodes.append(wrap)
	if solid:
		m._register_solid(wrap, 0.72, 1.2)
	return wrap

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
		var rocks: int = {"pearl": 1, "kelp": 2, "wreck": 4, "moon": 3, "rainbow": 1, "ice": 2}[kind]
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
		if i in [0, 2, 6, 9, 12, 15]:
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
				_place_family(rng, p, ["fanshell", "smallfanshell", "spiralshell"], 5, 2.2, 4.8, 3.0, 12.0)
				_place_family(rng, p, ["sponge_barrel"], 1, 2.8, 4.0, 4.0, 9.0)
				_place_family(rng, p, ["coral5", "coral2"], 2, 3.2, 5.2, 5.0, 12.0)
			"kelp":
				for k in range(8):
					var kp: Vector2 = _around(rng, p, 4.0, 18.0)
					m._gen2_seagrass(Vector3(kp.x, m.seabed_y(kp.x, kp.y), kp.y), rng.randf_range(5.0, 9.0))
				_place_family(rng, p, ["coral5", "sponge_tubes"], 2, 3.0, 5.5, 5.0, 14.0)
			"wreck":
				_place_family(rng, p, ["urchin_story"], 4, 1.8, 3.4, 5.0, 16.0)
				_place_family(rng, p, ["sponge_barrel", "sponge_tubes"], 1, 2.5, 4.2, 6.0, 14.0)
			"moon":
				_place_family(rng, p, ["anemone_story"], 5, 3.8, 7.5, 4.0, 16.0)
				_place_family(rng, p, ["spiralshell", "fanshell", "coral3"], 3, 2.4, 5.0, 4.0, 13.0)
			"rainbow":
				_place_family(rng, p, ["coral", "coral1", "coral4", "coral6"], 5, 2.8, 5.8, 5.0, 16.0)
				_place_family(rng, p, ["starfish"], 2, 1.8, 2.8, 4.0, 12.0)
			"ice":
				_place_family(rng, p, ["sponge_tubes", "sponge_barrel"], 3, 2.8, 5.2, 5.0, 16.0)
				_place_family(rng, p, ["smallfanshell", "coral5"], 2, 2.0, 4.2, 5.0, 13.0)
	build_scattered_boulders(rng)

func build_scattered_boulders(rng: RandomNumberGenerator) -> void:
	for i in range(42):
		var ang: float = rng.randf_range(0.0, TAU)
		var radius: float = rng.randf_range(62.0, 225.0)
		var p := Vector2(cos(ang), sin(ang)) * radius
		var target: float = rng.randf_range(6.0, 14.0)
		var name: String = "rock_largea" if i % 4 == 0 else "rock%d" % rng.randi_range(1, 5)
		var rock: Node3D = m._gen2_prop(name, Vector3(p.x, m.seabed_y(p.x, p.y), p.y), target, rng.randf_range(0.0, TAU), 0.2)
		if rock != null:
			m.flora_nodes.append(rock)
			if target >= 9.0:
				m._register_solid(rock)

func _place_family(rng: RandomNumberGenerator, center: Vector2, names: Array, count: int, min_size: float, max_size: float, min_radius: float, max_radius: float) -> void:
	for i in range(count):
		var p: Vector2 = _around(rng, center, min_radius, max_radius)
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
