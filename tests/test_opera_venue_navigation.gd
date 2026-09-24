extends SceneTree

const Nav := preload("res://scripts/opera_venue_navigation.gd")
var bad := 0


func _init() -> void:
	var nav := Nav.new()
	var mask := 0
	for count in range(16):
		var expected := mini(count / 4, 3)
		_check("stage after %d unique careers" % count, Nav.stage_for_mask(mask) == expected)
		_check("retired stars cannot unlock floors", Nav.stage_for_mask(mask | 0x4210) == expected)
		if count < 15:
			mask |= 1 << Nav.LIVE_ORDER[count]
	_check("later stars cannot bypass the opening quartet", Nav.stage_for_mask(mask & ~1) == 0)
	for stage in range(4):
		nav.rebuild(stage)
		for target_floor in range(4):
			var path := nav.route(Vector2(530, 690), 0,
				Vector2(820, Nav.FLOOR_Y[target_floor]), target_floor)
			_check("stage %d destination floor %d" % [stage, target_floor],
				path.is_empty() == (target_floor > stage))
			if target_floor > stage:
				continue
			_check("route preserves its origin", path[0].is_equal_approx(Vector2(530, 690)))
			_check("route ends at the pointed door", path[-1].is_equal_approx(Vector2(820, Nav.FLOOR_Y[target_floor])))
			if target_floor >= 1:
				_check("upper floor route follows stair treads", path.size() >= 7)
			if target_floor >= 2:
				_check("floor three uses the left lift", _has_edge(path, Vector2(263, 389), Vector2(263, 270)))
			if target_floor == 3:
				_check("floor four uses the right lift", _has_edge(path, Vector2(1010, 270), Vector2(1010, 151)))
			for i in range(1, path.size()):
				if path[i].y >= 512 and path[i - 1].y >= 512:
					_check("foyer route clears furniture", nav.clear_segment(path[i - 1], path[i]))
	nav.rebuild(3)
	var around := nav.route(Vector2(530, 630), 0, Vector2(820, 630), 0)
	_check("planter forces a detour", around.size() > 2)
	for i in range(1, around.size()):
		_check("every detour segment clears the inflated planter", nav.clear_segment(around[i - 1], around[i]))
	var snapped := nav.project(Vector2(650, 600), 0)
	_check("tap inside planter resolves to a reachable edge", nav.clear_segment(snapped, snapped))
	var up := nav.route(Vector2(452, 512), 0, Vector2(452, 270), 2)
	for point: Vector2 in up:
		if point.y > 389 and point.y < 512:
			var retarget := nav.route(point, 0, Vector2(820, 512), 0)
			_check("mid-stair retarget never teleports", not retarget.is_empty() and retarget[0].is_equal_approx(point))
	var down := nav.route(Vector2(820, 151), 3, Vector2(452, 512), 0)
	_check("return uses right lift down", _has_edge(down, Vector2(1010, 151), Vector2(1010, 270)))
	_check("return uses left lift down", _has_edge(down, Vector2(263, 270), Vector2(263, 389)))
	var initial_count := nav.graph.get_point_count()
	for i in range(100):
		nav.route(Vector2(530, 690), 0, Vector2(820, 151), 3)
	_check("retargeting does not leak graph nodes", nav.graph.get_point_count() == initial_count)
	print("OPERA NAVIGATION ALL OK" if bad == 0 else "OPERA NAVIGATION FAIL: %d" % bad)
	quit(0 if bad == 0 else 1)


func _has_edge(path: PackedVector2Array, a: Vector2, b: Vector2) -> bool:
	for i in range(1, path.size()):
		if path[i - 1].is_equal_approx(a) and path[i].is_equal_approx(b):
			return true
	return false


func _check(label: String, ok: bool) -> void:
	if not ok:
		bad += 1
		print("FAIL: " + label)
