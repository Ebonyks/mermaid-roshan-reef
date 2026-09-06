extends SceneTree

const Navigation := preload("res://scripts/stage_navigation_2d.gd")
var failures: int = 0

func _initialize() -> void:
	var nav := Navigation.new()
	var lanes: Array[PackedVector2Array] = [
		PackedVector2Array([Vector2(0, 0), Vector2(100, 0), Vector2(100, 100)]),
		PackedVector2Array([Vector2(50, 0), Vector2(50, -50)]),
	]
	nav.configure(lanes)
	_check(not nav.contains_point(Vector2(75, 50)), "furniture inside bounding rectangle is OOB")
	_check(nav.nearest_point(Vector2(90, 60)).is_equal_approx(Vector2(100, 60)), "OOB touch projects to floor")
	var route: PackedVector2Array = nav.route(Vector2(50, -35), Vector2(100, 80))
	_check(route.size() >= 4, "spur-to-spur route keeps both corners")
	_check(route[0].is_equal_approx(Vector2(50, -35)), "retarget mid-spur preserves feet")
	_check(route[route.size() - 1].is_equal_approx(Vector2(100, 80)), "route arrives at requested approach")
	_check(_route_is_allowed(nav, route), "every movement substep stays on floor")
	var reverse: PackedVector2Array = nav.route(Vector2(100, 80), Vector2(50, -35))
	_check(_route_is_allowed(nav, reverse), "reverse retarget uses same network")
	_check(nav.route(Vector2(50, 0), Vector2(50, 0)).size() > 0, "already-arrived intent is valid")
	lanes.append(PackedVector2Array([Vector2(300, 0), Vector2(400, 0)]))
	nav.configure(lanes)
	_check(nav.route(Vector2(0, 0), Vector2(350, 0)).is_empty(), "disconnected room cannot be crossed")
	lanes = [PackedVector2Array([Vector2(0, 50), Vector2(100, 50)]),
		PackedVector2Array([Vector2(50, 0), Vector2(50, 100)])]
	nav.configure(lanes)
	_check(_route_is_allowed(nav, nav.route(Vector2(0, 50), Vector2(50, 100))), "interior crossing forms junction")
	nav.configure([])
	_check(nav.route(Vector2.ZERO, Vector2.ONE).is_empty(), "missing geometry fails closed")
	_check(not nav.contains_point(Vector2.ZERO), "empty stage has no accessible floor")
	if failures == 0:
		print("STAGE NAVIGATION 2D | ALL OK")
	quit(1 if failures else 0)

func _route_is_allowed(nav: Navigation, route: PackedVector2Array) -> bool:
	if route.is_empty():
		return false
	for index in range(1, route.size()):
		for sample in range(101):
			if not nav.contains_point(route[index - 1].lerp(route[index], float(sample) / 100.0)):
				return false
	return true

func _check(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		print("STAGE NAVIGATION 2D | FAIL | " + message)
