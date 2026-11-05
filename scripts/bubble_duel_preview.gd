extends Control
## Selection and gameplay share the exact actor and attachment renderer.
var appearance: BubbleDuelCast
var profile: Dictionary = {}
var moving := false
var facing := 1.0
var clock := 0.0


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func _process(delta: float) -> void:
	clock += delta
	queue_redraw()


func _draw() -> void:
	if appearance != null and not profile.is_empty():
		var bounds := appearance.bounds(profile, moving, clock)
		var factor := minf((size.x - 8.0) / bounds.size.x, (size.y - 8.0) / bounds.size.y)
		var center := bounds.get_center()
		var at := size * 0.5 - Vector2(center.x * facing, center.y) * factor
		appearance.draw_actor(self, profile, at, facing, moving, clock, factor)
