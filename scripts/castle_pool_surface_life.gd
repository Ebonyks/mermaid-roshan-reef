class_name CastlePoolSurfaceLife
extends Polygon2D

# One bounded Canvas pass makes the broad painted pool read as living water.
# The background remains untouched; only approved project-original ripple and
# caustic textures feed the subtle Mobile-safe shader.

const SURFACE_SHADER := preload(
	"res://assets/shaders/castle_pool_surface_life.gdshader")
const RIPPLE_TEXTURE := preload("res://assets/terrain/up_water_nrm.jpg")
const CAUSTICS_TEXTURE := preload("res://assets/terrain/caustics.png")
const SURFACE_RECT := Rect2(Vector2(42.0, 300.0), Vector2(1196.0, 360.0))
const SURFACE_DEPTH := 0.58
const MAX_SURFACE_PIXELS := 1280 * 360


func _init() -> void:
	name = "MermaidPoolLivingSurface"
	polygon = PackedVector2Array([
		SURFACE_RECT.position,
		Vector2(SURFACE_RECT.end.x, SURFACE_RECT.position.y),
		SURFACE_RECT.end,
		Vector2(SURFACE_RECT.position.x, SURFACE_RECT.end.y),
	])
	uv = PackedVector2Array([
		Vector2(0.0, 0.0), Vector2(1.0, 0.0),
		Vector2(1.0, 1.0), Vector2(0.0, 1.0),
	])
	z_index = int(round(SURFACE_DEPTH * 100.0))
	color = Color.WHITE
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	var surface_material := ShaderMaterial.new()
	surface_material.shader = SURFACE_SHADER
	surface_material.set_shader_parameter("ripple", RIPPLE_TEXTURE)
	surface_material.set_shader_parameter("caustics", CAUSTICS_TEXTURE)
	material = surface_material
	set_meta("castle_pool_surface_life", true)
	set_meta("bounded_surface_rect", SURFACE_RECT)
	set_meta("mobile_fragment_bound", int(SURFACE_RECT.get_area()))
	set_meta("source_asset_role", "non_destructive_water_motion_overlay")


func audit_snapshot() -> Dictionary:
	return {
		"canvas_only": self is CanvasItem,
		"surface_rect": SURFACE_RECT,
		"surface_pixels": int(SURFACE_RECT.get_area()),
		"max_surface_pixels": MAX_SURFACE_PIXELS,
		"depth": SURFACE_DEPTH,
		"shader": SURFACE_SHADER.resource_path,
		"ripple": RIPPLE_TEXTURE.resource_path,
		"caustics": CAUSTICS_TEXTURE.resource_path,
		"point_count": polygon.size(),
	}
