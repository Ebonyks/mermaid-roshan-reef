extends SceneTree
# Structural and visual acceptance probe for the picture-first Pearl Castle.
# The historical filename remains so CI callers do not change, but modeled
# pearl-kit geometry is now a regression: world art must remain Sprite3D. The
# Main Hall tiles are opaque, unshaded Sprite3D cards; practical fixtures use
# HDR emission and the shared Environment for touch-controlled bloom.

const ROOM_IDS: Array[String] = [
	"main_hall", "opera_hall", "kitchen", "library", "playroom",
	"craft_room", "mermaid_pool", "bubble_bath",
]
const HALL_DESTINATION_IDS: Array[String] = [
	"family_gallery", "opera_hall", "kitchen", "library", "playroom",
	"craft_room", "mermaid_pool", "bubble_bath",
]
const HALL_SIGN_FILES := {
	"family_gallery": "sign_family_gallery.png",
	"opera_hall": "sign_opera_hall.png",
	"library": "sign_library.png",
	"kitchen": "sign_kitchen.png",
	"playroom": "sign_playroom.png",
	"craft_room": "sign_craft_room.png",
	"mermaid_pool": "sign_mermaid_pool.png",
	"bubble_bath": "sign_bubble_bath.png",
}
const FAMILY_SIGN_SHA256 := \
	"222d5a5a4c590b6ae951ff5d7f4431bd35ed539e48cf0346a2e31fd83a09a0dd"
const PLAYROOM_SIGN_SHA256 := \
	"22d9a3df8eda3b95ae93250165a64a947b4157a70b4405f90dc4d600edccd7df"
const FAMILY_SIGN_ALPHA_RECT := Rect2i(77, 72, 101, 112)
const PLAYROOM_SIGN_ALPHA_RECT := Rect2i(77, 83, 102, 90)
const HALL_SIGN_REUSE_MANIFEST := \
	"res://assets_src/imagegen/castle_main_hall_redraw_2026-08-03/" \
	+ "sign_reuse_manifest.json"
const HALL_SIGN_REUSE_MANIFEST_SHA256 := \
	"a6d0c762af29f11ca684b741a91235ad5e9aa027eff278cc4a360ec835642101"
const HALL_TILE_COLUMNS := 8
const HALL_TILE_ROWS := 2
const HALL_TILE_COUNT := HALL_TILE_COLUMNS * HALL_TILE_ROWS
const HALL_NATIVE_SIZE := Vector2(7280.0, 2048.0)
const HALL_LOGICAL_SIZE := Vector2(3344.0, 941.0)
const HALL_SCREEN_NATIVE_WIDTH := 3640.0
const HALL_TILE_NATIVE_HEIGHT := 1024.0
const HALL_TILE_NATIVE_WIDTHS: Array[int] = [
	910, 910, 910, 910, 910, 910, 910, 910,
]
const HALL_NATIVE_TO_LOGICAL := HALL_LOGICAL_SIZE / HALL_NATIVE_SIZE
const ROYAL_HALL_PORTAL_ID := "__royal_hall"
const ROYAL_HALL_MIST_TEXTURE := \
	"res://assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png"
const ROYAL_HALL_MIST_TEXTURE_SHA256 := \
	"ff0c49869ff0152323282b0228c2f76494ad2381ba64c0e535a68c8bc229e007"
const ROYAL_HALL_MIST_ALPHA_RECT := Rect2i(1, 1, 44, 254)
const ROYAL_HALL_MIST_SPECS: Array[Dictionary] = [
	{"pos": Vector2(2935.0, 385.0), "scale": 1.38, "z": 0.40,
		"alpha": 0.22},
	{"pos": Vector2(2990.0, 365.0), "scale": 1.55, "z": 0.42,
		"alpha": 0.27},
	{"pos": Vector2(3045.0, 405.0), "scale": 1.62, "z": 0.44,
		"alpha": 0.30},
	{"pos": Vector2(3100.0, 370.0), "scale": 1.48, "z": 0.46,
		"alpha": 0.26},
	{"pos": Vector2(3155.0, 400.0), "scale": 1.32, "z": 0.48,
		"alpha": 0.21},
]
const ELEVATOR_ROOM_IDS: Array[String] = [
	"main_hall", "opera_hall", "kitchen", "library",
	"playroom", "craft_room", "mermaid_pool", "bubble_bath",
	"dining_room", "royal_bedroom", "sleepover_bedroom", "movie_lounge",
]
const ELEVATOR_ICON_MANIFEST := \
	"res://assets/ui/castle_room_buttons_v2/elevator_picture_icon_manifest.json"
const INTERACTION_MANIFEST := \
	"res://assets/flats/castle/interactions_v3/castle_interactions_v3.json"
const LEGACY_INTERACTION_MANIFEST := \
	"res://assets/flats/castle/interactions/castle_interactions.json"
const EXPECTED_PHYSICAL_ITEM_COUNTS := {
	"main_hall": 13,
	"opera_hall": 8,
	"kitchen": 14,
	"library": 8,
	"playroom": 8,
	"craft_room": 8,
	"mermaid_pool": 8,
	"bubble_bath": 8,
}
const EXPECTED_ACTIVE_MANIFEST_ASSET_COUNT := 66
const EXPECTED_ACTIVE_MANIFEST_INSTANCE_COUNT := 71
const EXPECTED_V2_BASE_ASSET_COUNT := 28
const EXPECTED_V3_ADDITION_COUNT := 38
const EXPECTED_LEGACY_POOL_ASSET_COUNT := 4
const EXPECTED_OVERALL_UNIQUE_ASSET_COUNT := 70
const EXPECTED_OVERALL_PHYSICAL_ITEM_COUNT := 75
const EXPECTED_ACTIVE_SHADER_WATER_COUNT := 10
const EXPECTED_OVERALL_WATER_INTERACTION_COUNT := 14
const EXPECTED_JOLT_FIXTURE_COUNT := 8
const ROOM_DECODED_TEXTURE_BUDGET_BYTES := 24 * 1024 * 1024
const ROSHAN_ANCHORS := preload("res://scripts/roshan_sprite_anchors.gd")
const ROSHAN_FRAMES := preload("res://scripts/roshan_sprite_frames.gd")
const PLAYER_SCRIPT := preload("res://scripts/player.gd")

var main: ReefMain
var checks_failed := 0
var royal_hall_probe_entry_calls := 0
var royal_hall_probe_consumed_before_entry := false

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("CASTLE_ART|", label, "|", "OK" if ok else "FAIL", "|", detail)

func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame

func _on_royal_hall_probe_entry() -> void:
	royal_hall_probe_entry_calls += 1
	royal_hall_probe_consumed_before_entry = \
		main.castle_royal_hall_event_id.is_empty() \
		and not main.castle_royal_hall_event_entry.is_valid()

# The authored PNG, read straight off disk so the measurement is independent
# of whatever the importer decided to do with the sheet.
func _sheet_image(texture: Texture2D) -> Image:
	var image: Image = Image.load_from_file(
		ProjectSettings.globalize_path(texture.resource_path))
	if image == null:
		image = texture.get_image()
	if image != null and image.is_compressed():
		image.decompress()
	if image != null and image.is_compressed():
		return null
	return image

# Share of lit pixels inside a texture-space window, sampled on a 4px lattice.
func _alpha_coverage(image: Image, rect: Rect2) -> float:
	if image == null:
		return 0.0
	var lit := 0
	var total := 0
	var y := int(rect.position.y)
	while y < int(rect.position.y + rect.size.y):
		var x := int(rect.position.x)
		while x < int(rect.position.x + rect.size.x):
			if x >= 0 and y >= 0 \
					and x < image.get_width() and y < image.get_height():
				total += 1
				if image.get_pixel(x, y).a > 0.03:
					lit += 1
			x += 4
		y += 4
	return 0.0 if total == 0 else float(lit) / float(total)

func _alpha_visible_rect(image: Image, threshold: float = 0.03) -> Rect2i:
	if image == null:
		return Rect2i()
	var minimum := Vector2i(image.get_width(), image.get_height())
	var maximum := Vector2i(-1, -1)
	for y: int in range(image.get_height()):
		for x: int in range(image.get_width()):
			if image.get_pixel(x, y).a <= threshold:
				continue
			minimum.x = mini(minimum.x, x)
			minimum.y = mini(minimum.y, y)
			maximum.x = maxi(maximum.x, x)
			maximum.y = maxi(maximum.y, y)
	if maximum.x < minimum.x or maximum.y < minimum.y:
		return Rect2i()
	return Rect2i(minimum, maximum - minimum + Vector2i.ONE)

# Every frame of every 2.5D sheet must actually reach the screen.
#
# Sprite3D does not ignore hframes/vframes when a region is set: it divides
# region_rect by the grid and adds the frame offset itself. A per-frame window
# handed over as a single cell therefore shrank the quad to one sub-cell and
# sampled the wrong corner of it -- the castle showed no Roshan at all (the
# sampled corner was 0% alpha) and the Sky Lagoon showed a rectangular sliver
# of her hair (owner report 2026-08-02). Assert what the ENGINE will sample,
# not what the table intends, and that authored art lands inside it.
func _check_roshan_sampling_windows() -> void:
	var sheets: Dictionary = PLAYER_SCRIPT.ROSHAN_25D_SHEETS
	var gate := Sprite3D.new()
	var mismatched := 0
	var thin := 0
	var unreadable := 0
	var checked := 0
	var worst_coverage := 1.0
	var worst_label := ""
	var first_mismatch := ""
	for sheet_name: String in sheets.keys():
		var spec: Array = sheets[sheet_name]
		var texture: Texture2D = spec[0] as Texture2D
		var cols: int = int(spec[1])
		var rows: int = int(spec[2])
		var image: Image = _sheet_image(texture)
		if image == null:
			unreadable += 1
		gate.texture = texture
		gate.hframes = cols
		gate.vframes = rows
		for frame_index: int in range(cols * rows):
			gate.frame = frame_index
			ROSHAN_FRAMES.apply_region(gate, sheet_name, frame_index, cols)
			var intended: Rect2 = ROSHAN_FRAMES.region(
				sheet_name, frame_index, cols)
			var sampled: Rect2 = ROSHAN_FRAMES.sampled_rect(gate)
			checked += 1
			if not sampled.is_equal_approx(intended):
				mismatched += 1
				if first_mismatch.is_empty():
					first_mismatch = "%s[%d] sampled=%s intended=%s" % [
						sheet_name, frame_index, sampled, intended]
			if image == null:
				continue
			var coverage: float = _alpha_coverage(image, sampled)
			if coverage < worst_coverage:
				worst_coverage = coverage
				worst_label = "%s[%d]" % [sheet_name, frame_index]
			if coverage < 0.10:
				thin += 1
	gate.free()
	_ck("roshan_frames_sample_their_own_window",
		mismatched == 0 and checked == 128,
		"checked=%d off_window=%d %s" % [checked, mismatched, first_mismatch])
	# Lowest measured on the shipped sheets is 17.6% (swim_back[2..4]); the
	# windows this replaced sat at 0.0%. 10% is the floor between them.
	_ck("roshan_frames_render_real_art",
		thin == 0 and unreadable == 0,
		"below_10pct_alpha=%d unreadable_sheets=%d worst=%s at %.1f%%" % [
			thin, unreadable, worst_label, worst_coverage * 100.0])

func _audit_world_node(node: Node, counts: Dictionary) -> void:
	for child: Node in node.get_children():
		if child is Sprite3D:
			counts["sprite3d"] = int(counts.get("sprite3d", 0)) + 1
			var sprite := child as Sprite3D
			if sprite.visible:
				counts["visible_sprite3d"] = int(
					counts.get("visible_sprite3d", 0)) + 1
			if sprite.shaded:
				counts["shaded"] = int(counts.get("shaded", 0)) + 1
			if sprite.texture == null:
				counts["missing_texture"] = int(
					counts.get("missing_texture", 0)) + 1
			if bool(sprite.get_meta("castle_world_sprite3d", false)):
				var source_role: String = String(sprite.get_meta(
					"source_asset_role", ""))
				if source_role == "portal_glow":
					counts["portal_glow"] = int(
						counts.get("portal_glow", 0)) + 1
				var is_opaque_background: bool = \
					source_role == "clean_background_tile"
				var is_soft_depth_mist: bool = \
					source_role == "royal_hall_mist"
				var alpha_ok: bool = (
					not sprite.transparent
					and sprite.alpha_cut == SpriteBase3D.ALPHA_CUT_DISABLED
				) if is_opaque_background else (
					sprite.transparent
					and not sprite.no_depth_test
					and sprite.alpha_cut == SpriteBase3D.ALPHA_CUT_DISABLED
					if is_soft_depth_mist else
					sprite.alpha_cut == SpriteBase3D.ALPHA_CUT_DISABLED
					if source_role == "portal_glow" else
					sprite.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD
					and is_equal_approx(
						sprite.alpha_scissor_threshold, 0.5)
				)
				if not alpha_ok:
					counts["bad_alpha_depth"] = int(
						counts.get("bad_alpha_depth", 0)) + 1
		elif child is MeshInstance3D or child is MultiMeshInstance3D \
				or child is CSGShape3D or child is Decal:
			counts["modeled"] = int(counts.get("modeled", 0)) + 1
		elif child is CanvasItem:
			counts["canvas_world"] = int(
				counts.get("canvas_world", 0)) + 1
		_audit_world_node(child, counts)

func _room_detail_tile_ready(tile: Sprite3D) -> bool:
	var native_size: Vector2 = tile.get_meta(
		"native_texture_size", Vector2.ZERO) as Vector2
	if native_size.x <= 0.0 or native_size.y <= 0.0:
		return false
	var source_rect: Rect2 = tile.get_meta(
		"source_art_rect", Rect2()) as Rect2
	var render_rect: Rect2 = tile.get_meta(
		"render_art_rect", Rect2()) as Rect2
	var overlap_pixels: Vector2i = tile.get_meta(
		"runtime_seam_overlap_pixels", Vector2i(-1, -1)) as Vector2i
	var overlap_logical := Vector2(
		float(overlap_pixels.x) * source_rect.size.x / native_size.x,
		float(overlap_pixels.y) * source_rect.size.y / native_size.y)
	var expected_render_size: Vector2 = source_rect.size + overlap_logical
	return (
		tile.visible
		and tile.texture != null
		and not tile.transparent
		and tile.alpha_cut == SpriteBase3D.ALPHA_CUT_DISABLED
		and tile.texture.get_size() == native_size
		and maxf(native_size.x, native_size.y) <= 1024.0
		and tile.texture.resource_path.contains("rooms/background_tiles/")
		and overlap_pixels.x >= 0 and overlap_pixels.x <= 1
		and overlap_pixels.y >= 0 and overlap_pixels.y <= 1
		and render_rect.position == source_rect.position
		and render_rect.size.is_equal_approx(expected_render_size)
		and is_equal_approx(
			tile.scale.x, render_rect.size.x / source_rect.size.x)
		and is_equal_approx(
			tile.scale.y, render_rect.size.y / source_rect.size.y)
	)

func _hall_native_column_x(column: int) -> float:
	var x := 0.0
	for prior_column: int in range(column):
		x += float(HALL_TILE_NATIVE_WIDTHS[prior_column])
	return x

func _hall_expected_native_size(column: int) -> Vector2:
	return Vector2(
		float(HALL_TILE_NATIVE_WIDTHS[column]), HALL_TILE_NATIVE_HEIGHT)

func _hall_expected_logical_rect(row: int, column: int) -> Rect2:
	var native_position := Vector2(
		_hall_native_column_x(column),
		float(row) * HALL_TILE_NATIVE_HEIGHT)
	var native_size: Vector2 = _hall_expected_native_size(column)
	return Rect2(
		native_position * HALL_NATIVE_TO_LOGICAL,
		native_size * HALL_NATIVE_TO_LOGICAL)

func _hall_runtime_tile_seams_match(tiles: Array[Sprite3D]) -> Dictionary:
	var result := {
		"ok": tiles.size() == HALL_TILE_COUNT,
		"mismatch": "",
		"worst_mean_rgb_delta": 0.0,
	}
	if not bool(result["ok"]):
		result["mismatch"] = "tile_count=%d" % tiles.size()
		return result
	var images: Array[Image] = []
	for tile: Sprite3D in tiles:
		var image: Image = tile.texture.get_image() if tile.texture != null else null
		if image == null or image.is_empty():
			return {"ok": false, "mismatch": "%s:no_image" % tile.name}
		images.append(image)
	for index: int in range(tiles.size()):
		var row: int = index / HALL_TILE_COLUMNS
		var column: int = index % HALL_TILE_COLUMNS
		var tile: Sprite3D = tiles[index]
		var image: Image = images[index]
		var source_rect: Rect2 = tile.get_meta(
			"source_art_rect", Rect2()) as Rect2
		var expected_rect: Rect2 = _hall_expected_logical_rect(row, column)
		if not source_rect.is_equal_approx(expected_rect):
			return {"ok": false,
				"mismatch": "r%d_c%d:logical_rect=%s" % [
					row, column, source_rect]}
		if column < HALL_TILE_COLUMNS - 1:
			var right_image: Image = images[index + 1]
			var right_rect: Rect2 = tiles[index + 1].get_meta(
				"source_art_rect", Rect2()) as Rect2
			if not is_equal_approx(source_rect.end.x, right_rect.position.x):
				return {"ok": false, "mismatch":
					"r%d_c%d:horizontal_geometry_gap" % [row, column]}
			var shared_height := mini(image.get_height(), right_image.get_height())
			var vertical_edge_delta := 0.0
			for y: int in range(shared_height):
				var left_color: Color = image.get_pixel(image.get_width() - 1, y)
				var right_color: Color = right_image.get_pixel(0, y)
				vertical_edge_delta += absf(left_color.r - right_color.r) \
					+ absf(left_color.g - right_color.g) \
					+ absf(left_color.b - right_color.b)
			var vertical_mean_delta: float = vertical_edge_delta \
				/ maxf(1.0, float(shared_height * 3))
			result["worst_mean_rgb_delta"] = maxf(
				float(result["worst_mean_rgb_delta"]), vertical_mean_delta)
			if vertical_mean_delta > 0.18:
				return {"ok": false, "mismatch":
					"r%d_c%d:right_mean=%.4f" % [
						row, column, vertical_mean_delta]}
		if row == 0:
			var lower_image: Image = images[index + HALL_TILE_COLUMNS]
			var lower_rect: Rect2 = tiles[index + HALL_TILE_COLUMNS].get_meta(
				"source_art_rect", Rect2()) as Rect2
			if not is_equal_approx(source_rect.end.y, lower_rect.position.y):
				return {"ok": false, "mismatch":
					"r%d_c%d:vertical_geometry_gap" % [row, column]}
			var shared_width := mini(image.get_width(), lower_image.get_width())
			var horizontal_edge_delta := 0.0
			for x: int in range(shared_width):
				var upper_color: Color = image.get_pixel(x, image.get_height() - 1)
				var lower_color: Color = lower_image.get_pixel(x, 0)
				horizontal_edge_delta += absf(upper_color.r - lower_color.r) \
					+ absf(upper_color.g - lower_color.g) \
					+ absf(upper_color.b - lower_color.b)
			var horizontal_mean_delta: float = horizontal_edge_delta \
				/ maxf(1.0, float(shared_width * 3))
			result["worst_mean_rgb_delta"] = maxf(
				float(result["worst_mean_rgb_delta"]), horizontal_mean_delta)
			if horizontal_mean_delta > 0.18:
				return {"ok": false, "mismatch":
					"r%d_c%d:lower_mean=%.4f" % [
						row, column, horizontal_mean_delta]}
	return result

func _load_interaction_manifest(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string(path))
	return parsed as Dictionary if parsed is Dictionary else {}

func _interaction_manifest() -> Dictionary:
	return _load_interaction_manifest(INTERACTION_MANIFEST)

func _manifest_assets_by_instance(manifest: Dictionary) -> Dictionary:
	var result: Dictionary = {}
	var assets: Array = manifest.get("assets", []) as Array
	for asset_value: Variant in assets:
		var asset: Dictionary = asset_value as Dictionary
		var room_id: String = String(asset.get("room", ""))
		var instances: Array = asset.get("instances", []) as Array
		for instance_value: Variant in instances:
			var item_id: String = String(instance_value)
			result[room_id + ":" + item_id] = asset
	return result

func _room_decoded_rgba_bytes(
		manifest_assets: Dictionary, room_id: String) -> int:
	var unique_sheets: Dictionary = {}
	var total_bytes := 0
	var prefix := room_id + ":"
	for instance_key_value: Variant in manifest_assets:
		var instance_key := String(instance_key_value)
		if not instance_key.begins_with(prefix):
			continue
		var asset: Dictionary = manifest_assets[instance_key] as Dictionary
		var sheet_path := String(asset.get("sheet", ""))
		if sheet_path.is_empty() or unique_sheets.has(sheet_path):
			continue
		unique_sheets[sheet_path] = true
		var resource_path := sheet_path if sheet_path.begins_with("res://") \
			else "res://" + sheet_path
		var image: Image = Image.load_from_file(
			ProjectSettings.globalize_path(resource_path))
		if image == null or image.is_empty():
			return -1
		total_bytes += image.get_width() * image.get_height() * 4
	return total_bytes

func _expected_room_hotspot_count(room_id: String) -> int:
	if room_id == "main_hall":
		return 13
	if room_id == "kitchen":
		return 11
	return int(EXPECTED_PHYSICAL_ITEM_COUNTS.get(room_id, 0))

func _v3_addition_visual_contract(assets: Array) -> bool:
	var addition_count := 0
	for asset_value: Variant in assets:
		var asset: Dictionary = asset_value as Dictionary
		if String(asset.get("pack", "")) != "v3_addition":
			continue
		addition_count += 1
		var grid: Array = asset.get("grid", []) as Array
		var frame_hashes: Array = asset.get("frame_sha256", []) as Array
		var normalization: Dictionary = asset.get(
			"normalization", {}) as Dictionary
		var spread: Array = normalization.get(
			"anchor_spread_pixels", []) as Array
		var alpha_qa: Array = normalization.get(
			"per_frame_alpha_qa", []) as Array
		if int(asset.get("authored_frame_count", 0)) != 8 \
				or int(asset.get("unique_frame_count", 0)) != 8 \
				or grid.size() != 2 \
				or int(grid[0]) != 4 \
				or int(grid[1]) != 2 \
				or frame_hashes.size() != 8 \
				or not bool(asset.get("transparent_border", false)) \
				or String(asset.get("normalized_use_review", "")) \
					!= "codex_visual_review_accepted_2026-08-02" \
				or int(normalization.get("padding_pixels", 0)) < 6 \
				or int(normalization.get("edge_gap_pixels", 0)) < 6 \
				or float(normalization.get("uniform_scale", 0.0)) <= 0.0 \
				or not bool(normalization.get(
					"one_uniform_scale_across_all_frames", false)) \
				or bool(normalization.get("per_frame_scale_used", true)) \
				or not bool(normalization.get(
					"fixed_anchor_translation_only", false)) \
				or spread.size() != 2 \
				or absf(float(spread[0])) > 1.5 \
				or absf(float(spread[1])) > 1.5 \
				or alpha_qa.size() != 8:
			return false
		for qa_value: Variant in alpha_qa:
			var qa: Dictionary = qa_value as Dictionary
			if not bool(qa.get("transparent_canvas_border", false)) \
					or int(qa.get("visible_exact_chroma_pixels", -1)) != 0:
				return false
			if int(qa.get("visible_near_chroma_pixels", -1)) != 0:
				return false
	return addition_count == EXPECTED_V3_ADDITION_COUNT

func _dynamic_water_hold_contract(manifest_assets: Dictionary) -> bool:
	var expected_sequence: Array[int] = [0, 1, 2, 3, 4, 4, 4, 5, 6, 7]
	var expected_roles := {
		"kitchen:seafoam_kettle": ["cup_fill", "stream"],
		"bubble_bath:shell_shower": ["shower_stream", "tub_entry"],
	}
	for instance_key: String in expected_roles:
		var asset: Dictionary = manifest_assets.get(
			instance_key, {}) as Dictionary
		if asset.is_empty() \
				or String(asset.get("pack", "")) != "v3_addition" \
				or int(asset.get("authored_frame_count", 0)) != 8:
			return false
		var actual_sequence: Array[int] = []
		for frame_value: Variant in asset.get("timeline_sequence", []) as Array:
			actual_sequence.append(int(frame_value))
		if actual_sequence != expected_sequence:
			return false
		var actual_roles: Array[String] = []
		for layer_value: Variant in asset.get("water_layers", []) as Array:
			var layer: Dictionary = layer_value as Dictionary
			var role := String(layer.get("role", ""))
			actual_roles.append(role)
			var active_frames: Array = layer.get("active_frames", []) as Array
			if active_frames.size() != 1 or int(active_frames[0]) != 4:
				return false
			if role in ["stream", "shower_stream"] \
					and (layer.get("points_frames", []) as Array).size() != 8:
				return false
		actual_roles.sort()
		var required_roles: Array[String] = []
		for role_value: Variant in expected_roles[instance_key] as Array:
			required_roles.append(String(role_value))
		required_roles.sort()
		if actual_roles != required_roles:
			return false
	return true

func _legacy_pool_assets_by_instance(manifest: Dictionary) -> Dictionary:
	var result: Dictionary = {}
	var legacy_assets: Dictionary = _manifest_assets_by_instance(manifest)
	for instance_key_value: Variant in legacy_assets:
		var instance_key := String(instance_key_value)
		if not instance_key.begins_with("mermaid_pool:"):
			continue
		var asset: Dictionary = (
			legacy_assets[instance_key] as Dictionary).duplicate(true)
		var frame_count: int = int(asset.get("frame_count", 0))
		var timeline_sequence: Array[int] = []
		for frame_index: int in range(frame_count):
			timeline_sequence.append(frame_index)
		asset["legacy_room_derived"] = true
		asset["authored_frame_count"] = frame_count
		asset["timeline_frame_count"] = frame_count
		asset["timeline_sequence"] = timeline_sequence
		asset["grid"] = [
			int(asset.get("hframes", 0)), int(asset.get("vframes", 0))]
		asset["sheet"] = String(asset.get("atlas", ""))
		asset["rest_frame"] = 0
		asset["physics_mode"] = "none"
		asset["water_layers"] = []
		result[instance_key] = asset
	return result

func _atlas_frames_have_clear_border(sprite: Sprite3D,
		frame_count: int) -> bool:
	if sprite == null or sprite.texture == null \
			or sprite.hframes < 1 or sprite.vframes < 1:
		return false
	var image: Image = sprite.texture.get_image()
	if image == null or image.is_empty():
		return false
	if image.get_width() % sprite.hframes != 0 \
			or image.get_height() % sprite.vframes != 0:
		return false
	var cell_width: int = image.get_width() / sprite.hframes
	var cell_height: int = image.get_height() / sprite.vframes
	for frame_index: int in range(frame_count):
		var frame_column: int = frame_index % sprite.hframes
		var frame_row: int = frame_index / sprite.hframes
		var left: int = frame_column * cell_width
		var top: int = frame_row * cell_height
		var right: int = left + cell_width - 1
		var bottom: int = top + cell_height - 1
		for x: int in range(left, right + 1):
			if image.get_pixel(x, top).a > 0.01 \
					or image.get_pixel(x, bottom).a > 0.01:
				return false
		for y: int in range(top, bottom + 1):
			if image.get_pixel(left, y).a > 0.01 \
					or image.get_pixel(right, y).a > 0.01:
				return false
	return true

func _hotspot_overlap_fraction(first: Button, second: Button) -> float:
	if first == null or second == null:
		return 1.0
	var first_rect := Rect2(first.position, first.size)
	var second_rect := Rect2(second.position, second.size)
	var smaller_area: float = minf(
		first_rect.get_area(), second_rect.get_area())
	if smaller_area <= 0.0:
		return 1.0
	return first_rect.intersection(second_rect).get_area() / smaller_area

func _fixture_uv_matches_frame(sprite: Sprite3D, frame_index: int) -> bool:
	if sprite == null or sprite.hframes < 1 or sprite.vframes < 1:
		return false
	var material: ShaderMaterial = sprite.get_meta(
		"castle_fixture_material", null) as ShaderMaterial
	if material == null:
		return false
	var frame_column: int = frame_index % sprite.hframes
	var frame_row: int = int(frame_index / sprite.hframes)
	var expected_uv := Vector4(
		float(frame_column) / float(sprite.hframes),
		float(frame_row) / float(sprite.vframes),
		float(frame_column + 1) / float(sprite.hframes),
		float(frame_row + 1) / float(sprite.vframes))
	var metadata_value: Variant = sprite.get_meta("fixture_uv_rect", null)
	var shader_value: Variant = material.get_shader_parameter(
		"fixture_uv_rect")
	if not metadata_value is Vector4 or not shader_value is Vector4:
		return false
	var metadata_uv: Vector4 = metadata_value as Vector4
	var shader_uv: Vector4 = shader_value as Vector4
	return metadata_uv.is_equal_approx(expected_uv) \
		and shader_uv.is_equal_approx(expected_uv) \
		and shader_uv.is_equal_approx(metadata_uv)

func _visible_world_sprite3d_count() -> int:
	var counts: Dictionary = {}
	_audit_world_node(main.castle_room_world_root, counts)
	return int(counts.get("visible_sprite3d", 0))

func _hall_cull_snapshot() -> Dictionary:
	var snapshot := {
		"inventory": 0,
		"backgrounds": 0,
		"signs": 0,
		"royal_hall_mist_cards": 0,
		"visible": 0,
		"visible_backgrounds": 0,
		"visible_signs": 0,
		"visible_royal_hall_mist_cards": 0,
		"metadata_ok": true,
	}
	for tile: Sprite3D in main.castle_room_background_tiles:
		snapshot["inventory"] = int(snapshot["inventory"]) + 1
		snapshot["backgrounds"] = int(snapshot["backgrounds"]) + 1
		var tile_rect: Rect2 = tile.get_meta(
			"hall_horizontal_cull_rect", Rect2()) as Rect2
		var source_rect: Rect2 = tile.get_meta(
			"source_art_rect", Rect2()) as Rect2
		snapshot["metadata_ok"] = bool(snapshot["metadata_ok"]) \
			and bool(tile.get_meta("hall_horizontal_cull", false)) \
			and String(tile.get_meta("hall_horizontal_cull_kind", "")) \
				== "background_tile" \
			and tile_rect.has_area() \
			and tile_rect == source_rect
		if tile.visible:
			snapshot["visible"] = int(snapshot["visible"]) + 1
			snapshot["visible_backgrounds"] = \
				int(snapshot["visible_backgrounds"]) + 1
	if main.castle_room_mid_layer == null:
		snapshot["metadata_ok"] = false
		return snapshot
	for child: Node in main.castle_room_mid_layer.get_children():
		var card: Sprite3D = child as Sprite3D
		if card == null:
			continue
		var is_sign: bool = String(card.name).begins_with("HallDoorSign_")
		var is_royal_mist: bool = String(card.name).begins_with(
			"RoyalHallMist_")
		if not is_sign and not is_royal_mist:
			continue
		snapshot["inventory"] = int(snapshot["inventory"]) + 1
		var card_rect: Rect2 = card.get_meta(
			"hall_horizontal_cull_rect", Rect2()) as Rect2
		var expected_kind: String = "door_sign" \
			if is_sign else "royal_hall_mist"
		var expected_role: String = "room_door_sign" \
			if is_sign else "royal_hall_mist"
		snapshot["metadata_ok"] = bool(snapshot["metadata_ok"]) \
			and bool(card.get_meta("hall_horizontal_cull", false)) \
			and String(card.get_meta("hall_horizontal_cull_kind", "")) \
				== expected_kind \
			and String(card.get_meta("source_asset_role", "")) \
				== expected_role \
			and card_rect.has_area()
		if is_sign:
			snapshot["signs"] = int(snapshot["signs"]) + 1
			if card.visible:
				snapshot["visible_signs"] = \
					int(snapshot["visible_signs"]) + 1
		else:
			snapshot["royal_hall_mist_cards"] = \
				int(snapshot["royal_hall_mist_cards"]) + 1
			if card.visible:
				snapshot["visible_royal_hall_mist_cards"] = \
					int(snapshot["visible_royal_hall_mist_cards"]) + 1
		if card.visible:
			snapshot["visible"] = int(snapshot["visible"]) + 1
	return snapshot

func _expanded_runtime_water_roles(layers: Array) -> Array[String]:
	var roles: Array[String] = []
	for layer_value: Variant in layers:
		var layer: Dictionary = layer_value as Dictionary
		var role: String = String(layer.get("role", ""))
		if role == "bubble_emitter":
			var relative_centers: Array = layer.get(
				"relative_centers", []) as Array
			for _center_value: Variant in relative_centers:
				roles.append("bubble")
		else:
			roles.append(role)
	return roles


func _direct_visual_inventory() -> Dictionary:
	var inventory := {
		"art": 0,
		"water": 0,
		"jolt": 0,
		"other": 0,
		"total": 0,
	}
	if main.castle_room_item_visual_layer == null:
		return inventory
	for child: Node in main.castle_room_item_visual_layer.get_children():
		inventory["total"] = int(inventory["total"]) + 1
		if child is Sprite3D:
			if bool(child.get_meta("castle_fixture_water", false)):
				inventory["water"] = int(inventory["water"]) + 1
			else:
				inventory["art"] = int(inventory["art"]) + 1
		elif child is RigidBody3D \
				and bool(child.get_meta("castle_fixture_jolt_garnish", false)):
			inventory["jolt"] = int(inventory["jolt"]) + 1
		else:
			inventory["other"] = int(inventory["other"]) + 1
	return inventory


func _expected_room_fixture_inventory(
		manifest_assets: Dictionary, room_id: String) -> Dictionary:
	var expected := {"water": 0, "jolt": 0}
	var prefix := room_id + ":"
	for instance_key_value: Variant in manifest_assets:
		var instance_key := String(instance_key_value)
		if not instance_key.begins_with(prefix):
			continue
		var asset: Dictionary = manifest_assets[instance_key] as Dictionary
		var layers: Array = asset.get("water_layers", []) as Array
		expected["water"] = int(expected["water"]) \
			+ _expanded_runtime_water_roles(layers).size()
		if String(asset.get("physics_mode", "none")) != "none":
			expected["jolt"] = int(expected["jolt"]) + 1
	return expected


func _run_semantic_animation(rooms: CastleRooms25D, room_id: String,
		item_id: String, manifest_asset: Dictionary) -> Dictionary:
	var result := {
		"contract_ok": false,
		"sequence_ok": false,
		"transform_ok": false,
		"sound_ok": false,
		"busy_guard_ok": false,
		"fixture_uv_ok": true,
		"menu_order_ok": true,
		"water_profile_ok": false,
		"physics_motion_ok": true,
		"settled_ok": true,
		"peak_visible_cards": 0,
		"detail": "",
	}
	var record: Dictionary = main.castle_room_item_sprites.get(
		item_id, {}) as Dictionary
	var sprite: Sprite3D = record.get("sprite") as Sprite3D
	var item_data: Dictionary = record.get("data", {}) as Dictionary
	if sprite == null or manifest_asset.is_empty():
		result["detail"] = "missing runtime sprite or interaction manifest asset"
		return result
	var legacy_room_derived := bool(manifest_asset.get(
		"legacy_room_derived", false))
	var authored_count: int = int(manifest_asset.get(
		"authored_frame_count", 0))
	var timeline_count: int = int(manifest_asset.get(
		"timeline_frame_count", 0))
	var grid_values: Array = manifest_asset.get("grid", []) as Array
	var cell_size_values: Array = manifest_asset.get("cell_size", []) as Array
	var expected_sheet_path := "res://" + String(
		manifest_asset.get("sheet", ""))
	var expected_sound_path := "res://" + String(
		manifest_asset.get("sound", ""))
	var expected_sound_value := expected_sound_path.trim_prefix(
		"res://assets/audio/")
	var texture_size: Vector2 = sprite.texture.get_size() \
		if sprite.texture != null else Vector2.ZERO
	var expected_texture_size := Vector2.ZERO
	if cell_size_values.size() == 2 and grid_values.size() == 2:
		expected_texture_size = Vector2(
			float(cell_size_values[0]) * float(grid_values[0]),
			float(cell_size_values[1]) * float(grid_values[1]))
	var physics_mode: String = String(manifest_asset.get(
		"physics_mode", "none"))
	var initial_fixture_stats: Dictionary = rooms.fixture_rigs.stats()
	var rig: Dictionary = record.get("fixture_rig", {}) as Dictionary
	var body: RigidBody3D = rig.get("body") as RigidBody3D
	var water_layers: Array = manifest_asset.get("water_layers", []) as Array
	var runtime_water: Array = rig.get("water", []) as Array
	var expected_water_roles: Array[String] = \
		_expanded_runtime_water_roles(water_layers)
	var actual_water_roles: Array[String] = []
	var valid_water_roles: Array[String] = [
		"stream", "basin", "fill", "vortex", "ripple",
		"waterfall_band", "waterfall_splash", "bubble",
		"cup_fill", "wheel_feed", "paddle_splash",
		"shower_stream", "tub_entry",
	]
	var water_contract_ok: bool = \
		runtime_water.size() == expected_water_roles.size()
	var dynamic_fixture: bool = String(manifest_asset.get("id", "")) in [
		"kitchen_seafoam_kettle", "bubble_bath_shell_shower",
	]
	for water_value: Variant in runtime_water:
		var water: Dictionary = water_value as Dictionary
		var water_node: Sprite3D = water.get("node") as Sprite3D
		if water_node == null:
			water_contract_ok = false
			continue
		var water_material: ShaderMaterial = water.get(
			"material") as ShaderMaterial
		var water_role: String = String(water.get("role", ""))
		var normalized_center: Vector2 = water.get(
			"base_center_normalized", Vector2.INF) as Vector2
		var normalized_bounds: Rect2 = water_node.get_meta(
			"fixture_bounds_normalized", Rect2(-Vector2.ONE, Vector2.ZERO)) as Rect2
		var stored_bounds: Rect2 = water.get(
			"bounds_normalized", Rect2(-Vector2.ONE, Vector2.ZERO)) as Rect2
		var normalized_outlet: Vector2 = water_node.get_meta(
			"fixture_outlet_normalized", Vector2.INF) as Vector2
		var stored_outlet: Vector2 = water.get(
			"outlet_normalized", Vector2.INF) as Vector2
		var water_shape: String = String(water_node.get_meta("water_shape", ""))
		var stored_shape: String = String(water.get("shape", ""))
		var valid_water_shapes: Array[String] = ["ellipse", "polygon"]
		var active_frames: Array = water.get("active_frames", []) as Array
		var points_frames: Array = water.get("points_frames", []) as Array
		actual_water_roles.append(water_role)
		water_contract_ok = water_contract_ok \
			and water_role in valid_water_roles \
			and water_material != null \
			and water_material.shader != null \
			and water_material.shader.resource_path \
				== "res://assets/shaders/castle_fixture_water.gdshader" \
			and water_node.texture != null \
			and water_node.texture.get_size() == Vector2(96.0, 96.0) \
			and normalized_center.x >= 0.0 and normalized_center.x <= 1.0 \
			and normalized_center.y >= 0.0 and normalized_center.y <= 1.0 \
			and normalized_bounds.position.x >= 0.0 \
			and normalized_bounds.position.y >= 0.0 \
			and normalized_bounds.size.x > 0.0 \
			and normalized_bounds.size.y > 0.0 \
			and normalized_bounds.end.x <= 1.0 \
			and normalized_bounds.end.y <= 1.0 \
			and normalized_bounds.position.is_equal_approx(stored_bounds.position) \
			and normalized_bounds.size.is_equal_approx(stored_bounds.size) \
			and normalized_outlet.x >= 0.0 and normalized_outlet.x <= 1.0 \
			and normalized_outlet.y >= 0.0 and normalized_outlet.y <= 1.0 \
			and normalized_outlet.is_equal_approx(stored_outlet) \
			and water_shape in valid_water_shapes \
			and water_shape == stored_shape \
			and water_node.scale.x > 0.0 and water_node.scale.y > 0.0 \
			and not water_node.visible \
			and not water_node.no_depth_test \
			and water_node.cast_shadow \
				== GeometryInstance3D.SHADOW_CASTING_SETTING_OFF \
			and String(water_node.get_meta("water_role", "")) == water_role \
			and bool(water_node.get_meta("bounded_to_fixture", false)) \
			and bool(water_node.get_meta("sprite_masked_water", false)) \
			and bool(water_node.get_meta("depth_write_disabled", false)) \
			and not bool(water_node.get_meta("logic_authority", true)) \
			and float(water.get("flow_start", -1.0)) >= 0.0 \
			and float(water.get("flow_start", 2.0)) < 1.0 \
			and absf(float(water.get("flow_amount", -1.0))) <= 0.001
		if dynamic_fixture:
			water_contract_ok = water_contract_ok \
				and active_frames.size() == 1 \
				and int(active_frames[0]) == 4
			if water_role in ["stream", "shower_stream"]:
				water_contract_ok = water_contract_ok \
					and points_frames.size() == 8 \
					and water_shape == "polygon"
	expected_water_roles.sort()
	actual_water_roles.sort()
	water_contract_ok = water_contract_ok \
		and actual_water_roles == expected_water_roles
	var physics_metrics_present: bool = physics_mode == "none" or (
		rig.has("peak_angle_radians")
		and rig.has("peak_displacement")
		and rig.has("max_angle_radians")
		and rig.has("max_displacement")
	)
	var physics_contract_ok: bool = body == null if physics_mode == "none" else (
		body != null
		and body.collision_layer == 0
		and body.collision_mask == 0
		and bool(body.get_meta("castle_fixture_jolt_garnish", false))
		and not bool(body.get_meta("logic_authority", true))
		and bool(body.get_meta("depth_axis_locked", false))
		and physics_metrics_present
	)
	var asset_pack := String(manifest_asset.get("pack", ""))
	var expected_review := "codex_visual_review_accepted_2026-08-02" \
		if asset_pack == "v3_addition" \
		else "codex_visual_review_accepted_2026-08-01"
	var visual_delivery_contract_ok: bool = (
		String(manifest_asset.get("normalized_use_review", "")) \
			== "accepted_visual_review_2026-08-01"
		and not bool(sprite.get_meta("generated_full_object_states", false))
		and not bool(sprite.get_meta("primary_animation_is_overlay", false))
		and rig.is_empty()
		and sprite.texture_filter \
			== BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	) if legacy_room_derived else (
		String(manifest_asset.get("normalized_use_review", "")) \
			== expected_review
		and asset_pack in ["v2_base", "v3_addition"]
		and (asset_pack != "v3_addition" \
			or bool(sprite.get_meta("castle_component_rig_v3", false)))
		and not bool(manifest_asset.get("primary_animation_is_overlay", true))
		and not bool(sprite.get_meta("primary_animation_is_overlay", true))
		and bool(sprite.get_meta("generated_full_object_states", false))
		and String(sprite.get_meta("fixture_water_shader", "")) \
			== "res://assets/shaders/castle_fixture_water.gdshader"
		and String(sprite.get_meta("fixture_water_ripple_texture", "")) \
			== "res://assets/terrain/up_water_nrm.jpg"
		and String(sprite.get_meta("fixture_water_caustics_texture", "")) \
			== "res://assets/terrain/caustics.png"
		and sprite.texture_filter == BaseMaterial3D.TEXTURE_FILTER_LINEAR
	)
	result["contract_ok"] = (
		authored_count == 8
		and timeline_count >= 4 and timeline_count <= 12
		and int(sprite.get_meta("animation_frame_count", 0)) == authored_count
		and grid_values.size() == 2
		and sprite.hframes == int(grid_values[0])
		and sprite.vframes == int(grid_values[1])
		and sprite.hframes * sprite.vframes == authored_count
		and texture_size == expected_texture_size
		and maxf(texture_size.x, texture_size.y) <= 1024.0
		and sprite.texture != null
		and sprite.texture.resource_path == expected_sheet_path
		and String(sprite.get_meta("semantic_action", ""))
			== String(manifest_asset.get("semantic_action", ""))
		and String(item_data.get("semantic_action", ""))
			== String(manifest_asset.get("semantic_action", ""))
		and String(item_data.get("sound", "")) == expected_sound_value
		and int(item_data.get("sound_frame", -1))
			== int(manifest_asset.get("sound_frame", -2))
		and is_equal_approx(float(item_data.get("frame_duration", -1.0)),
			float(manifest_asset.get("frame_duration_seconds", -2.0)))
		and bool(sprite.get_meta("fixed_pivot_animation", false))
		and bool(manifest_asset.get("fixed_pivot", false))
		and bool(manifest_asset.get("transparent_border", false))
		and visual_delivery_contract_ok
		and int(manifest_asset.get("unique_frame_count", 0)) >= 4
		and int(manifest_asset.get("unique_frame_count", 0)) <= authored_count
		and sprite.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD
		and is_equal_approx(sprite.alpha_scissor_threshold, 0.5)
		and not sprite.no_depth_test
		and _atlas_frames_have_clear_border(sprite, authored_count)
		and ResourceLoader.exists(expected_sound_path)
		and water_contract_ok
		and physics_contract_ok
		and int(initial_fixture_stats.get("allocated", 99)) <= 12
		and int(initial_fixture_stats.get("awake", 99)) <= 8
		and int(initial_fixture_stats.get("body_cap", 0)) == 12
		and int(initial_fixture_stats.get("awake_cap", 0)) == 8
	)
	var start_position: Vector3 = sprite.position
	var start_scale: Vector3 = sprite.scale
	var start_rotation: Vector3 = sprite.rotation
	var fixture_uv_before := true
	if item_data.has("light_cluster"):
		fixture_uv_before = _fixture_uv_matches_frame(sprite, sprite.frame)
	var effects_before: int = \
		main.castle_room_item_effect_layer.get_child_count()
	if main.castle_room_prop_sfx != null:
		main.castle_room_prop_sfx.stop()
		main.castle_room_prop_sfx.stream = null
	if room_id == "kitchen" and item_id == "fridge" \
			and rooms.kitchen_menu_layer != null:
		rooms._close_kitchen_menu()
	var peak_visible_cards: int = _visible_world_sprite3d_count()
	rooms._activate_room_item(item_id)
	peak_visible_cards = maxi(
		peak_visible_cards, _visible_world_sprite3d_count())
	var active_fixture_stats: Dictionary = rooms.fixture_rigs.stats()
	result["contract_ok"] = bool(result["contract_ok"]) \
		and int(active_fixture_stats.get("allocated", 99)) <= 12 \
		and int(active_fixture_stats.get("awake", 99)) <= 8
	var busy_started: bool = bool(sprite.get_meta("busy", false))
	var menu_hidden_while_busy := true
	if room_id == "kitchen" and item_id == "fridge":
		menu_hidden_while_busy = rooms.kitchen_menu_layer == null \
			or not rooms.kitchen_menu_layer.visible
	var effects_after_first: int = \
		main.castle_room_item_effect_layer.get_child_count()
	rooms._activate_room_item(item_id)
	result["busy_guard_ok"] = busy_started \
		and main.castle_room_item_effect_layer.get_child_count() \
			== effects_after_first \
		and effects_after_first == effects_before
	var transform_ok := true
	var water_visible_seen: Array[bool] = []
	water_visible_seen.resize(runtime_water.size())
	water_visible_seen.fill(false)
	var dynamic_water_frame_seen: Array[bool] = []
	dynamic_water_frame_seen.resize(runtime_water.size())
	dynamic_water_frame_seen.fill(false)
	var dynamic_water_outside_active_frame_seen := false
	for water_index: int in range(runtime_water.size()):
		var initial_water: Dictionary = runtime_water[water_index] as Dictionary
		var initial_active_frames: Array = initial_water.get(
			"active_frames", []) as Array
		dynamic_water_frame_seen[water_index] = initial_active_frames.is_empty()
	var waited_frames := 0
	var deadline_ms: int = Time.get_ticks_msec() + 5000
	while bool(sprite.get_meta("busy", false)) \
			and Time.get_ticks_msec() < deadline_ms:
		await process_frame
		waited_frames += 1
		peak_visible_cards = maxi(
			peak_visible_cards, _visible_world_sprite3d_count())
		if physics_mode == "none":
			transform_ok = transform_ok \
				and sprite.position.is_equal_approx(start_position) \
				and sprite.scale.is_equal_approx(start_scale) \
				and sprite.rotation.is_equal_approx(start_rotation)
		for water_index: int in range(runtime_water.size()):
			var water: Dictionary = runtime_water[water_index] as Dictionary
			var water_node: Sprite3D = water.get("node") as Sprite3D
			if water_node != null and water_node.visible \
					and float(water.get("flow_amount", 0.0)) > 0.01:
				water_visible_seen[water_index] = true
				var active_frames: Array = water.get(
					"active_frames", []) as Array
				if not active_frames.is_empty():
					var water_atlas_frame := int(sprite.get_meta(
						"fixture_water_atlas_frame", -1))
					var water_frame_is_active := false
					for active_frame_value: Variant in active_frames:
						if int(active_frame_value) == water_atlas_frame:
							water_frame_is_active = true
							break
					if water_frame_is_active:
						dynamic_water_frame_seen[water_index] = true
					else:
						dynamic_water_outside_active_frame_seen = true
	var visited: Array = sprite.get_meta(
		"animation_frames_visited", []) as Array
	var timeline_visited: Array = sprite.get_meta(
		"animation_timeline_steps_visited", []) as Array
	var manifest_sequence_values: Array = manifest_asset.get(
		"timeline_sequence", []) as Array
	var manifest_sequence: Array[int] = []
	for frame_value: Variant in manifest_sequence_values:
		manifest_sequence.append(int(frame_value))
	var expected_steps := timeline_count
	if room_id == "kitchen" and item_id == "fridge":
		expected_steps = int(manifest_asset.get("open_hold_step", 4)) + 1
	var expected_timeline: Array[int] = []
	for timeline_step in range(expected_steps):
		expected_timeline.append(timeline_step)
	var atlas_sequence_ok := visited.size() == expected_steps
	if not item_data.has("light_cluster"):
		atlas_sequence_ok = atlas_sequence_ok \
			and visited == manifest_sequence.slice(0, expected_steps)
	var expected_rest_frame: int = int(manifest_asset.get("rest_frame", 0))
	if room_id == "kitchen" and item_id == "fridge":
		expected_rest_frame = manifest_sequence[expected_steps - 1]
	var all_water_seen := true
	for layer_seen: bool in water_visible_seen:
		all_water_seen = all_water_seen and layer_seen
	var dynamic_water_frames_ok := not dynamic_water_outside_active_frame_seen
	for active_frame_seen: bool in dynamic_water_frame_seen:
		dynamic_water_frames_ok = dynamic_water_frames_ok and active_frame_seen
	result["sequence_ok"] = busy_started \
		and not bool(sprite.get_meta("busy", true)) \
		and timeline_visited == expected_timeline \
		and atlas_sequence_ok \
		and sprite.frame == expected_rest_frame \
		and all_water_seen \
		and Time.get_ticks_msec() < deadline_ms
	var played_stream: AudioStream = main.castle_room_prop_sfx.stream \
		if main.castle_room_prop_sfx != null else null
	result["sound_ok"] = played_stream != null \
		and played_stream.resource_path == expected_sound_path
	if room_id == "kitchen" and item_id == "fridge":
		result["menu_order_ok"] = menu_hidden_while_busy \
			and rooms.kitchen_menu_layer != null \
			and rooms.kitchen_menu_layer.visible \
			and main.touch_control_blocks.has("kitchen_fridge_menu")
		rooms._close_kitchen_menu()
		var close_busy_started: bool = bool(sprite.get_meta("busy", false))
		var close_controls_gated: bool = close_busy_started \
			and main.touch_control_blocks.has("kitchen_fridge_close") \
			and not main.touch_control_blocks.has("kitchen_fridge_menu")
		var blocker: Control = rooms.fridge_close_input_blocker
		var close_input_gate_ok: bool = rooms._fridge_close_is_blocked() \
			and blocker != null \
			and blocker.mouse_filter == Control.MOUSE_FILTER_STOP \
			and bool(blocker.get_meta(
				"castle_fridge_close_input_gate", false))
		var room_id_before: String = main.castle_room_id
		var sink_record: Dictionary = main.castle_room_item_sprites.get(
			"sink", {}) as Dictionary
		var sink_sprite: Sprite3D = sink_record.get("sprite") as Sprite3D
		var sink_frame_before: int = sink_sprite.frame if sink_sprite != null else -1
		rooms._go_back()
		rooms._activate_room_item("sink")
		close_input_gate_ok = close_input_gate_ok \
			and main.castle_room_id == room_id_before \
			and sink_sprite != null \
			and not bool(sink_sprite.get_meta("busy", false)) \
			and sink_sprite.frame == sink_frame_before
		var close_deadline: int = Time.get_ticks_msec() + 3000
		while bool(sprite.get_meta("busy", false)) \
				and Time.get_ticks_msec() < close_deadline:
			close_controls_gated = close_controls_gated \
				and main.touch_control_blocks.has("kitchen_fridge_close")
			close_input_gate_ok = close_input_gate_ok \
				and rooms._fridge_close_is_blocked()
			await process_frame
			peak_visible_cards = maxi(
				peak_visible_cards, _visible_world_sprite3d_count())
			if bool(sprite.get_meta("busy", false)):
				close_controls_gated = close_controls_gated \
					and main.touch_control_blocks.has("kitchen_fridge_close")
		var expected_close_path := "res://" + String(
			manifest_asset.get("close_sound", ""))
		var close_stream: AudioStream = main.castle_room_prop_sfx.stream \
			if main.castle_room_prop_sfx != null else null
		var open_hold_step: int = int(manifest_asset.get("open_hold_step", 4))
		var expected_close_frames: Array = manifest_sequence.slice(
			open_hold_step, timeline_count)
		var expected_close_steps: Array[int] = []
		for close_step: int in range(open_hold_step, timeline_count):
			expected_close_steps.append(close_step)
		var close_frames_visited: Array = sprite.get_meta(
			"animation_frames_visited", []) as Array
		var close_steps_visited: Array = sprite.get_meta(
			"animation_timeline_steps_visited", []) as Array
		var close_sequence_ok: bool = close_busy_started \
			and not bool(sprite.get_meta("busy", true)) \
			and close_frames_visited == expected_close_frames \
			and close_steps_visited == expected_close_steps \
			and not expected_close_frames.is_empty() \
			and int(expected_close_frames[-1]) \
				== int(manifest_asset.get("rest_frame", 0)) \
			and sprite.frame == int(manifest_asset.get("rest_frame", 0)) \
			and Time.get_ticks_msec() < close_deadline
		result["sequence_ok"] = bool(result["sequence_ok"]) \
			and close_sequence_ok
		result["menu_order_ok"] = bool(result["menu_order_ok"]) \
			and close_sequence_ok \
			and close_controls_gated \
			and close_input_gate_ok \
			and not rooms._fridge_close_is_blocked() \
			and not main.touch_control_blocks.has("kitchen_fridge_close") \
			and rooms.kitchen_menu_layer == null
		result["sound_ok"] = bool(result["sound_ok"]) \
			and close_stream != null \
			and close_stream.resource_path == expected_close_path
	var water_at_rest := true
	for water_value: Variant in runtime_water:
		var water: Dictionary = water_value as Dictionary
		var water_node: Sprite3D = water.get("node") as Sprite3D
		var water_material: ShaderMaterial = water.get(
			"material") as ShaderMaterial
		water_at_rest = water_at_rest \
			and water_node != null \
			and not water_node.visible \
			and absf(float(water.get("flow_amount", -1.0))) <= 0.001 \
			and water_material != null \
			and water_material.get_shader_parameter("flow_amount") != null \
			and absf(float(water_material.get_shader_parameter(
				"flow_amount"))) <= 0.001
	result["water_profile_ok"] = water_contract_ok \
		and all_water_seen and water_at_rest and dynamic_water_frames_ok
	result["sequence_ok"] = bool(result["sequence_ok"]) \
		and bool(result["water_profile_ok"])
	var physics_motion_ok: bool = physics_mode == "none"
	var settled_ok: bool = physics_mode == "none"
	var peak_angle := 0.0
	var peak_displacement := 0.0
	var max_angle := 0.0
	var max_displacement := 0.0
	if physics_mode != "none" and body != null:
		var settle_deadline: int = Time.get_ticks_msec() + 5000
		while not body.freeze and Time.get_ticks_msec() < settle_deadline:
			await physics_frame
			peak_visible_cards = maxi(
				peak_visible_cards, _visible_world_sprite3d_count())
		peak_angle = float(rig.get("peak_angle_radians", -1.0))
		peak_displacement = float(rig.get("peak_displacement", -1.0))
		max_angle = float(rig.get("max_angle_radians", -1.0))
		max_displacement = float(rig.get("max_displacement", -1.0))
		physics_motion_ok = physics_metrics_present \
			and peak_angle > 0.001 \
			and peak_displacement > 0.001 \
			and max_angle > 0.001 and max_angle <= 0.65 \
			and max_displacement > 0.001 and max_displacement <= 0.35 \
			and peak_angle <= max_angle + 0.0001 \
			and peak_displacement <= max_displacement + 0.0001
		settled_ok = body.freeze and body.sleeping \
			and Time.get_ticks_msec() < settle_deadline
		transform_ok = transform_ok \
			and settled_ok \
			and sprite.position.distance_to(start_position) <= 0.02 \
			and sprite.scale.is_equal_approx(start_scale) \
			and absf(sprite.rotation.z - start_rotation.z) <= 0.02
	result["physics_motion_ok"] = physics_motion_ok
	result["settled_ok"] = settled_ok
	result["transform_ok"] = transform_ok and physics_motion_ok and settled_ok
	if item_data.has("light_cluster"):
		result["fixture_uv_ok"] = fixture_uv_before \
			and _fixture_uv_matches_frame(sprite, sprite.frame)
	result["peak_visible_cards"] = peak_visible_cards
	result["detail"] = (
		"%s atlas=%s steps=%s sound=%s wait=%d water=%d/%d/%d "
		+ "cards=%d jolt=%.4f/%.4f limits=%.4f/%.4f") % [
		room_id + ":" + item_id, str(visited), str(timeline_visited),
		played_stream.resource_path if played_stream != null else "missing",
		waited_frames, water_visible_seen.count(true), runtime_water.size(),
		expected_water_roles.size(), peak_visible_cards,
		peak_angle, peak_displacement,
		max_angle, max_displacement]
	if String(item_data.get("launch_activity", "")) == "castle_logo" \
			and main.castle_logo_layer != null:
		main._close_castle_logo()
		await process_frame
	return result

func _capture(room_id: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	# Capture the settled stage, not the intentional 0.24-second room fade.
	await _frames(20)
	await RenderingServer.frame_post_draw
	# CI sets CASTLE_SHOT_OUT and uploads from there. Without this the shots
	# landed in the gitignored res://audit/ and the "pearl-castle visual
	# review" artifact came back empty on every run since it was added —
	# green, because upload-artifact is configured if-no-files-found: warn.
	# Same env-var idiom as NORTH_SHOT_OUT / OPERA_SHOT_OUT / REEF_SHOT_OUT.
	var requested: String = OS.get_environment("CASTLE_SHOT_OUT")
	var output_dir: String = requested if requested != "" \
		else ProjectSettings.globalize_path("res://audit/castle_sprite3d")
	DirAccess.make_dir_recursive_absolute(output_dir)
	var output_path := output_dir.path_join(room_id + ".png")
	var save_error: Error = root.get_viewport().get_texture().get_image() \
		.save_png(output_path)
	print("CASTLE_ART|capture|", output_path, "|error=", save_error)

func _inventory_increment(counts: Dictionary, key: String) -> void:
	counts[key] = int(counts.get(key, 0)) + 1

func _collect_runtime_node_inventory(node: Node, inventory: Dictionary) -> void:
	if node == null:
		return
	var node_types: Dictionary = inventory["node_types"] as Dictionary
	_inventory_increment(node_types, node.get_class())
	if node is Sprite3D:
		var sprite: Sprite3D = node as Sprite3D
		var sprite_summary: Dictionary = inventory["sprite3d"] as Dictionary
		sprite_summary["total"] = int(sprite_summary["total"]) + 1
		sprite_summary["visible"] = int(sprite_summary["visible"]) \
			+ (1 if sprite.visible else 0)
		sprite_summary["unshaded"] = int(sprite_summary["unshaded"]) \
			+ (1 if not sprite.shaded else 0)
		sprite_summary["shaded"] = int(sprite_summary["shaded"]) \
			+ (1 if sprite.shaded else 0)
		sprite_summary["depth_tested"] = int(
			sprite_summary["depth_tested"]) \
			+ (1 if not sprite.no_depth_test else 0)
		sprite_summary["missing_texture"] = int(
			sprite_summary["missing_texture"]) \
			+ (1 if sprite.texture == null else 0)
		var role: String = String(sprite.get_meta(
			"source_asset_role", "unspecified_sprite3d"))
		var roles: Dictionary = inventory["world_art_roles"] as Dictionary
		_inventory_increment(roles, role)
		var texture_path := ""
		var texture_dimensions: Array[int] = []
		if sprite.texture != null:
			texture_path = sprite.texture.resource_path
			texture_dimensions = [
				sprite.texture.get_width(), sprite.texture.get_height()]
		var cards: Array = inventory["sprite3d_cards"] as Array
		cards.append({
			"node_path": String(sprite.get_path()),
			"role": role,
			"source_object_id": String(sprite.get_meta(
				"source_object_id", "")),
			"texture": texture_path,
			"texture_dimensions": texture_dimensions,
			"visible": sprite.visible,
			"unshaded": not sprite.shaded,
			"depth_tested": not sprite.no_depth_test,
			"transparent": sprite.transparent,
			"alpha_cut_mode": int(sprite.alpha_cut),
			"cast_shadow_mode": int(sprite.cast_shadow),
			"depth_z": sprite.position.z,
		})
	for child: Node in node.get_children():
		_collect_runtime_node_inventory(child, inventory)

func _write_main_hall_node_inventory() -> bool:
	if main.castle_room_world_root == null \
			or main.castle_room_id != "main_hall":
		return false
	var inventory := {
		"schema": 1,
		"purpose": "Castle Main Hall runtime Sprite3D node-type inventory",
		"engine": Engine.get_version_info(),
		"rendering_method": RenderingServer.get_current_rendering_method(),
		"room": main.castle_room_id,
		"node_types": {},
		"world_art_roles": {},
		"sprite3d": {
			"total": 0,
			"visible": 0,
			"unshaded": 0,
			"shaded": 0,
			"depth_tested": 0,
			"missing_texture": 0,
		},
		"sprite3d_cards": [],
	}
	_collect_runtime_node_inventory(main.castle_room_world_root, inventory)
	var node_types: Dictionary = inventory["node_types"] as Dictionary
	var sprite_summary: Dictionary = inventory["sprite3d"] as Dictionary
	var forbidden_types := {
		"Sprite2D": int(node_types.get("Sprite2D", 0)),
		"AnimatedSprite2D": int(node_types.get("AnimatedSprite2D", 0)),
		"TextureRect": int(node_types.get("TextureRect", 0)),
		"Polygon2D": int(node_types.get("Polygon2D", 0)),
		"MeshInstance3D": int(node_types.get("MeshInstance3D", 0)),
		"MultiMeshInstance3D": int(node_types.get("MultiMeshInstance3D", 0)),
		"CSGShape3D": int(node_types.get("CSGShape3D", 0)),
	}
	var forbidden_total := 0
	for forbidden_count: Variant in forbidden_types.values():
		forbidden_total += int(forbidden_count)
	var roles: Dictionary = inventory["world_art_roles"] as Dictionary
	var validation := {
		"registered_background_cards": main.castle_room_background_tiles.size(),
		"door_sign_cards": int(roles.get("room_door_sign", 0)),
		"royal_hall_mist_cards": int(roles.get("royal_hall_mist", 0)),
		"retained_throne_cards": int(roles.get(
			"retained_huluu_throne", 0)),
		"forbidden_world_art_nodes": forbidden_types,
		"forbidden_world_art_total": forbidden_total,
		"all_sprite3d_unshaded": int(sprite_summary["shaded"]) == 0,
		"all_sprite3d_depth_tested": int(sprite_summary["depth_tested"]) \
			== int(sprite_summary["total"]),
		"all_sprite3d_textured": int(sprite_summary["missing_texture"]) == 0,
	}
	validation["structural_pass"] = \
		int(validation["registered_background_cards"]) == HALL_TILE_COUNT \
		and int(validation["door_sign_cards"]) == 8 \
		and int(validation["royal_hall_mist_cards"]) \
			== ROYAL_HALL_MIST_SPECS.size() \
		and int(validation["retained_throne_cards"]) == 0 \
		and forbidden_total == 0 \
		and bool(validation["all_sprite3d_unshaded"]) \
		and bool(validation["all_sprite3d_depth_tested"]) \
		and bool(validation["all_sprite3d_textured"])
	inventory["validation"] = validation
	var requested: String = OS.get_environment("CASTLE_NODE_INVENTORY_OUT")
	var output_path: String = requested if requested != "" else \
		ProjectSettings.globalize_path(
			"res://audit/castle_sprite3d/" \
			+ "castle_main_hall_redraw_2026-08-03_node_inventory.json")
	DirAccess.make_dir_recursive_absolute(output_path.get_base_dir())
	var output: FileAccess = FileAccess.open(output_path, FileAccess.WRITE)
	if output == null:
		return false
	output.store_string(JSON.stringify(inventory, "\t", false) + "\n")
	output.close()
	return bool(validation["structural_pass"])

func _run() -> void:
	var main_scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = main_scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	main._skip_intro()
	main.pearl_count = main.PEARL_TOTAL
	for friend_value: Variant in main.friends:
		var friend: Dictionary = friend_value
		friend["found"] = true
		friend["won"] = true
	# The trusted suite reuses one isolated profile. Earlier probes may complete
	# this additive rescue, so establish the authored pre-rescue state explicitly
	# before auditing its three depth cards, camera rays, and navigation contacts.
	main.companion_id = ""
	for rescue_key: String in [
			"rescued_eagle", "rescued_eagle_pin_left",
			"rescued_eagle_pin_right"]:
		main.stuffie_wins.erase(rescue_key)
	main.g["castle_dust_bunnies_cleared"] = {}
	main.trophies = 5
	main.level2_done_once = true
	main._enter_level2_now(true, false, false)
	await _frames(12)
	main._enter_castle_interior_now(false)
	await _frames(18)

	var rooms: CastleRooms25D = main._castle_rooms_ref()
	_ck("room_stage_open", rooms.is_open())
	_ck("perspective_depth_camera",
		main.castle_room_camera != null
		and main.castle_room_camera.projection
			== Camera3D.PROJECTION_PERSPECTIVE)
	_ck("legacy_3d_hall_not_instantiated",
		main.game_nodes.is_empty()
		and main.arena_solids.is_empty()
		and main.arena_zones.is_empty()
		and not main.g.has("hall_exit")
		and not main.g.has("opera_gate"))
	var unique_route_buttons: Dictionary = {}
	var physical_routes_ok := (
		main.castle_room_buttons.size() == HALL_DESTINATION_IDS.size()
		and main.castle_room_door_hotspot_layer != null)
	for room_id: String in HALL_DESTINATION_IDS:
		var room_button: Button = main.castle_room_buttons.get(room_id) as Button
		physical_routes_ok = physical_routes_ok \
			and room_button != null \
			and room_button.get_parent() == main.castle_room_door_hotspot_layer \
			and room_button.name == "HallDoor_" + room_id
		if room_button != null:
			unique_route_buttons[room_button.get_instance_id()] = true
	_ck("main_hall_has_one_physical_route_per_room",
		physical_routes_ok
		and unique_route_buttons.size() == HALL_DESTINATION_IDS.size(),
		"routes=%d unique=%d" % [
			main.castle_room_buttons.size(), unique_route_buttons.size()])
	var elevator_button: Button = main.castle_room_stage.get_node_or_null(
		"ElevatorButton") as Button
	var elevator_pointer: Label = main.castle_room_stage.get_node_or_null(
		"ElevatorPointer") as Label
	var elevator_inventory_ok := (
		elevator_button != null
		and elevator_pointer != null
		and main.castle_room_menu_panel != null
		and not main.castle_room_menu_panel.visible
		and main.castle_room_menu_buttons.size() == ELEVATOR_ROOM_IDS.size()
		and not main.castle_room_menu_buttons.has("family_gallery"))
	var elevator_icon_manifest: Dictionary = _load_interaction_manifest(
		ELEVATOR_ICON_MANIFEST)
	var elevator_icon_records: Dictionary = {}
	for icon_record_value: Variant in elevator_icon_manifest.get(
			"icons", []) as Array:
		var icon_record: Dictionary = icon_record_value as Dictionary
		elevator_icon_records[String(icon_record.get("room_id", ""))] = \
			icon_record
	var elevator_collection_audit: Dictionary = elevator_icon_manifest.get(
		"collection_audit", {}) as Dictionary
	var elevator_after_audit: Dictionary = elevator_collection_audit.get(
		"after", {}) as Dictionary
	elevator_inventory_ok = elevator_inventory_ok \
		and int(elevator_icon_manifest.get("schema_version", 0)) == 2 \
		and int(elevator_icon_manifest.get("output_count", 0)) \
			== ELEVATOR_ROOM_IDS.size() \
		and not bool(elevator_icon_manifest.get("uses_image_generation", true)) \
		and float(elevator_collection_audit.get(
			"threshold_out_of_5", 0.0)) == 4.5 \
		and float(elevator_after_audit.get("overall", 0.0)) >= 4.5 \
		and String(elevator_after_audit.get("status", "")) \
			== "accepted_shared_door_crest_family" \
		and elevator_icon_records.size() == ELEVATOR_ROOM_IDS.size()
	var elevator_button_instances: Dictionary = {}
	for elevator_room_id: String in ELEVATOR_ROOM_IDS:
		var menu_button: Button = main.castle_room_menu_buttons.get(
			elevator_room_id) as Button
		var expected_icon_path := \
			"res://assets/ui/castle_room_buttons_v2/room_%s.png" \
			% elevator_room_id
		var icon_record: Dictionary = elevator_icon_records.get(
			elevator_room_id, {}) as Dictionary
		elevator_inventory_ok = elevator_inventory_ok \
			and menu_button != null \
			and menu_button.name == "ElevatorRoom_" + elevator_room_id \
			and menu_button.size.x >= StorybookUI.MIN_TOUCH.x \
			and menu_button.size.y >= StorybookUI.MIN_TOUCH.y \
			and menu_button.text.is_empty() \
			and menu_button.icon != null \
			and menu_button.icon.get_size() == Vector2(256.0, 256.0) \
			and menu_button.icon.resource_path == expected_icon_path \
			and menu_button.expand_icon \
			and String(menu_button.get_meta(
				"castle_room_destination", "")) == elevator_room_id
		elevator_inventory_ok = elevator_inventory_ok \
			and String(menu_button.get_meta(
				"castle_room_icon_path", "")) == expected_icon_path \
			and String(menu_button.get_meta(
				"castle_room_icon_family", "")) \
				== "pearl_castle_scallop_crest" \
			and String(icon_record.get("output", "")) \
				== expected_icon_path.trim_prefix("res://") \
			and FileAccess.get_sha256(ProjectSettings.globalize_path(
				expected_icon_path)) == String(icon_record.get(
					"output_sha256", ""))
		if menu_button != null:
			elevator_button_instances[menu_button.get_instance_id()] = true
	_ck("storybook_elevator_has_one_cohesive_twelve_crest_family",
		elevator_inventory_ok
		and elevator_button_instances.size() == ELEVATOR_ROOM_IDS.size()
		and elevator_button.size.x >= StorybookUI.MIN_TOUCH.x
		and elevator_button.size.y >= StorybookUI.MIN_TOUCH.y)
	_ck("contextual_back_remains_beside_elevator",
		main.castle_room_back_button != null
		and main.castle_room_back_button.name == "CastleBack"
		and main.castle_room_back_button.tooltip_text == "Castle courtyard")
	_ck("main_hall_redraw_has_no_legacy_architecture_overlays",
		main.castle_room_mid_layer.get_node_or_null(
			"HallStructure_family_wing_entry") == null
		and main.castle_room_mid_layer.get_node_or_null(
			"HallStructure_playroom_portal_bridge") == null
		and main.castle_room_mid_layer.get_node_or_null(
			"HallStructure_playroom_portal_marker") == null)
	var hall_portal_rects: Dictionary = {}
	var hall_portal_buttons: Dictionary = {}
	for hall_portal_record: Dictionary in main.castle_room_door_hotspots:
		var hall_portal_data: Dictionary = hall_portal_record.get("data", {})
		if not hall_portal_data.is_empty():
			var hall_portal_id: String = String(hall_portal_data["id"])
			hall_portal_rects[hall_portal_id] = \
				hall_portal_data["rect"]
			hall_portal_buttons[hall_portal_id] = hall_portal_record.get("button")
	var hall_sign_count := 0
	var craft_sign_count := 0
	var hall_signs_ok := true
	for hall_mid_child: Node in main.castle_room_mid_layer.get_children():
		if not String(hall_mid_child.name).begins_with("HallDoorSign_"):
			continue
		hall_sign_count += 1
		var hall_sign: Sprite3D = hall_mid_child as Sprite3D
		var sign_destination: String = String(hall_sign.get_meta(
			"room_destination", "")) if hall_sign != null else ""
		var portal_rect: Rect2 = hall_portal_rects.get(
			sign_destination, Rect2()) as Rect2
		var expected_sign_file: String = String(HALL_SIGN_FILES.get(
			sign_destination, ""))
		var expected_sign_scale: float = 1.0 \
			if sign_destination == "family_gallery" else 1.55 \
			if sign_destination == "opera_hall" else 1.0
		var sign_art_position := Vector2.INF
		if hall_sign != null:
			sign_art_position = hall_sign.get_meta(
				"source_art_position", Vector2.INF) as Vector2
		hall_signs_ok = hall_signs_ok \
			and hall_sign != null and hall_sign.texture != null \
			and not hall_sign.shaded \
			and hall_sign.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD \
			and String(hall_sign.get_meta("source_asset_role", "")) \
				== "room_door_sign" \
			and expected_sign_file != "" \
			and hall_sign.texture.resource_path.ends_with(expected_sign_file) \
			and is_equal_approx(hall_sign.scale.x, expected_sign_scale) \
			and HALL_DESTINATION_IDS.has(sign_destination) \
			and portal_rect.has_area() \
			and absf(sign_art_position.x - portal_rect.get_center().x) \
				<= portal_rect.size.x * 0.25 \
			and sign_art_position.y <= portal_rect.position.y \
				+ portal_rect.size.y * 0.20
		if sign_destination == "craft_room":
			craft_sign_count += 1
	_ck("main_hall_has_one_separate_sprite3d_sign_per_destination",
		hall_signs_ok
		and hall_sign_count == HALL_DESTINATION_IDS.size()
		and craft_sign_count == 1,
		"signs=%d craft=%d" % [hall_sign_count, craft_sign_count])
	var left_door_button: Button = main.castle_room_buttons.get(
		"family_gallery") as Button
	var left_door_rect: Rect2 = hall_portal_rects.get(
		"family_gallery", Rect2()) as Rect2
	var left_door_sign: Sprite3D = main.castle_room_mid_layer.get_node_or_null(
		"HallDoorSign_family_gallery") as Sprite3D
	_ck("main_hall_left_end_dream_house_door_is_clear_and_signed",
		left_door_button != null and left_door_button.visible
		and left_door_rect == Rect2(210.0, 300.0, 160.0, 305.0)
		and left_door_sign != null and left_door_sign.visible
		and left_door_sign.texture != null
		and left_door_sign.texture.resource_path.ends_with(
			"sign_family_gallery.png"))
	var retired_throne_count := 0
	for royal_mid_child: Node in main.castle_room_mid_layer.get_children():
		if royal_mid_child.name == "HallRetainedHuluuThrone" \
				or String(royal_mid_child.get_meta(
					"source_asset_role", "")) == "retained_huluu_throne":
			retired_throne_count += 1
	_ck("main_hall_runtime_retires_throne_overlay",
		retired_throne_count == 0
		and main.castle_room_mid_layer.get_node_or_null(
			"HallRetainedHuluuThrone") == null,
		"retained throne cards=%d" % retired_throne_count)
	var royal_hall_portal_rect: Rect2 = hall_portal_rects.get(
		ROYAL_HALL_PORTAL_ID, Rect2()) as Rect2
	var royal_hall_button: Button = hall_portal_buttons.get(
		ROYAL_HALL_PORTAL_ID) as Button
	_ck("main_hall_far_right_endpoint_is_royal_hall_event_gate",
		royal_hall_portal_rect == Rect2(2870.0, 150.0, 350.0, 470.0)
		and royal_hall_button != null
		and royal_hall_button.tooltip_text == "Royal Hall"
		and not hall_portal_rects.has("__throne"))
	var mist_image: Image
	var mist_alpha_rect := Rect2i()
	var mist_structure_ok := \
		main.castle_royal_hall_mist_cards.size() \
			== ROYAL_HALL_MIST_SPECS.size()
	var mist_detail: Array[String] = []
	for mist_index: int in range(ROYAL_HALL_MIST_SPECS.size()):
		var expected_mist: Dictionary = ROYAL_HALL_MIST_SPECS[mist_index]
		var mist: Sprite3D = main.castle_room_mid_layer.get_node_or_null(
			"RoyalHallMist_%d" % mist_index) as Sprite3D
		if mist == null or mist.texture == null:
			mist_structure_ok = false
			mist_detail.append("%d:missing" % mist_index)
			continue
		if mist_image == null:
			mist_image = _sheet_image(mist.texture)
			mist_alpha_rect = _alpha_visible_rect(mist_image)
		var art_position: Vector2 = expected_mist["pos"] as Vector2
		var visual_scale: float = float(expected_mist["scale"])
		var depth_z: float = float(expected_mist["z"])
		var rest_alpha: float = float(expected_mist["alpha"])
		var texture_size: Vector2 = mist.texture.get_size()
		var expected_art_rect := Rect2(
			art_position - texture_size * visual_scale * 0.5,
			texture_size * visual_scale)
		var visible_rect := Rect2(
			art_position + (Vector2(mist_alpha_rect.position)
				- texture_size * 0.5) * visual_scale,
			Vector2(mist_alpha_rect.size) * visual_scale)
		var source_art_rect: Rect2 = mist.get_meta(
			"source_art_rect", Rect2()) as Rect2
		var cull_rect: Rect2 = mist.get_meta(
			"hall_horizontal_cull_rect", Rect2()) as Rect2
		var rest_scale: Vector3 = mist.get_meta(
			"mist_rest_scale", Vector3.ZERO) as Vector3
		var contained: bool = royal_hall_portal_rect.has_area() \
			and visible_rect.position.x >= royal_hall_portal_rect.position.x \
			and visible_rect.end.x <= royal_hall_portal_rect.end.x \
			and visible_rect.position.y >= royal_hall_portal_rect.position.y \
			and visible_rect.end.y <= royal_hall_portal_rect.end.y
		mist_structure_ok = mist_structure_ok \
			and mist.texture.resource_path == ROYAL_HALL_MIST_TEXTURE \
			and mist.texture.get_size() == Vector2(46.0, 256.0) \
			and not mist.shaded and not mist.no_depth_test \
			and mist.cast_shadow \
				== GeometryInstance3D.SHADOW_CASTING_SETTING_OFF \
			and mist.transparent \
			and mist.alpha_cut == SpriteBase3D.ALPHA_CUT_DISABLED \
			and String(mist.get_meta("source_asset_role", "")) \
				== "royal_hall_mist" \
			and String(mist.get_meta("source_object_id", "")) \
				== "main_hall:royal_hall_mist_%d" % mist_index \
			and String(mist.get_meta("source_asset_path", "")) \
				== ROYAL_HALL_MIST_TEXTURE \
			and (mist.get_meta("source_art_position", Vector2.INF) \
				as Vector2).is_equal_approx(art_position) \
			and source_art_rect.is_equal_approx(expected_art_rect) \
			and cull_rect.is_equal_approx(source_art_rect) \
			and bool(mist.get_meta("hall_horizontal_cull", false)) \
			and String(mist.get_meta("hall_horizontal_cull_kind", "")) \
				== "royal_hall_mist" \
			and is_equal_approx(float(mist.get_meta("depth_z", -1.0)), depth_z) \
			and is_equal_approx(mist.position.z, depth_z) \
			and rest_scale.is_equal_approx(Vector3.ONE * visual_scale) \
			and is_equal_approx(float(mist.get_meta(
				"mist_rest_alpha", -1.0)), rest_alpha) \
			and contained
		mist_detail.append("%d:%s" % [mist_index, visible_rect])
	_ck("main_hall_has_five_audited_royal_hall_mist_sprite3d_cards",
		mist_structure_ok
		and mist_image != null
		and mist_alpha_rect == ROYAL_HALL_MIST_ALPHA_RECT
		and FileAccess.get_sha256(ProjectSettings.globalize_path(
			ROYAL_HALL_MIST_TEXTURE)) == ROYAL_HALL_MIST_TEXTURE_SHA256,
		"alpha=%s cards=%s" % [mist_alpha_rect, mist_detail])
	var original_companion_id: String = main.companion_id
	var original_level2_done_once: bool = main.level2_done_once
	main.level2_done_once = true
	main.companion_id = "mewsha"
	main.castle_room_camera.position = Vector3(
		rooms._hall_camera_x_for_foot(3045.0), 0.0,
		main.castle_room_camera.position.z)
	rooms._sync_hall_horizontal_culling()
	rooms._force_clear_royal_hall_event()
	rooms._tick_royal_hall_mist(1.0)
	var resting_mist_visible := true
	for resting_index: int in range(main.castle_royal_hall_mist_cards.size()):
		var resting_mist: Sprite3D = \
			main.castle_royal_hall_mist_cards[resting_index]
		var expected_rest_alpha: float = float(
			ROYAL_HALL_MIST_SPECS[resting_index]["alpha"])
		resting_mist_visible = resting_mist_visible \
			and resting_mist.visible \
			and resting_mist.modulate.a >= expected_rest_alpha * 0.90 \
			and resting_mist.modulate.a <= expected_rest_alpha * 1.01
	_ck("royal_hall_mist_seals_gate_while_no_major_event_is_armed",
		resting_mist_visible and rooms._royal_hall_event_id().is_empty())
	royal_hall_probe_entry_calls = 0
	royal_hall_probe_consumed_before_entry = false
	var royal_event_armed: bool = rooms.arm_royal_hall_event(
		"probe_major_event", Callable(self, "_on_royal_hall_probe_entry"))
	var royal_event_generation: int = rooms.royal_hall_event_token(
		"probe_major_event")
	rooms._tick_royal_hall_mist(1.0)
	var armed_mist_hidden := true
	for armed_mist: Sprite3D in main.castle_royal_hall_mist_cards:
		armed_mist_hidden = armed_mist_hidden \
			and not armed_mist.visible and armed_mist.modulate.a <= 0.012
	_ck("royal_hall_mist_clears_only_for_armed_major_event",
		royal_event_armed and armed_mist_hidden
		and rooms._royal_hall_event_id() == "probe_major_event")
	var royal_hall_foot := Vector2(3045.0, 620.0)
	rooms._position_player_at_foot(royal_hall_foot, false)
	main.castle_royal_hall_arrival_generation += 1
	main.castle_royal_hall_arrival_pending = true
	rooms._activate_royal_hall_event(
		main.castle_royal_hall_arrival_generation,
		"probe_major_event", royal_event_generation, royal_hall_foot)
	_ck("royal_hall_armed_callback_is_consumed_before_one_shot_entry",
		royal_hall_probe_entry_calls == 1
		and royal_hall_probe_consumed_before_entry
		and main.castle_royal_hall_event_id.is_empty()
		and not main.castle_royal_hall_event_entry.is_valid())
	rooms._tick_royal_hall_mist(1.0)
	var family_sign_image: Image = _sheet_image(left_door_sign.texture) \
		if left_door_sign != null else null
	var family_alpha_rect := _alpha_visible_rect(family_sign_image)
	var playroom_sign: Sprite3D = main.castle_room_mid_layer.get_node_or_null(
		"HallDoorSign_playroom") as Sprite3D
	var playroom_sign_image: Image = _sheet_image(playroom_sign.texture) \
		if playroom_sign != null else null
	var playroom_alpha_rect := _alpha_visible_rect(playroom_sign_image)
	var family_sign_position: Vector2 = left_door_sign.get_meta(
		"source_art_position", Vector2.INF) as Vector2 \
		if left_door_sign != null else Vector2.INF
	var playroom_sign_position: Vector2 = playroom_sign.get_meta(
		"source_art_position", Vector2.INF) as Vector2 \
		if playroom_sign != null else Vector2.INF
	var sign_reuse_manifest: Dictionary = _load_interaction_manifest(
		HALL_SIGN_REUSE_MANIFEST)
	var sign_collection_audit: Dictionary = sign_reuse_manifest.get(
		"collection_audit", {}) as Dictionary
	var sign_scores: Dictionary = sign_collection_audit.get(
		"per_icon_overall_scores", {}) as Dictionary
	var family_score: Dictionary = sign_scores.get(
		"family_gallery", {}) as Dictionary
	var playroom_score: Dictionary = sign_scores.get(
		"playroom", {}) as Dictionary
	_ck("main_hall_family_and_playroom_icons_are_cohesive_approved_crests",
		family_sign_image != null
		and family_sign_image.get_size() == Vector2i(256, 256)
		and family_alpha_rect == FAMILY_SIGN_ALPHA_RECT
		and FileAccess.get_sha256(ProjectSettings.globalize_path(
			left_door_sign.texture.resource_path)) == FAMILY_SIGN_SHA256
		and is_equal_approx(left_door_sign.scale.x, 1.0)
		and family_sign_position.is_equal_approx(Vector2(290.0, 340.0))
		and playroom_sign != null and playroom_sign.texture != null
		and playroom_sign.texture.resource_path.ends_with("sign_playroom.png")
		and playroom_sign_image != null
		and playroom_sign_image.get_size() == Vector2i(256, 256)
		and playroom_alpha_rect == PLAYROOM_SIGN_ALPHA_RECT
		and FileAccess.get_sha256(ProjectSettings.globalize_path(
			playroom_sign.texture.resource_path)) == PLAYROOM_SIGN_SHA256
		and is_equal_approx(playroom_sign.scale.x, 1.0)
		and playroom_sign_position.is_equal_approx(Vector2(2015.0, 340.0))
		and Vector2(family_alpha_rect.get_center()).distance_to(
			Vector2(128.0, 128.0)) <= 1.0
		and Vector2(playroom_alpha_rect.get_center()).distance_to(
			Vector2(128.0, 128.0)) <= 1.0
		and FileAccess.get_sha256(ProjectSettings.globalize_path(
			HALL_SIGN_REUSE_MANIFEST)) == HALL_SIGN_REUSE_MANIFEST_SHA256
		and String(sign_collection_audit.get("schema", "")) \
			== "castle_main_hall_physical_sign_audit_v1"
		and is_equal_approx(float(sign_collection_audit.get(
			"threshold_out_of_5", 0.0)), 4.5)
		and float(family_score.get("after", 0.0)) >= 4.5
		and String(family_score.get("status", "")) == "corrected_pass"
		and float(playroom_score.get("overall", 0.0)) >= 4.5
		and String(playroom_score.get("status", "")) \
			== "accepted_preserved",
		"family=%s playroom=%s" % [family_alpha_rect, playroom_alpha_rect])
	var left_camera_position := Vector3(
		rooms._hall_camera_x_for_foot(380.0), 0.0,
		main.castle_room_camera.position.z)
	main.castle_room_camera.position = left_camera_position
	rooms._sync_hall_horizontal_culling()
	rooms._update_hall_portals()
	var left_cull_snapshot: Dictionary = _hall_cull_snapshot()
	var left_local_sconce_record: Dictionary = \
		main.castle_room_item_sprites.get("sconce_a0", {}) as Dictionary
	var left_remote_sconce_record: Dictionary = \
		main.castle_room_item_sprites.get("sconce_b2", {}) as Dictionary
	var left_local_sconce: Sprite3D = \
		left_local_sconce_record.get("sprite") as Sprite3D
	var left_local_hotspot: Button = \
		left_local_sconce_record.get("hotspot") as Button
	var left_remote_sconce: Sprite3D = \
		left_remote_sconce_record.get("sprite") as Sprite3D
	var left_remote_hotspot: Button = \
		left_remote_sconce_record.get("hotspot") as Button
	var left_interaction_cull_ok: bool = left_local_sconce != null \
		and left_local_sconce.visible \
		and left_local_hotspot != null and left_local_hotspot.visible \
		and left_remote_sconce != null and not left_remote_sconce.visible \
		and left_remote_hotspot != null and not left_remote_hotspot.visible
	var hall_tile_inventory_complete: bool = \
		main.castle_room_background_tiles.size() == HALL_TILE_COUNT
	var left_tile_endpoints_ok := false
	if hall_tile_inventory_complete:
		left_tile_endpoints_ok = \
			main.castle_room_background_tiles[0].visible \
			and main.castle_room_background_tiles[HALL_TILE_COLUMNS].visible \
			and not main.castle_room_background_tiles[7].visible \
			and not main.castle_room_background_tiles[15].visible
	var right_door_button: Button = main.castle_room_buttons.get(
		"bubble_bath") as Button
	var right_door_sign: Sprite3D = main.castle_room_mid_layer.get_node_or_null(
		"HallDoorSign_bubble_bath") as Sprite3D
	main.castle_room_camera.position = Vector3(
		rooms._hall_camera_x_for_foot(3045.0), 0.0,
		left_camera_position.z)
	rooms._sync_hall_horizontal_culling()
	rooms._update_hall_portals()
	var right_cull_snapshot: Dictionary = _hall_cull_snapshot()
	var right_interaction_cull_ok: bool = left_local_sconce != null \
		and not left_local_sconce.visible \
		and left_local_hotspot != null and not left_local_hotspot.visible \
		and left_remote_sconce != null and left_remote_sconce.visible \
		and left_remote_hotspot != null and left_remote_hotspot.visible \
		and String(left_remote_sconce.get_meta(
			"hall_horizontal_cull_kind", "")) == "interaction" \
		and (left_remote_sconce.get_meta(
			"hall_horizontal_cull_rect", Rect2()) as Rect2).has_area()
	var right_tile_endpoints_ok := false
	if hall_tile_inventory_complete:
		right_tile_endpoints_ok = \
			main.castle_room_background_tiles[7].visible \
			and main.castle_room_background_tiles[15].visible \
			and not main.castle_room_background_tiles[0].visible \
			and not main.castle_room_background_tiles[HALL_TILE_COLUMNS].visible
	var right_mist_visible: bool = \
		main.castle_royal_hall_mist_cards.size() \
			== ROYAL_HALL_MIST_SPECS.size()
	for right_mist: Sprite3D in main.castle_royal_hall_mist_cards:
		right_mist_visible = right_mist_visible and right_mist.visible
	var right_endpoints_ok: bool = right_door_button != null \
		and right_door_button.visible \
		and right_door_sign != null and right_door_sign.visible \
		and royal_hall_button != null and royal_hall_button.visible \
		and right_mist_visible
	_ck("main_hall_horizontal_sprite3d_culling_preserves_endpoints",
		bool(left_cull_snapshot["metadata_ok"])
		and bool(right_cull_snapshot["metadata_ok"])
		and int(left_cull_snapshot["inventory"]) == 29
		and int(left_cull_snapshot["backgrounds"]) == HALL_TILE_COUNT
		and int(left_cull_snapshot["signs"]) == 8
		and int(left_cull_snapshot["royal_hall_mist_cards"]) \
			== ROYAL_HALL_MIST_SPECS.size()
		and int(left_cull_snapshot["visible_backgrounds"]) >= 8
		and int(left_cull_snapshot["visible_backgrounds"]) <= 12
		and int(left_cull_snapshot["visible_signs"]) == 4
		and int(left_cull_snapshot[
			"visible_royal_hall_mist_cards"]) == 0
		and int(left_cull_snapshot["visible"]) <= 16
		and int(right_cull_snapshot["visible_backgrounds"]) >= 8
		and int(right_cull_snapshot["visible_backgrounds"]) <= 12
		and int(right_cull_snapshot["visible_signs"]) == 4
		and int(right_cull_snapshot[
			"visible_royal_hall_mist_cards"]) \
			== ROYAL_HALL_MIST_SPECS.size()
		and int(right_cull_snapshot["visible"]) <= 21
		and left_tile_endpoints_ok and right_tile_endpoints_ok
		and right_endpoints_ok
		and left_interaction_cull_ok and right_interaction_cull_ok,
		"left=%s right=%s" % [left_cull_snapshot, right_cull_snapshot])
	main.castle_room_camera.position = left_camera_position
	rooms._sync_hall_horizontal_culling()
	rooms._update_hall_portals()
	_ck("main_hall_runtime_node_type_inventory",
		_write_main_hall_node_inventory())
	rooms._position_player_at_foot(Vector2(380.0, 835.0), false)
	await _frames(2)
	rooms.tick(1.0)
	main.castle_room_camera.position = left_camera_position
	rooms._sync_hall_horizontal_culling()
	rooms._update_hall_portals()
	await _capture("main_hall_screen_a")
	# Fast rendered review mode for iterative hall polish. The normal trusted
	# probe continues below; this opt-in path only stages A/seam/B plus the
	# omnipresent elevator so visual audits do not replay every room animation.
	if OS.get_environment("CASTLE_HALL_CAPTURE_ONLY") == "1":
		rooms._position_player_at_foot(Vector2(1672.0, 835.0), false)
		await _frames(2)
		rooms.tick(1.0)
		await _capture("main_hall_seam_bridge")
		rooms._position_player_at_foot(Vector2(2500.0, 835.0), false)
		await _frames(2)
		rooms.tick(1.0)
		await _capture("main_hall_screen_b")
		elevator_button.pressed.emit()
		await _frames(2)
		await _capture("elevator_menu")
		print("CASTLE_ART|RESULT=",
			"FAIL" if checks_failed > 0 else "OK",
			" checks_failed=", checks_failed)
		quit(1 if checks_failed > 0 else 0)
		return
	main.companion_id = original_companion_id
	main.level2_done_once = original_level2_done_once
	rooms._force_clear_royal_hall_event()
	rooms._tick_royal_hall_mist(1.0)
	rooms.show_room("family_gallery", false)
	await _frames(2)
	var gallery_destinations := {
		"gallery_dining_door": "dining_room",
		"gallery_royal_bedroom_door": "royal_bedroom",
		"gallery_sleepover_door": "sleepover_bedroom",
		"gallery_movie_door": "movie_lounge",
	}
	var gallery_doors_ok := true
	for item_id: String in gallery_destinations:
		var gallery_record: Dictionary = main.castle_room_item_sprites.get(
			item_id, {}) as Dictionary
		var gallery_sprite: Sprite3D = gallery_record.get("sprite") as Sprite3D
		var gallery_hotspot: Button = gallery_record.get("hotspot") as Button
		var destination: String = String(gallery_destinations[item_id])
		gallery_doors_ok = (
			gallery_doors_ok
			and gallery_sprite != null
			and gallery_hotspot != null
			and String(gallery_sprite.get_meta(
				"source_asset_role", "")) == "physical_room_door"
			and String(gallery_sprite.get_meta(
				"room_destination", "")) == destination
			and bool(gallery_hotspot.get_meta("physical_door", false))
			and String(gallery_hotspot.get_meta(
				"room_destination", "")) == destination
		)
	_ck("dream_house_gallery_physical_door_inventory",
		gallery_doors_ok
		and main.castle_room_detail_tiles.size() == 4
		and main.castle_room_item_sprites.size() == 4
		and main.castle_room_item_hotspot_layer.get_child_count() == 4
		and not main.castle_room_action_button.visible)
	_ck("dream_house_gallery_has_no_floating_route_buttons",
		main.castle_room_link_layer != null
		and main.castle_room_link_layer.get_child_count() == 0)
	await _capture("family_gallery")
	rooms.show_room("main_hall", false)
	await _frames(2)
	var castle_roshan: Sprite3D = main.castle_room_player_sprite
	var castle_roshan_loop: RoshanSpriteLoop = castle_roshan.get_node_or_null(
		"AlwaysAliveSpriteLoop") as RoshanSpriteLoop
	var castle_frame_height: float = castle_roshan.texture.get_height() \
		/ float(maxi(1, castle_roshan.vframes))
	_ck("castle_roshan_uses_primary_animated_sprite",
		castle_roshan_loop != null
		and castle_roshan.texture.resource_path.ends_with(
			"roshan_directional.png")
		and castle_roshan.hframes == 4
		and castle_roshan.vframes == 2
		and is_equal_approx(castle_frame_height, 256.0))
	var idle_offset: Vector2 = castle_roshan.offset
	castle_roshan_loop._process(0.3)
	_ck("castle_roshan_idle_never_freezes",
		castle_roshan_loop.animation_state() == "idle"
		and castle_roshan.offset != idle_offset,
		"state=%s offset=%s->%s" % [
			castle_roshan_loop.animation_state(), idle_offset,
			castle_roshan.offset])
	var walk_target := Vector2(500.0, 835.0)
	rooms._position_player_at_foot(walk_target, true)
	castle_roshan_loop._process(0.01)
	var moving_frame: int = castle_roshan.frame
	castle_roshan_loop._process(0.3)
	_ck("castle_roshan_swims_when_moving",
		bool(castle_roshan.get_meta("walking", false))
		and castle_roshan_loop.animation_state() == "swim"
		and castle_roshan.texture.resource_path.ends_with(
			"roshan_swim_front.png")
		and castle_roshan.vframes == 4
		and castle_roshan.frame != moving_frame,
		"state=%s frame=%d->%d" % [
			castle_roshan_loop.animation_state(),
			moving_frame, castle_roshan.frame])
	castle_roshan.flip_h = false
	var target_anchor: Vector2 = ROSHAN_ANCHORS.anchor("directional", 0)
	var max_anchor_drift := 0.0
	for frame_index: int in range(16):
		castle_roshan_loop._apply_frame(frame_index)
		# Anchors are measured in nominal cell space, but the sampled window is
		# nudged onto the figure so the lower rows keep her whole head
		# (RoshanSpriteFrames). Rebase the anchor onto that window before
		# checking that every frame still shares one torso point.
		var frame_anchor: Vector2 = ROSHAN_ANCHORS.anchor(
			"swim_front", frame_index) \
			- ROSHAN_FRAMES.shift("swim_front", frame_index)
		var frame_offset: Vector2 = castle_roshan.get_meta(
			"roshan_anchor_offset", Vector2.ZERO) as Vector2
		var corrected_anchor := Vector2(
			frame_anchor.x + frame_offset.x,
			frame_anchor.y - frame_offset.y)
		max_anchor_drift = maxf(
			max_anchor_drift, corrected_anchor.distance_to(target_anchor))
	_ck("castle_roshan_frames_share_anatomical_anchor",
		max_anchor_drift <= 0.11,
		"max_torso_drift_px=%.3f" % max_anchor_drift)
	_check_roshan_sampling_windows()
	_ck("castle_roshan_samples_her_own_window",
		ROSHAN_FRAMES.sampled_rect(castle_roshan).is_equal_approx(
			ROSHAN_FRAMES.region(castle_roshan_loop._sheet_key(),
				castle_roshan.frame, castle_roshan.hframes)),
		"sheet=%s frame=%d sampled=%s" % [
			castle_roshan_loop._sheet_key(), castle_roshan.frame,
			ROSHAN_FRAMES.sampled_rect(castle_roshan)])
	rooms._position_player_at_foot(Vector2(380.0, 835.0), false)
	castle_roshan_loop._process(0.2)
	_ck("castle_roshan_swim_finishes_at_arrival",
		castle_roshan_loop.animation_state() == "idle"
		and castle_roshan.texture.resource_path.ends_with(
			"roshan_directional.png")
		and castle_roshan.vframes == 2,
		"state=%s texture=%s" % [
			castle_roshan_loop.animation_state(),
			castle_roshan.texture.resource_path])

	var all_rooms_ok := true
	var room_structure_failures: Array[Dictionary] = []
	var all_depth_ok := true
	# LIGHTING_2P5D_AUDIT_2026-08-02 §E2: depth must be TONAL as well as
	# geometric. Foreground framing cards are multiplied by the light rig's
	# near tint so they settle back out of the room's light pool; the
	# background plate stays the untouched reference. A regression that
	# silently stops applying the rig leaves every plane at pure white again.
	var all_depth_tint_ok := true
	var saw_tinted_foreground := false
	var all_interaction_contracts_ok := true
	var all_semantic_sequences_ok := true
	var all_fixed_pivot_sequences_ok := true
	var all_item_audio_ok := true
	var all_busy_guards_ok := true
	var all_fixture_uv_resets_ok := true
	var all_water_profiles_ok := true
	var all_jolt_motion_ok := true
	var all_jolt_settles_ok := true
	var fridge_door_then_menu_ok := false
	var kitchen_pan_rack_group_ok := false
	var kitchen_normalized_use_examples_ok := false
	var approved_composite_backdrops_ok := true
	var all_detail_tile_grids_ok := true
	var all_room_object_bounds_ok := true
	var opera_split_hotspots_ok := false
	var pool_split_hotspots_ok := false
	var pool_interaction_set_ok := false
	var pool_waterfall_hotspot_ok := false
	var opera_split_overlap := 1.0
	var pool_split_overlap := 1.0
	var kitchen_prop_set_ok := false
	var kitchen_menu_empty_filter_ok := false
	var kitchen_menu_inventory_ok := false
	var kitchen_cooking_portal_ok := false
	var playroom_rescue_cards_ok := false
	var playroom_rescue_ray_ok := false
	var playroom_rescue_route_ok := false
	var max_visible_world_cards := 0
	var visible_card_peaks: Dictionary = {}
	var interaction_failures: Array[String] = []
	var interaction_manifest: Dictionary = _interaction_manifest()
	var active_manifest_assets: Dictionary = _manifest_assets_by_instance(
		interaction_manifest)
	var legacy_interaction_manifest: Dictionary = \
		_load_interaction_manifest(LEGACY_INTERACTION_MANIFEST)
	var legacy_pool_assets: Dictionary = _legacy_pool_assets_by_instance(
		legacy_interaction_manifest)
	var manifest_assets: Dictionary = active_manifest_assets.duplicate(true)
	manifest_assets.merge(legacy_pool_assets, true)
	var expected_physical_total := 0
	for expected_count_value: Variant in EXPECTED_PHYSICAL_ITEM_COUNTS.values():
		expected_physical_total += int(expected_count_value)
	var delivered_average := float(expected_physical_total) \
		/ float(EXPECTED_PHYSICAL_ITEM_COUNTS.size())
	var active_physical_total: int = expected_physical_total \
		- EXPECTED_LEGACY_POOL_ASSET_COUNT
	var manifest_rooms: Dictionary = interaction_manifest.get(
		"rooms", {}) as Dictionary
	var manifest_contract: Dictionary = interaction_manifest.get(
		"contract", {}) as Dictionary
	var manifest_frame_contract: Dictionary = interaction_manifest.get(
		"frame_contract", {}) as Dictionary
	var manifest_summary: Dictionary = interaction_manifest.get(
		"summary", {}) as Dictionary
	var manifest_unique_assets: Array = interaction_manifest.get(
		"assets", []) as Array
	var retired_rooms: Dictionary = interaction_manifest.get(
		"retired_rooms", {}) as Dictionary
	var visual_review_evidence: Dictionary = interaction_manifest.get(
		"visual_review_evidence", {}) as Dictionary
	var manifest_legacy_pool_assets: Array = interaction_manifest.get(
		"legacy_room_derived_assets", []) as Array
	var v2_base_asset_count := 0
	var v3_addition_asset_count := 0
	var active_shader_water_count := 0
	var active_jolt_count := 0
	var retired_pool_v2_absent := true
	for asset_value: Variant in manifest_unique_assets:
		var manifest_asset: Dictionary = asset_value as Dictionary
		var pack := String(manifest_asset.get("pack", ""))
		if pack == "v2_base":
			v2_base_asset_count += 1
			retired_pool_v2_absent = retired_pool_v2_absent \
				and String(manifest_asset.get("room", "")) != "mermaid_pool"
		elif pack == "v3_addition":
			v3_addition_asset_count += 1
		if not (manifest_asset.get("water_layers", []) as Array).is_empty():
			active_shader_water_count += 1
		if String(manifest_asset.get("physics_mode", "none")) != "none":
			active_jolt_count += 1
	var decoded_texture_bytes_by_room: Dictionary = {}
	var decoded_texture_budget_ok := true
	for room_id: String in ROOM_IDS:
		var decoded_bytes := _room_decoded_rgba_bytes(manifest_assets, room_id)
		decoded_texture_bytes_by_room[room_id] = decoded_bytes
		decoded_texture_budget_ok = decoded_texture_budget_ok \
			and decoded_bytes > 0 \
			and decoded_bytes <= ROOM_DECODED_TEXTURE_BUDGET_BYTES
	var interaction_manifest_ok: bool = \
		int(interaction_manifest.get("schema_version", 0)) == 3 \
		and manifest_unique_assets.size() \
			== EXPECTED_ACTIVE_MANIFEST_ASSET_COUNT \
		and active_manifest_assets.size() \
			== EXPECTED_ACTIVE_MANIFEST_INSTANCE_COUNT \
		and manifest_assets.size() == expected_physical_total \
		and expected_physical_total == EXPECTED_OVERALL_PHYSICAL_ITEM_COUNT \
		and int(manifest_summary.get("asset_count", 0)) \
			== EXPECTED_ACTIVE_MANIFEST_ASSET_COUNT \
		and int(manifest_summary.get("physical_instance_count", 0)) \
			== active_physical_total \
		and int(manifest_summary.get("generated_sheet_count", 0)) \
			== EXPECTED_ACTIVE_MANIFEST_ASSET_COUNT \
		and int(manifest_summary.get("v2_base_asset_count", 0)) \
			== EXPECTED_V2_BASE_ASSET_COUNT \
		and int(manifest_summary.get("v3_addition_asset_count", 0)) \
			== EXPECTED_V3_ADDITION_COUNT \
		and int(manifest_summary.get("overall_asset_count", 0)) \
			== EXPECTED_OVERALL_UNIQUE_ASSET_COUNT \
		and int(manifest_summary.get("overall_physical_instance_count", 0)) \
			== EXPECTED_OVERALL_PHYSICAL_ITEM_COUNT \
		and int(manifest_summary.get("water_interaction_count", 0)) \
			== EXPECTED_ACTIVE_SHADER_WATER_COUNT \
		and int(manifest_summary.get("overall_water_interaction_count", 0)) \
			== EXPECTED_OVERALL_WATER_INTERACTION_COUNT \
		and int(manifest_summary.get("jolt_component_count", 0)) \
			== EXPECTED_JOLT_FIXTURE_COUNT \
		and int(manifest_summary.get("missing_count", -1)) == 0 \
		and v2_base_asset_count == EXPECTED_V2_BASE_ASSET_COUNT \
		and v3_addition_asset_count == EXPECTED_V3_ADDITION_COUNT \
		and active_shader_water_count == EXPECTED_ACTIVE_SHADER_WATER_COUNT \
		and active_jolt_count == EXPECTED_JOLT_FIXTURE_COUNT \
		and retired_rooms.has("mermaid_pool") \
		and retired_pool_v2_absent \
		and manifest_legacy_pool_assets.size() \
			== EXPECTED_LEGACY_POOL_ASSET_COUNT \
		and legacy_pool_assets.size() == EXPECTED_LEGACY_POOL_ASSET_COUNT \
		and is_equal_approx(delivered_average, 75.0 / 8.0) \
		and int(manifest_frame_contract.get("minimum", 0)) == 4 \
		and int(manifest_frame_contract.get("maximum", 0)) == 12 \
		and int(manifest_frame_contract.get(
			"delivered_authored_states", 0)) == 8 \
		and int(manifest_frame_contract.get(
			"delivered_timeline_max", 0)) <= 12 \
		and String(manifest_contract.get("water_node_type", "")) == "Sprite3D" \
		and not bool(manifest_contract.get("water_depth_write", true)) \
		and not bool(manifest_contract.get("jolt_logic_authority", true)) \
		and String(visual_review_evidence.get(
			"human_review_status", "")) == "pending" \
		and _v3_addition_visual_contract(manifest_unique_assets) \
		and _dynamic_water_hold_contract(active_manifest_assets)
	var legacy_manifest_rooms: Dictionary = legacy_interaction_manifest.get(
		"rooms", {}) as Dictionary
	for expected_room_id: String in EXPECTED_PHYSICAL_ITEM_COUNTS:
		var manifest_room: Dictionary = manifest_rooms.get(
			expected_room_id, {}) as Dictionary
		var manifest_room_count := int(manifest_room.get(
			"physical_item_count", -1))
		if expected_room_id == "mermaid_pool":
			var legacy_room: Dictionary = legacy_manifest_rooms.get(
				expected_room_id, {}) as Dictionary
			manifest_room_count += int(legacy_room.get(
				"physical_item_count", -1))
		interaction_manifest_ok = interaction_manifest_ok \
			and manifest_room_count \
				== int(EXPECTED_PHYSICAL_ITEM_COUNTS[expected_room_id])
	for room_id: String in ROOM_IDS:
		rooms.show_room(room_id, false)
		await _frames(2)
		if room_id == "opera_hall":
			var stage_star_record: Dictionary = \
				main.castle_room_item_sprites.get("stage_star", {}) as Dictionary
			var footlights_record: Dictionary = \
				main.castle_room_item_sprites.get("footlights", {}) as Dictionary
			var stage_star_hotspot: Button = \
				stage_star_record.get("hotspot") as Button
			var footlights_hotspot: Button = \
				footlights_record.get("hotspot") as Button
			opera_split_overlap = _hotspot_overlap_fraction(
				stage_star_hotspot, footlights_hotspot)
			opera_split_hotspots_ok = stage_star_hotspot != null \
				and footlights_hotspot != null \
				and opera_split_overlap <= 0.20
		elif room_id == "mermaid_pool":
			var pool_actual_items: Array[String] = []
			for pool_item_id: Variant in main.castle_room_item_sprites.keys():
				pool_actual_items.append(String(pool_item_id))
			pool_actual_items.sort()
			var pool_expected_items: Array[String] = [
				"buoy_bell",
				"dock_chest",
				"flower_float",
				"sailboat",
				"seahorse_fountain",
				"star_float",
				"waterfall",
				"waterwheel",
			]
			pool_interaction_set_ok = pool_actual_items == pool_expected_items
			var waterfall_record: Dictionary = \
				main.castle_room_item_sprites.get(
					"waterfall", {}) as Dictionary
			var waterfall_hotspot: Button = \
				waterfall_record.get("hotspot") as Button
			pool_waterfall_hotspot_ok = waterfall_hotspot != null \
				and waterfall_hotspot.size.x >= 170.0 \
				and waterfall_hotspot.size.y >= 210.0
			var flower_record: Dictionary = \
				main.castle_room_item_sprites.get("flower_float", {}) as Dictionary
			var star_record: Dictionary = \
				main.castle_room_item_sprites.get("star_float", {}) as Dictionary
			var flower_hotspot: Button = flower_record.get("hotspot") as Button
			var star_hotspot: Button = star_record.get("hotspot") as Button
			pool_split_overlap = _hotspot_overlap_fraction(
				flower_hotspot, star_hotspot)
			pool_split_hotspots_ok = flower_hotspot != null \
				and star_hotspot != null \
				and pool_split_overlap <= 0.20
		var counts: Dictionary = {}
		_audit_world_node(main.castle_room_world_root, counts)
		var visible_sprite_count := int(counts.get("visible_sprite3d", 0))
		max_visible_world_cards = maxi(
			max_visible_world_cards, visible_sprite_count)
		visible_card_peaks[room_id] = maxi(
			int(visible_card_peaks.get(room_id, 0)), visible_sprite_count)
		var hall_mode: bool = room_id == "main_hall"
		var expected_room_tiles: int = (
			12 if room_id == "kitchen" else 4)
		var expected_physical_items: int = int(
			EXPECTED_PHYSICAL_ITEM_COUNTS[room_id])
		var expected_room_items: int = expected_physical_items
		if hall_mode:
			expected_room_items += 3
		elif room_id == "playroom" and not rooms._playroom_rescue_done():
			expected_room_items += 3
		var visible_hall_tile_count := 0
		if hall_mode:
			for hall_tile: Sprite3D in main.castle_room_background_tiles:
				if hall_tile.visible:
					visible_hall_tile_count += 1
		var background_ready: bool = (
			main.castle_room_background_tiles.size() == HALL_TILE_COUNT
			and main.castle_room_background_tiles.all(
				func(tile: Sprite3D) -> bool:
					return tile.texture != null \
						and bool(tile.get_meta(
							"hall_horizontal_cull", false)))
			and visible_hall_tile_count > 0
			and visible_hall_tile_count <= 12
			and not main.castle_room_background.visible
		) if hall_mode else (
			not main.castle_room_background.visible
			and main.castle_room_background.texture != null
			and main.castle_room_detail_tiles.size() == expected_room_tiles
			and main.castle_room_detail_tiles.all(_room_detail_tile_ready)
			and main.castle_room_background_tiles.all(
				func(tile: Sprite3D) -> bool:
					return not tile.visible)
		)
		var room_ok: bool = main.castle_room_id == room_id \
			and main.castle_room_background is Sprite3D \
			and not main.castle_room_background.shaded \
			and main.castle_room_item_sprites.size() == expected_room_items \
			and main.castle_room_item_hotspot_layer.get_child_count() \
				== _expected_room_hotspot_count(room_id) \
			and background_ready \
			and int(counts.get("modeled", 0)) == 0 \
			and int(counts.get("canvas_world", 0)) == 0 \
			and int(counts.get("bad_alpha_depth", 0)) == 0 \
			and int(counts.get("portal_glow", 0)) == 0 \
			and int(counts.get("shaded", 0)) == 0 \
			and int(counts.get("missing_texture", 0)) == 0
		if not room_ok:
			room_structure_failures.append({
				"room": room_id,
				"active_room": main.castle_room_id,
				"background_sprite3d": main.castle_room_background is Sprite3D,
				"background_unshaded": main.castle_room_background != null \
					and not main.castle_room_background.shaded,
				"items": main.castle_room_item_sprites.size(),
				"expected_items": expected_room_items,
				"hotspots": main.castle_room_item_hotspot_layer.get_child_count(),
				"expected_hotspots": _expected_room_hotspot_count(room_id),
				"background_ready": background_ready,
				"modeled": int(counts.get("modeled", 0)),
				"canvas_world": int(counts.get("canvas_world", 0)),
				"bad_alpha_depth": int(counts.get("bad_alpha_depth", 0)),
				"portal_glow": int(counts.get("portal_glow", 0)),
				"shaded": int(counts.get("shaded", 0)),
				"missing_texture": int(counts.get("missing_texture", 0)),
			})
		var depths: Dictionary = {}
		if hall_mode:
			depths[snappedf(
				main.castle_room_background_tiles[0].position.z, 0.01)] = true
		else:
			depths[snappedf(
				main.castle_room_detail_tiles[0].position.z, 0.01)] = true
		var semantic_item_ids: Array[String] = []
		for item_id_value: Variant in main.castle_room_item_sprites:
			var record: Dictionary = main.castle_room_item_sprites[
				item_id_value] as Dictionary
			var sprite: Sprite3D = record.get("sprite") as Sprite3D
			if sprite != null:
				depths[snappedf(sprite.position.z, 0.01)] = true
				if String(sprite.get_meta("semantic_action", "")) != "":
					semantic_item_ids.append(String(item_id_value))
		interaction_manifest_ok = interaction_manifest_ok \
			and semantic_item_ids.size() == expected_physical_items
		for foreground: Node in main.castle_room_front_layer.get_children():
			var front_card := foreground as Sprite3D
			if front_card == null:
				continue
			depths[snappedf(front_card.position.z, 0.01)] = true
			if main.light_rig().emits_light(front_card):
				continue
			# multiply-only: a tint may darken a painting, never brighten it
			var front_tint: Color = front_card.modulate
			all_depth_tint_ok = all_depth_tint_ok \
				and front_tint.r <= 1.001 and front_tint.g <= 1.001 \
				and front_tint.b <= 1.001
			if front_tint.r < 0.999 or front_tint.g < 0.999 \
					or front_tint.b < 0.999:
				saw_tinted_foreground = true
		if not hall_mode and main.castle_room_background != null:
			var back_tint: Color = main.castle_room_background.modulate
			all_depth_tint_ok = all_depth_tint_ok \
				and is_equal_approx(back_tint.r, 1.0) \
				and is_equal_approx(back_tint.g, 1.0) \
				and is_equal_approx(back_tint.b, 1.0)
		all_rooms_ok = all_rooms_ok and room_ok
		all_depth_ok = all_depth_ok and depths.size() >= 3
		if not hall_mode:
			approved_composite_backdrops_ok = \
				approved_composite_backdrops_ok \
				and main.castle_room_background.texture.resource_path \
					.ends_with("_background.png")
			var logical_rects: Array[Rect2] = []
			var logical_area := 0.0
			for detail_tile: Sprite3D in main.castle_room_detail_tiles:
				var logical_rect: Rect2 = detail_tile.get_meta(
					"source_art_rect", Rect2()) as Rect2
				for prior_rect: Rect2 in logical_rects:
					all_detail_tile_grids_ok = all_detail_tile_grids_ok \
						and not logical_rect.intersects(prior_rect)
				logical_rects.append(logical_rect)
				logical_area += logical_rect.get_area()
			all_detail_tile_grids_ok = all_detail_tile_grids_ok \
				and logical_rects.size() == expected_room_tiles \
				and is_equal_approx(logical_area, 1024.0 * 576.0)
			var canvas_rect := Rect2(0.0, 0.0, 1024.0, 576.0)
			for item_id_value: Variant in main.castle_room_item_sprites:
				var item_record: Dictionary = main.castle_room_item_sprites[
					item_id_value] as Dictionary
				var art_rect: Rect2 = item_record.get(
					"render_art_rect",
					item_record.get("art_rect", Rect2())) as Rect2
				all_room_object_bounds_ok = all_room_object_bounds_ok \
					and canvas_rect.encloses(art_rect)
		if room_id == "playroom":
			var eagle_record: Dictionary = main.castle_room_item_sprites.get(
				"baby_eagle_rescue", {}) as Dictionary
			var left_record: Dictionary = main.castle_room_item_sprites.get(
				"eagle_pin_left", {}) as Dictionary
			var right_record: Dictionary = main.castle_room_item_sprites.get(
				"eagle_pin_right", {}) as Dictionary
			var eagle: Sprite3D = eagle_record.get("sprite") as Sprite3D
			var left_bunny: Sprite3D = left_record.get("sprite") as Sprite3D
			var right_bunny: Sprite3D = right_record.get("sprite") as Sprite3D
			var rescue_pointer: Sprite3D = \
				main.castle_room_item_effect_layer.get_node_or_null(
					"BabyEagleRescuePointer") as Sprite3D
			playroom_rescue_cards_ok = (
				eagle != null
				and left_bunny != null
				and right_bunny != null
				and rescue_pointer != null
				and not eagle.shaded
				and not left_bunny.shaded
				and not right_bunny.shaded
				and not eagle.no_depth_test
				and not left_bunny.no_depth_test
				and not right_bunny.no_depth_test
				and eagle.position.z < left_bunny.position.z
				and eagle.position.z < right_bunny.position.z
				and left_record.get("hotspot") == null
				and right_record.get("hotspot") == null
				and String(left_bunny.get_meta(
					"dust_bunny_role", "")) == "playroom_pin_left"
				and String(right_bunny.get_meta(
					"dust_bunny_role", "")) == "playroom_pin_right"
				and String(eagle.texture.resource_path).ends_with(
					"assets/book/baby_eagle.png")
				and String(left_bunny.texture.resource_path).ends_with(
					"dust_bunnies/dust_bunny_hop.png")
				and String(right_bunny.texture.resource_path).ends_with(
					"dust_bunnies/dust_bunny_hop.png")
				and String(rescue_pointer.get_meta(
					"source_asset_role", "")) == "tutorial_pointer"
				and not main.castle_room_action_button.visible
			)
			playroom_rescue_ray_ok = true
			var playroom_walk: Rect2 = (
				CastleRooms25D.ROOM_LAYOUTS["playroom"] as Dictionary).get(
					"walk", Rect2()) as Rect2
			playroom_rescue_route_ok = true
			for bunny_record: Dictionary in [left_record, right_record]:
				var bunny: Sprite3D = bunny_record.get("sprite") as Sprite3D
				if bunny == null:
					playroom_rescue_ray_ok = false
					playroom_rescue_route_ok = false
					continue
				var screen_center: Vector2 = \
					main.castle_room_camera.unproject_position(
						bunny.global_position)
				var mapped_foot: Vector2 = \
					rooms._dust_bunny_foot_from_camera_ray(screen_center)
				var contact_foot: Vector2 = bunny_record.get(
					"contact_foot", Vector2.INF) as Vector2
				playroom_rescue_ray_ok = playroom_rescue_ray_ok \
					and mapped_foot != Vector2.INF \
					and mapped_foot.distance_to(contact_foot) <= 0.01
				playroom_rescue_route_ok = playroom_rescue_route_ok \
					and playroom_walk.has_point(contact_foot)
		await _capture(room_id)
		for semantic_item_id: String in semantic_item_ids:
			var manifest_key := room_id + ":" + semantic_item_id
			var manifest_asset: Dictionary = manifest_assets.get(
				manifest_key, {}) as Dictionary
			var audit: Dictionary = await _run_semantic_animation(
				rooms, room_id, semantic_item_id, manifest_asset)
			all_interaction_contracts_ok = all_interaction_contracts_ok \
				and bool(audit.get("contract_ok", false))
			all_semantic_sequences_ok = all_semantic_sequences_ok \
				and bool(audit.get("sequence_ok", false))
			all_fixed_pivot_sequences_ok = all_fixed_pivot_sequences_ok \
				and bool(audit.get("transform_ok", false))
			all_item_audio_ok = all_item_audio_ok \
				and bool(audit.get("sound_ok", false))
			all_busy_guards_ok = all_busy_guards_ok \
				and bool(audit.get("busy_guard_ok", false))
			all_fixture_uv_resets_ok = all_fixture_uv_resets_ok \
				and bool(audit.get("fixture_uv_ok", false))
			all_water_profiles_ok = all_water_profiles_ok \
				and bool(audit.get("water_profile_ok", false))
			all_jolt_motion_ok = all_jolt_motion_ok \
				and bool(audit.get("physics_motion_ok", false))
			all_jolt_settles_ok = all_jolt_settles_ok \
				and bool(audit.get("settled_ok", false))
			var animation_peak: int = int(audit.get(
				"peak_visible_cards", 0))
			max_visible_world_cards = maxi(
				max_visible_world_cards, animation_peak)
			visible_card_peaks[room_id] = maxi(
				int(visible_card_peaks.get(room_id, 0)), animation_peak)
			if room_id == "kitchen" and semantic_item_id == "fridge":
				fridge_door_then_menu_ok = bool(audit.get(
					"menu_order_ok", false))
			if not bool(audit.get("contract_ok", false)) \
					or not bool(audit.get("sequence_ok", false)) \
					or not bool(audit.get("transform_ok", false)) \
					or not bool(audit.get("sound_ok", false)) \
					or not bool(audit.get("busy_guard_ok", false)) \
					or not bool(audit.get("fixture_uv_ok", false)) \
					or not bool(audit.get("water_profile_ok", false)) \
					or not bool(audit.get("physics_motion_ok", false)) \
					or not bool(audit.get("settled_ok", false)):
				interaction_failures.append(String(audit.get("detail", "")))
		if hall_mode:
			for semantic_item_id: String in semantic_item_ids:
				var hall_record: Dictionary = main.castle_room_item_sprites.get(
					semantic_item_id, {}) as Dictionary
				var hall_data: Dictionary = hall_record.get("data", {}) as Dictionary
				if not hall_data.has("light_cluster"):
					continue
				var hall_sprite: Sprite3D = hall_record.get("sprite") as Sprite3D
				main.castle_room_light_states[semantic_item_id] = true
				rooms._apply_sconce_visual(hall_sprite, true)
			rooms._sync_hall_lighting()
		if room_id == "kitchen":
			var kitchen_ids: Array[String] = [
				"sink", "pan_1", "pan_2", "pan_3", "pan_4", "oven",
				"fridge", "seafoam_kettle", "soup_pot", "cookie_jar",
				"cutlery_drawer", "ladle_rack", "serving_tureen",
				"shell_cupboard",
			]
			kitchen_prop_set_ok = kitchen_ids.all(
				func(kitchen_id: String) -> bool:
					return main.castle_room_item_sprites.has(kitchen_id))
			var pan_ids: Array[String] = ["pan_1", "pan_2", "pan_3", "pan_4"]
			var pan_hotspot: Button = \
				main.castle_room_item_hotspot_layer.get_node_or_null(
					"Touch_pan_rack") as Button
			kitchen_pan_rack_group_ok = pan_hotspot != null
			for pan_id: String in pan_ids:
				var reset_record: Dictionary = main.castle_room_item_sprites.get(
					pan_id, {}) as Dictionary
				var reset_sprite: Sprite3D = reset_record.get("sprite") as Sprite3D
				if reset_sprite != null:
					reset_sprite.set_meta("animation_frames_visited", [])
					reset_sprite.set_meta(
						"animation_timeline_steps_visited", [])
			if pan_hotspot != null:
				pan_hotspot.pressed.emit()
			var pan_group_deadline: int = Time.get_ticks_msec() + 3000
			var pan_group_busy := true
			while pan_group_busy \
					and Time.get_ticks_msec() < pan_group_deadline:
				pan_group_busy = false
				for pan_id: String in pan_ids:
					var busy_record: Dictionary = \
						main.castle_room_item_sprites.get(
							pan_id, {}) as Dictionary
					var busy_sprite: Sprite3D = \
						busy_record.get("sprite") as Sprite3D
					pan_group_busy = pan_group_busy or (
						busy_sprite != null
						and bool(busy_sprite.get_meta("busy", false)))
				if pan_group_busy:
					await process_frame
			kitchen_pan_rack_group_ok = kitchen_pan_rack_group_ok \
				and not pan_group_busy \
				and Time.get_ticks_msec() < pan_group_deadline
			for pan_id: String in pan_ids:
				var pan_record: Dictionary = main.castle_room_item_sprites.get(
					pan_id, {}) as Dictionary
				var pan_sprite: Sprite3D = pan_record.get("sprite") as Sprite3D
				var pan_data: Dictionary = pan_record.get("data", {}) as Dictionary
				var pan_manifest: Dictionary = manifest_assets.get(
					"kitchen:" + pan_id, {}) as Dictionary
				var expected_pan_frames: Array[int] = []
				for frame_value: Variant in pan_manifest.get(
						"timeline_sequence", []) as Array:
					expected_pan_frames.append(int(frame_value))
				var actual_pan_frames: Array = pan_sprite.get_meta(
					"animation_frames_visited", []) as Array \
					if pan_sprite != null else []
				var pan_sequence_ok: bool = \
					actual_pan_frames.size() == expected_pan_frames.size()
				if pan_sequence_ok:
					for frame_index: int in range(expected_pan_frames.size()):
						pan_sequence_ok = pan_sequence_ok \
							and int(actual_pan_frames[frame_index]) \
								== expected_pan_frames[frame_index]
				kitchen_pan_rack_group_ok = kitchen_pan_rack_group_ok \
					and pan_sprite != null \
					and String(pan_data.get("hotspot_group", "")) \
						== "pan_rack" \
					and (pan_record.get("hotspot") != null) == (pan_id == "pan_1") \
					and pan_sequence_ok
			var kitchen_sink: Sprite3D = (
				main.castle_room_item_sprites["sink"] as Dictionary
			).get("sprite") as Sprite3D
			var kitchen_oven: Sprite3D = (
				main.castle_room_item_sprites["oven"] as Dictionary
			).get("sprite") as Sprite3D
			var kitchen_fridge: Sprite3D = (
				main.castle_room_item_sprites["fridge"] as Dictionary
			).get("sprite") as Sprite3D
			kitchen_normalized_use_examples_ok = kitchen_sink != null \
				and kitchen_oven != null and kitchen_fridge != null \
				and String(kitchen_sink.get_meta("semantic_action", "")) \
					== "turn_faucet_and_run_water" \
				and String(kitchen_oven.get_meta("semantic_action", "")) \
					== "open_oven_door_and_warm_fire" \
				and String(kitchen_fridge.get_meta("semantic_action", "")) \
					== "unlatch_and_open_fridge_door"
			main.opera_pantry.erase("carrots")
			main.opera_pantry["sugar"] = 2
			rooms._open_kitchen_menu()
			await _frames(1)
			var empty_pantry_label: Label = \
				rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenPantryInventory") as Label \
				if rooms.kitchen_menu_stage != null else null
			var empty_pantry_counts: Dictionary = empty_pantry_label.get_meta(
				"food_counts", {}) as Dictionary \
				if empty_pantry_label != null else {}
			kitchen_menu_empty_filter_ok = (
				rooms.kitchen_menu_layer != null
				and rooms.kitchen_menu_stage != null
				and rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenRecipe_pearl_cake") != null
				and rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenRecipe_carrot_cake") == null
				and int(empty_pantry_counts.get("carrots", 0)) == 0
				and int(empty_pantry_counts.get("sugar", 0)) == 2
			)
			rooms._close_kitchen_menu()
			await _frames(1)
			main.opera_pantry["carrots"] = 1
			rooms._open_kitchen_menu()
			await _frames(1)
			var pantry_label: Label = \
				rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenPantryInventory") as Label \
				if rooms.kitchen_menu_stage != null else null
			var pantry_counts: Dictionary = pantry_label.get_meta(
				"food_counts", {}) as Dictionary \
				if pantry_label != null else {}
			kitchen_menu_inventory_ok = (
				rooms.kitchen_menu_layer != null
				and rooms.kitchen_menu_stage != null
				and rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenRecipe_pearl_cake") != null
				and rooms.kitchen_menu_stage.get_node_or_null(
					"KitchenRecipe_carrot_cake") != null
				and int(pantry_counts.get("carrots", 0)) == 1
				and int(pantry_counts.get("sugar", 0)) == 2
			)
			rooms._launch_kitchen_recipe("carrot_cake")
			await _frames(2)
			var kitchen_act: OperaAct = rooms.kitchen_act
			kitchen_cooking_portal_ok = (
				main.game == "kitchen_cooking"
				and kitchen_act != null
				and kitchen_act.kind == "order"
				and String(kitchen_act.config.get("uses", "")) == "carrots"
				and kitchen_act.stage_phase == "puzzle"
			)
			if kitchen_act != null:
				kitchen_act.cancel()
			await _frames(3)
			kitchen_cooking_portal_ok = kitchen_cooking_portal_ok \
				and rooms.kitchen_act == null \
				and main.game == "level2" \
				and main.castle_room_id == "kitchen" \
				and main.castle_room_layer.visible
	_ck("all_eight_rooms_sprite3d_only", all_rooms_ok,
		"failures=%s" % [room_structure_failures])
	_ck("all_rooms_use_multiple_real_depths", all_depth_ok)
	_ck("depth_planes_are_tonally_separated",
		all_depth_tint_ok and saw_tinted_foreground,
		"multiply_only=%s saw_tinted_foreground=%s" % [
			all_depth_tint_ok, saw_tinted_foreground])
	_ck("approved_room_composites_preserved", approved_composite_backdrops_ok)
	_ck("all_destination_rooms_use_2k_exact_tile_grids",
		all_detail_tile_grids_ok)
	_ck("all_destination_room_objects_within_authored_canvas",
		all_room_object_bounds_ok)
	_ck("opera_star_and_footlights_hotspots_are_distinct",
		opera_split_hotspots_ok,
		"overlap=%.3f of smaller hotspot" % opera_split_overlap)
	_ck("pool_flower_and_star_hotspots_are_distinct",
		pool_split_hotspots_ok,
		"overlap=%.3f of smaller hotspot" % pool_split_overlap)
	_ck("pool_uses_coherent_interaction_set",
		pool_interaction_set_ok,
		"expected waterfall, flower float, star float, and seahorse fountain")
	_ck("pool_waterfall_hotspot_covers_full_fixture",
		pool_waterfall_hotspot_ok)
	_ck("v3_plus_room_derived_pool_match_70_assets_75_runtime_items",
		interaction_manifest_ok,
		"active=%d overall=%d average=%.2f" % [
			active_manifest_assets.size(), manifest_assets.size(),
			delivered_average])
	_ck("all_room_interaction_sheets_fit_24_mib_decoded_rgba",
		decoded_texture_budget_ok,
		str(decoded_texture_bytes_by_room))
	_ck("all_38_v3_sheets_have_clean_unique_fixed_anchor_states",
		_v3_addition_visual_contract(manifest_unique_assets))
	_ck("kettle_and_shower_water_tracks_authored_atlas_frame_four",
		_dynamic_water_hold_contract(active_manifest_assets))
	_ck("all_interactions_use_4_to_12_frame_semantic_atlases",
		all_interaction_contracts_ok, ";".join(interaction_failures))
	_ck("all_interactions_follow_audited_4_to_12_step_timelines",
		all_semantic_sequences_ok, ";".join(interaction_failures))
	_ck("all_item_specific_sequences_keep_fixed_root_transform",
		all_fixed_pivot_sequences_ok, ";".join(interaction_failures))
	_ck("all_interactions_play_manifest_castle_audio",
		all_item_audio_ok, ";".join(interaction_failures))
	_ck("all_interactions_reject_reentry_while_busy",
		all_busy_guards_ok, ";".join(interaction_failures))
	_ck("all_runtime_water_layers_activate_and_return_to_rest",
		all_water_profiles_ok, ";".join(interaction_failures))
	_ck("all_jolt_garnish_has_nonzero_bounded_motion",
		all_jolt_motion_ok, ";".join(interaction_failures))
	_ck("all_jolt_garnish_eventually_settles",
		all_jolt_settles_ok, ";".join(interaction_failures))
	_ck("kitchen_fourteen_independent_props", kitchen_prop_set_ok)
	_ck("kitchen_pan_rack_one_hotspot_animates_all_four_pans",
		kitchen_pan_rack_group_ok)
	_ck("kitchen_sink_oven_and_fridge_use_normalized_actions",
		kitchen_normalized_use_examples_ok)
	_ck("kitchen_fridge_opens_menu_after_door_sequence",
		fridge_door_then_menu_ok)
	_ck("kitchen_fridge_filters_missing_food",
		kitchen_menu_empty_filter_ok)
	_ck("kitchen_fridge_inventory_menu", kitchen_menu_inventory_ok)
	_ck("kitchen_fridge_launches_cooking_portal",
		kitchen_cooking_portal_ok)
	_ck("playroom_baby_eagle_rescue_depth_cards",
		playroom_rescue_cards_ok)
	_ck("playroom_bunny_camera_ray_touch_mapping",
		playroom_rescue_ray_ok)
	_ck("playroom_bunny_contacts_inside_navigation",
		playroom_rescue_route_ok)
	_ck("speedy_visible_card_budget", max_visible_world_cards <= 33,
		"maximum visible cards=%d rooms=%s" % [
			max_visible_world_cards, visible_card_peaks])
	await _frames(60)
	var repeated_rebuilds_clean := true
	for room_id: String in ROOM_IDS:
		rooms.show_room(room_id, false)
		await _frames(2)
		var expected_physical_items: int = int(
			EXPECTED_PHYSICAL_ITEM_COUNTS[room_id])
		var expected_runtime_items: int = expected_physical_items
		if room_id == "main_hall":
			expected_runtime_items += 3
		elif room_id == "playroom" and not rooms._playroom_rescue_done():
			expected_runtime_items += 3
		var expected_hotspots: int = _expected_room_hotspot_count(room_id)
		var expected_fixture_inventory: Dictionary = \
			_expected_room_fixture_inventory(manifest_assets, room_id)
		var first_visual_inventory: Dictionary = _direct_visual_inventory()
		var first_hotspot_count: int = \
			main.castle_room_item_hotspot_layer.get_child_count()
		var first_effect_count: int = \
			main.castle_room_item_effect_layer.get_child_count()
		var expected_persistent_effects: int = 1 \
			if room_id == "playroom" and not rooms._playroom_rescue_done() \
			else 0
		rooms.show_room(room_id, false)
		await _frames(2)
		var second_visual_inventory: Dictionary = _direct_visual_inventory()
		repeated_rebuilds_clean = repeated_rebuilds_clean \
			and main.castle_room_item_sprites.size() == expected_runtime_items \
			and second_visual_inventory == first_visual_inventory \
			and int(first_visual_inventory.get("art", -1)) \
				== expected_runtime_items \
			and int(first_visual_inventory.get("water", -1)) \
				== int(expected_fixture_inventory.get("water", -2)) \
			and int(first_visual_inventory.get("jolt", -1)) \
				== int(expected_fixture_inventory.get("jolt", -2)) \
			and int(first_visual_inventory.get("total", -1)) \
				== main.castle_room_item_visual_layer.get_child_count() \
			and main.castle_room_item_hotspot_layer.get_child_count() \
				== first_hotspot_count \
			and first_hotspot_count == expected_hotspots \
			and main.castle_room_item_effect_layer.get_child_count() \
				== first_effect_count \
			and first_effect_count == expected_persistent_effects
	_ck("repeated_room_rebuilds_do_not_leak_cards_or_hotspots",
		repeated_rebuilds_clean)

	rooms.show_room("main_hall", false)
	var castle_environment: Environment = main.castle_room_environment
	var expected_glow: float = 0.78 if main.quality == "speedy" else 1.00
	var expected_bloom: float = 0.10 if main.quality == "speedy" else 0.16
	var glow_on: float = castle_environment.glow_intensity \
		if castle_environment != null else 0.0
	var bloom_on: float = castle_environment.glow_bloom \
		if castle_environment != null else 0.0
	_ck("main_hall_dramatic_glow_environment",
		castle_environment != null
		and main.we_node != null
		and main.we_node.environment == castle_environment
		and castle_environment.glow_enabled
		and castle_environment.glow_blend_mode
			== Environment.GLOW_BLEND_MODE_SCREEN
		and is_equal_approx(glow_on, expected_glow)
		and is_equal_approx(bloom_on, expected_bloom)
		and castle_environment.glow_hdr_threshold >= 1.79
		and castle_environment.glow_hdr_threshold <= 1.81
		and castle_environment.glow_hdr_scale >= 1.99
		and castle_environment.glow_hdr_scale <= 2.01
		and castle_environment.tonemap_white >= 1.55
		and castle_environment.adjustment_saturation >= 1.0
		and castle_environment.adjustment_contrast <= 1.05
		and castle_environment.adjustment_brightness <= 1.0
		and castle_environment.ambient_light_energy <= 0.33,
		"quality=%s glow=%.3f bloom=%.3f threshold=%.3f scale=%.3f" % [
			main.quality, glow_on, bloom_on,
			castle_environment.glow_hdr_threshold
				if castle_environment != null else 0.0,
			castle_environment.glow_hdr_scale
				if castle_environment != null else 0.0])
	var original_quality: String = main.quality
	main.quality = "speedy"
	rooms._sync_hall_lighting()
	var speedy_shadow_count := 0
	for speedy_light: Light3D in main.castle_room_light_nodes:
		if speedy_light.visible and speedy_light.shadow_enabled:
			speedy_shadow_count += 1
	_ck("main_hall_speedy_glow_budget",
		castle_environment.glow_intensity <= 0.781
		and castle_environment.glow_bloom <= 0.101
		and speedy_shadow_count <= 1,
		"glow=%.3f bloom=%.3f shadows=%d" % [
			castle_environment.glow_intensity,
			castle_environment.glow_bloom, speedy_shadow_count])
	main.quality = original_quality
	rooms._sync_hall_lighting()
	var tile_paths_ok := true
	var tile_registration_ok := true
	var tile_index := 0
	for tile: Sprite3D in main.castle_room_background_tiles:
		var tile_row: int = tile_index / HALL_TILE_COLUMNS
		var tile_column: int = tile_index % HALL_TILE_COLUMNS
		var source_rect: Rect2 = tile.get_meta(
			"source_art_rect", Rect2()) as Rect2
		var master_rect: Rect2 = tile.get_meta(
			"source_master_rect", Rect2()) as Rect2
		var render_rect: Rect2 = tile.get_meta(
			"render_art_rect", Rect2()) as Rect2
		var screen_rect: Rect2 = tile.get_meta(
			"source_screen_rect", Rect2()) as Rect2
		var native_size: Vector2 = tile.get_meta(
			"native_texture_size", Vector2.ZERO) as Vector2
		var native_scale: Vector2 = tile.get_meta(
			"native_to_logical_scale", Vector2.ZERO) as Vector2
		var bleed_pixels: Vector2i = tile.get_meta(
			"runtime_seam_bleed_pixels", Vector2i(-1, -1)) as Vector2i
		var expected_source_rect: Rect2 = _hall_expected_logical_rect(
			tile_row, tile_column)
		var expected_native_size: Vector2 = _hall_expected_native_size(
			tile_column)
		var expected_native_scale: Vector2 = HALL_NATIVE_TO_LOGICAL
		var source_path: String = tile.texture.resource_path
		tile_paths_ok = tile_paths_ok \
			and tile.texture != null \
			and source_path.contains(
				"main_hall_redraw_2026-08-03/tiles/") \
			and not source_path.contains("/runtime_bleed/") \
			and source_path.ends_with(
				"_r%d_c%d.png" % [tile_row, tile_column]) \
			and tile.texture.get_size() == expected_native_size \
			and maxf(tile.texture.get_width(), tile.texture.get_height()) <= 1024.0 \
			and source_rect.is_equal_approx(expected_source_rect) \
			and render_rect == source_rect \
			and native_size == expected_native_size \
			and native_scale.is_equal_approx(expected_native_scale) \
			and is_equal_approx(tile.scale.x, expected_native_scale.x) \
			and is_equal_approx(tile.scale.y, expected_native_scale.y) \
			and bleed_pixels == Vector2i.ZERO \
			and String(tile.get_meta("source_asset_role", "")) \
				== "clean_background_tile" \
			and String(tile.get_meta("source_master_grid", "")) \
				== "2x8_7280x2048" \
			and not tile.shaded and not tile.transparent \
			and tile.alpha_cut == SpriteBase3D.ALPHA_CUT_DISABLED \
			and tile.texture_filter == BaseMaterial3D.TEXTURE_FILTER_LINEAR
		var expected_master_position := Vector2(
			_hall_native_column_x(tile_column),
			float(tile_row) * HALL_TILE_NATIVE_HEIGHT)
		var screen_index: int = tile_column / 4
		var expected_screen_position := Vector2(
			expected_master_position.x
				- float(screen_index) * HALL_SCREEN_NATIVE_WIDTH,
			expected_master_position.y)
		tile_registration_ok = tile_registration_ok \
			and master_rect == Rect2(
				expected_master_position, expected_native_size) \
			and screen_rect == Rect2(
				expected_screen_position, expected_native_size) \
			and String(tile.get_meta("source_screen_id", "")) \
				== ("a" if screen_index == 0 else "b")
		tile_index += 1
	_ck("main_hall_native_2x8_sprite3d_grid",
		main.castle_room_background_tiles.size() == HALL_TILE_COUNT \
		and tile_paths_ok)
	var per_screen_native_width := 0
	for local_column: int in range(HALL_TILE_COLUMNS / 2):
		per_screen_native_width += HALL_TILE_NATIVE_WIDTHS[local_column]
	_ck("main_hall_each_screen_has_eight_native_2k_tiles",
		HALL_TILE_COLUMNS == 8 and HALL_TILE_ROWS == 2 \
		and HALL_TILE_COUNT == 16 \
		and per_screen_native_width == int(HALL_SCREEN_NATIVE_WIDTH) \
		and per_screen_native_width >= 2048 \
		and int(HALL_TILE_NATIVE_HEIGHT) * HALL_TILE_ROWS >= 2048,
		"screen=%dx%d tiles_per_screen=%d total=%d" % [
			per_screen_native_width,
			int(HALL_TILE_NATIVE_HEIGHT) * HALL_TILE_ROWS,
			HALL_TILE_COUNT / 2, HALL_TILE_COUNT])
	_ck("main_hall_lossless_screen_registration",
		tile_registration_ok,
		"7280x2048 master -> sixteen exact 910x1024 cards")
	var runtime_seam_stress: Dictionary = _hall_runtime_tile_seams_match(
		main.castle_room_background_tiles)
	_ck("main_hall_runtime_tiles_reconstruct_without_gaps",
		bool(runtime_seam_stress.get("ok", false)),
		"%s worst_mean=%.4f" % [
			String(runtime_seam_stress.get("mismatch", "")),
			float(runtime_seam_stress.get("worst_mean_rgb_delta", -1.0))])
	var light_inventory_ok: bool = main.castle_room_light_nodes.size() == 5
	var visible_lights := 0
	var visible_shadow_lights := 0
	var touch_light_energy_ok := true
	var fill_on_energy := 0.0
	for light: Light3D in main.castle_room_light_nodes:
		light_inventory_ok = light_inventory_ok \
			and light != null and is_instance_valid(light)
		var light_role: String = String(light.get_meta(
			"castle_light_role", ""))
		if light_role == "ambient_fill":
			fill_on_energy = light.light_energy
		elif light_role == "touch_cluster":
			touch_light_energy_ok = touch_light_energy_ok \
				and is_equal_approx(float(
					light.get_meta("max_energy", 0.0)), 4.6)
		if light.visible:
			visible_lights += 1
			if light.shadow_enabled:
				visible_shadow_lights += 1
	_ck("main_hall_mobile_light_pool",
		light_inventory_ok and visible_lights <= 3
		and visible_shadow_lights >= 1 and visible_shadow_lights <= 2,
		"visible=%d shadowed=%d" % [visible_lights, visible_shadow_lights])
	_ck("main_hall_equal_cluster_energy",
		touch_light_energy_ok and is_equal_approx(fill_on_energy, 0.78),
		"fill=%.3f" % fill_on_energy)
	var sconce_manifest: Dictionary = manifest_assets.get(
		"main_hall:sconce_a0", {}) as Dictionary
	var banner_manifest: Dictionary = manifest_assets.get(
		"main_hall:banner_left", {}) as Dictionary
	var expected_fixture_asset_path: String = "res://" + String(
		sconce_manifest.get("sheet", ""))
	var expected_banner_asset_path: String = "res://" + String(
		banner_manifest.get("sheet", ""))
	var fixture_asset_path := ""
	var fixture_continuity_ok: bool = \
		expected_fixture_asset_path != "res://" \
		and expected_banner_asset_path != "res://"
	var fixture_y: float = -1.0
	var fixture_height_ok := true
	var fixture_bloom_emitters_ok := true
	var fixture_single_card_ok := true
	var fixture_uv_state_ok := true
	for fixture_id: String in [
			"sconce_a0", "sconce_a1", "sconce_a2",
			"sconce_b0", "sconce_b1", "sconce_b2"]:
		var fixture_record: Dictionary = main.castle_room_item_sprites.get(
			fixture_id, {})
		var fixture: Sprite3D = fixture_record.get("sprite") as Sprite3D
		if fixture == null or fixture.texture == null:
			fixture_continuity_ok = false
			fixture_bloom_emitters_ok = false
			fixture_single_card_ok = false
			fixture_uv_state_ok = false
			continue
		var fixture_material: ShaderMaterial = \
			fixture.material_override as ShaderMaterial
		var emission_energy: float = float(
			fixture_material.get_shader_parameter("emission_energy")) \
			if fixture_material != null else 0.0
		fixture_bloom_emitters_ok = fixture_bloom_emitters_ok \
			and bool(fixture.get_meta("castle_bloom_emitter", false)) \
			and emission_energy >= 3.8 \
			and is_equal_approx(float(fixture.get_meta(
				"castle_emission_energy", 0.0)), emission_energy) \
			and fixture_material != null \
			and fixture_material.shader != null \
			and fixture_material.shader.resource_path.ends_with(
				"castle_fixture_bloom.gdshader")
		fixture_single_card_ok = fixture_single_card_ok \
			and fixture.get_child_count() == 0 \
			and fixture.modulate == Color.WHITE \
			and not fixture.shaded \
			and fixture.cast_shadow \
				== GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		var expected_fixture_frame: int = 7 \
			if bool(main.castle_room_light_states.get(fixture_id, true)) \
			else 0
		fixture_uv_state_ok = fixture_uv_state_ok \
			and fixture.frame == expected_fixture_frame \
			and _fixture_uv_matches_frame(fixture, expected_fixture_frame)
		var path: String = fixture.texture.resource_path
		if fixture_asset_path == "":
			fixture_asset_path = path
			fixture_continuity_ok = fixture_continuity_ok \
				and path == expected_fixture_asset_path
		else:
			fixture_continuity_ok = fixture_continuity_ok \
				and path == fixture_asset_path
		var fixture_record_data: Dictionary = fixture_record.get("data", {})
		var fixture_position: Vector2 = fixture_record_data.get(
			"pos", Vector2.ZERO)
		if fixture_y < 0.0:
			fixture_y = fixture_position.y
		else:
			fixture_height_ok = fixture_height_ok \
				and is_equal_approx(fixture_position.y, fixture_y)
	var banner_record: Dictionary = main.castle_room_item_sprites.get(
		"banner_left", {}) as Dictionary
	var banner_sprite: Sprite3D = banner_record.get("sprite") as Sprite3D
	var coherent_banner_family: bool = banner_sprite != null \
		and banner_sprite.texture != null \
		and banner_sprite.texture.resource_path == expected_banner_asset_path \
		and not main.castle_room_item_sprites.has("tapestry_right")
	_ck("main_hall_fixture_family_continuity", fixture_continuity_ok)
	_ck("main_hall_uses_one_coherent_banner_family", coherent_banner_family)
	_ck("main_hall_fixture_height_alignment",
		fixture_height_ok and is_equal_approx(fixture_y, 215.0),
		"shared_y=%.1f" % fixture_y)
	_ck("main_hall_fixture_hdr_bloom_emitters",
		fixture_bloom_emitters_ok)
	_ck("main_hall_fixture_single_sprite3d_cards",
		fixture_single_card_ok)
	_ck("main_hall_fixture_atlas_uv_clamps_and_resets",
		fixture_uv_state_ok and all_fixture_uv_resets_ok)
	var hall_door_clearance_ok := true
	var hall_door_conflicts: Array[String] = []
	for item_id_value: Variant in main.castle_room_item_sprites:
		var item_record: Dictionary = main.castle_room_item_sprites[
			item_id_value] as Dictionary
		var item_rect: Rect2 = item_record.get("art_rect", Rect2())
		for portal_index: int in main.castle_room_door_hotspots.size():
			var portal_record: Dictionary = main.castle_room_door_hotspots[
				portal_index]
			var portal_data: Dictionary = portal_record.get("data", {})
			var portal_rect: Rect2 = portal_data.get("rect", Rect2())
			var approach_rect := Rect2(
				portal_rect.position.x,
				maxf(315.0, portal_rect.position.y),
				portal_rect.size.x,
				720.0 - maxf(315.0, portal_rect.position.y))
			if item_rect.intersects(approach_rect):
				hall_door_clearance_ok = false
				hall_door_conflicts.append(
					"%s:%s:portal_%d" % [
						String(item_id_value), item_rect, portal_index])
	_ck("main_hall_objects_clear_all_door_approaches",
		hall_door_clearance_ok, ",".join(hall_door_conflicts))
	var expected_hall_positions := {
		"shell_clock": Vector2(1260.0, 360.0),
		"visitor_bell": Vector2(1410.0, 375.0),
		"left_pearl_vitrine": Vector2(790.0, 480.0),
		"right_pearl_vitrine": Vector2(2785.0, 480.0),
		"banner_left": Vector2(1810.0, 360.0),
		"fern_planter": Vector2(1750.0, 790.0),
		"chest_bench": Vector2(1930.0, 845.0),
	}
	var hall_addition_positions_ok := true
	for expected_item_id: String in expected_hall_positions:
		var expected_record: Dictionary = main.castle_room_item_sprites.get(
			expected_item_id, {}) as Dictionary
		var expected_data: Dictionary = expected_record.get("data", {}) as Dictionary
		hall_addition_positions_ok = hall_addition_positions_ok \
			and (expected_data.get("pos", Vector2.INF) as Vector2).is_equal_approx(
				expected_hall_positions[expected_item_id] as Vector2)
	_ck("main_hall_additions_use_audited_placement_map",
		hall_addition_positions_ok)
	var sconce_a2_data: Dictionary = (main.castle_room_item_sprites.get(
		"sconce_a2", {}) as Dictionary).get("data", {}) as Dictionary
	var shell_bunny_data: Dictionary = (main.castle_room_item_sprites.get(
		"shell_bunny", {}) as Dictionary).get("data", {}) as Dictionary
	_ck("main_hall_hud_clear_runtime_placements",
		(sconce_a2_data.get("pos", Vector2.INF) as Vector2).is_equal_approx(
			Vector2(1390.0, 215.0))
		and (shell_bunny_data.get(
			"pos", Vector2.INF) as Vector2).is_equal_approx(
				Vector2(1250.0, 830.0)))
	var fern_sprite: Sprite3D = (main.castle_room_item_sprites.get(
		"fern_planter", {}) as Dictionary).get("sprite") as Sprite3D
	var chest_sprite: Sprite3D = (main.castle_room_item_sprites.get(
		"chest_bench", {}) as Dictionary).get("sprite") as Sprite3D
	rooms._position_player_at_foot(Vector2(1600.0, 680.0), false)
	var player_behind_floor_props: bool = fern_sprite != null \
		and chest_sprite != null \
		and main.castle_room_player_sprite.position.z < fern_sprite.position.z \
		and main.castle_room_player_sprite.position.z < chest_sprite.position.z
	rooms._position_player_at_foot(Vector2(1600.0, 900.0), false)
	var player_in_front_of_floor_props: bool = fern_sprite != null \
		and chest_sprite != null \
		and main.castle_room_player_sprite.position.z > fern_sprite.position.z \
		and main.castle_room_player_sprite.position.z > chest_sprite.position.z
	_ck("main_hall_floor_props_participate_in_depth_occlusion",
		player_behind_floor_props and player_in_front_of_floor_props
		and is_equal_approx(fern_sprite.position.z, 2.83)
		and is_equal_approx(chest_sprite.position.z, 2.88))
	rooms._position_player_at_foot(Vector2(1672.0, 835.0), false)
	await _frames(2)
	rooms.tick(1.0)
	var seam_a_lights := 0
	var seam_b_lights := 0
	for seam_light: Light3D in main.castle_room_light_nodes:
		if not seam_light.visible \
				or String(seam_light.get_meta(
					"castle_light_role", "")) != "touch_cluster":
			continue
		if String(seam_light.get_meta("hall_half", "")) == "a":
			seam_a_lights += 1
		elif String(seam_light.get_meta("hall_half", "")) == "b":
			seam_b_lights += 1
	_ck("main_hall_seam_uses_cross_screen_lights",
		seam_a_lights == 1 and seam_b_lights == 1,
		"A=%d B=%d" % [seam_a_lights, seam_b_lights])
	await _capture("main_hall_seam_bridge")
	rooms._position_player_at_foot(Vector2(380.0, 835.0), false)
	await _frames(2)
	rooms.tick(1.0)
	var sconce_record: Dictionary = main.castle_room_item_sprites.get(
		"sconce_a0", {})
	var sconce: Sprite3D = sconce_record.get("sprite") as Sprite3D
	var sconce_started_on: bool = sconce != null \
		and bool(sconce.get_meta("castle_light_on", false))
	rooms._activate_room_item("sconce_a0")
	await _frames(3)
	var sconce_toggled_off: bool = sconce != null \
		and not bool(sconce.get_meta("castle_light_on", true)) \
		and not bool(main.castle_room_light_states.get("sconce_a0", true))
	_ck("main_hall_touch_lighting_engine",
		sconce_started_on and sconce_toggled_off)
	rooms._activate_room_item("sconce_a1")
	rooms._activate_room_item("sconce_a2")
	await _frames(3)
	rooms._sync_hall_lighting()
	var a_spotlights_visible := 0
	for light: Light3D in main.castle_room_light_nodes:
		if light.visible and String(light.get_meta("hall_half", "")) == "a":
			a_spotlights_visible += 1
	_ck("main_hall_all_lights_off_affects_engine",
		a_spotlights_visible == 0)
	var fill_off_energy := 1.0
	for light: Light3D in main.castle_room_light_nodes:
		if String(light.get_meta("castle_light_role", "")) == "ambient_fill":
			fill_off_energy = light.light_energy
	var glow_off: float = castle_environment.glow_intensity
	var bloom_off: float = castle_environment.glow_bloom
	_ck("main_hall_bloom_tracks_light_state",
		glow_off <= 0.25 and bloom_off <= 0.02
		and glow_off < glow_on and bloom_off < bloom_on
		and fill_off_energy < fill_on_energy,
		"on=%.3f/%.3f off=%.3f/%.3f fill=%.3f->%.3f" % [
			glow_on, bloom_on, glow_off, bloom_off,
			fill_on_energy, fill_off_energy])
	await _capture("main_hall_lights_off")
	_ck("main_hall_physical_portal_inventory",
		main.castle_room_door_hotspots.size() == 9
		and main.castle_room_door_hotspot_layer != null
		and main.castle_room_door_hotspot_layer.visible)
	var bunny_ids: Array[String] = [
		"sleepy_bunny", "shell_bunny", "runner_bunny"]
	var expected_bunny_roles := {
		"sleepy_bunny": "sleeping_static",
		"shell_bunny": "shell_static",
		"runner_bunny": "runner",
	}
	var bunny_assets_ok := true
	var bunny_start_positions: Dictionary = {}
	for item_id: String in bunny_ids:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {})
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		bunny_assets_ok = bunny_assets_ok \
			and sprite != null \
			and sprite.texture != null \
			and sprite.texture.resource_path.contains("dust_bunnies/") \
			and not sprite.shaded \
			and not sprite.no_depth_test \
			and record.get("hotspot") == null \
			and String(sprite.get_meta("dust_bunny_role", "")) \
				== String(expected_bunny_roles[item_id]) \
			and String(sprite.get_meta("spawn_guide_id", "")) == item_id
		if sprite != null:
			bunny_start_positions[item_id] = sprite.position
	_ck("main_hall_three_depth_card_dust_bunnies", bunny_assets_ok)
	_ck("main_hall_bunnies_are_proximity_only",
		main.castle_room_item_hotspot_layer.get_child_count() == 13)
	var camera_ray_touch_ok := true
	var camera_ray_details: Array[String] = []
	for item_id: String in bunny_ids:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {}) \
			as Dictionary
		var sprite: Sprite3D = record.get("sprite") as Sprite3D
		if sprite == null:
			camera_ray_touch_ok = false
			camera_ray_details.append(item_id + ":missing")
			continue
		var contact_foot: Vector2 = record.get(
			"contact_foot", Vector2.ZERO) as Vector2
		main.castle_room_camera.position = Vector3(
			rooms._hall_camera_x_for_foot(contact_foot.x), 0.0,
			main.castle_room_camera.position.z)
		rooms._sync_hall_horizontal_culling()
		var center_screen: Vector2 = main.castle_room_camera.unproject_position(
			sprite.global_position)
		var ray_origin: Vector3 = main.castle_room_camera.project_ray_origin(
			center_screen)
		var ray_direction: Vector3 = main.castle_room_camera.project_ray_normal(
			center_screen)
		var sprite_distance: float = (
			sprite.global_position - ray_origin).dot(ray_direction)
		var sprite_ray_point: Vector3 = \
			ray_origin + ray_direction * sprite_distance
		var ray_error: float = sprite_ray_point.distance_to(
			sprite.global_position)
		var mapped_foot: Vector2 = rooms._dust_bunny_foot_from_camera_ray(
			center_screen)
		var foot_error: float = mapped_foot.distance_to(contact_foot)
		camera_ray_touch_ok = camera_ray_touch_ok \
			and ray_error <= 0.01 \
			and mapped_foot != Vector2.INF \
			and foot_error <= 0.01
		camera_ray_details.append(
			"%s:ray=%.4f foot=%.4f mapped=%s" % [
				item_id, ray_error, foot_error, mapped_foot])
	main.castle_room_camera.position = left_camera_position
	rooms._sync_hall_horizontal_culling()
	_ck("main_hall_bunny_camera_ray_touch_mapping", camera_ray_touch_ok,
		";".join(camera_ray_details))
	rooms.tick(0.5)
	var sleepy_record: Dictionary = main.castle_room_item_sprites.get(
		"sleepy_bunny", {}) as Dictionary
	var shell_record: Dictionary = main.castle_room_item_sprites.get(
		"shell_bunny", {}) as Dictionary
	var runner_record: Dictionary = main.castle_room_item_sprites.get(
		"runner_bunny", {}) as Dictionary
	var sleepy_now: Sprite3D = sleepy_record.get("sprite") as Sprite3D
	var shell_now: Sprite3D = shell_record.get("sprite") as Sprite3D
	var runner_now: Sprite3D = runner_record.get("sprite") as Sprite3D
	var static_bunnies_ok: bool = sleepy_now != null and shell_now != null
	if static_bunnies_ok:
		var sleepy_start: Vector3 = bunny_start_positions.get(
			"sleepy_bunny", Vector3.INF) as Vector3
		var shell_start: Vector3 = bunny_start_positions.get(
			"shell_bunny", Vector3.INF) as Vector3
		static_bunnies_ok = sleepy_now.position == sleepy_start \
			and shell_now.position == shell_start
	_ck("main_hall_two_static_dust_bunnies", static_bunnies_ok)
	var runner_moves_ok: bool = runner_now != null
	if runner_moves_ok:
		var runner_start: Vector3 = bunny_start_positions.get(
			"runner_bunny", Vector3.INF) as Vector3
		runner_moves_ok = runner_now.position.distance_to(runner_start) > 0.01
	_ck("main_hall_third_dust_bunny_runs", runner_moves_ok)
	var explosion_effects_before: int = \
		main.castle_room_item_effect_layer.get_child_count()
	var one_touch_explosions_ok := true
	for item_id: String in bunny_ids:
		var record: Dictionary = main.castle_room_item_sprites.get(item_id, {})
		var bunny_sprite: Sprite3D = record.get("sprite") as Sprite3D
		var contact_foot: Vector2 = record.get(
			"contact_foot", Vector2.ZERO) as Vector2
		rooms._position_player_at_foot(contact_foot, false)
		rooms.tick(0.016)
		one_touch_explosions_ok = one_touch_explosions_ok \
			and bunny_sprite != null \
			and bool(bunny_sprite.get_meta("exploding", false)) \
			and not main.castle_room_item_sprites.has(item_id) \
			and bool((main.g.get(
				"castle_dust_bunnies_cleared", {}) as Dictionary).get(
					item_id, false))
	_ck("main_hall_one_touch_dust_bunny_explosions",
		one_touch_explosions_ok \
		and main.castle_room_item_effect_layer.get_child_count() \
			>= explosion_effects_before + bunny_ids.size() * 12)
	var cleared_count_before_repeat: int = (
		main.g.get("castle_dust_bunnies_cleared", {}) as Dictionary).size()
	for item_id: String in bunny_ids:
		rooms._explode_dust_bunny(item_id)
	_ck("main_hall_dust_bunny_explosions_exactly_once",
		(main.g.get("castle_dust_bunnies_cleared", {}) as Dictionary).size()
			== cleared_count_before_repeat
		and cleared_count_before_repeat == 3)
	rooms.show_room("library", false)
	rooms.show_room("main_hall", false)
	_ck("main_hall_dust_bunnies_do_not_respawn_this_visit",
		main.castle_room_item_sprites.size() == 13
		and main.castle_room_item_hotspot_layer.get_child_count() == 13)
	rooms._position_player_at_foot(Vector2(2500.0, 835.0), false)
	await _frames(2)
	rooms.tick(1.0)
	_ck("main_hall_two_screen_camera_travel",
		main.castle_room_camera.position.x > 5.0,
		"camera_x=%.2f" % main.castle_room_camera.position.x)
	await _capture("main_hall_screen_b")
	elevator_button.pressed.emit()
	await _frames(2)
	_ck("storybook_elevator_expands_over_every_castle_room",
		main.castle_room_menu_open and main.castle_room_menu_panel.visible)
	await _capture("elevator_menu")
	rooms._set_elevator_menu_open(false, false)
	# Opera remains walkable through its painted physical door; the elevator is
	# an additional child-friendly travel aid, not a replacement doorway.
	var opera_door: Button = main.castle_room_buttons.get(
		"opera_hall") as Button
	if opera_door != null:
		opera_door.pressed.emit()
	await create_timer(1.2).timeout
	_ck("opera_opens_from_physical_hall_door",
		main.castle_room_id == "opera_hall")
	rooms.activate_current_room()
	await _frames(40)
	var opera_opened: bool = main.game == "opera" and main.opera_game != null
	_ck("opera_activity_opens_from_sprite_room", opera_opened)
	if opera_opened:
		main.opera_game._leave_early()
		await _frames(6)
	_ck("opera_returns_to_sprite_room",
		main.game == "level2"
		and String(main.g.get("phase", "")) == "hall"
		and rooms.is_open()
		and main.castle_room_id == "opera_hall")
	if main.castle_room_back_button != null:
		main.castle_room_back_button.pressed.emit()
	await _frames(4)
	_ck("room_back_has_single_main_hall_destination",
		main.castle_room_id == "main_hall"
		and main.castle_room_back_button.tooltip_text == "Castle courtyard")
	var environment_before_suspend: Environment = \
		main.castle_room_previous_environment
	rooms.suspend()
	_ck("castle_environment_restores_on_suspend",
		main.we_node.environment == environment_before_suspend)
	rooms.resume()
	_ck("castle_environment_reactivates_on_resume",
		main.we_node.environment == main.castle_room_environment)

	print("CASTLE_ART|RESULT=", "FAIL" if checks_failed > 0 else "OK",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)

func _init() -> void:
	call_deferred("_run")
