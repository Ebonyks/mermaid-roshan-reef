extends SceneTree
## Review-only export of the live Opera navigation contract.
##
## This intentionally consumes the same StagePaths records used by the world.
## It emits geometry and simple SVG overlays for human review; it never writes
## runtime assets or changes approved art.

const StagePaths := preload("res://scripts/opera_stage_paths.gd")
const CareerWorld := preload("res://scripts/opera_career_world_2d.gd")
const CastleRooms := preload("res://scripts/arena/castle_rooms_25d.gd")

const HTML_START := "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Stage navigation review</title><style>body{margin:32px auto;padding:0 24px;max-width:1280px;background:#14213a;color:#edf7ff;font:16px/1.5 system-ui,sans-serif}h1{font-size:32px;line-height:1.2}p{max-width:850px;color:#c5d7eb}a{color:#8eeeff}ul{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}li{padding:16px;background:#213551;border:1px solid #3c526e;border-radius:12px}li a{display:inline-block;padding:4px 0}object{max-width:100%;height:auto;aspect-ratio:16/9}small{color:#ffdca0}</style></head><body>"

const CAREERS: Array[String] = [
	"chef", "detective", "ballerina", "candymaker", "doctor", "farmer",
	"boxer", "magician", "painter", "astronaut", "racer", "popstar",
	"nursery", "geologist", "teacher",
]
const VARIANTS: Array[Dictionary] = [
	{"career": "ballerina", "variant": "stuffie_room", "kind": "chapter2_room"},
	{"career": "farmer", "variant": "sky_lagoon_farmer", "kind": "chapter2_lagoon"},
]
const REVIEW_ROOT := "res://audit/stage_pathfinding/reproductions"
const JSON_PATH := "res://audit/stage_pathfinding/opera_geometry.json"
const CASTLE_JSON_PATH := "res://audit/stage_pathfinding/castle_geometry.json"
const CASTLE_REVIEW_ROOT := "res://audit/stage_pathfinding/reproductions/castle"
const CASTLE_IDS: Array[String] = ["main_hall", "opera_hall", "kitchen", "library", "playroom", "craft_room", "mermaid_pool", "bubble_bath", "dining_room", "royal_bedroom", "sleepover_bedroom", "movie_lounge", "family_gallery"]

func _vec(value: Vector2) -> Array[float]:
	return [value.x, value.y]


func _points(points: PackedVector2Array) -> Array:
	var out: Array = []
	for point: Vector2 in points:
		out.append(_vec(point))
	return out


func _record(record: Dictionary) -> Dictionary:
	var out: Dictionary = {}
	for key: String in [
		"id", "landmark", "authored_object", "authored_spur", "spine_t",
	]:
		if record.has(key):
			out[key] = record[key]
	for key: String in ["pos", "object_pos", "approach_pos"]:
		if record.get(key, null) is Vector2:
			out[key] = _vec(record[key] as Vector2)
	for key: String in ["visual_size", "hotspot_size"]:
		if record.get(key, null) is Vector2:
			out[key] = _vec(record[key] as Vector2)
	for key: String in ["spur", "route"]:
		if record.get(key, null) is PackedVector2Array:
			out[key] = _points(record[key] as PackedVector2Array)
	return out


func _backdrop(career: String, variant: String) -> Dictionary:
	if career == "teacher":
		return {"mode": "room_tiles", "assets": _grid_assets("assets/flats/castle/interactions_v4/background_tiles/room_library_background_r%d_c%d.png", 4, 2), "source": "OperaWorldBackdrop2D._draw_stuffie_room_tiles", "provenance": "approved repository art; see ASSET_LICENSES.md"}
	if variant == "stuffie_room":
		return {"mode": "room_tiles", "assets": _grid_assets("assets/flats/castle/rooms/background_tiles/room_playroom_background_r%d_c%d.png", 4, 2), "source": "OperaWorldBackdrop2D._draw_stuffie_room_tiles", "provenance": "approved repository art; see ASSET_LICENSES.md"}
	if variant == "sky_lagoon_farmer":
		return {"mode": "sky_lagoon_crop", "assets": _grid_assets("assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png", 4, 2, 2), "source_crop": [0, 224, 1024, 576], "source": "OperaWorldBackdrop2D._draw_sky_lagoon_farmer", "provenance": "approved repository art; see ASSET_LICENSES.md"}
	return {
		"mode": "painted_world",
		"painting_reference": "assets/opera/worlds/backdrops/world_%s.png" % career,
		"world_assets": _career_grid_assets("world", career),
		"stage_assets": _career_grid_assets("stage", career),
		"source": "OperaWorldBackdrop2D._draw_tile_set (source_y=448 top row, 0 bottom row)",
		"provenance": "approved repository art; see ASSET_LICENSES.md",
	}


func _grid_assets(pattern: String, columns: int, rows: int,
		column_offset: int = 0) -> Array:
	var assets: Array = []
	for row in range(rows):
		for column in range(columns):
			var path := pattern % [row, column + column_offset]
			var absolute := ProjectSettings.globalize_path("res://" + path)
			assets.append({"path": path, "sha256": FileAccess.get_sha256(absolute) if FileAccess.file_exists(absolute) else "MISSING"})
	return assets


func _career_grid_assets(kind: String, career: String) -> Array:
	var assets: Array = []
	for row in range(2):
		for column in range(2):
			var path := "assets/opera/worlds/stage/finale_stage_c%dr%d.png" % [column, row] if kind == "stage" and career == "ballerina" else "assets/opera/worlds/backdrops/%s_%s_c%dr%d.png" % [kind, career, column, row]
			var absolute := ProjectSettings.globalize_path("res://" + path)
			assets.append({"path": path, "sha256": FileAccess.get_sha256(absolute) if FileAccess.file_exists(absolute) else "MISSING"})
	return assets


func _live_navigation(career: String, variant: String) -> Dictionary:
	var world := CareerWorld.new()
	world.career_id = career
	world.config = {"chapter2_scene": variant}
	world._configure_stage_paths()
	var snapshot := world.navigation_snapshot()
	world.free()
	return snapshot


func _variant_entry(career: String, variant: String, kind: String, stage_mode: bool) -> Dictionary:
	var navigation := _live_navigation(career, variant)
	var stage_points: PackedVector2Array = navigation.get("path", PackedVector2Array()) as PackedVector2Array
	var stations: Array[Dictionary] = navigation.get("stations", []) as Array[Dictionary]
	var station_data: Array = []
	for station: Dictionary in stations:
		station_data.append(_record(station))
	return {
		"career": career, "scene_variant": variant, "variant_kind": kind,
		"stage_mode": stage_mode, "viewport": [1280, 720],
		"coordinate_space": "frozen 1280x720 root; canvas scaled by runtime",
		"backdrop": _backdrop(career, variant),
		"path": _points(stage_points), "stations": station_data,
		"out_of_bounds": "complement of 112px spine / 96px spur visualization corridor; runtime movement follows centerline",
	}


func _svg(entry: Dictionary) -> String:
	var career := String(entry["career"])
	var variant := String(entry["scene_variant"])
	var suffix := "_%s" % variant if not variant.is_empty() else ""
	var title := "%s%s | stage_mode=%s" % [career, suffix, str(entry["stage_mode"])]
	var body := "<rect width='1280' height='720' fill='#17214d'/>"
	var backdrop: Dictionary = entry.get("backdrop", {}) as Dictionary
	var mode := String(backdrop.get("mode", ""))
	var assets: Array = backdrop.get("assets", []) as Array
	if mode == "painted_world":
		var key := "stage_assets" if bool(entry["stage_mode"]) else "world_assets"
		assets = backdrop.get(key, []) as Array
		var available := true
		for asset_value: Variant in assets:
			available = available and String((asset_value as Dictionary).get("sha256", "MISSING")) != "MISSING"
		if not available:
			if bool(entry["stage_mode"]):
				body += "<text x='24' y='62' fill='#ffd66e' font-size='16'>No authored stage tile set: runtime resolves world tiles</text>"
				assets = backdrop.get("world_assets", []) as Array
				available = true
				for fallback_value: Variant in assets:
					available = available and String((fallback_value as Dictionary).get("sha256", "MISSING")) != "MISSING"
			else:
				body += "<text x='24' y='62' fill='#ffd66e' font-size='16'>No authored tile set: runtime uses vector fallback</text>"
		var tile_count := assets.size() if available else 0
		for index in range(tile_count):
			var tile: Dictionary = assets[index] as Dictionary
			var col := index % 2
			var row := index / 2
			var source_y := 448 if row == 0 else 0
			body += "<svg x='%s' y='%s' width='640' height='360' viewBox='0 %s 1024 576' preserveAspectRatio='none'><image href='../../../%s' width='1024' height='1024'/></svg>" % [col * 640, row * 360, source_y, tile.get("path", "")]
	else:
		for index in range(assets.size()):
			var tile: Dictionary = assets[index] as Dictionary
			var col := index % 4 if mode == "room_tiles" else index % 2
			var row := index / 4 if mode == "room_tiles" else index / 2
			var width := 320 if mode == "room_tiles" else 640
			var height := 360
			if mode == "sky_lagoon_crop":
				body += "<svg x='%s' y='%s' width='640' height='360' viewBox='0 224 1024 576' preserveAspectRatio='none'><image href='../../../%s' width='1024' height='1024'/></svg>" % [col * 640, row * 360, tile.get("path", "")]
			else:
				body += "<image href='../../../%s' x='%s' y='%s' width='%s' height='%s' preserveAspectRatio='none'/>" % [tile.get("path", ""), col * width, row * height, width, height]
	body += "<text x='24' y='34' fill='white' font-size='22'>%s</text>" % title
	var points: Array = entry["path"] as Array
	var coords := ""
	for point: Array in points:
		coords += "%s,%s " % [point[0], point[1]]
	body += "<polyline points='%s' fill='none' stroke='#55e6ff' stroke-width='10' stroke-linecap='round' stroke-linejoin='round'/>" % coords
	# Tint the complement of a generous route corridor as OOB. This makes the
	# access protocol visible without pretending the viewport border is the map.
	body += "<defs><mask id='routeMask'><rect width='1280' height='720' fill='white'/><polyline points='%s' fill='none' stroke='black' stroke-width='112' stroke-linecap='round' stroke-linejoin='round'/>" % coords
	for station: Dictionary in entry["stations"]:
		var spur: Array = station.get("spur", []) as Array
		var spur_coords := ""
		for spur_point: Array in spur:
			spur_coords += "%s,%s " % [spur_point[0], spur_point[1]]
		if not spur_coords.is_empty():
			body += "<polyline points='%s' fill='none' stroke='black' stroke-width='96' stroke-linecap='round' stroke-linejoin='round'/>" % spur_coords
	body += "</mask></defs><rect width='1280' height='720' fill='#ff365e' opacity='.22' mask='url(#routeMask)'/>"
	for station: Dictionary in entry["stations"]:
		var approach: Array = station.get("approach_pos", [640, 360]) as Array
		var object: Array = station.get("object_pos", approach) as Array
		var spur: Array = station.get("spur", []) as Array
		var spur_coords := ""
		for spur_point: Array in spur:
			spur_coords += "%s,%s " % [spur_point[0], spur_point[1]]
		if not spur_coords.is_empty():
			body += "<polyline points='%s' fill='none' stroke='#55e6ff' stroke-width='8' stroke-linecap='round' stroke-linejoin='round'/>" % spur_coords
		body += "<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='#ffd66e' stroke-width='3' stroke-dasharray='8 6'/><circle cx='%s' cy='%s' r='11' fill='#ff77b7'/><circle cx='%s' cy='%s' r='8' fill='#fff3a6'/><text x='%s' y='%s' fill='white' font-size='15'>%s</text>" % [approach[0], approach[1], object[0], object[1], approach[0], approach[1], object[0], object[1], approach[0] + 12, approach[1] - 12, station.get("id", "station")]
	body += "<text x='24' y='700' fill='#ffb3c1' font-size='16'>RED = outside buffered walkable lanes/spurs; CYAN = route/spurs; YELLOW = approach to object</text>"
	return "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1280 720'>%s</svg>" % body


func _write(path: String, content: String) -> void:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("Could not write %s" % path)
		return
	file.store_string(content)


func _rect(value: Rect2) -> Array[float]:
	return [value.position.x, value.position.y, value.size.x, value.size.y]


func _json_value(value: Variant) -> Variant:
	if value is Vector2:
		return _vec(value as Vector2)
	if value is Vector2i:
		var vector := value as Vector2i
		return [vector.x, vector.y]
	if value is Rect2:
		return _rect(value as Rect2)
	if value is PackedVector2Array:
		return _points(value as PackedVector2Array)
	if value is Dictionary:
		var dictionary: Dictionary = value as Dictionary
		var converted: Dictionary = {}
		for key_value: Variant in dictionary:
			converted[String(key_value)] = _json_value(dictionary[key_value])
		return converted
	if value is Array:
		var converted_array: Array = []
		for element: Variant in value as Array:
			converted_array.append(_json_value(element))
		return converted_array
	return value


func _castle_entry(snapshot: Dictionary) -> Dictionary:
	var entry: Dictionary = _json_value(snapshot) as Dictionary
	entry["viewport"] = [1280, 720]
	entry["coordinate_space"] = \
		"live CastleRooms25D navigation_snapshot; canvas scaled by runtime"
	entry["out_of_bounds"] = \
		"complement of buffered live navigation branches; runtime follows centerlines"
	entry["provenance"] = \
		"live composed Castle room, approved repository art; see ASSET_LICENSES.md"
	for background_value: Variant in entry.get("backgrounds", []) as Array:
		var background: Dictionary = background_value as Dictionary
		var texture_path := String(background.get("texture_path", ""))
		var absolute := ProjectSettings.globalize_path(texture_path)
		background["sha256"] = FileAccess.get_sha256(absolute) \
			if FileAccess.file_exists(absolute) else "MISSING"
	for item_value: Variant in entry.get("items", []) as Array:
		var item: Dictionary = item_value as Dictionary
		var texture_path := String(item.get("texture_path", ""))
		var absolute := ProjectSettings.globalize_path(texture_path)
		item["sha256"] = FileAccess.get_sha256(absolute) \
			if FileAccess.file_exists(absolute) else "MISSING"
	return entry


func _castle_point_to_stage(entry: Dictionary, value: Array,
		coordinate_space: String) -> Vector2:
	var point := Vector2(float(value[0]), float(value[1]))
	if coordinate_space == "stage":
		return point
	var scale := float(entry.get("art_to_stage_scale", 1.0))
	var view_left := float(entry.get("art_view_left", 0.0))
	return Vector2((point.x - view_left) * scale, point.y * scale)


func _castle_rect_to_stage(entry: Dictionary, value: Array,
		coordinate_space: String) -> Rect2:
	var top_left := _castle_point_to_stage(
		entry, [value[0], value[1]], coordinate_space)
	if coordinate_space == "stage":
		return Rect2(top_left, Vector2(float(value[2]), float(value[3])))
	var scale := float(entry.get("art_to_stage_scale", 1.0))
	return Rect2(top_left, Vector2(float(value[2]), float(value[3])) * scale)


func _castle_svg(entry: Dictionary) -> String:
	var body := "<rect width='1280' height='720' fill='#17214d'/>"
	var art_space := String(entry.get("art_coordinate_space", "room_art"))
	var navigation_space := String(entry.get(
		"navigation_coordinate_space", "stage"))
	for background_value: Variant in entry.get("backgrounds", []) as Array:
		var tile: Dictionary = background_value as Dictionary
		var render_value: Array = tile.get("render_art_rect", []) as Array
		if render_value.size() != 4:
			continue
		var render_rect := _castle_rect_to_stage(entry, render_value, art_space)
		var texture_path := String(tile.get("texture_path", "")).trim_prefix("res://")
		body += "<image href='../../../../%s' x='%s' y='%s' width='%s' height='%s' preserveAspectRatio='none'/>" % [texture_path, render_rect.position.x, render_rect.position.y, render_rect.size.x, render_rect.size.y]
	# Draw each visible live Sprite2D from its current atlas cell. The nested SVG
	# viewBox performs the same non-destructive sheet crop as Sprite2D h/v frames.
	for item_value: Variant in entry.get("items", []) as Array:
		var item: Dictionary = item_value as Dictionary
		if not bool(item.get("visible", true)):
			continue
		var placement_value: Array = item.get(
			"full_render_art_rect", []) as Array
		var frame_value: Array = item.get("atlas_frame_rect", []) as Array
		var texture_size: Array = item.get("native_texture_size", []) as Array
		if placement_value.size() != 4 or frame_value.size() != 4 \
				or texture_size.size() != 2:
			continue
		var placement := _castle_rect_to_stage(
			entry, placement_value, art_space)
		var texture_path := String(item.get(
			"texture_path", "")).trim_prefix("res://")
		var fixture_svg := "<svg x='%s' y='%s' width='%s' height='%s' viewBox='%s %s %s %s' preserveAspectRatio='none' overflow='hidden'><image href='../../../../%s' width='%s' height='%s'/></svg>" % [placement.position.x, placement.position.y, placement.size.x, placement.size.y, frame_value[0], frame_value[1], frame_value[2], frame_value[3], texture_path, texture_size[0], texture_size[1]]
		if bool(item.get("flip_h", false)):
			body += "<g transform='translate(%s 0) scale(-1 1)'>%s</g>" % [2.0 * placement.position.x + placement.size.x, fixture_svg]
		else:
			body += fixture_svg
	body += "<text x='24' y='34' fill='white' stroke='#17214d' stroke-width='4' paint-order='stroke' font-size='22'>Castle %s | live room composition</text>" % entry["room_id"]
	var route_polylines: Array[String] = []
	for lane: Array in entry["lanes"]:
		var coords := ""
		for point: Array in lane:
			var stage_point := _castle_point_to_stage(
				entry, point, navigation_space)
			coords += "%s,%s " % [stage_point.x, stage_point.y]
		route_polylines.append(coords)
		body += "<polyline points='%s' fill='none' stroke='#55e6ff' stroke-width='8' opacity='.9'/>" % coords
	body += "<defs><mask id='castleRouteMask'><rect width='1280' height='720' fill='white'/>"
	for coords: String in route_polylines:
		body += "<polyline points='%s' fill='none' stroke='black' stroke-width='96' stroke-linecap='round' stroke-linejoin='round'/>" % coords
	body += "</mask></defs><rect width='1280' height='720' fill='#ff365e' opacity='.18' mask='url(#castleRouteMask)'/>"
	for blocker: Dictionary in entry["body_footprints"]:
		var blocker_value: Array = blocker.get("rect", []) as Array
		if blocker_value.size() != 4:
			continue
		var blocker_rect := _castle_rect_to_stage(
			entry, blocker_value, "stage")
		body += "<rect x='%s' y='%s' width='%s' height='%s' fill='#ff365e' opacity='.30' stroke='#ffb3c1' stroke-width='2'/><text x='%s' y='%s' fill='white' stroke='#17214d' stroke-width='3' paint-order='stroke' font-size='13'>BLOCK %s</text>" % [blocker_rect.position.x, blocker_rect.position.y, blocker_rect.size.x, blocker_rect.size.y, blocker_rect.position.x + 4.0, blocker_rect.position.y + 18.0, blocker.get("id", "fixture")]
	for item: Dictionary in entry["items"]:
		var contact: Array = item["route_contact"] as Array
		var contact_stage := _castle_point_to_stage(
			entry, contact, navigation_space)
		var fixture_value: Array = item.get("render_art_rect", []) as Array
		var object_stage := contact_stage
		if fixture_value.size() == 4:
			var fixture_rect := _castle_rect_to_stage(
				entry, fixture_value, art_space)
			object_stage = fixture_rect.get_center()
			body += "<rect x='%s' y='%s' width='%s' height='%s' fill='#8f62ff' opacity='.12' stroke='#d4c4ff' stroke-width='2'/>" % [fixture_rect.position.x, fixture_rect.position.y, fixture_rect.size.x, fixture_rect.size.y]
		body += "<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='#ffd66e' stroke-width='3' stroke-dasharray='8 6'/><circle cx='%s' cy='%s' r='10' fill='#ff77b7'/><circle cx='%s' cy='%s' r='8' fill='#fff3a6'/><text x='%s' y='%s' fill='white' stroke='#17214d' stroke-width='3' paint-order='stroke' font-size='13'>%s</text>" % [contact_stage.x, contact_stage.y, object_stage.x, object_stage.y, contact_stage.x, contact_stage.y, object_stage.x, object_stage.y, contact_stage.x + 10.0, contact_stage.y - 10.0, item["id"]]
	body += "<text x='24' y='700' fill='white' stroke='#17214d' stroke-width='4' paint-order='stroke' font-size='15'>CYAN = live route; RED = OOB and body blockers; PURPLE = live fixture bounds; YELLOW = contact socket.</text>"
	return "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1280 720'>%s</svg>" % body


func _init() -> void:
	call_deferred("_run")


func _frames(count: int) -> void:
	for unused: int in range(count):
		await process_frame


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(REVIEW_ROOT))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://audit/stage_pathfinding"))
	var entries: Array = []
	for career: String in CAREERS:
		for stage_mode: bool in [false, true]:
			entries.append(_variant_entry(career, "", "standard", stage_mode))
	for variant_record: Dictionary in VARIANTS:
		for stage_mode: bool in [false, true]:
			entries.append(_variant_entry(String(variant_record["career"]), String(variant_record["variant"]), String(variant_record["kind"]), stage_mode))
	var payload := {"schema": "opera_stage_pathfinding_v1", "generated_by": "scripts/debug_export_stage_pathfinding.gd", "entries": entries}
	_write(JSON_PATH, JSON.stringify(payload, "  "))
	var index := HTML_START + "<small>REVIEW ONLY · HUMAN GEOMETRY AND DEVICE APPROVAL PENDING</small><h1>Stage navigation review</h1><p>34 Opera layout views and 13 Castle rooms reuse the approved art. Cyan marks route centerlines, pink marks approach feet, yellow marks object centers, and red marks excluded space. Diagnostic line widths do not expand the playable route.</p><h2>Opera layouts</h2><ul>"
	for entry: Dictionary in entries:
		var career := String(entry["career"])
		var variant := String(entry["scene_variant"])
		var mode := "stage" if bool(entry["stage_mode"]) else "world"
		var name := career + ("_" + variant if not variant.is_empty() else "") + "_" + mode
		var svg_path := "%s/%s.svg" % [REVIEW_ROOT, name]
		_write(svg_path, _svg(entry))
		var html := HTML_START + "<a href='index.html'>All layouts</a><h1>%s</h1><p>Review reproduction. Original art preserved; geometry and device approval remain pending.</p><object data='%s.svg' type='image/svg+xml' width='1280' height='720'></object></body></html>" % [name.replace("_", " ").capitalize(), name]
		_write("%s/%s.html" % [REVIEW_ROOT, name], html)
		index += "<li><a href='%s.html'>%s</a> (<a href='%s.svg'>SVG</a>)</li>" % [name, name.replace("_", " ").capitalize(), name]
	index += "</ul></body></html>"
	_write("%s/index.html" % REVIEW_ROOT, index)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(CASTLE_REVIEW_ROOT))
	var castle_entries: Array = []
	var castle_index := HTML_START + "<a href='../index.html'>All layouts</a><h1>Castle rooms</h1><p>Live room art, fixture atlas frames, routes, contacts, and exclusion footprints. All 13 rooms are reproduced from the runtime snapshot. Human geometry and device approval remain pending.</p><ul>"
	var main_scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: ReefMain = main_scene.instantiate() as ReefMain
	root.add_child(main)
	await _frames(2)
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		main._launch_from_start_menu(false)
	else:
		main._skip_intro()
	await process_frame
	main._enter_castle_interior_now(false)
	await _frames(2)
	main.day_one_active = false
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	var castle_failures: Array[String] = []
	for room_id: String in CASTLE_IDS:
		rooms.show_room(room_id, false)
		await _frames(2)
		if main.castle_room_id != room_id:
			castle_failures.append("%s opened as %s" % [
				room_id, main.castle_room_id])
			continue
		var snapshot := rooms.navigation_snapshot()
		var entry := _castle_entry(snapshot)
		castle_entries.append(entry)
		var svg_name := "%s.svg" % room_id
		_write("%s/%s" % [CASTLE_REVIEW_ROOT, svg_name], _castle_svg(entry))
		castle_index += "<li><a href='%s'>%s</a></li>" % [svg_name, room_id.replace("_", " ").capitalize()]
	castle_index += "</ul></body></html>"
	_write("%s/index.html" % REVIEW_ROOT, index.replace("</ul></body></html>", "</ul><h2>Castle rooms</h2><a href='castle/index.html'>Open Castle atlas</a></body></html>"))
	_write("%s/index.html" % CASTLE_REVIEW_ROOT, castle_index)
	_write(CASTLE_JSON_PATH, JSON.stringify({"schema": "castle_stage_pathfinding_v1", "entries": castle_entries}, "  "))
	main.queue_free()
	await process_frame
	var counts_ok := entries.size() == 34 and castle_entries.size() == 13
	if not castle_failures.is_empty() or not counts_ok:
		push_error("Stage path export incomplete: opera=%d castle=%d failures=%s" % [entries.size(), castle_entries.size(), castle_failures])
		quit(1)
		return
	print("OPERA_STAGE_PATH_EXPORT|opera=%d|castle=%d|json=%s|review=%s" % [entries.size(), castle_entries.size(), JSON_PATH, REVIEW_ROOT])
	quit(0)
