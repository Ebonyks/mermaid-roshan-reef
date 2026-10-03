extends OperaGeologySurface
## NON_RUNTIME_COUNTERFACTUAL: original fossil pixels, complementary fracture
## partitions only. All inherited mechanics, saves, touch and input unchanged.
var _fracture_edge_runs: Dictionary = {}

const FRACTURE_A := [Vector2(0.333333333333, 0.0), Vector2(0.31, 0.13),
	Vector2(0.365, 0.27), Vector2(0.315, 0.40), Vector2(0.35, 0.54),
	Vector2(0.29, 0.69), Vector2(0.355, 0.84), Vector2(0.333333333333, 1.0)]
const FRACTURE_B := [Vector2(0.666666666667, 0.0), Vector2(0.705, 0.15),
	Vector2(0.64, 0.28), Vector2(0.69, 0.43), Vector2(0.63, 0.58),
	Vector2(0.70, 0.73), Vector2(0.645, 0.87), Vector2(0.666666666667, 1.0)]

func piece_partition(index: int) -> PackedVector2Array:
	var polygon := PackedVector2Array()
	if index == 0:
		polygon.append(Vector2.ZERO)
		for point: Vector2 in FRACTURE_A:
			polygon.append(point)
		polygon.append(Vector2(0.0, 1.0))
	elif index == 1:
		for point: Vector2 in FRACTURE_A:
			polygon.append(point)
		for i: int in range(FRACTURE_B.size() - 1, -1, -1):
			polygon.append(FRACTURE_B[i])
	else:
		for point: Vector2 in FRACTURE_B:
			polygon.append(point)
		polygon.append(Vector2.ONE)
		polygon.append(Vector2(1.0, 0.0))
	return polygon

func _draw_fossil_piece(index: int, rect: Rect2) -> void:
	var atlas := fossil_texture as AtlasTexture
	if atlas == null or atlas.atlas == null:
		super._draw_fossil_piece(index, rect)
		return
	var points := PackedVector2Array()
	var uvs := PackedVector2Array()
	var colors := PackedColorArray()
	var full_size := Vector2(rect.size.x * 3.0, rect.size.y)
	var offset := Vector2(float(index) / 3.0, 0.0)
	for point: Vector2 in piece_partition(index):
		points.append(rect.position + (point - offset) * full_size)
		uvs.append((atlas.region.position + point * atlas.region.size) / atlas.atlas.get_size())
		colors.append(Color.WHITE)
	draw_polygon(points, colors, uvs, atlas.atlas)

	if index > 0 and not (fossil_snapped[index] and fossil_snapped[index - 1]):
		_draw_exposed_fracture(index - 1, atlas, rect, offset, full_size)
	if index < 2 and not (fossil_snapped[index] and fossil_snapped[index + 1]):
		_draw_exposed_fracture(index, atlas, rect, offset, full_size)

func _opaque_fracture_runs(edge: int, atlas: AtlasTexture) -> Array:
	if _fracture_edge_runs.has(edge):
		return _fracture_edge_runs[edge]
	var image: Image = atlas.atlas.get_image()
	var curve: Array = FRACTURE_A if edge == 0 else FRACTURE_B
	var runs: Array[PackedVector2Array] = []
	var run := PackedVector2Array()
	for segment: int in range(curve.size() - 1):
		for step: int in range(49):
			if segment > 0 and step == 0:
				continue
			var point: Vector2 = curve[segment].lerp(curve[segment + 1], float(step) / 48.0)
			var pixel := atlas.region.position + point * atlas.region.size
			var x := clampi(floori(pixel.x), 0, image.get_width() - 1)
			var y := clampi(floori(pixel.y), 0, image.get_height() - 1)
			if image.get_pixel(x, y).a > 16.0 / 255.0:
				run.append(point)
			else:
				if run.size() > 1:
					runs.append(run)
				run = PackedVector2Array()
	if run.size() > 1:
		runs.append(run)
	_fracture_edge_runs[edge] = runs
	return runs

func _draw_exposed_fracture(edge: int, atlas: AtlasTexture, rect: Rect2,
		offset: Vector2, full_size: Vector2) -> void:
	for run: PackedVector2Array in _opaque_fracture_runs(edge, atlas):
		var points := PackedVector2Array()
		for point: Vector2 in run:
			points.append(rect.position + (point - offset) * full_size)
		draw_polyline(points, Color("#77516f"), 2.0, true)
