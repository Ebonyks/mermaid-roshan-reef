class_name PaintedFeedbackArt
extends RefCounted
## Shared authored pictures only; callers own interaction and progress.
var textures: Dictionary = {}

func art(path: String) -> Texture2D:
	if not textures.has(path):
		textures[path] = load(path) as Texture2D
	return textures[path] as Texture2D

func pearl(canvas: CanvasItem, at: Vector2, state: String, side: float = 26.0) -> void:
	var texture := art("res://assets/ui/pearl_" + state + ".png")
	if texture != null:
		canvas.draw_texture_rect(texture, Rect2(at - Vector2.ONE * side * 0.5,
			Vector2.ONE * side), false)

func invitation(canvas: CanvasItem, at: Vector2, side: float, key: int,
		opening: bool = false) -> void:
	var path := "res://assets/opera/worlds/props/fx_invite_open.png" if opening else \
		"res://assets/opera/worlds/props/fx_invite_ring_%d.png" % clampi(key, 0, 3)
	var texture := art(path)
	if texture != null:
		canvas.draw_texture_rect(texture, Rect2(at - Vector2.ONE * side * 0.5,
			Vector2.ONE * side), false)
