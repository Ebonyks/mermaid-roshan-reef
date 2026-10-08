extends SceneTree
const Astro := preload("res://scripts/opera_astronaut_surface.gd")
var rows: Array[Dictionary] = []
var failures := 0

func _check(label: String, value: bool) -> void:
	rows.append({"label": label, "pass": value})
	if not value:
		failures += 1

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	# Corruption/context/schema unit inputs only. The source mechanic below is
	# the actual isolated save from the earlier genuine viewport reproduction.
	var raw: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://tmp/astronaut_partial_save_repair_20261006/reef_save.json")) as Dictionary
	var main := (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	var save := SaveState.new(main, "res://tmp/astronaut_schema_unused.json")
	var legacy := save._normalise_save({"won": {}, "found": {}, "pearls": 0, "plays": 0, "future_field": {"keep": 7}})
	_check("legacy saves default Astronaut checkpoints without losing unknown fields", legacy.get("opera_astronaut_checkpoints") == {} and legacy.get("future_field") == {"keep": 7})
	_check("actual genuine save round-trips the registered checkpoint field", save._normalise_save(raw).get("opera_astronaut_checkpoints") == raw.get("opera_astronaut_checkpoints"))
	var entry: Dictionary = (raw.get("opera_astronaut_checkpoints", {}) as Dictionary).get("ordinary", {})
	var mechanic: Dictionary = entry.get("mechanic", {})
	var surface: Astro = Astro.new()
	surface.size = Vector2(852, 560)
	surface.configure("pipe", Color.WHITE, 1) # Production PIPES has no widget template/context.
	_check("actual released board-two snapshot restores valid conserved stock", surface.restore_progress(mechanic, 1.0, 3.0) and surface.pipe_round == 1 and surface.pipe_grid[0] == "SE" and not surface.held and surface.active_touch_index == -1)
	var before := surface.progress_snapshot()
	var bad := mechanic.duplicate(true)
	(bad["tray"] as Array).append("H")
	_check("duplicated pipe stock is rejected without mutating the valid board", not surface.restore_progress(bad, 1.0, 3.0) and surface.progress_snapshot() == before)
	bad = mechanic.duplicate(true)
	(bad["grid"] as Array)[4] = "H"
	_check("altered canonical fixed pipe is rejected", not surface.restore_progress(bad, 1.0, 3.0) and surface.progress_snapshot() == before)
	bad = mechanic.duplicate(true)
	bad["round"] = 1.5
	_check("fractional earned board is rejected", not surface.restore_progress(bad, 1.0, 3.0))
	bad = mechanic.duplicate(true)
	bad["context"] = "pipe_racer"
	_check("foreign mechanic identity is rejected", not surface.restore_progress(bad, 1.0, 3.0))
	var world := OperaCareerWorld2D.new()
	world.m = main
	world.career_id = "astronaut"
	world.phases = (world.PHASES["astronaut"] as Array).duplicate(true)
	world.astronaut_phase_signature = JSON.stringify(world.phases).sha256_text()
	main.save_data = raw.duplicate(true)
	_check("current ordinary phase signature finds the genuine checkpoint", not world._astronaut_saved_checkpoint().is_empty())
	world.config["chapter2_tutorial"] = true
	_check("tutorial context cannot consume ordinary earned work", world._astronaut_saved_checkpoint().is_empty())
	world.config.clear()
	world.using_chapter_two_phases = true
	world.scene_adapter = {"id": "chapter2_astronaut_rocket"}
	_check("birthday context cannot consume ordinary earned work", world._astronaut_saved_checkpoint().is_empty())
	world.using_chapter_two_phases = false
	world.surface = surface
	world.phase_index = 0
	world.phase_progress = 1.0
	var records: Dictionary = main.save_data["opera_astronaut_checkpoints"]
	(records["ordinary"] as Dictionary)["future_extra"] = {"preserve": 9}
	world._checkpoint_astronaut(false)
	records = main.save_data["opera_astronaut_checkpoints"]
	_check("updating current checkpoint preserves unknown context metadata", (records["ordinary"] as Dictionary).get("future_extra") == {"preserve": 9})
	(records["ordinary"] as Dictionary)["version"] = 2
	var preserved := records.duplicate(true)
	world._checkpoint_astronaut(false)
	_check("unsupported future checkpoint is preserved and not accepted", main.save_data["opera_astronaut_checkpoints"] == preserved and world._astronaut_saved_checkpoint().is_empty())
	print("ASTRO_SCHEMA_RESULT|", JSON.stringify({"checks": rows.size(), "failures": failures, "rows": rows, "scope": "Corruption and save-schema/context unit checks using a genuine source save. No naturally reached tutorial/birthday, native visual, device/child/owner acceptance."}))
	world.free()
	surface.free()
	main.free()
	quit(1 if failures else 0)
