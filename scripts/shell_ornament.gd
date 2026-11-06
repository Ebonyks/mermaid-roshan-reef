class_name ShellOrnament
extends Control
# One painted project-owned shell motif, shared without flattening a menu.
# Callers retain their original bounds, names, stacking and input ownership.

const PAINTED_SHELL: Texture2D = preload(
	"res://assets/flats/castle/logo_studio_v2/castle_banner_motif_shell.png")

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	resized.connect(queue_redraw)

func _draw() -> void:
	if size.x <= 1.0 or size.y <= 1.0:
		return
	# Keep the authored aspect and alpha edge at every existing crest size.
	# The hinge stays near the original lower edge of the ornament's box.
	var native_size: Vector2 = PAINTED_SHELL.get_size()
	var available := size * Vector2(0.86, 0.90)
	var fit: float = minf(available.x / native_size.x, available.y / native_size.y)
	var painted_size := native_size * fit
	var origin := Vector2((size.x - painted_size.x) * 0.5,
		size.y * 0.95 - painted_size.y)
	draw_texture_rect(PAINTED_SHELL, Rect2(origin, painted_size), false)
