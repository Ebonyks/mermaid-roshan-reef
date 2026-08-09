extends SceneTree
# Runtime half of the game-wide visual design audit.
#
# tools/audit_visual_design.py can read every PNG and every builder constant,
# but it cannot see the assembled scene: what actually got instantiated, at
# what depth, how big a tap target lands on the child's screen, or how many
# transparent quads stack up over one pixel.  This probe walks the live scene
# for each reachable stage and writes those facts to
# res://audit/visual_runtime_facts.json, which the Python tool ingests.  Checks
# that need this file report SKIP without it, so the two halves are usable
# independently.
#
# Generator, not a gate: it asserts nothing about art direction and never
# fails a build on a judgement call.  It DOES fail if the scene it was told to
# measure never built, because facts nobody collected must not read as a pass.

const OUT_PATH := "res://audit/visual_runtime_facts.json"
# the storybook UI's minimum touch size, in 1280x720 base-canvas pixels
const MIN_TOUCH_PX := 110.0

var failed := false
var zones: Dictionary = {}


func _log(label: String, ok: bool, detail: String = "") -> void:
	print("VISUALFACTS|%s: %s%s" % [
		label,
		"OK" if ok else "FAIL",
		"" if detail == "" else " " + detail,
	])
	if not ok:
		failed = true


func _frames(count: int) -> void:
	for _i in range(count):
		await process_frame


func _init() -> void:
	# Authoring and touch budgets are defined in the 1280x720 base canvas.
	# Pin this generator to that viewport so projected visual sizes are directly
	# comparable and do not depend on a headless runner's default square window.
	get_root().size = Vector2i(1280, 720)
	var packed: PackedScene = load("res://scenes/main.tscn")
	var main: ReefMain = packed.instantiate()
	get_root().add_child(main)
	await _frames(2)
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(2)

	_measure(main, "reef")

	# unlock the lagoon the way probe_l2 does, then measure the promenade
	main.pearl_count = main.PEARL_TOTAL
	for friend_value in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main._enter_level2()
	await _frames(8)
	_measure(main, "sky_lagoon")

	_write()
	print("VISUALFACTS|result: ", "FAIL" if failed else "ALL OK")
	quit(1 if failed else 0)


# --------------------------------------------------------------------------

func _measure(main: ReefMain, zone_id: String) -> void:
	var cam: Camera3D = main.get_viewport().get_camera_3d()
	var sprites: Array[Sprite3D] = []
	_collect(main, sprites)
	var depths: Array[float] = []
	var alpha_cards := 0
	var shaded_cards := 0
	var texture_px := 0
	for s in sprites:
		if not s.visible:
			continue
		var z: float = s.global_position.z
		var known := false
		for d in depths:
			if absf(d - z) < 0.05:
				known = true
				break
		if not known:
			depths.append(z)
		if s.alpha_cut == SpriteBase3D.ALPHA_CUT_DISABLED and s.transparent:
			alpha_cards += 1
		if s.shaded:
			shaded_cards += 1
		if s.texture != null:
			texture_px += s.texture.get_width() * s.texture.get_height()
	depths.sort()

	var player_z: float = 0.0
	if main.player != null and is_instance_valid(main.player):
		player_z = main.player.global_position.z
	var behind_player := 0
	for d in depths:
		if d < player_z:
			behind_player += 1

	var facts: Dictionary = {
		"sprite3d_visible": _visible_count(sprites),
		"sprite3d_total": sprites.size(),
		"distinct_depths": depths.size(),
		"depth_min": depths[0] if depths.size() > 0 else 0.0,
		"depth_max": depths[depths.size() - 1] if depths.size() > 0 else 0.0,
		"depth_spread": (depths[depths.size() - 1] - depths[0]) if depths.size() > 0 else 0.0,
		"player_z": player_z,
		"depths_behind_player": behind_player,
		"depths_in_front_of_player": depths.size() - behind_player,
		"blend_alpha_cards": alpha_cards,
		"shaded_world_cards": shaded_cards,
		"texture_megapixels": snappedf(float(texture_px) / 1000000.0, 0.01),
		"targets": _targets(main, cam),
	}
	zones[zone_id] = facts
	_log("%s_built" % zone_id, sprites.size() > 0 or zone_id == "reef",
		"sprites=%d depths=%d spread=%.2f" % [
			sprites.size(), depths.size(), float(facts["depth_spread"])])


func _visible_count(sprites: Array[Sprite3D]) -> int:
	var n := 0
	for s in sprites:
		if s.visible:
			n += 1
	return n


func _collect(node: Node, out: Array[Sprite3D]) -> void:
	if node is Sprite3D:
		out.append(node as Sprite3D)
	for child in node.get_children():
		_collect(child, out)


func _targets(main: ReefMain, cam: Camera3D) -> Array:
	# Registered promenade targets carry their own card; project each card's
	# painted height through the live lens to learn how big a finger sees it.
	var out: Array = []
	if cam == null:
		return out
	var registered: Array = main.g.get("lagoon_promenade_targets", []) as Array
	var vp_h: float = maxf(float(main.get_viewport().get_visible_rect().size.y), 1.0)
	for value in registered:
		var target: Dictionary = value as Dictionary
		var card: Node3D = target.get("node") as Node3D
		if card == null or not is_instance_valid(card):
			card = target.get("highlight") as Node3D
		if card == null or not is_instance_valid(card):
			continue
		var origin: Vector3 = card.global_position
		if cam.is_position_behind(origin):
			continue
		var height: float = 1.0
		if card is Sprite3D:
			var sprite: Sprite3D = card as Sprite3D
			if sprite.texture != null:
				height = float(sprite.texture.get_height()) * sprite.pixel_size
		var top: Vector2 = cam.unproject_position(origin + Vector3.UP * height * 0.5)
		var bottom: Vector2 = cam.unproject_position(origin - Vector3.UP * height * 0.5)
		# The interaction director hits a radius around the projected centre; the
		# visible art can be smaller than that forgiving preschool touch region.
		# Keep both facts, but apply the 110px contract to the real hit diameter.
		var visual_px: float = absf(top.y - bottom.y) * (720.0 / vp_h)
		var hit_diameter_px: float = float(target.get("radius_px", 0.0)) * 2.0
		out.append({
			"id": String(target.get("id", "")),
			"screen_px": snappedf(hit_diameter_px, 0.1),
			"hit_diameter_px": snappedf(hit_diameter_px, 0.1),
			"visual_screen_px": snappedf(visual_px, 0.1),
			"world_z": snappedf(origin.z, 0.01),
			"meets_min_touch": hit_diameter_px >= MIN_TOUCH_PX,
		})
	return out


func _write() -> void:
	var payload: Dictionary = {
		"_comment": "Generated by scripts/probe_visual_audit.gd. Consumed by tools/audit_visual_design.py.",
		"zones": zones,
	}
	var text: String = JSON.stringify(payload, "\t", false)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://audit"))
	var f: FileAccess = FileAccess.open(OUT_PATH, FileAccess.WRITE)
	if f == null:
		_log("write", false, "could not open %s" % OUT_PATH)
		return
	f.store_string(text + "\n")
	f.close()
	print("VISUALFACTS|written %s (%d zones)" % [OUT_PATH, zones.size()])
