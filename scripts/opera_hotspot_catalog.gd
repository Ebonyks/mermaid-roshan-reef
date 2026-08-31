class_name OperaHotspotCatalog
extends RefCounted
## Approved transparent object art for the diegetic Opera activity hotspots.
##
## Each shipping career phase declares one honest presentation: highlight the
## authored painted landmark, add a transparent local effect to it, or animate
## one isolated prop cutout. Full widget cards, opaque presentation fields,
## easels, task frames and broad stage tableaus are deliberately excluded.

const MIN_ALPHA_GUTTER := 6
const ALPHA_EDGE_MAX := 0.04
const MIN_VISUAL_SIZE := 48.0
const MAX_VISUAL_SIZE := 220.0
const MAX_VISUAL_OFFSET := 140.0

const VALID_MOTIONS: Array[String] = [
	"breathe", "spin", "rock", "tilt", "pour",
	"bounce", "shake", "slide", "pulse",
]
const VALID_PRESENTATIONS: Array[String] = ["overlay", "effect", "painted"]

## Kept beside SPECS so probes can compare this catalog with the shipping
## phase table without loading a career scene.
const EXPECTED_PHASES: Dictionary = {
	"chef": ["MIX", "STIR", "BAKE", "FROST", "TOP"],
	"detective": ["SEARCH", "CASE BOARD", "CROWN"],
	"ballerina": ["PHRASE", "POSE", "RIBBON", "TWIRL"],
	"candymaker": ["SYRUP", "SORT", "WRAP", "SHARE"],
	"doctor": ["WASH", "FIND", "X-RAY", "CAST", "BANDAGE"],
	"farmer": ["PLANT", "TOSS", "HERD", "PICNIC"],
	"boxer": ["COMBO", "TITLE ROUND", "BELT"],
	"magician": ["VANISH", "TRACK", "ROPE", "CABINET", "PORTAL"],
	"painter": ["PAINT", "STAMPS", "GALLERY"],
	"astronaut": ["PIPES", "PATCH", "VALVE", "LAUNCH"],
	"racer": ["TUNE", "TO THE LINE", "RACE"],
	"nursery": ["WASH HANDS", "CATCH BABIES", "FEED", "BURP", "BEDTIME"],
	"popstar": ["SOUND CHECK", "DANCE", "RHYTHM", "ENCORE"],
	"geologist": ["LAYERS", "FOSSIL", "SORT", "CRYSTAL"],
}

## Runtime consumes path, motion, size, presentation and an optional local
## landmark offset. Display sizes preserve each source canvas's aspect ratio;
## the independent hit target remains generous even for a wide, shallow object
## such as the magician rope.
const SPECS: Dictionary = {
	"chef": {
		"MIX": {"path": "res://assets/opera/worlds/widgets/widget_pour_chef_mover.png", "motion": "pour", "size": Vector2(126, 126), "presentation": "painted"},
		"STIR": {"path": "res://assets/opera/worlds/widgets/widget_crank_chef_mover.png", "motion": "spin", "size": Vector2(124, 124), "presentation": "painted"},
		"BAKE": {"path": "res://assets/opera/worlds/props/goal_chef.png", "motion": "pulse", "size": Vector2(150, 150), "presentation": "painted"},
		"FROST": {"path": "res://assets/opera/worlds/props/goal_chef.png", "motion": "rock", "size": Vector2(150, 150), "presentation": "painted"},
		"TOP": {"path": "res://assets/opera/worlds/widgets/widget_target_chef_piece_0.png", "motion": "bounce", "size": Vector2(68, 68), "offset": Vector2(65, -45), "presentation": "overlay"},
	},
	"detective": {
		"SEARCH": {"path": "res://assets/opera/worlds/ui/magnifier.png", "motion": "rock", "size": Vector2(136, 136), "presentation": "painted"},
		"CASE BOARD": {"path": "res://assets/opera/worlds/widgets/widget_clue_board_tokens.png", "motion": "slide", "size": Vector2(144, 48), "presentation": "painted"},
		"CROWN": {"path": "res://assets/opera/worlds/widgets/widget_crown_chest_closed.png", "motion": "shake", "size": Vector2(148, 148), "presentation": "painted"},
	},
	"ballerina": {
		"PHRASE": {"path": "res://assets/opera/worlds/widgets/widget_lanes_ballerina_lit.png", "motion": "pulse", "size": Vector2(210, 70), "presentation": "painted"},
		"POSE": {"path": "res://assets/opera/worlds/props/goal_ballerina.png", "motion": "breathe", "size": Vector2(140, 140), "presentation": "painted"},
		"RIBBON": {"path": "res://assets/opera/worlds/widgets/widget_crank_ballerina_mover.png", "motion": "slide", "size": Vector2(142, 142), "presentation": "painted"},
		"TWIRL": {"path": "res://assets/opera/worlds/widgets/widget_crank_ballerina_mover.png", "motion": "spin", "size": Vector2(142, 142), "presentation": "painted"},
	},
	"candymaker": {
		"SYRUP": {"path": "res://assets/opera/worlds/widgets/widget_pour_candymaker_mover.png", "motion": "pour", "size": Vector2(180, 90), "presentation": "painted"},
		"SORT": {"path": "res://assets/opera/worlds/widgets/widget_target_candymaker_piece_0.png", "motion": "bounce", "size": Vector2(104, 104), "presentation": "overlay"},
		"WRAP": {"path": "res://assets/opera/worlds/props/goal_candymaker.png", "motion": "spin", "size": Vector2(124, 124), "presentation": "painted"},
		"SHARE": {"path": "res://assets/opera/worlds/widgets/widget_target_candymaker_mover.png", "motion": "bounce", "size": Vector2(112, 112), "presentation": "overlay"},
	},
	"doctor": {
		"WASH": {"path": "res://assets/opera/worlds/widgets/widget_basin_doctor_bubbles.png", "motion": "pulse", "size": Vector2(220, 131), "presentation": "effect"},
		"FIND": {"path": "res://assets/opera/worlds/props/goal_doctor.png", "motion": "bounce", "size": Vector2(136, 136), "presentation": "painted"},
		"X-RAY": {"path": "res://assets/opera/worlds/widgets/widget_target_doctor_mover.png", "motion": "pulse", "size": Vector2(104, 104), "offset": Vector2(112, 10), "presentation": "overlay"},
		"CAST": {"path": "res://assets/opera/worlds/widgets/widget_crank_doctor_mover.png", "motion": "spin", "size": Vector2(88, 88), "offset": Vector2(112, 14), "presentation": "overlay"},
		"BANDAGE": {"path": "res://assets/opera/worlds/widgets/widget_crank_doctor_mover.png", "motion": "rock", "size": Vector2(112, 112), "presentation": "overlay"},
	},
	"farmer": {
		"PLANT": {"path": "res://assets/opera/worlds/widgets/widget_target_farmer_piece_2.png", "motion": "pulse", "size": Vector2(104, 104), "presentation": "painted"},
		"TOSS": {"path": "res://assets/opera/worlds/widgets/widget_target_farmer_piece_0.png", "motion": "bounce", "size": Vector2(100, 100), "presentation": "overlay"},
		"HERD": {"path": "res://assets/opera/worlds/widgets/widget_track_farmer_mover.png", "motion": "slide", "size": Vector2(126, 126), "presentation": "painted"},
		"PICNIC": {"path": "res://assets/opera/worlds/props/goal_farmer.png", "motion": "rock", "size": Vector2(84, 84), "offset": Vector2(0, 104), "presentation": "overlay"},
	},
	"boxer": {
		"COMBO": {"path": "res://assets/opera/worlds/widgets/widget_track_boxer_mover.png", "motion": "shake", "size": Vector2(128, 128), "presentation": "painted"},
		"TITLE ROUND": {"path": "res://assets/opera/worlds/widgets/widget_push_boxer_mover.png", "motion": "bounce", "size": Vector2(134, 134), "presentation": "overlay"},
		"BELT": {"path": "res://assets/opera/worlds/widgets/widget_target_boxer_mover.png", "motion": "pulse", "size": Vector2(154, 154), "presentation": "overlay"},
	},
	"magician": {
		"VANISH": {"path": "res://assets/opera/worlds/widgets/widget_magic_vanish_wand.png", "motion": "rock", "size": Vector2(160, 160), "presentation": "painted"},
		"TRACK": {"path": "res://assets/opera/worlds/widgets/widget_track_magician_mover.png", "motion": "slide", "size": Vector2(120, 120), "presentation": "overlay"},
		"ROPE": {"path": "res://assets/opera/worlds/hotspots/magician_rope.png", "motion": "rock", "size": Vector2(220, 55), "offset": Vector2(0, 12), "presentation": "overlay"},
		"CABINET": {"path": "res://assets/opera/worlds/widgets/widget_magic_cabinet_closed.png", "motion": "shake", "size": Vector2(150, 150), "presentation": "overlay"},
		"PORTAL": {"path": "res://assets/opera/worlds/widgets/widget_portal_magician_mover.png", "motion": "pulse", "size": Vector2(144, 144), "presentation": "overlay"},
	},
	"painter": {
		"PAINT": {"path": "res://assets/opera/worlds/widgets/widget_pour_painter_mover.png", "motion": "pulse", "size": Vector2(136, 136), "presentation": "painted"},
		"STAMPS": {"path": "res://assets/opera/worlds/widgets/widget_target_painter_mark.png", "motion": "pulse", "size": Vector2(88, 88), "presentation": "effect"},
		# The room frame is intentionally blank until this beat. The accepted
		# sunrise is therefore a completion insert, not a duplicate easel.
		"GALLERY": {"path": "res://assets/opera/worlds/props/goal_painter.png", "motion": "pulse", "size": Vector2(142, 142), "presentation": "overlay"},
	},
	"astronaut": {
		"PIPES": {"path": "res://assets/opera/worlds/widgets/widget_crank_astronaut_mover.png", "motion": "rock", "size": Vector2(124, 124), "presentation": "painted"},
		"PATCH": {"path": "res://assets/opera/worlds/widgets/widget_target_astronaut_piece_1.png", "motion": "pulse", "size": Vector2(82, 82), "offset": Vector2(-58, 35), "presentation": "overlay"},
		"VALVE": {"path": "res://assets/opera/worlds/widgets/widget_crank_astronaut_mover.png", "motion": "spin", "size": Vector2(124, 124), "presentation": "overlay"},
		"LAUNCH": {"path": "res://assets/opera/worlds/props/goal_astronaut.png", "motion": "bounce", "size": Vector2(144, 144), "presentation": "painted"},
	},
	"racer": {
		"TUNE": {"path": "res://assets/opera/worlds/widgets/widget_crank_racer_mover.png", "motion": "rock", "size": Vector2(110, 110), "presentation": "overlay"},
		"TO THE LINE": {"path": "res://assets/opera/worlds/widgets/widget_push_racer_mover.png", "motion": "slide", "size": Vector2(138, 138), "presentation": "painted"},
		"RACE": {"path": "res://assets/opera/worlds/widgets/widget_push_racer_mover.png", "motion": "bounce", "size": Vector2(118, 118), "offset": Vector2(0, 40), "presentation": "overlay"},
	},
	"nursery": {
		"WASH HANDS": {"path": "res://assets/opera/worlds/widgets/widget_basin_nursery_bubbles.png", "motion": "pulse", "size": Vector2(220, 131), "presentation": "effect"},
		"CATCH BABIES": {"path": "res://assets/opera/worlds/nursery/baby_0.png", "motion": "bounce", "size": Vector2(104, 104), "offset": Vector2(0, 24), "presentation": "overlay"},
		"FEED": {"path": "res://assets/opera/worlds/widgets/widget_pour_nursery_mover.png", "motion": "tilt", "size": Vector2(108, 108), "presentation": "overlay"},
		"BURP": {"path": "res://assets/opera/worlds/nursery/baby_1.png", "motion": "rock", "size": Vector2(108, 108), "offset": Vector2(0, 22), "presentation": "overlay"},
		"BEDTIME": {"path": "res://assets/opera/worlds/props/goal_nursery.png", "motion": "rock", "size": Vector2(150, 150), "presentation": "painted"},
	},
	"popstar": {
		"SOUND CHECK": {"path": "res://assets/opera/worlds/props/goal_popstar.png", "motion": "pulse", "size": Vector2(142, 142), "presentation": "painted"},
		"DANCE": {"path": "res://assets/opera/worlds/widgets/widget_track_popstar_mover.png", "motion": "pulse", "size": Vector2(120, 120), "presentation": "effect"},
		"RHYTHM": {"path": "res://assets/opera/worlds/widgets/widget_crank_popstar_mover.png", "motion": "pulse", "size": Vector2(128, 128), "presentation": "painted"},
		"ENCORE": {"path": "res://assets/opera/worlds/props/goal_popstar.png", "motion": "rock", "size": Vector2(142, 142), "presentation": "painted"},
	},
	"geologist": {
		"LAYERS": {"path": "res://assets/opera/worlds/hotspots/geologist_layered_rock.svg", "motion": "pulse", "size": Vector2(128, 128), "presentation": "painted"},
		"FOSSIL": {"path": "res://assets/opera/worlds/hotspots/geologist_fossil.svg", "motion": "rock", "size": Vector2(132, 132), "presentation": "painted"},
		"SORT": {"path": "res://assets/opera/worlds/hotspots/geologist_layered_rock.svg", "motion": "bounce", "size": Vector2(112, 112), "presentation": "overlay"},
		"CRYSTAL": {"path": "res://assets/opera/worlds/props/goal_geologist.svg", "motion": "pulse", "size": Vector2(150, 150), "presentation": "painted"},
	},
}

## Exact imported source-canvas dimensions verified against the repository PNGs.
## Painted entries retain their themed cutout here as provenance/source evidence
## even though runtime draws only the landmark glow. Roles remain limited to
## isolated objects, small object groups, or transparent local effects; a
## card/tableau role is not valid in this catalog.
const ASSET_META: Dictionary = {
	"res://assets/opera/worlds/widgets/widget_pour_chef_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_crank_chef_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/props/goal_chef.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_target_chef_piece_0.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/ui/magnifier.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_clue_board_tokens.png": {"dimensions": Vector2i(768, 256), "role": "object_group"},
	"res://assets/opera/worlds/widgets/widget_crown_chest_closed.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_crank_ballerina_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_lanes_ballerina_lit.png": {"dimensions": Vector2i(768, 256), "role": "object_group"},
	"res://assets/opera/worlds/props/goal_ballerina.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_pour_candymaker_mover.png": {"dimensions": Vector2i(512, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_target_candymaker_piece_0.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/props/goal_candymaker.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_target_candymaker_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_basin_doctor_bubbles.png": {"dimensions": Vector2i(1024, 608), "role": "effect"},
	"res://assets/opera/worlds/props/goal_doctor.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_target_doctor_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_crank_doctor_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_target_farmer_piece_2.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_target_farmer_piece_0.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_track_farmer_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/props/goal_farmer.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_track_boxer_mover.png": {"dimensions": Vector2i(256, 256), "role": "object_group"},
	"res://assets/opera/worlds/widgets/widget_push_boxer_mover.png": {"dimensions": Vector2i(256, 256), "role": "object_group"},
	"res://assets/opera/worlds/widgets/widget_target_boxer_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_magic_vanish_wand.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_track_magician_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/hotspots/magician_rope.png": {"dimensions": Vector2i(512, 128), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_magic_cabinet_closed.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_portal_magician_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_pour_painter_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_target_painter_mark.png": {"dimensions": Vector2i(128, 128), "role": "effect"},
	"res://assets/opera/worlds/props/goal_painter.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_crank_astronaut_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_target_astronaut_piece_1.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/props/goal_astronaut.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_crank_racer_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_push_racer_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_basin_nursery_bubbles.png": {"dimensions": Vector2i(1024, 608), "role": "effect"},
	"res://assets/opera/worlds/nursery/baby_0.png": {"dimensions": Vector2i(320, 320), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_pour_nursery_mover.png": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/nursery/baby_1.png": {"dimensions": Vector2i(320, 320), "role": "object"},
	"res://assets/opera/worlds/props/goal_nursery.png": {"dimensions": Vector2i(1024, 1024), "role": "object_group"},
	"res://assets/opera/worlds/props/goal_popstar.png": {"dimensions": Vector2i(512, 512), "role": "object"},
	"res://assets/opera/worlds/widgets/widget_track_popstar_mover.png": {"dimensions": Vector2i(256, 256), "role": "effect"},
	"res://assets/opera/worlds/widgets/widget_crank_popstar_mover.png": {"dimensions": Vector2i(256, 256), "role": "object_group"},
	"res://assets/opera/worlds/hotspots/geologist_layered_rock.svg": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/hotspots/geologist_fossil.svg": {"dimensions": Vector2i(256, 256), "role": "object"},
	"res://assets/opera/worlds/props/goal_geologist.svg": {"dimensions": Vector2i(256, 256), "role": "object_group"},
}


static func spec(career: String, phase_name: String) -> Dictionary:
	var career_specs: Dictionary = SPECS.get(career, {}) as Dictionary
	if not career_specs.has(phase_name):
		return {}
	return (career_specs[phase_name] as Dictionary).duplicate(true)


static func all_specs() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for career: String in SPECS:
		var career_specs: Dictionary = SPECS[career] as Dictionary
		for phase_name: String in career_specs:
			var entry: Dictionary = (career_specs[phase_name] as Dictionary).duplicate(true)
			entry["career"] = career
			entry["phase"] = phase_name
			result.append(entry)
	return result


static func has_spec(career: String, phase_name: String) -> bool:
	var career_specs: Dictionary = SPECS.get(career, {}) as Dictionary
	return career_specs.has(phase_name)


static func phases_for(career: String) -> PackedStringArray:
	var result: PackedStringArray = PackedStringArray()
	var career_specs: Dictionary = SPECS.get(career, {}) as Dictionary
	for phase_name: String in career_specs:
		result.append(phase_name)
	return result


## Returns every structural, resource, dimension, aspect and alpha-gutter
## problem. An empty array is the probe-ready success result.
static func validate_specs() -> PackedStringArray:
	var errors: PackedStringArray = PackedStringArray()
	var referenced_paths: Dictionary = {}
	var checked_paths: Dictionary = {}

	for career: String in EXPECTED_PHASES:
		var expected: Array = EXPECTED_PHASES[career] as Array
		for phase_value: Variant in expected:
			var phase_name := String(phase_value)
			if not has_spec(career, phase_name):
				errors.append("missing spec: %s/%s" % [career, phase_name])

	for career: String in SPECS:
		if not EXPECTED_PHASES.has(career):
			errors.append("unexpected career: %s" % career)
		var career_specs: Dictionary = SPECS[career] as Dictionary
		for phase_name: String in career_specs:
			if EXPECTED_PHASES.has(career) \
					and phase_name not in (EXPECTED_PHASES[career] as Array):
				errors.append("unexpected phase: %s/%s" % [career, phase_name])
			var entry: Dictionary = career_specs[phase_name] as Dictionary
			_validate_entry(career, phase_name, entry, errors)
			var path := String(entry.get("path", ""))
			if path.is_empty():
				continue
			referenced_paths[path] = true
			if checked_paths.has(path):
				continue
			checked_paths[path] = true
			errors.append_array(_validate_asset(path))

	for path: String in ASSET_META:
		if not referenced_paths.has(path):
			errors.append("unused asset metadata: %s" % path)
	return errors


static func _validate_entry(career: String, phase_name: String,
		entry: Dictionary, errors: PackedStringArray) -> void:
	var label := "%s/%s" % [career, phase_name]
	for required_key: String in ["path", "motion", "size", "presentation"]:
		if not entry.has(required_key):
			errors.append("%s missing %s" % [label, required_key])
	var path := String(entry.get("path", ""))
	if not _allowed_runtime_path(path):
		errors.append("%s uses disallowed art: %s" % [label, path])
	if not ASSET_META.has(path):
		errors.append("%s has no verified asset metadata: %s" % [label, path])
	var motion := String(entry.get("motion", ""))
	if motion not in VALID_MOTIONS:
		errors.append("%s has unsupported motion: %s" % [label, motion])
	var presentation := String(entry.get("presentation", ""))
	if presentation not in VALID_PRESENTATIONS:
		errors.append("%s has unsupported presentation: %s" % [
			label, presentation])
	elif ASSET_META.has(path):
		var presentation_meta: Dictionary = ASSET_META[path] as Dictionary
		var role := String(presentation_meta.get("role", ""))
		if presentation == "effect" and role != "effect":
			errors.append("%s effect presentation uses %s art: %s" % [
				label, role, path])
		elif presentation == "overlay" and role == "effect":
			errors.append("%s overlay presentation uses effect art: %s" % [
				label, path])
	var visual_size: Vector2 = entry.get("size", Vector2.ZERO) as Vector2
	if visual_size.x < MIN_VISUAL_SIZE or visual_size.y < MIN_VISUAL_SIZE \
			or visual_size.x > MAX_VISUAL_SIZE or visual_size.y > MAX_VISUAL_SIZE:
		errors.append("%s has unsafe visual size: %s" % [label, visual_size])
	if ASSET_META.has(path) and visual_size.y > 0.0:
		var meta: Dictionary = ASSET_META[path] as Dictionary
		var dimensions: Vector2i = meta.get("dimensions", Vector2i.ZERO) as Vector2i
		if dimensions.y > 0 and bool(meta.get("aspect_locked", true)):
			var source_aspect := float(dimensions.x) / float(dimensions.y)
			var visual_aspect := visual_size.x / visual_size.y
			if absf(source_aspect - visual_aspect) > source_aspect * 0.025:
				errors.append("%s distorts source aspect: %s -> %s" % [
					label, dimensions, visual_size])
	var display_offset: Vector2 = entry.get("offset", Vector2.ZERO) as Vector2
	if absf(display_offset.x) > MAX_VISUAL_OFFSET \
			or absf(display_offset.y) > MAX_VISUAL_OFFSET:
		errors.append("%s has unsafe landmark offset: %s" % [label, display_offset])


static func _allowed_runtime_path(path: String) -> bool:
	if path == "res://assets/opera/worlds/ui/magnifier.png":
		return true
	return path.begins_with("res://assets/opera/worlds/widgets/") \
		or path.begins_with("res://assets/opera/worlds/hotspots/") \
		or path.begins_with("res://assets/opera/worlds/props/goal_") \
		or path.begins_with("res://assets/opera/worlds/nursery/baby_")


static func _validate_asset(path: String) -> PackedStringArray:
	var errors: PackedStringArray = PackedStringArray()
	if not ResourceLoader.exists(path):
		errors.append("missing hotspot asset: %s" % path)
		return errors
	var texture: Texture2D = ResourceLoader.load(path) as Texture2D
	if texture == null:
		errors.append("hotspot asset is not Texture2D: %s" % path)
		return errors
	var meta: Dictionary = ASSET_META.get(path, {}) as Dictionary
	var expected: Vector2i = meta.get("dimensions", Vector2i.ZERO) as Vector2i
	var actual := Vector2i(texture.get_width(), texture.get_height())
	if actual != expected:
		errors.append("hotspot dimensions changed: %s expected %s got %s" % [
			path, expected, actual])
	var role := String(meta.get("role", ""))
	if role not in ["object", "object_group", "effect"]:
		errors.append("hotspot asset has rejected role %s: %s" % [role, path])
	var image: Image = texture.get_image()
	if image == null or image.is_empty():
		errors.append("hotspot asset has no readable image: %s" % path)
		return errors
	if image.is_compressed():
		var decompress_error: Error = image.decompress()
		if decompress_error != OK:
			errors.append("hotspot asset could not be decompressed for alpha audit: %s" % path)
			return errors
	if image.get_width() <= MIN_ALPHA_GUTTER * 2 \
			or image.get_height() <= MIN_ALPHA_GUTTER * 2:
		errors.append("hotspot asset too small for alpha audit: %s" % path)
	elif not _has_clear_alpha_gutter(image):
		errors.append("hotspot asset lost %dpx alpha gutter: %s" % [
			MIN_ALPHA_GUTTER, path])
	return errors


static func _has_clear_alpha_gutter(image: Image) -> bool:
	var width := image.get_width()
	var height := image.get_height()
	for inset in range(MIN_ALPHA_GUTTER):
		for x in range(width):
			if image.get_pixel(x, inset).a > ALPHA_EDGE_MAX \
					or image.get_pixel(x, height - 1 - inset).a > ALPHA_EDGE_MAX:
				return false
		for y in range(height):
			if image.get_pixel(inset, y).a > ALPHA_EDGE_MAX \
					or image.get_pixel(width - 1 - inset, y).a > ALPHA_EDGE_MAX:
				return false
	return true
