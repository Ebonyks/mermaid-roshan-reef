extends SceneTree

# Focused acceptance probe for generated Sky Lagoon ambient animals.

var failures: int = 0
var main: ReefMain


func _check(label: String, condition: bool, detail: String = "") -> void:
	print("LAGOONANIMALS|%s|%s%s" % [
		label,
		"OK" if condition else "FAIL",
		"" if detail == "" else "|%s" % detail,
	])
	if not condition:
		failures += 1


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	if main.intro_active:
		main._skip_intro()
	main._apply_quality("speedy")
	main._set_night(false)
	main.save_data["lagoon_plane_departed"] = true
	main._enter_level2_now(true, false, false)
	await _frames(45)

	var promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
	var animals: Array = main.g.get("lagoon_animals", [])
	_check("roster_count", animals.size() == 5, "count=%d" % animals.size())
	var ids: Dictionary = {}
	var atlas_contract_ok: bool = true
	var render_contract_ok: bool = true
	var raccoon: Dictionary = {}
	for value in animals:
		var animal: Dictionary = value as Dictionary
		var animal_id: String = String(animal.get("id", ""))
		ids[animal_id] = true
		if animal_id == "raccoon":
			raccoon = animal
		var node: Sprite3D = animal.get("node") as Sprite3D
		var idle_texture: Texture2D = animal.get("idle_texture") as Texture2D
		var startle_texture: Texture2D = animal.get("startle_texture") as Texture2D
		atlas_contract_ok = atlas_contract_ok \
			and idle_texture != null and startle_texture != null \
			and idle_texture.get_width() == 512 and idle_texture.get_height() == 512 \
			and startle_texture.get_width() == 512 and startle_texture.get_height() == 512
		render_contract_ok = render_contract_ok \
			and node != null and not node.shaded \
			and node.hframes == 2 and node.vframes == 2 \
			and node.alpha_cut == SpriteBase3D.ALPHA_CUT_DISCARD \
			and bool(node.get_meta("living_card", false)) \
			and String(node.get_meta("ambient_kind", "")) == "animal" \
			and float(node.get_meta("touch_footprint_px", 0.0)) >= 220.0 \
			and node.get_meta("contact_shadow") is Sprite3D
	_check("expected_roster", ids.has_all(["hare", "squirrel", "raccoon", "otter", "frog"])
		and not ids.has("fawn"))
	_check("atlas_contract", atlas_contract_ok)
	_check("render_contract", render_contract_ok)
	_check("raccoon_available", not raccoon.is_empty())

	if not raccoon.is_empty():
		var raccoon_node: Sprite3D = raccoon.get("node") as Sprite3D
		var idle_x: float = raccoon_node.position.x
		promenade._tick_animals(1.0)
		_check("idle_wanders", absf(raccoon_node.position.x - idle_x) > 0.1)
		main.player.position.x = main.LEVEL2_POS.x + raccoon_node.position.x
		await _frames(12)
		var cam: Camera3D = main.player.cam
		var screen_point: Vector2 = cam.unproject_position(raccoon_node.global_position)
		_check("raccoon_on_screen", get_root().get_viewport().get_visible_rect().has_point(
			screen_point), "point=%s" % str(screen_point))
		promenade.handle_touch(screen_point)
		_check("tap_starts_cute_exit", String(raccoon.get("state", "")) == "startle"
			and raccoon_node.texture == raccoon.get("startle_texture"))
		for _step: int in range(100):
			promenade._tick_animals(0.05)
		_check("exit_leaves_screen", String(raccoon.get("state", "")) == "hidden"
			and not raccoon_node.visible)
		raccoon["hidden_t"] = 0.0
		raccoon["wait_offscreen"] = false
		promenade._tick_animals(0.05)
		_check("safe_respawn", String(raccoon.get("state", "")) == "idle"
			and raccoon_node.visible and raccoon_node.texture == raccoon.get("idle_texture"))

	print("SKY_LAGOON_ANIMALS|ALL OK" if failures == 0 \
		else "SKY_LAGOON_ANIMALS|FAIL|count=%d" % failures)
	quit(0 if failures == 0 else 1)
