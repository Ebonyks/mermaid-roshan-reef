extends SceneTree
func _initialize() -> void:
	for c: Dictionary in preload("res://scripts/racer/reef_kart_courses.gd").COURSES:
		var t := ReefKartTrack.new(c)
		var margin := INF
		for point: Vector2 in t.center:
			margin = minf(margin, minf(minf(point.x, point.y), minf(t.world_size - point.x, t.world_size - point.y)))
		print("COURSE_BOUNDS|", t.id, "|minimum_field_margin=", margin, "|outer_curb=", ReefKartTrack.RAIL + 8.0)
	quit()
