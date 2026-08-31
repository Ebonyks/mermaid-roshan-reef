extends SceneTree
## Focused contract probe for Opera's diegetic room navigation. It validates
## authored station geography and the deterministic route network without
## loading the career world or depending on presentation nodes.

const StagePaths := preload("res://scripts/opera_stage_paths.gd")

const EXPECTED_STATIONS: Dictionary = {
	"chef": [
		"mixing_bowl", "hearth_oven", "cake_tower", "macaron_cart",
		"grand_cake_stage",
	],
	"detective": [
		"evidence_shelves", "pedestal_display", "magnifier_tower",
		"mirror_gallery", "treasure_dais",
	],
	"ballerina": [
		"curtain_alcove", "wave_tuffets", "shell_bandstand",
		"trifold_mirror", "rose_finale_stage",
	],
	"candymaker": [
		"gumball_vat", "taffy_press", "candy_bag_cottage",
		"sweet_display_shop", "candy_cart",
	],
	"doctor": [
		"starfish_triage", "stethoscope_clinic", "thermometer_garden",
		"exam_booth", "recovery_bed",
	],
	"farmer": [
		"barn_doors", "pearl_clam", "blossom_arch", "seed_beds",
		"hay_bales",
	],
	"boxer": [
		"glove_wall_shelf", "purple_sparring_mat", "teal_heavy_bag",
		"shell_pavilion_stage", "red_heavy_bag",
	],
	"magician": [
		"violet_shell_stage", "pearl_tide_pool", "teal_shell_stage",
		"pearl_lamp_avenue", "rose_shell_stage",
	],
	"painter": [
		"purple_paint_pot", "gazebo_easel", "coral_paint_pot",
		"rainbow_brush", "arch_easel",
	],
	"astronaut": [
		"coolant_tank_pad", "pipe_arch_planter", "periscope_elbow",
		"airlock_ring", "rocket_launch_dais",
	],
	"racer": [
		"pearl_start_arch", "teal_gem_buoy", "pearl_dome_pavilion",
		"rose_gem_buoy", "ribbon_finish_arch",
	],
	"popstar": [
		"shell_stage", "clam_coral_bed", "mic_gazebo",
		"pink_clam_reef", "record_dais",
	],
	"nursery": [
		"wash_basin", "cuddle_cushions", "bottle_nook", "moon_bed",
	],
	"geologist": [
		"layer_wall", "fossil_table", "specimen_trays", "crystal_gallery",
	],
}

## Mirrors the shipping PHASE_STATIONS bindings by station ID. Repeated IDs
## are intentional: this is the full 53-phase playable contract, not merely a
## set of the 45 physical landmarks those phases share.
const PLAYABLE_PHASE_STATIONS: Dictionary = {
	"chef": [
		"mixing_bowl", "mixing_bowl", "hearth_oven",
		"grand_cake_stage", "grand_cake_stage",
	],
	"detective": [
		"magnifier_tower", "evidence_shelves", "treasure_dais",
	],
	"ballerina": [
		"trifold_mirror", "wave_tuffets", "rose_finale_stage",
	],
	"candymaker": [
		"gumball_vat", "taffy_press", "candy_bag_cottage", "candy_cart",
	],
	"doctor": [
		"stethoscope_clinic", "starfish_triage", "exam_booth",
		"exam_booth", "recovery_bed",
	],
	"farmer": ["seed_beds", "hay_bales", "barn_doors", "blossom_arch"],
	"boxer": [
		"glove_wall_shelf", "purple_sparring_mat", "teal_heavy_bag",
		"shell_pavilion_stage", "shell_pavilion_stage",
	],
	"magician": [
		"violet_shell_stage", "pearl_tide_pool", "teal_shell_stage",
		"rose_shell_stage", "rose_shell_stage",
	],
	"painter": ["gazebo_easel", "rainbow_brush", "arch_easel"],
	"astronaut": [
		"coolant_tank_pad", "pipe_arch_planter", "periscope_elbow",
		"rocket_launch_dais",
	],
	"racer": [
		"pearl_dome_pavilion", "pearl_start_arch", "ribbon_finish_arch",
	],
	"nursery": [
		"wash_basin", "cuddle_cushions", "bottle_nook",
		"cuddle_cushions", "moon_bed",
	],
	"popstar": ["mic_gazebo", "record_dais", "shell_stage", "shell_stage"],
	"geologist": ["layer_wall", "fossil_table", "specimen_trays", "crystal_gallery"],
}

const SCREEN_BOUNDS := Rect2(Vector2.ZERO, Vector2(1280.0, 720.0))
const ROUTE_TOLERANCE := 0.35
const POSITION_TOLERANCE := 0.1
const MIN_TOUCH_TARGET := 110.0
const ROSHAN_BODY_SIZE := Vector2(96.0, 176.0)

var checks := 0
var failed := 0
var station_count := 0
var authored_spur_count := 0
var playable_phase_count := 0


func _ck(name: String, ok: bool, detail: String = "") -> void:
	checks += 1
	if ok:
		return
	failed += 1
	var suffix := "" if detail.is_empty() else "|%s" % detail
	print("OPERA_DIEGETIC_PATHS|FAIL|%s%s" % [name, suffix])


func _point_finite(point: Vector2) -> bool:
	return is_finite(point.x) and is_finite(point.y)


func _rect_inside(bounds: Rect2, rect: Rect2,
		tolerance: float = 0.01) -> bool:
	return rect.position.x >= bounds.position.x - tolerance \
		and rect.position.y >= bounds.position.y - tolerance \
		and rect.end.x <= bounds.end.x + tolerance \
		and rect.end.y <= bounds.end.y + tolerance


func _roshan_body_at(feet: Vector2) -> Rect2:
	# Runtime uses a 250px atlas cell with generous transparent padding. This
	# approximates the visible idle silhouette inside that cell at the same
	# painted-depth scale used by _place_on_stage().
	var depth := clampf(0.62 + (feet.y / StagePaths.SCREEN.y) * 0.55,
		0.62, 1.1)
	var body_size := ROSHAN_BODY_SIZE * depth
	return Rect2(
		Vector2(feet.x - body_size.x * 0.5,
			feet.y - body_size.y + 10.0 * depth),
		Vector2(body_size.x, body_size.y - 6.0 * depth))


func _contains_points_in_order(route: PackedVector2Array,
		expected: PackedVector2Array) -> bool:
	var route_index := 0
	for expected_point: Vector2 in expected:
		var found := false
		while route_index < route.size():
			if route[route_index].distance_to(expected_point) \
					<= POSITION_TOLERANCE:
				found = true
				route_index += 1
				break
			route_index += 1
		if not found:
			return false
	return true


func _reversed(points: PackedVector2Array) -> PackedVector2Array:
	var out := PackedVector2Array()
	for index in range(points.size() - 1, -1, -1):
		out.append(points[index])
	return out


func _max_distance_from_chord(points: PackedVector2Array) -> float:
	if points.size() < 3:
		return 0.0
	var start := points[0]
	var finish := points[points.size() - 1]
	var edge := finish - start
	var edge_length_squared := edge.length_squared()
	var maximum := 0.0
	for index in range(1, points.size() - 1):
		var local := 0.0
		if edge_length_squared > 0.0:
			local = clampf(
				(points[index] - start).dot(edge) / edge_length_squared,
				0.0, 1.0)
		maximum = maxf(maximum,
			points[index].distance_to(start.lerp(finish, local)))
	return maximum


func _route_contract(career: String, label: String,
		route: PackedVector2Array, expected_end: Vector2) -> void:
	_ck("%s/%s route exists" % [career, label], not route.is_empty())
	if route.is_empty():
		return
	_ck("%s/%s route ends at projection" % [career, label],
		route[route.size() - 1].distance_to(expected_end) <= POSITION_TOLERANCE)
	var points_inside := true
	var points_approved := true
	for point: Vector2 in route:
		points_inside = points_inside and _point_finite(point) \
			and SCREEN_BOUNDS.has_point(point)
		points_approved = points_approved \
			and StagePaths.point_is_on_approved_route(
				career, point, ROUTE_TOLERANCE)
	_ck("%s/%s route points stay in room" % [career, label], points_inside)
	_ck("%s/%s route points approved" % [career, label], points_approved)
	_ck("%s/%s route segments approved" % [career, label],
		StagePaths.route_is_approved(career, route, ROUTE_TOLERANCE))


func _audit_station(career: String, station_id: String,
		start: Vector2) -> void:
	station_count += 1
	var record: Dictionary = StagePaths.station_by_id(career, station_id)
	_ck("%s/%s explicit record" % [career, station_id],
		not record.is_empty() and String(record.get("id", "")) == station_id)
	if record.is_empty():
		return
	_ck("%s/%s has distinct navigation fields" % [career, station_id],
		record.has("object_pos") and record.has("approach_pos")
		and record.has("visual_size") and record.has("hotspot_size")
		and record.has("spur"))

	var object_pos: Vector2 = StagePaths.station_object_position(
		career, station_id)
	var approach_pos: Vector2 = StagePaths.station_approach(career, station_id)
	var visual_size: Vector2 = StagePaths.station_visual_size(
		career, station_id)
	var hotspot_size: Vector2 = record.get("hotspot_size", Vector2.ZERO)
	var spur: PackedVector2Array = StagePaths.station_spur(career, station_id)
	_ck("%s/%s helper values match record" % [career, station_id],
		object_pos.distance_to(record.get("object_pos", Vector2.ZERO))
			<= POSITION_TOLERANCE
		and approach_pos.distance_to(
			record.get("approach_pos", Vector2.ZERO)) <= POSITION_TOLERANCE
		and visual_size.distance_to(
			record.get("visual_size", Vector2.ZERO)) <= POSITION_TOLERANCE
		and spur == (record.get("spur", PackedVector2Array()) \
			as PackedVector2Array))
	_ck("%s/%s object and approach finite" % [career, station_id],
		_point_finite(object_pos) and _point_finite(approach_pos))
	_ck("%s/%s object and approach in room" % [career, station_id],
		SCREEN_BOUNDS.has_point(object_pos)
		and SCREEN_BOUNDS.has_point(approach_pos))

	# The isolated object and its local glow live inside the forgiving touch
	# target. All three remain wholly on-screen so no control is clipped.
	var hit_rect := Rect2(object_pos - hotspot_size * 0.5, hotspot_size)
	var visual_rect := Rect2(object_pos - visual_size * 0.5, visual_size)
	var glow_rect := visual_rect.grow(8.0)
	_ck("%s/%s visual dimensions plausible" % [career, station_id],
		visual_size.x >= 48.0 and visual_size.y >= 48.0
		and visual_size.x <= 220.0 and visual_size.y <= 220.0)
	_ck("%s/%s touch target >=110px" % [career, station_id],
		hotspot_size.x >= MIN_TOUCH_TARGET
		and hotspot_size.y >= MIN_TOUCH_TARGET)
	_ck("%s/%s hit bounds in room" % [career, station_id],
		_rect_inside(SCREEN_BOUNDS, hit_rect))
	_ck("%s/%s visual and glow bounds in hit target" % [career, station_id],
		_rect_inside(hit_rect, visual_rect)
		and _rect_inside(hit_rect, glow_rect)
		and _rect_inside(SCREEN_BOUNDS, glow_rect))

	_ck("%s/%s station spur exists" % [career, station_id],
		not spur.is_empty())
	if not spur.is_empty():
		_ck("%s/%s spur reaches approach" % [career, station_id],
			spur[spur.size() - 1].distance_to(approach_pos)
				<= POSITION_TOLERANCE)
		_ck("%s/%s spur points and segments approved" % [career, station_id],
			StagePaths.route_is_approved(
				career, spur, ROUTE_TOLERANCE))
	if bool(record.get("authored_spur", false)):
		authored_spur_count += 1
		_ck("%s/%s raised object has safe distinct approach" \
				% [career, station_id],
			spur.size() >= 2 and object_pos.distance_to(approach_pos) >= 4.0)

	var forward := StagePaths.player_route_to_station(
		career, start, station_id)
	_route_contract(career, "%s forward" % station_id,
		forward, approach_pos)
	var reverse := StagePaths.player_route_to_point(
		career, approach_pos, start)
	_route_contract(career, "%s reverse" % station_id,
		reverse, start)


func _audit_playable_phase_binding(career: String, station_id: String,
		phase_number: int) -> void:
	playable_phase_count += 1
	var label := "%s/phase_%d/%s" % [career, phase_number, station_id]
	var record: Dictionary = StagePaths.station_by_id(career, station_id)
	_ck("%s resolves explicit station" % label, not record.is_empty())
	if record.is_empty():
		return
	_ck("%s has painted semantic object anchor" % label,
		bool(record.get("authored_object", false)))
	_ck("%s has authored safe approach" % label,
		bool(record.get("authored_spur", false)))
	var object_pos: Vector2 = StagePaths.station_object_position(
		career, station_id)
	var approach_pos: Vector2 = StagePaths.station_approach(career, station_id)
	var visual_size: Vector2 = StagePaths.station_visual_size(career, station_id)
	var visual_rect := Rect2(object_pos - visual_size * 0.5, visual_size)
	var body_rect := _roshan_body_at(approach_pos)
	_ck("%s object and approach are distinct" % label,
		object_pos.distance_to(approach_pos) >= 24.0)
	_ck("%s complete hotspot visual remains on-screen" % label,
		_rect_inside(SCREEN_BOUNDS, visual_rect))
	_ck("%s idle Roshan clears hotspot visual" % label,
		not body_rect.intersects(visual_rect))


func _audit_projection(career: String, start: Vector2,
		target: Vector2, label: String) -> void:
	_ck("%s/%s raw touch is off route" % [career, label],
		not StagePaths.point_is_on_approved_route(
			career, target, ROUTE_TOLERANCE))
	var projection: Dictionary = StagePaths.nearest_approved_point(
		career, target)
	_ck("%s/%s projection exists" % [career, label],
		not projection.is_empty())
	if projection.is_empty():
		return
	var point: Vector2 = projection.get("point", Vector2(-1.0, -1.0))
	_ck("%s/%s projection differs from raw touch" % [career, label],
		point.distance_to(target) >= 20.0
		and float(projection.get("distance", 0.0)) >= 20.0)
	_ck("%s/%s projection is approved and in room" % [career, label],
		SCREEN_BOUNDS.has_point(point)
		and StagePaths.point_is_on_approved_route(
			career, point, POSITION_TOLERANCE))
	var route := StagePaths.player_route_to_point(career, start, target)
	_route_contract(career, "%s projected route" % label, route, point)


func _audit_career(career: String) -> void:
	var expected: Array = EXPECTED_STATIONS.get(career, [])
	var records: Array[Dictionary] = StagePaths.stations(career)
	var actual_ids: Array[String] = []
	for record: Dictionary in records:
		actual_ids.append(String(record.get("id", "")))
	_ck("%s station IDs exact and ordered" % career,
		actual_ids == expected)
	var unique_ids: Dictionary = {}
	var all_explicit := true
	for station_id: String in actual_ids:
		unique_ids[station_id] = true
		all_explicit = all_explicit and not station_id.is_empty() \
			and not station_id.begins_with("station_")
	_ck("%s station IDs unique and authored" % career,
		unique_ids.size() == expected.size() and all_explicit)

	var spine := StagePaths.path_points(career)
	_ck("%s authored spine has bends" % career, spine.size() >= 3)
	_ck("%s approved branches expose spine first" % career,
		String(StagePaths.approved_route_branches(career)[0].get(
			"id", "")) == "__spine")
	var start := spine[0]
	var finish := spine[spine.size() - 1]
	var forward := StagePaths.player_route_to_point(career, start, finish)
	_route_contract(career, "full spine forward", forward, finish)
	_ck("%s forward preserves every spine vertex" % career,
		_contains_points_in_order(forward, spine))
	var reverse := StagePaths.player_route_to_point(career, finish, start)
	_route_contract(career, "full spine reverse", reverse, start)
	_ck("%s reverse preserves every spine vertex" % career,
		_contains_points_in_order(reverse, _reversed(spine)))

	var chord := PackedVector2Array([start, finish])
	_ck("%s spine is materially curved" % career,
		_max_distance_from_chord(spine) > ROUTE_TOLERANCE * 2.0)
	_ck("%s rejects straight-chord shortcut" % career,
		not StagePaths.route_is_approved(career, chord, ROUTE_TOLERANCE))

	for station_id: String in expected:
		_audit_station(career, station_id, start)
	var playable: Array = PLAYABLE_PHASE_STATIONS.get(career, [])
	for phase_number in range(playable.size()):
		_audit_playable_phase_binding(
			career, String(playable[phase_number]), phase_number)
	_audit_projection(career, start,
		Vector2(StagePaths.SCREEN.x * 0.37, -180.0), "offscreen above")
	_audit_projection(career, finish,
		Vector2(StagePaths.SCREEN.x * 0.71,
			StagePaths.SCREEN.y + 180.0), "offscreen below")


func _init() -> void:
	_ck("exactly 14 careers covered", EXPECTED_STATIONS.size() == 14)
	_ck("playable bindings cover same 14 careers",
		PLAYABLE_PHASE_STATIONS.size() == 14)
	for career: String in EXPECTED_STATIONS:
		_audit_career(career)
	_ck("all 68 authored stations covered", station_count == 68,
		"actual=%d" % station_count)
	_ck("all raised-landmark exceptions exercised",
		authored_spur_count >= 8,
		"actual=%d" % authored_spur_count)
	_ck("all 57 playable phase anchors exercised",
		playable_phase_count == 57,
		"actual=%d" % playable_phase_count)
	var result := "ALL OK" if failed == 0 else "%d FAIL" % failed
	print(("OPERA_DIEGETIC_PATHS|result: %s (%d checks, %d careers, " \
		+ "%d stations, %d playable phases, %d authored spurs)") % [
		result,
		checks,
		EXPECTED_STATIONS.size(),
		station_count,
		playable_phase_count,
		authored_spur_count,
	])
	quit(0 if failed == 0 else 1)
