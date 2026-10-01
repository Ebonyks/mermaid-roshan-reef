extends SceneTree
## Explicit static contact fixtures; no runtime binding or action acceptance.

const OUT := "res://assets_src/imagegen/day2_refinement_20261001/fit/"
const ARMS := "res://assets_src/imagegen/day2_refinement_20261001/selected/D2A-0446.png"
const PADS := "res://assets_src/imagegen/day2_refinement_20261001/selected/D2A-0447.png"
var main: ReefMain
var records: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")

func frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame

func texture(path: String) -> Texture2D:
	return ImageTexture.create_from_image(Image.load_from_file(path))

func _case(width: int, variant: String) -> void:
	root.size = Vector2i(width, 720)
	DisplayServer.window_set_size(root.size)
	await frames(3)
	var config: Dictionary = {}
	for act: Dictionary in OperaHouse.ACTS:
		if String(act.get("costume", "")) == "nursery":
			config = act.duplicate(true)
	var competition := OperaCompetition.new()
	competition.configure("nursery")
	var world := OperaCareerWorld2D.new()
	main.add_child(world)
	world.setup(main, config, competition, Callable())
	world.set_process(false)
	world.phase_index = 1
	world.active = true
	world.reveal_t = 0.0
	world.phase_advance_pending = false
	world.phase_gap = 0.0
	world._arm_phase()
	world._open_task()
	await frames(3)
	var catch: OperaNurseryCatch = world.nursery_catch
	assert(catch != null)
	catch.set_process(false)
	catch.active = false
	if variant != "original":
		catch.cradle_texture = texture(ARMS)
	if variant == "arms-and-pads":
		var atlas := AtlasTexture.new()
		atlas.atlas = texture(PADS)
		atlas.region = Rect2(6, 115, 1014, 117)
		catch.pillows_texture = atlas
	for state: String in ["contact", "safe-floor", "settled-five"]:
		catch.catcher_x = 0.5
		catch.elapsed = 0.0
		catch.input_live_t = 1.0
		catch.fallers.clear()
		catch.safe_landings.clear()
		catch.settled.clear()
		if state == "contact":
			catch.fallers.append({"x": 0.5, "y": OperaNurseryCatch.CATCH_Y, "texture": 0})
		elif state == "safe-floor":
			catch.safe_landings.append({"x": 0.3, "texture": 1, "time": 1.0})
		else:
			catch.settled.assign([0, 1, 2, 3, 4])
		catch.queue_redraw()
		await frames(2)
		await RenderingServer.frame_post_draw
		var name := "%s--%s--%dx720.webp" % [variant, state, width]
		var image: Image = root.get_texture().get_image()
		var result: Error = image.save_webp(OUT + name, false)
		records.append({"image": name, "sha256": FileAccess.get_sha256(OUT + name),
			"variant": variant, "fixture": state, "dimensions": [width, 720],
			"save_error": result, "catch_bounds": [catch.position.x, catch.position.y, catch.size.x, catch.size.y],
			"candidate_arms": ARMS if variant != "original" else "",
			"candidate_pads": PADS if variant == "arms-and-pads" else "",
			"pads_atlas_region": [6, 115, 1014, 117] if variant == "arms-and-pads" else [],
			"method": "Direct phase plus declared contact/floor/settled fixtures, processing paused, original production drawing and geometry. No runtime edit.",
			"acceptance": "STATIC_DIAGNOSTIC_ONLY; actual input/contact/owner approval pending"})
	world.close()
	world.queue_free()
	await frames(3)

func _run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	main._save_state = SaveState.new(main, "res://tmp/day2_nursery_fit_save.json")
	root.add_child(main)
	await frames(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.set_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	for width: int in [1280, 1600]:
		for variant: String in ["original", "arms-only", "arms-and-pads"]:
			await _case(width, variant)
	var file := FileAccess.open(OUT + "capture_manifest.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine": Engine.get_version_info(),
		"renderer": RenderingServer.get_current_rendering_method(), "states": records,
		"harness_sha256": FileAccess.get_sha256("res://tools/capture_day2_nursery_fit.gd"),
		"arms_sha256": FileAccess.get_sha256(ARMS), "pads_sha256": FileAccess.get_sha256(PADS),
		"runtime_integration": false, "owner_accepted": false}, "\t"))
	file.close()
	print("NURSERYFIT|captured=", records.size())
	main.queue_free()
	await frames(2)
	quit()
