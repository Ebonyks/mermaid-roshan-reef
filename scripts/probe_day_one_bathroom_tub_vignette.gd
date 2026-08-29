extends SceneTree
## Deterministic Canvas2D contract for the filled, dirty Day One bathtub seam.
## The probe uses an in-memory fixture record so no room plate or asset is edited.

const ROOMS_SCRIPT: GDScript = preload(
	"res://scripts/arena/castle_rooms_25d.gd")
const WATER_SHADER: Shader = preload(
	"res://assets/shaders/castle_fixture_water.gdshader")
const CLEAN_ROOM_TEXTURE: Texture2D = preload(
	"res://assets/flats/castle/rooms/room_bubble_bath.png")
const DIRTY_ROOM_TEXTURE: Texture2D = preload(
	"res://assets/flats/castle/rooms/room_bubble_bath_dirty_day_one.png")

var checks_failed: int = 0


func _init() -> void:
	call_deferred("_run")


func _check(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("DAY_ONE_BATHTUB_TUB_VIGNETTE|", label, ": ",
		"OK" if ok else "FAIL",
		(" " + detail if detail != "" else ""))


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _all_canvas_items(node: Node) -> bool:
	for child: Node in node.get_children():
		if not child is CanvasItem:
			return false
		if not _all_canvas_items(child):
			return false
	return true


func _run() -> void:
	var main: ReefMain = ReefMain.new()
	var host: Node2D = Node2D.new()
	host.name = "DayOneBathtubVignetteHost"
	root.add_child(host)
	var dirty_room_plate := Sprite2D.new()
	dirty_room_plate.name = "DayOneDirtyBathroomPlate"
	dirty_room_plate.texture = DIRTY_ROOM_TEXTURE
	host.add_child(dirty_room_plate)
	_check("clean and dirty bathroom art are distinct true-2D versions",
		DIRTY_ROOM_TEXTURE != CLEAN_ROOM_TEXTURE
		and Vector2i(DIRTY_ROOM_TEXTURE.get_width(),
			DIRTY_ROOM_TEXTURE.get_height()) == Vector2i(1024, 576)
		and dirty_room_plate is CanvasItem)
	dirty_room_plate.queue_free()
	host.add_child(main)
	var rooms: CastleRooms25D = ROOMS_SCRIPT.new(main) as CastleRooms25D
	# ReefMain's ready path may restore the developer machine's user:// save.
	# Re-establish the probe's isolated Day One premise after mounting it.
	main._day_one_ref().day_one_active = true

	main.castle_room_id = "bubble_bath"
	var visual_layer: Node2D = Node2D.new()
	visual_layer.name = "TouchableRoomProps"
	host.add_child(visual_layer)
	main.castle_room_item_visual_layer = visual_layer

	var bathtub: Sprite2D = Sprite2D.new()
	bathtub.name = "Animated_bathtub"
	bathtub.z_index = 125
	visual_layer.add_child(bathtub)
	var fill: Sprite2D = Sprite2D.new()
	fill.name = "FixtureWater_fill"
	fill.z_index = 126
	fill.visible = false
	var material: ShaderMaterial = ShaderMaterial.new()
	material.shader = WATER_SHADER
	var clean_deep := Color(0.10, 0.50, 0.76, 1.0)
	var clean_shallow := Color(0.48, 0.90, 0.96, 1.0)
	var clean_foam := Color(0.96, 1.0, 1.0, 1.0)
	# Simulate a live fixture whose shader resource has not populated every
	# uniform yet. The implementation must retain the available deep color and
	# supply explicit clean fallbacks for the unset parameters.
	material.set_shader_parameter("deep_color", clean_deep)
	fill.material = material
	visual_layer.add_child(fill)
	main.castle_room_item_sprites["bathtub"] = {
		"sprite": bathtub,
		"fixture_rig": {"water": [{
			"role": "fill",
			"node": fill,
			"material": material,
			"flow_amount": 0.0,
		}]},
	}

	_check("fresh seam is not implicitly filled",
		not rooms.day_one_bathtub_swimmer_snapshot().get("fill_enabled", true)
		and not bool(rooms.day_one_bathtub_swimmer_snapshot().get("visible", true)))
	rooms.start_day_one_bathtub_rescue()
	await _frames(2)
	var dirty: Dictionary = rooms.day_one_bathtub_swimmer_snapshot()
	_check("dirty rescue entry fills the existing basin",
		bool(dirty.get("fill_enabled", false))
		and bool(dirty.get("filled", false))
		and bool(dirty.get("fill_water_visible", false))
		and String(dirty.get("water_state", "")) == "dirty"
		and float(dirty.get("dirty_progress", 0.0)) == 1.0)
	_check("dirty rescue reuses bounded true-2D swimmer",
		bool(dirty.get("visible", false))
		and bool(dirty.get("behind_tub_lip", false))
		and bool((dirty.get("swimmer", {}) as Dictionary).get("true_2d", false))
		and bool((dirty.get("swimmer", {}) as Dictionary).get(
			"fully_contained", false)))
	_check("dirty tint changes only the fixture fill",
		fill.modulate != Color.WHITE
		and not is_equal_approx(
			material.get_shader_parameter("deep_color").r, clean_deep.r)
		and bathtub.modulate == Color.WHITE
		and _all_canvas_items(visual_layer))

	rooms.set_day_one_bathtub_dirty_progress(0.4)
	await _frames(1)
	var partial: Dictionary = rooms.day_one_bathtub_swimmer_snapshot()
	_check("dirty progress is clamped and observable",
		is_equal_approx(float(partial.get("dirty_progress", -1.0)), 0.4)
		and bool(partial.get("visible", false))
		and String(partial.get("water_state", "")) == "dirty")

	rooms.complete_day_one_bathtub_rescue()
	await _frames(18)
	var clean: Dictionary = rooms.day_one_bathtub_swimmer_snapshot()
	_check("zero progress fades/removes swimmer but keeps clean water",
		is_equal_approx(float(clean.get("dirty_progress", -1.0)), 0.0)
		and not bool(clean.get("dirty_rescue_active", true))
		and bool(clean.get("fill_enabled", false))
		and bool(clean.get("fill_water_visible", false))
		and String(clean.get("water_state", "")) == "clean"
		and not bool(clean.get("visible", true)))
	_check("clean restoration is exact",
		fill.modulate.is_equal_approx(Color.WHITE)
		and material.get_shader_parameter("deep_color") == clean_deep
		and material.get_shader_parameter("shallow_color") == clean_shallow
		and material.get_shader_parameter("foam_color") == clean_foam
		and is_equal_approx(material.get_shader_parameter("alpha_base"), 0.24)
		and is_equal_approx(material.get_shader_parameter("turbulence"), 0.65)
		and is_equal_approx(material.get_shader_parameter("edge_foam"), 0.35))
	_check("unset live shader params use explicit clean fallbacks",
		material.get_shader_parameter("shallow_color") == clean_shallow
		and material.get_shader_parameter("foam_color") == clean_foam
		and is_equal_approx(material.get_shader_parameter("alpha_base"), 0.24)
		and is_equal_approx(material.get_shader_parameter("turbulence"), 0.65)
		and is_equal_approx(material.get_shader_parameter("edge_foam"), 0.35))
	rooms._sync_day_one_bathtub_swimmer()
	await _frames(2)
	_check("clean state does not recreate stale swimmer",
		not bool(rooms.day_one_bathtub_swimmer_snapshot().get("visible", true))
		and fill.visible)

	rooms.start_day_one_bathtub_cleanup()
	await _frames(2)
	var alias_dirty: Dictionary = rooms.day_one_bathtub_swimmer_snapshot()
	_check("cleanup alias starts the same seam exactly once",
		bool(alias_dirty.get("visible", false))
		and int(visual_layer.get_child_count()) == 3)
	rooms.close()
	await _frames(2)
	_check("close clears transient state and prevents re-entry ghosts",
		not bool(main.g.get("day_one_bathtub_filled", false))
		and rooms.day_one_bathtub_swimmer == null)

	# Release the RefCounted room owner and every local Canvas/resource handle
	# before quitting; otherwise the dummy renderer reports harmless-but-noisy
	# retained objects after all assertions have passed.
	rooms = null
	material = null
	fill = null
	bathtub = null
	visual_layer = null
	main = null
	host.queue_free()
	host = null
	await _frames(8)
	print("DAY_ONE_BATHTUB_TUB_VIGNETTE|RESULT: ",
		"PASS" if checks_failed == 0 else "FAIL",
		" checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)
